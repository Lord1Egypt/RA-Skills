#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
soul_skill.py — SoulSkill 角色灵魂系统

灵感来源: QMAI 的 SoulSkill 角色灵魂系统（60+ 角色视角）
核心思想: 为角色注入独特的认知模型、表达方式、价值观，防止所有角色共用一种"标准网文腔"。

包含 4 层角色灵魂:
  L1: 核心心智模型 — 角色如何理解世界
  L2: 表达DNA — 角色的语言指纹（词汇/句式/语气）
  L3: 决策启发式 — 角色做决定的方式
  L4: 价值观与反模式 — 角色的底线和禁区

用法:
  ss = SoulSkill()
  profile = ss.get_profile("老兵")  # 获取角色灵魂档案
  profile.to_prompt()               # 转换为注入 prompt 的文本
  ss.inject_into_context(context, ["老兵", "商人"])  # 批量注入
"""

import json, logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

_log = logging.getLogger("soul_skill")


@dataclass
class SoulProfile:
    """角色灵魂档案"""
    archetype: str              # 原型名
    category: str = "general"   # 分类: warrior/scholar/merchant/ruler/artist/commoner/antihero
    core_belief: str = ""       # 核心信念（一句话）
    mental_model: str = ""      # 心智模型：如何理解世界
    decision_heuristic: str = "" # 决策启发式：如何做决定
    voice_dna: str = ""         # 表达DNA：说话特征
    vocabulary: List[str] = field(default_factory=list)    # 常用词汇
    avoid_words: List[str] = field(default_factory=list)   # 避免的词汇
    values: List[str] = field(default_factory=list)        # 核心价值观
    anti_patterns: List[str] = field(default_factory=list) # 反模式（绝不做的事）
    emotional_range: str = ""   # 情绪范围
    typical_reactions: Dict[str, str] = field(default_factory=dict)  # 典型反应
    pov_filter: str = ""        # 视角滤镜：观察什么、忽略什么

    def to_prompt(self) -> str:
        """转换为注入 prompt 的文本"""
        lines = [f"[角色灵魂: {self.archetype}]"]
        if self.core_belief:
            lines.append(f"核心信念: {self.core_belief}")
        if self.mental_model:
            lines.append(f"思维模式: {self.mental_model}")
        if self.decision_heuristic:
            lines.append(f"决策方式: {self.decision_heuristic}")
        if self.voice_dna:
            lines.append(f"说话特征: {self.voice_dna}")
        if self.vocabulary:
            lines.append(f"常用词: {', '.join(self.vocabulary[:8])}")
        if self.avoid_words:
            lines.append(f"避免: {', '.join(self.avoid_words[:5])}")
        if self.emotional_range:
            lines.append(f"情绪范围: {self.emotional_range}")
        if self.pov_filter:
            lines.append(f"视角滤镜: {self.pov_filter}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "archetype": self.archetype,
            "category": self.category,
            "core_belief": self.core_belief,
            "mental_model": self.mental_model,
            "voice_dna": self.voice_dna,
            "vocabulary": self.vocabulary,
            "values": self.values,
            "anti_patterns": self.anti_patterns,
        }


class SoulSkill:
    """角色灵魂系统"""

    # ── 20 个核心角色原型 ──
    PROFILES: Dict[str, SoulProfile] = {
        # === 战斗/行动类 ===
        "老兵": SoulProfile(
            archetype="老兵",
            category="warrior",
            core_belief="活着就是最大的胜利",
            mental_model="世界是危险的，任何时候都要留后手。信任是要用命去验证的。",
            decision_heuristic="直觉优先。战斗经验告诉他，想太多会死。先动手再思考。",
            voice_dna="话少，用词粗糙，习惯用短句。不说话时比说话时更吓人。",
            vocabulary=["操", "妈的", "干", "走", "撤", "盯着", "小心", "命", "刀", "血"],
            avoid_words=["也许", "可能", "大概", "或许", "优雅", "精致", "美妙"],
            values=["生存", "战友", "承诺"],
            anti_patterns=["背叛战友", "临阵脱逃", "对平民下手"],
            emotional_range="压抑→爆发，无中间状态",
            typical_reactions={"威胁": "先下手", "赞美": "警惕", "告别": "沉默点头"},
            pov_filter="注意威胁/武器/出口/人数/地形。忽略装饰/天气/无关人员。",
        ),
        "杀手": SoulProfile(
            archetype="杀手",
            category="warrior",
            core_belief="效率高于一切",
            mental_model="每个目标都是一道题，找出最优解法。感情是干扰项。",
            decision_heuristic="冷静计算。评估风险/收益/暴露可能，选最优路径。",
            voice_dna="极简，不带情绪。需要时才说话，说完就闭嘴。",
            vocabulary=["目标", "清除", "确认", "撤离", "备用", "方案B"],
            avoid_words=["对不起", "谢谢", "爱", "恨", "喜欢", "讨厌"],
            values=["效率", "契约", "专业"],
            anti_patterns=["感情用事", "留下痕迹", "违背契约"],
            emotional_range="几乎平坦，偶有微波动",
            pov_filter="注意出口/监控/武器/人员流动。忽略闲聊/情感/无关信息。",
        ),
        "侠客": SoulProfile(
            archetype="侠客",
            category="warrior",
            core_belief="路见不平，拔刀相助",
            mental_model="世界上有对错。强者欺负弱者时，总得有人站出来。",
            decision_heuristic="道德直觉。先判断对错，再想后果。",
            voice_dna="豪爽直接，不拐弯抹角。喜欢用反问。",
            vocabulary=["公道", "欺负", "看不过去", "来", "战", "承让", "得罪"],
            avoid_words=["算了", "不管了", "忍忍", "假装", "妥协"],
            values=["正义", "自由", "尊严"],
            anti_patterns=["见死不救", "欺软怕硬", "背叛朋友"],
            emotional_range="外放型，喜怒形于色",
            pov_filter="注意不公平/弱者被欺/恃强凌弱。忽略权势/利益算计。",
        ),

        # === 智慧/学者类 ===
        "谋士": SoulProfile(
            archetype="谋士",
            category="scholar",
            core_belief="上兵伐谋，其次伐交，其次伐兵",
            mental_model="一切皆棋局。每个人都是棋子，包括自己。多想三步。",
            decision_heuristic="系统分析。列出所有可能→评估概率→选胜率最高的。",
            voice_dna="文雅但犀利，常用比喻和典故。说话留三分。",
            vocabulary=["局势", "权衡", "变数", "后手", "布局", "收网", "棋子"],
            avoid_words=["不知道", "随便", "差不多", "也许吧", "碰运气"],
            values=["智慧", "大局", "长远"],
            anti_patterns=["冲动决策", "信息不全就行动", "暴露底牌"],
            emotional_range="内敛，偶有赞赏或失望的微表情",
            pov_filter="注意信息/动机/关系/漏洞。忽略表面现象/情绪化表达。",
        ),
        "学者": SoulProfile(
            archetype="学者",
            category="scholar",
            core_belief="知识改变一切",
            mental_model="世界是可理解的。任何现象背后都有规律，找到规律就能预测。",
            decision_heuristic="数据驱动。收集足够信息→建立模型→验证→决策。",
            voice_dna="严谨精确，习惯用术语。说话像写论文。",
            vocabulary=["根据", "数据", "分析", "结论", "假设", "验证", "可能", "概率"],
            avoid_words=["一定", "绝对", "肯定", "毫无疑问", "显而易见"],
            values=["真理", "知识", "逻辑"],
            anti_patterns=["迷信权威", "跳过验证", "感情用事"],
            emotional_range="理性主导，对愚蠢缺乏耐心",
            pov_filter="注意数据/规律/异常/逻辑漏洞。忽略情绪/直觉/个人感受。",
        ),
        "智者": SoulProfile(
            archetype="智者",
            category="scholar",
            core_belief="大道至简",
            mental_model="万物有周期。盛极必衰，否极泰来。顺势而为。",
            decision_heuristic="看大势。不纠结细节，把握方向即可。",
            voice_dna="简练有禅意，常用反问和隐喻。话不多但句句有分量。",
            vocabulary=["道", "缘", "因果", "时候未到", "顺其自然", "水到渠成"],
            avoid_words=["必须", "立刻", "赶紧", "着急", "拼命"],
            values=["和谐", "智慧", "耐心"],
            anti_patterns=["逆天行事", "强求", "急功近利"],
            emotional_range="平和稳定，喜怒不形于色",
            pov_filter="注意大势/因果/时机。忽略短期波动/个人恩怨。",
        ),

        # === 商业/权力类 ===
        "商人": SoulProfile(
            archetype="商人",
            category="merchant",
            core_belief="天下没有不能做的生意",
            mental_model="一切皆有价。人情、权力、信息、时间，都是可以交易的。",
            decision_heuristic="成本收益分析。亏本的买卖不做，暴利的机会不放过。",
            voice_dna="圆滑周到，永远不说死。谈判时滴水不漏。",
            vocabulary=["价格", "利润", "成交", "定金", "风险", "回报", "合作"],
            avoid_words=["免费", "白送", "亏本", "认输", "放弃"],
            values=["利益", "信誉", "人脉"],
            anti_patterns=["亏本买卖", "得罪大客户", "不讲信用"],
            emotional_range="表面热情，内心冷静",
            pov_filter="注意利益/交易机会/风险/对手底牌。忽略道德评判/感情用事。",
        ),
        "权臣": SoulProfile(
            archetype="权臣",
            category="ruler",
            core_belief="权力是唯一真实的货币",
            mental_model="朝堂是棋盘。盟友今天的朋友是明天的敌人。永远不要相信任何人。",
            decision_heuristic="权力最大化。每一步都要增强自己的位置，削弱对手。",
            voice_dna="冠冕堂皇但暗藏机锋。表面说一套，实际想另一套。",
            vocabulary=["大局", "平衡", "考量", "暂且", "时机", "稳妥", "从长计议"],
            avoid_words=["我错了", "不知道", "随便你", "投降"],
            values=["权力", "秩序", "忠诚"],
            anti_patterns=["公开站错队", "暴露野心", "不给自己留退路"],
            emotional_range="永远不暴露真实情绪",
            pov_filter="注意权力关系/派系/利益交换/威胁。忽略情感/正义/公平。",
        ),
        "帝王": SoulProfile(
            archetype="帝王",
            category="ruler",
            core_belief="朕即天下",
            mental_model="所有人在朕面前都是臣子。朕的意志就是法律。但朕也是天下最孤独的人。",
            decision_heuristic="权衡利弊。杀伐果断，但每个决定都要考虑千秋万代。",
            voice_dna="威严不容置疑。用词正式，不解释。偶尔流露孤寂。",
            vocabulary=["朕", "准", "退下", "赐", "斩", "赏", "罚", "天下", "江山"],
            avoid_words=["对不起", "求求你", "也许", "随便"],
            values=["江山", "权威", "社稷"],
            anti_patterns=["当众示弱", "被臣子胁迫", "优柔寡断"],
            emotional_range="威严为主，偶有暴怒或孤独",
            pov_filter="注意威胁/忠诚/势力平衡。忽略个人情感/小事。",
        ),

        # === 艺术家/创造者类 ===
        "诗人": SoulProfile(
            archetype="诗人",
            category="artist",
            core_belief="美是唯一的真理",
            mental_model="世界是一首诗。每一个瞬间都值得被写成永恒。",
            decision_heuristic="情感驱动。跟着心走，理性是束缚。",
            voice_dna="优美抒情，善用比喻和意象。说话像写诗。",
            vocabulary=["风", "月", "醉", "梦", "归", "愁", "念", "天涯", "此生"],
            avoid_words=["效率", "成本", "计划", "系统", "标准", "流程"],
            values=["美", "自由", "真情"],
            anti_patterns=["为利益放弃追求", "妥协于平庸", "扼杀灵感"],
            emotional_range="敏感丰富，喜怒转换快",
            pov_filter="注意美/诗意/情感。忽略实用/效率/逻辑。",
        ),

        # === 普通人/反英雄类 ===
        "小人物": SoulProfile(
            archetype="小人物",
            category="commoner",
            core_belief="活着就好，不求大富大贵",
            mental_model="世界很大，我很小。惹不起的躲，躲不过的认。",
            decision_heuristic="安全第一。不做任何有风险的事，除非逼到绝路。",
            voice_dna="朴实接地气，带方言习惯。说话不自信，常用语气词。",
            vocabulary=["还行", "凑合", "算了", "不敢", "俺", "咱", "那啥", "拉倒"],
            avoid_words=["必须", "一定", "绝对", "命令", "原则"],
            values=["平安", "家人", "饭碗"],
            anti_patterns=["出头", "惹事", "冒险"],
            emotional_range="平淡为主，被逼急了才会爆发",
            pov_filter="注意危险/生活所需/身边人。忽略大局/权力/理想。",
        ),
        "赌徒": SoulProfile(
            archetype="赌徒",
            category="antihero",
            core_belief="人生就是一场豪赌",
            mental_model="富贵险中求。不敢赌的人永远翻不了身。",
            decision_heuristic="概率+直觉。赢面超过三成就值得博。",
            voice_dna="市井气重，说话带赌场术语。语气忽高忽低。",
            vocabulary=["博一把", "梭哈", "运气", "翻盘", "押", "开", "输了", "赢了"],
            avoid_words=["稳妥", "保险", "慢慢来", "谨慎"],
            values=["运气", "胆量", "翻身"],
            anti_patterns=["不敢下注", "犹豫不决", "认命"],
            emotional_range="大起大落，从狂喜到绝望",
            pov_filter="注意机会/风险/赔率。忽略长期规划/稳定。",
        ),
        "骗子": SoulProfile(
            archetype="骗子",
            category="antihero",
            core_belief="人都是可以被骗的，关键是用什么饵",
            mental_model="每个人都有一个弱点。找到它，你就有了钥匙。",
            decision_heuristic="看人下菜。不同的人用不同的骗法。",
            voice_dna="能说会道，永远真诚的语气。谎话比真话更可信。",
            vocabulary=["真的", "不骗你", "你想想", "机会难得", "内部消息", "兄弟"],
            avoid_words=["骗", "假", "陷阱", "圈套"],
            values=["生存", "利益", "自由"],
            anti_patterns=["说真话", "暴露底细", "对所有人用同一套"],
            emotional_range="表面丰富，内心冷漠",
            pov_filter="注意人的弱点/欲望/恐惧。忽略道德/信任/真伪。",
        ),

        # === 女性角色原型 ===
        "女强人": SoulProfile(
            archetype="女强人",
            category="ruler",
            core_belief="我不需要任何人的施舍",
            mental_model="在这个男人主导的世界，要得到尊重就得比所有人都强。",
            decision_heuristic="理性优先。感性在商场上等于自杀。",
            voice_dna="干脆利落，不用语气词。提问像审问。",
            vocabulary=["效率", "结果", "方案", "执行", "考核", "指标", "截止"],
            avoid_words=["人家", "嘛", "啦", "呀", "好不好", "帮帮忙"],
            values=["独立", "能力", "尊严"],
            anti_patterns=["示弱", "依赖他人", "感情用事"],
            emotional_range="克制，偶有脆弱但不让人看见",
            pov_filter="注意能力/效率/尊重。忽略性别偏见/无关情绪。",
        ),
        "白月光": SoulProfile(
            archetype="白月光",
            category="artist",
            core_belief="善良是这个世界上最稀缺的东西",
            mental_model="人性本善。每个人变坏都是有原因的。",
            decision_heuristic="善良优先。先想怎么帮人，再想自己。",
            voice_dna="温柔细腻，常用叠词。说话像春风。",
            vocabulary=["真好", "谢谢", "没关系", "辛苦了", "小心", "慢点"],
            avoid_words=["滚", "烦", "讨厌", "恶心", "去死"],
            values=["善良", "温暖", "希望"],
            anti_patterns=["伤害他人", "冷漠旁观", "放弃希望"],
            emotional_range="温暖为主，悲伤时安静不闹",
            pov_filter="注意美好/善良/需要帮助的人。忽略恶意/算计。",
        ),
        "疯批": SoulProfile(
            archetype="疯批",
            category="antihero",
            core_belief="既然世界对我不好，我为什么还要对它好",
            mental_model="规则是给弱者的。打破规则的人才真正活着。",
            decision_heuristic="冲动+执念。想到就做，不计后果。",
            voice_dna="阴晴不定，时而温柔时而刻薄。喜欢说反话。",
            vocabulary=["有意思", "无聊", "试试", "那又怎样", "谁在乎", "好玩"],
            avoid_words=["规矩", "应该", "正常", "理智", "冷静"],
            values=["自由", "刺激", "复仇"],
            anti_patterns=["服从", "认命", "妥协"],
            emotional_range="极端波动，从狂喜到暴怒切换极快",
            pov_filter="注意刺激/挑衅/机会。忽略后果/他人感受。",
        ),

        # === 少年/成长类 ===
        "热血少年": SoulProfile(
            archetype="热血少年",
            category="warrior",
            core_belief="只要不放弃，就没有做不到的事",
            mental_model="世界是公平的。努力就会有回报。坏人一定会被打败。",
            decision_heuristic="信念驱动。相信自己的感觉，不轻易动摇。",
            voice_dna="充满能量，感叹号多。说话直接不绕弯。",
            vocabulary=["加油", "冲", "决不放弃", "我相信", "一定能", "拼了"],
            avoid_words=["放弃", "算了", "认输", "不可能"],
            values=["友情", "努力", "胜利"],
            anti_patterns=["背叛朋友", "半途而废", "认输"],
            emotional_range="外放积极，失败时会短暂低落但很快振作",
            pov_filter="注意目标/伙伴/挑战。忽略悲观/妥协/算计。",
        ),
        "腹黑少年": SoulProfile(
            archetype="腹黑少年",
            category="antihero",
            core_belief="这个世界就是谁狠谁赢",
            mental_model="表面一套背后一套。让人以为你是无害的，才是最大的优势。",
            decision_heuristic="伪装+算计。永远不要让人看到真实的你。",
            voice_dna="人前乖巧礼貌，人后冷酷果断。语气转换自然。",
            vocabulary=["好的", "明白了", "谢谢关心", "交给我", "处理掉", "不留痕迹"],
            avoid_words=["我恨", "我要杀了", "去死", "凭什么"],
            values=["掌控", "信息", "伪装"],
            anti_patterns=["暴露真实想法", "冲动行事", "相信任何人"],
            emotional_range="表面单一，真实情绪深藏",
            pov_filter="注意信息差/可利用的人/威胁。忽略情感/信任。",
        ),
    }

    def get_profile(self, archetype: str) -> Optional[SoulProfile]:
        """获取角色灵魂档案"""
        return self.PROFILES.get(archetype)

    def get_by_category(self, category: str) -> List[SoulProfile]:
        """按分类获取角色列表"""
        return [p for p in self.PROFILES.values() if p.category == category]

    def list_all(self) -> List[str]:
        """列出所有可用原型"""
        return list(self.PROFILES.keys())

    def inject_into_prompt(self, system_prompt: str, characters: List[Dict[str, str]]) -> str:
        """将角色灵魂注入 System Prompt

        Args:
            system_prompt: 原始 System Prompt
            characters: 角色列表 [{"name": "林北", "archetype": "老兵"}, ...]

        Returns:
            注入后的 System Prompt
        """
        if not characters:
            return system_prompt

        soul_lines = ["\n\n【角色灵魂档案】"]
        for char in characters:
            profile = self.get_profile(char.get("archetype", ""))
            if profile:
                soul_lines.append(f"\n## {char['name']} ({profile.archetype})")
                soul_lines.append(f"- 思维: {profile.mental_model[:80]}")
                soul_lines.append(f"- 说话: {profile.voice_dna[:80]}")
                soul_lines.append(f"- 常用词: {', '.join(profile.vocabulary[:5])}")
                soul_lines.append(f"- 底线: {', '.join(profile.anti_patterns[:3])}")

        return system_prompt + "\n".join(soul_lines)

    def find_best_match(self, description: str) -> Optional[SoulProfile]:
        """根据描述模糊匹配最佳角色原型

        简单的关键词匹配，用于自动推荐角色原型。
        """
        desc_lower = description.lower()
        scores = {}

        keyword_map = {
            "战斗": ["warrior"], "打": ["warrior"], "武": ["warrior"],
            "兵": ["warrior"], "战": ["warrior"], "军": ["warrior"],
            "聪明": ["scholar"], "智慧": ["scholar"], "谋": ["scholar"],
            "学": ["scholar"], "书": ["scholar"], "研究": ["scholar"],
            "钱": ["merchant"], "商": ["merchant"], "买卖": ["merchant"],
            "生意": ["merchant"], "赚": ["merchant"],
            "权": ["ruler"], "官": ["ruler"], "帝": ["ruler"],
            "王": ["ruler"], "统治": ["ruler"],
            "美": ["artist"], "诗": ["artist"], "艺": ["artist"],
            "画": ["artist"], "音乐": ["artist"],
            "普通": ["commoner"], "平民": ["commoner"],
            "小人物": ["commoner"], "老实": ["commoner"],
            "坏": ["antihero"], "骗": ["antihero"], "疯": ["antihero"],
            "狠": ["antihero"], "腹黑": ["antihero"],
        }

        for keyword, categories in keyword_map.items():
            if keyword in desc_lower:
                for cat in categories:
                    scores[cat] = scores.get(cat, 0) + 1

        if not scores:
            return None

        best_cat = max(scores, key=scores.get)
        candidates = self.get_by_category(best_cat)
        return candidates[0] if candidates else None
