#!/usr/bin/env python3
"""
Portfolio Sentinel - Moat Audit Engine (FIXED)
Evaluates companies on competitive durability (Buffett Style)
Automatically rotates through the watchlist and holdings.
"""
import json
import subprocess
import sys
import os
import random
from datetime import datetime, timedelta

# --- Configuration ---
sys.path.insert(0, '/root/.openclaw/skills/_shared/')
from universal_model import get_ai_analysis

FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/abe2e939-a15a-44ba-b818-1cc01048b782"
INTELLIGENCE_FILE = "/root/.openclaw/workspace/investment_intelligence.json"
SKILL_CONFIG = "/root/.openclaw/skills/portfolio-sentinel/config.json"
HISTORY_FILE = "/root/.openclaw/skills/portfolio-sentinel/audit_history.json"

def web_search(query, count=5):
    result = subprocess.run(
        ["openclaw", "web-search", "--query", query, "--count", str(count)],
        capture_output=True, text=True, timeout=180
    )
    try:
        data = json.loads(result.stdout)
        return "\n".join([f"- {r['title']}: {r.get('description', '')}" for r in data.get('results', [])])
    except:
        return "Search failed."

def run_moat_audit(ticker):
    print(f"🏰 Auditing Moat for {ticker}...")
    
    # 1. Research fundamental durability
    news = web_search(f"{ticker} competitive advantage moat market share competitors 2026", count=8)
    
    # 2. AI Analysis (Buffett Persona)
    prompt = f"""You are Warren Buffett. Perform a Deep Moat Audit on {ticker}.
    
    Context:
    {news}
    
    Task:
    Evaluate the company based on:
    1. Moat Type (Network Effect, Switching Costs, Cost Advantage, or Intangibles).
    2. Moat Strength (Wide, Narrow, or None/Eroding).
    3. Management & Capital Allocation (How are they spending their cash?).
    4. 10-Year Durability (Will this company be more powerful in 2035?).
    
    Format: English, concise, high-conviction. Use Markdown headers."""
    
    audit = get_ai_analysis(prompt, reasoning=True)
    return audit

def send_to_feishu(ticker, audit):
    import requests
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": f"🏰 Moat Audit: {ticker}"},
                "template": "indigo"
            },
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": audit}}
            ]
        }
    }
    requests.post(FEISHU_WEBHOOK, json=payload)

def get_rotation_ticker():
    """Proper rotation: picks the least recently audited ticker that's NOT been done in the last 7 days."""
    try:
        # Load all tickers from intelligence file
        with open(INTELLIGENCE_FILE, 'r') as f:
            intel = json.load(f)
        all_tickers = intel.get("holdings", []) + intel.get("watchlist", [])
        all_tickers = list(set(all_tickers)) # Deduplicate
        
        # Load history
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        else:
            history = {}

        current_ts = datetime.now().timestamp()
        seven_days_ago = current_ts - (7 * 24 * 60 * 60)
        
        # Filter: tickers NOT audited in the last 7 days
        eligible = [t for t in all_tickers if history.get(t, 0) < seven_days_ago]
        
        if eligible:
            # Pick a random one from eligible
            chosen = random.choice(eligible)
            print(f"🎯 Rotation: {chosen} (not audited in 7 days)")
            return chosen
        else:
            # If ALL tickers were audited recently, pick the oldest one anyway
            all_tickers.sort(key=lambda t: history.get(t, 0))
            chosen = all_tickers[0]
            print(f"🔄 Fallback: {chosen} (all audited recently)")
            return chosen
            
    except Exception as e:
        print(f"Rotation error: {e}")
        return "NVDA"

def update_history(ticker):
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        else:
            history = {}
        
        history[ticker] = datetime.now().timestamp()
        
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except:
        pass

def main():
    if len(sys.argv) < 2:
        ticker = get_rotation_ticker()
    else:
        ticker = sys.argv[1]
        
    audit_result = run_moat_audit(ticker)
    send_to_feishu(ticker, audit_result)
    update_history(ticker)
    print(f"✅ Audit for {ticker} delivered to Feishu. History updated.")

if __name__ == "__main__":
    main()
