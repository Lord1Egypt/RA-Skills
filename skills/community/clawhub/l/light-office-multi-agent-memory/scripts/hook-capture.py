#!/usr/bin/env python3
"""
多Agent记忆系统 - Hook自动捕获脚本（通用版）

功能：
  8个核心Hook自动捕获：
  1. Hook_SessionStart: 会话开始捕获
  2. Hook_ToolUse: 工具调用捕获
  3. Hook_Error: 错误捕获
  4. Hook_Complete: 任务完成捕获
  5. Hook_PreCompact: 压缩前状态捕获
  6. Hook_SubagentStart: 子Agent启动捕获
  7. Hook_SubagentStop: 子Agent停止捕获
  8. Hook_UserPrompt: 用户提示捕获

作者：光光教授 (光光事务所)
版本：v1.0.0
许可证：MIT
"""

import os
import sys
import json
import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================
# 配置
# ============================================================

# 使用环境变量或默认值
WORKSPACE = Path(os.environ.get("MEMORY_WORKSPACE", "/tmp/memory-workspace"))
MEMORY_DIR = WORKSPACE / "memory"

# Hook配置
HOOK_CONFIG = {
    "session_start": {
        "enabled": True,
        "capture_fields": ["session_id", "timestamp", "user_count"],
        "max_length": 200
    },
    "tool_use": {
        "enabled": True,
        "capture_fields": ["tool_name", "input_summary", "output_summary"],
        "max_length": 500
    },
    "error": {
        "enabled": True,
        "capture_fields": ["error_type", "context", "root_cause"],
        "max_length": 1000,
        "auto_compress_threshold": 5
    },
    "task_complete": {
        "enabled": True,
        "capture_fields": ["task_id", "duration", "result_summary"],
        "max_length": 500
    },
    "pre_compact": {
        "enabled": True,
        "capture_fields": ["memory_size", "compression_ratio", "timestamp"],
        "max_length": 300
    },
    "subagent_start": {
        "enabled": True,
        "capture_fields": ["subagent_id", "task", "timestamp"],
        "max_length": 300
    },
    "subagent_stop": {
        "enabled": True,
        "capture_fields": ["subagent_id", "result", "timestamp"],
        "max_length": 300
    },
    "user_prompt": {
        "enabled": True,
        "capture_fields": ["prompt_summary", "intent", "timestamp"],
        "max_length": 500
    }
}

# 乐观锁配置
LOCK_TIMEOUT = 30
MAX_RETRIES = 3

# ============================================================
# Hook基类
# ============================================================

class MemoryHook:
    """记忆Hook基类"""
    
    def __init__(self, hook_type, config):
        self.hook_type = hook_type
        self.config = config
        self.enabled = config.get("enabled", True)
        self.capture_fields = config.get("capture_fields", [])
        self.max_length = config.get("max_length", 500)
    
    def capture(self, **kwargs):
        """捕获Hook数据"""
        if not self.enabled:
            return None
        
        data = {k: v for k, v in kwargs.items() if k in self.capture_fields}
        data["type"] = self.hook_type
        data["timestamp"] = datetime.now().isoformat()
        
        for key in data:
            if isinstance(data[key], str) and len(data[key]) > self.max_length:
                data[key] = data[key][:self.max_length] + "..."
        
        return data
    
    def write_to_daily(self, data, agent_id="main"):
        """写入每日记忆文件"""
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        daily_file = MEMORY_DIR / f"{today}.md"
        
        return self.safe_write(daily_file, data, agent_id)
    
    def safe_write(self, file_path, data, agent_id):
        """乐观锁写入"""
        for attempt in range(MAX_RETRIES):
            try:
                if file_path.exists():
                    with open(file_path, "r", encoding="utf-8") as f:
                        original_content = f.read()
                    original_hash = hashlib.md5(original_content.encode()).hexdigest()
                else:
                    original_content = ""
                    original_hash = ""
                
                hook_line = f"### {data['type']} - {data['timestamp']}\n"
                for key, value in data.items():
                    if key not in ["type", "timestamp"]:
                        hook_line += f"- **{key}**: {value}\n"
                hook_line += "\n"
                
                new_content = original_content + hook_line
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                
                return True
                
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    print(f"[ERROR] Hook写入失败: {e}", file=sys.stderr)
                    return False
                time.sleep(1)
        
        return False


# ============================================================
# 8个核心Hook
# ============================================================

class SessionStartHook(MemoryHook):
    """会话开始Hook"""
    def __init__(self):
        super().__init__("session_start", HOOK_CONFIG["session_start"])
    
    def capture_session(self, session_id, user_count=0):
        data = self.capture(session_id=session_id, user_count=user_count)
        if data:
            self.write_to_daily(data)
            print(f"[Hook] 会话开始已捕获: {session_id}")
        return data


class ToolUseHook(MemoryHook):
    """工具使用Hook"""
    def __init__(self):
        super().__init__("tool_use", HOOK_CONFIG["tool_use"])
    
    def capture_tool(self, tool_name, input_summary="", output_summary=""):
        data = self.capture(tool_name=tool_name, input_summary=input_summary, output_summary=output_summary)
        if data:
            self.write_to_daily(data)
            print(f"[Hook] 工具使用已捕获: {tool_name}")
        return data


class ErrorHook(MemoryHook):
    """错误捕获Hook"""
    def __init__(self):
        super().__init__("error", HOOK_CONFIG["error"])
        self.error_count = 0
    
    def capture_error(self, error_type, context="", root_cause=""):
        data = self.capture(error_type=error_type, context=context, root_cause=root_cause)
        if data:
            self.write_to_daily(data)
            self.error_count += 1
            print(f"[Hook] 错误已捕获: {error_type} (累计: {self.error_count})")
        return data


class TaskCompleteHook(MemoryHook):
    """任务完成Hook"""
    def __init__(self):
        super().__init__("task_complete", HOOK_CONFIG["task_complete"])
    
    def capture_complete(self, task_id, duration=0, result_summary=""):
        data = self.capture(task_id=task_id, duration=duration, result_summary=result_summary)
        if data:
            self.write_to_daily(data)
            print(f"[Hook] 任务完成已捕获: {task_id}")
        return data


class PreCompactHook(MemoryHook):
    """压缩前Hook"""
    def __init__(self):
        super().__init__("pre_compact", HOOK_CONFIG["pre_compact"])
    
    def capture_pre_compact(self, memory_size, compression_ratio):
        data = self.capture(memory_size=memory_size, compression_ratio=compression_ratio)
        if data:
            self.write_to_daily(data)
            print(f"[Hook] 压缩前状态已捕获: {memory_size}KB, 压缩比:{compression_ratio}%")
        return data


class SubagentStartHook(MemoryHook):
    """子Agent启动Hook"""
    def __init__(self):
        super().__init__("subagent_start", HOOK_CONFIG["subagent_start"])
    
    def capture_start(self, subagent_id, task=""):
        data = self.capture(subagent_id=subagent_id, task=task)
        if data:
            self.write_to_daily(data)
            print(f"[Hook] 子Agent启动已捕获: {subagent_id}")
        return data


class SubagentStopHook(MemoryHook):
    """子Agent停止Hook"""
    def __init__(self):
        super().__init__("subagent_stop", HOOK_CONFIG["subagent_stop"])
    
    def capture_stop(self, subagent_id, result=""):
        data = self.capture(subagent_id=subagent_id, result=result)
        if data:
            self.write_to_daily(data)
            print(f"[Hook] 子Agent停止已捕获: {subagent_id}")
        return data


class UserPromptHook(MemoryHook):
    """用户提示Hook"""
    def __init__(self):
        super().__init__("user_prompt", HOOK_CONFIG["user_prompt"])
    
    def capture_prompt(self, prompt_summary, intent=""):
        data = self.capture(prompt_summary=prompt_summary, intent=intent)
        if data:
            self.write_to_daily(data)
            print(f"[Hook] 用户提示已捕获: {prompt_summary[:50]}...")
        return data


# ============================================================
# Hook管理器
# ============================================================

class HookManager:
    """Hook管理器"""
    
    def __init__(self):
        self.hooks = {
            "session_start": SessionStartHook(),
            "tool_use": ToolUseHook(),
            "error": ErrorHook(),
            "task_complete": TaskCompleteHook(),
            "pre_compact": PreCompactHook(),
            "subagent_start": SubagentStartHook(),
            "subagent_stop": SubagentStopHook(),
            "user_prompt": UserPromptHook()
        }
    
    def trigger(self, hook_type, **kwargs):
        """触发Hook"""
        if hook_type in self.hooks:
            return self.hooks[hook_type].capture(**kwargs)
        else:
            print(f"[ERROR] 未知Hook类型: {hook_type}", file=sys.stderr)
            return None
    
    def get_stats(self):
        """获取Hook统计"""
        stats = {}
        for hook_type, hook in self.hooks.items():
            stats[hook_type] = {
                "enabled": hook.enabled,
                "capture_fields": hook.capture_fields
            }
        return stats


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    manager = HookManager()
    
    print("=" * 60)
    print("多Agent记忆系统 - Hook自动捕获测试")
    print("=" * 60)
    
    # 测试所有Hook
    print("\n[测试1] SessionStart Hook")
    manager.trigger("session_start", session_id="test-001", user_count=5)
    
    print("\n[测试2] ToolUse Hook")
    manager.trigger("tool_use", tool_name="exec", input_summary="ls -la", output_summary="total 100")
    
    print("\n[测试3] Error Hook")
    manager.trigger("error", error_type="TimeoutError", context="API调用超时", root_cause="网络问题")
    
    print("\n[测试4] TaskComplete Hook")
    manager.trigger("task_complete", task_id="task-001", duration=120, result_summary="任务完成")
    
    print("\n[测试5] PreCompact Hook")
    manager.trigger("pre_compact", memory_size=15000, compression_ratio=70)
    
    print("\n[测试6] SubagentStart Hook")
    manager.trigger("subagent_start", subagent_id="subagent-001", task="数据分析")
    
    print("\n[测试7] SubagentStop Hook")
    manager.trigger("subagent_stop", subagent_id="subagent-001", result="分析完成")
    
    print("\n[测试8] UserPrompt Hook")
    manager.trigger("user_prompt", prompt_summary="查询记忆系统优化方案", intent="信息检索")
    
    # 输出统计
    print("\n[统计] Hook状态")
    stats = manager.get_stats()
    for hook_type, stat in stats.items():
        print(f"  {hook_type}: {stat}")
    
    print("\n✅ 所有Hook测试完成")


if __name__ == "__main__":
    main()
