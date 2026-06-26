# 中国投资大师
from investment_gurus.base import BaseGuru
from investment_gurus.analyzer import InvestmentGuru as GuruAnalyzer
from investment_gurus.duan import DuanYongping
from investment_gurus.zhanglei import ZhangLei
from investment_gurus.liu_lu import LiLu
from investment_gurus.qiuguoluo import QiuGuoluo
from investment_gurus.wangguobin import WangGuobin
from investment_gurus.linyuan import LinYuan
from investment_gurus.danbing import DanBing

# 数据和分析
from investment_gurus.data_fetcher import StockDataFetcher, StockAnalyzer, quick_quote, quick_analysis
from investment_gurus.smart_analyzer import SmartGuruAnalyzer, smart_analyze, compare_all_methods
from investment_gurus.agent_handler import InvestmentGuruSkill, handle_user_message

# 国际投资大师 (新增)
from investment_gurus.international_gurus import (
    INTERNATIONAL_GURUS,
    ANALYSIS_DIMENSIONS,
    get_guru_info,
    get_all_gurus,
    analyze_guru_signal,
    generate_multi_guru_report,
    analyze_stock_international,
)

__version__ = "2.0.0"
__author__ = "Investment Gurus Team"

__all__ = [
    # 中国大师
    "BaseGuru",
    "GuruAnalyzer",
    "DuanYongping", 
    "ZhangLei",
    "LiLu",
    "QiuGuoluo",
    "WangGuobin",
    "LinYuan",
    "DanBing",
    
    # 数据和分析
    "StockDataFetcher",
    "StockAnalyzer",
    "quick_quote",
    "quick_analysis",
    "SmartGuruAnalyzer",
    "smart_analyze",
    "compare_all_methods",
    "InvestmentGuruSkill",
    "handle_user_message",
    
    # 国际大师 (新增)
    "INTERNATIONAL_GURUS",
    "ANALYSIS_DIMENSIONS",
    "get_guru_info",
    "get_all_gurus",
    "analyze_guru_signal",
    "generate_multi_guru_report",
    "analyze_stock_international",
]

# 默认导出
InvestmentGuru = GuruAnalyzer