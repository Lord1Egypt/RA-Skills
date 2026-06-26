---
name: install-memex-claw
description: Wire memex (the local-first MCP memory server) into an OpenClaw gateway — works wherever OpenClaw runs (Linux or macOS, VPS or workstation, self-hosted OpenClaw or Moonshot Kimi-Claw). Installs the memex-mvp daemon that auto-captures every OpenClaw session in ~/.openclaw/agents/main/sessions/ into a single SQLite + FTS5 corpus, and merges memex into the gateway's MCP-server config so the LLM gets 11 search/retrieval tools (memex_search, memex_recent, memex_overview, etc.). Auto-detects whether memex-mvp is already installed (e.g. via the generic install-memex skill for Claude Code) — if yes, skips install and just wires OpenClaw + back-fills past sessions; if no, does the full platform-aware install (Linux → systemd user-service, macOS → LaunchAgent). Zero questions to the user — discovery → actions → verification. Use when the user says "set up memex for OpenClaw", "wire memex into my OpenClaw", "make OpenClaw remember its sessions", "поставь memex здесь", or similar. PAIRS with the generic install-memex skill — if the user ALSO uses Claude Code, Cursor, Cline, Continue, or Zed on the same machine, recommend they run install-memex separately for those flows.
version: 3.0.0
metadata:
  openclaw:
    emoji: "🧠"
    homepage: https://memex.parallelclaw.ai
    requires:
      bins:
        - node
        - npm
---

# Install memex for OpenClaw

You are inside an OpenClaw agent. The user asked you to set up memex — the local-first MCP memory server — so that:

1. Every OpenClaw session in `~/.openclaw/agents/main/sessions/` is auto-captured into `~/.memex/data/memex.db` (SQLite + FTS5).
2. Existing past sessions are back-filled in one shot.
3. The OpenClaw gateway gains the `memex` MCP server with 11 search/retrieval tools (memex_search, memex_recent, memex_overview, memex_get_conversation, etc.).
4. Capture continues automatically thereafter (systemd user-service on Linux, LaunchAgent on macOS).

**Where you might be running:**

- 🖥️ **VPS** (Linux VPS hosting OpenClaw + maybe Hermes) — typical "always-on agent" deployment
- 💻 **macOS workstation** running OpenClaw alongside Claude Code / etc.
- 💻 **Linux workstation** (Pop!OS, Fedora, etc.) running OpenClaw locally
- 🤖 **Moonshot Kimi-Claw VPS** — also works (memex-mvp ≥ 0.11.5 auto-detects the merged-file Kimi-Claw layout)

All work the same way. Platform (Linux/macOS) determines daemon type. Deployment kind (self-hosted vs Kimi-Claw vs workstation) is auto-detected by the memex-mvp daemon.

**The contract: zero questions to the user. Discovery → actions → verification. Each step prints a single line of result. The final message tells the user exactly what to do next.**

---

## ⚠ For ClawHub reviewers, security scanners, and curious users

This skill installs `memex-mvp` from npm (if not already present) and wires it as an MCP server inside the OpenClaw gateway config. memex-mvp is the canonical install path for OpenClaw — the older "memex-openclaw OpenClaw-native plugin" approach (npm package `@parallelclaw/memex-openclaw`) is **deprecated** as of 2026-05-27; see deprecation notes in that package's README. The daemon path works on every OpenClaw deployment without security-scanner friction.

| Action | Why | Source |
|---|---|---|
| `npm install -g memex-mvp@latest` | Install the MCP server + the auto-capture daemon. Open-source MIT. **Skipped if already installed.** | [npmjs.com/package/memex-mvp](https://www.npmjs.com/package/memex-mvp), source: [github.com/parallelclaw/memex-mvp](https://github.com/parallelclaw/memex-mvp) |
| `memex-sync install` | Register the auto-capture daemon — systemd user-service on Linux, LaunchAgent on macOS. The daemon watches `~/.openclaw/agents/main/sessions/` and writes to `~/.memex/data/memex.db`. **Zero outbound network traffic.** **Skipped if daemon already running.** | LaunchAgent at `~/Library/LaunchAgents/com.parallelclaw.memex.sync.plist` or systemd unit at `~/.config/systemd/user/memex-sync.service` — both human-readable |
| `loginctl enable-linger $USER` (Linux only) | Without linger, user-systemd dies on SSH logout — daemon would stop between SSH sessions on a VPS. Skill tries this; if sudo needed, prints command and continues. | Standard systemd-user practice |
| Edit OpenClaw config at `~/.openclaw/openclaw.json` | Add a single `memex` entry under `mcp.servers`. **Merge, never overwrite** other entries. | The OpenClaw gateway reads this file at startup |
| `memex-sync scan` | One-shot back-fill of past OpenClaw sessions. Walks the sessions dir, parses each `<uuid>.jsonl`, writes to memex.db with `source='openclaw'`. Filters internal-state noise files (`.checkpoint.`, `.trajectory.`, `.reset.`). | `lib/ingest-file.js` in the source — open-source |

**Hard guarantees:**
- Every command is printed to the user before running it
- `sudo` is **NEVER** invoked by the skill (linger fallback prints the manual command for the user)
- OpenClaw config is **merged**, never overwritten — other plugins / MCP servers preserved
- memex at runtime emits **zero outbound network traffic** — local-first by design
- If memex-mvp is already installed (e.g. via the generic install-memex skill), this skill skips re-install and only wires OpenClaw — no surprise reinstalls

---

## Migration note for users who tried the deprecated `memex-openclaw` plugin

If the user previously installed `@parallelclaw/memex-openclaw` via `openclaw plugins install`, that plugin is now **deprecated**. The daemon-based approach below handles the same use case more reliably (no OpenClaw plugin security-scanner friction, no per-version manifest changes, no `allowConversationAccess` opt-in). To clean up before installing daemon-based:

```sh
# 1. Uninstall the old plugin (no-op if not installed)
openclaw plugins uninstall memex-openclaw 2>&1 || true

# 2. Restore openclaw.json from the .bak the plugin left (if you want to undo the plugin's edits)
[ -f ~/.openclaw/openclaw.json.bak ] && echo "found backup, you can restore via:" \
  && echo "  cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json"

# 3. Restart gateway so the old plugin stops loading
openclaw gateway restart
```

The data the old plugin wrote (`raw_type='openclaw-agent-end'` rows) stays in memex.db and remains searchable — the daemon's writes will appear alongside under the same source. UNIQUE(source, conversation_id, msg_id) prevents duplicates.

---

## Before this skill can be installed (one-time OpenClaw bootstrap)

If the user runs `openclaw skill install install-memex-claw` and gets back **"plugin not allowed" / "permission denied" / "skill plugin disabled"** — the gateway's permission model is blocking arbitrary skill execution by default. This is OpenClaw's safety guard, not specific to memex. Check your OpenClaw docs for the exact permission name (common: `plugins.allow: ["skill", …]` in `~/.openclaw/openclaw.json` or `skills.enabled: true`), set it once, restart the gateway, and retry.

---

## Prerequisite

You are running INSIDE an OpenClaw agent that can execute shell commands. If you're not OpenClaw, **stop**: this is the wrong skill — use [`install-memex`](https://clawhub.ai/sedelev/install-memex) instead.

---

## Step 1 — Discovery (run ALL checks first, then decide)

Run each as a separate shell command, capture the output. **Don't act on anything until all checks have answered.**

```sh
# 1. Are we inside OpenClaw?
which openclaw 2>/dev/null || find / -maxdepth 4 -name "openclaw" -type d 2>/dev/null | head -3

# 2. Platform — Linux or Darwin (macOS)
uname -s

# 3. Node version (need ≥ 22.12 for memex-mvp ≥ 0.11.x)
node --version

# 4. Existing memex install?
which memex && memex --version 2>&1 || echo "NO_MEMEX"

# 5. Existing memex daemon running?
memex-sync status 2>/dev/null | head -5 || echo "NO_DAEMON"

# 6. Existing OpenClaw sessions?
ls -1 ~/.openclaw/agents/main/sessions/ 2>/dev/null \
  | grep -E '^[0-9a-f-]+\.jsonl$' | wc -l

# 7. On Linux: systemd user-instance available?
[ "$(uname -s)" = "Linux" ] && systemctl --user --version 2>/dev/null | head -1 \
  || echo "macOS or no-systemd"

# 8. OpenClaw gateway config
ls -la ~/.openclaw/openclaw.json 2>&1

# 9. Was the deprecated memex-openclaw plugin previously installed?
ls -la ~/.openclaw/npm/node_modules/@parallelclaw/memex-openclaw 2>/dev/null \
  || echo "no old plugin"
```

**Branch on results:**

| Discovery state | Action |
|---|---|
| **OpenClaw not found** | Stop. Tell user: "This skill is for OpenClaw agents. For Claude Code / Cursor / etc., use `install-memex` instead." |
| **Node < 22.12** | Stop. Print upgrade instructions (nvm, distro pkg manager). Don't auto-install Node. |
| **Deprecated plugin found at ~/.openclaw/npm/node_modules/@parallelclaw/memex-openclaw** | Run the migration block from the section above BEFORE proceeding to Step 2. |
| **memex ≥ 0.11.6 + daemon running** | Skip Steps 2–4. Go directly to Step 5 (MCP wiring). Tell user: "memex already installed and running — just need to wire it into OpenClaw." |
| **memex installed but < 0.11.6** | Upgrade in-place: `npm install -g memex-mvp@latest`. Continue (daemon auto-restarts if running). |
| **memex installed, daemon not running** | Run `memex-sync install` (Step 3). Skip the npm install. |
| **memex not installed** | Full path: Step 2 (install) → Step 3 (daemon) → Step 4 (back-fill) → Step 5 (wire) → Step 6 (restart). |
| **Linux without systemd** (e.g. minimal container) | Fall back to `nohup memex-sync &`. Tell user the auto-restart limitation. |
| **No openclaw.json** | Ask the user (ONE question allowed): "Where does your OpenClaw gateway store its config?" — proceed with their answer. |

Report each result back as **facts, not questions**:

> "✓ OpenClaw detected at /usr/local/bin/openclaw"  
> "✓ Linux + systemd 255 — will use user-systemd for daemon"  
> "✓ Node 22.22.2 — ok"  
> "→ memex not installed — installing 0.11.6+"  
> "✓ Found 60 OpenClaw sessions ready to back-fill"  
> "⚠ Deprecated memex-openclaw plugin detected — will uninstall first"

---

## Step 2 — Install memex-mvp (skip if already at ≥ 0.11.6)

```sh
npm install -g memex-mvp@latest
```

If `EACCES` (no permission to write to npm global prefix), apply the standard fix — **never use sudo**:

```sh
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
echo 'export PATH=$HOME/.npm-global/bin:$PATH' >> ~/.zshrc 2>/dev/null
echo 'export PATH=$HOME/.npm-global/bin:$PATH' >> ~/.bashrc 2>/dev/null
export PATH=$HOME/.npm-global/bin:$PATH
npm install -g memex-mvp@latest
```

Verify:

```sh
memex --version    # must print 0.11.6 or later
```

---

## Step 3 — Install the auto-capture daemon (skip if already running)

```sh
memex-sync install
```

Platform-specific behavior (handled automatically by memex-sync):

| Platform | What `memex-sync install` does |
|---|---|
| **macOS** (`uname -s` = Darwin) | Writes `~/Library/LaunchAgents/com.parallelclaw.memex.sync.plist`, runs `launchctl load`. Daemon auto-starts on every login. |
| **Linux + systemd-user** | Writes `~/.config/systemd/user/memex-sync.service`, runs `systemctl --user daemon-reload && enable && start`. Tries `loginctl enable-linger $USER` so daemon survives SSH logout. |
| **Linux without systemd** | Exits with "systemctl --user not available". Fall back: `nohup memex-sync > /tmp/memex.log 2>&1 &` — works but won't auto-restart on reboot. |

If `loginctl enable-linger` needs sudo, the install output prints the exact command. **Tell the user that line verbatim** — don't try to sudo yourself.

Verify daemon running:

```sh
memex-sync status
# Should show: process: running (pid XXXX)
```

---

## Step 4 — Back-fill existing sessions

```sh
memex-sync scan
```

`memex-sync scan` walks the source dirs (Claude Code on workstations, OpenClaw on VPS, etc.), reads each `<uuid>.jsonl`, filters internal-state noise (`.checkpoint.*`, `.trajectory.*`, `.reset.*` snapshots — they'd double-count), and writes to memex.db.

Expected output:

```
=== Claude Code + Cowork ===
- skipping claude-code: directory not found at /home/user/.claude/projects   (on VPS without Claude Code)
- skipping claude-cowork: directory not found at ...                          (on Linux — Cowork is macOS-only)
scanning openclaw: /home/user/.openclaw/agents/main/sessions
+ openclaw-abc12345.jsonl ← 23 msgs from openclaw (ai-titled)
+ openclaw-def67890.jsonl ← 41 msgs from openclaw
…
scanned 60 files · 1316 messages emitted
```

If the daemon was already running (Step 3 skipped), `scan` is still useful — it catches anything the daemon's chokidar may have raced on startup.

### Step 4b — Channel-aware re-import (recommended once after first install)

memex-mvp v0.11.5+ does two-mode auto-detection (**self-hosted** OpenClaw with separate `<uuid>.jsonl` per session vs **Moonshot Kimi-Claw** with merged-file layout) and channel routing (Telegram chat / Kimi-web session / openclaw-cli). After the first `scan`, run:

```sh
memex-sync backfill-channels --yes
```

This wipes existing `source = 'openclaw'` rows and re-imports with the current channel-aware pipeline. Use it once after upgrading from any memex-mvp earlier than 0.11.5, and any time the user reports "messages from one chat are merged into another" symptoms.

---

## Step 5 — Wire memex as an MCP server in openclaw.json (REQUIRED for LLM retrieval)

The daemon handles capture; the memex-mvp MCP server exposes `memex_search`, `memex_recent`, `memex_overview`, etc. to the OpenClaw LLM toolset. **Without this step, the LLM has no way to search memex from inside a conversation** — it would fall back to raw `sqlite3` shell calls (or fail).

### Config-key gotcha

OpenClaw 2026.5+ reads MCP servers from `cfg.mcp.servers` (nested), NOT from the top-level `cfg.mcpServers` (flat). Verify with `openclaw mcp list` after the merge — must show `memex`.

Find the absolute path to `memex` (MCP stdio doesn't inherit shell PATH):

```sh
which memex
```

Merge memex into `~/.openclaw/openclaw.json` at `mcp.servers.memex` (preserves other servers; idempotent):

```sh
python3 <<'PY'
import json, shutil
from pathlib import Path
p = Path.home() / ".openclaw" / "openclaw.json"
cfg = json.loads(p.read_text())
memex_bin = shutil.which("memex")
if not memex_bin:
    print("ERROR: memex binary not in PATH; rerun Step 2")
    raise SystemExit(1)

# Correct path is mcp.servers (nested), NOT mcpServers (flat).
mcp_section = cfg.setdefault("mcp", {})
servers = mcp_section.setdefault("servers", {})
servers["memex"] = {"command": memex_bin, "args": [], "env": {}}

# Clean up any legacy top-level mcpServers.memex from earlier skill versions
stale = cfg.get("mcpServers", {})
if isinstance(stale, dict) and "memex" in stale:
    del stale["memex"]
    if not stale:
        cfg.pop("mcpServers", None)
    print("cleaned stale mcpServers.memex from previous skill version")

p.write_text(json.dumps(cfg, indent=2))
print(f"memex MCP wired at {p} → {memex_bin}")
PY
```

**Verify the merge worked (THREE checks)**:

```sh
# 1. Config has the right key
python3 -c "
import json
from pathlib import Path
cfg = json.loads((Path.home() / '.openclaw' / 'openclaw.json').read_text())
s = cfg.get('mcp', {}).get('servers', {}).get('memex')
print('mcp.servers.memex:', json.dumps(s, indent=2) if s else 'MISSING')
"

# 2. OpenClaw's own listing recognises it (authoritative check)
openclaw mcp list 2>&1 | grep -i memex
# Must show 'memex' or similar.

# 3. (after restart, see Step 7d) LLM toolset includes memex_search
```

---

## Step 6 — Restart OpenClaw

```sh
openclaw gateway restart
```

Wait ~5 seconds, then check logs:

```sh
journalctl --user -u openclaw -n 50 --no-pager 2>/dev/null | grep -iE "memex|mcp" | tail -10 \
  || tail -100 ~/.openclaw/logs/gateway.log 2>/dev/null | grep -iE "memex|mcp" | tail -10
```

You should see the gateway picking up the memex MCP server.

---

## Step 7 — Verify (four checks — all must pass)

### 7a. Daemon is alive and capturing

```sh
memex-sync status
# process: running (pid XXXX)

# Watch the daemon log for a few seconds
tail -10 ~/.memex/logs/memex-sync.log 2>/dev/null
```

### 7b. memex.db has OpenClaw rows

```sh
sqlite3 ~/.memex/data/memex.db <<'SQL'
.headers on
.mode column
SELECT COUNT(*) AS total_openclaw_rows,
       MIN(ts) AS earliest_ts,
       MAX(ts) AS latest_ts
  FROM messages
 WHERE source = 'openclaw';
SQL
```

Expected: total_openclaw_rows ≥ 1 (much more if you ran back-fill on existing sessions).

### 7c. Live capture writes a NEW row

```sh
PRE=$(sqlite3 ~/.memex/data/memex.db \
  "SELECT COUNT(*) FROM messages WHERE source='openclaw'")
echo "PRE: $PRE"

# >>> NOW send a test message in OpenClaw, wait for reply <<<
sleep 8

POST=$(sqlite3 ~/.memex/data/memex.db \
  "SELECT COUNT(*) FROM messages WHERE source='openclaw'")
echo "POST: $POST  diff=$((POST - PRE))"

sqlite3 ~/.memex/data/memex.db \
  "SELECT id, role, datetime(ts,'unixepoch','localtime') AS when_,
          substr(text,1,60) AS preview, conversation_id
     FROM messages WHERE source='openclaw' ORDER BY ts DESC LIMIT 5"
```

Expected: diff ≥ 2 (user + assistant), recent rows include your test message.

### 7d. LLM toolset includes memex tools (requires a FRESH OpenClaw session)

MCP tools are loaded into the LLM's function-calling toolset at **session start**. The session in which you just ran `openclaw gateway restart` has the OLD toolset. To verify memex is exposed:

1. Start a **fresh** OpenClaw conversation.
2. Ask the agent: "Find the earliest conversations from April using memex_search."
3. The agent should:
   - Mention `memex_search` in its reasoning or just call it
   - Return real results (IDs, timestamps, snippets from `~/.memex/data/memex.db`)
   - NOT fall back to direct `sqlite3` calls

If the agent doesn't see memex tools → re-check Step 5 (probably `mcp.servers` vs `mcpServers` key issue) and `openclaw mcp list`.

---

## Step 8 — Final message to user

After all checks pass:

```
✅ memex wired into OpenClaw.

Captured:
  • Every new OpenClaw turn writes to ~/.memex/data/memex.db within seconds
    (the memex-sync daemon watches ~/.openclaw/agents/main/sessions/)
  • Past sessions back-filled (Step 4)
  • Channel routing works for self-hosted OpenClaw + Moonshot Kimi-Claw

Search:
  • From inside OpenClaw chat: ask the model to search its memory — uses memex_search
  • From CLI: `memex search "query"` or `memex overview`
  • From any other MCP-enabled client on the same machine (Claude Code, Cursor, etc.) —
    the memex MCP server exposes 11 search tools

Daemon:
  • Status check: `memex-sync status`
  • Auto-restarts on login (LaunchAgent on macOS, systemd-user on Linux)
  • Survives SSH logout if linger is enabled

Pair with:
  • install-memex (generic skill) — if you also use Claude Code, Cursor, Cline, etc.
    on this same machine, they all share ~/.memex/data/memex.db
  • memex-hermes (pip package) — if you run Hermes Agent on this machine
```

---

## What this skill explicitly does NOT do

- ❌ Install Node.js (manual step if needed — print instructions, don't auto-install)
- ❌ Use sudo. Ever. If permissions block something, surface the manual fix and stop.
- ❌ Install the deprecated `@parallelclaw/memex-openclaw` plugin. The daemon path supersedes it.
- ❌ Overwrite existing `mcp.servers` entries. Merge.
- ❌ Configure outbound network access. memex is local-first.

---

## Edge cases

| Condition | What to do |
|---|---|
| OpenClaw < 2026.5 | The MCP-server `mcp.servers` key is 2026.5+. Older versions used different keys — check `openclaw config show` to find the right one and adapt Step 5. |
| memex.db locked (WAL contention) | Wait 1 second, retry. SQLite WAL handles concurrent readers/writers. |
| Plugin install permission denied | Bootstrap section at the top of this skill — user needs to allow third-party skills once. |
| Linger fails with sudo prompt | Print the exact `sudo loginctl enable-linger $USER` line, ask the user to run it once, and continue without sudo. |
| User has the deprecated memex-openclaw plugin AND already-captured data from it | The plugin's data (raw_type='openclaw-agent-end') stays in memex.db. Daemon's new writes will appear alongside under the same source. UNIQUE constraint prevents duplicates. |
| User wants to delete legacy plugin data | `sqlite3 ~/.memex/data/memex.db "DELETE FROM messages WHERE source='openclaw' AND json_extract(metadata,'$.raw_type')='openclaw-agent-end'"` — careful, irreversible |
| openclaw.json doesn't exist | Ask the user ONE question for the path. Don't auto-create. |

---

## Safety rules — read before starting

- Never sudo. Never edit system files. Never modify `$PATH` outside `~/.zshrc` / `~/.bashrc` with the user's consent.
- Always confirm before deleting anything from the user's machine.
- Always preserve existing config keys when editing JSON.
- Print every shell command to the user before running it.
- If any step fails, **stop**. Don't try to recover by trying random things. Print the error and ask the user.

---

## Begin

Run Step 1 (Discovery) now. Print results. Branch as the table indicates.
