#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对话质量引擎 — 自然度/角色差异化/潜台词"""

import re

from .engine_base import EngineBase

# 预编译正则
class DialogueEngine(EngineBase):
    """对话质量检测与评估"""

    engine_name = "dialogue"
    engine_tags = ["对话"]

    def analyze(self, text, **kwargs):
        issues = []
        issues.extend(self.check_naturalness(text))
        issues.extend(self.check_subtext_level(text))
        issues.extend(self.check_tag_quality(text))
        return issues

    @staticmethod
    def check_naturalness(text: str) -> list:
        """检测对话自然度"""
        issues = []
        # 检测过度书面化
        written = ["深感遗憾", "对此", "鉴于", "综上所述", "显而易见"]
        for w in written:
            if w in text:
                issues.append(f"书面化对话: '{w}' — 改口语")
                break
        # 检测对话标签单调
        said = len(re.findall(r'[说道问道回答解释]', text))
        total_tags = len(re.findall(r'[道说问答]', text))
        if total_tags > 3 and said / total_tags > 0.6:
            issues.append(f"对话标签单调 ({said}/{total_tags}) — 用动作替代")
        return issues



    # === 对话艺术增强 (源自12-art-of-dialogue.md) ===

    @staticmethod
    def check_subtext_level(text: str) -> list:
        """潜台词层级分析: 检测是否过直白"""

# 预编译正则
        issues = []
        # 直接信息交换检测
        info_exchange = len(re.findall(r"“[^\u201d]{10,50}”", text))
        direct_explain = sum(1 for w in ["其实", "就是", "也就是说", "意思是"] if w in text)
        if info_exchange > 3 and direct_explain > 0:
            issues.append("对话含直接信息交换 - 建议改为场景展示或内心独白")
        # 直白程度: 大量说类标签
        said_count = len(re.findall(r"[说道说]|道", text))
        total_lines = len(re.findall(r"“[^\u201d]*”", text))
        if total_lines > 0 and said_count / total_lines > 0.7:
            issues.append(f"对话标签使用过频繁({said_count}/{total_lines}) - 建议70%零标签, 20%动作标签, 10%说")
        return issues

    @staticmethod
    def check_power_games(text: str) -> list:
        """权力博弈模式分析 (源自08-dialogue-subtext.md 50+种)"""
        issues = []
        # 抢占先机型: 用开场定义对话
        if re.search(r'我们来谈谈|知道我是谁|你确定|我说了算|听我说', text):
            issues.append("[对话] 权力博弈—抢占先机式开场")
        # 防守反击型
        if re.search(r'你觉得我应该|你什么时候开始|你是不是|如果我说不', text):
            issues.append("[对话] 权力博弈—防守反击")
        # 压迫型
        if re.search(r'你考虑过后果|你活不过|我给你三息|你以为你知道', text):
            issues.append("[对话] 权力博弈—压迫型对话")
        # 示弱型
        if re.search(r'我打不过你|我是个废物|求你帮我|我害怕|我做不到', text):
            issues.append("[对话] 权力博弈—示弱策略（可能是伪装）")
        # 伪装策略
        if re.search(r'哦\?还有这种事|我不明白你在说什么|今天天气不错|先吃饭吧', text):
            issues.append("[对话] 权力博弈—伪装/转移话题")
        # 情感操控
        if re.search(r'我以为你懂我|如果你走了|你不该这样想|为了你我愿意', text):
            issues.append("[对话] 权力博弈—情感操控")
        return issues

    @staticmethod
    def check_subtext_three_layer(text: str) -> list:
        """三层潜文本分析: 表面信息层/行动意图层/权力关系层"""
        issues = []
        lines = re.findall(r'“[^”]*”', text)
        if len(lines) < 3:
            return issues

        # 检查信息倾倒式对话 (纯表面信息传递)
        for l in lines:
            inner = l[1:-1]
            if len(inner) > 30:
                cnt_info = sum(1 for w in ['你知道吗','实际上','所谓','众所周知'] if w in inner)
                if cnt_info >= 1:
                    issues.append(f"[P1] 信息倾倒式对话: 「{inner[:30]}...」— 角色在念百科全书")
                    break

        # 检查是否有潜文本 (非直白表达)
        subtext_count = 0
        for l in lines:
            inner = l[1:-1]
            # 使用反问、省略、不完整句等表示有潜文本
            if '?' in inner or '？' in inner or '...' in inner or inner.strip()[-1:] in '。':
                if len(inner) < 20:
                    subtext_count += 1
        if subtext_count < len(lines) * 0.3:
            issues.append(f"[P2] 潜文本不足: {subtext_count}/{len(lines)} 句有潜文本空间")

        return issues

    @staticmethod
    def check_dialogue_voice(text: str) -> list:
        """角色对话声音差异化分析"""
        issues = []
        # 提取对话行及其标签
        dialog_lines = []
        for m in re.finditer(r'[^\n]*“[^”]*”[^\n]*', text):
            dialog_lines.append(m.group())

        if len(dialog_lines) < 4:
            return issues

        # 检查所有人说话方式是否雷同 (词汇多样性)
        all_inner = ''.join(re.findall(r'“([^”]*)”', text))
        unique_words = set(re.findall(r'[一-鿿]{2,4}', all_inner))
        if len(unique_words) < 15 and len(all_inner) > 100:
            issues.append(f"[P2] 角色对话同质化: 仅{len(unique_words)}个不同词汇")

        # 检查是否缺乏动作语言
        action_tags = len(re.findall(r'(抬起|落下|转身|皱眉|握拳|微笑|摇头|点头|看向|瞥了)', text[:3000]))
        said_tags = len(re.findall(r'[说道问道回答说]', text[:3000]))
        if said_tags > action_tags * 2 and said_tags > 5:
            issues.append(f"[P1] 对话标签依赖过重 ({said_tags}说 vs {action_tags}动作)")

        return issues

    @staticmethod
    def check_dialogue_traps(text: str) -> list:
        """网文对话常见陷阱检测"""
        issues = []
        # 陷阱1: 信息倾倒
        info_dump = re.findall(r'“[^”]{40,100}你知道吗[^”]*”', text)
        if info_dump:
            issues.append(f"[P1] 信息倾倒式对话{len(info_dump)}处")

        # 陷阱2: 对话占比过高
        total = len(text)
        dialog_chars = sum(len(m[0]) for m in re.finditer(r'“[^”]*”', text))
        if total > 500 and dialog_chars / total > 0.6:
            issues.append(f"[P1] 对话占比过高 ({dialog_chars//total*100:.0f}%) — 每3-5句加动作/环境描写")

        # 陷阱3: 无潜文本
        direct_lines = len(re.findall(r'“[^”]{5,30}”', text))
        if direct_lines > len(re.findall(r'“[^”]*”', text)) * 0.6:
            issues.append("[P2] 大量无潜文本对话 — 对话不只是传递信息")

        return issues

    @staticmethod
    def check_turn_taking(text: str) -> list:
        """话轮节奏分析"""

# 预编译正则
        issues = []
        # 提取对话行
        lines = re.findall(r"“[^\u201d]*”", text)
        if len(lines) < 4:
            return []
        lengths = [len(l) for l in lines]
        if not lengths:
            return []
        avg = sum(lengths) / len(lengths)
        variance = sum((l - avg)**2 for l in lengths) / len(lengths)
        std_dev = variance ** 0.5
        if std_dev / avg < 0.2:
            issues.append(f"话轮长度高度一致(标准差{std_dev/avg:.0%}) - 对话节奏单调, 建议长短交替")
        return issues

    @staticmethod
    def role_differentiation(text: str) -> float:
        """评估角色对话差异化"""
        lines = [l for l in text.split('\n') if '说' in l or '道' in l]
        if len(lines) < 4:
            return 0.5
        # 简评：多角色时检查用词多样性
        words = set()
        for line in lines:
            for w in line.split():
                if len(w) >= 2:
                    words.add(w)
        return min(1.0, len(words) / 50)

    # === 对话标签增强 (源自dialogue-guide.md) ===
    @staticmethod
    def check_tag_quality(text):
        """对话标签质量: 动作标签占比/标签位置多样性"""

# 预编译正则
        issues = []
        if not text:
            return []
        # 检测"说/道/问/答"类标签
        said_tags = len(re.findall(r"说道|问道|回答|答道|回答说", text))
        # 检测动作标签 (非"说"类的对话引导)
        action_tags = len(re.findall(r"[拍笑叹坐站皱眉]|放下|拿起|点[头烟]", text))
        total_lines = len(re.findall(r"[」" + chr(0x201d) + "][^」" + chr(0x201d) + "]*", text))
        if total_lines == 0:
            total_lines = len(re.findall(r"[」" + chr(0x201d) + "]", text))
        if total_lines > 0:
            action_ratio = action_tags / max(total_lines, 1)
            said_ratio = said_tags / max(total_lines, 1)
            if action_ratio < 0.2 and said_ratio > 0.3:
                issues.append(f"对话标签偏重说类({int(said_ratio*100)}%) - 建议70%零标签, 20%动作标签, 10%说")
        # 检查是否所有对话都有标签 (该省略的地方没省略)
        if total_lines > 5 and said_tags / max(total_lines, 1) > 0.6:
            issues.append("每句对话都用'说'类标签 - 通过上下文可判断时省略标签")
        return issues

    @staticmethod
    def check_dialogue_personality(text):
        """检查角色对话差异化"""

# 预编译正则
        issues = []
        lines = re.findall(r"[」" + chr(0x201d) + "][^」" + chr(0x201d) + "]{5,50}", text)
        if len(lines) < 6:
            return []
        lengths = [len(l) for l in lines]
        avg = sum(lengths) / len(lengths)
        variance = sum((l - avg)**2 for l in lengths) / len(lengths)
        std = variance ** 0.5
        if std / max(avg, 1) < 0.15:
            issues.append(f"所有角色对话长度高度一致(变异{std/avg:.0%}) - 不同角色话轮应有差异")
        # 检查是否存在口语化特征
        has_oral = any(w in text for w in ["呃", "那个", "就是说", "这个嘛", "让我想想"])
        if not has_oral and len(text) > 500:
            issues.append("对话缺少口语特征(犹豫词/重复/打断) - 建议加入个性化停顿")
        return issues