"""
张磊投资方法 - 高瓴资本超长期主义

核心理念：
1. 超长期主义 - 做时间的朋友
2. 重仓中国
3. 动态护城河
4. 价值创造
5. 企业家精神

代表案例：
- 早期投资腾讯，持有超20年，收益300多倍
- 投资京东、格力、隆基绿能、百济神州
"""

from typing import Dict, List
from investment_gurus.base import BaseGuru, StockAnalysis, GuruFactory


class ZhangLei(BaseGuru):
    """张磊投资方法"""
    
    name = "张磊"
    alias = "高瓴资本创始人"
    background = """
    高瓴资本创始人，耶鲁大学校友基金投资主管。
    管理资产规模超1000亿美元，是亚洲最大私募之一。
    """
    
    core_philosophy = """
    1. 超长期主义 - 与优秀企业共同成长10年以上
    2. 重仓中国 - 相信中国的创新和增长潜力
    3. 动态护城河 - 护城河不是静态的，要持续创新
    4. 价值创造 - 不仅是投资，还要帮助企业创造价值
    5. 企业家精神 - 投资有格局的企业家
    """
    
    key_principles = [
        "超长期主义",
        "重仓中国",
        "动态护城河",
        "价值创造",
        "企业家精神",
        "长期持有",
        "逆向投资",
        "产业投资",
    ]
    
    representative_cases = {
        "腾讯": "2005年投资，持有超20年，收益300多倍",
        "京东": "2011年重仓，陪伴成长",
        "格力": "重仓家电龙头",
        "隆基绿能": "新能源赛道重仓",
        "百济神州": "创新药赛道重仓",
    }
    
    suitable_sectors = [
        "互联网",
        "消费",
        "医疗健康",
        "新能源",
        "先进制造",
    ]
    
    def analyze_stock(self, stock_code: str, **kwargs) -> StockAnalysis:
        """
        张磊方法分析股票
        
        重点关注：
        1. 是否有长期增长潜力
        2. 是否能持续创造价值
        3. 企业家是否靠谱
        4. 是否有动态护城河
        """
        stock_name = kwargs.get("stock_name", stock_code)
        
        business_score = self.evaluate_business(stock_code)
        valuation_score = self.evaluate_valuation(stock_code)
        growth_score = self.evaluate_growth(stock_code)
        competitive_score = self.evaluate_competitive(stock_code)
        management_score = self.evaluate_management(stock_code)
        
        # 张磊最看重成长性和管理团队
        overall = (
            growth_score * 0.30 +
            management_score * 0.25 +
            business_score * 0.20 +
            competitive_score * 0.15 +
            valuation_score * 0.10
        )
        
        recommendation = self.get_recommendation({"overall": overall})
        
        pros = self._get_pros(stock_code)
        cons = self._get_cons(stock_code)
        key_points = self._get_key_points(stock_code)
        
        return StockAnalysis(
            stock_code=stock_code,
            stock_name=stock_name,
            guru_name=self.name,
            guru_method="超长期主义+动态护城河",
            overall_score=round(overall, 1),
            business_score=business_score,
            valuation_score=valuation_score,
            growth_score=growth_score,
            competitive_score=competitive_score,
            management_score=management_score,
            recommendation=recommendation,
            holding_period="超长期（5-10年以上）",
            pros=pros,
            cons=cons,
            key_points=key_points,
        )
    
    def evaluate_growth(self, stock_code: str) -> float:
        """
        评估成长性 - 张磊最看重这个
        是否有长期增长空间
        """
        score = 65.0
        
        # 高成长赛道
        if stock_code in ["002594", "比亚迪", "300750", "宁德时代"]:
            score = 95.0  # 新能源龙头
        elif stock_code in ["600276", "恒瑞医药"]:
            score = 88.0  # 创新药
        elif stock_code in ["00700", "腾讯"]:
            score = 85.0  # 互联网龙头
        elif stock_code in ["600519", "贵州茅台"]:
            score = 75.0  # 稳定增长
            
        return score
    
    def evaluate_management(self, stock_code: str) -> float:
        """
        评估管理团队 - 企业家精神
        """
        score = 70.0
        
        # 优秀企业家
        if stock_code in ["002594", "比亚迪"]:
            score = 95.0  # 王传福
        elif stock_code in ["000333", "美的集团"]:
            score = 90.0  # 方洪波
        elif stock_code in ["00700", "腾讯"]:
            score = 88.0  # 马化腾
        elif stock_code in ["600276", "恒瑞医药"]:
            score = 85.0  # 孙飘扬
            
        return score
    
    def _get_pros(self, stock_code: str) -> List[str]:
        pros = [
            "长期增长潜力大",
            "行业空间广阔",
            "具有企业家精神的管理层",
        ]
        
        if stock_code in ["002594", "比亚迪"]:
            pros.extend([
                "新能源汽车龙头",
                "技术储备深厚",
                "全球竞争力强",
            ])
        
        return pros
    
    def _get_cons(self, stock_code: str) -> List[str]:
        return [
            "短期估值可能较高",
            "需要长期持有",
            "竞争格局可能变化",
        ]
    
    def _get_key_points(self, stock_code: str) -> List[str]:
        return [
            "是否有10年以上的增长潜力？",
            "企业家是否具有长期视野？",
            "能否持续创造价值（而不仅是赚钱）？",
            "护城河是否能持续加宽？",
            "是否愿意与之共同成长10年？",
        ]


GuruFactory.register("zhanglei", ZhangLei)
GuruFactory.register("张磊", ZhangLei)