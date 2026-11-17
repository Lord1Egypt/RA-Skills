"""KingDoc 日历视图（Calendar View）

按日期字段月/周布局，适合日程/任务排期。
零第三方依赖，自研渲染引擎。
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from engine.views.base import BaseView


class CalendarView(BaseView):
    """日历视图：按日期字段月/周布局。"""

    VIEW_TYPE = "calendar"

    DATE_FIELDS = ["日期", "date", "时间", "time", "开始时间", "截止日期", "deadline", "due"]

    def render(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """渲染日历视图。

        data: {
            "records": [{"fields": {"标题": "会议", "日期": "2026-08-20"}}],
            "fields": [{"name": "标题", "type": "text"}, {"name": "日期", "type": "date"}],
            "mode": "month" | "week"
        }
        """
        records = data.get("records", [])
        fields = data.get("fields", [])
        mode = data.get("mode", "month")
        date_field = self._detect_date_field(fields)
        title_field = self._detect_title_field(fields, date_field)

        # 解析日期并分组
        events = []
        for r in records:
            date_str = str(self._safe_get(r, f"fields.{date_field}", ""))
            title = self._safe_get(r, f"fields.{title_field}", "(无标题)")
            parsed_date = self._parse_date(date_str)
            if parsed_date:
                events.append({
                    "id": r.get("record_id", ""),
                    "title": title,
                    "date": parsed_date,
                    "fields": r.get("fields", {}),
                })

        # 计算月份范围
        if events:
            min_date = min(e["date"] for e in events)
            max_date = max(e["date"] for e in events)
        else:
            min_date = datetime.now()
            max_date = datetime.now()

        # 按天分组
        by_day: Dict[str, List[Dict]] = {}
        for e in events:
            key = e["date"].strftime("%Y-%m-%d")
            if key not in by_day:
                by_day[key] = []
            by_day[key].append({"id": e["id"], "title": e["title"], "fields": e["fields"]})

        # 月视图：生成 6 行 x 7 列日历网格
        grid = self._build_month_grid(min_date, by_day) if mode == "month" else []

        return {
            "view_type": "calendar",
            "date_field": date_field,
            "mode": mode,
            "total_events": len(events),
            "events": by_day,
            "grid": grid,
        }

    def _detect_date_field(self, fields: List[Dict]) -> str:
        """自动识别日期字段。"""
        field_names = [f.get("name", "") for f in fields]
        for candidate in self.DATE_FIELDS:
            if candidate in field_names:
                return candidate
        for f in fields:
            if f.get("type") in ("date", "datetime") and f.get("name"):
                return f["name"]
        return field_names[0] if field_names else "日期"

    def _detect_title_field(self, fields: List[Dict], date_field: str) -> str:
        """自动识别标题字段。"""
        title_keywords = ["标题", "title", "名称", "name", "事件", "event"]
        for kw in title_keywords:
            for f in fields:
                if kw in f.get("name", "") and f.get("name") != date_field:
                    return f["name"]
        for f in fields:
            if f.get("name") != date_field and f.get("type") == "text":
                return f.get("name", "")
        return fields[0].get("name", "") if fields else ""

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

    def _build_month_grid(self, month: datetime, by_day: Dict) -> List[List[Dict]]:
        """构建月视图日历网格（6x7）。"""
        first_day = month.replace(day=1)
        start_offset = first_day.weekday()  # 0=Mon
        # 当月天数
        if month.month == 12:
            days_in_month = (month.replace(year=month.year + 1, month=1, day=1) - timedelta(days=1)).day
        else:
            days_in_month = (month.replace(month=month.month + 1, day=1) - timedelta(days=1)).day

        grid = []
        week = [None] * 7
        day = 1
        for i in range(42):  # 6 rows x 7 cols
            row = i // 7
            col = i % 7
            if i >= start_offset and day <= days_in_month:
                date_key = f"{month.year}-{month.month:02d}-{day:02d}"
                week[col] = {
                    "day": day,
                    "date": date_key,
                    "events": by_day.get(date_key, []),
                }
                day += 1
            else:
                week[col] = None
            if col == 6:
                grid.append(week)
                week = [None] * 7
                if day > days_in_month:
                    break
        return grid
