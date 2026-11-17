#!/usr/bin/env python3
"""Read-only CLI for the public M5Burner firmware catalog."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from http.client import HTTPException
from typing import Any, Iterable, Mapping, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = os.environ.get(
    "M5BURNER_API_BASE_URL", "https://burner.m5stack.com"
).rstrip("/")
USER_AGENT = "m5stack-firmware-query/1.0"
SORT_VALUES = ("LATEST", "MOST_DOWNLOADED", "MOST_LIKED")

BASELINE_NAME_PATTERNS = (
    "userdemo",
    "demo",
    "test",
    "esp32-c6 wi-fi sdio",
    "esp-hosted firmware upgrade",
)


class ApiError(RuntimeError):
    """An HTTP, API-envelope, or local query error."""

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        payload: Any = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.payload = payload

    @property
    def request_id(self) -> str | None:
        if isinstance(self.payload, Mapping):
            value = self.payload.get("requestId")
            return str(value) if value else None
        return None


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def bounded_int(maximum: int):
    def parse(value: str) -> int:
        parsed = positive_int(value)
        if parsed > maximum:
            raise argparse.ArgumentTypeError(f"must be no greater than {maximum}")
        return parsed

    return parse


def compact_params(params: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in params.items()
        if value is not None and value != ""
    }


def json_payload(raw: bytes) -> Any:
    try:
        return json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ApiError("服务器返回的内容不是有效 JSON") from exc


def payload_message(payload: Any) -> str | None:
    if not isinstance(payload, Mapping):
        return None
    for key in ("msg", "message", "error"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    data = payload.get("data")
    if isinstance(data, Mapping):
        value = data.get("errorCode")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


class FirmwareApi:
    def __init__(self, base_url: str, timeout: int) -> None:
        base_url = base_url.strip().rstrip("/")
        if not base_url.startswith(("http://", "https://")):
            raise ApiError("base URL must start with http:// or https://")
        self.base_url = base_url
        self.timeout = timeout

    def get(
        self,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        query = urlencode(compact_params(params or {}))
        url = f"{self.base_url}/{path.lstrip('/')}"
        if query:
            url = f"{url}?{query}"
        request_headers = {
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        }
        request_headers.update(headers or {})
        request = Request(url, headers=request_headers, method="GET")

        try:
            with urlopen(request, timeout=self.timeout) as response:
                raw = response.read()
                status = response.status
        except HTTPError as exc:
            raw = exc.read()
            try:
                payload = json_payload(raw)
            except ApiError:
                payload = None
            message = payload_message(payload) or f"HTTP {exc.code}"
            raise ApiError(message, status=exc.code, payload=payload) from exc
        except (URLError, TimeoutError, HTTPException, OSError) as exc:
            reason = getattr(exc, "reason", None) or str(exc)
            raise ApiError(f"网络请求失败: {reason}") from exc

        if status < 200 or status >= 300:
            raise ApiError(f"HTTP {status}", status=status)
        payload = json_payload(raw)
        if isinstance(payload, Mapping):
            code = payload.get("code")
            if isinstance(code, int) and code >= 400:
                message = payload_message(payload) or f"API code {code}"
                raise ApiError(message, status=code, payload=payload)
        return payload


def list_data(payload: Any) -> list[Mapping[str, Any]]:
    if not isinstance(payload, Mapping):
        return []
    for key in ("rows", "data"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, Mapping)]
    return []


def object_data(payload: Any) -> Mapping[str, Any]:
    if isinstance(payload, Mapping) and isinstance(payload.get("data"), Mapping):
        return payload["data"]
    return {}


def as_mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def normalize(value: Any) -> str:
    return " ".join(str(value or "").replace("_", " ").replace("-", " ").split()).casefold()


def contains_any(haystack: str, terms: Iterable[str]) -> bool:
    for term in terms:
        normalized_term = normalize(term)
        if not normalized_term:
            continue
        if any(ord(char) > 127 for char in normalized_term):
            if normalized_term in haystack:
                return True
            continue
        if re.search(rf"(?<![a-z0-9]){re.escape(normalized_term)}(?![a-z0-9])", haystack):
            return True
    return False


def content_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, Mapping):
        content = value.get("content")
        return content_text(content) if content is not None else json.dumps(value, ensure_ascii=False)
    if not isinstance(value, str):
        return str(value)
    text = value.strip()
    if not text:
        return ""
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return text
    if isinstance(parsed, Mapping) and parsed.get("content") is not None:
        return content_text(parsed.get("content"))
    return content_text(parsed)


def clean_text(value: Any, *, maximum: int | None = None) -> str:
    text = " ".join(content_text(value).replace("\r", " ").replace("\n", " ").split())
    if maximum is not None and len(text) > maximum:
        return text[: maximum - 3] + "..."
    return text


def name_list(items: Any, key: str) -> list[str]:
    if not isinstance(items, list):
        return []
    return [
        str(item.get(key))
        for item in items
        if isinstance(item, Mapping) and item.get(key)
    ]


def parse_api_datetime(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def recency_points(value: Any) -> int:
    parsed = parse_api_datetime(value)
    if parsed is None:
        return 0
    now = datetime.now(parsed.tzinfo or timezone.utc)
    days = max((now - parsed).days, 0)
    if days <= 45:
        return 10
    if days <= 180:
        return 5
    return 0


def page_url(base_url: str, firmware_id: Any) -> str:
    return f"{base_url.rstrip('/')}/firmware/{quote(str(firmware_id), safe='')}"


def firmware_record(
    item: Mapping[str, Any],
    base_url: str,
    *,
    description_limit: int | None = 1200,
) -> dict[str, Any]:
    version = as_mapping(item.get("currentVersion"))
    stats = as_mapping(item.get("statistics"))
    firmware_id = item.get("firmwareId")
    return {
        "firmwareId": firmware_id,
        "firmwareName": item.get("firmwareName"),
        "versionName": version.get("versionName"),
        "versionId": version.get("versionId"),
        "versionStatus": version.get("status"),
        "publishTime": version.get("publishTime") or item.get("uploadedAt"),
        "sourceType": item.get("sourceType"),
        "sourceUrl": item.get("sourceUrl"),
        "pageUrl": page_url(base_url, firmware_id) if firmware_id else None,
        "categories": name_list(item.get("categories"), "categoryName"),
        "devices": name_list(item.get("supportedDevices"), "deviceName"),
        "downloadCount": stats.get("downloadCount") or 0,
        "likeCount": stats.get("likeCount") or 0,
        "commentCount": stats.get("commentCount") or 0,
        "description": clean_text(
            item.get("firmwareDescription"), maximum=description_limit
        ),
        "versionDescription": clean_text(
            version.get("versionDescription"), maximum=description_limit
        ),
    }


def firmware_analysis_record(
    item: Mapping[str, Any], base_url: str
) -> dict[str, Any]:
    """Keep output compact while giving classifiers the complete public text."""
    return firmware_record(item, base_url, description_limit=None)


AI_FEATURE_TERMS = (
    "artificial intelligence",
    "ai assistant",
    "ai chat",
    "ai chatbot",
    "ai agent",
    "chatbot",
    "chat bot",
    "chat capabilities",
    "language model",
    "large language",
    "local llm",
    "offline llm",
    "on-device llm",
    "on device llm",
    "llm",
    "gemini api",
    "gemini ai",
    "gemini",
    "ollama",
    "groq chatbot",
    "groq chat",
    "groq whisper",
    "whisper transcription",
    "xiaozhi core",
    "voice assistant",
    "text to speech",
    "speech to text",
    "tts playback",
    "react agent",
    "machine learning",
    "neural network",
    "model personality",
    "model/personality",
    "chat with a llm",
    "人工智能",
    "大语言模型",
    "语言模型",
    "聊天机器人",
    "语音助手",
    "本地模型",
    "离线大模型",
    "智能助手",
    "智能体",
    "语音转写",
    "文本转语音",
)

AI_NAME_TERMS = (
    "ai",
    "chatgpt",
    "gemini",
    "ollama",
    "groqputer",
    "xiaozhi",
    "小智",
    "m5claw",
    "claude desktop",
)

AI_AUTHORING_ONLY_TERMS = (
    "made with claude",
    "made with chatgpt",
    "created with claude",
    "written by chatgpt",
    "code was written by chatgpt",
    "modified by chatgpt",
)


def matched_terms(haystack: str, terms: Iterable[str]) -> list[str]:
    return [term for term in terms if contains_any(haystack, (term,))]


def classify_intent(record: Mapping[str, Any], intent: str) -> dict[str, Any]:
    """Classify a catalog record using its functional description, not only tags."""
    if intent != "ai":
        raise ApiError(f"不支持的查询意图: {intent}")

    name = normalize(record.get("firmwareName"))
    content = normalize(
        " ".join(
            [
                str(record.get("firmwareName") or ""),
                str(record.get("description") or ""),
                str(record.get("versionDescription") or ""),
            ]
        )
    )
    feature_signals = matched_terms(content, AI_FEATURE_TERMS)
    name_signals = matched_terms(name, AI_NAME_TERMS)
    authoring_signals = matched_terms(content, AI_AUTHORING_ONLY_TERMS)
    category_signal = "AI & Assistants" in [
        str(value) for value in record.get("categories") or []
    ]

    if feature_signals or name_signals:
        signals = [*name_signals, *feature_signals]
        confidence = "high" if feature_signals and (name_signals or len(feature_signals) >= 2) else "medium"
        return {
            "matched": True,
            "confidence": confidence,
            "signals": signals[:8],
            "reason": "名称或功能描述显示这是 AI/语音/大模型项目",
        }

    if authoring_signals:
        reason = "只提到项目由 ChatGPT/Claude 辅助编写，没有发现固件提供 AI 功能"
    elif category_signal:
        reason = "仓库分类标为 AI，但名称和功能描述没有发现 AI 功能信号"
    else:
        reason = "名称和功能描述没有发现 AI 功能信号"
    return {
        "matched": False,
        "confidence": "none",
        "signals": authoring_signals[:4],
        "reason": reason,
    }


def merge_record(base: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in update.items():
        if value not in (None, "", [], {}):
            merged[key] = value
    return merged


def recommendation_profile(record: Mapping[str, Any], *, include_baseline: bool) -> dict[str, Any]:
    name = str(record.get("firmwareName") or "")
    categories = [str(value) for value in record.get("categories") or []]
    haystack = normalize(
        " ".join(
            [
                name,
                " ".join(categories),
                str(record.get("description") or ""),
                str(record.get("versionDescription") or ""),
            ]
        )
    )
    downloads = int(record.get("downloadCount") or 0)
    likes = int(record.get("likeCount") or 0)
    base_score = min(downloads // 100, 35) + min(likes * 8, 24) + recency_points(record.get("publishTime"))
    features: list[tuple[str, int, str]] = []
    source_reason: str | None = None
    needs: list[str] = []

    def add(kind: str, points: int, reason: str) -> None:
        if not any(existing_kind == kind for existing_kind, _points, _reason in features):
            features.append((kind, points, reason))

    if "Audio & Media" in categories or contains_any(
        haystack,
        ("music", "synth", "sequencer", "recorder", "midi", "wav", "mp3", "音乐", "录音"),
    ):
        add("音乐/媒体", 18, "声音、录音、合成器或媒体玩法明确")
    ai_classification = classify_intent(record, "ai")
    if ai_classification["matched"]:
        add("AI/语音", 18, "功能描述明确包含 AI、语音或大模型交互")
    elif "AI & Assistants" in categories:
        add("AI/语音", 4, "仓库分类标为 AI，但功能描述信号不足")
    if "UI & Launcher" in categories or "launcher" in haystack:
        add("启动器", 20, "适合管理和切换多个固件")
    if "Games" in categories or contains_any(haystack, ("game", "emulator", "chess", "tetris", "reversi", "pong", "模拟器", "仙剑")):
        add("游戏/模拟器", 18, "游戏或模拟器属性明确")
    if contains_any(haystack, ("ssh", "vt100", "micropython", "shell", "scp")):
        add("开发终端", 18, "能把设备当终端或脚本环境使用")
    if contains_any(haystack, ("uvc", "screen streamer", "capture", "hdmi")):
        add("显示/采集", 16, "能扩展成显示、采集或串流工具")
    if contains_any(haystack, ("clock", "weather", "matrix", "dashboard", "gpsdo", "ntp", "moon", "月相", "时钟")):
        add("桌面信息屏", 14, "适合长期摆桌面显示状态信息")
    if "Network & Communication" in categories or contains_any(
        haystack,
        ("wi-fi", "wifi", "recon", "hid", "rf", "gnss", "gps", "uart", "bluetooth"),
    ):
        add("网络/硬件", 12, "偏硬件、网络或外设实验")
    if record.get("sourceUrl"):
        base_score += 4
        source_reason = "有源码或项目链接，方便确认用法"

    lowered_name = normalize(name)
    baseline = any(pattern in lowered_name for pattern in BASELINE_NAME_PATTERNS)
    if baseline and not include_baseline:
        base_score -= 28

    def add_need(value: str) -> None:
        if value not in needs:
            needs.append(value)

    sd_signal = contains_any(
        haystack,
        ("sd card", "micro sd", "microsd", "sd卡", "sd 卡", "/sd/", "/pal", "/roms"),
    )
    sd_required = contains_any(
        haystack,
        (
            "insert sd card",
            "sd card is required",
            "required on first boot",
            "fat32-formatted sd",
            "must download",
        ),
    )
    if sd_signal:
        add_need(
            "需要准备 microSD/SD 卡"
            if sd_required
            else "可能需要准备 microSD/SD 卡"
        )
    if contains_any(haystack, ("rom", "macintosh", "classic mac", "pal", "仙剑", ".nes", "游戏资源")):
        add_need("需要自备合法 ROM/游戏资源")
    if contains_any(
        haystack,
        ("external keyboard", "usb keyboard", "bluetooth keyboard", "外接键盘", "外部键盘"),
    ):
        add_need("外接键盘可能会明显提升体验")
    if contains_any(haystack, ("gemini",)):
        add_need("需要配置 Gemini API Key")
    elif contains_any(
        haystack, ("set mimo key", "model service", "openai-compatible")
    ):
        add_need("需要配置模型服务凭据")
    elif not contains_any(haystack, ("groq", "ollama")) and contains_any(
        haystack, ("api key", "openweathermap")
    ):
        add_need("需要配置第三方 API Key")
    if contains_any(haystack, ("groq",)):
        add_need("需要配置 Groq API Key")
    if contains_any(haystack, ("ollama",)):
        add_need("需要可访问的 Ollama 服务")
    network_signal = contains_any(
        haystack, ("wi-fi", "wifi", "captive portal", "setup ap", "联网", "network")
    )
    remote_ai_signal = contains_any(
        haystack, ("gemini", "groq", "ollama", "api key")
    )
    offline_ai_signal = contains_any(
        haystack, ("offline llm", "on-device offline llm", "本地模型", "离线大模型")
    )
    if ai_classification["matched"] and (network_signal or remote_ai_signal):
        add_need(
            "部分功能需要 Wi-Fi/网络连接"
            if offline_ai_signal and not remote_ai_signal
            else "需要 Wi-Fi/网络连接"
        )
    if contains_any(haystack, ("serial", "115200 baud")):
        add_need("首次配置可能需要通过串口")
    if contains_any(haystack, ("xiaozhi", "小智")):
        add_need("语音助手功能可能需要联网或平台绑定")
    if contains_any(haystack, ("model.bin", "model bin")):
        add_need("需要按项目说明准备模型文件")
    if contains_any(haystack, ("uvc", "capture", "hdmi", "gpsdo", "gnss", "rf", "gamepad", "usb")):
        add_need("可能需要对应外设/模块")

    selected_features = sorted(features, key=lambda item: item[1], reverse=True)[:3]
    score = base_score + sum(points for _kind, points, _reason in selected_features)
    kinds = [kind for kind, _points, _reason in selected_features]
    reasons = [reason for _kind, _points, reason in selected_features]
    if source_reason:
        reasons.append(source_reason)
    if baseline and not include_baseline:
        reasons.append("偏官方演示、底层组件或测试固件，默认降权")
    if not reasons:
        reasons.append("分类或描述较少，需打开详情页进一步确认")

    return {
        "score": score,
        "kind": " / ".join(kinds) if kinds else "待确认",
        "why": "；".join(reasons[:3]),
        "needs": needs,
        "baseline": baseline,
    }


def resolve_catalog_id(
    items: Iterable[Mapping[str, Any]],
    value: str,
    *,
    id_keys: Sequence[str],
    name_keys: Sequence[str],
    label: str,
) -> str:
    needle = normalize(value)
    exact: list[Mapping[str, Any]] = []
    for item in items:
        candidates = [item.get(key) for key in (*id_keys, *name_keys)]
        if any(normalize(candidate) == needle for candidate in candidates):
            exact.append(item)
    if len(exact) == 1:
        for key in id_keys:
            if exact[0].get(key):
                return str(exact[0][key])
    if len(exact) > 1:
        names = ", ".join(
            str(item.get(name_keys[0]) or item.get(id_keys[0]))
            for item in exact[:5]
        )
        raise ApiError(f"{label}匹配到多个结果: {names}")
    suggestions = [
        str(item.get(name_keys[0]) or item.get(id_keys[0]))
        for item in items
        if needle in normalize(item.get(name_keys[0]))
    ]
    suffix = f"。可选值: {', '.join(suggestions[:5])}" if suggestions else ""
    raise ApiError(f"未找到{label}: {value}{suffix}")


def resolve_device_id(api: FirmwareApi, value: str) -> str:
    payload = api.get("/api/v1/devices")
    return resolve_catalog_id(
        list_data(payload),
        value,
        id_keys=("deviceId",),
        name_keys=("deviceName", "deviceCode", "deviceSlug"),
        label="设备",
    )


def resolve_category_id(api: FirmwareApi, value: str, language: str) -> str:
    payload = api.get(
        "/api/v1/firmware-categories",
        headers={"language": language},
    )
    return resolve_catalog_id(
        list_data(payload),
        value,
        id_keys=("categoryId",),
        name_keys=("categoryName", "categoryCode"),
        label="分类",
    )


def command_search(api: FirmwareApi, args: argparse.Namespace) -> Any:
    device_id = args.device_id or (
        resolve_device_id(api, args.device_name) if args.device_name else None
    )
    category_id = args.category_id or (
        resolve_category_id(api, args.category_name, args.language)
        if args.category_name
        else None
    )
    return api.get(
        "/api/v1/firmwares",
        params={
            "keyword": args.keyword,
            "categoryId": category_id,
            "deviceId": device_id,
            "sort": args.sort,
            "pageNum": args.page,
            "pageSize": args.page_size,
        },
    )


def fetch_all_firmware_rows(
    api: FirmwareApi,
    *,
    params: Mapping[str, Any],
    page_size: int,
) -> tuple[list[Mapping[str, Any]], int, bool]:
    """Fetch every page when the API reports a total; return rows, total, truncated."""
    rows: list[Mapping[str, Any]] = []
    reported_total: int | None = None
    page = 1

    while page <= 100:
        payload = api.get(
            "/api/v1/firmwares",
            params={**params, "pageNum": page, "pageSize": page_size},
        )
        page_rows = list_data(payload)
        rows.extend(page_rows)
        if isinstance(payload, Mapping) and isinstance(payload.get("total"), int):
            reported_total = int(payload["total"])
        if not page_rows:
            break
        if reported_total is not None and len(rows) >= reported_total:
            break
        if reported_total is None and len(page_rows) < page_size:
            break
        page += 1

    total = reported_total if reported_total is not None else len(rows)
    return rows, total, reported_total is not None and len(rows) < reported_total


def command_intent_search(api: FirmwareApi, args: argparse.Namespace) -> Any:
    device_id = args.device_id or (
        resolve_device_id(api, args.device_name) if args.device_name else None
    )
    device_info: Mapping[str, Any] = {}
    if device_id:
        if args.device_name:
            device_info = {"deviceId": device_id, "deviceName": args.device_name}
        else:
            devices = list_data(api.get("/api/v1/devices"))
            device_info = next(
                (
                    item
                    for item in devices
                    if str(item.get("deviceId")) == str(device_id)
                ),
                {"deviceId": device_id},
            )
    category_id = args.category_id or (
        resolve_category_id(api, args.category_name, args.language)
        if args.category_name
        else None
    )
    rows, total, truncated = fetch_all_firmware_rows(
        api,
        params={
            "keyword": args.keyword,
            "categoryId": category_id,
            "deviceId": device_id,
            "sort": args.sort,
        },
        page_size=args.page_size,
    )

    matches: list[dict[str, Any]] = []
    notable_exclusions: list[dict[str, Any]] = []
    category_candidate_total = 0
    for item in rows:
        record = firmware_record(item, api.base_url)
        analysis_record = firmware_analysis_record(item, api.base_url)
        classification = classify_intent(analysis_record, args.intent)
        category_signal = "AI & Assistants" in record["categories"]
        if category_signal:
            category_candidate_total += 1
        if classification["matched"]:
            record["intent"] = classification
            profile = recommendation_profile(analysis_record, include_baseline=True)
            record["prerequisites"] = profile["needs"]
            matches.append(record)
        elif category_signal or classification["signals"]:
            notable_exclusions.append(
                {
                    "firmwareId": record.get("firmwareId"),
                    "firmwareName": record.get("firmwareName"),
                    "reason": classification["reason"],
                }
            )

    detail_errors: list[dict[str, Any]] = []
    for record in matches[: args.detail_limit]:
        firmware_id = record.get("firmwareId")
        if not firmware_id:
            continue
        try:
            detail_payload = api.get(
                f"/api/v1/firmwares/{quote(str(firmware_id), safe='')}"
            )
        except ApiError as exc:
            detail_errors.append(
                {
                    "firmwareId": firmware_id,
                    "error": str(exc),
                    "status": exc.status,
                    "requestId": exc.request_id,
                }
            )
            continue
        detail = object_data(detail_payload)
        if detail:
            enriched = firmware_record(detail, api.base_url)
            analysis_enriched = firmware_analysis_record(detail, api.base_url)
            enriched["intent"] = classify_intent(analysis_enriched, args.intent)
            enriched["prerequisites"] = recommendation_profile(
                analysis_enriched, include_baseline=True
            )["needs"]
            record.update(
                {
                    key: value
                    for key, value in enriched.items()
                    if value not in (None, "", [], {})
                }
            )

    warnings: list[str] = [
        "Functional intent matching is heuristic; ambiguous projects may need manual detail review."
    ]
    if truncated:
        warnings.append(
            f"API reported {total} candidates but only {len(rows)} records were returned."
        )
    if len(matches) > args.detail_limit:
        warnings.append(
            f"Only enriched the first {args.detail_limit} matched records with detail requests."
        )
    if len(notable_exclusions) > args.excluded_limit:
        warnings.append(
            f"Only returned the first {args.excluded_limit} notable exclusions."
        )
    if detail_errors:
        warnings.append("Some matched records could not be enriched from their detail pages.")

    return {
        "code": 200,
        "msg": "意图查询成功",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "intent": args.intent,
        "device": device_info,
        "deviceId": device_id,
        "categoryId": category_id,
        "sort": args.sort,
        "candidateTotal": total,
        "candidateReturned": len(rows),
        "categoryCandidateTotal": category_candidate_total,
        "matchedTotal": len(matches),
        "results": matches,
        "excludedTotal": len(rows) - len(matches),
        "notableExclusions": notable_exclusions[: args.excluded_limit],
        "notableExclusionTotal": len(notable_exclusions),
        "detailErrors": detail_errors,
        "warnings": warnings,
    }


def command_detail(api: FirmwareApi, args: argparse.Namespace) -> Any:
    firmware_id = quote(args.firmware_id, safe="")
    return api.get(f"/api/v1/firmwares/{firmware_id}")


def command_versions(api: FirmwareApi, args: argparse.Namespace) -> Any:
    firmware_id = quote(args.firmware_id, safe="")
    return api.get(
        f"/api/v1/firmwares/{firmware_id}/versions",
        params={"scope": args.scope},
    )


def command_devices(api: FirmwareApi, args: argparse.Namespace) -> Any:
    return api.get("/api/v1/devices", params={"developerId": args.developer_id})


def command_device_by_slug(api: FirmwareApi, args: argparse.Namespace) -> Any:
    slug = quote(args.slug, safe="")
    return api.get(f"/api/v1/devices/by-slug/{slug}")


def command_categories(api: FirmwareApi, args: argparse.Namespace) -> Any:
    return api.get(
        "/api/v1/firmware-categories",
        params={
            "deviceId": args.device_id,
            "developerUserId": args.developer_id,
        },
        headers={"language": args.language},
    )


def command_developers(api: FirmwareApi, args: argparse.Namespace) -> Any:
    return api.get(
        "/api/v1/developers",
        params={
            "keyword": args.keyword,
            "pageNum": args.page,
            "pageSize": args.page_size,
        },
    )


def command_developer(api: FirmwareApi, args: argparse.Namespace) -> Any:
    developer_id = quote(args.developer_id, safe="")
    return api.get(f"/api/v1/developers/{developer_id}")


def command_developer_firmwares(
    api: FirmwareApi, args: argparse.Namespace
) -> Any:
    developer_id = quote(args.developer_id, safe="")
    return api.get(
        f"/api/v1/developers/{developer_id}/firmwares",
        params={
            "keyword": args.keyword,
            "categoryId": args.category_id,
            "deviceId": args.device_id,
            "pageNum": args.page,
            "pageSize": args.page_size,
        },
    )


def command_uiflow2(api: FirmwareApi, args: argparse.Namespace) -> Any:
    return api.get("/api/v1/firmwares/uiflow2/latest")


def command_recommended(api: FirmwareApi, args: argparse.Namespace) -> Any:
    return api.get(
        "/api/v1/firmwares/recommended",
        params={"limit": args.limit},
    )


def command_ranking(api: FirmwareApi, args: argparse.Namespace) -> Any:
    route = (
        "/api/v1/firmwares/rankings/weekly"
        if args.kind == "weekly"
        else "/api/v1/firmwares/rankings/all-time"
    )
    return api.get(route, params={"limit": args.limit})


def command_comments(api: FirmwareApi, args: argparse.Namespace) -> Any:
    firmware_id = quote(args.firmware_id, safe="")
    return api.get(
        f"/api/v1/firmwares/{firmware_id}/comments",
        params={"pageNum": args.page, "pageSize": args.page_size},
    )


def command_recommend_device(api: FirmwareApi, args: argparse.Namespace) -> Any:
    devices_payload = api.get("/api/v1/devices")
    devices = list_data(devices_payload)
    device_id = args.device_id or resolve_catalog_id(
        devices,
        args.device_name,
        id_keys=("deviceId",),
        name_keys=("deviceName", "deviceCode", "deviceSlug"),
        label="设备",
    )
    device_info = next(
        (item for item in devices if str(item.get("deviceId")) == str(device_id)),
        {"deviceId": device_id},
    )

    merged: dict[str, dict[str, Any]] = {}
    totals: dict[str, int] = {}
    for sort_value in SORT_VALUES:
        payload = api.get(
            "/api/v1/firmwares",
            params={
                "deviceId": device_id,
                "sort": sort_value,
                "pageNum": 1,
                "pageSize": args.sample_size,
            },
        )
        if isinstance(payload, Mapping) and isinstance(payload.get("total"), int):
            totals[sort_value] = int(payload["total"])
        for item in list_data(payload):
            record = firmware_record(item, api.base_url)
            firmware_id = str(record.get("firmwareId") or "")
            if not firmware_id:
                continue
            record["seenInSorts"] = [sort_value]
            if firmware_id in merged:
                previous_sorts = merged[firmware_id].get("seenInSorts") or []
                record["seenInSorts"] = sorted(set([*previous_sorts, sort_value]))
                merged[firmware_id] = merge_record(merged[firmware_id], record)
            else:
                merged[firmware_id] = record

    for record in merged.values():
        record["recommendation"] = recommendation_profile(
            record,
            include_baseline=args.include_baseline,
        )

    candidates = sorted(
        merged.values(),
        key=lambda item: (
            int(as_mapping(item.get("recommendation")).get("score") or 0),
            int(item.get("downloadCount") or 0),
        ),
        reverse=True,
    )

    for record in candidates[: args.detail_limit]:
        firmware_id = record.get("firmwareId")
        if not firmware_id:
            continue
        try:
            detail_payload = api.get(f"/api/v1/firmwares/{quote(str(firmware_id), safe='')}")
        except ApiError as exc:
            record["detailError"] = {
                "error": str(exc),
                "status": exc.status,
                "requestId": exc.request_id,
            }
            continue
        detail = object_data(detail_payload)
        if detail:
            enriched = firmware_record(detail, api.base_url)
            enriched["seenInSorts"] = record.get("seenInSorts") or []
            merged[str(firmware_id)] = merge_record(record, enriched)
            merged[str(firmware_id)]["recommendation"] = recommendation_profile(
                merged[str(firmware_id)],
                include_baseline=args.include_baseline,
            )

    recommendations = sorted(
        merged.values(),
        key=lambda item: (
            int(as_mapping(item.get("recommendation")).get("score") or 0),
            int(item.get("downloadCount") or 0),
        ),
        reverse=True,
    )[: args.limit]

    warnings: list[str] = []
    total = max(totals.values()) if totals else len(merged)
    if any(value > args.sample_size for value in totals.values()):
        warnings.append(
            f"Only sampled the first {args.sample_size} records for one or more sort orders."
        )
    if not args.include_baseline:
        warnings.append("Baseline demos, tests, and low-level component firmware are down-ranked.")

    return {
        "code": 200,
        "msg": "聚合查询成功",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "device": device_info,
        "total": total,
        "sampled": len(merged),
        "sortsUsed": list(SORT_VALUES),
        "recommendations": recommendations,
        "latest": sorted(
            merged.values(),
            key=lambda item: parse_api_datetime(item.get("publishTime")) or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )[: min(args.limit, 10)],
        "mostDownloaded": sorted(
            merged.values(),
            key=lambda item: int(item.get("downloadCount") or 0),
            reverse=True,
        )[: min(args.limit, 10)],
        "warnings": warnings,
    }


def cell(value: Any, *, maximum: int = 48) -> str:
    if value is None:
        return "-"
    text = str(value).replace("\r", " ").replace("\n", " ")
    text = " ".join(text.split())
    if len(text) > maximum:
        return text[: maximum - 3] + "..."
    return text or "-"


def join_names(items: Any, key: str) -> str:
    if not isinstance(items, list):
        return "-"
    return ", ".join(
        str(item.get(key))
        for item in items
        if isinstance(item, Mapping) and item.get(key)
    ) or "-"


def firmware_table(items: list[Mapping[str, Any]]) -> tuple[list[str], list[list[Any]]]:
    headers = ["id", "firmware", "version", "devices", "downloads", "published"]
    rows: list[list[Any]] = []
    for item in items:
        version = item.get("currentVersion") or {}
        stats = item.get("statistics") or {}
        rows.append(
            [
                item.get("firmwareId"),
                item.get("firmwareName"),
                version.get("versionName"),
                join_names(item.get("supportedDevices"), "deviceName"),
                stats.get("downloadCount"),
                version.get("publishTime") or item.get("uploadedAt"),
            ]
        )
    return headers, rows


def version_table(items: list[Mapping[str, Any]]) -> tuple[list[str], list[list[Any]]]:
    headers = ["versionId", "version", "current", "status", "published", "downloads"]
    rows = [
        [
            item.get("versionId"),
            item.get("versionName"),
            item.get("current"),
            item.get("status"),
            item.get("publishTime"),
            item.get("downloadCount"),
        ]
        for item in items
    ]
    return headers, rows


def device_table(items: list[Mapping[str, Any]]) -> tuple[list[str], list[list[Any]]]:
    headers = ["deviceId", "device", "code", "firmwares"]
    rows = [
        [
            item.get("deviceId"),
            item.get("deviceName"),
            item.get("deviceCode"),
            item.get("firmwareCount"),
        ]
        for item in items
    ]
    return headers, rows


def category_table(items: list[Mapping[str, Any]]) -> tuple[list[str], list[list[Any]]]:
    headers = ["categoryId", "category", "code", "firmwares"]
    rows = [
        [
            item.get("categoryId"),
            item.get("categoryName"),
            item.get("categoryCode"),
            item.get("firmwareCount"),
        ]
        for item in items
    ]
    return headers, rows


def developer_table(items: list[Mapping[str, Any]]) -> tuple[list[str], list[list[Any]]]:
    headers = ["developerId", "nickname", "firmwares", "downloads", "likes"]
    rows: list[list[Any]] = []
    for item in items:
        stats = item.get("statistics") or {}
        rows.append(
            [
                item.get("developerId"),
                item.get("nickname"),
                stats.get("totalFirmware"),
                stats.get("totalDownloads"),
                stats.get("totalLikes"),
            ]
        )
    return headers, rows


def uiflow2_table(items: list[Mapping[str, Any]]) -> tuple[list[str], list[list[Any]]]:
    headers = ["deviceType", "firmware", "version", "firmwareId", "downloadUrl"]
    rows = [
        [
            item.get("deviceType"),
            item.get("firmwareName"),
            item.get("versionName"),
            item.get("firmwareId"),
            item.get("downloadUrl"),
        ]
        for item in items
    ]
    return headers, rows


def ranking_table(items: list[Mapping[str, Any]]) -> tuple[list[str], list[list[Any]]]:
    score_key = "weeklyScore" if any("weeklyScore" in item for item in items) else "totalScore"
    headers = ["rank", "firmware", "developer", score_key]
    rows = [
        [
            item.get("rank"),
            item.get("firmwareName"),
            item.get("developerName"),
            item.get(score_key),
        ]
        for item in items
    ]
    return headers, rows


def comment_table(items: list[Mapping[str, Any]]) -> tuple[list[str], list[list[Any]]]:
    headers = ["commentId", "user", "createdAt", "content"]
    rows: list[list[Any]] = []
    for item in items:
        user = item.get("user") or {}
        rows.append(
            [
                item.get("commentId"),
                user.get("nickname") or user.get("username") or user.get("userId"),
                item.get("createdAt"),
                item.get("content"),
            ]
        )
    return headers, rows


def recommendation_table(items: list[Mapping[str, Any]]) -> tuple[list[str], list[list[Any]]]:
    headers = ["firmware", "version", "downloads", "kind", "why", "needs", "url"]
    rows: list[list[Any]] = []
    for item in items:
        profile = as_mapping(item.get("recommendation"))
        rows.append(
            [
                item.get("firmwareName"),
                item.get("versionName"),
                item.get("downloadCount"),
                profile.get("kind"),
                profile.get("why"),
                ", ".join(str(value) for value in profile.get("needs") or []) or "-",
                item.get("pageUrl"),
            ]
        )
    return headers, rows


def intent_table(items: list[Mapping[str, Any]]) -> tuple[list[str], list[list[Any]]]:
    headers = [
        "firmware",
        "version",
        "published",
        "downloads",
        "confidence",
        "prerequisites",
        "url",
    ]
    rows: list[list[Any]] = []
    for item in items:
        intent = as_mapping(item.get("intent"))
        rows.append(
            [
                item.get("firmwareName"),
                item.get("versionName"),
                item.get("publishTime"),
                item.get("downloadCount"),
                intent.get("confidence"),
                ", ".join(str(value) for value in item.get("prerequisites") or []) or "-",
                item.get("pageUrl"),
            ]
        )
    return headers, rows


def render_grid(headers: list[str], rows: list[list[Any]]) -> str:
    if not rows:
        return "No results"
    rendered = [
        [
            cell(
                value,
                maximum=64 if headers[index].lower().endswith("url") else 36,
            )
            for index, value in enumerate(row)
        ]
        for row in rows
    ]
    widths = [
        min(
            max(len(headers[index]), *(len(row[index]) for row in rendered)),
            64 if headers[index].lower().endswith("url") else 36,
        )
        for index in range(len(headers))
    ]
    header = " | ".join(headers[index].ljust(widths[index]) for index in range(len(headers)))
    divider = "-+-".join("-" * width for width in widths)
    body = [
        " | ".join(row[index].ljust(widths[index]) for index in range(len(headers)))
        for row in rendered
    ]
    return "\n".join([header, divider, *body])


def detail_rows(data: Mapping[str, Any]) -> tuple[list[str], list[list[Any]]]:
    version = data.get("currentVersion") or {}
    stats = data.get("statistics") or {}
    rows = [
        ["firmwareId", data.get("firmwareId")],
        ["firmwareName", data.get("firmwareName")],
        ["version", version.get("versionName")],
        ["status", version.get("status")],
        ["published", version.get("publishTime")],
        ["devices", join_names(data.get("supportedDevices"), "deviceName")],
        ["categories", join_names(data.get("categories"), "categoryName")],
        ["downloads", stats.get("downloadCount")],
        ["likes", stats.get("likeCount")],
        ["comments", stats.get("commentCount")],
        ["sourceUrl", data.get("sourceUrl")],
    ]
    return ["field", "value"], rows


def developer_detail_rows(data: Mapping[str, Any]) -> tuple[list[str], list[list[Any]]]:
    stats = data.get("statistics") or {}
    rows = [
        ["developerId", data.get("developerId")],
        ["nickname", data.get("nickname")],
        ["website", data.get("website")],
        ["firmwares", stats.get("totalFirmware")],
        ["downloads", stats.get("totalDownloads")],
        ["likes", stats.get("totalLikes")],
        ["followers", stats.get("totalFollowers")],
    ]
    return ["field", "value"], rows


def table_for(command: str, payload: Any) -> str:
    items = list_data(payload)
    total = payload.get("total") if isinstance(payload, Mapping) else None
    prefix = f"total={total}\n" if total is not None else ""

    if command in ("search", "recommended", "developer-firmwares"):
        headers, rows = firmware_table(items)
    elif command == "intent-search":
        if isinstance(payload, Mapping):
            items = [
                item
                for item in payload.get("results", [])
                if isinstance(item, Mapping)
            ]
            device = as_mapping(payload.get("device"))
            device_label = device.get("deviceName") or payload.get("deviceId") or "-"
            prefix = (
                f"intent={payload.get('intent')} device={device_label} "
                f"candidates={payload.get('candidateTotal')} "
                f"category={payload.get('categoryCandidateTotal')} "
                f"matched={payload.get('matchedTotal')}\n"
            )
        else:
            items = []
        headers, rows = intent_table(items)
    elif command == "versions":
        headers, rows = version_table(items)
    elif command in ("devices", "device-by-slug"):
        data = object_data(payload) if command == "device-by-slug" else None
        if data:
            headers, rows = ["field", "value"], [
                [key, value]
                for key, value in data.items()
                if key not in {"imageUrl"}
            ]
        else:
            headers, rows = device_table(items)
    elif command == "categories":
        headers, rows = category_table(items)
        if isinstance(payload, Mapping) and payload.get("totalFirmwareCount") is not None:
            prefix = f"totalFirmwareCount={payload['totalFirmwareCount']}\n" + prefix
    elif command == "uiflow2":
        headers, rows = uiflow2_table(items)
    elif command in ("ranking",):
        headers, rows = ranking_table(items)
    elif command == "comments":
        headers, rows = comment_table(items)
    elif command == "developers":
        headers, rows = developer_table(items)
    elif command == "developer":
        headers, rows = developer_detail_rows(object_data(payload))
    elif command == "detail":
        headers, rows = detail_rows(object_data(payload))
    elif command == "recommend-device":
        if isinstance(payload, Mapping):
            items = [
                item
                for item in payload.get("recommendations", [])
                if isinstance(item, Mapping)
            ]
            device = as_mapping(payload.get("device"))
            device_name = device.get("deviceName") or device.get("deviceId") or "-"
            prefix = (
                f"device={device_name} total={payload.get('total')} "
                f"sampled={payload.get('sampled')}\n"
            )
        else:
            items = []
        headers, rows = recommendation_table(items)
    else:
        data = object_data(payload)
        if data:
            headers, rows = detail_rows(data)
        else:
            headers, rows = ["field", "value"], []

    if not rows:
        return prefix + "No results"
    return prefix + render_grid(headers, rows)


def error_output(exc: ApiError, output_format: str, pretty: bool) -> None:
    report: dict[str, Any] = {
        "error": str(exc),
        "status": exc.status,
    }
    if exc.request_id:
        report["requestId"] = exc.request_id
    if output_format == "json":
        print(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2 if pretty else None,
            )
        )
    else:
        suffix = f" requestId={exc.request_id}" if exc.request_id else ""
        print(f"Error: {exc}{suffix}", file=sys.stderr)


def add_output_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Compatible M5Burner base URL (or M5BURNER_API_BASE_URL)",
    )
    parser.add_argument("--timeout", type=bounded_int(120), default=20)
    parser.add_argument("--format", dest="output_format", choices=("json", "table"), default="json")
    parser.add_argument("--pretty", action="store_true", help="Indent JSON output")


def add_page_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--page", type=positive_int, default=1)
    parser.add_argument("--page-size", type=bounded_int(100), default=20)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read-only queries for the public M5Burner firmware catalog."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="Search public firmware projects")
    search.add_argument("--keyword")
    category_name = search.add_mutually_exclusive_group()
    category_name.add_argument("--category-id")
    category_name.add_argument("--category-name")
    device_name = search.add_mutually_exclusive_group()
    device_name.add_argument("--device-id")
    device_name.add_argument("--device-name")
    search.add_argument("--language", choices=("US", "CN", "JP"), default="US")
    search.add_argument("--sort", choices=SORT_VALUES, default="LATEST")
    add_page_options(search)
    add_output_options(search)

    intent_search = subparsers.add_parser(
        "intent-search",
        help="Search by a functional intent and verify candidate descriptions",
    )
    intent_search.add_argument("--intent", choices=("ai",), default="ai")
    intent_search.add_argument("--keyword")
    intent_category_name = intent_search.add_mutually_exclusive_group()
    intent_category_name.add_argument("--category-id")
    intent_category_name.add_argument("--category-name")
    intent_device_name = intent_search.add_mutually_exclusive_group()
    intent_device_name.add_argument("--device-id")
    intent_device_name.add_argument("--device-name")
    intent_search.add_argument("--language", choices=("US", "CN", "JP"), default="US")
    intent_search.add_argument("--sort", choices=SORT_VALUES, default="LATEST")
    intent_search.add_argument("--page-size", type=bounded_int(100), default=100)
    intent_search.add_argument(
        "--detail-limit", type=bounded_int(100), default=60
    )
    intent_search.add_argument(
        "--excluded-limit", type=bounded_int(100), default=20
    )
    add_output_options(intent_search)

    detail = subparsers.add_parser("detail", help="Get one firmware project's public detail")
    detail.add_argument("firmware_id")
    add_output_options(detail)

    versions = subparsers.add_parser("versions", help="List public versions for a firmware")
    versions.add_argument("firmware_id")
    versions.add_argument("--scope", default="PUBLIC")
    add_output_options(versions)

    devices = subparsers.add_parser("devices", help="List the public device catalog")
    devices.add_argument("--developer-id")
    add_output_options(devices)

    device_by_slug = subparsers.add_parser(
        "device-by-slug", help="Look up one device by its public route slug"
    )
    device_by_slug.add_argument("slug")
    add_output_options(device_by_slug)

    categories = subparsers.add_parser("categories", help="List localized firmware categories")
    categories.add_argument("--language", choices=("US", "CN", "JP"), default="US")
    categories.add_argument("--device-id")
    categories.add_argument("--developer-id")
    add_output_options(categories)

    developers = subparsers.add_parser("developers", help="Search public developers")
    developers.add_argument("--keyword")
    add_page_options(developers)
    add_output_options(developers)

    developer = subparsers.add_parser("developer", help="Get one public developer profile")
    developer.add_argument("developer_id")
    add_output_options(developer)

    developer_firmwares = subparsers.add_parser(
        "developer-firmwares", help="List a developer's public firmware"
    )
    developer_firmwares.add_argument("developer_id")
    developer_firmwares.add_argument("--keyword")
    developer_firmwares.add_argument("--category-id")
    developer_firmwares.add_argument("--device-id")
    add_page_options(developer_firmwares)
    add_output_options(developer_firmwares)

    uiflow2 = subparsers.add_parser("uiflow2", help="List the latest UIFlow2 firmware")
    add_output_options(uiflow2)

    recommended = subparsers.add_parser("recommended", help="List recommended firmware")
    recommended.add_argument("--limit", type=bounded_int(100), default=6)
    add_output_options(recommended)

    ranking = subparsers.add_parser("ranking", help="List weekly or all-time rankings")
    ranking.add_argument("--kind", choices=("weekly", "all-time"), default="weekly")
    ranking.add_argument("--limit", type=bounded_int(100), default=10)
    add_output_options(ranking)

    comments = subparsers.add_parser("comments", help="List public firmware comments")
    comments.add_argument("firmware_id")
    add_page_options(comments)
    add_output_options(comments)

    recommend_device = subparsers.add_parser(
        "recommend-device",
        help="Suggest interesting firmware for one device",
    )
    recommend_device_filter = recommend_device.add_mutually_exclusive_group(required=True)
    recommend_device_filter.add_argument("--device-id")
    recommend_device_filter.add_argument("--device-name")
    recommend_device.add_argument("--limit", type=bounded_int(30), default=10)
    recommend_device.add_argument("--sample-size", type=bounded_int(100), default=100)
    recommend_device.add_argument("--detail-limit", type=bounded_int(60), default=8)
    recommend_device.add_argument(
        "--include-baseline",
        action="store_true",
        help="Do not down-rank demos, tests, or low-level component firmware",
    )
    add_output_options(recommend_device)
    return parser


COMMANDS = {
    "search": command_search,
    "intent-search": command_intent_search,
    "detail": command_detail,
    "versions": command_versions,
    "devices": command_devices,
    "device-by-slug": command_device_by_slug,
    "categories": command_categories,
    "developers": command_developers,
    "developer": command_developer,
    "developer-firmwares": command_developer_firmwares,
    "uiflow2": command_uiflow2,
    "recommended": command_recommended,
    "ranking": command_ranking,
    "comments": command_comments,
    "recommend-device": command_recommend_device,
}


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        api = FirmwareApi(args.base_url, args.timeout)
        payload = COMMANDS[args.command](api, args)
    except ApiError as exc:
        error_output(exc, args.output_format, args.pretty)
        return 2

    if args.output_format == "table":
        print(table_for(args.command, payload))
    else:
        print(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
