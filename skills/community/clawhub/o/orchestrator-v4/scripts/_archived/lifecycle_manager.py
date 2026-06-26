"""
lifecycle_manager.py - 子 Agent 生命周期管理器

管理通过 sessions_spawn 创建的子 agent 生命周期，支持重启策略和指数退避。
"""

import asyncio
import time
import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Optional, Set


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RestartPolicy(Enum):
    """重启策略枚举"""
    NEVER = auto()       # 永不重启
    ON_FAILURE = auto()  # 失败时重启
    ALWAYS = auto()      # 总是重启


class ProcessStatus(Enum):
    """进程状态枚举"""
    PENDING = auto()     # 待启动
    RUNNING = auto()     # 运行中
    COMPLETED = auto()   # 已完成（成功）
    FAILED = auto()      # 已失败
    RESTARTING = auto()  # 重启中
    TERMINATED = auto()  # 已终止


@dataclass
class ManagedProcess:
    """被管理的进程数据类"""
    task_id: str
    session_key: str
    started_at: float = field(default_factory=time.time)
    status: ProcessStatus = ProcessStatus.PENDING
    restart_count: int = 0
    last_error: Optional[str] = None
    completed_at: Optional[float] = None
    restart_policy: RestartPolicy = RestartPolicy.ON_FAILURE
    # 重启窗口配置
    max_restarts: int = 3           # 窗口内最大重启次数
    restart_window_sec: float = 60.0  # 重启窗口（秒）
    _restart_history: list = field(default_factory=list)  # 重启时间戳历史

    def __post_init__(self):
        """初始化后处理"""
        if self.status == ProcessStatus.PENDING:
            self.status = ProcessStatus.RUNNING


class ProcessLifecycleManager:
    """进程生命周期管理器
    
    管理子 agent 的完整生命周期，包括注册、状态跟踪、失败重启等。
    支持指数退避策略和重启窗口限制。
    """
    
    def __init__(
        self,
        default_restart_policy: RestartPolicy = RestartPolicy.ON_FAILURE,
        default_max_restarts: int = 3,
        default_restart_window_sec: float = 60.0,
        base_delay: float = 1.0,      # 基础延迟（秒）
        max_delay: float = 60.0       # 最大延迟（秒）
    ):
        self._processes: Dict[str, ManagedProcess] = {}
        self._default_restart_policy = default_restart_policy
        self._default_max_restarts = default_max_restarts
        self._default_restart_window_sec = default_restart_window_sec
        self._base_delay = base_delay
        self._max_delay = max_delay
        self._lock = asyncio.Lock()
    
    async def register(
        self,
        task_id: str,
        session_key: str,
        restart_policy: Optional[RestartPolicy] = None,
        max_restarts: Optional[int] = None,
        restart_window_sec: Optional[float] = None
    ) -> ManagedProcess:
        """注册一个新的子 agent
        
        Args:
            task_id: 任务唯一标识
            session_key: 会话密钥（来自 sessions_spawn）
            restart_policy: 重启策略（默认 ON_FAILURE）
            max_restarts: 窗口内最大重启次数
            restart_window_sec: 重启窗口（秒）
        
        Returns:
            ManagedProcess: 创建的进程对象
        """
        async with self._lock:
            if task_id in self._processes:
                logger.warning(f"任务 {task_id} 已存在，将覆盖")
            
            process = ManagedProcess(
                task_id=task_id,
                session_key=session_key,
                restart_policy=restart_policy or self._default_restart_policy,
                max_restarts=max_restarts or self._default_max_restarts,
                restart_window_sec=restart_window_sec or self._default_restart_window_sec
            )
            self._processes[task_id] = process
            logger.info(f"任务 {task_id} 已注册，session_key={session_key}")
            return process
    
    async def unregister(self, task_id: str) -> bool:
        """取消注册一个子 agent
        
        Args:
            task_id: 任务唯一标识
        
        Returns:
            bool: 是否成功移除
        """
        async with self._lock:
            if task_id in self._processes:
                del self._processes[task_id]
                logger.info(f"任务 {task_id} 已取消注册")
                return True
            logger.warning(f"尝试取消注册不存在的任务 {task_id}")
            return False
    
    async def mark_completed(self, task_id: str, success: bool = True):
        """标记任务完成
        
        Args:
            task_id: 任务唯一标识
            success: 是否成功完成
        """
        async with self._lock:
            process = self._processes.get(task_id)
            if not process:
                logger.warning(f"标记完成时未找到任务 {task_id}")
                return
            
            process.completed_at = time.time()
            if success:
                process.status = ProcessStatus.COMPLETED
                logger.info(f"任务 {task_id} 标记为完成（成功）")
            else:
                process.status = ProcessStatus.FAILED
                logger.info(f"任务 {task_id} 标记为完成（失败）")
    
    async def mark_failed(self, task_id: str, error: str):
        """标记任务失败
        
        Args:
            task_id: 任务唯一标识
            error: 错误信息
        """
        async with self._lock:
            process = self._processes.get(task_id)
            if not process:
                logger.warning(f"标记失败时未找到任务 {task_id}")
                return
            
            process.status = ProcessStatus.FAILED
            process.last_error = error
            process.completed_at = time.time()
            logger.error(f"任务 {task_id} 失败: {error}")
    
    def should_restart(self, task_id: str) -> bool:
        """判断任务是否需要重启
        
        根据重启策略和重启窗口内的次数判断是否允许重启。
        
        Args:
            task_id: 任务唯一标识
        
        Returns:
            bool: 是否需要重启
        """
        process = self._processes.get(task_id)
        if not process:
            return False
        
        # 检查重启策略
        if process.restart_policy == RestartPolicy.NEVER:
            return False
        
        if process.restart_policy == RestartPolicy.ON_FAILURE:
            if process.status != ProcessStatus.FAILED:
                return False
        
        # 检查重启窗口内的次数
        now = time.time()
        window_start = now - process.restart_window_sec
        
        # 清理窗口外的重启记录
        process._restart_history = [
            ts for ts in process._restart_history if ts > window_start
        ]
        
        # 检查是否超过最大重启次数
        if len(process._restart_history) >= process.max_restarts:
            logger.warning(
                f"任务 {task_id} 在 {process.restart_window_sec} 秒内 "
                f"已重启 {len(process._restart_history)} 次，超过限制"
            )
            return False
        
        return True
    
    def get_restart_delay(self, task_id: str) -> float:
        """获取重启延迟时间（指数退避）
        
        延迟计算公式：base_delay * (2 ^ restart_count)
        但不超过 max_delay
        
        Args:
            task_id: 任务唯一标识
        
        Returns:
            float: 延迟秒数
        """
        process = self._processes.get(task_id)
        if not process:
            return self._base_delay
        
        # 指数退避：1s, 2s, 4s, 8s...
        delay = self._base_delay * (2 ** process.restart_count)
        return min(delay, self._max_delay)
    
    async def record_restart(self, task_id: str) -> bool:
        """记录一次重启
        
        Args:
            task_id: 任务唯一标识
        
        Returns:
            bool: 是否成功记录
        """
        async with self._lock:
            process = self._processes.get(task_id)
            if not process:
                logger.warning(f"记录重启时未找到任务 {task_id}")
                return False
            
            process.restart_count += 1
            process._restart_history.append(time.time())
            process.status = ProcessStatus.RESTARTING
            logger.info(f"任务 {task_id} 第 {process.restart_count} 次重启已记录")
            return True
    
    def get_status(self, task_id: str) -> Optional[ManagedProcess]:
        """获取任务状态
        
        Args:
            task_id: 任务唯一标识
        
        Returns:
            ManagedProcess: 进程对象，不存在则返回 None
        """
        return self._processes.get(task_id)
    
    def get_all(self) -> Dict[str, ManagedProcess]:
        """获取所有管理的进程
        
        Returns:
            Dict[str, ManagedProcess]: 任务ID到进程对象的映射
        """
        return self._processes.copy()
    
    async def cleanup_stale(self, max_age: float):
        """清理过期记录
        
        清理已完成/失败/终止且超过 max_age 秒的记录。
        
        Args:
            max_age: 最大存活时间（秒）
        """
        async with self._lock:
            now = time.time()
            to_remove: Set[str] = set()
            
            for task_id, process in self._processes.items():
                # 检查是否处于终止状态
                if process.status in (
                    ProcessStatus.COMPLETED,
                    ProcessStatus.FAILED,
                    ProcessStatus.TERMINATED
                ):
                    # 检查是否过期
                    if process.completed_at and (now - process.completed_at) > max_age:
                        to_remove.add(task_id)
            
            for task_id in to_remove:
                del self._processes[task_id]
                logger.info(f"过期任务 {task_id} 已清理")
            
            if to_remove:
                logger.info(f"共清理 {len(to_remove)} 个过期任务")
    
    def get_stats(self) -> Dict:
        """获取管理器统计信息
        
        Returns:
            Dict: 统计信息
        """
        total = len(self._processes)
        by_status = {}
        
        for process in self._processes.values():
            status_name = process.status.name
            by_status[status_name] = by_status.get(status_name, 0) + 1
        
        return {
            "total_processes": total,
            "by_status": by_status,
            "default_restart_policy": self._default_restart_policy.name,
            "default_max_restarts": self._default_max_restarts,
            "default_restart_window_sec": self._default_restart_window_sec
        }


# ========== 便捷函数 ==========

async def create_lifecycle_manager(**kwargs) -> ProcessLifecycleManager:
    """创建生命周期管理器"""
    return ProcessLifecycleManager(**kwargs)


# ========== 测试 ==========

async def _test():
    """简单测试"""
    print("=" * 50)
    print("ProcessLifecycleManager 测试")
    print("=" * 50)
    
    # 创建管理器
    manager = await create_lifecycle_manager(
        default_restart_policy=RestartPolicy.ON_FAILURE,
        default_max_restarts=3,
        base_delay=1.0,
        max_delay=30.0
    )
    
    # 测试注册
    print("\n1. 测试注册")
    process = await manager.register("task-001", "session-key-001")
    print(f"   注册成功: {process.task_id}, status={process.status.name}")
    
    # 测试获取状态
    print("\n2. 测试获取状态")
    status = manager.get_status("task-001")
    print(f"   状态: {status.status.name if status else 'None'}")
    
    # 测试标记完成
    print("\n3. 测试标记完成")
    await manager.mark_completed("task-001", success=True)
    status = manager.get_status("task-001")
    print(f"   完成后状态: {status.status.name if status else 'None'}")
    
    # 测试重启策略 - ON_FAILURE 策略下已完成任务不应重启
    print("\n4. 测试重启策略（ON_FAILURE + 已完成）")
    should_restart = manager.should_restart("task-001")
    print(f"   是否需要重启: {should_restart} (应为 False)")
    
    # 注册新任务并标记失败
    print("\n5. 测试失败重启")
    await manager.register("task-002", "session-key-002")
    await manager.mark_failed("task-002", "连接超时")
    should_restart = manager.should_restart("task-002")
    print(f"   失败后是否需要重启: {should_restart} (应为 True)")
    
    # 测试指数退避
    print("\n6. 测试指数退避延迟")
    for i in range(5):
        delay = manager.get_restart_delay("task-002")
        print(f"   第 {i} 次重启延迟: {delay}s")
        await manager.record_restart("task-002")
    
    # 测试重启次数限制
    print("\n7. 测试重启次数限制")
    await manager.register("task-003", "session-key-003")
    await manager.mark_failed("task-003", "错误")
    for i in range(5):
        if manager.should_restart("task-003"):
            await manager.record_restart("task-003")
            print(f"   第 {i+1} 次重启允许")
        else:
            print(f"   第 {i+1} 次重启被拒绝（已达上限）")
            break
    
    # 测试获取全部
    print("\n8. 测试获取全部任务")
    all_processes = manager.get_all()
    print(f"   总任务数: {len(all_processes)}")
    for tid, proc in all_processes.items():
        print(f"   - {tid}: {proc.status.name}, restarts={proc.restart_count}")
    
    # 测试统计
    print("\n9. 测试统计信息")
    stats = manager.get_stats()
    print(f"   {stats}")
    
    # 测试清理
    print("\n10. 测试清理过期记录")
    await manager.cleanup_stale(max_age=0)  # 立即清理
    all_processes = manager.get_all()
    print(f"    清理后任务数: {len(all_processes)}")
    
    # 测试取消注册
    print("\n11. 测试取消注册")
    await manager.register("task-004", "session-key-004")
    result = await manager.unregister("task-004")
    print(f"    取消注册结果: {result}")
    result = await manager.unregister("task-004")
    print(f"    重复取消注册结果: {result}")
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(_test())
