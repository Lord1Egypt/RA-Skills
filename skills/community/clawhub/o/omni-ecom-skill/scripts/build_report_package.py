#!/usr/bin/env python3
"""Build a traceable report package from a validated expert handoff.

This is the single input contract for downstream PDF/PPT/XLSX delivery. It
does not create new business claims; it only structures evidence-linked facts,
judgments and tracked actions. BLOCKED inputs produce a data-quality report.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CORE_SCRIPTS = ROOT / "skills" / "ecom-diagnosis-core" / "scripts"
if str(CORE_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(CORE_SCRIPTS))
from validate_handoff import validate as validate_handoff  # type: ignore  # noqa: E402
from client_registry import resolve_client_registry  # noqa: E402
from claim_guard import validate_claims  # noqa: E402
from host_runtime import valid_task_id  # noqa: E402


BLOCKED_TERMS = re.compile(r"预算|加投|投放|调价|降价|提价|库存补货|发布|利润|ROAS|净销售|增长承诺", re.I)
PATH_RE = re.compile(r"(?:[A-Za-z]:[\\/]|^[/\\])")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z]+(?:\.[0-9A-Za-z-]+)*)?$")
CLIENT_REGISTRY = resolve_client_registry(ROOT)
TASK_PROFILES = ROOT / "config" / "task-profiles.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def enforce_client_public_scope(package: dict[str, Any], markdown: str) -> None:
    """Block registered client terms that are outside this report's current scope."""
    registry = read_json(CLIENT_REGISTRY)
    terms = registry.get("registered_client_terms", []) if isinstance(registry, dict) else []
    if not isinstance(terms, list):
        raise ValueError("client_scope_leak_blocked")
    scope = package.get("scope", {}) if isinstance(package.get("scope"), dict) else {}
    allowed_text = " ".join(str(item or "") for item in (
        package.get("client_scope"), scope.get("store")
    )).casefold()
    public_text = (json.dumps(package, ensure_ascii=False) + "\n" + markdown).casefold()
    for term in terms:
        normalized = str(term).strip().casefold()
        if normalized and normalized not in allowed_text and normalized in public_text:
            raise ValueError("client_scope_leak_blocked")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_team_version(args: argparse.Namespace) -> tuple[dict[str, Any], Path]:
    version_path = Path(args.version_info).resolve() if args.version_info else ROOT / "version-info.json"
    if not version_path.is_file():
        raise ValueError(f"缺少专家团版本元数据: {version_path.name}")
    info = read_json(version_path)
    if not isinstance(info, dict):
        raise ValueError("version-info.json 根对象必须是 JSON 对象")
    team_version = str(args.team_version or info.get("team_version", ""))
    if not SEMVER_RE.fullmatch(team_version):
        raise ValueError("team_version 必须是语义化三段版本号")
    manifest_path = ROOT / ".codebuddy-plugin" / "plugin.json"
    if manifest_path.is_file():
        manifest = read_json(manifest_path)
        manifest_version = str(manifest.get("version", "")) if isinstance(manifest, dict) else ""
        if manifest_version and manifest_version != team_version:
            raise ValueError(f"版本元数据与 plugin.json 不一致: {team_version} != {manifest_version}")
    info = dict(info)
    info["team_id"] = str(info.get("team_id") or "omni-ecom")
    info["team_version"] = team_version
    info["changes"] = [str(item) for item in info.get("changes", [])]
    info["previous_version"] = str(info.get("previous_version") or "")
    info["release_name"] = str(info.get("release_name") or "版本升级")
    info["release_date"] = str(info.get("release_date") or "待确认")
    return info, version_path


def load_task_profile(task_type: str) -> dict[str, Any]:
    payload = read_json(TASK_PROFILES)
    profiles = payload.get("profiles", {}) if isinstance(payload, dict) else {}
    if not isinstance(profiles, dict) or task_type not in profiles:
        raise ValueError(f"task_type_invalid:{task_type}")
    profile = profiles[task_type]
    if not isinstance(profile, dict):
        raise ValueError(f"task_profile_invalid:{task_type}")
    required = {
        "display_name", "default_title", "period_grain", "comparison_expectation",
        "decision_focus", "default_collaboration_mode", "required_delivery", "minimum_charts",
    }
    if not required.issubset(profile) or int(profile.get("minimum_charts", 0)) < 3:
        raise ValueError(f"task_profile_invalid:{task_type}")
    return dict(profile)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_team_roster() -> list[dict[str, Any]]:
    manifest_path = ROOT / ".codebuddy-plugin" / "plugin.json"
    if not manifest_path.is_file():
        manifest_path = ROOT / "config" / "team-roster.json"
    manifest = read_json(manifest_path)
    members = manifest.get("members", []) if isinstance(manifest, dict) else []
    if not isinstance(members, list) or len(members) != 6:
        raise ValueError("专家团名册必须包含 1 位团长和 5 位成员")
    roster: list[dict[str, Any]] = []
    for item in members:
        if not isinstance(item, dict) or not item.get("id"):
            raise ValueError("专家团名册存在无效成员")
        display = item.get("displayName") or item.get("name") or {}
        profession = item.get("profession", {})
        roster.append({
            "agent_id": str(item["id"]),
            "display_name": str(display.get("zh") or display.get("en") or item["id"]),
            "profession": str(profession.get("zh") or profession.get("en") or "待确认岗位"),
            "role": str(item.get("role") or "member"),
        })
    return roster


def contribution_summary(payload: dict[str, Any]) -> str:
    explicit = str(payload.get("contribution_summary") or "").strip()
    if explicit:
        return explicit
    counts = {
        "事实": len(payload.get("facts", [])),
        "判断": len(payload.get("judgments", [])),
        "假设": len(payload.get("hypotheses", [])),
        "行动": len(payload.get("actions", [])),
    }
    return "、".join(f"{label}{count}项" for label, count in counts.items())


def load_collaboration(
    args: argparse.Namespace,
    primary: dict[str, Any],
    primary_path: Path,
) -> tuple[list[dict[str, Any]], str, list[dict[str, Any]]]:
    paths = [primary_path, *(Path(item).resolve() for item in (args.member_handoff or []))]
    unique_paths: list[Path] = []
    seen_paths: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen_paths:
            unique_paths.append(resolved)
            seen_paths.add(resolved)

    roster = load_team_roster()
    registered = {item["agent_id"] for item in roster}
    records: list[tuple[dict[str, Any], Path]] = []
    for path in unique_paths:
        payload = primary if path == primary_path else read_json(path)
        if not isinstance(payload, dict):
            raise ValueError(f"成员 handoff 根对象必须是对象: {path.name}")
        errors = validate_handoff(payload)
        if errors:
            raise ValueError(f"成员 handoff 校验失败 {path.name}: " + "；".join(errors))
        if payload.get("run_id") != primary.get("run_id"):
            raise ValueError(f"成员 handoff run_id 不一致: {path.name}")
        if payload.get("scope") != primary.get("scope"):
            raise ValueError(f"成员 handoff scope 不一致: {path.name}")
        agent_id = str(payload.get("agent_id", ""))
        if agent_id not in registered:
            raise ValueError(f"成员 handoff 使用未注册 Agent: {agent_id}")
        records.append((payload, path))

    contributed_ids = {str(payload.get("agent_id")) for payload, _ in records}
    if args.collaboration_mode == "comprehensive":
        if primary.get("agent_id") != "omni-ecom-team-lead":
            raise ValueError("collaboration_incomplete: 综合报告的主 handoff 必须由 omni-ecom-team-lead 提交")
        missing = [agent_id for agent_id in ("omni-ecom-team-lead", "data-analyst") if agent_id not in contributed_ids]
        if primary.get("gate_status") != "BLOCKED":
            for agent_id in ("platform-ops", "content-live-growth", "ad-profit-optimizer"):
                if agent_id not in contributed_ids:
                    missing.append(agent_id)
        if missing:
            raise ValueError(
                "collaboration_incomplete: 综合报告缺少 " + "、".join(missing)
                + " 的独立交接；不能生成综合报告。请通过 --member-handoff 提供同一 run_id 的成员 handoff"
            )
        missing_task_ids = sorted({
            str(payload.get("agent_id"))
            for payload, _ in records
            if payload.get("agent_id") != "omni-ecom-team-lead"
            and not valid_task_id(payload.get("agent_task_id"))
        })
        if missing_task_ids:
            raise ValueError(
                "collaboration_untraceable: 综合报告成员缺少真实宿主返回的 agent_task_id："
                + "、".join(missing_task_ids)
                + "；不能证明存在可单独查看的成员子任务"
            )
        unreturned = sorted({
            str(payload.get("agent_id"))
            for payload, _ in records
            if payload.get("agent_id") != "omni-ecom-team-lead"
            and (
                payload.get("agent_return_status") != "completed"
                or not str(payload.get("agent_returned_at") or "").strip()
                or not str(payload.get("agent_return_file") or "").endswith(".return.json")
                or len(str(payload.get("agent_return_sha256") or "")) != 64
            )
        })
        if unreturned:
            raise ValueError(
                "collaboration_unreturned: 综合报告成员缺少完整回传闩锁凭证："
                + "、".join(unreturned)
                + "；主任务不得在子 Agent 未真实回传时完成"
            )
        if "delivery-review" in contributed_ids:
            raise ValueError(
                "review_order_invalid: 报告候选稿必须在 delivery-review 之前冻结；"
                "不得把旧复核 handoff 写入后来生成或改写的报告"
            )
        collaboration_status = "verified_data_gate" if primary.get("gate_status") == "BLOCKED" else "awaiting_delivery_review"
    else:
        collaboration_status = "single_point"

    participation: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []
    for member in roster:
        agent_records = [(payload, path) for payload, path in records if payload.get("agent_id") == member["agent_id"]]
        handoff_files = [path.name for _, path in agent_records]
        hashes = [file_sha256(path) for _, path in agent_records]
        summaries = [contribution_summary(payload) for payload, _ in agent_records]
        task_ids = sorted({
            str(payload.get("agent_task_id"))
            for payload, _ in agent_records
            if payload.get("agent_task_id")
        })
        view_urls = sorted({
            str(payload.get("agent_view_url"))
            for payload, _ in agent_records
            if payload.get("agent_view_url")
        })
        item = dict(member)
        pending_review = (
            not agent_records and member["agent_id"] == "delivery-review"
            and args.collaboration_mode == "comprehensive"
        )
        item.update({
            "participation_status": "contributed" if agent_records else ("pending_review" if pending_review else "not_invoked"),
            "agent_task_ids": task_ids,
            "agent_view_urls": view_urls,
            "contribution_summary": "；".join(summaries) if summaries else (
                "等待报告候选稿冻结后独立复核" if pending_review else "本次未调度（无 handoff 证据）"
            ),
            "handoff_files": handoff_files,
            "handoff_sha256": hashes,
            "agent_versions": sorted({str(payload.get("agent_version")) for payload, _ in agent_records}),
            "agent_return_statuses": sorted({str(payload.get("agent_return_status")) for payload, _ in agent_records if payload.get("agent_return_status")}),
            "agent_returned_at": sorted({str(payload.get("agent_returned_at")) for payload, _ in agent_records if payload.get("agent_returned_at")}),
            "agent_return_files": sorted({str(payload.get("agent_return_file")) for payload, _ in agent_records if payload.get("agent_return_file")}),
        })
        participation.append(item)
        for (payload, path), digest in zip(agent_records, hashes):
            sources.append({
                "type": "expert_handoff",
                "agent_id": payload.get("agent_id"),
                "source": path.name,
                "sha256": digest,
                "status": payload.get("status"),
                "agent_task_id": payload.get("agent_task_id"),
                "agent_view_url": payload.get("agent_view_url"),
                "agent_return_status": payload.get("agent_return_status"),
                "agent_returned_at": payload.get("agent_returned_at"),
                "agent_return_file": payload.get("agent_return_file"),
                "agent_return_sha256": payload.get("agent_return_sha256"),
            })
    return participation, collaboration_status, sources


def safe_scope(value: str) -> str:
    value = value.strip()
    if not value or PATH_RE.search(value) or ".." in value:
        raise ValueError("client_scope 不能是绝对路径或包含 ..")
    return value


def source_label(value: Any, base: Path | None = None) -> tuple[str, str | None]:
    """Return a public source label and optional SHA256 without exposing a path."""
    text = str(value or "unknown-source")
    candidate = Path(text)
    if not candidate.is_absolute() and base:
        candidate = (base / candidate).resolve()
    digest: str | None = None
    if candidate.is_file():
        try:
            digest = hashlib.sha256(candidate.read_bytes()).hexdigest()
        except OSError:
            digest = None
        return candidate.name, digest
    return Path(text.replace("\\", "/")).name or "unknown-source", digest


def sanitize(value: Any, base: Path | None = None, key: str = "") -> Any:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for item_key, item_value in value.items():
            if item_key in {"source", "file", "path", "source_path", "input_path"}:
                label, digest = source_label(item_value, base)
                result[item_key] = label
                if digest:
                    result[f"{item_key}_sha256"] = digest
            else:
                result[item_key] = sanitize(item_value, base, item_key)
        return result
    if isinstance(value, list):
        return [sanitize(item, base, key) for item in value]
    if isinstance(value, str) and PATH_RE.search(value):
        return source_label(value, base)[0]
    return value


def load_actions(args: argparse.Namespace, handoff: dict[str, Any]) -> list[dict[str, Any]]:
    paths = [Path(item).resolve() for item in (args.action or [])]
    if args.actions_dir:
        directory = Path(args.actions_dir).resolve()
        if directory.is_dir():
            paths.extend(path for path in sorted(directory.glob("A*.json")) if not path.name.endswith(".approval.json"))
    actions: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in paths:
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise ValueError(f"行动文件根对象必须是对象: {path.name}")
        action_id = str(payload.get("action_id", ""))
        if action_id in seen:
            continue
        if payload.get("run_id") != handoff.get("run_id"):
            raise ValueError(f"行动 run_id 与 handoff 不一致: {action_id}")
        if payload.get("client_scope") != args.client_scope:
            raise ValueError(f"行动 client_scope 与当前运行不一致: {action_id}")
        seen.add(action_id)
        actions.append({
            "action_id": action_id,
            "priority": payload.get("priority"),
            "action": payload.get("action"),
            "owner": payload.get("owner"),
            "target": payload.get("target"),
            "baseline": payload.get("baseline", ""),
            "acceptance": payload.get("acceptance"),
            "stop_condition": payload.get("stop_condition"),
            "approval_required": bool(payload.get("approval_required")),
            "approval_state": payload.get("approval_state"),
            "status": payload.get("status"),
            "outcome": payload.get("outcome"),
            "source_ids": payload.get("source_ids", []),
            "artifact_refs": [Path(str(item)).name for item in payload.get("artifact_refs", [])],
            "record_file": path.name,
        })
    return actions


def action_from_handoff(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "action_id": item.get("id"),
        "priority": item.get("priority"),
        "action": item.get("action"),
        "owner": item.get("owner"),
        "due": item.get("due", "待指定"),
        "target": item.get("target", "待指定"),
        "baseline": item.get("baseline", ""),
        "acceptance": item.get("acceptance"),
        "stop_condition": item.get("stop_condition"),
        "approval_required": item.get("approval_required"),
        "approval_state": item.get("approval_state"),
        "status": "pending_approval" if item.get("approval_state") == "pending" else ("proposed" if item.get("approval_state") == "not_required" else item.get("approval_state")),
        "outcome": None,
        "source_ids": item.get("evidence_ids", []),
        "artifact_refs": [],
        "record_file": None,
    }


def merge_actions(handoff: dict[str, Any], tracked: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tracked_by_id = {str(item.get("action_id")): item for item in tracked}
    merged: list[dict[str, Any]] = []
    for item in handoff.get("actions", []):
        base = action_from_handoff(item)
        record = tracked_by_id.get(str(base["action_id"]))
        if record:
            base.update(record)
        merged.append(base)
    for item in tracked:
        if not any(str(existing.get("action_id")) == str(item.get("action_id")) for existing in merged):
            merged.append(item)
    return merged


def content_ready(handoff: dict[str, Any], actions: list[dict[str, Any]]) -> bool:
    if handoff.get("status") != "ready_for_review" or handoff.get("gate_status") == "BLOCKED":
        return False
    for action in actions:
        if not action.get("acceptance") or not action.get("stop_condition"):
            return False
        if action.get("approval_required") and action.get("approval_state") == "pending":
            return False
    return True


def safe_blocked_actions(actions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # In a data-only report retain only evidence/data remediation actions.
    allowed = re.compile(r"补|核|校验|映射|导出|去重|口径|字段|数据|证据", re.I)
    return [item for item in actions if allowed.search(str(item.get("action", ""))) and not BLOCKED_TERMS.search(str(item.get("action", "")))]


def build_package(args: argparse.Namespace) -> tuple[dict[str, Any], str]:
    handoff_path = Path(args.handoff).resolve()
    handoff = read_json(handoff_path)
    if not isinstance(handoff, dict):
        raise ValueError("handoff 根对象必须是 JSON 对象")
    errors = validate_handoff(handoff)
    if errors:
        raise ValueError("handoff 校验失败: " + "；".join(errors))
    team_info, team_info_path = load_team_version(args)
    task_profile = load_task_profile(args.task_type)
    claim_path = Path(args.claim_ledger).resolve() if args.claim_ledger else None
    if claim_path is None or not claim_path.is_file():
        raise ValueError("claim_ledger_required")
    report_root=Path(args.output_dir).resolve()
    if not claim_path.is_relative_to(report_root):
        raise ValueError('claim_ledger_must_be_inside_report_directory')
    claim_payload = read_json(claim_path)
    claim_errors, claim_counts = validate_claims(claim_payload)
    if claim_errors:
        raise ValueError("claim_guard_blocked: " + ";".join(claim_errors))
    if claim_payload.get("created_by_team_version") != team_info["team_version"]:
        raise ValueError("claim_team_version_mismatch")
    from claim_source_guard import validate_sources
    claim_source_checks = validate_sources(claim_payload, claim_path.parent)
    if claim_payload.get("run_id") != handoff.get("run_id"):
        raise ValueError("claim_run_id_mismatch")
    claim_period = str(claim_payload.get("period") or "")
    handoff_period = str(handoff.get("scope", {}).get("period") or "")
    if claim_period and handoff_period and claim_period != handoff_period:
        raise ValueError("claim_period_mismatch")
    if task_profile["default_collaboration_mode"] == "comprehensive" and args.collaboration_mode != "comprehensive":
        raise ValueError(f"task_profile_requires_comprehensive:{args.task_type}")
    participation, collaboration_status, collaboration_sources = load_collaboration(args, handoff, handoff_path)
    client_scope = safe_scope(args.client_scope)
    config: dict[str, Any] = {}
    if args.config:
        config = read_json(Path(args.config).resolve())
        if not isinstance(config, dict):
            raise ValueError("report config 必须是 JSON 对象")
    tracked = load_actions(args, handoff)
    actions = merge_actions(handoff, tracked)
    gate = handoff["gate_status"]
    ready = content_ready(handoff, actions)
    status = "data_blocked" if gate == "BLOCKED" else "draft_diagnosis"
    period = str(handoff.get("scope", {}).get("period", "待确认"))
    platform_label = str(handoff.get("scope", {}).get("platform", "全域"))
    title = str(config.get("title") or f"{platform_label}{task_profile['default_title']}")
    metrics: list[Any] = []
    sources: list[dict[str, Any]] = []
    version_label, version_digest = source_label(team_info_path, team_info_path.parent)
    sources.append({"type": "team_version", "source": version_label, "sha256": version_digest, "status": "verified", "team_version": team_info["team_version"]})
    sources.extend(collaboration_sources)
    if args.metrics:
        metrics_payload = read_json(Path(args.metrics).resolve())
        if not isinstance(metrics_payload, dict):
            raise ValueError("metrics 必须是 JSON 对象")
        if gate != "BLOCKED":
            metrics = sanitize(metrics_payload.get("rows", metrics_payload.get("metrics", [])), Path(args.metrics).resolve().parent)
        label, digest = source_label(metrics_payload.get("source", Path(args.metrics).name), Path(args.metrics).resolve().parent)
        sources.append({"type": "metrics", "source": label, "sha256": digest, "status": metrics_payload.get("gate_status", "unknown")})
    evidence = []
    for item in handoff.get("evidence_ledger", []):
        item_copy = dict(sanitize(item, handoff_path.parent))
        label, digest = source_label(item.get("source"), handoff_path.parent)
        item_copy["source"] = label
        if digest:
            item_copy["source_sha256"] = digest
        evidence.append(item_copy)
        sources.append({"type": "evidence", "id": item.get("id"), "source": label, "sha256": digest, "status": item.get("status")})
    if gate == "BLOCKED":
        facts = [item for item in handoff.get("facts", []) if not BLOCKED_TERMS.search(str(item.get("claim", "")))]
        judgments: list[Any] = []
        hypotheses: list[Any] = []
        actions = safe_blocked_actions(actions)
        metrics = []
    else:
        facts = handoff.get("facts", [])
        judgments = handoff.get("judgments", [])
        hypotheses = handoff.get("hypotheses", [])
    from artifact_contract import native_report_identity
    package: dict[str, Any] = {
        **native_report_identity(team_info["team_version"], handoff.get("schema_version"), claim_payload.get("schema_version")),
        "team_id": team_info["team_id"],
        "team_version": team_info["team_version"],
        "team_maintenance_revision": team_info.get("maintenance_revision"),
        "team_version_label": f"{team_info['team_id']} 专家团 v{team_info['team_version']}",
        "team_release_name": team_info["release_name"],
        "team_release_date": team_info["release_date"],
        "team_previous_version": team_info["previous_version"],
        "team_version_changes": team_info["changes"],
        "version_diff": {
            "from": team_info["previous_version"],
            "to": team_info["team_version"],
            "release_name": team_info["release_name"],
            "changes": team_info["changes"],
            "compatibility": team_info.get("compatibility", {}),
        },
        "report_revision": args.report_revision,
        "task_type": args.task_type,
        "task_profile": sanitize(task_profile, TASK_PROFILES.parent),
        "review_stage": "awaiting_delivery_review" if args.collaboration_mode == "comprehensive" else "not_required",
        "collaboration_mode": args.collaboration_mode,
        "collaboration_status": collaboration_status,
        "expert_participation": participation,
        "run_id": handoff["run_id"],
        "client_scope": client_scope,
        "gate_status": gate,
        "status": status,
        "title": title,
        "period": period,
        "scope": sanitize(handoff.get("scope", {}), handoff_path.parent),
        "generated_at": now(),
        "data_gate": {
            "status": gate,
            "delivery_status": status,
            "missing_data": handoff.get("missing_data", []),
            "risks": handoff.get("risks", []),
            "blocked_report": gate == "BLOCKED",
        },
        "claim_ledger": {
            "file": str(claim_path.relative_to(report_root)),
            "sha256": file_sha256(claim_path),
            **claim_counts,
            "source_checks": claim_source_checks,
            "claims": sanitize(claim_payload.get("claims", []), claim_path.parent),
        },
        "metrics": metrics,
        "facts": sanitize(facts, handoff_path.parent),
        "judgments": sanitize(judgments, handoff_path.parent),
        "hypotheses": sanitize(hypotheses, handoff_path.parent),
        "actions": sanitize(actions, handoff_path.parent),
        "missing_data": handoff.get("missing_data", []),
        "risks": handoff.get("risks", []),
        "sources": sources,
        "provenance": {
            "handoff_file": handoff_path.name,
            "handoff_agent_id": handoff.get("agent_id"),
            "handoff_agent_version": handoff.get("agent_version"),
            "evidence_ids": [item.get("id") for item in evidence if item.get("id")],
            "action_ids": [item.get("action_id") for item in actions if item.get("action_id")],
            "generated_by": "build_report_package.py",
            "team_version_source": version_label,
            "expert_handoff_agents": [item["agent_id"] for item in participation if item["participation_status"] == "contributed"],
            "expert_handoff_sha256": [digest for item in participation for digest in item["handoff_sha256"]],
        },
    }
    from previous_action_review import load_feedback
    feedback = load_feedback(getattr(args,'previous_action_review',None),
                             package['run_id'],client_scope,package['team_version'],report_root)
    if feedback is not None:
        package['previous_action_review']=feedback
        sources.append({'type':'previous_action_feedback','source':feedback['source_file'],
                        'sha256':feedback['source_sha256'],'status':feedback['status']})
    from data_quality_report_guard import validate_data_quality_report
    package["data_quality_scope_gate"] = validate_data_quality_report(package)
    stage0_sources = {
        "report_inventory": args.report_inventory,
        "report_clusters": args.report_clusters,
        "chapter_plan": args.chapter_plan,
        "coverage": args.coverage_gate,
    }
    stage0 = {"status": "stage0_missing", "report_count": 0, "cluster_count": 0,
              "chapter_count": 0, "coverage_rate": 0.0}
    stage0_loaded: dict[str, Any] = {}
    for key, raw in stage0_sources.items():
        if not raw:
            continue
        candidate = Path(raw)
        if not candidate.exists():
            continue
        stage0_loaded[key] = json.loads(candidate.read_text(encoding="utf-8"))
        stage0[f"{key}_sha256"] = file_sha256(candidate)
    if len(stage0_loaded) == 4:
        stage0.update({
            "status": "stage0_complete",
            "report_count": stage0_loaded["report_inventory"].get("report_count", 0),
            "cluster_count": stage0_loaded["report_clusters"].get("cluster_count", 0),
            "chapter_count": len(stage0_loaded["chapter_plan"].get("chapters", [])),
            "coverage_rate": stage0_loaded["coverage"].get("stats", {}).get("coverage_rate", 0.0),
        })
    package["stage0"] = stage0
    for key in ("report_inventory", "report_clusters", "chapter_plan", "coverage"):
        if key in stage0_loaded:
            package[key] = stage0_loaded[key]

    quality_root = Path(args.output_dir).resolve()
    baseline_path = quality_root / "baseline-pack.json"
    depth_path = quality_root / "depth-guard.json"
    conflict_path = quality_root / "conflict-scan.json"
    verdict_path = quality_root / "conflict-verdict.json"
    if baseline_path.is_file() and depth_path.is_file() and conflict_path.is_file():
        depth_payload = json.loads(depth_path.read_text(encoding="utf-8-sig"))
        conflict_payload = json.loads(conflict_path.read_text(encoding="utf-8-sig"))
        conflict_summary = conflict_payload.get("summary", {})
        verdict_payload = json.loads(verdict_path.read_text(encoding="utf-8-sig")) if verdict_path.is_file() else {}
        package["collaboration_quality"] = {
            "baseline_sha256": file_sha256(baseline_path),
            "depth_guard_status": depth_payload.get("status"),
            "agent_depth": [{key: item.get(key) for key in ("agent_id", "reached_level", "required_level", "gate_status", "status")} for item in depth_payload.get("results", [])],
            "conflict_scan_status": conflict_payload.get("status"),
            "hard_conflict_count": int(conflict_summary.get("hard", 0)),
            "soft_conflict_count": int(conflict_summary.get("soft", 0)),
            "challenge_round_status": "required" if conflict_summary.get("needs_challenge_round") else "not_required",
            "lead_recomputation_status": "required" if conflict_summary.get("lead_recomputation_required") else "not_required",
            "adjudication_count": len(verdict_payload.get("verdicts", [])) if isinstance(verdict_payload.get("verdicts", []), list) else 0,
        }
        for label, path in (("analysis_baseline", baseline_path), ("analysis_depth_guard", depth_path), ("conflict_scan", conflict_path)):
            package["sources"].append({"type": label, "source": path.name, "sha256": file_sha256(path), "status": "verified"})

    from decision_display import auto_attach
    auto_attach(package,args.output_dir,getattr(args,'decision_pack',None))
    from report_metric_guard import validate_delivery_metrics as validate_report_metrics
    if client_scope == 'runtime-acceptance-no-client-data':
        package['acceptance_only'] = True
        package['acceptance_notice'] = '仅为无客户机制验收；PASS 只指机制，客户经营数据缺失（经营 BLOCKED）。透明固定测试值仅检验复算和图表，不是实际经营表现，不得作为经营建议。'
        findings = []
        from mechanism_fact_guard import validate as validate_mechanism
        for member_path in args.member_handoff or []:
            member = read_json(Path(member_path).resolve())
            bindings = validate_mechanism(member.get('facts', []), package)
            findings.append({'agent_id': member['agent_id'], 'gate_status': member['gate_status'],
                             'facts': sanitize(member.get('facts', []), Path(member_path).resolve().parent),
                             'missing_data': sanitize(member.get('missing_data', []), Path(member_path).resolve().parent),
                             'source_bound_structural_counts': bindings})
        package['mechanism_findings'] = findings
        from acceptance_report_view import enrich
        enrich(package)
    validate_report_metrics(package)
    from narrative_value_guard import validate_narrative_numbers
    package['narrative_value_gate']=validate_narrative_numbers(package)
    from artifact_contract import validate_native_report
    package['artifact_contract_gate']=validate_native_report(package)
    markdown = render_markdown(package, config)
    enforce_client_public_scope(package, markdown)
    return package, markdown


def strip_tag(claim: Any) -> str:
    """Drop a leading 【...】 tag so callers can prefix without doubling it."""
    text = str(claim or "").strip()
    return re.sub(r"^【[^】]*】\s*", "", text)


def number_basis(item: dict[str, Any]) -> str:
    parts=[]
    for row in item.get('number_bindings',[]):
        if row.get('kind')=='claim': parts.append(f"{row.get('token')}→{row.get('claim_id')}")
        else: parts.append(f"{row.get('token')}→待验证{row.get('label')}（依据：{','.join(row.get('basis_claim_ids',[]))}）")
    return '；数字依据：'+'；'.join(parts) if parts else ''


def render_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(", ", ": "))
    return str(value)


def markdown_cell(value: Any) -> str:
    return render_value(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(package: dict[str, Any], config: dict[str, Any]) -> str:
    if package.get('acceptance_only'):
        from acceptance_report_view import markdown
        return markdown(package)
    blocked = package["gate_status"] == "BLOCKED"
    lines = [
        f"# {package['title']}",
        "",
        f"- 专家团版本：**{package['team_version_label']}**",
        f"- 版本发布日期：{package['team_release_date']}",
        f"- 版本基线：{package['team_previous_version'] or '首发'}",
        f"- 运行：`{package['run_id']}`",
        f"- 客户范围：{package['client_scope']}",
        f"- 期间：{package['period']}",
        f"- 数据闸门：**{package['gate_status']}**",
        f"- 交付状态：**{package['status']}**",
        "",
    ]
    from report_presentation import view
    presentation=view(package)
    package['presentation']=presentation
    lines.extend(['## 经营摘要与本次重点','', '；'.join(presentation['focus']), '',
                  '比较要求：'+str(presentation['comparison_expectation'] or '按已提供同口径资料比较'), ''])
    for item in (package.get('judgments') or package.get('facts') or [])[:3]:
        lines.append('- '+strip_tag(item.get('claim'))+number_basis(item))
    if package.get('task_type')=='weekly_report':
        from previous_action_review import feedback_lines
        lines.extend(['','上次行动回验：',*feedback_lines(package.get('previous_action_review'))])
    if package.get('team_maintenance_revision'):
        lines.extend(['','专家团维护批次：'+str(package['team_maintenance_revision'])])
    lines.extend(['', '完整分析、行动及资料覆盖见后续正文与附录。', ''])
    lines.extend(["## 版本信息", "", f"本报告由 **{package['team_version_label']}** 生成，报告修订号：**{package['report_revision']}**；任务类型：**{package['task_profile']['display_name']}**；发布说明：{package['team_release_name']}。", ""])
    if package.get('acceptance_only'):
        lines.extend(['> '+package['acceptance_notice'], ''])
    if package.get("review_stage") == "awaiting_delivery_review":
        lines.extend(["> 候选版本仅可记录 candidate_pipeline_complete，以 candidate-acceptance-receipt.json 为依据，不构成正式交付。" if '-candidate.' in package['team_version'] else "> 当前文件是待冻结和独立复核的候选稿；独立复核状态见 `release-receipt.json`，正式完成状态以 `completion-receipt.json` 为准。冻结后不得继续修改该稿。", ""])
    if package.get("team_version_changes"):
        lines.append("本次相对上一版本的变更：")
        lines.extend(f"- {item}" for item in package["team_version_changes"])
        lines.append("")
    inventory = package.get("report_inventory", {})
    clusters = package.get("report_clusters", {})
    chapter_plan = package.get("chapter_plan", {})
    if package.get("stage0", {}).get("status") == "stage0_complete":
        lines.extend(["## 数据概览与覆盖", "", "### 报表清单", "", "| 报表编号 | 文件 | 类型 | 期间 | 可分析性 |", "| --- | --- | --- | --- | --- |"])
        for item in inventory.get("reports", []):
            scope = item.get("time_scope", {})
            period = scope.get("note") or " ~ ".join(str(scope.get(key) or "") for key in ("start", "end"))
            lines.append(f"| {markdown_cell(item.get('report_id'))} | {markdown_cell(item.get('file_name'))} | {markdown_cell(item.get('report_type_label') or item.get('report_type'))} | {markdown_cell(period)} | {markdown_cell(item.get('verdict'))} |")
        lines.extend(["", "### 归类结果", "", "| 归类编号 | 业务域 | 名称 | 包含报表 | 状态 |", "| --- | --- | --- | --- | --- |"])
        for item in clusters.get("clusters", []):
            lines.append(f"| {markdown_cell(item.get('cluster_id'))} | {markdown_cell(item.get('domain'))} | {markdown_cell(item.get('label'))} | {markdown_cell(', '.join(item.get('members', [])))} | {markdown_cell(item.get('sufficiency'))} |")
        lines.extend(["", "### 章节与报表映射", "", "| 章节 | 标题 | 负责人 | 来源报表 |", "| --- | --- | --- | --- |"])
        for item in chapter_plan.get("chapters", []):
            lines.append(f"| {markdown_cell(item.get('chapter_id'))} | {markdown_cell(item.get('title'))} | {markdown_cell(item.get('owner_agent'))} | {markdown_cell(', '.join(item.get('source_report_ids', [])) or '无直接报表')} |")
        lines.append("")
    lines.extend([
        "## 本次专家协作记录",
        "",
        f"- 协作模式：`{package['collaboration_mode']}`",
        f"- 协作状态：`{package['collaboration_status']}`",
        "",
        "| 专家 | 岗位 | 本次状态 | Agent 子任务 | 回传状态/时间 | 贡献摘要 | handoff 证据 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    for item in package.get("expert_participation", []):
        handoff_refs = ", ".join(
            f"{name} / {digest[:12]}…" for name, digest in zip(item.get("handoff_files", []), item.get("handoff_sha256", []))
        ) or "无"
        reviewer_pending = item.get("agent_id") == "delivery-review" and item.get("participation_status") == "not_invoked"
        display_status = "awaiting_delivery_review" if reviewer_pending else item.get("participation_status", "")
        task_refs = ("候选稿冻结后启动" if reviewer_pending else
                     ", ".join(f"`{task_id}`" for task_id in item.get("agent_task_ids", [])) or "主任务/无独立子任务")
        return_refs = ("待独立复核" if reviewer_pending else
                       ", ".join(item.get("agent_return_statuses", [])) or "主任务")
        returned_at = ", ".join(item.get("agent_returned_at", []))
        if returned_at:
            return_refs += f" / {returned_at}"
        lines.append(
            f"| {markdown_cell(item.get('display_name', ''))} (`{markdown_cell(item.get('agent_id', ''))}`) "
            f"| {markdown_cell(item.get('profession', ''))} | `{markdown_cell(display_status)}` "
            f"| {task_refs} | {markdown_cell(return_refs)} | {markdown_cell(item.get('contribution_summary', ''))} | {markdown_cell(handoff_refs)} |"
        )
    lines.append("")
    quality = package.get("collaboration_quality", {})
    for item in package.get('mechanism_findings', []):
        lines.extend(['### '+item['agent_id']+' 独立机制核查', '', '岗位闸门：'+item['gate_status'], ''])
        for fact in item['facts']:
            lines.append('- '+strip_tag(fact.get('claim'))+'（证据：'+', '.join(fact.get('evidence_ids', []))+'）')
        lines.extend('- 未验证范围：'+str(missing) for missing in item.get('missing_data', []))
        lines.append('')
    if quality:
        lines.extend(["### 协作质量记录", "", f"- 共享基线 SHA256：`{quality.get('baseline_sha256', '')}`", f"- 深度闸门：`{quality.get('depth_guard_status', '')}`", "", "| 专家 | 达到层级 | 要求层级 | 数据闸门 | 深度状态 |", "| --- | --- | --- | --- | --- |"])
        for item in quality.get("agent_depth", []):
            lines.append(f"| {markdown_cell(item.get('agent_id'))} | {markdown_cell(item.get('reached_level'))} | {markdown_cell(item.get('required_level'))} | {markdown_cell(item.get('gate_status'))} | {markdown_cell(item.get('status'))} |")
        lines.extend(["", f"- 冲突扫描：`{quality.get('conflict_scan_status', '')}`；hard={quality.get('hard_conflict_count', 0)}，soft={quality.get('soft_conflict_count', 0)}", f"- 质疑轮：`{quality.get('challenge_round_status', '')}`", f"- 团长复算：`{quality.get('lead_recomputation_status', '')}`；裁决条目：{quality.get('adjudication_count', 0)}", ""])
    if blocked:
        lines.extend(["> 当前为数据质量报告。以下内容不构成利润、预算、投放、定价、库存或增长结论。", ""])
    from decision_display import markdown as decision_markdown
    lines.extend(decision_markdown(package))
    lines.extend(["## 一、摘要", ""])
    if blocked:
        lines.append("- 仅保留可确认事实、数据风险和补数动作；完成补数并重新通过闸门后再生成经营判断。")
    else:
        for item in package.get("facts", [])[:5]:
            lines.append(f"- 【事实】{strip_tag(item.get('claim'))}（证据：{', '.join(item.get('evidence_ids', []))}）{number_basis(item)}")
        for item in package.get("judgments", [])[:5]:
            lines.append(f"- 【判断/{item.get('confidence', '待定')}】{strip_tag(item.get('claim'))}（证据：{', '.join(item.get('evidence_ids', []))}）{number_basis(item)}")
    lines.extend(["", "## 二、数据闸门与指标", ""])
    lines.extend(['### 完整事实清单',''])
    for item in package.get('facts',[]):
        lines.append('- '+strip_tag(item.get('claim'))+'（证据：'+', '.join(item.get('evidence_ids',[]))+'）'+number_basis(item))
    if package.get("metrics"):
        lines.extend(["| 期间 | 指标", "| --- | --- |"])
        for item in package["metrics"]:
            if isinstance(item, dict):
                period = item.get("period", "")
                metrics = item.get("metrics", item)
                lines.append(f"| {period} | `{render_value(metrics)}` |")
    else:
        lines.append("暂无可用于经营判断的批准指标。")
    if package.get("missing_data"):
        lines.extend(["", "待补数据："])
        lines.extend(f"- {item}" for item in package["missing_data"])
    claim_ledger = package.get("claim_ledger", {})
    claim_rows = claim_ledger.get("claims", []) if isinstance(claim_ledger, dict) else []
    lines.extend(["", "## 数字来源与公式", "", f"- 数字来源闸门：`claim_guard`；索引文件：`{claim_ledger.get('file', 'claim-ledger.json')}`；条目数：{claim_ledger.get('claims_count', 0)}", "", "| Claim ID | 指标 | 数值 | 状态 | 来源字段 | 公式/归因 |", "| --- | --- | ---: | --- | --- | --- |"])
    for claim in claim_rows:
        if not isinstance(claim, dict):
            continue
        source = claim.get("source_ref", {}) if isinstance(claim.get("source_ref"), dict) else {}
        formula = claim.get("formula", {}) if isinstance(claim.get("formula"), dict) else {}
        formula_text = str(formula.get("expression") or "—")
        attribution = claim.get("attribution", {}) if isinstance(claim.get("attribution"), dict) else {}
        if attribution.get("source_id"):
            formula_text += f"；归因={attribution.get('source_id')}/{attribution.get('window')}"
        source_text = "/".join(str(source.get(key) or "") for key in ("source_file", "sheet", "range", "field") if source.get(key))
        lines.append(f"| {markdown_cell(claim.get('claim_id'))} | {markdown_cell(claim.get('metric'))} | {markdown_cell(claim.get('value'))} | {markdown_cell(claim.get('status'))} | {markdown_cell(source_text)} | {markdown_cell(formula_text)} |")
    if package.get("judgments"):
        lines.extend(["", "## 三、经营判断与限制", ""])
        for item in package["judgments"]:
            lines.append(f"- {item.get('claim', '')}；置信度：{item.get('confidence', '待定')}；反证条件：{'; '.join(item.get('counter_conditions', []))}{number_basis(item)}")
    if package.get("hypotheses"):
        lines.extend(["", "## 四、待验证假设", ""])
        for item in package["hypotheses"]:
            conditions = item.get('counter_conditions', [])
            qualification = f"；反证条件：{'; '.join(conditions)}" if conditions else ""
            lines.append(f"- {item.get('claim', '')}；验证：{item.get('verification_method', '')}{qualification}{number_basis(item)}")
    lines.extend(["", "## 五、行动与审批", ""])
    if package.get("actions"):
        lines.extend(["| ID | 优先级 | 动作 | 负责人 | 到期 | 审批 | 状态 | 验收 | 停止条件 | 数字依据 |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"])
        for item in package["actions"]:
            values={key:render_value(item.get(key,"")) for key in ("action_id","priority","action","owner","due","approval_state","status","acceptance","stop_condition")}
            values['number_basis']=render_value(number_basis(item).removeprefix('；数字依据：') or '—')
            lines.append("| {action_id} | {priority} | {action} | {owner} | {due} | {approval_state} | {status} | {acceptance} | {stop_condition} | {number_basis} |".format(**values))
    else:
        lines.append("暂无可执行行动；BLOCKED 状态只保留数据补齐动作。")
    if package.get("risks"):
        lines.extend(["", "## 六、风险与来源", ""])
        lines.extend(f"- 风险：{item}" for item in package["risks"])
    else:
        lines.extend(["", "## 六、来源索引", ""])
    for item in package.get("sources", []):
        suffix = f"，SHA256：`{item['sha256']}`" if item.get("sha256") else ""
        lines.append(f"- {item.get('id') or item.get('type')}: {item.get('source', '')}{suffix}")
    lines.extend(["", "---", "本文件由结构化交接包生成；未将草稿、审批中或未验证动作写成已执行。", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="从结构化 handoff 生成可追溯报告包")
    parser.add_argument("--handoff", required=True)
    parser.add_argument("--client-scope", required=True)
    parser.add_argument("--metrics")
    parser.add_argument('--previous-action-review',help='用户明确提供的上期行动反馈 JSON；核对本次客户/运行/版本，不自动认定已验收')
    parser.add_argument("--decision-pack", help="兼容显式指定；默认读取输出目录 quality-inputs.json 的 adjudication，显式文件不得与其冲突")
    parser.add_argument("--action", action="append")
    parser.add_argument("--actions-dir")
    parser.add_argument("--config")
    parser.add_argument("--version-info", help="专家团版本元数据 JSON；默认读取插件根目录 version-info.json")
    parser.add_argument("--team-version", help="显式覆盖版本元数据中的 team_version，并仍校验 plugin.json")
    parser.add_argument("--collaboration-mode", choices=["comprehensive", "single_point"], default="comprehensive", help="综合报告默认强制多 Agent 交接；单点任务必须显式选择 single_point")
    parser.add_argument("--task-type", default="store_diagnosis", help="任务类型：store_diagnosis/weekly_report/monthly_report/quarterly_report/annual_report/campaign_review/data_quality_audit/single_topic")
    parser.add_argument("--report-revision", default="R1", help="报告修订号，使用 R1/R2...；不得与专家团版本号混用")
    parser.add_argument("--report-inventory", help="Stage 0 报表清单 JSON（report_triage.py 产出）")
    parser.add_argument("--report-clusters", help="Stage 0 归类结果 JSON（cluster_reports.py 产出）")
    parser.add_argument("--chapter-plan", help="Stage 0 章节框架 JSON（cluster_reports.py 产出）")
    parser.add_argument("--coverage-gate", help="Stage 0 覆盖闸门 JSON（coverage_guard.py 产出）")
    parser.add_argument("--member-handoff", action="append", default=[], help="成员独立 handoff JSON，可重复；综合模式至少包含数据、相关领域和交付岗位")
    parser.add_argument("--claim-ledger", required=True, help="数字来源、公式和归因索引 JSON")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--format", choices=["markdown", "json", "both", "all"], default="all", help="兼容参数；v1.5.10 正式报告始终生成 JSON、Markdown 和带图表 PDF")
    args = parser.parse_args()
    try:
        if not re.fullmatch(r"R[1-9][0-9]*", args.report_revision):
            raise ValueError("report_revision 必须使用 R1/R2... 格式")
        from report_build_reuse import existing as existing_build, record as record_build
        build_key,prior=existing_build(args,ROOT)
        if prior is not None:
            print(json.dumps({'status':'PASS','output_dir':args.output_dir,'reused_unchanged_build':True,
                'delivery_completed':False,'files':list(prior['artifacts'])},ensure_ascii=False))
            return 0
        package, markdown = build_package(args)
        output_dir = Path(args.output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        report_json = output_dir / "report.json"
        report_markdown = output_dir / "report.md"
        report_pdf = output_dir / "report.pdf"
        pdf_receipt = output_dir / "pdf-delivery.json"
        write_json(report_json, package)
        report_markdown.write_text(markdown, encoding="utf-8")
        claim_receipt = output_dir / "claim-receipt.json"
        claim_check = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "claim_guard.py"),
                "validate",
                "--claims", str(Path(args.claim_ledger).resolve()),
                "--report", str(report_markdown),
                "--output", str(claim_receipt),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if claim_check.returncode != 0:
            raise ValueError("claim_guard_blocked: " + (claim_check.stderr.strip() or claim_check.stdout.strip() or "unknown"))
        generator = ROOT / "scripts" / "generate_pdf_report.py"
        completed = subprocess.run(
            [
                sys.executable,
                str(generator),
                "--report-json", str(report_json),
                "--output", str(report_pdf),
                "--qa-output", str(pdf_receipt),
                "--render-dir", str(output_dir / ".pdf_qa"),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if completed.returncode != 0:
            raise ValueError("pdf_required_but_generation_failed: " + (completed.stderr.strip() or completed.stdout.strip() or "unknown"))
        pdf_result = read_json(pdf_receipt)
        from artifact_contract import validate_receipt_identity
        validate_receipt_identity(pdf_result, "pdf_delivery", package["team_version"])
        if pdf_result.get("status") != "pdf_render_verified" or int(pdf_result.get("chart_count", 0)) < 3:
            raise ValueError("pdf_required_but_not_verified")
        files = [name for name in ("report.json", "report.md", "report.pdf", "pdf-delivery.json", "claim-receipt.json") if (output_dir / name).exists()]
        if existing_build(args,ROOT)[0]!=build_key:
            raise ValueError('report_build_inputs_changed')
        record_build(output_dir,build_key)
        print(json.dumps({"status": "PASS", "output_dir": str(output_dir), "task_type": package["task_type"], "report_status": package["status"], "gate_status": package["gate_status"], "pdf_status": pdf_result["status"], "chart_count": pdf_result["chart_count"], "files": files}, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, IndexError, TypeError, ArithmeticError, ImportError, RecursionError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
