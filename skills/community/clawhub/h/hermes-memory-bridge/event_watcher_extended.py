#!/usr/bin/env python3
"""
hermes-memory-bridge / event_watcher_extended.py
WorkBuddy 侧事件监听器扩展版 — 使用扩展版任务处理器

基于原始event_watcher.py，但使用task_processor_extended.py
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

logger = _get_logger("event_watcher_extended")

# ─── 路径 ──────────────────────────────────────────────────────────
SIGNAL_DIR = SHARED_DIR / "signals"
WATCH_DIR = SHARED_DIR  # 监听整个 shared 目录

# ─── 全局状态 ──────────────────────────────────────────────────────
_dry_run = False
_running = True
_callback: Optional[Callable[[dict], None]] = None


# ─── 工具函数 ──────────────────────────────────────────────────────

def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _safe_read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


def _poll_new_signals(source_filter: Optional[str] = None) -> list[dict]:
    """轮询新信号（状态为 pending）"""
    if not SIGNAL_DIR.exists():
        return []

    signals = []
    for fpath in SIGNAL_DIR.glob("sig_*.json"):
        sig = _safe_read(fpath)
        if sig is None:
            continue
        if sig.get("status") != "pending":
            continue
        if source_filter and sig.get("source") != source_filter:
            continue
        signals.append(sig)

    # 按创建时间排序（旧→新）
    signals.sort(key=lambda s: s.get("created_at", ""))
    return signals


# ─── 信号处理核心 ──────────────────────────────────────────────────

def _process_signal(sig: dict) -> None:
    """处理单个信号"""
    signal_id = sig.get("id", "")
    sig_type = sig.get("type", "")
    source = sig.get("source", "")

    logger.info(f"[处理] 信号 {signal_id[:12]} ({sig_type}): {sig.get('summary', '')[:60]}")

    # 只处理 task 类型的 Hermes 信号
    if sig_type != "task" or source != "Hermes":
        return

    # 提取命令和参数
    data = sig.get("data", {})
    command_type = data.get("command", "")
    params = data.get("params", {})

    if not command_type:
        logger.warning(f"信号 {signal_id} 缺少 command 字段")
        return

    # 1. 执行命令（使用扩展版任务处理器）
    try:
        import importlib
        task_processor = importlib.import_module("task_processor_extended")
        result = task_processor.process_command(command_type, params, signal_id)
    except Exception as e:
        logger.error(f"task_processor_extended 执行失败: {e}")
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
            _process_signal(sig)
        except Exception as e:
            logger.error(f"处理信号 {sig.get('id', '?')} 失败: {e}")

    return len(signals)


# ─── 自适应轮询器（FSEvents 不可用时的降级方案）────────────────────

class AdaptivePoller:
    """自适应轮询器，根据信号频率动态调整轮询间隔"""

    def __init__(self, base_interval: float = 60.0):
        self.base_interval = base_interval
        self.current_interval = base_interval
        self.min_interval = 5.0
        self.max_interval = 300.0
        self.last_signal_count = 0
        self.last_poll_time = time.time()

    def poll(self) -> int:
        """执行一次轮询，返回处理的信号数量"""
        processed = process_hermes_signals()
        now = time.time()

        # 自适应调整间隔
        if processed > 0:
            # 有信号，加快轮询
            self.current_interval = max(self.min_interval, self.current_interval * 0.7)
        else:
            # 无信号，减慢轮询（但不超过最大值）
            self.current_interval = min(self.max_interval, self.current_interval * 1.1)

        self.last_signal_count = processed
        self.last_poll_time = now
        return processed

    def get_next_interval(self) -> float:
        """获取下一次轮询的间隔（秒）"""
        return self.current_interval


# ─── 主监听循环 ────────────────────────────────────────────────────

def watch(poll_only: bool = False, once: bool = False, dry_run: bool = False) -> None:
    """
    启动事件监听。

    Args:
        poll_only: 强制使用轮询模式（即使 FSEvents 可用）
        once:      单次处理现有信号后退出
        dry_run:   处理但不回写结果（测试用）
    """
    global _running, _dry_run
    _dry_run = dry_run

    logger.info("启动 WorkBuddy 事件监听（扩展版，含天气查询）...")

    # 检查 FSEvents 可用性
    fsevents_available = False
    if not poll_only:
        try:
            import fsevents
            fsevents_available = True
            logger.info("✅ FSEvents 可用，使用文件系统事件监听")
        except ImportError:
            logger.warning("⚠️ FSEvents 不可用，使用自适应轮询模式")

    if fsevents_available and not poll_only:
        # FSEvents 模式
        try:
            import fsevents
            from fsevents import Stream
            
            def fsevents_callback(event):
                if event.name.endswith(".json") and "signals" in event.name:
                    process_hermes_signals(dry_run)
            
            stream = Stream(fsevents_callback, str(WATCH_DIR), file_events=True)
            stream.start()
            
            logger.info("FSEvents 监听已启动")
            
            # 等待退出信号
            def stop(signum, frame):
                global _running
                _running = False
                stream.stop()
            
            signal.signal(signal.SIGINT, stop)
            signal.signal(signal.SIGTERM, stop)
            
            while _running:
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"FSEvents 启动失败: {e}")
            fsevents_available = False

    if not fsevents_available or poll_only:
        # 自适应轮询模式
        poller = AdaptivePoller(base_interval=30.0)  # 初始间隔30秒
        
        def stop(signum, frame):
            global _running
            _running = False
        
        signal.signal(signal.SIGINT, stop)
        signal.signal(signal.SIGTERM, stop)
        
        logger.info(f"自适应轮询已启动（初始间隔 {poller.base_interval:.1f}s）")
        
        if once:
            # 单次模式
            processed = poller.poll()
            logger.info(f"单次处理完成，处理了 {processed} 个信号")
            return
        
        # 持续轮询
        while _running:
            processed = poller.poll()
            if processed > 0:
                logger.info(f"[Poller] 批处理 {processed} 条 Hermes 信号")
            
            # 等待下一次轮询
            interval = poller.get_next_interval()
            for _ in range(int(interval)):
                if not _running:
                    break
                time.sleep(1)


# ─── CLI 入口 ──────────────────────────────────────────────────────

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="WorkBuddy 事件监听器（扩展版）",
        epilog="示例：\n"
               "  python3 event_watcher_extended.py              # 持续监听\n"
               "  python3 event_watcher_extended.py --poll-only  # 强制轮询模式\n"
               "  python3 event_watcher_extended.py --once        # 单次处理现有信号\n"
               "  python3 event_watcher_extended.py --dry-run    # 处理但不回写（测试）"
    )
    
    parser.add_argument("--poll-only", action="store_true",
                       help="强制使用轮询模式（即使 FSEvents 可用）")
    parser.add_argument("--once", action="store_true",
                       help="单次处理现有信号后退出")
    parser.add_argument("--dry-run", action="store_true",
                       help="处理但不回写结果（测试用）")
    
    args = parser.parse_args()
    
    watch(
        poll_only=args.poll_only,
        once=args.once,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()