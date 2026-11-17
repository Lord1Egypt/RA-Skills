#!/usr/bin/env python3
"""
Generate N social media posts (90 days = 45 posts, 1 every other day) for a client.

Inputs:
  --client-json  : normalized client JSON (from fetch_client.py, either mode)
  --sitemap-file : list of page URLs (one per line) from the client's sitemap.xml
  --start-date   : YYYY-MM-DD (default: today)
  --count        : number of posts (default 45)
  --time         : post time (default 09:00:00)

LLM key: --llm-key flag, or env fallback DEEPSEEK_API_KEY / OPENAI_API_KEY.
The ONLY env var this package requires overall is HIGHLEVEL_ACCESS_TOKEN,
and only in HL mode. No other credentials are needed here.

Output: <out> CSV in HighLevel Social Planner import format + <out>-posts.json
"""
import argparse
import csv
import io
import json
import os
import re
import sys
import urllib.request
from datetime import date, datetime, timedelta

from common import load_env


def build_schedule(start_date: str, count: int = 45, time_str: str = "09:00:00") -> list[str]:
    d = datetime.strptime(start_date, "%Y-%m-%d")
    return [(d + timedelta(days=i * 2)).strftime("%Y-%m-%d") + " " + time_str for i in range(count)]


def call_llm(env, prompt: str, max_tokens: int = 12000, llm_key: str = "", llm_model: str = "", llm_base: str = "") -> str:
    key = llm_key
    if not key:
        print("ERROR: no LLM key. Pass --llm-key (the only env var in this package is HIGHLEVEL_ACCESS_TOKEN).", file=sys.stderr)
        sys.exit(2)
    model = llm_model or "deepseek-chat"
    base = llm_base or "https://api.deepseek.com/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.9,
    }).encode()
    req = urllib.request.Request(base, data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        resp = json.loads(r.read())
    return resp["choices"][0]["message"]["content"]


def parse_posts(raw: str) -> list[dict]:
    posts = []
    chunks = [c.strip() for c in re.split(r"\||\n", raw) if c.strip()]
    for ch in chunks:
        m = re.match(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})[,|](.*?)[,|]\s*(https?://\S+)\s*$", ch, re.S)
        if m:
            posts.append({"date": m.group(1), "content": m.group(2).strip(), "url": m.group(3).strip()})
    return posts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client-json", required=True)
    ap.add_argument("--sitemap-file", required=True)
    ap.add_argument("--start-date", default=date.today().isoformat())
    ap.add_argument("--count", type=int, default=45)
    ap.add_argument("--time", default="09:00:00")
    ap.add_argument("--out", default="")
    ap.add_argument("--llm-key", default="")
    ap.add_argument("--llm-model", default="")
    ap.add_argument("--llm-base", default="", help="OpenAI-compatible endpoint (default DeepSeek; use https://api.openai.com/v1/chat/completions for ChatGPT/OpenAI keys)")
    args = ap.parse_args()

    client = json.load(open(args.client_json))
    urls = [u.strip() for u in open(args.sitemap_file) if u.strip()]
    if len(urls) < 5:
        print(f"ERROR: only {len(urls)} sitemap URLs - need more to link posts", file=sys.stderr)
        sys.exit(2)

    schedule = build_schedule(args.start_date, args.count, args.time)
    company = client.get("companyName") or client.get("firstName") or "Client"
    cf = client.get("customFields", {})
    biz_cat = cf.get("Business Category") or cf.get("business category") or ""
    desc = cf.get("Company Description") or cf.get("company description") or ""
    city = client.get("city") or ""
    state = client.get("state") or ""
    site = (client.get("website") or "").replace("https://", "").replace("http://", "").rstrip("/")

    url_list = urls[:]
    assigned = [url_list[i % len(url_list)] for i in range(args.count)]

    prompt = f"""Act as a social media content expert. Create exactly {args.count} social media posts, one every 2 days, starting {args.start_date}, each at {args.time}. Dates in this format: {args.start_date} {args.time} (YYYY-MM-DD HH:mm:ss).

Platforms: Instagram, LinkedIn, Google Business, Facebook. Balance posts between entertaining/funny, informative, and self-promotional.

RULES:
- Each post must use exactly 1 URL from the provided list, and the post content must be relevant to that page (it is a service page, a service-area page, or a blog post). The URL goes at the end of each post line.
- The subject of each post should relate to the relevant page name.
- Be engaging: ask questions or reference any upcoming holidays within the next 60 days.
- Do not use emojis. Do not number the posts. Use no commas in the post text (other punctuation is ok).
- Show relevant hashtags at the end of the content.
- We create the images with AI, so do not claim the images show real work or real life, do not mention AI at all, and do not describe the type of image to create.
- This is for a {biz_cat} company in {city}, {state} called {company} (website: {site}).
- Company info: {desc}
- Page URLs (use 1 per post, in order, repeating if needed):
{chr(10).join(f'- {u}' for u in url_list)}

OUTPUT FORMAT: each post on its own line, exactly:
date,content,url
No extra text, no headers. {args.count} lines total."""

    env = load_env()
    raw = call_llm(env, prompt, llm_key=args.llm_key, llm_model=args.llm_model, llm_base=args.llm_base)
    posts = parse_posts(raw)

    if len(posts) != args.count:
        print(f"WARN: parsed {len(posts)}/{args.count} posts, rebuilding", file=sys.stderr)
        lines = [l for l in raw.splitlines() if l.strip()]
        posts = []
        for i in range(min(args.count, len(lines))):
            content = lines[i].strip()
            content = re.sub(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\s*[,|]\s*", "", content)
            content = re.sub(r"\s*[,|]\s*https?://\S+\s*$", "", content)
            posts.append({"date": schedule[i], "content": content, "url": assigned[i]})

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["postAtSpecificTime (YYYY-MM-DD HH:mm:ss)", "content", "link (OGmetaUrl)", "imageUrls", "gifUrl", "videoUrls", "thumbnailUrl"])
    for p in posts:
        writer.writerow([p["date"], p["content"], p["url"], "", "", "", ""])

    slug = re.sub(r"[^a-z0-9]+", "-", company.lower()).strip("-")
    out_path = args.out or f"output/{slug}-social-90d.csv"
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w") as f:
        f.write(buf.getvalue())

    posts_path = out_path.replace(".csv", "-posts.json")
    with open(posts_path, "w") as f:
        json.dump(posts, f, indent=2)

    print(f"WROTE {len(posts)} posts -> {out_path}")
    print(f"posts json -> {posts_path}")


if __name__ == "__main__":
    main()
