#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
StoryGate — 14维可插拔结构化评审

从 references/writing-techniques-allinone/09-editor-perspective.md
提取14维审查模型，目前实现了7个核心维度 + 7个扩展维度。
"""
import re, json, math
from typing import List, Dict, Tuple, Type
from .engine_base import EngineBase


PLATFORM_WEIGHTS: Dict[str, Dict[str, int]] = {
    "番茄": {"开篇": 15, "人设": 10, "节奏": 15, "冲突": 10, "悬念": 10, "情感": 10, "文笔": 10, "市场": 20},
    "起点": {"开篇": 10, "人设": 15, "节奏": 10, "冲突": 15, "悬念": 10, "情感": 10, "文笔": 15, "市场": 15},
    "晋江": {"开篇": 10, "人设": 20, "节奏": 10, "冲突": 10, "悬念": 10, "情感": 20, "文笔": 10, "市场": 10},
    "七猫": {"开篇": 15, "人设": 10, "节奏": 15, "冲突": 10, "悬念": 10, "情感": 10, "文笔": 5,  "市场": 25},
    "飞卢": {"开篇": 10, "人设": 10, "节奏": 20, "冲突": 10, "悬念": 15, "情感": 5,  "文笔": 5,  "市场": 25},
}
DEFAULT_WEIGHTS = {"开篇": 15, "人设": 15, "节奏": 15, "冲突": 15, "悬念": 10, "情感": 10, "文笔": 10, "市场": 10}


class GatePlugin(EngineBase):
    """评审维度插件基类"""
    dim_name: str = ""
    engine_tags = ["评审"]

    def score(self, text: str) -> Tuple[int, str]:
        raise NotImplementedError

    def analyze(self, text, **kwargs):
        score, suggestion = self.score(text)
        return [f"[{self.dim_name}] {score}/100 - {suggestion}"]


# ══════════════════════════════════════════════════════════════════
# 已存在的7个核心维度插件（保留，内容可能增强）
# ══════════════════════════════════════════════════════════════════

class ConsistencyPlugin(GatePlugin):
    dim_name = "一致性"
    engine_name = "gate_consistency"

    def score(self, text):
        s = 100
        time_jumps = re.findall(r'(?:三天后|一周后|一个月后|第二天|次日|转眼间)', text)
        if len(time_jumps) > 2:
            s -= min(30, len(time_jumps) * 10)
        quotes = text.count('"') if '"' in text else text.count('\u201c')
        if quotes % 2 != 0:
            s -= 15
        return max(s, 0), "时间跳跃过多" if s < 85 else "一致"


class CharacterPlugin(GatePlugin):
    dim_name = "人设"
    engine_name = "gate_character"

    def score(self, text):
        s = 85
        dialogs = re.findall(r'[\u4e00-\u9fff]{2,4}[\uff1a:]', text[:2000])
        if len(dialogs) < 2:
            s -= 20
        if re.search(r'(眼中闪过|嘴角勾起|哼冷一声|淡淡道)', text):
            s -= 10
        return max(s, 0), "对话区分度不够" if s < 70 else "合格"


class PacingPlugin(GatePlugin):
    dim_name = "节奏"
    engine_name = "gate_pacing"

    def score(self, text):
        s = 80
        paras = [p for p in text.split('\n') if p.strip()]
        if not paras:
            return 50, "段落结构异常"
        avg_para = sum(len(p) for p in paras) / len(paras)
        if avg_para > 200:
            s -= 20
        elif avg_para < 30:
            s -= 10
        if len(paras) < 5:
            s -= 15
        return max(s, 0), "段落过长或结构单一" if s < 70 else "节奏合理"


class ContinuityPlugin(GatePlugin):
    dim_name = "叙事"
    engine_name = "gate_continuity"

    def score(self, text):
        s = 85
        jumps = re.findall(r'(突然|就在这时|没想到|结果)', text[:500])
        if len(jumps) > 3:
            s -= 10
        return max(s, 0), "场景衔接突然" if s < 75 else "连贯"


class ForeshadowPlugin(GatePlugin):
    dim_name = "伏笔"
    engine_name = "gate_foreshadow"

    def score(self, text):
        s = 75
        hooks = re.findall(r'(难道|是不是|不对劲|有问题|奇怪|如|似乎|好像)', text)
        if len(hooks) < 2:
            s -= 15
        return max(s, 0), "伏笔密度低" if s < 65 else "有提示"


class AestheticPlugin(GatePlugin):
    dim_name = "审美"
    engine_name = "gate_aesthetic"

    def score(self, text):
        s = 80
        templates = re.findall(r'(眼中闪过[^\u3002]{0,10}|嘴角勾起[^\u3002]{0,10}|脸上露出[^\u3002]{0,10})', text)
        if templates:
            s -= min(20, len(templates) * 8)
        sentences = [ss for ss in re.split(r'[\u3002\uff01\uff1f!?]', text) if ss.strip()]
        if len(sentences) > 3:
            lens = [len(ss) for ss in sentences]
            avg = sum(lens) / len(lens)
            var = sum((l - avg) ** 2 for l in lens) / len(lens)
            if var < 10:
                s -= 10
        return max(s, 0), "模板化表达多" if s < 70 else "语言质感好"


class EngagementPlugin(GatePlugin):
    dim_name = "读者"
    engine_name = "gate_engagement"

    def score(self, text):
        s = 75
        first_300 = text[:300]
        if len(first_300) < 100:
            s -= 30
        else:
            hooks = re.findall(r'[\uff1f?]|突然|就在这时|没想到|可是|但是|却|发现|竟然', first_300)
            if len(hooks) < 2:
                s -= 15
        ending = text[-200:].strip()
        if ending.endswith(('\u3002', '.', '\uff0c', ',')):
            s -= 10
        return max(s, 0), "开头钩子不足或章末平淡" if s < 65 else "可读性高"


# ══════════════════════════════════════════════════════════════════
# 新增：7个扩展维度插件（基于 09-editor-perspective.md）
# ══════════════════════════════════════════════════════════════════

class OpeningHookPlugin(GatePlugin):
    """第一关：开篇吸引力"""
    dim_name = "开篇"
    engine_name = "gate_opening"

    def score(self, text):
        first_100 = text[:100]
        first_500 = text[:500]
        s = 70

        # 前100字是否有冲突/异常/悬念
        hooks_100 = re.findall(r'[\uff1f?]|怒|惊|杀|死|\u4f46|却|发\u73b0|突\u7136', first_100)
        if len(hooks_100) >= 2:
            s += 15
        elif len(hooks_100) == 1:
            s += 5
        else:
            s -= 15

        # 前500字信息密度是否合适
        info_chars = len(first_500)
        if info_chars < 50:
            s -= 20  # 太短，没有内容
        info_ratio = len(re.findall(r'[\u4e00-\u9fff]', first_500)) / max(len(first_500), 1)
        if info_ratio < 0.5:
            s -= 10  # 非中文内容太多

        level = "强" if s >= 80 else ("中" if s >= 60 else "弱")
        return max(0, min(100, s)), f"开篇吸引力{level}，前100字钩子{len(hooks_100)}个"


class ConflictPlugin(GatePlugin):
    """第四关：冲突设计"""
    dim_name = "冲突"
    engine_name = "gate_conflict"

    def score(self, text):
        first_3k = text[:3000]
        s = 75

        # 冲突密度
        conflict_words = re.findall(r'(怒|战|杀|斗|争|吵|挡|击|拍案|冷\u7b11|皱眉|握\u62f3)', first_3k)
        conflict_count = len(conflict_words)
        s += min(10, conflict_count)

        # 冲突层次 (即刻/中期/长期/隐性)
        if re.search(r'(难道|到底|为什么|幕后|真相)', first_3k):
            s += 5  # 有长期冲突暗示
        if re.search(r'(内心|挣扎|矛盾|犹豫|纠结)', first_3k):
            s += 5  # 有内心冲突

        # 冲突是否太单薄
        if conflict_count < 2:
            s -= 25
        elif conflict_count < 5:
            s -= 10

        level = "丰富" if s >= 85 else ("合格" if s >= 65 else "单薄")
        return max(0, min(100, s)), f"冲突{level}，{conflict_count}处冲突标记"


class SuspensePlugin(GatePlugin):
    """第五关：悬念密度"""
    dim_name = "悬念"
    engine_name = "gate_suspense"

    def score(self, text):
        s = 70
        # 章末悬念
        ending = text[-300:]
        suspense_ending = re.findall(r'[\uff1f]|突然|就在这时|难道|到底|发现|却|竟然', ending)
        if suspense_ending:
            s += 15
        else:
            s -= 10

        # 全局悬念暗示
        full = text[:2000]
        global_hooks = re.findall(r'(秘密|真相|幕后|身份|来历|谜)', full)
        s += min(10, len(global_hooks))

        # 悬念层次
        if re.search(r'(更大的|真正的|不简单|没那么)', full):
            s += 5

        level = "高" if s >= 85 else ("中" if s >= 65 else "低")
        return max(0, min(100, s)), f"悬念密度{level}，章末{'有' if suspense_ending else '无'}钩子"


class CharacterArcPlugin(GatePlugin):
    """第六关：人物弧光"""
    dim_name = "弧光"
    engine_name = "gate_arc"

    def score(self, text):
        s = 70
        full = text[:3000]

        # 欲望标识
        desire = re.findall(r'(想要|渴望|追求|梦想|目标|发誓|承诺|一定)', full)
        s += min(15, len(desire) * 3)

        # 挫折/转变
        setback = re.findall(r'(失败|受伤|打击|羞辱|跌|落|陷入|困境)', full)
        s += min(15, len(setback) * 3)

        # 内心反思
        reflect = re.findall(r'(心想|思索|回忆|想起|后悔|明白了|意识到)', full)
        s += min(10, len(reflect) * 2)

        level = "清晰" if s >= 85 else ("有" if s >= 65 else "模糊")
        return max(0, min(100, s)), f"人物弧光{level}，欲望{len(desire)}处+挫折{len(setback)}处"


class EmotionPlugin(GatePlugin):
    """第十一关：情感投入"""
    dim_name = "情感"
    engine_name = "gate_emotion"

    def score(self, text):
        s = 70
        full = text[:3000]

        # 情感词密度
        emotion_words = re.findall(r'(感动|悲伤|愤怒|喜悦|恐惧|孤独|温暖|心痛|激动|欣慰|骄傲|羞愧|委屈)', full)
        s += min(15, len(emotion_words) * 2)

        # 共情触发点
        empathy = re.findall(r'(理解|在乎|在一起|撑|支持|陪伴)|(我不要|我不想|我害怕|对不起|谢谢你)', full)
        s += min(10, len(empathy) * 2)

        # 情感场景强度
        if re.search(r'(泪|颤抖|哽咽|拥抱|握紧|坚持)', full):
            s += 5

        level = "强" if s >= 85 else ("中" if s >= 65 else "弱")
        return max(0, min(100, s)), f"情感投入{level}，情绪词{len(emotion_words)}个"


class MarketPlugin(GatePlugin):
    """第十三关：市场性评估"""
    dim_name = "市场"
    engine_name = "gate_market"

    def score(self, text):
        s = 70
        full = text[:3000]

        # 品类适配 (从文本特征判断品类倾向)
        if re.search(r'(系统|签到|抽奖|升级|打怪|副本)', full):
            s += 5  # 网游/系统文
        if re.search(r'(赘婿|退婚|弃少|神医|仙尊)', full):
            s += 5  # 爽文
        if re.search(r'(穿越|重生|转世|异界)', full):
            s += 5  # 穿越

        # 卖点清晰度（前300字能否提炼卖点）
        first_300 = text[:300]
        selling_points = re.findall(r'(奇怪|异常|与众不同|特别|唯一|独一无二)', first_300)
        s += min(5, len(selling_points))

        # 可持续性（是否有可展开的内容空间）
        if re.search(r'(世界|大陆|宇宙|宗门|家族|帝国|王朝)', full):
            s += 5

        level = "高" if s >= 85 else ("中" if s >= 65 else "低")
        return max(0, min(100, s)), f"市场潜力{level}"


# ══════════════════════════════════════════════════════════════════
# StoryGate 主类
# ══════════════════════════════════════════════════════════════════

class StoryGate(EngineBase):
    """14维可插拔结构化评审"""
    engine_name = "story_gate"
    engine_tags = ["故事", "评审"]
    _plugins: Dict[str, Type[GatePlugin]] = {}
    _initialized = False

    @classmethod
    def _ensure_plugins(cls):
        if cls._initialized:
            return
        # 核心7维
        for p_cls in [ConsistencyPlugin, CharacterPlugin, PacingPlugin,
                      ContinuityPlugin, ForeshadowPlugin, AestheticPlugin,
                      EngagementPlugin]:
            cls.register(p_cls)
        # 扩展7维
        for p_cls in [OpeningHookPlugin, ConflictPlugin, SuspensePlugin,
                      CharacterArcPlugin, EmotionPlugin, MarketPlugin]:
            cls.register(p_cls)
        cls._initialized = True

    @classmethod
    def register(cls, plugin_class: Type[GatePlugin]):
        name = plugin_class.dim_name
        if not name:
            raise ValueError(f"Plugin {plugin_class.__name__} must define dim_name")
        cls._plugins[name] = plugin_class

    @classmethod
    def unregister(cls, dim_name: str):
        cls._plugins.pop(dim_name, None)

    @classmethod
    def list_plugins(cls) -> List[str]:
        cls._ensure_plugins()
        return list(cls._plugins.keys())

    @classmethod
    def review(cls, text: str, chapter: int = 0, genre: str = "",
               platform: str = "") -> List[str]:
        if not text or not isinstance(text, str):
            return ["[StoryGate] 输入文本为空或类型错误"]
        cls._ensure_plugins()
        weights = _resolve_weights(platform)
        scores: Dict[str, int] = {}
        issues = []

        for dname, pcls in cls._plugins.items():
            try:
                p = pcls()
                score, suggestion = p.score(text)
                scores[dname] = score
            except Exception:
                scores[dname] = 50
                continue

        # 综合加权评分
        w_total = sum(scores.get(d, 50) * w for d, w in weights.items() if d in scores)
        w_max = sum(100 * w for d, w in weights.items() if d in scores)
        overall = w_total / max(w_max, 1) * 100

        # 按优先级产出 issues
        for dname, score in sorted(scores.items(), key=lambda x: weights.get(x[0], 10), reverse=True):
            w = weights.get(dname, 10)
            if score < 50:
                issues.append(f"[P0] [{dname}] {score}/100 (权重{w}%) — 必须修改")
            elif score < 65:
                issues.append(f"[P1] [{dname}] {score}/100 (权重{w}%) — 建议修改")
            elif score < 75:
                issues.append(f"[P2] [{dname}] {score}/100 (权重{w}%) — 可优化")

        issues.append(f"[综合] {overall:.0f}/100 — {_overall_label(overall)}")
        if overall < 60:
            issues.insert(0, f"[P0] 综合评分{overall:.0f}/100 — 建议重写本章")
        return issues

    def analyze(self, text, **kwargs):
        return self.review(text, genre=kwargs.get("genre", ""),
                           platform=kwargs.get("platform", ""))


def _resolve_weights(platform: str) -> Dict[str, int]:
    return PLATFORM_WEIGHTS.get(platform, DEFAULT_WEIGHTS)


def _overall_label(score: float) -> str:
    if score >= 90:
        return "优秀"
    elif score >= 75:
        return "良好"
    elif score >= 60:
        return "及格"
    else:
        return "需修改"


# Auto-register on module import
StoryGate._ensure_plugins()
