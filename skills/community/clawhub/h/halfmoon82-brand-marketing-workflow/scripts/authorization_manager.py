#!/usr/bin/env python3
"""Authorization interaction layer for brand-marketing-workflow.

Handles boundary detection, state transitions, and human-assist flows
including login gates and captcha gates.

Input JSON:
{
  "action": str,
  "data_access": "public"|"authorized"|"unknown",
  "requires_payment": bool,
  "human_response": str,
  "state": "running"|"awaiting_confirmation"|"resumed"|"degraded"|"blocked",
  "screenshot_path": str  (optional, for login_gate/captcha_gate)
}
"""
from __future__ import annotations

import json
import sys
from typing import Dict, List

RESPONSE_MAP = {
    "确认继续": "confirm",
    "授权执行": "authorize",
    "授权支付": "authorize_payment",
    "拒绝": "deny",
    "已登录": "confirm",
    "已完成": "confirm",
    "继续": "confirm",
}

ALWAYS_ALLOWED_ACTIONS = {"public_read", "draft_prepare", "content_generate", "competitor_analyze"}
CONFIRM_REQUIRED_ACTIONS = {"publish", "ad_launch", "authorized_data_access"}
PAYMENT_REQUIRED_ACTIONS = {"payment", "recharge"}
HUMAN_ASSIST_REQUIRED = {"login_gate", "captcha_gate"}

# Risk-based threshold adjustment based on historical success
RISK_THRESHOLDS = {
    "low": {"actions": {"draft_prepare", "content_generate", "competitor_analyze"}, "skip_auth": True},
    "medium": {"actions": {"publish", "ad_launch"}, "skip_auth": False},
    "high": {"actions": {"payment", "recharge", "authorized_data_access"}, "skip_auth": False},
}


def should_skip_auth(action: str, data_access: str, historical_success_rate: float = 0.0) -> bool:
    """
    基于动作类型、数据访问级别和历史成功率，判断是否可跳过 auth 触发。
    减少低风险场景的误触发。
    """
    # 低风险动作 + 公开数据 = 总是跳过
    if action in RISK_THRESHOLDS["low"]["actions"] and data_access == "public":
        return True
    
    # 历史成功率 > 90% 的常规动作 = 可跳过
    if historical_success_rate > 0.9 and action in RISK_THRESHOLDS["low"]["actions"]:
        return True
    
    return False


def normalize_response(response: str) -> str:
    r = (response or "").strip()
    return RESPONSE_MAP.get(r, r)


def boundary_reasons(action: str, data_access: str, requires_payment: bool, skip_auth: bool = False) -> List[str]:
    """检查边界原因，支持智能跳过低风险场景。"""
    if skip_auth:
        return []
    
    reasons: List[str] = []
    if action in CONFIRM_REQUIRED_ACTIONS:
        reasons.append("action '{}' requires human confirmation".format(action))
    if action in PAYMENT_REQUIRED_ACTIONS or requires_payment:
        reasons.append("payment/recharge requires explicit human authorization")
    if action == "login_gate":
        reasons.append("login wall detected: human must scan QR code or authorize login before proceeding")
    if action == "captcha_gate":
        reasons.append("captcha detected: human must solve the captcha before proceeding")
    if data_access not in {"public", "authorized"}:
        reasons.append("data access scope is unclear; only public/authorized sources are allowed")
    if action not in ALWAYS_ALLOWED_ACTIONS | CONFIRM_REQUIRED_ACTIONS | PAYMENT_REQUIRED_ACTIONS | HUMAN_ASSIST_REQUIRED:
        reasons.append("unknown action '{}' must be reviewed before execution".format(action))
    return reasons


def build_request(reasons: List[str]) -> str:
    details = "\n".join(["- " + r for r in reasons]) or "- requires human confirmation"
    return (
        "[需要人类确认]\n"
        "当前操作超出允许边界。\n\n"
        "原因：\n{}\n\n"
        "需要你的确认：\n"
        "- 是否继续\n"
        "- 是否授权访问\n"
        "- 是否授权发布/投放\n"
        "- 是否授权支付/充值\n\n"
        "可回复：\n"
        "- 确认继续\n"
        "- 授权执行\n"
        "- 授权支付\n"
        "- 拒绝"
    ).format(details)


def human_assist_request(action: str, screenshot_path: str = "") -> Dict[str, str]:
    if action == "login_gate":
        return {
            "type": "login_gate",
            "message": (
                "[需要扫码登录]\n"
                "浏览器遇到登录弹窗，无法继续采集内容。\n\n"
                "请操作：\n"
                "1. 查看截图确认登录弹窗\n"
                "2. 在浏览器中扫码完成登录\n"
                "3. 登录成功后回复 已登录 或 继续\n\n"
                "截图已发送。等待你的确认后继续执行。"
            ),
            "screenshot_path": screenshot_path,
            "resume_condition": "human replies 已登录 or 继续",
        }
    if action == "captcha_gate":
        return {
            "type": "captcha_gate",
            "message": (
                "[需要人工处理验证码]\n"
                "浏览器遇到验证码，无法自动通过。\n\n"
                "请操作：\n"
                "1. 查看截图确认验证码类型\n"
                "2. 在浏览器中手动完成验证\n"
                "3. 验证完成后回复 已完成 或 继续\n\n"
                "截图已发送。等待你的确认后继续执行。"
            ),
            "screenshot_path": screenshot_path,
            "resume_condition": "human replies 已完成 or 继续",
        }
    return {}


def transition(state: str, response: str, needs_payment: bool, has_boundary: bool) -> Dict[str, str]:
    response = normalize_response(response)
    if not has_boundary:
        return {"state": "running", "decision": "allow"}
    if response == "deny":
        return {"state": "degraded", "decision": "degrade"}
    if needs_payment:
        if response == "authorize_payment":
            return {"state": "resumed", "decision": "allow_payment"}
        return {"state": "awaiting_confirmation", "decision": "pause"}
    if response in {"confirm", "authorize"}:
        return {"state": "resumed", "decision": "allow"}
    if state in {"resumed", "running"} and response in {"confirm", "authorize", "authorize_payment"}:
        return {"state": "resumed", "decision": "allow"}
    return {"state": "awaiting_confirmation", "decision": "pause"}


def main() -> int:
    raw = sys.stdin.read().strip()
    payload = json.loads(raw) if raw else {}

    action = payload.get("action", "unknown")
    data_access = payload.get("data_access", "unknown")
    requires_payment = bool(payload.get("requires_payment", False))
    human_response = payload.get("human_response", "")
    state = payload.get("state", "running")
    screenshot_path = payload.get("screenshot_path", "")
    fallback = payload.get("fallback", "Use public data + official APIs + draft-only execution.")
    historical_success_rate = float(payload.get("historical_success_rate", 0.0))

    # Smart auth skipping for low-risk scenarios
    skip_auth = should_skip_auth(action, data_access, historical_success_rate)
    
    reasons = boundary_reasons(action, data_access, requires_payment, skip_auth)
    has_boundary = len(reasons) > 0
    t = transition(state, human_response, requires_payment, has_boundary)

    assist = {}
    if action in HUMAN_ASSIST_REQUIRED:
        assist = human_assist_request(action, screenshot_path)

    out = {
        "has_boundary": has_boundary,
        "reasons": reasons,
        "authorization_request": build_request(reasons) if has_boundary else "",
        "human_assist": assist,
        "state": t["state"],
        "decision": t["decision"],
        "pause": t["decision"] == "pause",
        "fallback": fallback if t["decision"] in {"degrade", "pause"} else "",
        "resume_condition": "explicit human confirmation" if t["decision"] == "pause" else "",
        "allowed_scope": "public+authorized-only",
        "auth_skipped": skip_auth,  # New field to track optimization
    }

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
