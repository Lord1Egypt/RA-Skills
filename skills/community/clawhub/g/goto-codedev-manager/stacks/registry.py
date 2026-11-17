"""技术栈名称 → 适配器实例 的工厂。新增栈在此登记。"""

from __future__ import annotations

from typing import TYPE_CHECKING

from executor.local_executor import LocalExecutor
from stacks.base import StackAdapterBase
from stacks.dotnet.efcore import EfCoreStackAdapter

if TYPE_CHECKING:
    from core.config_loader import ConfigLoader, WorkspaceConfig

_STACK_REGISTRY: dict[str, type[StackAdapterBase]] = {
    "dotnet": EfCoreStackAdapter,
}


def get_stack_adapter(
    stack: str, config: "ConfigLoader", executor: LocalExecutor | None = None
) -> StackAdapterBase:
    cls = _STACK_REGISTRY.get(stack)
    if cls is None:
        raise ValueError(f"暂不支持的技术栈：'{stack}'（已支持：{', '.join(_STACK_REGISTRY)}）")
    return cls(stack_config=config.get_stack_config(stack), executor=executor or LocalExecutor())


def resolve_stack(ws: "WorkspaceConfig", config: "ConfigLoader", executor: LocalExecutor | None = None) -> StackAdapterBase:
    """ws.stack=auto 时按各栈 detect() 自动判定，否则用显式 stack。"""
    if ws.stack and ws.stack != "auto":
        return get_stack_adapter(ws.stack, config, executor)
    for name in _STACK_REGISTRY:
        adapter = get_stack_adapter(name, config, executor)
        if adapter.detect(ws):
            return adapter
    raise ValueError(f"无法自动识别工作区 '{ws.id}' 的技术栈，请在 workspaces.yaml 显式设置 stack")
