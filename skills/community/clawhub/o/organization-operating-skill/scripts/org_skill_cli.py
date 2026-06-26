#!/usr/bin/env python3
"""Organization operating skill CLI.

本地保存最小会话信息，并封装组织平台的核心认证与组织操作接口。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent.parent
LEGACY_RUNTIME_DIR = ROOT_DIR / ".runtime"
LEGACY_SESSION_FILE = LEGACY_RUNTIME_DIR / "session.json"
DEFAULT_STATE_DIR = Path.home() / ".organization-operating-skill"
LEGACY_CODEX_STATE_DIR = Path.home() / ".codex-state" / "organization-operating-skill"
STATE_DIR_OVERRIDE = os.environ.get("ORG_SKILL_STATE_DIR", "").strip()
STATE_DIR = Path(STATE_DIR_OVERRIDE or str(DEFAULT_STATE_DIR)).expanduser()
SESSIONS_DIR = STATE_DIR / "sessions"
LEGACY_BASE_URL_ALIASES = {
    "https://api.zingup.club": "https://api.zingup.club/biz",
}
KNOWN_ENV_BASE_URLS = {
    "prod": "https://api.zingup.club/biz",
    "test": "https://test-api.groupoo.net/biz",
    "local": "http://localhost:8080/biz",
}
DEFAULT_ENV_NAME = os.environ.get("ORG_SKILL_ENV", "prod").strip().lower() or "prod"
DEFAULT_BASE_URL = os.environ.get(
    "ORG_SKILL_BASE_URL",
    KNOWN_ENV_BASE_URLS.get(DEFAULT_ENV_NAME, KNOWN_ENV_BASE_URLS["prod"]),
)
DEFAULT_LANGUAGE = os.environ.get("ORG_SKILL_X_LANGUAGE", "ch")
DEFAULT_PLATFORM = os.environ.get("ORG_SKILL_X_PLATFORM", "3")
DEFAULT_PACKAGE = os.environ.get("ORG_SKILL_X_PACKAGE", "com.groupoo.zingup")
DEFAULT_WEB_PLATFORM = os.environ.get("ORG_SKILL_WEB_X_PLATFORM", "3")
DEFAULT_WEB_VERSION = os.environ.get("ORG_SKILL_X_VERSION", "1.0.0")
DEFAULT_WEB_BUILDNUMBER = os.environ.get("ORG_SKILL_X_BUILDNUMBER", "20250101")
DEFAULT_WEB_MODEL = os.environ.get("ORG_SKILL_X_MODEL", "146.0.0.0")
DEFAULT_WEB_SYSTEM_VERSION = os.environ.get("ORG_SKILL_X_SYSTEM_VERSION", DEFAULT_WEB_MODEL)
DEFAULT_WEB_BRAND = os.environ.get("ORG_SKILL_X_BRAND", "Chrome")
DEFAULT_TIMEOUT = int(os.environ.get("ORG_SKILL_TIMEOUT", "30"))
HELP_EXAMPLES = """常用示例:
  python scripts/org_skill_cli.py session show
  python scripts/org_skill_cli.py --env test guest-generate
  python scripts/org_skill_cli.py --env test agent-login --open-id agent-demo --union-id agent-demo
  python scripts/org_skill_cli.py --env test refresh
  python scripts/org_skill_cli.py --env test org-create --name "Agent Org Demo"
  python scripts/org_skill_cli.py --env test post-create --org-id 1141 --text "求助帖：招募一位活动摄影志愿者"
  python scripts/org_skill_cli.py --env test activity-publish --draft-id 5912
"""


def detect_default_timezone() -> str:
    configured = os.environ.get("ORG_SKILL_X_TIMEZONE")
    if configured and configured.strip():
        return configured.strip()
    local_offset = datetime.now().astimezone().utcoffset()
    if local_offset is None:
        return "0"
    return str(int(local_offset.total_seconds() // 60))


DEFAULT_TIMEZONE = detect_default_timezone()
DEFAULT_TIMEZONE_HELP = f"按当前时区自动计算，当前 {DEFAULT_TIMEZONE}"


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def ensure_state_dir() -> None:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


def normalize_base_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    return LEGACY_BASE_URL_ALIASES.get(normalized, normalized)


def normalize_session_payload(session: dict[str, Any]) -> dict[str, Any]:
    payload = dict(session)
    base_url = payload.get("baseUrl")
    if isinstance(base_url, str) and base_url.strip():
        payload["baseUrl"] = normalize_base_url(base_url)
    platform = payload.get("platform")
    if platform is None or str(platform).strip() == "1":
        payload["platform"] = DEFAULT_PLATFORM
    payload.pop("timezone", None)
    return payload


def sanitize_env_name(raw: str) -> str:
    value = raw.strip().lower()
    if not value:
        return DEFAULT_ENV_NAME
    if value in KNOWN_ENV_BASE_URLS:
        return value
    cleaned = re.sub(r"[^a-z0-9-]+", "-", value).strip("-")
    return cleaned or DEFAULT_ENV_NAME


def infer_env_name_from_base_url(base_url: str) -> str:
    normalized = normalize_base_url(base_url)
    for env_name, known_url in KNOWN_ENV_BASE_URLS.items():
        if normalized == normalize_base_url(known_url):
            return env_name
    digest = hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:10]
    return f"custom-{digest}"


def default_base_url_for_env(env_name: str) -> str:
    return KNOWN_ENV_BASE_URLS.get(env_name, DEFAULT_BASE_URL)


def resolve_session_env(args: argparse.Namespace) -> str:
    explicit_env = getattr(args, "env_name", None)
    if explicit_env:
        return sanitize_env_name(explicit_env)
    explicit_base_url = getattr(args, "base_url", None)
    if explicit_base_url:
        return infer_env_name_from_base_url(explicit_base_url)
    return sanitize_env_name(os.environ.get("ORG_SKILL_ENV", DEFAULT_ENV_NAME))


def default_session_file(env_name: str) -> Path:
    return SESSIONS_DIR / f"{env_name}.json"


def legacy_codex_session_file(env_name: str) -> Path:
    return LEGACY_CODEX_STATE_DIR / "sessions" / f"{env_name}.json"


def legacy_session_matches_env(env_name: str) -> bool:
    if not LEGACY_SESSION_FILE.exists():
        return False
    try:
        session = json.loads(LEGACY_SESSION_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    legacy_base_url = session.get("baseUrl") or DEFAULT_BASE_URL
    legacy_env_name = infer_env_name_from_base_url(str(legacy_base_url))
    return legacy_env_name == env_name


def load_session_source(path: Path) -> tuple[Path | None, dict[str, Any]]:
    if path.exists():
        return path, normalize_session_payload(json.loads(path.read_text(encoding="utf-8")))
    if not STATE_DIR_OVERRIDE and path.parent == SESSIONS_DIR:
        legacy_codex_path = legacy_codex_session_file(path.stem)
        if legacy_codex_path.exists():
            return legacy_codex_path, normalize_session_payload(json.loads(legacy_codex_path.read_text(encoding="utf-8")))
    if path.parent == SESSIONS_DIR and legacy_session_matches_env(path.stem):
        return LEGACY_SESSION_FILE, normalize_session_payload(json.loads(LEGACY_SESSION_FILE.read_text(encoding="utf-8")))
    return None, {}


def session_path(args: argparse.Namespace) -> Path:
    if getattr(args, "session_file", None):
        return Path(args.session_file).expanduser().resolve()
    custom = os.environ.get("ORG_SKILL_SESSION_FILE")
    if custom:
        return Path(custom).expanduser().resolve()
    return default_session_file(resolve_session_env(args))


def load_session(path: Path) -> dict[str, Any]:
    _, session = load_session_source(path)
    return session


def save_session(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(data)
    payload["updatedAt"] = now_iso()
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not STATE_DIR_OVERRIDE and path.parent == SESSIONS_DIR:
        legacy_codex_session_file(path.stem).unlink(missing_ok=True)
    if path.parent == SESSIONS_DIR and legacy_session_matches_env(path.stem):
        LEGACY_SESSION_FILE.unlink(missing_ok=True)


def pretty_print(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def mask_secret(value: str) -> str:
    if len(value) <= 12:
        return "*" * len(value)
    return f"{value[:6]}...{value[-6:]}"


def redact_session_for_display(session: dict[str, Any]) -> dict[str, Any]:
    payload = dict(session)
    for key in ("token", "refreshToken"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            payload[key] = mask_secret(value)
    return payload


def coerce_value(raw: str) -> Any:
    lowered = raw.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "null":
        return None
    try:
        if raw.startswith("0") and raw != "0" and not raw.startswith("0."):
            return raw
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        return raw


def parse_key_value_pairs(items: list[str] | None) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for item in items or []:
        if "=" not in item:
            raise ValueError(f"参数必须是 KEY=VALUE 形式: {item}")
        key, value = item.split("=", 1)
        result[key] = coerce_value(value)
    return result


def parse_csv_values(raw: str | None) -> list[Any]:
    if not raw:
        return []
    return [coerce_value(item.strip()) for item in raw.split(",") if item.strip()]


def load_json_payload(json_body: str | None = None, json_file: str | None = None) -> Any:
    if json_body:
        return json.loads(json_body)
    if json_file:
        return json.loads(Path(json_file).read_text(encoding="utf-8"))
    return None


def apply_header_args_to_session(session: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if hasattr(args, "language") and args.language is not None:
        session["language"] = str(args.language)
    if hasattr(args, "platform") and args.platform is not None:
        session["platform"] = str(args.platform)
    if hasattr(args, "package_name") and args.package_name is not None:
        session["packageName"] = str(args.package_name)
    if hasattr(args, "timezone") and args.timezone is not None:
        session["timezone"] = str(args.timezone)
    return session


def rich_text_from_text(text: str) -> list[dict[str, str]]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"
    return [{"insert": normalized}]


def ensure_only_free_tickets(body: dict[str, Any]) -> None:
    tickets = body.get("tickets")
    if tickets is None:
        return
    if not isinstance(tickets, list) or not tickets:
        raise RuntimeError("活动请求体里的 tickets 不能为空。")
    if any(isinstance(ticket, dict) and ticket.get("paid") == 1 for ticket in tickets):
        raise RuntimeError("当前 skill 只支持免费票活动，请确保 tickets[].paid=0。")
    if not any(isinstance(ticket, dict) and ticket.get("hiddenTicket", 0) == 0 for ticket in tickets):
        raise RuntimeError("当前活动至少需要一张非隐藏票，请确保至少一个 tickets[].hiddenTicket=0。")


def build_base_headers(session: dict[str, Any], device_id: str | None = None) -> dict[str, str]:
    resolved_device_id = device_id or session.get("deviceId") or session.get("xDeviceId")
    resolved_timezone = session.get("timezone", DEFAULT_TIMEZONE)
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "x-platform": str(session.get("platform", DEFAULT_PLATFORM)),
        "x-language": str(session.get("language", DEFAULT_LANGUAGE)),
        "x-package": str(session.get("packageName", DEFAULT_PACKAGE)),
    }
    if resolved_timezone:
        headers["x-timezone"] = str(resolved_timezone)
    if resolved_device_id:
        headers["x-device-id"] = resolved_device_id
    return headers


def build_web_headers(
    session: dict[str, Any],
    *,
    device_id: str,
    version: str = DEFAULT_WEB_VERSION,
    buildnumber: str = DEFAULT_WEB_BUILDNUMBER,
    brand: str = DEFAULT_WEB_BRAND,
    model: str = DEFAULT_WEB_MODEL,
    system_version: str = DEFAULT_WEB_SYSTEM_VERSION,
) -> dict[str, str]:
    headers = build_base_headers(session, device_id=device_id)
    headers["x-device_id"] = device_id
    headers["x-version"] = str(version)
    headers["x-buildnumber"] = str(buildnumber)
    headers["x-brand"] = str(brand)
    headers["x-model"] = str(model)
    headers["x-system-version"] = str(system_version)
    headers["x-system_version"] = str(system_version)
    return headers


def apply_auth_header(headers: dict[str, str], session: dict[str, Any], auth_mode: str) -> None:
    if auth_mode == "none":
        return
    if auth_mode == "access":
        token = session.get("token")
        if not token:
            raise RuntimeError("当前 session 里没有 access token，请先 guest-generate 或 agent-login。")
        headers["authorization"] = f"Bearer {token}"
        return
    if auth_mode == "refresh":
        refresh_token = session.get("refreshToken")
        if not refresh_token:
            raise RuntimeError("当前 session 里没有 refreshToken，请先登录。")
        headers["RefreshToken"] = f"Bearer {refresh_token}"
        return
    raise ValueError(f"不支持的 auth_mode: {auth_mode}")


def apply_optional_access_token(headers: dict[str, str], session: dict[str, Any]) -> None:
    token = session.get("token")
    if token:
        headers["authorization"] = f"Bearer {token}"


def request_json(
    *,
    method: str,
    base_url: str,
    path: str,
    headers: dict[str, str],
    query: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> Any:
    target_path = path if path.startswith("/") else f"/{path}"
    base = base_url.rstrip("/")
    url = f"{base}{target_path}"
    if query:
        encoded = urllib.parse.urlencode({k: v for k, v in query.items() if v is not None})
        if encoded:
            url = f"{url}?{encoded}"

    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")

    request = urllib.request.Request(url=url, data=data, method=method.upper())
    for key, value in headers.items():
        request.add_header(key, value)

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            text = response.read().decode(charset)
    except urllib.error.HTTPError as exc:
        charset = exc.headers.get_content_charset() or "utf-8"
        text = exc.read().decode(charset, errors="replace")
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = {"status": exc.code, "body": text}
        raise RuntimeError(json.dumps(payload, ensure_ascii=False))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"请求失败: {exc}") from exc

    if not text.strip():
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}


def update_session_with_auth(
    session: dict[str, Any],
    response: dict[str, Any],
    *,
    base_url: str,
    device_id: str,
) -> dict[str, Any]:
    data = response.get("data") or {}
    session["baseUrl"] = base_url.rstrip("/")
    session["language"] = session.get("language", DEFAULT_LANGUAGE)
    session["platform"] = str(session.get("platform", DEFAULT_PLATFORM))
    session["packageName"] = session.get("packageName", DEFAULT_PACKAGE)
    session.pop("timezone", None)
    session["deviceId"] = device_id
    session["xDeviceId"] = device_id
    for key in ("accountId", "userId", "token", "refreshToken", "expireTimeAt", "loginType", "isFirst"):
        if key in data and data[key] is not None:
            session[key] = data[key]
    return session


def require_success(response: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(response, dict):
        raise RuntimeError("接口返回不是 JSON 对象。")
    code = response.get("code")
    if code not in (0, "0", None):
        raise RuntimeError(json.dumps(response, ensure_ascii=False, indent=2))
    return response


def resolve_device_id(args: argparse.Namespace, session: dict[str, Any]) -> str:
    if getattr(args, "device_id", None):
        return args.device_id
    if session.get("deviceId"):
        return str(session["deviceId"])
    return uuid.uuid4().hex


def resolve_base_url(args: argparse.Namespace, session: dict[str, Any]) -> str:
    explicit_base_url = getattr(args, "base_url", None)
    if explicit_base_url:
        return explicit_base_url
    if session.get("baseUrl"):
        return str(session["baseUrl"])
    return default_base_url_for_env(resolve_session_env(args))


def sync_session_connection(
    session: dict[str, Any],
    *,
    base_url: str,
    device_id: str,
) -> dict[str, Any]:
    session["deviceId"] = device_id
    session["xDeviceId"] = device_id
    session["baseUrl"] = base_url.rstrip("/")
    session.pop("timezone", None)
    return session


def load_structured_value(
    json_body: str | None,
    json_file: str | None,
    *,
    field_name: str,
    expected_type: type | tuple[type, ...],
) -> Any:
    value = load_json_payload(json_body, json_file)
    if value is None:
        return None
    if not isinstance(value, expected_type):
        if isinstance(expected_type, tuple):
            type_name = " 或 ".join(t.__name__ for t in expected_type)
        else:
            type_name = expected_type.__name__
        raise RuntimeError(f"{field_name} 必须是 JSON {type_name}。")
    return value


def extract_primary_media_url(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, dict):
        for key in ("url", "avatar", "background", "src"):
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate.strip():
                return candidate.strip()
    return None


def run_web_config_get(
    args: argparse.Namespace,
    session: dict[str, Any],
    *,
    platform: str = DEFAULT_WEB_PLATFORM,
    version: str = DEFAULT_WEB_VERSION,
    buildnumber: str = DEFAULT_WEB_BUILDNUMBER,
    brand: str = DEFAULT_WEB_BRAND,
    model: str = DEFAULT_WEB_MODEL,
    system_version: str = DEFAULT_WEB_SYSTEM_VERSION,
) -> tuple[dict[str, Any], str, str]:
    runtime_session = dict(session)
    apply_header_args_to_session(runtime_session, args)
    runtime_session["platform"] = str(platform)
    base_url = resolve_base_url(args, runtime_session)
    device_id = resolve_device_id(args, runtime_session)
    headers = build_web_headers(
        runtime_session,
        device_id=device_id,
        version=version,
        buildnumber=buildnumber,
        brand=brand,
        model=model,
        system_version=system_version,
    )
    apply_optional_access_token(headers, runtime_session)
    response = require_success(
        request_json(
            method="GET",
            base_url=base_url,
            path="/outer/api/nl/v1/web/config/get",
            headers=headers,
            timeout=args.timeout,
        )
    )
    return response, base_url, device_id


def get_default_org_avatar(
    args: argparse.Namespace,
    session: dict[str, Any],
) -> tuple[str, dict[str, Any]]:
    response, _, _ = run_web_config_get(args, session, platform=DEFAULT_WEB_PLATFORM)
    avatars = ((response.get("data") or {}).get("groupAvatarList") or [])
    for avatar in avatars:
        url = extract_primary_media_url(avatar)
        if url:
            return url, avatar
    raise RuntimeError("web-config-get 没有返回可用的默认组织头像。")


def build_org_request_body(args: argparse.Namespace, session: dict[str, Any], *, include_name: bool) -> dict[str, Any]:
    body = load_json_payload(args.json_body, args.json_file)
    if body is None:
        body = {}
    if not isinstance(body, dict):
        raise RuntimeError("组织请求体必须是 JSON 对象。")

    if include_name and args.name is not None:
        body["name"] = args.name
    if getattr(args, "org_id", None) is not None:
        body["id"] = args.org_id

    for source_key, target_key in (
        ("avatar", "avatar"),
        ("background", "background"),
        ("info", "info"),
        ("tag_id", "tagId"),
        ("location", "location"),
        ("country", "country"),
        ("city", "city"),
        ("region", "region"),
        ("diplomat", "diplomat"),
    ):
        value = getattr(args, source_key, None)
        if value is not None:
            body[target_key] = value

    avatar_new = load_structured_value(args.avatar_new_json, args.avatar_new_file, field_name="avatarNew", expected_type=dict)
    if avatar_new is not None:
        body["avatarNew"] = avatar_new
        body.setdefault("avatar", extract_primary_media_url(avatar_new))

    background_new = load_structured_value(
        args.background_new_json,
        args.background_new_file,
        field_name="backgroundNew",
        expected_type=dict,
    )
    if background_new is not None:
        body["backgroundNew"] = background_new
        body.setdefault("background", extract_primary_media_url(background_new))

    settings = load_structured_value(args.settings_json, args.settings_file, field_name="settings", expected_type=dict)
    if settings is not None:
        body["settings"] = settings

    rule_info = load_structured_value(args.rule_info_json, args.rule_info_file, field_name="ruleInfo", expected_type=list)
    if rule_info is not None:
        body["ruleInfo"] = rule_info

    avatar_url = extract_primary_media_url(body.get("avatar"))
    if avatar_url:
        body["avatar"] = avatar_url
    elif include_name:
        default_avatar_url, default_avatar = get_default_org_avatar(args, session)
        body["avatar"] = default_avatar_url
        body.setdefault("avatarNew", default_avatar)

    background_url = extract_primary_media_url(body.get("background"))
    if background_url:
        body["background"] = background_url

    if include_name and not body.get("name"):
        raise RuntimeError("创建组织至少要提供名称，请传 --name 或在 JSON 请求体中提供 name。")
    if include_name and not body.get("avatar"):
        raise RuntimeError("创建组织未拿到可用头像，请显式传 --avatar，或检查 web-config-get。")
    if not include_name and not body.get("id"):
        raise RuntimeError("更新组织至少要提供 --org-id，或在 JSON 请求体中提供 id。")

    return body


def cmd_session_show(args: argparse.Namespace) -> int:
    path = session_path(args)
    source_path, session = load_session_source(path)
    pretty_print(
        {
            "env": resolve_session_env(args),
            "sessionFile": str(path),
            "loadedFrom": str(source_path) if source_path else None,
            "exists": source_path is not None,
            "session": redact_session_for_display(session),
        }
    )
    return 0


def cmd_session_clear(args: argparse.Namespace) -> int:
    path = session_path(args)
    source_path, session = load_session_source(path)
    if not session:
        pretty_print({"cleared": False, "reason": "session 不存在"})
        return 0
    if args.keep_device_id and session.get("deviceId"):
        keep = {
            "deviceId": session["deviceId"],
            "xDeviceId": session["deviceId"],
            "baseUrl": session.get("baseUrl", default_base_url_for_env(resolve_session_env(args))),
            "language": session.get("language", DEFAULT_LANGUAGE),
            "platform": str(session.get("platform", DEFAULT_PLATFORM)),
            "packageName": session.get("packageName", DEFAULT_PACKAGE),
        }
        save_session(path, keep)
        if source_path and source_path != path:
            source_path.unlink(missing_ok=True)
        pretty_print({"cleared": True, "keptDeviceId": keep["deviceId"], "sessionFile": str(path), "env": resolve_session_env(args)})
        return 0
    path.unlink(missing_ok=True)
    if source_path and source_path != path:
        source_path.unlink(missing_ok=True)
    pretty_print({"cleared": True, "sessionFile": str(path)})
    return 0


def cmd_guest_generate(args: argparse.Namespace) -> int:
    path = session_path(args)
    session = load_session(path)
    apply_header_args_to_session(session, args)
    base_url = resolve_base_url(args, session)
    device_id = resolve_device_id(args, session)
    headers = build_base_headers(session, device_id=device_id)
    response = require_success(
        request_json(
            method="POST",
            base_url=base_url,
            path="/outer/api/nl/v1/guest/generate",
            headers=headers,
            timeout=args.timeout,
        )
    )
    save_session(path, update_session_with_auth(session, response, base_url=base_url, device_id=device_id))
    pretty_print(response)
    return 0


def cmd_agent_login(args: argparse.Namespace) -> int:
    path = session_path(args)
    session = load_session(path)
    apply_header_args_to_session(session, args)
    base_url = resolve_base_url(args, session)
    device_id = resolve_device_id(args, session)
    body = {
        "openId": args.open_id,
        "unionId": args.union_id,
        "loginType": 99,
        "nickName": args.nick_name,
        "gender": args.gender,
        "avatar": args.avatar,
        "email": args.email,
        "clientType": args.client_type,
        "channelId": args.channel_id,
        "code": args.code,
        "redirectUri": args.redirect_uri,
    }
    body = {key: value for key, value in body.items() if value is not None}
    headers = build_base_headers(session, device_id=device_id)
    response = require_success(
        request_json(
            method="POST",
            base_url=base_url,
            path="/outer/api/nl/v2/user/fastThirdLogin",
            headers=headers,
            body=body,
            timeout=args.timeout,
        )
    )
    save_session(path, update_session_with_auth(session, response, base_url=base_url, device_id=device_id))
    pretty_print(response)
    return 0


def cmd_refresh(args: argparse.Namespace) -> int:
    path = session_path(args)
    session = load_session(path)
    base_url = resolve_base_url(args, session)
    device_id = resolve_device_id(args, session)
    headers = build_base_headers(session, device_id=device_id)
    apply_auth_header(headers, session, "refresh")
    response = require_success(
        request_json(
            method="POST",
            base_url=base_url,
            path="/outer/api/nl/v1/user/refresh",
            headers=headers,
            timeout=args.timeout,
        )
    )
    save_session(path, update_session_with_auth(session, response, base_url=base_url, device_id=device_id))
    pretty_print(response)
    return 0


def cmd_user_info(args: argparse.Namespace) -> int:
    return run_common_request(
        args,
        method="GET",
        path="/outer/api/v1/common/user/info/basic",
        auth_mode="access",
    )


def cmd_user_update(args: argparse.Namespace) -> int:
    avatar = None
    if args.avatar_json:
        avatar = json.loads(args.avatar_json)
    elif args.avatar_file:
        avatar = json.loads(Path(args.avatar_file).read_text(encoding="utf-8"))
    body = {"nickName": args.nick_name}
    if avatar is not None:
        body["avatar"] = avatar
    return run_common_request(
        args,
        method="POST",
        path="/outer/api/v1/common/user/info/update",
        auth_mode="access",
        body=body,
    )


def cmd_post_create(args: argparse.Namespace) -> int:
    path = session_path(args)
    session = load_session(path)
    runtime_session = dict(session)
    apply_header_args_to_session(runtime_session, args)
    base_url = resolve_base_url(args, runtime_session)
    device_id = resolve_device_id(args, runtime_session)
    headers = build_web_headers(
        runtime_session,
        device_id=device_id,
        version=args.version,
        buildnumber=args.buildnumber,
        brand=args.brand,
        model=args.model,
        system_version=args.system_version,
    )
    apply_auth_header(headers, runtime_session, "access")

    body = load_json_payload(args.json_body, args.json_file)
    if body is None:
        if args.org_id is None or not args.text:
            raise RuntimeError("发帖至少要提供 --json-body/--json-file，或同时提供 --org-id 和 --text。")
        body = {
            "orgId": args.org_id,
            "article": {
                "richText": rich_text_from_text(args.text),
                "visibled": args.visibled,
                "vcmUids": parse_csv_values(args.vcm_uids),
            },
            "saasList": [],
        }

    response = require_success(
        request_json(
            method="POST",
            base_url=base_url,
            path="/outer/api/proxy/meta/api/v1/content/article/create",
            headers=headers,
            body=body,
            timeout=args.timeout,
        )
    )
    save_session(
        path,
        sync_session_connection(
            session,
            base_url=base_url,
            device_id=device_id,
        ),
    )
    pretty_print(response)
    return 0


def cmd_web_config_get(args: argparse.Namespace) -> int:
    path = session_path(args)
    session = load_session(path)
    response, base_url, device_id = run_web_config_get(
        args,
        session,
        platform=args.platform,
        version=args.version,
        buildnumber=args.buildnumber,
        brand=args.brand,
        model=args.model,
        system_version=args.system_version,
    )
    save_session(
        path,
        sync_session_connection(
            session,
            base_url=base_url,
            device_id=device_id,
        ),
    )
    pretty_print(response)
    return 0


def cmd_org_list(args: argparse.Namespace) -> int:
    query = {
        "page": args.page,
        "pageSize": args.page_size,
        "nextId": args.next_id,
        "userId": args.user_id,
        "my": args.my,
        "cs": args.cs,
        "type": args.type,
        "keyword": args.keyword,
    }
    return run_common_request(
        args,
        method="GET",
        path="/outer/api/v1/common/user/org/page",
        auth_mode="access",
        query=query,
    )


def cmd_org_detail(args: argparse.Namespace) -> int:
    return run_common_request(
        args,
        method="GET",
        path="/outer/api/v1/common/org/info/detail",
        auth_mode="access",
        query={"id": args.org_id},
    )


def cmd_org_basic(args: argparse.Namespace) -> int:
    return run_common_request(
        args,
        method="GET",
        path="/outer/api/v1/common/org/info/basic",
        auth_mode="access",
        query={"id": args.org_id},
    )


def cmd_org_create(args: argparse.Namespace) -> int:
    path = session_path(args)
    session = load_session(path)
    apply_header_args_to_session(session, args)
    body = build_org_request_body(args, session, include_name=True)
    base_url = resolve_base_url(args, session)
    device_id = resolve_device_id(args, session)
    headers = build_base_headers(session, device_id=device_id)
    apply_auth_header(headers, session, "access")
    response = require_success(
        request_json(
            method="POST",
            base_url=base_url,
            path="/outer/api/v1/common/org/create",
            headers=headers,
            body=body,
            timeout=args.timeout,
        )
    )
    save_session(
        path,
        sync_session_connection(
            session,
            base_url=base_url,
            device_id=device_id,
        ),
    )
    pretty_print(response)
    return 0


def cmd_org_update(args: argparse.Namespace) -> int:
    path = session_path(args)
    session = load_session(path)
    apply_header_args_to_session(session, args)
    body = build_org_request_body(args, session, include_name=False)
    base_url = resolve_base_url(args, session)
    device_id = resolve_device_id(args, session)
    headers = build_base_headers(session, device_id=device_id)
    apply_auth_header(headers, session, "access")
    response = require_success(
        request_json(
            method="PUT",
            base_url=base_url,
            path="/outer/api/v1/common/org/update",
            headers=headers,
            body=body,
            timeout=args.timeout,
        )
    )
    save_session(
        path,
        sync_session_connection(
            session,
            base_url=base_url,
            device_id=device_id,
        ),
    )
    pretty_print(response)
    return 0


def cmd_org_member_list(args: argparse.Namespace) -> int:
    return run_common_request(
        args,
        method="GET",
        path="/outer/api/v1/common/org/member/list",
        auth_mode="access",
        query={"orgId": args.org_id},
    )


def cmd_org_member_page(args: argparse.Namespace) -> int:
    query = {
        "orgId": args.org_id,
        "page": args.page,
        "count": args.count,
        "mtype": args.mtype,
        "enablePost": args.enable_post,
        "keyword": args.keyword,
        "lids": args.lids,
    }
    return run_common_request(
        args,
        method="GET",
        path="/outer/api/v1/common/org/member/page",
        auth_mode="access",
        query=query,
    )


def cmd_join_org(args: argparse.Namespace) -> int:
    body = {"orgId": args.org_id}
    if args.room_id is not None:
        body["roomId"] = args.room_id
    return run_common_request(
        args,
        method="POST",
        path="/outer/api/v1/common/voiceroom/member/joinOrg",
        auth_mode="access",
        body=body,
    )


def require_json_body(args: argparse.Namespace, message: str) -> dict[str, Any]:
    body = load_json_payload(args.json_body, args.json_file)
    if body is None:
        raise RuntimeError(message)
    if not isinstance(body, dict):
        raise RuntimeError("请求体必须是 JSON 对象。")
    return body


def cmd_activity_save(args: argparse.Namespace) -> int:
    body = require_json_body(args, "请通过 --json-body 或 --json-file 提供活动草稿请求体。")
    ensure_only_free_tickets(body)
    return run_common_request(
        args,
        method="PUT",
        path="/outer/api/v1/common/activity/save",
        auth_mode="access",
        body=body,
    )


def cmd_activity_publish(args: argparse.Namespace) -> int:
    body = load_json_payload(args.json_body, args.json_file)
    if body is None:
        if args.draft_id is None:
            raise RuntimeError("请通过 --draft-id，或 --json-body/--json-file 提供活动草稿 id。")
        body = {"id": args.draft_id}
    if not isinstance(body, dict):
        raise RuntimeError("活动发布请求体必须是 JSON 对象。")
    if not body.get("id"):
        raise RuntimeError("activity-publish 至少要提供草稿 id。")
    if "tickets" in body:
        ensure_only_free_tickets(body)
    return run_common_request(
        args,
        method="POST",
        path="/outer/api/v1/common/activity/publish",
        auth_mode="access",
        body=body,
    )


def cmd_activity_cancel(args: argparse.Namespace) -> int:
    body = load_json_payload(args.json_body, args.json_file)
    if body is None:
        if args.activity_id is None:
            raise RuntimeError("请提供 --activity-id，或通过 --json-body/--json-file 提供请求体。")
        body = {"id": args.activity_id}
    return run_common_request(
        args,
        method="PUT",
        path="/outer/api/v1/common/activity/cancel",
        auth_mode="access",
        body=body,
    )


def cmd_activity_delete(args: argparse.Namespace) -> int:
    body = load_json_payload(args.json_body, args.json_file)
    if body is None:
        if args.activity_id is None:
            raise RuntimeError("请提供 --activity-id，或通过 --json-body/--json-file 提供请求体。")
        body = {"id": args.activity_id}
    return run_common_request(
        args,
        method="DELETE",
        path="/outer/api/v1/common/activity/delete",
        auth_mode="access",
        body=body,
    )


def cmd_activity_detail(args: argparse.Namespace) -> int:
    return run_common_request(
        args,
        method="GET",
        path="/outer/api/v1/common/activity/detail",
        auth_mode="access",
        query={"id": args.activity_id},
    )


def cmd_activity_search(args: argparse.Namespace) -> int:
    query = {
        "keyword": args.keyword,
        "page": args.page,
        "pageSize": args.page_size,
        "nextId": args.next_id,
    }
    return run_common_request(
        args,
        method="GET",
        path="/outer/api/v1/common/activity/search",
        auth_mode="access",
        query=query,
    )


def cmd_activity_org_list(args: argparse.Namespace) -> int:
    query = {
        "orgId": args.org_id,
        "tab": args.tab,
        "location": args.location,
        "keyword": args.keyword,
        "page": args.page,
        "pageSize": args.page_size,
        "nextId": args.next_id,
    }
    return run_common_request(
        args,
        method="GET",
        path="/outer/api/v1/common/activity/org/ac",
        auth_mode="access",
        query=query,
    )


def cmd_activity_user_sign_list(args: argparse.Namespace) -> int:
    return run_common_request(
        args,
        method="GET",
        path="/outer/api/v1/common/activity/user/sign/list",
        auth_mode="access",
    )


def cmd_activity_sign_list(args: argparse.Namespace) -> int:
    query = {
        "activityId": args.activity_id,
        "page": args.page,
        "pageSize": args.page_size,
        "nextId": args.next_id,
    }
    return run_common_request(
        args,
        method="GET",
        path="/outer/api/v1/common/activity/sign/signList",
        auth_mode="access",
        query=query,
    )


def cmd_activity_signup(args: argparse.Namespace) -> int:
    body = load_json_payload(args.json_body, args.json_file)
    if body is None:
        if args.activity_id is None or args.ticket_id is None:
            raise RuntimeError("报名至少要提供 --json-body/--json-file，或同时提供 --activity-id 和 --ticket-id。")
        body = {
            "id": args.activity_id,
            "fullName": args.full_name,
            "phone": args.phone,
            "email": args.email,
            "answer": args.answer,
            "paid": args.paid,
            "tickets": [{"id": args.ticket_id, "quantity": args.quantity}],
        }
        body = {key: value for key, value in body.items() if value is not None}
    return run_common_request(
        args,
        method="POST",
        path="/outer/api/v1/common/activity/orders/signup",
        auth_mode="access",
        body=body,
    )


def cmd_request(args: argparse.Namespace) -> int:
    body = load_json_payload(args.json_body, args.json_file)
    query = parse_key_value_pairs(args.query)
    return run_common_request(
        args,
        method=args.method,
        path=args.path,
        auth_mode=args.auth_mode,
        query=query,
        body=body,
    )


def run_common_request(
    args: argparse.Namespace,
    *,
    method: str,
    path: str,
    auth_mode: str,
    query: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
) -> int:
    session = load_session(session_path(args))
    apply_header_args_to_session(session, args)
    base_url = resolve_base_url(args, session)
    device_id = resolve_device_id(args, session)
    headers = build_base_headers(session, device_id=device_id)
    apply_auth_header(headers, session, auth_mode)
    response = require_success(
        request_json(
            method=method,
            base_url=base_url,
            path=path,
            headers=headers,
            query=query,
            body=body,
            timeout=args.timeout,
        )
    )
    if auth_mode in {"access", "refresh"} or session.get("deviceId") != device_id:
        save_session(
            session_path(args),
            sync_session_connection(session, base_url=base_url, device_id=device_id),
        )
    pretty_print(response)
    return 0


def add_shared_session_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--session-file", help="显式指定 session 文件路径；不传则按 env 写入用户状态目录")
    parser.add_argument("--env", dest="env_name", help=f"环境名，默认 {DEFAULT_ENV_NAME}；常用 prod/test/local")
    parser.add_argument("--base-url", help=f"接口基座，默认 {DEFAULT_BASE_URL}")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="请求超时秒数")


def add_root_global_session_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--session-file", dest="global_session_file", help="全局 session 文件路径，可写在命令前")
    parser.add_argument("--env", dest="global_env_name", help=f"全局环境名，默认 {DEFAULT_ENV_NAME}")
    parser.add_argument("--base-url", dest="global_base_url", help="全局接口基座，可写在命令前")
    parser.add_argument("--timeout", dest="global_timeout", type=int, help="全局请求超时秒数，可写在命令前")


def merge_global_session_args(args: argparse.Namespace) -> argparse.Namespace:
    if getattr(args, "global_session_file", None):
        args.session_file = args.global_session_file
    if getattr(args, "global_env_name", None):
        args.env_name = args.global_env_name
    if getattr(args, "global_base_url", None):
        args.base_url = args.global_base_url
    if getattr(args, "global_timeout", None) is not None:
        args.timeout = args.global_timeout
    return args


def add_shared_header_args(parser: argparse.ArgumentParser, *, default_platform: str = DEFAULT_PLATFORM) -> None:
    parser.add_argument("--language", default=DEFAULT_LANGUAGE, help=f"x-language，默认 {DEFAULT_LANGUAGE}")
    parser.add_argument("--platform", default=default_platform, help=f"x-platform，默认 {default_platform}")
    parser.add_argument("--package-name", default=DEFAULT_PACKAGE, help=f"x-package，默认 {DEFAULT_PACKAGE}")
    parser.add_argument("--timezone", help=f"x-timezone，默认 {DEFAULT_TIMEZONE_HELP}")
    parser.add_argument("--device-id", help="显式指定 x-device-id；不传则复用 session 中的值或自动生成")


def add_json_body_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json-body", help="JSON 字符串请求体")
    parser.add_argument("--json-file", help="JSON 文件请求体")


def add_shared_web_client_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--version", default=DEFAULT_WEB_VERSION, help=f"x-version，默认 {DEFAULT_WEB_VERSION}")
    parser.add_argument("--buildnumber", default=DEFAULT_WEB_BUILDNUMBER, help=f"x-buildnumber，默认 {DEFAULT_WEB_BUILDNUMBER}")
    parser.add_argument("--brand", default=DEFAULT_WEB_BRAND, help=f"x-brand，默认 {DEFAULT_WEB_BRAND}")
    parser.add_argument("--model", default=DEFAULT_WEB_MODEL, help=f"x-model，默认 {DEFAULT_WEB_MODEL}")
    parser.add_argument(
        "--system-version",
        dest="system_version",
        default=DEFAULT_WEB_SYSTEM_VERSION,
        help=f"x-system-version，默认 {DEFAULT_WEB_SYSTEM_VERSION}",
    )


def add_org_body_args(parser: argparse.ArgumentParser, *, include_name: bool) -> None:
    if include_name:
        parser.add_argument("--name", help="组织名称")
    else:
        parser.add_argument("--org-id", type=int, help="组织 ID")
    parser.add_argument("--avatar", help="组织头像 URL")
    parser.add_argument("--avatar-new-json", help="avatarNew JSON 字符串")
    parser.add_argument("--avatar-new-file", help="avatarNew JSON 文件路径")
    parser.add_argument("--background", help="组织背景 URL")
    parser.add_argument("--background-new-json", help="backgroundNew JSON 字符串")
    parser.add_argument("--background-new-file", help="backgroundNew JSON 文件路径")
    parser.add_argument("--info", help="组织简介")
    parser.add_argument("--tag-id", type=int, help="组织标签 ID")
    parser.add_argument("--location", help="位置描述")
    parser.add_argument("--country", help="国家")
    parser.add_argument("--city", help="城市")
    parser.add_argument("--region", help="地区")
    parser.add_argument("--diplomat", type=int, help="外交官用户 ID")
    parser.add_argument("--settings-json", help="settings JSON 字符串")
    parser.add_argument("--settings-file", help="settings JSON 文件路径")
    parser.add_argument("--rule-info-json", help="ruleInfo JSON 字符串")
    parser.add_argument("--rule-info-file", help="ruleInfo JSON 文件路径")
    add_json_body_args(parser)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="organization-operating-skill 可执行 CLI",
        epilog=HELP_EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_root_global_session_args(parser)
    subparsers = parser.add_subparsers(dest="command", required=True)

    session_parser = subparsers.add_parser("session", help="查看或清理本地 session")
    add_shared_session_args(session_parser)
    session_subparsers = session_parser.add_subparsers(dest="session_command", required=True)

    show_parser = session_subparsers.add_parser("show", help="显示当前 session")
    show_parser.set_defaults(func=cmd_session_show)

    clear_parser = session_subparsers.add_parser("clear", help="清理当前 session")
    clear_parser.add_argument("--keep-device-id", action="store_true", help="清理 token，但保留 deviceId")
    clear_parser.set_defaults(func=cmd_session_clear)

    guest_parser = subparsers.add_parser("guest-generate", help="生成游客账号并保存 token；首次建 agent 前先调用")
    add_shared_session_args(guest_parser)
    add_shared_header_args(guest_parser)
    guest_parser.set_defaults(func=cmd_guest_generate)

    login_parser = subparsers.add_parser("agent-login", help="首次把游客账号升级为 agent 账号，使用 loginType=99")
    add_shared_session_args(login_parser)
    add_shared_header_args(login_parser)
    login_parser.add_argument("--open-id", required=True, help="agent 稳定 openId")
    login_parser.add_argument("--union-id", required=True, help="agent 稳定 unionId")
    login_parser.add_argument("--nick-name")
    login_parser.add_argument("--gender", type=int)
    login_parser.add_argument("--avatar")
    login_parser.add_argument("--email")
    login_parser.add_argument("--client-type", type=int)
    login_parser.add_argument("--channel-id", type=int)
    login_parser.add_argument("--code")
    login_parser.add_argument("--redirect-uri")
    login_parser.set_defaults(func=cmd_agent_login)

    refresh_parser = subparsers.add_parser("refresh", help="刷新 access token 并更新 session")
    add_shared_session_args(refresh_parser)
    add_shared_header_args(refresh_parser)
    refresh_parser.set_defaults(func=cmd_refresh)

    user_info_parser = subparsers.add_parser("user-info", help="查询当前用户基础资料")
    add_shared_session_args(user_info_parser)
    add_shared_header_args(user_info_parser)
    user_info_parser.set_defaults(func=cmd_user_info)

    user_update_parser = subparsers.add_parser("user-update", help="更新昵称和头像")
    add_shared_session_args(user_update_parser)
    add_shared_header_args(user_update_parser)
    user_update_parser.add_argument("--nick-name", required=True)
    user_update_parser.add_argument("--avatar-json", help="头像 JSON 字符串")
    user_update_parser.add_argument("--avatar-file", help="头像 JSON 文件路径")
    user_update_parser.set_defaults(func=cmd_user_update)

    post_create_parser = subparsers.add_parser("post-create", help="在组织内发布帖子")
    add_shared_session_args(post_create_parser)
    add_shared_header_args(post_create_parser, default_platform=DEFAULT_WEB_PLATFORM)
    post_create_parser.add_argument("--org-id", type=int, help="组织 ID；使用简化文本发帖时必填")
    post_create_parser.add_argument("--text", help="帖子正文；会自动转成 richText")
    post_create_parser.add_argument("--visibled", type=int, default=0, help="0公开 1组织内 2仅会员 3自定义，默认 0")
    post_create_parser.add_argument("--vcm-uids", help="自定义可见用户 ID，逗号分隔")
    add_json_body_args(post_create_parser)
    add_shared_web_client_args(post_create_parser)
    post_create_parser.set_defaults(func=cmd_post_create)

    web_config_parser = subparsers.add_parser("web-config-get", help="获取 web 端配置，包括默认组织头像列表")
    add_shared_session_args(web_config_parser)
    add_shared_header_args(web_config_parser, default_platform=DEFAULT_WEB_PLATFORM)
    add_shared_web_client_args(web_config_parser)
    web_config_parser.set_defaults(func=cmd_web_config_get)

    org_list_parser = subparsers.add_parser("org-list", help="查询我的或他人的组织列表")
    add_shared_session_args(org_list_parser)
    add_shared_header_args(org_list_parser)
    org_list_parser.add_argument("--page", type=int, default=1)
    org_list_parser.add_argument("--page-size", type=int, default=10)
    org_list_parser.add_argument("--next-id", type=int, default=0)
    org_list_parser.add_argument("--user-id", type=int, default=0)
    org_list_parser.add_argument("--my", type=int, default=0)
    org_list_parser.add_argument("--cs", type=int, default=0)
    org_list_parser.add_argument("--type", type=int, default=0)
    org_list_parser.add_argument("--keyword")
    org_list_parser.set_defaults(func=cmd_org_list)

    org_detail_parser = subparsers.add_parser("org-detail", help="查询组织主页详情")
    add_shared_session_args(org_detail_parser)
    add_shared_header_args(org_detail_parser)
    org_detail_parser.add_argument("--org-id", type=int, required=True)
    org_detail_parser.set_defaults(func=cmd_org_detail)

    org_basic_parser = subparsers.add_parser("org-basic", help="查询组织基础信息（管理态补充接口）")
    add_shared_session_args(org_basic_parser)
    add_shared_header_args(org_basic_parser)
    org_basic_parser.add_argument("--org-id", type=int, required=True)
    org_basic_parser.set_defaults(func=cmd_org_basic)

    org_create_parser = subparsers.add_parser("org-create", help="创建组织；不传头像时自动从 web-config-get 取默认头像")
    add_shared_session_args(org_create_parser)
    add_shared_header_args(org_create_parser)
    add_org_body_args(org_create_parser, include_name=True)
    org_create_parser.set_defaults(func=cmd_org_create)

    org_update_parser = subparsers.add_parser("org-update", help="修改组织，不支持改名称")
    add_shared_session_args(org_update_parser)
    add_shared_header_args(org_update_parser)
    add_org_body_args(org_update_parser, include_name=False)
    org_update_parser.set_defaults(func=cmd_org_update)

    org_member_list_parser = subparsers.add_parser("org-member-list", help="查询组织全部成员（非分页）")
    add_shared_session_args(org_member_list_parser)
    add_shared_header_args(org_member_list_parser)
    org_member_list_parser.add_argument("--org-id", type=int, required=True)
    org_member_list_parser.set_defaults(func=cmd_org_member_list)

    org_member_page_parser = subparsers.add_parser("org-member-page", help="分页查询组织成员")
    add_shared_session_args(org_member_page_parser)
    add_shared_header_args(org_member_page_parser)
    org_member_page_parser.add_argument("--org-id", type=int, required=True)
    org_member_page_parser.add_argument("--page", type=int, default=1)
    org_member_page_parser.add_argument("--count", type=int, default=20)
    org_member_page_parser.add_argument("--mtype", type=int, default=1, help="默认 1，2 会被服务端转为关注者视图")
    org_member_page_parser.add_argument("--enable-post", type=int)
    org_member_page_parser.add_argument("--keyword")
    org_member_page_parser.add_argument("--lids", help="按等级筛选，分号分隔，如 1;2;3")
    org_member_page_parser.set_defaults(func=cmd_org_member_page)

    join_org_parser = subparsers.add_parser("join-org", help="加入组织")
    add_shared_session_args(join_org_parser)
    add_shared_header_args(join_org_parser)
    join_org_parser.add_argument("--org-id", type=int, required=True)
    join_org_parser.add_argument("--room-id", default="", help="默认空字符串")
    join_org_parser.set_defaults(func=cmd_join_org)

    activity_save_parser = subparsers.add_parser("activity-save", help="保存活动草稿，返回 draft id")
    add_shared_session_args(activity_save_parser)
    add_shared_header_args(activity_save_parser)
    add_json_body_args(activity_save_parser)
    activity_save_parser.set_defaults(func=cmd_activity_save)

    activity_publish_parser = subparsers.add_parser("activity-publish", help="发布已保存的活动草稿，仅允许免费票")
    add_shared_session_args(activity_publish_parser)
    add_shared_header_args(activity_publish_parser)
    activity_publish_parser.add_argument("--draft-id", type=int, help="activity-save 返回的草稿 ID")
    add_json_body_args(activity_publish_parser)
    activity_publish_parser.set_defaults(func=cmd_activity_publish)

    activity_cancel_parser = subparsers.add_parser("activity-cancel", help="下架活动")
    add_shared_session_args(activity_cancel_parser)
    add_shared_header_args(activity_cancel_parser)
    activity_cancel_parser.add_argument("--activity-id", type=int, help="活动 ID")
    add_json_body_args(activity_cancel_parser)
    activity_cancel_parser.set_defaults(func=cmd_activity_cancel)

    activity_delete_parser = subparsers.add_parser("activity-delete", help="删除活动")
    add_shared_session_args(activity_delete_parser)
    add_shared_header_args(activity_delete_parser)
    activity_delete_parser.add_argument("--activity-id", type=int, help="活动 ID")
    add_json_body_args(activity_delete_parser)
    activity_delete_parser.set_defaults(func=cmd_activity_delete)

    activity_detail_parser = subparsers.add_parser("activity-detail", help="查询活动详情")
    add_shared_session_args(activity_detail_parser)
    add_shared_header_args(activity_detail_parser)
    activity_detail_parser.add_argument("--activity-id", type=int, required=True)
    activity_detail_parser.set_defaults(func=cmd_activity_detail)

    activity_search_parser = subparsers.add_parser("activity-search", help="搜索活动")
    add_shared_session_args(activity_search_parser)
    add_shared_header_args(activity_search_parser)
    activity_search_parser.add_argument("--keyword", required=True)
    activity_search_parser.add_argument("--page", type=int, default=1)
    activity_search_parser.add_argument("--page-size", type=int, default=10)
    activity_search_parser.add_argument("--next-id", type=int, default=0)
    activity_search_parser.set_defaults(func=cmd_activity_search)

    activity_org_list_parser = subparsers.add_parser("activity-org-list", help="查询组织活动列表")
    add_shared_session_args(activity_org_list_parser)
    add_shared_header_args(activity_org_list_parser)
    activity_org_list_parser.add_argument("--org-id", type=int)
    activity_org_list_parser.add_argument("--tab", type=int, default=0)
    activity_org_list_parser.add_argument("--location", default="")
    activity_org_list_parser.add_argument("--keyword", default="")
    activity_org_list_parser.add_argument("--page", type=int, default=1)
    activity_org_list_parser.add_argument("--page-size", type=int, default=10)
    activity_org_list_parser.add_argument("--next-id", type=int, default=0)
    activity_org_list_parser.set_defaults(func=cmd_activity_org_list)

    activity_user_sign_list_parser = subparsers.add_parser("activity-user-sign-list", help="查询当前用户已报名活动")
    add_shared_session_args(activity_user_sign_list_parser)
    add_shared_header_args(activity_user_sign_list_parser)
    activity_user_sign_list_parser.set_defaults(func=cmd_activity_user_sign_list)

    activity_sign_list_parser = subparsers.add_parser("activity-sign-list", help="查询活动报名列表")
    add_shared_session_args(activity_sign_list_parser)
    add_shared_header_args(activity_sign_list_parser)
    activity_sign_list_parser.add_argument("--activity-id", type=int, required=True)
    activity_sign_list_parser.add_argument("--page", type=int, default=1)
    activity_sign_list_parser.add_argument("--page-size", type=int, default=10)
    activity_sign_list_parser.add_argument("--next-id", type=int, default=0)
    activity_sign_list_parser.set_defaults(func=cmd_activity_sign_list)

    activity_signup_parser = subparsers.add_parser("activity-signup", help="活动报名")
    add_shared_session_args(activity_signup_parser)
    add_shared_header_args(activity_signup_parser)
    activity_signup_parser.add_argument("--activity-id", type=int, help="活动 ID")
    activity_signup_parser.add_argument("--ticket-id", help="票 ID")
    activity_signup_parser.add_argument("--quantity", type=int, default=1, help="购票数量，默认 1")
    activity_signup_parser.add_argument("--full-name")
    activity_signup_parser.add_argument("--phone")
    activity_signup_parser.add_argument("--email")
    activity_signup_parser.add_argument("--answer")
    activity_signup_parser.add_argument("--paid", type=int, default=0, help="默认 0，免费票报名")
    add_json_body_args(activity_signup_parser)
    activity_signup_parser.set_defaults(func=cmd_activity_signup)

    request_parser = subparsers.add_parser("request", help="发起通用 API 请求")
    add_shared_session_args(request_parser)
    add_shared_header_args(request_parser)
    request_parser.add_argument("--method", required=True, help="GET/POST/PUT/DELETE/PATCH")
    request_parser.add_argument("--path", required=True, help="相对 base-url 的路径")
    request_parser.add_argument("--auth-mode", choices=("none", "access", "refresh"), default="access")
    request_parser.add_argument("--query", action="append", help="查询参数，KEY=VALUE，可重复")
    add_json_body_args(request_parser)
    request_parser.set_defaults(func=cmd_request)

    return parser


def main(argv: list[str] | None = None) -> int:
    ensure_state_dir()
    parser = build_parser()
    args = parser.parse_args(argv)
    args = merge_global_session_args(args)
    try:
        return int(args.func(args))
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
