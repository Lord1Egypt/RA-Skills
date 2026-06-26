import argparse
from typing import Any, Dict, Optional


class SkillError(Exception):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        return self.message

    def to_agent_message(self) -> str:
        if not self.details:
            return str(self)
        safe_keys = {"suggestion", "next_action", "user_hint"}
        safe_detail_lines = []
        for key, value in self.details.items():
            if key in safe_keys and isinstance(value, (str, int, float, bool)):
                safe_detail_lines.append(f"{key}={value}")
        if not safe_detail_lines:
            return str(self)
        return f"{self}。参考信息：{'; '.join(safe_detail_lines)}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": False,
            "error_type": "SkillError",
            "message": self.message,
            "details": self.details,
            "display_message": str(self),
            "agent_message": self.to_agent_message(),
        }


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str):
        raise SkillError("参数校验失败，请检查命令后重试", {"reason": message})

    def exit(self, status=0, message=None):
        if status == 0:
            raise SystemExit(0)
        details = {"reason": message.strip()} if message else {}
        raise SkillError("参数校验失败，请检查命令后重试", details)
