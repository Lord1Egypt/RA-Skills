#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据源开发模板
复制此文件并修改即可快速创建新数据源
"""

import requests
from .base import BaseSource


class TemplateSource(BaseSource):
    """数据源模板"""
    
    def __init__(self):
        # 修改这里：数据源标识和显示名称
        super().__init__('template', '模板平台')
        
        # 修改这里：API 地址
        self.api_url = "https://api.example.com/hot"
        
        # 修改这里：请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        
        # 修改这里：筛选关键词
        self.keywords = ['AI', '人工智能', 'ChatGPT']
    
    def fetch(self):
        """
        获取热点数据
        
        必须返回列表，每个元素包含：
        - title: 标题（必填）
        - url: 链接（必填）
        - summary: 摘要（选填）
        - hot: 热度值（选填）
        """
        # 修改这里：实现你的数据获取逻辑
        resp = requests.get(self.api_url, headers=self.headers, timeout=10)
        data = resp.json()
        
        topics = []
        
        # 修改这里：解析 API 返回的数据
        for item in data.get('items', []):
            title = item.get('title', '')
            
            # 修改这里：筛选逻辑（可选）
            if any(kw in title for kw in self.keywords):
                topics.append({
                    'title': title,
                    'url': item.get('url', ''),
                    'summary': item.get('description', ''),
                    'hot': item.get('hot_score', 0)
                })
        
        return topics[:20]  # 返回前20条


# 测试代码
if __name__ == '__main__':
    source = TemplateSource()
    topics = source.fetch_with_error_handling()
    print(f"✅ {source.platform_name}：{len(topics)} 条\n")
    for i, t in enumerate(topics[:5], 1):
        print(f"{i}. {t['title']}")
