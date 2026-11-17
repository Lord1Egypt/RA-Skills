"""
Draft creation — create WeChat draft via draft/add API.
v2: adds verify_draft, push_loop, and republish_with_images helpers.
"""

import json
import re
import sys
import time
import requests
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class DraftResult:
    media_id: str


@dataclass
class VerifyResult:
    media_id: str
    title: str
    content_length: int
    has_images: bool
    image_count: int
    style_stats: dict
    raw_response: str


def _safe_title(title: str, max_chars: int = 64) -> str:
    if len(title) <= max_chars:
        return title
    return title[:max_chars]


def _safe_digest(digest: str, max_chars: int = 120) -> str:
    if len(digest) <= max_chars:
        return digest
    return digest[:max_chars]


def create_draft(
    access_token: str,
    title: str,
    html: str,
    digest: str,
    thumb_media_id: Optional[str] = None,
    author: Optional[str] = None,
) -> DraftResult:
    """Create a draft in WeChat."""
    safe_title = _safe_title(title, max_chars=64)
    safe_digest = _safe_digest(digest, max_chars=120)
    safe_author = (author or "")[:8]

    article = {
        "title": safe_title,
        "author": safe_author,
        "digest": safe_digest,
        "content": html,
        "show_cover_pic": 0,
    }
    if thumb_media_id:
        article["thumb_media_id"] = thumb_media_id

    body = {"articles": [article]}
    resp = requests.post(
        "https://api.weixin.qq.com/cgi-bin/draft/add",
        params={"access_token": access_token},
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    data = resp.json()
    errcode = data.get("errcode", 0)
    if errcode != 0:
        errmsg = data.get("errmsg", "unknown error")
        raise ValueError(f"create_draft error: errcode={errcode}, errmsg={errmsg}")
    if "media_id" not in data:
        raise ValueError(f"create_draft: missing media_id: {data}")
    return DraftResult(media_id=data["media_id"])


def verify_draft(access_token: str, media_id: str) -> VerifyResult:
    """Read back draft from WeChat server to verify storage integrity.
    
    CRITICAL: Must use resp.content.decode('utf-8') instead of resp.json()
    because WeChat draft/get returns Content-Type: text/plain with no charset,
    and resp.json() defaults to ISO-8859-1 causing fake mojibake.
    """
    resp = requests.post(
        "https://api.weixin.qq.com/cgi-bin/draft/get",
        params={"access_token": access_token},
        data=json.dumps({"media_id": media_id}).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    # Use decode('utf-8') NOT resp.json() — see docstring above
    raw_text = resp.content.decode("utf-8")
    data = json.loads(raw_text)

    errcode = data.get("errcode", 0)
    if errcode != 0:
        errmsg = data.get("errmsg", "unknown error")
        raise ValueError(f"verify_draft error: errcode={errcode}, errmsg={errmsg}")

    news_item = data.get("news_item", [{}])[0]
    content = news_item.get("content", "")

    # Analyze CSS style stats
    style_stats = {
        "border_radius": content.count("border-radius"),
        "box_shadow": content.count("box-shadow"),
        "linear_gradient": content.count("linear-gradient"),
        "letter_spacing": content.count("letter-spacing"),
        "opacity": content.count("opacity"),
        "text_shadow": content.count("text-shadow"),
        "flex": content.count("display:flex") + content.count("display: flex"),
        "grid": content.count("display:grid") + content.count("display: grid"),
        "class_attr": content.count('class="') + content.count("class='"),
        "style_attr": content.count('style="') + content.count("style='"),
        "img_tags": content.count("<img"),
    }

    return VerifyResult(
        media_id=media_id,
        title=news_item.get("title", ""),
        content_length=len(content),
        has_images="<img" in content,
        image_count=content.count("<img"),
        style_stats=style_stats,
        raw_response=raw_text[:500],
    )


def push_loop(
    appid: str,
    secret: str,
    max_retries: int = 30,
    sleep_sec: float = 2.0,
    get_token_fn=None,
) -> dict:
    """Auto-retry loop for IP whitelist rotation (China Mobile etc.).
    
    Usage:
        result = push_loop(appid, secret, get_token_fn=get_access_token)
        if result["token"]:
            print(f"Success after {result['attempts']} attempts, IP={result['ip']}")
        else:
            print(f"All failed. Seen IPs: {result['seen_ips']}")
    
    Returns dict with keys:
        token: str or None
        ip: str or None  
        attempts: int
        seen_ips: list[str]
    """
    seen = []
    for i in range(max_retries):
        try:
            if get_token_fn is None:
                # Delayed import to avoid circular deps
                from wechat_api import get_access_token
                get_token_fn = get_access_token
            token = get_token_fn(appid, secret)
            return {
                "token": token,
                "ip": None,
                "attempts": i + 1,
                "seen_ips": seen,
            }
        except Exception as e:
            msg = str(e)
            m = re.search(r"invalid ip ([\d.]+)", msg)
            if m:
                ip = m.group(1)
                if ip not in seen:
                    seen.append(ip)
                    print(f"[{i+1}/{max_retries}] IP={ip} (not whitelisted)")
            else:
                print(f"[{i+1}/{max_retries}] {msg}")
            time.sleep(sleep_sec)

    return {
        "token": None,
        "ip": None,
        "attempts": max_retries,
        "seen_ips": seen,
    }


def detect_mmbiz_images(md_content: str) -> list:
    """Detect mmbiz.qpic.cn URLs that may be stale (from deleted drafts)."""
    pattern = r"!\[([^\]]*)\]\((https://mmbiz\.qpic\.cn/[^)]+)\)"
    matches = re.findall(pattern, md_content)
    return [{"alt": alt, "url": url} for alt, url in matches]


def republish_with_images(
    access_token: str,
    media_id: str,
    title: str,
    html: str,
    digest: str,
    thumb_media_id: Optional[str] = None,
    author: Optional[str] = None,
) -> DraftResult:
    """Delete old draft and create new one (useful when images are stale)."""
    from wechat_api import delete_draft
    try:
        delete_draft(access_token, media_id)
        print(f"  Deleted old draft: {media_id[:30]}...")
    except Exception as e:
        print(f"  Warning: delete old draft failed: {e}")
    return create_draft(access_token, title, html, digest, thumb_media_id, author=author)
