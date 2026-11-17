"""KingDoc 甘特图视图（Gantt View）

时间轴+任务依赖箭头，适合项目进度管理。
零第三方依赖，自研渲染引擎。
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from engine.views.base import BaseView


class GanttView(BaseView):
    """甘特图视图：时间轴+任务依赖。"""

    VIEW_TYPE = "gantt"

    START_FIELDS = ["开始", "start", "开始时间", "start_date", "起始"]
    END_FIELDS = ["结束", "end", "截止日期", "end_date", "截止", "完成"]
    TITLE_FIELDS = ["标题", "title", "任务", "task", "名称", "name"]
    PROGRESS_FIELDS = ["进度", "progress", "完成度", "percent", "百分比"]
    DEPENDENCY_FIELDS = ["依赖", "dependency", "前置任务", "predecessor", "上一个"]

    def render(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """渲染甘特图视图。

        data: {
            "records": [{
                "record_id": "rec_1",
                "fields": {
                    "标题": "需求分析",
                    "开始": "2026-08-01",
                    "结束": "2026-08-10",
                    "进度": 80,
                    "依赖": ""
                }
            }],
            "fields": [...]
        }
        """
        records = data.get("records", [])
        fields = data.get("fields", [])

        start_field = self._detect_field(fields, self.START_FIELDS, "开始")
        end_field = self._detect_field(fields, self.END_FIELDS, "结束")
        title_field = self._detect_field(fields, self.TITLE_FIELDS, "标题")
        progress_field = self._detect_field(fields, self.PROGRESS_FIELDS, "")
        dep_field = self._detect_field(fields, self.DEPENDENCY_FIELDS, "")

        # 构建甘特条
        bars = []
        min_date = None
        max_date = None
        for r in records:
            start_str = str(self._safe_get(r, f"fields.{start_field}", ""))
            end_str = str(self._safe_get(r, f"fields.{end_field}", ""))
            start_dt = self._parse_date(start_str)
            end_dt = self._parse_date(end_str)

            if not start_dt or not end_dt:
                continue

            if min_date is None or start_dt < min_date:
                min_date = start_dt
            if max_date is None or end_dt > max_date:
                max_date = end_dt

            progress = self._safe_get(r, f"fields.{progress_field}", 0)
            try:
                progress = int(progress)
            except (ValueError, TypeError):
                progress = 0

            dependency = str(self._safe_get(r, f"fields.{dep_field}", "")).strip()

            bars.append({
                "id": r.get("record_id", ""),
                "title": self._safe_get(r, f"fields.{title_field}", "(无标题)"),
                "start": start_dt.strftime("%Y-%m-%d"),
                "end": end_dt.strftime("%Y-%m-%d"),
                "duration_days": (end_dt - start_dt).days,
                "progress": max(0, min(100, progress)),
                "dependency": dependency,
                "fields": r.get("fields", {}),
            })

        # 计算时间轴范围
        if min_date and max_date:
            total_days = (max_date - min_date).days + 1
            # 确保至少 30 天显示
            if total_days < 30:
                max_date = min_date + timedelta(days=29)
                total_days = 30
        else:
            min_date = datetime.now()
            max_date = min_date + timedelta(days=29)
            total_days = 30

        return {
            "view_type": "gantt",
            "total_bars": len(bars),
            "start_date": min_date.strftime("%Y-%m-%d"),
            "end_date": max_date.strftime("%Y-%m-%d"),
            "total_days": total_days,
            "bars": bars,
        }

    def _detect_field(self, fields: List[Dict], keywords: List[str], default: str) -> str:
        """自动识别字段。"""
        field_names = [f.get("name", "") for f in fields]
        for kw in keywords:
            if kw in field_names:
                return kw
        for f in fields:
            if any(kw in f.get("name", "") for kw in keywords) and f.get("name"):
                return f["name"]
        return default if default in field_names else ""

    def _parse_date(self, date_str: str) -> datetime | None:
        """解析日期字符串。"""
        if not date_str:
            return None
        formats = [
            "%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d", "%Y/%m/%d %H:%M", "%Y年%m月%d日",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        return None
