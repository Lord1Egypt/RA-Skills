#!/usr/bin/env python3
"""
工具执行追踪系统
参考 Claude Code 的 QueryEvent 设计

追踪每个工具的：
- 开始时间、结束时间、耗时
- 成功/失败状态
- 输出大小
- 错误信息（如果有）

数据存储：memory/logs/tool-tracker/
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict, field
from threading import Lock
from collections import defaultdict

MEMORY_ROOT = Path.home() / ".openclaw" / "bw-openclaw-boost" / "memory"
TRACKER_DIR = MEMORY_ROOT / "logs" / "tool-tracker"
TRACKER_FILE = TRACKER_DIR / "tool-tracker.json"


@dataclass
class ToolEvent:
    """工具执行事件"""
    tool_name: str
    tool_id: str
    started_at: str  # ISO format
    ended_at: Optional[str] = None
    duration_ms: int = 0
    success: bool = True
    error: Optional[str] = None
    output_size: int = 0  # bytes
    session_key: str = ""


class ToolTracker:
    """工具执行追踪器"""
    
    _instance: Optional['ToolTracker'] = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._events: Dict[str, ToolEvent] = {}  # tool_id -> event
        self._session_events: List[ToolEvent] = []
        self._session_start = datetime.now()
        self.load()
    
    def load(self):
        """从文件加载今天的记录"""
        if TRACKER_FILE.exists():
            try:
                data = json.loads(TRACKER_FILE.read_text())
                # 过滤掉今天之前的
                today = datetime.now().strftime("%Y-%m-%d")
                events = []
                for e in data.get("events", []):
                    if e.get("started_at", "").startswith(today):
                        events.append(e)
                self._session_events = [ToolEvent(**e) for e in events]
            except Exception as e:
                print(f"Failed to load tool tracker: {e}")
    
    def save(self):
        """保存到文件"""
        TRACKER_DIR.mkdir(parents=True, exist_ok=True)
        data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "events": [asdict(e) for e in self._session_events]
        }
        TRACKER_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    
    def tool_start(self, tool_name: str, tool_id: str, session_key: str = "") -> str:
        """
        记录工具开始执行
        返回 tool_id
        """
        event = ToolEvent(
            tool_name=tool_name,
            tool_id=tool_id,
            started_at=datetime.now().isoformat(),
            session_key=session_key
        )
        self._events[tool_id] = event
        print(f"[ToolTracker] 🔧 {tool_name} started (id={tool_id})", file=__import__('sys').stderr)
        return tool_id
    
    def tool_end(self, tool_id: str, success: bool = True, error: Optional[str] = None, output_size: int = 0):
        """
        记录工具结束执行
        """
        if tool_id not in self._events:
            print(f"[ToolTracker] ⚠️ tool_end called for unknown id: {tool_id}", file=__import__('sys').stderr)
            return
        
        event = self._events.pop(tool_id)
        event.ended_at = datetime.now().isoformat()
        
        # 计算耗时
        start = datetime.fromisoformat(event.started_at)
        end = datetime.fromisoformat(event.ended_at)
        event.duration_ms = int((end - start).total_seconds() * 1000)
        
        event.success = success
        event.error = error
        event.output_size = output_size
        
        self._session_events.append(event)
        self._session_events = self._session_events[-1000:]  # 只保留最近1000条
        self.save()
        
        status = "✅" if success else "❌"
        print(f"[ToolTracker] {status} {event.tool_name} ended in {event.duration_ms}ms", file=__import__('sys').stderr)
    
    def get_session_summary(self) -> str:
        """获取当前会话的追踪摘要"""
        if not self._session_events:
            return "暂无工具执行记录"
        
        # 统计
        total_calls = len(self._session_events)
        successful = sum(1 for e in self._session_events if e.success)
        failed = total_calls - successful
        total_time = sum(e.duration_ms for e in self._session_events)
        avg_time = total_time // total_calls if total_calls else 0
        
        # 按工具分组统计
        by_tool = defaultdict(lambda: {"count": 0, "total_time": 0, "failed": 0})
        for e in self._session_events:
            by_tool[e.tool_name]["count"] += 1
            by_tool[e.tool_name]["total_time"] += e.duration_ms
            if not e.success:
                by_tool[e.tool_name]["failed"] += 1
        
        lines = [
            "=" * 50,
            "🔧 工具执行追踪摘要",
            "=" * 50,
            f"会话开始: {self._session_start.strftime('%H:%M:%S')}",
            f"当前时间: {datetime.now().strftime('%H:%M:%S')}",
            "",
            f"总调用次数: {total_calls}",
            f"成功: {successful} | 失败: {failed}",
            f"总耗时: {total_time/1000:.1f}s | 平均: {avg_time}ms",
            "",
            "📊 按工具统计:",
        ]
        
        for tool_name, stats in sorted(by_tool.items(), key=lambda x: x[1]["total_time"], reverse=True):
            avg = stats["total_time"] // stats["count"]
            failed_info = f" (❌ {stats['failed']})" if stats["failed"] else ""
            lines.append(f"  {tool_name}: {stats['count']}次, 平均{avg}ms{failed_info}")
        
        # 最近5条执行记录
        lines.append("")
        lines.append("📝 最近执行:")
        for e in self._session_events[-5:]:
            status = "✅" if e.success else "❌"
            lines.append(f"  {status} {e.tool_name}: {e.duration_ms}ms")
        
        return "\n".join(lines)
    
    def get_slow_tools(self, threshold_ms: int = 5000) -> List[ToolEvent]:
        """获取慢工具（超过阈值）"""
        return [e for e in self._session_events if e.duration_ms > threshold_ms]
    
    def get_failed_tools(self) -> List[ToolEvent]:
        """获取失败的工具执行"""
        return [e for e in self._session_events if not e.success]
    
    def reset_session(self):
        """重置会话（开始新的一天时）"""
        self._events.clear()
        self._session_events.clear()
        self._session_start = datetime.now()
        self.save()


def get_tracker() -> ToolTracker:
    """获取追踪器单例"""
    return ToolTracker()


if __name__ == "__main__":
    import sys
    
    tracker = get_tracker()
    
    if len(sys.argv) < 2:
        print(tracker.get_session_summary())
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "--start" and len(sys.argv) >= 4:
        # 外部调用：记录开始
        tool_name = sys.argv[2]
        tool_id = sys.argv[3]
        session = sys.argv[4] if len(sys.argv) > 4 else ""
        tracker.tool_start(tool_name, tool_id, session)
    
    elif cmd == "--end" and len(sys.argv) >= 5:
        # 外部调用：记录结束
        tool_id = sys.argv[2]
        success = sys.argv[3] == "1"
        error = sys.argv[4] if sys.argv[4] != "0" else None
        output_size = int(sys.argv[5]) if len(sys.argv) > 5 else 0
        tracker.tool_end(tool_id, success, error, output_size)
    
    elif cmd == "summary":
        print(tracker.get_session_summary())
    
    elif cmd == "slow":
        slow = tracker.get_slow_tools()
        if slow:
            print(f"慢工具 (>5s):")
            for e in slow:
                print(f"  {e.tool_name}: {e.duration_ms}ms")
        else:
            print("没有慢工具")
    
    elif cmd == "failed":
        failed = tracker.get_failed_tools()
        if failed:
            print(f"失败工具 ({len(failed)}):")
            for e in failed:
                print(f"  {e.tool_name}: {e.error}")
        else:
            print("没有失败工具")
    
    elif cmd == "test":
        # 测试追踪
        import uuid
        tid = tracker.tool_start("exec", str(uuid.uuid4()))
        time.sleep(0.5)
        tracker.tool_end(tid, success=True, output_size=1024)
        
        tid = tracker.tool_start("read", str(uuid.uuid4()))
        time.sleep(0.2)
        tracker.tool_end(tid, success=True, output_size=512)
        
        tid = tracker.tool_start("web_search", str(uuid.uuid4()))
        time.sleep(1)
        tracker.tool_end(tid, success=False, error="Network timeout")
        
        print(tracker.get_session_summary())
    
    elif cmd == "reset":
        tracker.reset_session()
        print("已重置")
