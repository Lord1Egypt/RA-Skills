#!/usr/bin/env python3
"""Generate numbered DOCX artifact documents for One Person Company OS v1.0."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    artifact_dir_path,
    artifact_status_summary_markdown,
    display_path,
    emit_runtime_report,
    load_state,
    planned_docx_path,
    preflight_status,
    print_step,
    render_workspace,
    save_state,
    state_path,
    workspace_file_path,
    write_docx,
    write_record,
    write_text,
)
from localization import pick_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="生成 v1.0 带序号的正式 DOCX 产物。")
    parser.add_argument("company_dir", help="公司工作区目录")
    parser.add_argument("--title", required=True, help="产物标题")
    parser.add_argument("--category", choices=["delivery", "software", "business", "ops", "growth"], default="delivery", help="产物目录分类")
    parser.add_argument("--summary", default="待补充本次产物摘要", help="产物摘要")
    parser.add_argument("--evidence", action="append", default=[], help="证据或路径，可重复")
    parser.add_argument("--next-action", default="", help="下一步动作")
    return parser


def bullets(items: list[str], fallback: str) -> str:
    values = [item for item in items if item] or [fallback]
    return "\n".join(f"- {item}" for item in values)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    company_dir = Path(args.company_dir).expanduser().resolve()
    state = load_state(company_dir)
    language = state.get("language", "zh-CN")
    focus = state.get("focus", {})
    if args.summary == "待补充本次产物摘要" and language == "en-US":
        args.summary = "Add the summary for this artifact"

    print_step(1, 5, "模式判定", language=language)
    print_step(2, 5, "preflight 与保存策略检查", language=language)
    runtime = preflight_status(company_dir, language=language)
    if not runtime["runnable"]:
        parser.error(f"runtime not runnable: {runtime['runtime_error']}")

    print_step(3, 5, "草案 / 变更提议 / 当前状态装载", status=pick_text(language, "已完成（装载当前状态与文档参数）", "Completed (loaded the current state and document parameters)"), language=language)
    next_action = args.next_action or focus.get("today_action", pick_text(language, "补齐真实交付与证据", "Complete the real delivery and evidence"))
    output_path = planned_docx_path(artifact_dir_path(company_dir, args.category, language), args.title, completed=True)
    output_path_display = display_path(output_path, company_dir)
    markdown = "\n".join(
        [
            f"# {args.title}",
            "",
            f"{pick_text(language, '公司', 'Company')}: {state['company_name']}",
            f"{pick_text(language, '产品', 'Product')}: {state['product_name']}",
            f"{pick_text(language, '文档成熟度', 'Document Maturity')}: {pick_text(language, '交付就绪版', 'Delivery-Ready')}",
            f"{pick_text(language, '路径', 'Path')}: {output_path_display}",
            "",
            pick_text(language, "## 摘要", "## Summary"),
            "",
            args.summary,
            "",
            pick_text(language, "## 经营上下文", "## Operating Context"),
            "",
            f"- {pick_text(language, '当前主目标', 'Primary Goal')}: {focus.get('primary_goal', '')}",
            f"- {pick_text(language, '当前主瓶颈', 'Primary Bottleneck')}: {focus.get('primary_bottleneck', '')}",
            f"- {pick_text(language, '当前主战场', 'Primary Arena')}: {focus.get('primary_arena', '')}",
            "",
            pick_text(language, "## 证据", "## Evidence"),
            "",
            bullets(args.evidence, pick_text(language, "待补充文件路径、演示链接或验收证据", "Add file paths, demo links, or acceptance evidence")),
            "",
            pick_text(language, "## 下一步", "## Next Action"),
            "",
            f"- {next_action}",
            "",
        ]
    )

    print_step(4, 5, "执行与落盘", language=language)
    write_docx(output_path, markdown, title=args.title)
    write_text(workspace_file_path(company_dir, "delivery_directory", language), artifact_status_summary_markdown(company_dir, language))
    save_state(company_dir, state)
    render_workspace(company_dir, state)
    record = write_record(
        company_dir,
        "推进日志",
        pick_text(language, "文档产物", "artifact-document"),
        pick_text(language, f"生成正式交付文档 {args.title}", f"Generated formal deliverable document {args.title}"),
        [
            pick_text(language, f"- 产物标题: {args.title}", f"- Artifact Title: {args.title}"),
            pick_text(language, f"- 输出分类: {args.category}", f"- Output Category: {args.category}"),
            pick_text(language, f"- 实际文件: {output_path.name}", f"- Output File: {output_path.name}"),
            pick_text(language, f"- 下一步最短动作: {next_action}", f"- Shortest Next Action: {next_action}"),
        ],
    )

    print_step(5, 5, "验证与回报", language=language)
    emit_runtime_report(
        mode=pick_text(language, "生成正式交付文档", "Generate Formal Deliverable Document"),
        phase="验证与回报",
        stage=pick_text(language, "v1.0 经营闭环", "v1.0 Business Loop"),
        round_name=pick_text(language, "经营推进", "Operating Push"),
        role=pick_text(language, "经营总控", "Operating Lead"),
        artifact=f"{args.title} DOCX",
        next_action=next_action,
        needs_confirmation=pick_text(language, "否", "No"),
        persistence_mode="script-execution",
        company_dir=company_dir,
        saved_paths=[output_path, workspace_file_path(company_dir, "delivery_directory", language), record, state_path(company_dir)],
        changes=[pick_text(language, f"已生成正式 DOCX：{output_path.name}。", f"Generated a formal DOCX: {output_path.name}.")],
        language=language,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
