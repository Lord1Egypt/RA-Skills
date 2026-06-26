"""
批量审批模块

支持批量授权请求：
- 创建批量授权请求（将多个文件打包为一个审批项）
- 批量确认/拒绝
- 批量查询状态
- 批量审批的Web UI
"""

import json
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class BulkAuthStatus(Enum):
    """批量授权状态"""
    PENDING = "pending"       # 待审批
    CONFIRMED = "confirmed"   # 已批准
    DENIED = "denied"         # 已拒绝
    PARTIAL = "partial"       # 部分批准
    EXPIRED = "expired"       # 已过期


@dataclass
class BulkAuthItem:
    """
    批量授权中的单个项目
    """
    item_id: str
    resource_path: str
    operation: str
    data_level: str
    original_level: str           # 原始级别（用于升级场景）
    adjusted_level: str           # 调整后级别
    is_upgraded: bool             # 是否触发升级
    status: str = "pending"       # pending, approved, denied
    note: str = ""


@dataclass
class BulkAuthRequest:
    """
    批量授权请求
    
    将多个文件的访问请求打包为一个审批项
    """
    request_id: str
    agent_id: str
    operation: str
    items: List[BulkAuthItem]
    
    # 汇总信息
    total_count: int
    upgraded_count: int
    max_level: str
    
    # 状态
    status: BulkAuthStatus
    created_at: datetime
    expires_at: datetime
    
    # 审批结果
    confirmed_at: Optional[datetime] = None
    confirmed_by: Optional[str] = None
    approved_items: List[str] = field(default_factory=list)
    denied_items: List[str] = field(default_factory=list)
    
    # 上下文
    context: Dict[str, Any] = field(default_factory=dict)
    
    def get_summary(self) -> Dict[str, Any]:
        """获取摘要信息"""
        approved = len(self.approved_items)
        denied = len(self.denied_items)
        pending = self.total_count - approved - denied
        
        return {
            "request_id": self.request_id,
            "status": self.status.value,
            "total": self.total_count,
            "upgraded": self.upgraded_count,
            "approved": approved,
            "denied": denied,
            "pending": pending,
            "max_level": self.max_level
        }


class BulkRequestStore:
    """
    批量请求存储
    """
    
    def __init__(self):
        self._requests: Dict[str, BulkAuthRequest] = {}
    
    def save(self, request: BulkAuthRequest):
        """保存请求"""
        self._requests[request.request_id] = request
    
    def get(self, request_id: str) -> Optional[BulkAuthRequest]:
        """获取请求"""
        request = self._requests.get(request_id)
        if request and self._is_expired(request):
            request.status = BulkAuthStatus.EXPIRED
        return request
    
    def list_all(self) -> List[BulkAuthRequest]:
        """列出所有请求"""
        return list(self._requests.values())
    
    def list_pending(self) -> List[BulkAuthRequest]:
        """列出待处理请求"""
        return [
            r for r in self._requests.values()
            if r.status == BulkAuthStatus.PENDING
        ]
    
    def delete(self, request_id: str) -> bool:
        """删除请求"""
        if request_id in self._requests:
            del self._requests[request_id]
            return True
        return False
    
    def cleanup_expired(self) -> int:
        """清理过期请求"""
        expired_ids = [
            rid for rid, req in self._requests.items()
            if self._is_expired(req)
        ]
        for rid in expired_ids:
            del self._requests[rid]
        return len(expired_ids)
    
    def _is_expired(self, request: BulkAuthRequest) -> bool:
        """检查是否过期"""
        return datetime.now() > request.expires_at


class BulkAuthorizationService:
    """
    批量授权服务
    
    管理批量授权请求的生命周期
    """
    
    def __init__(self, request_store: Optional[BulkRequestStore] = None):
        self.store = request_store or BulkRequestStore()
        self._timeout_seconds = 300  # 默认5分钟超时
    
    def create_bulk_request(self,
                           agent_id: str,
                           items: List[Dict[str, Any]],
                           operation: str,
                           context: Optional[Dict[str, Any]] = None) -> BulkAuthRequest:
        """
        创建批量授权请求
        
        Args:
            agent_id: Agent ID
            items: 项目列表，每项包含 resource_path, data_level, is_upgraded 等
            operation: 操作类型
            context: 额外上下文
        
        Returns:
            BulkAuthRequest 对象
        """
        request_id = f"BULK-{secrets.token_hex(6)}"
        
        # 创建子项目
        bulk_items = []
        upgraded_count = 0
        max_level = "L1-PUBLIC"
        
        for i, item_data in enumerate(items):
            item = BulkAuthItem(
                item_id=f"{request_id}-{i:03d}",
                resource_path=item_data["resource_path"],
                operation=operation,
                data_level=item_data.get("adjusted_level", item_data["data_level"]),
                original_level=item_data["data_level"],
                adjusted_level=item_data.get("adjusted_level", item_data["data_level"]),
                is_upgraded=item_data.get("is_upgraded", False),
                note=item_data.get("note", "")
            )
            bulk_items.append(item)
            
            if item.is_upgraded:
                upgraded_count += 1
            
            # 跟踪最高级别
            if self._level_strictness(item.adjusted_level) > self._level_strictness(max_level):
                max_level = item.adjusted_level
        
        request = BulkAuthRequest(
            request_id=request_id,
            agent_id=agent_id,
            operation=operation,
            items=bulk_items,
            total_count=len(bulk_items),
            upgraded_count=upgraded_count,
            max_level=max_level,
            status=BulkAuthStatus.PENDING,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(seconds=self._timeout_seconds),
            context=context or {}
        )
        
        self.store.save(request)
        return request
    
    def confirm_bulk(self,
                    request_id: str,
                    user_identifier: Optional[str] = None,
                    approved_item_ids: Optional[List[str]] = None) -> bool:
        """
        确认批量授权
        
        Args:
            request_id: 请求ID
            user_identifier: 用户标识
            approved_item_ids: 指定批准的项目ID（None=全部批准）
        
        Returns:
            是否成功
        """
        request = self.store.get(request_id)
        if not request or request.status != BulkAuthStatus.PENDING:
            return False
        
        if approved_item_ids is None:
            # 全部批准
            approved_item_ids = [item.item_id for item in request.items]
        
        # 更新项目状态
        for item in request.items:
            if item.item_id in approved_item_ids:
                item.status = "approved"
                request.approved_items.append(item.item_id)
            else:
                item.status = "denied"
                request.denied_items.append(item.item_id)
        
        # 更新请求状态
        if len(request.approved_items) == request.total_count:
            request.status = BulkAuthStatus.CONFIRMED
        elif len(request.approved_items) > 0:
            request.status = BulkAuthStatus.PARTIAL
        else:
            request.status = BulkAuthStatus.DENIED
        
        request.confirmed_at = datetime.now()
        request.confirmed_by = user_identifier
        
        self.store.save(request)
        return True
    
    def deny_bulk(self, request_id: str, user_identifier: Optional[str] = None) -> bool:
        """
        拒绝批量授权
        
        Args:
            request_id: 请求ID
            user_identifier: 用户标识
        
        Returns:
            是否成功
        """
        request = self.store.get(request_id)
        if not request or request.status != BulkAuthStatus.PENDING:
            return False
        
        # 更新所有项目状态
        for item in request.items:
            item.status = "denied"
            request.denied_items.append(item.item_id)
        
        request.status = BulkAuthStatus.DENIED
        request.confirmed_at = datetime.now()
        request.confirmed_by = user_identifier
        
        self.store.save(request)
        return True
    
    def get_request_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """
        获取请求状态
        
        Returns:
            状态字典，包含摘要和项目详情
        """
        request = self.store.get(request_id)
        if not request:
            return None
        
        summary = request.get_summary()
        summary["items"] = [
            {
                "item_id": item.item_id,
                "resource_path": item.resource_path,
                "level": item.adjusted_level,
                "is_upgraded": item.is_upgraded,
                "status": item.status
            }
            for item in request.items
        ]
        summary["created_at"] = request.created_at.isoformat()
        summary["expires_at"] = request.expires_at.isoformat()
        
        return summary
    
    def list_requests(self, agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        列出批量请求
        
        Args:
            agent_id: 可选的Agent过滤
        
        Returns:
            请求摘要列表
        """
        requests = self.store.list_all()
        if agent_id:
            requests = [r for r in requests if r.agent_id == agent_id]
        
        return [r.get_summary() for r in requests]
    
    def _level_strictness(self, level: str) -> int:
        """获取级别严格度"""
        level_order = {
            "L1-PUBLIC": 1,
            "L2-INTERNAL": 2,
            "L3-RESTRICTED": 3,
            "L4-CONFIDENTIAL": 4,
            "L5-SECRET": 5,
            "L6-CRITICAL": 6
        }
        return level_order.get(level, 0)


class BulkAuthAPI:
    """
    批量授权 API 接口
    
    提供 HTTP API 用于批量授权管理
    """
    
    def __init__(self, service: BulkAuthorizationService):
        self.service = service
    
    def handle_create_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """处理创建批量请求"""
        try:
            request = self.service.create_bulk_request(
                agent_id=data.get("agent_id", "unknown"),
                items=data.get("items", []),
                operation=data.get("operation", "READ"),
                context=data.get("context", {})
            )
            
            return {
                "success": True,
                "request_id": request.request_id,
                "summary": request.get_summary(),
                "confirmation_url": f"/ui/bulk/{request.request_id}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def handle_confirm(self, request_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """处理确认请求"""
        success = self.service.confirm_bulk(
            request_id=request_id,
            user_identifier=data.get("user_identifier"),
            approved_item_ids=data.get("approved_item_ids")
        )
        
        if success:
            status = self.service.get_request_status(request_id)
            return {
                "success": True,
                "status": status,
                "message": f"已批准 {len(status.get('approved_items', []))} 个项目"
            }
        else:
            return {"success": False, "error": "确认失败，请求可能不存在或已处理"}
    
    def handle_deny(self, request_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """处理拒绝请求"""
        success = self.service.deny_bulk(
            request_id=request_id,
            user_identifier=data.get("user_identifier")
        )
        
        if success:
            return {
                "success": True,
                "status": self.service.get_request_status(request_id),
                "message": "已拒绝批量请求"
            }
        else:
            return {"success": False, "error": "拒绝失败，请求可能不存在或已处理"}
    
    def handle_get_status(self, request_id: str) -> Dict[str, Any]:
        """处理查询状态请求"""
        status = self.service.get_request_status(request_id)
        
        if status:
            return {"success": True, "status": status}
        else:
            return {"success": False, "error": "请求不存在"}
    
    def handle_list(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """处理列表请求"""
        requests = self.service.list_requests(agent_id)
        return {"success": True, "requests": requests}


def generate_bulk_auth_page(request: BulkAuthRequest, port: int) -> str:
    """
    生成批量授权 Web UI HTML
    
    Args:
        request: 批量授权请求
        port: HTTP 服务端口
    
    Returns:
        HTML 字符串
    """
    summary = request.get_summary()
    
    # 级别颜色
    level_colors = {
        "L1-PUBLIC": "#27ae60",
        "L2-INTERNAL": "#3498db",
        "L3-RESTRICTED": "#f39c12",
        "L4-CONFIDENTIAL": "#e67e22",
        "L5-SECRET": "#e74c3c",
        "L6-CRITICAL": "#c0392b"
    }
    
    # 生成项目列表HTML
    items_html = ""
    for item in request.items:
        color = level_colors.get(item.adjusted_level, "#3498db")
        upgrade_badge = "🔄 " if item.is_upgraded else ""
        items_html += f"""
        <div class="item-row" data-item-id="{item.item_id}">
            <input type="checkbox" class="item-checkbox" checked onchange="updateSummary()">
            <span class="item-path">{item.resource_path}</span>
            <span class="level-badge" style="background: {color}20; color: {color}">
                {upgrade_badge}{item.adjusted_level}
            </span>
        </div>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>批量授权请求 - OpenClaw</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 800px;
                margin: 30px auto;
                padding: 20px;
                background: #f5f5f5;
            }}
            .card {{
                background: white;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .header {{
                display: flex;
                align-items: center;
                margin-bottom: 24px;
                padding-bottom: 20px;
                border-bottom: 2px solid #eee;
            }}
            .icon {{
                width: 48px;
                height: 48px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 24px;
                margin-right: 16px;
            }}
            h1 {{ margin: 0; font-size: 22px; color: #333; }}
            .subtitle {{ color: #666; font-size: 14px; margin-top: 4px; }}
            .summary-box {{
                background: #f8f9fa;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 20px;
            }}
            .summary-row {{
                display: flex;
                justify-content: space-between;
                margin: 8px 0;
                font-size: 14px;
            }}
            .summary-label {{ color: #666; }}
            .summary-value {{ font-weight: 600; color: #333; }}
            .highlight {{ color: #e74c3c; }}
            .items-list {{
                max-height: 400px;
                overflow-y: auto;
                border: 1px solid #eee;
                border-radius: 8px;
                margin: 20px 0;
            }}
            .item-row {{
                display: flex;
                align-items: center;
                padding: 12px 16px;
                border-bottom: 1px solid #f0f0f0;
            }}
            .item-row:last-child {{ border-bottom: none; }}
            .item-checkbox {{
                margin-right: 12px;
                width: 18px;
                height: 18px;
                cursor: pointer;
            }}
            .item-path {{
                flex: 1;
                font-family: monospace;
                font-size: 13px;
                color: #333;
            }}
            .level-badge {{
                padding: 4px 10px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 600;
            }}
            .actions {{
                display: flex;
                gap: 12px;
                margin-top: 24px;
            }}
            button {{
                flex: 1;
                padding: 14px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
            }}
            button:hover {{ opacity: 0.9; transform: translateY(-1px); }}
            .btn-allow {{ background: #27ae60; color: white; }}
            .btn-deny {{ background: #e74c3c; color: white; }}
            .btn-select {{
                background: #f0f0f0;
                color: #666;
                font-size: 14px;
                padding: 8px 16px;
                flex: none;
            }}
            .selection-controls {{
                display: flex;
                gap: 8px;
                margin-bottom: 12px;
            }}
            .result {{
                text-align: center;
                padding: 40px;
                font-size: 18px;
            }}
            .result.success {{ color: #27ae60; }}
            .result.error {{ color: #e74c3c; }}
            .warning {{
                background: #fff3cd;
                border: 1px solid #ffc107;
                color: #856404;
                padding: 12px 16px;
                border-radius: 8px;
                margin-bottom: 16px;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="card" id="card">
            <div class="header">
                <div class="icon">📦</div>
                <div>
                    <h1>批量授权请求</h1>
                    <div class="subtitle">Agent "{request.agent_id}" 请求批量访问文件</div>
                </div>
            </div>
            
            <div class="summary-box">
                <div class="summary-row">
                    <span class="summary-label">操作类型</span>
                    <span class="summary-value">{request.operation}</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">文件总数</span>
                    <span class="summary-value">{summary['total']}</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">级别升级</span>
                    <span class="summary-value highlight">{summary['upgraded']} 个文件</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">最高级别</span>
                    <span class="summary-value">{summary['max_level']}</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">待批准</span>
                    <span class="summary-value" id="pending-count">{summary['total']}</span>
                </div>
            </div>
            
            {f'<div class="warning">⚠️ 注意：{summary["upgraded"]} 个文件因批量操作触发级别升级，需要额外确认</div>' if summary['upgraded'] > 0 else ''}
            
            <div class="selection-controls">
                <button class="btn-select" onclick="selectAll()">全选</button>
                <button class="btn-select" onclick="deselectAll()">全不选</button>
                <button class="btn-select" onclick="selectUpgraded()">仅升级项</button>
            </div>
            
            <div class="items-list">
                {items_html}
            </div>
            
            <div class="actions">
                <button class="btn-deny" onclick="deny()">拒绝全部</button>
                <button class="btn-allow" onclick="allow()">批准选中</button>
            </div>
        </div>
        
        <script>
            function updateSummary() {{
                const checkboxes = document.querySelectorAll('.item-checkbox');
                const checked = document.querySelectorAll('.item-checkbox:checked');
                document.getElementById('pending-count').textContent = checked.length;
            }}
            
            function selectAll() {{
                document.querySelectorAll('.item-checkbox').forEach(cb => cb.checked = true);
                updateSummary();
            }}
            
            function deselectAll() {{
                document.querySelectorAll('.item-checkbox').forEach(cb => cb.checked = false);
                updateSummary();
            }}
            
            function selectUpgraded() {{
                document.querySelectorAll('.item-row').forEach(row => {{
                    const badge = row.querySelector('.level-badge');
                    const checkbox = row.querySelector('.item-checkbox');
                    checkbox.checked = badge.textContent.includes('🔄');
                }});
                updateSummary();
            }}
            
            function getSelectedItems() {{
                const selected = [];
                document.querySelectorAll('.item-row').forEach(row => {{
                    const checkbox = row.querySelector('.item-checkbox');
                    if (checkbox.checked) {{
                        selected.push(row.dataset.itemId);
                    }}
                }});
                return selected;
            }}
            
            function showResult(success, message) {{
                const card = document.getElementById('card');
                card.innerHTML = '<div class="result ' + (success ? 'success' : 'error') + '">' + message + '</div>';
            }}
            
            function allow() {{
                const items = getSelectedItems();
                if (items.length === 0) {{
                    alert('请至少选择一项');
                    return;
                }}
                
                fetch('http://localhost:{port}/bulk/{request.request_id}/confirm', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{approved_item_ids: items}})
                }}).then(r => r.json()).then(data => {{
                    if (data.success) {{
                        const approved = data.status.approved || 0;
                        const total = data.status.total || {summary['total']};
                        showResult(true, '✓ 已批准 ' + approved + '/' + total + ' 项<br><small>您可以关闭此页面</small>');
                    }} else {{
                        showResult(false, '✗ 授权失败: ' + (data.error || '未知错误'));
                    }}
                }}).catch(e => {{
                    console.error('Fetch error:', e);
                    showResult(false, '✗ 请求失败: ' + e.message);
                }});
            }}
            
            function deny() {{
                if (!confirm('确定要拒绝全部请求吗？')) return;
                
                fetch('http://localhost:{port}/bulk/{request.request_id}/deny', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{}})
                }}).then(r => r.json()).then(data => {{
                    if (data.success) {{
                        showResult(false, '✗ 已拒绝全部请求<br><small>您可以关闭此页面</small>');
                    }} else {{
                        showResult(false, '✗ 操作失败: ' + (data.error || '未知错误'));
                    }}
                }}).catch(e => {{
                    console.error('Fetch error:', e);
                    showResult(false, '✗ 请求失败: ' + e.message);
                }});
            }}
        </script>
    </body>
    </html>
    """
    
    return html
