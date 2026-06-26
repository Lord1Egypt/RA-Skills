# -*- coding: utf-8 -*-
"""
预设管理器
管理播客风格预设，提供快捷配置组合
"""

import json
from typing import Dict, Any, List, Optional
from pathlib import Path


class PresetManager:
    """
    预设管理器

    提供【风格对标】快捷模板，将知名播客/访谈节目的风格
    映射为完整的 Persona + Style + 动态模式 配置组合
    """

    _instance = None
    _presets_cache: Dict[str, Dict[str, Any]] = {}

    def __new__(cls):
        """单例模式，避免重复加载"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_all_presets()
        return cls._instance

    def __init__(self):
        """初始化（实际加载在 __new__ 中完成）"""
        self.presets_dir = Path(__file__).parent.parent / "config" / "presets"

    def _load_all_presets(self):
        """加载所有预设文件到缓存"""
        self.presets_dir = Path(__file__).parent.parent / "config" / "presets"

        if not self.presets_dir.exists():
            print(f"[PresetManager] 预设目录不存在: {self.presets_dir}")
            return

        for preset_file in sorted(self.presets_dir.glob("*.json")):
            try:
                with open(preset_file, "r", encoding="utf-8") as f:
                    preset = json.load(f)
                    preset_name = preset.get("preset_name", preset_file.stem)
                    self._presets_cache[preset_name] = preset
            except Exception as e:
                print(f"[PresetManager] 加载预设失败 {preset_file}: {e}")

    def list_presets(self, tag: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        列出所有可用预设

        Args:
            tag: 按标签筛选（可选）

        Returns:
            预设信息列表，每项包含 name, description, tags, sample_topics
        """
        results = []
        for name, preset in self._presets_cache.items():
            if tag and tag not in preset.get("tags", []):
                continue

            results.append({
                "name": name,
                "description": preset.get("description", ""),
                "tags": preset.get("tags", []),
                "sample_topics": preset.get("sample_topics", []),
                "style": preset.get("style", "深度对谈")
            })

        return results

    def get_preset(self, name: str) -> Optional[Dict[str, Any]]:
        """
        获取指定预设的完整配置

        Args:
            name: 预设名称（如"鲁豫有约-鲁豫"）

        Returns:
            完整预设配置，包含 host_a, host_b, style 等
        """
        # 尝试精确匹配
        if name in self._presets_cache:
            return self._presets_cache[name]

        # 尝试模糊匹配（去掉空格、大小写）
        name_normalized = name.replace(" ", "").replace("-", "").lower()
        for preset_name, preset in self._presets_cache.items():
            preset_normalized = preset_name.replace(" ", "").replace("-", "").lower()
            if name_normalized == preset_normalized:
                return preset
            # 尝试匹配部分名称
            if name_normalized in preset_normalized or preset_normalized in name_normalized:
                return preset

        return None

    def apply_preset(self, name: str) -> Dict[str, Any]:
        """
        应用预设，返回可直接用于 pipeline 的配置

        Args:
            name: 预设名称

        Returns:
            包含 persona_config, style, dynamic_pattern 的字典

        Raises:
            ValueError: 预设不存在时抛出
        """
        preset = self.get_preset(name)
        if not preset:
            available = list(self._presets_cache.keys())
            raise ValueError(f"预设 '{name}' 不存在。可用预设: {available}")

        # 构建 persona_config
        persona_config = {
            "host_a": self._extract_host_persona(preset["host_a"]),
            "host_b": self._extract_host_persona(preset["host_b"])
        }

        return {
            "preset_name": preset["preset_name"],
            "persona_config": persona_config,
            "style": preset.get("style", "深度对谈"),
            "dynamic_pattern": preset.get("dynamic_pattern", {}),
            "style_reasoning": preset.get("style_reasoning", "")
        }

    def _extract_host_persona(self, host_data: Dict[str, Any]) -> Dict[str, Any]:
        """从预设数据中提取标准 persona 结构"""
        return {
            "identity": {
                "name": host_data.get("name", ""),
                "archetype": host_data.get("archetype", "观察者"),
                "core_drive": host_data.get("core_drive", ""),
                "chemistry": host_data.get("chemistry", "")
            },
            "expression": {
                "pace": host_data.get("pace", "normal"),
                "sentence_length": host_data.get("sentence_length", "mixed"),
                "signature_phrases": host_data.get("signature_phrases", []),
                "attitude": host_data.get("attitude", "curious"),
                "voice_id": host_data.get("voice_id", "")
            },
            "memory_seed": []
        }

    def get_preset_summary(self, name: str) -> str:
        """
        获取预设的可读摘要

        Args:
            name: 预设名称

        Returns:
            格式化的摘要文本
        """
        preset = self.get_preset(name)
        if not preset:
            return f"预设 '{name}' 不存在"

        lines = []
        lines.append(f"🎭 {preset['preset_name']}")
        lines.append(f"   {preset.get('description', '')}")
        lines.append("")

        host_a = preset["host_a"]
        host_b = preset["host_b"]

        lines.append(f"👤 主持人A ({host_a['name']}): {host_a['archetype']}")
        lines.append(f"   风格: {host_a['attitude']} | 语速: {host_a['pace']}")
        lines.append(f"   口头禅: {', '.join(host_a['signature_phrases'][:2])}")
        lines.append("")

        lines.append(f"👤 主持人B ({host_b['name']}): {host_b['archetype']}")
        lines.append(f"   风格: {host_b['attitude']} | 语速: {host_b['pace']}")
        lines.append(f"   口头禅: {', '.join(host_b['signature_phrases'][:2])}")
        lines.append("")

        lines.append(f"📻 对话风格: {preset.get('style', '深度对谈')}")
        lines.append(f"🏷️ 标签: {', '.join(preset.get('tags', []))}")

        return "\n".join(lines)

    def print_preset_menu(self):
        """打印预设选择菜单"""
        print("=" * 60)
        print("🎙️ 选择你的播客风格")
        print("=" * 60)
        print()

        presets = self.list_presets()

        for i, preset in enumerate(presets, 1):
            name = preset["name"]
            desc = preset["description"]
            style = preset["style"]

            # 截断描述
            if len(desc) > 40:
                desc = desc[:37] + "..."

            print(f"  {i}. {name}")
            print(f"     {desc} [{style}]")
            print()

        print("  0. 自定义配置")
        print()


def get_preset_names() -> List[str]:
    """便捷函数：获取所有预设名称"""
    manager = PresetManager()
    presets = manager.list_presets()
    return [p["name"] for p in presets]


def apply_preset(name: str) -> Dict[str, Any]:
    """便捷函数：应用指定预设"""
    manager = PresetManager()
    return manager.apply_preset(name)


def print_preset_list():
    """便捷函数：打印预设列表"""
    manager = PresetManager()
    manager.print_preset_menu()
