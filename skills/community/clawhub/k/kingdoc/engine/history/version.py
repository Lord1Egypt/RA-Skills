"""KingDoc 版本历史管理（v3.7.0 整合到历史管理）

版本历史：列出历史版本 + 回滚到指定版本。
所有操作调用金山文档官方 API。
"""
from __future__ import annotations

from typing import Dict, List, Optional


class VersionManager:
    """版本历史管理器。"""

    def __init__(self, backend=None):
        self.backend = backend

    def list_versions(self, file_id: str, limit: int = 20) -> Dict:
        """列出文档历史版本。"""
        if self.backend:
            return self._api_call("kdoc_version_list", file_id=file_id)
        return self._mock_result("version_list", {"file_id": file_id, "versions": []})

    def restore(self, file_id: str, version: int) -> Dict:
        """⚠️ 危险操作：回滚文档到指定历史版本。"""
        if self.backend:
            return self._api_call("kdoc_version_restore", file_id=file_id, version=version)
        return self._mock_result("version_restore", {"file_id": file_id, "version": version, "status": "restored"})

    def get_version_detail(self, file_id: str, version: int) -> Dict:
        """获取某版本详情。"""
        if self.backend:
            return self._api_call("kdoc_version_detail", file_id=file_id, version=version)
        return self._mock_result("version_detail", {"file_id": file_id, "version": version})

    def _api_call(self, method: str, **kwargs) -> Dict:
        """调用后端 API。"""
        try:
            func = getattr(self.backend, method)
            result = func(**kwargs)
            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _mock_result(self, action: str, data) -> Dict:
        return {
            "success": False,
            "action": action,
            "data": data,
            "hint": "需配置金山 App Key 后可用（版本历史为云端功能）",
        }
