---
name: rss-monitor
description: RSS监控技能 - 监控RSS/Atom订阅源，检测更新，获取新内容。
metadata: {"openclaw": {"requires": {"python": ["feedparser"]}, "install": []}}
tags: [rss, atom, feed, monitor, subscription]
version: 1.0.0
author: laosi
source: adapted
---

# RSS Monitor - RSS监控

> 激活词: RSS监控 / 订阅更新 / Feed监控

## 安装

```bash
pip install feedparser
```

## 功能

- 解析RSS/Atom feeds
- 检测新内容
- 过滤分类
- 历史记录

## Python函数

```python
import feedparser
import time
from datetime import datetime

class RSSMonitor:
    def __init__(self):
        self.feeds = {}
        self.last_check = {}
    
    def add_feed(self, name: str, url: str):
        self.feeds[name] = url
    
    def check_updates(self) -> list:
        updates = []
        for name, url in self.feeds.items():
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:5]:
                entry_time = datetime(*entry.published_parsed[:6])
                
                if name not in self.last_check or entry_time > self.last_check[name]:
                    updates.append({
                        'feed': name,
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.get('published', 'Unknown'),
                    })
            
            self.last_check[name] = datetime.now()
        
        return updates
    
    def get_entries(self, url: str, limit: int = 10):
        feed = feedparser.parse(url)
        return [{
            'title': e.title,
            'link': e.link,
            'summary': e.get('summary', '')[:200],
        } for e in feed.entries[:limit]]
```

## 命令行

```bash
# 解析RSS
curl -s "https://example.com/feed.xml" | grep -o '<title>.*</title>'
```

## 使用场景

1. 监控技术博客更新
2. 跟踪新闻源
3. 关注播客��集
4. 监控社交媒体动态