"""Structured logging with context propagation.

Uses the standard library logging module with a custom formatter that
emulates zerolog-style key=value output. A global LoggerAdapter carries
a request-scoped context dict through the application.
"""

from __future__ import annotations

import logging
import sys
import time
from typing import Any

_logger: ContextLogger | None = None


class ContextFormatter(logging.Formatter):
    """Formats log records as: TIME LEVEL key=value... message."""

    def format(self, record: logging.LogRecord) -> str:
        ts = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(record.created))
        ctx = getattr(record, "ctx", {})
        parts = [f"{ts} {record.levelname:<5}"]
        for k, v in ctx.items():
            parts.append(f"{k}={v}")
        parts.append(record.getMessage())
        return " ".join(parts)


class ContextLogger(logging.LoggerAdapter):
    """LoggerAdapter that merges a persistent context dict into every record."""

    def __init__(self, context: dict[str, Any] | None = None):
        super().__init__(logging.getLogger("twist"), context or {})

    def process(self, msg: str, kwargs: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        extra = kwargs.get("extra", {})
        extra["ctx"] = dict(self.extra)
        kwargs["extra"] = extra
        return msg, kwargs


def init(*, verbose: bool = False) -> None:
    """Initialise the global logger.

    Must be called once before any logging calls. When *verbose* is True,
    the log level is set to DEBUG instead of INFO.
    """
    global _logger

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(ContextFormatter())

    root = logging.getLogger("twist")
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging.DEBUG if verbose else logging.INFO)
    root.propagate = False

    _logger = ContextLogger()


def get() -> ContextLogger:
    """Return the global ContextLogger instance."""
    if _logger is None:
        init()
    return _logger  # type: ignore[return-value]
