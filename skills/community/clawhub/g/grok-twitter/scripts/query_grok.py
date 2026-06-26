#!/usr/bin/env python3
import sys
import json
import requests
import os

API_URL = os.getenv("GROK_API_URL", "https://api.cheaprouter.club/v1/chat/completions")
API_KEY = os.getenv("GROK_API_KEY")
MODEL = os.getenv("GROK_MODEL", "grok-4.20-beta")

if not API_KEY:
    print("❌ 错误: 请设置环境变量 GROK_API_KEY", file=sys.stderr)
    print("示例: export GROK_API_KEY='your-api-key'", file=sys.stderr)
    sys.exit(1)

def query_grok(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    
    result = response.json()
    return result["choices"][0]["message"]["content"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: query_grok.py <prompt>")
        sys.exit(1)
    
    prompt = " ".join(sys.argv[1:])
    result = query_grok(prompt)
    print(result)
