#!/usr/bin/env python3
"""
独行者 Daily - 变现雷达（独立版）
直接解析公开RSS源，无需本地NewsNow部署
用户下载即能用！
"""

import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime
import re

# 公开RSS源（无需认证）
RSS_SOURCES = [
    {
        "name": "36氪",
        "url": "https://36kr.com/feed",
        "category": "创业投资",
        "priority": 1
    },
    {
        "name": "知乎热榜",
        "url": "https://www.zhihu.com/rss",
        "category": "热门讨论",
        "priority": 2
    },
    {
        "name": "V2EX",
        "url": "https://www.v2ex.com/index.xml",
        "category": "开发者",
        "priority": 1
    },
    {
        "name": "Hacker News",
        "url": "https://hnrss.org/frontpage",
        "category": "科技前沿",
        "priority": 1
    }
]

def fetch_rss(url):
    """解析RSS源"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            items = []
            for item in root.findall('.//item')[:10]:  # 取前10条
                title = item.find('title').text if item.find('title') else ''
                link = item.find('link').text if item.find('link') else ''
                desc = item.find('description').text if item.find('description') else ''
                
                # 简化描述（取前200字）
                desc_clean = re.sub(r'<[^>]+>', '', desc)[:200]
                
                items.append({
                    "title": title,
                    "link": link,
                    "summary": desc_clean,
                    "fetch_time": datetime.now().isoformat()
                })
            
            return items
    except Exception as e:
        return [{"error": str(e), "url": url}]

def aggregate_news():
    """聚合所有源"""
    all_news = []
    
    for source in RSS_SOURCES:
        print(f"📡 正在获取 {source['name']}...")
        items = fetch_rss(source['url'])
        
        for item in items:
            if 'error' not in item:
                item['source'] = source['name']
                item['category'] = source['category']
                all_news.append(item)
    
    # 按优先级排序
    all_news.sort(key=lambda x: RSS_SOURCES.index(
        next(s for s in RSS_SOURCES if s['name'] == x.get('source', ''))
    ) if x.get('source') else 999)
    
    return all_news[:20]  # 返回前20条

def filter_monetization(news_list):
    """筛选变现相关内容"""
    keywords = ['变现', '创业', '副业', '收入', '赚钱', 'SaaS', '独立开发', '一人公司', '被动收入']
    
    filtered = []
    for news in news_list:
        title_lower = news.get('title', '').lower()
        summary_lower = news.get('summary', '').lower()
        
        if any(kw in title_lower or kw in summary_lower for kw in keywords):
            news['action_value'] = "💡 变现机会"
            filtered.append(news)
    
    return filtered

if __name__ == "__main__":
    print("🔍 独行者 Daily - 变现雷达启动")
    print("📍 无需本地部署，解析公开RSS源")
    
    news = aggregate_news()
    monetization_news = filter_monetization(news)
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "total_sources": len(RSS_SOURCES),
        "total_news": len(news),
        "monetization_news": len(monetization_news),
        "news": news[:10],  # 前10条普通新闻
        "变现雷达": monetization_news[:5]  # 前5条变现相关
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\n✅ 获取 {len(news)} 条新闻，筛选出 {len(monetization_news)} 条变现机会")