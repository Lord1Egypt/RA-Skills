"""
input_adapter.py — 输入适配层
Phase 3: 用 Pydantic/contract 校验所有入参，输出规范化的 PlanContext。
"""
from typing import Optional, List, Dict, Any
from .contracts import PlanContext, validate_plan_context


def build_plan_context(
    chapter_id: int,
    total_chapters: int,
    platform: str = "番茄",
    genre: str = "都市",
    core_summary: str = "",
    plot_points: Optional[List[str]] = None,
    word_count: int = 2500,
    ending_type: str = "悬疑收尾",
    before_state: Optional[Dict[str, Any]] = None,
) -> PlanContext:
    """从原始入参构建校验过的 PlanContext"""
    ctx = PlanContext(
        chapter_id=int(chapter_id),
        total_chapters=int(total_chapters),
        platform=str(platform),
        genre=str(genre),
        core_summary=str(core_summary or ""),
        plot_points=list(plot_points or []),
        word_count=max(500, min(10000, int(word_count))),
        ending_type=str(ending_type or "悬疑收尾"),
        before_state=dict(before_state or {}),
    )
    errors = validate_plan_context(ctx)
    if errors:
        raise ValueError(f"PlanContext validation failed: {'; '.join(errors)}")
    return ctx