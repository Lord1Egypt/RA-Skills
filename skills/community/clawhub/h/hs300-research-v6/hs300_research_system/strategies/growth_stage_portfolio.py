# -*- coding: utf-8 -*-
"""
成长期优选组合策略 (Growth-Stage Preferred Portfolio)

策略来源：国泰海通证券金融工程研究团队
2025年扣费后累计收益：84.1%（排名第一）
相对中证800累计超额：63.2%
调仓频率：月度
选股范围：全市场 → 三层筛选 → 50只

三层递进式筛选：
  第一层：生命周期定位（现金流三表筛选）→ 成长期个股池
  第二层：成长因子初筛（3因子等权打分）→ 前100只
  第三层：盈利能力优选（4因子等权打分）→ 前50只
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class GrowthStagePortfolioStrategy:
    """
    成长期优选组合策略
    
    核心逻辑：基于企业生命周期理论，通过现金流三表模式识别
    真正处于"成长期"的企业，再叠加成长和盈利因子精选。
    
    成长期企业特征：
      经营净现金流(CFO) > 0  — 自我造血
      投资净现金流(CFI) < 0  — 持续扩产
      筹资净现金流(CFF) > 0  — 外部资金支持
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.rebalance_freq = 'monthly'
        self.growth_pool_size = self.config.get('growth_pool_size', 100)
        self.final_pool_size = self.config.get('final_pool_size', 50)
    
    def get_stock_pool(self, date: str) -> List[str]:
        """获取全市场A股（剔除ST/停牌/次新）"""
        # TODO: 接入真实数据源
        return []
    
    def layer1_life_cycle_filter(self, stocks: List[str], date: str) -> List[str]:
        """
        第一层：生命周期定位 — 现金流三表筛选
        
        筛选条件：
        - CFO > 0: 经营净现金流为正
        - CFI < 0: 投资净现金流为负（扩产）
        - CFF > 0: 筹资净现金流为正（融资支持）
        """
        # TODO: 接入真实现金流数据
        growth_pool = []
        
        for stock in stocks:
            cfo = self._get_operating_cf(stock, date)
            cfi = self._get_investing_cf(stock, date)
            cff = self._get_financing_cf(stock, date)
            
            if cfo is not None and cfi is not None and cff is not None:
                if cfo > 0 and cfi < 0 and cff > 0:
                    growth_pool.append(stock)
        
        return growth_pool
    
    def layer2_growth_screen(self, growth_pool: List[str], date: str) -> List[str]:
        """
        第二层：成长因子初筛 — 3因子等权打分，选前100只
        
        因子：
        1. 一致预期净利润调整 — 分析师边际预期改善
        2. SUE（标准化未预期盈余）— 盈利惊喜程度
        3. 加速增长 — 盈利增速是否在加快
        """
        scores = {}
        for stock in growth_pool:
            f1 = self._calc_forecast_adjustment(stock, date)
            f2 = self._calc_sue(stock, date)
            f3 = self._calc_accelerating_growth(stock, date)
            
            # 等权打分（Rank百分位）
            scores[stock] = (
                self._rank_pct(f1) + self._rank_pct(f2) + self._rank_pct(f3)
            ) / 3
        
        # 选前N只
        sorted_stocks = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [s[0] for s in sorted_stocks[:self.growth_pool_size]]
    
    def layer3_profit_screen(self, preliminary_pool: List[str], date: str) -> List[str]:
        """
        第三层：盈利能力优选 — 4因子等权打分，选前50只
        
        因子：
        1. ROE同比 — 盈利能力的边际改善
        2. ROE — 绝对盈利质量
        3. 研发投入 — 研发费用占比/增速
        4. 动量因子 — 价格趋势性
        """
        scores = {}
        for stock in preliminary_pool:
            f1 = self._calc_roe_yoy(stock, date)
            f2 = self._calc_roe(stock, date)
            f3 = self._calc_rnd_intensity(stock, date)
            f4 = self._calc_momentum(stock, date)
            
            scores[stock] = (
                self._rank_pct(f1) + self._rank_pct(f2) + 
                self._rank_pct(f3) + self._rank_pct(f4)
            ) / 4
        
        sorted_stocks = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [s[0] for s in sorted_stocks[:self.final_pool_size]]
    
    def build_portfolio(self, stocks: List[str], date: str) -> pd.Series:
        """市值加权组合"""
        market_caps = {}
        for stock in stocks:
            cap = self._get_market_cap(stock, date)
            if cap is not None:
                market_caps[stock] = cap
        
        if market_caps:
            total = sum(market_caps.values())
            return pd.Series({s: c/total for s, c in market_caps.items()})
        else:
            return pd.Series(1.0/len(stocks), index=stocks) if stocks else pd.Series(dtype=float)
    
    def run(self, date: str) -> Dict:
        """执行成长期优选组合策略"""
        print(f"\n{'='*60}")
        print(f"[成长期优选组合策略] {date}")
        print(f"{'='*60}")
        
        # Layer 1
        all_stocks = self.get_stock_pool(date)
        growth_pool = self.layer1_life_cycle_filter(all_stocks, date)
        print(f"  [1/4] 全市场: {len(all_stocks)} → 成长期: {len(growth_pool)} 只")
        
        # Layer 2
        preliminary = self.layer2_growth_screen(growth_pool, date)
        print(f"  [2/4] 成长初筛: {len(preliminary)} 只")
        
        # Layer 3
        final = self.layer3_profit_screen(preliminary, date)
        print(f"  [3/4] 盈利优选: {len(final)} 只")
        
        # Portfolio
        weights = self.build_portfolio(final, date)
        print(f"  [4/4] 市值加权组合构建完成")
        
        print(f"\n  ✅ 成长期优选组合执行完成: {len(final)} 只")
        print(f"     前5: {final[:5]}")
        
        return {
            'stocks': final,
            'weights': weights,
            'date': date,
            'strategy': 'growth_stage_portfolio',
            'bench': '000906.SH',  # 中证800
        }
    
    # ---- 内部数据获取方法（需接入真实数据源） ----
    
    def _get_operating_cf(self, stock: str, date: str) -> Optional[float]:
        return None
    
    def _get_investing_cf(self, stock: str, date: str) -> Optional[float]:
        return None
    
    def _get_financing_cf(self, stock: str, date: str) -> Optional[float]:
        return None
    
    def _calc_forecast_adjustment(self, stock: str, date: str) -> Optional[float]:
        return None
    
    def _calc_sue(self, stock: str, date: str) -> Optional[float]:
        return None
    
    def _calc_accelerating_growth(self, stock: str, date: str) -> Optional[float]:
        return None
    
    def _calc_roe_yoy(self, stock: str, date: str) -> Optional[float]:
        return None
    
    def _calc_roe(self, stock: str, date: str) -> Optional[float]:
        return None
    
    def _calc_rnd_intensity(self, stock: str, date: str) -> Optional[float]:
        return None
    
    def _calc_momentum(self, stock: str, date: str) -> Optional[float]:
        return None
    
    def _get_market_cap(self, stock: str, date: str) -> Optional[float]:
        return None
    
    @staticmethod
    def _rank_pct(value, all_values: List[float] = None) -> float:
        """Rank百分位"""
        if all_values is None or len(all_values) == 0:
            return 0.5
        rank = sum(1 for v in all_values if v <= value)
        return rank / len(all_values)
