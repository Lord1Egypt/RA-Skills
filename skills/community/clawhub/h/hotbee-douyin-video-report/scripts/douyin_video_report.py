#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 HotBee 接口从抖音视频链接生成 HTML 拆解报告。"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import ipaddress
import json
import math
import mimetypes
import os
import re
import sys
import textwrap
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://www.smsz.xyz/prod-api"
COMMENT_PAGE_SIZE = 10
DEFAULT_COMMENT_PAGES = 3
MAX_COMMENT_LIMIT = 200
TRANSCRIPT_RETRY_DELAYS = [1.0, 2.2, 4.2]
VIDEO_INFO_VIP_RETRIES = 3
VIDEO_INFO_VIP_RETRY_DELAYS = [1.0, 2.0]
PLAY_COUNT_KEYS = ["play_count", "playCount", "play", "view_count", "viewCount"]
MAX_MEDIA_BYTES = 25 * 1024 * 1024
SENSITIVE_FIELD_NAMES = {
    "api-key",
    "api_key",
    "apikey",
    "authorization",
    "hotbee_douyin_key",
    "key",
    "password",
    "secret",
    "token",
    "access_token",
}


def now_slug() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sanitize_sensitive_data(payload), ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def redact_sensitive_text(value: Any, secret_values: list[str] | tuple[str, ...] = ()) -> str:
    text = str(value or "")
    for secret in secret_values:
        if secret and len(secret) >= 4:
            text = text.replace(secret, "[REDACTED]")
    return re.sub(
        r"(?i)([?&](?:api[-_]?key|access[-_]?token|authorization|key|password|secret|token)=)[^&#\s]+",
        r"\1[REDACTED]",
        text,
    )


def sanitize_sensitive_data(value: Any, secret_values: list[str] | tuple[str, ...] = ()) -> Any:
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if str(key).lower() in SENSITIVE_FIELD_NAMES else sanitize_sensitive_data(item, secret_values)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [sanitize_sensitive_data(item, secret_values) for item in value]
    if isinstance(value, tuple):
        return [sanitize_sensitive_data(item, secret_values) for item in value]
    if isinstance(value, str):
        return redact_sensitive_text(value, secret_values)
    return value


def redact_url_for_log(value: str) -> str:
    try:
        parsed = urllib.parse.urlsplit(value)
        if parsed.scheme and parsed.netloc:
            return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "[REDACTED]" if parsed.query else "", ""))
    except ValueError:
        pass
    return redact_sensitive_text(value)


def validate_base_url(value: str) -> str:
    text = str(value or "").strip().rstrip("/")
    try:
        parsed = urllib.parse.urlsplit(text)
    except ValueError as exc:
        raise ValueError("HotBee API Base URL 格式无效。") from exc
    if not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("HotBee API Base URL 不得包含账号、密码、查询参数或片段。")
    is_loopback = parsed.hostname == "localhost"
    try:
        is_loopback = is_loopback or ipaddress.ip_address(parsed.hostname).is_loopback
    except ValueError:
        pass
    if parsed.scheme != "https" and not (parsed.scheme == "http" and is_loopback):
        raise ValueError("HotBee API Base URL 必须使用 HTTPS；仅本机回环地址允许 HTTP。")
    return text


def hotbee_api_key() -> str:
    """Read the shared key first while keeping the former variable compatible."""
    return (os.environ.get("HOTBEE_API_KEY") or os.environ.get("HOTBEE_DOUYIN_KEY") or "").strip()


def is_allowed_media_url(value: str) -> bool:
    try:
        parsed = urllib.parse.urlsplit(value)
    except ValueError:
        return False
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        return False
    if parsed.hostname == "localhost" or parsed.hostname.endswith(".local"):
        return False
    try:
        return not (ipaddress.ip_address(parsed.hostname).is_private or ipaddress.ip_address(parsed.hostname).is_loopback)
    except ValueError:
        return True


def first_http_url(value: str) -> str:
    match = re.search(r"https?://[^\s\"'<>，。！？、；：）)】]+", value or "", re.I)
    return (match.group(0) if match else value).strip().rstrip("，。！？、；：）)】")


def normalize_remote_url(value: Any) -> str:
    url = str(value or "").strip()
    if not url or url == "[object Object]":
        return ""
    if url.startswith("//"):
        return f"https:{url}"
    if url.lower().startswith("http://"):
        return "https://" + url[7:]
    return url


def is_douyin_url(value: str) -> bool:
    return bool(re.search(r"douyin\.com|iesdouyin\.com", value or "", re.I))


def is_douyin_short_url(value: str) -> bool:
    return bool(re.search(r"v\.douyin\.com", value or "", re.I))


def is_standard_video_url(value: str) -> bool:
    return bool(re.search(r"douyin\.com/(?:share/)?video/\d+", value or "", re.I))


def collect_douyin_video_ids(value: str) -> list[str]:
    url = first_http_url(value)
    ids: list[str] = []
    seen: set[str] = set()

    def push(candidate: str | None) -> None:
        if not candidate:
            return
        text = candidate.strip()
        if re.fullmatch(r"\d+", text) and text not in seen:
            seen.add(text)
            ids.append(text)

    path_match = re.search(r"(?:douyin\.com|iesdouyin\.com)/(?:share/)?video/(\d+)", url, re.I)
    push(path_match.group(1) if path_match else None)

    try:
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        for key in ["modal_id", "aweme_id", "item_ids", "group_id", "vid"]:
            for item in params.get(key, []):
                push(item)
    except Exception:
        pass

    for match in re.finditer(r"[?&](?:modal_id|aweme_id|item_ids|group_id|vid)=(\d+)", url, re.I):
        push(match.group(1))

    return ids


def normalize_douyin_url(value: str) -> str:
    url = first_http_url(value)
    if not is_douyin_url(url):
        return url
    ids = collect_douyin_video_ids(url)
    if ids:
        return f"https://www.douyin.com/video/{ids[0]}"
    return url


def post_query(base_url: str, endpoint: str, params: dict[str, Any], timeout: int = 60) -> Any:
    clean_params = {key: value for key, value in params.items() if value is not None and value != ""}
    query = urllib.parse.urlencode(clean_params, doseq=True)
    url = f"{base_url.rstrip('/')}{endpoint}"
    if query:
        url = f"{url}?{query}"
    req = urllib.request.Request(
        url,
        data=b"",
        method="POST",
        headers={
            "Accept": "application/json,text/plain,*/*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 HotBee-Douyin-Video-Report/1.0",
        },
    )
    secret_values = [str(item) for key, item in clean_params.items() if key.lower() in SENSITIVE_FIELD_NAMES and item]
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
    except Exception as exc:
        raise RuntimeError(redact_sensitive_text(exc, secret_values)) from None
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {"code": response.status, "data": body}


def payload_ok(payload: Any) -> bool:
    return isinstance(payload, dict) and (payload.get("code") == 200 or payload.get("success") is True)


def api_error_message(payload: Any, fallback: str) -> str:
    if isinstance(payload, dict):
        for key in ["msg", "message", "error"]:
            value = str(payload.get(key) or "").strip()
            if value:
                return value
    return fallback


def collect_string_values(value: Any, depth: int = 0) -> list[str]:
    if depth > 5 or value is None:
        return []
    if isinstance(value, (str, int, float, bool)):
        return [str(value)]
    if isinstance(value, list):
        values: list[str] = []
        for item in value:
            values.extend(collect_string_values(item, depth + 1))
        return values
    if isinstance(value, dict):
        values = []
        for item in value.values():
            values.extend(collect_string_values(item, depth + 1))
        return values
    return []


def pick_resolved_douyin_url(payload: Any) -> str:
    for value in collect_string_values(payload):
        url = normalize_douyin_url(value)
        if is_standard_video_url(url):
            return url
    return ""


def resolve_douyin_url(raw_url: str, base_url: str, raw_dir: Path, warnings: list[str]) -> str:
    normalized = normalize_douyin_url(raw_url)
    if not is_douyin_short_url(normalized) or is_standard_video_url(normalized):
        return normalized

    try:
        req = urllib.request.Request(
            normalized,
            headers={"User-Agent": "Mozilla/5.0 HotBee-Douyin-Video-Report/1.0"},
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            resolved = normalize_douyin_url(response.geturl())
        if is_standard_video_url(resolved):
            return resolved
    except Exception as exc:
        warnings.append(f"抖音短链本地解析失败：{redact_sensitive_text(exc)}")

    try:
        payload = post_query(base_url, "/tool/douyin/Dy_convert_share_url", {"url": normalized}, timeout=10)
        write_json(raw_dir / "resolve_hotbee.json", payload)
        resolved = pick_resolved_douyin_url(payload)
        if resolved:
            return resolved
    except Exception as exc:
        warnings.append(f"HotBee 短链解析兜底失败：{redact_sensitive_text(exc)}")

    warnings.append("短链没有解析为标准抖音视频页，后续接口将直接尝试原链接。")
    return normalized


def to_number_or_text(value: Any) -> int | float | str:
    if isinstance(value, (int, float)) and math.isfinite(float(value)):
        return value
    text = str(value or "").strip()
    return text if text else "--"


def parse_metric(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value) if math.isfinite(float(value)) else 0.0
    raw = str(value or "").strip().replace(",", "")
    if not raw or raw == "--":
        return 0.0
    match = re.search(r"-?\d+(?:\.\d+)?", raw)
    if not match:
        return 0.0
    number = float(match.group(0))
    if re.search(r"[wW万]", raw):
        return number * 10000
    if re.search(r"[kK千]", raw):
        return number * 1000
    return number


def metric_has_value(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return math.isfinite(float(value)) and float(value) >= 0
    raw = str(value or "").strip()
    if not raw or raw == "--":
        return False
    return parse_metric(raw) > 0 or raw in {"0", "0.0"}


def metric_cache_value(value: Any) -> int | float | str:
    if isinstance(value, bool):
        return "--"
    if isinstance(value, (int, float)) and math.isfinite(float(value)):
        return int(value) if float(value).is_integer() else value
    return to_number_or_text(value)


def metric_key(value: Any) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value or "").lower())


def looks_like_metric_value(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return math.isfinite(float(value))
    raw = str(value or "").strip().replace(",", "")
    if not raw or raw == "--":
        return False
    return bool(re.fullmatch(r"\d+(?:\.\d+)?\s*(?:万|w|W|千|k|K)?(?:次|播放|观看|浏览|views?)?", raw, re.I))


def pick_metric_value(record: dict[str, Any], keys: list[str]) -> Any:
    normalized_keys = {metric_key(key) for key in keys}
    for key in keys:
        if key in record and looks_like_metric_value(record[key]):
            return record[key]
    for key, value in record.items():
        if metric_key(key) in normalized_keys and looks_like_metric_value(value):
            return value
    return None


def find_metric_value(value: Any, keys: list[str], depth: int = 0) -> Any:
    if depth > 7 or value is None:
        return None
    if isinstance(value, dict):
        direct = pick_metric_value(value, keys)
        if direct is not None:
            return direct
        priority_keys = ["statistics", "stats", "aweme_detail", "aweme", "item", "video", "data"]
        for key in priority_keys:
            if key in value:
                found = find_metric_value(value[key], keys, depth + 1)
                if found is not None:
                    return found
        for child_key, child in value.items():
            if child_key in priority_keys:
                continue
            found = find_metric_value(child, keys, depth + 1)
            if found is not None:
                return found
    if isinstance(value, list):
        for item in value:
            found = find_metric_value(item, keys, depth + 1)
            if found is not None:
                return found
    return None


def extract_play_count(payload: Any) -> int | float | str:
    value = find_metric_value(payload, PLAY_COUNT_KEYS)
    return metric_cache_value(value) if value is not None else "--"


def metric_source_from_endpoint(endpoint: str) -> str:
    return "vip" if endpoint.endswith("_VIP") else "regular"


def read_json_file(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def metrics_cache_path(output_root: Path) -> Path:
    return output_root / "_cache" / "douyin-video-metrics.json"


def video_identity_values(video: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for key in ["videoId", "resolvedUrl", "originalUrl", "inputUrl"]:
        text = str(video.get(key) or "").strip()
        if text:
            values.append(normalize_douyin_url(text) if is_douyin_url(text) else text)
    return values


def video_cache_keys(video: dict[str, Any]) -> list[str]:
    keys: list[str] = []
    seen: set[str] = set()
    for value in video_identity_values(video):
        if value and value != "--" and value not in seen:
            seen.add(value)
            keys.append(value)
    return keys


def primary_video_cache_key(video: dict[str, Any]) -> str:
    for key in video_cache_keys(video):
        if re.fullmatch(r"\d+", key):
            return key
    keys = video_cache_keys(video)
    return keys[0] if keys else ""


def same_video_identity(left: dict[str, Any], right: dict[str, Any]) -> bool:
    left_values = set(video_identity_values(left))
    right_values = set(video_identity_values(right))
    if left_values & right_values:
        return True
    left_ids: set[str] = set()
    right_ids: set[str] = set()
    for value in left_values:
        left_ids.update(collect_douyin_video_ids(value))
    for value in right_values:
        right_ids.update(collect_douyin_video_ids(value))
    return bool(left_ids and right_ids and left_ids & right_ids)


def parse_manifest_time(value: Any, fallback_path: Path) -> float:
    raw = str(value or "").strip()
    if raw:
        try:
            return dt.datetime.fromisoformat(raw).timestamp()
        except ValueError:
            pass
    try:
        return fallback_path.stat().st_mtime
    except OSError:
        return 0.0


def load_play_count_cache(output_root: Path) -> dict[str, Any]:
    payload = read_json_file(metrics_cache_path(output_root), {})
    return payload if isinstance(payload, dict) else {}


def save_play_count_cache(output_root: Path, cache: dict[str, Any]) -> None:
    write_json(metrics_cache_path(output_root), cache)


def cache_record_from_video(video: dict[str, Any], source: str, source_run_dir: Path | str, updated_at: str | None = None) -> dict[str, Any]:
    return {
        "videoId": str(video.get("videoId") or ""),
        "resolvedUrl": str(video.get("resolvedUrl") or video.get("originalUrl") or ""),
        "playCount": metric_cache_value(video.get("playCount")),
        "updatedAt": updated_at or dt.datetime.now().isoformat(timespec="seconds"),
        "source": source,
        "sourceRunDir": str(source_run_dir),
    }


def update_play_count_cache(output_root: Path, video: dict[str, Any], source: str, source_run_dir: Path | str, updated_at: str | None = None) -> None:
    if parse_metric(video.get("playCount")) <= 0:
        return
    key = primary_video_cache_key(video)
    if not key:
        return
    cache = load_play_count_cache(output_root)
    cache[key] = cache_record_from_video(video, source, source_run_dir, updated_at)
    save_play_count_cache(output_root, cache)


def cached_record_matches_video(record: Any, video: dict[str, Any]) -> bool:
    return isinstance(record, dict) and parse_metric(record.get("playCount")) > 0 and same_video_identity(record, video)


def history_play_count_records(output_root: Path, current_out_dir: Path, video: dict[str, Any]) -> list[tuple[float, dict[str, Any]]]:
    records: list[tuple[float, dict[str, Any]]] = []
    if not output_root.exists():
        return records

    cache = load_play_count_cache(output_root)
    for record in cache.values():
        if cached_record_matches_video(record, video):
            ts = parse_manifest_time(record.get("updatedAt"), output_root)
            normalized = dict(record)
            normalized.setdefault("source", "cache")
            records.append((ts, normalized))

    for run_dir in output_root.iterdir():
        if not run_dir.is_dir() or run_dir == current_out_dir or run_dir.name == "_cache":
            continue
        manifest_path = run_dir / "run_manifest.json"
        video_path = run_dir / "video.json"
        payload = read_json_file(manifest_path, {})
        candidate_video = payload.get("video") if isinstance(payload, dict) and isinstance(payload.get("video"), dict) else read_json_file(video_path, {})
        if not isinstance(candidate_video, dict) or not same_video_identity(candidate_video, video):
            continue
        if parse_metric(candidate_video.get("playCount")) <= 0:
            continue
        source = "history"
        if isinstance(payload, dict):
            metric_source = payload.get("metric_sources", {}).get("playCount") if isinstance(payload.get("metric_sources"), dict) else None
            if isinstance(metric_source, dict) and metric_source.get("source"):
                source = str(metric_source["source"])
            elif isinstance(payload.get("video_info_endpoint"), str):
                source = metric_source_from_endpoint(payload["video_info_endpoint"])
        ts = parse_manifest_time(payload.get("generated_at") if isinstance(payload, dict) else "", manifest_path if manifest_path.exists() else video_path)
        record = cache_record_from_video(candidate_video, source, run_dir, payload.get("generated_at") if isinstance(payload, dict) else None)
        records.append((ts, record))
    return records


def hydrate_play_count_from_cache(output_root: Path, current_out_dir: Path, video: dict[str, Any], metric_sources: dict[str, Any], warnings: list[str]) -> None:
    play_source = metric_sources.get("playCount")
    if metric_has_value(video.get("playCount")) and parse_metric(video.get("playCount")) > 0:
        source = play_source.get("source") if isinstance(play_source, dict) else "regular"
        update_play_count_cache(output_root, video, str(source or "regular"), current_out_dir)
        return

    records = history_play_count_records(output_root, current_out_dir, video)
    if records:
        _, record = max(records, key=lambda item: item[0])
        video["playCount"] = metric_cache_value(record.get("playCount"))
        metric_sources["playCount"] = {
            "source": "cache",
            "cachedAt": record.get("updatedAt"),
            "sourceRunDir": record.get("sourceRunDir"),
            "originalSource": record.get("source"),
        }
        update_play_count_cache(output_root, video, str(record.get("source") or "cache"), str(record.get("sourceRunDir") or current_out_dir), str(record.get("updatedAt") or ""))
        return

    metric_sources["playCount"] = {"source": "missing"}
    warning = "播放量实时接口未返回，且没有可用历史缓存。"
    if warning not in warnings:
        warnings.append(warning)


def format_metric(value: Any) -> str:
    number = parse_metric(value)
    raw = str(value or "").strip()
    if number <= 0 and raw not in {"0", "0.0"}:
        return raw or "--"
    if number >= 10000:
        wan = number / 10000
        return f"{wan:.1f}万".replace(".0万", "万")
    if float(number).is_integer():
        return f"{int(number):,}"
    return f"{number:,.1f}"


def format_display_value(value: Any) -> str:
    raw = str(value or "").strip()
    if "%" in raw or re.fullmatch(r"\d+\.\d+", raw):
        return raw
    return format_metric(value)


def format_percent(part: Any, total: Any) -> str:
    numerator = parse_metric(part)
    denominator = parse_metric(total)
    if numerator <= 0 or denominator <= 0:
        return "--"
    return f"{numerator / denominator * 100:.2f}%"


def format_ratio(part: Any, total: Any) -> str:
    numerator = parse_metric(part)
    denominator = parse_metric(total)
    if numerator <= 0 or denominator <= 0:
        return "--"
    return f"{numerator / denominator:.2f}"


def normalize_video(payload: Any, input_url: str, resolved_url: str) -> dict[str, Any]:
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), dict):
        raise RuntimeError(api_error_message(payload, "解析抖音视频失败。"))

    data = payload["data"]
    author = data.get("author") if isinstance(data.get("author"), dict) else {}
    video = data.get("video") if isinstance(data.get("video"), dict) else {}
    music = data.get("music") if isinstance(data.get("music"), dict) else {}
    stats = data.get("statistics") if isinstance(data.get("statistics"), dict) else {}
    image_urls = [normalize_remote_url(item) for item in data.get("images") or []]
    image_urls = [item for item in image_urls if item]

    return {
        "platform": "douyin",
        "title": str(data.get("title") or "未命名视频"),
        "authorName": str(author.get("nickname") or "--"),
        "authorId": str(author.get("unique_id") or author.get("uid") or "--"),
        "publishedAt": str(data.get("create_time_date") or "--"),
        "duration": str(video.get("Duration") or "--"),
        "videoId": str(data.get("aweme_id") or "--"),
        "coverUrl": normalize_remote_url(video.get("video_cover_url") or author.get("avatar_image")),
        "originalUrl": str(data.get("share_url") or resolved_url or input_url),
        "resolvedUrl": resolved_url,
        "downloadUrl": str(video.get("video_down_url") or ""),
        "musicTitle": str(music.get("music_title") or "--"),
        "musicUrl": str(music.get("music_url") or ""),
        "imageCount": len(image_urls),
        "imageUrls": image_urls,
        "playCount": extract_play_count(payload),
        "likeCount": to_number_or_text(stats.get("digg_count")),
        "commentCount": to_number_or_text(stats.get("comment_count")),
        "shareCount": to_number_or_text(stats.get("share_count")),
        "collectCount": to_number_or_text(stats.get("collect_count")),
        "description": str(data.get("title") or ""),
    }


def fetch_video_info(base_url: str, url: str, key: str, raw_dir: Path) -> tuple[dict[str, Any], str, dict[str, Any]]:
    attempts: list[tuple[str, dict[str, Any], int, int, int]] = []
    if key:
        for attempt_index in range(1, VIDEO_INFO_VIP_RETRIES + 1):
            attempts.append(("/tool/douyin/Dy_video_info_VIP", {"url": url, "key": key}, 90, attempt_index, VIDEO_INFO_VIP_RETRIES))
    attempts.append(("/tool/douyin/Dy_video_info", {"url": url, "key": key}, 45, 1, 1))

    last_error = ""
    for endpoint, params, timeout, attempt_index, attempt_total in attempts:
        raw_name = endpoint.rsplit("/", 1)[-1]
        raw_path = raw_dir / (f"{raw_name}_{attempt_index}.json" if attempt_total > 1 else f"{raw_name}.json")
        try:
            payload = post_query(base_url, endpoint, params, timeout=timeout)
            write_json(raw_path, payload)
            write_json(raw_dir / f"{raw_name}.json", payload)
            if payload_ok(payload):
                video = normalize_video(payload, params["url"], url)
                play_source = metric_source_from_endpoint(endpoint)
                metric_sources = {
                    "playCount": {
                        "source": play_source if metric_has_value(video.get("playCount")) else "missing",
                        "endpoint": endpoint,
                        "attempt": attempt_index,
                    }
                }
                return video, endpoint, metric_sources
            last_error = api_error_message(payload, "解析抖音视频失败。")
        except Exception as exc:
            last_error = redact_sensitive_text(exc, [key])
            error_payload = {"endpoint": endpoint, "attempt": attempt_index, "error": last_error}
            write_json(raw_dir / (f"{raw_name}_{attempt_index}_error.json" if attempt_total > 1 else f"{raw_name}_error.json"), error_payload)
            write_json(raw_dir / f"{raw_name}_error.json", error_payload)
        if attempt_total > 1 and attempt_index < attempt_total:
            time.sleep(VIDEO_INFO_VIP_RETRY_DELAYS[min(attempt_index - 1, len(VIDEO_INFO_VIP_RETRY_DELAYS) - 1)])
    raise RuntimeError(last_error or "解析抖音视频失败。")


def is_usable_transcript_text(value: str) -> bool:
    text = value.strip()
    if not text or re.match(r"^https?://", text, re.I):
        return False
    if re.fullmatch(r"\d+(?:\.\d+)?", text):
        return False
    if re.fullmatch(r"(ok|success|true|false)", text, re.I):
        return False
    return True


def collect_transcript_texts(value: Any, depth: int = 0) -> list[str]:
    if depth > 7 or value is None:
        return []
    if isinstance(value, (str, int, float)):
        text = str(value).strip()
        return [text] if is_usable_transcript_text(text) else []
    if isinstance(value, list):
        values: list[str] = []
        for item in value:
            values.extend(collect_transcript_texts(item, depth + 1))
        return values
    if not isinstance(value, dict):
        return []

    text_keys = {"text", "transcript", "transcription", "content", "sentence", "sentences", "utterance", "words"}
    direct: list[str] = []
    for key, child in value.items():
        if re.sub(r"[-_\s]", "", key).lower() in text_keys:
            direct.extend(collect_transcript_texts(child, depth + 1))
    if direct:
        return direct

    skip_keys = {"code", "msg", "message", "status", "success", "taskid", "id", "fileurl", "videourl", "url"}
    values = []
    for key, child in value.items():
        if re.sub(r"[-_\s]", "", key).lower() in skip_keys:
            continue
        values.extend(collect_transcript_texts(child, depth + 1))
    return values


def extract_speech_text(payload: Any) -> str:
    sources: list[Any] = []
    if isinstance(payload, dict):
        for key in ["result", "data", "text", "transcript", "transcription", "content"]:
            if key in payload:
                sources.append(payload[key])
    if not sources:
        sources = [payload]
    texts: list[str] = []
    seen: set[str] = set()
    for source in sources:
        for text in collect_transcript_texts(source):
            cleaned = text.strip()
            if cleaned and cleaned not in seen:
                seen.add(cleaned)
                texts.append(cleaned)
    return "\n\n".join(texts)


def transcript_sources(video: dict[str, Any], raw_url: str, resolved_url: str) -> list[str]:
    candidates = []
    video_id = str(video.get("videoId") or "").strip()
    if re.fullmatch(r"\d+", video_id):
        candidates.append(f"https://www.douyin.com/video/{video_id}")
    candidates.extend([resolved_url, str(video.get("originalUrl") or ""), normalize_douyin_url(raw_url), raw_url, str(video.get("downloadUrl") or "")])
    result: list[str] = []
    seen: set[str] = set()
    for item in candidates:
        text = str(item or "").strip()
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result


def fetch_transcript(base_url: str, video: dict[str, Any], raw_url: str, resolved_url: str, key: str, raw_dir: Path, warnings: list[str]) -> tuple[str, str]:
    if not key:
        warnings.append("没有配置 HOTBEE_API_KEY，已跳过音视频转文案。")
        return "", ""

    last_error = ""
    for index, source in enumerate(transcript_sources(video, raw_url, resolved_url), start=1):
        for attempt in range(len(TRANSCRIPT_RETRY_DELAYS) + 1):
            try:
                payload = post_query(base_url, "/tool/speech/speechToText", {"file_url": source, "key": key}, timeout=120)
                write_json(raw_dir / f"speechToText_{index}_{attempt + 1}.json", payload)
                if not payload_ok(payload):
                    raise RuntimeError(api_error_message(payload, "生成视频文案失败。"))
                text = extract_speech_text(payload)
                if text.strip():
                    return text, source
                raise RuntimeError("转写接口未返回文案。")
            except Exception as exc:
                last_error = redact_sensitive_text(exc, [key])
                if attempt < len(TRANSCRIPT_RETRY_DELAYS):
                    time.sleep(TRANSCRIPT_RETRY_DELAYS[attempt])
    warnings.append(f"文案转写失败：{last_error}")
    return "", ""


def pick_text(record: dict[str, Any], keys: list[str]) -> str:
    for key in keys:
        value = record.get(key)
        if isinstance(value, (str, int, float, bool)):
            text = str(value).strip()
            if text:
                return text
    return ""


def pick_nested_text(record: dict[str, Any], object_keys: list[str], value_keys: list[str]) -> str:
    for object_key in object_keys:
        nested = record.get(object_key)
        if isinstance(nested, dict):
            text = pick_text(nested, value_keys)
            if text:
                return text
    return ""


def classify_comment_intent(text: str) -> str:
    if re.search(r"网址|网站|链接|入口|哪里|哪儿|怎么进|发我|给我|求|waytoagi|豆包", text, re.I):
        return "求入口"
    if re.search(r"资料|资源|清单|模板|文档|教程|课件|安装包|关键词|文件", text, re.I):
        return "资料需求"
    if re.search(r"怎么|如何|步骤|操作|使用|搜索|打开|找不到|进不去|用不了|在哪里", text, re.I):
        return "操作追问"
    if re.search(r"收费|免费|付费|多少钱|会员|价格|贵|便宜|白嫖", text, re.I):
        return "价格付费"
    if re.search(r"假|骗|过期|真的假的|真实|质疑|没用|靠谱吗|不行|不能用", text, re.I):
        return "真实性质疑"
    if re.search(r"收藏|点赞|感谢|有用|学到|厉害|需要|码住|马上去|牛", text, re.I):
        return "认可收藏"
    if re.search(r"小白|新手|学生|老师|剪辑|运营|自媒体|创业|副业|公司|团队", text, re.I):
        return "人群场景"
    if re.search(r"分享|转发|推荐|朋友|同事|群里|扩散", text, re.I):
        return "分享传播"
    return "其他评论"


def normalize_comment_record(value: Any, index: int) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    text = (
        pick_text(value, ["text", "comment", "content", "comment_text", "commentText", "desc", "reply_comment", "replyComment", "aweme_desc", "awemeDesc"])
        or pick_nested_text(value, ["comment", "item", "data", "comments"], ["text", "content", "desc", "comment_text", "commentText"])
    )
    if not text:
        return None
    author = (
        pick_text(value, ["nickname", "user_name", "userName", "author", "name", "screen_name"])
        or pick_nested_text(value, ["user", "author", "user_info", "userInfo", "userInfoV2"], ["nickname", "name", "unique_id", "short_id"])
        or "匿名用户"
    )
    location = (
        pick_text(value, ["ip", "ip_label", "ipLabel", "location", "province", "city", "region"])
        or pick_nested_text(value, ["user", "author", "user_info", "userInfo"], ["ip_label", "ipLabel", "location"])
        or "--"
    )
    like_count = value.get("digg_count", value.get("like_count", value.get("likeCount", value.get("likes", value.get("zan", value.get("reply_comment_total", 0))))))
    comment_id = pick_text(value, ["cid", "id", "comment_id", "commentId", "aweme_id", "awemeId"]) or f"{index}-{text[:12]}"
    return {
        "id": comment_id,
        "author": author,
        "text": text,
        "time": pick_text(value, ["create_time_date", "create_time", "createTime", "time", "date", "created_at"]) or "--",
        "location": location,
        "likeCount": to_number_or_text(like_count),
        "intent": classify_comment_intent(text),
    }


def normalize_comment_tree(value: Any, parent_index: int = 0) -> list[dict[str, Any]]:
    primary = normalize_comment_record(value, parent_index)
    replies: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key in ["replies", "reply_comment_list", "replyCommentList", "reply_comments", "replyComments", "sub_comments", "subComments"]:
            source = value.get(key)
            if isinstance(source, list):
                for index, reply in enumerate(source):
                    item = normalize_comment_record(reply, parent_index * 1000 + index + 1)
                    if item:
                        replies.append(item)
                break
    return ([primary] if primary else []) + replies


COMMENT_COLLECTION_KEYS = {"data", "comments", "commentlist", "comment_list", "list", "items", "records"}


def collect_comment_collections(value: Any, depth: int = 0) -> list[list[Any]]:
    if depth > 6 or value is None:
        return []
    if isinstance(value, list):
        object_items = [item for item in value if isinstance(item, dict)]
        nested: list[list[Any]] = []
        for item in value:
            nested.extend(collect_comment_collections(item, depth + 1))
        return ([object_items] if object_items else []) + nested
    if not isinstance(value, dict):
        return []

    keyed: list[list[Any]] = []
    for key, child in value.items():
        normalized_key = re.sub(r"[-_\s]", "", key).lower()
        if normalized_key in COMMENT_COLLECTION_KEYS:
            keyed.extend(collect_comment_collections(child, depth + 1))
    if keyed:
        return keyed
    nested = []
    for child in value.values():
        nested.extend(collect_comment_collections(child, depth + 1))
    return nested


def normalize_comments_payload(payload: Any) -> list[dict[str, Any]]:
    comments: list[dict[str, Any]] = []
    for collection_index, items in enumerate(collect_comment_collections(payload)):
        for item_index, item in enumerate(items):
            comments.extend(normalize_comment_tree(item, collection_index * 1000 + item_index))
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in comments:
        key = f"{item['id']}-{item['text']}"
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def merge_comments_payloads(payloads: list[Any], limit: int) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for payload in payloads:
        for item in normalize_comments_payload(payload):
            key = f"{item['id']}-{item['text']}"
            if key in seen:
                continue
            seen.add(key)
            result.append(item)
            if len(result) >= limit:
                return result
    return result


def fetch_comments(base_url: str, video: dict[str, Any], raw_url: str, resolved_url: str, key: str, max_comments: int, raw_dir: Path, warnings: list[str]) -> list[dict[str, Any]]:
    if not key:
        warnings.append("没有配置 HOTBEE_API_KEY，已跳过评论采集。")
        return []

    expected_count = parse_metric(video.get("commentCount"))
    capped_limit = max(1, min(MAX_COMMENT_LIMIT, max_comments))
    expected_pages = math.ceil(min(expected_count, capped_limit) / COMMENT_PAGE_SIZE) if expected_count > 0 else DEFAULT_COMMENT_PAGES
    page_count = max(1, min(math.ceil(capped_limit / COMMENT_PAGE_SIZE), expected_pages or DEFAULT_COMMENT_PAGES))

    candidates = []
    video_id = str(video.get("videoId") or "").strip()
    if re.fullmatch(r"\d+", video_id):
        candidates.append(f"https://www.douyin.com/video/{video_id}")
    candidates.extend([resolved_url, normalize_douyin_url(raw_url), str(video.get("originalUrl") or ""), raw_url])

    unique_candidates: list[str] = []
    seen_candidates: set[str] = set()
    for item in candidates:
        text = str(item or "").strip()
        if is_douyin_url(text) and text not in seen_candidates:
            seen_candidates.add(text)
            unique_candidates.append(text)

    last_error = ""
    for candidate_index, candidate in enumerate(unique_candidates, start=1):
        payloads: list[Any] = []
        for page in range(1, page_count + 1):
            try:
                payload = post_query(
                    base_url,
                    "/tool/douyin/Dy_video_all_comments_VIP",
                    {"video_url": candidate, "page": page, "key": key},
                    timeout=90,
                )
                write_json(raw_dir / f"comments_{candidate_index}_{page}.json", payload)
                comments = normalize_comments_payload(payload)
                if not payload_ok(payload) and not comments:
                    raise RuntimeError(api_error_message(payload, "获取评论失败。"))
                if not comments and page > 1:
                    break
                payloads.append(payload)
                merged = merge_comments_payloads(payloads, capped_limit)
                if len(merged) >= capped_limit:
                    return merged
                if len(comments) < COMMENT_PAGE_SIZE:
                    break
                time.sleep(0.26)
            except Exception as exc:
                last_error = redact_sensitive_text(exc, [key])
                write_json(raw_dir / f"comments_{candidate_index}_{page}_error.json", {"video_url": candidate, "page": page, "error": last_error})
                break
        merged = merge_comments_payloads(payloads, capped_limit)
        if merged:
            return merged
    if expected_count > 0:
        warnings.append(f"评论采集未返回有效数据：{last_error or '接口为空'}")
    return []


STOP_WORDS = {"这个", "那个", "什么", "怎么", "可以", "就是", "还是", "没有", "不是", "一下", "一个", "这种", "现在", "感觉", "真的", "哈哈", "哈哈哈", "视频", "评论", "博主", "看看", "知道", "需要", "不能", "不会", "已经", "是不是"}
COMMENT_KEYWORD_GROUPS = [
    ("链接入口", ["链接", "网址", "网站", "入口", "发我", "给我", "求链接", "求网址"]),
    ("资料资源", ["资料", "资源", "清单", "模板", "文档", "文件"]),
    ("教程步骤", ["教程", "步骤", "怎么用", "如何使用", "操作", "搜索"]),
    ("价格收费", ["收费", "免费", "付费", "多少钱", "会员", "价格"]),
    ("真实性", ["真的", "假的", "真实", "骗人", "靠谱吗", "过期", "没用"]),
    ("收藏认可", ["收藏", "点赞", "感谢", "有用", "学到了", "码住", "厉害"]),
    ("AI工具", ["AI", "aigc", "工具", "豆包", "deepseek", "chatgpt", "waytoagi"]),
    ("适合人群", ["小白", "新手", "学生", "老师", "运营", "自媒体", "创业", "副业"]),
]


def normalize_comment_text(value: str) -> str:
    return re.sub(r"\s+", "", value.lower())


def match_alias(source: str, aliases: list[str]) -> bool:
    return any(normalize_comment_text(alias) in source for alias in aliases if normalize_comment_text(alias))


def useful_word(word: str) -> bool:
    text = word.strip()
    if len(text) < 2 or text in STOP_WORDS:
        return False
    if re.fullmatch(r"\d+", text):
        return False
    if re.fullmatch(r"[啊哈嗯哦诶呀吧吗呢了的得地是有和就都也在我你他她它们这那]+", text):
        return False
    return True


def extract_comment_keywords(text: str) -> list[str]:
    source = normalize_comment_text(text)
    words: set[str] = set()
    for label, aliases in COMMENT_KEYWORD_GROUPS:
        if match_alias(source, aliases):
            words.add(label)
    for tag in re.findall(r"#[^\s#，。！？、；：]+", text):
        word = tag.lstrip("#").strip()
        if useful_word(word):
            words.add(word)
    for word in re.findall(r"[A-Za-z][A-Za-z0-9-]{1,}", text):
        if useful_word(word):
            words.add(word)
    for run in re.findall(r"[\u4e00-\u9fff]{2,18}", text):
        for size in range(2, 5):
            if len(run) < size:
                continue
            for index in range(0, len(run) - size + 1):
                word = run[index:index + size]
                if useful_word(word):
                    words.add(word)
    return list(words)


def comment_stats(comments: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    intent_counts: dict[str, int] = {}
    keyword_counts: dict[str, int] = {}
    for comment in comments:
        intent = str(comment.get("intent") or "其他评论")
        intent_counts[intent] = intent_counts.get(intent, 0) + 1
        for word in extract_comment_keywords(str(comment.get("text") or "")):
            keyword_counts[word] = keyword_counts.get(word, 0) + 1
    intents = [{"label": label, "count": count} for label, count in sorted(intent_counts.items(), key=lambda item: (-item[1], item[0]))][:8]
    min_keyword_count = 2 if len(comments) >= 20 else 1
    keywords = [
        {"label": label, "count": count}
        for label, count in sorted(keyword_counts.items(), key=lambda item: (-item[1], -len(item[0]), item[0]))
        if count >= min_keyword_count
    ][:24]
    return intents, keywords


def split_sentences(text: str, max_count: int = 6) -> list[str]:
    normalized = re.sub(r"\s+", " ", text or "").strip()
    if not normalized:
        return []
    parts = [item.strip() for item in re.split(r"[。！？!?；;，,]", normalized) if item.strip()]
    source = parts or [normalized]
    if len(source) <= max_count:
        return source
    group_size = math.ceil(len(source) / max_count)
    return ["，".join(source[index:index + group_size]) for index in range(0, len(source), group_size)][:max_count]


def parse_duration_seconds(value: Any) -> int:
    text = str(value or "").strip()
    if not text or text == "--":
        return 0
    if re.fullmatch(r"\d+(?:\.\d+)?", text):
        return int(float(text))
    minute_second = re.fullmatch(r"(\d{1,2}):(\d{1,2})", text)
    if minute_second:
        return int(minute_second.group(1)) * 60 + int(minute_second.group(2))
    match = re.search(r"(\d+(?:\.\d+)?)", text)
    return int(float(match.group(1))) if match else 0


def extract_hot_words(text: str) -> list[str]:
    tags = list(dict.fromkeys(tag.lstrip("#").strip() for tag in re.findall(r"#[^\s#]+", text) if tag.strip()))
    keywords = [item for item in ["AI", "资料", "工具", "网站", "教程", "资源", "学习", "入口", "收藏", "评论", "干货", "模板", "转化"] if item.lower() in text.lower()]
    english = list(dict.fromkeys(word.strip() for word in re.findall(r"[A-Za-z][A-Za-z0-9-]{2,}", text)))
    return ([item for item in dict.fromkeys(tags + keywords + english) if item] or ["内容价值", "用户需求", "转化承接"])[:10]


def build_report_model(video: dict[str, Any], transcript: str, comments: list[dict[str, Any]]) -> dict[str, Any]:
    play_count = parse_metric(video.get("playCount"))
    like_count = parse_metric(video.get("likeCount"))
    collect_count = parse_metric(video.get("collectCount"))
    share_count = parse_metric(video.get("shareCount"))
    comment_count = parse_metric(video.get("commentCount"))

    narrative = "\n".join([transcript, str(video.get("description") or video.get("title") or "")]).strip()
    chunks = split_sentences(narrative or str(video.get("title") or ""), 6)
    duration = parse_duration_seconds(video.get("duration")) or max(18, len(chunks) * 4)
    timeline_source = chunks or [str(video.get("title") or "未命名视频")]
    scenes = ["开场抓停留", "价值证明", "细节展开", "峰值刺激", "行动提示", "收束转化"]
    actions = ["制造继续看的理由", "建立可信度", "把抽象价值落到具体画面", "放大利益点", "降低行动成本", "强化收藏或评论承接"]

    timeline = []
    for index, copy in enumerate(timeline_source):
        start = math.floor(duration * index / len(timeline_source))
        end = round(duration) if index == len(timeline_source) - 1 else math.floor(duration * (index + 1) / len(timeline_source))
        end = max(start + 1, end)
        strong_word = bool(re.search(r"最|直接|立刻|马上|免费|收藏|破防|失业|干货|教程|资源|必", copy))
        emotion = max(1, min(5, (3 if index == 0 else 2) + (1 if strong_word else 0) + (1 if index == 3 else 0)))
        timeline.append({
            "time": f"{start}-{end}s",
            "scene": scenes[index] if index < len(scenes) else "内容推进",
            "copy": copy[:96] + ("..." if len(copy) > 96 else ""),
            "emotion": emotion,
            "risk": "中" if len(copy) > 58 or index == len(timeline_source) - 1 else "低",
            "action": actions[index] if index < len(actions) else "推动用户继续理解内容",
        })

    top_intents, hot_keywords = comment_stats(comments)
    top_intent_label = top_intents[0]["label"] if top_intents else "暂无明显评论意图"
    summary = f"{video.get('authorName', '--')} 这条内容的核心看点是把“{video.get('title', '未命名视频')}”包装成可理解、可互动、可继续追问的内容。"
    hook = timeline[0]["copy"] if timeline else str(video.get("title") or "")
    themes = ["选题利益点明确", "信息密度较高", f"评论区主要反馈是：{top_intent_label}"]
    viral_factors = [
        "开头直接给出用户关心的结果或问题，降低理解成本。",
        "用具体场景、工具名或资源感建立可信度。",
        "评论区具备承接空间，适合用入口、教程、价格或适用人群继续转化。",
    ]
    suggestions = [
        "置顶评论补齐入口、价格、适合人群和使用门槛，减少重复追问。",
        "把评论里的高频需求拆成下一条视频选题，形成入口说明、教程步骤和避坑清单。",
        f"当前点赞率 {format_percent(like_count, play_count)}，建议继续测试更直接的 3 秒开头利益点。",
    ]
    if collect_count > like_count:
        suggestions[0] = "收藏强于点赞，结尾继续强化保存理由和资料入口。"
    if share_count > comment_count:
        suggestions[1] = "分享意愿高于评论意愿，适合包装成清单或步骤给用户转发。"

    script_blocks = [
        {"stage": "对立开场", "timeRange": timeline[0]["time"] if timeline else "0-4s", "label": "抓停留", "copy": hook},
        {"stage": "价值证明", "timeRange": timeline[1]["time"] if len(timeline) > 1 else "4-9s", "label": "建信任", "copy": timeline[1]["copy"] if len(timeline) > 1 else themes[0]},
        {"stage": "细节展开", "timeRange": timeline[2]["time"] if len(timeline) > 2 else "9-18s", "label": "推收藏", "copy": timeline[2]["copy"] if len(timeline) > 2 else viral_factors[0]},
        {"stage": "行动收束", "timeRange": timeline[-1]["time"] if timeline else "18s+", "label": "促动作", "copy": timeline[-1]["copy"] if timeline else suggestions[0]},
    ]
    return {
        "summary": summary,
        "hook": hook,
        "themes": themes,
        "viralFactors": viral_factors,
        "suggestions": suggestions,
        "timeline": timeline,
        "scriptBlocks": script_blocks,
        "hotWords": extract_hot_words("\n".join([str(video.get("title") or ""), str(video.get("description") or ""), transcript])),
        "commentIntents": top_intents,
        "commentKeywords": hot_keywords,
        "topComments": sorted(comments, key=lambda item: parse_metric(item.get("likeCount")), reverse=True)[:12],
    }


def build_breakdown_markdown(video: dict[str, Any], report: dict[str, Any], comments: list[dict[str, Any]]) -> str:
    lines = ["# 视频拆解报告", "", "## 核心摘要", report["summary"], "", "## 开场抓手", report["hook"], "", "## 主题判断"]
    lines.extend([f"- {item}" for item in report["themes"]])
    lines.extend(["", "## 爆款要素"])
    lines.extend([f"- {item}" for item in report["viralFactors"]])
    lines.extend(["", "## 画面拆解"])
    for item in report["timeline"]:
        lines.append(f"- {item['time']}｜{item['scene']}｜{item['copy']}｜动作：{item['action']}｜情绪 {item['emotion']}/5｜风险 {item['risk']}")
    lines.extend(["", "## 脚本拆解结构"])
    for item in report["scriptBlocks"]:
        lines.append(f"- {item['stage']}（{item['timeRange']}，{item['label']}）：{item['copy']}")
    lines.extend(["", "## 评论洞察"])
    if comments:
        for item in report["commentIntents"]:
            lines.append(f"- {item['label']}：{format_metric(item['count'])} 条")
    else:
        lines.append("- 暂无有效评论数据。")
    lines.extend(["", "## 优化建议"])
    lines.extend([f"- {item}" for item in report["suggestions"]])
    return "\n".join(lines).strip() + "\n"


def split_transcript_sentences(text: str) -> list[str]:
    transcript = re.sub(r"\r\n?", "\n", text or "").strip()
    if not transcript:
        return []
    if "\n" in transcript:
        return [line.strip() for line in transcript.splitlines() if line.strip()]
    return [item.strip() for item in re.split(r"(?<=[。！？!?])", transcript) if item.strip()] or [transcript]


def write_comments_csv(path: Path, comments: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["评论ID", "昵称", "评论内容", "时间", "地区", "点赞数", "意图"])
        for comment in comments:
            writer.writerow([comment.get("id", ""), comment.get("author", ""), comment.get("text", ""), comment.get("time", ""), comment.get("location", ""), comment.get("likeCount", ""), comment.get("intent", "")])


def guess_extension(url: str, content_type: str) -> str:
    from_type = mimetypes.guess_extension((content_type or "").split(";")[0].strip())
    if from_type:
        return ".jpg" if from_type == ".jpe" else from_type
    suffix = Path(urllib.parse.urlparse(url).path).suffix.lower()
    return suffix if suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif"} else ".jpg"


def download_media(url: str, target_stem: Path, warnings: list[str]) -> str:
    if not url:
        return ""
    if not is_allowed_media_url(url):
        warnings.append(f"已拒绝不安全的图片地址：{redact_url_for_log(url)}")
        return ""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 HotBee-Douyin-Video-Report/1.0", "Referer": "https://www.douyin.com/"})
        with urllib.request.urlopen(req, timeout=35) as response:
            declared_size = int(response.headers.get("Content-Length") or 0)
            if declared_size > MAX_MEDIA_BYTES:
                raise ValueError("图片超过 25 MB 安全上限。")
            content = response.read(MAX_MEDIA_BYTES + 1)
            if len(content) > MAX_MEDIA_BYTES:
                raise ValueError("图片超过 25 MB 安全上限。")
            content_type = response.headers.get("Content-Type", "")
        path = target_stem.with_suffix(guess_extension(url, content_type))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path.name
    except Exception as exc:
        warnings.append(f"图片下载失败：{redact_url_for_log(url)}；原因：{redact_sensitive_text(exc)}")
        return ""


def download_images(video: dict[str, Any], images_dir: Path, warnings: list[str]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    cover = download_media(str(video.get("coverUrl") or ""), images_dir / "cover", warnings)
    if cover:
        items.append({"label": "封面", "url": str(video.get("coverUrl") or ""), "file": f"images/{cover}"})
    for index, url in enumerate(video.get("imageUrls") or [], start=1):
        file_name = download_media(str(url), images_dir / f"image_{index:02d}", warnings)
        if file_name:
            items.append({"label": f"图集 {index}", "url": str(url), "file": f"images/{file_name}"})
    return items


def esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def render_list(items: list[str]) -> str:
    return "\n".join(f"<li>{esc(item)}</li>" for item in items)


def render_section_title(title: str, desc: str = "") -> str:
    description = f'<p class="section-desc">{esc(desc)}</p>' if desc else ""
    return f'<div class="section-title"><h3>{esc(title)}</h3>{description}</div>'


def render_primary_metric(label: str, value: Any) -> str:
    return f"""
    <div class="metric-card metric-card-primary">
      <div class="metric-label">{esc(label)}</div>
      <div class="metric-value">{esc(format_metric(value))}</div>
    </div>
    """


def render_metric(label: str, value: Any, hint: str = "") -> str:
    return f"""
    <div class="metric-card">
      <div class="metric-label">{esc(label)}</div>
      <div class="metric-value">{esc(format_display_value(value))}</div>
      <div class="metric-hint">{esc(hint)}</div>
    </div>
    """


def clamp_percent(value: Any, fallback: float = 0) -> int:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = fallback
    return max(0, min(100, round(number)))


def render_comment_cloud(items: list[dict[str, Any]]) -> str:
    entries = [item for item in items if item.get("label")]
    if not entries:
        return '<span class="comment-cloud-empty">暂无明显核心热词</span>'
    max_count = max((parse_metric(item.get("count")) for item in entries), default=1) or 1
    offsets = [-8, 5, -3, 9, -6, 4]
    rotations = [-6, 4, -2, 5, -4, 3]
    chips = []
    for index, item in enumerate(entries[:18]):
        ratio = max(0.18, parse_metric(item.get("count")) / max_count)
        font_size = round(14 + ratio * 22)
        padding_y = round(6 + ratio * 5)
        padding_x = round(10 + ratio * 14)
        style = (
            f"font-size:{font_size}px;line-height:1.08;"
            f"padding:{padding_y}px {padding_x}px;"
            f"transform:translateY({offsets[index % len(offsets)]}px) rotate({rotations[index % len(rotations)]}deg);"
        )
        label = str(item.get("label") or "")
        chips.append(
            f'<button type="button" class="comment-cloud-chip" data-comment-filter-type="keyword" data-comment-filter-value="{esc(label)}" '
            f'style="{esc(style)}" title="{esc(label)}：{esc(format_metric(item.get("count")))} 条评论">{esc(label)}</button>'
        )
    return "\n".join(chips)


def render_intent_stats(items: list[dict[str, Any]], total: int) -> str:
    if not items:
        return '<div class="intent-empty">暂无明显意图</div>'
    safe_total = max(1, total)
    rows = []
    for item in items:
        width = max(8, round(parse_metric(item.get("count")) / safe_total * 100))
        label = str(item.get("label") or "")
        rows.append(f"""
        <button type="button" class="intent-row" data-comment-filter-type="intent" data-comment-filter-value="{esc(label)}">
          <div class="intent-row-head"><span>{esc(item.get('label'))}</span><strong>{esc(format_metric(item.get('count')))}</strong></div>
          <div class="intent-track"><div class="intent-fill" style="width:{width}%"></div></div>
        </button>
        """)
    return "\n".join(rows)


def render_keyword_chips(items: list[dict[str, Any]], limit: int = 5) -> str:
    entries = [item for item in items if item.get("label")][:limit]
    if not entries:
        return '<span class="keyword-chip muted-chip">暂无明显热词</span>'
    return "\n".join(
        f'<button type="button" class="keyword-chip" data-comment-filter-type="keyword" data-comment-filter-value="{esc(item.get("label"))}">{esc(item.get("label"))} · {esc(format_metric(item.get("count")))}</button>'
        for item in entries
    )


def render_comment_cards(comments: list[dict[str, Any]]) -> str:
    if not comments:
        return '<div class="comment-empty">暂无评论样本。</div>'
    cards = []
    for comment in comments:
        cards.append(f"""
        <article class="comment-item">
          <div class="comment-meta"><span class="comment-intent">{esc(comment.get('intent'))}</span><span>{esc(comment.get('location'))} · 赞 {esc(format_metric(comment.get('likeCount')))}</span></div>
          <h4>{esc(comment.get('author'))}</h4>
          <p>{esc(comment.get('text'))}</p>
          <div class="comment-time">{esc(comment.get('time'))}</div>
        </article>
        """)
    return "\n".join(cards)


def render_comments_json(comments: list[dict[str, Any]]) -> str:
    payload = json.dumps(comments, ensure_ascii=False)
    return payload.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")


def render_html(video: dict[str, Any], report: dict[str, Any], transcript: str, comments: list[dict[str, Any]], media: list[dict[str, str]], warnings: list[str]) -> str:
    cover_file = next((item["file"] for item in media if item["label"] == "封面"), "")
    comment_total = len(comments)
    expected_comment_count = parse_metric(video.get("commentCount"))
    comment_desc = f"已拆解 {format_metric(comment_total)} 条评论"
    if expected_comment_count:
        comment_desc += f" / 视频评论 {format_metric(video.get('commentCount'))}"
    comments_html = render_comment_cards(comments)
    intent_html = render_intent_stats(report["commentIntents"], comment_total)
    keyword_html = render_keyword_chips(report["commentKeywords"], limit=5)
    cloud_html = render_comment_cloud(report["commentKeywords"])
    comments_json = render_comments_json(comments)
    timeline_html = "\n".join(
        f"""
        <div class="timeline-item">
          <div class="timeline-time"><strong>{esc(item['time'])}</strong><span>{esc(item['scene'])}</span></div>
          <div class="timeline-copy"><p>{esc(item['copy'])}</p><small>{esc(item['action'])}</small></div>
          <div class="timeline-signal">
            <div class="timeline-signal-head"><span>情绪 {esc(item['emotion'])}/5</span><span>风险 {esc(item['risk'])}</span></div>
            <div class="progress-track"><div class="progress-fill" style="width:{clamp_percent(parse_metric(item.get('emotion')) * 20)}%"></div></div>
          </div>
        </div>
        """
        for item in report["timeline"]
    )
    script_html = "\n".join(
        f"""
        <div class="script-card">
          <div class="script-title">{esc(item['stage'])}<span>{esc(item['label'])}</span></div>
          <small>{esc(item['timeRange'])}</small>
          <p>{esc(item['copy'])}</p>
        </div>
        """
        for item in report["scriptBlocks"]
    )
    warning_html = "\n".join(f"<li>{esc(item)}</li>" for item in warnings)
    platform_label = {"douyin": "抖音", "bilibili": "B站", "rednote": "小红书"}.get(str(video.get("platform") or "").lower(), str(video.get("platform") or "平台"))
    styles = """
    :root {
      --video-bg-0:#f2eee6;
      --video-bg-1:#ece7dd;
      --video-bg-2:#dedbd4;
      --video-text:#161616;
      --video-muted:rgba(20,20,20,.52);
      --video-soft:rgba(20,20,20,.66);
      --video-line:rgba(20,20,20,.13);
      --video-panel:rgba(255,252,244,.68);
      --video-panel-solid:rgba(255,252,244,.96);
      --video-warning:#9d2d2d;
      --video-font-serif:"Songti SC","Noto Serif CJK SC","Noto Serif SC","Source Han Serif SC","SimSun",serif;
      --video-font-sans:-apple-system,BlinkMacSystemFont,"Inter","PingFang SC","Microsoft YaHei",sans-serif;
    }
    * { box-sizing:border-box; }
    html,body { margin:0; min-height:100%; background:var(--video-bg-0); }
    body { color:var(--video-text); font-family:var(--video-font-sans); text-rendering:optimizeLegibility; }
    main { width:min(1450px,calc(100vw - 56px)); max-width:100%; margin:28px auto 40px; }
    .video-report { display:flex; flex-direction:column; gap:28px; width:100%; min-width:0; padding:0; background:var(--video-bg-0); color:var(--video-text); }
    .hero-grid { display:grid; grid-template-columns:minmax(220px,270px) minmax(0,1fr); gap:28px; align-items:stretch; }
    .hero-grid,.hero-card,.panel,.split-grid,.comment-grid,.metrics-grid,.script-grid,.suggestions-grid,.comment-subgrid { min-width:0; }
    .cover { display:flex; width:100%; min-height:360px; align-items:stretch; justify-content:center; border:0; background:transparent; }
    .cover img { display:block; width:100%; height:100%; border-radius:22px; object-fit:cover; filter:saturate(.92) contrast(.98); }
    .cover-empty { display:flex; min-height:320px; width:100%; align-items:center; justify-content:center; border:1px solid var(--video-line); border-radius:22px; background:var(--video-panel-solid); color:var(--video-muted); }
    .hero-card,.panel,.metric-card,.inner-card,.script-card,.comment-item { border:1px solid var(--video-line); background:var(--video-panel-solid); box-shadow:none; }
    .hero-card { min-height:360px; border-radius:22px; padding:30px; }
    .heading-row { display:flex; flex-wrap:wrap; align-items:center; gap:16px; }
    .kicker { font-family:var(--video-font-serif); font-size:24px; font-weight:400; line-height:1.15; }
    .pill,.hotword,.keyword-chip,.comment-cloud-chip,.comment-intent { display:inline-flex; align-items:center; justify-content:center; border:1px solid var(--video-line); border-radius:999px; background:rgba(255,252,244,.94); color:var(--video-soft); }
    .pill { min-height:32px; padding:7px 16px; font-size:14px; font-weight:500; }
    h1,h2,h3,h4,.metric-value,.timeline-time strong,.script-title { margin:0; color:var(--video-text); font-family:var(--video-font-serif); font-weight:400; letter-spacing:0; }
    h1 { display:-webkit-box; margin-top:24px; overflow:hidden; -webkit-box-orient:vertical; -webkit-line-clamp:2; font-size:clamp(42px,3.6vw,60px); line-height:1.18; overflow-wrap:anywhere; }
    .summary { margin:22px 0 0; color:var(--video-soft); font-family:var(--video-font-serif); font-size:30px; line-height:1.6; overflow-wrap:anywhere; }
    .hotwords { display:flex; flex-wrap:wrap; gap:10px; margin-top:24px; }
    .hotword { min-height:30px; padding:7px 15px; font-size:13px; font-weight:600; }
    .metrics-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:20px; }
    .metric-card { min-height:136px; border-radius:18px; padding:23px; }
    .metric-card-primary { background:var(--video-panel-solid); }
    .metric-label { color:var(--video-soft); font-size:15px; font-weight:650; }
    .metric-card-primary .metric-label { color:var(--video-text); }
    .metric-value { margin-top:16px; font-size:38px; line-height:1.05; }
    .metric-hint { margin-top:12px; color:var(--video-muted); font-size:12px; line-height:1.55; }
    .split-grid { display:grid; grid-template-columns:minmax(300px,390px) minmax(0,1fr); gap:24px; }
    .panel { border-radius:22px; padding:26px; }
    .section-title h3 { font-size:30px; line-height:1.2; }
    .section-desc { margin:8px 0 0; color:var(--video-soft); font-family:var(--video-font-serif); font-size:15px; line-height:1.6; }
    .inner-card { border-radius:18px; padding:22px; }
    .hook-label { color:var(--video-warning); font-size:14px; font-weight:700; }
    p { color:var(--video-soft); font-family:var(--video-font-serif); letter-spacing:0; overflow-wrap:anywhere; }
    .inner-card p,.viral-item p,.script-card p,.suggestion-card p { margin:12px 0 0; font-size:18px; line-height:1.85; }
    .theme-list { display:flex; flex-wrap:wrap; gap:14px; margin-top:18px; }
    .theme-card { min-width:190px; flex:1; border-radius:16px; background:var(--video-panel-solid); padding:18px; color:var(--video-soft); font-family:var(--video-font-serif); font-size:16px; line-height:1.65; }
    .viral-list { display:flex; flex-direction:column; gap:14px; margin-top:22px; }
    .viral-item { display:flex; gap:14px; border-radius:16px; background:var(--video-panel-solid); padding:18px; }
    .viral-index { display:flex; width:30px; height:30px; flex:0 0 30px; align-items:center; justify-content:center; border-radius:999px; background:#fff1ea; color:var(--video-warning); font-size:13px; font-weight:900; }
    .timeline-list { display:flex; flex-direction:column; gap:16px; margin-top:26px; }
    .timeline-item { display:grid; grid-template-columns:120px minmax(0,1fr) 210px; gap:24px; align-items:center; border:1px solid var(--video-line); border-radius:18px; background:var(--video-panel-solid); padding:20px; }
    .timeline-time strong { display:block; font-size:24px; line-height:1.1; }
    .timeline-time span,.timeline-copy small,.timeline-signal-head { color:var(--video-muted); font-size:13px; font-weight:650; }
    .timeline-time span { display:block; margin-top:9px; }
    .timeline-copy p { margin:0; font-size:17px; line-height:1.75; }
    .timeline-copy small { display:block; margin-top:8px; }
    .timeline-signal-head { display:flex; justify-content:space-between; gap:14px; }
    .progress-track,.intent-track { overflow:hidden; border-radius:999px; background:rgba(20,20,20,.12); }
    .progress-track { height:10px; margin-top:11px; }
    .progress-fill,.intent-fill { height:100%; border-radius:999px; background:var(--video-text); }
    .script-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:20px; margin-top:26px; }
    .script-card { border-radius:18px; padding:22px; }
    .script-head { display:flex; align-items:center; justify-content:space-between; gap:12px; }
    .script-title { font-size:20px; line-height:1.25; }
    .script-label { border-radius:999px; background:#fff1ea; padding:4px 12px; color:var(--video-warning); font-size:12px; font-weight:700; white-space:nowrap; }
    .script-time { margin-top:12px; color:var(--video-muted); font-size:13px; font-weight:650; }
    .script-card p { font-size:16px; line-height:1.78; }
    .comment-section { background:var(--video-panel-solid); }
    .comment-grid { display:grid; grid-template-columns:minmax(0,1fr) minmax(360px,1fr); gap:26px; align-items:stretch; margin-top:26px; }
    .comment-left { display:flex; min-height:0; flex-direction:column; gap:22px; }
    .comment-subgrid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:20px; }
    .comment-panel { border-radius:18px; background:var(--video-panel-solid); padding:22px; }
    .comment-panel-title { color:var(--video-text); font-family:var(--video-font-serif); font-size:20px; line-height:1.2; }
    .cloud-stage { position:relative; min-height:330px; margin:22px auto 0; overflow:hidden; padding:28px 18px; }
    .cloud-stage::before { content:""; position:absolute; inset:54px 36px 28px; border-radius:52%; background:#f3faff; opacity:.6; }
    .comment-cloud-list { position:relative; z-index:1; display:flex; min-height:260px; flex-wrap:wrap; align-content:center; align-items:center; justify-content:center; gap:16px; padding:22px; }
    .comment-cloud-chip { flex:0 0 auto; color:#383838; font-family:var(--video-font-sans); font-weight:900; white-space:nowrap; cursor:pointer; transition:border-color .16s ease, background .16s ease, color .16s ease; }
    .comment-cloud-chip:hover,.comment-cloud-chip.is-active { border-color:#161616; background:#fff; color:#161616; }
    .comment-cloud-empty,.intent-empty,.comment-empty { display:block; border:1px solid var(--video-line); border-radius:16px; background:var(--video-panel-solid); padding:16px; color:var(--video-muted); font-size:14px; font-weight:700; }
    .intent-list { display:flex; flex-direction:column; gap:12px; margin-top:18px; }
    .intent-row { display:block; width:100%; border:1px solid var(--video-line); border-radius:14px; background:var(--video-panel-solid); padding:14px; text-align:left; cursor:pointer; transition:border-color .16s ease, background .16s ease; }
    .intent-row:hover,.intent-row.is-active { border-color:#161616; background:#fff; }
    .intent-row-head { display:flex; justify-content:space-between; gap:12px; color:var(--video-text); font-size:15px; font-weight:900; }
    .intent-row-head strong { color:var(--video-soft); font-size:13px; }
    .intent-track { height:8px; margin-top:12px; }
    .keyword-list { display:flex; flex-wrap:wrap; gap:10px; margin-top:18px; }
    .keyword-chip { min-height:30px; padding:7px 13px; color:#383838; font-family:var(--video-font-sans); font-size:13px; font-weight:700; cursor:pointer; transition:border-color .16s ease, background .16s ease; }
    .keyword-chip:hover,.keyword-chip.is-active { border-color:#161616; background:#fff; }
    .muted-chip { color:var(--video-muted); }
    .comments-panel { display:flex; min-height:0; flex-direction:column; overflow:hidden; border-radius:18px; background:var(--video-panel-solid); padding:22px; }
    .comments-head { display:flex; flex-wrap:wrap; align-items:flex-start; justify-content:space-between; gap:16px; }
    .comments-head p { margin:5px 0 0; color:var(--video-muted); font-family:var(--video-font-sans); font-size:13px; }
    .comments-count { min-height:30px; padding:7px 14px; font-size:13px; font-weight:700; }
    .comments-filter { display:flex; flex-wrap:wrap; gap:10px; margin-top:18px; }
    .comments-list { flex:1 1 0%; min-height:0; max-height:688px; margin-top:18px; overflow:hidden; padding-right:8px; }
    .comment-item { border-radius:15px; background:var(--video-panel-solid); padding:12px 14px; }
    .comment-item + .comment-item { margin-top:9px; }
    .comment-meta { display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:8px; color:var(--video-muted); font-size:12px; font-weight:650; }
    .comment-intent { min-height:23px; padding:3px 10px; color:#383838; font-size:11px; font-weight:900; }
    .comment-item h4 { margin-top:7px; font-family:var(--video-font-sans); font-size:15px; font-weight:900; }
    .comment-item p { margin:5px 0 0; font-family:var(--video-font-sans); font-size:13px; line-height:1.65; white-space:pre-wrap; }
    .comment-time { margin-top:7px; color:var(--video-muted); font-size:11px; }
    .suggestions-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:16px; margin-top:22px; }
    .suggestion-card { border-radius:16px; background:var(--video-panel-solid); padding:18px; }
    .suggestion-card p { margin:0; font-size:16px; }
    .warnings { border-color:#f0d6c8; background:#fff1ea; color:#ad4826; }
    .warnings ul { margin:16px 0 0; padding-left:20px; }
    .report-attribution-footer { border:0; background:transparent; color:var(--video-soft); font-family:var(--video-font-serif); font-size:16px; font-style:italic; letter-spacing:.12em; line-height:1.75; text-align:center; }
    @media (max-width:1100px) {
      main { width:min(1450px,calc(100vw - 28px)); margin:14px auto 28px; }
      .hero-grid,.split-grid,.comment-grid { grid-template-columns:1fr; }
      .cover { min-height:0; }
      .cover img { max-height:460px; object-fit:contain; }
      .metrics-grid,.script-grid,.suggestions-grid,.comment-subgrid { grid-template-columns:repeat(2,minmax(0,1fr)); }
      .timeline-item { grid-template-columns:1fr; }
      h1 { font-size:36px; }
      .summary { font-size:22px; }
    }
    @media (max-width:680px) {
      main { width:calc(100vw - 24px); margin:12px auto 24px; }
      .metrics-grid,.script-grid,.suggestions-grid,.comment-subgrid { grid-template-columns:1fr; }
      .hero-card,.panel { padding:20px; }
      h1 { font-size:clamp(30px,9vw,36px); }
      .summary { font-size:20px; }
    }
    """

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(video.get('title'))} - HotBee 抖音视频拆解报告</title>
  <style>{styles}</style>
</head>
<body><main><div class="video-report">
  <div class="hero-grid">
    <div class="cover">{f'<img src="{esc(cover_file)}" alt="{esc(video.get("title"))}" />' if cover_file else '<div class="cover-empty">暂无封面</div>'}</div>
    <div class="hero-card">
      <div class="heading-row"><div class="kicker">视频解析</div><span class="pill">{esc(platform_label)}</span><span class="pill">{esc(video.get('duration') or '--')}</span></div>
      <h1>{esc(video.get('title'))}</h1>
      <p class="summary">{esc(report['summary'])}</p>
      <div class="hotwords">{"".join(f'<span class="hotword">{esc(word)}</span>' for word in report['hotWords'][:6])}</div>
    </div>
  </div>

  <div class="metrics-grid">
    {render_primary_metric("播放量", video.get("playCount"))}
    {render_primary_metric("点赞", video.get("likeCount"))}
    {render_primary_metric("评论", video.get("commentCount"))}
    {render_primary_metric("分享", video.get("shareCount"))}
  </div>
  <div class="metrics-grid">
    {render_metric("点赞率", format_percent(video.get("likeCount"), video.get("playCount")), f"点赞 {format_metric(video.get('likeCount'))} / 播放 {format_metric(video.get('playCount'))}")}
    {render_metric("收藏 / 点赞", format_ratio(video.get("collectCount"), video.get("likeCount")), "高于 1 时更偏工具型或资料型内容")}
    {render_metric("分享 / 评论", format_ratio(video.get("shareCount"), video.get("commentCount")), "越高越像可转发的安利内容")}
    {render_metric("评论密度", format_percent(video.get("commentCount"), video.get("playCount")), f"评论 {format_metric(video.get('commentCount'))}，看互动承接")}
  </div>

  <div class="split-grid">
    <section class="panel">
      {render_section_title("开场语定位")}
      <div class="inner-card" style="margin-top:22px"><div class="hook-label">开场钩子</div><p>{esc(report['hook'])}</p></div>
      <div class="theme-list">{"".join(f'<div class="theme-card">{esc(item)}</div>' for item in report['themes'])}</div>
    </section>
    <section class="panel">
      {render_section_title("爆款要素")}
      <div class="viral-list">{"".join(f'<div class="viral-item"><span class="viral-index">{index + 1}</span><p>{esc(item)}</p></div>' for index, item in enumerate(report['viralFactors']))}</div>
    </section>
  </div>

  <section class="panel">
    {render_section_title("画面拆解")}
    <div class="timeline-list">{timeline_html}</div>
  </section>

  <section class="panel">
    {render_section_title("脚本拆解结构")}
    <div class="script-grid">{script_html}</div>
  </section>

  <section class="panel comment-section">
    {render_section_title("评论意图与热词", comment_desc)}
    <div class="comment-grid">
      <div class="comment-left">
        <div class="comment-panel"><div class="comment-panel-title">热词词云</div><div class="cloud-stage"><div class="comment-cloud-list">{cloud_html}</div></div></div>
        <div class="comment-subgrid">
          <div class="comment-panel"><div class="comment-panel-title">高频意图统计</div><div class="intent-list">{intent_html}</div></div>
          <div class="comment-panel"><div class="comment-panel-title">高频需求词</div><div class="keyword-list">{keyword_html}</div></div>
        </div>
      </div>
      <div class="comments-panel">
        <div class="comments-head"><div><div class="comment-panel-title">相关评论</div><p id="comments-active-label">全部评论</p></div><span id="comments-count" class="comments-count keyword-chip">{esc(format_metric(comment_total))} 条</span></div>
        <div class="comments-filter"><button type="button" class="keyword-chip is-active" data-comment-filter-type="all" data-comment-filter-value="">全部评论 · {esc(format_metric(comment_total))}</button></div>
        <div id="comments-list" class="comments-list">{comments_html}</div>
      </div>
    </div>
  </section>

  <section class="panel">
    {render_section_title("优化建议")}
    <div class="suggestions-grid">{"".join(f'<div class="suggestion-card"><p>{esc(item)}</p></div>' for item in report['suggestions'])}</div>
  </section>
  {f'<section class="panel warnings">{render_section_title("本次警告")}<ul>{warning_html}</ul></section>' if warnings else ''}
  <footer class="report-attribution-footer">拆解洞察来自 HotBee.cn | 社媒公开数据采集与内容分析</footer>
  <script id="hotbee-comments-data" type="application/json">{comments_json}</script>
  <script>
  (() => {{
    const dataNode = document.getElementById("hotbee-comments-data");
    const listNode = document.getElementById("comments-list");
    const labelNode = document.getElementById("comments-active-label");
    const countNode = document.getElementById("comments-count");
    const buttons = Array.from(document.querySelectorAll("[data-comment-filter-type]"));
    if (!dataNode || !listNode || !labelNode || !countNode) return;

    let comments = [];
    try {{
      comments = JSON.parse(dataNode.textContent || "[]");
    }} catch (error) {{
      comments = [];
    }}

    const formatMetric = (value) => {{
      const number = Number(value);
      if (!Number.isFinite(number)) return String(value ?? "--");
      if (number >= 10000) return (number / 10000).toFixed(1).replace(".0", "") + "万";
      return String(Math.round(number));
    }};

    const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => {{
      if (char === "&") return "&amp;";
      if (char === "<") return "&lt;";
      if (char === ">") return "&gt;";
      if (char === '"') return "&quot;";
      return "&#39;";
    }});

    const matchComment = (comment, type, value) => {{
      if (type === "all") return true;
      const keyword = String(value || "").trim().toLowerCase();
      if (!keyword) return true;
      if (type === "intent") return String(comment.intent || "").trim() === value;
      const text = [comment.text, comment.author].map((item) => String(item || "").toLowerCase()).join(" ");
      return text.includes(keyword);
    }};

    const renderCard = (comment) => `
      <article class="comment-item">
        <div class="comment-meta"><span class="comment-intent">${{escapeHtml(comment.intent)}}</span><span>${{escapeHtml(comment.location)}} · 赞 ${{escapeHtml(formatMetric(comment.likeCount))}}</span></div>
        <h4>${{escapeHtml(comment.author)}}</h4>
        <p>${{escapeHtml(comment.text)}}</p>
        <div class="comment-time">${{escapeHtml(comment.time)}}</div>
      </article>
    `;

    const setActiveButton = (activeType, activeValue) => {{
      buttons.forEach((button) => {{
        const sameType = button.dataset.commentFilterType === activeType;
        const sameValue = (button.dataset.commentFilterValue || "") === activeValue;
        button.classList.toggle("is-active", sameType && sameValue);
      }});
    }};

    const renderComments = (type, value) => {{
      const filtered = comments.filter((comment) => matchComment(comment, type, value));
      const label = type === "all" ? "全部评论" : `匹配“${{value}}”的评论`;
      labelNode.textContent = label;
      countNode.textContent = `${{formatMetric(filtered.length)}} 条`;
      listNode.innerHTML = filtered.length
        ? filtered.map(renderCard).join("")
        : `<div class="comment-empty">当前词没有匹配评论，点击其他热词查看。</div>`;
      setActiveButton(type, value || "");
    }};

    buttons.forEach((button) => {{
      button.addEventListener("click", () => {{
        renderComments(button.dataset.commentFilterType || "all", button.dataset.commentFilterValue || "");
      }});
    }});
  }})();
  </script>
</div></main></body></html>
"""


def svg_text_lines(text: str, width: int = 24, max_lines: int = 5) -> list[str]:
    text = re.sub(r"\s+", " ", text or "").strip()
    if not text:
        return []
    wrapped = textwrap.wrap(text, width=width, break_long_words=True, replace_whitespace=False)
    lines = wrapped[:max_lines]
    if lines and len(wrapped) > max_lines:
        lines[-1] = lines[-1].rstrip("。,.，") + "..."
    return lines


def render_report_card_svg(path: Path, video: dict[str, Any], report: dict[str, Any], comments: list[dict[str, Any]]) -> None:
    title_lines = svg_text_lines(str(video.get("title") or ""), width=20, max_lines=3)
    summary_lines = svg_text_lines(report["summary"], width=28, max_lines=5)
    hook_lines = svg_text_lines(report["hook"], width=28, max_lines=4)
    top_comment = comments[0]["text"] if comments else "暂无评论样本"
    comment_lines = svg_text_lines(top_comment, width=30, max_lines=4)

    def tspan(lines: list[str], x: int, y: int, size: int, fill: str = "#172136", weight: int = 700) -> str:
        return "\n".join(f'<text x="{x}" y="{y + index * size * 1.35}" font-size="{size}" font-weight="{weight}" fill="{fill}">{esc(line)}</text>' for index, line in enumerate(lines))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1440" viewBox="0 0 1080 1440">
  <rect width="1080" height="1440" fill="#f2eee6"/>
  <rect x="60" y="60" width="960" height="1320" rx="36" fill="#ffffff" stroke="#dde7f5"/>
  <rect x="96" y="96" width="888" height="332" rx="32" fill="#fcf6ee"/>
  <text x="132" y="156" font-size="30" font-weight="900" fill="#dd5a2b">HotBee 抖音视频拆解</text>
  {tspan(title_lines, 132, 222, 48, "#241a14", 900)}
  <g transform="translate(132 474)">
    <rect width="178" height="110" rx="20" fill="#f8fbff" stroke="#dde7f5"/><text x="24" y="42" font-size="22" font-weight="700" fill="#667489">播放</text><text x="24" y="84" font-size="34" font-weight="900" fill="#172136">{esc(format_metric(video.get("playCount")))}</text>
    <rect x="202" width="178" height="110" rx="20" fill="#f8fbff" stroke="#dde7f5"/><text x="226" y="42" font-size="22" font-weight="700" fill="#667489">点赞</text><text x="226" y="84" font-size="34" font-weight="900" fill="#172136">{esc(format_metric(video.get("likeCount")))}</text>
    <rect x="404" width="178" height="110" rx="20" fill="#f8fbff" stroke="#dde7f5"/><text x="428" y="42" font-size="22" font-weight="700" fill="#667489">评论</text><text x="428" y="84" font-size="34" font-weight="900" fill="#172136">{esc(format_metric(video.get("commentCount")))}</text>
    <rect x="606" width="178" height="110" rx="20" fill="#f8fbff" stroke="#dde7f5"/><text x="630" y="42" font-size="22" font-weight="700" fill="#667489">分享</text><text x="630" y="84" font-size="34" font-weight="900" fill="#172136">{esc(format_metric(video.get("shareCount")))}</text>
  </g>
  <text x="132" y="672" font-size="30" font-weight="900" fill="#172136">核心摘要</text>
  {tspan(summary_lines, 132, 724, 30, "#273140", 600)}
  <rect x="96" y="900" width="888" height="210" rx="28" fill="#f8fbff" stroke="#dde7f5"/>
  <text x="132" y="960" font-size="30" font-weight="900" fill="#172136">开场抓手</text>
  {tspan(hook_lines, 132, 1012, 28, "#273140", 600)}
  <rect x="96" y="1150" width="888" height="170" rx="28" fill="#fcf6ee" stroke="#e9dfd2"/>
  <text x="132" y="1210" font-size="30" font-weight="900" fill="#172136">评论信号</text>
  {tspan(comment_lines, 132, 1260, 26, "#3a2d24", 600)}
  <text x="132" y="1350" font-size="20" font-weight="700" fill="#667489">HTML、评论 CSV、文案 MD 与原始 JSON 已同步落盘</text>
</svg>
"""
    write_text(path, svg)


def build_manifest(
    args: argparse.Namespace,
    out_dir: Path,
    video: dict[str, Any],
    media: list[dict[str, str]],
    warnings: list[str],
    endpoint: str,
    transcript_source: str,
    metric_sources: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "input_url": args.url,
        "resolved_url": video.get("resolvedUrl"),
        "base_url": args.base_url,
        "video_info_endpoint": endpoint,
        "metric_sources": metric_sources or {},
        "transcript_source": transcript_source,
        "max_comments": args.max_comments,
        "warnings": warnings,
        "video": video,
        "media": media,
        "artifacts": {
            "html_report": str(out_dir / "report.html"),
            "report_card_svg": str(out_dir / "images" / "report-card.svg"),
            "breakdown_markdown": str(out_dir / "breakdown.md"),
            "transcript_markdown": str(out_dir / "transcript.md"),
            "transcript_raw": str(out_dir / "transcript_raw.txt"),
            "comments_csv": str(out_dir / "comments.csv"),
            "comments_json": str(out_dir / "comments.json"),
            "video_json": str(out_dir / "video.json"),
            "raw_dir": str(out_dir / "raw"),
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="输入抖音视频链接，生成 HotBee HTML 视频拆解报告。")
    parser.add_argument("--url", required=True, help="抖音视频链接或包含链接的分享文本。")
    parser.add_argument("--output-dir", default="output/hotbee-douyin-video-report", help="输出根目录，脚本会自动创建时间戳子目录。")
    parser.add_argument("--base-url", default=os.environ.get("HOTBEE_API_BASE", DEFAULT_BASE_URL), help="HotBee API Base URL。")
    parser.add_argument("--max-comments", type=int, default=100, help="最多保存评论条数，默认 100。")
    parser.add_argument("--skip-transcript", action="store_true", help="跳过音视频转文案。")
    parser.add_argument("--skip-comments", action="store_true", help="跳过评论采集。")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    args.base_url = validate_base_url(args.base_url)
    key = hotbee_api_key()
    output_root = Path(args.output_dir).expanduser()
    out_dir = output_root / now_slug()
    raw_dir = out_dir / "raw"
    images_dir = out_dir / "images"
    warnings: list[str] = []
    raw_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)

    raw_url = first_http_url(args.url)
    if not is_douyin_url(raw_url):
        raise SystemExit("输入中未找到抖音链接。")

    resolved_url = resolve_douyin_url(raw_url, args.base_url, raw_dir, warnings)
    video, endpoint, metric_sources = fetch_video_info(args.base_url, resolved_url, key, raw_dir)
    video["inputUrl"] = raw_url
    video["resolvedUrl"] = resolved_url
    hydrate_play_count_from_cache(output_root, out_dir, video, metric_sources, warnings)
    write_json(out_dir / "video.json", video)

    transcript = ""
    transcript_source = ""
    if not args.skip_transcript:
        transcript, transcript_source = fetch_transcript(args.base_url, video, raw_url, resolved_url, key, raw_dir, warnings)
    write_text(out_dir / "transcript_raw.txt", transcript)
    transcript_md = "\n".join(split_transcript_sentences(transcript)) if transcript else "（本次没有可用文案）"
    write_text(out_dir / "transcript.md", transcript_md.strip() + "\n")

    comments: list[dict[str, Any]] = []
    if not args.skip_comments:
        comments = fetch_comments(args.base_url, video, raw_url, resolved_url, key, args.max_comments, raw_dir, warnings)
    write_json(out_dir / "comments.json", comments)
    write_comments_csv(out_dir / "comments.csv", comments)

    media = download_images(video, images_dir, warnings)
    report = build_report_model(video, transcript, comments)
    breakdown = build_breakdown_markdown(video, report, comments)
    write_text(out_dir / "breakdown.md", breakdown)
    write_json(out_dir / "report_data.json", {"video": video, "report": report, "comments": comments, "media": media, "warnings": warnings})

    render_report_card_svg(images_dir / "report-card.svg", video, report, comments)
    media.append({"label": "报告卡片", "url": "", "file": "images/report-card.svg"})
    write_text(out_dir / "report.html", render_html(video, report, transcript, comments, media, warnings))
    write_json(out_dir / "run_manifest.json", build_manifest(args, out_dir, video, media, warnings, endpoint, transcript_source, metric_sources))

    print(json.dumps({
        "ok": True,
        "output_dir": str(out_dir),
        "html_report": str(out_dir / "report.html"),
        "report_card_svg": str(images_dir / "report-card.svg"),
        "comments_count": len(comments),
        "transcript_chars": len(transcript),
        "warnings": warnings,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
