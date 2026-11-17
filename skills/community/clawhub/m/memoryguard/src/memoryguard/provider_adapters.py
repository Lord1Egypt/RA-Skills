"""Provider adapters: 把 Claude/Codex/Cursor 的原生记忆机制重定向到 MemoryGuard MCP。

每个 adapter 做 two things：
1. 写入宿主特定的指令文件，明确告诉 Agent 调用 memoryguard_memory_write MCP 工具记录记忆，
   不要用原生记忆机制（编辑 CLAUDE.md/AGENTS.md/.cursorrules 等）。
2. 生成/更新宿主的 MCP 配置，让它能启动 MemoryGuard MCP 服务器。

设计：
- install() 幂等：重复调用不产生重复配置（指令用标记段落替换，MCP 配置用 JSON key 覆盖）
- uninstall() 干净移除 install() 写入的内容（只动 memoryguard 段落/key，不碰用户其他内容）
- status() 返回 {installed: bool, instruction_file: str, mcp_configured: bool}
- 纯标准库，不引入新依赖
- 配置路径跨平台（Path.home() / 环境变量）
- MCP 启动命令用 python（要求 memoryguard 已 pip install），跨机器可移植
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


# ===========================================================================
# 常量
# ===========================================================================

MCP_SERVER_NAME = "memoryguard"
MCP_MODULE = "memoryguard.mcp_server"

# 指令文件中使用的标记（HTML 注释，Markdown/MDC 都安全）
_BEGIN_MARKER = "<!-- BEGIN memoryguard:provider-redirect -->"
_END_MARKER = "<!-- END memoryguard:provider-redirect -->"

# Codex TOML 配置使用的标记（# 注释）
_TOML_BEGIN = "# BEGIN memoryguard:provider-redirect"
_TOML_END = "# END memoryguard:provider-redirect"


# 共用指令正文：告诉 Agent 所有记忆操作走 MCP 工具
_INSTRUCTION_BODY = """\
## MemoryGuard 记忆重定向

当你需要记录或回忆任何长期记忆时，必须通过 MemoryGuard MCP 工具，不要使用原生记忆机制
（如编辑本指令文件、写入本地 memory.md/notes.md、或使用 GUI 记忆功能）。

### 记录记忆
调用 `memoryguard_memory_write` 工具：
- `body`（必填）：记忆内容
- `kind`（可选）：preference|fact|project|procedure|episode|correction，留空则自动分类
- `agent_instance_id`（可选）：你的 Agent 标识
- `share_group_id`（可选）：共享组 ID，默认 "default"

### 搜索 / 读取
- `memoryguard_memory_search`：按 query / kind / status 搜索
- `memoryguard_memory_read`：按 memory_id 读取单条
- `memoryguard_memory_status`：查看共享组状态

### 更新 / 删除
- `memoryguard_memory_update`：更新 body / kind / status
- `memoryguard_memory_delete`：软删除

### 规则
- 不要为了"记住"而编辑 CLAUDE.md / AGENTS.md / .cursorrules 等指令文件
- 不要把记忆写入本地文件
- 所有记忆操作都走 MCP 工具，确保被 MemoryGuard 治理（去重、冲突检测、隔离、影子保留）
"""


# ===========================================================================
# 工具函数
# ===========================================================================


def _mcp_command() -> list[str]:
    """返回启动 MemoryGuard MCP 服务器的 command + args。

    用 "python"（要求 memoryguard 已 pip install），跨机器可移植，
    避免 sys.executable 把机器特定路径写入 .mcp.json。
    """
    return ["python", "-m", MCP_MODULE]


def _mcp_server_config() -> dict[str, Any]:
    """返回 MemoryGuard MCP server 的配置片段（JSON 格式，Claude/Cursor 通用）。"""
    cmd = _mcp_command()
    return {
        "command": cmd[0],
        "args": cmd[1:],
    }


def _mcp_toml_section() -> str:
    """返回 MemoryGuard MCP server 的 TOML 配置段落（Codex 用）。

    用 json.dumps 产出合法的 TOML basic string（自动转义反斜杠）。
    """
    cmd = _mcp_command()
    command_str = json.dumps(cmd[0])  # TOML basic string 与 JSON string 语法兼容
    args_items = ", ".join(json.dumps(a) for a in cmd[1:])
    return (
        f"[mcp_servers.{MCP_SERVER_NAME}]\n"
        f"command = {command_str}\n"
        f"args = [{args_items}]"
    )


def _replace_section(text: str, begin_marker: str, end_marker: str,
                     section_content: str) -> str:
    """幂等替换标记之间的内容。标记不存在则追加新段落。"""
    begin_idx = text.find(begin_marker)
    end_idx = text.find(end_marker)
    if begin_idx != -1 and end_idx != -1 and end_idx > begin_idx:
        before = text[:begin_idx]
        after = text[end_idx + len(end_marker):]
        before = before.rstrip("\n")
        after = after.lstrip("\n")
        parts = []
        if before:
            parts.append(before + "\n\n")
        parts.append(f"{begin_marker}\n{section_content}\n{end_marker}")
        if after:
            parts.append("\n" + after)
        return "".join(parts)
    # 追加新段落
    stripped = text.rstrip()
    if stripped:
        return f"{stripped}\n\n{begin_marker}\n{section_content}\n{end_marker}\n"
    return f"{begin_marker}\n{section_content}\n{end_marker}\n"


def _remove_section(text: str, begin_marker: str, end_marker: str) -> str:
    """移除标记之间的内容，返回剩余文本。"""
    begin_idx = text.find(begin_marker)
    end_idx = text.find(end_marker)
    if begin_idx == -1 or end_idx == -1 or end_idx <= begin_idx:
        return text
    before = text[:begin_idx]
    after = text[end_idx + len(end_marker):]
    result = before + after
    while "\n\n\n" in result:
        result = result.replace("\n\n\n", "\n\n")
    if not result.strip():
        return ""
    return result.rstrip("\n") + "\n"


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def _save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _set_mcp_server(data: dict[str, Any], server_name: str, config: dict[str, Any]) -> None:
    data.setdefault("mcpServers", {})[server_name] = config


def _remove_mcp_server(data: dict[str, Any], server_name: str) -> bool:
    servers = data.get("mcpServers", {})
    if server_name in servers:
        del servers[server_name]
        if not servers:
            del data["mcpServers"]
        return True
    return False


def _has_mcp_server(data: dict[str, Any], server_name: str) -> bool:
    return server_name in data.get("mcpServers", {})


# ===========================================================================
# 基类
# ===========================================================================


class ProviderAdapter:
    """Provider adapter 基类契约。

    子类实现 install / uninstall / status，把宿主原生记忆重定向到 MemoryGuard MCP。
    遵循现有 adapters.py 的契约风格（raise NotImplementedError，不用 ABC）。
    """

    provider_name: str = "base"

    def _bind_with_store(self, redirect_paths: list[str]) -> str | None:
        """联动 AgentBindingStore 创建 binding。失败记 stderr 返回 None，不抛异常。"""
        try:
            from .agent_binding import AgentBindingStore
            from .schema_v3 import NativeMemoryMode
            store = AgentBindingStore(self.workspace)
            binding = store.bind_agent(
                agent_instance_id=self.provider_name,
                share_group_id="default",
                mcp_server_name=MCP_SERVER_NAME,
                native_memory_mode=NativeMemoryMode.REDIRECTED,
                redirect_paths=redirect_paths,
            )
            return binding.binding_id
        except Exception as e:
            print(f"memoryguard: bind_agent failed for {self.provider_name}: {e}", file=sys.stderr)
            return None

    def _unbind_with_store(self) -> str | None:
        """联动 AgentBindingStore 解绑该 provider 的 active binding。失败不抛异常。"""
        try:
            from .agent_binding import AgentBindingStore
            store = AgentBindingStore(self.workspace)
            bindings = store.find_by_agent(self.provider_name, include_inactive=False)
            if not bindings:
                return None
            binding_id = bindings[0].binding_id
            store.unbind_agent(binding_id)
            return binding_id
        except Exception as e:
            print(f"memoryguard: unbind_agent failed for {self.provider_name}: {e}", file=sys.stderr)
            return None

    def _find_binding(self) -> tuple[str | None, str | None]:
        """查找该 provider 的 active binding，返回 (binding_id, binding_status)。"""
        try:
            from .agent_binding import AgentBindingStore
            store = AgentBindingStore(self.workspace)
            bindings = store.find_by_agent(self.provider_name, include_inactive=False)
            if not bindings:
                return None, None
            b = bindings[0]
            return b.binding_id, b.status.value
        except Exception as e:
            print(f"memoryguard: find binding failed for {self.provider_name}: {e}", file=sys.stderr)
            return None, None

    def install(self, workspace: str | Path = "") -> dict[str, Any]:
        raise NotImplementedError

    def uninstall(self) -> dict[str, Any]:
        raise NotImplementedError

    def status(self) -> dict[str, Any]:
        raise NotImplementedError


# ===========================================================================
# ClaudeAdapter
# ===========================================================================


class ClaudeAdapter(ProviderAdapter):
    """Claude Code adapter。

    - 指令文件：<workspace>/CLAUDE.md（项目级）；无 workspace 时 ~/.claude/CLAUDE.md（用户级）
    - MCP 配置：<workspace>/.mcp.json（Claude Code 官方项目级 MCP 配置格式）
    - 支持环境变量 CLAUDE_CONFIG_DIR 覆盖 ~/.claude/
    """

    provider_name = "claude"

    def __init__(self, workspace: str | Path = ""):
        self._has_workspace = bool(workspace)
        self.workspace = Path(workspace).resolve() if workspace else Path.home()

    def _config_dir(self) -> Path:
        return Path(os.environ.get("CLAUDE_CONFIG_DIR", "")) or (Path.home() / ".claude")

    def _instruction_path(self) -> Path:
        if self._has_workspace:
            return self.workspace / "CLAUDE.md"
        return self._config_dir() / "CLAUDE.md"

    def _mcp_config_path(self) -> Path:
        return self.workspace / ".mcp.json"

    def install(self, workspace: str | Path = "") -> dict[str, Any]:
        if workspace:
            self._has_workspace = True
            self.workspace = Path(workspace).resolve()

        # 1. 写指令（标记段落，保留用户其他内容）
        instr_path = self._instruction_path()
        content = _read_text(instr_path)
        new_content = _replace_section(content, _BEGIN_MARKER, _END_MARKER, _INSTRUCTION_BODY)
        _write_text(instr_path, new_content)

        # 2. 写 MCP 配置（JSON merge，只动 memoryguard key）
        mcp_path = self._mcp_config_path()
        data = _load_json(mcp_path)
        _set_mcp_server(data, MCP_SERVER_NAME, _mcp_server_config())
        _save_json(mcp_path, data)

        return {
            "provider": self.provider_name,
            "installed": True,
            "instruction_file": str(instr_path),
            "mcp_config_file": str(mcp_path),
            "binding_id": self._bind_with_store([str(instr_path), str(mcp_path)]),
        }

    def uninstall(self) -> dict[str, Any]:
        instr_path = self._instruction_path()

        # 1. 移除指令段落
        content = _read_text(instr_path)
        if _BEGIN_MARKER in content:
            new_content = _remove_section(content, _BEGIN_MARKER, _END_MARKER)
            if new_content.strip():
                _write_text(instr_path, new_content)
            else:
                try:
                    instr_path.unlink()
                except OSError:
                    pass

        # 2. 移除 MCP 配置中的 memoryguard key
        mcp_path = self._mcp_config_path()
        data = _load_json(mcp_path)
        _remove_mcp_server(data, MCP_SERVER_NAME)
        if data:
            _save_json(mcp_path, data)
        else:
            try:
                mcp_path.unlink()
            except OSError:
                pass

        return {
            "provider": self.provider_name,
            "installed": False,
            "instruction_file": str(instr_path),
            "mcp_config_file": str(mcp_path),
            "binding_id": self._unbind_with_store(),
        }

    def status(self) -> dict[str, Any]:
        instr_path = self._instruction_path()
        mcp_path = self._mcp_config_path()

        content = _read_text(instr_path)
        instruction_installed = _BEGIN_MARKER in content and _END_MARKER in content

        data = _load_json(mcp_path)
        mcp_configured = _has_mcp_server(data, MCP_SERVER_NAME)

        binding_id, binding_status = self._find_binding()
        return {
            "installed": instruction_installed and mcp_configured,
            "instruction_file": str(instr_path),
            "mcp_configured": mcp_configured,
            "binding_id": binding_id,
            "binding_status": binding_status,
        }


# ===========================================================================
# CodexAdapter
# ===========================================================================


class CodexAdapter(ProviderAdapter):
    """Codex CLI adapter。

    - 指令文件：<workspace>/AGENTS.md（项目级）；无 workspace 时 ~/.codex/AGENTS.md
    - MCP 配置：~/.codex/config.toml（用户级，TOML 格式）
      段落：[mcp_servers.memoryguard]
    """

    provider_name = "codex"

    def __init__(self, workspace: str | Path = ""):
        self._has_workspace = bool(workspace)
        self.workspace = Path(workspace).resolve() if workspace else Path.home()

    def _instruction_path(self) -> Path:
        if self._has_workspace:
            return self.workspace / "AGENTS.md"
        return Path.home() / ".codex" / "AGENTS.md"

    def _mcp_config_path(self) -> Path:
        return Path.home() / ".codex" / "config.toml"

    def install(self, workspace: str | Path = "") -> dict[str, Any]:
        if workspace:
            self._has_workspace = True
            self.workspace = Path(workspace).resolve()

        # 1. 写指令（AGENTS.md，HTML 注释标记段落）
        instr_path = self._instruction_path()
        content = _read_text(instr_path)
        new_content = _replace_section(content, _BEGIN_MARKER, _END_MARKER, _INSTRUCTION_BODY)
        _write_text(instr_path, new_content)

        # 2. 写 MCP 配置（config.toml，# 注释标记段落）
        mcp_path = self._mcp_config_path()
        toml_content = _read_text(mcp_path)
        section = _mcp_toml_section()
        new_toml = _replace_section(toml_content, _TOML_BEGIN, _TOML_END, section)
        _write_text(mcp_path, new_toml)

        return {
            "provider": self.provider_name,
            "installed": True,
            "instruction_file": str(instr_path),
            "mcp_config_file": str(mcp_path),
            "binding_id": self._bind_with_store([str(instr_path), str(mcp_path)]),
        }

    def uninstall(self) -> dict[str, Any]:
        instr_path = self._instruction_path()

        # 1. 移除指令段落
        content = _read_text(instr_path)
        if _BEGIN_MARKER in content:
            new_content = _remove_section(content, _BEGIN_MARKER, _END_MARKER)
            if new_content.strip():
                _write_text(instr_path, new_content)
            else:
                try:
                    instr_path.unlink()
                except OSError:
                    pass

        # 2. 移除 TOML 中的 memoryguard 段落
        mcp_path = self._mcp_config_path()
        toml_content = _read_text(mcp_path)
        if _TOML_BEGIN in toml_content:
            new_toml = _remove_section(toml_content, _TOML_BEGIN, _TOML_END)
            if new_toml.strip():
                _write_text(mcp_path, new_toml)
            else:
                try:
                    mcp_path.unlink()
                except OSError:
                    pass

        return {
            "provider": self.provider_name,
            "installed": False,
            "instruction_file": str(instr_path),
            "mcp_config_file": str(mcp_path),
            "binding_id": self._unbind_with_store(),
        }

    def status(self) -> dict[str, Any]:
        instr_path = self._instruction_path()
        mcp_path = self._mcp_config_path()

        content = _read_text(instr_path)
        instruction_installed = _BEGIN_MARKER in content and _END_MARKER in content

        toml_content = _read_text(mcp_path)
        mcp_configured = _TOML_BEGIN in toml_content and _TOML_END in toml_content

        binding_id, binding_status = self._find_binding()
        return {
            "installed": instruction_installed and mcp_configured,
            "instruction_file": str(instr_path),
            "mcp_configured": mcp_configured,
            "binding_id": binding_id,
            "binding_status": binding_status,
        }


# ===========================================================================
# CursorAdapter
# ===========================================================================


class CursorAdapter(ProviderAdapter):
    """Cursor adapter。

    - 指令文件：<workspace>/.cursor/rules/memoryguard.mdc（新格式，MemoryGuard 专属文件）
      无 workspace 时 ~/.cursor/rules/memoryguard.mdc
    - MCP 配置：~/.cursor/mcp.json（用户级 JSON）
    """

    provider_name = "cursor"

    def __init__(self, workspace: str | Path = ""):
        self._has_workspace = bool(workspace)
        self.workspace = Path(workspace).resolve() if workspace else Path.home()

    def _instruction_path(self) -> Path:
        if self._has_workspace:
            return self.workspace / ".cursor" / "rules" / "memoryguard.mdc"
        return Path.home() / ".cursor" / "rules" / "memoryguard.mdc"

    def _mcp_config_path(self) -> Path:
        return Path.home() / ".cursor" / "mcp.json"

    def _instruction_content(self) -> str:
        """生成 MDC 文件完整内容（含 frontmatter + 标记段落）。"""
        frontmatter = (
            "---\n"
            "description: MemoryGuard memory redirect\n"
            "alwaysApply: true\n"
            "globs: []\n"
            "---\n"
        )
        return (
            frontmatter
            + _BEGIN_MARKER + "\n"
            + _INSTRUCTION_BODY + "\n"
            + _END_MARKER + "\n"
        )

    def install(self, workspace: str | Path = "") -> dict[str, Any]:
        if workspace:
            self._has_workspace = True
            self.workspace = Path(workspace).resolve()

        # 1. 写指令（MDC 文件是 MemoryGuard 专属，整体覆盖）
        instr_path = self._instruction_path()
        _write_text(instr_path, self._instruction_content())

        # 2. 写 MCP 配置（JSON merge）
        mcp_path = self._mcp_config_path()
        data = _load_json(mcp_path)
        _set_mcp_server(data, MCP_SERVER_NAME, _mcp_server_config())
        _save_json(mcp_path, data)

        return {
            "provider": self.provider_name,
            "installed": True,
            "instruction_file": str(instr_path),
            "mcp_config_file": str(mcp_path),
            "binding_id": self._bind_with_store([str(instr_path), str(mcp_path)]),
        }

    def uninstall(self) -> dict[str, Any]:
        # 1. 删除 MDC 指令文件
        instr_path = self._instruction_path()
        try:
            instr_path.unlink()
        except OSError:
            pass

        # 2. 移除 MCP 配置中的 memoryguard key
        mcp_path = self._mcp_config_path()
        data = _load_json(mcp_path)
        _remove_mcp_server(data, MCP_SERVER_NAME)
        if data:
            _save_json(mcp_path, data)
        else:
            try:
                mcp_path.unlink()
            except OSError:
                pass

        return {
            "provider": self.provider_name,
            "installed": False,
            "instruction_file": str(instr_path),
            "mcp_config_file": str(mcp_path),
            "binding_id": self._unbind_with_store(),
        }

    def status(self) -> dict[str, Any]:
        instr_path = self._instruction_path()
        mcp_path = self._mcp_config_path()

        instruction_installed = (
            instr_path.exists()
            and _BEGIN_MARKER in _read_text(instr_path)
        )

        data = _load_json(mcp_path)
        mcp_configured = _has_mcp_server(data, MCP_SERVER_NAME)

        binding_id, binding_status = self._find_binding()
        return {
            "installed": instruction_installed and mcp_configured,
            "instruction_file": str(instr_path),
            "mcp_configured": mcp_configured,
            "binding_id": binding_id,
            "binding_status": binding_status,
        }
