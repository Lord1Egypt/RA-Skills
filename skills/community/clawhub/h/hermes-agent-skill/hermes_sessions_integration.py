#!/usr/bin/env python3
"""
Hermes × OpenClaw sessions_spawn 自动集成
让新 spawn 的子智能体自动在 Hermes 注册订阅

隐私说明：
- sessions_send fallback 日志受 hermes_config.session_fallback_log_level 控制
- 默认为 "summary"，仅记录 topic，不记录 payload 内容
"""

import sys
import json
import threading
import time
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass

from hermes_config import hermes_config
from hermes import hermes, HermesMessage
from hermes_openclaw import hermes_workflow, WorkflowTask

@dataclass
class HermesSubAgent:
    """子智能体的 Hermes 注册信息"""
    session_key: str
    agent_id: str
    topics: List[str]
    subscribed_at: float
    auto_unsubscribe: bool = True

class HermesSessionsIntegration:
    """
    Hermes 与 OpenClaw sessions_spawn 集成
    自动处理子智能体订阅和生命周期
    """
    def __init__(self):
        self.hermes = hermes
        self.workflow = hermes_workflow
        self._subagents: Dict[str, HermesSubAgent] = {}
        self._lock = threading.RLock()

    def on_agent_spawn(self, session_key: str, agent_id: str,
                      hermes_topics: List[str],
                      message_handler: Optional[Callable[[str, Any], None]] = None) -> HermesSubAgent:
        """
        当 sessions_spawn 创建新 Agent 后调用此方法
        自动在 Hermes 注册订阅指定主题
        """
        with self._lock:
            sub_agent = HermesSubAgent(
                session_key=session_key,
                agent_id=agent_id,
                topics=hermes_topics,
                subscribed_at=time.time()
            )

            # 默认处理器：把消息发到会话
            if message_handler is None:
                message_handler = self._default_handler(session_key)

            # 订阅每个主题
            for topic in hermes_topics:
                # 如果是任务类型，订阅任务分发
                if topic.startswith("task:"):
                    task_type = topic[5:]
                    self.workflow.subscribe_task_type(
                        task_type,
                        agent_id,
                        lambda task, msg: message_handler(f"task:{task_type}", task)
                    )
                elif topic.startswith("done:"):
                    task_type = topic[5:]
                    self.workflow.subscribe_done(
                        task_type,
                        agent_id,
                        lambda task_id, result, ts: message_handler(f"done:{task_type}", {
                            "task_id": task_id,
                            "result": result,
                            "finished_at": ts
                        })
                    )
                elif topic.startswith("system:"):
                    event_type = topic[7:]
                    self.workflow.subscribe_system(
                        event_type,
                        agent_id,
                        lambda payload: message_handler(f"system:{event_type}", payload)
                    )
                else:
                    # 通用主题订阅
                    def handler(msg: HermesMessage):
                        message_handler(msg.topic, msg.payload)
                    self.hermes.subscribe(topic, agent_id, handler)

            self._subagents[session_key] = sub_agent
            return sub_agent

    def _default_handler(self, session_key: str) -> Callable:
        """默认处理器：把 Hermes 消息发到会话。payload 内容不直接打印到日志。"""
        def handler(topic: str, payload: Any):
            log_level = hermes_config.session_fallback_log_level
            if log_level == "off":
                return

            record = {
                "hermes": {
                    "topic": topic,
                    "session": session_key,
                }
            }
            if log_level == "full":
                record["hermes"]["payload"] = payload

            try:
                from sessions_send import sessions_send
                sessions_send(session_key, json.dumps(record, ensure_ascii=False))
            except ImportError:
                print(json.dumps(record, ensure_ascii=False), file=sys.stderr)
        return handler

    def on_agent_exit(self, session_key: str):
        """
        Agent 退出时自动取消所有订阅
        """
        with self._lock:
            if session_key not in self._subagents:
                return

            sub_agent = self._subagents[session_key]
            agent_id = sub_agent.agent_id

            # 取消所有订阅
            for topic in sub_agent.topics:
                if topic.startswith("task:"):
                    task_type = topic[5:]
                    self.hermes.unsubscribe(f"workflow:task:{task_type}", agent_id)
                elif topic.startswith("done:"):
                    task_type = topic[5:]
                    self.hermes.unsubscribe(f"workflow:done:{task_type}", agent_id)
                elif topic.startswith("system:"):
                    event_type = topic[7:]
                    self.hermes.unsubscribe(f"system:event:{event_type}", agent_id)
                else:
                    self.hermes.unsubscribe(topic, agent_id)

            del self._subagents[session_key]

    def submit_task_to_agents(self, task_type: str, creator: str, session_id: str,
                             payload: Dict[str, Any]) -> str:
        """
        提交任务，自动分发到所有订阅了该任务类型的在线子智能体
        这就是你日常使用最常用的入口
        """
        return self.workflow.submit_task(task_type, creator, session_id, payload)

    def list_agents(self) -> List[HermesSubAgent]:
        """列出所有当前注册的 Hermes 子智能体"""
        with self._lock:
            return list(self._subagents.values())

    def stats(self):
        """完整统计"""
        with self._lock:
            return {
                "registered_agents": len(self._subagents),
                "active_subagents": [
                    {"session": sa.session_key, "agent": sa.agent_id, "topics": sa.topics}
                    for sa in self._subagents.values()
                ],
                "hermes": self.hermes.get_global_stats(),
                "workflow": self.workflow.stats()
            }

# === 全局实例 ===
hermes_sessions = HermesSessionsIntegration()

# === 演示 ===
if __name__ == "__main__":
    print("🔌 Hermes 与 sessions_spawn 集成演示")
    print("=" * 60)

    # 模拟 spawn 几个子智能体，每个订阅不同主题
    # 这就是你日常调用 sessions_spawn 之后做的事情

    def mock_handler(agent_name):
        def handler(topic, payload):
            print(f"  [{agent_name}] 收到 {topic}: {json.dumps(payload, ensure_ascii=False)}")
        return handler

    # spawn 三个子智能体，分别订阅不同任务类型
    hermes_sessions.on_agent_spawn(
        session_key="session-code-1",
        agent_id="code-review-agent",
        hermes_topics=["task:code-review"],
        message_handler=mock_handler("code-agent")
    )

    hermes_sessions.on_agent_spawn(
        session_key="session-search-1",
        agent_id="web-search-agent",
        hermes_topics=["task:web-search", "system:*"],
        message_handler=mock_handler("search-agent")
    )

    hermes_sessions.on_agent_spawn(
        session_key="session-doc-1",
        agent_id="write-doc-agent",
        hermes_topics=["task:write-doc", "done:code-review"],
        message_handler=mock_handler("doc-agent")
    )

    print(f"\n📋 已注册 {len(hermes_sessions.list_agents())} 个子智能体")

    # 你提交一个任务，Hermes 自动分发
    print("\n🚀 提交 code-review 任务...")
    task_id = hermes_sessions.submit_task_to_agents(
        task_type="code-review",
        creator="user",
        session_id="main",
        payload={"pr": "https://github.com/openclaw/openclaw/pull/123"}
    )
    print(f"   任务已分发，task_id: {task_id}")

    print("\n📊 当前统计:")
    print(json.dumps(hermes_sessions.stats(), indent=2, ensure_ascii=False))

    # 演示退出自动清理
    print("\n🧹 模拟一个子智能体退出，自动取消订阅...")
    hermes_sessions.on_agent_exit("session-code-1")
    print(f"   剩余注册 Agent: {len(hermes_sessions.list_agents())}")

    print("\n✅ 集成就绪，现在可以用了！")
    print()
    print("""# 你的日常使用方式

当你要 spawn 一个负责特定任务的子智能体：

1. spawn 子智能体 (sessions_spawn)
2. 调用: hermes_sessions.on_agent_spawn(session_key, agent_id, ["task:code-review"])
3. 之后你只要: hermes_sessions.submit_task_to_agents("code-review", ...)
4. Hermes 自动分发 -> 子智能体自动收到 -> 处理完发布 done -> 关心结果的人收到

就像神经突触一样，精准，毫秒级，不浪费任何通信。
""")
