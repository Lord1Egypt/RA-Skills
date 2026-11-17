"""按 workspace 首选/回退 + adapters.yaml 优先级与可用性，挑选编程 Agent 适配器。

选择顺序（设计思路第三/五节）：
1. 显式 agent 参数（用户指定）
2. workspace.preferred_agent（若 enabled 且 is_available）
3. workspace.fallback_agent（同上）
4. adapters.yaml 中 enabled 的适配器按 priority 升序，第一个 is_available 的
5. 最终回落 generic/workspace_adapter（永远可用）
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import structlog

from adapters.base import CodingAgentAdapter
from adapters.claude_code.claude_cli_adapter import ClaudeCliAdapter
from adapters.codex.codex_cli_adapter import CodexCliAdapter
from adapters.cursor.cursor_workspace_adapter import CursorWorkspaceAdapter
from adapters.generic.cli_agent_adapter import CliAgentAdapter
from adapters.generic.configured_cli_adapter import ConfiguredCliAdapter
from adapters.generic.workspace_adapter import WorkspaceAdapter
from adapters.lingma.lingma_workspace_adapter import LingmaWorkspaceAdapter
from adapters.qoer.qoer_cli_adapter import QoerCliAdapter
from adapters.qoder.qoder_workspace_adapter import QoderWorkspaceAdapter
from adapters.trae.trae_cli_adapter import TraeCliAdapter
from adapters.vscode.vscode_tasks_adapter import VscodeTasksAdapter

if TYPE_CHECKING:
    from core.config_loader import ConfigLoader, WorkspaceConfig
    from executor.base import ExecutorBase

logger = structlog.get_logger(__name__)

# 适配器名称 → 实现类
_REGISTRY: dict[str, type[CodingAgentAdapter]] = {
    "codex": CodexCliAdapter,
    "claude_code": ClaudeCliAdapter,
    "vscode": VscodeTasksAdapter,
    "trae": TraeCliAdapter,
    "cursor": CursorWorkspaceAdapter,
    "qoer": QoerCliAdapter,
    "lingma": LingmaWorkspaceAdapter,
    "qoder": QoderWorkspaceAdapter,
    "generic_cli": CliAgentAdapter,
    "generic": WorkspaceAdapter,
}


class AdapterSelector:
    def __init__(self, config: "ConfigLoader", executor: "ExecutorBase | None" = None) -> None:
        self._config = config
        self._executor = executor

    def _build(self, name: str) -> CodingAgentAdapter | None:
        cfg = self._config.get_adapter_config(name)
        cls = _REGISTRY.get(name)
        if cls is not None:
            return cls(config=cfg, executor=self._executor)

        if cfg.get("type") in ("cli", "ide_cli") and cfg.get("command"):
            return ConfiguredCliAdapter(config=cfg, executor=self._executor, adapter_name=name)
        if cfg.get("type") == "workspace":
            return WorkspaceAdapter(config=cfg, executor=self._executor)
        return None

    def _enabled_and_available(self, name: str) -> CodingAgentAdapter | None:
        cfg = self._config.get_adapter_config(name)
        if not cfg.get("enabled", False) and name not in ("generic",):
            return None
        adapter = self._build(name)
        if adapter and adapter.is_available():
            return adapter
        return None

    def list_available(self) -> list[dict]:
        """供 list_adapters 动作使用：返回各适配器启用/可用状态与优先级。"""
        out: list[dict] = []
        for name, cfg in self._config.get_adapters_config().items():
            adapter = self._build(name)
            out.append({
                "name": name,
                "type": cfg.get("type", ""),
                "enabled": cfg.get("enabled", False),
                "available": bool(adapter and adapter.is_available()),
                "priority": cfg.get("priority", 999),
            })
        return sorted(out, key=lambda d: d["priority"])

    def select(self, ws: "WorkspaceConfig", agent: str | None = None) -> CodingAgentAdapter:
        # 1. 显式指定
        if agent:
            adapter = self._build(agent)
            if adapter is None:
                raise ValueError(f"未知适配器：'{agent}'")
            logger.info("adapter_selected", reason="explicit", adapter=agent,
                        available=adapter.is_available())
            return adapter

        # 2/3. workspace 首选 / 回退
        for candidate, reason in ((ws.preferred_agent, "preferred"), (ws.fallback_agent, "fallback")):
            if candidate:
                adapter = self._enabled_and_available(candidate)
                if adapter:
                    logger.info("adapter_selected", reason=reason, adapter=candidate)
                    return adapter

        # 4. 按 priority 升序找第一个可用
        for entry in self.list_available():
            if entry["available"] and entry["enabled"]:
                adapter = self._build(entry["name"])
                if adapter:
                    logger.info("adapter_selected", reason="priority", adapter=entry["name"])
                    return adapter

        # 5. 兜底
        logger.info("adapter_selected", reason="fallback_generic", adapter="generic")
        return WorkspaceAdapter(config=self._config.get_adapter_config("generic"), executor=self._executor)
