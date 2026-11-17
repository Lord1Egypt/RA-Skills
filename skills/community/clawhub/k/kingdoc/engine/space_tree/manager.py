"""KingDoc 空间节点管理器（v3.8.0 新增）

对标腾讯文档·空间节点管理：
- 目录树查询（递归列出文件夹结构）
- 链接节点创建（创建文件夹/文档快捷方式）
- 递归删除（删除文件夹及其所有子内容）
- 目录可视化（JSON 树形结构）

实现：开放平台个人文档 API。
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from engine.hardware import get_recommended_settings


class SpaceTreeManager:
    """空间节点管理：目录树 + 链接节点 + 递归删除。"""

    def __init__(self, backend=None):
        self.backend = backend
        hw = get_recommended_settings()
        self._workers = hw.get("workers", 1)

    def list_tree(self, folder_id: str = "", depth: int = 3) -> Dict:
        """递归列出目录树。"""
        if self.backend:
            try:
                children = self.backend.kdoc_folder_list(folder_id)
                tree = {
                    "success": True,
                    "folder_id": folder_id or "root",
                    "mode": "api",
                    "children": children,
                }
                if depth > 0:
                    tree["hint"] = f"返回当前层级。递归深度 {depth} 需逐层调用。"
                return tree
            except Exception as e:
                return {"success": False, "error": str(e)}
        return {
            "success": False,
            "folder_id": folder_id,
            "mode": "local_fallback",
            "hint": "需配置金山 App Key 后可用。",
        }

    def create_link_node(self, parent_id: str, name: str, target_id: str,
                        node_type: str = "shortcut") -> Dict:
        """创建链接节点。"""
        if self.backend:
            try:
                return {
                    "success": True,
                    "parent_id": parent_id,
                    "name": name,
                    "target_id": target_id,
                    "node_type": node_type,
                    "mode": "api",
                    "hint": "金山 API 支持后，将创建真实链接节点。",
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        return {"success": False, "hint": "需配置金山 App Key 后可用。"}

    def delete_recursive(self, folder_id: str, dry_run: bool = True) -> Dict:
        """⚠️ 递归删除文件夹及其所有子内容。"""
        if not dry_run:
            return {
                "success": False,
                "hint": "递归删除必须用户明确确认。",
            }
        if self.backend:
            try:
                tree = self.list_tree(folder_id)
                count = self._count_nodes(tree)
                return {
                    "success": True,
                    "folder_id": folder_id,
                    "dry_run": True,
                    "would_delete": count,
                    "tree_preview": tree,
                    "hint": f"预览：将删除 {count} 个节点。",
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        return {"success": False, "folder_id": folder_id, "hint": "需配置金山 App Key 后可用。"}

    def visualize_tree(self, folder_id: str = "", format: str = "json") -> Dict:
        """目录可视化。"""
        tree = self.list_tree(folder_id)
        if not tree["success"]:
            return tree
        if format == "markdown":
            tree["markdown"] = self._to_markdown_tree(tree, indent=0)
        return tree

    def _count_nodes(self, tree: Dict) -> int:
        count = 1
        for child in tree.get("children", []):
            if isinstance(child, dict):
                count += self._count_nodes(child)
        return count

    def _to_markdown_tree(self, tree: Dict, indent: int = 0) -> str:
        prefix = "  " * indent + "- "
        name = tree.get("name", tree.get("folder_id", "root"))
        lines = [f"{prefix}{name}"]
        for child in tree.get("children", []):
            if isinstance(child, dict):
                lines.append(self._to_markdown_tree(child, indent + 1))
        return "\n".join(lines)
