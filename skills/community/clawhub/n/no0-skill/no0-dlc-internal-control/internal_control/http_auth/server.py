"""
HTTP 授权服务 - HTTP API

使用 Python 内置 http.server，无外部依赖
"""

import json
import threading
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict, Any

from .models import (
    PendingAuthRequest, AuthStatus, Decision,
    AuthRequest, AuthResponse
)
from .request_store import RequestStore
from .notifications import NotificationService
from .token_vault import SecureTokenVault


class AuthHandler(BaseHTTPRequestHandler):
    """HTTP 请求处理器"""
    
    def __init__(self, *args, service=None, **kwargs):
        self.service = service
        super().__init__(*args, **kwargs)
    
    def log_message(self, format, *args):
        """简化日志输出"""
        print(f"[HTTP] {self.address_string()} - {format % args}")
    
    def _send_json(self, data: Dict, status: int = 200):
        """发送 JSON 响应"""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())
    
    def _send_html(self, html: str, status: int = 200):
        """发送 HTML 响应"""
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(html.encode())
    
    def _read_json(self) -> Optional[Dict]:
        """读取 JSON 请求体"""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 0:
                body = self.rfile.read(content_length).decode()
                return json.loads(body)
            return {}
        except:
            return None
    
    def do_GET(self):
        """处理 GET 请求"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        # 健康检查
        if path == "/health":
            self._send_json({"status": "ok", "service": "openclaw_auth"})
            return
        
        # 查询授权状态
        if path.startswith("/auth/") and len(path) > 6:
            parts = path.split("/")
            if len(parts) == 3:
                request_id = parts[2]
                self._handle_get_auth_status(request_id)
                return
        
        # Web UI 授权页面
        if path.startswith("/ui/auth/"):
            parts = path.split("/")
            if len(parts) == 4:
                request_id = parts[3]
                self._handle_auth_page(request_id)
                return
        
        self._send_json({"error": "Not found"}, 404)
    
    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def do_POST(self):
        """处理 POST 请求"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        # 创建授权请求
        if path == "/auth/request":
            self._handle_create_auth_request()
            return
        
        # 确认授权
        if path.startswith("/auth/") and path.endswith("/confirm"):
            parts = path.split("/")
            if len(parts) == 4:
                request_id = parts[2]
                self._handle_confirm(request_id)
                return
        
        # 拒绝授权
        if path.startswith("/auth/") and path.endswith("/deny"):
            parts = path.split("/")
            if len(parts) == 4:
                request_id = parts[2]
                self._handle_deny(request_id)
                return
        
        self._send_json({"error": "Not found"}, 404)
    
    def _handle_create_auth_request(self):
        """创建授权请求"""
        data = self._read_json()
        if not data:
            self._send_json({"error": "Invalid JSON"}, 400)
            return
        
        try:
            request_id = self.service.create_auth_request(
                agent_id=data.get("agent_id", "unknown"),
                resource_path=data.get("resource_path", ""),
                operation=data.get("operation", "READ"),
                data_level=data.get("data_level", "L3"),
                context=data.get("context", {}),
                timeout_seconds=data.get("timeout_seconds", 120)
            )
            
            request = self.service.request_store.get(request_id)
            
            self._send_json({
                "request_id": request_id,
                "status": request.status.value,
                "confirmation_url": f"http://localhost:{self.service.port}/ui/auth/{request_id}",
                "expires_at": request.expires_at.isoformat()
            })
        except Exception as e:
            self._send_json({"error": str(e)}, 500)
    
    def _handle_get_auth_status(self, request_id: str):
        """查询授权状态"""
        request = self.service.request_store.get(request_id)
        
        if not request:
            self._send_json({"error": "Request not found"}, 404)
            return
        
        self._send_json({
            "request_id": request_id,
            "status": request.status.value,
            "created_at": request.created_at.isoformat(),
            "expires_at": request.expires_at.isoformat(),
            "confirmed_at": request.confirmed_at.isoformat() if request.confirmed_at else None,
            "decision": request.decision.value if request.decision else None
        })
    
    def _handle_confirm(self, request_id: str):
        """用户确认授权"""
        data = self._read_json() or {}
        
        success = self.service.confirm_auth(
            request_id=request_id,
            user_identifier=data.get("user_identifier")
        )
        
        if success:
            self._send_json({"success": True, "message": "Authorization granted"})
        else:
            self._send_json({"success": False, "message": "Failed to confirm"}, 400)
    
    def _handle_deny(self, request_id: str):
        """用户拒绝授权"""
        data = self._read_json() or {}
        
        success = self.service.deny_auth(
            request_id=request_id,
            user_identifier=data.get("user_identifier")
        )
        
        if success:
            self._send_json({"success": True, "message": "Authorization denied"})
        else:
            self._send_json({"success": False, "message": "Failed to deny"}, 400)
    
    def _handle_auth_page(self, request_id: str):
        """渲染授权页面 HTML"""
        request = self.service.request_store.get(request_id)
        
        if not request:
            self._send_html("<h1>Request not found</h1>", 404)
            return
        
        if request.status != AuthStatus.PENDING:
            status_msg = {
                AuthStatus.CONFIRMED: "已授权",
                AuthStatus.DENIED: "已拒绝",
                AuthStatus.EXPIRED: "已过期"
            }.get(request.status, request.status.value)
            self._send_html(f"<h1>请求{status_msg}</h1>")
            return
        
        # 操作类型中文映射
        op_labels = {
            "READ": "读取",
            "WRITE": "写入",
            "DELETE": "删除",
            "EXECUTE": "执行"
        }
        
        # 级别颜色
        level_colors = {
            "L1-PUBLIC": "#27ae60",
            "L2-INTERNAL": "#3498db",
            "L3-RESTRICTED": "#f39c12",
            "L4-CONFIDENTIAL": "#e67e22",
            "L5-SECRET": "#e74c3c",
            "L6-CRITICAL": "#c0392b"
        }
        
        color = level_colors.get(request.data_level, "#3498db")
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>OpenClaw 授权请求</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    max-width: 600px;
                    margin: 50px auto;
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
                }}
                .icon {{
                    width: 48px;
                    height: 48px;
                    background: {color};
                    border-radius: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 24px;
                    margin-right: 16px;
                }}
                h1 {{ margin: 0; font-size: 20px; color: #333; }}
                .subtitle {{ color: #666; font-size: 14px; margin-top: 4px; }}
                .info-row {{
                    display: flex;
                    padding: 12px 0;
                    border-bottom: 1px solid #eee;
                }}
                .info-label {{ width: 100px; color: #666; font-size: 14px; }}
                .info-value {{ flex: 1; color: #333; font-size: 14px; font-family: monospace; }}
                .level-badge {{
                    display: inline-block;
                    padding: 4px 12px;
                    border-radius: 4px;
                    background: {color}20;
                    color: {color};
                    font-size: 12px;
                    font-weight: 600;
                }}
                .actions {{
                    display: flex;
                    gap: 12px;
                    margin-top: 30px;
                }}
                button {{
                    flex: 1;
                    padding: 14px 24px;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: opacity 0.2s;
                }}
                button:hover {{ opacity: 0.9; }}
                .btn-allow {{ background: #27ae60; color: white; }}
                .btn-deny {{ background: #e74c3c; color: white; }}
                .result {{
                    text-align: center;
                    padding: 40px;
                    font-size: 18px;
                }}
                .result.success {{ color: #27ae60; }}
                .result.error {{ color: #e74c3c; }}
            </style>
        </head>
        <body>
            <div class="card" id="card">
                <div class="header">
                    <div class="icon">🔐</div>
                    <div>
                        <h1>授权请求</h1>
                        <div class="subtitle">OpenClaw Agent 请求访问您的文件</div>
                    </div>
                </div>
                
                <div class="info-row">
                    <div class="info-label">请求资源</div>
                    <div class="info-value">{request.resource_path}</div>
                </div>
                
                <div class="info-row">
                    <div class="info-label">操作类型</div>
                    <div class="info-value">{op_labels.get(request.operation, request.operation)}</div>
                </div>
                
                <div class="info-row">
                    <div class="info-label">数据级别</div>
                    <div class="info-value">
                        <span class="level-badge">{request.data_level}</span>
                    </div>
                </div>
                
                <div class="actions">
                    <button class="btn-deny" onclick="deny()">拒绝</button>
                    <button class="btn-allow" onclick="allow()">允许</button>
                </div>
            </div>
            
            <script>
                function showResult(success, message) {{
                    const card = document.getElementById('card');
                    card.innerHTML = '<div class="result ' + (success ? 'success' : 'error') + '">' + message + '</div>';
                }}
                
                function allow() {{
                    fetch('http://localhost:{self.service.port}/auth/{request_id}/confirm', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{}})
                    }}).then(r => r.json()).then(data => {{
                        if (data.success) {{
                            showResult(true, '✓ 已授权<br><small>您可以关闭此页面</small>');
                        }} else {{
                            showResult(false, '✗ 授权失败: ' + data.message);
                        }}
                    }}).catch(e => {{
                        console.error('Fetch error:', e);
                        showResult(false, '✗ 请求失败: ' + e.message);
                    }});
                }}
                
                function deny() {{
                    fetch('http://localhost:{self.service.port}/auth/{request_id}/deny', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{}})
                    }}).then(r => r.json()).then(data => {{
                        if (data.success) {{
                            showResult(false, '✗ 已拒绝<br><small>您可以关闭此页面</small>');
                        }} else {{
                            showResult(false, '✗ 操作失败: ' + data.message);
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
        
        self._send_html(html)


class HTTPAuthService:
    """HTTP 授权服务"""
    
    def __init__(self, port: int = 0):
        self.port = port
        self.server: Optional[HTTPServer] = None
        self.request_store = RequestStore()
        self.token_vault = SecureTokenVault()
        self.notification_service: Optional[NotificationService] = None
        self._thread: Optional[threading.Thread] = None
        self._running = False
    
    def start(self) -> int:
        """启动服务，返回实际端口号"""
        # 创建 handler 工厂
        def handler_factory(*args, **kwargs):
            return AuthHandler(*args, service=self, **kwargs)
        
        # 尝试绑定端口
        if self.port == 0:
            # 动态分配
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", 0))
                self.port = s.getsockname()[1]
        
        self.server = HTTPServer(("127.0.0.1", self.port), handler_factory)
        
        # 初始化通知服务
        self.notification_service = NotificationService(self.port)
        
        # 启动服务线程
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._running = True
        self._thread.start()
        
        # 保存端口到文件
        self._save_port_file(self.port)
        
        print(f"[HTTP Auth Service] 启动于 http://127.0.0.1:{self.port}")
        return self.port
    
    def _serve(self):
        """服务循环"""
        try:
            self.server.serve_forever()
        except Exception as e:
            if self._running:
                print(f"[HTTP Auth Service] 错误: {e}")
    
    def stop(self):
        """停止服务"""
        self._running = False
        if self.server:
            self.server.shutdown()
        if self._thread:
            self._thread.join(timeout=5)
        self._remove_port_file()
        print("[HTTP Auth Service] 已停止")
    
    def create_auth_request(self,
                           agent_id: str,
                           resource_path: str,
                           operation: str,
                           data_level: str,
                           context: Dict[str, Any],
                           timeout_seconds: int = 120) -> str:
        """创建授权请求"""
        import secrets
        
        request_id = secrets.token_hex(4)  # 8字符短ID
        
        request = PendingAuthRequest(
            request_id=request_id,
            agent_id=agent_id,
            resource_path=resource_path,
            operation=operation,
            data_level=data_level,
            context=context,
            status=AuthStatus.PENDING,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(seconds=timeout_seconds)
        )
        
        self.request_store.save(request)
        
        # 发送通知
        if self.notification_service:
            self.notification_service.notify(request)
        
        # 启动超时处理（后台）
        import threading
        timer = threading.Timer(
            timeout_seconds,
            self._handle_timeout,
            args=[request_id]
        )
        timer.daemon = True
        timer.start()
        
        return request_id
    
    def confirm_auth(self, request_id: str, user_identifier: Optional[str] = None) -> bool:
        """确认授权"""
        request = self.request_store.get(request_id)
        
        if not request:
            return False
        
        if request.status != AuthStatus.PENDING:
            return False
        
        # 生成授权令牌
        token = self.token_vault.generate_token(
            request_id=request_id,
            resource_path=request.resource_path,
            operation=request.operation,
            expires_minutes=30
        )
        
        # 更新请求状态
        request.status = AuthStatus.CONFIRMED
        request.decision = Decision.GRANT
        request.confirmed_at = datetime.now()
        request.auth_token_hash = self.token_vault.hash_token(token)
        request.confirmed_by = user_identifier
        
        self.request_store.save(request)
        
        return True
    
    def deny_auth(self, request_id: str, user_identifier: Optional[str] = None) -> bool:
        """拒绝授权"""
        request = self.request_store.get(request_id)
        
        if not request:
            return False
        
        if request.status != AuthStatus.PENDING:
            return False
        
        request.status = AuthStatus.DENIED
        request.decision = Decision.DENY
        request.confirmed_at = datetime.now()
        request.confirmed_by = user_identifier
        
        self.request_store.save(request)
        
        return True
    
    def _handle_timeout(self, request_id: str):
        """处理超时"""
        request = self.request_store.get(request_id)
        if request and request.status == AuthStatus.PENDING:
            request.status = AuthStatus.EXPIRED
            self.request_store.save(request)
    
    def _save_port_file(self, port: int):
        """保存端口到文件"""
        import os
        port_file = os.path.expanduser("~/.openclaw/run/auth_service.port")
        os.makedirs(os.path.dirname(port_file), exist_ok=True)
        with open(port_file, 'w') as f:
            f.write(str(port))
    
    def _remove_port_file(self):
        """删除端口文件"""
        import os
        port_file = os.path.expanduser("~/.openclaw/run/auth_service.port")
        if os.path.exists(port_file):
            os.remove(port_file)
    
    @staticmethod
    def get_service_port() -> Optional[int]:
        """从文件读取服务端口"""
        import os
        port_file = os.path.expanduser("~/.openclaw/run/auth_service.port")
        if os.path.exists(port_file):
            with open(port_file, 'r') as f:
                return int(f.read().strip())
        return None
