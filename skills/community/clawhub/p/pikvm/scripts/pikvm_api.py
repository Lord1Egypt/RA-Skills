#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests


class PiKVMClient:
    def __init__(
        self,
        base_url: str,
        user: str,
        password: str,
        verify_ssl: bool = True,
        use_basic_auth: bool = False,
        timeout: int = 60,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.user = user
        self.password = password
        self.verify_ssl = verify_ssl
        self.use_basic_auth = use_basic_auth
        self.timeout = timeout
        self.session = requests.Session()
        if self.use_basic_auth:
            self.session.auth = (self.user, self.password)
        else:
            self.session.headers.update({
                "X-KVMD-User": self.user,
                "X-KVMD-Passwd": self.password,
            })

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: Any = None,
        headers: dict[str, str] | None = None,
        stream: bool = False,
    ) -> requests.Response:
        url = f"{self.base_url}{path}"
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            timeout=self.timeout,
            verify=self.verify_ssl,
            stream=stream,
        )
        response.raise_for_status()
        return response

    def get_json(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.request("GET", path, params=params).json()

    def post_json(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: Any = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        return self.request("POST", path, params=params, data=data, headers=headers).json()

    def delete_json(self, path: str) -> dict[str, Any]:
        return self.request("DELETE", path).json()


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def build_client(args: argparse.Namespace) -> PiKVMClient:
    base_url = args.url or os.getenv("PIKVM_URL")
    user = args.user or os.getenv("PIKVM_USER")
    password = args.password or os.getenv("PIKVM_PASS")
    verify_ssl = not args.insecure if args.insecure is not None else env_bool("PIKVM_VERIFY_SSL", True)
    use_basic_auth = args.basic_auth if args.basic_auth is not None else env_bool("PIKVM_USE_BASIC_AUTH", False)

    missing = [
        name
        for name, value in (("PIKVM_URL", base_url), ("PIKVM_USER", user), ("PIKVM_PASS", password))
        if not value
    ]
    if missing:
        raise SystemExit(f"Missing required configuration: {', '.join(missing)}")

    return PiKVMClient(
        base_url=base_url,
        user=user,
        password=password,
        verify_ssl=verify_ssl,
        use_basic_auth=use_basic_auth,
    )


def print_json(payload: Any) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def to_bool(value: str | bool | None) -> bool | None:
    if value is None or isinstance(value, bool):
        return value
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean value: {value}")


def cmd_info(client: PiKVMClient, args: argparse.Namespace) -> None:
    print_json(client.get_json("/api/info"))


def cmd_atx_state(client: PiKVMClient, args: argparse.Namespace) -> None:
    print_json(client.get_json("/api/atx"))


def cmd_atx_power(client: PiKVMClient, args: argparse.Namespace) -> None:
    print_json(client.post_json("/api/atx/power", params={"action": args.action, "wait": args.wait}))


def cmd_atx_click(client: PiKVMClient, args: argparse.Namespace) -> None:
    print_json(client.post_json("/api/atx/click", params={"button": args.button, "wait": args.wait}))


def cmd_hid_print(client: PiKVMClient, args: argparse.Namespace) -> None:
    params: dict[str, Any] = {"slow": args.slow}
    if args.limit is not None:
        params["limit"] = args.limit
    if args.keymap:
        params["keymap"] = args.keymap
    print_json(client.post_json("/api/hid/print", params=params, data=args.text.encode("utf-8")))


def cmd_hid_shortcut(client: PiKVMClient, args: argparse.Namespace) -> None:
    print_json(client.post_json("/api/hid/events/send_shortcut", params={"keys": args.keys}))


def cmd_hid_key(client: PiKVMClient, args: argparse.Namespace) -> None:
    print_json(client.post_json("/api/hid/events/send_key", params={"key": args.key}))


def cmd_mouse_button(client: PiKVMClient, args: argparse.Namespace) -> None:
    params: dict[str, Any] = {"button": args.button}
    if args.state is not None:
        params["state"] = args.state
    print_json(client.post_json("/api/hid/events/send_mouse_button", params=params))


def cmd_mouse_move(client: PiKVMClient, args: argparse.Namespace) -> None:
    print_json(client.post_json("/api/hid/events/send_mouse_move", params={"to_x": args.to_x, "to_y": args.to_y}))


def cmd_streamer_state(client: PiKVMClient, args: argparse.Namespace) -> None:
    print_json(client.get_json("/api/streamer"))


def cmd_snapshot(client: PiKVMClient, args: argparse.Namespace) -> None:
    params: dict[str, Any] = {
        "save": args.save,
        "load": args.load,
        "allow_offline": args.allow_offline,
        "preview": args.preview,
    }
    if args.preview_max_width is not None:
        params["preview_max_width"] = args.preview_max_width
    if args.preview_max_height is not None:
        params["preview_max_height"] = args.preview_max_height
    if args.preview_quality is not None:
        params["preview_quality"] = args.preview_quality
    if args.ocr:
        params["ocr"] = True
    if args.langs:
        params["ocr_langs"] = args.langs
    if args.left is not None:
        params["ocr_left"] = args.left
    if args.top is not None:
        params["ocr_top"] = args.top
    if args.right is not None:
        params["ocr_right"] = args.right
    if args.bottom is not None:
        params["ocr_bottom"] = args.bottom

    response = client.request("GET", "/api/streamer/snapshot", params=params, stream=True)
    content_type = response.headers.get("content-type", "")

    if "application/json" in content_type:
        print_json(response.json())
        return

    if not args.save_path:
        raise SystemExit("Snapshot returned image data. Provide --save-path to save it.")

    save_path = Path(args.save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with save_path.open("wb") as fh:
        for chunk in response.iter_content(chunk_size=1024 * 64):
            if chunk:
                fh.write(chunk)
    print_json({"ok": True, "saved_to": str(save_path), "content_type": content_type})


def cmd_ocr(client: PiKVMClient, args: argparse.Namespace) -> None:
    params: dict[str, Any] = {"ocr": True}
    if args.langs:
        params["ocr_langs"] = args.langs
    if args.left is not None:
        params["ocr_left"] = args.left
    if args.top is not None:
        params["ocr_top"] = args.top
    if args.right is not None:
        params["ocr_right"] = args.right
    if args.bottom is not None:
        params["ocr_bottom"] = args.bottom
    print_json(client.get_json("/api/streamer/snapshot", params=params))


def cmd_msd_state(client: PiKVMClient, args: argparse.Namespace) -> None:
    print_json(client.get_json("/api/msd"))


def cmd_msd_upload(client: PiKVMClient, args: argparse.Namespace) -> None:
    image_path = Path(args.file)
    if not image_path.is_file():
        raise SystemExit(f"Image file not found: {image_path}")
    with image_path.open("rb") as fh:
        print_json(client.post_json("/api/msd/write", params={"image": args.image or image_path.name}, data=fh))


def cmd_msd_download_remote(client: PiKVMClient, args: argparse.Namespace) -> None:
    params = {"url": args.remote_url}
    if args.image:
        params["image"] = args.image
    print_json(client.post_json("/api/msd/write_remote", params=params))


def cmd_msd_set(client: PiKVMClient, args: argparse.Namespace) -> None:
    params: dict[str, Any] = {}
    if args.image is not None:
        params["image"] = args.image
    if args.cdrom is not None:
        params["cdrom"] = args.cdrom
    if args.rw is not None:
        params["rw"] = args.rw
    print_json(client.post_json("/api/msd/set_params", params=params))


def cmd_msd_connect(client: PiKVMClient, args: argparse.Namespace) -> None:
    print_json(client.post_json("/api/msd/set_connected", params={"connected": args.connected}))


def cmd_msd_remove(client: PiKVMClient, args: argparse.Namespace) -> None:
    print_json(client.post_json("/api/msd/remove", params={"image": args.image}))


def cmd_switch_state(client: PiKVMClient, args: argparse.Namespace) -> None:
    print_json(client.get_json("/api/switch"))


def cmd_switch_active(client: PiKVMClient, args: argparse.Namespace) -> None:
    print_json(client.post_json("/api/switch/set_active", params={"port": args.port}))


def cmd_switch_atx_power(client: PiKVMClient, args: argparse.Namespace) -> None:
    print_json(client.post_json("/api/switch/atx/power", params={"port": args.port, "action": args.action}))


def add_common_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--url", help="PiKVM base URL. Defaults to PIKVM_URL.")
    parser.add_argument("--user", help="PiKVM username. Defaults to PIKVM_USER.")
    parser.add_argument("--password", help="PiKVM password. Defaults to PIKVM_PASS.")
    parser.add_argument("--insecure", action="store_true", default=None, help="Disable TLS certificate verification.")
    parser.add_argument("--basic-auth", action="store_true", default=None, help="Use HTTP Basic Auth instead of X-KVMD headers.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PiKVM HTTP API helper")
    add_common_options(parser)
    subparsers = parser.add_subparsers(dest="command", required=True)

    p = subparsers.add_parser("info")
    p.set_defaults(func=cmd_info)

    p = subparsers.add_parser("atx-state")
    p.set_defaults(func=cmd_atx_state)

    p = subparsers.add_parser("atx-power")
    p.add_argument("--action", required=True, choices=["on", "off", "off_hard", "reset_hard"])
    p.add_argument("--wait", type=to_bool, default=True)
    p.set_defaults(func=cmd_atx_power)

    p = subparsers.add_parser("atx-click")
    p.add_argument("--button", required=True, choices=["power", "power_long", "reset"])
    p.add_argument("--wait", type=to_bool, default=True)
    p.set_defaults(func=cmd_atx_click)

    p = subparsers.add_parser("hid-print")
    p.add_argument("--text", required=True)
    p.add_argument("--keymap")
    p.add_argument("--limit", type=int)
    p.add_argument("--slow", action="store_true")
    p.set_defaults(func=cmd_hid_print)

    p = subparsers.add_parser("hid-shortcut")
    p.add_argument("--keys", required=True, help="Comma-separated keys, e.g. ControlLeft,AltLeft,Delete")
    p.set_defaults(func=cmd_hid_shortcut)

    p = subparsers.add_parser("hid-key")
    p.add_argument("--key", required=True)
    p.set_defaults(func=cmd_hid_key)

    p = subparsers.add_parser("mouse-button")
    p.add_argument("--button", required=True, choices=["left", "middle", "right", "up", "down"])
    p.add_argument("--state", type=to_bool)
    p.set_defaults(func=cmd_mouse_button)

    p = subparsers.add_parser("mouse-move")
    p.add_argument("--to-x", required=True, type=int)
    p.add_argument("--to-y", required=True, type=int)
    p.set_defaults(func=cmd_mouse_move)

    p = subparsers.add_parser("streamer-state")
    p.set_defaults(func=cmd_streamer_state)

    p = subparsers.add_parser("snapshot")
    p.add_argument("--save", action="store_true")
    p.add_argument("--load", action="store_true")
    p.add_argument("--allow-offline", action="store_true")
    p.add_argument("--preview", action="store_true")
    p.add_argument("--preview-max-width", type=int)
    p.add_argument("--preview-max-height", type=int)
    p.add_argument("--preview-quality", type=int)
    p.add_argument("--ocr", action="store_true")
    p.add_argument("--langs", help="Comma-separated OCR languages, e.g. eng,deu")
    p.add_argument("--left", type=int)
    p.add_argument("--top", type=int)
    p.add_argument("--right", type=int)
    p.add_argument("--bottom", type=int)
    p.add_argument("--save-path", help="Where to save image bytes if snapshot returns binary data")
    p.set_defaults(func=cmd_snapshot)

    p = subparsers.add_parser("ocr")
    p.add_argument("--langs", help="Comma-separated OCR languages, e.g. eng,deu")
    p.add_argument("--left", type=int)
    p.add_argument("--top", type=int)
    p.add_argument("--right", type=int)
    p.add_argument("--bottom", type=int)
    p.set_defaults(func=cmd_ocr)

    p = subparsers.add_parser("msd-state")
    p.set_defaults(func=cmd_msd_state)

    p = subparsers.add_parser("msd-upload")
    p.add_argument("--file", required=True)
    p.add_argument("--image", help="Destination image name on PiKVM")
    p.set_defaults(func=cmd_msd_upload)

    p = subparsers.add_parser("msd-download-remote")
    p.add_argument("--remote-url", required=True)
    p.add_argument("--image")
    p.set_defaults(func=cmd_msd_download_remote)

    p = subparsers.add_parser("msd-set")
    p.add_argument("--image")
    p.add_argument("--cdrom", type=to_bool)
    p.add_argument("--rw", type=to_bool)
    p.set_defaults(func=cmd_msd_set)

    p = subparsers.add_parser("msd-connect")
    p.add_argument("--connected", type=to_bool, required=True)
    p.set_defaults(func=cmd_msd_connect)

    p = subparsers.add_parser("msd-remove")
    p.add_argument("--image", required=True)
    p.set_defaults(func=cmd_msd_remove)

    p = subparsers.add_parser("switch-state")
    p.set_defaults(func=cmd_switch_state)

    p = subparsers.add_parser("switch-active")
    p.add_argument("--port", required=True, help="Port number like 2 or 2,2")
    p.set_defaults(func=cmd_switch_active)

    p = subparsers.add_parser("switch-atx-power")
    p.add_argument("--port", required=True, help="Port number like 2 or 2,2")
    p.add_argument("--action", required=True, choices=["on", "off", "off_hard", "reset_hard"])
    p.set_defaults(func=cmd_switch_atx_power)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    client = build_client(args)
    try:
        args.func(client, args)
    except requests.HTTPError as exc:
        response = exc.response
        payload: dict[str, Any] = {
            "ok": False,
            "status_code": response.status_code if response is not None else None,
            "error": str(exc),
        }
        if response is not None:
            payload["response_text"] = response.text
        print_json(payload)
        return 1
    except requests.RequestException as exc:
        print_json({"ok": False, "error": str(exc)})
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
