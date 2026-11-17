"""统一日志模块

提供分级日志记录：
- DEBUG: 调试信息
- INFO: 一般运行信息
- WARNING: 警告
- ERROR: 错误
- CRITICAL: 严重错误

日志同时输出到控制台和文件（output/logs/{feature}_{timestamp}.log）
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

# 项目根目录
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_LOGS_DIR = _PROJECT_ROOT / "output" / "logs"


class Logger:
    """统一日志记录器"""

    LEVEL_MAP = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    def __init__(
        self,
        feature: str = "main",
        level: str = "INFO",
        log_to_file: bool = True,
        log_to_console: bool = True,
    ):
        """初始化日志记录器

        Args:
            feature: 功能模块名（用于日志文件命名）
            level: 日志级别 DEBUG/INFO/WARNING/ERROR/CRITICAL
            log_to_file: 是否写入日志文件
            log_to_console: 是否输出到控制台
        """
        self.feature = feature
        self.level = self.LEVEL_MAP.get(level.upper(), logging.INFO)
        self.logger = logging.getLogger(f"mc_skill.{feature}")
        self.logger.setLevel(self.level)
        # 防止重复添加handler
        self.logger.handlers.clear()

        # 日志格式
        fmt = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # 控制台输出
        if log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.level)
            console_handler.setFormatter(fmt)
            self.logger.addHandler(console_handler)

        # 文件输出
        if log_to_file:
            _LOGS_DIR.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = _LOGS_DIR / f"{feature}_{timestamp}.log"
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(self.level)
            file_handler.setFormatter(fmt)
            self.logger.addHandler(file_handler)
            self._log_file = log_file
        else:
            self._log_file = None

        # 设置propagate=False避免根logger重复输出
        self.logger.propagate = False

    @property
    def log_file(self) -> Path:
        """返回日志文件路径"""
        return self._log_file

    def debug(self, msg: str, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs):
        """记录异常信息（包含堆栈）"""
        self.logger.exception(msg, *args, **kwargs)


def get_logger(feature: str = "main", level: str = "INFO") -> Logger:
    """获取日志记录器实例

    Args:
        feature: 功能模块名
        level: 日志级别

    Returns:
        Logger实例
    """
    return Logger(feature=feature, level=level)
