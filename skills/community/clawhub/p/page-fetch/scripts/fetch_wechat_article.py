#!/usr/bin/env python3
import argparse
import json
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

MOBILE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 "
        "MicroMessenger/8.0.42(0x18002a2a) NetType/WIFI Language/zh_CN"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://mp.weixin.qq.com/",
}


def is_wechat_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc.endswith("mp.weixin.qq.com")


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def fetch_html(url: str, timeout: int, cookie: Optional[str] = None):
    headers = dict(MOBILE_HEADERS)
    if cookie:
        headers["Cookie"] = cookie
    response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
    response.raise_for_status()
    return response.text, response


def detect_access_limit(final_url: str, html: str) -> Optional[str]:
    final_url = final_url or ""
    signals = [
        "访问验证",
        "安全验证",
        "环境异常",
        "需要先完成验证",
        "操作过于频繁",
        "请在微信客户端打开链接",
    ]
    if "wappoc_appmsgcaptcha" in final_url or "captcha" in final_url.lower():
        return "wechat-captcha"
    for signal in signals:
        if signal in html:
            return f"wechat-access-limited:{signal}"
    return None


SCRIPT_PATTERNS = {
    "title": r"var\s+msg_title\s*=\s*'([^']+)'|var\s+msg_title\s*=\s*\"([^\"]+)\"",
    "author": r"var\s+msg_author\s*=\s*'([^']*)'|var\s+msg_author\s*=\s*\"([^\"]*)\"",
    "account_nickname": r"var\s+nickname\s*=\s*'([^']+)'|var\s+nickname\s*=\s*\"([^\"]+)\"",
    "biz": r"var\s+biz\s*=\s*'([^']+)'|var\s+__biz\s*=\s*'([^']+)'",
    "mid": r'var\s+mid\s*=\s*["\']?([0-9]+)',
    "idx": r'var\s+idx\s*=\s*["\']?([0-9]+)',
    "sn": r"var\s+sn\s*=\s*'([^']+)'|var\s+sn\s*=\s*\"([^\"]+)\"",
    "create_time": r'var\s+create_time\s*=\s*["\']?([0-9]{10})',
}


def first_group(match: re.Match) -> Optional[str]:
    for group in match.groups():
        if group:
            return group
    return None


def parse_meta(html: str, final_url: str) -> Dict[str, Optional[str]]:
    soup = BeautifulSoup(html, "html.parser")
    meta: Dict[str, Optional[str]] = {
        "title": None,
        "author": None,
        "account_nickname": None,
        "description": None,
        "published_time": None,
        "cover_image": None,
        "final_url": final_url,
    }

    meta_map = {
        "og:title": "title",
        "og:article:author": "author",
        "og:description": "description",
        "og:image": "cover_image",
        "weixin:account": "account_id",
    }
    for prop, key in meta_map.items():
        tag = soup.find("meta", property=prop)
        if tag and tag.get("content"):
            meta[key] = clean_text(tag["content"])

    scripts_text = "\n".join(script.get_text(" ", strip=False) for script in soup.find_all("script"))
    for key, pattern in SCRIPT_PATTERNS.items():
        if meta.get(key):
            continue
        m = re.search(pattern, scripts_text)
        if not m:
            continue
        val = first_group(m)
        if not val:
            continue
        if key == "create_time":
            meta["published_time"] = datetime.fromtimestamp(int(val)).isoformat()
            meta[key] = val
        else:
            meta[key] = val

    if not meta.get("title") and soup.title and soup.title.string:
        meta["title"] = clean_text(soup.title.string)

    return meta


def extract_content_html(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", id="js_content") or soup.find("div", class_="rich_media_content")
    if not content:
        return None
    for tag in content.find_all(["script", "style"]):
        tag.decompose()
    return str(content)


def extract_content_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", id="js_content") or soup.find("div", class_="rich_media_content")
    if not content:
        return ""
    parts: List[str] = []
    for node in content.find_all(["p", "section", "blockquote", "li", "h1", "h2", "h3", "h4"]):
        text = clean_text(node.get_text(" ", strip=True))
        if len(text) >= 2:
            parts.append(text)
    if not parts:
        parts = [clean_text(content.get_text(" ", strip=True))]
    text = "\n\n".join([p for p in parts if p])
    return text.strip()


def build_payload(url: str, html: str, response: requests.Response) -> Dict[str, object]:
    meta = parse_meta(html, str(response.url))
    access_limit = detect_access_limit(str(response.url), html)
    text = extract_content_text(html)
    content_html = extract_content_html(html)
    notes: List[str] = []

    if access_limit:
        notes.append(f"access limited: {access_limit}")
    if str(response.url) != url:
        notes.append("redirected before extraction")

    method = "wechat-dom"
    if access_limit and not text:
        method = "wechat-access-limited"

    excerpt = clean_text(text[:280]) if text else meta.get("description")
    payload: Dict[str, object] = {
        "url": url,
        "final_url": str(response.url),
        "status_code": response.status_code,
        "title": meta.get("title"),
        "description": meta.get("description"),
        "author": meta.get("author"),
        "account_nickname": meta.get("account_nickname"),
        "published_time": meta.get("published_time"),
        "method": method,
        "text": text,
        "content_html": content_html,
        "excerpt": excerpt,
        "notes": notes,
        "access_limited": bool(access_limit),
        "access_limit_reason": access_limit,
    }
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch WeChat public account article content without persistence.")
    parser.add_argument("url")
    parser.add_argument("--cookie", default=None)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--format", choices=["json", "text"], default="json")
    parser.add_argument("--max-chars", type=int, default=12000)
    args = parser.parse_args()

    if not is_wechat_url(args.url):
        payload = {"url": args.url, "error": "not a WeChat public article URL", "method": "wechat-invalid-url"}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 2

    try:
        html, response = fetch_html(args.url, args.timeout, args.cookie)
        payload = build_payload(args.url, html, response)
    except requests.RequestException as exc:
        payload = {
            "url": args.url,
            "error": str(exc),
            "method": "wechat-requests-failed",
            "next_step": "Try a valid cookie, a fresh short link, or report that access is restricted.",
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    if args.max_chars and payload.get("text"):
        payload["text"] = str(payload["text"])[: args.max_chars]

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"Title: {payload.get('title') or ''}")
    if payload.get("account_nickname"):
        print(f"Account: {payload['account_nickname']}")
    if payload.get("author"):
        print(f"Author: {payload['author']}")
    if payload.get("published_time"):
        print(f"Published: {payload['published_time']}")
    print(f"Method: {payload['method']}")
    if payload.get("access_limited"):
        print(f"Access: {payload.get('access_limit_reason')}")
    print()
    print(payload.get("text") or "")
    if payload.get("notes"):
        print()
        print("Notes:")
        for note in payload["notes"]:
            print(f"- {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
