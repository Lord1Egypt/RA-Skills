#!/usr/bin/env python3
"""
Market Oracle — News Fetcher
Fetches financial news from Google News RSS and Yahoo Finance RSS.
No API key required.
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
from html.parser import HTMLParser


class HTMLTextExtractor(HTMLParser):
    """Strip HTML tags from text."""
    def __init__(self):
        super().__init__()
        self._result = []

    def handle_data(self, data):
        self._result.append(data)

    def get_text(self):
        return ''.join(self._result).strip()


def strip_html(html_text):
    extractor = HTMLTextExtractor()
    extractor.feed(html_text or "")
    return extractor.get_text()


def fetch_url(url, timeout=15):
    """Fetch URL content with error handling."""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/131.0.0.0 Safari/537.36'
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"[WARN] Failed to fetch {url}: {e}", file=sys.stderr)
        return None


def fetch_google_news(query, lang='zh', limit=10):
    """Fetch news from Google News RSS."""
    hl = 'zh-CN' if lang == 'zh' else 'en-US'
    gl = 'CN' if lang == 'zh' else 'US'
    ceid = f'{gl}:{hl[:2]}'
    encoded_query = urllib.parse.quote(query)
    url = (f'https://news.google.com/rss/search?q={encoded_query}'
           f'&hl={hl}&gl={gl}&ceid={ceid}')

    content = fetch_url(url)
    if not content:
        return []

    articles = []
    try:
        root = ET.fromstring(content)
        for item in root.findall('.//item')[:limit]:
            title = item.findtext('title', '')
            link = item.findtext('link', '')
            pub_date = item.findtext('pubDate', '')
            source = item.findtext('source', '')
            description = strip_html(item.findtext('description', ''))

            articles.append({
                'title': title,
                'url': link,
                'source': source,
                'published': pub_date,
                'summary': description[:300] if description else '',
                'provider': 'google_news'
            })
    except ET.ParseError as e:
        print(f"[WARN] XML parse error for Google News: {e}", file=sys.stderr)

    return articles


def fetch_yahoo_finance_news(query, limit=10):
    """Fetch news from Yahoo Finance RSS."""
    encoded_query = urllib.parse.quote(query)
    url = f'https://feeds.finance.yahoo.com/rss/2.0/headline?s={encoded_query}&region=US&lang=en-US'

    content = fetch_url(url)
    if not content:
        return []

    articles = []
    try:
        root = ET.fromstring(content)
        for item in root.findall('.//item')[:limit]:
            title = item.findtext('title', '')
            link = item.findtext('link', '')
            pub_date = item.findtext('pubDate', '')
            description = strip_html(item.findtext('description', ''))

            articles.append({
                'title': title,
                'url': link,
                'source': 'Yahoo Finance',
                'published': pub_date,
                'summary': description[:300] if description else '',
                'provider': 'yahoo_finance'
            })
    except ET.ParseError as e:
        print(f"[WARN] XML parse error for Yahoo Finance: {e}", file=sys.stderr)

    return articles


def fetch_finviz_news(limit=10):
    """Fetch top financial news headlines from Finviz RSS."""
    url = 'https://finviz.com/news_export.ashx?v=3'
    content = fetch_url(url)
    if not content:
        return []

    articles = []
    try:
        root = ET.fromstring(content)
        for item in root.findall('.//item')[:limit]:
            title = item.findtext('title', '')
            link = item.findtext('link', '')
            pub_date = item.findtext('pubDate', '')

            articles.append({
                'title': title,
                'url': link,
                'source': 'Finviz',
                'published': pub_date,
                'summary': '',
                'provider': 'finviz'
            })
    except ET.ParseError as e:
        print(f"[WARN] XML parse error for Finviz: {e}", file=sys.stderr)

    return articles


# Financial keyword mapping for better search
KEYWORD_MAP = {
    '黄金': 'gold',
    '白银': 'silver',
    '原油': 'crude oil',
    '石油': 'oil',
    '比特币': 'bitcoin',
    '以太坊': 'ethereum',
    '加密货币': 'cryptocurrency',
    '数字货币': 'cryptocurrency',
    '股票': 'stock market',
    '美联储': 'federal reserve',
    '降息': 'rate cut',
    '加息': 'rate hike',
    'OPEC': 'OPEC',
    '通胀': 'inflation',
    '大盘': 'S&P 500',
}


def expand_query(query):
    """Expand Chinese financial keywords to English equivalents for better RSS results."""
    en_terms = []
    for zh, en in KEYWORD_MAP.items():
        if zh in query:
            en_terms.append(en)
    if en_terms:
        return query + ' ' + ' OR '.join(en_terms)
    return query


def fetch_global_headlines(limit=10):
    """Fetch current top global financial headlines from multiple sources.

    This fetches GENERAL top headlines, not filtered by any specific query.
    Used to provide global context alongside a user's specific event.
    """
    all_headlines = []

    # 1. Google News top financial headlines (English)
    url_en = ('https://news.google.com/rss/search?q=financial+markets+OR+stock+OR+economy'
              '&hl=en-US&gl=US&ceid=US:en')
    content = fetch_url(url_en)
    if content:
        try:
            root = ET.fromstring(content)
            for item in root.findall('.//item')[:limit]:
                title = item.findtext('title', '')
                link = item.findtext('link', '')
                pub_date = item.findtext('pubDate', '')
                source = item.findtext('source', '')
                description = strip_html(item.findtext('description', ''))
                all_headlines.append({
                    'title': title, 'url': link, 'source': source,
                    'published': pub_date,
                    'summary': description[:300] if description else '',
                    'provider': 'google_news_global',
                })
        except ET.ParseError:
            pass

    # 2. Google News top financial headlines (Chinese)
    url_zh = ('https://news.google.com/rss/search?q=金融+OR+股市+OR+经济+OR+央行'
              '&hl=zh-CN&gl=CN&ceid=CN:zh')
    content = fetch_url(url_zh)
    if content:
        try:
            root = ET.fromstring(content)
            for item in root.findall('.//item')[:limit // 2]:
                title = item.findtext('title', '')
                link = item.findtext('link', '')
                pub_date = item.findtext('pubDate', '')
                source = item.findtext('source', '')
                description = strip_html(item.findtext('description', ''))
                all_headlines.append({
                    'title': title, 'url': link, 'source': source,
                    'published': pub_date,
                    'summary': description[:300] if description else '',
                    'provider': 'google_news_global_zh',
                })
        except ET.ParseError:
            pass

    # 3. Finviz top headlines (always global financial)
    finviz_articles = fetch_finviz_news(limit=limit)
    all_headlines.extend(finviz_articles)

    # Deduplicate
    seen = set()
    unique = []
    for a in all_headlines:
        key = a['title'].strip().lower()
        if key and key not in seen:
            seen.add(key)
            unique.append(a)

    unique.sort(key=lambda x: x.get('published', ''), reverse=True)
    return unique[:limit * 2]


def main():
    parser = argparse.ArgumentParser(description='Fetch financial news from multiple sources')
    parser.add_argument('--query', '-q', help='Search keywords')
    parser.add_argument('--lang', '-l', default='zh', choices=['zh', 'en'], help='Language (default: zh)')
    parser.add_argument('--limit', '-n', type=int, default=10, help='Max articles per source (default: 10)')
    parser.add_argument('--source', '-s', default='all', choices=['google', 'yahoo', 'finviz', 'all'],
                        help='News source (default: all)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--global-headlines', action='store_true',
                        help='Fetch global top headlines (no query needed)')

    args = parser.parse_args()

    # ── Global headlines mode ──
    if args.global_headlines:
        headlines = fetch_global_headlines(limit=args.limit)
        if args.json:
            print(json.dumps({
                'query': '__global_headlines__',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'count': len(headlines),
                'articles': headlines
            }, ensure_ascii=False, indent=2))
        else:
            print(f"🌍 全球实时重大新闻头条")
            print(f"⏰ 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📄 共抓取 {len(headlines)} 条头条\n")
            for i, a in enumerate(headlines, 1):
                print(f"  [{i}] {a['title']}")
                print(f"      来源: {a['source']} | {a['published']}")
        return

    # ── Normal query mode ──
    if not args.query:
        print("ERROR: 请提供 --query 或 --global-headlines 参数", file=sys.stderr)
        sys.exit(1)

    all_articles = []
    expanded_query = expand_query(args.query)

    if args.source in ('google', 'all'):
        articles = fetch_google_news(args.query, lang=args.lang, limit=args.limit)
        all_articles.extend(articles)
        # Also search with expanded English terms
        if expanded_query != args.query:
            en_articles = fetch_google_news(expanded_query, lang='en', limit=args.limit // 2)
            all_articles.extend(en_articles)

    if args.source in ('yahoo', 'all'):
        # Yahoo Finance RSS works best with ticker symbols
        yahoo_query = expanded_query if expanded_query != args.query else args.query
        articles = fetch_yahoo_finance_news(yahoo_query, limit=args.limit)
        all_articles.extend(articles)

    if args.source in ('finviz', 'all'):
        articles = fetch_finviz_news(limit=args.limit)
        all_articles.extend(articles)

    # Deduplicate by title
    seen_titles = set()
    unique_articles = []
    for article in all_articles:
        title_key = article['title'].strip().lower()
        if title_key and title_key not in seen_titles:
            seen_titles.add(title_key)
            unique_articles.append(article)

    # Sort by published date (most recent first)
    unique_articles.sort(key=lambda x: x.get('published', ''), reverse=True)

    # Limit total output
    unique_articles = unique_articles[:args.limit * 2]

    if args.json:
        print(json.dumps({
            'query': args.query,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'count': len(unique_articles),
            'articles': unique_articles
        }, ensure_ascii=False, indent=2))
    else:
        print(f"📰 新闻搜索结果: \"{args.query}\"")
        print(f"⏰ 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📄 共找到 {len(unique_articles)} 条相关新闻\n")
        print("=" * 70)

        for i, article in enumerate(unique_articles, 1):
            print(f"\n[{i}] {article['title']}")
            print(f"    来源: {article['source']} | {article['published']}")
            if article['summary']:
                print(f"    摘要: {article['summary'][:150]}...")
            print(f"    链接: {article['url']}")
            print("-" * 70)

    if not unique_articles:
        print("\n⚠️  未找到相关新闻，请尝试调整关键词。", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
