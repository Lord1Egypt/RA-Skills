# -*- coding: utf-8 -*-
"""
Persona管理器
处理Persona的保存、加载、确认流程
"""

import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime


class PersonaManager:
    """Persona管理器 - 支持多persona存储"""

    def __init__(self, user_id: str, persona_name: str = "default"):
        self.user_id = user_id
        self.persona_name = persona_name
        self.config_dir = Path(__file__).parent.parent / "config" / "user_personas" / user_id
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.persona_file = self.config_dir / f"{persona_name}.json"

    def exists(self) -> bool:
        """检查用户是否已有Persona"""
        return self.persona_file.exists()

    def save(self, persona: Dict[str, Any]) -> bool:
        """
        保存Persona

        Args:
            persona: 三层Persona字典

        Returns:
            是否保存成功
        """
        try:
            # 添加元数据
            persona_with_meta = {
                "_meta": {
                    "user_id": self.user_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "version": "1.0"
                },
                "persona": persona
            }

            with open(self.persona_file, "w", encoding="utf-8") as f:
                json.dump(persona_with_meta, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print(f"保存Persona失败: {e}")
            return False

    def load(self) -> Optional[Dict[str, Any]]:
        """
        加载Persona

        Returns:
            Persona字典或None
        """
        if not self.exists():
            return None

        try:
            with open(self.persona_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 兼容有_meta和没有_meta的情况
            if "persona" in data:
                return data["persona"]
            else:
                return data

        except Exception as e:
            print(f"加载Persona失败: {e}")
            return None

    def update(self, persona: Dict[str, Any]) -> bool:
        """更新Persona（保留元数据）"""
        if not self.exists():
            return self.save(persona)

        try:
            with open(self.persona_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            data["persona"] = persona
            data["_meta"]["updated_at"] = datetime.now().isoformat()

            with open(self.persona_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print(f"更新Persona失败: {e}")
            return False

    def delete(self) -> bool:
        """删除Persona"""
        if self.exists():
            try:
                self.persona_file.unlink()
                return True
            except Exception as e:
                print(f"删除Persona失败: {e}")
                return False
        return True

    @classmethod
    def list_personas(cls, user_id: str) -> List[Dict[str, Any]]:
        """
        列出用户的所有Persona

        Returns:
            List[{"name": str, "updated_at": str, "archetype": str, "has_memory": bool}]
        """
        config_dir = Path(__file__).parent.parent / "config" / "user_personas" / user_id
        if not config_dir.exists():
            return []

        personas = []
        for json_file in sorted(config_dir.glob("*.json")):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                meta = data.get("_meta", {})
                persona = data.get("persona", {})
                identity = persona.get("identity", {})
                memory_seed = persona.get("memory_seed", [])

                personas.append({
                    "name": json_file.stem,
                    "updated_at": meta.get("updated_at", ""),
                    "archetype": identity.get("archetype", "未知"),
                    "display_name": identity.get("name") or json_file.stem,
                    "has_memory": len(memory_seed) > 0
                })
            except Exception:
                continue

        # 按更新时间倒序
        personas.sort(key=lambda x: x["updated_at"], reverse=True)
        return personas

    @classmethod
    def load_by_name(cls, user_id: str, persona_name: str) -> Optional[Dict[str, Any]]:
        """通过名称加载特定persona"""
        manager = cls(user_id, persona_name)
        return manager.load()

    @classmethod
    def switch_active(cls, user_id: str, persona_name: str) -> bool:
        """
        切换当前激活的persona
        将指定persona复制为default.json
        """
        source = Path(__file__).parent.parent / "config" / "user_personas" / user_id / f"{persona_name}.json"
        target = Path(__file__).parent.parent / "config" / "user_personas" / user_id / "default.json"

        if not source.exists():
            return False

        try:
            import shutil
            shutil.copy2(source, target)
            return True
        except Exception as e:
            print(f"切换persona失败: {e}")
            return False

    @staticmethod
    def format_for_display(persona: Dict[str, Any]) -> str:
        """
        格式化Persona为人类可读文本

        Args:
            persona: Persona字典

        Returns:
            可展示的文本
        """
        identity = persona.get("identity", {})
        expression = persona.get("expression", {})
        memory_seed = persona.get("memory_seed", [])

        lines = []
        lines.append("=" * 50)
        lines.append("📋 你的Persona档案")
        lines.append("=" * 50)

        # Identity
        lines.append("\n🎭 基础人格")
        lines.append(f"  名称: {identity.get('name') or '(未命名)'}" )
        lines.append(f"  原型: {identity.get('archetype', '观察者')}")
        lines.append(f"  核心驱动力: {identity.get('core_drive') or '(未设置)'}")
        lines.append(f"  互动方式: {identity.get('chemistry') or '(未设置)'}")

        # Expression
        lines.append("\n🗣️ 表达风格")
        lines.append(f"  语速: {expression.get('pace', 'normal')}")
        lines.append(f"  句长: {expression.get('sentence_length', 'mixed')}")

        phrases = expression.get("signature_phrases", [])
        if phrases:
            lines.append(f"  口头禅: {', '.join(phrases)}")
        else:
            lines.append("  口头禅: (未提取)")

        lines.append(f"  态度: {expression.get('attitude', 'curious')}")

        # Memory
        lines.append(f"\n💭 记忆种子 ({len(memory_seed)}条)")
        for i, mem in enumerate(memory_seed[:5], 1):  # 最多显示5条
            if isinstance(mem, dict):
                title = mem.get("title", f"记忆{i}")
                content = mem.get("content", "")[:50]  # 截断
                lines.append(f"  {i}. {title}: {content}...")

        if len(memory_seed) > 5:
            lines.append(f"  ... 还有 {len(memory_seed) - 5} 条")

        lines.append("\n" + "=" * 50)

        return "\n".join(lines)

    @staticmethod
    def quick_adjust(persona: Dict[str, Any], adjustments: Dict[str, Any]) -> Dict[str, Any]:
        """
        快速调整Persona

        Args:
            persona: 原Persona
            adjustments: 调整项

        Returns:
            调整后的Persona
        """
        # 调整identity
        if "identity" in adjustments:
            persona["identity"].update(adjustments["identity"])

        # 调整expression
        if "expression" in adjustments:
            persona["expression"].update(adjustments["expression"])

        # 调整signature_phrases（追加或替换）
        if "add_phrases" in adjustments:
            persona["expression"]["signature_phrases"].extend(adjustments["add_phrases"])
            # 去重并限制3个
            unique = list(dict.fromkeys(persona["expression"]["signature_phrases"]))
            persona["expression"]["signature_phrases"] = unique[:3]

        # 调整memory（追加）
        if "add_memory" in adjustments:
            persona["memory_seed"].append(adjustments["add_memory"])

        return persona


class DoublePersonaManager:
    """双主持人Persona管理 - 支持host固定 + guest可变"""

    def __init__(self, user_id: str, session_guest: Optional[str] = None):
        """
        Args:
            user_id: 用户ID
            session_guest: 本期嘉宾persona名称（可选，临时指定）
        """
        self.user_id = user_id
        self.session_guest = session_guest
        self.config_dir = Path(__file__).parent.parent / "config" / "user_personas" / user_id
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.double_file = self.config_dir / "_double_config.json"

    def save(self, host_a: Dict[str, Any], host_b: Dict[str, Any], host_a_name: str = "me", host_b_name: str = "partner") -> bool:
        """
        保存双Persona配置

        Args:
            host_a: 主持人A（通常是用户的persona）
            host_b: 主持人B（嘉宾persona）
            host_a_name: 主持人A的persona名称
            host_b_name: 主持人B的persona名称
        """
        try:
            data = {
                "_meta": {
                    "user_id": self.user_id,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "version": "2.0"
                },
                "host_a": {
                    "persona_name": host_a_name,
                    "persona": host_a
                },
                "host_b": {
                    "persona_name": host_b_name,
                    "persona": host_b,
                    "is_variable": True  # 标记嘉宾是否可变
                }
            }

            with open(self.double_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print(f"保存双Persona失败: {e}")
            return False

    def load(self) -> Optional[tuple]:
        """
        加载双Persona
        如果指定了session_guest，会用该guest替换默认host_b

        Returns:
            (host_a_persona, host_b_persona) 或 None
        """
        if not self.double_file.exists():
            return None

        try:
            with open(self.double_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            host_a = data.get("host_a", {}).get("persona")
            host_b_data = data.get("host_b", {})

            # 如果有临时嘉宾，加载临时嘉宾的persona
            if self.session_guest:
                guest_persona = PersonaManager.load_by_name(self.user_id, self.session_guest)
                if guest_persona:
                    host_b = guest_persona
                else:
                    host_b = host_b_data.get("persona")
            else:
                host_b = host_b_data.get("persona")

            return (host_a, host_b)

        except Exception as e:
            print(f"加载双Persona失败: {e}")
            return None

    def exists(self) -> bool:
        """检查是否存在双Persona配置"""
        return self.double_file.exists()

    def get_host_a_name(self) -> Optional[str]:
        """获取主持人A的persona名称"""
        if not self.double_file.exists():
            return None
        try:
            with open(self.double_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("host_a", {}).get("persona_name")
        except Exception:
            return None


# 便捷函数
def get_persona_manager(user_id: str, persona_name: str = "default") -> PersonaManager:
    """获取Persona管理器实例"""
    return PersonaManager(user_id, persona_name)


def check_first_time(user_id: str) -> bool:
    """检查是否首次使用（该用户没有任何Persona）"""
    config_dir = Path(__file__).parent.parent / "config" / "user_personas" / user_id
    if not config_dir.exists():
        return True
    # 检查是否有任何persona文件
    json_files = list(config_dir.glob("*.json"))
    return len(json_files) == 0


def list_user_personas(user_id: str) -> List[Dict[str, Any]]:
    """便捷函数：列出用户的所有persona"""
    return PersonaManager.list_personas(user_id)


def delete_persona(user_id: str, persona_name: str) -> bool:
    """便捷函数：删除指定persona"""
    manager = PersonaManager(user_id, persona_name)
    return manager.delete()
