#!/usr/bin/env python3
"""Grok API 调用脚本 - 纯标准库版本
Usage:
  python3 grok_chat.py "你好，Grok"
  python3 grok_chat.py --model grok-4.1-thinking --reasoning high "分析一下"
  python3 grok_chat.py --image "neon cat city"
  python3 grok_chat.py --list-models
"""
import os, sys, json, argparse, urllib.request, urllib.error

BASE_URL = os.environ.get("GROK_BASE_URL", "https://apileon.leonai.top/grok/v1")
API_KEY = os.environ.get("GROK_API_KEY", "")

HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json", "User-Agent": "GrokCLI/1.0"}

def _post(path, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(f"{BASE_URL}{path}", data=data, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read())

def _get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}", headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

def chat(prompt, model="grok-4.1-mini", system=None, reasoning=None, temperature=0.8):
    messages = []
    if system: messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    body = {"model": model, "messages": messages, "stream": False, "temperature": temperature}
    if reasoning: body["reasoning_effort"] = reasoning
    data = _post("/chat/completions", body)
    content = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    print(content)
    print(f"\n---\n📊 Model: {data.get('model')} | Tokens: {usage.get('prompt_tokens',0)}→{usage.get('completion_tokens',0)} ({usage.get('total_tokens',0)} total)")

def generate_image(prompt, size="1024x1024", n=1):
    data = _post("/images/generations", {"prompt": prompt, "model": "grok-imagine-1.0", "n": n, "size": size, "response_format": "url"})
    for i, img in enumerate(data.get("data", [])):
        print(f"🖼️ Image {i+1}: {img.get('url', 'no-url')}")

def generate_video(prompt, size="1792x1024", seconds=6, quality="standard"):
    data = _post("/videos", {"prompt": prompt, "model": "grok-imagine-1.0-video", "size": size, "seconds": seconds, "quality": quality})
    print(json.dumps(data, indent=2, ensure_ascii=False))

def list_models():
    data = _get("/models")
    for m in data.get("data", []):
        print(f"  {m['id']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grok API CLI")
    parser.add_argument("prompt", nargs="?", default=None)
    parser.add_argument("--model", "-m", default="grok-4.1-mini")
    parser.add_argument("--system", "-s", default=None)
    parser.add_argument("--reasoning", "-r", choices=["none","minimal","low","medium","high","xhigh"], default=None)
    parser.add_argument("--temperature", "-t", type=float, default=0.8)
    parser.add_argument("--image", action="store_true")
    parser.add_argument("--video", action="store_true")
    parser.add_argument("--size", default=None)
    parser.add_argument("--list-models", action="store_true")
    args = parser.parse_args()
    if not API_KEY: print("❌ GROK_API_KEY not set"); sys.exit(1)
    if args.list_models: list_models()
    elif args.image: generate_image(args.prompt, size=args.size or "1024x1024")
    elif args.video: generate_video(args.prompt, size=args.size or "1792x1024")
    elif args.prompt: chat(args.prompt, model=args.model, system=args.system, reasoning=args.reasoning, temperature=args.temperature)
    else: parser.print_help()
