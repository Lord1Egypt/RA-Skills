"""
技术指标测试
"""

import unittest
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/market-data-hub/src')

from indicators import (
    calculate_ma,
    calculate_macd,
    calculate_rsi,
    calculate_bollinger_bands,
    calculate_kdj
)


class TestMovingAverage(unittest.TestCase):
    """移动平均线测试"""
    
    def test_calculate_sma(self):
        """测试简单移动平均线"""
        df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
        result = calculate_ma(df, periods=[3])
        
        # 验证第3个值 (10+11+12)/3 = 11
        self.assertAlmostEqual(result['MA3'].iloc[2], 11.0)
    
    def test_calculate_ema(self):
        """测试指数移动平均线"""
        df = pd.DataFrame({'close': [10, 11, 12, 13, 14, 15]})
        result = calculate_ma(df, periods=[3], ma_type='ema')
        
        self.assertIn('EMA3', result.columns)
        # EMA会给予近期数据更高权重
        self.assertGreater(result['EMA3'].iloc[-1], result['EMA3'].iloc[0])
    
    def test_multiple_periods(self):
        """测试多周期计算"""
        df = pd.DataFrame({'close': range(100)})
        result = calculate_ma(df, periods=[5, 10, 20, 60])
        
        self.assertIn('MA5', result.columns)
        self.assertIn('MA10', result.columns)
        self.assertIn('MA20', result.columns)
        self.assertIn('MA60', result.columns)


class TestMACD(unittest.TestCase):
    """MACD指标测试"""
    
    def test_calculate_macd(self):
        """测试MACD计算"""
        # 生成上升走势
        df = pd.DataFrame({'close': range(30)})
        result = calculate_macd(df)
        
        self.assertIn('MACD_DIF', result.columns)
        self.assertIn('MACD_DEA', result.columns)
        self.assertIn('MACD_HIST', result.columns)
    
    def test_golden_cross(self):
        """测试金叉信号"""
        # 创建金叉场景：DIF从低于DEA变成高于DEA
        df = pd.DataFrame({'close': [10] * 26 + [11] * 10})
        result = calculate_macd(df)
        
        self.assertIn('MACD_golden_cross', result.columns)
    
    def test_death_cross(self):
        """测试死叉信号"""
        # 创建死叉场景：DIF从高于DEA变成低于DEA
        df = pd.DataFrame({'close': [20] * 26 + [19] * 10})
        result = calculate_macd(df)
        
        self.assertIn('MACD_death_cross', result.columns)


class TestRSI(unittest.TestCase):
    """RSI指标测试"""
    
    def test_calculate_rsi(self):
        """测试RSI计算"""
        df = pd.DataFrame({'close': [10, 12, 11, 13, 12, 14, 13, 15, 14, 16]})
        result = calculate_rsi(df, period=6)
        
        self.assertIn('RSI', result.columns)
        # RSI应在0-100之间
        for val in result['RSI'].dropna():
            self.assertTrue(0 <= val <= 100)
    
    def test_overbought_signal(self):
        """测试超买信号"""
        # 连续上涨，应该产生超买信号
        df = pd.DataFrame({'close': [10] + [10 + i * 0.5 for i in range(1, 21)]})
        result = calculate_rsi(df, period=6)
        
        self.assertIn('RSI_overbought', result.columns)
        # 最后应该有超买信号或高RSI值
        self.assertTrue(any(result['RSI_overbought']) or result['RSI'].iloc[-1] > 50)
    
    def test_oversold_signal(self):
        """测试超卖信号"""
        # 连续下跌，应该产生超卖信号
        df = pd.DataFrame({'close': [20] + [20 - i * 0.5 for i in range(1, 21)]})
        result = calculate_rsi(df, period=6)
        
        self.assertIn('RSI_oversold', result.columns)


class TestBollingerBands(unittest.TestCase):
    """布林带指标测试"""
    
    def test_calculate_bollinger_bands(self):
        """测试布林带计算"""
        np.random.seed(42)
        df = pd.DataFrame({'close': 100 + np.random.randn(30).cumsum()})
        result = calculate_bollinger_bands(df, period=20)
        
        self.assertIn('BB_MIDDLE', result.columns)
        self.assertIn('BB_UPPER', result.columns)
        self.assertIn('BB_LOWER', result.columns)
    
    def test_band_relationship(self):
        """测试布林带上下轨关系"""
        np.random.seed(42)
        df = pd.DataFrame({'close': 100 + np.random.randn(50).cumsum()})
        result = calculate_bollinger_bands(df, period=20)
        
        # 验证上轨 >= 中轨 >= 下轨
        for i in range(19, len(result)):
            self.assertGreaterEqual(result['BB_UPPER'].iloc[i], result['BB_MIDDLE'].iloc[i])
            self.assertGreaterEqual(result['BB_MIDDLE'].iloc[i], result['BB_LOWER'].iloc[i])
    
    def test_percent_b(self):
        """测试%B指标"""
        np.random.seed(42)
        df = pd.DataFrame({'close': 100 + np.random.randn(30).cumsum()})
        result = calculate_bollinger_bands(df, period=20)
        
        self.assertIn('BB_percent_b', result.columns)


class TestKDJ(unittest.TestCase):
    """KDJ指标测试"""
    
    def test_calculate_kdj(self):
        """测试KDJ计算"""
        df = pd.DataFrame({
            'high': [12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
            'low': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
            'close': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        })
        result = calculate_kdj(df, n_period=9)
        
        self.assertIn('KDJ_K', result.columns)
        self.assertIn('KDJ_D', result.columns)
        self.assertIn('KDJ_J', result.columns)
    
    def test_kdj_range(self):
        """测试KDJ数值范围"""
        df = pd.DataFrame({
            'high': [12, 13, 14, 15, 16, 17, 18, 19, 20, 21] * 5,
            'low': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17] * 5,
            'close': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19] * 5
        })
        result = calculate_kdj(df, n_period=9)
        
        # K和D应该在0-100范围内（除初始值外）
        for i in range(1, len(result)):
            self.assertTrue(0 <= result['KDJ_K'].iloc[i] <= 100)
            self.assertTrue(0 <= result['KDJ_D'].iloc[i] <= 100)
    
    def test_cross_signals(self):
        """测试交叉信号"""
        df = pd.DataFrame({
            'high': [12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
            'low': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
            'close': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        })
        result = calculate_kdj(df, n_period=9)
        
        self.assertIn('KDJ_golden_cross', result.columns)
        self.assertIn('KDJ_death_cross', result.columns)


if __name__ == '__main__':
    unittest.main(verbosity=2)
