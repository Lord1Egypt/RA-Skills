"""Unified error contracts and exit-code mapping."""

from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from hkipo_next.contracts.common import ResponseMeta


class ErrorCode(str, Enum):
    E_ARG = "E_ARG"
    E_SOURCE = "E_SOURCE"
    E_RULE = "E_RULE"
    E_SYSTEM = "E_SYSTEM"


ERROR_EXIT_CODES = {
    ErrorCode.E_ARG: 2,
    ErrorCode.E_SOURCE: 10,
    ErrorCode.E_RULE: 20,
    ErrorCode.E_SYSTEM: 30,
}


class AppError(BaseModel):
    """Structured application error."""

    model_config = ConfigDict(extra="forbid")

    code: ErrorCode
    message: str
    details: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def arg(cls, message: str, *, details: dict[str, Any] | None = None) -> "AppError":
        return cls(code=ErrorCode.E_ARG, message=message, details=details or {})

    @classmethod
    def source(cls, message: str, *, details: dict[str, Any] | None = None) -> "AppError":
        return cls(code=ErrorCode.E_SOURCE, message=message, details=details or {})

    @classmethod
    def rule(cls, message: str, *, details: dict[str, Any] | None = None) -> "AppError":
        return cls(code=ErrorCode.E_RULE, message=message, details=details or {})

    @classmethod
    def system(cls, message: str, *, details: dict[str, Any] | None = None) -> "AppError":
        return cls(code=ErrorCode.E_SYSTEM, message=message, details=details or {})


class ErrorResponse(BaseModel):
    """Standard top-level error envelope."""

    model_config = ConfigDict(extra="forbid")

    ok: Literal[False] = False
    error: AppError
    meta: ResponseMeta


class AppException(Exception):
    """Raised when a command should render a structured error."""

    def __init__(self, error: AppError):
        super().__init__(error.message)
        self.error = error


def build_error_response(error: AppError, meta: ResponseMeta) -> ErrorResponse:
    return ErrorResponse(error=error, meta=meta)


def exit_code_for(error_code: ErrorCode) -> int:
    return ERROR_EXIT_CODES[error_code]
