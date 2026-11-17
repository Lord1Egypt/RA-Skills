#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""当前账号积存金持仓/收益 — 统一入口（Agent 内部调用）。"""
import argparse
import json
import sys
import urllib.error
from typing import List, Optional, Tuple

import jos
import bff_client
from query_holdings import (
    VIEW_MODE,
    extract_specified_accounts,
    is_current_account_query,
    parse_intent,
    render_holdings,
)

EXIT_NOT_LOGGED_IN = 10
EXIT_WRONG_ACCOUNT = 11
EXIT_BAD_INTENT = 12
EXIT_API_ERROR = 3


def _log_internal(msg: str) -> None:
    print(f"[内部] {msg}", file=sys.stderr)


def _account_mismatch_message(specified: List[str], session_pin: Optional[str], uid: Optional[str]) -> str:
    current = session_pin or "您的登录账号"
    spec = "、".join(specified)
    return (
        "仅支持查询您当前登录账户的信息。\n"
        f"您指定了：{spec}\n"
        f"当前登录账号：{current}\n"
        "如需查询自己的持仓，请说「查询我的持仓」或「查询收益」。"
    )


def _not_logged_in_message(auth_url: Optional[str], wait_hint: bool) -> str:
    lines = [
        "请先完成登录授权，然后我再帮您查询持仓/收益。",
    ]
    if auth_url:
        lines.append("")
        lines.append(auth_url)
    if wait_hint:
        lines.append("")
        lines.append("完成授权后将自动继续查询。")
    return "\n".join(lines)


def _pin_not_supported_message(specified: List[str]) -> str:
    spec = "、".join(specified)
    return (
        "仅支持查询您当前登录账户的持仓/收益，不支持指定其他账号。\n"
        f"您提到了：{spec}\n"
        "请说「查询我的持仓」，或先完成登录后再查询。"
    )


def _validate_account_scope(text: str, logged_in: bool) -> Tuple[bool, Optional[str]]:
    specified = extract_specified_accounts(text)
    if not specified:
        return True, None

    if not is_current_account_query(text):
        if not logged_in:
            return False, _pin_not_supported_message(specified)
        session_pin, uid = jos.get_session_pin()
        for item in specified:
            low = item.lower()
            if low.startswith("jd_"):
                if session_pin and low == session_pin.lower():
                    continue
                if uid and low.replace("jd_", "") == str(uid):
                    continue
                return False, _account_mismatch_message(specified, session_pin, uid)
            if session_pin and item != session_pin and item.lower() != session_pin.lower():
                return False, _account_mismatch_message(specified, session_pin, uid)
    return True, None


def _ensure_auth_url() -> str:
    try:
        return jos.start_login_daemon()
    except RuntimeError:
        url, _ = jos.get_login_auth_url()
        return url


def _run_query(intent: str, json_out: bool) -> int:
    try:
        data = jos.fetch_holdings()
        session_pin, _ = jos.get_session_pin()
    except urllib.error.URLError as e:
        _log_internal(f"网络错误: {e}")
        print("查询暂时失败，请稍后重试。", file=sys.stderr)
        return EXIT_API_ERROR
    except RuntimeError as e:
        if getattr(e, "code", None) == 403:
            print(e.message, file=sys.stderr)
            return EXIT_API_ERROR
        _log_internal(f"业务错误: {e}")
        print("查询暂时失败，请稍后重试。", file=sys.stderr)
        return EXIT_API_ERROR

    jos.clear_pending_holdings()
    if json_out:
        print(json.dumps({
            "view": VIEW_MODE,
            "intent": intent,
            "session_pin": session_pin,
            "data": data,
        }, ensure_ascii=False, indent=2))
    else:
        print(render_holdings(data, intent, session_pin=session_pin))
    return 0


def run(text: Optional[str], intent: str, *, wait_login: bool, json_out: bool, resume: bool, intent_explicit: bool = False) -> int:
    if resume:
        pending = jos.load_pending_holdings()
        if not pending:
            _log_internal("无 pending 续查请求")
            print("暂无待查询的持仓/收益请求。", file=sys.stderr)
            return 1
        text = pending.get("text") or ""
        intent = pending.get("intent") or "both"
        intent_explicit = False  # resume 时以 pending 为准

    if text:
        parsed = parse_intent(text)
        if parsed:
            # 仅在未显式指定 --intent 时用文本解析结果覆盖
            if not intent_explicit:
                intent = parsed
        elif not resume:
            print("请说「查询持仓」「查询收益」或「查询我的持仓」。", file=sys.stderr)
            return EXIT_BAD_INTENT

    logged_in, _ = jos.check_token()
    ok_scope, scope_err = _validate_account_scope(text or "", logged_in)
    if not ok_scope:
        print(scope_err, file=sys.stderr)
        return EXIT_WRONG_ACCOUNT if logged_in else EXIT_NOT_LOGGED_IN

    if not logged_in:
        jos.save_pending_holdings({"text": text or "", "intent": intent})
        auth_url = _ensure_auth_url()
        print(_not_logged_in_message(auth_url, wait_login))
        if not wait_login:
            return EXIT_NOT_LOGGED_IN
        _log_internal("等待用户完成授权…")
        ok, _ = jos.wait_for_token(timeout_sec=300)
        if not ok:
            print("登录超时，请重新发起查询。", file=sys.stderr)
            return EXIT_NOT_LOGGED_IN
        print("\n登录成功，正在为您查询…\n")
        ok_scope, scope_err = _validate_account_scope(text or "", True)
        if not ok_scope:
            print(scope_err, file=sys.stderr)
            jos.clear_pending_holdings()
            return EXIT_WRONG_ACCOUNT

    return _run_query(intent, json_out)


def main(argv=None):
    p = argparse.ArgumentParser(description="当前账号积存金持仓/收益统一入口")
    p.add_argument("--parse", "-p", metavar="TEXT", help="用户原文")
    p.add_argument("--intent", choices=("holdings", "income", "both"), default="both")
    p.add_argument("--wait-login", action="store_true", help="未登录时等待授权完成后自动续查")
    p.add_argument("--resume", action="store_true", help="登录完成后续查上次请求")
    p.add_argument("--json", action="store_true", help="输出 JSON")
    p.add_argument("--claw", help="上报客户端 claw 类型（如 codex、openclaw）")
    args = p.parse_args(argv)
    bff_client.set_claw(args.claw)

    if not args.parse and not args.resume:
        p.print_help()
        return 1

    # 判断 --intent 是否被用户显式指定（而非使用默认值 "both"）
    intent_explicit = "--intent" in (argv or sys.argv[1:])

    return run(args.parse, args.intent, wait_login=args.wait_login, json_out=args.json, resume=args.resume, intent_explicit=intent_explicit)


if __name__ == "__main__":
    sys.exit(main())
