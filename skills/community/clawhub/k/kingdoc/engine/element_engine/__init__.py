"""KingDoc 智能画布元素级精细编辑引擎（v3.8.0 新增）

对标腾讯文档·智能画布的元素级编辑：元素查询/新增/更新/删除/Markdown 追加。
实现：金山开放平台「在线文档导出结构化数据」+ 增量追加。
降级：无 API Key 时提供本地 Markdown 编辑器模拟（整文件覆盖追加）。
"""
from __future__ import annotations

from engine.element_engine.editor import CanvasElementEditor

__all__ = ["CanvasElementEditor"]
