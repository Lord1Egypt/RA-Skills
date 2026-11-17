"""MCP 客户端：真实发现与资源列举。

纯标准库实现。通过 stdio 与用户已配置的 MCP server 交互，
支持 initialize / tools/list / resources/list / tools/call。

发现位置：
- Claude: ~/.claude.json (top-level mcpServers) + ./.mcp.json (project-local)
- Cursor: ~/.cursor/mcp.json
- Codex:   ~/.codex/config.toml ([mcp_servers.NAME])

安全约束：只调用 resources/list 与 tools/list（只读发现），
不调用任何 tools/call（与 external_mcp_detector 的安全策略一致）。
单个 server 失败不影响其他 server。
"""

from __future__ import annotations

import json
import os
import queue
import subprocess
import threading
import time
from pathlib import Path
from typing import Any

# MCP 协议常量（与 mcp_server.py 对齐）
PROTOCOL_VERSION = "2024-11-05"
CLIENT_NAME = "memoryguard-mcp-client"
CLIENT_VERSION = "0.1.0"
DEFAULT_TIMEOUT = 10.0  # 每个 server 交互 10 秒超时


# ---------------------------------------------------------------------------
# MCPClient：单个 MCP server 的 stdio 客户端
# ---------------------------------------------------------------------------


class MCPClient:
    """通过 stdio 与单个 MCP server 交互的客户端。

    用法：
        client = MCPClient(["cmd"], ["/c", "npx", "server"])
        client.initialize()
        tools = client.list_tools()
        resources = client.list_resources()
        client.close()
    """

    def __init__(self, command: list[str], args: list[str] | None = None,
                 env: dict[str, str] | None = None, timeout: float = DEFAULT_TIMEOUT):
        self.command = list(command)
        self.args = list(args or [])
        self.env = dict(env or {})
        self.timeout = timeout
        self._proc: subprocess.Popen | None = None
        self._next_id = 1
        self._initialized = False
        self._server_info: dict[str, Any] = {}
        self._server_capabilities: dict[str, Any] = {}
        self._stderr_lines: list[str] = []
        self._stderr_thread: threading.Thread | None = None
        self._reader_thread: threading.Thread | None = None
        self._line_queue: queue.Queue | None = None
        self._closed = False

    # -- 子进程管理 --------------------------------------------------------

    def _start(self) -> None:
        if self._proc is not None:
            return
        full_env = {**os.environ, **self.env}
        cmd = self.command + self.args
        try:
            self._proc = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=full_env,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
            )
        except (OSError, ValueError) as e:
            raise RuntimeError(f"failed to start MCP server {cmd}: {e}")
        # 单个常驻 reader 线程：把 stdout 行投递到队列，避免竞争与管道阻塞
        self._line_queue = queue.Queue()
        self._reader_thread = threading.Thread(target=self._reader_loop, daemon=True)
        self._reader_thread.start()
        # 后台排空 stderr，避免 stderr 缓冲区写满导致 server 阻塞
        self._stderr_thread = threading.Thread(target=self._drain_stderr, daemon=True)
        self._stderr_thread.start()

    def _reader_loop(self) -> None:
        proc = self._proc
        if proc is None or proc.stdout is None or self._line_queue is None:
            return
        try:
            for line in proc.stdout:
                self._line_queue.put(line)
            self._line_queue.put(None)  # EOF 哨兵
        except Exception as e:
            self._line_queue.put(e)

    def _drain_stderr(self) -> None:
        proc = self._proc
        if proc is None or proc.stderr is None:
            return
        try:
            for line in proc.stderr:
                self._stderr_lines.append(line)
        except Exception:
            pass

    # -- JSON-RPC 传输 -----------------------------------------------------

    def _send_request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        if self._proc is None:
            self._start()
        assert self._proc is not None and self._proc.stdin is not None
        req_id = self._next_id
        self._next_id += 1
        request: dict[str, Any] = {"jsonrpc": "2.0", "id": req_id, "method": method}
        if params is not None:
            request["params"] = params
        try:
            self._proc.stdin.write(json.dumps(request, ensure_ascii=False) + "\n")
            self._proc.stdin.flush()
        except (BrokenPipeError, OSError) as e:
            raise ConnectionError(f"failed to send request {method}: {e}")
        return self._read_response(req_id)

    def _send_notification(self, method: str, params: dict[str, Any] | None = None) -> None:
        if self._proc is None or self._proc.stdin is None:
            return
        notif: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            notif["params"] = params
        try:
            self._proc.stdin.write(json.dumps(notif, ensure_ascii=False) + "\n")
            self._proc.stdin.flush()
        except (BrokenPipeError, OSError):
            pass

    def _read_response(self, req_id: int) -> dict[str, Any]:
        assert self._line_queue is not None
        deadline = time.monotonic() + self.timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f"no response for id={req_id} within {self.timeout}s")
            try:
                item = self._line_queue.get(timeout=remaining)
            except queue.Empty:
                raise TimeoutError(f"no response for id={req_id} within {self.timeout}s")
            if item is None:
                raise ConnectionError("MCP server closed stdout")
            if isinstance(item, Exception):
                raise ConnectionError(f"stdout read failed: {item}")
            line = item.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue  # 跳过非 JSON 行
            if not isinstance(msg, dict):
                continue
            if msg.get("id") != req_id:
                continue  # 跳过通知/其他 id 的响应
            err = msg.get("error")
            if err:
                raise RuntimeError(f"MCP error from server: {err}")
            return msg.get("result", {})

    # -- MCP 协议方法 ------------------------------------------------------

    def initialize(self) -> dict[str, Any]:
        """initialize 握手：能力协商。"""
        result = self._send_request("initialize", {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": CLIENT_NAME, "version": CLIENT_VERSION},
        })
        self._server_info = result.get("serverInfo", {})
        self._server_capabilities = result.get("capabilities", {})
        # 发送 initialized 通知（无响应，参考 mcp_server.handle_request 的 notifications/initialized 分支）
        self._send_notification("notifications/initialized")
        self._initialized = True
        return result

    def list_tools(self) -> list[dict[str, Any]]:
        """tools/list。"""
        result = self._send_request("tools/list")
        return list(result.get("tools", []))

    def list_resources(self) -> list[dict[str, Any]]:
        """resources/list（关键能力：列举 server 暴露的资源）。"""
        result = self._send_request("resources/list")
        return list(result.get("resources", []))

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        """tools/call。注意：发现层不调用，仅提供能力。"""
        params: dict[str, Any] = {"name": name}
        if arguments is not None:
            params["arguments"] = arguments
        return self._send_request("tools/call", params)

    def close(self) -> None:
        if self._closed or self._proc is None:
            self._closed = True
            return
        self._closed = True
        try:
            if self._proc.stdin is not None:
                self._proc.stdin.close()  # EOF，提示 server 退出
        except Exception:
            pass
        try:
            self._proc.terminate()
            self._proc.wait(timeout=2)
        except Exception:
            try:
                self._proc.kill()
            except Exception:
                pass

    @property
    def server_info(self) -> dict[str, Any]:
        return self._server_info

    @property
    def server_capabilities(self) -> dict[str, Any]:
        return self._server_capabilities

    @property
    def stderr_text(self) -> str:
        return "".join(self._stderr_lines)

    def __enter__(self) -> "MCPClient":
        return self

    def __exit__(self, *exc) -> None:
        self.close()


# ---------------------------------------------------------------------------
# MCPDiscovery：扫描用户已配置的 MCP server
# ---------------------------------------------------------------------------


class MCPDiscovery:
    """扫描 Claude / Cursor / Codex 的 MCP server 配置并发现资源。

    安全：scan_all() 只读配置文件；discover_resources() 只调用
    resources/list（只读），不调用任何 tools/call。单个 server 失败被隔离。
    """

    def __init__(self, timeout: float = DEFAULT_TIMEOUT):
        self.home = Path.home()
        self.timeout = timeout

    # -- 扫描 -------------------------------------------------------------

    def scan_all(self) -> list[dict[str, Any]]:
        """扫描所有已知位置的 MCP 配置。

        返回 [{server_name, command, args, env, config_source}]。
        跨平台：用 Path.home()。无配置时返回空列表，不报错。
        """
        servers: list[dict[str, Any]] = []
        servers.extend(self._scan_claude_global())
        servers.extend(self._scan_claude_project_local())
        servers.extend(self._scan_cursor())
        servers.extend(self._scan_codex())
        return servers

    def _scan_claude_global(self) -> list[dict[str, Any]]:
        path = self.home / ".claude.json"
        data = self._load_json(path)
        if not data:
            return []
        return self._parse_claude_servers(data.get("mcpServers", {}),
                                          "claude:~/.claude.json")

    def _scan_claude_project_local(self) -> list[dict[str, Any]]:
        path = Path.cwd() / ".mcp.json"
        data = self._load_json(path)
        if not data:
            return []
        return self._parse_claude_servers(data.get("mcpServers", {}),
                                          "claude:.mcp.json")

    def _scan_cursor(self) -> list[dict[str, Any]]:
        path = self.home / ".cursor" / "mcp.json"
        data = self._load_json(path)
        if not data:
            return []
        return self._parse_claude_servers(data.get("mcpServers", {}),
                                          "cursor:~/.cursor/mcp.json")

    def _scan_codex(self) -> list[dict[str, Any]]:
        path = self.home / ".codex" / "config.toml"
        if not path.exists():
            return []
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            return []
        try:
            data = _parse_toml(text)
        except Exception:
            return []
        servers = data.get("mcp_servers", {})
        results: list[dict[str, Any]] = []
        if not isinstance(servers, dict):
            return results
        for name, cfg in servers.items():
            if not isinstance(cfg, dict):
                continue
            command = cfg.get("command")
            if not command or not isinstance(command, str):
                continue
            args = cfg.get("args", [])
            if isinstance(args, str):
                args = [args]
            else:
                args = list(args or [])
            env = cfg.get("env", {})
            if not isinstance(env, dict):
                env = {}
            results.append({
                "server_name": str(name),
                "command": [command],
                "args": [str(a) for a in args],
                "env": {str(k): str(v) for k, v in env.items()},
                "config_source": "codex:~/.codex/config.toml",
            })
        return results

    # -- 解析辅助 ---------------------------------------------------------

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any] | None:
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return None
        return data if isinstance(data, dict) else None

    @staticmethod
    def _parse_claude_servers(mcp_servers: Any, source: str) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        if not isinstance(mcp_servers, dict):
            return results
        for name, cfg in mcp_servers.items():
            if not isinstance(cfg, dict):
                continue
            command = cfg.get("command")
            if not command:
                continue
            # 只支持 stdio 类型；跳过 sse/http
            stype = cfg.get("type", "stdio")
            if stype not in ("stdio", None, ""):
                continue
            if isinstance(command, str):
                cmd_list = [command]
            elif isinstance(command, list):
                cmd_list = [str(c) for c in command]
            else:
                continue
            args = cfg.get("args", [])
            if isinstance(args, str):
                args = [args]
            else:
                args = [str(a) for a in (args or [])]
            env = cfg.get("env", {})
            if not isinstance(env, dict):
                env = {}
            results.append({
                "server_name": str(name),
                "command": cmd_list,
                "args": args,
                "env": {str(k): str(v) for k, v in env.items()},
                "config_source": source,
            })
        return results

    # -- 资源发现 ---------------------------------------------------------

    def discover_resources(self) -> list[dict[str, Any]]:
        """对每个已配置 server 调 resources/list，汇总返回。

        单个 server 失败不影响其他。不调用任何 tool。
        返回 [{server_name, config_source, resources, resource_count, error}]。
        """
        results: list[dict[str, Any]] = []
        for srv in self.scan_all():
            entry: dict[str, Any] = {
                "server_name": srv["server_name"],
                "config_source": srv["config_source"],
                "resources": [],
                "resource_count": 0,
                "error": None,
            }
            client = MCPClient(srv["command"], srv["args"], srv.get("env", {}),
                               timeout=self.timeout)
            try:
                try:
                    client.initialize()
                    resources = client.list_resources()
                finally:
                    client.close()
                entry["resources"] = resources
                entry["resource_count"] = len(resources)
            except Exception as e:
                entry["error"] = f"{type(e).__name__}: {e}"
            results.append(entry)
        return results


# ---------------------------------------------------------------------------
# TOML 解析（Codex config.toml）
# ---------------------------------------------------------------------------

try:
    import tomllib as _tomllib  # Python 3.11+ 标准库

    def _parse_toml(text: str) -> dict[str, Any]:
        return _tomllib.loads(text)
except ModuleNotFoundError:
    # Python 3.10 没有 tomllib：最小子集解析器，仅覆盖 Codex config 常见结构
    # （section / key=value / 字符串 / 数组 / int / bool）。不支持多行数组与复杂转义。
    def _parse_toml(text: str) -> dict[str, Any]:
        root: dict[str, Any] = {}
        current: dict[str, Any] = root
        for raw in text.splitlines():
            line = _strip_toml_comment(raw).strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                header = line[1:-1].strip()
                section_path = [p.strip().strip('"').strip("'") for p in header.split(".")]
                current = root
                for part in section_path:
                    node = current.get(part)
                    if not isinstance(node, dict):
                        node = {}
                        current[part] = node
                    current = node
                continue
            if "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip().strip('"').strip("'")
            current[key] = _parse_toml_value(val.strip())
        return root


def _strip_toml_comment(line: str) -> str:
    in_single = in_double = False
    for i, ch in enumerate(line):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            return line[:i]
    return line


def _parse_toml_value(s: str) -> Any:
    s = s.strip()
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    if len(s) >= 2 and s[0] == "'" and s[-1] == "'":
        return s[1:-1]
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [_parse_toml_value(p) for p in _split_toml_array(inner)]
    if s == "true":
        return True
    if s == "false":
        return False
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


def _split_toml_array(s: str) -> list[str]:
    parts: list[str] = []
    cur = ""
    in_single = in_double = False
    for ch in s:
        if ch == "'" and not in_double:
            in_single = not in_single
            cur += ch
        elif ch == '"' and not in_single:
            in_double = not in_double
            cur += ch
        elif ch == "," and not in_single and not in_double:
            if cur.strip():
                parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts
