# -*- coding: utf-8 -*-
"""
过滤规则模块 v2
引用 rules_config 的统一配置
"""

import re
try:
    from .config import CORE_KEYWORDS, AUXILIARY_KEYWORDS, HOLIDAYS_2026
    from .rules_config import (
        EXCLUDED_TOPICS,
        INVALID_KEYWORDS,
        is_excluded_by_topic,
        is_public_notice,
        contains_invalid_keyword
    )
except ImportError:
    from config import CORE_KEYWORDS, AUXILIARY_KEYWORDS, HOLIDAYS_2026
    from rules_config import (
        EXCLUDED_TOPICS,
        INVALID_KEYWORDS,
        is_excluded_by_topic,
        is_public_notice,
        contains_invalid_keyword
    )


def is_excluded_topic(title, content):
    """
    检查是否为排除主题（调用 rules_config 的统一函数）
    """
    return is_excluded_by_topic(title + ' ' + content)


def is_relevant(title, content):
    """
    检查相关性
    """
    text = (title + ' ' + content).lower()
    
    # 核心关键词
    if any(kw in text for kw in CORE_KEYWORDS):
        return True
    
    # 辅助关键词≥2
    aux_count = sum(1 for kw in AUXILIARY_KEYWORDS if kw in text)
    if aux_count >= 2:
        return True
    
    return False


def is_valid_news(title, content, url):
    """
    验证新闻有效性
    """
    # 标题长度
    if len(title) < 10 or len(title) > 100:
        return False, "Title length"
    
    # 内容长度
    if len(content) < 100:
        return False, "Content too short"
    
    # 排除纯公告类（汇率中间价等无信息增量的公告）
    if is_public_notice(title):
        return False, "Public notice"

    # 排除主题
    if is_excluded_topic(title, content):
        return False, "Excluded topic"
    
    # 相关性
    if not is_relevant(title, content):
        return False, "Not relevant"
    
    # 无效关键词（调用统一函数）
    if contains_invalid_keyword(title + ' ' + content):
        return False, "Invalid keyword"
    
    # URL 检查
    url_lower = url.lower()
    if any(p in url_lower for p in ['/about/', '/contact', '/jobs', '.pdf']):
        return False, "Invalid URL"
    
    return True, "OK"


def clean_content(content):
    """
    清理内容
    """
    # 清理电头
    content = re.sub(r'^[（(]?新华社 [^）)]*[）)]?', '', content, flags=re.MULTILINE)
    content = re.sub(r'^[（(]?人民日报 [^）)]*[）)]?', '', content, flags=re.MULTILINE)
    content = re.sub(r'^[（(]?光明日报 [^）)]*[）)]?', '', content, flags=re.MULTILINE)
    content = re.sub(r'^[（(]?科技日报 [^）)]*[）)]?', '', content, flags=re.MULTILINE)
    content = re.sub(r'^记者\s*\S+\s*报道', '', content, flags=re.MULTILINE)
    
    # 清理副标题
    content = re.sub(r'^——.*$', '', content, flags=re.MULTILINE)
    
    # 清理网页导航
    content = re.sub(r'当前位置：.*', '', content, flags=re.MULTILINE)
    content = re.sub(r'地方频道.*', '', content, flags=re.MULTILINE)
    content = re.sub(r'本文链接：.*', '', content, flags=re.MULTILINE)
    content = re.sub(r'责任编辑：.*', '', content, flags=re.MULTILINE)
    
    # 清理空行
    content = re.sub(r'\n\s*\n', '\n', content)
    content = re.sub(r'  +', ' ', content)
    
    return content.strip()
