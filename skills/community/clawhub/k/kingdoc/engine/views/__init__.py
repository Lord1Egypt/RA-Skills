"""KingDoc 多维表格视图引擎（v3.7.0 新增）

对标 Airtable 的多维表格视图能力：看板 / 日历 / 甘特图。
通过 dbt API 视图配置实现，零第三方依赖。

硬件自适应：渲染并发不超过 hardware.py 推荐的 workers。
"""
from __future__ import annotations

from engine.views.kanban import KanbanView
from engine.views.calendar import CalendarView
from engine.views.gantt import GanttView

__all__ = ["KanbanView", "CalendarView", "GanttView", "render_view"]


def render_view(view_type: str, data: dict, config: dict | None = None) -> dict:
    """统一渲染入口，按视图类型路由。"""
    if view_type == "kanban":
        return KanbanView(config=config).render(data)
    if view_type == "calendar":
        return CalendarView(config=config).render(data)
    if view_type == "gantt":
        return GanttView(config=config).render(data)
    raise ValueError(f"不支持的视图类型：{view_type}（可选：kanban/calendar/gantt）")
