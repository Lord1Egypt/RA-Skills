r"""
workflow_state.py — 流程钩子系统

每条流程线定义前置依赖：
  line1: template → inject_params → compose → validate → report
  line2: backup → convert → branch → final_validate → report
  line3: backup → inject → final_validate → report
  line4: extract → compose → template → reuse → final_validate → report
  standalone: execute → final_validate → report （推荐流程，不强制）

特点：
  - 所有流程线最后两步强制为 final_validate + report
  - line2/line3 第一步强制为 backup（保障原文不被破坏）
  - 每步执行前 check() 验证前置，跳过则报错
  - standalone 模式的 validate + report 为推荐（非强制）
  - 状态持久化在 scripts/.workflow/ 目录
"""

import json
import os
import sys
from pathlib import Path


# ── 流程线步骤定义 ──────────────────────────────────────
WORKFLOW_DEFS = {
    "line1": {
        "label": "新建文档",
        "steps": ["template", "inject_params", "compose", "validate", "report"],
        "deps": {
            "template": [],
            "inject_params": ["template"],
            "compose": ["template", "inject_params"],
            "validate": ["compose"],
            "report": ["validate"],
        },
        "backup_required": False,
        "validate_always": True,
    },
    "line2": {
        "label": "改造",
        "steps": ["backup", "convert", "branch", "final_validate", "report"],
        "deps": {
            "backup": [],
            "convert": ["backup"],
            "branch": ["backup", "convert"],
            "final_validate": ["backup", "convert", "branch"],
            "report": ["backup", "convert", "branch", "final_validate"],
        },
        "backup_required": True,
        "validate_always": True,
    },
    "line3": {
        "label": "增量编辑",
        "steps": ["backup", "inject", "final_validate", "report"],
        "deps": {
            "backup": [],
            "inject": ["backup"],
            "final_validate": ["backup", "inject"],
            "report": ["backup", "inject", "final_validate"],
        },
        "backup_required": True,
        "validate_always": True,
    },
    "line4": {
        "label": "组件复用",
        "steps": ["extract", "compose", "template", "reuse", "final_validate", "report"],
        "deps": {
            "extract": [],
            "compose": ["extract"],
            "template": ["extract", "compose"],
            "reuse": ["extract", "compose", "template"],
            "final_validate": ["extract", "compose", "template", "reuse"],
            "report": ["extract", "compose", "template", "reuse", "final_validate"],
        },
        "backup_required": False,
        "validate_always": True,
    },
    "standalone": {
        "label": "独立模式",
        "steps": ["execute", "final_validate", "report"],
        "deps": {
            "execute": [],
            "final_validate": ["execute"],
            "report": ["execute", "final_validate"],
        },
        "backup_required": False,
        "validate_always": False,  # 推荐但不强制
    },
}

STATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "scripts", ".workflow")


def _state_path(workflow_id: str) -> str:
    os.makedirs(STATE_DIR, exist_ok=True)
    return os.path.join(STATE_DIR, f"{workflow_id}.json")


def init(workflow_id: str, params: dict = None) -> dict:
    """初始化一条流程线的状态"""
    wf = WORKFLOW_DEFS.get(workflow_id)
    if not wf:
        return {"error": f"未知流程线: {workflow_id}", "success": False}

    state = {
        "workflow": workflow_id,
        "label": wf["label"],
        "steps": {s: "pending" for s in wf["steps"]},
        "params": params or {},
        "step_order": wf["steps"],
    }

    path = _state_path(workflow_id)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return {"error": f"写入状态文件失败: {e}", "success": False}

    return {"success": True, "state": state}


def check(workflow_id: str, step_name: str) -> dict:
    """检查指定步骤是否可以执行（前置步骤是否全部完成）"""
    wf = WORKFLOW_DEFS.get(workflow_id)
    if not wf:
        return {"allowed": False, "error": f"未知流程线: {workflow_id}"}

    path = _state_path(workflow_id)
    if not os.path.isfile(path):
        return {"allowed": False, "error": f"流程线 {workflow_id} 未初始化，请先运行 init"}

    try:
        with open(path, "r", encoding="utf-8") as f:
            state = json.load(f)
    except Exception as e:
        return {"allowed": False, "error": f"读取状态文件失败: {e}"}

    deps = wf["deps"].get(step_name, [])
    pending_deps = [d for d in deps if state["steps"].get(d) != "completed"]

    if pending_deps:
        return {
            "allowed": False,
            "error": f"前置步骤未完成: {', '.join(pending_deps)}",
            "pending": pending_deps,
            "step_status": state["steps"].get(step_name, "unknown"),
        }

    return {"allowed": True, "step_status": state["steps"].get(step_name, "pending")}


def complete(workflow_id: str, step_name: str) -> dict:
    """标记指定步骤为已完成"""
    path = _state_path(workflow_id)
    if not os.path.isfile(path):
        return {"error": f"流程线 {workflow_id} 未初始化", "success": False}

    try:
        with open(path, "r", encoding="utf-8") as f:
            state = json.load(f)
    except Exception as e:
        return {"error": f"读取状态文件失败: {e}", "success": False}

    if step_name not in state["steps"]:
        return {"error": f"步骤 {step_name} 不属于流程线 {workflow_id}", "success": False}

    state["steps"][step_name] = "completed"

    # 检查是否全部完成
    all_done = all(v == "completed" for v in state["steps"].values())
    state["all_completed"] = all_done

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return {"error": f"写入状态文件失败: {e}", "success": False}

    return {"success": True, "all_completed": all_done, "state": state}


def status(workflow_id: str) -> dict:
    """查询流程线当前状态"""
    path = _state_path(workflow_id)
    if not os.path.isfile(path):
        return {"error": f"流程线 {workflow_id} 未初始化", "success": False}

    with open(path, "r", encoding="utf-8") as f:
        state = json.load(f)

    return {"success": True, "state": state}


def guard(workflow_id: str, step_name: str) -> bool:
    """守卫函数：检查并尝试通过。用于脚本入口处。
    
    逻辑：
    1. 如果状态文件不存在 → 自动初始化
    2. 检查前置步骤 → 不满足则报错退出
    3. 检查当前步骤状态 → 如果已完成则警告
    4. 返回 True 表示可以继续
    """
    path = _state_path(workflow_id)

    # 自动初始化
    if not os.path.isfile(path):
        init(workflow_id)

    # 检查前置
    c = check(workflow_id, step_name)
    if not c["allowed"]:
        print(f"[guard] ⛔ 流程 {workflow_id} 步骤 {step_name} 被拦截")
        print(f"[guard]    原因: {c['error']}")
        print(f"[guard]    请先完成前置步骤: {c.get('pending', [])}")
        return False

    # 如果已标记完成
    if c.get("step_status") == "completed":
        print(f"[guard] ⚠ 步骤 {step_name} 已标记为完成，请确认是否需要重复执行")

    return True


def advance(workflow_id: str, step_name: str) -> dict:
    """守卫 + 自动标记完成的组合函数"""
    g = guard(workflow_id, step_name)
    if not g:
        return {"success": False, "error": "守卫拦截"}

    # 调用方执行完毕后应调用 complete
    return {"success": True, "action": "proceed"}


def print_status(workflow_id: str):
    """打印流程线状态"""
    s = status(workflow_id)
    if not s["success"]:
        print(f"[workflow] {s['error']}")
        return

    st = s["state"]
    print(f"[workflow] 流程线: {st['workflow']} ({st['label']})")
    print(f"[workflow] 步骤状态:")
    for step_name in st.get("step_order", []):
        status_icon = {"completed": "✅", "pending": "⬜", "in_progress": "🔄"}.get(
            st["steps"].get(step_name, "pending"), "⬜")
        print(f"  {status_icon} {step_name}: {st['steps'].get(step_name, 'pending')}")
    if st.get("all_completed"):
        print(f"[workflow] 🎉 全部步骤已完成!")


# ── CLI ──────────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description="流程钩子系统")
    parser.add_argument("action", choices=["init", "check", "complete", "status", "advance"],
                        help="操作")
    parser.add_argument("--workflow", "-w", required=True, help="流程线 ID")
    parser.add_argument("--step", "-s", default="", help="步骤名")
    parser.add_argument("--param", "-p", default="", help="初始化参数 (JSON)")

    args = parser.parse_args()

    if args.action == "init":
        params = json.loads(args.param) if args.param else {}
        r = init(args.workflow, params)
        if r["success"]:
            print(f"[workflow] 流程线 {args.workflow} 已初始化")
            print_status(args.workflow)
        else:
            print(f"[workflow] 初始化失败: {r.get('error')}")
            sys.exit(1)

    elif args.action == "check":
        if not args.step:
            print("[workflow] --step 是必填参数")
            sys.exit(1)
        r = check(args.workflow, args.step)
        if r["allowed"]:
            print(f"[workflow] ✅ 步骤 {args.step} 可以执行")
        else:
            print(f"[workflow] ⛔ {r['error']}")
            sys.exit(1)

    elif args.action == "complete":
        if not args.step:
            print("[workflow] --step 是必填参数")
            sys.exit(1)
        r = complete(args.workflow, args.step)
        if r["success"]:
            print(f"[workflow] ✅ 步骤 {args.step} 已完成")
            if r.get("all_completed"):
                print(f"[workflow] 🎉 流程线 {args.workflow} 全部完成!")
        else:
            print(f"[workflow] 标记失败: {r.get('error')}")
            sys.exit(1)

    elif args.action == "status":
        print_status(args.workflow)

    elif args.action == "advance":
        if not args.step:
            print("[workflow] --step 是必填参数")
            sys.exit(1)
        r = advance(args.workflow, args.step)
        if r["success"]:
            print(f"[workflow] ✅ 守卫通过，步骤 {args.step} 可以执行")
            print(f"[workflow]    执行完成后请调用: workflow_state.py complete -w {args.workflow} -s {args.step}")
        else:
            print(f"[workflow] ⛔ {r.get('error', '守卫拦截')}")
            sys.exit(1)


if __name__ == "__main__":
    main()
