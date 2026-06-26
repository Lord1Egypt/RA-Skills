#!/usr/bin/env python3
"""Hik-Cloud OpenAPI device control helper."""

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

ARM_SET_PATH = "/api/v1/ezviz/devices/actions/setDefence/deviceSerial"
ARM_GET_PATH = "/api/v1/ezviz/devices/queryDeviceDefenceStatus"
PTZ_START_PATH = "/api/v1/open/basic/channels/actions/ptz/start"
PTZ_STOP_PATH = "/api/v1/open/basic/channels/actions/ptz/stop"
CAPTURE_PATH = "/api/v1/open/basic/channels/actions/capture"
OSD_SET_NAME_PATH = "/api/v1/ezviz/devices/actions/setOsdName"
OSD_GET_NAME_PATH = "/api/v1/ezviz/devices/actions/getOsdName"
OSD_CONFIG_PATH = "/api/v1/ezviz/devices/osd/config"
TIME_GET_PATH = "/api/v1/device/isapi/system/time"
TIME_SET_PATH = "/api/v1/device/isapi/system/time"
NTP_GET_PATH = "/api/v1/device/isapi/system/time/ntpServers"
NTP_SET_PATH = "/api/v1/device/isapi/system/time/ntpServers"
NTP_CONFIG_GET_PATH = "/api/v1/device/isapi/system/time/ntpServers/config"
NTP_CONFIG_SET_PATH = "/api/v1/device/isapi/system/time/ntpServers/config"
STORAGE_INIT_PATH = "/v1/carrier/charon/storage/open/init"
STORAGE_INIT_PROGRESS_PATH = "/v1/carrier/charon/storage/open/init/progress"
TOKEN_PATH = "/oauth/token"

PTZ_DIRECTIONS = set(range(12))
PTZ_SPEED_MODE_ZERO = {0, 1, 2}
PTZ_SPEED_MODE_ONE = set(range(8))
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
    """Prefer UTF-8 for Windows console output so Chinese text stays readable."""
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


def strtobool(value: str) -> bool:
    lowered = value.lower()
    if lowered in {"1", "true", "yes", "y", "on"}:
        return True
    if lowered in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"invalid boolean value: {value}")


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


def build_arm_set_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="POST",
        path=ARM_SET_PATH,
        query={"deviceSerial": args.device_serial, "isDefence": args.is_defence},
    )


def build_arm_get_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="GET",
        path=ARM_GET_PATH,
        query={"deviceSerial": args.device_serial},
    )


def validate_ptz_args(direction: int, speed: int | None, mode: int | None) -> None:
    if direction not in PTZ_DIRECTIONS:
        raise ApiError(f"invalid direction: {direction}")
    resolved_mode = 0 if mode is None else mode
    if speed is None:
        return
    if resolved_mode == 0 and speed not in PTZ_SPEED_MODE_ZERO:
        raise ApiError(f"invalid speed for mode=0: {speed}")
    if resolved_mode == 1 and speed not in PTZ_SPEED_MODE_ONE:
        raise ApiError(f"invalid speed for mode=1: {speed}")


def build_ptz_start_spec(args: argparse.Namespace) -> RequestSpec:
    validate_ptz_args(args.direction, args.speed, args.mode)
    body: dict[str, Any] = {
        "deviceSerial": args.device_serial,
        "channelNo": args.channel_no,
        "speed": args.speed,
        "direction": args.direction,
    }
    if args.mode is not None:
        body["mode"] = args.mode
    return RequestSpec(method="POST", path=PTZ_START_PATH, json_body=body)


def build_ptz_stop_spec(args: argparse.Namespace) -> RequestSpec:
    validate_ptz_args(args.direction, None, None)
    return RequestSpec(
        method="POST",
        path=PTZ_STOP_PATH,
        json_body={
            "deviceSerial": args.device_serial,
            "channelNo": args.channel_no,
            "direction": args.direction,
        },
    )


def build_capture_spec(args: argparse.Namespace) -> RequestSpec:
    body: dict[str, Any] = {
        "deviceSerial": args.device_serial,
        "channelNo": args.channel_no,
    }
    if args.quality is not None:
        body["quality"] = args.quality
    return RequestSpec(method="POST", path=CAPTURE_PATH, json_body=body)


def build_osd_set_name_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="POST",
        path=OSD_SET_NAME_PATH,
        json_body={
            "deviceSerial": args.device_serial,
            "osdName": args.osd_name,
            "channelNo": str(args.channel_no),
        },
    )


def build_osd_get_name_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="GET",
        path=OSD_GET_NAME_PATH,
        query={"deviceSerial": args.device_serial, "channelNo": args.channel_no},
    )


def build_osd_config_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="POST",
        path=OSD_CONFIG_PATH,
        json_body={
            "deviceSerial": args.device_serial,
            "channelNo": str(args.channel_no),
            "channelNameOsd": {
                "enabled": args.channel_name_osd_enabled,
                "positionX": args.channel_name_osd_position_x,
                "positionY": args.channel_name_osd_position_y,
            },
        },
    )


def build_time_get_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="GET",
        path=TIME_GET_PATH,
        query={"deviceSerial": args.device_serial},
    )


def build_time_set_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="POST",
        path=TIME_SET_PATH,
        json_body={"deviceSerial": args.device_serial, "timeMode": args.time_mode},
    )


def build_ntp_server_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "id": str(args.ntp_server_id),
        "addressingFormatType": args.addressing_format_type,
        "portNo": args.port_no,
        "synchronizeInterval": args.synchronize_interval,
    }
    if args.host_name is not None:
        payload["hostName"] = args.host_name
    if args.ip_address is not None:
        payload["ipAddress"] = args.ip_address
    if args.ipv6_address is not None:
        payload["ipv6Address"] = args.ipv6_address
    return payload


def build_ntp_get_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="GET",
        path=NTP_GET_PATH,
        query={"deviceSerial": args.device_serial},
    )


def build_ntp_set_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="POST",
        path=NTP_SET_PATH,
        json_body={
            "deviceSerial": args.device_serial,
            "ntpServer": build_ntp_server_payload(args),
        },
    )


def build_ntp_config_get_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="GET",
        path=NTP_CONFIG_GET_PATH,
        query={"deviceSerial": args.device_serial, "ntpServerId": args.ntp_server_id},
    )


def build_ntp_config_set_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="POST",
        path=NTP_CONFIG_SET_PATH,
        json_body={
            "deviceSerial": args.device_serial,
            "ntpServerId": args.ntp_server_id,
            "ntpServer": build_ntp_server_payload(args),
        },
    )


def build_storage_init_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="POST",
        path=STORAGE_INIT_PATH,
        json_body={"devSerial": args.device_serial},
    )


def build_storage_init_progress_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="POST",
        path=STORAGE_INIT_PROGRESS_PATH,
        json_body={"devSerial": args.device_serial},
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


def add_channel_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--channel-no", required=True, type=int)


def add_ntp_server_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--ntp-server-id", required=True, type=int)
    parser.add_argument("--addressing-format-type", required=True)
    parser.add_argument("--host-name", default=None)
    parser.add_argument("--ip-address", default=None)
    parser.add_argument("--ipv6-address", default=None)
    parser.add_argument("--port-no", required=True, type=int)
    parser.add_argument("--synchronize-interval", required=True, type=int)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hik-Cloud device control helper.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    arm_set = subparsers.add_parser("arm-set")
    add_common_arguments(arm_set)
    add_device_serial_argument(arm_set)
    arm_set.add_argument("--is-defence", required=True, type=int)
    arm_set.set_defaults(spec_builder=build_arm_set_spec)

    arm_get = subparsers.add_parser("arm-get")
    add_common_arguments(arm_get)
    add_device_serial_argument(arm_get)
    arm_get.set_defaults(spec_builder=build_arm_get_spec)

    ptz_start = subparsers.add_parser("ptz-start")
    add_common_arguments(ptz_start)
    add_device_serial_argument(ptz_start)
    add_channel_argument(ptz_start)
    ptz_start.add_argument("--direction", required=True, type=int)
    ptz_start.add_argument("--speed", required=True, type=int)
    ptz_start.add_argument("--mode", type=int, default=None)
    ptz_start.set_defaults(spec_builder=build_ptz_start_spec)

    ptz_stop = subparsers.add_parser("ptz-stop")
    add_common_arguments(ptz_stop)
    add_device_serial_argument(ptz_stop)
    add_channel_argument(ptz_stop)
    ptz_stop.add_argument("--direction", required=True, type=int)
    ptz_stop.set_defaults(spec_builder=build_ptz_stop_spec)

    capture = subparsers.add_parser("capture")
    add_common_arguments(capture)
    add_device_serial_argument(capture)
    add_channel_argument(capture)
    capture.add_argument("--quality", type=int, default=None)
    capture.set_defaults(spec_builder=build_capture_spec)

    osd_set_name = subparsers.add_parser("osd-set-name")
    add_common_arguments(osd_set_name)
    add_device_serial_argument(osd_set_name)
    add_channel_argument(osd_set_name)
    osd_set_name.add_argument("--osd-name", required=True)
    osd_set_name.set_defaults(spec_builder=build_osd_set_name_spec)

    osd_get_name = subparsers.add_parser("osd-get-name")
    add_common_arguments(osd_get_name)
    add_device_serial_argument(osd_get_name)
    add_channel_argument(osd_get_name)
    osd_get_name.set_defaults(spec_builder=build_osd_get_name_spec)

    osd_config = subparsers.add_parser("osd-config")
    add_common_arguments(osd_config)
    add_device_serial_argument(osd_config)
    add_channel_argument(osd_config)
    osd_config.add_argument("--channel-name-osd-enabled", required=True, type=strtobool)
    osd_config.add_argument("--channel-name-osd-position-x", required=True, type=int)
    osd_config.add_argument("--channel-name-osd-position-y", required=True, type=int)
    osd_config.set_defaults(spec_builder=build_osd_config_spec)

    time_get = subparsers.add_parser("time-get")
    add_common_arguments(time_get)
    add_device_serial_argument(time_get)
    time_get.set_defaults(spec_builder=build_time_get_spec)

    time_set = subparsers.add_parser("time-set")
    add_common_arguments(time_set)
    add_device_serial_argument(time_set)
    time_set.add_argument("--time-mode", required=True)
    time_set.set_defaults(spec_builder=build_time_set_spec)

    ntp_get = subparsers.add_parser("ntp-get")
    add_common_arguments(ntp_get)
    add_device_serial_argument(ntp_get)
    ntp_get.set_defaults(spec_builder=build_ntp_get_spec)

    ntp_set = subparsers.add_parser("ntp-set")
    add_common_arguments(ntp_set)
    add_device_serial_argument(ntp_set)
    add_ntp_server_arguments(ntp_set)
    ntp_set.set_defaults(spec_builder=build_ntp_set_spec)

    ntp_config_get = subparsers.add_parser("ntp-config-get")
    add_common_arguments(ntp_config_get)
    add_device_serial_argument(ntp_config_get)
    ntp_config_get.add_argument("--ntp-server-id", required=True, type=int)
    ntp_config_get.set_defaults(spec_builder=build_ntp_config_get_spec)

    ntp_config_set = subparsers.add_parser("ntp-config-set")
    add_common_arguments(ntp_config_set)
    add_device_serial_argument(ntp_config_set)
    add_ntp_server_arguments(ntp_config_set)
    ntp_config_set.set_defaults(spec_builder=build_ntp_config_set_spec)

    storage_init = subparsers.add_parser("storage-init")
    add_common_arguments(storage_init)
    add_device_serial_argument(storage_init)
    storage_init.set_defaults(spec_builder=build_storage_init_spec)

    storage_init_progress = subparsers.add_parser("storage-init-progress")
    add_common_arguments(storage_init_progress)
    add_device_serial_argument(storage_init_progress)
    storage_init_progress.set_defaults(spec_builder=build_storage_init_progress_spec)

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
