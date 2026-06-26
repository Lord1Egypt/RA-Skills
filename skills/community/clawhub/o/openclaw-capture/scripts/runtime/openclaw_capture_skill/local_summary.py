"""Deterministic local summary engine used when no remote model key is available."""

from __future__ import annotations

import re


class DeterministicSummaryEngine:
    def summarize(self, evidence):
        from openclaw_capture_workflow.models import SummaryResult

        title = _title_from_evidence(evidence)
        source_url = str(getattr(evidence, "source_url", "") or "").strip()
        text = re.sub(r"\s+", " ", str(getattr(evidence, "text", "") or "").strip())
        conclusion = _build_conclusion(evidence, text)
        bullets = [
            f"内容类型: {getattr(evidence, 'source_kind', '') or 'unknown'}",
            f"核心结论: {conclusion}",
        ]
        if source_url:
            bullets.append(f"项目与链接: {source_url}")
        else:
            bullets.append("项目与链接: 当前输入没有提供外部链接。")
        if text:
            bullets.append(f"核心事实: {text[:120].rstrip()}")
        actions = ["如需正式归档，提供模型 Key 后可生成更完整的总结和笔记。"]
        return SummaryResult(
            title=title,
            primary_topic=title,
            secondary_topics=[],
            entities=[],
            conclusion=conclusion,
            bullets=bullets,
            evidence_quotes=[text[:80]] if text else [],
            coverage="full" if text else "partial",
            confidence="medium",
            note_tags=[],
            follow_up_actions=actions,
            timeliness="medium",
            effectiveness="medium",
            recommendation_level="recommended",
            reader_judgment="当前结果适合作为本地预览和链路验证。",
        )


def _title_from_evidence(evidence) -> str:
    title = str(getattr(evidence, "title", "") or "").strip()
    if title:
        return title[:80]
    text = re.sub(r"\s+", " ", str(getattr(evidence, "text", "") or "").strip())
    if not text:
        return "本地捕获结果"
    return text[:32].strip() or "本地捕获结果"


def _build_conclusion(evidence, text: str) -> str:
    source_kind = str(getattr(evidence, "source_kind", "") or "").strip()
    if source_kind == "pasted_text":
        return "已基于输入文字生成本地可读摘要。"
    if source_kind == "image":
        return "已基于图片提取结果生成本地可读摘要。"
    if source_kind == "video_url":
        return "已基于视频证据生成本地可读摘要。"
    if text:
        return "已基于当前证据生成本地可读摘要。"
    return "已收到输入，但证据内容仍然较少。"

