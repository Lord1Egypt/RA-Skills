#!/usr/bin/env python3
"""
Create an AIOB realtime outbound call task.

Default behavior:
- Load AK/SK/robotId/mobile/callerNum and other defaults from config.json
- Allow CLI args to override config values (especially mobile)
- Support convenient dialogVar overrides via --name, --owner-name and --user-intent

Typical usage:
1) Call default configured phone
   python3 create_realtime_call.py

2) Override phone only ("打电话给 1333333")
   python3 create_realtime_call.py --mobile "13333333333"

3) Pass common dialog variables
   python3 create_realtime_call.py --mobile "13333333333" --name "张三" --owner-name "王五" --user-intent "下午三点开会"

4) Use custom config path
   python3 create_realtime_call.py --config ./my-config.json --mobile "13333333333"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

import requests

TOKEN_URL = "https://aiob-open.baidu.com/api/v2/getToken"
REALTIME_CALL_URL = "https://aiob-open.baidu.com/api/v3/console/realtime/status/create"


REQUIRED_CONFIG_KEYS = ["accessKey", "secretKey", "robotId", "mobile"]


def parse_json_arg(raw: str | None, field_name: str) -> Dict[str, Any] | None:
    if raw is None:
        return None
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{field_name} is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be a JSON object")
    return value


def load_config(config_path: str) -> Dict[str, Any]:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"config file not found: {config_path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in config file: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("config root must be a JSON object")
    return data


def get_access_token(access_key: str, secret_key: str, timeout: int = 15) -> str:
    payload = {"accessKey": access_key, "secretKey": secret_key}
    resp = requests.post(TOKEN_URL, json=payload, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()

    if data.get("code") != 200 or not data.get("data", {}).get("accessToken"):
        raise RuntimeError(f"getToken failed: {json.dumps(data, ensure_ascii=False)}")

    return data["data"]["accessToken"]


def create_realtime_call(access_token: str, body: Dict[str, Any], timeout: int = 20) -> Dict[str, Any]:
    headers = {
        "Content-Type": "application/json",
        "Authorization": access_token,
    }
    resp = requests.post(REALTIME_CALL_URL, headers=headers, json=body, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def get_value(config: Dict[str, Any], cli_value: Any, key: str, required: bool = False) -> Any:
    value = cli_value if cli_value is not None else config.get(key)
    if required and (value is None or value == ""):
        raise ValueError(f"missing required value: {key} (set in config or CLI)")
    return value


def merge_dialog_var(config: Dict[str, Any], args: argparse.Namespace) -> Dict[str, Any] | None:
    dialog_var = parse_json_arg(args.dialog_var, "dialogVar") if args.dialog_var is not None else config.get("dialogVar")
    if dialog_var is not None and not isinstance(dialog_var, dict):
        raise ValueError("dialogVar must be a JSON object")

    merged = dict(dialog_var or {})
    if args.name is not None:
        merged["name"] = args.name
    if args.owner_name is not None:
        merged["owner_name"] = args.owner_name
    if args.user_intent is not None:
        merged["user_intent"] = args.user_intent

    merged["internal_request_from"] = "openClaw"

    cleaned = {
        key: value
        for key, value in merged.items()
        if value is not None and (not isinstance(value, str) or value.strip() != "")
    }

    return cleaned or None


def build_call_body(config: Dict[str, Any], args: argparse.Namespace) -> Dict[str, Any]:
    robot_id = get_value(config, args.robot_id, "robotId", required=True)
    mobile = get_value(config, args.mobile, "mobile", required=True)
    secret_type = get_value(config, args.secret_type, "secretType")
    if secret_type is None:
        secret_type = 2

    body: Dict[str, Any] = {
        "robotId": robot_id,
        "mobile": mobile,
        "secretType": int(secret_type),
    }

    caller_num = args.caller_num if args.caller_num is not None else config.get("callerNum")
    if caller_num:
        body["callerNum"] = caller_num

    stop_date = get_value(config, args.stop_date, "stopDate")
    if stop_date:
        body["stopDate"] = stop_date

    dialog_var = merge_dialog_var(config, args)
    if dialog_var is not None:
        body["dialogVar"] = dialog_var

    secret_id = get_value(config, args.secret_id, "secretId")
    if secret_id is not None:
        body["secretId"] = secret_id

    plain_text = get_value(config, args.plain_text, "plainText")
    if plain_text is not None:
        body["plainText"] = plain_text

    cipher_text = get_value(config, args.cipher_text, "cipherText")
    if cipher_text is not None:
        body["cipherText"] = cipher_text

    callback_url = get_value(config, args.callback_url, "callBackUrl")
    if callback_url is not None:
        body["callBackUrl"] = callback_url

    ext_json = get_value(config, args.ext_json, "extJson")
    if ext_json is not None:
        body["extJson"] = ext_json

    return body


def make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Create AIOB realtime call task (config-first)")
    p.add_argument("--config", default="config.json", help="Path to config JSON (default: config.json)")
    p.add_argument("--access-key", help="Override accessKey")
    p.add_argument("--secret-key", help="Override secretKey")
    p.add_argument("--robot-id", help="Override robotId")
    p.add_argument("--mobile", help="Override mobile")
    p.add_argument("--secret-type", type=int, choices=[1, 2, 3], help="Override secretType")
    p.add_argument("--caller-num", nargs="*", help="Override callerNum list")
    p.add_argument("--stop-date", help="Override stopDate, format yyyy-MM-dd HH:mm:ss")
    p.add_argument("--dialog-var", help="Override dialogVar JSON object string")
    p.add_argument("--name", help="Set dialogVar.name, e.g. 张三")
    p.add_argument("--owner-name", help="Set dialogVar.owner_name, e.g. 王五")
    p.add_argument("--user-intent", help="Set dialogVar.user_intent, e.g. 下午三点开会")
    p.add_argument("--secret-id", help="Override secretId")
    p.add_argument("--plain-text", help="Override plainText")
    p.add_argument("--cipher-text", help="Override cipherText")
    p.add_argument("--callback-url", help="Override callBackUrl")
    p.add_argument("--ext-json", help="Override extJson")
    return p


def main() -> int:
    parser = make_parser()
    args = parser.parse_args()

    try:
        config = load_config(args.config)

        # Validate required keys presence in merged config/CLI path
        for key in REQUIRED_CONFIG_KEYS:
            cli_map = {
                "accessKey": args.access_key,
                "secretKey": args.secret_key,
                "robotId": args.robot_id,
                "mobile": args.mobile,
            }
            if cli_map[key] is None and not config.get(key):
                raise ValueError(f"missing required value: {key} (set in {args.config} or CLI)")

        access_key = get_value(config, args.access_key, "accessKey", required=True)
        secret_key = get_value(config, args.secret_key, "secretKey", required=True)

        token = get_access_token(access_key, secret_key)
        call_body = build_call_body(config, args)
        result = create_realtime_call(token, call_body)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"request": call_body, "response": result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
