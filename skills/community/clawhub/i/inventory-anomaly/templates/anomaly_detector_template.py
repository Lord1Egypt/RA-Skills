from typing import Dict, List
import numpy as np
import pandas as pd

class AnomalyDetector:
    def __init__(self, data_manager):
        self.dm = data_manager
    
    def detect_inventory_anomalies(self) -> List[Dict]:
        anomalies = []
        
        for part_id in self.dm.inventory['配件ID']:
            inventory = self.dm.get_inventory(part_id)
            if not inventory:
                continue
            
            current_stock = inventory['当前库存']
            safety_stock = inventory['安全库存']
            
            if current_stock <= 0:
                anomalies.append({
                    '配件ID': part_id,
                    '异常类型': '严重缺货',
                    '当前库存': current_stock,
                    '安全库存': safety_stock,
                    '严重程度': '高',
                    '建议': '立即补货'
                })
            elif current_stock < safety_stock:
                shortage = safety_stock - current_stock
                anomalies.append({
                    '配件ID': part_id,
                    '异常类型': '库存不足',
                    '当前库存': current_stock,
                    '安全库存': safety_stock,
                    '严重程度': '中',
                    '建议': f'需补货 {shortage} 件'
                })
        
        return anomalies
    
    def detect_demand_anomalies(self, days: int = 90) -> List[Dict]:
        anomalies = []
        
        for part_id in self.dm.inventory['配件ID']:
            orders = self.dm.get_part_orders(part_id)
            if orders.empty:
                continue
            
            orders = orders.sort_values('日期')
            
            weekly_demand = self._calculate_weekly_demand(orders)
            
            if len(weekly_demand) < 4:
                continue
            
            mean_demand = np.mean(weekly_demand)
            std_demand = np.std(weekly_demand)
            
            if std_demand == 0:
                continue
            
            latest_week_demand = weekly_demand[-1]
            
            threshold = 3 * std_demand
            
            if latest_week_demand > mean_demand + threshold:
                anomaly_ratio = (latest_week_demand - mean_demand) / std_demand
                anomalies.append({
                    '配件ID': part_id,
                    '异常类型': '需求异常跳升',
                    '最新周需求': int(latest_week_demand),
                    '平均周需求': round(mean_demand, 2),
                    '标准差': round(std_demand, 2),
                    '异常倍数': round(anomaly_ratio, 2),
                    '严重程度': self._get_severity(anomaly_ratio),
                    '建议': '需求异常增加，建议增加备货'
                })
        
        return anomalies
    
    def detect_all_anomalies(self, days: int = 90) -> Dict[str, List[Dict]]:
        inventory_anomalies = self.detect_inventory_anomalies()
        demand_anomalies = self.detect_demand_anomalies(days)
        
        return {
            '库存异常': inventory_anomalies,
            '需求异常': demand_anomalies,
            '总计': len(inventory_anomalies) + len(demand_anomalies)
        }
    
    def _calculate_weekly_demand(self, orders: pd.DataFrame) -> List[float]:
        orders['周'] = orders['日期'].dt.isocalendar().week
        orders['年'] = orders['日期'].dt.isocalendar().year
        orders['年周'] = orders['年'].astype(str) + '-' + orders['周'].astype(str).str.zfill(2)
        
        weekly_demand = orders.groupby('年周')['数量'].sum().values
        return weekly_demand.tolist()
    
    def _get_severity(self, anomaly_ratio: float) -> str:
        if anomaly_ratio >= 5:
            return '极高'
        elif anomaly_ratio >= 4:
            return '高'
        elif anomaly_ratio >= 3:
            return '中'
        else:
            return '低'