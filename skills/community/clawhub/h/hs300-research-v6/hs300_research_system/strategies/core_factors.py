# -*- coding: utf-8 -*-
"""
多策略量化选股系统 — 共享因子处理库

所有策略共用的底层因子计算能力：
1. 因子预处理：MAD去极值、Z-Score标准化、Rank标准化
2. 中性化：市值中性化、行业中性化
3. 正交化：对称正交化(SVD分解)
4. 因子合成：等权合成、ICIR加权合成
5. 组合构建：等权、市值加权、约束优化
6. 绩效评估：超额收益、信息比率

来源：综合国泰海通、方正金工、中信建投等头部券商方法论
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple


# ============================================================
# 一、因子预处理
# ============================================================

def mad_winsorize(series: pd.Series, multiplier: float = 3.0) -> pd.Series:
    """
    MAD去极值 — 中位数绝对偏差法
    
    将所有超过 [median ± multiplier × MAD] 的值缩回边界。
    相比3σ法更稳健，对异常值不敏感。
    """
    median = series.median()
    mad = (series - median).abs().median()
    if mad == 0 or np.isnan(mad):
        return series
    upper = median + multiplier * mad
    lower = median - multiplier * mad
    return series.clip(lower, upper)


def zscore_standardize(series: pd.Series) -> pd.Series:
    """Z-Score标准化: (x - mean) / std"""
    mean = series.mean()
    std = series.std()
    if std < 1e-10:
        return pd.Series(0.0, index=series.index)
    return (series - mean) / std


def rank_normalize(series: pd.Series) -> pd.Series:
    """Rank百分位归一化: 将因子值映射到[0,1]区间"""
    return series.rank(pct=True)


def process_factors(df: pd.DataFrame, columns: List[str] = None,
                    method: str = 'zscore') -> pd.DataFrame:
    """
    因子预处理流水线：去极值 → 标准化
    
    Args:
        df: 因子矩阵 (n_stocks × n_factors)
        columns: 需要处理的列，默认全部数值列
        method: 标准化方法 ('zscore' | 'rank' | 'robust')
    Returns:
        处理后的因子矩阵
    """
    result = df.copy()
    cols = columns if columns else df.select_dtypes(include=[np.number]).columns.tolist()
    
    for col in cols:
        if col not in result.columns:
            continue
        s = result[col].dropna()
        if len(s) < 2:
            continue
        
        # Step 1: MAD去极值
        s = mad_winsorize(s, multiplier=3.0)
        
        # Step 2: 标准化
        if method == 'rank':
            result[col] = rank_normalize(s)
        elif method == 'robust':
            median = s.median()
            mad_val = (s - median).abs().median()
            if mad_val > 1e-10:
                result[col] = (s - median) / (mad_val * 1.4826)
            else:
                result[col] = 0.0
        else:
            result[col] = zscore_standardize(s)
    
    return result


# ============================================================
# 二、中性化
# ============================================================

def neutralize_factor(factor_values: pd.Series,
                      market_cap: pd.Series = None,
                      industry_dummies: pd.DataFrame = None) -> pd.Series:
    """
    因子中性化 — 剔除市值和行业风格影响
    
    通过横截面回归取残差实现：
        factor = α + β₁·ln(market_cap) + β₂·industry + ε
    返回 ε 作为中性化后的因子值。
    """
    common_idx = factor_values.dropna().index
    
    # 构建解释变量矩阵
    X_parts = []
    
    if market_cap is not None:
        valid_cap = market_cap.reindex(common_idx).dropna()
        if len(valid_cap) > 0:
            X_parts.append(('log_cap', np.log(valid_cap.values + 1)))
            common_idx = valid_cap.index
    
    if industry_dummies is not None:
        valid_ind = industry_dummies.reindex(common_idx).dropna()
        if len(valid_ind) > 0:
            ind_cols = valid_ind.columns[1:] if len(valid_ind.columns) > 1 else valid_ind.columns
            for c in ind_cols:
                X_parts.append((f'ind_{c}', valid_ind[c].values))
            common_idx = valid_ind.index
    
    if not X_parts or len(common_idx) < 10:
        return factor_values
    
    # 横截面回归
    y = factor_values.loc[common_idx].values
    X = np.column_stack([np.ones(len(common_idx))] + [p[1] for p in X_parts])
    
    try:
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        residual = y - X @ beta
        result = factor_values.copy()
        result.loc[common_idx] = residual
        return result
    except Exception:
        return factor_values


# ============================================================
# 三、对称正交化 (SVD)
# ============================================================

def symmetric_orthogonalize(factor_matrix: np.ndarray) -> np.ndarray:
    """
    对称正交化 — 通过SVD分解消除因子间多重共线性
    
    核心公式: F_orth = U @ diag(S)
    其中 F = U @ diag(S) @ V^T 是F的SVD分解
    
    优势: 对所有因子一视同仁，无施密特正交化的顺序依赖问题。
    """
    # 中心化
    F = factor_matrix - factor_matrix.mean(axis=0)
    
    # 处理NaN（用列均值填充）
    for j in range(F.shape[1]):
        col_nan = np.isnan(F[:, j])
        if col_nan.any():
            F[col_nan, j] = np.nanmean(F[:, j])
    
    # SVD分解
    U, S, Vt = np.linalg.svd(F, full_matrices=False)
    
    # 对称正交化
    F_orth = U @ np.diag(S)
    
    return F_orth


def orthogonalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """对DataFrame进行对称正交化"""
    matrix = df.values.astype(float)
    F_orth = symmetric_orthogonalize(matrix)
    return pd.DataFrame(F_orth, index=df.index, columns=df.columns)


# ============================================================
# 四、IC/ICIR 计算与加权
# ============================================================

def compute_rank_ic(factor_values: pd.Series,
                    forward_returns: pd.Series) -> float:
    """
    计算单期Rank IC（Spearman秩相关系数）
    
    IC > 0: 因子值越高，预期收益越高（正向因子）
    IC < 0: 因子值越低，预期收益越高（反向因子，如16因子量价）
    """
    common = factor_values.index.intersection(forward_returns.index)
    if len(common) < 10:
        return np.nan
    return factor_values.loc[common].rank().corr(forward_returns.loc[common].rank())


def compute_icir(ic_series: pd.Series) -> float:
    """
    计算ICIR = IC均值 / IC标准差
    
    2025年实证：ICIR加权在沪深300上超额10.7%，
    相比IC均值加权的6.8%提升了3.9个百分点。
    """
    ic_mean = ic_series.mean()
    ic_std = ic_series.std()
    if ic_std < 1e-10:
        return 0.0
    return ic_mean / ic_std


def compute_icir_weights(ic_history: pd.DataFrame,
                         lookback: int = 24) -> pd.Series:
    """
    基于历史IC序列计算ICIR权重
    
    Args:
        ic_history: (n_periods × n_factors) IC历史序列
        lookback: 回看窗口期数
    Returns:
        (n_factors,) 归一化后的ICIR权重
    """
    recent = ic_history.tail(lookback)
    ic_mean = recent.mean()
    ic_std = recent.std()
    icir = ic_mean / (ic_std + 1e-8)
    
    # 取绝对值并归一化
    abs_icir = icir.abs()
    weights = abs_icir / abs_icir.sum()
    return weights


# ============================================================
# 五、因子合成
# ============================================================

def equal_weight_composite(factor_df: pd.DataFrame,
                           columns: List[str] = None) -> pd.Series:
    """等权合成综合因子"""
    cols = columns if columns else factor_df.columns.tolist()
    return factor_df[cols].mean(axis=1)


def icir_weight_composite(factor_df: pd.DataFrame,
                          weights: pd.Series) -> pd.Series:
    """ICIR加权合成综合因子"""
    score = pd.Series(0.0, index=factor_df.index)
    for col, w in weights.items():
        if col in factor_df.columns:
            score += w * factor_df[col].fillna(0)
    return score


def custom_weight_composite(factor_df: pd.DataFrame,
                            weights: Dict[str, float]) -> pd.Series:
    """自定义权重因子合成"""
    score = pd.Series(0.0, index=factor_df.index)
    total_w = sum(weights.values())
    for col, w in weights.items():
        if col in factor_df.columns:
            score += (w / total_w) * factor_df[col].fillna(0)
    return score


# ============================================================
# 六、组合构建工具
# ============================================================

def select_top_n(scores: pd.Series, n: int) -> List[str]:
    """按综合得分选取Top N只股票"""
    return scores.nlargest(min(n, len(scores))).index.tolist()


def select_bottom_n(scores: pd.Series, n: int) -> List[str]:
    """按综合得分选取Bottom N只股票（用于反向因子）"""
    return scores.nsmallest(min(n, len(scores))).index.tolist()


def equal_weight_portfolio(stocks: List[str]) -> pd.Series:
    """等权配置组合"""
    if not stocks:
        return pd.Series(dtype=float)
    weight = 1.0 / len(stocks)
    return pd.Series(weight, index=stocks)


def market_cap_weight_portfolio(stocks: List[str],
                                 market_caps: pd.Series) -> pd.Series:
    """市值加权组合"""
    if not stocks:
        return pd.Series(dtype=float)
    caps = market_caps.reindex(stocks).dropna()
    if caps.empty:
        return equal_weight_portfolio(stocks)
    return caps / caps.sum()


# ============================================================
# 七、组合优化约束
# ============================================================

def apply_constraints(weights: pd.Series,
                      benchmark_weights: pd.Series = None,
                      max_active_weight: float = 0.015,
                      single_stock_max: float = 0.05,
                      industry_deviation: float = 0.02,
                      industry_map: Dict[str, str] = None) -> pd.Series:
    """
    应用组合优化约束
    
    - 个股权重偏离 ≤ max_active_weight (默认1.5%)
    - 单股最大权重 ≤ single_stock_max (默认5%)
    """
    w = weights.copy()
    
    # 约束1: 单股最大权重
    w = w.clip(upper=single_stock_max)
    
    # 约束2: 主动权重偏离
    if benchmark_weights is not None:
        bench = benchmark_weights.reindex(w.index).fillna(0)
        active = w - bench
        excess = active.abs()
        if excess.max() > max_active_weight:
            scale = max_active_weight / excess.max()
            w = bench + active * scale
    
    # 归一化
    total = w.sum()
    if total > 0:
        w = w / total
    
    return w


# ============================================================
# 八、绩效评估工具
# ============================================================

def compute_excess_return(portfolio_returns: pd.Series,
                          benchmark_returns: pd.Series) -> Tuple[float, float, float]:
    """
    计算超额收益指标
    
    Returns:
        (年化超额收益, 年化跟踪误差, 信息比率)
    """
    excess = portfolio_returns - benchmark_returns
    periods_per_year = 12  # 假设月频
    
    ann_excess = excess.mean() * periods_per_year
    ann_te = excess.std() * np.sqrt(periods_per_year)
    ir = ann_excess / ann_te if ann_te > 1e-10 else 0.0
    
    return ann_excess, ann_te, ir
