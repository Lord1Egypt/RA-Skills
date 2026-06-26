"""
李录投资方法 - 芒格家族资产管理人

核心理念：
1. 文明视角 - 从历史文明角度看投资
2. 跨市场投资 - 中美市场都要关注
3. 极度安全边际 - 宁可错过不要买贵
4. 长期价值 - 伴随伟大企业成长

代表案例：
- 查理·芒格唯一公开认可的中国投资人
- 投资比亚迪等
"""

from typing import Dict, List
from investment_gurus.base import BaseGuru, StockAnalysis, GuruFactory


class LiLu(BaseGuru):
    """李录投资方法"""
    
    name = "李录"
    alias = "芒格家族资产管理人"
    background = """
    喜马拉雅资本创始人，查理·芒格家族资产管理人。
    芒格唯一公开认可的中国投资人，管理的资产超100亿美元。
    """
    
    core_philosophy = """
    1. 文明视角 - 从人类文明演进角度看投资
    2. 跨市场配置 - 同时关注中美市场机会
    3. 极度安全边际 - 宁错过不做错
    4. 长期持有 - 与优秀企业共同成长
    5. 能力圈投资 - 只投自己真正懂的
    """
    
    key_principles = [
        "文明视角",
        "跨市场投资",
        "极度安全边际",
        "长期价值",
        "能力圈",
        "逆向思维",
        "价值投资",
    ]
    
    representative_cases = {
        "比亚迪": "早期投资，获利丰厚",
        "贵州茅台": "长期持有",
        "招商银行": "金融板块代表",
    }
    
    suitable_sectors = [
        "消费",
        "科技",
        "金融",
        "新能源",
    ]
    
    def analyze_stock(self, stock_code: str, **kwargs) -> StockAnalysis:
        stock_name = kwargs.get("stock_name", stock_code)
        
        # 李录极度重视安全边际
        business_score = self.evaluate_business(stock_code)
        valuation_score = self.evaluate_valuation(stock_code)
        growth_score = self.evaluate_growth(stock_code)
        competitive_score = self.evaluate_competitive(stock_code)
        management_score = self.evaluate_management(stock_code)
        
        # 安全边际最重要
        overall = (
            valuation_score * 0.35 +
            business_score * 0.25 +
            competitive_score * 0.20 +
            management_score * 0.10 +
            growth_score * 0.10
        )
        
        recommendation = self.get_recommendation({"overall": overall})
        
        return StockAnalysis(
            stock_code=stock_code,
            stock_name=stock_name,
            guru_name=self.name,
            guru_method="文明视角+极度安全边际",
            overall_score=round(overall, 1),
            business_score=business_score,
            valuation_score=valuation_score,
            growth_score=growth_score,
            competitive_score=competitive_score,
            management_score=management_score,
            recommendation=recommendation,
            holding_period="长期",
            pros=self._get_pros(stock_code),
            cons=self._get_cons(stock_code),
            key_points=self._get_key_points(stock_code),
        )
    
    def evaluate_valuation(self, stock_code: str) -> float:
        """李录最看重估值 - 极度安全边际"""
        score = 65.0
        
        # 只有非常便宜时才买
        if stock_code in ["600519", "贵州茅台"]:
            score = 80.0  # 茅台pe正常30-40
        elif stock_code in ["000001", "平安银行"]:
            score = 75.0  # 银行估值低
            
        return score
    
    def _get_pros(self, stock_code: str) -> List[str]:
        return [
            "安全边际足够",
            "商业模式清晰",
            "长期价值明显",
        ]
    
    def _get_cons(self, stock_code: str) -> List[str]:
        return [
            "需要等待好价格",
            "可能错过热点",
        ]
    
    def _get_key_points(self, stock_code: str) -> List[str]:
        return [
            "是否有足够的安全边际？",
            "是否真正理解这个生意？",
            "能否承受50%的下跌？",
        ]


GuruFactory.register("lilu", LiLu)
GuruFactory.register("李录", LiLu)