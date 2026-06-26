"""
AI Art Prompt Generator - Generate prompts for Midjourney/DALL-E/SDXL
Powered by OpenClaw + SkillPay
"""

import json
import requests
import re
import random

# SkillPay Configuration
SKILLPAY_API_KEY = "sk_93c5ff38cc3e6112623d361fffcc5d1eb1b5844eac9c40043b57c0e08f91430e"
PRICE_USDT = "0.001"
SKILLPAY_API_URL = "https://skillpay.me/api/v1/billing"

# Prompt templates and modifiers
LIGHTING = [
    "cinematic lighting", "golden hour", "soft studio lighting", "neon lighting",
    "volumetric lighting", "rim lighting", "natural light", "dramatic shadows",
    "bioluminescent", "ray tracing", "god rays", "backlit"
]

STYLES = [
    "hyperrealistic", "digital painting", "concept art", "3D render", "anime style",
    "oil painting", "watercolor", "photorealistic", "illustration", "vector art",
    "low poly", "pixel art", "cyberpunk", "steampunk", "fantasy", "sci-fi"
]

COMPOSITIONS = [
    "wide angle", "close-up", "bird's eye view", "worm's eye view", "portrait",
    "full body shot", "dynamic angle", "rule of thirds", "centered composition",
    "symmetrical", "leading lines", "depth of field"
]

QUALITY = [
    "8K resolution", "4K", "highly detailed", "masterpiece", "best quality",
    "extremely detailed", "professional photography", "cinematic quality"
]

def charge_user(user_id: str) -> dict:
    """Charge user via SkillPay"""
    try:
        payload = {
            "api_key": SKILLPAY_API_KEY,
            "user_id": user_id,
            "amount": PRICE_USDT,
            "skill_id": SKILL_ID, "currency": "USDT",
            "description": "AI prompt generation"
        }
            headers = {"Content-Type": "application/json", "X-API-Key": SKILLPAY_API_KEY}
        response = requests.post(f"{SKILLPAY_API_URL}/charge", json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        return {"success": False, "error": response.text}
    except Exception as e:
        return {"success": True, "demo": True, "error": str(e)}

def extract_subject(text: str) -> str:
    """Extract the main subject from input"""
    text = text.lower()
    # Remove common phrases
    for phrase in ["generate a prompt", "create prompt", "prompt for", "prompt about", "a prompt", "for a", "an"]:
        text = text.replace(phrase, "")
    return text.strip()

def generate_prompt(subject: str) -> dict:
    """Generate optimized AI art prompt"""
    # Select random modifiers
    lighting = random.choice(LIGHTING)
    style = random.choice(STYLES)
    composition = random.choice(COMPOSITIONS)
    quality = random.choice(QUALITY)
    
    # Generate different prompt versions
    prompts = {
        "midjourney": f"{subject}, {lighting}, {style}, {composition}, {quality}, --ar 16:9 --v 6",
        "dalle": f"{subject}. {lighting}, {style}, {composition}, {quality}. High detail.",
        "sdxl": f"{subject}, {lighting}, {style}, {composition}, {quality}, masterpiece, best quality"
    }
    
    # Also create a mixed version
    mixed = f"{subject}, {lighting}, {style}, {composition}, {quality}, {random.choice(QUALITY)}"
    
    return {
        "subject": subject,
        "prompts": {
            "midjourney": prompts["midjourney"],
            "dalle": prompts["dalle"],
            "sdxl": prompts["sdxl"],
            "general": mixed
        },
        "tips": [
            f"Try adding '{random.choice(LIGHTING)}' for more atmosphere",
            f"Use '{random.choice(COMPOSITIONS)}' for better composition",
            "Start with the subject, then add modifiers",
            "Use commas to separate concepts for better results"
        ]
    }

def handle(input_text: str, user_id: str = "default") -> dict:
    """Main handler"""
    subject = extract_subject(input_text)
    
    if not subject:
        return {
            "error": "Please provide a subject",
            "usage": "Example: 'Generate prompt for a cyberpunk city'"
        }
    
    charge_result = charge_user(user_id)
    
    if not charge_result.get("success") and not charge_result.get("demo"):
        return {
            "payment_required": True,
            "amount": PRICE_USDT,
            "skill_id": SKILL_ID, "payment_url": charge_result.get("payment_url", "https://skillpay.me")
        }
    
    result = generate_prompt(subject)
    result["payment_status"] = "free_demo" if charge_result.get("demo") else "paid"
    return result

if __name__ == "__main__":
    import sys
    user_input = sys.argv[1] if len(sys.argv) > 1 else input("Subject: ")
    user_id = sys.argv[2] if len(sys.argv) > 2 else "cli"
    print(json.dumps(handle(user_input, user_id), indent=2, ensure_ascii=False))
