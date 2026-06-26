#!/usr/bin/env python3
"""Hik-Cloud OpenAPI device group management helper."""

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
TOKEN_PATH = "/oauth/token"

CREATE_GROUP_PATH = "/api/v1/open/basic/groups/create"
DELETE_GROUP_PATH = "/api/v1/open/basic/groups/delete"
UPDATE_GROUP_PATH = "/api/v1/open/basic/groups/update"
GET_GROUP_PATH = "/api/v1/open/basic/groups/get"
LIST_ALL_GROUPS_PATH = "/api/v1/open/basic/groups/actions/listAll"
LIST_CHILDREN_PATH = "/api/v1/open/basic/groups/actions/childrenList"
DEVICE_TRANSFER_PATH = "/v1/carrier/device/open/devices/actions/deviceTransfer"

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
    *,
    base_url: str,
    timeout: float,
    cache_file: Path,
    explicit_token: str | None,
    spec: RequestSpec,
) -> dict[str, Any]:
    token, token_from_refresh = resolve_access_token(base_url, timeout, cache_file, explicit_token)
    response = _perform_api_request(base_url, timeout, token, spec)
    if response["status"] == 401 and explicit_token is None:
        if not token_from_refresh:
            cache_payload = None
            if cache_file.exists():
                cache_payload = load_token_cache(cache_file)
            if cache_payload is not None:
                try:
                    cache_file.unlink()
                except OSError:
                    pass
        refreshed_token, _ = resolve_access_token(base_url, timeout, cache_file, None)
        response = _perform_api_request(base_url, timeout, refreshed_token, spec)

    payload = response["payload"]
    if response["status"] != 200:
        error_code, error_message = summarize_error_payload(payload)
        raise ApiError(
            "request failed: "
            f"http={response['status']}, code={error_code}, message={error_message}"
        )
    return response


def _perform_api_request(
    base_url: str,
    timeout: float,
    token: str,
    spec: RequestSpec,
) -> dict[str, Any]:
    status, payload = http_json_request(
        method=spec.method,
        url=spec.build_url(base_url),
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
        json_body=spec.json_body,
    )
    return {
        "status": status,
        "payload": payload,
        "request": {
            "method": spec.method,
            "url": spec.build_url(base_url),
            "query": spec.query,
            "json_body": spec.json_body,
        },
    }


def build_create_spec(args: argparse.Namespace) -> RequestSpec:
    payload: dict[str, Any] = {"groupName": args.group_name, "groupNo": args.group_no}
    if args.parent_no is not None:
        payload["parentNo"] = args.parent_no
    return RequestSpec(method="POST", path=CREATE_GROUP_PATH, json_body=payload)


def build_delete_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(method="POST", path=DELETE_GROUP_PATH, query={"groupNo": args.group_no})


def build_update_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="POST",
        path=UPDATE_GROUP_PATH,
        json_body={"groupNo": args.group_no, "groupName": args.group_name},
    )


def build_get_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(method="GET", path=GET_GROUP_PATH, query={"groupNo": args.group_no})


def build_list_all_spec(args: argparse.Namespace) -> RequestSpec:
    del args
    return RequestSpec(method="GET", path=LIST_ALL_GROUPS_PATH)


def build_list_children_spec(args: argparse.Namespace) -> RequestSpec:
    query = {"parentNo": args.parent_no} if args.parent_no is not None else None
    return RequestSpec(method="GET", path=LIST_CHILDREN_PATH, query=query)


def build_device_transfer_spec(args: argparse.Namespace) -> RequestSpec:
    return RequestSpec(
        method="POST",
        path=DEVICE_TRANSFER_PATH,
        json_body={
            "deviceSerial": args.device_serial,
            "targetGroupId": args.target_group_id,
        },
    )


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--base-url", help="Override API base URL")
    parser.add_argument("--access-token", help="Use explicit access token")
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Request timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    parser.add_argument(
        "--token-cache-file",
        type=Path,
        default=DEFAULT_TOKEN_CACHE,
        help=f"Token cache path (default: {DEFAULT_TOKEN_CACHE})",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hik-Cloud device group management helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Create a device group")
    add_common_args(create_parser)
    create_parser.add_argument("--group-name", required=True)
    create_parser.add_argument("--group-no", required=True)
    create_parser.add_argument("--parent-no")
    create_parser.set_defaults(spec_builder=build_create_spec)

    delete_parser = subparsers.add_parser("delete", help="Delete a device group")
    add_common_args(delete_parser)
    delete_parser.add_argument("--group-no", required=True)
    delete_parser.set_defaults(spec_builder=build_delete_spec)

    update_parser = subparsers.add_parser("update", help="Update a device group")
    add_common_args(update_parser)
    update_parser.add_argument("--group-no", required=True)
    update_parser.add_argument("--group-name", required=True)
    update_parser.set_defaults(spec_builder=build_update_spec)

    get_parser = subparsers.add_parser("get", help="Get one device group detail")
    add_common_args(get_parser)
    get_parser.add_argument("--group-no", required=True)
    get_parser.set_defaults(spec_builder=build_get_spec)

    list_all_parser = subparsers.add_parser("list-all", help="List all device groups")
    add_common_args(list_all_parser)
    list_all_parser.set_defaults(spec_builder=build_list_all_spec)

    list_children_parser = subparsers.add_parser("list-children", help="List child groups")
    add_common_args(list_children_parser)
    list_children_parser.add_argument("--parent-no")
    list_children_parser.set_defaults(spec_builder=build_list_children_spec)

    transfer_parser = subparsers.add_parser("device-transfer", help="Transfer device to target group")
    add_common_args(transfer_parser)
    transfer_parser.add_argument("--device-serial", required=True)
    transfer_parser.add_argument("--target-group-id", required=True)
    transfer_parser.set_defaults(spec_builder=build_device_transfer_spec)

    return parser.parse_args(argv)


def print_text_result(command: str, response: dict[str, Any]) -> None:
    payload = response["payload"]
    code = payload.get("code")
    message = payload.get("message")
    data = payload.get("data")
    print(f"command={command}")
    if code is not None:
        print(f"code={code}")
    if message is not None:
        print(f"message={message}")
    if data is None:
        return
    if isinstance(data, list):
        print(f"items={len(data)}")
        if data:
            print(json.dumps(data[:3], ensure_ascii=False, indent=2))
        return
    print(json.dumps(data, ensure_ascii=False, indent=2))


def run_command(args: argparse.Namespace) -> int:
    spec = args.spec_builder(args)
    base_url = resolve_base_url(args.base_url)
    response = api_request(
        base_url=base_url,
        timeout=args.timeout,
        cache_file=args.token_cache_file,
        explicit_token=args.access_token,
        spec=spec,
    )
    if args.format == "json":
        print(json.dumps(response, ensure_ascii=False, indent=2))
    else:
        print_text_result(args.command, response)
    return 0


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
