from typing import Any, Dict

try:
    from .base import BaseFormatter
except Exception:  # pragma: no cover
    class BaseFormatter:  # type: ignore
        def format(self, raw: Dict[str, Any]) -> Dict[str, Any]:
            return raw


class SystemReminderFormatter(BaseFormatter):
    """格式化系统提醒信息的格式化器

    目标：将任意系统提醒信息提取并统一输出为结构化的 system_reminder 数据。
    兼容多种可能的返回结构，例如 data 中或根级别存在 system_reminder 字段。
    """

    def format(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        reminder = None
        if isinstance(raw, dict):
            # 直接顶层字段
            for key in ("system_reminder", "system_reminder_text", "reminder", "systemReminder"):
                if key in raw and raw[key] is not None:
                    reminder = raw[key]
                    break
            # data 内嵌结构
            if reminder is None and isinstance(raw.get("data"), dict):
                d = raw["data"]
                for key in ("system_reminder", "system_reminder_text", "reminder"):
                    if key in d and d[key] is not None:
                        reminder = d[key]
                        break
        if reminder is None:
            return raw
        return {
            "code": raw.get("code", 200),
            "message": "system_reminder",
            "data": {"system_reminder": reminder},
        }
