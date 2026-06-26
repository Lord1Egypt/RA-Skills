#!/usr/bin/env python3
"""
卡片创建脚本
子命令:
  create   -- 创建卡片任务并同步等待结果（返回本地图片路径，agent 可继续后续操作）
  transfer -- 本地文件中转到 R2
  history  -- 读取操作日志历史

所有命令输出 JSON 格式，供 Agent 解析。
"""
from __future__ import annotations

import argparse
import json
import os
import ssl
import struct
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plume_api
import action_log
import config

# ─── 熔断机制（基于 action_log，无独立文件，agent 无法绕过）────
FAIL_STATUSES = {"failed", "timeout", "cancelled"}


def _get_circuit_breaker_config() -> tuple[int, int]:
    """从 EXTEND.md 读取熔断配置，默认 600 秒/2 次"""
    cfg = config.load_extend_config()
    breaker = cfg.get("circuit_breaker", {})
    if not isinstance(breaker, dict):
        return 600, 2
    window = breaker.get("window_seconds", 600)
    threshold = breaker.get("threshold", 2)
    return window, threshold


def _check_circuit_breaker(channel: str | None) -> str | None:
    """从 action_log 统计最近失败次数，达到阈值则熔断"""
    window, threshold = _get_circuit_breaker_config()
    entries = action_log.read_log(channel or "")
    cutoff = time.time() - window
    recent_fails = [
        e for e in entries
        if e.get("status") in FAIL_STATUSES
        and e.get("completed_at", e.get("created_at", 0)) > cutoff
    ]
    if len(recent_fails) >= threshold:
        task_ids = [e.get("task_id", "?") for e in recent_fails]
        return (
            f"熔断保护：最近 {window // 60} 分钟内已有 {len(recent_fails)} 次任务失败"
            f"（task_ids: {', '.join(task_ids)}），"
            f"请等待 {window // 60} 分钟后再试，或联系管理员排查后端问题。"
        )
    return None


def log(msg: str):
    """输出脱敏调试日志到 stderr（不影响 stdout 的 JSON 输出）"""
    safe_msg = config.strip_credentials(msg)
    print(f"[plume-notecard] {safe_msg}", file=sys.stderr, flush=True)


def output(data: dict):
    """输出脱敏 JSON 结果到 stdout"""
    safe_json = config.strip_credentials(json.dumps(data, ensure_ascii=False))
    print(safe_json)


# ─── transfer 子命令 ───────────────────────────────────────

def _get_image_dimensions(file_path: str) -> tuple[int, int] | None:
    """读取本地图片的宽高（支持 JPEG/PNG/GIF/BMP/WebP），纯标准库实现"""
    try:
        with open(file_path, "rb") as f:
            header = f.read(32)
            if len(header) < 8:
                return None

            if header[:8] == b"\x89PNG\r\n\x1a\n":
                w, h = struct.unpack(">II", header[16:24])
                return (w, h)

            if header[:6] in (b"GIF87a", b"GIF89a"):
                w, h = struct.unpack("<HH", header[6:10])
                return (w, h)

            if header[:2] == b"BM":
                w, h = struct.unpack("<ii", header[18:26])
                return (abs(w), abs(h))

            if header[:4] == b"RIFF" and header[8:12] == b"WEBP":
                f.seek(0)
                data = f.read(64)
                if b"VP8 " in data:
                    idx = data.index(b"VP8 ") + 10
                    w = struct.unpack("<H", data[idx:idx + 2])[0] & 0x3FFF
                    h = struct.unpack("<H", data[idx + 2:idx + 4])[0] & 0x3FFF
                    return (w, h)
                if b"VP8L" in data:
                    idx = data.index(b"VP8L") + 9
                    bits = struct.unpack("<I", data[idx:idx + 4])[0]
                    w = (bits & 0x3FFF) + 1
                    h = ((bits >> 14) & 0x3FFF) + 1
                    return (w, h)

            if header[:2] == b"\xff\xd8":
                f.seek(2)
                while True:
                    marker = f.read(2)
                    if len(marker) < 2:
                        return None
                    if marker[0] != 0xFF:
                        return None
                    m = marker[1]
                    if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                             0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                        f.read(3)
                        h, w = struct.unpack(">HH", f.read(4))
                        return (w, h)
                    length_data = f.read(2)
                    if len(length_data) < 2:
                        return None
                    length = struct.unpack(">H", length_data)[0]
                    f.seek(length - 2, 1)

    except Exception:
        return None
    return None


def cmd_transfer(args):
    """上传本地文件到 R2（参考图上传用）"""
    local_file = args.file

    if not local_file:
        output({"success": False, "error": "必须指定 --file 参数"})
        return

    if local_file.startswith("file://"):
        local_file = local_file[7:]

    if not os.path.exists(local_file):
        output({"success": False, "error": f"文件不存在: {local_file}"})
        return

    dimensions = _get_image_dimensions(local_file)
    local_width = dimensions[0] if dimensions else None
    local_height = dimensions[1] if dimensions else None
    if dimensions:
        log(f"transfer: 本地读取尺寸 {local_width}x{local_height}")

    log(f"transfer: 本地文件上传 R2, file={os.path.basename(local_file)}")
    upload_result = plume_api.upload_image(local_file)

    if not upload_result.get("success"):
        output({"success": False, "step": "upload_to_r2",
                "error": upload_result.get("message", "R2 上传失败")})
        return

    data = upload_result.get("data", {})
    output({
        "success": True,
        "image_url": data.get("file_url"),
        "file_key": data.get("file_key"),
        "file_size": data.get("file_size"),
        "width": data.get("width") or local_width,
        "height": data.get("height") or local_height,
    })


# ─── create 子命令 ──────────────────────────────────────────

def _is_local_path(url: str) -> bool:
    if not url:
        return False
    return url.startswith("file://") or url.startswith("/")


SUPPORTED_RATIOS = [
    ("16:9", 16 / 9),
    ("4:3", 4 / 3),
    ("1:1", 1 / 1),
    ("3:4", 3 / 4),
    ("9:16", 9 / 16),
]


def _infer_aspect_ratio(width: int, height: int) -> str:
    """根据参考图宽高推算最接近的支持比例"""
    if width <= 0 or height <= 0:
        return "3:4"
    actual = width / height
    best_ratio = "3:4"
    best_diff = float("inf")
    for label, value in SUPPORTED_RATIOS:
        diff = abs(actual - value)
        if diff < best_diff:
            best_diff = diff
            best_ratio = label
    log(f"参考图 {width}x{height} (ratio={actual:.3f}) → 推算比例 {best_ratio}")
    return best_ratio


def _build_params_snapshot(args, mode: str) -> dict:
    """提取创建参数快照，用于重试时还原"""
    params = {}
    for key in ("article", "style_hint", "aspect_ratio", "locale"):
        val = getattr(args, key, None)
        if val is not None:
            params[key] = val
    if mode == "reference":
        for key in ("reference_type", "reference_image_urls",
                     "reference_topic", "reference_article"):
            val = getattr(args, key, None)
            if val is not None:
                params[key] = val
    if (args.count or 1) >= 2:
        params["count"] = args.count
        if args.child_reference_type:
            params["child_reference_type"] = args.child_reference_type
    if getattr(args, 'deck_mode', False):
        params["deck_mode"] = True
        if args.page_count:
            params["page_count"] = args.page_count
        if getattr(args, 'pages', None) is not None:
            params["pages"] = args.pages
    return params


def _validate_params(args) -> str | None:
    """参数校验，返回错误信息或 None"""
    if args.action:
        if not args.last_task_id:
            return "重试动作需要提供 --last-task-id"
        if args.mode == "reference":
            if not args.reference_type:
                return "参考图重试需要提供 --reference-type"
            if not args.reference_image_urls:
                return "参考图重试需要提供 --reference-image-urls"
            if args.action == "switch_content":
                if args.reference_type == "style_transfer" and not args.reference_topic and not args.reference_article:
                    return "仿风格换内容重试需要提供 --reference-topic 或 --reference-article"
                if args.reference_type == "product_embed" and not args.reference_article:
                    return "产品融入换内容重试需要提供 --reference-article"
                if args.reference_type == "content_rewrite" and not args.reference_article and not args.reference_topic:
                    return "内容改写换内容重试需要提供 --reference-article 或 --reference-topic"
        return None

    if getattr(args, 'deck_mode', False):
        if args.mode == "reference":
            return "幻灯片套件模式不支持参考图模式，请使用 article 模式"
        if (args.count or 1) >= 2:
            return "幻灯片套件模式与批量模式（count>=2）互斥"
        if not args.mode:
            return "幻灯片套件模式需要指定 --mode (topic/article)"
        has_pages = getattr(args, 'pages', None) is not None
        if args.mode == "topic" and not args.topic and not has_pages:
            return "幻灯片套件主题模式需要提供 --topic 或 --pages"
        if args.mode == "article" and not args.article and not has_pages:
            return "幻灯片套件长文模式需要提供 --article 或 --pages"
        return None

    if not args.mode:
        return "必须指定 --mode (topic/article/reference)"

    if args.mode == "topic" and not args.topic:
        return "主题模式需要提供 --topic"
    if args.mode == "article" and not args.article:
        return "长文模式需要提供 --article"
    if args.mode == "reference":
        if not args.reference_type:
            return "参考图模式需要提供 --reference-type (sketch/style_transfer/product_embed/content_rewrite)"
        if not args.reference_image_urls:
            return "参考图模式需要提供 --reference-image-urls"
        if args.reference_type == "style_transfer" and not args.reference_topic and not args.reference_article:
            return "仿风格模式需要提供 --reference-topic 或 --reference-article"
        if args.reference_type == "product_embed" and not args.reference_article:
            return "产品融入模式需要提供 --reference-article"
        if args.reference_type == "content_rewrite" and not args.reference_article and not args.reference_topic:
            return "内容改写模式需要提供 --reference-article 或 --reference-topic"

    count = args.count or 1
    if count >= 2 and args.mode == "reference":
        return "批量卡片暂不支持参考图模式，请使用 topic 或 article 模式"

    return None


def _do_create(args) -> dict:
    """创建卡片任务的核心逻辑，返回结果 dict（不直接 output）"""
    if args.mode == "reference" and args.article and not args.reference_article:
        log("reference 模式参数映射: article → reference_article")
        args.reference_article = args.article

    err = _validate_params(args)
    if err:
        return {"success": False, "error": err}

    ref_urls = None
    if args.reference_image_urls:
        ref_urls = [u.strip() for u in args.reference_image_urls.split(",") if u.strip()]
        for url in ref_urls:
            if _is_local_path(url):
                return {"success": False, "error": f"--reference-image-urls 不接受本地文件路径，请先通过 'transfer --file {url}' 上传后使用返回的远程 URL。"}

    mode = args.mode
    if args.article and len(args.article.strip()) > 50 and mode == "topic":
        log("mode 归一化: topic → article (检测到长文内容)")
        mode = "article"

    count = min(max(round(args.count or 1), 1), 10)
    is_batch = count >= 2
    is_deck = getattr(args, 'deck_mode', False)

    if args.aspect_ratio:
        aspect_ratio = args.aspect_ratio
    elif is_deck:
        aspect_ratio = "16:9"
    elif (mode == "reference"
          and getattr(args, "reference_type", None) != "product_embed"
          and args.reference_image_width and args.reference_image_height):
        aspect_ratio = _infer_aspect_ratio(args.reference_image_width, args.reference_image_height)
    else:
        aspect_ratio = "3:4"

    generation_config = {
        "responseModalities": ["IMAGE"],
        "imageConfig": {
            "aspectRatio": aspect_ratio,
            "image_size": "2K",
        },
    }

    if args.action:
        category = "infographic-batch" if is_batch else "infographic"
        content = {
            "mode": mode,
            "article": args.article,
            "reference_type": args.reference_type,
            "reference_image_urls": ref_urls,
            "reference_topic": args.reference_topic,
            "reference_article": args.reference_article,
            "action": args.action,
            "last_task_id": args.last_task_id,
            "locale": args.locale or "zh-CN",
            "generationConfig": generation_config,
        }
    elif is_deck:
        category = "infographic-deck"
        pages_data = None
        if getattr(args, 'pages', None) is not None:
            try:
                pages_data = json.loads(args.pages)
                if not isinstance(pages_data, list) or len(pages_data) < 2:
                    return {"success": False, "error": "--pages 必须是包含至少 2 项的 JSON 数组"}
            except (json.JSONDecodeError, TypeError) as e:
                return {"success": False, "error": f"--pages 参数 JSON 解析失败: {e}"}
        page_count = len(pages_data) if pages_data else min(max(round(args.page_count or 5), 3), 10)
        content = {
            "base_mode": mode,
            "topic": args.topic,
            "article": args.article,
            "article_summary": args.article_summary,
            "style_hint": args.style_hint,
            "template_id": args.template_id,
            "page_count": page_count,
            "aspect_ratio": aspect_ratio,
            "locale": args.locale or "zh-CN",
            "generationConfig": generation_config,
        }
        if pages_data:
            content["pages"] = pages_data
    elif is_batch:
        category = "infographic-batch"
        content = {
            "base_mode": mode,
            "count": count,
            "topic": args.topic,
            "article": args.article,
            "article_summary": args.article_summary,
            "style_hint": args.style_hint,
            "child_reference_type": args.child_reference_type or "style_transfer",
            "locale": args.locale or "zh-CN",
            "template_id": args.template_id,
            "generationConfig": generation_config,
        }
    else:
        category = "infographic"
        content = {
            "mode": mode,
            "topic": args.topic,
            "article": args.article,
            "article_summary": args.article_summary,
            "style_hint": args.style_hint,
            "locale": args.locale or "zh-CN",
            "template_id": args.template_id,
            "generationConfig": generation_config,
        }
        if mode == "reference":
            content["reference_type"] = args.reference_type
            content["reference_image_urls"] = ref_urls
            content["reference_topic"] = args.reference_topic
            content["reference_article"] = args.reference_article

    content = {k: v for k, v in content.items() if v is not None}

    log(f"create: category={category}, mode={mode}, count={count}, deck={is_deck}")

    title = args.title
    if not title:
        def _label():
            if args.topic:
                return args.topic
            if args.article:
                text = args.article.strip().split("\n")[0][:15]
                return text + ("..." if len(args.article.strip()) > 15 else "")
            return None

        if args.action:
            title = "卡片-重试"
        elif is_deck:
            title = f"卡片-幻灯片-{_label() or '套件'}-{page_count}页"
        elif is_batch:
            title = f"卡片-批量-{_label() or '转换'}-{count}张"
        elif mode == "topic":
            title = f"卡片-{args.topic}"
        elif mode == "article":
            title = f"卡片-{_label() or '长文转换'}"
        elif mode == "reference":
            ref_names = {
                "sketch": "手绘转卡片",
                "style_transfer": "仿风格卡片",
                "product_embed": "产品融入卡片",
                "content_rewrite": "内容改写",
            }
            title = f"卡片-{ref_names.get(args.reference_type, '参考图模式')}"

    result = plume_api.create_task(
        category=category,
        content=content,
        title=title,
    )

    log(f"create result: success={result.get('success')}, task_id={result.get('data', {}).get('id')}")

    if result.get("success"):
        task_data = result.get("data", {})
        task_id = task_data.get("id")

        if task_id:
            log_entry = {
                "task_id": task_id,
                "action": args.action,
                "last_task_id": args.last_task_id,
                "mode": mode,
                "params": _build_params_snapshot(args, mode),
            }
            action_log.append_entry(args.channel or "", log_entry)

        return {
            "success": True,
            "task_id": task_id,
            "category": category,
            "count": count,
            "status": task_data.get("status"),
            "credits_cost": task_data.get("credits_cost"),
        }
    else:
        return {
            "success": False,
            "code": result.get("code"),
            "error": result.get("message", "任务创建失败"),
        }


# ─── 同步轮询与下载 ──────────────────────────────────────────

SSL_CONTEXT = ssl.create_default_context()
MAX_REDIRECTS = 5
ALLOWED_CONTENT_TYPES = ("image/",)


class RedirectLimitHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, max_redirects: int = 5):
        self.max_redirects = max_redirects
        self.redirect_count = 0

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if self.redirect_count >= self.max_redirects:
            raise urllib.error.URLError("Too many redirects")
        if not newurl.startswith("https://"):
            raise urllib.error.URLError("Only HTTPS redirects are allowed")
        self.redirect_count += 1
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _poll_until_done(task_id: str, interval: int, timeout: int) -> dict:
    """同步轮询直到任务终态或超时"""
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed > timeout:
            return {"timeout": True, "elapsed": elapsed}

        result = plume_api.get_task(task_id)
        if not result.get("success"):
            code = result.get("code", "")
            if code in ("NOT_FOUND", "UNAUTHORIZED", "FORBIDDEN"):
                return {"error": True, "code": code,
                        "message": result.get("message", "")}
            log(f"查询失败 [{code}]，{interval}s 后重试")
            time.sleep(interval)
            continue

        task = result.get("data", {})
        status = task.get("status", 0)

        if status >= 3:
            return {"done": True, "task": task, "status": status}

        log(f"任务 {task_id} 处理中 (status={status}, elapsed={elapsed:.0f}s/{timeout}s)")
        time.sleep(interval)


def _download_file(url: str, output_path: str, timeout: int = 120) -> bool:
    """安全下载文件到本地：仅 HTTPS + 限制重定向 + 校验 Content-Type"""
    if not url.startswith("https://"):
        log(f"下载拒绝：仅允许 HTTPS URL, url={url[:80]}")
        return False

    opener = urllib.request.build_opener(
        RedirectLimitHandler(MAX_REDIRECTS),
        urllib.request.HTTPSHandler(context=SSL_CONTEXT),
    )

    req = urllib.request.Request(url, headers={"User-Agent": "Plume-Notecard/1.0"})
    try:
        with opener.open(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if not content_type.startswith(ALLOWED_CONTENT_TYPES):
                log(f"下载拒绝：非法 Content-Type={content_type}")
                return False

            with open(output_path, "wb") as f:
                while True:
                    chunk = resp.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
        if os.path.getsize(output_path) == 0:
            os.remove(output_path)
            return False
        return True
    except Exception as e:
        log(f"下载失败: {e}")
        try:
            if os.path.exists(output_path):
                os.remove(output_path)
        except OSError:
            pass
        return False


def _extract_result_urls(task_result: dict) -> list[tuple[str, str]]:
    """从任务结果中提取所有结果 URL，返回 [(url, media_type), ...]"""
    results = []
    if not isinstance(task_result, dict):
        return results

    parts = task_result.get("parts")
    if isinstance(parts, list):
        for part in parts:
            if isinstance(part, dict):
                url = part.get("imageUrl") or part.get("url")
                if url:
                    results.append((url, "image"))

    if not results:
        url = task_result.get("imageUrl") or task_result.get("url")
        if url:
            results.append((url, "image"))

    return results


def _download_results(task_id: str, task: dict) -> dict:
    """下载任务结果图片到本地，返回包含路径列表的 dict"""
    task_result = task.get("result")
    if isinstance(task_result, str):
        try:
            task_result = json.loads(task_result)
        except json.JSONDecodeError:
            pass

    urls = _extract_result_urls(task_result)
    if not urls:
        return {"success": True, "images": [], "result_urls": []}

    media_dir = config.get_media_dir()
    media_dir.mkdir(parents=True, exist_ok=True)

    local_files = []
    result_urls = []
    for i, (url, _media_type) in enumerate(urls):
        suffix = ".jpg" if ".jpg" in url.lower() or ".jpeg" in url.lower() else ".png"
        idx_label = f"_{i + 1}" if len(urls) > 1 else ""
        local_file = str(media_dir / f"result_{task_id}{idx_label}{suffix}")
        if _download_file(url, local_file):
            local_files.append(local_file)
            result_urls.append(url)
            log(f"下载完成 ({i + 1}/{len(urls)}): {local_file}")
        else:
            log(f"下载失败 ({i + 1}/{len(urls)})")

    return {"success": True, "images": local_files, "result_urls": result_urls}


def _create_zip_archive(image_paths: list[str], output_path: str | None = None) -> dict:
    """
    Package multiple images into a ZIP file

    Args:
        image_paths: List of image file paths
        output_path: Output ZIP path (optional, defaults to first image directory)

    Returns:
        {"success": bool, "zip_path": str, "file_count": int, "file_size_mb": float}
    """
    import zipfile

    if not image_paths:
        return {"success": False, "error": "Image list is empty"}

    # Verify all image files exist
    missing_files = [p for p in image_paths if not os.path.exists(p)]
    if missing_files:
        return {
            "success": False,
            "error": f"Image files not found: {', '.join(missing_files)}"
        }

    # Generate default output path
    if not output_path:
        first_image_dir = os.path.dirname(image_paths[0])
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(first_image_dir, f"notecards_{timestamp}.zip")

    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for path in image_paths:
                # Use filename as path inside ZIP
                arcname = os.path.basename(path)
                zipf.write(path, arcname)
                log(f"Added to ZIP: {arcname}")

        # Get file size
        file_size = os.path.getsize(output_path) / (1024 * 1024)

        log(f"ZIP packaging successful: {output_path} ({len(image_paths)} files, {file_size:.2f} MB)")

        return {
            "success": True,
            "zip_path": output_path,
            "file_count": len(image_paths),
            "file_size_mb": round(file_size, 2)
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"ZIP packaging failed: {str(e)}"
        }


def _merge_images_to_pdf(image_paths: list[str], output_path: str | None = None) -> dict:
    """
    Merge multiple images into a PDF

    Args:
        image_paths: List of image file paths
        output_path: Output PDF path (optional, defaults to first image directory)

    Returns:
        {"success": bool, "pdf_path": str, "page_count": int, "file_size_mb": float}
    """
    try:
        from PIL import Image
    except ImportError:
        return {
            "success": False,
            "error": "Pillow library not installed. Please run: pip install Pillow"
        }

    if not image_paths:
        return {"success": False, "error": "Image list is empty"}

    # Verify all image files exist
    missing_files = [p for p in image_paths if not os.path.exists(p)]
    if missing_files:
        return {
            "success": False,
            "error": f"Image files not found: {', '.join(missing_files)}"
        }

    # Generate default output path
    if not output_path:
        first_image_dir = os.path.dirname(image_paths[0])
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(first_image_dir, f"merged_{timestamp}.pdf")

    try:
        # Load all images and convert to RGB
        images = []
        for path in image_paths:
            try:
                img = Image.open(path)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                images.append(img)
                log(f"Loaded image: {path}")
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Cannot open image {path}: {str(e)}"
                }

        if not images:
            return {"success": False, "error": "No valid images"}

        # Save as PDF
        images[0].save(
            output_path,
            save_all=True,
            append_images=images[1:] if len(images) > 1 else [],
            resolution=100.0,
            quality=95
        )

        # Get file size
        file_size = os.path.getsize(output_path) / (1024 * 1024)

        log(f"PDF merge successful: {output_path} ({len(images)} pages, {file_size:.2f} MB)")

        return {
            "success": True,
            "pdf_path": output_path,
            "page_count": len(images),
            "file_size_mb": round(file_size, 2)
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"PDF merge failed: {str(e)}"
        }


def cmd_merge_pdf(args):
    """Merge multiple images into PDF"""
    if not args.images:
        output({"success": False, "error": "--images parameter is required"})
        return

    image_paths = [p.strip() for p in args.images.split(",") if p.strip()]
    if not image_paths:
        output({"success": False, "error": "Image list is empty"})
        return

    result = _merge_images_to_pdf(image_paths, args.output)
    output(result)


def cmd_create_zip(args):
    """Package multiple images into ZIP"""
    if not args.images:
        output({"success": False, "error": "--images parameter is required"})
        return

    image_paths = [p.strip() for p in args.images.split(",") if p.strip()]
    if not image_paths:
        output({"success": False, "error": "Image list is empty"})
        return

    result = _create_zip_archive(image_paths, args.output)
    output(result)


def cmd_history(args):
    """读取操作日志历史"""
    entries = action_log.read_log(args.channel or "")
    if args.limit and args.limit > 0:
        entries = entries[-args.limit:]
    output({
        "success": True,
        "channel": args.channel,
        "count": len(entries),
        "entries": entries,
    })


def cmd_create(args):
    """创建卡片任务并同步等待结果"""
    breaker_msg = _check_circuit_breaker(args.channel)
    if breaker_msg:
        log(f"熔断触发: {breaker_msg}")
        output({
            "success": False,
            "code": "CIRCUIT_BREAKER",
            "error": breaker_msg,
        })
        return

    create_result = _do_create(args)
    if not create_result.get("success"):
        output(create_result)
        return

    task_id = create_result["task_id"]
    log(f"任务已创建 task_id={task_id}，开始同步等待...")

    poll_result = _poll_until_done(task_id, args.poll_interval, args.timeout)

    if poll_result.get("timeout"):
        output({
            "success": False,
            "task_id": task_id,
            "status": "timeout",
            "error": f"等待超时（{args.timeout}s），任务仍在处理中",
            "credits_cost": create_result.get("credits_cost"),
        })
        return

    if poll_result.get("error"):
        output({
            "success": False,
            "task_id": task_id,
            "code": poll_result["code"],
            "error": poll_result.get("message", "查询任务失败"),
        })
        return

    task = poll_result["task"]
    status = poll_result["status"]

    if status != 3:
        status_map = {4: "失败", 5: "超时", 6: "作废"}
        status_text = status_map.get(status, f"未知({status})")
        error_info = task.get("result", "")

        status_key_map = {4: "failed", 5: "timeout", 6: "cancelled"}
        action_log.update_entry(args.channel or "", task_id, {
            "status": status_key_map.get(status, f"unknown_{status}"),
            "error": str(error_info) if error_info else None,
        })

        output({
            "success": False,
            "task_id": task_id,
            "status": status,
            "status_text": status_text,
            "error": str(error_info) if error_info else status_text,
        })
        return

    dl = _download_results(task_id, task)

    action_log.update_entry(args.channel or "", task_id, {
        "status": "success",
        "result_url": dl["result_urls"][0] if dl["result_urls"] else None,
        "result_urls": dl["result_urls"],
        "local_file": dl["images"][0] if dl["images"] else None,
        "local_files": dl["images"],
    })

    result = {
        "success": True,
        "task_id": task_id,
        "status": status,
        "images": dl["images"],
        "result_urls": dl["result_urls"],
        "count": len(dl["images"]),
        "credits_cost": create_result.get("credits_cost"),
    }

    # If --merge-to-pdf is enabled and multiple images, auto-merge
    if args.merge_to_pdf and len(dl["images"]) > 1:
        log("Detected --merge-to-pdf option, starting PDF merge...")
        pdf_result = _merge_images_to_pdf(dl["images"])
        if pdf_result.get("success"):
            result["pdf"] = {
                "path": pdf_result["pdf_path"],
                "page_count": pdf_result["page_count"],
                "file_size_mb": pdf_result["file_size_mb"]
            }
            log(f"PDF merge successful: {pdf_result['pdf_path']}")
        else:
            log(f"PDF merge failed: {pdf_result.get('error')}")
            result["pdf_error"] = pdf_result.get("error")

    # If --create-zip is enabled and multiple images, auto-package
    if args.create_zip and len(dl["images"]) > 1:
        log("Detected --create-zip option, starting ZIP packaging...")
        zip_result = _create_zip_archive(dl["images"])
        if zip_result.get("success"):
            result["zip"] = {
                "path": zip_result["zip_path"],
                "file_count": zip_result["file_count"],
                "file_size_mb": zip_result["file_size_mb"]
            }
            log(f"ZIP packaging successful: {zip_result['zip_path']}")
        else:
            log(f"ZIP packaging failed: {zip_result.get('error')}")
            result["zip_error"] = zip_result.get("error")

    output(result)


def main():
    parser = argparse.ArgumentParser(description="Plume 卡片创建脚本")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_transfer = subparsers.add_parser("transfer", help="本地文件中转到 R2")
    p_transfer.add_argument("--file", required=True, help="本地文件路径")

    p_history = subparsers.add_parser("history", help="读取操作日志历史")
    p_history.add_argument("--channel", help="渠道标识")
    p_history.add_argument("--limit", type=int, default=10, help="返回最近 N 条记录")

    p_merge_pdf = subparsers.add_parser("merge-pdf", help="Merge multiple images into PDF")
    p_merge_pdf.add_argument("--images", required=True, help="Image paths, comma-separated")
    p_merge_pdf.add_argument("--output", help="Output PDF path (optional)")

    p_create_zip = subparsers.add_parser("create-zip", help="Package multiple images into ZIP")
    p_create_zip.add_argument("--images", required=True, help="Image paths, comma-separated")
    p_create_zip.add_argument("--output", help="Output ZIP path (optional)")

    p_create = subparsers.add_parser("create", help="创建卡片任务并同步等待结果")
    p_create.add_argument("--mode", choices=["topic", "article", "reference"], help="卡片模式")
    p_create.add_argument("--topic", help="主题（mode=topic 时必填）")
    p_create.add_argument("--article", help="长文内容（mode=article 时必填）")
    p_create.add_argument("--article-summary", help="文章摘要（可选）")
    p_create.add_argument("--style-hint", help="风格提示（最多10字，可选）")
    p_create.add_argument("--aspect-ratio", default=None, help="比例: 3:4(默认) / 4:3 / 1:1 / 16:9 / 9:16")
    p_create.add_argument("--locale", default=None, help="语言: zh-CN(默认) / en-US / ja-JP 等")
    p_create.add_argument("--count", type=int, default=1, help="生成数量，>=2 触发批量模式")
    p_create.add_argument("--deck-mode", action="store_true", default=False, help="生成幻灯片套件，默认 16:9")
    p_create.add_argument("--page-count", type=int, default=None, help="幻灯片套件页数（3-10）")
    p_create.add_argument("--pages", default=None, help="幻灯片套件结构化页面内容，JSON 数组字符串")
    p_create.add_argument("--child-reference-type", choices=["style_transfer", "content_rewrite"], help="批量模式子任务策略")
    p_create.add_argument("--action", choices=["repeat_last_task", "switch_style", "switch_content", "switch_all"], help="重试动作")
    p_create.add_argument("--last-task-id", help="重试时的上一个任务 ID")
    p_create.add_argument("--template-id", help="指定模板 ID（可选）")
    p_create.add_argument("--reference-type", choices=["sketch", "style_transfer", "product_embed", "content_rewrite"], help="参考图类型")
    p_create.add_argument("--reference-image-urls", help="参考图 URL，逗号分隔")
    p_create.add_argument("--reference-topic", help="参考图模式下的新主题")
    p_create.add_argument("--reference-article", help="参考图模式下的新内容")
    p_create.add_argument("--reference-image-width", type=int, default=None, help="参考图宽度（px）")
    p_create.add_argument("--reference-image-height", type=int, default=None, help="参考图高度（px）")
    p_create.add_argument("--channel", help="渠道标识，用于写入操作日志")
    p_create.add_argument("--title", help="任务标题（可选）")
    p_create.add_argument("--poll-interval", type=int, default=10, help="轮询间隔秒数（默认 10）")
    p_create.add_argument("--timeout", type=int, default=1800, help="最大等待秒数（默认 1800）")
    p_create.add_argument("--merge-to-pdf", action="store_true", default=False, help="Auto-merge multiple images to PDF (batch/deck mode only)")
    p_create.add_argument("--create-zip", action="store_true", default=False, help="Auto-package multiple images to ZIP (batch/deck mode only)")

    args = parser.parse_args()

    commands = {
        "transfer": cmd_transfer,
        "history": cmd_history,
        "merge-pdf": cmd_merge_pdf,
        "create-zip": cmd_create_zip,
        "create": cmd_create,
    }

    try:
        log(f"=== create_notecard.py {args.command} called, argv={sys.argv[1:]} ===")
        commands[args.command](args)
    except Exception as e:
        output({"success": False, "error": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()
