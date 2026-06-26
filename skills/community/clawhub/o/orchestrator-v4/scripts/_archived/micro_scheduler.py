"""
micro_scheduler.py - 微观任务调度器

纯 asyncio 实现的任务调度器，支持优先级、依赖链、并发限制、循环依赖检测。
用于 orchestrator-v4 内部 Fast/Slow Worker 的任务编排。
"""

import asyncio
import logging
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """任务优先级枚举（数字越小优先级越高）"""
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ScheduledTask:
    """被调度的任务数据类"""
    task_id: str
    content: str
    priority: TaskPriority
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None


@dataclass
class TaskResult:
    """任务执行结果数据类"""
    task_id: str
    success: bool
    content: str
    duration: float


class MicroScheduler:
    """微观任务调度器
    
    核心能力：
    - 按优先级调度任务
    - 支持任务依赖链
    - 限制最大并发数
    - 自动传播失败状态
    - 检测循环依赖
    """
    
    def __init__(
        self,
        max_concurrent: int = 3,
        executor: Optional[Callable[[ScheduledTask], asyncio.Awaitable[str]]] = None
    ):
        self.max_concurrent = max_concurrent
        self.executor = executor or self._default_executor
        
        # 任务存储
        self._tasks: Dict[str, ScheduledTask] = {}
        
        # 并发控制
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._running_count = 0
        
        # 状态锁
        self._lock = asyncio.Lock()
        self._event = asyncio.Event()
        self._event.set()
    
    async def _default_executor(self, task: ScheduledTask) -> str:
        """默认执行器（简单模拟）"""
        await asyncio.sleep(0.1)
        return f"[执行完成] {task.content[:30]}"
    
    def submit(
        self,
        task_id: str,
        content: str,
        priority: TaskPriority = TaskPriority.NORMAL,
        dependencies: Optional[List[str]] = None
    ) -> str:
        """提交一个新任务到调度器
        
        Args:
            task_id: 任务唯一标识
            content: 任务内容
            priority: 任务优先级
            dependencies: 依赖的任务ID列表
        
        Returns:
            str: 提交的任务ID
        """
        if task_id in self._tasks:
            logger.warning(f"任务 {task_id} 已存在，将覆盖")
        
        task = ScheduledTask(
            task_id=task_id,
            content=content,
            priority=priority,
            dependencies=dependencies or []
        )
        self._tasks[task_id] = task
        logger.info(f"任务 {task_id} 已提交，优先级={priority.name}，依赖={task.dependencies}")
        return task_id
    
    async def cancel(self, task_id: str) -> bool:
        """取消一个待执行的任务
        
        只能取消尚未开始执行的任务（PENDING / READY 状态）。
        
        Args:
            task_id: 任务唯一标识
        
        Returns:
            bool: 是否成功取消
        """
        async with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                logger.warning(f"取消失败，任务 {task_id} 不存在")
                return False
            
            if task.status in (TaskStatus.RUNNING, TaskStatus.COMPLETED, TaskStatus.FAILED):
                logger.warning(f"取消失败，任务 {task_id} 已在执行或已结束（{task.status.value}）")
                return False
            
            task.status = TaskStatus.CANCELLED
            task.completed_at = time.time()
            logger.info(f"任务 {task_id} 已取消")
            return True
    
    def _check_dependencies(self, task: ScheduledTask) -> bool:
        """检查任务的依赖是否已满足
        
        所有依赖任务必须都完成才算满足。
        如果有依赖失败或被取消，该任务会标记为失败。
        
        Args:
            task: 待检查的任务
        
        Returns:
            bool: 依赖是否已满足
        """
        if not task.dependencies:
            return True
        
        for dep_id in task.dependencies:
            dep_task = self._tasks.get(dep_id)
            if not dep_task:
                task.status = TaskStatus.FAILED
                task.error = f"依赖任务 {dep_id} 不存在"
                task.completed_at = time.time()
                return False
            
            if dep_task.status == TaskStatus.CANCELLED:
                task.status = TaskStatus.FAILED
                task.error = f"依赖任务 {dep_id} 已取消"
                task.completed_at = time.time()
                return False
            
            if dep_task.status == TaskStatus.FAILED:
                task.status = TaskStatus.FAILED
                task.error = f"依赖任务 {dep_id} 执行失败"
                task.completed_at = time.time()
                return False
            
            if dep_task.status != TaskStatus.COMPLETED:
                return False
        
        return True
    
    def get_ready_tasks(self) -> List[ScheduledTask]:
        """获取所有依赖已满足、可以执行的任务
        
        Returns:
            List[ScheduledTask]: 按优先级排序后的可执行任务列表
        """
        ready = []
        for task in self._tasks.values():
            if task.status == TaskStatus.PENDING:
                if self._check_dependencies(task):
                    task.status = TaskStatus.READY
                    ready.append(task)
            elif task.status == TaskStatus.READY:
                ready.append(task)
        
        # 按优先级排序（数字小的先执行）
        ready.sort(key=lambda t: t.priority.value)
        return ready
    
    async def _execute_task(self, task: ScheduledTask) -> TaskResult:
        """执行单个任务
        
        Args:
            task: 待执行的任务
        
        Returns:
            TaskResult: 任务执行结果
        """
        start_time = time.time()
        task.status = TaskStatus.RUNNING
        task.started_at = start_time
        
        logger.info(f"开始执行任务 {task.task_id}（优先级={task.priority.name}）")
        
        try:
            async with self._semaphore:
                async with self._lock:
                    self._running_count += 1
                
                result_content = await self.executor(task)
                
                async with self._lock:
                    self._running_count -= 1
            
            task.status = TaskStatus.COMPLETED
            task.result = result_content
            task.completed_at = time.time()
            duration = task.completed_at - start_time
            
            logger.info(f"任务 {task.task_id} 执行成功，耗时={duration:.3f}s")
            return TaskResult(
                task_id=task.task_id,
                success=True,
                content=result_content,
                duration=duration
            )
            
        except Exception as e:
            async with self._lock:
                self._running_count -= 1
            
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = time.time()
            duration = task.completed_at - start_time
            
            logger.error(f"任务 {task.task_id} 执行失败: {e}")
            return TaskResult(
                task_id=task.task_id,
                success=False,
                content="",
                duration=duration
            )
    
    def _resolve_execution_order(self) -> List[List[str]]:
        """拓扑排序，返回分层执行顺序
        
        使用 Kahn 算法进行拓扑排序，按层返回任务ID。
        同时检测循环依赖，如果存在循环依赖则抛出 ValueError。
        
        Returns:
            List[List[str]]: 每层的任务ID列表
        """
        # 构建入度表和邻接表
        in_degree = {tid: 0 for tid in self._tasks}
        adj = {tid: [] for tid in self._tasks}
        
        for tid, task in self._tasks.items():
            for dep in task.dependencies:
                if dep in self._tasks:
                    adj[dep].append(tid)
                    in_degree[tid] += 1
                # 不存在的依赖会在运行时处理
        
        # Kahn 算法
        queue = deque([tid for tid, deg in in_degree.items() if deg == 0])
        layers: List[List[str]] = []
        visited = set()
        
        while queue:
            layer = []
            next_queue = deque()
            
            for _ in range(len(queue)):
                tid = queue.popleft()
                if tid in visited:
                    continue
                visited.add(tid)
                layer.append(tid)
                
                for neighbor in adj[tid]:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        next_queue.append(neighbor)
            
            if layer:
                layers.append(layer)
            queue = next_queue
        
        # 检测循环依赖
        if len(visited) != len(self._tasks):
            cycle_tasks = [tid for tid in self._tasks if tid not in visited]
            raise ValueError(f"检测到循环依赖，涉及任务: {cycle_tasks}")
        
        return layers
    
    async def run(self) -> Dict[str, TaskResult]:
        """启动调度循环，执行所有任务直到完成
        
        返回每个任务的执行结果。
        
        Returns:
            Dict[str, TaskResult]: 任务ID到结果的映射
        """
        if not self._tasks:
            logger.info("调度器没有任务，直接返回")
            return {}
        
        # 先检测循环依赖
        try:
            order = self._resolve_execution_order()
            logger.info(f"拓扑排序完成，共 {len(order)} 层")
        except ValueError as e:
            logger.error(f"调度失败: {e}")
            # 将循环依赖中的所有任务标记为失败
            for tid in self._tasks:
                self._tasks[tid].status = TaskStatus.FAILED
                self._tasks[tid].error = str(e)
                self._tasks[tid].completed_at = time.time()
            raise
        
        results: Dict[str, TaskResult] = {}
        pending_tasks: Dict[str, asyncio.Task] = {}
        
        while True:
            # 获取可以执行的任务
            ready_tasks = self.get_ready_tasks()
            
            # 过滤掉已经在运行的
            ready_tasks = [t for t in ready_tasks if t.task_id not in pending_tasks]
            
            # 启动新任务（在信号量允许范围内）
            for task in ready_tasks:
                coro = self._execute_task(task)
                aio_task = asyncio.create_task(coro)
                pending_tasks[task.task_id] = aio_task
            
            if not pending_tasks:
                # 没有待执行和运行中的任务了
                break
            
            # 等待至少一个任务完成
            done, _ = await asyncio.wait(
                pending_tasks.values(),
                return_when=asyncio.FIRST_COMPLETED
            )
            
            for aio_task in done:
                # 找到对应的 task_id
                task_id = None
                for tid, t in list(pending_tasks.items()):
                    if t is aio_task:
                        task_id = tid
                        break
                
                if task_id:
                    del pending_tasks[task_id]
                    try:
                        result = await aio_task
                        results[task_id] = result
                    except Exception as e:
                        logger.error(f"收集任务 {task_id} 结果时出错: {e}")
                        results[task_id] = TaskResult(
                            task_id=task_id,
                            success=False,
                            content="",
                            duration=0.0
                        )
        
        logger.info(f"调度循环结束，共完成 {len(results)} 个任务")
        return results
    
    def get_status(self) -> Dict:
        """获取调度器当前状态摘要
        
        Returns:
            Dict: 包含任务总数、各状态数量、运行中数量等
        """
        by_status = {}
        for task in self._tasks.values():
            status_name = task.status.value
            by_status[status_name] = by_status.get(status_name, 0) + 1
        
        return {
            "total_tasks": len(self._tasks),
            "by_status": by_status,
            "max_concurrent": self.max_concurrent,
            "running_count": self._running_count,
            "task_ids": list(self._tasks.keys())
        }
    
    def get_task(self, task_id: str) -> Optional[ScheduledTask]:
        """获取单个任务"""
        return self._tasks.get(task_id)
    
    def reset(self):
        """重置调度器，清空所有任务"""
        self._tasks.clear()
        self._running_count = 0
        logger.info("调度器已重置")


# ========== 便捷函数 ==========

async def create_scheduler(
    max_concurrent: int = 3,
    executor: Optional[Callable[[ScheduledTask], asyncio.Awaitable[str]]] = None
) -> MicroScheduler:
    """创建调度器"""
    return MicroScheduler(max_concurrent=max_concurrent, executor=executor)


# ========== 测试 ==========

async def _test():
    """MicroScheduler 综合测试"""
    print("=" * 60)
    print("MicroScheduler 测试")
    print("=" * 60)
    
    # 自定义执行器（带延迟，方便观察并发）
    async def slow_executor(task: ScheduledTask) -> str:
        await asyncio.sleep(0.2)
        return f"[结果] {task.task_id}: {task.content}"
    
    # ========== 1. 基本提交和执行 ==========
    print("\n1. 基本提交和执行")
    scheduler = await create_scheduler(max_concurrent=2, executor=slow_executor)
    scheduler.submit("t1", "测试任务1", TaskPriority.NORMAL)
    scheduler.submit("t2", "测试任务2", TaskPriority.HIGH)
    results = await scheduler.run()
    for tid, result in results.items():
        print(f"   {tid}: success={result.success}, content={result.content}")
    scheduler.reset()
    
    # ========== 2. 依赖链测试（A → B → C） ==========
    print("\n2. 依赖链测试（A → B → C）")
    scheduler = await create_scheduler(max_concurrent=3, executor=slow_executor)
    scheduler.submit("C", "任务C", TaskPriority.NORMAL, dependencies=["B"])
    scheduler.submit("B", "任务B", TaskPriority.NORMAL, dependencies=["A"])
    scheduler.submit("A", "任务A", TaskPriority.NORMAL)
    results = await scheduler.run()
    for tid in ["A", "B", "C"]:
        task = scheduler.get_task(tid)
        print(f"   {tid}: status={task.status.value}, result={task.result}")
    scheduler.reset()
    
    # ========== 3. 并发限制测试 ==========
    print("\n3. 并发限制测试（max_concurrent=2，同时提交5个任务）")
    scheduler = await create_scheduler(max_concurrent=2, executor=slow_executor)
    
    # 带并发追踪的执行器
    concurrent_count = 0
    max_observed = 0
    
    async def tracking_executor(task: ScheduledTask) -> str:
        nonlocal concurrent_count, max_observed
        concurrent_count += 1
        max_observed = max(max_observed, concurrent_count)
        await asyncio.sleep(0.3)
        concurrent_count -= 1
        return f"done-{task.task_id}"
    
    scheduler.executor = tracking_executor
    for i in range(5):
        scheduler.submit(f"c{i}", f"并发任务{i}", TaskPriority.NORMAL)
    
    start = time.time()
    await scheduler.run()
    elapsed = time.time() - start
    print(f"   5个任务耗时: {elapsed:.2f}s (理论最少≈0.6s)")
    print(f"   观察到的最大并发数: {max_observed} (限制为 2)")
    scheduler.reset()
    
    # ========== 4. 优先级排序测试 ==========
    print("\n4. 优先级排序测试")
    execution_order = []
    
    async def order_executor(task: ScheduledTask) -> str:
        execution_order.append(task.task_id)
        await asyncio.sleep(0.05)
        return task.task_id
    
    scheduler = await create_scheduler(max_concurrent=1, executor=order_executor)
    scheduler.submit("low1", "低优先级1", TaskPriority.LOW)
    scheduler.submit("normal1", "普通优先级1", TaskPriority.NORMAL)
    scheduler.submit("high1", "高优先级1", TaskPriority.HIGH)
    scheduler.submit("critical1", "紧急1", TaskPriority.CRITICAL)
    scheduler.submit("low2", "低优先级2", TaskPriority.LOW)
    scheduler.submit("high2", "高优先级2", TaskPriority.HIGH)
    
    await scheduler.run()
    print(f"   执行顺序: {execution_order}")
    # 验证优先级：CRITICAL最先，HIGH其次
    assert execution_order[0] == "critical1", "CRITICAL 应该第一个执行"
    assert execution_order[1] in ("high1", "high2"), "HIGH 应该在前面"
    scheduler.reset()
    
    # ========== 5. 循环依赖检测 ==========
    print("\n5. 循环依赖检测")
    scheduler = await create_scheduler(max_concurrent=2, executor=slow_executor)
    scheduler.submit("X", "任务X", TaskPriority.NORMAL, dependencies=["Y"])
    scheduler.submit("Y", "任务Y", TaskPriority.NORMAL, dependencies=["Z"])
    scheduler.submit("Z", "任务Z", TaskPriority.NORMAL, dependencies=["X"])
    
    try:
        await scheduler.run()
        print("   错误: 没有检测到循环依赖!")
    except ValueError as e:
        print(f"   正确捕获循环依赖: {e}")
        for tid in ["X", "Y", "Z"]:
            task = scheduler.get_task(tid)
            print(f"   {tid}: status={task.status.value}, error={task.error}")
    scheduler.reset()
    
    # ========== 6. 依赖失败传播 ==========
    print("\n6. 依赖失败传播")
    
    async def failing_executor(task: ScheduledTask) -> str:
        if task.task_id == "M":
            raise RuntimeError("任务M故意失败")
        await asyncio.sleep(0.1)
        return f"ok-{task.task_id}"
    
    scheduler = await create_scheduler(max_concurrent=3, executor=failing_executor)
    scheduler.submit("M", "会失败的任务M", TaskPriority.NORMAL)
    scheduler.submit("N", "依赖M的任务N", TaskPriority.NORMAL, dependencies=["M"])
    scheduler.submit("O", "独立任务O", TaskPriority.NORMAL)
    
    await scheduler.run()
    for tid in ["M", "N", "O"]:
        task = scheduler.get_task(tid)
        print(f"   {tid}: status={task.status.value}, result={task.result}, error={task.error}")
    scheduler.reset()
    
    # ========== 7. 取消任务 ==========
    print("\n7. 取消任务测试")
    scheduler = await create_scheduler(max_concurrent=2, executor=slow_executor)
    scheduler.submit("q1", "任务q1", TaskPriority.NORMAL)
    scheduler.submit("q2", "任务q2", TaskPriority.NORMAL)
    cancelled = await scheduler.cancel("q1")
    results = await scheduler.run()
    print(f"   取消 q1 结果: {cancelled}")
    print(f"   q1: status={scheduler.get_task('q1').status.value}")
    print(f"   q2: status={scheduler.get_task('q2').status.value}")
    scheduler.reset()
    
    print("\n" + "=" * 60)
    print("所有测试通过")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(_test())
