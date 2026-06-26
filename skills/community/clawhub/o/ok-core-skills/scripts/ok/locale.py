"""OK.com 多国家多地域 Locale 管理

国家为固定映射（数量少），城市和分类通过 ok.com API 动态获取。
"""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any

import requests

from .client.base import BaseClient
from .errors import OKAPIError, OKLocaleError
from .types import Category, City, Locale
from .urls import (
    build_base_url,
    build_categories_api_url,
    build_cities_api_url,
    build_city_search_api_url,
    parse_url,
)

logger = logging.getLogger("ok-locale")

# ─── 固定的国家映射（数量有限，约 10 个） ─────────────────────────

COUNTRIES: dict[str, dict[str, Any]] = {
    "singapore": {"subdomain": "sg", "code": "SG", "bus_id": 100005},
    "canada": {"subdomain": "ca", "code": "CA", "bus_id": 100003},
    "usa": {"subdomain": "us", "code": "US", "bus_id": 100003},
    "uae": {"subdomain": "ae", "code": "AE", "bus_id": 100002},
    "australia": {"subdomain": "au", "code": "AU", "bus_id": 100006},
    "hong_kong": {"subdomain": "hk", "code": "HK", "bus_id": 100007},
    "japan": {"subdomain": "jp", "code": "JP", "bus_id": 100006},
    "uk": {"subdomain": "gb", "code": "GB", "bus_id": 100004},
    "malaysia": {"subdomain": "my", "code": "MY", "bus_id": 100008},
    "new_zealand": {"subdomain": "nz", "code": "NZ", "bus_id": 100006},
}

# 子域名反向索引
_SUBDOMAIN_TO_COUNTRY = {v["subdomain"]: k for k, v in COUNTRIES.items()}

# 城市和分类缓存
_city_cache: dict[str, list[City]] = {}
_category_cache: dict[str, list[Category]] = {}


def list_countries() -> list[dict[str, str]]:
    """列出所有支持的国家"""
    return [
        {"name": name, "subdomain": info["subdomain"], "code": info["code"]}
        for name, info in COUNTRIES.items()
    ]


def get_country_info(country: str) -> dict[str, Any]:
    """根据国家名或子域名获取国家信息"""
    # 先按国家名查找
    if country.lower() in COUNTRIES:
        return COUNTRIES[country.lower()]

    # 按子域名查找
    country_name = _SUBDOMAIN_TO_COUNTRY.get(country.lower())
    if country_name:
        return COUNTRIES[country_name]

    # 按 ISO code 查找
    for name, info in COUNTRIES.items():
        if info["code"].lower() == country.lower():
            return info

    raise OKLocaleError(
        f"不支持的国家: {country}。支持的国家: {', '.join(COUNTRIES.keys())}"
    )


def _build_api_headers(country_info: dict, lang: str = "en") -> dict[str, str]:
    """构建 API 请求头"""
    return {
        "busId": str(country_info["bus_id"]),
        "language": lang,
        "country": country_info["code"],
        "platform": "-1",
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
    }


# ─── 城市动态获取 ─────────────────────────────────────────────

def fetch_cities(country: str, lang: str = "en", use_cache: bool = True) -> list[City]:
    """从 ok.com API 动态获取指定国家的城市列表

    Args:
        country: 国家名、子域名或 ISO code
        lang: 语言代码（默认 en）
        use_cache: 是否使用缓存

    Returns:
        城市列表
    """
    country_info = get_country_info(country)
    cache_key = f"{country_info['subdomain']}_{lang}"

    if use_cache and cache_key in _city_cache:
        return _city_cache[cache_key]

    api_url = build_cities_api_url(country_info["subdomain"])
    headers = _build_api_headers(country_info, lang)

    logger.info("获取城市列表: %s (country=%s)", api_url, country_info["code"])

    try:
        resp = requests.get(api_url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        raise OKAPIError(f"获取城市列表失败: {e}")

    if data.get("responseCode") != 200:
        raise OKAPIError(
            f"API 返回错误: {data.get('responseMsg', 'Unknown')}",
            response_code=data.get("responseCode"),
        )

    # 解析城市列表
    cities: list[City] = []
    result_data = data.get("data", {})

    # 解析 popularCities
    for c in result_data.get("popularCities", []):
        cities.append(City(
            local_id=str(c.get("localId", "")),
            name=c.get("name", ""),
            code=c.get("code", ""),
        ))

    # 解析 cityList（按首字母索引 A-Z）
    seen_codes = {c.code for c in cities}
    city_list = result_data.get("cityList", [])
    for group in city_list:
        letter_cities = group.get("cities", [])
        for c in letter_cities:
            code = c.get("code", "")
            if code and code not in seen_codes:
                cities.append(City(
                    local_id=str(c.get("localId", "")),
                    name=c.get("name", ""),
                    code=code,
                ))
                seen_codes.add(code)

    _city_cache[cache_key] = cities
    logger.info("获取到 %d 个城市", len(cities))
    return cities


def search_cities(
    country: str, keyword: str, lang: str = "en"
) -> list[City]:
    """通过搜索接口模糊匹配城市（补全 allCities 接口缺失的地域）

    使用 POST /smartProbe/api/local/search?keyword=X

    Args:
        country: 国家名、子域名或 ISO code
        keyword: 搜索关键词（如 "ha" 匹配 Hawaii, Hartford 等）
        lang: 语言代码

    Returns:
        匹配的城市列表
    """
    country_info = get_country_info(country)
    api_url = build_city_search_api_url(country_info["subdomain"], keyword)
    headers = _build_api_headers(country_info, lang)

    logger.info("搜索城市: keyword=%s (country=%s)", keyword, country_info["code"])

    try:
        resp = requests.post(api_url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        raise OKAPIError(f"搜索城市失败: {e}")

    if data.get("responseCode") != 200:
        raise OKAPIError(
            f"API 返回错误: {data.get('responseMsg', 'Unknown')}",
            response_code=data.get("responseCode"),
        )

    cities: list[City] = []
    for item in data.get("data", []):
        cities.append(City(
            local_id=str(item.get("localId", "")),
            name=item.get("name", ""),
            code=item.get("code", ""),
        ))

    logger.info("搜索到 %d 个匹配城市", len(cities))
    return cities


def fetch_all_cities(
    country: str,
    keyword_prefixes: list[str] | None = None,
    lang: str = "en",
) -> list[City]:
    """合并 allCities + search 接口，尽可能获取完整城市列表

    先调用 fetch_cities（allCities API）获取基础列表，
    再通过 search_cities 按字母前缀批量搜索，合并去重。

    Args:
        country: 国家名、子域名或 ISO code
        keyword_prefixes: 搜索关键词前缀列表，默认 a-z
        lang: 语言代码

    Returns:
        合并去重后的完整城市列表
    """
    if keyword_prefixes is None:
        keyword_prefixes = [chr(c) for c in range(ord("a"), ord("z") + 1)]

    # 1. 先获取 allCities 基础列表
    base_cities = fetch_cities(country, lang, use_cache=True)
    seen_codes: set[str] = {c.code for c in base_cities}
    merged: list[City] = list(base_cities)

    # 2. 通过 search 接口补全
    for prefix in keyword_prefixes:
        try:
            results = search_cities(country, prefix, lang)
            for city in results:
                if city.code and city.code not in seen_codes:
                    merged.append(city)
                    seen_codes.add(city.code)
        except OKAPIError as e:
            logger.warning("搜索前缀 '%s' 失败: %s", prefix, e)
            continue

    logger.info(
        "合并完成: allCities=%d + search 补全=%d = 总计 %d",
        len(base_cities), len(merged) - len(base_cities), len(merged),
    )
    return merged


def get_popular_cities(country: str, lang: str = "en") -> list[City]:
    """获取热门城市（接口中的 popularCities 部分）"""
    country_info = get_country_info(country)
    api_url = build_cities_api_url(country_info["subdomain"])
    headers = _build_api_headers(country_info, lang)

    try:
        resp = requests.get(api_url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        raise OKAPIError(f"获取热门城市失败: {e}")

    if data.get("responseCode") != 200:
        raise OKAPIError(
            f"API 返回错误: {data.get('responseMsg', 'Unknown')}",
            response_code=data.get("responseCode"),
        )

    popular = data.get("data", {}).get("popularCities", [])
    return [
        City(local_id=str(c.get("localId", "")), name=c.get("name", ""), code=c.get("code", ""))
        for c in popular
    ]


# ─── 分类动态获取 ─────────────────────────────────────────────

def fetch_categories(country: str, lang: str = "en", use_cache: bool = True) -> list[Category]:
    """从 ok.com API 动态获取分类树

    Args:
        country: 国家名、子域名或 ISO code
        lang: 语言代码
        use_cache: 是否使用缓存

    Returns:
        分类树列表
    """
    country_info = get_country_info(country)
    cache_key = f"{country_info['subdomain']}_{lang}"

    if use_cache and cache_key in _category_cache:
        return _category_cache[cache_key]

    api_url = build_categories_api_url(country_info["subdomain"])
    headers = _build_api_headers(country_info, lang)

    logger.info("获取分类列表: %s (country=%s)", api_url, country_info["code"])

    try:
        resp = requests.get(api_url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        raise OKAPIError(f"获取分类列表失败: {e}")

    if data.get("responseCode") != 200:
        raise OKAPIError(
            f"API 返回错误: {data.get('responseMsg', 'Unknown')}",
            response_code=data.get("responseCode"),
        )

    def parse_category(item: dict) -> Category:
        children = [parse_category(ch) for ch in item.get("children", [])]
        return Category(
            category_id=str(item.get("categoryId", "")),
            name=item.get("name", ""),
            code=item.get("code", ""),
            children=children,
        )

    categories = [parse_category(item) for item in data.get("data", [])]
    _category_cache[cache_key] = categories
    logger.info("获取到 %d 个顶级分类", len(categories))
    return categories


# ─── Locale 管理 ─────────────────────────────────────────────

def build_locale(country: str, city: str, lang: str = "en") -> Locale:
    """构建 Locale 对象"""
    info = get_country_info(country)
    # 查找 country name
    country_name = country.lower()
    if country_name not in COUNTRIES:
        for name, i in COUNTRIES.items():
            if i["subdomain"] == country.lower() or i["code"].lower() == country.lower():
                country_name = name
                break

    return Locale(
        country=country_name,
        country_code=info["code"],
        subdomain=info["subdomain"],
        city=city,
        lang=lang,
        bus_id=info["bus_id"],
    )


def parse_locale_from_url(url: str) -> Locale | None:
    """从 ok.com URL 解析 Locale"""
    parsed = parse_url(url)
    subdomain = parsed.get("subdomain")
    if not subdomain or subdomain not in _SUBDOMAIN_TO_COUNTRY:
        return None

    country_name = _SUBDOMAIN_TO_COUNTRY[subdomain]
    info = COUNTRIES[country_name]

    return Locale(
        country=country_name,
        country_code=info["code"],
        subdomain=subdomain,
        city=parsed.get("city", ""),
        lang=parsed.get("lang", "en"),
        bus_id=info["bus_id"],
    )


def navigate_to_locale(bridge: BaseClient, country: str, city: str, lang: str = "en") -> Locale:
    """通过 Bridge 导航到指定 locale

    Args:
        bridge: BridgeClient 实例
        country: 国家名、子域名或 ISO code
        city: 城市 code（从 fetch_cities 获取）
        lang: 语言代码

    Returns:
        当前 Locale
    """
    locale = build_locale(country, city, lang)
    url = build_base_url(locale.subdomain, locale.lang, locale.city)
    bridge.navigate(url)
    bridge.wait_dom_stable()
    logger.info("已导航到: %s", url)
    return locale


def get_current_locale(bridge: BaseClient) -> Locale | None:
    """从当前页面 URL 中解析 Locale 信息"""
    url = bridge.get_url()
    return parse_locale_from_url(url)
