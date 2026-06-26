#!/usr/bin/env python3
"""Advance the revenue pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import emit_runtime_report, load_state, preflight_status, print_step, render_workspace, root_doc_path, save_state, state_path, write_record
from localization import pick_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="推进机会与成交管道。")
    parser.add_argument("company_dir", help="公司工作区目录")
    parser.add_argument("--discovering", type=int, help="发现数")
    parser.add_argument("--talking", type=int, help="对话数")
    parser.add_argument("--trial", type=int, help="试用数")
    parser.add_argument("--proposal", type=int, help="报价数")
    parser.add_argument("--won", type=int, help="成交数")
    parser.add_argument("--lost", type=int, help="丢失数")
    parser.add_argument("--next-revenue-action", help="下一条真实成交动作")
    parser.add_argument("--opportunity-name", help="机会名称")
    parser.add_argument("--opportunity-stage", help="机会阶段")
    parser.add_argument("--opportunity-next-action", help="机会下一步")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    company_dir = Path(args.company_dir).expanduser().resolve()
    state = load_state(company_dir)
    language = state["language"]
    pipeline = state["pipeline"]
    summary = pipeline["stage_summary"]

    print_step(1, 5, "模式判定", language=language)
    print_step(2, 5, "preflight 与保存策略检查", language=language)
    runtime = preflight_status(company_dir, language=language)
    if not runtime["runnable"]:
        parser.error(f"runtime not runnable: {runtime['runtime_error']}")
    print_step(3, 5, "草案 / 变更提议 / 当前状态装载", status=pick_text(language, "已完成（加载当前状态）", "Completed (loaded current state)"), language=language)

    for field in ("discovering", "talking", "trial", "proposal", "won", "lost"):
        value = getattr(args, field)
        if value is not None:
            summary[field] = value
    if args.next_revenue_action:
        pipeline["next_revenue_action"] = args.next_revenue_action
    if args.opportunity_name:
        pipeline.setdefault("opportunities", []).append(
            {
                "name": args.opportunity_name,
                "stage": args.opportunity_stage or pick_text(language, "待确认", "TBD"),
                "next_action": args.opportunity_next_action or pick_text(language, "待补充", "Add next step"),
            }
        )

    state["focus"]["primary_arena"] = "sales"
    print_step(4, 5, "执行与落盘", language=language)
    save_state(company_dir, state)
    render_workspace(company_dir, state)
    record = write_record(
        company_dir,
        "经营日志",
        "advance-pipeline",
        pick_text(language, "推进成交管道", "Advanced Pipeline"),
        [
            pick_text(language, f"- 对话: {summary['talking']}", f"- Talking: {summary['talking']}"),
            pick_text(language, f"- 报价: {summary['proposal']}", f"- Proposal: {summary['proposal']}"),
            pick_text(language, f"- 成交: {summary['won']}", f"- Won: {summary['won']}"),
            pick_text(language, f"- 下一条真实成交动作: {pipeline['next_revenue_action']}", f"- Next Real Revenue Action: {pipeline['next_revenue_action']}"),
        ],
    )
    print_step(5, 5, "验证与回报", language=language)
    emit_runtime_report(
        mode=pick_text(language, "推进成交管道", "Advance Pipeline"),
        phase="验证与回报",
        stage=pick_text(language, "v1.0 经营闭环", "v1.0 Business Loop"),
        round_name=pick_text(language, "经营推进", "Operating Push"),
        role=pick_text(language, "经营总控", "Operating Lead"),
        artifact=pick_text(language, "机会与成交管道", "Opportunity and revenue pipeline"),
        next_action=pipeline["next_revenue_action"],
        needs_confirmation=pick_text(language, "否", "No"),
        persistence_mode="script-execution",
        company_dir=company_dir,
        saved_paths=[root_doc_path(company_dir, "pipeline", language), root_doc_path(company_dir, "dashboard", language), record, state_path(company_dir)],
        changes=[pick_text(language, "已刷新成交漏斗和下一条真实成交动作。", "Refreshed the revenue funnel and next real revenue action.")],
        language=language,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
