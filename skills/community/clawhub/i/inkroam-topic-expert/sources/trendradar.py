#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多平台数据源（自建爬虫）
已验证可用：微博、知乎、GitHub
"""

import requests
from datetime import datetime
from bs4 import BeautifulSoup


class MultiPlatformSource:
    """多平台数据源"""
    
    def __init__(self):
        """初始化"""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
    
    def fetch_all(self):
        """获取所有平台热点"""
        all_topics = []
        
        # 微博
        weibo = self.fetch_weibo()
        all_topics.extend(weibo)
        
        # 知乎
        zhihu = self.fetch_zhihu()
        all_topics.extend(zhihu)
        
        # GitHub
        github = self.fetch_github()
        all_topics.extend(github)
        
        return all_topics
    
    def fetch_weibo(self):
        """获取微博热搜（AI 相关）"""
        try:
            url = "https://weibo.com/ajax/side/hotSearch"
            headers = {**self.headers, "Referer": "https://weibo.com/"}
            resp = requests.get(url, headers=headers, timeout=10)
            data = resp.json()
            
            if data.get('ok') != 1:
                return []
            
            hot_list = []
            ai_keywords = ['AI', '人工智能', 'ChatGPT', 'GPT', 'Claude', '大模型', 
                          'OpenAI', '智能', '机器人', '算法', '科技', '互联网']
            
            for item in data.get('data', {}).get('realtime', []):
                if item.get('ad_channel') == 1 or item.get('is_ad') == 1:
                    continue
                
                title = item.get('word', '')
                if any(kw in title for kw in ai_keywords):
                    hot_list.append({
                        "title": title,
                        "url": f"https://m.weibo.cn/search?containerid=100103&q=%23{title}%23",
                        "hot": item.get('num', 0),
                        "summary": "",
                        "source": "weibo",
                        "platform": "微博",
                        "fetch_time": datetime.now().isoformat()
                    })
            
            return hot_list[:20]
        except Exception as e:
            print(f"[微博] 获取失败: {e}")
            return []
    
    def fetch_zhihu(self):
        """获取知乎热榜（AI 相关）"""
        try:
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50"
            resp = requests.get(url, headers=self.headers, timeout=10)
            data = resp.json()
            
            hot_list = []
            ai_keywords = ['AI', '人工智能', 'ChatGPT', 'GPT', 'Claude', '大模型', 
                          'OpenAI', '效率', '工具', '自动化', '科技']
            
            for item in data.get('data', []):
                target = item.get('target', {})
                title = target.get('title', '')
                
                if any(kw in title for kw in ai_keywords):
                    hot_list.append({
                        "title": title,
                        "url": target.get('url', ''),
                        "summary": target.get('excerpt', ''),
                        "hot": item.get('detail_text', ''),
                        "source": "zhihu",
                        "platform": "知乎",
                        "fetch_time": datetime.now().isoformat()
                    })
            
            return hot_list[:20]
        except Exception as e:
            print(f"[知乎] 获取失败: {e}")
            return []
    
    def fetch_github(self):
        """获取 GitHub Trending（AI 相关）"""
        try:
            url = "https://github.com/trending?since=daily&spoken_language_code=en"
            resp = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            hot_list = []
            ai_keywords = ['ai', 'machine-learning', 'deep-learning', 'llm', 
                          'chatgpt', 'gpt', 'transformer', 'neural']
            
            repos = soup.select('article.Box-row')[:20]
            for repo in repos:
                title_elem = repo.select_one('h2 a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True).replace('\n', '').replace(' ', '')
                desc_elem = repo.select_one('p')
                desc = desc_elem.get_text(strip=True) if desc_elem else ''
                
                # 筛选 AI 相关项目
                if any(kw in title.lower() or kw in desc.lower() for kw in ai_keywords):
                    hot_list.append({
                        "title": title,
                        "url": f"https://github.com{title_elem.get('href', '')}",
                        "summary": desc,
                        "hot": 0,
                        "source": "github",
                        "platform": "GitHub",
                        "fetch_time": datetime.now().isoformat()
                    })
            
            return hot_list
        except Exception as e:
            print(f"[GitHub] 获取失败: {e}")
            return []


# 使用示例
if __name__ == '__main__':
    source = MultiPlatformSource()
    
    print("获取全网热点...\n")
    
    # 获取所有平台
    all_topics = source.fetch_all()
    print(f"✅ 共获取 {len(all_topics)} 条\n")
    
    # 统计各平台数量
    from collections import Counter
    platform_counts = Counter(t['source'] for t in all_topics)
    print("各平台数量：")
    for platform, count in platform_counts.most_common():
        platform_name = {'weibo': '微博', 'zhihu': '知乎', 'github': 'GitHub'}.get(platform, platform)
        print(f"  {platform_name}: {count} 条")
    
    # 显示前5条
    print("\n前5条热点：")
    for i, topic in enumerate(all_topics[:5], 1):
        print(f"{i}. [{topic['platform']}] {topic['title']}")
