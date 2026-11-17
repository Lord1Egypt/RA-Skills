"""Reddit MCP Buddy connector for Reach.

Invokes reddit-mcp-buddy (npm package) via stdio JSON-RPC to browse Reddit,
search posts, and fetch post details. No Reddit API key required for anonymous
mode (10 req/min). Optional OAuth credentials raise limits to 60-100 req/min.

MCP server: reddit-mcp-buddy (npm)
Install:   npx -y reddit-mcp-buddy
"""
from __future__ import annotations

import json
import subprocess
import threading
from typing import Any, Dict, Optional


class _MCPClient:
    """Minimal stdio JSON-RPC client for MCP servers."""

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
        """Send MCP initialize handshake."""
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
        # Send initialized notification
        self._send_notification("notifications/initialized")

    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Call an MCP tool and return the result content dict."""
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

        # Parse the result — MCP returns content array
        result = resp.get("result", {})
        content = result.get("content", [])
        if not content:
            return result

        # Extract text from text-type content blocks
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                texts.append(block.get("text", ""))

        combined = "\n".join(texts).strip()
        # Try to parse as JSON if it looks like JSON
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

    def _send_notification(self, method: str, params: dict = None):
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


# ── Module-level client cache ──────────────────────────────────────────────
_client: Optional[_MCPClient] = None


def _get_client(auth: dict) -> _MCPClient:
    global _client
    if _client is None or _client._proc is None or _client._proc.poll() is not None:
        env = {}
        for key in ("REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USERNAME", "REDDIT_PASSWORD"):
            val = auth.get(key) or auth.get(key.lower())
            if val:
                env[key] = val
        _client = _MCPClient(["npx", "-y", "reddit-mcp-buddy"], env=env if env else None)
        _client.start()
    return _client


def _close_client():
    global _client
    if _client:
        _client.close()
        _client = None


# ── Reach query interface ──────────────────────────────────────────────────

def query(action: str, params: dict, auth: dict) -> dict:
    """
    Reach-facing query entry point.

    Actions:
      browse   — Browse a subreddit. Params: subreddit, sort, time, limit
      search   — Search Reddit. Params: query, subreddit, sort, time, limit
      post     — Get post details. Params: url or post_id
      user     — Analyze a user. Params: username
      explain  — Explain a Reddit term. Params: term
    """
    client = _get_client(auth)

    try:
        if action == "browse":
            return _action_browse(client, params)
        elif action == "search":
            return _action_search(client, params)
        elif action == "post":
            return _action_post(client, params)
        elif action == "user":
            return _action_user(client, params)
        elif action == "explain":
            return _action_explain(client, params)
        else:
            return {"error": f"Unknown action: {action}", "valid_actions": ["browse", "search", "post", "user", "explain"]}
    except Exception as e:
        # Reset client on failure so next call reinitializes
        _close_client()
        return {"error": str(e), "action": action}


def _action_browse(client: _MCPClient, params: dict) -> dict:
    args = {
        "subreddit": params.get("subreddit", "all"),
        "sort": params.get("sort", "hot"),
        "time": params.get("time", "day"),
        "limit": int(params.get("limit", 25)),
    }
    if params.get("include_subreddit_info"):
        args["include_subreddit_info"] = True
    return client.call_tool("browse_subreddit", args)


def _action_search(client: _MCPClient, params: dict) -> dict:
    args = {
        "query": params.get("query", ""),
        "sort": params.get("sort", "relevance"),
        "time": params.get("time", "week"),
        "limit": int(params.get("limit", 25)),
    }
    if params.get("subreddit"):
        args["subreddit"] = params["subreddit"]
    if params.get("author"):
        args["author"] = params["author"]
    if params.get("flair"):
        args["flair"] = params["flair"]
    return client.call_tool("search_reddit", args)


def _action_post(client: _MCPClient, params: dict) -> dict:
    if params.get("url"):
        args = {"url": params["url"]}
    elif params.get("post_id"):
        args = {"post_id": params["post_id"]}
        if params.get("subreddit"):
            args["subreddit"] = params["subreddit"]
    else:
        return {"error": "post requires 'url' or 'post_id'"}
    if params.get("sort"):
        args["sort"] = params["sort"]
    if params.get("depth"):
        args["depth"] = int(params["depth"])
    return client.call_tool("get_post_details", args)


def _action_user(client: _MCPClient, params: dict) -> dict:
    if not params.get("username"):
        return {"error": "user requires 'username'"}
    return client.call_tool("user_analysis", {"username": params["username"]})


def _action_explain(client: _MCPClient, params: dict) -> dict:
    if not params.get("term"):
        return {"error": "explain requires 'term'"}
    return client.call_tool("reddit_explain", {"term": params["term"]})
