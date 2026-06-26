#!/usr/bin/env python3
"""Upgrade an existing workspace into the business-loop layout."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import emit_runtime_report, load_state, preflight_status, print_step, render_workspace, root_doc_path, save_state, state_path
from localization import pick_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="迁移现有工作区到经营闭环骨架。")
    parser.add_argument("company_dir", help="公司工作区目录")
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
    print_step(3, 5, "草案 / 变更提议 / 当前状态装载", status=pick_text(language, "已完成（升级状态）", "Completed (upgraded state)"), language=language)
    print_step(4, 5, "执行与落盘", language=language)
    save_state(company_dir, state)
    render_workspace(company_dir, state)
    print_step(5, 5, "验证与回报", language=language)
    emit_runtime_report(
        mode=pick_text(language, "迁移工作区", "Migrate Workspace"),
        phase="验证与回报",
        stage=pick_text(language, "v1.0 经营闭环", "v1.0 Business Loop"),
        round_name=pick_text(language, "经营推进", "Operating Push"),
        role=pick_text(language, "经营总控", "Operating Lead"),
        artifact=pick_text(language, "经营闭环工作区", "Business-loop workspace"),
        next_action=state["focus"]["today_action"],
        needs_confirmation=pick_text(language, "否", "No"),
        persistence_mode="script-execution",
        company_dir=company_dir,
        saved_paths=[
            root_doc_path(company_dir, "dashboard", language),
            root_doc_path(company_dir, "offer", language),
            root_doc_path(company_dir, "product_status", language),
            root_doc_path(company_dir, "delivery_cash", language),
            state_path(company_dir),
        ],
        changes=[pick_text(language, "已把旧工作区迁移到 v1.0 经营闭环骨架；旧阶段/回合资料只作为历史材料保留。", "Migrated the legacy workspace to the v1.0 business-loop layout; old stage/round material is kept only as history.")],
        language=language,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
