"""
hermes-memory-bridge / adaptive_poller.py
自适应轮询器 — 根据活跃程度动态调整轮询间隔

策略：
- 启动间隔 60s（检测到活动后缩短）
- 无活动时，每轮乘以 decay_factor (1.15)，最多延长到 max_interval (300s)
- 有活动时，乘以 growth_factor (0.7)，最低不低于 min_interval (60s)
- 出错时强制回到 min_interval
"""

from __future__ import annotations

import json
import logging
import os
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

SKILL_DIR = Path(__file__).parent

try:
    from config import SHARED_DIR, _get_logger
except ImportError:
    SHARED_DIR = Path.home() / ".hermes" / "shared"
    import logging
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    _get_logger = lambda n: logging.getLogger(n)

logger = _get_logger("adaptive_poller")

# ─── 配置 ──────────────────────────────────────────────────────────
MIN_INTERVAL = 60.0     # 最短轮询间隔（秒）
MAX_INTERVAL = 300.0    # 最长轮询间隔（秒）
DECAY_FACTOR = 1.15     # 无活动时乘以这个因子
GROWTH_FACTOR = 0.7    # 有活动时乘以这个因子
SIGNAL_DIR = SHARED_DIR / "signals"
QUEUE_DIR = SHARED_DIR / "queue"


def _safe_read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


def _poll_for_signals() -> list[dict]:
    """轮询新信号（来自 WorkBuddy 的信号）"""
    if not SIGNAL_DIR.exists():
        return []

    signals = []
    try:
        for fpath in sorted(SIGNAL_DIR.glob("sig_*.json"), key=lambda f: f.stat().st_mtime, reverse=True):
            sig = _safe_read(fpath)
            if sig is None:
                continue
            if sig.get("status") != "pending":
                continue
            if sig.get("source") != "WorkBuddy":
                continue
            signals.append(sig)
            if len(signals) >= 5:  # 每次最多处理 5 条
                break
    except PermissionError:
        pass
    return signals


def _poll_for_queue(direction: str = "wb_to_hm") -> list[dict]:
    """轮询新队列消息（来自 WorkBuddy 的队列）"""
    if not QUEUE_DIR.exists():
        return []

    prefix = "wb2hm"
    items = []
    try:
        for fpath in sorted(QUEUE_DIR.glob(f"{prefix}_*.json"), key=lambda f: f.stat().st_mtime):
            item = _safe_read(fpath)
            if item is None:
                continue
            if item.get("status") not in ("pending", "processing"):
                continue
            items.append(item)
            if len(items) >= 5:
                break
    except PermissionError:
        pass
    return items


def _adjust_interval(current: float, has_activity: bool) -> float:
    """根据是否有活动调整间隔"""
    if has_activity:
        new_interval = current * GROWTH_FACTOR
        return max(MIN_INTERVAL, new_interval)
    else:
        new_interval = current * DECAY_FACTOR
        return min(MAX_INTERVAL, new_interval)


class AdaptivePoller:
    """
    自适应轮询器。

    使用示例：
        poller = AdaptivePoller()
        poller.start()

        # 注册回调（每收到一条新信号调用一次）
        poller.on_signal(lambda sig: print(f"收到信号: {sig['type']}"))

        # 停止
        poller.stop()
    """

    def __init__(self):
        self._interval = 60.0
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._callbacks: list[Callable[[dict], None]] = []
        self._lock = threading.Lock()

    def on_signal(self, cb: Callable[[dict], None]) -> "AdaptivePoller":
        """注册信号回调（支持链式调用）"""
        with self._lock:
            self._callbacks.append(cb)
        return self

    def start(self) -> None:
        if self._running:
            logger.warning("轮询器已在运行，忽略重复启动")
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True, name="adaptive-poller")
        self._thread.start()
        logger.info(f"自适应轮询已启动（初始间隔 {self._interval}s）")

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=10)
        logger.info("自适应轮询已停止")

    def _run(self) -> None:
        while self._running:
            try:
                signals = _poll_for_signals()
                if signals:
                    logger.info(f"[Poller] 检测到 {len(signals)} 条新信号")
                    with self._lock:
                        cbs = list(self._callbacks)
                    for sig in signals:
                        for cb in cbs:
                            try:
                                cb(sig)
                            except Exception as e:
                                logger.error(f"回调异常: {e}")
                    self._interval = _adjust_interval(self._interval, has_activity=True)
                else:
                    self._interval = _adjust_interval(self._interval, has_activity=False)

                logger.debug(f"[Poller] 下次轮询间隔: {self._interval:.1f}s")
            except Exception as e:
                logger.error(f"轮询异常: {e}")
                self._interval = MIN_INTERVAL

            time.sleep(self._interval)

    @property
    def current_interval(self) -> float:
        return self._interval


def run_cli() -> None:
    """CLI 模式：直接轮询并打印结果"""
    logger.info("启动自适应轮询器（CLI 模式）...")

    poller = AdaptivePoller()
    poller.on_signal(
        lambda sig: print(f"📬 [{sig.get('id')}] {sig.get('type')} | {sig.get('summary', '')}")
    )
    poller.start()

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        poller.stop()
        print("已停止")


if __name__ == "__main__":
    run_cli()
