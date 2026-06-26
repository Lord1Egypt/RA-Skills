#!/usr/bin/env python3
"""
重试降级适配器
与 clawhub-retry-fallback Skill 联动
"""

import time
import functools
from typing import Callable, Any, Optional, Type
from dataclasses import dataclass
from enum import Enum


class RetryStrategy(Enum):
    """重试策略"""
    FIXED = "fixed"           # 固定间隔
    EXPONENTIAL = "exponential"  # 指数退避
    LINEAR = "linear"         # 线性增长


@dataclass
class RetryConfig:
    """重试配置"""
    max_attempts: int = 3
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL
    initial_delay: float = 1.0
    max_delay: float = 10.0
    backoff_factor: float = 2.0
    retry_exceptions: tuple = (Exception,)


class RetryAdapter:
    """
    重试适配器
    为文件解析等操作提供自动重试能力
    """
    
    def __init__(self, config: RetryConfig = None):
        """
        初始化适配器
        
        Args:
            config: 重试配置
        """
        self.config = config or RetryConfig()
        self.attempt_history = []
    
    def with_retry(self, func: Callable = None, *, 
                   max_attempts: int = None,
                   strategy: RetryStrategy = None) -> Callable:
        """
        装饰器：为函数添加重试能力
        
        Usage:
            @adapter.with_retry
            def my_func():
                pass
                
            @adapter.with_retry(max_attempts=5)
            def my_func():
                pass
        """
        config = RetryConfig(
            max_attempts=max_attempts or self.config.max_attempts,
            strategy=strategy or self.config.strategy
        )
        
        def decorator(f: Callable) -> Callable:
            @functools.wraps(f)
            def wrapper(*args, **kwargs) -> Any:
                return self.execute_with_retry(f, config, *args, **kwargs)
            return wrapper
        
        if func is None:
            return decorator
        else:
            return decorator(func)
    
    def execute_with_retry(self, func: Callable, config: RetryConfig = None,
                          *args, **kwargs) -> Any:
        """
        执行带重试的函数
        
        Args:
            func: 要执行的函数
            config: 重试配置
            *args, **kwargs: 函数参数
            
        Returns:
            函数返回值
            
        Raises:
            最后一次重试的异常
        """
        config = config or self.config
        last_exception = None
        
        for attempt in range(1, config.max_attempts + 1):
            try:
                result = func(*args, **kwargs)
                
                # 记录成功
                self._log_attempt(func.__name__, attempt, "success")
                
                return result
                
            except config.retry_exceptions as e:
                last_exception = e
                
                # 记录失败
                self._log_attempt(func.__name__, attempt, "failed", str(e))
                
                if attempt < config.max_attempts:
                    # 计算延迟
                    delay = self._calculate_delay(config, attempt)
                    
                    print(f"[RetryAdapter] {func.__name__} 第 {attempt} 次尝试失败: {e}")
                    print(f"[RetryAdapter] {delay:.1f} 秒后重试...")
                    
                    time.sleep(delay)
                else:
                    print(f"[RetryAdapter] {func.__name__} 达到最大重试次数 ({config.max_attempts})，放弃")
        
        # 所有重试都失败
        raise last_exception
    
    def _calculate_delay(self, config: RetryConfig, attempt: int) -> float:
        """计算重试延迟"""
        if config.strategy == RetryStrategy.FIXED:
            return config.initial_delay
        
        elif config.strategy == RetryStrategy.EXPONENTIAL:
            delay = config.initial_delay * (config.backoff_factor ** (attempt - 1))
            return min(delay, config.max_delay)
        
        elif config.strategy == RetryStrategy.LINEAR:
            delay = config.initial_delay * attempt
            return min(delay, config.max_delay)
        
        return config.initial_delay
    
    def _log_attempt(self, func_name: str, attempt: int, 
                     status: str, error: str = None):
        """记录尝试历史"""
        self.attempt_history.append({
            "function": func_name,
            "attempt": attempt,
            "status": status,
            "error": error,
            "timestamp": time.time()
        })


class FallbackHandler:
    """
    降级处理器
    当主逻辑失败时，执行降级逻辑
    """
    
    def __init__(self):
        self.fallback_registry = {}
    
    def register_fallback(self, exception_type: Type[Exception]):
        """
        注册降级处理函数
        
        Usage:
            @handler.register_fallback(ParseError)
            def handle_parse_error(file_path):
                return parse_lite(file_path)
        """
        def decorator(func: Callable) -> Callable:
            self.fallback_registry[exception_type] = func
            return func
        return decorator
    
    def execute_with_fallback(self, primary_func: Callable,
                             fallback_func: Callable = None,
                             *args, **kwargs) -> Any:
        """
        执行带降级的函数
        
        Args:
            primary_func: 主函数
            fallback_func: 降级函数（可选）
            *args, **kwargs: 函数参数
            
        Returns:
            主函数或降级函数的返回值
        """
        try:
            return primary_func(*args, **kwargs)
        except Exception as e:
            print(f"[FallbackHandler] 主函数失败: {e}")
            
            # 检查是否有注册的降级处理器
            for exc_type, handler in self.fallback_registry.items():
                if isinstance(e, exc_type):
                    print(f"[FallbackHandler] 使用注册的降级处理器")
                    return handler(*args, **kwargs)
            
            # 使用传入的降级函数
            if fallback_func:
                print(f"[FallbackHandler] 使用传入的降级函数")
                return fallback_func(*args, **kwargs)
            
            # 没有降级处理器，重新抛出异常
            raise


# 与 clawhub-retry-fallback 集成的适配器
class ClawhubRetryIntegration:
    """
    ClawHub 重降 Skill 集成适配器
    检测并重定向到 clawhub-retry-fallback
    """
    
    def __init__(self):
        self.retry_fallback_available = self._check_retry_fallback()
    
    def _check_retry_fallback(self) -> bool:
        """检查 clawhub-retry-fallback 是否可用"""
        try:
            # 检查是否存在重降 Skill
            retry_skill_path = Path(__file__).parent.parent.parent / "clawhub-retry-fallback"
            return retry_skill_path.exists()
        except:
            return False
    
    def get_retry_handler(self) -> Any:
        """获取重试处理器"""
        if self.retry_fallback_available:
            try:
                import sys
                sys.path.insert(0, str(Path(__file__).parent.parent.parent / "clawhub-retry-fallback" / "scripts"))
                from retry_handler import RetryHandler
                return RetryHandler()
            except Exception as e:
                print(f"[ClawhubRetryIntegration] 导入重降 Skill 失败: {e}")
        
        # 返回本地适配器
        return RetryAdapter()


# 便捷函数
def with_retry(max_attempts: int = 3, 
               strategy: RetryStrategy = RetryStrategy.EXPONENTIAL):
    """便捷装饰器"""
    adapter = RetryAdapter(RetryConfig(
        max_attempts=max_attempts,
        strategy=strategy
    ))
    return adapter.with_retry
