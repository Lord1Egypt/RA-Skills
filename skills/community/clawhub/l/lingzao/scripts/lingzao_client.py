#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import http.client
import json
import mimetypes
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, TextIO

CONFIG_FILE = Path.home() / ".lingzao" / "config.json"
DEFAULT_TIMEOUT = 180
GENERATE_IMAGE_POLL_TIMEOUT = 300
GENERATE_IMAGE_DOWNLOAD_TIMEOUT_BUFFER = 60
SKILL_ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = SKILL_ROOT / "VERSION"
DEFAULT_SKILL_BASE_URL = "https://assets-tian.midao.site/skills/lingzao"
LEGACY_WINDOWS_ENCODINGS = {"gbk", "gb2312", "cp936", "mbcs"}
FIXED_TIME_SAVED_MINUTES = {
    "search-notes": 20,
    "search-users": 20,
    "get-user-info": 5,
    "get-user-posted-notes": 15,
    "get-note-detail": 8,
    "get-note-comments": 12,
    "get-article-detail": 8,
    "get-article-stats": 5,
    "get-related-articles": 15,
    "generate-image": 40,
}
PUBLIC_SERVICE_ERROR_LABELS = {
    "NOTE_NOT_FOUND_OR_INACCESSIBLE": "目标内容未读取到或不可访问",
    "CREATOR_NOT_FOUND_OR_RESTRICTED": "目标频道未读取到或不可访问",
    "CONTENT_NOT_FOUND_OR_RESTRICTED": "目标视频未读取到或不可访问",
    "COMMENTS_UNAVAILABLE": "该视频的公开评论不可用",
    "YOUTUBE_CONTENT_TYPE_REQUIRED": "请指定 YouTube 视频类型",
    "YOUTUBE_CONTENT_TYPE_MISMATCH": "YouTube 视频类型与 URL 不一致",
    "UNSUPPORTED_CONTENT_TYPE_HINT": "当前平台不接受该视频类型参数",
    "NO_SUBTITLE_AVAILABLE": "该视频没有可用的原声字幕",
    "INSUFFICIENT_CREDITS": "当前积分不足，请充值后重试。",
    "PROVIDER_UNAVAILABLE": "灵造服务暂时不可用",
    "PROVIDER_TIMEOUT": "灵造服务响应超时",
}


def configure_standard_streams() -> None:
    configure_text_stream(sys.stdout)
    configure_text_stream(sys.stderr)


def configure_text_stream(stream: TextIO) -> None:
    reconfigure = getattr(stream, "reconfigure", None)
    if not callable(reconfigure):
        return

    options = {"errors": "replace"}
    if should_force_utf8(stream):
        options["encoding"] = "utf-8"

    try:
        reconfigure(**options)
    except (OSError, TypeError, ValueError):
        pass


def should_force_utf8(stream: TextIO) -> bool:
    encoding = normalize_encoding(getattr(stream, "encoding", None))
    return os.name == "nt" or encoding in LEGACY_WINDOWS_ENCODINGS


def normalize_encoding(value: Optional[str]) -> str:
    return (value or "").strip().lower().replace("_", "-")


def safe_print(value: object = "", *, file: Optional[TextIO] = None) -> None:
    stream = file or sys.stdout
    text = str(value)
    try:
        print(text, file=stream)
    except UnicodeEncodeError:
        write_text_safely(stream, text + "\n")


def write_text_safely(stream: TextIO, text: str) -> None:
    encoding = getattr(stream, "encoding", None) or "utf-8"
    try:
        safe_text = text.encode(encoding, errors="replace").decode(encoding, errors="replace")
        stream.write(safe_text)
        stream.flush()
        return
    except (OSError, UnicodeError, ValueError):
        pass

    buffer = getattr(stream, "buffer", None)
    if buffer is None:
        return

    try:
        buffer.write(text.encode("utf-8", errors="replace"))
        buffer.flush()
    except OSError:
        pass


def main() -> int:
    configure_standard_streams()

    parser = argparse.ArgumentParser(description="Lingzao API client for agent skills.")
    parser.add_argument("--base-url", help="Override Lingzao API base URL")
    parser.add_argument("--api-key", help="Override Lingzao API key")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument(
        "--skill-base-url",
        default=os.environ.get("LINGZAO_SKILL_BASE_URL", DEFAULT_SKILL_BASE_URL),
        help="Lingzao Skill package base URL for version checks",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    check_version_parser = subparsers.add_parser("check-version", help="Check whether the Lingzao skill has an update")
    check_version_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    doctor_parser = subparsers.add_parser("doctor", help="Validate config and API key without billing")
    doctor_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    search_notes_parser = subparsers.add_parser("search-notes", help="Search public content notes")
    search_notes_parser.add_argument("--platform", required=True)
    search_notes_parser.add_argument("--keyword", required=True)
    search_notes_parser.add_argument("--limit", type=int, default=20)
    search_notes_parser.add_argument("--cursor")
    search_notes_parser.add_argument(
        "--sort",
        choices=["general", "most_liked", "popularity_descending", "comment_descending", "collect_descending"],
        default="general",
    )
    search_notes_parser.add_argument("--note-type", choices=["不限", "视频笔记", "图文笔记", "直播笔记"], default="不限")
    search_notes_parser.add_argument("--time-filter", choices=["不限", "一天内", "一周内", "半年内"], default="不限")
    search_notes_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    search_users_parser = subparsers.add_parser("search-users", help="Search public creators")
    search_users_parser.add_argument("--platform", required=True)
    search_users_parser.add_argument("--keyword", required=True)
    search_users_parser.add_argument("--limit", type=int, default=20)
    search_users_parser.add_argument("--cursor")
    search_users_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    user_info_parser = subparsers.add_parser("get-user-info", help="Get public creator profile info")
    user_info_parser.add_argument("--platform")
    user_info_parser.add_argument("--url")
    user_info_parser.add_argument("--user-id")
    user_info_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    user_notes_parser = subparsers.add_parser(
        "get-user-posted-notes",
        help="Get recent public notes from a creator profile",
    )
    user_notes_parser.add_argument("--platform")
    user_notes_parser.add_argument("--url")
    user_notes_parser.add_argument("--user-id")
    user_notes_parser.add_argument("--limit", type=int, default=20)
    user_notes_parser.add_argument("--cursor")
    user_notes_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    analyze_user_profile_parser = subparsers.add_parser(
        "analyze-user-profile",
        help="Get deeper creator profile post data",
    )
    analyze_user_profile_parser.add_argument("--platform")
    analyze_user_profile_parser.add_argument("--url")
    analyze_user_profile_parser.add_argument("--user-id")
    analyze_user_profile_parser.add_argument("--limit", type=int, default=20)
    analyze_user_profile_parser.add_argument("--force-new", action="store_true")
    analyze_user_profile_parser.add_argument("--full-page", action=argparse.BooleanOptionalAction, default=None)
    analyze_user_profile_parser.add_argument("--cursor")
    analyze_user_profile_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    note_detail_parser = subparsers.add_parser("get-note-detail", help="Get one public note detail")
    note_detail_parser.add_argument("--platform")
    note_detail_parser.add_argument("--url")
    note_detail_parser.add_argument("--note-id")
    note_detail_parser.add_argument("--xhs-note-type", choices=["image", "video"])
    note_detail_parser.add_argument("--content-type", choices=["video", "short"])
    note_detail_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    note_comments_parser = subparsers.add_parser("get-note-comments", help="Get top-level comments for one public note")
    note_comments_parser.add_argument("--platform")
    note_comments_parser.add_argument("--url")
    note_comments_parser.add_argument("--note-id")
    note_comments_parser.add_argument("--cursor")
    note_comments_parser.add_argument("--limit", type=int, default=20)
    note_comments_parser.add_argument("--sort", choices=["latest", "most_liked"], default="latest")
    note_comments_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    article_detail_parser = subparsers.add_parser(
        "get-article-detail",
        help="Get one public WeChat official-account article detail",
    )
    article_detail_parser.add_argument("--platform")
    article_detail_parser.add_argument("--url", required=True)
    article_detail_parser.add_argument("--output", help="Optional path to write the full article Markdown file")
    article_detail_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    article_stats_parser = subparsers.add_parser(
        "get-article-stats",
        help="Get public metrics for one WeChat official-account article",
    )
    article_stats_parser.add_argument("--platform")
    article_stats_parser.add_argument("--url", required=True)
    article_stats_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    related_articles_parser = subparsers.add_parser(
        "get-related-articles",
        help="Get related public WeChat official-account articles",
    )
    related_articles_parser.add_argument("--platform")
    related_articles_parser.add_argument("--url", required=True)
    related_articles_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    extract_video_copy_parser = subparsers.add_parser(
        "extract-video-copy",
        help="Extract spoken copy/transcript from short video links",
    )
    extract_video_copy_parser.add_argument("--url", action="append", required=True)
    extract_video_copy_parser.add_argument(
        "--operation-id",
        help="UUID for retrying the same extraction intent within 24 hours. Omit for a new intent.",
    )
    extract_video_copy_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    generate_image_parser = subparsers.add_parser(
        "generate-image",
        help="Generate creator image assets from a prompt",
    )
    generate_image_parser.add_argument("--prompt", help="Image generation prompt text")
    generate_image_parser.add_argument(
        "--prompt-file",
        help="Read the image generation prompt from a UTF-8 text file. Useful for long or multiline prompts.",
    )
    generate_image_parser.add_argument(
        "--prompt-stdin",
        action="store_true",
        help="Read the image generation prompt from stdin. Useful when shell quoting is unreliable.",
    )
    generate_image_parser.add_argument(
        "--size",
        default="1024x1024",
        help="Image size, for example auto, 1024x1024, 1024x1536, 1536x2048, or 9:16.",
    )
    generate_image_parser.add_argument("--count", type=int, default=1, help="Number of images to create, 1-5.")
    generate_image_parser.add_argument("--output-format", choices=["png", "jpeg", "webp"], default="png")
    generate_image_parser.add_argument(
        "--reference-mode",
        choices=["shared", "one_to_one"],
        default="shared",
        help=(
            "How repeated --image files map to outputs. "
            "one_to_one requires the number of images to equal --count and supports at most 4 images."
        ),
    )
    generate_image_parser.add_argument(
        "--image",
        action="append",
        help="Optional reference image path. Repeat for multiple reference images.",
    )
    generate_image_parser.add_argument("--output", help="Optional path to write the generated image file")
    generate_image_parser.add_argument(
        "--client-request-id",
        help="UUID for explicitly retrying the same generation intent. Omit for a new intent.",
    )
    generate_image_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    for command in ("search-products", "get-product-detail", "get-product-reviews"):
        commerce_parser = subparsers.add_parser(command, help="Research public Xiaohongshu products")
        commerce_parser.add_argument("--platform", choices=["xhs"], required=True)
        commerce_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
        if command == "search-products":
            commerce_parser.add_argument("--keyword", required=True)
        else:
            commerce_parser.add_argument("--sku")
            commerce_parser.add_argument("--url")
        if command != "get-product-detail":
            commerce_parser.add_argument("--limit", type=int, default=20)
            commerce_parser.add_argument("--cursor")
        if command == "get-product-reviews":
            commerce_parser.add_argument("--sort", choices=["general", "latest"], default="general")

    args = parser.parse_args()

    if args.command == "check-version":
        payload = check_skill_version(args.skill_base_url, timeout=args.timeout)
        if args.format == "json":
            safe_print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            safe_print(render_version_check(payload))
        return 0

    validation_error = validate_args(args)
    if validation_error:
        safe_print(validation_error, file=sys.stderr)
        return 2

    config = resolve_config(args)

    generate_image_client_request_id: Optional[str] = None
    extract_video_copy_operation_id: Optional[str] = None
    try:
        if args.command == "doctor":
            payload = request_json(config, "GET", "/api/v1/me", timeout=args.timeout)
        elif args.command in {"search-products", "get-product-detail", "get-product-reviews"}:
            body = {"platform": args.platform}
            for field in ("keyword", "sku", "url", "limit", "cursor", "sort"):
                value = getattr(args, field, None)
                if value is not None:
                    body[field] = value
            payload = request_json(config, "POST", f"/api/v1/commerce/{args.command}", body, timeout=args.timeout)
        elif args.command == "search-notes":
            payload = request_json(
                config,
                "POST",
                "/api/v1/research/search-notes",
                compact({
                    "platform": args.platform,
                    "query": args.keyword,
                    "limit": args.limit,
                    "cursor": args.cursor,
                    "sort": args.sort,
                    "note_type": args.note_type,
                    "time_filter": args.time_filter,
                }),
                timeout=args.timeout,
            )
        elif args.command == "search-users":
            payload = request_json(
                config,
                "POST",
                "/api/v1/research/search-users",
                compact({
                    "platform": args.platform,
                    "query": args.keyword,
                    "limit": args.limit,
                    "cursor": args.cursor,
                }),
                timeout=args.timeout,
            )
        elif args.command == "get-user-info":
            payload = request_json(
                config,
                "POST",
                "/api/v1/research/get-user-info",
                compact({"platform": args.platform, "url": args.url, "user_id": args.user_id}),
                timeout=args.timeout,
            )
        elif args.command == "get-user-posted-notes":
            payload = request_json(
                config,
                "POST",
                "/api/v1/research/get-user-posted-notes",
                compact({
                    "platform": getattr(args, "platform", None),
                    "url": args.url,
                    "user_id": getattr(args, "user_id", None),
                    "limit": args.limit,
                    "cursor": getattr(args, "cursor", None),
                }),
                timeout=args.timeout,
            )
        elif args.command == "analyze-user-profile":
            payload = request_json(
                config,
                "POST",
                "/api/v1/research/analyze-user-profile",
                compact({
                    "platform": getattr(args, "platform", None),
                    "url": args.url,
                    "user_id": getattr(args, "user_id", None),
                    "limit": args.limit,
                    "force_new": args.force_new,
                    "full_page": args.full_page,
                    "cursor": args.cursor,
                }),
                timeout=args.timeout,
            )
        elif args.command == "get-note-detail":
            payload = request_json(
                config,
                "POST",
                "/api/v1/research/get-note-detail",
                compact({
                    "platform": getattr(args, "platform", None),
                    "url": args.url,
                    "note_id": getattr(args, "note_id", None),
                    "xhs_note_type": getattr(args, "xhs_note_type", None),
                    "content_type": getattr(args, "content_type", None),
                }),
                timeout=args.timeout,
            )
        elif args.command == "get-note-comments":
            payload = request_json(
                config,
                "POST",
                "/api/v1/research/get-note-comments",
                compact({
                    "platform": getattr(args, "platform", None),
                    "url": args.url,
                    "note_id": getattr(args, "note_id", None),
                    "cursor": getattr(args, "cursor", None),
                    "limit": getattr(args, "limit", 20),
                    "sort": getattr(args, "sort", None),
                }),
                timeout=args.timeout,
            )
        elif args.command == "get-article-detail":
            payload = request_json(
                config,
                "POST",
                "/api/v1/research/get-article-detail",
                compact({"platform": getattr(args, "platform", None), "url": args.url}),
                timeout=args.timeout,
            )
        elif args.command == "get-article-stats":
            payload = request_json(
                config,
                "POST",
                "/api/v1/research/get-article-stats",
                compact({"platform": getattr(args, "platform", None), "url": args.url}),
                timeout=args.timeout,
            )
        elif args.command == "get-related-articles":
            payload = request_json(
                config,
                "POST",
                "/api/v1/research/get-related-articles",
                compact({"platform": getattr(args, "platform", None), "url": args.url}),
                timeout=args.timeout,
            )
        elif args.command == "extract-video-copy":
            urls = [url for url in (getattr(args, "url", None) or []) if url]
            body = {"url": urls[0]} if len(urls) == 1 else {"urls": urls}
            extract_video_copy_operation_id = (
                getattr(args, "operation_id", None) or str(uuid.uuid4())
            )
            safe_print(f"文案提取请求 ID：{extract_video_copy_operation_id}", file=sys.stderr)
            payload = request_json(
                config,
                "POST",
                "/api/v1/research/extract-video-copy",
                body,
                timeout=args.timeout,
                headers={"Idempotency-Key": extract_video_copy_operation_id},
            )
        elif args.command == "generate-image":
            prompt = resolve_generate_image_prompt(args)
            generate_image_client_request_id = (
                getattr(args, "client_request_id", None) or str(uuid.uuid4())
            )
            body = {
                "prompt": prompt,
                "size": args.size,
                "output_format": args.output_format,
                "count": args.count,
                "client_request_id": generate_image_client_request_id,
            }
            if args.reference_mode == "one_to_one":
                body["reference_mode"] = args.reference_mode
            image_paths = getattr(args, "image", None) or []
            safe_print(
                f"图片生成请求 ID：{generate_image_client_request_id}",
                file=sys.stderr,
            )
            try:
                payload = submit_generate_image_batch(
                    config,
                    body,
                    image_paths,
                    timeout=args.timeout,
                )
            except LingzaoApiError as error:
                active_payload = active_generate_image_batch_payload_from_error(
                    error,
                    requested_count=args.count,
                )
                if not active_payload:
                    raise
                active_data = as_dict(active_payload.get("data"))
                safe_print(
                    "检测到另一个图片生成批次正在运行，"
                    f"等待其结束后再提交当前请求：{active_data.get('batch_id')}",
                    file=sys.stderr,
                )
                wait_for_generate_image_batch(config, active_payload, timeout=args.timeout)
                safe_print("已有批次已结束，正在提交当前图片生成请求...", file=sys.stderr)
                payload = submit_generate_image_batch(
                    config,
                    body,
                    image_paths,
                    timeout=args.timeout,
                )
            payload = wait_for_generate_image_batch(config, payload, timeout=args.timeout)
            ensure_generate_image_success(payload)
        else:
            raise RuntimeError(f"Unsupported command: {args.command}")
    except LingzaoError as error:
        safe_print(str(error), file=sys.stderr)
        if (
            args.command == "generate-image"
            and generate_image_client_request_id
            and should_show_generate_image_recovery_hint(error)
        ):
            safe_print(
                "如果网络响应不确定或轮询中断，请保持原请求参数不变，并重试时添加 "
                f"`--client-request-id {generate_image_client_request_id}`。",
                file=sys.stderr,
            )
        return 1

    local_outputs: List[str] = []
    local_article_output: Optional[str] = None
    try:
        if args.command == "generate-image" and getattr(args, "output", None):
            local_outputs = write_generated_images(payload, args.output)
        elif args.command == "get-article-detail" and getattr(args, "output", None):
            local_article_output = write_article_markdown(payload, args.output)
    except LingzaoError as error:
        safe_print(str(error), file=sys.stderr)
        return 1

    if args.format == "json":
        safe_print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if local_outputs:
            payload = {**payload, "_local_output": local_outputs[0], "_local_outputs": local_outputs}
        if local_article_output:
            payload = {**payload, "_local_article_output": local_article_output}
        safe_print(to_markdown(args.command, payload))
    return 0


class LingzaoError(Exception):
    pass


class LingzaoApiError(LingzaoError):
    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        code: Optional[str] = None,
        error_id: Optional[str] = None,
        payload: Optional[dict] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.error_id = error_id
        self.payload = payload or {}


def classify_youtube_detail_input(args: argparse.Namespace, url: str) -> str:
    if getattr(args, "note_id", None):
        return "video"
    if not url:
        return "invalid"

    try:
        parsed = urllib.parse.urlparse(url)
    except ValueError:
        return "invalid"

    hostname = (parsed.hostname or "").lower()
    path = parsed.path.rstrip("/")
    if hostname == "youtu.be" or hostname.endswith(".youtu.be"):
        return "video" if path.strip("/") else "invalid"
    if hostname != "youtube.com" and not hostname.endswith(".youtube.com"):
        return "invalid"
    if path == "/watch" and urllib.parse.parse_qs(parsed.query).get("v"):
        return "video"
    if path.startswith("/shorts/") and path[len("/shorts/") :]:
        return "short"
    if path.startswith(("/channel/", "/@", "/c/", "/user/")):
        return "profile"
    return "invalid"


def validate_args(args: argparse.Namespace) -> Optional[str]:
    if args.command in {"search-products", "get-product-detail", "get-product-reviews"}:
        if not 1 <= getattr(args, "limit", 20) <= 20:
            return "商品研究 --limit 必须在 1 到 20 之间。"
        if args.command == "search-products":
            if not 1 <= len(args.keyword.strip()) <= 80:
                return "商品关键词长度必须在 1 到 80 之间。"
        else:
            sku = getattr(args, "sku", None)
            url = getattr(args, "url", None)
            if not sku and not url:
                return "请提供搜索结果中的 --sku 或商品 --url。"
            if sku and (not re.fullmatch(r"[a-f0-9]{24}", sku) or sku == "0" * 24):
                return "商品 sku 无效，请使用搜索结果里的 sku。"
            if url:
                parsed = urllib.parse.urlparse(url)
                match = re.fullmatch(r"/goods-detail/([a-f0-9]{24})/?", parsed.path)
                if parsed.scheme != "https" or parsed.netloc not in {"www.xiaohongshu.com", "xiaohongshu.com"} or not match or match[1] == "0" * 24 or (sku and sku != match[1]):
                    return "请提供正确的小红书商品链接，sku 必须与链接一致。"
        return None

    if args.command == "get-user-posted-notes" and not 1 <= args.limit <= 100:
        return "get-user-posted-notes --limit must be between 1 and 100; values 21–100 return at most 20 with a notice; use next_cursor with --cursor for more."
    platform = (getattr(args, "platform", None) or "").strip().lower()
    raw_url = getattr(args, "url", None)
    if isinstance(raw_url, list):
        url = " ".join(str(value) for value in raw_url).strip().lower()
    else:
        url = str(raw_url or "").strip().lower()
    is_youtube = platform in {"youtube", "yt"} or "youtube.com" in url or "youtu.be" in url
    is_tiktok = platform in {"tiktok", "tt"} or "tiktok.com" in url
    is_instagram = platform in {"instagram", "ig", "ins"} or "instagram.com" in url
    is_wechat_channels = (
        platform in {"wechat_channels", "weixin_channels", "channels", "finder"}
        or "weixin.qq.com/sph/" in url
    )

    if args.command in {"search-notes", "search-users"} and (is_youtube or is_wechat_channels) and args.limit > 20:
        label = "WeChat Channels" if is_wechat_channels else "YouTube"
        return f"{label} {args.command} supports --limit 20 at most."

    if args.command == "search-notes" and is_youtube:
        if args.sort != "general":
            return "YouTube search-notes supports only --sort general."
        if args.note_type not in {"不限", "视频笔记"}:
            return "YouTube search-notes supports only --note-type 不限 or 视频笔记."
        if args.time_filter not in {"不限", "一天内", "一周内"}:
            return "YouTube search-notes supports only --time-filter 不限, 一天内, or 一周内."

    if args.command == "search-notes" and is_wechat_channels:
        if args.sort not in {"general", "most_liked", "popularity_descending"}:
            return "WeChat Channels search-notes supports only general, most_liked, or popularity_descending sorting."
        if args.note_type not in {"不限", "视频笔记"}:
            return "WeChat Channels search-notes supports video content only; use --note-type 视频笔记."

    if args.command == "get-note-detail":
        content_type = getattr(args, "content_type", None)
        if is_youtube:
            input_kind = classify_youtube_detail_input(args, url)
            if input_kind == "profile":
                return (
                    "YouTube channel URLs are not content-detail inputs. "
                    "Use get-user-info or get-user-posted-notes; use search-users first for @handle, /c/, or /user/ URLs."
                )
            if input_kind == "invalid":
                return (
                    "YouTube get-note-detail accepts a video ID, watch?v= URL, youtu.be URL, or /shorts/ URL."
                )
            if input_kind == "short" and content_type == "video":
                return "YouTube /shorts/ URLs only accept --content-type short."
            if input_kind == "video" and not content_type:
                return (
                    "YouTube video IDs, watch?v= URLs, and youtu.be URLs require "
                    "--content-type video or --content-type short."
                )
        elif content_type:
            return "--content-type is supported for YouTube get-note-detail only."

    if args.command == "get-note-comments" and (args.limit < 1 or args.limit > 20):
        return "get-note-comments --limit must be between 1 and 20."
    if args.command == "get-note-comments" and not (
        is_tiktok or is_instagram or is_youtube or is_wechat_channels
    ) and args.limit != 20:
        return "Custom get-note-comments --limit is currently supported for TikTok, Instagram, YouTube, or WeChat Channels only."

    if args.command == "extract-video-copy":
        operation_id = getattr(args, "operation_id", None)
        if operation_id and not is_uuid(operation_id):
            return "extract-video-copy --operation-id must be a UUID."

    if args.command == "generate-image":
        prompt_arg = getattr(args, "prompt", None)
        prompt_sources = sum([
            prompt_arg is not None,
            bool(getattr(args, "prompt_file", None)),
            bool(getattr(args, "prompt_stdin", False)),
        ])
        if prompt_sources == 0:
            return "generate-image requires one prompt source: --prompt, --prompt-file, or --prompt-stdin."
        if prompt_sources > 1:
            return "generate-image accepts only one prompt source. Use one of --prompt, --prompt-file, or --prompt-stdin."
        if prompt_arg is not None and not prompt_arg.strip():
            return "generate-image prompt cannot be empty."
        client_request_id = getattr(args, "client_request_id", None)
        if client_request_id and not is_uuid(client_request_id):
            return "generate-image --client-request-id must be a UUID."
        count = getattr(args, "count", 1)
        if count < 1 or count > 5:
            return "generate-image --count must be between 1 and 5."
        image_paths = getattr(args, "image", None) or []
        reference_mode = getattr(args, "reference_mode", "shared")
        if reference_mode == "one_to_one" and count > 4:
            return "generate-image --reference-mode one_to_one supports at most 4 reference images."
        if len(image_paths) > 4:
            return "generate-image accepts at most 4 --image files."
        if (
            reference_mode == "one_to_one" and
            len(image_paths) != count
        ):
            return (
                "generate-image --reference-mode one_to_one requires "
                "the number of --image files to equal --count."
            )
        if getattr(args, "format", "markdown") == "markdown" and not getattr(args, "output", None):
            return (
                "generate-image markdown output requires --output so generated images are saved. "
                "Use --format json for structured automation data."
            )

    if args.command == "get-article-detail" and getattr(args, "output", None):
        try:
            preflight_article_output_path(args.output)
        except LingzaoError as error:
            return str(error)

    if args.command == "get-note-comments" and getattr(args, "sort", None) == "most_liked":
        if platform in {"douyin", "dy"} or "douyin.com" in url or "iesdouyin.com" in url:
            return (
                "Douyin get-note-comments supports only --sort latest. "
                "Do not pass --sort most_liked for Douyin comments."
            )
        if platform in {"tiktok", "tt"} or "tiktok.com" in url:
            return (
                "TikTok get-note-comments supports only --sort latest (service-default order). "
                "Do not pass --sort most_liked for TikTok comments."
            )
        if platform in {"instagram", "ig", "ins"} or "instagram.com" in url:
            return (
                "Instagram get-note-comments supports only --sort latest. "
                "Do not pass --sort most_liked for Instagram comments."
            )
        if is_wechat_channels:
            return (
                "WeChat Channels get-note-comments supports only --sort latest. "
                "Do not pass --sort most_liked for WeChat Channels comments."
            )

    platform = (getattr(args, "platform", None) or "").strip().lower()
    raw_url = getattr(args, "url", None)
    url = raw_url.strip().lower() if isinstance(raw_url, str) else ""
    if platform in {"tiktok", "tt"} or "tiktok.com" in url:
        if args.command == "analyze-user-profile":
            return "TikTok analyze-user-profile is not available in V1; compose get-user-info and get-user-posted-notes."
        if args.command in {"search-notes", "search-users", "get-note-comments"}:
            limit = getattr(args, "limit", 20)
            if limit < 1 or limit > 20:
                return f"TikTok {args.command} --limit must be between 1 and 20."
        if args.command == "search-notes":
            if getattr(args, "note_type", "不限") == "直播笔记":
                return "TikTok search-notes does not support --note-type 直播笔记."
            if getattr(args, "sort", "general") in {"comment_descending", "collect_descending"}:
                return "TikTok search-notes supports only general, most_liked, or popularity_descending sorting."

    if platform in {"instagram", "ig", "ins"} or "instagram.com" in url:
        if args.command == "analyze-user-profile":
            return "Instagram analyze-user-profile is not available in V1; compose get-user-info and get-user-posted-notes only when both are needed."
        if args.command in {"search-notes", "search-users", "get-note-comments"}:
            limit = getattr(args, "limit", 20)
            if limit < 1 or limit > 20:
                return f"Instagram {args.command} --limit must be between 1 and 20."
        if args.command == "search-notes":
            if getattr(args, "sort", "general") != "general":
                return "Instagram search-notes supports only --sort general."
            if getattr(args, "note_type", "不限") not in {"不限", "视频笔记"}:
                return "Instagram content search is Reels-only; use --note-type 视频笔记."
            if getattr(args, "time_filter", "不限") != "不限":
                return "Instagram search-notes supports only --time-filter 不限."
        if args.command == "get-note-comments":
            note_id = str(getattr(args, "note_id", "") or "")
            if note_id.isdigit():
                return "Instagram get-note-comments --note-id must be a public shortcode, not a decimal media ID; otherwise pass the canonical content URL."

    if platform in {"wechat_channels", "weixin_channels", "channels", "finder"} or "weixin.qq.com/sph/" in url:
        if args.command == "analyze-user-profile":
            return "WeChat Channels analyze-user-profile is not available in V1; compose get-user-info and get-user-posted-notes only when both are needed."
        if args.command in {"search-notes", "search-users", "get-note-comments"}:
            limit = getattr(args, "limit", 20)
            if limit < 1 or limit > 20:
                return f"WeChat Channels {args.command} --limit must be between 1 and 20."
        if args.command == "get-note-comments":
            note_id = str(getattr(args, "note_id", "") or "")
            if url or not note_id.isdigit():
                return "WeChat Channels get-note-comments requires the numeric --note-id returned by get-note-detail; content URLs and export IDs are not accepted."

    return None


def resolve_generate_image_prompt(args: argparse.Namespace) -> str:
    if getattr(args, "prompt_file", None):
        path = Path(str(args.prompt_file)).expanduser()
        try:
            prompt = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            raise LingzaoError("generate-image --prompt-file must be a UTF-8 text file.") from error
        except OSError as error:
            raise LingzaoError(f"generate-image --prompt-file could not be read: {path}") from error
    elif getattr(args, "prompt_stdin", False):
        try:
            prompt = sys.stdin.buffer.read().decode("utf-8")
        except UnicodeDecodeError as error:
            raise LingzaoError("generate-image --prompt-stdin must be UTF-8 text.") from error
    else:
        prompt = str(getattr(args, "prompt", "") or "")

    if not prompt.strip():
        raise LingzaoError("generate-image prompt cannot be empty.")
    return prompt


def check_skill_version(skill_base_url: str, timeout: int = DEFAULT_TIMEOUT) -> dict:
    local_version = read_local_version()
    remote_version = None
    error = None
    base_url = str(skill_base_url or DEFAULT_SKILL_BASE_URL).strip().rstrip("/")
    version_url = f"{base_url}/VERSION"

    try:
        request = urllib.request.Request(
            version_url,
            headers={
                "accept": "text/plain",
                "user-agent": "LingzaoSkill/1.0",
            },
            method="GET",
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            remote_version = response.read().decode("utf-8").strip()
    except (OSError, UnicodeDecodeError, TimeoutError) as exc:
        error = str(exc)

    update_available = (
        bool(local_version and remote_version)
        and compare_versions(remote_version, local_version) > 0
    )
    return {
        "ok": error is None,
        "local_version": local_version,
        "remote_version": remote_version,
        "update_available": update_available,
        "version_url": version_url,
        "error": error,
    }


def read_local_version() -> str:
    try:
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        return "unknown"


def compare_versions(left: str, right: str) -> int:
    left_parts = version_parts(left)
    right_parts = version_parts(right)
    width = max(len(left_parts), len(right_parts))
    left_parts.extend([0] * (width - len(left_parts)))
    right_parts.extend([0] * (width - len(right_parts)))
    if left_parts > right_parts:
        return 1
    if left_parts < right_parts:
        return -1
    return 0


def version_parts(value: str) -> List[int]:
    parts: List[int] = []
    for raw_part in value.strip().lstrip("v").split("."):
        number = ""
        for char in raw_part:
            if char.isdigit():
                number += char
            else:
                break
        parts.append(int(number or "0"))
    return parts


def resolve_config(args: argparse.Namespace) -> dict:
    saved = load_config()
    api_key = args.api_key or os.environ.get("LINGZAO_API_KEY") or saved.get("api_key")
    base_url = (
        args.base_url
        or os.environ.get("LINGZAO_BASE_URL")
        or os.environ.get("LINGZAO_API_BASE_URL")
        or saved.get("base_url")
    )

    if not api_key:
        raise LingzaoError(
            "Missing Lingzao API key. Lingzao Skill can be installed for free, "
            "but public-content lookup, deep research, and image generation require "
            "online access and an API key. "
            "Open https://lingzao.atian.vip for tutorials on setup, Agent usage, and "
            "self-media workflows; when you need lookup access, get your API key, "
            "then run setup or set LINGZAO_API_KEY."
        )
    if not base_url:
        raise LingzaoError(
            "Missing Lingzao base URL. Open https://lingzao.atian.vip for the current "
            "web dashboard, tutorials, and API setup instructions, then run setup or "
            "set LINGZAO_BASE_URL."
        )

    return {"api_key": str(api_key).strip(), "base_url": str(base_url).strip().rstrip("/")}


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}


def is_uuid(value: Optional[str]) -> bool:
    if not value:
        return False
    try:
        return str(uuid.UUID(value)) == value.lower()
    except (ValueError, AttributeError):
        return False


def request_json(
    config: dict,
    method: str,
    path: str,
    body: Optional[Dict[str, Any]] = None,
    timeout: int = DEFAULT_TIMEOUT,
    headers: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    url = config["base_url"] + path
    data = None
    request_headers = {
        "accept": "application/json",
        "authorization": f"Bearer {config['api_key']}",
    }
    if headers:
        request_headers.update(headers)
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        request_headers["content-type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=request_headers, method=method)
    try:
        record_timeout_probe(method, path, timeout)
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return parse_json_response(response.read())
    except urllib.error.HTTPError as error:
        payload = parse_json_response(error.read())
        raise build_lingzao_api_error(error.code, payload) from error
    except urllib.error.URLError as error:
        raise LingzaoError(f"Lingzao API network error: {error.reason}") from error
    except (TimeoutError, socket.timeout) as error:
        raise LingzaoError("Lingzao API request timed out.") from error
    except (OSError, http.client.HTTPException) as error:
        raise LingzaoError(f"Lingzao API network error: {error}") from error


def request_multipart(
    config: dict,
    method: str,
    path: str,
    fields: Dict[str, Any],
    image_paths: List[str],
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    boundary = f"----LingzaoSkill{uuid.uuid4().hex}"
    data = encode_multipart_body(boundary, fields, image_paths)
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {config['api_key']}",
        "content-type": f"multipart/form-data; boundary={boundary}",
    }
    request = urllib.request.Request(config["base_url"] + path, data=data, headers=headers, method=method)
    try:
        record_timeout_probe(method, path, timeout)
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return parse_json_response(response.read())
    except urllib.error.HTTPError as error:
        payload = parse_json_response(error.read())
        raise build_lingzao_api_error(error.code, payload) from error
    except urllib.error.URLError as error:
        raise LingzaoError(f"Lingzao API network error: {error.reason}") from error
    except (TimeoutError, socket.timeout) as error:
        raise LingzaoError("Lingzao API request timed out.") from error
    except (OSError, http.client.HTTPException) as error:
        raise LingzaoError(f"Lingzao API network error: {error}") from error


def submit_generate_image_batch(
    config: dict,
    body: Dict[str, Any],
    image_paths: List[str],
    timeout: int,
) -> Dict[str, Any]:
    if image_paths:
        return request_multipart(
            config,
            "POST",
            "/api/v1/research/generate-image",
            body,
            image_paths,
            timeout=timeout,
        )
    return request_json(
        config,
        "POST",
        "/api/v1/research/generate-image",
        body,
        timeout=timeout,
    )


def wait_for_generate_image_batch(config: dict, payload: dict, timeout: int = DEFAULT_TIMEOUT) -> dict:
    data = as_dict(payload.get("data"))
    batch_id = data.get("batch_id")
    if not isinstance(batch_id, str) or not batch_id:
        return payload

    per_image_timeout = max(generate_image_poll_timeout(), timeout)
    batch_get_timeout = generate_image_batch_get_timeout(per_image_timeout)
    requested_count = max(1, generate_image_progress_signature(data)[0])
    total_timeout = generate_image_total_poll_timeout(per_image_timeout, requested_count)
    deadline = time.time() + total_timeout
    current = payload
    last_progress: Optional[tuple[int, int, int, int]] = None
    while True:
        current_data = as_dict(current.get("data"))
        status = str(current_data.get("status") or "").lower()
        pending_count = to_positive_int(current_data.get("pending_count")) or 0
        if status in {"completed", "failed"} or (status == "partial" and pending_count == 0):
            return current

        blocked_codes = non_retryable_generate_image_pending_errors(current_data)
        if blocked_codes:
            if first_generated_image(current):
                return current
            raise LingzaoError("；".join(public_error_label(code) for code in blocked_codes))

        progress = generate_image_progress_signature(current_data)
        if progress != last_progress:
            safe_print(format_generate_image_progress(progress), file=sys.stderr)
            last_progress = progress

        remaining = deadline - time.time()
        if remaining <= 0:
            if first_generated_image(current):
                return current
            raise LingzaoError(generate_image_timeout_message(batch_id, total_timeout, current_data))
        time.sleep(min(1.0, max(0.2, remaining)))
        remaining = deadline - time.time()
        if remaining <= 0:
            if first_generated_image(current):
                return current
            raise LingzaoError(generate_image_timeout_message(batch_id, total_timeout, current_data))
        try:
            current = request_json(
                config,
                "GET",
                f"/api/v1/research/generate-image/batches/{batch_id}",
                timeout=batch_get_timeout,
            )
        except LingzaoError as error:
            if is_lingzao_request_timeout(error) and first_generated_image(current):
                return current
            raise


def is_generate_image_batch_terminal(payload: dict) -> bool:
    data = as_dict(payload.get("data"))
    status = str(data.get("status") or "").lower()
    pending_count = to_non_negative_int(data.get("pending_count"))
    return status in {"completed", "failed"} or (status == "partial" and pending_count == 0)


def generate_image_poll_timeout() -> int:
    override = os.environ.get("LINGZAO_TEST_GENERATE_IMAGE_POLL_TIMEOUT")
    if override:
        try:
            parsed = int(override)
            if parsed > 0:
                return parsed
        except ValueError:
            pass
    return GENERATE_IMAGE_POLL_TIMEOUT


def generate_image_batch_get_timeout(per_image_timeout: int) -> int:
    return per_image_timeout + generate_image_download_timeout_buffer()


def generate_image_total_poll_timeout(per_image_timeout: int, requested_count: int) -> int:
    per_image_worker_timeout = per_image_timeout + generate_image_download_timeout_buffer()
    return per_image_worker_timeout * max(1, requested_count)


def generate_image_download_timeout_buffer() -> int:
    override = os.environ.get("LINGZAO_TEST_GENERATE_IMAGE_DOWNLOAD_TIMEOUT_BUFFER")
    if override is not None:
        try:
            parsed = int(override)
            if parsed >= 0:
                return parsed
        except ValueError:
            pass
    return GENERATE_IMAGE_DOWNLOAD_TIMEOUT_BUFFER


def active_generate_image_batch_payload_from_error(error: LingzaoApiError, requested_count: int) -> Optional[dict]:
    if error.code != "GENERATION_IN_PROGRESS":
        return None

    error_payload = as_dict(as_dict(error.payload).get("error"))
    batch_id = first_non_empty_str(error_payload.get("active_batch_id"), error_payload.get("batch_id"))
    if not batch_id:
        return None

    status = first_non_empty_str(error_payload.get("status")) or "queued"
    poll_url = first_non_empty_str(error_payload.get("poll_url")) or f"/api/v1/research/generate-image/batches/{batch_id}"
    poll_interval = to_positive_int(error_payload.get("recommended_poll_interval_seconds"))
    expires_at = first_non_empty_str(error_payload.get("expires_at"))
    active_count = to_positive_int(error_payload.get("requested_count")) or requested_count
    count = max(1, active_count)

    return {
        "ok": True,
        "request_id": batch_id,
        "cost_credits": 0,
        "data": compact({
            "type": "generate-image",
            "mode": "async",
            "batch_id": batch_id,
            "poll_url": poll_url,
            "recommended_poll_interval_seconds": poll_interval,
            "status": status,
            "expires_at": expires_at,
            "requested_count": count,
            "succeeded_count": 0,
            "failed_count": 0,
            "pending_count": count,
            "images": [{"index": index, "status": status} for index in range(count)],
        }),
    }


def is_lingzao_request_timeout(error: LingzaoError) -> bool:
    return str(error) == "Lingzao API request timed out."


def should_show_generate_image_recovery_hint(error: LingzaoError) -> bool:
    message = str(error)
    return (
        "Lingzao API network error:" in message
        or is_lingzao_request_timeout(error)
        or (isinstance(error, LingzaoApiError) and (error.status_code or 0) >= 500)
        or message in {
            "Lingzao API returned invalid JSON.",
            "Lingzao API returned unexpected JSON.",
        }
        or (message.startswith("Image batch ") and " did not finish within " in message)
    )


def generate_image_timeout_message(batch_id: str, total_timeout: int, data: dict) -> str:
    errors = generate_image_item_error_summaries(data)
    suffix = f" ({', '.join(errors)})" if errors else ""
    return f"Image batch {batch_id} did not finish within {total_timeout} seconds{suffix}."


def public_error_label(code: Any) -> str:
    if not isinstance(code, str) or not code:
        return ""
    return PUBLIC_SERVICE_ERROR_LABELS.get(code, code)


def public_error_message(code: Optional[str], message: str) -> str:
    if code in PUBLIC_SERVICE_ERROR_LABELS:
        return PUBLIC_SERVICE_ERROR_LABELS[code]
    return message


def record_timeout_probe(method: str, path: str, timeout: int) -> None:
    probe_path = os.environ.get("LINGZAO_TEST_TIMEOUT_PROBE")
    if not probe_path:
        return
    try:
        with open(probe_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps({"method": method, "path": path, "timeout": timeout}, ensure_ascii=False) + "\n")
    except OSError:
        pass


def ensure_generate_image_success(payload: dict) -> None:
    data = as_dict(payload.get("data"))
    if data.get("type") != "generate-image" or first_generated_image(payload):
        return

    status = str(data.get("status") or "").strip().lower()
    pending = to_non_negative_int(data.get("pending_count"))
    terminal = status in {"completed", "failed"} or (status == "partial" and pending == 0)
    if not terminal:
        return

    errors = generate_image_item_error_summaries(data)
    suffix = f" ({', '.join(errors)})" if errors else ""
    raise LingzaoError(f"Image generation failed: no successful image was produced{suffix}.")


def non_retryable_generate_image_pending_errors(data: dict) -> List[str]:
    codes: List[str] = []
    for item in as_list(data.get("images")):
        record = as_dict(item)
        status = str(record.get("status") or "").strip().lower()
        error_code = record.get("error_code")
        if status not in {"queued", "running"} or error_code != "INSUFFICIENT_CREDITS":
            continue
        if error_code not in codes:
            codes.append(error_code)
    return codes


def generate_image_item_error_summaries(data: dict) -> List[str]:
    errors: List[str] = []
    for item in as_list(data.get("images")):
        record = as_dict(item)
        error_code = record.get("error_code")
        error_id = record.get("error_id")
        parts: List[str] = []
        if isinstance(error_code, str) and error_code:
            parts.append(public_error_label(error_code))
        if isinstance(error_id, str) and error_id:
            parts.append(f"error_id={error_id}")
        if not parts:
            continue
        summary = " ".join(parts)
        if summary not in errors:
            errors.append(summary)
    return errors


def generate_image_progress_signature(data: dict) -> tuple[int, int, int, int]:
    requested = to_non_negative_int(data.get("requested_count"))
    succeeded = to_non_negative_int(data.get("succeeded_count"))
    failed = to_non_negative_int(data.get("failed_count"))
    pending = to_non_negative_int(data.get("pending_count"))
    if requested <= 0:
        requested = max(1, succeeded + failed + pending)
    return (requested, succeeded, failed, pending)


def format_generate_image_progress(progress: tuple[int, int, int, int]) -> str:
    requested, succeeded, failed, pending = progress
    message = f"正在等待图片生成：{succeeded}/{requested} 已完成，{pending} 张仍在生成中"
    if failed > 0:
        message += f"，{failed} 张失败"
    return message + "..."


def encode_multipart_body(boundary: str, fields: Dict[str, Any], image_paths: List[str]) -> bytes:
    chunks: List[bytes] = []
    for key, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8"),
                f"{value}\r\n".encode("utf-8"),
            ]
        )

    for image_path in image_paths:
        path = Path(image_path).expanduser()
        if not path.is_file():
            raise LingzaoError(f"Reference image not found: {path}")
        mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if mime_type not in {"image/png", "image/jpeg", "image/webp"}:
            raise LingzaoError("Reference images must be png, jpeg, or webp files.")
        try:
            image_bytes = path.read_bytes()
        except OSError as error:
            raise LingzaoError(f"Reference image could not be read: {path}") from error
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                (
                    'Content-Disposition: form-data; name="image"; '
                    f'filename="{escape_multipart_header(path.name)}"\r\n'
                ).encode("utf-8"),
                f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"),
                image_bytes,
                b"\r\n",
            ]
        )

    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks)


def escape_multipart_header(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\r", "").replace("\n", "")


def parse_json_response(raw: bytes) -> dict:
    if not raw:
        return {}
    try:
        value = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as error:
        raise LingzaoError("Lingzao API returned invalid JSON.") from error
    if not isinstance(value, dict):
        raise LingzaoError("Lingzao API returned unexpected JSON.")
    return value


def extract_error_message(payload: dict) -> Optional[str]:
    error = payload.get("error")
    if isinstance(error, dict) and isinstance(error.get("message"), str):
        return error["message"]
    if isinstance(payload.get("message"), str):
        return payload["message"]
    return None


def extract_error_code(payload: dict) -> Optional[str]:
    error = payload.get("error")
    if isinstance(error, dict) and isinstance(error.get("code"), str):
        return error["code"]
    if isinstance(payload.get("code"), str):
        return payload["code"]
    return None


def extract_error_id(payload: dict) -> Optional[str]:
    error = payload.get("error")
    if isinstance(error, dict) and isinstance(error.get("error_id"), str):
        return error["error_id"]
    if isinstance(payload.get("error_id"), str):
        return payload["error_id"]
    return None


def extract_error_object(payload: dict) -> dict:
    error = payload.get("error")
    return error if isinstance(error, dict) else {}


def format_error_value(value: Any) -> Optional[str]:
    if isinstance(value, str) and value:
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        items = [item for item in value if isinstance(item, str) and item]
        return ",".join(items) if items else None
    return None


def compact_error_json(value: Any, max_length: int = 180) -> Optional[str]:
    if not isinstance(value, (dict, list, str, int, float, bool)):
        return None
    text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return text if len(text) <= max_length else f"{text[:max_length]}..."


def first_error_example(error: dict, key: str) -> Optional[str]:
    examples = error.get("examples")
    if not isinstance(examples, dict):
        return None
    values = examples.get(key)
    if not isinstance(values, list) or not values:
        return None
    first = values[0]
    if not isinstance(first, dict):
        return compact_error_json(first)
    description = first.get("description")
    request = first.get("request")
    shape = first.get("shape")
    parts = []
    if isinstance(description, str) and description:
        parts.append(description)
    compact_request = compact_error_json(request or shape)
    if compact_request:
        parts.append(compact_request)
    return " ".join(parts) if parts else None


def build_error_guidance(error: dict) -> str:
    fields = [
        ("agent_action", error.get("agent_action")),
        ("detected_input", error.get("detected_input")),
        ("expected_input", error.get("expected_input")),
        ("suggested_capabilities", error.get("suggested_capabilities")),
        ("retryable", error.get("retryable")),
    ]
    parts = []
    for label, value in fields:
        formatted = format_error_value(value)
        if formatted:
            parts.append(f"{label}={formatted}")
    valid_example = first_error_example(error, "valid_inputs")
    if valid_example:
        parts.append(f"valid_example={valid_example}")
    invalid_example = first_error_example(error, "invalid_inputs")
    if invalid_example:
        parts.append(f"invalid_example={invalid_example}")
    failed_items = render_video_copy_error_items(error)
    if failed_items:
        parts.append(f"failed_items={failed_items}")
    if error.get("billing_effect") == "no_charge":
        parts.append("本次未扣费")
    return f" ({'; '.join(parts)})" if parts else ""


def render_video_copy_error_items(error: dict) -> str:
    rendered = []
    for index, value in enumerate(as_list(error.get("items")), start=1):
        item = as_dict(value)
        if item.get("status") != "failed":
            continue
        details = [
            f"item {index}",
            f"url={item.get('origin_url')}" if item.get("origin_url") else None,
            f"error={public_error_label(item.get('error_code')) or item.get('error_code') or '-'}",
        ]
        details.extend(line.removeprefix("- ") for line in render_video_copy_item_guidance(item))
        rendered.append(", ".join(detail for detail in details if detail))
    return " | ".join(rendered)


def build_lingzao_api_error(status_code: int, payload: dict) -> LingzaoApiError:
    code = extract_error_code(payload)
    message = public_error_message(code, extract_error_message(payload) or f"HTTP {status_code}")
    code_label = f" [{public_error_label(code)}]" if code and code not in PUBLIC_SERVICE_ERROR_LABELS else ""
    error_id = extract_error_id(payload)
    error_id_label = f" error_id={error_id}" if error_id else ""
    guidance = build_error_guidance(extract_error_object(payload))
    return LingzaoApiError(
        f"Lingzao API error{code_label}{error_id_label}: {message}{guidance}",
        status_code=status_code,
        code=code,
        error_id=error_id,
        payload=payload,
    )


def first_non_empty_str(*values: Any) -> Optional[str]:
    for value in values:
        if isinstance(value, str) and value:
            return value
    return None


def compact(value: Dict[str, Any]) -> Dict[str, Any]:
    return {key: item for key, item in value.items() if item is not None}


def preflight_article_output_path(output_path: str) -> None:
    target = Path(output_path).expanduser()
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise LingzaoError(f"Failed to prepare article output path: {target.parent}: {error}") from error

    if target.exists() and target.is_dir():
        raise LingzaoError(f"Article output path points to a directory: {target}")

    try:
        with target.open("ab"):
            pass
    except OSError as error:
        raise LingzaoError(f"Article output path is not writable: {target}: {error}") from error


def write_article_markdown(payload: dict, output_path: str) -> str:
    document = article_markdown_document(payload)
    target = Path(output_path).expanduser()
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise LingzaoError(f"Failed to prepare article output path: {target.parent}: {error}") from error

    try:
        target.write_text(document, encoding="utf-8")
    except OSError as error:
        raise LingzaoError(f"Failed to write article output: {target}: {error}") from error
    return str(target.resolve())


def article_markdown_document(payload: dict) -> str:
    data = as_dict(payload.get("data"))
    article = as_dict(data.get("article"))
    title = str(article.get("title") or "未命名文章")
    content = str(article.get("content_text") or "").strip()
    lines = [
        f"# {title}",
        "",
        f"- 链接: {article.get('url') or '-'}",
        f"- 公众号: {article.get('account_name') or '-'}",
        f"- 作者: {article.get('author') or '-'}",
        f"- 发布时间: {article.get('published_at') or '-'}",
        f"- 封面: {article.get('cover_url') or '-'}",
        f"- 摘要: {article.get('digest') or '-'}",
        "",
        "## 正文",
        "",
        content or "未返回正文文本。",
    ]
    return "\n".join(lines).strip() + "\n"


def write_generated_images(payload: dict, output_path: str) -> List[str]:
    records = generated_image_records(payload)
    if not records:
        raise LingzaoError("Lingzao API returned no generated image data.")

    target = Path(output_path).expanduser()
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise LingzaoError(f"Failed to prepare generated image output path: {target.parent}: {error}") from error

    written_paths: List[str] = []
    for record in records:
        image = as_dict(record.get("image"))
        image_bytes = decode_generated_image(image)
        image_target = generated_image_output_path(
            target,
            image,
            to_non_negative_int(record.get("index")),
            max(1, to_non_negative_int(record.get("total"))),
        )
        try:
            image_target.write_bytes(image_bytes)
        except OSError as error:
            raise LingzaoError(f"Failed to write generated image output: {image_target}: {error}") from error
        written_paths.append(str(image_target))
    return written_paths


def write_generated_image(payload: dict, output_path: str) -> str:
    paths = write_generated_images(payload, output_path)
    if not paths:
        raise LingzaoError("Lingzao API returned no generated image data.")
    return paths[0]


def decode_generated_image(image: dict) -> bytes:
    b64_json = image.get("b64_json")
    if not isinstance(b64_json, str) or not b64_json.strip():
        raise LingzaoError("Lingzao API returned no generated image data.")

    try:
        return base64.b64decode(b64_json, validate=True)
    except ValueError as error:
        raise LingzaoError("Lingzao API returned invalid image base64.") from error


def generated_image_output_path(target: Path, image: dict, index: int, total: int) -> Path:
    if total == 1:
        return target
    suffix = target.suffix or generated_image_extension(image)
    stem = target.stem if target.suffix else target.name
    return target.with_name(f"{stem}-{index + 1}{suffix}")


def generated_image_extension(image: dict) -> str:
    mime_type = image.get("mime_type")
    if isinstance(mime_type, str):
        if mime_type == "image/jpeg":
            return ".jpg"
        extension = mimetypes.guess_extension(mime_type)
        if extension:
            return extension
    return ".png"


def generated_images(payload: dict) -> List[dict]:
    return [as_dict(record.get("image")) for record in generated_image_records(payload)]


def generated_image_records(payload: dict) -> List[dict]:
    data = as_dict(payload.get("data"))
    items = as_list(data.get("images"))
    requested_count = to_non_negative_int(data.get("requested_count"))
    total = max(requested_count, len(items), 1)
    records: List[dict] = []
    for fallback_index, item in enumerate(items):
        record = as_dict(item)
        image = as_dict(record.get("image"))
        if image:
            item_index = to_optional_non_negative_int(record.get("index"))
            records.append({
                "image": image,
                "index": item_index if item_index is not None else fallback_index,
                "total": total,
            })
    if records:
        return records

    image = as_dict(data.get("image"))
    if image:
        return [{"image": image, "index": 0, "total": max(requested_count, 1)}]
    return []


def first_generated_image(payload: dict) -> dict:
    data = as_dict(payload.get("data"))
    image = as_dict(data.get("image"))
    if image:
        return image
    for item in as_list(data.get("images")):
        record = as_dict(item)
        image = as_dict(record.get("image"))
        if image:
            return image
    return {}


def to_markdown(command: str, payload: dict) -> str:
    if command in {"search-products", "get-product-detail", "get-product-reviews"}:
        data = payload.get("data", {})
        lines = [f"本次工具费用：{payload.get('cost_credits', 0)} 积分；价格单位：人民币元。"]
        if data.get("review_overview", {}).get("status") == "unavailable":
            lines.append("商品详情已读取；评分统计暂不可用，本次仍收取30积分。")
        lines.append(json.dumps(data, ensure_ascii=False, indent=2))
        lines.append("缺少销量表示未知，带 + 的销量是下限；评价时间原样展示，不含年份。")
        return "\n\n".join(lines)

    if command == "doctor":
        return render_doctor(payload)
    rendered = None
    if command == "search-notes":
        rendered = render_search_notes(payload)
    elif command == "search-users":
        rendered = render_search_users(payload)
    elif command == "get-user-info":
        rendered = render_user_info(payload)
    elif command == "get-user-posted-notes":
        rendered = render_user_posted_notes(payload)
    elif command == "analyze-user-profile":
        rendered = render_analyze_user_profile(payload)
    elif command == "get-note-detail":
        rendered = render_note(payload)
    elif command == "get-note-comments":
        rendered = render_note_comments(payload)
    elif command == "get-article-detail":
        rendered = render_article_detail(payload)
    elif command == "get-article-stats":
        rendered = render_article_stats(payload)
    elif command == "get-related-articles":
        rendered = render_related_articles(payload)
    elif command == "extract-video-copy":
        rendered = render_extract_video_copy(payload)
    elif command == "generate-image":
        rendered = render_generate_image(payload)
    else:
        return "```json\n" + json.dumps(payload, ensure_ascii=False, indent=2) + "\n```"

    footer = render_time_saved_footer(command, payload)
    if footer:
        return f"{rendered}\n\n{footer}"
    return rendered


def render_time_saved_footer(command: str, payload: dict) -> Optional[str]:
    if payload.get("ok") is not True:
        return None

    minutes = estimate_time_saved_minutes(command, payload)
    if minutes is None or minutes <= 0:
        return None
    return f"本次灵造调用预计节省约 {minutes} 分钟手动搜索与整理时间。"


def estimate_time_saved_minutes(command: str, payload: dict) -> Optional[int]:
    if command in FIXED_TIME_SAVED_MINUTES:
        return FIXED_TIME_SAVED_MINUTES[command]
    if command == "analyze-user-profile":
        data = as_dict(payload.get("data"))
        page = as_dict(data.get("page"))
        limit = to_positive_int(page.get("limit"))
        if limit is None:
            limit = to_positive_int(page.get("returned_count"))
        if limit is None:
            limit = len(as_list(data.get("items"))) or 20
        return 60 if limit <= 20 else 100
    if command == "extract-video-copy":
        data = as_dict(payload.get("data"))
        total = 0
        for item in as_list(data.get("items")):
            record = as_dict(item)
            status = str(record.get("status") or "").strip().lower()
            if status and status != "success":
                continue
            if not status and not record.get("content"):
                continue
            seconds = to_positive_int(record.get("duration_seconds")) or 0
            video_minutes = (seconds + 59) // 60
            total += max(8, video_minutes * 6)
        return total or None
    return None


def to_positive_int(value: Any) -> Optional[int]:
    if isinstance(value, bool):
        return None
    if isinstance(value, int) and value > 0:
        return value
    if isinstance(value, float) and value > 0:
        return int(value)
    if isinstance(value, str):
        try:
            parsed = int(float(value))
        except ValueError:
            return None
        return parsed if parsed > 0 else None
    return None


def to_non_negative_int(value: Any) -> int:
    if isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return max(0, value)
    if isinstance(value, float):
        return max(0, int(value))
    if isinstance(value, str):
        try:
            return max(0, int(float(value)))
        except ValueError:
            return 0
    return 0


def to_optional_non_negative_int(value: Any) -> Optional[int]:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value >= 0 else None
    if isinstance(value, float):
        parsed = int(value)
        return parsed if parsed >= 0 else None
    if isinstance(value, str):
        try:
            parsed = int(float(value))
        except ValueError:
            return None
        return parsed if parsed >= 0 else None
    return None


def render_doctor(payload: dict) -> str:
    user = as_dict(payload.get("user"))
    api_key = as_dict(payload.get("api_key"))
    return "\n".join(
        [
            "# Lingzao 连接检查",
            "",
            f"- 状态: {'正常' if payload.get('ok') else '异常'}",
            f"- API Key: {api_key.get('key_prefix', '-')}",
            f"- 用户: {render_user_identity(user)}",
        ]
    )


def render_search_notes(payload: dict) -> str:
    data = as_dict(payload.get("data"))
    items = as_list(data.get("items"))
    page = as_dict(data.get("page"))
    platform = str(data.get("platform") or "").lower()
    lines = [
        f"# {platform_label(data)}关键词线索：{data.get('query') or '-'}",
        "",
        f"- 下一页 Cursor: {page.get('next_cursor') or '-'}",
        "",
    ]
    for index, item in enumerate(items, start=1):
        note = as_dict(item)
        lines.extend(render_note_item(index, note, include_content_id=platform == "wechat_channels"))
    if not items:
        lines.append("未返回公开内容线索。")
    lines.extend(render_opaque_page(data))
    return "\n".join(lines).strip()


def render_search_users(payload: dict) -> str:
    data = as_dict(payload.get("data"))
    users = as_list(data.get("users"))
    page = as_dict(data.get("page"))
    platform = str(data.get("platform") or "").lower()
    lines = [
        f"# {platform_label(data)}创作者搜索：{data.get('query') or '-'}",
        "",
        f"- 下一页 Cursor: {page.get('next_cursor') or '-'}",
        "",
    ]
    for index, item in enumerate(users, start=1):
        profile = as_dict(item)
        stats = as_dict(profile.get("stats"))
        red_id = profile.get("red_id") or profile.get("redId")
        handle = profile.get("handle")
        bio = profile.get("bio") or profile.get("bio_preview")
        item_lines = [
            f"### {index}. {profile.get('name') or profile.get('id') or '-'}",
            f"- 用户ID: {profile.get('id') or '-'}",
            f"- 主页链接: {profile_public_url(platform, profile)}",
        ]
        if red_id:
            item_lines.append(f"- RED ID: {red_id}")
        if handle:
            item_lines.append(f"- Handle: {handle}")
        item_lines.extend([
            f"- 简介: {bio or '-'}",
            f"- 粉丝: {value_or_dash(stats.get('fans'))}",
            f"- 获赞: {value_or_dash(stats.get('liked'))}",
        ])
        lines.extend(item_lines)
        lines.append("")
    if not users:
        lines.append("未返回公开创作者候选。")
    lines.extend(render_opaque_page(data))
    return "\n".join(lines).strip()


def render_user_info(payload: dict) -> str:
    data = as_dict(payload.get("data"))
    profile = as_dict(data.get("profile"))
    stats = as_dict(profile.get("stats"))
    platform = str(data.get("platform") or "").lower()
    bio = profile.get("bio") or profile.get("bio_preview")
    lines = [
        f"# {platform_label(data)}主页资料：{profile.get('name') or profile.get('id') or '-'}",
        "",
        f"- 主页链接: {profile_public_url(platform, profile)}",
        f"- 简介: {bio or '-'}",
        f"- 粉丝: {value_or_dash(stats.get('fans'))}",
        f"- 获赞: {value_or_dash(stats.get('liked'))}",
        f"- 收藏: {value_or_dash(stats.get('collected'))}",
    ]
    return "\n".join(lines).strip()


def render_user_posted_notes(payload: dict) -> str:
    data = as_dict(payload.get("data"))
    notes = as_list(data.get("items"))
    page = as_dict(data.get("page"))
    platform = str(data.get("platform") or "").lower()
    lines = [
        f"# {platform_label(data)}主页近期公开内容",
        "",
        f"- 下一页 Cursor: {page.get('next_cursor') or '-'}",
        "",
        "## 近期笔记",
    ]
    if data.get("notice") == "limit_clamped":
        lines[2:2] = [f"- 提示（limit_clamped）: {data.get('notice_message') or '每次最多返回 20 条，更多请原样传 next_cursor。'}"]
    for index, item in enumerate(notes, start=1):
        lines.extend(
            render_note_item(
                index,
                as_dict(item),
                include_content_id=platform == "wechat_channels",
            )
        )
    if not notes:
        lines.append("未返回近期公开笔记。")
    lines.extend(render_opaque_page(data))
    if platform == "douyin":
        followup = (
            "如需继续查看主页作品结构、商业信号、内容热词和相似创作者，可继续请求 analyze-user-profile；"
            "如需抖音单条视频口播文案，使用 extract-video-copy；我不会自动调用。"
        )
    elif platform == "youtube":
        followup = "YouTube V1 不支持 analyze-user-profile；如需查看某条公开视频详情或评论，显式调用对应单条工具；我不会自动调用。"
    elif platform == "tiktok":
        followup = "TikTok V1 仅支持基础主页资料和近期公开内容；如需完整主页资料，可继续请求 get-user-info；我不会自动调用。"
    elif platform == "wechat_channels":
        followup = "视频号 V1 不支持 analyze-user-profile；如需完整主页资料，可继续请求 get-user-info；查看评论前先调用 get-note-detail 获取纯数字内容 ID；我不会自动调用。"
    else:
        followup = "如需继续查看主页作品正文、中文字幕、封面和商单/商品信号，可继续请求 analyze-user-profile；我不会自动调用。"
    lines.extend(
        [
            "",
            "基础主页分析通常不需要再调用 get-user-info；只有用户明确需要简介、粉丝数、关注数、总获赞、总收藏或总笔记数时才补充调用。",
            followup,
        ]
    )
    return "\n".join(lines).strip()


def render_note_comments(payload: dict) -> str:
    data = as_dict(payload.get("data"))
    comments = as_list(data.get("comments"))
    page = as_dict(data.get("page"))
    lines = [
        f"# {platform_label(data)}内容评论：{data.get('note_id') or '-'}",
        "",
        f"- 排序: {data.get('sort') or 'latest'}",
        f"- 返回: {page.get('returned_count', len(comments))}",
        f"- 总数: {page.get('total') if page.get('total') is not None else '-'}",
        f"- 还有下一页: {page.get('has_more', False)}",
        f"- 下一页 Cursor: {page.get('next_cursor') or '-'}",
        "",
    ]
    for index, item in enumerate(comments, start=1):
        comment = as_dict(item)
        author = as_dict(comment.get("author"))
        lines.extend(
            [
                f"### {index}. {author.get('name') or author.get('id') or '-'}",
                f"- 评论: {comment.get('text') or '-'}",
                f"- 点赞: {comment.get('liked_count', '-')}",
                f"- 回复数: {comment.get('reply_count', '-')}",
                f"- 时间: {comment.get('created_at') or '-'}",
                "",
            ]
        )
    if not comments:
        lines.append("未返回公开评论。")
    return "\n".join(lines).strip()


def render_analyze_user_profile(payload: dict) -> str:
    data = as_dict(payload.get("data"))
    user = as_dict(data.get("user"))
    page = as_dict(data.get("page"))
    items = as_list(data.get("items"))
    artifacts = as_dict(data.get("artifacts"))
    subtitle_markdown = as_dict(artifacts.get("subtitle_markdown"))
    lines = [
        f"# {platform_label(data)}深度主页数据：{user.get('nickname') or user.get('id') or '-'}",
        "",
        f"- 主页链接: {profile_public_url(str(data.get('platform') or '').lower(), user)}",
        f"- 返回: {page.get('returned_count', len(items))} / {page.get('limit', '-')}",
        f"- 下一页 Cursor: {page.get('next_cursor') or '-'}",
        "",
    ]
    if page.get("full_page") is True:
        lines.append("- 整页模式: 条数不固定，每页50积分；下一页原样传回 Cursor。")
    lines.extend(render_success_notice(payload))
    lines.extend(render_data_warnings(data))
    if subtitle_markdown.get("status") == "ready" and subtitle_markdown.get("url"):
        url = str(subtitle_markdown.get("url"))
        lines.extend(
            [
                "## 完整字幕 Markdown",
                "",
                "- 字段路径: data.artifacts.subtitle_markdown.url",
                "- 注意: 这是整个 analyze-user-profile 的顶层 artifact，不是 items[] 里的单条字幕链接。",
                f"- URL: {url}",
                "- 下载到临时文件后再做深度分析：",
                "",
                "```bash",
                f"curl -L {shell_quote(url)} -o /tmp/lingzao-profile-subtitles.md",
                "```",
                "",
            ]
        )
    elif subtitle_markdown.get("status") == "unsupported":
        lines.extend(
            [
                "## 主页字幕",
                "",
                "- 状态: unsupported",
                "- 当前平台主页解析不提取字幕；如需口播文案，请对具体视频使用 extract-video-copy。",
                "",
            ]
        )
    elif subtitle_markdown:
        lines.extend(
            [
                "## 完整字幕 Markdown",
                "",
                f"- 状态: {subtitle_markdown.get('status') or '-'}",
                "",
            ]
        )
    lines.extend(render_profile_insights(data))
    for index, item in enumerate(items, start=1):
        note = as_dict(item)
        metrics = as_dict(note.get("metrics"))
        media = as_dict(note.get("media"))
        text = as_dict(note.get("text"))
        subtitle = as_dict(text.get("subtitle"))
        monetization = as_dict(note.get("monetization"))
        collaboration = as_dict(monetization.get("collaboration"))
        commerce_note = as_dict(monetization.get("commerce_note"))
        plain_text = str(subtitle.get("plain_text_preview") or subtitle.get("plain_text") or "")
        preview = plain_text[:240] + ("..." if len(plain_text) > 240 else "")
        item_lines = [
            f"### {index}. {note.get('title') or note.get('id') or '未命名笔记'}",
            f"- 链接: {note.get('url') or '-'}",
            f"- 类型: {note.get('type') or '-'}",
            f"- 详情参数: xhs_note_type={note.get('xhs_note_type')}" if note.get("xhs_note_type") else "- 详情参数: -",
            f"- 指标: 点赞 {metrics.get('liked', 0)} / 收藏 {metrics.get('collected', 0)} / 评论 {metrics.get('commented', 0)} / 分享 {metrics.get('shared', 0)}",
            f"- 封面: {media.get('cover_large_url') or '-'}",
            f"- 时长: {media.get('video_duration_seconds') or '-'} 秒",
        ]
        if str(data.get("platform") or "").lower() == "douyin":
            item_lines.append("- 商业信号: 当前平台未提供")
        else:
            item_lines.append(
                f"- 商单: {collaboration.get('likely_collaboration', False)} / 商品笔记: {commerce_note.get('likely_goods_note', False)}"
            )
        item_lines.extend(
            [
                f"- 字幕: {subtitle.get('status') or '-'} / {subtitle.get('language') or '-'} / truncated={subtitle.get('truncated', False)}",
                f"- 摘要: {text.get('desc') or '-'}",
                f"- 字幕预览: {preview or '-'}",
                "",
            ]
        )
        lines.extend(item_lines)
    if not items:
        lines.append("未返回深度主页数据。")
    return "\n".join(lines).strip()


def render_success_notice(payload: dict) -> List[str]:
    message = str(payload.get("message") or "").strip()
    if payload.get("deduped") is True:
        message = "已复用近期同参结果；如需重新分析，请使用 --force-new。"
    if not message:
        return []
    message = message.replace("请传 force_new=true", "请使用 --force-new")
    return [f"> {message}", ""]


def render_data_warnings(data: dict) -> List[str]:
    warnings = as_list(data.get("warnings"))
    partial_data = data.get("partial_data") is True
    messages: List[str] = []
    for item in warnings:
        warning = as_dict(item)
        message = str(warning.get("message") or "").strip()
        if message:
            messages.append(message)
    if not messages and partial_data:
        messages.append("部分主页洞察暂不可用；不要把缺失洞察解读为没有数据。")
    if not messages:
        return []

    lines = ["## 数据提示", ""]
    for message in messages:
        lines.append(f"- {message}")
    lines.append("")
    return lines


def render_profile_insights(data: dict) -> List[str]:
    insights = as_dict(data.get("profile_insights"))
    if not insights:
        return []

    hot_keywords = as_dict(insights.get("content_hot_keywords"))
    hot_keyword_items = as_list(hot_keywords.get("items"))
    similar_creators = as_dict(insights.get("similar_creators"))
    similar_creator_items = as_list(similar_creators.get("items"))
    if not hot_keywords and not similar_creators:
        return []

    lines = ["## 主页洞察", ""]
    if hot_keywords:
        hot_keyword_status = str(hot_keywords.get("status") or "-")
        lines.append(f"- 内容热词: {hot_keyword_status} / {len(hot_keyword_items)}")
        if hot_keyword_status == "unavailable":
            lines.append("  - 暂不可用；主页作品数据仍可使用，不要解读为没有热词数据。")
        for item in hot_keyword_items[:8]:
            keyword = as_dict(item)
            details = [
                f"score={value_or_dash(keyword.get('score'))}",
                f"rank={value_or_dash(keyword.get('rank'))}",
                f"category={value_or_dash(keyword.get('category'))}",
            ]
            lines.append(f"  - {keyword.get('text') or '-'} ({', '.join(details)})")
        lines.append("")

    if similar_creators:
        similar_creator_status = str(similar_creators.get("status") or "-")
        lines.append(f"- 相似创作者: {similar_creator_status} / {len(similar_creator_items)}")
        if similar_creator_status == "unavailable":
            lines.append("  - 暂不可用；主页作品数据仍可使用，不要解读为没有相似创作者。")
        for item in similar_creator_items[:5]:
            creator = as_dict(item)
            tags = as_list(creator.get("tags"))
            reasons = as_list(creator.get("recommend_reasons"))
            lines.append(
                "  - "
                + f"{creator.get('name') or creator.get('id') or '-'}"
                + f" / 粉丝 {value_or_dash(creator.get('fans'))}"
                + f" / 预期播放 {value_or_dash(creator.get('expected_play_count'))}"
                + f" / 相似度 {value_or_dash(creator.get('similarity'))}"
                + f" / 标签 {', '.join(str(tag) for tag in tags) if tags else '-'}"
                + f" / 推荐原因 {', '.join(str(reason) for reason in reasons) if reasons else '-'}"
            )
        lines.append("")

    return lines


def value_or_dash(value: Any) -> str:
    if value is None or value == "":
        return "-"
    return str(value)


def shell_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def render_note(payload: dict) -> str:
    data = as_dict(payload.get("data"))
    note = as_dict(data.get("item"))
    platform = str(data.get("platform") or "").lower()
    include_body_images = (
        platform == "xhs"
        and str(note.get("xhs_note_type") or "").lower() == "image"
    )
    lines = [
        f"# {platform_label(data)}内容：{note.get('title') or note.get('id') or '-'}",
        "",
    ]
    lines.extend(
        render_note_item(
            1,
            note,
            include_index=False,
            include_content_id=platform == "wechat_channels",
            include_body_images=include_body_images,
        )
    )
    return "\n".join(lines).strip()


def render_article_detail(payload: dict) -> str:
    data = as_dict(payload.get("data"))
    article = as_dict(data.get("article"))
    title = article.get("title") or "未命名文章"
    local_article_output = payload.get("_local_article_output")
    if isinstance(local_article_output, str) and local_article_output:
        summary = article.get("digest") or article_text_preview(str(article.get("content_text") or ""), limit=240)
        lines = [
            f"# {platform_label(data)}文章：{title}",
            "",
            f"- 文件: {local_article_output}",
            f"- 摘要: {summary or '-'}",
        ]
        return "\n".join(lines).strip()

    lines = [
        f"# {platform_label(data)}文章：{title}",
        "",
        f"- 链接: {article.get('url') or '-'}",
        f"- 公众号: {article.get('account_name') or '-'}",
        f"- 作者: {article.get('author') or '-'}",
        f"- 发布时间: {article.get('published_at') or '-'}",
        f"- 封面: {article.get('cover_url') or '-'}",
        f"- 摘要: {article.get('digest') or '-'}",
        "",
        "## 正文预览",
        "",
        article_text_preview(str(article.get("content_text") or "")),
    ]
    return "\n".join(lines).strip()


def render_article_stats(payload: dict) -> str:
    data = as_dict(payload.get("data"))
    metrics = as_dict(data.get("metrics"))
    lines = [
        f"# {platform_label(data)}文章数据",
        "",
        f"- 链接: {data.get('article_url') or '-'}",
        f"- 阅读: {metrics.get('read_count', '-')}",
        f"- 点赞: {metrics.get('like_count', '-')}",
        f"- 在看: {metrics.get('wow_count', '-')}",
        f"- 分享: {metrics.get('share_count', '-')}",
        f"- 收藏: {metrics.get('collect_count', '-')}",
        f"- 评论: {metrics.get('comment_count', '-')}",
        f"- 星标: {metrics.get('star_count', '-')}",
    ]
    return "\n".join(lines).strip()


def render_related_articles(payload: dict) -> str:
    data = as_dict(payload.get("data"))
    page = as_dict(data.get("page"))
    articles = as_list(data.get("articles"))
    lines = [
        f"# {platform_label(data)}相关文章",
        "",
        f"- 原文链接: {data.get('article_url') or '-'}",
        f"- 返回: {page.get('returned_count', len(articles))}",
        f"- 总数: {page.get('total') if page.get('total') is not None else '-'}",
        "",
    ]
    for index, item in enumerate(articles, start=1):
        article = as_dict(item)
        lines.extend(
            [
                f"### {index}. {article.get('title') or '未命名文章'}",
                f"- 链接: {article.get('url') or '-'}",
                f"- 公众号: {article.get('account_name') or '-'}",
                f"- 发布时间: {article.get('published_at') or '-'}",
                f"- 摘要: {article.get('digest') or '-'}",
                "",
            ]
        )
    if not articles:
        lines.append("未返回相关文章。")
    return "\n".join(lines).strip()


def article_text_preview(value: str, limit: int = 1200) -> str:
    text = " ".join(value.split())
    if not text:
        return "未返回正文文本。"
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def render_extract_video_copy(payload: dict) -> str:
    data = as_dict(payload.get("data"))
    batch = as_dict(data.get("batch"))
    items = as_list(data.get("items"))
    lines = [
        "# 短视频文案提取",
        "",
        f"- Batch ID: {batch.get('batch_id', '-')}",
        f"- 成功: {batch.get('success_count', 0)} / {batch.get('total_count', len(items))}",
    ]
    if payload.get("replayed") is True:
        lines.extend(
            [
                "",
                "> 已重放同一文案提取请求的成功结果，本次新增费用为 0。继续重试请复用当前 --operation-id；明确发起新提取时请使用新的 operation ID。",
            ]
        )
    lines.append("")
    for index, item in enumerate(items, start=1):
        record = as_dict(item)
        error_code = record.get("error_code")
        error_code_label = public_error_label(error_code) or "-"
        error_message = public_error_message(error_code if isinstance(error_code, str) else None, str(record.get("message") or "-"))
        lines.extend(
            [
                f"### {index}. {record.get('title') or record.get('origin_url') or '-'}",
                f"- 平台: {record.get('platform') or '-'}",
                f"- 链接: {record.get('origin_url') or record.get('input_url') or '-'}",
                f"- 状态: {record.get('status') or '-'}",
                f"- 错误: {error_code_label} / {error_message}",
                *render_video_copy_item_guidance(record),
                f"- 时长: {record.get('duration_seconds') or '-'} 秒",
                "",
                str(record.get("content") or "未返回文案。"),
                "",
            ]
        )
        subtitle = as_dict(record.get("subtitle"))
        if subtitle.get("format") == "webvtt" and subtitle.get("content"):
            lines.extend(
                [
                    f"- 原声字幕: WebVTT / {subtitle.get('language') or '语言未知'} / 完整={subtitle.get('complete') is True}",
                    "",
                    "```webvtt",
                    str(subtitle["content"]),
                    "```",
                    "",
                ]
            )
    if not items:
        lines.append("未返回文案提取结果。")
    return "\n".join(lines).strip()


def render_video_copy_item_guidance(record: dict) -> List[str]:
    lines = []
    if isinstance(record.get("retryable"), bool):
        lines.append(f"- 是否重试: {'可以稍后重试' if record['retryable'] else '不要重试该链接'}")
    if record.get("billing_effect") == "no_charge":
        lines.append("- 结果: 该失败项未扣费")
    if record.get("agent_action") == "ask_user_for_shorter_video":
        lines.append("- 下一步: 请更换较短的视频链接")
    return lines


def render_generate_image(payload: dict) -> str:
    data = as_dict(payload.get("data"))
    image = first_generated_image(payload)
    local_output = payload.get("_local_output")
    local_outputs = [item for item in as_list(payload.get("_local_outputs")) if isinstance(item, str) and item]
    blocked_codes = non_retryable_generate_image_pending_errors(data)
    item_errors = generate_image_item_error_summaries(data)
    lines = [
        "# 图片生成结果",
        "",
        f"- Batch: {data.get('batch_id') or '-'}",
        f"- 状态: {data.get('status') or '-'}",
        f"- 数量: {data.get('succeeded_count', 0)} 成功 / {data.get('requested_count', 1)} 请求",
        f"- 尺寸: {data.get('size') or '-'}",
        f"- 格式: {data.get('output_format') or '-'}",
        f"- 参考图: {data.get('reference_image_count') if data.get('reference_image_count') is not None else 0}",
        f"- MIME: {image.get('mime_type') or '-'}",
        f"- SHA256: {image.get('sha256') or '-'}",
    ]
    if len(local_outputs) > 1:
        lines.append("- 文件:")
        lines.extend(f"  - {path}" for path in local_outputs)
    elif local_outputs:
        lines.append(f"- 文件: {local_outputs[0]}")
    elif local_output:
        lines.append(f"- 文件: {local_output}")
    else:
        lines.append("- 文件: 未保存；下次可加 `--output /tmp/lingzao-image.png`")
    if blocked_codes:
        lines.append(f"- 未完成: {', '.join(public_error_label(code) for code in blocked_codes)}")
    if item_errors:
        lines.append(f"- 错误: {', '.join(item_errors)}")
    lines.extend(
        [
            "",
            "## Agent 提示",
            "",
            "- CLI 会在请求前打印请求 ID。网络响应不确定或轮询中断时，保持原参数不变并添加 `--client-request-id <打印的 UUID>`，服务端会恢复同一个 Batch；新生成请省略该参数。",
            "- 同提示词需要多张图时，一次调用 `generate-image --count N`（N=2..5），不要循环多次 `--count 1`；需要不同概念时请改写 prompt。",
        ]
    )
    lines.append("")
    return "\n".join(lines).strip()


def render_version_check(payload: dict) -> str:
    local_version = payload.get("local_version") or "unknown"
    remote_version = payload.get("remote_version") or "unknown"
    if payload.get("update_available"):
        return "\n".join(
            [
                "# Lingzao Skill 更新可用",
                "",
                f"- 当前版本: {local_version}",
                f"- 最新版本: {remote_version}",
                "",
                "必须先更新到最新版本，再继续处理用户的灵造搜索、主页分析、字幕或文案提取请求。",
                "请告诉用户：灵造技能有新版本，我需要先更新后再继续。",
                "",
                "更新时执行：",
                "",
                "```bash",
                "npx skills add https://assets-tian.midao.site/skills/lingzao --skill lingzao -g --copy",
                "```",
                "",
                "更新会保留 ~/.lingzao/config.json 里的 API 配置，通常不需要重新设置 API key。",
                "",
                "如果更新后 ~/.lingzao/bin/lingzao 不存在或命令入口失效，再运行 setup.sh --skip-doctor 修复命令入口。",
            ]
        )
    if payload.get("ok"):
        return "\n".join(
            [
                "# Lingzao Skill 已是最新",
                "",
                f"- 当前版本: {local_version}",
            ]
        )
    return "\n".join(
        [
            "# Lingzao Skill 版本检查未完成",
            "",
            f"- 当前版本: {local_version}",
            "- 可以继续使用灵造技能。",
        ]
    )


def platform_label(data: dict) -> str:
    platform = str(data.get("platform") or "xhs").lower()
    if platform == "xhs":
        return "小红书"
    if platform == "douyin":
        return "抖音"
    if platform == "youtube":
        return "YouTube"
    if platform == "tiktok":
        return "TikTok"
    if platform == "instagram":
        return "Instagram"
    if platform == "wechat_channels":
        return "视频号"
    if platform == "wechat_mp":
        return "微信公众号"
    return platform


def render_note_item(
    index: int,
    note: dict,
    include_index: bool = True,
    include_content_id: bool = False,
    include_body_images: bool = False,
) -> List[str]:
    metrics = as_dict(note.get("metrics"))
    author = as_dict(note.get("author"))
    title_prefix = f"{index}. " if include_index else ""
    tags = as_list(note.get("tags"))
    lines = [
        f"### {title_prefix}{note.get('title') or note.get('id') or '未命名笔记'}",
        f"- 链接: {note.get('url') or '-'}",
        f"- 作者: {author.get('name') or author.get('id') or '-'}",
        f"- 类型: {note.get('content_type') or note.get('type') or '-'}",
    ]
    if include_content_id:
        lines.insert(1, f"- 内容 ID: {note.get('id') or '-'}")
    if note.get("xhs_note_type"):
        lines.append(f"- 详情参数: xhs_note_type={note.get('xhs_note_type')}")
    lines.extend(
        [
            f"- 指标: 点赞 {metrics.get('liked', 0)} / 收藏 {metrics.get('collected', 0)} / 评论 {metrics.get('commented', 0)} / 分享 {metrics.get('shared', 0)}",
            f"- 标签: {', '.join(str(tag) for tag in tags) if tags else '-'}",
            f"- 摘要: {note.get('summary') or '-'}",
        ]
    )
    if include_body_images:
        image_urls = note_body_image_urls(note)
        lines.extend(["", f"#### 正文图片（{len(image_urls)} 张）", ""])
        if image_urls:
            lines.extend(f"{image_index}. <{url}>" for image_index, url in enumerate(image_urls, start=1))
            lines.extend(["", "> 图片链接可能过期，请及时使用；灵造不下载、代理或长期保存这些图片。"])
        else:
            lines.append("无正文图片链接。")
    lines.append("")
    return lines


def note_body_image_urls(note: dict) -> List[str]:
    media = as_dict(note.get("media"))
    urls: List[str] = []
    seen = set()
    for item in as_list(media.get("images")):
        if isinstance(item, str):
            url = item.strip()
        else:
            image = as_dict(item)
            url = str(image.get("url") or "").strip()
        if not url or url in seen:
            continue
        seen.add(url)
        urls.append(url)
    return urls


def render_user_identity(user: dict) -> str:
    if user.get("name"):
        return str(user["name"])
    if user.get("email"):
        return mask_email(str(user["email"]))
    if user.get("id"):
        return str(user["id"])
    return "-"


def profile_public_url(platform: str, profile: dict) -> str:
    for key in ("url", "profile_url", "homepage_url", "share_url", "link"):
        value = profile.get(key)
        if not value:
            continue
        text = str(value)
        if text.startswith(("https://", "http://")):
            return text
    profile_id = profile.get("id") or profile.get("user_id") or profile.get("userid")
    if platform in {"xhs", "xiaohongshu", ""} and profile_id:
        return f"https://www.xiaohongshu.com/user/profile/{quote_path_segment(str(profile_id))}"
    if platform in {"douyin", "dy"} and profile_id:
        return f"https://www.douyin.com/user/{quote_path_segment(str(profile_id))}"
    if platform in {"youtube", "yt"} and profile_id:
        return f"https://www.youtube.com/channel/{quote_path_segment(str(profile_id))}"
    return "-"


def render_opaque_page(data: dict) -> List[str]:
    page = as_dict(data.get("page"))
    if not page:
        return []
    return [
        "",
        f"- 返回: {page.get('returned_count', '-')}",
        f"- 还有下一页: {page.get('has_more', False)}",
        f"- 下一页 Cursor: {page.get('next_cursor') or '-'}",
    ]


def quote_path_segment(value: str) -> str:
    return urllib.parse.quote(value, safe="")


def mask_email(value: str) -> str:
    if "@" not in value:
        return value[:2] + "***" if len(value) > 2 else "***"
    local, domain = value.split("@", 1)
    if not local:
        return "***@" + domain
    return local[:1] + "***@" + domain


def as_dict(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list:
    return value if isinstance(value, list) else []


if __name__ == "__main__":
    raise SystemExit(main())
