"""
王国斌投资方法 - 泉果基金创始人

核心理念：
1. 幸运的行业+能干的企业+合理价格
2. 投资中国最优秀的公司
3. 长期持有
4. 注重企业质地

代表案例：
- 《投资中国》
"""

from typing import Dict, List
from investment_gurus.base import BaseGuru, StockAnalysis, GuruFactory


class WangGuobin(BaseGuru):
    """王国斌投资方法"""
    
    name = "王国斌"
    alias = "泉果基金创始人"
    background = """
    泉果基金创始人，曾任东方红资管董事长。
    20多年A股实战经验，被誉为"A股第一代价投"。
    """
    
    core_philosophy = """
    1. 幸运的行业 - 选择比努力重要
    2. 能干的企业 - 优秀的管理层
    3. 合理价格 - 不必等待极端低估
    4. 价值投资 - 陪伴优秀企业成长
    5. 长期视角 - 以3-5年为单位
    """
    
    key_principles = [
        "幸运的行业",
        "能干的企业",
        "合理价格",
        "长期持有",
        "价值投资",
        "企业质地",
    ]
    
    representative_cases = {
        "茅台": "长期持有",
        "腾讯": "互联网龙头",
        "美的": "制造业标杆",
    }
    
    suitable_sectors = [
        "消费",
        "科技",
        "先进制造",
    ]
    
    def analyze_stock(self, stock_code: str, **kwargs) -> StockAnalysis:
        stock_name = kwargs.get("stock_name", stock_code)
        
        business_score = self.evaluate_business(stock_code)
        valuation_score = self.evaluate_valuation(stock_code)
        growth_score = self.evaluate_growth(stock_code)
        competitive_score = self.evaluate_competitive(stock_code)
        management_score = self.evaluate_management(stock_code)
        
        # 行业最重要
        overall = (
            business_score * 0.30 +
            competitive_score * 0.25 +
            management_score * 0.20 +
            valuation_score * 0.15 +
            growth_score * 0.10
        )
        
        recommendation = self.get_recommendation({"overall": overall})
        
        return StockAnalysis(
            stock_code=stock_code,
            stock_name=stock_name,
            guru_name=self.name,
            guru_method="幸运的行业+能干的企业+合理价格",
            overall_score=round(overall, 1),
            business_score=business_score,
            valuation_score=valuation_score,
            growth_score=growth_score,
            competitive_score=competitive_score,
            management_score=management_score,
            recommendation=recommendation,
            holding_period="中长期",
            pros=self._get_pros(stock_code),
            cons=self._get_cons(stock_code),
            key_points=self._get_key_points(stock_code),
        )
    
    def evaluate_business(self, stock_code: str) -> float:
        """幸运的行业"""
        score = 60.0
        
        if stock_code in ["002594", "比亚迪"]:
            score = 95.0  # 新能源是好行业
        elif stock_code in ["600519", "贵州茅台"]:
            score = 95.0  # 白酒是好行业
            
        return score
    
    def evaluate_management(self, stock_code: str) -> float:
        """能干的企业"""
        score = 65.0
        
        if stock_code in ["002594", "比亚迪", "000333", "美的"]:
            score = 90.0
            
        return score
    
    def _get_pros(self, stock_code: str) -> List[str]:
        return [
            "幸运的行业",
            "能干的企业",
            "合理价格",
        ]
    
    def _get_cons(self, stock_code: str) -> List[str]:
        return [
            "好行业好公司不便宜",
            "需要长期持有",
        ]
    
    def _get_key_points(self, stock_code: str) -> List[str]:
        return [
            "是否是幸运的行业（空间大、门槛高）？",
            "是否是能干的企业（管理层优秀）？",
            "价格是否合理？",
        ]


GuruFactory.register("wangguobin", WangGuobin)
GuruFactory.register("王国斌", WangGuobin)