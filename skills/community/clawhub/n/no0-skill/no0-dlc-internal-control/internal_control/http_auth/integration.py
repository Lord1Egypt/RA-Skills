"""
HTTP 授权服务 - 与 Reference Monitor 集成

提供交互式授权策略实现
"""

import asyncio
import time
from datetime import datetime
from typing import Optional
import urllib.request
import urllib.error
import json

from ..reference_monitor import (
    AccessDecision, AccessResult, AccessRequest, AccessOperation,
    DataLevel, PolicyDecision
)
from .models import AuthResponse, Decision
from .server import HTTPAuthService


class HTTPAuthorizationStrategy:
    """
    HTTP 交互式授权策略
    
    通过本地 HTTP 服务向用户请求授权确认
    """
    
    def __init__(self):
        self.service_port = HTTPAuthService.get_service_port()
        self._service: Optional[HTTPAuthService] = None
    
    async def ensure_service_running(self) -> int:
        """确保 HTTP 服务正在运行"""
        if self.service_port is None:
            # 启动服务
            self._service = HTTPAuthService(port=0)
            self.service_port = self._service.start()
        return self.service_port
    
    async def request_authorization(
        self,
        request: AccessRequest,
        level: DataLevel,
        timeout_seconds: int = 120
    ) -> AccessResult:
        """
        请求交互式授权
        
        流程：
        1. 确保 HTTP 服务运行
        2. 向 HTTP 服务发送授权请求
        3. 等待用户响应（轮询）
        4. 返回授权结果
        """
        # 确保服务运行
        port = await self.ensure_service_running()
        
        # 发送授权请求
        request_id = await self._create_auth_request(
            port=port,
            agent_id=request.agent_id,
            resource_path=request.file_path,
            operation=request.operation.value,
            data_level=level.value,
            context=request.context,
            timeout_seconds=timeout_seconds
        )
        
        if not request_id:
            return AccessResult(
                decision=AccessDecision.DENY,
                token=None,
                expires_at=None,
                level=level,
                policy="http_auth_failed",
                reason="Failed to create auth request",
                audit_record_id=""
            )
        
        # 轮询等待用户响应
        result = await self._poll_for_response(
            port=port,
            request_id=request_id,
            timeout_seconds=timeout_seconds
        )
        
        return result
    
    async def _create_auth_request(self, port: int, **kwargs) -> Optional[str]:
        """创建授权请求"""
        try:
            url = f"http://127.0.0.1:{port}/auth/request"
            data = json.dumps(kwargs).encode('utf-8')
            
            req = urllib.request.Request(
                url,
                data=data,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('request_id')
        except Exception as e:
            print(f"[HTTP Auth] 创建请求失败: {e}")
            return None
    
    async def _poll_for_response(
        self,
        port: int,
        request_id: str,
        timeout_seconds: int
    ) -> AccessResult:
        """轮询等待用户响应"""
        start_time = time.time()
        poll_interval = 1  # 每秒轮询一次
        
        while time.time() - start_time < timeout_seconds:
            try:
                url = f"http://127.0.0.1:{port}/auth/{request_id}"
                
                with urllib.request.urlopen(url, timeout=5) as response:
                    status = json.loads(response.read().decode('utf-8'))
                    
                    status_value = status.get('status')
                    
                    if status_value == 'confirmed':
                        # 用户已确认
                        decision = status.get('decision')
                        if decision == 'grant':
                            return AccessResult(
                                decision=AccessDecision.ALLOW,
                                token=None,  # 令牌不离开 HTTP 服务
                                expires_at=datetime.now() + __import__('datetime').timedelta(minutes=30),
                                level=DataLevel[status.get('data_level', 'L3_RESTRICTED').replace('-', '_')],
                                policy="http_interactive_authorized",
                                reason=f"User confirmed authorization (request: {request_id})",
                                audit_record_id=""
                            )
                        else:
                            return AccessResult(
                                decision=AccessDecision.DENY,
                                token=None,
                                expires_at=None,
                                level=DataLevel.L3_RESTRICTED,
                                policy="http_interactive_denied",
                                reason="User denied authorization",
                                audit_record_id=""
                            )
                    
                    elif status_value == 'denied':
                        return AccessResult(
                            decision=AccessDecision.DENY,
                            token=None,
                            expires_at=None,
                            level=DataLevel.L3_RESTRICTED,
                            policy="http_interactive_denied",
                            reason="User denied authorization",
                            audit_record_id=""
                        )
                    
                    elif status_value == 'expired':
                        return AccessResult(
                            decision=AccessDecision.DENY,
                            token=None,
                            expires_at=None,
                            level=DataLevel.L3_RESTRICTED,
                            policy="http_interactive_expired",
                            reason="Authorization request expired",
                            audit_record_id=""
                        )
                
                # 继续等待
                await asyncio.sleep(poll_interval)
                
            except Exception as e:
                print(f"[HTTP Auth] 轮询错误: {e}")
                await asyncio.sleep(poll_interval)
        
        # 超时
        return AccessResult(
            decision=AccessDecision.DENY,
            token=None,
            expires_at=None,
            level=DataLevel.L3_RESTRICTED,
            policy="http_interactive_timeout",
            reason="Authorization request timeout",
            audit_record_id=""
        )
    
    def stop_service(self):
        """停止 HTTP 服务"""
        if self._service:
            self._service.stop()
            self._service = None


class PolicyEngineWithHTTPAuth:
    """
    集成 HTTP 授权的策略引擎
    
    扩展策略引擎，支持 HTTP 交互式授权
    """
    
    def __init__(self):
        self.http_strategy = HTTPAuthorizationStrategy()
    
    async def evaluate(
        self,
        agent,
        classification,
        operation: AccessOperation,
        context: dict
    ) -> PolicyDecision:
        """
        评估访问策略（支持 HTTP 授权）
        """
        from ..reference_monitor import Agent, AgentPermissionLevel
        
        # 获取分级对应的策略
        from ..reference_monitor import PolicyEngine
        base_engine = PolicyEngine()
        base_decision = await base_engine.evaluate(
            agent, classification, operation, context
        )
        
        # 如果需要授权，使用 HTTP 交互式授权
        if base_decision.decision == AccessDecision.PENDING:
            # 检查 Agent 是否有权限发起授权请求
            if not agent.can_access(classification.level, operation):
                return PolicyDecision(
                    decision=AccessDecision.DENY,
                    reason="Agent lacks required permission level"
                )
            
            # 构建 AccessRequest
            request = AccessRequest(
                agent_id=agent.agent_id,
                file_path=classification.path,
                operation=operation,
                context=context,
                timestamp=datetime.now()
            )
            
            # 执行 HTTP 授权流程
            result = await self.http_strategy.request_authorization(
                request=request,
                level=classification.level
            )
            
            if result.decision == AccessDecision.ALLOW:
                return PolicyDecision(
                    decision=AccessDecision.ALLOW,
                    reason="HTTP interactive authorization granted",
                    requires_auth=True,
                    auth_method='http_interactive'
                )
            else:
                return PolicyDecision(
                    decision=AccessDecision.DENY,
                    reason=result.reason
                )
        
        return base_decision
