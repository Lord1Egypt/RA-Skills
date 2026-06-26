#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
constants.py - 统一搜索引擎定义

所有脚本应从此模块导入引擎配置，确保一致性。
"""
from typing import Dict, List, Any

# 统一搜索引擎定义
ENGINES: Dict[str, Dict[str, Any]] = {
    # ── 主要搜索引擎 ────────────────────────────────────────────
    "google": {
        "name": "Google",
        "name_zh": "Google 搜索",
        "base_url": "https://www.google.com/search",
        "query_param": "q",
        "supports_time": True,
        "time_param": "tbs",
        "time_map": {
            "hour": "qdr:h",
            "day": "qdr:d",
            "week": "qdr:w",
            "month": "qdr:m",
            "year": "qdr:y",
        },
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": False,  # 可能有 rate limit
        "privacy_friendly": False,
    },
    "brave": {
        "name": "Brave Search",
        "name_zh": "Brave 搜索",
        "base_url": "https://search.brave.com/search",
        "query_param": "q",
        "supports_time": True,
        "time_param": "tf",
        "time_map": {
            "hour": "ph",
            "day": "pd",
            "week": "pw",
            "month": "pm",
            "year": "py",
        },
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": True,
    },
    "ddg": {
        "name": "DuckDuckGo",
        "name_zh": "DuckDuckGo",
        "base_url": "https://duckduckgo.com/html/",
        "query_param": "q",
        "supports_time": False,
        "time_param": None,
        "time_map": {},
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": True,
    },
    "duckduckgo": {  # 别名
        "name": "DuckDuckGo",
        "name_zh": "DuckDuckGo",
        "base_url": "https://duckduckgo.com/html/",
        "query_param": "q",
        "supports_time": False,
        "time_param": None,
        "time_map": {},
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": True,
        "_alias_of": "ddg",
    },
    "bing": {
        "name": "Bing",
        "name_zh": "微软 Bing",
        "base_url": "https://www.bing.com/search",
        "query_param": "q",
        "supports_time": True,
        "time_param": "tf",
        "time_map": {
            "hour": "qdr:h",
            "day": "qdr:d",
            "week": "qdr:w",
            "month": "qdr:m",
            "year": "qdr:y",
        },
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": False,
    },
    "yahoo": {
        "name": "Yahoo",
        "name_zh": "Yahoo 搜索",
        "base_url": "https://search.yahoo.com/search",
        "query_param": "p",
        "supports_time": False,
        "time_param": None,
        "time_map": {},
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": False,
    },
    "startpage": {
        "name": "Startpage",
        "name_zh": "Startpage",
        "base_url": "https://www.startpage.com/sp/search",
        "query_param": "query",
        "supports_time": True,
        "time_param": "time",  # day/week/month/year
        "time_map": {
            "day": "day",
            "week": "week",
            "month": "month",
            "year": "year",
        },
        "supports_site": True,
        "site_operator": "site:",  # 或用 domains= 参数
        "domain_param": "domains",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": True,
    },
    "ecosia": {
        "name": "Ecosia",
        "name_zh": "Ecosia 环保搜索",
        "base_url": "https://www.ecosia.org/search",
        "query_param": "q",
        "supports_time": False,
        "time_param": None,
        "time_map": {},
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": True,
    },
    "qwant": {
        "name": "Qwant",
        "name_zh": "Qwant (EU)",
        "base_url": "https://www.qwant.com/",
        "query_param": "q",
        "supports_time": False,
        "time_param": None,
        "time_map": {},
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": True,
    },
    # ── 额外引擎（ddgs 专用）──────────────────────────────────
    "yandex": {
        "name": "Yandex",
        "name_zh": "Yandex",
        "base_url": "https://yandex.com/search/",
        "query_param": "text",
        "supports_time": False,
        "time_param": None,
        "time_map": {},
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": False,
    },
    "wikipedia": {
        "name": "Wikipedia",
        "name_zh": "维基百科",
        "base_url": "https://en.wikipedia.org/w/index.php",
        "query_param": "search",
        "supports_time": False,
        "time_param": None,
        "time_map": {},
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": True,
    },
    "mojeek": {
        "name": "Mojeek",
        "name_zh": "Mojeek",
        "base_url": "https://www.mojeek.com/search",
        "query_param": "q",
        "supports_time": False,
        "time_param": None,
        "time_map": {},
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": True,
    },
    "google_hk": {
        "name": "Google HK",
        "name_zh": "谷歌香港",
        "base_url": "https://www.google.com.hk/search",
        "query_param": "q",
        "supports_time": True,
        "time_param": "tbs",
        "time_map": {
            "hour": "qdr:h",
            "day": "qdr:d",
            "week": "qdr:w",
            "month": "qdr:m",
            "year": "qdr:y",
        },
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": False,
    },
    "wolframalpha": {
        "name": "WolframAlpha",
        "name_zh": "WolframAlpha",
        "base_url": "https://www.wolframalpha.com/input?i",
        "query_param": "i",
        "supports_time": False,
        "time_param": None,
        "time_map": {},
        "supports_site": False,
        "site_operator": None,
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": True,
        "is_computational": True,
    },
    # ── 国内搜索引擎 ──────────────────────────────────────────
    "baidu": {
        "name": "Baidu",
        "name_zh": "百度",
        "base_url": "https://www.baidu.com/s",
        "query_param": "wd",
        "supports_time": False,
        "time_param": None,
        "time_map": {},
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": False,
    },
    "bing_cn": {
        "name": "Bing CN",
        "name_zh": "必应中国版",
        "base_url": "https://cn.bing.com/search",
        "query_param": "q",
        "extra_params": "&ensearch=0",
        "supports_time": True,
        "time_param": "tf",
        "time_map": {
            "hour": "qdr:h",
            "day": "qdr:d",
            "week": "qdr:w",
            "month": "qdr:m",
            "year": "qdr:y",
        },
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": False,
        "region": "cn",
    },
    "bing_int": {
        "name": "Bing INT",
        "name_zh": "必应国际版",
        "base_url": "https://cn.bing.com/search",
        "query_param": "q",
        "extra_params": "&ensearch=1",
        "supports_time": True,
        "time_param": "tf",
        "time_map": {
            "hour": "qdr:h",
            "day": "qdr:d",
            "week": "qdr:w",
            "month": "qdr:m",
            "year": "qdr:y",
        },
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": False,
        "region": "global",
    },
    "360": {
        "name": "360 Search",
        "name_zh": "360搜索",
        "base_url": "https://www.so.com/s",
        "query_param": "q",
        "supports_time": False,
        "time_param": None,
        "time_map": {},
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": False,
    },
    "sogou": {
        "name": "Sogou",
        "name_zh": "搜狗",
        "base_url": "https://www.sogou.com/web",
        "query_param": "query",
        "supports_time": False,
        "time_param": None,
        "time_map": {},
        "supports_site": True,
        "site_operator": "site:",
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": False,
    },
    "wechat": {
        "name": "WeChat",
        "name_zh": "微信搜索",
        "base_url": "https://wx.sogou.com/weixin",
        "query_param": "query",
        "type_param": "type",
        "supports_time": False,
        "time_param": None,
        "time_map": {},
        "supports_site": False,
        "site_operator": None,
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": False,
    },
    "shenma": {
        "name": "Shenma",
        "name_zh": "神马搜索",
        "base_url": "https://m.sm.cn/s",
        "query_param": "q",
        "supports_time": False,
        "time_param": None,
        "time_map": {},
        "supports_site": False,
        "site_operator": None,
        "requires_api": False,
        "is_free": True,
        "privacy_friendly": False,
    },
}

# ── 便捷列表 ──────────────────────────────────────────────────────────────

# 所有可用引擎名称（去重别名）
ALL_ENGINES: List[str] = list(ENGINES.keys())

# ddgs 支持的引擎（intersection）
# 注意：ddgs CLI 的 backends 是: bing, brave, duckduckgo, mojeek, mullvad_brave, mullvad_google, wikipedia, yahoo, yandex
# 其中 google 不可用，需要在 search_ddgs 中映射到 mullvad_google
DDGS_ENGINES: List[str] = [
    "bing", "brave", "duckduckgo", "yandex", "yahoo", "wikipedia", "mojeek", "mullvad_google"
]

# 免费引擎（无 API Key 要求）
FREE_ENGINES: List[str] = [
    "brave", "ddg", "startpage", "yahoo",
    "ecosia", "qwant", "yandex", "wikipedia", "mojeek"
]

# 隐私友好引擎
PRIVACY_ENGINES: List[str] = [
    "brave", "ddg", "startpage", "ecosia", "qwant", "mojeek"
]

# 国内搜索引擎
CHINESE_ENGINES: List[str] = ["baidu", "bing_cn", "bing_int", "360", "sogou", "wechat", "shenma"]

# 国际搜索引擎（不包括特殊用途）
INTERNATIONAL_ENGINES: List[str] = [
    "google", "google_hk", "brave", "ddg", "bing", "yahoo",
    "startpage", "ecosia", "qwant", "yandex", "mojeek"
]

# 专业知识引擎
SPECIALTY_ENGINES: List[str] = ["wikipedia", "wolframalpha"]

# prismfy_search.sh 支持的引擎
PRISMFY_ENGINES: List[str] = [
    "google", "brave", "ddg", "bing", "yahoo", "startpage", "ecosia", "qwant"
]

# 默认引擎组合
DEFAULT_ENGINES: List[str] = ["google", "brave"]
DEFAULT_ENGINE: str = DEFAULT_ENGINES[0]  # 单引擎默认值（兼容旧代码）

# ── 地区代码 ──────────────────────────────────────────────────────────────

REGIONS: Dict[str, str] = {
    "us-en": "美国 (US)",
    "uk-en": "英国 (UK)",
    "au-en": "澳大利亚",
    "de-de": "德国",
    "fr-fr": "法国",
    "jp-jp": "日本",
    "cn-zh": "中国",
    "hk-hk": "香港",
    "tw-zh": "台湾",
    "kr-kr": "韩国",
    "in-en": "印度 (EN)",
}

# ── 工具函数 ──────────────────────────────────────────────────────────────

def get_engine(engine_name: str) -> Dict[str, Any]:
    """获取引擎配置，支持别名解析"""
    engine = ENGINES.get(engine_name)
    if engine and "_alias_of" in engine:
        return ENGINES[engine["_alias_of"]]
    return engine


def is_valid_engine(engine_name: str) -> bool:
    """检查引擎是否有效"""
    return engine_name in ENGINES


def is_ddgs_engine(engine_name: str) -> bool:
    """检查引擎是否被 ddgs 支持"""
    return engine_name in DDGS_ENGINES


def normalize_engine_name(engine_name: str) -> str:
    """标准化引擎名称（别名 -> 主名）"""
    engine = ENGINES.get(engine_name)
    if engine and "_alias_of" in engine:
        return engine["_alias_of"]
    return engine_name


def get_time_filter(engine_name: str, time_value: str) -> str:
    """
    获取时间过滤参数值。
    
    Args:
        engine_name: 引擎名称
        time_value: 时间值 (hour/day/week/month/year)
    
    Returns:
        时间过滤参数字符串，或空字符串表示不支持
    """
    engine = get_engine(engine_name)
    if not engine or not engine.get("supports_time"):
        return ""
    
    time_map = engine.get("time_map", {})
    time_param = engine.get("time_param")
    
    if time_value in time_map:
        mapped_value = time_map[time_value]
        return f"{time_param}={mapped_value}"
    
    return ""


def get_free_engines() -> List[str]:
    """获取所有免费引擎列表"""
    return FREE_ENGINES.copy()


def get_privacy_engines() -> List[str]:
    """获取所有隐私友好引擎列表"""
    return PRIVACY_ENGINES.copy()


if __name__ == "__main__":
    # 简单测试
    print("=== 引擎列表 ===")
    print(f"总引擎数: {len(ALL_ENGINES)}")
    print(f"ddgs 支持: {DDGS_ENGINES}")
    print(f"免费引擎: {FREE_ENGINES}")
    print(f"隐私引擎: {PRIVACY_ENGINES}")
    print()
    
    print("=== 引擎配置示例 ===")
    brave = get_engine("brave")
    print(f"Brave 时间过滤: {get_time_filter('brave', 'week')}")
    print(f"Google 时间过滤: {get_time_filter('google', 'month')}")
    print()
    
    print("=== 别名解析 ===")
    print(f"duckduckgo -> {normalize_engine_name('duckduckgo')}")
