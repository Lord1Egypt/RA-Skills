#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300晨间多因子投研系统 - 市场环境判断模块
升级新增：市场情绪、趋势判断、仓位建议
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)


class MarketRegimeDetector:
    """市场环境检测器"""
    
    def __init__(self):
        self.regimes = ['BULL', 'BULL_STRONG', 'NEUTRAL', 'BEAR', 'BEAR_STRONG', 'VOLATILE']
    
    def analyze_trend(self, index_df, ma_short=20, ma_mid=60, ma_long=120):
        """
        分析指数趋势
        
        Args:
            index_df: 指数日线DataFrame
            ma_short: 短期均线周期
            ma_mid: 中期均线周期
            ma_long: 长期均线周期
        
        Returns:
            dict: 趋势分析结果
        """
        if index_df is None or len(index_df) < ma_long:
            return {'trend': 'UNKNOWN', 'strength': 0}
        
        df = index_df.copy()
        close = df['close']
        
        # 计算均线
        ma_short_val = close.rolling(ma_short).mean().iloc[-1]
        ma_mid_val = close.rolling(ma_mid).mean().iloc[-1]
        ma_long_val = close.rolling(ma_long).mean().iloc[-1]
        current_price = close.iloc[-1]
        
        # 趋势强度得分
        trend_score = 0
        
        # 价格与均线位置
        if current_price > ma_short_val:
            trend_score += 1
        if current_price > ma_mid_val:
            trend_score += 1
        if current_price > ma_long_val:
            trend_score += 2
        
        # 均线排列
        if ma_short_val > ma_mid_val > ma_long_val:
            trend_score += 2  # 多头排列
        elif ma_short_val < ma_mid_val < ma_long_val:
            trend_score -= 2  # 空头排列
        
        # 均线方向
        ma_short_prev = close.rolling(ma_short).mean().iloc[-5]
        ma_mid_prev = close.rolling(ma_mid).mean().iloc[-5]
        if ma_short_val > ma_short_prev:
            trend_score += 1
        if ma_mid_val > ma_mid_prev:
            trend_score += 1
        
        # 判断趋势类型
        if trend_score >= 6:
            trend = 'BULL_STRONG'
        elif trend_score >= 3:
            trend = 'BULL'
        elif trend_score >= 0:
            trend = 'NEUTRAL'
        elif trend_score >= -2:
            trend = 'BEAR'
        else:
            trend = 'BEAR_STRONG'
        
        return {
            'trend': trend,
            'trend_score': trend_score,
            'ma_short': ma_short_val,
            'ma_mid': ma_mid_val,
            'ma_long': ma_long_val,
            'current_price': current_price
        }
    
    def analyze_momentum(self, index_df):
        """
        分析市场动量
        
        Args:
            index_df: 指数日线DataFrame
        
        Returns:
            dict: 动量分析结果
        """
        if index_df is None or len(index_df) < 60:
            return {'momentum': 'UNKNOWN'}
        
        close = index_df['close']
        
        # 不同周期的涨跌幅
        ret_5d = (close.iloc[-1] - close.iloc[-6]) / close.iloc[-6] if len(close) > 5 else 0
        ret_20d = (close.iloc[-1] - close.iloc[-21]) / close.iloc[-21] if len(close) > 20 else 0
        ret_60d = (close.iloc[-1] - close.iloc[-61]) / close.iloc[-61] if len(close) > 60 else 0
        
        # 动量得分
        momentum_score = ret_5d * 0.3 + ret_20d * 0.4 + ret_60d * 0.3
        
        # 判断动量状态
        if momentum_score > 0.05:
            momentum = 'STRONG_UP'
        elif momentum_score > 0:
            momentum = 'UP'
        elif momentum_score > -0.05:
            momentum = 'DOWN'
        else:
            momentum = 'STRONG_DOWN'
        
        return {
            'momentum': momentum,
            'momentum_score': momentum_score,
            'return_5d': ret_5d,
            'return_20d': ret_20d,
            'return_60d': ret_60d
        }
    
    def analyze_volatility(self, index_df, window=20):
        """
        分析市场波动率
        
        Args:
            index_df: 指数日线DataFrame
            window: 波动率计算窗口
        
        Returns:
            dict: 波动率分析结果
        """
        if index_df is None or len(index_df) < window + 1:
            return {'volatility_regime': 'UNKNOWN'}
        
        returns = index_df['close'].pct_change().dropna()
        current_vol = returns.tail(window).std() * np.sqrt(252)
        avg_vol = returns.std() * np.sqrt(252)
        
        vol_ratio = current_vol / avg_vol if avg_vol > 0 else 1
        
        if vol_ratio > 1.5:
            vol_regime = 'HIGH_VOL'
        elif vol_ratio > 0.8:
            vol_regime = 'NORMAL'
        else:
            vol_regime = 'LOW_VOL'
        
        return {
            'volatility_regime': vol_regime,
            'annualized_volatility': current_vol,
            'volatility_ratio': vol_ratio
        }
    
    def calculate_market_temperature(self, stocks_data, factors_df):
        """
        计算市场温度
        
        Args:
            stocks_data: 所有股票数据
            factors_df: 因子DataFrame
        
        Returns:
            dict: 市场温度指标
        """
        temperature = 50  # 基准温度50度
        
        # 指标1: 涨跌比
        if 'pct_chg' in factors_df.columns:
            up_count = len(factors_df[factors_df['pct_chg'] > 0])
            down_count = len(factors_df[factors_df['pct_chg'] < 0])
            if up_count + down_count > 0:
                up_ratio = up_count / (up_count + down_count)
                temperature += (up_ratio - 0.5) * 40  # 全涨加20，全跌减20
        
        # 指标2: MACD金叉比例
        if 'macd_golden' in factors_df.columns:
            gold_ratio = factors_df['macd_golden'].mean()
            temperature += (gold_ratio - 0.3) * 30  # 金叉超过30%加分
        
        # 指标3: 均线多头排列比例
        if 'bullish_alignment' in factors_df.columns:
            bull_ratio = factors_df['bullish_alignment'].mean()
            temperature += bull_ratio * 20
        
        # 指标4: 综合得分分布
        if 'composite_score' in factors_df.columns:
            avg_score = factors_df['composite_score'].mean()
            temperature += avg_score * 15
        
        # 指标5: 均线位置
        if 'price_to_ma20' in factors_df.columns:
            above_ma_ratio = (factors_df['price_to_ma20'] > 0).mean()
            temperature += (above_ma_ratio - 0.5) * 20
        
        # 限制在0-100范围内
        temperature = max(0, min(100, temperature))
        
        # 温度解读
        if temperature >= 80:
            interpretation = '🔥 过热（谨慎追高）'
        elif temperature >= 60:
            interpretation = '☀️ 偏热（适当加仓）'
        elif temperature >= 40:
            interpretation = '🌤️ 正常（保持仓位）'
        elif temperature >= 20:
            interpretation = '⛅ 偏冷（谨慎操作）'
        else:
            interpretation = '❄️ 过冷（观望为主）'
        
        return {
            'temperature': round(temperature, 1),
            'interpretation': interpretation,
            'up_ratio': up_ratio if 'up_ratio' in dir() else None,
            'gold_cross_ratio': gold_ratio if 'gold_ratio' in dir() else None
        }
    
    def get_position_suggestion(self, regime_analysis):
        """
        根据市场环境给出仓位建议
        
        Args:
            regime_analysis: 市场环境分析结果
        
        Returns:
            dict: 仓位建议
        """
        trend = regime_analysis.get('trend', {}).get('trend', 'NEUTRAL')
        vol = regime_analysis.get('volatility', {}).get('volatility_regime', 'NORMAL')
        temperature = regime_analysis.get('temperature', {}).get('temperature', 50)
        
        # 基础仓位
        base_position = {
            'BULL_STRONG': 0.8,
            'BULL': 0.7,
            'NEUTRAL': 0.5,
            'BEAR': 0.3,
            'BEAR_STRONG': 0.15
        }
        
        suggested_position = base_position.get(trend, 0.5)
        
        # 根据波动率调整
        if vol == 'HIGH_VOL':
            suggested_position *= 0.7  # 高波动率降低仓位
        elif vol == 'LOW_VOL':
            suggested_position *= 1.1  # 低波动率可适当增加
        
        # 根据市场温度微调
        if temperature > 80:
            suggested_position *= 0.8  # 过热减仓
        elif temperature < 20:
            suggested_position *= 0.8  # 过冷也减仓（等待机会）
        
        return {
            'suggested_total_position': round(suggested_position, 2),
            'single_stock_max': round(suggested_position / 5, 3),
            'regime': trend,
            'volatility': vol
        }
    
    def comprehensive_analysis(self, index_df, stocks_data=None, factors_df=None):
        """
        综合市场环境分析
        
        Args:
            index_df: 指数日线数据
            stocks_data: 股票数据字典
            factors_df: 因子DataFrame
        
        Returns:
            dict: 完整的市场分析报告
        """
        analysis = {
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'trend': self.analyze_trend(index_df),
            'momentum': self.analyze_momentum(index_df),
            'volatility': self.analyze_volatility(index_df)
        }
        
        # 如果有股票数据，计算市场温度
        if stocks_data is not None and factors_df is not None:
            analysis['market_temperature'] = self.calculate_market_temperature(stocks_data, factors_df)
        
        # 仓位建议
        analysis['position_suggestion'] = self.get_position_suggestion(analysis)
        
        # 生成总体市场状态描述
        trend_desc = {
            'BULL_STRONG': '强势多头',
            'BULL': '多头',
            'NEUTRAL': '震荡中性',
            'BEAR': '空头',
            'BEAR_STRONG': '强势空头',
            'UNKNOWN': '未知'
        }
        
        vol_desc = {
            'HIGH_VOL': '高波动',
            'NORMAL': '正常波动',
            'LOW_VOL': '低波动',
            'UNKNOWN': '未知'
        }
        
        analysis['market_summary'] = (
            f"{trend_desc.get(analysis['trend']['trend'], '未知')} "
            f"{vol_desc.get(analysis['volatility']['volatility_regime'], '')}"
        )
        
        logger.info(f"市场环境分析完成: {analysis['market_summary']}")
        
        return analysis


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    # 测试市场环境检测器
    detector = MarketRegimeDetector()
    
    # 创建模拟指数数据
    dates = pd.date_range('2024-01-01', periods=150, freq='D')
    prices = 3000 + np.cumsum(np.random.randn(150) * 20)
    
    test_index = pd.DataFrame({
        'date': dates,
        'close': prices,
        'volume': [100000000 + np.random.randint(-5000000, 5000000) for _ in range(150)]
    })
    
    # 进行分析
    analysis = detector.comprehensive_analysis(test_index)
    
    print("=" * 50)
    print("市场环境分析报告")
    print("=" * 50)
    print(f"市场状态: {analysis['market_summary']}")
    print(f"趋势得分: {analysis['trend']['trend_score']}")
    print(f"年化波动率: {analysis['volatility']['annualized_volatility']:.2%}")
    print(f"建议仓位: {analysis['position_suggestion']['suggested_total_position']:.0%}")
    print(f"单股上限: {analysis['position_suggestion']['single_stock_max']:.1%}")
    print("=" * 50)
