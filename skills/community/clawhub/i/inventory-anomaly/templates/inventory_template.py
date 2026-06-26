import pandas as pd
import numpy as np

class InventoryManager:
    def __init__(self, data_manager):
        self.dm = data_manager
    
    def query_inventory(self, part_id):
        inventory = self.dm.get_inventory(part_id)
        current = inventory['当前库存']
        safety = inventory['安全库存']
        max_stock = inventory['最大库存']
        
        status = '正常'
        if current <= 0:
            status = '严重缺货'
        elif current < safety:
            status = '库存不足'
        
        return {
            '配件ID': part_id,
            '配件名称': self.dm.get_part_info(part_id)['配件名称'],
            '当前库存': current,
            '安全库存': safety,
            '最大库存': max_stock,
            '库存状态': status,
            '预警信息': self._get_warning_message(status, current, safety)
        }
    
    def query_all_inventory(self):
        results = []
        for part_id in self.dm.inventory['配件ID']:
            results.append(self.query_inventory(part_id))
        return results
    
    def _get_warning_message(self, status, current, safety):
        if status == '严重缺货':
            return '库存为零，急需补货！'
        elif status == '库存不足':
            shortage = safety - current
            return f'库存低于安全库存{safety}件，需补货 {shortage} 件'
        return '库存正常'