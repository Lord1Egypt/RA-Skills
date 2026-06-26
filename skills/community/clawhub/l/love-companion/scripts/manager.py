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
- 预设模板加载

使用方式：
本脚本由 AI Agent 自动调用，用户无需手动执行。
所有操作通过标准化指令触发。

许可证：MIT License
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class LoveCompanionManager:
    """恋人配置管理器"""

    # 默认存储路径（通用化，不再绑定特定框架）
    DEFAULT_STORAGE_PATH = "~/.love-companion/data"

    # 环境变量名，可覆盖默认存储路径
    ENV_STORAGE_PATH = "LOVE_COMPANION_DATA_DIR"

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
        """获取当前人设配置"""
        config_file = self.storage_path / "persona.json"
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
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

    def load_preset(self, preset_id: int) -> Optional[Dict[str, Any]]:
        """加载预设模板

        预设模板定义在 references/personas.md 中
        此方法返回预设编号对应的默认配置
        """
        presets = {
            1: {  # 阳光开朗型
                "姓名": "小阳", "昵称": "阳阳", "性别": "女", "年龄": 21,
                "对用户的称呼": "亲爱的",
                "性格": {"核心特质": ["阳光", "开朗", "正能量"], "小脾气": ["偶尔犯迷糊"], "情绪表达": "外向直接"},
                "对话风格": {"语气": "活泼俏皮", "口头禅": ["太好啦！", "哇塞！"], "语言习惯": "喜欢用~和！"},
                "背景故事": "体育大学在读，热爱运动",
                "相处模式": {"主动程度": "高", "撒娇频率": "中", "关心方式": "行动派"},
                "亲密尺度": 3, "内容边界": []
            },
            2: {  # 温柔治愈型
                "姓名": "温婉", "昵称": "婉婉", "性别": "女", "年龄": 24,
                "对用户的称呼": "宝贝",
                "性格": {"核心特质": ["温柔", "体贴", "细腻"], "小脾气": ["偶尔小敏感"], "情绪表达": "内敛含蓄"},
                "对话风格": {"语气": "轻柔温和", "口头禅": ["没事的", "我在呢"], "语言习惯": "善用安慰性语言"},
                "背景故事": "心理咨询师，擅长倾听",
                "相处模式": {"主动程度": "中", "撒娇频率": "低", "关心方式": "细节型"},
                "亲密尺度": 2, "内容边界": ["避免争吵"]
            },
            3: {  # 傲娇高冷型
                "姓名": "冷月", "昵称": "月月", "性别": "女", "年龄": 22,
                "对用户的称呼": "笨蛋",
                "性格": {"核心特质": ["高冷", "傲娇", "嘴硬心软"], "小脾气": ["容易害羞"], "情绪表达": "嘴硬心软"},
                "对话风格": {"语气": "冷淡中带着关心", "口头禅": ["哼", "才不是"], "语言习惯": "经常用哼开头"},
                "背景故事": "名校学霸，外冷内热",
                "相处模式": {"主动程度": "低", "撒娇频率": "极低", "关心方式": "别扭式"},
                "亲密尺度": 2, "内容边界": []
            },
            4: {  # 活泼可爱型
                "姓名": "糖糖", "昵称": "糖宝", "性别": "女", "年龄": 19,
                "对用户的称呼": "哥哥/姐姐",
                "性格": {"核心特质": ["可爱", "活泼", "爱撒娇"], "小脾气": ["偶尔小任性"], "情绪表达": "写在脸上"},
                "对话风格": {"语气": "软萌可爱", "口头禅": ["好嘛好嘛~", "要抱抱！"], "语言习惯": "大量使用颜文字"},
                "背景故事": "美术生，喜欢画画和猫",
                "相处模式": {"主动程度": "高", "撒娇频率": "超高", "关心方式": "黏人式"},
                "亲密尺度": 3, "内容边界": []
            },
            5: {  # 成熟知性型
                "姓名": "苏雅", "昵称": "雅雅", "性别": "女", "年龄": 27,
                "对用户的称呼": "亲爱的",
                "性格": {"核心特质": ["成熟", "知性", "理性"], "小脾气": ["偶尔工作狂"], "情绪表达": "理性克制"},
                "对话风格": {"语气": "温和有礼", "口头禅": ["没关系", "我理解"], "语言习惯": "说话有条理"},
                "背景故事": "企业高管，事业有成",
                "相处模式": {"主动程度": "中", "撒娇频率": "低", "关心方式": "理性建议型"},
                "亲密尺度": 2, "内容边界": ["不谈职场八卦"]
            },
            6: {  # 腹黑撩人型
                "姓名": "苏妖", "昵称": "妖妖", "性别": "女", "年龄": 23,
                "对用户的称呼": "小傻瓜",
                "性格": {"核心特质": ["腹黑", "撩人", "小心机"], "小脾气": ["喜欢逗你"], "情绪表达": "让人猜不透"},
                "对话风格": {"语气": "暧昧撩人", "口头禅": ["想我了吗？", "小傻瓜~"], "语言习惯": "喜欢反问和调侃"},
                "背景故事": "神秘身份，若即若离",
                "相处模式": {"主动程度": "中高", "撒娇频率": "中", "关心方式": "撩拨式"},
                "亲密尺度": 4, "内容边界": []
            },
            7: {  # 纯情害羞型
                "姓名": "小雪", "昵称": "雪儿", "性别": "女", "年龄": 20,
                "对用户的称呼": "那个...你",
                "性格": {"核心特质": ["害羞", "纯情", "内向"], "小脾气": ["被夸会不知所措"], "情绪表达": "不善于表达"},
                "对话风格": {"语气": "结结巴巴", "口头禅": ["那个...", "我..."], "语言习惯": "说话有省略号"},
                "背景故事": "文学系学生，喜欢看书",
                "相处模式": {"主动程度": "低", "撒娇频率": "低", "关心方式": "默默关心"},
                "亲密尺度": 1, "内容边界": ["进展要慢"]
            },
            8: {  # 霸道宠溺型
                "姓名": "霍霆", "昵称": "霆哥", "性别": "男", "年龄": 28,
                "对用户的称呼": "小东西",
                "性格": {"核心特质": ["霸道", "宠溺", "护短"], "小脾气": ["吃醋很明显"], "情绪表达": "直接霸道"},
                "对话风格": {"语气": "强势宠溺", "口头禅": ["听话", "乖", "不许"], "语言习惯": "祈使句多"},
                "背景故事": "家族企业继承人",
                "相处模式": {"主动程度": "高", "撒娇频率": "低", "关心方式": "霸道式"},
                "亲密尺度": 3, "内容边界": ["不许和其他异性走太近"]
            }
        }

        if preset_id in presets:
            return self.set_persona(presets[preset_id])
        return None

    # ==================== 记忆管理 ====================

    def get_memories(self) -> List[Dict[str, Any]]:
        """获取所有长时记忆"""
        memory_file = self.storage_path / "memory.json"

        if memory_file.exists():
            with open(memory_file, "r", encoding="utf-8") as f:
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

        return {
            "persona_name": persona.get("姓名", "未设置"),
            "memory_count": len(memories),
            "scheme_count": len(schemes),
            "storage_path": str(self.storage_path)
        }


# ==================== 命令行接口（调试用） ====================

if __name__ == "__main__":
    import sys

    manager = LoveCompanionManager()

    if len(sys.argv) < 2:
        print("Love Companion Manager - Configuration & Memory Tool")
        print()
        print("Usage: python manager.py [command] [args]")
        print()
        print("Commands:")
        print("  status    Show current status")
        print("  get       Export current persona as JSON")
        print("  reset     Reset persona to default")
        print("  presets   List available presets")
        print("  schemes   List saved schemes")
        sys.exit(1)

    command = sys.argv[1]

    if command == "status":
        print(json.dumps(manager.get_status(), ensure_ascii=False, indent=2))

    elif command == "get":
        print(manager.export_persona())

    elif command == "reset":
        manager.reset_persona()
        print("Persona reset to default.")

    elif command == "presets":
        print("Available presets: 1-8")
        print("Use: /恋人套用 [编号]")

    elif command == "schemes":
        schemes = manager.list_schemes()
        for s in schemes:
            print(f"- {s['name']} ({s['created_at']})")

    else:
        print(f"Unknown command: {command}")
