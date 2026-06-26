#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度热搜数据源
"""

import requests
from .base import BaseSource


class BaiduSource(BaseSource):
    """百度热搜"""
    
    def __init__(self):
        super().__init__('baidu', '百度')
        self.url = "https://top.baidu.com/api/board?platform=wise&tab=realtime"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        self.keywords = ['AI', '人工智能', 'ChatGPT', 'GPT', 'Claude', '大模型', '智能', '科技']
    
    def fetch(self):
        """获取百度热搜"""
        try:
            resp = requests.get(self.url, headers=self.headers, timeout=10)
            data = resp.json()
            
            topics = []
            
            for item in data.get('data', {}).get('cards', []):
                for content in item.get('content', []):
                    title = content.get('word', '')
                    url = content.get('url', '')
                    hot = content.get('hotScore', 0)
                    
                    # 筛选 AI 相关
                    if any(kw in title for kw in self.keywords):
                        topics.append({
                            'title': title,
                            'url': url if url else f"https://www.baidu.com/s?wd={title}",
                            'summary': content.get('desc', ''),
                            'hot': hot
                        })
            
            return topics[:20]
            
        except Exception:
            return []


# 测试
if __name__ == '__main__':
    source = BaiduSource()
    topics = source.fetch_with_error_handling()
    print(f"✅ 百度热搜：{len(topics)} 条\n")
    for i, t in enumerate(topics[:5], 1):
        print(f"{i}. {t['title']} (热度: {t['hot']})")
