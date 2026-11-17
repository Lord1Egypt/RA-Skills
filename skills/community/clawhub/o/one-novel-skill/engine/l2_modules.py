#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L2 anti-AI writing modules

Architecture: detection + prompt-embedded generation control.
"ready=True" means the detection rule is ready for L3 prompt embedding.

Modules 1-4: 原生反AI本能（body law / memory trace / itch law / show-not-tell）
Modules 5-10: 展开设计文档阶段的反AI本能（anti-balance / anti-perfect / vocab temp / subtext / voice / momentum）
Modules 11-12: story-deslop + Humanizer-zh 融合检测

融合源:
  - chinese-novelist-skill (反AI本能体系)
  - story-deslop (自然文本基线 + 删除比例分级 + 替换参考)
  - Humanizer-zh (24模式检测)
"""

import re
import math


class L2Module:
    """Base class for L2 anti-AI detection modules"""

    def __init__(self, name, level, description):
        self.name = name
        self.level = level
        self.description = description
        self.ready = False  # True = ready for L3 prompt embedding

    def check(self, text):
        """Override in subclasses - return list of issues found"""
        return []

    def prompt(self):
        """Return the L3 embedding prompt for this module"""
        return ""


# ─── Module 1: Body Law (P0) — 原生 ───
class BodyLaw(L2Module):
    def __init__(self):
        super().__init__("BodyLaw", "P0",
                         "Forbidden: use abstract emotion words. Must show via non-standard body actions.")
        self.ready = True
        self.forbidden = ["感到", "觉得", "认为", "知道"]

    def check(self, text):
        issues = []
        for word in self.forbidden:
            count = text.count(word)
            if count > 0:
                issues.append(f"P0 Body Law: '{word}' x{count}")
        return issues

    def prompt(self):
        return "DO NOT use: 感到, 觉得, 认为, 知道. Show emotions through actions."


# ─── Module 2: Memory Trace (P0) — 原生 ───
class MemoryTrace(L2Module):
    def __init__(self):
        super().__init__("MemoryTrace", "P0",
                         "Character reactions must have traceable memory sources.")
        self.ready = True

    def check(self, text):
        issues = []
        triggers = ["习惯性", "下意识", "条件反射", "本能地"]
        for t in triggers:
            pos = 0
            while True:
                pos = text.find(t, pos)
                if pos == -1:
                    break
                after = text[pos+len(t):pos+len(t)+40]
                has_source = any(w in after for w in
                    ["因为", "以前", "曾经", "一直", "多年", "从小", "过去"])
                if not has_source:
                    issues.append(f"Memory Trace: {t} at pos {pos} has no source")
                    break
                pos += len(t)
        return issues

    def prompt(self):
        return "Character reactions need traceable memory/habit sources."


# ─── Module 3: Itch Law (P0) — 原生 ───
class ItchLaw(L2Module):
    def __init__(self):
        super().__init__("ItchLaw", "P0",
                         "Chapter end must raise new questions, not give old answers.")
        self.ready = True

    def check(self, text):
        issues = []
        endings = ["他终于明白了", "她终于懂了",
                   "就这样结束了", "一切归于平静",
                   "总算", "终于告一段落"]
        for e in endings:
            if e in text[-200:]:
                issues.append(f"Itch Law: old answer ending '{e}'")
        return issues

    def prompt(self):
        return "Chapter end must raise NEW questions, not resolve old ones."


# ─── Module 4: Show Not Tell (P0) — 原生 ───
class ShowNotTell(L2Module):
    def __init__(self):
        super().__init__("ShowNotTell", "P0",
                         "Forbid direct evaluation. Use three concrete details instead of one conclusion.")
        self.ready = True

    def check(self, text):
        issues = []
        patterns = [
            (r"他是\w+的", "direct eval: he is XX"),
            (r"显得很\w+", "shows very XX"),
            (r"看起来很\w+", "looks very XX"),
        ]
        for pat, hint in patterns:
            if re.search(pat, text):
                issues.append(f"ShowNotTell: {hint}")
                break
        return issues

    def prompt(self):
        return "DO NOT say someone IS something. Show through actions and details."


# ─── Module 5: Anti-Balance (P1) — 新: 反平衡 ───
# 高潮段落字数密度 x3，低潮段落 /3；禁止连续3段同一情感色调
# 参考: one-novel-skill 原设计文档 + story-deslop 节奏控制
class AntiBalance(L2Module):
    def __init__(self):
        super().__init__("AntiBalance", "P1",
                         "High-tension paragraphs need 3x word density; low-tension needs /3. No 3 consecutive same-emotion paragraphs.")
        self.ready = True

    def check(self, text):
        issues = []
        paras = [p.strip() for p in text.split('\n') if len(p.strip()) > 20]
        if len(paras) < 3:
            return issues

        # 检测段落字数方差（过度均匀 = AI味）
        lengths = [len(self._cn_only(p)) for p in paras]
        if lengths:
            avg = sum(lengths) / len(lengths)
            variance = sum((x - avg) ** 2 for x in lengths) / len(lengths)
            std = math.sqrt(variance)
            # 方差过小 = 段落长度均匀 = AI特征
            if std < avg * 0.25:
                issues.append(f"P1 AntiBalance: 段落方差过小 std={std:.0f} (avg={avg:.0f}), 段落长度过于均匀")

        # 检测连续相似句式
        same_structure = 0
        prev_start = ""
        for p in paras[:30]:
            first_chars = self._cn_only(p[:12])
            if first_chars and prev_start and first_chars[:4] == prev_start[:4]:
                same_structure += 1
            else:
                same_structure = 0
            prev_start = first_chars
            if same_structure >= 3:
                issues.append("P1 AntiBalance: 连续3+段以相同结构开头")
                break
        return issues

    def _cn_only(self, t):
        return ''.join(c for c in t if '\u4e00' <= c <= '\u9fff')

    def prompt(self):
        return "Vary paragraph density: high-tension scenes use short dense paragraphs; low-tension use loose. Avoid 3 consecutive same-structure paragraphs."


# ─── Module 6: Anti-Perfect (P2) — 新: 反完美 ───
# 对话不准说完所有信息，允许答非所问，允许无明显功能的描写
class AntiPerfect(L2Module):
    def __init__(self):
        super().__init__("AntiPerfect", "P2",
                         "Dialog should not convey all information. Allow non-sequiturs and non-functional descriptions.")
        self.ready = True

    def check(self, text):
        issues = []
        # 检测对话是否过度"完整"（连续问答都对得上）
        dialog_lines = re.findall(r'[「「][^」」]+[」」]|[""][^""]+[""]', text)
        if len(dialog_lines) >= 6:
            # 检查QA对是否过于完整
            consecutive_full = 0
            for line in dialog_lines[:min(20, len(dialog_lines))]:
                content = line.strip('「」""')
                if len(content) > 20:  # 过长对话
                    consecutive_full += 1
                else:
                    consecutive_full = 0
                if consecutive_full >= 3:
                    issues.append("P2 AntiPerfect: 连续3+对话过长(>20字), 信息过满")
                    break

            # 检查是否有省略、停顿
            full_text = ''.join(dialog_lines)
            if '……' not in full_text and '...' not in full_text:
                issues.append("P2 AntiPerfect: 无省略号, 对话可能过于完整")

        return issues

    def prompt(self):
        return "Dialogue: allow incomplete sentences, non-sequiturs, interruptions. Not every question needs a direct answer."


# ─── Module 7: Vocab Temperature (P1) — 新: 词汇温度计 ───
# 检测AI高频词汇密度，控制词汇正式度
class VocabTemperature(L2Module):
    def __init__(self):
        super().__init__("VocabTemperature", "P1",
                         "Detect AI high-frequency vocabulary density and formality level.")
        self.ready = True
        self.ai_vocabs = [
            "此外", "至关重要", "深入探讨", "强调", "持久的",
            "增强", "培养", "获得", "突出", "相互作用",
            "复杂", "复杂性", "关键", "格局", "关键性的",
            "展示", "织锦", "证明", "宝贵的", "充满活力的",
            "深刻的", "广泛的", "显著的", "革命性的", "前所未有的",
            "此外", "与此同时", "在此背景下",
            "不容忽视", "值得关注", "不可替代",
        ]

    def check(self, text):
        issues = []
        cn_chars = self._cn_only(text)
        if not cn_chars:
            return issues
        n_cn = len(cn_chars)
        matches = []
        for word in self.ai_vocabs:
            c = text.count(word)
            if c > 0:
                matches.extend([(word, c)])
        total = sum(c for _, c in matches)
        density = total / n_cn * 1000  # 每千字中AI词汇数
        if density > 2.0:
            top = sorted(matches, key=lambda x: -x[1])[:3]
            top_str = "; ".join(f"'{w}'x{c}" for w, c in top)
            issues.append(f"P1 VocabTemperature: AI词汇密度 {density:.1f}/千字 (阈值2.0). Top: {top_str}")
        elif total >= 3:
            top = sorted(matches, key=lambda x: -x[1])[:2]
            top_str = "; ".join(f"'{w}'x{c}" for w, c in top)
            issues.append(f"P1 VocabTemperature: AI词汇命中 {total}处. {top_str}")
        return issues

    def _cn_only(self, t):
        return ''.join(c for c in t if '\u4e00' <= c <= '\u9fff')

    def prompt(self):
        return "Avoid AI overused vocabulary: 此外, 至关重要, 深入探讨, 强调, 不可忽视, 值得关注. Use simpler, more direct language."


# ─── Module 8: Subtext (P2) — 新: 潜台词检测 ───
# 对话要有未尽之意，检测是否所有对话都过于直白
class Subtext(L2Module):
    def __init__(self):
        super().__init__("Subtext", "P2",
                         "Dialogue should have subtext. Detect overly explicit conversation.")
        self.ready = True

    def check(self, text):
        issues = []
        dialog_markers = ["说道", "问道", "回答道", "解释道", "补充道", "告诉"]
        count = sum(text.count(m) for m in dialog_markers)
        cn_chars = self._cn_only(text)
        if cn_chars and count > 0:
            density = count / len(cn_chars) * 1000
            if density > 3.0:
                issues.append(f"P2 Subtext: 对话标签密度过高 {density:.1f}/千字 (阈值3.0). 多用动作替代'说道'")
        return issues

    def _cn_only(self, t):
        return ''.join(c for c in t if '\u4e00' <= c <= '\u9fff')

    def prompt(self):
        return "Use action beats instead of dialogue tags. Not every line needs 'said/asked'. Let subtext carry meaning."


# ─── Module 9: Voice (P1) — 新: 视角呼吸 ───
# 检测叙述距离是否单一（全章同一距离 = AI味）
class VoiceBreath(L2Module):
    def __init__(self):
        super().__init__("VoiceBreath", "P1",
                         "Narrative distance should change. Single distance = AI writing.")
        self.ready = True

    def check(self, text):
        issues = []
        # 检测是否过度使用"他/她"开头（全知客观视角）
        sentences = [s.strip() for s in re.split(r'[。！？\n]', text) if len(s.strip()) > 5]
        if not sentences:
            return issues
        start_he_she = sum(1 for s in sentences[:50] if re.match(r'^[他她它]', s))
        if len(sentences) >= 10:
            ratio = start_he_she / min(len(sentences), 50)
            if ratio > 0.6:
                issues.append(f"P1 VoiceBreath: '他/她/它'开头占 {ratio*100:.0f}%, 叙述距离单一")

        # 检测感官描写类型是否均衡
        senses = {"视觉": 0, "听觉": 0, "触觉": 0, "嗅觉": 0}
        sense_kw = {
            "视觉": ["看见", "看到", "映入", "映入眼帘", "显示"],
            "听觉": ["听见", "听到", "传来", "声响", "声音"],
            "触觉": ["摸到", "触摸", "冰凉", "温热", "刺痛"],
            "嗅觉": ["闻到", "气味", "味道", "气息", "飘来"],
        }
        for sense, keywords in sense_kw.items():
            for kw in keywords:
                senses[sense] += text.count(kw)
        max_sense = max(senses.values())
        if max_sense > 0:
            total_sense = sum(senses.values())
            sense_ratio = max_sense / total_sense
            if sense_ratio > 0.7:
                dominant = max(senses, key=senses.get)
                issues.append(f"P1 VoiceBreath: 感官描写{'视觉' if dominant else ''}占比 {sense_ratio*100:.0f}%, 类型不均衡")
        return issues

    def prompt(self):
        return "Vary narrative distance. Mix close third-person with occasional omniscient. Include multiple sensory modalities."


# ─── Module 10: Momentum (P1) — 新: 动量守恒 ───
# 检测情绪曲线是否单调（无情绪起伏 = AI味）
class Momentum(L2Module):
    def __init__(self):
        super().__init__("Momentum", "P1",
                         "Emotional curve should have ups and downs. Flat = AI writing.")
        self.ready = True

    def check(self, text):
        issues = []
        # 基于标点情绪标记检测
        cn_chars = self._cn_only(text)
        if not cn_chars:
            return issues
        exclamations = text.count('！') + text.count('!')
        questions = text.count('？') + text.count('?')
        ellipsis = text.count('……')
        wc = len(cn_chars)
        # 检测情绪密度
        emotive = exclamations + questions + ellipsis
        density = emotive / wc * 1000
        if density < 2.0 and wc > 500:
            issues.append(f"P1 Momentum: 情绪标记密度过低 {density:.1f}/千字. 可能需要增加情绪起伏")

        # 分段检测情绪变化
        paras = [p.strip() for p in text.split('\n') if len(self._cn_only(p)) > 30]
        if len(paras) >= 4:
            segments = len(paras) // 4
            segment_scores = []
            for i in range(segments):
                seg = ''.join(paras[i*4:(i+1)*4])
                seg_exc = seg.count('！') + seg.count('!')
                seg_q = seg.count('？') + seg.count('?')
                segment_scores.append(seg_exc + seg_q)
            if len(segment_scores) >= 2:
                variance = sum((s - sum(segment_scores)/len(segment_scores))**2 for s in segment_scores)
                if variance < 0.5:
                    issues.append("P1 Momentum: 各段情绪标记方差过小, 情绪曲线可能过于平坦")
        return issues

    def _cn_only(self, t):
        return ''.join(c for c in t if '\u4e00' <= c <= '\u9fff')

    def prompt(self):
        return "Create emotional peaks and valleys. Not every paragraph should have the same intensity. Vary tension across the chapter."


# ─── Module 11: Deslop Natural (P1) — 新: story-deslop 自然文本基线 ───
# 检测自然文本特征: 段落长度分布、对话标签比例、语气词密度
class DeslopNatural(L2Module):
    def __init__(self):
        super().__init__("DeslopNatural", "P1",
                         "Natural text baseline from story-deslop: paragraph length, dialog tag ratio, colloquial particles.")
        self.ready = True

    def check(self, text):
        issues = []
        paras = [p.strip() for p in text.split('\n') if len(self._cn_only(p)) >= 10]
        if not paras:
            return issues

        # 1. 段落句子数分布
        sentences_per_para = []
        for p in paras:
            sents = [s for s in re.split(r'[。！？\n]', p) if len(self._cn_only(s)) >= 3]
            sentences_per_para.append(len(sents))
        if sentences_per_para:
            avg_sents = sum(sentences_per_para) / len(sentences_per_para)
            if avg_sents > 4.0:
                issues.append(f"P1 DeslopNatural: 平均每段 {avg_sents:.1f} 句 (自然文本1-3句为主)")

        # 2. 对话标签比例
        total_dialog = len(re.findall(r'[「「"「"「].*?[」」"」"」]', text))
        dialog_tags = sum(text.count(t) for t in ["说道", "问道", "回答道", "解释道", "问", "说"])
        cn_chars = len(self._cn_only(text))
        if cn_chars > 0 and total_dialog > 0:
            tag_ratio = dialog_tags / total_dialog
            if tag_ratio > 0.4:
                issues.append(f"P1 DeslopNatural: 对话标签率 {tag_ratio*100:.0f}% (自然文本60%+无标签)")

        # 3. 语气词密度
        particles = ['嘤', '嘶', '靠', '行吧', '得嘞', '啧', '嘛', '呗', '咯', '咩']
        particle_count = sum(text.count(p) for p in particles)
        density = particle_count / cn_chars * 1000 if cn_chars > 0 else 0
        # 检测是否完全没有语气词（过度正式）
        if particle_count == 0 and cn_chars > 300:
            issues.append("P1 DeslopNatural: 无语气词, 对话可能过于书面化")
        elif density > 8.0:
            issues.append(f"P1 DeslopNatural: 语气词密度 {density:.1f}/千字, 可能过度")

        # 4. 排比结构检测
        parallel_count = len(re.findall(r'(?:[，、][^，、]{2,8}[，、][^，、]{2,8}(?:和|与)[^，、]{2,8})', text))
        if parallel_count >= 3:
            issues.append(f"P1 DeslopNatural: 排比结构 {parallel_count}次, 连续3+排比是AI特征")

        return issues

    def _cn_only(self, t):
        return ''.join(c for c in t if '\u4e00' <= c <= '\u9fff')

    def prompt(self):
        return "Natural text markers: 1-3 sentences per paragraph, use action tags not dialog tags, include colloquial particles, avoid consecutive parallelism."


# ─── Module 12: HumanizerZH (P1) — 新: Humanizer-zh 融合检测 ───
# 检测 Humanizer-zh 24模式中的核心模式: 夸大意义、宣传语言、填充短语、模糊归因
class HumanizerZH(L2Module):
    def __init__(self):
        super().__init__("HumanizerZH", "P1",
                         "Humanizer-zh pattern detection: significance exaggeration, promotional language, filler phrases.")
        self.ready = True
        self.patterns = {
            "夸大意义": ["重要意义", "奠定了", "不可替代", "极其重要", "划时代",
                         "标志着", "见证了", "的体现", "的证明", "不可磨灭",
                         "深深植根于", "关键转折点"],
            "宣传语言": ["值得关注", "值得推荐", "不容错过", "必读", "值得拥有",
                         "完美", "绝佳", "极致", "巅峰", "首选"],
            "填充短语": ["我们可以看到", "我们会发现", "换句话说", "也就是说",
                         "值得注意的是", "需要强调的是", "可以观察到的是",
                         "我们需要认识到", "我们必须注意到"],
            "模糊归因": ["行业报告显示", "观察者指出", "专家认为", "一些批评者认为",
                         "多个来源", "据报道", "据了解", "业内人士表示"],
            "三段式": ["第一", "第二", "第三", "首先", "其次", "最后",
                      "一方面", "另一方面", "最后一方面"],
        }

    def check(self, text):
        issues = []
        for category, keywords in self.patterns.items():
            matches = [(kw, text.count(kw)) for kw in keywords if text.count(kw) > 0]
            total = sum(c for _, c in matches)
            threshold = {"夸大意义": 2, "宣传语言": 2, "填充短语": 3, "模糊归因": 1, "三段式": 3}.get(category, 2)
            if total >= threshold:
                top = sorted(matches, key=lambda x: -x[1])[:3]
                top_str = "; ".join(f"'{w}'x{c}" for w, c in top)
                issues.append(f"P1 HumanizerZH[{category}]: 命中{total}处 (阈值{threshold}). {top_str}")
        return issues

    def prompt(self):
        return "Avoid: 夸大意义('重要意义''奠定了'), 宣传语言('不容错过''必读'), 填充短语('我们可以看到'等), 模糊归因('据专家分析'等). Be specific."


# ─── Module Registry ───
_L2_MODULES = [
    BodyLaw(),          # 1 - P0
    MemoryTrace(),      # 2 - P0
    ItchLaw(),          # 3 - P0
    ShowNotTell(),      # 4 - P0
    AntiBalance(),      # 5 - P1 (new)
    AntiPerfect(),      # 6 - P2 (new)
    VocabTemperature(), # 7 - P1 (new)
    Subtext(),          # 8 - P2 (new)
    VoiceBreath(),      # 9 - P1 (new)
    Momentum(),         # 10 - P1 (new)
    DeslopNatural(),    # 11 - P1 (new)
    HumanizerZH(),      # 12 - P1 (new)
]


def check_all(text):
    """Run all L2 checks on text, return list of issues from all modules."""
    all_issues = []
    for mod in _L2_MODULES:
        try:
            issues = mod.check(text)
            if issues:
                all_issues.extend(issues)
        except Exception as e:
            all_issues.append(f"[{mod.name}] check error: {e}")
    return all_issues


def get_prompt_block():
    """Build L3 prompt block from all ready modules."""
    prompts = [mod.prompt() for mod in _L2_MODULES if mod.ready]
    return "\n".join(prompts)


def list_modules():
    return [{"name": mod.name, "level": mod.level, "ready": mod.ready, "description": mod.description}
            for mod in _L2_MODULES]
