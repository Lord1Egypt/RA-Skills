"""Late-bound access to server runtime helpers.

Late binding keeps legacy ``server._get``/``server._post`` monkeypatches working
after tool implementations move into domain modules.
"""

from collections.abc import Callable
from typing import Any


class RuntimeCallable:
    def __init__(self, runtime_globals: dict[str, Any], name: str) -> None:
        self._runtime_globals = runtime_globals
        self._name = name

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        target: Callable[..., Any] = self._runtime_globals[self._name]
        return target(*args, **kwargs)


def bind_runtime(
    module_globals: dict[str, Any],
    runtime_globals: dict[str, Any],
    dependencies: tuple[str, ...],
) -> None:
    for name in dependencies:
        value = runtime_globals[name]
        module_globals[name] = RuntimeCallable(runtime_globals, name) if callable(value) else value
