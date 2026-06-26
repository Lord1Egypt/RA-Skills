# -*- coding: utf-8 -*-
"""
策略基类 — 所有策略的统一接口

每个策略必须实现:
  1. get_stock_pool()    — 获取股票池
  2. calculate_factors() — 计算因子
  3. composite_score()   — 综合得分
  4. build_portfolio()   — 组合构建
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime


class BaseStrategy(ABC):
    """策略基类"""
    
    def __init__(self, name: str, description: str, 
                 rebalance_freq: str = 'monthly', bench: str = ''):
        self.name = name
        self.description = description
        self.rebalance_freq = rebalance_freq  # 'daily', 'weekly', 'monthly'
        self.bench = bench
        self.last_run = None
    
    @abstractmethod
    def get_stock_pool(self, date: str) -> List[str]:
        """获取选股范围"""
        pass
    
    @abstractmethod
    def calculate_factors(self, stocks: List[str], date: str) -> pd.DataFrame:
        """计算因子矩阵 (n_stocks × n_factors)"""
        pass
    
    @abstractmethod
    def composite_score(self, factor_df: pd.DataFrame, **kwargs) -> pd.Series:
        """计算综合得分"""
        pass
    
    @abstractmethod
    def build_portfolio(self, scores: pd.Series, top_n: int = 50,
                        **kwargs) -> Dict:
        """
        构建组合
        
        Returns:
            {'stocks': List[str], 'weights': pd.Series}
        """
        pass
    
    def run(self, date: str, top_n: int = 50, **kwargs) -> Dict:
        """执行完整策略流程"""
        print(f"\n{'='*60}")
        print(f"[{self.name}] 执行中 — {date}")
        print(f"{'='*60}")
        
        # Step 1
        stocks = self.get_stock_pool(date)
        print(f"  [1/4] 股票池: {len(stocks)} 只")
        
        # Step 2
        factor_df = self.calculate_factors(stocks, date)
        print(f"  [2/4] 因子维度: {factor_df.shape}")
        
        # Step 3
        scores = self.composite_score(factor_df, **kwargs)
        
        # Step 4
        result = self.build_portfolio(scores, top_n, **kwargs)
        print(f"  [3/4] 综合得分完成")
        print(f"  [4/4] 选中 {len(result['stocks'])} 只股票")
        
        self.last_run = datetime.now()
        
        return {
            'stocks': result['stocks'],
            'weights': result['weights'],
            'scores': scores,
            'date': date,
            'strategy': self.name,
            'bench': self.bench,
            'rebalance_freq': self.rebalance_freq,
        }
    
    def get_info(self) -> Dict:
        return {
            'name': self.name,
            'description': self.description,
            'rebalance_freq': self.rebalance_freq,
            'bench': self.bench,
            'last_run': self.last_run.isoformat() if self.last_run else None,
        }
