---
name: openclaw-admin
version: 1.2.0
description: Use when installing, updating, diagnosing, configuring, fixing, tuning, or setting up anything in OpenClaw — gateway not responding, channel silent, model failover issues, auth errors, agent routing problems, config validation failures, plugin drift after update, or any operational task involving openclaw.json, the gateway, agents, channels, or the openclaw CLI.
---

# OpenClaw Admin

Operate, diagnose, configure, and fix OpenClaw installations. You have direct filesystem access — use it to read config, search docs, and make safe edits.

**Source:** https://github.com/rendrag-git/openclaw-admin-skill — if the installed copy looks materially out of date compared to the repo (missing sections, older patterns, stale frontmatter `version`), flag it to the user. Do not auto-update.

## Agent Context (Read First)

Identify your execution context before acting — the safe path differs:

**External agent (Claude Code, Codex CLI, shell user):**
- Use `openclaw` CLI commands directly. You survive `gateway restart` / `stop` / service reinstall — the gateway dying does not kill you.
- Standard diagnostic ladder below applies as written.

**OpenClaw agent running inside the gateway (you were dispatched via ACP, a channel, or cron):**
- Prefer native gateway tools when available: `gateway config.get`, `gateway config.patch`, `gateway config.schema.lookup`, `cron`, `message`. These don't leak secrets into your context and don't require shelling out.
- **You die with your gateway.** Before triggering `gateway restart`, `gateway stop`, or any service reinstall, schedule a cron wake event for after the restart so you can resume verification. Otherwise the conversation ends mid-repair.
- Treat shell-out paths as a fallback for things native tools cannot do; never use shell to read secrets the native API would never have surfaced.
- If you are uncertain whether you are in-gateway, check whether `context.gateway` / `context.cron` (or equivalent native APIs) are available before assuming external.

## Local Install Profile

Before non-trivial OpenClaw work, read `local-install.md` in this skill directory. That file is the only intended local customization point for host-specific install facts.

- If `local-install.md` is missing or still says `Status: uninitialized template`, build it first from read-only discovery commands.
- If live discovery disagrees with `local-install.md`, treat the file as stale, verify current state, and update it with non-secret facts before relying on it.
- Update `local-install.md` whenever the user changes install type, host, profile, service manager, config path, gateway port, package source, plugin roots, rescue gateway, or secondary instance layout.
- Update `local-install.md` whenever the OpenClaw version changes; package installs refresh the bundled docs snapshot, and refreshing the live docs cache is useful when you want current published docs indexed locally.
- Keep `SKILL.md` generic. Do not add user-specific hostnames, ports, profiles, or service names here.
- Never record secrets, tokens, env-file contents, session bodies, agent workspace contents, or private conversation text in `local-install.md`.

## Scope & Safety

This skill operates **locally only** on the user's OpenClaw installation. Before acting, observe these rails:

- **Never open `~/.openclaw/secrets.json` or `~/.openclaw/.env`.** Reference them by path when explaining config, but do not read their contents into the conversation, tool output, logs, or any external destination. If a diagnostic genuinely requires a secret value, ask the user to paste the specific field.
- **Never transmit config, env, secrets, session data, or agent workspace contents to any external service** (web fetches, paste sites, third-party APIs, remote agents). Local commands and user-approved doc lookups only.
- **Require explicit user confirmation before any of:**
  - writing to `~/.openclaw/openclaw.json` beyond a single validated `openclaw config set`
  - `openclaw gateway restart` / `stop` / service reinstall
  - rotating, deleting, or overwriting tokens, OAuth profiles, or plugin credentials
  - deleting agents, sessions, plugins, or cron jobs
  - any `rm`, `mv`, or destructive git/systemd action touching OpenClaw state
- **Back up before editing.** Use the Safe Config Editing Workflow below for any `openclaw.json` change — never batch-write the whole file.
- **Read-only investigation is fine without asking** (status commands, log tailing, config validation, grepping docs).
- **Agent sessions and workspaces may contain user conversations, prompts, and PII.** Listing them (names, timestamps, sizes, file paths) is fine without asking. Before reading the *contents* of any file under `~/.openclaw/agents/<id>/sessions/` or an agent workspace, ask the user first — explain what you're looking for and why so they can approve, narrow the scope, or point you at the right session (they may not know which one without your help). Never quote or summarize session bodies in external fetches, cross-agent messages, or any destination outside this conversation, even after approval.

## Key Paths

These are generic defaults. Prefer `local-install.md` when it has been initialized and verified for the current host.

| What | Path |
|------|------|
| **Config** | `~/.openclaw/openclaw.json` (JSON5 — comments + trailing commas OK) |
| **Env vars** | `~/.openclaw/.env` — **do not open; reference by path only** (see Scope & Safety) |
| **Secrets** | `~/.openclaw/secrets.json` — **do not open; reference by path only** (see Scope & Safety) |
| **Agent workspaces** | `~/.openclaw/agents/<agentId>/` |
| **Sessions** | `~/.openclaw/agents/<agentId>/sessions/` |
| **Extensions** | `~/.openclaw/extensions/` (+ paths in `plugins.load.paths`) |
| **Local docs (package snapshot)** | `<npm-prefix>/lib/node_modules/openclaw/docs/` — package install/update refreshes this bundled docs snapshot. It is broad but may omit generated/published artifacts such as API specs. |
| **Docs cache (downloaded)** | Recommended optional live published-docs cache. Default: `${XDG_CACHE_HOME:-~/.cache}/openclaw-admin/openclaw-docs/current/`, populated from `https://docs.openclaw.ai/llms.txt`. |
| **CLI binary** | `<npm-prefix>/bin/openclaw` (find with `which openclaw`) |
| **Managed skills** | `<npm-prefix>/lib/node_modules/openclaw/skills/` |
| **Hooks** | `~/.openclaw/hooks/` |
| **Custom scripts** | `~/.openclaw/bin/` |

## Diagnostic Ladder

Always start by checking the installed version so you know which docs/behavior apply:

```bash
openclaw --version                 # record this — docs and flags drift between builds
```

Then run these in order when something is broken:

```bash
openclaw status                    # channel health + recent errors
openclaw gateway status            # runtime state + RPC probe
openclaw logs --follow             # real-time log stream
openclaw doctor                    # config validation + guided repairs
openclaw channels status --probe   # per-channel connection check
```

**Healthy signals:** gateway status shows `Runtime: running` + `RPC probe: ok`. Doctor reports no blocking issues. Channels show connected/ready.

**Silent failures** (no errors in logs) almost always mean an allowlist or policy is blocking. Surface dropped messages with:
```bash
openclaw config set logging.level debug   # or trace for maximum detail
openclaw logs --follow                     # then reproduce the issue
```

## Install / Update Runbook

Use this path when OpenClaw is being installed, updated, or acting strange after an update. The reusable rule is to prove which layer is broken before changing state.

### 1. Identify the install shape

Do not assume the service manager or package layout. First determine:

- Whether `local-install.md` already captures the current install shape
- Host type: local machine, VPS, Docker/container, LXC/Incus, system package, or manual process
- Install type: npm global, Homebrew/package manager, source checkout, release-managed symlink, container image, or bundled app
- Service manager: systemd, launchd, Docker/Compose, supervisor, tmux/screen, cron/autopilot, or unmanaged foreground process
- Active config/profile: default profile, named profile, user-specific home, container home, or service account home

Useful read-only probes:

```bash
which openclaw
openclaw --version
openclaw config file
openclaw gateway status
openclaw status --deep
```

### 2. Verify service reality from multiple angles

Do not trust only one signal. Compare the service manager, live process, listening port, health endpoint, and logs. Common post-update failures include a service unit that exists but is not loaded, a detached old process still serving traffic, and a restarted service reading a different environment than the shell.

Use whichever checks match the install:

```bash
openclaw gateway status
openclaw health
openclaw logs
ps -ef | rg openclaw
ss -ltnp | rg '18789|19001|openclaw'
```

For systemd, launchd, Docker, or container-managed installs, inspect the native manager state as well. Keep commands read-only until you know which process is actually serving the gateway.

### 3. Verify docs sources

OpenClaw package installs include a bundled docs snapshot under the package root. Package update refreshes that directory as part of replacing the package; do not store manual edits there because update can replace them.

After install/update, record the shipped docs path and version in `local-install.md`:

```bash
openclaw --version
npm root -g
find "$(npm root -g)/openclaw/docs" -maxdepth 2 -type f | sed -n '1,40p'
```

Refresh the live docs cache when you want current published docs, generated artifacts missing from npm, or an offline grep-able copy of `https://docs.openclaw.ai/llms.txt`. It is not required for routine installed-version lookup, but it is a useful companion after each OpenClaw version update.

**Do not auto-refresh mid-incident.** When the gateway is down, a channel is silent, or config is broken, the refresh (hundreds of pages, time, tokens) competes with the actual fix. If docs look stale or missing during an incident, mention it to the user and offer to refresh after the immediate problem is resolved.

```bash
./scripts/refresh-openclaw-docs.sh
```

If the script is not available in the installed skill copy, do the minimum safe manual refresh:

```bash
DOCS_CACHE="${OPENCLAW_DOCS_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/openclaw-admin/openclaw-docs}"
OC_VERSION="$(openclaw --version | awk '{print $NF}')"
mkdir -p "$DOCS_CACHE/$OC_VERSION"
curl -fsSL https://docs.openclaw.ai/llms.txt -o "$DOCS_CACHE/$OC_VERSION/llms.txt"
if [ ! -e "$DOCS_CACHE/current" ] || [ -L "$DOCS_CACHE/current" ]; then
  ln -sfn "$DOCS_CACHE/$OC_VERSION" "$DOCS_CACHE/current"
fi
```

After a live-docs refresh, record the cache path, docs source URL, OpenClaw version, and verification command in `local-install.md`. If the network is unavailable, say the live docs cache is stale or missing and use the package docs with that caveat.

### 4. Snapshot package, plugin, config, and runtime health

Before fixing, capture the real current state:

```bash
openclaw --version
openclaw doctor --non-interactive --no-workspace-suggestions
openclaw plugins doctor
openclaw plugins list --json
openclaw channels status --deep
openclaw tasks audit
```

Then inspect recent startup logs for plugin load failures, config validation errors, channel auth failures, context-engine fallback, active-memory timeouts, event-loop degradation, and task restart blocking.

### 5. Reconcile drift before reinstalling broadly

Post-update breakage often comes from inconsistent state rather than a bad binary:

- Host package version and plugin package versions are on different cohorts
- A bundled plugin is shadowed by an older global/npm plugin
- Plugin install records point at missing or older on-disk packages
- Config still names removed provider/plugin IDs or legacy keys
- A service env file changed while the interactive shell env did not
- Task ledger corruption makes a healthy gateway look degraded

Prefer the smallest consistency fix: refresh the plugin registry, update one stale plugin, correct one stale config key, or repair one task ledger issue. Avoid `plugins update --all`, plugin uninstall/reinstall, or broad config rewrites until install records, loaded plugin paths, and config intent are understood.

### 6. Verify after each narrow fix

After an update or repair, "gateway is running" is not enough. Re-run the relevant checks:

```bash
openclaw --version
openclaw doctor --non-interactive --no-workspace-suggestions
openclaw plugins doctor
openclaw status --deep
openclaw channels status --deep
openclaw tasks audit
```

When symptoms match known update regressions, read `update-failure-patterns.md` in this skill directory for concrete inspection and recovery patterns.

## Safe Config Editing Workflow

> **AI Agent Warning**: NEVER batch-write the entire `openclaw.json` file. Always read, backup, edit individual keys, and validate. Overwriting the whole file is the #1 cause of catastrophic config loss. Use `openclaw config set <key> <value>` for individual changes when possible.

1. **Read** current config: `cat ~/.openclaw/openclaw.json` or `openclaw config get <key>`
2. **Backup**: `cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-$(date +%Y%m%d-%H%M%S)`
3. **Edit** individual keys (or use `openclaw config set <key> <value>`)
4. **Validate**: `openclaw config validate`
5. **Restart only if needed**: most config hot-reloads automatically. See config-map.md for what requires `openclaw gateway restart`.

**Auto-repair**: `openclaw doctor --fix` writes a `.bak` backup and removes unknown keys.

## Finding the Right Doc

**First, always check the version** so you read docs that match the installed build:
```bash
openclaw --version
```

Package installs include a broad local docs snapshot under `<npm-prefix>/lib/node_modules/openclaw/docs/`. Install and update refresh that snapshot with the installed package. Some generated or published artifacts, such as API specs, may be absent. Use these sources in order:

1. **Local package docs** — `<npm-prefix>/lib/node_modules/openclaw/docs/`
   Best first stop for installed-version docs. Search directly:
   ```bash
   rg -n "gateway|discord|plugins|your search term" "$(npm root -g)/openclaw/docs"
   ```

2. **Downloaded live docs cache** — `${OPENCLAW_DOCS_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/openclaw-admin/openclaw-docs}/current/`
   Use this for fast local search across current published docs, when local package docs are missing the page, or when generated artifacts are needed. Refresh it before relying on it if the cache is missing or stale:
   ```bash
   rg -n "gateway|discord|plugins|your search term" "$HOME/.cache/openclaw-admin/openclaw-docs/current"
   ```
   The cache is built from `https://docs.openclaw.ai/llms.txt`, which lists the current published Markdown and API docs.

3. **Online docs** — https://docs.openclaw.ai/
   Fastest live lookup. Rendered, searchable. Use WebFetch when you need a specific page and local cache is absent or stale.

4. **Full source docs on GitHub** — https://github.com/openclaw/openclaw/tree/main/docs
   Authoritative source. Browse the tree or fetch raw markdown via WebFetch, e.g.:
   `https://raw.githubusercontent.com/openclaw/openclaw/main/docs/<path>.md`
   Cross-check the tag/commit against `openclaw --version` if behavior seems off.

5. **Offline source checkout** — clone the repo when you need git history or exact tags:
   ```bash
   git clone https://github.com/openclaw/openclaw.git ~/src/openclaw
   # then grep the local tree:
   grep -rl "your search term" ~/src/openclaw/docs/ --include="*.md"
   ```
   Pull/refresh before relying on it; check out the tag matching your installed version if you need an exact match.

Docs use consistent frontmatter — search the `read_when` and `summary` fields to find the right page:
```yaml
---
summary: "One-line description"
read_when:
  - "Contextual trigger for when to read this doc"
title: "Page Title"
---
```

**Key doc directories (in the online/GitHub/cloned tree):**
- `cli/` — command reference (one file per command)
- `gateway/` — config reference, troubleshooting, security
- `channels/` — per-platform setup guides
- `concepts/` — architecture, sessions, models, OAuth
- `providers/` — model provider setup (Anthropic, OpenAI, etc.)
- `help/` — FAQ, troubleshooting triage
- `automation/` — cron jobs, scheduling, webhooks
- `tools/` — built-in tools (web search, TTS, media, etc.)
- `nodes/` — mobile node pairing (iOS/Android)
- `plugins/` — extension development and management
- `install/` — platform-specific deployment guides
- `platforms/` — deployment platforms (VPS, Docker, etc.)
- `security/` — threat models, security audit
- `start/` — onboarding, getting started
- `web/` — Control UI, dashboard

## Common Pitfalls

### Discord

**Dual Discord allowlists**: Discord channels must be in BOTH `channels.discord.guilds.<guildId>.channels` AND `channels.discord.accounts.<account>.guilds.<guildId>.channels`. Missing either = silent message drop. This is the #1 cause of "bot doesn't respond in new channel." Non-default accounts are especially prone — their channels often get added to the account allowlist but not the top-level guild allowlist.

**DM policy defaults**: `dmPolicy: "pairing"` (default) requires sender approval via pairing code. Unrecognized senders are silently held, not rejected.

**Group mention gating**: Groups default to `requireMention: true`. Bot won't respond unless @-mentioned or text matches `mentionPatterns`.

**Bot token contention (gateway-WS layer, not channel/guild)**: A single Discord bot token can serve any number of guilds and channels over one gateway WebSocket — that part is fine. The contention is at the `wss://gateway.discord.gg/...` connection: Discord allows exactly one active non-sharded `IDENTIFY` per token. If two processes (main + rescue, main + an EC2 failover, two `openclaw` services on the same host, etc.) each open a gateway WS with the same token, Discord drops whichever is older every time the other re-IDENTIFIEs — producing a reconnect storm.

Symptoms in pmg-side logs:
- `discord client initialized as <botUserId>; awaiting gateway readiness` repeated for the same bot ID mid-session (not just at startup)
- `discord: gateway READY wait timed out after 15000ms; reconnecting with backoff (attempt N)`
- Mixed close codes piling up: `closed: 1006` (TCP drop), `closed: 1000` (lib close), `closed: 4000` (carbon "tick timeout" — heartbeat watchdog) — hundreds per day per bot under contention
- Each agent reply that needs that bot stalls ~15–30s waiting for the new WS to reach READY

Real-world example: `openclaw-failover-backup` ASG (cold-standby EC2 in us-east-1) launched on a heartbeat-stale alarm during a home-box BIOS update, pulled the same SSM-stored Discord bot tokens as the home gateway, and stayed up because `Failback=manual`. 21 hours of contention until the ASG was scaled to 0.

Fix: either ensure only one process holds a given token's gateway WS at a time (clean Failback that revokes/swaps tokens on cutover), or shard the connection deliberately (`shard:[id,total]` in IDENTIFY) — but `@buape/carbon` doesn't expose sharding currently, so distinct tokens per gateway is the practical answer. To check from AWS: `aws autoscaling describe-auto-scaling-groups` for any `*failover*` group with `DesiredCapacity>0`, and read the launch template userdata for `DISCORD_*_TOKEN` SSM param names.

**Same-bot inter-agent messaging**: The bot ignores its own messages. Agents sharing one bot token can't trigger each other — Agent A's message appears as the bot, so Agent B's binding skips it. Fix: use multiple bot accounts so inter-agent messages appear as cross-bot communication.

**Agent-to-bot mapping is NOT 1:1**: Multiple agents can share a bot token. Always verify which bot token an agent uses (`channels.discord.accounts` in config) before making changes — don't assume each agent has its own.

### Auth & Secrets

**Model failover profile pinning**: If both OAuth and API key exist for a provider, round-robin can flip profiles unexpectedly. Fix: set `auth.order[provider]` to lock profile order. Also watch for stale `usageStats` with `errorCount` poisoning profile selection.

**OAuth write-back limitation**: OAuth refresh tokens (e.g., openai-codex) CANNOT go in 1Password because SecretRef is read-only and OAuth needs write-back. These must stay as inline tokens.

**Secrets provider errors**: The `op` binary must be owned by the current user (uid match) OR its directory must be in `trustedDirs`. Use a wrapper script (e.g., `~/.openclaw/bin/op-secrets.sh`) instead of pointing directly at `/usr/bin/op`. The wrapper also needs `passEnv: ["HOME", "OP_SERVICE_ACCOUNT_TOKEN"]` for exec providers.

**1Password rate limit exhaustion**: A crash-looping gateway with exec-based secrets burns the entire 1P account-level rate limit (1000 ops, 21-hour reset). Account-level means new service account tokens don't help. Fix: deploy a local 1Password Connect server (Docker) — the wrapper script tries Connect first, falls back to CLI.

### Gateway & Config

**AI agents destroying config**: Never batch-write the entire `openclaw.json` file. Always backup first, edit individual keys, and validate after each change. This is the #1 cause of catastrophic config loss.

**Systemd crash loop**: `Restart=always` + invalid config = infinite restart loop (one case hit 18,000 restarts). Systemd can't distinguish "crashed" from "config validation failure." Consider adding `StartLimitBurst`/`StartLimitIntervalSec` to the service unit.

**Clean-exit restart landmine (`Restart=on-failure`)**: The inverse of the crash loop. OpenClaw's config-reload "full process restart (supervisor restart)" exits the gateway with status 0 and expects the service manager to start it again. A unit with `Restart=on-failure` treats the clean exit as final — the gateway goes `inactive (dead)` after an innocuous config change (a `plugins.installs.*` write was enough in two real incidents) and stays down until someone notices. Use `Restart=always` on every gateway unit, paired with `StartLimitBurst`/`StartLimitIntervalSec` to keep the crash-loop case bounded. Diagnostic tell: unit inactive, last exit status 0, no error in the final log lines.

**Impostor gateway (health 200 from the wrong process)**: A passing health endpoint proves *something* is serving the port — not that it's the right something. A leftover unit (e.g., a disabled legacy user-level service that a watchdog or stray start resurrected) can grab the gateway port, return `{"ok":true}`, and dispatch zero sessions because it runs an old install with broken plugins. One real case served for 8 days this way. When behavior and health disagree, verify the serving PID and its binary path (`ss -ltnp`, then `readlink /proc/<pid>/exe` or the unit's `MainPID`) against the unit and install you expect, and remove or mask superseded units once found.

**Binding validation errors**: A single invalid binding entry blocks the entire gateway from starting. Always run `openclaw config validate` after editing bindings. Dangling references to deleted agents are a common cause after agent cleanup.

**Carbon/WebSocket memory leak**: The `@buape/carbon` Discord library (beta) leaks WebSocket resources across reconnects. Multiple bot accounts multiply the leak rate. Mitigate with scheduled gateway restarts (every 2-4 hours). Awaiting upstream fix.

### Agents & Plugins

**Workspace is NOT a sandbox**: Agent workspaces at `~/.openclaw/agents/<id>/` are just the default cwd. Absolute paths escape. Enable `agents.defaults.sandbox.mode` for Docker isolation.

**Plugin duplicate loading**: Directory-level entries in `plugins.load.paths` cause sibling scanning, loading plugins multiple times. Be explicit about plugin paths — point to the specific plugin directory, not its parent.

**Native module bindings missing**: Extensions with native dependencies (commonly `better-sqlite3`) can install without compiled bindings — the gateway starts, but every hook touching the module fails with `Could not locate the bindings file`. Fix by running `npm rebuild <module>` in the extension directory as the owning user. **Trap**: if npm config has `ignore-scripts=true`, the rebuild prints "rebuilt dependencies successfully" while building nothing — use `npm rebuild <module> --ignore-scripts=false --foreground-scripts` and confirm the `.node` file actually exists (e.g., `node_modules/better-sqlite3/build/Release/better_sqlite3.node`) before restarting.

**Cron init-time limitation**: `context.cron` is NOT available at plugin init time — only inside gateway method handlers. This affects any plugin trying to register or query cron jobs during initialization.

**Cron requires enabled**: `cron.enabled: false` silently prevents all jobs from running.

## Plugins

OpenClaw uses a plugin system for extensions. Plugins live in `~/.openclaw/extensions/` and are configured via `plugins` in config.

```bash
openclaw plugins list                      # list installed plugins
```

Key config:
- `plugins.enabled` — master toggle
- `plugins.load.paths` — additional plugin directories (be specific — directory-level paths cause sibling scanning)
- `plugins.slots.memory` / `plugins.slots.contextEngine` — slot-based plugin selection
- `plugins.entries.<id>` — per-plugin config (`enabled`, `apiKey`, `env`, hooks)
- `plugins.deny` — plugin deny list

## ACP (Agent Communication Protocol)

ACP enables agent-to-agent communication and dispatch through the gateway. The default backend is `acpx`.

Key config:
- `acp.enabled` — global gate
- `acp.backend` — runtime backend (e.g., `"acpx"`)
- `acp.defaultAgent` — fallback target agent
- `acp.allowedAgents` — allowlist of permitted agent IDs
- `acp.stream` — streaming config (coalescing, chunking, delivery mode)
- `acp.runtime` — TTL and install settings

```bash
openclaw acp                               # ACP tools
```

## Channels Beyond Discord

The skill focuses on Discord, but OpenClaw also supports:
- **Slack** — native streaming, typing reactions, exec approvals, thread session isolation
- **BlueBubbles** — iMessage bridge integration
- **Telegram** — standard chat channel
- **WhatsApp** — web transport with reconnect config (`web` config section)
- **Google Chat** — via `googlechat` config
- **Mattermost** — via plugin
- **Signal** — encrypted messaging

Each channel has its own allowlist/policy patterns similar to Discord. Check `docs/channels/` for per-platform guides.

## Internal Hooks

Internal hooks are configured under `hooks.internal`. Each can be individually enabled/disabled via `hooks.internal.<name>.enabled`. Hook source files live in `~/.openclaw/hooks/`.

Common hooks include session-memory, agent-delegate, and command-logger. List your active hooks in config under `hooks.internal`.

## Rescue Bot (Optional)

A rescue bot can run on a separate `--profile rescue` to monitor and fix the main gateway independently. See `docs/gateway/multiple-gateways.md`.

| What | Detail |
|------|--------|
| Profile | `openclaw --profile rescue` |
| Config | `~/.openclaw-rescue/openclaw.json` |
| State | `~/.openclaw-rescue/` |
| Port | Choose a port different from main (e.g., 19789) |
| Service | Install with `openclaw --profile rescue gateway install` |

Key considerations:
- Each gateway MUST use a unique Discord bot token
- The rescue agent needs filesystem access to the main gateway's config
- Keep the rescue bot's model chain independent from main

```bash
openclaw --profile rescue status          # check rescue bot health
openclaw --profile rescue gateway status  # runtime + RPC
openclaw --profile rescue cron list       # health check + backup jobs
```

## CLI Discovery

The CLI is the source of truth for commands and flags — do not rely on a parallel catalog that will drift:

```bash
openclaw --help                    # top-level commands
openclaw <command> --help          # command-specific flags
openclaw <command> <sub> --help    # nested subcommand flags
```

Notable invocations referenced by this skill:

- `openclaw doctor --non-interactive --no-workspace-suggestions` — script-friendly doctor for update verification
- `openclaw status --deep` — extended runtime status used by the install/update runbook
- `openclaw plugins inspect <id>` — shows loaded source path, origin, version, slots
- `openclaw tasks audit` — task ledger health (run after restart/update)
- Legacy aliases: `openclaw daemon` (alias for `gateway`), `openclaw clawbot` (legacy command aliases)

## Reference Files

For config key hot-reload vs restart behavior, read `config-map.md` in this skill directory.
For local install facts, service-manager commands, and this install's notable config choices, read `local-install.md` in this skill directory.
For install/update regression examples, read `update-failure-patterns.md` in this skill directory.
