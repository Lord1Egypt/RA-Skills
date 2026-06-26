"""Application error taxonomy."""

from __future__ import annotations

from enum import StrEnum


class ErrorCode(StrEnum):
    PROXY_UNREACHABLE = "PROXY_UNREACHABLE"
    TARGET_TIMEOUT = "TARGET_TIMEOUT"
    RATE_LIMITED = "RATE_LIMITED"
    COOKIE_EXPIRED = "COOKIE_EXPIRED"
    PARSING_FAILED = "PARSING_FAILED"
    NO_RESULT = "NO_RESULT"
    PLATFORM_BLOCKED = "PLATFORM_BLOCKED"


class AppError(Exception):
    def __init__(self, code: ErrorCode, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code.value}: {message}")


class ProviderError(AppError):
    pass


def user_error_message(exc: Exception) -> str:
    if isinstance(exc, AppError):
        return f"{exc.code.value}: {exc.message}"
    return f"{ErrorCode.PARSING_FAILED.value}: {exc}"
