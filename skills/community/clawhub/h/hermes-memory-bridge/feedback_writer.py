"""
hermes-memory-bridge / feedback_writer.py
结果回写器 — WorkBuddy 处理完 Hermes 命令后，将结果写入共享目录

工作原理：
1. task_processor.py 执行完命令后，调用 write_feedback() 回写结果
2. 结果以 signal 形式写入 ~/.hermes/shared/feedback/ 目录
3. Hermes 通过 event_signaler.py feedback poll 命令读取结果

用法（作为模块导入）：
  from feedback_writer import write_feedback
  write_feedback(signal_id, command_type, result)
"""

from __future__ import annotations

import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

try:
    from config import SHARED_DIR, _get_logger
except ImportError:
    SHARED_DIR = Path.home() / ".hermes" / "shared"
    import logging
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    _get_logger = lambda n: logging.getLogger(n)

logger = _get_logger("feedback_writer")

# ─── 路径 ──────────────────────────────────────────────────────────
FEEDBACK_DIR = SHARED_DIR / "feedback"  # WorkBuddy 结果 → Hermes 读取


# ─── 工具函数 ──────────────────────────────────────────────────────

def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _safe_write(path: Path, data: Any) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except (PermissionError, OSError) as e:
        logger.error(f"写入失败 {path}: {e}")
        return False


def _ensure_dir() -> bool:
    try:
        FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
        return True
    except PermissionError:
        logger.error(f"权限不足，无法创建目录 {FEEDBACK_DIR}")
        return False


# ─── 核心函数 ──────────────────────────────────────────────────────

def write_feedback(
    signal_id: str,
    command_type: str,
    result: dict,
    source_signal: Optional[dict] = None,
) -> Optional[str]:
    """
    将命令执行结果写入反馈文件。

    Args:
        signal_id:      Hermes 原始信号的 ID（用于关联）
        command_type:   命令类型
        result:         task_processor.process_command() 的返回结果
        source_signal:  原始信号 dict（可选，用于复制元数据）

    Returns:
        feedback_id 或 None（失败时）
    """
    if not _ensure_dir():
        return None

    fid = str(uuid.uuid4())[:12]

    feedback = {
        "id": f"fb_{fid}",
        "ref_signal_id": signal_id,
        "command": command_type,
        "source": "WorkBuddy",
        "target": "Hermes",
        "status": "done" if result.get("success") else "error",
        "result": result,
        "created_at": _ts(),
        "processed_at": result.get("_meta", {}).get("processed_at", _ts()),
        "elapsed_ms": result.get("_meta", {}).get("elapsed_ms", 0),
    }

    # 复制原始信号的摘要信息
    if source_signal:
        feedback["source_summary"] = source_signal.get("data", {}).get(
            "summary", source_signal.get("summary", "")
        )
        feedback["source_type"] = source_signal.get("type", command_type)

    fname = FEEDBACK_DIR / f"fb_{command_type}_{fid}.json"
    if _safe_write(fname, feedback):
        logger.info(f"结果回写成功 [{signal_id[:8]}]: fb_{fid} ({command_type})")
        return f"fb_{fid}"
    return None


def read_feedback(feedback_id: str) -> Optional[dict]:
    """按 feedback_id 读取单条反馈（Hermes 侧用）"""
    try:
        fpath = FEEDBACK_DIR / f"fb_*{feedback_id}*.json"
        matches = list(FEEDBACK_DIR.glob(f"fb_*{feedback_id}*.json"))
        if not matches:
            return None
        return json.loads(matches[0].read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def list_pending_feedback(source: str = "WorkBuddy", limit: int = 20) -> list[dict]:
    """
    列出未读的反馈（供 Hermes 轮询）。

    Args:
        source: 过滤来源，"WorkBuddy" = WorkBuddy 发给 Hermes 的结果
        limit:  返回条数上限

    Returns:
        反馈列表（按时间升序 = 最早的在前）
    """
    if not FEEDBACK_DIR.exists():
        return []

    feedback_list: list[dict] = []
    for fpath in sorted(FEEDBACK_DIR.glob("fb_*.json"), key=lambda f: f.stat().st_mtime):
        try:
            fb = json.loads(fpath.read_text(encoding="utf-8"))
            if fb.get("source") == source:
                feedback_list.append(fb)
                if len(feedback_list) >= limit:
                    break
        except (json.JSONDecodeError, OSError):
            continue

    return feedback_list


def mark_feedback_read(feedback_id: str) -> bool:
    """标记反馈为已读（写入 .read 标记文件，幂等）"""
    try:
        marker = FEEDBACK_DIR / f".read_{feedback_id}"
        marker.write_text(_ts(), encoding="utf-8")
        return True
    except OSError:
        return False


def is_feedback_read(feedback_id: str) -> bool:
    """检查反馈是否已被 Hermes 读取"""
    return (FEEDBACK_DIR / f".read_{feedback_id}").exists()


def cleanup_old_feedback(max_age_hours: int = 24) -> int:
    """
    删除超过 max_age_hours 的反馈文件（默认 24h）。

    Returns:
        删除数量
    """
    if not FEEDBACK_DIR.exists():
        return 0

    import time as time_module
    cutoff = time_module.time() - max_age_hours * 3600
    removed = 0

    for fpath in FEEDBACK_DIR.glob("fb_*.json"):
        if fpath.stat().st_mtime < cutoff:
            try:
                fpath.unlink(missing_ok=True)
                removed += 1
            except OSError:
                pass

    if removed > 0:
        logger.debug(f"清理反馈文件 {removed} 条")

    return removed


# ─── CLI 入口 ──────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="WorkBuddy → Hermes 反馈写入器")
    sub = parser.add_subparsers(dest="cmd", help="子命令")

    p_list = sub.add_parser("list", help="列出待读反馈")
    p_list.add_argument("--limit", type=int, default=20)
    p_list.add_argument("--unread", action="store_true", help="仅显示未读")

    p_write = sub.add_parser("write", help="写入反馈")
    p_write.add_argument("--signal-id", required=True)
    p_write.add_argument("--command", required=True)
    p_write.add_argument("--result", required=True, help="JSON 字符串")
    p_write.add_argument("--ref-summary", default="")

    p_cleanup = sub.add_parser("cleanup", help="清理旧反馈")
    p_cleanup.add_argument("--max-hours", type=int, default=24)

    args = parser.parse_args()

    if args.cmd == "list":
        fbs = list_pending_feedback(limit=args.limit)
        print(f"待读反馈共 {len(fbs)} 条：\n")
        for fb in fbs:
            read_mark = "✅已读" if is_feedback_read(fb["id"]) else "📩未读"
            print(f"[{read_mark}] {fb['id']} | {fb['command']} | {fb['created_at'][:16]} | {fb['result'].get('success', '?')}")
            print(f"  → {json.dumps(fb['result'], ensure_ascii=False)[:200]}")
            print()

    elif args.cmd == "write":
        try:
            result_data = json.loads(args.result)
        except json.JSONDecodeError:
            print(f"JSON 解析失败: {args.result}")
            sys.exit(1)
        source_signal = {"summary": args.ref_summary} if args.ref_summary else None
        fid = write_feedback(args.signal_id, args.command, result_data, source_signal)
        print(f"写入成功: {fid}" if fid else "写入失败")

    elif args.cmd == "cleanup":
        n = cleanup_old_feedback(args.max_hours)
        print(f"清理完成，删除 {n} 条")

    else:
        parser.print_help()
