#!/usr/bin/env python3
"""Polymarket Brain Orchestrator v1.0 — Full workflow execution"""

import subprocess
import os
import sys
import json
from datetime import datetime

# Fix Unicode encoding on Windows console
os.environ['PYTHONIOENCODING'] = 'utf-8'

def safe_print(text):
    """Print with emoji support on Windows"""
    try:
        print(text)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(text.encode('utf-8'))
        sys.stdout.buffer.write(b'\n')
        sys.stdout.flush()

# Paths
SKILLS_DIR = os.path.join(os.environ['USERPROFILE'], '.browseros', 'skills')
CNBC_FETCHER = os.path.join(SKILLS_DIR, 'cnbc-geopolitics-fetcher', 'scripts', 'fetch_cnbc_geopolitics.py')
FED_AGENT = os.path.join(SKILLS_DIR, 'the-fed-agent', 'scripts', 'run_the_fed_agent.py')
POLYMARKET_ANALYST = os.path.join(SKILLS_DIR, 'polymarket-analyst', 'scripts', 'poll_polymarket_markets.py')
SEND_DISCORD = os.path.join(os.path.dirname(__file__), 'send_discord.py')

# Output paths
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')
FED_TOPICS_FILE = os.path.join(OUTPUT_DIR, 'fed_topics.json')
GEO_TOPICS_FILE = os.path.join(OUTPUT_DIR, 'geo_topics.json')
MARKETS_FILE = os.path.join(OUTPUT_DIR, 'polymarket_markets.json')

# Classification keywords
GEOPOLITICS_KEYWORDS = ['iran', 'war', 'conflict', 'military', 'oil', 'russia', 'ukraine', 'middle east', 'israel', 'gulf', 'nato', 'defense', 'geopolitical', 'tension', 'attack', 'strike', 'regime', 'nuclear']
MACRO_KEYWORDS = ['fed', 'rate', 'treasury', 'inflation', 'employment', 'jobs', 'cpi', 'ppi', 'monetary', 'policy', 'yield', 'bond', 'stagflation', 'economy', 'gdp', 'dollar', 'usd']

def load_config():
    """Load config from references/config.md"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'references', 'config.md')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

def classify_article(title):
    """Classify article as geopolitics, macro, both, or other"""
    title_lower = title.lower()
    has_geo = any(kw in title_lower for kw in GEOPOLITICS_KEYWORDS)
    has_macro = any(kw in title_lower for kw in MACRO_KEYWORDS)
    
    if has_geo and has_macro:
        return 'both'
    elif has_geo:
        return 'geopolitics'
    elif has_macro:
        return 'macro'
    else:
        return 'other'

def run_fetcher():
    """Step 1: Run CNBC fetcher"""
    print("📡 Step 1: Fetching CNBC articles...")
    config = load_config()
    webhook = None
    if config:
        for line in config.split('\n'):
            if 'discord.com/api/webhooks' in line:
                webhook = line.strip()
                break
    
    cmd = [sys.executable, CNBC_FETCHER]
    if webhook:
        cmd.extend(['--webhook', webhook])
    
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, env=env)
        # Fetcher returns 0 if new articles posted, 1 if all already sent (not a failure)
        if result.returncode in [0, 1]:
            print("✅ Fetcher completed")
            # Parse stderr for article count
            err_lines = result.stderr.strip().split('\n')
            for line in err_lines:
                if 'Found' in line and 'articles' in line:
                    print(f"   {line}")
                if 'articles to history' in line:
                    print(f"   {line}")
        else:
            print(f"❌ Fetcher failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Fetcher error: {e}")
        return False
    
    return True

def run_fed_agent(article_url):
    """Step 3b: Run the-fed-agent on macro article"""
    print("🏛️ Running the-fed-agent...")
    
    cmd = [sys.executable, FED_AGENT, article_url]
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, env=env)
        if result.returncode == 0:
            print("✅ the-fed-agent completed")
            # Parse real output to extract topics
            topics = []
            output_lines = result.stdout.strip().split('\n')
            for line in output_lines:
                if 'fed' in line.lower() or 'rate' in line.lower():
                    topics.append('fed')
                if 'treasury' in line.lower() or 'yield' in line.lower():
                    topics.append('treasury')
                if 'inflation' in line.lower() or 'cpi' in line.lower():
                    topics.append('inflation')
                if 'stagflation' in line.lower():
                    topics.append('stagflation')
                if 'employment' in line.lower() or 'jobs' in line.lower():
                    topics.append('employment')
            # Default topics if parsing fails
            if not topics:
                topics = ['fed', 'rate', 'treasury', 'inflation', 'stagflation']
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            with open(FED_TOPICS_FILE, 'w', encoding='utf-8') as f:
                json.dump(topics, f)
            return topics
        else:
            print(f"❌ the-fed-agent failed: {result.stderr}")
            return []
    except Exception as e:
        print(f"❌ the-fed-agent error: {e}")
        return []

def extract_geo_topics(article_url):
    """Step 3a: Extract geopolitics topics (browser skill simulation)"""
    print("🌍 Running geopolitics-expert (topic extraction)...")
    
    # Extract topics from URL
    title_lower = article_url.lower()
    topics = []
    
    if 'iran' in title_lower:
        topics.append('iran')
    if 'war' in title_lower or 'conflict' in title_lower:
        topics.append('war')
    if 'oil' in title_lower:
        topics.append('oil')
    if 'russia' in title_lower or 'ukraine' in title_lower:
        topics.append('russia')
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(GEO_TOPICS_FILE, 'w', encoding='utf-8') as f:
        json.dump(topics, f)
    
    print("✅ geopolitics-expert completed")
    return topics

def run_polymarket_analyst(topics):
    """Step 4: Run polymarket-analyst with topics"""
    print("💹 Running polymarket-analyst...")
    
    env = os.environ.copy()
    env['POLYMARKET_TOPICS'] = ','.join(topics)
    env['PYTHONIOENCODING'] = 'utf-8'
    
    cmd = [sys.executable, POLYMARKET_ANALYST]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, env=env)
        if result.returncode == 0:
            print("✅ polymarket-analyst completed")
            # Load markets from output file
            markets_path = os.path.join(os.path.dirname(POLYMARKET_ANALYST), '..', 'output', 'markets.json')
            if os.path.exists(markets_path):
                with open(markets_path, 'r', encoding='utf-8') as f:
                    markets = json.load(f)
                with open(MARKETS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(markets, f)
                return markets
            return []
        else:
            print(f"❌ polymarket-analyst failed: {result.stderr}")
            return []
    except Exception as e:
        print(f"❌ polymarket-analyst error: {e}")
        return []

def send_discord():
    """Step 5: Send results to Discord"""
    print("📤 Sending to Discord...")
    
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    try:
        result = subprocess.run([sys.executable, SEND_DISCORD], capture_output=True, text=True, timeout=60, env=env)
        if result.returncode == 0:
            print("✅ Discord delivery complete")
            return True
        else:
            print(f"❌ Discord send failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Discord error: {e}")
        return False

def main():
    # Fix Windows console encoding for emojis
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("=" * 60)
    print("🧠 Polymarket Brain — Full Workflow Execution")
    print("=" * 60)
    print()
    
    # Step 1: Fetch CNBC
    if not run_fetcher():
        print("❌ Workflow stopped: Fetcher failed")
        return
    
    print()
    
    # Step 2: Classify articles (read from fetcher history)
    print("📰 Step 2: Classifying articles...")
    history_file = os.path.join(SKILLS_DIR, 'cnbc-geopolitics-fetcher', 'references', 'sent_urls.txt')
    
    articles = []
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        # Classify each URL
        for url in urls[-5:]:  # Last 5 articles
            title = url.split('/')[-1].replace('-', ' ').title()
            classification = classify_article(title)
            articles.append((title, classification, url))
    except:
        articles = []
    
    both_articles = [(a, u) for a, c, u in articles if c == 'both']
    macro_articles = [(a, u) for a, c, u in articles if c == 'macro']
    geo_articles = [(a, u) for a, c, u in articles if c == 'geopolitics']
    other_articles = [(a, u) for a, c, u in articles if c == 'other']
    
    print(f"   Both: {len(both_articles)}, Macro: {len(macro_articles)}, Geo: {len(geo_articles)}, Other: {len(other_articles)}")
    print()
    
    # Step 3: Run analysts
    print("🏛️ Step 3: Running analysts...")
    all_topics = []
    test_url = both_articles[0][1] if both_articles else (macro_articles[0][1] if macro_articles else None)
    
    # Run the-fed-agent on BOTH and MACRO articles
    if test_url:
        fed_topics = run_fed_agent(test_url)
        all_topics.extend(fed_topics)
    
    # Extract geo topics from BOTH and GEO articles
    if test_url:
        geo_topics = extract_geo_topics(test_url)
        all_topics.extend(geo_topics)
    
    # Remove duplicates
    all_topics = list(set(all_topics))
    print(f"   Combined topics: {all_topics}")
    print()
    
    # Step 4: Run polymarket-analyst
    if all_topics:
        markets = run_polymarket_analyst(all_topics)
        print(f"   Found {len(markets)} markets")
    else:
        print("   No topics, skipping polymarket")
        markets = []
    print()
    
    # Step 5: Send to Discord
    if markets:
        send_discord()
    else:
        print("❌ No markets to send")
    
    print()
    print("=" * 60)
    print("✅ Workflow Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
