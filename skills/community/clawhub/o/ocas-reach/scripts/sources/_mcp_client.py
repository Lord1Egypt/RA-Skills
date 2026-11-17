"""Minimal stdio JSON-RPC client for MCP servers — shared base class.

Used by linkedin_mcp, paper_search_mcp, and yahoo_finance_mcp.
"""
from __future__ import annotations

import json
import subprocess
import threading
from typing import Any, Dict, Optional


class MCPClient:
    """Minimal stdio JSON-RPC client for MCP servers.

    Subclasses override cmd/args. Set env vars on the subclass to pass
    through to the child process.
    """

    def __init__(self, cmd: list[str], env: Optional[dict] = None):
        self._proc: Optional[subprocess.Popen] = None
        self._cmd = cmd
        self._env = env
        self._lock = threading.Lock()
        self._id_counter = 0

    def start(self):
        import os
        env = os.environ.copy()
        if self._env:
            env.update(self._env)
        self._proc = subprocess.Popen(
            self._cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            bufsize=1,
        )
        self._initialize()

    def _initialize(self):
        req = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "ocas-reach", "version": "3.4.0"},
            },
        }
        resp = self._send(req)
        if "error" in resp:
            raise RuntimeError(f"MCP init failed: {resp['error']}")
        self._send_notification("notifications/initialized")

    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        self._ensure_running()
        req = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        }
        resp = self._send(req)
        if "error" in resp:
            return {"error": resp["error"].get("message", str(resp["error"])), "raw": resp["error"]}
        result = resp.get("result", {})
        content = result.get("content", [])
        if not content:
            return result
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                texts.append(block.get("text", ""))
        combined = "\n".join(texts).strip()
        if combined.startswith("{") or combined.startswith("["):
            try:
                return json.loads(combined)
            except json.JSONDecodeError:
                pass
        return {"text": combined}

    def _send(self, req: dict) -> dict:
        self._ensure_running()
        assert self._proc is not None
        payload = json.dumps(req) + "\n"
        self._proc.stdin.write(payload)  # type: ignore[union-attr]
        self._proc.stdin.flush()  # type: ignore[union-attr]
        line = self._proc.stdout.readline()  # type: ignore[union-attr]
        if not line:
            raise RuntimeError("MCP server closed stdout")
        return json.loads(line)

    def _send_notification(self, method: str, params: Optional[dict] = None):
        self._ensure_running()
        assert self._proc is not None
        req: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params:
            req["params"] = params
        payload = json.dumps(req) + "\n"
        self._proc.stdin.write(payload)  # type: ignore[union-attr]
        self._proc.stdin.flush()  # type: ignore[union-attr]

    def _next_id(self) -> int:
        self._id_counter += 1
        return self._id_counter

    def _ensure_running(self):
        if self._proc is None:
            self.start()
        elif self._proc.poll() is not None:
            raise RuntimeError("MCP server process has exited")

    def close(self):
        proc = self._proc
        self._proc = None
        if proc is not None and proc.poll() is None:
            try:
                proc.stdin.close()  # type: ignore[union-attr]
            except Exception:
                pass
            proc.wait(timeout=5)
