"""
Unified logging utilities for IMA video generation.
"""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(
    name: str = "ima_skills",
    log_level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 7,
    console_output: bool = True,
) -> logging.Logger:
    """Create or return a configured logger with file + console handlers."""
    log_dir = Path.home() / ".openclaw" / "logs" / "ima_skills"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"ima_create_{datetime.now().strftime('%Y%m%d')}.log"
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-5s | %(funcName)-20s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError:
        # Fall back to console-only logging in restricted environments.
        pass

    if console_output:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def get_logger(name: str = "ima_skills") -> logging.Logger:
    """Get an existing configured logger or create one."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger


def cleanup_old_logs(days: int = 7) -> None:
    """Delete log files older than the configured retention period."""
    try:
        log_dir = Path.home() / ".openclaw" / "logs" / "ima_skills"
        if not log_dir.exists():
            return

        cutoff_time = datetime.now().timestamp() - (days * 24 * 3600)
        for log_file in log_dir.glob("ima_create_*.log*"):
            if log_file.stat().st_mtime < cutoff_time:
                log_file.unlink()
    except Exception:
        pass


def log_info(message: str) -> None:
    """Log info message to stderr."""
    print(message, file=sys.stderr)


def log_error(message: str) -> None:
    """Log error message to stderr."""
    print(f"ERROR: {message}", file=sys.stderr)


def log_debug(message: str) -> None:
    """Log debug message to stderr only if IMA_DEBUG is set."""
    if os.getenv("IMA_DEBUG"):
        print(f"DEBUG: {message}", file=sys.stderr)


def log_warning(message: str) -> None:
    """Log warning message to stderr."""
    print(f"WARNING: {message}", file=sys.stderr)
