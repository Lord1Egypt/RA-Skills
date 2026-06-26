#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虎嗅数据源
科技媒体资讯
"""

import requests
from bs4 import BeautifulSoup
from .base import BaseSource


class HuxiuSource(BaseSource):
    """虎嗅"""
    
    def __init__(self):
        super().__init__('huxiu', '虎嗅')
        self.url = "https://www.huxiu.com/channel/105.html"  # 科技频道
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        self.keywords = ['AI', '人工智能', 'ChatGPT', '大模型', '智能', '科技']
    
    def fetch(self):
        """获取虎嗅科技频道"""
        try:
            resp = requests.get(self.url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            topics = []
            
            # 虎嗅文章列表
            articles = soup.select('.article-item__title a')[:20]
            
            for article in articles:
                title = article.get_text(strip=True)
                url = article.get('href', '')
                
                if url and not url.startswith('http'):
                    url = f"https://www.huxiu.com{url}"
                
                # 筛选 AI 相关
                if any(kw in title for kw in self.keywords):
                    topics.append({
                        'title': title,
                        'url': url,
                        'summary': '',
                        'hot': 0
                    })
            
            return topics
            
        except Exception:
            return []


# 测试
if __name__ == '__main__':
    source = HuxiuSource()
    topics = source.fetch_with_error_handling()
    print(f"✅ 虎嗅：{len(topics)} 条\n")
    for i, t in enumerate(topics[:5], 1):
        print(f"{i}. {t['title']}")
