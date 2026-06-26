#!/usr/bin/env python3
"""
独行者 Daily - 变现雷达（完整版v2）
10个可靠数据源，包含华尔街见闻API
"""

import json
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime
import re
import html

# 10个数据源：包含华尔街见闻API
RSS_SOURCES = [
    # 创业/投资类
    {"name": "36氪", "url": "https://36kr.com/feed", "category": "创业投资", "keywords": ["创业", "融资", "SaaS", "变现", "副业"]},
    {"name": "虎嗅", "url": "https://www.huxiu.com/rss/0.xml", "category": "商业洞察", "keywords": ["商业模式", "创业", "变现"]},
    {"name": "创业邦", "url": "https://www.cyzone.cn/rss.xml", "category": "创业资讯", "keywords": ["创业", "融资", "一人公司"]},
    {"name": "华尔街见闻", "url": "https://api-one.wallstcn.com/apiv1/content/lives?channel=global-channel&limit=30", "category": "财经资讯", "keywords": ["财经", "投资", "融资"], "type": "api"},
    # 开发者类
    {"name": "V2EX综合", "url": "https://www.v2ex.com/index.xml", "category": "开发者社区", "keywords": ["独立开发", "SaaS", "副业"]},
    {"name": "V2EX程序员", "url": "https://www.v2ex.com/tab/programmers.xml", "category": "程序员话题", "keywords": ["独立开发", "副业"]},
    {"name": "Indie Hackers", "url": "https://feeds.transistor.fm/indie-hackers-podcast", "category": "独立开发", "keywords": ["indie", "revenue", "profit"]},
    # 技术类
    {"name": "Hacker News", "url": "https://hnrss.org/frontpage", "category": "科技前沿", "keywords": ["startup", "indie", "side project"]},
    {"name": "GitHub Trending", "url": "https://mshibanami.github.io/GitHubTrendingRSS/daily.xml", "category": "开源趋势", "keywords": ["工具", "效率"]},
    {"name": "掘金前端", "url": "https://juejin.cn/rss", "category": "技术社区", "keywords": ["开源", "副业"]}
]

def fetch_wallstreetcn():
    """获取华尔街见闻API数据"""
    try:
        url = "https://api-one.wallstcn.com/apiv1/content/lives?channel=global-channel&limit=30"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            items = []
            for item in data['data']['items'][:20]:
                items.append({
                    'id': item['id'],
                    'title': item.get('title') or item.get('content_text', '')[:150],
                    'url': item['uri'],
                    'summary': '',
                    'source': '华尔街见闻',
                    'category': '财经资讯',
                    'fetch_time': datetime.now().isoformat()
                })
            return items
    except Exception as e:
        return [{'error': str(e), 'source': '华尔街见闻'}]

def clean_text(text):
    """清理文本"""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()

def fetch_rss(url, source_name, source_category):
    """解析RSS源"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_data = response.read().decode('utf-8', errors='ignore')
            root = ET.fromstring(xml_data)
            
            items = []
            for item in root.findall('.//item')[:15]:
                title = clean_text(item.find('title').text if item.find('title') else '')
                link = clean_text(item.find('link').text if item.find('link') else '')
                desc = clean_text(item.find('description').text if item.find('description') else '')[:300]
                
                if title and link:
                    items.append({
                        'title': title,
                        'link': link,
                        'url': link,
                        'summary': desc,
                        'source': source_name,
                        'category': source_category,
                        'fetch_time': datetime.now().isoformat()
                    })
            return items
    except Exception as e:
        return [{'error': str(e), 'source': source_name}]

def calculate_relevance(news_item, keywords):
    """计算相关性"""
    title_lower = news_item.get('title', '').lower()
    score = 0
    matched = []
    for kw in keywords:
        if kw.lower() in title_lower:
            score += 10
            matched.append(kw)
    return score, matched

def aggregate_news():
    """聚合所有源"""
    all_news = []
    monetization_news = []
    
    print(f"🔍 启动数据聚合（{len(RSS_SOURCES)}个数据源）")
    
    for source in RSS_SOURCES:
        print(f"📡 正在获取 {source['name']}...")
        
        if source.get('type') == 'api':
            items = fetch_wallstreetcn()
        else:
            items = fetch_rss(source['url'], source['name'], source['category'])
        
        for item in items:
            if 'error' not in item and item.get('title'):
                score, matched = calculate_relevance(item, source['keywords'])
                item['relevance_score'] = score
                item['matched_keywords'] = matched
                
                all_news.append(item)
                
                if score >= 5:
                    item['action_value'] = f"💡 {', '.join(set(matched))}"
                    monetization_news.append(item)
    
    monetization_news.sort(key=lambda x: x['relevance_score'], reverse=True)
    all_news.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
    
    return all_news, monetization_news

if __name__ == "__main__":
    print("=" * 50)
    print("独行者 Daily - 变现雷达（v2完整版）")
    print("10个数据源：含华尔街见闻API")
    print("=" * 50)
    
    all_news, monetization_news = aggregate_news()
    
    print(f"\n📊 统计：")
    print(f"  数据源：{len(RSS_SOURCES)}个")
    print(f"  总新闻：{len(all_news)}条")
    print(f"  变现相关：{len(monetization_news)}条")
    
    if monetization_news:
        print("\n💡 变现精选：")
        for i, news in enumerate(monetization_news[:5], 1):
            print(f"{i}. [{news['source']}] {news['title'][:60]}...")
    
    print("\n✅ 完成！")