#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知乎热榜数据源
"""

import requests
from .base import BaseSource


class ZhihuSource(BaseSource):
    """知乎热榜"""
    
    def __init__(self):
        super().__init__('zhihu', '知乎')
        self.api_url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        # AI 相关关键词
        self.keywords = [
            'AI', '人工智能', 'ChatGPT', 'GPT', 'Claude', '大模型',
            'OpenAI', '效率', '工具', '自动化', '科技'
        ]
    
    def fetch(self):
        """获取知乎热榜"""
        resp = requests.get(self.api_url, headers=self.headers, timeout=10)
        data = resp.json()
        
        topics = []
        for item in data.get('data', []):
            target = item.get('target', {})
            title = target.get('title', '')
            
            # 只保留 AI 相关
            if any(kw in title for kw in self.keywords):
                topics.append({
                    'title': title,
                    'url': target.get('url', ''),
                    'summary': target.get('excerpt', ''),
                    'hot': item.get('detail_text', '')
                })
        
        return topics[:20]


# 测试
if __name__ == '__main__':
    source = ZhihuSource()
    topics = source.fetch_with_error_handling()
    print(f"✅ 知乎热榜：{len(topics)} 条\n")
    for i, t in enumerate(topics[:5], 1):
        print(f"{i}. {t['title']}")
