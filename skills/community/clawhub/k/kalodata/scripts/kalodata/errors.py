"""Error types shared across the CLI.

Errors are structured output on stdout, with actionable suggestions,
and exit codes 0 (success/no-op), 1 (error), 2 (usage error).
"""

from __future__ import annotations


class UsageError(Exception):
    """Bad invocation (unknown flag, invalid value, missing argument). Exit 2."""

    def __init__(self, message: str, help_lines: list[str] | None = None):
        super().__init__(message)
        self.help_lines = help_lines or []


class KaloError(Exception):
    """Runtime failure (auth, membership, upstream, network). Exit 1.

    kind: auth | membership | parameter | network | api
    """

    def __init__(self, message: str, kind: str = "api", help_lines: list[str] | None = None):
        super().__init__(message)
        self.kind = kind
        self.help_lines = help_lines or []
