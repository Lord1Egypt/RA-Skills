#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
news-cn：抓取新闻/资讯列表页 HTML，提取站内文章链接；可选 RSS/Atom（部分源不稳定）。
digest 子命令：抓取后输出按来源分组的 Markdown（标题+链接简报，不上传任何数据至外部 LLM）。

依赖：pip install beautifulsoup4（网页模式必填）
"""

from __future__ import annotations

import html
import ipaddress
import json
import os
import re
import socket
import sys
import gzip
import urllib.request
import ssl
from datetime import date
from urllib.parse import urljoin, urlparse
from typing import Any, Dict, List, Optional, Tuple
from xml.etree import ElementTree as ET

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None  # type: ignore

# 预设「列表页」网址（键 -> 配置）。常见中文科技/资讯门户首页或频道。
# 若某站改版导致链接变少，可在请求 JSON 的 pages 里传完整 URL，或用 selector 收窄解析区域。
DEFAULT_PAGES: Dict[str, Dict[str, Any]] = {
    # 原 /information/tech 已 404，改为快讯列表（含 /p/ 深度稿链接）
    "36kr": {"url": "https://www.36kr.com/newsflashes"},
    "jiqizhixin": {"url": "https://www.jiqizhixin.com"},
    "qbitai": {"url": "https://www.qbitai.com"},
    "ithome": {"url": "https://www.ithome.com"},
    # 网易：频道首页（文章链接多在 www.163.com / dy 等子域，已做同系域名匹配）
    "netease_news": {"url": "https://news.163.com/"},
    "netease_tech": {"url": "https://tech.163.com/"},
    # 新浪：新闻 / 科技频道
    "sina_news": {"url": "https://news.sina.com.cn/"},
    "sina_tech": {"url": "https://tech.sina.com.cn/"},
    "guancha": {"url": "https://www.guancha.cn"},
    "thepaper": {"url": "https://www.thepaper.cn"},
    "solidot": {"url": "https://www.solidot.org"},
    "techcrunch": {"url": "https://techcrunch.com"},
    "theverge": {"url": "https://www.theverge.com"},
}

# 备用：RSS（显式 mode=rss 时使用）
# 说明：BBC 简体中文 feed（…/simp/rss.xml）在不少网络环境下无法连接，
# 默认键 bbc_zh 指向繁体主 feed（…/trad/rss.xml），内容与「BBC 中文」一致。
# 大陆部分地区对 bbci.co.uk 整体不可用，请改用 solidot_rss 或网页模式。
DEFAULT_FEEDS: Dict[str, str] = {
    "bbc_zh": "https://feeds.bbci.co.uk/zhongwen/trad/rss.xml",
    "bbc_zh_simp": "https://feeds.bbci.co.uk/zhongwen/simp/rss.xml",
    "solidot_rss": "https://www.solidot.org/index.rss",
}

_SKIP_TITLE_RE = re.compile(
    r"^(登录|登\s*录|注册|更多>>?|首页|设为首页|关于我们|联系我们|搜索|下载\s*APP|关注微信)",
    re.I,
)


def _host_key(host: str) -> str:
    h = (host or "").lower()
    if h.startswith("www."):
        h = h[4:]
    return h


def _local_tag(tag: str) -> str:
    if tag.startswith("{"):
        return tag.split("}", 1)[1]
    return tag


def _text(el: Optional[ET.Element]) -> str:
    if el is None:
        return ""
    parts = [el.text or ""]
    for c in el:
        parts.append(_text(c))
        parts.append(c.tail or "")
    return "".join(parts).strip()


def _find_children(parent: ET.Element, name: str) -> List[ET.Element]:
    return [c for c in list(parent) if _local_tag(c.tag) == name]


def _first_child_text(parent: ET.Element, name: str) -> str:
    for c in list(parent):
        if _local_tag(c.tag) == name:
            return _text(c)
    return ""


def _strip_html(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def _normalize_title(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip()).lower()


def _decode_html_bytes(b: bytes) -> str:
    for enc in ("utf-8", "utf-8-sig", "gb18030", "gbk", "latin-1"):
        try:
            return b.decode(enc).lstrip("\ufeff")
        except Exception:
            continue
    return b.decode("utf-8", errors="replace")


def _decode_xml_bytes(b: bytes) -> str:
    for enc in ("utf-8", "utf-8-sig", "gb18030", "gbk", "latin-1"):
        try:
            t = b.decode(enc).lstrip("\ufeff")
            return t
        except Exception:
            continue
    return b.decode("utf-8", errors="replace")


def _env_on(name: str, default: str = "1") -> bool:
    v = os.environ.get(name, default).strip().lower()
    return v not in ("0", "false", "no", "off")


def _host_allowed_by_env(host: str) -> bool:
    """
    可选域名白名单：
    - NEWS_CN_ALLOW_HOSTS="36kr.com,ithome.com,.sina.com.cn"
    - 支持精确匹配与前缀点后缀匹配（.example.com 表示子域）
    """
    raw = os.environ.get("NEWS_CN_ALLOW_HOSTS", "").strip()
    if not raw:
        return True
    h = (host or "").lower().strip(".")
    if not h:
        return False
    for item in raw.split(","):
        p = item.strip().lower()
        if not p:
            continue
        if p.startswith("."):
            sfx = p[1:]
            if sfx and (h == sfx or h.endswith("." + sfx)):
                return True
        else:
            if h == p or h.endswith("." + p):
                return True
    return False


def _resolve_host_ips(host: str) -> List[str]:
    out: List[str] = []
    try:
        infos = socket.getaddrinfo(host, None)
    except Exception:
        return out
    for info in infos:
        try:
            ip = info[4][0]
        except Exception:
            continue
        if ip and ip not in out:
            out.append(ip)
    return out


def _ip_is_privateish(ip: str) -> bool:
    try:
        a = ipaddress.ip_address(ip)
    except Exception:
        return True
    return bool(
        a.is_loopback
        or a.is_private
        or a.is_link_local
        or a.is_multicast
        or a.is_reserved
        or a.is_unspecified
    )


def _validate_remote_url(url: str) -> None:
    """
    URL 访问安全检查：
    - 仅 http/https
    - 可选白名单 NEWS_CN_ALLOW_HOSTS
    - 默认拦截本机/私网/链路本地等地址（NEWS_CN_BLOCK_PRIVATE=0 可关闭）
    """
    p = urlparse(url)
    if p.scheme not in ("http", "https"):
        raise ValueError("only http(s) URLs allowed")
    host = (p.hostname or "").strip().lower()
    if not host:
        raise ValueError("url host is empty")
    if not _host_allowed_by_env(host):
        raise ValueError("host not allowed by NEWS_CN_ALLOW_HOSTS: %s" % host)
    if not _env_on("NEWS_CN_BLOCK_PRIVATE", "1"):
        return
    if host == "localhost" or host.endswith(".localhost"):
        raise ValueError("blocked private/local host: %s" % host)
    ips = _resolve_host_ips(host)
    if not ips:
        # 解析失败时保持安全默认，避免未知主机绕过
        raise ValueError("dns resolve failed for host: %s" % host)
    bad = [ip for ip in ips if _ip_is_privateish(ip)]
    if bad:
        raise ValueError("blocked private/local address for host %s: %s" % (host, ",".join(bad)))


def _fetch_url(url: str, timeout: float, max_bytes: int = 3_500_000) -> bytes:
    _validate_remote_url(url)
    ua = os.environ.get(
        "NEWS_CN_UA",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    )
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            # 避免 urllib 不解压 gzip 导致乱解析
            "Accept-Encoding": "identity",
        },
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        data = resp.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ValueError("response too large (max_bytes=%s)" % max_bytes)
    # 少数服务仍返回 gzip
    if len(data) >= 2 and data[0] == 0x1F and data[1] == 0x8B:
        try:
            data = gzip.decompress(data)
        except Exception:
            pass
    return data


def _parse_feed(xml_bytes: bytes, feed_label: str) -> List[Dict[str, str]]:
    text = _decode_xml_bytes(xml_bytes)
    root = ET.fromstring(text)
    root_name = _local_tag(root.tag)
    out: List[Dict[str, str]] = []

    if root_name == "rss":
        channel = _find_children(root, "channel")
        ch = channel[0] if channel else root
        for item in _find_children(ch, "item"):
            title = _strip_html(_first_child_text(item, "title"))
            link = _strip_html(_first_child_text(item, "link")).split()[0] if _first_child_text(item, "link") else ""
            if not link:
                link = _strip_html(_first_child_text(item, "guid")).split()[0] if _first_child_text(item, "guid") else ""
            desc = _strip_html(_first_child_text(item, "description"))
            pub = _strip_html(_first_child_text(item, "pubDate"))
            if title:
                out.append(
                    {
                        "feed": feed_label,
                        "title": title,
                        "link": link,
                        "summary": desc[:2000] if desc else "",
                        "pub": pub,
                    }
                )
        return out

    if root_name == "feed":
        for entry in _find_children(root, "entry"):
            title = _strip_html(_first_child_text(entry, "title"))
            link = ""
            for c in list(entry):
                if _local_tag(c.tag) == "link":
                    link = (c.attrib.get("href") or "").strip()
                    if link:
                        break
            if not link:
                lid = _first_child_text(entry, "id")
                link = _strip_html(lid).split()[0] if lid else ""
            summ = _first_child_text(entry, "summary")
            if not summ:
                summ = _first_child_text(entry, "content")
            desc = _strip_html(summ)
            pub = _strip_html(_first_child_text(entry, "updated") or _first_child_text(entry, "published"))
            if title:
                out.append(
                    {
                        "feed": feed_label,
                        "title": title,
                        "link": link,
                        "summary": desc[:2000] if desc else "",
                        "pub": pub,
                    }
                )
        return out

    raise ValueError("unsupported feed root: %s (expect rss or feed)" % root_name)


def _resolve_page(key_or_url: str) -> Tuple[str, str, Optional[str]]:
    s = (key_or_url or "").strip()
    if not s:
        raise ValueError("empty page key or url")
    if s.startswith("http://") or s.startswith("https://"):
        return s, s, None
    if s in DEFAULT_PAGES:
        cfg = DEFAULT_PAGES[s]
        sel = cfg.get("selector")
        if isinstance(sel, str) and sel.strip():
            return str(cfg["url"]), s, sel.strip()
        return str(cfg["url"]), s, None
    raise ValueError("unknown page key: %s (use list or pass full URL)" % s)


def _resolve_feed_url(key_or_url: str) -> Tuple[str, str]:
    s = (key_or_url or "").strip()
    if not s:
        raise ValueError("empty feed key or url")
    if s.startswith("http://") or s.startswith("https://"):
        return s, s
    if s in DEFAULT_FEEDS:
        return DEFAULT_FEEDS[s], s
    raise ValueError("unknown feed key: %s" % s)


def _same_site(listing_host: str, link_host: str) -> bool:
    return _host_key(listing_host) == _host_key(link_host)


def _netease_family(host: str) -> bool:
    h = (host or "").lower()
    return h == "163.com" or h.endswith(".163.com")


def _sina_family(host: str) -> bool:
    h = (host or "").lower()
    return "sina.com.cn" in h or h.endswith(".sina.cn")


def _same_site_relaxed(listing_host: str, link_host: str) -> bool:
    """同站或网易系 / 新浪系互相跳转（列表页与正文常见不同子域）。"""
    if _same_site(listing_host, link_host):
        return True
    if _netease_family(listing_host) and _netease_family(link_host):
        return True
    if _sina_family(listing_host) and _sina_family(link_host):
        return True
    return False


def _path_looks_like_article(path: str, link_netloc: str) -> bool:
    if not path or path == "/":
        return False
    # 过滤常见非文章路径
    low = path.lower()
    noise = (
        "/user/",
        "/login",
        "/register",
        "/about",
        "/contact",
        "/tag/",
        "/topic/",
        "/channel/",
        "/comment/",
        ".css",
        ".js",
        "/rss",
    )
    if any(x in low for x in noise):
        return False
    depth = len([p for p in path.split("/") if p])
    if depth >= 2:
        return True
    if "ithome" in link_netloc and re.search(r"/\d+/\d+/\d+\.htm", low):
        return True
    if "36kr" in link_netloc and "/p/" in low:
        return True
    if "jiqizhixin" in link_netloc and "/articles/" in low:
        return True
    if "qbitai" in link_netloc and "/20" in low:
        return True
    if "solidot" in link_netloc and "/story" in low:
        return True
    if "techcrunch" in link_netloc and re.search(r"/20\d{2}/", low):
        return True
    if "theverge" in link_netloc and ("/news/" in low or re.search(r"/20\d{2}/", low)):
        return True
    if "guancha" in link_netloc and len(path) > 15:
        return True
    if "thepaper" in link_netloc and "/news/" in low:
        return True
    if _netease_family(link_netloc):
        if "/dy/article/" in low or "/article/" in low or "/war/article/" in low:
            return True
        if low.endswith(".html") and "/v/video" not in low and depth >= 2:
            return True
    if _sina_family(link_netloc):
        if ".shtml" in low or "/doc-" in low or "/doc/" in low:
            return True
        if re.search(r"/\d{4}-\d{2}-\d{2}/", low) and depth >= 4:
            return True
        if "/c/" in low and "iframe" not in low and depth >= 3 and len(low) > 25:
            return True
    return depth >= 1 and len(path) > 30


def _extract_from_listing_page(
    listing_url: str,
    html_bytes: bytes,
    source_label: str,
    per_page: int,
    css_selector: Optional[str],
) -> List[Dict[str, str]]:
    if BeautifulSoup is None:
        raise RuntimeError("web page mode requires: pip install beautifulsoup4")

    html_text = _decode_html_bytes(html_bytes)
    soup = BeautifulSoup(html_text, "html.parser")
    base_host = urlparse(listing_url).netloc
    root = soup
    if css_selector:
        found = soup.select_one(css_selector)
        if found:
            root = found

    items: List[Dict[str, str]] = []
    seen_url = set()

    for a in root.find_all("a", href=True):
        if len(items) >= per_page:
            break
        href = (a.get("href") or "").strip()
        if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue
        full = urljoin(listing_url, href)
        p = urlparse(full)
        if p.scheme not in ("http", "https"):
            continue
        if not _same_site_relaxed(base_host, p.netloc):
            continue
        title = a.get_text(separator=" ", strip=True)
        title = re.sub(r"\s+", " ", title).strip()
        if len(title) < 8 or len(title) > 220:
            continue
        if _SKIP_TITLE_RE.match(title):
            continue
        if not _path_looks_like_article(p.path or "/", p.netloc):
            continue
        norm = full.split("#")[0]
        if norm in seen_url:
            continue
        seen_url.add(norm)
        items.append(
            {
                "feed": source_label,
                "title": title,
                "link": norm,
                "summary": "",
                "pub": "",
            }
        )
    return items


def _read_json_arg() -> Dict[str, Any]:
    raw = sys.argv[2] if len(sys.argv) >= 3 else ""
    if isinstance(raw, str):
        rs = raw.strip()
        if rs == "-":
            raw = sys.stdin.read()
        elif rs.startswith("@") and len(rs) > 1:
            with open(rs[1:], "r", encoding="utf-8") as f:
                raw = f.read()
    if not raw.strip():
        return {}
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise ValueError("JSON must be an object")
    return obj


def _items_to_markdown(items: List[Dict[str, str]], title: str) -> str:
    lines = ["## %s" % title, ""]
    for it in items:
        t = it.get("title") or ""
        u = it.get("link") or ""
        src = it.get("feed") or ""
        summ = (it.get("summary") or "")[:300]
        if u:
            lines.append("- **[%s](%s)** — `%s`" % (t, u, src))
        else:
            lines.append("- **%s** — `%s`" % (t, src))
        if summ:
            lines.append("  - %s" % summ)
    return "\n".join(lines) + "\n"


def cmd_list() -> None:
    obj = {
        "pages": [{"key": k, "url": v["url"], "selector": v.get("selector")} for k, v in sorted(DEFAULT_PAGES.items())],
        "feeds_rss": [{"key": k, "url": v} for k, v in sorted(DEFAULT_FEEDS.items())],
    }
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _cmd_fetch_pages(req: Dict[str, Any]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    pages = req.get("pages")
    if not isinstance(pages, list) or not pages:
        pages = ["netease_news", "sina_news", "36kr", "ithome"]
    try:
        per_page = int(req.get("per_page", req.get("per_feed", 12)))
    except Exception:
        per_page = 12
    per_page = max(1, min(per_page, 40))
    try:
        timeout = float(req.get("timeout", 30))
    except Exception:
        timeout = 30.0
    try:
        max_bytes = int(req.get("max_html_bytes", 3_500_000))
    except Exception:
        max_bytes = 3_500_000

    all_items: List[Dict[str, str]] = []
    errors: List[Dict[str, str]] = []

    for key in pages:
        key_s = str(key).strip()
        try:
            if isinstance(key, dict):
                pu = str(key.get("url") or "").strip()
                lab = str(key.get("key") or pu).strip() or pu
                sel = key.get("selector")
                sel_s = str(sel).strip() if sel else None
                if not pu.startswith("http"):
                    raise ValueError("object page entry needs url")
                listing_url, label, selector = pu, lab, sel_s
            else:
                listing_url, label, selector = _resolve_page(key_s)
            body = _fetch_url(listing_url, timeout, max_bytes=max_bytes)
            items = _extract_from_listing_page(listing_url, body, label, per_page, selector)
            all_items.extend(items)
        except Exception as e:
            errors.append({"page": key_s, "message": str(e)})

    return all_items, errors


def _cmd_fetch_rss(req: Dict[str, Any]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    feed_keys = req.get("feeds")
    if not isinstance(feed_keys, list) or not feed_keys:
        feed_keys = ["solidot_rss"]
    try:
        per_feed = int(req.get("per_feed", 10))
    except Exception:
        per_feed = 10
    per_feed = max(1, min(per_feed, 50))
    try:
        timeout = float(req.get("timeout", 25))
    except Exception:
        timeout = 25.0

    all_items: List[Dict[str, str]] = []
    errors: List[Dict[str, str]] = []

    for key in feed_keys:
        key_s = str(key).strip()
        try:
            url, label = _resolve_feed_url(key_s)
            body = _fetch_url(url, timeout)
            items = _parse_feed(body, label)
            all_items.extend(items[:per_feed])
        except Exception as e:
            errors.append({"feed": key_s, "message": str(e)})

    return all_items, errors


def _run_fetch_pipeline(req: Dict[str, Any]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]], str]:
    """拉取 + 去重 + max_total，返回 (items, errors, used_mode)。"""
    mode = str(req.get("mode") or "auto").lower()

    if mode == "rss":
        all_items, errors = _cmd_fetch_rss(req)
        used_mode = "rss"
    elif mode == "pages":
        all_items, errors = _cmd_fetch_pages(req)
        used_mode = "pages"
    else:
        plist = req.get("pages")
        flist = req.get("feeds")
        has_pages = isinstance(plist, list) and len(plist) > 0
        has_feeds = isinstance(flist, list) and len(flist) > 0
        if has_feeds and not has_pages:
            all_items, errors = _cmd_fetch_rss(req)
            used_mode = "rss"
        else:
            all_items, errors = _cmd_fetch_pages(req)
            used_mode = "pages"

    dedupe = bool(req.get("dedupe", True))
    if dedupe:
        seen = set()
        unique: List[Dict[str, str]] = []
        for it in all_items:
            k = _normalize_title(it.get("title", ""))
            if not k or k in seen:
                continue
            seen.add(k)
            unique.append(it)
        all_items = unique

    max_total = req.get("max_total")
    try:
        max_total_i = int(max_total) if max_total is not None else None
    except Exception:
        max_total_i = None
    if max_total_i is not None and max_total_i > 0:
        all_items = all_items[:max_total_i]

    return all_items, errors, used_mode


def _digest_date_line(req: Dict[str, Any]) -> str:
    d = req.get("date")
    if isinstance(d, str) and d.strip():
        return d.strip()
    return date.today().isoformat()


def _digest_markdown(items: List[Dict[str, str]], headline: str, date_line: str) -> str:
    lines = [
        "# %s" % headline,
        "",
        "> 日期：%s（按来源分组；可直接发布或由上游 Agent 再摘要）" % date_line,
        "",
    ]
    by_src: Dict[str, List[Dict[str, str]]] = {}
    for it in items:
        src = it.get("feed") or "其他"
        by_src.setdefault(src, []).append(it)
    for src in sorted(by_src.keys()):
        lines.append("## %s\n" % src)
        for it in by_src[src][:20]:
            t = it.get("title") or ""
            u = it.get("link") or ""
            if u:
                lines.append("- [%s](%s)" % (t, u))
            else:
                lines.append("- %s" % t)
        lines.append("")
    lines.append("---\n*采集自上述站点列表页，详情请阅读原文。*\n")
    return "\n".join(lines)


def cmd_digest() -> None:
    req = _read_json_arg()
    all_items, errors, used_mode = _run_fetch_pipeline(req)

    headline = str(req.get("digest_title") or req.get("md_title") or "今日新闻简报")
    date_line = _digest_date_line(req)
    text = _digest_markdown(all_items, headline, date_line)

    if int(req.get("stderr_meta", 0)) == 1 and errors:
        print(
            json.dumps({"warnings": errors, "mode": used_mode, "item_count": len(all_items)}, ensure_ascii=False),
            file=sys.stderr,
        )
    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")


def cmd_fetch() -> None:
    req = _read_json_arg()
    all_items, errors, used_mode = _run_fetch_pipeline(req)

    out_fmt = str(req.get("format") or "json").lower()
    if out_fmt == "markdown":
        md_title = str(req.get("md_title") or "中文网页新闻简报")
        sys.stdout.write(_items_to_markdown(all_items, md_title))
        return

    out_obj: Dict[str, Any] = {"ok": True, "mode": used_mode, "count": len(all_items), "items": all_items}
    if errors:
        out_obj["errors"] = errors
    print(json.dumps(out_obj, ensure_ascii=False, indent=2))


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  fetch.py list\n"
            "  fetch.py fetch '{\"pages\":[\"36kr\",\"ithome\"],\"per_page\":12}'\n"
            "  fetch.py fetch '{\"mode\":\"rss\",\"feeds\":[\"solidot_rss\",\"bbc_zh\"]}'\n"
            "  fetch.py digest @req.json   # 一键 Markdown 简报（仅本地抓取，无 LLM）\n"
            "  fetch.py fetch @req.json\n"
            "Requires: pip install beautifulsoup4 (for page mode)\n",
            file=sys.stderr,
        )
        sys.exit(1)
    cmd = sys.argv[1].strip().lower()
    try:
        if cmd in ("list", "list-feeds", "list_feeds", "list-pages", "list_pages"):
            cmd_list()
        elif cmd == "fetch":
            cmd_fetch()
        elif cmd == "digest":
            cmd_digest()
        else:
            print("unknown command: %s" % cmd, file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
