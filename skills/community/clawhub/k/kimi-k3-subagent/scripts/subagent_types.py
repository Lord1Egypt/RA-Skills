"""
Subagent 类型定义 - 借鉴 Kimi Code 架构

关键设计:
- 生命周期: spawn -> resume -> retry 三级操作
- 状态机: idle -> running -> completed/failed/aborted
- 结果包含 usage 追踪
- 支持前台/后台模式
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class SubagentStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ABORTED = "aborted"
    SUSPENDED = "suspended"


class SubagentState(Enum):
    STARTED = "started"
    NOT_STARTED = "not_started"


class SubagentEventType(Enum):
    SPAWNED = "subagent.spawned"
    STARTED = "subagent.started"
    COMPLETED = "subagent.completed"
    FAILED = "subagent.failed"
    SUSPENDED = "subagent.suspended"


@dataclass
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read: int = 0
    cache_write: int = 0

    def total(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass
class SubagentHandle:
    agent_id: str
    profile_name: str
    resumed: bool = False
    completion: Any = None


@dataclass
class SubagentResult:
    task: Any
    agent_id: Optional[str] = None
    status: str = "failed"
    state: Optional[str] = None
    result: Optional[str] = None
    usage: Optional[TokenUsage] = None
    error: Optional[str] = None


@dataclass
class QueuedSubagentTask:
    data: Any
    prompt: str
    description: str
    profile_name: str = "coder"
    parent_tool_call_id: str = ""
    swarm_index: Optional[int] = None
    swarm_item: Optional[str] = None
    run_in_background: bool = False
    timeout: Optional[float] = None
    signal: Any = None
    model_choice: Optional[str] = None


@dataclass
class TaskState:
    index: int
    task: QueuedSubagentTask
    agent_id: Optional[str] = None
    retry_agent_id: Optional[str] = None
    retry_count: int = 0
    retry_ready_at: float = 0
    started: bool = False


@dataclass
class SubagentProfile:
    name: str
    description: str = ""
    when_to_use: str = ""
    tools: list = field(default_factory=list)
    disallowed_tools: list = field(default_factory=list)
    model_preference: Optional[str] = None
    system_prompt: Optional[str] = None


@dataclass
class SubagentSuspendedEvent:
    task: QueuedSubagentTask
    agent_id: str
    reason: str


BUILTIN_SUBAGENT_PROFILES = {
    "coder": SubagentProfile(
        name="coder",
        description="\u901a\u7528\u7f16\u7801\u548c\u6267\u884c\u5b50Agent",
        when_to_use="\u9700\u8981\u6267\u884c\u4ee3\u7801\u3001\u641c\u7d22\u6587\u4ef6\u3001\u8fd0\u884c\u547d\u4ee4\u65f6",
        tools=["read", "write", "edit", "bash", "grep", "glob"],
    ),
    "explore": SubagentProfile(
        name="explore",
        description="\u63a2\u7d22\u548c\u8c03\u7814\u5b50Agent",
        when_to_use="\u9700\u8981\u63a2\u7d22\u4ee3\u7801\u5e93\u3001\u67e5\u627e\u4fe1\u606f\u65f6",
        tools=["read", "grep", "glob", "web_search", "web_fetch"],
    ),
    "plan": SubagentProfile(
        name="plan",
        description="\u89c4\u5212\u548c\u8bbe\u8ba1\u5b50Agent",
        when_to_use="\u9700\u8981\u5236\u5b9a\u8ba1\u5212\u3001\u8bbe\u8ba1\u65b9\u6848\u65f6",
        tools=["read", "write", "web_search"],
        model_preference="primary",
    ),
    "btw": SubagentProfile(
        name="btw",
        description="\u4fa7\u901a\u9053\u95ee\u7b54\u5b50Agent, \u65e0\u5de5\u5177\u6743\u9650",
        when_to_use="\u7528\u6237\u987a\u4fbf\u95ee\u95ee\u9898\u65f6",
        tools=[],
        model_preference="secondary",
    ),
}
