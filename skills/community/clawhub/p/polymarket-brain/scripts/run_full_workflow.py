#!/usr/bin/env python3
"""
Polymarket Brain - Full Workflow Execution
End-to-end: Fetch → Classify → Analysts → Polymarket → Discord (one-by-one format)
"""

import subprocess
import sys
import os
import json
import requests
from datetime import datetime
from pathlib import Path

# Paths
SKILLS_DIR = Path(r"C:\Users\Legion 5i Pro\.browseros\skills")
FETCHER_DIR = SKILLS_DIR / "cnbc-geopolitics-fetcher"
FED_AGENT_DIR = SKILLS_DIR / "the-fed-agent"
POLYMARKET_DIR = SKILLS_DIR / "polymarket-analyst"
CONFIG_FILE = FETCHER_DIR / "references" / "config.md"
HISTORY_FILE = FETCHER_DIR / "references" / "sent_urls.txt"

# Load webhook from config
def load_webhook():
    if CONFIG_FILE.exists():
        content = CONFIG_FILE.read_text(encoding='utf-8')
        for line in content.split('\n'):
            if 'webhook' in line.lower():
                return line.split('=')[1].strip()
    return None

WEBHOOK_URL = load_webhook()

def send_discord_message(content):
    """Send message to Discord webhook"""
    if not WEBHOOK_URL:
        print("❌ No webhook URL configured")
        return False
    
    try:
        payload = {
            "content": content,
            "username": "Polymarket Brain"
        }
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        return response.status_code == 204
    except Exception as e:
        print(f"Discord error: {e}")
        return False

def run_fetcher():
    """Step 1: Run CNBC fetcher"""
    print("📰 Step 1: Fetching CNBC articles...")
    
    script = FETCHER_DIR / "scripts" / "fetch_cnbc_geopolitics.py"
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        env=env,
        timeout=120
    )
    
    if result.returncode != 0:
        print(f"❌ Fetcher failed: {result.stderr}")
        return None
    
    # Read history to get count
    if HISTORY_FILE.exists():
        urls = HISTORY_FILE.read_text(encoding='utf-8').strip().split('\n')
        urls = [u for u in urls if u.strip()]
        return urls
    return []

def classify_articles(urls):
    """Step 2: Classify articles"""
    print("🏷️ Step 2: Classifying articles...")
    
    geopolitics_keywords = ['iran', 'war', 'conflict', 'military', 'oil', 'russia', 'ukraine', 
                           'middle east', 'israel', 'gulf', 'nato', 'defense', 'geopolitical', 
                           'tension', 'attack', 'strike', 'regime', 'nuclear']
    macro_keywords = ['fed', 'rate', 'treasury', 'inflation', 'employment', 'jobs', 'cpi', 
                     'ppi', 'monetary', 'policy', 'yield', 'bond', 'stagflation', 'economy', 'gdp', 'dollar', 'usd']
    
    geo_urls = []
    macro_urls = []
    both_urls = []
    other_urls = []
    
    for url in urls:
        url_lower = url.lower()
        has_geo = any(kw in url_lower for kw in geopolitics_keywords)
        has_macro = any(kw in url_lower for kw in macro_keywords)
        
        if has_geo and has_macro:
            both_urls.append(url)
        elif has_geo:
            geo_urls.append(url)
        elif has_macro:
            macro_urls.append(url)
        else:
            other_urls.append(url)
    
    return {
        'geopolitics': geo_urls,
        'macro': macro_urls,
        'both': both_urls,
        'other': other_urls
    }

def run_geopolitics_expert(urls):
    """Step 3a: Geopolitics expert - extract topics from URLs"""
    print("🏛️ Step 3a: Running geopolitics-expert...")
    
    if not urls:
        return []
    
    # Extract topics from URL keywords
    topics = []
    for url in urls:
        url_lower = url.lower()
        if 'iran' in url_lower:
            topics.append('iran')
        if 'war' in url_lower or 'conflict' in url_lower:
            topics.append('war')
        if 'oil' in url_lower:
            topics.append('oil')
        if 'russia' in url_lower or 'ukraine' in url_lower:
            topics.append('russia')
        if 'israel' in url_lower:
            topics.append('israel')
    
    return list(set(topics))

def run_fed_agent(urls):
    """Step 3b: The Fed Agent - run script and extract topics"""
    print("🏛️ Step 3b: Running the-fed-agent...")
    
    if not urls:
        return []
    
    script = FED_AGENT_DIR / "scripts" / "run_the_fed_agent.py"
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        env=env,
        timeout=120
    )
    
    if result.returncode != 0:
        print(f"⚠️ Fed agent warning: {result.stderr}")
        return ['fed', 'rate', 'inflation']  # Default topics
    
    # Extract topics from output
    topics = ['fed', 'rate', 'treasury', 'inflation', 'stagflation']
    return topics

def run_polymarket_analyst(topics):
    """Step 4: Polymarket analyst - match markets to topics"""
    print("📊 Step 4: Running polymarket-analyst...")
    
    if not topics:
        topics = ['fed', 'rate', 'inflation']
    
    script = POLYMARKET_DIR / "scripts" / "poll_polymarket_markets.py"
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    env['POLYMARKET_TOPICS'] = ','.join(topics)
    
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        env=env,
        timeout=120
    )
    
    if result.returncode != 0:
        print(f"❌ Polymarket analyst failed: {result.stderr}")
        return []
    
    # Parse markets from output
    try:
        # Look for JSON output
        for line in result.stdout.split('\n'):
            if line.strip().startswith('{'):
                data = json.loads(line)
                return data.get('markets', [])
    except:
        pass
    
    return []

def format_market_message(market, index, total):
    """Format single market message for Discord"""
    name = market.get('name', 'Unknown Market')
    odds = market.get('odds', 50)
    expert_prob = market.get('expert_probability', 50)
    gap = abs(odds - expert_prob)
    
    if gap >= 20:
        emoji = "✅"
        rec = "Strong conviction"
    elif gap >= 10:
        emoji = "⚠️"
        rec = "Fair/Lean"
    else:
        emoji = "⚖️"
        rec = "Fair Value"
    
    resolution = market.get('resolution', 'Dec 31')
    
    msg = f"""📊 Market {index}/{total}
Market: {name}
Resolution: {resolution}
Market Odds: {odds}% Yes
Expert Probability: {expert_prob}%
Recommendation: {emoji} {rec} — {gap}% gap

Link: {name}
Polymarket
{name}
View real-time odds for "{name}" as of {datetime.now().strftime('%B %d, %Y')} and trade on The World's Largest Prediction Market™
{name}"""
    
    return msg

def send_header(counts, analysts):
    """Send workflow header"""
    header = f"""🧠 Polymarket Brain — Workflow Started
Date: {datetime.now().strftime('%Y-%m-%d')}
Articles Fetched: {counts['total']} articles from CNBC
Classification: {counts['geo']} geopolitics, {counts['macro']} macro, {counts['both']} mixed
Analysts: {analysts}

Running full analysis workflow..."""
    
    send_discord_message(header)

def send_markets_one_by_one(markets):
    """Send each market as separate message"""
    for i, market in enumerate(markets, 1):
        msg = format_market_message(market, i, len(markets))
        send_discord_message(msg)
        print(f"✅ Sent market {i}/{len(markets)}")

def send_footer():
    """Send workflow completion footer"""
    footer = """✅ Workflow Complete
Frameworks: Strategic Gravity, Five Pathways, Fed Policy, Inflation Transmission"""
    
    send_discord_message(footer)

def main():
    print("🚀 Starting Polymarket Brain Workflow...\n")
    
    # Step 1: Fetch
    urls = run_fetcher()
    if not urls:
        send_discord_message("⚠️ No new articles fetched. Workflow stopped.")
        print("❌ No articles found")
        return
    
    # Step 2: Classify
    classification = classify_articles(urls)
    
    # Step 3: Route to analysts
    analysts = []
    all_topics = []
    
    if classification['geopolitics'] or classification['both']:
        geo_topics = run_geopolitics_expert(classification['geopolitics'] + classification['both'])
        all_topics.extend(geo_topics)
        analysts.append('geopolitics-expert')
    
    if classification['macro'] or classification['both']:
        macro_topics = run_fed_agent(classification['macro'] + classification['both'])
        all_topics.extend(macro_topics)
        analysts.append('the-fed-agent')
    
    # Step 4: Polymarket
    markets = run_polymarket_analyst(list(set(all_topics)))
    
    if not markets:
        send_discord_message("⚠️ No markets found for extracted topics.")
        print("❌ No markets found")
        return
    
    # Step 5: Send to Discord
    counts = {
        'total': len(urls),
        'geo': len(classification['geopolitics']),
        'macro': len(classification['macro']),
        'both': len(classification['both'])
    }
    
    send_header(counts, ' + '.join(analysts))
    send_markets_one_by_one(markets)
    send_footer()
    
    print("\n✅ Workflow Complete!")
    print(f"📰 {len(urls)} articles classified")
    print(f"🏛️ {len(analysts)} analysts ran: {', '.join(analysts)}")
    print(f"📊 {len(markets)} markets sent to Discord")

if __name__ == '__main__':
    main()
