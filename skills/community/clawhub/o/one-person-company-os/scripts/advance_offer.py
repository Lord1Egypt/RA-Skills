#!/usr/bin/env python3
"""Advance the offer definition."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import emit_runtime_report, load_state, preflight_status, print_step, render_workspace, root_doc_path, save_state, state_path, write_record
from localization import pick_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="推进价值承诺与报价。")
    parser.add_argument("company_dir", help="公司工作区目录")
    parser.add_argument("--promise", help="价值承诺")
    parser.add_argument("--target-customer", help="目标客户")
    parser.add_argument("--scenario", help="高频场景")
    parser.add_argument("--pricing", help="定价方式")
    parser.add_argument("--proof", action="append", default=[], help="新增证据")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    company_dir = Path(args.company_dir).expanduser().resolve()
    state = load_state(company_dir)
    language = state["language"]
    offer = state["offer"]

    print_step(1, 5, "模式判定", language=language)
    print_step(2, 5, "preflight 与保存策略检查", language=language)
    runtime = preflight_status(company_dir, language=language)
    if not runtime["runnable"]:
        parser.error(f"runtime not runnable: {runtime['runtime_error']}")
    print_step(3, 5, "草案 / 变更提议 / 当前状态装载", status=pick_text(language, "已完成（加载当前状态）", "Completed (loaded current state)"), language=language)

    if args.promise:
        offer["promise"] = args.promise
    if args.target_customer:
        offer["target_customer"] = args.target_customer
        state.setdefault("buyer", {})["segment"] = args.target_customer
    if args.scenario:
        offer["scenario"] = args.scenario
        state.setdefault("buyer", {})["urgent_problem"] = args.scenario
    if args.pricing:
        offer["pricing"] = args.pricing
    for proof in args.proof:
        if proof not in offer["proof"]:
            offer["proof"].append(proof)

    state["focus"]["primary_arena"] = "sales"
    print_step(4, 5, "执行与落盘", language=language)
    save_state(company_dir, state)
    render_workspace(company_dir, state)
    record = write_record(
        company_dir,
        "经营日志",
        "advance-offer",
        pick_text(language, "推进价值承诺", "Advanced Offer"),
        [
            pick_text(language, f"- 承诺: {offer['promise']}", f"- Promise: {offer['promise']}"),
            pick_text(language, f"- 客户: {offer['target_customer']}", f"- Customer: {offer['target_customer']}"),
            pick_text(language, f"- 场景: {offer['scenario']}", f"- Scenario: {offer['scenario']}"),
            pick_text(language, f"- 定价: {offer['pricing']}", f"- Pricing: {offer['pricing']}"),
        ],
    )
    print_step(5, 5, "验证与回报", language=language)
    emit_runtime_report(
        mode=pick_text(language, "推进价值承诺", "Advance Offer"),
        phase="验证与回报",
        stage=pick_text(language, "v1.0 经营闭环", "v1.0 Business Loop"),
        round_name=pick_text(language, "经营推进", "Operating Push"),
        role=pick_text(language, "经营总控", "Operating Lead"),
        artifact=pick_text(language, "价值承诺与报价", "Value promise and pricing"),
        next_action=state["focus"]["today_action"],
        needs_confirmation=pick_text(language, "否", "No"),
        persistence_mode="script-execution",
        company_dir=company_dir,
        saved_paths=[root_doc_path(company_dir, "offer", language), root_doc_path(company_dir, "dashboard", language), record, state_path(company_dir)],
        changes=[pick_text(language, "已刷新价值承诺、目标客户、场景或定价。", "Refreshed the promise, target customer, scenario, or pricing.")],
        language=language,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
