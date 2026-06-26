#!/usr/bin/env python3
"""
行业资讯小哨兵 - 通过 RSS 获取昨日新闻
"""

import os
import sys
import yaml
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import urllib.request
import urllib.error

# 配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(os.path.dirname(SCRIPT_DIR), 'config.yaml')

def load_config():
    """加载配置"""
    default_config = {
        'rss_sources': [
            {'name': '36氪', 'url': 'https://36kr.com/feed'},
            {'name': '虎嗅', 'url': 'https://www.huxiu.com/rss/0.xml'},
            {'name': '少数派', 'url': 'https://sspai.com/feed'},
            {'name': '爱范儿', 'url': 'https://www.ifanr.com/feed'}
        ],
        'keywords_include': ['AI', '智能体', '大模型', 'Agent', 'OpenClaw'],
        'keywords_exclude': ['招聘', '培训', '课程', '广告', '软文'],
        'max_results_per_source': 5,
        'max_total_results': 15
    }
    
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            user_config = yaml.safe_load(f) or {}
            for key in default_config:
                if key not in user_config:
                    user_config[key] = default_config[key]
            return user_config
    
    return default_config

def get_yesterday():
    """获取昨天的日期"""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

def get_recent_24h_range():
    """获取最近24小时的时间范围"""
    now = datetime.now()
    start = now - timedelta(hours=24)
    return start, now

def fetch_rss(source):
    """抓取 RSS 源"""
    articles = []
    try:
        # 使用 urllib 请求
        req = urllib.request.Request(
            source['url'],
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8', errors='ignore')
        
        # 解析 XML
        root = ET.fromstring(content)
        
        # 查找所有 item
        for item in root.iter('item'):
            try:
                title_elem = item.find('title')
                link_elem = item.find('link')
                desc_elem = item.find('description')
                pubdate_elem = item.find('pubDate')
                if pubdate_elem is None:
                    pubdate_elem = item.find('published')
                
                if title_elem is None or link_elem is None:
                    continue
                
                title = title_elem.text or ''
                url = link_elem.text or ''
                content_text = desc_elem.text if desc_elem is not None else ''
                
                # 解析发布时间
                pub_date = None
                if pubdate_elem is not None and pubdate_elem.text:
                    try:
                        # 尝试多种日期格式
                        date_str = pubdate_elem.text.strip()
                        # 处理 36kr 格式: "2026-03-26 22:33:08  +0800"
                        date_str = re.sub(r'\s+', ' ', date_str)  # 多个空格变成一个
                        date_str = re.sub(r'\s*[+-]\d{4}\s*$', '', date_str)  # 去掉时区
                        date_str = re.sub(r'\s*GMT\s*$', '', date_str)
                        date_str = re.sub(r'\s*UTC\s*$', '', date_str)
                        
                        for fmt in [
                            '%Y-%m-%d %H:%M:%S',
                            '%a, %d %b %Y %H:%M:%S',
                            '%d %b %Y %H:%M:%S',
                            '%Y-%m-%dT%H:%M:%S',
                            '%Y-%m-%d',
                            '%a, %d %b %Y',
                            '%d %b %Y'
                        ]:
                            try:
                                pub_date = datetime.strptime(date_str.strip(), fmt)
                                break
                            except:
                                continue
                    except:
                        pass
                
                # 只保留最近24小时的文章
                if pub_date:
                    start, end = get_recent_24h_range()
                    if not (start <= pub_date <= end):
                        continue
                else:
                    # 没有日期的文章跳过
                    continue
                
                articles.append({
                    'title': title,
                    'url': url,
                    'content': content_text,
                    'date': pub_date.strftime('%Y-%m-%d') if pub_date else '未知',
                    'source': source['name']
                })
                
            except Exception as e:
                continue
        
    except Exception as e:
        print(f"   ⚠️ {source['name']} RSS 抓取失败: {e}", file=sys.stderr)
    
    return articles

def filter_articles(articles, config):
    """过滤文章"""
    keywords_include = config.get('keywords_include', [])
    keywords_exclude = config.get('keywords_exclude', [])
    
    seen_urls = set()
    filtered = []
    
    for article in articles:
        url = article.get('url', '')
        
        # 去重
        if url in seen_urls:
            continue
        seen_urls.add(url)
        
        title = article.get('title', '')
        content = article.get('content', '')
        text = title + ' ' + content
        
        # 检查包含关键词（至少匹配一个）
        has_keyword = False
        for kw in keywords_include:
            if kw.lower() in text.lower():
                has_keyword = True
                break
        
        if not has_keyword:
            continue
        
        # 检查排除词
        should_exclude = False
        for ex_word in keywords_exclude:
            if ex_word in text:
                should_exclude = True
                break
        
        if not should_exclude:
            filtered.append(article)
    
    # 如果关键词过滤后为空，返回最新的几条文章（fallback）
    if not filtered and articles:
        print("⚠️ 关键词过滤后无结果，返回最新文章", file=sys.stderr)
        # 去重后返回前5条
        seen = set()
        for article in articles:
            url = article.get('url', '')
            if url not in seen:
                seen.add(url)
                filtered.append(article)
                if len(filtered) >= 5:
                    break
    
    return filtered

def format_output(articles, date_str):
    """格式化输出 - 固定格式，强制一致性
    
    输出格式（强制）：
    ### 序号. 标题
    **日期**：YYYY-MM-DD
    **媒体**：媒体名称
    
    **摘要**：100字摘要...
    
    **链接**：URL
    ---
    """
    if not articles:
        return f"📰 行业资讯 - {date_str}\n\n暂无新资讯"
    
    output = f"📰 行业资讯 - {date_str}\n"
    output += "=" * 40 + "\n\n"
    
    for i, article in enumerate(articles, 1):
        title = article.get('title', '无标题')
        source = article.get('source', '未知')
        url = article.get('url', '')
        content = article.get('content', '')
        date = article.get('date', '未知')
        
        # 清理 HTML 和截取（固定100字）
        content = re.sub(r'<[^>]+>', '', content)
        content = re.sub(r'&[a-z]+;', '', content)
        summary = content[:100].strip() if content else '暂无摘要'
        
        # 强制固定格式
        output += f"### {i}. {title}\n"
        output += f"**日期**：{date}\n"
        output += f"**媒体**：{source}\n\n"
        output += f"**摘要**：{summary}...\n\n"
        output += f"**链接**：{url}\n"
        output += "---\n\n"
    
    output += f"共 {len(articles)} 条资讯"
    return output

def main():
    print("🔍 行业资讯小哨兵 启动...")
    print("⚠️ 通过 RSS 订阅获取媒体最新文章\n")
    
    config = load_config()
    yesterday = get_yesterday()
    
    print(f"📅 抓取日期: {yesterday}（昨天）")
    
    all_articles = []
    
    # 抓取 RSS 源
    rss_sources = config.get('rss_sources', [])
    max_per_source = config.get('max_results_per_source', 5)
    
    for source in rss_sources:
        print(f"🔎 [{source['name']}] RSS 获取中...")
        articles = fetch_rss(source)
        
        # 每个来源限制数量
        articles = articles[:max_per_source]
        
        print(f"   找到 {len(articles)} 条")
        all_articles.extend(articles)
    
    print(f"\n📊 共获取 {len(all_articles)} 条结果")
    
    # 过滤
    articles = filter_articles(all_articles, config)
    print(f"✅ 过滤后保留 {len(articles)} 条")
    
    # 限制总数
    max_total = config.get('max_total_results', 15)
    articles = articles[:max_total]
    
    # 输出
    output = format_output(articles, yesterday)
    print("\n" + output)
    
    return output

if __name__ == '__main__':
    main()
