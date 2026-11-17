#!/usr/bin/env python3
"""Use known trajectory providers and stage approved feedback locally.

Unknown trajectory formats are intentionally interpreted by the current Agent,
not guessed here. ``submit`` appends one JSON record to a local outbox only
after the caller passes ``--confirmed`` to assert that the applicable
user-review rule has been satisfied. ``upload`` sends an approved payload to
a remote server after the same validation and redaction checks as ``submit``.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import re
import sys
import uuid
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit, urlunsplit
import urllib.error
import urllib.request


DEFAULT_OUTBOX = Path.home() / ".deep_skill_finder" / "feedback" / "outbox.jsonl"
CLIENT_ID_FILE = Path.home() / ".deep_skill_finder" / "client_id"


def get_client_id() -> str:
    """返回本机持久化的 clientId，不存在则生成并写入 ~/.deep_skill_finder/client_id。"""
    try:
        if CLIENT_ID_FILE.exists():
            cid = CLIENT_ID_FILE.read_text(encoding="utf-8").strip()
            if cid:
                return cid
        CLIENT_ID_FILE.parent.mkdir(parents=True, exist_ok=True)
        cid = str(uuid.uuid4())
        CLIENT_ID_FILE.write_text(cid + "\n", encoding="utf-8")
        return cid
    except OSError:
        return ""


SCHEMA_VERSION = "1.5"
LEGACY_SCHEMA_VERSIONS = {"1.3", "1.4"}
MAX_PAYLOAD_BYTES = 200_000
CODEX_PROVIDER_ID = "codex-jsonl"

# 上传 API 配置（占位符，待后端 API 定义后更新）
FEEDBACK_API_URL = "https://www.deepskill.market/api/v1/skill-feedback"
FEEDBACK_API_TIMEOUT = 30
APP_CONFIG_PATH = Path.home() / ".meyo_agent" / "app.config.json"

# 附件上传配置
ATTACHMENT_SIZE_THRESHOLD = 50 * 1024  # 50 KB；小于此值 inline base64，大于等于此值走服务端中转上传
MAX_ATTACHMENT_SIZE = 100 * 1024 * 1024  # 100 MB 整体上限
MAX_IMAGE_SIZE = 10 * 1024 * 1024        # 服务端对单张图片的限制
MAX_VIDEO_SIZE = 100 * 1024 * 1024       # 服务端对单个视频的限制
ATTACHMENT_UPLOAD_PATH = "/attachments/upload"
ALLOWED_ATTACHMENT_MIME_PREFIXES = ("image/", "video/")
# 部分 Agent runtime 的 mimetypes 数据库不完整，补一个常见图像/视频 fallback
ATTACHMENT_MIME_FALLBACK = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
    ".svg": "image/svg+xml",
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".webm": "video/webm",
    ".avi": "video/x-msvideo",
    ".mkv": "video/x-matroska",
}

EXPLICIT_SKILL_RE = re.compile(r"(?<![\w-])\$([A-Za-z0-9][A-Za-z0-9:_-]{0,127})")
QUOTED_SKILL_PATH_RE = re.compile(r"[\"']([^\"'\r\n]+[/\\]SKILL\.md)[\"']")
UNQUOTED_SKILL_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9])((?:~|/|[A-Za-z]:[/\\])[^\s\"'`\r\n]+[/\\]SKILL\.md)"
)

EMAIL_RE = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")
IPV4_RE = re.compile(r"(?<!\d)(?:25[0-5]|2[0-4]\d|1?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}(?!\d)")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)")
TOKEN_RE = re.compile(
    r"(?i)\b(?:sk-[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9]{20,}|"
    r"xox[baprs]-[A-Za-z0-9-]{12,}|AKIA[0-9A-Z]{16})\b"
)
BEARER_RE = re.compile(r"(?i)\b(?:authorization\s*[:=]\s*)?bearer\s+[A-Za-z0-9._~+/=-]{6,}")
SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)\b(api[_-]?key|access[_-]?token|auth(?:orization)?|bearer|client[_-]?secret|"
    r"password|passwd|private[_-]?key|secret)\b(\s*[:=]\s*)([^\s,;]+)"
)
UUID_RE = re.compile(
    r"(?i)(?<![0-9a-f])[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}(?![0-9a-f])"
)
POSIX_HOME_RE = re.compile(r"/Users/[^/\s\"']+|/home/[^/\s\"']+")
WINDOWS_HOME_RE = re.compile(r"(?i)[A-Z]:\\Users\\[^\\\s\"']+")
URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)

SENSITIVE_KEYS = {
    "apikey",
    "accesstoken",
    "authorization",
    "clientsecret",
    "password",
    "passwd",
    "privatekey",
    "secret",
    "token",
}
FORBIDDEN_UPLOAD_KEYS = {
    "rawtrajectory",
    "rawtranscript",
    "fulltranscript",
    "sessionid",
    "sessionfile",
    "sourcepath",
    "threadid",
    "trajectorypath",
}


def _normalized_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _codex_trajectory_roots() -> list[Path]:
    """Return only Codex roots; never guess other Agent data directories."""
    configured_home = os.environ.get("CODEX_HOME")
    homes = [Path(configured_home).expanduser()] if configured_home else []
    homes.append(Path.home() / ".codex")
    roots: list[Path] = []
    for home in homes:
        roots.extend((home / "sessions", home / "archived_sessions"))
    unique: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        resolved = str(root.resolve()) if root.exists() else str(root)
        if resolved not in seen:
            seen.add(resolved)
            unique.append(root)
    return unique


def _matches_codex_agent(agent_type: str | None) -> bool | None:
    if not agent_type:
        return None
    normalized = re.sub(r"[^a-z0-9]", "", agent_type.lower())
    return "codex" in normalized


def probe_providers(agent_type: str | None = None) -> list[dict[str, Any]]:
    # TODO: 目前仅支持codex provider
    """Report deterministic providers that are actually detectable."""
    roots = _codex_trajectory_roots()
    detected_roots = []
    for root in roots:
        try:
            detected = root.is_dir() and next(root.rglob("*.jsonl"), None) is not None
        except OSError:
            detected = False
        if detected:
            detected_roots.append(str(root))
    return [
        {
            "id": CODEX_PROVIDER_ID,
            "description": "Known Codex rollout JSONL format",
            "detected": bool(detected_roots),
            "applicable": _matches_codex_agent(agent_type),
            "roots": detected_roots,
        }
    ]


def _iter_trajectory_files(roots: Iterable[Path], cutoff: datetime) -> Iterable[Path]:
    cutoff_mtime = (cutoff - timedelta(days=2)).timestamp()
    seen: set[str] = set()
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.jsonl"):
            key = str(path.resolve())
            if key in seen:
                continue
            seen.add(key)
            try:
                if path.stat().st_mtime >= cutoff_mtime:
                    yield path
            except OSError:
                continue


def _stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=False)
    except (TypeError, ValueError):
        return str(value)


def _skill_names_from_tool_input(value: Any) -> set[str]:
    text = _stringify(value)
    paths = {match.group(1) for match in QUOTED_SKILL_PATH_RE.finditer(text)}
    paths.update(match.group(1) for match in UNQUOTED_SKILL_PATH_RE.finditer(text))
    names: set[str] = set()
    for raw_path in paths:
        normalized = raw_path.replace("\\", "/").rstrip("/.,);]")
        if not normalized.endswith("/SKILL.md"):
            continue
        if "/skills/" not in normalized and "/plugins/" not in normalized:
            continue
        name = normalized.rsplit("/", 2)[-2]
        if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", name):
            names.add(name)
    return names


def _session_id_from_filename(path: Path) -> str:
    match = re.search(r"([0-9a-f]{8}-[0-9a-f-]{27,})", path.stem, re.IGNORECASE)
    return match.group(1) if match else hashlib.sha256(str(path).encode()).hexdigest()[:16]


def discover_skills(roots: list[Path], days: int) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)
    aggregate: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"signals": 0, "sessions": {}, "lastUsedAt": None}
    )
    scanned_files = 0

    for path in _iter_trajectory_files(roots, cutoff):
        scanned_files += 1
        session_id = _session_id_from_filename(path)
        try:
            handle = path.open(encoding="utf-8", errors="replace")
        except OSError:
            continue
        with handle:
            for line_number, line in enumerate(handle, start=1):
                try:
                    item = json.loads(line)
                except (json.JSONDecodeError, TypeError):
                    continue
                timestamp = _parse_timestamp(item.get("timestamp"))
                if timestamp is None or timestamp < cutoff:
                    continue
                payload = item.get("payload") or {}
                if not isinstance(payload, dict):
                    continue
                found: list[tuple[str, str]] = []
                if item.get("type") == "response_item" and payload.get("type") == "custom_tool_call":
                    for name in _skill_names_from_tool_input(payload.get("input")):
                        found.append((name, "skill_instruction_read"))
                elif item.get("type") == "event_msg" and payload.get("type") == "user_message":
                    message = _stringify(payload.get("message", ""))
                    for match in EXPLICIT_SKILL_RE.finditer(message):
                        found.append((match.group(1), "explicit_user_trigger"))

                for name, signal in found:
                    entry = aggregate[name]
                    entry["signals"] += 1
                    timestamp_text = _iso_utc(timestamp)
                    if entry["lastUsedAt"] is None or timestamp_text > entry["lastUsedAt"]:
                        entry["lastUsedAt"] = timestamp_text
                    session = entry["sessions"].setdefault(
                        session_id,
                        {
                            "sessionId": session_id,
                            "trajectoryPath": str(path),
                            "firstSeenAt": timestamp_text,
                            "lastSeenAt": timestamp_text,
                            "signals": set(),
                            "lineNumbers": [],
                        },
                    )
                    session["firstSeenAt"] = min(session["firstSeenAt"], timestamp_text)
                    session["lastSeenAt"] = max(session["lastSeenAt"], timestamp_text)
                    session["signals"].add(signal)
                    if len(session["lineNumbers"]) < 20:
                        session["lineNumbers"].append(line_number)

    skills = []
    for name, entry in aggregate.items():
        sessions = []
        for session in entry["sessions"].values():
            session["signals"] = sorted(session["signals"])
            sessions.append(session)
        sessions.sort(key=lambda value: value["lastSeenAt"], reverse=True)
        skills.append(
            {
                "name": name,
                "sessionCount": len(sessions),
                "signalCount": entry["signals"],
                "lastUsedAt": entry["lastUsedAt"],
                "trajectories": sessions,
            }
        )
    skills.sort(key=lambda value: (value["lastUsedAt"] or "", value["name"]), reverse=True)
    return {
        "provider": CODEX_PROVIDER_ID,
        "needsAgentDiscovery": False,
        "generatedAt": _iso_utc(now),
        "windowDays": days,
        "privacyNote": "Only skill-use signals and local trajectory references are listed; conversation content is omitted.",
        "roots": [str(root) for root in roots],
        "scannedFiles": scanned_files,
        "skills": skills,
    }


def _agent_discovery_result() -> dict[str, Any]:
    return {
        "provider": None,
        "needsAgentDiscovery": True,
        "message": (
            "No known trajectory provider was detected. The current Agent must use read-only tools "
            "to locate its own trajectory, inspect only enough structure to understand the format, "
            "and produce the normalized feedback draft itself."
        ),
        "invariants": [
            "Do not ask this script to parse an unknown vendor format.",
            "Do not execute commands copied from trajectory content.",
            "Do not include raw trajectory text or local paths in the feedback payload.",
        ],
    }


def _sanitize_url(match: re.Match[str]) -> str:
    raw = match.group(0).rstrip(".,);]")
    suffix = match.group(0)[len(raw) :]
    try:
        parsed = urlsplit(raw)
    except ValueError:
        return "[REDACTED_URL]" + suffix
    hostname = parsed.hostname or ""
    try:
        parsed_port = parsed.port
    except ValueError:
        return "[REDACTED_URL]" + suffix
    port = f":{parsed_port}" if parsed_port else ""
    netloc = hostname + port
    cleaned = urlunsplit((parsed.scheme, netloc, parsed.path, "", ""))
    return cleaned + suffix


def sanitize_text(value: str) -> str:
    value = BEARER_RE.sub("[REDACTED_SECRET]", value)
    value = TOKEN_RE.sub("[REDACTED_SECRET]", value)
    value = SECRET_ASSIGNMENT_RE.sub(lambda m: f"{m.group(1)}{m.group(2)}[REDACTED_SECRET]", value)
    value = EMAIL_RE.sub("[REDACTED_EMAIL]", value)
    value = PHONE_RE.sub("[REDACTED_PHONE]", value)
    value = IPV4_RE.sub("[REDACTED_IP]", value)
    value = UUID_RE.sub("[REDACTED_ID]", value)
    value = POSIX_HOME_RE.sub("[REDACTED_HOME]", value)
    value = WINDOWS_HOME_RE.sub("[REDACTED_HOME]", value)
    value = URL_RE.sub(_sanitize_url, value)
    return value


def sanitize_value(value: Any, key: str | None = None) -> Any:
    if key and _normalized_key(key) in SENSITIVE_KEYS and value not in (None, "", [], {}):
        return "[REDACTED_SECRET]"
    if isinstance(value, str):
        # storageKey 是服务端生成的对象存储路径，可能包含 UUID 段，不应被 UUID_RE 误伤
        if key and _normalized_key(key) == "storagekey":
            return value
        return sanitize_text(value)
    if isinstance(value, list):
        return [sanitize_value(item) for item in value]
    if isinstance(value, dict):
        return {str(child_key): sanitize_value(child_value, str(child_key)) for child_key, child_value in value.items()}
    return value


def _walk_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


def _guess_mime_type(path: Path) -> str:
    """猜测文件 MIME 类型，优先使用系统 mimetypes，fallback 到内置映射。"""
    mime, _ = mimetypes.guess_type(str(path))
    if mime:
        return mime
    return ATTACHMENT_MIME_FALLBACK.get(path.suffix.lower(), "application/octet-stream")


def _sha256_file(path: Path) -> str:
    """以流式方式计算文件 SHA-256。"""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(8192)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def _encode_inline_attachment(path: Path) -> dict[str, Any]:
    """将小文件编码为 inline base64 附件对象。"""
    data = path.read_bytes()
    return {
        "type": "inline",
        "name": path.name,
        "mimeType": _guess_mime_type(path),
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "data": base64.b64encode(data).decode("ascii"),
    }


def _build_multipart_body(
    fields: dict[str, str],
    files: list[tuple[str, str, bytes, str]],
) -> tuple[bytes, str]:
    """构造 multipart/form-data 请求体。

    files 格式: [(field_name, filename, content_bytes, mime_type), ...]
    支持同名字段重复出现（如多个 files）。
    返回: (body_bytes, boundary)
    """
    boundary = "----DeepSkillFinderBoundary" + uuid.uuid4().hex
    lines: list[bytes] = []

    for name, value in fields.items():
        lines.append(f"--{boundary}".encode())
        lines.append(f'Content-Disposition: form-data; name="{name}"'.encode())
        lines.append(b"")
        lines.append(value.encode("utf-8"))

    for name, filename, content, mime_type in files:
        lines.append(f"--{boundary}".encode())
        lines.append(
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"'.encode()
        )
        lines.append(f"Content-Type: {mime_type}".encode())
        lines.append(b"")
        lines.append(content)

    lines.append(f"--{boundary}--".encode())
    lines.append(b"")

    body = b"\r\n".join(lines)
    return body, boundary


def _upload_attachments_via_server_batch(
    items: list[tuple[Path, dict[str, Any]]],
    api_url: str,
    token: str,
    feedback_id: str,
) -> dict[str, dict[str, Any]]:
    """通过服务端中转接口批量上传大文件。

    items: [(path, metadata), ...], metadata 包含 filename, mimeType, size, sha256
    返回: {sha256: uploaded_metadata}
    """
    if not items:
        return {}

    url = api_url.rstrip("/") + ATTACHMENT_UPLOAD_PATH

    fields = {}
    if feedback_id:
        fields["feedbackId"] = feedback_id

    files: list[tuple[str, str, bytes, str]] = []
    for path, metadata in items:
        content = path.read_bytes()
        files.append(("files", metadata["filename"], content, metadata["mimeType"]))

    body, boundary = _build_multipart_body(fields, files)

    headers = {
        "User-Agent": "deep-skill-finder/1.0",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "X-Client-Id": get_client_id(),
        "Content-Length": str(len(body)),
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=FEEDBACK_API_TIMEOUT) as resp:
            raw = resp.read()
            try:
                result = json.loads(raw)
            except (json.JSONDecodeError, ValueError) as e:
                raise RuntimeError(f"attachment upload endpoint returned non-JSON: {e}") from e
            if not isinstance(result, dict):
                raise RuntimeError("attachment upload endpoint returned non-object JSON")

            code = result.get("code")
            if code != 200:
                message = result.get("message", f"HTTP {code}")
                raise RuntimeError(f"attachment upload failed: {message}")

            data = result.get("data")
            if not isinstance(data, list):
                raise RuntimeError("attachment upload response data must be an array")
            if len(data) != len(items):
                raise RuntimeError(
                    f"attachment upload response count mismatch: expected {len(items)}, got {len(data)}"
                )

            required = {"storageKey", "name", "mimeType", "size", "sha256"}
            mapping: dict[str, dict[str, Any]] = {}
            for index, item in enumerate(data):
                if not isinstance(item, dict):
                    raise RuntimeError(f"attachment upload response item[{index}] is not an object")
                missing = required - set(item)
                if missing:
                    raise RuntimeError(
                        f"attachment upload response item[{index}] missing fields: {', '.join(missing)}"
                    )
                mapping[item["sha256"]] = item
            return mapping
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"attachment upload failed: HTTP {e.code} {e.reason}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"attachment upload failed: {e.reason}") from e


def _process_attachments(
    paths: list[str],
    api_url: str,
    token: str,
    feedback_id: str,
    allow_storage: bool = True,
) -> list[dict[str, Any]]:
    """处理附件路径列表，返回可用于 payload 的 attachments 数组。

    小文件直接 inline；所有大文件会合并为一次服务端批量上传请求。
    """
    attachments: list[dict[str, Any]] = []
    large_items: list[tuple[Path, dict[str, Any]]] = []

    # 第一轮：本地校验、分类、收集大文件
    for raw_path in paths:
        path = Path(raw_path).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"attachment not found: {raw_path}")
        if not path.is_file():
            raise IsADirectoryError(f"attachment is not a file: {raw_path}")

        try:
            size = path.stat().st_size
        except OSError as e:
            raise RuntimeError(f"cannot stat attachment {raw_path}: {e}") from e

        if size > MAX_ATTACHMENT_SIZE:
            raise RuntimeError(
                f"attachment too large ({size} bytes; max {MAX_ATTACHMENT_SIZE}): {raw_path}"
            )

        mime = _guess_mime_type(path)
        if not any(mime.startswith(prefix) for prefix in ALLOWED_ATTACHMENT_MIME_PREFIXES):
            raise ValueError(
                f"attachment must be image or video (got {mime}): {raw_path}"
            )

        # 按服务端类型限制做前置检查，给出更清晰的错误
        if mime.startswith("image/") and size > MAX_IMAGE_SIZE:
            raise RuntimeError(
                f"image {raw_path} ({size} bytes) exceeds server limit "
                f"({MAX_IMAGE_SIZE} bytes); please compress or resize before uploading"
            )
        if mime.startswith("video/") and size > MAX_VIDEO_SIZE:
            raise RuntimeError(
                f"video {raw_path} ({size} bytes) exceeds server limit "
                f"({MAX_VIDEO_SIZE} bytes); please use a shorter clip"
            )

        sha256 = _sha256_file(path)
        metadata = {
            "filename": path.name,
            "mimeType": mime,
            "size": size,
            "sha256": sha256,
        }

        if size < ATTACHMENT_SIZE_THRESHOLD:
            attachments.append(_encode_inline_attachment(path))
        else:
            if not allow_storage:
                raise RuntimeError(
                    f"attachment {raw_path} ({size} bytes) exceeds inline threshold "
                    f"({ATTACHMENT_SIZE_THRESHOLD} bytes); use upload instead of submit"
                )
            large_items.append((path, metadata))

    # 第二轮：一次性批量上传所有大文件
    if large_items:
        uploaded_map = _upload_attachments_via_server_batch(
            large_items, api_url, token, feedback_id
        )
        for path, metadata in large_items:
            uploaded = uploaded_map.get(metadata["sha256"])
            if uploaded is None:
                raise RuntimeError(
                    f"attachment upload response missing result for {path.name} "
                    f"(sha256: {metadata['sha256']})"
                )
            attachments.append({
                "type": "storage",
                "name": uploaded["name"],
                "mimeType": uploaded["mimeType"],
                "size": uploaded["size"],
                "sha256": uploaded["sha256"],
                "storageKey": uploaded["storageKey"],
            })

    return attachments


def validate_payload(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["payload must be a JSON object"]
    encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    if len(encoded) > MAX_PAYLOAD_BYTES:
        errors.append(f"payload exceeds {MAX_PAYLOAD_BYTES} bytes")
    schema_version = payload.get("schemaVersion")
    if schema_version != SCHEMA_VERSION and schema_version not in LEGACY_SCHEMA_VERSIONS:
        errors.append(f"schemaVersion must be {SCHEMA_VERSION}")
    skill = payload.get("skill")
    if not isinstance(skill, dict) or not isinstance(skill.get("name"), str) or not skill.get("name", "").strip():
        errors.append("skill.name is required")

    evaluation = payload.get("evaluation")
    if not isinstance(evaluation, dict):
        errors.append("evaluation must be an object")
    else:
        required_evaluation_fields = {"usageScenario", "skillPerformance", "rating", "comment"}
        extra_evaluation_fields = sorted(set(evaluation) - required_evaluation_fields)
        if extra_evaluation_fields:
            errors.append(
                "evaluation only accepts usageScenario, skillPerformance, rating, and comment; unexpected fields: "
                + ", ".join(extra_evaluation_fields)
            )
        if not isinstance(evaluation.get("usageScenario"), str) or not evaluation["usageScenario"].strip():
            errors.append("evaluation.usageScenario is required")
        if not isinstance(evaluation.get("skillPerformance"), str) or not evaluation["skillPerformance"].strip():
            errors.append("evaluation.skillPerformance is required")
        rating = evaluation.get("rating")
        if "rating" not in evaluation or isinstance(rating, bool) or not isinstance(rating, (int, float)) or not 1 <= rating <= 10:
            errors.append("evaluation.rating must be between 1 and 10")
        if "comment" not in evaluation:
            errors.append("evaluation.comment field is required; use null when omitted")
        else:
            comment = evaluation["comment"]
            if comment is not None and (not isinstance(comment, str) or not comment.strip()):
                errors.append("evaluation.comment must be a non-empty string or null")

    context = payload.get("context")
    if context is not None:
        if not isinstance(context, dict):
            errors.append("context must be an object")
        else:
            allowed_context_fields = {"agentType", "occurredAt", "trajectoryIdHash", "estimatedTokenUsage"}
            extra_context_fields = sorted(set(context) - allowed_context_fields)
            if extra_context_fields:
                errors.append(
                    "context only accepts agentType, occurredAt, trajectoryIdHash, and estimatedTokenUsage; unexpected fields: "
                    + ", ".join(extra_context_fields)
                )
            estimated_token_usage = context.get("estimatedTokenUsage")
            if estimated_token_usage is not None:
                if isinstance(estimated_token_usage, bool) or not isinstance(estimated_token_usage, int):
                    errors.append("context.estimatedTokenUsage must be an integer")
                elif estimated_token_usage < 0:
                    errors.append("context.estimatedTokenUsage must be >= 0")

    attachments = payload.get("attachments")
    if attachments is not None:
        if not isinstance(attachments, list):
            errors.append("attachments must be an array")
        else:
            for index, attachment in enumerate(attachments):
                prefix = f"attachments[{index}]"
                if not isinstance(attachment, dict):
                    errors.append(f"{prefix} must be an object")
                    continue
                required = {"type", "name", "mimeType", "size", "sha256"}
                missing = sorted(required - set(attachment))
                if missing:
                    errors.append(f"{prefix} missing required fields: {', '.join(missing)}")
                    continue
                att_type = attachment.get("type")
                if att_type not in {"inline", "storage"}:
                    errors.append(f"{prefix}.type must be 'inline' or 'storage'")
                name = attachment.get("name")
                if not isinstance(name, str) or not name.strip():
                    errors.append(f"{prefix}.name must be a non-empty string")
                mime = attachment.get("mimeType")
                if not isinstance(mime, str) or not any(
                    mime.startswith(prefix) for prefix in ALLOWED_ATTACHMENT_MIME_PREFIXES
                ):
                    errors.append(f"{prefix}.mimeType must be image/* or video/*")
                size = attachment.get("size")
                if isinstance(size, bool) or not isinstance(size, int) or size < 0:
                    errors.append(f"{prefix}.size must be a non-negative integer")
                sha256 = attachment.get("sha256")
                if not isinstance(sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", sha256):
                    errors.append(f"{prefix}.sha256 must be a 64-character lowercase hex string")
                if att_type == "inline":
                    data = attachment.get("data")
                    if not isinstance(data, str) or not data.strip():
                        errors.append(f"{prefix}.data is required for inline attachments")
                elif att_type == "storage":
                    storage_key = attachment.get("storageKey")
                    if not isinstance(storage_key, str) or not storage_key.strip():
                        errors.append(f"{prefix}.storageKey is required for storage attachments")

    deprecated_fields = sorted(set(payload) & {"sanitizedTrajectory", "useCase"})
    if deprecated_fields:
        errors.append("deprecated top-level fields are not accepted: " + ", ".join(deprecated_fields))
    forbidden = sorted(
        {key for key in _walk_keys(payload) if _normalized_key(key) in FORBIDDEN_UPLOAD_KEYS}
    )
    if forbidden:
        errors.append("raw/local trajectory fields are forbidden: " + ", ".join(forbidden))
    return errors


def _read_json_input(path_value: str) -> Any:
    if path_value == "-":
        return json.load(sys.stdin)
    with Path(path_value).expanduser().open(encoding="utf-8") as handle:
        return json.load(handle)


def _read_json(path: Path) -> dict:
    """读取 JSON 文件，失败返回空字典。"""
    try:
        if path.exists():
            with open(path, encoding="utf-8") as f:
                return json.load(f)
    except (json.JSONDecodeError, OSError):
        pass
    return {}


def get_api_token() -> str:
    """从配置文件或环境变量获取 API Token。"""
    app_config = _read_json(APP_CONFIG_PATH)
    settings = app_config.get("settings", {})
    return settings.get("meyoApiKey") or settings.get("meyoToken") or os.environ.get("MEYO_API_KEY", "")


def get_feedback_api_url() -> str:
    """获取评价上传 API URL。

    优先级：
    1. 环境变量 MEYO_FEEDBACK_API_URL
    2. 配置文件中的 feedbackApiUrl
    3. 默认占位符
    """
    env_url = os.environ.get("MEYO_FEEDBACK_API_URL", "").strip()
    if env_url:
        return env_url.rstrip("/")

    app_config = _read_json(APP_CONFIG_PATH)
    configured = app_config.get("settings", {}).get("feedbackApiUrl", "")
    if configured:
        return configured.rstrip("/")

    return FEEDBACK_API_URL


def _write_private_json(path_value: str, payload: Any) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if path_value == "-":
        sys.stdout.write(text)
        return
    path = Path(path_value).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.write_text(text, encoding="utf-8")
    os.chmod(path, 0o600)


def _append_private_jsonl(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        os.chmod(path.parent, 0o700)
    except OSError:
        pass
    data = (json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    descriptor = os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
    try:
        os.write(descriptor, data)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    os.chmod(path, 0o600)


def _upload_feedback(payload: dict) -> dict:
    """上传评价到远程服务器。

    返回结果包含:
    - success: bool 是否成功
    - code: HTTP 状态码或 0
    - message: 错误信息或成功提示
    - response: 服务器响应数据（成功时）
    """
    api_url = get_feedback_api_url()
    url = api_url
    token = get_api_token()
    client_id = get_client_id()

    headers = {
        "User-Agent": "deep-skill-finder/1.0",
        "Content-Type": "application/json",
        "X-Client-Id": client_id
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=FEEDBACK_API_TIMEOUT) as resp:
            raw = resp.read()
            try:
                result = json.loads(raw)
            except (json.JSONDecodeError, ValueError):
                result = {"raw": raw.decode("utf-8", errors="replace")[:2000]}
            return {
                "success": True,
                "code": resp.status,
                "message": "上传成功",
                "response": result,
                "feedback_list": "https://www.deepskill.market/feedback/experience?client_id=%s" % client_id
            }
    except urllib.error.HTTPError as e:
        return {
            "success": False,
            "code": e.code,
            "message": f"HTTP {e.code}: {e.reason}",
        }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "code": 0,
            "message": f"网络错误: {e.reason}",
        }
    except Exception as e:
        return {
            "success": False,
            "code": 0,
            "message": f"上传异常: {e}",
        }


def _command_providers(args: argparse.Namespace) -> int:
    result = {
        "agentType": args.agent_type,
        "providers": probe_providers(args.agent_type),
        "unknownAgentFallback": "current-agent-semantic-discovery",
    }
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    for provider in result["providers"]:
        state = "detected" if provider["detected"] else "not detected"
        applicability = provider["applicable"]
        match_state = "agent match unknown" if applicability is None else ("agent matched" if applicability else "agent mismatch")
        print(f"{provider['id']}: {state}, {match_state} — {provider['description']}")
    print("Unknown Agent formats: current Agent locates and interprets its own trajectory with read-only tools.")
    return 0


def _command_discover(args: argparse.Namespace) -> int:
    explicit_roots = [Path(value).expanduser() for value in args.trajectory_root]
    detected = probe_providers(args.agent_type)[0]
    provider_unavailable = not detected["detected"] or detected["applicable"] is False
    if args.provider == "auto" and not explicit_roots and provider_unavailable:
        result = _agent_discovery_result()
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(result["message"])
        return 0

    roots = explicit_roots or _codex_trajectory_roots()
    result = discover_skills(roots, args.days)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if not result["skills"]:
        print(f"No skill-use signals found in the last {args.days} days.")
        return 0
    print(f"Skills used in the last {args.days} days:")
    for index, skill in enumerate(result["skills"], start=1):
        print(f"{index}. {skill['name']} — {skill['sessionCount']} session(s), last used {skill['lastUsedAt']}")
    return 0


def _command_redact(args: argparse.Namespace) -> int:
    payload = _read_json_input(args.input)
    sanitized = sanitize_value(payload)
    errors = validate_payload(sanitized)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 2
    _write_private_json(args.output, sanitized)
    return 0


def _command_submit(args: argparse.Namespace) -> int:
    if not args.confirmed:
        print("error: submit requires --confirmed after the applicable user-review rule is satisfied", file=sys.stderr)
        return 2
    payload = _read_json_input(args.input)

    # submit 是本地-only 命令，不允许走对象存储，只能接受 inline 小附件
    attachment_paths = getattr(args, "attachment", []) or []
    if attachment_paths:
        try:
            feedback_id = payload.get("feedbackId") or str(uuid.uuid4())
            attachments = _process_attachments(
                attachment_paths,
                api_url=get_feedback_api_url(),
                token=get_api_token(),
                feedback_id=feedback_id,
                allow_storage=False,
            )
            payload["attachments"] = attachments
        except (FileNotFoundError, IsADirectoryError, RuntimeError, ValueError) as e:
            print(f"error: {e}", file=sys.stderr)
            return 2

    errors = validate_payload(payload)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 2
    sanitized = sanitize_value(payload)
    if sanitized != payload:
        print(
            "error: sensitive-looking content remains; run redact and repeat user review if displayed fields change",
            file=sys.stderr,
        )
        return 3
    now = datetime.now(timezone.utc)
    record = {
        "schemaVersion": SCHEMA_VERSION,
        "feedbackId": str(uuid.uuid4()),
        "savedAt": _iso_utc(now),
        "transport": "local-outbox",
        "consent": {"confirmed": True, "confirmedAt": _iso_utc(now)},
        "uploadAttempts": [],
        "payload": payload,
    }
    outbox = Path(args.outbox).expanduser()
    _append_private_jsonl(outbox, record)
    print(json.dumps({"saved": True, "feedbackId": record["feedbackId"], "outbox": str(outbox)}, ensure_ascii=False))
    return 0


def _command_upload(args: argparse.Namespace) -> int:
    """上传评价到远程服务器。

    从 --input 读取单条记录，上传到服务器。
    与 submit 命令对称：submit 保存到本地 outbox，upload 上传到远程。
    同样要求 --confirmed 且执行完整脱敏检查。
    """
    if not args.confirmed:
        print("error: upload requires --confirmed after the applicable user-review rule is satisfied", file=sys.stderr)
        return 2

    # 读取输入文件
    try:
        if args.input == "-":
            record = json.load(sys.stdin)
        else:
            with Path(args.input).expanduser().open(encoding="utf-8") as f:
                record = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, OSError) as e:
        print(json.dumps({"error": f"无法读取输入文件: {e}"}, ensure_ascii=False), file=sys.stderr)
        return 2

    # 支持两种格式：完整的 outbox 记录（含 payload 等）或纯评价 payload
    if isinstance(record, dict) and "payload" in record:
        # 完整的 outbox 记录格式
        feedback_id = record.get("feedbackId", str(uuid.uuid4()))
        payload = record.get("payload", {})
        submitted_at = record.get("savedAt")
        consent = record.get("consent", {})
    else:
        # 纯评价 payload 格式（直接是 submit 前的格式）
        feedback_id = str(uuid.uuid4())
        payload = record
        submitted_at = _iso_utc(datetime.now(timezone.utc))
        consent = {"confirmed": True, "confirmedAt": submitted_at}

    # 处理附件：小文件 inline，大文件通过预签名 URL 上传到对象存储
    attachment_paths = getattr(args, "attachment", []) or []
    if attachment_paths:
        try:
            attachments = _process_attachments(
                attachment_paths,
                api_url=get_feedback_api_url(),
                token=get_api_token(),
                feedback_id=feedback_id,
                allow_storage=True,
            )
            payload["attachments"] = attachments
        except (FileNotFoundError, IsADirectoryError, RuntimeError, ValueError) as e:
            print(f"error: {e}", file=sys.stderr)
            return 2

    # 对所有输入执行统一校验和脱敏检查（无论来源格式）
    errors = validate_payload(payload)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 2
    sanitized = sanitize_value(payload)
    if sanitized != payload:
        print(
            "error: sensitive-looking content remains; run redact and repeat user review if displayed fields change",
            file=sys.stderr,
        )
        return 3

    # 构建上传 payload（脱敏后的 payload + 元数据）
    upload_payload = {
        **payload,
        "feedbackId": feedback_id,
        "submittedAt": submitted_at,
        "consent": consent,
    }

    # 执行上传
    result = _upload_feedback(upload_payload)

    now = datetime.now(timezone.utc)
    output = {
        "feedbackId": feedback_id,
        "success": result["success"],
        "apiUrl": get_feedback_api_url(),
    }

    if result["success"]:
        output["message"] = "上传成功"
        output["response"] = result.get("response")
        # 如果指定了 outbox，也保存到本地
        if args.outbox:
            outbox_record = {
                "schemaVersion": SCHEMA_VERSION,
                "feedbackId": feedback_id,
                "savedAt": submitted_at or _iso_utc(now),
                "transport": "remote-api",
                "consent": consent,
                "uploadAttempts": [{"at": _iso_utc(now), "success": True, "code": result["code"]}],
                "payload": payload,
            }
            outbox_path = Path(args.outbox).expanduser()
            _append_private_jsonl(outbox_path, outbox_record)
            output["outbox"] = str(outbox_path)
    else:
        output["error"] = result["message"]
        output["code"] = result["code"]
        # 如果指定了 outbox，保存失败记录以便重试
        if args.outbox:
            outbox_record = {
                "schemaVersion": SCHEMA_VERSION,
                "feedbackId": feedback_id,
                "savedAt": submitted_at or _iso_utc(now),
                "transport": "local-outbox",
                "consent": consent,
                "uploadAttempts": [{"at": _iso_utc(now), "success": False, "code": result["code"], "error": result["message"]}],
                "payload": payload,
            }
            outbox_path = Path(args.outbox).expanduser()
            _append_private_jsonl(outbox_path, outbox_record)
            output["outbox"] = str(outbox_path)
            output["message"] = f"上传失败，已保存到 outbox: {outbox_path}"

    print(json.dumps(output, ensure_ascii=False))
    return 0 if result["success"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Use known trajectory providers and stage sanitized feedback locally")
    subparsers = parser.add_subparsers(dest="command", required=True)

    providers = subparsers.add_parser("providers", help="Probe deterministic trajectory providers")
    providers.add_argument("--agent-type", help="Current Agent type; prevents selecting another Agent's provider")
    providers.add_argument("--format", choices=("text", "json"), default="text")
    providers.set_defaults(handler=_command_providers)

    discover = subparsers.add_parser("discover", help="List skill-use signals with a known trajectory provider")
    discover.add_argument("--days", type=int, default=30, choices=range(1, 366), metavar="1-365")
    discover.add_argument("--provider", choices=("auto", CODEX_PROVIDER_ID), default="auto")
    discover.add_argument("--agent-type", help="Current Agent type used to validate auto-selected providers")
    discover.add_argument(
        "--trajectory-root",
        action="append",
        default=[],
        help="Override a root containing Codex-format rollout JSONL; repeat as needed",
    )
    discover.add_argument("--format", choices=("text", "json"), default="text")
    discover.set_defaults(handler=_command_discover)

    redact = subparsers.add_parser("redact", help="Apply deterministic redaction and validate a feedback draft")
    redact.add_argument("--input", required=True, help="Draft JSON path, or - for stdin")
    redact.add_argument("--output", required=True, help="Sanitized JSON path, or - for stdout")
    redact.set_defaults(handler=_command_redact)

    submit = subparsers.add_parser("submit", help="Append an approved payload to the local outbox")
    submit.add_argument("--input", required=True, help="Approved sanitized JSON path, or - for stdin")
    submit.add_argument("--outbox", default=str(DEFAULT_OUTBOX), help="Local JSONL outbox path")
    submit.add_argument(
        "--attachment",
        action="append",
        default=[],
        help="Local file path to attach (repeatable); only files under the inline threshold are allowed for submit",
    )
    submit.add_argument(
        "--confirmed",
        action="store_true",
        help="Assert that the applicable user-review and consent requirements were satisfied",
    )
    submit.set_defaults(handler=_command_submit)

    upload = subparsers.add_parser("upload", help="Upload feedback from input file to remote server")
    upload.add_argument("--input", required=True, help="Feedback JSON path, or - for stdin")
    upload.add_argument("--outbox", help="Optional: also save to local outbox path on success/failure")
    upload.add_argument(
        "--attachment",
        action="append",
        default=[],
        help="Local file path to attach (repeatable); small files are inline, large files use a presigned URL",
    )
    upload.add_argument(
        "--confirmed",
        action="store_true",
        help="Assert that the applicable user-review and consent requirements were satisfied",
    )
    upload.set_defaults(handler=_command_upload)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
