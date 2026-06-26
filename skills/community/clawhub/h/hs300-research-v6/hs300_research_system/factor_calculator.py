#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300晨间多因子投研系统 - 因子计算模块
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime

from config import FACTOR_CONFIG, TECH_PARAMS

logger = logging.getLogger(__name__)


class FactorCalculator:
    """因子计算类"""
    
    def __init__(self):
        self.tech_params = TECH_PARAMS
    
    def calculate_ma(self, df, periods=None):
        """计算移动平均线"""
        if periods is None:
            periods = self.tech_params['ma_periods']
        
        result = {}
        for period in periods:
            if len(df) >= period:
                ma = df['close'].rolling(window=period).mean()
                result[f'ma{period}'] = ma.iloc[-1]
                # 计算价格相对于MA的位置
                result[f'price_to_ma{period}'] = df['close'].iloc[-1] / ma.iloc[-1] - 1
            else:
                result[f'ma{period}'] = np.nan
                result[f'price_to_ma{period}'] = np.nan
        
        return result
    
    def calculate_macd(self, df):
        """计算MACD"""
        fast = self.tech_params['macd_fast']
        slow = self.tech_params['macd_slow']
        signal = self.tech_params['macd_signal']
        
        if len(df) < slow:
            return {'macd': np.nan, 'macd_signal': np.nan, 'macd_hist': np.nan, 'macd_golden': False}
        
        ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        hist = macd_line - signal_line
        
        # 检测金叉死叉
        golden_cross = False
        if len(hist) >= 2:
            if hist.iloc[-2] < 0 and hist.iloc[-1] > 0:
                golden_cross = True
        
        return {
            'macd': macd_line.iloc[-1],
            'macd_signal': signal_line.iloc[-1],
            'macd_hist': hist.iloc[-1],
            'macd_golden': golden_cross,
            'macd_death': hist.iloc[-2] > 0 and hist.iloc[-1] < 0 if len(hist) >= 2 else False
        }
    
    def calculate_rsi(self, df, period=None):
        """计算RSI"""
        if period is None:
            period = self.tech_params['rsi_period']
        
        if len(df) < period + 1:
            return {'rsi': np.nan, 'rsi_overbought': False, 'rsi_oversold': False}
        
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = (-delta).where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        current_rsi = rsi.iloc[-1]
        
        return {
            'rsi': current_rsi,
            'rsi_overbought': current_rsi > 70,
            'rsi_oversold': current_rsi < 30
        }
    
    def calculate_kdj(self, df):
        """计算KDJ"""
        n = self.tech_params['kdj_n']
        m1 = self.tech_params['kdj_m1']
        m2 = self.tech_params['kdj_m2']
        
        if len(df) < n:
            return {'k': np.nan, 'd': np.nan, 'j': np.nan, 'kdj_golden': False}
        
        low_list = df['low'].rolling(n, min_periods=1).min()
        high_list = df['high'].rolling(n, min_periods=1).max()
        rsv = (df['close'] - low_list) / (high_list - low_list) * 100
        
        k = rsv.ewm(com=m1 - 1, adjust=False).mean()
        d = k.ewm(com=m2 - 1, adjust=False).mean()
        j = 3 * k - 2 * d
        
        # 金叉检测
        golden_cross = False
        if len(k) >= 2:
            if k.iloc[-2] < d.iloc[-2] and k.iloc[-1] > d.iloc[-1]:
                golden_cross = True
        
        return {
            'kdj_k': k.iloc[-1],
            'kdj_d': d.iloc[-1],
            'kdj_j': j.iloc[-1],
            'kdj_golden': golden_cross,
            'kdj_overbought': k.iloc[-1] > 80,
            'kdj_oversold': k.iloc[-1] < 20
        }
    
    def calculate_momentum(self, df):
        """计算动量因子"""
        result = {}
        close_prices = df['close']
        
        # 不同周期的收益率
        periods = {'return_1m': 20, 'return_3m': 60, 'return_6m': 120, 'return_12m': 240}
        
        for name, period in periods.items():
            if len(df) >= period:
                result[name] = close_prices.iloc[-1] / close_prices.iloc[-period] - 1
            else:
                result[name] = np.nan
        
        # 计算相对强弱（相对于沪深300的超额收益）- 这里简化处理
        result['momentum_score'] = result.get('return_1m', 0) * 0.4 + result.get('return_3m', 0) * 0.6
        
        return result
    
    def calculate_volatility(self, df):
        """计算波动率因子"""
        result = {}
        
        returns = df['close'].pct_change().dropna()
        
        # 不同周期的波动率
        periods = {'std_1m': 20, 'std_3m': 60}
        
        for name, period in periods.items():
            if len(returns) >= period:
                result[name] = returns.tail(period).std() * np.sqrt(252)  # 年化波动率
            else:
                result[name] = np.nan
        
        # 计算最大回撤
        if len(df) >= 20:
            prices = df['close'].tail(60)
            rolling_max = prices.expanding().max()
            drawdown = prices / rolling_max - 1
            result['max_drawdown_1m'] = drawdown.min()
        else:
            result['max_drawdown_1m'] = np.nan
        
        return result
    
    def calculate_volume_factor(self, df):
        """计算成交量因子"""
        if len(df) < 10:
            return {'volume_ratio': np.nan, 'volume_trend': 0}
        
        volume = df['volume']
        current_vol = volume.iloc[-1]
        avg_vol_20 = volume.tail(20).mean() if len(volume) >= 20 else volume.mean()
        
        volume_ratio = current_vol / avg_vol_20
        
        # 成交量趋势
        vol_ma5 = volume.tail(5).mean()
        vol_ma10 = volume.tail(10).mean()
        volume_trend = vol_ma5 / vol_ma10 - 1 if vol_ma10 > 0 else 0
        
        return {
            'volume_ratio': volume_ratio,
            'volume_trend': volume_trend,
            'volume_increasing': volume_ratio > 1.2
        }
    
    def calculate_trend_factor(self, df):
        """计算趋势因子"""
        result = {}
        
        if len(df) < 60:
            return result
        
        close = df['close']
        
        # MA排列
        ma5 = close.rolling(5).mean().iloc[-1]
        ma10 = close.rolling(10).mean().iloc[-1]
        ma20 = close.rolling(20).mean().iloc[-1]
        ma60 = close.rolling(60).mean().iloc[-1]
        
        # 多头排列判断
        bullish_alignment = (ma5 > ma10) and (ma10 > ma20) and (ma20 > ma60)
        bearish_alignment = (ma5 < ma10) and (ma10 < ma20) and (ma20 < ma60)
        
        result['bullish_alignment'] = bullish_alignment
        result['bearish_alignment'] = bearish_alignment
        
        # 趋势强度分数
        trend_score = 0
        if ma5 > ma10: trend_score += 1
        if ma10 > ma20: trend_score += 1
        if ma20 > ma60: trend_score += 1
        result['trend_score'] = trend_score
        
        # 价格位置（相对于最近60天的位置）
        prices_60 = close.tail(60)
        price_position = (close.iloc[-1] - prices_60.min()) / (prices_60.max() - prices_60.min()) if prices_60.max() != prices_60.min() else 0.5
        result['price_position_60d'] = price_position
        
        return result
    
    def calculate_valuation_factors(self, stock_code, current_price):
        """
        计算估值因子
        由于真实估值数据需要额外接口，这里提供一个基于价格的相对估值
        """
        # 简化的估值因子：基于历史价格的相对位置
        result = {
            'pe': np.nan,  # 需要真实PE数据
            'pb': np.nan,  # 需要真实PB数据
            'price_to_52week_high': np.nan,  # 相对52周高点的位置
            'price_to_52week_low': np.nan     # 相对52周低点的位置
        }
        
        return result
    
    def calculate_all_factors(self, stock_data):
        """
        计算单只股票的所有因子
        
        Args:
            stock_data: 股票数据字典，包含 'name', 'code', 'daily'
        
        Returns:
            dict: 包含所有因子的字典
        """
        df = stock_data['daily']
        
        if df is None or len(df) < 30:
            logger.warning(f"股票 {stock_data['name']} 数据不足，跳过因子计算")
            return None
        
        result = {
            'code': stock_data['code'],
            'name': stock_data['name'],
            'date': df['date'].iloc[-1],
            'close_price': df['close'].iloc[-1],
            'pct_chg': df['pct_chg'].iloc[-1] if 'pct_chg' in df.columns else 0
        }
        
        # 计算各类因子
        result.update(self.calculate_ma(df))
        result.update(self.calculate_macd(df))
        result.update(self.calculate_rsi(df))
        result.update(self.calculate_kdj(df))
        result.update(self.calculate_momentum(df))
        result.update(self.calculate_volatility(df))
        result.update(self.calculate_volume_factor(df))
        result.update(self.calculate_trend_factor(df))
        
        return result
    
    def calculate_factor_score(self, factors_df):
        """
        计算综合因子得分
        
        Args:
            factors_df: 所有股票的因子DataFrame
        
        Returns:
            DataFrame: 带有综合得分的因子DataFrame
        """
        df = factors_df.copy()
        
        # 定义各因子的方向（正向还是负向）
        factor_directions = {
            # 动量因子（正向）
            'return_1m': 1, 'return_3m': 1, 'return_6m': 1,
            
            # 技术因子
            'trend_score': 1,  # 趋势得分越高越好
            'price_position_60d': 1,
            'macd_golden': 1,  # 金叉加分
            'kdj_golden': 1,
            
            # 波动率（负向，波动小好）
            'std_1m': -1, 'std_3m': -1,
            'max_drawdown_1m': -1,  # 最大回撤（负向，因为是负数，所以需要调整）
            
            # RSI（适中为好，这里简化处理）
            'rsi': 0,  # 单独处理
            
            # 成交量
            'volume_ratio': 1,  # 放量上涨加分
        }
        
        # 计算得分（先进行标准化）
        score_columns = []
        
        for col, direction in factor_directions.items():
            if col in df.columns and direction != 0:
                # 标准化（Z-score）
                valid_data = df[col].dropna()
                if len(valid_data) > 0:
                    mean_val = valid_data.mean()
                    std_val = valid_data.std()
                    if std_val > 0:
                        z_score = (df[col] - mean_val) / std_val
                        df[f'{col}_score'] = z_score * direction
                        score_columns.append(f'{col}_score')
        
        # 特殊处理RSI（50左右最好，太高太低都不好）
        if 'rsi' in df.columns:
            df['rsi_distance'] = abs(df['rsi'] - 50)
            valid_data = df['rsi_distance'].dropna()
            if len(valid_data) > 0:
                mean_val = valid_data.mean()
                std_val = valid_data.std()
                if std_val > 0:
                    z_score = (df['rsi_distance'] - mean_val) / std_val
                    df['rsi_score'] = -z_score  # 距离越小得分越高
                    score_columns.append('rsi_score')
        
        # 计算综合得分
        if score_columns:
            df['composite_score'] = df[score_columns].mean(axis=1)
            
            # 对有金叉信号的股票额外加分
            if 'macd_golden' in df.columns:
                df.loc[df['macd_golden'] == True, 'composite_score'] += 0.3
            if 'kdj_golden' in df.columns:
                df.loc[df['kdj_golden'] == True, 'composite_score'] += 0.2
            if 'bullish_alignment' in df.columns:
                df.loc[df['bullish_alignment'] == True, 'composite_score'] += 0.3
        else:
            df['composite_score'] = 0
        
        return df


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    from data_fetcher import DataFetcher
    
    fetcher = DataFetcher()
    calculator = FactorCalculator()
    
    # 获取几只股票测试
    stocks = fetcher.get_hs300_stocks()
    if stocks:
        test_stocks = stocks[:3]
        all_factors = []
        
        for stock in test_stocks:
            print(f"\n计算 {stock['name']}({stock['code']}) 的因子...")
            
            daily_data = fetcher.get_stock_daily(stock['code'])
            if daily_data is not None:
                stock_data = {
                    'code': stock['code'],
                    'name': stock['name'],
                    'daily': daily_data
                }
                
                factors = calculator.calculate_all_factors(stock_data)
                if factors:
                    all_factors.append(factors)
                    print(f"  计算完成，因子数量: {len(factors)}")
        
        if all_factors:
            factors_df = pd.DataFrame(all_factors)
            print("\n因子数据前5列:")
            print(factors_df.head())
            
            # 计算综合得分
            scored_df = calculator.calculate_factor_score(factors_df)
            print("\n综合得分排名:")
            print(scored_df[['code', 'name', 'composite_score']].sort_values('composite_score', ascending=False))
