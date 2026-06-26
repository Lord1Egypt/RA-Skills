"""
指数退避重试策略

提供带指数退避的重试机制，用于处理临时性网络或API错误。
"""

import time
import random
from typing import Callable, Any, Optional, Tuple, List
from functools import wraps


class RetryStrategy:
    """
    指数退避重试策略
    
    当函数执行失败时，按照指数退避策略进行重试，
    即每次重试的等待时间按指数增长。
    
    Attributes:
        max_retries: 最大重试次数
        base_delay: 基础延迟时间（秒）
        max_delay: 最大延迟时间（秒）
        exponential_base: 指数基数
        jitter: 是否添加随机抖动避免惊群效应
        retry_exceptions: 需要重试的异常类型列表
    """
    
    def __init__(self, 
                 max_retries: int = 3, 
                 base_delay: float = 1.0,
                 max_delay: float = 60.0,
                 exponential_base: float = 2.0,
                 jitter: bool = True,
                 retry_exceptions: Optional[Tuple[type, ...]] = None):
        """
        初始化重试策略
        
        Args:
            max_retries: 最大重试次数，默认3次
            base_delay: 基础延迟时间（秒），默认1秒
            max_delay: 最大延迟时间（秒），默认60秒
            exponential_base: 指数基数，默认2（即1, 2, 4, 8...）
            jitter: 是否添加随机抖动，默认True
            retry_exceptions: 需要重试的异常类型元组，默认捕获所有Exception
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.retry_exceptions = retry_exceptions or (Exception,)
        self._last_attempt = 0
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """
        执行带重试的函数
        
        Args:
            func: 要执行的函数
            *args: 函数位置参数
            **kwargs: 函数关键字参数
            
        Returns:
            Any: 函数执行结果
            
        Raises:
            Exception: 所有重试都失败后抛出最后一次异常
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            self._last_attempt = attempt
            
            try:
                return func(*args, **kwargs)
            except self.retry_exceptions as e:
                last_exception = e
                
                if attempt == self.max_retries:
                    # 所有重试都已用完
                    raise last_exception
                
                # 计算延迟时间
                delay = self._calculate_delay(attempt)
                time.sleep(delay)
        
        # 理论上不会执行到这里
        raise last_exception if last_exception else Exception("Unknown error")
    
    def _calculate_delay(self, attempt: int) -> float:
        """
        计算重试延迟时间
        
        Args:
            attempt: 当前尝试次数（从0开始）
            
        Returns:
            float: 需要延迟的秒数
        """
        # 指数退避: base_delay * (exponential_base ^ attempt)
        delay = self.base_delay * (self.exponential_base ** attempt)
        
        # 限制最大延迟
        delay = min(delay, self.max_delay)
        
        # 添加随机抖动 (±20%)，避免惊群效应
        if self.jitter:
            delay = delay * (0.8 + random.random() * 0.4)
        
        return delay
    
    def get_last_attempt(self) -> int:
        """
        获取上次执行的尝试次数
        
        Returns:
            int: 尝试次数（0表示第一次就成功）
        """
        return self._last_attempt
    
    def decorator(self, func: Callable) -> Callable:
        """
        将重试策略作为装饰器使用
        
        用法:
            @retry_strategy.decorator
            def my_func():
                ...
                
        Args:
            func: 要包装的函数
            
        Returns:
            Callable: 包装后的函数
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.execute(func, *args, **kwargs)
        return wrapper


class CircuitBreaker:
    """
    熔断器
    
    当连续失败达到一定阈值时，暂时阻止请求，
    防止级联故障。
    """
    
    STATE_CLOSED = 'closed'      # 正常状态
    STATE_OPEN = 'open'          # 熔断状态
    STATE_HALF_OPEN = 'half_open'  # 半开状态
    
    def __init__(self, failure_threshold: int = 5, 
                 recovery_timeout: float = 30.0):
        """
        初始化熔断器
        
        Args:
            failure_threshold: 触发熔断的失败次数阈值
            recovery_timeout: 熔断后恢复等待时间（秒）
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self._failure_count = 0
        self._last_failure_time = None
        self._state = self.STATE_CLOSED
    
    def can_execute(self) -> bool:
        """
        检查是否可以执行
        
        Returns:
            bool: 可以执行返回True
        """
        if self._state == self.STATE_CLOSED:
            return True
        
        if self._state == self.STATE_OPEN:
            if time.time() - self._last_failure_time >= self.recovery_timeout:
                self._state = self.STATE_HALF_OPEN
                return True
            return False
        
        return True  # HALF_OPEN
    
    def record_success(self) -> None:
        """记录成功"""
        self._failure_count = 0
        self._state = self.STATE_CLOSED
    
    def record_failure(self) -> None:
        """记录失败"""
        self._failure_count += 1
        self._last_failure_time = time.time()
        
        if self._failure_count >= self.failure_threshold:
            self._state = self.STATE_OPEN
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """
        在熔断器保护下执行函数
        
        Args:
            func: 要执行的函数
            
        Returns:
            Any: 函数执行结果
            
        Raises:
            Exception: 熔断器打开时抛出异常
        """
        if not self.can_execute():
            raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self.record_success()
            return result
        except Exception as e:
            self.record_failure()
            raise e
