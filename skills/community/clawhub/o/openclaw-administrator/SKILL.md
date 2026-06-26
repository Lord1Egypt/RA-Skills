---
name: openclaw-administrator
description: Administration guide for the OpenClaw CLI. Use this skill whenever the user asks how to run, configure, or troubleshoot any openclaw command or concept, including: gateway and daemon lifecycle, setup and onboarding (interactive and headless/VPS), multi-agent setup and routing bindings, sub-agent spawning and delegation, workspace and bootstrap file management (AGENTS.md, SOUL.md, IDENTITY.md, USER.md, TOOLS.md), adding and configuring AI model providers, setting primary and fallback models, per-agent model overrides, the model allowlist, local models (Ollama/vLLM/LM Studio), custom providers via models.providers, the OpenAI-compatible HTTP endpoint (Open WebUI, LobeChat, LibreChat integration), channel login and connectivity, messaging, memory and wiki, plugins and skills, MCP servers, cron, tasks, flows, sandbox, browser automation, nodes, security audits, backups, and diagnostics. Also use for global flags (--dev, --profile, --container), command family routing, and any question about how openclaw subcommands work.
---

### 🛡️ EMERGENCY SAFETY PROTOCOL
- **NO OVERWRITES:** Never use `cat`, redirection (>), or raw file writes to `openclaw.json`. Use a validated JSON utility script that loads-modifies-saves.
- **SCHEMA VALIDITY:** Before adding new keys (e.g., `mcp`, `tools`), verify against official schema. Never guess keys.
- **PRE-BOUNCE VERIFICATION:** 
    1. Validate JSON syntax (`python -m json.tool`).
    2. Run `openclaw doctor`.
    3. If any errors, **ABORT** the bounce.
- **BACKUP INTEGRITY:** Maintain a rotating history of up to 3 validated backups (`openclaw.json.bak.1` to `.bak.3`). After a verified successful bounce, prune any backups older than 24 hours and maintain the most recent 3 verified snapshots.
- **SECRET HYGIENE:** Never write credential-like patterns (`PAT`, `TOKEN`, `KEY`) into any workspace file. Before removing any existing configuration that contains keys/credentials, ensure they are secured in the environment (`~/.openclaw/credentials/.env`) first.
- **EXPLICIT AUTHORIZATION:** I must never make changes to the `openclaw.json` or system configuration without *first* proposing the change, explaining the "Why," and obtaining explicit user permission.
- **EXTERNAL SKILL AUDIT:** Never install a skill from ClawHub or any external repository without *first* inspecting the source code. Look specifically for:
    - Exfiltration of data/tokens to unknown URLs.
    - Malicious/damaging system commands (e.g., recursive deletion, system modifications).
    - Hardcoded or suspicious credential usage.
    Only proceed with installation once the source has been audited as benign.


## Execution Workflow

1. **Clarify the target state.** Ask what should change and what must stay untouched.
2. **Select runtime scope first.** Default profile unless isolation is explicitly needed:
   - `openclaw --dev ...` → isolated dev state under `~/.openclaw-dev`, gateway port `19001`.
   - `openclaw --profile <n> ...` → isolated state under `~/.openclaw-<n>`.
   - `openclaw --container <n> ...` → target a named container for execution.
3. **Route to the right command family.** Use `references/command-map.md` for quick routing.
4. **Expand subcommands before risky operations.** Run `openclaw <family> --help` for starred families; confirm flags before executing.
5. **Prefer machine-readable output for automation.** Use `--json` where available; parse and verify.
6. **Verify outcomes explicitly.** Check with `openclaw status`, `openclaw health`, `openclaw doctor`, or command-specific follow-up.

## Safety Rules

- Require explicit user confirmation before `reset`, `uninstall`, destructive `--force` flows, or operations that remove stored provider keys.
- Prefer non-destructive diagnostics first: `status`, `health`, `doctor`, `logs`, `security audit`.
- Keep profile scope consistent across a workflow — never mix `--dev` and default in the same sequence.
- For gateway issues, diagnose before restart unless restart is explicitly requested.
- Keep the OpenAI HTTP endpoint on loopback/tailnet only — never expose to the public internet.

## Triage Sequence

For any "OpenClaw not working" incident:

1. `openclaw status`
2. `openclaw health`
3. `openclaw doctor`
4. `openclaw security audit` (if config or provider connection settings may be misconfigured)
5. `openclaw backup verify <archive>` (if data integrity is suspected)
6. Check `openclaw gateway ...`, `openclaw channels ...`, or `openclaw nodes ...` based on where failure appears.
7. Escalate to targeted commands in `references/command-map.md`.

---

## Architecture Overview

OpenClaw runs as a **single Gateway** (WebSocket, default `127.0.0.1:18789`) that:
- Owns all messaging surfaces (WhatsApp/Telegram/Discord/Slack/Signal/iMessage/etc.)
- Hosts one or many **agents**, each with isolated workspace + auth + session store
- Exposes a **typed WS API** for CLI/app/automation clients
- Optionally serves an **OpenAI-compatible HTTP surface** at the same port

Clients (CLI, macOS app, web UI) connect over WebSocket. Nodes (macOS/iOS/Android/headless) also connect with `role: node`. The canvas UI is served at `/__openclaw__/canvas/`.

---

## Workspace and Bootstrap Files

Each agent has a **workspace** directory (`~/.openclaw/workspace` by default) containing markdown files the agent reads on boot:

| File | Purpose |
|---|---|
| `AGENTS.md` | Core instructions, memory, tool policy |
| `SOUL.md` | Persona, tone, boundaries |
| `IDENTITY.md` | Name, emoji, theme, avatar |
| `USER.md` | Who the user is; preferences |
| `TOOLS.md` | Tool usage notes and policies |
| `HEARTBEAT.md` | Periodic check-in template |
| `BOOT.md` | One-time boot ritual (delete after) |
| `BOOTSTRAP.md` | Startup sequence instructions |
| `MEMORY.md` + `memory/*.md` | Persistent memory store |

- Missing files get a placeholder marker injected at session start; execution continues.
- Size limits: `bootstrapMaxChars` (default 12 000 chars per file), `bootstrapTotalMaxChars` (default 60 000 total).
- `openclaw setup --workspace <path>` recreates any missing defaults without overwriting existing ones.
- Keep the workspace in a **private git repo** for backup and recovery. Never commit `~/.openclaw/` state dirs.
- If `~/openclaw/` (old path) exists alongside `~/.openclaw/workspace`, keep only one active workspace to avoid auth/session drift.

---

## Agent System

### Single-Agent Mode (default)

Out of the box: one agent, `agentId = main`, sessions keyed `agent:main:<mainKey>`.

### Multi-Agent Setup

Each agent is a fully isolated brain:
- Own workspace (`agents.defaults.workspace` or per-agent override)
- Own `agentDir` (`~/.openclaw/agents/<agentId>/agent`) — holds `auth-profiles.json`, model registry, per-agent config
- Own session store (`~/.openclaw/agents/<agentId>/sessions`)
- **Never reuse `agentDir` across agents** — causes auth/session collisions.

**Creating a new agent:**
```bash
openclaw agents add coding
openclaw agents add work --workspace ~/.openclaw/workspace-work --non-interactive
```

**Identity setup:**
```bash
openclaw agents set-identity --agent main --name "OpenClaw" --emoji "🦞" --avatar avatars/oc.png
openclaw agents set-identity --workspace ~/.openclaw/workspace --from-identity   # reads IDENTITY.md
```

**Listing and verifying:**
```bash
openclaw agents list
openclaw agents list --bindings
openclaw agents bindings --agent work
```

### Routing Bindings

Bindings route inbound messages to the correct agent. **Most-specific match wins** (priority order):

1. `peer` (exact DM/group id)
2. `parentPeer` (thread inheritance)
3. `guildId + roles` (Discord role routing)
4. `guildId` (Discord server)
5. `teamId` (Slack workspace)
6. Explicit `accountId` for a channel
7. `accountId: "*"` (channel-wide fallback, all accounts)
8. Default agent (`agents.list[].default`, else first entry, else `main`)

**Managing bindings:**
```bash
openclaw agents bind --agent work --bind telegram:ops --bind discord:guild-a
openclaw agents unbind --agent work --bind telegram:ops
openclaw agents unbind --agent work --all
```

Omitting `--agent` targets the current default. A channel-only binding (no `accountId`) is auto-upgraded to account-scoped when you later add an explicit accountId for the same channel+agent.

**Config example (WhatsApp DM split):**
```json
{
  "agents": {
    "list": [
      { "id": "home", "default": true, "workspace": "~/.openclaw/workspace-home" },
      { "id": "work", "workspace": "~/.openclaw/workspace-work" }
    ]
  },
  "bindings": [
    { "agentId": "home", "match": { "channel": "whatsapp", "accountId": "personal" } },
    { "agentId": "work", "match": { "channel": "whatsapp", "accountId": "biz" } }
  ]
}
```

See `references/multi-agent-recipes.md` for full Discord, Telegram, and WhatsApp examples.

### Sub-Agents

Sub-agents are background agent runs spawned by the main agent to handle tasks in parallel. They run in their own isolated session (`agent:<agentId>:subagent:<uuid>`), receive only the instructions given to them (not full conversation history), and announce results back to the requester channel when done.

**Key characteristics:**
- Depth limit: currently flat (sub-agents cannot spawn their own sub-agents; this restriction is expected to be lifted in a future release)
- Restricted tool policies relative to the parent
- Auto-announce on completion (direct delivery first, falls back to queue routing, then exponential backoff)
- Tracked as background tasks; inspect/control via slash commands

**Slash command control:**
```
/subagents          # list all background sub-agent runs
/subagents spawn <agentId> <task> [--model <m>] [--thinking <level>]
/focus <target>     # bind current thread to a sub-agent session
/unfocus            # detach thread binding
/session idle       # inspect/update inactivity auto-unfocus
/session max-age    # control hard session age cap
```

**When to use sub-agents vs sessions_send:**
- Sub-agent (`sessions_spawn`): need the result now, in this conversation; parallel fan-out.
- `sessions_send`: fire-and-forget delegation; the other agent works independently and responds later.

**Allowlist config (to let sub-agents target named agents):**
```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "subagents": {
          "allowAgents": ["coding", "research"]
        }
      }
    ]
  }
}
```

---

## Running an Agent Turn

```bash
# Run via gateway (default)
openclaw agent --to +15555550123 --message "Status update" --deliver
openclaw agent --agent ops --message "Summarize logs" --thinking medium
openclaw agent --session-id 1234 --message "Summarize inbox" --json

# Run embedded (local, no gateway)
openclaw agent --agent ops --message "Run locally" --local

# Deliver to a different channel/account
openclaw agent --agent ops --message "Generate report" \
  --deliver --reply-channel slack --reply-to "#reports"
```

Key flags: `--thinking <off|minimal|low|medium|high|xhigh>`, `--verbose <on|off>`, `--timeout <seconds>`.

Gateway mode falls back to embedded when the gateway request fails; `--local` forces embedded up front.

---

## OpenAI-Compatible HTTP API

The Gateway can serve an OpenAI-compatible HTTP surface at the same port as WebSocket. **Disabled by default.**

**Enable in `~/.openclaw/openclaw.json`:**
```json
{
  "gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": { "enabled": true }
      }
    }
  }
}
```

**Endpoints (when enabled):**
- `POST /v1/chat/completions`
- `GET /v1/models` / `GET /v1/models/{id}`
- `POST /v1/embeddings`
- `POST /v1/responses`

**Model field = agent target:**
- `"openclaw"` or `"openclaw/default"` → configured default agent
- `"openclaw/<agentId>"` → specific agent (e.g. `"openclaw/research"`)
- Legacy aliases: `"openclaw:<agentId>"`, `"agent:<agentId>"`

**Optional request headers:**
- `x-openclaw-model: <provider/model>` — override backend model for the agent
- `x-openclaw-agent-id: <agentId>` — compatibility agent override
- `x-openclaw-session-key: <key>` — control session routing
- `x-openclaw-message-channel: <channel>` — set synthetic ingress channel context

**Session behavior:** stateless per request by default. If the request includes an OpenAI `user` string, a stable session key is derived from it so repeated calls share the same agent session.

**Note:** OpenClaw's gateway token is what any connected client uses to authenticate. Keep this endpoint on loopback or a private network (tailnet/VPN) — don't expose it directly to the public internet.

**Examples:**
```bash
# Non-streaming
curl -sS http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"model":"openclaw/default","messages":[{"role":"user","content":"hi"}]}'

# Streaming with backend model override
curl -N http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-model: openai/gpt-4o' \
  -d '{"model":"openclaw/research","stream":true,"messages":[{"role":"user","content":"hi"}]}'

# List agent targets
curl -sS http://127.0.0.1:18789/v1/models \
  -H 'Authorization: Bearer YOUR_TOKEN'

# Embeddings
curl -sS http://127.0.0.1:18789/v1/embeddings \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-model: openai/text-embedding-3-small' \
  -d '{"model":"openclaw/default","input":["alpha","beta"]}'
```

**Open WebUI quick setup:**
- Base URL: `http://127.0.0.1:18789/v1` (Docker on macOS: `http://host.docker.internal:18789/v1`)
- API key: your gateway bearer token
- Model: `openclaw/default`

---

## Storing provider keys outside the config file (SecretRefs)

OpenClaw supports referencing provider keys via environment variables, files, or exec commands instead of writing plaintext values into `openclaw.json`. This is an OpenClaw configuration feature — the skill just explains how to set it up.

| Reference type | Syntax | Example |
|---|---|---|
| Env variable | `secretref-env:VAR_NAME` | `secretref-env:ANTHROPIC_API_KEY` |
| File path | `secretref-file:/path/to/file` | `secretref-file:~/.secrets/openai_key` |
| Exec command | `secretref-exec:command` | `secretref-exec:op read op://vault/item/field` |

**Set a reference via CLI:**
```bash
openclaw config set providers.anthropic.key \
  --ref-provider env --ref-source ANTHROPIC_API_KEY

openclaw secrets configure       # interactive setup wizard
openclaw secrets reload          # reload without gateway restart
openclaw secrets audit           # check all references resolve correctly
openclaw secrets audit --check   # non-zero exit on failures (CI use)
```

**Use ref mode during non-interactive onboard:**
```bash
openclaw onboard --non-interactive \
  --auth-choice anthropic-api-key \
  --secret-input-mode ref \
  --anthropic-api-key secretref-env:ANTHROPIC_API_KEY
```

---

## Setup and Onboarding

**Interactive (recommended for first-time):**
```bash
openclaw onboard
```

**Non-interactive (VPS/headless):**
```bash
openclaw onboard \
  --non-interactive \
  --auth-choice anthropic-api-key \
  --anthropic-api-key <key> \
  --gateway-bind loopback \
  --install-daemon \
  --daemon-runtime node \
  --node-manager pnpm \
  --skip-channels \
  --skip-search
```

Key `--auth-choice` values: `anthropic-api-key`, `openai-api-key`, `openrouter-api-key`, `gemini-api-key`, `github-copilot`, `chutes`, `deepseek-api-key`, `custom-api-key`, `skip`.

Key gateway bind modes: `loopback` (default), `lan`, `tailnet`, `auto`.

For Tailscale: `--tailscale <off|serve|funnel>`.
For remote gateway: `--mode remote --remote-url <url> --remote-token <token>`.

---

## Models and Providers

**Read `references/models-and-providers.md` for the full reference.** It covers: model selection order, primary/fallback config, per-agent overrides, the model allowlist, custom providers, local models (Ollama/vLLM/LM Studio), multi-key rotation, how failover and cooldowns work, and sub-agent model config.

**Quick orientation:**

Model refs use `provider/model` format: `anthropic/claude-opus-4-6`, `openai/gpt-5.4`, `ollama/llama3.3`.

```bash
# Essential commands
openclaw models list                            # see configured models
openclaw models status                          # primary, fallbacks, auth overview
openclaw models set anthropic/claude-opus-4-6  # set primary model
openclaw models set-image openai/gpt-image-1   # set image model
openclaw models fallbacks add openrouter/auto   # add a fallback
openclaw models aliases add Opus anthropic/claude-opus-4-6
openclaw models auth login                      # add/re-auth a provider
openclaw models auth login-github-copilot       # GitHub Copilot device login
openclaw models scan                            # find free models on OpenRouter
```

**Config: primary + fallback chain:**
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-6",
        "fallbacks": [
          "openrouter/anthropic/claude-opus-4-6",
          "openai/gpt-5.4"
        ]
      }
    }
  }
}
```

**Config: add a custom/third-party provider** (any OpenAI-compatible API):
```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "my-provider": {
        "baseUrl": "https://api.example.com/v1",
        "apiKey": "${MY_PROVIDER_KEY}",
        "api": "openai-completions",
        "models": [
          { "id": "my-model", "name": "My Model" }
        ]
      }
    }
  }
}
```

Use `api: "anthropic-messages"` for Anthropic-compatible endpoints. After adding a provider: `openclaw config validate`, `openclaw models list --provider my-provider`, `openclaw gateway restart`.

**Per-agent model** (each agent can use a different model):
```json
{
  "agents": {
    "list": [
      { "id": "main", "model": "anthropic/claude-opus-4-6" },
      { "id": "fast", "model": "anthropic/claude-haiku-4-5" }
    ]
  }
}
```

For built-in providers (Anthropic, OpenAI, Google, OpenRouter, GitHub Copilot, Mistral, xAI, DeepSeek, Ollama, and 20+ more) and their `--auth-choice` values, see `references/models-and-providers.md`.

---

## Inference CLI (`infer` / `capability`)

Direct inference without a full agent run:

```bash
openclaw infer list                                    # list capabilities
openclaw infer model run --model anthropic/claude-sonnet-4-6 --prompt "hi"
openclaw infer image generate --prompt "a lobster in space"
openclaw infer image describe path/to/image.jpg
openclaw infer audio transcribe recording.mp3
openclaw infer tts convert --text "Hello" --voice nova
openclaw infer web search "latest OpenClaw release"
openclaw infer web fetch https://example.com
openclaw infer embedding create --input "embed this text"
```

---

## Channels

```bash
openclaw channels list
openclaw channels status --probe            # live per-account probe
openclaw channels add --channel telegram --account alerts --token $TOKEN
openclaw channels add --channel discord --account work --token $DISCORD_TOKEN
openclaw channels remove --channel discord --account work --delete
openclaw channels login --channel whatsapp --account personal --verbose
openclaw channels logout --channel whatsapp --account personal
openclaw channels capabilities --channel telegram --account alerts
openclaw channels logs --channel whatsapp --lines 200
```

Supported channels: `whatsapp`, `telegram`, `discord`, `googlechat`, `slack`, `signal`, `imessage`, `msteams`, `mattermost` (plugin), and many more via plugins.

DM security policies: `dmPolicy: "pairing"` (unknown senders get a code), `dmPolicy: "allowlist"` (explicit list only), `dmPolicy: "open"`.

---

## Resources

Read the appropriate reference file before answering deep questions in these areas:

| Reference | When to read it |
|---|---|
| `references/command-map.md` | Full command tree, routing quick-map, common recipes, caution commands |
| `references/models-and-providers.md` | Adding providers, fallback chains, custom config, local models, auth rotation, failover |
| `references/multi-agent-recipes.md` | Annotated multi-agent JSON configs (WhatsApp, Discord, Telegram, channel split) |
| `references/openai-http-api.md` | Enabling the HTTP endpoint, model targeting, headers, Open WebUI setup |

Live docs: `openclaw docs [query]` or `https://docs.openclaw.ai`
