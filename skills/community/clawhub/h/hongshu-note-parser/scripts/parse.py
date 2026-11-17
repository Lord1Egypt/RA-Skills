#!/usr/bin/env python3
"""
hongshu-note-parser — 小红书笔记解析采集层
解析小红书图文/视频笔记，提取标题/正文/图片/标签/互动数据，输出结构化 JSON。
分析由调用方 AI 完成，不内嵌任何 LLM API。

用法:
    # 采集模式（默认）：解析笔记，stdout 输出 JSON
    python parse.py "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy"

    # 生成 HTML 模式：读分析 JSON，生成胶囊卡片报告
    python parse.py --generate-html analysis.json
"""

import argparse
import base64
import datetime as dt
import html
import json
import os
import re
import sys
import tempfile
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

# Fix Windows GBK encoding
if sys.platform == "win32":
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


# ═══════════════════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════════════════

XHS_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

XHS_HEADERS = {
    "User-Agent": XHS_UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.xiaohongshu.com/",
}


# ═══════════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════════

def _safe_filename(s: str, max_len: int = 40) -> str:
    for ch in r'\/:*?"<>|':
        s = s.replace(ch, "_")
    return s.strip().replace(" ", "_")[:max_len]


def _e(s) -> str:
    """HTML escape，防止 XSS。"""
    if s is None:
        return ""
    return html.escape(str(s), quote=True)


def _e_safe(s) -> str:
    """HTML escape 但保留 <em></em> 标签（用于 summary 高亮）。"""
    if s is None:
        return ""
    s = html.escape(str(s), quote=True)
    s = s.replace("&lt;em&gt;", "<em>").replace("&lt;/em&gt;", "</em>")
    return s


def _normalize_url(url: str) -> str:
    """补全协议。"""
    if url.startswith("//"):
        return "https:" + url
    if not url.startswith("http"):
        return "https://" + url
    return url


def _http_get(url: str, headers: dict = None, timeout: int = 20) -> str:
    """urllib GET 请求，返回 HTML 文本。"""
    req = urllib.request.Request(url, headers=headers or XHS_HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _http_download(url: str, dest: Path, headers: dict = None, timeout: int = 60) -> bool:
    """urllib 下载文件到指定路径。"""
    req = urllib.request.Request(url, headers=headers or XHS_HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        with open(dest, "wb") as f:
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                f.write(chunk)
    return dest.exists()


def _image_to_base64(img_ref: str, analysis_dir: Path = None) -> str:
    """
    将图片转为 base64 data URI，用于 HTML 内嵌。
    支持本地文件路径和 HTTP URL。
    返回 data URI 字符串，失败返回空字符串。
    """
    if not img_ref:
        return ""

    # 本地文件路径
    local_path = None
    if os.path.isfile(img_ref):
        local_path = Path(img_ref)
    elif analysis_dir:
        # 尝试相对于分析 JSON 目录的路径
        candidate = analysis_dir / img_ref
        if candidate.is_file():
            local_path = candidate

    if local_path:
        try:
            data = local_path.read_bytes()
            ext = local_path.suffix.lower()
            mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
                    "webp": "image/webp", "gif": "image/gif"}.get(ext.lstrip("."), "image/jpeg")
            b64 = base64.b64encode(data).decode("ascii")
            return f"data:{mime};base64,{b64}"
        except Exception:
            return ""

    # HTTP URL — 下载并转 base64
    if img_ref.startswith("http"):
        # 不同域名需要不同的 Referer 才能下载
        referer_list = [XHS_HEADERS.get("Referer", "")]
        if "docs.qq.com" in img_ref or "docimg" in img_ref:
            referer_list = ["https://docs.qq.com/", "https://www.docs.qq.com/"]
        elif "xiaohongshu" in img_ref or "xhscdn" in img_ref or "sns-img" in img_ref:
            referer_list = ["https://www.xiaohongshu.com/"]
        else:
            referer_list = ["https://www.xiaohongshu.com/", "https://docs.qq.com/", ""]

        for referer in referer_list:
            try:
                hdrs = {"User-Agent": XHS_HEADERS.get("User-Agent", "Mozilla/5.0")}
                if referer:
                    hdrs["Referer"] = referer
                req = urllib.request.Request(img_ref, headers=hdrs)
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = resp.read()
                    if len(data) < 100:
                        continue
                    ct = resp.headers.get("Content-Type", "")
                    if "image" in ct:
                        mime = ct.split(";")[0].strip()
                    elif ".png" in img_ref.lower():
                        mime = "image/png"
                    elif ".webp" in img_ref.lower():
                        mime = "image/webp"
                    elif ".gif" in img_ref.lower():
                        mime = "image/gif"
                    else:
                        mime = "image/jpeg"
                    b64 = base64.b64encode(data).decode("ascii")
                    return f"data:{mime};base64,{b64}"
            except Exception:
                continue
        return ""

    return ""
# 1. URL 解析
# ═══════════════════════════════════════════════════════════

def parse_url(raw_url: str) -> tuple:
    """
    从 URL 中提取 note_id 和 xsec_token。
    支持长链、短链（xhslink.com）、分享文本。
    返回 (note_id, xsec_token, full_url)。
    """
    # 从分享文本中提取 URL
    url_match = re.search(r'(https?://[^\s]+)', raw_url)
    if url_match:
        url = url_match.group(1)
    else:
        url = raw_url.strip()

    # 短链跟随重定向
    if "xhslink.com" in url:
        try:
            print("  [XHS] 跟随短链重定向...", file=sys.stderr)
            req = urllib.request.Request(url, headers=XHS_HEADERS)
            with urllib.request.urlopen(req, timeout=15) as resp:
                url = resp.geturl()
                print(f"  [XHS] 重定向到: {url[:80]}...", file=sys.stderr)
        except Exception as e:
            print(f"  [XHS] 短链跟随失败: {e}", file=sys.stderr)

    # 提取 note_id
    # 匹配 /explore/<id> 或 /discovery/item/<id>
    note_id = None
    m = re.search(r'xiaohongshu\.com/(?:explore|discovery/item)/([a-zA-Z0-9]+)', url)
    if m:
        note_id = m.group(1)
    else:
        # 尝试从路径中提取
        m2 = re.search(r'/([a-zA-Z0-9]{24})', url)
        if m2:
            note_id = m2.group(1)

    # 提取 xsec_token
    xsec_token = None
    tm = re.search(r'xsec_token=([^&]+)', url)
    if tm:
        xsec_token = tm.group(1)

    if not note_id:
        return None, None, url

    # 构建完整 URL
    full_url = f"https://www.xiaohongshu.com/explore/{note_id}"
    if xsec_token:
        full_url += f"?xsec_token={xsec_token}&xsec_source=pc_share"

    return note_id, xsec_token, full_url


# ═══════════════════════════════════════════════════════════
# 2. 内容抓取
# ═══════════════════════════════════════════════════════════

def fetch_note_page(note_id: str, xsec_token: str = None) -> str:
    """获取小红书笔记页面 HTML。"""
    url = f"https://www.xiaohongshu.com/explore/{note_id}"
    if xsec_token:
        url += f"?xsec_token={xsec_token}&xsec_source=pc_share"

    print(f"  [XHS] 请求笔记页面...", file=sys.stderr)
    return _http_get(url)


def extract_initial_state(html_content: str) -> dict | None:
    """
    从页面 HTML 中提取 window.__INITIAL_STATE__。
    使用大括号匹配而非正则，更健壮。
    """
    marker = 'window.__INITIAL_STATE__='
    idx = html_content.find(marker)
    if idx == -1:
        return None

    start = idx + len(marker)
    # 跳过可能的空白
    while start < len(html_content) and html_content[start] in ' \n\t':
        start += 1
    if start >= len(html_content) or html_content[start] != '{':
        return None

    # 大括号匹配找到 JSON 结尾
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(html_content)):
        c = html_content[i]
        if escape:
            escape = False
            continue
        if c == '\\':
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                json_str = html_content[start:i + 1]
                # 替换 undefined 为 null
                json_str = re.sub(r'\bundefined\b', 'null', json_str)
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    return None
    return None


def extract_meta_fallback(html_content: str) -> dict:
    """
    降级方案：从 og: meta 标签提取基本信息。
    当 __INITIAL_STATE__ 不可用时使用。
    """
    result = {}

    def _meta(prop):
        m = re.search(
            rf'<meta\s+[^>]*property=["\']og:{prop}["\'][^>]*content=["\']([^"\']*)["\']',
            html_content, re.IGNORECASE
        )
        if not m:
            m = re.search(
                rf'<meta\s+[^>]*content=["\']([^"\']*)["\'][^>]*property=["\']og:{prop}["\']',
                html_content, re.IGNORECASE
            )
        return m.group(1) if m else None

    title = _meta("title")
    desc = _meta("description")
    image = _meta("image")

    if title:
        result["title"] = title
    if desc:
        result["desc"] = desc
    if image:
        result["images"] = [{"url": _normalize_url(image)}]

    return result if result else None


def _build_fallback_note(fallback: dict, note_id: str) -> dict:
    """从 meta 标签降级数据构建笔记数据结构。"""
    raw_images = fallback.get("images", [])
    # images 可能是 [{"url": "..."}] 格式
    images = []
    for img in raw_images:
        if isinstance(img, dict):
            url = img.get("url", "")
        else:
            url = str(img)
        if url:
            images.append({"url": url, "width": 0, "height": 0, "local_path": ""})

    return {
        "note_id": note_id,
        "title": fallback.get("title", ""),
        "desc": fallback.get("desc", ""),
        "note_type": "图文笔记",
        "publish_date": "",
        "author": {"nickname": "", "user_id": "", "avatar_url": "", "red_id": ""},
        "images": images,
        "video_url": None,
        "interactions": {"liked_count": "0", "collected_count": "0",
                         "comment_count": "0", "share_count": "0"},
        "tags": [],
        "topics": [],
    }


# ═══════════════════════════════════════════════════════════
# 3. 数据提取
# ═══════════════════════════════════════════════════════════

def parse_note_data(state: dict, note_id: str) -> dict | None:
    """从 __INITIAL_STATE__ 中提取笔记数据。"""
    note_section = state.get("note", {})
    note_detail_map = note_section.get("noteDetailMap", {})

    # 优先精确匹配 note_id
    note_data = None
    if note_id and note_id in note_detail_map:
        note_data = note_detail_map[note_id].get("note")

    # 降级：取第一个可用的笔记
    if not note_data:
        for key, val in note_detail_map.items():
            if isinstance(val, dict) and val.get("note"):
                note_data = val["note"]
                break

    if not note_data:
        return None

    return _extract_note_fields(note_data)


def _extract_note_fields(note: dict) -> dict:
    """从笔记数据中提取结构化字段。"""
    # 基本信息
    title = note.get("title", "")
    desc = note.get("desc", "")
    note_type_raw = note.get("type", "normal")
    note_type = "视频笔记" if note_type_raw == "video" else "图文笔记"
    note_id = note.get("noteId", "")
    time_str = note.get("time", "")
    last_update = note.get("lastUpdateTime", "")

    # 发布时间转换（毫秒时间戳 → 日期）
    publish_date = ""
    if time_str:
        try:
            ts = int(time_str)
            if ts > 1e12:  # 毫秒
                ts = ts / 1000
            publish_date = dt.datetime.fromtimestamp(ts).strftime("%Y.%m.%d")
        except (ValueError, OSError):
            pass

    # 作者信息
    user = note.get("user", {})
    author = {
        "nickname": user.get("nickname", ""),
        "user_id": user.get("userId", ""),
        "avatar_url": _normalize_url(user.get("avatar", "")) if user.get("avatar") else "",
        "red_id": user.get("redId", ""),
    }

    # 图片列表
    image_list = note.get("imageList", [])
    images = []
    for img in image_list:
        url = img.get("urlDefault", "") or img.get("urlPre", "") or img.get("url", "")
        if url:
            url = _normalize_url(url)
            images.append({
                "url": url,
                "width": img.get("width", 0),
                "height": img.get("height", 0),
                "local_path": "",  # 下载后填充
            })

    # 视频信息（如果是视频笔记）
    video_url = None
    video = note.get("video", {})
    if video:
        media = video.get("media", {})
        stream = media.get("stream", {})
        for codec in ["h264", "h265", "h266", "av1"]:
            streams = stream.get(codec, [])
            if streams:
                video_url = streams[0].get("masterUrl", "")
                if video_url:
                    break

    # 互动数据
    interact = note.get("interactInfo", {})
    interactions = {
        "liked_count": interact.get("likedCount", "0"),
        "collected_count": interact.get("collectedCount", "0"),
        "comment_count": interact.get("commentCount", "0"),
        "share_count": interact.get("shareCount", "0"),
    }

    # 标签列表
    tag_list = note.get("tagList", [])
    tags = []
    for tag in tag_list:
        name = tag.get("name", "")
        if name:
            tags.append(name)

    # 从正文中提取话题标签（#xxx 格式）
    if desc:
        desc_tags = re.findall(r'#([^#\s]+?)(?:\[话题\])?#', desc)
        for t in desc_tags:
            if t not in tags:
                tags.append(t)

    # 话题
    topic_list = []
    if tag_list:
        for tag in tag_list:
            if tag.get("type") == "topic":
                topic_list.append(tag.get("name", ""))

    return {
        "note_id": note_id,
        "title": title,
        "desc": desc,
        "note_type": note_type,
        "publish_date": publish_date,
        "author": author,
        "images": images,
        "video_url": video_url,
        "interactions": interactions,
        "tags": tags,
        "topics": topic_list,
    }


# ═══════════════════════════════════════════════════════════
# 4. 图片下载
# ═══════════════════════════════════════════════════════════

def download_images(note_data: dict, out_dir: Path, prefix: str) -> dict:
    """下载笔记图片到输出目录，更新 local_path。"""
    images = note_data.get("images", [])
    if not images:
        return note_data

    img_dir = out_dir / f"{prefix}-img"
    img_dir.mkdir(parents=True, exist_ok=True)

    for i, img in enumerate(images):
        url = img.get("url", "")
        if not url:
            continue
        ext = ".jpg"
        if ".png" in url:
            ext = ".png"
        elif ".webp" in url:
            ext = ".webp"
        dest = img_dir / f"img_{i}{ext}"
        try:
            print(f"  [XHS] 下载图片 {i + 1}/{len(images)}...", file=sys.stderr)
            if _http_download(url, dest):
                img["local_path"] = str(dest)
            else:
                print(f"  [XHS] 图片 {i + 1} 下载失败", file=sys.stderr)
        except Exception as e:
            print(f"  [XHS] 图片 {i + 1} 下载失败: {e}", file=sys.stderr)

    note_data["images"] = images
    return note_data


# ═══════════════════════════════════════════════════════════
# 5. HTML 报告生成 — 胶囊卡片交互式布局
# ═══════════════════════════════════════════════════════════

HTML_CSS = """
  :root {
    --bg: oklch(0.975 0.005 90);
    --surface: #fff;
    --text: oklch(0.18 0.01 90);
    --text-secondary: oklch(0.42 0.01 90);
    --text-muted: oklch(0.58 0.01 90);
    --accent: oklch(0.55 0.20 25);
    --accent-light: oklch(0.70 0.14 28);
    --accent-bg: oklch(0.93 0.05 28);
    --border: oklch(0.88 0.01 85);
    --shadow-sm: 0 1px 3px oklch(0 0 0 / 0.06);
    --shadow-md: 0 4px 16px oklch(0 0 0 / 0.08);
    --shadow-lg: 0 8px 32px oklch(0 0 0 / 0.10);
    --radius-sm: 8px;
    --radius-md: 14px;
    --radius-lg: 22px;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    font-family: system-ui, -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
    background:var(--bg); color:var(--text);
    line-height:1.75; -webkit-font-smoothing:antialiased;
  }
  .container { max-width:880px; margin:0 auto; padding:0 24px; }

  .hero { text-align:center; padding:80px 0 40px; }
  .hero-badge { display:inline-flex; align-items:center; gap:8px; padding:6px 18px; border-radius:999px; background:oklch(0.94 0.02 30 / 0.5); border:1px solid oklch(0.85 0.06 30 / 0.3); font-size:13px; color:var(--accent); font-weight:500; letter-spacing:0.5px; margin-bottom:28px; }
  .hero-badge .dot { width:6px; height:6px; border-radius:50%; background:var(--accent); }
  .hero h1 { font-family:'PingFang SC', 'Noto Serif CJK SC', serif; font-size:clamp(1.6rem, 4.5vw, 2.6rem); font-weight:900; line-height:1.3; letter-spacing:0.03em; margin-bottom:16px; }
  .hero-meta { font-size:13px; color:var(--text-muted); display:flex; justify-content:center; gap:20px; flex-wrap:wrap; margin-bottom:20px; }

  .stats-bar { display:flex; justify-content:center; gap:28px; padding:16px 0; }
  .stat { display:flex; align-items:center; gap:6px; }
  .stat-icon { font-size:16px; }
  .stat-num { font-weight:700; font-size:15px; color:var(--text); }
  .stat-label { font-size:11px; color:var(--text-muted); }

  .gallery { display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:12px; margin-bottom:56px; }
  .gallery-item { position:relative; cursor:pointer; }
  .gallery-item .gallery-img { width:100%; border-radius:var(--radius-md); box-shadow:var(--shadow-sm); border:1px solid var(--border); transition:transform 0.2s, box-shadow 0.2s; display:block; }
  .gallery-item:hover .gallery-img { transform:scale(1.02); box-shadow:var(--shadow-lg); }
  .gallery-failed { display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:200px; border-radius:var(--radius-md); border:2px dashed var(--border); background:oklch(0.95 0.005 90); }
  .gallery-placeholder { text-align:center; color:var(--text-muted); font-size:2rem; line-height:1.5; }
  .gallery-placeholder span { font-size:0.8rem; }
  .gallery-url { font-size:0.7rem; color:var(--text-muted); word-break:break-all; padding:8px; text-align:center; }
  .gallery-count { font-size:0.8rem; color:var(--text-muted); margin-left:auto; padding:2px 10px; background:var(--accent-bg); border-radius:20px; }
  .gallery-count.failed { color:var(--accent); }
  .lightbox { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.9); z-index:9999; align-items:center; justify-content:center; }
  .lightbox.show { display:flex; }
  .lightbox-content { position:relative; max-width:90vw; max-height:90vh; }
  .lightbox-content img { max-width:90vw; max-height:90vh; border-radius:8px; }
  .lightbox-close { position:absolute; top:-40px; right:0; background:none; border:none; color:#fff; font-size:2rem; cursor:pointer; }
  .lightbox-prev, .lightbox-next { position:absolute; top:50%; transform:translateY(-50%); background:none; border:none; color:#fff; font-size:3rem; cursor:pointer; padding:16px; opacity:0.7; }
  .lightbox-prev { left:-60px; } .lightbox-next { right:-60px; }
  .lightbox-prev:hover, .lightbox-next:hover { opacity:1; }

  .summary-card { background:var(--surface); border-radius:var(--radius-lg); padding:48px 40px; margin:0 0 56px; box-shadow:var(--shadow-lg); border:1px solid var(--border); position:relative; overflow:hidden; }
  .summary-card::before { content:''; position:absolute; top:0; left:0; width:4px; height:100%; background:linear-gradient(180deg,var(--accent),var(--accent-light)); border-radius:4px 0 0 4px; }
  .summary-card .label { font-size:11px; text-transform:uppercase; letter-spacing:0.14em; color:var(--accent); font-weight:600; margin-bottom:16px; }
  .summary-card .big-text { font-family:'PingFang SC', 'Noto Serif CJK SC', serif; font-size:clamp(1.15rem, 2.2vw, 1.45rem); font-weight:600; color:var(--text); line-height:1.9; }
  .summary-card .big-text em { font-style:normal; color:var(--accent); font-weight:700; }

  .quotes-section { margin-bottom:64px; }
  .section-head { display:flex; align-items:center; gap:12px; margin-bottom:28px; }
  .section-head .icon { width:32px; height:32px; border-radius:8px; background:var(--accent-bg); display:flex; align-items:center; justify-content:center; font-size:16px; }
  .section-head h2 { font-family:'PingFang SC', 'Noto Serif CJK SC', serif; font-size:1.4rem; font-weight:700; color:var(--text); }

  .visual-section { margin-bottom:64px; }
  .visual-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:16px; }
  .visual-card { background:var(--surface); border-radius:var(--radius-md); padding:28px 24px; box-shadow:var(--shadow-md); border:1px solid var(--border); transition:transform 0.2s ease,box-shadow 0.2s ease; }
  .visual-card:hover { transform:translateY(-2px); box-shadow:var(--shadow-lg); }
  .visual-card .vc-label { font-size:12px; text-transform:uppercase; letter-spacing:0.1em; color:var(--accent); font-weight:600; margin-bottom:10px; }
  .visual-card .vc-body { font-size:0.88rem; color:var(--text-secondary); line-height:1.8; }

  .capsule-quotes { display:flex; flex-direction:column; gap:16px; }
  .capsule-quote { display:flex; gap:12px; align-items:flex-start; padding:16px 20px; background:oklch(0.97 0.005 88); border-radius:var(--radius-sm); }
  .capsule-quote .cq-mark { font-family:'PingFang SC', 'Noto Serif CJK SC', serif; font-size:2rem; font-weight:900; color:var(--accent-bg); line-height:0.8; flex-shrink:0; }
  .capsule-quote .cq-text { font-family:'PingFang SC', 'Noto Serif CJK SC', serif; font-size:1rem; font-weight:600; color:var(--text); line-height:1.7; }

  .bookshelf-section { margin-bottom:64px; }
  .capsule-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:14px; }
  .capsule { background:var(--surface); border-radius:var(--radius-md); padding:24px 20px; box-shadow:var(--shadow-sm); border:1px solid var(--border); cursor:pointer; transition:all 0.25s ease; }
  .capsule:hover { box-shadow:var(--shadow-md); transform:translateY(-1px); border-color:var(--accent-light); }
  .capsule .cap-icon { font-size:1.6rem; margin-bottom:12px; display:block; }
  .capsule .cap-title { font-family:'PingFang SC', 'Noto Serif CJK SC', serif; font-size:0.95rem; font-weight:700; color:var(--text); margin-bottom:4px; }
  .capsule .cap-sub { font-size:12px; color:var(--text-muted); line-height:1.5; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }

  .capsule-detail { display:none; margin-top:16px; background:var(--surface); border-radius:var(--radius-lg); padding:40px 36px; box-shadow:var(--shadow-lg); border:1px solid var(--border); position:relative; animation:slideUp 0.3s ease; }
  .capsule-detail.active { display:block; }
  @keyframes slideUp { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:translateY(0); } }
  .capsule-detail .close-btn { position:absolute; top:16px; right:20px; width:36px; height:36px; border-radius:50%; border:1px solid var(--border); background:var(--surface); cursor:pointer; font-size:18px; display:flex; align-items:center; justify-content:center; color:var(--text-muted); transition:all 0.2s; }
  .capsule-detail .close-btn:hover { background:oklch(0.94 0.005 85); color:var(--text); }
  .capsule-detail .detail-title { font-family:'PingFang SC', 'Noto Serif CJK SC', serif; font-size:1.3rem; font-weight:700; color:var(--text); margin-bottom:24px; padding-right:40px; }

  .points-list { display:flex; flex-direction:column; gap:20px; }
  .point-item { display:flex; gap:16px; align-items:flex-start; }
  .point-item .point-num { flex-shrink:0; width:36px; height:36px; border-radius:10px; background:var(--accent-bg); display:flex; align-items:center; justify-content:center; font-weight:700; font-size:14px; color:var(--accent); }
  .point-item .point-content h4 { font-size:0.95rem; font-weight:700; color:var(--text); margin-bottom:4px; }
  .point-item .point-content p { font-size:0.85rem; color:var(--text-secondary); line-height:1.7; }

  .struct-list { display:flex; flex-direction:column; gap:16px; }
  .struct-item { display:flex; gap:16px; align-items:baseline; }
  .struct-item .struct-label { flex-shrink:0; font-weight:700; font-size:0.88rem; color:var(--accent); min-width:80px; }
  .struct-item .struct-content { font-size:0.9rem; color:var(--text-secondary); line-height:1.7; }

  .judge-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:16px; }
  .judge-mini { padding:20px; background:oklch(0.97 0.005 88); border-radius:var(--radius-sm); }
  .judge-mini .jm-label { font-size:11px; text-transform:uppercase; letter-spacing:0.08em; color:var(--accent); font-weight:600; margin-bottom:8px; }
  .judge-mini .jm-title { font-weight:700; font-size:0.9rem; margin-bottom:6px; color:var(--text); }
  .judge-mini .jm-desc { font-size:0.82rem; color:var(--text-secondary); line-height:1.7; }

  .highlight-list { display:flex; flex-direction:column; gap:1px; background:var(--border); border-radius:var(--radius-sm); overflow:hidden; }
  .highlight-item { display:grid; grid-template-columns:44px 1fr auto; align-items:center; gap:16px; padding:14px 18px; background:var(--surface); }
  .highlight-item .hl-rank { font-family:'PingFang SC', 'Noto Serif CJK SC', serif; font-size:1.5rem; font-weight:900; color:var(--accent-light); text-align:center; }
  .highlight-item .hl-rank.top3 { color:var(--accent); }
  .highlight-item .hl-name { font-weight:700; font-size:0.9rem; color:var(--text); }
  .highlight-item .hl-desc { font-size:0.82rem; color:var(--text-secondary); margin-top:2px; }
  .highlight-item .hl-tag { font-size:11px; padding:3px 10px; border-radius:999px; background:oklch(0.95 0.005 90); color:var(--text-muted); white-space:nowrap; }

  .footer { text-align:center; padding:48px 0; border-top:1px solid var(--border); margin-top:32px; color:var(--text-muted); font-size:13px; line-height:1.8; }

  @media (max-width:640px) {
    .summary-card { padding:32px 24px; }
    .capsule-grid { grid-template-columns:repeat(2,1fr); }
    .capsule-detail { padding:28px 20px; }
    .hero { padding:48px 0 32px; }
    .visual-grid { grid-template-columns:1fr; }
    .stats-bar { gap:16px; }
  }
"""

HTML_PAGE_TOP = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · 小红书笔记解析</title>
<style>{css}</style>
</head>
<body>
<div class="container">
"""

HTML_PAGE_BOTTOM = """
<footer class="footer">
  <p style="font-weight:600;color:var(--text)">hongshu-note-parser</p>
  <p style="font-size:12px;margin-top:2px">丢一条小红书笔记链接，还你一份结构化品牌分析</p>
</footer>
</div>

<script>
var activeCapsule = null;
document.addEventListener('click', function(e) {
  var cap = e.target.closest('[data-cid]');
  if (cap) {
    var cid = cap.getAttribute('data-cid');
    if (activeCapsule) activeCapsule.classList.remove('active');
    var detail = document.getElementById('detail-' + cid);
    if (detail) {
      detail.classList.add('active');
      detail.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      activeCapsule = detail;
    }
    return;
  }
  var closeBtn = e.target.closest('.close-btn');
  if (closeBtn) {
    if (activeCapsule) { activeCapsule.classList.remove('active'); activeCapsule = null; }
    return;
  }
});
</script>
</body>
</html>"""


def _render_hero(analysis: dict) -> str:
    """渲染 Hero 区域。"""
    meta = analysis.get("meta", {})
    title = _e(meta.get("title", ""))
    note_type = _e(meta.get("note_type", ""))
    date = _e(meta.get("date", dt.datetime.now().strftime("%Y.%m.%d")))
    author = _e(meta.get("author", ""))

    badge_text = "小红书笔记 · 品牌解析"

    meta_items = []
    if author:
        meta_items.append(f'<span>@{author}</span>')
    if note_type:
        meta_items.append(f'<span>{note_type}</span>')
    meta_items.append(f'<span>{date}</span>')

    # 互动数据栏
    stats = meta.get("stats", {})
    stats_html = ""
    if stats:
        stat_items = []
        if stats.get("likes"):
            stat_items.append(f'<span class="stat"><span class="stat-icon">&#128077;</span><span class="stat-num">{_e(stats["likes"])}</span><span class="stat-label">赞</span></span>')
        if stats.get("collects"):
            stat_items.append(f'<span class="stat"><span class="stat-icon">&#11088;</span><span class="stat-num">{_e(stats["collects"])}</span><span class="stat-label">收藏</span></span>')
        if stats.get("comments"):
            stat_items.append(f'<span class="stat"><span class="stat-icon">&#128172;</span><span class="stat-num">{_e(stats["comments"])}</span><span class="stat-label">评论</span></span>')
        if stats.get("shares"):
            stat_items.append(f'<span class="stat"><span class="stat-icon">&#128279;</span><span class="stat-num">{_e(stats["shares"])}</span><span class="stat-label">分享</span></span>')
        if stat_items:
            stats_html = f'<div class="stats-bar">{"".join(stat_items)}</div>'

    hero = f'<header class="hero">\n'
    hero += f'  <div class="hero-badge"><span class="dot"></span>{badge_text}</div>\n'
    hero += f'  <h1>{title}</h1>\n'
    if meta_items:
        hero += f'  <div class="hero-meta">{"".join(meta_items)}</div>\n'
    hero += stats_html
    hero += f'</header>\n'
    return hero


def _render_image_gallery(analysis: dict, analysis_dir: Path = None) -> str:
    """渲染笔记图片画廊 — base64 内嵌 + 点击放大灯箱。"""
    images = analysis.get("meta", {}).get("images", [])
    if not images:
        return ""

    imgs_html = ""
    success_count = 0
    fail_count = 0
    for i, img in enumerate(images):
        # 支持 string 和 {url, local_path} 两种格式
        if isinstance(img, dict):
            img_ref = img.get("local_path") or img.get("url", "")
        else:
            img_ref = img

        data_uri = _image_to_base64(img_ref, analysis_dir)
        if data_uri:
            imgs_html += f'    <div class="gallery-item" data-idx="{i}">\n'
            imgs_html += f'      <img src="{data_uri}" class="gallery-img" loading="lazy" />\n'
            imgs_html += f'    </div>\n'
            success_count += 1
        else:
            # 占位卡片
            url_display = _e(img_ref[:80] + "..." if len(img_ref) > 80 else img_ref)
            imgs_html += f'    <div class="gallery-item gallery-failed" data-idx="{i}">\n'
            imgs_html += f'      <div class="gallery-placeholder">&#128247;<br/><span>图片加载失败</span></div>\n'
            imgs_html += f'      <div class="gallery-url" title="{_e(img_ref)}">{url_display}</div>\n'
            imgs_html += f'    </div>\n'
            fail_count += 1

    if success_count > 0:
        status_badge = f'<span class="gallery-count">{success_count} 张图片</span>'
    else:
        status_badge = '<span class="gallery-count failed">0 张图片</span>'

    # 灯箱 HTML + JS
    lightbox_html = """
  <div id="xhs-lightbox" class="lightbox" onclick="this.classList.remove('show')">
    <div class="lightbox-content">
      <img id="xhs-lightbox-img" src="" />
      <button class="lightbox-close" onclick="document.getElementById('xhs-lightbox').classList.remove('show')">&times;</button>
      <button class="lightbox-prev" onclick="xhsLightboxNav(-1)">&#8249;</button>
      <button class="lightbox-next" onclick="xhsLightboxNav(1)">&#8250;</button>
    </div>
  </div>
  <script>
    var xhsImages=[],xhsIdx=0;
    document.querySelectorAll('.gallery-item').forEach(function(el){
      var img=el.querySelector('.gallery-img');
      if(img){xhsImages.push(img.src);el.addEventListener('click',function(){
        xhsIdx=parseInt(el.dataset.idx||0);
        document.getElementById('xhs-lightbox-img').src=img.src;
        document.getElementById('xhs-lightbox').classList.add('show');
      });}
    });
    function xhsLightboxNav(d){xhsIdx=(xhsIdx+d+xhsImages.length)%xhsImages.length;
      document.getElementById('xhs-lightbox-img').src=xhsImages[xhsIdx];}
    document.addEventListener('keydown',function(e){
      var lb=document.getElementById('xhs-lightbox');
      if(!lb.classList.contains('show'))return;
      if(e.key==='ArrowLeft')xhsLightboxNav(-1);
      if(e.key==='ArrowRight')xhsLightboxNav(1);
      if(e.key==='Escape')lb.classList.remove('show');
    });
  </script>"""

    return f"""<section class="quotes-section">
  <div class="section-head">
    <div class="icon">&#128247;</div>
    <h2>笔记图片</h2>
    {status_badge}
  </div>
  <div class="gallery">
{imgs_html}  </div>
{lightbox_html}
</section>
"""


def _render_summary(analysis: dict) -> str:
    """渲染一句话总结卡片。"""
    s = analysis.get("summary", "")
    if not s:
        return ""
    return f"""<div class="summary-card">
  <div class="label">一句话总结</div>
  <p class="big-text">{_e_safe(s)}</p>
</div>
"""


def _render_visual_strategy(analysis: dict) -> str:
    """渲染视觉策略分析区（独立区块，品牌策划核心维度）。"""
    items = analysis.get("visual_strategy", [])
    if not items:
        return ""
    cards = ""
    for item in items:
        label = _e(item.get("label", ""))
        body = _e(item.get("body", ""))
        cards += f"""    <div class="visual-card">
      <div class="vc-label">{label}</div>
      <div class="vc-body">{body}</div>
    </div>
"""
    return f"""<section class="visual-section">
  <div class="section-head">
    <div class="icon">&#127912;</div>
    <h2>视觉策略分析</h2>
  </div>
  <div class="visual-grid">
{cards}  </div>
</section>
"""


def _render_quotes_in_capsule(content: list) -> str:
    """渲染胶囊内的金句列表 (type: quotes)。"""
    if not content:
        return ""
    items = ""
    for q in content:
        text = _e(q.get("text", ""))
        items += f"""    <div class="capsule-quote">
      <span class="cq-mark">&ldquo;</span>
      <span class="cq-text">{text}</span>
    </div>
"""
    return f'  <div class="capsule-quotes">\n{items}  </div>\n'


def _render_capsule_section(analysis: dict) -> str:
    """渲染胶囊卡片 + 详情面板。"""
    capsules = analysis.get("capsules", [])
    if not capsules:
        return ""

    # 胶囊卡片网格（使用 data-cid 事件委托，不用 inline onclick）
    cards = ""
    for c in capsules:
        cid = _e(c.get("id", ""))
        icon = _e(c.get("icon", ""))
        title = _e(c.get("title", ""))
        subtitle = _e(c.get("subtitle", ""))
        cards += f"""    <div class="capsule" data-cid="{cid}">
      <span class="cap-icon">{icon}</span>
      <div class="cap-title">{title}</div>
      <div class="cap-sub">{subtitle}</div>
    </div>
"""

    details = ""
    for c in capsules:
        cid = _e(c.get("id", ""))
        ctype = c.get("type", "points")
        dtitle = _e(c.get("detail_title", c.get("title", "")))
        content = c.get("content", [])

        detail_html = ""
        if ctype == "points":
            detail_html = _render_points(content)
        elif ctype == "structure":
            detail_html = _render_structure(content)
        elif ctype == "judgment":
            detail_html = _render_judgment(content)
        elif ctype == "highlights":
            detail_html = _render_highlights(content)
        elif ctype == "quotes":
            detail_html = _render_quotes_in_capsule(content)
        else:
            detail_html = _render_points(content)

        details += f"""  <div class="capsule-detail" id="detail-{cid}">
    <button class="close-btn" type="button">&times;</button>
    <div class="detail-title">{dtitle}</div>
{detail_html}  </div>
"""

    return f"""<section class="bookshelf-section">
  <div class="section-head">
    <div class="icon">&#128218;</div>
    <h2>深度解析：点击查看详情</h2>
  </div>
  <div class="capsule-grid">
{cards}  </div>
{details}</section>
"""


def _render_points(content: list) -> str:
    """渲染观点列表 (type: points)。"""
    if not content:
        return ""
    items = ""
    for i, p in enumerate(content, 1):
        num = f"0{i}" if i < 10 else str(i)
        title = _e(p.get("title", ""))
        body = _e(p.get("body", ""))
        items += f"""    <div class="point-item">
      <div class="point-num">{num}</div>
      <div class="point-content">
        <h4>{title}</h4>
        <p>{body}</p>
      </div>
    </div>
"""
    return f'  <div class="points-list">\n{items}  </div>\n'


def _render_structure(content: list) -> str:
    """渲染结构拆解 (type: structure)。"""
    if not content:
        return ""
    items = ""
    for s in content:
        label = _e(s.get("label", ""))
        body = _e(s.get("body", ""))
        items += f"""    <div class="struct-item">
      <div class="struct-label">{label}</div>
      <div class="struct-content">{body}</div>
    </div>
"""
    return f'  <div class="struct-list">\n{items}  </div>\n'


def _render_judgment(content: list) -> str:
    """渲染判断面板 (type: judgment)。"""
    if not content:
        return ""
    items = ""
    for j in content:
        label = _e(j.get("label", ""))
        title = _e(j.get("title", ""))
        body = _e(j.get("body", ""))
        items += f"""    <div class="judge-mini">
      <div class="jm-label">{label}</div>
      <div class="jm-title">{title}</div>
      <div class="jm-desc">{body}</div>
    </div>
"""
    return f'  <div class="judge-grid">\n{items}  </div>\n'


def _render_highlights(content: list) -> str:
    """渲染亮点列表 (type: highlights)。"""
    if not content:
        return ""
    use_ranked = any("name" in c for c in content)
    if not use_ranked:
        return _render_points(content)

    items = ""
    for i, c in enumerate(content, 1):
        rank = c.get("rank", i)
        rank_cls = "hl-rank top3" if isinstance(rank, int) and rank <= 3 else "hl-rank"
        rank_str = f"0{rank}" if isinstance(rank, int) and rank < 10 else str(rank)
        name = _e(c.get("name", ""))
        desc = _e(c.get("desc", ""))
        tag = _e(c.get("tag", ""))
        tag_html = f'<div class="hl-tag">{tag}</div>' if tag else '<div></div>'
        items += f"""    <div class="highlight-item">
      <div class="{rank_cls}">{rank_str}</div>
      <div>
        <div class="hl-name">{name}</div>
        <div class="hl-desc">{desc}</div>
      </div>
      {tag_html}
    </div>
"""
    return f'  <div class="highlight-list">\n{items}  </div>\n'


def generate_html(analysis_json_path: str) -> tuple:
    """从分析 JSON 生成胶囊卡片式 HTML 报告。返回 (html, analysis_dict)。"""
    analysis_path = Path(analysis_json_path).resolve()
    with open(analysis_path, "r", encoding="utf-8") as f:
        analysis = json.load(f)

    title = analysis.get("meta", {}).get("title", "笔记解析")
    analysis_dir = analysis_path.parent

    parts = [
        HTML_PAGE_TOP.format(title=_e(title), css=HTML_CSS),
        _render_hero(analysis),
        _render_image_gallery(analysis, analysis_dir),
        _render_summary(analysis),
        _render_visual_strategy(analysis),
        _render_capsule_section(analysis),
        HTML_PAGE_BOTTOM,
    ]
    return "".join(parts), analysis


# ═══════════════════════════════════════════════════════════
# 6. 主入口
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="小红书笔记解析 + HTML 报告生成")
    parser.add_argument("url_or_file", nargs="?", default=None,
                        help="小红书笔记链接（采集模式），或 --generate-html 时的分析 JSON 路径")
    parser.add_argument("--generate-html", metavar="ANALYSIS_JSON", default=None,
                        help="从分析 JSON 生成 HTML 报告")
    parser.add_argument("--out-dir", default=None, help="输出目录 (默认 output/)")
    parser.add_argument("--no-images", action="store_true", help="跳过图片下载")
    args = parser.parse_args()

    out_dir = Path(args.out_dir) if args.out_dir else Path.cwd() / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── 模式 A：生成 HTML ──
    if args.generate_html:
        html_content, analysis = generate_html(args.generate_html)
        title = analysis.get("meta", {}).get("title", "untitled")
        date_pfx = dt.datetime.now().strftime("%m%d")
        sfx = _safe_filename(title)
        html_path = out_dir / f"{date_pfx}-小红书-{sfx}-报告.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(json.dumps({"status": "generated", "html_path": str(html_path)}, ensure_ascii=False))
        return

    # ── 模式 B：采集（默认） ──
    if not args.url_or_file:
        sys.exit("用法: python parse.py <小红书笔记链接>\n       python parse.py --generate-html analysis.json")

    url = args.url_or_file
    print("[1/3] 解析链接...", file=sys.stderr)

    # Step 1: 解析 URL
    note_id, xsec_token, full_url = parse_url(url)
    if not note_id:
        result = {
            "status": "error",
            "error": "无法从链接中提取笔记 ID。请确保链接格式正确，或使用「分享→复制链接」获取完整链接。",
            "input_url": url,
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    print(f"  [XHS] note_id: {note_id}", file=sys.stderr)
    print(f"  [XHS] xsec_token: {'有' if xsec_token else '无'}", file=sys.stderr)

    # Step 2: 抓取页面
    print("[2/3] 抓取笔记内容...", file=sys.stderr)
    try:
        page_html = fetch_note_page(note_id, xsec_token)
    except urllib.error.HTTPError as e:
        result = {
            "status": "error",
            "error": f"HTTP {e.code}: {'需要登录或链接已失效' if e.code == 461 else '页面访问失败'}",
            "note_id": note_id,
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        result = {
            "status": "error",
            "error": f"网络请求失败: {e}",
            "note_id": note_id,
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    # 解析 __INITIAL_STATE__
    state = extract_initial_state(page_html)
    note_data = None
    needs_token = False
    data_source = "full"  # full = __INITIAL_STATE__, fallback = meta tags

    if state:
        note_data = parse_note_data(state, note_id)
        if not note_data:
            # __INITIAL_STATE__ 存在但 noteDetailMap 为空 → 缺 xsec_token
            note_map = state.get("note", {}).get("noteDetailMap", {})
            if not note_map:
                needs_token = True
                print("  [XHS] noteDetailMap 为空，可能缺少 xsec_token", file=sys.stderr)
                # 尝试 meta 标签降级
                fallback = extract_meta_fallback(page_html)
                if fallback:
                    note_data = _build_fallback_note(fallback, note_id)
                    data_source = "fallback"

    if not note_data and not needs_token:
        # __INITIAL_STATE__ 完全不存在
        print("  [XHS] __INITIAL_STATE__ 未找到，尝试 meta 标签...", file=sys.stderr)
        fallback = extract_meta_fallback(page_html)
        if fallback:
            note_data = _build_fallback_note(fallback, note_id)
            data_source = "fallback"

    if not note_data:
        token_hint = ""
        if needs_token or not xsec_token:
            token_hint = " 链接中缺少 xsec_token 参数——请在小红书 APP 中打开笔记，点「分享→复制链接」，粘贴完整链接（含 xsec_token）。"
        result = {
            "status": "error",
            "error": f"无法解析笔记内容。{token_hint} 如果已有 xsec_token 仍失败，笔记可能需要登录或已被删除。".strip(),
            "note_id": note_id,
            "has_xsec_token": bool(xsec_token),
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    # Step 3: 下载图片
    date_pfx = dt.datetime.now().strftime("%m%d")
    sfx = _safe_filename(note_data.get("title", "") or note_id)
    prefix = f"{date_pfx}-小红书-{sfx}"

    if not args.no_images and note_data.get("images"):
        print("[3/3] 下载图片...", file=sys.stderr)
        note_data = download_images(note_data, out_dir, prefix)
    else:
        print("[3/3] 跳过图片下载", file=sys.stderr)

    # 写入笔记数据 JSON
    json_path = out_dir / f"{prefix}-笔记数据.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(note_data, f, ensure_ascii=False, indent=2)

    print(f"\n  完成! 数据已保存: {json_path}", file=sys.stderr)

    # 输出 JSON（stdout）— AI 读取这个做分析
    result = {
        "status": "parsed",
        "note_id": note_data.get("note_id", ""),
        "platform": "小红书",
        "title": note_data.get("title", ""),
        "desc": note_data.get("desc", ""),
        "note_type": note_data.get("note_type", ""),
        "publish_date": note_data.get("publish_date", ""),
        "author": note_data.get("author", {}),
        "interactions": note_data.get("interactions", {}),
        "tags": note_data.get("tags", []),
        "images": [
            {"url": img.get("url", ""), "local_path": img.get("local_path", ""),
             "width": img.get("width", 0), "height": img.get("height", 0)}
            for img in note_data.get("images", [])
        ],
        "video_url": note_data.get("video_url"),
        "data_source": data_source,
        "data_path": str(json_path),
        "output_dir": str(out_dir),
    }
    if data_source == "fallback":
        result["warning"] = "数据来自 meta 标签降级提取，可能不完整。请使用含 xsec_token 的分享链接获取完整笔记数据。"
        print("  [XHS] 警告: 使用降级数据，内容可能不完整", file=sys.stderr)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
