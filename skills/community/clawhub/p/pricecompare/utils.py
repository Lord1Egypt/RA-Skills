#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数
"""

import re
import requests
from typing import Optional, Dict, Any, List
try:
    from config import (
        API_BASE_URL, API_PREFIX, API_TIMEOUT,
        PLATFORMS, TOKEN_PATTERNS
    )
except ImportError:
    from .config import (
        API_BASE_URL, API_PREFIX, API_TIMEOUT,
        PLATFORMS, TOKEN_PATTERNS
    )


def call_api(endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    调用服务器API

    Args:
        endpoint: API端点
        data: 请求数据

    Returns:
        API响应数据，失败返回None
    """
    try:
        url = f"{API_BASE_URL}{API_PREFIX}{endpoint}"
        response = requests.post(url, json=data, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {'success': False, 'error': '请求超时，请稍后重试'}
    except requests.exceptions.ConnectionError:
        return {'success': False, 'error': '无法连接到服务器，请检查服务器是否运行'}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': f'请求失败: {str(e)}'}
    except Exception as e:
        return {'success': False, 'error': f'未知错误: {str(e)}'}


def detect_platform(text: str) -> Optional[str]:
    """
    检测文本所属平台

    Args:
        text: 输入文本

    Returns:
        平台代码，未识别返回None
    """
    text_lower = text.lower()

    for platform_code, platform_info in PLATFORMS.items():
        for keyword in platform_info['keywords']:
            if keyword.lower() in text_lower:
                return platform_code

    for platform_code, platform_info in PLATFORMS.items():
        for pattern in platform_info['link_patterns']:
            if re.search(pattern, text, re.IGNORECASE):
                return platform_code

    return None


def is_token_format(content: str) -> bool:
    """
    检测内容是否包含口令格式（与服务器端 goods.py 保持一致）

    优先级：
    1. 京东专用: 数字:/前缀、！CODE！、CA数字后缀
    2. 半角感叹号: !CODE!
    3. 淘宝: $...$:// 等特殊格式
    4. 对称符号包裹的纯代码
    5. 17位以上混合字符串

    Args:
        content: 输入内容

    Returns:
        是否为口令格式
    """
    # 纯URL跳过
    stripped = content.strip()
    if stripped.startswith(('http://', 'https://')):
        return False

    # --- JD专用模式 ---
    jd_prefix = getattr(TOKEN_PATTERNS, 'get', lambda k, d: d)(
        'jd_prefix', TOKEN_PATTERNS.get('jd_prefix', r'\d{2,}:/'))
    if isinstance(jd_prefix, str) and re.search(jd_prefix, content):
        return True

    ca_suffix = TOKEN_PATTERNS.get('jd_ca_suffix', r'\sCA\d{4}')
    if isinstance(ca_suffix, str) and re.search(ca_suffix, content):
        return True

    fb_bang = TOKEN_PATTERNS.get('jd_fullwidth_bang', r'\uff01([A-Za-z0-9]{10,30})\uff01')
    if isinstance(fb_bang, str) and re.search(fb_bang, content):
        return True

    hw_bang = TOKEN_PATTERNS.get('halfwidth_bang', r'!([A-Za-z0-9]{10,30})!')
    if isinstance(hw_bang, str) and re.search(hw_bang, content):
        return True

    # --- 特殊格式（淘宝$://等） ---
    for pattern in TOKEN_PATTERNS.get('special_format', []):
        if re.search(pattern, content):
            return True

    # --- 对称符号（只匹配纯代码，不含中文） ---
    for start, end in TOKEN_PATTERNS.get('symmetric', []):
        inner = r'[A-Za-z0-9!@#$%^&*()_+\-=\[\]{}|;:.,<>?/~]{10,}'
        pattern = re.escape(start) + inner + re.escape(end)
        if re.search(pattern, content):
            return True

    # --- 混合字符串（排除URL） ---
    ms = TOKEN_PATTERNS.get('mixed_string', {})
    if ms.get('exclude_urls', False):
        content = re.sub(r'https?://[^\s]+', '', content)

    token_pattern = r'[A-Za-z0-9!@#$%^&*()_+\-=\[\]{}|;:\'",.<>?/~`]{17,}'
    matches = re.findall(token_pattern, content)

    for match in matches:
        has_upper = any(c.isupper() for c in match)
        has_lower = any(c.islower() for c in match)
        has_digit = any(c.isdigit() for c in match)
        has_special = any(not c.isalnum() for c in match)
        type_count = sum([has_upper, has_lower, has_digit, has_special])
        if type_count >= ms.get('min_types', 2):
            return True

    return False


detect_token = is_token_format


def extract_platform_keyword(text: str) -> Optional[str]:
    """
    从文本中提取平台关键词

    Args:
        text: 输入文本

    Returns:
        平台代码，未找到返回None
    """
    patterns = {
        'jd': r'(?:在|用)?京东(?:搜索|找)?',
        'taobao': r'(?:在|用)?(?:淘宝|天猫)(?:搜索|找)?',
        'pinduoduo': r'(?:在|用)?拼多多(?:搜索|找)?',
    }

    for platform, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            return platform

    return None


def extract_search_keyword(text: str) -> tuple:
    """
    从文本中提取搜索关键词和平台

    Args:
        text: 输入文本

    Returns:
        (搜索关键词, 平台) 元组，未找到返回 (None, None)
    """
    platform_patterns = {
        'jd': r'^(?:在|用)?京东(?:搜索|找)?\s*(.+)$',
        'taobao': r'^(?:在|用)?(?:淘宝|天猫)(?:搜索|找)?\s*(.+)$',
        'pinduoduo': r'^(?:在|用)?拼多多(?:搜索|找)?\s*(.+)$',
    }

    for platform, pattern in platform_patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return (match.group(1).strip(), platform)

    general_patterns = [
        r'^(?:搜索|查询|找|查找|搜寻)\s*(.+)$',
    ]

    for pattern in general_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return (match.group(1).strip(), None)

    return (None, None)


def is_compare_request(text: str) -> bool:
    """
    检测是否为价格对比请求

    Args:
        text: 输入文本

    Returns:
        是否为价格对比请求
    """
    patterns = [
        r'^(?:对比|比价|价格对比)',
        r'对比.*价格',
        r'比较.*价格',
    ]

    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


def extract_compare_keyword(text: str) -> Optional[str]:
    """
    从文本中提取价格对比关键词

    Args:
        text: 输入文本

    Returns:
        对比关键词，未找到返回None
    """
    patterns = [
        r'^(?:对比|比价|价格对比)\s*(.+)$',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return None


def extract_url(text: str) -> Optional[str]:
    """
    从文本中提取URL

    Args:
        text: 输入文本

    Returns:
        URL，未找到返回None
    """
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    match = re.search(url_pattern, text)
    if match:
        return match.group(0)
    return None


def calculate_save_amount(original_price: float, final_price: float) -> float:
    """
    计算节省金额

    Args:
        original_price: 原价
        final_price: 券后价

    Returns:
        节省金额
    """
    if original_price <= 0 or final_price <= 0:
        return 0

    save_amount = original_price - final_price
    return max(save_amount, 0)


def calculate_discount(original_price: float, final_price: float) -> str:
    """
    计算折扣

    Args:
        original_price: 原价
        final_price: 券后价

    Returns:
        折扣字符串
    """
    if original_price <= 0 or final_price <= 0:
        return ''

    discount = (final_price / original_price) * 10
    discount = max(discount, 1)

    return f"{discount:.1f}折"


def format_price(price: float) -> str:
    """
    格式化价格

    Args:
        price: 价格

    Returns:
        格式化后的价格字符串
    """
    if price <= 0:
        return '¥0.00'

    return f"¥{price:.2f}"
