---
name: lsp-assist
description: >
  Language Server Protocol integration for OpenClaw agents. Enables precise code navigation:
  go-to-definition, find-references, hover type info, diagnostics, and symbol search.
  Supports TypeScript (via typescript-language-server) and Python (via pyright).
  Two modes: one-shot (query then quit) and daemon (persistent server for multi-query sessions).
  Use when editing code and need to find where a function/type is defined, see all usages,
  check types, diagnose errors, or search workspace symbols.
  Use when the user says "go to definition", "find references", "what does this type mean",
  "check for errors", or when navigating large codebases where grep is insufficient.
---

# LSP Assist

Precise code navigation via Language Server Protocol.

## Modes

| Mode | How | When to use |
|------|-----|-------------|
| **Daemon** (recommended) | `daemon --port 9876` then HTTP queries | Multiple queries in a session (start once, query many) |
| **One-shot** | `goto/refs/hover/diag/symbols` directly | Single quick query, or scripting |

## Requirements

- **Runtime**: Python 3.10+ (standard library only)
- **OS**: Linux, macOS
- **Language servers** (install separately):
  - TypeScript: `npm i -g typescript-language-server typescript`
  - Python: `pip install pyright`
- **Project config**:
  - TypeScript: `tsconfig.json` in project root
  - Python: `pyproject.toml` or `pyrightconfig.json`

## Security

### Binding
Daemon binds to `127.0.0.1` only — no external/remote access:
```python
server = HTTPServer(("127.0.0.1", port), DaemonHandler)
```

### File Access Control
All file reads go through `_open_file()`, which enforces project-root containment:
```python
def _open_file(self, filepath: str):
    path = Path(filepath).resolve()          # resolve symlinks, .., etc.
    if str(path) in self._opened_files:
        return                               # skip duplicate opens
    common = os.path.commonpath([str(path), self.root_path])
    if common != self.root_path:             # must be direct ancestor of root
        raise ValueError(f"File outside project root: {path}")
    # Only then: read file content and send didOpen to language server
```
- `Path.resolve()` canonicalizes the path (resolves symlinks, `..`, `~`)
- `os.path.commonpath` rejects sibling dirs (e.g. `/root/openclaw-backup/` when root is `/root/openclaw`)
- Tested against: symlink escape, `..` traversal, trailing-slash differences, sibling-prefix collision

### Auth Token (optional)
When `--token <secret>` is passed, every HTTP request must include `Authorization: Bearer <secret>`:
```python
def _check_auth(self) -> bool:
    expected = getattr(self.server, "auth_token", None)
    if expected is None:
        return True                          # no token required
    header = self.headers.get("Authorization", "")
    if header == f"Bearer {expected}":
        return True
    self._respond({"error": "unauthorized"}, 401)
    return False
```
- Checked in both `do_GET` and `do_POST` before any handler logic
- Without `--token`, daemon is open on localhost (intended for local single-user use)

### Shutdown Handling
```python
elif self.path == "/shutdown":
    self._respond({"status": "shutting down"})
    threading.Thread(target=lambda: (time.sleep(0.5), os._exit(0)), daemon=True).start()
```
Responds first, then exits after 0.5s delay to ensure the HTTP response is flushed.

### Process Isolation
- One-shot mode: fresh server per query, auto-terminates (15s timeout)
- Daemon mode: persistent server, but `is_alive()` check returns 503 if the language server crashes
- Language server communication is local stdio only

## Quick Reference

### Daemon Mode (recommended for multi-query)

```bash
# Start daemon (blocks, run in background or separate terminal)
python3 scripts/lsp_client.py daemon --lang typescript --root /path/to/project --port 9876

# Start with auth token (requests need Bearer token)
python3 scripts/lsp_client.py daemon --lang typescript --root /path/to/project --port 9876 --token mysecret

# Query via HTTP (all output JSON)
curl -s http://127.0.0.1:9876/goto   -d '{"file":"src/main.ts","line":10,"col":5}'
curl -s http://127.0.0.1:9876/refs   -d '{"file":"src/main.ts","line":10,"col":5}'
curl -s http://127.0.0.1:9876/hover  -d '{"file":"src/main.ts","line":10,"col":5}'
curl -s http://127.0.0.1:9876/diag   -d '{"file":"src/main.ts"}'
curl -s http://127.0.0.1:9876/symbols -d '{"query":"UserService"}'
curl -s http://127.0.0.1:9876/shutdown
curl -s http://127.0.0.1:9876/ping   # health check

# With auth token
curl -s -H "Authorization: Bearer mysecret" http://127.0.0.1:9876/ping
```

### One-shot Mode

| Action | Command |
|--------|---------|
| Go to definition | `python3 scripts/lsp_client.py --lang ts --root <dir> goto --file <f> --line <n> --col <n>` |
| Find references | `python3 scripts/lsp_client.py --lang ts --root <dir> refs --file <f> --line <n> --col <n>` |
| Hover type info | `python3 scripts/lsp_client.py --lang ts --root <dir> hover --file <f> --line <n> --col <n>` |
| Diagnostics | `python3 scripts/lsp_client.py --lang ts --root <dir> diag --file <f>` |
| Symbol search | `python3 scripts/lsp_client.py --lang ts --root <dir> symbols [--query <text>]` |

Language shorthand: `--lang typescript` or `--lang ts` or `--lang python`.

## Output Format

All commands output **JSON** for structured consumption:

```json
// goto / refs
[{"file": "/path/to/file.ts", "line": 42, "col": 10}]

// hover
"function foo(bar: string): number"

// diag
[{"severity": "ERROR", "line": 10, "message": "Cannot find name 'x'"}]

// symbols
[{"name": "UserService", "kind": 5, "file": "/path/to/file.ts", "line": 12, "container": "models"}]
```

## When to Use vs Grep

| Scenario | Use |
|----------|-----|
| "Where is this function defined?" | LSP goto |
| "Who calls this function?" | LSP refs |
| "What type is this variable?" | LSP hover |
| "Any compile errors?" | LSP diag |
| "Find all classes matching X" | LSP symbols |
| "Search for text pattern 'TODO'" | grep |
| "Find all .json files" | glob |
| "Search across non-code files" | grep |

## Supported Languages

| Language | Server | Install |
|----------|--------|---------|
| TypeScript/JavaScript | typescript-language-server | `npm i -g typescript-language-server typescript` |
| Python | pyright | `pip install pyright` |

Adding a language: edit `SERVERS` dict in `lsp_client.py` — add the server command and file extensions.
