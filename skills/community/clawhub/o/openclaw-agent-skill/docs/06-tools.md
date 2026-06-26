# Agent Tools

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 31

---

<!-- SOURCE: https://docs.openclaw.ai/tools/reactions -->

# Reactions - OpenClaw

## Reaction tooling

Shared reaction semantics across channels:

*   `emoji` is required when adding a reaction.
*   `emoji=""` removes the bot’s reaction(s) when supported.
*   `remove: true` removes the specified emoji when supported (requires `emoji`).

Channel notes:

*   **Discord/Slack**: empty `emoji` removes all of the bot’s reactions on the message; `remove: true` removes just that emoji.
*   **Google Chat**: empty `emoji` removes the app’s reactions on the message; `remove: true` removes just that emoji.
*   **Telegram**: empty `emoji` removes the bot’s reactions; `remove: true` also removes reactions but still requires a non-empty `emoji` for tool validation.
*   **WhatsApp**: empty `emoji` removes the bot reaction; `remove: true` maps to empty emoji (still requires `emoji`).
*   **Zalo Personal (`zalouser`)**: requires non-empty `emoji`; `remove: true` removes that specific emoji reaction.
*   **Signal**: inbound reaction notifications emit system events when `channels.signal.reactionNotifications` is enabled.

---

<!-- SOURCE: https://docs.openclaw.ai/tools/acp-agents -->

# ACP Agents - OpenClaw

[Agent Client Protocol (ACP)](https://agentclientprotocol.com/) sessions let OpenClaw run external coding harnesses (for example Pi, Claude Code, Codex, OpenCode, and Gemini CLI) through an ACP backend plugin. If you ask OpenClaw in plain language to “run this in Codex” or “start Claude Code in a thread”, OpenClaw should route that request to the ACP runtime (not the native sub-agent runtime).

## Fast operator flow

Use this when you want a practical `/acp` runbook:

1.  Spawn a session:
    *   `/acp spawn codex --mode persistent --thread auto`
2.  Work in the bound thread (or target that session key explicitly).
3.  Check runtime state:
    *   `/acp status`
4.  Tune runtime options as needed:
    *   `/acp model <provider/model>`
    *   `/acp permissions <profile>`
    *   `/acp timeout <seconds>`
5.  Nudge an active session without replacing context:
    *   `/acp steer tighten logging and continue`
6.  Stop work:
    *   `/acp cancel` (stop current turn), or
    *   `/acp close` (close session + remove bindings)

## Quick start for humans

Examples of natural requests:

*   “Start a persistent Codex session in a thread here and keep it focused.”
*   “Run this as a one-shot Claude Code ACP session and summarize the result.”
*   “Use Gemini CLI for this task in a thread, then keep follow-ups in that same thread.”

What OpenClaw should do:

1.  Pick `runtime: "acp"`.
2.  Resolve the requested harness target (`agentId`, for example `codex`).
3.  If thread binding is requested and the current channel supports it, bind the ACP session to the thread.
4.  Route follow-up thread messages to that same ACP session until unfocused/closed/expired.

## ACP versus sub-agents

Use ACP when you want an external harness runtime. Use sub-agents when you want OpenClaw-native delegated runs.

| Area | ACP session | Sub-agent run |
| --- | --- | --- |
| Runtime | ACP backend plugin (for example acpx) | OpenClaw native sub-agent runtime |
| Session key | `agent:<agentId>:acp:<uuid>` | `agent:<agentId>:subagent:<uuid>` |
| Main commands | `/acp ...` | `/subagents ...` |
| Spawn tool | `sessions_spawn` with `runtime:"acp"` | `sessions_spawn` (default runtime) |

See also [Sub-agents](https://docs.openclaw.ai/tools/subagents).

## Thread-bound sessions (channel-agnostic)

When thread bindings are enabled for a channel adapter, ACP sessions can be bound to threads:

*   OpenClaw binds a thread to a target ACP session.
*   Follow-up messages in that thread route to the bound ACP session.
*   ACP output is delivered back to the same thread.
*   Unfocus/close/archive/idle-timeout or max-age expiry removes the binding.

Thread binding support is adapter-specific. If the active channel adapter does not support thread bindings, OpenClaw returns a clear unsupported/unavailable message. Required feature flags for thread-bound ACP:

*   `acp.enabled=true`
*   `acp.dispatch.enabled` is on by default (set `false` to pause ACP dispatch)
*   Channel-adapter ACP thread-spawn flag enabled (adapter-specific)
    *   Discord: `channels.discord.threadBindings.spawnAcpSessions=true`
    *   Telegram: `channels.telegram.threadBindings.spawnAcpSessions=true`

### Thread supporting channels

*   Any channel adapter that exposes session/thread binding capability.
*   Current built-in support:
    *   Discord threads/channels
    *   Telegram topics (forum topics in groups/supergroups and DM topics)
*   Plugin channels can add support through the same binding interface.

## Channel specific settings

For non-ephemeral workflows, configure persistent ACP bindings in top-level `bindings[]` entries.

### Binding model

*   `bindings[].type="acp"` marks a persistent ACP conversation binding.
*   `bindings[].match` identifies the target conversation:
    *   Discord channel or thread: `match.channel="discord"` + `match.peer.id="<channelOrThreadId>"`
    *   Telegram forum topic: `match.channel="telegram"` + `match.peer.id="<chatId>:topic:<topicId>"`
*   `bindings[].agentId` is the owning OpenClaw agent id.
*   Optional ACP overrides live under `bindings[].acp`:
    *   `mode` (`persistent` or `oneshot`)
    *   `label`
    *   `cwd`
    *   `backend`

### Runtime defaults per agent

Use `agents.list[].runtime` to define ACP defaults once per agent:

*   `agents.list[].runtime.type="acp"`
*   `agents.list[].runtime.acp.agent` (harness id, for example `codex` or `claude`)
*   `agents.list[].runtime.acp.backend`
*   `agents.list[].runtime.acp.mode`
*   `agents.list[].runtime.acp.cwd`

Override precedence for ACP bound sessions:

1.  `bindings[].acp.*`
2.  `agents.list[].runtime.acp.*`
3.  global ACP defaults (for example `acp.backend`)

Example:

```
{
  agents: {
    list: [
      {
        id: "codex",
        runtime: {
          type: "acp",
          acp: {
            agent: "codex",
            backend: "acpx",
            mode: "persistent",
            cwd: "/workspace/openclaw",
          },
        },
      },
      {
        id: "claude",
        runtime: {
          type: "acp",
          acp: { agent: "claude", backend: "acpx", mode: "persistent" },
        },
      },
    ],
  },
  bindings: [
    {
      type: "acp",
      agentId: "codex",
      match: {
        channel: "discord",
        accountId: "default",
        peer: { kind: "channel", id: "222222222222222222" },
      },
      acp: { label: "codex-main" },
    },
    {
      type: "acp",
      agentId: "claude",
      match: {
        channel: "telegram",
        accountId: "default",
        peer: { kind: "group", id: "-1001234567890:topic:42" },
      },
      acp: { cwd: "/workspace/repo-b" },
    },
    {
      type: "route",
      agentId: "main",
      match: { channel: "discord", accountId: "default" },
    },
    {
      type: "route",
      agentId: "main",
      match: { channel: "telegram", accountId: "default" },
    },
  ],
  channels: {
    discord: {
      guilds: {
        "111111111111111111": {
          channels: {
            "222222222222222222": { requireMention: false },
          },
        },
      },
    },
    telegram: {
      groups: {
        "-1001234567890": {
          topics: { "42": { requireMention: false } },
        },
      },
    },
  },
}
```

Behavior:

*   OpenClaw ensures the configured ACP session exists before use.
*   Messages in that channel or topic route to the configured ACP session.
*   In bound conversations, `/new` and `/reset` reset the same ACP session key in place.
*   Temporary runtime bindings (for example created by thread-focus flows) still apply where present.

## Start ACP sessions (interfaces)

### From `sessions_spawn`

Use `runtime: "acp"` to start an ACP session from an agent turn or tool call.

```
{
  "task": "Open the repo and summarize failing tests",
  "runtime": "acp",
  "agentId": "codex",
  "thread": true,
  "mode": "session"
}
```

Notes:

*   `runtime` defaults to `subagent`, so set `runtime: "acp"` explicitly for ACP sessions.
*   If `agentId` is omitted, OpenClaw uses `acp.defaultAgent` when configured.
*   `mode: "session"` requires `thread: true` to keep a persistent bound conversation.

Interface details:

*   `task` (required): initial prompt sent to the ACP session.
*   `runtime` (required for ACP): must be `"acp"`.
*   `agentId` (optional): ACP target harness id. Falls back to `acp.defaultAgent` if set.
*   `thread` (optional, default `false`): request thread binding flow where supported.
*   `mode` (optional): `run` (one-shot) or `session` (persistent).
    *   default is `run`
    *   if `thread: true` and mode omitted, OpenClaw may default to persistent behavior per runtime path
    *   `mode: "session"` requires `thread: true`
*   `cwd` (optional): requested runtime working directory (validated by backend/runtime policy).
*   `label` (optional): operator-facing label used in session/banner text.
*   `streamTo` (optional): `"parent"` streams initial ACP run progress summaries back to the requester session as system events.
    *   When available, accepted responses include `streamLogPath` pointing to a session-scoped JSONL log (`<sessionId>.acp-stream.jsonl`) you can tail for full relay history.

## Sandbox compatibility

ACP sessions currently run on the host runtime, not inside the OpenClaw sandbox. Current limitations:

*   If the requester session is sandboxed, ACP spawns are blocked for both `sessions_spawn({ runtime: "acp" })` and `/acp spawn`.
    *   Error: `Sandboxed sessions cannot spawn ACP sessions because runtime="acp" runs on the host. Use runtime="subagent" from sandboxed sessions.`
*   `sessions_spawn` with `runtime: "acp"` does not support `sandbox: "require"`.
    *   Error: `sessions_spawn sandbox="require" is unsupported for runtime="acp" because ACP sessions run outside the sandbox. Use runtime="subagent" or sandbox="inherit".`

Use `runtime: "subagent"` when you need sandbox-enforced execution.

### From `/acp` command

Use `/acp spawn` for explicit operator control from chat when needed.

```
/acp spawn codex --mode persistent --thread auto
/acp spawn codex --mode oneshot --thread off
/acp spawn codex --thread here
```

Key flags:

*   `--mode persistent|oneshot`
*   `--thread auto|here|off`
*   `--cwd <absolute-path>`
*   `--label <name>`

See [Slash Commands](https://docs.openclaw.ai/tools/slash-commands).

## Session target resolution

Most `/acp` actions accept an optional session target (`session-key`, `session-id`, or `session-label`). Resolution order:

1.  Explicit target argument (or `--session` for `/acp steer`)
    *   tries key
    *   then UUID-shaped session id
    *   then label
2.  Current thread binding (if this conversation/thread is bound to an ACP session)
3.  Current requester session fallback

If no target resolves, OpenClaw returns a clear error (`Unable to resolve session target: ...`).

## Spawn thread modes

`/acp spawn` supports `--thread auto|here|off`.

| Mode | Behavior |
| --- | --- |
| `auto` | In an active thread: bind that thread. Outside a thread: create/bind a child thread when supported. |
| `here` | Require current active thread; fail if not in one. |
| `off` | No binding. Session starts unbound. |

Notes:

*   On non-thread binding surfaces, default behavior is effectively `off`.
*   Thread-bound spawn requires channel policy support:
    *   Discord: `channels.discord.threadBindings.spawnAcpSessions=true`
    *   Telegram: `channels.telegram.threadBindings.spawnAcpSessions=true`

## ACP controls

Available command family:

*   `/acp spawn`
*   `/acp cancel`
*   `/acp steer`
*   `/acp close`
*   `/acp status`
*   `/acp set-mode`
*   `/acp set`
*   `/acp cwd`
*   `/acp permissions`
*   `/acp timeout`
*   `/acp model`
*   `/acp reset-options`
*   `/acp sessions`
*   `/acp doctor`
*   `/acp install`

`/acp status` shows the effective runtime options and, when available, both runtime-level and backend-level session identifiers. Some controls depend on backend capabilities. If a backend does not support a control, OpenClaw returns a clear unsupported-control error.

## ACP command cookbook

| Command | What it does | Example |
| --- | --- | --- |
| `/acp spawn` | Create ACP session; optional thread bind. | `/acp spawn codex --mode persistent --thread auto --cwd /repo` |
| `/acp cancel` | Cancel in-flight turn for target session. | `/acp cancel agent:codex:acp:<uuid>` |
| `/acp steer` | Send steer instruction to running session. | `/acp steer --session support inbox prioritize failing tests` |
| `/acp close` | Close session and unbind thread targets. | `/acp close` |
| `/acp status` | Show backend, mode, state, runtime options, capabilities. | `/acp status` |
| `/acp set-mode` | Set runtime mode for target session. | `/acp set-mode plan` |
| `/acp set` | Generic runtime config option write. | `/acp set model openai/gpt-5.2` |
| `/acp cwd` | Set runtime working directory override. | `/acp cwd /Users/user/Projects/repo` |
| `/acp permissions` | Set approval policy profile. | `/acp permissions strict` |
| `/acp timeout` | Set runtime timeout (seconds). | `/acp timeout 120` |
| `/acp model` | Set runtime model override. | `/acp model anthropic/claude-opus-4-5` |
| `/acp reset-options` | Remove session runtime option overrides. | `/acp reset-options` |
| `/acp sessions` | List recent ACP sessions from store. | `/acp sessions` |
| `/acp doctor` | Backend health, capabilities, actionable fixes. | `/acp doctor` |
| `/acp install` | Print deterministic install and enable steps. | `/acp install` |

## Runtime options mapping

`/acp` has convenience commands and a generic setter. Equivalent operations:

*   `/acp model <id>` maps to runtime config key `model`.
*   `/acp permissions <profile>` maps to runtime config key `approval_policy`.
*   `/acp timeout <seconds>` maps to runtime config key `timeout`.
*   `/acp cwd <path>` updates runtime cwd override directly.
*   `/acp set <key> <value>` is the generic path.
    *   Special case: `key=cwd` uses the cwd override path.
*   `/acp reset-options` clears all runtime overrides for target session.

## acpx harness support (current)

Current acpx built-in harness aliases:

*   `pi`
*   `claude`
*   `codex`
*   `opencode`
*   `gemini`
*   `kimi`

When OpenClaw uses the acpx backend, prefer these values for `agentId` unless your acpx config defines custom agent aliases. Direct acpx CLI usage can also target arbitrary adapters via `--agent <command>`, but that raw escape hatch is an acpx CLI feature (not the normal OpenClaw `agentId` path).

## Required config

Core ACP baseline:

```
{
  acp: {
    enabled: true,
    // Optional. Default is true; set false to pause ACP dispatch while keeping /acp controls.
    dispatch: { enabled: true },
    backend: "acpx",
    defaultAgent: "codex",
    allowedAgents: ["pi", "claude", "codex", "opencode", "gemini", "kimi"],
    maxConcurrentSessions: 8,
    stream: {
      coalesceIdleMs: 300,
      maxChunkChars: 1200,
    },
    runtime: {
      ttlMinutes: 120,
    },
  },
}
```

Thread binding config is channel-adapter specific. Example for Discord:

```
{
  session: {
    threadBindings: {
      enabled: true,
      idleHours: 24,
      maxAgeHours: 0,
    },
  },
  channels: {
    discord: {
      threadBindings: {
        enabled: true,
        spawnAcpSessions: true,
      },
    },
  },
}
```

If thread-bound ACP spawn does not work, verify the adapter feature flag first:

*   Discord: `channels.discord.threadBindings.spawnAcpSessions=true`

See [Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference).

## Plugin setup for acpx backend

Install and enable plugin:

```
openclaw plugins install acpx
openclaw config set plugins.entries.acpx.enabled true
```

Local workspace install during development:

```
openclaw plugins install ./extensions/acpx
```

Then verify backend health:

### acpx command and version configuration

By default, the acpx plugin (published as `@openclaw/acpx`) uses the plugin-local pinned binary:

1.  Command defaults to `extensions/acpx/node_modules/.bin/acpx`.
2.  Expected version defaults to the extension pin.
3.  Startup registers ACP backend immediately as not-ready.
4.  A background ensure job verifies `acpx --version`.
5.  If the plugin-local binary is missing or mismatched, it runs: `npm install --omit=dev --no-save acpx@<pinned>` and re-verifies.

You can override command/version in plugin config:

```
{
  "plugins": {
    "entries": {
      "acpx": {
        "enabled": true,
        "config": {
          "command": "../acpx/dist/cli.js",
          "expectedVersion": "any"
        }
      }
    }
  }
}
```

Notes:

*   `command` accepts an absolute path, relative path, or command name (`acpx`).
*   Relative paths resolve from OpenClaw workspace directory.
*   `expectedVersion: "any"` disables strict version matching.
*   When `command` points to a custom binary/path, plugin-local auto-install is disabled.
*   OpenClaw startup remains non-blocking while the backend health check runs.

See [Plugins](https://docs.openclaw.ai/tools/plugin).

## Permission configuration

ACP sessions run non-interactively — there is no TTY to approve or deny file-write and shell-exec permission prompts. The acpx plugin provides two config keys that control how permissions are handled:

### `permissionMode`

Controls which operations the harness agent can perform without prompting.

| Value | Behavior |
| --- | --- |
| `approve-all` | Auto-approve all file writes and shell commands. |
| `approve-reads` | Auto-approve reads only; writes and exec require prompts. |
| `deny-all` | Deny all permission prompts. |

### `nonInteractivePermissions`

Controls what happens when a permission prompt would be shown but no interactive TTY is available (which is always the case for ACP sessions).

| Value | Behavior |
| --- | --- |
| `fail` | Abort the session with `AcpRuntimeError`. **(default)** |
| `deny` | Silently deny the permission and continue (graceful degradation). |

### Configuration

Set via plugin config:

```
openclaw config set plugins.entries.acpx.config.permissionMode approve-all
openclaw config set plugins.entries.acpx.config.nonInteractivePermissions fail
```

Restart the gateway after changing these values.

> **Important:** OpenClaw currently defaults to `permissionMode=approve-reads` and `nonInteractivePermissions=fail`. In non-interactive ACP sessions, any write or exec that triggers a permission prompt can fail with `AcpRuntimeError: Permission prompt unavailable in non-interactive mode`. If you need to restrict permissions, set `nonInteractivePermissions` to `deny` so sessions degrade gracefully instead of crashing.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `ACP runtime backend is not configured` | Backend plugin missing or disabled. | Install and enable backend plugin, then run `/acp doctor`. |
| `ACP is disabled by policy (acp.enabled=false)` | ACP globally disabled. | Set `acp.enabled=true`. |
| `ACP dispatch is disabled by policy (acp.dispatch.enabled=false)` | Dispatch from normal thread messages disabled. | Set `acp.dispatch.enabled=true`. |
| `ACP agent "<id>" is not allowed by policy` | Agent not in allowlist. | Use allowed `agentId` or update `acp.allowedAgents`. |
| `Unable to resolve session target: ...` | Bad key/id/label token. | Run `/acp sessions`, copy exact key/label, retry. |
| `--thread here requires running /acp spawn inside an active ... thread` | `--thread here` used outside a thread context. | Move to target thread or use `--thread auto`/`off`. |
| `Only <user-id> can rebind this thread.` | Another user owns thread binding. | Rebind as owner or use a different thread. |
| `Thread bindings are unavailable for <channel>.` | Adapter lacks thread binding capability. | Use `--thread off` or move to supported adapter/channel. |
| `Sandboxed sessions cannot spawn ACP sessions ...` | ACP runtime is host-side; requester session is sandboxed. | Use `runtime="subagent"` from sandboxed sessions, or run ACP spawn from a non-sandboxed session. |
| `sessions_spawn sandbox="require" is unsupported for runtime="acp" ...` | `sandbox="require"` requested for ACP runtime. | Use `runtime="subagent"` for required sandboxing, or use ACP with `sandbox="inherit"` from a non-sandboxed session. |
| Missing ACP metadata for bound session | Stale/deleted ACP session metadata. | Recreate with `/acp spawn`, then rebind/focus thread. |
| `AcpRuntimeError: Permission prompt unavailable in non-interactive mode` | `permissionMode` blocks writes/exec in non-interactive ACP session. | Set `plugins.entries.acpx.config.permissionMode` to `approve-all` and restart gateway. See [Permission configuration](https://docs.openclaw.ai/tools/acp-agents#permission-configuration). |
| ACP session fails early with little output | Permission prompts are blocked by `permissionMode`/`nonInteractivePermissions`. | Check gateway logs for `AcpRuntimeError`. For full permissions, set `permissionMode=approve-all`; for graceful degradation, set `nonInteractivePermissions=deny`. |
| ACP session stalls indefinitely after completing work | Harness process finished but ACP session did not report completion. | Monitor with `ps aux \| grep acpx`; kill stale processes manually. |

---

<!-- SOURCE: https://docs.openclaw.ai/tools/multi-agent-sandbox-tools -->

# Multi-Agent Sandbox & Tools - OpenClaw

## Multi-Agent Sandbox & Tools Configuration

## Overview

Each agent in a multi-agent setup can now have its own:

*   **Sandbox configuration** (`agents.list[].sandbox` overrides `agents.defaults.sandbox`)
*   **Tool restrictions** (`tools.allow` / `tools.deny`, plus `agents.list[].tools`)

This allows you to run multiple agents with different security profiles:

*   Personal assistant with full access
*   Family/work agents with restricted tools
*   Public-facing agents in sandboxes

`setupCommand` belongs under `sandbox.docker` (global or per-agent) and runs once when the container is created. Auth is per-agent: each agent reads from its own `agentDir` auth store at:

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

Credentials are **not** shared between agents. Never reuse `agentDir` across agents. If you want to share creds, copy `auth-profiles.json` into the other agent’s `agentDir`. For how sandboxing behaves at runtime, see [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing). For debugging “why is this blocked?”, see [Sandbox vs Tool Policy vs Elevated](https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated) and `openclaw sandbox explain`.

* * *

## Configuration Examples

### Example 1: Personal + Restricted Family Agent

```
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "name": "Personal Assistant",
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" }
      },
      {
        "id": "family",
        "name": "Family Bot",
        "workspace": "~/.openclaw/workspace-family",
        "sandbox": {
          "mode": "all",
          "scope": "agent"
        },
        "tools": {
          "allow": ["read"],
          "deny": ["exec", "write", "edit", "apply_patch", "process", "browser"]
        }
      }
    ]
  },
  "bindings": [
    {
      "agentId": "family",
      "match": {
        "provider": "whatsapp",
        "accountId": "*",
        "peer": {
          "kind": "group",
          "id": "120363424282127706@g.us"
        }
      }
    }
  ]
}
```

**Result:**

*   `main` agent: Runs on host, full tool access
*   `family` agent: Runs in Docker (one container per agent), only `read` tool

* * *

### Example 2: Work Agent with Shared Sandbox

```
{
  "agents": {
    "list": [
      {
        "id": "personal",
        "workspace": "~/.openclaw/workspace-personal",
        "sandbox": { "mode": "off" }
      },
      {
        "id": "work",
        "workspace": "~/.openclaw/workspace-work",
        "sandbox": {
          "mode": "all",
          "scope": "shared",
          "workspaceRoot": "/tmp/work-sandboxes"
        },
        "tools": {
          "allow": ["read", "write", "apply_patch", "exec"],
          "deny": ["browser", "gateway", "discord"]
        }
      }
    ]
  }
}
```

* * *

### Example 2b: Global coding profile + messaging-only agent

```
{
  "tools": { "profile": "coding" },
  "agents": {
    "list": [
      {
        "id": "support",
        "tools": { "profile": "messaging", "allow": ["slack"] }
      }
    ]
  }
}
```

**Result:**

*   default agents get coding tools
*   `support` agent is messaging-only (+ Slack tool)

* * *

### Example 3: Different Sandbox Modes per Agent

```
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main", // Global default
        "scope": "session"
      }
    },
    "list": [
      {
        "id": "main",
        "workspace": "~/.openclaw/workspace",
        "sandbox": {
          "mode": "off" // Override: main never sandboxed
        }
      },
      {
        "id": "public",
        "workspace": "~/.openclaw/workspace-public",
        "sandbox": {
          "mode": "all", // Override: public always sandboxed
          "scope": "agent"
        },
        "tools": {
          "allow": ["read"],
          "deny": ["exec", "write", "edit", "apply_patch"]
        }
      }
    ]
  }
}
```

* * *

## Configuration Precedence

When both global (`agents.defaults.*`) and agent-specific (`agents.list[].*`) configs exist:

### Sandbox Config

Agent-specific settings override global:

```
agents.list[].sandbox.mode > agents.defaults.sandbox.mode
agents.list[].sandbox.scope > agents.defaults.sandbox.scope
agents.list[].sandbox.workspaceRoot > agents.defaults.sandbox.workspaceRoot
agents.list[].sandbox.workspaceAccess > agents.defaults.sandbox.workspaceAccess
agents.list[].sandbox.docker.* > agents.defaults.sandbox.docker.*
agents.list[].sandbox.browser.* > agents.defaults.sandbox.browser.*
agents.list[].sandbox.prune.* > agents.defaults.sandbox.prune.*
```

**Notes:**

*   `agents.list[].sandbox.{docker,browser,prune}.*` overrides `agents.defaults.sandbox.{docker,browser,prune}.*` for that agent (ignored when sandbox scope resolves to `"shared"`).

### Tool Restrictions

The filtering order is:

1.  **Tool profile** (`tools.profile` or `agents.list[].tools.profile`)
2.  **Provider tool profile** (`tools.byProvider[provider].profile` or `agents.list[].tools.byProvider[provider].profile`)
3.  **Global tool policy** (`tools.allow` / `tools.deny`)
4.  **Provider tool policy** (`tools.byProvider[provider].allow/deny`)
5.  **Agent-specific tool policy** (`agents.list[].tools.allow/deny`)
6.  **Agent provider policy** (`agents.list[].tools.byProvider[provider].allow/deny`)
7.  **Sandbox tool policy** (`tools.sandbox.tools` or `agents.list[].tools.sandbox.tools`)
8.  **Subagent tool policy** (`tools.subagents.tools`, if applicable)

Each level can further restrict tools, but cannot grant back denied tools from earlier levels. If `agents.list[].tools.sandbox.tools` is set, it replaces `tools.sandbox.tools` for that agent. If `agents.list[].tools.profile` is set, it overrides `tools.profile` for that agent. Provider tool keys accept either `provider` (e.g. `google-antigravity`) or `provider/model` (e.g. `openai/gpt-5.2`).

### Tool groups (shorthands)

Tool policies (global, agent, sandbox) support `group:*` entries that expand to multiple concrete tools:

*   `group:runtime`: `exec`, `bash`, `process`
*   `group:fs`: `read`, `write`, `edit`, `apply_patch`
*   `group:sessions`: `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
*   `group:memory`: `memory_search`, `memory_get`
*   `group:ui`: `browser`, `canvas`
*   `group:automation`: `cron`, `gateway`
*   `group:messaging`: `message`
*   `group:nodes`: `nodes`
*   `group:openclaw`: all built-in OpenClaw tools (excludes provider plugins)

### Elevated Mode

`tools.elevated` is the global baseline (sender-based allowlist). `agents.list[].tools.elevated` can further restrict elevated for specific agents (both must allow). Mitigation patterns:

*   Deny `exec` for untrusted agents (`agents.list[].tools.deny: ["exec"]`)
*   Avoid allowlisting senders that route to restricted agents
*   Disable elevated globally (`tools.elevated.enabled: false`) if you only want sandboxed execution
*   Disable elevated per agent (`agents.list[].tools.elevated.enabled: false`) for sensitive profiles

* * *

## Migration from Single Agent

**Before (single agent):**

```
{
  "agents": {
    "defaults": {
      "workspace": "~/.openclaw/workspace",
      "sandbox": {
        "mode": "non-main"
      }
    }
  },
  "tools": {
    "sandbox": {
      "tools": {
        "allow": ["read", "write", "apply_patch", "exec"],
        "deny": []
      }
    }
  }
}
```

**After (multi-agent with different profiles):**

```
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" }
      }
    ]
  }
}
```

Legacy `agent.*` configs are migrated by `openclaw doctor`; prefer `agents.defaults` + `agents.list` going forward.

* * *

### Read-only Agent

```
{
  "tools": {
    "allow": ["read"],
    "deny": ["exec", "write", "edit", "apply_patch", "process"]
  }
}
```

### Safe Execution Agent (no file modifications)

```
{
  "tools": {
    "allow": ["read", "exec", "process"],
    "deny": ["write", "edit", "apply_patch", "browser", "gateway"]
  }
}
```

### Communication-only Agent

```
{
  "tools": {
    "sessions": { "visibility": "tree" },
    "allow": ["sessions_list", "sessions_send", "sessions_history", "session_status"],
    "deny": ["exec", "write", "edit", "apply_patch", "read", "browser"]
  }
}
```

* * *

## Common Pitfall: “non-main”

`agents.defaults.sandbox.mode: "non-main"` is based on `session.mainKey` (default `"main"`), not the agent id. Group/channel sessions always get their own keys, so they are treated as non-main and will be sandboxed. If you want an agent to never sandbox, set `agents.list[].sandbox.mode: "off"`.

* * *

## Testing

After configuring multi-agent sandbox and tools:

1.  **Check agent resolution:**
    
    ```
    openclaw agents list --bindings
    ```
    
2.  **Verify sandbox containers:**
    
    ```
    docker ps --filter "name=openclaw-sbx-"
    ```
    
3.  **Test tool restrictions:**
    *   Send a message requiring restricted tools
    *   Verify the agent cannot use denied tools
4.  **Monitor logs:**
    
    ```
    tail -f "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/logs/gateway.log" | grep -E "routing|sandbox|tools"
    ```
    

* * *

## Troubleshooting

### Agent not sandboxed despite `mode: "all"`

*   Check if there’s a global `agents.defaults.sandbox.mode` that overrides it
*   Agent-specific config takes precedence, so set `agents.list[].sandbox.mode: "all"`

### Tools still available despite deny list

*   Check tool filtering order: global → agent → sandbox → subagent
*   Each level can only further restrict, not grant back
*   Verify with logs: `[tools] filtering tools for agent:${agentId}`

### Container not isolated per agent

*   Set `scope: "agent"` in agent-specific sandbox config
*   Default is `"session"` which creates one container per session

* * *

## See Also

*   [Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent)
*   [Sandbox Configuration](https://docs.openclaw.ai/gateway/configuration#agentsdefaults-sandbox)
*   [Session Management](https://docs.openclaw.ai/concepts/session)

---

<!-- SOURCE: https://docs.openclaw.ai/tools/skills -->

# Skills - OpenClaw

OpenClaw uses **[AgentSkills](https://agentskills.io/)\-compatible** skill folders to teach the agent how to use tools. Each skill is a directory containing a `SKILL.md` with YAML frontmatter and instructions. OpenClaw loads **bundled skills** plus optional local overrides, and filters them at load time based on environment, config, and binary presence.

## Locations and precedence

Skills are loaded from **three** places:

1.  **Bundled skills**: shipped with the install (npm package or OpenClaw.app)
2.  **Managed/local skills**: `~/.openclaw/skills`
3.  **Workspace skills**: `<workspace>/skills`

If a skill name conflicts, precedence is: `<workspace>/skills` (highest) → `~/.openclaw/skills` → bundled skills (lowest) Additionally, you can configure extra skill folders (lowest precedence) via `skills.load.extraDirs` in `~/.openclaw/openclaw.json`.

In **multi-agent** setups, each agent has its own workspace. That means:

*   **Per-agent skills** live in `<workspace>/skills` for that agent only.
*   **Shared skills** live in `~/.openclaw/skills` (managed/local) and are visible to **all agents** on the same machine.
*   **Shared folders** can also be added via `skills.load.extraDirs` (lowest precedence) if you want a common skills pack used by multiple agents.

If the same skill name exists in more than one place, the usual precedence applies: workspace wins, then managed/local, then bundled.

## Plugins + skills

Plugins can ship their own skills by listing `skills` directories in `openclaw.plugin.json` (paths relative to the plugin root). Plugin skills load when the plugin is enabled and participate in the normal skill precedence rules. You can gate them via `metadata.openclaw.requires.config` on the plugin’s config entry. See [Plugins](https://docs.openclaw.ai/tools/plugin) for discovery/config and [Tools](https://docs.openclaw.ai/tools) for the tool surface those skills teach.

## ClawHub (install + sync)

ClawHub is the public skills registry for OpenClaw. Browse at [https://clawhub.com](https://clawhub.com/). Use it to discover, install, update, and back up skills. Full guide: [ClawHub](https://docs.openclaw.ai/tools/clawhub). Common flows:

*   Install a skill into your workspace:
    *   `clawhub install <skill-slug>`
*   Update all installed skills:
    *   `clawhub update --all`
*   Sync (scan + publish updates):
    *   `clawhub sync --all`

By default, `clawhub` installs into `./skills` under your current working directory (or falls back to the configured OpenClaw workspace). OpenClaw picks that up as `<workspace>/skills` on the next session.

## Security notes

*   Treat third-party skills as **untrusted code**. Read them before enabling.
*   Prefer sandboxed runs for untrusted inputs and risky tools. See [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing).
*   Workspace and extra-dir skill discovery only accepts skill roots and `SKILL.md` files whose resolved realpath stays inside the configured root.
*   `skills.entries.*.env` and `skills.entries.*.apiKey` inject secrets into the **host** process for that agent turn (not the sandbox). Keep secrets out of prompts and logs.
*   For a broader threat model and checklists, see [Security](https://docs.openclaw.ai/gateway/security).

## Format (AgentSkills + Pi-compatible)

`SKILL.md` must include at least:

```
---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image
---
```

Notes:

*   We follow the AgentSkills spec for layout/intent.
*   The parser used by the embedded agent supports **single-line** frontmatter keys only.
*   `metadata` should be a **single-line JSON object**.
*   Use `{baseDir}` in instructions to reference the skill folder path.
*   Optional frontmatter keys:
    *   `homepage` — URL surfaced as “Website” in the macOS Skills UI (also supported via `metadata.openclaw.homepage`).
    *   `user-invocable` — `true|false` (default: `true`). When `true`, the skill is exposed as a user slash command.
    *   `disable-model-invocation` — `true|false` (default: `false`). When `true`, the skill is excluded from the model prompt (still available via user invocation).
    *   `command-dispatch` — `tool` (optional). When set to `tool`, the slash command bypasses the model and dispatches directly to a tool.
    *   `command-tool` — tool name to invoke when `command-dispatch: tool` is set.
    *   `command-arg-mode` — `raw` (default). For tool dispatch, forwards the raw args string to the tool (no core parsing). The tool is invoked with params: `{ command: "<raw args>", commandName: "<slash command>", skillName: "<skill name>" }`.

## Gating (load-time filters)

OpenClaw **filters skills at load time** using `metadata` (single-line JSON):

```
---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["uv"], "env": ["GEMINI_API_KEY"], "config": ["browser.enabled"] },
        "primaryEnv": "GEMINI_API_KEY",
      },
  }
---
```

Fields under `metadata.openclaw`:

*   `always: true` — always include the skill (skip other gates).
*   `emoji` — optional emoji used by the macOS Skills UI.
*   `homepage` — optional URL shown as “Website” in the macOS Skills UI.
*   `os` — optional list of platforms (`darwin`, `linux`, `win32`). If set, the skill is only eligible on those OSes.
*   `requires.bins` — list; each must exist on `PATH`.
*   `requires.anyBins` — list; at least one must exist on `PATH`.
*   `requires.env` — list; env var must exist **or** be provided in config.
*   `requires.config` — list of `openclaw.json` paths that must be truthy.
*   `primaryEnv` — env var name associated with `skills.entries.<name>.apiKey`.
*   `install` — optional array of installer specs used by the macOS Skills UI (brew/node/go/uv/download).

Note on sandboxing:

*   `requires.bins` is checked on the **host** at skill load time.
*   If an agent is sandboxed, the binary must also exist **inside the container**. Install it via `agents.defaults.sandbox.docker.setupCommand` (or a custom image). `setupCommand` runs once after the container is created. Package installs also require network egress, a writable root FS, and a root user in the sandbox. Example: the `summarize` skill (`skills/summarize/SKILL.md`) needs the `summarize` CLI in the sandbox container to run there.

Installer example:

```
---
name: gemini
description: Use Gemini CLI for coding assistance and Google search lookups.
metadata:
  {
    "openclaw":
      {
        "emoji": "♊️",
        "requires": { "bins": ["gemini"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gemini-cli",
              "bins": ["gemini"],
              "label": "Install Gemini CLI (brew)",
            },
          ],
      },
  }
---
```

Notes:

*   If multiple installers are listed, the gateway picks a **single** preferred option (brew when available, otherwise node).
*   If all installers are `download`, OpenClaw lists each entry so you can see the available artifacts.
*   Installer specs can include `os: ["darwin"|"linux"|"win32"]` to filter options by platform.
*   Node installs honor `skills.install.nodeManager` in `openclaw.json` (default: npm; options: npm/pnpm/yarn/bun). This only affects **skill installs**; the Gateway runtime should still be Node (Bun is not recommended for WhatsApp/Telegram).
*   Go installs: if `go` is missing and `brew` is available, the gateway installs Go via Homebrew first and sets `GOBIN` to Homebrew’s `bin` when possible.
*   Download installs: `url` (required), `archive` (`tar.gz` | `tar.bz2` | `zip`), `extract` (default: auto when archive detected), `stripComponents`, `targetDir` (default: `~/.openclaw/tools/<skillKey>`).

If no `metadata.openclaw` is present, the skill is always eligible (unless disabled in config or blocked by `skills.allowBundled` for bundled skills).

## Config overrides (`~/.openclaw/openclaw.json`)

Bundled/managed skills can be toggled and supplied with env values:

```
{
  skills: {
    entries: {
      "nano-banana-pro": {
        enabled: true,
        apiKey: { source: "env", provider: "default", id: "GEMINI_API_KEY" }, // or plaintext string
        env: {
          GEMINI_API_KEY: "GEMINI_KEY_HERE",
        },
        config: {
          endpoint: "https://example.invalid",
          model: "nano-pro",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

Note: if the skill name contains hyphens, quote the key (JSON5 allows quoted keys). Config keys match the **skill name** by default. If a skill defines `metadata.openclaw.skillKey`, use that key under `skills.entries`. Rules:

*   `enabled: false` disables the skill even if it’s bundled/installed.
*   `env`: injected **only if** the variable isn’t already set in the process.
*   `apiKey`: convenience for skills that declare `metadata.openclaw.primaryEnv`. Supports plaintext string or SecretRef object (`{ source, provider, id }`).
*   `config`: optional bag for custom per-skill fields; custom keys must live here.
*   `allowBundled`: optional allowlist for **bundled** skills only. If set, only bundled skills in the list are eligible (managed/workspace skills unaffected).

## Environment injection (per agent run)

When an agent run starts, OpenClaw:

1.  Reads skill metadata.
2.  Applies any `skills.entries.<key>.env` or `skills.entries.<key>.apiKey` to `process.env`.
3.  Builds the system prompt with **eligible** skills.
4.  Restores the original environment after the run ends.

This is **scoped to the agent run**, not a global shell environment.

## Session snapshot (performance)

OpenClaw snapshots the eligible skills **when a session starts** and reuses that list for subsequent turns in the same session. Changes to skills or config take effect on the next new session. Skills can also refresh mid-session when the skills watcher is enabled or when a new eligible remote node appears (see below). Think of this as a **hot reload**: the refreshed list is picked up on the next agent turn.

## Remote macOS nodes (Linux gateway)

If the Gateway is running on Linux but a **macOS node** is connected **with `system.run` allowed** (Exec approvals security not set to `deny`), OpenClaw can treat macOS-only skills as eligible when the required binaries are present on that node. The agent should execute those skills via the `nodes` tool (typically `nodes.run`). This relies on the node reporting its command support and on a bin probe via `system.run`. If the macOS node goes offline later, the skills remain visible; invocations may fail until the node reconnects.

## Skills watcher (auto-refresh)

By default, OpenClaw watches skill folders and bumps the skills snapshot when `SKILL.md` files change. Configure this under `skills.load`:

```
{
  skills: {
    load: {
      watch: true,
      watchDebounceMs: 250,
    },
  },
}
```

## Token impact (skills list)

When skills are eligible, OpenClaw injects a compact XML list of available skills into the system prompt (via `formatSkillsForPrompt` in `pi-coding-agent`). The cost is deterministic:

*   **Base overhead (only when ≥1 skill):** 195 characters.
*   **Per skill:** 97 characters + the length of the XML-escaped `<name>`, `<description>`, and `<location>` values.

Formula (characters):

```
total = 195 + Σ (97 + len(name_escaped) + len(description_escaped) + len(location_escaped))
```

Notes:

*   XML escaping expands `& < > " '` into entities (`&amp;`, `&lt;`, etc.), increasing length.
*   Token counts vary by model tokenizer. A rough OpenAI-style estimate is ~4 chars/token, so **97 chars ≈ 24 tokens** per skill plus your actual field lengths.

## Managed skills lifecycle

OpenClaw ships a baseline set of skills as **bundled skills** as part of the install (npm package or OpenClaw.app). `~/.openclaw/skills` exists for local overrides (for example, pinning/patching a skill without changing the bundled copy). Workspace skills are user-owned and override both on name conflicts.

## Config reference

See [Skills config](https://docs.openclaw.ai/tools/skills-config) for the full configuration schema.

## Looking for more skills?

Browse [https://clawhub.com](https://clawhub.com/).

* * *

---

<!-- SOURCE: https://docs.openclaw.ai/tools/plugin -->

# Plugins - OpenClaw

## Plugins (Extensions)

## Quick start (new to plugins?)

A plugin is just a **small code module** that extends OpenClaw with extra features (commands, tools, and Gateway RPC). Most of the time, you’ll use plugins when you want a feature that’s not built into core OpenClaw yet (or you want to keep optional features out of your main install). Fast path:

1.  See what’s already loaded:

2.  Install an official plugin (example: Voice Call):

```
openclaw plugins install @openclaw/voice-call
```

Npm specs are **registry-only** (package name + optional **exact version** or **dist-tag**). Git/URL/file specs and semver ranges are rejected. Bare specs and `@latest` stay on the stable track. If npm resolves either of those to a prerelease, OpenClaw stops and asks you to opt in explicitly with a prerelease tag such as `@beta`/`@rc` or an exact prerelease version.

3.  Restart the Gateway, then configure under `plugins.entries.<id>.config`.

See [Voice Call](https://docs.openclaw.ai/plugins/voice-call) for a concrete example plugin. Looking for third-party listings? See [Community plugins](https://docs.openclaw.ai/plugins/community).

## Available plugins (official)

*   Microsoft Teams is plugin-only as of 2026.1.15; install `@openclaw/msteams` if you use Teams.
*   Memory (Core) — bundled memory search plugin (enabled by default via `plugins.slots.memory`)
*   Memory (LanceDB) — bundled long-term memory plugin (auto-recall/capture; set `plugins.slots.memory = "memory-lancedb"`)
*   [Voice Call](https://docs.openclaw.ai/plugins/voice-call) — `@openclaw/voice-call`
*   [Zalo Personal](https://docs.openclaw.ai/plugins/zalouser) — `@openclaw/zalouser`
*   [Matrix](https://docs.openclaw.ai/channels/matrix) — `@openclaw/matrix`
*   [Nostr](https://docs.openclaw.ai/channels/nostr) — `@openclaw/nostr`
*   [Zalo](https://docs.openclaw.ai/channels/zalo) — `@openclaw/zalo`
*   [Microsoft Teams](https://docs.openclaw.ai/channels/msteams) — `@openclaw/msteams`
*   Google Antigravity OAuth (provider auth) — bundled as `google-antigravity-auth` (disabled by default)
*   Gemini CLI OAuth (provider auth) — bundled as `google-gemini-cli-auth` (disabled by default)
*   Qwen OAuth (provider auth) — bundled as `qwen-portal-auth` (disabled by default)
*   Copilot Proxy (provider auth) — local VS Code Copilot Proxy bridge; distinct from built-in `github-copilot` device login (bundled, disabled by default)

OpenClaw plugins are **TypeScript modules** loaded at runtime via jiti. **Config validation does not execute plugin code**; it uses the plugin manifest and JSON Schema instead. See [Plugin manifest](https://docs.openclaw.ai/plugins/manifest). Plugins can register:

*   Gateway RPC methods
*   Gateway HTTP routes
*   Agent tools
*   CLI commands
*   Background services
*   Context engines
*   Optional config validation
*   **Skills** (by listing `skills` directories in the plugin manifest)
*   **Auto-reply commands** (execute without invoking the AI agent)

Plugins run **in‑process** with the Gateway, so treat them as trusted code. Tool authoring guide: [Plugin agent tools](https://docs.openclaw.ai/plugins/agent-tools).

## Runtime helpers

Plugins can access selected core helpers via `api.runtime`. For telephony TTS:

```
const result = await api.runtime.tts.textToSpeechTelephony({
  text: "Hello from OpenClaw",
  cfg: api.config,
});
```

Notes:

*   Uses core `messages.tts` configuration (OpenAI or ElevenLabs).
*   Returns PCM audio buffer + sample rate. Plugins must resample/encode for providers.
*   Edge TTS is not supported for telephony.

For STT/transcription, plugins can call:

```
const { text } = await api.runtime.stt.transcribeAudioFile({
  filePath: "/tmp/inbound-audio.ogg",
  cfg: api.config,
  // Optional when MIME cannot be inferred reliably:
  mime: "audio/ogg",
});
```

Notes:

*   Uses core media-understanding audio configuration (`tools.media.audio`) and provider fallback order.
*   Returns `{ text: undefined }` when no transcription output is produced (for example skipped/unsupported input).

## Gateway HTTP routes

Plugins can expose HTTP endpoints with `api.registerHttpRoute(...)`.

```
api.registerHttpRoute({
  path: "/acme/webhook",
  auth: "plugin",
  match: "exact",
  handler: async (_req, res) => {
    res.statusCode = 200;
    res.end("ok");
    return true;
  },
});
```

Route fields:

*   `path`: route path under the gateway HTTP server.
*   `auth`: required. Use `"gateway"` to require normal gateway auth, or `"plugin"` for plugin-managed auth/webhook verification.
*   `match`: optional. `"exact"` (default) or `"prefix"`.
*   `replaceExisting`: optional. Allows the same plugin to replace its own existing route registration.
*   `handler`: return `true` when the route handled the request.

Notes:

*   `api.registerHttpHandler(...)` is obsolete. Use `api.registerHttpRoute(...)`.
*   Plugin routes must declare `auth` explicitly.
*   Exact `path + match` conflicts are rejected unless `replaceExisting: true`, and one plugin cannot replace another plugin’s route.
*   Overlapping routes with different `auth` levels are rejected. Keep `exact`/`prefix` fallthrough chains on the same auth level only.

## Plugin SDK import paths

Use SDK subpaths instead of the monolithic `openclaw/plugin-sdk` import when authoring plugins:

*   `openclaw/plugin-sdk/core` for generic plugin APIs, provider auth types, and shared helpers.
*   `openclaw/plugin-sdk/compat` for bundled/internal plugin code that needs broader shared runtime helpers than `core`.
*   `openclaw/plugin-sdk/telegram` for Telegram channel plugins.
*   `openclaw/plugin-sdk/discord` for Discord channel plugins.
*   `openclaw/plugin-sdk/slack` for Slack channel plugins.
*   `openclaw/plugin-sdk/signal` for Signal channel plugins.
*   `openclaw/plugin-sdk/imessage` for iMessage channel plugins.
*   `openclaw/plugin-sdk/whatsapp` for WhatsApp channel plugins.
*   `openclaw/plugin-sdk/line` for LINE channel plugins.
*   `openclaw/plugin-sdk/msteams` for the bundled Microsoft Teams plugin surface.
*   Bundled extension-specific subpaths are also available: `openclaw/plugin-sdk/acpx`, `openclaw/plugin-sdk/bluebubbles`, `openclaw/plugin-sdk/copilot-proxy`, `openclaw/plugin-sdk/device-pair`, `openclaw/plugin-sdk/diagnostics-otel`, `openclaw/plugin-sdk/diffs`, `openclaw/plugin-sdk/feishu`, `openclaw/plugin-sdk/google-gemini-cli-auth`, `openclaw/plugin-sdk/googlechat`, `openclaw/plugin-sdk/irc`, `openclaw/plugin-sdk/llm-task`, `openclaw/plugin-sdk/lobster`, `openclaw/plugin-sdk/matrix`, `openclaw/plugin-sdk/mattermost`, `openclaw/plugin-sdk/memory-core`, `openclaw/plugin-sdk/memory-lancedb`, `openclaw/plugin-sdk/minimax-portal-auth`, `openclaw/plugin-sdk/nextcloud-talk`, `openclaw/plugin-sdk/nostr`, `openclaw/plugin-sdk/open-prose`, `openclaw/plugin-sdk/phone-control`, `openclaw/plugin-sdk/qwen-portal-auth`, `openclaw/plugin-sdk/synology-chat`, `openclaw/plugin-sdk/talk-voice`, `openclaw/plugin-sdk/test-utils`, `openclaw/plugin-sdk/thread-ownership`, `openclaw/plugin-sdk/tlon`, `openclaw/plugin-sdk/twitch`, `openclaw/plugin-sdk/voice-call`, `openclaw/plugin-sdk/zalo`, and `openclaw/plugin-sdk/zalouser`.

Compatibility note:

*   `openclaw/plugin-sdk` remains supported for existing external plugins.
*   New and migrated bundled plugins should use channel or extension-specific subpaths; use `core` for generic surfaces and `compat` only when broader shared helpers are required.

## Read-only channel inspection

If your plugin registers a channel, prefer implementing `plugin.config.inspectAccount(cfg, accountId)` alongside `resolveAccount(...)`. Why:

*   `resolveAccount(...)` is the runtime path. It is allowed to assume credentials are fully materialized and can fail fast when required secrets are missing.
*   Read-only command paths such as `openclaw status`, `openclaw status --all`, `openclaw channels status`, `openclaw channels resolve`, and doctor/config repair flows should not need to materialize runtime credentials just to describe configuration.

Recommended `inspectAccount(...)` behavior:

*   Return descriptive account state only.
*   Preserve `enabled` and `configured`.
*   Include credential source/status fields when relevant, such as:
    *   `tokenSource`, `tokenStatus`
    *   `botTokenSource`, `botTokenStatus`
    *   `appTokenSource`, `appTokenStatus`
    *   `signingSecretSource`, `signingSecretStatus`
*   You do not need to return raw token values just to report read-only availability. Returning `tokenStatus: "available"` (and the matching source field) is enough for status-style commands.
*   Use `configured_unavailable` when a credential is configured via SecretRef but unavailable in the current command path.

This lets read-only commands report “configured but unavailable in this command path” instead of crashing or misreporting the account as not configured. Performance note:

*   Plugin discovery and manifest metadata use short in-process caches to reduce bursty startup/reload work.
*   Set `OPENCLAW_DISABLE_PLUGIN_DISCOVERY_CACHE=1` or `OPENCLAW_DISABLE_PLUGIN_MANIFEST_CACHE=1` to disable these caches.
*   Tune cache windows with `OPENCLAW_PLUGIN_DISCOVERY_CACHE_MS` and `OPENCLAW_PLUGIN_MANIFEST_CACHE_MS`.

## Discovery & precedence

OpenClaw scans, in order:

1.  Config paths

*   `plugins.load.paths` (file or directory)

2.  Workspace extensions

*   `<workspace>/.openclaw/extensions/*.ts`
*   `<workspace>/.openclaw/extensions/*/index.ts`

3.  Global extensions

*   `~/.openclaw/extensions/*.ts`
*   `~/.openclaw/extensions/*/index.ts`

4.  Bundled extensions (shipped with OpenClaw, mostly disabled by default)

*   `<openclaw>/extensions/*`

Most bundled plugins must be enabled explicitly via `plugins.entries.<id>.enabled` or `openclaw plugins enable <id>`. Default-on bundled plugin exceptions:

*   `device-pair`
*   `phone-control`
*   `talk-voice`
*   active memory slot plugin (default slot: `memory-core`)

Installed plugins are enabled by default, but can be disabled the same way. Hardening notes:

*   If `plugins.allow` is empty and non-bundled plugins are discoverable, OpenClaw logs a startup warning with plugin ids and sources.
*   Candidate paths are safety-checked before discovery admission. OpenClaw blocks candidates when:
    *   extension entry resolves outside plugin root (including symlink/path traversal escapes),
    *   plugin root/source path is world-writable,
    *   path ownership is suspicious for non-bundled plugins (POSIX owner is neither current uid nor root).
*   Loaded non-bundled plugins without install/load-path provenance emit a warning so you can pin trust (`plugins.allow`) or install tracking (`plugins.installs`).

Each plugin must include a `openclaw.plugin.json` file in its root. If a path points at a file, the plugin root is the file’s directory and must contain the manifest. If multiple plugins resolve to the same id, the first match in the order above wins and lower-precedence copies are ignored.

### Package packs

A plugin directory may include a `package.json` with `openclaw.extensions`:

```
{
  "name": "my-pack",
  "openclaw": {
    "extensions": ["./src/safety.ts", "./src/tools.ts"]
  }
}
```

Each entry becomes a plugin. If the pack lists multiple extensions, the plugin id becomes `name/<fileBase>`. If your plugin imports npm deps, install them in that directory so `node_modules` is available (`npm install` / `pnpm install`). Security guardrail: every `openclaw.extensions` entry must stay inside the plugin directory after symlink resolution. Entries that escape the package directory are rejected. Security note: `openclaw plugins install` installs plugin dependencies with `npm install --ignore-scripts` (no lifecycle scripts). Keep plugin dependency trees “pure JS/TS” and avoid packages that require `postinstall` builds.

### Channel catalog metadata

Channel plugins can advertise onboarding metadata via `openclaw.channel` and install hints via `openclaw.install`. This keeps the core catalog data-free. Example:

```
{
  "name": "@openclaw/nextcloud-talk",
  "openclaw": {
    "extensions": ["./index.ts"],
    "channel": {
      "id": "nextcloud-talk",
      "label": "Nextcloud Talk",
      "selectionLabel": "Nextcloud Talk (self-hosted)",
      "docsPath": "/channels/nextcloud-talk",
      "docsLabel": "nextcloud-talk",
      "blurb": "Self-hosted chat via Nextcloud Talk webhook bots.",
      "order": 65,
      "aliases": ["nc-talk", "nc"]
    },
    "install": {
      "npmSpec": "@openclaw/nextcloud-talk",
      "localPath": "extensions/nextcloud-talk",
      "defaultChoice": "npm"
    }
  }
}
```

OpenClaw can also merge **external channel catalogs** (for example, an MPM registry export). Drop a JSON file at one of:

*   `~/.openclaw/mpm/plugins.json`
*   `~/.openclaw/mpm/catalog.json`
*   `~/.openclaw/plugins/catalog.json`

Or point `OPENCLAW_PLUGIN_CATALOG_PATHS` (or `OPENCLAW_MPM_CATALOG_PATHS`) at one or more JSON files (comma/semicolon/`PATH`\-delimited). Each file should contain `{ "entries": [ { "name": "@scope/pkg", "openclaw": { "channel": {...}, "install": {...} } } ] }`.

## Plugin IDs

Default plugin ids:

*   Package packs: `package.json` `name`
*   Standalone file: file base name (`~/.../voice-call.ts` → `voice-call`)

If a plugin exports `id`, OpenClaw uses it but warns when it doesn’t match the configured id.

## Config

```
{
  plugins: {
    enabled: true,
    allow: ["voice-call"],
    deny: ["untrusted-plugin"],
    load: { paths: ["~/Projects/oss/voice-call-extension"] },
    entries: {
      "voice-call": { enabled: true, config: { provider: "twilio" } },
    },
  },
}
```

Fields:

*   `enabled`: master toggle (default: true)
*   `allow`: allowlist (optional)
*   `deny`: denylist (optional; deny wins)
*   `load.paths`: extra plugin files/dirs
*   `slots`: exclusive slot selectors such as `memory` and `contextEngine`
*   `entries.<id>`: per‑plugin toggles + config

Config changes **require a gateway restart**. Validation rules (strict):

*   Unknown plugin ids in `entries`, `allow`, `deny`, or `slots` are **errors**.
*   Unknown `channels.<id>` keys are **errors** unless a plugin manifest declares the channel id.
*   Plugin config is validated using the JSON Schema embedded in `openclaw.plugin.json` (`configSchema`).
*   If a plugin is disabled, its config is preserved and a **warning** is emitted.

## Plugin slots (exclusive categories)

Some plugin categories are **exclusive** (only one active at a time). Use `plugins.slots` to select which plugin owns the slot:

```
{
  plugins: {
    slots: {
      memory: "memory-core", // or "none" to disable memory plugins
      contextEngine: "legacy", // or a plugin id such as "lossless-claw"
    },
  },
}
```

Supported exclusive slots:

*   `memory`: active memory plugin (`"none"` disables memory plugins)
*   `contextEngine`: active context engine plugin (`"legacy"` is the built-in default)

If multiple plugins declare `kind: "memory"` or `kind: "context-engine"`, only the selected plugin loads for that slot. Others are disabled with diagnostics.

### Context engine plugins

Context engine plugins own session context orchestration for ingest, assembly, and compaction. Register them from your plugin with `api.registerContextEngine(id, factory)`, then select the active engine with `plugins.slots.contextEngine`. Use this when your plugin needs to replace or extend the default context pipeline rather than just add memory search or hooks.

## Control UI (schema + labels)

The Control UI uses `config.schema` (JSON Schema + `uiHints`) to render better forms. OpenClaw augments `uiHints` at runtime based on discovered plugins:

*   Adds per-plugin labels for `plugins.entries.<id>` / `.enabled` / `.config`
*   Merges optional plugin-provided config field hints under: `plugins.entries.<id>.config.<field>`

If you want your plugin config fields to show good labels/placeholders (and mark secrets as sensitive), provide `uiHints` alongside your JSON Schema in the plugin manifest. Example:

```
{
  "id": "my-plugin",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "apiKey": { "type": "string" },
      "region": { "type": "string" }
    }
  },
  "uiHints": {
    "apiKey": { "label": "API Key", "sensitive": true },
    "region": { "label": "Region", "placeholder": "us-east-1" }
  }
}
```

## CLI

```
openclaw plugins list
openclaw plugins info <id>
openclaw plugins install <path>                 # copy a local file/dir into ~/.openclaw/extensions/<id>
openclaw plugins install ./extensions/voice-call # relative path ok
openclaw plugins install ./plugin.tgz           # install from a local tarball
openclaw plugins install ./plugin.zip           # install from a local zip
openclaw plugins install -l ./extensions/voice-call # link (no copy) for dev
openclaw plugins install @openclaw/voice-call # install from npm
openclaw plugins install @openclaw/voice-call --pin # store exact resolved name@version
openclaw plugins update <id>
openclaw plugins update --all
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw plugins doctor
```

`plugins update` only works for npm installs tracked under `plugins.installs`. If stored integrity metadata changes between updates, OpenClaw warns and asks for confirmation (use global `--yes` to bypass prompts). Plugins may also register their own top‑level commands (example: `openclaw voicecall`).

## Plugin API (overview)

Plugins export either:

*   A function: `(api) => { ... }`
*   An object: `{ id, name, configSchema, register(api) { ... } }`

Context engine plugins can also register a runtime-owned context manager:

```
export default function (api) {
  api.registerContextEngine("lossless-claw", () => ({
    info: { id: "lossless-claw", name: "Lossless Claw", ownsCompaction: true },
    async ingest() {
      return { ingested: true };
    },
    async assemble({ messages }) {
      return { messages, estimatedTokens: 0 };
    },
    async compact() {
      return { ok: true, compacted: false };
    },
  }));
}
```

Then enable it in config:

```
{
  plugins: {
    slots: {
      contextEngine: "lossless-claw",
    },
  },
}
```

## Plugin hooks

Plugins can register hooks at runtime. This lets a plugin bundle event-driven automation without a separate hook pack install.

### Example

```
export default function register(api) {
  api.registerHook(
    "command:new",
    async () => {
      // Hook logic here.
    },
    {
      name: "my-plugin.command-new",
      description: "Runs when /new is invoked",
    },
  );
}
```

Notes:

*   Register hooks explicitly via `api.registerHook(...)`.
*   Hook eligibility rules still apply (OS/bins/env/config requirements).
*   Plugin-managed hooks show up in `openclaw hooks list` with `plugin:<id>`.
*   You cannot enable/disable plugin-managed hooks via `openclaw hooks`; enable/disable the plugin instead.

### Agent lifecycle hooks (`api.on`)

For typed runtime lifecycle hooks, use `api.on(...)`:

```
export default function register(api) {
  api.on(
    "before_prompt_build",
    (event, ctx) => {
      return {
        prependSystemContext: "Follow company style guide.",
      };
    },
    { priority: 10 },
  );
}
```

Important hooks for prompt construction:

*   `before_model_resolve`: runs before session load (`messages` are not available). Use this to deterministically override `modelOverride` or `providerOverride`.
*   `before_prompt_build`: runs after session load (`messages` are available). Use this to shape prompt input.
*   `before_agent_start`: legacy compatibility hook. Prefer the two explicit hooks above.

Core-enforced hook policy:

*   Operators can disable prompt mutation hooks per plugin via `plugins.entries.<id>.hooks.allowPromptInjection: false`.
*   When disabled, OpenClaw blocks `before_prompt_build` and ignores prompt-mutating fields returned from legacy `before_agent_start` while preserving legacy `modelOverride` and `providerOverride`.

`before_prompt_build` result fields:

*   `prependContext`: prepends text to the user prompt for this run. Best for turn-specific or dynamic content.
*   `systemPrompt`: full system prompt override.
*   `prependSystemContext`: prepends text to the current system prompt.
*   `appendSystemContext`: appends text to the current system prompt.

Prompt build order in embedded runtime:

1.  Apply `prependContext` to the user prompt.
2.  Apply `systemPrompt` override when provided.
3.  Apply `prependSystemContext + current system prompt + appendSystemContext`.

Merge and precedence notes:

*   Hook handlers run by priority (higher first).
*   For merged context fields, values are concatenated in execution order.
*   `before_prompt_build` values are applied before legacy `before_agent_start` fallback values.

Migration guidance:

*   Move static guidance from `prependContext` to `prependSystemContext` (or `appendSystemContext`) so providers can cache stable system-prefix content.
*   Keep `prependContext` for per-turn dynamic context that should stay tied to the user message.

## Provider plugins (model auth)

Plugins can register **model provider auth** flows so users can run OAuth or API-key setup inside OpenClaw (no external scripts needed). Register a provider via `api.registerProvider(...)`. Each provider exposes one or more auth methods (OAuth, API key, device code, etc.). These methods power:

*   `openclaw models auth login --provider <id> [--method <id>]`

Example:

```
api.registerProvider({
  id: "acme",
  label: "AcmeAI",
  auth: [
    {
      id: "oauth",
      label: "OAuth",
      kind: "oauth",
      run: async (ctx) => {
        // Run OAuth flow and return auth profiles.
        return {
          profiles: [
            {
              profileId: "acme:default",
              credential: {
                type: "oauth",
                provider: "acme",
                access: "...",
                refresh: "...",
                expires: Date.now() + 3600 * 1000,
              },
            },
          ],
          defaultModel: "acme/opus-1",
        };
      },
    },
  ],
});
```

Notes:

*   `run` receives a `ProviderAuthContext` with `prompter`, `runtime`, `openUrl`, and `oauth.createVpsAwareHandlers` helpers.
*   Return `configPatch` when you need to add default models or provider config.
*   Return `defaultModel` so `--set-default` can update agent defaults.

### Register a messaging channel

Plugins can register **channel plugins** that behave like built‑in channels (WhatsApp, Telegram, etc.). Channel config lives under `channels.<id>` and is validated by your channel plugin code.

```
const myChannel = {
  id: "acmechat",
  meta: {
    id: "acmechat",
    label: "AcmeChat",
    selectionLabel: "AcmeChat (API)",
    docsPath: "/channels/acmechat",
    blurb: "demo channel plugin.",
    aliases: ["acme"],
  },
  capabilities: { chatTypes: ["direct"] },
  config: {
    listAccountIds: (cfg) => Object.keys(cfg.channels?.acmechat?.accounts ?? {}),
    resolveAccount: (cfg, accountId) =>
      cfg.channels?.acmechat?.accounts?.[accountId ?? "default"] ?? {
        accountId,
      },
  },
  outbound: {
    deliveryMode: "direct",
    sendText: async () => ({ ok: true }),
  },
};

export default function (api) {
  api.registerChannel({ plugin: myChannel });
}
```

Notes:

*   Put config under `channels.<id>` (not `plugins.entries`).
*   `meta.label` is used for labels in CLI/UI lists.
*   `meta.aliases` adds alternate ids for normalization and CLI inputs.
*   `meta.preferOver` lists channel ids to skip auto-enable when both are configured.
*   `meta.detailLabel` and `meta.systemImage` let UIs show richer channel labels/icons.

### Channel onboarding hooks

Channel plugins can define optional onboarding hooks on `plugin.onboarding`:

*   `configure(ctx)` is the baseline setup flow.
*   `configureInteractive(ctx)` can fully own interactive setup for both configured and unconfigured states.
*   `configureWhenConfigured(ctx)` can override behavior only for already configured channels.

Hook precedence in the wizard:

1.  `configureInteractive` (if present)
2.  `configureWhenConfigured` (only when channel status is already configured)
3.  fallback to `configure`

Context details:

*   `configureInteractive` and `configureWhenConfigured` receive:
    *   `configured` (`true` or `false`)
    *   `label` (user-facing channel name used by prompts)
    *   plus the shared config/runtime/prompter/options fields
*   Returning `"skip"` leaves selection and account tracking unchanged.
*   Returning `{ cfg, accountId? }` applies config updates and records account selection.

### Write a new messaging channel (step‑by‑step)

Use this when you want a **new chat surface** (a “messaging channel”), not a model provider. Model provider docs live under `/providers/*`.

1.  Pick an id + config shape

*   All channel config lives under `channels.<id>`.
*   Prefer `channels.<id>.accounts.<accountId>` for multi‑account setups.

2.  Define the channel metadata

*   `meta.label`, `meta.selectionLabel`, `meta.docsPath`, `meta.blurb` control CLI/UI lists.
*   `meta.docsPath` should point at a docs page like `/channels/<id>`.
*   `meta.preferOver` lets a plugin replace another channel (auto-enable prefers it).
*   `meta.detailLabel` and `meta.systemImage` are used by UIs for detail text/icons.

3.  Implement the required adapters

*   `config.listAccountIds` + `config.resolveAccount`
*   `capabilities` (chat types, media, threads, etc.)
*   `outbound.deliveryMode` + `outbound.sendText` (for basic send)

4.  Add optional adapters as needed

*   `setup` (wizard), `security` (DM policy), `status` (health/diagnostics)
*   `gateway` (start/stop/login), `mentions`, `threading`, `streaming`
*   `actions` (message actions), `commands` (native command behavior)

5.  Register the channel in your plugin

*   `api.registerChannel({ plugin })`

Minimal config example:

```
{
  channels: {
    acmechat: {
      accounts: {
        default: { token: "ACME_TOKEN", enabled: true },
      },
    },
  },
}
```

Minimal channel plugin (outbound‑only):

```
const plugin = {
  id: "acmechat",
  meta: {
    id: "acmechat",
    label: "AcmeChat",
    selectionLabel: "AcmeChat (API)",
    docsPath: "/channels/acmechat",
    blurb: "AcmeChat messaging channel.",
    aliases: ["acme"],
  },
  capabilities: { chatTypes: ["direct"] },
  config: {
    listAccountIds: (cfg) => Object.keys(cfg.channels?.acmechat?.accounts ?? {}),
    resolveAccount: (cfg, accountId) =>
      cfg.channels?.acmechat?.accounts?.[accountId ?? "default"] ?? {
        accountId,
      },
  },
  outbound: {
    deliveryMode: "direct",
    sendText: async ({ text }) => {
      // deliver `text` to your channel here
      return { ok: true };
    },
  },
};

export default function (api) {
  api.registerChannel({ plugin });
}
```

Load the plugin (extensions dir or `plugins.load.paths`), restart the gateway, then configure `channels.<id>` in your config.

### Agent tools

See the dedicated guide: [Plugin agent tools](https://docs.openclaw.ai/plugins/agent-tools).

### Register a gateway RPC method

```
export default function (api) {
  api.registerGatewayMethod("myplugin.status", ({ respond }) => {
    respond(true, { ok: true });
  });
}
```

### Register CLI commands

```
export default function (api) {
  api.registerCli(
    ({ program }) => {
      program.command("mycmd").action(() => {
        console.log("Hello");
      });
    },
    { commands: ["mycmd"] },
  );
}
```

### Register auto-reply commands

Plugins can register custom slash commands that execute **without invoking the AI agent**. This is useful for toggle commands, status checks, or quick actions that don’t need LLM processing.

```
export default function (api) {
  api.registerCommand({
    name: "mystatus",
    description: "Show plugin status",
    handler: (ctx) => ({
      text: `Plugin is running! Channel: ${ctx.channel}`,
    }),
  });
}
```

Command handler context:

*   `senderId`: The sender’s ID (if available)
*   `channel`: The channel where the command was sent
*   `isAuthorizedSender`: Whether the sender is an authorized user
*   `args`: Arguments passed after the command (if `acceptsArgs: true`)
*   `commandBody`: The full command text
*   `config`: The current OpenClaw config

Command options:

*   `name`: Command name (without the leading `/`)
*   `nativeNames`: Optional native-command aliases for slash/menu surfaces. Use `default` for all native providers, or provider-specific keys like `discord`
*   `description`: Help text shown in command lists
*   `acceptsArgs`: Whether the command accepts arguments (default: false). If false and arguments are provided, the command won’t match and the message falls through to other handlers
*   `requireAuth`: Whether to require authorized sender (default: true)
*   `handler`: Function that returns `{ text: string }` (can be async)

Example with authorization and arguments:

```
api.registerCommand({
  name: "setmode",
  description: "Set plugin mode",
  acceptsArgs: true,
  requireAuth: true,
  handler: async (ctx) => {
    const mode = ctx.args?.trim() || "default";
    await saveMode(mode);
    return { text: `Mode set to: ${mode}` };
  },
});
```

Notes:

*   Plugin commands are processed **before** built-in commands and the AI agent
*   Commands are registered globally and work across all channels
*   Command names are case-insensitive (`/MyStatus` matches `/mystatus`)
*   Command names must start with a letter and contain only letters, numbers, hyphens, and underscores
*   Reserved command names (like `help`, `status`, `reset`, etc.) cannot be overridden by plugins
*   Duplicate command registration across plugins will fail with a diagnostic error

### Register background services

```
export default function (api) {
  api.registerService({
    id: "my-service",
    start: () => api.logger.info("ready"),
    stop: () => api.logger.info("bye"),
  });
}
```

## Naming conventions

*   Gateway methods: `pluginId.action` (example: `voicecall.status`)
*   Tools: `snake_case` (example: `voice_call`)
*   CLI commands: kebab or camel, but avoid clashing with core commands

## Skills

Plugins can ship a skill in the repo (`skills/<name>/SKILL.md`). Enable it with `plugins.entries.<id>.enabled` (or other config gates) and ensure it’s present in your workspace/managed skills locations.

## Distribution (npm)

Recommended packaging:

*   Main package: `openclaw` (this repo)
*   Plugins: separate npm packages under `@openclaw/*` (example: `@openclaw/voice-call`)

Publishing contract:

*   Plugin `package.json` must include `openclaw.extensions` with one or more entry files.
*   Entry files can be `.js` or `.ts` (jiti loads TS at runtime).
*   `openclaw plugins install <npm-spec>` uses `npm pack`, extracts into `~/.openclaw/extensions/<id>/`, and enables it in config.
*   Config key stability: scoped packages are normalized to the **unscoped** id for `plugins.entries.*`.

## Example plugin: Voice Call

This repo includes a voice‑call plugin (Twilio or log fallback):

*   Source: `extensions/voice-call`
*   Skill: `skills/voice-call`
*   CLI: `openclaw voicecall start|status`
*   Tool: `voice_call`
*   RPC: `voicecall.start`, `voicecall.status`
*   Config (twilio): `provider: "twilio"` + `twilio.accountSid/authToken/from` (optional `statusCallbackUrl`, `twimlUrl`)
*   Config (dev): `provider: "log"` (no network)

See [Voice Call](https://docs.openclaw.ai/plugins/voice-call) and `extensions/voice-call/README.md` for setup and usage.

## Safety notes

Plugins run in-process with the Gateway. Treat them as trusted code:

*   Only install plugins you trust.
*   Prefer `plugins.allow` allowlists.
*   Restart the Gateway after changes.

## Testing plugins

Plugins can (and should) ship tests:

*   In-repo plugins can keep Vitest tests under `src/**` (example: `src/plugins/voice-call.plugin.test.ts`).
*   Separately published plugins should run their own CI (lint/build/test) and validate `openclaw.extensions` points at the built entrypoint (`dist/index.js`).

---

<!-- SOURCE: https://docs.openclaw.ai/brave-search -->

# Brave Search - OpenClaw

OpenClaw supports Brave Search API as a `web_search` provider.

## Get an API key

1.  Create a Brave Search API account at [https://brave.com/search/api/](https://brave.com/search/api/)
2.  In the dashboard, choose the **Search** plan and generate an API key.
3.  Store the key in config or set `BRAVE_API_KEY` in the Gateway environment.

## Config example

```
{
  tools: {
    web: {
      search: {
        provider: "brave",
        apiKey: "BRAVE_API_KEY_HERE",
        maxResults: 5,
        timeoutSeconds: 30,
      },
    },
  },
}
```

| Parameter | Description |
| --- | --- |
| `query` | Search query (required) |
| `count` | Number of results to return (1-10, default: 5) |
| `country` | 2-letter ISO country code (e.g., “US”, “DE”) |
| `language` | ISO 639-1 language code for search results (e.g., “en”, “de”, “fr”) |
| `ui_lang` | ISO language code for UI elements |
| `freshness` | Time filter: `day` (24h), `week`, `month`, or `year` |
| `date_after` | Only results published after this date (YYYY-MM-DD) |
| `date_before` | Only results published before this date (YYYY-MM-DD) |

**Examples:**

```
// Country and language-specific search
await web_search({
  query: "renewable energy",
  country: "DE",
  language: "de",
});

// Recent results (past week)
await web_search({
  query: "AI news",
  freshness: "week",
});

// Date range search
await web_search({
  query: "AI developments",
  date_after: "2024-01-01",
  date_before: "2024-06-30",
});
```

## Notes

*   OpenClaw uses the Brave **Search** plan. If you have a legacy subscription (e.g. the original Free plan with 2,000 queries/month), it remains valid but does not include newer features like LLM Context or higher rate limits.
*   Each Brave plan includes \*\*5/monthinfreecredit∗∗(renewing).TheSearchplancosts5/month in free credit\*\* (renewing). The Search plan costs 5 per 1,000 requests, so the credit covers 1,000 queries/month. Set your usage limit in the Brave dashboard to avoid unexpected charges. See the [Brave API portal](https://brave.com/search/api/) for current plans.
*   The Search plan includes the LLM Context endpoint and AI inference rights. Storing results to train or tune models requires a plan with explicit storage rights. See the Brave [Terms of Service](https://api-dashboard.search.brave.com/terms-of-service).
*   Results are cached for 15 minutes by default (configurable via `cacheTtlMinutes`).

See [Web tools](https://docs.openclaw.ai/tools/web) for the full web\_search configuration.

---

<!-- SOURCE: https://docs.openclaw.ai/tools/diffs -->

# Diffs - OpenClaw

`diffs` is an optional plugin tool with short built-in system guidance and a companion skill that turns change content into a read-only diff artifact for agents. It accepts either:

*   `before` and `after` text
*   a unified `patch`

It can return:

*   a gateway viewer URL for canvas presentation
*   a rendered file path (PNG or PDF) for message delivery
*   both outputs in one call

When enabled, the plugin prepends concise usage guidance into system-prompt space and also exposes a detailed skill for cases where the agent needs fuller instructions.

## Quick start

1.  Enable the plugin.
2.  Call `diffs` with `mode: "view"` for canvas-first flows.
3.  Call `diffs` with `mode: "file"` for chat file delivery flows.
4.  Call `diffs` with `mode: "both"` when you need both artifacts.

## Enable the plugin

```
{
  plugins: {
    entries: {
      diffs: {
        enabled: true,
      },
    },
  },
}
```

## Disable built-in system guidance

If you want to keep the `diffs` tool enabled but disable its built-in system-prompt guidance, set `plugins.entries.diffs.hooks.allowPromptInjection` to `false`:

```
{
  plugins: {
    entries: {
      diffs: {
        enabled: true,
        hooks: {
          allowPromptInjection: false,
        },
      },
    },
  },
}
```

This blocks the diffs plugin’s `before_prompt_build` hook while keeping the plugin, tool, and companion skill available. If you want to disable both the guidance and the tool, disable the plugin instead.

## Typical agent workflow

1.  Agent calls `diffs`.
2.  Agent reads `details` fields.
3.  Agent either:
    *   opens `details.viewerUrl` with `canvas present`
    *   sends `details.filePath` with `message` using `path` or `filePath`
    *   does both

## Input examples

Before and after:

```
{
  "before": "# Hello\n\nOne",
  "after": "# Hello\n\nTwo",
  "path": "docs/example.md",
  "mode": "view"
}
```

Patch:

```
{
  "patch": "diff --git a/src/example.ts b/src/example.ts\n--- a/src/example.ts\n+++ b/src/example.ts\n@@ -1 +1 @@\n-const x = 1;\n+const x = 2;\n",
  "mode": "both"
}
```

All fields are optional unless noted:

*   `before` (`string`): original text. Required with `after` when `patch` is omitted.
*   `after` (`string`): updated text. Required with `before` when `patch` is omitted.
*   `patch` (`string`): unified diff text. Mutually exclusive with `before` and `after`.
*   `path` (`string`): display filename for before and after mode.
*   `lang` (`string`): language override hint for before and after mode.
*   `title` (`string`): viewer title override.
*   `mode` (`"view" | "file" | "both"`): output mode. Defaults to plugin default `defaults.mode`.
*   `theme` (`"light" | "dark"`): viewer theme. Defaults to plugin default `defaults.theme`.
*   `layout` (`"unified" | "split"`): diff layout. Defaults to plugin default `defaults.layout`.
*   `expandUnchanged` (`boolean`): expand unchanged sections when full context is available. Per-call option only (not a plugin default key).
*   `fileFormat` (`"png" | "pdf"`): rendered file format. Defaults to plugin default `defaults.fileFormat`.
*   `fileQuality` (`"standard" | "hq" | "print"`): quality preset for PNG or PDF rendering.
*   `fileScale` (`number`): device scale override (`1`\-`4`).
*   `fileMaxWidth` (`number`): max render width in CSS pixels (`640`\-`2400`).
*   `ttlSeconds` (`number`): viewer artifact TTL in seconds. Default 1800, max 21600.
*   `baseUrl` (`string`): viewer URL origin override. Must be `http` or `https`, no query/hash.

Validation and limits:

*   `before` and `after` each max 512 KiB.
*   `patch` max 2 MiB.
*   `path` max 2048 bytes.
*   `lang` max 128 bytes.
*   `title` max 1024 bytes.
*   Patch complexity cap: max 128 files and 120000 total lines.
*   `patch` and `before` or `after` together are rejected.
*   Rendered file safety limits (apply to PNG and PDF):
    *   `fileQuality: "standard"`: max 8 MP (8,000,000 rendered pixels).
    *   `fileQuality: "hq"`: max 14 MP (14,000,000 rendered pixels).
    *   `fileQuality: "print"`: max 24 MP (24,000,000 rendered pixels).
    *   PDF also has a max of 50 pages.

## Output details contract

The tool returns structured metadata under `details`. Shared fields for modes that create a viewer:

*   `artifactId`
*   `viewerUrl`
*   `viewerPath`
*   `title`
*   `expiresAt`
*   `inputKind`
*   `fileCount`
*   `mode`

File fields when PNG or PDF is rendered:

*   `filePath`
*   `path` (same value as `filePath`, for message tool compatibility)
*   `fileBytes`
*   `fileFormat`
*   `fileQuality`
*   `fileScale`
*   `fileMaxWidth`

Mode behavior summary:

*   `mode: "view"`: viewer fields only.
*   `mode: "file"`: file fields only, no viewer artifact.
*   `mode: "both"`: viewer fields plus file fields. If file rendering fails, viewer still returns with `fileError`.

## Collapsed unchanged sections

*   The viewer can show rows like `N unmodified lines`.
*   Expand controls on those rows are conditional and not guaranteed for every input kind.
*   Expand controls appear when the rendered diff has expandable context data, which is typical for before and after input.
*   For many unified patch inputs, omitted context bodies are not available in the parsed patch hunks, so the row can appear without expand controls. This is expected behavior.
*   `expandUnchanged` applies only when expandable context exists.

## Plugin defaults

Set plugin-wide defaults in `~/.openclaw/openclaw.json`:

```
{
  plugins: {
    entries: {
      diffs: {
        enabled: true,
        config: {
          defaults: {
            fontFamily: "Fira Code",
            fontSize: 15,
            lineSpacing: 1.6,
            layout: "unified",
            showLineNumbers: true,
            diffIndicators: "bars",
            wordWrap: true,
            background: true,
            theme: "dark",
            fileFormat: "png",
            fileQuality: "standard",
            fileScale: 2,
            fileMaxWidth: 960,
            mode: "both",
          },
        },
      },
    },
  },
}
```

Supported defaults:

*   `fontFamily`
*   `fontSize`
*   `lineSpacing`
*   `layout`
*   `showLineNumbers`
*   `diffIndicators`
*   `wordWrap`
*   `background`
*   `theme`
*   `fileFormat`
*   `fileQuality`
*   `fileScale`
*   `fileMaxWidth`
*   `mode`

Explicit tool parameters override these defaults.

## Security config

*   `security.allowRemoteViewer` (`boolean`, default `false`)
    *   `false`: non-loopback requests to viewer routes are denied.
    *   `true`: remote viewers are allowed if tokenized path is valid.

Example:

```
{
  plugins: {
    entries: {
      diffs: {
        enabled: true,
        config: {
          security: {
            allowRemoteViewer: false,
          },
        },
      },
    },
  },
}
```

## Artifact lifecycle and storage

*   Artifacts are stored under the temp subfolder: `$TMPDIR/openclaw-diffs`.
*   Viewer artifact metadata contains:
    *   random artifact ID (20 hex chars)
    *   random token (48 hex chars)
    *   `createdAt` and `expiresAt`
    *   stored `viewer.html` path
*   Default viewer TTL is 30 minutes when not specified.
*   Maximum accepted viewer TTL is 6 hours.
*   Cleanup runs opportunistically after artifact creation.
*   Expired artifacts are deleted.
*   Fallback cleanup removes stale folders older than 24 hours when metadata is missing.

## Viewer URL and network behavior

Viewer route:

*   `/plugins/diffs/view/{artifactId}/{token}`

Viewer assets:

*   `/plugins/diffs/assets/viewer.js`
*   `/plugins/diffs/assets/viewer-runtime.js`

URL construction behavior:

*   If `baseUrl` is provided, it is used after strict validation.
*   Without `baseUrl`, viewer URL defaults to loopback `127.0.0.1`.
*   If gateway bind mode is `custom` and `gateway.customBindHost` is set, that host is used.

`baseUrl` rules:

*   Must be `http://` or `https://`.
*   Query and hash are rejected.
*   Origin plus optional base path is allowed.

## Security model

Viewer hardening:

*   Loopback-only by default.
*   Tokenized viewer paths with strict ID and token validation.
*   Viewer response CSP:
    *   `default-src 'none'`
    *   scripts and assets only from self
    *   no outbound `connect-src`
*   Remote miss throttling when remote access is enabled:
    *   40 failures per 60 seconds
    *   60 second lockout (`429 Too Many Requests`)

File rendering hardening:

*   Screenshot browser request routing is deny-by-default.
*   Only local viewer assets from `http://127.0.0.1/plugins/diffs/assets/*` are allowed.
*   External network requests are blocked.

## Browser requirements for file mode

`mode: "file"` and `mode: "both"` need a Chromium-compatible browser. Resolution order:

1.  `browser.executablePath` in OpenClaw config.
2.  Environment variables:
    *   `OPENCLAW_BROWSER_EXECUTABLE_PATH`
    *   `BROWSER_EXECUTABLE_PATH`
    *   `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`
3.  Platform command/path discovery fallback.

Common failure text:

*   `Diff PNG/PDF rendering requires a Chromium-compatible browser...`

Fix by installing Chrome, Chromium, Edge, or Brave, or setting one of the executable path options above.

## Troubleshooting

Input validation errors:

*   `Provide patch or both before and after text.`
    *   Include both `before` and `after`, or provide `patch`.
*   `Provide either patch or before/after input, not both.`
    *   Do not mix input modes.
*   `Invalid baseUrl: ...`
    *   Use `http(s)` origin with optional path, no query/hash.
*   `{field} exceeds maximum size (...)`
    *   Reduce payload size.
*   Large patch rejection
    *   Reduce patch file count or total lines.

Viewer accessibility issues:

*   Viewer URL resolves to `127.0.0.1` by default.
*   For remote access scenarios, either:
    *   pass `baseUrl` per tool call, or
    *   use `gateway.bind=custom` and `gateway.customBindHost`
*   Enable `security.allowRemoteViewer` only when you intend external viewer access.

Unmodified-lines row has no expand button:

*   This can happen for patch input when the patch does not carry expandable context.
*   This is expected and does not indicate a viewer failure.

Artifact not found:

*   Artifact expired due TTL.
*   Token or path changed.
*   Cleanup removed stale data.

## Operational guidance

*   Prefer `mode: "view"` for local interactive reviews in canvas.
*   Prefer `mode: "file"` for outbound chat channels that need an attachment.
*   Keep `allowRemoteViewer` disabled unless your deployment requires remote viewer URLs.
*   Set explicit short `ttlSeconds` for sensitive diffs.
*   Avoid sending secrets in diff input when not required.
*   If your channel compresses images aggressively (for example Telegram or WhatsApp), prefer PDF output (`fileFormat: "pdf"`).

Diff rendering engine:

*   Powered by [Diffs](https://diffs.com/).

*   [Tools overview](https://docs.openclaw.ai/tools)
*   [Plugins](https://docs.openclaw.ai/tools/plugin)
*   [Browser](https://docs.openclaw.ai/tools/browser)

---

<!-- SOURCE: https://docs.openclaw.ai/tools/elevated -->

# Elevated Mode - OpenClaw

## Elevated Mode (/elevated directives)

## What it does

*   `/elevated on` runs on the gateway host and keeps exec approvals (same as `/elevated ask`).
*   `/elevated full` runs on the gateway host **and** auto-approves exec (skips exec approvals).
*   `/elevated ask` runs on the gateway host but keeps exec approvals (same as `/elevated on`).
*   `on`/`ask` do **not** force `exec.security=full`; configured security/ask policy still applies.
*   Only changes behavior when the agent is **sandboxed** (otherwise exec already runs on the host).
*   Directive forms: `/elevated on|off|ask|full`, `/elev on|off|ask|full`.
*   Only `on|off|ask|full` are accepted; anything else returns a hint and does not change state.

## What it controls (and what it doesn’t)

*   **Availability gates**: `tools.elevated` is the global baseline. `agents.list[].tools.elevated` can further restrict elevated per agent (both must allow).
*   **Per-session state**: `/elevated on|off|ask|full` sets the elevated level for the current session key.
*   **Inline directive**: `/elevated on|ask|full` inside a message applies to that message only.
*   **Groups**: In group chats, elevated directives are only honored when the agent is mentioned. Command-only messages that bypass mention requirements are treated as mentioned.
*   **Host execution**: elevated forces `exec` onto the gateway host; `full` also sets `security=full`.
*   **Approvals**: `full` skips exec approvals; `on`/`ask` honor them when allowlist/ask rules require.
*   **Unsandboxed agents**: no-op for location; only affects gating, logging, and status.
*   **Tool policy still applies**: if `exec` is denied by tool policy, elevated cannot be used.
*   **Separate from `/exec`**: `/exec` adjusts per-session defaults for authorized senders and does not require elevated.

## Resolution order

1.  Inline directive on the message (applies only to that message).
2.  Session override (set by sending a directive-only message).
3.  Global default (`agents.defaults.elevatedDefault` in config).

## Setting a session default

*   Send a message that is **only** the directive (whitespace allowed), e.g. `/elevated full`.
*   Confirmation reply is sent (`Elevated mode set to full...` / `Elevated mode disabled.`).
*   If elevated access is disabled or the sender is not on the approved allowlist, the directive replies with an actionable error and does not change session state.
*   Send `/elevated` (or `/elevated:`) with no argument to see the current elevated level.

## Availability + allowlists

*   Feature gate: `tools.elevated.enabled` (default can be off via config even if the code supports it).
*   Sender allowlist: `tools.elevated.allowFrom` with per-provider allowlists (e.g. `discord`, `whatsapp`).
*   Unprefixed allowlist entries match sender-scoped identity values only (`SenderId`, `SenderE164`, `From`); recipient routing fields are never used for elevated authorization.
*   Mutable sender metadata requires explicit prefixes:
    *   `name:<value>` matches `SenderName`
    *   `username:<value>` matches `SenderUsername`
    *   `tag:<value>` matches `SenderTag`
    *   `id:<value>`, `from:<value>`, `e164:<value>` are available for explicit identity targeting
*   Per-agent gate: `agents.list[].tools.elevated.enabled` (optional; can only further restrict).
*   Per-agent allowlist: `agents.list[].tools.elevated.allowFrom` (optional; when set, the sender must match **both** global + per-agent allowlists).
*   Discord fallback: if `tools.elevated.allowFrom.discord` is omitted, the `channels.discord.allowFrom` list is used as a fallback (legacy: `channels.discord.dm.allowFrom`). Set `tools.elevated.allowFrom.discord` (even `[]`) to override. Per-agent allowlists do **not** use the fallback.
*   All gates must pass; otherwise elevated is treated as unavailable.

## Logging + status

*   Elevated exec calls are logged at info level.
*   Session status includes elevated mode (e.g. `elevated=ask`, `elevated=full`).

---

<!-- SOURCE: https://docs.openclaw.ai/tools/apply-patch -->

# apply\_patch Tool - OpenClaw

Apply file changes using a structured patch format. This is ideal for multi-file or multi-hunk edits where a single `edit` call would be brittle. The tool accepts a single `input` string that wraps one or more file operations:

```
*** Begin Patch
*** Add File: path/to/file.txt
+line 1
+line 2
*** Update File: src/app.ts
@@
-old line
+new line
*** Delete File: obsolete.txt
*** End Patch
```

## Parameters

*   `input` (required): Full patch contents including `*** Begin Patch` and `*** End Patch`.

## Notes

*   Patch paths support relative paths (from the workspace directory) and absolute paths.
*   `tools.exec.applyPatch.workspaceOnly` defaults to `true` (workspace-contained). Set it to `false` only if you intentionally want `apply_patch` to write/delete outside the workspace directory.
*   Use `*** Move to:` within an `*** Update File:` hunk to rename files.
*   `*** End of File` marks an EOF-only insert when needed.
*   Experimental and disabled by default. Enable with `tools.exec.applyPatch.enabled`.
*   OpenAI-only (including OpenAI Codex). Optionally gate by model via `tools.exec.applyPatch.allowModels`.
*   Config is only under `tools.exec`.

## Example

```
{
  "tool": "apply_patch",
  "input": "*** Begin Patch\n*** Update File: src/index.ts\n@@\n-const foo = 1\n+const foo = 2\n*** End Patch"
}
```

---

<!-- SOURCE: https://docs.openclaw.ai/perplexity -->

# Perplexity Sonar - OpenClaw

OpenClaw can use Perplexity Sonar for the `web_search` tool. You can connect through Perplexity’s direct API or via OpenRouter.

## API options

### Perplexity (direct)

*   Base URL: [https://api.perplexity.ai](https://api.perplexity.ai/)
*   Environment variable: `PERPLEXITY_API_KEY`

### OpenRouter (alternative)

*   Base URL: [https://openrouter.ai/api/v1](https://openrouter.ai/api/v1)
*   Environment variable: `OPENROUTER_API_KEY`
*   Supports prepaid/crypto credits.

## Config example

```
{
  tools: {
    web: {
      search: {
        provider: "perplexity",
        perplexity: {
          apiKey: "pplx-...",
          baseUrl: "https://api.perplexity.ai",
          model: "perplexity/sonar-pro",
        },
      },
    },
  },
}
```

## Switching from Brave

```
{
  tools: {
    web: {
      search: {
        provider: "perplexity",
        perplexity: {
          apiKey: "pplx-...",
          baseUrl: "https://api.perplexity.ai",
        },
      },
    },
  },
}
```

If both `PERPLEXITY_API_KEY` and `OPENROUTER_API_KEY` are set, set `tools.web.search.perplexity.baseUrl` (or `tools.web.search.perplexity.apiKey`) to disambiguate. If no base URL is set, OpenClaw chooses a default based on the API key source:

*   `PERPLEXITY_API_KEY` or `pplx-...` → direct Perplexity (`https://api.perplexity.ai`)
*   `OPENROUTER_API_KEY` or `sk-or-...` → OpenRouter (`https://openrouter.ai/api/v1`)
*   Unknown key formats → OpenRouter (safe fallback)

## Models

*   `perplexity/sonar` — fast Q&A with web search
*   `perplexity/sonar-pro` (default) — multi-step reasoning + web search
*   `perplexity/sonar-reasoning-pro` — deep research

See [Web tools](https://docs.openclaw.ai/tools/web) for the full web\_search configuration.

---

<!-- SOURCE: https://docs.openclaw.ai/tools/exec -->

# Exec Tool - OpenClaw

Run shell commands in the workspace. Supports foreground + background execution via `process`. If `process` is disallowed, `exec` runs synchronously and ignores `yieldMs`/`background`. Background sessions are scoped per agent; `process` only sees sessions from the same agent.

## Parameters

*   `command` (required)
*   `workdir` (defaults to cwd)
*   `env` (key/value overrides)
*   `yieldMs` (default 10000): auto-background after delay
*   `background` (bool): background immediately
*   `timeout` (seconds, default 1800): kill on expiry
*   `pty` (bool): run in a pseudo-terminal when available (TTY-only CLIs, coding agents, terminal UIs)
*   `host` (`sandbox | gateway | node`): where to execute
*   `security` (`deny | allowlist | full`): enforcement mode for `gateway`/`node`
*   `ask` (`off | on-miss | always`): approval prompts for `gateway`/`node`
*   `node` (string): node id/name for `host=node`
*   `elevated` (bool): request elevated mode (gateway host); `security=full` is only forced when elevated resolves to `full`

Notes:

*   `host` defaults to `sandbox`.
*   `elevated` is ignored when sandboxing is off (exec already runs on the host).
*   `gateway`/`node` approvals are controlled by `~/.openclaw/exec-approvals.json`.
*   `node` requires a paired node (companion app or headless node host).
*   If multiple nodes are available, set `exec.node` or `tools.exec.node` to select one.
*   On non-Windows hosts, exec uses `SHELL` when set; if `SHELL` is `fish`, it prefers `bash` (or `sh`) from `PATH` to avoid fish-incompatible scripts, then falls back to `SHELL` if neither exists.
*   On Windows hosts, exec prefers PowerShell 7 (`pwsh`) discovery (Program Files, ProgramW6432, then PATH), then falls back to Windows PowerShell 5.1.
*   Host execution (`gateway`/`node`) rejects `env.PATH` and loader overrides (`LD_*`/`DYLD_*`) to prevent binary hijacking or injected code.
*   OpenClaw sets `OPENCLAW_SHELL=exec` in the spawned command environment (including PTY and sandbox execution) so shell/profile rules can detect exec-tool context.
*   Important: sandboxing is **off by default**. If sandboxing is off and `host=sandbox` is explicitly configured/requested, exec now fails closed instead of silently running on the gateway host. Enable sandboxing or use `host=gateway` with approvals.
*   Script preflight checks (for common Python/Node shell-syntax mistakes) only inspect files inside the effective `workdir` boundary. If a script path resolves outside `workdir`, preflight is skipped for that file.

## Config

*   `tools.exec.notifyOnExit` (default: true): when true, backgrounded exec sessions enqueue a system event and request a heartbeat on exit.
*   `tools.exec.approvalRunningNoticeMs` (default: 10000): emit a single “running” notice when an approval-gated exec runs longer than this (0 disables).
*   `tools.exec.host` (default: `sandbox`)
*   `tools.exec.security` (default: `deny` for sandbox, `allowlist` for gateway + node when unset)
*   `tools.exec.ask` (default: `on-miss`)
*   `tools.exec.node` (default: unset)
*   `tools.exec.pathPrepend`: list of directories to prepend to `PATH` for exec runs (gateway + sandbox only).
*   `tools.exec.safeBins`: stdin-only safe binaries that can run without explicit allowlist entries. For behavior details, see [Safe bins](https://docs.openclaw.ai/tools/exec-approvals#safe-bins-stdin-only).
*   `tools.exec.safeBinTrustedDirs`: additional explicit directories trusted for `safeBins` path checks. `PATH` entries are never auto-trusted. Built-in defaults are `/bin` and `/usr/bin`.
*   `tools.exec.safeBinProfiles`: optional custom argv policy per safe bin (`minPositional`, `maxPositional`, `allowedValueFlags`, `deniedFlags`).

Example:

```
{
  tools: {
    exec: {
      pathPrepend: ["~/bin", "/opt/oss/bin"],
    },
  },
}
```

### PATH handling

*   `host=gateway`: merges your login-shell `PATH` into the exec environment. `env.PATH` overrides are rejected for host execution. The daemon itself still runs with a minimal `PATH`:
    *   macOS: `/opt/homebrew/bin`, `/usr/local/bin`, `/usr/bin`, `/bin`
    *   Linux: `/usr/local/bin`, `/usr/bin`, `/bin`
*   `host=sandbox`: runs `sh -lc` (login shell) inside the container, so `/etc/profile` may reset `PATH`. OpenClaw prepends `env.PATH` after profile sourcing via an internal env var (no shell interpolation); `tools.exec.pathPrepend` applies here too.
*   `host=node`: only non-blocked env overrides you pass are sent to the node. `env.PATH` overrides are rejected for host execution and ignored by node hosts. If you need additional PATH entries on a node, configure the node host service environment (systemd/launchd) or install tools in standard locations.

Per-agent node binding (use the agent list index in config):

```
openclaw config get agents.list
openclaw config set agents.list[0].tools.exec.node "node-id-or-name"
```

Control UI: the Nodes tab includes a small “Exec node binding” panel for the same settings.

## Session overrides (`/exec`)

Use `/exec` to set **per-session** defaults for `host`, `security`, `ask`, and `node`. Send `/exec` with no arguments to show the current values. Example:

```
/exec host=gateway security=allowlist ask=on-miss node=mac-1
```

`/exec` is only honored for **authorized senders** (channel allowlists/pairing plus `commands.useAccessGroups`). It updates **session state only** and does not write config. To hard-disable exec, deny it via tool policy (`tools.deny: ["exec"]` or per-agent). Host approvals still apply unless you explicitly set `security=full` and `ask=off`.

## Exec approvals (companion app / node host)

Sandboxed agents can require per-request approval before `exec` runs on the gateway or node host. See [Exec approvals](https://docs.openclaw.ai/tools/exec-approvals) for the policy, allowlist, and UI flow. When approvals are required, the exec tool returns immediately with `status: "approval-pending"` and an approval id. Once approved (or denied / timed out), the Gateway emits system events (`Exec finished` / `Exec denied`). If the command is still running after `tools.exec.approvalRunningNoticeMs`, a single `Exec running` notice is emitted.

## Allowlist + safe bins

Manual allowlist enforcement matches **resolved binary paths only** (no basename matches). When `security=allowlist`, shell commands are auto-allowed only if every pipeline segment is allowlisted or a safe bin. Chaining (`;`, `&&`, `||`) and redirections are rejected in allowlist mode unless every top-level segment satisfies the allowlist (including safe bins). Redirections remain unsupported. `autoAllowSkills` is a separate convenience path in exec approvals. It is not the same as manual path allowlist entries. For strict explicit trust, keep `autoAllowSkills` disabled. Use the two controls for different jobs:

*   `tools.exec.safeBins`: small, stdin-only stream filters.
*   `tools.exec.safeBinTrustedDirs`: explicit extra trusted directories for safe-bin executable paths.
*   `tools.exec.safeBinProfiles`: explicit argv policy for custom safe bins.
*   allowlist: explicit trust for executable paths.

Do not treat `safeBins` as a generic allowlist, and do not add interpreter/runtime binaries (for example `python3`, `node`, `ruby`, `bash`). If you need those, use explicit allowlist entries and keep approval prompts enabled. `openclaw security audit` warns when interpreter/runtime `safeBins` entries are missing explicit profiles, and `openclaw doctor --fix` can scaffold missing custom `safeBinProfiles` entries. For full policy details and examples, see [Exec approvals](https://docs.openclaw.ai/tools/exec-approvals#safe-bins-stdin-only) and [Safe bins versus allowlist](https://docs.openclaw.ai/tools/exec-approvals#safe-bins-versus-allowlist).

## Examples

Foreground:

```
{ "tool": "exec", "command": "ls -la" }
```

Background + poll:

```
{"tool":"exec","command":"npm run build","yieldMs":1000}
{"tool":"process","action":"poll","sessionId":"<id>"}
```

Send keys (tmux-style):

```
{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["Enter"]}
{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["C-c"]}
{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["Up","Up","Enter"]}
```

Submit (send CR only):

```
{ "tool": "process", "action": "submit", "sessionId": "<id>" }
```

Paste (bracketed by default):

```
{ "tool": "process", "action": "paste", "sessionId": "<id>", "text": "line1\nline2\n" }
```

## apply\_patch (experimental)

`apply_patch` is a subtool of `exec` for structured multi-file edits. Enable it explicitly:

```
{
  tools: {
    exec: {
      applyPatch: { enabled: true, workspaceOnly: true, allowModels: ["gpt-5.2"] },
    },
  },
}
```

Notes:

*   Only available for OpenAI/OpenAI Codex models.
*   Tool policy still applies; `allow: ["exec"]` implicitly allows `apply_patch`.
*   Config lives under `tools.exec.applyPatch`.
*   `tools.exec.applyPatch.workspaceOnly` defaults to `true` (workspace-contained). Set it to `false` only if you intentionally want `apply_patch` to write/delete outside the workspace directory.

---

<!-- SOURCE: https://docs.openclaw.ai/tools/llm-task -->

# LLM Task - OpenClaw

`llm-task` is an **optional plugin tool** that runs a JSON-only LLM task and returns structured output (optionally validated against JSON Schema). This is ideal for workflow engines like Lobster: you can add a single LLM step without writing custom OpenClaw code for each workflow.

## Enable the plugin

1.  Enable the plugin:

```
{
  "plugins": {
    "entries": {
      "llm-task": { "enabled": true }
    }
  }
}
```

2.  Allowlist the tool (it is registered with `optional: true`):

```
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": { "allow": ["llm-task"] }
      }
    ]
  }
}
```

## Config (optional)

```
{
  "plugins": {
    "entries": {
      "llm-task": {
        "enabled": true,
        "config": {
          "defaultProvider": "openai-codex",
          "defaultModel": "gpt-5.4",
          "defaultAuthProfileId": "main",
          "allowedModels": ["openai-codex/gpt-5.4"],
          "maxTokens": 800,
          "timeoutMs": 30000
        }
      }
    }
  }
}
```

`allowedModels` is an allowlist of `provider/model` strings. If set, any request outside the list is rejected.

*   `prompt` (string, required)
*   `input` (any, optional)
*   `schema` (object, optional JSON Schema)
*   `provider` (string, optional)
*   `model` (string, optional)
*   `authProfileId` (string, optional)
*   `temperature` (number, optional)
*   `maxTokens` (number, optional)
*   `timeoutMs` (number, optional)

## Output

Returns `details.json` containing the parsed JSON (and validates against `schema` when provided).

## Example: Lobster workflow step

```
openclaw.invoke --tool llm-task --action json --args-json '{
  "prompt": "Given the input email, return intent and draft.",
  "input": {
    "subject": "Hello",
    "body": "Can you help?"
  },
  "schema": {
    "type": "object",
    "properties": {
      "intent": { "type": "string" },
      "draft": { "type": "string" }
    },
    "required": ["intent", "draft"],
    "additionalProperties": false
  }
}'
```

## Safety notes

*   The tool is **JSON-only** and instructs the model to output only JSON (no code fences, no commentary).
*   No tools are exposed to the model for this run.
*   Treat output as untrusted unless you validate with `schema`.
*   Put approvals before any side-effecting step (send, post, exec).

---

<!-- SOURCE: https://docs.openclaw.ai/tools/exec-approvals -->

# Exec Approvals - OpenClaw

Exec approvals are the **companion app / node host guardrail** for letting a sandboxed agent run commands on a real host (`gateway` or `node`). Think of it like a safety interlock: commands are allowed only when policy + allowlist + (optional) user approval all agree. Exec approvals are **in addition** to tool policy and elevated gating (unless elevated is set to `full`, which skips approvals). Effective policy is the **stricter** of `tools.exec.*` and approvals defaults; if an approvals field is omitted, the `tools.exec` value is used. If the companion app UI is **not available**, any request that requires a prompt is resolved by the **ask fallback** (default: deny).

## Where it applies

Exec approvals are enforced locally on the execution host:

*   **gateway host** → `openclaw` process on the gateway machine
*   **node host** → node runner (macOS companion app or headless node host)

macOS split:

*   **node host service** forwards `system.run` to the **macOS app** over local IPC.
*   **macOS app** enforces approvals + executes the command in UI context.

## Settings and storage

Approvals live in a local JSON file on the execution host: `~/.openclaw/exec-approvals.json` Example schema:

```
{
  "version": 1,
  "socket": {
    "path": "~/.openclaw/exec-approvals.sock",
    "token": "base64url-token"
  },
  "defaults": {
    "security": "deny",
    "ask": "on-miss",
    "askFallback": "deny",
    "autoAllowSkills": false
  },
  "agents": {
    "main": {
      "security": "allowlist",
      "ask": "on-miss",
      "askFallback": "deny",
      "autoAllowSkills": true,
      "allowlist": [
        {
          "id": "B0C8C0B3-2C2D-4F8A-9A3C-5A4B3C2D1E0F",
          "pattern": "~/Projects/**/bin/rg",
          "lastUsedAt": 1737150000000,
          "lastUsedCommand": "rg -n TODO",
          "lastResolvedPath": "/Users/user/Projects/.../bin/rg"
        }
      ]
    }
  }
}
```

## Policy knobs

### Security (`exec.security`)

*   **deny**: block all host exec requests.
*   **allowlist**: allow only allowlisted commands.
*   **full**: allow everything (equivalent to elevated).

### Ask (`exec.ask`)

*   **off**: never prompt.
*   **on-miss**: prompt only when allowlist does not match.
*   **always**: prompt on every command.

### Ask fallback (`askFallback`)

If a prompt is required but no UI is reachable, fallback decides:

*   **deny**: block.
*   **allowlist**: allow only if allowlist matches.
*   **full**: allow.

## Allowlist (per agent)

Allowlists are **per agent**. If multiple agents exist, switch which agent you’re editing in the macOS app. Patterns are **case-insensitive glob matches**. Patterns should resolve to **binary paths** (basename-only entries are ignored). Legacy `agents.default` entries are migrated to `agents.main` on load. Examples:

*   `~/Projects/**/bin/peekaboo`
*   `~/.local/bin/*`
*   `/opt/homebrew/bin/rg`

Each allowlist entry tracks:

*   **id** stable UUID used for UI identity (optional)
*   **last used** timestamp
*   **last used command**
*   **last resolved path**

## Auto-allow skill CLIs

When **Auto-allow skill CLIs** is enabled, executables referenced by known skills are treated as allowlisted on nodes (macOS node or headless node host). This uses `skills.bins` over the Gateway RPC to fetch the skill bin list. Disable this if you want strict manual allowlists.

## Safe bins (stdin-only)

`tools.exec.safeBins` defines a small list of **stdin-only** binaries (for example `jq`) that can run in allowlist mode **without** explicit allowlist entries. Safe bins reject positional file args and path-like tokens, so they can only operate on the incoming stream. Validation is deterministic from argv shape only (no host filesystem existence checks), which prevents file-existence oracle behavior from allow/deny differences. File-oriented options are denied for default safe bins (for example `sort -o`, `sort --output`, `sort --files0-from`, `sort --compress-program`, `wc --files0-from`, `jq -f/--from-file`, `grep -f/--file`). Safe bins also enforce explicit per-binary flag policy for options that break stdin-only behavior (for example `sort -o/--output/--compress-program` and grep recursive flags). Safe bins also force argv tokens to be treated as **literal text** at execution time (no globbing and no `$VARS` expansion) for stdin-only segments, so patterns like `*` or `$HOME/...` cannot be used to smuggle file reads. Safe bins must also resolve from trusted binary directories (system defaults plus the gateway process `PATH` at startup). This blocks request-scoped PATH hijacking attempts. Shell chaining and redirections are not auto-allowed in allowlist mode. Shell chaining (`&&`, `||`, `;`) is allowed when every top-level segment satisfies the allowlist (including safe bins or skill auto-allow). Redirections remain unsupported in allowlist mode. Command substitution (`$()` / backticks) is rejected during allowlist parsing, including inside double quotes; use single quotes if you need literal `$()` text. On macOS companion-app approvals, raw shell text containing shell control or expansion syntax (`&&`, `||`, `;`, `|`, `` ` ``, `$`, `<`, `>`, `(`, `)`) is treated as an allowlist miss unless the shell binary itself is allowlisted. Default safe bins: `jq`, `cut`, `uniq`, `head`, `tail`, `tr`, `wc`. `grep` and `sort` are not in the default list. If you opt in, keep explicit allowlist entries for their non-stdin workflows. For `grep` in safe-bin mode, provide the pattern with `-e`/`--regexp`; positional pattern form is rejected so file operands cannot be smuggled as ambiguous positionals.

## Control UI editing

Use the **Control UI → Nodes → Exec approvals** card to edit defaults, per‑agent overrides, and allowlists. Pick a scope (Defaults or an agent), tweak the policy, add/remove allowlist patterns, then **Save**. The UI shows **last used** metadata per pattern so you can keep the list tidy. The target selector chooses **Gateway** (local approvals) or a **Node**. Nodes must advertise `system.execApprovals.get/set` (macOS app or headless node host). If a node does not advertise exec approvals yet, edit its local `~/.openclaw/exec-approvals.json` directly. CLI: `openclaw approvals` supports gateway or node editing (see [Approvals CLI](https://docs.openclaw.ai/cli/approvals)).

## Approval flow

When a prompt is required, the gateway broadcasts `exec.approval.requested` to operator clients. The Control UI and macOS app resolve it via `exec.approval.resolve`, then the gateway forwards the approved request to the node host. When approvals are required, the exec tool returns immediately with an approval id. Use that id to correlate later system events (`Exec finished` / `Exec denied`). If no decision arrives before the timeout, the request is treated as an approval timeout and surfaced as a denial reason. The confirmation dialog includes:

*   command + args
*   cwd
*   agent id
*   resolved executable path
*   host + policy metadata

Actions:

*   **Allow once** → run now
*   **Always allow** → add to allowlist + run
*   **Deny** → block

## Approval forwarding to chat channels

You can forward exec approval prompts to any chat channel (including plugin channels) and approve them with `/approve`. This uses the normal outbound delivery pipeline. Config:

```
{
  approvals: {
    exec: {
      enabled: true,
      mode: "session", // "session" | "targets" | "both"
      agentFilter: ["main"],
      sessionFilter: ["discord"], // substring or regex
      targets: [
        { channel: "slack", to: "U12345678" },
        { channel: "telegram", to: "123456789" },
      ],
    },
  },
}
```

Reply in chat:

```
/approve <id> allow-once
/approve <id> allow-always
/approve <id> deny
```

### macOS IPC flow

```
Gateway -> Node Service (WS)
                 |  IPC (UDS + token + HMAC + TTL)
                 v
             Mac App (UI + approvals + system.run)
```

Security notes:

*   Unix socket mode `0600`, token stored in `exec-approvals.json`.
*   Same-UID peer check.
*   Challenge/response (nonce + HMAC token + request hash) + short TTL.

## System events

Exec lifecycle is surfaced as system messages:

*   `Exec running` (only if the command exceeds the running notice threshold)
*   `Exec finished`
*   `Exec denied`

These are posted to the agent’s session after the node reports the event. Gateway-host exec approvals emit the same lifecycle events when the command finishes (and optionally when running longer than the threshold). Approval-gated execs reuse the approval id as the `runId` in these messages for easy correlation.

## Implications

*   **full** is powerful; prefer allowlists when possible.
*   **ask** keeps you in the loop while still allowing fast approvals.
*   Per-agent allowlists prevent one agent’s approvals from leaking into others.
*   Approvals only apply to host exec requests from **authorized senders**. Unauthorized senders cannot issue `/exec`.
*   `/exec security=full` is a session-level convenience for authorized operators and skips approvals by design. To hard-block host exec, set approvals security to `deny` or deny the `exec` tool via tool policy.

Related:

*   [Exec tool](https://docs.openclaw.ai/tools/exec)
*   [Elevated mode](https://docs.openclaw.ai/tools/elevated)
*   [Skills](https://docs.openclaw.ai/tools/skills)

---

<!-- SOURCE: https://docs.openclaw.ai/tools/loop-detection -->

# Tool-loop detection - OpenClaw

OpenClaw can keep agents from getting stuck in repeated tool-call patterns. The guard is **disabled by default**. Enable it only where needed, because it can block legitimate repeated calls with strict settings.

## Why this exists

*   Detect repetitive sequences that do not make progress.
*   Detect high-frequency no-result loops (same tool, same inputs, repeated errors).
*   Detect specific repeated-call patterns for known polling tools.

## Configuration block

Global defaults:

```
{
  tools: {
    loopDetection: {
      enabled: false,
      historySize: 30,
      warningThreshold: 10,
      criticalThreshold: 20,
      globalCircuitBreakerThreshold: 30,
      detectors: {
        genericRepeat: true,
        knownPollNoProgress: true,
        pingPong: true,
      },
    },
  },
}
```

Per-agent override (optional):

```
{
  agents: {
    list: [
      {
        id: "safe-runner",
        tools: {
          loopDetection: {
            enabled: true,
            warningThreshold: 8,
            criticalThreshold: 16,
          },
        },
      },
    ],
  },
}
```

### Field behavior

*   `enabled`: Master switch. `false` means no loop detection is performed.
*   `historySize`: number of recent tool calls kept for analysis.
*   `warningThreshold`: threshold before classifying a pattern as warning-only.
*   `criticalThreshold`: threshold for blocking repetitive loop patterns.
*   `globalCircuitBreakerThreshold`: global no-progress breaker threshold.
*   `detectors.genericRepeat`: detects repeated same-tool + same-params patterns.
*   `detectors.knownPollNoProgress`: detects known polling-like patterns with no state change.
*   `detectors.pingPong`: detects alternating ping-pong patterns.

## Recommended setup

*   Start with `enabled: true`, defaults unchanged.
*   Keep thresholds ordered as `warningThreshold < criticalThreshold < globalCircuitBreakerThreshold`.
*   If false positives occur:
    *   raise `warningThreshold` and/or `criticalThreshold`
    *   (optionally) raise `globalCircuitBreakerThreshold`
    *   disable only the detector causing issues
    *   reduce `historySize` for less strict historical context

## Logs and expected behavior

When a loop is detected, OpenClaw reports a loop event and blocks or dampens the next tool-cycle depending on severity. This protects users from runaway token spend and lockups while preserving normal tool access.

*   Prefer warning and temporary suppression first.
*   Escalate only when repeated evidence accumulates.

## Notes

*   `tools.loopDetection` is merged with agent-level overrides.
*   Per-agent config fully overrides or extends global values.
*   If no config exists, guardrails stay off.

---

<!-- SOURCE: https://docs.openclaw.ai/tools/thinking -->

# Thinking Levels - OpenClaw

## Thinking Levels (/think directives)

## What it does

*   Inline directive in any inbound body: `/t <level>`, `/think:<level>`, or `/thinking <level>`.
*   Levels (aliases): `off | minimal | low | medium | high | xhigh | adaptive`
    *   minimal → “think”
    *   low → “think hard”
    *   medium → “think harder”
    *   high → “ultrathink” (max budget)
    *   xhigh → “ultrathink+” (GPT-5.2 + Codex models only)
    *   adaptive → provider-managed adaptive reasoning budget (supported for Anthropic Claude 4.6 model family)
    *   `x-high`, `x_high`, `extra-high`, `extra high`, and `extra_high` map to `xhigh`.
    *   `highest`, `max` map to `high`.
*   Provider notes:
    *   Anthropic Claude 4.6 models default to `adaptive` when no explicit thinking level is set.
    *   Z.AI (`zai/*`) only supports binary thinking (`on`/`off`). Any non-`off` level is treated as `on` (mapped to `low`).
    *   Moonshot (`moonshot/*`) maps `/think off` to `thinking: { type: "disabled" }` and any non-`off` level to `thinking: { type: "enabled" }`. When thinking is enabled, Moonshot only accepts `tool_choice` `auto|none`; OpenClaw normalizes incompatible values to `auto`.

## Resolution order

1.  Inline directive on the message (applies only to that message).
2.  Session override (set by sending a directive-only message).
3.  Global default (`agents.defaults.thinkingDefault` in config).
4.  Fallback: `adaptive` for Anthropic Claude 4.6 models, `low` for other reasoning-capable models, `off` otherwise.

## Setting a session default

*   Send a message that is **only** the directive (whitespace allowed), e.g. `/think:medium` or `/t high`.
*   That sticks for the current session (per-sender by default); cleared by `/think:off` or session idle reset.
*   Confirmation reply is sent (`Thinking level set to high.` / `Thinking disabled.`). If the level is invalid (e.g. `/thinking big`), the command is rejected with a hint and the session state is left unchanged.
*   Send `/think` (or `/think:`) with no argument to see the current thinking level.

## Application by agent

*   **Embedded Pi**: the resolved level is passed to the in-process Pi agent runtime.

## Verbose directives (/verbose or /v)

*   Levels: `on` (minimal) | `full` | `off` (default).
*   Directive-only message toggles session verbose and replies `Verbose logging enabled.` / `Verbose logging disabled.`; invalid levels return a hint without changing state.
*   `/verbose off` stores an explicit session override; clear it via the Sessions UI by choosing `inherit`.
*   Inline directive affects only that message; session/global defaults apply otherwise.
*   Send `/verbose` (or `/verbose:`) with no argument to see the current verbose level.
*   When verbose is on, agents that emit structured tool results (Pi, other JSON agents) send each tool call back as its own metadata-only message, prefixed with `<emoji> <tool-name>: <arg>` when available (path/command). These tool summaries are sent as soon as each tool starts (separate bubbles), not as streaming deltas.
*   Tool failure summaries remain visible in normal mode, but raw error detail suffixes are hidden unless verbose is `on` or `full`.
*   When verbose is `full`, tool outputs are also forwarded after completion (separate bubble, truncated to a safe length). If you toggle `/verbose on|full|off` while a run is in-flight, subsequent tool bubbles honor the new setting.

## Reasoning visibility (/reasoning)

*   Levels: `on|off|stream`.
*   Directive-only message toggles whether thinking blocks are shown in replies.
*   When enabled, reasoning is sent as a **separate message** prefixed with `Reasoning:`.
*   `stream` (Telegram only): streams reasoning into the Telegram draft bubble while the reply is generating, then sends the final answer without reasoning.
*   Alias: `/reason`.
*   Send `/reasoning` (or `/reasoning:`) with no argument to see the current reasoning level.

*   Elevated mode docs live in [Elevated mode](https://docs.openclaw.ai/tools/elevated).

## Heartbeats

*   Heartbeat probe body is the configured heartbeat prompt (default: `Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`). Inline directives in a heartbeat message apply as usual (but avoid changing session defaults from heartbeats).
*   Heartbeat delivery defaults to the final payload only. To also send the separate `Reasoning:` message (when available), set `agents.defaults.heartbeat.includeReasoning: true` or per-agent `agents.list[].heartbeat.includeReasoning: true`.

## Web chat UI

*   The web chat thinking selector mirrors the session’s stored level from the inbound session store/config when the page loads.
*   Picking another level applies only to the next message (`thinkingOnce`); after sending, the selector snaps back to the stored session level.
*   To change the session default, send a `/think:<level>` directive (as before); the selector will reflect it after the next reload.

---

<!-- SOURCE: https://docs.openclaw.ai/tools/lobster -->

# Lobster - OpenClaw

Lobster is a workflow shell that lets OpenClaw run multi-step tool sequences as a single, deterministic operation with explicit approval checkpoints.

## Hook

Your assistant can build the tools that manage itself. Ask for a workflow, and 30 minutes later you have a CLI plus pipelines that run as one call. Lobster is the missing piece: deterministic pipelines, explicit approvals, and resumable state.

## Why

Today, complex workflows require many back-and-forth tool calls. Each call costs tokens, and the LLM has to orchestrate every step. Lobster moves that orchestration into a typed runtime:

*   **One call instead of many**: OpenClaw runs one Lobster tool call and gets a structured result.
*   **Approvals built in**: Side effects (send email, post comment) halt the workflow until explicitly approved.
*   **Resumable**: Halted workflows return a token; approve and resume without re-running everything.

## Why a DSL instead of plain programs?

Lobster is intentionally small. The goal is not “a new language,” it’s a predictable, AI-friendly pipeline spec with first-class approvals and resume tokens.

*   **Approve/resume is built in**: A normal program can prompt a human, but it can’t _pause and resume_ with a durable token without you inventing that runtime yourself.
*   **Determinism + auditability**: Pipelines are data, so they’re easy to log, diff, replay, and review.
*   **Constrained surface for AI**: A tiny grammar + JSON piping reduces “creative” code paths and makes validation realistic.
*   **Safety policy baked in**: Timeouts, output caps, sandbox checks, and allowlists are enforced by the runtime, not each script.
*   **Still programmable**: Each step can call any CLI or script. If you want JS/TS, generate `.lobster` files from code.

## How it works

OpenClaw launches the local `lobster` CLI in **tool mode** and parses a JSON envelope from stdout. If the pipeline pauses for approval, the tool returns a `resumeToken` so you can continue later.

## Pattern: small CLI + JSON pipes + approvals

Build tiny commands that speak JSON, then chain them into a single Lobster call. (Example command names below — swap in your own.)

```
inbox list --json
inbox categorize --json
inbox apply --json
```

```
{
  "action": "run",
  "pipeline": "exec --json --shell 'inbox list --json' | exec --stdin json --shell 'inbox categorize --json' | exec --stdin json --shell 'inbox apply --json' | approve --preview-from-stdin --limit 5 --prompt 'Apply changes?'",
  "timeoutMs": 30000
}
```

If the pipeline requests approval, resume with the token:

```
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

AI triggers the workflow; Lobster executes the steps. Approval gates keep side effects explicit and auditable. Example: map input items into tool calls:

```
gog.gmail.search --query 'newer_than:1d' \
  | openclaw.invoke --tool message --action send --each --item-key message --args-json '{"provider":"telegram","to":"..."}'
```

## JSON-only LLM steps (llm-task)

For workflows that need a **structured LLM step**, enable the optional `llm-task` plugin tool and call it from Lobster. This keeps the workflow deterministic while still letting you classify/summarize/draft with a model. Enable the tool:

```
{
  "plugins": {
    "entries": {
      "llm-task": { "enabled": true }
    }
  },
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": { "allow": ["llm-task"] }
      }
    ]
  }
}
```

Use it in a pipeline:

```
openclaw.invoke --tool llm-task --action json --args-json '{
  "prompt": "Given the input email, return intent and draft.",
  "input": { "subject": "Hello", "body": "Can you help?" },
  "schema": {
    "type": "object",
    "properties": {
      "intent": { "type": "string" },
      "draft": { "type": "string" }
    },
    "required": ["intent", "draft"],
    "additionalProperties": false
  }
}'
```

See [LLM Task](https://docs.openclaw.ai/tools/llm-task) for details and configuration options.

## Workflow files (.lobster)

Lobster can run YAML/JSON workflow files with `name`, `args`, `steps`, `env`, `condition`, and `approval` fields. In OpenClaw tool calls, set `pipeline` to the file path.

```
name: inbox-triage
args:
  tag:
    default: "family"
steps:
  - id: collect
    command: inbox list --json
  - id: categorize
    command: inbox categorize --json
    stdin: $collect.stdout
  - id: approve
    command: inbox apply --approve
    stdin: $categorize.stdout
    approval: required
  - id: execute
    command: inbox apply --execute
    stdin: $categorize.stdout
    condition: $approve.approved
```

Notes:

*   `stdin: $step.stdout` and `stdin: $step.json` pass a prior step’s output.
*   `condition` (or `when`) can gate steps on `$step.approved`.

## Install Lobster

Install the Lobster CLI on the **same host** that runs the OpenClaw Gateway (see the [Lobster repo](https://github.com/openclaw/lobster)), and ensure `lobster` is on `PATH`.

Lobster is an **optional** plugin tool (not enabled by default). Recommended (additive, safe):

```
{
  "tools": {
    "alsoAllow": ["lobster"]
  }
}
```

Or per-agent:

```
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": {
          "alsoAllow": ["lobster"]
        }
      }
    ]
  }
}
```

Avoid using `tools.allow: ["lobster"]` unless you intend to run in restrictive allowlist mode. Note: allowlists are opt-in for optional plugins. If your allowlist only names plugin tools (like `lobster`), OpenClaw keeps core tools enabled. To restrict core tools, include the core tools or groups you want in the allowlist too.

## Example: Email triage

Without Lobster:

```
User: "Check my email and draft replies"
→ openclaw calls gmail.list
→ LLM summarizes
→ User: "draft replies to #2 and #5"
→ LLM drafts
→ User: "send #2"
→ openclaw calls gmail.send
(repeat daily, no memory of what was triaged)
```

With Lobster:

```
{
  "action": "run",
  "pipeline": "email.triage --limit 20",
  "timeoutMs": 30000
}
```

Returns a JSON envelope (truncated):

```
{
  "ok": true,
  "status": "needs_approval",
  "output": [{ "summary": "5 need replies, 2 need action" }],
  "requiresApproval": {
    "type": "approval_request",
    "prompt": "Send 2 draft replies?",
    "items": [],
    "resumeToken": "..."
  }
}
```

User approves → resume:

```
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

One workflow. Deterministic. Safe.

### `run`

Run a pipeline in tool mode.

```
{
  "action": "run",
  "pipeline": "gog.gmail.search --query 'newer_than:1d' | email.triage",
  "cwd": "workspace",
  "timeoutMs": 30000,
  "maxStdoutBytes": 512000
}
```

Run a workflow file with args:

```
{
  "action": "run",
  "pipeline": "/path/to/inbox-triage.lobster",
  "argsJson": "{\"tag\":\"family\"}"
}
```

### `resume`

Continue a halted workflow after approval.

```
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

### Optional inputs

*   `cwd`: Relative working directory for the pipeline (must stay within the current process working directory).
*   `timeoutMs`: Kill the subprocess if it exceeds this duration (default: 20000).
*   `maxStdoutBytes`: Kill the subprocess if stdout exceeds this size (default: 512000).
*   `argsJson`: JSON string passed to `lobster run --args-json` (workflow files only).

## Output envelope

Lobster returns a JSON envelope with one of three statuses:

*   `ok` → finished successfully
*   `needs_approval` → paused; `requiresApproval.resumeToken` is required to resume
*   `cancelled` → explicitly denied or cancelled

The tool surfaces the envelope in both `content` (pretty JSON) and `details` (raw object).

## Approvals

If `requiresApproval` is present, inspect the prompt and decide:

*   `approve: true` → resume and continue side effects
*   `approve: false` → cancel and finalize the workflow

Use `approve --preview-from-stdin --limit N` to attach a JSON preview to approval requests without custom jq/heredoc glue. Resume tokens are now compact: Lobster stores workflow resume state under its state dir and hands back a small token key.

## OpenProse

OpenProse pairs well with Lobster: use `/prose` to orchestrate multi-agent prep, then run a Lobster pipeline for deterministic approvals. If a Prose program needs Lobster, allow the `lobster` tool for sub-agents via `tools.subagents.tools`. See [OpenProse](https://docs.openclaw.ai/prose).

## Safety

*   **Local subprocess only** — no network calls from the plugin itself.
*   **No secrets** — Lobster doesn’t manage OAuth; it calls OpenClaw tools that do.
*   **Sandbox-aware** — disabled when the tool context is sandboxed.
*   **Hardened** — fixed executable name (`lobster`) on `PATH`; timeouts and output caps enforced.

## Troubleshooting

*   **`lobster subprocess timed out`** → increase `timeoutMs`, or split a long pipeline.
*   **`lobster output exceeded maxStdoutBytes`** → raise `maxStdoutBytes` or reduce output size.
*   **`lobster returned invalid JSON`** → ensure the pipeline runs in tool mode and prints only JSON.
*   **`lobster failed (code …)`** → run the same pipeline in a terminal to inspect stderr.

## Learn more

*   [Plugins](https://docs.openclaw.ai/tools/plugin)
*   [Plugin tool authoring](https://docs.openclaw.ai/plugins/agent-tools)

One public example: a “second brain” CLI + Lobster pipelines that manage three Markdown vaults (personal, partner, shared). The CLI emits JSON for stats, inbox listings, and stale scans; Lobster chains those commands into workflows like `weekly-review`, `inbox-triage`, `memory-consolidation`, and `shared-task-sync`, each with approval gates. AI handles judgment (categorization) when available and falls back to deterministic rules when not.

*   Thread: [https://x.com/plattenschieber/status/2014508656335770033](https://x.com/plattenschieber/status/2014508656335770033)
*   Repo: [https://github.com/bloomedai/brain-cli](https://github.com/bloomedai/brain-cli)

---

<!-- SOURCE: https://docs.openclaw.ai/tools/browser -->

# Browser (OpenClaw-managed) - OpenClaw

OpenClaw can run a **dedicated Chrome/Brave/Edge/Chromium profile** that the agent controls. It is isolated from your personal browser and is managed through a small local control service inside the Gateway (loopback only). Beginner view:

*   Think of it as a **separate, agent-only browser**.
*   The `openclaw` profile does **not** touch your personal browser profile.
*   The agent can **open tabs, read pages, click, and type** in a safe lane.
*   The default `chrome` profile uses the **system default Chromium browser** via the extension relay; switch to `openclaw` for the isolated managed browser.

## What you get

*   A separate browser profile named **openclaw** (orange accent by default).
*   Deterministic tab control (list/open/focus/close).
*   Agent actions (click/type/drag/select), snapshots, screenshots, PDFs.
*   Optional multi-profile support (`openclaw`, `work`, `remote`, …).

This browser is **not** your daily driver. It is a safe, isolated surface for agent automation and verification.

## Quick start

```
openclaw browser --browser-profile openclaw status
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

If you get “Browser disabled”, enable it in config (see below) and restart the Gateway.

## Profiles: `openclaw` vs `chrome`

*   `openclaw`: managed, isolated browser (no extension required).
*   `chrome`: extension relay to your **system browser** (requires the OpenClaw extension to be attached to a tab).

Set `browser.defaultProfile: "openclaw"` if you want managed mode by default.

## Configuration

Browser settings live in `~/.openclaw/openclaw.json`.

```
{
  browser: {
    enabled: true, // default: true
    ssrfPolicy: {
      dangerouslyAllowPrivateNetwork: true, // default trusted-network mode
      // allowPrivateNetwork: true, // legacy alias
      // hostnameAllowlist: ["*.example.com", "example.com"],
      // allowedHostnames: ["localhost"],
    },
    // cdpUrl: "http://127.0.0.1:18792", // legacy single-profile override
    remoteCdpTimeoutMs: 1500, // remote CDP HTTP timeout (ms)
    remoteCdpHandshakeTimeoutMs: 3000, // remote CDP WebSocket handshake timeout (ms)
    defaultProfile: "chrome",
    color: "#FF4500",
    headless: false,
    noSandbox: false,
    attachOnly: false,
    executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },
      work: { cdpPort: 18801, color: "#0066CC" },
      remote: { cdpUrl: "http://10.0.0.42:9222", color: "#00AA00" },
    },
  },
}
```

Notes:

*   The browser control service binds to loopback on a port derived from `gateway.port` (default: `18791`, which is gateway + 2). The relay uses the next port (`18792`).
*   If you override the Gateway port (`gateway.port` or `OPENCLAW_GATEWAY_PORT`), the derived browser ports shift to stay in the same “family”.
*   `cdpUrl` defaults to the relay port when unset.
*   `remoteCdpTimeoutMs` applies to remote (non-loopback) CDP reachability checks.
*   `remoteCdpHandshakeTimeoutMs` applies to remote CDP WebSocket reachability checks.
*   Browser navigation/open-tab is SSRF-guarded before navigation and best-effort re-checked on final `http(s)` URL after navigation.
*   `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork` defaults to `true` (trusted-network model). Set it to `false` for strict public-only browsing.
*   `browser.ssrfPolicy.allowPrivateNetwork` remains supported as a legacy alias for compatibility.
*   `attachOnly: true` means “never launch a local browser; only attach if it is already running.”
*   `color` + per-profile `color` tint the browser UI so you can see which profile is active.
*   Default profile is `openclaw` (OpenClaw-managed standalone browser). Use `defaultProfile: "chrome"` to opt into the Chrome extension relay.
*   Auto-detect order: system default browser if Chromium-based; otherwise Chrome → Brave → Edge → Chromium → Chrome Canary.
*   Local `openclaw` profiles auto-assign `cdpPort`/`cdpUrl` — set those only for remote CDP.

## Use Brave (or another Chromium-based browser)

If your **system default** browser is Chromium-based (Chrome/Brave/Edge/etc), OpenClaw uses it automatically. Set `browser.executablePath` to override auto-detection: CLI example:

```
openclaw config set browser.executablePath "/usr/bin/google-chrome"
```

```
// macOS
{
  browser: {
    executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
  }
}

// Windows
{
  browser: {
    executablePath: "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
  }
}

// Linux
{
  browser: {
    executablePath: "/usr/bin/brave-browser"
  }
}
```

## Local vs remote control

*   **Local control (default):** the Gateway starts the loopback control service and can launch a local browser.
*   **Remote control (node host):** run a node host on the machine that has the browser; the Gateway proxies browser actions to it.
*   **Remote CDP:** set `browser.profiles.<name>.cdpUrl` (or `browser.cdpUrl`) to attach to a remote Chromium-based browser. In this case, OpenClaw will not launch a local browser.

Remote CDP URLs can include auth:

*   Query tokens (e.g., `https://provider.example?token=<token>`)
*   HTTP Basic auth (e.g., `https://user:pass@provider.example`)

OpenClaw preserves the auth when calling `/json/*` endpoints and when connecting to the CDP WebSocket. Prefer environment variables or secrets managers for tokens instead of committing them to config files.

## Node browser proxy (zero-config default)

If you run a **node host** on the machine that has your browser, OpenClaw can auto-route browser tool calls to that node without any extra browser config. This is the default path for remote gateways. Notes:

*   The node host exposes its local browser control server via a **proxy command**.
*   Profiles come from the node’s own `browser.profiles` config (same as local).
*   Disable if you don’t want it:
    *   On the node: `nodeHost.browserProxy.enabled=false`
    *   On the gateway: `gateway.nodes.browser.mode="off"`

## Browserless (hosted remote CDP)

[Browserless](https://browserless.io/) is a hosted Chromium service that exposes CDP endpoints over HTTPS. You can point a OpenClaw browser profile at a Browserless region endpoint and authenticate with your API key. Example:

```
{
  browser: {
    enabled: true,
    defaultProfile: "browserless",
    remoteCdpTimeoutMs: 2000,
    remoteCdpHandshakeTimeoutMs: 4000,
    profiles: {
      browserless: {
        cdpUrl: "https://production-sfo.browserless.io?token=<BROWSERLESS_API_KEY>",
        color: "#00AA00",
      },
    },
  },
}
```

Notes:

*   Replace `<BROWSERLESS_API_KEY>` with your real Browserless token.
*   Choose the region endpoint that matches your Browserless account (see their docs).

## Direct WebSocket CDP providers

Some hosted browser services expose a **direct WebSocket** endpoint rather than the standard HTTP-based CDP discovery (`/json/version`). OpenClaw supports both:

*   **HTTP(S) endpoints** (e.g. Browserless) — OpenClaw calls `/json/version` to discover the WebSocket debugger URL, then connects.
*   **WebSocket endpoints** (`ws://` / `wss://`) — OpenClaw connects directly, skipping `/json/version`. Use this for services like [Browserbase](https://www.browserbase.com/) or any provider that hands you a WebSocket URL.

### Browserbase

[Browserbase](https://www.browserbase.com/) is a cloud platform for running headless browsers with built-in CAPTCHA solving, stealth mode, and residential proxies.

```
{
  browser: {
    enabled: true,
    defaultProfile: "browserbase",
    remoteCdpTimeoutMs: 3000,
    remoteCdpHandshakeTimeoutMs: 5000,
    profiles: {
      browserbase: {
        cdpUrl: "wss://connect.browserbase.com?apiKey=<BROWSERBASE_API_KEY>",
        color: "#F97316",
      },
    },
  },
}
```

Notes:

*   [Sign up](https://www.browserbase.com/sign-up) and copy your **API Key** from the [Overview dashboard](https://www.browserbase.com/overview).
*   Replace `<BROWSERBASE_API_KEY>` with your real Browserbase API key.
*   Browserbase auto-creates a browser session on WebSocket connect, so no manual session creation step is needed.
*   The free tier allows one concurrent session and one browser hour per month. See [pricing](https://www.browserbase.com/pricing) for paid plan limits.
*   See the [Browserbase docs](https://docs.browserbase.com/) for full API reference, SDK guides, and integration examples.

## Security

Key ideas:

*   Browser control is loopback-only; access flows through the Gateway’s auth or node pairing.
*   If browser control is enabled and no auth is configured, OpenClaw auto-generates `gateway.auth.token` on startup and persists it to config.
*   Keep the Gateway and any node hosts on a private network (Tailscale); avoid public exposure.
*   Treat remote CDP URLs/tokens as secrets; prefer env vars or a secrets manager.

Remote CDP tips:

*   Prefer encrypted endpoints (HTTPS or WSS) and short-lived tokens where possible.
*   Avoid embedding long-lived tokens directly in config files.

## Profiles (multi-browser)

OpenClaw supports multiple named profiles (routing configs). Profiles can be:

*   **openclaw-managed**: a dedicated Chromium-based browser instance with its own user data directory + CDP port
*   **remote**: an explicit CDP URL (Chromium-based browser running elsewhere)
*   **extension relay**: your existing Chrome tab(s) via the local relay + Chrome extension

Defaults:

*   The `openclaw` profile is auto-created if missing.
*   The `chrome` profile is built-in for the Chrome extension relay (points at `http://127.0.0.1:18792` by default).
*   Local CDP ports allocate from **18800–18899** by default.
*   Deleting a profile moves its local data directory to Trash.

All control endpoints accept `?profile=<name>`; the CLI uses `--browser-profile`.

## Chrome extension relay (use your existing Chrome)

OpenClaw can also drive **your existing Chrome tabs** (no separate “openclaw” Chrome instance) via a local CDP relay + a Chrome extension. Full guide: [Chrome extension](https://docs.openclaw.ai/tools/chrome-extension) Flow:

*   The Gateway runs locally (same machine) or a node host runs on the browser machine.
*   A local **relay server** listens at a loopback `cdpUrl` (default: `http://127.0.0.1:18792`).
*   You click the **OpenClaw Browser Relay** extension icon on a tab to attach (it does not auto-attach).
*   The agent controls that tab via the normal `browser` tool, by selecting the right profile.

If the Gateway runs elsewhere, run a node host on the browser machine so the Gateway can proxy browser actions.

### Sandboxed sessions

If the agent session is sandboxed, the `browser` tool may default to `target="sandbox"` (sandbox browser). Chrome extension relay takeover requires host browser control, so either:

*   run the session unsandboxed, or
*   set `agents.defaults.sandbox.browser.allowHostControl: true` and use `target="host"` when calling the tool.

### Setup

1.  Load the extension (dev/unpacked):

```
openclaw browser extension install
```

*   Chrome → `chrome://extensions` → enable “Developer mode”
*   “Load unpacked” → select the directory printed by `openclaw browser extension path`
*   Pin the extension, then click it on the tab you want to control (badge shows `ON`).

2.  Use it:

*   CLI: `openclaw browser --browser-profile chrome tabs`
*   Agent tool: `browser` with `profile="chrome"`

Optional: if you want a different name or relay port, create your own profile:

```
openclaw browser create-profile \
  --name my-chrome \
  --driver extension \
  --cdp-url http://127.0.0.1:18792 \
  --color "#00AA00"
```

Notes:

*   This mode relies on Playwright-on-CDP for most operations (screenshots/snapshots/actions).
*   Detach by clicking the extension icon again.
*   Leave the relay loopback-only by default. If the relay must be reachable from a different network namespace (for example Gateway in WSL2, Chrome on Windows), set `browser.relayBindHost` to an explicit bind address such as `0.0.0.0` while keeping the surrounding network private and authenticated.

WSL2 / cross-namespace example:

```
{
  browser: {
    enabled: true,
    relayBindHost: "0.0.0.0",
    defaultProfile: "chrome",
  },
}
```

## Isolation guarantees

*   **Dedicated user data dir**: never touches your personal browser profile.
*   **Dedicated ports**: avoids `9222` to prevent collisions with dev workflows.
*   **Deterministic tab control**: target tabs by `targetId`, not “last tab”.

## Browser selection

When launching locally, OpenClaw picks the first available:

1.  Chrome
2.  Brave
3.  Edge
4.  Chromium
5.  Chrome Canary

You can override with `browser.executablePath`. Platforms:

*   macOS: checks `/Applications` and `~/Applications`.
*   Linux: looks for `google-chrome`, `brave`, `microsoft-edge`, `chromium`, etc.
*   Windows: checks common install locations.

## Control API (optional)

For local integrations only, the Gateway exposes a small loopback HTTP API:

*   Status/start/stop: `GET /`, `POST /start`, `POST /stop`
*   Tabs: `GET /tabs`, `POST /tabs/open`, `POST /tabs/focus`, `DELETE /tabs/:targetId`
*   Snapshot/screenshot: `GET /snapshot`, `POST /screenshot`
*   Actions: `POST /navigate`, `POST /act`
*   Hooks: `POST /hooks/file-chooser`, `POST /hooks/dialog`
*   Downloads: `POST /download`, `POST /wait/download`
*   Debugging: `GET /console`, `POST /pdf`
*   Debugging: `GET /errors`, `GET /requests`, `POST /trace/start`, `POST /trace/stop`, `POST /highlight`
*   Network: `POST /response/body`
*   State: `GET /cookies`, `POST /cookies/set`, `POST /cookies/clear`
*   State: `GET /storage/:kind`, `POST /storage/:kind/set`, `POST /storage/:kind/clear`
*   Settings: `POST /set/offline`, `POST /set/headers`, `POST /set/credentials`, `POST /set/geolocation`, `POST /set/media`, `POST /set/timezone`, `POST /set/locale`, `POST /set/device`

All endpoints accept `?profile=<name>`. If gateway auth is configured, browser HTTP routes require auth too:

*   `Authorization: Bearer <gateway token>`
*   `x-openclaw-password: <gateway password>` or HTTP Basic auth with that password

### Playwright requirement

Some features (navigate/act/AI snapshot/role snapshot, element screenshots, PDF) require Playwright. If Playwright isn’t installed, those endpoints return a clear 501 error. ARIA snapshots and basic screenshots still work for openclaw-managed Chrome. For the Chrome extension relay driver, ARIA snapshots and screenshots require Playwright. If you see `Playwright is not available in this gateway build`, install the full Playwright package (not `playwright-core`) and restart the gateway, or reinstall OpenClaw with browser support.

#### Docker Playwright install

If your Gateway runs in Docker, avoid `npx playwright` (npm override conflicts). Use the bundled CLI instead:

```
docker compose run --rm openclaw-cli \
  node /app/node_modules/playwright-core/cli.js install chromium
```

To persist browser downloads, set `PLAYWRIGHT_BROWSERS_PATH` (for example, `/home/node/.cache/ms-playwright`) and make sure `/home/node` is persisted via `OPENCLAW_HOME_VOLUME` or a bind mount. See [Docker](https://docs.openclaw.ai/install/docker).

## How it works (internal)

High-level flow:

*   A small **control server** accepts HTTP requests.
*   It connects to Chromium-based browsers (Chrome/Brave/Edge/Chromium) via **CDP**.
*   For advanced actions (click/type/snapshot/PDF), it uses **Playwright** on top of CDP.
*   When Playwright is missing, only non-Playwright operations are available.

This design keeps the agent on a stable, deterministic interface while letting you swap local/remote browsers and profiles.

## CLI quick reference

All commands accept `--browser-profile <name>` to target a specific profile. All commands also accept `--json` for machine-readable output (stable payloads). Basics:

*   `openclaw browser status`
*   `openclaw browser start`
*   `openclaw browser stop`
*   `openclaw browser tabs`
*   `openclaw browser tab`
*   `openclaw browser tab new`
*   `openclaw browser tab select 2`
*   `openclaw browser tab close 2`
*   `openclaw browser open https://example.com`
*   `openclaw browser focus abcd1234`
*   `openclaw browser close abcd1234`

Inspection:

*   `openclaw browser screenshot`
*   `openclaw browser screenshot --full-page`
*   `openclaw browser screenshot --ref 12`
*   `openclaw browser screenshot --ref e12`
*   `openclaw browser snapshot`
*   `openclaw browser snapshot --format aria --limit 200`
*   `openclaw browser snapshot --interactive --compact --depth 6`
*   `openclaw browser snapshot --efficient`
*   `openclaw browser snapshot --labels`
*   `openclaw browser snapshot --selector "#main" --interactive`
*   `openclaw browser snapshot --frame "iframe#main" --interactive`
*   `openclaw browser console --level error`
*   `openclaw browser errors --clear`
*   `openclaw browser requests --filter api --clear`
*   `openclaw browser pdf`
*   `openclaw browser responsebody "**/api" --max-chars 5000`

Actions:

*   `openclaw browser navigate https://example.com`
*   `openclaw browser resize 1280 720`
*   `openclaw browser click 12 --double`
*   `openclaw browser click e12 --double`
*   `openclaw browser type 23 "hello" --submit`
*   `openclaw browser press Enter`
*   `openclaw browser hover 44`
*   `openclaw browser scrollintoview e12`
*   `openclaw browser drag 10 11`
*   `openclaw browser select 9 OptionA OptionB`
*   `openclaw browser download e12 report.pdf`
*   `openclaw browser waitfordownload report.pdf`
*   `openclaw browser upload /tmp/openclaw/uploads/file.pdf`
*   `openclaw browser fill --fields '[{"ref":"1","type":"text","value":"Ada"}]'`
*   `openclaw browser dialog --accept`
*   `openclaw browser wait --text "Done"`
*   `openclaw browser wait "#main" --url "**/dash" --load networkidle --fn "window.ready===true"`
*   `openclaw browser evaluate --fn '(el) => el.textContent' --ref 7`
*   `openclaw browser highlight e12`
*   `openclaw browser trace start`
*   `openclaw browser trace stop`

State:

*   `openclaw browser cookies`
*   `openclaw browser cookies set session abc123 --url "https://example.com"`
*   `openclaw browser cookies clear`
*   `openclaw browser storage local get`
*   `openclaw browser storage local set theme dark`
*   `openclaw browser storage session clear`
*   `openclaw browser set offline on`
*   `openclaw browser set headers --headers-json '{"X-Debug":"1"}'`
*   `openclaw browser set credentials user pass`
*   `openclaw browser set credentials --clear`
*   `openclaw browser set geo 37.7749 -122.4194 --origin "https://example.com"`
*   `openclaw browser set geo --clear`
*   `openclaw browser set media dark`
*   `openclaw browser set timezone America/New_York`
*   `openclaw browser set locale en-US`
*   `openclaw browser set device "iPhone 14"`

Notes:

*   `upload` and `dialog` are **arming** calls; run them before the click/press that triggers the chooser/dialog.
*   Download and trace output paths are constrained to OpenClaw temp roots:
    *   traces: `/tmp/openclaw` (fallback: `${os.tmpdir()}/openclaw`)
    *   downloads: `/tmp/openclaw/downloads` (fallback: `${os.tmpdir()}/openclaw/downloads`)
*   Upload paths are constrained to an OpenClaw temp uploads root:
    *   uploads: `/tmp/openclaw/uploads` (fallback: `${os.tmpdir()}/openclaw/uploads`)
*   `upload` can also set file inputs directly via `--input-ref` or `--element`.
*   `snapshot`:
    *   `--format ai` (default when Playwright is installed): returns an AI snapshot with numeric refs (`aria-ref="<n>"`).
    *   `--format aria`: returns the accessibility tree (no refs; inspection only).
    *   `--efficient` (or `--mode efficient`): compact role snapshot preset (interactive + compact + depth + lower maxChars).
    *   Config default (tool/CLI only): set `browser.snapshotDefaults.mode: "efficient"` to use efficient snapshots when the caller does not pass a mode (see [Gateway configuration](https://docs.openclaw.ai/gateway/configuration#browser-openclaw-managed-browser)).
    *   Role snapshot options (`--interactive`, `--compact`, `--depth`, `--selector`) force a role-based snapshot with refs like `ref=e12`.
    *   `--frame "<iframe selector>"` scopes role snapshots to an iframe (pairs with role refs like `e12`).
    *   `--interactive` outputs a flat, easy-to-pick list of interactive elements (best for driving actions).
    *   `--labels` adds a viewport-only screenshot with overlayed ref labels (prints `MEDIA:<path>`).
*   `click`/`type`/etc require a `ref` from `snapshot` (either numeric `12` or role ref `e12`). CSS selectors are intentionally not supported for actions.

## Snapshots and refs

OpenClaw supports two “snapshot” styles:

*   **AI snapshot (numeric refs)**: `openclaw browser snapshot` (default; `--format ai`)
    *   Output: a text snapshot that includes numeric refs.
    *   Actions: `openclaw browser click 12`, `openclaw browser type 23 "hello"`.
    *   Internally, the ref is resolved via Playwright’s `aria-ref`.
*   **Role snapshot (role refs like `e12`)**: `openclaw browser snapshot --interactive` (or `--compact`, `--depth`, `--selector`, `--frame`)
    *   Output: a role-based list/tree with `[ref=e12]` (and optional `[nth=1]`).
    *   Actions: `openclaw browser click e12`, `openclaw browser highlight e12`.
    *   Internally, the ref is resolved via `getByRole(...)` (plus `nth()` for duplicates).
    *   Add `--labels` to include a viewport screenshot with overlayed `e12` labels.

Ref behavior:

*   Refs are **not stable across navigations**; if something fails, re-run `snapshot` and use a fresh ref.
*   If the role snapshot was taken with `--frame`, role refs are scoped to that iframe until the next role snapshot.

## Wait power-ups

You can wait on more than just time/text:

*   Wait for URL (globs supported by Playwright):
    *   `openclaw browser wait --url "**/dash"`
*   Wait for load state:
    *   `openclaw browser wait --load networkidle`
*   Wait for a JS predicate:
    *   `openclaw browser wait --fn "window.ready===true"`
*   Wait for a selector to become visible:
    *   `openclaw browser wait "#main"`

These can be combined:

```
openclaw browser wait "#main" \
  --url "**/dash" \
  --load networkidle \
  --fn "window.ready===true" \
  --timeout-ms 15000
```

## Debug workflows

When an action fails (e.g. “not visible”, “strict mode violation”, “covered”):

1.  `openclaw browser snapshot --interactive`
2.  Use `click <ref>` / `type <ref>` (prefer role refs in interactive mode)
3.  If it still fails: `openclaw browser highlight <ref>` to see what Playwright is targeting
4.  If the page behaves oddly:
    *   `openclaw browser errors --clear`
    *   `openclaw browser requests --filter api --clear`
5.  For deep debugging: record a trace:
    *   `openclaw browser trace start`
    *   reproduce the issue
    *   `openclaw browser trace stop` (prints `TRACE:<path>`)

## JSON output

`--json` is for scripting and structured tooling. Examples:

```
openclaw browser status --json
openclaw browser snapshot --interactive --json
openclaw browser requests --filter api --json
openclaw browser cookies --json
```

Role snapshots in JSON include `refs` plus a small `stats` block (lines/chars/refs/interactive) so tools can reason about payload size and density.

## State and environment knobs

These are useful for “make the site behave like X” workflows:

*   Cookies: `cookies`, `cookies set`, `cookies clear`
*   Storage: `storage local|session get|set|clear`
*   Offline: `set offline on|off`
*   Headers: `set headers --headers-json '{"X-Debug":"1"}'` (legacy `set headers --json '{"X-Debug":"1"}'` remains supported)
*   HTTP basic auth: `set credentials user pass` (or `--clear`)
*   Geolocation: `set geo <lat> <lon> --origin "https://example.com"` (or `--clear`)
*   Media: `set media dark|light|no-preference|none`
*   Timezone / locale: `set timezone ...`, `set locale ...`
*   Device / viewport:
    *   `set device "iPhone 14"` (Playwright device presets)
    *   `set viewport 1280 720`

## Security & privacy

*   The openclaw browser profile may contain logged-in sessions; treat it as sensitive.
*   `browser act kind=evaluate` / `openclaw browser evaluate` and `wait --fn` execute arbitrary JavaScript in the page context. Prompt injection can steer this. Disable it with `browser.evaluateEnabled=false` if you do not need it.
*   For logins and anti-bot notes (X/Twitter, etc.), see [Browser login + X/Twitter posting](https://docs.openclaw.ai/tools/browser-login).
*   Keep the Gateway/node host private (loopback or tailnet-only).
*   Remote CDP endpoints are powerful; tunnel and protect them.

Strict-mode example (block private/internal destinations by default):

```
{
  browser: {
    ssrfPolicy: {
      dangerouslyAllowPrivateNetwork: false,
      hostnameAllowlist: ["*.example.com", "example.com"],
      allowedHostnames: ["localhost"], // optional exact allow
    },
  },
}
```

## Troubleshooting

For Linux-specific issues (especially snap Chromium), see [Browser troubleshooting](https://docs.openclaw.ai/tools/browser-linux-troubleshooting). For WSL2 Gateway + Windows Chrome split-host setups, see [WSL2 + Windows + remote Chrome CDP troubleshooting](https://docs.openclaw.ai/tools/browser-wsl2-windows-remote-cdp-troubleshooting).

The agent gets **one tool** for browser automation:

*   `browser` — status/start/stop/tabs/open/focus/close/snapshot/screenshot/navigate/act

How it maps:

*   `browser snapshot` returns a stable UI tree (AI or ARIA).
*   `browser act` uses the snapshot `ref` IDs to click/type/drag/select.
*   `browser screenshot` captures pixels (full page or element).
*   `browser` accepts:
    *   `profile` to choose a named browser profile (openclaw, chrome, or remote CDP).
    *   `target` (`sandbox` | `host` | `node`) to select where the browser lives.
    *   In sandboxed sessions, `target: "host"` requires `agents.defaults.sandbox.browser.allowHostControl=true`.
    *   If `target` is omitted: sandboxed sessions default to `sandbox`, non-sandbox sessions default to `host`.
    *   If a browser-capable node is connected, the tool may auto-route to it unless you pin `target="host"` or `target="node"`.

This keeps the agent deterministic and avoids brittle selectors.

---

<!-- SOURCE: https://docs.openclaw.ai/tools/browser-login -->

# Browser Login - OpenClaw

## Browser login + X/Twitter posting

## Manual login (recommended)

When a site requires login, **sign in manually** in the **host** browser profile (the openclaw browser). Do **not** give the model your credentials. Automated logins often trigger anti‑bot defenses and can lock the account. Back to the main browser docs: [Browser](https://docs.openclaw.ai/tools/browser).

## Which Chrome profile is used?

OpenClaw controls a **dedicated Chrome profile** (named `openclaw`, orange‑tinted UI). This is separate from your daily browser profile. Two easy ways to access it:

1.  **Ask the agent to open the browser** and then log in yourself.
2.  **Open it via CLI**:

```
openclaw browser start
openclaw browser open https://x.com
```

If you have multiple profiles, pass `--browser-profile <name>` (the default is `openclaw`).

## X/Twitter: recommended flow

*   **Read/search/threads:** use the **host** browser (manual login).
*   **Post updates:** use the **host** browser (manual login).

## Sandboxing + host browser access

Sandboxed browser sessions are **more likely** to trigger bot detection. For X/Twitter (and other strict sites), prefer the **host** browser. If the agent is sandboxed, the browser tool defaults to the sandbox. To allow host control:

```
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        browser: {
          allowHostControl: true,
        },
      },
    },
  },
}
```

Then target the host browser:

```
openclaw browser open https://x.com --browser-profile openclaw --target host
```

Or disable sandboxing for the agent that posts updates.

---

<!-- SOURCE: https://docs.openclaw.ai/tools/browser-linux-troubleshooting -->

# Browser Troubleshooting - OpenClaw

## Problem: “Failed to start Chrome CDP on port 18800”

OpenClaw’s browser control server fails to launch Chrome/Brave/Edge/Chromium with the error:

```
{"error":"Error: Failed to start Chrome CDP on port 18800 for profile \"openclaw\"."}
```

### Root Cause

On Ubuntu (and many Linux distros), the default Chromium installation is a **snap package**. Snap’s AppArmor confinement interferes with how OpenClaw spawns and monitors the browser process. The `apt install chromium` command installs a stub package that redirects to snap:

```
Note, selecting 'chromium-browser' instead of 'chromium'
chromium-browser is already the newest version (2:1snap1-0ubuntu2).
```

This is NOT a real browser — it’s just a wrapper.

### Solution 1: Install Google Chrome (Recommended)

Install the official Google Chrome `.deb` package, which is not sandboxed by snap:

```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y  # if there are dependency errors
```

Then update your OpenClaw config (`~/.openclaw/openclaw.json`):

```
{
  "browser": {
    "enabled": true,
    "executablePath": "/usr/bin/google-chrome-stable",
    "headless": true,
    "noSandbox": true
  }
}
```

### Solution 2: Use Snap Chromium with Attach-Only Mode

If you must use snap Chromium, configure OpenClaw to attach to a manually-started browser:

1.  Update config:

```
{
  "browser": {
    "enabled": true,
    "attachOnly": true,
    "headless": true,
    "noSandbox": true
  }
}
```

2.  Start Chromium manually:

```
chromium-browser --headless --no-sandbox --disable-gpu \
  --remote-debugging-port=18800 \
  --user-data-dir=$HOME/.openclaw/browser/openclaw/user-data \
  about:blank &
```

3.  Optionally create a systemd user service to auto-start Chrome:

```
# ~/.config/systemd/user/openclaw-browser.service
[Unit]
Description=OpenClaw Browser (Chrome CDP)
After=network.target

[Service]
ExecStart=/snap/bin/chromium --headless --no-sandbox --disable-gpu --remote-debugging-port=18800 --user-data-dir=%h/.openclaw/browser/openclaw/user-data about:blank
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

Enable with: `systemctl --user enable --now openclaw-browser.service`

### Verifying the Browser Works

Check status:

```
curl -s http://127.0.0.1:18791/ | jq '{running, pid, chosenBrowser}'
```

Test browsing:

```
curl -s -X POST http://127.0.0.1:18791/start
curl -s http://127.0.0.1:18791/tabs
```

### Config Reference

| Option | Description | Default |
| --- | --- | --- |
| `browser.enabled` | Enable browser control | `true` |
| `browser.executablePath` | Path to a Chromium-based browser binary (Chrome/Brave/Edge/Chromium) | auto-detected (prefers default browser when Chromium-based) |
| `browser.headless` | Run without GUI | `false` |
| `browser.noSandbox` | Add `--no-sandbox` flag (needed for some Linux setups) | `false` |
| `browser.attachOnly` | Don’t launch browser, only attach to existing | `false` |
| `browser.cdpPort` | Chrome DevTools Protocol port | `18800` |

### Problem: “Chrome extension relay is running, but no tab is connected”

You’re using the `chrome` profile (extension relay). It expects the OpenClaw browser extension to be attached to a live tab. Fix options:

1.  **Use the managed browser:** `openclaw browser start --browser-profile openclaw` (or set `browser.defaultProfile: "openclaw"`).
2.  **Use the extension relay:** install the extension, open a tab, and click the OpenClaw extension icon to attach it.

Notes:

*   The `chrome` profile uses your **system default Chromium browser** when possible.
*   Local `openclaw` profiles auto-assign `cdpPort`/`cdpUrl`; only set those for remote CDP.

---

<!-- SOURCE: https://docs.openclaw.ai/tools/chrome-extension -->

# Chrome Extension - OpenClaw

## Chrome extension (browser relay)

The OpenClaw Chrome extension lets the agent control your **existing Chrome tabs** (your normal Chrome window) instead of launching a separate openclaw-managed Chrome profile. Attach/detach happens via a **single Chrome toolbar button**.

## What it is (concept)

There are three parts:

*   **Browser control service** (Gateway or node): the API the agent/tool calls (via the Gateway)
*   **Local relay server** (loopback CDP): bridges between the control server and the extension (`http://127.0.0.1:18792` by default)
*   **Chrome MV3 extension**: attaches to the active tab using `chrome.debugger` and pipes CDP messages to the relay

OpenClaw then controls the attached tab through the normal `browser` tool surface (selecting the right profile).

## Install / load (unpacked)

1.  Install the extension to a stable local path:

```
openclaw browser extension install
```

2.  Print the installed extension directory path:

```
openclaw browser extension path
```

3.  Chrome → `chrome://extensions`

*   Enable “Developer mode”
*   “Load unpacked” → select the directory printed above

4.  Pin the extension.

## Updates (no build step)

The extension ships inside the OpenClaw release (npm package) as static files. There is no separate “build” step. After upgrading OpenClaw:

*   Re-run `openclaw browser extension install` to refresh the installed files under your OpenClaw state directory.
*   Chrome → `chrome://extensions` → click “Reload” on the extension.

## Use it (set gateway token once)

OpenClaw ships with a built-in browser profile named `chrome` that targets the extension relay on the default port. Before first attach, open extension Options and set:

*   `Port` (default `18792`)
*   `Gateway token` (must match `gateway.auth.token` / `OPENCLAW_GATEWAY_TOKEN`)

Use it:

*   CLI: `openclaw browser --browser-profile chrome tabs`
*   Agent tool: `browser` with `profile="chrome"`

If you want a different name or a different relay port, create your own profile:

```
openclaw browser create-profile \
  --name my-chrome \
  --driver extension \
  --cdp-url http://127.0.0.1:18792 \
  --color "#00AA00"
```

### Custom Gateway ports

If you’re using a custom gateway port, the extension relay port is automatically derived: **Extension Relay Port = Gateway Port + 3** Example: if `gateway.port: 19001`, then:

*   Extension relay port: `19004` (gateway + 3)

Configure the extension to use the derived relay port in the extension Options page.

*   Open the tab you want OpenClaw to control.
*   Click the extension icon.
    *   Badge shows `ON` when attached.
*   Click again to detach.

## Which tab does it control?

*   It does **not** automatically control “whatever tab you’re looking at”.
*   It controls **only the tab(s) you explicitly attached** by clicking the toolbar button.
*   To switch: open the other tab and click the extension icon there.

## Badge + common errors

*   `ON`: attached; OpenClaw can drive that tab.
*   `…`: connecting to the local relay.
*   `!`: relay not reachable/authenticated (most common: relay server not running, or gateway token missing/wrong).

If you see `!`:

*   Make sure the Gateway is running locally (default setup), or run a node host on this machine if the Gateway runs elsewhere.
*   Open the extension Options page; it validates relay reachability + gateway-token auth.

## Remote Gateway (use a node host)

If the Gateway runs on the same machine as Chrome, it starts the browser control service on loopback and auto-starts the relay server. The extension talks to the local relay; the CLI/tool calls go to the Gateway.

### Remote Gateway (Gateway runs elsewhere) — **run a node host**

If your Gateway runs on another machine, start a node host on the machine that runs Chrome. The Gateway will proxy browser actions to that node; the extension + relay stay local to the browser machine. If multiple nodes are connected, pin one with `gateway.nodes.browser.node` or set `gateway.nodes.browser.mode`.

If your agent session is sandboxed (`agents.defaults.sandbox.mode != "off"`), the `browser` tool can be restricted:

*   By default, sandboxed sessions often target the **sandbox browser** (`target="sandbox"`), not your host Chrome.
*   Chrome extension relay takeover requires controlling the **host** browser control server.

Options:

*   Easiest: use the extension from a **non-sandboxed** session/agent.
*   Or allow host browser control for sandboxed sessions:

```
{
  agents: {
    defaults: {
      sandbox: {
        browser: {
          allowHostControl: true,
        },
      },
    },
  },
}
```

Then ensure the tool isn’t denied by tool policy, and (if needed) call `browser` with `target="host"`. Debugging: `openclaw sandbox explain`

## Remote access tips

*   Keep the Gateway and node host on the same tailnet; avoid exposing relay ports to LAN or public Internet.
*   Pair nodes intentionally; disable browser proxy routing if you don’t want remote control (`gateway.nodes.browser.mode="off"`).
*   Leave the relay on loopback unless you have a real cross-namespace need. For WSL2 or similar split-host setups, set `browser.relayBindHost` to an explicit bind address such as `0.0.0.0`, then keep access constrained with Gateway auth, node pairing, and a private network.

## How “extension path” works

`openclaw browser extension path` prints the **installed** on-disk directory containing the extension files. The CLI intentionally does **not** print a `node_modules` path. Always run `openclaw browser extension install` first to copy the extension to a stable location under your OpenClaw state directory. If you move or delete that install directory, Chrome will mark the extension as broken until you reload it from a valid path.

## Security implications (read this)

This is powerful and risky. Treat it like giving the model “hands on your browser”.

*   The extension uses Chrome’s debugger API (`chrome.debugger`). When attached, the model can:
    *   click/type/navigate in that tab
    *   read page content
    *   access whatever the tab’s logged-in session can access
*   **This is not isolated** like the dedicated openclaw-managed profile.
    *   If you attach to your daily-driver profile/tab, you’re granting access to that account state.

Recommendations:

*   Prefer a dedicated Chrome profile (separate from your personal browsing) for extension relay usage.
*   Keep the Gateway and any node hosts tailnet-only; rely on Gateway auth + node pairing.
*   Avoid exposing relay ports over LAN (`0.0.0.0`) and avoid Funnel (public).
*   The relay blocks non-extension origins and requires gateway-token auth for both `/cdp` and `/extension`.

Related:

*   Browser tool overview: [Browser](https://docs.openclaw.ai/tools/browser)
*   Security audit: [Security](https://docs.openclaw.ai/gateway/security)
*   Tailscale setup: [Tailscale](https://docs.openclaw.ai/gateway/tailscale)

---

<!-- SOURCE: https://docs.openclaw.ai/tools/browser-wsl2-windows-remote-cdp-troubleshooting -->

# WSL2 + Windows + remote Chrome CDP troubleshooting

This guide covers the common split-host setup where:

*   OpenClaw Gateway runs inside WSL2
*   Chrome runs on Windows
*   browser control must cross the WSL2/Windows boundary

It also covers the layered failure pattern from [issue #39369](https://github.com/openclaw/openclaw/issues/39369): several independent problems can show up at once, which makes the wrong layer look broken first.

## Choose the right browser mode first

You have two valid patterns:

### Option 1: Raw remote CDP

Use a remote browser profile that points from WSL2 to a Windows Chrome CDP endpoint. Choose this when:

*   you only need browser control
*   you are comfortable exposing Chrome remote debugging to WSL2
*   you do not need the Chrome extension relay

### Option 2: Chrome extension relay

Use the built-in `chrome` profile plus the OpenClaw Chrome extension. Choose this when:

*   you want to attach to an existing Windows Chrome tab with the toolbar button
*   you want extension-based control instead of raw `--remote-debugging-port`
*   the relay itself must be reachable across the WSL2/Windows boundary

If you use the extension relay across namespaces, `browser.relayBindHost` is the important setting introduced in [Browser](https://docs.openclaw.ai/tools/browser) and [Chrome extension](https://docs.openclaw.ai/tools/chrome-extension).

## Working architecture

Reference shape:

*   WSL2 runs the Gateway on `127.0.0.1:18789`
*   Windows opens the Control UI in a normal browser at `http://127.0.0.1:18789/`
*   Windows Chrome exposes a CDP endpoint on port `9222`
*   WSL2 can reach that Windows CDP endpoint
*   OpenClaw points a browser profile at the address that is reachable from WSL2

## Why this setup is confusing

Several failures can overlap:

*   WSL2 cannot reach the Windows CDP endpoint
*   the Control UI is opened from a non-secure origin
*   `gateway.controlUi.allowedOrigins` does not match the page origin
*   token or pairing is missing
*   the browser profile points at the wrong address
*   the extension relay is still loopback-only when you actually need cross-namespace access

Because of that, fixing one layer can still leave a different error visible.

## Critical rule for the Control UI

When the UI is opened from Windows, use Windows localhost unless you have a deliberate HTTPS setup. Use: `http://127.0.0.1:18789/` Do not default to a LAN IP for the Control UI. Plain HTTP on a LAN or tailnet address can trigger insecure-origin/device-auth behavior that is unrelated to CDP itself. See [Control UI](https://docs.openclaw.ai/web/control-ui).

## Validate in layers

Work top to bottom. Do not skip ahead.

### Layer 1: Verify Chrome is serving CDP on Windows

Start Chrome on Windows with remote debugging enabled:

```
chrome.exe --remote-debugging-port=9222
```

From Windows, verify Chrome itself first:

```
curl http://127.0.0.1:9222/json/version
curl http://127.0.0.1:9222/json/list
```

If this fails on Windows, OpenClaw is not the problem yet.

### Layer 2: Verify WSL2 can reach that Windows endpoint

From WSL2, test the exact address you plan to use in `cdpUrl`:

```
curl http://WINDOWS_HOST_OR_IP:9222/json/version
curl http://WINDOWS_HOST_OR_IP:9222/json/list
```

Good result:

*   `/json/version` returns JSON with Browser / Protocol-Version metadata
*   `/json/list` returns JSON (empty array is fine if no pages are open)

If this fails:

*   Windows is not exposing the port to WSL2 yet
*   the address is wrong for the WSL2 side
*   firewall / port forwarding / local proxying is still missing

Fix that before touching OpenClaw config.

### Layer 3: Configure the correct browser profile

For raw remote CDP, point OpenClaw at the address that is reachable from WSL2:

```
{
  browser: {
    enabled: true,
    defaultProfile: "remote",
    profiles: {
      remote: {
        cdpUrl: "http://WINDOWS_HOST_OR_IP:9222",
        attachOnly: true,
        color: "#00AA00",
      },
    },
  },
}
```

Notes:

*   use the WSL2-reachable address, not whatever only works on Windows
*   keep `attachOnly: true` for externally managed browsers
*   test the same URL with `curl` before expecting OpenClaw to succeed

### Layer 4: If you use the Chrome extension relay instead

If the browser machine and the Gateway are separated by a namespace boundary, the relay may need a non-loopback bind address. Example:

```
{
  browser: {
    enabled: true,
    defaultProfile: "chrome",
    relayBindHost: "0.0.0.0",
  },
}
```

Use this only when needed:

*   default behavior is safer because the relay stays loopback-only
*   `0.0.0.0` expands exposure surface
*   keep Gateway auth, node pairing, and the surrounding network private

If you do not need the extension relay, prefer the raw remote CDP profile above.

### Layer 5: Verify the Control UI layer separately

Open the UI from Windows: `http://127.0.0.1:18789/` Then verify:

*   the page origin matches what `gateway.controlUi.allowedOrigins` expects
*   token auth or pairing is configured correctly
*   you are not debugging a Control UI auth problem as if it were a browser problem

Helpful page:

*   [Control UI](https://docs.openclaw.ai/web/control-ui)

### Layer 6: Verify end-to-end browser control

From WSL2:

```
openclaw browser open https://example.com --browser-profile remote
openclaw browser tabs --browser-profile remote
```

For the extension relay:

```
openclaw browser tabs --browser-profile chrome
```

Good result:

*   the tab opens in Windows Chrome
*   `openclaw browser tabs` returns the target
*   later actions (`snapshot`, `screenshot`, `navigate`) work from the same profile

## Common misleading errors

Treat each message as a layer-specific clue:

*   `control-ui-insecure-auth`
    *   UI origin / secure-context problem, not a CDP transport problem
*   `token_missing`
    *   auth configuration problem
*   `pairing required`
    *   device approval problem
*   `Remote CDP for profile "remote" is not reachable`
    *   WSL2 cannot reach the configured `cdpUrl`
*   `gateway timeout after 1500ms`
    *   often still CDP reachability or a slow/unreachable remote endpoint
*   `Chrome extension relay is running, but no tab is connected`
    *   extension relay profile selected, but no attached tab exists yet

## Fast triage checklist

1.  Windows: does `curl http://127.0.0.1:9222/json/version` work?
2.  WSL2: does `curl http://WINDOWS_HOST_OR_IP:9222/json/version` work?
3.  OpenClaw config: does `browser.profiles.<name>.cdpUrl` use that exact WSL2-reachable address?
4.  Control UI: are you opening `http://127.0.0.1:18789/` instead of a LAN IP?
5.  Extension relay only: do you actually need `browser.relayBindHost`, and if so is it set explicitly?

## Practical takeaway

The setup is usually viable. The hard part is that browser transport, Control UI origin security, token/pairing, and extension-relay topology can each fail independently while looking similar from the user side. When in doubt:

*   verify the Windows Chrome endpoint locally first
*   verify the same endpoint from WSL2 second
*   only then debug OpenClaw config or Control UI auth

---

<!-- SOURCE: https://docs.openclaw.ai/tools/agent-send -->

# Agent Send - OpenClaw

## `openclaw agent` (direct agent runs)

`openclaw agent` runs a single agent turn without needing an inbound chat message. By default it goes **through the Gateway**; add `--local` to force the embedded runtime on the current machine.

## Behavior

*   Required: `--message <text>`
*   Session selection:
    *   `--to <dest>` derives the session key (group/channel targets preserve isolation; direct chats collapse to `main`), **or**
    *   `--session-id <id>` reuses an existing session by id, **or**
    *   `--agent <id>` targets a configured agent directly (uses that agent’s `main` session key)
*   Runs the same embedded agent runtime as normal inbound replies.
*   Thinking/verbose flags persist into the session store.
*   Output:
    *   default: prints reply text (plus `MEDIA:<url>` lines)
    *   `--json`: prints structured payload + metadata
*   Optional delivery back to a channel with `--deliver` + `--channel` (target formats match `openclaw message --target`).
*   Use `--reply-channel`/`--reply-to`/`--reply-account` to override delivery without changing the session.

If the Gateway is unreachable, the CLI **falls back** to the embedded local run.

## Examples

```
openclaw agent --to +15555550123 --message "status update"
openclaw agent --agent ops --message "Summarize logs"
openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium
openclaw agent --to +15555550123 --message "Trace logs" --verbose on --json
openclaw agent --to +15555550123 --message "Summon reply" --deliver
openclaw agent --agent ops --message "Generate report" --deliver --reply-channel slack --reply-to "#reports"
```

## Flags

*   `--local`: run locally (requires model provider API keys in your shell)
*   `--deliver`: send the reply to the chosen channel
*   `--channel`: delivery channel (`whatsapp|telegram|discord|googlechat|slack|signal|imessage`, default: `whatsapp`)
*   `--reply-to`: delivery target override
*   `--reply-channel`: delivery channel override
*   `--reply-account`: delivery account id override
*   `--thinking <off|minimal|low|medium|high|xhigh>`: persist thinking level (GPT-5.2 + Codex models only)
*   `--verbose <on|full|off>`: persist verbose level
*   `--timeout <seconds>`: override agent timeout
*   `--json`: output structured JSON

---

<!-- SOURCE: https://docs.openclaw.ai/tools/creating-skills -->

# Creating Skills - OpenClaw

## Creating Custom Skills 🛠

OpenClaw is designed to be easily extensible. “Skills” are the primary way to add new capabilities to your assistant.

## What is a Skill?

A skill is a directory containing a `SKILL.md` file (which provides instructions and tool definitions to the LLM) and optionally some scripts or resources.

## Step-by-Step: Your First Skill

### 1\. Create the Directory

Skills live in your workspace, usually `~/.openclaw/workspace/skills/`. Create a new folder for your skill:

```
mkdir -p ~/.openclaw/workspace/skills/hello-world
```

### 2\. Define the `SKILL.md`

Create a `SKILL.md` file in that directory. This file uses YAML frontmatter for metadata and Markdown for instructions.

```
---
name: hello_world
description: A simple skill that says hello.
---

# Hello World Skill

When the user asks for a greeting, use the `echo` tool to say "Hello from your custom skill!".
```

### 3\. Add Tools (Optional)

You can define custom tools in the frontmatter or instruct the agent to use existing system tools (like `bash` or `browser`).

### 4\. Refresh OpenClaw

Ask your agent to “refresh skills” or restart the gateway. OpenClaw will discover the new directory and index the `SKILL.md`.

## Best Practices

*   **Be Concise**: Instruct the model on _what_ to do, not how to be an AI.
*   **Safety First**: If your skill uses `bash`, ensure the prompts don’t allow arbitrary command injection from untrusted user input.
*   **Test Locally**: Use `openclaw agent --message "use my new skill"` to test.

You can also browse and contribute skills to [ClawHub](https://clawhub.com/).

---

<!-- SOURCE: https://docs.openclaw.ai/tools/subagents -->

# Sub-Agents - OpenClaw

Sub-agents are background agent runs spawned from an existing agent run. They run in their own session (`agent:<agentId>:subagent:<uuid>`) and, when finished, **announce** their result back to the requester chat channel.

## Slash command

Use `/subagents` to inspect or control sub-agent runs for the **current session**:

*   `/subagents list`
*   `/subagents kill <id|#|all>`
*   `/subagents log <id|#> [limit] [tools]`
*   `/subagents info <id|#>`
*   `/subagents send <id|#> <message>`
*   `/subagents steer <id|#> <message>`
*   `/subagents spawn <agentId> <task> [--model <model>] [--thinking <level>]`

Thread binding controls: These commands work on channels that support persistent thread bindings. See **Thread supporting channels** below.

*   `/focus <subagent-label|session-key|session-id|session-label>`
*   `/unfocus`
*   `/agents`
*   `/session idle <duration|off>`
*   `/session max-age <duration|off>`

`/subagents info` shows run metadata (status, timestamps, session id, transcript path, cleanup).

### Spawn behavior

`/subagents spawn` starts a background sub-agent as a user command, not an internal relay, and it sends one final completion update back to the requester chat when the run finishes.

*   The spawn command is non-blocking; it returns a run id immediately.
*   On completion, the sub-agent announces a summary/result message back to the requester chat channel.
*   For manual spawns, delivery is resilient:
    *   OpenClaw tries direct `agent` delivery first with a stable idempotency key.
    *   If direct delivery fails, it falls back to queue routing.
    *   If queue routing is still not available, the announce is retried with a short exponential backoff before final give-up.
*   The completion handoff to the requester session is runtime-generated internal context (not user-authored text) and includes:
    *   `Result` (`assistant` reply text, or latest `toolResult` if the assistant reply is empty)
    *   `Status` (`completed successfully` / `failed` / `timed out` / `unknown`)
    *   compact runtime/token stats
    *   a delivery instruction telling the requester agent to rewrite in normal assistant voice (not forward raw internal metadata)
*   `--model` and `--thinking` override defaults for that specific run.
*   Use `info`/`log` to inspect details and output after completion.
*   `/subagents spawn` is one-shot mode (`mode: "run"`). For persistent thread-bound sessions, use `sessions_spawn` with `thread: true` and `mode: "session"`.
*   For ACP harness sessions (Codex, Claude Code, Gemini CLI), use `sessions_spawn` with `runtime: "acp"` and see [ACP Agents](https://docs.openclaw.ai/tools/acp-agents).

Primary goals:

*   Parallelize “research / long task / slow tool” work without blocking the main run.
*   Keep sub-agents isolated by default (session separation + optional sandboxing).
*   Keep the tool surface hard to misuse: sub-agents do **not** get session tools by default.
*   Support configurable nesting depth for orchestrator patterns.

Cost note: each sub-agent has its **own** context and token usage. For heavy or repetitive tasks, set a cheaper model for sub-agents and keep your main agent on a higher-quality model. You can configure this via `agents.defaults.subagents.model` or per-agent overrides.

Use `sessions_spawn`:

*   Starts a sub-agent run (`deliver: false`, global lane: `subagent`)
*   Then runs an announce step and posts the announce reply to the requester chat channel
*   Default model: inherits the caller unless you set `agents.defaults.subagents.model` (or per-agent `agents.list[].subagents.model`); an explicit `sessions_spawn.model` still wins.
*   Default thinking: inherits the caller unless you set `agents.defaults.subagents.thinking` (or per-agent `agents.list[].subagents.thinking`); an explicit `sessions_spawn.thinking` still wins.
*   Default run timeout: if `sessions_spawn.runTimeoutSeconds` is omitted, OpenClaw uses `agents.defaults.subagents.runTimeoutSeconds` when set; otherwise it falls back to `0` (no timeout).

Tool params:

*   `task` (required)
*   `label?` (optional)
*   `agentId?` (optional; spawn under another agent id if allowed)
*   `model?` (optional; overrides the sub-agent model; invalid values are skipped and the sub-agent runs on the default model with a warning in the tool result)
*   `thinking?` (optional; overrides thinking level for the sub-agent run)
*   `runTimeoutSeconds?` (defaults to `agents.defaults.subagents.runTimeoutSeconds` when set, otherwise `0`; when set, the sub-agent run is aborted after N seconds)
*   `thread?` (default `false`; when `true`, requests channel thread binding for this sub-agent session)
*   `mode?` (`run|session`)
    *   default is `run`
    *   if `thread: true` and `mode` omitted, default becomes `session`
    *   `mode: "session"` requires `thread: true`
*   `cleanup?` (`delete|keep`, default `keep`)
*   `sandbox?` (`inherit|require`, default `inherit`; `require` rejects spawn unless target child runtime is sandboxed)
*   `sessions_spawn` does **not** accept channel-delivery params (`target`, `channel`, `to`, `threadId`, `replyTo`, `transport`). For delivery, use `message`/`sessions_send` from the spawned run.

## Thread-bound sessions

When thread bindings are enabled for a channel, a sub-agent can stay bound to a thread so follow-up user messages in that thread keep routing to the same sub-agent session.

### Thread supporting channels

*   Discord (currently the only supported channel): supports persistent thread-bound subagent sessions (`sessions_spawn` with `thread: true`), manual thread controls (`/focus`, `/unfocus`, `/agents`, `/session idle`, `/session max-age`), and adapter keys `channels.discord.threadBindings.enabled`, `channels.discord.threadBindings.idleHours`, `channels.discord.threadBindings.maxAgeHours`, and `channels.discord.threadBindings.spawnSubagentSessions`.

Quick flow:

1.  Spawn with `sessions_spawn` using `thread: true` (and optionally `mode: "session"`).
2.  OpenClaw creates or binds a thread to that session target in the active channel.
3.  Replies and follow-up messages in that thread route to the bound session.
4.  Use `/session idle` to inspect/update inactivity auto-unfocus and `/session max-age` to control the hard cap.
5.  Use `/unfocus` to detach manually.

Manual controls:

*   `/focus <target>` binds the current thread (or creates one) to a sub-agent/session target.
*   `/unfocus` removes the binding for the current bound thread.
*   `/agents` lists active runs and binding state (`thread:<id>` or `unbound`).
*   `/session idle` and `/session max-age` only work for focused bound threads.

Config switches:

*   Global default: `session.threadBindings.enabled`, `session.threadBindings.idleHours`, `session.threadBindings.maxAgeHours`
*   Channel override and spawn auto-bind keys are adapter-specific. See **Thread supporting channels** above.

See [Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference) and [Slash commands](https://docs.openclaw.ai/tools/slash-commands) for current adapter details. Allowlist:

*   `agents.list[].subagents.allowAgents`: list of agent ids that can be targeted via `agentId` (`["*"]` to allow any). Default: only the requester agent.
*   Sandbox inheritance guard: if the requester session is sandboxed, `sessions_spawn` rejects targets that would run unsandboxed.

Discovery:

*   Use `agents_list` to see which agent ids are currently allowed for `sessions_spawn`.

Auto-archive:

*   Sub-agent sessions are automatically archived after `agents.defaults.subagents.archiveAfterMinutes` (default: 60).
*   Archive uses `sessions.delete` and renames the transcript to `*.deleted.<timestamp>` (same folder).
*   `cleanup: "delete"` archives immediately after announce (still keeps the transcript via rename).
*   Auto-archive is best-effort; pending timers are lost if the gateway restarts.
*   `runTimeoutSeconds` does **not** auto-archive; it only stops the run. The session remains until auto-archive.
*   Auto-archive applies equally to depth-1 and depth-2 sessions.

## Nested Sub-Agents

By default, sub-agents cannot spawn their own sub-agents (`maxSpawnDepth: 1`). You can enable one level of nesting by setting `maxSpawnDepth: 2`, which allows the **orchestrator pattern**: main → orchestrator sub-agent → worker sub-sub-agents.

### How to enable

```
{
  agents: {
    defaults: {
      subagents: {
        maxSpawnDepth: 2, // allow sub-agents to spawn children (default: 1)
        maxChildrenPerAgent: 5, // max active children per agent session (default: 5)
        maxConcurrent: 8, // global concurrency lane cap (default: 8)
        runTimeoutSeconds: 900, // default timeout for sessions_spawn when omitted (0 = no timeout)
      },
    },
  },
}
```

### Depth levels

| Depth | Session key shape | Role | Can spawn? |
| --- | --- | --- | --- |
| 0   | `agent:<id>:main` | Main agent | Always |
| 1   | `agent:<id>:subagent:<uuid>` | Sub-agent (orchestrator when depth 2 allowed) | Only if `maxSpawnDepth >= 2` |
| 2   | `agent:<id>:subagent:<uuid>:subagent:<uuid>` | Sub-sub-agent (leaf worker) | Never |

### Announce chain

Results flow back up the chain:

1.  Depth-2 worker finishes → announces to its parent (depth-1 orchestrator)
2.  Depth-1 orchestrator receives the announce, synthesizes results, finishes → announces to main
3.  Main agent receives the announce and delivers to the user

Each level only sees announces from its direct children.

### Tool policy by depth

*   **Depth 1 (orchestrator, when `maxSpawnDepth >= 2`)**: Gets `sessions_spawn`, `subagents`, `sessions_list`, `sessions_history` so it can manage its children. Other session/system tools remain denied.
*   **Depth 1 (leaf, when `maxSpawnDepth == 1`)**: No session tools (current default behavior).
*   **Depth 2 (leaf worker)**: No session tools — `sessions_spawn` is always denied at depth 2. Cannot spawn further children.

### Per-agent spawn limit

Each agent session (at any depth) can have at most `maxChildrenPerAgent` (default: 5) active children at a time. This prevents runaway fan-out from a single orchestrator.

### Cascade stop

Stopping a depth-1 orchestrator automatically stops all its depth-2 children:

*   `/stop` in the main chat stops all depth-1 agents and cascades to their depth-2 children.
*   `/subagents kill <id>` stops a specific sub-agent and cascades to its children.
*   `/subagents kill all` stops all sub-agents for the requester and cascades.

## Authentication

Sub-agent auth is resolved by **agent id**, not by session type:

*   The sub-agent session key is `agent:<agentId>:subagent:<uuid>`.
*   The auth store is loaded from that agent’s `agentDir`.
*   The main agent’s auth profiles are merged in as a **fallback**; agent profiles override main profiles on conflicts.

Note: the merge is additive, so main profiles are always available as fallbacks. Fully isolated auth per agent is not supported yet.

## Announce

Sub-agents report back via an announce step:

*   The announce step runs inside the sub-agent session (not the requester session).
*   If the sub-agent replies exactly `ANNOUNCE_SKIP`, nothing is posted.
*   Otherwise delivery depends on requester depth:
    *   top-level requester sessions use a follow-up `agent` call with external delivery (`deliver=true`)
    *   nested requester subagent sessions receive an internal follow-up injection (`deliver=false`) so the orchestrator can synthesize child results in-session
    *   if a nested requester subagent session is gone, OpenClaw falls back to that session’s requester when available
*   Child completion aggregation is scoped to the current requester run when building nested completion findings, preventing stale prior-run child outputs from leaking into the current announce.
*   Announce replies preserve thread/topic routing when available on channel adapters.
*   Announce context is normalized to a stable internal event block:
    *   source (`subagent` or `cron`)
    *   child session key/id
    *   announce type + task label
    *   status line derived from runtime outcome (`success`, `error`, `timeout`, or `unknown`)
    *   result content from the announce step (or `(no output)` if missing)
    *   a follow-up instruction describing when to reply vs. stay silent
*   `Status` is not inferred from model output; it comes from runtime outcome signals.

Announce payloads include a stats line at the end (even when wrapped):

*   Runtime (e.g., `runtime 5m12s`)
*   Token usage (input/output/total)
*   Estimated cost when model pricing is configured (`models.providers.*.models[].cost`)
*   `sessionKey`, `sessionId`, and transcript path (so the main agent can fetch history via `sessions_history` or inspect the file on disk)
*   Internal metadata is meant for orchestration only; user-facing replies should be rewritten in normal assistant voice.

By default, sub-agents get **all tools except session tools** and system tools:

*   `sessions_list`
*   `sessions_history`
*   `sessions_send`
*   `sessions_spawn`

When `maxSpawnDepth >= 2`, depth-1 orchestrator sub-agents additionally receive `sessions_spawn`, `subagents`, `sessions_list`, and `sessions_history` so they can manage their children. Override via config:

```
{
  agents: {
    defaults: {
      subagents: {
        maxConcurrent: 1,
      },
    },
  },
  tools: {
    subagents: {
      tools: {
        // deny wins
        deny: ["gateway", "cron"],
        // if allow is set, it becomes allow-only (deny still wins)
        // allow: ["read", "exec", "process"]
      },
    },
  },
}
```

## Concurrency

Sub-agents use a dedicated in-process queue lane:

*   Lane name: `subagent`
*   Concurrency: `agents.defaults.subagents.maxConcurrent` (default `8`)

## Stopping

*   Sending `/stop` in the requester chat aborts the requester session and stops any active sub-agent runs spawned from it, cascading to nested children.
*   `/subagents kill <id>` stops a specific sub-agent and cascades to its children.

## Limitations

*   Sub-agent announce is **best-effort**. If the gateway restarts, pending “announce back” work is lost.
*   Sub-agents still share the same gateway process resources; treat `maxConcurrent` as a safety valve.
*   `sessions_spawn` is always non-blocking: it returns `{ status: "accepted", runId, childSessionKey }` immediately.
*   Sub-agent context only injects `AGENTS.md` + `TOOLS.md` (no `SOUL.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, or `BOOTSTRAP.md`).
*   Maximum nesting depth is 5 (`maxSpawnDepth` range: 1–5). Depth 2 is recommended for most use cases.
*   `maxChildrenPerAgent` caps active children per session (default: 5, range: 1–20).

---

<!-- SOURCE: https://docs.openclaw.ai/tools/slash-commands -->

# Slash Commands - OpenClaw

Commands are handled by the Gateway. Most commands must be sent as a **standalone** message that starts with `/`. The host-only bash chat command uses `! <cmd>` (with `/bash <cmd>` as an alias). There are two related systems:

*   **Commands**: standalone `/...` messages.
*   **Directives**: `/think`, `/verbose`, `/reasoning`, `/elevated`, `/exec`, `/model`, `/queue`.
    *   Directives are stripped from the message before the model sees it.
    *   In normal chat messages (not directive-only), they are treated as “inline hints” and do **not** persist session settings.
    *   In directive-only messages (the message contains only directives), they persist to the session and reply with an acknowledgement.
    *   Directives are only applied for **authorized senders**. If `commands.allowFrom` is set, it is the only allowlist used; otherwise authorization comes from channel allowlists/pairing plus `commands.useAccessGroups`. Unauthorized senders see directives treated as plain text.

There are also a few **inline shortcuts** (allowlisted/authorized senders only): `/help`, `/commands`, `/status`, `/whoami` (`/id`). They run immediately, are stripped before the model sees the message, and the remaining text continues through the normal flow.

## Config

```
{
  commands: {
    native: "auto",
    nativeSkills: "auto",
    text: true,
    bash: false,
    bashForegroundMs: 2000,
    config: false,
    debug: false,
    restart: false,
    allowFrom: {
      "*": ["user1"],
      discord: ["user:123"],
    },
    useAccessGroups: true,
  },
}
```

*   `commands.text` (default `true`) enables parsing `/...` in chat messages.
    *   On surfaces without native commands (WhatsApp/WebChat/Signal/iMessage/Google Chat/MS Teams), text commands still work even if you set this to `false`.
*   `commands.native` (default `"auto"`) registers native commands.
    *   Auto: on for Discord/Telegram; off for Slack (until you add slash commands); ignored for providers without native support.
    *   Set `channels.discord.commands.native`, `channels.telegram.commands.native`, or `channels.slack.commands.native` to override per provider (bool or `"auto"`).
    *   `false` clears previously registered commands on Discord/Telegram at startup. Slack commands are managed in the Slack app and are not removed automatically.
*   `commands.nativeSkills` (default `"auto"`) registers **skill** commands natively when supported.
    *   Auto: on for Discord/Telegram; off for Slack (Slack requires creating a slash command per skill).
    *   Set `channels.discord.commands.nativeSkills`, `channels.telegram.commands.nativeSkills`, or `channels.slack.commands.nativeSkills` to override per provider (bool or `"auto"`).
*   `commands.bash` (default `false`) enables `! <cmd>` to run host shell commands (`/bash <cmd>` is an alias; requires `tools.elevated` allowlists).
*   `commands.bashForegroundMs` (default `2000`) controls how long bash waits before switching to background mode (`0` backgrounds immediately).
*   `commands.config` (default `false`) enables `/config` (reads/writes `openclaw.json`).
*   `commands.debug` (default `false`) enables `/debug` (runtime-only overrides).
*   `commands.allowFrom` (optional) sets a per-provider allowlist for command authorization. When configured, it is the only authorization source for commands and directives (channel allowlists/pairing and `commands.useAccessGroups` are ignored). Use `"*"` for a global default; provider-specific keys override it.
*   `commands.useAccessGroups` (default `true`) enforces allowlists/policies for commands when `commands.allowFrom` is not set.

## Command list

Text + native (when enabled):

*   `/help`
*   `/commands`
*   `/skill <name> [input]` (run a skill by name)
*   `/status` (show current status; includes provider usage/quota for the current model provider when available)
*   `/allowlist` (list/add/remove allowlist entries)
*   `/approve <id> allow-once|allow-always|deny` (resolve exec approval prompts)
*   `/context [list|detail|json]` (explain “context”; `detail` shows per-file + per-tool + per-skill + system prompt size)
*   `/export-session [path]` (alias: `/export`) (export current session to HTML with full system prompt)
*   `/whoami` (show your sender id; alias: `/id`)
*   `/session idle <duration|off>` (manage inactivity auto-unfocus for focused thread bindings)
*   `/session max-age <duration|off>` (manage hard max-age auto-unfocus for focused thread bindings)
*   `/subagents list|kill|log|info|send|steer|spawn` (inspect, control, or spawn sub-agent runs for the current session)
*   `/acp spawn|cancel|steer|close|status|set-mode|set|cwd|permissions|timeout|model|reset-options|doctor|install|sessions` (inspect and control ACP runtime sessions)
*   `/agents` (list thread-bound agents for this session)
*   `/focus <target>` (Discord: bind this thread, or a new thread, to a session/subagent target)
*   `/unfocus` (Discord: remove the current thread binding)
*   `/kill <id|#|all>` (immediately abort one or all running sub-agents for this session; no confirmation message)
*   `/steer <id|#> <message>` (steer a running sub-agent immediately: in-run when possible, otherwise abort current work and restart on the steer message)
*   `/tell <id|#> <message>` (alias for `/steer`)
*   `/config show|get|set|unset` (persist config to disk, owner-only; requires `commands.config: true`)
*   `/debug show|set|unset|reset` (runtime overrides, owner-only; requires `commands.debug: true`)
*   `/usage off|tokens|full|cost` (per-response usage footer or local cost summary)
*   `/tts off|always|inbound|tagged|status|provider|limit|summary|audio` (control TTS; see [/tts](https://docs.openclaw.ai/tts))
    *   Discord: native command is `/voice` (Discord reserves `/tts`); text `/tts` still works.
*   `/stop`
*   `/restart`
*   `/dock-telegram` (alias: `/dock_telegram`) (switch replies to Telegram)
*   `/dock-discord` (alias: `/dock_discord`) (switch replies to Discord)
*   `/dock-slack` (alias: `/dock_slack`) (switch replies to Slack)
*   `/activation mention|always` (groups only)
*   `/send on|off|inherit` (owner-only)
*   `/reset` or `/new [model]` (optional model hint; remainder is passed through)
*   `/think <off|minimal|low|medium|high|xhigh>` (dynamic choices by model/provider; aliases: `/thinking`, `/t`)
*   `/verbose on|full|off` (alias: `/v`)
*   `/reasoning on|off|stream` (alias: `/reason`; when on, sends a separate message prefixed `Reasoning:`; `stream` = Telegram draft only)
*   `/elevated on|off|ask|full` (alias: `/elev`; `full` skips exec approvals)
*   `/exec host=<sandbox|gateway|node> security=<deny|allowlist|full> ask=<off|on-miss|always> node=<id>` (send `/exec` to show current)
*   `/model <name>` (alias: `/models`; or `/<alias>` from `agents.defaults.models.*.alias`)
*   `/queue <mode>` (plus options like `debounce:2s cap:25 drop:summarize`; send `/queue` to see current settings)
*   `/bash <command>` (host-only; alias for `! <command>`; requires `commands.bash: true` + `tools.elevated` allowlists)

Text-only:

*   `/compact [instructions]` (see [/concepts/compaction](https://docs.openclaw.ai/concepts/compaction))
*   `! <command>` (host-only; one at a time; use `!poll` + `!stop` for long-running jobs)
*   `!poll` (check output / status; accepts optional `sessionId`; `/bash poll` also works)
*   `!stop` (stop the running bash job; accepts optional `sessionId`; `/bash stop` also works)

Notes:

*   Commands accept an optional `:` between the command and args (e.g. `/think: high`, `/send: on`, `/help:`).
*   `/new <model>` accepts a model alias, `provider/model`, or a provider name (fuzzy match); if no match, the text is treated as the message body.
*   For full provider usage breakdown, use `openclaw status --usage`.
*   `/allowlist add|remove` requires `commands.config=true` and honors channel `configWrites`.
*   `/usage` controls the per-response usage footer; `/usage cost` prints a local cost summary from OpenClaw session logs.
*   `/restart` is enabled by default; set `commands.restart: false` to disable it.
*   Discord-only native command: `/vc join|leave|status` controls voice channels (requires `channels.discord.voice` and native commands; not available as text).
*   Discord thread-binding commands (`/focus`, `/unfocus`, `/agents`, `/session idle`, `/session max-age`) require effective thread bindings to be enabled (`session.threadBindings.enabled` and/or `channels.discord.threadBindings.enabled`).
*   ACP command reference and runtime behavior: [ACP Agents](https://docs.openclaw.ai/tools/acp-agents).
*   `/verbose` is meant for debugging and extra visibility; keep it **off** in normal use.
*   Tool failure summaries are still shown when relevant, but detailed failure text is only included when `/verbose` is `on` or `full`.
*   `/reasoning` (and `/verbose`) are risky in group settings: they may reveal internal reasoning or tool output you did not intend to expose. Prefer leaving them off, especially in group chats.
*   **Fast path:** command-only messages from allowlisted senders are handled immediately (bypass queue + model).
*   **Group mention gating:** command-only messages from allowlisted senders bypass mention requirements.
*   **Inline shortcuts (allowlisted senders only):** certain commands also work when embedded in a normal message and are stripped before the model sees the remaining text.
    *   Example: `hey /status` triggers a status reply, and the remaining text continues through the normal flow.
*   Currently: `/help`, `/commands`, `/status`, `/whoami` (`/id`).
*   Unauthorized command-only messages are silently ignored, and inline `/...` tokens are treated as plain text.
*   **Skill commands:** `user-invocable` skills are exposed as slash commands. Names are sanitized to `a-z0-9_` (max 32 chars); collisions get numeric suffixes (e.g. `_2`).
    *   `/skill <name> [input]` runs a skill by name (useful when native command limits prevent per-skill commands).
    *   By default, skill commands are forwarded to the model as a normal request.
    *   Skills may optionally declare `command-dispatch: tool` to route the command directly to a tool (deterministic, no model).
    *   Example: `/prose` (OpenProse plugin) — see [OpenProse](https://docs.openclaw.ai/prose).
*   **Native command arguments:** Discord uses autocomplete for dynamic options (and button menus when you omit required args). Telegram and Slack show a button menu when a command supports choices and you omit the arg.

## Usage surfaces (what shows where)

*   **Provider usage/quota** (example: “Claude 80% left”) shows up in `/status` for the current model provider when usage tracking is enabled.
*   **Per-response tokens/cost** is controlled by `/usage off|tokens|full` (appended to normal replies).
*   `/model status` is about **models/auth/endpoints**, not usage.

## Model selection (`/model`)

`/model` is implemented as a directive. Examples:

```
/model
/model list
/model 3
/model openai/gpt-5.2
/model opus@anthropic:default
/model status
```

Notes:

*   `/model` and `/model list` show a compact, numbered picker (model family + available providers).
*   On Discord, `/model` and `/models` open an interactive picker with provider and model dropdowns plus a Submit step.
*   `/model <#>` selects from that picker (and prefers the current provider when possible).
*   `/model status` shows the detailed view, including configured provider endpoint (`baseUrl`) and API mode (`api`) when available.

## Debug overrides

`/debug` lets you set **runtime-only** config overrides (memory, not disk). Owner-only. Disabled by default; enable with `commands.debug: true`. Examples:

```
/debug show
/debug set messages.responsePrefix="[openclaw]"
/debug set channels.whatsapp.allowFrom=["+1555","+4477"]
/debug unset messages.responsePrefix
/debug reset
```

Notes:

*   Overrides apply immediately to new config reads, but do **not** write to `openclaw.json`.
*   Use `/debug reset` to clear all overrides and return to the on-disk config.

## Config updates

`/config` writes to your on-disk config (`openclaw.json`). Owner-only. Disabled by default; enable with `commands.config: true`. Examples:

```
/config show
/config show messages.responsePrefix
/config get messages.responsePrefix
/config set messages.responsePrefix="[openclaw]"
/config unset messages.responsePrefix
```

Notes:

*   Config is validated before write; invalid changes are rejected.
*   `/config` updates persist across restarts.

## Surface notes

*   **Text commands** run in the normal chat session (DMs share `main`, groups have their own session).
*   **Native commands** use isolated sessions:
    *   Discord: `agent:<agentId>:discord:slash:<userId>`
    *   Slack: `agent:<agentId>:slack:slash:<userId>` (prefix configurable via `channels.slack.slashCommand.sessionPrefix`)
    *   Telegram: `telegram:slash:<userId>` (targets the chat session via `CommandTargetSessionKey`)
*   **`/stop`** targets the active chat session so it can abort the current run.
*   **Slack:** `channels.slack.slashCommand` is still supported for a single `/openclaw`\-style command. If you enable `commands.native`, you must create one Slack slash command per built-in command (same names as `/help`). Command argument menus for Slack are delivered as ephemeral Block Kit buttons.
    *   Slack native exception: register `/agentstatus` (not `/status`) because Slack reserves `/status`. Text `/status` still works in Slack messages.

---

<!-- SOURCE: https://docs.openclaw.ai/tts -->

# Text-to-Speech - OpenClaw

OpenClaw can convert outbound replies into audio using ElevenLabs, OpenAI, or Edge TTS. It works anywhere OpenClaw can send audio; Telegram gets a round voice-note bubble.

## Supported services

*   **ElevenLabs** (primary or fallback provider)
*   **OpenAI** (primary or fallback provider; also used for summaries)
*   **Edge TTS** (primary or fallback provider; uses `node-edge-tts`, default when no API keys)

### Edge TTS notes

Edge TTS uses Microsoft Edge’s online neural TTS service via the `node-edge-tts` library. It’s a hosted service (not local), uses Microsoft’s endpoints, and does not require an API key. `node-edge-tts` exposes speech configuration options and output formats, but not all options are supported by the Edge service. citeturn2search0 Because Edge TTS is a public web service without a published SLA or quota, treat it as best-effort. If you need guaranteed limits and support, use OpenAI or ElevenLabs. Microsoft’s Speech REST API documents a 10‑minute audio limit per request; Edge TTS does not publish limits, so assume similar or lower limits. citeturn0search3

## Optional keys

If you want OpenAI or ElevenLabs:

*   `ELEVENLABS_API_KEY` (or `XI_API_KEY`)
*   `OPENAI_API_KEY`

Edge TTS does **not** require an API key. If no API keys are found, OpenClaw defaults to Edge TTS (unless disabled via `messages.tts.edge.enabled=false`). If multiple providers are configured, the selected provider is used first and the others are fallback options. Auto-summary uses the configured `summaryModel` (or `agents.defaults.model.primary`), so that provider must also be authenticated if you enable summaries.

## Service links

*   [OpenAI Text-to-Speech guide](https://platform.openai.com/docs/guides/text-to-speech)
*   [OpenAI Audio API reference](https://platform.openai.com/docs/api-reference/audio)
*   [ElevenLabs Text to Speech](https://elevenlabs.io/docs/api-reference/text-to-speech)
*   [ElevenLabs Authentication](https://elevenlabs.io/docs/api-reference/authentication)
*   [node-edge-tts](https://github.com/SchneeHertz/node-edge-tts)
*   [Microsoft Speech output formats](https://learn.microsoft.com/azure/ai-services/speech-service/rest-text-to-speech#audio-outputs)

## Is it enabled by default?

No. Auto‑TTS is **off** by default. Enable it in config with `messages.tts.auto` or per session with `/tts always` (alias: `/tts on`). Edge TTS **is** enabled by default once TTS is on, and is used automatically when no OpenAI or ElevenLabs API keys are available.

## Config

TTS config lives under `messages.tts` in `openclaw.json`. Full schema is in [Gateway configuration](https://docs.openclaw.ai/gateway/configuration).

### Minimal config (enable + provider)

```
{
  messages: {
    tts: {
      auto: "always",
      provider: "elevenlabs",
    },
  },
}
```

### OpenAI primary with ElevenLabs fallback

```
{
  messages: {
    tts: {
      auto: "always",
      provider: "openai",
      summaryModel: "openai/gpt-4.1-mini",
      modelOverrides: {
        enabled: true,
      },
      openai: {
        apiKey: "openai_api_key",
        baseUrl: "https://api.openai.com/v1",
        model: "gpt-4o-mini-tts",
        voice: "alloy",
      },
      elevenlabs: {
        apiKey: "elevenlabs_api_key",
        baseUrl: "https://api.elevenlabs.io",
        voiceId: "voice_id",
        modelId: "eleven_multilingual_v2",
        seed: 42,
        applyTextNormalization: "auto",
        languageCode: "en",
        voiceSettings: {
          stability: 0.5,
          similarityBoost: 0.75,
          style: 0.0,
          useSpeakerBoost: true,
          speed: 1.0,
        },
      },
    },
  },
}
```

### Edge TTS primary (no API key)

```
{
  messages: {
    tts: {
      auto: "always",
      provider: "edge",
      edge: {
        enabled: true,
        voice: "en-US-MichelleNeural",
        lang: "en-US",
        outputFormat: "audio-24khz-48kbitrate-mono-mp3",
        rate: "+10%",
        pitch: "-5%",
      },
    },
  },
}
```

### Disable Edge TTS

```
{
  messages: {
    tts: {
      edge: {
        enabled: false,
      },
    },
  },
}
```

### Custom limits + prefs path

```
{
  messages: {
    tts: {
      auto: "always",
      maxTextLength: 4000,
      timeoutMs: 30000,
      prefsPath: "~/.openclaw/settings/tts.json",
    },
  },
}
```

### Only reply with audio after an inbound voice note

```
{
  messages: {
    tts: {
      auto: "inbound",
    },
  },
}
```

```
{
  messages: {
    tts: {
      auto: "always",
    },
  },
}
```

Then run:

### Notes on fields

*   `auto`: auto‑TTS mode (`off`, `always`, `inbound`, `tagged`).
    *   `inbound` only sends audio after an inbound voice note.
    *   `tagged` only sends audio when the reply includes `[[tts]]` tags.
*   `enabled`: legacy toggle (doctor migrates this to `auto`).
*   `mode`: `"final"` (default) or `"all"` (includes tool/block replies).
*   `provider`: `"elevenlabs"`, `"openai"`, or `"edge"` (fallback is automatic).
*   If `provider` is **unset**, OpenClaw prefers `openai` (if key), then `elevenlabs` (if key), otherwise `edge`.
*   `summaryModel`: optional cheap model for auto-summary; defaults to `agents.defaults.model.primary`.
    *   Accepts `provider/model` or a configured model alias.
*   `modelOverrides`: allow the model to emit TTS directives (on by default).
    *   `allowProvider` defaults to `false` (provider switching is opt-in).
*   `maxTextLength`: hard cap for TTS input (chars). `/tts audio` fails if exceeded.
*   `timeoutMs`: request timeout (ms).
*   `prefsPath`: override the local prefs JSON path (provider/limit/summary).
*   `apiKey` values fall back to env vars (`ELEVENLABS_API_KEY`/`XI_API_KEY`, `OPENAI_API_KEY`).
*   `elevenlabs.baseUrl`: override ElevenLabs API base URL.
*   `openai.baseUrl`: override the OpenAI TTS endpoint.
    *   Resolution order: `messages.tts.openai.baseUrl` -> `OPENAI_TTS_BASE_URL` -> `https://api.openai.com/v1`
    *   Non-default values are treated as OpenAI-compatible TTS endpoints, so custom model and voice names are accepted.
*   `elevenlabs.voiceSettings`:
    *   `stability`, `similarityBoost`, `style`: `0..1`
    *   `useSpeakerBoost`: `true|false`
    *   `speed`: `0.5..2.0` (1.0 = normal)
*   `elevenlabs.applyTextNormalization`: `auto|on|off`
*   `elevenlabs.languageCode`: 2-letter ISO 639-1 (e.g. `en`, `de`)
*   `elevenlabs.seed`: integer `0..4294967295` (best-effort determinism)
*   `edge.enabled`: allow Edge TTS usage (default `true`; no API key).
*   `edge.voice`: Edge neural voice name (e.g. `en-US-MichelleNeural`).
*   `edge.lang`: language code (e.g. `en-US`).
*   `edge.outputFormat`: Edge output format (e.g. `audio-24khz-48kbitrate-mono-mp3`).
    *   See Microsoft Speech output formats for valid values; not all formats are supported by Edge.
*   `edge.rate` / `edge.pitch` / `edge.volume`: percent strings (e.g. `+10%`, `-5%`).
*   `edge.saveSubtitles`: write JSON subtitles alongside the audio file.
*   `edge.proxy`: proxy URL for Edge TTS requests.
*   `edge.timeoutMs`: request timeout override (ms).

## Model-driven overrides (default on)

By default, the model **can** emit TTS directives for a single reply. When `messages.tts.auto` is `tagged`, these directives are required to trigger audio. When enabled, the model can emit `[[tts:...]]` directives to override the voice for a single reply, plus an optional `[[tts:text]]...[[/tts:text]]` block to provide expressive tags (laughter, singing cues, etc) that should only appear in the audio. `provider=...` directives are ignored unless `modelOverrides.allowProvider: true`. Example reply payload:

```
Here you go.

[[tts:voiceId=pMsXgVXv3BLzUgSXRplE model=eleven_v3 speed=1.1]]
[[tts:text]](laughs) Read the song once more.[[/tts:text]]
```

Available directive keys (when enabled):

*   `provider` (`openai` | `elevenlabs` | `edge`, requires `allowProvider: true`)
*   `voice` (OpenAI voice) or `voiceId` (ElevenLabs)
*   `model` (OpenAI TTS model or ElevenLabs model id)
*   `stability`, `similarityBoost`, `style`, `speed`, `useSpeakerBoost`
*   `applyTextNormalization` (`auto|on|off`)
*   `languageCode` (ISO 639-1)
*   `seed`

Disable all model overrides:

```
{
  messages: {
    tts: {
      modelOverrides: {
        enabled: false,
      },
    },
  },
}
```

Optional allowlist (enable provider switching while keeping other knobs configurable):

```
{
  messages: {
    tts: {
      modelOverrides: {
        enabled: true,
        allowProvider: true,
        allowSeed: false,
      },
    },
  },
}
```

## Per-user preferences

Slash commands write local overrides to `prefsPath` (default: `~/.openclaw/settings/tts.json`, override with `OPENCLAW_TTS_PREFS` or `messages.tts.prefsPath`). Stored fields:

*   `enabled`
*   `provider`
*   `maxLength` (summary threshold; default 1500 chars)
*   `summarize` (default `true`)

These override `messages.tts.*` for that host.

## Output formats (fixed)

*   **Telegram**: Opus voice note (`opus_48000_64` from ElevenLabs, `opus` from OpenAI).
    *   48kHz / 64kbps is a good voice-note tradeoff and required for the round bubble.
*   **Other channels**: MP3 (`mp3_44100_128` from ElevenLabs, `mp3` from OpenAI).
    *   44.1kHz / 128kbps is the default balance for speech clarity.
*   **Edge TTS**: uses `edge.outputFormat` (default `audio-24khz-48kbitrate-mono-mp3`).
    *   `node-edge-tts` accepts an `outputFormat`, but not all formats are available from the Edge service. citeturn2search0
    *   Output format values follow Microsoft Speech output formats (including Ogg/WebM Opus). citeturn1search0
    *   Telegram `sendVoice` accepts OGG/MP3/M4A; use OpenAI/ElevenLabs if you need guaranteed Opus voice notes. citeturn1search1
    *   If the configured Edge output format fails, OpenClaw retries with MP3.

OpenAI/ElevenLabs formats are fixed; Telegram expects Opus for voice-note UX.

## Auto-TTS behavior

When enabled, OpenClaw:

*   skips TTS if the reply already contains media or a `MEDIA:` directive.
*   skips very short replies (< 10 chars).
*   summarizes long replies when enabled using `agents.defaults.model.primary` (or `summaryModel`).
*   attaches the generated audio to the reply.

If the reply exceeds `maxLength` and summary is off (or no API key for the summary model), audio is skipped and the normal text reply is sent.

## Flow diagram

```
Reply -> TTS enabled?
  no  -> send text
  yes -> has media / MEDIA: / short?
          yes -> send text
          no  -> length > limit?
                   no  -> TTS -> attach audio
                   yes -> summary enabled?
                            no  -> send text
                            yes -> summarize (summaryModel or agents.defaults.model.primary)
                                      -> TTS -> attach audio
```

## Slash command usage

There is a single command: `/tts`. See [Slash commands](https://docs.openclaw.ai/tools/slash-commands) for enablement details. Discord note: `/tts` is a built-in Discord command, so OpenClaw registers `/voice` as the native command there. Text `/tts ...` still works.

```
/tts off
/tts always
/tts inbound
/tts tagged
/tts status
/tts provider openai
/tts limit 2000
/tts summary off
/tts audio Hello from OpenClaw
```

Notes:

*   Commands require an authorized sender (allowlist/owner rules still apply).
*   `commands.text` or native command registration must be enabled.
*   `off|always|inbound|tagged` are per‑session toggles (`/tts on` is an alias for `/tts always`).
*   `limit` and `summary` are stored in local prefs, not the main config.
*   `/tts audio` generates a one-off audio reply (does not toggle TTS on).

The `tts` tool converts text to speech and returns a `MEDIA:` path. When the result is Telegram-compatible, the tool includes `[[audio_as_voice]]` so Telegram sends a voice bubble.

## Gateway RPC

Gateway methods:

*   `tts.status`
*   `tts.enable`
*   `tts.disable`
*   `tts.convert`
*   `tts.setProvider`
*   `tts.providers`

---

<!-- SOURCE: https://docs.openclaw.ai/tools/skills-config -->

# Skills Config - OpenClaw

All skills-related configuration lives under `skills` in `~/.openclaw/openclaw.json`.

```
{
  skills: {
    allowBundled: ["gemini", "peekaboo"],
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills", "~/Projects/oss/some-skill-pack/skills"],
      watch: true,
      watchDebounceMs: 250,
    },
    install: {
      preferBrew: true,
      nodeManager: "npm", // npm | pnpm | yarn | bun (Gateway runtime still Node; bun not recommended)
    },
    entries: {
      "nano-banana-pro": {
        enabled: true,
        apiKey: { source: "env", provider: "default", id: "GEMINI_API_KEY" }, // or plaintext string
        env: {
          GEMINI_API_KEY: "GEMINI_KEY_HERE",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

## Fields

*   `allowBundled`: optional allowlist for **bundled** skills only. When set, only bundled skills in the list are eligible (managed/workspace skills unaffected).
*   `load.extraDirs`: additional skill directories to scan (lowest precedence).
*   `load.watch`: watch skill folders and refresh the skills snapshot (default: true).
*   `load.watchDebounceMs`: debounce for skill watcher events in milliseconds (default: 250).
*   `install.preferBrew`: prefer brew installers when available (default: true).
*   `install.nodeManager`: node installer preference (`npm` | `pnpm` | `yarn` | `bun`, default: npm). This only affects **skill installs**; the Gateway runtime should still be Node (Bun not recommended for WhatsApp/Telegram).
*   `entries.<skillKey>`: per-skill overrides.

Per-skill fields:

*   `enabled`: set `false` to disable a skill even if it’s bundled/installed.
*   `env`: environment variables injected for the agent run (only if not already set).
*   `apiKey`: optional convenience for skills that declare a primary env var. Supports plaintext string or SecretRef object (`{ source, provider, id }`).

## Notes

*   Keys under `entries` map to the skill name by default. If a skill defines `metadata.openclaw.skillKey`, use that key instead.
*   Changes to skills are picked up on the next agent turn when the watcher is enabled.

### Sandboxed skills + env vars

When a session is **sandboxed**, skill processes run inside Docker. The sandbox does **not** inherit the host `process.env`. Use one of:

*   `agents.defaults.sandbox.docker.env` (or per-agent `agents.list[].sandbox.docker.env`)
*   bake the env into your custom sandbox image

Global `env` and `skills.entries.<skill>.env/apiKey` apply to **host** runs only.

---

<!-- SOURCE: https://docs.openclaw.ai/tools/clawhub -->

# ClawHub - OpenClaw

ClawHub is the **public skill registry for OpenClaw**. It is a free service: all skills are public, open, and visible to everyone for sharing and reuse. A skill is just a folder with a `SKILL.md` file (plus supporting text files). You can browse skills in the web app or use the CLI to search, install, update, and publish skills. Site: [clawhub.ai](https://clawhub.ai/)

## What ClawHub is

*   A public registry for OpenClaw skills.
*   A versioned store of skill bundles and metadata.
*   A discovery surface for search, tags, and usage signals.

## How it works

1.  A user publishes a skill bundle (files + metadata).
2.  ClawHub stores the bundle, parses metadata, and assigns a version.
3.  The registry indexes the skill for search and discovery.
4.  Users browse, download, and install skills in OpenClaw.

## What you can do

*   Publish new skills and new versions of existing skills.
*   Discover skills by name, tags, or search.
*   Download skill bundles and inspect their files.
*   Report skills that are abusive or unsafe.
*   If you are a moderator, hide, unhide, delete, or ban.

## Who this is for (beginner-friendly)

If you want to add new capabilities to your OpenClaw agent, ClawHub is the easiest way to find and install skills. You do not need to know how the backend works. You can:

*   Search for skills by plain language.
*   Install a skill into your workspace.
*   Update skills later with one command.
*   Back up your own skills by publishing them.

## Quick start (non-technical)

1.  Install the CLI (see next section).
2.  Search for something you need:
    *   `clawhub search "calendar"`
3.  Install a skill:
    *   `clawhub install <skill-slug>`
4.  Start a new OpenClaw session so it picks up the new skill.

## Install the CLI

Pick one:

## How it fits into OpenClaw

By default, the CLI installs skills into `./skills` under your current working directory. If a OpenClaw workspace is configured, `clawhub` falls back to that workspace unless you override `--workdir` (or `CLAWHUB_WORKDIR`). OpenClaw loads workspace skills from `<workspace>/skills` and will pick them up in the **next** session. If you already use `~/.openclaw/skills` or bundled skills, workspace skills take precedence. For more detail on how skills are loaded, shared, and gated, see [Skills](https://docs.openclaw.ai/tools/skills).

## Skill system overview

A skill is a versioned bundle of files that teaches OpenClaw how to perform a specific task. Each publish creates a new version, and the registry keeps a history of versions so users can audit changes. A typical skill includes:

*   A `SKILL.md` file with the primary description and usage.
*   Optional configs, scripts, or supporting files used by the skill.
*   Metadata such as tags, summary, and install requirements.

ClawHub uses metadata to power discovery and safely expose skill capabilities. The registry also tracks usage signals (such as stars and downloads) to improve ranking and visibility.

## What the service provides (features)

*   **Public browsing** of skills and their `SKILL.md` content.
*   **Search** powered by embeddings (vector search), not just keywords.
*   **Versioning** with semver, changelogs, and tags (including `latest`).
*   **Downloads** as a zip per version.
*   **Stars and comments** for community feedback.
*   **Moderation** hooks for approvals and audits.
*   **CLI-friendly API** for automation and scripting.

## Security and moderation

ClawHub is open by default. Anyone can upload skills, but a GitHub account must be at least one week old to publish. This helps slow down abuse without blocking legitimate contributors. Reporting and moderation:

*   Any signed in user can report a skill.
*   Report reasons are required and recorded.
*   Each user can have up to 20 active reports at a time.
*   Skills with more than 3 unique reports are auto hidden by default.
*   Moderators can view hidden skills, unhide them, delete them, or ban users.
*   Abusing the report feature can result in account bans.

Interested in becoming a moderator? Ask in the OpenClaw Discord and contact a moderator or maintainer.

## CLI commands and parameters

Global options (apply to all commands):

*   `--workdir <dir>`: Working directory (default: current dir; falls back to OpenClaw workspace).
*   `--dir <dir>`: Skills directory, relative to workdir (default: `skills`).
*   `--site <url>`: Site base URL (browser login).
*   `--registry <url>`: Registry API base URL.
*   `--no-input`: Disable prompts (non-interactive).
*   `-V, --cli-version`: Print CLI version.

Auth:

*   `clawhub login` (browser flow) or `clawhub login --token <token>`
*   `clawhub logout`
*   `clawhub whoami`

Options:

*   `--token <token>`: Paste an API token.
*   `--label <label>`: Label stored for browser login tokens (default: `CLI token`).
*   `--no-browser`: Do not open a browser (requires `--token`).

Search:

*   `clawhub search "query"`
*   `--limit <n>`: Max results.

Install:

*   `clawhub install <slug>`
*   `--version <version>`: Install a specific version.
*   `--force`: Overwrite if the folder already exists.

Update:

*   `clawhub update <slug>`
*   `clawhub update --all`
*   `--version <version>`: Update to a specific version (single slug only).
*   `--force`: Overwrite when local files do not match any published version.

List:

*   `clawhub list` (reads `.clawhub/lock.json`)

Publish:

*   `clawhub publish <path>`
*   `--slug <slug>`: Skill slug.
*   `--name <name>`: Display name.
*   `--version <version>`: Semver version.
*   `--changelog <text>`: Changelog text (can be empty).
*   `--tags <tags>`: Comma-separated tags (default: `latest`).

Delete/undelete (owner/admin only):

*   `clawhub delete <slug> --yes`
*   `clawhub undelete <slug> --yes`

Sync (scan local skills + publish new/updated):

*   `clawhub sync`
*   `--root <dir...>`: Extra scan roots.
*   `--all`: Upload everything without prompts.
*   `--dry-run`: Show what would be uploaded.
*   `--bump <type>`: `patch|minor|major` for updates (default: `patch`).
*   `--changelog <text>`: Changelog for non-interactive updates.
*   `--tags <tags>`: Comma-separated tags (default: `latest`).
*   `--concurrency <n>`: Registry checks (default: 4).

## Common workflows for agents

### Search for skills

```
clawhub search "postgres backups"
```

### Download new skills

```
clawhub install my-skill-pack
```

### Update installed skills

### Back up your skills (publish or sync)

For a single skill folder:

```
clawhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.0.0 --tags latest
```

To scan and back up many skills at once:

## Advanced details (technical)

### Versioning and tags

*   Each publish creates a new **semver** `SkillVersion`.
*   Tags (like `latest`) point to a version; moving tags lets you roll back.
*   Changelogs are attached per version and can be empty when syncing or publishing updates.

### Local changes vs registry versions

Updates compare the local skill contents to registry versions using a content hash. If local files do not match any published version, the CLI asks before overwriting (or requires `--force` in non-interactive runs).

### Sync scanning and fallback roots

`clawhub sync` scans your current workdir first. If no skills are found, it falls back to known legacy locations (for example `~/openclaw/skills` and `~/.openclaw/skills`). This is designed to find older skill installs without extra flags.

### Storage and lockfile

*   Installed skills are recorded in `.clawhub/lock.json` under your workdir.
*   Auth tokens are stored in the ClawHub CLI config file (override via `CLAWHUB_CONFIG_PATH`).

### Telemetry (install counts)

When you run `clawhub sync` while logged in, the CLI sends a minimal snapshot to compute install counts. You can disable this entirely:

```
export CLAWHUB_DISABLE_TELEMETRY=1
```

## Environment variables

*   `CLAWHUB_SITE`: Override the site URL.
*   `CLAWHUB_REGISTRY`: Override the registry API URL.
*   `CLAWHUB_CONFIG_PATH`: Override where the CLI stores the token/config.
*   `CLAWHUB_WORKDIR`: Override the default workdir.
*   `CLAWHUB_DISABLE_TELEMETRY=1`: Disable telemetry on `sync`.

---

<!-- SOURCE: https://docs.openclaw.ai/tools/pdf -->

# PDF Tool - OpenClaw

`pdf` analyzes one or more PDF documents and returns text. Quick behavior:

*   Native provider mode for Anthropic and Google model providers.
*   Extraction fallback mode for other providers (extract text first, then page images when needed).
*   Supports single (`pdf`) or multi (`pdfs`) input, max 10 PDFs per call.

## Availability

The tool is only registered when OpenClaw can resolve a PDF-capable model config for the agent:

1.  `agents.defaults.pdfModel`
2.  fallback to `agents.defaults.imageModel`
3.  fallback to best effort provider defaults based on available auth

If no usable model can be resolved, the `pdf` tool is not exposed.

## Input reference

*   `pdf` (`string`): one PDF path or URL
*   `pdfs` (`string[]`): multiple PDF paths or URLs, up to 10 total
*   `prompt` (`string`): analysis prompt, default `Analyze this PDF document.`
*   `pages` (`string`): page filter like `1-5` or `1,3,7-9`
*   `model` (`string`): optional model override (`provider/model`)
*   `maxBytesMb` (`number`): per-PDF size cap in MB

Input notes:

*   `pdf` and `pdfs` are merged and deduplicated before loading.
*   If no PDF input is provided, the tool errors.
*   `pages` is parsed as 1-based page numbers, deduped, sorted, and clamped to the configured max pages.
*   `maxBytesMb` defaults to `agents.defaults.pdfMaxBytesMb` or `10`.

## Supported PDF references

*   local file path (including `~` expansion)
*   `file://` URL
*   `http://` and `https://` URL

Reference notes:

*   Other URI schemes (for example `ftp://`) are rejected with `unsupported_pdf_reference`.
*   In sandbox mode, remote `http(s)` URLs are rejected.
*   With workspace-only file policy enabled, local file paths outside allowed roots are rejected.

## Execution modes

### Native provider mode

Native mode is used for provider `anthropic` and `google`. The tool sends raw PDF bytes directly to provider APIs. Native mode limits:

*   `pages` is not supported. If set, the tool returns an error.

Fallback mode is used for non-native providers. Flow:

1.  Extract text from selected pages (up to `agents.defaults.pdfMaxPages`, default `20`).
2.  If extracted text length is below `200` chars, render selected pages to PNG images and include them.
3.  Send extracted content plus prompt to the selected model.

Fallback details:

*   Page image extraction uses a pixel budget of `4,000,000`.
*   If the target model does not support image input and there is no extractable text, the tool errors.
*   Extraction fallback requires `pdfjs-dist` (and `@napi-rs/canvas` for image rendering).

## Config

```
{
  agents: {
    defaults: {
      pdfModel: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["openai/gpt-5-mini"],
      },
      pdfMaxBytesMb: 10,
      pdfMaxPages: 20,
    },
  },
}
```

See [Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference) for full field details.

## Output details

The tool returns text in `content[0].text` and structured metadata in `details`. Common `details` fields:

*   `model`: resolved model ref (`provider/model`)
*   `native`: `true` for native provider mode, `false` for fallback
*   `attempts`: fallback attempts that failed before success

Path fields:

*   single PDF input: `details.pdf`
*   multiple PDF inputs: `details.pdfs[]` with `pdf` entries
*   sandbox path rewrite metadata (when applicable): `rewrittenFrom`

## Error behavior

*   Missing PDF input: throws `pdf required: provide a path or URL to a PDF document`
*   Too many PDFs: returns structured error in `details.error = "too_many_pdfs"`
*   Unsupported reference scheme: returns `details.error = "unsupported_pdf_reference"`
*   Native mode with `pages`: throws clear `pages is not supported with native PDF providers` error

## Examples

Single PDF:

```
{
  "pdf": "/tmp/report.pdf",
  "prompt": "Summarize this report in 5 bullets"
}
```

Multiple PDFs:

```
{
  "pdfs": ["/tmp/q1.pdf", "/tmp/q2.pdf"],
  "prompt": "Compare risks and timeline changes across both documents"
}
```

Page-filtered fallback model:

```
{
  "pdf": "https://example.com/report.pdf",
  "pages": "1-3,7",
  "model": "openai/gpt-5-mini",
  "prompt": "Extract only customer-impacting incidents"
}
```

---

<!-- SOURCE: https://docs.openclaw.ai/tools/firecrawl -->

# Firecrawl - OpenClaw

OpenClaw can use **Firecrawl** as a fallback extractor for `web_fetch`. It is a hosted content extraction service that supports bot circumvention and caching, which helps with JS-heavy sites or pages that block plain HTTP fetches.

## Get an API key

1.  Create a Firecrawl account and generate an API key.
2.  Store it in config or set `FIRECRAWL_API_KEY` in the gateway environment.

## Configure Firecrawl

```
{
  tools: {
    web: {
      fetch: {
        firecrawl: {
          apiKey: "FIRECRAWL_API_KEY_HERE",
          baseUrl: "https://api.firecrawl.dev",
          onlyMainContent: true,
          maxAgeMs: 172800000,
          timeoutSeconds: 60,
        },
      },
    },
  },
}
```

Notes:

*   `firecrawl.enabled` defaults to true when an API key is present.
*   `maxAgeMs` controls how old cached results can be (ms). Default is 2 days.

## Stealth / bot circumvention

Firecrawl exposes a **proxy mode** parameter for bot circumvention (`basic`, `stealth`, or `auto`). OpenClaw always uses `proxy: "auto"` plus `storeInCache: true` for Firecrawl requests. If proxy is omitted, Firecrawl defaults to `auto`. `auto` retries with stealth proxies if a basic attempt fails, which may use more credits than basic-only scraping.

## How `web_fetch` uses Firecrawl

`web_fetch` extraction order:

1.  Readability (local)
2.  Firecrawl (if configured)
3.  Basic HTML cleanup (last fallback)

See [Web tools](https://docs.openclaw.ai/tools/web) for the full web tool setup.

---

<!-- SOURCE: https://docs.openclaw.ai/tools/web -->

# Web Tools - OpenClaw

OpenClaw ships two lightweight web tools:

*   `web_search` — Search the web using Brave Search API, Gemini with Google Search grounding, Grok, Kimi, or Perplexity Search API.
*   `web_fetch` — HTTP fetch + readable extraction (HTML → markdown/text).

These are **not** browser automation. For JS-heavy sites or logins, use the [Browser tool](https://docs.openclaw.ai/tools/browser).

## How it works

*   `web_search` calls your configured provider and returns results.
*   Results are cached by query for 15 minutes (configurable).
*   `web_fetch` does a plain HTTP GET and extracts readable content (HTML → markdown/text). It does **not** execute JavaScript.
*   `web_fetch` is enabled by default (unless explicitly disabled).

See [Brave Search setup](https://docs.openclaw.ai/brave-search) and [Perplexity Search setup](https://docs.openclaw.ai/perplexity) for provider-specific details.

## Choosing a search provider

| Provider | Result shape | Provider-specific filters | Notes | API key |
| --- | --- | --- | --- | --- |
| **Brave Search API** | Structured results with snippets | `country`, `language`, `ui_lang`, time | Supports Brave `llm-context` mode | `BRAVE_API_KEY` |
| **Gemini** | AI-synthesized answers + citations | —   | Uses Google Search grounding | `GEMINI_API_KEY` |
| **Grok** | AI-synthesized answers + citations | —   | Uses xAI web-grounded responses | `XAI_API_KEY` |
| **Kimi** | AI-synthesized answers + citations | —   | Uses Moonshot web search | `KIMI_API_KEY` / `MOONSHOT_API_KEY` |
| **Perplexity Search API** | Structured results with snippets | `country`, `language`, time, `domain_filter` | Supports content extraction controls; OpenRouter uses Sonar compatibility path | `PERPLEXITY_API_KEY` / `OPENROUTER_API_KEY` |

### Auto-detection

The table above is alphabetical. If no `provider` is explicitly set, runtime auto-detection checks providers in this order:

1.  **Brave** — `BRAVE_API_KEY` env var or `tools.web.search.apiKey` config
2.  **Gemini** — `GEMINI_API_KEY` env var or `tools.web.search.gemini.apiKey` config
3.  **Grok** — `XAI_API_KEY` env var or `tools.web.search.grok.apiKey` config
4.  **Kimi** — `KIMI_API_KEY` / `MOONSHOT_API_KEY` env var or `tools.web.search.kimi.apiKey` config
5.  **Perplexity** — `PERPLEXITY_API_KEY`, `OPENROUTER_API_KEY`, or `tools.web.search.perplexity.apiKey` config

If no keys are found, it falls back to Brave (you’ll get a missing-key error prompting you to configure one).

## Setting up web search

Use `openclaw configure --section web` to set up your API key and choose a provider.

### Brave Search

1.  Create a Brave Search API account at [brave.com/search/api](https://brave.com/search/api/)
2.  In the dashboard, choose the **Search** plan and generate an API key.
3.  Run `openclaw configure --section web` to store the key in config, or set `BRAVE_API_KEY` in your environment.

Each Brave plan includes \*\*5/monthinfreecredit∗∗(renewing).TheSearchplancosts5/month in free credit\*\* (renewing). The Search plan costs 5 per 1,000 requests, so the credit covers 1,000 queries/month. Set your usage limit in the Brave dashboard to avoid unexpected charges. See the [Brave API portal](https://brave.com/search/api/) for current plans and pricing.

### Perplexity Search

1.  Create a Perplexity account at [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)
2.  Generate an API key in the dashboard
3.  Run `openclaw configure --section web` to store the key in config, or set `PERPLEXITY_API_KEY` in your environment.

For legacy Sonar/OpenRouter compatibility, set `OPENROUTER_API_KEY` instead, or configure `tools.web.search.perplexity.apiKey` with an `sk-or-...` key. Setting `tools.web.search.perplexity.baseUrl` or `model` also opts Perplexity back into the chat-completions compatibility path. See [Perplexity Search API Docs](https://docs.perplexity.ai/guides/search-quickstart) for more details.

### Where to store the key

**Via config:** run `openclaw configure --section web`. It stores the key under `tools.web.search.apiKey` or `tools.web.search.perplexity.apiKey`, depending on provider. **Via environment:** set `PERPLEXITY_API_KEY`, `OPENROUTER_API_KEY`, or `BRAVE_API_KEY` in the Gateway process environment. For a gateway install, put it in `~/.openclaw/.env` (or your service environment). See [Env vars](https://docs.openclaw.ai/help/faq#how-does-openclaw-load-environment-variables).

### Config examples

**Brave Search:**

```
{
  tools: {
    web: {
      search: {
        enabled: true,
        provider: "brave",
        apiKey: "YOUR_BRAVE_API_KEY", // optional if BRAVE_API_KEY is set // pragma: allowlist secret
      },
    },
  },
}
```

**Brave LLM Context mode:**

```
{
  tools: {
    web: {
      search: {
        enabled: true,
        provider: "brave",
        apiKey: "YOUR_BRAVE_API_KEY", // optional if BRAVE_API_KEY is set // pragma: allowlist secret
        brave: {
          mode: "llm-context",
        },
      },
    },
  },
}
```

`llm-context` returns extracted page chunks for grounding instead of standard Brave snippets. In this mode, `country` and `language` / `search_lang` still work, but `ui_lang`, `freshness`, `date_after`, and `date_before` are rejected. **Perplexity Search:**

```
{
  tools: {
    web: {
      search: {
        enabled: true,
        provider: "perplexity",
        perplexity: {
          apiKey: "pplx-...", // optional if PERPLEXITY_API_KEY is set
        },
      },
    },
  },
}
```

**Perplexity via OpenRouter / Sonar compatibility:**

```
{
  tools: {
    web: {
      search: {
        enabled: true,
        provider: "perplexity",
        perplexity: {
          apiKey: "<openrouter-api-key>", // optional if OPENROUTER_API_KEY is set
          baseUrl: "https://openrouter.ai/api/v1",
          model: "perplexity/sonar-pro",
        },
      },
    },
  },
}
```

## Using Gemini (Google Search grounding)

Gemini models support built-in [Google Search grounding](https://ai.google.dev/gemini-api/docs/grounding), which returns AI-synthesized answers backed by live Google Search results with citations.

### Getting a Gemini API key

1.  Go to [Google AI Studio](https://aistudio.google.com/apikey)
2.  Create an API key
3.  Set `GEMINI_API_KEY` in the Gateway environment, or configure `tools.web.search.gemini.apiKey`

### Setting up Gemini search

```
{
  tools: {
    web: {
      search: {
        provider: "gemini",
        gemini: {
          // API key (optional if GEMINI_API_KEY is set)
          apiKey: "AIza...",
          // Model (defaults to "gemini-2.5-flash")
          model: "gemini-2.5-flash",
        },
      },
    },
  },
}
```

**Environment alternative:** set `GEMINI_API_KEY` in the Gateway environment. For a gateway install, put it in `~/.openclaw/.env`.

### Notes

*   Citation URLs from Gemini grounding are automatically resolved from Google’s redirect URLs to direct URLs.
*   Redirect resolution uses the SSRF guard path (HEAD + redirect checks + http/https validation) before returning the final citation URL.
*   Redirect resolution uses strict SSRF defaults, so redirects to private/internal targets are blocked.
*   The default model (`gemini-2.5-flash`) is fast and cost-effective. Any Gemini model that supports grounding can be used.

## web\_search

Search the web using your configured provider.

### Requirements

*   `tools.web.search.enabled` must not be `false` (default: enabled)
*   API key for your chosen provider:
    *   **Brave**: `BRAVE_API_KEY` or `tools.web.search.apiKey`
    *   **Gemini**: `GEMINI_API_KEY` or `tools.web.search.gemini.apiKey`
    *   **Grok**: `XAI_API_KEY` or `tools.web.search.grok.apiKey`
    *   **Kimi**: `KIMI_API_KEY`, `MOONSHOT_API_KEY`, or `tools.web.search.kimi.apiKey`
    *   **Perplexity**: `PERPLEXITY_API_KEY`, `OPENROUTER_API_KEY`, or `tools.web.search.perplexity.apiKey`

### Config

```
{
  tools: {
    web: {
      search: {
        enabled: true,
        apiKey: "BRAVE_API_KEY_HERE", // optional if BRAVE_API_KEY is set
        maxResults: 5,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
      },
    },
  },
}
```

### Tool parameters

All parameters work for Brave and for native Perplexity Search API unless noted. Perplexity’s OpenRouter / Sonar compatibility path supports only `query` and `freshness`. If you set `tools.web.search.perplexity.baseUrl` / `model`, use `OPENROUTER_API_KEY`, or configure an `sk-or-...` key, Search API-only filters return explicit errors.

| Parameter | Description |
| --- | --- |
| `query` | Search query (required) |
| `count` | Results to return (1-10, default: 5) |
| `country` | 2-letter ISO country code (e.g., “US”, “DE”) |
| `language` | ISO 639-1 language code (e.g., “en”, “de”) |
| `freshness` | Time filter: `day`, `week`, `month`, or `year` |
| `date_after` | Results after this date (YYYY-MM-DD) |
| `date_before` | Results before this date (YYYY-MM-DD) |
| `ui_lang` | UI language code (Brave only) |
| `domain_filter` | Domain allowlist/denylist array (Perplexity only) |
| `max_tokens` | Total content budget, default 25000 (Perplexity only) |
| `max_tokens_per_page` | Per-page token limit, default 2048 (Perplexity only) |

**Examples:**

```
// German-specific search
await web_search({
  query: "TV online schauen",
  country: "DE",
  language: "de",
});

// Recent results (past week)
await web_search({
  query: "TMBG interview",
  freshness: "week",
});

// Date range search
await web_search({
  query: "AI developments",
  date_after: "2024-01-01",
  date_before: "2024-06-30",
});

// Domain filtering (Perplexity only)
await web_search({
  query: "climate research",
  domain_filter: ["nature.com", "science.org", ".edu"],
});

// Exclude domains (Perplexity only)
await web_search({
  query: "product reviews",
  domain_filter: ["-reddit.com", "-pinterest.com"],
});

// More content extraction (Perplexity only)
await web_search({
  query: "detailed AI research",
  max_tokens: 50000,
  max_tokens_per_page: 4096,
});
```

When Brave `llm-context` mode is enabled, `ui_lang`, `freshness`, `date_after`, and `date_before` are not supported. Use Brave `web` mode for those filters.

## web\_fetch

Fetch a URL and extract readable content.

### web\_fetch requirements

*   `tools.web.fetch.enabled` must not be `false` (default: enabled)
*   Optional Firecrawl fallback: set `tools.web.fetch.firecrawl.apiKey` or `FIRECRAWL_API_KEY`.

### web\_fetch config

```
{
  tools: {
    web: {
      fetch: {
        enabled: true,
        maxChars: 50000,
        maxCharsCap: 50000,
        maxResponseBytes: 2000000,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
        maxRedirects: 3,
        userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        readability: true,
        firecrawl: {
          enabled: true,
          apiKey: "FIRECRAWL_API_KEY_HERE", // optional if FIRECRAWL_API_KEY is set
          baseUrl: "https://api.firecrawl.dev",
          onlyMainContent: true,
          maxAgeMs: 86400000, // ms (1 day)
          timeoutSeconds: 60,
        },
      },
    },
  },
}
```

### web\_fetch tool parameters

*   `url` (required, http/https only)
*   `extractMode` (`markdown` | `text`)
*   `maxChars` (truncate long pages)

Notes:

*   `web_fetch` uses Readability (main-content extraction) first, then Firecrawl (if configured). If both fail, the tool returns an error.
*   Firecrawl requests use bot-circumvention mode and cache results by default.
*   `web_fetch` sends a Chrome-like User-Agent and `Accept-Language` by default; override `userAgent` if needed.
*   `web_fetch` blocks private/internal hostnames and re-checks redirects (limit with `maxRedirects`).
*   `maxChars` is clamped to `tools.web.fetch.maxCharsCap`.
*   `web_fetch` caps the downloaded response body size to `tools.web.fetch.maxResponseBytes` before parsing; oversized responses are truncated and include a warning.
*   `web_fetch` is best-effort extraction; some sites will need the browser tool.
*   See [Firecrawl](https://docs.openclaw.ai/tools/firecrawl) for key setup and service details.
*   Responses are cached (default 15 minutes) to reduce repeated fetches.
*   If you use tool profiles/allowlists, add `web_search`/`web_fetch` or `group:web`.
*   If the API key is missing, `web_search` returns a short setup hint with a docs link.



---

<!-- SOURCE: https://docs.openclaw.ai/tools -->

# Tools - OpenClaw

OpenClaw exposes **first-class agent tools** for browser, canvas, nodes, and cron. These replace the old `openclaw-*` skills: the tools are typed, no shelling, and the agent should rely on them directly.

You can globally allow/deny tools via `tools.allow` / `tools.deny` in `openclaw.json` (deny wins). This prevents disallowed tools from being sent to model providers.

```
{
  tools: { deny: ["browser"] },
}
```

Notes:

*   Matching is case-insensitive.
*   `*` wildcards are supported (`"*"` means all tools).
*   If `tools.allow` only references unknown or unloaded plugin tool names, OpenClaw logs a warning and ignores the allowlist so core tools stay available.

`tools.profile` sets a **base tool allowlist** before `tools.allow`/`tools.deny`. Per-agent override: `agents.list[].tools.profile`. Profiles:

*   `minimal`: `session_status` only
*   `coding`: `group:fs`, `group:runtime`, `group:sessions`, `group:memory`, `image`
*   `messaging`: `group:messaging`, `sessions_list`, `sessions_history`, `sessions_send`, `session_status`
*   `full`: no restriction (same as unset)

Example (messaging-only by default, allow Slack + Discord tools too):

```
{
  tools: {
    profile: "messaging",
    allow: ["slack", "discord"],
  },
}
```

Example (coding profile, but deny exec/process everywhere):

```
{
  tools: {
    profile: "coding",
    deny: ["group:runtime"],
  },
}
```

Example (global coding profile, messaging-only support agent):

```
{
  tools: { profile: "coding" },
  agents: {
    list: [
      {
        id: "support",
        tools: { profile: "messaging", allow: ["slack"] },
      },
    ],
  },
}
```

Use `tools.byProvider` to **further restrict** tools for specific providers (or a single `provider/model`) without changing your global defaults. Per-agent override: `agents.list[].tools.byProvider`. This is applied **after** the base tool profile and **before** allow/deny lists, so it can only narrow the tool set. Provider keys accept either `provider` (e.g. `google-antigravity`) or `provider/model` (e.g. `openai/gpt-5.2`). Example (keep global coding profile, but minimal tools for Google Antigravity):

```
{
  tools: {
    profile: "coding",
    byProvider: {
      "google-antigravity": { profile: "minimal" },
    },
  },
}
```

Example (provider/model-specific allowlist for a flaky endpoint):

```
{
  tools: {
    allow: ["group:fs", "group:runtime", "sessions_list"],
    byProvider: {
      "openai/gpt-5.2": { allow: ["group:fs", "sessions_list"] },
    },
  },
}
```

Example (agent-specific override for a single provider):

```
{
  agents: {
    list: [
      {
        id: "support",
        tools: {
          byProvider: {
            "google-antigravity": { allow: ["message", "sessions_list"] },
          },
        },
      },
    ],
  },
}
```

Tool policies (global, agent, sandbox) support `group:*` entries that expand to multiple tools. Use these in `tools.allow` / `tools.deny`. Available groups:

*   `group:runtime`: `exec`, `bash`, `process`
*   `group:fs`: `read`, `write`, `edit`, `apply_patch`
*   `group:sessions`: `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
*   `group:memory`: `memory_search`, `memory_get`
*   `group:web`: `web_search`, `web_fetch`
*   `group:ui`: `browser`, `canvas`
*   `group:automation`: `cron`, `gateway`
*   `group:messaging`: `message`
*   `group:nodes`: `nodes`
*   `group:openclaw`: all built-in OpenClaw tools (excludes provider plugins)

Example (allow only file tools + browser):

```
{
  tools: {
    allow: ["group:fs", "browser"],
  },
}
```

Plugins can register **additional tools** (and CLI commands) beyond the core set. See [Plugins](https://docs.openclaw.ai/tools/plugin) for install + config, and [Skills](https://docs.openclaw.ai/tools/skills) for how tool usage guidance is injected into prompts. Some plugins ship their own skills alongside tools (for example, the voice-call plugin). Optional plugin tools:

*   [Lobster](https://docs.openclaw.ai/tools/lobster): typed workflow runtime with resumable approvals (requires the Lobster CLI on the gateway host).
*   [LLM Task](https://docs.openclaw.ai/tools/llm-task): JSON-only LLM step for structured workflow output (optional schema validation).
*   [Diffs](https://docs.openclaw.ai/tools/diffs): read-only diff viewer and PNG or PDF file renderer for before/after text or unified patches.

### `apply_patch`

Apply structured patches across one or more files. Use for multi-hunk edits. Experimental: enable via `tools.exec.applyPatch.enabled` (OpenAI models only). `tools.exec.applyPatch.workspaceOnly` defaults to `true` (workspace-contained). Set it to `false` only if you intentionally want `apply_patch` to write/delete outside the workspace directory.

### `exec`

Run shell commands in the workspace. Core parameters:

*   `command` (required)
*   `yieldMs` (auto-background after timeout, default 10000)
*   `background` (immediate background)
*   `timeout` (seconds; kills the process if exceeded, default 1800)
*   `elevated` (bool; run on host if elevated mode is enabled/allowed; only changes behavior when the agent is sandboxed)
*   `host` (`sandbox | gateway | node`)
*   `security` (`deny | allowlist | full`)
*   `ask` (`off | on-miss | always`)
*   `node` (node id/name for `host=node`)
*   Need a real TTY? Set `pty: true`.

Notes:

*   Returns `status: "running"` with a `sessionId` when backgrounded.
*   Use `process` to poll/log/write/kill/clear background sessions.
*   If `process` is disallowed, `exec` runs synchronously and ignores `yieldMs`/`background`.
*   `elevated` is gated by `tools.elevated` plus any `agents.list[].tools.elevated` override (both must allow) and is an alias for `host=gateway` + `security=full`.
*   `elevated` only changes behavior when the agent is sandboxed (otherwise it’s a no-op).
*   `host=node` can target a macOS companion app or a headless node host (`openclaw node run`).
*   gateway/node approvals and allowlists: [Exec approvals](https://docs.openclaw.ai/tools/exec-approvals).

### `process`

Manage background exec sessions. Core actions:

*   `list`, `poll`, `log`, `write`, `kill`, `clear`, `remove`

Notes:

*   `poll` returns new output and exit status when complete.
*   `log` supports line-based `offset`/`limit` (omit `offset` to grab the last N lines).
*   `process` is scoped per agent; sessions from other agents are not visible.

### `loop-detection` (tool-call loop guardrails)

OpenClaw tracks recent tool-call history and blocks or warns when it detects repetitive no-progress loops. Enable with `tools.loopDetection.enabled: true` (default is `false`).

```
{
  tools: {
    loopDetection: {
      enabled: true,
      warningThreshold: 10,
      criticalThreshold: 20,
      globalCircuitBreakerThreshold: 30,
      historySize: 30,
      detectors: {
        genericRepeat: true,
        knownPollNoProgress: true,
        pingPong: true,
      },
    },
  },
}
```

*   `genericRepeat`: repeated same tool + same params call pattern.
*   `knownPollNoProgress`: repeating poll-like tools with identical outputs.
*   `pingPong`: alternating `A/B/A/B` no-progress patterns.
*   Per-agent override: `agents.list[].tools.loopDetection`.

### `web_search`

Search the web using Perplexity, Brave, Gemini, Grok, or Kimi. Core parameters:

*   `query` (required)
*   `count` (1–10; default from `tools.web.search.maxResults`)

Notes:

*   Requires an API key for the chosen provider (recommended: `openclaw configure --section web`).
*   Enable via `tools.web.search.enabled`.
*   Responses are cached (default 15 min).
*   See [Web tools](https://docs.openclaw.ai/tools/web) for setup.

### `web_fetch`

Fetch and extract readable content from a URL (HTML → markdown/text). Core parameters:

*   `url` (required)
*   `extractMode` (`markdown` | `text`)
*   `maxChars` (truncate long pages)

Notes:

*   Enable via `tools.web.fetch.enabled`.
*   `maxChars` is clamped by `tools.web.fetch.maxCharsCap` (default 50000).
*   Responses are cached (default 15 min).
*   For JS-heavy sites, prefer the browser tool.
*   See [Web tools](https://docs.openclaw.ai/tools/web) for setup.
*   See [Firecrawl](https://docs.openclaw.ai/tools/firecrawl) for the optional anti-bot fallback.

### `browser`

Control the dedicated OpenClaw-managed browser. Core actions:

*   `status`, `start`, `stop`, `tabs`, `open`, `focus`, `close`
*   `snapshot` (aria/ai)
*   `screenshot` (returns image block + `MEDIA:<path>`)
*   `act` (UI actions: click/type/press/hover/drag/select/fill/resize/wait/evaluate)
*   `navigate`, `console`, `pdf`, `upload`, `dialog`

Profile management:

*   `profiles` — list all browser profiles with status
*   `create-profile` — create new profile with auto-allocated port (or `cdpUrl`)
*   `delete-profile` — stop browser, delete user data, remove from config (local only)
*   `reset-profile` — kill orphan process on profile’s port (local only)

Common parameters:

*   `profile` (optional; defaults to `browser.defaultProfile`)
*   `target` (`sandbox` | `host` | `node`)
*   `node` (optional; picks a specific node id/name) Notes:
*   Requires `browser.enabled=true` (default is `true`; set `false` to disable).
*   All actions accept optional `profile` parameter for multi-instance support.
*   When `profile` is omitted, uses `browser.defaultProfile` (defaults to “chrome”).
*   Profile names: lowercase alphanumeric + hyphens only (max 64 chars).
*   Port range: 18800-18899 (~100 profiles max).
*   Remote profiles are attach-only (no start/stop/reset).
*   If a browser-capable node is connected, the tool may auto-route to it (unless you pin `target`).
*   `snapshot` defaults to `ai` when Playwright is installed; use `aria` for the accessibility tree.
*   `snapshot` also supports role-snapshot options (`interactive`, `compact`, `depth`, `selector`) which return refs like `e12`.
*   `act` requires `ref` from `snapshot` (numeric `12` from AI snapshots, or `e12` from role snapshots); use `evaluate` for rare CSS selector needs.
*   Avoid `act` → `wait` by default; use it only in exceptional cases (no reliable UI state to wait on).
*   `upload` can optionally pass a `ref` to auto-click after arming.
*   `upload` also supports `inputRef` (aria ref) or `element` (CSS selector) to set `<input type="file">` directly.

### `canvas`

Drive the node Canvas (present, eval, snapshot, A2UI). Core actions:

*   `present`, `hide`, `navigate`, `eval`
*   `snapshot` (returns image block + `MEDIA:<path>`)
*   `a2ui_push`, `a2ui_reset`

Notes:

*   Uses gateway `node.invoke` under the hood.
*   If no `node` is provided, the tool picks a default (single connected node or local mac node).
*   A2UI is v0.8 only (no `createSurface`); the CLI rejects v0.9 JSONL with line errors.
*   Quick smoke: `openclaw nodes canvas a2ui push --node <id> --text "Hello from A2UI"`.

### `nodes`

Discover and target paired nodes; send notifications; capture camera/screen. Core actions:

*   `status`, `describe`
*   `pending`, `approve`, `reject` (pairing)
*   `notify` (macOS `system.notify`)
*   `run` (macOS `system.run`)
*   `camera_list`, `camera_snap`, `camera_clip`, `screen_record`
*   `location_get`, `notifications_list`, `notifications_action`
*   `device_status`, `device_info`, `device_permissions`, `device_health`

Notes:

*   Camera/screen commands require the node app to be foregrounded.
*   Images return image blocks + `MEDIA:<path>`.
*   Videos return `FILE:<path>` (mp4).
*   Location returns a JSON payload (lat/lon/accuracy/timestamp).
*   `run` params: `command` argv array; optional `cwd`, `env` (`KEY=VAL`), `commandTimeoutMs`, `invokeTimeoutMs`, `needsScreenRecording`.

Example (`run`):

```
{
  "action": "run",
  "node": "office-mac",
  "command": ["echo", "Hello"],
  "env": ["FOO=bar"],
  "commandTimeoutMs": 12000,
  "invokeTimeoutMs": 45000,
  "needsScreenRecording": false
}
```

### `image`

Analyze an image with the configured image model. Core parameters:

*   `image` (required path or URL)
*   `prompt` (optional; defaults to “Describe the image.”)
*   `model` (optional override)
*   `maxBytesMb` (optional size cap)

Notes:

*   Only available when `agents.defaults.imageModel` is configured (primary or fallbacks), or when an implicit image model can be inferred from your default model + configured auth (best-effort pairing).
*   Uses the image model directly (independent of the main chat model).

### `pdf`

Analyze one or more PDF documents. For full behavior, limits, config, and examples, see [PDF tool](https://docs.openclaw.ai/tools/pdf).

### `message`

Send messages and channel actions across Discord/Google Chat/Slack/Telegram/WhatsApp/Signal/iMessage/MS Teams. Core actions:

*   `send` (text + optional media; MS Teams also supports `card` for Adaptive Cards)
*   `poll` (WhatsApp/Discord/MS Teams polls)
*   `react` / `reactions` / `read` / `edit` / `delete`
*   `pin` / `unpin` / `list-pins`
*   `permissions`
*   `thread-create` / `thread-list` / `thread-reply`
*   `search`
*   `sticker`
*   `member-info` / `role-info`
*   `emoji-list` / `emoji-upload` / `sticker-upload`
*   `role-add` / `role-remove`
*   `channel-info` / `channel-list`
*   `voice-status`
*   `event-list` / `event-create`
*   `timeout` / `kick` / `ban`

Notes:

*   `send` routes WhatsApp via the Gateway; other channels go direct.
*   `poll` uses the Gateway for WhatsApp and MS Teams; Discord polls go direct.
*   When a message tool call is bound to an active chat session, sends are constrained to that session’s target to avoid cross-context leaks.

### `cron`

Manage Gateway cron jobs and wakeups. Core actions:

*   `status`, `list`
*   `add`, `update`, `remove`, `run`, `runs`
*   `wake` (enqueue system event + optional immediate heartbeat)

Notes:

*   `add` expects a full cron job object (same schema as `cron.add` RPC).
*   `update` uses `{ jobId, patch }` (`id` accepted for compatibility).

### `gateway`

Restart or apply updates to the running Gateway process (in-place). Core actions:

*   `restart` (authorizes + sends `SIGUSR1` for in-process restart; `openclaw gateway` restart in-place)
*   `config.schema.lookup` (inspect one config path at a time without loading the full schema into prompt context)
*   `config.get`
*   `config.apply` (validate + write config + restart + wake)
*   `config.patch` (merge partial update + restart + wake)
*   `update.run` (run update + restart + wake)

Notes:

*   `config.schema.lookup` expects a targeted config path such as `gateway.auth` or `agents.list.*.heartbeat`.
*   Paths may include slash-delimited plugin ids when addressing `plugins.entries.<id>`, for example `plugins.entries.pack/one.config`.
*   Use `delayMs` (defaults to 2000) to avoid interrupting an in-flight reply.
*   `config.schema` remains available to internal Control UI flows and is not exposed through the agent `gateway` tool.
*   `restart` is enabled by default; set `commands.restart: false` to disable it.

### `sessions_list` / `sessions_history` / `sessions_send` / `sessions_spawn` / `session_status`

List sessions, inspect transcript history, or send to another session. Core parameters:

*   `sessions_list`: `kinds?`, `limit?`, `activeMinutes?`, `messageLimit?` (0 = none)
*   `sessions_history`: `sessionKey` (or `sessionId`), `limit?`, `includeTools?`
*   `sessions_send`: `sessionKey` (or `sessionId`), `message`, `timeoutSeconds?` (0 = fire-and-forget)
*   `sessions_spawn`: `task`, `label?`, `runtime?`, `agentId?`, `model?`, `thinking?`, `cwd?`, `runTimeoutSeconds?`, `thread?`, `mode?`, `cleanup?`, `sandbox?`, `streamTo?`, `attachments?`, `attachAs?`
*   `session_status`: `sessionKey?` (default current; accepts `sessionId`), `model?` (`default` clears override)

Notes:

*   `main` is the canonical direct-chat key; global/unknown are hidden.
*   `messageLimit > 0` fetches last N messages per session (tool messages filtered).
*   Session targeting is controlled by `tools.sessions.visibility` (default `tree`: current session + spawned subagent sessions). If you run a shared agent for multiple users, consider setting `tools.sessions.visibility: "self"` to prevent cross-session browsing.
*   `sessions_send` waits for final completion when `timeoutSeconds > 0`.
*   Delivery/announce happens after completion and is best-effort; `status: "ok"` confirms the agent run finished, not that the announce was delivered.
*   `sessions_spawn` supports `runtime: "subagent" | "acp"` (`subagent` default). For ACP runtime behavior, see [ACP Agents](https://docs.openclaw.ai/tools/acp-agents).
*   For ACP runtime, `streamTo: "parent"` routes initial-run progress summaries back to the requester session as system events instead of direct child delivery.
*   `sessions_spawn` starts a sub-agent run and posts an announce reply back to the requester chat.
    *   Supports one-shot mode (`mode: "run"`) and persistent thread-bound mode (`mode: "session"` with `thread: true`).
    *   If `thread: true` and `mode` is omitted, mode defaults to `session`.
    *   `mode: "session"` requires `thread: true`.
    *   If `runTimeoutSeconds` is omitted, OpenClaw uses `agents.defaults.subagents.runTimeoutSeconds` when set; otherwise timeout defaults to `0` (no timeout).
    *   Discord thread-bound flows depend on `session.threadBindings.*` and `channels.discord.threadBindings.*`.
    *   Reply format includes `Status`, `Result`, and compact stats.
    *   `Result` is the assistant completion text; if missing, the latest `toolResult` is used as fallback.
*   Manual completion-mode spawns send directly first, with queue fallback and retry on transient failures (`status: "ok"` means run finished, not that announce delivered).
*   `sessions_spawn` supports inline file attachments for subagent runtime only (ACP rejects them). Each attachment has `name`, `content`, and optional `encoding` (`utf8` or `base64`) and `mimeType`. Files are materialized into the child workspace at `.openclaw/attachments/<uuid>/` with a `.manifest.json` metadata file. The tool returns a receipt with `count`, `totalBytes`, per file `sha256`, and `relDir`. Attachment content is automatically redacted from transcript persistence.
    *   Configure limits via `tools.sessions_spawn.attachments` (`enabled`, `maxTotalBytes`, `maxFiles`, `maxFileBytes`, `retainOnSessionKeep`).
    *   `attachAs.mountPath` is a reserved hint for future mount implementations.
*   `sessions_spawn` is non-blocking and returns `status: "accepted"` immediately.
*   ACP `streamTo: "parent"` responses may include `streamLogPath` (session-scoped `*.acp-stream.jsonl`) for tailing progress history.
*   `sessions_send` runs a reply‑back ping‑pong (reply `REPLY_SKIP` to stop; max turns via `session.agentToAgent.maxPingPongTurns`, 0–5).
*   After the ping‑pong, the target agent runs an **announce step**; reply `ANNOUNCE_SKIP` to suppress the announcement.
*   Sandbox clamp: when the current session is sandboxed and `agents.defaults.sandbox.sessionToolsVisibility: "spawned"`, OpenClaw clamps `tools.sessions.visibility` to `tree`.

### `agents_list`

List agent ids that the current session may target with `sessions_spawn`. Notes:

*   Result is restricted to per-agent allowlists (`agents.list[].subagents.allowAgents`).
*   When `["*"]` is configured, the tool includes all configured agents and marks `allowAny: true`.

## Parameters (common)

Gateway-backed tools (`canvas`, `nodes`, `cron`):

*   `gatewayUrl` (default `ws://127.0.0.1:18789`)
*   `gatewayToken` (if auth enabled)
*   `timeoutMs`

Note: when `gatewayUrl` is set, include `gatewayToken` explicitly. Tools do not inherit config or environment credentials for overrides, and missing explicit credentials is an error. Browser tool:

*   `profile` (optional; defaults to `browser.defaultProfile`)
*   `target` (`sandbox` | `host` | `node`)
*   `node` (optional; pin a specific node id/name)
*   Troubleshooting guides:
    *   Linux startup/CDP issues: [Browser troubleshooting (Linux)](https://docs.openclaw.ai/tools/browser-linux-troubleshooting)
    *   WSL2 Gateway + Windows remote Chrome CDP: [WSL2 + Windows + remote Chrome CDP troubleshooting](https://docs.openclaw.ai/tools/browser-wsl2-windows-remote-cdp-troubleshooting)

## Recommended agent flows

Browser automation:

1.  `browser` → `status` / `start`
2.  `snapshot` (ai or aria)
3.  `act` (click/type/press)
4.  `screenshot` if you need visual confirmation

Canvas render:

1.  `canvas` → `present`
2.  `a2ui_push` (optional)
3.  `snapshot`

Node targeting:

1.  `nodes` → `status`
2.  `describe` on the chosen node
3.  `notify` / `run` / `camera_snap` / `screen_record`

## Safety

*   Avoid direct `system.run`; use `nodes` → `run` only with explicit user consent.
*   Respect user consent for camera/screen capture.
*   Use `status/describe` to ensure permissions before invoking media commands.

Tools are exposed in two parallel channels:

1.  **System prompt text**: a human-readable list + guidance.
2.  **Tool schema**: the structured function definitions sent to the model API.

That means the agent sees both “what tools exist” and “how to call them.” If a tool doesn’t appear in the system prompt or the schema, the model cannot call it.



---

<!-- SOURCE: https://docs.openclaw.ai/web -->

# Web - OpenClaw

## Web (Gateway)

The Gateway serves a small **browser Control UI** (Vite + Lit) from the same port as the Gateway WebSocket:

*   default: `http://<host>:18789/`
*   optional prefix: set `gateway.controlUi.basePath` (e.g. `/openclaw`)

Capabilities live in [Control UI](https://docs.openclaw.ai/web/control-ui). This page focuses on bind modes, security, and web-facing surfaces.

## Webhooks

When `hooks.enabled=true`, the Gateway also exposes a small webhook endpoint on the same HTTP server. See [Gateway configuration](https://docs.openclaw.ai/gateway/configuration) → `hooks` for auth + payloads.

## Config (default-on)

The Control UI is **enabled by default** when assets are present (`dist/control-ui`). You can control it via config:

```
{
  gateway: {
    controlUi: { enabled: true, basePath: "/openclaw" }, // basePath optional
  },
}
```

## Tailscale access

### Integrated Serve (recommended)

Keep the Gateway on loopback and let Tailscale Serve proxy it:

```
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "serve" },
  },
}
```

Then start the gateway:

Open:

*   `https://<magicdns>/` (or your configured `gateway.controlUi.basePath`)

### Tailnet bind + token

```
{
  gateway: {
    bind: "tailnet",
    controlUi: { enabled: true },
    auth: { mode: "token", token: "your-token" },
  },
}
```

Then start the gateway (token required for non-loopback binds):

Open:

*   `http://<tailscale-ip>:18789/` (or your configured `gateway.controlUi.basePath`)

### Public internet (Funnel)

```
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "funnel" },
    auth: { mode: "password" }, // or OPENCLAW_GATEWAY_PASSWORD
  },
}
```

## Security notes

*   Gateway auth is required by default (token/password or Tailscale identity headers).
*   Non-loopback binds still **require** a shared token/password (`gateway.auth` or env).
*   The wizard generates a gateway token by default (even on loopback).
*   The UI sends `connect.params.auth.token` or `connect.params.auth.password`.
*   For non-loopback Control UI deployments, set `gateway.controlUi.allowedOrigins` explicitly (full origins). Without it, gateway startup is refused by default.
*   `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback=true` enables Host-header origin fallback mode, but is a dangerous security downgrade.
*   With Serve, Tailscale identity headers can satisfy Control UI/WebSocket auth when `gateway.auth.allowTailscale` is `true` (no token/password required). HTTP API endpoints still require token/password. Set `gateway.auth.allowTailscale: false` to require explicit credentials. See [Tailscale](https://docs.openclaw.ai/gateway/tailscale) and [Security](https://docs.openclaw.ai/gateway/security). This tokenless flow assumes the gateway host is trusted.
*   `gateway.tailscale.mode: "funnel"` requires `gateway.auth.mode: "password"` (shared password).

## Building the UI

The Gateway serves static files from `dist/control-ui`. Build them with:

```
pnpm ui:build # auto-installs UI deps on first run
```

