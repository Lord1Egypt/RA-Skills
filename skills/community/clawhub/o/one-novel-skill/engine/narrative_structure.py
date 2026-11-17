#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
narrative_structure.py — 叙事结构增强引擎

SKILL.md 声明功能：
- 八段式章节结构（本章目标→有利出现→困难降临→积极应对→突发转折→认知颠覆→本章高潮→悬念留钩）
- 反直觉追问法（每章规划时的三个问题）
- 升番逻辑（信息揭露逐级升级：基础揭示→进阶揭示→出乎意料）
- 情绪生理反应置换表（愤怒→手背青筋暴起等）
"""

import logging
from typing import Dict, List, Optional, Any

_log = logging.getLogger("narrative_structure")


class NarrativeStructureEngine:
    """叙事结构增强引擎 — 八段式结构 + 反直觉追问 + 升番逻辑 + 情绪置换"""

    # === 八段式章节结构 ===
    EIGHT_BEAT_STRUCTURE = [
        {
            "beat": 1, "name": "本章目标",
            "ratio": (0.00, 0.05),
            "goal": "开篇锚定：一句话说清本章要解决的核心问题",
            "check": "读者看完前5%能不能一句话说出本章要讲什么？",
            "red_flag": "前300字没有明确冲突目标",
            "example": "李牧必须在天黑前找到失踪的妹妹，否则线索会断。",
        },
        {
            "beat": 2, "name": "有利出现",
            "ratio": (0.05, 0.20),
            "goal": "给主角一个阶段性优势/进展/希望",
            "check": "读者是否觉得'有希望了'？",
            "red_flag": "连续2段以上没有推进目标的进展",
            "example": "李牧在旧宅找到了妹妹留下的密码纸条。",
        },
        {
            "beat": 3, "name": "困难降临",
            "ratio": (0.20, 0.40),
            "goal": "优势被打破，出现新的障碍/敌人/意外",
            "check": "读者是否感到'麻烦了'？障碍是否有新意？",
            "red_flag": "障碍和上一章重复（同样的反派用同样的手段）",
            "example": "解读密码时，三个黑衣人突然包围了旧宅。",
        },
        {
            "beat": 4, "name": "积极应对",
            "ratio": (0.40, 0.55),
            "goal": "主角不放弃，展示机智/勇气/成长",
            "check": "主角的应对是否展示了角色特质（非被动挨打）？",
            "red_flag": "主角靠运气/巧合脱困，非自身能力",
            "example": "李牧利用旧宅的地道从后门突围，同时记下了黑衣人的特征。",
        },
        {
            "beat": 5, "name": "突发转折",
            "ratio": (0.55, 0.70),
            "goal": "一个出乎意料的信息/事件颠覆之前认知",
            "check": "读者是否惊讶'原来如此'？转折是否有伏笔支撑？",
            "red_flag": "转折毫无预兆（机械降神）",
            "example": "突围后李牧发现密码指向的地点不是废弃工厂，而是警察局——妹妹在报警。",
        },
        {
            "beat": 6, "name": "认知颠覆",
            "ratio": (0.70, 0.80),
            "goal": "主角重新理解事件的全貌，认知升级",
            "check": "主角是否学到了什么？世界观是否被扩展？",
            "red_flag": "主角的认知没有任何变化（原地踏步）",
            "example": "李牧意识到：这不是绑架，妹妹发现了某个秘密，正在被灭口——她不是受害者，是证人。",
        },
        {
            "beat": 7, "name": "本章高潮",
            "ratio": (0.80, 0.92),
            "goal": "本章最激烈的冲突/对决/情感爆发点",
            "check": "读者是否心跳加速？是否展示了角色成长？",
            "red_flag": "高潮没有情感浓度，纯动作堆砌",
            "example": "警察局门口，李牧与黑衣人正面交锋，在妹妹的证词帮助下反杀。",
        },
        {
            "beat": 8, "name": "悬念留钩",
            "ratio": (0.92, 1.00),
            "goal": "结尾制造新悬念/新问题，驱动翻页",
            "check": "读者是否想知道'接下来呢'？钩子是否具体（非'更大的挑战还在后面'）？",
            "red_flag": "总结式结尾（'他终于明白了...'），无具体悬念",
            "example": "黑衣人倒下时，手机响了。来电显示：妈妈。",
        },
    ]

    # === 反直觉追问法 ===
    COUNTER_INTUITIVE_QUESTIONS = [
        {
            "id": "q1",
            "question": "本章最想让读者意外的是什么？",
            "guide": "每章至少一个读者没想到但合理的展开。可以是角色行为、情节走向、信息揭露。",
            "anti_pattern": "读者看3段就能猜到结局 → 需要插入反直觉元素",
        },
        {
            "id": "q2",
            "question": "读者读完本章应该有什么情绪？",
            "guide": "明确一种主导情绪+一种次情绪。如：紧张(70%)+好奇(30%)。检查每段是否服务于目标情绪。",
            "anti_pattern": "全章情绪单一无波动 → 需要情绪曲线设计",
        },
        {
            "id": "q3",
            "question": "本章推进了谁的成长弧光？",
            "guide": "每章至少推进一个角色的成长。即使配角，也要有状态变化（从A到B）。",
            "anti_pattern": "所有角色状态无变化 → 本章可删",
        },
    ]

    # === 升番逻辑 ===
    ESCALATION_LEVELS = [
        {
            "level": 1,
            "name": "基础揭示",
            "description": "揭示表层信息：角色身份、事件经过、世界规则的基本层面",
            "reader_response": "原来如此。",
            "example": "发现黑衣人来自某个组织。",
        },
        {
            "level": 2,
            "name": "进阶揭示",
            "description": "揭示深层关联：不同信息之间的联系、隐藏的动机、暗线交汇",
            "reader_response": "竟然是这样！",
            "example": "黑衣人组织就是当年害死父亲的同一伙人。",
        },
        {
            "level": 3,
            "name": "出乎意料",
            "description": "颠覆性揭示：彻底反转之前认知，但回头看有完整伏笔支撑",
            "reader_response": "天哪，我从没想过会是这样！但回头看都对得上。",
            "example": "组织首领正是李牧失散多年的哥哥——他一直以另一种身份保护妹妹。",
        },
    ]

    ESCALATION_SCHEDULE = {
        "前3章":  {"min_level": 1, "max_level": 1, "note": "建立世界观，只做基础揭示"},
        "4-10章":  {"min_level": 1, "max_level": 2, "note": "开始铺设进阶线索"},
        "11-30章": {"min_level": 1, "max_level": 3, "note": "第一次大反转"},
        "31-60章": {"min_level": 2, "max_level": 3, "note": "进阶揭示为主，铺垫最终反转"},
        "60章+":   {"min_level": 2, "max_level": 3, "note": "密集揭示和终极反转"},
    }

    # === 情绪生理反应置换表 ===
    EMOTION_PHYSICAL_MAP = {
        "愤怒": {
            "强度1": ["呼吸变重", "握紧拳头", "咬紧牙关"],
            "强度2": ["手背青筋暴起", "一拳砸在桌上", "声音压得很低但每个字都在抖"],
            "强度3": ["眼前发黑", "砸碎了手边的东西", "浑身发抖说不出话"],
            "禁用写法": ["他很生气", "他感到愤怒", "他的怒火在燃烧"],
        },
        "恐惧": {
            "强度1": ["后背发凉", "手心出汗", "下意识后退半步"],
            "强度2": ["牙齿打颤", "腿发软", "声音变了调"],
            "强度3": ["动弹不得", "心脏像要从嗓子眼跳出来", "大脑一片空白"],
            "禁用写法": ["他很害怕", "恐惧笼罩了他", "他感到一阵恐惧"],
        },
        "悲伤": {
            "强度1": ["喉咙发紧", "眼眶发酸", "沉默了很久"],
            "强度2": ["眼泪止不住地流", "肩膀在抖", "攥紧了衣角"],
            "强度3": ["蹲在地上嚎啕大哭", "像被抽空了所有力气", "一拳一拳砸着地面"],
            "禁用写法": ["他很悲伤", "悲伤涌上心头", "他感到难过"],
        },
        "紧张": {
            "强度1": ["手心出汗", "反复检查", "频繁看时间"],
            "强度2": ["呼吸急促", "手指在桌上敲个不停", "说话语速变快"],
            "强度3": ["胃部痉挛", "额头全是冷汗", "手抖得拿不住东西"],
            "禁用写法": ["他很紧张", "气氛很紧张", "紧张感弥漫"],
        },
        "放松": {
            "强度1": ["肩膀垮下来", "长出一口气", "靠在了椅背上"],
            "强度2": ["嘴角不自觉上扬", "伸了个懒腰", "闭上眼睛养神"],
            "强度3": ["笑出了声", "瘫在沙发上", "第一次睡得这么沉"],
            "禁用写法": ["他放松下来", "他终于放松了", "他感到很放松"],
        },
        "惊讶": {
            "强度1": ["愣住了", "眉毛一挑", "手上动作顿了一下"],
            "强度2": ["嘴巴微微张开", "眼睛瞪大", "倒退一步"],
            "强度3": ["整个人僵在原地", "茶水洒了一身都没察觉", "手机掉在了地上"],
            "禁用写法": ["他很惊讶", "他感到惊讶", "惊讶的表情出现在脸上"],
        },
        "厌恶": {
            "强度1": ["皱起眉头", "别过脸去", "用手扇了扇空气"],
            "强度2": ["捂住鼻子", "胃里一阵翻涌", "退后了好几步"],
            "强度3": ["干呕", "一脚踢开", "像看到脏东西一样避开"],
            "禁用写法": ["他很厌恶", "他感到厌恶", "厌恶之情溢于言表"],
        },
        "期待": {
            "强度1": ["眼神发亮", "不自觉搓了搓手", "嘴角带着笑"],
            "强度2": ["坐立不安", "隔几分钟就看一眼门口", "手指在腿上敲着节拍"],
            "强度3": ["一整夜没睡着", "提前两个小时就到了", "心跳快得像擂鼓"],
            "禁用写法": ["他很期待", "他充满期待", "期待的心情"],
        },
    }

    # ====== 公共 API ======

    def get_eight_beat_guide(self, chapter: int) -> List[Dict]:
        """获取八段式章节结构指导"""
        return [
            {
                "beat": b["beat"],
                "name": b["name"],
                "ratio_range": f"{int(b['ratio'][0]*100)}%-{int(b['ratio'][1]*100)}%",
                "goal": b["goal"],
                "check": b["check"],
                "red_flag": b["red_flag"],
            }
            for b in self.EIGHT_BEAT_STRUCTURE
        ]

    def get_eight_beat_checklist(self, chapter: int) -> List[str]:
        """获取八段式检查清单"""
        return [
            f"[第{b['beat']}拍] {b['name']}: {b['goal']} — 红线: {b['red_flag']}"
            for b in self.EIGHT_BEAT_STRUCTURE
        ]

    def analyze_beat_coverage(self, text: str, chapter: int) -> Dict[str, Any]:
        """分析正文对八段式的覆盖情况（基于字数比例估算）"""
        total_chars = len(text)
        if total_chars < 100:
            return {"verdict": "文本太短，无法分析", "beats_covered": 0, "total_beats": 8}

        covered = 0
        beat_details = []
        for b in self.EIGHT_BEAT_STRUCTURE:
            start_pos = int(b["ratio"][0] * total_chars)
            end_pos = int(b["ratio"][1] * total_chars)
            segment = text[start_pos:end_pos] if end_pos <= total_chars else text[start_pos:]
            has_content = len(segment.strip()) > 50
            if has_content:
                covered += 1
            beat_details.append({
                "beat": b["beat"],
                "name": b["name"],
                "position": f"{start_pos}-{end_pos}",
                "chars_in_segment": len(segment.strip()),
                "covered": has_content,
            })

        return {
            "verdict": f"覆盖 {covered}/8 拍" + (" ✅" if covered >= 6 else " ⚠️"),
            "beats_covered": covered,
            "total_beats": 8,
            "details": beat_details,
            "missing_beats": [
                d["name"] for d in beat_details if not d["covered"]
            ],
        }

    # === 反直觉追问法 ===

    def get_counter_intuitive_questions(self) -> List[Dict]:
        """获取反直觉三问"""
        return self.COUNTER_INTUITIVE_QUESTIONS

    def ask_counter_intuitive(self, chapter_plan: Dict = None) -> Dict[str, str]:
        """执行反直觉追问（返回三个问题+建议答案框架）"""
        result = {}
        for q in self.COUNTER_INTUITIVE_QUESTIONS:
            result[q["id"]] = {
                "question": q["question"],
                "guide": q["guide"],
                "anti_pattern": q["anti_pattern"],
                "answer": "",  # 由调用方（Agent/LLM）填充
            }
        return result

    # === 升番逻辑 ===

    def get_escalation_levels(self) -> List[Dict]:
        """获取升番三级"""
        return self.ESCALATION_LEVELS

    def get_escalation_requirement(self, chapter: int) -> Dict:
        """根据当前章节数获取升番要求"""
        if chapter <= 3:
            zone = "前3章"
        elif chapter <= 10:
            zone = "4-10章"
        elif chapter <= 30:
            zone = "11-30章"
        elif chapter <= 60:
            zone = "31-60章"
        else:
            zone = "60章+"

        req = self.ESCALATION_SCHEDULE.get(zone, self.ESCALATION_SCHEDULE["前3章"])
        return {
            "chapter": chapter,
            "zone": zone,
            "min_level": req["min_level"],
            "max_level": req["max_level"],
            "note": req["note"],
            "level_names": [
                self.ESCALATION_LEVELS[i - 1]["name"]
                for i in range(req["min_level"], req["max_level"] + 1)
            ],
        }

    def analyze_escalation_in_text(self, text: str, chapter: int) -> Dict[str, Any]:
        """分析正文中的信息揭露层次（基于关键词检测）"""
        level_keywords = {
            1: ["发现", "原来", "得知", "了解到", "确认", "查明"],
            2: ["竟然", "居然是", "没想到", "隐藏的", "背后", "真相", "关联"],
            3: ["反转", "颠覆", "一切都是", "从来不是", "真正的", "从一开始"],
        }

        found_levels = set()
        details = {}
        for level, keywords in level_keywords.items():
            found = []
            for kw in keywords:
                if kw in text:
                    found.append(kw)
            if found:
                found_levels.add(level)
                details[f"level{level}"] = {"found_keywords": found, "count": sum(text.count(kw) for kw in found)}

        req = self.get_escalation_requirement(chapter)
        min_ok = min(found_levels) >= req["min_level"] if found_levels else False
        max_ok = max(found_levels) <= req["max_level"] if found_levels else True  # 没有发现=不超标

        issues = []
        if not min_ok:
            issues.append("缺少基础揭示(level1)")
        if found_levels and not max_ok:
            issues.append(f"过早出现高级揭示(level{max(found_levels)})，此时应为level{req['max_level']}以内")

        return {
            "found_levels": sorted(found_levels),
            "required_min": req["min_level"],
            "required_max": req["max_level"],
            "details": details,
            "verdict": "合格" if not issues else "需调整",
            "issues": issues,
        }

    # === 情绪生理反应置换表 ===

    def get_emotion_physical_map(self) -> Dict[str, Dict]:
        """获取完整情绪生理反应置换表"""
        return self.EMOTION_PHYSICAL_MAP

    def translate_emotion(self, emotion: str, intensity: int = 1) -> Dict:
        """将抽象情绪词翻译为具体生理反应"""
        emotion = emotion.strip()
        # 模糊匹配
        for key in self.EMOTION_PHYSICAL_MAP:
            if key in emotion or emotion in key:
                intensity_key = f"强度{min(max(1, intensity), 3)}"
                alternatives = self.EMOTION_PHYSICAL_MAP[key].get(intensity_key, [])
                forbidden = self.EMOTION_PHYSICAL_MAP[key].get("禁用写法", [])
                return {
                    "emotion": key,
                    "intensity": intensity,
                    "alternatives": alternatives,
                    "forbidden_patterns": forbidden,
                }
        return {
            "emotion": emotion,
            "intensity": intensity,
            "alternatives": ["[未匹配到具体反应，建议：用动作/环境/生理反应替代]"],
            "forbidden_patterns": [f"他很{emotion}", f"他感到{emotion}"],
        }

    def detect_tell_emotions(self, text: str) -> List[Dict]:
        """检测正文中直接告知情绪的地方（违反Show-Not-Tell）"""
        import re
        tell_patterns = [
            (r"他很(生气|愤怒|害怕|恐惧|紧张|悲伤|难过|高兴|开心|兴奋|惊讶|厌恶|期待|失望|焦虑|烦躁|得意)", "直接告知情绪"),
            (r"他感到(一阵)?(生气|愤怒|害怕|恐惧|紧张|悲伤|难过|高兴|开心|兴奋|惊讶|厌恶|期待|失望|焦虑|烦躁|得意|温暖|寒意)", "感到+情绪"),
            (r"她觉得(很)?(生气|愤怒|害怕|恐惧|紧张|悲伤|难过|高兴|开心|兴奋|惊讶|厌恶|期待|失望|焦虑|烦躁|得意)", "她觉得+情绪"),
            (r"(愤怒|恐惧|悲伤|紧张|惊讶|厌恶|期待)的(情绪|感觉|心情|表情|眼神|语气)", "情绪修饰词"),
        ]

        issues = []
        for pattern, category in tell_patterns:
            for match in re.finditer(pattern, text):
                pos = match.start()
                context_start = max(0, pos - 30)
                context_end = min(len(text), pos + 30)
                issues.append({
                    "type": "tell_emotion",
                    "category": category,
                    "match": match.group(0),
                    "position": pos,
                    "context": text[context_start:context_end],
                    "suggestion": self._suggest_physical(text[context_start:context_end]),
                })

        return issues

    def _suggest_physical(self, context: str) -> str:
        """根据上下文语境建议生理反应替代方案"""
        for emotion, levels in self.EMOTION_PHYSICAL_MAP.items():
            if emotion in context:
                return f"建议用动作替代：{levels['强度2'][:2]}"
        return "建议用具体动作替代抽象情绪描述"

    def inject_into_prompt(self, chapter: int, genre: str = "") -> str:
        """生成注入到 LLM prompt 的叙事结构指导文本"""
        parts = []

        # 八段式
        parts.append("【八段式章节结构】")
        for b in self.EIGHT_BEAT_STRUCTURE:
            parts.append(f"  第{b['beat']}拍「{b['name']}」({int(b['ratio'][0]*100)}%-{int(b['ratio'][1]*100)}%): {b['goal']}")
        parts.append("")

        # 反直觉追问
        parts.append("【反直觉追问（写前自查）】")
        for q in self.COUNTER_INTUITIVE_QUESTIONS:
            parts.append(f"  {q['question']}")
        parts.append("")

        # 升番逻辑
        req = self.get_escalation_requirement(chapter)
        parts.append(f"【升番逻辑】本章要求: {req['note']}（{'→'.join(req['level_names'])}）")
        parts.append("")

        # 情绪置换
        parts.append("【情绪生理反应置换】")
        for emotion, levels in self.EMOTION_PHYSICAL_MAP.items():
            examples = levels["强度2"][:2]
            parts.append(f"  {emotion}: " + " / ".join(examples))
        parts.append("")

        return "\n".join(parts)

    # === 兼容 Engine 接口 ===

    def analyze(self, text: str, chapter: int = 1, **kwargs) -> Dict[str, Any]:
        """统一 analyze 接口（兼容 registry 规范）"""
        beat_result = self.analyze_beat_coverage(text, chapter)
        escalation_result = self.analyze_escalation_in_text(text, chapter)
        tell_emotions = self.detect_tell_emotions(text)

        issues = []
        if beat_result["beats_covered"] < 6:
            issues.append(f"八段式覆盖不足: {beat_result['beats_covered']}/8")
        if escalation_result["verdict"] != "合格":
            issues.extend(escalation_result.get("issues", []))
        if len(tell_emotions) > 3:
            issues.append(f"直接告知情绪 {len(tell_emotions)} 处，建议用生理反应替代")

        return {
            "verdict": "合格" if not issues else "需优化",
            "beat_coverage": beat_result,
            "escalation": escalation_result,
            "tell_emotions_count": len(tell_emotions),
            "tell_emotions": tell_emotions[:5],
            "issues": issues,
        }
