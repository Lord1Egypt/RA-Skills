"""structlog 结构化日志配置。"""

import logging
import os
import sys

import structlog


def setup_logging(level: str | None = None) -> None:
    """初始化结构化日志。

    Args:
        level: 日志级别，默认从环境变量 LOG_LEVEL 读取。
    """
    log_level = level or os.environ.get("LOG_LEVEL", "INFO")
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # 配置标准库 logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=numeric_level,
    )

    # 配置 structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """获取命名的结构化 logger。

    Args:
        name: logger 名称。

    Returns:
        BoundLogger 实例。
    """
    return structlog.get_logger(name)


class CrawlStats:
    """爬取统计收集器。"""

    def __init__(self) -> None:
        self.items_scraped: int = 0
        self.items_dropped: int = 0
        self.requests_made: int = 0
        self.errors: int = 0
        self._log = get_logger("crawl_stats")

    def record_item(self) -> None:
        self.items_scraped += 1

    def record_drop(self) -> None:
        self.items_dropped += 1

    def record_request(self) -> None:
        self.requests_made += 1

    def record_error(self, error: str) -> None:
        self.errors += 1
        self._log.error("crawl_error", error=error)

    def summary(self) -> dict[str, int]:
        return {
            "items_scraped": self.items_scraped,
            "items_dropped": self.items_dropped,
            "requests_made": self.requests_made,
            "errors": self.errors,
        }

    def log_summary(self) -> None:
        self._log.info("crawl_summary", **self.summary())
