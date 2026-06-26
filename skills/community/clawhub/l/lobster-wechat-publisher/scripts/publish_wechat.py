#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat Article Publisher v2 - Enhanced
从 Markdown 或 HTML 发布图文到微信公众号，支持本地图片自动上传。

改进点（相比 v1）：
1. HTML 输入支持 + <body> 提取
2. 本地图片自动上传至微信 CDN 并替换 src
3. 封面图自动 resize 为 900×383（2.35:1）
4. 上传失败自动重试 3 次，超时从 30s 升级到 120s
5. Token 缓存至 .token_cache.json
6. 草稿创建必须使用永久素材 media_id 作 thumb
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urljoin

try:
    import markdown
    import requests
    from PIL import Image
    from bs4 import BeautifulSoup
    import yaml
except ImportError:
    markdown = None
    requests = None
    Image = None
    BeautifulSoup = None
    yaml = None


# ── API 常量 ────────────────────────────────────────────────────────────────
TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
DRAFT_ADD_URL = "https://api.weixin.qq.com/cgi-bin/draft/add"
PUBLISH_SUBMIT_URL = "https://api.weixin.qq.com/cgi-bin/freepublish/submit"
PUBLISH_GET_URL = "https://api.weixin.qq.com/cgi-bin/freepublish/get"
MATERIAL_ADD_URL = "https://api.weixin.qq.com/cgi-bin/material/add_material"
MEDIA_UPLOAD_URL = "https://api.weixin.qq.com/cgi-bin/media/upload"

# 封面图目标尺寸（2.35:1 比例）
COVER_TARGET = (900, 383)


# ── 异常 ─────────────────────────────────────────────────────────────────────
class WeChatPublishError(RuntimeError):
    def __init__(self, msg: str, errcode: Optional[int] = None):
        self.errcode = errcode
        super().__init__(msg)


# ── 数据模型 ───────────────────────────────────────────────────────────────
@dataclass
class Article:
    title: str
    author: str
    content: str  # HTML
    source_url: str
    digest: str
    first_image_url: str


# ── 工具函数 ────────────────────────────────────────────────────────────────
def load_config(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data.get("wechat"), dict):
        return data
    if isinstance(data.get("platforms", {}).get("wechat"), dict):
        return {"wechat": data["platforms"]["wechat"]}
    raise RuntimeError("config.json 缺少 wechat 配置")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    text = text.lstrip("\ufeff")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                return yaml.safe_load(parts[1]) or {}, parts[2].strip()
            except Exception:
                pass
    return {}, text


def extract_title_from_md(text: str) -> str:
    text = text.lstrip("\ufeff")
    match = re.search(r"^#\s+(.+)$", text, re.M)
    if match:
        return match.group(1).strip()
    for line in text.splitlines():
        s = re.sub(r"^#+\s*", "", line.strip())
        if s:
            return s[:64]
    return "未命名文章"


def slugify(text: str) -> str:
    t = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", text.strip().lower())
    t = re.sub(r"-{2,}", "-", t).strip("-")
    return t or "wechat-article"


# ── 核心逻辑 ────────────────────────────────────────────────────────────────
def is_url(text: str) -> bool:
    return bool(re.match(r"^https?://", (text or "").strip(), re.I))


def is_probably_html(text: str) -> bool:
    sample = (text or "").strip()[:500].lower()
    return bool(re.search(
        r"<(article|section|div|p|h[1-6]|ul|ol|pre|table|img|blockquote)\b",
        sample
    ))


def markdown_to_html(text: str) -> str:
    if not text:
        return ""
    if is_probably_html(text):
        return text
    return markdown.markdown(
        text,
        extensions=["extra", "tables", "nl2br", "codehilite"],
        output_format="html",
    )


def extract_body(html: str) -> str:
    m = re.search(r"<body[^>]*>(.*)</body>", html, re.DOTALL)
    return m.group(1).strip() if m else html


def html_to_plain_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    txt = soup.get_text("\n", strip=True)
    return re.sub(r"\n+", "\n", txt)


def optimize_for_wechat(content_html: str, template: str = "standard") -> str:
    soup = BeautifulSoup(content_html, "html.parser")

    for tag in soup.find_all(["script", "style"]):
        tag.decompose()

    for h2 in soup.find_all("h2"):
        h2["style"] = (
            "margin:1.6em 0 0.75em;padding:0.35em 0.65em;font-size:1.2em;line-height:1.5;"
            "color:#1a1a1a;font-weight:700;background:#f0f4ff;"
            "border-left:4px solid #3b6dd8;border-radius:2px;"
        )

    for h3 in soup.find_all("h3"):
        h3["style"] = (
            "margin:1.3em 0 0.55em;padding:0.3em 0.6em;font-size:1.05em;line-height:1.5;"
            "color:#2d3748;font-weight:700;background:#f8fafc;"
            "border-left:3px solid #6b8cf6;border-radius:2px;"
        )

    for h4 in soup.find_all("h4"):
        h4["style"] = (
            "margin:1.1em 0 0.45em;padding:0.25em 0.5em;font-size:0.98em;line-height:1.5;"
            "color:#374151;font-weight:700;"
        )

    # 首段引言样式
    body_node = soup.find("body")
    first_p = None
    if body_node:
        for t in body_node.children:
            if hasattr(t, 'name') and t.name == 'p':
                first_p = t
                break
    if not first_p:
        first_p = soup.find("p")

    lead_style = (
        "margin:0.5em 0 1.2em;padding:1em 1.1em;line-height:2;"
        "font-size:16px;color:#2b2f38;background:#f8f9fc;"
        "border-radius:10px;border:1px solid #e8ecf4;"
    )

    for p in soup.find_all("p"):
        if p.find_parent(["li", "blockquote", "td", "th", "pre"]):
            continue
        if p is first_p:
            p["style"] = lead_style
        else:
            p["style"] = (
                "margin:0.85em 0;line-height:1.95;font-size:16px;color:#2b2f38;"
                "text-align:justify;letter-spacing:0.01em;"
            )

    for a in soup.find_all("a"):
        a["style"] = "color:#1f57c3;text-decoration:underline;word-break:break-all;"
        a["target"] = "_blank"

    for strong in soup.find_all("strong"):
        strong["style"] = "font-weight:700;color:#1f2937;"

    for blockquote in soup.find_all("blockquote"):
        blockquote["style"] = (
            "margin:1.1em 0;padding:0.8em 1em;border-left:3px solid #7aa2ff;"
            "background:#f4f7ff;color:#43506a;line-height:1.8;border-radius:4px;"
        )

    for ul in soup.find_all("ul"):
        ul["style"] = (
            "margin:0.95em 0;padding:0.75em 0.95em 0.75em 1.55em;line-height:1.8;"
            "color:#2f3441;background:#f8fafc;border-radius:6px;"
            "border:1px solid #edf2f7;list-style-position:outside;list-style-type:disc;"
        )

    for ol in soup.find_all("ol"):
        ol["style"] = (
            "margin:0.95em 0;padding:0.75em 0.95em 0.75em 1.55em;line-height:1.8;"
            "color:#2f3441;background:#f8fafc;border-radius:6px;"
            "border:1px solid #edf2f7;list-style-position:outside;list-style-type:decimal;"
        )

    for li in soup.find_all("li"):
        li["style"] = "margin:0.28em 0;font-size:16px;line-height:1.82;"

    for img in soup.find_all("img"):
        img["style"] = "max-width:100%;border-radius:8px;margin:1em 0;"

    body_html = "".join(str(n) for n in soup.contents)
    wrapper = (
        "<section style='margin:0 auto;max-width:640px;padding:0 16px;"
        "font-family:-apple-system,BlinkMacSystemFont,\"PingFang SC\",\"Microsoft YaHei\",sans-serif;"
        "color:#333;font-size:16px;line-height:1.9;'>"
        f"{body_html}"
        "</section>"
    )
    return wrapper


# ── 封面图处理 ─────────────────────────────────────────────────────────────
def resize_cover(src_path: Path, dst_path: Path, target: tuple[int, int] = COVER_TARGET) -> Path:
    """将封面图 resize 为指定比例，保存为 PNG。"""
    img = Image.open(src_path)
    w, h = target
    # 计算裁切区域（居中）
    orig_w, orig_h = img.size
    target_ratio = w / h
    orig_ratio = orig_w / orig_h
    if abs(orig_ratio - target_ratio) < 0.01:
        resized = img.resize((w, h), Image.LANCZOS)
    elif orig_ratio > target_ratio:
        # 原图更宽，裁左右
        new_w = int(orig_h * target_ratio)
        left = (orig_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, orig_h))
        resized = img.resize((w, h), Image.LANCZOS)
    else:
        # 原图更高，裁上下
        new_h = int(orig_w / target_ratio)
        top = (orig_h - new_h) // 2
        img = img.crop((0, top, orig_w, top + new_h))
        resized = img.resize((w, h), Image.LANCZOS)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    resized.save(dst_path, "PNG")
    return dst_path


# ── 微信 API ────────────────────────────────────────────────────────────────
class WeChatClient:
    def __init__(self, app_id: str, app_secret: str, timeout: int = 30):
        self.app_id = app_id
        self.app_secret = app_secret
        self.timeout = timeout

    def get_token(self, force_refresh: bool = False) -> str:
        cache_path = Path(__file__).resolve().parent.parent / ".token_cache.json"
        cache = {}
        if not force_refresh and cache_path.exists():
            try:
                cache = json.loads(cache_path.read_text(encoding="utf-8"))
            except Exception:
                pass
            if cache.get("expires_at", 0) > time.time() + 60:
                return cache["access_token"]

        r = requests.get(TOKEN_URL, params={
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret,
        }, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        if data.get("errcode"):
            raise WeChatPublishError(f"Token 获取失败: {data}", data.get("errcode"))

        token = data["access_token"]
        try:
            json.dump({
                "access_token": token,
                "expires_at": time.time() + 7100
            }, cache_path.open("w", encoding="utf-8"))
        except Exception:
            pass
        return token

    def _post_json(self, url: str, params: dict, payload: dict) -> dict:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        r = requests.post(url, params=params, data=body,
                          headers={"Content-Type": "application/json; charset=utf-8"},
                          timeout=self.timeout)
        r.raise_for_status()
        return json.loads(r.content.decode("utf-8"))

    def upload_image_retry(self, token: str, image_path: Path,
                           retries: int = 3, timeout: int = 120) -> str:
        """上传图片到临时素材，返回 CDN URL。失败重试 retries 次。"""
        url = f"{MEDIA_UPLOAD_URL}?access_token=***&type=image"
        last_err = None
        for attempt in range(retries):
            try:
                with image_path.open("rb") as f:
                    r = requests.post(url, files={"media": f}, timeout=timeout)
                d = r.json()
                if d.get("errcode"):
                    last_err = d
                    raise WeChatPublishError(
                        f"图片上传失败 ({image_path.name}): {d}", d.get("errcode")
                    )
                return d["url"]
            except (requests.exceptions.RequestException, WeChatPublishError) as e:
                last_err = e
                if attempt < retries - 1:
                    print(f"  上传图片失败，重试 {attempt + 2}/{retries}...")
                    time.sleep(2)
        raise WeChatPublishError(
            f"图片上传失败（已重试 {retries} 次）: {last_err}"
        )

    def upload_permanent_retry(self, token: str, image_path: Path,
                               retries: int = 3, timeout: int = 120) -> tuple[str, str]:
        """上传为永久素材，返回 (media_id, url)。失败重试 retries 次。"""
        url = f"{MATERIAL_ADD_URL}?access_token=***&type=image"
        last_err = None
        for attempt in range(retries):
            try:
                with image_path.open("rb") as f:
                    r = requests.post(url, files={"media": f}, timeout=timeout)
                d = r.json()
                if d.get("errcode"):
                    last_err = d
                    raise WeChatPublishError(
                        f"永久素材上传失败 ({image_path.name}): {d}", d.get("errcode")
                    )
                return d["media_id"], d.get("url", "")
            except (requests.exceptions.RequestException, WeChatPublishError) as e:
                last_err = e
                if attempt < retries - 1:
                    print(f"  永久素材上传失败，重试 {attempt + 2}/{retries}...")
                    time.sleep(2)
        raise WeChatPublishError(
            f"永久素材上传失败（已重试 {retries} 次）: {last_err}"
        )

    def add_draft(self, token: str, title: str, author: str,
                  digest: str, content_html: str, source_url: str,
                  thumb_media_id: str) -> str:
        payload = {
            "articles": [{
                "title": title[:64],
                "author": author[:16],
                "digest": digest[:120],
                "content": content_html,
                "content_source_url": source_url[:200],
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 1,
                "only_fans_can_comment": 0,
            }]
        }
        data = self._post_json(DRAFT_ADD_URL, {"access_token": token}, payload)
        if data.get("errcode"):
            raise WeChatPublishError(f"草稿创建失败: {data}", data.get("errcode"))
        media_id = data.get("media_id")
        if not media_id:
            raise WeChatPublishError("草稿创建成功但未返回 media_id")
        return media_id

    def submit_publish(self, token: str, media_id: str) -> str:
        data = self._post_json(
            PUBLISH_SUBMIT_URL, {"access_token": token},
            {"media_id": media_id}
        )
        if data.get("errcode"):
            raise WeChatPublishError(f"发布失败: {data}", data.get("errcode"))
        return data.get("publish_id", "")


# ── 文章解析 ────────────────────────────────────────────────────────────────
def extract_article(input_path: Path, source_url_override: str = "") -> Article:
    raw = input_path.read_text(encoding="utf-8").lstrip("\ufeff")

    if is_probably_html(raw):
        body_content = extract_body(raw)
        html_content = body_content
        # 从 <title> 或 <h1> 提取标题，忽略章节小标题
        soup = BeautifulSoup(raw, "html.parser")
        title_node = soup.find("title") or soup.find("h1")
        if not title_node:
            # 找第一个在 body 直接子元素层级的 h2（不是章节小标题）
            body = soup.find("body")
            if body:
                for tag in body.find_all(re.compile(r"^h[1-6]$"), recursive=False):
                    title_node = tag
                    break
        if not title_node:
            h2s = soup.find_all("h2")
            if h2s:
                title_node = h2s[0]
        title = title_node.get_text(strip=True)[:64] if title_node else "未命名文章"
        title = re.sub(r"^[一二三四五六七八九十、\s]+", "", title).strip()
        author = ""
        digest = html_to_plain_text(html_content)[:120]
        first_img = soup.find("img")
        first_image_url = first_img.get("src", "") if first_img else ""
        source_url = source_url_override
    else:
        frontmatter, body = parse_frontmatter(raw)
        title = (frontmatter.get("title") or extract_title_from_md(body))[:64]
        author = frontmatter.get("author", "")
        html_content = markdown_to_html(body)
        digest = html_to_plain_text(html_content)[:120]
        first_image_url = ""
        match = re.search(r"!\[[^\]]*\]\(([^)]+)\)", body)
        if match:
            first_image_url = match.group(1).strip()
        source_url = source_url_override or frontmatter.get("source_url", "")

    return Article(
        title=title or "未命名文章",
        author=author,
        content=html_content,
        source_url=source_url,
        digest=digest,
        first_image_url=first_image_url,
    )


# ── 本地图片替换（预览模式，不上传） ──────────────────────────────────────
def rewrite_local_images_preview(html_content: str, base_dir: Path) -> str:
    """
    仅验证本地图片路径，不上传到微信 CDN。
    将相对路径解析为完整路径，检查文件是否存在。
    """
    soup = BeautifulSoup(html_content, "html.parser")
    img_tags = soup.find_all("img")
    found = 0
    for img in img_tags:
        src = (img.get("src") or "").strip()
        if not src or src.startswith(("http://", "https://")):
            continue
        if src.startswith("/"):
            local_path = base_dir / src.lstrip("/")
        else:
            local_path = base_dir / src
        if local_path.exists():
            print(f"  [OK] 图片存在: {src}")
            found += 1
        else:
            print(f"  [WARN] 图片不存在: {local_path}")
    print(f"  共检测 {found} 张本地图片（预览模式，不上传）")
    return str(soup)


# ── 本地图片替换 ────────────────────────────────────────────────────────────
def rewrite_local_images(html_content: str, base_dir: Path,
                        client: WeChatClient, token: str) -> str:
    """
    扫描 HTML 中的 <img src="...">，
    - 若为 http:///https:// 开头，跳过
    - 若为相对路径，拼接 base_dir 上传至微信 CDN，替换 src 为返回的 URL
    - 若本地文件不存在，跳过并打印警告
    """
    soup = BeautifulSoup(html_content, "html.parser")
    img_tags = soup.find_all("img")
    replaced = 0

    for img in img_tags:
        src = (img.get("src") or "").strip()
        if not src:
            continue
        if src.startswith(("http://", "https://")):
            continue

        # 相对路径 → 拼接 base_dir
        # src 可能是 "龙虾4号_images/lobster_history.png" 形式，
        # 需要保留完整相对路径拼接，不能只用 os.path.basename()
        if src.startswith("/"):
            local_path = base_dir / src.lstrip("/")
        else:
            local_path = base_dir / src

        if not local_path.exists():
            print(f"  [WARN] 本地图片不存在，跳过: {local_path}")
            continue

        try:
            cdn_url = client.upload_image_retry(token, local_path)
            img["src"] = cdn_url
            print(f"  替换图片: {local_path.name} -> {cdn_url[:50]}...")
            replaced += 1
        except WeChatPublishError as e:
            print(f"  [WARN] 图片上传失败，跳过: {local_path.name} ({e})")

    return str(soup)


# ── 封面图处理 ─────────────────────────────────────────────────────────────
def prepare_cover(cover_path: Optional[Path], default_cover_dir: Path,
                  article: Article, client: WeChatClient, token: str) -> str:
    """
    处理封面图：
    1. 若指定了 cover_path，使用它
    2. 若 article.first_image_url 是本地文件，使用它
    3. 否则使用 default_cover_dir/cover.png
    4. resize 为 900×383 并上传为永久素材，返回 media_id
    """
    src_path: Optional[Path] = None

    if cover_path and cover_path.exists():
        src_path = cover_path
    elif article.first_image_url and not article.first_image_url.startswith(("http://", "https://")):
        candidate = default_cover_dir / article.first_image_url
        if candidate.exists():
            src_path = candidate

    if src_path is None:
        default = default_cover_dir / "cover.png"
        if default.exists():
            src_path = default

    if src_path is None:
        raise WeChatPublishError(
            "未找到封面图，请通过 --cover-image 指定，或确保正文第一张图片存在"
        )

    # 检查尺寸，判断是否需要 resize
    try:
        img = Image.open(src_path)
        w, h = img.size
        target_ratio = COVER_TARGET[0] / COVER_TARGET[1]
        orig_ratio = w / h
        needs_resize = abs(orig_ratio - target_ratio) > 0.01 or w < 900
    except Exception:
        needs_resize = True

    if needs_resize:
        processed = src_path.parent / (src_path.stem + "_2_35_1.png")
        resize_cover(src_path, processed, COVER_TARGET)
        print(f"  封面图已 resize 为 900×383: {processed.name}")
        src_path = processed

    _, url = client.upload_permanent_retry(token, src_path)
    # 返回 media_id 需要用永久素材接口重新获取
    media_id_path = src_path.parent / (src_path.stem + "_media_id.txt")
    # 实际上传以获取 media_id
    media_id, _ = client.upload_permanent_retry(token, src_path)
    return media_id


# ── 主流程 ──────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="发布文章到微信公众号 v2")
    parser.add_argument("input", nargs="?", help="Markdown 或 HTML 文件路径")
    parser.add_argument("--config", default="", help="配置文件路径")
    parser.add_argument("--cover-image", default="", help="封面图本地路径")
    parser.add_argument("--template", choices=["standard", "viral"], default="standard")
    parser.add_argument("--author", default="", help="覆盖作者名")
    parser.add_argument("--title", default="", help="文章标题（HTML 文件时必填，Markdown 会自动从 frontmatter 提取）")
    parser.add_argument("--source-url", default="", help="原文链接")
    parser.add_argument("--image-dir", default="", help="图片目录（默认使用输入文件所在目录）")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()

    if args.install:
        import subprocess
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "-r", str(Path(__file__).resolve().parent / "requirements.txt")
        ])
        print(json.dumps({"success": True, "installed": True}))
        return

    if not args.input:
        raise RuntimeError("缺少输入参数：请传入 Markdown 或 HTML 文件路径")

    skill_dir = Path(__file__).resolve().parent.parent
    config_path = Path(args.config) if args.config else skill_dir / "config.json"
    cfg = load_config(config_path)
    wc = cfg["wechat"]
    app_id = (wc.get("app_id") or "").strip()
    app_secret = (wc.get("app_secret") or "").strip()
    default_author = (args.author or wc.get("author") or "").strip()

    if not app_id or not app_secret:
        raise RuntimeError("config.json 缺少 app_id 或 app_secret")

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        raise RuntimeError(f"文件不存在: {input_path}")

    print(f"读取文章: {input_path}")
    article = extract_article(input_path, source_url_override=args.source_url.strip())
    # HTML 文件无法自动提取准确标题，允许通过 --title 覆盖
    if args.title:
        article.title = args.title.strip()[:64]
    if not article.title or article.title == "未命名文章":
        if args.title:
            article.title = args.title.strip()[:64]
    print(f"标题: {article.title}")

    if args.image_dir:
        base_dir = Path(args.image_dir).resolve()
    else:
        base_dir = input_path.parent

    if args.dry_run:
        # dry-run 时仍替换图片路径（仅做本地路径解析，不上传）
        article.content = rewrite_local_images_preview(article.content, base_dir)
        content_html = optimize_for_wechat(article.content, args.template)
        preview = base_dir / f"{slugify(article.title)}-preview.html"
        preview.write_text(content_html, encoding="utf-8")
        print(f"预览文件: {preview}")
        print(json.dumps({
            "success": True, "mode": "dry-run",
            "title": article.title,
            "preview_html": str(preview),
        }))
        return

    client = WeChatClient(app_id=app_id, app_secret=app_secret, timeout=args.timeout)
    print("获取 Token...")
    token = client.get_token()

    # 上传本地图片
    print("处理正文图片...")
    article.content = rewrite_local_images(
        article.content, base_dir, client, token
    )

    # 处理封面
    print("处理封面图...")
    cover_path = Path(args.cover_image) if args.cover_image else None
    if cover_path and not cover_path.exists():
        print(f"  [WARN] 指定封面不存在: {cover_path}，忽略")
        cover_path = None

    thumb_media_id = prepare_cover(
        cover_path, base_dir, article, client, token
    )
    print(f"封面 media_id: {thumb_media_id}")

    # 优化 HTML
    content_html = optimize_for_wechat(article.content, args.template)

    # 创建草稿
    print("创建草稿...")
    draft_id = client.add_draft(
        token=token,
        title=article.title,
        author=default_author or article.author or "龙虾5号",
        digest=article.digest,
        content_html=content_html,
        source_url=article.source_url,
        thumb_media_id=thumb_media_id,
    )
    print(f"草稿 ID: {draft_id}")

    result = {
        "success": True,
        "title": article.title,
        "draft_media_id": draft_id,
    }

    if args.publish:
        publish_id = client.submit_publish(token, draft_id)
        result["publish_id"] = publish_id
        if args.status:
            result["status"] = client.get_publish_status(token, publish_id)

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({
            "success": False,
            "error": str(exc),
            "type": type(exc).__name__,
        }, ensure_ascii=False))
        sys.exit(1)