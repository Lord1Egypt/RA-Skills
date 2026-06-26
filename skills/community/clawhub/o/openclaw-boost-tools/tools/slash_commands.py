#!/usr/bin/env python3
"""
Slash Commands System
斜杠命令系统

内置命令：
- /help     - 显示帮助
- /cost     - 查看成本统计
- /status   - 查看系统状态
- /memory   - 查看记忆状态
- /tasks    - 查看定时任务
- /logs     - 查看最近日志
- /tools    - 查看可用工具
- /clear    - 清理会话

用法：
python3 slash_commands.py <command>
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Callable, Optional

MEMORY_ROOT = Path.home() / ".openclaw" / "bw-openclaw-boost" / "memory"
TOOLS_DIR = Path.home() / ".openclaw" / "bw-openclaw-boost" / "tools"


class SlashCommands:
    """斜杠命令注册表"""
    
    def __init__(self):
        self.commands: Dict[str, Callable] = {
            "help": self.cmd_help,
            "cost": self.cmd_cost,
            "status": self.cmd_status,
            "memory": self.cmd_memory,
            "tasks": self.cmd_tasks,
            "logs": self.cmd_logs,
            "tools": self.cmd_tools,
            "clear": self.cmd_clear,
            "version": self.cmd_version,
        }
    
    def execute(self, command: str, args: str = "") -> str:
        """执行命令"""
        cmd = command.lstrip("/")
        
        if cmd in self.commands:
            return self.commands[cmd](args)
        else:
            return f"未知命令: /{cmd}\n\n输入 /help 查看可用命令"
    
    def cmd_help(self, args: str) -> str:
        """帮助命令"""
        commands = [
            ("/help", "显示帮助信息"),
            ("/cost", "查看成本统计"),
            ("/status", "查看系统状态"),
            ("/memory", "查看记忆状态"),
            ("/tasks", "查看定时任务"),
            ("/logs", "查看最近日志"),
            ("/tools", "查看可用工具"),
            ("/clear", "清理会话缓存"),
            ("/version", "查看版本信息"),
        ]
        
        lines = [
            "=" * 50,
            "📚 可用命令",
            "=" * 50,
            "",
        ]
        
        for cmd, desc in commands:
            lines.append(f"  {cmd:<15} - {desc}")
        
        lines.append("")
        lines.append("💡 提示：输入 /command 即可执行")
        
        return "\n".join(lines)
    
    def cmd_cost(self, args: str) -> str:
        """成本统计"""
        try:
            result = subprocess.run(
                ["python3", str(TOOLS_DIR / "cost_tracker.py")],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout if result.returncode == 0 else f"获取失败: {result.stderr}"
        except Exception as e:
            return f"获取成本失败: {e}"
    
    def cmd_status(self, args: str) -> str:
        """系统状态"""
        try:
            result = subprocess.run(
                ["openclaw", "status"],
                capture_output=True, text=True, timeout=10
            )
            # 只取关键信息
            output = result.stdout
            
            lines = [
                "=" * 50,
                "🔧 系统状态",
                "=" * 50,
                "",
            ]
            
            # 提取关键行
            for line in output.split('\n'):
                if any(kw in line for kw in ['Sessions', 'Tasks', 'Gateway', 'Dashboard']):
                    lines.append(line.strip())
            
            return "\n".join(lines)
        except Exception as e:
            return f"获取状态失败: {e}"
    
    def cmd_memory(self, args: str) -> str:
        """记忆状态"""
        try:
            result = subprocess.run(
                ["python3", str(TOOLS_DIR / "memory_relevance.py"), "scan"],
                capture_output=True, text=True, timeout=10
            )
            output = result.stdout
            
            lines = [
                "=" * 50,
                "🧠 记忆状态",
                "=" * 50,
                "",
            ]
            
            # 提取统计信息
            if "找到" in output:
                for line in output.split('\n')[:15]:
                    if line.strip():
                        lines.append(line.strip())
            
            return "\n".join(lines)
        except Exception as e:
            return f"获取记忆状态失败: {e}"
    
    def cmd_tasks(self, args: str) -> str:
        """定时任务"""
        try:
            result = subprocess.run(
                ["openclaw", "cron", "list", "--json"],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode != 0:
                return f"获取任务失败: {result.stderr}"
            
            data = json.loads(result.stdout)
            
            lines = [
                "=" * 50,
                "📅 定时任务",
                "=" * 50,
                "",
            ]
            
            for job in data.get("jobs", []):
                name = job.get("name", "未命名")
                schedule = job.get("schedule", {})
                
                if schedule.get("kind") == "cron":
                    expr = schedule.get("expr", "")
                    tz = schedule.get("tz", "")
                    schedule_str = f"cron: {expr} ({tz})"
                elif schedule.get("kind") == "every":
                    ms = schedule.get("everyMs", 0)
                    minutes = ms // 60000
                    schedule_str = f"every {minutes}m"
                else:
                    schedule_str = str(schedule)
                
                lines.append(f"• {name}")
                lines.append(f"  {schedule_str}")
                lines.append("")
            
            return "\n".join(lines)
        except Exception as e:
            return f"获取任务失败: {e}"
    
    def cmd_logs(self, args: str) -> str:
        """最近日志"""
        try:
            logs_dir = MEMORY_ROOT / "logs"
            if not logs_dir.exists():
                return "暂无日志"
            
            # 找最近的日志文件
            log_files = []
            for root, dirs, files in os.walk(logs_dir):
                for f in files:
                    if f.endswith('.md'):
                        path = Path(root) / f
                        mtime = datetime.fromtimestamp(path.stat().st_mtime)
                        log_files.append((mtime, path, f))
            
            log_files.sort(reverse=True)
            
            lines = [
                "=" * 50,
                "📋 最近日志",
                "=" * 50,
                "",
            ]
            
            for mtime, path, fname in log_files[:10]:
                size = path.stat().st_size
                date_str = mtime.strftime("%m-%d %H:%M")
                lines.append(f"• {date_str}  {fname} ({size} bytes)")
            
            return "\n".join(lines)
        except Exception as e:
            return f"获取日志失败: {e}"
    
    def cmd_tools(self, args: str) -> str:
        """可用工具"""
        tools = [
            ("cost_tracker.py", "成本追踪"),
            ("memory_relevance.py", "相关性记忆检索"),
            ("compaction_manager.py", "多层压缩管理"),
            ("tool_tracker.py", "工具执行追踪"),
            ("permission_manager.py", "权限管理"),
            ("stream_exec.py", "流式执行"),
            ("coordinator.py", "多Agent协调"),
            ("dream_consolidation.py", "自动记忆整理"),
        ]
        
        lines = [
            "=" * 50,
            "🔧 可用工具",
            "=" * 50,
            "",
        ]
        
        for tool, desc in tools:
            lines.append(f"  {tool:<30} - {desc}")
        
        lines.append("")
        lines.append("使用方式: python3 tools/<tool>.py [command]")
        
        return "\n".join(lines)
    
    def cmd_clear(self, args: str) -> str:
        """清理缓存"""
        try:
            # 清理 Python 缓存
            cache_dirs = [
                TOOLS_DIR / "__pycache__",
                MEMORY_ROOT / "__pycache__",
            ]
            
            cleared = 0
            for d in cache_dirs:
                if d.exists():
                    import shutil
                    shutil.rmtree(d)
                    cleared += 1
            
            return f"✅ 已清理 {cleared} 个缓存目录"
        except Exception as e:
            return f"清理失败: {e}"
    
    def cmd_version(self, args: str) -> str:
        """版本信息"""
        try:
            result = subprocess.run(
                ["openclaw", "--version"],
                capture_output=True, text=True, timeout=5
            )
            version = result.stdout.strip() if result.returncode == 0 else "未知"
            
            return f"""= Version Info =
OpenClaw: {version}
Python: {sys.version.split()[0]}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        except Exception as e:
            return f"获取版本失败: {e}"


def main():
    if len(sys.argv) < 2:
        print("用法: slash_commands.py <command>")
        print("示例: slash_commands.py help")
        sys.exit(1)
    
    command = sys.argv[1]
    args = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
    
    commander = SlashCommands()
    result = commander.execute(command, args)
    print(result)


if __name__ == "__main__":
    main()
