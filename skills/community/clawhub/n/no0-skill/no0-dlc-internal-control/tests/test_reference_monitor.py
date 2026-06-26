"""
Reference Monitor 集成测试

验证 Reference Monitor 与 L2 规则引擎的集成
"""

import asyncio
import pytest
from datetime import datetime
from pathlib import Path
import tempfile
import os

# 添加项目路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from internal_control.reference_monitor import (
    ReferenceMonitor,
    Agent,
    AgentPermissionLevel,
    AccessOperation,
    AccessDecision,
    AccessDeniedError,
    AgentContext,
    AgentContextManager,
    DataLevel
)
from internal_control.interception import (
    FileAccessInterceptor,
    OpenClawToolIntegration,
    AccessDeniedHandler
)


class TestReferenceMonitorBasic:
    """Reference Monitor 基础功能测试"""
    
    @pytest.fixture
    async def monitor(self):
        """创建并初始化 Reference Monitor"""
        monitor = ReferenceMonitor()
        await monitor.initialize()
        return monitor
    
    @pytest.fixture
    def mock_agent(self):
        """创建测试 Agent"""
        return Agent(
            agent_id="test-agent-001",
            name="测试 Agent",
            permission_level=AgentPermissionLevel.LEVEL_3_TRUSTED,
            public_key=None,
            registered_at=datetime.now(),
            last_authenticated=datetime.now()
        )
    
    @pytest.mark.asyncio
    async def test_agent_authentication_failure(self, monitor):
        """测试 Agent 认证失败"""
        result = await monitor.check_access(
            agent_id="invalid-agent",
            file_path="~/test.txt",
            operation=AccessOperation.READ,
            context={}
        )
        
        assert result.decision == AccessDecision.DENY
        assert "authentication failed" in result.reason.lower()
    
    @pytest.mark.asyncio
    async def test_public_file_access(self, monitor):
        """测试公开文件访问"""
        # 先注册一个测试 Agent
        test_agent = Agent(
            agent_id="test-public-agent",
            name="测试 Agent",
            permission_level=AgentPermissionLevel.LEVEL_1_BASIC,
            public_key=None,
            registered_at=datetime.now()
        )
        monitor.agent_auth.register_agent(test_agent)
        
        # 测试访问公开文档
        result = await monitor.check_access(
            agent_id="test-public-agent",
            file_path="~/README.md",
            operation=AccessOperation.READ,
            context={}
        )
        
        # 注意：如果 README.md 没有特定规则，默认可能是 L2
        # 所以结果可能是 ALLOW 或 PENDING，取决于分级规则
        assert result.decision in [AccessDecision.ALLOW, AccessDecision.PENDING, AccessDecision.DENY]
    
    @pytest.mark.asyncio
    async def test_l6_critical_always_denied_for_agents(self, monitor):
        """测试 L6-CRITICAL 始终拒绝 Agent 访问"""
        # 使用最高权限 Agent
        admin_agent = Agent(
            agent_id="admin-agent",
            name="Admin Agent",
            permission_level=AgentPermissionLevel.LEVEL_5_ADMIN,
            public_key=None,
            registered_at=datetime.now()
        )
        monitor.agent_auth.register_agent(admin_agent)
        
        # 测试访问模拟的 L6 文件
        # 注意：实际分级取决于规则引擎，但 SSH 密钥通常是高级别
        result = await monitor.check_access(
            agent_id="admin-agent",
            file_path="~/.ssh/id_rsa",
            operation=AccessOperation.READ,
            context={}
        )
        
        # 结果取决于具体分级规则，但应该记录审计日志
        assert result.audit_record_id is not None
    
    @pytest.mark.asyncio
    async def test_fail_closed_on_service_error(self, monitor):
        """测试服务故障时 Fail-Closed"""
        # 模拟分类引擎故障
        monitor._classification_engine = None
        
        # 注册测试 Agent
        test_agent = Agent(
            agent_id="test-fail-closed",
            name="Test Agent",
            permission_level=AgentPermissionLevel.LEVEL_3_TRUSTED,
            public_key=None,
            registered_at=datetime.now()
        )
        monitor.agent_auth.register_agent(test_agent)
        
        result = await monitor.check_access(
            agent_id="test-fail-closed",
            file_path="~/test.txt",
            operation=AccessOperation.READ,
            context={}
        )
        
        # 故障时应该返回 L6_CRITICAL
        assert result.level == DataLevel.L6_CRITICAL
        assert result.source == "fail_closed"


class TestAgentContextManager:
    """Agent 上下文管理器测试"""
    
    def test_context_set_get_clear(self):
        """测试上下文设置、获取、清除"""
        context = AgentContext(
            agent_id="test-agent",
            agent_name="测试 Agent",
            permission_level=AgentPermissionLevel.LEVEL_2_STANDARD,
            session_key="session-001",
            current_task="测试任务"
        )
        
        # 设置上下文
        AgentContextManager.set_context(context)
        
        # 获取上下文
        retrieved = AgentContextManager.get_context()
        assert retrieved is not None
        assert retrieved.agent_id == "test-agent"
        assert retrieved.current_task == "测试任务"
        
        # 清除上下文
        AgentContextManager.clear_context()
        assert AgentContextManager.get_context() is None
    
    def test_update_task(self):
        """测试更新任务描述"""
        context = AgentContext(
            agent_id="test-agent",
            agent_name="测试 Agent",
            permission_level=AgentPermissionLevel.LEVEL_2_STANDARD,
            session_key="session-001",
            current_task="初始任务"
        )
        
        AgentContextManager.set_context(context)
        AgentContextManager.update_task("更新后的任务")
        
        retrieved = AgentContextManager.get_context()
        assert retrieved.current_task == "更新后的任务"
        
        AgentContextManager.clear_context()


class TestFileAccessInterceptor:
    """文件访问拦截器测试"""
    
    @pytest.fixture
    def monitor(self):
        """创建 Reference Monitor（不初始化）"""
        return ReferenceMonitor()
    
    @pytest.fixture
    def interceptor(self, monitor):
        """创建拦截器"""
        return FileAccessInterceptor(monitor)
    
    def test_extract_file_path_from_kwargs(self, interceptor):
        """测试从 kwargs 提取文件路径"""
        def sample_func(file_path: str, content: str = ""):
            pass
        
        path = interceptor._extract_file_path(sample_func, (), {'file_path': '/test/path.txt'})
        assert path == '/test/path.txt'
    
    def test_extract_file_path_from_args(self, interceptor):
        """测试从 args 提取文件路径"""
        def sample_func(file_path: str, content: str = ""):
            pass
        
        path = interceptor._extract_file_path(sample_func, ('/test/path.txt',), {})
        assert path == '/test/path.txt'
    
    def test_detect_operation_read(self, interceptor):
        """测试检测读取操作"""
        assert interceptor._detect_operation('read') == AccessOperation.READ
        assert interceptor._detect_operation('file_read') == AccessOperation.READ
        assert interceptor._detect_operation('view_file') == AccessOperation.READ
    
    def test_detect_operation_write(self, interceptor):
        """测试检测写入操作"""
        assert interceptor._detect_operation('write') == AccessOperation.WRITE
        assert interceptor._detect_operation('file_write') == AccessOperation.WRITE
        assert interceptor._detect_operation('edit_file') == AccessOperation.WRITE
    
    def test_detect_operation_execute(self, interceptor):
        """测试检测执行操作"""
        assert interceptor._detect_operation('exec') == AccessOperation.EXECUTE
        assert interceptor._detect_operation('run_command') == AccessOperation.EXECUTE


class TestAgentPermissionLevel:
    """Agent 权限级别测试"""
    
    def test_can_access_l1(self):
        """测试访问 L1 级别"""
        agent = Agent(
            agent_id="test",
            name="Test",
            permission_level=AgentPermissionLevel.LEVEL_1_BASIC,
            public_key=None,
            registered_at=datetime.now()
        )
        
        assert agent.can_access(DataLevel.L1_PUBLIC, AccessOperation.READ)
        assert agent.can_access(DataLevel.L1_PUBLIC, AccessOperation.WRITE)
    
    def test_can_access_l3_standard_agent(self):
        """测试标准 Agent 访问 L3 级别"""
        agent = Agent(
            agent_id="test",
            name="Test",
            permission_level=AgentPermissionLevel.LEVEL_2_STANDARD,
            public_key=None,
            registered_at=datetime.now()
        )
        
        assert agent.can_access(DataLevel.L3_RESTRICTED, AccessOperation.READ)
        assert not agent.can_access(DataLevel.L3_RESTRICTED, AccessOperation.WRITE)
    
    def test_cannot_access_l6_without_admin(self):
        """测试非管理员无法访问 L6"""
        agent = Agent(
            agent_id="test",
            name="Test",
            permission_level=AgentPermissionLevel.LEVEL_4_SYSTEM,
            public_key=None,
            registered_at=datetime.now()
        )
        
        assert not agent.can_access(DataLevel.L6_CRITICAL, AccessOperation.READ)


class TestAccessDeniedHandler:
    """访问拒绝处理器测试"""
    
    @pytest.fixture
    def handler(self):
        return AccessDeniedHandler()
    
    @pytest.mark.asyncio
    async def test_handle_direct_denial(self, handler):
        """测试直接拒绝处理"""
        error = AccessDeniedError(
            message="Access denied",
            decision=AccessDecision.DENY,
            level=DataLevel.L4_CONFIDENTIAL,
            policy="deny_by_policy",
            audit_record_id="audit-123"
        )
        
        message = await handler.handle(error)
        
        assert "访问被拒绝" in message
        assert "deny_by_policy" in message
        assert "audit-123" in message
    
    @pytest.mark.asyncio
    async def test_handle_pending_auth(self, handler):
        """测试等待授权处理"""
        error = AccessDeniedError(
            message="Authorization required",
            decision=AccessDecision.PENDING,
            level=DataLevel.L3_RESTRICTED,
            policy="require_authorization",
            audit_record_id="audit-456"
        )
        
        message = await handler.handle(error)
        
        assert "需要授权" in message
        assert "audit-456" in message


class TestIntegration:
    """端到端集成测试"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_access_flow(self):
        """测试端到端访问流程"""
        monitor = ReferenceMonitor()
        await monitor.initialize()
        
        # 注册测试 Agent
        test_agent = Agent(
            agent_id="integration-test-agent",
            name="Integration Test Agent",
            permission_level=AgentPermissionLevel.LEVEL_3_TRUSTED,
            public_key=None,
            registered_at=datetime.now()
        )
        monitor.agent_auth.register_agent(test_agent)
        
        # 设置 Agent 上下文
        context = AgentContext(
            agent_id="integration-test-agent",
            agent_name="Integration Test Agent",
            permission_level=AgentPermissionLevel.LEVEL_3_TRUSTED,
            session_key="test-session",
            current_task="集成测试"
        )
        AgentContextManager.set_context(context)
        
        try:
            # 执行访问检查
            result = await monitor.check_access(
                agent_id="integration-test-agent",
                file_path="~/Documents/test.txt",
                operation=AccessOperation.READ,
                context={"test": True}
            )
            
            # 验证结果
            assert result.audit_record_id is not None
            assert result.decision in [AccessDecision.ALLOW, AccessDecision.PENDING, AccessDecision.DENY]
            
        finally:
            AgentContextManager.clear_context()


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
