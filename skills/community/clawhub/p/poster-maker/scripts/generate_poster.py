#!/usr/bin/env python3
"""
AI 海报生成器。用法：
  python3 generate_poster.py --prompt prompt.txt -o poster.png
  python3 generate_poster.py --text "生成一张..." -o poster.png --size 1080x1080
"""
import json, base64, os, sys, argparse, urllib.request

def generate(prompt, size, api_key):
    payload = json.dumps({"model":"google/gemini-3-pro-image-preview","prompt":prompt,"size":size,"response_format":"b64_json"}).encode()
    req = urllib.request.Request("https://api.ofox.ai/v1/images/generations",data=payload,
        headers={"Content-Type":"application/json","Authorization":f"Bearer {api_key}"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode())
    imgs = data.get("data",[])
    if imgs and imgs[0].get("b64_json"):
        return base64.b64decode(imgs[0]["b64_json"])
    raise RuntimeError(f"No image: {json.dumps(data)[:200]}")

def main():
    p = argparse.ArgumentParser(description="AI 海报生成器")
    p.add_argument("--prompt",help="Prompt 文件路径")
    p.add_argument("--text",help="直接传入 prompt")
    p.add_argument("-o","--output",required=True)
    p.add_argument("--size",default="1024x1792")
    args = p.parse_args()
    prompt = open(args.prompt).read() if args.prompt else args.text
    if not prompt: print("ERROR: --prompt or --text required"); sys.exit(1)
    api_key = os.environ.get("OFOX_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
    if not api_key: print("ERROR: set IMAGE_API_KEY (Ofox or OpenRouter key)"); sys.exit(1)
    print(f"Size: {args.size} | Generating...",flush=True)
    img = generate(prompt, args.size, api_key)
    with open(args.output,"wb") as f: f.write(img)
    print(f"Done: {args.output} ({len(img)} bytes)")

if __name__=="__main__": main()
