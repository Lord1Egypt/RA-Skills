#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
multi_view_review.py — 多视角对抗式审查

融合源:
  - story-review (4-agent multi-perspective: story-architect/character-designer/narrative-writer/consistency-checker)
  - openclaw-novel-write (5-view reader feedback: Target/Casual/Expert/Critic/Editor)
  - chinese-novelist-skill (Phase 4 auto-validation)

功能: 对章节进行多视角审查，输出结构化报告
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Tuple
from pathlib import Path
import json
import re


# === 审查视角定义 ===
REVIEW_PERSPECTIVES = {
    "target_reader": {
        "name": "目标读者",
        "description": "代入目标读者群体的阅读体验",
        "focus": ["读到这里烦不烦", "有没有想跳过去的地方", "看完本章想不想继续"],
        "weight": 3,
    },
    "casual_reader": {
        "name": "普通读者",
        "description": "普通网文读者的直觉感受",
        "focus": ["搞不搞得清楚在说啥", "名字/关系会不会绕晕", "开头300字抓住人吗"],
        "weight": 2,
    },
    "expert_editor": {
        "name": "资深编辑",
        "description": "从出版/平台角度评估",
        "focus": ["节奏是否可控", "市场定位", "AI检测通过率", "开头三章是否有必杀钩子"],
        "weight": 3,
    },
    "critic": {
        "name": "毒舌读者",
        "description": "严格挑剔读者视角",
        "focus": ["有没有看不懂的句子", "有没有假大空的词", "有没有啰嗦的车轱辘话",
                  "有没有刻意煽情", "一句话能说清就别用三句"],
        "weight": 2,
    },
    "consistency_checker": {
        "name": "一致性检查",
        "description": "跨章节角色/设定一致性",
        "focus": ["角色状态是否与追踪一致", "伏笔是否合理回收", "时间线有无冲突",
                  "设定有无前后矛盾", "已死角色是否误复活"],
        "weight": 3,
    },
}


# === review-deslop 同源的结构化报告格式 ===
class ReviewReportStructure:
    """审查报告结构 — 与 story-review 兼容"""
    
    REQUESTED_MODE = None  # "full" / "lean" / "solo"
    EFFECTIVE_MODE = None
    FALLBACK = "none"
    RUBRIC = "generic web-fiction"
    RUBRIC_SOURCE = "embedded fallback"


@dataclass
class ReviewIssue:
    """审查发现的问题"""
    perspective: str          # 视角ID
    category: str             # 节奏/角色/文字/对抗AI/结构
    severity: str             # critical/major/minor/suggestion
    location: str             # "第3段" / "开头300字" / "结尾"
    description: str          # 问题描述
    suggestion: str           # 修改建议（可选）
    ai_flag: bool = False     # 是否涉及AI味
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ReviewScore:
    """审查评分"""
    perspective: str
    score: float               # 0-10
    max_score: int = 10
    issues_count: int = 0
    strengths: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ReviewReport:
    """完整审查报告"""
    chapter: int
    chapter_title: str = ""
    scores: List[ReviewScore] = field(default_factory=list)
    issues: List[ReviewIssue] = field(default_factory=list)
    overall_score: float = 0.0
    verdict: str = "待评估"     # 通过 / 需修改 / 重写
    ai_assessment: str = ""     # AI味评估结果
    mode_info: str = ""         # 审查模式信息
    created_at: str = ""
    
    def add_issue(self, perspective: str, category: str, severity: str,
                  location: str, description: str, suggestion: str = "",
                  ai_flag: bool = False) -> None:
        self.issues.append(ReviewIssue(
            perspective=perspective, category=category, severity=severity,
            location=location, description=description, suggestion=suggestion,
            ai_flag=ai_flag,
        ))
    
    def set_score(self, perspective: str, score: float, 
                  strengths: List[str] = None) -> None:
        existing = next((s for s in self.scores if s.perspective == perspective), None)
        if existing:
            existing.score = score
            if strengths:
                existing.strengths.extend(strengths)
        else:
            self.scores.append(ReviewScore(
                perspective=perspective, score=score,
                issues_count=len([i for i in self.issues if i.perspective == perspective]),
                strengths=strengths or [],
            ))
    
    def compute_overall(self) -> float:
        """加权计算总分"""
        if not self.scores:
            return 0.0
        total_weight = 0
        weighted_sum = 0.0
        for s in self.scores:
            p = REVIEW_PERSPECTIVES.get(s.perspective, {})
            w = p.get("weight", 1)
            weighted_sum += s.score * w
            total_weight += w
        self.overall_score = round(weighted_sum / total_weight, 1) if total_weight > 0 else 0.0
        
        # 判定标准
        if self.overall_score >= 7.0:
            self.verdict = "通过"
        elif self.overall_score >= 4.0:
            self.verdict = "需修改"
        else:
            self.verdict = "建议重写"
        
        # 检查critical issue
        criticals = [i for i in self.issues if i.severity == "critical"]
        if criticals:
            self.verdict = "需修改"
        return self.overall_score
    
    def to_dict(self) -> dict:
        return {
            "chapter": self.chapter,
            "chapter_title": self.chapter_title,
            "scores": [s.to_dict() for s in self.scores],
            "issues": [i.to_dict() for i in self.issues],
            "overall_score": self.overall_score,
            "verdict": self.verdict,
            "ai_assessment": self.ai_assessment,
            "mode_info": self.mode_info,
            "created_at": self.created_at,
        }
    
    def to_markdown(self) -> str:
        from datetime import datetime
        self.created_at = datetime.now().isoformat()
        
        lines = [
            f"# 第{self.chapter}章 审查报告",
            f"**审查模式**: {self.mode_info or '标准'}",
            f"**整体评分**: {self.overall_score}/10 | **结论**: {self.verdict}",
            "",
            "## 各视角评分",
            "",
            "| 视角 | 评分 | 建议数 | 亮点 |",
            "|------|------|--------|------|",
        ]
        for s in self.scores:
            p = REVIEW_PERSPECTIVES.get(s.perspective, {})
            pname = p.get("name", s.perspective)
            strengths_str = "; ".join(s.strengths[:3]) if s.strengths else "-"
            lines.append(f"| {pname} | {s.score}/10 | {s.issues_count} | {strengths_str} |")
        
        if self.issues:
            lines.extend(["", "## 问题清单", ""])
            for issue in self.issues:
                pname = REVIEW_PERSPECTIVES.get(issue.perspective, {}).get("name", issue.perspective)
                sev_icon = {"critical": "🔴", "major": "🟠", "minor": "🟡", "suggestion": "💡"}
                icon = sev_icon.get(issue.severity, "⚪")
                lines.append(f"{icon} **[{pname}]** {issue.description}")
                lines.append(f"   _位置: {issue.location} | 分类: {issue.category}")
                if issue.suggestion:
                    lines.append(f"   💬 {issue.suggestion}")
                lines.append("")
        
        if self.ai_assessment:
            lines.extend(["", "## AI痕迹评估", f"\n{self.ai_assessment}", ""])
        
        lines.append(f"\n> 报告生成: {self.created_at}")
        return "\n".join(lines)
    
    def save(self, book_dir: Path) -> bool:
        review_dir = book_dir / "评审"
        review_dir.mkdir(parents=True, exist_ok=True)
        md_path = review_dir / f"第{self.chapter:03d}章.md"
        json_path = review_dir / f"第{self.chapter:03d}章.json"
        try:
            md_path.write_text(self.to_markdown(), encoding="utf-8")
            json_path.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
            return True
        except OSError:
            return False


class MultiViewReviewer:
    """多视角审查器 — 协调各视角评估"""

    def __init__(self, book_dir: Path = None):
        self.book_dir = Path(book_dir) if book_dir else None

    def review(self, text: str, chapter: int, title: str = "",
               perspectives: List[str] = None) -> ReviewReport:
        """执行多视角审查，返回结构化报告"""
        if perspectives is None:
            perspectives = list(REVIEW_PERSPECTIVES.keys())
        
        report = ReviewReport(chapter=chapter, chapter_title=title, mode_info=f"视角数: {len(perspectives)}")
        
        for pid in perspectives:
            p = REVIEW_PERSPECTIVES.get(pid)
            if not p:
                continue
            score, issues = self._score_perspective(text, pid, p)
            report.set_score(pid, score)
            for issue_data in issues:
                report.add_issue(**issue_data)
        
        # AI味融合评估
        try:
            from .l2_modules import check_all
            l2_issues = check_all(text)
            if l2_issues:
                report.ai_assessment = f"L2检测命中 {len(l2_issues)} 项:\n"
                report.ai_assessment += "\n".join(f"  - {i}" for i in l2_issues[:10])
                report.add_issue(
                    perspective="consistency_checker",
                    category="对抗AI",
                    severity="major" if len(l2_issues) > 3 else "minor",
                    location="全文",
                    description=f"L2检测命中{len(l2_issues)}项AI特征",
                    suggestion="运行去AI管线处理",
                    ai_flag=True,
                )
        except ImportError:
            pass
        
        report.compute_overall()
        return report

    def _score_perspective(self, text: str, pid: str, p_def: dict) -> Tuple[float, List[dict]]:
        """对单个视角评分"""
        base_score = 7.0
        issues = []
        word_count = len(text)
        
        if pid == "target_reader":
            # 目标读者：开头是否有钩子，是否有明显瓶颈
            if word_count < 1000:
                base_score -= 1.0
                issues.append({
                    "perspective": pid, "category": "节奏",
                    "severity": "minor", "location": "全文",
                    "description": "章节字数偏少(<1000字)",
                    "suggestion": "建议扩展到2000-3500字",
                })
            # 检测章末是否有动作收尾或悬念
            last_100 = text[-100:]
            if any(w in last_100 for w in ["结束了", "完了", "总算", "终于明白", "知道了"]):
                base_score -= 1.5
                issues.append({
                    "perspective": pid, "category": "结构",
                    "severity": "major", "location": "结尾",
                    "description": "章末有总结性/感悟式结尾",
                    "suggestion": "改为动作收尾或悬念钩子",
                })
        
        elif pid == "casual_reader":
            # 普通读者：可读性和清晰度
            long_sentences = len(re.findall(r'[^。！？\n]{60,}[。！？]', text))
            if long_sentences > 3:
                base_score -= 1.0
                issues.append({
                    "perspective": pid, "category": "文字",
                    "severity": "minor", "location": "全文",
                    "description": f"发现 {long_sentences} 个超长句(>60字)",
                    "suggestion": "拆分长句，建议每句不超过48字",
                })
        
        elif pid == "consistency_checker":
            # 一致性检查
            if self.book_dir:
                char_tracker = self.book_dir / "追踪" / "角色状态.md"
                if char_tracker.exists():
                    # 角色基本检查不深入读文件
                    pass
            # 标点一致性
            punct = {"，": 0, "。": 0, "！": 0, "？": 0}
            for p, _ in punct.items():
                punct[p] = text.count(p)
            if punct.get("。", 0) > 0:
                ratio = punct.get("，", 0) / punct.get("。", 1)
                if ratio > 8:
                    base_score -= 0.5
                    issues.append({
                        "perspective": pid, "category": "文字",
                        "severity": "minor", "location": "全文",
                        "description": f"逗号句号比 {ratio:.1f}:1 (推荐1.2-8.6:1)",
                        "suggestion": "适当增加句号断句",
                    })
        
        elif pid == "expert_editor":
            # 编辑视角：质量评估
            para_count = len([p for p in text.split('\n') if len(p.strip()) > 20])
            if para_count > 0 and word_count > 0:
                avg_para = word_count / para_count
                if 200 < avg_para < 800:
                    base_score += 0.5  # 段落长度合适
                elif avg_para > 1000:
                    base_score -= 0.5
                    issues.append({
                        "perspective": pid, "category": "节奏",
                        "severity": "minor", "location": "全文",
                        "description": f"平均段落字数 {avg_para:.0f}, 可能偏长",
                        "suggestion": "适当分段控制每段200-500字",
                    })
        
        elif pid == "critic":
            # 毒舌视角：冗余和废话
            filler_count = sum(text.count(w) for w in ["的", "了", "着", "过", "在", "就", "也", "都"])
            cn_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
            if cn_chars > 0:
                filler_ratio = filler_count / cn_chars
                if filler_ratio > 0.3:
                    base_score -= 0.5
                    issues.append({
                        "perspective": pid, "category": "文字",
                        "severity": "minor", "location": "全文",
                        "description": f"高频虚词占比 {filler_ratio*100:.0f}%, 可能存在冗余",
                        "suggestion": "删除多余的'的''了'",
                    })
        
        score = max(0.0, min(10.0, base_score))
        return score, issues


# === Dispatch modes (full / lean / solo) — 参考 story-review 的 Agent 分发架构 ===

REVIEW_MODE_FULL = ["target_reader", "casual_reader", "expert_editor", "critic", "consistency_checker"]
REVIEW_MODE_LEAN = ["target_reader", "consistency_checker"]
REVIEW_MODE_SOLO = ["target_reader"]


def review_mode_select(mode: str = "full") -> List[str]:
    """选择审查模式对应的视角列表"""
    mode_map = {
        "full": REVIEW_MODE_FULL,
        "lean": REVIEW_MODE_LEAN,
        "solo": REVIEW_MODE_SOLO,
    }
    return mode_map.get(mode, REVIEW_MODE_FULL)


class ReviewDispatcher:
    """审查分发器 — 支持全/简/单模式的分散执行
    
    架构:
      - full: spawn 全部5个视角（story-architect/character-designer/narrative-writer/consistency-checker/critic）
            需要 story-setup 部署的 agent 环境；不可用时自动降级 solo
      - lean: spawn story-architect + consistency-checker；不可用时降级 solo
      - solo: 当前会话执行基础审查
    
    当前实现: 同步聚合模式（所有视角在当前进程内执行）
    未来: 支持 async spawn 子Agent 并行审查
    """
    
    def __init__(self, book_dir=None):
        self.book_dir = Path(book_dir) if book_dir else None
        self.fallback_reason = "none"
    
    def dispatch(self, text: str, chapter: int, title: str = "",
                 mode: str = "full") -> ReviewReport:
        """分发审查任务
        
        当前实现: 同步聚合（5视角均在当前进程执行）
        未来: spawn 子Agent 后，由各个 Agent 分别报告
        """
        requested = mode
        effective = mode
        
        # 检查是否支持 spawn（当前版本: 不支持异步spawn）
        has_spawn = False
        if not has_spawn and mode in ("full", "lean"):
            effective = "solo"
            self.fallback_reason = "agent tool unavailable -> solo"
        
        viewer = MultiViewReviewer(self.book_dir)
        perspectives = review_mode_select(effective)
        report = viewer.review(text, chapter, title, perspectives)
        
        # 记录模式信息
        report.mode_info = f"Requested: {requested} | Effective: {effective}"
        if self.fallback_reason != "none":
            report.mode_info += f" | Fallback: {self.fallback_reason}"
        
        report.compute_overall()
        return report
    
    def dispatch_async(self, text: str, chapter: int, title: str = "",
                       mode: str = "full") -> None:
        """异步派发（预留接口 — 用于 spawn 子Agent）
        
        每个 Agent 收到独立任务:
          1. story-architect → 结构/节奏/伏笔
          2. character-designer → 角色一致性/声线
          3. narrative-writer → 文字质量/对话
          4. consistency-checker → 前后一致性/标点/字数
          5. critic → 毒舌/冗余/废话
        
        使用: sessions_spawn 或 subprocess 派发独立审查任务
        结果: 各 Agent 独立输出审查报告，由 dispatcher 聚合
        """
        pass
