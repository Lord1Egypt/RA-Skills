#!/usr/bin/env python3
"""Update the primary focus of the business-loop workspace."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import emit_runtime_report, load_state, preflight_status, print_step, render_workspace, root_doc_path, save_state, state_path, write_record
from localization import pick_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="更新当前经营主焦点。")
    parser.add_argument("company_dir", help="公司工作区目录")
    parser.add_argument("--primary-goal", help="头号目标")
    parser.add_argument("--primary-bottleneck", help="当前主瓶颈")
    parser.add_argument("--primary-arena", choices=["sales", "product", "delivery", "cash", "asset"], help="当前主战场")
    parser.add_argument("--today-action", help="今天最短动作")
    parser.add_argument("--week-outcome", help="本周唯一结果")
    parser.add_argument("--note", default="", help="补充说明")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    company_dir = Path(args.company_dir).expanduser().resolve()
    state = load_state(company_dir)
    language = state["language"]
    focus = state["focus"]

    print_step(1, 5, "模式判定", language=language)
    print_step(2, 5, "preflight 与保存策略检查", language=language)
    runtime = preflight_status(company_dir, language=language)
    if not runtime["runnable"]:
        parser.error(f"runtime not runnable: {runtime['runtime_error']}")
    print_step(3, 5, "草案 / 变更提议 / 当前状态装载", status=pick_text(language, "已完成（加载当前状态）", "Completed (loaded current state)"), language=language)

    if args.primary_goal:
        focus["primary_goal"] = args.primary_goal
    if args.primary_bottleneck:
        focus["primary_bottleneck"] = args.primary_bottleneck
    if args.primary_arena:
        focus["primary_arena"] = args.primary_arena
    if args.today_action:
        focus["today_action"] = args.today_action
    if args.week_outcome:
        focus["week_outcome"] = args.week_outcome

    print_step(4, 5, "执行与落盘", language=language)
    save_state(company_dir, state)
    render_workspace(company_dir, state)
    record = write_record(
        company_dir,
        "经营日志",
        "update-focus",
        pick_text(language, "更新经营主焦点", "Updated Business Focus"),
        [
            pick_text(language, f"- 头号目标: {focus['primary_goal']}", f"- Primary Goal: {focus['primary_goal']}"),
            pick_text(language, f"- 当前主瓶颈: {focus['primary_bottleneck']}", f"- Primary Bottleneck: {focus['primary_bottleneck']}"),
            pick_text(language, f"- 当前主战场: {focus['primary_arena']}", f"- Primary Arena: {focus['primary_arena']}"),
            pick_text(language, f"- 今天最短动作: {focus['today_action']}", f"- Shortest Action Today: {focus['today_action']}"),
            pick_text(language, f"- 本周唯一结果: {focus['week_outcome']}", f"- Single Weekly Outcome: {focus['week_outcome']}"),
            pick_text(language, f"- 备注: {args.note or '无'}", f"- Note: {args.note or 'None'}"),
        ],
    )

    print_step(5, 5, "验证与回报", language=language)
    emit_runtime_report(
        mode=pick_text(language, "更新主焦点", "Update Focus"),
        phase="验证与回报",
        stage=pick_text(language, "v1.0 经营闭环", "v1.0 Business Loop"),
        round_name=pick_text(language, "经营推进", "Operating Push"),
        role=pick_text(language, "经营总控", "Operating Lead"),
        artifact=pick_text(language, "经营驾驶舱", "Operating cockpit"),
        next_action=focus["today_action"],
        needs_confirmation=pick_text(language, "否", "No"),
        persistence_mode="script-execution",
        company_dir=company_dir,
        saved_paths=[
            root_doc_path(company_dir, "dashboard", language),
            root_doc_path(company_dir, "week_focus", language),
            root_doc_path(company_dir, "today_action", language),
            record,
            state_path(company_dir),
        ],
        changes=[
            pick_text(language, "已刷新头号目标、主瓶颈、主战场与今日动作。", "Refreshed the primary goal, bottleneck, arena, and today's action."),
        ],
        language=language,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
