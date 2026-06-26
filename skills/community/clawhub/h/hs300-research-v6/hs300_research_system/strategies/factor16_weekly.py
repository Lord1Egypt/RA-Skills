# -*- coding: utf-8 -*-
"""
16因子综合量价策略（周度调仓版）

策略来源：方正金工
多空年化收益：82.67%
周度最大回撤：5.75%
调仓频率：周度

与月频版的区别：
  - 调仓频率：月度 → 周度（每周一调仓）
  - 平滑窗口：5日 → 3日（更灵敏）
  - 交易成本更高，但Alpha捕获效率更高
"""

from .factor16_monthly import Factor16MonthlyStrategy
from typing import Dict, List, Optional, Tuple
import pandas as pd


class Factor16WeeklyStrategy(Factor16MonthlyStrategy):
    """16因子综合量价策略（周度版）— 继承月频版，仅调整参数"""
    
    def __init__(self, config: Optional[Dict] = None):
        config = config or {}
        config['smoothing_window'] = config.get('smoothing_window', 3)  # 更短平滑
        config['top_n'] = config.get('top_n', 50)
        config['bottom_n'] = config.get('bottom_n', 50)
        super().__init__(config)
        self.rebalance_freq = 'weekly'
    
    def run(self, date: str) -> Dict:
        """执行16因子量价周度策略"""
        print(f"\n{'='*60}")
        print(f"[16因子综合量价(周频)] {date}")
        print(f"{'='*60}")
        
        stocks = self.get_stock_pool(date)
        print(f"  [1/5] 股票池: {len(stocks)} 只")
        
        factor_df = self.calculate_16_factors(stocks, date)
        print(f"  [2/5] 16因子计算完成: {factor_df.shape}")
        
        smoothed = self.smooth_factors(factor_df, self.smoothing_window)
        print(f"  [3/5] {self.smoothing_window}日平滑完成")
        
        processed = self.preprocess_factors(smoothed)
        ortho = self.orthogonalize_factors(processed)
        print(f"  [4/5] 预处理+正交化完成")
        
        scores = self.composite_score(ortho)
        long_stocks, short_stocks = self.select_stocks(scores)
        print(f"  [5/5] 多头{len(long_stocks)}只 / 空头{len(short_stocks)}只")
        
        print(f"\n  ✅ 16因子量价周频策略执行完成")
        print(f"     多头前5: {long_stocks[:5]}")
        print(f"     空头前5: {short_stocks[:5]}")
        
        return {
            'long': long_stocks,
            'short': short_stocks,
            'scores': scores,
            'date': date,
            'strategy': 'factor16_weekly',
            'rebalance_freq': 'weekly',
        }
