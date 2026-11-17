"""KingDoc 回收站管理（v3.7.0 整合到历史管理）

回收站：软删除列表 + 还原 + 彻底删除。
所有操作调用金山文档官方 API。
"""
from __future__ import annotations

from typing import Dict, List, Optional


class TrashManager:
    """回收站管理器。"""

    def __init__(self, backend=None):
        self.backend = backend  # KingDocMcpServer 实例

    def list_trashed(self, limit: int = 20, offset: int = 0) -> Dict:
        """列出回收站文件。"""
        if self.backend:
            return self._api_call("kdoc_trash_list", limit=limit, offset=offset)
        return self._mock_result("trash_list", [])

    def restore(self, file_id: str) -> Dict:
        """从回收站恢复文件。"""
        if self.backend:
            return self._api_call("kdoc_trash_recover", file_id=file_id)
        return self._mock_result("trash_restore", {"file_id": file_id, "status": "restored"})

    def destroy(self, file_id: str) -> Dict:
        """⚠️ 危险操作：彻底删除回收站文件（不可逆）。"""
        if self.backend:
            return self._api_call("kdoc_trash_destroy", file_id=file_id)
        return self._mock_result("trash_destroy", {"file_id": file_id, "status": "destroyed"})

    def _api_call(self, method: str, **kwargs) -> Dict:
        """调用后端 API。"""
        try:
            func = getattr(self.backend, method)
            result = func(**kwargs)
            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _mock_result(self, action: str, data) -> Dict:
        """无后端时的占位结果。"""
        return {
            "success": False,
            "action": action,
            "data": data,
            "hint": "需配置金山 App Key 后可用（回收站为云端功能）",
        }
