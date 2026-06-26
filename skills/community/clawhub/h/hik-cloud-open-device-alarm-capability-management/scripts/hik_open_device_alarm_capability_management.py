#!/usr/bin/env python3
"""Hik-Cloud OpenAPI device alarm capability helper."""

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

ALARM_CAPABILITY_LIST_PATH = "/api/v1/open/basic/abilities/list"
ALARM_CAPABILITY_UPDATE_STATUS_PATH = "/api/v1/open/basic/abilities/updateStatus"
INTELLIGENCE_DETECTION_SWITCH_PATH = "/v1/carrier/charon/storage/open/setIntelligenceDetectionSwitch"
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
    elif isinstance(data, list):
        lines.append(f"data: {data}")
    elif data is not None:
        lines.append(f"data: {data}")
    return "\n".join(lines)


def dump_output(command: str, payload: dict[str, Any], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps({"command": command, "result": payload}, ensure_ascii=False, indent=2))
        return
    print(format_text_output(command, payload))


def build_list_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="GET",
        path=ALARM_CAPABILITY_LIST_PATH,
        query={"deviceSerial": args.device_serial},
    )


def build_update_status_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="POST",
        path=ALARM_CAPABILITY_UPDATE_STATUS_PATH,
        json_body={
            "channelId": args.channel_id,
            "abilityCode": args.ability_code,
            "status": args.status,
        },
    )


def build_intelligence_switch_spec(args: argparse.Namespace) -> RequestSpec:
    body: dict[str, Any] = {
        "deviceSerial": args.device_serial,
        "enable": args.enable,
    }
    if args.channel_no is not None:
        body["channelNo"] = args.channel_no
    if args.type is not None:
        body["type"] = args.type
    return RequestSpec(
        method="POST",
        path=INTELLIGENCE_DETECTION_SWITCH_PATH,
        json_body=body,
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


def add_device_serial_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--device-serial", required=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hik-Cloud device alarm capability helper.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list")
    add_common_arguments(list_parser)
    add_device_serial_argument(list_parser)
    list_parser.set_defaults(spec_builder=build_list_spec)

    update_status = subparsers.add_parser("update-status")
    add_common_arguments(update_status)
    update_status.add_argument("--channel-id", required=True)
    update_status.add_argument("--ability-code", required=True)
    update_status.add_argument("--status", required=True, type=int)
    update_status.set_defaults(spec_builder=build_update_status_spec)

    intelligence_switch = subparsers.add_parser("intelligence-switch")
    add_common_arguments(intelligence_switch)
    add_device_serial_argument(intelligence_switch)
    intelligence_switch.add_argument("--enable", required=True, type=int)
    intelligence_switch.add_argument("--channel-no", type=int, default=None)
    intelligence_switch.add_argument("--type", default=None)
    intelligence_switch.set_defaults(spec_builder=build_intelligence_switch_spec)

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
