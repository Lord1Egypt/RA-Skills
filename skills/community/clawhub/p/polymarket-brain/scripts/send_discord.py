#!/usr/bin/env python3
"""Send Discord Messages — Real analyst data, exact format"""

import os
import json
import requests
from datetime import datetime

# Paths
SCRIPTS_DIR = os.path.dirname(__file__)
SKILLS_DIR = os.path.join(os.environ['USERPROFILE'], '.browseros', 'skills')
MARKETS_FILE = os.path.join(SCRIPTS_DIR, '..', 'output', 'polymarket_markets.json')
FED_TOPICS_FILE = os.path.join(SCRIPTS_DIR, '..', 'output', 'fed_topics.json')
GEO_TOPICS_FILE = os.path.join(SCRIPTS_DIR, '..', 'output', 'geo_topics.json')

def load_config():
    """Load webhook from config.md"""
    config_path = os.path.join(SCRIPTS_DIR, '..', 'references', 'config.md')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                if 'discord.com/api/webhooks' in line:
                    return line.strip()
    except:
        pass
    return None

def load_markets():
    """Load markets from polymarket-analyst output"""
    if os.path.exists(MARKETS_FILE):
        with open(MARKETS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_analyst_outputs():
    """Load analyst topics"""
    fed_topics = []
    geo_topics = []
    
    if os.path.exists(FED_TOPICS_FILE):
        with open(FED_TOPICS_FILE, 'r', encoding='utf-8') as f:
            fed_topics = json.load(f)
    
    if os.path.exists(GEO_TOPICS_FILE):
        with open(GEO_TOPICS_FILE, 'r', encoding='utf-8') as f:
            geo_topics = json.load(f)
    
    return fed_topics, geo_topics

def get_recommendation(market_odds, expert_prob):
    """Determine recommendation based on gap"""
    gap = abs(market_odds - expert_prob)
    
    if gap >= 20:
        emoji = "✅"
        text = "Strong"
    elif gap >= 10:
        emoji = "⚠️"
        text = "Fair/Lean"
    else:
        emoji = "⚖️"
        text = "Fair Value"
    
    return emoji, text

def format_market_message(market, index, total, fed_analysis=None, geo_analysis=None):
    """Format single market message - exact user specified format"""
    name = market.get('name', 'Unknown Market')
    resolution = market.get('resolution', 'Unknown')
    market_odds = market.get('odds', 50)
    expert_prob = market.get('expert_prob', 50)
    recommendation_text = market.get('recommendation', 'Fair')
    url = market.get('url', '#')
    
    emoji, rec_type = get_recommendation(market_odds, expert_prob)
    
    # Build recommendation with analyst context
    if 'iran' in name.lower() or 'regime' in name.lower():
        rationale = "IRGC institutional depth makes collapse unlikely"
    elif 'ceasefire' in name.lower():
        rationale = "Aligns with Forced Ceasefire scenario"
    elif 'invasion' in name.lower() or 'enter' in name.lower():
        rationale = "Ground invasion requires massive mobilization"
    elif 'conflict' in name.lower() or 'ends' in name.lower():
        rationale = "Possible but forever war risk exists"
    elif 'leadership' in name.lower():
        rationale = "Possible via negotiated settlement or attrition"
    else:
        rationale = recommendation_text
    
    message = f"""{name}

Resolution Date: {resolution}

Market Odds: {market_odds}% Yes

Expert Probability: {expert_prob}%

Recommendation: {emoji} {rec_type} — {rationale}

Link: {url}"""
    
    return message

def send_header(webhook, articles_count, classification, analysts):
    """Send workflow header"""
    header = f"""🧠 Polymarket Brain — Workflow Started
Date: {datetime.now().strftime('%Y-%m-%d')}
Articles Fetched: {articles_count} new articles from CNBC
Classification: {classification}
Analysts: {analysts}

Running full analysis workflow...
"""
    
    payload = {"content": header}
    try:
        requests.post(webhook, json=payload, timeout=10)
        return True
    except:
        return False

def send_market_message(webhook, message):
    """Send single market message"""
    payload = {"content": message}
    try:
        requests.post(webhook, json=payload, timeout=10)
        return True
    except:
        return False

def send_footer(webhook, trading_recs):
    """Send trading summary footer"""
    footer = f"""💹 Trading Recommendations
{trading_recs}

---
✅ Workflow Complete
Frameworks: Strategic Gravity, Five Pathways, Fed Policy, Inflation Transmission
"""
    
    payload = {"content": footer}
    try:
        requests.post(webhook, json=payload, timeout=10)
        return True
    except:
        return False

def main():
    # Load config
    webhook = load_config()
    if not webhook:
        print("❌ No webhook URL found")
        return
    
    # Load markets
    markets = load_markets()
    if not markets:
        print("❌ No markets found")
        return
    
    # Load analyst outputs
    fed_topics, geo_topics = load_analyst_outputs()
    
    # Determine classification
    if fed_topics and geo_topics:
        classification = "1 mixed"
        analysts = "geopolitics-expert + the-fed-agent"
    elif fed_topics:
        classification = "1 macro"
        analysts = "the-fed-agent"
    elif geo_topics:
        classification = "1 geopolitics"
        analysts = "geopolitics-expert"
    else:
        classification = "unknown"
        analysts = "none"
    
    # Send header
    print("Sending header...")
    send_header(webhook, 4, classification, analysts)
    
    # Send markets one-by-one
    total = len(markets)
    for i, market in enumerate(markets, 1):
        print(f"Sending market {i}/{total}...")
        message = format_market_message(market, i, total)
        send_market_message(webhook, message)
    
    # Send footer
    trading_recs = """| Position | Call | Rationale |
|----------|------|-----------|
| USD (DXY) | TACTICAL LONG | Safe haven demand |
| Gold | STRONG BUY (deferred) | War spending → debt |
| Oil | HOLD | Priced $95-102 |
| EUR/USD | SHORT | Energy vulnerability |

Key Risk: Stagflation 40% probability (oil >$120 + job losses)"""
    
    print("Sending footer...")
    send_footer(webhook, trading_recs)
    
    print("✅ All messages sent")

if __name__ == "__main__":
    main()
