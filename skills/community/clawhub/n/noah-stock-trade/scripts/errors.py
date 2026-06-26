class TradeCliError(Exception):
    def __init__(
        self,
        message,
        hint=None,
        endpoint=None,
        http_status=None,
        biz_code=None,
        trace_id=None,
        retryable=False,
    ):
        super().__init__(message)
        self.message = message
        self.hint = hint
        self.endpoint = endpoint
        self.http_status = http_status
        self.biz_code = biz_code
        self.trace_id = trace_id
        self.retryable = retryable


class ConfigError(TradeCliError):
    pass


class ValidationError(TradeCliError):
    pass


class TradeApiError(TradeCliError):
    pass


class TradeBizError(TradeCliError):
    pass


class ReadOnlyViolation(TradeCliError):
    pass
