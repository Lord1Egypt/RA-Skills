#!/usr/bin/env python3
"""
独行者 Daily - 变现雷达（完整版）
真正提供9+可靠数据源，聚焦一人公司变现内容
"""

import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime
import re
import html

# 扩展数据源：聚焦一人公司、创业、变现
RSS_SOURCES = [
    # 创业/投资类
    {
        "name": "36氪",
        "url": "https://36kr.com/feed",
        "category": "创业投资",
        "keywords": ["创业", "融资", "投资", "SaaS", "变现"]
    },
    {
        "name": "虎嗅",
        "url": "https://www.huxiu.com/rss/0.xml",
        "category": "商业洞察",
        "keywords": ["商业模式", "创业", "变现"]
    },
    {
        "name": "创业邦",
        "url": "https://www.cyzone.cn/rss.xml",
        "category": "创业资讯",
        "keywords": ["创业", "创业者", "融资"]
    },
    # 开发者/独立开发类
    {
        "name": "V2EX综合",
        "url": "https://www.v2ex.com/index.xml",
        "category": "开发者社区",
        "keywords": ["独立开发", "SaaS", "副业", "赚钱"]
    },
    {
        "name": "V2EX程序员",
        "url": "https://www.v2ex.com/tab/programmers.xml",
        "category": "程序员话题",
        "keywords": ["独立开发", "副业", "开源"]
    },
    {
        "name": "Indie Hackers",
        "url": "https://feeds.transistor.fm/indie-hackers-podcast",
        "category": "独立开发",
        "keywords": ["indie", "maker", "revenue", "profit"]
    },
    # 技术资讯类
    {
        "name": "Hacker News",
        "url": "https://hnrss.org/frontpage",
        "category": "科技前沿",
        "keywords": ["startup", "indie", "side project"]
    },
    {
        "name": "GitHub Trending",
        "url": "https://mshibanami.github.io/GitHubTrendingRSS/daily.xml",
        "category": "开源趋势",
        "keywords": ["工具", "效率", "开源"]
    },
    {
        "name": "掘金前端",
        "url": "https://juejin.cn/rss",
        "category": "技术社区",
        "keywords": ["开源", "工具", "副业"]
    }
]

def clean_text(text):
    """清理HTML标签和特殊字符"""
    if not text:
        return ""
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    # 解码HTML实体
    text = html.unescape(text)
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def fetch_rss(url, source_name):
    """解析RSS源（增强版）"""
    try:
        req = urllib.request.Request(
            url, 
            headers={
                'User-Agent': 'Mozilla/5.0 (compatible; IndieDaily/1.0)',
                'Accept': 'application/rss+xml, application/xml, text/xml'
            }
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_data = response.read().decode('utf-8', errors='ignore')
            
            # 尝试解析XML
            try:
                root = ET.fromstring(xml_data)
            except ET.ParseError:
                # 尝试修复常见XML问题
                xml_data = xml_data.replace('&', '&amp;')
                root = ET.fromstring(xml_data)
            
            items = []
            
            # RSS 2.0格式
            for item in root.findall('.//item')[:15]:
                title_elem = item.find('title')
                link_elem = item.find('link')
                desc_elem = item.find('description') or item.find('summary')
                
                title = clean_text(title_elem.text if title_elem is not None else '')
                link = clean_text(link_elem.text if link_elem is not None else '')
                desc = clean_text(desc_elem.text if desc_elem is not None else '')
                
                if title and link:  # 只保留有效数据
                    items.append({
                        "title": title[:150],
                        "link": link,
                        "summary": desc[:300],
                        "source": source_name,
                        "fetch_time": datetime.now().isoformat()
                    })
            
            # Atom格式（备用）
            if not items:
                for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry')[:15]:
                    title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                    link_elem = entry.find('{http://www.w3.org/2005/Atom}link')
                    
                    title = clean_text(title_elem.text if title_elem is not None else '')
                    link = link_elem.get('href') if link_elem is not None else ''
                    
                    if title and link:
                        items.append({
                            "title": title[:150],
                            "link": link,
                            "summary": "",
                            "source": source_name,
                            "fetch_time": datetime.now().isoformat()
                        })
            
            return items
            
    except Exception as e:
        return [{
            "error": str(e),
            "url": url,
            "source": source_name
        }]

def calculate_relevance(news_item, keywords):
    """计算变现相关性评分"""
    title_lower = news_item.get('title', '').lower()
    summary_lower = news_item.get('summary', '').lower()
    
    score = 0
    matched_keywords = []
    
    for kw in keywords:
        if kw.lower() in title_lower:
            score += 10  # 标题匹配权重高
            matched_keywords.append(kw)
        if kw.lower() in summary_lower:
            score += 5   # 内容匹配
            matched_keywords.append(kw)
    
    return score, matched_keywords

def aggregate_news():
    """聚合所有源并筛选变现相关内容"""
    all_news = []
    monetization_news = []
    
    print(f"🔍 启动数据聚合（{len(RSS_SOURCES)}个数据源）")
    
    for source in RSS_SOURCES:
        print(f"📡 正在获取 {source['name']}...")
        items = fetch_rss(source['url'], source['name'])
        
        for item in items:
            if 'error' not in item and item.get('title'):
                item['category'] = source['category']
                
                # 计算变现相关性
                score, matched_kw = calculate_relevance(item, source['keywords'])
                item['relevance_score'] = score
                item['matched_keywords'] = matched_kw
                
                all_news.append(item)
                
                # 筛选高相关性内容（score >= 5）
                if score >= 5:
                    item['action_value'] = f"💡 变现相关：{', '.join(set(matched_kw))}"
                    monetization_news.append(item)
    
    # 按相关性排序
    monetization_news.sort(key=lambda x: x['relevance_score'], reverse=True)
    all_news.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
    
    return all_news, monetization_news

if __name__ == "__main__":
    print("=" * 50)
    print("独行者 Daily - 变现雷达（完整版）")
    print("真正提供9+可靠数据源，聚焦一人公司变现")
    print("=" * 50)
    
    all_news, monetization_news = aggregate_news()
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "sources_count": len(RSS_SOURCES),
        "sources_list": [s['name'] for s in RSS_SOURCES],
        "total_news": len(all_news),
        "valid_news": len([n for n in all_news if n.get('title')]),
        "monetization_count": len(monetization_news),
        "monetization_news": monetization_news[:10],
        "all_news": all_news[:20]
    }
    
    print("\n" + "=" * 50)
    print(f"📊 数据统计：")
    print(f"  数据源：{len(RSS_SOURCES)}个")
    print(f"  总新闻：{len(all_news)}条")
    print(f"  有效新闻：{len([n for n in all_news if n.get('title')])}条")
    print(f"  变现相关：{len(monetization_news)}条")
    print("=" * 50)
    
    if monetization_news:
        print("\n💡 变现雷达精选：")
        for i, news in enumerate(monetization_news[:5], 1):
            print(f"{i}. [{news['source']}] {news['title'][:60]}...")
            print(f"   关键词：{news.get('matched_keywords', [])}")
    
    # 输出JSON（可选）
    if '--json' in sys.argv if sys.argv else False:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n✅ 数据聚合完成！")