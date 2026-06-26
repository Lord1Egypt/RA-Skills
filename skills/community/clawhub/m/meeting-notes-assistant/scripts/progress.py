#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进度条显示模块

用于显示转写、生成等长时间操作的处理进度
"""

import time
import threading
from typing import Callable, Optional


class ProgressBar:
    """简单的命令行进度条"""
    
    def __init__(self, total: int = 100, width: int = 40, 
                 prefix: str = "进度", suffix: str = "完成"):
        self.total = total
        self.width = width
        self.prefix = prefix
        self.suffix = suffix
        self.progress = 0
        self._lock = threading.Lock()
        
    def update(self, progress: int, message: Optional[str] = None):
        """更新进度"""
        with self._lock:
            self.progress = min(progress, self.total)
            percent = self.progress / self.total * 100
            filled = int(self.width * self.progress // self.total)
            bar = '█' * filled + '░' * (self.width - filled)
            
            msg = ""
            if message:
                msg = f" - {message}"
            
            # 使用 \r 返回行首覆盖
            print(f"\r{self.prefix}: |{bar}| {percent:.1f}%{msg}", end='', flush=True)
    
    def increment(self, amount: int = 1, message: Optional[str] = None):
        """增加进度"""
        self.update(self.progress + amount, message)
    
    def finish(self, message: Optional[str] = None):
        """完成进度"""
        self.update(self.total, message or self.suffix)
        print()  # 换行


class Spinner:
    """旋转加载指示器"""
    
    _chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    
    def __init__(self, message: str = "处理中"):
        self.message = message
        self._running = False
        self._thread = None
        self._lock = threading.Lock()
        
    def start(self):
        """启动旋转器"""
        if self._running:
            return
            
        self._running = True
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()
    
    def _spin(self):
        """旋转动画"""
        idx = 0
        while self._running:
            with self._lock:
                char = self._chars[idx % len(self._chars)]
                print(f"\r{self.message} {char}...", end='', flush=True)
            idx += 1
            time.sleep(0.1)
    
    def stop(self, message: Optional[str] = None):
        """停止旋转器"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=0.2)
        
        msg = message or "完成"
        print(f"\r{self.message}: {msg}")


def run_with_progress(
    func: Callable,
    total: int,
    progress_callback: Callable[[int, str], None],
    message_prefix: str = "处理"
):
    """
    在函数执行过程中显示进度
    
    Args:
        func: 要执行的函数
        total: 总进度值
        progress_callback: 进度回调函数 (progress, message)
        message_prefix: 进度消息前缀
    """
    def wrapper(*args, **kwargs):
        progress_bar = ProgressBar(total, prefix=message_prefix)
        
        def callback(progress: int, message: str = ""):
            progress_bar.update(progress, message)
        
        # 执行函数并更新进度
        result = func(callback, *args, **kwargs)
        
        progress_bar.finish()
        return result
    
    return wrapper


class ProgressMonitor:
    """进度监控器（用于长时间任务）"""
    
    def __init__(self, total: int, message: str = "处理中"):
        self.total = total
        self.message = message
        self.progress = 0
        self.current_message = ""
        self.start_time = time.time()
        self.spinner = Spinner(message)
        self.spinner.start()
        
    def update(self, progress: int, message: str = ""):
        """更新进度"""
        self.progress = min(progress, self.total)
        self.current_message = message
        
        # 计算预计剩余时间
        elapsed = time.time() - self.start_time
        if self.progress > 0:
            rate = self.progress / elapsed
            remaining = (self.total - self.progress) / rate
            remaining_str = f"（预计剩余 {remaining:.0f} 秒）"
        else:
            remaining_str = ""
        
        # 重新显示
        percent = self.progress / self.total * 100
        self.spinner.stop()
        self.spinner = Spinner(f"{self.message} {percent:.0f}%{remaining_str}")
        if message:
            self.spinner = Spinner(f"{self.message} {percent:.0f}% - {message}{remaining_str}")
        self.spinner.start()
    
    def finish(self, message: str = "完成"):
        """完成"""
        elapsed = time.time() - self.start_time
        elapsed_str = f"（耗时 {elapsed:.1f} 秒）"
        self.spinner.stop(f"{message}{elapsed_str}")


# 示例用法
if __name__ == "__main__":
    print("进度条示例：\n")
    
    # 示例 1: 简单进度条
    bar = ProgressBar(total=100, prefix="转写进度", suffix="完成")
    for i in range(0, 101, 10):
        bar.update(i, f"正在处理 {i}%")
        time.sleep(0.2)
    bar.finish()
    
    print("\n旋转器示例：\n")
    
    # 示例 2: 旋转器
    spinner = Spinner("加载中")
    spinner.start()
    time.sleep(2)
    spinner.stop("加载完成")
    
    print("\n进度监控器示例：\n")
    
    # 示例 3: 进度监控器
    monitor = ProgressMonitor(total=100, message="生成纪要")
    for i in range(0, 101, 20):
        time.sleep(0.3)
        messages = ["解析文本", "提取议题", "识别待办", "生成文档"]
        monitor.update(i, messages[i // 20])
    monitor.finish("生成完成")
