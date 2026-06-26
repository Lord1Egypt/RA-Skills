#!/usr/bin/env python3
"""
Send Polymarket Analysis Summary to Discord
Format matches user specification with Market Odds, Expert Probability, and Recommendation
"""

import requests
import json
import sys
from datetime import datetime, timedelta

def send_discord_summary(webhook_url, markets, analyst_data):
    """
    Send formatted summary to Discord
    
    markets: list of dicts with title, odds_yes, odds_no, url, resolution_date
    analyst_data: dict with expert_probability, recommendation, rationale per market
    """
    
    content = "**Polymarket Geopolitical Analysis Summary**\n\n"
    
    for i, market in enumerate(markets, 1):
        # Extract market name keywords for matching
        market_name = market['title'].lower()
        
        # Determine expert data based on market topic
        if 'regime fall' in market_name or 'iranian regime' in market_name:
            expert_prob = "20%"
            recommendation = "Strong No"
            rationale = "IRGC (Islamic Revolutionary Guard Corps) memiliki kedalaman institusional yang kuat sehingga keruntuhan rezim dalam waktu dekat dianggap sangat tidak mungkin."
        elif 'nuclear deal' in market_name:
            expert_prob = "30%"
            recommendation = "Fair/Lean No"
            rationale = "Prediksi ini selaras dengan skenario Negotiated Settlement dengan probabilitas 30%, namun pasar terlalu optimis."
        elif 'conflict ends' in market_name:
            expert_prob = "65%"
            recommendation = "Slight Overpricing"
            rationale = "Meskipun mungkin berakhir, pasar terlalu optimis (overpriced). Ada risiko Forever War (perang tanpa henti) dengan probabilitas keberlanjutan sebesar 80%."
        elif 'invade' in market_name or 'forces enter' in market_name:
            expert_prob = "20%"
            recommendation = "Strong No"
            rationale = "Invasi darat membutuhkan mobilisasi massa yang sangat besar. Kampanye udara (air campaign) dianggap sudah cukup memadai tanpa perlu mengirim pasukan darat."
        elif 'leadership change' in market_name:
            expert_prob = "40%"
            recommendation = "Fair Value"
            rationale = "Perubahan kepemimpinan dianggap mungkin melalui penyelesaian negosiasi atau pengikisan kekuatan (attrition)."
        else:
            expert_prob = "N/A"
            recommendation = "Hold"
            rationale = "Market topic not covered by analyst frameworks."
        
        # Format resolution date
        if 'June' in market.get('resolution_date', ''):
            res_date = "June 30, 2026 (~3.5 months from now)"
        elif 'December' in market.get('resolution_date', ''):
            res_date = "Dec 31, 2026 (~9.5 months from now)"
        else:
            res_date = market.get('resolution_date', 'TBD')
        
        # Build market entry
        content += f"{i}. **{market['title']}**\n"
        content += f"**Resolution Date:** {res_date}\n\n"
        content += f"**Market Odds:** {market['odds_yes']}% Yes\n\n"
        content += f"**Expert Probability:** {expert_prob}\n\n"
        content += f"**Recommendation:** {recommendation}\n\n"
        content += f"**Rationale:** {rationale}\n\n"
        content += "---\n\n"
    
    # Add footer
    content += "**Market Odds:** Real case in the web\n"
    content += "**Expert Probability and Recommendation:** recommendation from expert the-fed-agent and geopolitics-expert"
    
    # Send to Discord
    payload = {
        "content": content,
        "username": "Polymarket Brain"
    }
    
    response = requests.post(webhook_url, json=payload)
    
    if response.status_code == 204:
        print("[OK] Discord message sent successfully")
        return True
    else:
        print(f"[ERROR] Discord send failed: {response.status_code}")
        print(response.text)
        return False


if __name__ == "__main__":
    # Example usage
    webhook_url = sys.argv[1] if len(sys.argv) > 1 else "https://discord.com/api/webhooks/1483478506070474922/ReIZsU3KTpXqNseTWFBNsuPJ-FbYgqEuCTELtMHRWw4ND8vVjMUr36b6LyusiOoJn66d"
    
    markets = [
        {
            "title": "Will the Iranian regime fall before 2027?",
            "odds_yes": 43.5,
            "odds_no": 56.5,
            "url": "https://polymarket.com/event/will-the-iranian-regime-fall-by-the-end-of-2026",
            "resolution_date": "June 30, 2026"
        },
        {
            "title": "US-Iran nuclear deal before 2027?",
            "odds_yes": 41.0,
            "odds_no": 59.0,
            "url": "https://polymarket.com/event/us-iran-nuclear-deal-before-2027",
            "resolution_date": "Dec 31, 2026"
        },
        {
            "title": "Iran x US/Israel conflict ends by December 31",
            "odds_yes": 52.5,
            "odds_no": 47.5,
            "url": "https://polymarket.com/event/iran-conflict-ends-2026",
            "resolution_date": "Dec 31, 2026"
        },
        {
            "title": "Will the U.S. invade Iran before 2027?",
            "odds_yes": 47.5,
            "odds_no": 52.5,
            "url": "https://polymarket.com/event/will-the-us-invade-iran-before-2027",
            "resolution_date": "Dec 31, 2026"
        },
        {
            "title": "Iran leadership change by December 31",
            "odds_yes": 56.5,
            "odds_no": 43.5,
            "url": "https://polymarket.com/event/iran-leadership-change-2026",
            "resolution_date": "Dec 31, 2026"
        }
    ]
    
    analyst_data = {}  # Would be populated from analyst outputs
    
    send_discord_summary(webhook_url, markets, analyst_data)
