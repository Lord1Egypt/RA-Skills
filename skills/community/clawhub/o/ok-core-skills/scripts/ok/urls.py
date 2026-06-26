"""OK.com URL 常量和构建器"""

from __future__ import annotations

import re


def is_city_shell_url(url: str) -> bool:
    """是否为带 ``/lang/city-{slug}/`` 的标准城市壳（列表、详情等子路径也算）。"""
    if "ok.com" not in url:
        return False
    return bool(re.search(r"ok\.com/[^/]+/city-[^/]+/", url))


def build_base_url(subdomain: str, lang: str = "en", city: str | None = None) -> str:
    """构建基础 URL

    Examples:
        >>> build_base_url("sg", "en", "singapore")
        'https://sg.ok.com/en/city-singapore/'
        >>> build_base_url("ca", "en")
        'https://ca.ok.com/en/'
    """
    base = f"https://{subdomain}.ok.com/{lang}/"
    if city:
        base += f"city-{city}/"
    return base


def build_category_url(subdomain: str, lang: str, city: str, category_code: str) -> str:
    """构建分类页 URL

    Examples:
        >>> build_category_url("sg", "en", "singapore", "marketplace")
        'https://sg.ok.com/en/city-singapore/cate-marketplace/'
    """
    return f"https://{subdomain}.ok.com/{lang}/city-{city}/cate-{category_code}/"


def build_search_url(subdomain: str, lang: str, city: str) -> str:
    """构建搜索页 URL（关键词通过 UI 输入）"""
    return f"https://{subdomain}.ok.com/{lang}/city-{city}/listpage/"


def build_listing_url(subdomain: str, lang: str, city: str, category: str, slug: str) -> str:
    """构建帖子详情 URL"""
    return f"https://{subdomain}.ok.com/{lang}/city-{city}/cate-{category}/{slug}/"


def build_api_base(subdomain: str) -> str:
    """构建 API 基础 URL

    Examples:
        >>> build_api_base("sg")
        'https://sgpub.ok.com/smartProbe/api'
    """
    return f"https://{subdomain}pub.ok.com/smartProbe/api"


def build_cities_api_url(subdomain: str) -> str:
    """构建城市列表 API URL"""
    return f"{build_api_base(subdomain)}/local/allCities"


def build_categories_api_url(subdomain: str, exclude_self: int = 1, depth: int = 3) -> str:
    """构建分类列表 API URL"""
    return f"{build_api_base(subdomain)}/getLevelCates?excludeSelf={exclude_self}&depth={depth}"


def build_city_search_api_url(subdomain: str, keyword: str) -> str:
    """构建城市搜索 API URL（POST 请求）

    Examples:
        >>> build_city_search_api_url("us", "ha")
        'https://uspub.ok.com/smartProbe/api/local/search?keyword=ha'
    """
    from urllib.parse import quote
    return f"{build_api_base(subdomain)}/local/search?keyword={quote(keyword)}"


def append_keyword_to_url(url: str, keyword: str) -> str:
    """在现有 URL 上安全追加 keyword 查询参数

    Examples:
        >>> append_keyword_to_url("https://us.ok.com/en/city-hawaii/cate-property/", "house")
        'https://us.ok.com/en/city-hawaii/cate-property/?keyword=house'
        >>> append_keyword_to_url("https://sg.ok.com/en/city-singapore/", "laptop bag")
        'https://sg.ok.com/en/city-singapore/?keyword=laptop+bag'
    """
    from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    qs["keyword"] = [keyword]
    new_query = urlencode(qs, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


def parse_url(url: str) -> dict:
    """从 ok.com URL 解析出 locale 信息

    Examples:
        >>> parse_url("https://sg.ok.com/en/city-singapore/cate-marketplace/")
        {'subdomain': 'sg', 'lang': 'en', 'city': 'singapore', 'category': 'marketplace'}
    """
    import re

    result = {}

    # 提取子域名
    m = re.search(r"https?://([a-z]+)\.ok\.com", url)
    if m:
        result["subdomain"] = m.group(1)

    # 提取语言
    m = re.search(r"ok\.com/([a-z]{2})/", url)
    if m:
        result["lang"] = m.group(1)

    # 提取城市
    m = re.search(r"/city-([^/]+)/", url)
    if m:
        result["city"] = m.group(1)

    # 提取分类
    m = re.search(r"/cate-([^/]+)/", url)
    if m:
        result["category"] = m.group(1)

    # 提取帖子 slug（分类后面的路径）
    m = re.search(r"/cate-[^/]+/([^/]+)/", url)
    if m:
        result["listing_slug"] = m.group(1)

    return result
