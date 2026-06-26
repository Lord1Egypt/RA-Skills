# MCP Server Connection Diagnostics

Diagnose and resolve MCP server connection issues.

## Step 0: Disambiguate "stale config" vs "server crashed"

If the failure happened **right after** an `mcp add/remove` or a config edit, the running agent may be holding **stale config** — disk is updated, agent's in-memory state isn't. This is different from "the server entry was fine but the server itself died".

Pick the activation step per trigger (see `add.md` → "Activate the change" for full per-agent procedure):

| Trigger | What you need | Claude Code command (other agents: see add.md) |
|---------|---------------|------------------------------------------------|
| Config file just changed (`mcp add` / `.mcp.json` edit) | Re-read config from disk + start newly-added servers | `/reload-plugins` |
| Server in error / disconnected state (config unchanged, or `/reload-plugins` left it Failed) | Re-spawn the existing server entry | `/mcp` → Reconnect |
| Either reload reports errors | Per-server failure detail | `/doctor` (Claude Code) |

The two slash commands are **orthogonal**, not redundant. `/reload-plugins` is for config sync; it will NOT recover a server that is already in an error state — even after you fix the underlying cause. Always use `/mcp` Reconnect once the cause is fixed.

If the in-session reload command doesn't exist for your agent (or it reports persistent errors after one retry), restart the agent. Then proceed to the steps below to diagnose root cause.

## Diagnostic Steps

### 1. Quick Status Check (Start Here)

```bash
# List all MCP servers and their connection status
claude mcp list
```

If the server appears as **Disconnected** or is missing entirely, proceed to Step 2.

### 2. Verify Configuration Files (Check ALL in order)

| Priority | File | Description |
|----------|------|-------------|
| 1 | `~/.claude.json` | **Claude Code global MCP config** (mcpServers section) |
| 2 | `~/.claude/settings.json` | Claude Code settings mcpServers |
| 3 | `~/.claude/settings.local.json` | Local overrides |
| 4 | `.mcp.json` (project root) | Project-level MCP config |
| 5 | `~/.config/claude/mcp.json` | User-level (legacy) |
| 6 | `~/.utcp_config.json` | UTCP-specific config |
| 7 | Plugin cache (`~/.claude/plugins/cache/`) | MCP servers provided by plugins |

**Always check `~/.claude.json` first** — this is the primary file where Claude Code stores MCP server configurations.

### 3. Common Errors and Solutions

#### "Connection closed" / "MCP error -32000"

**Cause**: Server process exits immediately after starting.

**Check**:
- Command path is correct (`which npx`, `which node`)
- Environment variables are set
- Native module build failures

#### "Failed to reconnect to [server-name]"

**Cause**: Previously connected server is no longer responding.

**Resolution**:
1. Check server status with `/mcp` command
2. Restart server or verify configuration

#### uvx-based MCP servers on Windows (pydantic-core / onnxruntime traps)

Two patterns that bite Python MCP servers (mcp-server-qdrant, etc.) launched via `uvx` on Windows:

**Trap A — uvx defaults to a Python version with no prebuilt wheels**

If uvx runs the bleeding-edge Python (e.g., 3.14 right after release), packages like `pydantic-core` may not yet publish wheels for that version. uvx then pulls the sdist and tries to compile the Rust crate, which often times out under the MCP launcher's startup budget.

- **Symptom**: log shows `cargo rustc ... pydantic-core` or `maturin failed`, MCP shows `Failed to connect`
- **Fix**: pin the interpreter in the MCP command — change `uvx mcp-server-qdrant` to `uvx --python 3.12 mcp-server-qdrant` (or any version with prebuilt wheels)
- **CLI**: `claude mcp remove <name> -s <scope> && claude mcp add <name> --scope <scope> -e ... -- uvx --python 3.12 <package>`

**Trap B — `onnxruntime` DLL load failure (missing VC++ Redistributable)**

Packages that bundle `onnxruntime` (e.g., `fastembed`, used by `mcp-server-qdrant` for local embeddings) need the Microsoft Visual C++ Runtime on Windows. A fresh machine without VC++ Redist installed will install onnxruntime fine but fail at import.

- **Symptom**: `ImportError: DLL load failed while importing onnxruntime_pybind11_state: <module-not-found>`
- **Check**: `reg query "HKLM\SOFTWARE\WOW6432Node\Microsoft\VisualStudio\14.0\VC\Runtimes\X64" /v Installed` — empty result = not installed
- **Fix**: install Microsoft Visual C++ 2015-2022 Redistributable x64 (`choco install vcredist140 -y`, `winget install Microsoft.VCRedist.2015+.x64`, or the MSI from microsoft.com). No reboot required for most apps; re-run `/reload-plugins` after install

#### UTCP code-mode Specific Issues

**isolated-vm build failure**:
- Node.js version compatibility (LTS 22.x recommended)
- No prebuilt binaries for arm64 macOS
- Fix: `asdf local nodejs 22.14.0` then reinstall

**Empty config file**:
- If `~/.utcp_config.json` is `{}`, initialization failed
- Minimum required config:
```json
{
  "load_variables_from": [],
  "manual_call_templates": [],
  "tool_repository": {
    "tool_repository_type": "in_memory"
  },
  "tool_search_strategy": {
    "tool_search_strategy_type": "tag_and_description_word_match"
  },
  "post_processing": []
}
```

### 4. Check Logs

```bash
# Latest MCP debug logs (UUID-based filenames)
ls -lt ~/.claude/debug/ | head -5

# Read a specific log
cat ~/.claude/debug/<uuid>.txt
```

### 5. Manual Server Test

Run the server command directly outside Claude Code to see raw errors:

```bash
# npx-based server
npx -y @utcp/code-mode-mcp

# npx with environment variables
UTCP_CONFIG_FILE=~/.utcp_config.json npx -y @utcp/code-mode-mcp

# uvx-based server (e.g., serena, postgres)
uvx --from "git+https://github.com/oraios/serena" serena start-mcp-server --context claude-code
```

**Key**: Copy the exact `command` + `args` from `~/.claude.json` and run it in your terminal. The error output will reveal the root cause (missing dependency, wrong argument, auth failure, etc.).
