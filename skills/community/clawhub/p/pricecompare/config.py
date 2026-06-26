#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
"""

import os

# API配置
# 开发环境: http://localhost:8000
# 生产环境: https://op.squirrel2.cn
API_BASE_URL = os.getenv('API_BASE_URL', 'https://op.squirrel2.cn')
API_PREFIX = '/api/v1'
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))

PLATFORMS = {
    'jd': {
        'name': '京东',
        'keywords': ['京东', 'jd.com', 'jingfen', 'u.jd.com', '3.cn'],
        'link_patterns': [
            r'https?://item\.jd\.com/\d+\.html',
            r'https?://u\.jd\.com/[\w\-]+',
            r'https?://3\.cn/[\w\-]+',
            r'https?://jingfen\.jd\.com/detail/[\w\-]+',
        ]
    },
    'taobao': {
        'name': '淘宝',
        'keywords': ['淘宝', '天猫', 'taobao.com', 'tmall.com', 'tb.cn'],
        'link_patterns': [
            r'https?://item\.taobao\.com/item\.htm\?id=\d+',
            r'https?://detail\.tmall\.com/item\.htm\?id=\d+',
            r'https?://m\.tb\.cn/[\w\-]+',
            r'https?://e\.tb\.cn/[\w\-]+',
            r'https?://s\.click\.taobao\.com/[\w\-]+',
        ]
    },
    'pinduoduo': {
        'name': '拼多多',
        'keywords': ['拼多多', 'pinduoduo.com', 'yangkeduo.com'],
        'link_patterns': [
            r'https?://mobile\.yangkeduo\.com/goods\.html\?goods_id=\d+',
            r'https?://p\.pinduoduo\.com/[\w\-]+',
            r'https?://yangkeduo\.com/goods\.html\?goods_id=\d+',
        ]
    }
}

TOKEN_PATTERNS = {
    'jd_prefix': r'\d{2,}:/',            # JD 数字前缀: 10:/ 19:/ 17:/ 等
    'jd_ca_suffix': r'\sCA\d{4}',         # JD CA后缀: CA3576 CA8680 等
    'jd_fullwidth_bang': r'\uff01([A-Za-z0-9]{10,30})\uff01',  # JD 全角叹号: ！CODE！
    'halfwidth_bang': r'!([A-Za-z0-9]{10,30})!',  # 半角叹号: !CODE!
    'symmetric': [
        ('$', '$'), ('%', '%'), ('#', '#'), ('@', '@'), ('&', '&'),
        ('\uffe5', '\uffe5'),  # ￥
    ],
    'special_format': [
        r'\$[^\$\s]{8,}\$://',
        r'\uffe5[^\uffe5\s]{8,}\uffe5://',
    ],
    'mixed_string': {
        'min_length': 17,
        'min_types': 2,
        'exclude_urls': True,
    }
}

DEFAULT_SEARCH_PAGE_SIZE = 10  # 拼多多要求 >= 10
MAX_SEARCH_RESULTS = 10

# Skill 本地版本，发布时需同步更新
SKILL_VERSION = "1.5.1"

ERROR_MESSAGES = {
    'parse_failed': '口令解析失败',
    'invalid_link': '无法识别的链接格式',
    'no_results': '未找到相关商品',
    'api_error': '系统繁忙，请稍后重试',
    'platform_not_supported': '不支持的平台',
}

SUCCESS_MESSAGES = {
    'parse_success': '商品信息已解析',
    'search_success': '找到相关商品',
    'convert_success': '优惠链接已生成',
    'compare_success': '价格对比完成',
}
