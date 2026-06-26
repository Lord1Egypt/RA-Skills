"""
工具层拦截器 - 拦截所有 Agent 文件访问，强制经过 Reference Monitor

L1 层集成：拦截 read/edit/exec 等文件操作工具
"""

import inspect
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union
import logging

from ..reference_monitor import (
    ReferenceMonitor,
    AccessOperation,
    AccessDecision,
    AccessDeniedError,
    AgentContextManager
)

logger = logging.getLogger(__name__)


# ========== 工具拦截器 ==========

class FileAccessInterceptor:
    """
    文件访问拦截器
    
    拦截所有文件操作工具调用，强制经过 Reference Monitor
    """
    
    def __init__(self, monitor: ReferenceMonitor):
        self.monitor = monitor
        self._original_tools: Dict[str, Callable] = {}
    
    def intercept_tool(self, tool_func: Callable) -> Callable:
        """
        包装工具函数，添加访问控制检查
        
        使用示例:
            @interceptor.intercept_tool
            def read(file_path: str) -> str:
                ...
        """
        @wraps(tool_func)
        async def wrapper(*args, **kwargs):
            # 提取文件路径参数
            file_path = self._extract_file_path(tool_func, args, kwargs)
            
            if not file_path:
                # 非文件操作，直接放行
                return await tool_func(*args, **kwargs)
            
            # 确定操作类型
            operation = self._detect_operation(tool_func.__name__)
            
            # 获取当前 Agent 上下文
            agent_context = AgentContextManager.get_context()
            
            if not agent_context:
                # 没有 Agent 上下文，可能是用户直接调用
                # 在这种情况下，允许访问但记录审计日志
                logger.debug(f"No agent context, allowing direct access to {file_path}")
                return await tool_func(*args, **kwargs)
            
            # Reference Monitor 检查
            result = await self.monitor.check_access(
                agent_id=agent_context.agent_id,
                file_path=file_path,
                operation=operation,
                context={
                    "task": agent_context.current_task,
                    "tool": tool_func.__name__,
                    "args": self._sanitize_args(args, kwargs)
                }
            )
            
            if result.decision == AccessDecision.DENY:
                # 访问被拒绝
                raise AccessDeniedError(
                    f"Access denied for {file_path}: {result.reason}",
                    decision=result.decision,
                    level=result.level,
                    policy=result.policy,
                    audit_record_id=result.audit_record_id
                )
            
            elif result.decision == AccessDecision.PENDING:
                # 需要授权 - 这里应该触发授权流程
                # 简化实现：直接抛出异常，实际应该等待用户确认
                raise AccessDeniedError(
                    f"Authorization required for {file_path}: {result.reason}",
                    decision=result.decision,
                    level=result.level,
                    policy=result.policy,
                    audit_record_id=result.audit_record_id
                )
            
            # 访问被允许，执行原始工具
            return await tool_func(*args, **kwargs)
        
        return wrapper
    
    def _extract_file_path(self, func: Callable, args: tuple, kwargs: dict) -> Optional[str]:
        """从函数参数中提取文件路径"""
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        
        # 常见文件路径参数名
        path_params = ['file_path', 'path', 'file', 'filename', 'src', 'dst', 'source', 'target']
        
        # 检查 kwargs
        for param in path_params:
            if param in kwargs:
                return kwargs[param]
        
        # 检查 args 位置参数
        for i, param in enumerate(params):
            if param in path_params and i < len(args):
                value = args[i]
                if isinstance(value, str):
                    return value
        
        # 第一个字符串参数可能是路径
        for arg in args:
            if isinstance(arg, str) and ('/' in arg or '\\' in arg or '.' in arg):
                return arg
        
        return None
    
    def _detect_operation(self, tool_name: str) -> AccessOperation:
        """根据工具名检测操作类型"""
        name_lower = tool_name.lower()
        
        read_ops = ['read', 'cat', 'view', 'load', 'open', 'fetch', 'get']
        write_ops = ['write', 'edit', 'save', 'create', 'append', 'modify', 'update']
        delete_ops = ['delete', 'remove', 'rm', 'trash']
        exec_ops = ['exec', 'run', 'execute', 'spawn', 'shell']
        
        if any(op in name_lower for op in read_ops):
            return AccessOperation.READ
        elif any(op in name_lower for op in write_ops):
            return AccessOperation.WRITE
        elif any(op in name_lower for op in delete_ops):
            return AccessOperation.DELETE
        elif any(op in name_lower for op in exec_ops):
            return AccessOperation.EXECUTE
        
        return AccessOperation.READ  # 默认读取
    
    def _sanitize_args(self, args: tuple, kwargs: dict) -> Dict[str, Any]:
        """清理参数，移除敏感信息"""
        # 简化实现，实际应该更仔细地处理
        return {
            "args_count": len(args),
            "kwargs_keys": list(kwargs.keys())
        }


# ========== OpenClaw 集成 ==========

# 需要拦截的文件访问工具配置
INTERCEPTED_TOOLS = {
    # 文件读取工具
    'read': {
        'operation': AccessOperation.READ,
        'path_params': ['file_path', 'path'],
        'description': '读取文件内容'
    },
    'web_fetch': {
        'operation': AccessOperation.WRITE,  # 会写入缓存
        'path_params': [],
        'description': '获取网页内容（检查缓存写入）'
    },
    
    # 文件写入工具
    'write': {
        'operation': AccessOperation.WRITE,
        'path_params': ['file_path', 'path'],
        'description': '写入文件'
    },
    'edit': {
        'operation': AccessOperation.WRITE,
        'path_params': ['file_path', 'path'],
        'description': '编辑文件'
    },
    
    # 执行工具
    'exec': {
        'operation': AccessOperation.EXECUTE,
        'path_params': ['command'],  # 需要解析命令中的文件路径
        'description': '执行命令'
    },
    'sessions_spawn': {
        'operation': AccessOperation.READ,  # 会读取工作目录
        'path_params': ['cwd'],
        'description': '创建子会话'
    },
}

# 完全放行的工具（不经过 Reference Monitor）
ALLOWLISTED_TOOLS = {
    'web_search',      # 仅网络访问，不操作本地文件
    'memory_search',   # 仅内存搜索
    'memory_get',      # 仅读取内存文件
    'sessions_list',   # 仅查询会话状态
    'session_status',  # 仅查询状态
    'message',         # 消息发送
    'cron',            # 定时任务管理
    'gateway',         # 网关管理
    'nodes',           # 节点管理
    'browser',         # 浏览器操作（需要单独处理）
}


class OpenClawToolIntegration:
    """
    OpenClaw 工具集成
    
    在 OpenClaw 工具注册时自动添加拦截器
    """
    
    def __init__(self, monitor: ReferenceMonitor):
        self.monitor = monitor
        self.interceptor = FileAccessInterceptor(monitor)
        self._patched = False
        self._wrapped_tools: Dict[str, Callable] = {}
    
    def patch_tool_registry(self):
        """
        拦截 OpenClaw 的工具注册机制
        
        在工具注册时自动包装文件访问工具
        """
        if self._patched:
            return
        
        logger.info("Patching OpenClaw tool registry...")
        
        # 尝试多种方式获取 OpenClaw 工具
        tools_patched = 0
        
        # 方式 1: 直接替换内置函数（如果可用）
        try:
            import builtins
            for tool_name in INTERCEPTED_TOOLS.keys():
                if hasattr(builtins, tool_name):
                    original = getattr(builtins, tool_name)
                    wrapped = self.interceptor.intercept_tool(original)
                    setattr(builtins, tool_name, wrapped)
                    self._wrapped_tools[tool_name] = wrapped
                    tools_patched += 1
                    logger.info(f"Patched builtin tool: {tool_name}")
        except Exception as e:
            logger.warning(f"Failed to patch builtins: {e}")
        
        # 方式 2: 尝试从 openclaw 模块获取
        try:
            # 尝试导入 openclaw.tools
            import importlib
            openclaw_module = importlib.import_module('openclaw.tools')
            
            if hasattr(openclaw_module, 'registry'):
                registry = openclaw_module.registry
                for tool_name in INTERCEPTED_TOOLS.keys():
                    if registry.get(tool_name):
                        original = registry.get(tool_name)
                        wrapped = self.interceptor.intercept_tool(original)
                        registry.register(tool_name, wrapped, force=True)
                        self._wrapped_tools[tool_name] = wrapped
                        tools_patched += 1
                        logger.info(f"Patched registry tool: {tool_name}")
        except Exception as e:
            logger.warning(f"Failed to patch openclaw.tools: {e}")
        
        self._patched = True
        logger.info(f"Tool registry patched. {tools_patched} tools wrapped.")
    
    def restore_original_tools(self):
        """恢复原始工具（用于回滚）"""
        # 简化实现，实际应该保存原始引用
        logger.warning("Restore original tools not fully implemented")


# ========== 装饰器模式（替代方案）==========

def with_access_control(monitor: Optional[ReferenceMonitor] = None):
    """
    访问控制装饰器
    
    使用示例:
        monitor = ReferenceMonitor()
        
        @with_access_control(monitor)
        async def my_tool(file_path: str):
            ...
    """
    if monitor is None:
        monitor = ReferenceMonitor()
    
    interceptor = FileAccessInterceptor(monitor)
    
    def decorator(func: Callable) -> Callable:
        return interceptor.intercept_tool(func)
    
    return decorator


# ========== 访问拒绝处理器 ==========

class AccessDeniedHandler:
    """
    访问拒绝处理器
    
    向用户提供清晰、可操作的拒绝信息
    """
    
    async def handle(self, error: AccessDeniedError, context: Dict[str, Any] = None) -> str:
        """处理访问拒绝事件"""
        
        context = context or {}
        
        # 根据决策类型提供不同提示
        handlers = {
            AccessDecision.DENY: self._handle_direct_denial,
            AccessDecision.PENDING: self._handle_pending_auth,
            AccessDecision.ESCALATE: self._handle_escalation,
        }
        
        handler = handlers.get(error.decision, self._handle_generic_denial)
        return await handler(error, context)
    
    async def _handle_direct_denial(self, error: AccessDeniedError, context: Dict[str, Any]) -> str:
        """处理直接拒绝"""
        
        level_emoji = {
            None: "🔒",
        }
        
        emoji = "🔒"
        
        message = f"""
{emoji} **访问被拒绝**

**原因**: {error.reason}
**策略**: {error.policy}
**审计记录**: {error.audit_record_id}

**可能的解决方案**:
1. 确认您确实需要访问此文件
2. 如需访问，请联系管理员提升 Agent 权限
3. 如果是误报，请检查文件分级配置
"""
        return message.strip()
    
    async def _handle_pending_auth(self, error: AccessDeniedError, context: Dict[str, Any]) -> str:
        """处理等待授权"""
        
        message = f"""
⏳ **需要授权**

**原因**: {error.reason}
**审计记录**: {error.audit_record_id}

请通过以下方式确认:
1. 查看系统通知
2. 访问授权页面确认
"""
        return message.strip()
    
    async def _handle_escalation(self, error: AccessDeniedError, context: Dict[str, Any]) -> str:
        """处理上报"""
        
        message = f"""
📤 **需要上报审批**

**原因**: {error.reason}
**审计记录**: {error.audit_record_id}

此访问请求已上报给管理员审批。
"""
        return message.strip()
    
    async def _handle_generic_denial(self, error: AccessDeniedError, context: Dict[str, Any]) -> str:
        """处理通用拒绝"""
        return f"访问被拒绝: {error.reason}"
