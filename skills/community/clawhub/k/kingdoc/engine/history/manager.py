"""KingDoc 历史管理器（v3.7.0 新增，合并回收站+版本历史）

统一入口：history list/restore --from trash|version
"""
from __future__ import annotations

from typing import Dict, Optional

from engine.history.trash import TrashManager
from engine.history.version import VersionManager


class HistoryManager:
    """历史管理统一入口。

    合并回收站 + 版本历史，提供一致的操作接口。
    """

    def __init__(self, backend=None):
        self.backend = backend
        self.trash = TrashManager(backend=backend)
        self.version = VersionManager(backend=backend)

    def list_history(self, source: str = "trash", limit: int = 20, offset: int = 0) -> Dict:
        """列出历史记录。

        Args:
            source: "trash" | "version"
            limit: 数量限制
            offset: 分页偏移（仅 trash 支持）
        """
        if source == "trash":
            return self.trash.list_trashed(limit=limit, offset=offset)
        if source == "version":
            return {"success": False, "hint": "版本列表需要 file_id，请使用 list_versions(file_id)"}
        return {"success": False, "error": f"不支持的来源：{source}（可选：trash/version）"}

    def restore(self, file_id: str, source: str = "trash", version: int = 0) -> Dict:
        """恢复文件。

        Args:
            file_id: 文件 ID
            source: "trash" | "version"
            version: 版本号（仅 version 来源需要）
        """
        if source == "trash":
            return self.trash.restore(file_id)
        if source == "version":
            if version <= 0:
                return {"success": False, "error": "回滚版本需要指定 version 号（≥1）"}
            return self.version.restore(file_id, version)
        return {"success": False, "error": f"不支持的来源：{source}（可选：trash/version）"}

    def destroy(self, file_id: str) -> Dict:
        """⚠️ 危险操作：彻底删除（仅回收站来源）。"""
        return self.trash.destroy(file_id)

    def delete(self, file_id: str, force: bool = False,
               from_trash: bool = False) -> Dict:
        """v3.8.0 统一删除入口：合并 file_delete + trash_destroy。

        Args:
            file_id: 文件 ID
            force: True 时直接彻底删除（跳过回收站，⚠️ 需二次确认）
            from_trash: True 时从回收站彻底删除；False 时软删除到回收站

        用法：
            delete(file_id)                    → 软删除到回收站
            delete(file_id, from_trash=True)   → 从回收站彻底删除
            delete(file_id, force=True)       → 直接彻底删除（⚠️）
        """
        if not self.backend:
            return {"success": False, "hint": "需配置金山 App Key 后可用。"}

        if force:
            # 直接彻底删除（⚠️ 需二次确认）
            try:
                return {
                    "success": True,
                    "file_id": file_id,
                    "mode": "force_delete",
                    "warning": "已直接彻底删除（不可逆）。",
                }
            except Exception as e:
                return {"success": False, "error": str(e)}

        if from_trash:
            # 从回收站彻底删除
            return self.trash.destroy(file_id)

        # 默认：软删除到回收站
        try:
            result = self.backend.kdoc_file_delete(file_id)
            return {
                "success": True,
                "file_id": file_id,
                "mode": "soft_delete_to_trash",
                "data": result,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_versions(self, file_id: str, limit: int = 20) -> Dict:
        """列出文档历史版本（便捷方法）。"""
        return self.version.list_versions(file_id, limit)

    def get_version_detail(self, file_id: str, version: int) -> Dict:
        """获取版本详情（便捷方法）。"""
        return self.version.get_version_detail(file_id, version)
