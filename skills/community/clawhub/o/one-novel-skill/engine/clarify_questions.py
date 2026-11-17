#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clarify_questions.py — 三层递进式问答系统

融合源: openclaw-novel-write 的 /novel clarify (5个关键问题)
       + chinese-novelist-skill 的三层递进式问答 (Layer 1-3 + 🎲随机/跳过)
功能: 
  - Layer 1: 5个核心必答问题
  - Layer 2: 5个深度可跳过问题
  - Layer 3: 标题生成（支持随机）
  - 每个问题支持🎲随机生成和"跳过"机制
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
from pathlib import Path
import random


# === Layer 1: 5个核心澄清问题 ===
CORE_QUESTIONS = [
    {
        "id": "genre",
        "question": "题材方向: 你想写什么类型的小说？",
        "type": "choice",
        "options": ["都市", "修仙", "玄幻", "悬疑", "言情", "科幻", "历史", "游戏", "🎲 随机"],
        "default": "都市",
        "why": "题材决定写作规则和平台适配",
    },
    {
        "id": "protagonist",
        "question": "主角设定: 主角是谁？有什么特点？",
        "type": "choice",
        "options": ["废柴逆袭型", "天才成长型", "重生型", "穿越型", "系统获得型", "🎲 随机"],
        "default": "废柴逆袭型",
        "why": "主角设定决定读者代入感的核心",
    },
    {
        "id": "core_conflict",
        "question": "核心冲突: 故事的主要矛盾是什么？",
        "type": "choice",
        "options": ["生存vs死亡", "查案vs真相", "复仇vs宽恕", "成长vs瓶颈",
                     "爱情vs身份", "权力vs良心", "守护vs牺牲", "🎲 随机"],
        "default": "生存vs死亡",
        "why": "冲突是故事引擎，说不清冲突的故事撑不长",
    },
    {
        "id": "narrative_scope",
        "question": "叙述视角: 用第三人称还是第一人称？",
        "type": "choice",
        "options": ["第三人称(他/她)", "第一人称(我)", "多视角切换", "🎲 随机"],
        "default": "第三人称(他/她)",
        "why": "视角直接影响读者代入感和信息呈现方式",
    },
    {
        "id": "emotional_core",
        "question": "核心情绪: 你想让读者主要感受什么情绪？",
        "type": "choice",
        "options": ["爽感释放", "甜宠甜蜜", "悬疑紧张", "热血燃",
                     "虐心催泪", "治愈温暖", "轻松搞笑", "🎲 随机"],
        "default": "爽感释放",
        "why": "每章场景都必须服务情绪目标",
    },
]

# === Layer 2: 5个深度定制问题（可跳过） ===
DEEP_QUESTIONS = [
    {
        "id": "world_detail",
        "question": "世界观深度: 你希望世界观有多详细？",
        "type": "choice",
        "options": ["核心设定就够了", "一般详细(势力+地理简图)", "非常详细(地理+政治+经济)"],
        "default": "一般详细",
        "skippable": True,
    },
    {
        "id": "chapter_target",
        "question": "目标字数: 每章预期多少字？",
        "type": "number",
        "default": 2500,
        "min": 1000,
        "max": 8000,
        "skippable": True,
    },
    {
        "id": "pacing_preference",
        "question": "节奏偏好: 开篇多快进入主线？",
        "type": "choice",
        "options": ["极快(500字内)", "快(前三章)", "中等(5-10章)", "慢热(10章+)", "🎲 随机"],
        "default": "快(前三章)",
        "skippable": True,
    },
    {
        "id": "hook_density",
        "question": "钩子密度: 每章留多少个悬念？",
        "type": "choice",
        "options": ["一个章末钩子", "章内1-2+章末1", "密集钩子(每段都有)"],
        "default": "一个章末钩子",
        "skippable": True,
    },
    {
        "id": "side_characters",
        "question": "配角体系: 多复杂？",
        "type": "choice",
        "options": ["精简1-2个", "中等3-5个", "丰富(多势力)"],
        "default": "中等3-5个",
        "skippable": True,
    },
]

# === Layer 3: 标题库 ===
TITLE_TEMPLATES = {
    "爽感释放": [
        "{}：{}逆天改命",
        "开局{}，{}",
        "{}：我有{}我怕谁",
        "{}从{}开始",
        "我的{}是{}！",
        "{}：{}归来",
        "{}：开局就{}",
    ],
    "甜宠甜蜜": [
        "{}后，{}",
        "{}的{}，{}",
        "{}：{}别想逃",
        "{}一下，{}了",
        "嫁给{}后，{}",
    ],
    "悬疑紧张": [
        "{}谜案：{}",
        "第{}个{}",
        "{}：所有人都{}",
        "{}的{}",
    ],
    "热血燃": [
        "{}：{}",
        "{}：从{}开始{}",
        "{}的{}要{}！",
    ],
}

DEFAULT_TITLE_TEMPLATES = [
    "{}",
    "{}：{}",
    "{}之{}",
    "{}，{}",
]


# === 问答结果 ===

@dataclass
class ClarifyAnswers:
    """澄清问答结果"""
    answers: Dict[str, str] = field(default_factory=dict)
    deep_answers: Dict[str, str] = field(default_factory=dict)
    title: str = ""
    all_random: bool = False   # 是否全部🎲随机

    def get(self, qid: str, default: str = "") -> str:
        return self.answers.get(qid, self.deep_answers.get(qid, default))

    def to_dict(self) -> dict:
        return {
            "core": dict(self.answers),
            "deep": dict(self.deep_answers),
            "title": self.title,
            "emotional_core": self.answers.get("emotional_core", "爽感释放"),
        }

    def get_prompt_block(self) -> str:
        """生成写入prompt的决策块"""
        lines = ["[创作决策]"]
        for q in CORE_QUESTIONS:
            val = self.answers.get(q["id"])
            if val:
                lines.append(f"  {q['id']}: {val}")
        for q in DEEP_QUESTIONS:
            val = self.deep_answers.get(q["id"])
            if val:
                lines.append(f"  {q['id']}: {val}")
        if self.title:
            lines.append(f"  书名: {self.title}")
        return "\n".join(lines)

    def save(self, path: Path) -> bool:
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            md_lines = ["# 创作决策澄清（三层递进问答）", ""]
            if self.all_random:
                md_lines.append("> 全部采用🎲随机生成\n")
            md_lines.append("## Layer 1: 核心定位\n")
            for q in CORE_QUESTIONS:
                val = self.answers.get(q["id"])
                if val:
                    md_lines.append(f"- **{q['question']}**: {val}")
            md_lines.extend(["", "## Layer 2: 深度定制\n"])
            for q in DEEP_QUESTIONS:
                val = self.deep_answers.get(q["id"])
                if val:
                    md_lines.append(f"- **{q['question']}**: {val}")
            if self.title:
                md_lines.extend(["", f"## 选定书名\n\n{self.title}"])
            path.write_text("\n".join(md_lines), encoding="utf-8")
            
            import json
            json_path = path.with_suffix(".json")
            json_path.write_text(
                json.dumps(self.to_dict(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            return True
        except OSError:
            return False


# === 辅助函数 ===

def get_random_answer(q: dict) -> str:
    """🎲随机生成回答"""
    opts = q.get("options", [])
    # 过滤掉"🎲 随机"选项本身
    clean = [o for o in opts if "随机" not in o]
    if q.get("type") == "number":
        return str(random.randint(q.get("min", 1000), q.get("max", 8000)))
    return random.choice(clean) if clean else opts[0] if opts else ""


def generate_title_suggestions(genre: str, emotion: str, protagonist: str = "",
                                setting: str = "", count: int = 5) -> List[str]:
    """生成候选标题"""
    suggestions = []
    templates = TITLE_TEMPLATES.get(emotion, DEFAULT_TITLE_TEMPLATES)
    fill_values = [protagonist or "主角", setting or "世界", genre or "幻想", emotion or "燃"]
    
    for _ in range(count * 2):
        tpl = random.choice(templates)
        try:
            slot_count = tpl.count("{}")
            if slot_count <= len(fill_values):
                filled = tpl.format(*fill_values[:slot_count])
                suggestions.append(filled)
        except (IndexError, ValueError):
            continue
    return list(dict.fromkeys(suggestions))[:count]


def get_answer_summary(answers: ClarifyAnswers) -> str:
    """生成决策摘要（嵌入prompt）"""
    lines = ["[创作决策]"]
    lines.append(f"情绪目标: {answers.get('emotional_core', '爽感释放')}")
    lines.append(f"叙述视角: {answers.get('narrative_scope', '第三人称')}")
    lines.append(f"题材: {answers.get('genre', '都市')}")
    if answers.title:
        lines.append(f"书名: {answers.title}")
    if answers.all_random:
        lines.append("模式: 全部随机")
    return "\n".join(lines)
