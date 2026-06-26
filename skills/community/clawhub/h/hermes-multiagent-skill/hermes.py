#!/usr/bin/env python3
"""
Hermes 协议 - 集成到 OpenClaw 的突触式多智能体调度器
按照人类神经突触原理，实现毫秒级分发与精准对齐
"""

import threading
import time
import json
import uuid
from typing import Dict, Set, Callable, Any, Optional, List
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

# === 核心数据结构 ===

@dataclass
class HermesMessage:
    """Hermes 消息，类似神经突触释放的递质"""
    topic: str
    from_agent: str
    session_id: str
    payload: Any
    trace_id: str
    sent_at: float


class HermesSynapse:
    """
    Hermes 突触：连接发布者和订阅者
    负责一次分发，精准投递
    """
    __slots__ = ('topic', 'subscribers', 'lock')

    def __init__(self, topic: str):
        self.topic = topic
        self.subscribers: Dict[str, Callable[[HermesMessage], None]] = {}
        self.lock = threading.RLock()

    def add(self, agent_id: str, handler: Callable[[HermesMessage], None]):
        with self.lock:
            self.subscribers[agent_id] = handler

    def remove(self, agent_id: str):
        with self.lock:
            if agent_id in self.subscribers:
                del self.subscribers[agent_id]
                return len(self.subscribers) == 0
        return False

    def deliver(self, msg: HermesMessage, executor: ThreadPoolExecutor) -> int:
        """异步投递到所有订阅者，返回投递数量"""
        with self.lock:
            subscribers = dict(self.subscribers)

        if msg.from_agent in subscribers:
            del subscribers[msg.from_agent]

        count = len(subscribers)
        for agent_id, handler in subscribers.items():
            executor.submit(handler, msg)

        return count


class HermesRouter:
    """
    Hermes 核心路由器
    管理所有突触（主题），处理订阅、发布
    """
    def __init__(self, max_workers: int = None, pool_max: int = 1000):
        self._synapses: Dict[str, HermesSynapse] = {}
        self._global_lock = threading.RLock()
        self._executor = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="hermes-synapse-"
        )
        self._pool: List[HermesMessage] = []
        self._pool_lock = threading.Lock()
        self._pool_max = pool_max
        self._stats = {
            "total_published": 0,
            "total_delivered": 0,
            "active_subscriptions": 0
        }

    def _acquire_message(self, topic: str, from_agent: str,
                        session_id: str, payload: Any,
                        trace_id: str) -> HermesMessage:
        """从池分配消息，无锁快速路径"""
        with self._pool_lock:
            if self._pool:
                msg = self._pool.pop()
            else:
                msg = HermesMessage("", "", "", None, "", 0.0)
        msg.topic = topic
        msg.from_agent = from_agent
        msg.session_id = session_id
        msg.payload = payload
        msg.trace_id = trace_id
        msg.sent_at = time.time()
        return msg

    def _release_message(self, msg: HermesMessage):
        """归还消息到池"""
        with self._pool_lock:
            if len(self._pool) < self._pool_max:
                self._pool.append(msg)

    def subscribe(self, topic: str, agent_id: str,
                  handler: Callable[[HermesMessage], None]):
        """订阅一个主题"""
        with self._global_lock:
            if topic not in self._synapses:
                self._synapses[topic] = HermesSynapse(topic)
            self._synapses[topic].add(agent_id, handler)
            self._stats["active_subscriptions"] += 1

    def unsubscribe(self, topic: str, agent_id: str) -> bool:
        """取消订阅"""
        with self._global_lock:
            if topic not in self._synapses:
                return False
            synapse = self._synapses[topic]
            if agent_id not in dict(synapse.subscribers):
                return False
            empty = synapse.remove(agent_id)
            if empty:
                del self._synapses[topic]
            self._stats["active_subscriptions"] -= 1
            return True

    def publish(self, topic: str, from_agent: str, session_id: str,
                payload: Any, trace_id: str = "") -> int:
        """
        发布消息，异步投递
        返回预计投递数量
        """
        with self._global_lock:
            self._stats["total_published"] += 1
            if topic not in self._synapses:
                return 0
            synapse = self._synapses[topic]

        msg = self._acquire_message(topic, from_agent, session_id, payload, trace_id)
        delivered = synapse.deliver(msg, self._executor)

        with self._global_lock:
            self._stats["total_delivered"] += delivered

        self._executor.submit(self._safe_release, msg)

        return delivered

    def _safe_release(self, msg: HermesMessage):
        """安全回收消息，吞掉 handler 抛出的异常"""
        try:
            self._release_message(msg)
        except Exception:
            pass

    def get_stats(self) -> Dict[str, Any]:
        """获取当前统计"""
        with self._global_lock:
            return {
                **dict(self._stats),
                "topics": len(self._synapses),
                "pool_size": len(self._pool)
            }

    def shutdown(self):
        """关闭线程池"""
        self._executor.shutdown(wait=True)


# === Hermes 智能体基类 ===

class HermesAgent:
    """
    Hermes Agent 基类
    每个 Agent 只通过 Hermes 路由器和其他 Agent 通信
    """
    def __init__(self, agent_id: str, router: HermesRouter):
        self.agent_id = agent_id
        self.router = router
        self._subscribed_topics: Set[str] = set()
        self.received_count = 0
        self._lock = threading.Lock()

    def subscribe(self, topic: str, handler: Callable[[HermesMessage], None]):
        """订阅主题"""
        self._subscribed_topics.add(topic)
        self.router.subscribe(topic, self.agent_id, self._wrap_handler(handler))

    def unsubscribe(self, topic: str):
        """取消订阅"""
        if topic in self._subscribed_topics:
            self._subscribed_topics.discard(topic)
            self.router.unsubscribe(topic, self.agent_id)

    def publish(self, topic: str, session_id: str, payload: Any, trace_id: str = ""):
        """发布消息"""
        return self.router.publish(topic, self.agent_id, session_id, payload, trace_id)

    def _wrap_handler(self, handler: Callable[[HermesMessage], None]):
        def wrapped(msg: HermesMessage):
            try:
                handler(msg)
            finally:
                with self._lock:
                    self.received_count += 1
        return wrapped

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "agent_id": self.agent_id,
                "subscribed_topics": len(self._subscribed_topics),
                "received_count": self.received_count
            }


# === OpenClaw Hermes 集成 ===

class OpenClawHermes:
    """
    OpenClaw Hermes 调度器
    给当前 OpenClaw 实例提供 Hermes 风格的多智能体调度能力
    """
    _instance: Optional['OpenClawHermes'] = None

    def __new__(cls, max_workers: int = None):
        if cls._instance is None:
            instance = super().__new__(cls)
            instance._initialized = False
            with threading.Lock():
                if cls._instance is None:
                    cls._instance = instance
        return cls._instance

    def __init__(self, max_workers: int = None):
        if getattr(self, '_initialized', False):
            return
        self._initialized = True
        self.router = HermesRouter(max_workers=max_workers)
        self._agents: Dict[str, HermesAgent] = {}
        self._agents_lock = threading.RLock()

    def register_agent(self, agent_id: str) -> HermesAgent:
        """注册一个 Agent"""
        if not agent_id:
            raise ValueError("agent_id 不能为空")
        with self._agents_lock:
            if agent_id in self._agents:
                return self._agents[agent_id]
            agent = HermesAgent(agent_id, self.router)
            self._agents[agent_id] = agent
            return agent

    def unregister_agent(self, agent_id: str):
        """注销 Agent，取消所有订阅"""
        with self._agents_lock:
            if agent_id not in self._agents:
                return
            agent = self._agents[agent_id]
            for topic in list(agent._subscribed_topics):
                self.router.unsubscribe(topic, agent_id)
            del self._agents[agent_id]

    def subscribe(self, agent_id: str, topic: str,
                  handler: Callable[[HermesMessage], None]):
        """Agent 订阅主题"""
        if not agent_id or not topic:
            raise ValueError("agent_id 和 topic 不能为空")
        agent = self.register_agent(agent_id)
        agent.subscribe(topic, handler)

    def unsubscribe(self, topic: str, agent_id: str) -> bool:
        """Agent 取消订阅"""
        if agent_id not in self._agents:
            return False
        agent = self._agents[agent_id]
        agent.unsubscribe(topic)
        return True

    def publish(self, topic: str, from_agent: str, session_id: str,
                payload: Any, trace_id: str = "") -> int:
        """发布消息"""
        if not topic or not from_agent:
            raise ValueError("topic 和 from_agent 不能为空")
        return self.router.publish(topic, from_agent, session_id, payload, trace_id)

    def get_global_stats(self) -> Dict[str, Any]:
        """获取全局统计"""
        with self._agents_lock:
            return {
                "router": self.router.get_stats(),
                "total_agents": len(self._agents),
                "agents": [a.stats() for a in self._agents.values()]
            }

    def shutdown(self):
        """关闭"""
        self.router.shutdown()


# === 全局实例 ===
hermes = OpenClawHermes()

_received_counter = 0
_counter_lock = threading.Lock()


# === 演示 ===
if __name__ == "__main__":
    print("Hermes 协议 - OpenClaw 突触式调度器测试")
    print("=" * 60)

    N = 100
    received_total = 0
    received_lock = threading.Lock()

    def on_message(msg: HermesMessage):
        global received_total
        with received_lock:
            received_total += 1

    start = time.time()

    topics = ["task:start", "task:progress", "task:done", "error", "broadcast"]
    for i in range(N):
        agent_id = f"test-agent-{i}"
        agent = hermes.register_agent(agent_id)
        for t in topics:
            if (i + hash(t)) % 2 == 0:
                agent.subscribe(t, on_message)

    reg_time = time.time()
    print(f"注册完成 {N} Agent，耗时: {(reg_time - start)*1000:.2f}ms")

    def publisher(agent_idx: int):
        agent_id = f"test-agent-{agent_idx}"
        for m in range(10):
            topic = topics[(agent_idx + m) % len(topics)]
            hermes.publish(topic, agent_id, "test-session", {
                "seq": m,
                "data": f"data-from-{agent_idx}-{m}"
            })

    threads = []
    publish_start = time.time()
    for i in range(N):
        t = threading.Thread(target=publisher, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    publish_end = time.time()
    time.sleep(0.2)
    total_time = time.time() - start

    stats = hermes.get_global_stats()
    print(f"发布完成，耗时: {(publish_end - publish_start)*1000:.2f}ms")
    print(f"总耗时: {total_time*1000:.2f}ms")
    print()
    print("统计:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    print()
    print(f"实际收到消息: {received_total}")
    if received_total > 0:
        print(f"平均每条耗时: {(total_time*1000)/received_total:.3f}ms")

    hermes.shutdown()
    print()
    print("Hermes 调度器就绪！")
