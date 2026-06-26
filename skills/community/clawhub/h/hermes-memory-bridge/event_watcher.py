#!/usr/bin/env python3
"""
hermes-memory-bridge / event_watcher.py
WorkBuddy 侧事件监听器 — FSEvents + 自适应轮询双模式

v2.0 新增：
- 内置任务处理器（task_processor）集成
- 收到 Hermes 命令后自动处理并回写结果（feedback_writer）
- CLI 参数：--dry-run（仅处理，不回写）、--once（单次轮询）

用法（独立运行）：
  python3 event_watcher.py              # 持续监听
  python3 event_watcher.py --poll-only  # 强制轮询模式
  python3 event_watcher.py --once        # 单次处理现有信号后退出
  python3 event_watcher.py --dry-run    # 处理但不回写（测试用）

用法（作为模块导入）：
  from event_watcher import watch, set_callback, process_hermes_signals
  watch()
"""

from __future__ import annotations

import json
import os
import signal
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

try:
    from config import SHARED_DIR, _get_logger
except ImportError:
    SHARED_DIR = Path.home() / ".hermes" / "shared"
    import logging
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    _get_logger = lambda n: logging.getLogger(n)

logger = _get_logger("event_watcher")

# ─── 路径 ──────────────────────────────────────────────────────────
SIGNAL_DIR = SHARED_DIR / "signals"
WATCH_DIR = SHARED_DIR  # 监听整个 shared 目录

# ─── 配置 ──────────────────────────────────────────────────────────
POLL_FALLBACK_INTERVAL_SEC = 5.0
LAST_SEEN_FILE = SIGNAL_DIR / ".last_seen_signals"
PROCESSED_FILE = SIGNAL_DIR / ".processed_signals"


# ─── 回调机制（v1 兼容）────────────────────────────────────────────

_callback: Optional[Callable[[str, dict], None]] = None
_callback_lock = threading.Lock()


def set_callback(cb: Callable[[str, dict], None]) -> None:
    global _callback
    with _callback_lock:
        _callback = cb


def _dispatch(event_type: str, data: dict) -> None:
    with _callback_lock:
        cb = _callback
    if cb is None:
        logger.debug(f"无回调，分发跳过: {event_type}")
        return
    try:
        cb(event_type, data)
        logger.info(f"事件已分发: {event_type}")
    except Exception as e:
        logger.error(f"回调执行异常: {e}")


# ─── 工具函数 ──────────────────────────────────────────────────────

def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _safe_read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


def _read_processed() -> set[str]:
    data = _safe_read(PROCESSED_FILE, {"processed": []})
    return set(data.get("processed", []))


def _write_processed(processed: set[str]) -> None:
    SIGNAL_DIR.mkdir(parents=True, exist_ok=True)
    try:
        items = list(processed)[-200:]
        PROCESSED_FILE.write_text(
            json.dumps({"processed": items, "updated_at": _ts()}, ensure_ascii=False),
            encoding="utf-8",
        )
    except OSError:
        pass


def _poll_new_signals(source_filter: str = "Hermes") -> list[dict]:
    if not SIGNAL_DIR.exists():
        return []

    processed = _read_processed()
    new_signals = []

    for fpath in sorted(SIGNAL_DIR.glob("sig_*.json"), key=lambda f: f.stat().st_mtime):
        sig = _safe_read(fpath)
        if sig is None:
            continue
        sid = sig.get("id", "")
        if sid in processed:
            continue
        if sig.get("source") != source_filter:
            continue
        new_signals.append(sig)
        processed.add(sid)

    if new_signals:
        _write_processed(processed)

    return new_signals


# ─── v2.0 新增：任务处理集成 ──────────────────────────────────────

_dry_run = False


def set_dry_run(val: bool = True) -> None:
    global _dry_run
    _dry_run = val


def _process_single_signal(sig: dict) -> None:
    """
    处理单条 Hermes 信号：
    1. 提取命令类型和参数
    2. 调用 task_processor 执行
    3. 调用 feedback_writer 回写结果
    4. 对原始信号发 ACK
    """
    import importlib

    signal_id = sig.get("id", "")
    signal_type = sig.get("type", "")
    signal_data = sig.get("data", {})

    logger.info(
        f"[处理] 信号 {signal_id[:12]} ({signal_type}): "
        f"{signal_data.get('summary', signal_data.get('message', ''))[:60]}"
    )

    # 提取命令类型（优先从 data.command 获取，其次从 type 推断）
    command_type = signal_data.get("command", "")
    if not command_type:
        type_to_command = {
            "task_done": "echo",
            "sync": "sync_session",
            "config_change": "ack",
            "ack": "ack",
            "feedback": "ack",
        }
        command_type = type_to_command.get(signal_type, signal_type)

    # 提取参数
    params = signal_data.get("params", signal_data)

    # 1. 执行命令
    try:
        task_processor = importlib.import_module("task_processor")
        result = task_processor.process_command(command_type, params, signal_id)
    except Exception as e:
        logger.error(f"task_processor 执行失败: {e}")
        result = {"success": False, "error": str(e)}

    # 2. 回写结果（dry_run 模式下跳过）
    if not _dry_run:
        try:
            feedback_writer = importlib.import_module("feedback_writer")
            feedback_id = feedback_writer.write_feedback(
                signal_id, command_type, result, source_signal=sig
            )
            if feedback_id:
                logger.info(f"[回写] 反馈 {feedback_id} 已写入 feedback 目录")
        except Exception as e:
            logger.error(f"feedback_writer 回写失败: {e}")

    # 3. 对原始信号发 ACK
    if not _dry_run:
        try:
            comm_queue = importlib.import_module("communication_queue")
            comm_queue.signal_ack(signal_id, "WorkBuddy")
            logger.info(f"[ACK] 已确认信号 {signal_id[:12]}")
        except Exception as e:
            logger.error(f"ACK 失败: {e}")


def process_hermes_signals(dry_run: bool = False) -> int:
    """
    处理所有待处理的 Hermes 信号（一次性，不阻塞）。

    Args:
        dry_run: True = 处理但不回写结果（测试用）

    Returns:
        处理的信号数量
    """
    global _dry_run
    _dry_run = dry_run

    signals = _poll_new_signals(source_filter="Hermes")
    if not signals:
        return 0

    for sig in signals:
        try:
            _process_single_signal(sig)
        except Exception as e:
            logger.error(f"处理信号异常: {e}")

    return len(signals)


# ─── FSEvents 模式 ────────────────────────────────────────────────

def _try_fsevents() -> bool:
    try:
        import MacOS.FSEvents as FSEvents  # type: ignore
        return True
    except ImportError:
        return False


class FSEventsWatcher:
    def __init__(self, path: Path, latency: float = 0.5):
        self.path = str(path)
        self.latency = latency
        self._stream_ref: Optional[Any] = None
        self._running = False
        self._watch_thread: Optional[threading.Thread] = None

    def _create_stream(self):
        import MacOS.FSEvents as FSEvents  # type: ignore
        self._stream_ref = FSEvents.EventStream(
            [self.path],
            self.latency,
            FSEvents.kFSEventStreamCreateFlagFileEvents,
        )
        def callback(
            stream_ref, client_callback_info,
            num_events, event_paths, event_flags, event_ids,
        ):
            for i in range(num_events):
                path = event_paths[i]
                flag = event_flags[i]
                if flag & 0x0100:  # kFSEventStreamEventFlagItemCreated
                    self._on_create(Path(path))

        self._stream_ref.start()
        self._running = True
        logger.info(f"FSEvents 监听已启动: {self.path}")

    def _on_create(self, fpath: Path) -> None:
        if fpath.suffix != ".json":
            return
        sig = _safe_read(fpath)
        if sig and sig.get("source") == "Hermes":
            logger.info(f"[FSEvents] 检测到 Hermes 命令: {sig.get('id')} ({sig.get('type')})")
            try:
                _process_single_signal(sig)
            except Exception as e:
                logger.error(f"FSEvents 处理异常: {e}")

    def start(self) -> None:
        if not _try_fsevents():
            logger.warning("FSEvents 不可用，降级为轮询模式")
            return
        try:
            self._create_stream()
        except Exception as e:
            logger.warning(f"FSEvents 启动失败，降级为轮询: {e}")
            return
        self._watch_thread = threading.Thread(target=self._run_loop, daemon=True)
        self._watch_thread.start()

    def _run_loop(self) -> None:
        try:
            while self._running:
                time.sleep(1)
        except Exception:
            pass

    def stop(self) -> None:
        self._running = False
        if self._stream_ref:
            try:
                self._stream_ref.stop()
            except Exception:
                pass
        logger.info("FSEvents 监听已停止")


# ─── 自适应轮询模式 ────────────────────────────────────────────────

class AdaptivePoller:
    def __init__(self):
        self._interval = 60.0
        self._min_interval = 60.0
        self._max_interval = 300.0
        self._decay_factor = 1.15
        self._growth_factor = 0.7
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True, name="adaptive-poller")
        self._thread.start()
        logger.info(f"自适应轮询已启动（初始间隔 {self._interval}s）")

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("自适应轮询已停止")

    def _run(self) -> None:
        while self._running:
            try:
                processed = process_hermes_signals(dry_run=False)
                if processed > 0:
                    logger.info(f"[Poller] 批处理 {processed} 条 Hermes 信号")
                    self._interval = max(
                        self._min_interval,
                        self._interval * self._growth_factor,
                    )
                else:
                    self._interval = min(
                        self._max_interval,
                        self._interval * self._decay_factor,
                    )
            except Exception as e:
                logger.error(f"轮询异常: {e}")
                self._interval = self._min_interval

            time.sleep(self._interval)


# ─── 统一入口 ──────────────────────────────────────────────────────

_watcher: Optional[FSEventsWatcher] = None
_poller: Optional[AdaptivePoller] = None


# ─── Hermes 协调任务监控器 ────────────────────────────────────────
# 检测 Hermes 发来的协调任务，主动通知用户确认后再执行

COORD_DIR = SHARED_DIR / "coordination"
COORD_ALERT_FILE = SIGNAL_DIR / ".coord_alert_state"

_coord_alert_state: dict[str, Any] = {"last_seen_task": None}


def _load_coord_state() -> dict[str, Any]:
    data = _safe_read(COORD_ALERT_FILE, {"last_seen_task": None, "notified_ids": []})
    return data


def _save_coord_state(state: dict) -> None:
    try:
        COORD_ALERT_FILE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass


def _get_pending_coord_tasks() -> list[dict]:
    """找出 Hermes 发来的、未通知过用户的协调任务"""
    if not COORD_DIR.exists():
        return []

    state = _load_coord_state()
    notified = set(state.get("notified_ids", []))
    pending = []

    for fpath in sorted(COORD_DIR.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True):
        try:
            content = fpath.read_text(encoding="utf-8")
            # 提取任务 ID（文件名格式: type_taskid.md）
            fname = fpath.stem
            parts = fname.split("_", 1)
            if len(parts) < 2:
                continue
            task_id = parts[1]

            if task_id in notified:
                continue

            # 解析协调任务元信息（从文件内容提取）
            title = ""
            lines = content.strip().split("\n")
            for line in lines[:10]:
                if line.startswith("# "):
                    title = line[2:].strip()
                    break

            pending.append({
                "id": task_id,
                "title": title or fname,
                "file": str(fpath),
                "preview": content[:200].strip(),
            })
            notified.add(task_id)

        except (OSError, UnicodeDecodeError):
            continue

    if pending:
        state["notified_ids"] = list(notified)
        _save_coord_state(state)

    return pending


def check_hermes_coordination_tasks() -> list[dict]:
    """
    主入口：检查 Hermes 是否有新的协调任务。
    发现新任务后写入 feedback 目录，通知用户确认后再执行。

    Returns:
        新发现的任务列表（每次最多返回 1 条，优先最新）
    """
    tasks = _get_pending_coord_tasks()
    if not tasks:
        return []

    # 只通知最新一条（避免刷屏）
    task = tasks[0]
    alert_msg = (
        f"📋 **Hermes 新协调任务**\n\n"
        f"**任务 ID**: {task['id'][:12]}\n"
        f"**任务标题**: {task['title']}\n\n"
        f"请确认是否执行此任务。回复「确认」开始执行，或「跳过」忽略。\n"
        f"> 查看详情：`cat {task['file']}`"
    )

    # 写入 feedback，让 Hermes 下次轮询时读到并推送给用户
    _write_coord_alert_feedback(task, alert_msg)
    logger.info(f"[HermesAlert] 发现新协调任务: {task['id'][:12]} - {task['title']}")

    return [task]


def _write_coord_alert_feedback(task: dict, message: str) -> None:
    """将协调任务提醒写入 feedback 目录"""
    feedback_dir = SHARED_DIR / "feedback"
    feedback_dir.mkdir(exist_ok=True)

    feedback_id = f"coord_{task['id'][:12]}"
    fb_file = feedback_dir / f"fb_{feedback_id}.json"

    payload = {
        "id": f"fb_{feedback_id}",
        "type": "coordination_alert",
        "source": "WorkBuddy",
        "target": "user",
        "timestamp": _ts(),
        "task_id": task["id"],
        "task_title": task["title"],
        "message": message,
        "status": "awaiting_confirmation",
        "requires_user_action": True,
        "action_options": ["confirm", "skip"],
        "content_preview": task["preview"],
    }

    try:
        fb_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info(f"[HermesAlert] 已写入反馈: fb_{feedback_id}.json")
    except OSError as e:
        logger.error(f"[HermesAlert] 写入反馈失败: {e}")


# ─── 在主轮询循环中集成 ──────────────────────────────────────────

def _process_adaptive_with_alert() -> int:
    """
    轮询 Hermes 信号 + 检查协调任务。
    发现协调任务时主动通知用户（不自动处理）。
    """
    # 1. 检查协调任务（优先）
    try:
        new_tasks = check_hermes_coordination_tasks()
        if new_tasks:
            # 有新协调任务：写入通知，跳过自动处理，等用户确认
            logger.info(f"[HermesAlert] {len(new_tasks)} 条协调任务已通知用户，等待确认")
    except Exception as e:
        logger.error(f"[HermesAlert] 检查协调任务异常: {e}")

    # 2. 处理普通 Hermes 信号
    try:
        processed = process_hermes_signals(dry_run=False)
        return processed
    except Exception as e:
        logger.error(f"处理信号异常: {e}")
        return 0


class AdaptivePollerWithAlert(AdaptivePoller):
    """带协调任务监控的自适应轮询器"""

    def _run(self) -> None:
        while self._running:
            try:
                # 检查协调任务（不触发普通信号处理，保留给下一步）
                processed_signals = _process_adaptive_with_alert()

                if processed_signals > 0:
                    logger.info(f"[Poller] 批处理 {processed_signals} 条 Hermes 信号")
                    self._interval = max(
                        self._min_interval,
                        self._interval * self._growth_factor,
                    )
                else:
                    self._interval = min(
                        self._max_interval,
                        self._interval * self._decay_factor,
                    )
            except Exception as e:
                logger.error(f"轮询异常: {e}")
                self._interval = self._min_interval

            time.sleep(self._interval)


# ─── 覆盖原 watch() 函数的轮询器 ─────────────────────────────────

def watch() -> None:
    global _watcher, _poller

    logger.info("启动 WorkBuddy 事件监听（v2.0 含任务处理 + 主动通知）...")

    if _try_fsevents():
        _watcher = FSEventsWatcher(WATCH_DIR)
        _watcher.start()
        logger.info("✅ 使用 FSEvents 模式")
        # FSEvents 检测到信号后也需要检查协调任务
    else:
        logger.info("⚠️ FSEvents 不可用，使用自适应轮询模式")
        _poller = AdaptivePollerWithAlert()
        _poller.start()

    def signal_handler(signum, frame):
        logger.info("收到退出信号，正在停止...")
        stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        stop()


def stop() -> None:
    if _watcher:
        _watcher.stop()
    if _poller:
        _poller.stop()
    logger.info("事件监听已停止")


# ─── CLI 入口 ──────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="WorkBuddy 事件监听器（含任务处理闭环）"
    )
    parser.add_argument("--poll-only", action="store_true", help="强制轮询模式")
    parser.add_argument("--once", action="store_true", help="单次处理现有信号后退出")
    parser.add_argument("--dry-run", action="store_true", help="处理但不回写结果（测试用）")

    args = parser.parse_args()

    if args.once:
        count = process_hermes_signals(dry_run=args.dry_run)
        print(f"处理了 {count} 条 Hermes 信号（dry_run={args.dry_run}）")
    else:
        if args.poll_only:
            _poller = AdaptivePoller()
            _poller.start()
            print("轮询模式已启动，按 Ctrl+C 退出")
            try:
                while True:
                    time.sleep(3600)
            except KeyboardInterrupt:
                _poller.stop()
                print("已停止")
        else:
            print("启动 WorkBuddy 事件监听（FSEvents + 自适应轮询）...")
            if args.dry_run:
                set_dry_run(True)
                print("⚠️ DRY-RUN 模式：处理但不回写结果")
            watch()
