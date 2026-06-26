# OpenClaw CLI Command Map

## Table of Contents

1. [Global Flags](#global-flags)
2. [Command Routing Quick Map](#command-routing-quick-map)
3. [Full Command Tree](#full-command-tree)
4. [Command Families Reference](#command-families-reference)
5. [Common Recipes](#common-recipes)
6. [Caution Commands](#caution-commands)

---

## Global Flags

Apply before the command family:

```bash
openclaw [--dev] [--profile <n>] [--container <n>] <command>
```

| Flag | Effect |
|---|---|
| `--dev` | Isolate under `~/.openclaw-dev`; default gateway port `19001` |
| `--profile <n>` | Isolate under `~/.openclaw-<n>` |
| `--container <n>` | Target a named container for execution |
| `--no-color` | Disable ANSI colors (also `NO_COLOR=1`) |
| `--update` | Shorthand for `openclaw update` (source installs only) |
| `-V`, `--version`, `-v` | Print version and exit |
| `-h`, `--help` | Show help |

Always choose profile flags before the command family:
```bash
openclaw --dev status
openclaw --profile staging gateway start
```

---

## Command Routing Quick Map

| Goal | Command family |
|---|---|
| Setup / first-time onboarding | `onboard`, `setup`, `configure` |
| Interactive config wizard | `configure`, `config` (no subcommand) |
| Non-interactive config | `config get/set/unset/validate` |
| Diagnose health | `status`, `health`, `doctor`, `logs` |
| Run an agent turn | `agent` |
| Manage isolated agents | `agents` |
| Spawn/control sub-agents (in-session) | `/subagents` slash command |
| Operate gateway runtime | `gateway`, `daemon` |
| Operate headless node service | `node`, `nodes` |
| Manage channel auth/connectivity | `channels`, `pairing`, `devices`, `qr` |
| Send/read messages | `message` |
| Direct inference (no agent) | `infer` (alias: `capability`) |
| Model discovery/config | `models` |
| Memory management | `memory`, `wiki` |
| Background tasks | `tasks`, `flows` |
| Scheduled jobs | `cron` |
| Plugin/extension management | `plugins` |
| Skill management | `skills` |
| MCP server management | `mcp` |
| ACP tooling | `acp` |
| Security and policy | `security`, `approvals`, `sandbox` |
| Config file references (env vars, files, exec) | `secrets` |
| Backup / restore | `backup` |
| Browser automation | `browser` |
| Voice calls | `voicecall` (plugin, if installed) |
| System events / presence | `system` |
| Live docs search | `docs` |
| Control UI | `dashboard` |
| Terminal UI | `tui` |
| DNS helpers | `dns` |
| Contact/group directory | `directory` |
| Device pairing tokens | `devices` |
| Update CLI | `update` |
| Reset local data | `reset` |
| Full removal | `uninstall` |

For starred families (`*`), always inspect subcommands first:
```bash
openclaw <family> --help
```

---

## Full Command Tree

```
openclaw [--dev] [--profile <n>] [--container <n>] <command>

# Setup and Configuration
  setup            Initialize config + workspace
  onboard          Interactive/non-interactive full setup
  configure        Interactive configuration wizard
  config
    get <path>
    set <path> <value>
    set --ref-provider <p> --ref-source <s> --ref-id <id>   (SecretRef mode)
    set --batch-json '<json>'                                 (batch mode)
    set --batch-file <path>
    set --dry-run [--json] [--allow-exec]
    unset <path>
    file
    schema
    validate [--json]
  completion [-s <shell>] [-i]
  doctor [--repair] [--deep] [--yes] [--non-interactive]

# Updates and Maintenance
  update [--channel <stable|beta|dev>] [--tag <spec>] [--yes] [--dry-run]
  update status [--json]
  update wizard
  backup
    create [--output <path>] [--dry-run] [--verify] [--only-config]
    verify <archive>

# Dashboard and UI
  dashboard [--no-open]
  tui

# Security and Secrets
  security
    audit [--deep] [--fix]
  secrets
    reload [--url] [--token] [--timeout] [--expect-final] [--json]
    audit [--check] [--allow-exec] [--json]
    configure [--apply] [--yes] [--providers-only] [--agent <id>] [--json]
    apply --from <path> [--dry-run] [--allow-exec] [--json]
  approvals
    get
    set
    allowlist add|remove

# Gateway and Services
  gateway
    run                     (foreground)
    start | stop | restart
    install | uninstall
    service                 (alias for lifecycle subcommands)
    health
    status
    call <method> [params]
    usage-cost
    probe
    discover
  daemon                    (legacy alias for gateway service commands)
    status | install | uninstall | start | stop | restart
  logs [--lines <n>]

# Agents and Sessions
  agent
    -m/--message <text>
    -t/--to <dest>
    --session-id <id>
    --agent <id>
    --thinking <off|minimal|low|medium|high|xhigh>
    --verbose <on|off>
    --deliver
    --local
    --reply-channel <channel>
    --reply-to <target>
    --reply-account <id>
    --timeout <seconds>
    --json
  agents
    list [--bindings] [--json]
    add [name] [--workspace <dir>] [--model <id>] [--bind <ch[:acctId]>] [--non-interactive]
    bindings [--agent <id>] [--json]
    bind --agent <id> --bind <ch[:acctId]> (repeatable)
    unbind --agent <id> --bind <ch[:acctId]> | --all
    delete <id> [--force]
    set-identity [--agent <id>] [--from-identity] [--name] [--theme] [--emoji] [--avatar]
  sessions
    cleanup
  hooks
    list | info | check | enable | disable | install | update

# Inference
  infer (alias: capability)
    list
    inspect
    model run|list|inspect|providers
    model auth login|logout|status
    image generate|edit|describe|describe-many|providers
    audio transcribe|providers
    tts convert|voices|providers|status|enable|disable|set-provider
    video generate|describe|providers
    web search|fetch|providers
    embedding create|providers
    auth add|login|login-github-copilot|setup-token|paste-token
    auth order get|set|clear

# Models
  models
    list [--json]
    status
    set <model>
    set-image <model>
    aliases list|add|remove
    fallbacks list|add|remove|clear
    image-fallbacks list|add|remove|clear
    scan
    auth add|login|login-github-copilot|setup-token|paste-token
    auth order get|set|clear

# Memory and Knowledge
  memory
    status [--deep] [--fix]
    index
    search "<query>" | --query "<query>"
    promote
  wiki
    status | doctor | init | ingest | compile | lint | search | get | apply
    bridge import
    unsafe-local import
    obsidian status|search|open|command|daily

# Messaging and Channels
  message
    send --target <dest> --message <text> [--channel <ch>] [--json]
    broadcast
    poll
    react | reactions
    read | edit | delete | pin | unpin | pins
    permissions | search
    thread create|list|reply
    emoji list|upload
    sticker send|upload
    role info|add|remove
    channel info|list
    member info
    voice status
    event list|create
    timeout | kick | ban
  channels
    list [--no-usage] [--json]
    status [--probe] [--timeout <ms>] [--json]
    capabilities [--channel <n>] [--account <id>] [--target <dest>] [--json]
    resolve <entries...> [--channel <n>] [--kind <auto|user|group>] [--json]
    add [--channel <n>] [--account <id>] [--name <label>] [--token ...]
    remove [--channel <n>] [--account <id>] [--delete]
    login [--channel <ch>] [--account <id>] [--verbose]
    logout [--channel <ch>] [--account <id>]
    logs [--channel <name|all>] [--lines <n>] [--json]
  directory
    self
    peers list [--query <text>] [--limit <n>]
    groups list [--query <text>] [--limit <n>]
    groups members --group-id <id> [--limit <n>]
  pairing
    list | approve
  devices
    list | remove | clear | approve | reject | rotate | revoke
  qr
  clawbot
    qr                      (legacy alias)

# Tasks and Automation
  tasks
    list | audit | maintenance | show | notify | cancel
    flow list|show|cancel
  flows
  cron
    status | list | add | edit | rm | enable | disable | runs | run

# Plugins and Skills
  plugins
    list [--json]
    inspect <id>
    install <path|.tgz|npm-spec|plugin@marketplace> [--force]
    marketplace list <marketplace>
    enable <id> | disable <id>
    uninstall <id>
    update [<id>|--all]
    doctor
  skills
    search [query...] [--limit <n>] [--json]
    install <slug> [--version <v>] [--force]
    update <slug|--all>
    list [--verbose] [--eligible] [--json]
    info <n> [--json]
    check [--json]

# MCP and ACP
  mcp
    serve
    list [--json]
    show [name]
    set <name> <value>
    unset <name>
  acp
    client

# Sandbox
  sandbox
    list [--browser] [--json]
    recreate [--all] [--session <key>] [--agent <id>] [--browser] [--force]
    explain [--session <key>] [--agent <id>] [--json]

# System
  system
    event
    heartbeat last|enable|disable
    presence
  status
  health [--verbose]

# Node Host (headless)
  node
    run | status | install | uninstall | stop | restart
  nodes
    status | describe | list | pending | approve | reject | rename
    invoke | notify | push
    canvas snapshot|present|hide|navigate|eval
    canvas a2ui push|reset
    camera list|snap|clip
    screen record
    location get

# Browser
  browser
    status | start | stop | reset-profile
    tabs | open | focus | close
    profiles | create-profile | delete-profile
    screenshot | snapshot
    navigate | resize | click | type | press | hover | drag | select
    upload | fill | dialog | wait | evaluate | console | pdf

# Utility
  docs [query...]
  dns
    setup
  webhooks
    gmail setup|run
  update           (see above)
  reset
  uninstall
  voicecall        (plugin; if installed)
```

---

## Command Families Reference

### `gateway` ★

Run/inspect/manage the WebSocket Gateway.

```bash
openclaw gateway                     # start foreground (logs to stdout)
openclaw gateway start               # start as background service
openclaw gateway stop
openclaw gateway restart
openclaw gateway install             # register launchd/systemd
openclaw gateway uninstall
openclaw gateway health              # fetch health via RPC
openclaw gateway status              # show service state
openclaw gateway call <method>       # raw RPC call
openclaw gateway usage-cost          # token/cost summary
openclaw gateway probe               # live connectivity probe
openclaw gateway discover            # find other gateway instances
openclaw --dev gateway               # isolated dev gateway
openclaw gateway --port 18789
openclaw gateway --force             # forcefully clear port conflicts (CAUTION)
```

### `agent`

Execute one agent turn via the Gateway (or embedded with `--local`).

```bash
openclaw agent --to +15555550123 --message "Run summary" --deliver
openclaw agent --agent ops --message "Summarize inbox" --thinking high
openclaw agent --session-id 1234 --message "Continue" --json
openclaw agent --agent ops --message "Task" --deliver \
  --reply-channel slack --reply-to "#ops"
```

### `agents` ★

Manage isolated agents, auth, routing, workspaces.

```bash
openclaw agents list --bindings
openclaw agents add coding
openclaw agents add work --workspace ~/.openclaw/workspace-work --non-interactive
openclaw agents bind --agent work --bind telegram:work-bot
openclaw agents unbind --agent work --all
openclaw agents set-identity --agent main --from-identity
openclaw agents delete work --force
```

`main` cannot be added (reserved) or deleted.

### `channels` ★

Manage chat channel connections. Multi-account supported on most platforms.

```bash
openclaw channels list
openclaw channels status --probe
openclaw channels add --channel telegram --account alerts --name "Alerts" --token $TOKEN
openclaw channels login --channel whatsapp --account personal --verbose
openclaw channels capabilities --channel telegram
openclaw channels logs --channel all --lines 500
```

### `models` ★

Discover, configure, and authenticate model providers.

```bash
openclaw models list
openclaw models set anthropic/claude-sonnet-4-6
openclaw models fallbacks add openrouter/anthropic/claude-sonnet-4-6
openclaw models auth login
openclaw models auth login-github-copilot
openclaw models auth order set anthropic openrouter openai
openclaw models scan
```

### `infer` ★ (alias: `capability`)

Direct inference without a full agent session.

```bash
openclaw infer list
openclaw infer model run --model anthropic/claude-haiku-4-5 --prompt "Hello"
openclaw infer image generate --prompt "a lobster"
openclaw infer audio transcribe meeting.mp3
openclaw infer tts convert --text "Hello" --voice nova
openclaw infer web search "OpenClaw changelog"
openclaw infer embedding create --input "embed this"
```

### `config` ★

Non-interactive config helpers.

```bash
openclaw config get agents.defaults.model
openclaw config set agents.defaults.model anthropic/claude-sonnet-4-6
openclaw config set providers.openai.key --ref-provider env --ref-source OPENAI_API_KEY
openclaw config set --batch-file updates.json
openclaw config set --dry-run --json
openclaw config unset channels.slack.token
openclaw config file
openclaw config schema
openclaw config validate --json
```

### `onboard`

Interactive or non-interactive full setup.

```bash
# Interactive
openclaw onboard

# Non-interactive headless
openclaw onboard \
  --non-interactive \
  --auth-choice anthropic-api-key \
  --anthropic-api-key $ANTHROPIC_KEY \
  --gateway-bind loopback \
  --gateway-auth token \
  --install-daemon \
  --daemon-runtime node \
  --node-manager pnpm \
  --skip-channels \
  --skip-search

# With Tailscale
openclaw onboard --non-interactive --tailscale serve

# Custom provider
openclaw onboard --non-interactive \
  --auth-choice custom-api-key \
  --custom-base-url https://api.example.com/v1 \
  --custom-model-id my-model \
  --custom-api-key $CUSTOM_KEY \
  --custom-compatibility openai
```

`--auth-choice` values include: `anthropic-api-key`, `openai-api-key`, `openrouter-api-key`, `gemini-api-key`, `github-copilot`, `chutes`, `deepseek-api-key`, `kilocode-api-key`, `litellm-api-key`, `moonshot-api-key`, `venice-api-key`, `xai-api-key`, `mistral-api-key`, `qwen-api-key`, `volcengine-api-key`, `custom-api-key`, `skip`.

### `memory`

Vector search over workspace memory files.

```bash
openclaw memory status --deep
openclaw memory index
openclaw memory search "previous conversations about deployment"
openclaw memory promote                # rank and optionally append top recalls to MEMORY.md
```

### `wiki`

Workspace wiki management with optional Obsidian integration.

```bash
openclaw wiki init
openclaw wiki ingest
openclaw wiki compile
openclaw wiki search "authentication patterns"
openclaw wiki get "my-note-title"
openclaw wiki obsidian status
openclaw wiki obsidian daily
```

### `tasks`

Manage background task queue.

```bash
openclaw tasks list
openclaw tasks show <id>
openclaw tasks cancel <id>
openclaw tasks audit
openclaw tasks maintenance
openclaw tasks flow list
openclaw tasks flow cancel <id>
```

### `cron`

Manage scheduled agent jobs.

```bash
openclaw cron list
openclaw cron add --schedule "0 9 * * *" --message "Daily summary" --agent main
openclaw cron edit <id>
openclaw cron rm <id>
openclaw cron enable <id> | disable <id>
openclaw cron runs <id>
openclaw cron run <id>          # trigger immediately
```

### `plugins` ★

Manage extensions.

```bash
openclaw plugins list
openclaw plugins install my-plugin
openclaw plugins install @myorg/plugin@marketplace
openclaw plugins install ./local-plugin --force
openclaw plugins enable my-plugin
openclaw plugins disable my-plugin
openclaw plugins doctor
openclaw plugins marketplace list openclaw-marketplace
```

Most plugin changes require a gateway restart.

### `skills` ★

List and manage ClawHub skills.

```bash
openclaw skills search "github"
openclaw skills install my-skill-slug
openclaw skills install my-skill-slug --version 1.2.0 --force
openclaw skills update --all
openclaw skills list --verbose
openclaw skills info my-skill-slug
openclaw skills check
```

### `mcp`

Manage MCP (Model Context Protocol) servers.

```bash
openclaw mcp list
openclaw mcp show my-server
openclaw mcp set my-server someKey someValue
openclaw mcp unset my-server someKey
openclaw mcp serve          # start an MCP server on stdio
```

### `sandbox`

Manage isolated execution containers.

```bash
openclaw sandbox list
openclaw sandbox list --browser
openclaw sandbox recreate --all
openclaw sandbox recreate --agent coding
openclaw sandbox explain --agent coding
```

`recreate` removes existing runtimes so the next use re-seeds them from current config.

### `security`

Security tooling and config audits.

```bash
openclaw security audit             # audit config + state
openclaw security audit --deep      # best-effort live gateway probe
openclaw security audit --fix       # tighten safe defaults automatically
```

### `secrets`

Manage config file references — store provider keys as environment variable refs, file paths, or exec commands instead of plaintext in `openclaw.json`.

```bash
openclaw secrets audit
openclaw secrets audit --check          # non-zero exit on findings (CI use)
openclaw secrets reload                 # hot-reload without gateway restart
openclaw secrets configure              # interactive setup
openclaw secrets apply --from plan.json # apply a pre-built plan
openclaw secrets apply --from plan.json --dry-run
```

### `backup`

Create and verify local state archives.

```bash
openclaw backup create
openclaw backup create --output ~/backups/openclaw-$(date +%Y%m%d).tar.gz
openclaw backup create --verify                  # create and immediately verify
openclaw backup create --only-config             # config only, no workspace
openclaw backup verify my-backup.tar.gz
```

### `browser` ★

Manage and automate a dedicated browser instance.

```bash
openclaw browser status
openclaw browser start
openclaw browser navigate "https://example.com"
openclaw browser screenshot --output page.png
openclaw browser click --selector "#submit-btn"
openclaw browser type --selector "#search" --text "query"
openclaw browser evaluate --script "return document.title"
openclaw browser tabs
openclaw browser pdf --output page.pdf
```

### `nodes` ★

Manage gateway-owned node pairings (macOS/iOS/Android/headless).

```bash
openclaw nodes list
openclaw nodes status
openclaw nodes pending
openclaw nodes approve <nodeId>
openclaw nodes invoke <nodeId> <command>
openclaw nodes canvas snapshot <nodeId>
openclaw nodes camera snap <nodeId>
openclaw nodes location get <nodeId>
```

### `doctor`

Run health checks and quick fixes.

```bash
openclaw doctor
openclaw doctor --repair                  # attempt automatic repairs
openclaw doctor --deep                    # scan for extra gateway installs
openclaw doctor --yes --non-interactive   # headless / CI
```

### `status` and `health`

```bash
openclaw status             # channel health + recent recipients + provider usage
openclaw status --deep      # broader gateway health probes
openclaw health             # fetch health from running gateway
openclaw health --verbose   # live probe + expanded human-readable output
```

### `update`

```bash
openclaw update
openclaw update --channel beta
openclaw update --tag 2026.4.9
openclaw update --dry-run --json
openclaw update status
```

### `logs`

```bash
openclaw logs                     # tail gateway logs via RPC
openclaw logs --lines 500
```

---

## Common Recipes

### Full fresh setup (headless VPS with Anthropic)

```bash
npm install -g openclaw
openclaw onboard \
  --non-interactive \
  --auth-choice anthropic-api-key \
  --anthropic-api-key $ANTHROPIC_API_KEY \
  --gateway-bind loopback \
  --install-daemon \
  --node-manager pnpm \
  --skip-channels
openclaw doctor
openclaw status
```

### Add a second agent and bind to Telegram bot

```bash
openclaw agents add research --workspace ~/.openclaw/workspace-research
openclaw channels add --channel telegram --account research-bot --token $TG_TOKEN
openclaw agents bind --agent research --bind telegram:research-bot
openclaw gateway restart
openclaw agents list --bindings
```

### Enable Open WebUI via the HTTP API

```bash
# Edit ~/.openclaw/openclaw.json
openclaw config set gateway.http.endpoints.chatCompletions.enabled true
openclaw gateway restart
# Then in Open WebUI: base URL = http://127.0.0.1:18789/v1, model = openclaw/default
```

### Run a gateway locally with dev profile

```bash
openclaw --dev gateway --port 19001
openclaw --dev status
```

### Diagnose channel disconnection

```bash
openclaw status
openclaw channels status --probe
openclaw channels logs --channel all
openclaw doctor --repair
```

### Send a message with JSON output

```bash
openclaw message send --target +15555550123 --message "Hello" --json
openclaw message send --channel telegram --target @mychat --message "Hello"
```

### Run an agent turn and deliver reply

```bash
openclaw agent --to +15555550123 --message "Run daily summary" --deliver
```

### Set model failover chain

```bash
openclaw models set anthropic/claude-opus-4-6
openclaw models fallbacks add openrouter/anthropic/claude-opus-4-6
openclaw models fallbacks add openai/gpt-4o
openclaw models fallbacks list
```

### Non-destructive full diagnostic

```bash
openclaw status
openclaw health --verbose
openclaw doctor
openclaw security audit
openclaw channels status --probe
openclaw nodes status
```

### Backup before a risky operation

```bash
openclaw backup create --verify --output ~/backups/pre-update.tar.gz
openclaw update
openclaw doctor
```

---

## Caution Commands

Always confirm intent before running these:

| Command | Effect |
|---|---|
| `openclaw reset` | Destructive local state + config reset (CLI stays installed) |
| `openclaw uninstall` | Removes gateway service + all local data |
| `openclaw gateway --force` | Forcefully kills port conflicts |
| `openclaw sandbox recreate --all` | Destroys all sandbox runtimes |
| `openclaw agents delete <id> --force` | Moves workspace/state/sessions to Trash without prompting |
| `openclaw onboard --reset --reset-scope full` | Full wipe including workspace |

**Recommended pre-flight for any caution command:**
```bash
openclaw backup create --verify
```
