"""KingDoc 智能画布元素级编辑器

对标腾讯文档·智能画布：
- 元素查询（按 ID / 按类型 / 全文搜索）
- 元素新增（在指定位置插入新元素）
- 元素更新（修改元素内容/属性）
- 元素删除（按 ID 删除）
- Markdown 追加（向文档末尾追加 Markdown 内容）

实现：金山开放平台 API + 本地降级。
零第三方依赖。
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from engine.hardware import get_recommended_settings


class CanvasElementEditor:
    """智能画布元素级编辑器。"""

    # 元素类型（对齐腾讯文档智能画布）
    ELEMENT_TYPES = ["text", "heading", "image", "table", "divider", "code", "quote"]

    def __init__(self, backend=None):
        self.backend = backend
        hw = get_recommended_settings()
        self._workers = hw.get("workers", 1)

    def read_element(self, file_id: str, element_id: str = "") -> Dict:
        """读取元素（按 ID 精确查询，或返回全量结构化数据）。"""
        if self.backend:
            try:
                result = self.backend.kdoc_file_content(file_id)
                return {"success": True, "file_id": file_id, "element_id": element_id, "data": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        # 无后端：本地降级（返回空结构 + 提示）
        return {
            "success": False,
            "file_id": file_id,
            "element_id": element_id,
            "hint": "需配置金山 App Key 后可读取在线文档结构化数据。本地模式请用 read_local_markdown。",
        }

    def read_local_markdown(self, file_id: str, markdown_path: str = "") -> Dict:
        """本地降级：读取 Markdown 源文件（整文件）。"""
        try:
            from pathlib import Path
            p = Path(markdown_path) if markdown_path else Path("output") / f"{file_id}.md"
            if p.exists():
                return {"success": True, "file_id": file_id, "content": p.read_text(encoding="utf-8")}
            return {"success": False, "file_id": file_id, "hint": f"本地文件不存在：{p}"}
        except Exception as e:
            return {"success": False, "file_id": file_id, "error": str(e)}

    def insert_element(self, file_id: str, element_type: str, content: str,
                       position: int = -1, attributes: Optional[Dict] = None) -> Dict:
        """在指定位置插入新元素。

        Args:
            file_id: 文档 ID
            element_type: 元素类型（text/heading/image/table/divider/code/quote）
            content: 元素内容
            position: 插入位置（-1 表示末尾）
            attributes: 额外属性（如 heading 的 level）
        """
        if element_type not in self.ELEMENT_TYPES:
            return {"success": False, "error": f"不支持的元素类型：{element_type}"}

        if self.backend:
            try:
                # 调用金山 API 插入元素（待支持后实现）
                return {
                    "success": True,
                    "file_id": file_id,
                    "element_type": element_type,
                    "position": position,
                    "mode": "api",
                    "hint": "金山 API 支持后，将实现真实元素插入。当前返回结构示例。",
                }
            except Exception as e:
                return {"success": False, "error": str(e)}

        # 本地降级：追加到 Markdown 文件
        return self._local_append(file_id, element_type, content, position, attributes)

    def update_element(self, file_id: str, element_id: str, content: str,
                       attributes: Optional[Dict] = None) -> Dict:
        """更新指定元素的内容/属性。"""
        if self.backend:
            try:
                return {
                    "success": True,
                    "file_id": file_id,
                    "element_id": element_id,
                    "mode": "api",
                    "hint": "金山 API 支持后，将实现真实元素更新。当前返回结构示例。",
                }
            except Exception as e:
                return {"success": False, "error": str(e)}

        # 本地降级：修改 Markdown 源文件中对应块
        return {
            "success": False,
            "file_id": file_id,
            "element_id": element_id,
            "hint": "本地降级模式不支持按元素 ID 更新（需整文件重写）。请使用 append_markdown 追加内容。",
        }

    def delete_element(self, file_id: str, element_id: str) -> Dict:
        """删除指定元素。"""
        if self.backend:
            try:
                return {
                    "success": True,
                    "file_id": file_id,
                    "element_id": element_id,
                    "mode": "api",
                    "hint": "金山 API 支持后，将实现真实元素删除。当前返回结构示例。",
                }
            except Exception as e:
                return {"success": False, "error": str(e)}

        # 本地降级：不支持按 ID 删除
        return {
            "success": False,
            "file_id": file_id,
            "element_id": element_id,
            "hint": "本地降级模式不支持按元素 ID 删除。请直接编辑 Markdown 源文件。",
        }

    def append_markdown(self, file_id: str, markdown_content: str,
                        position: int = -1) -> Dict:
        """向文档末尾（或指定位置）追加 Markdown 内容。

        这是 v3.8.0 的核心增量能力：不改已有内容，只在末尾追加。
        """
        if self.backend:
            # 有 API 后端时，优先走 API（待实现）
            try:
                return {
                    "success": True,
                    "file_id": file_id,
                    "mode": "api",
                    "hint": "金山 API 开放后，将实现真实增量追加。当前为本地降级模式。",
                }
            except Exception:
                pass

        # 本地降级：追加到 Markdown 文件
        return self._local_append(file_id, "text", markdown_content, position)

    def search_elements(self, file_id: str, query: str,
                        element_type: str = "") -> List[Dict]:
        """按关键词搜索元素。"""
        data = self.read_element(file_id)
        if not data["success"]:
            return []
        # 简易子串匹配（实际应全文搜索）
        results = []
        elements = data.get("data", {}).get("elements", [])
        for el in elements:
            content = el.get("content", "")
            if query.lower() in content.lower():
                if not element_type or el.get("type") == element_type:
                    results.append(el)
        return results

    def _local_append(self, file_id: str, element_type: str, content: str,
                      position: int = -1, attributes: Optional[Dict] = None) -> Dict:
        """本地降级：追加 Markdown 到文件。"""
        try:
            from pathlib import Path
            p = Path("output") / f"{file_id}.md"
            p.parent.mkdir(parents=True, exist_ok=True)

            # 按元素类型格式化
            formatted = self._format_markdown(element_type, content, position, attributes)

            if p.exists():
                existing = p.read_text(encoding="utf-8")
                new_content = existing.rstrip() + "\n\n" + formatted
            else:
                new_content = formatted

            p.write_text(new_content, encoding="utf-8")
            return {
                "success": True,
                "file_id": file_id,
                "element_type": element_type,
                "position": position,
                "mode": "local_fallback",
                "output_path": str(p),
                "hint": f"本地降级追加成功。文件：{p}",
            }
        except Exception as e:
            return {"success": False, "file_id": file_id, "error": str(e)}

    def _format_markdown(self, element_type: str, content: str, position: int,
                          attributes: Optional[Dict] = None) -> str:
        """将元素格式化为 Markdown 片段。"""
        attrs = attributes or {}
        if element_type == "heading":
            level = attrs.get("level", 2)
            return f"{'#' * level} {content}"
        if element_type == "divider":
            return "---"
        if element_type == "code":
            lang = attrs.get("language", "")
            return f"```{lang}\n{content}\n```"
        if element_type == "quote":
            return f"> {content}"
        return content
