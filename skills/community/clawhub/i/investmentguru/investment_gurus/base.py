"""
投资大师基类 - 定义通用接口和方法
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class StockAnalysis:
    """股票分析结果"""
    stock_code: str
    stock_name: str
    guru_name: str
    guru_method: str
    
    # 评分 (0-100)
    overall_score: float
    
    # 各维度评分
    business_score: float      # 商业模式
    valuation_score: float     # 估值合理性
    growth_score: float        # 成长性
    competitive_score: float   # 竞争优势
    management_score: float    # 管理团队
    
    # 建议
    recommendation: str        # 买入/持有/卖出
    target_price: Optional[float] = None
    holding_period: str = "长期"  # 短期/中期/长期
    
    # 分析要点
    pros: List[str] = None     # 优势
    cons: List[str] = None     # 风险
    key_points: List[str] = None  # 关键点
    
    def __post_init__(self):
        if self.pros is None:
            self.pros = []
        if self.cons is None:
            self.cons = []
        if self.key_points is None:
            self.key_points = []
    
    def to_dict(self) -> Dict:
        return {
            "stock_code": self.stock_code,
            "stock_name": self.stock_name,
            "guru": self.guru_name,
            "method": self.guru_method,
            "scores": {
                "overall": self.overall_score,
                "business": self.business_score,
                "valuation": self.valuation_score,
                "growth": self.growth_score,
                "competitive": self.competitive_score,
                "management": self.management_score,
            },
            "recommendation": self.recommendation,
            "target_price": self.target_price,
            "holding_period": self.holding_period,
            "pros": self.pros,
            "cons": self.cons,
            "key_points": self.key_points,
        }


class BaseGuru(ABC):
    """投资大师基类"""
    
    # 大师信息
    name: str = ""
    alias: str = ""
    background: str = ""
    
    # 核心理念
    core_philosophy: str = ""
    key_principles: List[str] = []
    
    # 代表案例
    representative_cases: Dict[str, str] = {}
    
    # 适用场景
    suitable_sectors: List[str] = []
    suitable_stocks: List[str] = []
    
    def __init__(self):
        self.name = self.__class__.name
        self.alias = self.__class__.alias
        self.background = self.__class__.background
    
    @abstractmethod
    def analyze_stock(self, stock_code: str, **kwargs) -> StockAnalysis:
        """
        分析股票
        
        Args:
            stock_code: 股票代码
            
        Returns:
            StockAnalysis: 分析结果
        """
        pass
    
    def evaluate_business(self, stock_code: str) -> float:
        """
        评估商业模式 (0-100)
        """
        return 50.0
    
    def evaluate_valuation(self, stock_code: str) -> float:
        """
        评估估值合理性 (0-100)
        """
        return 50.0
    
    def evaluate_growth(self, stock_code: str) -> float:
        """
        评估成长性 (0-100)
        """
        return 50.0
    
    def evaluate_competitive(self, stock_code: str) -> float:
        """
        评估竞争优势 (0-100)
        """
        return 50.0
    
    def evaluate_management(self, stock_code: str) -> float:
        """
        评估管理团队 (0-100)
        """
        return 50.0
    
    def get_recommendation(self, scores: Dict[str, float]) -> str:
        """根据评分给出建议"""
        overall = scores.get("overall", 50)
        if overall >= 80:
            return "强烈推荐买入"
        elif overall >= 65:
            return "建议买入"
        elif overall >= 50:
            return "持有观察"
        elif overall >= 35:
            return "建议减仓"
        else:
            return "建议卖出"
    
    def get_info(self) -> Dict:
        """获取大师信息"""
        return {
            "name": self.name,
            "alias": self.alias,
            "background": self.background,
            "philosophy": self.core_philosophy,
            "principles": self.key_principles,
            "cases": self.representative_cases,
            "sectors": self.suitable_sectors,
        }
    
    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"


class GuruFactory:
    """投资大师工厂"""
    
    _gurus: Dict[str, type] = {}
    
    @classmethod
    def register(cls, name: str, guru_class: type):
        cls._gurus[name] = guru_class
    
    @classmethod
    def create(cls, name: str) -> Optional[BaseGuru]:
        if name in cls._gurus:
            return cls._gurus[name]()
        return None
    
    @classmethod
    def get_all_gurus(cls) -> Dict[str, type]:
        return cls._gurus.copy()


# 注册所有大师
from investment_gurus.duan import DuanYongping
from investment_gurus.zhanglei import ZhangLei
from investment_gurus.liu_lu import LiLu
from investment_gurus.qiuguoluo import QiuGuoluo
from investment_gurus.wangguobin import WangGuobin
from investment_gurus.linyuan import LinYuan
from investment_gurus.danbing import DanBing

GuruFactory.register("duan", DuanYongping)
GuruFactory.register("段永平", DuanYongping)
GuruFactory.register("zhanglei", ZhangLei)
GuruFactory.register("张磊", ZhangLei)
GuruFactory.register("lilu", LiLu)
GuruFactory.register("李录", LiLu)
GuruFactory.register("qiuguoluo", QiuGuoluo)
GuruFactory.register("邱国鹭", QiuGuoluo)
GuruFactory.register("wangguobin", WangGuobin)
GuruFactory.register("王国斌", WangGuobin)
GuruFactory.register("linyuan", LinYuan)
GuruFactory.register("林园", LinYuan)
GuruFactory.register("danbing", DanBing)
GuruFactory.register("但斌", DanBing)