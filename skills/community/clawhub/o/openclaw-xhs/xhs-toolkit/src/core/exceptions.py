"""
小红书工具包统一异常处理模块

定义自定义异常类，实现统一的错误处理机制
"""

from typing import Optional, Dict, Any, Callable
from functools import wraps
from ..utils.logger import get_logger

logger = get_logger(__name__)


class XHSToolkitError(Exception):
    """小红书工具包基础异常类"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """将异常转换为字典格式，便于日志记录和API返回"""
        return {
            "error": True,
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details
        }


class ConfigurationError(XHSToolkitError):
    """配置相关错误"""
    
    def __init__(self, message: str, config_item: Optional[str] = None):
        super().__init__(message, "CONFIG_ERROR", {"config_item": config_item})


class BrowserError(XHSToolkitError):
    """浏览器相关错误"""
    
    def __init__(self, message: str, browser_action: Optional[str] = None):
        super().__init__(message, "BROWSER_ERROR", {"browser_action": browser_action})


class AuthenticationError(XHSToolkitError):
    """认证相关错误"""
    
    def __init__(self, message: str, auth_type: Optional[str] = None):
        super().__init__(message, "AUTH_ERROR", {"auth_type": auth_type})


class PublishError(XHSToolkitError):
    """发布相关错误"""
    
    def __init__(self, message: str, publish_step: Optional[str] = None):
        super().__init__(message, "PUBLISH_ERROR", {"publish_step": publish_step})


class NetworkError(XHSToolkitError):
    """网络相关错误"""
    
    def __init__(self, message: str, url: Optional[str] = None, status_code: Optional[int] = None):
        super().__init__(message, "NETWORK_ERROR", {"url": url, "status_code": status_code})


class ValidationError(XHSToolkitError):
    """数据验证错误"""
    
    def __init__(self, message: str, field_name: Optional[str] = None, field_value: Optional[Any] = None):
        super().__init__(message, "VALIDATION_ERROR", {"field_name": field_name, "field_value": field_value})


def handle_exception(func: Callable) -> Callable:
    """
    异常处理装饰器
    
    用于统一处理函数/方法中的异常
    """
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except XHSToolkitError:
            # 已知的工具包异常，直接重新抛出
            raise
        except Exception as e:
            # 未知异常，包装为工具包异常
            logger.error(f"未处理的异常 in {func.__name__}: {str(e)}")
            raise XHSToolkitError(f"执行 {func.__name__} 时发生未知错误: {str(e)}") from e
    
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except XHSToolkitError:
            # 已知的工具包异常，直接重新抛出
            raise
        except Exception as e:
            # 未知异常，包装为工具包异常
            logger.error(f"未处理的异常 in {func.__name__}: {str(e)}")
            raise XHSToolkitError(f"执行 {func.__name__} 时发生未知错误: {str(e)}") from e
    
    # 根据函数是否为协程选择不同的包装器
    import asyncio
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


def format_error_message(error: XHSToolkitError) -> str:
    """
    格式化错误消息，用于用户友好的错误显示
    
    Args:
        error: 工具包异常实例
        
    Returns:
        格式化后的错误消息
    """
    base_message = error.message
    
    # 根据错误类型提供建议
    suggestions = {
        "CONFIG_ERROR": "请检查环境变量配置或.env文件",
        "BROWSER_ERROR": "请检查Chrome浏览器和ChromeDriver的配置",
        "AUTH_ERROR": "请检查登录状态或重新获取cookies",
        "PUBLISH_ERROR": "请检查发布内容格式或重试发布",
        "NETWORK_ERROR": "请检查网络连接或稍后重试",
        "VALIDATION_ERROR": "请检查输入数据格式是否正确"
    }
    
    suggestion = suggestions.get(error.error_code, "请查看详细错误信息或联系支持")
    
    return f"{base_message}\n💡 建议: {suggestion}"


class ErrorHandler:
    """错误处理器类"""
    
    def __init__(self):
        self.error_count = 0
        self.last_error = None
    
    def handle_error(self, error: Exception) -> None:
        """
        处理错误
        
        Args:
            error: 异常实例
        """
        self.error_count += 1
        self.last_error = error
        
        if isinstance(error, XHSToolkitError):
            logger.error(f"❌ {error.error_code}: {error.message}")
            if error.details:
                logger.debug(f"错误详情: {error.details}")
        else:
            logger.error(f"❌ 未知错误: {str(error)}")
    
    def reset_error_count(self) -> None:
        """重置错误计数"""
        self.error_count = 0
        self.last_error = None
    
    def has_errors(self) -> bool:
        """是否有错误"""
        return self.error_count > 0
    
    def get_error_summary(self) -> Dict[str, Any]:
        """获取错误摘要"""
        return {
            "error_count": self.error_count,
            "last_error": str(self.last_error) if self.last_error else None,
            "last_error_type": type(self.last_error).__name__ if self.last_error else None
        } 