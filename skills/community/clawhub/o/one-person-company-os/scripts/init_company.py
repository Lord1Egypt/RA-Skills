#!/usr/bin/env python3
"""Initialize a Chinese-first One Person Company OS workspace."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    artifact_dir_path,
    emit_runtime_report,
    now_string,
    preflight_status,
    print_step,
    render_workspace,
    root_doc_path,
    safe_workspace_name,
    save_state,
    state_path,
    workspace_file_path,
)
from localization import normalize_language, pick_text
from state_v3 import default_state_v3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a One Person Company OS workspace.")
    parser.add_argument("company_name", help="公司名称")
    parser.add_argument("--path", required=True, help="工作区父目录")
    parser.add_argument("--product-name", default="未命名产品", help="产品名称")
    parser.add_argument("--stage", default="", help="旧版兼容参数；v1.0 不再写入阶段状态")
    parser.add_argument("--target-user", default="待确认用户", help="目标用户")
    parser.add_argument("--core-problem", default="待确认核心问题", help="核心问题")
    parser.add_argument("--product-pitch", default="待补充产品一句话定义", help="产品一句话定义")
    parser.add_argument("--company-goal", default="先跑通最小闭环并拿到第一轮真实反馈", help="当前主目标")
    parser.add_argument("--current-bottleneck", default="尚未识别当前主瓶颈", help="当前瓶颈")
    parser.add_argument("--language", default="auto", help="工作语言，如 zh-CN、en-US 或 auto")
    parser.add_argument("--confirmed", action="store_true", help="确认创始人已确认方向与创建草案")
    parser.add_argument("--force", action="store_true", help="允许写入已存在目录")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    language = normalize_language(
        args.language,
        args.company_name,
        args.product_name,
        args.stage,
        args.target_user,
        args.core_problem,
        args.product_pitch,
    )
    if args.product_name == "未命名产品" and language == "en-US":
        args.product_name = "Untitled Product"
    if args.target_user == "待确认用户" and language == "en-US":
        args.target_user = "Target user to be confirmed"
    if args.core_problem == "待确认核心问题" and language == "en-US":
        args.core_problem = "Core problem to be confirmed"
    if args.product_pitch == "待补充产品一句话定义" and language == "en-US":
        args.product_pitch = "Add the one-line product pitch"
    if args.company_goal == "先跑通最小闭环并拿到第一轮真实反馈" and language == "en-US":
        args.company_goal = "Ship the smallest useful loop and collect the first real feedback"
    if args.current_bottleneck == "尚未识别当前主瓶颈" and language == "en-US":
        args.current_bottleneck = "The primary bottleneck has not been identified yet"
    if not args.confirmed:
        parser.error(
            pick_text(
                language,
                "初始化前必须先确认创业方向与创建草案。先和创始人澄清一句话想法、首批买家与核心问题，确认后再带上 --confirmed 创建工作区。",
                "Direction confirmation is required before initialization. Clarify the one-line idea, first buyer, and core problem with the founder, then rerun with --confirmed to create the workspace.",
            )
        )

    placeholder_values = {
        "product_name": {"未命名产品", "Untitled Product"},
        "target_user": {"待确认用户", "Target user to be confirmed"},
        "core_problem": {"待确认核心问题", "Core problem to be confirmed"},
        "product_pitch": {"待补充产品一句话定义", "Add the one-line product pitch"},
    }
    missing_fields = [
        key
        for key, values in placeholder_values.items()
        if getattr(args, key) in values
    ]
    if missing_fields:
        parser.error(
            pick_text(
                language,
                f"创建前还缺少关键信息：{', '.join(missing_fields)}。请先补齐方向草案，再执行初始化。",
                f"Key founder inputs are still missing before creation: {', '.join(missing_fields)}. Complete the direction draft first, then initialize.",
            )
        )

    print_step(1, 5, "模式判定", language=language)
    root = Path(args.path).expanduser().resolve()
    company_dir = root / safe_workspace_name(args.company_name)
    if company_dir.exists() and not args.force:
        parser.error(f"target already exists: {company_dir}")

    print_step(2, 5, "preflight 与保存策略检查", language=language)
    runtime = preflight_status(company_dir, language=language)
    if not runtime["runnable"]:
        parser.error(f"runtime not runnable: {runtime['runtime_error']}")
    if not runtime["writable"]:
        parser.error(f"target not writable: {runtime['writable_target']}")

    print_step(
        3,
        5,
        "草案 / 变更提议 / 当前状态装载",
        status=pick_text(language, "已完成（组装初始状态）", "Completed (assembled the initial state)"),
        language=language,
    )
    active_roles = ["founder-ceo", "control-tower", "product-strategist"]
    state = default_state_v3(
        company_name=args.company_name,
        product_name=args.product_name,
        language=language,
        target_user=args.target_user,
        core_problem=args.core_problem,
        product_pitch=args.product_pitch,
        company_goal=args.company_goal,
        current_bottleneck=args.current_bottleneck,
        active_roles=active_roles,
    )
    state["focus"]["today_action"] = pick_text(language, "打开经营驾驶舱，补齐价值承诺、买家和第一条成交动作", "Open the operating cockpit and complete the promise, buyer, and first revenue action")
    state["focus"]["week_outcome"] = pick_text(language, "形成可演示、可试用、可推进成交的最小经营闭环", "Create the smallest demoable, trialable, revenue-moving operating loop")

    print_step(4, 5, "执行与落盘", language=language)
    save_state(company_dir, state)
    render_workspace(company_dir, state)

    print_step(5, 5, "验证与回报", language=language)
    emit_runtime_report(
        mode="创建公司" if language == "zh-CN" else "Create Company",
        phase="验证与回报",
        stage=pick_text(language, "v1.0 经营闭环", "v1.0 Business Loop"),
        round_name=pick_text(language, "经营推进", "Operating Push"),
        role=pick_text(language, "经营总控", "Operating Lead"),
        artifact=pick_text(language, "经营驾驶舱", "Operating cockpit"),
        next_action=pick_text(language, "先进入主工作面，继续收敛价值承诺、产品和成交路径", "Enter the main work surfaces and continue tightening the offer, product, and revenue path"),
        needs_confirmation=pick_text(language, "否", "No"),
        persistence_mode="script-execution",
        company_dir=company_dir,
        saved_paths=[
            root_doc_path(company_dir, "dashboard", language),
            root_doc_path(company_dir, "founder_constraints", language),
            root_doc_path(company_dir, "offer", language),
            root_doc_path(company_dir, "pipeline", language),
            root_doc_path(company_dir, "product_status", language),
            root_doc_path(company_dir, "delivery_cash", language),
            workspace_file_path(company_dir, "role_index", language),
            artifact_dir_path(company_dir, "delivery", language) / pick_text(language, "01-实际产出总表.docx", "01-actual-deliverables-index.docx"),
            state_path(company_dir),
        ],
        work_scope=[
            pick_text(language, "创建一人公司 v1.0 经营工作区与状态文件。", "Create the one-person-company v1.0 operating workspace and state file."),
            pick_text(language, "直接生成经营驾驶舱、价值承诺、成交管道、产品状态、交付回款和视觉素材。", "Generate the operating cockpit, offer, revenue pipeline, product status, delivery plus cash, and visual assets."),
            pick_text(language, "明确这次是否已真实保存以及下一步怎么继续。", "Explain clearly what was persisted and what should happen next."),
        ],
        non_scope=[
            pick_text(language, "不会替创始人自动做高风险商业决策。", "Do not make high-risk business decisions on behalf of the founder."),
            pick_text(language, "不会跳过确认边界去伪造不存在的角色执行结果。", "Do not fake role execution outcomes by skipping approval boundaries."),
        ],
        changes=[
            pick_text(language, "已创建经营总盘、价值承诺、成交管道、产品状态、交付回款和当前状态文件。", "Created the operating dashboard, value offer, revenue pipeline, product status, delivery plus cash view, and current-state file."),
            pick_text(language, "已把工作区切到 v1.0 经营闭环模型，不再写入旧阶段/回合字段。", "Shifted the workspace to the v1.0 business-loop model without legacy stage/round fields."),
            pick_text(language, "当前公司已进入可继续推进产品、成交、交付和回款的状态。", "The company workspace is now ready to advance product, sales, delivery, and cash collection."),
        ],
        language=language,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
