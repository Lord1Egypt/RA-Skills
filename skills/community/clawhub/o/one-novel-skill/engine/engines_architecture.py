#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""架构引擎 — 小说结构/节奏/章节规划"""


class ArchitectureEngine:
    """小说总体架构规划与验证"""


    def analyze(self, text, **kwargs):
        """架构分析入口 — 文本节奏/叙事密度/结构完整性"""
        issues = []
        chapter = kwargs.get("ch", 0)
        total = kwargs.get("total", 100)

        # 1. 节奏位置分析
        if chapter > 0:
            rhythm = self.calc_rhythm(chapter, total)
            issues.append(f"[架构] ch{chapter}/全书{total}: 阶段={rhythm['阶段']}, {rhythm['建议']}")

        # 2. 发现与突转检测
        if text:
            result = self.check_anagnorisis_peripeteia(text)
            verdict = result.get("verdict", "")
            if "缺少" in verdict:
                issues.append(f"[架构] {verdict}")

        return issues

    @staticmethod
    def design_volumes(total_chapters: int) -> list:
        """按15-20-30-20原则设计分卷"""
        if total_chapters <= 20:
            return [{"start": 1, "end": total_chapters, "type": "单卷"}]
        vol_size = max(20, total_chapters // 5)
        vols = []
        start = 1
        while start <= total_chapters:
            end = min(start + vol_size - 1, total_chapters)
            ratio = (start - 1) / total_chapters
            if ratio < 0.05:
                t = "开局"
            elif ratio < 0.25:
                t = "发展"
            elif ratio < 0.75:
                t = "深化"
            else:
                t = "高潮结局"
            vols.append({"start": start, "end": end, "type": t})
            start = end + 1
        return vols

    @staticmethod
    def calc_rhythm(current: int, total: int) -> dict:
        """计算当前章节在全书中的节奏位置"""
        ratio = current / total
        if ratio <= 0.05:
            return {"阶段": "开局", "建议": "密集爽点，每日更新"}
        elif ratio <= 0.25:
            return {"阶段": "早期", "建议": "平均节奏，逐步展开"}
        elif ratio <= 0.75:
            return {"阶段": "中期", "建议": "深化设定，穿插大小高潮"}
        else:
            return {"阶段": "后期", "建议": "节奏加快，收束支线"}

    # === 故事三角检测 (源自04-story.md 麦基) ===
    @staticmethod
    def detect_story_triangle(genre, has_linear=True, has_closure=True):
        """检测故事类型在故事三角中的位置"""
        if genre in ("悬疑", "推理", "冒险"):
            return {"triangle": "大情节", "char": "因果/线性/闭合", "note": "经典设计"}
        if genre in ("文艺", "文学", "情感"):
            if not has_closure:
                return {"triangle": "小情节", "char": "开放式/内在冲突", "note": "极简主义"}
        if genre in ("实验", "先锋"):
            return {"triangle": "反情节", "char": "非线性/多重现实", "note": "解构主义"}
        return {"triangle": "大情节（默认）", "char": "经典设计", "note": "匹配标准叙事"}
    # === 分支叙事三模型 (源自01-game-narrative.md) ===
    @staticmethod
    def branching_narrative_model(model="线性"):
        models = {
            "线性+分支": "主线固定, 关键节点2-3个分支选项, 影响中期走向",
            "辐射状": "从中心事件向外发散, 每个分支独立探索",
            "网状": "全自由选择, 每个选择影响后续所有可能性",
        }
        return {"model": model, "desc": models.get(model, "线性"),
                "complexity": "低" if model == "线性+分支" else "中" if model == "辐射状" else "高"}

    @staticmethod
    def check_narrative_density(chapter_events):
        """叙事密度递进: 前半每章1-2事件, 后半每章2-3事件 (novella pacing)"""
        if not chapter_events or len(chapter_events) < 4:
            return {"verdict": "数据不足"}
        mid = len(chapter_events) // 2
        first_half = chapter_events[:mid]
        second_half = chapter_events[mid:]
        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)
        return {
            "first_half_avg": round(avg_first, 1),
            "second_half_avg": round(avg_second, 1),
            "trend": "密度递增" if avg_second > avg_first else "密度递减",
            "recommend": "后半密度应大于前半" if avg_second <= avg_first else "",
        }
    # === 视觉小说结构 (源自02-visual-novel.md) ===
    @staticmethod
    def vn_structure_check(chapters, char_count):
        """VN结构: 共同线40%/角色线50%/结局10%"""
        if chapters < 10:
            return {"verdict": "章节过少(需10+)"}
        common = int(chapters * 0.4)
        route = int(chapters * 0.5)
        ending = chapters - common - route
        return {
            "common_line": f"1-{common}章: 世界观+全角色引入",
            "route_line": f"{common+1}-{common+route}章: 角色线展开",
            "ending": f"{common+route+1}-{chapters}章: 结局分支",
            "char_count_warning": f"角色数{char_count}>5: VN建议核心<=5" if char_count > 5 else "",
        }
    # === 亚里士多德诗学 (源自01-poetics.md) ===
    @staticmethod
    def check_anagnorisis_peripeteia(text):
        """检测发现与突转: 每章应有认知升级或情势转折"""
        if not text:
            return {"has_discovery": False, "has_reversal": False}
        issue_count = text.count("原来") + text.count("发现") + text.count("终于知道")
        reversal_count = text.count("没想到") + text.count("却") + text.count("但是")
        return {
            "discovery_count": issue_count,
            "reversal_count": reversal_count,
            "has_discovery": issue_count > 0,
            "has_reversal": reversal_count > 1,
            "verdict": "有发现+突转" if issue_count > 0 and reversal_count > 1
                       else "缺少突转" if reversal_count <= 1
                       else "缺少发现",
        }