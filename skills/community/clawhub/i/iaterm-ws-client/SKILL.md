---
name: iaterm-ws-agent
description: Interact with IATerm terminals via the local WebSocket API (ws://127.0.0.1:19790/ws). Use when the user asks to list workspaces, displays, or panels, view active terminal connections, send commands to a terminal, or capture/subscribe to terminal output. Also use when integrating external AI agents with IATerm.
metadata:
  short-description: Control IATerm terminals via WebSocket API
---

# IATerm WebSocket Agent

Control IATerm terminals via the local WebSocket API.

## CRITICAL: Always use the ws_client.py script

**NEVER write inline WebSocket code.** Always use the provided CLI script at `scripts/ws_client.py` (relative to this skill file).

Find the script path:
```bash
SKILL_DIR="$(dirname "$(find ~/.opc/skills -name ws_client.py -path "*/iaterm-ws-agent/*" 2>/dev/null | head -1)")"
WS_CLIENT="$SKILL_DIR/ws_client.py"
```

### Prerequisites

```bash
pip install websockets 2>/dev/null || pip3 install websockets 2>/dev/null
```

### Session ID (IMPORTANT)

`IATERM_SESSION_ID` environment variable must be set by the host application (e.g. IATerm) before invoking the client. **Do NOT generate this value yourself** — if the variable is missing, the client will exit with an error, indicating the host application has not properly initialized the session.

The first command triggers user approval in the IATerm UI. Once approved, the WS token is cached at `~/.cache/iaterm-ws-client/ws_token.json` (permissions 0600). Subsequent commands reuse the cached token and skip approval.

If the token expires, the client automatically clears the cache and re-prompts for approval.

### Operation Approval

`send_input` and `subscribe_output` require interactive confirmation before execution:

```
[Approval] send_input to conn-123: 'ls -la\n'
  y = approve this time  |  n = reject  |  a = always approve for this target
  [y/n/a]:
```

- **y** — approve this single invocation
- **n** — reject (command exits with error)
- **a** — always approve for this specific target (saved to `~/.cache/iaterm-ws-client/approval.json`)

Use `--auto-approve` to skip all confirmation prompts (for automated pipelines):

```bash
python3 "$WS_CLIENT" --auto-approve send_input --connection-id <id> --data "ls\n"
```

## Commands

### List workspaces
```bash
python3 "$WS_CLIENT" list_workspaces
```

### List displays for a workspace
```bash
python3 "$WS_CLIENT" list_displays --workspace-id <id>
```

### List panels (all or filtered by workspace)
```bash
python3 "$WS_CLIENT" list_panels
python3 "$WS_CLIENT" list_panels --workspace-id <id>
```

### Get panel info
```bash
python3 "$WS_CLIENT" get_panel_info --panel-id <id>
```

### List active connections

**IMPORTANT:** `list_connections` only returns **remote** connections (SSH, Serial, JumpServer). Local terminal connections are automatically filtered out by the backend. If this command returns connections, they are ALL remote — do NOT judge by the `name` field. Always check the `connection_type` field to determine the actual type:
- `ssh` — SSH remote connection
- `serial` — Serial port connection

If the result is empty, it means there are no active remote connections (local terminals may still exist but are excluded from this API).

```bash
python3 "$WS_CLIENT" list_connections
python3 "$WS_CLIENT" list_connections --type ssh
```

### Send input to a terminal
```bash
python3 "$WS_CLIENT" send_input --connection-id <id> --data "ls -la\n"
```
Use `\n` for Enter, `\t` for Tab, `\x03` for Ctrl-C.

### Subscribe to terminal output (long-lived, Ctrl-C to stop)
```bash
python3 "$WS_CLIENT" subscribe_output --connection-id <id>
```

## How it works

1. **Each command** establishes an independent WebSocket connection, executes, and disconnects.
2. **First connection** — sends `identify(session_id)` → user approves in IATerm UI (up to 60s) → receives `ws_token` → cached to disk.
3. **Subsequent connections** — sends `identify(session_id + cached token)` → server recognizes the token → skips approval → executes immediately.
4. **Token expiry** — if the server rejects a cached token (error -15 or `connection_rejected`), the client clears the cache and retries with a fresh approval flow.
5. **Approval gate** — `send_input` and `subscribe_output` prompt for interactive confirmation (y/n/a) unless `--auto-approve` is set.

## Configuration

| Env Variable | Default | Description |
|---|---|---|
| `IATERM_SESSION_ID` | *(required)* | Stable identifier for this agent session |
| `IATERM_WS_PORT` | `19790` | WebSocket server port |
| `XDG_CACHE_HOME` | `~/.cache` | Base directory for token/approval cache |

## Changelog

### v2.0.0 — 无 Daemon 直连架构 + 安全防护增强

**架构重写：去 Daemon 化**
- 删除 `WsDaemon` 类、Unix socket IPC、daemon 生命周期管理（`_send_msg`/`_recv_msg`/`_start_daemon_bg`/`_stop_daemon` 等）
- 删除 `daemon`、`stop` 子命令和 `--session` 参数
- 删除不再需要的 imports：`signal`、`socket`、`struct`、`subprocess`
- 每条命令独立建立 WS 连接，执行完断开，无常驻后台进程

**连接与认证**
- Session ID 从 `IATERM_SESSION_ID` 环境变量获取，由宿主应用设置，禁止自行生成，缺失则报错退出
- 首次连接：`identify(session_id)` → IATerm UI 审批 → 获得 `ws_token` → 缓存至 `~/.cache/iaterm-ws-client/ws_token.json`（权限 0600）
- 后续连接：`identify(session_id + cached token)` → 服务端识别 → 跳过审批 → 直接执行
- Token 失效（error -15 或 `connection_rejected`）时自动清缓存，重走审批流程

**操作审批**
- `send_input` / `subscribe_output` 执行前交互式确认：y（本次通过）/ n（拒绝）/ a（始终通过）
- 选 `a` 记入 `~/.cache/iaterm-ws-client/approval.json`，后续同目标操作自动通过
- `--auto-approve` CLI 参数跳过所有确认（用于自动化流水线）

**文档补充**
- `list_connections` 明确只返回远程连接（SSH/Serial/JumpServer），本地终端被后端过滤
- 连接类型判断统一使用 `connection_type` 字段，不依赖 `name` 字段

### v1.0.2 — Security scan compliance

- Daemon startup via `subprocess.Popen(start_new_session=True)`
- State directory moved to `~/.cache/iaterm-ws-client/` (XDG)
- Explicit `.replace()` escapes instead of `.encode().decode("unicode_escape")`
- Session token written to file (permissions 0600) instead of stderr

## Typical Workflow

```bash
# IATERM_SESSION_ID is set by the host application — do not generate it manually

# 1. Connect — first call triggers approval in IATerm UI
python3 "$WS_CLIENT" list_workspaces

# 2. Discover — find the connection_id (token cached, no re-approval)
python3 "$WS_CLIENT" list_panels
python3 "$WS_CLIENT" list_connections

# 3. Execute — send command to a terminal (prompts for approval)
python3 "$WS_CLIENT" send_input --connection-id <id> --data "ls -la\n"

# 4. Read — get terminal output
python3 "$WS_CLIENT" subscribe_output --connection-id <id>
```

## API Reference (for understanding responses)

### Response format
- Success: `{ "result": { ... } }`
- Error: `{ "error": { "code": <int>, "message": "..." } }`

### Error codes
| Code | Meaning |
|------|---------|
| -1 | Method not found |
| -2 | Invalid params |
| -3 | Internal error |
| -5 | Connection not found |
| -6 | Rate limited |
| -14 | Connection limit (another client connected) |
| -15 | Auth failed (invalid or missing token) |

### Key object fields
- **workspace**: `id`, `name`, `description`, `is_default`, `sort_order`
- **display**: `id`, `workspace_id`, `display_index`, `name`
- **panel**: `id`, `workspace_id`, `connection_id`, `display_id`, `name`, `grid_row`, `grid_column`
- **connection**: `id`, `name`, `connection_type` (**use this to determine type, NOT `name`**), `status`, `created_at`, `bytes_sent`, `bytes_received`

## Important Notes

- IATerm must be running for the API to be available
- The API only binds to 127.0.0.1; not accessible remotely
- First connection requires user approval in IATerm UI (60s timeout)
- Only one client connection allowed at a time
- `send_input` is rate-limited to 30 calls/sec per connection
- `connection_id` comes from `list_connections` or panel's `connection_id` field

## Custom Theme Format

Custom themes are stored as JSON in `~/.iaterm/themes/{theme-id}.json`. Optional CSS override: `~/.iaterm/themes/{theme-id}.css`.

```json
{
  "id": "my-theme",
  "name": "my-theme",
  "displayName": "My Theme",
  "type": "dark",
  "designRationale": "Design description (200-500 chars)",
  "variables": {
    "backgroundPrimary": "#0d1117",
    "backgroundSecondary": "#161b22",
    "backgroundTertiary": "#21262d",
    "backgroundCard": "#1c2128",
    "backgroundCardHover": "#262c36",
    "textPrimary": "#e6edf3",
    "textSecondary": "#8b949e",
    "textMuted": "#484f58",
    "accentPrimary": "#58a6ff",
    "error": "#f85149",
    "success": "#3fb950",
    "warning": "#d29922",
    "borderPrimary": "#30363d",
    "borderSubtle": "#21262d",
    "borderAccent": "#58a6ff",
    "iconDefault": "#8b949e",
    "iconHover": "#e6edf3"
  }
}
```

- `type`: `"light"` | `"dark"` | `"auto"`
- All color values: hex format (`#rrggbb` or `#rrggbbaa`)
- CSS variables auto-mapped: `backgroundPrimary` → `--color-background-primary`
