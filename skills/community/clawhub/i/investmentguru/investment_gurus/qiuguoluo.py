"""
邱国鹭投资方法 - 高毅资产董事长

核心理念：
1. 逆向投资 - 人多的地方不要去
2. 三好原则 - 好行业、好公司、好价格
3. 常识投资 - 用简单常识做判断
4. 价值陷阱 - 避开低估值陷阱

代表案例：
- 《投资中最简单的事》《投资中不简单的事》
"""

from typing import Dict, List
from investment_gurus.base import BaseGuru, StockAnalysis, GuruFactory


class QiuGuoluo(BaseGuru):
    """邱国鹭投资方法"""
    
    name = "邱国鹭"
    alias = "高毅资产董事长"
    background = """
    高毅资产董事长，曾任南方基金投资总监。
    15年从业经验，以逆向投资著称。
    """
    
    core_philosophy = """
    1. 逆向投资 - 人多的地方不要去
    2. 三好原则 - 好行业、好公司、好价格
    3. 常识投资 - 用简单常识做判断
    4. 注重估值 - 宁买贵的好公司，不买便宜的差公司
    5. 行业轮动 - 把握行业周期
    """
    
    key_principles = [
        "逆向投资",
        "三好原则",
        "好行业",
        "好公司",
        "好价格",
        "常识投资",
        "价值陷阱",
    ]
    
    representative_cases = {
        "银行": "低估时买入，高估时卖出",
        "地产": "行业下行期逆向布局",
        "消费": "长期持有好公司",
    }
    
    suitable_sectors = [
        "金融",
        "地产",
        "消费",
        "周期股",
    ]
    
    def analyze_stock(self, stock_code: str, **kwargs) -> StockAnalysis:
        stock_name = kwargs.get("stock_name", stock_code)
        
        business_score = self.evaluate_business(stock_code)
        valuation_score = self.evaluate_valuation(stock_code)
        growth_score = self.evaluate_growth(stock_code)
        competitive_score = self.evaluate_competitive(stock_code)
        management_score = self.evaluate_management(stock_code)
        
        # 三好原则同等重要
        overall = (
            business_score * 0.25 +
            valuation_score * 0.25 +
            competitive_score * 0.20 +
            growth_score * 0.15 +
            management_score * 0.15
        )
        
        recommendation = self.get_recommendation({"overall": overall})
        
        return StockAnalysis(
            stock_code=stock_code,
            stock_name=stock_name,
            guru_name=self.name,
            guru_method="三好原则+逆向投资",
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
    
    def evaluate_valuation(self, stock_code: str) -> float:
        """好价格"""
        score = 60.0
        
        # 低估值
        if stock_code in ["601398", "工商银行"]:
            score = 90.0
        elif stock_code in ["600036", "招商银行"]:
            score = 80.0
            
        return score
    
    def evaluate_business(self, stock_code: str) -> float:
        """好行业"""
        score = 60.0
        
        # 好行业
        if stock_code in ["600519", "贵州茅台"]:
            score = 95.0
        elif stock_code in ["601318", "中国平安"]:
            score = 85.0
            
        return score
    
    def _get_pros(self, stock_code: str) -> List[str]:
        return [
            "好行业",
            "好公司",
            "好价格",
        ]
    
    def _get_cons(self, stock_code: str) -> List[str]:
        return [
            "需要等待好的买入时机",
            "逆向投资需要勇气",
        ]
    
    def _get_key_points(self, stock_code: str) -> List[str]:
        return [
            "是否好行业（门槛高、空间大）？",
            "是否好公司（竞争壁垒强）？",
            "是否好价格（安全边际够）？",
            "是否是价值陷阱？",
        ]


GuruFactory.register("qiuguoluo", QiuGuoluo)
GuruFactory.register("邱国鹭", QiuGuoluo)