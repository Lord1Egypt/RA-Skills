#!/usr/bin/env python3
"""
X Monitor — Result Formatter
Takes JSON search results and outputs Hootsuite-style formatted cards.
Usage: python3 scripts/format-results.py --term "polymer clay" --source google --count 10
"""

import json
import sys
import argparse
from datetime import datetime

def format_card(entry, term, source):
    """Format a single result as a Hootsuite-style card."""
    text = entry.get('text') or entry.get('description') or entry.get('title', '')
    url = entry.get('url') or entry.get('link', '')
    published = entry.get('published', '')
    
    # Truncate text to 280 chars
    preview = text[:280] + ('...' if len(text) > 280 else '')
    
    # Format engagement if available
    likes = entry.get('likes', entry.get('like_count', '—'))
    retweets = entry.get('retweets', entry.get('retweet_count', '—'))
    replies = entry.get('replies', entry.get('reply_count', '—'))
    
    # Format relative time if available
    time_ago = published if published else 'recently'
    
    card = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 {term.upper()} — {source.upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 {entry.get('author', entry.get('user', 'Anonymous'))} · {time_ago}
{'❤️ ' + str(likes) if likes != '—' else ''} {'🔁 ' + str(retweets) if retweets != '—' else ''} {'💬 ' + str(replies) if replies != '—' else ''}
\"{preview}\"
{'↗️ ' + url if url else ''}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    return card

def format_dashboard(results, term, source):
    """Format all results as a Hootsuite-style dashboard."""
    header = f"""
╔═══════════════════════════════════════════════════════════╗
║  📊 SOCIAL MONITOR — {datetime.now().strftime('%Y-%m-%d')}                          ║
║  Keyword: {term:<50} ║
║  Source: {source:<50} ║
╚═══════════════════════════════════════════════════════════╝"""
    
    cards = [format_card(r, term, source) for r in results]
    
    footer = f"""
╔═══════════════════════════════════════════════════════════╗
║  ✅ {len(results)} results found for "{term}"                ║
╚═══════════════════════════════════════════════════════════╝"""
    
    return header + '\n'.join(cards) + '\n' + footer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Format search results as Hootsuite-style cards')
    parser.add_argument('--term', required=True, help='Search term/keyword')
    parser.add_argument('--source', default='web', help='Source (google, twitter, web)')
    parser.add_argument('--count', type=int, default=10, help='Max results to show')
    parser.add_argument('--json', help='JSON input file (if no stdin)')
    args = parser.parse_args()
    
    # Read JSON from file or stdin
    if args.json:
        with open(args.json) as f:
            results = json.load(f)
    else:
        try:
            results = json.load(sys.stdin)
        except json.JSONDecodeError:
            results = []
    
    output = format_dashboard(results[:args.count], args.term, args.source)
    print(output)
