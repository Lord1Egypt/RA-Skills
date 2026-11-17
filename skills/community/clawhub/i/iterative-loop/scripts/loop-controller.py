#!/usr/bin/env python3
"""
loop-controller.py — 迭代循环控制器

管理迭代循环的状态、条件检测和生命周期。
借鉴 Claude Code Ralph Wiggum 的 Stop Hook 自引用循环模式。

子命令:
  init     - 初始化新的迭代循环
  check    - 检查是否应继续迭代
  update   - 更新当前迭代的结果
  complete - 标记循环完成

用法:
  python loop-controller.py init --name "task" --mode max --max 10
  python loop-controller.py check --state loop-state.json
  python loop-controller.py update --state loop-state.json --result pass --summary "done"
  python loop-controller.py complete --state loop-state.json --reason "目标达成"
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


# ─── 常量 ───────────────────────────────────────────────────────────────────

DEFAULT_STATE_FILE = "loop-state.json"
VALID_MODES = ("fixed", "max", "adaptive")
VALID_RESULTS = ("pass", "fail", "partial")
VALID_STATUSES = ("running", "completed", "failed", "cancelled")
DEFAULT_PATIENCE = 3


# ─── 工具函数 ────────────────────────────────────────────────────────────────

def load_state(path: str) -> dict:
    """加载状态文件，返回解析后的字典。文件不存在或格式错误时退出。"""
    p = Path(path)
    if not p.exists():
        error_exit(f"状态文件不存在: {path}")
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        error_exit(f"状态文件格式错误: {e}")
    except OSError as e:
        error_exit(f"读取状态文件失败: {e}")


def save_state(path: str, state: dict) -> None:
    """将状态字典写入文件。"""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except OSError as e:
        error_exit(f"写入状态文件失败: {e}")


def error_exit(msg: str, code: int = 1) -> None:
    """输出错误 JSON 并退出。"""
    print(json.dumps({"error": msg, "success": False}, ensure_ascii=False))
    sys.exit(code)


def output_result(data: dict) -> None:
    """输出结果 JSON 到 stdout。"""
    data["success"] = True
    print(json.dumps(data, ensure_ascii=False, indent=2))


def now_iso() -> str:
    """返回当前 UTC 时间的 ISO 格式字符串。"""
    return datetime.now(timezone.utc).isoformat()


# ─── 子命令实现 ──────────────────────────────────────────────────────────────

def cmd_init(args: argparse.Namespace) -> None:
    """初始化新的迭代循环。"""
    # 验证模式
    mode = args.mode
    if mode not in VALID_MODES:
        error_exit(f"无效模式 '{mode}'，可选: {', '.join(VALID_MODES)}")

    # 验证最大次数
    max_iter = args.max
    if max_iter < 1:
        error_exit("--max 必须 >= 1")

    # 解析完成条件
    completion_check = {"type": "none", "pattern": ""}
    if args.condition:
        if ":" in args.condition:
            ctype, pattern = args.condition.split(":", 1)
            ctype = ctype.strip().lower()
            if ctype not in ("regex", "file", "file-changed", "llm"):
                error_exit(f"无效条件类型 '{ctype}'，可选: regex, file, file-changed, llm")
            completion_check = {"type": ctype, "pattern": pattern.strip()}
        else:
            error_exit("条件格式错误，应为 'type:pattern'，如 'regex:BUILD SUCCESS'")

    # adaptive 模式的 patience
    patience = args.patience if args.patience else DEFAULT_PATIENCE

    # 构建初始状态
    state = {
        "name": args.name,
        "mode": mode,
        "max_iterations": max_iter,
        "current_iteration": 0,
        "completion_check": completion_check,
        "patience": patience,
        "no_improvement_count": 0,
        "history": [],
        "artifacts": [],
        "status": "running",
        "metadata": {},
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }

    # 写入状态文件
    state_path = args.state or DEFAULT_STATE_FILE
    save_state(state_path, state)

    output_result({
        "action": "init",
        "state_file": state_path,
        "name": args.name,
        "mode": mode,
        "max_iterations": max_iter,
        "message": f"循环已初始化: {args.name} (模式={mode}, 最大={max_iter})"
    })


def cmd_check(args: argparse.Namespace) -> None:
    """检查是否应继续迭代。"""
    state_path = args.state or DEFAULT_STATE_FILE
    state = load_state(state_path)

    # 检查状态
    if state["status"] != "running":
        output_result({
            "action": "check",
            "should_continue": False,
            "reason": f"循环已停止 (status={state['status']})",
            "iteration": state["current_iteration"],
        })
        return

    current = state["current_iteration"]
    max_iter = state["max_iterations"]
    mode = state["mode"]

    # fixed 模式：只看次数
    if mode == "fixed":
        should_continue = current < max_iter
        output_result({
            "action": "check",
            "should_continue": should_continue,
            "iteration": current,
            "max_iterations": max_iter,
            "remaining": max(0, max_iter - current),
            "reason": "固定次数未用完" if should_continue else "已达最大次数",
        })
        return

    # max 模式：次数 + 完成条件
    if mode == "max":
        if current >= max_iter:
            output_result({
                "action": "check",
                "should_continue": False,
                "iteration": current,
                "reason": "已达最大迭代次数",
            })
            return

        # 检查完成条件
        check = state.get("completion_check", {})
        condition_met = evaluate_condition(check, state)

        output_result({
            "action": "check",
            "should_continue": not condition_met,
            "iteration": current,
            "max_iterations": max_iter,
            "condition_met": condition_met,
            "reason": "完成条件已满足" if condition_met else "继续迭代",
        })
        return

    # adaptive 模式：次数 + 自适应改进检测
    if mode == "adaptive":
        if current >= max_iter:
            output_result({
                "action": "check",
                "should_continue": False,
                "iteration": current,
                "reason": "已达最大迭代次数",
            })
            return

        patience = state.get("patience", DEFAULT_PATIENCE)
        no_improve = state.get("no_improvement_count", 0)

        if no_improve >= patience:
            output_result({
                "action": "check",
                "should_continue": False,
                "iteration": current,
                "no_improvement_count": no_improve,
                "patience": patience,
                "reason": f"连续 {no_improve} 轮无改进 (patience={patience})",
            })
            return

        output_result({
            "action": "check",
            "should_continue": True,
            "iteration": current,
            "no_improvement_count": no_improve,
            "patience": patience,
            "remaining": max(0, max_iter - current),
            "reason": "继续迭代",
        })
        return


def cmd_update(args: argparse.Namespace) -> None:
    """更新当前迭代的结果。"""
    state_path = args.state or DEFAULT_STATE_FILE
    state = load_state(state_path)

    if state["status"] != "running":
        error_exit(f"循环已停止 (status={state['status']})，无法更新")

    result = args.result
    if result not in VALID_RESULTS:
        error_exit(f"无效结果 '{result}'，可选: {', '.join(VALID_RESULTS)}")

    # 推进迭代计数
    state["current_iteration"] += 1
    current = state["current_iteration"]

    # 记录历史
    entry = {
        "iteration": current,
        "timestamp": now_iso(),
        "result": result,
        "summary": args.summary or "",
    }
    if args.metrics:
        try:
            entry["metrics"] = json.loads(args.metrics)
        except json.JSONDecodeError:
            error_exit("--metrics 必须是有效的 JSON 字符串")

    state["history"].append(entry)

    # adaptive 模式：更新无改进计数
    if state["mode"] == "adaptive":
        if result == "pass":
            state["no_improvement_count"] = 0
        elif result == "partial":
            # partial 算半个改进，不重置计数
            pass
        else:  # fail
            state["no_improvement_count"] = state.get("no_improvement_count", 0) + 1

    # 更新 artifacts
    if args.artifact:
        if args.artifact not in state["artifacts"]:
            state["artifacts"].append(args.artifact)

    state["updated_at"] = now_iso()
    save_state(state_path, state)

    output_result({
        "action": "update",
        "iteration": current,
        "result": result,
        "message": f"迭代 {current} 已记录 (result={result})",
    })


def cmd_complete(args: argparse.Namespace) -> None:
    """标记循环完成。"""
    state_path = args.state or DEFAULT_STATE_FILE
    state = load_state(state_path)

    reason = args.reason or "手动完成"
    status = args.status if args.status else "completed"

    if status not in VALID_STATUSES:
        error_exit(f"无效状态 '{status}'，可选: {', '.join(VALID_STATUSES)}")

    state["status"] = status
    state["completion_reason"] = reason
    state["completed_at"] = now_iso()
    state["updated_at"] = now_iso()

    save_state(state_path, state)

    # 生成摘要
    total = state["current_iteration"]
    history = state.get("history", [])
    passes = sum(1 for h in history if h.get("result") == "pass")
    fails = sum(1 for h in history if h.get("result") == "fail")

    output_result({
        "action": "complete",
        "status": status,
        "reason": reason,
        "total_iterations": total,
        "passes": passes,
        "fails": fails,
        "message": f"循环已完成: {total} 轮迭代, {passes} 通过, {fails} 失败",
    })


# ─── 条件评估 ────────────────────────────────────────────────────────────────

def evaluate_condition(check: dict, state: dict) -> bool:
    """
    评估完成条件是否满足。

    返回 True 表示条件已满足（应停止迭代）。
    """
    ctype = check.get("type", "none")
    pattern = check.get("pattern", "")

    if ctype == "none":
        return False

    if ctype == "regex":
        # 在最后一轮的 summary 中匹配正则
        history = state.get("history", [])
        if not history:
            return False
        last_summary = history[-1].get("summary", "")
        try:
            return bool(re.search(pattern, last_summary))
        except re.error:
            return False

    if ctype == "file":
        # 检查文件是否存在
        return Path(pattern).exists()

    if ctype == "file-changed":
        # 检查文件是否在最近一轮被修改
        p = Path(pattern)
        if not p.exists():
            return False
        history = state.get("history", [])
        if not history:
            return False
        # 比较文件修改时间和最后一轮的时间戳
        try:
            mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
            last_time = datetime.fromisoformat(history[-1]["timestamp"])
            return mtime > last_time
        except (OSError, ValueError):
            return False

    if ctype == "llm":
        # LLM 判断需要外部处理，这里返回 False 让调用者处理
        return False

    return False


# ─── 参数解析 ────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        description="迭代循环控制器 — 管理迭代状态和生命周期",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # init
    p_init = subparsers.add_parser("init", help="初始化新的迭代循环")
    p_init.add_argument("--name", required=True, help="循环任务名称")
    p_init.add_argument("--mode", default="max", choices=VALID_MODES, help="迭代模式 (默认: max)")
    p_init.add_argument("--max", type=int, default=10, help="最大迭代次数 (默认: 10)")
    p_init.add_argument("--condition", help="完成条件，格式: type:pattern")
    p_init.add_argument("--patience", type=int, help="adaptive 模式的耐心值 (默认: 3)")
    p_init.add_argument("--state", help="状态文件路径 (默认: loop-state.json)")

    # check
    p_check = subparsers.add_parser("check", help="检查是否应继续迭代")
    p_check.add_argument("--state", help="状态文件路径 (默认: loop-state.json)")

    # update
    p_update = subparsers.add_parser("update", help="更新当前迭代结果")
    p_update.add_argument("--state", help="状态文件路径 (默认: loop-state.json)")
    p_update.add_argument("--result", required=True, choices=VALID_RESULTS, help="本轮结果")
    p_update.add_argument("--summary", help="本轮摘要")
    p_update.add_argument("--metrics", help="指标数据 (JSON 字符串)")
    p_update.add_argument("--artifact", help="产出文件路径")

    # complete
    p_complete = subparsers.add_parser("complete", help="标记循环完成")
    p_complete.add_argument("--state", help="状态文件路径 (默认: loop-state.json)")
    p_complete.add_argument("--reason", help="完成原因")
    p_complete.add_argument("--status", choices=VALID_STATUSES, help="最终状态 (默认: completed)")

    return parser


# ─── 主入口 ──────────────────────────────────────────────────────────────────

def main() -> None:
    """主入口：解析参数并分发到对应子命令。"""
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "init": cmd_init,
        "check": cmd_check,
        "update": cmd_update,
        "complete": cmd_complete,
    }

    handler = commands.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
