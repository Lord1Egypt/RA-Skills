#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
36氪数据源
科技资讯和创业新闻
"""

import requests
from bs4 import BeautifulSoup
from .base import BaseSource


class Kr36Source(BaseSource):
    """36氪"""
    
    def __init__(self):
        super().__init__('36kr', '36氪')
        self.url = "https://www.36kr.com/information/artificial_intelligence/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        self.keywords = ['AI', '人工智能', 'ChatGPT', '大模型', '智能']
    
    def fetch(self):
        """获取36氪 AI 频道"""
        try:
            resp = requests.get(self.url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            topics = []
            
            # 36氪文章列表
            articles = soup.select('.article-item-title a')[:20]
            
            for article in articles:
                title = article.get_text(strip=True)
                url = article.get('href', '')
                
                if url and not url.startswith('http'):
                    url = f"https://www.36kr.com{url}"
                
                # 筛选 AI 相关
                if any(kw in title for kw in self.keywords):
                    topics.append({
                        'title': title,
                        'url': url,
                        'summary': '',
                        'hot': 0
                    })
            
            return topics
            
        except Exception as e:
            # 如果页面结构变化，尝试备用方案
            return self._fetch_from_api()
    
    def _fetch_from_api(self):
        """备用方案：通过 API 获取"""
        try:
            api_url = "https://www.36kr.com/api/search-column/mainsite"
            params = {
                'per_page': 20,
                'column_id': 'artificial_intelligence'
            }
            resp = requests.get(api_url, params=params, headers=self.headers, timeout=10)
            data = resp.json()
            
            topics = []
            for item in data.get('data', {}).get('items', []):
                title = item.get('title', '')
                if any(kw in title for kw in self.keywords):
                    topics.append({
                        'title': title,
                        'url': f"https://www.36kr.com/p/{item.get('id', '')}",
                        'summary': item.get('summary', ''),
                        'hot': 0
                    })
            
            return topics
        except:
            return []


# 测试
if __name__ == '__main__':
    source = Kr36Source()
    topics = source.fetch_with_error_handling()
    print(f"✅ 36氪：{len(topics)} 条\n")
    for i, t in enumerate(topics[:5], 1):
        print(f"{i}. {t['title']}")
