#!/usr/bin/env python3
"""Validate the omni-ecom WorkBuddy expert package beyond manifest schema checks."""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from pathlib import Path


TEXT_SUFFIXES = {".md", ".json", ".py", ".yaml", ".yml", ".ps1"}
PACKAGE_SUFFIXES = {".md", ".txt", ".json", ".py", ".yaml", ".yml", ".png"}
FORBIDDEN_PACKAGE_NAMES = {".gitkeep"}
FORBIDDEN_PACKAGE_PARTS = {"__pycache__"}
ANALYSIS_AGENTS = ("data-analyst", "platform-ops", "content-live-growth", "ad-profit-optimizer")


def frontmatter_name(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8-sig")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not match:
        return None
    name = re.search(r"(?m)^name:\s*[\"']?([^\"'\n]+)", match.group(1))
    return name.group(1).strip() if name else None


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("不是有效 PNG")
    return struct.unpack(">II", header[16:24])


def inside(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def validate(root: Path, denied_terms: list[str]) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    manifest_path = root / ".codebuddy-plugin" / "plugin.json"
    if not manifest_path.exists():
        return {"status": "FAIL", "errors": ["缺少 .codebuddy-plugin/plugin.json"], "warnings": []}

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"status": "FAIL", "errors": [f"plugin.json 无法解析: {exc}"], "warnings": []}

    if manifest.get("name") != root.name:
        errors.append("plugin name 与目录名不一致")

    for package_path in root.rglob("*"):
        if not package_path.is_file():
            continue
        rel = package_path.relative_to(root)
        if package_path.name in FORBIDDEN_PACKAGE_NAMES:
            errors.append(f"发布包含禁用文件: {rel}")
        if any(part in FORBIDDEN_PACKAGE_PARTS for part in rel.parts):
            errors.append(f"发布包含缓存目录: {rel}")
        suffix = package_path.suffix.casefold()
        if suffix == ".pyc":
            errors.append(f"发布包含 Python 缓存: {rel}")
        elif suffix not in PACKAGE_SUFFIXES:
            errors.append(f"发布包含未允许的文件类型: {rel}")
    version = str(manifest.get("version", ""))
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z]+(?:\.[0-9A-Za-z-]+)*)?", version):
        errors.append("version 不是语义化三段版本号")
    version_info_path = root / "version-info.json"
    if version_info_path.is_file():
        try:
            version_info = json.loads(version_info_path.read_text(encoding="utf-8-sig"))
            if str(version_info.get("team_version", "")) != version:
                errors.append("version-info.json 与 plugin.json 版本不一致")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"version-info.json 无法解析: {exc}")
    else:
        errors.append("缺少 version-info.json")

    agent_ids: list[str] = []
    for rel in manifest.get("agents", []):
        path = (root / rel).resolve()
        if not inside(root, path) or not path.is_file():
            errors.append(f"Agent 路径无效: {rel}")
            continue
        declared = frontmatter_name(path)
        if declared != path.stem:
            errors.append(f"Agent name 与文件名不一致: {rel} -> {declared}")
        agent_ids.append(path.stem)

    team = manifest.get("teamInfo", {})
    expected_team = [team.get("leadAgent"), *team.get("memberAgents", [])]
    member_ids = [item.get("id") for item in manifest.get("members", [])]
    if agent_ids != expected_team:
        errors.append("agents 顺序或成员与 teamInfo 不一致")
    if set(member_ids) != set(expected_team):
        errors.append("members 与 teamInfo 不一致")
    if manifest.get("agentName") != team.get("leadAgent"):
        errors.append("agentName 与 leadAgent 不一致")

    for rel in manifest.get("skills", []):
        path = (root / rel).resolve()
        skill_md = path / "SKILL.md"
        if not inside(root, path) or not skill_md.is_file():
            errors.append(f"Skill 路径无效: {rel}")
            continue
        declared = frontmatter_name(skill_md)
        if declared != path.name:
            errors.append(f"Skill name 与目录名不一致: {rel} -> {declared}")

    required_files = (
        "requirements-runtime.txt",
        "schemas/handoff.schema.json",
        "schemas/action-record.schema.json",
        "schemas/approval-record.schema.json",
        "schemas/report-package.schema.json",
        "schemas/review-manifest.schema.json",
        "schemas/review-attestation.schema.json",
        "schemas/completion-receipt.schema.json",
        "schemas/team-bootstrap.schema.json",
        "schemas/task-profile.schema.json",
        "schemas/pdf-delivery.schema.json",
        "schemas/run-record.schema.json",
        "schemas/run-scope.schema.json",
        "schemas/claim-ledger.schema.json",
        "schemas/host-orchestration-plan.schema.json",
        "schemas/platform-field-mappings.schema.json",
        "schemas/platform-read-observation.schema.json",
        "schemas/model-route-assessment.schema.json",
        "schemas/monitor-policy-reference.schema.json",
        "config/host-profiles.json",
        "evals/cases.json",
        "evals/fixture-responses.json",
        "scripts/run_evals.py",
        "scripts/verify_workbuddy_load.py",
        "scripts/runtime_acceptance.py",
        "scripts/runtime_dependency_guard.py",
        "scripts/runtime_dependency_guard_smoke.py",
        "scripts/data_quality_report_guard.py",
        "scripts/data_quality_report_guard_smoke.py",
        "scripts/prepare_codex_acceptance.py",
        "scripts/release_guard.py",
        "scripts/release_guard_smoke.py",
        "skills/ecom-diagnosis-core/references/platform-field-mappings.json",
        "skills/ecom-diagnosis-core/references/context-isolation.md",
        "skills/ecom-diagnosis-core/scripts/normalize_reports.py",
        "skills/ecom-diagnosis-core/scripts/validate_handoff.py",
        "skills/ecom-diagnosis-core/scripts/context_guard.py",
        "skills/ecom-diagnosis-core/scripts/run_record.py",
        "skills/ecom-diagnosis-core/references/report-package-contract.md",
        "scripts/action_tracker.py",
        "scripts/build_report_package.py",
        "scripts/client_registry.py",
        "scripts/team_bootstrap_guard.py",
        "scripts/host_orchestration_guard.py",
        "scripts/platform_read_guard.py",
        "scripts/platform_read_smoke.py",
        "scripts/model_route_guard.py",
        "scripts/model_route_smoke.py",
        "scripts/monitor_policy_store.py",
        "scripts/monitor_policy_store_smoke.py",
        "references/runtime-v2.md",
        "references/platform-read-v2.md",
        "scripts/collaboration_resume_guard.py",
        "scripts/resume_smoke.py",
        "scripts/collaboration_smoke.py",
        "scripts/wait_for_agent_returns.py",
        "scripts/connector_smoke.py",
        "scripts/public_output_guard.py",
        "scripts/review_guard.py",
        "scripts/completion_gate.py",
        "scripts/claim_guard.py",
        "scripts/claim_guard_smoke.py",
        "scripts/task_profile_smoke.py",
        "scripts/generate_pdf_report.py",
        "scripts/pdf_smoke.py",
        "config/client-brand-registry.json",
        "config/task-profiles.json",
        "connectors/__init__.py",
        "connectors/contract.py",
        "connectors/mock_platform.py",
        "schemas/connector-capability.schema.json",
        "schemas/connector-call.schema.json",
        "schemas/action-policy-decision.schema.json",
        "schemas/action-readback.schema.json",
        "schemas/action-outcome.schema.json",
        "schemas/behavior-monitor-policy.schema.json",
        "schemas/behavior-monitor-comparison.schema.json",
        "schemas/human-feedback.schema.json",
        "schemas/quality-observation.schema.json",
        "schemas/collaboration-event.schema.json",
        "schemas/delivery-completed-event.schema.json",
        "schemas/analysis-depth-guard.schema.json",
        "schemas/conflict-scan.schema.json",
        "schemas/conflict-verdict.schema.json",
        "schemas/object-registry.schema.json",
        "schemas/credential-ref.schema.json",
    )
    for rel in required_files:
        if not (root / rel).is_file():
            errors.append(f"缺少当前版本必需资源: {rel}")

    lead_path = root / "agents" / "omni-ecom-team-lead.md"
    if lead_path.is_file():
        lead_text = lead_path.read_text(encoding="utf-8-sig")
        for required_term in ("TeamCreate", "ToolSearch", "DeferExecuteTool", '{"tool_names":["TeamCreate"]}', "TaskCreate", "TaskList", "TaskUpdate", "phase_task_status_incomplete", "首次尝试必须直接符合正式 handoff 契约", "成员不要调用 `TaskList / TaskUpdate`", "同一分析阶段连续调用四个 Agent", "只允许向 `team-lead` 执行一次 `SendMessage`", "data-analyst", "platform-ops", "content-live-growth", "ad-profit-optimizer", "delivery-review-r1", "纯工具调用回合", "collaboration_unavailable", "collaboration_unavailable_timeout", "client_scope_leak_blocked", "public_output_guard.py", "public-output-receipt.json", "review_guard.py prepare", "review_guard.py attest-result", "--review-attempt-id", "review_guard.py verify", "review_stale_blocked", "review_release_verified", "completion_gate.py", "completion-receipt.json", "formal_delivery_complete", "task-profiles.json", "--task-type", "--claim-ledger", "claim_guard.py", "claim_guard_passed", "claim_report_binding_stale", "数字来源与公式", "访客价值/UV价值", "present_files", "pending_review", "conditional_pass", "No active team found", "collaboration_wait_timeout", "agent_task_id", "attempt_id", "wait_for_agent_returns.py", "collaboration_resume_guard.py", "team_bootstrap_guard.py", "TaskOutput(block=true", "TeamDelete", "--report-revision R1", "report.pdf", "pdf-delivery.json", "pdf_render_verified", "至少 3 张", "结论等价"):
            if required_term not in lead_text:
                errors.append(f"团长缺少多 Agent 协作硬约束: {required_term}")

    for agent_id in (*ANALYSIS_AGENTS, "delivery-review"):
        member_path = root / "agents" / f"{agent_id}.md"
        if member_path.is_file():
            member_text = member_path.read_text(encoding="utf-8-sig")
            for required_term in ("只允许向 `team-lead` 执行一次 `SendMessage`", "禁止给同级专家发消息"):
                if required_term not in member_text:
                    errors.append(f"成员缺少单次回传边界: {agent_id}:{required_term}")

    avatar_paths = {manifest.get("avatar")}
    avatar_paths.update(item.get("avatar") for item in manifest.get("members", []))
    for member in manifest.get("members", []):
        if not member.get("displayName") or member.get("name") is not None:
            errors.append(f"WorkBuddy Team 清单必须沿用 v1.0 的 displayName 且不能使用 name: {member.get('id', 'unknown')}")
    for rel in sorted(path for path in avatar_paths if path):
        path = (root / rel).resolve()
        if not inside(root, path) or not path.is_file():
            errors.append(f"头像路径无效: {rel}")
            continue
        if path.stat().st_size > 500 * 1024:
            errors.append(f"头像超过 500KB: {rel} ({path.stat().st_size} bytes)")
        if path.suffix.lower() == ".png":
            try:
                width, height = png_size(path)
                if (width, height) != (512, 512):
                    errors.append(f"头像尺寸不是 512x512: {rel} ({width}x{height})")
            except ValueError as exc:
                errors.append(f"头像无效: {rel} ({exc})")

    zh_description = str(manifest.get("displayDescription", {}).get("zh", ""))
    han_count = len(re.findall(r"[\u4e00-\u9fff]", zh_description))
    if not 40 <= han_count <= 50:
        warnings.append(f"displayDescription.zh 汉字数建议 40~50，当前 {han_count}")
    if len(manifest.get("tags", [])) != 3:
        warnings.append("建议恰好配置 3 个 tags")
    if len(manifest.get("quickPrompts", [])) != 3:
        warnings.append("建议恰好配置 3 个 quickPrompts")

    private_path = re.compile(r"(?i)(?:[A-Z]:\\Users\\|[A-Z]:\\workbuddy专家团)")
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES or path.resolve() == Path(__file__).resolve():
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(root)
        if rel.as_posix() != "scripts/validate_package.py" and re.search(r"\[TODO|TODO:", text, re.I):
            errors.append(f"存在 TODO 占位: {rel}")
        if private_path.search(text):
            errors.append(f"存在创建者私有绝对路径: {rel}")
        for term in denied_terms:
            if term and term.casefold() in text.casefold():
                errors.append(f"命中禁止公开词: {rel} -> {term}")

    marketplace_path = root.parent.parent / ".codebuddy-plugin" / "marketplace.json"
    if marketplace_path.exists():
        try:
            marketplace = json.loads(marketplace_path.read_text(encoding="utf-8-sig"))
            entries = [item for item in marketplace.get("plugins", []) if item.get("name") == manifest.get("name")]
            if len(entries) != 1:
                errors.append("marketplace.json 中专家条目不是唯一一项")
            elif entries[0].get("version") and entries[0].get("version") != version:
                errors.append("marketplace.json 版本与 plugin.json 不一致")
            elif not entries[0].get("version"):
                warnings.append("marketplace.json 未提供显式版本，以 plugin.json 为版本权威")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"marketplace.json 无法解析: {exc}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "plugin": manifest.get("name"),
        "version": version,
        "agents": len(agent_ids),
        "skills": len(manifest.get("skills", [])),
        "avatars": len(avatar_paths),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 WorkBuddy omni-ecom 专家包")
    parser.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--deny-term", action="append", default=[], help="禁止出现在公域包中的词，可重复")
    args = parser.parse_args()
    result = validate(Path(args.root).resolve(), args.deny_term)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
