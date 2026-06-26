"""
APScheduler实现
使用APScheduler库提供完整的调度功能
"""

import logging
from typing import Any, Callable, Dict, Optional, Union
from datetime import datetime
import pytz

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger
    from apscheduler.jobstores.memory import MemoryJobStore
    from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
    from apscheduler.executors.pool import ThreadPoolExecutor
    APSCHEDULER_AVAILABLE = True
except ImportError:
    APSCHEDULER_AVAILABLE = False

from .base import Scheduler, ScheduledTask
from ..exceptions import SchedulerError, ConfigurationError
from ..config import SchedulerConfig

logger = logging.getLogger(__name__)


class APScheduler(Scheduler):
    """基于APScheduler的调度器实现"""
    
    def __init__(self, config: SchedulerConfig):
        """
        初始化APScheduler
        
        Args:
            config: 调度器配置
            
        Raises:
            ConfigurationError: APScheduler库未安装
        """
        if not APSCHEDULER_AVAILABLE:
            raise ConfigurationError(
                "APScheduler库未安装，请运行: pip install APScheduler"
            )
        
        super().__init__(config)
        self._apscheduler: Optional[BackgroundScheduler] = None
        
        logger.debug("初始化APScheduler实现")
    
    def start(self) -> None:
        """启动调度器"""
        with self._lock:
            if self.running:
                logger.warning("调度器已经在运行")
                return
            
            try:
                # 配置jobstore
                jobstores = {}
                if self.config.job_store == "sqlite":
                    jobstores['default'] = SQLAlchemyJobStore(
                        url='sqlite:///jobs.sqlite'
                    )
                else:
                    jobstores['default'] = MemoryJobStore()
                
                # 配置executor
                executors = {
                    'default': ThreadPoolExecutor(self.config.max_workers)
                }
                
                # 配置job_defaults
                job_defaults = {
                    'coalesce': True,  # 合并错过的执行
                    'max_instances': 3,  # 最大实例数
                    'misfire_grace_time': 60  # 错过执行的宽限时间
                }
                
                # 创建调度器
                self._apscheduler = BackgroundScheduler(
                    jobstores=jobstores,
                    executors=executors,
                    job_defaults=job_defaults,
                    timezone=pytz.timezone(self.config.timezone)
                )
                
                # 启动调度器
                self._apscheduler.start()
                
                # 调用父类的start方法
                super().start()
                
                logger.info("APScheduler启动成功")
                
            except Exception as e:
                logger.error(f"APScheduler启动失败: {e}")
                self.running = False
                raise SchedulerError(f"APScheduler启动失败: {e}") from e
    
    def shutdown(self, wait: bool = True) -> None:
        """关闭调度器"""
        with self._lock:
            if not self.running:
                logger.warning("调度器已经停止")
                return
            
            # 停止APScheduler
            if self._apscheduler:
                self._apscheduler.shutdown(wait=wait)
                self._apscheduler = None
            
            # 调用父类的shutdown方法
            super().shutdown(wait)
    
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
                
                # 创建CronTrigger
                cron_parts = schedule.split()
                if len(cron_parts) != 5:
                    raise ValueError(f"无效的Cron表达式，需要5个部分: {schedule}")
                
                trigger = CronTrigger(
                    minute=cron_parts[0],
                    hour=cron_parts[1],
                    day=cron_parts[2],
                    month=cron_parts[3],
                    day_of_week=cron_parts[4],
                    timezone=pytz.timezone(self.config.timezone)
                )
                
                # 添加到APScheduler
                if not self._apscheduler:
                    raise SchedulerError("调度器未启动")
                
                # 包装函数以跟踪执行
                def wrapped_func():
                    return self._execute_wrapped_task(func, task_id, args, kwargs)
                
                job = self._apscheduler.add_job(
                    wrapped_func,
                    trigger=trigger,
                    id=task_id,
                    name=task_name,
                    args=args,
                    kwargs=kwargs,
                    replace_existing=True
                )
                
                # 计算下次运行时间
                next_run = job.next_run_time
                
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
                
                logger.info(f"添加APScheduler任务: {task_name} (ID: {task_id}), 调度: {schedule}")
                
                return task_id
                
            except Exception as e:
                logger.error(f"添加APScheduler任务失败: {e}")
                raise SchedulerError(f"添加任务失败: {e}") from e
    
    def _execute_wrapped_task(self, func: Callable, task_id: str, 
                             args: tuple, kwargs: Dict[str, Any]) -> Any:
        """
        包装任务执行，用于跟踪和统计
        
        Args:
            func: 原始函数
            task_id: 任务ID
            args: 位置参数
            kwargs: 关键字参数
            
        Returns:
            函数执行结果
        """
        import time
        
        with self._lock:
            if task_id not in self.tasks:
                logger.warning(f"任务不存在，跳过执行: {task_id}")
                return None
            
            task = self.tasks[task_id]
            
            if not task.enabled:
                logger.debug(f"任务已禁用，跳过执行: {task.name}")
                return None
        
        start_time = time.time()
        
        try:
            logger.info(f"APScheduler开始执行任务: {task.name}")
            
            # 执行函数
            result = func(*args, **kwargs)
            
            execution_time = time.time() - start_time
            
            # 更新任务状态
            with self._lock:
                task.last_run = datetime.now()
                task.run_count += 1
                task.success_count += 1
                self.stats["completed_tasks"] += 1
                self.stats["total_execution_time"] += execution_time
            
            logger.info(
                f"APScheduler任务执行成功: {task.name}, "
                f"耗时: {execution_time:.2f}s"
            )
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            # 更新任务状态
            with self._lock:
                task.last_run = datetime.now()
                task.run_count += 1
                task.error_count += 1
                task.last_error = str(e)
                self.stats["failed_tasks"] += 1
                self.stats["total_execution_time"] += execution_time
            
            logger.error(
                f"APScheduler任务执行失败: {task.name}, "
                f"错误: {e}, "
                f"耗时: {execution_time:.2f}s"
            )
            
            raise
    
    def remove_task(self, task_id: str) -> bool:
        """移除计划任务"""
        with self._lock:
            if task_id not in self.tasks:
                logger.warning(f"任务不存在: {task_id}")
                return False
            
            # 从APScheduler中移除
            if self._apscheduler:
                try:
                    self._apscheduler.remove_job(task_id)
                except Exception as e:
                    logger.warning(f"从APScheduler移除任务失败 {task_id}: {e}")
            
            # 从本地任务列表中移除
            task = self.tasks[task_id]
            del self.tasks[task_id]
            
            self.stats["active_tasks"] -= 1
            
            logger.info(f"移除APScheduler任务: {task.name} (ID: {task_id})")
            return True
    
    def enable_task(self, task_id: str) -> bool:
        """启用任务"""
        with self._lock:
            if task_id not in self.tasks:
                logger.warning(f"任务不存在: {task_id}")
                return False
            
            task = self.tasks[task_id]
            task.enabled = True
            
            # 在APScheduler中恢复任务（如果需要）
            if self._apscheduler:
                try:
                    job = self._apscheduler.get_job(task_id)
                    if job:
                        job.resume()
                except Exception as e:
                    logger.warning(f"在APScheduler中启用任务失败 {task_id}: {e}")
            
            logger.debug(f"启用APScheduler任务: {task.name} (ID: {task_id})")
            return True
    
    def disable_task(self, task_id: str) -> bool:
        """禁用任务"""
        with self._lock:
            if task_id not in self.tasks:
                logger.warning(f"任务不存在: {task_id}")
                return False
            
            task = self.tasks[task_id]
            task.enabled = False
            
            # 在APScheduler中暂停任务
            if self._apscheduler:
                try:
                    job = self._apscheduler.get_job(task_id)
                    if job:
                        job.pause()
                except Exception as e:
                    logger.warning(f"在APScheduler中禁用任务失败 {task_id}: {e}")
            
            logger.debug(f"禁用APScheduler任务: {task.name} (ID: {task_id})")
            return True
    
    def run_task_now(self, task_id: str) -> bool:
        """立即运行任务"""
        with self._lock:
            if task_id not in self.tasks:
                logger.warning(f"任务不存在: {task_id}")
                return False
            
            task = self.tasks[task_id]
            
            if not task.enabled:
                logger.warning(f"任务已禁用: {task.name}")
                return False
            
            # 立即运行任务
            if self._apscheduler:
                try:
                    self._apscheduler.modify_job(task_id, next_run_time=datetime.now())
                    logger.info(f"立即运行APScheduler任务: {task.name} (ID: {task_id})")
                    return True
                except Exception as e:
                    logger.error(f"立即运行任务失败 {task_id}: {e}")
                    return False
            else:
                return super().run_task_now(task_id)
    
    def _validate_cron(self, cron_expr: str) -> bool:
        """验证Cron表达式"""
        try:
            # 使用APScheduler的CronTrigger验证
            cron_parts = cron_expr.split()
            if len(cron_parts) != 5:
                return False
            
            # 尝试创建CronTrigger来验证
            CronTrigger(
                minute=cron_parts[0],
                hour=cron_parts[1],
                day=cron_parts[2],
                month=cron_parts[3],
                day_of_week=cron_parts[4]
            )
            
            return True
            
        except Exception:
            return False
    
    def _calculate_next_run(self, cron_expr: str) -> datetime:
        """计算下次运行时间"""
        try:
            cron_parts = cron_expr.split()
            if len(cron_parts) != 5:
                raise ValueError(f"无效的Cron表达式: {cron_expr}")
            
            trigger = CronTrigger(
                minute=cron_parts[0],
                hour=cron_parts[1],
                day=cron_parts[2],
                month=cron_parts[3],
                day_of_week=cron_parts[4],
                timezone=pytz.timezone(self.config.timezone)
            )
            
            return trigger.get_next_fire_time(None, datetime.now())
            
        except Exception as e:
            logger.error(f"计算下次运行时间失败: {e}")
            # 返回一个较晚的时间，避免频繁出错
            return datetime.now().replace(year=datetime.now().year + 1)
    
    def get_apscheduler_stats(self) -> Dict[str, Any]:
        """
        获取APScheduler的详细统计信息
        
        Returns:
            APScheduler统计信息
        """
        if not self._apscheduler:
            return {"error": "APScheduler未启动"}
        
        try:
            jobs = self._apscheduler.get_jobs()
            
            return {
                "job_count": len(jobs),
                "running_jobs": sum(1 for job in jobs if job.next_run_time),
                "paused_jobs": sum(1 for job in jobs if hasattr(job, 'paused') and job.paused),
                "executor_info": str(self._apscheduler.executors),
                "jobstore_info": str(self._apscheduler.jobstores),
                "scheduler_state": self._apscheduler.state
            }
            
        except Exception as e:
            return {"error": f"获取APScheduler统计失败: {e}"}