#!/usr/bin/env python3
"""Run a runtime preflight check for One Person Company OS."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import emit_runtime_report, load_state, preflight_status, print_step
from localization import normalize_language, pick_text
from workspace_layout import existing_state_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check runtime readiness and persistence status for One Person Company OS.")
    parser.add_argument("--mode", default="创建公司", help="当前准备执行的模式标签")
    parser.add_argument("--company-dir", help="可选，公司工作区目录")
    parser.add_argument("--language", default="auto", help="工作语言，如 zh-CN、en-US 或 auto")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    company_dir = Path(args.company_dir).expanduser().resolve() if args.company_dir else None
    state = load_state(company_dir) if company_dir and existing_state_path(company_dir).is_file() else None
    language = normalize_language(args.language, args.mode, state.get("language") if state else None)

    print_step(1, 5, "模式判定", language=language)
    print_step(2, 5, "preflight 与保存策略检查", language=language)
    status = preflight_status(company_dir, language=language)
    print_step(3, 5, "草案 / 变更提议 / 当前状态装载", status=pick_text(language, "已完成（读取当前工作区）", "Completed (loaded the current workspace)"), language=language)
    print_step(4, 5, "执行与落盘", status=pick_text(language, "跳过（本次只做预检与策略判定）", "Skipped (this run only performs preflight and strategy selection)"), language=language)

    stage = pick_text(language, "未确认", "Unconfirmed")
    round_name = pick_text(language, "未确认", "Unconfirmed")
    role = pick_text(language, "总控台", "Control Tower")
    next_action = pick_text(language, "环境可运行后再执行正式创建或更新", "Run the formal creation or update after the environment becomes runnable")
    if company_dir and status["workspace_created"] and status["persisted"]:
        state = state or load_state(company_dir)
        stage = state.get("stage_label", stage)
        round_name = state.get("current_round", {}).get("name", round_name)
        role = state.get("current_round", {}).get("owner_role_name", role)
        next_action = state.get("current_round", {}).get("next_action", next_action)

    if status["recommended_mode_id"] == "script-execution-switch-python":
        next_action = pick_text(language, "优先让 OpenClaw 智能体切换到兼容 Python 后重跑脚本", "Ask the OpenClaw agent to switch to a compatible Python runtime and rerun the script")
    elif status["recommended_mode_id"] == "manual-persistence" and not status["python_supported"] and status["writable"]:
        next_action = pick_text(language, "先查看 scripts/ensure_python_runtime.py 给出的兼容解释器与手动安装方案；若当前环境不便安装，再切到手动落盘", "Review the compatible-runtime and manual-install guidance from scripts/ensure_python_runtime.py first; if installation is not practical, switch to manual persistence")
    elif status["recommended_mode_id"] == "manual-persistence":
        next_action = pick_text(language, "跳过脚本执行，直接手动写入 markdown/json 到工作区", "Skip script execution and write markdown/json into the workspace directly")
    if status["recommended_mode_id"] == "chat-only":
        next_action = pick_text(language, "先解释当前内容未保存，再等待用户确认或修复环境", "Explain that nothing is persisted yet, then wait for user approval or an environment fix")

    print_step(5, 5, "验证与回报", language=language)
    emit_runtime_report(
        mode=args.mode if args.mode else pick_text(language, "创建公司", "Create Company"),
        phase="验证与回报",
        stage=stage,
        round_name=round_name,
        role=role,
        artifact=pick_text(language, "运行环境检查结果", "Runtime preflight result"),
        next_action=next_action,
        needs_confirmation=pick_text(language, "否", "No"),
        persistence_mode=status["recommended_mode_id"],
        company_dir=company_dir,
        saved_paths=[],
        unsaved_reason=pick_text(language, "本次仅执行预检，没有新增落盘", "This run only executed preflight checks and did not persist new files"),
        work_scope=[
            pick_text(language, "检查当前环境能不能直接运行脚本。", "Check whether the current environment can run the scripts directly."),
            pick_text(language, "判断现在该走脚本执行、手动落盘还是纯对话推进。", "Decide whether this run should use script execution, manual persistence, or chat-only progression."),
            pick_text(language, "把保存状态和恢复动作翻译成用户可理解的话。", "Translate persistence status and recovery actions into plain user-facing language."),
        ],
        non_scope=[
            pick_text(language, "不会在这一步创建新公司文件。", "Do not create new company files in this step."),
            pick_text(language, "不会把预检结果冒充成正式执行结果。", "Do not present preflight output as formal execution output."),
        ],
        changes=[
            pick_text(language, f"已确认当前推荐执行模式为 {status['recommended_mode']}。", f"Confirmed that the recommended execution mode is {status['recommended_mode']}."),
            pick_text(language, "本次没有写入新文件，只更新了对环境与保存策略的判断。", "No new files were written in this run; only the environment and persistence strategy assessment was updated."),
        ],
        language=language,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
