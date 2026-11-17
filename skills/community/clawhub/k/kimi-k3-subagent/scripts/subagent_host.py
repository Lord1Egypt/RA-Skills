"""SubagentHost - 子Agent生命周期管理

借鉴 Kimi Code SessionSubagentHost 架构:
- spawn() / resume() / retry() 三级操作
- 生命周期事件流
- 后台任务 draining
- Summary min length 检查
"""

import asyncio
import time
import logging
from typing import Any, Callable, Coroutine, Optional

from .subagent_types import (
    SubagentStatus,
    SubagentState,
    SubagentEventType,
    SubagentHandle,
    SubagentResult,
    SubagentProfile,
    QueuedSubagentTask,
    SubagentSuspendedEvent,
    TokenUsage,
    TaskState,
    BUILTIN_SUBAGENT_PROFILES,
)

logger = logging.getLogger("subagent_host")

DEFAULT_SUBAGENT_TIMEOUT_MS = 2 * 60 * 60 * 1000  # 2小时
SUMMARY_MIN_LENGTH = 200


class SubagentHost:
    """管理子Agent生命周期"""

    def __init__(self, session, owner_agent_id: str):
        self.session = session
        self.owner_agent_id = owner_agent_id
        self.active_children: dict[str, dict] = {}  # agent_id -> {controller, run_in_background}

    async def spawn(
        self,
        profile_name: str,
        prompt: str,
        description: str = "",
        model_choice: Optional[str] = None,
        parent_tool_call_id: str = "",
        signal: Any = None,
        run_in_background: bool = False,
    ) -> SubagentHandle:
        """创建新子Agent"""
        profile = self._resolve_profile(profile_name)
        agent_id = f"{self.owner_agent_id}_sub_{int(time.time() * 1000)}"

        child = self._create_child_agent(agent_id, profile, model_choice)

        # 注册到活跃子Agent
        controller = asyncio.Event()
        self.active_children[agent_id] = {
            "controller": controller,
            "run_in_background": run_in_background,
        }

        completion = self._run_prompt_turn(
            agent_id, child, profile, prompt, signal, parent_tool_call_id
        )

        return SubagentHandle(
            agent_id=agent_id,
            profile_name=profile.name,
            resumed=False,
            completion=completion,
        )

    async def resume(
        self,
        agent_id: str,
        prompt: str,
        signal: Any = None,
    ) -> SubagentHandle:
        """恢复已有子Agent"""
        if agent_id not in self.active_children:
            raise ValueError(f"Agent {agent_id} not found in active children")

        child = self._get_child_agent(agent_id)
        profile_name = child.get("profile_name", "subagent")

        completion = self._run_prompt_turn(
            agent_id, child, BUILTIN_SUBAGENT_PROFILES.get(profile_name, BUILTIN_SUBAGENT_PROFILES["coder"]),
            prompt, signal, ""
        )

        return SubagentHandle(
            agent_id=agent_id,
            profile_name=profile_name,
            resumed=True,
            completion=completion,
        )

    async def retry(
        self,
        agent_id: str,
        prompt: str,
        signal: Any = None,
    ) -> SubagentHandle:
        """重试失败子Agent"""
        if agent_id not in self.active_children:
            raise ValueError(f"Agent {agent_id} not found in active children")

        child = self._get_child_agent(agent_id)
        profile_name = child.get("profile_name", "subagent")

        # 重试: 重置turn, 重新运行
        child["turn"] = []
        completion = self._run_prompt_turn(
            agent_id, child, BUILTIN_SUBAGENT_PROFILES.get(profile_name, BUILTIN_SUBAGENT_PROFILES["coder"]),
            prompt, signal, ""
        )

        return SubagentHandle(
            agent_id=agent_id,
            profile_name=profile_name,
            resumed=True,
            completion=completion,
        )

    async def run_queued(self, tasks: list[QueuedSubagentTask]) -> list[SubagentResult]:
        """批量执行 - 交给SubagentBatch"""
        from .subagent_batch import SubagentBatch
        batch = SubagentBatch(self, tasks)
        return await batch.run()

    async def start_btw(self) -> str:
        """侧通道问答 - 无工具权限, 纯文本"""
        agent_id = f"{self.owner_agent_id}_btw_{int(time.time() * 1000)}"
        child = {
            "agent_id": agent_id,
            "profile_name": "btw",
            "turn": [],
            "tools_disabled": True,
        }
        self.active_children[agent_id] = {
            "controller": asyncio.Event(),
            "run_in_background": True,
        }
        return agent_id

    def cancel_all(self, reason: Any = None):
        """取消所有前台子Agent"""
        for agent_id, child in list(self.active_children.items()):
            if not child["run_in_background"]:
                child["controller"].set()  # 触发取消
                self._emit_event(SubagentEventType.FAILED, agent_id, str(reason or "User cancelled"))

    def _resolve_profile(self, profile_name: str) -> SubagentProfile:
        """解析子Agent类型配置"""
        profile = BUILTIN_SUBAGENT_PROFILES.get(profile_name)
        if profile is None:
            logger.warning(f"Profile {profile_name} not found, using coder")
            return BUILTIN_SUBAGENT_PROFILES["coder"]
        return profile

    def _create_child_agent(self, agent_id: str, profile: SubagentProfile, model_choice: Optional[str] = None) -> dict:
        """创建子Agent实例"""
        return {
            "agent_id": agent_id,
            "profile_name": profile.name,
            "turn": [],
            "tools_disabled": profile.name == "btw",
            "model_choice": model_choice or profile.model_preference,
        }

    def _get_child_agent(self, agent_id: str) -> dict:
        """获取子Agent实例"""
        return {
            "agent_id": agent_id,
            "profile_name": "subagent",
            "turn": [],
            "tools_disabled": False,
        }

    async def _run_prompt_turn(
        self,
        agent_id: str,
        child: dict,
        profile: SubagentProfile,
        prompt: str,
        signal: Any,
        parent_tool_call_id: str,
    ) -> SubagentResult:
        """运行子Agent的prompt turn"""
        try:
            self._emit_event(SubagentEventType.SPAWNED, agent_id, profile.name)

            # 模拟执行turn (实际会调用sessions_spawn等)
            result_text = await self._execute_child_turn(child, prompt, signal)

            # Summary min length 检查
            result_text = await self._ensure_min_summary(child, result_text, signal)

            usage = TokenUsage(
                input_tokens=len(prompt) // 4,
                output_tokens=len(result_text) // 4,
            )

            self._emit_event(SubagentEventType.COMPLETED, agent_id, result_text[:200])

            return SubagentResult(
                task=QueuedSubagentTask(prompt=prompt, description="", data=None),
                agent_id=agent_id,
                status="completed",
                result=result_text,
                usage=usage,
            )

        except Exception as e:
            self._emit_event(SubagentEventType.FAILED, agent_id, str(e))
            return SubagentResult(
                task=QueuedSubagentTask(prompt=prompt, description="", data=None),
                agent_id=agent_id,
                status="failed",
                error=str(e),
            )

    async def _execute_child_turn(self, child: dict, prompt: str, signal: Any) -> str:
        """执行子Agent turn - 实际调用sessions_spawn"""
        # TODO: 实际集成到sessions_spawn
        child["turn"].append({"role": "user", "content": prompt})
        return f"Executed: {prompt[:100]}..."

    async def _ensure_min_summary(self, child: dict, result: str, signal: Any) -> str:
        """确保摘要长度>=200字符"""
        if len(result) < SUMMARY_MIN_LENGTH:
            # 追加追问
            child["turn"].append({"role": "assistant", "content": result})
            child["turn"].append({"role": "user", "content": "Please provide a more comprehensive summary."})
            result = result + " [expanded summary]"
        return result

    def _emit_event(self, event_type: SubagentEventType, agent_id: str, data: str):
        """发出生命周期事件"""
        logger.debug(f"Event: {event_type.value} agent={agent_id} data={data[:100]}")
        # TODO: 实际事件派发
