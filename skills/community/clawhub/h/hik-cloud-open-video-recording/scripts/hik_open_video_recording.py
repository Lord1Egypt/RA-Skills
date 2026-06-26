#!/usr/bin/env python3
"""Hik-Cloud OpenAPI video recording helper."""

from __future__ import annotations

import argparse
import ctypes
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TextIO
from urllib import error, parse, request


DEFAULT_BASE_URL = "https://api2.hik-cloud.com"
BASE_URL_ENV_VAR = "HIK_OPEN_BASE_URL"
DEFAULT_TIMEOUT = 20.0
DEFAULT_TOKEN_CACHE = Path.home() / ".cache" / "hik_open" / "token.json"

PROJECT_PATH = "/api/v1/ezviz/record/project"
PROJECT_LIST_PATH = "/api/v1/ezviz/record/projects"
RECORD_VIDEO_PATH = "/api/v1/ezviz/record/video"
RECORD_PREVIEW_PATH = "/api/v1/ezviz/record/video/preview"
RECORD_INSTANT_PATH = "/api/v1/ezviz/record/video/instant"
FRAME_INTERVAL_PATH = "/api/v1/ezviz/record/video/frame/interval"
FRAME_TIMING_PATH = "/api/v1/ezviz/record/video/frame/timing"
FRAME_INSTANT_PATH = "/api/v1/ezviz/record/video/frame/instant"
TASK_STOP_PATH = "/api/v1/ezviz/record/delete/task"
TASK_GET_PATH = "/api/v1/ezviz/record/task"
TASK_LIST_PATH = "/api/v1/ezviz/record/tasks"
FILE_TASK_LIST_PATH = "/api/v1/ezviz/record/query/video/file/list"
FILE_GET_PATH = "/api/v1/ezviz/record/file"
FILE_LIST_PATH = "/api/v1/ezviz/record/files"
FILE_DELETE_PATH = "/api/v1/ezviz/record/file"
FILE_DOWNLOAD_PATH = "/api/v1/ezviz/record/file/download"
FLOW_UPDATE_PATH = "/api/v1/ezviz/record/project/flowLimit"
TENANT_INFO_PATH = "/api/v1/ezviz/record/queryVideoTenantInfo"
UPLOAD_ADDRESS_PATH = "/api/v1/ezviz/cloudrecord/vod/file/upload"
SAVE_FILE_PATH = "/api/v1/ezviz/cloudrecord/vod/file/register"
CLIP_PATH = "/api/v1/ezviz/cloudrecord/video/convert"
CLIP_FILE_QUERY_PATH = "/api/v1/ezviz/cloudrecord/vod/task/files/query"
TOKEN_PATH = "/oauth/token"

UTF8_CODE_PAGE = 65001


class ApiError(RuntimeError):
    """Raised when the remote API or request contract fails."""


@dataclass
class RequestSpec:
    method: str
    path: str
    query: dict[str, Any] | None = None
    json_body: dict[str, Any] | None = None

    def build_url(self, base_url: str) -> str:
        url = base_url.rstrip("/") + self.path
        if self.query:
            url += "?" + parse.urlencode(self.query)
        return url


def _is_tty(stream: TextIO) -> bool:
    isatty = getattr(stream, "isatty", None)
    if not callable(isatty):
        return False
    try:
        return bool(isatty())
    except Exception:
        return False


def _reconfigure_stream(stream: TextIO) -> None:
    reconfigure = getattr(stream, "reconfigure", None)
    if not callable(reconfigure):
        return
    try:
        reconfigure(encoding="utf-8", errors="replace")
    except TypeError:
        reconfigure(encoding="utf-8")
    except ValueError:
        return


def _set_windows_utf8_code_page() -> None:
    try:
        kernel32 = ctypes.windll.kernel32
    except Exception:
        return

    for method_name in ("SetConsoleOutputCP", "SetConsoleCP"):
        method = getattr(kernel32, method_name, None)
        if not callable(method):
            continue
        try:
            method(UTF8_CODE_PAGE)
        except Exception:
            continue


def configure_windows_utf8_output(
    *, stdout: TextIO | None = None, stderr: TextIO | None = None
) -> None:
    if os.name != "nt":
        return

    actual_stdout = sys.stdout if stdout is None else stdout
    actual_stderr = sys.stderr if stderr is None else stderr
    if _is_tty(actual_stdout) or _is_tty(actual_stderr):
        _set_windows_utf8_code_page()

    _reconfigure_stream(actual_stdout)
    _reconfigure_stream(actual_stderr)


def normalize_base_url(base_url: str) -> str:
    normalized = base_url.strip()
    if not normalized:
        raise ApiError("base URL must not be empty")
    return normalized.rstrip("/")


def resolve_base_url(explicit_base_url: str | None) -> str:
    if explicit_base_url:
        return normalize_base_url(explicit_base_url)
    env_base_url = os.getenv(BASE_URL_ENV_VAR)
    if env_base_url:
        return normalize_base_url(env_base_url)
    return DEFAULT_BASE_URL


def load_token_cache(cache_file: Path) -> dict[str, Any] | None:
    if not cache_file.exists():
        return None
    try:
        return json.loads(cache_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def save_token_cache(cache_file: Path, payload: dict[str, Any]) -> None:
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def token_still_valid(cache_payload: dict[str, Any]) -> bool:
    token = cache_payload.get("access_token")
    expires_at = cache_payload.get("expires_at")
    if not token or not isinstance(expires_at, (int, float)):
        return False
    return time.time() < float(expires_at) - 60


def http_json_request(
    method: str,
    url: str,
    headers: dict[str, str] | None,
    timeout: float,
    json_body: dict[str, Any] | None = None,
    form_body: dict[str, Any] | None = None,
) -> tuple[int, Any]:
    if json_body is not None and form_body is not None:
        raise ValueError("json_body and form_body are mutually exclusive")

    data = None
    final_headers = dict(headers or {})
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        final_headers.setdefault("Content-Type", "application/json")
    elif form_body is not None:
        data = parse.urlencode(form_body).encode("utf-8")
        final_headers.setdefault("Content-Type", "application/x-www-form-urlencoded")

    req = request.Request(url=url, data=data, headers=final_headers, method=method)
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw else {}
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            body = {"raw": raw}
        return exc.code, body
    except error.URLError as exc:
        raise ApiError(f"request failed: {exc}") from exc


def summarize_error_payload(payload: Any) -> tuple[Any, Any]:
    if not isinstance(payload, dict):
        return None, None
    return payload.get("code"), payload.get("message")


def fetch_access_token(
    base_url: str,
    client_id: str,
    client_secret: str,
    timeout: float,
) -> dict[str, Any]:
    status, payload = http_json_request(
        method="POST",
        url=base_url.rstrip("/") + TOKEN_PATH,
        headers=None,
        timeout=timeout,
        form_body={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "scope": "app",
        },
    )
    if status != 200 or "access_token" not in payload:
        error_code, error_message = summarize_error_payload(payload)
        raise ApiError(
            "failed to fetch access token: "
            f"http={status}, code={error_code}, message={error_message}"
        )
    expires_in = int(payload.get("expires_in", 0))
    return {
        "access_token": payload["access_token"],
        "expires_in": expires_in,
        "expires_at": time.time() + max(expires_in, 0),
        "token_type": payload.get("token_type", "bearer"),
    }


def resolve_access_token(
    base_url: str,
    timeout: float,
    cache_file: Path,
    explicit_token: str | None,
) -> tuple[str, bool]:
    if explicit_token:
        return explicit_token, False

    env_token = os.getenv("HIK_OPEN_ACCESS_TOKEN")
    if env_token:
        return env_token, False

    cache_payload = load_token_cache(cache_file)
    if cache_payload and token_still_valid(cache_payload):
        return str(cache_payload["access_token"]), False

    client_id = os.getenv("HIK_OPEN_CLIENT_ID")
    client_secret = os.getenv("HIK_OPEN_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise ApiError(
            "missing credentials: set HIK_OPEN_CLIENT_ID and HIK_OPEN_CLIENT_SECRET, "
            "or pass --access-token"
        )

    token_payload = fetch_access_token(base_url, client_id, client_secret, timeout)
    save_token_cache(cache_file, token_payload)
    return str(token_payload["access_token"]), True


def api_request(
    base_url: str,
    timeout: float,
    cache_file: Path,
    explicit_token: str | None,
    spec: RequestSpec,
    force_refresh: bool = False,
) -> dict[str, Any]:
    if force_refresh and cache_file.exists():
        cache_file.unlink()

    token, refreshed = resolve_access_token(base_url, timeout, cache_file, explicit_token)
    headers = {"Authorization": f"Bearer {token}"}
    status, payload = http_json_request(
        method=spec.method,
        url=spec.build_url(base_url),
        headers=headers,
        timeout=timeout,
        json_body=spec.json_body,
    )
    if status == 401 and explicit_token is None and not refreshed:
        token, _ = resolve_access_token(base_url, timeout, cache_file, None)
        headers["Authorization"] = f"Bearer {token}"
        status, payload = http_json_request(
            method=spec.method,
            url=spec.build_url(base_url),
            headers=headers,
            timeout=timeout,
            json_body=spec.json_body,
        )
    if status >= 400:
        error_code, error_message = summarize_error_payload(payload)
        raise ApiError(
            f"request failed: http={status}, code={error_code}, message={error_message}"
        )
    return payload


def format_text_output(command: str, payload: dict[str, Any]) -> str:
    lines = [f"command: {command}"]
    if "code" in payload:
        lines.append(f"code: {payload['code']}")
    if "message" in payload:
        lines.append(f"message: {payload['message']}")
    data = payload.get("data")
    if isinstance(data, dict):
        for key in sorted(data):
            lines.append(f"{key}: {data[key]}")
    elif data is not None:
        lines.append(f"data: {data}")
    return "\n".join(lines)


def dump_output(command: str, payload: dict[str, Any], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps({"command": command, "result": payload}, ensure_ascii=False, indent=2))
        return
    print(format_text_output(command, payload))


def _add_optional(body: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        body[key] = value


def build_project_create_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="POST",
        path=PROJECT_PATH,
        json_body={
            "projectName": args.project_name,
            "expireDays": args.expire_days,
            "flowLimit": args.flow_limit,
        },
    )


def build_project_get_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="GET",
        path=PROJECT_PATH,
        query={"projectId": args.project_id},
    )


def build_project_update_spec(args: argparse.Namespace) -> RequestSpec:
    body: dict[str, Any] = {
        "projectId": args.project_id,
        "projectName": args.project_name,
    }
    _add_optional(body, "expireDays", args.expire_days)
    return RequestSpec(method="PUT", path=PROJECT_PATH, json_body=body)


def build_project_delete_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(method="DELETE", path=PROJECT_PATH, query={"projectId": args.project_id})


def build_project_list_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="GET",
        path=PROJECT_LIST_PATH,
        query={"pageNo": args.page_no, "pageSize": args.page_size},
    )


def _build_record_body(args: argparse.Namespace) -> dict[str, Any]:
    body: dict[str, Any] = {
        "projectId": args.project_id,
        "channelNo": args.channel_no,
        "deviceSerial": args.device_serial,
    }
    _add_optional(body, "validateCode", getattr(args, "validate_code", None))
    _add_optional(body, "streamType", getattr(args, "stream_type", None))
    _add_optional(body, "devProto", getattr(args, "dev_proto", None))
    return body


def build_record_replay_spec(args: argparse.Namespace) -> RequestSpec:
    body = _build_record_body(args)
    _add_optional(body, "fileId", args.file_id)
    body["startTime"] = args.start_time
    body["endTime"] = args.end_time
    body["recType"] = args.rec_type
    return RequestSpec(method="POST", path=RECORD_VIDEO_PATH, json_body=body)


def build_record_preview_spec(args: argparse.Namespace) -> RequestSpec:
    body = _build_record_body(args)
    body["startTime"] = args.start_time
    body["endTime"] = args.end_time
    _add_optional(body, "sliceDuration", args.slice_duration)
    return RequestSpec(method="POST", path=RECORD_PREVIEW_PATH, json_body=body)


def build_record_instant_spec(args: argparse.Namespace) -> RequestSpec:
    body: dict[str, Any] = {
        "deviceSerial": args.device_serial,
        "channelNo": args.channel_no,
        "projectId": args.project_id,
        "recordSeconds": args.record_seconds,
    }
    _add_optional(body, "streamType", args.stream_type)
    _add_optional(body, "validateCode", args.validate_code)
    _add_optional(body, "voiceSwitch", args.voice_switch)
    _add_optional(body, "devProto", args.dev_proto)
    _add_optional(body, "sliceDuration", args.slice_duration)
    return RequestSpec(method="POST", path=RECORD_INSTANT_PATH, json_body=body)


def build_frame_interval_spec(args: argparse.Namespace) -> RequestSpec:
    body = _build_record_body(args)
    body["recType"] = args.rec_type
    body["frameInterval"] = args.frame_interval
    body["startTime"] = args.start_time
    _add_optional(body, "frameModel", args.frame_model)
    return RequestSpec(method="POST", path=FRAME_INTERVAL_PATH, json_body=body)


def build_frame_timing_spec(args: argparse.Namespace) -> RequestSpec:
    body = _build_record_body(args)
    body["recType"] = args.rec_type
    body["timingPoints"] = args.timing_points
    _add_optional(body, "frameModel", args.frame_model)
    return RequestSpec(method="POST", path=FRAME_TIMING_PATH, json_body=body)


def build_frame_instant_spec(args: argparse.Namespace) -> RequestSpec:
    body = _build_record_body(args)
    body["recType"] = args.rec_type
    _add_optional(body, "streamType", args.stream_type)
    return RequestSpec(method="POST", path=FRAME_INSTANT_PATH, json_body=body)


def build_task_stop_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(method="POST", path=TASK_STOP_PATH, json_body={"taskId": args.task_id})


def build_task_get_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(method="GET", path=TASK_GET_PATH, query={"taskId": args.task_id})


def build_task_list_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="GET",
        path=TASK_LIST_PATH,
        query={"projectId": args.project_id, "pageNo": args.page_no, "pageSize": args.page_size},
    )


def build_file_task_list_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="GET",
        path=FILE_TASK_LIST_PATH,
        query={"taskId": args.task_id, "pageNo": args.page_no, "pageSize": args.page_size},
    )


def build_file_get_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(method="GET", path=FILE_GET_PATH, query={"projectId": args.project_id, "fileId": args.file_id})


def build_file_list_spec(args: argparse.Namespace) -> RequestSpec:
    query: dict[str, Any] = {"projectId": args.project_id, "pageNo": args.page_no, "pageSize": args.page_size}
    _add_optional(query, "startTime", args.start_time)
    _add_optional(query, "endTime", args.end_time)
    return RequestSpec(method="GET", path=FILE_LIST_PATH, query=query)


def build_file_delete_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="DELETE",
        path=FILE_DELETE_PATH,
        query={"projectId": args.project_id, "fileId": args.file_id},
    )


def build_file_download_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="GET",
        path=FILE_DOWNLOAD_PATH,
        query={"projectId": args.project_id, "fileId": args.file_id},
    )


def build_flow_update_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="PUT",
        path=FLOW_UPDATE_PATH,
        query={"projectId": args.project_id, "flowLimit": args.flow_limit},
    )


def build_tenant_info_spec(args: argparse.Namespace) -> RequestSpec:
    del args
    return RequestSpec(method="GET", path=TENANT_INFO_PATH)


def build_upload_address_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="POST",
        path=UPLOAD_ADDRESS_PATH,
        json_body={
            "suffix": args.suffix,
            "fileNum": args.file_num,
            "fileType": args.file_type,
            "fileChildType": args.file_child_type,
        },
    )


def build_save_file_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="POST",
        path=SAVE_FILE_PATH,
        json_body={
            "sourceUrl": args.source_url,
            "sourceType": args.source_type,
            "fileType": args.file_type,
            "fileChildType": args.file_child_type,
            "fileName": args.file_name,
        },
    )


def build_clip_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(method="POST", path=CLIP_PATH, json_body={"timeLines": args.timeline_json})


def build_clip_file_query_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="POST",
        path=CLIP_FILE_QUERY_PATH,
        json_body={"taskId": args.task_id, "expireSeconds": args.expire_seconds},
    )


def run_command(args: argparse.Namespace) -> int:
    base_url = resolve_base_url(args.base_url)
    spec = args.spec_builder(args)
    payload = api_request(
        base_url=base_url,
        timeout=args.timeout,
        cache_file=Path(args.token_cache_file).expanduser(),
        explicit_token=args.access_token,
        spec=spec,
    )
    dump_output(args.command, payload, args.format)
    return 0


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--access-token", default=None)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--token-cache-file", default=str(DEFAULT_TOKEN_CACHE))
    parser.add_argument("--format", choices=("text", "json"), default="text")


def add_project_id_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--project-id", required=True)


def add_device_serial_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--device-serial", required=True)


def add_channel_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--channel-no", required=True, type=int)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hik-Cloud video recording helper.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    project_create = subparsers.add_parser("project-create")
    add_common_arguments(project_create)
    project_create.add_argument("--project-name", required=True)
    project_create.add_argument("--expire-days", required=True, type=int)
    project_create.add_argument("--flow-limit", required=True, type=int)
    project_create.set_defaults(spec_builder=build_project_create_spec)

    project_get = subparsers.add_parser("project-get")
    add_common_arguments(project_get)
    add_project_id_argument(project_get)
    project_get.set_defaults(spec_builder=build_project_get_spec)

    project_update = subparsers.add_parser("project-update")
    add_common_arguments(project_update)
    add_project_id_argument(project_update)
    project_update.add_argument("--project-name", required=True)
    project_update.add_argument("--expire-days", type=int, default=None)
    project_update.set_defaults(spec_builder=build_project_update_spec)

    project_delete = subparsers.add_parser("project-delete")
    add_common_arguments(project_delete)
    add_project_id_argument(project_delete)
    project_delete.set_defaults(spec_builder=build_project_delete_spec)

    project_list = subparsers.add_parser("project-list")
    add_common_arguments(project_list)
    project_list.add_argument("--page-no", required=True, type=int)
    project_list.add_argument("--page-size", required=True, type=int)
    project_list.set_defaults(spec_builder=build_project_list_spec)

    record_replay = subparsers.add_parser("record-replay")
    add_common_arguments(record_replay)
    add_project_id_argument(record_replay)
    add_device_serial_argument(record_replay)
    add_channel_argument(record_replay)
    record_replay.add_argument("--file-id", default=None)
    record_replay.add_argument("--start-time", required=True)
    record_replay.add_argument("--end-time", required=True)
    record_replay.add_argument("--rec-type", required=True)
    record_replay.add_argument("--validate-code", default=None)
    record_replay.add_argument("--stream-type", type=int, default=None)
    record_replay.add_argument("--dev-proto", default=None)
    record_replay.set_defaults(spec_builder=build_record_replay_spec)

    record_preview = subparsers.add_parser("record-preview")
    add_common_arguments(record_preview)
    add_project_id_argument(record_preview)
    add_device_serial_argument(record_preview)
    add_channel_argument(record_preview)
    record_preview.add_argument("--start-time", required=True)
    record_preview.add_argument("--end-time", required=True)
    record_preview.add_argument("--validate-code", default=None)
    record_preview.add_argument("--stream-type", type=int, default=None)
    record_preview.add_argument("--dev-proto", default=None)
    record_preview.add_argument("--slice-duration", type=int, default=None)
    record_preview.set_defaults(spec_builder=build_record_preview_spec)

    record_instant = subparsers.add_parser("record-instant")
    add_common_arguments(record_instant)
    add_project_id_argument(record_instant)
    add_device_serial_argument(record_instant)
    add_channel_argument(record_instant)
    record_instant.add_argument("--record-seconds", required=True, type=int)
    record_instant.add_argument("--stream-type", type=int, default=None)
    record_instant.add_argument("--validate-code", default=None)
    record_instant.add_argument("--voice-switch", type=int, default=2)
    record_instant.add_argument("--dev-proto", default=None)
    record_instant.add_argument("--slice-duration", type=int, default=None)
    record_instant.set_defaults(spec_builder=build_record_instant_spec)

    frame_interval = subparsers.add_parser("frame-interval")
    add_common_arguments(frame_interval)
    add_project_id_argument(frame_interval)
    add_device_serial_argument(frame_interval)
    add_channel_argument(frame_interval)
    frame_interval.add_argument("--rec-type", required=True)
    frame_interval.add_argument("--frame-interval", required=True, type=int)
    frame_interval.add_argument("--start-time", required=True)
    frame_interval.add_argument("--validate-code", default=None)
    frame_interval.add_argument("--frame-model", type=int, default=0)
    frame_interval.add_argument("--stream-type", type=int, default=None)
    frame_interval.add_argument("--dev-proto", default=None)
    frame_interval.set_defaults(spec_builder=build_frame_interval_spec)

    frame_timing = subparsers.add_parser("frame-timing")
    add_common_arguments(frame_timing)
    add_project_id_argument(frame_timing)
    add_device_serial_argument(frame_timing)
    add_channel_argument(frame_timing)
    frame_timing.add_argument("--rec-type", required=True)
    frame_timing.add_argument("--timing-points", required=True)
    frame_timing.add_argument("--validate-code", default=None)
    frame_timing.add_argument("--frame-model", type=int, default=0)
    frame_timing.add_argument("--stream-type", type=int, default=None)
    frame_timing.add_argument("--dev-proto", default=None)
    frame_timing.set_defaults(spec_builder=build_frame_timing_spec)

    frame_instant = subparsers.add_parser("frame-instant")
    add_common_arguments(frame_instant)
    add_project_id_argument(frame_instant)
    add_device_serial_argument(frame_instant)
    add_channel_argument(frame_instant)
    frame_instant.add_argument("--rec-type", required=True)
    frame_instant.add_argument("--validate-code", default=None)
    frame_instant.add_argument("--stream-type", type=int, default=None)
    frame_instant.add_argument("--dev-proto", default=None)
    frame_instant.set_defaults(spec_builder=build_frame_instant_spec)

    task_stop = subparsers.add_parser("task-stop")
    add_common_arguments(task_stop)
    task_stop.add_argument("--task-id", required=True)
    task_stop.set_defaults(spec_builder=build_task_stop_spec)

    task_get = subparsers.add_parser("task-get")
    add_common_arguments(task_get)
    task_get.add_argument("--task-id", required=True)
    task_get.set_defaults(spec_builder=build_task_get_spec)

    task_list = subparsers.add_parser("task-list")
    add_common_arguments(task_list)
    add_project_id_argument(task_list)
    task_list.add_argument("--page-no", required=True, type=int)
    task_list.add_argument("--page-size", required=True, type=int)
    task_list.set_defaults(spec_builder=build_task_list_spec)

    file_task_list = subparsers.add_parser("file-task-list")
    add_common_arguments(file_task_list)
    file_task_list.add_argument("--task-id", required=True)
    file_task_list.add_argument("--page-no", required=True, type=int)
    file_task_list.add_argument("--page-size", required=True, type=int)
    file_task_list.set_defaults(spec_builder=build_file_task_list_spec)

    file_get = subparsers.add_parser("file-get")
    add_common_arguments(file_get)
    add_project_id_argument(file_get)
    file_get.add_argument("--file-id", required=True)
    file_get.set_defaults(spec_builder=build_file_get_spec)

    file_list = subparsers.add_parser("file-list")
    add_common_arguments(file_list)
    add_project_id_argument(file_list)
    file_list.add_argument("--page-no", required=True, type=int)
    file_list.add_argument("--page-size", required=True, type=int)
    file_list.add_argument("--start-time", default=None)
    file_list.add_argument("--end-time", default=None)
    file_list.set_defaults(spec_builder=build_file_list_spec)

    file_delete = subparsers.add_parser("file-delete")
    add_common_arguments(file_delete)
    add_project_id_argument(file_delete)
    file_delete.add_argument("--file-id", required=True)
    file_delete.set_defaults(spec_builder=build_file_delete_spec)

    file_download = subparsers.add_parser("file-download")
    add_common_arguments(file_download)
    add_project_id_argument(file_download)
    file_download.add_argument("--file-id", required=True)
    file_download.set_defaults(spec_builder=build_file_download_spec)

    flow_update = subparsers.add_parser("flow-update")
    add_common_arguments(flow_update)
    add_project_id_argument(flow_update)
    flow_update.add_argument("--flow-limit", required=True, type=int)
    flow_update.set_defaults(spec_builder=build_flow_update_spec)

    tenant_info = subparsers.add_parser("tenant-info")
    add_common_arguments(tenant_info)
    tenant_info.set_defaults(spec_builder=build_tenant_info_spec)

    upload_address = subparsers.add_parser("upload-address")
    add_common_arguments(upload_address)
    upload_address.add_argument("--suffix", required=True)
    upload_address.add_argument("--file-num", required=True, type=int)
    upload_address.add_argument("--file-type", required=True, type=int)
    upload_address.add_argument("--file-child-type", required=True)
    upload_address.set_defaults(spec_builder=build_upload_address_spec)

    save_file = subparsers.add_parser("save-file")
    add_common_arguments(save_file)
    save_file.add_argument("--source-url", required=True)
    save_file.add_argument("--source-type", required=True, type=int)
    save_file.add_argument("--file-type", required=True, type=int)
    save_file.add_argument("--file-child-type", required=True)
    save_file.add_argument("--file-name", required=True)
    save_file.set_defaults(spec_builder=build_save_file_spec)

    clip = subparsers.add_parser("clip")
    add_common_arguments(clip)
    clip.add_argument("--timeline-json", required=True, type=json.loads)
    clip.set_defaults(spec_builder=build_clip_spec)

    clip_query = subparsers.add_parser("clip-file-query")
    add_common_arguments(clip_query)
    clip_query.add_argument("--task-id", required=True)
    clip_query.add_argument("--expire-seconds", required=True, type=int)
    clip_query.set_defaults(spec_builder=build_clip_file_query_spec)

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    configure_windows_utf8_output()
    try:
        args = parse_args(argv)
        return run_command(args)
    except ApiError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
