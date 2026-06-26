"""
但斌投资方法 - 东方港湾

核心理念：
1. 长期持有伟大企业
2. 世界改变不了的公司
3. 改变世界的公司
4. 时间的玫瑰

代表案例：
- 《时间的玫瑰》
- 长期持有茅台、腾讯
"""

from typing import Dict, List
from investment_gurus.base import BaseGuru, StockAnalysis, GuruFactory


class DanBing(BaseGuru):
    """但斌投资方法"""
    
    name = "但斌"
    alias = "东方港湾创始人"
    background = """
    东方港湾创始人，知名私募基金经理。
    《时间的玫瑰》作者，价值投资布道者。
    """
    
    core_philosophy = """
    1. 长期持有 - 伴随伟大企业成长
    2. 世界改变不了的公司 - 茅台等消费龙头
    3. 改变世界的公司 - 科技股
    4. 时间的玫瑰 - 时间是最好朋友
    5. 组合投资 - 分散但集中于好公司
    """
    
    key_principles = [
        "长期持有",
        "伟大企业",
        "世界改变不了",
        "改变世界",
        "时间的玫瑰",
        "价值投资",
    ]
    
    representative_cases = {
        "贵州茅台": "持有10年以上",
        "腾讯": "互联网龙头",
        "苹果": "全球最成功企业",
        "亚马逊": "改变世界",
    }
    
    suitable_sectors = [
        "消费",
        "互联网",
        "科技",
        "高端制造",
    ]
    
    def analyze_stock(self, stock_code: str, **kwargs) -> StockAnalysis:
        stock_name = kwargs.get("stock_name", stock_code)
        
        business_score = self.evaluate_business(stock_code)
        valuation_score = self.evaluate_valuation(stock_code)
        growth_score = self.evaluate_growth(stock_code)
        competitive_score = self.evaluate_competitive(stock_code)
        management_score = self.evaluate_management(stock_code)
        
        # 商业模式和竞争优势最重要
        overall = (
            business_score * 0.30 +
            competitive_score * 0.30 +
            growth_score * 0.15 +
            management_score * 0.15 +
            valuation_score * 0.10
        )
        
        recommendation = self.get_recommendation({"overall": overall})
        
        return StockAnalysis(
            stock_code=stock_code,
            stock_name=stock_name,
            guru_name=self.name,
            guru_method="长期持有伟大企业+时间的玫瑰",
            overall_score=round(overall, 1),
            business_score=business_score,
            valuation_score=valuation_score,
            growth_score=growth_score,
            competitive_score=competitive_score,
            management_score=management_score,
            recommendation=recommendation,
            holding_period="长期（5-10年以上）",
            pros=self._get_pros(stock_code),
            cons=self._get_cons(stock_code),
            key_points=self._get_key_points(stock_code),
        )
    
    def evaluate_business(self, stock_code: str) -> float:
        """伟大企业"""
        score = 60.0
        
        # 改变不了的公司
        if stock_code in ["600519", "贵州茅台"]:
            score = 100.0
        elif stock_code in ["00700", "腾讯"]:
            score = 90.0
        elif stock_code in ["AAPL", "苹果"]:
            score = 95.0
        elif stock_code in ["AMZN", "亚马逊"]:
            score = 90.0
            
        return score
    
    def evaluate_competitive(self, stock_code: str) -> float:
        """竞争优势"""
        score = 60.0
        
        if stock_code in ["600519", "贵州茅台"]:
            score = 100.0
        elif stock_code in ["00700", "腾讯"]:
            score = 90.0
        elif stock_code in ["AAPL", "苹果"]:
            score = 95.0
            
        return score
    
    def _get_pros(self, stock_code: str) -> List[str]:
        pros = [
            "伟大企业",
            "长期增长潜力",
        ]
        
        if stock_code in ["600519", "贵州茅台"]:
            pros.extend(["世界改变不了的公司", "时间的玫瑰"])
        elif stock_code in ["00700", "腾讯"]:
            pros.extend(["社交护城河", "生态优势"])
            
        return pros
    
    def _get_cons(self, stock_code: str) -> List[str]:
        return [
            "短期可能下跌",
            "需要长期坚持",
            "估值波动大",
        ]
    
    def _get_key_points(self, stock_code: str) -> List[str]:
        return [
            "是否是伟大企业？",
            "能否改变世界或世界改变不了？",
            "能否持有10年以上？",
            "是否愿意与时间做朋友？",
        ]


GuruFactory.register("danbing", DanBing)
GuruFactory.register("但斌", DanBing)