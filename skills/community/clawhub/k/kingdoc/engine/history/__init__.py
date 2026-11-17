"""KingDoc 历史管理模块（v3.7.0 新增，合并回收站+版本历史）

统一入口：history list/restore --from trash|version
"""
from __future__ import annotations

from engine.history.manager import HistoryManager

__all__ = ["HistoryManager"]
