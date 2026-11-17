"""KingDoc 视图基类"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


class BaseView:
    """多维表格视图基类。"""

    VIEW_TYPE: str = "base"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    def render(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """渲染视图，子类必须实现。"""
        raise NotImplementedError

    def _safe_get(self, record: Dict, field: str, default: Any = "") -> Any:
        """兼容嵌套字段（如 fields.标题）"""
        keys = field.split(".")
        cur = record
        for k in keys:
            if isinstance(cur, dict):
                cur = cur.get(k, default)
            else:
                return default
        return cur if cur is not None else default

    def _collect_field_values(self, records: List[Dict], field: str) -> List[Any]:
        """收集某字段所有非空值（用于自动推断分组字段）"""
        seen = set()
        values = []
        for r in records:
            v = self._safe_get(r, field)
            if v and v not in seen:
                seen.add(v)
                values.append(v)
        return values
