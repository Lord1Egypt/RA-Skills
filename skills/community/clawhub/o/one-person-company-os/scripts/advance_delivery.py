#!/usr/bin/env python3
"""Advance delivery and receivable state."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import emit_runtime_report, load_state, preflight_status, print_step, render_workspace, root_doc_path, save_state, state_path, write_record
from localization import pick_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="推进交付与回款。")
    parser.add_argument("company_dir", help="公司工作区目录")
    parser.add_argument("--active-customers", type=int, help="活跃客户数")
    parser.add_argument("--delivery-status", help="交付状态")
    parser.add_argument("--blocking-issue", help="交付阻塞")
    parser.add_argument("--next-delivery-action", help="下一步交付动作")
    parser.add_argument("--receivable", type=float, help="待回款")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    company_dir = Path(args.company_dir).expanduser().resolve()
    state = load_state(company_dir)
    language = state["language"]
    delivery = state["delivery"]

    print_step(1, 5, "模式判定", language=language)
    print_step(2, 5, "preflight 与保存策略检查", language=language)
    runtime = preflight_status(company_dir, language=language)
    if not runtime["runnable"]:
        parser.error(f"runtime not runnable: {runtime['runtime_error']}")
    print_step(3, 5, "草案 / 变更提议 / 当前状态装载", status=pick_text(language, "已完成（加载当前状态）", "Completed (loaded current state)"), language=language)

    if args.active_customers is not None:
        delivery["active_customers"] = args.active_customers
    if args.delivery_status:
        delivery["delivery_status"] = args.delivery_status
    if args.blocking_issue is not None:
        delivery["blocking_issue"] = args.blocking_issue
    if args.next_delivery_action:
        delivery["next_delivery_action"] = args.next_delivery_action
    if args.receivable is not None:
        state["cash"]["receivable"] = args.receivable

    state["focus"]["primary_arena"] = "delivery"
    print_step(4, 5, "执行与落盘", language=language)
    save_state(company_dir, state)
    render_workspace(company_dir, state)
    record = write_record(
        company_dir,
        "经营日志",
        "advance-delivery",
        pick_text(language, "推进交付与回款", "Advanced Delivery And Receivable"),
        [
            pick_text(language, f"- 活跃客户数: {delivery['active_customers']}", f"- Active Customers: {delivery['active_customers']}"),
            pick_text(language, f"- 交付状态: {delivery['delivery_status']}", f"- Delivery Status: {delivery['delivery_status']}"),
            pick_text(language, f"- 下一步交付动作: {delivery['next_delivery_action']}", f"- Next Delivery Action: {delivery['next_delivery_action']}"),
            pick_text(language, f"- 待回款: {state['cash']['receivable']}", f"- Receivable: {state['cash']['receivable']}"),
        ],
    )
    print_step(5, 5, "验证与回报", language=language)
    emit_runtime_report(
        mode=pick_text(language, "推进交付与回款", "Advance Delivery"),
        phase="验证与回报",
        stage=pick_text(language, "v1.0 经营闭环", "v1.0 Business Loop"),
        round_name=pick_text(language, "经营推进", "Operating Push"),
        role=pick_text(language, "经营总控", "Operating Lead"),
        artifact=pick_text(language, "客户交付与回款", "Delivery and cash collection"),
        next_action=delivery["next_delivery_action"],
        needs_confirmation=pick_text(language, "否", "No"),
        persistence_mode="script-execution",
        company_dir=company_dir,
        saved_paths=[root_doc_path(company_dir, "delivery_cash", language), root_doc_path(company_dir, "cash_health", language), record, state_path(company_dir)],
        changes=[pick_text(language, "已刷新客户交付、待回款和下一步交付动作。", "Refreshed delivery, receivables, and the next delivery action.")],
        language=language,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
