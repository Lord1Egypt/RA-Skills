#!/usr/bin/env python3
"""
Polymarket Brain Orchestrator v1.3
Main workflow: CNBC Fetch → Classify → Analyst (geo/macro) → Polymarket → Discord
"""

import subprocess
import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime, timedelta

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Paths
SKILLS_ROOT = Path(os.environ.get('SKILLS_ROOT', 'C:/Users/Legion 5i Pro/.openclaw/workspace/skills'))
POLYMARKET_BRAIN = SKILLS_ROOT / 'polymarket-brain'
CNBC_FETCHER = SKILLS_ROOT / 'cnbc-geopolitics-fetcher'
FED_AGENT = SKILLS_ROOT / 'the-fed-agent'
POLYMARKET_ANALYST = SKILLS_ROOT / 'polymarket-analyst'
GEOPOLITICS_EXPERT = SKILLS_ROOT / 'geopolitics-expert'

# Config
CONFIG_FILE = POLYMARKET_BRAIN / 'references' / 'config.md'
SENT_URLS_FILE = CNBC_FETCHER / 'references' / 'sent_urls.txt'
MEMORY_DIR = Path(os.environ.get('MEMORY_DIR', 'C:/Users/Legion 5i Pro/.openclaw/workspace/memory'))

# Classification keywords
GEOPOLITICS_KEYWORDS = ['iran', 'israel', 'russia', 'ukraine', 'china', 'middle east', 
                        'war', 'conflict', 'strike', 'missile', 'drone', 'military',
                        'hormuz', 'strait', 'oil', 'crude', 'energy', 'barrel',
                        'sanctions', 'tariff', 'invasion', 'regime']

MACRO_KEYWORDS = ['fed', 'powell', 'rate', 'interest', 'inflation', 'cpi',
                  'treasury', 'yield', 'bond', 'dollar', 'forex', 'currency',
                  'employment', 'payroll', 'unemployment', 'pmi', 'sentiment',
                  'recession', 'nber', 'gdp', 'economic']


def load_webhook():
    """Load Discord webhook from config."""
    if CONFIG_FILE.exists():
        content = CONFIG_FILE.read_text(encoding='utf-8')
        for line in content.split('\n'):
            if 'discord.com/api/webhooks' in line:
                return line.strip()
    return None


def send_discord_message(webhook, content):
    """Send message to Discord webhook."""
    import requests
    if not webhook:
        print("⚠️ No Discord webhook configured")
        return False
    
    try:
        response = requests.post(webhook, json={'content': content}, timeout=10)
        return response.status_code == 204
    except Exception as e:
        print(f"⚠️ Discord error: {e}")
        return False


def classify_article(title, text):
    """Classify article as geopolitics, macro, or both."""
    text_lower = (title + text).lower()
    
    geo_matches = sum(1 for kw in GEOPOLITICS_KEYWORDS if kw in text_lower)
    macro_matches = sum(1 for kw in MACRO_KEYWORDS if kw in text_lower)
    
    if geo_matches > 0 and macro_matches > 0:
        return 'BOTH'
    elif geo_matches > 0:
        return 'GEOPOLITICS'
    elif macro_matches > 0:
        return 'MACRO'
    return 'OTHER'


def extract_topics_from_article(title, text):
    """Extract topics for Polymarket matching."""
    topics = []
    text_lower = (title + text).lower()
    
    topic_keywords = {
        'iran': ['iran', 'iranian', 'tehran'],
        'israel': ['israel', 'israeli'],
        'russia': ['russia', 'russian', 'putin'],
        'ukraine': ['ukraine', 'ukrainian'],
        'china': ['china', 'chinese'],
        'oil': ['oil', 'crude', 'wti', 'brent', 'barrel'],
        'fed': ['fed', 'federal reserve', 'powell'],
        'rate': ['rate', 'interest', 'yield'],
        'inflation': ['inflation', 'cpi', 'pce'],
        'war': ['war', 'conflict', 'strike', 'missile'],
        'hormuz': ['hormuz', 'strait'],
    }
    
    for topic, keywords in topic_keywords.items():
        if any(kw in text_lower for kw in keywords):
            topics.append(topic)
    
    return topics


def run_cnbc_fetcher():
    """Step 1: Run CNBC geopolitics fetcher (TEST mode - no Discord posts)."""
    print("\n📰 Step 1: Fetching CNBC news (TEST mode - no Discord posts)...")
    
    script = CNBC_FETCHER / 'scripts' / 'fetch_cnbc_geopolitics.py'
    if not script.exists():
        print(f"⚠️ Script not found: {script}")
        return []
    
    # TEST mode: Don't pass webhook, so fetcher won't post to Discord
    cmd = [
        sys.executable, str(script),
        '--count', '5',
        '--verbose',
        '--test'  # TEST mode flag
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        # In TEST mode, fetcher returns 1 but still extracts articles - check stdout
        if result.returncode == 0 or 'TEST MODE: Extracted' in result.stderr:
            print("✅ CNBC fetcher completed (TEST mode)")
            return extract_fetched_articles()
        else:
            print(f"⚠️ Fetcher error: {result.stderr}")
            return []
    except Exception as e:
        print(f"⚠️ Fetcher exception: {e}")
        return []


def extract_fetched_articles():
    """Extract article data from memory files (today + yesterday)."""
    articles = []
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f"  Checking memory files: today={today}, yesterday={yesterday}")
    
    # Check today's file first, then yesterday
    for date in [today, yesterday]:
        memory_file = MEMORY_DIR / f'{date}-cnbc-geopolitics.md'
        if memory_file.exists():
            print(f"  Found memory file: {memory_file.name}")
            content = memory_file.read_text(encoding='utf-8')
            
            # Parse ## N. Title format
            title_pattern = re.compile(r'##\s+\d+\.\s+(.+?)\n', re.MULTILINE)
            # Match both **URL:** and plain URL: formats
            url_pattern = re.compile(r'(?:\*\*URL:\*\*|URL:)\s*(https://www\.cnbc\.com/[^\s]+)', re.MULTILINE)
            # Match both **Hard Facts:** and **Summary:** formats
            text_pattern = re.compile(r'(?:\*\*Hard Facts:\*\*|Summary:)\s*(.*?)(?=##|\Z)', re.MULTILINE | re.DOTALL)
            
            titles = title_pattern.findall(content)
            urls = url_pattern.findall(content)
            texts = text_pattern.findall(content)
            
            print(f"  Parsed: {len(titles)} titles, {len(urls)} URLs, {len(texts)} texts")
            
            for i, title in enumerate(titles):
                if i < len(urls):
                    articles.append({
                        'title': title.strip(),
                        'url': urls[i],
                        'text': texts[i] if i < len(texts) else '',
                        'classification': classify_article(title, texts[i] if i < len(texts) else '')
                    })
        else:
            print(f"  Memory file not found: {memory_file.name}")
    
    print(f"  Total articles extracted: {len(articles)}")
    return articles


def run_geopolitics_expert(url):
    """Step 3a: Run geopolitics-expert via browser automation (no Python script)."""
    print(f"  🌍 Geopolitics expert: {url}")
    
    # This skill is browser-based - extract topics from URL content
    # In production, this would use browser automation to run the skill
    # For now, extract topics directly
    topics = extract_topics_from_url(url)
    return {'analyst': 'geopolitics-expert', 'topics': topics, 'url': url}


def extract_topics_from_url(url):
    """Extract topics from article URL/title."""
    # Parse URL for keywords
    title = url.replace('-', ' ').replace('/', ' ')
    return extract_topics_from_article(title, title)


def run_fed_agent(url):
    """Step 3b: Run the-fed-agent via subprocess."""
    print(f"  🏦 Fed agent: {url}")
    
    script = FED_AGENT / 'scripts' / 'run_the_fed_agent.py'
    if not script.exists():
        print(f"  ⚠️ Script not found: {script}")
        return {'analyst': 'the-fed-agent', 'topics': ['fed', 'rate'], 'url': url}
    
    cmd = [sys.executable, str(script), url]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            topics = ['fed', 'rate', 'treasury', 'inflation']
            return {'analyst': 'the-fed-agent', 'topics': topics, 'url': url}
        else:
            print(f"  ⚠️ Fed agent error: {result.stderr}")
            return {'analyst': 'the-fed-agent', 'topics': ['fed', 'rate'], 'url': url}
    except Exception as e:
        print(f"  ⚠️ Fed agent exception: {e}")
        return {'analyst': 'the-fed-agent', 'topics': ['fed', 'rate'], 'url': url}


def run_polymarket_analyst(topics):
    """Step 4: Run polymarket-analyst with topics from analysts."""
    print("\n📊 Step 4: Running Polymarket analyst...")
    
    script = POLYMARKET_ANALYST / 'scripts' / 'poll_polymarket_markets.py'
    if not script.exists():
        print(f"⚠️ Script not found: {script}")
        return []
    
    # Pass topics as JSON input
    topics_json = json.dumps(topics)
    env = os.environ.copy()
    env['POLYMARKET_TOPICS'] = topics_json
    
    cmd = [sys.executable, str(script)]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, env=env)
        if result.returncode == 0:
            print("✅ Polymarket analyst completed")
            return parse_polymarket_output(result.stdout)
        else:
            print(f"⚠️ Polymarket error: {result.stderr}")
            return []
    except Exception as e:
        print(f"⚠️ Polymarket exception: {e}")
        return []


def parse_polymarket_output(output):
    """Parse Polymarket analyst output."""
    markets = []
    
    # Parse market data from output
    market_pattern = re.compile(r'(\d+)\.\s+(.+?)\n\s+Buy:\s+Yes\s+([\d.]+)%', re.MULTILINE)
    
    for match in market_pattern.finditer(output):
        markets.append({
            'number': match.group(1),
            'title': match.group(2).strip(),
            'odds': float(match.group(3)),
        })
    
    return markets


def format_market_message(market, expert_prob, recommendation):
    """Format single market message for Discord."""
    emoji = '✅' if abs(market['odds'] - expert_prob) > 20 else '⚠️' if abs(market['odds'] - expert_prob) > 10 else '⚖️'
    
    return f"""{emoji} **{market['title']}**

**Market Odds:** {market['odds']}%
**Expert Probability:** {expert_prob}%
**Recommendation:** {recommendation}

https://polymarket.com/event/{market['title'].lower().replace(' ', '-')}"""


def send_workflow_output(analysts, markets, test_mode=False):
    """Step 5: Send workflow output to Discord one-by-one."""
    if test_mode:
        print("  TEST MODE: Skipping Discord posts")
        return
    
    webhook = load_webhook()
    if not webhook:
        print("⚠️ No Discord webhook for output")
        return
    
    # Header
    analyst_line = f"Analysts: {' + '.join(analysts)}" if len(analysts) > 1 else f"Analyst: {analysts[0]}"
    header = f"""🧠 **Polymarket Brain Analysis**
📅 {datetime.now().strftime('%Y-%m-%d')}
{analyst_line}"""
    
    send_discord_message(webhook, header)
    
    # Send each market one-by-one
    for i, market in enumerate(markets[:10]):
        expert_prob = 50  # Default, would come from analyst output
        recommendation = "Hold"  # Default, would come from analyst
        
        msg = format_market_message(market, expert_prob, recommendation)
        send_discord_message(webhook, msg)


def main():
    print("🧠 Polymarket Brain Workflow v1.3")
    print("=" * 50)
    
    # Step 1: Fetch CNBC news
    articles = run_cnbc_fetcher()
    
    if not articles:
        webhook = load_webhook()
        if webhook:
            send_discord_message(webhook, "⚠️ No new CNBC articles found - all URLs already in history")
        print("⚠️ No new articles - stopping workflow")
        return
    
    print(f"✅ Found {len(articles)} new articles")
    
    # Step 2: Classify and route to analysts
    print("\n📋 Step 2: Classifying articles...")
    analysts_used = set()
    all_topics = []
    
    for article in articles:
        print(f"  📰 {article['title'][:60]}...")
        print(f"     Classification: {article['classification']}")
        
        if article['classification'] in ['GEOPOLITICS', 'BOTH']:
            result = run_geopolitics_expert(article['url'])
            analysts_used.add('geopolitics-expert')
            all_topics.extend(result['topics'])
        
        if article['classification'] in ['MACRO', 'BOTH']:
            result = run_fed_agent(article['url'])
            analysts_used.add('the-fed-agent')
            all_topics.extend(result['topics'])
    
    # Deduplicate topics
    all_topics = list(set(all_topics))
    print(f"\n🏷️ Extracted topics: {all_topics}")
    
    # Step 4: Run Polymarket analyst with topics
    markets = run_polymarket_analyst(all_topics)
    
    if not markets:
        print("⚠️ No matching Polymarket markets found")
        return
    
    print(f"✅ Found {len(markets)} matching markets")
    
    # Step 5: Send to Discord one-by-one
    print("\n💬 Step 5: Sending to Discord...")
    send_workflow_output(list(analysts_used), markets, test_mode=True)
    
    print("\n✅ Polymarket Brain workflow complete!")


if __name__ == '__main__':
    main()
