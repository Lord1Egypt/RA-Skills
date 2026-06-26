---
name: blog-watcher
description: 博客监控技能 - 监控博客和网站更新，通过RSS或网页变化检测。
metadata: {"openclaw": {"requires": {"python": ["feedparser", "beautifulsoup4"]}, "install": []}}
tags: [blog, monitor, scraping, website, tracking]
version: 1.0.0
author: laosi
source: adapted
---

# Blog Watcher - 博客监控

> 激活词: 博客监控 / 网站更新 / 追踪博客

## 安装

```bash
pip install feedparser beautifulsoup4 requests
```

## 功能

- RSS订阅监控
- 网页变化检测
- 定时检查
- 通知提醒

## Python函数

```python
import feedparser
import hashlib
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class BlogWatcher:
    def __init__(self):
        self.watch_list = []
        self.content_hashes = {}
    
    def add_blog(self, name: str, url: str, use_rss: bool = True):
        self.watch_list.append({
            'name': name,
            'url': url,
            'use_rss': use_rss,
        })
    
    def check_updates(self):
        results = []
        for blog in self.watch_list:
            if blog['use_rss']:
                result = self._check_rss(blog)
            else:
                result = self._check_webpage(blog)
            
            if result:
                results.append(result)
        
        return results
    
    def _check_rss(self, blog: dict) -> dict:
        feed = feedparser.parse(blog['url'])
        if feed.entries:
            latest = feed.entries[0]
            return {
                'name': blog['name'],
                'title': latest.title,
                'link': latest.link,
                'published': latest.get('published', 'Unknown'),
            }
        return None
    
    def _check_webpage(self, blog: dict) -> dict:
        response = requests.get(blog['url'])
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取页面标题
        title = soup.title.string if soup.title else 'No title'
        
        # 计算内容哈希
        content_hash = hashlib.md5(response.text.encode()).hexdigest()
        
        if blog['url'] in self.content_hashes:
            if self.content_hashes[blog['url']] != content_hash:
                self.content_hashes[blog['url']] = content_hash
                return {'name': blog['name'], 'title': title, 'updated': True}
        else:
            self.content_hashes[blog['url']] = content_hash
        
        return None
```

## 使用示例

```python
watcher = BlogWatcher()

# 添加博客
watcher.add_blog('技术博客', 'https://blog.example.com/feed.xml')
watcher.add_blog('AI新闻', 'https://news.example.com/rss')

# 检查更新
updates = watcher.check_updates()
for update in updates:
    print(f"[{update['name']}] {update['title']}")
```

## 输出格式

```markdown
## 博客更新

### 检测到 3 个更新

1. **技术博客**
   - 新文章: Python新特性解析
   - 链接: https://blog.example.com/post/123
   - 时间: 2026-04-28

2. **AI新闻**
   - 新文章: GPT-5发布
   - 链接: https://news.example.com/gpt5
   - 时间: 2026-04-28
```