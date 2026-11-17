"""KingDoc 看板视图（Kanban View）

按"状态"字段分组卡片，每列一个状态。
零第三方依赖，自研渲染引擎。
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from engine.views.base import BaseView


class KanbanView(BaseView):
    """看板视图：按状态字段分组卡片。"""

    VIEW_TYPE = "kanban"

    # 常见状态字段名自动识别
    STATUS_FIELDS = ["状态", "status", "阶段", "stage", "进度", "priority", "优先级"]

    def render(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """渲染看板视图。

        data: {
            "records": [{"fields": {"标题": "任务A", "状态": "进行中", ...}}],
            "fields": [{"name": "标题", "type": "text"}, {"name": "状态", "type": "select"}]
        }
        """
        records = data.get("records", [])
        fields = data.get("fields", [])
        status_field = self._detect_status_field(fields)

        # 按状态分组
        columns: Dict[str, List[Dict]] = {}
        for r in records:
            status = str(self._safe_get(r, f"fields.{status_field}", "未分配"))
            if status not in columns:
                columns[status] = []
            columns[status].append(r)

        # 卡片摘要（取第一个文本字段作为标题）
        title_field = self._detect_title_field(fields, status_field)
        cards = []
        for status, items in columns.items():
            for item in items:
                cards.append({
                    "id": item.get("record_id", ""),
                    "title": self._safe_get(item, f"fields.{title_field}", "(无标题)"),
                    "status": status,
                    "fields": item.get("fields", {}),
                })

        return {
            "view_type": "kanban",
            "status_field": status_field,
            "columns": list(columns.keys()),
            "total_cards": len(cards),
            "cards": cards,
        }

    def _detect_status_field(self, fields: List[Dict]) -> str:
        """自动识别状态字段。"""
        field_names = [f.get("name", "") for f in fields]
        # 优先匹配已知状态字段
        for candidate in self.STATUS_FIELDS:
            if candidate in field_names:
                return candidate
        # 其次找 select 类型字段
        for f in fields:
            if f.get("type") == "select" and f.get("name"):
                return f["name"]
        # 默认返回第一个字段
        return field_names[0] if field_names else "状态"

    def _detect_title_field(self, fields: List[Dict], status_field: str) -> str:
        """自动识别标题字段。"""
        field_names = [f.get("name", "") for f in fields]
        title_keywords = ["标题", "title", "名称", "name", "任务", "task"]
        for kw in title_keywords:
            for fn in field_names:
                if kw in fn and fn != status_field:
                    return fn
        # 返回第一个非状态文本字段
        for f in fields:
            if f.get("name") != status_field and f.get("type") in ("text", ""):
                return f.get("name", "")
        return field_names[0] if field_names else ""
