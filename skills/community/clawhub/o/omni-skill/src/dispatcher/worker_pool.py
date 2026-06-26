"""
预热工作线程池 (Pre-warmed Worker Pool)
"""
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable, Any
import config.settings as settings

class PrewarmedPool:
    """线程池管理与预热"""
    def __init__(self, max_workers: int = settings.WORKER_POOL_SIZE):
        self.max_workers = max_workers
        self.pool = ThreadPoolExecutor(max_workers=max_workers)
        self._prewarm()

    def _dummy_task(self):
        """空任务，用于强制操作系统分配线程"""
        pass

    def _prewarm(self):
        """预热线程"""
        # 提交等同于最大线程数的空任务，迫使操作系统预先分配线程资源
        # 此举可消除首次调用的冷启动延迟
        futures = [self.pool.submit(self._dummy_task) for _ in range(self.max_workers)]
        for future in futures:
            future.result() # 等待空任务结束，确保所有线程就位

    def execute(self, func: Callable, *args, **kwargs) -> Future:
        """将任务提交给线程执行"""
        return self.pool.submit(func, *args, **kwargs)

    def shutdown(self, wait: bool = True):
        """关闭线程池"""
        self.pool.shutdown(wait=wait)