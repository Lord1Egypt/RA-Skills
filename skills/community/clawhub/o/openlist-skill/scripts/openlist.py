#!/usr/bin/env python
"""OpenList automation CLI for Codex skill workflows."""

import argparse
import getpass
import json
import os
import posixpath
import ssl
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request


DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_DELETE_POLICY = "delete_never"
DEFAULT_AUDIT_PATH = Path.home() / ".codex" / "openlist" / "audit.jsonl"
DEFAULT_CONFLICT_POLICY = "fail"
ALLOWED_CONFLICT_POLICIES = {"fail", "auto_rename", "skip"}
ALLOWED_RENAME_CONFLICT_POLICIES = {"fail", "auto_rename"}
ALLOWED_DELETE_POLICIES = {
    "delete_on_upload_succeed",
    "delete_on_upload_failed",
    "delete_never",
    "delete_always",
    "upload_download_stream",
}
ALLOWED_PLAN_TYPES = {"fs_move", "fs_rename", "fs_remove", "offline_create"}
ALLOWED_ENDPOINTS = {
    "/api/fs/move",
    "/api/fs/rename",
    "/api/fs/remove",
    "/api/fs/add_offline_download",
}
PLAN_ENDPOINTS = {
    "fs_move": "/api/fs/move",
    "fs_rename": "/api/fs/rename",
    "fs_remove": "/api/fs/remove",
    "offline_create": "/api/fs/add_offline_download",
}
TASK_TYPES = {
    "move": "/api/task/move",
    "offline_download": "/api/task/offline_download",
}


class UserFacingError(Exception):
    def __init__(
        self,
        message: str,
        *,
        openlist_code: Optional[int] = None,
        data: Optional[Any] = None,
        hints: Optional[Sequence[str]] = None,
        stderr: Optional[str] = None,
    ) -> None:
        super(UserFacingError, self).__init__(message)
        self.message = message
        self.openlist_code = openlist_code
        self.data = data
        self.hints = list(hints or [])
        self.stderr = stderr or message


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def new_uuid() -> str:
    return str(uuid.uuid4())


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_env_text(content: str) -> Dict[str, str]:
    values = {}
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        values[key] = value
    return values


def load_dotenv_values() -> Dict[str, str]:
    env_values = {}
    for env_file in (repo_root() / ".env", skill_root() / ".env"):
        if env_file.exists():
            env_values.update(parse_env_text(env_file.read_text(encoding="utf-8")))
    return env_values


def parse_bool(value: Optional[str], default: bool) -> bool:
    if value is None or value == "":
        return default
    lowered = str(value).strip().lower()
    if lowered in {"1", "true", "yes", "on"}:
        return True
    if lowered in {"0", "false", "no", "off"}:
        return False
    raise UserFacingError(
        "OPENLIST_VERIFY_TLS must be one of true/false/1/0.",
        hints=["Update OPENLIST_VERIFY_TLS in your environment or .env file."],
    )


def sanitize_base_url(base_url: Optional[str]) -> str:
    if not base_url:
        raise UserFacingError(
            "Missing OPENLIST_BASE_URL.",
            hints=[
                "Set OPENLIST_BASE_URL to your OpenList root URL, for example http://localhost:5244.",
                "You can also place the value in the repository .env or skills/openlist/.env file.",
            ],
        )
    parsed = urllib_parse.urlsplit(base_url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise UserFacingError(
            "OPENLIST_BASE_URL must be a valid http or https URL.",
            hints=["Example: OPENLIST_BASE_URL=http://localhost:5244"],
        )
    path = parsed.path.rstrip("/")
    return urllib_parse.urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))


def build_effective_env() -> Dict[str, str]:
    effective = load_dotenv_values()
    for key, value in os.environ.items():
        effective[key] = value
    return effective


def load_config(require_auth: bool = True) -> Dict[str, Any]:
    env_values = build_effective_env()
    config = {
        "base_url": sanitize_base_url(env_values.get("OPENLIST_BASE_URL")) if (require_auth or env_values.get("OPENLIST_BASE_URL")) else None,
        "token": env_values.get("OPENLIST_TOKEN", "").strip(),
        "timeout_seconds": DEFAULT_TIMEOUT_SECONDS,
        "verify_tls": parse_bool(env_values.get("OPENLIST_VERIFY_TLS"), True),
        "audit_path": Path(env_values.get("OPENLIST_AUDIT_PATH", str(DEFAULT_AUDIT_PATH))).expanduser(),
    }
    timeout_value = env_values.get("OPENLIST_TIMEOUT_SECONDS")
    if timeout_value:
        try:
            timeout_seconds = int(timeout_value)
        except ValueError:
            raise UserFacingError(
                "OPENLIST_TIMEOUT_SECONDS must be an integer.",
                hints=["Set OPENLIST_TIMEOUT_SECONDS to a positive whole number such as 30."],
            )
        if timeout_seconds <= 0:
            raise UserFacingError("OPENLIST_TIMEOUT_SECONDS must be greater than 0.")
        config["timeout_seconds"] = timeout_seconds
    if require_auth and not config["token"]:
        raise UserFacingError(
            "Missing OPENLIST_TOKEN.",
            hints=[
                "Set OPENLIST_TOKEN to an OpenList Admin Token or valid login token.",
                "Do not prefix the token with Bearer.",
            ],
        )
    return config


def join_base_url(base_url: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
    parsed = urllib_parse.urlsplit(base_url)
    base_path = parsed.path.rstrip("/")
    endpoint_path = endpoint if endpoint.startswith("/") else "/" + endpoint
    full_path = posixpath.normpath((base_path or "") + endpoint_path)
    if not full_path.startswith("/"):
        full_path = "/" + full_path
    query = urllib_parse.urlencode(params or {}, doseq=True)
    return urllib_parse.urlunsplit((parsed.scheme, parsed.netloc, full_path, query, ""))


def normalize_openlist_path(path_value: str, *, allow_root: bool = True) -> str:
    if path_value is None:
        raise UserFacingError("Path is required.")
    raw = str(path_value).strip()
    if not raw:
        raise UserFacingError("Path cannot be empty.")
    if not raw.startswith("/"):
        raise UserFacingError("OpenList paths must start with '/'.")
    segments = [segment for segment in raw.split("/") if segment not in {"", "."}]
    if ".." in segments:
        raise UserFacingError("OpenList paths cannot contain '..'.")
    normalized = "/" + "/".join(segments)
    if normalized == "/":
        if allow_root:
            return "/"
        raise UserFacingError("The root path '/' is not allowed for this operation.")
    return normalized


def split_dir_and_name(path_value: str) -> Tuple[str, str]:
    normalized = normalize_openlist_path(path_value, allow_root=False)
    parent = posixpath.dirname(normalized) or "/"
    name = posixpath.basename(normalized)
    if not name:
        raise UserFacingError("The path must point to a file or directory entry.")
    return parent, name


def validate_new_name(new_name: str) -> str:
    candidate = (new_name or "").strip()
    if not candidate:
        raise UserFacingError("The new name cannot be empty.")
    if candidate in {".", ".."} or "/" in candidate or "\\" in candidate:
        raise UserFacingError(
            "The new name must be a plain entry name without '/' or '\\'.",
            hints=["Example: report-2026.pdf"],
        )
    return candidate


def split_name_parts(name: str) -> Tuple[str, str]:
    if name.startswith(".") and name.count(".") == 1:
        return name, ""
    stem, ext = posixpath.splitext(name)
    return stem or name, ext


def generate_auto_name(existing_names: Iterable[str], desired_name: str) -> str:
    existing = set(existing_names)
    if desired_name not in existing:
        return desired_name
    stem, ext = split_name_parts(desired_name)
    index = 1
    while True:
        candidate = "%s (%d)%s" % (stem, index, ext)
        if candidate not in existing:
            return candidate
        index += 1


def choose_offline_tool(tools: Sequence[str]) -> Optional[str]:
    items = [item for item in tools if item]
    if not items:
        return None
    if "SimpleHttp" in items:
        return "SimpleHttp"
    return items[0]


def filter_urls(urls: Sequence[str]) -> List[str]:
    return [item.strip() for item in urls if item and item.strip()]


def make_hints(message: str, operation_type: Optional[str] = None) -> List[str]:
    lowered = (message or "").lower()
    hints = []
    if any(token in lowered for token in ["permission", "forbidden", "403"]):
        hints.append("Confirm the token has the required OpenList permissions for this path or task.")
    if "not found" in lowered or "does not exist" in lowered:
        hints.append("Use fs-get or fs-list to confirm the path or task ID before retrying.")
    if "exists" in lowered or "conflict" in lowered:
        hints.append("Retry with conflict-policy auto_rename or skip after reviewing the preview.")
    if any(token in lowered for token in ["timeout", "temporarily unavailable", "connection", "refused"]):
        hints.append("Check network reachability to OPENLIST_BASE_URL and verify timeout/TLS settings.")
    if "offline" in lowered and "tool" in lowered:
        hints.append("Run offline-tools to inspect the enabled download backends on this instance.")
    if operation_type == "offline_create":
        hints.append("Use task-info or task-list to inspect progress after creation.")
    return list(dict.fromkeys(hints))


def make_result(
    ok: bool,
    message: str,
    *,
    openlist_code: Optional[int] = None,
    data: Optional[Any] = None,
    tasks: Optional[List[Dict[str, Any]]] = None,
    audit_event_id: Optional[str] = None,
    hints: Optional[Sequence[str]] = None,
    rollback_hint: Optional[str] = None,
) -> Dict[str, Any]:
    result = {
        "ok": bool(ok),
        "message": message,
        "openlist_code": openlist_code,
        "data": data if data is not None else {},
        "tasks": list(tasks or []),
    }
    if audit_event_id:
        result["audit_event_id"] = audit_event_id
    if hints:
        result["hints"] = list(dict.fromkeys(hints))
    if rollback_hint:
        result["rollback_hint"] = rollback_hint
    return result


def sanitize_for_audit(value: Any) -> Any:
    sensitive_tokens = ("token", "authorization", "password", "secret")
    if isinstance(value, dict):
        sanitized = {}
        for key, item in value.items():
            if any(token in str(key).lower() for token in sensitive_tokens):
                sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = sanitize_for_audit(item)
        return sanitized
    if isinstance(value, list):
        return [sanitize_for_audit(item) for item in value]
    return value


def write_audit_record(
    config: Dict[str, Any],
    *,
    phase: str,
    operation_type: str,
    inputs: Dict[str, Any],
    outcome: Dict[str, Any],
    request_id: Optional[str] = None,
    plan_id: Optional[str] = None,
) -> str:
    audit_path = config["audit_path"]
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    event_id = new_uuid()
    record = {
        "event_id": event_id,
        "timestamp": now_iso(),
        "phase": phase,
        "request_id": request_id,
        "plan_id": plan_id,
        "operation_type": operation_type,
        "inputs": sanitize_for_audit(inputs),
        "outcome": sanitize_for_audit(outcome),
    }
    with audit_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True, separators=(",", ":")) + "\n")
    return event_id


def load_audit_records(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    audit_path = config["audit_path"]
    if not audit_path.exists():
        return []
    records = []
    with audit_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except ValueError:
                continue
    return records


def emit_json(payload: Dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=True, indent=2) + "\n")


def print_error_stderr(message: str) -> None:
    sys.stderr.write(message.rstrip() + "\n")


def render_plan(plan: Dict[str, Any]) -> None:
    lines = [
        "OperationPlan",
        "  type: %s" % plan.get("type"),
        "  plan_id: %s" % plan.get("plan_id"),
        "  request_id: %s" % plan.get("request_id"),
        "  endpoint: %s" % plan.get("resolved", {}).get("endpoint"),
    ]
    final_path = plan.get("resolved", {}).get("final_path")
    if final_path:
        lines.append("  final_path: %s" % final_path)
    entry_type = plan.get("resolved", {}).get("entry_type")
    if entry_type:
        lines.append("  entry_type: %s" % entry_type)
    if plan.get("resolved", {}).get("noop"):
        lines.append("  result: no-op")
    lines.append("  prechecks:")
    for item in plan.get("prechecks", []):
        status = "ok" if item.get("ok") else "fail"
        lines.append("    - [%s] %s: %s" % (status, item.get("name"), item.get("detail", "")))
    if plan.get("conflicts"):
        lines.append("  conflicts:")
        for item in plan["conflicts"]:
            lines.append("    - %s: %s" % (item.get("kind"), item.get("detail")))
    if plan.get("risk", {}).get("notes"):
        lines.append("  notes:")
        for note in plan["risk"]["notes"]:
            lines.append("    - %s" % note)
    lines.append("  next: python skills/openlist/scripts/openlist.py apply --plan-file <plan.json> --json")
    sys.stdout.write("\n".join(lines) + "\n")


def render_result(result: Dict[str, Any]) -> None:
    status = "OK" if result.get("ok") else "ERROR"
    lines = ["[%s] %s" % (status, result.get("message", ""))]
    if result.get("tasks"):
        for task in result["tasks"]:
            lines.append("task: %s %s" % (task.get("task_type"), task.get("tid")))
    if result.get("audit_event_id"):
        lines.append("audit_event_id: %s" % result["audit_event_id"])
    if result.get("rollback_hint"):
        lines.append("rollback: %s" % result["rollback_hint"])
    for hint in result.get("hints", []):
        lines.append("hint: %s" % hint)
    sys.stdout.write("\n".join(lines) + "\n")


def extract_openlist_data_list(data: Any) -> List[Dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict) and isinstance(data.get("content"), list):
        return [item for item in data["content"] if isinstance(item, dict)]
    return []


def extract_openlist_tasks(data: Any, task_type: str) -> List[Dict[str, Any]]:
    if not isinstance(data, dict):
        return []
    task_items = data.get("tasks")
    if not isinstance(task_items, list):
        return []
    tasks = []
    for item in task_items:
        if not isinstance(item, dict):
            continue
        tid = item.get("id") or item.get("tid")
        if tid:
            tasks.append({"task_type": task_type, "tid": str(tid)})
    return tasks


def scan_for_dangerous_signals(value: Any, prefix: str = "") -> List[str]:
    findings = []
    if isinstance(value, dict):
        for key, item in value.items():
            path = ("%s.%s" % (prefix, key)).strip(".")
            lowered_key = str(key).lower()
            if lowered_key == "overwrite" and bool(item):
                findings.append("%s must remain false" % path)
            if lowered_key == "endpoint" and isinstance(item, str) and item not in ALLOWED_ENDPOINTS:
                findings.append("%s is not in the endpoint allowlist" % path)
            if lowered_key in {"delete", "remove", "force"} and bool(item):
                findings.append("%s is not allowed" % path)
            findings.extend(scan_for_dangerous_signals(item, path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            findings.extend(scan_for_dangerous_signals(item, "%s[%d]" % (prefix, index)))
    return findings


def validate_plan_schema(plan: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(plan, dict):
        raise UserFacingError("Plan file must contain a JSON object.")
    required = ["plan_id", "request_id", "created_at", "type", "api", "prechecks", "conflicts", "risk", "resolved"]
    missing = [field for field in required if field not in plan]
    if missing:
        raise UserFacingError("Plan file is missing required fields: %s." % ", ".join(missing))
    plan_type = plan.get("type")
    if plan_type not in ALLOWED_PLAN_TYPES:
        raise UserFacingError("Unsupported plan type: %s." % plan_type)
    api = plan.get("api") or {}
    if not isinstance(api, dict) or api.get("base_url") != config.get("base_url"):
        raise UserFacingError(
            "Plan base_url does not match the current OPENLIST_BASE_URL.",
            hints=["Re-run the preview command against the same OpenList instance and use the new plan file."],
        )
    resolved = plan.get("resolved")
    if not isinstance(resolved, dict):
        raise UserFacingError("Plan resolved section must be an object.")
    endpoint = resolved.get("endpoint")
    if endpoint not in ALLOWED_ENDPOINTS:
        raise UserFacingError("Plan endpoint is not allowed: %s." % endpoint)
    if endpoint != PLAN_ENDPOINTS.get(plan_type):
        raise UserFacingError("Plan endpoint does not match the plan type: %s." % endpoint)
    findings = scan_for_dangerous_signals(plan)
    if findings:
        raise UserFacingError(
            "Plan validation failed because it contains unsafe fields.",
            data={"findings": findings},
            hints=["Generate a fresh preview plan instead of editing the plan file by hand."],
        )
    prechecks = plan.get("prechecks") or []
    if any(not item.get("ok") for item in prechecks if isinstance(item, dict)):
        raise UserFacingError(
            "Plan prechecks did not pass, so apply was denied.",
            data={"prechecks": prechecks},
        )
    if plan.get("conflicts"):
        raise UserFacingError(
            "Plan still contains unresolved conflicts, so apply was denied.",
            data={"conflicts": plan.get("conflicts")},
            hints=["Resolve conflicts in preview by changing the conflict policy or adjusting the target."],
        )
    body = resolved.get("body")
    if not isinstance(body, dict):
        raise UserFacingError("Plan resolved.body must be an object.")
    if body.get("overwrite") not in {None, False}:
        raise UserFacingError("Plan overwrite must remain false.")
    request = plan.get("request")
    if isinstance(request, dict) and request.get("type") not in {None, plan_type}:
        raise UserFacingError("Plan request.type does not match the plan type.")
    if plan_type == "fs_remove":
        validate_delete_plan(plan)
    return plan


def load_plan_file(path_value: str) -> Dict[str, Any]:
    plan_path = Path(path_value).expanduser()
    if not plan_path.exists():
        raise UserFacingError("Plan file does not exist: %s." % plan_path)
    try:
        return json.loads(plan_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise UserFacingError("Plan file is not valid JSON: %s." % exc)


def make_request_payload(operation_type: str, **kwargs: Any) -> Dict[str, Any]:
    payload = {
        "request_id": new_uuid(),
        "requested_at": now_iso(),
        "actor": getpass.getuser() or "codex",
        "type": operation_type,
    }
    payload.update(kwargs)
    return payload


def make_precheck(name: str, ok: bool, detail: str) -> Dict[str, Any]:
    return {"name": name, "ok": bool(ok), "detail": detail}


def make_plan(
    config: Dict[str, Any],
    request_payload: Dict[str, Any],
    *,
    endpoint: str,
    body: Dict[str, Any],
    prechecks: List[Dict[str, Any]],
    conflicts: List[Dict[str, Any]],
    notes: List[str],
    resolved_extras: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    plan = {
        "plan_id": new_uuid(),
        "request_id": request_payload["request_id"],
        "created_at": now_iso(),
        "expires_at": (datetime.now(timezone.utc).astimezone() + timedelta(hours=1)).isoformat(),
        "type": request_payload["type"],
        "api": {"base_url": config["base_url"]},
        "request": request_payload,
        "prechecks": prechecks,
        "conflicts": conflicts,
        "risk": {"level": "low" if not conflicts else "medium", "notes": notes},
        "resolved": {
            "endpoint": endpoint,
            "body": body,
            "noop": False,
        },
    }
    if resolved_extras:
        plan["resolved"].update(resolved_extras)
    return plan


class OpenListClient(object):
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    def _ssl_context(self) -> Optional[ssl.SSLContext]:
        if self.config.get("verify_tls", True):
            return None
        return ssl._create_unverified_context()  # type: ignore[attr-defined]

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = join_base_url(self.config["base_url"], endpoint, params=params)
        data = None
        headers = {"Accept": "application/json"}
        token = self.config.get("token")
        if token:
            headers["Authorization"] = token
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib_request.Request(url, data=data, headers=headers, method=method.upper())
        response_bytes = b""
        status = 0
        try:
            with urllib_request.urlopen(
                request,
                timeout=self.config["timeout_seconds"],
                context=self._ssl_context(),
            ) as response:
                status = getattr(response, "status", response.getcode())
                response_bytes = response.read()
        except urllib_error.HTTPError as exc:
            status = exc.code
            response_bytes = exc.read()
        except urllib_error.URLError as exc:
            raise UserFacingError(
                "Failed to reach OpenList: %s." % exc.reason,
                hints=["Check OPENLIST_BASE_URL, network access, and TLS settings."],
            )
        except Exception as exc:  # pragma: no cover
            raise UserFacingError("Unexpected HTTP failure: %s." % exc)

        text = response_bytes.decode("utf-8", "replace").strip()
        parsed = None
        if text:
            try:
                parsed = json.loads(text)
            except ValueError:
                parsed = None
        if isinstance(parsed, dict) and "code" in parsed:
            openlist_code = parsed.get("code")
            data_payload = parsed.get("data")
            message = str(parsed.get("message") or ("success" if openlist_code == 200 else "OpenList request failed"))
            return {
                "ok": openlist_code == 200,
                "message": message,
                "openlist_code": openlist_code,
                "data": data_payload,
                "http_status": status,
            }
        return {
            "ok": 200 <= status < 300,
            "message": text or ("HTTP %s" % status),
            "openlist_code": status if endpoint.endswith("/ping") else None,
            "data": parsed if parsed is not None else {"raw": text},
            "http_status": status,
        }


def read_path_info(client: OpenListClient, path_value: str) -> Dict[str, Any]:
    return client.request("POST", "/api/fs/get", body={"path": path_value})


def read_dir_listing(client: OpenListClient, path_value: str, refresh: bool = False) -> Dict[str, Any]:
    return client.request("POST", "/api/fs/list", body={"path": path_value, "refresh": bool(refresh)})


def list_entry_names(result: Dict[str, Any]) -> List[str]:
    return [item.get("name") for item in extract_openlist_data_list(result.get("data")) if item.get("name")]


def detect_entry_type(data: Any) -> str:
    if not isinstance(data, dict):
        return "unknown"
    if data.get("is_dir") is True:
        return "dir"
    if data.get("is_dir") is False:
        return "file"
    return "unknown"


def validate_delete_plan(plan: Dict[str, Any]) -> None:
    request = plan.get("request") or {}
    resolved = plan.get("resolved") or {}
    body = resolved.get("body")
    if not isinstance(body, dict):
        raise UserFacingError("Delete plan resolved.body must be an object.")
    dir_path = normalize_openlist_path(body.get("dir"))
    names = body.get("names")
    if not isinstance(names, list) or len(names) != 1:
        raise UserFacingError("Delete plans must target exactly one path.")
    if not isinstance(names[0], str):
        raise UserFacingError("Delete plan entry name must be a string.")
    entry_name = validate_new_name(names[0])
    source_path = normalize_openlist_path(resolved.get("source_path"), allow_root=False)
    final_path = normalize_openlist_path(resolved.get("final_path"), allow_root=False)
    expected_path = posixpath.join(dir_path, entry_name)
    if source_path != expected_path or final_path != source_path:
        raise UserFacingError("Delete plan path fields do not match the resolved request.")
    if request.get("path") != source_path:
        raise UserFacingError("Delete plan request.path must match the resolved source path.")
    if resolved.get("entry_type") not in {"file", "dir"}:
        raise UserFacingError("Delete plan entry_type must remain 'file' or 'dir'.")
    if (plan.get("risk") or {}).get("level") != "high":
        raise UserFacingError("Delete plans must keep risk level 'high'.")


def build_move_preview(
    client: OpenListClient,
    config: Dict[str, Any],
    src_path: str,
    dst_dir: str,
    conflict_policy: str,
) -> Dict[str, Any]:
    if conflict_policy not in ALLOWED_CONFLICT_POLICIES:
        raise UserFacingError("Unsupported conflict policy for move: %s." % conflict_policy)
    normalized_src = normalize_openlist_path(src_path, allow_root=False)
    normalized_dst = normalize_openlist_path(dst_dir)
    src_dir, src_name = split_dir_and_name(normalized_src)
    request_payload = make_request_payload(
        "fs_move",
        src_path=normalized_src,
        dst_dir=normalized_dst,
        conflict_policy=conflict_policy,
    )
    notes = [
        "不会覆盖写入；需要用户确认后才执行。",
        "目标存在冲突时默认拒绝，除非显式选择 skip 或 auto_rename。",
    ]
    source_info = read_path_info(client, normalized_src)
    prechecks = [make_precheck("source_exists", source_info["ok"], source_info["message"])]
    dest_info = read_path_info(client, normalized_dst)
    dest_is_dir = bool(dest_info["ok"] and isinstance(dest_info.get("data"), dict) and dest_info["data"].get("is_dir"))
    prechecks.append(make_precheck("dst_dir_exists", dest_is_dir, dest_info["message"]))
    conflicts = []
    noop = False
    skip_existing = False
    rename_before_move = None
    effective_name = src_name

    if source_info["ok"] and dest_is_dir:
        target_path = posixpath.join(normalized_dst, src_name)
        if target_path == normalized_src:
            noop = True
            notes.append("源路径已经位于目标目录，无需执行变更。")
        else:
            listing = read_dir_listing(client, normalized_dst)
            if listing["ok"]:
                existing_names = list_entry_names(listing)
                if src_name in existing_names:
                    if conflict_policy == "fail":
                        conflicts.append(
                            {
                                "kind": "name_conflict",
                                "path": target_path,
                                "detail": "Destination already contains '%s'." % src_name,
                            }
                        )
                    elif conflict_policy == "skip":
                        skip_existing = True
                        notes.append("目标目录已存在同名项，执行时会跳过该条目。")
                    elif conflict_policy == "auto_rename":
                        candidate_pool = list(existing_names)
                        if src_dir != normalized_dst:
                            source_listing = read_dir_listing(client, src_dir)
                            if source_listing["ok"]:
                                candidate_pool.extend(list_entry_names(source_listing))
                        effective_name = generate_auto_name(candidate_pool, src_name)
                        rename_before_move = {
                            "endpoint": "/api/fs/rename",
                            "body": {"path": normalized_src, "name": effective_name, "overwrite": False},
                        }
                        notes.append(
                            "目标目录存在同名项，将先在源目录中重命名为 '%s' 后再移动。" % effective_name
                        )
            else:
                prechecks.append(make_precheck("dst_listing", False, listing["message"]))

    body = {
        "src_dir": src_dir,
        "dst_dir": normalized_dst,
        "names": [effective_name if rename_before_move else src_name],
        "overwrite": False,
        "skip_existing": skip_existing,
    }
    final_path = posixpath.join(normalized_dst, effective_name)
    rollback_hint = (
        "如需回退，可对 '%s' 执行 preview-move 回到 '%s'，或在目标目录中执行 preview-rename 改回原名。"
        % (final_path, src_dir)
    )
    resolved_extras = {
        "source_path": normalized_src,
        "final_path": final_path,
        "rollback_hint": rollback_hint,
    }
    if rename_before_move:
        resolved_extras["rename_before_move"] = rename_before_move
    plan = make_plan(
        config,
        request_payload,
        endpoint="/api/fs/move",
        body=body,
        prechecks=prechecks,
        conflicts=conflicts,
        notes=notes,
        resolved_extras=resolved_extras,
    )
    if noop:
        plan["resolved"]["noop"] = True
        plan["risk"]["notes"].append("apply 会返回 no-op 成功并写入审计。")
    return plan


def build_rename_preview(
    client: OpenListClient,
    config: Dict[str, Any],
    path_value: str,
    new_name: str,
    conflict_policy: str,
) -> Dict[str, Any]:
    if conflict_policy not in ALLOWED_RENAME_CONFLICT_POLICIES:
        raise UserFacingError("Unsupported conflict policy for rename: %s." % conflict_policy)
    normalized_path = normalize_openlist_path(path_value, allow_root=False)
    normalized_name = validate_new_name(new_name)
    parent_dir, current_name = split_dir_and_name(normalized_path)
    request_payload = make_request_payload(
        "fs_rename",
        path=normalized_path,
        new_name=normalized_name,
        conflict_policy=conflict_policy,
    )
    source_info = read_path_info(client, normalized_path)
    prechecks = [make_precheck("source_exists", source_info["ok"], source_info["message"])]
    notes = ["重命名默认不覆盖。"]
    conflicts = []
    noop = normalized_name == current_name
    final_name = normalized_name
    if noop:
        notes.append("新名称与当前名称一致，无需执行变更。")
    elif source_info["ok"]:
        listing = read_dir_listing(client, parent_dir)
        if listing["ok"]:
            existing_names = [name for name in list_entry_names(listing) if name != current_name]
            if normalized_name in existing_names:
                if conflict_policy == "fail":
                    conflicts.append(
                        {
                            "kind": "name_conflict",
                            "path": posixpath.join(parent_dir, normalized_name),
                            "detail": "The directory already contains '%s'." % normalized_name,
                        }
                    )
                else:
                    final_name = generate_auto_name(existing_names, normalized_name)
                    notes.append("目标名称已存在，执行时将自动改名为 '%s'。" % final_name)
        else:
            prechecks.append(make_precheck("parent_listing", False, listing["message"]))
    body = {"path": normalized_path, "name": final_name, "overwrite": False}
    final_path = posixpath.join(parent_dir, final_name)
    rollback_hint = "如需回退，可再次执行 preview-rename 将 '%s' 改回 '%s'。" % (final_name, current_name)
    plan = make_plan(
        config,
        request_payload,
        endpoint="/api/fs/rename",
        body=body,
        prechecks=prechecks,
        conflicts=conflicts,
        notes=notes,
        resolved_extras={"final_path": final_path, "rollback_hint": rollback_hint},
    )
    if noop:
        plan["resolved"]["noop"] = True
    return plan


def build_offline_preview(
    client: OpenListClient,
    config: Dict[str, Any],
    urls: Sequence[str],
    dst_dir: str,
    tool_name: Optional[str],
    delete_policy: str,
) -> Dict[str, Any]:
    filtered_urls = filter_urls(urls)
    if not filtered_urls:
        raise UserFacingError("At least one non-empty --url value is required.")
    if delete_policy not in ALLOWED_DELETE_POLICIES:
        raise UserFacingError("Unsupported delete policy: %s." % delete_policy)
    normalized_dst = normalize_openlist_path(dst_dir)
    request_payload = make_request_payload(
        "offline_create",
        urls=filtered_urls,
        dst_dir=normalized_dst,
        tool=tool_name,
        delete_policy=delete_policy,
    )
    dest_info = read_path_info(client, normalized_dst)
    dest_is_dir = bool(dest_info["ok"] and isinstance(dest_info.get("data"), dict) and dest_info["data"].get("is_dir"))
    prechecks = [make_precheck("dst_dir_exists", dest_is_dir, dest_info["message"])]
    tools_result = client.request("GET", "/api/public/offline_download_tools")
    tool_candidates = [str(item) for item in tools_result.get("data", [])] if isinstance(tools_result.get("data"), list) else []
    selected_tool = tool_name or choose_offline_tool(tool_candidates)
    if not selected_tool:
        prechecks.append(make_precheck("tool_available", False, "No offline download tool is enabled."))
    else:
        prechecks.append(make_precheck("tool_available", True, "Selected tool: %s." % selected_tool))
    notes = [
        "空 URL 已被过滤。",
        "默认 delete_policy 为 delete_never。",
        "创建后可使用 task-info 或 task-list 查询离线任务状态。",
    ]
    plan = make_plan(
        config,
        request_payload,
        endpoint="/api/fs/add_offline_download",
        body={
            "urls": filtered_urls,
            "path": normalized_dst,
            "tool": selected_tool,
            "delete_policy": delete_policy,
        },
        prechecks=prechecks,
        conflicts=[],
        notes=notes,
        resolved_extras={
            "final_path": normalized_dst,
            "rollback_hint": "如实例支持，可对返回的 offline_download 任务执行 task-cancel。",
        },
    )
    return plan


def build_delete_preview(
    client: OpenListClient,
    config: Dict[str, Any],
    path_value: str,
) -> Dict[str, Any]:
    normalized_path = normalize_openlist_path(path_value, allow_root=False)
    parent_dir, entry_name = split_dir_and_name(normalized_path)
    request_payload = make_request_payload("fs_remove", path=normalized_path)
    source_info = read_path_info(client, normalized_path)
    entry_type = detect_entry_type(source_info.get("data"))
    prechecks = [make_precheck("source_exists", source_info["ok"], source_info["message"])]
    notes = [
        "删除是不可逆操作；执行前必须重新获得用户明确确认。",
        "apply 前必须向用户展示规范化后的精确路径和对象类型。",
        "删除仅支持单个显式路径，不支持根目录或批量路径。",
    ]
    plan = make_plan(
        config,
        request_payload,
        endpoint="/api/fs/remove",
        body={"dir": parent_dir, "names": [entry_name]},
        prechecks=prechecks,
        conflicts=[],
        notes=notes,
        resolved_extras={
            "source_path": normalized_path,
            "final_path": normalized_path,
            "entry_type": entry_type,
        },
    )
    plan["risk"]["level"] = "high"
    return plan


def audit_preview(config: Dict[str, Any], plan: Dict[str, Any]) -> str:
    return write_audit_record(
        config,
        phase="preview",
        operation_type=plan["type"],
        inputs=plan.get("request", {}),
        outcome={
            "status": "preview_ready",
            "conflicts": plan.get("conflicts"),
            "prechecks": plan.get("prechecks"),
            "final_path": plan.get("resolved", {}).get("final_path"),
        },
        request_id=plan.get("request_id"),
        plan_id=plan.get("plan_id"),
    )


def execute_plan(client: OpenListClient, config: Dict[str, Any], plan: Dict[str, Any]) -> Dict[str, Any]:
    validated = validate_plan_schema(plan, config)
    resolved = validated["resolved"]
    rollback_hint = resolved.get("rollback_hint")
    if resolved.get("noop"):
        result = make_result(
            True,
            "No change was required.",
            data={"plan_id": validated["plan_id"], "noop": True},
            rollback_hint=rollback_hint,
        )
        result["audit_event_id"] = write_audit_record(
            config,
            phase="apply",
            operation_type=validated["type"],
            inputs=validated.get("request", {}),
            outcome=result,
            request_id=validated["request_id"],
            plan_id=validated["plan_id"],
        )
        return result

    plan_type = validated["type"]
    if plan_type == "fs_move":
        rename_before_move = resolved.get("rename_before_move")
        if rename_before_move:
            rename_result = client.request(
                "POST",
                rename_before_move["endpoint"],
                body=rename_before_move["body"],
            )
            if not rename_result["ok"]:
                hints = make_hints(rename_result["message"], plan_type)
                result = make_result(
                    False,
                    "Pre-move rename failed: %s" % rename_result["message"],
                    openlist_code=rename_result.get("openlist_code"),
                    data=rename_result.get("data"),
                    hints=hints,
                )
                result["audit_event_id"] = write_audit_record(
                    config,
                    phase="apply",
                    operation_type=plan_type,
                    inputs=validated.get("request", {}),
                    outcome=result,
                    request_id=validated["request_id"],
                    plan_id=validated["plan_id"],
                )
                return result
        response = client.request("POST", resolved["endpoint"], body=resolved["body"])
        tasks = extract_openlist_tasks(response.get("data"), "move")
        result = make_result(
            response["ok"],
            response["message"],
            openlist_code=response.get("openlist_code"),
            data=response.get("data"),
            tasks=tasks,
            hints=make_hints(response["message"], plan_type),
            rollback_hint=rollback_hint,
        )
    elif plan_type == "fs_rename":
        response = client.request("POST", resolved["endpoint"], body=resolved["body"])
        result = make_result(
            response["ok"],
            response["message"],
            openlist_code=response.get("openlist_code"),
            data=response.get("data"),
            hints=make_hints(response["message"], plan_type),
            rollback_hint=rollback_hint,
        )
    elif plan_type == "fs_remove":
        source_path = resolved["source_path"]
        expected_entry_type = resolved["entry_type"]
        current_info = read_path_info(client, source_path)
        current_entry_type = detect_entry_type(current_info.get("data"))
        if not current_info["ok"]:
            result = make_result(
                False,
                "Delete target no longer exists, so apply was denied.",
                data={
                    "source_path": source_path,
                    "expected_entry_type": expected_entry_type,
                    "actual_entry_type": "missing",
                },
                hints=["Run preview-delete again and confirm the updated path before retrying."],
            )
            result["audit_event_id"] = write_audit_record(
                config,
                phase="apply",
                operation_type=plan_type,
                inputs=validated.get("request", {}),
                outcome=result,
                request_id=validated["request_id"],
                plan_id=validated["plan_id"],
            )
            return result
        if current_entry_type != expected_entry_type:
            result = make_result(
                False,
                "Delete target type changed since preview, so apply was denied.",
                data={
                    "source_path": source_path,
                    "expected_entry_type": expected_entry_type,
                    "actual_entry_type": current_entry_type,
                },
                hints=["Run preview-delete again and confirm the updated target before retrying."],
            )
            result["audit_event_id"] = write_audit_record(
                config,
                phase="apply",
                operation_type=plan_type,
                inputs=validated.get("request", {}),
                outcome=result,
                request_id=validated["request_id"],
                plan_id=validated["plan_id"],
            )
            return result
        response = client.request("POST", resolved["endpoint"], body=resolved["body"])
        result = make_result(
            response["ok"],
            response["message"],
            openlist_code=response.get("openlist_code"),
            data=response.get("data"),
            hints=make_hints(response["message"], plan_type),
        )
    elif plan_type == "offline_create":
        response = client.request("POST", resolved["endpoint"], body=resolved["body"])
        tasks = extract_openlist_tasks(response.get("data"), "offline_download")
        result = make_result(
            response["ok"],
            response["message"],
            openlist_code=response.get("openlist_code"),
            data=response.get("data"),
            tasks=tasks,
            hints=make_hints(response["message"], plan_type),
            rollback_hint=rollback_hint,
        )
    else:  # pragma: no cover
        raise UserFacingError("Unsupported plan type: %s." % plan_type)

    result["audit_event_id"] = write_audit_record(
        config,
        phase="apply",
        operation_type=validated["type"],
        inputs=validated.get("request", {}),
        outcome=result,
        request_id=validated["request_id"],
        plan_id=validated["plan_id"],
    )
    return result


def deny_plan(config: Dict[str, Any], plan: Dict[str, Any], error: UserFacingError) -> Dict[str, Any]:
    result = make_result(
        False,
        error.message,
        openlist_code=error.openlist_code,
        data=error.data,
        hints=error.hints,
    )
    result["audit_event_id"] = write_audit_record(
        config,
        phase="deny",
        operation_type=plan.get("type", "unknown"),
        inputs=plan.get("request", {}),
        outcome=result,
        request_id=plan.get("request_id"),
        plan_id=plan.get("plan_id"),
    )
    return result


def handle_read_only(
    config: Dict[str, Any],
    operation_type: str,
    response: Dict[str, Any],
    *,
    inputs: Dict[str, Any],
    task_type: Optional[str] = None,
) -> Dict[str, Any]:
    tasks = extract_openlist_tasks(response.get("data"), task_type or operation_type)
    result = make_result(
        response["ok"],
        response["message"],
        openlist_code=response.get("openlist_code"),
        data=response.get("data"),
        tasks=tasks,
        hints=make_hints(response["message"], operation_type),
    )
    result["audit_event_id"] = write_audit_record(
        config,
        phase="command",
        operation_type=operation_type,
        inputs=inputs,
        outcome=result,
        request_id=new_uuid(),
        plan_id=None,
    )
    return result


def filter_audit_records(
    records: Sequence[Dict[str, Any]],
    *,
    event_id: Optional[str] = None,
    plan_id: Optional[str] = None,
    tid: Optional[str] = None,
) -> List[Dict[str, Any]]:
    matches = []
    for record in records:
        if event_id and record.get("event_id") != event_id:
            continue
        if plan_id and record.get("plan_id") != plan_id:
            continue
        if tid:
            outcome = record.get("outcome") or {}
            tasks = outcome.get("tasks") or []
            has_tid = any(isinstance(item, dict) and str(item.get("tid")) == tid for item in tasks)
            if not has_tid:
                continue
        matches.append(record)
    return matches


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OpenList automation CLI")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("ping", help="Check OpenList connectivity")
    subparsers.add_parser("whoami", help="Return the current user")

    fs_get = subparsers.add_parser("fs-get", help="Get a file or directory")
    fs_get.add_argument("--path", required=True)

    fs_list = subparsers.add_parser("fs-list", help="List a directory")
    fs_list.add_argument("--path", required=True)
    fs_list.add_argument("--refresh", action="store_true")

    subparsers.add_parser("offline-tools", help="List offline download tools")

    task_info = subparsers.add_parser("task-info", help="Get task info")
    task_info.add_argument("--task-type", required=True, choices=sorted(TASK_TYPES))
    task_info.add_argument("--tid", required=True)

    task_list = subparsers.add_parser("task-list", help="List tasks")
    task_list.add_argument("--task-type", required=True, choices=sorted(TASK_TYPES))
    task_list.add_argument("--state", default="undone", choices=["undone", "done"])

    task_cancel = subparsers.add_parser("task-cancel", help="Cancel a task")
    task_cancel.add_argument("--task-type", required=True, choices=sorted(TASK_TYPES))
    task_cancel.add_argument("--tid", required=True)

    preview_move = subparsers.add_parser("preview-move", help="Preview a move")
    preview_move.add_argument("--src-path", required=True)
    preview_move.add_argument("--dst-dir", required=True)
    preview_move.add_argument("--conflict-policy", default=DEFAULT_CONFLICT_POLICY, choices=sorted(ALLOWED_CONFLICT_POLICIES))

    preview_rename = subparsers.add_parser("preview-rename", help="Preview a rename")
    preview_rename.add_argument("--path", required=True)
    preview_rename.add_argument("--new-name", required=True)
    preview_rename.add_argument("--conflict-policy", default=DEFAULT_CONFLICT_POLICY, choices=sorted(ALLOWED_RENAME_CONFLICT_POLICIES))

    preview_delete = subparsers.add_parser("preview-delete", help="Preview a delete")
    preview_delete.add_argument("--path", required=True)

    preview_offline = subparsers.add_parser("preview-offline-create", help="Preview an offline task")
    preview_offline.add_argument("--url", action="append", required=True)
    preview_offline.add_argument("--dst-dir", required=True)
    preview_offline.add_argument("--tool")
    preview_offline.add_argument("--delete-policy", default=DEFAULT_DELETE_POLICY, choices=sorted(ALLOWED_DELETE_POLICIES))

    apply_cmd = subparsers.add_parser("apply", help="Execute an OperationPlan")
    apply_cmd.add_argument("--plan-file", required=True)

    audit_show = subparsers.add_parser("audit-show", help="Query audit records")
    audit_show.add_argument("--event-id")
    audit_show.add_argument("--plan-id")
    audit_show.add_argument("--tid")

    return parser


def command_result(args: argparse.Namespace) -> Dict[str, Any]:
    if args.command == "audit-show":
        config = load_config(require_auth=False)
        records = filter_audit_records(
            load_audit_records(config),
            event_id=args.event_id,
            plan_id=args.plan_id,
            tid=args.tid,
        )
        return make_result(True, "Found %d audit record(s)." % len(records), data={"records": records})

    config = load_config(require_auth=True)
    client = OpenListClient(config)

    if args.command == "ping":
        return handle_read_only(config, "ping", client.request("GET", "/ping"), inputs={"command": "ping"})
    if args.command == "whoami":
        return handle_read_only(config, "whoami", client.request("GET", "/api/me"), inputs={"command": "whoami"})
    if args.command == "fs-get":
        path_value = normalize_openlist_path(args.path)
        response = client.request("POST", "/api/fs/get", body={"path": path_value})
        return handle_read_only(config, "fs_get", response, inputs={"path": path_value})
    if args.command == "fs-list":
        path_value = normalize_openlist_path(args.path)
        response = client.request("POST", "/api/fs/list", body={"path": path_value, "refresh": bool(args.refresh)})
        return handle_read_only(config, "fs_list", response, inputs={"path": path_value, "refresh": bool(args.refresh)})
    if args.command == "offline-tools":
        return handle_read_only(
            config,
            "offline_tools",
            client.request("GET", "/api/public/offline_download_tools"),
            inputs={"command": "offline-tools"},
        )
    if args.command == "task-info":
        endpoint = TASK_TYPES[args.task_type] + "/info"
        response = client.request("POST", endpoint, params={"tid": args.tid})
        return handle_read_only(
            config,
            "task_info",
            response,
            inputs={"task_type": args.task_type, "tid": args.tid},
            task_type=args.task_type,
        )
    if args.command == "task-list":
        endpoint = TASK_TYPES[args.task_type] + "/" + args.state
        response = client.request("GET", endpoint)
        return handle_read_only(
            config,
            "task_list",
            response,
            inputs={"task_type": args.task_type, "state": args.state},
            task_type=args.task_type,
        )
    if args.command == "task-cancel":
        endpoint = TASK_TYPES[args.task_type] + "/cancel"
        response = client.request("POST", endpoint, params={"tid": args.tid})
        result = handle_read_only(
            config,
            "task_cancel",
            response,
            inputs={"task_type": args.task_type, "tid": args.tid},
            task_type=args.task_type,
        )
        if not result["ok"] and not result.get("hints"):
            result["hints"] = ["If cancellation is not supported on this instance, keep monitoring the task with task-info."]
        return result
    if args.command == "preview-move":
        plan = build_move_preview(client, config, args.src_path, args.dst_dir, args.conflict_policy)
        plan["audit_event_id"] = audit_preview(config, plan)
        return plan
    if args.command == "preview-rename":
        plan = build_rename_preview(client, config, args.path, args.new_name, args.conflict_policy)
        plan["audit_event_id"] = audit_preview(config, plan)
        return plan
    if args.command == "preview-delete":
        plan = build_delete_preview(client, config, args.path)
        plan["audit_event_id"] = audit_preview(config, plan)
        return plan
    if args.command == "preview-offline-create":
        plan = build_offline_preview(client, config, args.url, args.dst_dir, args.tool, args.delete_policy)
        plan["audit_event_id"] = audit_preview(config, plan)
        return plan
    if args.command == "apply":
        plan = load_plan_file(args.plan_file)
        try:
            return execute_plan(client, config, plan)
        except UserFacingError as exc:
            return deny_plan(config, plan, exc)
    raise UserFacingError("Unknown command.")


def main(argv: Optional[Sequence[str]] = None) -> int:
    raw_args = list(sys.argv[1:] if argv is None else argv)
    json_requested = False
    filtered_args = []
    for item in raw_args:
        if item == "--json":
            json_requested = True
        else:
            filtered_args.append(item)
    parser = build_parser()
    args = parser.parse_args(filtered_args)
    args.json = json_requested or getattr(args, "json", False)
    if not args.command:
        parser.print_help()
        return 0
    try:
        result = command_result(args)
    except UserFacingError as exc:
        payload = make_result(
            False,
            exc.message,
            openlist_code=exc.openlist_code,
            data=exc.data,
            hints=exc.hints,
        )
        if getattr(args, "json", False):
            emit_json(payload)
            print_error_stderr(exc.stderr)
        else:
            render_result(payload)
        return 1
    if getattr(args, "json", False):
        emit_json(result)
    else:
        if isinstance(result, dict) and "resolved" in result and "plan_id" in result:
            render_plan(result)
        else:
            render_result(result)
    return 0 if not isinstance(result, dict) or result.get("ok", True) else 1


if __name__ == "__main__":
    sys.exit(main())
