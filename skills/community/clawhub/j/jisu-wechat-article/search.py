#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章搜索（网页抓取版）

- 通过 Sogou Weixin 搜索页抓取文章列表
- 返回：标题、摘要、发布时间、公众号名称、链接
- 可选：解析中间跳转链接为微信真实文章链接
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import time
import urllib.parse
from typing import Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup

SEARCH_URL = "https://weixin.sogou.com/weixin"
DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
UA_POOL = [
    DEFAULT_UA,
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Edg/124.0.2478.97",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.3 Safari/605.1.15",
]


def _safe_text(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def _normalize_result_url(href: str) -> str:
    h = (href or "").strip()
    if h.startswith("/"):
        return "https://weixin.sogou.com" + h
    return h


def _ua_candidates(ua: str, ua_rotate: bool) -> List[str]:
    fixed = (ua or "").strip()
    if fixed:
        return [fixed]
    if ua_rotate:
        return UA_POOL[:]
    return [DEFAULT_UA]


def _request_with_retry(
    url: str,
    *,
    params: Optional[Dict[str, str]] = None,
    timeout: float = 15.0,
    allow_redirects: bool = True,
    ua_candidates: Optional[List[str]] = None,
    retries: int = 1,
    retry_delay: float = 0.3,
) -> Tuple[Optional[requests.Response], str]:
    uas = ua_candidates[:] if ua_candidates else [DEFAULT_UA]
    tries = max(1, int(retries))
    last_error = ""

    for i in range(tries):
        ua = uas[i % len(uas)]
        headers = {"User-Agent": ua, "Referer": "https://weixin.sogou.com/"}
        try:
            r = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
                allow_redirects=allow_redirects,
            )
            r.raise_for_status()
            return r, ua
        except Exception as e:
            last_error = str(e)
            if i < tries - 1:
                time.sleep(max(0.0, float(retry_delay)))
    return None, last_error


def _is_antispider_url(u: str) -> bool:
    s = (u or "").lower()
    return "/antispider/" in s or "antispider?" in s


def _is_mp_weixin_url(u: str) -> bool:
    s = (u or "").strip().lower()
    return s.startswith("http://mp.weixin.qq.com/") or s.startswith("https://mp.weixin.qq.com/")


def _parse_publish_time(li: BeautifulSoup) -> str:
    t = _safe_text((li.select_one("span.s2") or li).get_text(" ", strip=True))
    if t and "document.write" not in t:
        return t

    script_node = li.select_one("div.s-p span.s2 script")
    raw = (script_node.get_text(" ", strip=True) if script_node else "") or ""
    m = re.search(r"timeConvert\(\s*'?(\d{9,13})'?\s*\)", raw)
    if not m:
        return ""
    ts = int(m.group(1))
    if ts > 10_000_000_000:
        ts = ts // 1000
    try:
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ""


def _extract_real_from_url(u: str) -> Optional[str]:
    if not u:
        return None
    p = urllib.parse.urlparse(u)
    qs = urllib.parse.parse_qs(p.query)
    for k in ("url", "target", "target_url"):
        if k in qs and qs[k]:
            v = (qs[k][0] or "").strip()
            if v.startswith("http://") or v.startswith("https://"):
                return v
    return None


def _resolve_real_url(
    url: str,
    timeout: float = 10.0,
    ua_candidates: Optional[List[str]] = None,
    sleep_s: float = 0.2,
    retries: int = 1,
    retry_delay: float = 0.3,
) -> Optional[str]:
    direct = _extract_real_from_url(url)
    if direct:
        return direct

    r, _ = _request_with_retry(
        url,
        timeout=timeout,
        allow_redirects=False,
        ua_candidates=ua_candidates,
        retries=retries,
        retry_delay=retry_delay,
    )
    if not r:
        return None
    time.sleep(max(0.0, sleep_s))
    loc = r.headers.get("Location", "").strip()
    if not loc:
        return None
    if loc.startswith("/"):
        loc = "https://weixin.sogou.com" + loc
    out = _extract_real_from_url(loc) or loc
    return _normalize_result_url(out)


def _extract_article_content(
    url: str,
    timeout: float,
    ua_candidates: Optional[List[str]],
    max_chars: int,
    retries: int = 1,
    retry_delay: float = 0.3,
) -> Dict[str, str]:
    r, err = _request_with_retry(
        url,
        timeout=timeout,
        allow_redirects=True,
        ua_candidates=ua_candidates,
        retries=retries,
        retry_delay=retry_delay,
    )
    if not r:
        return {"content_status": "fetch_error", "content_error": err or "request_failed", "content_text": ""}

    html = r.text or ""
    if (
        "请输入图中的验证码" in html
        or "访问过于频繁" in html
        or "antispider" in html.lower()
    ):
        return {"content_status": "blocked", "content_error": "antispider", "content_text": ""}

    soup = BeautifulSoup(html, "html.parser")
    node = soup.select_one("#js_content")
    if not node:
        return {"content_status": "parse_empty", "content_error": "missing_js_content", "content_text": ""}

    text = _safe_text(node.get_text("\n", strip=True))
    if max_chars > 0 and len(text) > max_chars:
        text = text[:max_chars] + "..."

    tnode = soup.select_one("#activity-name")
    title = _safe_text(tnode.get_text(" ", strip=True) if tnode else "")
    if not title:
        ogt = soup.select_one('meta[property="og:title"]')
        if ogt:
            title = _safe_text(ogt.get("content") or "")

    return {
        "content_status": "ok",
        "content_error": "",
        "content_title": title,
        "content_text": text,
    }


def _parse_search_html(html: str, limit: int) -> List[Dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    out: List[Dict[str, str]] = []
    seen = set()

    for li in soup.select(".news-box ul.news-list > li"):
        if len(out) >= limit:
            break
        a = li.select_one("div.txt-box h3 a")
        if not a:
            continue
        title = _safe_text(a.get_text(" ", strip=True))
        href = _normalize_result_url(a.get("href") or "")
        summary = _safe_text((li.select_one("p.txt-info") or li).get_text(" ", strip=True))
        source = _safe_text(
            (li.select_one("div.s-p .all-time-y2") or li.select_one("a.account") or li.select_one("span.s-p")).get_text(" ", strip=True)
            if (li.select_one("div.s-p .all-time-y2") or li.select_one("a.account") or li.select_one("span.s-p"))
            else ""
        )
        pub = _parse_publish_time(li)

        if not title or not href:
            continue
        k = (title.lower(), href)
        if k in seen:
            continue
        seen.add(k)
        out.append(
            {
                "title": title,
                "url": href,
                "detail_url": href,
                "summary": summary,
                "publish_time": pub,
                "source_account": source,
            }
        )

    if not out:
        for a in soup.select("h3 a"):
            if len(out) >= limit:
                break
            href = _normalize_result_url(a.get("href") or "")
            title = _safe_text(a.get_text(" ", strip=True))
            if not href or not title:
                continue
            if (
                "weixin.sogou.com/link" not in href
                and "mp.weixin.qq.com" not in href
                and not href.startswith("https://weixin.sogou.com/link?")
            ):
                continue
            k = (title.lower(), href)
            if k in seen:
                continue
            seen.add(k)
            out.append(
                {
                    "title": title,
                    "url": href,
                    "detail_url": href,
                    "summary": "",
                    "publish_time": "",
                    "source_account": "",
                }
            )
    return out


def search_wechat(
    query: str,
    num: int = 10,
    resolve_url: bool = False,
    timeout: float = 15.0,
    keep_antispider: bool = False,
    fetch_content: bool = False,
    content_max_chars: int = 6000,
    ua: str = "",
    ua_rotate: bool = False,
    retries: int = 1,
    retry_delay: float = 0.3,
) -> Dict[str, object]:
    n = max(1, min(int(num), 50))
    ua_cands = _ua_candidates(ua, ua_rotate)
    params = {"type": "2", "query": query}
    r, err = _request_with_retry(
        SEARCH_URL,
        params=params,
        timeout=timeout,
        allow_redirects=True,
        ua_candidates=ua_cands,
        retries=retries,
        retry_delay=retry_delay,
    )
    if not r:
        raise RuntimeError("search_request_failed: %s" % (err or "unknown"))
    items = _parse_search_html(r.text, n)
    if resolve_url or fetch_content:
        for it in items:
            real = _resolve_real_url(
                it.get("url", ""),
                timeout=timeout,
                ua_candidates=ua_cands,
                retries=retries,
                retry_delay=retry_delay,
            ) or ""
            real_is_blocked = bool(real and _is_antispider_url(real))
            fallback_link = it.get("url", "") or ""
            if real and not real_is_blocked:
                detail_url = real
            elif real and real_is_blocked and keep_antispider:
                detail_url = real
            else:
                detail_url = fallback_link

            # 统一可用详情链接（尽量非空）
            it["detail_url"] = detail_url or fallback_link

            if resolve_url:
                if real_is_blocked:
                    it["url_real"] = real if keep_antispider else ""
                    it["resolve_status"] = "blocked"
                elif real:
                    it["url_real"] = real
                    it["resolve_status"] = "ok"
                else:
                    it["url_real"] = ""
                    it["resolve_status"] = "empty"

            if fetch_content:
                if real_is_blocked:
                    it["content_status"] = "blocked"
                    it["content_error"] = "antispider"
                    it["content_url"] = it.get("detail_url", "") or fallback_link
                    it["content_text"] = ""
                    continue

                content_url = ""
                if _is_mp_weixin_url(real):
                    content_url = real
                elif _is_mp_weixin_url(it.get("url", "")):
                    content_url = it.get("url", "")

                if not content_url:
                    it["content_status"] = "no_mp_url"
                    it["content_error"] = "no_mp_weixin_url"
                    it["content_url"] = it.get("detail_url", "") or fallback_link
                    it["content_text"] = ""
                    continue

                content_data = _extract_article_content(
                    content_url,
                    timeout=timeout,
                    ua_candidates=ua_cands,
                    max_chars=max(200, int(content_max_chars)),
                    retries=retries,
                    retry_delay=retry_delay,
                )
                it["content_url"] = content_url
                it.update(content_data)
    return {"ok": True, "query": query, "count": len(items), "items": items}


def main() -> None:
    ap = argparse.ArgumentParser(description="搜索微信公众号文章（Sogou Weixin 页面抓取）")
    ap.add_argument("query", help="搜索关键词")
    ap.add_argument("-n", "--num", type=int, default=10, help="返回条数（默认 10，最大 50）")
    ap.add_argument("-o", "--output", default="", help="输出 JSON 文件路径（可选）")
    ap.add_argument("-r", "--resolve-url", action="store_true", help="尝试解析微信真实文章链接")
    ap.add_argument("--fetch-content", action="store_true", help="尝试抓取文章正文文本")
    ap.add_argument("--content-max-chars", type=int, default=6000, help="正文文本最大字符数（默认 6000）")
    ap.add_argument("--ua", default="", help="自定义 User-Agent")
    ap.add_argument("--ua-rotate", action="store_true", help="启用内置 User-Agent 轮换")
    ap.add_argument("--retries", type=int, default=1, help="每个请求最大重试次数（默认 1）")
    ap.add_argument("--retry-delay", type=float, default=0.3, help="重试间隔秒数（默认 0.3）")
    ap.add_argument("--keep-antispider", action="store_true", help="保留 antispider 风控链接（默认不保留）")
    ap.add_argument("--timeout", type=float, default=15.0, help="请求超时秒数（默认 15）")
    args = ap.parse_args()

    try:
        res = search_wechat(
            query=args.query.strip(),
            num=args.num,
            resolve_url=bool(args.resolve_url),
            timeout=float(args.timeout),
            keep_antispider=bool(args.keep_antispider),
            fetch_content=bool(args.fetch_content),
            content_max_chars=int(args.content_max_chars),
            ua=args.ua,
            ua_rotate=bool(args.ua_rotate),
            retries=max(1, int(args.retries)),
            retry_delay=max(0.0, float(args.retry_delay)),
        )
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    text = json.dumps(res, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    print(text)


if __name__ == "__main__":
    main()

