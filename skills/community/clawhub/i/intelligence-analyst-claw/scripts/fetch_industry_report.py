#!/usr/bin/env python3
"""
行业报告批量下载脚本 — 生成搜索词列表，供 Agent 批量抓取。
用法：Agent 调用此脚本生成搜索计划，再逐一执行 web_search/web_fetch。
"""

import json
from datetime import datetime

# 主流行业报告来源
REPORT_SOURCES = {
    "艾瑞咨询": "site:iresearch.com.cn",
    "36氪研究院": "site:36kr.com 研究院",
    "Gartner": "site:gartner.com",
    "IDC": "site:idc.com",
    "麦肯锡": "site:mckinsey.com",
    "BCG": "site:bcg.com",
    "毕马威": "site:kpmg.com",
}

def generate_search_plan(keyword: str, sources: list[str] = None, year: int = None) -> dict:
    """
    生成行业报告搜索计划
    
    Args:
        keyword: 行业关键词，如 "新能源汽车"
        sources: 指定来源列表，默认全部
        year: 报告年份，默认当前年
    
    Returns:
        搜索计划 dict，包含搜索词列表
    """
    if year is None:
        year = datetime.now().year
    
    if sources is None:
        sources = list(REPORT_SOURCES.keys())
    
    queries = []
    
    # 通用搜索
    queries.append(f"{keyword} 市场规模 {year} 研究报告")
    queries.append(f"{keyword} industry market size report {year}")
    queries.append(f"{keyword} 行业分析 趋势 {year}")
    
    # 按来源搜索
    for source in sources:
        if source in REPORT_SOURCES:
            site_filter = REPORT_SOURCES[source]
            queries.append(f"{keyword} {site_filter} {year}")
    
    return {
        "keyword": keyword,
        "year": year,
        "sources": sources,
        "queries": queries,
        "instructions": "按顺序执行 web_search，对有价值的结果执行 web_fetch 获取全文"
    }


if __name__ == "__main__":
    plan = generate_search_plan("新能源汽车", sources=["艾瑞咨询", "36氪研究院"])
    print(json.dumps(plan, ensure_ascii=False, indent=2))
