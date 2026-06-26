#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IT之家数据源
科技新闻资讯
"""

import requests
from bs4 import BeautifulSoup
from .base import BaseSource


class IthomeSource(BaseSource):
    """IT之家"""
    
    def __init__(self):
        super().__init__('ithome', 'IT之家')
        self.url = "https://www.ithome.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        self.keywords = ['AI', '人工智能', 'ChatGPT', 'GPT', 'Claude', '大模型', '智能']
    
    def fetch(self):
        """获取IT之家热门"""
        try:
            resp = requests.get(self.url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            topics = []
            
            # IT之家文章列表
            articles = soup.select('.lst-article li a')[:30]
            
            for article in articles:
                title = article.get_text(strip=True)
                url = article.get('href', '')
                
                if not url:
                    continue
                
                if not url.startswith('http'):
                    url = f"https://www.ithome.com{url}"
                
                # 筛选 AI 相关
                if any(kw in title for kw in self.keywords):
                    topics.append({
                        'title': title,
                        'url': url,
                        'summary': '',
                        'hot': 0
                    })
            
            return topics[:20]
            
        except Exception:
            return []


# 测试
if __name__ == '__main__':
    source = IthomeSource()
    topics = source.fetch_with_error_handling()
    print(f"✅ IT之家：{len(topics)} 条\n")
    for i, t in enumerate(topics[:5], 1):
        print(f"{i}. {t['title']}")
