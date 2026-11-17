#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
style_router.py — A/B风格制与风格对抗引擎

参考：概念解析文档中段 — A/B风格制 / 风格对抗
核心功能：
  - 对关键场景生成两个平行版本（A冷峻/B热烈）
  - 调用评论家代理对比两个版本
  - 输出融合建议
"""

import logging
import hashlib
from typing import Dict, List, Optional, Tuple

_log = logging.getLogger("style_router")

# 预设风格模板
STYLE_TEMPLATES = {
    "冷峻": {
        "description": "冷静、简洁、克制，用环境暗示情绪",
        "rules": ["句子不超过20字", "禁止使用感叹号", "情绪全部外化为动作"],
        "word_target": "短句为主，段落2-4句",
    },
    "热烈": {
        "description": "热烈、细腻、充满感官细节",
        "rules": ["加入1-2个感官细节(气味/触感/声音)", "情绪直接表达", "段落长短交错"],
        "word_target": "长短交替，段落4-6句",
    },
    "古龙": {
        "description": "极简、留白、机锋对话",
        "rules": ["每段不超过3句", "多用句号断句", "对话不用引号"],
        "word_target": "极短段落，1-2句",
    },
    "写实": {
        "description": "生活化、细节真实、语言自然",
        "rules": ["加入口语化表达", "避免戏剧化描写", "保留生活噪点"],
        "word_target": "自然节奏，不限",
    },
}

# 流派默认风格对
GENRE_DEFAULTS = {
    "玄幻": ("冷峻", "热烈"),
    "都市": ("写实", "热烈"),
    "悬疑": ("冷峻", "写实"),
    "言情": ("热烈", "写实"),
}


class StyleRouter:
    """A/B风格制路由引擎"""

    def __init__(self):
        self._version_log: List[Dict] = []

    def get_styles(self, genre: str = "") -> Tuple[str, str]:
        """根据题材获取推荐的 A/B 风格对"""
        if genre in GENRE_DEFAULTS:
            return GENRE_DEFAULTS[genre]
        return ("冷峻", "热烈")

    def get_style_prompt(self, style_name: str, scene_context: str = "") -> str:
        """获取指定风格的生成指令"""
        template = STYLE_TEMPLATES.get(style_name, STYLE_TEMPLATES["冷峻"])
        prompt = f"[风格: {style_name}] {template['description']}"
        prompt += f"\n风格规则: {'; '.join(template['rules'])}"
        prompt += f"\n字数要求: {template['word_target']}"
        if scene_context:
            prompt += f"\n场景: {scene_context}"
        return prompt

    def compare_versions(self, version_a: str, version_b: str) -> Dict:
        """对比两个版本，输出差异分析和融合建议"""
        analysis = {
            "word_count_a": len(version_a),
            "word_count_b": len(version_b),
            "diff_ratio": 0,
            "verdict": "",
        }
        # 简单对比
        common = set(version_a[:100]) & set(version_b[:100])
        total = max(len(set(version_a[:100]) | set(version_b[:100])), 1)
        analysis["diff_ratio"] = round(1 - len(common) / total, 2)

        if analysis["diff_ratio"] > 0.5:
            analysis["verdict"] = "两个版本差异显著，建议取A的前半+B的后半融合"
        elif analysis["diff_ratio"] > 0.3:
            analysis["verdict"] = "差异适中，可选取情感更强烈的版本"
        else:
            analysis["verdict"] = "差异不大，任选或微调即可"

        # 记录版本日志
        self._version_log.append({
            "a_len": len(version_a),
            "b_len": len(version_b),
            "diff": analysis["diff_ratio"],
            "verdict": analysis["verdict"],
        })
        return analysis

    def get_version_log(self) -> str:
        if not self._version_log:
            return ""
        lines = ["【A/B版本历史】"]
        for i, v in enumerate(self._version_log[-10:]):
            lines.append(f"  版本{i+1}: A={v['a_len']}字 B={v['b_len']}字 diff={v['diff']} {v['verdict']}")
        return "\n".join(lines)

    def available(self) -> bool:
        return True
