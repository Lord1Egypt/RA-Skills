"""Lightweight structured logging and runtime helpers."""

from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import json
import logging
import time
from typing import Any, Iterator


def configure_logging(level: str = "INFO") -> None:
    root = logging.getLogger("portfolio_risk_desk")
    if root.handlers:
        root.setLevel(level.upper())
        return
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    root.addHandler(handler)
    root.setLevel(level.upper())
    root.propagate = False


def get_logger() -> logging.Logger:
    return logging.getLogger("portfolio_risk_desk")


def log_event(event: str, **fields: Any) -> None:
    logger = get_logger()
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        **fields,
    }
    logger.info(json.dumps(payload, sort_keys=True))


@contextmanager
def timed_stage(stage: str, **fields: Any) -> Iterator[None]:
    started = time.perf_counter()
    log_event(f"{stage}.started", **fields)
    try:
        yield
    except Exception as error:
        elapsed_ms = round((time.perf_counter() - started) * 1000)
        log_event(f"{stage}.failed", elapsed_ms=elapsed_ms, error=str(error), **fields)
        raise
    elapsed_ms = round((time.perf_counter() - started) * 1000)
    log_event(f"{stage}.completed", elapsed_ms=elapsed_ms, **fields)
