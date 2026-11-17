#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""逻辑引擎 — 规则推理/一致性校验/设定检查"""
import re

from .engine_base import EngineBase

# 预编译正则
class LogicEngine(EngineBase):
    """基于规则的逻辑校验 + 设定一致性"""

    engine_name = "logic"
    engine_tags = ["逻辑", "一致性"]

    def analyze(self, text, **kwargs):
        issues = []
        for method in [self.self_check_logic, self.check_coincidence, self.check_show_vs_tell, self.check_causal_chain]:
            try:
                r = method(text)
                if r: issues.extend(r if isinstance(r, list) else [str(r)])
            except Exception:
                pass
        return issues

    CONTRADICTION_PATTERNS = [
        ("死了", "活着"), ("死了", "回来"), ("死了", "复活"),
        ("昏迷", "醒来"), ("离开", "回到"),
        ("失去", "拥有"), ("失败", "成功"),
        ("被杀", "反杀"), ("封印", "破封"),
    ]

    def verify(self, data):
        issues = []
        if isinstance(data, str):
            for a, b in self.CONTRADICTION_PATTERNS:
                if a in data and b in data:
                    pos_a = data.index(a)
                    pos_b = data.index(b)
                    if abs(pos_a - pos_b) < 200:
                        issues.append("可能的逻辑矛盾: " + a + "附近出现" + b)
        return issues

    def validate_state(self, state):
        if not state:
            return ["状态为空"]
        issues = []
        chars = state.get("characters", {})
        for name, info in chars.items():
            loc = info.get("location", "")
            age = info.get("age", 0)
            if isinstance(age, (int, float)) and age > 200:
                issues.append(name + "年龄" + str(age) + "异常")
        return issues

    # === 设定一致性 (源自consistency-system.md) ===
    def check_show_vs_tell(self, text):
        issues = []
        patterns = ["在这个世界里", "这个世界有", "传说", "众所周知", "据记载"]
        for p in patterns:
            if p in text:
                issues.append("设定通过说明式展示 - 建议改为行动/对话展示")
                break
        return issues

    def check_power_balance(self, power_system):
        issues = []
        if not power_system:
            return ["无力量体系"]
        cost = power_system.get("cost", 0)
        growth = power_system.get("growth", 0)
        diversity = power_system.get("diversity", 0)
        total = cost + growth + diversity
        if total == 0:
            return ["力量体系未量化: 需定义cost/growth/diversity(1-10)"]
        if cost / total < 0.15:
            issues.append("消耗偏弱 - 可能导致体系失衡")
        if growth / total < 0.15:
            issues.append("成长偏弱 - 可能导致升级无感")
        if diversity / total < 0.15:
            issues.append("多样性偏弱 - 可能导致体系单调")
        return issues

    def extract_settings(self, text):
        changes = []
        pats = [
            (r"[练修][气仙].{0,4}(?:金丹|元婴|化神|筑基)", "等级"),
            (r".{1,6}(?:城|村|宫|谷|洞|山|岛)", "地点"),
        ]
        for pat, cat in pats:
            matches = re.findall(pat, text)
            for m in matches[:3]:
                changes.append({"cat": cat, "content": m})
        return changes

    # === 小说漏洞自检 (源自self-check-rules.md) ===

    def self_check_logic(self, text):
        """逻辑漏洞: 因果链/时间线/空间/信息差"""
        issues = []
        if not text:
            return ["无文本"]
        # 因果跳跃检测
        if "然后" in text and "因为" not in text:
            if text.count("然后") > 3:
                issues.append("因果链不完整 - 过多'然后'连接,建议补充因果关系")
        # 时间线矛盾检测
        time_words = ["昨天", "今天", "明天", "三天前", "三天后"]
        found_times = [w for w in time_words if w in text]
        if len(found_times) >= 3:
            issues.append("时间线检查:确认时间词使用顺序合理")
        # 空间跳跃检测
        locs = re.findall(r".{1,4}(?:城|村|宫|谷|洞|山|岛|殿)", text)
        if len(set(locs)) >= 3 and len(text) < 1000:
            issues.append(f"短文本内出现{len(set(locs))}个地点 - 确认非空间跳跃")
        return issues

    def self_check_setting(self, text, settings=None):
        """设定漏洞: 力量体系/规则一致性"""
        issues = []
        # 力量等级矛盾检测
        tiers = re.findall(r"(炼气|筑基|金丹|元婴|化神|大乘)", text)
        if tiers:
            order = ["炼气", "筑基", "金丹", "元婴", "化神", "大乘"]
            for i, t in enumerate(tiers):
                if t in order and i > 0:
                    prev = tiers[i-1]
                    if prev in order and t in order:
                        if order.index(t) < order.index(prev) and abs(order.index(t) - order.index(prev)) > 1:
                            issues.append(f"力量等级矛盾: {prev}->{t}降级")
        return issues

    def self_check_character(self, data):
        """角色漏洞: 性格一致/行为动机"""
        issues = []
        if not isinstance(data, dict):
            return []
        chars = data.get("characters", {})
        for name, info in chars.items():
            if isinstance(info, dict):
                motivation = info.get("motivation", "")
                action = info.get("last_action", "")
                if motivation and action:
                    if not any(w in action for w in motivation.split()):
                        pass  # 简化版不深入检查
        return issues

    def self_check_structure(self, text):
        """结构漏洞: 节奏/章节定位"""
        issues = []
        paras = text.split(chr(10))
        if len(paras) > 30:
            issues.append(f"段落数{len(paras)}偏多 - 建议单章10-20段")
        if len(paras) < 3:
            issues.append("段落数过少 - 建议适当分段")
        return issues
    # === 巧合变因果检查 (源自narrative-theory.md) ===
    def check_coincidence(self, text):
        """检测过度依赖巧合代替因果"""

# 预编译正则
        issues = []
        coincidence_markers = ["正好", "恰巧", "刚好", "碰巧", "刚好这时"]
        count = sum(text.count(w) for w in coincidence_markers)
        if count > 2:
            issues.append(f"巧合词出现{count}次 - 建议用因果铺垫替代'正好/恰巧/刚好'")
        # 检测无前因的突然事件
        sudden_markers = ["突然", "忽然", "猛地"]
        sudden_count = sum(text.count(w) for w in sudden_markers)
        if sudden_count > 4:
            issues.append(f"突然性事件{sudden_count}次 - 建议给重要事件前置铺垫")
        return issues
    # === 因果链密度 (源自05-story-workshop: 如果...那么检查) ===
    def check_causal_chain(self, text):
        """因果链密度: 如果...那么类条件句数量"""

# 预编译正则
        if not text or len(text) < 200:
            return []
        causal_markers = ["因为", "所以", "因此", "于是", "结果", "导致",
                          "引发", "带来", "从而", "为了", "基于"]
        count = sum(text.count(w) for w in causal_markers)
        cn_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
        density = count / max(cn_chars / 1000, 1)
        if density < 3 and cn_chars > 1000:
            return [f"因果链密度偏低({density:.1f}/千字) - 建议加强因果关系"]
        return []

    # === 设定冲突检测 (源自15-cross-genre-creation) ===
    def check_setting_conflict(self, types, text):
        """类型杂交的设定冲突检测"""
        if len(types) < 2:
            return []
        issues = []
        conflict_pairs = [("理性", "魔法"), ("科学", "修仙"), ("逻辑", "直觉")]
        for a, b in conflict_pairs:
            if any(a in str(t) for t in types) and any(b in str(t) for t in types):
                if a in text and b in text:
                    issues.append(f"类型矛盾: {a}与{b}并置 - 确认是否刻意为之")
        return issues
    # === OOC光谱检测 (源自01-fanfic-culture.md) ===
    @staticmethod
    def check_ooc(character_actions):
        """角色OOC光谱分析: 严格忠实→扩展→AU"""
        if not character_actions:
            return []
        issues = []
        for action in character_actions[:10]:
            if isinstance(action, dict):
                char = action.get("character", "")
                expected = action.get("expected", "")
                actual = action.get("actual", "")
                if expected and actual and expected != actual:
                    distance = abs(len(actual) - len(expected)) / max(len(expected), 1)
                    if distance > 0.5:
                        issues.append(f"OOC风险: {char}预期'{expected[:10]}'实际'{actual[:10]}'")
        return issues
    # === 跨文化DNA保留检测 (源自03-cross-culture-adap.md) ===
    @staticmethod
    def check_cross_culture_dna(text, core_dna=None):
        if core_dna is None:
            core_dna = []
        """检测改编时是否保留了核心DNA"""
        if not core_dna:
            return {"verdict": "需定义核心DNA要素"}
        found = [dna for dna in core_dna if dna in text]
        missing = [dna for dna in core_dna if dna not in found]
        return {
            "found": found, "missing": missing,
            "preservation": round(len(found) / len(core_dna) * 100),
            "verdict": "核心DNA保留" if len(found) >= len(core_dna) * 0.5 else "核心DNA丢失风险",
        }