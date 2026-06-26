#!/usr/bin/env python3
"""Send Discord messages for Polymarket-Brain v1.0 - Reads from recommendations.json"""

import requests
import json
import sys
import os
import time

WEBHOOK_URL = "https://discord.com/api/webhooks/1483478506070474922/ReIZsU3KTpXqNseTWFBNsuPJ-FbYgqEuCTELtMHRWw4ND8vVjMUr36b6LyusiOoJn66d"

def send_message(msg):
    """Send single market analysis to Discord"""
    try:
        # Build content with ASCII-safe characters for Windows console
        lines = [
            f"**{msg.get('market', 'Unknown Market')}**",
            "",
            f"**Resolution Date:** {msg.get('resolution', 'N/A')}",
            f"**Market Odds:** {msg.get('market_odds', 'N/A')}",
            f"**Expert Probability:** {msg.get('expert_probability', 'N/A')}",
            f"**Recommendation:** {msg.get('recommendation', 'N/A')}",
            "",
            f"**Reasoning:** {msg.get('reasoning', 'N/A')}",
            "",
            f"**Link:** {msg.get('link', 'N/A')}",
            "",
            f"**Edge:** {msg.get('edge', '0%')} market mispricing",
            "",
            "--- Analyzed by Polymarket-Brain v1.0 | Confidence: HIGH"
        ]
        
        content = "\n".join(lines)
        
        payload = {"content": content}
        response = requests.post(WEBHOOK_URL, json=payload, timeout=30)
        
        if response.status_code == 204:
            print(f"  [OK] {msg.get('market', 'Unknown')}")
            time.sleep(1.2)  # Delay to avoid rate limiting
            return True
        else:
            print(f"  [FAIL] HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

def send_header():
    """Send workflow header"""
    try:
        header = {
            "content": "**POLYMARKET-BRAIN v1.0 WORKFLOW INITIATED**\n\n" +
                       "Phase 1: CNBC News Fetched\n" +
                       "Phase 2: Expert Analysis Complete\n" +
                       "Phase 3: Market Matching Complete\n" +
                       "Phase 4: Discord Output\n\n" +
                       "---"
        }
        response = requests.post(WEBHOOK_URL, json=header, timeout=30)
        if response.status_code == 204:
            print("[OK] Header sent")
            time.sleep(1.2)
        else:
            print(f"[WARN] Header: HTTP {response.status_code}")
    except Exception as e:
        print(f"[WARN] Header: {e}")

def send_summary(recommendations):
    """Send summary of all recommendations"""
    try:
        # Build summary with key edges
        edges = []
        for rec in recommendations:
            if rec['edge'].startswith('+'):
                edges.append(f"- {rec['market']}: {rec['edge']} ({rec['recommendation']})")
        
        edge_text = "\n".join(edges[:5]) if edges else "No significant edges found"
        
        summary = {
            "content": "**POLYMARKET-BRAIN v1.0 COMPLETE**\n\n" +
                      "**Key Trading Edges:**\n" + edge_text + "\n\n" +
                      "**Expert Agents Used:**\n" +
                      "- AI-powered geopolitics analysis\n" +
                      "- AI-powered Fed policy analysis\n" +
                      "- Real-time Polymarket odds matching\n\n" +
                      "---"
        }
        
        response = requests.post(WEBHOOK_URL, json=summary, timeout=30)
        if response.status_code == 204:
            print("[OK] Summary sent")
        else:
            print(f"[WARN] Summary: HTTP {response.status_code}")
    except Exception as e:
        print(f"[WARN] Summary: {e}")

def main():
    print("Sending Polymarket-Brain analysis to Discord...")
    
    # Send header
    send_header()
    
    # Load recommendations
    rec_file = r"C:\Users\Legion 5i Pro\.browseros\skills\polymarket-brain\output\phase3_markets.json"
    
    if not os.path.exists(rec_file):
        print(f"[ERROR] Recommendations file not found: {rec_file}")
        sys.exit(1)
    
    with open(rec_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    recommendations = data.get('markets', data.get('recommendations', []))
    print(f"Loaded {len(recommendations)} recommendations")
    
    # Send each recommendation
    for i, rec in enumerate(recommendations, 1):
        print(f"Sending {i}/{len(recommendations)}...", end=" ", flush=True)
        send_message(rec)
    
    # Send summary
    send_summary(recommendations)
    
    print("\nAll messages sent!")

if __name__ == "__main__":
    main()
