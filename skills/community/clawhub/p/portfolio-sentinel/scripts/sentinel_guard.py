#!/usr/bin/env python3
"""
Portfolio Sentinel - Buffett Guardian Version
Dynamic Tier Management: Holdings, Top Watchers, Waitlist
"""
import json
import subprocess
import os
import shlex
import requests
import yfinance as yf
from datetime import datetime, time
import pytz
import sys

# --- Configuration ---
TELEGRAM_CHAT_ID = "8441114571"
# PRIMARY DATA SOURCE: The workspace investment intelligence file
INTELLIGENCE_FILE = "/root/.openclaw/workspace/investment_intelligence.json"
# LOCAL CONFIG: For metadata and tier overrides (e.g., top_watchers)
SKILL_CONFIG = "/root/.openclaw/skills/portfolio-sentinel/config.json"

BJS = pytz.timezone('Asia/Shanghai')
EST = pytz.timezone('America/New_York')

def load_intelligence():
    """Load primary tickers from the workspace intelligence file."""
    try:
        with open(INTELLIGENCE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"holdings": [], "watchlist": []}

def load_skill_config():
    """Load internal skill-specific overrides (like top_watchers)."""
    try:
        with open(SKILL_CONFIG, 'r') as f:
            return json.load(f)
    except:
        return {"tiers": {"top_watchers": []}}

def get_market_data(tickers):
    data = {}
    for ticker in tickers:
        try:
            # Handle HK tickers for yfinance
            yf_ticker = ticker
            if ".HK" in ticker:
                yf_ticker = ticker.split(".")[0].zfill(5) + ".HK"
            
            t = yf.Ticker(yf_ticker)
            info = t.info
            price = info.get('regularMarketPrice') or info.get('currentPrice')
            prev = info.get('regularMarketPreviousClose')
            change = ((price - prev) / prev * 100) if price and prev else 0
            data[ticker] = {"price": price, "change": change}
        except:
            data[ticker] = {"price": "N/A", "change": 0}
    return data

def send_telegram(message):
    safe_msg = shlex.quote(message)
    subprocess.run(f'openclaw message send --channel telegram --target {TELEGRAM_CHAT_ID} --message {safe_msg}', shell=True)

def daily_digest():
    intel = load_intelligence()
    config = load_skill_config()
    
    holdings = intel.get("holdings", [])
    top_watchers = config.get("tiers", {}).get("top_watchers", [])
    waitlist = [t for t in intel.get("watchlist", []) if t not in top_watchers]
    
    print(f"📊 Preparing Tiered Sentinel Report...")
    
    # Process market data
    reporting_tickers = list(set(holdings + top_watchers))
    market_data = get_market_data(reporting_tickers)
    
    # Use OpenClaw Universal Model for three-section analysis
    sys.path.insert(0, '/root/.openclaw/skills/_shared/')
    from universal_model import get_ai_analysis

    prompt = f"""You are a Buffett-style CIO. Generate a three-section Portfolio Sentinel Report.
    
    Holdings: {json.dumps(holdings)}
    Top Watchers: {json.dumps(top_watchers)}
    Waitlist: {json.dumps(waitlist)}
    Market Data: {json.dumps(market_data)}
    
    TASK:
    Section 1: Core Holdings News
    - Search for major breaking news or earnings updates for the Holdings tickers.
    - Provide a concise summary for each relevant news item.
    - Include a markdown link [Source Title](URL) for each.

    Section 2: Top Watcher Promotions/Demotions
    - Analyze if any Top Watcher is qualified for promotion (Holdings) or demotion (Waitlist).
    - Provide a detailed fundamental reason based on moat durability or valuation.

    Section 3: Waitlist Radar
    - Identify 1-2 new companies for the Radar/Waitlist.
    - Give a clear reason why they are being added (e.g., emerging moat, industry tailwind).

    FORMAT:
    Return THREE clear blocks of text separated by "---SECTION_BREAK---". Use Lark Markdown syntax."""
    
    raw_analysis = get_ai_analysis(prompt, reasoning=True)
    sections = raw_analysis.split("---SECTION_BREAK---")
    
    # Ensure we have 3 sections or pad with empty strings
    while len(sections) < 3:
        sections.append("No updates for this section.")

    # Push to Feishu Card
    webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/abe2e939-a15a-44ba-b818-1cc01048b782"
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"tag": "plain_text", "content": "🛡️ Portfolio Sentinel: Strategic Briefing"}, "template": "indigo"},
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": "**Core Holdings Intelligence**\n" + sections[0].strip()}
                },
                {"tag": "hr"},
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": "**Tier Transitions**\n" + sections[1].strip()}
                },
                {"tag": "hr"},
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": "**Radar & Waitlist Expansion**\n" + sections[2].strip()}
                }
            ]
        }
    }
    requests.post(webhook, json=payload)
    print("Report delivered to Feishu.")

def main():
    now_bjs = datetime.now(BJS)
    # Check if it's the 7:45 AM BJ (approximate schedule for morning digest)
    # The actual cron handles the timing, this script just executes.
    daily_digest()

if __name__ == "__main__":
    main()
