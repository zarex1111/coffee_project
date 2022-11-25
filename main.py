from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QDialog
from PyQt5 import uic
import sys
import sqlite3


class Program(QWidget):

    def __init__(self):
        
        super().__init__()
        uic.loadUi('design.ui', self)

        self.drinks_columns = ['id', 'Название', 'Содержание молока (%)', 'Вид молока',
            'Зёрна (id)', 'Содержание кофе (%)', 'Сахар (г)', 'Цена (руб)', 'Объём (мл)', 'Способ приготовления', 'Другое']
        self.seeds_columns = ['id', 'Название сорта', 'Обжарка', 'Вид', 'Вкус', 'Цена (руб)', 'Объём пачки (мл)']

        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()

        self.update_drinks_table()
        self.update_seeds_table()
    
    def update_drinks_table(self):
        data = self._get_drinks_data()
        self.tableWidget.setColumnCount(len(self.drinks_columns))
        self.tableWidget.setHorizontalHeaderLabels(self.drinks_columns)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, item in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))
        self.tableWidget.resizeColumnsToContents()

        self.tableWidget.cellActivated.connect(self.open_dialog)
    
    def open_dialog(self, row, column):
        if column == 4:
            item = self.tableWidget.item(row, column).text()
            d = seed_info(int(item))
            d.exec_()
        

    def _get_drinks_data(self):
        return self.cur.execute('''SELECT * FROM Drinks''').fetchall()

    def update_seeds_table(self):
        data = self.cur.execute('SELECT * FROM Type').fetchall()
        self.tableWidget_2.setColumnCount(len(self.seeds_columns))
        self.tableWidget_2.setHorizontalHeaderLabels(self.seeds_columns)
        self.tableWidget_2.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget_2.setRowCount(self.tableWidget.rowCount() + 1)
            for j, item in enumerate(row):
                self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(item)))
        self.tableWidget_2.resizeColumnsToContents()


class seed_info(QDialog):

    def __init__(self, seed_id):
        super().__init__()
        uic.loadUi('seed_info.ui', self)

        self.s = seed_id
        self.set_table()

        self.pushButton.clicked.connect(self.close)
    
    def set_table(self):
        seed = p.cur.execute(f'''SELECT * FROM Type
    WHERE id={self.s}''').fetchall()
        seed = seed[0]
        self.tableWidget.setColumnCount(len(p.seeds_columns))
        self.tableWidget.setHorizontalHeaderLabels(p.seeds_columns)
        self.tableWidget.setRowCount(1)
        for i, item in enumerate(seed):
            self.tableWidget.setItem(0, i, QTableWidgetItem(str(item)))
        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    p = Program()
    p.show()
    sys.exit(app.exec())