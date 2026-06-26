#!/usr/bin/env python3
from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import json
import mimetypes
import os
import pathlib
import re
import sys
import tempfile
import time
import typing as t
import urllib.error
import urllib.parse
import urllib.request
import uuid

MAINLAND_CHINA_API_BASE_URL = "https://pc-api.pagepop.cn"
GLOBAL_API_BASE_URL = "https://pc-api.pagepop.ai"
DEFAULT_API_BASE_URL = GLOBAL_API_BASE_URL
DEFAULT_SKILL_ID = "pagepop-skill"
DEFAULT_CLIENT_NAME = "openclaw"
DEFAULT_CLIENT_VERSION = "1.0.0"
DEFAULT_DISPLAY_APP_NAME = "OpenClaw"
DEFAULT_CLIENT_TYPE = 11
DEFAULT_VERSION = "openclaw-v1"
DEFAULT_UPDATE_CHANNEL = "prod"
DEFAULT_POLL_TIMEOUT_SECONDS = 600
DEFAULT_STREAM_TIMEOUT_SECONDS = 300
DEFAULT_MAX_STREAM_RECONNECTS = 5
DEFAULT_IMAGE_DOWNLOAD_TIMEOUT_SECONDS = 30
DEFAULT_MAX_IMAGE_DOWNLOAD_BYTES = 25 * 1024 * 1024
IMAGE_DOWNLOAD_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
HEARTBEAT_PROGRESS_INTERVAL_SECONDS = 15
URL_TEXT_RE = re.compile(r"https?://[^\s<>()\"']+")
MAINLAND_CHINA_REGION_VALUES = {
    "cn",
    "chn",
    "china",
    "china-mainland",
    "cn-mainland",
    "mainland",
    "mainland-china",
    "mainland-cn",
    "prc",
    "zh-cn",
    "zh-hans-cn",
}
GLOBAL_REGION_VALUES = {
    "global",
    "intl",
    "international",
    "non-cn",
    "non-mainland",
    "outside-cn",
    "outside-mainland",
    "overseas",
    "world",
}
MAINLAND_CHINA_TIMEZONES = {
    "Asia/Beijing",
    "Asia/Shanghai",
    "Asia/Chongqing",
    "Asia/Harbin",
    "Asia/Urumqi",
}

SUCCESS_CODE = 1000
STATE_FILE_NAME = "state.json"
MANIFEST_FILE_NAME = "skill-manifest.json"
MANIFEST_TEMPLATE_FILE_NAME = "skill-manifest.template.json"
SOURCE_INSTALL_PACKAGE_VERSION = "source"
SOURCE_INSTALL_BUILD_SHA = "source"
SOURCE_INSTALL_REPO = "pagepop/skills"

KEY_RESET_REASONS = {
    "SKILL_KEY_INVALID",
    "SKILL_KEY_REVOKED",
    "SKILL_KEY_EXPIRED",
    "MEMBERSHIP_REQUIRED",
}

TERMINAL_CONTROL_COMMANDS = {"done", "error", "manual_retry", "cancled"}


class PagepopAPIError(RuntimeError):
    def __init__(
        self,
        *,
        code: int,
        message: str,
        reason: str = "",
        metadata: t.Optional[dict[str, t.Any]] = None,
        data: t.Any = None,
    ) -> None:
        super().__init__(message or reason or "pagepop api error")
        self.code = code
        self.message = message or ""
        self.reason = reason or ""
        self.metadata = metadata or {}
        self.data = data

    @property
    def openclaw_reason(self) -> str:
        value = self.metadata.get("openclaw_reason")
        return str(value).strip() if value is not None else ""

    def should_reset_access_key(self) -> bool:
        return self.openclaw_reason in KEY_RESET_REASONS

    def to_record(self) -> dict[str, t.Any]:
        return {
            "kind": "error",
            "code": self.code,
            "message": self.message,
            "reason": self.reason,
            "metadata": self.metadata,
            "data": self.data,
        }


class AuthorizationPending(RuntimeError):
    pass


class PagepopHTTPError(RuntimeError):
    def __init__(
        self,
        *,
        status: int,
        url: str,
        content_type: str,
        response_preview: str,
        parse_error: str = "",
    ) -> None:
        message = f"http {status} {url}"
        if parse_error:
            message += f": non-json response: {parse_error}"
        elif response_preview:
            message += f": {response_preview}"
        super().__init__(message)
        self.status = status
        self.url = url
        self.content_type = content_type
        self.response_preview = response_preview
        self.parse_error = parse_error

    def to_record(self) -> dict[str, t.Any]:
        return {
            "kind": "error",
            "code": "http_error",
            "message": str(self),
            "http_status": self.status,
            "url": self.url,
            "content_type": self.content_type,
            "response_preview": self.response_preview,
            "parse_error": self.parse_error,
        }


@dataclasses.dataclass
class PendingRun:
    goal: str
    artifact_type: str = "auto"
    links: list[str] = dataclasses.field(default_factory=list)
    conversation_id: str = ""
    created_at: str = dataclasses.field(default_factory=lambda: utc_now().isoformat())


@dataclasses.dataclass
class SkillManifest:
    skill_id: str
    package_version: str
    channel: str = DEFAULT_UPDATE_CHANNEL
    build_sha: str = ""
    repo: str = ""
    release_tag: str = ""
    published_at: str = ""


@dataclasses.dataclass
class PendingAuth:
    auth_session_id: str
    authorize_url: str
    expires_at: str = ""
    poll_interval_seconds: int = 3
    created_at: str = dataclasses.field(default_factory=lambda: utc_now().isoformat())


@dataclasses.dataclass
class SavedConversation:
    conversation_id: str
    label: str = ""
    last_goal: str = ""
    artifact_type: str = "auto"
    last_activity_at: str = dataclasses.field(default_factory=lambda: utc_now().isoformat())


@dataclasses.dataclass
class ConversationStreamState:
    cursor_offset: int = 0
    last_done_offset: int = 0
    last_terminal_command: str = ""
    updated_at: str = dataclasses.field(default_factory=lambda: utc_now().isoformat())


@dataclasses.dataclass
class SkillState:
    access_key: str = ""
    pending_run: t.Optional[PendingRun] = None
    pending_auth: t.Optional[PendingAuth] = None
    active_conversation_id: str = ""
    active_conversation_updated_at: str = ""
    saved_conversations: list[SavedConversation] = dataclasses.field(default_factory=list)
    conversation_streams: dict[str, ConversationStreamState] = dataclasses.field(default_factory=dict)
    updated_at: str = dataclasses.field(default_factory=lambda: utc_now().isoformat())

    @classmethod
    def from_dict(cls, raw: dict[str, t.Any]) -> "SkillState":
        pending_raw = raw.get("pending_run")
        pending_run = None
        if isinstance(pending_raw, dict):
            pending_run = PendingRun(
                goal=str(pending_raw.get("goal", "")).strip(),
                artifact_type=str(pending_raw.get("artifact_type", "auto")).strip() or "auto",
                links=[str(item).strip() for item in pending_raw.get("links", []) if str(item).strip()],
                conversation_id=str(pending_raw.get("conversation_id", "")).strip(),
                created_at=str(pending_raw.get("created_at", "")).strip() or utc_now().isoformat(),
            )
        pending_auth_raw = raw.get("pending_auth")
        pending_auth = None
        if isinstance(pending_auth_raw, dict):
            pending_auth = PendingAuth(
                auth_session_id=str(pending_auth_raw.get("auth_session_id", "")).strip(),
                authorize_url=str(pending_auth_raw.get("authorize_url", "")).strip(),
                expires_at=str(pending_auth_raw.get("expires_at", "")).strip(),
                poll_interval_seconds=int(pending_auth_raw.get("poll_interval_seconds", 3) or 3),
                created_at=str(pending_auth_raw.get("created_at", "")).strip() or utc_now().isoformat(),
            )
        saved_conversations: list[SavedConversation] = []
        saved_raw = raw.get("saved_conversations")
        if isinstance(saved_raw, list):
            for item in saved_raw:
                if not isinstance(item, dict):
                    continue
                conversation_id = str(item.get("conversation_id", "")).strip()
                if not conversation_id:
                    continue
                saved_conversations.append(
                    SavedConversation(
                        conversation_id=conversation_id,
                        label=str(item.get("label", "")).strip(),
                        last_goal=str(item.get("last_goal", "")).strip(),
                        artifact_type=str(item.get("artifact_type", "auto")).strip() or "auto",
                        last_activity_at=str(item.get("last_activity_at", "")).strip() or utc_now().isoformat(),
                    )
                )
        conversation_streams: dict[str, ConversationStreamState] = {}
        streams_raw = raw.get("conversation_streams")
        if isinstance(streams_raw, dict):
            for raw_conversation_id, item in streams_raw.items():
                conversation_id = str(raw_conversation_id).strip()
                if not conversation_id or not isinstance(item, dict):
                    continue
                try:
                    cursor_offset = int(item.get("cursor_offset", 0) or 0)
                except (TypeError, ValueError):
                    cursor_offset = 0
                try:
                    last_done_offset = int(item.get("last_done_offset", 0) or 0)
                except (TypeError, ValueError):
                    last_done_offset = 0
                conversation_streams[conversation_id] = ConversationStreamState(
                    cursor_offset=max(cursor_offset, 0),
                    last_done_offset=max(last_done_offset, 0),
                    last_terminal_command=str(item.get("last_terminal_command", "")).strip(),
                    updated_at=str(item.get("updated_at", "")).strip() or utc_now().isoformat(),
                )
        return cls(
            access_key=str(raw.get("access_key", "")).strip(),
            pending_run=pending_run,
            pending_auth=pending_auth if pending_auth and pending_auth.auth_session_id else None,
            active_conversation_id=str(raw.get("active_conversation_id", "")).strip(),
            active_conversation_updated_at=str(raw.get("active_conversation_updated_at", "")).strip(),
            saved_conversations=saved_conversations,
            conversation_streams=conversation_streams,
            updated_at=str(raw.get("updated_at", "")).strip() or utc_now().isoformat(),
        )

    def to_dict(self) -> dict[str, t.Any]:
        payload: dict[str, t.Any] = {
            "access_key": self.access_key,
            "updated_at": self.updated_at,
        }
        if self.pending_run is not None:
            payload["pending_run"] = dataclasses.asdict(self.pending_run)
        if self.pending_auth is not None:
            payload["pending_auth"] = dataclasses.asdict(self.pending_auth)
        if self.active_conversation_id:
            payload["active_conversation_id"] = self.active_conversation_id
        if self.active_conversation_updated_at:
            payload["active_conversation_updated_at"] = self.active_conversation_updated_at
        if self.saved_conversations:
            payload["saved_conversations"] = [dataclasses.asdict(item) for item in self.saved_conversations]
        if self.conversation_streams:
            payload["conversation_streams"] = {
                conversation_id: dataclasses.asdict(item)
                for conversation_id, item in sorted(self.conversation_streams.items())
            }
        return payload

    def masked_dict(self) -> dict[str, t.Any]:
        payload = self.to_dict()
        payload["access_key"] = mask_secret(self.access_key)
        return payload


@dataclasses.dataclass
class Config:
    api_base_url: str
    skill_id: str
    state_path: pathlib.Path
    region: str = ""
    region_context_missing: bool = False
    package_version: str = "dev"
    update_channel: str = DEFAULT_UPDATE_CHANNEL
    update_repo: str = ""
    update_release_tag: str = ""
    login_token_file: t.Optional[pathlib.Path] = None
    client_name: str = DEFAULT_CLIENT_NAME
    client_version: str = DEFAULT_CLIENT_VERSION
    source_app: str = ""
    display_app_name: str = DEFAULT_DISPLAY_APP_NAME
    return_mode: str = "manual"
    return_target: str = ""
    wait_for_authorization: bool = False
    artifact_dir: pathlib.Path = dataclasses.field(default_factory=lambda: pathlib.Path.cwd() / ".pagepop-artifacts")
    download_artifact_images: bool = True
    client_type: int = DEFAULT_CLIENT_TYPE
    version: str = DEFAULT_VERSION
    timezone: str = ""
    poll_timeout_seconds: int = DEFAULT_POLL_TIMEOUT_SECONDS
    stream_timeout_seconds: int = DEFAULT_STREAM_TIMEOUT_SECONDS
    max_stream_reconnects: int = DEFAULT_MAX_STREAM_RECONNECTS
    image_download_timeout_seconds: int = DEFAULT_IMAGE_DOWNLOAD_TIMEOUT_SECONDS
    max_image_download_bytes: int = DEFAULT_MAX_IMAGE_DOWNLOAD_BYTES


@dataclasses.dataclass
class SSEEvent:
    event: str
    raw_data: str
    data: t.Any


@dataclasses.dataclass
class StreamResult:
    conversation_id: str
    terminal_command: str
    last_offset: int


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def skill_root_dir() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def source_install_manifest() -> SkillManifest:
    return SkillManifest(
        skill_id=DEFAULT_SKILL_ID,
        package_version=SOURCE_INSTALL_PACKAGE_VERSION,
        channel=DEFAULT_UPDATE_CHANNEL,
        build_sha=SOURCE_INSTALL_BUILD_SHA,
        repo=SOURCE_INSTALL_REPO,
        release_tag="",
        published_at="",
    )


def load_skill_manifest() -> SkillManifest:
    root_dir = skill_root_dir()
    manifest_path = root_dir / MANIFEST_FILE_NAME
    try:
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        if (root_dir / MANIFEST_TEMPLATE_FILE_NAME).exists():
            return source_install_manifest()
        raise RuntimeError(f"skill manifest not found: {manifest_path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"skill manifest is invalid json: {manifest_path}") from exc

    if not isinstance(raw, dict):
        raise RuntimeError(f"skill manifest has unexpected shape: {manifest_path}")

    skill_id = str(raw.get("skill_id", "")).strip()
    package_version = str(raw.get("package_version", "")).strip()
    if not skill_id:
        raise RuntimeError(f"skill manifest missing skill_id: {manifest_path}")
    if not package_version:
        raise RuntimeError(f"skill manifest missing package_version: {manifest_path}")

    return SkillManifest(
        skill_id=skill_id,
        package_version=package_version,
        channel=str(raw.get("channel", DEFAULT_UPDATE_CHANNEL)).strip() or DEFAULT_UPDATE_CHANNEL,
        build_sha=str(raw.get("build_sha", "")).strip(),
        repo=str(raw.get("repo", "")).strip(),
        release_tag=str(raw.get("release_tag", "")).strip(),
        published_at=str(raw.get("published_at", "")).strip(),
    )


def mask_secret(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if len(value) <= 8:
        return "***"
    return value[:4] + "***" + value[-4:]


def emit_record(payload: dict[str, t.Any]) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def emit_event(kind: str, **payload: t.Any) -> None:
    emit_record({"kind": kind, **payload})


def compact_whitespace(value: str) -> str:
    return " ".join(value.split())


def truncate_text(value: str, max_len: int = 160) -> str:
    value = compact_whitespace(value.strip())
    if len(value) <= max_len:
        return value
    return value[: max_len - 3].rstrip() + "..."


def first_non_empty(*values: t.Any) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def first_non_null(*values: t.Any) -> t.Any:
    for value in values:
        if value is not None and value != "":
            return value
    return None


def dedupe_strings(values: t.Iterable[str], *, limit: int = 20) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
        if len(result) >= limit:
            break
    return result


def collect_urls(value: t.Any) -> list[str]:
    urls: list[str] = []

    def visit(node: t.Any) -> None:
        if isinstance(node, str):
            raw = node.strip()
            if raw.startswith(("http://", "https://")):
                urls.append(raw)
            return
        if isinstance(node, dict):
            for child in node.values():
                visit(child)
            return
        if isinstance(node, list):
            for child in node:
                visit(child)

    visit(value)
    return dedupe_strings(urls)


def clip_text(value: str, max_len: int = 4000) -> str:
    value = value.strip()
    if len(value) <= max_len:
        return value
    return value[:max_len].rstrip()


def build_saved_conversation_label(*, goal: str, artifact_type: str) -> str:
    goal_text = truncate_text(goal, max_len=60)
    if goal_text:
        return goal_text
    artifact_text = humanize_artifact_type(artifact_type)
    if artifact_text:
        return f"{artifact_text.title()} chat"
    return "Conversation"


def upsert_saved_conversation(
    saved_conversations: list[SavedConversation],
    *,
    conversation_id: str,
    goal: str,
    artifact_type: str,
    limit: int = 20,
) -> list[SavedConversation]:
    conversation_id = conversation_id.strip()
    if not conversation_id:
        return saved_conversations
    next_item = SavedConversation(
        conversation_id=conversation_id,
        label=build_saved_conversation_label(goal=goal, artifact_type=artifact_type),
        last_goal=goal.strip(),
        artifact_type=artifact_type.strip() or "auto",
        last_activity_at=utc_now().isoformat(),
    )
    items = [item for item in saved_conversations if item.conversation_id != conversation_id]
    items.insert(0, next_item)
    return items[:limit]


def normalize_sse_offset(value: t.Any) -> int:
    try:
        offset = int(value)
    except (TypeError, ValueError):
        return 0
    return max(offset, 0)


def normalize_user_region(value: str) -> str:
    normalized = value.strip().lower().replace("_", "-")
    if not normalized:
        return ""
    if normalized in MAINLAND_CHINA_REGION_VALUES:
        return "CN"
    if normalized in GLOBAL_REGION_VALUES:
        return "GLOBAL"
    if len(normalized) == 2 and normalized.isalpha():
        return normalized.upper()
    return normalized


def infer_user_region_from_timezone(timezone: str) -> str:
    timezone = timezone.strip()
    if not timezone:
        return ""
    if timezone in MAINLAND_CHINA_TIMEZONES:
        return "CN"
    return "GLOBAL"


def resolve_user_region(region: str, timezone: str) -> str:
    return normalize_user_region(region) or infer_user_region_from_timezone(timezone)


def resolve_api_base_url(explicit_api_base_url: str, *, region: str, timezone: str) -> str:
    explicit_api_base_url = explicit_api_base_url.strip()
    if explicit_api_base_url:
        return explicit_api_base_url.rstrip("/")
    resolved_region = resolve_user_region(region, timezone)
    if resolved_region == "CN":
        return MAINLAND_CHINA_API_BASE_URL
    return GLOBAL_API_BASE_URL


def get_conversation_stream_state(state: SkillState, conversation_id: str) -> ConversationStreamState:
    conversation_id = conversation_id.strip()
    if not conversation_id:
        return ConversationStreamState()
    stream_state = state.conversation_streams.get(conversation_id)
    if stream_state is None:
        stream_state = ConversationStreamState()
        state.conversation_streams[conversation_id] = stream_state
    return stream_state


def update_conversation_stream_state(
    state: SkillState,
    *,
    conversation_id: str,
    cursor_offset: int,
    terminal_command: str = "",
) -> ConversationStreamState:
    stream_state = get_conversation_stream_state(state, conversation_id)
    normalized_offset = normalize_sse_offset(cursor_offset)
    stream_state.cursor_offset = normalized_offset
    terminal_command = terminal_command.strip()
    if terminal_command:
        stream_state.last_terminal_command = terminal_command
    if terminal_command == "done":
        stream_state.last_done_offset = normalized_offset
    stream_state.updated_at = utc_now().isoformat()
    return stream_state


def conversation_stream_payload(stream_state: t.Optional[ConversationStreamState]) -> dict[str, t.Any]:
    if stream_state is None:
        return {
            "sse_cursor_offset": 0,
            "last_done_offset": 0,
            "last_terminal_command": "",
            "sse_cursor_updated_at": "",
        }
    return {
        "sse_cursor_offset": stream_state.cursor_offset,
        "last_done_offset": stream_state.last_done_offset,
        "last_terminal_command": stream_state.last_terminal_command,
        "sse_cursor_updated_at": stream_state.updated_at,
    }


def build_conversation_history_items(
    saved_conversations: list[SavedConversation],
    conversation_streams: t.Optional[dict[str, ConversationStreamState]] = None,
) -> list[dict[str, t.Any]]:
    streams = conversation_streams or {}
    items: list[dict[str, t.Any]] = []
    for item in saved_conversations:
        payload = {
            "conversation_id": item.conversation_id,
            "label": item.label,
            "last_goal": item.last_goal,
            "artifact_type": item.artifact_type,
            "last_activity_at": item.last_activity_at,
        }
        payload.update(conversation_stream_payload(streams.get(item.conversation_id)))
        items.append(payload)
    return items


def build_chat_context_payload(
    *,
    mode: str,
    state: SkillState,
    conversation_id: str = "",
) -> dict[str, t.Any]:
    active_item = None
    if conversation_id:
        active_item = next((item for item in state.saved_conversations if item.conversation_id == conversation_id), None)
    title = "Continuing current chat" if mode == "continue" else "Starting a new chat"
    message = (
        "This request will continue your current PagePop conversation by default."
        if mode == "continue"
        else "This request will start a fresh PagePop conversation without reusing the previous context."
    )
    return {
        "mode": mode,
        "conversation_id": conversation_id,
        "label": active_item.label if active_item is not None else "",
        "last_goal": active_item.last_goal if active_item is not None else "",
        "saved_conversation_count": len(state.saved_conversations),
        "actions": [
            {"id": "new_chat", "label": "New chat"},
            {"id": "switch_chat", "label": "Switch chat"},
        ],
        "title": title,
        "message": message,
        "result_hint": (
            "Use New chat for a clean context, or list saved conversations and choose one to continue."
        ),
    }


def extract_page_count(payload: t.Any) -> t.Optional[int]:
    if not isinstance(payload, dict):
        return None
    for key in ("slides", "image_list", "images", "pages"):
        value = payload.get(key)
        if isinstance(value, list) and value:
            return len(value)
    return None


def is_image_url(url: str) -> bool:
    path = urllib.parse.urlparse(url).path.lower()
    return path.endswith((".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg"))


def replace_image_urls_for_display(value: str, image_urls: list[str]) -> str:
    image_url_set = {url.strip().strip("<>") for url in image_urls if url.strip()}
    if not value.strip() or not image_url_set:
        return value

    def replace(match: re.Match[str]) -> str:
        url = match.group(0).strip().strip("<>")
        if url in image_url_set:
            return "已随图片消息发送"
        return match.group(0)

    return URL_TEXT_RE.sub(replace, value).replace("<已随图片消息发送>", "已随图片消息发送")


def build_resource_links(urls: list[str]) -> list[dict[str, str]]:
    resources: list[dict[str, str]] = []
    for url in urls:
        path = urllib.parse.urlparse(url).path.lower()
        label = ""
        if path.endswith(".json"):
            label = "Export JSON"
        elif path.endswith(".docx"):
            label = "DOCX file"
        elif path.endswith(".pdf"):
            label = "PDF file"
        elif path.endswith((".ppt", ".pptx")):
            label = "PPT file"
        if label:
            resources.append({"label": label, "url": url})
    return resources


def resolve_pagepop_web_base_url(api_base_url: str) -> str:
    parsed = urllib.parse.urlparse(api_base_url.strip())
    host = parsed.netloc.strip().lower()
    scheme = parsed.scheme or "https"
    if not host:
        return ""

    local_hosts = {
        "127.0.0.1",
        "localhost",
        "127.0.0.1:10086",
        "localhost:10086",
    }
    if host in local_hosts:
        return "http://127.0.0.1:11073"

    for api_prefix, web_prefix in (
        ("skills-pc-api.", "www."),
        ("pc-api.", "www."),
    ):
        if host.startswith(api_prefix):
            return f"{scheme}://{web_prefix}{host[len(api_prefix):]}"
    return ""


def is_local_pagepop_host(host: str) -> bool:
    return host.strip().lower() in {
        "127.0.0.1",
        "localhost",
        "127.0.0.1:11073",
        "localhost:11073",
    }


def build_pagepop_project_url(api_base_url: str, conversation_id: str) -> str:
    conversation_id = conversation_id.strip()
    if not conversation_id:
        return ""
    web_base_url = resolve_pagepop_web_base_url(api_base_url)
    if not web_base_url:
        return ""
    params = urllib.parse.urlencode({"cid": conversation_id})
    return f"{web_base_url}/project?{params}"


def extract_message_text(payload: t.Any) -> str:
    if not isinstance(payload, dict):
        return ""
    if str(payload.get("type", "")).strip() != "message":
        return ""
    value = payload.get("data")
    if isinstance(value, str):
        return clip_text(value)
    return ""


def extract_suggestion_actions(payload: t.Any) -> list[str]:
    if not isinstance(payload, dict):
        return []
    if str(payload.get("type", "")).strip() != "tool_call":
        return []
    if str(payload.get("status", "")).strip() != "done":
        return []
    if str(payload.get("name", "")).strip() not in {"suggestion", "suggestion_tool"}:
        return []
    data = payload.get("data") if isinstance(payload.get("data"), dict) else {}
    raw_items = []
    for key in ("tags", "list"):
        value = data.get(key) if isinstance(data, dict) else None
        if isinstance(value, list):
            raw_items.extend(str(item).strip() for item in value if str(item).strip())
    return dedupe_strings(raw_items, limit=10)


def humanize_artifact_type(value: str) -> str:
    mapping = {
        "slide": "slides",
        "slides": "slides",
        "designer": "design",
        "basic_image_ops": "image result",
        "rednote": "rednote post",
        "official-account-layout": "article layout",
        "file": "file",
        "word": "document",
    }
    key = value.strip().lower()
    return mapping.get(key, key.replace("_", " ") or "artifact")


def humanize_tool_name(value: str) -> str:
    key = value.strip()
    if not key:
        return "tool"
    mapping = {
        "finish_work": "final artifact generation",
        "suggestion": "suggestion generation",
        "suggestion_tool": "suggestion generation",
        "search_web": "web search",
        "read_url": "content reading",
        "crawler": "content reading",
        "think_tool": "reasoning",
    }
    return mapping.get(key, key.replace("_", " "))


def map_finish_work_type(value: str) -> str:
    mapping = {
        "slides": "slide",
        "slide": "slide",
        "designer": "designer",
        "basic_image_ops": "basic_image_ops",
        "rednote": "rednote",
        "official-account-layout": "official-account-layout",
        "file": "file",
        "word": "word",
    }
    key = value.strip().lower()
    return mapping.get(key, key)


def build_progress_record(
    *,
    conversation_id: str,
    stage: str,
    summary: str,
    event: str,
    status: str = "",
    raw_type: str = "",
    name: str = "",
) -> dict[str, t.Any]:
    return {
        "kind": "progress_update",
        "conversation_id": conversation_id,
        "stage": stage,
        "status": status,
        "event": event,
        "raw_type": raw_type,
        "name": name,
        "summary": summary,
    }


def summarize_progress_event(event: str, payload: t.Any) -> t.Optional[dict[str, t.Any]]:
    if not isinstance(payload, dict):
        return None

    conversation_id = str(payload.get("conversation_id", "")).strip()
    raw_type = str(payload.get("type", "")).strip()

    if event == "control":
        cmd = str(payload.get("cmd", "")).strip()
        if cmd == "retry":
            return build_progress_record(
                conversation_id=conversation_id,
                stage="retry",
                status=cmd,
                event=event,
                raw_type=raw_type,
                summary="PagePop asked the client to retry the stream.",
            )
        if cmd == "done":
            return build_progress_record(
                conversation_id=conversation_id,
                stage="completed",
                status=cmd,
                event=event,
                raw_type=raw_type,
                summary="PagePop finished streaming all events.",
            )
        if cmd == "error":
            return build_progress_record(
                conversation_id=conversation_id,
                stage="error",
                status=cmd,
                event=event,
                raw_type=raw_type,
                summary="PagePop reported an error while streaming results.",
            )
        return None

    if raw_type == "tool_call":
        name = str(payload.get("name", "")).strip()
        status = str(payload.get("status", "")).strip()
        tool_name = humanize_tool_name(name)
        data = payload.get("data") if isinstance(payload.get("data"), dict) else {}
        detail = first_non_empty(
            str(data.get("title", "")).strip() if isinstance(data, dict) else "",
            str(data.get("tool_display_name", "")).strip() if isinstance(data, dict) else "",
        )
        detail_suffix = f" ({detail})" if detail else ""
        summary_map = {
            "begin": f"PagePop started {tool_name}{detail_suffix}.",
            "running": f"PagePop is running {tool_name}{detail_suffix}.",
            "done": f"PagePop finished {tool_name}{detail_suffix}.",
            "failed": f"PagePop failed while running {tool_name}{detail_suffix}.",
            "paused": f"PagePop paused {tool_name}{detail_suffix}.",
        }
        if status in summary_map:
            return build_progress_record(
                conversation_id=conversation_id,
                stage="tool",
                status=status,
                event=event,
                raw_type=raw_type,
                name=name,
                summary=summary_map[status],
            )
        return None

    if raw_type == "artifact":
        artifact = payload.get("artifact") if isinstance(payload.get("artifact"), dict) else {}
        artifact_type = humanize_artifact_type(str(artifact.get("artifact_type", "")).strip())
        lifecycle = str(artifact.get("type", "")).strip()
        stage = str(artifact.get("stage", "")).strip()
        title = first_non_empty(
            str((artifact.get("payload") or {}).get("title", "")).strip()
            if isinstance(artifact.get("payload"), dict)
            else "",
        )
        title_suffix = f" ({title})" if title else ""
        if lifecycle.endswith("done") or stage == "report":
            summary = f"PagePop finished the {artifact_type}{title_suffix}."
        else:
            summary = f"PagePop is generating the {artifact_type}{title_suffix}."
        return build_progress_record(
            conversation_id=conversation_id,
            stage="artifact",
            status=lifecycle or stage,
            event=event,
            raw_type=raw_type,
            name=str(payload.get("name", "")).strip(),
            summary=summary,
        )

    return None


def build_artifact_summary(payload: t.Any) -> t.Optional[dict[str, t.Any]]:
    if not isinstance(payload, dict):
        return None

    conversation_id = str(payload.get("conversation_id", "")).strip()
    message_id = str(payload.get("message_id", "")).strip()
    raw_type = str(payload.get("type", "")).strip()

    if raw_type == "artifact":
        artifact = payload.get("artifact") if isinstance(payload.get("artifact"), dict) else {}
        if not artifact:
            return None
        artifact_payload = artifact.get("payload") if isinstance(artifact.get("payload"), dict) else {}
        artifact_type = str(artifact.get("artifact_type", "")).strip()
        lifecycle = str(artifact.get("type", "")).strip()
        stage = str(artifact.get("stage", "")).strip()
        text_content = clip_text(first_non_empty(str(artifact_payload.get("content", "")).strip()))
        return {
            "source": "artifact",
            "conversation_id": conversation_id,
            "message_id": message_id,
            "artifact_id": str(artifact.get("artifact_id", "")).strip(),
            "artifact_type": artifact_type,
            "scope_id": str(artifact.get("scope_id", "")).strip(),
            "status": lifecycle or stage,
            "title": first_non_empty(
                str(artifact_payload.get("title", "")).strip(),
                str(payload.get("title", "")).strip(),
            ),
            "text_content": text_content,
            "text_preview": truncate_text(text_content),
            "current_version": first_non_null(
                artifact_payload.get("currentVersion"),
                artifact_payload.get("version_id"),
                artifact_payload.get("version"),
            ),
            "page_count": extract_page_count(artifact_payload),
            "urls": collect_urls(artifact_payload),
            "ready": lifecycle.endswith("done") or stage == "report",
        }

    if raw_type == "tool_call" and str(payload.get("name", "")).strip() == "finish_work":
        data = payload.get("data") if isinstance(payload.get("data"), dict) else {}
        nested_data = data.get("data") if isinstance(data.get("data"), dict) else {}
        artifact_type = map_finish_work_type(str(data.get("type", "")).strip())
        text_content = clip_text(
            first_non_empty(
                str(data.get("content", "")).strip(),
                str(nested_data.get("content", "")).strip(),
            )
        )
        return {
            "source": "finish_work",
            "conversation_id": conversation_id,
            "message_id": message_id,
            "artifact_id": first_non_empty(
                str(data.get("artifact_id", "")).strip(),
                str(nested_data.get("artifact_id", "")).strip(),
                str(nested_data.get("outline_id", "")).strip(),
            ),
            "artifact_type": artifact_type,
            "scope_id": "",
            "status": str(payload.get("status", "")).strip(),
            "title": first_non_empty(
                str(data.get("title", "")).strip(),
                str(nested_data.get("title", "")).strip(),
            ),
            "text_content": text_content,
            "text_preview": truncate_text(text_content),
            "current_version": first_non_null(
                nested_data.get("currentVersion"),
                nested_data.get("version_id"),
                nested_data.get("version"),
                data.get("version"),
            ),
            "page_count": first_non_null(
                extract_page_count(nested_data),
                extract_page_count(data),
            ),
            "urls": collect_urls(nested_data or data),
            "ready": str(payload.get("status", "")).strip() == "done",
        }

    return None


def artifact_summary_key(summary: dict[str, t.Any]) -> str:
    return "|".join(
        [
            str(summary.get("source", "")),
            str(summary.get("conversation_id", "")),
            str(summary.get("message_id", "")),
            str(summary.get("artifact_id", "")),
            str(summary.get("artifact_type", "")),
        ]
    )


def merge_artifact_summary(base: t.Optional[dict[str, t.Any]], update: dict[str, t.Any]) -> dict[str, t.Any]:
    if base is None:
        merged = dict(update)
        merged["urls"] = dedupe_strings([str(item) for item in update.get("urls", []) if str(item).strip()])
        return merged

    merged = dict(base)
    for key, value in update.items():
        if key == "urls":
            merged["urls"] = dedupe_strings(
                [str(item) for item in base.get("urls", []) if str(item).strip()]
                + [str(item) for item in update.get("urls", []) if str(item).strip()]
            )
            continue
        if value in ("", None, [], {}):
            continue
        if key == "ready":
            merged[key] = bool(base.get("ready")) or bool(value)
            continue
        merged[key] = value
    return merged


def build_delivery_fallback_text(
    *,
    headline: str,
    subtitle: str,
    summary: str,
    actions: list[str],
    pagepop_project_url: str,
) -> str:
    parts = [headline]
    if subtitle:
        parts.append(subtitle)
    if summary:
        parts.append(summary)
    if actions:
        parts.append("You can continue with: " + "; ".join(actions[:3]))
    if pagepop_project_url:
        parts.append("Open in PagePop for the full rendered view: " + pagepop_project_url)
    return "\n".join(parts)


def normalize_channel_name(value: str) -> str:
    normalized = value.strip().lower().replace("-", "_")
    aliases = {
        "lark": "feishu",
        "feishu_bot": "feishu",
        "lark_bot": "feishu",
        "slack_bot": "slack",
    }
    return aliases.get(normalized, normalized)


def truncate_plain_text(value: str, max_len: int) -> str:
    value = compact_whitespace(value.strip())
    if len(value) <= max_len:
        return value
    return value[: max_len - 1].rstrip() + "…"


def slack_escape(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def feishu_safe_url(value: str) -> str:
    # Feishu lark_md auto-linking may stop at underscores in bare URLs.
    # Percent-encoding keeps the target equivalent while avoiding that tokenizer edge.
    return value.strip().replace("_", "%5F")


def feishu_safe_text_urls(value: str) -> str:
    return URL_TEXT_RE.sub(lambda match: feishu_safe_url(match.group(0)), value)


def build_feishu_plain_text(presentation: dict[str, t.Any]) -> str:
    headline = str(presentation.get("headline", "")).strip()
    subtitle = str(presentation.get("subtitle", "")).strip()
    full_text = str(presentation.get("full_text", "")).strip()
    summary = str(presentation.get("summary", "")).strip()
    actions = [str(item).strip() for item in presentation.get("actions", []) if str(item).strip()]
    resources = [
        item for item in presentation.get("resources", []) if isinstance(item, dict) and str(item.get("url", "")).strip()
    ]

    parts: list[str] = []
    if headline:
        parts.append(headline)
    if subtitle:
        parts.append(subtitle)
    if full_text:
        parts.append(feishu_safe_text_urls(full_text))
    elif summary:
        parts.append(feishu_safe_text_urls(summary))
    if resources:
        resource_lines = []
        for resource in resources[:5]:
            label = first_non_empty(str(resource.get("label", "")).strip(), "Resource")
            resource_lines.append(f"{label}: {feishu_safe_url(str(resource.get('url', '')).strip())}")
        parts.append("\n".join(resource_lines))
    if actions:
        parts.append("可以继续调整：\n" + "\n".join(f"- {feishu_safe_text_urls(item)}" for item in actions[:3]))
    return "\n\n".join(parts)


def build_local_image_messages(image_attachments: list[dict[str, t.Any]]) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    for attachment in image_attachments:
        local_path = str(attachment.get("local_path", "")).strip()
        if not local_path:
            continue
        messages.append(
            {
                "type": "local_image",
                "path": local_path,
                "alt_text": str(attachment.get("label", "")).strip() or "PagePop image",
                "mime_type": str(attachment.get("mime_type", "")).strip(),
            }
        )
    return messages


def build_slack_blocks(presentation: dict[str, t.Any]) -> list[dict[str, t.Any]]:
    headline = str(presentation.get("headline", "")).strip()
    subtitle = str(presentation.get("subtitle", "")).strip()
    summary = str(presentation.get("summary", "")).strip()
    preview_images = [str(url).strip() for url in presentation.get("preview_images", []) if str(url).strip()]
    actions = [str(item).strip() for item in presentation.get("actions", []) if str(item).strip()]
    resources = [
        item for item in presentation.get("resources", []) if isinstance(item, dict) and str(item.get("url", "")).strip()
    ]

    blocks: list[dict[str, t.Any]] = []
    if headline:
        blocks.append(
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": truncate_plain_text(headline, 150),
                    "emoji": True,
                },
            }
        )
    if subtitle:
        blocks.append(
            {
                "type": "context",
                "elements": [{"type": "mrkdwn", "text": slack_escape(truncate_plain_text(subtitle, 300))}],
            }
        )
    if summary:
        blocks.append(
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": slack_escape(truncate_plain_text(summary, 2800))},
            }
        )
    for index, image_url in enumerate(preview_images[:3], start=1):
        blocks.append(
            {
                "type": "image",
                "image_url": image_url,
                "alt_text": truncate_plain_text(headline or f"PagePop preview {index}", 200),
            }
        )
    if actions:
        next_steps = "\n".join(f"• {slack_escape(truncate_plain_text(item, 220))}" for item in actions[:3])
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": f"*Try next:*\n{next_steps}"}})

    buttons: list[dict[str, t.Any]] = []
    for index, resource in enumerate(resources[:3]):
        label = first_non_empty(str(resource.get("label", "")).strip(), f"Open resource {index + 1}")
        button: dict[str, t.Any] = {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": truncate_plain_text(label, 75),
                "emoji": True,
            },
            "url": str(resource.get("url", "")).strip(),
        }
        if index == 0:
            button["style"] = "primary"
        buttons.append(button)
    if buttons:
        blocks.append({"type": "actions", "elements": buttons})

    return blocks


def build_feishu_card(presentation: dict[str, t.Any]) -> dict[str, t.Any]:
    headline = str(presentation.get("headline", "")).strip()
    subtitle = str(presentation.get("subtitle", "")).strip()
    summary = str(presentation.get("summary", "")).strip()
    actions = [str(item).strip() for item in presentation.get("actions", []) if str(item).strip()]
    resources = [
        item for item in presentation.get("resources", []) if isinstance(item, dict) and str(item.get("url", "")).strip()
    ]

    text_parts = []
    if subtitle:
        text_parts.append(f"**{subtitle}**")
    if summary:
        text_parts.append(feishu_safe_text_urls(summary))

    elements: list[dict[str, t.Any]] = []
    if text_parts:
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": "\n\n".join(text_parts)}})
    if actions:
        next_steps = "\n".join(f"- {feishu_safe_text_urls(truncate_plain_text(item, 220))}" for item in actions[:3])
        elements.append({"tag": "hr"})
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": f"**可以继续调整：**\n{next_steps}"}})

    buttons: list[dict[str, t.Any]] = []
    for index, resource in enumerate(resources[:3]):
        label = first_non_empty(str(resource.get("label", "")).strip(), f"打开资源 {index + 1}")
        buttons.append(
            {
                "tag": "button",
                "text": {"tag": "plain_text", "content": truncate_plain_text(label, 40)},
                "url": feishu_safe_url(str(resource.get("url", "")).strip()),
                "type": "primary" if index == 0 else "default",
            }
        )
    if buttons:
        elements.append({"tag": "action", "actions": buttons})

    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "template": "blue",
            "title": {
                "tag": "plain_text",
                "content": truncate_plain_text(headline or "PagePop artifact ready", 80),
            },
        },
        "elements": elements,
    }


def build_channel_presentations(
    presentation: dict[str, t.Any],
    *,
    source_app: str,
    image_attachments: t.Optional[list[dict[str, t.Any]]] = None,
) -> dict[str, t.Any]:
    preview_images = [str(url).strip() for url in presentation.get("preview_images", []) if str(url).strip()]
    attachments = image_attachments or []
    local_image_messages = build_local_image_messages(attachments)
    fallback_text = str(presentation.get("fallback_text", "")).strip()
    preferred_channel = normalize_channel_name(source_app)
    return {
        "preferred": preferred_channel,
        "slack": {
            "format": "slack_block_kit",
            "fallback_text": fallback_text,
            "blocks": build_slack_blocks(presentation),
        },
        "feishu": {
            "format": "feishu_interactive_card",
            "fallback_text": feishu_safe_text_urls(fallback_text),
            "plain_text": build_feishu_plain_text(presentation),
            "card": build_feishu_card(presentation),
            "media": {
                "preview_image_urls": preview_images,
                "image_attachments": attachments,
                "local_image_messages": local_image_messages,
                "image_message_required": bool(preview_images),
                "image_upload_required": bool(preview_images),
                "text_should_omit_image_urls": True,
            },
            "host_instruction": (
                "Send local_image_messages as Feishu image messages, then send plain_text. "
                "Do not paste source image URLs into lark_md."
            ),
        },
    }


def build_artifact_delivery(
    summary: dict[str, t.Any],
    *,
    api_base_url: str,
    latest_text_message: str,
    suggestions: list[str],
    source_app: str = "",
    image_attachments: t.Optional[list[dict[str, t.Any]]] = None,
) -> dict[str, t.Any]:
    artifact_type = str(summary.get("artifact_type", "")).strip()
    type_label = humanize_artifact_type(artifact_type).title()
    title = first_non_empty(str(summary.get("title", "")).strip(), type_label or "Generated artifact")
    image_urls = [url for url in summary.get("urls", []) if is_image_url(str(url))]
    resource_links = build_resource_links([str(url) for url in summary.get("urls", []) if str(url).strip()])
    page_count = first_non_null(summary.get("page_count"))
    status = first_non_empty(str(summary.get("status", "")).strip(), "done")
    conversation_id = str(summary.get("conversation_id", "")).strip()
    pagepop_project_url = build_pagepop_project_url(api_base_url, conversation_id)
    text_content = first_non_empty(
        str(summary.get("text_content", "")).strip(),
        latest_text_message,
    )
    copyable_text = replace_image_urls_for_display(text_content, image_urls)
    summary_text = replace_image_urls_for_display(
        first_non_empty(
            str(summary.get("text_preview", "")).strip(),
            copyable_text,
        ),
        image_urls,
    )
    summary_text = truncate_text(summary_text, max_len=220)
    display_text = feishu_safe_text_urls(copyable_text)
    display_copyable_text = display_text
    display_summary_text = feishu_safe_text_urls(summary_text)

    subtitle_parts = [type_label] if type_label else []
    if isinstance(page_count, int) and page_count > 0:
        subtitle_parts.append(f"{page_count} page{'s' if page_count > 1 else ''}")
    subtitle = " · ".join(subtitle_parts)

    headline = f'Generated "{title}"'
    preview_images = image_urls[:3]
    actions = suggestions[:3]
    fallback_text = build_delivery_fallback_text(
        headline=headline,
        subtitle=subtitle,
        summary=summary_text,
        actions=actions,
        pagepop_project_url=pagepop_project_url,
    )

    presentation_resources = list(resource_links)
    if pagepop_project_url:
        presentation_resources.insert(
            0,
            {
                "label": "Open in PagePop",
                "url": pagepop_project_url,
            },
        )

    artifact = {
        "id": str(summary.get("artifact_id", "")).strip(),
        "type": artifact_type,
        "title": title,
        "status": status,
        "pages": page_count,
        "current_version": summary.get("current_version"),
        "text": text_content,
        "copyable_text": copyable_text,
        "text_preview": summary_text,
        "display_text": display_text,
        "display_copyable_text": display_copyable_text,
        "display_text_preview": display_summary_text,
        "image_urls": image_urls,
        "image_attachments": image_attachments or [],
        "resource_links": resource_links,
        "pagepop_project_url": pagepop_project_url,
        "ready": bool(summary.get("ready")),
    }

    presentation = {
        "headline": headline,
        "subtitle": subtitle,
        "full_text": copyable_text,
        "summary": summary_text,
        "display_summary": display_summary_text,
        "preview_images": preview_images,
        "image_attachments": image_attachments or [],
        "actions": actions,
        "resources": presentation_resources,
        "fallback_text": fallback_text,
    }

    debug = {
        "conversation_id": conversation_id,
        "message_id": str(summary.get("message_id", "")).strip(),
        "artifact_id": str(summary.get("artifact_id", "")).strip(),
        "source": str(summary.get("source", "")).strip(),
        "scope_id": str(summary.get("scope_id", "")).strip(),
    }

    return {
        "kind": "artifact_delivery",
        "conversation_id": debug["conversation_id"],
        "artifact": artifact,
        "presentation": presentation,
        "attachments": {
            "images": image_attachments or [],
            "send_images_as": "image_message",
        },
        "channel_presentations": build_channel_presentations(
            presentation,
            source_app=source_app,
            image_attachments=image_attachments,
        ),
        "target": {
            "source_app": source_app,
            "preferred_channel": normalize_channel_name(source_app),
        },
        "host_instruction": (
            "If local image attachments are present, send them as image messages and send the structured text separately. "
            "Keep source image URLs out of chat markdown."
        ),
        "debug": debug,
    }


def build_authorize_prompt(*, authorize_url: str, is_reauth: bool) -> dict[str, t.Any]:
    host_instruction = (
        "Display authorize_url to the user and stop this run. "
        "After the user completes authorization in the browser, invoke the same skill command again."
    )
    if is_reauth:
        return {
            "title": "PagePop authorization expired",
            "message": "Open the authorization page in your browser and confirm once to continue.",
            "action_text": "Open authorization page",
            "result_hint": "After authorization, return to the source app and continue the current request.",
            "authorize_url": authorize_url,
            "is_reauth": True,
            "requires_user_action": True,
            "pause_execution": True,
            "resume_mode": "rerun_same_command",
            "host_instruction": host_instruction,
        }
    return {
        "title": "Authorize PagePop before first use",
        "message": "Open the authorization page in your browser and confirm once before using this skill.",
        "action_text": "Open authorization page",
        "result_hint": "After authorization, return to the source app and continue the current request.",
        "authorize_url": authorize_url,
        "is_reauth": False,
        "requires_user_action": True,
        "pause_execution": True,
        "resume_mode": "rerun_same_command",
        "host_instruction": host_instruction,
    }


def env_value(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return default


def parse_env_bool(*names: str, default: bool = False) -> bool:
    raw = env_value(*names).strip().lower()
    if not raw:
        return default
    if raw in {"1", "true", "yes", "on"}:
        return True
    if raw in {"0", "false", "no", "off"}:
        return False
    return default


def response_preview(raw: bytes, max_len: int = 500) -> str:
    text = raw.decode("utf-8", errors="replace")
    text = compact_whitespace(text)
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rstrip() + "..."


def should_warn_default_launch_context(config: Config) -> bool:
    return not config.source_app.strip() and config.display_app_name.strip() == DEFAULT_DISPLAY_APP_NAME


def build_launch_context_warning(config: Config) -> dict[str, t.Any]:
    return {
        "title": "Using default authorization context",
        "message": (
            "This run will label the authorization page as OpenClaw. "
            "That is expected for direct OpenClaw usage. "
            "If the skill is invoked from Feishu, Slack, or another host app, "
            "set source_app and display_app_name before calling auth/init."
        ),
        "action_text": "Configure launch context",
        "result_hint": (
            "For example, set PAGEPOP_SKILL_SOURCE_APP=feishu and "
            "PAGEPOP_SKILL_DISPLAY_APP_NAME=飞书 before running auth."
        ),
        "current_source_app": config.source_app,
        "current_display_app_name": config.display_app_name,
    }


def should_warn_missing_region_context(config: Config) -> bool:
    return config.region_context_missing


def build_region_context_warning(config: Config) -> dict[str, t.Any]:
    return {
        "title": "Region context missing",
        "message": (
            "The host should determine whether the current user is in mainland China "
            "before invoking this skill. Pass PAGEPOP_SKILL_REGION=CN for mainland China; "
            "pass another country/region code or GLOBAL for non-mainland users. "
            "Without region context, PagePop uses the global .ai production domain."
        ),
        "action_text": "Pass user region",
        "result_hint": "Set PAGEPOP_SKILL_REGION from the host's user, tenant, locale, or deployment context.",
        "current_region": config.region,
        "current_api_base_url": config.api_base_url,
        "default_api_base_url": DEFAULT_API_BASE_URL,
    }


def is_source_install(config: Config) -> bool:
    return config.package_version == SOURCE_INSTALL_PACKAGE_VERSION


def emit_skill_update_event(config: Config) -> None:
    if is_source_install(config):
        return
    try:
        update_data = get_skill_update(config)
    except Exception:
        return
    update_level = str(update_data.get("update_level", "")).strip().lower()
    if update_level not in {"recommended", "required"}:
        return

    payload = {
        "current_version": str(update_data.get("current_version", "")).strip() or config.package_version,
        "latest_version": str(update_data.get("latest_version", "")).strip(),
        "min_supported_version": str(update_data.get("min_supported_version", "")).strip(),
        "update_level": update_level,
        "download_url": str(update_data.get("download_url", "")).strip(),
        "sha256": str(update_data.get("sha256", "")).strip(),
        "repo": str(update_data.get("repo", "")).strip() or config.update_repo,
        "release_tag": str(update_data.get("release_tag", "")).strip() or config.update_release_tag,
        "published_at": str(update_data.get("published_at", "")).strip(),
        "message": str(update_data.get("message", "")).strip(),
        "release_notes": [
            str(item).strip() for item in update_data.get("release_notes", []) if str(item).strip()
        ],
    }

    emit_event("skill_update_required" if update_level == "required" else "skill_update_available", **payload)
    if update_level == "required":
        raise RuntimeError(
            payload["message"] or "This PagePop skill version is no longer supported. Please update it first."
        )


def ensure_parent_dir(path: pathlib.Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def save_state(path: pathlib.Path, state: SkillState) -> None:
    ensure_parent_dir(path)
    state.updated_at = utc_now().isoformat()
    tmp_file = tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=str(path.parent),
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    )
    tmp_path = pathlib.Path(tmp_file.name)
    try:
        with tmp_file:
            tmp_file.write(json.dumps(state.to_dict(), ensure_ascii=False, indent=2) + "\n")
        try:
            os.chmod(tmp_path, 0o600)
        except OSError:
            pass
        os.replace(tmp_path, path)
    finally:
        try:
            if tmp_path.exists():
                tmp_path.unlink()
        except OSError:
            pass


def load_state(path: pathlib.Path) -> SkillState:
    if not path.exists():
        return SkillState()
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return SkillState()
    return SkillState.from_dict(raw)


def clear_state(path: pathlib.Path) -> None:
    if path.exists():
        path.unlink()


def build_config(args: argparse.Namespace) -> Config:
    manifest = load_skill_manifest()
    state_dir = pathlib.Path(args.state_dir).expanduser().resolve()
    login_token_file = (
        args.login_token_file
        or env_value("PAGEPOP_SKILL_LOGIN_TOKEN_FILE", "PAGEPOP_OPENCLAW_LOGIN_TOKEN_FILE")
    ).strip()
    timezone = (args.timezone or env_value("PAGEPOP_SKILL_TIMEZONE", "PAGEPOP_OPENCLAW_TIMEZONE")).strip()
    region = (
        args.region
        or env_value(
            "PAGEPOP_SKILL_REGION",
            "PAGEPOP_OPENCLAW_REGION",
            "PAGEPOP_USER_REGION",
            "PAGEPOP_COUNTRY_CODE",
        )
    ).strip()
    explicit_api_base_url = args.api_base_url or env_value("PAGEPOP_API_BASE_URL", "PAGEPOP_OPENCLAW_API_BASE_URL")
    resolved_region = resolve_user_region(region, timezone)
    api_base_url = resolve_api_base_url(explicit_api_base_url, region=region, timezone=timezone)
    source_app = (args.source_app or env_value("PAGEPOP_SKILL_SOURCE_APP", "PAGEPOP_OPENCLAW_SOURCE_APP")).strip()
    display_app_name = (
        args.display_app_name or env_value("PAGEPOP_SKILL_DISPLAY_APP_NAME", "PAGEPOP_OPENCLAW_DISPLAY_APP_NAME")
    ).strip()
    return_mode = (
        args.return_mode or env_value("PAGEPOP_SKILL_RETURN_MODE", "PAGEPOP_OPENCLAW_RETURN_MODE", default="manual")
    ).strip() or "manual"
    return_target = (
        args.return_target or env_value("PAGEPOP_SKILL_RETURN_TARGET", "PAGEPOP_OPENCLAW_RETURN_TARGET")
    ).strip()
    artifact_dir = (
        args.artifact_dir
        or env_value("PAGEPOP_SKILL_ARTIFACT_DIR", "PAGEPOP_OPENCLAW_ARTIFACT_DIR")
        or str(pathlib.Path.cwd() / ".pagepop-artifacts")
    )
    update_channel = (
        env_value("PAGEPOP_SKILL_UPDATE_CHANNEL", "PAGEPOP_OPENCLAW_UPDATE_CHANNEL")
        or manifest.channel
        or DEFAULT_UPDATE_CHANNEL
    )
    wait_for_authorization = bool(args.wait_for_authorization) or parse_env_bool(
        "PAGEPOP_SKILL_WAIT_FOR_AUTHORIZATION",
        "PAGEPOP_OPENCLAW_WAIT_FOR_AUTHORIZATION",
    )
    return Config(
        api_base_url=api_base_url,
        skill_id=(args.skill_id or manifest.skill_id).strip() or manifest.skill_id,
        state_path=state_dir / STATE_FILE_NAME,
        region=resolved_region,
        region_context_missing=not explicit_api_base_url.strip() and not resolved_region,
        package_version=manifest.package_version,
        update_channel=update_channel,
        update_repo=manifest.repo,
        update_release_tag=manifest.release_tag,
        login_token_file=pathlib.Path(login_token_file).expanduser().resolve() if login_token_file else None,
        client_version=(
            args.client_version
            or env_value("PAGEPOP_SKILL_CLIENT_VERSION", "PAGEPOP_OPENCLAW_CLIENT_VERSION", default=DEFAULT_CLIENT_VERSION)
        ).strip()
        or DEFAULT_CLIENT_VERSION,
        source_app=source_app,
        display_app_name=display_app_name or DEFAULT_DISPLAY_APP_NAME,
        return_mode=return_mode,
        return_target=return_target,
        wait_for_authorization=wait_for_authorization,
        artifact_dir=pathlib.Path(artifact_dir).expanduser().resolve(),
        download_artifact_images=not bool(args.no_download_images)
        and parse_env_bool("PAGEPOP_SKILL_DOWNLOAD_IMAGES", "PAGEPOP_OPENCLAW_DOWNLOAD_IMAGES", default=True),
        timezone=timezone,
    )


def http_json(
    method: str,
    url: str,
    *,
    headers: t.Optional[dict[str, str]] = None,
    payload: t.Optional[dict[str, t.Any]] = None,
    timeout_seconds: int = 30,
) -> dict[str, t.Any]:
    body: t.Optional[bytes] = None
    request_headers = {"Accept": "application/json"}
    if headers:
        request_headers.update(headers)
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        request_headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=body, headers=request_headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
            content = resp.read()
    except urllib.error.HTTPError as exc:
        content = exc.read()
        content_type = exc.headers.get("Content-Type", "") if exc.headers else ""
        try:
            return unwrap_base_response(content)
        except PagepopAPIError:
            raise
        except Exception as parse_exc:
            raise PagepopHTTPError(
                status=exc.code,
                url=url,
                content_type=content_type,
                response_preview=response_preview(content),
                parse_error=str(parse_exc),
            ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"request failed: {url}: {exc}") from exc

    return unwrap_base_response(content)


def unwrap_base_response(raw: bytes) -> dict[str, t.Any]:
    payload = json.loads(raw.decode("utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("unexpected response shape")
    code = int(payload.get("code", 0))
    if code != SUCCESS_CODE:
        raise PagepopAPIError(
            code=code,
            message=str(payload.get("message", "")).strip(),
            reason=str(payload.get("reason", "")).strip(),
            metadata=payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {},
            data=payload.get("data"),
        )
    data = payload.get("data")
    if isinstance(data, dict):
        return data
    if data is None:
        return {}
    raise RuntimeError("unexpected success payload shape")


def maybe_parse_json(raw: str) -> t.Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def parse_sse_events(lines: t.Iterable[str]) -> t.Iterator[SSEEvent]:
    event_name = "message"
    data_lines: list[str] = []
    for raw_line in lines:
        line = raw_line.rstrip("\r\n")
        if not line:
            if data_lines:
                raw_data = "\n".join(data_lines)
                yield SSEEvent(event=event_name, raw_data=raw_data, data=maybe_parse_json(raw_data))
            event_name = "message"
            data_lines = []
            continue
        if line.startswith(":"):
            continue
        field, _, value = line.partition(":")
        if value.startswith(" "):
            value = value[1:]
        if field == "event":
            event_name = value or "message"
        elif field == "data":
            data_lines.append(value)
    if data_lines:
        raw_data = "\n".join(data_lines)
        yield SSEEvent(event=event_name, raw_data=raw_data, data=maybe_parse_json(raw_data))


def normalize_login_token(raw: str) -> str:
    raw = raw.strip()
    if not raw:
        return ""
    for chunk in raw.split(";"):
        part = chunk.strip()
        if part.startswith("pagepop-token="):
            return part[len("pagepop-token=") :].strip()
        if part.startswith("f-pagepop-token="):
            return part[len("f-pagepop-token=") :].strip()
    return raw


def load_login_token(config: Config) -> str:
    if config.login_token_file is None:
        return ""
    try:
        raw = config.login_token_file.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise RuntimeError(f"login token file not found: {config.login_token_file}") from exc
    token = normalize_login_token(raw)
    if not token:
        raise RuntimeError(f"login token file is empty: {config.login_token_file}")
    return token


def auth_headers(access_key: str, skill_id: str) -> dict[str, str]:
    return {
        "X-Pagepop-Skill-Key": access_key,
        "X-Pagepop-Skill-Id": skill_id,
        "X-Pagepop-Client": DEFAULT_CLIENT_NAME,
        "Accept": "application/json",
    }


def request_auth_headers(config: Config, state: SkillState) -> dict[str, str]:
    login_token = load_login_token(config)
    if login_token:
        return {
            "token": login_token,
            "X-Pagepop-Client": DEFAULT_CLIENT_NAME,
            "Accept": "application/json",
        }
    if not state.access_key:
        raise RuntimeError("access key is missing")
    return auth_headers(state.access_key, config.skill_id)


def init_auth(config: Config) -> dict[str, t.Any]:
    return http_json(
        "POST",
        f"{config.api_base_url}/v1/openclaw/auth/init",
        payload={
            "skill_id": config.skill_id,
            "client_name": config.client_name,
            "client_version": config.client_version,
            "launch_context": {
                "source_app": config.source_app,
                "display_app_name": config.display_app_name,
                "return_mode": config.return_mode,
                "return_target": config.return_target,
            },
        },
    )


def get_skill_update(config: Config) -> dict[str, t.Any]:
    params = urllib.parse.urlencode(
        {
            "skill_id": config.skill_id,
            "package_version": config.package_version,
            "channel": config.update_channel,
        }
    )
    return http_json("GET", f"{config.api_base_url}/v1/openclaw/skill/update?{params}")


def get_auth_status(config: Config, auth_session_id: str) -> dict[str, t.Any]:
    params = urllib.parse.urlencode({"auth_session_id": auth_session_id})
    return http_json("GET", f"{config.api_base_url}/v1/openclaw/auth/status?{params}")



def normalize_authorize_url(config: Config, authorize_url: str) -> str:
    authorize_url = authorize_url.strip()
    if not authorize_url:
        return authorize_url

    parsed_auth = urllib.parse.urlparse(authorize_url)
    if not parsed_auth.scheme or not parsed_auth.netloc:
        return authorize_url

    if is_local_pagepop_host(parsed_auth.netloc):
        web_base_url = resolve_pagepop_web_base_url(config.api_base_url)
        parsed_web = urllib.parse.urlparse(web_base_url)
        if parsed_web.scheme and parsed_web.netloc and not is_local_pagepop_host(parsed_web.netloc):
            parsed_auth = parsed_auth._replace(scheme=parsed_web.scheme, netloc=parsed_web.netloc)

    if parsed_auth.path == "/openclaw/authorize":
        parsed_auth = parsed_auth._replace(path="/openclaw/authorize-v2")
    return urllib.parse.urlunparse(parsed_auth)


def emit_auth_required_event(
    *,
    auth_session_id: str,
    authorize_url: str,
    expires_at: str,
    poll_interval_seconds: int,
    is_reauth: bool,
    status: str = "pending",
    reuse_existing_session: bool = False,
) -> None:
    emit_event(
        "auth_required",
        auth_session_id=auth_session_id,
        expires_at=expires_at,
        poll_interval_seconds=poll_interval_seconds,
        status=status,
        reuse_existing_session=reuse_existing_session,
        **build_authorize_prompt(authorize_url=authorize_url, is_reauth=is_reauth),
    )


def wait_for_authorization(config: Config, state: SkillState, pending_auth: PendingAuth, *, is_reauth: bool) -> SkillState:
    emit_auth_required_event(
        auth_session_id=pending_auth.auth_session_id,
        authorize_url=pending_auth.authorize_url,
        expires_at=pending_auth.expires_at,
        poll_interval_seconds=pending_auth.poll_interval_seconds,
        is_reauth=is_reauth,
        status="pending",
        reuse_existing_session=is_reauth,
    )
    deadline = time.time() + config.poll_timeout_seconds
    while time.time() < deadline:
        status_data = get_auth_status(config, pending_auth.auth_session_id)
        status = str(status_data.get("status", "")).strip()
        emit_event(
            "auth_polling",
            auth_session_id=pending_auth.auth_session_id,
            status=status,
            expires_at=status_data.get("expires_at"),
        )
        if status == "authorized":
            access_key = str(status_data.get("access_key", "")).strip()
            if not access_key:
                raise RuntimeError("authorized status returned without access_key")
            state.access_key = access_key
            state.pending_auth = None
            save_state(config.state_path, state)
            emit_event(
                "auth_authorized",
                auth_session_id=pending_auth.auth_session_id,
                user=status_data.get("user"),
                access_key=mask_secret(access_key),
            )
            return state
        if status in {"expired", "denied"}:
            state.pending_auth = None
            save_state(config.state_path, state)
            raise RuntimeError(f"authorization session ended with status={status}")
        time.sleep(max(pending_auth.poll_interval_seconds, 1))
    raise RuntimeError("authorization timed out")


def submit_chat(
    config: Config,
    state: SkillState,
    *,
    goal: str,
    artifact_type: str,
    links: list[str],
    conversation_id: str = "",
) -> dict[str, t.Any]:
    payload: dict[str, t.Any] = {
        "conversation_id": conversation_id,
        "msg": goal,
        "client_type": config.client_type,
        "links": links,
        "message_id": str(uuid.uuid4()),
        "meta": {
            "source": "openclaw",
            "skill_id": config.skill_id,
            "artifact_type": artifact_type,
        },
        "version": config.version,
    }
    if config.timezone:
        payload["timezone"] = config.timezone
    return http_json(
        "POST",
        f"{config.api_base_url}/v2/chat",
        headers=request_auth_headers(config, state),
        payload=payload,
    )


def ensure_authorized(config: Config, state: SkillState) -> SkillState:
    if load_login_token(config):
        emit_event(
            "auth_bypassed",
            mode="token_header",
            login_token_file=str(config.login_token_file) if config.login_token_file else "",
        )
        return state
    if state.access_key:
        return state

    if state.pending_auth is not None and state.pending_auth.auth_session_id:
        pending_auth_session_id = state.pending_auth.auth_session_id
        status_data = get_auth_status(config, state.pending_auth.auth_session_id)
        status = str(status_data.get("status", "")).strip()
        if status == "authorized":
            access_key = str(status_data.get("access_key", "")).strip()
            if not access_key:
                raise RuntimeError("authorized status returned without access_key")
            state.access_key = access_key
            state.pending_auth = None
            save_state(config.state_path, state)
            emit_event(
                "auth_authorized",
                auth_session_id=str(status_data.get("auth_session_id", "")).strip() or pending_auth_session_id,
                user=status_data.get("user"),
                access_key=mask_secret(access_key),
            )
            return state

        if status == "pending":
            authorize_url = normalize_authorize_url(config, state.pending_auth.authorize_url)
            pending_auth = PendingAuth(
                auth_session_id=state.pending_auth.auth_session_id,
                authorize_url=authorize_url,
                expires_at=str(status_data.get("expires_at", "")).strip() or state.pending_auth.expires_at,
                poll_interval_seconds=state.pending_auth.poll_interval_seconds,
                created_at=state.pending_auth.created_at,
            )
            state.pending_auth = pending_auth
            save_state(config.state_path, state)
            if config.wait_for_authorization:
                return wait_for_authorization(config, state, pending_auth, is_reauth=True)
            emit_auth_required_event(
                auth_session_id=pending_auth.auth_session_id,
                authorize_url=pending_auth.authorize_url,
                expires_at=pending_auth.expires_at,
                poll_interval_seconds=pending_auth.poll_interval_seconds,
                is_reauth=True,
                status=status,
                reuse_existing_session=True,
            )
            raise AuthorizationPending("authorization is waiting for browser confirmation")

        state.pending_auth = None
        save_state(config.state_path, state)

    if should_warn_default_launch_context(config):
        emit_event("integration_warning", **build_launch_context_warning(config))
    if should_warn_missing_region_context(config):
        emit_event("integration_warning", **build_region_context_warning(config))

    init_data = init_auth(config)
    auth_session_id = str(init_data.get("auth_session_id", "")).strip()
    authorize_url = normalize_authorize_url(config, str(init_data.get("authorize_url", "")).strip())
    expires_at = str(init_data.get("expires_at", "")).strip()
    poll_interval = int(init_data.get("poll_interval_seconds", 3) or 3)
    pending_auth = PendingAuth(
        auth_session_id=auth_session_id,
        authorize_url=authorize_url,
        expires_at=expires_at,
        poll_interval_seconds=poll_interval,
    )
    state.pending_auth = pending_auth
    save_state(config.state_path, state)
    if config.wait_for_authorization:
        return wait_for_authorization(config, state, pending_auth, is_reauth=False)
    emit_auth_required_event(
        auth_session_id=auth_session_id,
        authorize_url=authorize_url,
        expires_at=expires_at,
        poll_interval_seconds=poll_interval,
        is_reauth=False,
        status="pending",
        reuse_existing_session=False,
    )
    raise AuthorizationPending("authorization is waiting for browser confirmation")


def safe_path_part(value: str, default: str = "item") -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip(".-")
    return cleaned[:80] or default


def image_extension_for_url(url: str, content_type: str = "") -> str:
    suffix = pathlib.Path(urllib.parse.urlparse(url).path).suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg"}:
        return suffix
    mime_type = content_type.split(";", 1)[0].strip().lower()
    guessed = mimetypes.guess_extension(mime_type)
    if guessed in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg"}:
        return guessed
    return ".img"


def image_mime_type_for_path(path: pathlib.Path, content_type: str = "") -> str:
    mime_type = content_type.split(";", 1)[0].strip().lower()
    if mime_type.startswith("image/"):
        return mime_type
    guessed, _ = mimetypes.guess_type(str(path))
    return guessed or "application/octet-stream"


def image_download_headers() -> dict[str, str]:
    return {
        "User-Agent": IMAGE_DOWNLOAD_USER_AGENT,
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }


def build_image_attachment_label(index: int) -> str:
    if index == 1:
        return "封面"
    return f"配图 {index - 1}"


def download_image_attachment(config: Config, *, conversation_id: str, url: str, index: int) -> dict[str, t.Any]:
    label = build_image_attachment_label(index)
    base_payload: dict[str, t.Any] = {
        "label": label,
        "source_url": url,
        "send_as": "image_message",
    }
    if not config.download_artifact_images:
        return {**base_payload, "download_skipped": True}

    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
    conversation_dir = config.artifact_dir / safe_path_part(conversation_id, "conversation")
    ensure_parent_dir(conversation_dir / "placeholder")
    req = urllib.request.Request(url, headers=image_download_headers(), method="GET")
    try:
        with urllib.request.urlopen(req, timeout=config.image_download_timeout_seconds) as resp:
            content_type = resp.headers.get("Content-Type", "")
            extension = image_extension_for_url(url, content_type)
            local_path = conversation_dir / f"image-{index}-{digest}{extension}"
            raw = resp.read(config.max_image_download_bytes + 1)
            if len(raw) > config.max_image_download_bytes:
                raise RuntimeError("image exceeds max download size")
            local_path.write_bytes(raw)
        return {
            **base_payload,
            "local_path": str(local_path),
            "filename": local_path.name,
            "mime_type": image_mime_type_for_path(local_path, content_type),
            "size_bytes": local_path.stat().st_size,
        }
    except Exception as exc:
        return {
            **base_payload,
            "download_error": str(exc),
        }


def download_image_attachments(config: Config, *, conversation_id: str, image_urls: list[str]) -> list[dict[str, t.Any]]:
    attachments: list[dict[str, t.Any]] = []
    for index, url in enumerate(dedupe_strings([url for url in image_urls if url.strip()], limit=10), start=1):
        attachments.append(download_image_attachment(config, conversation_id=conversation_id, url=url, index=index))
    return attachments


def should_retry_stream(exc: Exception) -> bool:
    return isinstance(exc, (urllib.error.URLError, TimeoutError, OSError, RuntimeError))


def _emit_artifact_delivery_once(
    *,
    config: Config,
    summary: dict[str, t.Any],
    summary_key: str,
    latest_text_message: str,
    suggestions: list[str],
    emitted_signatures: dict[str, str],
) -> None:
    image_attachments = download_image_attachments(
        config,
        conversation_id=str(summary.get("conversation_id", "")).strip(),
        image_urls=[str(url) for url in summary.get("urls", []) if is_image_url(str(url))],
    )
    delivery = build_artifact_delivery(
        summary,
        api_base_url=config.api_base_url,
        latest_text_message=latest_text_message,
        suggestions=suggestions,
        source_app=config.source_app,
        image_attachments=image_attachments,
    )
    delivery_signature = json.dumps(delivery, ensure_ascii=False, sort_keys=True)
    if emitted_signatures.get(summary_key) != delivery_signature:
        emitted_signatures[summary_key] = delivery_signature
        emit_record(delivery)


def stream_sse_events(config: Config, state: SkillState, *, conversation_id: str, offset: int) -> StreamResult:
    reconnects = 0
    last_offset = int(offset)
    last_heartbeat_progress_at = 0.0
    last_progress_signature = ""
    latest_text_message = ""
    suggestions: list[str] = []
    artifact_summaries: dict[str, dict[str, t.Any]] = {}
    emitted_artifact_ready: set[str] = set()
    emitted_artifact_delivery_signatures: dict[str, str] = {}
    while True:
        params = urllib.parse.urlencode({"conversation_id": conversation_id, "offset": str(last_offset)})
        url = f"{config.api_base_url}/v2/sse/events?{params}"
        req = urllib.request.Request(
            url,
            headers={
                **request_auth_headers(config, state),
                "Accept": "text/event-stream",
            },
            method="GET",
        )
        try:
            with urllib.request.urlopen(req, timeout=config.stream_timeout_seconds) as resp:
                content_type = resp.headers.get("Content-Type", "")
                if "text/event-stream" not in content_type.lower():
                    raw = resp.read()
                    try:
                        unwrap_base_response(raw)
                    except PagepopAPIError as api_exc:
                        raise api_exc
                    raise RuntimeError(f"unexpected sse response content-type: {content_type}")
                reconnects = 0
                for event in parse_sse_events(line.decode("utf-8", errors="replace") for line in resp):
                    payload = event.data
                    now_monotonic = time.monotonic()
                    event_offset: t.Optional[int] = None
                    if isinstance(payload, dict):
                        try:
                            event_offset = normalize_sse_offset(payload.get("offset", last_offset))
                            last_offset = event_offset
                        except (TypeError, ValueError):
                            pass
                    if event_offset is not None:
                        update_conversation_stream_state(
                            state,
                            conversation_id=conversation_id,
                            cursor_offset=event_offset,
                        )
                        save_state(config.state_path, state)
                    emit_event(
                        "sse_event",
                        conversation_id=conversation_id,
                        event=event.event,
                        raw_data=event.raw_data,
                        data=payload,
                    )
                    if isinstance(payload, dict):
                        next_text_message = extract_message_text(payload)
                        if next_text_message:
                            latest_text_message = next_text_message

                        next_suggestions = extract_suggestion_actions(payload)
                        if next_suggestions:
                            suggestions = dedupe_strings(suggestions + next_suggestions, limit=10)

                        if event.event == "control" and str(payload.get("cmd", "")).strip() == "heartbeat":
                            if now_monotonic - last_heartbeat_progress_at >= HEARTBEAT_PROGRESS_INTERVAL_SECONDS:
                                last_heartbeat_progress_at = now_monotonic
                                save_state(config.state_path, state)
                                emit_event(
                                    "progress_update",
                                    conversation_id=conversation_id,
                                    stage="working",
                                    status="heartbeat",
                                    event=event.event,
                                    raw_type=str(payload.get("type", "")).strip(),
                                    name="",
                                    summary="PagePop is still generating. Waiting for the next update.",
                                )
                        else:
                            progress_record = summarize_progress_event(event.event, payload)
                            if progress_record is not None:
                                progress_signature = json.dumps(progress_record, ensure_ascii=False, sort_keys=True)
                                if progress_signature != last_progress_signature:
                                    last_progress_signature = progress_signature
                                    emit_record(progress_record)

                        artifact_summary = build_artifact_summary(payload)
                        if artifact_summary is not None:
                            summary_key = artifact_summary_key(artifact_summary)
                            merged_summary = merge_artifact_summary(
                                artifact_summaries.get(summary_key),
                                artifact_summary,
                            )
                            artifact_summaries[summary_key] = merged_summary
                            emit_event(
                                "artifact_update",
                                conversation_id=conversation_id,
                                artifact=merged_summary,
                            )
                            if merged_summary.get("ready") and summary_key not in emitted_artifact_ready:
                                emitted_artifact_ready.add(summary_key)
                                emit_event(
                                    "artifact_ready",
                                    conversation_id=conversation_id,
                                    artifact=merged_summary,
                                )
                            if merged_summary.get("ready"):
                                _emit_artifact_delivery_once(
                                    config=config,
                                    summary=merged_summary,
                                    summary_key=summary_key,
                                    latest_text_message=latest_text_message,
                                    suggestions=suggestions,
                                    emitted_signatures=emitted_artifact_delivery_signatures,
                                )

                        if next_suggestions:
                            for ready_key in list(emitted_artifact_ready):
                                ready_summary = artifact_summaries.get(ready_key)
                                if not ready_summary:
                                    continue
                                _emit_artifact_delivery_once(
                                    config=config,
                                    summary=ready_summary,
                                    summary_key=ready_key,
                                    latest_text_message=latest_text_message,
                                    suggestions=suggestions,
                                    emitted_signatures=emitted_artifact_delivery_signatures,
                                )
                    if event.event == "control" and isinstance(payload, dict):
                        cmd = str(payload.get("cmd", "")).strip()
                        if cmd in TERMINAL_CONTROL_COMMANDS:
                            update_conversation_stream_state(
                                state,
                                conversation_id=conversation_id,
                                cursor_offset=last_offset,
                                terminal_command=cmd,
                            )
                            save_state(config.state_path, state)
                            return StreamResult(
                                conversation_id=conversation_id,
                                terminal_command=cmd,
                                last_offset=last_offset,
                            )
                        if cmd == "retry":
                            break
                else:
                    update_conversation_stream_state(
                        state,
                        conversation_id=conversation_id,
                        cursor_offset=last_offset,
                        terminal_command="done",
                    )
                    save_state(config.state_path, state)
                    return StreamResult(
                        conversation_id=conversation_id,
                        terminal_command="done",
                        last_offset=last_offset,
                    )
        except urllib.error.HTTPError as exc:
            body = exc.read()
            try:
                unwrap_base_response(body)
            except PagepopAPIError as api_exc:
                raise api_exc from exc
            raise RuntimeError(f"sse http error: {exc.code}") from exc
        except Exception as exc:
            reconnects += 1
            if reconnects > config.max_stream_reconnects or not should_retry_stream(exc):
                raise
            emit_event(
                "stream_retrying",
                conversation_id=conversation_id,
                offset=last_offset,
                reconnects=reconnects,
                message=str(exc),
            )
            time.sleep(min(reconnects, 5))


def _reset_access_key_and_emit(config: Config, state: SkillState, exc: PagepopAPIError) -> None:
    state.access_key = ""
    save_state(config.state_path, state)
    emit_event(
        "access_key_reset",
        reason=exc.openclaw_reason or exc.reason,
        message="Open the authorization page again and confirm once to continue.",
        backend_message=exc.message,
        title="PagePop authorization expired",
        action_text="Re-authorize PagePop",
        result_hint="After authorization, return to the source app and continue the current request.",
        is_reauth=True,
    )


def run_stream_command(config: Config, args: argparse.Namespace) -> int:
    emit_skill_update_event(config)
    state = load_state(config.state_path)
    explicit_conversation_id = (args.conversation_id or "").strip()
    resume_conversation_id = (getattr(args, "resume_conversation_id", "") or "").strip()
    if explicit_conversation_id and resume_conversation_id and explicit_conversation_id != resume_conversation_id:
        raise RuntimeError("cannot use --conversation-id and --resume-conversation-id with different values")
    explicit_conversation_id = resume_conversation_id or explicit_conversation_id
    if getattr(args, "new_conversation", False) and explicit_conversation_id:
        raise RuntimeError("cannot use --new-conversation with --conversation-id or --resume-conversation-id")
    pending_run = PendingRun(
        goal=(args.goal or "").strip(),
        artifact_type=(args.artifact_type or "auto").strip() or "auto",
        links=[item.strip() for item in args.link if item.strip()],
        conversation_id=explicit_conversation_id,
    )

    if not pending_run.goal:
        if state.pending_run is None or not state.pending_run.goal:
            raise RuntimeError("goal is required when there is no pending run")
        pending_run = state.pending_run
        emit_event(
            "chat_context",
            **build_chat_context_payload(
                mode="continue" if pending_run.conversation_id else "new",
                state=state,
                conversation_id=pending_run.conversation_id,
            ),
        )
        emit_event("pending_run_restored", pending_run=dataclasses.asdict(pending_run))
    else:
        if getattr(args, "new_conversation", False):
            previous_conversation_id = state.active_conversation_id
            state.active_conversation_id = ""
            state.active_conversation_updated_at = ""
            if previous_conversation_id:
                emit_event("chat_context", **build_chat_context_payload(mode="new", state=state))
        elif not pending_run.conversation_id and state.active_conversation_id:
            pending_run.conversation_id = state.active_conversation_id
            emit_event(
                "chat_context",
                **build_chat_context_payload(
                    mode="continue",
                    state=state,
                    conversation_id=pending_run.conversation_id,
                ),
            )
        elif pending_run.conversation_id:
            emit_event(
                "chat_context",
                **build_chat_context_payload(
                    mode="continue",
                    state=state,
                    conversation_id=pending_run.conversation_id,
                ),
            )
        else:
            emit_event("chat_context", **build_chat_context_payload(mode="new", state=state))
        state.pending_run = pending_run
        save_state(config.state_path, state)
        emit_event("pending_run_saved", pending_run=dataclasses.asdict(pending_run))

    for auth_attempt in range(2):
        if not state.access_key:
            state = ensure_authorized(config, state)

        try:
            chat_data = submit_chat(
                config,
                state,
                goal=pending_run.goal,
                artifact_type=pending_run.artifact_type,
                links=pending_run.links,
                conversation_id=pending_run.conversation_id,
            )
            conversation_id = str(chat_data.get("conversation_id", "")).strip()
            if not conversation_id:
                raise RuntimeError("chat response missing conversation_id")
            sse_max_offset = normalize_sse_offset(chat_data.get("sse_max_offset", 0))
            emit_event(
                "chat_submitted",
                conversation_id=conversation_id,
                sse_max_offset=sse_max_offset,
            )
            state.active_conversation_id = conversation_id
            state.active_conversation_updated_at = utc_now().isoformat()
            update_conversation_stream_state(
                state,
                conversation_id=conversation_id,
                cursor_offset=sse_max_offset,
            )
            state.saved_conversations = upsert_saved_conversation(
                state.saved_conversations,
                conversation_id=conversation_id,
                goal=pending_run.goal,
                artifact_type=pending_run.artifact_type,
            )
            save_state(config.state_path, state)
            result = stream_sse_events(
                config,
                state,
                conversation_id=conversation_id,
                offset=sse_max_offset,
            )
            update_conversation_stream_state(
                state,
                conversation_id=result.conversation_id,
                cursor_offset=result.last_offset,
                terminal_command=result.terminal_command,
            )
            state.pending_run = None
            save_state(config.state_path, state)
            emit_event(
                "stream_finished",
                conversation_id=result.conversation_id,
                status=result.terminal_command,
                offset=result.last_offset,
            )
            return 0
        except PagepopAPIError as exc:
            if auth_attempt == 0 and exc.should_reset_access_key():
                _reset_access_key_and_emit(config, state, exc)
                continue
            raise
    raise RuntimeError("failed to finish stream after reauthorization")


def resolve_resume_stream_conversation_id(state: SkillState, args: argparse.Namespace) -> str:
    explicit_conversation_id = (getattr(args, "conversation_id", "") or "").strip()
    resume_conversation_id = (getattr(args, "resume_conversation_id", "") or "").strip()
    if explicit_conversation_id and resume_conversation_id and explicit_conversation_id != resume_conversation_id:
        raise RuntimeError("cannot use --conversation-id and --resume-conversation-id with different values")
    conversation_id = resume_conversation_id or explicit_conversation_id or state.active_conversation_id
    if not conversation_id:
        raise RuntimeError("conversation_id is required when there is no active conversation")
    return conversation_id


def resolve_resume_stream_offset(state: SkillState, conversation_id: str, args: argparse.Namespace) -> tuple[int, str]:
    explicit_offset = getattr(args, "offset", None)
    if explicit_offset is not None:
        offset = normalize_sse_offset(explicit_offset)
        return offset, "explicit"
    stream_state = state.conversation_streams.get(conversation_id)
    if stream_state is not None:
        return stream_state.cursor_offset, "state"
    return 0, "default"


def run_resume_stream_command(config: Config, args: argparse.Namespace) -> int:
    emit_skill_update_event(config)
    state = load_state(config.state_path)
    conversation_id = resolve_resume_stream_conversation_id(state, args)
    raw_offset = getattr(args, "offset", None)
    if raw_offset is not None and int(raw_offset) < 0:
        raise RuntimeError("offset must be greater than or equal to 0")
    offset, offset_source = resolve_resume_stream_offset(state, conversation_id, args)
    update_conversation_stream_state(
        state,
        conversation_id=conversation_id,
        cursor_offset=offset,
    )
    save_state(config.state_path, state)
    emit_event(
        "chat_context",
        **build_chat_context_payload(
            mode="continue",
            state=state,
            conversation_id=conversation_id,
        ),
    )

    for auth_attempt in range(2):
        if not state.access_key:
            state = ensure_authorized(config, state)

        try:
            emit_event(
                "stream_resumed",
                conversation_id=conversation_id,
                offset=offset,
                offset_source=offset_source,
                message="Resuming existing PagePop SSE stream without submitting a new chat request.",
            )
            result = stream_sse_events(
                config,
                state,
                conversation_id=conversation_id,
                offset=offset,
            )
            update_conversation_stream_state(
                state,
                conversation_id=result.conversation_id,
                cursor_offset=result.last_offset,
                terminal_command=result.terminal_command,
            )
            state.active_conversation_id = result.conversation_id
            state.active_conversation_updated_at = utc_now().isoformat()
            save_state(config.state_path, state)
            emit_event(
                "stream_finished",
                conversation_id=result.conversation_id,
                status=result.terminal_command,
                offset=result.last_offset,
            )
            return 0
        except PagepopAPIError as exc:
            if auth_attempt == 0 and exc.should_reset_access_key():
                _reset_access_key_and_emit(config, state, exc)
                continue
            raise
    raise RuntimeError("failed to resume stream after reauthorization")


def run_auth_command(config: Config) -> int:
    emit_skill_update_event(config)
    state = load_state(config.state_path)
    state = ensure_authorized(config, state)
    emit_event("state", state=state.masked_dict())
    return 0


def run_status_command(config: Config) -> int:
    emit_skill_update_event(config)
    state = load_state(config.state_path)
    emit_record(
        {
            "kind": "state",
            "state": state.masked_dict(),
            "state_path": str(config.state_path),
            "package_version": config.package_version,
            "update_channel": config.update_channel,
            "active_conversation_id": state.active_conversation_id,
            "active_conversation_updated_at": state.active_conversation_updated_at,
            "active_conversation_stream": conversation_stream_payload(
                state.conversation_streams.get(state.active_conversation_id)
            ),
        }
    )
    return 0


def run_conversations_command(config: Config) -> int:
    state = load_state(config.state_path)
    emit_record(
        {
            "kind": "conversation_history",
            "active_conversation_id": state.active_conversation_id,
            "items": build_conversation_history_items(state.saved_conversations, state.conversation_streams),
        }
    )
    return 0


def run_clear_state_command(config: Config) -> int:
    clear_state(config.state_path)
    emit_event("state_cleared", state_path=str(config.state_path))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PagePop Skill client")
    parser.add_argument(
        "--api-base-url",
        default="",
        help="Explicit PagePop API base URL; overrides region-based production domain selection",
    )
    parser.add_argument(
        "--skill-id",
        default=env_value("PAGEPOP_SKILL_ID", "PAGEPOP_OPENCLAW_SKILL_ID", default=DEFAULT_SKILL_ID),
        help="PagePop skill identifier",
    )
    parser.add_argument(
        "--state-dir",
        default=env_value(
            "PAGEPOP_SKILL_STATE_DIR",
            "PAGEPOP_OPENCLAW_STATE_DIR",
            default=str(pathlib.Path.home() / ".pagepop-skill"),
        ),
        help="Directory used to persist access_key and pending_run",
    )
    parser.add_argument(
        "--timezone",
        default="",
        help="Optional IANA timezone, for example Asia/Shanghai",
    )
    parser.add_argument(
        "--region",
        default="",
        help="Optional user region or country code; mainland China uses pagepop.cn, other regions use pagepop.ai",
    )
    parser.add_argument(
        "--client-version",
        default=env_value("PAGEPOP_SKILL_CLIENT_VERSION", "PAGEPOP_OPENCLAW_CLIENT_VERSION", default=DEFAULT_CLIENT_VERSION),
        help="Client version sent to auth/init",
    )
    parser.add_argument(
        "--source-app",
        default=env_value("PAGEPOP_SKILL_SOURCE_APP", "PAGEPOP_OPENCLAW_SOURCE_APP"),
        help="Source app identifier passed to auth/init; channel integrations should set this, for example feishu or slack",
    )
    parser.add_argument(
        "--display-app-name",
        default=env_value("PAGEPOP_SKILL_DISPLAY_APP_NAME", "PAGEPOP_OPENCLAW_DISPLAY_APP_NAME"),
        help="Source app display name shown on the PagePop authorization page; channel integrations should set this, for example 飞书 or Slack",
    )
    parser.add_argument(
        "--return-mode",
        default=env_value("PAGEPOP_SKILL_RETURN_MODE", "PAGEPOP_OPENCLAW_RETURN_MODE", default="manual"),
        help="Return behavior hint passed to auth/init, for example manual, close, or history_back",
    )
    parser.add_argument(
        "--return-target",
        default=env_value("PAGEPOP_SKILL_RETURN_TARGET", "PAGEPOP_OPENCLAW_RETURN_TARGET"),
        help="Return target passed to auth/init for future deep-link or web redirect handling",
    )
    parser.add_argument(
        "--login-token-file",
        default=env_value("PAGEPOP_SKILL_LOGIN_TOKEN_FILE", "PAGEPOP_OPENCLAW_LOGIN_TOKEN_FILE"),
        help="Optional local file containing a PagePop login token; when set, auth/init is bypassed and requests use the token header directly",
    )
    parser.add_argument(
        "--artifact-dir",
        default=env_value("PAGEPOP_SKILL_ARTIFACT_DIR", "PAGEPOP_OPENCLAW_ARTIFACT_DIR"),
        help="Directory for downloaded PagePop artifact files, defaults to .pagepop-artifacts in the current workspace",
    )
    parser.add_argument(
        "--no-download-images",
        action="store_true",
        help="Do not download generated image URLs into local image attachments",
    )
    parser.add_argument(
        "--wait-for-authorization",
        action="store_true",
        default=parse_env_bool("PAGEPOP_SKILL_WAIT_FOR_AUTHORIZATION", "PAGEPOP_OPENCLAW_WAIT_FOR_AUTHORIZATION"),
        help="Block and poll auth/status until the browser authorization finishes; primarily for local debugging",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("auth", help="Run browser authorization and persist access_key")
    subparsers.add_parser("status", help="Print masked local state")
    subparsers.add_parser("conversations", help="List saved local conversations for switch-chat flows")
    subparsers.add_parser("clear-state", help="Delete local state file")

    stream_parser = subparsers.add_parser("stream", help="Submit /v2/chat and relay raw SSE events")
    stream_parser.add_argument("--goal", default="", help="User goal sent to /v2/chat")
    stream_parser.add_argument("--artifact-type", default="auto", help="Artifact type hint stored in meta")
    stream_parser.add_argument("--conversation-id", default="", help="Optional existing conversation_id")
    stream_parser.add_argument(
        "--resume-conversation-id",
        default="",
        help="Explicitly continue a saved conversation by id; useful for switch-chat flows",
    )
    stream_parser.add_argument(
        "--new-conversation",
        "--new-chat",
        action="store_true",
        help="Start a new conversation instead of reusing the active local conversation context",
    )
    stream_parser.add_argument(
        "--link",
        action="append",
        default=[],
        help="Optional network reference URL; repeat the flag to pass multiple links",
    )

    resume_stream_parser = subparsers.add_parser(
        "resume-stream",
        help="Relay SSE events for an existing conversation without submitting /v2/chat",
    )
    resume_stream_parser.add_argument("--conversation-id", default="", help="Existing conversation_id to stream")
    resume_stream_parser.add_argument(
        "--resume-conversation-id",
        default="",
        help="Explicitly stream a saved conversation by id; useful for switch-chat flows",
    )
    resume_stream_parser.add_argument(
        "--offset",
        type=int,
        default=None,
        help="SSE offset to resume from; defaults to the saved cursor for this conversation",
    )
    return parser


def main(argv: t.Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = build_config(args)
    try:
        if args.command == "auth":
            return run_auth_command(config)
        if args.command == "status":
            return run_status_command(config)
        if args.command == "conversations":
            return run_conversations_command(config)
        if args.command == "clear-state":
            return run_clear_state_command(config)
        if args.command == "stream":
            return run_stream_command(config, args)
        if args.command == "resume-stream":
            return run_resume_stream_command(config, args)
        raise RuntimeError(f"unsupported command: {args.command}")
    except PagepopAPIError as exc:
        emit_record(exc.to_record())
        return 1
    except PagepopHTTPError as exc:
        emit_record(exc.to_record())
        return 1
    except AuthorizationPending:
        return 0
    except Exception as exc:
        emit_event("error", message=str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
