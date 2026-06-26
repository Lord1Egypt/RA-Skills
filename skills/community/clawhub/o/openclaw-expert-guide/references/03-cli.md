# OpenClaw CLI — Complete Command Reference

> **Source:** All 53 CLI documentation pages from https://docs.openclaw.ai/cli  
> **Fetched:** 2026-04-24  
> **Entry point:** `openclaw` — the main CLI binary

---

## Table of Contents

1. [Global Flags & Output Modes](#global-flags--output-modes)
2. [ACP](#acp)
3. [Agent](#agent)
4. [Agents](#agents)
5. [Approvals / exec-policy](#approvals--exec-policy)
6. [Backup](#backup)
7. [Browser](#browser)
8. [Channels](#channels)
9. [Clawbot (legacy alias)](#clawbot-legacy-alias)
10. [Completion](#completion)
11. [Config](#config)
12. [Configure](#configure)
13. [Cron](#cron)
14. [Daemon (legacy alias)](#daemon-legacy-alias)
15. [Dashboard](#dashboard)
16. [Devices](#devices)
17. [Directory](#directory)
18. [DNS](#dns)
19. [Docs](#docs)
20. [Doctor](#doctor)
21. [Flows (redirect → tasks)](#flows-redirect--tasks)
22. [Gateway](#gateway)
23. [Health](#health)
24. [Hooks](#hooks)
25. [Infer / capability](#infer--capability)
26. [Logs](#logs)
27. [MCP](#mcp)
28. [Memory](#memory)
29. [Message](#message)
30. [Models](#models)
31. [Node](#node)
32. [Nodes](#nodes)
33. [Onboard](#onboard)
34. [Pairing](#pairing)
35. [Plugins](#plugins)
36. [Proxy](#proxy)
37. [QR](#qr)
38. [Reset](#reset)
39. [Sandbox](#sandbox)
40. [Secrets](#secrets)
41. [Security](#security)
42. [Sessions](#sessions)
43. [Setup](#setup)
44. [Skills](#skills)
45. [Status](#status)
46. [System](#system)
47. [Tasks](#tasks)
48. [TUI / chat / terminal](#tui--chat--terminal)
49. [Uninstall](#uninstall)
50. [Update](#update)
51. [Voicecall (plugin)](#voicecall-plugin)
52. [Webhooks](#webhooks)
53. [Wiki](#wiki)
54. [Quick Reference Table](#quick-reference-table)

---

## Global Flags & Output Modes

Applied to **every** `openclaw` command:

| Flag | Description |
|---|---|
| `--dev` | Isolate state under `~/.openclaw-dev`; shifts default ports |
| `--profile <name>` | Isolate state under `~/.openclaw-<name>` |
| `--container <name>` | Target a named container for execution |
| `--no-color` | Disable ANSI colors (`NO_COLOR=1` env also works) |
| `--update` | Shorthand for `openclaw update` (source installs only) |
| `-V`, `--version`, `-v` | Print version and exit |

**Output modes:**
- ANSI colors + progress indicators render only in TTY.
- OSC-8 hyperlinks for supported terminals; falls back to plain URLs.
- `--json` disables styling for clean machine-readable output.
- `--no-color` keeps human layout but disables ANSI.
- Long-running commands show a progress indicator (OSC 9;4 when supported).

**Chat slash commands** (inside TUI sessions):

| Command | Purpose |
|---|---|
| `/status` | Show session + model status |
| `/trace` | Toggle trace logging |
| `/config` | Open configure wizard inline |
| `/debug` | Verbose debug output (requires `commands.debug: true` in config to be available) |
| `/models` | Model selection |
| `/new` | New session |
| `/reset` | Reset session |
| `/dreaming on\|off\|status` | Dreaming control |
| `/auth [provider]` | Local-mode auth |

---

## ACP

**Synopsis:** `openclaw acp [options]`

**Description:** Agent Client Protocol bridge — speaks ACP over stdio for IDEs, forwards prompts to the Gateway over WebSocket. Keeps ACP sessions mapped to Gateway session keys.

Use `openclaw acp` when an IDE/client speaks ACP and you want it to drive an OpenClaw Gateway session. NOT the same as ACP harness sessions.

### Options

| Flag | Description |
|---|---|
| `--url <url>` | Gateway WebSocket URL |
| `--token <token>` | Gateway auth token |
| `--token-file <path>` | Read token from file (preferred over inline) |
| `--password <password>` | Gateway password |
| `--password-file <path>` | Read password from file |
| `--session <key>` | Default session key |
| `--session-label <label>` | Default session label to resolve |
| `--require-existing` | Fail if session key/label does not exist |
| `--reset-session` | Reset session key before first use |
| `--no-prefix-cwd` | Do not prefix prompts with working directory |
| `--provenance <off\|meta\|meta+receipt>` | ACP provenance metadata |
| `--verbose, -v` | Verbose logging to stderr |

### Subcommand: `acp client`

Debug ACP client — spawns the bridge and lets you type prompts interactively.

| Flag | Description |
|---|---|
| `--cwd <dir>` | Working directory for ACP session |
| `--server <command>` | ACP server command (default: `openclaw`) |
| `--server-args <args...>` | Extra args passed to ACP server |
| `--server-verbose` | Enable verbose logging on ACP server |
| `--verbose, -v` | Verbose client logging |

### Examples

```bash
openclaw acp
openclaw acp --url wss://gateway-host:18789 --token <token>
openclaw acp --url wss://gateway-host:18789 --token-file ~/.openclaw/gateway.token
openclaw acp --session agent:main:main
openclaw acp --session-label "support inbox"
openclaw acp --session agent:main:main --reset-session
openclaw acp client
```

### Zed Editor Config

```json
{
  "agent_servers": {
    "OpenClaw ACP": {
      "type": "custom",
      "command": "openclaw",
      "args": ["acp"]
    }
  }
}
```

### ACP Compatibility Matrix

| Feature | Status |
|---|---|
| `initialize`, `newSession`, `prompt`, `cancel` | ✅ Implemented |
| `listSessions`, slash commands | ✅ Implemented |
| `loadSession` | ⚠️ Partial (text history only, no tool history) |
| Prompt content (text, resource, images) | ⚠️ Partial |
| Session modes | ⚠️ Partial |
| Tool streaming | ⚠️ Partial |
| Per-session MCP servers (`mcpServers`) | ❌ Unsupported |
| Client filesystem methods | ❌ Unsupported |
| Client terminal methods | ❌ Unsupported |
| Session plans / thought streaming | ❌ Unsupported |

### Notes/Gotchas

- Prefer `--token-file`/`--password-file` over inline secrets (visible in process listings).
- Env vars: `OPENCLAW_GATEWAY_TOKEN`, `OPENCLAW_GATEWAY_PASSWORD`.
- Setting `--url` does NOT reuse config/env credentials — pass explicit `--token`/`--password`.
- ACP client auto-approval is allowlist-based (scoped reads, readonly search tools only).
- `OPENCLAW_SHELL=acp` is set in ACP backend child processes; `acp-client` for the debug client.

---

## Agent

**Synopsis:** `openclaw agent [options]`

**Description:** Run an agent turn via the Gateway. Pass at least one session selector (`--to`, `--session-id`, or `--agent`).

### Options

| Flag | Description |
|---|---|
| `-m, --message <text>` | Required message body |
| `-t, --to <dest>` | Recipient to derive session key |
| `--session-id <id>` | Explicit session id |
| `--agent <id>` | Agent id; overrides routing bindings |
| `--thinking <level>` | Thinking level: `off\|minimal\|low\|medium\|high\|xhigh\|adaptive\|max` |
| `--verbose <on\|off>` | Persist verbose level for session |
| `--channel <channel>` | Delivery channel |
| `--reply-to <target>` | Delivery target override |
| `--reply-channel <channel>` | Delivery channel override |
| `--reply-account <id>` | Delivery account override |
| `--local` | Run embedded agent directly (no Gateway) |
| `--deliver` | Send reply back to selected channel/target |
| `--timeout <seconds>` | Override agent timeout (default 600) |
| `--json` | JSON output |

### Examples

```bash
openclaw agent --to +15555550123 --message "status update" --deliver
openclaw agent --agent ops --message "Summarize logs"
openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium
openclaw agent --agent ops --message "Generate report" --deliver --reply-channel slack --reply-to "#reports"
openclaw agent --agent ops --message "Run locally" --local
```

### Notes/Gotchas

- Gateway mode falls back to embedded when Gateway request fails; use `--local` to force embedded.
- `--local` still preloads plugin registry.
- `--channel`, `--reply-channel`, `--reply-account` affect reply delivery, not session routing.

---

## Agents

**Synopsis:** `openclaw agents [subcommand] [options]`

**Description:** Manage isolated agents (workspaces, auth, routing). No subcommand = `agents list`.

### Subcommands

#### `agents list`
```bash
openclaw agents list
openclaw agents list --bindings
openclaw agents list --json
```

#### `agents add [name]`
```bash
openclaw agents add work --workspace ~/.openclaw/workspace-work
openclaw agents add ops --workspace ~/.openclaw/workspace-ops --bind telegram:ops --non-interactive
```

Options: `--workspace <dir>`, `--model <id>`, `--agent-dir <dir>`, `--bind <channel[:accountId]>` (repeatable), `--non-interactive`, `--json`

> **Note:** `main` is reserved; cannot be used as a new agent id.

#### `agents bindings`
```bash
openclaw agents bindings
openclaw agents bindings --agent work --json
```

Options: `--agent <id>`, `--json`

#### `agents bind`
```bash
openclaw agents bind --agent work --bind telegram:ops --bind discord:guild-a
```

Options: `--agent <id>`, `--bind <channel[:accountId]>` (repeatable), `--json`

#### `agents unbind`
```bash
openclaw agents unbind --agent work --bind telegram:ops
openclaw agents unbind --agent work --all
```

Options: `--agent <id>`, `--bind` (repeatable), `--all`, `--json`

#### `agents delete <id>`
```bash
openclaw agents delete work
openclaw agents delete work --force
```

Options: `--force` (skip confirmation), `--json`

> Workspace/state directories are moved to Trash (not hard-deleted). `main` cannot be deleted.

#### `agents set-identity`
```bash
openclaw agents set-identity --workspace ~/.openclaw/workspace --from-identity
openclaw agents set-identity --agent main --name "OpenClaw" --emoji "🦞" --avatar avatars/openclaw.png
```

Options: `--agent <id>`, `--workspace <dir>`, `--identity-file <path>`, `--from-identity`, `--name`, `--theme`, `--emoji`, `--avatar`, `--json`

### Notes/Gotchas

- Binding without `accountId` matches channel default account only.
- `accountId: "*"` is a channel-wide fallback (less specific than explicit account binding).
- `--from-identity` reads from workspace root `IDENTITY.md` or explicit `--identity-file`.

---

## Approvals / exec-policy

**Synopsis:** `openclaw approvals [subcommand] [options]`  
**Alias:** `openclaw exec-approvals`

**Description:** Manage exec approvals for local host, gateway host, or a node host.

### `openclaw exec-policy` (local convenience)

```bash
openclaw exec-policy show
openclaw exec-policy show --json
openclaw exec-policy preset yolo
openclaw exec-policy preset cautious
openclaw exec-policy set --host gateway --security full --ask off --ask-fallback full
```

> Local-only. Updates local config + approvals file. `--host node` is rejected.

### Core Commands

```bash
# Get effective policy
openclaw approvals get
openclaw approvals get --node <id|name|ip>
openclaw approvals get --gateway

# Replace approvals from file/stdin
openclaw approvals set --file ./exec-approvals.json
openclaw approvals set --stdin <<'EOF'
{ version: 1, defaults: { security: "full", ask: "off" } }
EOF
openclaw approvals set --node <id|name|ip> --file ./exec-approvals.json
openclaw approvals set --gateway --file ./exec-approvals.json

# Allowlist management
openclaw approvals allowlist add "~/Projects/**/bin/rg"
openclaw approvals allowlist add --agent main --node <id|name|ip> "/usr/bin/uptime"
openclaw approvals allowlist add --agent "*" "/usr/bin/uname"
openclaw approvals allowlist remove "~/Projects/**/bin/rg"
```

### Common Options

All `get`/`set`/`allowlist` support:
- `--node <id|name|ip>`
- `--gateway`
- `--url <url>`, `--token <token>`, `--timeout <ms>`, `--json`

`allowlist add|remove` also supports:
- `--agent <id>` (defaults to `*` — applies to all agents)

### Notes/Gotchas

- Approvals files stored at `~/.openclaw/exec-approvals.json`.
- Host approvals file is the enforceable source of truth.
- Node host must advertise `system.execApprovals.get/set`.
- Set `tools.exec.host=gateway` to use host exec even with sandbox configured.

---

## Backup

**Synopsis:** `openclaw backup create [options]` / `openclaw backup verify <archive>`

**Description:** Create restorable backup archives of OpenClaw state, config, credentials, sessions, and workspace.

### Commands

```bash
openclaw backup create
openclaw backup create --output ~/Backups
openclaw backup create --dry-run --json
openclaw backup create --verify
openclaw backup create --no-include-workspace
openclaw backup create --only-config
openclaw backup verify ./2026-03-09T00-00-00.000Z-openclaw-backup.tar.gz
```

### Options

| Flag | Description |
|---|---|
| `--output <dir>` | Output directory (default: CWD) |
| `--dry-run` | Print actions without writing archive |
| `--json` | Machine-readable output |
| `--verify` | Validate archive after writing |
| `--no-include-workspace` | Skip workspace discovery |
| `--only-config` | Back up only the active JSON config file |

### What Gets Backed Up

- State directory (`~/.openclaw`)
- Active config file
- Resolved `credentials/` directory
- Workspace directories from current config (unless `--no-include-workspace`)

### Notes/Gotchas

- Archive includes `manifest.json` with resolved source paths.
- Timestamped `.tar.gz` output in CWD by default.
- Existing archive files are NEVER overwritten.
- If config is invalid and workspace backup enabled, fails fast. Rerun with `--no-include-workspace`.

---

## Browser

**Synopsis:** `openclaw browser [--browser-profile <name>] <subcommand> [options]`

**Description:** Manage OpenClaw's browser control — lifecycle, profiles, tabs, snapshots, navigation, input, state, and debugging.

> Requires bundled browser plugin to be in `plugins.allow`.

### Common Flags

| Flag | Description |
|---|---|
| `--url <gatewayWsUrl>` | Gateway WebSocket URL |
| `--token <token>` | Gateway token |
| `--timeout <ms>` | Request timeout |
| `--expect-final` | Wait for final response |
| `--browser-profile <name>` | Browser profile (default from config) |
| `--json` | Machine-readable output |

### Quick Start

```bash
openclaw browser profiles
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

### Lifecycle

```bash
openclaw browser status
openclaw browser doctor        # CDP readiness check
openclaw browser start
openclaw browser stop
openclaw browser --browser-profile openclaw reset-profile
```

### Profiles

```bash
openclaw browser profiles
openclaw browser create-profile --name work --color "#FF5A36"
openclaw browser create-profile --name chrome-live --driver existing-session
openclaw browser create-profile --name remote --cdp-url https://browser-host.example.com
openclaw browser delete-profile --name work
openclaw browser --browser-profile work tabs
```

**Profile types:**
- `openclaw`: dedicated OpenClaw-managed Chrome (isolated user data dir)
- `user`: existing signed-in Chrome via Chrome DevTools MCP
- custom CDP profiles: point at local/remote CDP endpoint

### Tabs & Navigation

```bash
openclaw browser tabs
openclaw browser tab new
openclaw browser tab select 2
openclaw browser tab close 2
openclaw browser open https://docs.openclaw.ai
openclaw browser focus <targetId>
openclaw browser close <targetId>
openclaw browser navigate https://example.com
```

### Snapshot / Screenshot

```bash
openclaw browser snapshot
openclaw browser snapshot --urls          # append discovered link destinations
openclaw browser screenshot
openclaw browser screenshot --full-page
openclaw browser screenshot --ref e12
openclaw browser screenshot --labels       # overlay current snapshot refs
```

> `--full-page` cannot combine with `--ref`/`--element`. `existing-session`/`user` profiles support `--ref` screenshots but not CSS `--element`.

### UI Automation (ref-based)

```bash
openclaw browser click <ref>
openclaw browser type <ref> "hello"
openclaw browser press Enter
openclaw browser hover <ref>
openclaw browser scrollintoview <ref>
openclaw browser drag <startRef> <endRef>
openclaw browser select <ref> OptionA OptionB
openclaw browser fill --fields '[{"ref":"1","value":"Ada"}]'
openclaw browser wait --text "Done"
openclaw browser evaluate --fn '(el) => el.textContent' --ref <ref>
openclaw browser upload /tmp/openclaw/uploads/file.pdf --ref <ref>
openclaw browser waitfordownload
openclaw browser download <ref> report.pdf
openclaw browser dialog --accept
```

### State and Storage

```bash
openclaw browser resize 1280 720
openclaw browser set viewport 1280 720
openclaw browser set offline on
openclaw browser set media dark
openclaw browser set timezone Europe/London
openclaw browser set locale en-GB
openclaw browser set geo 51.5074 -0.1278 --accuracy 25
openclaw browser set device "iPhone 14"
openclaw browser set headers '{"x-test":"1"}'
openclaw browser set credentials myuser mypass
openclaw browser cookies
openclaw browser cookies set session abc123 --url https://example.com
openclaw browser cookies clear
openclaw browser storage local get
openclaw browser storage local set token abc123
openclaw browser storage session clear
```

### Debugging

```bash
openclaw browser console --level error
openclaw browser pdf
openclaw browser responsebody "**/api"
openclaw browser highlight <ref>
openclaw browser errors --clear
openclaw browser requests --filter api
openclaw browser trace start
openclaw browser trace stop --out trace.zip
```

### Notes/Gotchas

- If `openclaw browser` is unknown, check `plugins.allow` in `openclaw.json`.
- `--full-page` cannot be combined with `--ref` or `--element`.
- For remote browser control, run a node host on the machine with Chrome.
- `existing-session` profile: no `slowly=true`, no `delayMs`, no `networkidle`.
- `attachOnly`/remote CDP: `stop` closes control session even if OpenClaw didn't launch the browser.

---

## Channels

**Synopsis:** `openclaw channels <subcommand> [options]`

**Description:** Manage chat channel accounts and their runtime status on the Gateway.

### Commands

```bash
openclaw channels list
openclaw channels status
openclaw channels status --probe
openclaw channels status --probe --timeout 5000 --json
openclaw channels capabilities
openclaw channels capabilities --channel discord --target channel:123
openclaw channels resolve --channel slack "#general" "@jane"
openclaw channels logs --channel all
openclaw channels logs --channel telegram --lines 50 --json
```

### Add / Remove Accounts

```bash
openclaw channels add --channel telegram --token <bot-token>
openclaw channels add --channel nostr --private-key "$NOSTR_PRIVATE_KEY"
openclaw channels remove --channel telegram --delete
```

**Per-channel non-interactive add flags:**
- Bot-token channels: `--token`, `--bot-token`, `--app-token`, `--token-file`
- Signal/iMessage: `--signal-number`, `--cli-path`, `--http-url`, `--http-host`, `--http-port`, `--db-path`, `--service`, `--region`
- Google Chat: `--webhook-path`, `--webhook-url`, `--audience-type`, `--audience`
- Matrix: `--homeserver`, `--user-id`, `--access-token`, `--password`, `--device-name`, `--initial-sync-limit`
- Nostr: `--private-key`, `--relay-urls`
- Tlon: `--ship`, `--url`, `--code`, `--group-channels`, `--dm-allowlist`, `--auto-discover-channels`
- `--use-env`: default-account env-backed auth

### Login / Logout (Interactive)

```bash
openclaw channels login --channel whatsapp
openclaw channels logout --channel whatsapp
```

### Resolve Names to IDs

```bash
openclaw channels resolve --channel slack "#general" "@jane"
openclaw channels resolve --channel discord "My Server/#support" "@someone"
openclaw channels resolve --channel matrix "Project Room"
# Options: --kind user|group|auto
```

### Notes/Gotchas

- `channels status --probe` is the live path; without it falls back to config-only.
- Run `openclaw doctor --fix` if config is in mixed state.

---

## Clawbot (legacy alias)

```bash
openclaw clawbot qr  # same as: openclaw qr
```

Only supported alias. Kept for backwards compatibility. Use `openclaw qr` directly.

---

## Completion

**Synopsis:** `openclaw completion [options]`

**Description:** Generate shell completion scripts.

### Options

| Flag | Description |
|---|---|
| `-s, --shell <shell>` | Target shell: `zsh\|bash\|powershell\|fish` (default: `zsh`) |
| `-i, --install` | Install completion into shell profile |
| `--write-state` | Write script to `$OPENCLAW_STATE_DIR/completions` |
| `-y, --yes` | Skip confirmation prompts |

### Examples

```bash
openclaw completion
openclaw completion --shell zsh
openclaw completion --install
openclaw completion --shell fish --install
openclaw completion --write-state
openclaw completion --shell bash --write-state
```

---

## Config

**Synopsis:** `openclaw config [subcommand] [path] [value] [options]`

**Description:** Non-interactive config edits for `openclaw.json`. No subcommand = opens configure wizard.

### Subcommands

```bash
openclaw config file              # Print active config file path
openclaw config schema            # Print JSON schema to stdout
openclaw config schema > openclaw.schema.json
openclaw config get <path>        # Get value at path
openclaw config get browser.executablePath
openclaw config get agents.list[0].id
openclaw config set <path> <value>
openclaw config unset <path>
openclaw config validate
openclaw config validate --json
```

### `config get` Options
- `--json`: print raw value as JSON

### `config set` — Four Assignment Modes

**1. Value mode (default):**
```bash
openclaw config set browser.executablePath "/usr/bin/google-chrome"
openclaw config set agents.defaults.heartbeat.every "2h"
```

**2. SecretRef builder mode:**
```bash
openclaw config set channels.discord.token \
  --ref-provider default \
  --ref-source env \
  --ref-id DISCORD_BOT_TOKEN
```

**3. Provider builder mode** (`secrets.providers.<alias>` only):
```bash
openclaw config set secrets.providers.vault \
  --provider-source exec \
  --provider-command /usr/local/bin/my-vault \
  --provider-arg read \
  --provider-arg openai/api-key \
  --provider-timeout-ms 5000
```

**4. Batch mode:**
```bash
openclaw config set --batch-json '[
  { "path": "secrets.providers.default", "provider": { "source": "env" } },
  { "path": "channels.discord.token", "ref": { "source": "env", "provider": "default", "id": "DISCORD_BOT_TOKEN" } }
]'
openclaw config set --batch-file ./config-set.batch.json --dry-run
```

### `config set` Additional Options

| Flag | Description |
|---|---|
| `--strict-json` | Require JSON5 parsing |
| `--merge` | Merge into maps/lists instead of replacing |
| `--replace` | Force complete replacement of protected maps |
| `--dry-run` | Validate without writing |
| `--allow-exec` | Allow exec SecretRef checks in dry-run |

### Provider Builder Flags

Common:
- `--provider-source <env|file|exec>`
- `--provider-timeout-ms <ms>`

Env provider: `--provider-allowlist <ENV_VAR>` (repeatable)

File provider: `--provider-path <path>`, `--provider-mode <singleValue|json>`, `--provider-max-bytes`, `--provider-allow-insecure-path`

Exec provider: `--provider-command <path>`, `--provider-arg <arg>` (repeatable), `--provider-no-output-timeout-ms`, `--provider-max-output-bytes`, `--provider-json-only`, `--provider-env <KEY=VALUE>` (repeatable), `--provider-pass-env`, `--provider-trusted-dir`, `--provider-allow-insecure-path`, `--provider-allow-symlink-command`

### Notes/Gotchas

- Values parsed as JSON5 when possible; otherwise treated as strings.
- Protected maps (e.g. `agents.defaults.models`, `plugins.entries`) refuse replacements that remove existing entries unless `--replace`.
- Config path must be a regular file — symlinks not supported for writes.
- If write is rejected, inspect `openclaw.json.rejected.*` for the rejected payload.

---

## Configure

**Synopsis:** `openclaw configure [options]`

**Description:** Interactive prompt-driven setup wizard. Same as `openclaw config` with no subcommand.

### Options

- `--section <section>` (repeatable): filter to specific section

Available sections: `workspace`, `model`, `web`, `gateway`, `daemon`, `channels`, `plugins`, `skills`, `health`

### Examples

```bash
openclaw configure
openclaw configure --section web
openclaw configure --section model --section channels
openclaw configure --section gateway --section daemon
```

### Notes/Gotchas

- **Model section**: multi-select for `agents.defaults.models` allowlist; merges, not replaces.
- Provider setup choices merge selected models; use `openclaw models set <model>` to change default.
- Re-running preserves existing `agents.defaults.model.primary`.

---

## Cron

**Synopsis:** `openclaw cron <subcommand> [options]`

**Description:** Manage cron jobs for the Gateway scheduler.

### Admin Commands

```bash
openclaw cron status
openclaw cron list
openclaw cron list --json
openclaw cron show <job-id>
openclaw cron run <job-id>
openclaw cron run <job-id> --due      # only if due
openclaw cron runs --id <job-id> --limit 50
openclaw cron enable <job-id>
openclaw cron disable <job-id>
openclaw cron rm <job-id>
```

### Add a Job

```bash
# Recurring
openclaw cron add \
  --name "Morning brief" \
  --cron "0 7 * * *" \
  --session isolated \
  --message "Summarize overnight updates." \
  --announce --channel telegram --to "123456789"

# One-shot (runs once at specified time)
openclaw cron add \
  --name "Reminder" \
  --at "2026-04-25T09:00:00" \
  --tz "America/New_York" \
  --message "Check email" \
  --announce

# Lightweight isolated
openclaw cron add \
  --name "Brief" \
  --cron "0 7 * * *" \
  --session isolated \
  --message "Summarize overnight updates." \
  --light-context \
  --no-deliver
```

### Edit a Job

```bash
openclaw cron edit <job-id> --announce --channel telegram --to "123456789"
openclaw cron edit <job-id> --no-deliver
openclaw cron edit <job-id> --light-context
openclaw cron edit <job-id> --announce --channel slack --to "channel:C1234567890"
openclaw cron edit <job-id> --agent ops
openclaw cron edit <job-id> --clear-agent
openclaw cron edit <job-id> --session current
openclaw cron edit <job-id> --session "session:daily-brief"
openclaw cron edit <job-id> --best-effort-deliver
openclaw cron edit <job-id> --no-best-effort-deliver
openclaw cron add --model openai/gpt-5.4 ...
```

### Key Options

| Flag | Description |
|---|---|
| `--name <name>` | Job name |
| `--cron <expr>` | Cron expression (recurring) |
| `--at <datetime>` | ISO datetime for one-shot job (UTC unless `--tz`) |
| `--tz <timezone>` | Timezone for `--at` |
| `--session <key>` | `main\|isolated\|current\|session:<id>` |
| `--message <text>` | Message to inject |
| `--announce` | Deliver output to channel |
| `--no-deliver` | Keep output internal |
| `--light-context` | Lightweight bootstrap context |
| `--agent <id>` | Target agent |
| `--model <model>` | Model override |
| `--best-effort-deliver` | Best-effort delivery (don't fail on delivery error) |
| `--keep-after-run` | Keep one-shot job after success |

### Notes/Gotchas

- `--session` values: `main`, `isolated`, `current`, `session:<id>`.
- `--at` without `--tz` is treated as UTC.
- One-shot jobs delete after success by default (use `--keep-after-run` to keep).
- Isolated `cron add` defaults to `--announce` delivery. Use `--no-deliver` to keep output internal. `--deliver` is deprecated alias.
- Retry backoff: 30s → 1m → 5m → 15m → 60m (resets after next success).
- `cron run` returns immediately with `{ ok: true, enqueued: true, runId }`. Use `--due` to keep older "only run if due" behavior.
- `cron runs` entries include delivery diagnostics: intended target, resolved target, message-tool sends, fallback use, delivered state.
- If isolated run returns only `NO_REPLY`/`no_reply`, delivery is suppressed (direct outbound + fallback queued summary).
- **Stale ack guard:** If first result is just interim status ("on it", etc.) and no descendant subagent handles the answer, cron re-prompts once for real result.
- **Model switch retry:** If an isolated run throws `LiveSessionModelSwitchError`, cron persists the switched provider/model (and auth profile) then retries. Bounded: initial + 2 switch retries, then abort.
- **Failure notifications:** `delivery.failureDestination` → global `cron.failureDestination` → primary announce target fallback.
- Retention: `cron.sessionRetention` (default `24h`), `cron.runLog.maxBytes`, `cron.runLog.keepLines`.
- **Doctor migration:** `openclaw doctor --fix` normalizes legacy cron fields (`jobId`, `schedule.cron`, top-level delivery, legacy `threadId`, `notify: true` webhook fallback).

---

## Daemon (legacy alias)

**Synopsis:** `openclaw daemon <subcommand>`

**Description:** Legacy alias for gateway service management. Maps to `openclaw gateway <service-cmd>`.

```bash
openclaw daemon status
openclaw daemon install
openclaw daemon start
openclaw daemon stop
openclaw daemon restart
openclaw daemon uninstall
```

**Prefer:** `openclaw gateway` for current usage.

**Common options:** `--url`, `--token`, `--password`, `--timeout`, `--no-probe`, `--require-rpc`, `--deep`, `--json`, `--port`, `--runtime <node|bun>`, `--force`

---

## Dashboard

**Synopsis:** `openclaw dashboard [options]`

**Description:** Open the Control UI using current auth.

```bash
openclaw dashboard
openclaw dashboard --no-open
```

**Notes:**
- For SecretRef-managed tokens, prints a non-tokenized URL (avoids exposing secrets in terminal or browser-launch args).

---

## Devices

**Synopsis:** `openclaw devices <subcommand> [options]`

**Description:** Manage device pairing requests and device-scoped tokens.

### Commands

```bash
# List all devices
openclaw devices list
openclaw devices list --json

# Remove a device
openclaw devices remove <deviceId>
openclaw devices remove <deviceId> --json

# Clear pending requests
openclaw devices clear --yes
openclaw devices clear --yes --pending
openclaw devices clear --yes --pending --json

# Approve / reject pairing
openclaw devices approve               # preview (requires rerun with explicit ID)
openclaw devices approve <requestId>
openclaw devices approve --latest
openclaw devices reject <requestId>

# Token rotation
openclaw devices rotate --device <deviceId> --role operator --scope operator.read --scope operator.write

# Token revocation
openclaw devices revoke --device <deviceId> --role node
```

### Common Options

- `--url <url>`, `--token <token>`, `--password <password>`, `--timeout <ms>`, `--json`

### Token Drift Recovery

```bash
openclaw config get gateway.auth.token
openclaw devices list
openclaw devices rotate --device <deviceId> --role operator
# If not enough:
openclaw devices remove <deviceId>
openclaw devices list
openclaw devices approve <requestId>
```

### Notes/Gotchas

- `devices approve` requires explicit request ID before minting tokens.
- Non-admin callers can remove/revoke only their own device.
- `devices clear` gated by `--yes`.
- Token rotation returns new token (treat as secret).
- Commands require `operator.pairing` (or `operator.admin`) scope.

---

## Directory

**Synopsis:** `openclaw directory [self|peers|groups] [options]`

**Description:** Directory lookups for channels that support contacts/groups.

### Common Flags

- `--channel <name>`: channel id/alias (required with multiple channels)
- `--account <id>`: account id
- `--json`

### Commands

```bash
openclaw directory self --channel zalouser
openclaw directory peers list --channel zalouser
openclaw directory peers list --channel zalouser --query "name" --limit 50
openclaw directory groups list --channel zalouser
openclaw directory groups list --channel zalouser --query "work"
openclaw directory groups members --channel zalouser --group-id <id>
```

### ID Formats by Channel

| Channel | Format |
|---|---|
| WhatsApp | `+15551234567` (DM), `1234567890-1234567890@g.us` (group) |
| Telegram | `@username` or numeric chat id |
| Slack | `user:U…`, `channel:C…` |
| Discord | `user:<id>`, `channel:<id>` |
| Matrix | `user:@user:server`, `room:!roomId:server`, `#alias:server` |
| Microsoft Teams | `user:<id>`, `conversation:<id>` |

---

## DNS

**Synopsis:** `openclaw dns setup [options]`

**Description:** DNS helpers for wide-area discovery (Tailscale + CoreDNS). Currently focused on macOS + Homebrew.

### Options

| Flag | Description |
|---|---|
| `--domain <domain>` | Wide-area discovery domain (e.g. `openclaw.internal`) |
| `--apply` | Install/update CoreDNS config and restart service (sudo; macOS only) |

### Examples

```bash
openclaw dns setup
openclaw dns setup --domain openclaw.internal
openclaw dns setup --apply
```

### Notes/Gotchas

- Without `--apply`, planning helper only (prints recommended setup).
- `--apply` bootstraps zone file, ensures CoreDNS import stanza, restarts `coredns` brew service.

---

## Docs

**Synopsis:** `openclaw docs [query...]`

**Description:** Search the live docs index.

```bash
openclaw docs
openclaw docs browser existing-session
openclaw docs sandbox allowHostControl
openclaw docs gateway token secretref
```

- No query opens live docs search entrypoint.
- Multi-word queries passed as one search request.

---

## Doctor

**Synopsis:** `openclaw doctor [options]`

**Description:** Health checks + quick fixes for gateway and channels.

### Options

| Flag | Description |
|---|---|
| `--no-workspace-suggestions` | Disable workspace memory/search suggestions |
| `--yes` | Accept defaults without prompting |
| `--repair` / `--fix` | Apply recommended repairs without prompting |
| `--force` | Apply aggressive repairs, overwrite custom service config |
| `--non-interactive` | Run without prompts; safe migrations only |
| `--generate-gateway-token` | Generate and configure a gateway token |
| `--deep` | Scan system services for extra gateway installs |

### Examples

```bash
openclaw doctor
openclaw doctor --repair
openclaw doctor --deep
openclaw doctor --repair --non-interactive
openclaw doctor --generate-gateway-token
```

### What Doctor Does

- Health checks for gateway and channels.
- `--fix` writes backup to `~/.openclaw/openclaw.json.bak`, drops unknown config keys.
- Detects orphan transcript files; can archive as `.deleted.<timestamp>`.
- Scans and normalizes legacy cron job shapes.
- Repairs missing bundled plugin runtime dependencies.
- Auto-migrates legacy flat Talk config.
- Includes memory-search readiness check.
- Warns if sandbox mode enabled but Docker unavailable.

### macOS: Stale Env Overrides

```bash
# Check for stale overrides (can cause persistent "unauthorized" errors)
launchctl getenv OPENCLAW_GATEWAY_TOKEN
launchctl getenv OPENCLAW_GATEWAY_PASSWORD
# Remove them:
launchctl unsetenv OPENCLAW_GATEWAY_TOKEN
launchctl unsetenv OPENCLAW_GATEWAY_PASSWORD
```

---

## Flows (redirect → tasks)

Flow commands are subcommands of `openclaw tasks`, not standalone:

```bash
openclaw tasks flow list [--json]
openclaw tasks flow show <lookup>
openclaw tasks flow cancel <lookup>
```

See [Tasks](#tasks).

---

## Gateway

**Synopsis:** `openclaw gateway [subcommand] [options]`

**Description:** OpenClaw's WebSocket server (channels, nodes, sessions, hooks).

### Run the Gateway

```bash
openclaw gateway          # requires gateway.mode=local in config
openclaw gateway run      # foreground alias
```

### Run Options

| Flag | Description |
|---|---|
| `--port <port>` | WebSocket port (default: `18789`) |
| `--bind <loopback\|lan\|tailnet\|auto\|custom>` | Listener bind mode |
| `--auth <token\|password>` | Auth mode override |
| `--token <token>` | Token override |
| `--password <password>` | Password (⚠️ visible in process listings) |
| `--password-file <path>` | Read password from file |
| `--tailscale <off\|serve\|funnel>` | Expose via Tailscale |
| `--tailscale-reset-on-exit` | Reset Tailscale config on shutdown |
| `--allow-unconfigured` | Allow start without `gateway.mode=local` |
| `--dev` | Create dev config + workspace if missing |
| `--reset` | Reset dev config + credentials + sessions + workspace (requires `--dev`) |
| `--force` | Kill existing listener on port before starting |
| `--verbose` | Verbose logs |
| `--cli-backend-logs` | Only show CLI backend logs |
| `--ws-log <auto\|full\|compact>` | WebSocket log style |
| `--compact` | Alias for `--ws-log compact` |
| `--raw-stream` | Log raw model stream events to jsonl |
| `--raw-stream-path <path>` | Raw stream jsonl path |

**Startup profiling:** `OPENCLAW_GATEWAY_STARTUP_TRACE=1`

### Query Commands (Gateway RPC)

Shared options: `--url`, `--token`, `--password`, `--timeout <ms>`, `--expect-final`

> When you set `--url`, the CLI does NOT fall back to config/env credentials. Pass `--token`/`--password` explicitly.

#### `gateway health`
```bash
openclaw gateway health --url ws://127.0.0.1:18789
```
- `/healthz` = liveness; `/readyz` = strict readiness (waits for channels/hooks)

#### `gateway usage-cost`
```bash
openclaw gateway usage-cost
openclaw gateway usage-cost --days 7    # default: 30
openclaw gateway usage-cost --json
```

#### `gateway stability`
```bash
openclaw gateway stability
openclaw gateway stability --type payload.large
openclaw gateway stability --bundle latest
openclaw gateway stability --bundle latest --export
openclaw gateway stability --json
```

Options: `--limit <n>` (max 1000, default 25), `--type <type>`, `--since-seq <seq>`, `--bundle [path]`, `--export`, `--output <path>`

#### `gateway diagnostics export`
```bash
openclaw gateway diagnostics export
openclaw gateway diagnostics export --output openclaw-diagnostics.zip
openclaw gateway diagnostics export --json
```

Options: `--output <path>`, `--log-lines <count>` (default 5000), `--log-bytes <bytes>` (default 1000000), `--url`, `--token`, `--password`, `--timeout <ms>`, `--no-stability-bundle`, `--json`

#### `gateway status`
```bash
openclaw gateway status
openclaw gateway status --json
openclaw gateway status --require-rpc
```

Options: `--url`, `--token`, `--password`, `--timeout <ms>`, `--no-probe`, `--deep`, `--require-rpc`

> `--require-rpc`: upgrade probe to read probe; exit non-zero when it fails. Use in scripts.

#### `gateway probe`
```bash
openclaw gateway probe
openclaw gateway probe --json
openclaw gateway probe --ssh user@gateway-host
openclaw gateway probe --ssh user@gateway-host:22 --ssh-identity ~/.ssh/id_rsa
openclaw gateway probe --ssh-auto
```

**Probe interpretation:**
- `Reachable: yes` — at least one target accepted WebSocket connect
- `Capability: read-only|write-capable|admin-capable|pairing-pending|connect-only`
- `Read probe: ok` — read-scope RPC calls succeeded

**Warning codes:** `ssh_tunnel_failed`, `multiple_gateways`, `auth_secretref_unresolved`, `probe_scope_limited`

#### `gateway call <method>`
```bash
openclaw gateway call status
openclaw gateway call logs.tail --params '{"sinceMs": 60000}'
```

Options: `--params <json>`, `--url`, `--token`, `--password`, `--timeout <ms>`, `--expect-final`, `--json`

### Service Management

```bash
openclaw gateway install
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway uninstall
```

Options for `install`: `--port`, `--runtime <node|bun>`, `--token`, `--force`, `--json`

### Discovery (Bonjour / mDNS)

```bash
openclaw gateway discover
openclaw gateway discover --timeout 4000
openclaw gateway discover --json | jq '.beacons[].wsUrl'
```

Options: `--timeout <ms>` (default 2000), `--json`

**Wide-Area Bonjour TXT records:** `role`, `transport`, `gatewayPort`, `sshPort`, `tailnetDns`, `gatewayTls`, `gatewayTlsSha256`, `cliPath`

### Notes/Gotchas

- Gateway refuses to start unless `gateway.mode=local` is set. Use `--allow-unconfigured` for ad-hoc.
- Binding beyond loopback without auth is blocked.
- `SIGUSR1` triggers in-process restart (when `commands.restart` enabled).
- For password auth, prefer `OPENCLAW_GATEWAY_PASSWORD`, `--password-file`, or SecretRef.
- If both token and password are configured and `gateway.auth.mode` unset, install is blocked.

---

## Health

**Synopsis:** `openclaw health [options]`

**Description:** Fetch health from the running Gateway.

### Options

| Flag | Description |
|---|---|
| `--json` | Machine-readable output |
| `--timeout <ms>` | Connection timeout (default `10000`) |
| `--verbose` | Verbose logging (forces live probe) |
| `--debug` | Alias for `--verbose` |

### Examples

```bash
openclaw health
openclaw health --json
openclaw health --timeout 2500
openclaw health --verbose
openclaw health --debug
```

### Notes/Gotchas

- Default: asks Gateway for cached health snapshot.
- `--verbose` forces live probe; expands output across all configured accounts and agents.
- Output includes per-agent session stores when multiple agents configured.

---

## Hooks

**Synopsis:** `openclaw hooks [subcommand] [options]`

**Description:** Manage agent hooks (event-driven automations for `/new`, `/reset`, gateway startup). No subcommand = `hooks list`.

### Commands

```bash
openclaw hooks list
openclaw hooks list --eligible
openclaw hooks list --verbose
openclaw hooks list --json
openclaw hooks info session-memory
openclaw hooks info session-memory --json
openclaw hooks check
openclaw hooks check --json
openclaw hooks enable session-memory
openclaw hooks enable boot-md
openclaw hooks disable command-logger
```

### Install / Update Hook Packs

```bash
openclaw plugins install <package>          # ClawHub first, then npm
openclaw plugins install <package> --pin    # pin version
openclaw plugins install <path>             # local path
openclaw plugins install -l ./my-hook-pack  # link without copying
openclaw plugins update <id>
openclaw plugins update --all
openclaw plugins update --dry-run
```

> `openclaw hooks install`/`hooks update` still work but print deprecation warnings and forward to `plugins install`/`update`.

### Bundled Hooks

| Hook | Events | Description |
|---|---|---|
| `session-memory` | `command:new`, `command:reset` | Saves session context to memory on `/new`/`/reset` |
| `bootstrap-extra-files` | `agent:bootstrap` | Injects additional bootstrap files |
| `command-logger` | all commands | Logs all command events to `~/.openclaw/logs/commands.log` |
| `boot-md` | `gateway:startup` | Runs `BOOT.md` when gateway starts |

```bash
openclaw hooks enable session-memory
openclaw hooks enable boot-md
openclaw hooks enable bootstrap-extra-files
openclaw hooks enable command-logger

# View command-logger output:
tail -n 20 ~/.openclaw/logs/commands.log
cat ~/.openclaw/logs/commands.log | jq .
grep '"action":"new"' ~/.openclaw/logs/commands.log | jq .
```

### Notes/Gotchas

- Plugin-managed hooks cannot be enabled/disabled here; enable/disable the owning plugin.
- Workspace hooks are disabled by default until enabled.
- Npm specs are registry-only (exact version or dist-tag only). No semver ranges.
- After enabling/disabling: **restart the gateway**.

---

## Infer / capability

**Synopsis:** `openclaw infer <subcommand> [options]`  
**Alias:** `openclaw capability`

**Description:** Headless surface for provider-backed inference — model, image, audio, TTS, video, web, embedding.

### Command Tree

```
openclaw infer
  list
  inspect

  model
    run
    list / inspect / providers
    auth login / logout / status

  image
    generate / edit / describe / describe-many / providers

  audio
    transcribe / providers

  tts
    convert / voices / providers / status / enable / disable / set-provider

  video
    generate / describe / providers

  web
    search / fetch / providers

  embedding
    create / providers
```

### Common Task → Command

| Task | Command |
|---|---|
| Text/model prompt | `openclaw infer model run --prompt "..." --json` |
| Generate image | `openclaw infer image generate --prompt "..." --json` |
| Describe image | `openclaw infer image describe --file ./image.png --json` |
| Transcribe audio | `openclaw infer audio transcribe --file ./memo.m4a --json` |
| Synthesize speech | `openclaw infer tts convert --text "..." --output ./speech.mp3 --json` |
| Generate video | `openclaw infer video generate --prompt "..." --json` |
| Describe video | `openclaw infer video describe --file ./clip.mp4 --json` |
| Web search | `openclaw infer web search --query "..." --json` |
| Fetch page | `openclaw infer web fetch --url https://example.com --json` |
| Create embeddings | `openclaw infer embedding create --text "..." --json` |

### Model Examples

```bash
openclaw infer model run --prompt "Reply with exactly: smoke-ok" --json
openclaw infer model run --prompt "Summarize this changelog entry" --provider openai --json
openclaw infer model providers --json
openclaw infer model inspect --name gpt-5.5 --json
```

### Image Examples

```bash
openclaw infer image generate --prompt "friendly lobster illustration" --json
openclaw infer image describe --file ./photo.jpg --json
openclaw infer image describe --file ./ui-screenshot.png --model openai/gpt-4.1-mini --json
openclaw infer image describe --file ./photo.jpg --model ollama/qwen2.5vl:7b --json
openclaw infer image providers --json
# Smoke test:
openclaw infer image generate \
  --model google/gemini-3.1-flash-image-preview \
  --prompt "Minimal flat test image: one blue square on white background, no text." \
  --output ./smoke.png --json
```

### Audio Examples

```bash
openclaw infer audio transcribe --file ./memo.m4a --json
openclaw infer audio transcribe --file ./team-sync.m4a --language en --prompt "Focus on names and action items" --json
openclaw infer audio transcribe --file ./memo.m4a --model openai/whisper-1 --json
```

### TTS Examples

```bash
openclaw infer tts convert --text "hello from openclaw" --output ./hello.mp3 --json
openclaw infer tts providers --json
openclaw infer tts status --json
openclaw infer tts voices --json
```

### Video Examples

```bash
openclaw infer video generate --prompt "cinematic sunset over the ocean" --json
openclaw infer video describe --file ./clip.mp4 --json
openclaw infer video describe --file ./clip.mp4 --model openai/gpt-4.1-mini --json
```

### Web Examples

```bash
openclaw infer web search --query "OpenClaw docs" --json
openclaw infer web fetch --url https://docs.openclaw.ai/cli/infer --json
openclaw infer web providers --json
```

### Embedding Examples

```bash
openclaw infer embedding create --text "friendly lobster" --json
openclaw infer embedding create --text "customer support ticket" --model openai/text-embedding-3-large --json
openclaw infer embedding providers --json
```

### JSON Output Envelope

```json
{
  "ok": true,
  "capability": "image.generate",
  "transport": "local",
  "provider": "openai",
  "model": "gpt-image-2",
  "attempts": [],
  "outputs": []
}
```

Stable fields: `ok`, `capability`, `transport`, `provider`, `model`, `attempts`, `outputs`, `error`

### Notes/Gotchas

- For `image describe`, `audio transcribe`, `video describe`: `--model` MUST be `<provider/model>`.
- Stateless execution defaults to local (no Gateway required for most commands).
- `tts status` defaults to gateway (reflects gateway-managed TTS state).
- Common mistake: `openclaw infer media image generate` → WRONG. Use `openclaw infer image generate`.
- For local Ollama vision: `OLLAMA_API_KEY=ollama-local` (any placeholder value).

---

## Logs

**Synopsis:** `openclaw logs [options]`

**Description:** Tail Gateway file logs over RPC (works in remote mode).

### Options

| Flag | Description |
|---|---|
| `--limit <n>` | Max log lines (default `200`) |
| `--max-bytes <n>` | Max bytes from log file (default `250000`) |
| `--follow` | Follow the log stream |
| `--interval <ms>` | Polling interval while following (default `1000`) |
| `--json` | Line-delimited JSON events |
| `--plain` | Plain text, no styling |
| `--no-color` | Disable ANSI colors |
| `--local-time` | Timestamps in local timezone |
| `--url <url>` | Gateway WebSocket URL |
| `--token <token>` | Gateway token |
| `--timeout <ms>` | Timeout (default `30000`) |
| `--expect-final` | Wait for final response |

### Examples

```bash
openclaw logs
openclaw logs --follow
openclaw logs --follow --interval 2000
openclaw logs --limit 500 --max-bytes 500000
openclaw logs --json
openclaw logs --plain
openclaw logs --no-color
openclaw logs --limit 500
openclaw logs --local-time
openclaw logs --follow --local-time
openclaw logs --url ws://127.0.0.1:18789 --token "$OPENCLAW_GATEWAY_TOKEN"
```

### Notes/Gotchas

- When passing `--url`, also pass explicit `--token` (no auto-apply of config credentials).
- If local loopback Gateway asks for pairing, `logs` falls back to configured local log file. Explicit `--url` does NOT use this fallback.

---

## MCP

**Synopsis:** `openclaw mcp <subcommand>`

**Description:** Two jobs: (1) run OpenClaw as MCP server with `mcp serve`; (2) manage OpenClaw-owned outbound MCP server definitions.

### `mcp serve` — OpenClaw as MCP Server

```bash
openclaw mcp serve
openclaw mcp serve --url wss://gateway-host:18789 --token-file ~/.openclaw/gateway.token
openclaw mcp serve --url wss://gateway-host:18789 --password-file ~/.openclaw/gateway.password
openclaw mcp serve --verbose
openclaw mcp serve --claude-channel-mode off
```

**Options:**

| Flag | Description |
|---|---|
| `--url <url>` | Gateway WebSocket URL |
| `--token <token>` | Gateway token |
| `--token-file <path>` | Read token from file |
| `--password <password>` | Gateway password |
| `--password-file <path>` | Read password from file |
| `--claude-channel-mode <auto\|on\|off>` | Claude notification mode (default `auto`) |
| `-v, --verbose` | Verbose logs on stderr |

### Bridge Tools Exposed

| Tool | Description |
|---|---|
| `conversations_list` | List recent session-backed conversations |
| `conversation_get` | Get one conversation by `session_key` |
| `messages_read` | Read recent transcript messages |
| `attachments_fetch` | Extract non-text message content blocks |
| `events_poll` | Read queued live events since cursor |
| `events_wait` | Long-polls until next matching event or timeout |
| `messages_send` | Send text through the same route |
| `permissions_list_open` | List pending exec/plugin approval requests |
| `permissions_respond` | Resolve approval: `allow-once\|allow-always\|deny` |

### Claude Channel Notifications

When `--claude-channel-mode on|auto`:
- Inbound `user` transcript messages → `notifications/claude/channel`
- Claude permission requests → `notifications/claude/channel/permission`

### MCP Client Config

```json
{
  "mcpServers": {
    "openclaw": {
      "command": "openclaw",
      "args": [
        "mcp", "serve",
        "--url", "wss://gateway-host:18789",
        "--token-file", "/path/to/gateway.token"
      ]
    }
  }
}
```

### Saved MCP Server Definitions (Registry)

```bash
openclaw mcp list
openclaw mcp show context7 --json
openclaw mcp set context7 '{"command":"uvx","args":["context7-mcp"]}'
openclaw mcp set docs '{"url":"https://mcp.example.com"}'
openclaw mcp unset context7
```

**Transport shapes:**

```json
// Stdio
{ "command": "uvx", "args": ["context7-mcp"], "env": {}, "cwd": "/path" }

// SSE/HTTP
{ "url": "https://mcp.example.com", "headers": { "Authorization": "Bearer <token>" } }

// Streamable HTTP
{ "url": "https://mcp.example.com/stream", "transport": "streamable-http", "connectionTimeoutMs": 10000 }
```

### Notes/Gotchas

- Live queue starts when bridge connects; older history read with `messages_read`.
- `events_poll`/`events_wait` do NOT replay older Gateway history.
- `permissions_list_open` only shows approvals while bridge was connected.
- Blocked stdio env keys: `NODE_OPTIONS`, `PYTHONSTARTUP`, `PYTHONPATH`, `PERL5OPT`, `RUBYOPT`, `SHELLOPTS`, `PS4`, etc.
- `mcp list/show/set/unset` do NOT connect to the MCP server — config only.

---

## Memory

**Synopsis:** `openclaw memory <subcommand> [options]`

**Description:** Manage semantic memory indexing and search. Provided by active memory plugin (default: `memory-core`).

### Examples

```bash
openclaw memory status
openclaw memory status --deep
openclaw memory status --deep --index
openclaw memory status --fix
openclaw memory status --json
openclaw memory status --agent main
openclaw memory index --force
openclaw memory index --agent main --verbose
openclaw memory search "meeting notes"
openclaw memory search --query "deployment" --max-results 20
openclaw memory promote --limit 10 --min-score 0.75
openclaw memory promote --apply
openclaw memory promote --json --min-recall-count 0 --min-unique-queries 0
openclaw memory promote-explain "router vlan"
openclaw memory promote-explain "router vlan" --json
openclaw memory rem-harness
openclaw memory rem-harness --json
```

### Options

**`memory status`:**
- `--deep`: probe vector + embedding availability
- `--index`: run reindex if store is dirty (implies `--deep`)
- `--fix`: repair stale recall locks and normalize promotion metadata
- `--agent <id>`: scope to one agent
- `--verbose`: detailed logs
- `--json`

**`memory index`:**
- `--force`: force full reindex
- `--agent <id>`, `--verbose`

**`memory search`:**
- `[query]` or `--query <text>` (`--query` wins if both)
- `--agent <id>`, `--max-results <n>`, `--min-score <n>`, `--json`

**`memory promote`:**
- `--apply`: write to `MEMORY.md` (default: preview)
- `--limit <n>`, `--include-promoted`, `--agent <id>`
- `--min-score <n>`, `--min-recall-count <n>`, `--min-unique-queries <n>`
- `--json`

**`memory promote-explain <selector>`:**
- `--agent <id>`, `--include-promoted`, `--json`

**`memory rem-harness`:**
- `--agent <id>`, `--include-promoted`, `--json`

### Dreaming (Background Memory Consolidation)

Three phases: **light** (sort/stage) → **REM** (reflect/surface themes) → **deep** (promote to `MEMORY.md`)

Enable:
```json
{
  "plugins": {
    "entries": {
      "memory-core": {
        "config": { "dreaming": { "enabled": true } }
      }
    }
  }
}
```

Toggle in chat: `/dreaming on|off` or `/dreaming status`

**Defaults:** sweep at `0 3 * * *`; deep thresholds: `minScore=0.8`, `minRecallCount=3`, `minUniqueQueries=3`, `recencyHalfLifeDays=14`, `maxAgeDays=30`

Human-readable output → `DREAMS.md`; durable memory → `MEMORY.md`

### Notes/Gotchas

- `memory status` shows `Dreaming status: blocked` → managed cron enabled but heartbeat not firing.
- Only the deep phase writes durable memory to `MEMORY.md`.
- `memory rem-harness --path <file-or-dir> --grounded` previews without writing anything.

---

## Message

**Synopsis:** `openclaw message <subcommand> [flags]`

**Description:** Single outbound command for sending messages and channel actions across all configured channels.

**Supported channels:** Discord, Google Chat, iMessage, Matrix, Mattermost (plugin), Microsoft Teams, Signal, Slack, Telegram, WhatsApp

### Channel Selection & Target Formats

- `--channel` required if more than one channel configured.

| Channel | `--target` format |
|---|---|
| WhatsApp | E.164 or group JID |
| Telegram | chat id or `@username` |
| Discord | `channel:<id>`, `user:<id>`, or `<@id>` |
| Google Chat | `spaces/<spaceId>` or `users/<userId>` |
| Slack | `channel:<id>` or `user:<id>` |
| Mattermost | `channel:<id>`, `user:<id>`, or `@username` |
| Signal | `+E.164`, `group:<id>`, `signal:+E.164`, `username:<name>` |
| iMessage | handle, `chat_id:<id>`, `chat_guid:<guid>` |
| Matrix | `@user:server`, `!room:server`, `#alias:server` |
| Microsoft Teams | `19:...@thread.tacv2`, `conversation:<id>`, `user:<aad-object-id>` |

### Common Flags

- `--channel <name>`, `--account <id>`, `--target <dest>`, `--targets <name>` (repeatable; broadcast)
- `--json`, `--dry-run`, `--verbose`

### Core Actions

**`send`**
```bash
openclaw message send --channel discord --target channel:123 --message "hi" --reply-to 456
openclaw message send --channel telegram --target @mychat --media ./diagram.png --force-document
```
Optional: `--media`, `--presentation`, `--delivery`, `--pin`, `--reply-to`, `--thread-id`, `--gif-playback` (WhatsApp), `--force-document` (Telegram), `--silent` (Telegram/Discord)

**`poll`**
```bash
openclaw message poll --channel discord --target channel:123 \
  --poll-question "Snack?" --poll-option Pizza --poll-option Sushi \
  --poll-multi --poll-duration-hours 48

openclaw message poll --channel telegram --target @mychat \
  --poll-question "Lunch?" --poll-option Pizza --poll-option Sushi \
  --poll-duration-seconds 120 --silent
```

**`react`**
```bash
openclaw message react --channel slack --target C123 --message-id 456 --emoji "✅"
openclaw message react --channel signal --target signal:group:abc123 --message-id 1737630212345 \
  --emoji "✅" --target-author-uuid 123e4567-e89b-12d3-a456-426614174000
```
Required: `--message-id`, `--target`; Optional: `--emoji`, `--remove`, `--participant`, `--from-me`, `--target-author`, `--target-author-uuid`

**`reactions`** (Discord/Google Chat/Slack/Matrix): `--message-id`, `--target`, `--limit`

**`read`** (Discord/Slack/Matrix): `--target`, `--limit`, `--before`, `--after`; Discord: `--around`

**`edit`** (Discord/Slack/Matrix): `--message-id`, `--message`, `--target`

**`delete`** (Discord/Slack/Telegram/Matrix): `--message-id`, `--target`

**`pin`/`unpin`/`pins`** (Discord/Slack/Matrix): `--message-id`, `--target`

**`search`** (Discord): `--guild-id`, `--query`; Optional: `--channel-id`, `--channel-ids`, `--author-id`, `--author-ids`, `--limit`

### Threads (Discord)

```bash
openclaw message thread create --thread-name "Help" --target channel:123
openclaw message thread list --guild-id <guildId>
openclaw message thread reply --target <threadId> --message "Reply text"
```

### Emojis & Stickers (Discord)

```bash
openclaw message emoji list --guild-id <guildId>
openclaw message emoji upload --guild-id <guildId> --emoji-name "clawbot" --media ./emoji.png
openclaw message sticker send --target channel:123 --sticker-id <id>
openclaw message sticker upload --guild-id <guildId> --sticker-name "claw" --sticker-desc "clawbot" --sticker-tags "claw" --media ./sticker.png
```

### Roles / Channels / Members / Voice / Events / Moderation (Discord)

```bash
openclaw message role info --guild-id <guildId>
openclaw message role add --guild-id <guildId> --user-id <userId> --role-id <roleId>
openclaw message role remove --guild-id <guildId> --user-id <userId> --role-id <roleId>
openclaw message channel info --target <channelId>
openclaw message channel list --guild-id <guildId>
openclaw message member info --user-id <userId> --guild-id <guildId>
openclaw message voice status --guild-id <guildId> --user-id <userId>
openclaw message event list --guild-id <guildId>
openclaw message event create --guild-id <guildId> --event-name "Launch" --start-time "2026-05-01T14:00:00Z"
openclaw message timeout --guild-id <guildId> --user-id <userId> --duration-min 10
openclaw message kick --guild-id <guildId> --user-id <userId> --reason "Spam"
openclaw message ban --guild-id <guildId> --user-id <userId> --delete-days 1 --reason "Spam"
```

### Broadcast

```bash
openclaw message broadcast --channel all --targets "+15551234567" "+15559876543" --message "Hello"
openclaw message broadcast --channel discord --targets "channel:123" "channel:456" --media ./image.png --dry-run
```

### Presentation Blocks

```bash
openclaw message send --channel discord --target channel:123 --message "Choose:" \
  --presentation '{"blocks":[{"type":"buttons","buttons":[{"label":"Approve","value":"approve","style":"success"},{"label":"Decline","value":"decline","style":"danger"}]}]}'
```

Core renders the same `presentation` payload into Discord components, Slack blocks, Telegram inline buttons, etc., based on channel capabilities.

---

## Models

**Synopsis:** `openclaw models <subcommand> [options]`

**Description:** Model discovery, scanning, and configuration (default model, fallbacks, auth profiles).

### Common Commands

```bash
openclaw models status
openclaw models list
openclaw models list --all
openclaw models list --provider moonshot
openclaw models set openai/gpt-5.4
openclaw models scan
openclaw models aliases list
openclaw models fallbacks list
```

### `models status` Options

| Flag | Description |
|---|---|
| `--json` | Machine-readable output |
| `--plain` | Plain output |
| `--check` | Exit 1=expired/missing, 2=expiring |
| `--probe` | Live probe of configured auth profiles |
| `--probe-provider <name>` | Probe one provider |
| `--probe-profile <id>` | Probe specific profiles (repeat or comma-separated) |
| `--probe-timeout <ms>` | Probe timeout |
| `--probe-concurrency <n>` | Probe concurrency |
| `--probe-max-tokens <n>` | Max tokens for probe |
| `--agent <id>` | Inspect a configured agent's model/auth state |

**Probe status buckets:** `ok`, `auth`, `rate_limit`, `billing`, `timeout`, `format`, `unknown`, `no_model`

### Auth Profiles

```bash
openclaw models auth add
openclaw models auth login --provider openai-codex --set-default
openclaw models auth setup-token --provider <id>
openclaw models auth paste-token
# With expiry:
openclaw models auth paste-token --expires-in 365d
```

### Auth Order (Per-Agent)

```bash
openclaw models auth order get --provider anthropic
openclaw models auth order set --provider anthropic anthropic:default
openclaw models auth order clear --provider anthropic
```

### Image Fallbacks

```bash
openclaw models image-fallbacks list
openclaw models image-fallbacks add <provider/model>
openclaw models image-fallbacks remove <provider/model>
openclaw models image-fallbacks clear
```

### `models scan` Options

| Flag | Description |
|---|---|
| `--no-probe` | Metadata only; no config/secrets lookup |
| `--min-params <b>` | Minimum param size |
| `--max-age-days <days>` | Max model age |
| `--provider <name>` | Filter by provider |
| `--max-candidates <n>` | Max candidates |
| `--timeout <ms>` | Catalog + per-probe timeout |
| `--concurrency <n>` | Probe concurrency |
| `--yes` | Auto-confirm |
| `--no-input` | Non-interactive |
| `--set-default` | Apply best result as default (requires live probe) |
| `--set-image` | Apply best result as image model (requires live probe) |
| `--json` | JSON output |

### Notes/Gotchas

- `models set` accepts `provider/model` or alias.
- `models list` is read-only — does NOT rewrite `models.json`.
- `models list --all` includes bundled provider-owned static catalog rows even when you haven't authenticated.
- `--provider` filter uses provider id (e.g. `moonshot`), NOT display label.
- Model refs parsed by splitting on first `/`. For OpenRouter: `openrouter/moonshotai/kimi-k2`.
- `models status` may show `marker(<value>)` for non-secret placeholders.
- Add `--probe` for live auth probes (real requests — may consume tokens).
- **Usage-window providers:** Anthropic, GitHub Copilot, Gemini CLI, OpenAI Codex, MiniMax, Xiaomi, z.ai — `models status` shows quota snapshots when available.
- **Probe detail/reason codes:** `excluded_by_auth_order`, `missing_credential`, `invalid_expires`, `expired`, `unresolved_ref`, `no_model`.
- `paste-token` requires `--provider`, prompts for token value, writes to profile `<provider>:manual` unless `--profile-id` is specified. `--expires-in <duration>` stores absolute expiry.

---

## Node

**Synopsis:** `openclaw node <subcommand> [options]`

**Description:** Run a headless node host that connects to the Gateway and exposes `system.run`/`system.which` on this machine.

### Run (foreground)

```bash
openclaw node run --host <gateway-host> --port 18789
```

Options: `--host <host>`, `--port <port>`, `--tls`, `--tls-fingerprint <sha256>`, `--node-id <id>`, `--display-name <name>`

### Service (background)

```bash
openclaw node install --host <gateway-host> --port 18789
openclaw node status
openclaw node stop
openclaw node restart
openclaw node uninstall
```

Additional `install` options: `--runtime <node|bun>`, `--force`

### Gateway Auth for Node Host

Resolution order:
1. `OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD` env vars
2. Local config: `gateway.auth.token` / `gateway.auth.password`
3. In `gateway.mode=remote`: remote client fields per remote precedence rules

### Pairing

```bash
# First connection creates pending pairing request:
openclaw devices list
openclaw devices approve <requestId>
```

Node host stores state in `~/.openclaw/node.json`.

### Exec Approvals

`system.run` gated by local exec approvals (`~/.openclaw/exec-approvals.json`):
```bash
openclaw approvals --node <id|name|ip>
```

### Browser Proxy (zero-config)

Node hosts automatically advertise a browser proxy. Disable:
```json5
{ "nodeHost": { "browserProxy": { "enabled": false } } }
```

### Notes/Gotchas

- For non-loopback `ws://` on trusted private network: `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1`
- `openclaw node install` persists this env var into the supervised node service when present.
- Approved async node exec uses canonical `systemRunPlan` — edits after approval request rejected.

---

## Nodes

**Synopsis:** `openclaw nodes <subcommand> [options]`

**Description:** Manage paired nodes and invoke node capabilities.

### Common Commands

```bash
openclaw nodes list
openclaw nodes list --connected
openclaw nodes list --last-connected 24h
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes reject <requestId>
openclaw nodes rename --node <id|name|ip> --name <displayName>
openclaw nodes status
openclaw nodes status --connected
openclaw nodes status --last-connected 24h
```

### Invoke

```bash
openclaw nodes invoke --node <id|name|ip> --command <command> --params '{"key":"value"}'
```

Options: `--params <json>`, `--invoke-timeout <ms>` (default 15000), `--idempotency-key <key>`

> `system.run` and `system.run.prepare` are blocked here; use `exec` tool with `host=node` for shell execution.

### Common Options

- `--url`, `--token`, `--timeout`, `--json`

### Approval Scope Requirements

- `nodes pending`: pairing scope only
- `nodes approve <requestId>`:
  - commandless: pairing only
  - non-exec node commands: pairing + write
  - `system.run`/`system.run.prepare`/`system.which`: pairing + admin

---

## Onboard

**Synopsis:** `openclaw onboard [options]`

**Description:** Interactive onboarding for local or remote Gateway setup.

### Examples

```bash
openclaw onboard
openclaw onboard --flow quickstart
openclaw onboard --flow manual
openclaw onboard --skip-bootstrap
openclaw onboard --mode remote --remote-url wss://gateway-host:18789

# Non-interactive custom provider
openclaw onboard --non-interactive \
  --auth-choice custom-api-key \
  --custom-base-url "https://llm.example.com/v1" \
  --custom-model-id "foo-large" \
  --custom-api-key "$CUSTOM_API_KEY" \
  --secret-input-mode plaintext \
  --custom-compatibility openai

# Non-interactive Ollama
openclaw onboard --non-interactive \
  --auth-choice ollama \
  --custom-base-url "http://ollama-host:11434" \
  --custom-model-id "qwen3.5:27b" \
  --accept-risk

# Store as SecretRef instead of plaintext
openclaw onboard --non-interactive \
  --auth-choice openai-api-key \
  --secret-input-mode ref \
  --accept-risk

# Gateway token as SecretRef
export OPENCLAW_GATEWAY_TOKEN="your-token"
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice skip \
  --gateway-auth token \
  --gateway-token-ref-env OPENCLAW_GATEWAY_TOKEN \
  --accept-risk
```

### Key Options

| Flag | Description |
|---|---|
| `--flow <quickstart\|manual>` | Onboarding flow |
| `--skip-bootstrap` | Skip creating workspace bootstrap files |
| `--mode <local\|remote>` | Onboarding mode |
| `--remote-url <url>` | Remote Gateway WebSocket URL |
| `--non-interactive` | Run without prompts |
| `--auth-choice <choice>` | Auth provider choice |
| `--custom-base-url <url>` | Custom provider base URL |
| `--custom-model-id <id>` | Custom model ID |
| `--custom-api-key <key>` | Custom API key |
| `--custom-compatibility <openai\|anthropic\|unknown>` | Compatibility mode |
| `--secret-input-mode <plaintext\|ref>` | How to store secrets |
| `--gateway-auth <token\|password\|none>` | Gateway auth mode |
| `--gateway-token <token>` | Gateway token (plaintext) |
| `--gateway-token-ref-env <name>` | Gateway token env SecretRef |
| `--install-daemon` | Install gateway daemon |
| `--skip-health` | Skip waiting for reachable local gateway |
| `--accept-risk` | Accept risk warnings |

### Notes/Gotchas

- `quickstart`: minimal prompts, auto-generates gateway token.
- `manual` / `advanced`: full prompts for port/bind/auth.
- `--json` does NOT imply non-interactive mode. Use `--non-interactive` for scripts.
- `--gateway-token` and `--gateway-token-ref-env` are mutually exclusive.
- Local onboarding writes `gateway.mode="local"` into config.

---

## Pairing

**Synopsis:** `openclaw pairing <subcommand> [options]`

**Description:** Approve or inspect DM pairing requests for channels that support pairing.

### Commands

```bash
openclaw pairing list telegram
openclaw pairing list --channel telegram --account work
openclaw pairing list telegram --json

openclaw pairing approve <code>
openclaw pairing approve telegram <code>
openclaw pairing approve --channel telegram --account work <code> --notify
```

### `pairing list` Options

- `[channel]` (positional), `--channel <channel>`, `--account <accountId>`, `--json`

### `pairing approve` Options

- `--channel <channel>`, `--account <accountId>`, `--notify` (send confirmation back to requester)

### Notes/Gotchas

- With multiple pairing-capable channels configured, must provide channel.
- With only one channel: `pairing approve <code>` without specifying channel is allowed.

---

## Plugins

**Synopsis:** `openclaw plugins <subcommand> [options]`

**Description:** Manage Gateway plugins, hook packs, and compatible bundles.

### Commands

```bash
openclaw plugins list
openclaw plugins list --enabled
openclaw plugins list --verbose
openclaw plugins list --json
openclaw plugins install <path-or-spec>
openclaw plugins inspect <id>
openclaw plugins inspect <id> --json
openclaw plugins inspect --all
openclaw plugins info <id>          # alias for inspect
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw plugins uninstall <id>
openclaw plugins uninstall <id> --dry-run
openclaw plugins uninstall <id> --keep-files
openclaw plugins doctor
openclaw plugins update <id-or-npm-spec>
openclaw plugins update --all
openclaw plugins update <id-or-npm-spec> --dry-run
openclaw plugins marketplace list <source>
openclaw plugins marketplace list <source> --json
```

### Install

```bash
openclaw plugins install <package>                       # ClawHub first, then npm
openclaw plugins install clawhub:<package>               # ClawHub only
openclaw plugins install clawhub:<package>@1.2.3         # Specific ClawHub version
openclaw plugins install <package> --force               # overwrite existing
openclaw plugins install <package> --pin                 # pin version
openclaw plugins install <package> --dangerously-force-unsafe-install
openclaw plugins install <path>                          # local path
openclaw plugins install -l ./my-plugin                  # link without copying
openclaw plugins install <plugin>@<marketplace>          # marketplace
openclaw plugins install <plugin> --marketplace <name>
openclaw plugins install <plugin> --marketplace https://github.com/<owner>/<repo>
```

### Update

```bash
openclaw plugins update <id-or-npm-spec>
openclaw plugins update --all
openclaw plugins update <id-or-npm-spec> --dry-run
openclaw plugins update @openclaw/voice-call@beta
```

### Inspect

Shows: identity, load status, source, capabilities, hooks, tools, commands, services, gateway methods, HTTP routes, policy flags, diagnostics, install metadata, bundle capabilities, MCP/LSP server support.

**Plugin shape classifications:**
- `plain-capability`: one capability type
- `hybrid-capability`: multiple capability types
- `hook-only`: only hooks
- `non-capability`: tools/commands/services but no capabilities

### Doctor

```bash
openclaw plugins doctor
# For module-shape failures, set: OPENCLAW_PLUGIN_LOAD_DEBUG=1
```

### Marketplace Sources

- Local marketplace path or `marketplace.json` path
- `owner/repo` GitHub shorthand
- GitHub URL or git URL

### Notes/Gotchas

- Npm specs: registry-only (exact version or dist-tag). No git/URL/file specs or semver ranges.
- Bare specs and `@latest` stay on stable track. If npm resolves to prerelease, OpenClaw stops.
- `--force` overwrites existing install in place.
- `--link` adds to `plugins.load.paths` instead of copying.
- `--dangerously-force-unsafe-install` for false positives in scanner (does NOT bypass policy blocks).
- After changing plugin code/enablement/hooks: **restart the Gateway**.
- If `plugins.allow` present in config, bundled browser plugin must be listed explicitly.
- `plugins list` is NOT a live runtime probe — does not probe running Gateway.

---

## Proxy

**Synopsis:** `openclaw proxy <subcommand> [options]`

**Description:** Run local explicit debug proxy and inspect captured traffic. For transport-level investigation.

### Commands

```bash
openclaw proxy start [--host <host>] [--port <port>]
openclaw proxy run [--host <host>] [--port <port>] -- <cmd...>
openclaw proxy coverage
openclaw proxy sessions [--limit <count>]
openclaw proxy query --preset <name> [--session <id>]
openclaw proxy blob --id <blobId>
openclaw proxy purge
```

### Query Presets

`openclaw proxy query --preset <name>` accepts:
- `double-sends`, `retry-storms`, `cache-busting`
- `ws-duplicate-frames`, `missing-ack`, `error-bursts`

### Notes/Gotchas

- `start` defaults to `127.0.0.1` unless `--host` set.
- `run` starts local debug proxy then runs command after `--`.
- Use `openclaw proxy purge` when done to remove capture data.

---

## QR

**Synopsis:** `openclaw qr [options]`

**Description:** Generate a mobile pairing QR and setup code from your current Gateway configuration.

### Options

| Flag | Description |
|---|---|
| `--remote` | Prefer `gateway.remote.url` |
| `--url <url>` | Override gateway URL in payload |
| `--public-url <url>` | Override public URL in payload |
| `--token <token>` | Override gateway token for bootstrap flow |
| `--password <password>` | Override gateway password for bootstrap flow |
| `--setup-code-only` | Print only setup code |
| `--no-ascii` | Skip ASCII QR rendering |
| `--json` | Emit JSON: `setupCode`, `gatewayUrl`, `auth`, `urlSource` |

### Examples

```bash
openclaw qr
openclaw qr --setup-code-only
openclaw qr --json
openclaw qr --remote
openclaw qr --url wss://gateway.example/ws
```

### Notes/Gotchas

- `--token` and `--password` are mutually exclusive.
- Setup code carries a short-lived `bootstrapToken`, NOT the shared gateway token/password.
- Mobile pairing fails closed for Tailscale/public `ws://` URLs. Private LAN `ws://` supported.
- With `--remote`, requires `gateway.remote.url` or `gateway.tailscale.mode=serve|funnel`.
- After scanning: `openclaw devices list` → `openclaw devices approve <requestId>`

---

## Reset

**Synopsis:** `openclaw reset [options]`

**Description:** Reset local config/state (keeps the CLI installed).

### Options

| Flag | Description |
|---|---|
| `--scope <scope>` | `config`, `config+creds+sessions`, or `full` |
| `--yes` | Skip confirmation prompts |
| `--non-interactive` | Disable prompts (requires `--scope` and `--yes`) |
| `--dry-run` | Print actions without removing files |

### Examples

```bash
openclaw backup create    # backup first!
openclaw reset
openclaw reset --dry-run
openclaw reset --scope config --yes --non-interactive
openclaw reset --scope config+creds+sessions --yes --non-interactive
openclaw reset --scope full --yes --non-interactive
```

---

## Sandbox

**Synopsis:** `openclaw sandbox <subcommand> [options]`

**Description:** Manage sandbox runtimes for isolated agent execution (Docker, SSH, OpenShell).

### Commands

```bash
# Explain effective sandbox settings
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --agent work
openclaw sandbox explain --json

# List sandbox runtimes
openclaw sandbox list
openclaw sandbox list --browser
openclaw sandbox list --json

# Recreate runtimes
openclaw sandbox recreate --all
openclaw sandbox recreate --session main
openclaw sandbox recreate --agent mybot
openclaw sandbox recreate --browser
openclaw sandbox recreate --all --force
```

### Use Cases

```bash
# After updating Docker image
docker pull openclaw-sandbox:latest
docker tag openclaw-sandbox:latest openclaw-sandbox:bookworm-slim
openclaw sandbox recreate --all

# After changing sandbox config
# Edit: agents.defaults.sandbox.*
openclaw sandbox recreate --all

# After changing SSH target
# Edit: agents.defaults.sandbox.ssh.*
openclaw sandbox recreate --all

# For a specific agent only
openclaw sandbox recreate --agent alfred
```

### Configuration (in `openclaw.json`)

```jsonc
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "all",        // off, non-main, all
        "backend": "docker",  // docker, ssh, openshell
        "scope": "agent",     // session, agent, shared
        "docker": {
          "image": "openclaw-sandbox:bookworm-slim",
          "containerPrefix": "openclaw-sbx-"
        },
        "prune": {
          "idleHours": 24,
          "maxAgeDays": 7
        }
      }
    }
  }
}
```

### Notes/Gotchas

- Existing runtimes keep running with old settings until recreated or 24h idle prune.
- For SSH/OpenShell `remote`, `recreate` deletes the canonical remote workspace (re-seeded on next use).
- Prefer `openclaw sandbox recreate` over manual backend-specific cleanup.

---

## Secrets

**Synopsis:** `openclaw secrets <subcommand> [options]`

**Description:** Manage SecretRefs and keep active runtime snapshot healthy.

### Recommended Operator Loop

```bash
openclaw secrets audit --check
openclaw secrets configure
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json
openclaw secrets audit --check
openclaw secrets reload
```

### `secrets reload`

```bash
openclaw secrets reload
openclaw secrets reload --json
openclaw secrets reload --url ws://127.0.0.1:18789 --token <token>
```

> If resolution fails, gateway keeps last-known-good snapshot (no partial activation).

### `secrets audit`

```bash
openclaw secrets audit
openclaw secrets audit --check          # exit 1 on findings, 2 on unresolved refs
openclaw secrets audit --json
openclaw secrets audit --allow-exec     # also check exec SecretRefs
```

**Scans for:** plaintext storage, unresolved refs, precedence drift, generated model.json residues, legacy residues

**Finding codes:** `PLAINTEXT_FOUND`, `REF_UNRESOLVED`, `REF_SHADOWED`, `LEGACY_RESIDUE`

### `secrets configure` (Interactive TTY required)

```bash
openclaw secrets configure
openclaw secrets configure --plan-out /tmp/openclaw-secrets-plan.json
openclaw secrets configure --apply --yes
openclaw secrets configure --providers-only
openclaw secrets configure --skip-provider-setup
openclaw secrets configure --agent ops
```

Options: `--providers-only`, `--skip-provider-setup`, `--agent <id>`, `--allow-exec`, `--json`

### `secrets apply`

```bash
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --allow-exec
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run --allow-exec
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --json
```

**What `apply` updates:** `openclaw.json` (SecretRef targets + provider upserts), `auth-profiles.json`, legacy `auth.json`, `~/.openclaw/.env` known secret keys

### Notes/Gotchas

- No rollback backups — apply path is one-way for scrubbed plaintext values.
- Write mode rejects exec-containing plans unless `--allow-exec` set.
- Safety: strict preflight + atomic-ish apply with best-effort in-memory restore on failure.

---

## Security

**Synopsis:** `openclaw security audit [options]`

**Description:** Security audit tools with optional fixes.

### Audit

```bash
openclaw security audit
openclaw security audit --deep
openclaw security audit --deep --token <token>
openclaw security audit --fix
openclaw security audit --json
```

### What Audit Warns About

- Multiple DM senders sharing main session (recommends `session.dmScope="per-channel-peer"`)
- Shared-user ingress heuristic (open DM/group policy, wildcard sender rules)
- Small models (≤300B) without sandboxing with web/browser tools enabled
- Webhook ingress security (token reuse, short token, path="/", etc.)
- Sandbox Docker settings with sandbox mode off
- Ineffective `gateway.nodes.denyCommands` patterns (exact command-name only, not shell-text)
- Open groups exposing runtime/filesystem tools without sandbox guards
- `gateway.allowRealIpFallback=true` (header-spoofing risk)
- `discovery.mdns.mode="full"` (metadata leakage)
- Unpinned/missing-integrity npm-based plugin install records
- Channel allowlists using mutable names instead of stable IDs
- `gateway.auth.mode="none"` (no shared secret)
- Sandbox browser using Docker `bridge` network without `sandbox.browser.cdpSourceRange`

### JSON for CI/Policy Checks

```bash
openclaw security audit --json | jq '.summary'
openclaw security audit --deep --json | jq '.findings[] | select(.severity=="critical") | .checkId'
openclaw security audit --fix --json | jq '{fix: .fix.ok, summary: .report.summary}'
```

### What `--fix` Changes

✅ Changes:
- Flips `groupPolicy="open"` to `groupPolicy="allowlist"`
- Seeds `groupAllowFrom` from `allowFrom` file (WhatsApp)
- Sets `logging.redactSensitive` from `"off"` to `"tools"`
- Tightens permissions for state/config and sensitive files

❌ Does NOT change:
- Rotate tokens/passwords/API keys
- Disable tools
- Change gateway bind/auth/network choices
- Remove plugins/skills

---

## Sessions

**Synopsis:** `openclaw sessions [options]`

**Description:** List stored conversation sessions.

### Examples

```bash
openclaw sessions
openclaw sessions --agent work
openclaw sessions --all-agents
openclaw sessions --active 120
openclaw sessions --verbose
openclaw sessions --json
```

### Scope Selection

- Default: configured default agent store
- `--agent <id>`: one configured agent store
- `--all-agents`: all configured agent stores
- `--store <path>`: explicit store path

### Cleanup

```bash
openclaw sessions cleanup --dry-run
openclaw sessions cleanup --agent work --dry-run
openclaw sessions cleanup --all-agents --dry-run
openclaw sessions cleanup --enforce
openclaw sessions cleanup --enforce --active-key "agent:main:telegram:direct:123"
openclaw sessions cleanup --json
```

**Cleanup options:** `--dry-run`, `--enforce` (apply even in warn mode), `--fix-missing`, `--active-key <key>`, `--agent <id>`, `--all-agents`, `--store <path>`, `--json`

### Notes/Gotchas

- `sessions cleanup` maintains session stores/transcripts only. Cron run logs managed separately.
- `--all-agents` reads configured stores AND discovers disk-only stores under default `agents/` root.

---

## Setup

**Synopsis:** `openclaw setup [options]`

**Description:** Initialize `~/.openclaw/openclaw.json` and agent workspace.

### Options

| Flag | Description |
|---|---|
| `--workspace <dir>` | Agent workspace directory |
| `--wizard` | Run onboarding |
| `--non-interactive` | Run without prompts |
| `--mode <local\|remote>` | Onboarding mode |
| `--remote-url <url>` | Remote Gateway WebSocket URL |
| `--remote-token <token>` | Remote Gateway token |

### Examples

```bash
openclaw setup
openclaw setup --workspace ~/.openclaw/workspace
openclaw setup --wizard
openclaw setup --non-interactive --mode remote --remote-url wss://gateway-host:18789 --remote-token <token>
```

### Notes/Gotchas

- Plain `openclaw setup` initializes config + workspace WITHOUT the full onboarding flow.
- Onboarding auto-runs when any onboarding flags present (`--wizard`, `--non-interactive`, `--mode`, etc.).

---

## Skills

**Synopsis:** `openclaw skills <subcommand> [options]`

**Description:** Inspect local skills and install/update from ClawHub.

### Commands

```bash
openclaw skills search "calendar"
openclaw skills search --limit 20 --json
openclaw skills install <slug>
openclaw skills install <slug> --version <version>
openclaw skills install <slug> --force
openclaw skills update <slug>
openclaw skills update --all
openclaw skills list
openclaw skills list --eligible
openclaw skills list --json
openclaw skills list --verbose
openclaw skills info <name>
openclaw skills info <name> --json
openclaw skills check
openclaw skills check --json
```

### Notes/Gotchas

- `search`/`install`/`update` use ClawHub; install into active workspace `skills/` directory.
- `list`/`info`/`check` inspect local skills (not live ClawHub).
- `install --force` overwrites existing workspace skill folder.
- `update --all` only updates tracked ClawHub installs in active workspace.
- `list` is default action when no subcommand provided.

---

## Status

**Synopsis:** `openclaw status [options]`

**Description:** Diagnostics for channels + sessions.

### Examples

```bash
openclaw status
openclaw status --all
openclaw status --deep
openclaw status --usage
```

### Notes/Gotchas

- `--deep`: runs live probes (WhatsApp Web, Telegram, Discord, Slack, Signal).
- `--usage`: prints normalized provider usage windows as `X% left`.
- Session status: `Runtime:` = execution path/sandbox state; `Runner:` = embedded Pi, CLI-backed, or ACP.
- Output includes per-agent session stores when multiple agents configured.
- Overview includes Gateway + node host service status, update channel + git SHA.
- If update available, hints to run `openclaw update`.
- `--all` includes Secrets overview and diagnosis section.
- SecretRefs resolved in read-only mode for targeted config paths.

---

## System

**Synopsis:** `openclaw system <subcommand> [options]`

**Description:** System-level helpers for the Gateway: system events, heartbeat control, presence.

All subcommands use Gateway RPC. Shared options: `--url`, `--token`, `--timeout <ms>`, `--expect-final`

### Commands

```bash
# Enqueue system event (injected at next heartbeat as "System:" prompt line)
openclaw system event --text "Check for urgent follow-ups" --mode now
openclaw system event --text "Check for urgent follow-ups" --url ws://127.0.0.1:18789 --token "$OPENCLAW_GATEWAY_TOKEN"

# Heartbeat controls
openclaw system heartbeat enable
openclaw system heartbeat disable
openclaw system heartbeat last

# Presence
openclaw system presence
openclaw system presence --json
```

### `system event` Flags

- `--text <text>`: required event text
- `--mode <now|next-heartbeat>`: when to trigger (default `next-heartbeat`)
- `--json`

### Notes/Gotchas

- Requires running Gateway.
- System events are ephemeral — not persisted across restarts.

---

## Tasks

**Synopsis:** `openclaw tasks [subcommand] [options]`

**Description:** Inspect durable background tasks and Task Flow state. No subcommand = `tasks list`.

### Commands

```bash
openclaw tasks
openclaw tasks list
openclaw tasks list --runtime acp
openclaw tasks list --status running
openclaw tasks list --json
openclaw tasks show <lookup>
openclaw tasks notify <lookup> state_changes
openclaw tasks cancel <lookup>
openclaw tasks audit
openclaw tasks audit --severity warn --code <name> --limit 50 --json
openclaw tasks maintenance
openclaw tasks maintenance --apply
openclaw tasks maintenance --apply --json
openclaw tasks flow list
openclaw tasks flow list --status running --json
openclaw tasks flow show <lookup>
openclaw tasks flow cancel <lookup>
```

### Root Options

- `--json`
- `--runtime <subagent|acp|cron|cli>`: filter by runtime kind
- `--status <queued|running|succeeded|failed|timed_out|cancelled|lost>`: filter by status

### Subcommands

| Subcommand | Description |
|---|---|
| `list` | List background tasks, newest first |
| `show <lookup>` | Show one task by task ID, run ID, or session key |
| `notify <lookup> <policy>` | Change notification policy: `done_only\|state_changes\|silent` |
| `cancel <lookup>` | Cancel a running task |
| `audit` | Surface stale, lost, delivery-failed, or inconsistent task records |
| `maintenance [--apply]` | Preview or apply task reconciliation, cleanup, and pruning |
| `flow list` | List Task Flow state |
| `flow show <lookup>` | Show one Task Flow |
| `flow cancel <lookup>` | Cancel a Task Flow |

---

## TUI / chat / terminal

**Synopsis:** `openclaw tui [options]`  
**Aliases:** `openclaw chat` = `openclaw terminal` = `openclaw tui --local`

**Description:** Open the terminal UI connected to the Gateway, or run in local embedded mode.

### Examples

```bash
openclaw chat
openclaw tui --local
openclaw tui
openclaw tui --url ws://127.0.0.1:18789 --token <token>
openclaw tui --session main --deliver
openclaw chat --message "Compare my config to the docs and tell me what to fix"
openclaw tui --session bugfix   # auto-infers agent when run inside agent workspace dir
```

### Key Options

- `--local`: run embedded agent directly (most local tools work; Gateway-only features unavailable)
- `--url <url>`, `--token <token>`, `--password <password>`: explicit Gateway connection
- `--session <key>`: session key
- `--deliver`: send reply back to selected channel

### Config Repair Loop

```bash
# When config is already valid, use local mode:
openclaw chat

# Inside TUI:
# !openclaw config file
# !openclaw docs gateway auth token secretref
# !openclaw config validate
# !openclaw doctor
```

> If `openclaw config validate` is failing, use `openclaw configure` or `openclaw doctor --fix` first.

### Notes/Gotchas

- `chat` and `terminal` are aliases for `openclaw tui --local`.
- `--local` cannot be combined with `--url`, `--token`, or `--password`.
- Plugin approval gates still apply in local mode.
- When launched from inside a configured agent workspace, auto-selects that agent for session key default.
- Local mode adds `/auth [provider]` inside the TUI command surface.

---

## Uninstall

**Synopsis:** `openclaw uninstall [options]`

**Description:** Uninstall gateway service + local data (CLI binary remains).

### Options

| Flag | Description |
|---|---|
| `--service` | Remove gateway service |
| `--state` | Remove state and config |
| `--workspace` | Remove workspace directories |
| `--app` | Remove macOS app |
| `--all` | Remove service, state, workspace, and app |
| `--yes` | Skip confirmation prompts |
| `--non-interactive` | Disable prompts (requires `--yes`) |
| `--dry-run` | Print actions without removing files |

### Examples

```bash
openclaw backup create    # backup first!
openclaw uninstall
openclaw uninstall --service --yes --non-interactive
openclaw uninstall --state --workspace --yes --non-interactive
openclaw uninstall --all --yes
openclaw uninstall --dry-run
```

---

## Update

**Synopsis:** `openclaw update [options]`

**Description:** Safely update OpenClaw and switch between stable/beta/dev channels.

### Commands

```bash
openclaw update
openclaw update status
openclaw update wizard
openclaw update --channel beta
openclaw update --channel dev
openclaw update --tag beta
openclaw update --tag main
openclaw update --dry-run
openclaw update --no-restart
openclaw update --yes
openclaw update --json
openclaw --update            # shorthand
```

### Options

| Flag | Description |
|---|---|
| `--no-restart` | Skip restarting Gateway after update |
| `--channel <stable\|beta\|dev>` | Set update channel (persisted in config) |
| `--tag <dist-tag\|version\|spec>` | Override package target for this update only |
| `--dry-run` | Preview actions without writing/installing |
| `--json` | Print machine-readable `UpdateRunResult` JSON |
| `--timeout <seconds>` | Per-step timeout (default 1200s) |
| `--yes` | Skip confirmation prompts |

### `update status`

```bash
openclaw update status
openclaw update status --json
openclaw update status --timeout 10
```

### `update wizard`

Interactive flow to pick channel and confirm restart behavior.

### Channels

| Channel | Behavior |
|---|---|
| `stable` | npm `latest` tag |
| `beta` | npm `beta` tag (falls back to stable if missing/older) |
| `dev` | git checkout of `main` branch |

### Git Checkout Flow (source installs)

1. Requires clean worktree.
2. Switches to selected channel (tag or branch).
3. Fetches upstream (dev only).
4. Dev: preflight lint + TypeScript build in temp worktree; walks back up to 10 commits if tip fails.
5. Rebases onto selected commit (dev only).
6. Installs deps.
7. Builds + Control UI.
8. Runs `openclaw doctor`.
9. Syncs plugins.

### Notes/Gotchas

- Downgrades require confirmation (older versions can break config).
- If exact pinned npm plugin resolves to artifact with different integrity, update aborts.
- For git checkout with pnpm: bootstraps `pnpm` on demand via `corepack`.

---

## Voicecall (plugin)

**Synopsis:** `openclaw voicecall <subcommand>`

**Description:** Plugin-provided command. Only appears if voice-call plugin is installed and enabled.

### Commands

```bash
openclaw voicecall status --call-id <id>
openclaw voicecall call --to "+15555550123" --message "Hello" --mode notify
openclaw voicecall continue --call-id <id> --message "Any questions?"
openclaw voicecall dtmf --call-id <id> --digits "ww123456#"
openclaw voicecall end --call-id <id>

# Expose webhooks (Tailscale)
openclaw voicecall expose --mode serve
openclaw voicecall expose --mode funnel
openclaw voicecall expose --mode off
```

### Notes/Gotchas

- Only expose webhook endpoint to trusted networks. Prefer Tailscale Serve over Funnel.
- See: [Voice Call plugin docs](https://docs.openclaw.ai/plugins/voice-call)

---

## Webhooks

**Synopsis:** `openclaw webhooks <subcommand> [options]`

**Description:** Webhook helpers and integrations (Gmail Pub/Sub).

### Gmail

```bash
openclaw webhooks gmail setup --account you@example.com
openclaw webhooks gmail setup --account you@example.com --project my-gcp-project --json
openclaw webhooks gmail setup --account you@example.com --hook-url https://gateway.example.com/hooks/gmail
openclaw webhooks gmail run --account you@example.com
```

### `webhooks gmail setup` Options

| Flag | Description |
|---|---|
| `--account <email>` | Required |
| `--project <id>` | GCP project |
| `--topic <name>` | Pub/Sub topic |
| `--subscription <name>` | Pub/Sub subscription |
| `--label <label>` | Gmail label |
| `--hook-url <url>` | OpenClaw webhook URL |
| `--hook-token <token>` | Webhook auth token |
| `--push-token <token>` | Pub/Sub push token |
| `--bind <host>` | Bind host |
| `--port <port>` | Bind port |
| `--path <path>` | Webhook path |
| `--include-body` | Include email body |
| `--max-bytes <n>` | Max body bytes |
| `--renew-minutes <n>` | Auto-renewal interval |
| `--tailscale <funnel\|serve\|off>` | Tailscale exposure mode |
| `--tailscale-path <path>` | Tailscale path |
| `--tailscale-target <target>` | Tailscale target |
| `--push-endpoint <url>` | Push endpoint URL |
| `--json` | Machine-readable output |

### `webhooks gmail run` Options

Same as `setup` minus `--push-endpoint` and `--json`. Runs `gog watch serve` plus auto-renew loop.

---

## Wiki

**Synopsis:** `openclaw wiki <subcommand> [options]`

**Description:** Inspect and maintain the `memory-wiki` vault. Provided by the bundled `memory-wiki` plugin.

### Commands

```bash
openclaw wiki status
openclaw wiki doctor
openclaw wiki init
openclaw wiki ingest ./notes/alpha.md
openclaw wiki compile
openclaw wiki lint
openclaw wiki search "alpha"
openclaw wiki get entity.alpha
openclaw wiki get syntheses/alpha-summary.md --from 1 --lines 80

# Apply narrow mutations
openclaw wiki apply synthesis "Alpha Summary" \
  --body "Short synthesis body" \
  --source-id source.alpha

openclaw wiki apply metadata entity.alpha \
  --source-id source.alpha \
  --status review \
  --question "Still active?"

# Bridge import (bridge mode)
openclaw wiki bridge import

# Unsafe local import
openclaw wiki unsafe-local import

# Obsidian helpers
openclaw wiki obsidian status
openclaw wiki obsidian search "alpha"
openclaw wiki obsidian open syntheses/alpha-summary.md
openclaw wiki obsidian command workspace:quick-switcher
openclaw wiki obsidian daily
```

### Command Reference

| Command | Description |
|---|---|
| `wiki status` | Inspect vault mode, health, Obsidian CLI availability |
| `wiki doctor` | Run health checks, surface config/vault problems |
| `wiki init` | Create wiki vault layout and starter pages |
| `wiki ingest <path-or-url>` | Import content into wiki source layer |
| `wiki compile` | Rebuild indexes, dashboards, compiled digests |
| `wiki lint` | Lint vault: structural issues, contradictions, stale pages |
| `wiki search <query>` | Search wiki content |
| `wiki get <lookup>` | Read wiki page by id or relative path |
| `wiki apply` | Apply narrow mutations (synthesis, metadata, claims) |
| `wiki bridge import` | Import from active memory plugin (bridge mode) |
| `wiki unsafe-local import` | Import from local paths (experimental) |
| `wiki obsidian ...` | Obsidian helper commands |

### Configuration Tie-ins

- `plugins.entries.memory-wiki.config.vaultMode`
- `plugins.entries.memory-wiki.config.search.backend`
- `plugins.entries.memory-wiki.config.search.corpus`
- `plugins.entries.memory-wiki.config.bridge.*`
- `plugins.entries.memory-wiki.config.obsidian.*`
- `plugins.entries.memory-wiki.config.render.*`
- `plugins.entries.memory-wiki.config.context.includeCompiledDigestPrompt`

### Practical Guidance

- Use `wiki search` + `wiki get` when provenance and page identity matter.
- Use `wiki apply` instead of hand-editing managed generated sections.
- Use `wiki lint` before trusting contradictory or low-confidence content.
- Use `wiki compile` after bulk imports for fresh dashboards immediately.
- Use `wiki bridge import` when bridge mode depends on newly exported memory artifacts.

---

## Quick Reference Table

| Command | One-line Description |
|---|---|
| `openclaw acp` | ACP bridge from IDE → Gateway over WebSocket |
| `openclaw acp client` | Debug ACP client — type prompts interactively |
| `openclaw agent` | Run a single agent turn via Gateway |
| `openclaw agents list` | List configured agents |
| `openclaw agents add` | Add a new isolated agent |
| `openclaw agents bind` | Add channel routing binding to agent |
| `openclaw agents unbind` | Remove channel routing binding |
| `openclaw agents delete` | Delete an isolated agent |
| `openclaw agents set-identity` | Set agent identity (name/emoji/avatar) |
| `openclaw approvals get` | Show effective exec approval policy |
| `openclaw approvals set` | Replace exec approvals from file/stdin |
| `openclaw approvals allowlist` | Add/remove exec allowlist entries |
| `openclaw exec-policy` | Local shortcut for exec approval presets |
| `openclaw backup create` | Create backup archive of state + config + workspace |
| `openclaw backup verify` | Validate a backup archive |
| `openclaw browser` | Manage browser control (lifecycle/tabs/automation) |
| `openclaw channels list` | List configured channel accounts |
| `openclaw channels status` | Show channel status (with optional live probe) |
| `openclaw channels capabilities` | Inspect channel capabilities |
| `openclaw channels resolve` | Resolve names to channel IDs |
| `openclaw channels logs` | Tail channel logs |
| `openclaw channels add` | Add a channel account |
| `openclaw channels remove` | Remove a channel account |
| `openclaw channels login` | Interactive OAuth login for channel |
| `openclaw channels logout` | Logout channel account |
| `openclaw clawbot qr` | Legacy alias for `openclaw qr` |
| `openclaw completion` | Generate shell completion scripts |
| `openclaw config get` | Get a config value by path |
| `openclaw config set` | Set a config value (value/SecretRef/provider/batch) |
| `openclaw config unset` | Unset a config value |
| `openclaw config file` | Print active config file path |
| `openclaw config schema` | Print JSON schema for openclaw.json |
| `openclaw config validate` | Validate config file |
| `openclaw configure` | Interactive config setup wizard |
| `openclaw cron list` | List cron jobs |
| `openclaw cron add` | Add a cron job |
| `openclaw cron edit` | Edit a cron job |
| `openclaw cron rm` | Remove a cron job |
| `openclaw cron run` | Manually trigger a cron job |
| `openclaw cron enable/disable` | Enable or disable a cron job |
| `openclaw cron runs` | Show run history for a cron job |
| `openclaw daemon` | Legacy alias for `openclaw gateway` service commands |
| `openclaw dashboard` | Open Control UI |
| `openclaw devices list` | List paired devices |
| `openclaw devices approve` | Approve a device pairing request |
| `openclaw devices reject` | Reject a device pairing request |
| `openclaw devices remove` | Remove a paired device |
| `openclaw devices clear` | Clear pending device requests |
| `openclaw devices rotate` | Rotate a device token |
| `openclaw devices revoke` | Revoke a device token |
| `openclaw directory self` | Look up own channel identity |
| `openclaw directory peers list` | List channel contacts/peers |
| `openclaw directory groups list` | List channel groups |
| `openclaw directory groups members` | List group members |
| `openclaw dns setup` | Configure wide-area DNS discovery |
| `openclaw docs` | Search live docs |
| `openclaw doctor` | Health checks + quick fixes |
| `openclaw gateway` | Run or query the Gateway |
| `openclaw gateway health` | Check Gateway health |
| `openclaw gateway status` | Show Gateway service status |
| `openclaw gateway probe` | Debug-probe all Gateway targets |
| `openclaw gateway stability` | Fetch diagnostic stability recorder |
| `openclaw gateway diagnostics export` | Export diagnostics zip |
| `openclaw gateway usage-cost` | Fetch usage-cost summaries |
| `openclaw gateway call` | Low-level Gateway RPC call |
| `openclaw gateway discover` | Discover Gateways via Bonjour |
| `openclaw gateway install/start/stop/restart/uninstall` | Manage Gateway service |
| `openclaw health` | Fetch health from running Gateway |
| `openclaw hooks list` | List agent hooks |
| `openclaw hooks info` | Show hook details |
| `openclaw hooks check` | Show hook eligibility summary |
| `openclaw hooks enable` | Enable a hook |
| `openclaw hooks disable` | Disable a hook |
| `openclaw infer model run` | Run a text/model prompt |
| `openclaw infer image generate` | Generate an image |
| `openclaw infer image describe` | Describe an image file |
| `openclaw infer audio transcribe` | Transcribe audio file |
| `openclaw infer tts convert` | Synthesize speech |
| `openclaw infer video generate` | Generate a video |
| `openclaw infer video describe` | Describe a video file |
| `openclaw infer web search` | Search the web |
| `openclaw infer web fetch` | Fetch a web page |
| `openclaw infer embedding create` | Create vector embeddings |
| `openclaw logs` | Tail Gateway file logs |
| `openclaw mcp serve` | Run OpenClaw as MCP server |
| `openclaw mcp list/show/set/unset` | Manage saved MCP server definitions |
| `openclaw memory status` | Show memory plugin status |
| `openclaw memory index` | Reindex memory store |
| `openclaw memory search` | Search semantic memory |
| `openclaw memory promote` | Preview/apply memory promotions to MEMORY.md |
| `openclaw memory promote-explain` | Explain promotion score breakdown |
| `openclaw memory rem-harness` | Preview REM reflections without writing |
| `openclaw message send` | Send message on any channel |
| `openclaw message poll` | Create a poll |
| `openclaw message react` | React to a message |
| `openclaw message read` | Read messages from a channel |
| `openclaw message broadcast` | Broadcast message to multiple targets |
| `openclaw models status` | Show model/auth status |
| `openclaw models list` | List available models |
| `openclaw models set` | Set default model |
| `openclaw models auth` | Manage provider auth profiles |
| `openclaw node run` | Run headless node host (foreground) |
| `openclaw node install` | Install headless node host as service |
| `openclaw nodes list` | List paired nodes |
| `openclaw nodes approve/reject` | Approve/reject node pairing |
| `openclaw nodes invoke` | Invoke a node capability |
| `openclaw onboard` | Interactive Gateway onboarding |
| `openclaw pairing list` | List pending DM pairing requests |
| `openclaw pairing approve` | Approve a DM pairing code |
| `openclaw plugins list` | List installed plugins |
| `openclaw plugins install` | Install a plugin |
| `openclaw plugins update` | Update a plugin |
| `openclaw plugins enable/disable` | Enable or disable a plugin |
| `openclaw plugins uninstall` | Uninstall a plugin |
| `openclaw plugins inspect` | Deep-inspect a plugin |
| `openclaw plugins doctor` | Report plugin load errors |
| `openclaw plugins marketplace list` | List plugins from a marketplace |
| `openclaw proxy start` | Start local debug proxy |
| `openclaw proxy run` | Start proxy then run a child command |
| `openclaw proxy query` | Query captured traffic by preset |
| `openclaw proxy sessions` | List proxy capture sessions |
| `openclaw proxy purge` | Purge local proxy capture data |
| `openclaw qr` | Generate mobile pairing QR and setup code |
| `openclaw reset` | Reset local config/state |
| `openclaw sandbox explain` | Explain effective sandbox settings |
| `openclaw sandbox list` | List sandbox runtimes |
| `openclaw sandbox recreate` | Recreate sandbox runtimes |
| `openclaw secrets audit` | Scan for plaintext secrets and unresolved refs |
| `openclaw secrets configure` | Interactive secret provider setup |
| `openclaw secrets apply` | Apply a secrets migration plan |
| `openclaw secrets reload` | Reload Gateway runtime secret snapshot |
| `openclaw security audit` | Security audit with optional fixes |
| `openclaw sessions` | List conversation sessions |
| `openclaw sessions cleanup` | Run session maintenance |
| `openclaw setup` | Initialize config and workspace |
| `openclaw skills search` | Search ClawHub for skills |
| `openclaw skills install` | Install a skill from ClawHub |
| `openclaw skills update` | Update installed skills |
| `openclaw skills list` | List local skills |
| `openclaw skills info` | Show skill details |
| `openclaw skills check` | Check skill eligibility |
| `openclaw status` | Diagnostics for channels + sessions |
| `openclaw system event` | Enqueue a system event |
| `openclaw system heartbeat` | Control/query heartbeat |
| `openclaw system presence` | List system presence entries |
| `openclaw tasks list` | List background tasks |
| `openclaw tasks show` | Show one task |
| `openclaw tasks cancel` | Cancel a running task |
| `openclaw tasks notify` | Change task notification policy |
| `openclaw tasks audit` | Surface inconsistent/stale task records |
| `openclaw tasks maintenance` | Apply task cleanup/pruning |
| `openclaw tasks flow` | Inspect Task Flow state |
| `openclaw tui` | Open terminal UI connected to Gateway |
| `openclaw chat` | Alias for `openclaw tui --local` |
| `openclaw terminal` | Alias for `openclaw tui --local` |
| `openclaw uninstall` | Uninstall Gateway service + local data |
| `openclaw update` | Update OpenClaw |
| `openclaw update status` | Show update channel and availability |
| `openclaw update wizard` | Interactive update channel wizard |
| `openclaw voicecall` | Voice call plugin commands (if installed) |
| `openclaw webhooks gmail setup` | Configure Gmail Pub/Sub webhook |
| `openclaw webhooks gmail run` | Run Gmail watch + auto-renew loop |
| `openclaw wiki status` | Wiki vault status |
| `openclaw wiki search` | Search wiki content |
| `openclaw wiki get` | Read a wiki page |
| `openclaw wiki apply` | Apply wiki mutations |
| `openclaw wiki compile` | Rebuild wiki indexes and digests |
| `openclaw wiki lint` | Lint wiki vault |
| `openclaw wiki ingest` | Import content into wiki |
| `openclaw wiki bridge import` | Import from memory plugin (bridge mode) |
| `openclaw wiki obsidian` | Obsidian integration helpers |
