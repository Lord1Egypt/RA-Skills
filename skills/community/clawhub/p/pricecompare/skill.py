#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
省钱购物助手 Skill
"""

import re
from typing import Optional, Dict, Any
import os

try:
    from config import PLATFORMS, TOKEN_PATTERNS, DEFAULT_SEARCH_PAGE_SIZE, SKILL_VERSION
    from utils import (
        call_api, detect_platform, extract_url
    )
    from formatters import (
        format_search_results, format_convert_result, format_parse_result,
        format_compare_result, format_error_message
    )
except ImportError:
    from .config import PLATFORMS, TOKEN_PATTERNS, DEFAULT_SEARCH_PAGE_SIZE, SKILL_VERSION
    from .utils import (
        call_api, detect_platform, extract_url
    )
    from .formatters import (
        format_search_results, format_convert_result, format_parse_result,
        format_compare_result, format_error_message
    )

# ---------- 版本检查 ----------

from datetime import date

CLAWHUB_SLUG = "pricecompare"
CLAWHUB_API = f"https://clawhub.ai/api/v1/skills/{CLAWHUB_SLUG}"
CLAWHUB_URL = f"https://clawhub.ai/skills/{CLAWHUB_SLUG}"

_version_last_checked = None
_update_hint = ""

def _check_version():
    """通过 ClawHub API 检查最新版本，每天最多一次，不匹配时生成更新提示"""
    global _version_last_checked, _update_hint
    if os.getenv("PRICECOMPARE_NO_VERSION_CHECK"):
        return
    today = date.today()
    if _version_last_checked == today:
        return
    _version_last_checked = today

    try:
        import requests
        resp = requests.get(CLAWHUB_API, timeout=5)
        if resp.status_code == 200:
            info = resp.json()
            latest = info.get("latestVersion", {})
            remote = latest.get("version", "")

            if remote and remote != SKILL_VERSION:
                _update_hint = (
                    f"\n\n---\n"
                    f"🔄 **Skill 版本更新**\n"
                    f"当前: {SKILL_VERSION} → 最新: {remote}\n"
                    f"请更新: `openclaw skills install {CLAWHUB_SLUG}`\n"
                    f"项目地址: {CLAWHUB_URL}"
                )
    except Exception:
        pass  # 版本检查失败不影响主功能

# 模块导入时自动检查一次（不阻塞，失败静默）
try:
    _check_version()
except Exception:
    pass


def _wrapped_call_api(endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """封装 call_api，附带版本检查"""
    _check_version()
    return call_api(endpoint, data)


def search_goods(keyword: str, platform: str = None, page_size: int = DEFAULT_SEARCH_PAGE_SIZE) -> str:
    """
    搜索商品

    Args:
        keyword: 搜索关键词
        platform: 平台标识（可选）
        page_size: 每页数量

    Returns:
        格式化的搜索结果
    """
    if platform:
        result = _wrapped_call_api('/search', {
            'platform': platform,
            'keyword': keyword,
            'page': 1,
            'page_size': page_size
        })
    else:
        result = _wrapped_call_api('/compare', {
            'keyword': keyword
        })

        if result and result.get('success'):
            comparison = result.get('comparison', [])
            return format_search_results(comparison, keyword)

    if not result:
        return format_error_message('api_error')

    if not result.get('success'):
        error = result.get('error', '未知错误')
        return f"❌ 搜索失败：{error}"

    data = result.get('data', [])
    return format_search_results(data if isinstance(data, list) else [data], keyword)


def convert_link(url: str, platform: str = None) -> str:
    """
    转换链接

    Args:
        url: 商品链接
        platform: 平台标识（可选）

    Returns:
        格式化的转换结果
    """
    if not platform:
        platform = detect_platform(url)

    if not platform:
        return format_error_message('invalid_link')

    result = _wrapped_call_api('/convert', {
        'platform': platform,
        'url': url
    })

    if not result:
        return format_error_message('api_error')

    if not result.get('success'):
        error = result.get('error', '未知错误')
        return f"❌ 转换失败：{error}"

    return format_convert_result(result)


def parse_share_content(content: str) -> str:
    """
    解析分享内容

    Args:
        content: 分享内容

    Returns:
        格式化的解析结果
    """
    result = _wrapped_call_api('/parse_share', {
        'content': content
    })

    if not result:
        return format_error_message('api_error')

    if not result.get('success'):
        return format_error_message('parse_failed')

    platform = result.get('platform', '未知平台')
    data = result.get('data', result)

    return format_parse_result(data, platform)


def compare_prices(keyword: str) -> str:
    """
    价格对比

    Args:
        keyword: 商品关键词

    Returns:
        格式化的对比结果
    """
    result = _wrapped_call_api('/compare', {
        'keyword': keyword
    })

    if not result:
        return format_error_message('api_error')

    if not result.get('success'):
        error = result.get('error', '未知错误')
        return f"❌ 价格对比失败：{error}"

    return format_compare_result(result)


def handle_message(message: str, keyword: str = None) -> Optional[str]:
    """
    处理用户消息（主入口函数）

    Args:
        message: 用户输入的原始消息（用于路由判断——检测 URL）
        keyword: agent 提取的商品关键词（用于搜索/比价），不提供时回退到 message

    Returns:
        格式化结果字符串，无需处理返回 None
    """
    if not message or not message.strip():
        return None

    message = message.strip()
    search_kw = keyword or message
    result = None

    # 1. 检测 URL → 转链
    url = extract_url(message)
    if url:
        result = convert_link(url)
    else:
        # 2. 先试口令解析，失败 fallback 到搜索
        result = parse_share_content(message)
        if not result or '失败' in result:
            result = search_goods(search_kw)

    if result and _update_hint:
        result = _update_hint + "\n" + result
    return result


# ==================== 测试入口 ====================

if __name__ == '__main__':
    import sys

    print("=" * 60)
    print("省钱购物助手 Skill 测试")
    print("=" * 60)

    test_cases = [
        ("https://item.jd.com/10021724657015.html", None),
        ("帮我查一下iPhone 16的价格", "iPhone 16"),
        ("【淘宝】假一赔四 https://e.tb.cn/h.iVW7Wnbs5Woz1ZI", None),
    ]

    if len(sys.argv) > 1:
        test_message = ' '.join(sys.argv[1:])
        print(f"输入: {test_message}")
        print()
        result = handle_message(test_message)
        print(result or "无需处理")
    else:
        for test_msg, test_kw in test_cases:
            print(f"\n{'=' * 60}")
            print(f"输入: {test_msg}")
            if test_kw:
                print(f"关键词: {test_kw}")
            print('-' * 60)
            result = handle_message(test_msg, keyword=test_kw)
            print(result or "无需处理")
