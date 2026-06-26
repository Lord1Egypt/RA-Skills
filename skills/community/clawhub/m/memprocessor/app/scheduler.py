"""任务调度器 - 每日沉淀和每周归档"""
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config import settings
from app.services.memory_service import get_memory_service


class TaskScheduler:
    """任务调度器"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self._started = False
    
    def setup(self):
        """设置定时任务"""
        # 每日沉淀任务 - 23:50
        self.scheduler.add_job(
            self._daily_persistence,
            trigger=CronTrigger(
                hour=settings.DAILY_PERSISTENCE_HOUR,
                minute=settings.DAILY_PERSISTENCE_MINUTE
            ),
            id="daily_persistence",
            name="每日记忆沉淀",
            replace_existing=True
        )
        
        # 每周归档任务 - 周日00:00
        self.scheduler.add_job(
            self._weekly_archive,
            trigger=CronTrigger(
                day_of_week=settings.WEEKLY_ARCHIVE_DAY,
                hour=settings.WEEKLY_ARCHIVE_HOUR,
                minute=0
            ),
            id="weekly_archive",
            name="每周记忆归档",
            replace_existing=True
        )
        
        print("[Scheduler] Tasks configured:")
        print(f"  - Daily persistence: {settings.DAILY_PERSISTENCE_HOUR}:{settings.DAILY_PERSISTENCE_MINUTE}")
        print(f"  - Weekly archive: Sunday {settings.WEEKLY_ARCHIVE_HOUR}:00")
    
    async def _daily_persistence(self):
        """每日沉淀任务"""
        print(f"[Scheduler] Running daily persistence at {datetime.utcnow()}")
        try:
            service = await get_memory_service()
            await service.run_daily_persistence()
            print("[Scheduler] Daily persistence completed")
        except Exception as e:
            print(f"[Scheduler] Daily persistence failed: {e}")
    
    async def _weekly_archive(self):
        """每周归档任务"""
        print(f"[Scheduler] Running weekly archive at {datetime.utcnow()}")
        try:
            service = await get_memory_service()
            await service.run_weekly_archive()
            print("[Scheduler] Weekly archive completed")
        except Exception as e:
            print(f"[Scheduler] Weekly archive failed: {e}")
    
    def start(self):
        """启动调度器"""
        if not self._started:
            self.setup()
            self.scheduler.start()
            self._started = True
            print("[Scheduler] Started")
    
    def stop(self):
        """停止调度器"""
        if self._started:
            self.scheduler.shutdown()
            self._started = False
            print("[Scheduler] Stopped")
    
    def get_jobs(self):
        """获取所有任务"""
        return self.scheduler.get_jobs()


# 单例
_scheduler: TaskScheduler = TaskScheduler()


def get_scheduler() -> TaskScheduler:
    """获取调度器单例"""
    return _scheduler
