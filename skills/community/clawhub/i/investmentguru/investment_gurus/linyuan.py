"""
林园投资方法 - 民间股神

核心理念：
1. 嘴巴经济 - 投资与嘴巴相关的企业
2. 垄断成瘾 - 寻找垄断企业
3. 集中投资 - 重仓少数几只股票
4. 长期持有 - 持有到永远

代表案例：
- 持有贵州茅台、片仔癀超20年，收益数百倍
"""

from typing import Dict, List
from investment_gurus.base import BaseGuru, StockAnalysis, GuruFactory


class LinYuan(BaseGuru):
    """林园投资方法"""
    
    name = "林园"
    alias = "民间股神"
    background = """
    民间知名投资人，从8000元起家到百亿身家。
    20多年专注消费和医药，被称"民间股神"。
    """
    
    core_philosophy = """
    1. 嘴巴经济 - 投资民以食为天相关的企业
    2. 垄断成瘾 - 寻找具有垄断地位的企业
    3. 集中投资 - 重仓少数几只股票
    4. 长期持有 - 持有到永远
    5. 确定性优先 - 只投确定性高的
    """
    
    key_principles = [
        "嘴巴经济",
        "垄断成瘾",
        "集中投资",
        "长期持有",
        "确定性",
        "消费",
        "医药",
    ]
    
    representative_cases = {
        "贵州茅台": "持有20多年，收益数百倍",
        "片仔癀": "中药垄断，持有多年",
        "五粮液": "白酒龙头",
        "同仁堂": "中药老字号",
    }
    
    suitable_sectors = [
        "白酒",
        "医药",
        "食品饮料",
        "消费",
    ]
    
    def analyze_stock(self, stock_code: str, **kwargs) -> StockAnalysis:
        stock_name = kwargs.get("stock_name", stock_code)
        
        business_score = self.evaluate_business(stock_code)
        valuation_score = self.evaluate_valuation(stock_code)
        growth_score = self.evaluate_growth(stock_code)
        competitive_score = self.evaluate_competitive(stock_code)
        management_score = self.evaluate_management(stock_code)
        
        # 垄断和嘴巴最重要
        overall = (
            competitive_score * 0.35 +
            business_score * 0.30 +
            valuation_score * 0.15 +
            growth_score * 0.10 +
            management_score * 0.10
        )
        
        recommendation = self.get_recommendation({"overall": overall})
        
        return StockAnalysis(
            stock_code=stock_code,
            stock_name=stock_name,
            guru_name=self.name,
            guru_method="嘴巴经济+垄断成瘾",
            overall_score=round(overall, 1),
            business_score=business_score,
            valuation_score=valuation_score,
            growth_score=growth_score,
            competitive_score=competitive_score,
            management_score=management_score,
            recommendation=recommendation,
            holding_period="长期（10年以上）",
            pros=self._get_pros(stock_code),
            cons=self._get_cons(stock_code),
            key_points=self._get_key_points(stock_code),
        )
    
    def evaluate_competitive(self, stock_code: str) -> float:
        """垄断成瘾"""
        score = 60.0
        
        # 垄断企业
        if stock_code in ["600519", "贵州茅台"]:
            score = 100.0  # 最强垄断
        elif stock_code in ["600436", "片仔癀"]:
            score = 95.0   # 绝密配方垄断
        elif stock_code in ["000858", "五粮液"]:
            score = 85.0   # 白酒龙头
        elif stock_code in ["600276", "恒瑞医药"]:
            score = 80.0   # 医药龙头
            
        return score
    
    def evaluate_business(self, stock_code: str) -> float:
        """嘴巴经济"""
        score = 60.0
        
        # 嘴巴相关
        if stock_code in ["600519", "贵州茅台", "000858", "五粮液"]:
            score = 95.0  # 白酒
        elif stock_code in ["600436", "片仔癀"]:
            score = 90.0  # 医药
        elif stock_code in ["600887", "伊利股份"]:
            score = 80.0  # 乳制品
            
        return score
    
    def _get_pros(self, stock_code: str) -> List[str]:
        pros = [
            "嘴巴经济，刚需",
        ]
        
        if stock_code in ["600519", "贵州茅台"]:
            pros.extend(["最强垄断", "品牌溢价", "存货升值"])
        elif stock_code in ["600436", "片仔癀"]:
            pros.extend(["绝密配方", "持续提价"])
            
        return pros
    
    def _get_cons(self, stock_code: str) -> List[str]:
        return [
            "股价波动大",
            "需要长期持有",
            "可能高估值",
        ]
    
    def _get_key_points(self, stock_code: str) -> List[str]:
        return [
            "是否与嘴巴相关（刚需）？",
            "是否有垄断地位？",
            "能否持续提价？",
            "能否持有10年以上？",
        ]


GuruFactory.register("linyuan", LinYuan)
GuruFactory.register("林园", LinYuan)