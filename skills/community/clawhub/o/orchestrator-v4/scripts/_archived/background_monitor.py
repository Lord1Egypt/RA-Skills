"""
background_monitor.py - 子 Agent 健康状态监控模块

核心设计：
- 纯 asyncio 实现，无外部依赖
- 监控通过 sessions_spawn 创建的子 agent
- 支持心跳检测、超时回调、状态查询
"""

import asyncio
import time
import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Callable, Any, Set


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BackgroundMonitor")


class ProcessStatus(Enum):
    """Agent 运行状态枚举"""
    RUNNING = auto()      # 运行中
    COMPLETED = auto()    # 正常完成
    FAILED = auto()       # 执行失败
    TIMEOUT = auto()      # 超时
    UNKNOWN = auto()      # 未知状态


@dataclass
class MonitoredAgent:
    """被监控的 Agent 信息"""
    task_id: str                          # 任务唯一标识
    session_key: str                      # 会话密钥（用于追踪）
    registered_at: float                  # 注册时间戳
    last_heartbeat: float                 # 最后心跳时间
    status: ProcessStatus                 # 当前状态
    timeout: float                        # 超时阈值（秒）
    metadata: Dict[str, Any] = field(default_factory=dict)  # 额外元数据


@dataclass
class UnhealthyAgent:
    """不健康的 Agent 信息"""
    task_id: str
    session_key: str
    status: ProcessStatus
    last_heartbeat: float
    elapsed_since_heartbeat: float
    reason: str


@dataclass
class MonitorSummary:
    """监控摘要"""
    total_agents: int
    running: int
    completed: int
    failed: int
    timeout: int
    unknown: int
    unhealthy_count: int
    check_interval: float
    uptime: float


class BackgroundMonitor:
    """后台监控器 - 管理子 Agent 健康状态"""
    
    def __init__(self, check_interval: float = 5.0):
        """
        初始化监控器
        
        Args:
            check_interval: 健康检查间隔（秒），默认 5 秒
        """
        self.check_interval = check_interval
        self._agents: Dict[str, MonitoredAgent] = {}
        self._monitor_task: Optional[asyncio.Task] = None
        self._shutdown = False
        self._started_at: Optional[float] = None
        
        # 回调函数
        self._timeout_callbacks: List[Callable[[MonitoredAgent], None]] = []
        self._failure_callbacks: List[Callable[[MonitoredAgent], None]] = []
        
        # 锁，用于线程安全
        self._lock = asyncio.Lock()
    
    async def start(self):
        """启动监控循环"""
        if self._monitor_task is not None:
            logger.warning("监控器已在运行中")
            return
        
        self._shutdown = False
        self._started_at = time.time()
        self._monitor_task = asyncio.create_task(self._monitor_loop())
        logger.info(f"后台监控器已启动，检查间隔: {self.check_interval}秒")
    
    async def stop(self):
        """停止监控循环"""
        self._shutdown = True
        
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
            self._monitor_task = None
        
        logger.info("后台监控器已停止")
    
    async def register(
        self, 
        task_id: str, 
        session_key: str, 
        timeout: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> MonitoredAgent:
        """
        注册需要监控的子 Agent
        
        Args:
            task_id: 任务唯一标识
            session_key: 会话密钥
            timeout: 超时阈值（秒），超过此时间未收到心跳则判定为超时
            metadata: 可选的元数据字典
        
        Returns:
            MonitoredAgent: 创建的监控对象
        """
        now = time.time()
        agent = MonitoredAgent(
            task_id=task_id,
            session_key=session_key,
            registered_at=now,
            last_heartbeat=now,
            status=ProcessStatus.RUNNING,
            timeout=timeout,
            metadata=metadata or {}
        )
        
        async with self._lock:
            self._agents[task_id] = agent
        
        logger.info(f"Agent 已注册: task_id={task_id}, session_key={session_key}, timeout={timeout}s")
        return agent
    
    async def unregister(self, task_id: str) -> bool:
        """
        取消对指定 Agent 的监控
        
        Args:
            task_id: 任务唯一标识
        
        Returns:
            bool: 是否成功移除
        """
        async with self._lock:
            if task_id in self._agents:
                del self._agents[task_id]
                logger.info(f"Agent 已注销: task_id={task_id}")
                return True
        
        logger.warning(f"尝试注销不存在的 Agent: task_id={task_id}")
        return False
    
    async def heartbeat(self, task_id: str) -> bool:
        """
        记录心跳（子 Agent 报告自己还活着）
        
        Args:
            task_id: 任务唯一标识
        
        Returns:
            bool: 是否成功更新心跳
        """
        async with self._lock:
            if task_id not in self._agents:
                logger.warning(f"收到未知 Agent 的心跳: task_id={task_id}")
                return False
            
            agent = self._agents[task_id]
            agent.last_heartbeat = time.time()
            
            # 如果之前是超时或未知状态，恢复为运行中
            if agent.status in (ProcessStatus.TIMEOUT, ProcessStatus.UNKNOWN):
                agent.status = ProcessStatus.RUNNING
                logger.info(f"Agent 状态恢复为 RUNNING: task_id={task_id}")
            
            logger.debug(f"Agent 心跳更新: task_id={task_id}")
            return True
    
    async def mark_done(self, task_id: str, success: bool) -> bool:
        """
        标记 Agent 任务完成
        
        Args:
            task_id: 任务唯一标识
            success: 是否成功完成
        
        Returns:
            bool: 是否成功标记
        """
        async with self._lock:
            if task_id not in self._agents:
                logger.warning(f"尝试标记不存在的 Agent: task_id={task_id}")
                return False
            
            agent = self._agents[task_id]
            agent.status = ProcessStatus.COMPLETED if success else ProcessStatus.FAILED
            
            status_str = "成功" if success else "失败"
            logger.info(f"Agent 任务已标记为完成({status_str}): task_id={task_id}")
            
            # 如果失败，触发失败回调
            if not success:
                for callback in self._failure_callbacks:
                    try:
                        callback(agent)
                    except Exception as e:
                        logger.error(f"失败回调执行异常: {e}")
            
            return True
    
    async def check_health(self) -> List[UnhealthyAgent]:
        """
        检查所有 Agent 的健康状态
        
        Returns:
            List[UnhealthyAgent]: 不健康的 Agent 列表
        """
        unhealthy: List[UnhealthyAgent] = []
        now = time.time()
        
        async with self._lock:
            for agent in self._agents.values():
                # 跳过已完成的
                if agent.status in (ProcessStatus.COMPLETED, ProcessStatus.FAILED):
                    continue
                
                elapsed = now - agent.last_heartbeat
                
                # 检查是否超时
                if elapsed > agent.timeout:
                    unhealthy.append(UnhealthyAgent(
                        task_id=agent.task_id,
                        session_key=agent.session_key,
                        status=ProcessStatus.TIMEOUT,
                        last_heartbeat=agent.last_heartbeat,
                        elapsed_since_heartbeat=elapsed,
                        reason=f"超过 {agent.timeout} 秒未收到心跳"
                    ))
                # 检查是否长时间无心跳（超过 2 倍检查间隔）
                elif elapsed > self.check_interval * 2 and agent.status == ProcessStatus.RUNNING:
                    unhealthy.append(UnhealthyAgent(
                        task_id=agent.task_id,
                        session_key=agent.session_key,
                        status=ProcessStatus.UNKNOWN,
                        last_heartbeat=agent.last_heartbeat,
                        elapsed_since_heartbeat=elapsed,
                        reason=f"超过 {self.check_interval * 2} 秒无心跳，状态未知"
                    ))
        
        return unhealthy
    
    async def poke(self, task_id: Optional[str] = None) -> Dict[str, Any]:
        """
        "拍一拍"查状态 - 查询指定或所有 Agent 的状态
        
        Args:
            task_id: 可选，指定任务 ID；为 None 时返回所有 Agent 状态
        
        Returns:
            Dict: 状态信息字典
        """
        now = time.time()
        
        async with self._lock:
            if task_id:
                # 查询单个 Agent
                if task_id not in self._agents:
                    return {
                        "found": False,
                        "task_id": task_id,
                        "message": "Agent 不存在"
                    }
                
                agent = self._agents[task_id]
                return {
                    "found": True,
                    "task_id": agent.task_id,
                    "session_key": agent.session_key,
                    "status": agent.status.name,
                    "registered_at": agent.registered_at,
                    "last_heartbeat": agent.last_heartbeat,
                    "elapsed_since_heartbeat": now - agent.last_heartbeat,
                    "timeout": agent.timeout,
                    "metadata": agent.metadata
                }
            else:
                # 查询所有 Agent
                agents_info = []
                for agent in self._agents.values():
                    agents_info.append({
                        "task_id": agent.task_id,
                        "session_key": agent.session_key,
                        "status": agent.status.name,
                        "elapsed_since_heartbeat": now - agent.last_heartbeat,
                        "timeout": agent.timeout
                    })
                
                return {
                    "total": len(agents_info),
                    "agents": agents_info
                }
    
    def on_timeout(self, callback: Callable[[MonitoredAgent], None]):
        """
        注册超时回调函数
        
        Args:
            callback: 回调函数，接收 MonitoredAgent 参数
        """
        self._timeout_callbacks.append(callback)
        logger.debug(f"已注册超时回调，当前共 {len(self._timeout_callbacks)} 个")
    
    def on_failure(self, callback: Callable[[MonitoredAgent], None]):
        """
        注册失败回调函数
        
        Args:
            callback: 回调函数，接收 MonitoredAgent 参数
        """
        self._failure_callbacks.append(callback)
        logger.debug(f"已注册失败回调，当前共 {len(self._failure_callbacks)} 个")
    
    async def get_summary(self) -> MonitorSummary:
        """
        获取监控摘要
        
        Returns:
            MonitorSummary: 监控摘要对象
        """
        counts = {status: 0 for status in ProcessStatus}
        
        async with self._lock:
            for agent in self._agents.values():
                counts[agent.status] += 1
        
        unhealthy = await self.check_health()
        uptime = time.time() - self._started_at if self._started_at else 0
        
        return MonitorSummary(
            total_agents=len(self._agents),
            running=counts[ProcessStatus.RUNNING],
            completed=counts[ProcessStatus.COMPLETED],
            failed=counts[ProcessStatus.FAILED],
            timeout=counts[ProcessStatus.TIMEOUT],
            unknown=counts[ProcessStatus.UNKNOWN],
            unhealthy_count=len(unhealthy),
            check_interval=self.check_interval,
            uptime=uptime
        )
    
    async def _monitor_loop(self):
        """监控循环 - 定期检查 Agent 健康状态"""
        while not self._shutdown:
            try:
                await self._check_and_handle_timeouts()
                await asyncio.sleep(self.check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"监控循环异常: {e}")
                await asyncio.sleep(self.check_interval)
    
    async def _check_and_handle_timeouts(self):
        """检查并处理超时"""
        now = time.time()
        timed_out_agents: List[MonitoredAgent] = []
        
        async with self._lock:
            for agent in self._agents.values():
                # 只检查运行中的 Agent
                if agent.status != ProcessStatus.RUNNING:
                    continue
                
                elapsed = now - agent.last_heartbeat
                
                # 检查是否超时
                if elapsed > agent.timeout:
                    agent.status = ProcessStatus.TIMEOUT
                    timed_out_agents.append(agent)
                    logger.warning(
                        f"Agent 超时: task_id={agent.task_id}, "
                        f"elapsed={elapsed:.1f}s, timeout={agent.timeout}s"
                    )
        
        # 触发超时回调（在锁外执行）
        for agent in timed_out_agents:
            for callback in self._timeout_callbacks:
                try:
                    callback(agent)
                except Exception as e:
                    logger.error(f"超时回调执行异常: {e}")


# ========== 便捷入口 ==========

async def create_monitor(check_interval: float = 5.0) -> BackgroundMonitor:
    """创建并启动监控器"""
    monitor = BackgroundMonitor(check_interval=check_interval)
    await monitor.start()
    return monitor


# ========== 测试入口 ==========

async def _test():
    """简单的测试用例"""
    print("=" * 50)
    print("BackgroundMonitor 测试")
    print("=" * 50)
    
    # 创建监控器
    monitor = BackgroundMonitor(check_interval=2.0)
    await monitor.start()
    
    # 注册回调
    def on_timeout_callback(agent: MonitoredAgent):
        print(f"[回调] Agent 超时: {agent.task_id}")
    
    def on_failure_callback(agent: MonitoredAgent):
        print(f"[回调] Agent 失败: {agent.task_id}")
    
    monitor.on_timeout(on_timeout_callback)
    monitor.on_failure(on_failure_callback)
    
    # 注册几个 Agent
    await monitor.register("task-001", "session-key-001", timeout=3.0, metadata={"type": "slow"})
    await monitor.register("task-002", "session-key-002", timeout=5.0, metadata={"type": "fast"})
    await monitor.register("task-003", "session-key-003", timeout=10.0, metadata={"type": "slow"})
    
    print("\n--- 初始状态 ---")
    summary = await monitor.get_summary()
    print(f"总 Agent 数: {summary.total_agents}")
    print(f"运行中: {summary.running}")
    
    # 模拟 task-001 的心跳
    print("\n--- task-001 发送心跳 ---")
    await monitor.heartbeat("task-001")
    
    # 模拟 task-002 完成
    print("\n--- task-002 标记完成 ---")
    await monitor.mark_done("task-002", success=True)
    
    # 等待一段时间，让 task-001 超时
    print("\n--- 等待 4 秒（task-001 应该超时）---")
    await asyncio.sleep(4)
    
    # 检查健康状态
    print("\n--- 健康检查结果 ---")
    unhealthy = await monitor.check_health()
    for u in unhealthy:
        print(f"  不健康: {u.task_id}, 状态: {u.status.name}, 原因: {u.reason}")
    
    # 拍一拍查询
    print("\n--- 拍一拍查询 ---")
    poke_result = await monitor.poke("task-001")
    print(f"task-001 状态: {poke_result.get('status')}")
    
    all_status = await monitor.poke()
    print(f"所有 Agent: {all_status.get('total')} 个")
    for info in all_status.get('agents', []):
        print(f"  - {info['task_id']}: {info['status']}")
    
    # 最终摘要
    print("\n--- 最终监控摘要 ---")
    summary = await monitor.get_summary()
    print(f"总 Agent 数: {summary.total_agents}")
    print(f"运行中: {summary.running}")
    print(f"已完成: {summary.completed}")
    print(f"超时: {summary.timeout}")
    print(f"不健康: {summary.unhealthy_count}")
    print(f"运行时间: {summary.uptime:.1f}秒")
    
    # 停止监控器
    await monitor.stop()
    print("\n测试完成！")


if __name__ == "__main__":
    asyncio.run(_test())
