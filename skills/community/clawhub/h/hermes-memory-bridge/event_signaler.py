#!/usr/bin/env python3
"""
hermes-memory-bridge / event_signaler.py
Hermes 侧信号发射器 — 将 Hermes 的重要操作主动通知 WorkBuddy

v1.3 新增（闭环命令系统）：
- send_task   — 向 WorkBuddy 发送命令任务
- feedback    — 轮询 WorkBuddy 的处理结果
- mark_read   — 标记反馈为已读

用法（从 Hermes Agent 调用）：
  python3 event_signaler.py <command> [args...]

命令：
  emit <type> <summary>         发射通知信号
  send_task <command> [params]  发送一条命令给 WorkBuddy 执行
  feedback [limit] [--unread]     轮询 WorkBuddy 的处理结果
  mark_read <feedback_id>        标记反馈为已读
  ack <signal_id>                确认收到某信号
  stats                          显示信号统计
"""

from __future__ import annotations

import json
import os
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

HERMES_HOME = Path.home() / ".hermes"
SHARED_DIR = HERMES_HOME / "shared"
SIGNAL_DIR = SHARED_DIR / "signals"
QUEUE_DIR = SHARED_DIR / "queue"
FEEDBACK_DIR = SHARED_DIR / "feedback"

# 日志配置
_log_level = os.getenv("BRIDGE_LOG_LEVEL", "INFO").upper()
import logging
logging.basicConfig(
    level=getattr(logging, _log_level, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("event_signaler")


def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _safe_read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


def _safe_write(path: Path, data: Any) -> bool:
    try:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except (PermissionError, OSError) as e:
        logger.error(f"写入失败 {path}: {e}")
        return False


def _ensure_dir(p: Path) -> None:
    try:
        p.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        logger.error(f"权限不足: {p}")


def _write_log(message: str) -> None:
    """写入 Hermes 运行日志"""
    log_path = SHARED_DIR / "hermes.log"
    _ensure_dir(SHARED_DIR)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    try:
        log_path.write_text(
            log_path.read_text(encoding="utf-8") + entry, encoding="utf-8"
        )
        lines = log_path.read_text(encoding="utf-8").strip().split("\n")
        if len(lines) > 500:
            log_path.write_text("\n".join(lines[-500:]) + "\n", encoding="utf-8")
    except OSError:
        pass


# ─── 信号发射 ──────────────────────────────────────────────────────

def emit_signal(signal_type: str, summary: str, data: dict | None = None) -> str | None:
    """
    从 Hermes 发射信号，通知 WorkBuddy。
    """
    _ensure_dir(SIGNAL_DIR)

    sid = str(uuid.uuid4())[:12]
    signal = {
        "id": sid,
        "type": signal_type,
        "source": "Hermes",
        "priority": "normal",
        "summary": summary,
        "data": data or {},
        "created_at": _ts(),
        "status": "pending",
    }

    fname = SIGNAL_DIR / f"sig_{signal_type}_{sid}.json"
    if _safe_write(fname, signal):
        logger.info(f"[Hermes→] 信号发射: {signal_type} ({sid})")
        _write_log(f"[SIGNAL→WorkBuddy] {signal_type}: {summary}")
        return sid
    return None


# ─── 命令任务发送（v1.3 新增）──────────────────────────────────────

def send_task(command: str, params: dict | None = None) -> str | None:
    """
    向 WorkBuddy 发送一条命令任务（带完整参数）。
    WorkBuddy 的 task_processor 会自动解析并执行。

    Args:
        command: 命令类型
                  search_memory | sync_session | create_task |
                  complete_task | list_tasks | ack | echo
        params:  命令参数字典

    Returns:
        信号 ID 或 None
    """
    _ensure_dir(SIGNAL_DIR)

    tid = str(uuid.uuid4())[:12]

    task_signal = {
        "id": tid,
        "type": "task",
        "source": "Hermes",
        "priority": "normal",
        "summary": f"[命令] {command}",
        "data": {
            "command": command,
            "params": params or {},
        },
        "created_at": _ts(),
        "status": "pending",
    }

    fname = SIGNAL_DIR / f"sig_task_{tid}.json"
    if _safe_write(fname, task_signal):
        _write_log(f"[TASK→WorkBuddy] command={command}, id={tid}, params={params}")
        logger.info(f"[Hermes→WorkBuddy] 命令已发送: {command} ({tid})")
        return tid
    return None


# ─── 结果反馈轮询（v1.3 新增）─────────────────────────────────────

def _is_feedback_read(feedback_id: str) -> bool:
    return (FEEDBACK_DIR / f".read_{feedback_id}").exists()


def _mark_feedback_read(feedback_id: str) -> bool:
    try:
        _ensure_dir(FEEDBACK_DIR)
        marker = FEEDBACK_DIR / f".read_{feedback_id}"
        marker.write_text(_ts(), encoding="utf-8")
        return True
    except OSError:
        return False


def poll_feedback(limit: int = 10, mark_read: bool = False) -> list[dict]:
    """
    轮询 WorkBuddy 发来的处理结果反馈。
    """
    if not FEEDBACK_DIR.exists():
        return []

    feedback_list: list[dict] = []
    for fpath in sorted(FEEDBACK_DIR.glob("fb_*.json"), key=lambda f: f.stat().st_mtime):
        fb = _safe_read(fpath)
        if fb is None:
            continue
        if fb.get("source") != "WorkBuddy":
            continue
        feedback_list.append(fb)
        if len(feedback_list) >= limit:
            break

    if mark_read:
        for fb in feedback_list:
            _mark_feedback_read(fb["id"])

    return feedback_list


# ─── 原有功能 ──────────────────────────────────────────────────────

def poll_signals(direction: str = "wb_to_hm", limit: int = 10) -> list[dict]:
    if not SIGNAL_DIR.exists():
        return []
    signals = []
    for fpath in sorted(SIGNAL_DIR.glob("sig_*.json"), key=lambda f: f.stat().st_mtime, reverse=True):
        sig = _safe_read(fpath)
        if sig is None:
            continue
        if sig.get("status") != "pending":
            continue
        if sig.get("source") != "WorkBuddy":
            continue
        signals.append(sig)
        if len(signals) >= limit:
            break
    return signals


def ack_signal(signal_id: str) -> bool:
    if not SIGNAL_DIR.exists():
        return False
    for fpath in SIGNAL_DIR.glob("sig_*.json"):
        sig = _safe_read(fpath)
        if sig is None:
            continue
        if sig.get("id") != signal_id:
            continue
        sig["status"] = "acknowledged"
        sig["acked_by"] = "Hermes"
        sig["acked_at"] = _ts()
        _safe_write(fpath, sig)
        _write_log(f"[ACK] 确认信号 {signal_id}，type={sig.get('type')}")
        logger.info(f"[Hermes] ACK 信号: {signal_id}")
        return True
    logger.warning(f"[Hermes] ACK 找不到信号: {signal_id}")
    return False


def get_signal_stats() -> dict[str, Any]:
    stats = {"total": 0, "pending": 0, "acknowledged": 0, "by_type": {}}
    if not SIGNAL_DIR.exists():
        return stats
    for fpath in SIGNAL_DIR.glob("sig_*.json"):
        sig = _safe_read(fpath)
        if sig is None:
            continue
        stats["total"] += 1
        status = sig.get("status", "unknown")
        if status == "pending":
            stats["pending"] += 1
        elif status == "acknowledged":
            stats["acknowledged"] += 1
        stype = sig.get("type", "unknown")
        stats["by_type"][stype] = stats["by_type"].get(stype, 0) + 1
    return stats


# ─── CLI 入口 ──────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        _print_help()
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "emit":
        if len(sys.argv) < 4:
            print("用法: emit <type> <summary> [json_data]", file=sys.stderr)
            sys.exit(1)
        sig_type = sys.argv[2]
        summary = sys.argv[3]
        data = None
        if len(sys.argv) >= 5:
            try:
                data = json.loads(sys.argv[4])
            except json.JSONDecodeError:
                print(f"❌ JSON 解析失败: {sys.argv[4]}", file=sys.stderr)
                sys.exit(1)
        sid = emit_signal(sig_type, summary, data)
        print(f"✅ 信号已发射: {sid}" if sid else "❌ 发射失败")

    elif cmd == "send_task":
        if len(sys.argv) < 3:
            print("用法: send_task <command> [params_json]", file=sys.stderr)
            sys.exit(1)
        task_cmd = sys.argv[2]
        task_params = None
        if len(sys.argv) >= 4:
            try:
                task_params = json.loads(sys.argv[3])
            except json.JSONDecodeError:
                print(f"❌ JSON 解析失败: {sys.argv[3]}", file=sys.stderr)
                sys.exit(1)
        tid = send_task(task_cmd, task_params)
        print(f"✅ 任务已发送: {task_cmd} → {tid}" if tid else "❌ 发送失败")

    elif cmd == "feedback":
        unread_only = "--unread" in sys.argv
        limit = 10
        for a in sys.argv[2:]:
            if a.isdigit():
                limit = int(a)
                break
        fb_list = poll_feedback(limit=limit, mark_read=not unread_only)
        if not fb_list:
            print("📭 没有待读反馈（WorkBuddy 尚未处理任务）")
        else:
            print(f"📬 WorkBuddy 处理结果 ({len(fb_list)} 条)：")
            for fb in fb_list:
                read_mark = "✅" if _is_feedback_read(fb["id"]) else "📩"
                result_ok = fb.get("result", {}).get("success", False)
                ok_mark = "✅成功" if result_ok else "❌失败"
                print(f"\n  [{read_mark}] {fb['id']} | {fb['command']} | {ok_mark} | {fb['created_at'][:16]}")
                print(f"  → {json.dumps(fb.get('result', {}), ensure_ascii=False)[:300]}")
            if not unread_only:
                print(f"\n（已自动标记 {len(fb_list)} 条为已读）")

    elif cmd == "mark_read":
        if len(sys.argv) < 3:
            print("用法: mark_read <feedback_id>", file=sys.stderr)
            sys.exit(1)
        ok = _mark_feedback_read(sys.argv[2])
        print(f"{'✅' if ok else '❌'} 标记已读 {sys.argv[2]}")

    elif cmd == "poll":
        signals = poll_signals(limit=int(sys.argv[2]) if len(sys.argv) >= 3 and sys.argv[2].isdigit() else 10)
        if not signals:
            print("📭 没有待处理信号")
        else:
            print(f"📬 待处理信号 ({len(signals)} 条)：")
            for sig in signals:
                print(f"  [{sig['id']}] {sig['type']} | {sig.get('summary', '')} | {sig.get('created_at', '')[:16]}")

    elif cmd == "ack":
        if len(sys.argv) < 3:
            print("用法: ack <signal_id>", file=sys.stderr)
            sys.exit(1)
        ok = ack_signal(sys.argv[2])
        print(f"{'✅' if ok else '❌'} ACK {sys.argv[2]}")

    elif cmd == "stats":
        stats = get_signal_stats()
        print(f"📊 信号统计")
        print(f"  总数:   {stats['total']}")
        print(f"  待确认: {stats['pending']}")
        print(f"  已确认: {stats['acknowledged']}")
        print(f"  按类型:")
        for t, n in stats.get("by_type", {}).items():
            print(f"    {t}: {n}")
        # 反馈统计
        _ensure_dir(FEEDBACK_DIR)
        fb_count = len(list(FEEDBACK_DIR.glob("fb_*.json"))) if FEEDBACK_DIR.exists() else 0
        print(f"  反馈:   {fb_count} 条")

    else:
        print(f"❌ 未知命令: {cmd}", file=sys.stderr)
        _print_help()
        sys.exit(1)


def _print_help():
    print("""
Hermes Event Signaler (v1.3) — 闭环命令任务系统

  emit     <type> <summary> [json_data]  发射通知信号到 WorkBuddy
  send_task <command> [params_json]      发送一条命令给 WorkBuddy 执行
  feedback [limit] [--unread]            轮询 WorkBuddy 的处理结果
  mark_read <feedback_id>               标记反馈为已读
  poll     [limit]                       轮询来自 WorkBuddy 的待处理信号
  ack      <signal_id>                   确认收到某信号
  stats                                显示信号统计

命令类型（send_task）：
  search_memory  {"keyword": "..."}
  sync_session   {"topic": "...", "summary": "..."}
  create_task    {"title": "..."}
  complete_task  {"task_id": "..."}
  list_tasks     {}
  ack            {"signal_id": "...", "message": "..."}
  echo           {"message": "..."}

示例:
  # 通知 WorkBuddy 某事完成
  python3 event_signaler.py emit task_done "完成项目A的开发"

  # 让 WorkBuddy 执行 echo 测试
  python3 event_signaler.py send_task echo '{"message":"ping"}'

  # 让 WorkBuddy 搜索记忆
  python3 event_signaler.py send_task search_memory '{"keyword":"辽望客户端"}'

  # 轮询 WorkBuddy 的处理结果
  python3 event_signaler.py feedback

  # 轮询（只看未读）
  python3 event_signaler.py feedback 5 --unread
    """)


if __name__ == "__main__":
    main()
