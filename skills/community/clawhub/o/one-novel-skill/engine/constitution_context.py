#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
constitution_context.py — 创作宪法/风格设置

融合源: openclaw-novel-write 的 /novel constitution 七步方法论
功能: 
  1. 定义写作风格预设（自然人声/网文爽文/文学质感/古风典雅/极简白描）
  2. 生成 style profile 作为宪法基础
  3. 为生成器提供风格上下文 embedding prompt
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
import json
from pathlib import Path


# === 风格预设 ===
STYLE_PRESETS = {
    "自然人声": {
        "description": "真实感优先，口语化强，句短，情绪密度高",
        "p0_rules": ["禁用'感到/觉得/认为/知道'引出情绪", "章末不能总结而是要制造新问题"],
        "p1_rules": ["句长18-48字混合", "每200字至少1句对话", "短句占比>40%"],
        "tone": "口语化, 第一人称视角, 动作展示情绪",
        "dialog_style": "动作替代标签, 声线差异大, 允许方言语气词",
        "platform_affinity": ["番茄", "七猫"],
    },
    "网文爽文": {
        "description": "快节奏, 爽点密集, 每章有钩子, 节奏明快",
        "p0_rules": ["禁用感悟式结尾", "每200字内必须有推进", "禁止连续2章无爽点"],
        "p1_rules": ["每500字设1个未解答疑问", "每3-5章中小高潮", "每8-12章大高潮"],
        "tone": "第三人称为主, 节奏紧凑, 打脸装逼循环递进",
        "dialog_style": "简洁有力, 角色声线鲜明",
        "platform_affinity": ["飞卢", "番茄", "起点"],
    },
    "文学质感": {
        "description": "文笔精炼, 注重意境和象征, 慢热但有深度",
        "p0_rules": ["禁用陈词滥调", "禁止信息灌水", "每个词有功能"],
        "p1_rules": ["段落字数方差>8", "感官描写至少3种", "比喻需原创"],
        "tone": "谨慎用词, 留白多, 情绪克制",
        "dialog_style": "含蓄, 潜台词丰富, 话里有话",
        "platform_affinity": ["起点", "豆瓣阅读"],
    },
    "古风典雅": {
        "description": "古风语言, 工整对仗, 诗词典故穿插",
        "p0_rules": ["禁止现代口语穿越", "古风用词必须考究"],
        "p1_rules": ["适当骈文结构", "引用需符合时代背景"],
        "tone": "用典多, 意象丰富, 节奏舒缓",
        "dialog_style": "注重称谓和礼节",
        "platform_affinity": ["起点", "晋江"],
    },
    "极简白描": {
        "description": "少修饰, 少形容词, 全靠对话和动作推进",
        "p0_rules": ["禁止过度修饰", "每个副词必须问'有必要吗'"],
        "p1_rules": ["动词精准优先", "描述不超过读者需要知道的"],
        "tone": "克制, 冷静, 留给读者想象空间",
        "dialog_style": "极简, 话少信息量大",
        "platform_affinity": ["起点", "知乎盐选"],
    },
}


@dataclass
class Constitution:
    """创作宪法 — 写作风格与规则契约"""
    name: str
    style_preset: str          # 预设名称
    custom_notes: str = ""     # 自定义补充
    p0_rules: List[str] = field(default_factory=list)
    p1_rules: List[str] = field(default_factory=list)
    tone_description: str = ""
    dialog_style: str = ""
    platform_affinity: List[str] = field(default_factory=list)
    created_at: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "style_preset": self.style_preset,
            "custom_notes": self.custom_notes,
            "p0_rules": self.p0_rules,
            "p1_rules": self.p1_rules,
            "tone_description": self.tone_description,
            "dialog_style": self.dialog_style,
            "platform_affinity": self.platform_affinity,
            "created_at": self.created_at,
        }

    @classmethod
    def from_preset(cls, name: str, style: str, custom_notes: str = "", 
                    override_rules: Optional[Dict[str, List[str]]] = None) -> "Constitution":
        preset = STYLE_PRESETS.get(style, STYLE_PRESETS["网文爽文"])
        p0 = list(preset.get("p0_rules", []))
        p1 = list(preset.get("p1_rules", []))
        if override_rules:
            if "p0" in override_rules:
                p0.extend(override_rules["p0"])
            if "p1" in override_rules:
                p1.extend(override_rules["p1"])
        from datetime import datetime
        return cls(
            name=name,
            style_preset=style,
            custom_notes=custom_notes,
            p0_rules=p0,
            p1_rules=p1,
            tone_description=preset.get("tone", ""),
            dialog_style=preset.get("dialog_style", ""),
            platform_affinity=list(preset.get("platform_affinity", [])),
            created_at=datetime.now().isoformat(),
        )


class ConstitutionManager:
    """宪法管理器 — 加载/保存/应用创作宪法"""

    def __init__(self, book_dir: Path):
        self.book_dir = Path(book_dir)
        self._constitution: Optional[Constitution] = None

    def get_path(self) -> Path:
        return self.book_dir / "设定" / "创作宪法.md"

    def exists(self) -> bool:
        return self.get_path().exists()

    def load(self) -> Optional[Constitution]:
        path = self.get_path()
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return Constitution(**data)
        except (json.JSONDecodeError, TypeError, KeyError):
            return None

    def save(self, constitution: Constitution) -> bool:
        path = self.get_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            path.write_text(json.dumps(constitution.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
            self._constitution = constitution
            return True
        except OSError:
            return False

    def get_prompt_block(self) -> str:
        """返回嵌入到生成prompt中的宪法约束块"""
        c = self._constitution or self.load()
        if not c:
            return ""
        lines = ["[创作宪法]"]
        lines.append(f"风格: {c.style_preset}")
        if c.tone_description:
            lines.append(f"语调: {c.tone_description}")
        if c.dialog_style:
            lines.append(f"对话: {c.dialog_style}")
        if c.p0_rules:
            lines.append("P0必须遵守:")
            for r in c.p0_rules:
                lines.append(f"  - {r}")
        if c.p1_rules:
            lines.append("P1建议遵守:")
            for r in c.p1_rules:
                lines.append(f"  - {r}")
        if c.custom_notes:
            lines.append(f"自定义: {c.custom_notes}")
        return "\n".join(lines)

    def list_presets(self) -> Dict[str, str]:
        return {k: v["description"] for k, v in STYLE_PRESETS.items()}
