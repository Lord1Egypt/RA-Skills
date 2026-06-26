"""
HTTP 授权服务 - 请求存储

提供授权请求的内存存储和查询能力
"""

import threading
from datetime import datetime
from typing import Optional, Dict, List
from .models import PendingAuthRequest, AuthStatus


class RequestStore:
    """
    授权请求存储
    
    使用内存存储（适合短期请求），支持过期清理
    """
    
    def __init__(self):
        self._requests: Dict[str, PendingAuthRequest] = {}
        self._lock = threading.RLock()
    
    def save(self, request: PendingAuthRequest) -> None:
        """保存请求"""
        with self._lock:
            self._requests[request.request_id] = request
    
    def get(self, request_id: str) -> Optional[PendingAuthRequest]:
        """获取请求"""
        with self._lock:
            request = self._requests.get(request_id)
            if request and self._is_expired(request):
                request.status = AuthStatus.EXPIRED
            return request
    
    def delete(self, request_id: str) -> bool:
        """删除请求"""
        with self._lock:
            if request_id in self._requests:
                del self._requests[request_id]
                return True
            return False
    
    def list_all(self) -> List[PendingAuthRequest]:
        """列出所有请求"""
        with self._lock:
            # 更新过期状态
            for request in self._requests.values():
                if self._is_expired(request):
                    request.status = AuthStatus.EXPIRED
            return list(self._requests.values())
    
    def list_pending(self) -> List[PendingAuthRequest]:
        """列出待处理请求"""
        with self._lock:
            pending = []
            for request in self._requests.values():
                if request.status == AuthStatus.PENDING:
                    if self._is_expired(request):
                        request.status = AuthStatus.EXPIRED
                    else:
                        pending.append(request)
            return pending
    
    def cleanup_expired(self) -> int:
        """清理过期请求，返回清理数量"""
        with self._lock:
            expired_ids = [
                req_id for req_id, req in self._requests.items()
                if self._is_expired(req) or req.status == AuthStatus.EXPIRED
            ]
            for req_id in expired_ids:
                del self._requests[req_id]
            return len(expired_ids)
    
    def _is_expired(self, request: PendingAuthRequest) -> bool:
        """检查请求是否过期"""
        return datetime.now() > request.expires_at
    
    def get_stats(self) -> Dict[str, int]:
        """获取统计信息"""
        with self._lock:
            stats = {
                "total": len(self._requests),
                "pending": 0,
                "confirmed": 0,
                "denied": 0,
                "expired": 0
            }
            for request in self._requests.values():
                status_key = request.status.value
                if status_key in stats:
                    stats[status_key] += 1
            return stats
