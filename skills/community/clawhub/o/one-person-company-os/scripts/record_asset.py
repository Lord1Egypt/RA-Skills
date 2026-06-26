#!/usr/bin/env python3
"""Record reusable assets or automation."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import emit_runtime_report, load_state, preflight_status, print_step, render_workspace, root_doc_path, save_state, state_path, workspace_file_path, write_record
from localization import pick_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="记录资产沉淀。")
    parser.add_argument("company_dir", help="公司工作区目录")
    parser.add_argument("--kind", required=True, choices=["sops", "templates", "cases", "automations", "reusable_code"], help="资产类型")
    parser.add_argument("--item", required=True, help="资产内容")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    company_dir = Path(args.company_dir).expanduser().resolve()
    state = load_state(company_dir)
    language = state["language"]
    assets = state["assets"]

    print_step(1, 5, "模式判定", language=language)
    print_step(2, 5, "preflight 与保存策略检查", language=language)
    runtime = preflight_status(company_dir, language=language)
    if not runtime["runnable"]:
        parser.error(f"runtime not runnable: {runtime['runtime_error']}")
    print_step(3, 5, "草案 / 变更提议 / 当前状态装载", status=pick_text(language, "已完成（加载当前状态）", "Completed (loaded current state)"), language=language)

    bucket = assets.setdefault(args.kind, [])
    if args.item not in bucket:
        bucket.append(args.item)
    state["focus"]["primary_arena"] = "asset"

    print_step(4, 5, "执行与落盘", language=language)
    save_state(company_dir, state)
    render_workspace(company_dir, state)
    record = write_record(
        company_dir,
        "经营日志",
        "record-asset",
        pick_text(language, "记录资产沉淀", "Recorded Asset"),
        [pick_text(language, f"- 类型: {args.kind}", f"- Kind: {args.kind}"), pick_text(language, f"- 内容: {args.item}", f"- Item: {args.item}")],
    )
    print_step(5, 5, "验证与回报", language=language)
    emit_runtime_report(
        mode=pick_text(language, "记录资产沉淀", "Record Asset"),
        phase="验证与回报",
        stage=pick_text(language, "v1.0 经营闭环", "v1.0 Business Loop"),
        round_name=pick_text(language, "经营推进", "Operating Push"),
        role=pick_text(language, "经营总控", "Operating Lead"),
        artifact=pick_text(language, "资产与自动化", "Assets and automation"),
        next_action=state["focus"]["today_action"],
        needs_confirmation=pick_text(language, "否", "No"),
        persistence_mode="script-execution",
        company_dir=company_dir,
        saved_paths=[root_doc_path(company_dir, "assets_automation", language), workspace_file_path(company_dir, "assets_inventory", language), record, state_path(company_dir)],
        changes=[pick_text(language, "已把新的 SOP、模板、案例、自动化或代码资产写入工作区。", "Wrote a new SOP, template, case, automation, or code asset into the workspace.")],
        language=language,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
