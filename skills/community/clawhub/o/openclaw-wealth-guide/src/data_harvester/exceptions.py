"""
异常处理模块
定义数据采集器相关的异常类
"""


class DataHarvesterError(Exception):
    """数据采集器基础异常"""
    pass


class ConfigurationError(DataHarvesterError):
    """配置错误异常"""
    pass


class AdapterError(DataHarvesterError):
    """适配器错误异常"""
    pass


class FetchError(AdapterError):
    """数据获取错误异常"""
    pass


class ProcessingError(DataHarvesterError):
    """数据处理错误异常"""
    pass


class ExportError(DataHarvesterError):
    """数据导出错误异常"""
    pass


class SchedulerError(DataHarvesterError):
    """调度器错误异常"""
    pass


class ValidationError(DataHarvesterError):
    """数据验证错误异常"""
    pass


class PluginError(DataHarvesterError):
    """插件错误异常"""
    pass


class ResourceError(DataHarvesterError):
    """资源错误异常（如文件不存在、网络连接失败等）"""
    pass


class AuthenticationError(DataHarvesterError):
    """认证错误异常"""
    pass


class RateLimitError(DataHarvesterError):
    """速率限制错误异常"""
    pass


class TimeoutError(DataHarvesterError):
    """超时错误异常"""
    pass


class RetryExhaustedError(DataHarvesterError):
    """重试耗尽错误异常"""
    def __init__(self, message: str, last_exception: Exception = None):
        super().__init__(message)
        self.last_exception = last_exception


class DataQualityError(DataHarvesterError):
    """数据质量错误异常"""
    def __init__(self, message: str, quality_score: float = 0.0):
        super().__init__(message)
        self.quality_score = quality_score


class IntegrationError(DataHarvesterError):
    """集成错误异常（如OpenClaw集成失败）"""
    pass