#!/usr/bin/env python3
"""进阶版点评 API 客户端。

当前客户端默认禁用，不会读取 API Key，也不会发起网络请求。
API 服务上线后，由部署者提供配置文件并将 enabled 设置为 true 才能启用。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any

# 允许的配置字段。部署者可以在运行环境中提供 JSON 配置，但配置不随 Skill 分发。
CONFIG_FIELDS = {"enabled", "base_url", "api_key_env", "timeout_seconds"}

# 允许上传的请求字段。严格白名单用于避免意外提交孩子隐私信息。
REQUEST_FIELDS = {
    "grade_level",
    "title",
    "composition_type",
    "teacher_requirements",
    "essay_text",
    "parent_question",
    "consent",
}

# consent 的固定字段。
CONSENT_FIELDS = {"upload_full_text", "acknowledged_privacy_notice"}

# 禁止出现在请求中的字段。即使服务端未来要求更多信息，也必须先修改协议并更新隐私说明。
FORBIDDEN_FIELDS = {
    "student_name",
    "child_name",
    "school",
    "class_name",
    "address",
    "parent_name",
    "phone",
    "email",
}


def fail(message: str) -> None:
    """输出错误并退出。"""
    print(json.dumps({"ok": False, "error": message}, ensure_ascii=False), file=sys.stderr)
    raise SystemExit(1)


def require_object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{name} 必须是 JSON 对象")
    return value


def require_exact_fields(value: dict[str, Any], allowed: set[str], name: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        fail(f"{name} 包含未知字段: {', '.join(unknown)}")


def load_config(path: Path) -> dict[str, Any]:
    """读取并校验进阶版配置。"""
    if not path.is_file():
        return {
            "enabled": False,
            "base_url": None,
            "api_key_env": None,
            "timeout_seconds": None,
        }
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"无法读取配置文件: {exc}")
        raise
    config = require_object(value, "advanced config")
    require_exact_fields(config, CONFIG_FIELDS, "advanced config")
    if not isinstance(config["enabled"], bool):
        fail("advanced config.enabled 必须是布尔值")
    if config["enabled"]:
        if not isinstance(config["base_url"], str) or not config["base_url"].startswith("https://"):
            fail("advanced config.base_url 必须是 https:// 地址")
        if not isinstance(config["api_key_env"], str) or not config["api_key_env"]:
            fail("advanced config.api_key_env 必须是非空字符串")
        timeout = config["timeout_seconds"]
        if type(timeout) is not int or not 1 <= timeout <= 60:
            fail("advanced config.timeout_seconds 必须是 1-60 的整数")
    return config


def validate_request(value: dict[str, Any]) -> dict[str, Any]:
    """校验请求内容，确保不提交协议外的隐私字段。"""
    request = require_object(value, "request")
    require_exact_fields(request, REQUEST_FIELDS, "request")
    forbidden = sorted(set(request) & FORBIDDEN_FIELDS)
    if forbidden:
        fail(f"请求包含禁止字段: {', '.join(forbidden)}")

    grade_level = request["grade_level"]
    if type(grade_level) is not int or not 1 <= grade_level <= 6:
        fail("request.grade_level 必须是 1-6 的整数")
    for field in ("title", "composition_type", "teacher_requirements", "essay_text", "parent_question"):
        if request[field] is not None and not isinstance(request[field], str):
            fail(f"request.{field} 必须是字符串或 null")

    consent = require_object(request["consent"], "request.consent")
    require_exact_fields(consent, CONSENT_FIELDS, "request.consent")
    upload_full_text = consent["upload_full_text"]
    privacy_confirmed = consent["acknowledged_privacy_notice"]
    if not isinstance(upload_full_text, bool) or not isinstance(privacy_confirmed, bool):
        fail("request.consent 中的两个字段必须都是布尔值")
    if not privacy_confirmed:
        fail("家长尚未确认隐私说明，不能调用进阶服务")
    if not upload_full_text and request["essay_text"]:
        fail("upload_full_text=false 时不能上传作文全文")

    return request


def build_payload(request: dict[str, Any]) -> dict[str, Any]:
    """构造服务端请求体。"""
    return {
        "request_id": str(uuid.uuid4()),
        **request,
    }


def request_advanced(config_path: Path, request_path: Path) -> None:
    """调用进阶版 API。只有配置显式启用时才会执行。"""
    config = load_config(config_path)
    if not config["enabled"]:
        fail("进阶版服务当前未启用")

    try:
        raw_request = json.loads(request_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"无法读取请求文件: {exc}")
        raise
    request = validate_request(raw_request)
    payload = build_payload(request)

    api_key = os.environ.get(config["api_key_env"])
    if not api_key:
        fail(f"未设置环境变量 {config['api_key_env']}，不能调用进阶服务")

    endpoint = config["base_url"].rstrip("/") + "/v1/composition-review/advanced"
    http_request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "parent-composition-coach/1",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(http_request, timeout=config["timeout_seconds"]) as response:
            body = response.read().decode("utf-8")
            result = require_object(json.loads(body), "API response")
            print(json.dumps({"ok": True, "response": result}, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as exc:
        fail(f"进阶服务返回 HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')}")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        fail(f"进阶服务调用失败: {exc}")


def show_status(config_path: Path) -> None:
    """输出当前启用状态。默认不启用。"""
    config = load_config(config_path)
    print(
        json.dumps(
            {
                "ok": True,
                "enabled": config["enabled"],
                "base_url": config["base_url"],
                "api_key_configured": bool(config["api_key_env"] and os.environ.get(config["api_key_env"])),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数。"""
    parser = argparse.ArgumentParser(description="进阶版小学作文点评 API 客户端")
    parser.add_argument(
        "--config",
        default=os.environ.get("PARENT_COMPOSITION_ADVANCED_CONFIG"),
        help="进阶服务配置 JSON 路径；未提供时表示禁用",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("status", help="查看启用状态")
    request_parser = subparsers.add_parser("request", help="调用进阶点评服务")
    request_parser.add_argument("--input", required=True, help="请求 JSON 文件路径")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if not args.config:
        if args.command == "status":
            print(
                json.dumps(
                    {"ok": True, "enabled": False, "base_url": None, "api_key_configured": False},
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return
        fail("未提供 --config，进阶版服务保持禁用")

    config_path = Path(args.config).expanduser().resolve()
    if args.command == "status":
        show_status(config_path)
        return
    request_advanced(config_path, Path(args.input).expanduser().resolve())


if __name__ == "__main__":
    main()
