#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
short_story_mode.py — 短故事模式引擎

SKILL.md 声明功能：
- 用户请求短故事时自动切换，不走长篇流程
- SS0 平台识别与选题：目标平台、类型、字数、核心反转确认
- SS1 人物与大纲：主角锚点>=2，三至五幕结构
- SS2 正文生成与平台适配：生成→检测→平台格式校验→定稿
- 字数体系：微小说500-1000/超短篇1000-3000/标准短篇6000-15000/知乎盐选8000-30000
- 红线：开篇200字未进核心冲突→重写开头；中段无情绪推进→插入爆点；结尾无反转或情绪落点→重写结尾
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple

_log = logging.getLogger("short_story_mode")


class ShortStoryModeEngine:
    """短故事模式引擎 — 三阶段自动化流程"""

    # === 字数体系 ===
    WORD_SYSTEMS = {
        "微小说": {
            "range": (500, 1000),
            "platforms": ["小红书", "头条"],
            "structure": "三幕短结构",
            "max_characters": 3,
            "rule": "50字内必须出现冲突，每句双重功能",
        },
        "超短篇": {
            "range": (1000, 3000),
            "platforms": ["小红书", "知乎"],
            "structure": "五段式",
            "max_characters": 5,
            "rule": "前200字冲突，单主线",
        },
        "标准短篇": {
            "range": (6000, 15000),
            "platforms": ["番茄", "七猫"],
            "structure": "五幕结构",
            "max_characters": 8,
            "rule": "三至五幕，核心反转在60%-75%位置",
        },
        "知乎盐选": {
            "range": (8000, 30000),
            "platforms": ["知乎"],
            "structure": "七段式",
            "max_characters": 10,
            "rule": "开篇前500字必须有强冲突，分节标题有吸引力",
        },
    }

    # === 平台选题参数 ===
    PLATFORM_PROFILES = {
        "小红书": {
            "tone": "亲切/分享感/口语化",
            "structure": "hook→展开→反转→总结",
            "word_style": "短句/分段多/emoji可选",
            "forbidden": ["官腔", "论文腔", "长篇大论"],
        },
        "头条": {
            "tone": "资讯感/观点明确/引发讨论",
            "structure": "标题钩子→事件→分析→观点",
            "word_style": "中等段落/逻辑清晰",
            "forbidden": ["模棱两可", "没有观点"],
        },
        "知乎": {
            "tone": "专业感/亲历者视角/有理有据",
            "structure": "开场钩子→故事展开→观点提炼→互动引导",
            "word_style": "长段可接受/逻辑严密/引用加分",
            "forbidden": ["空洞抒情", "无实质内容"],
        },
        "番茄": {
            "tone": "快节奏/爽感/网文化",
            "structure": "冲突→升级→反转→高潮→余韵",
            "word_style": "短段/对话多/章末钩子",
            "forbidden": ["慢热铺垫", "大段描写"],
        },
        "七猫": {
            "tone": "情感导向/温暖/治愈或虐心",
            "structure": "相遇→发展→冲突→和解/分离→余韵",
            "word_style": "情感描写细腻/对话有温度",
            "forbidden": ["冷血无情", "无情感线"],
        },
    }

    # === 故事结构模板 ===
    STRUCTURE_TEMPLATES = {
        "三幕短结构": [
            {"act": 1, "name": "建立", "ratio": (0.00, 0.25), "goal": "建立角色+冲突，读者在50字内知道核心矛盾"},
            {"act": 2, "name": "发展", "ratio": (0.25, 0.70), "goal": "冲突升级，展示角色应对，有至少1次情绪波动"},
            {"act": 3, "name": "反转", "ratio": (0.70, 1.00), "goal": "反转或情绪落点，读者有意料之外的感觉"},
        ],
        "五段式": [
            {"act": 1, "name": "开场", "ratio": (0.00, 0.10), "goal": "200字内冲突入场"},
            {"act": 2, "name": "展开", "ratio": (0.10, 0.35), "goal": "发展矛盾，引入次要角色"},
            {"act": 3, "name": "转折", "ratio": (0.35, 0.60), "goal": "第一次转折，改变局势"},
            {"act": 4, "name": "高潮", "ratio": (0.60, 0.85), "goal": "核心冲突爆发"},
            {"act": 5, "name": "结尾", "ratio": (0.85, 1.00), "goal": "反转或情绪落点"},
        ],
        "五幕结构": [
            {"act": 1, "name": "开端", "ratio": (0.00, 0.15), "goal": "建立世界+核心冲突"},
            {"act": 2, "name": "上升", "ratio": (0.15, 0.40), "goal": "冲突升级+第一次小高潮"},
            {"act": 3, "name": "中点", "ratio": (0.40, 0.60), "goal": "转折点/伪胜利或伪失败"},
            {"act": 4, "name": "下降", "ratio": (0.60, 0.85), "goal": "高潮前积累+终极冲突"},
            {"act": 5, "name": "结局", "ratio": (0.85, 1.00), "goal": "反转+余韵"},
        ],
        "七段式": [
            {"act": 1, "name": "开场钩子", "ratio": (0.00, 0.08), "goal": "500字内强冲突"},
            {"act": 2, "name": "背景铺垫", "ratio": (0.08, 0.25), "goal": "适度展开世界/角色"},
            {"act": 3, "name": "第一次转折", "ratio": (0.25, 0.40), "goal": "意料之外的展开"},
            {"act": 4, "name": "深度发展", "ratio": (0.40, 0.60), "goal": "情感深化+第二次冲突"},
            {"act": 5, "name": "第二次转折", "ratio": (0.60, 0.75), "goal": "核心反转"},
            {"act": 6, "name": "高潮", "ratio": (0.75, 0.90), "goal": "终极冲突/揭示"},
            {"act": 7, "name": "余韵", "ratio": (0.90, 1.00), "goal": "反转+情绪落点+思考空间"},
        ],
    }

    def __init__(self):
        pass

    # ====== SS0: 平台识别与选题 ======

    def identify_platform(self, word_count: int, target_platform: str = "") -> Dict[str, Any]:
        """SS0: 识别目标平台和故事类型"""
        # 确定故事类型
        story_type = self._classify_story_type(word_count)

        # 确定平台
        platform = target_platform if target_platform else story_type["platforms"][0]

        # 获取平台参数
        platform_profile = self.PLATFORM_PROFILES.get(platform, self.PLATFORM_PROFILES["番茄"])

        return {
            "phase": "SS0",
            "story_type": story_type["name"],
            "word_range": f"{story_type['range'][0]}-{story_type['range'][1]}字",
            "actual_words": word_count,
            "target_platform": platform,
            "platform_profile": platform_profile,
            "structure": story_type["structure"],
            "max_characters": story_type["max_characters"],
            "core_rule": story_type["rule"],
        }

    def generate_topic_prompt(self, platform: str, word_count: int) -> str:
        """SS0: 生成选题引导提示"""
        ss0 = self.identify_platform(word_count, platform)
        return "\n".join([
            f"【SS0 平台识别与选题】",
            f"故事类型: {ss0['story_type']}",
            f"字数范围: {ss0['word_range']}",
            f"目标平台: {ss0['target_platform']}",
            f"平台风格: {ss0['platform_profile']['tone']}",
            f"核心规则: {ss0['core_rule']}",
            f"最多角色数: {ss0['max_characters']}",
            f"",
            f"请确认以下要素：",
            f"1. 核心冲突/反转是什么？",
            f"2. 主角的核心特征（至少2个锚点：身份+性格）",
            f"3. 结局的情感落点（让读者有什么感觉？）",
        ])

    # ====== SS1: 人物与大纲 ======

    def validate_character_anchors(self, character: Dict) -> Dict[str, Any]:
        """SS1: 验证角色是否有至少2个锚点"""
        anchors = []
        if character.get("identity"):
            anchors.append(f"身份: {character['identity']}")
        if character.get("personality"):
            anchors.append(f"性格: {character['personality']}")
        if character.get("goal"):
            anchors.append(f"目标: {character['goal']}")
        if character.get("flaw"):
            anchors.append(f"缺陷: {character['flaw']}")

        return {
            "name": character.get("name", "?"),
            "anchor_count": len(anchors),
            "anchors": anchors,
            "passed": len(anchors) >= 2,
            "issue": None if len(anchors) >= 2 else "角色锚点不足2个，请补充身份/性格/目标/缺陷中至少2项",
        }

    def get_structure_template(self, structure_name: str) -> List[Dict]:
        """SS1: 获取故事结构模板"""
        return self.STRUCTURE_TEMPLATES.get(structure_name, self.STRUCTURE_TEMPLATES["五段式"])

    def generate_outline_prompt(self, word_count: int, platform: str, core_reversal: str = "",
                                character_count: int = 3) -> str:
        """SS1: 生成大纲规划引导提示"""
        ss0 = self.identify_platform(word_count, platform)
        structure = self.get_structure_template(ss0["structure"])

        lines = [f"【SS1 人物与大纲】"]
        lines.append(f"结构类型: {ss0['structure']}")
        lines.append(f"目标字数: {word_count}字")
        lines.append(f"角色数限制: ≤{ss0['max_characters']}个")
        if core_reversal:
            lines.append(f"核心反转: {core_reversal}")
        lines.append("")
        lines.append("故事结构：")

        for act in structure:
            start_pct = int(act["ratio"][0] * 100)
            end_pct = int(act["ratio"][1] * 100)
            lines.append(f"  {act['act']}. {act['name']} ({start_pct}%-{end_pct}%): {act['goal']}")

        lines.append("")
        lines.append(f"角色要求：")
        lines.append(f"  - 主角必须有≥2个锚点（身份/性格/目标/缺陷）")
        lines.append(f"  - 配角总数≤{ss0['max_characters']}人")
        lines.append(f"  - 每个角色有明确的出场目的")

        return "\n".join(lines)

    # ====== SS2: 正文生成与平台适配 ======

    def validate_opening(self, text: str, platform: str) -> Dict[str, Any]:
        """SS2 红线检查：开篇200字是否进入核心冲突"""
        opening = text[:200] if len(text) >= 200 else text
        conflict_markers = ["冲突", "矛盾", "问题", "危机", "麻烦", "意外", "突然",
                           "消失", "死亡", "背叛", "追杀", "发现", "秘密", "危险",
                           "害怕", "愤怒", "紧张", "恐惧", "崩溃"]

        has_conflict = any(m in opening for m in conflict_markers)

        # 平台差异化要求
        platform_requirements = {
            "小红书": {"min_chars": 50, "label": "50字内"},
            "头条": {"min_chars": 100, "label": "100字内"},
            "知乎": {"min_chars": 200, "label": "200字内"},
            "番茄": {"min_chars": 200, "label": "200字内"},
            "七猫": {"min_chars": 200, "label": "200字内"},
        }
        req = platform_requirements.get(platform, {"min_chars": 200, "label": "200字内"})

        # 更精准检测：在要求字数内
        required_opening = text[:req["min_chars"]] if len(text) >= req["min_chars"] else text
        has_conflict_in_required = any(m in required_opening for m in conflict_markers)

        return {
            "check": "开篇冲突",
            "passed": has_conflict_in_required,
            "issue": None if has_conflict_in_required else
                     f"开篇{req['label']}未进入核心冲突，需要重写开头",
            "platform_requirement": req,
            "detected_markers": [m for m in conflict_markers if m in opening],
        }

    def validate_midpoint(self, text: str) -> Dict[str, Any]:
        """SS2 红线检查：中段是否有情绪推进"""
        if len(text) < 500:
            return {"check": "中段情绪", "passed": True, "issue": None, "note": "文本太短"}

        mid_start = len(text) // 3
        mid_end = len(text) * 2 // 3
        mid_section = text[mid_start:mid_end]

        # 检测情绪变化
        emotion_changes = 0
        prev_emotion = None
        positive_kw = ["笑", "开心", "轻松", "温暖", "希望", "兴奋", "得意"]
        negative_kw = ["怒", "怕", "紧张", "悲伤", "痛苦", "绝望", "担心"]

        # 按段落分析
        paragraphs = [p.strip() for p in mid_section.split("\n") if p.strip() and len(p.strip()) > 20]
        for p in paragraphs:
            pos = sum(p.count(kw) for kw in positive_kw)
            neg = sum(p.count(kw) for kw in negative_kw)
            current = "+" if pos > neg else "-" if neg > pos else "0"
            if prev_emotion and current != prev_emotion:
                emotion_changes += 1
            prev_emotion = current

        return {
            "check": "中段情绪推进",
            "passed": emotion_changes >= 1,
            "issue": None if emotion_changes >= 1 else "中段无情绪推进，建议插入爆点/转折",
            "emotion_changes_detected": emotion_changes,
        }

    def validate_ending(self, text: str) -> Dict[str, Any]:
        """SS2 红线检查：结尾是否有反转或情绪落点"""
        if len(text) < 200:
            return {"check": "结尾", "passed": True, "issue": None, "note": "文本太短"}

        ending = text[-200:]

        # 检查反转标记
        reversal_markers = ["原来", "居然", "竟然", "没想到", "反转", "真相", "真正",
                           "其实是", "从来不是", "一直都是", "骗了", "假的"]

        # 检查情绪落点标记
        emotion_landing = ["泪", "哭", "笑", "沉默", "安静", "温暖", "冷", "痛",
                          "放下", "释然", "后悔", "遗憾", "满足", "幸福"]

        # 检查坏结尾
        bad_endings = ["他终于明白", "她终于懂得", "总的来说", "总而言之", "就这样结束了"]

        has_reversal = any(m in ending for m in reversal_markers)
        has_emotion = any(m in ending for m in emotion_landing)
        has_bad_ending = any(m in ending for m in bad_endings)

        passed = (has_reversal or has_emotion) and not has_bad_ending

        issue = None
        if has_bad_ending:
            issue = "结尾使用了禁止的总结式收尾，需要重写"
        elif not (has_reversal or has_emotion):
            issue = "结尾缺少反转或情绪落点，需要重写"

        return {
            "check": "结尾反转/情绪",
            "passed": passed,
            "issue": issue,
            "has_reversal": has_reversal,
            "has_emotion_landing": has_emotion,
            "has_bad_ending": has_bad_ending,
        }

    def validate_all_redlines(self, text: str, platform: str) -> Dict[str, Any]:
        """SS2: 执行全部红线检查"""
        opening = self.validate_opening(text, platform)
        midpoint = self.validate_midpoint(text)
        ending = self.validate_ending(text)

        all_passed = opening["passed"] and midpoint["passed"] and ending["passed"]

        return {
            "phase": "SS2",
            "passed": all_passed,
            "checks": {
                "opening": opening,
                "midpoint": midpoint,
                "ending": ending,
            },
            "verdict": "✅ 全部通过" if all_passed else "❌ 需要修改",
            "action_required": [
                c["issue"] for c in [opening, midpoint, ending] if c["issue"]
            ],
        }

    def validate_platform_format(self, text: str, platform: str) -> Dict[str, Any]:
        """SS2: 平台格式校验"""
        platform_rules = {
            "小红书": {
                "max_paragraph_length": 150,
                "requires_emoji": False,
                "requires_hashtags": True,
                "check": "检查分段长度和话题标签",
            },
            "知乎": {
                "max_paragraph_length": 500,
                "requires_sections": True,
                "requires_hashtags": False,
                "check": "检查分节标题和逻辑结构",
            },
            "头条": {
                "max_paragraph_length": 300,
                "requires_title_hook": True,
                "check": "检查标题吸引力和段落长度",
            },
            "番茄": {
                "max_paragraph_length": 200,
                "check": "检查段落长度和钩子密度",
            },
            "七猫": {
                "max_paragraph_length": 250,
                "check": "检查情感线完整度",
            },
        }

        rules = platform_rules.get(platform, platform_rules["番茄"])
        issues = []

        # 检查段落长度
        paragraphs = [p for p in text.split("\n") if p.strip()]
        long_paragraphs = [i for i, p in enumerate(paragraphs) if len(p) > rules["max_paragraph_length"]]
        if long_paragraphs:
            issues.append(f"{len(long_paragraphs)}段超过{platform}平台建议长度({rules['max_paragraph_length']}字)")

        # 平台特有检查
        if rules.get("requires_hashtags") and "#" not in text:
            issues.append("小红书平台需要话题标签 #")
        if rules.get("requires_sections") and not re.search(r'#{1,3}\s', text):
            issues.append("知乎平台建议使用分节标题")

        return {
            "platform": platform,
            "rules": rules,
            "passed": len(issues) == 0,
            "issues": issues,
        }

    # ====== 完整流程 ======

    def run_full_workflow(self, word_count: int, platform: str, text: str = "",
                          core_reversal: str = "") -> Dict[str, Any]:
        """执行完整短故事三阶段流程"""
        result = {
            "word_count": word_count,
            "platform": platform,
        }

        # SS0
        result["SS0"] = self.identify_platform(word_count, platform)
        result["SS0_prompt"] = self.generate_topic_prompt(platform, word_count)

        # SS1
        result["SS1"] = {
            "structure": self.get_structure_template(result["SS0"]["structure"]),
            "outline_prompt": self.generate_outline_prompt(
                word_count, platform, core_reversal,
                result["SS0"]["max_characters"]
            ),
        }

        # SS2
        if text:
            result["SS2"] = self.validate_all_redlines(text, platform)
            result["SS2_format"] = self.validate_platform_format(text, platform)
        else:
            result["SS2"] = {"status": "等待正文生成"}

        return result

    # ====== 私有方法 ======

    def _classify_story_type(self, word_count: int) -> Dict:
        """根据字数分类故事类型"""
        for name, info in self.WORD_SYSTEMS.items():
            low, high = info["range"]
            if low <= word_count <= high:
                return {"name": name, **info}
        # 超出范围按最近匹配
        if word_count < 500:
            return {"name": "微小说", **self.WORD_SYSTEMS["微小说"]}
        return {"name": "标准短篇", **self.WORD_SYSTEMS["标准短篇"]}

    # === 兼容 Engine 接口 ===

    def analyze(self, text: str = "", platform: str = "番茄", word_count: int = 0, **kwargs) -> Dict[str, Any]:
        """统一 analyze 接口（兼容 registry 规范）"""
        if not text:
            return {"verdict": "无文本", "issues": ["请提供待检测的文本"]}
        if word_count <= 0:
            word_count = len(text)
        return self.validate_all_redlines(text, platform)
