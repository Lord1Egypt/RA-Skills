"""
error_utils.py — 统一错误处理工具
2026-07-18 新增，Phase 1.3 错误处理

提供：
- retry_with_backoff: 指数退避重试
- graceful_degradation: 降级策略装饰器
- log_error: 结构化错误日志
"""

import sys
import time
import functools
import traceback
from datetime import datetime


def log_error(module: str, operation: str, error: Exception, context: dict = None):
    """结构化错误日志，输出到 stderr"""
    ts = datetime.now().strftime("%H:%M:%S")
    ctx_str = ""
    if context:
        ctx_str = " | " + " | ".join(f"{k}={v}" for k, v in context.items())
    print(f"[{ts}] ❌ {module}.{operation}: {type(error).__name__}: {error}{ctx_str}",
          file=sys.stderr)


def log_warning(module: str, operation: str, message: str):
    """结构化警告日志"""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] ⚠️  {module}.{operation}: {message}", file=sys.stderr)


def log_info(module: str, operation: str, message: str):
    """结构化信息日志"""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] ℹ️  {module}.{operation}: {message}", file=sys.stderr)


def retry_with_backoff(func=None, *, max_retries: int = 3, base_delay: float = 1.0,
                       max_delay: float = 10.0, retryable_exceptions: tuple = (Exception,)):
    """
    指数退避重试装饰器。

    用法:
        @retry_with_backoff(max_retries=3)
        def call_api(): ...

        # 或直接调用
        result = retry_with_backoff(call_api, max_retries=2)
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries + 1):
                try:
                    return fn(*args, **kwargs)
                except retryable_exceptions as e:
                    last_error = e
                    if attempt < max_retries:
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        log_warning(
                            fn.__module__ or "unknown",
                            fn.__name__,
                            f"尝试 {attempt + 1}/{max_retries} 失败: {e}, "
                            f"{delay:.1f}s 后重试"
                        )
                        time.sleep(delay)
                    else:
                        log_error(
                            fn.__module__ or "unknown",
                            fn.__name__,
                            e,
                            {"attempts": max_retries + 1}
                        )
            raise last_error
        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


def safe_execute(default=None, log_errors=True):
    """
    安全执行装饰器：捕获异常，返回默认值。

    用法:
        @safe_execute(default=[])
        def risky_operation(): ...
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    log_error(
                        fn.__module__ or "unknown",
                        fn.__name__,
                        e
                    )
                return default
        return wrapper
    return decorator


def validate_input(data, required_fields: list, module: str = "unknown") -> list:
    """
    输入验证：检查必填字段，返回错误列表。

    Returns:
        [] if valid, [error_msg, ...] if invalid
    """
    errors = []
    for field in required_fields:
        value = data.get(field) if isinstance(data, dict) else getattr(data, field, None)
        if value is None or (isinstance(value, (str, list, dict)) and len(value) == 0):
            errors.append(f"缺少必填字段: {field}")
    if errors:
        log_warning(module, "validate_input", "; ".join(errors))
    return errors
