"""Shared errors for skill commands."""

from __future__ import annotations


class ScriptError(RuntimeError):
    """Expected command failure."""


class ParamError(ScriptError):
    """Invalid local command input."""


class ToolInstallRequiredError(ParamError):
    """A required local tool is missing and needs explicit user approval."""

    error_code = "tool_install_required"

    def __init__(self, message: str, *, tool: str, install_command: str) -> None:
        super().__init__(message)
        self.tool = tool
        self.install_command = install_command


class CredentialRequiredError(ParamError):
    """The user must configure an API key before calling the service."""

    def __init__(self, message: str, *, locale: str = "") -> None:
        super().__init__(message)
        self.locale = locale
