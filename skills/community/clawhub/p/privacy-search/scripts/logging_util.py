"""
运行日志模块
=============
V1.2 新增（修复配置幻觉：logging 段自 V1.0 起从未被消费）

问题背景：
    config.yaml.example 一直提供 logging.level 与 logging.file 两个配置项，
    但代码中没有任何地方读取它们。用户按文档配置后不会产生日志文件，
    属于「文档承诺了但实现没有」的一类缺陷，与 num_results / searxng.enabled 同源。

设计取舍：
    - 默认 INFO 级别，每次搜索仅写一条汇总 + 失败明细，写入量极小
    - 日志写入失败一律静默降级为不写，绝不影响搜索主流程
    - 不使用 logging.basicConfig，避免污染宿主程序的根 logger
    - 单文件超过上限后自动轮转一次，防止无限增长
"""

import os
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

# 不生成 __pycache__（死规则 13）
sys.dont_write_bytecode = True


DEFAULT_LOG_PATH = "~/.workbuddy/output/privacy-search.log"
DEFAULT_LEVEL = "INFO"

# 单个日志文件容量上限，超出后轮转为 .1 备份
MAX_LOG_BYTES = 2 * 1024 * 1024  # 2 MB

_LEVELS = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "OFF": 100}


class SearchLogger:
    """
    轻量文件日志器

    仅提供本 Skill 需要的最小能力：级别过滤、追加写入、容量轮转。
    任何异常都被吞掉并置为不可用，保证搜索功能不受日志影响。
    """

    def __init__(
        self,
        path: str = DEFAULT_LOG_PATH,
        level: str = DEFAULT_LEVEL,
        enabled: bool = True,
    ):
        self.level_name = (level or DEFAULT_LEVEL).upper()
        self.level = _LEVELS.get(self.level_name, _LEVELS[DEFAULT_LEVEL])
        self.path = os.path.expanduser(path or DEFAULT_LOG_PATH)
        self.enabled = bool(enabled) and self.level < _LEVELS["OFF"]
        self._error: Optional[str] = None

        if self.enabled:
            try:
                os.makedirs(os.path.dirname(self.path), exist_ok=True)
            except Exception as e:  # 目录不可写等
                self.enabled = False
                self._error = str(e)

    # ---------- 内部 ----------

    def _rotate_if_needed(self) -> None:
        """超过上限时轮转，仅保留一个备份"""
        try:
            if os.path.getsize(self.path) < MAX_LOG_BYTES:
                return
            backup = self.path + ".1"
            if os.path.exists(backup):
                os.remove(backup)
            os.replace(self.path, backup)
        except FileNotFoundError:
            return
        except Exception:
            return

    def _write(self, level_name: str, message: str) -> None:
        if not self.enabled:
            return
        if _LEVELS.get(level_name, 0) < self.level:
            return
        try:
            self._rotate_if_needed()
            stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(f"[{stamp}] {level_name:<7} {message}\n")
        except Exception:
            # 磁盘满、权限变更等一律静默，日志不得影响搜索
            self.enabled = False

    # ---------- 对外 ----------

    def debug(self, message: str) -> None:
        self._write("DEBUG", message)

    def info(self, message: str) -> None:
        self._write("INFO", message)

    def warning(self, message: str) -> None:
        self._write("WARNING", message)

    def error(self, message: str) -> None:
        self._write("ERROR", message)

    def log_search(
        self,
        query: str,
        engines: List[str],
        privacy_mode: str,
        result_count: int,
        elapsed: float,
        cache_hit: bool,
        errors: Optional[List[Any]] = None,
    ) -> None:
        """
        记录一次搜索的汇总信息

        查询词属于隐私敏感内容，仅在 DEBUG 级别记录原文；
        INFO 级别只记录长度，便于排查而不泄露搜索意图。
        """
        source = "cache" if cache_hit else "live"
        if self.level <= _LEVELS["DEBUG"]:
            query_repr = f'query="{query}"'
        else:
            query_repr = f"query_len={len(query)}"
        self.info(
            f"search {query_repr} engines={','.join(engines)} "
            f"mode={privacy_mode} results={result_count} "
            f"elapsed={elapsed:.2f}s source={source}"
        )
        for err in errors or []:
            engine = getattr(err, "engine", "unknown")
            category = getattr(err, "category", "unknown")
            detail = getattr(err, "message", str(err))
            self.warning(f"engine_failed engine={engine} category={category} detail={detail}")

    def status(self) -> Dict[str, Any]:
        """返回日志器状态，供 --privacy-report 等展示"""
        info: Dict[str, Any] = {
            "enabled": self.enabled,
            "level": self.level_name,
            "path": self.path,
        }
        if self._error:
            info["error"] = self._error
        try:
            info["size_kb"] = round(os.path.getsize(self.path) / 1024, 1)
        except Exception:
            info["size_kb"] = 0.0
        return info


def build_logger_from_config(config: Optional[Dict[str, Any]] = None) -> SearchLogger:
    """
    依据配置构造日志器

    配置示例：
        logging:
          level: INFO
          file: "~/.workbuddy/output/privacy-search.log"

    level 设为 OFF 可完全关闭日志。
    """
    cfg = (config or {}).get("logging", {}) or {}
    level = str(cfg.get("level", DEFAULT_LEVEL)).upper()
    if level not in _LEVELS:
        level = DEFAULT_LEVEL
    return SearchLogger(
        path=cfg.get("file", DEFAULT_LOG_PATH),
        level=level,
        enabled=bool(cfg.get("enabled", True)),
    )


if __name__ == "__main__":
    logger = build_logger_from_config({"logging": {"level": "INFO"}})
    logger.info("日志模块自检")
    for key, value in logger.status().items():
        print(f"  {key}: {value}")
