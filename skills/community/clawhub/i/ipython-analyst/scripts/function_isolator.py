"""
function_isolator.py — Run a function with mocked dependencies.

Useful for testing a function in isolation when its dependencies (filesystem,
external modules, environment variables) are unavailable or would have side
effects. Especially handy for debugging "this works on my machine" issues
where the difference is env or filesystem state.
"""
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any, Callable
from unittest.mock import MagicMock, patch


class FunctionIsolator:
    """Execute functions with mocked dependencies.

    Set up mocks for modules, files, and env vars, then call your function
    inside the isolator's context. All mocks are reverted on exit.
    """

    def __init__(self):
        self._module_mocks: dict[str, Any] = {}
        self._file_mocks: dict[str, Any] = {}
        self._original_env: dict[str, str | None] = {}

    def mock_module(self, name: str, obj: Any = None, **attrs) -> None:
        """Mock a module path (e.g. 'requests.get') with a MagicMock or custom obj."""
        if obj is None:
            obj = MagicMock()
        for k, v in attrs.items():
            setattr(obj, k, v)
        self._module_mocks[name] = obj

    def mock_file(self, path: str, content: str) -> None:
        """Mock `open(path)` to return a file-like object yielding `content`."""
        mock = MagicMock()
        mock.__enter__ = MagicMock(return_value=mock)
        mock.__exit__ = MagicMock(return_value=False)
        mock.read.return_value = content
        mock.write.return_value = len(content)
        self._file_mocks[path] = mock

    def mock_env(self, env_vars: dict[str, str]) -> None:
        """Set environment variables for the duration of the next context."""
        for k, v in env_vars.items():
            self._original_env[k] = os.environ.get(k)
            os.environ[k] = v

    @contextmanager
    def context(self):
        """Apply all registered mocks for the duration of the with-block."""
        patches = []
        try:
            # Patch module attributes
            for name, mock in self._module_mocks.items():
                p = patch(name, mock)
                p.start()
                patches.append(p)

            # Patch builtins.open to handle mocked file paths
            if self._file_mocks:
                real_open = open
                def patched_open(path, *args, **kwargs):
                    # Normalize path for lookup
                    key = str(path)
                    if key in self._file_mocks:
                        return self._file_mocks[key]
                    return real_open(path, *args, **kwargs)
                p = patch("builtins.open", side_effect=patched_open)
                p.start()
                patches.append(p)

            yield self

        finally:
            for p in patches:
                p.stop()
            # Restore env
            for k, original in self._original_env.items():
                if original is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = original
            self._original_env.clear()

    def run(self, func: Callable, *args, **kwargs) -> dict[str, Any]:
        """Run `func` inside the isolation context. Returns {result, error}."""
        with self.context():
            try:
                return {"result": func(*args, **kwargs), "error": None}
            except Exception as e:
                return {"result": None, "error": e}


__all__ = ["FunctionIsolator"]
