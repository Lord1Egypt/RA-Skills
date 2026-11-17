"""KingDoc 块级编辑引擎

v3.9.0 新增：以 block_id 为操作主键，封装金山开放平台块接口。
实现段落级在线编辑替代整文件替换。

能力：
- 拉取文档块列表（blocks_list）
- 按 block_id 执行替换（block_replace）
- 按 block_id 执行插入（block_insert）
- 按 block_id 执行删除（block_delete）
- 按 block_id 执行移动（block_move）
- 内置块类型映射表（段落/标题/列表/表格）
- 未知块类型跳过并提示而非报错中断
- 本地降级优先（无 API 时返回友好提示）

设计原则：
- 零第三方依赖（仅标准库）
- 硬件自适应（批量操作时读取 hardware.py）
- 零密钥可用（本地降级模式）
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 块类型映射表：金山 API block_type → 内部类型
BLOCK_TYPE_MAP: Dict[str, str] = {
    "paragraph": "paragraph",
    "heading": "heading",
    "list": "list",
    "table": "table",
    "image": "image",
    "divider": "divider",
    "code": "code",
    "quote": "quote",
    "todo": "todo",
    "callout": "callout",
    "equation": "equation",
    "toc": "toc",
    "column": "column",
    "column_set": "column_set",
    "file": "file",
    "video": "video",
    "audio": "audio",
    "embed": "embed",
    "mindmap": "mindmap",
    "baike": "baike",
    "board": "board",
    "undefined": "unknown",
}

# 内部类型 → 默认内容模板
BLOCK_TEMPLATES: Dict[str, str] = {
    "paragraph": "",
    "heading": "",
    "list": "",
    "table": "",
    "image": "",
    "divider": "---",
    "code": "",
    "quote": "",
    "todo": "",
    "callout": "",
    "equation": "",
    "toc": "",
    "column": "",
    "column_set": "",
    "file": "",
    "video": "",
    "audio": "",
    "embed": "",
    "mindmap": "",
    "baike": "",
    "board": "",
    "unknown": "",
}


class BlockEditor:
    """块级编辑器

    封装金山开放平台块接口，提供段落级在线编辑能力。
    本地降级模式下返回友好提示，不调用外部 API。
    """

    def __init__(self, backend: Optional[Any] = None):
        self.backend = backend
        self._local_mode = backend is None
        self._unknown_types: List[str] = []  # 记录未知块类型

    @property
    def is_local_mode(self) -> bool:
        return self._local_mode

    def _get_block_type(self, block: Dict) -> str:
        """获取块的类型，未知类型返回 'unknown'"""
        raw_type = block.get("type", "undefined")
        mapped = BLOCK_TYPE_MAP.get(raw_type, "unknown")
        if mapped == "unknown" and raw_type not in self._unknown_types:
            self._unknown_types.append(raw_type)
        return mapped

    def _get_block_text(self, block: Dict) -> str:
        """提取块的文本内容"""
        block_type = self._get_block_type(block)
        content = block.get("content", {})

        if block_type == "paragraph":
            texts = content.get("text", [])
            return "".join(t.get("text", "") for t in texts if isinstance(t, dict))
        elif block_type == "heading":
            texts = content.get("text", [])
            level = content.get("level", 1)
            text = "".join(t.get("text", "") for t in texts if isinstance(t, dict))
            return f"{'#' * level} {text}"
        elif block_type == "list":
            items = content.get("items", [])
            return "\n".join(f"- {item}" for item in items if item)
        elif block_type == "code":
            return content.get("code", "")
        elif block_type == "quote":
            return content.get("text", "")
        elif block_type == "divider":
            return "---"
        elif block_type == "todo":
            checked = "x" if content.get("checked", False) else " "
            text = content.get("text", "")
            return f"- [{checked}] {text}"
        else:
            # 未知类型：返回原始 JSON 摘要
            return f"[{block_type}]"

    def blocks_list(self, file_id: str) -> Dict:
        """拉取文档块列表

        Args:
            file_id: 文档 ID

        Returns:
            {"blocks": [...], "total": int, "unknown_types": [...]}
        """
        if self._local_mode:
            return {
                "success": False,
                "error": "本地降级模式：无法拉取块列表",
                "hint": "请配置金山 App Key 后使用 kdoc.block.list",
                "blocks": [],
                "total": 0,
                "unknown_types": [],
            }

        try:
            result = self.backend.kdoc_block_list(file_id)
            blocks = result.get("blocks", [])
            # 标记未知类型
            self._unknown_types = []
            for block in blocks:
                self._get_block_type(block)
            return {
                "success": True,
                "file_id": file_id,
                "blocks": blocks,
                "total": len(blocks),
                "unknown_types": list(self._unknown_types),
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"拉取块列表失败: {e}",
                "blocks": [],
                "total": 0,
                "unknown_types": [],
            }

    def block_replace(self, file_id: str, block_id: str, content: str,
                      block_type: str = "paragraph") -> Dict:
        """按 block_id 替换块内容

        Args:
            file_id: 文档 ID
            block_id: 块 ID
            content: 新内容
            block_type: 块类型（默认 paragraph）

        Returns:
            {"success": bool, "block_id": str, "message": str}
        """
        if self._local_mode:
            return {
                "success": False,
                "error": "本地降级模式：无法替换块",
                "hint": "请配置金山 App Key 后使用 kdoc.block.replace",
                "block_id": block_id,
            }

        # 检查块类型是否已知
        if block_type not in BLOCK_TYPE_MAP and block_type != "paragraph":
            return {
                "success": False,
                "error": f"未知块类型: {block_type}",
                "hint": f"已知类型: {list(BLOCK_TYPE_MAP.keys())}",
                "block_id": block_id,
                "skipped": True,
            }

        try:
            result = self.backend.kdoc_block_replace(file_id, block_id, content, block_type)
            return {
                "success": True,
                "file_id": file_id,
                "block_id": block_id,
                "message": f"块 {block_id} 已替换",
                "data": result,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"替换块失败: {e}",
                "block_id": block_id,
            }

    def block_insert(self, file_id: str, block_id: str, content: str,
                     position: str = "after", block_type: str = "paragraph") -> Dict:
        """按 block_id 插入新块

        Args:
            file_id: 文档 ID
            block_id: 参考块 ID（在此块之后/之前插入）
            content: 新块内容
            position: after（之后）或 before（之前）
            block_type: 块类型

        Returns:
            {"success": bool, "block_id": str, "new_block_id": str}
        """
        if self._local_mode:
            return {
                "success": False,
                "error": "本地降级模式：无法插入块",
                "hint": "请配置金山 App Key 后使用 kdoc.block.insert",
                "block_id": block_id,
            }

        if block_type not in BLOCK_TYPE_MAP and block_type != "paragraph":
            return {
                "success": False,
                "error": f"未知块类型: {block_type}",
                "skipped": True,
            }

        try:
            result = self.backend.kdoc_block_insert(file_id, block_id, content, position, block_type)
            new_block_id = result.get("block_id", "")
            return {
                "success": True,
                "file_id": file_id,
                "block_id": block_id,
                "new_block_id": new_block_id,
                "message": f"已在 {block_id} {position} 插入新块",
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"插入块失败: {e}",
                "block_id": block_id,
            }

    def block_delete(self, file_id: str, block_id: str) -> Dict:
        """按 block_id 删除块

        Args:
            file_id: 文档 ID
            block_id: 块 ID

        Returns:
            {"success": bool, "block_id": str}
        """
        if self._local_mode:
            return {
                "success": False,
                "error": "本地降级模式：无法删除块",
                "hint": "请配置金山 App Key 后使用 kdoc.block.delete",
                "block_id": block_id,
            }

        try:
            result = self.backend.kdoc_block_delete(file_id, block_id)
            return {
                "success": True,
                "file_id": file_id,
                "block_id": block_id,
                "message": f"块 {block_id} 已删除",
                "data": result,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"删除块失败: {e}",
                "block_id": block_id,
            }

    def block_move(self, file_id: str, block_id: str,
                   target_block_id: str, position: str = "after") -> Dict:
        """按 block_id 移动块

        Args:
            file_id: 文档 ID
            block_id: 要移动的块 ID
            target_block_id: 目标块 ID
            position: after 或 before

        Returns:
            {"success": bool, "block_id": str}
        """
        if self._local_mode:
            return {
                "success": False,
                "error": "本地降级模式：无法移动块",
                "hint": "请配置金山 App Key 后使用 kdoc.block.move",
                "block_id": block_id,
            }

        try:
            result = self.backend.kdoc_block_move(file_id, block_id, target_block_id, position)
            return {
                "success": True,
                "file_id": file_id,
                "block_id": block_id,
                "target_block_id": target_block_id,
                "position": position,
                "message": f"块 {block_id} 已移动到 {target_block_id} {position}",
                "data": result,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"移动块失败: {e}",
                "block_id": block_id,
            }

    def batch_replace(self, file_id: str, replacements: List[Dict]) -> Dict:
        """批量替换块（硬件自适应削峰）

        Args:
            file_id: 文档 ID
            replacements: [{"block_id": str, "content": str, "block_type": str}]

        Returns:
            {"success": bool, "total": int, "succeeded": int, "failed": int, "errors": [...]}
        """
        if self._local_mode:
            return {
                "success": False,
                "error": "本地降级模式：无法批量替换块",
                "hint": "请配置金山 App Key 后使用 kdoc.block.batch_replace",
                "total": len(replacements),
                "succeeded": 0,
                "failed": len(replacements),
                "errors": [],
            }

        # 硬件自适应：读取并发限制
        try:
            from engine.hardware import get_recommended_settings
            settings = get_recommended_settings()
            max_workers = settings.get("workers", 4)
        except Exception:
            max_workers = 4

        succeeded = 0
        failed = 0
        errors = []

        # 分批处理，每批不超过 max_workers
        for i in range(0, len(replacements), max_workers):
            batch = replacements[i:i + max_workers]
            for item in batch:
                block_id = item.get("block_id", "")
                content = item.get("content", "")
                block_type = item.get("block_type", "paragraph")
                result = self.block_replace(file_id, block_id, content, block_type)
                if result.get("success"):
                    succeeded += 1
                else:
                    failed += 1
                    errors.append({"block_id": block_id, "error": result.get("error", "")})

        return {
            "success": failed == 0,
            "file_id": file_id,
            "total": len(replacements),
            "succeeded": succeeded,
            "failed": failed,
            "errors": errors,
        }

    def get_unknown_types(self) -> List[str]:
        """获取遇到的未知块类型列表"""
        return list(self._unknown_types)

    def get_block_type_map(self) -> Dict[str, str]:
        """获取块类型映射表"""
        return dict(BLOCK_TYPE_MAP)


def list_blocks(backend: Optional[Any] = None, file_id: str = "") -> Dict:
    """便捷函数：拉取块列表"""
    editor = BlockEditor(backend)
    return editor.blocks_list(file_id)


def replace_block(backend: Optional[Any] = None, file_id: str = "",
                  block_id: str = "", content: str = "",
                  block_type: str = "paragraph") -> Dict:
    """便捷函数：替换块"""
    editor = BlockEditor(backend)
    return editor.block_replace(file_id, block_id, content, block_type)


def insert_block(backend: Optional[Any] = None, file_id: str = "",
                 block_id: str = "", content: str = "",
                 position: str = "after", block_type: str = "paragraph") -> Dict:
    """便捷函数：插入块"""
    editor = BlockEditor(backend)
    return editor.block_insert(file_id, block_id, content, position, block_type)


def delete_block(backend: Optional[Any] = None, file_id: str = "",
                 block_id: str = "") -> Dict:
    """便捷函数：删除块"""
    editor = BlockEditor(backend)
    return editor.block_delete(file_id, block_id)


def move_block(backend: Optional[Any] = None, file_id: str = "",
               block_id: str = "", target_block_id: str = "",
               position: str = "after") -> Dict:
    """便捷函数：移动块"""
    editor = BlockEditor(backend)
    return editor.block_move(file_id, block_id, target_block_id, position)
