#!/usr/bin/env python3
"""Build role-agent briefs for One Person Company OS."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional

from common import (
    ensure_within_directory,
    emit_runtime_report,
    load_json,
    load_role_specs,
    load_stage_defaults,
    normalize_stage,
    preflight_status,
    print_step,
    role_display_names,
    role_spec,
    write_text,
)
from localization import normalize_language, pick_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build one or more v1 operating role-agent briefs.")
    parser.add_argument("--primary-arena", default="", choices=["", "sales", "product", "delivery", "cash", "asset"], help="当前主战场")
    parser.add_argument("--stage", default="", help=argparse.SUPPRESS)
    parser.add_argument("--role", help="单个角色 id")
    parser.add_argument("--all-default-roles", action="store_true", help="输出当前主战场的默认角色集")
    parser.add_argument("--include-optional", action="store_true", help="同时包含可选角色")
    parser.add_argument("--language", default="zh-CN", help="工作语言")
    parser.add_argument("--company-name", default="未命名公司", help="公司名称")
    parser.add_argument("--company-dir", help="可选，公司工作区目录；如果需要落盘 brief，则 output-dir 必须位于该目录内")
    parser.add_argument("--objective", default="推进当前主瓶颈", help="当前目标")
    parser.add_argument("--current-round", default="", help=argparse.SUPPRESS)
    parser.add_argument("--round-goal", default="", help=argparse.SUPPRESS)
    parser.add_argument("--current-bottleneck", default="待确认", help="当前瓶颈")
    parser.add_argument("--trigger-reason", default="无", help="触发原因")
    parser.add_argument("--next-shortest-action", default="待确认", help="下一步最短动作")
    parser.add_argument("--input", action="append", default=[], help="补充输入，可重复")
    parser.add_argument("--artifact", action="append", default=[], help="补充输出，可重复")
    parser.add_argument("--constraint", action="append", default=[], help="补充约束，可重复")
    parser.add_argument("--approval-gate", action="append", default=[], help="补充审批点，可重复")
    parser.add_argument("--pending-approval", action="append", default=[], help="待创始人确认事项")
    parser.add_argument("--output-format", choices=["markdown", "json"], default="markdown", help="输出格式")
    parser.add_argument("--output-dir", help="批量写入的目录")
    return parser


def unique(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result


def role_ids_for_stage(stage_id: str, include_optional: bool) -> list[str]:
    defaults = load_stage_defaults()
    role_ids = list(defaults["stage_defaults"][stage_id])
    if include_optional:
        role_ids.extend(defaults["stage_optional_roles"].get(stage_id, []))
    return unique(role_ids)


def stage_id_for_primary_arena(primary_arena: str, stage_value: str) -> str:
    """Map the v1 visible arena to the existing internal role-default groups."""
    if stage_value:
        return normalize_stage(stage_value)
    return {
        "sales": "validate",
        "product": "build",
        "delivery": "launch",
        "cash": "operate",
        "asset": "grow",
    }.get(primary_arena or "product", "build")


def build_packet(
    spec: dict[str, Any],
    *,
    stage_id: str,
    primary_arena: str,
    role_specs: dict[str, dict[str, Any]],
    company_name: str,
    language: str,
    objective: str,
    current_bottleneck: str,
    trigger_reason: str,
    next_shortest_action: str,
    extra_inputs: list[str],
    extra_artifacts: list[str],
    constraints: list[str],
    extra_approval_gates: list[str],
    pending_approvals: list[str],
) -> dict[str, Any]:
    return {
        "operating_model": pick_text(language, "v1.0 经营闭环", "v1.0 Business Loop"),
        "primary_arena": primary_arena or "product",
        "internal_role_group": stage_id,
        "working_language": language,
        "company_name": company_name,
        "role_id": spec["role_id"],
        "role_display_name": spec["display_name"],
        "objective": objective,
        "current_bottleneck": current_bottleneck,
        "next_shortest_action": next_shortest_action,
        "mission": spec["mission"],
        "owns": spec["owns"],
        "inputs": unique(spec["inputs_required"] + extra_inputs),
        "required_outputs": unique(spec["outputs_required"] + extra_artifacts),
        "constraints": constraints or [pick_text(language, "尊重创始人是最终决策者。", "Respect the founder as the final decision-maker.")],
        "approval_gates": unique(spec["approval_required_for"] + extra_approval_gates),
        "handoff_targets": role_display_names(spec["handoff_to"], role_specs, language),
        "guardrails": spec["do_not_do"],
        "continuation_context": {
            "primary_goal": objective,
            "primary_arena": primary_arena or "product",
            "current_bottleneck": current_bottleneck,
            "trigger_reason": trigger_reason,
            "next_shortest_action": next_shortest_action,
            "pending_approvals": pending_approvals,
            "recommended_next_owner": role_display_names(spec["handoff_to"][:1], role_specs, language)[0]
            if spec["handoff_to"]
            else pick_text(language, "创始人", "Founder"),
        },
    }


def format_markdown(packet: dict[str, Any], schema: dict[str, Any]) -> str:
    language = packet["working_language"]
    lines = [
        f"# {pick_text(language, '角色 Brief', 'Role Brief')}: {packet['role_display_name']}",
        "",
        f"## {pick_text(language, '会话框架', 'Session Frame')}",
        f"- {pick_text(language, '经营模型', 'Operating Model')}: {packet['operating_model']}",
        f"- {pick_text(language, '工作语言', 'Working Language')}: {packet['working_language']}",
        f"- {pick_text(language, '公司', 'Company')}: {packet['company_name']}",
        f"- {pick_text(language, '当前目标', 'Current Objective')}: {packet['objective']}",
        f"- {pick_text(language, '当前主战场', 'Primary Arena')}: {packet['primary_arena']}",
        f"- {pick_text(language, '当前瓶颈', 'Current Bottleneck')}: {packet['current_bottleneck']}",
        f"- {pick_text(language, '下一步最短动作', 'Shortest Next Action')}: {packet['next_shortest_action']}",
        "",
        f"## {pick_text(language, '角色使命', 'Role Mission')}",
        f"- {pick_text(language, '角色 ID', 'Role ID')}: {packet['role_id']}",
        f"- {pick_text(language, '使命', 'Mission')}: {packet['mission']}",
        "",
        f"## {pick_text(language, '负责范围', 'Ownership')}",
    ]
    lines.extend(f"- {item}" for item in packet["owns"])
    lines.extend(["", f"## {pick_text(language, '输入', 'Inputs')}"])
    lines.extend(f"- {item}" for item in packet["inputs"])
    lines.extend(["", f"## {pick_text(language, '输出', 'Outputs')}"])
    lines.extend(f"- {item}" for item in packet["required_outputs"])
    lines.extend(["", f"## {pick_text(language, '约束', 'Constraints')}"])
    lines.extend(f"- {item}" for item in packet["constraints"])
    lines.extend(["", f"## {pick_text(language, '审批点', 'Approval Gates')}"])
    lines.extend(f"- {item}" for item in packet["approval_gates"])
    lines.extend(["", f"## {pick_text(language, '默认交接对象', 'Default Handoff Targets')}"])
    lines.extend(f"- {item}" for item in packet["handoff_targets"])
    lines.extend(["", f"## {pick_text(language, '不该做的事', 'Guardrails')}"])
    lines.extend(f"- {item}" for item in packet["guardrails"])
    lines.extend(
        [
            "",
            f"## {pick_text(language, '延续上下文', 'Continuation Context')}",
            f"- {pick_text(language, '当前瓶颈', 'Current Bottleneck')}: {packet['continuation_context']['current_bottleneck']}",
            f"- {pick_text(language, '触发原因', 'Trigger Reason')}: {packet['continuation_context']['trigger_reason']}",
            f"- {pick_text(language, '下一步最短动作', 'Shortest Next Action')}: {packet['continuation_context']['next_shortest_action']}",
            f"- {pick_text(language, '推荐下一负责人', 'Recommended Next Owner')}: {packet['continuation_context']['recommended_next_owner']}",
            "",
            f"## {pick_text(language, '待确认事项', 'Pending Confirmations')}",
        ]
    )
    pending = packet["continuation_context"]["pending_approvals"] or [pick_text(language, "无", "None")]
    lines.extend(f"- {item}" for item in pending)
    lines.extend(["", "## Schema", f"- {pick_text(language, '必填字段', 'Required Fields')}: {', '.join(schema['required_fields'])}"])
    return "\n".join(lines) + "\n"


def write_packet(packet: dict[str, Any], output_format: str, output_dir: Optional[Path], schema: dict[str, Any]) -> Optional[Path]:
    if output_format == "json":
        rendered = json.dumps(packet, ensure_ascii=False, indent=2) + "\n"
        suffix = ".json"
    else:
        rendered = format_markdown(packet, schema)
        suffix = ".md"

    if output_dir is None:
        print(rendered, end="")
        return None

    filename = packet["role_display_name"] + suffix
    path = output_dir / filename
    write_text(path, rendered)
    print(path)
    return path


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    language = normalize_language(
        args.language,
        args.stage,
        args.primary_arena,
        args.company_name,
        args.objective,
        args.current_bottleneck,
        args.next_shortest_action,
    )
    if args.company_name == "未命名公司" and language == "en-US":
        args.company_name = "Untitled Company"
    if args.objective == "推进当前主瓶颈" and language == "en-US":
        args.objective = "Advance the current primary bottleneck"
    if args.current_bottleneck == "待确认" and language == "en-US":
        args.current_bottleneck = "Pending confirmation"
    if args.trigger_reason == "无" and language == "en-US":
        args.trigger_reason = "None"
    if args.next_shortest_action == "待确认" and language == "en-US":
        args.next_shortest_action = "Pending confirmation"

    print_step(1, 5, "模式判定", stream=sys.stderr, language=language)
    if not args.role and not args.all_default_roles:
        parser.error("use --role or --all-default-roles")

    if not args.primary_arena:
        args.primary_arena = "product"
    stage_id = stage_id_for_primary_arena(args.primary_arena, args.stage)
    company_dir = Path(args.company_dir).expanduser().resolve() if args.company_dir else None
    output_dir = Path(args.output_dir).expanduser() if args.output_dir else None
    if output_dir is not None and company_dir is not None and not output_dir.is_absolute():
        output_dir = company_dir / output_dir

    print_step(2, 5, "preflight 与保存策略检查", stream=sys.stderr, language=language)
    runtime = preflight_status(output_dir or company_dir, language=language)
    if not runtime["runnable"]:
        parser.error(f"runtime not runnable: {runtime['runtime_error']}")
    if output_dir is not None and not runtime["writable"]:
        parser.error(f"target not writable: {runtime['writable_target']}")

    role_specs = load_role_specs()
    schema = load_json(Path(__file__).resolve().parent.parent / "orchestration" / "handoff-schema.json")

    if args.role:
        role_ids = [args.role]
    else:
        role_ids = role_ids_for_stage(stage_id, args.include_optional)

    missing = [role_id for role_id in role_ids if role_id not in role_specs]
    if missing:
        parser.error(f"unknown role ids: {', '.join(missing)}")

    if output_dir is None and len(role_ids) > 1:
        parser.error("multiple briefs require --output-dir")
    if output_dir is not None and company_dir is None:
        parser.error("persisted role briefs require --company-dir so the write boundary stays inside the workspace")
    if output_dir is not None and company_dir is not None:
        try:
            output_dir = ensure_within_directory(output_dir, company_dir, label="output-dir")
        except ValueError as exc:
            parser.error(str(exc))

    print_step(3, 5, "草案 / 变更提议 / 当前状态装载", status=pick_text(language, "已完成（组装角色 Brief）", "Completed (assembled the role brief)"), stream=sys.stderr, language=language)
    saved_paths: list[Path] = []
    print_step(4, 5, "执行与落盘", stream=sys.stderr, language=language)
    for role_id in role_ids:
        packet = build_packet(
            role_spec(role_id, role_specs, language),
            stage_id=stage_id,
            primary_arena=args.primary_arena,
            role_specs=role_specs,
            company_name=args.company_name,
            language=language,
            objective=args.objective,
            current_bottleneck=args.current_bottleneck,
            trigger_reason=args.trigger_reason,
            next_shortest_action=args.next_shortest_action,
            extra_inputs=args.input,
            extra_artifacts=args.artifact,
            constraints=args.constraint,
            extra_approval_gates=args.approval_gate,
            pending_approvals=args.pending_approval,
        )
        written = write_packet(packet, args.output_format, output_dir, schema)
        if written is not None:
            saved_paths.append(written)

    print_step(5, 5, "验证与回报", stream=sys.stderr, language=language)
    emit_runtime_report(
        mode=pick_text(language, "生成角色 Brief", "Build Agent Brief"),
        phase="验证与回报",
        stage=pick_text(language, "v1.0 经营闭环", "v1.0 Business Loop"),
        round_name=args.objective,
        role=("、".join(role_spec(role_id, role_specs, language)["display_name"] for role_id in role_ids) if language == "zh-CN" else ", ".join(role_spec(role_id, role_specs, language)["display_name"] for role_id in role_ids)),
        artifact=pick_text(language, "角色智能体 brief", "role-agent brief"),
        next_action=pick_text(language, "把 brief 交给对应角色或继续推进今日最短动作", "Hand the brief to the target role or continue the shortest action today"),
        needs_confirmation=pick_text(language, "否", "No"),
        persistence_mode="script-execution" if output_dir is not None else "chat-only",
        company_dir=output_dir,
        saved_paths=saved_paths,
        unsaved_reason=pick_text(language, "当前内容仅输出到标准输出，未指定 --output-dir", "The brief was only written to stdout because --output-dir was not provided") if output_dir is None else pick_text(language, "无", "None"),
        work_scope=[
            pick_text(language, "基于当前主目标、主瓶颈和主战场生成角色执行 brief。", "Generate role-execution briefs based on the current goal, bottleneck, and primary arena."),
            pick_text(language, "明确角色输入、输出、约束和交接对象。", "Clarify role inputs, outputs, constraints, and handoff targets."),
            pick_text(language, "说明这些 brief 是否已经落盘。", "Explain whether the briefs were actually persisted."),
        ],
        non_scope=[
            pick_text(language, "不会跳过经营上下文直接生成空白角色模板。", "Do not generate blank role templates without operating context."),
            pick_text(language, "不会把标准输出误说成已经写入工作区。", "Do not describe stdout-only output as already written into the workspace."),
        ],
        changes=[
            pick_text(language, f"本次共生成 {len(role_ids)} 份角色 brief。", f"Generated {len(role_ids)} role brief(s) in this run."),
            pick_text(language, "已把角色使命、输入输出、审批点和延续上下文整理成标准格式。", "Standardized role missions, inputs, outputs, approval gates, and continuation context."),
            pick_text(language, "如果未指定输出目录，本次内容仅存在于标准输出。", "If no output directory is provided, the content exists only in stdout."),
        ],
        stream=sys.stderr,
        language=language,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
