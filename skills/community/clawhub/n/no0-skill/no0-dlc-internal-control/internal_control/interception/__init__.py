"""
拦截模块 - 工具层拦截与 OpenClaw 集成

L1 层集成：拦截所有文件访问工具，强制经过 Reference Monitor
"""

from .tool_interceptor import (
    FileAccessInterceptor,
    OpenClawToolIntegration,
    with_access_control,
    AccessDeniedHandler,
    INTERCEPTED_TOOLS,
    ALLOWLISTED_TOOLS
)

__all__ = [
    'FileAccessInterceptor',
    'OpenClawToolIntegration',
    'with_access_control',
    'AccessDeniedHandler',
    'INTERCEPTED_TOOLS',
    'ALLOWLISTED_TOOLS'
]
