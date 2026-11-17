#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""quality.py — 不降质量护栏度量（确定性结构清单，离线、无 LLM）

为北极星「在不降低交付质量的前提下…」提供可量化、零成本、可复现的质量信号：
- 每个交付物在 executor 渲染后即算 quality_score (0-100) 与逐项检查清单；
- diagnose 聚合整体 / 分类型 avg_quality；
- report_engine 用 QUALITY_FLOOR 门槛 + 关键章节是否缺失，决定「节省是否可信」护栏横幅
  （任一关键检查项失败，则该份交付物直接判为不可信，即便总分过门槛）。

设计原则：只用正则做结构断言，绝不调用 LLM（否则重新产生 token 成本、需联网，
直接违背北极星「降低 AI 使用成本」）。清单随任务类型不同而不同，可逐步扩展。
本模块不 import 任何项目内其他模块，避免循环依赖。
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

# 质量分门槛：低于此值，节省声明视为「不可信」（护栏触发）。
QUALITY_FLOOR = 70


@dataclass
class ScoreResult:
    """单次交付物的质量评分。score=None 表示「该类型未配置质量清单 / 未测」。"""
    score: int = None
    checks: list = field(default_factory=list)  # list[(name:str, passed:bool)]
    floor: int = QUALITY_FLOOR
    critical: set = field(default_factory=set)  # 关键检查项：任一失败即「不可信」

    @property
    def critical_failed(self) -> bool:
        return any((not ok) and (name in self.critical) for name, ok in self.checks)

    @property
    def credible(self) -> bool:
        # 过门槛 + 无关键项失败，二者皆满足才可信（护栏对「缺必要章节」生效）。
        return (
            self.score is not None
            and self.score >= self.floor
            and not self.critical_failed
        )

    def summary(self) -> str:
        if self.score is None:
            return "（未测）"
        marks = " ".join(f"{n}{'✓' if ok else '✗'}" for n, ok in self.checks)
        return f"{self.score}/100（{marks}）"


# ─────────────────────────────────────────────────────────────
# 各任务类型的结构清单（对渲染后的 markdown 做断言）
# ─────────────────────────────────────────────────────────────

def score_weekly_report(md: str) -> ScoreResult:
    """周报：概览 / 重点工作非空 / 下周计划 / 风险与阻塞 四要素。"""
    checks = []
    checks.append(("概览", "## 本周概览" in md or "本周概览" in md))
    # 渲染器在无内容时塞「（暂无记录）」占位，据此判非空
    checks.append(("重点工作非空", "（暂无记录）" not in md))
    checks.append(("下周计划", "（待补充）" not in md and ("## 下周计划" in md or "下周计划" in md)))
    checks.append(("风险与阻塞", "## 风险与阻塞" in md or "风险与阻塞" in md))
    passed = sum(1 for _, ok in checks if ok)
    score = round(passed / len(checks) * 100)
    # 风险与阻塞是周报最关键章节：缺失即视为质量未保住，节省声明不可信。
    return ScoreResult(score=score, checks=checks, critical={"风险与阻塞"})


def score_meeting_minutes(md: str) -> ScoreResult:
    """纪要：核心结论 / 待办事项 / 行动项有负责人或截止 / 参会与背景。"""
    checks = []
    has_conclusion = "## 核心结论" in md and "（会议未形成明确结论）" not in md
    checks.append(("核心结论", has_conclusion))
    has_action = "## 待办事项" in md and "（无明确待办）" not in md
    checks.append(("待办事项", has_action))
    has_owner = ("负责人：" in md) or ("@" in md)
    checks.append(("行动项有负责人/截止", has_owner))
    has_attendee = "## 参会与背景" in md
    checks.append(("参会与背景", has_attendee))
    passed = sum(1 for _, ok in checks if ok)
    score = round(passed / len(checks) * 100)
    # 核心结论是纪要的灵魂：无结论的纪要等于没开，节省声明不可信。
    return ScoreResult(score=score, checks=checks, critical={"核心结论"})


_DROP_RE = re.compile(r"忽略\s*(\d+)\s*个单元格")


def score_analysis(md: str) -> ScoreResult:
    """数据分析：关键指标表存在 + 无隐藏丢行（复用数据丢弃披露行）。"""
    checks = []
    has_table = "## 关键指标" in md
    checks.append(("关键指标表", has_table))
    m = _DROP_RE.search(md)
    dropped = int(m.group(1)) if m else 0
    checks.append(("无隐藏丢行", dropped == 0))
    if not has_table:
        score = 0
    else:
        # 有丢行按丢行数扣分（最多扣 40），结构完整仍保留基础分
        score = max(0, 100 - min(40, dropped))
    # 隐藏丢行是数据完整性最严重问题：静默丢数据比少张表更危险，缺失即不可信。
    return ScoreResult(score=score, checks=checks, critical={"无隐藏丢行"})


def score_distill(md: str) -> ScoreResult:
    """文档整理：保守结构断言（无源长度上下文）—— 大纲要点数 + 要点有实质内容。"""
    points = [ln for ln in (md or "").splitlines() if ln.strip().startswith("- ")]
    n = len(points)
    checks = []
    checks.append(("要点≥3", n >= 3))
    avg_len = (sum(len(p) for p in points) / n) if n else 0
    checks.append(("要点有实质内容", avg_len >= 12))
    passed = sum(1 for _, ok in checks if ok)
    score = round(passed / len(checks) * 100) if n else 0
    # 要点数不足 3 视为「整理过于单薄」，未达成文档整理的基本价值，不可信。
    return ScoreResult(score=score, checks=checks, critical={"要点≥3"})


_DISPATCH = {
    "周报生成": score_weekly_report,
    "会议纪要": score_meeting_minutes,
    "数据分析": score_analysis,
    "文档整理": score_distill,
}


def score_deliverable(task_type: str, md: str) -> ScoreResult:
    """按任务类型给渲染后的交付物打分；未配置清单的类型返回 score=None（未测）。"""
    fn = _DISPATCH.get(task_type)
    if fn is None:
        return ScoreResult(score=None, checks=[])
    return fn(md or "")
