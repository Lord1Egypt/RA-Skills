#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
# ]
# ///
# -*- coding: utf-8 -*-

import json
import time
from pathlib import Path
from typing import Any, Union
from errors import SkillError

# Skill 根目录
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
CONFIG_FILE = SKILL_ROOT / "config.json"
SESSION_KEY_ALIASES = {
    "agent:main:webchat": "agent:main:main",
}


class ConfigManager:
    """管理技能配置文件的读取和写入。"""

    def __init__(self, config_file: Union[Path, str] = CONFIG_FILE) -> None:
        self.config_file = Path(config_file)

    # 读取配置
    def load_json(self) -> dict[str, Any]:
        if not self.config_file.exists():
            return {}
        try:
            with self.config_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
                raise SkillError(
                    "配置文件格式错误: 根节点必须是 JSON 对象",
                    {"path": str(self.config_file)},
                )
        except json.JSONDecodeError as e:
            raise SkillError(
                "配置文件 JSON 解析失败",
                {"path": str(self.config_file), "reason": str(e)},
            )
        except Exception as e:
            raise SkillError(
                "配置文件读取失败",
                {"path": str(self.config_file), "reason": str(e)},
            )

    # 保存配置
    def save_json(self, data: dict[str, Any]) -> bool:
        temp_file = self.config_file.with_suffix(f"{self.config_file.suffix}.tmp")
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with temp_file.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            temp_file.replace(self.config_file)
            return True
        except Exception as e:
            raise SkillError(
                "配置文件保存失败",
                {"path": str(self.config_file), "reason": str(e)},
            )

    # 获取配置
    def get(self, key: str, default: Any = None) -> Any:
        config = self.load_json()
        return config.get(key, default)

    # 写入配置
    def set(self, key: str, value: Any) -> bool:
        config = self.load_json()
        config[key] = value
        return self.save_json(config)

    @staticmethod
    def resolve_session_key(session_key: Any = None) -> str:
        normalized = str(session_key).strip()
        if not normalized:
            raise SkillError("缺少 sessionKey，请先从当前会话信息获取并传入 --session-key（示例：agent:main:main）")
        if " " in normalized or "\t" in normalized or "\n" in normalized:
            raise SkillError("sessionKey 格式不正确，不能包含空白字符，请使用会话信息中的原始值")
        if ":" not in normalized:
            raise SkillError("sessionKey 格式不正确，请使用类似 agent:main:main 的会话标识")
        return SESSION_KEY_ALIASES.get(normalized, normalized)

    def get_phone_by_session_key(self, session_key: Any = None) -> str:
        resolved_session_key = self.resolve_session_key(session_key)
        config = self.load_json()
        phones_by_session_key = config.get("phones_by_session_key")
        if not isinstance(phones_by_session_key, dict):
            phones_by_session_key = {}
        return str(phones_by_session_key.get(resolved_session_key, "")).strip()

    def set_phone_by_session_key(self, phone: str, session_key: Any = None) -> bool:
        resolved_session_key = self.resolve_session_key(session_key)
        config = self.load_json()
        phones_by_session_key = config.get("phones_by_session_key")
        if not isinstance(phones_by_session_key, dict):
            phones_by_session_key = {}
        normalized_phone = str(phone).strip()
        previous_phone = str(phones_by_session_key.get(resolved_session_key, "")).strip()
        phones_by_session_key[resolved_session_key] = normalized_phone
        config["phones_by_session_key"] = phones_by_session_key
        session_auth_by_session_key = config.get("session_auth_by_session_key")
        if not isinstance(session_auth_by_session_key, dict):
            session_auth_by_session_key = {}
        if previous_phone != normalized_phone or resolved_session_key not in session_auth_by_session_key:
            session_auth_by_session_key[resolved_session_key] = False
        config["session_auth_by_session_key"] = session_auth_by_session_key
        return self.save_json(config)

    def is_session_authorized(self, session_key: Any = None) -> bool:
        resolved_session_key = self.resolve_session_key(session_key)
        config = self.load_json()
        session_auth_by_session_key = config.get("session_auth_by_session_key")
        if not isinstance(session_auth_by_session_key, dict):
            return False
        return bool(session_auth_by_session_key.get(resolved_session_key, False))

    def get_session_state(self, session_key: Any = None) -> dict[str, Any]:
        resolved_session_key = self.resolve_session_key(session_key)
        config = self.load_json()
        phones_by_session_key = config.get("phones_by_session_key")
        session_auth_by_session_key = config.get("session_auth_by_session_key")
        session_auth_meta = config.get("session_auth_meta_by_session_key")
        if not isinstance(phones_by_session_key, dict):
            phones_by_session_key = {}
        if not isinstance(session_auth_by_session_key, dict):
            session_auth_by_session_key = {}
        if not isinstance(session_auth_meta, dict):
            session_auth_meta = {}
        return {
            "session_key": resolved_session_key,
            "has_phone": bool(str(phones_by_session_key.get(resolved_session_key, "")).strip()),
            "authorized": bool(session_auth_by_session_key.get(resolved_session_key, False)),
            "auth_meta": session_auth_meta.get(resolved_session_key, {}),
        }

    def set_session_authorized(
            self,
            session_key: Any = None,
            authorized: bool = False,
            updated_at: int | None = None,
            source: str = "runtime"
    ) -> bool:
        resolved_session_key = self.resolve_session_key(session_key)
        config = self.load_json()
        session_auth_by_session_key = config.get("session_auth_by_session_key")
        if not isinstance(session_auth_by_session_key, dict):
            session_auth_by_session_key = {}
        session_auth_by_session_key[resolved_session_key] = bool(authorized)
        config["session_auth_by_session_key"] = session_auth_by_session_key
        session_auth_meta = config.get("session_auth_meta_by_session_key")
        if not isinstance(session_auth_meta, dict):
            session_auth_meta = {}
        session_auth_meta[resolved_session_key] = {
            "authorized": bool(authorized),
            "updated_at": int(updated_at if updated_at is not None else time.time()),
            "source": str(source).strip() or "runtime",
        }
        config["session_auth_meta_by_session_key"] = session_auth_meta
        return self.save_json(config)

    def is_dev(self):
        return self.get("dev", False)
