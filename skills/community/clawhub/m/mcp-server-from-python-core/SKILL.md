---
name: mcp-server-from-python-core
description: Wrap an existing Python app or engine as a local stdio MCP server, register it with OpenClaw, and prove the tools actually work. Covers reusing the app venv, the mcp v1 vs v2 rename trap, sys.path for vendored modules, and the "Connection closed" probe failure.
version: 1.0.0
license: MIT
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# MCP server from a Python core

Turn a Python app that already works into a local stdio MCP server for OpenClaw,
without importing the GUI and without rewriting the business logic.

## 1. Separate the reusable core from the interface

Before writing anything, map the code: `grep -n '^class ' file.py` plus per-class
line counts. A GUI app often hides its logic inside `__init__` and the window
class. Reuse the core engine class and its model weights; do not import the GUI.
A small engine class plus a small storage class is usually the payload; the large
UI class is not.

## 2. Pin the MCP SDK to v1

Use the plain **`mcp`** SDK, not a newer major. SDK 2.x renamed `FastMCP` to
`MCPServer`, so `from mcp.server.fastmcp import FastMCP` written against v1
raises `ModuleNotFoundError` ("FastMCP renamed to MCPServer").

```bash
pip install 'mcp<2'
python -c "from mcp.server.fastmcp import FastMCP"
```

Verify the import before wiring anything.

## 3. Reuse the app's own virtualenv

Run the server with the app's `venv/bin/python` so torch/onnx/CLIP weights
already resolve. If `venv/bin/pip` fails with `cannot execute: required file not found`
(the shebang points at a path the project no longer occupies after a move),
install through the interpreter instead:

```bash
venv/bin/python -m pip install 'mcp<2'
```

## 4. Put vendored packages on sys.path

A vendored module (an in-project `clip/` package, for example) is not in
site-packages. A project that imports it from its own directory needs:

```python
sys.path.insert(0, str(PROJ))
```

in the server, or the MCP process dies at import time.

## 5. Make tool functions callable without MCP, then wrap them

Define plain functions and thin `@mcp.tool()` wrappers that delegate:

```python
def tool_look(image): ...
@mcp.tool()
def look(image: str) -> dict:
    return tool_look(image)
```

This lets you test the real logic in-process before debugging the protocol, and
separates tool bugs from transport bugs.

## 6. Inputs: file path or data URL

Accept either. Decode a data URL through `numpy.frombuffer` + `cv2.imdecode`.
Keep model loads lazy and memoized in module globals so the first call pays the
cold-load cost once and repeated calls do not.

## 7. Register, then probe

`openclaw mcp add` may finish silently and write nothing. Use `openclaw mcp set`
and confirm the definition landed in the config:

```bash
openclaw mcp set <name> '{"command":"<venv>/bin/python","args":["<server>.py"]}'
openclaw mcp doctor <name> --probe
```

A saved definition is not reachability. `doctor --probe` must print
`<name>: ok`. `openclaw mcp tools <name>` takes `--include/--exclude/--clear`.

## 8. "Connection closed" means read the real traceback

Run the server by hand:

```bash
venv/bin/python server.py </dev/null
```

A startup traceback (bad import, the v2 rename) is the cause, not the OpenClaw
config. Confirm the tool list over the protocol with JSON-RPC lines —
`initialize`, `notifications/initialized`, `tools/list` — piped into the server
on stdin, and check each expected tool name appears.

Keep the verification gates distinct: import works → server starts → protocol
handshake → `tools/list` → OpenClaw registration → agent-visible tools. Report
which gate passed, not "it works".

## 9. Write the companion usage skill

Tell the agent what each tool returns, what cold-start and CPU cost to expect,
and any ethical guard (for example: do not describe flagged content). Point it at
the server path, venv, weights, and data directory so debugging does not require
asking.

## What this does not solve

Model weights that need a GPU, and long-running inference, still block the turn.
If a tool call can take minutes, say so in the tool description instead of
letting the agent discover it by timeout.
