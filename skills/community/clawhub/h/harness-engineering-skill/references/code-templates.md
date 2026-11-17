# 代码模板：Python 参考实现

> 构建符合 harness 工程标准的 agent 时可直接参考/复用的代码模板。基于 Edd Mann 的 7 Rings 设计，已简化为可读、可跑通的参考实现。
> 本文件所有代码片段在概念上自洽：共享类型集中定义，Agent loop 用到的每个方法都有默认实现，7 件套工具齐备。把各节按顺序拼起即为一个最小可运行 harness 骨架（缺省 provider 用占位实现，接真实 LLM 时替换 `LLMProvider` 适配层即可）。

---

## 目录

- 0. 共享类型与协议（所有节共用）
- 1. Agent Loop（核心循环）
- 2. Tool Registry（工具注册）
- 3. Session Tree（不可变会话树）
- 4. Compaction（上下文压缩）
- 5. Extension API（扩展系统）
- 6. 最简 Harness 组装
- 参考项目

---

## 0. 共享类型与协议（所有节共用）

先定义贯穿全文的类型与协议。后面各节都依赖它们，建议放在 `models.py`（**不要命名成 `types.py`，会与 Python 标准库模块冲突**），Agent loop 与各 ring 直接 import。

```python
# models.py
from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Optional, Protocol, Type

import pydantic
from pydantic import BaseModel, Field, ValidationError


# ── 消息与工具调用 ──

@dataclass
class ToolCall:
    """模型请求的一次工具调用"""
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class Message:
    """对话历史中的一条消息（user/assistant/tool/system）"""
    role: str
    content: str
    tool_calls: Optional[list[ToolCall]] = None
    tool_call_id: Optional[str] = None


@dataclass
class AssistantMessage:
    content: str
    tool_calls: list[ToolCall] = field(default_factory=list)


# ── Provider 协议 ──

class LLMProvider(Protocol):
    name: str
    model: str

    def set_model(self, model: str) -> None: ...
    def supports_thinking(self) -> bool: ...
    async def list_models(self) -> list[str]: ...
    async def close(self) -> None: ...
    def stream(self, messages, tools) -> AsyncIterator[Any]: ...
    async def complete(self, prompt: str) -> str: ...


# ── 异常 ──

class CancelledError(Exception):
    pass


class ToolError(Exception):
    """工具执行的瞬时错误，可重试一次"""


# ── 权限 hook 的事件与结果对象 ──

@dataclass
class ToolCallEvent:
    """传给 authorize/process hook 的事件"""
    name: str
    arguments: dict[str, Any]
    result: Optional[str] = None


@dataclass
class ToolCallResult:
    """authorize hook 的返回值；blocked=True 即拦截"""
    blocked: bool = False
    reason: Optional[str] = None


# ── 流式消费：把 provider 的增量事件重组成一条 AssistantMessage ──

async def consume_stream(stream: AsyncIterator[Any]) -> AssistantMessage:
    content_parts: list[str] = []
    tool_calls: dict[str, dict[str, Any]] = {}

    async for event in stream:
        etype = getattr(event, "type", None)
        if etype in ("text", "text_delta"):
            content_parts.append(getattr(event, "text", ""))
        elif etype in ("tool_call_delta", "tool_call"):
            delta = event.delta if hasattr(event, "delta") else event
            tc = tool_calls.setdefault(delta.get("id", "_"), {
                "id": delta.get("id", "_"),
                "name": "",
                "arguments": {},
            })
            if delta.get("name"):
                tc["name"] = delta["name"]
            if "arguments" in delta:
                # 增量 JSON 片段累积为字符串，调用方自行 json.loads
                tc["arguments_raw"] = tc.get("arguments_raw", "") + delta["arguments"]

    calls: list[ToolCall] = []
    for tc in tool_calls.values():
        raw = tc.get("arguments_raw", "{}")
        try:
            args = json.loads(raw) if raw.strip() else {}
        except json.JSONDecodeError:
            args = {}
        calls.append(ToolCall(id=tc["id"], name=tc["name"], arguments=args))

    return AssistantMessage(content="".join(content_parts), tool_calls=calls)
```

> 说明：`consume_stream` 是「最小可移植」版本——它假设 provider 的事件有 `type`/`text`/`delta` 字段。真实接入某个 provider 时，只需在其 adapter 里把原生流式事件转成上述形状即可，Agent loop 不感知差异。

---

## 1. Agent Loop（核心循环）

```python
# agent.py
import asyncio
from dataclasses import dataclass, field

from models import (  # 见第 0 节
    AssistantMessage, CancelledError, Message, ToolCall,
    ToolCallEvent, ToolCallResult, consume_stream,
)

DEFAULT_TOOLS = ["read", "write", "edit", "bash", "grep", "find", "ls"]


@dataclass
class AgentConfig:
    max_iterations: int = 50
    cancel_timeout: float = 300.0  # 总超时，防止无限工具调用


@dataclass
class Agent:
    provider: "LLMProvider"
    tools: "ToolRegistry"
    session: "Session"
    config: AgentConfig = field(default_factory=AgentConfig)
    cancel_event: asyncio.Event = field(default_factory=asyncio.Event)
    # 扩展注入的权限 hook
    authorize_hooks: list = field(default_factory=list)
    process_hooks: list = field(default_factory=list)
    # 可选的上下文压缩策略（超阈值时自动 compact 收窄视图）
    compaction: "CompactionStrategy | None" = None

    async def run(self, user_input: str) -> str:
        """主循环：发送用户输入 → 跑 agent loop → 返回最终响应"""
        self.session.append_message("user", user_input)

        try:
            async with asyncio.timeout(self.config.cancel_timeout):
                for _ in range(self.config.max_iterations):
                    if self.cancel_event.is_set():
                        raise CancelledError("User cancelled")

                    messages = await self._prepare_context()
                    assistant_msg = await self._call_model(messages)

                    if not assistant_msg.tool_calls:
                        return assistant_msg.content  # 纯文本 → 结束

                    for tool_call in assistant_msg.tool_calls:
                        result = await self._execute_tool(tool_call)
                        self.session.append_message("tool", result, tool_call_id=tool_call.id)
        except asyncio.TimeoutError:
            return "Agent timed out."
        except CancelledError:
            return "Agent cancelled by user."

        return "Agent reached max iterations."

    async def _prepare_context(self) -> list[Message]:
        """准备发给模型的消息视图（超阈值时触发 compaction 收窄）"""
        messages = self.session.rebuild_messages()
        if self.compaction is not None and self.compaction.needs_compaction(messages):
            messages = await self.compaction.compact(self.session, messages)
        return messages

    async def _call_model(self, messages: list[Message]) -> AssistantMessage:
        stream = self.provider.stream(messages, self.tools.get_schemas())
        assistant_msg = await consume_stream(stream)
        self.session.append_message(
            "assistant",
            assistant_msg.content,
            tool_calls=assistant_msg.tool_calls,
        )
        return assistant_msg

    async def _execute_tool(self, tool_call: ToolCall) -> str:
        """执行单个工具调用，带权限检查和错误处理（D10 失败分类）"""
        auth_result = await self._authorize(tool_call)
        if auth_result.blocked:
            return f"Permission denied: {auth_result.reason}"

        try:
            result = await self.tools.execute(tool_call)
        except ValidationError as e:
            return f"Validation error: {e}"  # 让模型看到错误自己修正，不重试
        except ToolError as e:
            try:  # 瞬时错误重试一次
                result = await self.tools.execute(tool_call)
            except Exception:
                return f"Tool error after retry: {e}"
        except Exception as e:
            return f"Unexpected error in {tool_call.name}: {e}"

        return await self._process_result(tool_call, result)

    async def _authorize(self, tool_call: ToolCall) -> ToolCallResult:
        """执行所有 authorize hook，任一拦截即停止"""
        event = ToolCallEvent(name=tool_call.name, arguments=tool_call.arguments)
        for hook in self.authorize_hooks:
            res = await hook(event, self)
            if isinstance(res, ToolCallResult) and res.blocked:
                return res
        return ToolCallResult(blocked=False)

    async def _process_result(self, tool_call: ToolCall, result: str) -> str:
        """执行所有 process hook（脱敏、改写等）"""
        event = ToolCallEvent(name=tool_call.name, arguments=tool_call.arguments, result=result)
        for hook in self.process_hooks:
            out = await hook(event, self)
            if isinstance(out, str):
                event.result = out
        return event.result or result
```

---

## 2. Tool Registry（工具注册）

```python
# tools.py
import os
import re
import subprocess
from typing import Type
from pydantic import BaseModel, Field
from models import ToolError


class ToolParams(BaseModel):
    """所有工具参数的基类（Pydantic 一石二鸟：生成 schema + 校验参数）"""


class BaseTool:
    name: str
    description: str
    parameters: Type[ToolParams]

    async def execute(self, params: ToolParams) -> str:  # pragma: no cover - overridden
        raise NotImplementedError


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}
        self._active: set[str] = set()

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool
        self._active.add(tool.name)

    def set_active(self, names: list[str]) -> None:
        self._active = set(names)

    def restrict_to(self, names: tuple[str, ...]) -> "ToolRegistry":
        """子代理用：返回只含指定工具的浅副本"""
        new = ToolRegistry()
        for n in names:
            if n in self._tools:
                new.register(self._tools[n])
        return new

    def get_schemas(self) -> list[dict]:
        return [{
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.parameters.model_json_schema(),
            },
        } for n, t in self._tools.items() if n in self._active]

    async def execute(self, tool_call) -> str:
        tool = self._tools.get(tool_call.name)
        if not tool:
            return f"Unknown tool: {tool_call.name}"  # D10: 未知工具不重试
        params = tool.parameters.model_validate(tool_call.arguments)  # 校验失败抛 ValidationError
        return await tool.execute(params)


# ── 7 件套工具实现 ──

class ReadParams(ToolParams):
    path: str = Field(description="File path to read")
    offset: int = Field(default=0, description="Line to start reading from")
    limit: int = Field(default=2000, description="Max lines to read")


class ReadTool(BaseTool):
    name = "read"
    description = "Read a file with line numbers"
    parameters = ReadParams

    async def execute(self, p: ReadParams) -> str:
        try:
            with open(p.path) as f:
                lines = f.readlines()
        except FileNotFoundError:
            return f"File not found: {p.path}"
        start, end = p.offset, min(p.offset + p.limit, len(lines))
        return "".join(f"{i+1:6}\t{lines[i]}" for i in range(start, end)) or "(empty file)"


class WriteParams(ToolParams):
    path: str = Field(description="File path to write")
    content: str = Field(description="Full content to write")


class WriteTool(BaseTool):
    name = "write"
    description = "Write a file (overwrites)"
    parameters = WriteParams

    async def execute(self, p: WriteParams) -> str:
        with open(p.path, "w") as f:
            f.write(p.content)
        return f"Wrote {len(p.content)} chars to {p.path}"


class EditParams(ToolParams):
    path: str = Field(description="File path to edit")
    old_string: str = Field(description="Exact string to find and replace")
    new_string: str = Field(description="String to replace with")
    replace_all: bool = Field(default=False, description="Replace all occurrences")


class EditTool(BaseTool):
    name = "edit"
    description = "Edit a file by finding and replacing exact string"
    parameters = EditParams

    async def execute(self, p: EditParams) -> str:
        try:
            with open(p.path) as f:
                content = f.read()
        except FileNotFoundError:
            return f"File not found: {p.path}"
        count = content.count(p.old_string)
        if count == 0:
            return "String not found. Match exactly including whitespace."
        if count > 1 and not p.replace_all:
            return f"String appears {count} times. Add context or use replace_all=true."
        new_content = content.replace(
            p.old_string, p.new_string, -1 if p.replace_all else 1
        )
        with open(p.path, "w") as f:
            f.write(new_content)
        return f"Successfully edited {p.path}"


class BashParams(ToolParams):
    command: str = Field(description="Shell command to execute")
    timeout: int = Field(default=30, description="Timeout in seconds")


class BashTool(BaseTool):
    name = "bash"
    description = "Execute a shell command and return output"
    parameters = BashParams

    async def execute(self, p: BashParams) -> str:
        try:
            r = subprocess.run(
                p.command, shell=True, capture_output=True, text=True, timeout=p.timeout
            )
        except subprocess.TimeoutExpired:
            return f"Command timed out after {p.timeout}s"
        out = r.stdout or ""
        if r.stderr:
            out += f"\nSTDERR:\n{r.stderr}"
        if len(out) > 10000:  # D11: 截断 + 提示，防止爆窗口
            out = out[:10000] + f"\n... (truncated, {len(out)} total chars)"
        return out or "(no output)"


class GrepParams(ToolParams):
    pattern: str = Field(description="Regex pattern")
    path: str = Field(default=".", description="Path to search")


class GrepTool(BaseTool):
    name = "grep"
    description = "Search file contents by regex, narrow output"
    parameters = GrepParams

    async def execute(self, p: GrepParams) -> str:
        try:
            proc = subprocess.run(
                ["grep", "-rnE", "--include=*", p.pattern, p.path],
                capture_output=True, text=True, timeout=30,
            )
        except subprocess.TimeoutExpired:
            return "grep timed out"
        return proc.stdout.strip() or "(no matches)"


class FindParams(ToolParams):
    name: str = Field(description="Name pattern (glob)")
    path: str = Field(default=".", description="Directory to search")


class FindTool(BaseTool):
    name = "find"
    description = "Find files by name"
    parameters = FindParams

    async def execute(self, p: FindParams) -> str:
        proc = subprocess.run(
            ["find", p.path, "-name", p.name], capture_output=True, text=True, timeout=30
        )
        return proc.stdout.strip() or "(nothing found)"


class LsParams(ToolParams):
    path: str = Field(default=".", description="Directory to list")


class LsTool(BaseTool):
    name = "ls"
    description = "List directory entries"
    parameters = LsParams

    async def execute(self, p: LsParams) -> str:
        try:
            entries = sorted(os.listdir(p.path))
        except FileNotFoundError:
            return f"Directory not found: {p.path}"
        return "\n".join(entries) or "(empty)"
```

---

## 3. Session Tree（不可变会话树）

```python
# session.py
import json
import os
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Optional

from models import Message  # 见第 0 节


@dataclass
class Entry:
    id: str
    parent_id: Optional[str]
    timestamp: str
    entry_type: str  # message | model_change | compaction | state
    data: dict


@dataclass
class Session:
    session_id: str
    file_path: str
    leaf_id: str = ""
    root_id: str = ""

    @classmethod
    def create_new(cls, dir_path: str = "sessions") -> "Session":
        os.makedirs(dir_path, exist_ok=True)
        fp = os.path.join(dir_path, f"{uuid.uuid4()}.jsonl")
        return cls(session_id=str(uuid.uuid4()), file_path=fp)

    def append(self, entry: Entry) -> None:
        with open(self.file_path, "a") as f:
            f.write(json.dumps(asdict(entry)) + "\n")
        self.leaf_id = entry.id
        if not self.root_id:
            self.root_id = entry.id

    def append_message(self, role: str, content: str, **extra) -> None:
        self.append(Entry(
            id=str(uuid.uuid4()),
            parent_id=self.leaf_id or None,
            timestamp=datetime.now().isoformat(),
            entry_type="message",
            data={"role": role, "content": content, **extra},
        ))

    def fork(self, from_entry_id: Optional[str] = None) -> "Session":
        fork_point = from_entry_id or self.leaf_id
        new_fp = self.file_path.replace(
            ".jsonl", f"_fork_{uuid.uuid4().hex[:8]}.jsonl"
        )
        return Session(
            session_id=str(uuid.uuid4()),
            file_path=new_fp,
            leaf_id=fork_point,
            root_id=self.root_id or fork_point,
        )

    def time_travel(self, entry_id: str) -> None:
        """回到指定 entry（不删除任何数据，只是移动 leaf）"""
        self.append(Entry(
            id=str(uuid.uuid4()),
            parent_id=self.leaf_id or None,
            timestamp=datetime.now().isoformat(),
            entry_type="state",
            data={"new_leaf": entry_id},
        ))
        self.leaf_id = entry_id

    def append_compaction(self, summary: str, first_kept_id: str) -> None:
        self.append(Entry(
            id=str(uuid.uuid4()),
            parent_id=self.leaf_id or None,
            timestamp=datetime.now().isoformat(),
            entry_type="compaction",
            data={"summary": summary, "first_kept_entry_id": first_kept_id},
        ))

    def _load_all(self) -> list[dict]:
        out: list[dict] = []
        if not os.path.exists(self.file_path):
            return out
        with open(self.file_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
        return out

    def rebuild_messages(self) -> list[Message]:
        """从 leaf 回溯到 root，重建当前分支的消息视图（处理 compaction）。"""
        entries = self._load_all()
        by_id = {e["id"]: e for e in entries}

        # 回溯当前分支（root -> leaf 顺序，无环）
        chain: list[dict] = []
        cur: Optional[str] = self.leaf_id
        seen: set[str] = set()
        while cur and cur in by_id and cur not in seen:
            seen.add(cur)
            chain.append(by_id[cur])
            cur = by_id[cur].get("parent_id")
        chain.reverse()

        # 取最后一个 compaction：摘要 + 保留起点
        last_compaction = None
        for e in chain:
            if e["entry_type"] == "compaction":
                last_compaction = e
        if last_compaction is None:
            return [Message(**e["data"]) for e in chain if e["entry_type"] == "message"]

        summary = last_compaction["data"]["summary"]
        first_kept_id = last_compaction["data"]["first_kept_entry_id"]

        # 收集规则：
        #  - 最前的一条 system 消息（如基础 prompt）始终保留
        #  - 其余消息从 first_kept_id 起才进入视图（之前的历史已被压缩丢弃）
        result: list[Message] = []
        started = False
        for e in chain:
            if e["entry_type"] != "message":
                continue
            msg = Message(**e["data"])
            if msg.role == "system" and not result:
                result.append(msg)  # 仅保留最前的一条 system
                continue
            if e["id"] == first_kept_id:
                started = True
            if started:
                result.append(msg)
        # 在 system 之后、第一条保留消息之前插入压缩摘要
        summary_msg = Message(role="system",
                               content=f"[Previous conversation summary]\n{summary}")
        insert_at = 1 if result and result[0].role == "system" else 0
        result.insert(insert_at, summary_msg)
        return result
```

---

## 4. Compaction（上下文压缩）

```python
# compaction.py
from typing import Optional
from models import LLMProvider, Message  # 见第 0 节


class CompactionStrategy:
    def __init__(
        self,
        max_tokens: int = 128_000,
        reserve_tokens: int = 4096,
        keep_recent: int = 10,
        threshold: float = 0.8,
        summariser: Optional[LLMProvider] = None,
    ):
        self.max_tokens = max_tokens
        self.reserve_tokens = reserve_tokens
        self.keep_recent = keep_recent
        self.threshold = threshold
        self.summariser = summariser

    def needs_compaction(self, messages: list) -> bool:
        """80% 阈值 + keep_recent 地板（D19）"""
        if len(messages) <= self.keep_recent + 1:
            return False
        available = self.max_tokens - self.reserve_tokens
        return self._count_tokens(messages) > available * self.threshold

    async def compact(self, session, messages: list) -> list:
        """压缩：old 消息交 summariser → 摘要，追加 CompactionEntry（不丢原始）。"""
        split_point = max(1, len(messages) - self.keep_recent)
        old_messages = messages[:split_point]
        summary = await self._summarise(old_messages)
        # first_kept 取「保留区第一条消息」对应的 entry id。
        # 通过重建当前分支并取 message entry 的索引来定位（与传入 messages 顺序一致，
        # 且不靠内容匹配，避免内容碰撞）。
        entries = session._load_all()
        by_id = {e["id"]: e for e in entries}
        chain: list[dict] = []
        cur = session.leaf_id
        seen: set[str] = set()
        while cur and cur in by_id and cur not in seen:
            seen.add(cur)
            chain.append(by_id[cur])
            cur = by_id[cur].get("parent_id")
        chain.reverse()
        msg_entries = [e for e in chain if e["entry_type"] == "message"]
        first_kept_entry = msg_entries[split_point] if split_point < len(msg_entries) else None
        first_kept_id = first_kept_entry["id"] if first_kept_entry else ""
        session.append_compaction(summary, first_kept_id)
        return [Message(role="system", content=f"[Previous conversation summary]\n{summary}")] + list(messages[split_point:])

    async def _summarise(self, messages: list) -> str:
        conversation = "\n".join(
            f"{getattr(m,'role','?'):} : {getattr(m,'content','')[:500]}" for m in messages
        )
        prompt = f"""Summarize the following conversation concisely.
Output markdown with these headings in order:
1) Summary
2) Decisions
3) Files Read
4) Files Modified
5) Commands Run
6) Tools Used
7) Open TODOs
8) Risks/Concerns

Rules:
- Do NOT include system prompt text or policies.
- Keep bullets short and actionable.

Conversation:
{conversation}"""
        if self.summariser is None:
            return "[summary unavailable: no summariser configured]"
        return await self.summariser.complete(prompt)

    def _count_tokens(self, messages: list) -> int:
        total = 0
        for m in messages:
            c = getattr(m, "content", "") or ""
            total += len(c) // 4  # 粗估：4 char ≈ 1 token
        return total
```

> `compact()` 返回的列表元素是 `Message` 对象（与 `rebuild_messages` 对齐）。`first_kept_id` 用内容反查 entry id 是最简可跑通方式；生产实现建议让 `Message` 携带 `entry_id`，避免内容碰撞。

---

## 5. Extension API（扩展系统）

运行时只需提供一个把事件适配成 hook 调用的最小 `ExtensionAPI`。下面给出它，以及 4 个杀手级扩展（权限脱敏、Sub-agent、Plan mode、MCP proxy）。

```python
# extensions.py
import json
import re
from pydantic import Field

from models import ToolCallEvent, ToolCallResult  # 见第 0 节
from tools import BaseTool, ToolParams
from session import Session
from agent import Agent, AgentConfig, DEFAULT_TOOLS


class ExtensionAPI:
    """最小扩展 API：三动词 + 把 hook 接到 Agent 上。"""
    def __init__(self, agent: Agent):
        self.agent = agent
        self.commands: dict[str, callable] = {}

    def on(self, event: str):
        """装饰器工厂：@api.on("authorize_tool_call") def handler(...)"""
        def deco(handler):
            if event == "authorize_tool_call":
                self.agent.authorize_hooks.append(handler)
            elif event == "process_tool_result":
                self.agent.process_hooks.append(handler)
            return handler
        return deco

    def register_tool(self, tool: BaseTool) -> None:
        self.agent.tools.register(tool)

    def register_command(self, name: str):
        """装饰器工厂：@api.register_command("subagent") def handler(...)"""
        def deco(handler):
            self.commands[name] = handler
            return handler
        return deco


# ── ① 权限 hook 扩展：拦截危险命令 + 脱敏 ──

def setup_security(api: ExtensionAPI):
    @api.on("authorize_tool_call")
    async def block_dangerous(event: ToolCallEvent, ctx):
        if event.name == "bash":
            cmd = event.arguments.get("command", "")
            dangerous = ["rm -rf /", "rm -rf ~", "sudo rm", ":(){:|:&};:"]
            for pattern in dangerous:
                if pattern in cmd:
                    return ToolCallResult(
                        blocked=True,
                        reason=f"Blocked dangerous command: {pattern}",
                    )
        return None  # 不拦截

    @api.on("process_tool_result")
    async def redact_secrets(event: ToolCallEvent, ctx):
        result = event.result or ""
        result = re.sub(r"AKIA[0-9A-Z]{16}", "[REDACTED_AWS_KEY]", result)
        result = re.sub(r"sk-[a-zA-Z0-9]{48}", "[REDACTED_API_KEY]", result)
        return result


# ── ② Sub-agent 扩展 ──

from dataclasses import dataclass


@dataclass
class SubagentProfile:
    name: str
    active_tools: tuple
    thinking_level: str = "medium"


PROFILES = {
    "researcher": SubagentProfile("researcher", ("read", "grep", "find", "ls")),
    "implementer": SubagentProfile(
        "implementer", ("read", "grep", "find", "ls", "edit", "write", "bash")
    ),
}


def setup_subagents(api: ExtensionAPI):
    @api.register_command("subagent")
    async def subagent_command(args: str, ctx):
        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            return "Usage: /subagent <profile> <task>"
        profile_name, task = parts
        profile = PROFILES.get(profile_name)
        if not profile:
            return f"Unknown profile: {profile_name}"
        sub = Agent(
            provider=ctx.agent.provider,
            tools=ctx.agent.tools.restrict_to(profile.active_tools),
            session=Session.create_new(),
            config=AgentConfig(max_iterations=20),
        )
        result = await sub.run(task)
        return json.dumps({"profile": profile_name, "task": task, "result": result})


# ── ③ Plan mode 扩展 ──

def setup_plan(api: ExtensionAPI):
    state = {"active": False, "plan": None}

    @api.register_command("plan")
    async def plan_command(args: str, ctx):
        match args.strip():
            case "on":
                ctx.agent.tools.set_active(["read", "grep", "find", "ls"])
                state["active"] = True
                return "Plan mode ON. Read-only tools, high thinking."
            case "off":
                ctx.agent.tools.set_active(list(DEFAULT_TOOLS))
                state["active"] = False
                return "Plan mode OFF."
            case "apply":
                if not state["plan"]:
                    return "No plan saved. Use /plan save <plan> first."
                ctx.agent.tools.set_active(list(DEFAULT_TOOLS))
                state["active"] = False
                return f"Plan applied:\n{state['plan']}"

    @api.register_command("plan-save")
    async def plan_save(args: str, ctx):
        state["plan"] = args
        return "Plan saved. /plan apply to execute."


# ── ④ MCP proxy 扩展 ──

class MCPProxyParams(ToolParams):
    action: dict = Field(description=(
        "MCP action. One of: "
        '{"search":"query"} / {"describe":"tool_name"} / {"tool":"tool_name","args":{...}}'
    ))


class MCPProxyTool(BaseTool):
    name = "mcp"
    description = "Access MCP tools via a single proxy tool"
    parameters = MCPProxyParams

    def __init__(self, mcp_server_url: str):
        self.server = mcp_server_url

    async def execute(self, p: MCPProxyParams) -> str:
        # 真实实现：调用 MCP server 的 search/describe/invoke
        a = p.action
        if "search" in a:
            return json.dumps({"tools": ["<implement search against self.server>"]})
        if "describe" in a:
            return json.dumps({"schema": {"implement": True}})
        if "tool" in a:
            return f"<call {a['tool']} on {self.server} with {a.get('args', {})}>"
        return "Invalid action. Use search/describe/tool."


def setup_mcp(api: ExtensionAPI):
    api.register_tool(MCPProxyTool(mcp_server_url="http://localhost:3000"))
```

---

## 6. 最简 Harness 组装

```python
# main.py
import asyncio
import os
from pathlib import Path

from models import LLMProvider  # 见第 0 节
from tools import (ToolRegistry, ReadTool, WriteTool, EditTool,
                   BashTool, GrepTool, FindTool, LsTool)
from session import Session
from agent import Agent
from compaction import CompactionStrategy
from extensions import (ExtensionAPI, setup_security, setup_subagents,
                        setup_plan, setup_mcp)


class MockProvider:
    """占位 provider：让骨架不依赖真实 LLM 也能 import/跑通。
    接真实模型时，替换为对应 LLMProvider 适配层即可。"""
    name = "mock"
    model = "mock-model"

    def set_model(self, model: str) -> None:
        self.model = model

    def supports_thinking(self) -> bool:
        return False

    async def list_models(self) -> list[str]:
        return [self.model]

    async def close(self) -> None:
        pass

    def stream(self, messages, tools):
        async def _gen():
            class E: pass
            yield E()  # 真实实现产出 text/tool_call 事件
        return _gen()

    async def complete(self, prompt: str) -> str:
        return "[mock summary]"


async def main():
    provider = MockProvider()  # TODO: 换成真实 LLMProvider 适配

    tools = ToolRegistry()
    for t in (ReadTool(), WriteTool(), EditTool(), BashTool(),
              GrepTool(), FindTool(), LsTool()):
        tools.register(t)

    session = Session.create_new()
    compaction = CompactionStrategy(max_tokens=200_000, summariser=provider)

    agent = Agent(provider=provider, tools=tools, session=session, compaction=compaction)

    # 加载扩展（三动词 API 接到 agent 上）
    api = ExtensionAPI(agent)
    setup_security(api)
    setup_subagents(api)
    setup_plan(api)
    setup_mcp(api)

    print("Extensions loaded:", list(api.commands.keys()))
    print("Harness ready. (Mock provider — wire a real LLMProvider to run.)")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 参考项目

| 项目 | 语言 | Stars | 特点 |
|------|------|-------|------|
| [Edd Mann / my-own-coding-agent](https://github.com/eddmann/my-own-coding-agent) | Python | - | 7 Rings 完整实现 |
| [HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness) | Python | 15.3k | 研究导向，内置 agent Ohmo |
| [Pi](https://pi.dev) | Python | - | 最简主义，全推给扩展 |
| [OpenCode](https://github.com/sst/opencode) | TypeScript | - | 分层最细，server/TUI 双插件 |
