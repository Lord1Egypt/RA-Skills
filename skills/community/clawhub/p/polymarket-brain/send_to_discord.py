#!/usr/bin/env python3
"""
Phase 4: Send AI analysis to Discord webhook
"""

import json
import os
import sys
import requests
from datetime import datetime

# Discord webhook for market analysis (Phase 4)
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1483478506070474922/ReIZsU3KTpXqNseTWFBNsuPJ-FbYgqEuCTELtMHRWw4ND8vVjMUr36b6LyusiOoJn66d"

def send_to_discord(phase3_file):
    """Send final analysis to Discord"""
    print(f"\n{'='*60}")
    print("PHASE 4: Discord Dispatch")
    print("="*60)
    
    with open(phase3_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    timestamp = data.get('timestamp', datetime.now().isoformat())
    summaries = data.get('market_summaries', [])
    
    if not summaries:
        print("  ⚠️ No market summaries to send")
        return
    
    # Build Discord embeds
    embeds = []
    
    for summary in summaries:
        market = summary['market']
        rec = summary['recommendation']
        analysis = summary['analysis']
        
        # Determine color based on recommendation
        color_map = {
            "BUY": 0x00ff00,  # Green
            "SELL": 0xff0000, # Red
            "HOLD": 0xffff00, # Yellow
        }
        color = color_map.get(rec['action'], 0x808080)
        
        embed = {
            "title": f"{market['title'][:100]}",
            "description": f"**Recommendation: {rec['action']}**\n\n{rec['reasoning'][:2000]}",
            "color": color,
            "fields": [
                {
                    "name": "Market Odds",
                    "value": f"Yes: {market.get('yes_odds', 'N/A')}% | No: {market.get('no_odds', 'N/A')}%",
                    "inline": True
                },
                {
                    "name": "Expert Probability",
                    "value": f"Yes: {analysis.get('expert_probability_yes', 'N/A')}%",
                    "inline": True
                },
                {
                    "name": "Edge",
                    "value": f"{rec['edge_percent']}%",
                    "inline": True
                },
                {
                    "name": "Matched Articles",
                    "value": str(len(summary.get('matched_articles', []))),
                    "inline": True
                }
            ],
            "url": market.get('polymarket_url', ''),
            "timestamp": timestamp
        }
        embeds.append(embed)
    
    # Send in batches (Discord limit: 10 embeds per message)
    batch_size = 10
    for i in range(0, len(embeds), batch_size):
        batch = embeds[i:i+batch_size]
        
        payload = {
            "content": f"🧠 **Polymarket AI Analysis** | {len(summaries)} opportunities found\n<t:{int(datetime.now().timestamp())}:R>",
            "embeds": batch
        }
        
        try:
            resp = requests.post(
                DISCORD_WEBHOOK,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if resp.status_code == 204:
                print(f"  ✓ Sent batch {i//batch_size + 1} ({len(batch)} markets)")
            else:
                print(f"  ✗ Discord error {resp.status_code}: {resp.text}")
                
        except Exception as e:
            print(f"  ✗ Failed to send: {e}")
    
    print(f"\n  ✓ Phase 4 COMPLETE: Sent to Discord webhook")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        phase3_file = os.path.join(output_dir, 'phase3_market_matches.json')
    else:
        phase3_file = sys.argv[1]
    
    if not os.path.exists(phase3_file):
        print(f"  ✗ Error: Phase 3 output not found: {phase3_file}")
        print("  → Run AI analyzer first: python ai_analyzer.py")
        sys.exit(1)
    
    send_to_discord(phase3_file)
