# -*- coding: utf-8 -*-
"""
相似度计算模块
"""

import re
from collections import Counter


def tokenize(text):
    """
    中文分词（简单版：按字符 n-gram）
    """
    # 清理噪声
    text = re.sub(r'[^\w\u4e00-\u9fff]', '', text)
    
    # 使用 2-gram 分词
    n = 2
    tokens = [text[i:i+n] for i in range(len(text) - n + 1)]
    
    return tokens


def calculate_similarity(text1, text2):
    """
    计算两段文本的 Jaccard 相似度
    
    Args:
        text1: 文本 1
        text2: 文本 2
    
    Returns:
        float: 相似度 (0-1)
    """
    if not text1 or not text2:
        return 0.0
    
    # 分词
    tokens1 = set(tokenize(text1))
    tokens2 = set(tokenize(text2))
    
    if not tokens1 or not tokens2:
        return 0.0
    
    # Jaccard 相似度
    intersection = tokens1 & tokens2
    union = tokens1 | tokens2
    
    similarity = len(intersection) / len(union)
    
    return similarity


def calculate_similarity_weighted(text1, text2):
    """
    计算加权相似度（标题权重更高）
    
    Args:
        title1, summary1: 文本 1 的标题和摘要
        title2, summary2: 文本 2 的标题和摘要
    
    Returns:
        float: 相似度 (0-1)
    """
    # 简单版本：直接计算整体相似度
    return calculate_similarity(text1, text2)


def find_duplicates(news_list, threshold=0.90):
    """
    查找重复新闻
    
    Args:
        news_list: 新闻列表，每项包含 'title', 'summary'
        threshold: 相似度阈值
    
    Returns:
        list: 重复新闻的索引列表
    """
    dup_indices = set()
    
    for i in range(len(news_list)):
        if i in dup_indices:
            continue
        
        text1 = news_list[i].get('title', '') + ' ' + (news_list[i].get('summary', '') or '')
        
        for j in range(i + 1, len(news_list)):
            if j in dup_indices:
                continue
            
            text2 = news_list[j].get('title', '') + ' ' + (news_list[j].get('summary', '') or '')
            similarity = calculate_similarity(text1, text2)
            
            if similarity >= threshold:
                dup_indices.add(j)
                news_list[j]['similarity'] = similarity
                news_list[j]['duplicate_of'] = i
    
    return list(dup_indices)
