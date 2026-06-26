#!/usr/bin/env python3
"""
Hermes 协议 - 集成到 OpenClaw 的突触式多智能体调度器
按照人类神经突触原理，实现毫秒级分发与精准对齐
"""

import threading
import time
import json
from typing import Dict, Set, Callable, Any, Optional, List
from dataclasses import dataclass, asdict
from collections import defaultdict
import asyncio
from concurrent.futures import ThreadPoolExecutor
import copy

# === 核心数据结构 ===

@dataclass
class HermesMessage:
    """Hermes 消息，类似神经突触释放的递质"""
    topic: str
    from_agent: str
    session_id: str
    payload: Any
    trace_id: str
    sent_at: float  # 时间戳，毫秒级对齐

@dataclass
class Subscription:
    """订阅记录"""
    agent_id: str
    topic: str
    handler: Callable[[HermesMessage], None]
    subscribed_at: float

class HermesSynapse:
    """
    Hermes 突触：连接发布者和订阅者
    负责一次分发，精准投递
    """
    __slots__ = ['topic', 'subscribers', 'lock']
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

    def deliver(self, msg: HermesMessage, executor: ThreadPoolExecutor):
        """异步投递到所有订阅者"""
        with self.lock:
            for agent_id, handler in self.subscribers.items():
                if agent_id == msg.from_agent:
                    continue  # 不自播
                executor.submit(handler, msg)

        return len(self.subscribers) - (1 if msg.from_agent in self.subscribers else 0)

class HermesRouter:
    """
    Hermes 核心路由器
    管理所有突触（主题），处理订阅、发布
    """
    def __init__(self, max_workers: int = None):
        # 按主题分组的突触
        self._synapses: Dict[str, HermesSynapse] = {}
        self._global_lock = threading.RLock()

        # 线程池用于异步投递
        self._executor = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="hermes-synapse-"
        )

        # 对象池复用消息对象
        self._pool: List[HermesMessage] = []
        self._pool_lock = threading.Lock()

        # 统计
        self.stats = {
            "total_published": 0,
            "total_delivered": 0,
            "active_subscriptions": 0
        }

    def _get_message(self) -> HermesMessage:
        # 已弃用对象池，高并发下会导致脏乱数据，直接返回新对象即可
        return HermesMessage(None, None, None, None, "", 0)

    def _put_message(self, msg: HermesMessage):
        # 弃用回收
        pass

    def subscribe(self, topic: str, agent_id: str, handler: Callable[[HermesMessage], None]):
        """订阅一个主题"""
        with self._global_lock:
            if topic not in self._synapses:
                self._synapses[topic] = HermesSynapse(topic)
            synapse = self._synapses[topic]
            synapse.add(agent_id, handler)
            self.stats["active_subscriptions"] += 1

    def unsubscribe(self, topic: str, agent_id: str) -> bool:
        """取消订阅"""
        with self._global_lock:
            if topic not in self._synapses:
                return False
            synapse = self._synapses[topic]
            empty = synapse.remove(agent_id)
            if empty:
                del self._synapses[topic]
            if self.stats["active_subscriptions"] > 0:
                self.stats["active_subscriptions"] -= 1
            return True

    def publish(self, topic: str, from_agent: str, session_id: str,
                payload: Any, trace_id: str = "") -> int:
        """
        发布消息，异步投递
        返回预计投递数量
        """
        with self._global_lock:
            self.stats["total_published"] += 1
            if topic not in self._synapses:
                return 0

            synapse = self._synapses[topic]

        # 使用深拷贝分配新消息，确保多租户 Payload 隔离
        msg = HermesMessage(
            topic=topic,
            from_agent=from_agent,
            session_id=session_id,
            payload=copy.deepcopy(payload),
            trace_id=trace_id,
            sent_at=time.time()
        )

        # 投递
        delivered = synapse.deliver(msg, self._executor)

        with self._global_lock:
            self.stats["total_delivered"] += delivered

        # 返回预计投递数
        return delivered

    def get_stats(self):
        """获取当前统计"""
        with self._global_lock:
            return {
                **self.stats,
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
            self.router.unsubscribe(topic, self.agent_id)
            self._subscribed_topics.remove(topic)

    def publish(self, topic: str, session_id: str, payload: Any, trace_id: str = ""):
        """发布消息"""
        return self.router.publish(topic, self.agent_id, session_id, payload, trace_id)

    def _wrap_handler(self, handler: Callable[[HermesMessage], None]):
        def wrapped(msg: HermesMessage):
            with self._lock:
                self.received_count += 1
            handler(msg)
        return wrapped

    def stats(self):
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
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """单例模式，全局一个路由器"""
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, max_workers: int = None):
        if self._initialized:
            return
        self._initialized = True
        self.router = HermesRouter(max_workers=max_workers)
        self._agents: Dict[str, HermesAgent] = {}
        self._agents_lock = threading.RLock()

    def register_agent(self, agent_id: str) -> HermesAgent:
        """注册一个 Agent"""
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
            # 取消所有订阅
            for topic in list(agent._subscribed_topics):
                self.router.unsubscribe(topic, agent_id)
            del self._agents[agent_id]

    def subscribe(self, agent_id: str, topic: str, handler: Callable[[HermesMessage], None]):
        """Agent 订阅主题"""
        agent = self.register_agent(agent_id)
        agent.subscribe(topic, handler)

    def unsubscribe(self, topic: str, agent_id: str) -> bool:
        """Agent 取消订阅"""
        if agent_id not in self._agents:
            return False
        agent = self._agents[agent_id]
        agent.unsubscribe(topic)
        return self.router.unsubscribe(topic, agent_id)

    def publish(self, topic: str, from_agent: str, session_id: str, payload: Any, trace_id: str = ""):
        """发布消息"""
        return self.router.publish(topic, from_agent, session_id, payload, trace_id)

    def get_global_stats(self):
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

# === 开箱即用的全局实例 ===
# 现在 OpenClaw 直接拥有 Hermes 能力了！

hermes = OpenClawHermes()

# 示例：使用方式
if __name__ == "__main__":
    print("🧠 Hermes 协议 - OpenClaw 突触式调度器测试")
    print("=" * 60)

    # 测试：100 个 Agent 并发
    N = 100

    received_total = 0
    received_lock = threading.Lock()

    def on_message(msg: HermesMessage):
        global received_total
        with received_lock:
            received_total += 1

    start = time.time()

    # 注册 100 个 Agent，每个订阅几个主题
    topics = ["task:start", "task:progress", "task:done", "error", "broadcast"]
    for i in range(N):
        agent_id = f"test-agent-{i}"
        agent = hermes.register_agent(agent_id)
        # 稀疏订阅
        for t in topics:
            if (i + hash(t)) % 2 == 0:
                agent.subscribe(t, on_message)

    reg_time = time.time()
    print(f"注册完成 {N} Agent，耗时: {(reg_time - start)*1000:.2f}ms")

    # 并发发布
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

    # 等待投递完成
    time.sleep(0.2)

    total_time = time.time() - start

    stats = hermes.get_global_stats()
    print(f"发布完成，耗时: {(publish_end - publish_start)*1000:.2f}ms")
    print(f"总耗时: {total_time*1000:.2f}ms")
    print()
    print("📊 统计:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    print()
    print(f"实际收到消息: {received_total}")
    if received_total > 0:
        print(f"平均每条耗时: {(total_time*1000)/received_total:.3f}ms")

    hermes.shutdown()
    print()
    print("✅ Hermes 调度器就绪！OpenClaw 现在拥有毫秒级分发能力了。")
