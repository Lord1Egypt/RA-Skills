#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股历史数据选股器（已更新：仅返回胜率最高的1只股票）
使用前一日收盘数据在盘前选股
"""
import os
import sys
import json
import requests
from datetime import datetime, timedelta
import time
import random

class HKHistoricalPicker:
    """港股历史数据选股器"""
    
    def __init__(self):
        """初始化"""
        self.output_dir = "output/signals"
        self.trades_dir = "output/trades"
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.trades_dir, exist_ok=True)
        
        # 股票池
        self.stock_pool = [
            {"code": "09988.HK", "name": "阿里巴巴-SW"},
            {"code": "00700.HK", "name": "腾讯控股"},
            {"code": "03690.HK", "name": "美团-W"},
            {"code": "01810.HK", "name": "小米集团-W"},
            {"code": "02318.HK", "name": "中国平安"},
            {"code": "00941.HK", "name": "中国移动"},
            {"code": "01299.HK", "name": "友邦保险"},
            {"code": "00005.HK", "name": "汇丰控股"},
            {"code": "00388.HK", "name": "香港交易所"},
            {"code": "02628.HK", "name": "中国人寿"}
        ]
    
    def get_historical_data(self, code, date=None):
        """获取历史数据"""
        if date is None:
            date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # 模拟数据（实际使用时替换为真实API）
        base_prices = {
            "09988.HK": 130.0,
            "00700.HK": 510.0,
            "03690.HK": 74.0,
            "01810.HK": 31.5,
            "02318.HK": 45.0,
            "00941.HK": 68.0,
            "01299.HK": 85.0,
            "00005.HK": 60.0,
            "00388.HK": 250.0,
            "02628.HK": 12.0
        }
        
        base_price = base_prices.get(code, 50.0)
        change_pct = random.uniform(-3.0, 3.0)
        price = base_price * (1 + change_pct / 100)
        open_price = price * (1 + random.uniform(-0.02, 0.02))
        high_price = max(price, open_price) * (1 + random.uniform(0, 0.03))
        low_price = min(price, open_price) * (1 - random.uniform(0, 0.03))
        volume = random.randint(1000000, 10000000)
        amp = (high_price - low_price) / price * 100
        
        return {
            "code": code,
            "date": date,
            "price": round(price, 3),
            "change_pct": round(change_pct, 2),
            "open": round(open_price, 3),
            "high": round(high_price, 3),
            "low": round(low_price, 3),
            "volume": volume,
            "amp": round(amp, 2)
        }
    
    def calculate_score(self, data):
        """基于历史数据计算评分"""
        if not data:
            return 0
        
        score = 0
        price = data.get('price', 0)
        change_pct = data.get('change_pct', 0)
        amp = data.get('amp', 0)
        volume = data.get('volume', 0)
        
        # 涨跌幅评分 (0-30分)
        if -1.5 <= change_pct <= 1.0:
            score += 25
        elif 1.0 < change_pct <= 2.5:
            score += 18
        elif -2.5 <= change_pct < -1.5:
            score += 15
        elif change_pct > 2.5:
            score += 10
        elif change_pct < -2.5:
            score += 8
        else:
            score += 12
        
        # 波动性评分 (0-25分)
        if 1.5 <= amp <= 3.5:
            score += 20
        elif 1.0 <= amp < 1.5:
            score += 15
        elif 3.5 < amp <= 5.0:
            score += 12
        elif amp > 5.0:
            score += 8
        else:
            score += 10
        
        # 流动性评分 (0-20分)
        if volume > 5000000:
            score += 20
        elif volume > 2000000:
            score += 15
        elif volume > 1000000:
            score += 10
        else:
            score += 5
        
        # 价格合理性评分 (0-15分)
        if 10 <= price <= 500:
            score += 10
        elif price < 1 or price > 1000:
            score -= 10
        
        # 数据完整性评分 (0-10分)
        required_fields = ['price', 'change_pct', 'amp', 'volume']
        complete_fields = sum(1 for field in required_fields if field in data and data[field] is not None)
        score += min(complete_fields * 2.5, 10)
        
        return max(0, min(100, score))
    
    def calculate_trading_prices(self, data, score):
        """基于历史数据计算交易价格"""
        if not data:
            return None
        
        price = data.get('price', 0)
        amp = data.get('amp', 0)
        
        if price <= 0:
            return None
        
        atr_pct = max(amp / 100, 0.015)
        
        # 根据评分调整风险收益比
        if score >= 80:
            target_gain_pct = atr_pct * 0.7
            stop_loss_pct = atr_pct * 0.35
        elif score >= 70:
            target_gain_pct = atr_pct * 0.6
            stop_loss_pct = atr_pct * 0.4
        elif score >= 60:
            target_gain_pct = atr_pct * 0.5
            stop_loss_pct = atr_pct * 0.5
        else:
            target_gain_pct = atr_pct * 0.4
            stop_loss_pct = atr_pct * 0.6
        
        buy_discount = 0.0075
        buy_price = round(price * (1 - buy_discount), 3)
        sell_target = round(buy_price * (1 + target_gain_pct), 3)
        stop_loss = round(buy_price * (1 - stop_loss_pct), 3)
        
        return {
            'buy_price': buy_price,
            'sell_target': sell_target,
            'stop_loss': stop_loss,
            'target_gain_pct': round(target_gain_pct * 100, 2),
            'stop_loss_pct': round(stop_loss_pct * 100, 2),
            'risk_reward_ratio': round(target_gain_pct / stop_loss_pct, 2) if stop_loss_pct > 0 else 0
        }
    
    def select_best_stocks(self, top_n=1):
        """选择最佳股票（默认仅返回胜率最高的1只）"""
        print("=" * 60)
        print("港股历史数据选股")
        print("=" * 60)
        print(f"选股时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"使用数据: 前一日收盘数据")
        print(f"选股规则: 仅返回评分最高的{top_n}只股票")
        print()
        
        scored_stocks = []
        
        for stock in self.stock_pool:
            code = stock['code']
            name = stock['name']
            
            data = self.get_historical_data(code)
            if not data:
                continue
            
            score = self.calculate_score(data)
            if score <= 0:
                continue
            
            prices = self.calculate_trading_prices(data, score)
            if not prices:
                continue
            
            stock_info = {
                'code': code,
                'name': name,
                'score': score,
                'historical_data': data,
                'trading_prices': prices,
                'selection_reason': f"历史数据评分: {score}/100，昨日涨跌幅{data['change_pct']}%，振幅{data['amp']}%"
            }
            
            scored_stocks.append(stock_info)
            print(f"📊 {code} {name}: {score}分")
        
        scored_stocks.sort(key=lambda x: x['score'], reverse=True)
        best_stocks = scored_stocks[:top_n]
        
        print()
        print(f"✅ 评分完成: {len(scored_stocks)} 只股票获得有效评分")
        print(f"🏆 选择最佳股票: {best_stocks[0]['code']} {best_stocks[0]['name']} (评分: {best_stocks[0]['score']}/100)")
        
        return best_stocks
    
    def generate_trading_plan(self, stock_info):
        """生成交易计划"""
        data = stock_info['historical_data']
        prices = stock_info['trading_prices']
        
        plan = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'stock_code': stock_info['code'],
            'stock_name': stock_info['name'],
            'score': stock_info['score'],
            'buy_price': prices['buy_price'],
            'sell_target': prices['sell_target'],
            'stop_loss': prices['stop_loss'],
            'target_gain_pct': prices['target_gain_pct'],
            'stop_loss_pct': prices['stop_loss_pct'],
            'risk_reward_ratio': prices['risk_reward_ratio'],
            'selection_reason': stock_info['selection_reason'],
            'execution_time': {
                'buy_window': "09:30-10:00",
                'sell_window': "14:30-15:00",
                'stop_loss_execution': "触发即执行"
            },
            'position_sizing': {
                'suggested_position': "2-3% of capital",
                'max_position': "5% of capital"
            }
        }
        
        return plan
    
    def save_plan(self, plan):
        """保存交易计划"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"plan_{timestamp}.json"
        filepath = os.path.join(self.trades_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        
        print(f"📁 交易计划已保存: {filename}")
        return filepath
    
    def save_signal(self, plan):
        """保存选股信号"""
        date_str = datetime.now().strftime('%Y%m%d')
        filename = f"{date_str}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        signal = {
            'date': plan['date'],
            'time': plan['time'],
            'stock_code': plan['stock_code'],
            'stock_name': plan['stock_name'],
            'current_price': plan['historical_data']['price'],
            'change_pct': plan['historical_data']['change_pct'],
            'amp': plan['historical_data']['amp'],
            'volume': plan['historical_data']['volume'],
            'score': plan['score'],
            'buy_price': plan['buy_price'],
            'sell_target': plan['sell_target'],
            'stop_loss': plan['stop_loss'],
            'target_gain_pct': plan['target_gain_pct'],
            'stop_loss_pct': plan['stop_loss_pct'],
            'risk_reward_ratio': plan['risk_reward_ratio'],
            'selection_reason': plan['selection_reason'],
            'execution_time': plan['execution_time'],
            'position_sizing': plan['position_sizing']
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(signal, f, ensure_ascii=False, indent=2)
        
        print(f"📁 选股信号已保存: {filename}")
        return filepath
    
    def run(self):
        """执行选股流程"""
        try:
            best_stocks = self.select_best_stocks(top_n=1)
            if not best_stocks:
                print("❌ 没有选出符合条件的股票")
                return False
            
            for stock in best_stocks:
                plan = self.generate_trading_plan(stock)
                self.save_plan(plan)
                self.save_signal(plan)
                
                print()
                print("🎯 最终选股结果:")
                print(f"股票代码: {plan['stock_code']}")
                print(f"股票名称: {plan['stock_name']}")
                print(f"评分: {plan['score']}/100")
                print(f"买入价: {plan['buy_price']}港元")
                print(f"目标卖出: {plan['sell_target']}港元 (+{plan['target_gain_pct']}%)")
                print(f"止损价: {plan['stop_loss']}港元 (-{plan['stop_loss_pct']}%)")
                print(f"风险收益比: {plan['risk_reward_ratio']}:1")
                print(f"选股理由: {plan['selection_reason']}")
            
            print()
            print("✅ 选股流程执行完成")
            return True
            
        except Exception as e:
            print(f"❌ 选股流程执行失败: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    picker = HKHistoricalPicker()
    success = picker.run()
    sys.exit(0 if success else 1)
