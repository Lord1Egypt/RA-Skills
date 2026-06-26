#!/usr/bin/env python3
"""Update cashflow state."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import emit_runtime_report, load_state, preflight_status, print_step, render_workspace, root_doc_path, save_state, state_path, write_record
from localization import pick_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="更新现金状态。")
    parser.add_argument("company_dir", help="公司工作区目录")
    parser.add_argument("--cash-in", type=float, help="收入")
    parser.add_argument("--cash-out", type=float, help="成本")
    parser.add_argument("--receivable", type=float, help="待回款")
    parser.add_argument("--monthly-target", type=float, help="月目标收入")
    parser.add_argument("--runway-note", help="runway 备注")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    company_dir = Path(args.company_dir).expanduser().resolve()
    state = load_state(company_dir)
    language = state["language"]
    cash = state["cash"]

    print_step(1, 5, "模式判定", language=language)
    print_step(2, 5, "preflight 与保存策略检查", language=language)
    runtime = preflight_status(company_dir, language=language)
    if not runtime["runnable"]:
        parser.error(f"runtime not runnable: {runtime['runtime_error']}")
    print_step(3, 5, "草案 / 变更提议 / 当前状态装载", status=pick_text(language, "已完成（加载当前状态）", "Completed (loaded current state)"), language=language)

    if args.cash_in is not None:
        cash["cash_in"] = args.cash_in
    if args.cash_out is not None:
        cash["cash_out"] = args.cash_out
    if args.receivable is not None:
        cash["receivable"] = args.receivable
    if args.monthly_target is not None:
        cash["monthly_target"] = args.monthly_target
    if args.runway_note:
        cash["runway_note"] = args.runway_note

    print_step(4, 5, "执行与落盘", language=language)
    save_state(company_dir, state)
    render_workspace(company_dir, state)
    record = write_record(
        company_dir,
        "经营日志",
        "update-cash",
        pick_text(language, "更新现金状态", "Updated Cash State"),
        [
            f"- cash in: {cash['cash_in']}",
            f"- cash out: {cash['cash_out']}",
            pick_text(language, f"- 待回款: {cash['receivable']}", f"- Receivable: {cash['receivable']}"),
            pick_text(language, f"- 月目标收入: {cash['monthly_target']}", f"- Monthly Target: {cash['monthly_target']}"),
            f"- runway: {cash['runway_note']}",
        ],
    )
    print_step(5, 5, "验证与回报", language=language)
    emit_runtime_report(
        mode=pick_text(language, "更新现金状态", "Update Cash"),
        phase="验证与回报",
        stage=pick_text(language, "v1.0 经营闭环", "v1.0 Business Loop"),
        round_name=pick_text(language, "经营推进", "Operating Push"),
        role=pick_text(language, "经营总控", "Operating Lead"),
        artifact=pick_text(language, "现金流与经营健康", "Cashflow and business health"),
        next_action=state["focus"]["today_action"],
        needs_confirmation=pick_text(language, "否", "No"),
        persistence_mode="script-execution",
        company_dir=company_dir,
        saved_paths=[root_doc_path(company_dir, "cash_health", language), root_doc_path(company_dir, "dashboard", language), record, state_path(company_dir)],
        changes=[pick_text(language, "已刷新收入、成本、待回款和现金安全边界。", "Refreshed income, cost, receivable, and runway.")],
        language=language,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
