"""
Token Bucket 漏斗桶限流器实现

基于令牌桶算法的限流器，用于控制API请求频率。
"""

import time
import threading
from typing import Optional


class TokenBucket:
    """
    漏斗桶（令牌桶）限流器
    
    使用令牌桶算法实现限流，可以平滑请求频率并允许一定程度的突发。
    
    Attributes:
        rate: 令牌填充速率，每秒多少个令牌
        capacity: 桶的容量，最大可积累的令牌数
        tokens: 当前可用令牌数
        last_update: 上次更新时间
    """
    
    def __init__(self, rate: float, capacity: int):
        """
        初始化限流器
        
        Args:
            rate: 令牌填充速率，每秒多少个（如 0.5 表示每2秒1个）
            capacity: 桶容量，最大可突发请求数
        """
        self.rate = rate  # 每秒填充速率
        self.capacity = capacity  # 桶容量
        self.tokens = float(capacity)  # 当前令牌数，使用float便于计算
        self.last_update = time.time()
        self._lock = threading.Lock()
    
    def _add_tokens(self) -> None:
        """
        根据时间流逝添加新令牌
        
        基于上次更新时间计算应该添加的令牌数
        """
        now = time.time()
        elapsed = now - self.last_update
        # 根据经过的时间添加令牌
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now
    
    def acquire(self, tokens: int = 1, blocking: bool = False, 
                timeout: Optional[float] = None) -> bool:
        """
        获取令牌
        
        Args:
            tokens: 需要的令牌数，默认为1
            blocking: 是否阻塞等待，默认False立即返回
            timeout: 阻塞等待的最大时间（秒），None表示无限等待
            
        Returns:
            bool: 成功获取令牌返回True，否则返回False
        """
        with self._lock:
            self._add_tokens()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            
            if not blocking:
                return False
            
            # 计算需要等待的时间
            needed = tokens - self.tokens
            wait_time = needed / self.rate
            
            if timeout is not None and wait_time > timeout:
                return False
        
        # 在锁外等待
        if blocking:
            time.sleep(wait_time)
            return self.acquire(tokens, blocking=False)
        
        return False
    
    def try_acquire(self, tokens: int = 1) -> bool:
        """
        尝试获取令牌（非阻塞）
        
        Args:
            tokens: 需要的令牌数
            
        Returns:
            bool: 成功返回True，否则返回False
        """
        return self.acquire(tokens, blocking=False)
    
    def get_available_tokens(self) -> float:
        """
        获取当前可用令牌数
        
        Returns:
            float: 当前可用令牌数
        """
        with self._lock:
            self._add_tokens()
            return self.tokens
    
    def reset(self) -> None:
        """重置令牌桶到满状态"""
        with self._lock:
            self.tokens = float(self.capacity)
            self.last_update = time.time()
