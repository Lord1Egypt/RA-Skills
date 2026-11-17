"""加载并校验 adapters.yaml / workspaces.yaml / stacks.yaml，合并环境变量。"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

_ENV_VAR_RE = re.compile(r"\$\{([^}]+)\}")

CONFIG_DIR = Path(__file__).parent.parent / "config"


def _expand_env(value: Any) -> Any:
    """递归将 ${VAR} 占位符替换为环境变量值。"""
    if isinstance(value, str):
        return _ENV_VAR_RE.sub(lambda m: os.environ.get(m.group(1), ""), value)
    if isinstance(value, dict):
        return {k: _expand_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand_env(i) for i in value]
    return value


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return _expand_env(data)


# ── Pydantic 模型 ──────────────────────────────────────────────────────────────

class WorkspaceConfig(BaseModel):
    id: str
    name: str
    path: str
    stack: str = "auto"                       # auto / dotnet / ...
    git_repo: str = ""                        # 留空则等于 path
    preferred_agent: str = ""                 # 对应 adapters.yaml 的 key
    fallback_agent: str = ""
    database_change_mode: str = "migration_first"
    environment: str = "test"                 # test / prod，决定权限策略
    # .NET / EF Core
    ef_project: str = ""
    ef_startup_project: str = ""
    db_context: str = ""
    test_db_connection: str = ""              # 测试库连接串；禁止填生产库
    # 命令覆盖（留空则用 stacks.yaml 默认）
    test_command: str = ""
    build_command: str = ""

    @property
    def repo_path(self) -> str:
        return self.git_repo or self.path


# ── ConfigLoader ──────────────────────────────────────────────────────────────

class ConfigLoader:
    def __init__(self, config_dir: Path = CONFIG_DIR) -> None:
        self._config_dir = config_dir
        self._workspaces: dict[str, WorkspaceConfig] = {}
        self._adapters: dict[str, Any] = {}
        self._stacks: dict[str, Any] = {}
        self._loaded = False

    def load(self) -> None:
        ws_data = _load_yaml(self._config_dir / "workspaces.yaml")
        for raw in ws_data.get("workspaces", []):
            cfg = WorkspaceConfig.model_validate(raw)
            self._workspaces[cfg.id] = cfg

        self._adapters = _load_yaml(self._config_dir / "adapters.yaml").get("adapters", {})
        self._stacks = _load_yaml(self._config_dir / "stacks.yaml").get("stacks", {})
        self._loaded = True

    def _ensure_loaded(self) -> None:
        if not self._loaded:
            self.load()

    # ── workspaces ──
    def get_workspace(self, workspace_id: str) -> WorkspaceConfig:
        self._ensure_loaded()
        if workspace_id not in self._workspaces:
            raise KeyError(f"工作区 '{workspace_id}' 不在 workspaces.yaml 中")
        return self._workspaces[workspace_id]

    def list_workspaces(self) -> list[WorkspaceConfig]:
        self._ensure_loaded()
        return list(self._workspaces.values())

    # ── adapters ──
    def get_adapters_config(self) -> dict[str, dict]:
        self._ensure_loaded()
        return self._adapters

    def get_adapter_config(self, name: str) -> dict:
        self._ensure_loaded()
        return self._adapters.get(name, {})

    # ── stacks ──
    def get_stack_config(self, stack: str) -> dict:
        self._ensure_loaded()
        return self._stacks.get(stack, {})

    def all_stacks(self) -> dict[str, dict]:
        self._ensure_loaded()
        return self._stacks
