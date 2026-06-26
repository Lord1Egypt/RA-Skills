"""
调度器模块
提供任务调度功能
"""

from .base import Scheduler, ScheduledTask

__all__ = [
    "Scheduler",
    "ScheduledTask",
]

# 条件导入APScheduler实现
try:
    from .apscheduler_impl import APScheduler
    __all__.append("APScheduler")
except ImportError:
    # APScheduler未安装，跳过
    pass