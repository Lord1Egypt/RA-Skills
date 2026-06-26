#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests",
#   "beautifulsoup4",
#   "feedparser",
#   "rich"
# ]
# ///

"""
Advanced news fetcher for market intelligence.
Fetches news from multiple sources with categorization.
"""

import sys
import requests
from bs4 import BeautifulSoup
import feedparser
from rich.console import Console
from rich.table import Table
from datetime import datetime
from typing import List, Dict

console = Console()

# News source configurations
NEWS_SOURCES = {
    "yahoo_finance": {
        "name": "Yahoo Finance",
        "rss": "https://finance.yahoo.com/news/rssindex",
        "category": "general"
    },
    "moneycontrol": {
        "name": "Moneycontrol",
        "rss": "https://www.moneycontrol.com/rss/latestnews.xml",
        "category": "india"
    },
    "economic_times": {
        "name": "Economic Times",
        "rss": "https://economictimes.indiatimes.com/rssfeedstopstories.cms",
        "category": "india"
    },
    "business_standard": {
        "name": "Business Standard",
        "rss": "https://www.business-standard.com/rss/home_page_top_stories.rss",
        "category": "india"
    },
    "reuters_business": {
        "name": "Reuters Business",
        "rss": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
        "category": "global"
    }
}

GEOPOLITICAL_KEYWORDS = [
    'election', 'fed', 'federal reserve', 'rbi', 'reserve bank',
    'ecb', 'european central bank', 'boj', 'bank of japan',
    'war', 'conflict', 'sanctions', 'trade war', 'tariff',
    'treaty', 'diplomacy', 'summit', 'g7', 'g20',
    'imf', 'world bank', 'inflation', 'recession',
    'unemployment', 'gdp', 'interest rate', 'policy'
]


def fetch_rss_feed(url: str, max_items: int = 10) -> List[Dict]:
    """Fetch news from RSS feed."""
    try:
        feed = feedparser.parse(url)
        items = []
        
        for entry in feed.entries[:max_items]:
            items.append({
                "title": entry.get('title', 'No title'),
                "link": entry.get('link', ''),
                "published": entry.get('published', 'Unknown'),
                "summary": entry.get('summary', entry.get('description', ''))[:300]
            })
        
        return items
    except Exception as e:
        console.print(f"[yellow]Error fetching RSS: {e}[/yellow]")
        return []


def categorize_news(news_item: Dict) -> str:
    """Categorize news based on content."""
    text = (news_item.get('title', '') + ' ' + news_item.get('summary', '')).lower()
    
    if any(kw in text for kw in GEOPOLITICAL_KEYWORDS):
        return "geopolitical"
    elif any(kw in text for kw in ['nifty', 'sensex', 'nse', 'bse', 'india', 'rupee', 'inr']):
        return "india"
    elif any(kw in text for kw in ['stock', 'market', 'trade', 'investor']):
        return "markets"
    elif any(kw in text for kw in ['tech', 'technology', 'ai', 'crypto', 'bitcoin']):
        return "technology"
    else:
        return "general"


def fetch_all_news(category_filter: str = None, max_per_source: int = 5) -> List[Dict]:
    """Fetch news from all sources."""
    all_news = []
    
    for source_id, config in NEWS_SOURCES.items():
        if category_filter and config['category'] != category_filter:
            continue
        
        console.print(f"[cyan]Fetching from {config['name']}...[/cyan]")
        items = fetch_rss_feed(config['rss'], max_per_source)
        
        for item in items:
            item['source'] = config['name']
            item['source_category'] = config['category']
            item['content_category'] = categorize_news(item)
            all_news.append(item)
    
    return all_news


def display_news_table(news_items: List[Dict]):
    """Display news in a formatted table."""
    table = Table(title="Market News", show_header=True, header_style="bold magenta")
    table.add_column("Source", style="cyan", width=20)
    table.add_column("Category", style="yellow", width=15)
    table.add_column("Title", style="white", width=60)
    table.add_column("Published", style="dim", width=20)
    
    for item in news_items:
        table.add_row(
            item['source'],
            item['content_category'],
            item['title'][:60] + "..." if len(item['title']) > 60 else item['title'],
            item['published'][:20] if len(item['published']) > 20 else item['published']
        )
    
    console.print(table)


def cmd_fetch(category: str = None, limit: int = 20):
    """Fetch and display news."""
    console.print("\n[bold cyan]📰 Fetching Market News[/bold cyan]\n")
    
    news = fetch_all_news(category_filter=category, max_per_source=10)
    
    # Sort by timestamp if possible
    news = news[:limit]
    
    display_news_table(news)
    
    console.print(f"\n[green]Fetched {len(news)} news items[/green]")
    
    # Display detailed view
    console.print("\n[bold]Detailed News:[/bold]\n")
    for i, item in enumerate(news[:10], 1):
        console.print(f"[bold]{i}. {item['title']}[/bold]")
        console.print(f"   Source: {item['source']} | Category: {item['content_category']}")
        console.print(f"   {item['summary'][:200]}...")
        console.print(f"   [blue underline]{item['link']}[/blue underline]\n")


def cmd_geopolitical(limit: int = 15):
    """Fetch geopolitical news."""
    console.print("\n[bold cyan]🌐 Geopolitical News Affecting Markets[/bold cyan]\n")
    
    all_news = fetch_all_news(max_per_source=10)
    geo_news = [n for n in all_news if n['content_category'] == 'geopolitical']
    
    geo_news = geo_news[:limit]
    
    if not geo_news:
        console.print("[yellow]No geopolitical news found at this time[/yellow]")
        return
    
    for i, item in enumerate(geo_news, 1):
        console.print(f"[bold]{i}. {item['title']}[/bold]")
        console.print(f"   Source: {item['source']} | {item['published']}")
        console.print(f"   {item['summary'][:250]}...")
        console.print(f"   [blue underline]{item['link']}[/blue underline]\n")


def main():
    if len(sys.argv) < 2:
        console.print("[red]Usage: news_fetcher.py <command> [options][/red]")
        console.print("\nCommands:")
        console.print("  fetch [--category india|global] [--limit N] - Fetch all news")
        console.print("  geopolitical [--limit N]                    - Fetch geopolitical news")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    try:
        if command == "fetch":
            category = None
            limit = 20
            
            if "--category" in sys.argv:
                cat_idx = sys.argv.index("--category") + 1
                if cat_idx < len(sys.argv):
                    category = sys.argv[cat_idx]
            
            if "--limit" in sys.argv:
                limit_idx = sys.argv.index("--limit") + 1
                if limit_idx < len(sys.argv):
                    limit = int(sys.argv[limit_idx])
            
            cmd_fetch(category, limit)
        
        elif command == "geopolitical":
            limit = 15
            if "--limit" in sys.argv:
                limit_idx = sys.argv.index("--limit") + 1
                if limit_idx < len(sys.argv):
                    limit = int(sys.argv[limit_idx])
            cmd_geopolitical(limit)
        
        else:
            console.print(f"[red]Unknown command: {command}[/red]")
            sys.exit(1)
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
