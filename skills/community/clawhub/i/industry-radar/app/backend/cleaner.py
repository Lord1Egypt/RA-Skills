"""
M3 正文抽取与清洗。

职责
----
1. URL 归一化（去掉 utm_* 等跟踪参数、去掉 fragment），用于跨源去重。
2. HTML 正文抽取：优先 trafilatura（质量高），退化为 BeautifulSoup。
3. 文本清洗：去空白、去广告段落、限长。
"""
from __future__ import annotations

import hashlib
import logging
import re
from typing import Dict
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

import net_guard
from config import FETCH_FULLTEXT, MAX_FETCH_BYTES, REQUEST_TIMEOUT, USER_AGENT

log = logging.getLogger("industryradar.cleaner")

_HEADERS = {"User-Agent": USER_AGENT}

# 需要剔除的跟踪参数
_TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "spm", "from", "share_token", "ref", "fbclid", "gclid", "source",
}

# 广告 / 无关块的正则
_NOISE_PATTERNS = [
    re.compile(r"(点击|扫描)(上方|下方|这里)?.*?(关注|二维码)"),
    re.compile(r"(微信|公众号)[:：]?\s*[\w\-]{3,}"),
    re.compile(r"(广告|赞助|推广|Advertisement)", re.IGNORECASE),
    re.compile(r"^\s*(编辑|作者|来源|责任编辑|撰文|文|责辑)\s*[:：|｜丨]\s*.{0,12}$", re.MULTILINE),
    re.compile(r"^\s*(责编|评论|审校)\s*[:：]?\s*\S{0,10}$", re.MULTILINE),
    re.compile(r"^\s*本文(约)?\s*\d+\s*字.*$", re.MULTILINE),
    re.compile(r"^\s*建议阅读\s*\d+\s*分钟\s*$", re.MULTILINE),
    re.compile(r"^\s*文章链接[:：]?.*$", re.MULTILINE),
    # 面包屑导航 / 页面元数据（IT之家等源 RSS 正文常见）
    re.compile(r"^\s*(首页|末页|上一页|下一页|返回|查看更多)\s*$", re.MULTILINE),
    re.compile(r"^\s*[>»›]\s*$", re.MULTILINE),
    re.compile(r"^\s*\d{4}[/\-]\d{1,2}[/\-]\d{1,2}\s*\d{1,2}:\d{2}(:\d{2})?\s*$", re.MULTILINE),
    re.compile(r"(版权|©|Copyright).{0,60}$", re.MULTILINE | re.IGNORECASE),
]
_WS = re.compile(r"[ \t\u00a0]+")
_MULTI_NL = re.compile(r"\n{3,}")

# 乱码检测：UTF-8 被按 Latin-1 解码后会出现大量 \u0080-\u00ff 区间字符
# （正常中英文文本几乎不含该区间），如 "ç«å±±å¼æ"。
_GARBLED_CH = re.compile(r"[\u0080-\u00ff]")
# 反爬 / 人机验证页特征（只出现在验证页文案里，正常文章正文不会整段命中）
_JUNK_PAGE_MARKS = ("正在加速", "请耐心等待", "请完成以下验证", "访问过于频繁", "滑动验证")


def normalize_url(url: str) -> str:
    """归一化 URL：小写 scheme/host，去跟踪参数，去 fragment，去尾斜杠。"""
    try:
        p = urlparse(url.strip())
        query = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
                 if k.lower() not in _TRACKING_PARAMS]
        path = p.path.rstrip("/") or "/"
        norm = urlunparse((
            p.scheme.lower(),
            p.netloc.lower(),
            path,
            "",
            urlencode(query),
            "",
        ))
        return norm
    except Exception:  # noqa: BLE001
        return url.strip()


def url_hash(url: str) -> str:
    return hashlib.sha1(normalize_url(url).encode("utf-8")).hexdigest()


def clean_text(text: str, max_len: int = 12000) -> str:
    if not text:
        return ""
    # 反爬验证页：整页丢弃（返回空串，由上层用标题/链接兜底）
    if any(m in text for m in _JUNK_PAGE_MARKS):
        return ""
    # 乱码页（编码错乱的解耦文本）：Latin-1 补充区字符占比 > 2% 即判废
    if len(_GARBLED_CH.findall(text)) / len(text) > 0.02:
        return ""
    text = BeautifulSoup(text, "lxml").get_text("\n")
    text = _WS.sub(" ", text)
    raw = [l.strip() for l in text.split("\n")]

    # 面包屑上下文剔除：独立 ">" 行本身及其前后相邻的短行（≤12 字）
    # 都是导航片段（如「首页 > 智车之家 > 车用技术」），整链丢弃。
    drop = set()
    for i, s in enumerate(raw):
        if s in (">", "»", "›"):
            drop.add(i)
            j = i - 1
            while j >= 0 and not raw[j]:
                j -= 1
            if j >= 0 and len(raw[j]) <= 12:
                drop.add(j)
            j = i + 1
            while j < len(raw) and not raw[j]:
                j += 1
            if j < len(raw) and len(raw[j]) <= 12:
                drop.add(j)

    lines = []
    for i, s in enumerate(raw):
        if not s or i in drop:
            continue
        if any(p.search(s) for p in _NOISE_PATTERNS):
            continue
        lines.append(s)
    out = "\n".join(lines)
    out = _MULTI_NL.sub("\n\n", out).strip()
    return out[:max_len]


def _extract_with_trafilatura(html: str, url: str) -> str:
    try:
        import trafilatura  # type: ignore
        txt = trafilatura.extract(
            html, url=url, include_comments=False, include_tables=False,
            favor_precision=True,
        )
        return txt or ""
    except Exception:  # noqa: BLE001
        return ""


def _extract_with_bs4(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form", "iframe"]):
        tag.decompose()
    node = (soup.find("article")
            or soup.find("div", class_=re.compile(r"(content|article|post|main)", re.I))
            or soup.body
            or soup)
    return node.get_text("\n") if node else ""


def fetch_fulltext(url: str) -> str:
    """抓取网页并抽取正文；失败返回空串（交由上层用 RSS 摘要兜底）。

    URL 来自 RSS 条目（外部可控），因此必须走 net_guard 出站校验，
    禁止访问内网 / 云元数据地址，并禁止跳转到内网。
    """
    if not FETCH_FULLTEXT:
        return ""
    if not net_guard.is_fetchable(url):
        return ""
    try:
        resp = net_guard.safe_get(
            url, headers=_HEADERS, timeout=REQUEST_TIMEOUT, max_bytes=MAX_FETCH_BYTES,
        )
        resp.raise_for_status()
        if "html" not in resp.headers.get("Content-Type", "").lower():
            return ""
        html = resp.text
    except (requests.RequestException, net_guard.UnsafeUrlError, OSError) as exc:
        log.debug("fulltext fetch failed: %s (%s)", url, exc)
        return ""
    except Exception as exc:  # noqa: BLE001  解析层异常同样降级
        log.debug("fulltext fetch failed: %s (%s)", url, exc)
        return ""

    txt = _extract_with_trafilatura(html, url) or _extract_with_bs4(html)
    return clean_text(txt)


def enrich(item: Dict) -> Dict:
    """把采集条目补全为带干净正文、稳定 url_hash 的文章字典。"""
    url = item.get("url", "")
    content = fetch_fulltext(url)
    if not content:
        content = clean_text(item.get("raw_content", ""))
    item["url"] = url
    item["url_hash"] = url_hash(url)
    item["content"] = content
    return item