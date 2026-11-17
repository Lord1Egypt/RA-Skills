#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CircuitBreaker — 熔断器 + 半开恢复 + 指数退避

架构重构要点：
  1. HALF_OPEN 自动超时恢复（不再永久 OPEN）
  2. 指数退避重试（独立函数，不依赖 threading.Thread）
  3. 移除幂等性检查（不属于熔断器职责）
  4. 熔断计数支持滑动窗口（避免旧失败累积误判）
  5. 指标导出（监控友好）
"""

import time
import random
import logging
import functools
from enum import Enum

logger = logging.getLogger("circuit_breaker")


class CircuitState(Enum):
    CLOSED = "closed"      # 正常
    OPEN = "open"          # 熔断中
    HALF_OPEN = "half_open"  # 半开试探


class CircuitBreaker:
    """
    熔断器 — 保护下游调用不被无限重试拖垮

    状态机：
      CLOSED ──(连续 N 次失败)──▶ OPEN
      OPEN ──(超过 recovery_timeout)──▶ HALF_OPEN
      HALF_OPEN ──(1 次成功)──▶ CLOSED
      HALF_OPEN ──(1 次失败)──▶ OPEN  (重置 recovery_timeout)
    """

    def __init__(
        self,
        max_consecutive_failures: int = 3,
        recovery_timeout: float = 60.0,
        window_seconds: float = 300.0,
    ):
        self.max_failures = max_consecutive_failures
        self.recovery_timeout = recovery_timeout
        self.window_seconds = window_seconds

        self.state = CircuitState.CLOSED
        self._failures: list = []            # [(timestamp,), ...] 滑动窗口
        self._consecutive = 0                # 当前连续失败计数
        self._last_open_time = 0.0
        self.total_failures = 0
        self.total_skipped = 0
        self.total_successes = 0

    # ── 运行 ──────────────────────────────────

    def run(self, fn, *args, timeout: float = 180.0, fallback=None, **kwargs):
        """
        在熔断保护下执行 fn

        参数:
          fn        — 要执行的函数
          timeout   — 超时秒数
          fallback  — 熔断时的回退值
        """
        # 检查是否 OPEN
        if self.state == CircuitState.OPEN:
            elapsed = time.time() - self._last_open_time
            if elapsed >= self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                logger.info(f"circuit_breaker: OPEN→HALF_OPEN (经过 {elapsed:.0f}s)")
            else:
                self.total_skipped += 1
                logger.warning(
                    f"circuit_breaker: {fn.__name__} 跳过 (OPEN, "
                    f"剩余 {self.recovery_timeout - elapsed:.0f}s)"
                )
                return fallback, False, "circuit_open"

        # 执行
        result, ok, reason = self._do_call(fn, timeout, *args, **kwargs)

        if ok:
            self._record_success()
        else:
            self._record_failure()

        return result, ok, reason

    def run_with_timeout(self, fn, chapter: int, *args, **kwargs):
        """兼容旧接口的包装"""
        result, ok, reason = self.run(fn, *args, timeout=self.recovery_timeout, **kwargs)
        if not ok:
            logger.warning(f"circuit_breaker: ch{chapter} fail: {reason}")
        return result, ok, reason

    # ── 内部 ──────────────────────────────────

    def _do_call(self, fn, timeout, *args, **kwargs):
        """执行调用（无超时版本—由业务层自行处理超时）"""
        import threading
        result_container = []
        exception_container = []

        def target():
            try:
                result = fn(*args, **kwargs)
                result_container.append(result)
            except Exception as e:
                exception_container.append(e)

        t = threading.Thread(target=target, daemon=True)
        t.start()
        t.join(timeout=timeout)

        if t.is_alive():
            return None, False, f"timeout ({timeout}s)"
        if exception_container:
            return None, False, str(exception_container[0])
        return result_container[0], True, ""

    def _record_success(self):
        self._consecutive = 0
        self.total_successes += 1
        self.state = CircuitState.CLOSED

    def _record_failure(self):
        now = time.time()
        # 滑动窗口：移除窗口外的旧失败记录
        self._failures = [t for t in self._failures if now - t < self.window_seconds]
        self._failures.append(now)
        self._consecutive += 1
        self.total_failures += 1

        # 连续失败 >= N 或 窗口内失败 >= N*2 → 熔断
        if self._consecutive >= self.max_failures:
            self._open()
        elif len(self._failures) >= self.max_failures * 2:
            self._open()

    def _open(self):
        self.state = CircuitState.OPEN
        self._last_open_time = time.time()
        logger.warning(
            f"circuit_breaker: CIRCUIT OPEN "
            f"(连续{self._consecutive}次失败, "
            f"窗口{self.window_seconds:.0f}s内{len(self._failures)}次)"
        )

    # ── 重置 ──────────────────────────────────

    def reset(self):
        """手动重置熔断器"""
        self.state = CircuitState.CLOSED
        self._consecutive = 0
        self._failures.clear()
        logger.info("circuit_breaker: 手动重置")

    def stats(self) -> dict:
        """指标快照"""
        return {
            "state": self.state.value,
            "consecutive_failures": self._consecutive,
            "window_failures": len(self._failures),
            "total_failures": self.total_failures,
            "total_successes": self.total_successes,
            "total_skipped": self.total_skipped,
        }


# ── 函数装饰器：指数退避重试 ─────────────────


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    retryable_exceptions: tuple = (Exception,),
):
    """
    指数退避 + 随机抖动 重试装饰器

    用法:
        @retry_with_backoff(max_retries=3)
        def upload(data):
            ...
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(max_retries + 1):
                try:
                    return fn(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exc = e
                    if attempt == max_retries:
                        raise
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    jitter = delay * random.uniform(-0.3, 0.3)
                    actual = delay + jitter
                    logger.debug(
                        f"retry_with_backoff: {fn.__name__} "
                        f"attempt {attempt + 1}/{max_retries} "
                        f"重试 in {actual:.1f}s: {e}"
                    )
                    time.sleep(actual)
            raise last_exc
        return wrapper
    return decorator


def check_idempotent_chapter(novel_state_or_repo, chapter_id: int) -> bool:
    """检查章节是否已写（幂等性校验）

    兼容两种参数类型：
    - NovelState 对象（旧接口，通过 property 代理到 __state）
    - StateRepository 对象（新接口）

    written 统一为 int。
    """
    from pathlib import Path as _Path

    # 尝试通过 StateRepository 读取
    try:
        if hasattr(novel_state_or_repo, 'load'):
            state = novel_state_or_repo.load()
            written = state.progress.written
            book_dir = getattr(novel_state_or_repo, 'book_dir',
                               getattr(novel_state_or_repo, '_state_path', _Path('.')).parent)
        else:
            # 旧接口兼容：通过 NovelState property
            progress = novel_state_or_repo._state.get("progress", {})
            written = progress.get("written", 0)
            if isinstance(written, list):
                written = max(written) if written else 0
            book_dir = getattr(novel_state_or_repo, 'book_dir', _Path('.'))
    except Exception:
        return True  # 无法判断时允许继续

    if chapter_id <= written:
        ch_dir = _Path(book_dir) / "正文"
        ch_file = ch_dir / f"第{chapter_id:03d}章.txt"
        if ch_file.exists():
            logger.warning(f"ch{chapter_id} already written, skip")
            return False
    return True
