#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility Functions Module
工具函数模块：提供通用的辅助功能
"""

import os
import json
import hashlib
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import requests

def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    计算文本相似度（余弦相似度）
    
    Args:
        text1: 文本1
        text2: 文本2
        
    Returns:
        相似度分数 (0-1)
    """
    try:
        # 简单的基于词频的相似度计算
        from collections import Counter
        import math
        
        def get_word_vector(text):
            # 简单分词（按空格和标点）
            words = re.findall(r'\w+', text.lower())
            return Counter(words)
        
        vec1 = get_word_vector(text1)
        vec2 = get_word_vector(text2)
        
        if not vec1 or not vec2:
            return 0.0
        
        # 计算余弦相似度
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        
        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        
        if not denominator:
            return 0.0
            
        return numerator / denominator
        
    except Exception as e:
        print(f"计算文本相似度失败: {e}")
        return 0.0

def is_valid_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_time_format(time_str: str) -> bool:
    """验证时间格式 HH:MM"""
    pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
    return re.match(pattern, time_str) is not None

def get_domain_from_url(url: str) -> str:
    """从URL提取域名"""
    try:
        from urllib.parse import urlparse
        return urlparse(url).netloc
    except:
        return ''

def validate_news_item(news_item: Dict[str, Any]) -> bool:
    """验证新闻条目是否有效"""
    required_fields = ['title', 'url']
    for field in required_fields:
        if field not in news_item or not news_item[field]:
            return False
    
    # 检查标题长度
    if len(news_item['title']) < 5:
        return False
    
    # 检查URL有效性
    if not news_item['url'].startswith(('http://', 'https://')):
        return False
    
    return True

def filter_news_by_date(news_items: List[Dict[str, Any]], days: int = 7) -> List[Dict[str, Any]]:
    """根据日期过滤新闻"""
    cutoff_date = datetime.now() - timedelta(days=days)
    filtered_news = []
    
    for news in news_items:
        try:
            pub_date_str = news.get('published', '')
            if not pub_date_str:
                filtered_news.append(news)
                continue
                
            # 尝试解析日期
            pub_date = parse_date_string(pub_date_str)
            if pub_date and pub_date >= cutoff_date:
                filtered_news.append(news)
                
        except Exception:
            # 无法解析日期的新闻保留
            filtered_news.append(news)
    
    return filtered_news

def parse_date_string(date_str: str) -> Optional[datetime]:
    """解析日期字符串"""
    if not date_str:
        return None
    
    # 常见日期格式
    formats = [
        '%Y-%m-%d',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y/%m/%d',
        '%Y年%m月%d日',
        '%a, %d %b %Y %H:%M:%S %Z',
        '%a, %d %b %Y %H:%M:%S',
        '%d %b %Y %H:%M:%S %Z',
        '%d %b %Y %H:%M:%S'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    # 尝试使用dateutil（如果可用）
    try:
        from dateutil import parser
        return parser.parse(date_str)
    except ImportError:
        pass
    except Exception:
        pass
    
    return None

def generate_news_id(title: str, url: str) -> str:
    """生成新闻唯一ID"""
    combined = f"{title}_{url}"
    return hashlib.md5(combined.encode()).hexdigest()

def check_url_accessibility(url: str, timeout: int = 10) -> bool:
    """检查URL可访问性"""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code == 200
    except:
        try:
            response = requests.get(url, timeout=timeout, allow_redirects=True)
            return response.status_code == 200
        except:
            return False

def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    
    # 在句子边界处截断
    sentence_endings = ['。', '！', '？', '.', '!', '?']
    truncated = text[:max_length]
    
    # 查找最后一个句子结束符
    last_end = -1
    for ending in sentence_endings:
        pos = truncated.rfind(ending)
        if pos > last_end:
            last_end = pos
    
    if last_end > 0:
        return truncated[:last_end + 1]
    else:
        return truncated + suffix

def merge_configs(base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
    """合并配置字典"""
    merged = base_config.copy()
    merged.update(override_config)
    return merged

def ensure_directory_exists(directory_path: str):
    """确保目录存在"""
    Path(directory_path).mkdir(parents=True, exist_ok=True)

def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载JSON文件失败 {file_path}: {e}")
        return None

def save_json_file(file_path: str, data: Dict[str, Any]):
    """保存JSON文件"""
    try:
        ensure_directory_exists(Path(file_path).parent)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存JSON文件失败 {file_path}: {e}")

def get_current_timestamp() -> str:
    """获取当前时间戳"""
    return datetime.now().isoformat()

def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {size_names[i]}"

# 导出常用函数
__all__ = [
    'calculate_text_similarity',
    'is_valid_email', 
    'is_valid_time_format',
    'get_domain_from_url',
    'validate_news_item',
    'filter_news_by_date',
    'parse_date_string',
    'generate_news_id',
    'check_url_accessibility',
    'truncate_text',
    'merge_configs',
    'ensure_directory_exists',
    'load_json_file',
    'save_json_file',
    'get_current_timestamp',
    'format_size'
]