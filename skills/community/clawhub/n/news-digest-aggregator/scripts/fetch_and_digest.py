#!/usr/bin/env python3
"""
News Digest Aggregator
Fetches RSS feeds, summarizes articles using LLM, and sends to messaging channels.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import List, Dict, Any

# RSS parsing
try:
    import feedparser
except ImportError:
    print("Installing required package: feedparser")
    os.system(f"{sys.executable} -m pip install feedparser")
    import feedparser

# HTTP requests
try:
    import requests
except ImportError:
    print("Installing required package: requests")
    os.system(f"{sys.executable} -m pip install requests")
    import requests


class NewsDigestAggregator:
    def __init__(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.articles = []
        
    def fetch_feeds(self, max_per_source: int = 5) -> List[Dict[str, Any]]:
        """Fetch articles from all configured RSS sources."""
        all_articles = []
        
        for source in self.config.get('sources', []):
            try:
                print(f"Fetching: {source['name']}...")
                feed = feedparser.parse(source['url'])
                
                for entry in feed.entries[:max_per_source]:
                    article = {
                        'title': entry.get('title', 'No title'),
                        'link': entry.get('link', ''),
                        'summary': entry.get('summary', '')[:300],
                        'published': entry.get('published', ''),
                        'source': source['name'],
                        'category': source.get('category', 'general')
                    }
                    all_articles.append(article)
                    
            except Exception as e:
                print(f"Error fetching {source['name']}: {e}")
                
        self.articles = all_articles
        return all_articles
    
    def generate_digest(self) -> str:
        """Generate formatted digest text."""
        if not self.articles:
            return "📰 No articles found today."
        
        # Group by category
        categories = {}
        for article in self.articles:
            cat = article.get('category', 'general')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(article)
        
        # Build digest
        lines = [
            f"📰 **Daily News Digest** - {datetime.now().strftime('%Y-%m-%d')}",
            f"📊 {len(self.articles)} articles from {len(self.config.get('sources', []))} sources",
            "",
        ]
        
        for category, articles in categories.items():
            lines.append(f"\n🏷️ **{category.upper()}**")
            for article in articles:
                lines.append(f"• [{article['title']}]({article['link']})")
                if article['summary']:
                    summary = article['summary'][:150] + "..." if len(article['summary']) > 150 else article['summary']
                    lines.append(f"  _{summary}_")
            lines.append("")
        
        return "\n".join(lines)
    
    def send_to_discord(self, webhook_url: str, content: str):
        """Send digest to Discord via webhook."""
        chunks = [content[i:i+1900] for i in range(0, len(content), 1900)]
        
        for chunk in chunks:
            payload = {
                "content": chunk,
                "username": "News Digest"
            }
            response = requests.post(webhook_url, json=payload)
            if response.status_code != 204:
                print(f"Discord error: {response.status_code} - {response.text}")
            else:
                print("✓ Sent to Discord")
    
    def send_to_slack(self, webhook_url: str, content: str):
        """Send digest to Slack via webhook."""
        payload = {
            "text": content,
            "username": "News Digest"
        }
        response = requests.post(webhook_url, json=payload)
        if response.status_code != 200:
            print(f"Slack error: {response.status_code} - {response.text}")
        else:
            print("✓ Sent to Slack")
    
    def send_to_feishu(self, webhook_url: str, content: str):
        """Send digest to Feishu via webhook."""
        payload = {
            "msg_type": "text",
            "content": {
                "text": content.replace('**', '').replace('_', '')  # Remove markdown for plain text
            }
        }
        response = requests.post(webhook_url, json=payload)
        if response.status_code != 200:
            print(f"Feishu error: {response.status_code} - {response.text}")
        else:
            print("✓ Sent to Feishu")


def main():
    parser = argparse.ArgumentParser(description='News Digest Aggregator')
    parser.add_argument('--config', default='references/sources.json', help='Path to sources config')
    parser.add_argument('--channel', choices=['discord', 'slack', 'feishu'], required=True, help='Target channel')
    parser.add_argument('--max-articles', type=int, default=5, help='Max articles per source')
    args = parser.parse_args()
    
    # Initialize aggregator
    aggregator = NewsDigestAggregator(args.config)
    
    # Fetch articles
    print("Fetching news feeds...")
    aggregator.fetch_feeds(max_per_source=args.max_articles)
    
    # Generate digest
    digest = aggregator.generate_digest()
    print("\n" + "="*50)
    print(digest)
    print("="*50)
    
    # Send to channel
    if args.channel == 'discord':
        webhook = os.getenv('DISCORD_WEBHOOK_URL')
        if not webhook:
            print("Error: DISCORD_WEBHOOK_URL not set")
            sys.exit(1)
        aggregator.send_to_discord(webhook, digest)
        
    elif args.channel == 'slack':
        webhook = os.getenv('SLACK_WEBHOOK_URL')
        if not webhook:
            print("Error: SLACK_WEBHOOK_URL not set")
            sys.exit(1)
        aggregator.send_to_slack(webhook, digest)
        
    elif args.channel == 'feishu':
        webhook = os.getenv('FEISHU_WEBHOOK_URL')
        if not webhook:
            print("Error: FEISHU_WEBHOOK_URL not set")
            sys.exit(1)
        aggregator.send_to_feishu(webhook, digest)


if __name__ == '__main__':
    main()
