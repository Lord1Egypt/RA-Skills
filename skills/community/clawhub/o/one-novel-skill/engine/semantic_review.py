#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
semantic_review.py — L3-L4 语义层审查引擎

SKILL.md 声明功能：
- L3 内容质量：情节逻辑自洽(六条连续性法则)、角色弧光推进、世界观一致、伏笔管理追踪、无连续500字纯描写
- L4 阅读体验：温度感(具体>抽象)、独特性(只有本书才有的表达)、翻页驱动力(章末有追问冲动)、人味(像真人写的)
- 六条连续性法则：伤势/情绪/关系/秘密/能力随身记、世界规则不突破、伏笔新增/推进/回收、以弱胜强需铺垫、升级需过程、反派有目标
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple

_log = logging.getLogger("semantic_review")


class L3ContentQualityEngine:
    """L3 内容质量审查引擎"""

    # === 六条连续性法则 ===
    CONTINUITY_LAWS = [
        {
            "id": 1,
            "name": "角色状态随身记",
            "rule": "角色伤势、情绪、关系、秘密、能力不能凭空消失或变化",
            "check": "检查同一角色在连续章节中的伤势/情绪/位置是否一致",
            "red_flag": "角色上一章受伤，本章若无治疗却痊愈",
        },
        {
            "id": 2,
            "name": "世界规则不突破",
            "rule": "世界观设定的规则、限制和代价不能随意突破",
            "check": "检查是否有违反正文开头建立的规则体系的行为",
            "red_flag": "前面说修炼需要灵石，本章突然不需要了",
        },
        {
            "id": 3,
            "name": "伏笔闭环管理",
            "rule": "每章至少推进或新增1个伏笔，回收的伏笔必须有铺垫",
            "check": "统计本章的伏笔新增/推进/回收数量",
            "red_flag": "连续3章无伏笔推进 → 节奏崩塌",
        },
        {
            "id": 4,
            "name": "以弱胜强有代价",
            "rule": "以弱胜强必须有铺垫(计谋/环境/他人帮助)、过程(逐步逆转)和代价(受伤/消耗/牺牲)",
            "check": "检查战斗/对抗场景是否满足铺垫-过程-代价三要素",
            "red_flag": "主角一拳打飞高两个境界的对手，没有任何代价",
        },
        {
            "id": 5,
            "name": "升级有过程有风险",
            "rule": "主角升级必须有过程(修炼/领悟/战斗)、风险(失败可能/走火入魔)和瓶颈(卡住→突破)",
            "check": "检查升级场景是否有过程描写、是否提到失败风险和瓶颈",
            "red_flag": "主角睡一觉就连升三级",
        },
        {
            "id": 6,
            "name": "反派有目标有资源",
            "rule": "反派必须有明确目标、可用资源和行动逻辑，不能是单纯的送经验工具人",
            "check": "检查反派出场是否有动机说明、是否有反制手段",
            "red_flag": "反派智商忽高忽低，上一章深谋远虑本章无脑送",
        },
    ]

    def __init__(self):
        self._continuity_log: List[Dict] = []

    def get_continuity_laws(self) -> List[Dict]:
        """获取六条连续性法则"""
        return self.CONTINUITY_LAWS

    def get_continuity_checklist(self) -> List[str]:
        """获取连续性检查清单"""
        return [f"[法则{law['id']}] {law['name']}: {law['rule']} — 红线: {law['red_flag']}" for law in self.CONTINUITY_LAWS]

    def analyze(self, text: str, chapter: int = 1, state: Dict = None, **kwargs) -> Dict[str, Any]:
        """执行 L3 内容质量审查"""
        issues = []

        # 1. 检查连续纯描写段落
        desc_issues = self._check_pure_description(text)
        issues.extend(desc_issues)

        # 2. 检查以弱胜强场景
        combat_issues = self._check_combat_balance(text)
        issues.extend(combat_issues)

        # 3. 检查升级场景
        upgrade_issues = self._check_upgrade_scenes(text)
        issues.extend(upgrade_issues)

        # 4. 检查反派智商
        villain_issues = self._check_villain_intelligence(text)
        issues.extend(villain_issues)

        # 5. 检查世界规则一致性
        world_issues = self._check_world_consistency(text)
        issues.extend(world_issues)

        # 6. 检查伏笔闭环
        hook_issues = self._check_hook_closure(text, chapter)
        issues.extend(hook_issues)

        passed = len(issues) == 0
        return {
            "verdict": "通过" if passed else "需优化",
            "layer": "L3",
            "issues": issues,
            "continuity_score": max(0, 100 - len(issues) * 15),
            "details": {
                "pure_description": len(desc_issues),
                "combat_balance": len(combat_issues),
                "upgrade_scenes": len(upgrade_issues),
                "villain_intelligence": len(villain_issues),
                "world_consistency": len(world_issues),
                "hook_closure": len(hook_issues),
            },
        }

    def _check_pure_description(self, text: str) -> List[str]:
        """检查连续500字纯描写（无对话/无动作推进）"""
        issues = []
        # 将文本按自然段分割
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        if not paragraphs:
            return issues

        # 检测连续纯描写段落
        desc_streak = 0
        desc_chars = 0
        for p in paragraphs:
            has_dialogue = any(marker in p for marker in ['"', '"', '"', '「', '」', '：', '说', '道', '问', '喊'])
            has_action = bool(re.search(r'[走向跑跳打踢踹砸摔拿放推拉抱背扛]+', p))
            if not has_dialogue and not has_action and len(p) > 30:
                desc_streak += 1
                desc_chars += len(p)
            else:
                if desc_chars >= 500:
                    issues.append(f"[连续纯描写] 连续{desc_chars}字纯描写无对话/动作推进，建议打断节奏")
                desc_streak = 0
                desc_chars = 0

        if desc_chars >= 500:
            issues.append(f"[连续纯描写] 连续{desc_chars}字纯描写无对话/动作推进，建议打断节奏")

        return issues

    def _check_combat_balance(self, text: str) -> List[str]:
        """检查以弱胜强是否有铺垫/过程/代价"""
        issues = []
        # 检测战斗/对抗场景关键词
        combat_keywords = ["战斗", "对决", "交手", "激战", "对抗", "搏斗", "厮杀"]
        has_combat = any(kw in text for kw in combat_keywords)

        if has_combat:
            # 检查铺垫（计谋/环境/他人帮助）
            prep_keywords = ["计划", "计谋", "策略", "埋伏", "地形", "陷阱", "帮手", "增援", "牵制"]
            has_prep = any(kw in text for kw in prep_keywords)

            # 检查过程（逐步逆转）
            process_keywords = ["先", "然后", "接着", "随后", "突然", "反转", "逆转", "逐渐", "慢慢"]
            has_process = any(kw in text for kw in process_keywords)

            # 检查代价（受伤/消耗/牺牲）
            cost_keywords = ["受伤", "伤口", "血", "消耗", "疲惫", "力竭", "代价", "牺牲", "废了"]
            has_cost = any(kw in text for kw in cost_keywords)

            if not has_prep:
                issues.append("[以弱胜强] 战斗场景缺少铺垫（计谋/环境/帮手），主角可能过于轻松取胜")
            if not has_cost:
                issues.append("[以弱胜强] 战斗场景缺少代价描写（受伤/消耗/牺牲），主角可能碾压")

        return issues

    def _check_upgrade_scenes(self, text: str) -> List[str]:
        """检查升级场景是否有过程/风险/瓶颈"""
        issues = []
        upgrade_keywords = ["突破", "晋级", "升级", "进阶", "提升", "觉醒", "领悟", "顿悟"]
        has_upgrade = any(kw in text for kw in upgrade_keywords)

        if has_upgrade:
            # 检查过程
            process_kw = ["修炼", "打坐", "冥想", "运转", "冲击", "吸收", "炼化", "融合"]
            has_process = any(kw in text for kw in process_kw)

            # 检查风险
            risk_kw = ["风险", "危险", "走火入魔", "反噬", "失败", "崩溃", "不稳", "失控"]
            has_risk = any(kw in text for kw in risk_kw)

            if not has_process:
                issues.append("[升级场景] 缺少修炼/突破过程描写，可能过于突兀")
            if not has_risk:
                issues.append("[升级场景] 未提及升级失败的风险或代价")

        return issues

    def _check_villain_intelligence(self, text: str) -> List[str]:
        """检查反派是否有目标和反制手段"""
        issues = []
        # 检测反派相关关键词
        villain_keywords = ["敌人", "反派", "对手", "追杀", "阻击", "埋伏", "暗算"]
        has_villain = any(kw in text for kw in villain_keywords)

        if has_villain:
            # 检查反派动机
            motive_kw = ["因为", "为了", "想要", "目的是", "计划", "目标是"]
            has_motive = any(kw in text for kw in motive_kw)

            # 检查反制手段
            counter_kw = ["反制", "应对", "预案", "后手", "底牌", "防备", "预留"]
            has_counter = any(kw in text for kw in counter_kw)

            if not has_motive:
                issues.append("[反派智商] 反派出场未交代动机/目标，可能沦为工具人")
            if not has_counter:
                issues.append("[反派智商] 反派未展示反制手段，可能被主角轻松击败")

        return issues

    def _check_world_consistency(self, text: str) -> List[str]:
        """检查世界规则一致性（基于规则标记）"""
        issues = []
        # 检测规则声明的关键词
        rule_declarations = re.findall(r'(?:在|按照|根据)(?:这[个种]|整个)?[^，。]{0,20}(?:规则|法则|定律|设定|体系)[^，。]{0,20}(?:是|为|必须|只能|不能|禁止)', text)

        # 检测可能违反规则的行为
        if rule_declarations:
            violation_keywords = ["但是", "不过", "除非", "除了", "特殊", "例外", "居然", "竟然"]
            for rule in rule_declarations:
                # 在规则后1000字内搜索例外标记
                rule_pos = text.find(rule)
                if rule_pos >= 0:
                    after_rule = text[rule_pos:rule_pos + 1000]
                    violations = [kw for kw in violation_keywords if kw in after_rule]
                    if violations:
                        issues.append(f"[世界观一致] 规则声明 '{rule[:30]}...' 后出现可能的例外标记: {violations}")

        return issues

    def _check_hook_closure(self, text: str, chapter: int) -> List[str]:
        """检查伏笔闭环"""
        issues = []
        # 统计伏笔关键词出现频率
        hook_markers = ["伏笔", "暗示", "预示", "预兆", "铺垫", "线索"]
        hook_count = sum(text.count(m) for m in hook_markers)

        if chapter > 3 and hook_count == 0:
            issues.append("[伏笔闭环] 本章无伏笔推进或新增，连续缺失可能导致故事张力下降")

        return issues


class L4ReadingExperienceEngine:
    """L4 阅读体验审查引擎"""

    def __init__(self):
        pass

    def analyze(self, text: str, chapter: int = 1, **kwargs) -> Dict[str, Any]:
        """执行 L4 阅读体验审查"""
        issues = []

        # 1. 温度感检查（具体 vs 抽象）
        warmth_issues = self._check_warmth(text)
        issues.extend(warmth_issues)

        # 2. 独特性检查
        uniqueness_issues = self._check_uniqueness(text)
        issues.extend(uniqueness_issues)

        # 3. 翻页驱动力检查
        page_turn_issues = self._check_page_turning(text)
        issues.extend(page_turn_issues)

        # 4. 人味检查
        human_issues = self._check_human_flavor(text)
        issues.extend(human_issues)

        # 5. 情感波动检查
        emotion_issues = self._check_emotional_variety(text)
        issues.extend(emotion_issues)

        passed = len(issues) == 0
        return {
            "verdict": "通过" if passed else "需优化",
            "layer": "L4",
            "issues": issues,
            "experience_score": max(0, 100 - len(issues) * 12),
            "details": {
                "warmth": len(warmth_issues),
                "uniqueness": len(uniqueness_issues),
                "page_turning": len(page_turn_issues),
                "human_flavor": len(human_issues),
                "emotional_variety": len(emotion_issues),
            },
        }

    def _check_warmth(self, text: str) -> List[str]:
        """检查温度感：具体 > 抽象"""
        issues = []
        # 检测抽象情绪告知
        abstract_emotions = [
            "他很生气", "他很害怕", "他很紧张", "他很高兴", "他很悲伤",
            "他感到愤怒", "他感到恐惧", "他感到温暖", "他感到难过",
            "她觉得开心", "她觉得害怕", "她觉得愤怒",
        ]
        found = [ae for ae in abstract_emotions if ae in text]
        if found:
            issues.append(f"[温度感] 发现{len(found)}处直接告知情绪: {found[:3]}，建议用动作/环境/生理反应替代")

        # 检测感官描写密度
        sensory_markers = {
            "视觉": ["看到", "看见", "映入眼帘", "远远望去", "望去", "望去"],
            "听觉": ["听到", "听见", "传入耳", "响声", "声音", "回荡"],
            "嗅觉": ["闻到", "气味", "香味", "臭味", "弥漫"],
            "触觉": ["摸到", "碰到", "冰凉", "滚烫", "粗糙", "光滑"],
            "味觉": ["尝到", "味道", "酸甜苦辣", "涩", "甘甜"],
        }
        sensory_count = {}
        for sense, markers in sensory_markers.items():
            count = sum(text.count(m) for m in markers)
            if count > 0:
                sensory_count[sense] = count

        if len(sensory_count) < 2:
            issues.append(f"[感官描写] 仅使用了{len(sensory_count)}种感官（建议每场景至少2种），当前: {list(sensory_count.keys())}")

        return issues

    def _check_uniqueness(self, text: str) -> List[str]:
        """检查独特性：是否有只有本书才有的表达"""
        issues = []
        # 检测通用模板化表达
        generic_patterns = [
            (r"眼中闪过一丝\S{1,4}", "万能表情模板"),
            (r"嘴角勾起一抹\S{1,4}", "万能表情模板"),
            (r"仿佛是?\S{1,4}一般", "文喻模板"),
            (r"犹如\S{1,4}般", "文喻模板"),
            (r"宛若\S{1,4}", "文喻模板"),
            (r"时间一分一秒[地]?过去", "时间过渡模板"),
            (r"夜幕降临", "时间过渡模板"),
            (r"与此同时", "过渡词模板"),
            (r"就在这[时个]?时候?", "过渡词模板"),
            (r"紧接着", "过渡词模板"),
        ]
        for pattern, category in generic_patterns:
            matches = re.findall(pattern, text)
            if matches:
                issues.append(f"[独特性] 发现{len(matches)}处{category}: {matches[:3]}")

        return issues

    def _check_page_turning(self, text: str) -> List[str]:
        """检查翻页驱动力：章末是否有追问冲动"""
        issues = []
        if len(text) < 200:
            return issues

        last_300 = text[-300:]

        # 检查章末是否是总结式
        bad_endings = [
            "他终于明白了", "她终于懂得", "他终于学会",
            "总的来说", "总而言之", "综上所述",
            "他不知道的是", "她不知道的是",
            "更大的挑战还在后面", "更大的风暴即将来临",
            "这一夜，注定无人入眠",
        ]
        for be in bad_endings:
            if be in last_300:
                issues.append(f"[翻页驱动] 章末使用了禁止的总结式结尾: '{be}'")
                break

        # 检查是否有钩子标记
        hook_markers = ["?", "？", "突然", "就在这时", "他愣住了", "她愣住了",
                       "门开了", "脚步声", "敲门声", "电话响了", "屏幕亮了",
                       "还没", "不知道", "为什么", "怎么", "难道"]
        has_hook = any(m in last_300 for m in hook_markers)

        if not has_hook:
            issues.append("[翻页驱动] 章末可能缺少具体钩子，读者可能没有翻页冲动")

        return issues

    def _check_human_flavor(self, text: str) -> List[str]:
        """检查人味：像真人写的"""
        issues = []

        # 检测 AI 腔特征
        ai_patterns = [
            (r"不是\S{1,10}而是\S{1,10}", "否排句式(不是A而是B)"),
            (r"不仅\S{1,10}而且\S{1,10}", "并列句式"),
            (r"一方面\S{1,10}另一方面\S{1,10}", "论文腔"),
        ]
        for pattern, category in ai_patterns:
            matches = re.findall(pattern, text)
            if len(matches) > 1:
                issues.append(f"[人味] 发现{len(matches)}处{category}，AI特征明显")

        # 检测句长方差
        sentences = re.split(r'[。！？\n]', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) >= 5]
        if len(sentences) >= 5:
            lengths = [len(s) for s in sentences]
            avg_len = sum(lengths) / len(lengths)
            variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
            if variance < 64:  # 标准差 < 8
                issues.append(f"[人味] 句长方差过小({variance:.0f}<64)，句子长度过于均匀，缺乏自然变化")

        # 检测口语化特征
        oral_markers = ["啧", "得嘞", "靠", "我去", "卧槽", "行吧", "好吧", "嗯", "啊", "哦", "咦"]
        oral_count = sum(text.count(m) for m in oral_markers)
        if oral_count == 0 and len(text) > 500:
            issues.append("[人味] 全文无口语化特征，可能过于书面化")

        return issues

    def _check_emotional_variety(self, text: str) -> List[str]:
        """检查情感波动"""
        issues = []
        if len(text) < 500:
            return issues

        # 按段落检测情感关键词分布
        paragraphs = [p.strip() for p in text.split("\n") if p.strip() and len(p.strip()) > 20]
        if len(paragraphs) < 3:
            return issues

        emotion_segments = []
        positive_kw = ["笑", "开心", "高兴", "兴奋", "轻松", "温暖", "得意", "满足", "希望"]
        negative_kw = ["怒", "气", "怕", "恐惧", "紧张", "悲伤", "难过", "痛苦", "绝望", "担心"]
        neutral_kw = ["想", "思考", "沉思", "沉默", "平静", "冷静", "安静"]

        for p in paragraphs:
            pos = sum(p.count(kw) for kw in positive_kw)
            neg = sum(p.count(kw) for kw in negative_kw)
            neu = sum(p.count(kw) for kw in neutral_kw)
            if pos > neg and pos > neu:
                emotion_segments.append("+")
            elif neg > pos and neg > neu:
                emotion_segments.append("-")
            else:
                emotion_segments.append("0")

        # 检查情绪是否单一
        unique_emotions = set(emotion_segments)
        if len(unique_emotions) == 1:
            emo_name = {"+": "正面", "-": "负面", "0": "中性"}.get(list(unique_emotions)[0], "单一")
            issues.append(f"[情感波动] 全章情绪单一（{emo_name}），缺少情感起伏")

        return issues


class SemanticReviewEngine:
    """L3+L4 统一审查入口"""

    def __init__(self):
        self.l3 = L3ContentQualityEngine()
        self.l4 = L4ReadingExperienceEngine()

    def analyze(self, text: str, chapter: int = 1, state: Dict = None, **kwargs) -> Dict[str, Any]:
        """执行完整 L3+L4 审查"""
        l3_result = self.l3.analyze(text, chapter, state)
        l4_result = self.l4.analyze(text, chapter)

        all_issues = l3_result.get("issues", []) + l4_result.get("issues", [])
        passed = len(all_issues) == 0

        return {
            "verdict": "通过" if passed else "需优化",
            "layers": ["L3", "L4"],
            "l3": l3_result,
            "l4": l4_result,
            "issues": all_issues,
            "total_issues": len(all_issues),
            "composite_score": (l3_result.get("continuity_score", 0) + l4_result.get("experience_score", 0)) // 2,
            "continuity_laws": self.l3.get_continuity_laws(),
        }

    def get_checklist(self) -> Dict[str, List[str]]:
        """获取完整审查清单"""
        return {
            "L3_continuity": self.l3.get_continuity_checklist(),
            "L4_experience": [
                "[温度感] 每场景至少2种感官描写",
                "[独特性] 避免通用模板表达",
                "[翻页驱动] 章末有具体钩子",
                "[人味] 句长有变化，有口语化特征",
                "[情感波动] 全章至少2次情绪转换",
            ],
        }

    def inject_into_prompt(self, chapter: int) -> str:
        """生成注入 LLM prompt 的审查要求"""
        lines = [
            "【L3-L4 语义层审查要求】",
            "",
            "## L3 内容质量",
        ]
        for law in self.l3.get_continuity_laws():
            lines.append(f"- {law['name']}: {law['rule']} (红线: {law['red_flag']})")

        lines.append("")
        lines.append("## L4 阅读体验")
        lines.append("- 温度感：用动作/环境/感官展示，不要直接告知情绪")
        lines.append("- 独特性：避免'眼中闪过一丝/嘴角勾起一抹/仿佛……一般'等模板")
        lines.append("- 翻页驱动：章末必须有具体的新问题/新悬念")
        lines.append("- 人味：句长要有变化，插入口语化表达，避免AI腔")
        lines.append("- 情感波动：全章至少2次情绪转换")

        return "\n".join(lines)
