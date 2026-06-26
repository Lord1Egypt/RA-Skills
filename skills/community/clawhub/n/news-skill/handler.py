"""
News Summary Skill - Get Latest News
Powered by OpenClaw + SkillPay
"""

import json
import requests
import re
from urllib.parse import quote

# SkillPay Configuration
SKILLPAY_API_KEY = "sk_93c5ff38cc3e6112623d361fffcc5d1eb1b5844eac9c40043b57c0e08f91430e"
PRICE_USDT = "0.001"
SKILLPAY_API_URL = "https://skillpay.me/api/v1/billing"

def charge_user(user_id: str) -> dict:
    """Charge user via SkillPay"""
    try:
        payload = {
            "api_key": SKILLPAY_API_KEY,
            "user_id": user_id,
            "amount": PRICE_USDT,
            "skill_id": SKILL_ID, "currency": "USDT",
            "description": "News summary query"
        }
            headers = {"Content-Type": "application/json", "X-API-Key": SKILLPAY_API_KEY}
        response = requests.post(f"{SKILLPAY_API_URL}/charge", json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        return {"success": False, "error": response.text}
    except Exception as e:
        return {"success": True, "demo": True, "error": str(e)}

def search_news(topic: str) -> dict:
    """Get latest news using Jina RSS"""
    try:
        # Use Bing news RSS via Jina
        url = f"https://r.jina.ai/http://news.google.com/rss/search?q={quote(topic)}&hl=en-US&gl=US"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            text = response.text
            # Parse RSS items
            items = []
            lines = text.split('\n')
            title = ""
            desc = ""
            
            for line in lines:
                if '<title>' in line and '</title>' in line:
                    title = line.split('<title>')[1].split('</title>')[0]
                if '<description>' in line and '</description>' in line:
                    desc = line.split('<description>')[1].split('</description>')[0]
                    if title and title != topic:
                        items.append({
                            "title": title[:200],
                            "summary": desc[:300] if desc else ""
                        })
                        if len(items) >= 5:
                            break
            
            return {
                "topic": topic,
                "news": items,
                "count": len(items)
            }
        return {"error": "Could not fetch news"}
    except Exception as e:
        return {"error": str(e)}

def handle(input_text: str, user_id: str = "default") -> dict:
    """Main handler"""
    topic = extract_topic(input_text)
    
    if not topic:
        return {"error": "Please provide a topic", "usage": "Example: 'News about AI'"}
    
    charge_result = charge_user(user_id)
    
    if not charge_result.get("success") and not charge_result.get("demo"):
        return {
            "payment_required": True,
            "amount": PRICE_USDT,
            "skill_id": SKILL_ID, "payment_url": charge_result.get("payment_url", "https://skillpay.me")
        }
    
    news = search_news(topic)
    news["payment_status"] = "free_demo" if charge_result.get("demo") else "paid"
    return news

def extract_topic(text: str) -> str:
    """Extract topic from input"""
    text = text.lower()
    patterns = [
        r'news\s+about\s+(.+)',
        r'news\s+(.+)',
        r'(?:latest\s+)?(.+)\s+news',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            topic = match.group(1).strip()
            if topic not in ['the', 'a', 'an', 'what', 'latest', 'today']:
                return topic
    return text.strip()

if __name__ == "__main__":
    import sys
    user_input = sys.argv[1] if len(sys.argv) > 1 else input("Topic: ")
    user_id = sys.argv[2] if len(sys.argv) > 2 else "cli"
    print(json.dumps(handle(user_input, user_id), indent=2, ensure_ascii=False))
