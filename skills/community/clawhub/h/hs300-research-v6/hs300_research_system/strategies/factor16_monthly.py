# -*- coding: utf-8 -*-
"""
16因子综合量价策略（月度调仓版）

策略来源：方正金工
多空年化收益：47.51%
月度最大回撤：1.24%
调仓频率：月度

核心特色：
  - 全部因子基于分钟级行情数据构建
  - 高频因子低频化：分钟因子 → 日线平滑 → 月度选股
  - 对称正交化消除因子共线性
  - 等权合成综合得分
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class Factor16MonthlyStrategy:
    """
    16因子综合量价策略（月度版）
    
    16个因子分类：
    1. 价格类因子 (4): 日内趋势、隔夜收益、尾盘效应、高低点位置
    2. 成交量类因子 (4): 量价配合、异常放量、缩量企稳、量比变化
    3. 波动类因子 (4): 日内波动分布、极差比率、波动率变化、波动偏度
    4. 资金流类因子 (4): 大单净流入、主力买卖差、资金集中度、资金加速度
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.rebalance_freq = 'monthly'
        self.top_n = self.config.get('top_n', 50)
        self.bottom_n = self.config.get('bottom_n', 50)
        self.smoothing_window = self.config.get('smoothing_window', 5)  # 5日平滑
    
    def get_stock_pool(self, date: str) -> List[str]:
        """全市场A股（剔除ST/停牌/次新/涨跌停）"""
        # TODO: 接入真实数据源
        return []
    
    def calculate_16_factors(self, stocks: List[str], date: str) -> pd.DataFrame:
        """
        计算16个分钟级量价因子
        
        数据需求：
        - 个股分钟级K线（开高低收量）
        - 逐笔成交数据（可选）
        - 日频数据（辅助计算）
        """
        # TODO: 接入真实分钟数据计算
        factor_cols = [
            # 价格类
            'intraday_trend', 'overnight_return', 'tail_effect', 'highlow_position',
            # 成交量类
            'volume_price_corr', 'abnormal_volume', 'volume_shrink', 'volume_ratio_change',
            # 波动类
            'intraday_volatility', 'range_ratio', 'volatility_change', 'volatility_skew',
            # 资金流类
            'large_order_flow', 'main_force_diff', 'capital_concentration', 'capital_acceleration',
        ]
        return pd.DataFrame(columns=factor_cols)
    
    def smooth_factors(self, factor_df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
        """
        高频因子低频化：滚动窗口平滑
        
        分钟级因子噪音大，通过N日均线平滑后更稳定。
        """
        smoothed = factor_df.rolling(window=window, min_periods=1).mean()
        return smoothed
    
    def preprocess_factors(self, factor_df: pd.DataFrame) -> pd.DataFrame:
        """
        因子预处理流水线：
        1. MAD去极值
        2. Z-Score标准化
        3. 市值中性化（可选）
        """
        processed = factor_df.copy()
        
        # MAD去极值
        for col in processed.columns:
            median = processed[col].median()
            mad = (processed[col] - median).abs().median()
            if mad > 0:
                processed[col] = processed[col].clip(median - 3*mad, median + 3*mad)
        
        # Z-Score标准化
        for col in processed.columns:
            mean = processed[col].mean()
            std = processed[col].std()
            if std > 1e-10:
                processed[col] = (processed[col] - mean) / std
        
        return processed
    
    def orthogonalize_factors(self, factor_df: pd.DataFrame) -> pd.DataFrame:
        """对称正交化（SVD）消除因子共线性"""
        matrix = factor_df.values.astype(float)
        for j in range(matrix.shape[1]):
            col_nan = np.isnan(matrix[:, j])
            if col_nan.any():
                matrix[col_nan, j] = np.nanmean(matrix[:, j])
        
        F = matrix - matrix.mean(axis=0)
        U, S, Vt = np.linalg.svd(F, full_matrices=False)
        F_orth = U @ np.diag(S)
        
        return pd.DataFrame(F_orth, index=factor_df.index, columns=factor_df.columns)
    
    def composite_score(self, factor_df: pd.DataFrame) -> pd.Series:
        """
        等权合成综合得分
        
        16因子量价因子全部为等权合成（方正金工实证结果）
        """
        return factor_df.mean(axis=1)
    
    def select_stocks(self, scores: pd.Series) -> Tuple[List[str], List[str]]:
        """
        选股：多头Top N + 空头Bottom N
        
        量价因子通常为反向因子（得分越低越好），
        所以多头选得分最低的，空头选得分最高的
        """
        # 量价因子多为反向因子
        long = scores.nsmallest(self.top_n).index.tolist()
        short = scores.nlargest(self.bottom_n).index.tolist()
        return long, short
    
    def run(self, date: str) -> Dict:
        """执行16因子量价月度策略"""
        print(f"\n{'='*60}")
        print(f"[16因子综合量价(月频)] {date}")
        print(f"{'='*60}")
        
        stocks = self.get_stock_pool(date)
        print(f"  [1/5] 股票池: {len(stocks)} 只")
        
        factor_df = self.calculate_16_factors(stocks, date)
        print(f"  [2/5] 16因子计算完成: {factor_df.shape}")
        
        smoothed = self.smooth_factors(factor_df, self.smoothing_window)
        print(f"  [3/5] 5日平滑完成")
        
        processed = self.preprocess_factors(smoothed)
        ortho = self.orthogonalize_factors(processed)
        print(f"  [4/5] 预处理+正交化完成")
        
        scores = self.composite_score(ortho)
        long_stocks, short_stocks = self.select_stocks(scores)
        print(f"  [5/5] 多头{len(long_stocks)}只 / 空头{len(short_stocks)}只")
        
        print(f"\n  ✅ 16因子量价月频策略执行完成")
        print(f"     多头前5: {long_stocks[:5]}")
        print(f"     空头前5: {short_stocks[:5]}")
        
        return {
            'long': long_stocks,
            'short': short_stocks,
            'scores': scores,
            'date': date,
            'strategy': 'factor16_monthly',
            'rebalance_freq': 'monthly',
        }
