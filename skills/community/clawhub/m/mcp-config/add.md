# Add MCP Server

Procedure for registering a new MCP server.

## CRITICAL: Claude Code uses `claude mcp add` CLI

**Do NOT manually edit `.mcp.json` for Claude Code.** Manually adding entries to `.mcp.json` does NOT make Claude Code recognize the server. Always use the `claude mcp add` CLI command.

```bash
# stdio server (project scope)
claude mcp add --scope project my-server -- npx my-mcp-server

# HTTP server (project scope)
claude mcp add --transport http --scope project my-server https://example.com/mcp

# stdio server with env vars
claude mcp add --scope project -e API_KEY=xxx my-server -- npx my-mcp-server
```

**Name restriction**: Only letters, numbers, hyphens, underscores. No spaces.

## Required Procedure: Scope Selection (AskUserQuestion Required)

**Before adding an MCP server, always use AskUserQuestion in 2 steps:**

### Step 1: Scope Selection

| Option | Description |
|--------|-------------|
| Global | Add to each agent's config file (proceed to step 2) |
| Project | Add only to the current project |

### Step 2: When Global is selected → Agent Selection (multiSelect)

| Agent | Method | Difference |
|-------|--------|------------|
| Claude Code | `claude mcp add --scope user` | CLI required, manual `.mcp.json` edit NOT recognized |
| Cursor | Edit `~/.cursor/mcp.json` | `transport` field not required |
| Antigravity | Edit `~/.gemini/antigravity/mcp_config.json` | `"transport": "stdio"` required |

**multiSelect: true** — can add to multiple agents simultaneously.

**Do not decide arbitrarily.** Even if `.mcp.json` exists in the project directory, the user may want to add globally, and vice versa.

### Claude Code Scope Options

| Scope | Flag | Config File | Key Path | Description |
|-------|------|-------------|----------|-------------|
| local | `--scope local` (default) | `~/.claude.json` | `projects["/path/to/project"].mcpServers` | This machine, this project only |
| user | `--scope user` | `~/.claude.json` | root `mcpServers` | This machine, all projects |
| project | `--scope project` | `./.mcp.json` | `mcpServers` | Committed to repo, shared with team |

## Core Rule: Register as Separate Server

New MCP server = register as a separate key. **Do not put it inside an existing server's `env`.**

## Validation Checklist

- [ ] Claude Code: used `claude mcp add` CLI (NOT manual `.mcp.json` edit)
- [ ] Cursor/Antigravity: JSON syntax is valid
- [ ] Each server is registered as a separate key
- [ ] Server name contains only letters, numbers, hyphens, underscores
- [ ] `claude mcp list` shows the server as Connected

## Activate the change (MANDATORY — after every config edit or `mcp add`)

A new MCP entry (or edits to existing ones) is NOT picked up by the running agent until it reloads its MCP state. **Don't default to "restart your session"** — most agents have a lighter in-session reload.

Two distinct events to disambiguate before choosing the activation step:

| Trigger | Meaning | Activation goal |
|---------|---------|-----------------|
| **Config file changed** (you ran `mcp add` / `mcp remove` / hand-edited the config) | Agent's loaded config is stale vs disk | Agent must re-read the config file |
| **Server already in config but disconnected** (command was right but server died / network blip / dependency missing) | Config is fine; the connection process needs to be retried | Agent must re-spawn / reconnect the existing server entry |

Pick the right reload mechanism for your agent (see agent-specific notes below). After activation, verify with `claude mcp list` (or your agent's equivalent) — the server should show `Connected`.

### Claude Code

| Slash command (Claude-Code only) | Use after | What it does |
|----------------------------------|-----------|--------------|
| `/reload-plugins` | **Config file changed** (`.mcp.json` / `~/.claude.json` edited, `mcp add` run) | Re-reads plugins + MCP server list from disk and starts newly added / changed servers. Reports `N errors during load` if any new server fails to start. **Does NOT re-spawn servers that are already in an error/disconnected state** — config reload alone won't recover a crashed server |
| `/mcp` → "Reconnect" on the target server | **Server in error / disconnected state** (config unchanged, or after `/reload-plugins` left it Failed) | Re-spawns the existing server entry. Use whenever a server shows Disconnected/Failed regardless of why — `/reload-plugins` won't recover it |
| `/doctor` | After either of the above reports errors | Shows the per-server failure detail (command not found, env missing, endpoint unreachable, etc.) |

Sequence for a fresh `mcp add`: `claude mcp add ...` → `/reload-plugins` → if any server is Failed → `/doctor` (diagnose) → fix the underlying issue → `/mcp` Reconnect that server (`/reload-plugins` will NOT recover an error-state server even after the underlying issue is fixed).

> Empirical note: `/reload-plugins` is scoped to "pick up config changes", not "recover failed servers". Treat the two slash commands as orthogonal — config-change vs error-recovery — even though they look similar.

### Other agents

| Agent | Reload mechanism (best-effort summary — verify against your version) |
|-------|----------------------------------------------------------------------|
| Cursor | Settings → MCP → toggle server off/on, or restart Cursor |
| Antigravity | Restart the IDE (no in-session reload as of this writing) |
| Codex / Gemini CLI | Restart the CLI process |

If your agent isn't listed, check its docs for "MCP reload" or "MCP reconnect" — the underlying need is the same as the trigger table above.

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Default-advise "restart your session" after a config edit | Use the agent's in-session reload first (Claude Code: `/reload-plugins`) |
| 2 | Conflate "config changed" with "server disconnected" | Pick the trigger row above first, then map to the agent's command |
| 3 | Skip the agent's diagnostics command (Claude Code: `/doctor`) when the reload reports errors | Run diagnostics — that's where the per-server failure detail lives |
