#!/usr/bin/env python3
"""Shared helpers for NBA_TR tools."""

from __future__ import annotations


class NBAReportError(RuntimeError):
    """Raised when fetching or rendering NBA report data fails."""

    def __init__(self, message: str, *, status: int | None = None, kind: str = "request_failed") -> None:
        super().__init__(message)
        self.status = status
        self.kind = kind
