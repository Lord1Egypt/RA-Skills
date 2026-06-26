import pandas as pd
import numpy as np

class DemandCalculator:
    def __init__(self, data_manager):
        self.dm = data_manager
    
    def calculate_demand(self, part_id, days=30):
        orders = self.dm.get_part_orders(part_id)
        orders = orders[orders['日期'] >= (pd.Timestamp.now() - pd.Timedelta(days=days))]
        
        if orders.empty:
            return {
                '配件ID': part_id,
                '日均需求': 0,
                '周均需求': 0,
                '月均需求': 0
            }
        
        daily_demand = orders.groupby(orders['日期'].dt.date)['数量'].sum().mean()
        weekly_demand = daily_demand * 7
        monthly_demand = daily_demand * 30
        
        return {
            '配件ID': part_id,
            '日均需求': round(daily_demand, 2),
            '周均需求': round(weekly_demand, 2),
            '月均需求': round(monthly_demand, 2)
        }
    
    def calculate_all_demands(self, days=30):
        results = []
        for part_id in self.dm.inventory['配件ID']:
            results.append(self.calculate_demand(part_id, days))
        return results
    
    def calculate_replenishment(self, part_id, days=30):
        demand = self.calculate_demand(part_id, days)
        inventory = self.dm.get_inventory(part_id)
        
        current = inventory['当前库存']
        safety = inventory['安全库存']
        monthly_demand = demand['月均需求']
        
        shortage = max(0, safety - current)
        recommended = max(safety, monthly_demand) - current
        
        return {
            '配件ID': part_id,
            '当前库存': current,
            '安全库存': safety,
            '月均需求': monthly_demand,
            '缺货数量': shortage,
            '建议补货数量': recommended
        }
    
    def calculate_all_replenishments(self, days=30):
        results = []
        for part_id in self.dm.inventory['配件ID']:
            results.append(self.calculate_replenishment(part_id, days))
        return results