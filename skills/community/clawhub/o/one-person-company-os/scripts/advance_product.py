#!/usr/bin/env python3
"""Advance product build and launch state."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import emit_runtime_report, load_state, preflight_status, print_step, render_workspace, root_doc_path, save_state, state_path, write_record
from localization import pick_text


PRODUCT_STATES = ("idea", "defined", "prototype", "internal", "external", "launchable", "live")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="推进产品与上线状态。")
    parser.add_argument("company_dir", help="公司工作区目录")
    parser.add_argument("--state", choices=PRODUCT_STATES, help="产品状态")
    parser.add_argument("--current-version", help="当前版本")
    parser.add_argument("--core-capability", action="append", default=[], help="核心能力")
    parser.add_argument("--current-gap", action="append", default=[], help="当前缺口")
    parser.add_argument("--launch-blocker", help="上线阻塞")
    parser.add_argument("--repository", help="仓库路径或地址")
    parser.add_argument("--launch-path", help="上线入口")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    company_dir = Path(args.company_dir).expanduser().resolve()
    state = load_state(company_dir)
    language = state["language"]
    product = state["product"]

    print_step(1, 5, "模式判定", language=language)
    print_step(2, 5, "preflight 与保存策略检查", language=language)
    runtime = preflight_status(company_dir, language=language)
    if not runtime["runnable"]:
        parser.error(f"runtime not runnable: {runtime['runtime_error']}")
    print_step(3, 5, "草案 / 变更提议 / 当前状态装载", status=pick_text(language, "已完成（加载当前状态）", "Completed (loaded current state)"), language=language)

    if args.state:
        product["state"] = args.state
    if args.current_version:
        product["current_version"] = args.current_version
    if args.core_capability:
        product["core_capability"] = args.core_capability
    if args.current_gap:
        product["current_gap"] = args.current_gap
    if args.launch_blocker:
        product["launch_blocker"] = args.launch_blocker
    if args.repository:
        product["repository"] = args.repository
    if args.launch_path:
        product["launch_path"] = args.launch_path

    state["focus"]["primary_arena"] = "product"
    print_step(4, 5, "执行与落盘", language=language)
    save_state(company_dir, state)
    render_workspace(company_dir, state)
    record = write_record(
        company_dir,
        "经营日志",
        "advance-product",
        pick_text(language, "推进产品与上线", "Advanced Product And Launch"),
        [
            pick_text(language, f"- 产品状态: {product['state']}", f"- Product State: {product['state']}"),
            pick_text(language, f"- 当前版本: {product['current_version']}", f"- Current Version: {product['current_version']}"),
            pick_text(language, f"- 上线阻塞: {product['launch_blocker']}", f"- Launch Blocker: {product['launch_blocker']}"),
        ],
    )
    print_step(5, 5, "验证与回报", language=language)
    emit_runtime_report(
        mode=pick_text(language, "推进产品与上线", "Advance Product"),
        phase="验证与回报",
        stage=pick_text(language, "v1.0 经营闭环", "v1.0 Business Loop"),
        round_name=pick_text(language, "经营推进", "Operating Push"),
        role=pick_text(language, "经营总控", "Operating Lead"),
        artifact=pick_text(language, "产品与上线状态", "Product and launch status"),
        next_action=state["focus"]["today_action"],
        needs_confirmation=pick_text(language, "否", "No"),
        persistence_mode="script-execution",
        company_dir=company_dir,
        saved_paths=[root_doc_path(company_dir, "product_status", language), root_doc_path(company_dir, "dashboard", language), record, state_path(company_dir)],
        changes=[pick_text(language, "已刷新产品状态、版本、缺口和上线信息。", "Refreshed product state, version, gaps, and launch information.")],
        language=language,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
