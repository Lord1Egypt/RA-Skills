import pandas as pd
import numpy as np
from pathlib import Path

class DataManager:
    def __init__(self, excel_path):
        self.excel_path = Path(excel_path)
        self._load_data()
    
    def _load_data(self):
        self.parts_info = pd.read_excel(self.excel_path, sheet_name='配件信息')
        self.inventory = pd.read_excel(self.excel_path, sheet_name='库存')
        self.orders = pd.read_excel(self.excel_path, sheet_name='订单历史')
        
        self.orders['日期'] = pd.to_datetime(self.orders['日期'])
    
    def get_part_info(self, part_id):
        return self.parts_info[self.parts_info['配件ID'] == part_id].to_dict('records')[0]
    
    def get_inventory(self, part_id):
        return self.inventory[self.inventory['配件ID'] == part_id].to_dict('records')[0]
    
    def get_part_orders(self, part_id):
        return self.orders[self.orders['配件ID'] == part_id].copy()
    
    def save_data(self):
        with pd.ExcelWriter(self.excel_path, engine='openpyxl') as writer:
            self.parts_info.to_excel(writer, sheet_name='配件信息', index=False)
            self.inventory.to_excel(writer, sheet_name='库存', index=False)
            self.orders.to_excel(writer, sheet_name='订单历史', index=False)