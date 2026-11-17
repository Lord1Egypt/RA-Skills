#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Love Companion - Configuration & Memory Manager
恋人主题技能 - 配置与记忆管理模块

功能：
- 人设配置的 CRUD 操作
- 多方案管理与切换
- 长时记忆存储与检索
- 配置导入导出
- 预设模板加载（唯一数据源：references/personas.md）

使用方式：
本脚本由 AI Agent 自动调用，用户无需手动执行。
所有操作通过标准化指令触发。

许可证：MIT License
"""

import copy
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class LoveCompanionManager:
    """恋人配置管理器"""

    # 默认存储路径（通用化，不再绑定特定框架）
    DEFAULT_STORAGE_PATH = "~/.love-companion/data"

    # 环境变量名，可覆盖默认存储路径
    ENV_STORAGE_PATH = "LOVE_COMPANION_DATA_DIR"

    # 预设人设的唯一数据源（技能包根目录下的 references/personas.md）
    # 代码内不再保留第二份预设，避免与文档文案漂移
    PERSONAS_FILE = Path(__file__).resolve().parent.parent / "references" / "personas.md"

    # 环境变量名，可覆盖预设文件路径（便于测试或自定义预设库）
    ENV_PERSONAS_FILE = "LOVE_COMPANION_PERSONAS_FILE"

    # 默认人设模板
    DEFAULT_PERSONA = {
        "姓名": "",
        "昵称": "",
        "性别": "",
        "年龄": 0,
        "对用户的称呼": "",
        "性格": {
            "核心特质": [],
            "小脾气": [],
            "情绪表达": ""
        },
        "对话风格": {
            "语气": "",
            "口头禅": [],
            "语言习惯": ""
        },
        "背景故事": "",
        "相处模式": {
            "主动程度": "中",
            "撒娇频率": "中",
            "关心方式": ""
        },
        "亲密尺度": 3,
        "内容边界": []
    }

    # ---- 预设文档（personas.md）解析规则 ----

    # 章节标题，如 "### 【1号】阳光开朗型"
    _PRESET_SECTION_RE = re.compile(r"^###\s*【(\d+)\s*号】\s*(.+?)\s*$", re.M)

    # 章节内首个 JSON 配置块
    _PRESET_JSON_RE = re.compile(r"```json\s*\n(.*?)\n```", re.S)

    # 章节内的特点描述，如 "**特点**：像小太阳一样温暖…"
    _PRESET_DESC_RE = re.compile(r"\*\*特点\*\*：(.+)")

    def __init__(self, storage_path: Optional[str] = None):
        """初始化管理器

        存储路径优先级：
        1. 构造参数 storage_path
        2. 环境变量 LOVE_COMPANION_DATA_DIR
        3. 默认路径 ~/.love-companion/data
        """
        resolved = (
            storage_path
            or os.environ.get(self.ENV_STORAGE_PATH)
            or self.DEFAULT_STORAGE_PATH
        )
        self.storage_path = Path(os.path.expanduser(resolved))
        self._preset_cache: Optional[List[Dict[str, Any]]] = None
        self._ensure_storage_dirs()

    def _ensure_storage_dirs(self) -> None:
        """确保存储目录存在"""
        dirs = [
            self.storage_path,
            self.storage_path / "schemes"
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    # ==================== 配置管理 ====================

    def get_persona(self) -> Dict[str, Any]:
        """获取当前人设配置（utf-8-sig：兼容 Windows 记事本/WPS 写入的 BOM 文件）"""
        config_file = self.storage_path / "persona.json"
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        return self.DEFAULT_PERSONA.copy()

    def set_persona(self, persona: Dict[str, Any]) -> Dict[str, Any]:
        """设置完整人设配置"""
        config_file = self.storage_path / "persona.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(persona, f, ensure_ascii=False, indent=2)
        return persona

    def update_persona(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """更新部分人设配置（合并）"""
        current = self.get_persona()
        current = self._deep_merge(current, updates)
        return self.set_persona(current)

    def set_persona_field(self, path: str, value: Any) -> Dict[str, Any]:
        """设置人设的单个字段

        Args:
            path: 字段路径，如 "性格.核心特质" 或 "姓名"
            value: 要设置的值
        """
        current = self.get_persona()
        keys = path.split(".")
        obj = current

        for key in keys[:-1]:
            if key not in obj:
                obj[key] = {}
            obj = obj[key]

        obj[keys[-1]] = value
        return self.set_persona(current)

    def reset_persona(self) -> Dict[str, Any]:
        """重置为默认人设"""
        return self.set_persona(self.DEFAULT_PERSONA.copy())

    # ==================== 方案管理 ====================

    def list_schemes(self) -> List[Dict[str, Any]]:
        """列出所有已保存的人设方案"""
        schemes_dir = self.storage_path / "schemes"
        schemes = []

        for scheme_file in schemes_dir.glob("*.json"):
            with open(scheme_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                schemes.append({
                    "name": scheme_file.stem,
                    "created_at": data.get("_created_at", ""),
                    "persona": data.get("persona", {})
                })

        return schemes

    def save_scheme(self, name: str) -> bool:
        """保存当前人设为方案"""
        persona = self.get_persona()
        scheme_data = {
            "persona": persona,
            "_created_at": datetime.now().isoformat()
        }

        scheme_file = self.storage_path / "schemes" / f"{name}.json"
        with open(scheme_file, "w", encoding="utf-8") as f:
            json.dump(scheme_data, f, ensure_ascii=False, indent=2)
        return True

    def load_scheme(self, name: str) -> Optional[Dict[str, Any]]:
        """加载指定方案"""
        scheme_file = self.storage_path / "schemes" / f"{name}.json"

        if not scheme_file.exists():
            return None

        with open(scheme_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            persona = data.get("persona", {})
            return self.set_persona(persona)

    def delete_scheme(self, name: str) -> bool:
        """删除指定方案"""
        scheme_file = self.storage_path / "schemes" / f"{name}.json"

        if scheme_file.exists():
            scheme_file.unlink()
            return True
        return False

    # ==================== 预设模板 ====================

    @classmethod
    def personas_file(cls) -> Path:
        """返回预设人设文件路径（支持环境变量覆盖）"""
        override = os.environ.get(cls.ENV_PERSONAS_FILE)
        return Path(override).expanduser() if override else cls.PERSONAS_FILE

    def _read_personas_md(self) -> str:
        """读取预设人设文档内容"""
        path = self.personas_file()
        if not path.exists():
            raise FileNotFoundError(
                f"预设人设文件不存在：{path}。"
                f"请确认 references/personas.md 与 scripts/manager.py 位于同一技能包内，"
                f"或用环境变量 {self.ENV_PERSONAS_FILE} 指定路径。"
            )
        return path.read_text(encoding="utf-8")

    def _parse_presets(self) -> List[Dict[str, Any]]:
        """解析 references/personas.md，提取全部预设人设

        解析规则：
        - 以「### 【N号】类型名」切分章节
        - 每节内首个 ```json 代码块即该预设的完整人设配置
        - 「**特点**：…」作为预设描述

        Raises:
            FileNotFoundError: 预设文档不存在
            ValueError: 找不到章节，或某预设的 JSON 配置无法解析（错误信息会指出编号）
        """
        md = self._read_personas_md()
        marks = list(self._PRESET_SECTION_RE.finditer(md))
        if not marks:
            raise ValueError(
                f"未在预设文件中找到任何「### 【N号】」章节：{self.personas_file()}"
            )

        presets: List[Dict[str, Any]] = []
        for index, mark in enumerate(marks):
            start = mark.end()
            end = marks[index + 1].start() if index + 1 < len(marks) else len(md)
            section = md[start:end]

            preset_id = int(mark.group(1))
            preset_type = mark.group(2).strip()

            json_match = self._PRESET_JSON_RE.search(section)
            if not json_match:
                raise ValueError(
                    f"预设 {preset_id} 号（{preset_type}）缺少 ```json 配置块"
                )
            try:
                persona = json.loads(json_match.group(1))
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"预设 {preset_id} 号（{preset_type}）的 JSON 配置无法解析：{exc}。"
                    f"常见原因：配置文案中存在未转义的双引号。"
                ) from exc

            desc_match = self._PRESET_DESC_RE.search(section)
            presets.append({
                "id": preset_id,
                "类型": preset_type,
                "描述": desc_match.group(1).strip() if desc_match else "",
                "persona": persona,
            })

        return presets

    def _get_presets(self) -> List[Dict[str, Any]]:
        """获取预设列表（首次读取后缓存）"""
        if self._preset_cache is None:
            self._preset_cache = self._parse_presets()
        return self._preset_cache

    def list_presets(self) -> List[Dict[str, Any]]:
        """列出所有可用预设（不含完整人设内容）

        Returns:
            [{"id": 1, "类型": "阳光开朗型", "描述": "…"}, …]
        """
        return [
            {k: v for k, v in preset.items() if k != "persona"}
            for preset in self._get_presets()
        ]

    def load_preset(self, preset_id: int) -> Optional[Dict[str, Any]]:
        """套用预设模板，写入当前人设配置

        Args:
            preset_id: 预设编号，对应 personas.md 中的「N号」

        Returns:
            套用后的人设配置；编号不存在时返回 None
        """
        for preset in self._get_presets():
            if preset["id"] == int(preset_id):
                # 深拷贝，避免调用方修改污染缓存的预设模板
                return self.set_persona(copy.deepcopy(preset["persona"]))
        return None

    # ==================== 记忆管理 ====================

    def get_memories(self) -> List[Dict[str, Any]]:
        """获取所有长时记忆（utf-8-sig：兼容带 BOM 的文件）"""
        memory_file = self.storage_path / "memory.json"

        if memory_file.exists():
            with open(memory_file, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        return []

    def add_memory(self, content: str) -> Dict[str, Any]:
        """添加记忆"""
        memories = self.get_memories()
        new_memory = {
            "id": len(memories) + 1,
            "content": content,
            "created_at": datetime.now().isoformat()
        }
        memories.append(new_memory)

        memory_file = self.storage_path / "memory.json"
        with open(memory_file, "w", encoding="utf-8") as f:
            json.dump(memories, f, ensure_ascii=False, indent=2)

        return new_memory

    def delete_memory(self, keyword: str) -> int:
        """删除包含关键词的记忆，返回删除数量"""
        memories = self.get_memories()
        original_count = len(memories)

        memories = [m for m in memories if keyword.lower() not in m.get("content", "").lower()]

        memory_file = self.storage_path / "memory.json"
        with open(memory_file, "w", encoding="utf-8") as f:
            json.dump(memories, f, ensure_ascii=False, indent=2)

        return original_count - len(memories)

    def clear_memories(self) -> int:
        """清空所有记忆，返回清除数量"""
        memories = self.get_memories()
        count = len(memories)

        memory_file = self.storage_path / "memory.json"
        with open(memory_file, "w", encoding="utf-8") as f:
            json.dump([], f)

        return count

    # ==================== 导入导出 ====================

    def export_persona(self) -> str:
        """导出人设配置为JSON字符串"""
        persona = self.get_persona()
        return json.dumps(persona, ensure_ascii=False, indent=2)

    def import_persona(self, json_str: str) -> Dict[str, Any]:
        """从JSON字符串导入人设配置"""
        persona = json.loads(json_str)
        if not isinstance(persona, dict):
            raise ValueError(f"人设必须是 JSON 对象，收到 {type(persona).__name__}")
        return self.set_persona(persona)

    # ==================== 工具方法 ====================

    def _deep_merge(self, base: Dict, updates: Dict) -> Dict:
        """深度合并两个字典"""
        result = base.copy()

        for key, value in updates.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    def get_status(self) -> Dict[str, Any]:
        """获取当前状态"""
        persona = self.get_persona()
        memories = self.get_memories()
        schemes = self.list_schemes()

        try:
            preset_count: Optional[int] = len(self._get_presets())
        except (FileNotFoundError, ValueError):
            preset_count = None

        return {
            "persona_name": persona.get("姓名", "未设置"),
            "memory_count": len(memories),
            "scheme_count": len(schemes),
            "preset_count": preset_count,
            "storage_path": str(self.storage_path)
        }


# ==================== 命令行接口（调试用） ====================

USAGE = """Love Companion Manager - Configuration & Memory Tool

Usage: python manager.py <command> [args]

Commands:
  status                  Show current status
  get                     Print current persona as JSON
  set <path> <value>      Set one persona field (path 用点分隔，如 性格.核心特质)
  update <json>           Merge a partial persona JSON into current config
  import <json>           Replace persona with a full JSON document
  reset                   Reset persona to default
  presets                 List preset personas (source: references/personas.md)
  apply <n>               Apply preset #n as the current persona
  schemes                 List saved schemes
  save <name>             Save current persona as a named scheme
  switch <name>           Load a saved scheme as the current persona
  delete-scheme <name>    Delete a saved scheme
  memory-list             List long-term memories
  memory-clear            Clear all long-term memories
"""


if __name__ == "__main__":
    import sys

    manager = LoveCompanionManager()
    args = sys.argv[1:]

    if not args:
        print(USAGE)
        sys.exit(1)

    command, params = args[0], args[1:]

    def require(what: str) -> str:
        if not params:
            print(f"Missing argument: {what}")
            sys.exit(1)
        return params[0]

    if command == "status":
        print(json.dumps(manager.get_status(), ensure_ascii=False, indent=2))

    elif command == "get":
        print(manager.export_persona())

    elif command == "set":
        path = require("field path")
        raw = require("value")
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            value = raw
        manager.set_persona_field(path, value)
        print(f"Set {path}.")

    elif command == "update":
        raw = require("partial persona json")
        try:
            manager.update_persona(json.loads(raw))
        except json.JSONDecodeError as exc:
            print(f"Invalid JSON: {exc}")
            sys.exit(1)
        print("Persona updated.")

    elif command == "import":
        raw = require("full persona json")
        try:
            manager.import_persona(raw)
        except (json.JSONDecodeError, ValueError) as exc:
            print(f"Invalid persona JSON: {exc}")
            sys.exit(1)
        print("Persona imported.")

    elif command == "reset":
        manager.reset_persona()
        print("Persona reset to default.")

    elif command == "presets":
        for preset in manager.list_presets():
            print(f"{preset['id']}. {preset['类型']} - {preset['描述']}")

    elif command == "apply":
        raw_id = require("preset id")
        try:
            preset_id = int(raw_id)
        except ValueError:
            print(f"Preset id must be a number, got: {raw_id}")
            sys.exit(1)
        if manager.load_preset(preset_id) is None:
            print(f"Preset #{preset_id} not found.")
            sys.exit(1)
        print(f"Applied preset #{preset_id}: {manager.get_persona().get('姓名', '')}")

    elif command == "schemes":
        schemes = manager.list_schemes()
        if not schemes:
            print("No saved schemes.")
        for scheme in schemes:
            print(f"- {scheme['name']} ({scheme['created_at']})")

    elif command == "save":
        name = require("scheme name")
        manager.save_scheme(name)
        print(f"Scheme saved: {name}")

    elif command == "switch":
        name = require("scheme name")
        if manager.load_scheme(name) is None:
            print(f"Scheme not found: {name}")
            sys.exit(1)
        print(f"Switched to scheme: {name}")

    elif command == "delete-scheme":
        name = require("scheme name")
        if manager.delete_scheme(name):
            print(f"Scheme deleted: {name}")
        else:
            print(f"Scheme not found: {name}")
            sys.exit(1)

    elif command == "memory-list":
        memories = manager.get_memories()
        if not memories:
            print("No memories.")
        for memory in memories:
            print(f"{memory['id']}. {memory['content']} ({memory['created_at']})")

    elif command == "memory-clear":
        print(f"Cleared {manager.clear_memories()} memories.")

    else:
        print(f"Unknown command: {command}")
        print()
        print(USAGE)
        sys.exit(1)
