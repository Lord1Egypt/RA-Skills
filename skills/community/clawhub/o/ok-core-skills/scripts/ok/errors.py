"""OK.com 异常体系"""


class OKError(Exception):
    """OK.com 自动化基础异常"""


class OKBridgeError(OKError):
    """Bridge 通信相关错误"""


class OKNotLoggedIn(OKError):
    """未登录错误"""


class OKTimeout(OKError):
    """操作超时"""


class OKElementNotFound(OKError):
    """页面元素未找到"""


class OKLocaleError(OKError):
    """Locale（国家/城市/语言）相关错误"""


class OKAPIError(OKError):
    """API 调用错误"""

    def __init__(self, message: str, response_code: int | None = None):
        super().__init__(message)
        self.response_code = response_code
