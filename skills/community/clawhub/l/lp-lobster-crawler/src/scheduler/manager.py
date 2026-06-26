"""定时调度管理器 — APScheduler 集成。

支持：
- 按站点 cron 表达式调度爬取任务
- 任务生命周期管理（添加/暂停/恢复/删除）
- 从 YAML 配置自动注册任务
"""

import logging
import subprocess
import sys
from typing import Any

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED, JobExecutionEvent
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from src.config import get_setting, load_all_sites

logger = logging.getLogger(__name__)


def run_spider(spider_name: str, **kwargs: str) -> None:
    """运行 Scrapy 爬虫（通过子进程调用）。

    Args:
        spider_name: 爬虫名称。
        **kwargs: 传递给爬虫的参数。
    """
    cmd = [sys.executable, "-m", "scrapy", "crawl", spider_name]
    for key, value in kwargs.items():
        cmd.extend(["-a", f"{key}={value}"])

    logger.info("Starting spider: %s with args %s", spider_name, kwargs)
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600,
        )
        if result.returncode == 0:
            logger.info("Spider %s completed successfully", spider_name)
        else:
            logger.error("Spider %s failed: %s", spider_name, result.stderr[-500:] if result.stderr else "unknown")
    except subprocess.TimeoutExpired:
        logger.error("Spider %s timed out after 3600s", spider_name)
    except Exception as e:
        logger.error("Failed to run spider %s: %s", spider_name, e)


class ScheduleManager:
    """调度管理器。"""

    def __init__(self, timezone: str | None = None) -> None:
        """初始化调度器。

        Args:
            timezone: 时区字符串，默认从配置读取。
        """
        tz = timezone or get_setting("scheduler", "timezone", default="Asia/Shanghai")
        self._scheduler = BackgroundScheduler(timezone=tz)
        self._scheduler.add_listener(self._on_job_event, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self._jobs: dict[str, dict[str, Any]] = {}

    def add_spider_job(
        self,
        site_name: str,
        cron_expr: str,
        spider_name: str | None = None,
        spider_kwargs: dict[str, str] | None = None,
    ) -> str:
        """添加爬虫定时任务。

        Args:
            site_name: 站点名称（用作 job ID 前缀）。
            cron_expr: cron 表达式，如 "0 */6 * * *"。
            spider_name: 爬虫名称，默认与 site_name 相同。
            spider_kwargs: 传递给爬虫的额外参数。

        Returns:
            任务 ID。
        """
        job_id = f"crawl_{site_name}"
        spider = spider_name or site_name
        kwargs = spider_kwargs or {}

        trigger = CronTrigger.from_crontab(cron_expr)
        self._scheduler.add_job(
            run_spider,
            trigger=trigger,
            args=[spider],
            kwargs=kwargs,
            id=job_id,
            replace_existing=True,
            name=f"Crawl {site_name}",
        )

        self._jobs[job_id] = {
            "site_name": site_name,
            "spider_name": spider,
            "cron": cron_expr,
            "status": "active",
        }
        logger.info("Added job %s: %s with cron '%s'", job_id, spider, cron_expr)
        return job_id

    def remove_job(self, job_id: str) -> bool:
        """移除定时任务。

        Args:
            job_id: 任务 ID。

        Returns:
            True 表示成功移除。
        """
        try:
            self._scheduler.remove_job(job_id)
            self._jobs.pop(job_id, None)
            logger.info("Removed job %s", job_id)
            return True
        except Exception:
            return False

    def pause_job(self, job_id: str) -> bool:
        """暂停任务。"""
        try:
            self._scheduler.pause_job(job_id)
            if job_id in self._jobs:
                self._jobs[job_id]["status"] = "paused"
            return True
        except Exception:
            return False

    def resume_job(self, job_id: str) -> bool:
        """恢复任务。"""
        try:
            self._scheduler.resume_job(job_id)
            if job_id in self._jobs:
                self._jobs[job_id]["status"] = "active"
            return True
        except Exception:
            return False

    def list_jobs(self) -> list[dict[str, Any]]:
        """列出所有注册的任务。"""
        result = []
        for job_id, info in self._jobs.items():
            job = self._scheduler.get_job(job_id)
            next_run = str(job.next_run_time) if job and job.next_run_time else "N/A"
            result.append({
                "job_id": job_id,
                "site_name": info["site_name"],
                "spider_name": info["spider_name"],
                "cron": info["cron"],
                "status": info["status"],
                "next_run": next_run,
            })
        return result

    def load_from_config(self) -> int:
        """从站点配置自动注册所有启用的爬取任务。

        Returns:
            注册的任务数量。
        """
        sites = load_all_sites()
        default_cron = get_setting("scheduler", "default_cron", default="0 */6 * * *")
        count = 0

        for site_name, site_config in sites.items():
            schedule = site_config.get("schedule", {})
            if not schedule.get("enabled", True):
                continue

            cron_expr = schedule.get("cron", default_cron)
            spider_name = site_config.get("site", {}).get("name", site_name)
            self.add_spider_job(site_name, cron_expr, spider_name=spider_name)
            count += 1

        logger.info("Loaded %d scheduled jobs from config", count)
        return count

    def start(self) -> None:
        """启动调度器。"""
        if not self._scheduler.running:
            self._scheduler.start()
            logger.info("Scheduler started")

    def stop(self) -> None:
        """停止调度器。"""
        if self._scheduler.running:
            self._scheduler.shutdown(wait=False)
            logger.info("Scheduler stopped")

    @property
    def is_running(self) -> bool:
        """调度器是否正在运行。"""
        return self._scheduler.running

    @staticmethod
    def _on_job_event(event: JobExecutionEvent) -> None:
        """任务执行事件回调。"""
        if event.exception:
            logger.error("Job %s raised an exception: %s", event.job_id, event.exception)
        else:
            logger.info("Job %s executed successfully", event.job_id)
