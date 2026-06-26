#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Trending 数据源
"""

import requests
from bs4 import BeautifulSoup
from .base import BaseSource


class GitHubSource(BaseSource):
    """GitHub Trending"""
    
    def __init__(self):
        super().__init__('github', 'GitHub')
        self.url = "https://github.com/trending?since=daily&spoken_language_code=en"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        # AI 相关关键词
        self.keywords = [
            'ai', 'machine-learning', 'deep-learning', 'llm',
            'chatgpt', 'gpt', 'transformer', 'neural', 'model'
        ]
    
    def fetch(self):
        """获取 GitHub Trending"""
        resp = requests.get(self.url, headers=self.headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        topics = []
        repos = soup.select('article.Box-row')[:20]
        
        for repo in repos:
            title_elem = repo.select_one('h2 a')
            if not title_elem:
                continue
            
            title = title_elem.get_text(strip=True).replace('\n', '').replace(' ', '')
            desc_elem = repo.select_one('p')
            desc = desc_elem.get_text(strip=True) if desc_elem else ''
            
            # 筛选 AI 相关项目
            if any(kw in title.lower() or kw in desc.lower() for kw in self.keywords):
                topics.append({
                    'title': title,
                    'url': f"https://github.com{title_elem.get('href', '')}",
                    'summary': desc,
                    'hot': 0
                })
        
        return topics


# 测试
if __name__ == '__main__':
    source = GitHubSource()
    topics = source.fetch_with_error_handling()
    print(f"✅ GitHub Trending：{len(topics)} 条\n")
    for i, t in enumerate(topics[:5], 1):
        print(f"{i}. {t['title']}")
        if t['summary']:
            print(f"   {t['summary'][:80]}...")
