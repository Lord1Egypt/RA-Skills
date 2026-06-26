from typing import Dict, List
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')

class DemandPredictor:
    def __init__(self, data_manager):
        self.dm = data_manager
    
    def predict_weekly_demand(self, part_id, weeks_ahead: int = 4) -> Dict:
        orders = self.dm.get_part_orders(part_id)
        
        if orders.empty or len(orders) < 12:
            return {
                '配件ID': part_id,
                '预测状态': '失败',
                '失败原因': '数据不足'
            }
        
        try:
            weekly_demand = self._prepare_weekly_data(orders)
            
            if len(weekly_demand) < 8:
                return {
                    '配件ID': part_id,
                    '预测状态': '失败',
                    '失败原因': '历史数据不足'
                }
            
            model = ARIMA(weekly_demand, order=(1,1,0))
            model_fit = model.fit()
            
            forecast = model_fit.forecast(steps=weeks_ahead)
            forecast = [max(0, x) for x in forecast]
            
            historical_mean = np.mean(weekly_demand)
            historical_std = np.std(weekly_demand)
            
            anomalies = []
            for i, pred in enumerate(forecast):
                if historical_std > 0:
                    z_score = (pred - historical_mean) / historical_std
                    if abs(z_score) > 3:
                        anomalies.append({
                            '预测周次': i + 1,
                            '预测需求': int(pred),
                            '历史均值': round(historical_mean, 2),
                            'Z分数': round(z_score, 2),
                            '异常类型': '需求异常跳升' if pred > historical_mean else '需求异常下降'
                        })
            
            return {
                '配件ID': part_id,
                '预测状态': '成功',
                '预测需求': [int(x) for x in forecast],
                '异常提醒': anomalies
            }
        
        except Exception as e:
            return {
                '配件ID': part_id,
                '预测状态': '失败',
                '失败原因': f'模型拟合失败: {str(e)}'
            }
    
    def predict_all_demands(self, weeks_ahead: int = 4) -> List[Dict]:
        results = []
        for part_id in self.dm.inventory['配件ID']:
            results.append(self.predict_weekly_demand(part_id, weeks_ahead))
        return results
    
    def get_urgent_replenishment_list(self, weeks_ahead: int = 4) -> List[Dict]:
        urgent_items = []
        
        for part_id in self.dm.inventory['配件ID']:
            prediction = self.predict_weekly_demand(part_id, weeks_ahead)
            
            if prediction['预测状态'] != '成功':
                continue
            
            total_forecast = sum(prediction['预测需求'])
            inventory = self.dm.get_inventory(part_id)
            current = inventory['当前库存']
            safety = inventory['安全库存']
            
            gap = max(0, safety + total_forecast - current)
            
            if gap > 0:
                urgent_items.append({
                    '配件ID': part_id,
                    '缺口': gap
                })
        
        return urgent_items
    
    def _prepare_weekly_data(self, orders: pd.DataFrame) -> List[float]:
        orders['周'] = orders['日期'].dt.isocalendar().week
        orders['年'] = orders['日期'].dt.isocalendar().year
        orders['年周'] = orders['年'].astype(str) + '-' + orders['周'].astype(str).str.zfill(2)
        
        weekly_demand = orders.groupby('年周')['数量'].sum().values
        return weekly_demand.tolist()