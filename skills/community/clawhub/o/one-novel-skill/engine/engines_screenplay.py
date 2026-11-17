#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""剧本引擎 — 场景质量分析/转场自然度/钩子强度

驱动数据:
  09-editor-perspective.md (14道审查关卡: 开篇吸引力/悬念密度/节奏)
  04-reader-psychology.md (蔡格尼克效应/峰终定律)
  01-narrative-architectures.md (叙事结构)
"""

import re

from .engine_base import EngineBase


class ScreenplayEngine(EngineBase):
    """场景与转场质量评估"""

    engine_name = "screenplay"
    engine_tags = ["场景"]

    def analyze(self, text, **kwargs):
        issues = []
        hi = self.check_hook_density(text)
        if hi: issues.extend(hi if isinstance(hi, list) else [str(hi)])
        ri = self.check_value_reversal(text)
        if ri: issues.extend(ri if isinstance(ri, list) else [str(ri)])
        return issues

    @staticmethod
    def scene_analysis(text: str) -> dict:
        """场景质量多维度分析"""
        if not text:
            return {"scenes": 0, "avg_para_len": 0, "dialog_ratio": 0, "score": 0}

        paras = [p for p in text.split('\n') if len(p.strip()) > 20]
        if not paras:
            return {"scenes": 1, "avg_para_len": len(text), "dialog_ratio": 0, "score": 10}

        # 段落长度分析
        para_lens = [len(p) for p in paras]
        avg_para = sum(para_lens) / len(para_lens)
        max_para = max(para_lens)
        min_para = min(para_lens)
        var_para = sum((l - avg_para) ** 2 for l in para_lens) / len(para_lens)

        # 对话密度
        quote_count = text.count("\u201c") + text.count("\u300c") + text.count('"')
        dialog_ratio = quote_count / max(len(text), 1)

        # 场景数估算 (场景切换标记)
        scene_breaks = len(re.findall(r'(?:\n\s*\n)|(?:\r\n\s*\r\n)', text))
        scenes = max(1, scene_breaks + 1)

        # 09-编辑视角 第1关: 开篇吸引力
        opening = text[:300]
        opening_score = 0
        for kw in ["?", "！", "？", "!", "突然", "就在这时", "没想到"]:
            if kw in opening:
                opening_score += 2
        opening_score = min(10, opening_score)

        # 09-编辑视角 第5关: 悬念密度
        ending = text[-200:]
        hook_score = 0
        for kw in ["?", "！", "？", "!", "突然", "就在这时", "但是", "可是", "却"]:
            if kw in ending:
                hook_score += 2
        hook_score = min(10, hook_score)

        # 段落节奏评分 (09-编辑视角: 长短交替)
        rhythm_score = 10
        if var_para < 1000:
            rhythm_score -= 3  # 段落太均匀
        if avg_para > 200:
            rhythm_score -= 2  # 段落太长
        if avg_para < 40:
            rhythm_score -= 1  # 段落太碎
        rhythm_score = max(1, rhythm_score)

        # 综合场景评分
        total_score = (opening_score * 0.3 + hook_score * 0.3 + rhythm_score * 0.4)

        return {
            "scenes": scenes,
            "avg_para_len": round(avg_para, 1),
            "max_para_len": max_para,
            "min_para_len": min_para,
            "para_variance": round(var_para, 0),
            "dialog_ratio": round(dialog_ratio, 3),
            "opening_hook_score": opening_score,
            "ending_hook_score": hook_score,
            "rhythm_score": rhythm_score,
            "score": round(total_score, 1),
            "grade": "S" if total_score >= 9 else "A" if total_score >= 7 else "B" if total_score >= 5 else "C",
        }

    @staticmethod
    def transition_quality(text: str) -> float:
        """评估转场自然度 (09-编辑视角)"""
        if not text or len(text) < 100:
            return 0.5

        # 突兀转场词
        abrupt_markers = ["突然", "就这样", "不知过了多久", "与此同时", "镜头一转"]
        abrupt_count = sum(1 for w in abrupt_markers if w in text)
        abrupt_count -= text.count("突然想到")  # 内心活动不算突兀

        # 自然过渡词
        smooth_markers = ["然后", "接着", "过了一会儿", "半小时后", "第二天"]
        smooth_count = sum(1 for w in smooth_markers if w in text)

        score = 0.7  # 基础分
        score -= abrupt_count * 0.1
        score += smooth_count * 0.05
        return max(0.0, min(1.0, score))

    @staticmethod
    def check_hook_density(text: str) -> dict:
        """分析钩子密度和分布"""
        if not text:
            return {"hook_count": 0, "density": 0, "distribution": [], "verdict": "无数据"}

        hooks = []
        # 章节钩子标记
        markers = [("?", "疑问"), ("！", "感叹"), ("突然", "突发事件"),
                   ("就在这时", "偶然"), ("没想到", "反转"), ("但是", "转折"),
                   ("可是", "转折"), ("却", "转折"), ("发现", "揭示"),
                   ("秘密", "秘密"), ("真相", "真相")]

        for marker, htype in markers:
            idx = 0
            while True:
                found = text.find(marker, idx)
                if found == -1:
                    break
                # 计算钩子出现位置(百分比)
                position = round(found / len(text), 3)
                hooks.append({"pos": position, "type": htype, "marker": marker})
                idx = found + 1

        # 去重: 同位置取第一个
        seen_positions = set()
        unique_hooks = []
        for h in hooks:
            pos_key = int(h["pos"] * 100)
            if pos_key not in seen_positions:
                seen_positions.add(pos_key)
                unique_hooks.append(h)

        total = len(unique_hooks)
        density = round(total / max(len(text) / 1000, 1), 2)

        # 分布均匀性检查
        verdict = "良好"
        if density < 2:
            verdict = "钩子密度偏低"
        elif density > 20:
            verdict = "钩子过于密集,可能过度使用"

        return {
            "hook_count": total,
            "density": density,
            "unique_types": len(set(h["type"] for h in unique_hooks)),
            "distribution": unique_hooks[:20],
            "verdict": verdict,
        }
    # === 场景价值反转检测 (源自04-story.md 麦基) ===
    @staticmethod
    def check_value_reversal(text):
        """检测场景是否包含价值反转: 结尾与开头主角处境/认知/情感不同"""
        if not text or len(text) < 200:
            return {"has_reversal": False, "verdict": "文本过短"}
        opening = text[:100]
        ending = text[-100:]
        # 检测正向↔负向词汇变化
        positive_words = ["成功", "胜利", "高兴", "开心", "突破", "获得", "相遇", "拯救"]
        negative_words = ["失败", "失去", "受伤", "死亡", "悲伤", "崩溃", "分离", "毁灭"]
        op_pos = sum(opening.count(w) for w in positive_words)
        op_neg = sum(opening.count(w) for w in negative_words)
        en_pos = sum(ending.count(w) for w in positive_words)
        en_neg = sum(ending.count(w) for w in negative_words)
        op_val = op_pos - op_neg
        en_val = en_pos - en_neg
        reversal = (op_val > 0 and en_val < 0) or (op_val < 0 and en_val > 0)
        return {"has_reversal": reversal, "open_val": op_val, "end_val": en_val,
                "verdict": "有价值反转" if reversal else "无价值反转 - 建议重构场景"}
    # === 12种开场钩子识别 (源自07-golden-three-chapters.md) ===
    HOOK_TYPES = {
        "悬念钩": ["?", "？", "秘密", "真相", "究竟"],
        "危机钩": ["威胁", "危险", "追杀", "陷阱", "死期"],
        "冲突钩": ["冲突", "对抗", "争吵", "对峙", "战斗"],
        "反差钩": ["原来", "没想到", "竟然", "居然"],
        "金手指钩": ["系统", "金手指", "技能", "天赋", "觉醒"],
        "情感钩": ["眼泪", "拥抱", "温暖", "心疼", "守护"],
        "穿越钩": ["穿越", "来到", "异世界", "转生"],
        "力量钩": ["力量", "强大", "突破", "境界", "升级"],
        "身份钩": ["身份", "真实身份", "隐藏", "秘密"],
    }

    @staticmethod
    def classify_opening_hooks(text):
        """识别开场300字中的钩子类型"""
        if not text:
            return {"types": [], "count": 0}
        opening = text[:300]
        found = []
        for htype, markers in ScreenplayEngine.HOOK_TYPES.items():
            if any(m in opening for m in markers):
                found.append(htype)
        return {"types": found, "count": len(found),
                "verdict": f"检测到{len(found)}种钩子" if found else "无钩子 - 开场需建立冲突/悬念"}

    # === 困境具体度检测 (源自14-web-novel-opening-strategy.md) ===
    @staticmethod
    def check_dilemma_specificity(text):
        """主角困境是否具体可感"""
        if not text:
            return {"score": 0}
        opening = text[:300]
        abstract_words = ["处境", "艰难", "困难", "复杂", "不幸"]
        specific_words = ["今天", "必须", "还剩", "明天就要", "正在"]
        abstract_count = sum(opening.count(w) for w in abstract_words)
        specific_count = sum(opening.count(w) for w in specific_words)
        score = min(10, specific_count * 3)
        if abstract_count > specific_count:
            score -= abstract_count
        return {"score": max(0, score), "verdict": "困境具体" if score >= 5 else "困境抽象 - 建议具体化"}