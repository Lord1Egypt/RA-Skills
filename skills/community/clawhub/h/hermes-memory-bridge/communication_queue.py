"""
hermes-memory-bridge / communication_queue.py
事件驱动队列 v1.2 — 支持信号事件与 ACK 确认机制

新增 v1.2：
- signal_event / signal_ack / wait_for_ack / list_pending_signals
- 支持 Hermes ↔ WorkBuddy 之间的实时信号通知
"""

from __future__ import annotations

import json
import logging
import os
import threading
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

from config import SHARED_DIR, _get_logger

logger = _get_logger("communication_queue")

# ─── 路径 ──────────────────────────────────────────────────────────
QUEUE_DIR = SHARED_DIR / "queue"
SIGNAL_DIR = SHARED_DIR / "signals"

# ─── ACK 超时（秒）─────────────────────────────────────────────────
ACK_TIMEOUT_SEC = 300  # 5 分钟超时
CLEANUP_INTERVAL_SEC = 60  # 清理线程运行间隔
MAX_QUEUE_AGE_DAYS = 7  # 超过 7 天的队列文件删除
MAX_SIGNAL_AGE_HOURS = 6  # 信号文件保留 6 小时


# ─── 初始化 ────────────────────────────────────────────────────────
def _ensure_dirs() -> bool:
    for d in [QUEUE_DIR, SIGNAL_DIR]:
        try:
            d.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            logger.error(f"权限不足，无法创建目录 {d}")
            return False
    return True


# ─── 工具函数 ──────────────────────────────────────────────────────

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


def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _queue_fname(prefix: str, qid: str) -> Path:
    return QUEUE_DIR / f"{prefix}_{qid}.json"


# ─── 原有队列功能 ──────────────────────────────────────────────────

def enqueue(direction: str, payload: dict) -> str | None:
    """
    将消息放入队列。

    Args:
        direction: 'wb_to_hm' | 'hm_to_wb'
        payload:  任意 JSON 可序列化数据

    Returns:
        队列 ID，或 None（失败时）
    """
    if not _ensure_dirs():
        return None

    qid = str(uuid.uuid4())[:8]
    item = {
        "id": qid,
        "direction": direction,
        "payload": payload,
        "created_at": _ts(),
        "status": "pending",
    }

    prefix = "wb2hm" if direction == "wb_to_hm" else "hm2wb"
    fpath = _queue_fname(prefix, qid)

    if _safe_write(fpath, item):
        logger.debug(f"入队 [{direction}]: {qid}")
        return qid
    return None


def dequeue(direction: str) -> dict | None:
    """
    按 FIFO 顺序取出一条待处理消息，并标记为 processing。

    Returns:
        消息 dict 或 None（队列为空）
    """
    if not QUEUE_DIR.exists():
        return None

    prefix = "wb2hm" if direction == "wb_to_hm" else "hm2wb"
    try:
        files = sorted(QUEUE_DIR.glob(f"{prefix}_*.json"), key=lambda f: f.name)
    except PermissionError:
        return None

    for fpath in files:
        item = _safe_read(fpath)
        if item is None:
            continue
        if item.get("status") != "pending":
            continue

        item["status"] = "processing"
        item["processed_at"] = _ts()
        _safe_write(fpath, item)
        logger.debug(f"出队 [{direction}]: {item['id']}")
        return item

    return None


def ack(queue_id: str, direction: str) -> bool:
    """
    确认一条消息处理完成（幂等操作）。

    Args:
        queue_id: 消息 ID
        direction: 'wb_to_hm' | 'hm_to_wb'

    Returns:
        是否成功确认
    """
    prefix = "wb2hm" if direction == "wb_to_hm" else "hm2wb"
    fpath = _queue_fname(prefix, queue_id)
    item = _safe_read(fpath)
    if item is None:
        logger.warning(f"ACK 找不到消息: {queue_id}")
        return False

    item["status"] = "done"
    item["acked_at"] = _ts()
    _safe_write(fpath, item)
    logger.debug(f"ACK [{direction}]: {queue_id}")
    return True


def get_queue_stats() -> dict[str, Any]:
    """返回队列统计信息"""
    stats: dict[str, Any] = {"pending": 0, "processing": 0, "done": 0, "total": 0}
    if not QUEUE_DIR.exists():
        return stats

    for fpath in QUEUE_DIR.glob("*.json"):
        item = _safe_read(fpath)
        if item is None:
            continue
        status = item.get("status", "unknown")
        if status in stats:
            stats[status] += 1
        stats["total"] += 1

    return stats


# ─── v1.2 新增：信号事件 ───────────────────────────────────────────

def signal_event(
    signal_type: str,
    data: dict,
    source: str = "unknown",
    priority: str = "normal",
) -> str | None:
    """
    发射一个信号事件（跨 Agent 通知）。

    与普通队列消息不同，信号是"立即可感知"的事件，
    配合 event_watcher.py 的 FSEvents 监听可实现近实时通知。

    Args:
        signal_type: 'task_done' | 'sync' | 'config_change' | 'ack' | 自定义
        data: 事件数据
        source: 'WorkBuddy' | 'Hermes'
        priority: 'low' | 'normal' | 'high'

    Returns:
        信号 ID 或 None
    """
    if not _ensure_dirs():
        return None

    sid = str(uuid.uuid4())[:12]
    signal = {
        "id": sid,
        "type": signal_type,
        "source": source,
        "priority": priority,
        "data": data,
        "created_at": _ts(),
        "status": "pending",
        "ack_id": None,
    }

    fname = SIGNAL_DIR / f"sig_{signal_type}_{sid}.json"
    if _safe_write(fname, signal):
        logger.info(f"信号发射 [{source}→{signal_type}]: {sid}")
        return sid
    return None


def signal_ack(signal_id: str, from_source: str) -> bool:
    """
    确认收到某信号。

    用于接收方告知发送方"已处理"。
    实际上是在对应信号文件中写入 ack 记录。

    Args:
        signal_id: 信号 ID（不含前缀）
        from_source: 'WorkBuddy' | 'Hermes'
    """
    if not SIGNAL_DIR.exists():
        return False

    for fpath in SIGNAL_DIR.glob("sig_*.json"):
        sig = _safe_read(fpath)
        if sig is None:
            continue
        # 通过文件名中的 id 部分匹配
        if sig.get("id") != signal_id:
            continue

        sig["status"] = "acknowledged"
        sig["acked_by"] = from_source
        sig["acked_at"] = _ts()
        _safe_write(fpath, sig)
        logger.debug(f"信号 ACK [{from_source}]: {signal_id}")
        return True

    logger.warning(f"signal_ack 找不到信号: {signal_id}")
    return False


def wait_for_ack(
    signal_id: str,
    timeout_sec: float = ACK_TIMEOUT_SEC,
    poll_interval: float = 1.0,
) -> dict | None:
    """
    等待某个信号被对方 ACK（阻塞轮询）。

    适用于 WorkBuddy 主动发射信号后，等待 Hermes 处理完成的场景。

    Args:
        signal_id: 信号 ID
        timeout_sec: 超时秒数
        poll_interval: 轮询间隔（秒）

    Returns:
        信号 dict（已确认）或 None（超时）
    """
    deadline = time.time() + timeout_sec

    while time.time() < deadline:
        if not SIGNAL_DIR.exists():
            time.sleep(poll_interval)
            continue

        for fpath in SIGNAL_DIR.glob("sig_*.json"):
            sig = _safe_read(fpath)
            if sig is None:
                continue
            if sig.get("id") != signal_id:
                continue

            if sig.get("status") == "acknowledged":
                logger.debug(f"收到信号 ACK: {signal_id}")
                return sig
            # pending 或其他状态，继续等待
            break

        time.sleep(poll_interval)

    logger.warning(f"等待信号 ACK 超时: {signal_id}")
    return None


def list_pending_signals(
    signal_type: str | None = None,
    source: str | None = None,
    limit: int = 20,
) -> list[dict]:
    """
    列出待确认的信号。

    Args:
        signal_type: 过滤类型，None 表示全部
        source: 过滤来源，None 表示全部
        limit: 返回条数上限

    Returns:
        信号列表（按时间倒序）
    """
    if not SIGNAL_DIR.exists():
        return []

    signals: list[dict] = []
    for fpath in sorted(SIGNAL_DIR.glob("sig_*.json"), key=lambda f: f.stat().st_mtime, reverse=True):
        sig = _safe_read(fpath)
        if sig is None:
            continue
        if sig.get("status") == "done":
            continue  # 已归档，跳过
        if signal_type and sig.get("type") != signal_type:
            continue
        if source and sig.get("source") != source:
            continue
        signals.append(sig)
        if len(signals) >= limit:
            break

    return signals


# ─── 清理线程 ──────────────────────────────────────────────────────

_cleanup_lock = threading.Lock()
_cleanup_running = False


def start_cleanup_thread() -> None:
    """启动后台清理线程（幂等调用）"""
    global _cleanup_running
    with _cleanup_lock:
        if _cleanup_running:
            return
        _cleanup_running = True

    def run():
        while True:
            time.sleep(CLEANUP_INTERVAL_SEC)
            try:
                cleanup_stale_files()
            except Exception as e:
                logger.error(f"清理线程异常: {e}")

    t = threading.Thread(target=run, daemon=True, name="queue-cleanup")
    t.start()
    logger.info("队列清理线程已启动")


def cleanup_stale_files() -> int:
    """
    删除过期的队列和信号文件。

    Returns:
        删除的文件数量
    """
    removed = 0
    now = datetime.now()

    for d in [QUEUE_DIR, SIGNAL_DIR]:
        if not d.exists():
            continue
        for fpath in d.glob("*.json"):
            try:
                mtime = datetime.fromtimestamp(fpath.stat().st_mtime)
                if d == QUEUE_DIR:
                    age_days = (now - mtime).days
                    if age_days > MAX_QUEUE_AGE_DAYS:
                        fpath.unlink(missing_ok=True)
                        removed += 1
                else:  # SIGNAL_DIR
                    age_hours = (now - mtime).total_seconds() / 3600
                    sig = _safe_read(fpath)
                    # 删除超过 6 小时或已完成的信号
                    if age_hours > MAX_SIGNAL_AGE_HOURS or (
                        sig and sig.get("status") in ("acknowledged", "done")
                    ):
                        fpath.unlink(missing_ok=True)
                        removed += 1
            except OSError:
                pass

    if removed > 0:
        logger.debug(f"清理完成，删除 {removed} 个过期文件")
    return removed
