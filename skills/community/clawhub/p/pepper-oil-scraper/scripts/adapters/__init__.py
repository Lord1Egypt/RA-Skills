"""
适配器注册表 — 通过 adapter_id 获取对应的爬虫类。
"""

from .price_adapters import CnhnbScraper, YmtScraper, CnfinIndexScraper, HuajiaoBigdataScraper, HuajiaoCnScraper
from .report_adapters import ChinabaogaoScraper, AskciScraper, ChyxxScraper, QianzhanScraper, ChinairnScraper, GonynScraper
from .company_adapters import CninfoScraper, EastmoneyScraper, SinaFinanceScraper, OilcnScraper
from .gov_adapters import ForestryScraper, MoaScraper, CustomsScraper, SamrStdScraper
from .media_adapters import Kr36Scraper, JiemianScraper, CbndataScraper, CnrScraper
from .global_adapters import BriScraper, VmrScraper, WiseguyScraper

# adapter_id → class
ADAPTER_REGISTRY: dict[str, type] = {
    # A: 价格
    "cnhnb":           CnhnbScraper,
    "ymt":             YmtScraper,
    "cnfin_index":     CnfinIndexScraper,
    "huajiao_bigdata": HuajiaoBigdataScraper,
    "huajiao_cn":      HuajiaoCnScraper,
    # B: 报告
    "chinabaogao":     ChinabaogaoScraper,
    "askci":           AskciScraper,
    "chyxx":           ChyxxScraper,
    "qianzhan":        QianzhanScraper,
    "chinairn":        ChinairnScraper,
    "gonyn":           GonynScraper,
    # C: 企业
    "cninfo":          CninfoScraper,
    "eastmoney":       EastmoneyScraper,
    "sina_finance":    SinaFinanceScraper,
    "oilcn":           OilcnScraper,
    # D: 政府
    "forestry":        ForestryScraper,
    "moa":             MoaScraper,
    "customs":         CustomsScraper,
    "samr_std":        SamrStdScraper,
    # E: 媒体
    "kr36":            Kr36Scraper,
    "jiemian":         JiemianScraper,
    "cbndata":         CbndataScraper,
    "cnr":             CnrScraper,
    # F: 全球
    "bri":             BriScraper,
    "vmr":             VmrScraper,
    "wiseguy":         WiseguyScraper,
}

CATEGORY_MAP: dict[str, list[str]] = {
    "price":   ["cnhnb", "ymt", "cnfin_index", "huajiao_bigdata", "huajiao_cn"],
    "market":  ["chinabaogao", "askci", "chyxx", "qianzhan", "chinairn", "gonyn"],
    "company": ["cninfo", "eastmoney", "sina_finance", "oilcn"],
    "gov":     ["forestry", "moa", "customs", "samr_std"],
    "media":   ["kr36", "jiemian", "cbndata", "cnr"],
    "global":  ["bri", "vmr", "wiseguy"],
}

def get_adapter(adapter_id: str, config: dict = None):
    cls = ADAPTER_REGISTRY.get(adapter_id)
    if cls is None:
        raise ValueError(f"Unknown adapter: {adapter_id}. Available: {list(ADAPTER_REGISTRY)}")
    return cls(config=config)

def get_adapters_by_category(category: str, config: dict = None) -> list:
    ids = CATEGORY_MAP.get(category, [])
    return [get_adapter(aid, config) for aid in ids]
