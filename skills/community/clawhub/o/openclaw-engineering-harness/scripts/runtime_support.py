from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

TEXT_SUFFIXES = {".json", ".md", ".py", ".txt", ".yaml", ".yml"}
_EMPTY_VALUES = (None, "", [], {})


def load_json_file(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON 根节点必须是对象: {path}")
    return data


def ensure_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} 必须是对象")
    return value


def ensure_string_list(value: Any, field_name: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{field_name} 必须是数组")
    return [item for item in value if isinstance(item, str)]



def is_missing_value(value: Any) -> bool:
    return value in _EMPTY_VALUES


def summarize_present_fields(request: dict[str, Any], field_names: list[str]) -> list[str]:
    return [field_name for field_name in field_names if not is_missing_value(request.get(field_name))]


def summarize_missing_fields(request: dict[str, Any], field_names: list[str]) -> list[str]:
    return [field_name for field_name in field_names if is_missing_value(request.get(field_name))]


def compile_blocked_patterns(policy: dict[str, Any]) -> list[tuple[str, re.Pattern[str]]]:
    blocked = policy.get("blocked_patterns", [])
    compiled: list[tuple[str, re.Pattern[str]]] = []
    for item in blocked:
        if not isinstance(item, dict):
            raise ValueError("blocked_patterns 项必须是对象")
        name = str(item.get("name", "unnamed-rule"))
        pattern = item.get("pattern")
        if not isinstance(pattern, str) or not pattern:
            raise ValueError(f"规则缺少 pattern: {item}")
        compiled.append((name, re.compile(pattern, re.IGNORECASE)))
    return compiled


def iter_audit_files(root: Path, policy: dict[str, Any]) -> list[Path]:
    suffixes = policy.get("text_suffixes") or sorted(TEXT_SUFFIXES)
    allowed = {suffix.lower() for suffix in suffixes if isinstance(suffix, str)}
    excluded = {
        name.lower()
        for name in policy.get("exclude_directories", [])
        if isinstance(name, str)
    }
    files: list[Path] = []
    for file_path in sorted(root.rglob("*")):
        if not file_path.is_file() or file_path.suffix.lower() not in allowed:
            continue
        relative_parts = file_path.relative_to(root).parts
        if any(part.lower() in excluded for part in relative_parts):
            continue
        files.append(file_path)
    return files


def audit_directory(root: Path, policy: dict[str, Any]) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    compiled = compile_blocked_patterns(policy)
    audit_files = iter_audit_files(root, policy)
    for file_path in audit_files:
        content = file_path.read_text(encoding="utf-8")
        for rule_name, pattern in compiled:
            for match in pattern.finditer(content):
                snippet = match.group(0).strip() or match.group(0)
                findings.append(
                    {
                        "rule": rule_name,
                        "snippet": snippet[:120],
                        "file": file_path.relative_to(root).as_posix(),
                    }
                )
                break
    return {
        "audited_root": root.name or ".",
        "audited_files": len(audit_files),
        "blocked": bool(findings),
        "findings": findings,
    }


def phase_name_map(policy: dict[str, Any]) -> dict[str, str]:
    phase_display = ensure_mapping(policy.get("phase_display", {}), "phase_display")
    return {str(key): str(value) for key, value in phase_display.items()}


def build_tool_layer(
    request: dict[str, Any],
    workflow_policy: dict[str, Any],
    tool_config: dict[str, Any],
) -> dict[str, Any]:
    groups = ensure_mapping(tool_config.get("tool_groups", {}), "tool_groups")
    phase_tool_groups = ensure_mapping(tool_config.get("phase_tool_groups", {}), "phase_tool_groups")
    phase_order = ensure_string_list(workflow_policy.get("phase_order", []), "phase_order")
    runtime = ensure_mapping(tool_config.get("runtime", {}), "runtime")

    available_tools_raw = request.get("available_tools")
    availability_known = isinstance(available_tools_raw, list) and bool(available_tools_raw)
    available_tools = {str(item) for item in available_tools_raw or [] if isinstance(item, str)}

    group_records: list[dict[str, Any]] = []
    expanded_groups: dict[str, list[str]] = {}
    for group_id in sorted(groups):
        group = ensure_mapping(groups[group_id], f"tool_groups.{group_id}")
        tools = ensure_string_list(group.get("tools", []), f"tool_groups.{group_id}.tools")
        expanded_groups[group_id] = tools
        present_tools = [tool_name for tool_name in tools if tool_name in available_tools] if availability_known else []
        missing_tools = [tool_name for tool_name in tools if tool_name not in available_tools] if availability_known else []
        group_records.append(
            {
                "id": group_id,
                "title": str(group.get("title", group_id)),
                "tools": tools,
                "availability_known": availability_known,
                "present_tools": present_tools,
                "missing_tools": missing_tools,
            }
        )

    phase_records: list[dict[str, Any]] = []
    tool_ready = True
    for phase_key in phase_order:
        group_ids = ensure_string_list(phase_tool_groups.get(phase_key, []), f"phase_tool_groups.{phase_key}")
        required_tools: list[str] = []
        missing_groups: list[str] = []
        unavailable_tools: list[str] = []
        for group_id in group_ids:
            tools = expanded_groups.get(group_id)
            if tools is None:
                missing_groups.append(group_id)
                continue
            for tool_name in tools:
                if tool_name not in required_tools:
                    required_tools.append(tool_name)
                if availability_known and tool_name not in available_tools and tool_name not in unavailable_tools:
                    unavailable_tools.append(tool_name)
        phase_ready = not missing_groups and (not availability_known or not unavailable_tools)
        tool_ready = tool_ready and phase_ready
        phase_records.append(
            {
                "phase": phase_key,
                "group_ids": group_ids,
                "required_tools": required_tools,
                "availability_known": availability_known,
                "missing_groups": missing_groups,
                "unavailable_tools": unavailable_tools,
                "ready": phase_ready,
            }
        )

    return {
        "runtime_hard_limits": {
            "skill_mode": str(runtime.get("skill_mode", "single")),
            "stdlib_only": bool(runtime.get("stdlib_only", False)),
            "no_host_text_copy": bool(runtime.get("no_host_text_copy", False)),
        },
        "availability_known": availability_known,
        "groups": group_records,
        "phases": phase_records,
        "ready": tool_ready,
    }


def build_state_layer(
    request: dict[str, Any],
    workflow_policy: dict[str, Any],
    state_policy: dict[str, Any],
) -> dict[str, Any]:
    state_order = ensure_string_list(state_policy.get("state_order", []), "state_order")
    state_display = ensure_mapping(state_policy.get("state_display", {}), "state_display")
    state_requirements = ensure_mapping(state_policy.get("state_requirements", {}), "state_requirements")
    phase_bindings = ensure_mapping(state_policy.get("phase_state_bindings", {}), "phase_state_bindings")
    required_fields = ensure_string_list(workflow_policy.get("required_fields", []), "required_fields")
    entry_state = str(state_policy.get("entry_state", state_order[0] if state_order else "intake"))

    states: list[dict[str, Any]] = []
    current_state = entry_state
    for state_key in state_order:
        required_inputs = ensure_string_list(state_requirements.get(state_key, []), f"state_requirements.{state_key}")
        missing_inputs = summarize_missing_fields(request, required_inputs)
        ready = not missing_inputs
        if ready:
            current_state = state_key
        states.append(
            {
                "id": state_key,
                "title": str(state_display.get(state_key, state_key)),
                "required_inputs": required_inputs,
                "present_inputs": summarize_present_fields(request, required_inputs),
                "missing_inputs": missing_inputs,
                "ready": ready,
            }
        )

    phase_order = ensure_string_list(workflow_policy.get("phase_order", []), "phase_order")
    missing_in_state = [phase_key for phase_key in phase_order if phase_key not in phase_bindings]
    extra_bindings = [phase_key for phase_key in phase_bindings if phase_key not in phase_order]

    return {
        "entry_state": entry_state,
        "current_state": current_state,
        "missing_core_fields": summarize_missing_fields(request, required_fields),
        "phase_alignment": {
            "missing_in_state": missing_in_state,
            "extra_bindings": extra_bindings,
        },
        "states": states,
        "ready": all(state["ready"] for state in states),
    }


def resolve_context_path(context: dict[str, Any], dotted_path: str) -> tuple[bool, Any]:
    current: Any = context
    if not dotted_path:
        return True, current
    for segment in dotted_path.split("."):
        if isinstance(current, dict) and segment in current:
            current = current[segment]
            continue
        if isinstance(current, list) and segment.isdigit():
            index = int(segment)
            if 0 <= index < len(current):
                current = current[index]
                continue
        return False, None
    return True, current


def evaluate_operator(operator: str, found: bool, actual: Any, expected: Any) -> bool:
    if operator == "equals":
        return found and actual == expected
    if operator == "empty":
        if not found:
            return False
        if actual in _EMPTY_VALUES:
            return True
        try:
            return len(actual) == 0
        except TypeError:
            return False
    if operator == "truthy":
        return found and bool(actual)
    if operator == "falsy":
        return found and not bool(actual)
    raise ValueError(f"Unsupported constraint operator: {operator}")



def evaluate_constraints(
    context: dict[str, Any],
    constraint_policy: dict[str, Any],
) -> dict[str, Any]:
    rules = constraint_policy.get("rules", [])
    if not isinstance(rules, list):
        raise ValueError("rules 必须是数组")

    evaluations: list[dict[str, Any]] = []
    blocked = False
    for rule in rules:
        if not isinstance(rule, dict):
            raise ValueError("rules 项必须是对象")
        rule_id = str(rule.get("id", "unnamed-rule"))
        title = str(rule.get("title", rule_id))
        level = str(rule.get("level", "error"))
        path = str(rule.get("path", ""))
        operator = str(rule.get("operator", "equals"))
        found, actual = resolve_context_path(context, path)
        passed = evaluate_operator(operator, found, actual, rule.get("value"))
        blocked = blocked or (level == "error" and not passed)
        evaluations.append(
            {
                "id": rule_id,
                "title": title,
                "level": level,
                "path": path,
                "operator": operator,
                "passed": passed,
                "found": found,
                "actual": actual,
                "expected": rule.get("value"),
            }
        )

    return {
        "delivery": ensure_mapping(constraint_policy.get("delivery", {}), "delivery"),
        "blocked": blocked,
        "rules": evaluations,
    }
