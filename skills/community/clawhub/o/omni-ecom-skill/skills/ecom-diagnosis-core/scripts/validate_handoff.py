#!/usr/bin/env python3
"""Validate the machine-readable handoff envelope before the lead consumes it."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED = (
    "schema_version",
    "artifact_type",
    "contract_name",
    "contract_version",
    "created_by_team_version",
    "legacy_compatibility",
    "run_id",
    "agent_id",
    "agent_version",
    "scope",
    "gate_status",
    "status",
    "facts",
    "judgments",
    "hypotheses",
    "actions",
    "risks",
    "missing_data",
    "evidence_ledger",
)
GATE_STATUSES = {"PASS", "WARN", "BLOCKED"}
STATUSES = {"data_blocked", "draft_diagnosis", "ready_for_review"}
CONFIDENCE = {"high", "medium", "low"}
APPROVAL = {"not_required", "pending", "approved", "rejected", "executed", "verified"}
BLOCKED_ACTION_TERMS = re.compile(r"预算|加投|调价|降价|提价|库存补货|发布|投放启停|加大投放")


def add(errors: list[str], path: str, message: str) -> None:
    errors.append(f"{path}: {message}")


def string_field(obj: dict[str, Any], key: str, errors: list[str], path: str) -> str | None:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        add(errors, f"{path}.{key}", "必须是非空字符串")
        return None
    return value.strip()


def evidence_refs(value: Any, evidence_ids: set[str], errors: list[str], path: str) -> None:
    if not isinstance(value, list) or not value:
        add(errors, path, "必须是非空证据 ID 数组")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str) or not re.fullmatch(r"E[0-9A-Za-z._-]+", item):
            add(errors, f"{path}[{index}]", "不是合法证据 ID")
        elif item not in evidence_ids:
            add(errors, f"{path}[{index}]", f"未在 evidence_ledger 中定义: {item}")


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED:
        if key not in payload:
            add(errors, key, "缺少必填字段")
    if errors:
        return errors

    if payload.get("schema_version") != "2.0":
        add(errors, "schema_version", "当前专家回传必须为 2.0；1.0 只能走只读历史迁移")
    if payload.get("artifact_type") != "expert_handoff":
        add(errors, "artifact_type", "必须为 expert_handoff")
    if payload.get("contract_name") != "omni-ecom.expert-handoff":
        add(errors, "contract_name", "必须为 omni-ecom.expert-handoff")
    if payload.get("contract_version") != "2.0":
        add(errors, "contract_version", "必须为 2.0")
    run_id = string_field(payload, "run_id", errors, "handoff")
    if run_id and not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{2,80}", run_id):
        add(errors, "run_id", "包含不安全字符或长度不合法")
    for key in ("agent_id", "agent_version"):
        string_field(payload, key, errors, "handoff")
    if payload.get("created_by_team_version") != payload.get("agent_version"):
        add(errors, "created_by_team_version", "必须与 agent_version 一致")
    legacy = payload.get("legacy_compatibility")
    if not isinstance(legacy, dict) or legacy != {
        "read_only_import": ["omni-ecom.expert-handoff@1.0"],
        "current_agent_return": False,
        "execution_permission_inherited": False,
    }:
        add(errors, "legacy_compatibility", "旧交接件只能只读导入且不得继承当前回传或执行权限")

    scope = payload.get("scope")
    if not isinstance(scope, dict):
        add(errors, "scope", "必须是对象")
    else:
        for key in ("platform", "store", "period", "grain"):
            string_field(scope, key, errors, "scope")

    gate_status = payload.get("gate_status")
    status = payload.get("status")
    if gate_status not in GATE_STATUSES:
        add(errors, "gate_status", f"必须是 {sorted(GATE_STATUSES)} 之一")
    if status not in STATUSES:
        add(errors, "status", f"必须是 {sorted(STATUSES)} 之一")
    if gate_status == "BLOCKED" and status != "data_blocked":
        add(errors, "status", "BLOCKED 只能交接为 data_blocked")
    if status == "ready_for_review" and gate_status == "BLOCKED":
        add(errors, "status", "BLOCKED 不得标记 ready_for_review")

    for key in ("facts", "judgments", "hypotheses", "actions", "risks", "missing_data", "evidence_ledger"):
        if not isinstance(payload.get(key), list):
            add(errors, key, "必须是数组")

    evidence_ids: set[str] = set()
    for index, item in enumerate(payload.get("evidence_ledger", [])):
        path = f"evidence_ledger[{index}]"
        if not isinstance(item, dict):
            add(errors, path, "必须是对象")
            continue
        evidence_id = string_field(item, "id", errors, path)
        if evidence_id:
            if not re.fullmatch(r"E[0-9A-Za-z._-]+", evidence_id):
                add(errors, f"{path}.id", "不是合法证据 ID")
            elif evidence_id in evidence_ids:
                add(errors, f"{path}.id", "证据 ID 重复")
            evidence_ids.add(evidence_id)
        for key in ("source", "period", "metric", "status"):
            string_field(item, key, errors, path)
        if item.get("status") not in {"verified", "warning", "blocked", "unverified"}:
            add(errors, f"{path}.status", "不是合法证据状态")

    for index, item in enumerate(payload.get("facts", [])):
        path = f"facts[{index}]"
        if not isinstance(item, dict):
            add(errors, path, "必须是对象")
            continue
        string_field(item, "id", errors, path)
        string_field(item, "claim", errors, path)
        evidence_refs(item.get("evidence_ids"), evidence_ids, errors, f"{path}.evidence_ids")

    for index, item in enumerate(payload.get("judgments", [])):
        path = f"judgments[{index}]"
        if not isinstance(item, dict):
            add(errors, path, "必须是对象")
            continue
        string_field(item, "id", errors, path)
        string_field(item, "claim", errors, path)
        if item.get("confidence") not in CONFIDENCE:
            add(errors, f"{path}.confidence", "不是 high/medium/low")
        evidence_refs(item.get("evidence_ids"), evidence_ids, errors, f"{path}.evidence_ids")
        if not isinstance(item.get("counter_conditions"), list):
            add(errors, f"{path}.counter_conditions", "必须是数组")

    for index, item in enumerate(payload.get("hypotheses", [])):
        path = f"hypotheses[{index}]"
        if not isinstance(item, dict):
            add(errors, path, "必须是对象")
            continue
        for key in ("id", "claim", "verification_method"):
            string_field(item, key, errors, path)
        if not isinstance(item.get("counter_conditions"), list):
            add(errors, f"{path}.counter_conditions", "必须是数组")

    for index, item in enumerate(payload.get("actions", [])):
        path = f"actions[{index}]"
        if not isinstance(item, dict):
            add(errors, path, "必须是对象")
            continue
        for key in ("id", "action", "owner", "due", "acceptance", "stop_condition"):
            string_field(item, key, errors, path)
        if item.get("priority") not in {"P0", "P1", "P2"}:
            add(errors, f"{path}.priority", "不是 P0/P1/P2")
        if not isinstance(item.get("approval_required"), bool):
            add(errors, f"{path}.approval_required", "必须是布尔值")
        if item.get("approval_state") not in APPROVAL:
            add(errors, f"{path}.approval_state", "不是合法审批状态")
        if gate_status == "BLOCKED" and BLOCKED_ACTION_TERMS.search(str(item.get("action", ""))):
            add(errors, f"{path}.action", "BLOCKED 时不得输出预算、投放、定价、库存或发布动作")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 omni-ecom 结构化专家交接")
    parser.add_argument("input", help="handoff JSON 文件")
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        return 1
    errors = validate(payload) if isinstance(payload, dict) else ["根对象必须是 JSON 对象"]
    result = {"status": "PASS" if not errors else "FAIL", "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
