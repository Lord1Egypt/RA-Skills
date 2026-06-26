#!/usr/bin/env python3
"""
Hermes × OpenClaw sessions_spawn 自动集成
让新 spawn 的子智能体自动在 Hermes 注册订阅
"""

import json
import threading
import time
import uuid
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass

from hermes import hermes, HermesMessage, HermesAgent, OpenClawHermes


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
    def __init__(self, router: Optional[OpenClawHermes] = None,
                 pending_task_ttl: float = 3600.0):
        self._router = router or hermes
        self._subagents: Dict[str, HermesSubAgent] = {}
        self._handlers: Dict[str, Callable] = {}
        self._lock = threading.RLock()
        self._pending_tasks: Dict[str, Dict[str, Any]] = {}
        self._task_counter = 0
        self._task_lock = threading.Lock()
        self._pending_task_ttl = pending_task_ttl

    def _generate_task_id(self) -> str:
        """生成唯一任务 ID"""
        with self._task_lock:
            self._task_counter += 1
            return f"task-{self._task_counter}-{uuid.uuid4().hex[:8]}"

    def _cleanup_pending_tasks(self):
        """清理超时的 pending 任务，防止内存泄漏"""
        if self._pending_task_ttl <= 0:
            return
        now = time.time()
        cutoff = now - self._pending_task_ttl
        with self._lock:
            expired = [k for k, v in self._pending_tasks.items()
                       if v.get("submitted_at", 0) < cutoff]
            for k in expired:
                del self._pending_tasks[k]

    def on_agent_spawn(self, session_key: str, agent_id: str,
                      hermes_topics: List[str],
                      message_handler: Optional[Callable[[str, Any], None]] = None
                      ) -> HermesSubAgent:
        """
        当 sessions_spawn 创建新 Agent 后调用此方法
        自动在 Hermes 注册订阅指定主题
        """
        if not session_key or not agent_id:
            raise ValueError("session_key 和 agent_id 不能为空")
        if not hermes_topics:
            raise ValueError("hermes_topics 不能为空")

        for topic in hermes_topics:
            if not isinstance(topic, str):
                raise TypeError(f"topic 必须是 str，得到 {type(topic).__name__}")

        # 防御：防止重复注册，先清理旧的
        with self._lock:
            if session_key in self._subagents:
                self._force_exit(session_key)

        agent = self._router.register_agent(agent_id)

        if message_handler is None:
            message_handler = self._default_handler(session_key)

        sub_agent = HermesSubAgent(
            session_key=session_key,
            agent_id=agent_id,
            topics=list(hermes_topics),
            subscribed_at=time.time()
        )

        with self._lock:
            self._subagents[session_key] = sub_agent
            self._handlers[session_key] = message_handler

        for topic in hermes_topics:
            self._subscribe_topic(topic, agent, session_key)

        return sub_agent

    def _subscribe_topic(self, topic: str, agent: HermesAgent, session_key: str):
        """根据 topic 类型选择合适的订阅方法"""
        if topic.startswith("task:"):
            task_type = topic[5:]
            if task_type:
                self._subscribe_task(topic, agent, session_key, task_type)
        elif topic.startswith("done:"):
            task_type = topic[5:]
            if task_type:
                self._subscribe_done(topic, agent, session_key, task_type)
        elif topic.startswith("system:"):
            event_type = topic[7:]
            if event_type:
                self._subscribe_system(topic, agent, session_key, event_type)
        else:
            def make_handler(sk: str, t: str):
                def handler(msg: HermesMessage):
                    h = self._handlers.get(sk)
                    if h:
                        h(t, msg.payload)
                return handler
            agent.subscribe(topic, make_handler(session_key, topic))

    def _subscribe_task(self, topic: str, agent: HermesAgent,
                        session_key: str, task_type: str):
        def handler(msg: HermesMessage):
            h = self._handlers.get(session_key)
            if h:
                h(f"task:{task_type}", msg.payload)
        agent.subscribe(topic, handler)

    def _subscribe_done(self, topic: str, agent: HermesAgent,
                        session_key: str, task_type: str):
        def handler(msg: HermesMessage):
            h = self._handlers.get(session_key)
            if h:
                h(f"done:{task_type}", msg.payload)
        agent.subscribe(topic, handler)

    def _subscribe_system(self, topic: str, agent: HermesAgent,
                           session_key: str, event_type: str):
        def handler(msg: HermesMessage):
            h = self._handlers.get(session_key)
            if h:
                h(f"system:{event_type}", msg.payload)
        agent.subscribe(topic, handler)

    def _default_handler(self, session_key: str) -> Callable:
        """默认处理器，可被子类覆盖"""
        def handler(topic: str, payload: Any):
            pass
        return handler

    def _force_exit(self, session_key: str):
        """强制退出，不抛异常"""
        try:
            self._unsafe_exit(session_key)
        except Exception:
            pass

    def _unsafe_exit(self, session_key: str):
        """退出核心逻辑，无锁"""
        sub_agent = self._subagents[session_key]
        agent_id = sub_agent.agent_id
        for topic in sub_agent.topics:
            if isinstance(topic, str):
                try:
                    self._router.unsubscribe(topic, agent_id)
                except Exception:
                    pass
        self._router.unregister_agent(agent_id)
        self._handlers.pop(session_key, None)
        del self._subagents[session_key]

    def on_agent_exit(self, session_key: str):
        """Agent 退出时自动取消所有订阅"""
        with self._lock:
            if session_key not in self._subagents:
                return
            self._unsafe_exit(session_key)

    def submit_task_to_agents(self, task_type: str, creator: str,
                             session_id: str,
                             payload: Dict[str, Any]) -> str:
        """
        提交任务，自动分发到所有订阅了该任务类型的在线子智能体
        """
        if not task_type or not creator:
            raise ValueError("task_type 和 creator 不能为空")

        self._cleanup_pending_tasks()

        task_id = self._generate_task_id()
        topic = f"task:{task_type}"

        with self._lock:
            self._pending_tasks[task_id] = {
                "task_type": task_type,
                "creator": creator,
                "session_id": session_id,
                "payload": payload,
                "submitted_at": time.time()
            }

        self._router.publish(topic, creator, session_id, {
            "task_id": task_id,
            "task_type": task_type,
            "payload": payload
        })

        return task_id

    def publish_done(self, task_type: str, task_id: str, result: Any,
                     session_id: str, agent_id: str):
        """发布任务完成消息"""
        topic = f"done:{task_type}"
        self._router.publish(topic, agent_id, session_id, {
            "task_id": task_id,
            "result": result,
            "finished_at": time.time()
        })

    def publish_system(self, event_type: str, payload: Any,
                       session_id: str, agent_id: str):
        """发布系统事件"""
        topic = f"system:{event_type}"
        self._router.publish(topic, agent_id, session_id, payload)

    def list_agents(self) -> List[HermesSubAgent]:
        """列出所有当前注册的 Hermes 子智能体"""
        with self._lock:
            return list(self._subagents.values())

    def stats(self) -> Dict[str, Any]:
        """完整统计"""
        with self._lock:
            return {
                "registered_agents": len(self._subagents),
                "active_subagents": [
                    {"session": sa.session_key, "agent": sa.agent_id,
                     "topics": sa.topics}
                    for sa in self._subagents.values()
                ],
                "hermes": (self._router.get_global_stats()
                           if hasattr(self._router, 'get_global_stats')
                           else {}),
                "pending_tasks": len(self._pending_tasks)
            }


# === 全局实例 ===
hermes_sessions = HermesSessionsIntegration()


# === 演示 ===
if __name__ == "__main__":
    print("Hermes 与 sessions_spawn 集成演示")
    print("=" * 60)

    received = []
    received_lock = threading.Lock()

    def mock_handler(agent_name: str):
        def handler(topic: str, payload: Any):
            with received_lock:
                received.append((agent_name, topic, payload))
            print(f"  [{agent_name}] 收到 {topic}: "
                  f"{json.dumps(payload, ensure_ascii=False)}")
        return handler

    hermes_sessions.on_agent_spawn(
        session_key="session-code-1",
        agent_id="code-review-agent",
        hermes_topics=["task:code-review"],
        message_handler=mock_handler("code-agent")
    )

    hermes_sessions.on_agent_spawn(
        session_key="session-search-1",
        agent_id="web-search-agent",
        hermes_topics=["task:web-search"],
        message_handler=mock_handler("search-agent")
    )

    hermes_sessions.on_agent_spawn(
        session_key="session-doc-1",
        agent_id="write-doc-agent",
        hermes_topics=["task:write-doc", "done:code-review"],
        message_handler=mock_handler("doc-agent")
    )

    print(f"\n已注册 {len(hermes_sessions.list_agents())} 个子智能体")

    print("\n提交 code-review 任务...")
    task_id = hermes_sessions.submit_task_to_agents(
        task_type="code-review",
        creator="user",
        session_id="main",
        payload={"pr": "https://github.com/openclaw/openclaw/pull/123"}
    )
    print(f"   任务已分发，task_id: {task_id}")

    time.sleep(0.1)

    print("\n模拟 Agent 发布 done 消息...")
    hermes_sessions.publish_done(
        task_type="code-review",
        task_id=task_id,
        result={"status": "approved", "score": 95},
        session_id="main",
        agent_id="code-review-agent"
    )

    time.sleep(0.1)

    print(f"\n实际收到消息数: {len(received)}")
    print("\n当前统计:")
    print(json.dumps(hermes_sessions.stats(), indent=2, ensure_ascii=False))

    print("\n模拟一个子智能体退出...")
    hermes_sessions.on_agent_exit("session-code-1")
    print(f"   剩余注册 Agent: {len(hermes_sessions.list_agents())}")

    print("\n集成就绪！")
