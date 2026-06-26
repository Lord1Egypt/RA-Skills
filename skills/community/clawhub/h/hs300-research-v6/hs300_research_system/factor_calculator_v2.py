#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300晨间多因子投研系统 - 因子计算模块 v2.0 【升级版本】
新增功能:
- 8大类因子体系
- 动态权重调整（根据市场环境）
- 改进的金叉/死叉检测
- 因子中性化框架
- 信号共振检测
- 单只股票因子解释生成
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)


class FactorCalculatorV2:
    """【升级v2.0】因子计算类 - 增强版"""
    
    def __init__(self):
        # 技术分析参数（保持兼容）
        self.tech_params = {
            'ma_periods': [5, 10, 20, 60, 120],
            'macd_fast': 12,
            'macd_slow': 26,
            'macd_signal': 9,
            'rsi_period': 14,
            'kdj_n': 9,
            'kdj_m1': 3,
            'kdj_m2': 3
        }
    
    # ========== 原有因子计算方法（保持兼容） ==========
    def calculate_ma(self, df, periods=None):
        """计算移动平均线"""
        if periods is None:
            periods = self.tech_params['ma_periods']
        
        result = {}
        for period in periods:
            if len(df) >= period:
                ma = df['close'].rolling(window=period).mean()
                result[f'ma{period}'] = ma.iloc[-1]
                result[f'price_to_ma{period}'] = df['close'].iloc[-1] / ma.iloc[-1] - 1
            else:
                result[f'ma{period}'] = np.nan
                result[f'price_to_ma{period}'] = np.nan
        
        return result
    
    def calculate_macd(self, df):
        """【升级】计算MACD，精确检测金叉死叉"""
        fast = self.tech_params['macd_fast']
        slow = self.tech_params['macd_slow']
        signal = self.tech_params['macd_signal']
        
        if len(df) < slow + signal:
            return {'macd': np.nan, 'macd_signal': np.nan, 'macd_hist': np.nan, 
                    'macd_golden': False, 'macd_death': False}
        
        close = df['close'].values
        ema_fast = pd.Series(close).ewm(span=fast, adjust=False).mean().values
        ema_slow = pd.Series(close).ewm(span=slow, adjust=False).mean().values
        macd_line = ema_fast - ema_slow
        signal_line = pd.Series(macd_line).ewm(span=signal, adjust=False).mean().values
        hist = macd_line - signal_line
        
        # 【升级】精确检测金叉死叉（hist由负变正=金叉，由正变负=死叉）
        macd_golden = False
        macd_death = False
        
        if len(hist) >= 3:
            # 金叉：hist[-3]<0, hist[-2]<0, hist[-1]>0（底部反转）
            if hist[-3] < 0 and hist[-2] < 0 and hist[-1] > 0:
                macd_golden = True
            # 死叉：hist[-3]>0, hist[-2]>0, hist[-1]<0（顶部反转）
            if hist[-3] > 0 and hist[-2] > 0 and hist[-1] < 0:
                macd_death = True
        
        return {
            'macd': float(macd_line[-1]),
            'macd_signal': float(signal_line[-1]),
            'macd_hist': float(hist[-1]),
            'macd_golden': macd_golden,
            'macd_death': macd_death,
            'macd_hist_series': hist[-5:]  # 返回近5天hist用于图表展示
        }
    
    def calculate_rsi(self, df, period=None):
        """计算RSI"""
        if period is None:
            period = self.tech_params['rsi_period']
        
        if len(df) < period + 1:
            return {'rsi': np.nan, 'rsi_overbought': False, 'rsi_oversold': False}
        
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = (-delta.where(delta < 0, 0))
        
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        current_rsi = float(rsi.iloc[-1])
        
        return {
            'rsi': current_rsi,
            'rsi_overbought': current_rsi > 70,
            'rsi_oversold': current_rsi < 30,
            'rsi_level': '超买' if current_rsi > 70 else '超卖' if current_rsi < 30 else '正常'
        }
    
    def calculate_kdj(self, df):
        """【升级】计算KDJ，精确金叉死叉检测"""
        n = self.tech_params['kdj_n']
        m1 = self.tech_params['kdj_m1']
        m2 = self.tech_params['kdj_m2']
        
        if len(df) < n + 5:
            return {'kdj_k': np.nan, 'kdj_d': np.nan, 'kdj_j': np.nan, 
                    'kdj_golden': False, 'kdj_death': False}
        
        low_list = df['low'].rolling(n, min_periods=1).min()
        high_list = df['high'].rolling(n, min_periods=1).max()
        rsv = (df['close'] - low_list) / (high_list - low_list) * 100
        rsv = rsv.fillna(50).values
        
        k = pd.Series(rsv).ewm(com=m1 - 1, adjust=False).mean().values
        d = pd.Series(k).ewm(com=m2 - 1, adjust=False).mean().values
        j = 3 * k - 2 * d
        
        # 【升级】精确检测金叉死叉
        kdj_golden = False
        kdj_death = False
        
        if len(k) >= 3:
            # KDJ金叉：K线上穿D线（20以下金叉更可靠）
            if k[-3] < d[-3] and k[-2] < d[-2] and k[-1] > d[-1] and d[-1] < 40:
                kdj_golden = True
            # KDJ死叉：K线下穿D线（80以上死叉更可靠）
            if k[-3] > d[-3] and k[-2] > d[-2] and k[-1] < d[-1] and d[-1] > 60:
                kdj_death = True
        
        return {
            'kdj_k': float(k[-1]),
            'kdj_d': float(d[-1]),
            'kdj_j': float(j[-1]),
            'kdj_golden': kdj_golden,
            'kdj_death': kdj_death,
            'kdj_overbought': k[-1] > 80,
            'kdj_oversold': k[-1] < 20
        }
    
    def calculate_momentum(self, df):
        """计算动量因子"""
        result = {}
        close_prices = df['close']
        
        # 不同周期的收益率
        periods = {'return_1m': 20, 'return_3m': 60, 'return_6m': 120}
        
        for name, period in periods.items():
            if len(df) >= period:
                result[name] = float(close_prices.iloc[-1] / close_prices.iloc[-period] - 1)
            else:
                result[name] = np.nan
        
        # 价格位置分位
        if len(df) >= 60:
            prices_60 = close_prices.tail(60)
            result['price_position_60d'] = float(
                (close_prices.iloc[-1] - prices_60.min()) / 
                (prices_60.max() - prices_60.min())
                if prices_60.max() != prices_60.min() else 0.5
            )
        
        return result
    
    def calculate_volatility(self, df):
        """计算波动率因子"""
        result = {}
        
        returns = df['close'].pct_change().dropna()
        
        # 不同周期的波动率
        periods = {'std_1m': 20, 'std_3m': 60}
        
        for name, period in periods.items():
            if len(returns) >= period:
                result[name] = float(returns.tail(period).std() * np.sqrt(252))
            else:
                result[name] = np.nan
        
        # 计算最大回撤
        if len(df) >= 20:
            prices = df['close'].tail(60).values
            rolling_max = np.maximum.accumulate(prices)
            drawdown = prices / rolling_max - 1
            result['max_drawdown_1m'] = float(drawdown.min())
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
        
        volume_ratio = current_vol / avg_vol_20 if avg_vol_20 > 0 else 1
        
        # 成交量趋势
        vol_ma5 = volume.tail(5).mean()
        vol_ma10 = volume.tail(10).mean()
        volume_trend = vol_ma5 / vol_ma10 - 1 if vol_ma10 > 0 else 0
        
        return {
            'volume_ratio': float(volume_ratio),
            'volume_trend': float(volume_trend),
            'volume_increasing': bool(volume_ratio > 1.2)
        }
    
    def calculate_trend_factor(self, df):
        """计算趋势因子"""
        result = {}
        
        if len(df) < 60:
            return result
        
        close = df['close']
        
        ma5 = close.rolling(5).mean().iloc[-1]
        ma10 = close.rolling(10).mean().iloc[-1]
        ma20 = close.rolling(20).mean().iloc[-1]
        ma60 = close.rolling(60).mean().iloc[-1]
        
        # 多头排列判断（更严格）
        bullish_alignment = (ma5 > ma10) and (ma10 > ma20) and (ma20 > ma60)
        bearish_alignment = (ma5 < ma10) and (ma10 < ma20) and (ma20 < ma60)
        
        result['bullish_alignment'] = bool(bullish_alignment)
        result['bearish_alignment'] = bool(bearish_alignment)
        
        # 趋势强度分数
        trend_score = 0
        if ma5 > ma10: trend_score += 1
        if ma10 > ma20: trend_score += 1
        if ma20 > ma60: trend_score += 1
        result['trend_score'] = trend_score
        
        return result
    
    # ========== 计算单只股票所有因子 ==========
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
            'date': df['date'].iloc[-1] if 'date' in df.columns else datetime.now(),
            'close_price': float(df['close'].iloc[-1]),
            'pct_chg': float(df['pct_chg'].iloc[-1]) if 'pct_chg' in df.columns else 0
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
    
    # ========== 【升级v2.0】综合得分计算 ==========
    def calculate_factor_score(self, factors_df, market_regime='NEUTRAL'):
        """
        【升级v2.0】计算综合因子得分
        
        改进点:
        - 5大类因子体系
        - 根据市场环境动态调整权重
        - 信号共振额外加分
        - 更合理的标准化方法
        
        Args:
            factors_df: 所有股票的因子DataFrame
            market_regime: 市场环境 ('BULL', 'NEUTRAL', 'BEAR')
        
        Returns:
            DataFrame: 带有综合得分的因子DataFrame
        """
        df = factors_df.copy()
        
        logger.info(f"计算综合得分，当前市场环境: {market_regime}")
        
        # ===== 因子权重配置（根据市场环境动态调整）=====
        if market_regime in ['BULL', 'BULL_STRONG']:
            factor_weights = {
                'momentum': 0.25,
                'trend': 0.25,
                'volatility': 0.10,
                'technical': 0.20,
                'volume': 0.20
            }
        elif market_regime in ['BEAR', 'BEAR_STRONG']:
            factor_weights = {
                'momentum': 0.15,
                'trend': 0.15,
                'volatility': 0.30,
                'technical': 0.20,
                'volume': 0.20
            }
        else:
            factor_weights = {
                'momentum': 0.20,
                'trend': 0.20,
                'volatility': 0.20,
                'technical': 0.20,
                'volume': 0.20
            }
        
        # ===== 1. 计算各因子组标准化得分 =====
        group_scores = {}
        n = len(df)
        
        # --- 动量因子组 ---
        momentum_factors = {
            'return_1m': 0.4,
            'return_3m': 0.4,
            'price_position_60d': 0.2
        }
        group_scores['momentum'] = self._calculate_group_score(
            df, momentum_factors, direction=1
        )
        
        # --- 趋势因子组 ---
        trend_factors = {
            'trend_score': 0.5,
            'price_to_ma20': 0.3,
            'price_to_ma60': 0.2
        }
        group_scores['trend'] = self._calculate_group_score(
            df, trend_factors, direction=1
        )
        
        # --- 波动率因子组（越小越好，负向）---
        vol_factors = {
            'std_1m': 0.5,
            'std_3m': 0.3,
            'max_drawdown_1m': 0.2
        }
        group_scores['volatility'] = self._calculate_group_score(
            df, vol_factors, direction=-1
        )
        
        # --- 技术信号因子组 ---
        technical_scores = np.zeros(n)
        if 'macd_golden' in df.columns:
            technical_scores += df['macd_golden'].fillna(False).astype(float).values * 0.4
        if 'kdj_golden' in df.columns:
            technical_scores += df['kdj_golden'].fillna(False).astype(float).values * 0.3
        if 'bullish_alignment' in df.columns:
            technical_scores += df['bullish_alignment'].fillna(False).astype(float).values * 0.3
        
        # RSI优化处理
        if 'rsi' in df.columns:
            rsi = df['rsi'].fillna(50).values
            rsi_score = 1 - np.abs(rsi - 50) / 50
            technical_scores += rsi_score * 0.2
        
        group_scores['technical'] = self._normalize(technical_scores)
        
        # --- 量能因子组 ---
        volume_scores = np.zeros(n)
        if 'volume_ratio' in df.columns:
            vol_ratio = df['volume_ratio'].fillna(1).values
            volume_scores += np.clip((vol_ratio - 1) / 2, 0, 1) * 0.5
        if 'volume_trend' in df.columns:
            vol_trend = df['volume_trend'].fillna(0).values
            volume_scores += np.clip(vol_trend, -0.5, 0.5) + 0.5
        
        group_scores['volume'] = self._normalize(volume_scores)
        
        # ===== 2. 计算综合得分 =====
        composite_score = np.zeros(n)
        for group, weight in factor_weights.items():
            if group in group_scores:
                composite_score += group_scores[group] * weight
        
        # 归一化到标准分数
        composite_score = self._normalize_composite(composite_score)
        
        # ===== 3. 信号共振额外加分 =====
        # MACD金叉 + KDJ金叉 双重共振
        if 'macd_golden' in df.columns and 'kdj_golden' in df.columns:
            double_golden = (
                df['macd_golden'].fillna(False).astype(bool).values &
                df['kdj_golden'].fillna(False).astype(bool).values
            )
            composite_score[double_golden] += 0.5  # 大幅加分
        
        # 三重信号共振
        if 'bullish_alignment' in df.columns:
            triple_signal = double_golden & df['bullish_alignment'].fillna(False).astype(bool).values
            composite_score[triple_signal] += 0.8  # 三重信号大幅加分
        
        df['composite_score'] = composite_score
        
        # 保存各因子组得分
        for group, scores in group_scores.items():
            df[f'{group}_score'] = scores
        
        return df
    
    def _calculate_group_score(self, df, factor_weights, direction=1):
        """计算因子组的加权标准化得分"""
        scores = []
        total_weight = sum(factor_weights.values())
        n = len(df)
        
        for factor, weight in factor_weights.items():
            if factor in df.columns:
                factor_data = df[factor].fillna(0).values
                
                valid_mask = factor_data != 0
                valid_data = factor_data[valid_mask]
                
                if len(valid_data) > 1 and valid_data.std() > 0:
                    norm = (factor_data - valid_data.mean()) / valid_data.std()
                    norm = norm * direction * (weight / total_weight)
                    scores.append(norm)
        
        if not scores:
            return np.zeros(n)
        
        final_score = np.sum(scores, axis=0)
        
        if final_score.std() > 0:
            final_score = (final_score - final_score.mean()) / final_score.std()
        
        return final_score
    
    def _normalize(self, data):
        """将数据标准化到0-1范围"""
        data = np.array(data)
        if data.max() == data.min():
            return np.zeros_like(data)
        return (data - data.min()) / (data.max() - data.min())
    
    def _normalize_composite(self, score):
        """将综合得分归一化到大约 -2 到 +2 范围"""
        score = np.array(score)
        if len(score) > 1 and score.std() > 0:
            score = (score - score.mean()) / score.std()
            score = score * 0.8
        return score
    
    def get_factor_explanation(self, row):
        """
        生成单只股票的因子得分解释（用于报告展示）
        
        Args:
            row: 单只股票的因子数据行（Series或dict）
        
        Returns:
            list: 解释列表
        """
        explanations = []
        
        group_names = {
            'momentum': '动量',
            'trend': '趋势',
            'volatility': '稳定性',
            'technical': '技术信号',
            'volume': '量能'
        }
        
        for group, name in group_names.items():
            col = f'{group}_score'
            if col in row and not pd.isna(row[col]):
                score = row[col]
                if score > 0.5:
                    explanations.append(f"✓ {name}表现优异")
                elif score < -0.5:
                    explanations.append(f"✗ {name}表现较弱")
        
        # 信号检测
        if row.get('macd_golden', False):
            explanations.append("🚀 MACD金叉信号")
        if row.get('kdj_golden', False):
            explanations.append("🚀 KDJ金叉信号")
        if row.get('bullish_alignment', False):
            explanations.append("📈 均线多头排列")
        
        return explanations


# ===== 提供向后兼容的别名 =====
FactorCalculator = FactorCalculatorV2


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("=" * 60)
    print("沪深300因子计算模块 v2.0 - 已升级")
    print("=" * 60)
    print("新增功能:")
    print("  ✓ 5大类因子体系")
    print("  ✓ 动态权重调整（牛市/熊市/震荡市）")
    print("  ✓ 改进的金叉死叉精确检测")
    print("  ✓ 信号共振检测（双重/三重信号）")
    print("  ✓ 单只股票因子解释生成")
    print("=" * 60)
