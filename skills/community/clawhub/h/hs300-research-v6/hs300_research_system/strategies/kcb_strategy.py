# -*- coding: utf-8 -*-
"""
科创板策略 (STAR Market Strategy)

策略来源：华福证券
2025年收益：~18.61%
调仓频率：月度
选股范围：科创板全样本

四因子等权模型：
  1. 成长预期因子 — 营收增长率/利润增长率/分析师预期
  2. 研发投入因子 — 研发费用占比/研发人员占比/专利数量
  3. 财务质量因子 — ROE/毛利率/现金流质量
  4. 趋势动量因子 — 价格动量/相对强度/突破信号
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class KCBStrategy:
    """
    科创板策略
    
    核心逻辑：科创板公司普遍处于成长期，高研发投入、高增长预期
    是核心特征。四因子等权模型针对科创板特性设计。
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.rebalance_freq = 'monthly'
        self.top_n = self.config.get('top_n', 30)
        self.factor_weights = {
            'growth_expectation': 0.25,
            'rnd_investment': 0.25,
            'financial_quality': 0.25,
            'trend_momentum': 0.25,
        }
        self.factor_weights.update(self.config.get('factor_weights', {}))
    
    def get_stock_pool(self, date: str) -> List[str]:
        """获取科创板全样本"""
        # TODO: 接入真实数据源 (AKShare可获取科创板成分)
        return []
    
    def calculate_growth_factor(self, stocks: List[str], date: str) -> pd.Series:
        """
        成长预期因子
        
        指标：
        - 营收增长率（同比/环比）
        - 净利润增长率
        - 分析师一致预期营收/利润调整
        """
        scores = {}
        for stock in stocks:
            rev_growth = self._get_revenue_growth(stock, date)
            profit_growth = self._get_profit_growth(stock, date)
            analyst_adj = self._get_analyst_adjustment(stock, date)
            
            valid = [v for v in [rev_growth, profit_growth, analyst_adj] if v is not None]
            scores[stock] = np.mean(valid) if valid else 0
        
        series = pd.Series(scores)
        return series.rank(pct=True) if len(series) > 0 else series
    
    def calculate_rnd_factor(self, stocks: List[str], date: str) -> pd.Series:
        """
        研发投入因子
        
        指标：
        - 研发费用/营收
        - 研发人员占比
        - 专利数量/增长率
        """
        scores = {}
        for stock in stocks:
            rnd_ratio = self._get_rnd_ratio(stock, date)
            rnd_staff = self._get_rnd_staff_ratio(stock, date)
            patents = self._get_patent_count(stock, date)
            
            valid = [v for v in [rnd_ratio, rnd_staff, patents] if v is not None]
            scores[stock] = np.mean(valid) if valid else 0
        
        series = pd.Series(scores)
        return series.rank(pct=True) if len(series) > 0 else series
    
    def calculate_financial_factor(self, stocks: List[str], date: str) -> pd.Series:
        """
        财务质量因子
        
        指标：
        - ROE
        - 毛利率
        - 经营现金流/净利润（现金流质量）
        """
        scores = {}
        for stock in stocks:
            roe = self._get_roe(stock, date)
            gross_margin = self._get_gross_margin(stock, date)
            cash_quality = self._get_cash_flow_quality(stock, date)
            
            valid = [v for v in [roe, gross_margin, cash_quality] if v is not None]
            scores[stock] = np.mean(valid) if valid else 0
        
        series = pd.Series(scores)
        return series.rank(pct=True) if len(series) > 0 else series
    
    def calculate_momentum_factor(self, stocks: List[str], date: str) -> pd.Series:
        """
        趋势动量因子
        
        指标：
        - 20日/60日价格动量
        - 相对强度（相对科创板指数）
        - 突破信号（创新高次数）
        """
        scores = {}
        for stock in stocks:
            mom_20d = self._get_momentum(stock, date, days=20)
            mom_60d = self._get_momentum(stock, date, days=60)
            relative_strength = self._get_relative_strength(stock, date)
            
            valid = [v for v in [mom_20d, mom_60d, relative_strength] if v is not None]
            scores[stock] = np.mean(valid) if valid else 0
        
        series = pd.Series(scores)
        return series.rank(pct=True) if len(series) > 0 else series
    
    def composite_score(self, growth: pd.Series, rnd: pd.Series,
                        financial: pd.Series, momentum: pd.Series) -> pd.Series:
        """四因子等权合成"""
        score = (
            self.factor_weights['growth_expectation'] * growth +
            self.factor_weights['rnd_investment'] * rnd +
            self.factor_weights['financial_quality'] * financial +
            self.factor_weights['trend_momentum'] * momentum
        )
        return score
    
    def run(self, date: str) -> Dict:
        """执行科创板策略"""
        print(f"\n{'='*60}")
        print(f"[科创板策略] {date}")
        print(f"{'='*60}")
        
        stocks = self.get_stock_pool(date)
        print(f"  [1/5] 科创板股票: {len(stocks)} 只")
        
        growth = self.calculate_growth_factor(stocks, date)
        rnd = self.calculate_rnd_factor(stocks, date)
        financial = self.calculate_financial_factor(stocks, date)
        momentum = self.calculate_momentum_factor(stocks, date)
        print(f"  [2/5] 四因子计算完成")
        
        scores = self.composite_score(growth, rnd, financial, momentum)
        print(f"  [3/5] 等权合成完成")
        
        top = scores.nlargest(self.top_n).index.tolist()
        print(f"  [4/5] 选中 {len(top)} 只")
        
        weights = pd.Series(1.0/len(top), index=top) if top else pd.Series(dtype=float)
        print(f"  [5/5] 等权组合构建完成")
        
        print(f"\n  ✅ 科创板策略执行完成")
        print(f"     前5: {top[:5]}")
        
        return {
            'stocks': top,
            'weights': weights,
            'scores': scores,
            'date': date,
            'strategy': 'kcb_strategy',
            'bench': '000688.SH',  # 科创50
        }
    
    # ---- 内部数据获取方法（需接入真实数据源） ----
    def _get_revenue_growth(self, stock, date): return None
    def _get_profit_growth(self, stock, date): return None
    def _get_analyst_adjustment(self, stock, date): return None
    def _get_rnd_ratio(self, stock, date): return None
    def _get_rnd_staff_ratio(self, stock, date): return None
    def _get_patent_count(self, stock, date): return None
    def _get_roe(self, stock, date): return None
    def _get_gross_margin(self, stock, date): return None
    def _get_cash_flow_quality(self, stock, date): return None
    def _get_momentum(self, stock, date, days=20): return None
    def _get_relative_strength(self, stock, date): return None
