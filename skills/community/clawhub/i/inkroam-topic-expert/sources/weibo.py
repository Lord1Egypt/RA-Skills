#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜数据源
"""

import requests
from .base import BaseSource


class WeiboSource(BaseSource):
    """微博热搜"""
    
    def __init__(self):
        super().__init__('weibo', '微博')
        self.api_url = "https://weibo.com/ajax/side/hotSearch"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Referer": "https://weibo.com/"
        }
        # AI 相关关键词
        self.keywords = [
            'AI', '人工智能', 'ChatGPT', 'GPT', 'Claude', '大模型',
            'OpenAI', '智能', '机器人', '算法', '科技', '互联网'
        ]
    
    def fetch(self):
        """获取微博热搜"""
        resp = requests.get(self.api_url, headers=self.headers, timeout=10)
        data = resp.json()
        
        if data.get('ok') != 1:
            return []
        
        topics = []
        for item in data.get('data', {}).get('realtime', []):
            # 过滤广告
            if item.get('ad_channel') == 1 or item.get('is_ad') == 1:
                continue
            
            title = item.get('word', '')
            
            # 只保留 AI 相关
            if any(kw in title for kw in self.keywords):
                topics.append({
                    'title': title,
                    'url': f"https://m.weibo.cn/search?containerid=100103&q=%23{title}%23",
                    'hot': item.get('num', 0),
                    'summary': ''
                })
        
        return topics[:20]


# 测试
if __name__ == '__main__':
    source = WeiboSource()
    topics = source.fetch_with_error_handling()
    print(f"✅ 微博热搜：{len(topics)} 条\n")
    for i, t in enumerate(topics[:5], 1):
        print(f"{i}. {t['title']} (热度: {t['hot']})")
