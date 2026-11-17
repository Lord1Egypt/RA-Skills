#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
multi_line_engine.py — 多线叙事权重调度与合规校验引擎

参考：《网络文学AI工业化创作全体系深度研究报告（续二十一）》
第186节 多线叙事算法模型与代码引擎落地

核心功能：
  - 四线权重自动校验（主线/功能性支线/人物性支线/伏笔暗线）
  - 无效支线排查（无回流、无闭环）
  - 支线篇幅合规检测
  - 长线伏笔持续校验
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

_log = logging.getLogger("multi_line_engine")


class MultiLineNarrativeEngine:
    """多线叙事权重调度与合规校验引擎"""

    def __init__(self):
        # 四线权重配置
        self.line_weight = {
            "主线锚点线": 10,
            "功能性支线": 7,
            "人物性支线": 5,
            "伏笔暗线": 3,
        }
        self.chapter_limit = {"功能性支线": 25, "人物性支线": 20}
        self.lines_log: List[Dict] = []

    # ========== 数据录入 ==========

    def add_line_record(
        self,
        chapter_num: int,
        line_type: str,
        content_len: int,
        has_backflow: bool = False,
        has_clue: bool = False,
        desc: str = "",
    ):
        """录入单章多线剧情数据"""
        if line_type not in self.line_weight:
            _log.warning(f"未知线类型: {line_type}，跳过录入")
            return
        self.lines_log.append({
            "chapter": chapter_num,
            "line_type": line_type,
            "content_len": content_len,
            "has_backflow": has_backflow,
            "has_clue": has_clue,
            "desc": desc,
            "weight": self.line_weight[line_type],
        })

    def load_from_state(self, state_data: dict):
        """从 NovelState 加载多线历史数据"""
        lines = state_data.get("multi_line_log", [])
        if lines:
            self.lines_log = lines
            _log.info(f"MultiLineEngine: loaded {len(lines)} records from state")

    # ========== 合规校验 ==========

    def check_narrative_compliance(self) -> Dict[str, Any]:
        """多线合规性校验 — 排查脱线、灌水、权重失衡"""
        if not self.lines_log:
            return {"compliance": True, "level": "无数据", "problems": [], "suggest": "尚无章节数据"}

        problems = []
        total_weight = sum(i["weight"] for i in self.lines_log)
        main_weight = sum(
            i["weight"] for i in self.lines_log if i["line_type"] == "主线锚点线"
        )

        # 1. 主线权重校验
        if total_weight > 0 and main_weight / total_weight < 0.4:
            problems.append(
                f"主线权重偏低 ({main_weight}/{total_weight}={main_weight/total_weight:.0%})，"
                "支线可能喧宾夺主"
            )

        # 2. 支线长度超限
        branch_over = [
            i
            for i in self.lines_log
            if i["line_type"] in self.chapter_limit
            and i["content_len"] > self.chapter_limit[i["line_type"]]
        ]
        if branch_over:
            problems.append(
                f"{len(branch_over)} 处支线篇幅超限，易造成剧情拖沓"
            )

        # 3. 支线回流校验
        no_backflow = [
            i
            for i in self.lines_log
            if i["line_type"] != "主线锚点线" and not i["has_backflow"]
        ]
        if no_backflow:
            problems.append(
                f"{len(no_backflow)} 条支线无主线回流，属于无效灌水"
            )

        # 4. 暗线伏笔校验
        no_clue = [
            i
            for i in self.lines_log
            if i["line_type"] == "伏笔暗线" and not i["has_clue"]
        ]
        if no_clue:
            problems.append(f"{len(no_clue)} 条暗线无伏笔埋点，长线续航不足")

        # 5. 章节覆盖校验
        covered_chapters = len(set(i["chapter"] for i in self.lines_log))
        total_chapters = max(i["chapter"] for i in self.lines_log) if self.lines_log else 0
        if total_chapters > 0 and covered_chapters / total_chapters < 0.6:
            problems.append(
                f"仅 {covered_chapters}/{total_chapters} 章有多线记录，建议提高章节覆盖率"
            )

        # 合规评级
        if not problems:
            level = "优秀稳定"
            suggest = "多线叙事耦合良好，权重均衡，无脱线灌水问题"
        elif len(problems) <= 2:
            level = "轻度风险"
            suggest = "建议优先处理主线权重和回流问题"
        else:
            level = "需人工干预"
            suggest = "建议暂停创作，全量排查多线布局后继续"

        main_pct = round(main_weight / total_weight * 100, 1) if total_weight > 0 else 0
        return {
            "compliance": len(problems) == 0,
            "level": level,
            "problems": problems,
            "main_line_pct": f"{main_pct}%",
            "total_records": len(self.lines_log),
            "suggest": suggest,
        }

    # ========== 单章分析 ==========

    def analyze_chapter(self, text: str, chapter: int) -> List[str]:
        """分析单章的多线叙事质量，返回问题清单"""
        issues = []

        # 检测是否只有单一叙事线（无支线）
        line_markers = {
            "主线锚点线": ["主线", "核心", "目标", "任务"],
            "功能性支线": ["副本", "任务", "秘境", "探索", "试炼"],
            "人物性支线": ["他", "她", "朋友", "兄弟", "师父", "徒弟"],
            "伏笔暗线": ["秘密", "谜", "真相", "传说", "预言", "神秘"],
        }
        detected_lines = set()
        for line_type, markers in line_markers.items():
            if any(m in text for m in markers):
                detected_lines.add(line_type)

        if len(detected_lines) < 2:
            issues.append(f"本章仅检测到 {len(detected_lines)} 条叙事线，建议引入支线对比")

        # 检测多线切换生硬（连续出现固定段落模式）
        paragraphs = [p for p in text.split("\n") if p.strip()]
        if len(paragraphs) >= 6:
            # 检测是否有规律的段落长度模式（AI模板化特征）
            lengths = [len(p) for p in paragraphs[:10]]
            # 如果段落长度方差过小，可能是模板化
            if sum(lengths) / len(lengths) > 0:
                avg = sum(lengths) / len(lengths)
                variance = sum((l - avg) ** 2 for l in lengths) / len(lengths)
                if variance < 500:  # 段落长度过于均匀 → 模板化
                    issues.append("段落长度过于均匀，存在AI模板化叙事特征")

        # 检测章末钩子
        last_200 = text[-200:]
        hook_words = ["突然", "就在这时", "没想到", "可是", "但是", "却", "?", "？"]
        if not any(w in last_200 for w in hook_words):
            issues.append("章末缺乏钩子，建议留悬念或未完成状态")

        return issues

    # ========== 状态持久化 ==========

    def to_dict(self) -> dict:
        return {"lines_log": self.lines_log[-200:]}  # 保留最近200条

    def reset(self):
        self.lines_log.clear()


# 便捷工厂函数
def create_engine() -> MultiLineNarrativeEngine:
    return MultiLineNarrativeEngine()
