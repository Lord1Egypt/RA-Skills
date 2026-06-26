"""
Logging system for NextLink skill.
Provides configurable logging with file rotation and multiple levels.
"""

import os
import sys
import json
import logging
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict, Any

# Log levels
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields if present
        if hasattr(record, "data") and record.data:
            log_data["data"] = record.data

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, default=str)


class ColoredFormatter(logging.Formatter):
    """Colored formatter for terminal output."""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        color = self.COLORS.get(record.levelname, "")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Base message
        msg = f"{timestamp} [{record.levelname}] {record.getMessage()}"

        # Add extra data if present
        if hasattr(record, "data") and record.data:
            msg += f" | {json.dumps(record.data, default=str)}"

        # Colorize
        return f"{color}{msg}{self.RESET}"


class Logger:
    """
    Configurable logger for NextLink skill.

    Environment variables:
    - IMM_LOG_LEVEL: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - IMM_LOG_FILE: Log file path (default: ~/.nexlink/logs/imm.log)
    - IMM_LOG_FORMAT: Output format (json, text, colored)
    - IMM_LOG_MAX_SIZE: Max log file size in MB (default: 10)
    - IMM_LOG_BACKUP_COUNT: Number of backup files (default: 5)
    - IMM_LOG_CONSOLE: Enable console logging (true/false, default: true)
    """

    def __init__(self, name: str = "nexlink"):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Capture all, handlers filter

        # Prevent duplicate handlers
        if self.logger.handlers:
            return

        # Configuration from environment
        self.log_level = self._get_log_level()
        self.log_file = self._get_log_file()
        self.log_format = os.environ.get("IMM_LOG_FORMAT", "colored")
        self.max_bytes = int(os.environ.get("IMM_LOG_MAX_SIZE", "10")) * 1024 * 1024
        self.backup_count = int(os.environ.get("IMM_LOG_BACKUP_COUNT", "5"))
        self.console_enabled = (
            os.environ.get("IMM_LOG_CONSOLE", "true").lower() == "true"
        )

        # Setup handlers
        self._setup_handlers()

    def _get_log_level(self) -> int:
        """Get log level from environment."""
        level_str = os.environ.get("IMM_LOG_LEVEL", "INFO").upper()
        return LOG_LEVELS.get(level_str, logging.INFO)

    def _get_log_file(self) -> Optional[str]:
        """Get log file path from environment."""
        log_file = os.environ.get("IMM_LOG_FILE")
        if log_file:
            return log_file

        # Default location
        log_dir = os.path.expanduser("~/.nexlink/logs")
        os.makedirs(log_dir, exist_ok=True)
        return os.path.join(log_dir, "imm.log")

    def _setup_handlers(self):
        """Setup logging handlers."""
        # Console handler
        if self.console_enabled:
            console_handler = logging.StreamHandler(sys.stderr)
            console_handler.setLevel(self.log_level)

            if self.log_format == "json":
                console_handler.setFormatter(JSONFormatter())
            else:
                console_handler.setFormatter(ColoredFormatter())

            self.logger.addHandler(console_handler)

        # File handler with rotation
        if self.log_file:
            try:
                # Ensure directory exists with restrictive permissions
                log_dir = os.path.dirname(self.log_file)
                if log_dir:
                    os.makedirs(log_dir, exist_ok=True)
                    Path(log_dir).chmod(0o700)

                file_handler = RotatingFileHandler(
                    self.log_file,
                    maxBytes=self.max_bytes,
                    backupCount=self.backup_count,
                )
                file_handler.setLevel(self.log_level)
                file_handler.setFormatter(JSONFormatter())
                self.logger.addHandler(file_handler)
                Path(self.log_file).chmod(0o600)
            except (OSError, IOError) as e:
                # Can't write to log file, continue with console only
                self.logger.warning(f"Cannot write to log file {self.log_file}: {e}")

    def _log(self, level: int, message: str, data: Optional[Dict[str, Any]] = None):
        """Internal logging method."""
        extra = {"data": data} if data else {}
        self.logger.log(level, message, extra=extra)

    def debug(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log debug message."""
        self._log(logging.DEBUG, message, data)

    def info(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log info message."""
        self._log(logging.INFO, message, data)

    def warning(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log warning message."""
        self._log(logging.WARNING, message, data)

    def error(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log error message."""
        self._log(logging.ERROR, message, data)

    def critical(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log critical message."""
        self._log(logging.CRITICAL, message, data)

    def exception(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log exception with traceback."""
        extra = {"data": data} if data else {}
        self.logger.exception(message, extra=extra)

    # Convenience methods for common operations
    def log_request(self, method: str, url: str, data: Optional[Dict] = None):
        """Log HTTP request."""
        self.debug(f"Request: {method} {url}", {"data": data})

    def log_response(self, method: str, url: str, status: int, duration_ms: float):
        """Log HTTP response."""
        self.debug(
            f"Response: {method} {url}", {"status": status, "duration_ms": duration_ms}
        )

    def log_email_action(
        self, action: str, email_id: str, details: Optional[Dict] = None
    ):
        """Log email operation."""
        self.info(f"Email {action}", {"email_id": email_id, **(details or {})})

    def log_calendar_action(
        self, action: str, event_id: str, details: Optional[Dict] = None
    ):
        """Log calendar operation."""
        self.info(f"Calendar {action}", {"event_id": event_id, **(details or {})})

    def log_task_action(
        self, action: str, task_id: str, details: Optional[Dict] = None
    ):
        """Log task operation."""
        self.info(f"Task {action}", {"task_id": task_id, **(details or {})})

    def log_connection(self, server: str, email: str, success: bool):
        """Log connection attempt."""
        if success:
            self.info("Connected to Exchange", {"server": server, "email": email})
        else:
            self.error("Connection failed", {"server": server, "email": email})


# Global logger instance
_logger: Optional[Logger] = None


def get_logger(name: str = "nexlink") -> Logger:
    """Get or create logger instance."""
    global _logger
    if _logger is None:
        _logger = Logger(name)
    return _logger


def configure_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format: str = "colored",
    console: bool = True,
) -> Logger:
    """
    Configure logging from code.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (None to disable file logging)
        format: Output format (json, text, colored)
        console: Enable console logging

    Returns:
        Configured logger instance
    """
    # Set environment variables before creating logger
    os.environ["IMM_LOG_LEVEL"] = level
    if log_file:
        os.environ["IMM_LOG_FILE"] = log_file
    os.environ["IMM_LOG_FORMAT"] = format
    os.environ["IMM_LOG_CONSOLE"] = "true" if console else "false"

    # Reset global logger to apply new config
    global _logger
    _logger = Logger("nexlink")

    return _logger
