"""加载并校验 servers.yaml / providers.yaml / credentials.yaml，合并环境变量。"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, field_validator

load_dotenv()

_ENV_VAR_RE = re.compile(r"\$\{([^}]+)\}")

CONFIG_DIR = Path(__file__).parent.parent / "config"


def _expand_env(value: Any) -> Any:
    """递归将 ${VAR} 占位符替换为环境变量值。"""
    if isinstance(value, str):
        def _replace(m: re.Match) -> str:
            env_val = os.environ.get(m.group(1), "")
            return env_val
        return _ENV_VAR_RE.sub(_replace, value)
    if isinstance(value, dict):
        return {k: _expand_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand_env(i) for i in value]
    return value


def _load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return _expand_env(data)


# ── Pydantic 模型 ──────────────────────────────────────────────────────────────

class SshConnection(BaseModel):
    port: int = 22
    username: str = "root"
    key_path: str = "~/.ssh/id_rsa"
    password: str = ""


class WinrmConnection(BaseModel):
    port: int = 5986
    use_ssl: bool = True
    username: str = "Administrator"
    password: str = ""


class ConnectionConfig(BaseModel):
    type: str                            # cloud_assistant / tat / ssh / winrm
    fallback: str = ""
    ssh: SshConnection = SshConnection()
    winrm: WinrmConnection = WinrmConnection()


class DatabaseConfig(BaseModel):
    type: str                            # sqlserver / mysql / postgresql / redis
    version: str = ""
    port: int = 0


class ServerConfig(BaseModel):
    id: str
    name: str
    provider: str                        # aliyun / tencent / tencent-lighthouse / huawei
    region: str
    instance_id: str
    os_type: str                         # windows / linux
    os_version: str
    connection: ConnectionConfig
    role: list[str] = []
    databases: list[DatabaseConfig] = []
    environment: str = "test"
    tags: dict[str, str] = {}
    public_ip: str = ""                  # SSH/WinRM 兜底连接用；留空时由 dispatcher 实时查云厂商 API 补全
    private_ip: str = ""

    @field_validator("provider")
    @classmethod
    def _valid_provider(cls, v: str) -> str:
        allowed = {"aliyun", "tencent", "tencent-lighthouse", "huawei"}
        if v not in allowed:
            raise ValueError(f"provider must be one of {allowed}, got '{v}'")
        return v

    @field_validator("os_type")
    @classmethod
    def _valid_os_type(cls, v: str) -> str:
        if v not in {"windows", "linux"}:
            raise ValueError(f"os_type must be 'windows' or 'linux', got '{v}'")
        return v


# ── ConfigLoader ──────────────────────────────────────────────────────────────

class ConfigLoader:
    def __init__(self, config_dir: Path = CONFIG_DIR) -> None:
        self._config_dir = config_dir
        self._servers: dict[str, ServerConfig] = {}
        self._providers: dict[str, Any] = {}
        self._credentials: dict[str, Any] = {}
        self._loaded = False

    def load(self) -> None:
        servers_data = _load_yaml(self._config_dir / "servers.yaml")
        for raw in servers_data.get("servers", []):
            cfg = ServerConfig.model_validate(raw)
            self._servers[cfg.id] = cfg

        self._providers = _load_yaml(self._config_dir / "providers.yaml").get("providers", {})

        cred_path = self._config_dir / "credentials.yaml"
        if cred_path.exists():
            self._credentials = _load_yaml(cred_path)

        self._loaded = True

    def _ensure_loaded(self) -> None:
        if not self._loaded:
            self.load()

    def get_server(self, server_id: str) -> ServerConfig:
        self._ensure_loaded()
        if server_id not in self._servers:
            raise KeyError(f"Server '{server_id}' not found in servers.yaml")
        return self._servers[server_id]

    def list_servers(self, environment: str | None = None, provider: str | None = None) -> list[ServerConfig]:
        self._ensure_loaded()
        servers = list(self._servers.values())
        if environment:
            servers = [s for s in servers if s.environment == environment]
        if provider:
            servers = [s for s in servers if s.provider == provider]
        return servers

    def get_provider_config(self, provider: str) -> dict:
        self._ensure_loaded()
        if provider not in self._providers:
            raise KeyError(f"Provider '{provider}' not found in providers.yaml")
        return self._providers[provider]

    def get_server_credentials(self, server_id: str) -> dict:
        self._ensure_loaded()
        return self._credentials.get("servers", {}).get(server_id, {})

    def get_provider_credentials(self, provider: str) -> dict:
        self._ensure_loaded()
        env_creds = self._credentials.get("providers", {}).get(provider, {})
        # 环境变量优先级更高，已在 providers.yaml 中通过 ${VAR} 展开
        provider_cfg = self._providers.get(provider, {})
        auth = provider_cfg.get("auth", {})
        return {**env_creds, **auth}
