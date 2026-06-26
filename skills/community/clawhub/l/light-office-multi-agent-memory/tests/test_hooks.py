#!/usr/bin/env python3
"""
多Agent记忆系统 - Hook测试

作者：光光教授 (光光事务所)
版本：v1.0.0
许可证：MIT
"""

import pytest
import sys
from pathlib import Path

# 添加技能脚本到路径
SKILL_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SKILL_DIR))

from hook_capture import HookManager, SessionStartHook, ToolUseHook, ErrorHook


class TestHookCapture:
    """Hook捕获测试"""
    
    def test_session_start_hook(self):
        """测试会话开始Hook"""
        hook = SessionStartHook()
        data = hook.capture_session("test-001", user_count=5)
        
        assert data is not None
        assert data["type"] == "session_start"
        assert data["session_id"] == "test-001"
        assert data["user_count"] == 5
    
    def test_tool_use_hook(self):
        """测试工具使用Hook"""
        hook = ToolUseHook()
        data = hook.capture_tool("exec", input_summary="ls -la", output_summary="total 100")
        
        assert data is not None
        assert data["type"] == "tool_use"
        assert data["tool_name"] == "exec"
    
    def test_error_hook(self):
        """测试错误Hook"""
        hook = ErrorHook()
        data = hook.capture_error("TimeoutError", context="API调用超时", root_cause="网络问题")
        
        assert data is not None
        assert data["type"] == "error"
        assert data["error_type"] == "TimeoutError"
    
    def test_hook_manager(self):
        """测试Hook管理器"""
        manager = HookManager()
        
        # 触发Hook
        result = manager.trigger("session_start", session_id="test-001", user_count=5)
        assert result is not None
        
        # 获取统计
        stats = manager.get_stats()
        assert "session_start" in stats
        assert stats["session_start"]["enabled"] == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
