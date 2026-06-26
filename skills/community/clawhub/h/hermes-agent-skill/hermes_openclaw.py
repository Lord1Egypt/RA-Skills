#!/usr/bin/env python3
"""
Hermes 协议 × OpenClaw 日常工作流集成
让 Hermes 承担实际的多智能体调度，而不只是测试
"""

import sys
import json
import threading
import time
import traceback
from typing import Dict, Callable, Any, Optional, List
from dataclasses import dataclass

# 导入核心 Hermes
from hermes import HermesRouter, HermesMessage, OpenClawHermes, hermes

# === 日常工作流中的 Hermes 应用 ===
# 1. 子任务分发：多个子 Agent 只订阅自己关心的任务类型
# 2. 进度通知：感兴趣的 Agent 自然会收到，不需要全量通知
# 3. 结果汇聚：发布者只接收完成事件，精准对齐
# 4. 广播控制：系统控制消息只给订阅者，不打扰所有人

@dataclass
class WorkflowTask:
    """日常工作流任务"""
    task_id: str
    task_type: str
    session_id: str
    creator: str
    payload: Dict[str, Any]
    created_at: float

@dataclass
class TaskProgress:
    """任务进度更新"""
    task_id: str
    status: str  # pending/running/done/failed
    progress: int  # 0-100
    message: str
    updated_at: float

# 主题命名规范（日常工作流）
TOPIC_TASK_NEW = "workflow:task:{task_type}"
TOPIC_TASK_PROGRESS = "workflow:progress:{task_id}"
TOPIC_TASK_DONE = "workflow:done:{task_type}"
TOPIC_SYSTEM_EVENT = "system:event:{event_type}"

class HermesWorkflowScheduler:
    """
    Hermes 驱动的 OpenClaw 日常工作流调度器
    融入你的日常多智能体工作，不只是测试
    """
    def __init__(self):
        self.hermes = hermes  # 使用全局单例
        self._running_tasks: Dict[str, WorkflowTask] = {}
        self._lock = threading.RLock()

        # 注册自己作为系统代理
        self.agent_id = "hermes-workflow-scheduler"
        self.hermes.register_agent(self.agent_id)

    def submit_task(self, task_type: str, creator: str, session_id: str,
                   payload: Dict[str, Any]) -> str:
        """
        提交一个新任务到 Hermes 调度
        只有订阅了这个 task_type 的 Agent 会收到
        """
        import uuid
        task_id = str(uuid.uuid4())[:8]

        task = WorkflowTask(
            task_id=task_id,
            task_type=task_type,
            session_id=session_id,
            creator=creator,
            payload=payload,
            created_at=time.time()
        )

        with self._lock:
            self._running_tasks[task_id] = task

        # 发布到对应主题，订阅了这个任务类型的 Agent 会自动收到
        topic = f"workflow:task:{task_type}"
        self.hermes.publish(
            topic=topic,
            from_agent=self.agent_id,
            session_id=session_id,
            payload={
                "task": task.__dict__
            },
            trace_id=task_id
        )

        return task_id

    def subscribe_task_type(self, task_type: str, agent_id: str,
                           handler: Callable[[WorkflowTask, HermesMessage], None]):
        """Agent 订阅某种类型的任务"""
        topic = f"workflow:task:{task_type}"

        def wrapped(msg: HermesMessage):
            task_data = msg.payload["task"]
            task = WorkflowTask(**task_data)
            handler(task, msg)

        self.hermes.subscribe(topic, agent_id, wrapped)

    def publish_progress(self, task_id: str, agent_id: str,
                        status: str, progress: int, message: str = ""):
        """发布任务进度"""
        progress = TaskProgress(
            task_id=task_id,
            status=status,
            progress=progress,
            message=message,
            updated_at=time.time()
        )

        topic = f"workflow:progress:{task_id}"
        self.hermes.publish(
            topic=topic,
            from_agent=agent_id,
            session_id="",  # 从任务获取
            payload=progress.__dict__
        )

    def subscribe_progress(self, task_id: str, handler: Callable[[TaskProgress], None]):
        """订阅某个任务的进度更新"""
        topic = f"workflow:progress:{task_id}"

        def wrapped(msg: HermesMessage):
            progress = TaskProgress(**msg.payload)
            handler(progress)

        self.hermes.subscribe(topic, "waiter-" + task_id, wrapped)

    def publish_done(self, task_type: str, task_id: str, agent_id: str,
                    result: Any):
        """任务完成发布"""
        topic = f"workflow:done:{task_type}"
        self.hermes.publish(
            topic=topic,
            from_agent=agent_id,
            session_id="",
            payload={
                "task_id": task_id,
                "result": result,
                "finished_at": time.time()
            }
        )

        with self._lock:
            if task_id in self._running_tasks:
                del self._running_tasks[task_id]

    def subscribe_done(self, task_type: str, agent_id: str,
                      handler: Callable[[str, Any, float], None]):
        """订阅某种任务的完成事件"""
        topic = f"workflow:done:{task_type}"

        def wrapped(msg: HermesMessage):
            payload = msg.payload
            handler(payload["task_id"], payload["result"], payload["finished_at"])

        self.hermes.subscribe(topic, agent_id, wrapped)

    def system_event(self, event_type: str, payload: Dict[str, Any]):
        """发布系统事件"""
        topic = f"system:event:{event_type}"
        self.hermes.publish(
            topic=topic,
            from_agent=self.agent_id,
            session_id="",
            payload=payload
        )

    def subscribe_system(self, event_type: str, agent_id: str,
                        handler: Callable[[Dict[str, Any]], None]):
        """订阅系统事件"""
        topic = f"system:event:{event_type}"

        def wrapped(msg: HermesMessage):
            handler(msg.payload)

        self.hermes.subscribe(topic, agent_id, wrapped)

    def stats(self):
        """获取当前调度状态"""
        with self._lock:
            return {
                "hermes": self.hermes.get_global_stats(),
                "running_tasks": len(self._running_tasks),
                "running_task_ids": list(self._running_tasks.keys())
            }

# === 实际使用例子：日常多任务处理 ===
# 你日常工作中，把不同类型任务分给不同 Agent 处理，用 Hermes 调度

class WorkerPoolExample:
    """
    例子：工作池模式
    多个 Worker Agent，每个只处理特定类型任务
    Hermes 自动分发，不需要你做路由
    """
    def __init__(self):
        self.scheduler = HermesWorkflowScheduler()
        self.results: Dict[str, Any] = {}
        self._result_lock = threading.Lock()

    def add_worker(self, worker_id: str, task_type: str):
        """添加一个工作者，订阅特定类型任务"""
        def handle_task(task: WorkflowTask, msg: HermesMessage):
            # 这里就是 Worker 处理任务
            print(f"⚡ {worker_id} 收到任务 [{task.task_type}] #{task.task_id}")

            # 模拟处理，发布进度
            self.scheduler.publish_progress(
                task.task_id, worker_id, "running", 50, "halfway"
            )

            time.sleep(0.1)  # 模拟工作

            # 完成，发布结果
            result = f"{worker_id} done: {task.payload}"
            self.scheduler.publish_done(
                task.task_type, task.task_id, worker_id, result
            )

            with self._result_lock:
                self.results[task.task_id] = result

        self.scheduler.subscribe_task_type(task_type, worker_id, handle_task)

    def run_parallel_tasks(self, task_type: str, count: int, creator: str = "user"):
        """并行提交多个任务"""
        task_ids = []
        for i in range(count):
            task_id = self.scheduler.submit_task(
                task_type=task_type,
                creator=creator,
                session_id="main",
                payload={"index": i}
            )
            task_ids.append(task_id)
        return task_ids

# === 日常使用入口 ===

hermes_workflow = HermesWorkflowScheduler()

if __name__ == "__main__":
    print("🧠 Hermes 集成到 OpenClaw 日常工作流")
    print("=" * 60)

    # 演示：并行处理多个任务
    pool = WorkerPoolExample()

    # 添加不同 worker 处理不同类型任务
    # 就像你日常 spawn 多个子智能体，每个负责不同领域
    pool.add_worker("code-agent", "code-review")
    pool.add_worker("doc-agent", "write-doc")
    pool.add_worker("search-agent", "web-search")
    pool.add_worker("summary-agent", "summarize")

    print("\n📋 Worker 已注册：")
    print("   - code-agent    → 处理 code-review 任务")
    print("   - doc-agent     → 处理 write-doc 任务")
    print("   - search-agent  → 处理 web-search 任务")
    print("   - summary-agent → 处理 summarize 任务")

    # 并行提交多个不同类型任务
    print("\n🚀 并行提交 8 个任务...")
    tasks = [
        ("code-review", 3),
        ("write-doc", 2),
        ("web-search", 2),
        ("summarize", 1),
    ]

    all_task_ids = []
    for task_type, count in tasks:
        ids = pool.run_parallel_tasks(task_type, count)
        all_task_ids.extend(ids)

    # 等一会儿让它们完成
    time.sleep(0.5)

    print("\n✅ 所有任务完成！")
    print(f"   完成: {len(pool.results)}/{len(all_task_ids)}")

    print("\n📊 当前 Hermes 状态:")
    print(json.dumps(hermes_workflow.stats(), indent=2, ensure_ascii=False))

    print("\n🎉 Hermes 已融入日常工作流，可以使用了！")
    print("\n使用方式：")
    print("from hermes_openclaw import hermes_workflow")
    print("task_id = hermes_workflow.submit_task('code-review', 'user', 'session', {'pr': 123})")
    print("  → 自动分发给订阅了 code-review 的 Agent")
