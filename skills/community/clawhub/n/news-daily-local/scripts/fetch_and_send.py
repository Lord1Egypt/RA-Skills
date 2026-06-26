#!/usr/bin/env python3
"""
新闻日报获取和发送脚本
通过 RSS 获取新闻，发送到飞书 Webhook
与原始 news-digest 项目格式完全一致

使用方式：
  python3 fetch_and_send.py                  # 直接发送到配置好的 Webhook
  python3 fetch_and_send.py --output-json    # 输出 JSON 格式
  python3 fetch_and_send.py yesterday         # 获取昨天的新闻
"""

import json
import os
import sys
import urllib.request
import urllib.error
import datetime
import ssl
import xml.etree.ElementTree as ET
import re
from html import unescape

# 创建不验证 SSL 证书的上下文
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# 配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")
CONFIG_EXAMPLE = os.path.join(SCRIPT_DIR, "config.example.json")

# 默认配置（不含敏感信息）
DEFAULT_CONFIG = {
    "date": "today",
    "categories": {
        "国内": 10,
        "国际": 10,
        "科技": 10,
        "AI": 10
    }
}

# RSS 源配置
RSS_FEEDS = {
    "国内": [
        "http://www.chinanews.com.cn/rss/scroll-news.xml",
        "https://feedx.net/rss/people.xml",
    ],
    "国际": [
        "https://cn.nytimes.com/rss/",
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://www.theguardian.com/world/rss",
    ],
    "科技": [
        "https://36kr.com/feed",
        "https://sspai.com/feed",
        "https://techcrunch.com/feed/",
        "https://www.theverge.com/rss/index.xml",
    ],
    "AI": [
        "https://www.infoq.cn/feed",
        "https://www.jiqizhixin.com/rss",
        "https://www.technologyreview.com/feed/",
        "https://venturebeat.com/category/ai/feed/",
    ]
}

# 分类 Emoji 和名称
CATEGORY_INFO = {
    "国内": ("📰", "国内新闻"),
    "国际": ("🌍", "国外新闻"),
    "科技": ("💻", "科技新闻"),
    "AI": ("🤖", "AI新闻")
}


def get_webhook_url():
    """获取 webhook URL，优先从环境变量读取"""
    # 优先从环境变量读取
    webhook = os.environ.get('NEWS_DAILY_WEBHOOK')
    if webhook:
        return webhook
    
    # 其次从 config.json 读取
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('webhook_url', '')
    
    # 如果没有 config.json，尝试 config.example.json
    if os.path.exists(CONFIG_EXAMPLE):
        with open(CONFIG_EXAMPLE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('webhook_url', '')
    return ''


def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # 如果没有 config.json，尝试 config.example.json
    if os.path.exists(CONFIG_EXAMPLE):
        with open(CONFIG_EXAMPLE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return DEFAULT_CONFIG


def clean_title(title):
    """清理标题"""
    if not title:
        return ""
    title = unescape(title)
    title = re.sub(r'<[^>]+>', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    if len(title) > 100:
        title = title[:97] + "..."
    return title


def get_link(item):
    """从 RSS item 中提取链接"""
    for tag in ['link', 'guid']:
        elem = item.find(tag)
        if elem is not None and elem.text:
            return elem.text.strip()
    return ""


def fetch_rss(url, limit=10):
    """从 RSS 源获取新闻"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/rss+xml, application/xml, text/xml, application/atom+xml'
            }
        )
        with urllib.request.urlopen(req, timeout=15, context=ssl_context) as response:
            content = response.read().decode('utf-8', errors='ignore')
            return parse_rss(content, limit)
    except Exception as e:
        print(f"获取失败: {url} - {e}")
        return []


def parse_rss(content, limit):
    """解析 RSS 内容"""
    items = []
    try:
        root = ET.fromstring(content)
        for item in root.findall('.//item')[:limit]:
            title_elem = item.find('title')
            title = clean_title(title_elem.text) if title_elem is not None else ""
            link = get_link(item)
            if title:
                items.append({"title": title, "link": link})
    except Exception:
        pass
    
    if not items:
        try:
            root = ET.fromstring(content)
            for entry in root.findall('.//entry')[:limit]:
                title_elem = entry.find('title')
                title = clean_title(title_elem.text) if title_elem is not None else ""
                link = get_link(entry)
                if title:
                    items.append({"title": title, "link": link})
        except Exception:
            pass
    
    return items


def fetch_news(categories_config):
    """获取新闻"""
    results = {}
    for category, count in categories_config.items():
        feeds = RSS_FEEDS.get(category, [])
        all_items = []
        
        for feed_url in feeds:
            items = fetch_rss(feed_url, count)
            if items:
                all_items.extend(items)
                if len(all_items) >= count:
                    break
        
        # 去重
        seen = set()
        unique_items = []
        for item in all_items:
            key = item['title'][:50].lower()
            if key not in seen:
                seen.add(key)
                unique_items.append(item)
        
        results[category] = unique_items[:count]
    
    return results


def format_as_feishu_card(news_data, date_str):
    """格式化为飞书卡片"""
    elements = []
    
    for category, items in news_data.items():
        if not items:
            continue
        
        count = len(items)
        emoji, name = CATEGORY_INFO.get(category, ("", category))
        title = f"**{emoji} {name} ({count}条)**"
        
        content = f"\n{title}\n\n"
        
        for i, item in enumerate(items[:10]):
            title_text = item['title'].replace('[', '(').replace(']', ')').replace('|', '-')
            link = item['link']
            
            if link:
                content += f"{i+1}. [{title_text}]({link})\n"
            else:
                content += f"{i+1}. {title_text}\n"
        
        elements.append({
            "tag": "markdown",
            "content": content
        })
    
    if not elements:
        elements.append({
            "tag": "markdown",
            "content": "暂无新闻数据"
        })
    
    card = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"新闻热榜 - {date_str}"
                },
                "template": "blue"
            },
            "elements": elements
        }
    }
    return card


def send_to_feishu(webhook_url, payload):
    """发送到飞书 Webhook"""
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
        result = json.loads(response.read().decode('utf-8'))
        if result.get('code') == 0:
            print("发送成功!")
            return True
        else:
            print(f"发送失败: {result.get('msg')}")
            return False


def main():
    # 检查参数
    output_json = '--output-json' in sys.argv or '-j' in sys.argv
    
    print("=" * 50)
    print("新闻日报获取和发送")
    print("=" * 50)
    
    # 加载配置
    config = load_config()
    webhook_url = get_webhook_url()
    date_str = config.get('date', 'today')
    categories = config.get('categories', DEFAULT_CONFIG['categories'])
    
    # 如果参数指定日期
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        date_str = sys.argv[1]
    
    # 格式化日期
    if date_str == "today":
        display_date = datetime.datetime.now().strftime("%Y-%m-%d")
    elif date_str == "yesterday":
        display_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        display_date = date_str
    
    print(f"\n获取日期: {display_date}")
    
    if output_json:
        print("模式: 输出 JSON")
    else:
        print(f"目标群: {webhook_url.split('/')[-1] if webhook_url else '未配置'}")
    
    print(f"类目: {', '.join(categories.keys())}")
    print(f"RSS 源:")
    for cat, feeds in RSS_FEEDS.items():
        print(f"  {cat}: {len(feeds)} 个源")
    
    # 获取数据
    print("\n正在获取新闻...")
    news_data = fetch_news(categories)
    
    for category, items in news_data.items():
        print(f"  {category}: {len(items)} 条")
    
    total = sum(len(items) for items in news_data.values())
    print(f"\n共获取 {total} 条新闻")
    
    # 输出或发送
    if output_json:
        card = format_as_feishu_card(news_data, display_date)
        print("\n" + json.dumps(card, ensure_ascii=False))
    else:
        if not webhook_url:
            print("\n错误: 未配置 webhook URL")
            print("请设置环境变量 NEWS_DAILY_WEBHOOK 或在 config.json 中配置")
            sys.exit(1)
        
        print("\n正在发送...")
        card = format_as_feishu_card(news_data, display_date)
        success = send_to_feishu(webhook_url, card)
        
        if success:
            print("\n✅ 新闻日报发送完成!")
        else:
            print("\n❌ 发送失败")
            sys.exit(1)


if __name__ == "__main__":
    main()
