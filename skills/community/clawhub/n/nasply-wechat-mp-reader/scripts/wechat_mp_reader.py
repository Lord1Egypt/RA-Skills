#!/usr/bin/env python3
"""Prototype WeChat Official Account reader.

Capabilities:
- parse a WeChat article URL
- fetch article HTML
- extract basic metadata
- extract article body
- try to recover account fakeid from MP backend search using mp_name/biz
- optionally list recent account articles when MP session cookie/token are available
- manage and validate MP backend session material
- start/poll QR login to capture fresh session material
- emit structured JSON
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from html import unescape
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
    from playwright.sync_api import sync_playwright
except Exception:  # pragma: no cover
    sync_playwright = None
    PlaywrightTimeoutError = Exception

try:
    import requests
except Exception as exc:  # pragma: no cover
    print(f"requests import failed: {exc}", file=sys.stderr)
    sys.exit(2)

CURRENT_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = CURRENT_DIR / "wechat_mp_reader"
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

from account_cache import get_cached_account, put_cached_account
from auth import check_session, has_session
from qr_login import login_start, login_status
from session_store import resolve_session, save_session_file

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0.0.0 Safari/537.36"
)


@dataclass
class Account:
    name: str = ""
    biz: str = ""
    fakeid: str = ""
    avatar: str = ""
    signature: str = ""


@dataclass
class Article:
    title: str = ""
    url: str = ""
    publish_time: str = ""
    publish_time_raw: str = ""
    author: str = ""
    account_name: str = ""
    content_html: str = ""
    content_markdown: str = ""
    images: list[str] = field(default_factory=list)


@dataclass
class ArticleListItem:
    title: str = ""
    url: str = ""
    publish_time: str = ""
    publish_time_raw: str = ""
    cover: str = ""
    summary: str = ""


def parse_article_url(url: str) -> dict[str, str]:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    return {
        "biz": first(query.get("__biz")),
        "mid": first(query.get("mid")),
        "idx": first(query.get("idx")),
        "sn": first(query.get("sn")),
        "url": url,
    }


def first(values: list[str] | None) -> str:
    return values[0] if values else ""


def fetch_html(url: str, timeout: int = 20) -> str:
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding or resp.encoding
    return resp.text


def is_verification_page(html: str) -> bool:
    markers = [
        "环境异常",
        "完成验证后即可继续访问",
        "当前环境异常",
        "secitptpage",
        'id="js_verify"',
        "weui-msg__title",
    ]
    return any(marker in html for marker in markers)


def should_use_article_fallback(html: str) -> bool:
    if is_verification_page(html):
        return True

    has_js_content = bool(re.search(r'''<div[^>]+id=["']js_content["']''', html, re.I))
    has_publish_time = bool(re.search(r'''id=["']publish_time["']''', html, re.I)) or "var publish_time" in html
    has_clean_title = bool(re.search(r"""var\s+msg_title\s*=\s*['\"][^'\"]+['\"]\s*;""", html))

    suspicious_markers = [
        "data-miniprogram-nickname",
        ".html(false);",
        "msg_desc = htmlDecode(",
    ]
    suspicious = any(marker in html for marker in suspicious_markers)

    if suspicious:
        return True
    if not has_js_content:
        return True
    if not has_publish_time:
        return True
    if not has_clean_title:
        return True
    return False


def extract_var(html: str, names: list[str]) -> str:
    patterns = []
    for name in names:
        patterns.extend(
            [
                rf'var\s+{re.escape(name)}\s*=\s*"(.*?)"\s*;',
                rf"var\s+{re.escape(name)}\s*=\s*'(.*?)'\s*;",
                rf'{re.escape(name)}\s*[:=]\s*"(.*?)"',
                rf"{re.escape(name)}\s*[:=]\s*'(.*?)'",
            ]
        )
    for pattern in patterns:
        m = re.search(pattern, html, re.S)
        if m:
            return unescape(m.group(1)).strip()
    return ""


def extract_publish_time(html: str) -> str:
    m = re.search(r"var\s+publish_time\s*=\s*['\"]?(\d{9,})['\"]?", html)
    return m.group(1) if m else ""


def format_publish_time(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if text.isdigit() and len(text) >= 9:
        try:
            dt = datetime.fromtimestamp(int(text))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return text
    return text


def extract_body_html(html: str) -> str:
    patterns = [
        r'<div[^>]+id="js_content"[^>]*>(.*?)</div>\\s*<script',
        r"<div[^>]+id='js_content'[^>]*>(.*?)</div>\\s*<script",
        r'<div[^>]+id="js_content"[^>]*>(.*?)</div>',
        r"<div[^>]+id='js_content'[^>]*>(.*?)</div>",
    ]
    for pattern in patterns:
        m = re.search(pattern, html, re.S | re.I)
        if m:
            return m.group(1).strip()
    return ""


def strip_tags(value: str) -> str:
    value = re.sub(r"<script[\s\S]*?</script>", "", value, flags=re.I)
    value = re.sub(r"<style[\s\S]*?</style>", "", value, flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    value = value.replace("\xa0", " ")
    value = re.sub(r"[ \t]+\n", "\n", value)
    value = re.sub(r"\n[ \t]+", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return unescape(value).strip()


def html_to_markdownish(body_html: str) -> str:
    text = body_html
    text = re.sub(r"<(strong|b)[^>]*>(.*?)</\1>", r"**\2**", text, flags=re.I | re.S)
    text = re.sub(r"<(em|i)[^>]*>(.*?)</\1>", r"*\2*", text, flags=re.I | re.S)
    text = re.sub(
        r'<img[^>]+(?:data-src|src)="([^"]+)"[^>]*>',
        lambda m: f'\n\n![]({m.group(1).strip()})\n\n',
        text,
        flags=re.I,
    )
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</p\s*>", "\n\n", text, flags=re.I)
    text = re.sub(r"<p[^>]*>", "", text, flags=re.I)
    text = re.sub(r"</div\s*>", "\n\n", text, flags=re.I)
    text = re.sub(r"<div[^>]*>", "", text, flags=re.I)
    text = re.sub(r"</section\s*>", "\n\n", text, flags=re.I)
    text = re.sub(r"<section[^>]*>", "", text, flags=re.I)
    text = re.sub(r"<blockquote[^>]*>", "\n> ", text, flags=re.I)
    text = re.sub(r"</blockquote\s*>", "\n\n", text, flags=re.I)
    text = re.sub(r"<ul[^>]*>", "\n", text, flags=re.I)
    text = re.sub(r"</ul\s*>", "\n", text, flags=re.I)
    text = re.sub(r"<ol[^>]*>", "\n", text, flags=re.I)
    text = re.sub(r"</ol\s*>", "\n", text, flags=re.I)
    text = re.sub(r"<li[^>]*>", "\n- ", text, flags=re.I)
    text = re.sub(r"</li\s*>", "", text, flags=re.I)
    text = re.sub(r"<h[1-6][^>]*>", "\n## ", text, flags=re.I)
    text = re.sub(r"</h[1-6]>", "\n\n", text, flags=re.I)
    text = strip_tags(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n-\s*\n", "\n- ", text)
    text = re.sub(r"\n>\s*\n", "\n> ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()
    lines = text.splitlines()
    while lines:
        first = lines[0].strip()
        if not first:
            lines.pop(0)
            continue
        if re.fullmatch(r">?\s*[：:]+.*", first):
            lines.pop(0)
            continue
        if re.fullmatch(r">\s*[^一-鿿A-Za-z0-9]{0,4}", first):
            lines.pop(0)
            continue
        break
    text = "\n".join(lines).strip()
    return text

def extract_images(body_html: str) -> list[str]:
    urls = []
    for m in re.finditer(r'<img[^>]+(?:data-src|src)="(.*?)"', body_html, re.I):
        url = m.group(1).strip()
        if url and url not in urls:
            urls.append(url)
    return urls


def fetch_article_via_playwright(url: str, timeout: int = 20000) -> dict[str, Any]:
    if sync_playwright is None:
        raise RuntimeError("playwright not available")

    page = None
    browser = None
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=True)
        try:
            page = browser.new_page(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                viewport={"width": 1440, "height": 2200},
            )
            page.goto(url, wait_until="domcontentloaded", timeout=timeout)
            try:
                page.wait_for_selector("#js_content", timeout=8000)
            except PlaywrightTimeoutError:
                pass
            page.wait_for_timeout(1200)
            html = page.content()

            content_html = ""
            try:
                content_html = page.locator("#js_content").inner_html(timeout=3000).strip()
            except Exception:
                pass

            def js_eval(expr: str) -> str:
                try:
                    value = page.evaluate(expr)
                    return (value or "").strip() if isinstance(value, str) else str(value or "").strip()
                except Exception:
                    return ""

            title = (
                js_eval("() => (typeof msg_title !== 'undefined' ? msg_title : '')")
                or js_eval("() => document.querySelector('#activity-name')?.textContent || ''")
                or extract_var(html, ["msg_title", "title"])
            )
            author = (
                js_eval("() => (typeof nickname !== 'undefined' ? nickname : '')")
                or js_eval("() => (typeof user_name !== 'undefined' ? user_name : '')")
                or extract_var(html, ["nickname", "user_name", "account_name", "author", "ori_name"])
            )
            publish_time = (
                js_eval("() => { const el = document.querySelector('#publish_time'); return (el && el.textContent) ? el.textContent.trim() : ''; }")
                or js_eval("() => (typeof globalThis.publish_time === 'number' || typeof globalThis.publish_time === 'string' ? String(globalThis.publish_time) : '')")
                or extract_publish_time(html)
            )
            biz = js_eval("() => (typeof biz !== 'undefined' ? biz : '')") or extract_var(html, ["biz"])
            logo = (
                js_eval("() => (typeof ori_head_img_url !== 'undefined' ? ori_head_img_url : '')")
                or extract_var(html, ["ori_head_img_url", "hd_head_img"])
            )

            return {
                "title": title,
                "author": author,
                "publish_time": publish_time,
                "content": content_html,
                "mp_info": {
                    "mp_name": author,
                    "biz": biz,
                    "logo": logo,
                },
                "source": "local-playwright",
            }
        finally:
            if page is not None:
                try:
                    page.close()
                except Exception:
                    pass
            if browser is not None:
                try:
                    browser.close()
                except Exception:
                    pass



def fetch_article_details(url: str, timeout: int = 20) -> tuple[str, dict[str, Any], list[str]]:
    warnings: list[str] = []
    html = fetch_html(url, timeout=timeout)
    fallback: dict[str, Any] = {}
    if should_use_article_fallback(html):
        try:
            fallback = fetch_article_via_playwright(url, timeout=timeout * 1000)
            warnings.append("http fetch looked non-canonical for wechat article; used local Playwright browser fallback")
        except Exception as exc:
            warnings.append(f"article fallback failed: local Playwright failed: {exc}")
    return html, fallback, warnings


def search_account_via_mp_backend(name: str, session_cfg: dict[str, str], limit: int = 5, offset: int = 0) -> dict[str, Any]:
    url = "https://mp.weixin.qq.com/cgi-bin/searchbiz"
    params = {
        "action": "search_biz",
        "begin": offset,
        "count": limit,
        "query": name,
        "token": session_cfg["token"],
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
    }
    headers = {
        "Cookie": session_cfg["cookie"],
        "User-Agent": USER_AGENT,
        "Referer": "https://mp.weixin.qq.com/",
    }
    resp = requests.get(url, params=params, headers=headers, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data.get("publish_page"), str):
        try:
            data["publish_page"] = json.loads(data["publish_page"])
        except Exception:
            pass
    return data


def extract_search_candidates(mp_data: dict[str, Any]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    pages = []

    top_list = mp_data.get("list")
    if isinstance(top_list, list):
        pages.extend(top_list)

    publish_page = mp_data.get("publish_page")
    if isinstance(publish_page, dict):
        for key in ("list", "publish_list", "biz_list"):
            value = publish_page.get(key)
            if isinstance(value, list):
                pages.extend(value)

    for item in pages:
        candidates.append(
            {
                "name": item.get("nickname") or item.get("name") or item.get("username") or "",
                "fakeid": item.get("fakeid") or item.get("fake_id") or "",
                "biz": item.get("biz") or item.get("alias") or "",
                "avatar": item.get("round_head_img") or item.get("avatar") or item.get("headimgurl") or "",
                "signature": item.get("signature") or item.get("desc") or "",
            }
        )
    return candidates


def score_candidate(candidate: dict[str, Any], account: Account) -> int:
    score = 0
    cand_name = (candidate.get("name") or "").strip().lower()
    acc_name = (account.name or "").strip().lower()
    cand_biz = (candidate.get("biz") or "").strip()
    acc_biz = (account.biz or "").strip()

    if acc_name and cand_name == acc_name:
        score += 100
    elif acc_name and acc_name in cand_name:
        score += 60

    if acc_biz and cand_biz and cand_biz == acc_biz:
        score += 120

    if candidate.get("fakeid"):
        score += 5

    return score


def enrich_account_with_search(account: Account, session_cfg: dict[str, str], limit: int = 10) -> tuple[Account, list[dict[str, Any]], str]:
    if not has_session(session_cfg):
        return account, [], "missing mp session"
    if not account.name:
        return account, [], "missing account name"

    data = search_account_via_mp_backend(account.name, session_cfg, limit=limit)
    base_resp = data.get("base_resp") or {}
    if base_resp.get("ret") not in (0, None):
        return account, [], base_resp.get("err_msg", f"ret={base_resp.get('ret')}")

    candidates = extract_search_candidates(data)
    if not candidates:
        return account, [], "no candidates"

    ranked = sorted(candidates, key=lambda item: score_candidate(item, account), reverse=True)
    best = ranked[0]
    if score_candidate(best, account) <= 0:
        return account, ranked, "no confident match"

    if not account.fakeid:
        account.fakeid = best.get("fakeid", "")
    if not account.avatar:
        account.avatar = best.get("avatar", "")
    if not account.signature:
        account.signature = best.get("signature", "")
    if not account.name:
        account.name = best.get("name", "")
    return account, ranked, "matched"


def list_articles_via_mp_backend(fakeid: str, session_cfg: dict[str, str], count: int = 5, begin: int = 0) -> dict[str, Any]:
    url = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish"
    params = {
        "sub": "list",
        "sub_action": "list_ex",
        "begin": begin,
        "count": count,
        "fakeid": fakeid,
        "token": session_cfg["token"],
        "lang": "zh_CN",
        "f": "json",
        "ajax": 1,
    }
    headers = {
        "Cookie": session_cfg["cookie"],
        "User-Agent": USER_AGENT,
        "Referer": "https://mp.weixin.qq.com/",
    }
    resp = requests.get(url, params=params, headers=headers, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data.get("publish_page"), str):
        try:
            data["publish_page"] = json.loads(data["publish_page"])
        except Exception:
            pass
    return data


def extract_article_list(mp_data: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    publish_page = mp_data.get("publish_page") or {}
    publish_list = publish_page.get("publish_list") if isinstance(publish_page, dict) else []
    if not isinstance(publish_list, list):
        return items
    for block in publish_list:
        publish_info = block.get("publish_info")
        if isinstance(publish_info, str):
            try:
                publish_info = json.loads(publish_info)
            except Exception:
                continue
        if not isinstance(publish_info, dict):
            continue
        appmsgex = publish_info.get("appmsgex") or []
        if not isinstance(appmsgex, list):
            continue
        for art in appmsgex:
            items.append(
                asdict(
                    ArticleListItem(
                        title=art.get("title", ""),
                        url=art.get("link", ""),
                        publish_time=format_publish_time(art.get("update_time", "")),
                        publish_time_raw=str(art.get("update_time", "") or ""),
                        cover=art.get("cover", ""),
                        summary=art.get("digest", ""),
                    )
                )
            )
    return items


def build_session_status(session_cfg: dict[str, str]) -> dict[str, Any]:
    return check_session(session_cfg)


def find_matching_article_item(items: list[dict[str, Any]], url: str) -> dict[str, Any] | None:
    for item in items:
        if (item.get("url") or "").strip() == url.strip():
            return item
    return None


def resolve_from_article(url: str, with_account_articles: bool = False, list_count: int = 5, session_path: str | None = None) -> dict[str, Any]:
    html, fallback_article, warnings = fetch_article_details(url)
    parsed_url = parse_article_url(url)
    body_html = extract_body_html(html)
    session_cfg = resolve_session(session_path)
    session_status = build_session_status(session_cfg)

    fallback_mp = fallback_article.get("mp_info") or {}

    html_account_name = extract_var(html, ["nickname", "user_name", "account_name"])
    if html_account_name.startswith("data-"):
        html_account_name = ""

    html_title = extract_var(html, ["msg_title", "title"])
    if html_title and ("var msg_desc" in html_title or "html(false)" in html_title):
        html_title = ""

    account = Account(
        name=fallback_mp.get("mp_name", "") or html_account_name or fallback_article.get("author", ""),
        biz=parsed_url.get("biz", "") or fallback_mp.get("biz", ""),
        fakeid=extract_var(html, ["fakeid"]),
        avatar=fallback_mp.get("logo", "") or extract_var(html, ["ori_head_img_url", "hd_head_img"]),
        signature=extract_var(html, ["signature", "desc"]),
    )

    cached = get_cached_account(account.biz, account.name)
    if cached:
        if not account.fakeid:
            account.fakeid = str(cached.get("fakeid", "") or "")
        if not account.avatar:
            account.avatar = str(cached.get("avatar", "") or "")
        if not account.signature:
            account.signature = str(cached.get("signature", "") or "")
        if not account.name:
            account.name = str(cached.get("name", "") or "")
        if not account.biz:
            account.biz = str(cached.get("biz", "") or "")

    fallback_content = fallback_article.get("content", "")
    if not body_html and fallback_content and fallback_content != "DELETED":
        body_html = fallback_content

    article_publish_time_raw = str(fallback_article.get("publish_time", "") or extract_publish_time(html) or "")
    article = Article(
        title=fallback_article.get("title", "") or html_title,
        url=url,
        publish_time=format_publish_time(article_publish_time_raw),
        publish_time_raw=article_publish_time_raw,
        author=fallback_article.get("author", "") or extract_var(html, ["author", "ori_name"]),
        account_name=account.name,
        content_html=body_html,
        content_markdown=html_to_markdownish(body_html) if body_html else "",
        images=extract_images(body_html),
    )
    article_list: list[dict[str, Any]] = []
    search_candidates: list[dict[str, Any]] = []

    if not account.fakeid and session_status["valid"]:
        try:
            account, search_candidates, match_status = enrich_account_with_search(account, session_cfg)
            if match_status != "matched":
                warnings.append(f"fakeid recovery status: {match_status}")
        except Exception as exc:
            warnings.append(f"fakeid recovery failed: {exc}")
    elif not account.fakeid and session_status["present"] and not session_status["valid"]:
        warnings.append(f"session invalid: {session_status['reason']}")

    if account.fakeid or account.biz or account.name:
        try:
            put_cached_account(asdict(account))
        except Exception:
            pass

    if with_account_articles:
        if account.fakeid and session_status["valid"]:
            try:
                raw_list = list_articles_via_mp_backend(account.fakeid, session_cfg, count=list_count)
                base_resp = raw_list.get("base_resp") or {}
                if base_resp.get("ret") not in (0, None):
                    warnings.append(f"account article listing failed: {base_resp.get('err_msg', base_resp)}")
                else:
                    article_list = extract_article_list(raw_list)
            except Exception as exc:
                warnings.append(f"account article listing failed: {exc}")
        else:
            warnings.append(
                "account article listing requires fakeid plus a valid WECHAT_MP_COOKIE/WECHAT_MP_TOKEN or saved session"
            )

    matched_item = find_matching_article_item(article_list, url)
    if matched_item:
        if not article.title:
            article.title = matched_item.get("title", "")
        if not article.publish_time:
            article.publish_time = format_publish_time(matched_item.get("publish_time", ""))
        if not article.publish_time_raw:
            article.publish_time_raw = str(matched_item.get("publish_time_raw", "") or matched_item.get("publish_time", "") or "")
        if not account.name:
            account.name = article.author or matched_item.get("title", "")
        article.account_name = account.name

    return {
        "mode": "article-url",
        "session": session_status,
        "account": asdict(account),
        "article": asdict(article),
        "search_candidates": search_candidates,
        "account_articles": article_list,
        "url_parts": parsed_url,
        "warnings": warnings,
    }


def search_account(name: str, limit: int = 5, session_path: str | None = None) -> dict[str, Any]:
    session_cfg = resolve_session(session_path)
    session_status = build_session_status(session_cfg)
    if not session_status["present"]:
        return {
            "mode": "account-name",
            "session": session_status,
            "query": name,
            "supported": False,
            "message": (
                "Search by account name requires WECHAT_MP_COOKIE and WECHAT_MP_TOKEN, "
                "or a saved session file. Prefer passing any article URL from the target account first."
            ),
            "candidates": [],
        }
    if not session_status["valid"]:
        return {
            "mode": "account-name",
            "session": session_status,
            "query": name,
            "supported": False,
            "message": f"session invalid: {session_status['reason']}",
            "candidates": [],
        }
    try:
        data = search_account_via_mp_backend(name, session_cfg, limit=limit)
        return {
            "mode": "account-name",
            "session": session_status,
            "query": name,
            "supported": True,
            "candidates": extract_search_candidates(data),
            "raw_base_resp": data.get("base_resp", {}),
        }
    except Exception as exc:
        return {
            "mode": "account-name",
            "session": session_status,
            "query": name,
            "supported": False,
            "message": str(exc),
            "candidates": [],
        }


def session_command(action: str, session_path: str | None = None) -> dict[str, Any]:
    session_cfg = resolve_session(session_path)
    if action == "check":
        return {
            "mode": "session",
            "action": action,
            "session": build_session_status(session_cfg),
        }
    if action == "show":
        return {
            "mode": "session",
            "action": action,
            "session": {
                **build_session_status(session_cfg),
                "cookie_len": len(session_cfg.get("cookie", "")),
                "token_len": len(session_cfg.get("token", "")),
            },
        }
    if action == "save":
        if not has_session(session_cfg):
            return {
                "mode": "session",
                "action": action,
                "saved": False,
                "message": "no session found in env or session file",
            }
        path = save_session_file(session_cfg, session_path)
        return {
            "mode": "session",
            "action": action,
            "saved": True,
            "path": path,
            "session": build_session_status(session_cfg),
        }
    if action == "login-start":
        return {
            "mode": "session",
            "action": action,
            **login_start(),
        }
    if action == "login-status":
        return {
            "mode": "session",
            "action": action,
            **login_status(session_path=session_path),
        }
    return {"mode": "session", "action": action, "error": "unknown action"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="WeChat MP reader prototype")
    parser.add_argument("--session-path", default=None, help="Optional session file path")
    sub = parser.add_subparsers(dest="command", required=True)

    p_article = sub.add_parser("article", help="Resolve and extract from article URL")
    p_article.add_argument("url", help="WeChat article URL")
    p_article.add_argument("--with-account-articles", action="store_true", help="Also try to list recent account articles")
    p_article.add_argument("--list-count", type=int, default=5, help="How many account articles to request")

    p_search = sub.add_parser("search", help="Search by account name")
    p_search.add_argument("name", help="Account name or keyword")
    p_search.add_argument("--limit", type=int, default=5, help="How many candidates to request")

    p_session = sub.add_parser("session", help="Inspect or persist MP backend session")
    p_session.add_argument(
        "action",
        choices=["check", "show", "save", "login-start", "login-status"],
        help="Session action",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "article":
        result = resolve_from_article(
            args.url,
            with_account_articles=args.with_account_articles,
            list_count=args.list_count,
            session_path=args.session_path,
        )
    elif args.command == "search":
        result = search_account(args.name, limit=args.limit, session_path=args.session_path)
    elif args.command == "session":
        result = session_command(args.action, session_path=args.session_path)
    else:  # pragma: no cover
        parser.error("unknown command")
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
