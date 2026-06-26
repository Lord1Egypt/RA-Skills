#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300晨间多因子投研系统 - 风险管理模块
升级新增：黑名单过滤、风险预警、持仓跟踪
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RiskManager:
    """风险管理类"""
    
    def __init__(self):
        self.blacklist_rules = {
            'st_stock': True,           # 排除ST股票
            'suspend': True,             # 排除停牌
            'abnormal_volume': True,     # 排除成交量异常
            'excessive_gain': True,      # 排除短期涨幅过大
            'insufficient_data': True    # 排除数据不足
        }
    
    def filter_blacklist(self, stock_data, df_daily=None):
        """
        黑名单过滤
        
        Args:
            stock_data: 股票数据字典 {'code': '', 'name': '', 'daily': df}
            df_daily: 日线数据（可选，如果stock_data已有则不需要）
        
        Returns:
            tuple: (is_filtered, filter_reason)
        """
        code = stock_data.get('code', '')
        name = stock_data.get('name', '')
        
        if df_daily is None:
            df_daily = stock_data.get('daily')
        
        if df_daily is None or len(df_daily) < 30:
            return True, '数据不足'
        
        # 规则1: ST/*ST股票过滤
        if self.blacklist_rules['st_stock']:
            if 'ST' in name or '*ST' in name or '退' in name:
                logger.info(f"黑名单过滤: {name}({code}) - ST股票")
                return True, 'ST股票'
        
        # 规则2: 停牌检查（成交量为0或接近0）
        if self.blacklist_rules['suspend']:
            recent_vol = df_daily['volume'].tail(5)
            if (recent_vol == 0).sum() >= 3:
                logger.info(f"黑名单过滤: {name}({code}) - 连续停牌")
                return True, '停牌中'
        
        # 规则3: 短期涨幅过大（近20日涨幅>30%）
        if self.blacklist_rules['excessive_gain'] and len(df_daily) >= 20:
            price_20d_ago = df_daily['close'].iloc[-20]
            price_now = df_daily['close'].iloc[-1]
            gain_20d = (price_now - price_20d_ago) / price_20d_ago
            if gain_20d > 0.3:
                logger.info(f"黑名单过滤: {name}({code}) - 20日涨幅{gain_20d*100:.1f}%过大")
                return True, '短期涨幅过大'
        
        # 规则4: 成交量异常（近5日成交量波动过大）
        if self.blacklist_rules['abnormal_volume'] and len(df_daily) >= 20:
            vol_5d = df_daily['volume'].tail(5).mean()
            vol_20d = df_daily['volume'].tail(20).mean()
            if vol_20d > 0 and vol_5d / vol_20d > 5:
                logger.info(f"黑名单过滤: {name}({code}) - 成交量异常放大")
                return True, '成交量异常'
        
        return False, '正常'
    
    def batch_filter_stocks(self, all_stocks_data):
        """
        批量过滤股票
        
        Args:
            all_stocks_data: 所有股票数据字典 {code: {name, daily}}
        
        Returns:
            tuple: (filtered_data, filter_report)
        """
        filtered_data = {}
        filter_report = {
            'total': len(all_stocks_data),
            'filtered': 0,
            'passed': 0,
            'reasons': {}
        }
        
        for code, stock_data in all_stocks_data.items():
            is_filtered, reason = self.filter_blacklist(stock_data)
            
            if is_filtered:
                filter_report['filtered'] += 1
                filter_report['reasons'][reason] = filter_report['reasons'].get(reason, 0) + 1
            else:
                filtered_data[code] = stock_data
                filter_report['passed'] += 1
        
        logger.info(f"黑名单过滤完成：总数{filter_report['total']}只，通过{filter_report['passed']}只，过滤{filter_report['filtered']}只")
        logger.info(f"过滤原因分布: {filter_report['reasons']}")
        
        return filtered_data, filter_report
    
    def calculate_risk_score(self, factors_df):
        """
        计算个股风险得分
        
        Args:
            factors_df: 因子DataFrame
        
        Returns:
            DataFrame: 带有风险得分的DataFrame
        """
        df = factors_df.copy()
        risk_scores = []
        
        for _, row in df.iterrows():
            score = 0
            
            # 波动率风险（分数越低风险越高）
            std_1m = row.get('std_1m', 0.02)
            if std_1m > 0.05:
                score += 2
            elif std_1m > 0.03:
                score += 1
            
            # 最大回撤风险
            max_dd = row.get('max_drawdown_1m', -0.05)
            if max_dd < -0.15:
                score += 2
            elif max_dd < -0.1:
                score += 1
            
            # RSI超买
            rsi = row.get('rsi', 50)
            if rsi > 80:
                score += 2
            elif rsi > 70:
                score += 1
            
            # 均线空头排列
            bearish = row.get('bearish_alignment', False)
            if bearish:
                score += 1
            
            risk_scores.append(score)
        
        df['risk_score'] = risk_scores
        df['risk_level'] = pd.cut(df['risk_score'], 
                                   bins=[-1, 1, 3, 10],
                                   labels=['低风险', '中风险', '高风险'])
        
        return df
    
    def position_sizing_suggestion(self, stock_row, market_env='neutral'):
        """
        给出仓位建议
        
        Args:
            stock_row: 单只股票的因子数据
            market_env: 市场环境 (bull, neutral, bear)
        
        Returns:
            dict: 仓位建议
        """
        risk_level = stock_row.get('risk_level', '中风险')
        composite_score = stock_row.get('composite_score', 0)
        
        # 基础仓位
        base_position = {
            'bull': 0.15,      # 牛市单只最高15%
            'neutral': 0.10,   # 震荡市单只最高10%
            'bear': 0.05       # 熊市单只最高5%
        }
        
        max_position = base_position.get(market_env, 0.10)
        
        # 根据得分调整
        if composite_score > 1.0:
            suggested = min(max_position, max_position)
        elif composite_score > 0.5:
            suggested = max_position * 0.7
        elif composite_score > 0:
            suggested = max_position * 0.4
        else:
            suggested = 0
        
        # 根据风险等级调整
        if risk_level == '高风险':
            suggested = suggested * 0.5
        elif risk_level == '低风险':
            suggested = suggested * 1.2
        
        return {
            'suggested_position': round(suggested, 3),
            'risk_level': risk_level,
            'stop_loss_pct': -0.08 if risk_level == '高风险' else -0.05
        }


class PortfolioManager:
    """组合管理类"""
    
    def __init__(self):
        self.historical_recommendations = []
        self.performance_record = []
    
    def add_recommendation(self, rec_date, recommendations):
        """
        记录推荐股票
        
        Args:
            rec_date: 推荐日期
            recommendations: 推荐股票列表 [{'code': '', 'name': '', 'score': 0, 'price': 0}]
        """
        self.historical_recommendations.append({
            'date': rec_date,
            'stocks': recommendations
        })
    
    def calculate_performance(self, rec_date, current_prices):
        """
        计算历史推荐表现
        
        Args:
            rec_date: 推荐日期
            current_prices: 当前价格字典 {code: price}
        
        Returns:
            dict: 表现统计
        """
        for rec in self.historical_recommendations:
            if rec['date'] == rec_date:
                returns = []
                for stock in rec['stocks']:
                    code = stock['code']
                    if code in current_prices:
                        ret = (current_prices[code] - stock['price']) / stock['price']
                        returns.append({
                            'code': code,
                            'name': stock['name'],
                            'entry_price': stock['price'],
                            'current_price': current_prices[code],
                            'return': ret
                        })
                
                if returns:
                    avg_return = np.mean([r['return'] for r in returns])
                    win_rate = sum(1 for r in returns if r['return'] > 0) / len(returns)
                    
                    performance = {
                        'date': rec_date,
                        'stock_count': len(returns),
                        'avg_return': avg_return,
                        'win_rate': win_rate,
                        'details': returns
                    }
                    self.performance_record.append(performance)
                    return performance
        
        return None


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    # 测试风险管理
    rm = RiskManager()
    
    # 测试黑名单过滤
    test_stock = {
        'code': '600000',
        'name': '浦发银行',
        'daily': pd.DataFrame({
            'close': [10 + i*0.01 for i in range(50)],
            'volume': [10000000 + i*10000 for i in range(50)]
        })
    }
    
    is_filtered, reason = rm.filter_blacklist(test_stock)
    print(f"测试股票过滤结果: {is_filtered}, 原因: {reason}")
    
    # 测试ST股票
    st_stock = {
        'code': '600001',
        'name': '*ST测试',
        'daily': test_stock['daily']
    }
    
    is_filtered, reason = rm.filter_blacklist(st_stock)
    print(f"ST股票过滤结果: {is_filtered}, 原因: {reason}")
