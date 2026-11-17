"""KingDoc 自定义异常"""


class KingDocError(Exception):
    """基础异常"""
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class AuthError(KingDocError):
    """鉴权失败"""
    def __init__(self, message: str = "Token 鉴权失败"):
        super().__init__("KD001", message)


class PermissionError(KingDocError):
    """权限不足"""
    def __init__(self, message: str = "权限不足"):
        super().__init__("KD002", message)


class QuotaError(KingDocError):
    """配额不足"""
    def __init__(self, message: str = "API 配额不足"):
        super().__init__("KD003", message)


class DocTypeError(KingDocError):
    """文档类型不匹配"""
    def __init__(self, message: str = "文档类型不匹配"):
        super().__init__("KD004", message)


class DocNotFoundError(KingDocError):
    """文档不存在"""
    def __init__(self, message: str = "文档不存在"):
        super().__init__("KD005", message)


class RateLimitError(KingDocError):
    """限流"""
    def __init__(self, retry_after: int = 60):
        self.retry_after = retry_after
        super().__init__("KD006", f"请求过于频繁，{retry_after}秒后重试")


class VersionConflictError(KingDocError):
    """版本冲突"""
    def __init__(self, message: str = "文档版本冲突"):
        super().__init__("KD007", message)


class FileTooLargeError(KingDocError):
    """文件过大"""
    def __init__(self, max_size: str = "100MB"):
        super().__init__("KD008", f"文件大小超过限制 ({max_size})")


class FileTypeBlockedError(KingDocError):
    """文件类型被拦截"""
    def __init__(self, ext: str = ""):
        super().__init__("KD009", f"文件类型被拦截: {ext or '未知类型'}")


class ServiceUnavailableError(KingDocError):
    """服务不可用"""
    def __init__(self, message: str = "服务暂时不可用"):
        super().__init__("KD010", message)


class ParamError(KingDocError):
    """参数错误"""
    def __init__(self, message: str = "请求参数错误"):
        super().__init__("KD011", message)


# 错误码映射
ERROR_MAP = {
    401: AuthError,
    402: QuotaError,
    403: PermissionError,
    404: DocNotFoundError,
    409: VersionConflictError,
    413: FileTooLargeError,
    429: RateLimitError,
    500: ServiceUnavailableError,
    503: ServiceUnavailableError,
}
