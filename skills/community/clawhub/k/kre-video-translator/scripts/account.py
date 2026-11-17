"""Configure local API-key access and inspect the production account."""

from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
import tempfile
import warnings
from pathlib import Path
from typing import Any

import credentials
import terminal
import translate
from errors import CredentialRequiredError, ScriptError, ToolInstallRequiredError


class AccountError(ScriptError):
    """Expected account helper failure."""


def _emit(marker: str, payload: dict[str, Any]) -> None:
    print(f"{marker}={json.dumps(payload, ensure_ascii=False)}")


def _get_with_key(args: argparse.Namespace, route: str, action: str, api_key: str) -> dict[str, Any]:
    request_lib = translate._require_requests(allow_install=args.allow_install_tools)
    base_url = translate._normalize_base_url(args.base_url)
    with request_lib.Session() as session:
        return translate._request_json(
            session, "GET", f"{base_url}{route}", action=action,
            timeout_seconds=args.request_timeout,
            headers=translate._authorization_headers(api_key),
        )


def _get(args: argparse.Namespace, route: str, action: str) -> dict[str, Any]:
    return _get_with_key(args, route, action, credentials.require_key(args.locale))


def _scope_report(payload: dict[str, Any], locale: str) -> dict[str, Any]:
    scopes = payload.get("scopes")
    if not isinstance(scopes, list) or not all(isinstance(scope, str) for scope in scopes):
        return {
            "scope_check": "unavailable", "granted_scopes": None,
            "missing_scopes": None,
            "unverified_scopes": ["task:write", "task:read"],
        }
    granted = sorted(set(scopes))
    missing = [scope for scope in credentials.REQUIRED_SCOPES if scope not in granted]
    if missing:
        raise AccountError(
            ("API Key 缺少必要权限：" if locale == "zh" else "API key is missing required scopes: ")
            + ", ".join(missing)
        )
    return {"scope_check": "verified", "granted_scopes": granted, "missing_scopes": []}


def _verify_key_value(args: argparse.Namespace, api_key: str) -> dict[str, Any]:
    api_key = credentials.validate_key(api_key)
    try:
        account = _get_with_key(args, "/external/me", "Verify API key", api_key)
    except ScriptError as exc:
        exc.args = (str(exc).replace(api_key, "[redacted]"),)
        raise
    report = _scope_report(account, args.locale)
    return {
        "configured": True,
        "status": "verified" if report["scope_check"] == "verified" else "account_verified",
        **report, "account": account,
    }


def _verify(args: argparse.Namespace) -> int:
    result = _verify_key_value(args, credentials.require_key(args.locale))
    _emit("KRE_VIDEO_TRANSLATOR_AUTH_JSON", result)
    return 0


def _detect(args: argparse.Namespace) -> int:
    _emit("KRE_VIDEO_TRANSLATOR_AUTH_JSON", {"locale": args.locale, **credentials.status()})
    return 0


def _save_key(args: argparse.Namespace) -> int:
    if sys.stdin.isatty():
        raise AccountError(
            "请使用 auth setup 在隐藏输入提示中配置 Key。"
            if args.locale == "zh" else "Use auth setup for hidden key input."
        )
    candidate = sys.stdin.readline().strip()
    if not candidate:
        raise AccountError("API Key 不能为空。" if args.locale == "zh" else "API key cannot be empty.")
    result = _verify_key_value(args, candidate)
    path = credentials.write_key(candidate, Path(args.key_file) if args.key_file else None)
    _emit("KRE_VIDEO_TRANSLATOR_AUTH_JSON", {**result, "saved": True, "api_key_file": str(path)})
    return 0


def _setup(args: argparse.Namespace) -> int:
    if not terminal.input_available():
        raise AccountError(
            "无法显示隐藏输入提示。请使用 auth launch 打开终端，或在自己的终端运行 auth setup。"
            if args.locale == "zh"
            else "Hidden input is unavailable. Use auth launch or run auth setup in your own terminal."
        )
    current = credentials.status()
    if current["configured"]:
        prompt = (
            "已检测到 API Key。按回车确认；更换请粘贴新 Key（输入不会回显）："
            if args.locale == "zh"
            else "API key detected. Press Enter to confirm, or paste a replacement (input hidden): "
        )
    else:
        prompt = (
            "请粘贴 API Key 并回车（输入不会回显，留空取消）："
            if args.locale == "zh"
            else "Paste your API key and press Enter (input hidden; blank cancels): "
        )
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", getpass.GetPassWarning)
            candidate = getpass.getpass(prompt).strip()
    except (EOFError, KeyboardInterrupt, getpass.GetPassWarning) as exc:
        raise AccountError("API Key 配置未完成。" if args.locale == "zh" else "API key setup was not completed.") from exc
    if not candidate:
        if not current["configured"]:
            raise AccountError("已取消配置。" if args.locale == "zh" else "Setup canceled.")
        result = {**_verify_key_value(args, credentials.require_key(args.locale)), "saved": False}
    else:
        if current["source"] == "environment":
            raise AccountError(
                "当前 Key 来自环境变量，请先移除该变量再更换。"
                if args.locale == "zh"
                else "Remove the current API-key environment variable before replacing the key."
            )
        result = _verify_key_value(args, candidate)
        path = credentials.write_key(candidate)
        result.update(saved=True, api_key_file=str(path))
    _receipt(args, result)
    _emit("KRE_VIDEO_TRANSLATOR_AUTH_JSON", result)
    if result["scope_check"] == "verified":
        print("API Key 已配置并验证。" if args.locale == "zh" else "API key configured and verified.")
    else:
        print(
            "API Key 已配置，账户访问已验证；服务端未提供任务权限信息。"
            if args.locale == "zh"
            else "API key configured and account access verified; task scopes are unavailable from this server."
        )
    return 0


def _receipt(args: argparse.Namespace, result: dict[str, Any]) -> None:
    if path := getattr(args, "result_file", ""):
        fields = ("status", "configured", "saved", "scope_check", "missing_scopes", "api_key_file", "error_code")
        translate._write_json_atomic(Path(path), {field: result[field] for field in fields if field in result})


def _launch(args: argparse.Namespace) -> int:
    result_file = Path(tempfile.mkdtemp(prefix="kre-key-setup-")) / "result.json"
    argv = [
        sys.executable, str(Path(__file__).resolve()), "--locale", args.locale,
        "--base-url", translate._normalize_base_url(args.base_url),
        "--request-timeout", str(args.request_timeout), "auth", "setup",
        "--result-file", str(result_file), "--keep-open",
    ]
    if args.allow_install_tools:
        argv.insert(2, "--allow-install-tools")
    translate._write_json_atomic(result_file, {"status": "awaiting_input", "configured": False})
    launched = terminal.launch(argv)
    _emit("KRE_VIDEO_TRANSLATOR_AUTH_JSON", {
        "status": "launched" if launched else "manual_required",
        "result_file": str(result_file),
        "setup_command": terminal.command_text(argv),
    })
    return 0


def _status(args: argparse.Namespace) -> int:
    _emit("KRE_VIDEO_TRANSLATOR_ACCOUNT_JSON", _get(args, "/external/me", "Read account status"))
    return 0


def _packages(args: argparse.Namespace) -> int:
    _emit("KRE_VIDEO_TRANSLATOR_PACKAGES_JSON", _get(args, "/external/packages", "Read packages"))
    return 0


def _console(args: argparse.Namespace) -> int:
    _emit("KRE_VIDEO_TRANSLATOR_CONSOLE_JSON", credentials.guidance(args.locale))
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locale", choices=credentials.SUPPORTED_LOCALES, required=True,
                        help="zh for Chinese conversations; en otherwise.")
    parser.add_argument("--base-url", default=os.getenv(translate.BASE_URL_ENV_NAME, translate.DEFAULT_BASE_URL))
    parser.add_argument("--request-timeout", type=float, default=30.0)
    parser.add_argument(
        "--allow-install-tools",
        action="store_true",
        help="Install missing local tools after the user has approved the installation.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    for name, handler, help_text in (
        ("status", _status, "Read account quota"),
        ("packages", _packages, "Read resource packages"),
        ("console", _console, "Print official URLs without opening a browser"),
    ):
        commands.add_parser(name, help=help_text).set_defaults(handler=handler)
    save = commands.add_parser("save-key", help="Validate and save a key from a secure input stream")
    save.add_argument("--stdin", action="store_true", required=True)
    save.add_argument("--key-file", default="")
    save.set_defaults(handler=_save_key)
    auth = commands.add_parser("auth", help="Detect, configure, or verify API-key access")
    auth_commands = auth.add_subparsers(dest="auth_command", required=True)
    for name, handler, help_text in (
        ("detect", _detect, "Detect local configuration without a network call"),
        ("launch", _launch, "Open a visible terminal and run setup"),
        ("setup", _setup, "Prompt for a key, verify it, and save locally"),
        ("verify", _verify, "Verify the configured key and scopes"),
    ):
        command = auth_commands.add_parser(name, help=help_text)
        command.set_defaults(handler=handler)
        if name == "setup":
            command.add_argument("--result-file", default="", help=argparse.SUPPRESS)
            command.add_argument("--keep-open", action="store_true", help=argparse.SUPPRESS)
    return parser


def main(argv: list[str] | None = None) -> int:
    translate._configure_stdio_utf8()
    args = _build_parser().parse_args(argv)
    try:
        return int(args.handler(args))
    except (ScriptError, OSError) as exc:
        if isinstance(exc, CredentialRequiredError) and getattr(args, "auth_command", "") != "setup":
            _emit("KRE_VIDEO_TRANSLATOR_CREDENTIAL_GUIDANCE_JSON", credentials.guidance(args.locale))
        _receipt(args, {"status": "failed", "configured": False, "error_code": getattr(exc, "error_code", "setup_failed")})
        print(f"ERROR: {exc}", file=sys.stderr)
        error_payload = {
            "command": args.command, "error": str(exc),
            "request_id": getattr(exc, "request_id", "") or None,
            "retryable": bool(getattr(exc, "retryable", False)),
        }
        if isinstance(exc, ToolInstallRequiredError):
            error_payload.update(
                next_action="ask_user_to_approve_tool_install",
                install_required=True,
                tool=exc.tool,
                install_command=exc.install_command,
            )
        _emit("KRE_VIDEO_TRANSLATOR_ACCOUNT_ERROR_JSON", error_payload)
        return 1
    finally:
        if getattr(args, "keep_open", False) and terminal.input_available():
            try:
                input("按回车关闭此配置程序。" if args.locale == "zh" else "Press Enter to close setup.")
            except (EOFError, KeyboardInterrupt):
                pass


if __name__ == "__main__":
    raise SystemExit(main())
