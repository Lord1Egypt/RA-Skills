#!/usr/bin/env python3
"""pipeline_state.py — auto-research skill 的轻量级状态机

参考 AutoResearchClaw/researchclaw/pipeline/stages.py + runner.py，
提取核心机制，适配 OpenClaw skill 场景（Agent 通过 exec 调用）。

核心能力:
1. Checkpoint — 每个 Stage 完成后原子写入 checkpoint.json
2. Resume — 读取 checkpoint 自动定位到下一个 Stage
3. Gate — 3 个关键阶段(S5/S9/S20)需要确认后才继续
4. Rollback — S15 PIVOT/REFINE 决策触发回退
5. Stage 状态追踪 — 完整的 stage_history.jsonl 记录

用法 (Agent 通过 exec 调用):
    # 初始化运行
    python3 pipeline_state.py init --run-dir ./artifacts/ar-xxx/

    # 查询当前状态（Agent 每个 Stage 开始前调用）
    python3 pipeline_state.py status --run-dir ./artifacts/ar-xxx/

    # 标记 Stage 完成
    python3 pipeline_state.py complete --run-dir ./artifacts/ar-xxx/ --stage 1

    # 标记 Stage 失败
    python3 pipeline_state.py fail --run-dir ./artifacts/ar-xxx/ --stage 1 --error "描述"

    # Gate 审批（S5/S9/S20）
    python3 pipeline_state.py gate --run-dir ./artifacts/ar-xxx/ --stage 5 --action approve
    python3 pipeline_state.py gate --run-dir ./artifacts/ar-xxx/ --stage 5 --action reject

    # S15 决策
    python3 pipeline_state.py decide --run-dir ./artifacts/ar-xxx/ --decision proceed
    python3 pipeline_state.py decide --run-dir ./artifacts/ar-xxx/ --decision pivot
    python3 pipeline_state.py decide --run-dir ./artifacts/ar-xxx/ --decision refine

    # 查看完整历史
    python3 pipeline_state.py history --run-dir ./artifacts/ar-xxx/
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
from datetime import datetime, timezone
from enum import IntEnum
from pathlib import Path
from typing import Any


# ============================================================
# Stage 定义 (同 AutoResearchClaw)
# ============================================================

class Stage(IntEnum):
    TOPIC_INIT = 1
    PROBLEM_DECOMPOSE = 2
    SEARCH_STRATEGY = 3
    LITERATURE_COLLECT = 4
    LITERATURE_SCREEN = 5        # GATE
    KNOWLEDGE_EXTRACT = 6
    SYNTHESIS = 7
    HYPOTHESIS_GEN = 8
    EXPERIMENT_DESIGN = 9        # GATE
    CODE_GENERATION = 10
    RESOURCE_PLANNING = 11
    EXPERIMENT_RUN = 12
    ITERATIVE_REFINE = 13
    RESULT_ANALYSIS = 14
    RESEARCH_DECISION = 15       # 决策点
    PAPER_OUTLINE = 16
    PAPER_DRAFT = 17
    PEER_REVIEW = 18
    PAPER_REVISION = 19
    QUALITY_GATE = 20            # GATE
    KNOWLEDGE_ARCHIVE = 21
    EXPORT_PUBLISH = 22
    CITATION_VERIFY = 23


STAGE_NAMES = {
    1: "TOPIC_INIT",         2: "PROBLEM_DECOMPOSE",
    3: "SEARCH_STRATEGY",    4: "LITERATURE_COLLECT",
    5: "LITERATURE_SCREEN",  6: "KNOWLEDGE_EXTRACT",
    7: "SYNTHESIS",          8: "HYPOTHESIS_GEN",
    9: "EXPERIMENT_DESIGN",  10: "CODE_GENERATION",
    11: "RESOURCE_PLANNING", 12: "EXPERIMENT_RUN",
    13: "ITERATIVE_REFINE",  14: "RESULT_ANALYSIS",
    15: "RESEARCH_DECISION", 16: "PAPER_OUTLINE",
    17: "PAPER_DRAFT",       18: "PEER_REVIEW",
    19: "PAPER_REVISION",    20: "QUALITY_GATE",
    21: "KNOWLEDGE_ARCHIVE", 22: "EXPORT_PUBLISH",
    23: "CITATION_VERIFY",
}

PHASE_MAP = {
    "A: Research Scoping": [1, 2],
    "B: Literature Discovery": [3, 4, 5, 6],
    "C: Knowledge Synthesis": [7, 8],
    "D: Experiment Design": [9, 10, 11],
    "E: Experiment Execution": [12, 13],
    "F: Analysis & Decision": [14, 15],
    "G: Paper Writing": [16, 17, 18, 19],
    "H: Finalization": [20, 21, 22, 23],
}

# Gate 阶段 — 需要确认才能继续
GATE_STAGES = {5, 9, 20}

# Gate 被拒绝时的回退目标
GATE_ROLLBACK = {
    5: 4,   # LITERATURE_SCREEN reject → 重新收集文献
    9: 8,   # EXPERIMENT_DESIGN reject → 重新生成假设
    20: 16, # QUALITY_GATE reject → 重写论文
}

# S15 RESEARCH_DECISION 的回退目标
DECISION_ROLLBACK = {
    "pivot": 8,   # 假设有根本问题 → 回退到 HYPOTHESIS_GEN
    "refine": 13, # 假设没问题但实验需调整 → 回退到 ITERATIVE_REFINE
}

MAX_PIVOTS = 2  # 防止无限循环

# 非关键阶段 — 失败可跳过
NONCRITICAL = {20, 21}


# ============================================================
# 状态管理
# ============================================================

def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _atomic_write(path: Path, data: dict) -> None:
    """原子写入 JSON（tmp + rename），防止 checkpoint 损坏。

    参考: AutoResearchClaw/runner.py _write_checkpoint()
    """
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp", prefix=path.stem + "_")
    os.close(fd)
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        Path(tmp).replace(path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def _append_history(run_dir: Path, entry: dict) -> None:
    """追加一条记录到 stage_history.jsonl"""
    history_path = run_dir / "stage_history.jsonl"
    with open(history_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_checkpoint(run_dir: Path) -> dict | None:
    """读取 checkpoint.json"""
    cp = run_dir / "checkpoint.json"
    if not cp.exists():
        return None
    try:
        return json.loads(cp.read_text("utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def read_state(run_dir: Path) -> dict:
    """读取 pipeline_state.json（包含 gate 状态、决策历史等）"""
    sp = run_dir / "pipeline_state.json"
    if not sp.exists():
        return {
            "run_id": run_dir.name,
            "status": "initialized",
            "current_stage": 1,
            "pivot_count": 0,
            "gates": {},       # {stage_num: "pending"|"approved"|"rejected"}
            "decisions": [],   # [{decision, timestamp, rollback_to}]
            "created": _utcnow(),
            "updated": _utcnow(),
        }
    try:
        return json.loads(sp.read_text("utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"status": "corrupted"}


def save_state(run_dir: Path, state: dict) -> None:
    state["updated"] = _utcnow()
    _atomic_write(run_dir / "pipeline_state.json", state)


# ============================================================
# 命令实现
# ============================================================

def cmd_init(run_dir: Path, run_id: str = "") -> dict:
    """初始化一个新的 pipeline 运行"""
    run_dir.mkdir(parents=True, exist_ok=True)

    rid = run_id or run_dir.name
    state = {
        "run_id": rid,
        "status": "running",
        "current_stage": 1,
        "pivot_count": 0,
        "gates": {},
        "decisions": [],
        "created": _utcnow(),
        "updated": _utcnow(),
    }
    save_state(run_dir, state)

    _append_history(run_dir, {
        "event": "init",
        "run_id": rid,
        "timestamp": _utcnow(),
    })

    return {"action": "init", "run_id": rid, "status": "ok", "next_stage": 1}


def cmd_status(run_dir: Path) -> dict:
    """查询当前状态 — Agent 每个 Stage 开始前调用"""
    state = read_state(run_dir)
    cp = read_checkpoint(run_dir)

    current = state.get("current_stage", 1)
    status = state.get("status", "unknown")

    # 如果有 checkpoint，用 checkpoint 推算下一个 stage
    if cp:
        last_done = cp.get("last_completed_stage", 0)
        if last_done >= 23:
            current = 23
            status = "completed"
        else:
            current = last_done + 1

    # 检查是否在 Gate 等待中
    gate_status = None
    if current in GATE_STAGES:
        gate_status = state.get("gates", {}).get(str(current), "pending")

    # 当前 Phase
    current_phase = "unknown"
    for phase, stages in PHASE_MAP.items():
        if current in stages:
            current_phase = phase
            break

    return {
        "action": "status",
        "run_id": state.get("run_id", "unknown"),
        "status": status,
        "current_stage": current,
        "current_stage_name": STAGE_NAMES.get(current, "unknown"),
        "current_phase": current_phase,
        "is_gate": current in GATE_STAGES,
        "gate_status": gate_status,
        "pivot_count": state.get("pivot_count", 0),
        "max_pivots": MAX_PIVOTS,
        "checkpoint": cp,
    }


def cmd_complete(run_dir: Path, stage: int) -> dict:
    """标记 Stage 完成，写入 checkpoint"""
    state = read_state(run_dir)

    # 如果是 Gate 阶段，检查是否已 approved
    if stage in GATE_STAGES:
        gate_st = state.get("gates", {}).get(str(stage))
        if gate_st not in ("approved", None):
            # Gate 阶段完成后需要等待审批
            state.setdefault("gates", {})[str(stage)] = "pending"
            save_state(run_dir, state)
            return {
                "action": "complete",
                "stage": stage,
                "status": "blocked",
                "message": f"Stage {stage} ({STAGE_NAMES[stage]}) is a GATE stage. "
                           f"Run: gate --stage {stage} --action approve/reject",
            }

    # 写 checkpoint
    checkpoint = {
        "last_completed_stage": stage,
        "last_completed_name": STAGE_NAMES.get(stage, "unknown"),
        "run_id": state.get("run_id", ""),
        "timestamp": _utcnow(),
    }
    _atomic_write(run_dir / "checkpoint.json", checkpoint)

    # 更新 state
    next_stage = stage + 1 if stage < 23 else None
    state["current_stage"] = next_stage or 23
    if stage >= 23:
        state["status"] = "completed"
    save_state(run_dir, state)

    # 记录历史
    _append_history(run_dir, {
        "event": "stage_complete",
        "stage": stage,
        "stage_name": STAGE_NAMES.get(stage),
        "timestamp": _utcnow(),
    })

    result = {
        "action": "complete",
        "stage": stage,
        "stage_name": STAGE_NAMES.get(stage),
        "status": "done",
    }
    if next_stage:
        result["next_stage"] = next_stage
        result["next_stage_name"] = STAGE_NAMES.get(next_stage)
        result["next_is_gate"] = next_stage in GATE_STAGES
    else:
        result["message"] = "Pipeline completed!"

    return result


def cmd_fail(run_dir: Path, stage: int, error: str = "") -> dict:
    """标记 Stage 失败"""
    state = read_state(run_dir)

    is_critical = stage not in NONCRITICAL
    action = "abort" if is_critical else "skip"

    _append_history(run_dir, {
        "event": "stage_fail",
        "stage": stage,
        "stage_name": STAGE_NAMES.get(stage),
        "error": error,
        "critical": is_critical,
        "timestamp": _utcnow(),
    })

    if is_critical:
        state["status"] = "failed"
        save_state(run_dir, state)
        return {
            "action": "fail",
            "stage": stage,
            "status": "failed",
            "critical": True,
            "message": f"Stage {stage} ({STAGE_NAMES.get(stage)}) FAILED: {error}. "
                       "Pipeline aborted. Fix the issue and resume.",
        }
    else:
        # 非关键阶段 — 跳过继续
        return cmd_complete(run_dir, stage)


def cmd_gate(run_dir: Path, stage: int, action: str) -> dict:
    """Gate 审批: approve 或 reject"""
    if stage not in GATE_STAGES:
        return {"action": "gate", "error": f"Stage {stage} is not a gate stage"}

    state = read_state(run_dir)

    if action == "approve":
        state.setdefault("gates", {})[str(stage)] = "approved"
        save_state(run_dir, state)

        _append_history(run_dir, {
            "event": "gate_approved",
            "stage": stage,
            "timestamp": _utcnow(),
        })

        # 自动完成 gate stage，推进到下一个
        return cmd_complete(run_dir, stage)

    elif action == "reject":
        rollback_to = GATE_ROLLBACK.get(stage, stage - 1)
        state.setdefault("gates", {})[str(stage)] = "rejected"
        state["current_stage"] = rollback_to
        save_state(run_dir, state)

        _append_history(run_dir, {
            "event": "gate_rejected",
            "stage": stage,
            "rollback_to": rollback_to,
            "timestamp": _utcnow(),
        })

        return {
            "action": "gate",
            "stage": stage,
            "status": "rejected",
            "rollback_to": rollback_to,
            "rollback_to_name": STAGE_NAMES.get(rollback_to),
            "message": f"Gate {stage} rejected. Rolling back to Stage {rollback_to} "
                       f"({STAGE_NAMES.get(rollback_to)})",
        }

    return {"action": "gate", "error": f"Unknown gate action: {action}"}


def cmd_decide(run_dir: Path, decision: str) -> dict:
    """S15 RESEARCH_DECISION 决策: proceed / pivot / refine"""
    state = read_state(run_dir)

    if decision == "proceed":
        _append_history(run_dir, {
            "event": "decision",
            "decision": "proceed",
            "timestamp": _utcnow(),
        })
        return cmd_complete(run_dir, 15)

    if decision not in DECISION_ROLLBACK:
        return {"action": "decide", "error": f"Unknown decision: {decision}"}

    pivot_count = state.get("pivot_count", 0)
    if pivot_count >= MAX_PIVOTS:
        _append_history(run_dir, {
            "event": "decision",
            "decision": decision,
            "forced_proceed": True,
            "reason": f"Max pivots ({MAX_PIVOTS}) reached",
            "timestamp": _utcnow(),
        })
        return {
            "action": "decide",
            "decision": decision,
            "status": "forced_proceed",
            "message": f"Max pivots ({MAX_PIVOTS}) reached. Forcing PROCEED.",
        }

    rollback_to = DECISION_ROLLBACK[decision]
    state["pivot_count"] = pivot_count + 1
    state["current_stage"] = rollback_to
    state.setdefault("decisions", []).append({
        "decision": decision,
        "rollback_to": rollback_to,
        "pivot_number": pivot_count + 1,
        "timestamp": _utcnow(),
    })
    save_state(run_dir, state)

    _append_history(run_dir, {
        "event": "decision",
        "decision": decision,
        "rollback_to": rollback_to,
        "pivot_number": pivot_count + 1,
        "timestamp": _utcnow(),
    })

    return {
        "action": "decide",
        "decision": decision,
        "status": "rollback",
        "rollback_to": rollback_to,
        "rollback_to_name": STAGE_NAMES.get(rollback_to),
        "pivot_number": pivot_count + 1,
        "max_pivots": MAX_PIVOTS,
        "message": f"{decision.upper()}: Rolling back to Stage {rollback_to} "
                   f"({STAGE_NAMES.get(rollback_to)}). "
                   f"Attempt {pivot_count + 1}/{MAX_PIVOTS}.",
    }


def cmd_history(run_dir: Path) -> dict:
    """查看完整历史"""
    history_path = run_dir / "stage_history.jsonl"
    entries = []
    if history_path.exists():
        for line in history_path.read_text("utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return {
        "action": "history",
        "entries": entries,
        "count": len(entries),
    }


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="auto-research pipeline 状态机",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # init
    p = sub.add_parser("init", help="初始化运行")
    p.add_argument("--run-dir", required=True, type=Path)
    p.add_argument("--run-id", default="")

    # status
    p = sub.add_parser("status", help="查询当前状态")
    p.add_argument("--run-dir", required=True, type=Path)

    # complete
    p = sub.add_parser("complete", help="标记 Stage 完成")
    p.add_argument("--run-dir", required=True, type=Path)
    p.add_argument("--stage", required=True, type=int)

    # fail
    p = sub.add_parser("fail", help="标记 Stage 失败")
    p.add_argument("--run-dir", required=True, type=Path)
    p.add_argument("--stage", required=True, type=int)
    p.add_argument("--error", default="")

    # gate
    p = sub.add_parser("gate", help="Gate 审批")
    p.add_argument("--run-dir", required=True, type=Path)
    p.add_argument("--stage", required=True, type=int)
    p.add_argument("--action", required=True, choices=["approve", "reject"])

    # decide
    p = sub.add_parser("decide", help="S15 研究决策")
    p.add_argument("--run-dir", required=True, type=Path)
    p.add_argument("--decision", required=True, choices=["proceed", "pivot", "refine"])

    # history
    p = sub.add_parser("history", help="查看完整历史")
    p.add_argument("--run-dir", required=True, type=Path)

    args = parser.parse_args()

    if args.command == "init":
        result = cmd_init(args.run_dir, args.run_id)
    elif args.command == "status":
        result = cmd_status(args.run_dir)
    elif args.command == "complete":
        result = cmd_complete(args.run_dir, args.stage)
    elif args.command == "fail":
        result = cmd_fail(args.run_dir, args.stage, args.error)
    elif args.command == "gate":
        result = cmd_gate(args.run_dir, args.stage, args.action)
    elif args.command == "decide":
        result = cmd_decide(args.run_dir, args.decision)
    elif args.command == "history":
        result = cmd_history(args.run_dir)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
