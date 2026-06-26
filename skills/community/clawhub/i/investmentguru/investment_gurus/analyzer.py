"""
投资大师综合分析器

整合所有大师的分析方法，提供：
1. 多大师对比分析
2. 综合建议生成
3. 选股建议
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from investment_gurus.base import (
    BaseGuru, StockAnalysis, GuruFactory, 
    DuanYongping, ZhangLei, LiLu, QiuGuoluo,
    WangGuobin, LinYuan, DanBing
)
from investment_gurus.smart_analyzer import smart_analyze, compare_all_methods


@dataclass
class ComparisonResult:
    """多大师对比结果"""
    stock_code: str
    stock_name: str
    analyses: Dict[str, StockAnalysis]
    consensus: str
    best_guru: str
    average_score: float


class InvestmentGuru:
    """
    投资大师综合分析器
    
    Usage:
        guru = InvestmentGuru()
        
        # 单大师分析
        result = guru.analyze("贵州茅台", method="duan")
        
        # 多大师对比
        comparison = guru.compare("宁德时代")
        
        # 综合建议
        advice = guru.get_advice("消费")
    """
    
    # 支持的大师
    GURUS = {
        "duan": DuanYongping,
        "段永平": DuanYongping,
        "zhanglei": ZhangLei,
        "张磊": ZhangLei,
        "lilu": LiLu,
        "李录": LiLu,
        "qiuguoluo": QiuGuoluo,
        "邱国鹭": QiuGuoluo,
        "wangguobin": WangGuobin,
        "王国斌": WangGuobin,
        "linyuan": LinYuan,
        "林园": LinYuan,
        "danbing": DanBing,
        "但斌": DanBing,
    }
    
    def __init__(self):
        self._gurus: Dict[str, BaseGuru] = {}
        self._init_gurus()
    
    def _init_gurus(self):
        """初始化所有大师"""
        for name, guru_class in self.GURUS.items():
            if name not in self._gurus:
                self._gurus[name] = guru_class()
    
    def get_available_gurus(self) -> List[str]:
        """获取可用的大师列表"""
        return list(set(self.GURUS.keys()))
    
    def analyze(
        self, 
        stock_code: str, 
        method: str = "duan",
        stock_name: str = None,
        **kwargs
    ) -> StockAnalysis:
        """
        使用指定大师的方法分析股票
        
        Args:
            stock_code: 股票代码
            method: 大师方法 (duan/zhanglei/linyuan等)
            stock_name: 股票名称
            
        Returns:
            StockAnalysis: 分析结果
        """
        guru = self.get_guru(method)
        if guru is None:
            raise ValueError(f"未知的大师方法: {method}")
        
        return guru.analyze_stock(stock_code, stock_name=stock_name or stock_code, **kwargs)
    
    def get_guru(self, method: str) -> Optional[BaseGuru]:
        """获取指定大师"""
        return self._gurus.get(method)
    
    def compare(self, stock_code: str, stock_name: str = None) -> ComparisonResult:
        """
        多大师对比分析
        
        对比所有大师对同一只股票的分析，给出共识建议
        """
        analyses = {}
        
        for name, guru in self._gurus.items():
            try:
                analysis = guru.analyze_stock(
                    stock_code, 
                    stock_name=stock_name or stock_code
                )
                analyses[name] = analysis
            except Exception as e:
                print(f"警告: {name} 分析失败: {e}")
        
        # 计算平均分
        scores = [a.overall_score for a in analyses.values()]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # 找最佳大师
        best_guru = max(analyses.items(), key=lambda x: x[1].overall_score)[0]
        
        # 生成共识
        consensus = self._generate_consensus(analyses, avg_score)
        
        return ComparisonResult(
            stock_code=stock_code,
            stock_name=stock_name or stock_code,
            analyses={name: a.to_dict() for name, a in analyses.items()},
            consensus=consensus,
            best_guru=best_guru,
            average_score=round(avg_score, 1),
        )
    
    def _generate_consensus(self, analyses: Dict[str, StockAnalysis], avg_score: float) -> str:
        """生成共识建议"""
        buy_count = sum(1 for a in analyses.values() if "买入" in a.recommendation)
        hold_count = sum(1 for a in analyses.values() if "持有" in a.recommendation)
        sell_count = sum(1 for a in analyses.values() if "卖出" in a.recommendation)
        
        total = buy_count + hold_count + sell_count
        
        if buy_count > total * 0.6:
            return "多数大师建议买入"
        elif sell_count > total * 0.6:
            return "多数大师建议卖出"
        else:
            return "大师建议分歧，建议持有观察"
    
    def comprehensive_analysis(self, stock_code: str, stock_name: str = None) -> Dict:
        """
        综合分析报告
        
        整合所有大师的分析，生成完整报告
        """
        comparison = self.compare(stock_code, stock_name)
        
        return {
            "stock": {
                "code": comparison.stock_code,
                "name": comparison.stock_name,
            },
            "consensus": comparison.consensus,
            "best_guru": comparison.best_guru,
            "average_score": comparison.average_score,
            "detailed_analysis": comparison.analyses,
            "investment_principles": self._get_investment_principles(comparison.best_guru),
        }
    
    def _get_investment_principles(self, guru_name: str) -> Dict:
        """获取投资原则"""
        guru = self._gurus.get(guru_name)
        if guru:
            return guru.get_info()
        return {}
    
    def get_advice(self, sector: str) -> Dict:
        """
        行业投资建议
        
        根据大师方法给出行业投资建议
        """
        sector_map = {
            "消费": {
                "recommended_gurus": ["duan", "linyuan", "danbing"],
                "focus": "嘴巴经济、垄断品牌",
                "stocks": ["贵州茅台", "五粮液", "片仔癀"],
            },
            "科技": {
                "recommended_gurus": ["zhanglei", "danbing"],
                "focus": "长期增长、创新能力",
                "stocks": ["腾讯", "宁德时代", "比亚迪"],
            },
            "金融": {
                "recommended_gurus": ["qiuguoluo", "wangguobin"],
                "focus": "估值、ROE",
                "stocks": ["招商银行", "中国平安"],
            },
            "医药": {
                "recommended_gurus": ["linyuan", "zhanglei"],
                "focus": "创新、垄断",
                "stocks": ["恒瑞医药", "片仔癀"],
            },
            "新能源": {
                "recommended_gurus": ["zhanglei", "wangguobin"],
                "focus": "行业空间、竞争力",
                "stocks": ["宁德时代", "比亚迪", "隆基绿能"],
            },
        }
        
        return sector_map.get(sector, {"message": "未找到该行业建议"})


# 便捷函数
def quick_analyze(stock_code: str, method: str = "duan") -> Dict:
    """快速分析"""
    guru = InvestmentGuru()
    result = guru.analyze(stock_code, method=method)
    return result.to_dict()


def compare_all(stock_code: str) -> ComparisonResult:
    """对比所有大师"""
    guru = InvestmentGuru()
    return guru.compare(stock_code)