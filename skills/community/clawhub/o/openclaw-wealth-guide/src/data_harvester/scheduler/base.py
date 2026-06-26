"""
调度器基类模块
提供任务调度功能
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import time
import threading
from concurrent.futures import ThreadPoolExecutor, Future

from ..exceptions import SchedulerError
from ..config import SchedulerConfig

logger = logging.getLogger(__name__)


@dataclass
class ScheduledTask:
    """计划任务数据类"""
    task_id: str
    name: str
    func: Callable
    args: tuple
    kwargs: Dict[str, Any]
    schedule: str  # Cron表达式
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    run_count: int = 0
    success_count: int = 0
    error_count: int = 0
    last_error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "task_id": self.task_id,
            "name": self.name,
            "schedule": self.schedule,
            "enabled": self.enabled,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "run_count": self.run_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "success_rate": f"{(self.success_count / self.run_count * 100):.1f}%" if self.run_count > 0 else "0%",
            "last_error": self.last_error,
            "created_at": self.created_at.isoformat()
        }


class Scheduler(ABC):
    """调度器基类"""
    
    def __init__(self, config: SchedulerConfig):
        """
        初始化调度器
        
        Args:
            config: 调度器配置
        """
        self.config = config
        self.tasks: Dict[str, ScheduledTask] = {}
        self.running = False
        self._executor: Optional[ThreadPoolExecutor] = None
        self._lock = threading.RLock()
        self._task_counter = 0
        
        # 统计信息
        self.stats = {
            "total_tasks": 0,
            "active_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "total_execution_time": 0.0,
            "start_time": None,
            "uptime": 0
        }
        
        logger.debug(f"初始化调度器，配置: {config}")
    
    def start(self) -> None:
        """
        启动调度器
        
        Raises:
            SchedulerError: 启动失败
        """
        with self._lock:
            if self.running:
                logger.warning("调度器已经在运行")
                return
            
            try:
                # 创建线程池
                self._executor = ThreadPoolExecutor(
                    max_workers=self.config.max_workers,
                    thread_name_prefix="scheduler_worker"
                )
                
                # 启动调度循环
                self.running = True
                self.stats["start_time"] = datetime.now()
                
                # 启动监控线程
                monitor_thread = threading.Thread(
                    target=self._monitor_loop,
                    name="scheduler_monitor",
                    daemon=True
                )
                monitor_thread.start()
                
                logger.info(f"调度器启动成功，工作线程数: {self.config.max_workers}")
                
            except Exception as e:
                logger.error(f"调度器启动失败: {e}")
                self.running = False
                raise SchedulerError(f"调度器启动失败: {e}") from e
    
    def shutdown(self, wait: bool = True) -> None:
        """
        关闭调度器
        
        Args:
            wait: 是否等待正在执行的任务完成
        """
        with self._lock:
            if not self.running:
                logger.warning("调度器已经停止")
                return
            
            self.running = False
            
            if self._executor:
                self._executor.shutdown(wait=wait)
                self._executor = None
            
            logger.info("调度器已关闭")
    
    def add_task(self, func: Callable, schedule: str, name: Optional[str] = None,
                args: tuple = (), kwargs: Optional[Dict[str, Any]] = None) -> str:
        """
        添加计划任务
        
        Args:
            func: 要执行的函数
            schedule: 调度表达式（Cron格式）
            name: 任务名称（可选）
            args: 函数位置参数
            kwargs: 函数关键字参数
            
        Returns:
            str: 任务ID
            
        Raises:
            SchedulerError: 添加任务失败
        """
        with self._lock:
            try:
                # 验证Cron表达式
                if not self._validate_cron(schedule):
                    raise ValueError(f"无效的Cron表达式: {schedule}")
                
                # 生成任务ID
                self._task_counter += 1
                task_id = f"task_{self._task_counter:04d}"
                
                # 确定任务名称
                task_name = name or f"Task_{self._task_counter}"
                
                # 计算下次运行时间
                next_run = self._calculate_next_run(schedule)
                
                # 创建任务对象
                task = ScheduledTask(
                    task_id=task_id,
                    name=task_name,
                    func=func,
                    args=args or (),
                    kwargs=kwargs or {},
                    schedule=schedule,
                    next_run=next_run
                )
                
                # 保存任务
                self.tasks[task_id] = task
                self.stats["total_tasks"] += 1
                self.stats["active_tasks"] += 1
                
                logger.info(f"添加计划任务: {task_name} (ID: {task_id}), 调度: {schedule}")
                
                return task_id
                
            except Exception as e:
                logger.error(f"添加计划任务失败: {e}")
                raise SchedulerError(f"添加计划任务失败: {e}") from e
    
    def remove_task(self, task_id: str) -> bool:
        """
        移除计划任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否成功移除
        """
        with self._lock:
            if task_id not in self.tasks:
                logger.warning(f"任务不存在: {task_id}")
                return False
            
            task = self.tasks[task_id]
            del self.tasks[task_id]
            
            self.stats["active_tasks"] -= 1
            
            logger.info(f"移除计划任务: {task.name} (ID: {task_id})")
            return True
    
    def enable_task(self, task_id: str) -> bool:
        """
        启用任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否成功启用
        """
        with self._lock:
            if task_id not in self.tasks:
                logger.warning(f"任务不存在: {task_id}")
                return False
            
            task = self.tasks[task_id]
            task.enabled = True
            
            logger.debug(f"启用任务: {task.name} (ID: {task_id})")
            return True
    
    def disable_task(self, task_id: str) -> bool:
        """
        禁用任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否成功禁用
        """
        with self._lock:
            if task_id not in self.tasks:
                logger.warning(f"任务不存在: {task_id}")
                return False
            
            task = self.tasks[task_id]
            task.enabled = False
            
            logger.debug(f"禁用任务: {task.name} (ID: {task_id})")
            return True
    
    def get_task(self, task_id: str) -> Optional[ScheduledTask]:
        """
        获取任务信息
        
        Args:
            task_id: 任务ID
            
        Returns:
            ScheduledTask: 任务信息，如果不存在则返回None
        """
        with self._lock:
            return self.tasks.get(task_id)
    
    def list_tasks(self, enabled_only: bool = False) -> List[Dict[str, Any]]:
        """
        列出所有任务
        
        Args:
            enabled_only: 是否只列出启用的任务
            
        Returns:
            任务信息列表
        """
        with self._lock:
            tasks = []
            for task in self.tasks.values():
                if enabled_only and not task.enabled:
                    continue
                tasks.append(task.to_dict())
            return tasks
    
    def run_task_now(self, task_id: str) -> bool:
        """
        立即运行任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否成功提交执行
        """
        with self._lock:
            if task_id not in self.tasks:
                logger.warning(f"任务不存在: {task_id}")
                return False
            
            task = self.tasks[task_id]
            
            if not task.enabled:
                logger.warning(f"任务已禁用: {task.name}")
                return False
            
            # 提交任务执行
            try:
                self._submit_task(task)
                logger.info(f"立即运行任务: {task.name} (ID: {task_id})")
                return True
                
            except Exception as e:
                logger.error(f"提交任务执行失败: {e}")
                return False
    
    def get_stats(self) -> Dict[str, Any]:
        """获取调度器统计信息"""
        with self._lock:
            stats = self.stats.copy()
            
            # 计算运行时间
            if stats["start_time"]:
                stats["uptime"] = (datetime.now() - stats["start_time"]).total_seconds()
            
            # 添加任务统计
            task_stats = {
                "total": len(self.tasks),
                "enabled": sum(1 for t in self.tasks.values() if t.enabled),
                "disabled": sum(1 for t in self.tasks.values() if not t.enabled),
                "by_status": {
                    "pending": sum(1 for t in self.tasks.values() if t.run_count == 0),
                    "running": 0,  # 需要跟踪正在运行的任务
                    "completed": sum(1 for t in self.tasks.values() if t.run_count > 0),
                }
            }
            
            stats["task_stats"] = task_stats
            stats["running"] = self.running
            stats["config"] = self.config.dict() if hasattr(self.config, "dict") else vars(self.config)
            
            return stats
    
    @abstractmethod
    def _validate_cron(self, cron_expr: str) -> bool:
        """
        验证Cron表达式
        
        Args:
            cron_expr: Cron表达式
            
        Returns:
            bool: 表达式是否有效
        """
        pass
    
    @abstractmethod
    def _calculate_next_run(self, cron_expr: str) -> datetime:
        """
        计算下次运行时间
        
        Args:
            cron_expr: Cron表达式
            
        Returns:
            datetime: 下次运行时间
        """
        pass
    
    def _monitor_loop(self) -> None:
        """监控循环，检查并执行到期的任务"""
        logger.info("调度器监控循环启动")
        
        try:
            while self.running:
                with self._lock:
                    current_time = datetime.now()
                    
                    # 检查每个任务是否需要执行
                    for task in self.tasks.values():
                        if not task.enabled:
                            continue
                        
                        if task.next_run and current_time >= task.next_run:
                            # 提交任务执行
                            self._submit_task(task)
                            
                            # 更新下次运行时间
                            task.next_run = self._calculate_next_run(task.schedule)
                
                # 等待一段时间再检查
                time.sleep(1)  # 每秒检查一次
                
        except Exception as e:
            logger.error(f"调度器监控循环异常: {e}")
        finally:
            logger.info("调度器监控循环结束")
    
    def _submit_task(self, task: ScheduledTask) -> Future:
        """
        提交任务执行
        
        Args:
            task: 要执行的任务
            
        Returns:
            Future: 执行结果Future
            
        Raises:
            SchedulerError: 提交失败
        """
        if not self._executor:
            raise SchedulerError("调度器未启动或执行器不可用")
        
        try:
            # 更新任务状态
            task.last_run = datetime.now()
            task.run_count += 1
            
            # 提交任务到线程池
            future = self._executor.submit(
                self._execute_task,
                task
            )
            
            # 添加回调处理结果
            future.add_done_callback(
                lambda f: self._handle_task_result(f, task)
            )
            
            logger.debug(f"提交任务执行: {task.name} (ID: {task.task_id})")
            
            return future
            
        except Exception as e:
            logger.error(f"提交任务失败 {task.name}: {e}")
            raise SchedulerError(f"提交任务失败: {e}") from e
    
    def _execute_task(self, task: ScheduledTask) -> Any:
        """
        执行任务
        
        Args:
            task: 要执行的任务
            
        Returns:
            Any: 任务执行结果
        """
        start_time = time.time()
        
        try:
            logger.info(f"开始执行任务: {task.name}")
            
            # 执行函数
            result = task.func(*task.args, **task.kwargs)
            
            execution_time = time.time() - start_time
            
            logger.info(
                f"任务执行成功: {task.name}, "
                f"耗时: {execution_time:.2f}s"
            )
            
            return {
                "success": True,
                "result": result,
                "execution_time": execution_time,
                "task_id": task.task_id,
                "task_name": task.name
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            logger.error(
                f"任务执行失败: {task.name}, "
                f"错误: {e}, "
                f"耗时: {execution_time:.2f}s"
            )
            
            return {
                "success": False,
                "error": str(e),
                "execution_time": execution_time,
                "task_id": task.task_id,
                "task_name": task.name
            }
    
    def _handle_task_result(self, future: Future, task: ScheduledTask) -> None:
        """
        处理任务执行结果
        
        Args:
            future: 任务执行Future
            task: 对应的任务
        """
        try:
            result = future.result(timeout=0.1)
            
            with self._lock:
                if result["success"]:
                    task.success_count += 1
                    self.stats["completed_tasks"] += 1
                else:
                    task.error_count += 1
                    task.last_error = result["error"]
                    self.stats["failed_tasks"] += 1
                
                # 更新总执行时间
                self.stats["total_execution_time"] += result["execution_time"]
                
        except Exception as e:
            logger.error(f"处理任务结果失败 {task.name}: {e}")
            
            with self._lock:
                task.error_count += 1
                task.last_error = str(e)
                self.stats["failed_tasks"] += 1
    
    @property
    def task_count(self) -> int:
        """获取任务数量"""
        with self._lock:
            return len(self.tasks)