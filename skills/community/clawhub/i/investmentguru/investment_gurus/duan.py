"""
段永平投资方法 - 中国巴菲特

核心理念：
1. 买股票就是买公司
2. 不懂不做（能力圈）
3. 长期持有
4. 严守估值底线
5. 不预测市场

代表案例：
- 2001年抄底网易（1美元以下），赚100多倍
- 长期重仓苹果、茅台
"""

from typing import Dict, List
from investment_gurus.base import BaseGuru, StockAnalysis, GuruFactory


class DuanYongping(BaseGuru):
    """段永平投资方法"""
    
    name = "段永平"
    alias = "中国巴菲特"
    background = """
    步步高/OPPO/VIVO创始人，2001年开始投资生涯。
    以价值投资著称，被誉为"中国巴菲特"。
    """
    
    core_philosophy = """
    1. 买股票就是买公司 - 不关心短期波动，关注企业本质
    2. 不懂不做 - 只投资自己能力圈内的公司
    3. 长期持有 - 持有可能是一辈子
    4. 商业模式优先 - 重视企业的竞争壁垒和商业模式
    5. 合理价格买好公司 - 不追高，等低估
    """
    
    key_principles = [
        "买股票就是买公司",
        "不懂不做",
        "长期持有",
        "价值投资",
        "安全边际",
        "不预测市场",
        "能力圈原则",
        "商业模式为王",
    ]
    
    representative_cases = {
        "网易": "2001年1美元以下买入，持有至100美元以上，收益超100倍",
        "苹果": "2011年开始重仓，长期持有至今",
        "贵州茅台": "长期持有，高端白酒商业模式最优",
        "腾讯": "在市场恐慌时买入，长期持有",
    }
    
    suitable_sectors = [
        "消费",
        "互联网",
        "高端制造",
        "白酒",
    ]
    
    def analyze_stock(self, stock_code: str, **kwargs) -> StockAnalysis:
        """
        段永平方法分析股票
        
        重点关注：
        1. 商业模式是否理解
        2. 是否有竞争壁垒
        3. 管理层是否靠谱
        4. 估值是否合理
        """
        stock_name = kwargs.get("stock_name", stock_code)
        
        # 评估各维度
        business_score = self.evaluate_business(stock_code)
        valuation_score = self.evaluate_valuation(stock_code)
        growth_score = self.evaluate_growth(stock_code)
        competitive_score = self.evaluate_competitive(stock_code)
        management_score = self.evaluate_management(stock_code)
        
        # 段永平最看重商业模式和竞争优势
        overall = (
            business_score * 0.30 +
            competitive_score * 0.25 +
            valuation_score * 0.20 +
            management_score * 0.15 +
            growth_score * 0.10
        )
        
        recommendation = self.get_recommendation({"overall": overall})
        
        # 构建分析要点
        pros = self._get_pros(stock_code)
        cons = self._get_cons(stock_code)
        key_points = self._get_key_points(stock_code)
        
        return StockAnalysis(
            stock_code=stock_code,
            stock_name=stock_name,
            guru_name=self.name,
            guru_method="能力圈+商业模式",
            overall_score=round(overall, 1),
            business_score=business_score,
            valuation_score=valuation_score,
            growth_score=growth_score,
            competitive_score=competitive_score,
            management_score=management_score,
            recommendation=recommendation,
            holding_period="长期（3-5年以上）",
            pros=pros,
            cons=cons,
            key_points=key_points,
        )
    
    def evaluate_business(self, stock_code: str) -> float:
        """
        评估商业模式 - 段永平最看重这个
        好的商业模式：轻资产、高ROE、可复制、现金流好
        """
        # 模拟评分 - 实际应该从数据库或API获取
        # 这里返回示例评分
        score = 75.0
        
        # 白酒、互联网等好商业模式加分
        if stock_code in ["600519", "贵州茅台", "00700", "腾讯"]:
            score = 95.0
        elif stock_code in ["000333", "美的集团"]:
            score = 80.0
        elif stock_code in ["002475", "立讯精密"]:
            score = 70.0
            
        return score
    
    def evaluate_competitive(self, stock_code: str) -> float:
        """
        评估竞争优势 - 是否有护城河
        """
        score = 70.0
        
        # 有明显护城河的公司
        if stock_code in ["600519", "贵州茅台"]:
            score = 98.0  # 品牌壁垒+定价权
        elif stock_code in ["00700", "腾讯"]:
            score = 90.0  # 社交网络护城河
        elif stock_code in ["600276", "恒瑞医药"]:
            score = 85.0  # 研发壁垒
            
        return score
    
    def _get_pros(self, stock_code: str) -> List[str]:
        """优势分析"""
        pros = [
            "商业模式清晰易懂",
            "行业地位稳固",
            "现金流良好",
        ]
        
        if stock_code in ["600519", "贵州茅台"]:
            pros.extend([
                "高端白酒龙头",
                "品牌壁垒极强",
                "定价权高",
                "库存越久越值钱",
            ])
        
        return pros
    
    def _get_cons(self, stock_code: str) -> List[str]:
        """风险分析"""
        cons = [
            "短期估值可能偏高",
            "需要耐心持有",
        ]
        
        if stock_code in ["600519", "贵州茅台"]:
            cons.append("股价波动需要承受")
            
        return cons
    
    def _get_key_points(self, stock_code: str) -> List[str]:
        """关键分析点"""
        return [
            "是否真正理解这个商业模式？",
            "是否在能力圈内？",
            "管理层是否值得信任？",
            "估值是否合理（不追高）？",
            "能否持有5年以上？",
        ]


# 注册
GuruFactory.register("duan", DuanYongping)
GuruFactory.register("段永平", DuanYongping)