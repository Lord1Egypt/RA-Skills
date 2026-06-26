#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
url_builder.py - 统一的 URL 构建工具

提供各类搜索引擎的 URL 构建功能，支持：
- 多引擎 URL 生成
- 时间过滤
- 站点搜索
- 地区过滤
- DuckDuckGo Lite 格式
"""
import urllib.parse
from typing import Optional, Dict, Any
from constants import (
    get_engine, is_valid_engine, get_time_filter,
    ENGINES, REGIONS
)


def url_encode(query: str) -> str:
    """
    URL 编码查询字符串。
    使用 urllib.parse.quote 确保正确编码。
    """
    return urllib.parse.quote(query, safe="")


def build_search_url(
    engine: str,
    query: str,
    domain: Optional[str] = None,
    time_filter: Optional[str] = None,
    region: Optional[str] = None,
    extra_params: Optional[Dict[str, str]] = None
) -> str:
    """
    构建搜索引擎 URL。
    
    Args:
        engine: 引擎名称 (google, brave, ddg, etc.)
        query: 搜索查询
        domain: 站点过滤 (如 github.com)
        time_filter: 时间过滤 (hour/day/week/month/year)
        region: 地区代码
        extra_params: 额外 URL 参数
    
    Returns:
        完整的搜索 URL
    
    Raises:
        ValueError: 无效的引擎名称
    """
    engine_config = get_engine(engine)
    if not engine_config:
        raise ValueError(f"Unknown engine: {engine}")
    
    # 构建查询字符串
    query_str = query
    if domain:
        query_str = f"site:{domain} {query}"
    
    # 注意：不要在这里预编码，让 urlencode 处理所有编码
    # encoded_query = url_encode(query_str)  # 删除这行
    
    # 获取基础 URL 和查询参数名
    base_url = engine_config["base_url"]
    query_param = engine_config["query_param"]
    
    # 构建 URL - 直接使用原始 query_str，urlencode 会正确编码
    params = {query_param: query_str}
    
    # 添加时间过滤
    if time_filter and engine_config.get("supports_time"):
        tf = get_time_filter(engine, time_filter)
        if tf:
            key, value = tf.split("=")
            params[key] = value
    
    # 添加地区过滤
    if region and engine == "ddg":
        params["kl"] = region
    
    # 处理 startpage 特殊参数
    if engine == "startpage" and domain:
        params["domains"] = domain
    
    # 处理 wechat 特殊参数
    if engine == "wechat":
        params["type"] = "2"  # 文章搜索
    
    # 添加额外参数
    if extra_params:
        params.update(extra_params)
    
    # 组合 URL
    query_string = urllib.parse.urlencode(params)
    
    # 特殊处理某些引擎
    if "?" in base_url:
        # URL 已包含查询字符串
        return f"{base_url}&{query_string}"
    else:
        return f"{base_url}?{query_string}"


def build_duckduckgo_lite_url(
    query: str,
    region: str = "us-en"
) -> str:
    """
    构建 DuckDuckGo Lite URL。
    用于 web_fetch 方式的无 API 搜索。
    """
    encoded_query = url_encode(query)
    return f"https://lite.duckduckgo.com/lite/?q={encoded_query}&kl={region}"


def build_google_url(
    query: str,
    domain: Optional[str] = None,
    time_filter: Optional[str] = None,
    lang: Optional[str] = None,
    region: Optional[str] = None,
    search_type: Optional[str] = None  # isch/nws/vid/map/shop/bks
) -> str:
    """
    构建 Google 搜索 URL，支持高级参数。
    """
    query_str = query
    if domain:
        query_str = f"site:{domain} {query}"
    
    encoded_query = url_encode(query_str)
    
    params = [("q", encoded_query)]
    
    if time_filter:
        tf = get_time_filter("google", time_filter)
        if tf:
            params.append(tuple(tf.split("=")))
    
    if lang:
        params.append(("hl", lang))
    
    if region:
        params.append(("gl", region))
    
    if search_type:
        params.append(("tbm", search_type))
    
    query_string = urllib.parse.urlencode(params)
    return f"https://www.google.com/search?{query_string}"


def build_brave_url(
    query: str,
    domain: Optional[str] = None,
    time_filter: Optional[str] = None
) -> str:
    """
    构建 Brave Search URL。
    """
    return build_search_url("brave", query, domain, time_filter)


def build_ddg_url(
    query: str,
    domain: Optional[str] = None,
    region: Optional[str] = None,
    safe_search: int = 1  # 1=严格, -1=关闭
) -> str:
    """
    构建 DuckDuckGo HTML URL。
    """
    query_str = query
    if domain:
        query_str = f"site:{domain} {query}"
    
    encoded_query = url_encode(query_str)
    params = [("q", encoded_query)]
    
    if region:
        params.append(("kl", region))
    
    params.append(("kp", str(safe_search)))
    
    query_string = urllib.parse.urlencode(params)
    return f"https://duckduckgo.com/html/?{query_string}"


def build_baidu_url(
    query: str,
    domain: Optional[str] = None,
    page: int = 1
) -> str:
    """
    构建百度搜索 URL。
    """
    query_str = query
    if domain:
        query_str = f"site:{domain} {query}"
    
    encoded_query = url_encode(query_str)
    pn = (page - 1) * 10  # 百度每页 10 条
    
    params = [("wd", encoded_query), ("pn", str(pn))]
    
    query_string = urllib.parse.urlencode(params)
    return f"https://www.baidu.com/s?{query_string}"


def build_sogou_url(
    query: str,
    domain: Optional[str] = None,
    page: int = 1
) -> str:
    """
    构建搜狗搜索 URL。
    """
    query_str = query
    if domain:
        query_str = f"site:{domain} {query}"
    
    encoded_query = url_encode(query_str)
    page_param = (page - 1) * 10
    
    params = [("query", encoded_query), ("page", str(page))]
    
    query_string = urllib.parse.urlencode(params)
    return f"https://sogou.com/web?{query_string}"


def build_wechat_url(query: str) -> str:
    """
    构建搜狗微信搜索 URL。
    """
    encoded_query = url_encode(query)
    return f"https://wx.sogou.com/weixin?type=2&query={encoded_query}"


def build_arxiv_url(
    query: str,
    max_results: int = 10,
    sort_by: str = "submittedDate",
    sort_order: str = "descending"
) -> str:
    """
    构建 arXiv API 查询 URL。
    """
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": sort_by,
        "sortOrder": sort_order,
    }
    
    query_string = urllib.parse.urlencode(params)
    return f"https://export.arxiv.org/api/query?{query_string}"


def build_wolframalpha_url(query: str) -> str:
    """
    构建 WolframAlpha 查询 URL。
    """
    encoded_query = url_encode(query)
    return f"https://www.wolframalpha.com/input?i={encoded_query}"


def build_google_scholar_url(query: str) -> str:
    """
    构建 Google Scholar 搜索 URL。
    """
    encoded_query = url_encode(query)
    return f"https://scholar.google.com/scholar?q={encoded_query}"


def build_bing_url(
    query: str,
    domain: Optional[str] = None,
    time_filter: Optional[str] = None,
    market: str = "en-US"
) -> str:
    """
    构建 Bing 搜索 URL。
    """
    query_str = query
    if domain:
        query_str = f"site:{domain} {query}"
    
    encoded_query = url_encode(query_str)
    params = [("q", encoded_query), ("mkt", market)]
    
    if time_filter:
        tf = get_time_filter("bing", time_filter)
        if tf:
            params.append(tuple(tf.split("=")))
    
    query_string = urllib.parse.urlencode(params)
    return f"https://www.bing.com/search?{query_string}"


def get_web_fetch_command(url: str, max_chars: int = 8000, extract_mode: str = "text") -> str:
    """
    生成 web_fetch 调用命令。
    """
    return f'web_fetch(url="{url}", extractMode="{extract_mode}", maxChars={max_chars})'


def format_results_for_display(results: list) -> str:
    """
    格式化搜索结果为可读文本。
    """
    if not results:
        return "No results found."
    
    output = []
    for i, r in enumerate(results, 1):
        title = r.get("title", "Untitled")
        url = r.get("url", "")
        snippet = r.get("snippet", "")
        source = r.get("source", "")
        
        output.append(f"{i}. {title}")
        if url:
            output.append(f"   🔗 {url}")
        if snippet:
            output.append(f"   💬 {snippet[:200]}...")
        if source:
            output.append(f"   📍 来源: {source}")
        output.append("")
    
    return "\n".join(output)


# ── 便捷构建函数 ────────────────────────────────────────────────────────

def quick_search_url(query: str, engine: str = "google") -> str:
    """快速构建简单搜索 URL（无额外参数）"""
    return build_search_url(engine, query)


def multi_engine_urls(
    query: str,
    engines: list,
    domain: Optional[str] = None,
    time_filter: Optional[str] = None,
    region: Optional[str] = None
) -> Dict[str, str]:
    """
    一次性构建多引擎 URL。
    
    Returns:
        Dict[engine_name, url]
    """
    urls = {}
    for engine in engines:
        try:
            urls[engine] = build_search_url(
                engine, query, domain, time_filter, region
            )
        except ValueError:
            continue
    return urls


if __name__ == "__main__":
    print("=== URL Builder 测试 ===\n")
    
    # 测试基础构建
    print("1. Google 搜索:")
    print(f"   {build_google_url('python tutorial')}")
    
    print("\n2. Brave + 时间过滤:")
    print(f"   {build_brave_url('AI news', time_filter='week')}")
    
    print("\n3. DDG + 站点过滤:")
    print(f"   {build_ddg_url('react hooks', domain='github.com')}")
    
    print("\n4. 多引擎 URL:")
    urls = multi_engine_urls(
        "machine learning",
        ["google", "brave", "ddg"],
        time_filter="month"
    )
    for eng, url in urls.items():
        print(f"   {eng}: {url}")
    
    print("\n5. web_fetch 命令:")
    url = build_google_url("test query")
    print(f"   {get_web_fetch_command(url)}")
    
    print("\n6. 百度搜索:")
    print(f"   {build_baidu_url('深度学习')}")
    
    print("\n7. 微信搜索:")
    print(f"   {build_wechat_url('机器学习')}")
