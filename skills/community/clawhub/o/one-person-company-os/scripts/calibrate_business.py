#!/usr/bin/env python3
"""Record a business calibration decision."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import emit_runtime_report, load_state, preflight_status, print_step, render_workspace, root_doc_path, save_state, state_path, write_record
from localization import pick_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="校准经营决策。")
    parser.add_argument("company_dir", help="公司工作区目录")
    parser.add_argument("--reason", required=True, help="校准原因")
    parser.add_argument("--decision", required=True, help="校准结论")
    parser.add_argument("--next-action", required=True, help="校准后的下一步")
    parser.add_argument("--primary-arena", choices=["sales", "product", "delivery", "cash", "asset"], help="校准后的主战场")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    company_dir = Path(args.company_dir).expanduser().resolve()
    state = load_state(company_dir)
    language = state["language"]

    print_step(1, 5, "模式判定", language=language)
    print_step(2, 5, "preflight 与保存策略检查", language=language)
    runtime = preflight_status(company_dir, language=language)
    if not runtime["runnable"]:
        parser.error(f"runtime not runnable: {runtime['runtime_error']}")
    print_step(3, 5, "草案 / 变更提议 / 当前状态装载", status=pick_text(language, "已完成（加载当前状态）", "Completed (loaded current state)"), language=language)

    state["focus"]["primary_bottleneck"] = args.reason
    state["focus"]["today_action"] = args.next_action
    if args.primary_arena:
        state["focus"]["primary_arena"] = args.primary_arena
    if args.decision not in state["risk"]["pending_decisions"]:
        state["risk"]["pending_decisions"].append(args.decision)
    state.setdefault("decision", {}).setdefault("recent_decisions", []).append(args.decision)
    if args.reason not in state["risk"]["top_risks"]:
        state["risk"]["top_risks"].append(args.reason)

    print_step(4, 5, "执行与落盘", language=language)
    save_state(company_dir, state)
    render_workspace(company_dir, state)
    record = write_record(
        company_dir,
        "经营决策",
        "calibrate-business",
        pick_text(language, "校准经营决策", "Calibrated Business Decision"),
        [
            pick_text(language, f"- 原因: {args.reason}", f"- Reason: {args.reason}"),
            pick_text(language, f"- 结论: {args.decision}", f"- Decision: {args.decision}"),
            pick_text(language, f"- 下一步: {args.next_action}", f"- Next Action: {args.next_action}"),
        ],
    )
    print_step(5, 5, "验证与回报", language=language)
    emit_runtime_report(
        mode=pick_text(language, "校准经营决策", "Calibrate Business"),
        phase="验证与回报",
        stage=pick_text(language, "v1.0 经营闭环", "v1.0 Business Loop"),
        round_name=pick_text(language, "经营推进", "Operating Push"),
        role=pick_text(language, "经营总控", "Operating Lead"),
        artifact=pick_text(language, "风险与关键决策", "Risks and key decisions"),
        next_action=args.next_action,
        needs_confirmation=pick_text(language, "否", "No"),
        persistence_mode="script-execution",
        company_dir=company_dir,
        saved_paths=[root_doc_path(company_dir, "risks", language), root_doc_path(company_dir, "today_action", language), record, state_path(company_dir)],
        changes=[pick_text(language, "已把校准结论写入风险与关键决策，并刷新下一步动作。", "Wrote the calibration outcome into risks and key decisions, and refreshed the next action.")],
        language=language,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
