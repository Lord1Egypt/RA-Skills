# -*- coding: utf-8 -*-
"""
多策略复合因子组合（沪深300增强）
Multi-Strategy Composite Factor Portfolio

策略来源：国泰海通证券金融工程研究团队
2016年以来年化超额收益：12.6% | 跟踪误差：5.2% | 信息比：2.38
较基础策略提升：+3.6% (年化)

三层复合架构：
  基础指数增强(60%) + 域内卫星(30%) + 域外卫星(10%)
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class BaseMultiFactorStrategy:
    """基础指数增强策略 — ICIR加权多因子模型（成分股内）"""
    
    def __init__(self, ic_lookback: int = 24):
        self.ic_lookback = ic_lookback
    
    def composite_score(self, stock_pool: pd.DataFrame,
                        ic_history: pd.DataFrame = None) -> pd.Series:
        """ICIR加权合成综合得分"""
        processed = self._preprocess_factors(stock_pool)
        
        if ic_history is not None and len(ic_history) > 0:
            recent = ic_history.tail(self.ic_lookback)
            ic_mean = recent.mean()
            ic_std = recent.std()
            icir = ic_mean / (ic_std + 1e-8)
            abs_icir = icir.abs()
            weights = abs_icir / abs_icir.sum()
        else:
            # 等权
            weights = pd.Series(1.0/len(processed.columns), index=processed.columns)
        
        score = pd.Series(0.0, index=processed.index)
        for col, w in weights.items():
            if col in processed.columns:
                score += w * processed[col].fillna(0)
        return score
    
    def _preprocess_factors(self, df: pd.DataFrame) -> pd.DataFrame:
        """MAD去极值 + Z-Score标准化"""
        processed = df.copy()
        for col in processed.columns:
            median = processed[col].median()
            mad = (processed[col] - median).abs().median()
            if mad > 0:
                processed[col] = processed[col].clip(median - 3*mad, median + 3*mad)
            mean = processed[col].mean()
            std = processed[col].std()
            if std > 1e-10:
                processed[col] = (processed[col] - mean) / std
        return processed


class IntraDomainSatelliteStrategy:
    """域内卫星策略 — 动量+基本面因子选股（成分股内）"""
    
    def __init__(self, momentum_lookback: int = 60):
        self.mom_lookback = momentum_lookback
    
    def compute_combined_score(self, price_data: pd.DataFrame,
                               earnings_data: pd.DataFrame) -> pd.Series:
        """综合得分 = 0.5×动量得分 + 0.5×盈利改善得分"""
        # 动量得分（6/3/1月等权）
        if price_data.shape[1] >= 21:
            mom_1m = price_data.iloc[:, -21:].pct_change(periods=21, axis=1).iloc[:, -1]
        else:
            mom_1m = pd.Series(0, index=price_data.index)
        
        if price_data.shape[1] >= 63:
            mom_3m = price_data.iloc[:, -63:].pct_change(periods=63, axis=1).iloc[:, -1]
        else:
            mom_3m = pd.Series(0, index=price_data.index)
        
        mom_score = pd.DataFrame({'mom_1m': mom_1m, 'mom_3m': mom_3m}).rank(pct=True).mean(axis=1)
        
        # 盈利改善得分
        if earnings_data is not None and earnings_data.shape[1] >= 2:
            yoy = earnings_data.iloc[:, -1] / (earnings_data.iloc[:, -2] + 1e-8)
            earn_score = yoy.rank(pct=True)
        else:
            earn_score = pd.Series(0.5, index=price_data.index)
        
        return 0.5 * mom_score + 0.5 * earn_score


class ExtraDomainSatelliteStrategy:
    """域外卫星策略 — 小市值高增长组合（全市场）"""
    
    def __init__(self, cap_percentile: float = 0.3):
        self.cap_threshold = cap_percentile
    
    def compute_combined_score(self, market_cap: pd.Series,
                               revenue_growth: pd.DataFrame,
                               earnings_growth: pd.DataFrame) -> pd.Series:
        """综合得分 = 0.4×小市值得分 + 0.6×高增长得分"""
        cap_score = 1 - market_cap.rank(pct=True)
        
        rev_g = revenue_growth.mean(axis=1).rank(pct=True) if revenue_growth is not None else pd.Series(0.5, index=market_cap.index)
        earn_g = earnings_growth.mean(axis=1).rank(pct=True) if earnings_growth is not None else pd.Series(0.5, index=market_cap.index)
        growth_score = pd.DataFrame({'rev': rev_g, 'earn': earn_g}).mean(axis=1)
        
        return 0.4 * cap_score + 0.6 * growth_score


class CompositeStrategy:
    """
    多策略复合因子组合（沪深300增强）
    
    三层复合架构：
    - 基础指增(60%): ICIR加权多因子模型
    - 域内卫星(30%): 动量+基本面因子
    - 域外卫星(10%): 小市值高增长组合
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.rebalance_freq = 'monthly'
        self.base_weight = self.config.get('base_weight', 0.60)
        self.intra_weight = self.config.get('intra_weight', 0.30)
        self.extra_weight = self.config.get('extra_weight', 0.10)
        
        assert abs(self.base_weight + self.intra_weight + self.extra_weight - 1.0) < 1e-6
        
        self.base_strategy = BaseMultiFactorStrategy()
        self.intra_strategy = IntraDomainSatelliteStrategy()
        self.extra_strategy = ExtraDomainSatelliteStrategy()
    
    def run(self, date: str,
            csi300_stocks: List[str] = None,
            factor_data: pd.DataFrame = None,
            price_data: pd.DataFrame = None,
            earnings_data: pd.DataFrame = None,
            all_stocks: List[str] = None,
            market_cap: pd.Series = None,
            revenue_growth: pd.DataFrame = None,
            earnings_growth: pd.DataFrame = None,
            base_top_n: int = 60,
            intra_top_n: int = 40,
            extra_top_n: int = 30) -> Dict:
        """执行多策略复合组合"""
        print(f"\n{'='*60}")
        print(f"[多策略复合因子组合] {date}")
        print(f"{'='*60}")
        print(f"  基础指增: {self.base_weight*100:.0f}% | 域内卫星: {self.intra_weight*100:.0f}% | 域外卫星: {self.extra_weight*100:.0f}%")
        
        final_weights = {}
        
        # Step 1: 基础策略
        if factor_data is not None and len(factor_data) > 0:
            base_stocks = csi300_stocks or factor_data.index.tolist()
            base_data = factor_data.loc[base_stocks] if base_stocks else factor_data
            base_scores = self.base_strategy.composite_score(base_data)
            base_top = base_scores.nlargest(base_top_n).index.tolist()
            for s in base_top:
                final_weights[s] = final_weights.get(s, 0) + self.base_weight / len(base_top)
            print(f"  [1/4] 基础策略: {len(base_top)} 只")
        
        # Step 2: 域内卫星
        if price_data is not None and len(price_data) > 0:
            intra_scores = self.intra_strategy.compute_combined_score(price_data, earnings_data)
            intra_stocks = csi300_stocks or price_data.index.tolist()
            intra_scores = intra_scores[intra_scores.index.isin(intra_stocks)]
            intra_top = intra_scores.nlargest(intra_top_n).index.tolist()
            for s in intra_top:
                final_weights[s] = final_weights.get(s, 0) + self.intra_weight / len(intra_top)
            print(f"  [2/4] 域内卫星: {len(intra_top)} 只")
        
        # Step 3: 域外卫星
        if market_cap is not None and len(market_cap) > 0:
            extra_scores = self.extra_strategy.compute_combined_score(market_cap, revenue_growth, earnings_growth)
            if all_stocks:
                extra_scores = extra_scores[extra_scores.index.isin(all_stocks)]
            if csi300_stocks:
                extra_scores = extra_scores.drop(index=[s for s in extra_scores.index if s in csi300_stocks], errors='ignore')
            extra_top = extra_scores.nlargest(extra_top_n).index.tolist()
            for s in extra_top:
                final_weights[s] = final_weights.get(s, 0) + self.extra_weight / len(extra_top)
            print(f"  [3/4] 域外卫星: {len(extra_top)} 只")
        
        # 归一化
        total = sum(final_weights.values())
        if total > 0:
            final_weights = {k: v / total for k, v in final_weights.items()}
        
        weights_series = pd.Series(final_weights)
        
        print(f"  [4/4] 权重合并完成")
        print(f"\n  ✅ 多策略复合策略执行完成: {len(final_weights)} 只")
        
        return {
            'stocks': list(final_weights.keys()),
            'weights': weights_series,
            'date': date,
            'strategy': 'multi_strategy_composite',
            'bench': '000300.SH',
        }
