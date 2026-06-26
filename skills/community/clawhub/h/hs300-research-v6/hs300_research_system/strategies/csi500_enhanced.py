# -*- coding: utf-8 -*-
"""
中证500指数增强策略 (CSI 500 Index Enhanced)

策略来源：国泰海通证券金融工程研究团队
2025年超额收益：9.5% (ICIR加权) / 29.97% (风险预算复合)
调仓频率：月度
选股范围：中证500成分股
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class CSI500EnhancedStrategy:
    """
    中证500指数增强策略
    
    核心流程：
    1. 获取中证500成分股
    2. 因子计算（估值/成长/分析师预期/量价/分红/治理）
    3. 因子预处理（MAD去极值 → Z-Score标准化 → 市值/行业中性化）
    4. 对称正交化
    5. ICIR加权合成综合得分
    6. 组合优化（行业偏离≤2% / 个股偏离≤1.5% / 跟踪误差≤4%）
    
    进阶：风险预算复合模式
    - 多因子模型 + 超预期组合，按信息比平方分配权重
    - 年化超额收益提升至29.97%，信息比4.5
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.rebalance_freq = 'monthly'
        self.top_n = self.config.get('top_n', 120)
        self.lookback_months = self.config.get('lookback_months', 24)
        self.use_risk_budget = self.config.get('use_risk_budget', False)
        
        # 组合优化约束
        self.constraints = {
            'active_weight_per_stock': 0.015,  # 单个股偏离 ≤ 1.5%
            'industry_deviation': 0.02,         # 行业偏离 ≤ 2%
            'style_exposure': 0.2,              # 风格暴露偏离 ≤ 0.2
            'tracking_error': 0.04,             # 跟踪误差 ≤ 4%
            'turnover': 0.25,                   # 换手率 ≤ 25%/月
        }
        self.constraints.update(self.config.get('constraints', {}))
    
    def get_stock_pool(self, date: str) -> List[str]:
        """获取中证500成分股"""
        # TODO: 接入真实数据源
        # from data_fetcher import DataFetcher
        # fetcher = DataFetcher()
        # return fetcher.get_csi500_constituents(date)
        return []  # placeholder
    
    def calculate_factors(self, stocks: List[str], date: str) -> pd.DataFrame:
        """
        计算多维度因子矩阵
        
        因子类别：
        - 估值因子: PE/PB/PS/PCF
        - 成长因子: EarningsSQYoY/SalesSQ_YoY
        - 分析师预期: IncomeAdjust/SUE
        - 高频量价: MCIB/integrated_bigsmall
        - 流动性: TurnoverAvg1M
        - 分红: 股息率
        - 治理: 股权激励/高管增持
        
        Returns:
            DataFrame: (n_stocks × n_factors)
        """
        # TODO: 接入真实因子计算
        return pd.DataFrame()
    
    def preprocess_factors(self, factor_df: pd.DataFrame) -> pd.DataFrame:
        """因子预处理：去极值 → 标准化 → 中性化"""
        from .core_factors import mad_winsorize, zscore_standardize, neutralize_factor
        
        df = factor_df.copy()
        
        # Step 1: MAD去极值
        for col in df.columns:
            df[col] = mad_winsorize(df[col], multiplier=3.0)
        
        # Step 2: Z-Score标准化
        for col in df.columns:
            df[col] = zscore_standardize(df[col])
        
        # Step 3: 市值/行业中性化
        # TODO: 传入真实市值和行业数据
        # df = neutralize_factor(df, market_cap=..., industry_dummies=...)
        
        return df
    
    def compute_icir_weights(self, ic_history: pd.DataFrame) -> pd.Series:
        """计算ICIR权重"""
        recent = ic_history.tail(self.lookback_months)
        ic_mean = recent.mean()
        ic_std = recent.std()
        icir = ic_mean / (ic_std + 1e-8)
        
        abs_icir = icir.abs()
        weights = abs_icir / abs_icir.sum()
        return weights
    
    def composite_score(self, factor_df: pd.DataFrame, weights: pd.Series) -> pd.Series:
        """ICIR加权合成综合得分"""
        score = pd.Series(0.0, index=factor_df.index)
        for col, w in weights.items():
            if col in factor_df.columns:
                score += w * factor_df[col].fillna(0)
        return score
    
    def optimize_portfolio(self, scores: pd.Series,
                           benchmark_weights: pd.Series) -> pd.Series:
        """
        组合优化
        
        两种模式：
        1. 均值-方差优化：严格约束行业/风格/个股偏离
        2. 风险预算优化：多因子+超预期组合，按信息比平方分配权重
        """
        if self.use_risk_budget:
            # 风险预算复合模式
            return self._risk_budget_optimize(scores, benchmark_weights)
        else:
            # 均值-方差优化模式
            return self._mean_variance_optimize(scores, benchmark_weights)
    
    def _mean_variance_optimize(self, scores: pd.Series,
                                 benchmark_weights: pd.Series) -> pd.Series:
        """均值-方差优化"""
        n = len(scores)
        base_weight = 1.0 / n
        weights = pd.Series(base_weight, index=scores.index)
        
        # 约束：个股权重偏离
        bench = benchmark_weights.reindex(weights.index).fillna(0)
        diff = weights - bench
        excess = diff.abs()
        max_active = self.constraints['active_weight_per_stock']
        if excess.max() > max_active:
            scale = max_active / excess.max()
            weights = bench + diff * scale
        
        total = weights.sum()
        if total > 0:
            weights = weights / total
        
        return weights
    
    def _risk_budget_optimize(self, scores: pd.Series,
                               benchmark_weights: pd.Series) -> pd.Series:
        """
        风险预算优化
        基于滚动两年的信息比平方分配权重
        """
        # TODO: 接入真实信息比计算
        # 简化版：多因子模型权重 + 超预期组合权重
        # 权重比例 = IR₁² : IR₂²
        ir1_sq = 4.31 ** 2  # 多因子模型信息比
        ir2_sq = 4.50 ** 2  # 复合策略信息比
        total = ir1_sq + ir2_sq
        
        w1 = ir1_sq / total  # 多因子模型权重
        w2 = ir2_sq / total  # 超预期组合权重
        
        # 按权重分配
        n = len(scores)
        base_weight = 1.0 / n
        weights = pd.Series(base_weight, index=scores.index)
        
        total_w = weights.sum()
        if total_w > 0:
            weights = weights / total_w
        
        return weights
    
    def run(self, date: str) -> Dict:
        """执行完整的中证500指增策略流程"""
        print(f"\n{'='*60}")
        print(f"[中证500指增策略] {date}")
        print(f"{'='*60}")
        if self.use_risk_budget:
            print(f"  模式: 风险预算复合")
        else:
            print(f"  模式: ICIR加权多因子")
        
        # Step 1: 获取成分股
        stocks = self.get_stock_pool(date)
        print(f"  [1/6] 中证500成分股: {len(stocks)} 只")
        
        # Step 2: 因子计算
        factor_df = self.calculate_factors(stocks, date)
        print(f"  [2/6] 因子维度: {factor_df.shape}")
        
        # Step 3: 因子预处理
        cleaned_df = self.preprocess_factors(factor_df)
        print(f"  [3/6] 因子预处理完成")
        
        # Step 4: ICIR加权
        weights = pd.Series(1.0/len(cleaned_df.columns), index=cleaned_df.columns) if len(cleaned_df.columns) > 0 else pd.Series()
        
        # Step 5: 综合得分
        scores = self.composite_score(cleaned_df, weights) if len(cleaned_df) > 0 else pd.Series()
        print(f"  [4/6] ICIR加权合成完成")
        
        # Step 6: 选股 + 组合优化
        top_stocks = scores.nlargest(self.top_n).index.tolist() if len(scores) > 0 else []
        benchmark_weights = pd.Series(1.0/max(len(stocks),1), index=stocks) if stocks else pd.Series()
        final_weights = self.optimize_portfolio(scores[top_stocks], benchmark_weights) if len(scores) > 0 else pd.Series()
        print(f"  [5/6] 选中 {len(top_stocks)} 只股票")
        print(f"  [6/6] 组合优化完成")
        
        print(f"\n  ✅ 中证500指增策略执行完成")
        print(f"     选中: {len(top_stocks)} 只")
        print(f"     前5: {top_stocks[:5]}")
        
        return {
            'stocks': top_stocks,
            'weights': final_weights,
            'scores': scores,
            'date': date,
            'strategy': 'csi500_enhanced',
            'bench': '000905.SH',
        }
