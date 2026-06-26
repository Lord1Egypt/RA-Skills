#!/usr/bin/env python3
"""State model helpers for One Person Company OS v1.0."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from localization import normalize_language, pick_text
from workspace_layout import existing_state_path, state_path


STATE_VERSION = "1.0"
STATE_FILE = Path(".opcos", "state", "current-state.json")

PRODUCT_STATE_ORDER = (
    "idea",
    "defined",
    "prototype",
    "internal",
    "external",
    "launchable",
    "live",
)

PIPELINE_STAGES = ("discovering", "talking", "trial", "proposal", "won", "lost")


def default_state_v3(
    *,
    company_name: str,
    product_name: str,
    language: str,
    target_user: str = "",
    core_problem: str = "",
    product_pitch: str = "",
    company_goal: str = "",
    current_bottleneck: str = "",
    stage_id: str = "validate",
    active_roles: list[str] | None = None,
    current_round: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a v1.0 state.

    The function name stays stable for existing imports, but the payload is no
    longer stage/round compatible. v1.0 treats stage and round as old product
    concepts and keeps the business loop as the only state contract.
    """
    _ = stage_id, current_round
    language = normalize_language(language, company_name, product_name, product_pitch, target_user, core_problem)
    state = {
        "version": STATE_VERSION,
        "language": language,
        "company_name": company_name,
        "product_name": product_name,
        "founder": {
            "goal_mode": "business-loop",
            "time_budget": pick_text(language, "待确认", "To be confirmed"),
            "cash_pressure": pick_text(language, "待确认", "To be confirmed"),
            "strengths": [],
            "constraints": [],
            "working_mode": pick_text(language, "单人主控", "Solo control"),
        },
        "focus": {
            "primary_goal": company_goal or pick_text(language, "先跑通最小价值闭环", "Run the smallest value loop first"),
            "primary_bottleneck": current_bottleneck or pick_text(language, "还没有识别当前主瓶颈", "The primary bottleneck has not been identified yet"),
            "primary_arena": "sales",
            "today_action": pick_text(language, "先定义今天最短动作", "Define the shortest action for today"),
            "week_outcome": pick_text(language, "先定义本周唯一结果", "Define the single weekly outcome"),
        },
        "offer": {
            "promise": product_pitch or pick_text(language, "待补充价值承诺", "Add the value promise"),
            "target_customer": target_user or pick_text(language, "待确认首批付费用户", "Confirm the first paying user"),
            "scenario": core_problem or pick_text(language, "待确认高频使用场景", "Confirm the high-frequency scenario"),
            "pricing": pick_text(language, "待设计", "To be designed"),
            "proof": [],
        },
        "buyer": {
            "segment": target_user or pick_text(language, "待确认首批付费用户", "Confirm the first paying user"),
            "urgent_problem": core_problem or pick_text(language, "待确认高频使用场景", "Confirm the high-frequency scenario"),
            "buying_signal": pick_text(language, "待验证", "To be validated"),
            "objections": [],
        },
        "pipeline": {
            "stage_summary": {key: 0 for key in PIPELINE_STAGES},
            "next_revenue_action": pick_text(language, "先补齐第一条真实成交动作", "Add the first real revenue action"),
            "opportunities": [],
        },
        "product": {
            "state": "idea",
            "current_version": pick_text(language, "v0.1 草案", "v0.1 draft"),
            "core_capability": [product_pitch] if product_pitch else [],
            "current_gap": [core_problem] if core_problem else [],
            "launch_blocker": current_bottleneck or pick_text(language, "待识别", "To be identified"),
            "repository": "",
            "launch_path": "",
        },
        "delivery": {
            "active_customers": 0,
            "delivery_status": pick_text(language, "还没有成交客户", "No signed customers yet"),
            "blocking_issue": pick_text(language, "无", "None"),
            "next_delivery_action": pick_text(language, "先为第一位客户设计交付闭环", "Design the delivery loop for the first customer"),
        },
        "cash": {
            "cash_in": 0,
            "cash_out": 0,
            "receivable": 0,
            "monthly_target": 0,
            "runway_note": pick_text(language, "待补充现金安全边界", "Add the runway note"),
        },
        "learning": {
            "latest_signal": pick_text(language, "待记录", "To be recorded"),
            "validated_lessons": [],
            "next_experiment": pick_text(language, "待定义", "To be defined"),
        },
        "assets": {
            "sops": [],
            "templates": [],
            "cases": [],
            "automations": [],
            "reusable_code": [],
        },
        "risk": {
            "top_risks": [current_bottleneck] if current_bottleneck else [],
            "pending_decisions": [],
        },
        "decision": {
            "founder_approval_required": [],
            "recent_decisions": [],
        },
        "visuals": {
            "deterministic": True,
            "ai_image_layer": "optional",
            "last_rendered": "",
        },
        "active_roles": list(active_roles or ["founder-ceo", "control-tower", "product-strategist"]),
    }
    return sync_legacy_fields(state)


def _legacy_value(state: dict[str, Any], key: str, fallback: str = "") -> str:
    value = state.get(key)
    return value if isinstance(value, str) and value else fallback


def sync_legacy_fields(state: dict[str, Any]) -> dict[str, Any]:
    """Normalize a payload into the v1.0 business-loop contract."""
    normalized = deepcopy(state)
    language = normalize_language(
        normalized.get("language"),
        normalized.get("company_name"),
        normalized.get("product_name"),
        normalized.get("offer", {}).get("promise"),
        normalized.get("offer", {}).get("target_customer"),
    )
    normalized["version"] = STATE_VERSION
    normalized["language"] = language

    normalized.setdefault("company_name", pick_text(language, "未命名公司", "Untitled Company"))
    normalized.setdefault("product_name", pick_text(language, "未命名产品", "Untitled Product"))

    focus = normalized.setdefault("focus", {})
    offer = normalized.setdefault("offer", {})
    buyer = normalized.setdefault("buyer", {})
    pipeline = normalized.setdefault("pipeline", {})
    product = normalized.setdefault("product", {})
    delivery = normalized.setdefault("delivery", {})
    cash = normalized.setdefault("cash", {})
    learning = normalized.setdefault("learning", {})
    assets = normalized.setdefault("assets", {})
    risk = normalized.setdefault("risk", {})
    founder = normalized.setdefault("founder", {})
    decision = normalized.setdefault("decision", {})
    visuals = normalized.setdefault("visuals", {})

    focus.setdefault("primary_goal", _legacy_value(normalized, "company_goal", pick_text(language, "先跑通最小价值闭环", "Run the smallest value loop first")))
    focus.setdefault("primary_bottleneck", _legacy_value(normalized, "current_bottleneck", pick_text(language, "还没有识别当前主瓶颈", "The primary bottleneck has not been identified yet")))
    focus.setdefault("primary_arena", "sales")
    focus.setdefault("today_action", normalized.get("current_round", {}).get("next_action") or pick_text(language, "先定义今天最短动作", "Define the shortest action for today"))
    focus.setdefault("week_outcome", normalized.get("current_round", {}).get("goal") or pick_text(language, "先定义本周唯一结果", "Define the single weekly outcome"))

    offer.setdefault("promise", _legacy_value(normalized, "product_pitch", pick_text(language, "待补充价值承诺", "Add the value promise")))
    offer.setdefault("target_customer", _legacy_value(normalized, "target_user", pick_text(language, "待确认首批付费用户", "Confirm the first paying user")))
    offer.setdefault("scenario", _legacy_value(normalized, "core_problem", pick_text(language, "待确认高频使用场景", "Confirm the high-frequency scenario")))
    offer.setdefault("pricing", pick_text(language, "待设计", "To be designed"))
    offer.setdefault("proof", [])

    buyer.setdefault("segment", offer["target_customer"])
    buyer.setdefault("urgent_problem", offer["scenario"])
    buyer.setdefault("buying_signal", pick_text(language, "待验证", "To be validated"))
    buyer.setdefault("objections", [])

    pipeline.setdefault("stage_summary", {})
    for key in PIPELINE_STAGES:
        pipeline["stage_summary"].setdefault(key, 0)
    pipeline.setdefault("next_revenue_action", pick_text(language, "先补齐第一条真实成交动作", "Add the first real revenue action"))
    pipeline.setdefault("opportunities", [])

    product.setdefault("state", "idea")
    product.setdefault("current_version", pick_text(language, "v0.1 草案", "v0.1 draft"))
    product.setdefault("core_capability", [])
    product.setdefault("current_gap", [])
    product.setdefault("launch_blocker", focus["primary_bottleneck"])
    product.setdefault("repository", "")
    product.setdefault("launch_path", "")

    delivery.setdefault("active_customers", 0)
    delivery.setdefault("delivery_status", pick_text(language, "还没有成交客户", "No signed customers yet"))
    delivery.setdefault("blocking_issue", pick_text(language, "无", "None"))
    delivery.setdefault("next_delivery_action", pick_text(language, "先为第一位客户设计交付闭环", "Design the delivery loop for the first customer"))

    cash.setdefault("cash_in", 0)
    cash.setdefault("cash_out", 0)
    cash.setdefault("receivable", 0)
    cash.setdefault("monthly_target", 0)
    cash.setdefault("runway_note", pick_text(language, "待补充现金安全边界", "Add the runway note"))

    learning.setdefault("latest_signal", pick_text(language, "待记录", "To be recorded"))
    learning.setdefault("validated_lessons", [])
    learning.setdefault("next_experiment", pick_text(language, "待定义", "To be defined"))

    for key in ("sops", "templates", "cases", "automations", "reusable_code"):
        assets.setdefault(key, [])

    risk.setdefault("top_risks", [])
    risk.setdefault("pending_decisions", [])
    founder.setdefault("goal_mode", "business-loop")
    founder.setdefault("time_budget", pick_text(language, "待确认", "To be confirmed"))
    founder.setdefault("cash_pressure", pick_text(language, "待确认", "To be confirmed"))
    founder.setdefault("strengths", [])
    founder.setdefault("constraints", [])
    founder.setdefault("working_mode", pick_text(language, "单人主控", "Solo control"))
    decision.setdefault("founder_approval_required", [])
    decision.setdefault("recent_decisions", [])
    visuals.setdefault("deterministic", True)
    visuals.setdefault("ai_image_layer", "optional")
    visuals.setdefault("last_rendered", "")
    normalized.setdefault("active_roles", ["founder-ceo", "control-tower", "product-strategist"])

    for legacy_key in (
        "stage_id",
        "stage_label",
        "current_round",
        "company_goal",
        "current_bottleneck",
        "target_user",
        "core_problem",
        "product_pitch",
    ):
        normalized.pop(legacy_key, None)

    return normalized


def upgrade_legacy_state(state: dict[str, Any]) -> dict[str, Any]:
    if str(state.get("version", "")) == STATE_VERSION:
        return sync_legacy_fields(state)
    return sync_legacy_fields(state)


def read_state_any_version(company_dir: Path) -> dict[str, Any]:
    path = existing_state_path(company_dir)
    payload = json.loads(path.read_text(encoding="utf-8"))
    return upgrade_legacy_state(payload)


def write_state_v3(company_dir: Path, state: dict[str, Any]) -> dict[str, Any]:
    upgraded = upgrade_legacy_state(state)
    path = state_path(company_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(upgraded, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return upgraded
