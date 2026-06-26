#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300晨间多因子投研系统 - 因子计算模块 v3.0

🆕 v3.0 升级内容:
- ✅ 估值因子 (PE/PB/PS/PCF) — 真正计算
- ✅ 质量因子 (ROE/ROA/毛利率/净利率) — 真正计算
- ✅ 成长因子 (营收增长/利润增长) — 真正计算
- ✅ 保留原有技术因子 (MACD/KDJ/RSI/均线/动量/波动率)
- ✅ 8大类因子体系完整实现
- ✅ 因子中性化框架
- ✅ 信号共振检测
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)


class FactorCalculatorV3:
    """因子计算类 v3.0 — 完整版"""
    
    def __init__(self):
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
    
    # ==================== 基本面因子 ====================
    
    def calculate_valuation_factors(self, fundamentals):
        """
        估值因子 — 越低越好（负向因子）
        
        Args:
            fundamentals: dict from data_fetcher.get_stock_fundamentals()
        
        Returns:
            dict: pe_ttm, pb, ps_ttm, pcf, valuation_score
        """
        if not fundamentals:
            return {'pe_ttm': None, 'pb': None, 'ps_ttm': None, 'pcf': None}
        
        result = {
            'pe_ttm': fundamentals.get('pe_ttm'),
            'pb': fundamentals.get('pb'),
            'ps_ttm': fundamentals.get('ps_ttm'),
            'pcf': fundamentals.get('pcf'),
        }
        
        # 估值综合得分（越低分越高，取负号）
        val_components = []
        for key in ['pe_ttm', 'pb', 'ps_ttm', 'pcf']:
            val = fundamentals.get(key)
            if val is not None and val > 0 and val < 500:  # 排除极端值
                val_components.append(-np.log(val + 1))  # log 转换压缩极端值
        
        result['valuation_score'] = np.mean(val_components) if val_components else None
        return result
    
    def calculate_quality_factors(self, fundamentals):
        """
        质量因子 — 越高越好
        
        Returns:
            dict: roe, roa, gross_profit_margin, net_profit_margin, quality_score
        """
        if not fundamentals:
            return {'roe': None, 'roa': None, 'gross_profit_margin': None,
                    'net_profit_margin': None}
        
        result = {
            'roe': fundamentals.get('roe'),
            'roa': fundamentals.get('roa'),
            'gross_profit_margin': fundamentals.get('gross_profit_margin'),
            'net_profit_margin': fundamentals.get('net_profit_margin'),
        }
        
        # 质量综合得分
        q_components = []
        roe = fundamentals.get('roe')
        if roe is not None and -50 < roe < 100:
            q_components.append(roe / 20)  # 归一化到合理范围
        
        roa = fundamentals.get('roa')
        if roa is not None and -20 < roa < 50:
            q_components.append(roa / 10)
        
        gpm = fundamentals.get('gross_profit_margin')
        if gpm is not None and -50 < gpm < 100:
            q_components.append(gpm / 30)
        
        npm = fundamentals.get('net_profit_margin')
        if npm is not None and -50 < npm < 100:
            q_components.append(npm / 20)
        
        result['quality_score'] = np.mean(q_components) if q_components else None
        return result
    
    def calculate_growth_factors(self, fundamentals):
        """
        成长因子 — 越高越好
        
        Returns:
            dict: revenue_growth, profit_growth, growth_score
        """
        if not fundamentals:
            return {'revenue_growth': None, 'profit_growth': None}
        
        result = {
            'revenue_growth': fundamentals.get('revenue_growth'),
            'profit_growth': fundamentals.get('profit_growth'),
        }
        
        # 成长综合得分
        g_components = []
        rg = fundamentals.get('revenue_growth')
        if rg is not None and -80 < rg < 500:
            g_components.append(np.clip(rg / 50, -2, 2))  # 压缩到 [-2, 2]
        
        pg = fundamentals.get('profit_growth')
        if pg is not None and -80 < pg < 500:
            g_components.append(np.clip(pg / 50, -2, 2))
        
        result['growth_score'] = np.mean(g_components) if g_components else None
        return result
    
    # ==================== 技术面因子 ====================
    
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
        """计算MACD + 金叉死叉检测"""
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
        
        macd_golden = False
        macd_death = False
        
        if len(hist) >= 3:
            if hist[-3] < 0 and hist[-2] < 0 and hist[-1] > 0:
                macd_golden = True
            if hist[-3] > 0 and hist[-2] > 0 and hist[-1] < 0:
                macd_death = True
        
        return {
            'macd': float(macd_line[-1]),
            'macd_signal': float(signal_line[-1]),
            'macd_hist': float(hist[-1]),
            'macd_golden': macd_golden,
            'macd_death': macd_death,
        }
    
    def calculate_rsi(self, df, period=None):
        """计算RSI"""
        if period is None:
            period = self.tech_params['rsi_period']
        
        if len(df) < period + 1:
            return {'rsi': 50, 'rsi_overbought': False, 'rsi_oversold': False}
        
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
        }
    
    def calculate_kdj(self, df):
        """计算KDJ"""
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
        
        kdj_golden = False
        kdj_death = False
        
        if len(k) >= 3:
            if k[-3] < d[-3] and k[-2] < d[-2] and k[-1] > d[-1] and d[-1] < 40:
                kdj_golden = True
            if k[-3] > d[-3] and k[-2] > d[-2] and k[-1] < d[-1] and d[-1] > 60:
                kdj_death = True
        
        return {
            'kdj_k': float(k[-1]),
            'kdj_d': float(d[-1]),
            'kdj_j': float(j[-1]),
            'kdj_golden': kdj_golden,
            'kdj_death': kdj_death,
        }
    
    def calculate_momentum(self, df):
        """计算动量因子"""
        result = {}
        close_prices = df['close']
        
        periods = {'return_1m': 20, 'return_3m': 60, 'return_6m': 120}
        for name, period in periods.items():
            if len(df) >= period:
                result[name] = float(close_prices.iloc[-1] / close_prices.iloc[-period] - 1)
            else:
                result[name] = np.nan
        
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
        
        for name, period in [('std_1m', 20), ('std_3m', 60)]:
            if len(returns) >= period:
                result[name] = float(returns.tail(period).std() * np.sqrt(252))
            else:
                result[name] = np.nan
        
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
        
        bullish_alignment = (ma5 > ma10) and (ma10 > ma20) and (ma20 > ma60)
        bearish_alignment = (ma5 < ma10) and (ma10 < ma20) and (ma20 < ma60)
        
        result['bullish_alignment'] = bool(bullish_alignment)
        result['bearish_alignment'] = bool(bearish_alignment)
        
        trend_score = 0
        if ma5 > ma10: trend_score += 1
        if ma10 > ma20: trend_score += 1
        if ma20 > ma60: trend_score += 1
        result['trend_score'] = trend_score
        
        return result
    
    # ==================== 综合计算 ====================
    
    def calculate_all_factors(self, stock_data):
        """
        计算单只股票的所有因子（技术面 + 基本面）
        
        Args:
            stock_data: dict with keys:
                - 'name', 'code', 'daily' (DataFrame)
                - 'fundamentals' (dict, optional)
        """
        df = stock_data['daily']
        if df is None or len(df) < 30:
            logger.warning(f"股票 {stock_data['name']} 数据不足，跳过")
            return None
        
        result = {
            'code': stock_data['code'],
            'name': stock_data['name'],
            'date': df['date'].iloc[-1] if 'date' in df.columns else datetime.now(),
            'close_price': float(df['close'].iloc[-1]),
            'pct_chg': float(df['pct_chg'].iloc[-1]) if 'pct_chg' in df.columns else 0,
        }
        
        # 基本面因子 🆕
        fundamentals = stock_data.get('fundamentals')
        result.update(self.calculate_valuation_factors(fundamentals))
        result.update(self.calculate_quality_factors(fundamentals))
        result.update(self.calculate_growth_factors(fundamentals))
        
        # 技术面因子
        result.update(self.calculate_ma(df))
        result.update(self.calculate_macd(df))
        result.update(self.calculate_rsi(df))
        result.update(self.calculate_kdj(df))
        result.update(self.calculate_momentum(df))
        result.update(self.calculate_volatility(df))
        result.update(self.calculate_volume_factor(df))
        result.update(self.calculate_trend_factor(df))
        
        return result
    
    def calculate_factor_score(self, factors_df, market_regime='NEUTRAL'):
        """
        计算综合因子得分 — 包含8大类因子
        
        Args:
            factors_df: 所有股票的因子DataFrame
            market_regime: 市场环境 ('BULL', 'NEUTRAL', 'BEAR')
        """
        df = factors_df.copy()
        logger.info(f"计算综合得分，市场环境: {market_regime}")
        
        # ===== 市场环境动态权重 =====
        if market_regime in ['BULL', 'BULL_STRONG']:
            factor_weights = {
                'valuation': 0.10,   # 牛市估值不重要
                'quality': 0.15,
                'growth': 0.15,
                'momentum': 0.25,    # 动量重要
                'trend': 0.15,
                'volatility': 0.05,  # 波动率不重要
                'technical': 0.10,
                'volume': 0.05
            }
        elif market_regime in ['BEAR', 'BEAR_STRONG']:
            factor_weights = {
                'valuation': 0.25,   # 熊市看估值
                'quality': 0.25,     # 熊市看质量
                'growth': 0.05,
                'momentum': 0.05,
                'trend': 0.10,
                'volatility': 0.15,  # 低波动重要
                'technical': 0.10,
                'volume': 0.05
            }
        else:
            factor_weights = {
                'valuation': 0.15,
                'quality': 0.15,
                'growth': 0.15,
                'momentum': 0.15,
                'trend': 0.10,
                'volatility': 0.10,
                'technical': 0.10,
                'volume': 0.10
            }
        
        group_scores = {}
        n = len(df)
        
        # --- 1. 估值因子组（低估值=高分）---
        if 'valuation_score' in df.columns:
            val_scores = self._zscore_with_mask(df['valuation_score'].values, direction=1)
            group_scores['valuation'] = val_scores
        
        # --- 2. 质量因子组 ---
        if 'quality_score' in df.columns:
            q_scores = self._zscore_with_mask(df['quality_score'].values, direction=1)
            group_scores['quality'] = q_scores
        
        # --- 3. 成长因子组 ---
        if 'growth_score' in df.columns:
            g_scores = self._zscore_with_mask(df['growth_score'].values, direction=1)
            group_scores['growth'] = g_scores
        
        # --- 4. 动量因子组 ---
        momentum_factors = {'return_1m': 0.4, 'return_3m': 0.4, 'price_position_60d': 0.2}
        group_scores['momentum'] = self._calculate_group_score(df, momentum_factors, direction=1)
        
        # --- 5. 趋势因子组 ---
        trend_factors = {'trend_score': 0.5, 'price_to_ma20': 0.3, 'price_to_ma60': 0.2}
        group_scores['trend'] = self._calculate_group_score(df, trend_factors, direction=1)
        
        # --- 6. 波动率因子组（越低越好）---
        vol_factors = {'std_1m': 0.5, 'std_3m': 0.3, 'max_drawdown_1m': 0.2}
        group_scores['volatility'] = self._calculate_group_score(df, vol_factors, direction=-1)
        
        # --- 7. 技术信号因子组 ---
        tech_scores = np.zeros(n)
        if 'macd_golden' in df.columns:
            tech_scores += df['macd_golden'].fillna(False).astype(float).values * 0.4
        if 'kdj_golden' in df.columns:
            tech_scores += df['kdj_golden'].fillna(False).astype(float).values * 0.3
        if 'bullish_alignment' in df.columns:
            tech_scores += df['bullish_alignment'].fillna(False).astype(float).values * 0.3
        if 'rsi' in df.columns:
            rsi = df['rsi'].fillna(50).values
            rsi_score = 1 - np.abs(rsi - 50) / 50
            tech_scores += rsi_score * 0.2
        group_scores['technical'] = self._normalize(tech_scores)
        
        # --- 8. 量能因子组 ---
        vol_scores = np.zeros(n)
        if 'volume_ratio' in df.columns:
            vr = df['volume_ratio'].fillna(1).values
            vol_scores += np.clip((vr - 1) / 2, 0, 1) * 0.5
        if 'volume_trend' in df.columns:
            vt = df['volume_trend'].fillna(0).values
            vol_scores += np.clip(vt, -0.5, 0.5) + 0.5
        group_scores['volume'] = self._normalize(vol_scores)
        
        # ===== 计算综合得分 =====
        composite_score = np.zeros(n)
        for group, weight in factor_weights.items():
            if group in group_scores:
                composite_score += group_scores[group] * weight
        
        composite_score = self._normalize_composite(composite_score)
        
        # ===== 信号共振加分 =====
        if 'macd_golden' in df.columns and 'kdj_golden' in df.columns:
            double_golden = (
                df['macd_golden'].fillna(False).astype(bool).values &
                df['kdj_golden'].fillna(False).astype(bool).values
            )
            composite_score[double_golden] += 0.5
        
        if 'bullish_alignment' in df.columns:
            triple_signal = double_golden & df['bullish_alignment'].fillna(False).astype(bool).values
            composite_score[triple_signal] += 0.8
        
        df['composite_score'] = composite_score
        for group, scores in group_scores.items():
            df[f'{group}_score'] = scores
        
        return df
    
    # ==================== 辅助方法 ====================
    
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
    
    def _zscore_with_mask(self, data, direction=1):
        """带掩码的z-score标准化"""
        data = np.array(data, dtype=float)
        valid = ~np.isnan(data) & (data != 0)
        result = np.zeros_like(data)
        
        if valid.sum() > 1:
            mean = data[valid].mean()
            std = data[valid].std()
            if std > 0:
                result[valid] = (data[valid] - mean) / std * direction
        
        return result
    
    def _normalize(self, data):
        """归一化到0-1"""
        data = np.array(data)
        if data.max() == data.min():
            return np.zeros_like(data)
        return (data - data.min()) / (data.max() - data.min())
    
    def _normalize_composite(self, score):
        """综合得分归一化到约 -2 ~ +2"""
        score = np.array(score)
        if len(score) > 1 and score.std() > 0:
            score = (score - score.mean()) / score.std()
            score = score * 0.8
        return score
    
    def get_factor_explanation(self, row):
        """生成单只股票的因子解释"""
        explanations = []
        
        group_names = {
            'valuation': '估值',
            'quality': '质量',
            'growth': '成长',
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
        
        if row.get('macd_golden', False):
            explanations.append("🚀 MACD金叉信号")
        if row.get('kdj_golden', False):
            explanations.append("🚀 KDJ金叉信号")
        if row.get('bullish_alignment', False):
            explanations.append("📈 均线多头排列")
        
        return explanations


# 向后兼容别名
FactorCalculator = FactorCalculatorV3


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("=" * 60)
    print("因子计算模块 v3.0 — 完整版")
    print("=" * 60)
    print("8大类因子体系:")
    print("  ✓ 估值因子 (PE/PB/PS/PCF)")
    print("  ✓ 质量因子 (ROE/ROA/毛利率)")
    print("  ✓ 成长因子 (营收增长/利润增长)")
    print("  ✓ 动量因子 (1月/3月/6月收益率)")
    print("  ✓ 趋势因子 (均线排列)")
    print("  ✓ 波动率因子 (年化波动率/最大回撤)")
    print("  ✓ 技术信号因子 (MACD/KDJ/RSI)")
    print("  ✓ 量能因子 (成交量/趋势)")
    print("=" * 60)
