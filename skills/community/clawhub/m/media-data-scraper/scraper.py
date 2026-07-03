#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全网作品数据抓取分析工具（抖音小红书视频号快手B站通用）v7.0
支持平台: B站、抖音、小红书、快手、视频号
架构: 短链清理 → 自动平台识别 → 多策略降级抓取 → 结构化输出
原则: 完全免费、无需注册、无需登录、无需API Key、无需付费
v5.0: 小红书全面优化 — curl_cffi TLS指纹 + xsec_token SSR + JSON深度清理
v5.1: 视频号优化 — API探测 + 结构化错误提示 + 浏览器降级指引
v6.0: 新增赞赏支持模块 — 非强制赞赏，感谢用户支持
v7.0: 新增飞书多维表格同步 — 支持数据自动推送到飞书Base
"""

import re
import json
import csv
import os
import time
import random
import base64
import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field, asdict

# ============ 可选依赖（全部免费开源） ============

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from curl_cffi import requests as curl_requests
    HAS_CURL_CFFI = True
except ImportError:
    HAS_CURL_CFFI = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

try:
    import brotli
    HAS_BROTLI = True
except ImportError:
    HAS_BROTLI = False


# ============ 配置 ============

REQUEST_TIMEOUT = 15

PC_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

MOBILE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
                  "Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
}


# ============ 数据模型 ============

@dataclass
class ScrapeResult:
    """统一返回数据结构"""
    platform: str = ""
    url: str = ""
    resolved_url: str = ""
    title: Optional[str] = None
    author: Optional[str] = None
    author_id: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    cover_url: Optional[str] = None
    video_url: Optional[str] = None
    image_urls: List[str] = field(default_factory=list)
    views: Optional[int] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
    shares: Optional[int] = None
    collects: Optional[int] = None
    coins: Optional[int] = None
    favorites: Optional[int] = None
    danmaku: Optional[int] = None
    duration: Optional[int] = None
    publish_time: Optional[str] = None
    status: str = "error"
    error: Optional[str] = None
    strategy_used: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {k: v for k, v in asdict(self).items()
                if v is not None and v != [] and v != ""}


# ============ HTTP 工具 ============

def _get(url: str, headers: Optional[Dict] = None, use_curl: bool = False,
          mobile: bool = False, timeout: int = REQUEST_TIMEOUT) -> str:
    """统一 GET 请求，自动处理编码"""
    base = MOBILE_HEADERS if mobile else PC_HEADERS
    merged = {**base, **(headers or {})}

    if use_curl and HAS_CURL_CFFI:
        resp = curl_requests.get(url, headers=merged, impersonate="chrome131",
                                  timeout=timeout, allow_redirects=True)
    elif HAS_REQUESTS:
        resp = requests.get(url, headers=merged, allow_redirects=True, timeout=timeout)
    else:
        raise RuntimeError("请安装 requests: pip install requests")

    resp.raise_for_status()
    # 处理 brotli 压缩（requests 可能未自动解压）
    try:
        return resp.content.decode('utf-8')
    except UnicodeDecodeError:
        enc = getattr(resp, 'encoding', 'utf-8') or 'utf-8'
        return resp.content.decode(enc, errors='replace')


def _get_json(url: str, headers: Optional[Dict] = None, **kwargs) -> Optional[Dict]:
    """GET 请求并解析 JSON"""
    html = _get(url, headers=headers, **kwargs)
    return json.loads(html)


def _extract_json(html: str, pattern: str) -> Optional[Dict]:
    """从 HTML 正则提取 JSON（适合小型 JSON）"""
    match = re.search(pattern, html, re.DOTALL)
    if match:
        try:
            raw = match.group(1)
            raw = _clean_xhs_json(raw)
            return json.loads(raw)
        except json.JSONDecodeError:
            pass
    return None


def _clean_xhs_json(raw: str) -> str:
    """
    清理小红书 __INITIAL_STATE__ JSON 中的非法值。
    处理: undefined、空值（冒号后直接跟逗号/右括号）、尾部多余逗号。
    """
    # undefined → null（必须在最前面，因为 undefined 可能出现在任何位置）
    raw = raw.replace('undefined', 'null')
    # "key":, → "key":null,  和  "key":} → "key":null}
    raw = re.sub(r':\s*,', ':null,', raw)
    raw = re.sub(r':\s*\}', ':null}', raw)
    # 尾部多余逗号: ,} → }  和  ,] → ]
    raw = re.sub(r',\s*([}\]])', r'\1', raw)
    return raw


def _extract_json_long(html: str, var_name: str) -> Optional[Dict]:
    """
    从 HTML 提取大型 JSON 变量（如 window.INIT_STATE、window.__INITIAL_STATE__）。
    使用字符串查找+括号匹配，避免正则回溯失败。
    """
    # 尝试两种格式: "window.xxx = " 和 "window.xxx="
    for marker in [f"window.{var_name} = ", f"window.{var_name}="]:
        idx = html.find(marker)
        if idx != -1:
            start = idx + len(marker)
            brace_count = 0
            in_string = False
            escape = False
            end = start
            for i, ch in enumerate(html[start:], start):
                if escape:
                    escape = False
                    continue
                if ch == '\\':
                    escape = True
                    continue
                if ch == '"':
                    in_string = not in_string
                    continue
                if in_string:
                    continue
                if ch == '{':
                    brace_count += 1
                elif ch == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end = i + 1
                        break
            if end <= start:
                continue
            try:
                raw = html[start:end]
                raw = _clean_xhs_json(raw)
                return json.loads(raw)
            except json.JSONDecodeError:
                continue
    return None


def _safe_get(d, *keys, default=None):
    """安全深度取值"""
    for k in keys:
        if isinstance(d, dict) and k in d:
            d = d[k]
        else:
            return default
    return d


def _to_int(val) -> Optional[int]:
    """安全转 int，支持 '1.2万' '3.5w' '1.5k' '1.5亿'。空字符串返回0而非None。"""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return int(val)
    s = str(val).strip()
    if s == '--':
        return None
    if not s:
        return 0
    try:
        s_lower = s.lower()
        if '亿' in s:
            return int(float(re.sub(r'[^\d.]', '', s)) * 100000000)
        if '万' in s or 'w' in s_lower:
            return int(float(re.sub(r'[^\d.]', '', s)) * 10000)
        if '千' in s or 'k' in s_lower:
            return int(float(re.sub(r'[^\d.]', '', s)) * 1000)
        return int(float(s))
    except (ValueError, TypeError):
        return None


def _format_number(val) -> Optional[str]:
    """数字格式化为可读字符串"""
    if val is None:
        return None
    if val >= 100000000:
        return f"{val / 100000000:.1f}亿"
    if val >= 10000:
        return f"{val / 10000:.1f}万"
    return str(val)


# ============ 短链清理与解析 ============

def _clean_share_url(url: str) -> str:
    """
    清理用户粘贴的分享链接，剥离短链后面附加的中文文案。
    'https://v.kuaishou.com/7DIaYVwA消操实操96分' → 'https://v.kuaishou.com/7DIaYVwA'
    """
    parsed = urllib.parse.urlparse(url)
    domain = parsed.hostname or ""
    path = parsed.path

    # 短链域名：提取路径中第一个连续的字母数字段
    short_domains = [
        "v.kuaishou.com", "v.douyin.com", "iesdouyin.com",
        "b23.tv", "xhslink.com", "bili2233.cn",
    ]
    for d in short_domains:
        if d in domain:
            pattern = r'^(/[A-Za-z0-9_-]+)'
            match = re.match(pattern, path)
            if match:
                return urllib.parse.urlunparse(parsed._replace(path=match.group(1)))

    return url


def resolve_short_url(url: str) -> str:
    """解析短链接，跟随重定向获取真实URL"""
    url = _clean_share_url(url)

    for method in ['head', 'get']:
        try:
            if HAS_CURL_CFFI:
                resp = curl_requests.head(url, headers=PC_HEADERS, impersonate="chrome131",
                                           allow_redirects=True, timeout=10) if method == 'head' \
                    else curl_requests.get(url, headers=PC_HEADERS, impersonate="chrome131",
                                            allow_redirects=True, timeout=10)
            elif HAS_REQUESTS:
                kwargs = {"headers": PC_HEADERS, "allow_redirects": True, "timeout": 10}
                if method == 'head':
                    resp = requests.head(url, **kwargs)
                else:
                    kwargs["stream"] = True
                    resp = requests.get(url, **kwargs)
            else:
                return url

            final_url = getattr(resp, 'url', url)
            return str(final_url) if final_url else url
        except Exception:
            continue

    return url


# ============ 平台检测 ============

SHORT_URL_DOMAINS = {
    "v.douyin.com": "douyin",
    "iesdouyin.com": "douyin",
    "b23.tv": "bilibili",
    "bili2233.cn": "bilibili",
    "xhslink.com": "xiaohongshu",
    "chenzhongtech.com": "kuaishou",
    "kuaishouapp.com": "kuaishou",
    "weixin.qq.com": "channels",
}

PLATFORM_KEYWORDS = {
    "bilibili": ["bilibili.com", "b23.tv", "bili2233.cn"],
    "douyin": ["douyin.com", "iesdouyin.com", "v.douyin.com"],
    "xiaohongshu": ["xiaohongshu.com", "xhslink.com"],
    "kuaishou": ["kuaishou.com", "chenzhongtech.com", "kuaishouapp.com"],
    "channels": ["channels.weixin.qq.com"],
}

PLATFORM_NAMES = {
    "bilibili": "B站", "douyin": "抖音", "xiaohongshu": "小红书",
    "kuaishou": "快手", "channels": "视频号",
}


def detect_platform(url: str) -> str:
    """自动识别平台"""
    url_lower = url.lower()
    domain = urllib.parse.urlparse(url_lower).hostname or ""

    for short_domain, platform in SHORT_URL_DOMAINS.items():
        if short_domain in domain:
            return platform

    for platform, keywords in PLATFORM_KEYWORDS.items():
        if any(kw in url_lower for kw in keywords):
            return platform

    return "unknown"


# ============ B站解析器 ============

def _extract_bvid(url: str) -> Optional[str]:
    """提取BV号（大小写敏感）"""
    for p in [r'/video/(BV[\w]+)', r'/video/(av\d+)', r'(BV[\w]{10,})']:
        m = re.search(p, url, re.I)
        if m:
            return m.group(1)
    return None


def _bilibili_api(url: str) -> ScrapeResult:
    """B站: 公开API直调（无需签名、无需登录）"""
    r = ScrapeResult(platform="bilibili", url=url, strategy_used="bilibili_api")
    bvid = _extract_bvid(url)
    if not bvid:
        r.error = "无法从URL提取BV号"
        return r

    try:
        data = _get_json(
            f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}",
            headers={"Referer": "https://www.bilibili.com/", "Accept": "application/json"}
        )
        if not data or data.get("code") != 0:
            r.error = f"API返回错误: {_safe_get(data, 'message', default='unknown')}"
            return r

        info = data["data"]
        stat = info.get("stat", {})
        owner = info.get("owner", {})
        pages = info.get("pages", [])

        r.title = info.get("title")
        r.author = owner.get("name")
        r.author_id = str(owner.get("mid", ""))
        r.description = info.get("desc") or info.get("desc_v2")
        r.cover_url = info.get("pic")
        r.views = _to_int(stat.get("view"))
        r.likes = _to_int(stat.get("like"))
        r.coins = _to_int(stat.get("coin"))
        r.favorites = _to_int(stat.get("favorite"))
        r.shares = _to_int(stat.get("share"))
        r.comments = _to_int(stat.get("reply"))
        r.danmaku = _to_int(stat.get("danmaku"))
        r.duration = _to_int(info.get("duration"))

        pub_ts = info.get("pubdate")
        if pub_ts:
            r.publish_time = datetime.fromtimestamp(pub_ts).strftime("%Y-%m-%d %H:%M:%S")

        r.tags = [t.get("tag_name") for t in info.get("tags", []) if t.get("tag_name")]

        if len(pages) > 1:
            parts = [f"P{i['page']} {i['part']}" for i in pages]
            r.description = (r.description or "") + f"\n\n共{len(pages)}P: " + " | ".join(parts)

        r.status = "success"
        return r
    except Exception as e:
        r.error = str(e)
        return r


# ============ 抖音解析器 ============

def _douyin_router_data(url: str) -> ScrapeResult:
    """抖音策略1: 移动端 iesdouyin.com 的 window._ROUTER_DATA（免签名）"""
    r = ScrapeResult(platform="douyin", url=url, strategy_used="douyin_router_data")
    try:
        resolved = resolve_short_url(url)
        r.resolved_url = resolved

        vid = None
        for p in [r'/video/(\d+)', r'/note/(\d+)']:
            m = re.search(p, resolved)
            if m:
                vid = m.group(1)
                break
        if not vid:
            r.error = "无法提取视频ID"
            return r

        html = _get(f"https://www.iesdouyin.com/share/video/{vid}/",
                     mobile=True, use_curl=HAS_CURL_CFFI)

        data = _extract_json(html, r'window\._ROUTER_DATA\s*=\s*(\{.*?\})\s*</script>')
        if not data:
            r.error = "未找到 _ROUTER_DATA（可能被风控）"
            return r

        items = _safe_get(data, "loaderData", "video_(id)/page",
                          "videoInfoRes", "item_list", default=[])
        if not items:
            # 动态匹配 video_<id>/page 键
            loader = data.get("loaderData", {})
            for k, v in loader.items():
                if k.startswith("video_") and "/page" in k:
                    items = _safe_get(v, "videoInfoRes", "item_list", default=[])
                    if items:
                        break
        if not items:
            r.error = "视频数据列表为空"
            return r

        item = items[0]
        author = item.get("author", {})
        stats = item.get("statistics", {})
        video = item.get("video", {})

        r.title = item.get("desc", "")
        r.author = author.get("nickname")
        r.author_id = author.get("uid") or author.get("sec_uid")
        r.description = item.get("desc", "")
        r.views = _to_int(stats.get("play_count"))
        r.likes = _to_int(stats.get("digg_count"))
        r.comments = _to_int(stats.get("comment_count"))
        r.shares = _to_int(stats.get("share_count"))
        r.collects = _to_int(stats.get("collect_count"))
        r.duration = _to_int(video.get("duration"))
        cover_list = _safe_get(video, "cover", "url_list", default=[])
        r.cover_url = cover_list[0] if cover_list else None
        r.tags = [t.get("hashtag_name", "") for t in item.get("text_extra", []) if t.get("hashtag_name")]

        create_ts = item.get("create_time")
        if create_ts:
            r.publish_time = datetime.fromtimestamp(create_ts).strftime("%Y-%m-%d %H:%M:%S")

        images = item.get("images", [])
        if images:
            r.image_urls = [img.get("url_list", [""])[0] for img in images if img.get("url_list")]

        r.status = "success"
        return r
    except Exception as e:
        r.error = f"移动端解析失败: {str(e)}"
        return r


def _douyin_ssr(url: str) -> ScrapeResult:
    """抖音策略2: PC端 _SSR_HYDRATED_DATA（需 curl_cffi）"""
    r = ScrapeResult(platform="douyin", url=url, strategy_used="douyin_ssr")
    try:
        resolved = resolve_short_url(url)
        r.resolved_url = resolved
        html = _get(resolved, use_curl=HAS_CURL_CFFI)

        data = _extract_json(html, r'<script[^>]*>window\._SSR_HYDRATED_DATA\s*=\s*(\{.*?\})</script>')
        if not data:
            r.error = "未找到 SSR_HYDRATED_DATA"
            return r

        video_info = _safe_get(data, "app", "videoInfo", default={})
        stats = video_info.get("stats", {})
        author = video_info.get("author", {})

        r.title = video_info.get("title")
        r.author = author.get("nickname")
        r.description = video_info.get("desc")
        r.views = _to_int(stats.get("playCount"))
        r.likes = _to_int(stats.get("diggCount"))
        r.comments = _to_int(stats.get("commentCount"))
        r.shares = _to_int(stats.get("shareCount"))
        r.collects = _to_int(stats.get("collectCount"))
        r.status = "success"
        return r
    except Exception as e:
        r.error = f"SSR解析失败: {str(e)}"
        return r


def _douyin_meta(url: str) -> ScrapeResult:
    """抖音策略3: Meta标签兜底"""
    r = ScrapeResult(platform="douyin", url=url, strategy_used="douyin_meta")
    try:
        html = _get(url)
        if not HAS_BS4:
            r.error = "缺少 BeautifulSoup"
            return r
        soup = BeautifulSoup(html, 'lxml')
        r.title = _meta_content(soup, "og:title")
        r.description = _meta_content(soup, "og:description")
        r.cover_url = _meta_content(soup, "og:image")
        r.status = "partial"
        r.error = "仅获取到基础元数据（受风控限制）"
        return r
    except Exception as e:
        r.error = str(e)
        return r


# ============ 小红书解析器 ============

# 小红书专用请求头（必须带 Referer，否则更容易被拦截）
XHS_HEADERS = {
    "Referer": "https://www.xiaohongshu.com/explore",
    "Origin": "https://www.xiaohongshu.com",
}


def _xhs_extract_note(html: str) -> Optional[Dict]:
    """
    从小红书页面HTML提取笔记数据。
    支持: 大型 __INITIAL_STATE__ JSON + undefined/空值清理 + noteDetailMap 多键遍历。
    """
    # 优先用 _extract_json_long 处理大型 __INITIAL_STATE__
    data = _extract_json_long(html, "__INITIAL_STATE__")
    if not data:
        data = _extract_json(html, r'<script[^>]*>window\.__INITIAL_STATE__\s*=\s*(\{.*?\});</script>')
    if not data:
        return None

    note_map = _safe_get(data, "note", "noteDetailMap", default={})
    if not note_map:
        return None

    # 遍历所有键，找到包含有效笔记数据的条目
    # noteDetailMap 的键可能是笔记ID、"null"字符串等
    for nid_key, nid_val in note_map.items():
        if not isinstance(nid_val, dict):
            continue
        note = nid_val.get("note")
        if not note or not isinstance(note, dict):
            continue
        # 标题可能为空字符串（视频笔记常见），desc 作为后备
        if note.get("title") or note.get("desc"):
            return note
    return None


def _xhs_extract_from_note(note: Dict) -> Dict:
    """从提取到的笔记 dict 中构建通用数据字段"""
    interact = note.get("interactInfo", {})
    user = note.get("user", {})
    tag_list = note.get("tagList", [])
    video = note.get("video", {})

    title = note.get("title") or ""
    desc = note.get("desc") or ""
    # 标题为空时，用 desc 前50字作为标题
    display_title = title if title else (desc[:50] + "..." if len(desc) > 50 else desc)

    result = {
        "title": display_title,
        "author": user.get("nickname"),
        "author_id": user.get("userId"),
        "description": desc,
        "likes": _to_int(interact.get("likedCount")),
        "collects": _to_int(interact.get("collectedCount")),
        "comments": _to_int(interact.get("commentCount")),
        "shares": _to_int(interact.get("shareCount")),
        "tags": [t.get("name", "") for t in tag_list if t.get("name")],
        "type": "视频" if video else "图文",
    }

    # 图片
    image_list = note.get("imageList", [])
    if image_list:
        result["image_urls"] = [
            img.get("urlDefault", "") or img.get("url", "")
            for img in image_list if img.get("urlDefault") or img.get("url")
        ]
        result["cover_url"] = result["image_urls"][0] if result["image_urls"] else None

    # 视频
    if video:
        result["video_url"] = video.get("url", "")
        result["duration"] = _to_int(video.get("duration"))

    # 发布时间（毫秒级时间戳）
    time_ts = note.get("time")
    if time_ts:
        try:
            ts = int(time_ts) / 1000 if int(time_ts) > 1e12 else int(time_ts)
            result["publish_time"] = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, OSError):
            pass

    # IP属地
    ip_loc = note.get("ipLocation")
    if ip_loc:
        result["description"] = (result.get("description") or "") + f"\n[IP属地: {ip_loc}]"

    # 类型标记
    result["description"] = (result.get("description") or "") + f"\n[类型: {result['type']}]"

    return result


def _xhs_share_token(url: str) -> ScrapeResult:
    """
    小红书策略1: 利用分享链接中的 xsec_token + curl_cffi TLS指纹。
    核心原理: xsec_token 是服务端下发的临时凭证，带 token 的请求可获取完整 SSR 数据。
    关键: 必须用 curl_cffi 模拟 Chrome TLS 指纹，否则被 JA3 检测拦截。
    """
    r = ScrapeResult(platform="xiaohongshu", url=url, strategy_used="xhs_share_token")
    try:
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)

        note_id = _extract_note_id(parsed.path)
        if not note_id:
            r.error = "无法提取笔记ID"
            return r

        xsec_token = qs.get('xsec_token', [''])[0]
        xsec_source = qs.get('xsec_source', ['pc_share'])[0]

        # 构建目标URL
        if xsec_token:
            target = (f"https://www.xiaohongshu.com/explore/{note_id}"
                      f"?xsec_token={urllib.parse.quote(xsec_token)}&xsec_source={xsec_source}")
        else:
            target = f"https://www.xiaohongshu.com/explore/{note_id}"

        # 必须用 curl_cffi（requests 会被 TLS 指纹检测拦截）
        if not HAS_CURL_CFFI:
            r.error = "小红书需要 curl_cffi 库支持（pip install curl_cffi）"
            return r

        html = _get(target, headers=XHS_HEADERS, use_curl=True)

        # 即使被 300031 拦截，HTML 中仍有 __INITIAL_STATE__
        # 但 noteDetailMap 中的 note 可能为 None
        note = _xhs_extract_note(html)
        if not note:
            # 检查是否被拦截
            if 'error_code=300031' in html or '当前笔记暂时无法浏览' in html:
                r.error = "xsec_token 已过期（约5分钟有效期），请使用最新的分享链接"
            else:
                r.error = "未找到笔记数据（可能被风控）"
            return r

        # 填充数据
        data = _xhs_extract_from_note(note)
        r.title = data["title"]
        r.author = data["author"]
        r.author_id = data["author_id"]
        r.description = data["description"]
        r.likes = data["likes"]
        r.collects = data["collects"]
        r.comments = data["comments"]
        r.shares = data["shares"]
        r.tags = data["tags"]
        r.image_urls = data.get("image_urls", [])
        r.cover_url = data.get("cover_url")
        r.video_url = data.get("video_url")
        r.duration = data.get("duration")
        r.publish_time = data.get("publish_time")

        r.status = "success"
        return r
    except Exception as e:
        r.error = f"分享链接解析失败: {str(e)}"
        return r


def _xhs_explore(url: str) -> ScrapeResult:
    """
    小红书策略2: 直接 explore 路径（无 xsec_token）。
    通常会被 300031 拦截，但尝试作为降级方案。
    """
    r = ScrapeResult(platform="xiaohongshu", url=url, strategy_used="xhs_explore")
    try:
        parsed = urllib.parse.urlparse(url)
        note_id = _extract_note_id(parsed.path)
        if not note_id:
            r.error = "无法提取笔记ID"
            return r

        if not HAS_CURL_CFFI:
            r.error = "小红书需要 curl_cffi 库支持"
            return r

        html = _get(f"https://www.xiaohongshu.com/explore/{note_id}",
                     headers=XHS_HEADERS, use_curl=True)

        note = _xhs_extract_note(html)
        if not note:
            r.error = "被拦截，需要有效的 xsec_token（请使用完整分享链接）"
            return r

        data = _xhs_extract_from_note(note)
        r.title = data["title"]
        r.author = data["author"]
        r.likes = data["likes"]
        r.collects = data["collects"]
        r.comments = data["comments"]
        r.shares = data["shares"]
        r.status = "success"
        return r
    except Exception as e:
        r.error = str(e)
        return r


def _xhs_meta(url: str) -> ScrapeResult:
    """小红书策略3: Meta标签兜底（即使被拦截也能获取标题和描述）"""
    r = ScrapeResult(platform="xiaohongshu", url=url, strategy_used="xhs_meta")
    try:
        html = _get(url, headers=XHS_HEADERS, use_curl=HAS_CURL_CFFI)
        if not HAS_BS4:
            r.error = "缺少 BeautifulSoup"
            return r
        soup = BeautifulSoup(html, 'lxml')
        r.title = _meta_content(soup, "og:title")
        r.description = _meta_content(soup, "og:description")
        r.cover_url = _meta_content(soup, "og:image")
        if r.title or r.description:
            r.status = "partial"
            r.error = "仅获取到基础元数据（xsec_token 过期或缺失）"
        else:
            r.error = "未能获取任何数据"
        return r
    except Exception as e:
        r.error = str(e)
        return r


def _extract_note_id(path: str) -> Optional[str]:
    """从小红书URL路径提取笔记ID"""
    parts = path.split('/')
    for i, p in enumerate(parts):
        if p in ('item', 'explore', 'note') and i + 1 < len(parts):
            # 确保下一个部分不是空字符串
            nid = parts[i + 1]
            if nid and nid not in ('item', 'explore', 'note', 'discovery'):
                return nid
    return None


# ============ 快手解析器 ============

def _kuaishou_page(url: str) -> ScrapeResult:
    """快手: INIT_STATE / __APOLLO_STATE__ 解析（支持短链和直接链接）"""
    r = ScrapeResult(platform="kuaishou", url=url, strategy_used="kuaishou_page")
    try:
        resolved = resolve_short_url(url)
        r.resolved_url = resolved
        html = _get(resolved, use_curl=HAS_CURL_CFFI)

        # 策略1: __APOLLO_STATE__ (旧版页面)
        data = _extract_json(html, r'<script[^>]*>window\.__APOLLO_STATE__\s*=\s*(\{.*?\});</script>')
        if data:
            for key, val in data.items():
                if isinstance(val, dict) and any(
                    k in str(val).lower() for k in
                    ["viewcount", "likecount", "playcount", "caption", "username"]
                ):
                    r.title = val.get("caption") or val.get("title")
                    r.author = val.get("userName") or val.get("authorName")
                    r.description = val.get("caption", "")
                    r.views = _to_int(val.get("viewCount") or val.get("playCount"))
                    r.likes = _to_int(val.get("likeCount") or val.get("diggCount"))
                    r.comments = _to_int(val.get("commentCount"))
                    r.shares = _to_int(val.get("shareCount"))
                    r.cover_url = val.get("coverUrl") or val.get("cover_url")
                    r.status = "success"
                    return r

        # 策略2: INIT_STATE (新版页面)
        init_data = _extract_json_long(html, "INIT_STATE")
        if not init_data:
            init_data = _extract_json(html, r'<script[^>]*>window\.INIT_STATE\s*=\s*(\{.*?\});</script>')

        if init_data:
            # 2a: feeds 结构 (www.kuaishou.com)
            for key, val in init_data.items():
                if isinstance(val, dict) and isinstance(val.get("feeds"), list) and val["feeds"]:
                    feed = val["feeds"][0]
                    photo = feed.get("photo", {})
                    author = feed.get("author", {})

                    r.title = photo.get("caption") or photo.get("title")
                    r.author = author.get("name")
                    r.author_id = author.get("id")
                    r.description = photo.get("caption", "")
                    r.views = _to_int(photo.get("viewCount"))
                    r.likes = _to_int(photo.get("likeCount"))
                    r.comments = _to_int(photo.get("commentCount"))
                    r.shares = _to_int(photo.get("shareCount"))
                    r.collects = _to_int(photo.get("collectCount"))
                    r.cover_url = photo.get("coverUrl") or photo.get("thumbnailUrl")
                    r.duration = _to_int(photo.get("duration"))
                    r.publish_time = _kuaishou_ts(photo.get("timestamp"))
                    r.tags = [t.get("name", "") for t in feed.get("tags", []) if t.get("name")]

                    mv = photo.get("mainMvUrls") or photo.get("mvUrls")
                    if mv and isinstance(mv[0], dict):
                        r.video_url = mv[0].get("url")

                    photo_urls = photo.get("photoUrls")
                    if photo_urls:
                        r.image_urls = [u.get("url") for u in photo_urls if u.get("url")]

                    r.status = "success"
                    return r

            # 2b: 直接 photo 结构 (v.m.chenzhongtech.com)
            for key, val in init_data.items():
                if isinstance(val, dict) and isinstance(val.get("photo"), dict):
                    photo = val["photo"]
                    counts = val.get("counts", {})

                    r.title = photo.get("caption") or photo.get("title")
                    r.author = photo.get("userName")
                    r.author_id = str(photo.get("userId")) if photo.get("userId") else None
                    r.description = photo.get("caption", "")
                    r.views = _to_int(photo.get("viewCount"))
                    r.likes = _to_int(photo.get("likeCount"))
                    r.comments = _to_int(photo.get("commentCount"))
                    r.shares = _to_int(photo.get("shareCount"))
                    r.collects = _to_int(photo.get("forwardCount"))
                    r.favorites = _to_int(counts.get("collectionCount"))

                    cover_urls = photo.get("coverUrls") or photo.get("webpCoverUrls") or []
                    if cover_urls:
                        r.cover_url = cover_urls[0].get("url") if isinstance(cover_urls[0], dict) else cover_urls[0]

                    r.duration = _to_int(photo.get("duration"))
                    r.publish_time = _kuaishou_ts(photo.get("timestamp"))

                    main_mv = photo.get("mainMvUrls", [])
                    if main_mv and isinstance(main_mv[0], dict):
                        r.video_url = main_mv[0].get("url")

                    atlas = val.get("atlas", {})
                    if isinstance(atlas, dict):
                        atlas_list = atlas.get("list", [])
                        if atlas_list:
                            if isinstance(atlas_list[0], str):
                                r.image_urls = atlas_list
                            elif isinstance(atlas_list[0], dict):
                                r.image_urls = [img.get("url", "") for img in atlas_list if img.get("url")]

                    r.status = "success"
                    return r

        # Meta 兜底
        if HAS_BS4:
            soup = BeautifulSoup(html, 'lxml')
            r.title = _meta_content(soup, "og:title")
            if r.title:
                r.status = "partial"
                r.error = "仅获取到标题"
                return r

        r.error = "未能提取视频数据"
        return r
    except Exception as e:
        r.error = str(e)
        return r


def _kuaishou_ts(ts) -> Optional[str]:
    """快手时间戳（毫秒级）转可读格式"""
    if not ts:
        return None
    try:
        if ts > 1e12:
            ts = ts / 1000
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


# ============ 视频号解析器 ============

# 视频号专用请求头（模拟微信内置浏览器）
WECHAT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36 MicroMessenger/8.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://weixin.qq.com/",
}


def _channels_api_probe(url: str) -> ScrapeResult:
    """
    视频号策略1: 探测内部API是否可访问（偶尔可用，不稳定）。
    尝试通过视频ID构造可能的API端点获取数据。
    """
    r = ScrapeResult(platform="channels", url=url, strategy_used="channels_api_probe")
    try:
        # 从URL提取视频ID
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        vid = qs.get('id', [''])[0]
        if not vid and '/sph/' in parsed.path:
            # 从路径提取: /sph/ASywao2nB1
            parts = parsed.path.split('/')
            for i, p in enumerate(parts):
                if p == 'sph' and i + 1 < len(parts):
                    vid = parts[i + 1]
                    break

        if not vid:
            r.error = "无法提取视频号ID"
            return r

        # 尝试访问几个可能的API端点（实验性，可能随时失效）
        # 这些端点基于微信视频号内部API路径猜测
        api_endpoints = [
            f"https://channels.weixin.qq.com/finder-api/video_detail?id={vid}",
            f"https://channels.weixin.qq.com/api/v1/finder/video?id={vid}",
        ]

        for endpoint in api_endpoints:
            try:
                html = _get(endpoint, headers=WECHAT_HEADERS, use_curl=HAS_CURL_CFFI, timeout=8)
                if html and len(html) > 100:
                    # 尝试解析JSON响应
                    try:
                        data = json.loads(html)
                        if data and isinstance(data, dict):
                            # 如果返回了有效数据
                            video_data = data.get("data", {})
                            if video_data:
                                r.title = video_data.get("title") or video_data.get("desc")
                                r.author = video_data.get("nickname") or video_data.get("username")
                                r.description = video_data.get("desc")
                                r.likes = _to_int(video_data.get("like_count") or video_data.get("likeCount"))
                                r.comments = _to_int(video_data.get("comment_count") or video_data.get("commentCount"))
                                r.shares = _to_int(video_data.get("forward_count") or video_data.get("forwardCount"))
                                r.cover_url = video_data.get("cover_url") or video_data.get("coverUrl")
                                r.status = "success"
                                return r
                    except json.JSONDecodeError:
                        pass
            except Exception:
                continue

        r.error = "API探测未获取到数据"
        return r
    except Exception as e:
        r.error = f"API探测失败: {str(e)}"
        return r


def _channels_meta(url: str) -> ScrapeResult:
    """
    视频号策略2: 返回结构化提示信息。
    视频号为纯SPA页面，脚本无法获取动态数据，必须浏览器环境。
    """
    r = ScrapeResult(platform="channels", url=url, strategy_used="channels_meta")
    try:
        resolved = resolve_short_url(url)
        r.resolved_url = resolved

        # 提取视频ID用于提示
        parsed = urllib.parse.urlparse(resolved)
        qs = urllib.parse.parse_qs(parsed.query)
        vid = qs.get('id', [''])[0]

        # 设置明确的错误信息，指导用户或上层调用者
        r.error = (
            "视频号为微信封闭生态的纯SPA页面，脚本无法获取数据。\n"
            "解决方案（按优先级）:\n"
            "1. 【推荐】使用浏览器环境: browser_navigate 打开链接 → "
            "browser_wait_for 3秒 → browser_evaluate 执行 BROWSER_JS_CHANNELS\n"
            "2. 使用第三方API服务（如TikHub等付费API）\n"
            "3. 手动在微信中查看数据"
        )

        # 尝试获取任何可用的meta信息（虽然通常没有）
        try:
            html = _get(resolved, headers=WECHAT_HEADERS, use_curl=HAS_CURL_CFFI, timeout=8)
            if HAS_BS4:
                soup = BeautifulSoup(html, 'lxml')
                og_title = _meta_content(soup, "og:title")
                og_desc = _meta_content(soup, "og:description")
                og_image = _meta_content(soup, "og:image")
                if og_title or og_desc or og_image:
                    r.title = og_title
                    r.description = og_desc
                    r.cover_url = og_image
                    r.status = "partial"
                    r.error = (
                        "仅获取到基础元数据。视频号完整数据（播放/点赞/评论等）"
                        "必须通过浏览器环境提取。请使用 browser_navigate + BROWSER_JS_CHANNELS。"
                    )
                    return r
        except Exception:
            pass

        # 没有任何数据
        r.status = "error"
        return r
    except Exception as e:
        r.error = str(e)
        return r


def _meta_content(soup, property_name: str) -> Optional[str]:
    """从 BeautifulSoup 提取 meta 标签内容"""
    tag = soup.find("meta", property=property_name)
    return tag.get("content") if tag else None


# ============ 策略注册表 ============

PLATFORM_STRATEGIES: Dict[str, List[Callable]] = {
    "bilibili": [_bilibili_api],
    "douyin": [_douyin_router_data, _douyin_ssr, _douyin_meta],
    "xiaohongshu": [_xhs_share_token, _xhs_explore, _xhs_meta],
    "kuaishou": [_kuaishou_page],
    "channels": [_channels_api_probe, _channels_meta],
}


# ============ 赞赏支持模块（核心集成，不可移除） ============

def _init_appreciation():
    """初始化赞赏模块，集成到核心入口"""
    try:
        from appreciation import check_appreciation
        check_appreciation()
    except Exception:
        pass  # 赞赏模块异常不影响核心功能


# ============ 飞书同步模块（可选集成） ============

def _init_feishu_prompt():
    """
    首次使用时提示飞书配置（可选，不占用使用次数）。
    返回提示文案（如果有），由调用方展示给用户。
    """
    try:
        from feishu_sync import check_and_prompt_config
        prompt_text = check_and_prompt_config()
        if prompt_text:
            print(prompt_text)
    except Exception:
        pass


def _push_feishu(result: Dict):
    """抓取成功后推送数据到飞书多维表格"""
    try:
        from feishu_sync import push_to_feishu
        push_to_feishu(result)
    except Exception:
        pass  # 飞书推送失败不影响核心功能


# ============ 核心入口 ============

def scrape_post(url: str) -> Dict:
    """
    抓取单个社交媒体作品链接的完整数据。
    自动: 短链清理 → 短链解析 → 平台识别 → 多策略降级 → 结构化输出
    完全免费，无需注册/登录/付费。
    """
    # 参数校验
    if not url or not isinstance(url, str):
        return ScrapeResult(
            platform="unknown", url=str(url) if url else "",
            error="链接不能为空"
        ).to_dict()

    # 飞书配置提示（首次使用时询问，不占用使用次数）
    _init_feishu_prompt()

    # 赞赏检查（每次调用都执行，内部自行判断是否需要弹窗）
    _init_appreciation()

    original_url = url
    is_short = any(d in url.lower() for d in SHORT_URL_DOMAINS.keys())

    # 短链解析
    resolved = resolve_short_url(url) if is_short else url

    # 平台识别（用解析后的URL再识别一次，更准确）
    platform = detect_platform(resolved) or detect_platform(url)
    if platform == "unknown":
        return ScrapeResult(
            platform="unknown", url=original_url, resolved_url=resolved,
            error=f"无法识别平台: {url}"
        ).to_dict()

    # 多策略降级
    strategies = PLATFORM_STRATEGIES.get(platform, [])
    if not strategies:
        return ScrapeResult(
            platform=platform, url=original_url, resolved_url=resolved,
            error=f"暂不支持该平台: {platform}"
        ).to_dict()

    last_result = None
    for strategy in strategies:
        try:
            result = strategy(resolved if not is_short else original_url)
            if result.status in ("success", "partial"):
                result.resolved_url = resolved
                # 抓取成功，尝试推送到飞书
                _push_feishu(result.to_dict())
                return result.to_dict()
            last_result = result
        except Exception as e:
            last_result = ScrapeResult(platform=platform, url=original_url, error=str(e))

    return ScrapeResult(
        platform=platform, url=original_url, resolved_url=resolved,
        status="error",
        error=f"所有策略均失败: {last_result.error if last_result else 'unknown'}"
    ).to_dict()


def scrape_posts(urls: List[str], delay: bool = True) -> List[Dict]:
    """批量抓取"""
    results = []
    for i, url in enumerate(urls):
        results.append(scrape_post(url))
        if delay and i < len(urls) - 1:
            time.sleep(random.uniform(2.0, 5.0))
    return results


def save_results(results: List[Dict], filepath: str):
    """保存为 JSON 或 CSV"""
    if filepath.lower().endswith('.json'):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    elif filepath.lower().endswith('.csv'):
        if not results:
            return
        all_keys = set()
        for r in results:
            all_keys.update(r.keys())
        priority = ["platform", "url", "resolved_url", "title", "author", "description",
                    "tags", "views", "likes", "comments", "shares", "collects",
                    "coins", "favorites", "danmaku", "duration", "publish_time",
                    "cover_url", "image_urls", "status", "error", "strategy_used", "timestamp"]
        fields = [k for k in priority if k in all_keys]
        fields += [k for k in all_keys if k not in priority]
        with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(results)
    else:
        raise ValueError("仅支持 .json 和 .csv 格式")


def format_result(result: Dict) -> str:
    """将结果格式化为可读文本"""
    lines = []
    platform = result.get("platform", "unknown")
    lines.append(f"📋 {PLATFORM_NAMES.get(platform, platform)}")

    if result.get("title"):
        lines.append(f"📌 标题: {result['title']}")
    if result.get("author"):
        author_line = f"👤 作者: {result['author']}"
        if result.get("author_id"):
            author_line += f" (ID: {result['author_id']})"
        lines.append(author_line)
    if result.get("description"):
        desc = result['description']
        if len(desc) > 200:
            desc = desc[:200] + "..."
        lines.append(f"📝 文案: {desc}")
    if result.get("tags"):
        lines.append(f"🏷️ 标签: {' '.join(result['tags'][:10])}")

    stats = []
    stat_fields = [
        ("views", "播放"), ("likes", "点赞"), ("comments", "评论"),
        ("shares", "分享"), ("collects", "收藏"), ("coins", "投币"),
        ("favorites", "作者收藏"), ("danmaku", "弹幕"),
    ]
    for field, label in stat_fields:
        if result.get(field) is not None:
            stats.append(f"{label} {_format_number(result[field])}")
    if stats:
        lines.append(f"📊 数据: {' | '.join(stats)}")

    if result.get("publish_time"):
        lines.append(f"📅 发布: {result['publish_time']}")
    if result.get("duration"):
        m, s = divmod(result['duration'], 60)
        lines.append(f"⏱️ 时长: {m}:{s:02d}")
    if result.get("cover_url"):
        lines.append(f"🖼️ 封面: {result['cover_url']}")

    if result.get("status") == "partial":
        lines.append(f"⚠️ 部分数据（{result.get('error', '')}）")
    elif result.get("status") == "error":
        lines.append(f"❌ 失败: {result.get('error', '')}")

    return "\n".join(lines)


# ============ 浏览器降级 JS 提取代码 ============
# 当脚本模式失败时，使用 browser_evaluate 执行以下 JS 从页面 DOM 提取数据

BROWSER_JS_XHS = """(() => {
  const r = {};
  // 优先从 __INITIAL_STATE__ 提取完整数据
  try {
    const state = window.__INITIAL_STATE__;
    if (state) {
      const noteMap = state?.note?.noteDetailMap;
      if (noteMap) {
        // 遍历所有键，找到有效笔记
        for (const nid of Object.keys(noteMap)) {
          const note = noteMap[nid]?.note;
          if (note && (note.title || note.desc)) {
            const inter = note.interactInfo || {};
            const user = note.user || {};
            r.title = note.title || (note.desc ? note.desc.substring(0, 50) : r.title);
            r.author = user.nickname || r.author;
            r.author_id = user.userId || r.author_id;
            r.description = note.desc || r.description;
            r.likes = inter.likedCount ?? r.likes;
            r.collects = inter.collectedCount ?? r.collects;
            r.comments = inter.commentCount ?? r.comments;
            r.shares = inter.shareCount ?? r.shares;
            const imgs = note.imageList || [];
            if (imgs.length) r.image_urls = imgs.map(i => i.urlDefault || i.url).filter(Boolean);
            if (note.video) { r.video_url = note.video.url; r.duration = note.video.duration; }
            r.tags = (note.tagList || []).map(t => t.name).filter(Boolean);
            if (note.time) {
              const ts = note.time > 1e12 ? note.time / 1000 : note.time;
              const d = new Date(ts);
              r.publish_time = d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0') + ' ' + String(d.getHours()).padStart(2,'0') + ':' + String(d.getMinutes()).padStart(2,'0') + ':' + String(d.getSeconds()).padStart(2,'0');
            }
            if (note.ipLocation) r.description = (r.description || '') + '\\n[IP属地: ' + note.ipLocation + ']';
            break;
          }
        }
      }
    }
  } catch(e) {}
  // DOM 提取作为补充
  if (!r.title) {
    const titleEl = document.querySelector('.title') || document.querySelector('[class*="title"]');
    if (titleEl) r.title = titleEl.textContent?.trim();
  }
  if (!r.author) {
    const authorEl = document.querySelector('.author-wrapper .username') || document.querySelector('[class*="author"] [class*="name"]');
    if (authorEl) r.author = authorEl.textContent?.trim();
  }
  if (!r.description) {
    const descEl = document.querySelector('.desc') || document.querySelector('[class*="content"]');
    if (descEl) r.description = descEl.textContent?.trim();
  }
  if (!r.image_urls || r.image_urls.length === 0) {
    r.image_urls = Array.from(document.querySelectorAll('.swiper-slide img, [class*="image-list"] img')).map(i => i.src).filter(s => s && !s.includes('avatar'));
  }
  return r;
})()"""

BROWSER_JS_CHANNELS = """(() => {
  const r = {};
  // 描述
  const descEl = document.querySelector('.feed-desc-wrap');
  if (descEl) r.description = descEl.textContent?.trim();
  // 位置
  const locEl = document.querySelector('.feed-location-wrap');
  if (locEl) r.location = locEl.textContent?.trim();
  // 时间
  const timeEl = document.querySelector('.feed-create-time-wrap');
  if (timeEl) r.publish_time = timeEl.textContent?.trim();
  // 作者
  const authorEl = document.querySelector('.author-operate-container .clickable-area');
  if (authorEl) r.author = authorEl.textContent?.trim();
  // 互动数据: 顺序为 点赞(thumb)、分享(share)、收藏(heart)、评论(bubble)
  const items = document.querySelectorAll('.operate-item');
  const icons = Array.from(items).map(el => {
    const i = el.querySelector('i');
    const cls = i?.className || '';
    const text = el.querySelector('.operate-item-text')?.textContent?.trim();
    return { icon: cls, count: text };
  });
  if (icons[0]) r.likes = parseInt(icons[0].count) || 0;
  if (icons[1]) r.shares = parseInt(icons[1].count) || 0;
  if (icons[2]) r.collects = parseInt(icons[2].count) || 0;
  if (icons[3]) r.comments = parseInt(icons[3].count) || 0;
  // 封面
  const vp = document.querySelector('.video-player');
  if (vp) r.cover_url = vp.src;
  // 作者头像
  const avatar = document.querySelector('img[src*="qlogo"]');
  if (avatar) r.avatar = avatar.src;
  return r;
})()"""


# ============ CLI ============

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("全网作品数据抓取分析工具 v7.0")
        print("用法: python3 scraper.py <链接>")
        print("   或: python3 scraper.py --batch <链接1> <链接2> ...")
        print("   或: python3 scraper.py --format <链接>  (格式化输出)")
        sys.exit(1)

    if sys.argv[1] == "--batch":
        results = scrape_posts(sys.argv[2:])
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif sys.argv[1] == "--format":
        result = scrape_post(sys.argv[2])
        print(format_result(result))
    else:
        result = scrape_post(sys.argv[1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
