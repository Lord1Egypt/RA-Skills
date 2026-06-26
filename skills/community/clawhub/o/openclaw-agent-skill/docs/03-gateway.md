# Gateway

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 31

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/security -->

# Network model - OpenClaw

Most operations flow through the Gateway (`openclaw gateway`), a single long-running process that owns channel connections and the WebSocket control plane.

## Core rules

*   One Gateway per host is recommended. It is the only process allowed to own the WhatsApp Web session. For rescue bots or strict isolation, run multiple gateways with isolated profiles and ports. See [Multiple gateways](https://docs.openclaw.ai/gateway/multiple-gateways).
*   Loopback first: the Gateway WS defaults to `ws://127.0.0.1:18789`. The wizard generates a gateway token by default, even for loopback. For tailnet access, run `openclaw gateway --bind tailnet --token ...` because tokens are required for non-loopback binds.
*   Nodes connect to the Gateway WS over LAN, tailnet, or SSH as needed. The legacy TCP bridge is deprecated.
*   Canvas host is served by the Gateway HTTP server on the **same port** as the Gateway (default `18789`):
    *   `/__openclaw__/canvas/`
    *   `/__openclaw__/a2ui/` When `gateway.auth` is configured and the Gateway binds beyond loopback, these routes are protected by Gateway auth. Node clients use node-scoped capability URLs tied to their active WS session. See [Gateway configuration](https://docs.openclaw.ai/gateway/configuration) (`canvasHost`, `gateway`).
*   Remote use is typically SSH tunnel or tailnet VPN. See [Remote access](https://docs.openclaw.ai/gateway/remote) and [Discovery](https://docs.openclaw.ai/gateway/discovery).

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/tailscale -->

# Tailscale - OpenClaw

## Tailscale (Gateway dashboard)

OpenClaw can auto-configure Tailscale **Serve** (tailnet) or **Funnel** (public) for the Gateway dashboard and WebSocket port. This keeps the Gateway bound to loopback while Tailscale provides HTTPS, routing, and (for Serve) identity headers.

## Modes

*   `serve`: Tailnet-only Serve via `tailscale serve`. The gateway stays on `127.0.0.1`.
*   `funnel`: Public HTTPS via `tailscale funnel`. OpenClaw requires a shared password.
*   `off`: Default (no Tailscale automation).

## Auth

Set `gateway.auth.mode` to control the handshake:

*   `token` (default when `OPENCLAW_GATEWAY_TOKEN` is set)
*   `password` (shared secret via `OPENCLAW_GATEWAY_PASSWORD` or config)

When `tailscale.mode = "serve"` and `gateway.auth.allowTailscale` is `true`, Control UI/WebSocket auth can use Tailscale identity headers (`tailscale-user-login`) without supplying a token/password. OpenClaw verifies the identity by resolving the `x-forwarded-for` address via the local Tailscale daemon (`tailscale whois`) and matching it to the header before accepting it. OpenClaw only treats a request as Serve when it arrives from loopback with Tailscale’s `x-forwarded-for`, `x-forwarded-proto`, and `x-forwarded-host` headers. HTTP API endpoints (for example `/v1/*`, `/tools/invoke`, and `/api/channels/*`) still require token/password auth. This tokenless flow assumes the gateway host is trusted. If untrusted local code may run on the same host, disable `gateway.auth.allowTailscale` and require token/password auth instead. To require explicit credentials, set `gateway.auth.allowTailscale: false` or force `gateway.auth.mode: "password"`.

## Config examples

### Tailnet-only (Serve)

```
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "serve" },
  },
}
```

Open: `https://<magicdns>/` (or your configured `gateway.controlUi.basePath`)

### Tailnet-only (bind to Tailnet IP)

Use this when you want the Gateway to listen directly on the Tailnet IP (no Serve/Funnel).

```
{
  gateway: {
    bind: "tailnet",
    auth: { mode: "token", token: "your-token" },
  },
}
```

Connect from another Tailnet device:

*   Control UI: `http://<tailscale-ip>:18789/`
*   WebSocket: `ws://<tailscale-ip>:18789`

Note: loopback (`http://127.0.0.1:18789`) will **not** work in this mode.

### Public internet (Funnel + shared password)

```
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "funnel" },
    auth: { mode: "password", password: "replace-me" },
  },
}
```

Prefer `OPENCLAW_GATEWAY_PASSWORD` over committing a password to disk.

## CLI examples

```
openclaw gateway --tailscale serve
openclaw gateway --tailscale funnel --auth password
```

## Notes

*   Tailscale Serve/Funnel requires the `tailscale` CLI to be installed and logged in.
*   `tailscale.mode: "funnel"` refuses to start unless auth mode is `password` to avoid public exposure.
*   Set `gateway.tailscale.resetOnExit` if you want OpenClaw to undo `tailscale serve` or `tailscale funnel` configuration on shutdown.
*   `gateway.bind: "tailnet"` is a direct Tailnet bind (no HTTPS, no Serve/Funnel).
*   `gateway.bind: "auto"` prefers loopback; use `tailnet` if you want Tailnet-only.
*   Serve/Funnel only expose the **Gateway control UI + WS**. Nodes connect over the same Gateway WS endpoint, so Serve can work for node access.

## Browser control (remote Gateway + local browser)

If you run the Gateway on one machine but want to drive a browser on another machine, run a **node host** on the browser machine and keep both on the same tailnet. The Gateway will proxy browser actions to the node; no separate control server or Serve URL needed. Avoid Funnel for browser control; treat node pairing like operator access.

## Tailscale prerequisites + limits

*   Serve requires HTTPS enabled for your tailnet; the CLI prompts if it is missing.
*   Serve injects Tailscale identity headers; Funnel does not.
*   Funnel requires Tailscale v1.38.3+, MagicDNS, HTTPS enabled, and a funnel node attribute.
*   Funnel only supports ports `443`, `8443`, and `10000` over TLS.
*   Funnel on macOS requires the open-source Tailscale app variant.

## Learn more

*   Tailscale Serve overview: [https://tailscale.com/kb/1312/serve](https://tailscale.com/kb/1312/serve)
*   `tailscale serve` command: [https://tailscale.com/kb/1242/tailscale-serve](https://tailscale.com/kb/1242/tailscale-serve)
*   Tailscale Funnel overview: [https://tailscale.com/kb/1223/tailscale-funnel](https://tailscale.com/kb/1223/tailscale-funnel)
*   `tailscale funnel` command: [https://tailscale.com/kb/1311/tailscale-funnel](https://tailscale.com/kb/1311/tailscale-funnel)

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/remote -->

# Remote Access - OpenClaw

## Remote access (SSH, tunnels, and tailnets)

This repo supports “remote over SSH” by keeping a single Gateway (the master) running on a dedicated host (desktop/server) and connecting clients to it.

*   For **operators (you / the macOS app)**: SSH tunneling is the universal fallback.
*   For **nodes (iOS/Android and future devices)**: connect to the Gateway **WebSocket** (LAN/tailnet or SSH tunnel as needed).

## The core idea

*   The Gateway WebSocket binds to **loopback** on your configured port (defaults to 18789).
*   For remote use, you forward that loopback port over SSH (or use a tailnet/VPN and tunnel less).

## Common VPN/tailnet setups (where the agent lives)

Think of the **Gateway host** as “where the agent lives.” It owns sessions, auth profiles, channels, and state. Your laptop/desktop (and nodes) connect to that host.

### 1) Always-on Gateway in your tailnet (VPS or home server)

Run the Gateway on a persistent host and reach it via **Tailscale** or SSH.

*   **Best UX:** keep `gateway.bind: "loopback"` and use **Tailscale Serve** for the Control UI.
*   **Fallback:** keep loopback + SSH tunnel from any machine that needs access.
*   **Examples:** [exe.dev](https://docs.openclaw.ai/install/exe-dev) (easy VM) or [Hetzner](https://docs.openclaw.ai/install/hetzner) (production VPS).

This is ideal when your laptop sleeps often but you want the agent always-on.

### 2) Home desktop runs the Gateway, laptop is remote control

The laptop does **not** run the agent. It connects remotely:

*   Use the macOS app’s **Remote over SSH** mode (Settings → General → “OpenClaw runs”).
*   The app opens and manages the tunnel, so WebChat + health checks “just work.”

Runbook: [macOS remote access](https://docs.openclaw.ai/platforms/mac/remote).

### 3) Laptop runs the Gateway, remote access from other machines

Keep the Gateway local but expose it safely:

*   SSH tunnel to the laptop from other machines, or
*   Tailscale Serve the Control UI and keep the Gateway loopback-only.

Guide: [Tailscale](https://docs.openclaw.ai/gateway/tailscale) and [Web overview](https://docs.openclaw.ai/web).

## Command flow (what runs where)

One gateway service owns state + channels. Nodes are peripherals. Flow example (Telegram → node):

*   Telegram message arrives at the **Gateway**.
*   Gateway runs the **agent** and decides whether to call a node tool.
*   Gateway calls the **node** over the Gateway WebSocket (`node.*` RPC).
*   Node returns the result; Gateway replies back out to Telegram.

Notes:

*   **Nodes do not run the gateway service.** Only one gateway should run per host unless you intentionally run isolated profiles (see [Multiple gateways](https://docs.openclaw.ai/gateway/multiple-gateways)).
*   macOS app “node mode” is just a node client over the Gateway WebSocket.

Create a local tunnel to the remote Gateway WS:

```
ssh -N -L 18789:127.0.0.1:18789 user@host
```

With the tunnel up:

*   `openclaw health` and `openclaw status --deep` now reach the remote gateway via `ws://127.0.0.1:18789`.
*   `openclaw gateway {status,health,send,agent,call}` can also target the forwarded URL via `--url` when needed.

Note: replace `18789` with your configured `gateway.port` (or `--port`/`OPENCLAW_GATEWAY_PORT`). Note: when you pass `--url`, the CLI does not fall back to config or environment credentials. Include `--token` or `--password` explicitly. Missing explicit credentials is an error.

## CLI remote defaults

You can persist a remote target so CLI commands use it by default:

```
{
  gateway: {
    mode: "remote",
    remote: {
      url: "ws://127.0.0.1:18789",
      token: "your-token",
    },
  },
}
```

When the gateway is loopback-only, keep the URL at `ws://127.0.0.1:18789` and open the SSH tunnel first.

## Credential precedence

Gateway credential resolution follows one shared contract across call/probe/status paths, Discord exec-approval monitoring, and node-host connections:

*   Explicit credentials (`--token`, `--password`, or tool `gatewayToken`) always win on call paths that accept explicit auth.
*   URL override safety:
    *   CLI URL overrides (`--url`) never reuse implicit config/env credentials.
    *   Env URL overrides (`OPENCLAW_GATEWAY_URL`) may use env credentials only (`OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD`).
*   Local mode defaults:
    *   token: `OPENCLAW_GATEWAY_TOKEN` -> `gateway.auth.token` -> `gateway.remote.token`
    *   password: `OPENCLAW_GATEWAY_PASSWORD` -> `gateway.auth.password` -> `gateway.remote.password`
*   Remote mode defaults:
    *   token: `gateway.remote.token` -> `OPENCLAW_GATEWAY_TOKEN` -> `gateway.auth.token`
    *   password: `OPENCLAW_GATEWAY_PASSWORD` -> `gateway.remote.password` -> `gateway.auth.password`
*   Remote probe/status token checks are strict by default: they use `gateway.remote.token` only (no local token fallback) when targeting remote mode.
*   Legacy `CLAWDBOT_GATEWAY_*` env vars are only used by compatibility call paths; probe/status/auth resolution uses `OPENCLAW_GATEWAY_*` only.

## Chat UI over SSH

WebChat no longer uses a separate HTTP port. The SwiftUI chat UI connects directly to the Gateway WebSocket.

*   Forward `18789` over SSH (see above), then connect clients to `ws://127.0.0.1:18789`.
*   On macOS, prefer the app’s “Remote over SSH” mode, which manages the tunnel automatically.

## macOS app “Remote over SSH”

The macOS menu bar app can drive the same setup end-to-end (remote status checks, WebChat, and Voice Wake forwarding). Runbook: [macOS remote access](https://docs.openclaw.ai/platforms/mac/remote).

## Security rules (remote/VPN)

Short version: **keep the Gateway loopback-only** unless you’re sure you need a bind.

*   **Loopback + SSH/Tailscale Serve** is the safest default (no public exposure).
*   Plaintext `ws://` is loopback-only by default. For trusted private networks, set `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` on the client process as break-glass.
*   **Non-loopback binds** (`lan`/`tailnet`/`custom`, or `auto` when loopback is unavailable) must use auth tokens/passwords.
*   `gateway.remote.token` / `.password` are client credential sources. They do **not** configure server auth by themselves.
*   Local call paths can use `gateway.remote.*` as fallback when `gateway.auth.*` is unset.
*   `gateway.remote.tlsFingerprint` pins the remote TLS cert when using `wss://`.
*   **Tailscale Serve** can authenticate Control UI/WebSocket traffic via identity headers when `gateway.auth.allowTailscale: true`; HTTP API endpoints still require token/password auth. This tokenless flow assumes the gateway host is trusted. Set it to `false` if you want tokens/passwords everywhere.
*   Treat browser control like operator access: tailnet-only + deliberate node pairing.

Deep dive: [Security](https://docs.openclaw.ai/gateway/security).

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/configuration -->

# Configuration - OpenClaw

OpenClaw reads an optional config from `~/.openclaw/openclaw.json`. If the file is missing, OpenClaw uses safe defaults. Common reasons to add a config:

*   Connect channels and control who can message the bot
*   Set models, tools, sandboxing, or automation (cron, hooks)
*   Tune sessions, media, networking, or UI

See the [full reference](https://docs.openclaw.ai/gateway/configuration-reference) for every available field.

## Minimal config

```
// ~/.openclaw/openclaw.json
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

## Editing config

*   Interactive wizard
    
*   CLI (one-liners)
    
*   Control UI
    
*   Direct edit
    

```
openclaw onboard       # full setup wizard
openclaw configure     # config wizard
```

```
openclaw config get agents.defaults.workspace
openclaw config set agents.defaults.heartbeat.every "2h"
openclaw config unset tools.web.search.apiKey
```

Open [http://127.0.0.1:18789](http://127.0.0.1:18789/) and use the **Config** tab. The Control UI renders a form from the config schema, with a **Raw JSON** editor as an escape hatch.

Edit `~/.openclaw/openclaw.json` directly. The Gateway watches the file and applies changes automatically (see [hot reload](https://docs.openclaw.ai/gateway/configuration#config-hot-reload)).

## Strict validation

When validation fails:

*   The Gateway does not boot
*   Only diagnostic commands work (`openclaw doctor`, `openclaw logs`, `openclaw health`, `openclaw status`)
*   Run `openclaw doctor` to see exact issues
*   Run `openclaw doctor --fix` (or `--yes`) to apply repairs

## Common tasks

## Config hot reload

The Gateway watches `~/.openclaw/openclaw.json` and applies changes automatically — no manual restart needed for most settings.

### Reload modes

| Mode | Behavior |
| --- | --- |
| **`hybrid`** (default) | Hot-applies safe changes instantly. Automatically restarts for critical ones. |
| **`hot`** | Hot-applies safe changes only. Logs a warning when a restart is needed — you handle it. |
| **`restart`** | Restarts the Gateway on any config change, safe or not. |
| **`off`** | Disables file watching. Changes take effect on the next manual restart. |

```
{
  gateway: {
    reload: { mode: "hybrid", debounceMs: 300 },
  },
}
```

### What hot-applies vs what needs a restart

Most fields hot-apply without downtime. In `hybrid` mode, restart-required changes are handled automatically.

| Category | Fields | Restart needed? |
| --- | --- | --- |
| Channels | `channels.*`, `web` (WhatsApp) — all built-in and extension channels | No  |
| Agent & models | `agent`, `agents`, `models`, `routing` | No  |
| Automation | `hooks`, `cron`, `agent.heartbeat` | No  |
| Sessions & messages | `session`, `messages` | No  |
| Tools & media | `tools`, `browser`, `skills`, `audio`, `talk` | No  |
| UI & misc | `ui`, `logging`, `identity`, `bindings` | No  |
| Gateway server | `gateway.*` (port, bind, auth, tailscale, TLS, HTTP) | **Yes** |
| Infrastructure | `discovery`, `canvasHost`, `plugins` | **Yes** |

## Config RPC (programmatic updates)

## Environment variables

OpenClaw reads env vars from the parent process plus:

*   `.env` from the current working directory (if present)
*   `~/.openclaw/.env` (global fallback)

Neither file overrides existing env vars. You can also set inline env vars in config:

```
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: { GROQ_API_KEY: "gsk-..." },
  },
}
```

Shell env import (optional)

If enabled and expected keys aren’t set, OpenClaw runs your login shell and imports only the missing keys:

```
{
  env: {
    shellEnv: { enabled: true, timeoutMs: 15000 },
  },
}
```

Env var equivalent: `OPENCLAW_LOAD_SHELL_ENV=1`

Env var substitution in config values

Reference env vars in any config string value with `${VAR_NAME}`:

```
{
  gateway: { auth: { token: "${OPENCLAW_GATEWAY_TOKEN}" } },
  models: { providers: { custom: { apiKey: "${CUSTOM_API_KEY}" } } },
}
```

Rules:

*   Only uppercase names matched: `[A-Z_][A-Z0-9_]*`
*   Missing/empty vars throw an error at load time
*   Escape with `$${VAR}` for literal output
*   Works inside `$include` files
*   Inline substitution: `"${BASE}/v1"` → `"https://api.example.com/v1"`

Secret refs (env, file, exec)

For fields that support SecretRef objects, you can use:

```
{
  models: {
    providers: {
      openai: { apiKey: { source: "env", provider: "default", id: "OPENAI_API_KEY" } },
    },
  },
  skills: {
    entries: {
      "nano-banana-pro": {
        apiKey: {
          source: "file",
          provider: "filemain",
          id: "/skills/entries/nano-banana-pro/apiKey",
        },
      },
    },
  },
  channels: {
    googlechat: {
      serviceAccountRef: {
        source: "exec",
        provider: "vault",
        id: "channels/googlechat/serviceAccount",
      },
    },
  },
}
```

SecretRef details (including `secrets.providers` for `env`/`file`/`exec`) are in [Secrets Management](https://docs.openclaw.ai/gateway/secrets). Supported credential paths are listed in [SecretRef Credential Surface](https://docs.openclaw.ai/reference/secretref-credential-surface).

See [Environment](https://docs.openclaw.ai/help/environment) for full precedence and sources.

## Full reference

For the complete field-by-field reference, see **[Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)**.

* * *

_Related: [Configuration Examples](https://docs.openclaw.ai/gateway/configuration-examples) · [Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference) · [Doctor](https://docs.openclaw.ai/gateway/doctor)_

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/configuration-reference -->

# Configuration Reference - OpenClaw

Every field available in `~/.openclaw/openclaw.json`. For a task-oriented overview, see [Configuration](https://docs.openclaw.ai/gateway/configuration). Config format is **JSON5** (comments + trailing commas allowed). All fields are optional — OpenClaw uses safe defaults when omitted.

* * *

## Channels

Each channel starts automatically when its config section exists (unless `enabled: false`).

### DM and group access

All channels support DM policies and group policies:

DM policy

Behavior

`pairing` (default)

Unknown senders get a one-time pairing code; owner must approve

`allowlist`

Only senders in `allowFrom` (or paired allow store)

`open`

Allow all inbound DMs (requires `allowFrom: ["*"]`)

`disabled`

Ignore all inbound DMs

Group policy

Behavior

`allowlist` (default)

Only groups matching the configured allowlist

`open`

Bypass group allowlists (mention-gating still applies)

`disabled`

Block all group/room messages

### Channel model overrides

Use `channels.modelByChannel` to pin specific channel IDs to a model. Values accept `provider/model` or configured model aliases. The channel mapping applies when a session does not already have a model override (for example, set via `/model`).

```
{
  channels: {
    modelByChannel: {
      discord: {
        "123456789012345678": "anthropic/claude-opus-4-6",
      },
      slack: {
        C1234567890: "openai/gpt-4.1",
      },
      telegram: {
        "-1001234567890": "openai/gpt-4.1-mini",
        "-1001234567890:topic:99": "anthropic/claude-sonnet-4-6",
      },
    },
  },
}
```

### Channel defaults and heartbeat

Use `channels.defaults` for shared group-policy and heartbeat behavior across providers:

```
{
  channels: {
    defaults: {
      groupPolicy: "allowlist", // open | allowlist | disabled
      heartbeat: {
        showOk: false,
        showAlerts: true,
        useIndicator: true,
      },
    },
  },
}
```

*   `channels.defaults.groupPolicy`: fallback group policy when a provider-level `groupPolicy` is unset.
*   `channels.defaults.heartbeat.showOk`: include healthy channel statuses in heartbeat output.
*   `channels.defaults.heartbeat.showAlerts`: include degraded/error statuses in heartbeat output.
*   `channels.defaults.heartbeat.useIndicator`: render compact indicator-style heartbeat output.

### WhatsApp

WhatsApp runs through the gateway’s web channel (Baileys Web). It starts automatically when a linked session exists.

```
{
  channels: {
    whatsapp: {
      dmPolicy: "pairing", // pairing | allowlist | open | disabled
      allowFrom: ["+15555550123", "+447700900123"],
      textChunkLimit: 4000,
      chunkMode: "length", // length | newline
      mediaMaxMb: 50,
      sendReadReceipts: true, // blue ticks (false in self-chat mode)
      groups: {
        "*": { requireMention: true },
      },
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
  },
  web: {
    enabled: true,
    heartbeatSeconds: 60,
    reconnect: {
      initialMs: 2000,
      maxMs: 120000,
      factor: 1.4,
      jitter: 0.2,
      maxAttempts: 0,
    },
  },
}
```

Multi-account WhatsApp

```
{
  channels: {
    whatsapp: {
      accounts: {
        default: {},
        personal: {},
        biz: {
          // authDir: "~/.openclaw/credentials/whatsapp/biz",
        },
      },
    },
  },
}
```

*   Outbound commands default to account `default` if present; otherwise the first configured account id (sorted).
*   Optional `channels.whatsapp.defaultAccount` overrides that fallback default account selection when it matches a configured account id.
*   Legacy single-account Baileys auth dir is migrated by `openclaw doctor` into `whatsapp/default`.
*   Per-account overrides: `channels.whatsapp.accounts.<id>.sendReadReceipts`, `channels.whatsapp.accounts.<id>.dmPolicy`, `channels.whatsapp.accounts.<id>.allowFrom`.

### Telegram

```
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "your-bot-token",
      dmPolicy: "pairing",
      allowFrom: ["tg:123456789"],
      groups: {
        "*": { requireMention: true },
        "-1001234567890": {
          allowFrom: ["@admin"],
          systemPrompt: "Keep answers brief.",
          topics: {
            "99": {
              requireMention: false,
              skills: ["search"],
              systemPrompt: "Stay on topic.",
            },
          },
        },
      },
      customCommands: [
        { command: "backup", description: "Git backup" },
        { command: "generate", description: "Create an image" },
      ],
      historyLimit: 50,
      replyToMode: "first", // off | first | all
      linkPreview: true,
      streaming: "partial", // off | partial | block | progress (default: off)
      actions: { reactions: true, sendMessage: true },
      reactionNotifications: "own", // off | own | all
      mediaMaxMb: 100,
      retry: {
        attempts: 3,
        minDelayMs: 400,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
      network: {
        autoSelectFamily: true,
        dnsResultOrder: "ipv4first",
      },
      proxy: "socks5://localhost:9050",
      webhookUrl: "https://example.com/telegram-webhook",
      webhookSecret: "secret",
      webhookPath: "/telegram-webhook",
    },
  },
}
```

*   Bot token: `channels.telegram.botToken` or `channels.telegram.tokenFile`, with `TELEGRAM_BOT_TOKEN` as fallback for the default account.
*   Optional `channels.telegram.defaultAccount` overrides default account selection when it matches a configured account id.
*   In multi-account setups (2+ account ids), set an explicit default (`channels.telegram.defaultAccount` or `channels.telegram.accounts.default`) to avoid fallback routing; `openclaw doctor` warns when this is missing or invalid.
*   `configWrites: false` blocks Telegram-initiated config writes (supergroup ID migrations, `/config set|unset`).
*   Top-level `bindings[]` entries with `type: "acp"` configure persistent ACP bindings for forum topics (use canonical `chatId:topic:topicId` in `match.peer.id`). Field semantics are shared in [ACP Agents](https://docs.openclaw.ai/tools/acp-agents#channel-specific-settings).
*   Telegram stream previews use `sendMessage` + `editMessageText` (works in direct and group chats).
*   Retry policy: see [Retry policy](https://docs.openclaw.ai/concepts/retry).

### Discord

```
{
  channels: {
    discord: {
      enabled: true,
      token: "your-bot-token",
      mediaMaxMb: 8,
      allowBots: false,
      actions: {
        reactions: true,
        stickers: true,
        polls: true,
        permissions: true,
        messages: true,
        threads: true,
        pins: true,
        search: true,
        memberInfo: true,
        roleInfo: true,
        roles: false,
        channelInfo: true,
        voiceStatus: true,
        events: true,
        moderation: false,
      },
      replyToMode: "off", // off | first | all
      dmPolicy: "pairing",
      allowFrom: ["1234567890", "123456789012345678"],
      dm: { enabled: true, groupEnabled: false, groupChannels: ["openclaw-dm"] },
      guilds: {
        "123456789012345678": {
          slug: "friends-of-openclaw",
          requireMention: false,
          ignoreOtherMentions: true,
          reactionNotifications: "own",
          users: ["987654321098765432"],
          channels: {
            general: { allow: true },
            help: {
              allow: true,
              requireMention: true,
              users: ["987654321098765432"],
              skills: ["docs"],
              systemPrompt: "Short answers only.",
            },
          },
        },
      },
      historyLimit: 20,
      textChunkLimit: 2000,
      chunkMode: "length", // length | newline
      streaming: "off", // off | partial | block | progress (progress maps to partial on Discord)
      maxLinesPerMessage: 17,
      ui: {
        components: {
          accentColor: "#5865F2",
        },
      },
      threadBindings: {
        enabled: true,
        idleHours: 24,
        maxAgeHours: 0,
        spawnSubagentSessions: false, // opt-in for sessions_spawn({ thread: true })
      },
      voice: {
        enabled: true,
        autoJoin: [
          {
            guildId: "123456789012345678",
            channelId: "234567890123456789",
          },
        ],
        daveEncryption: true,
        decryptionFailureTolerance: 24,
        tts: {
          provider: "openai",
          openai: { voice: "alloy" },
        },
      },
      retry: {
        attempts: 3,
        minDelayMs: 500,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
  },
}
```

*   Token: `channels.discord.token`, with `DISCORD_BOT_TOKEN` as fallback for the default account.
*   Optional `channels.discord.defaultAccount` overrides default account selection when it matches a configured account id.
*   Use `user:<id>` (DM) or `channel:<id>` (guild channel) for delivery targets; bare numeric IDs are rejected.
*   Guild slugs are lowercase with spaces replaced by `-`; channel keys use the slugged name (no `#`). Prefer guild IDs.
*   Bot-authored messages are ignored by default. `allowBots: true` enables them; use `allowBots: "mentions"` to only accept bot messages that mention the bot (own messages still filtered).
*   `channels.discord.guilds.<id>.ignoreOtherMentions` (and channel overrides) drops messages that mention another user or role but not the bot (excluding @everyone/@here).
*   `maxLinesPerMessage` (default 17) splits tall messages even when under 2000 chars.
*   `channels.discord.threadBindings` controls Discord thread-bound routing:
    *   `enabled`: Discord override for thread-bound session features (`/focus`, `/unfocus`, `/agents`, `/session idle`, `/session max-age`, and bound delivery/routing)
    *   `idleHours`: Discord override for inactivity auto-unfocus in hours (`0` disables)
    *   `maxAgeHours`: Discord override for hard max age in hours (`0` disables)
    *   `spawnSubagentSessions`: opt-in switch for `sessions_spawn({ thread: true })` auto thread creation/binding
*   Top-level `bindings[]` entries with `type: "acp"` configure persistent ACP bindings for channels and threads (use channel/thread id in `match.peer.id`). Field semantics are shared in [ACP Agents](https://docs.openclaw.ai/tools/acp-agents#channel-specific-settings).
*   `channels.discord.ui.components.accentColor` sets the accent color for Discord components v2 containers.
*   `channels.discord.voice` enables Discord voice channel conversations and optional auto-join + TTS overrides.
*   `channels.discord.voice.daveEncryption` and `channels.discord.voice.decryptionFailureTolerance` pass through to `@discordjs/voice` DAVE options (`true` and `24` by default).
*   OpenClaw additionally attempts voice receive recovery by leaving/rejoining a voice session after repeated decrypt failures.
*   `channels.discord.streaming` is the canonical stream mode key. Legacy `streamMode` and boolean `streaming` values are auto-migrated.
*   `channels.discord.autoPresence` maps runtime availability to bot presence (healthy => online, degraded => idle, exhausted => dnd) and allows optional status text overrides.
*   `channels.discord.dangerouslyAllowNameMatching` re-enables mutable name/tag matching (break-glass compatibility mode).

**Reaction notification modes:** `off` (none), `own` (bot’s messages, default), `all` (all messages), `allowlist` (from `guilds.<id>.users` on all messages).

### Google Chat

```
{
  channels: {
    googlechat: {
      enabled: true,
      serviceAccountFile: "/path/to/service-account.json",
      audienceType: "app-url", // app-url | project-number
      audience: "https://gateway.example.com/googlechat",
      webhookPath: "/googlechat",
      botUser: "users/1234567890",
      dm: {
        enabled: true,
        policy: "pairing",
        allowFrom: ["users/1234567890"],
      },
      groupPolicy: "allowlist",
      groups: {
        "spaces/AAAA": { allow: true, requireMention: true },
      },
      actions: { reactions: true },
      typingIndicator: "message",
      mediaMaxMb: 20,
    },
  },
}
```

*   Service account JSON: inline (`serviceAccount`) or file-based (`serviceAccountFile`).
*   Service account SecretRef is also supported (`serviceAccountRef`).
*   Env fallbacks: `GOOGLE_CHAT_SERVICE_ACCOUNT` or `GOOGLE_CHAT_SERVICE_ACCOUNT_FILE`.
*   Use `spaces/<spaceId>` or `users/<userId>` for delivery targets.
*   `channels.googlechat.dangerouslyAllowNameMatching` re-enables mutable email principal matching (break-glass compatibility mode).

### Slack

```
{
  channels: {
    slack: {
      enabled: true,
      botToken: "xoxb-...",
      appToken: "xapp-...",
      dmPolicy: "pairing",
      allowFrom: ["U123", "U456", "*"],
      dm: { enabled: true, groupEnabled: false, groupChannels: ["G123"] },
      channels: {
        C123: { allow: true, requireMention: true, allowBots: false },
        "#general": {
          allow: true,
          requireMention: true,
          allowBots: false,
          users: ["U123"],
          skills: ["docs"],
          systemPrompt: "Short answers only.",
        },
      },
      historyLimit: 50,
      allowBots: false,
      reactionNotifications: "own",
      reactionAllowlist: ["U123"],
      replyToMode: "off", // off | first | all
      thread: {
        historyScope: "thread", // thread | channel
        inheritParent: false,
      },
      actions: {
        reactions: true,
        messages: true,
        pins: true,
        memberInfo: true,
        emojiList: true,
      },
      slashCommand: {
        enabled: true,
        name: "openclaw",
        sessionPrefix: "slack:slash",
        ephemeral: true,
      },
      typingReaction: "hourglass_flowing_sand",
      textChunkLimit: 4000,
      chunkMode: "length",
      streaming: "partial", // off | partial | block | progress (preview mode)
      nativeStreaming: true, // use Slack native streaming API when streaming=partial
      mediaMaxMb: 20,
    },
  },
}
```

*   **Socket mode** requires both `botToken` and `appToken` (`SLACK_BOT_TOKEN` + `SLACK_APP_TOKEN` for default account env fallback).
*   **HTTP mode** requires `botToken` plus `signingSecret` (at root or per-account).
*   `configWrites: false` blocks Slack-initiated config writes.
*   Optional `channels.slack.defaultAccount` overrides default account selection when it matches a configured account id.
*   `channels.slack.streaming` is the canonical stream mode key. Legacy `streamMode` and boolean `streaming` values are auto-migrated.
*   Use `user:<id>` (DM) or `channel:<id>` for delivery targets.

**Reaction notification modes:** `off`, `own` (default), `all`, `allowlist` (from `reactionAllowlist`). **Thread session isolation:** `thread.historyScope` is per-thread (default) or shared across channel. `thread.inheritParent` copies parent channel transcript to new threads.

*   `typingReaction` adds a temporary reaction to the inbound Slack message while a reply is running, then removes it on completion. Use a Slack emoji shortcode such as `"hourglass_flowing_sand"`.

Action group

Default

Notes

reactions

enabled

React + list reactions

messages

enabled

Read/send/edit/delete

pins

enabled

Pin/unpin/list

memberInfo

enabled

Member info

emojiList

enabled

Custom emoji list

### Mattermost

Mattermost ships as a plugin: `openclaw plugins install @openclaw/mattermost`.

```
{
  channels: {
    mattermost: {
      enabled: true,
      botToken: "mm-token",
      baseUrl: "https://chat.example.com",
      dmPolicy: "pairing",
      chatmode: "oncall", // oncall | onmessage | onchar
      oncharPrefixes: [">", "!"],
      commands: {
        native: true, // opt-in
        nativeSkills: true,
        callbackPath: "/api/channels/mattermost/command",
        // Optional explicit URL for reverse-proxy/public deployments
        callbackUrl: "https://gateway.example.com/api/channels/mattermost/command",
      },
      textChunkLimit: 4000,
      chunkMode: "length",
    },
  },
}
```

Chat modes: `oncall` (respond on @-mention, default), `onmessage` (every message), `onchar` (messages starting with trigger prefix). When Mattermost native commands are enabled:

*   `commands.callbackPath` must be a path (for example `/api/channels/mattermost/command`), not a full URL.
*   `commands.callbackUrl` must resolve to the OpenClaw gateway endpoint and be reachable from the Mattermost server.
*   For private/tailnet/internal callback hosts, Mattermost may require `ServiceSettings.AllowedUntrustedInternalConnections` to include the callback host/domain. Use host/domain values, not full URLs.
*   `channels.mattermost.configWrites`: allow or deny Mattermost-initiated config writes.
*   `channels.mattermost.requireMention`: require `@mention` before replying in channels.
*   Optional `channels.mattermost.defaultAccount` overrides default account selection when it matches a configured account id.

### Signal

```
{
  channels: {
    signal: {
      enabled: true,
      account: "+15555550123", // optional account binding
      dmPolicy: "pairing",
      allowFrom: ["+15551234567", "uuid:123e4567-e89b-12d3-a456-426614174000"],
      configWrites: true,
      reactionNotifications: "own", // off | own | all | allowlist
      reactionAllowlist: ["+15551234567", "uuid:123e4567-e89b-12d3-a456-426614174000"],
      historyLimit: 50,
    },
  },
}
```

**Reaction notification modes:** `off`, `own` (default), `all`, `allowlist` (from `reactionAllowlist`).

*   `channels.signal.account`: pin channel startup to a specific Signal account identity.
*   `channels.signal.configWrites`: allow or deny Signal-initiated config writes.
*   Optional `channels.signal.defaultAccount` overrides default account selection when it matches a configured account id.

### BlueBubbles

BlueBubbles is the recommended iMessage path (plugin-backed, configured under `channels.bluebubbles`).

```
{
  channels: {
    bluebubbles: {
      enabled: true,
      dmPolicy: "pairing",
      // serverUrl, password, webhookPath, group controls, and advanced actions:
      // see /channels/bluebubbles
    },
  },
}
```

*   Core key paths covered here: `channels.bluebubbles`, `channels.bluebubbles.dmPolicy`.
*   Optional `channels.bluebubbles.defaultAccount` overrides default account selection when it matches a configured account id.
*   Full BlueBubbles channel configuration is documented in [BlueBubbles](https://docs.openclaw.ai/channels/bluebubbles).

### iMessage

OpenClaw spawns `imsg rpc` (JSON-RPC over stdio). No daemon or port required.

```
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "imsg",
      dbPath: "~/Library/Messages/chat.db",
      remoteHost: "user@gateway-host",
      dmPolicy: "pairing",
      allowFrom: ["+15555550123", "user@example.com", "chat_id:123"],
      historyLimit: 50,
      includeAttachments: false,
      attachmentRoots: ["/Users/*/Library/Messages/Attachments"],
      remoteAttachmentRoots: ["/Users/*/Library/Messages/Attachments"],
      mediaMaxMb: 16,
      service: "auto",
      region: "US",
    },
  },
}
```

*   Optional `channels.imessage.defaultAccount` overrides default account selection when it matches a configured account id.
*   Requires Full Disk Access to the Messages DB.
*   Prefer `chat_id:<id>` targets. Use `imsg chats --limit 20` to list chats.
*   `cliPath` can point to an SSH wrapper; set `remoteHost` (`host` or `user@host`) for SCP attachment fetching.
*   `attachmentRoots` and `remoteAttachmentRoots` restrict inbound attachment paths (default: `/Users/*/Library/Messages/Attachments`).
*   SCP uses strict host-key checking, so ensure the relay host key already exists in `~/.ssh/known_hosts`.
*   `channels.imessage.configWrites`: allow or deny iMessage-initiated config writes.

iMessage SSH wrapper example

```
#!/usr/bin/env bash
exec ssh -T gateway-host imsg "$@"
```

### Microsoft Teams

Microsoft Teams is extension-backed and configured under `channels.msteams`.

```
{
  channels: {
    msteams: {
      enabled: true,
      configWrites: true,
      // appId, appPassword, tenantId, webhook, team/channel policies:
      // see /channels/msteams
    },
  },
}
```

*   Core key paths covered here: `channels.msteams`, `channels.msteams.configWrites`.
*   Full Teams config (credentials, webhook, DM/group policy, per-team/per-channel overrides) is documented in [Microsoft Teams](https://docs.openclaw.ai/channels/msteams).

### IRC

IRC is extension-backed and configured under `channels.irc`.

```
{
  channels: {
    irc: {
      enabled: true,
      dmPolicy: "pairing",
      configWrites: true,
      nickserv: {
        enabled: true,
        service: "NickServ",
        password: "${IRC_NICKSERV_PASSWORD}",
        register: false,
        registerEmail: "bot@example.com",
      },
    },
  },
}
```

*   Core key paths covered here: `channels.irc`, `channels.irc.dmPolicy`, `channels.irc.configWrites`, `channels.irc.nickserv.*`.
*   Optional `channels.irc.defaultAccount` overrides default account selection when it matches a configured account id.
*   Full IRC channel configuration (host/port/TLS/channels/allowlists/mention gating) is documented in [IRC](https://docs.openclaw.ai/channels/irc).

### Multi-account (all channels)

Run multiple accounts per channel (each with its own `accountId`):

```
{
  channels: {
    telegram: {
      accounts: {
        default: {
          name: "Primary bot",
          botToken: "123456:ABC...",
        },
        alerts: {
          name: "Alerts bot",
          botToken: "987654:XYZ...",
        },
      },
    },
  },
}
```

*   `default` is used when `accountId` is omitted (CLI + routing).
*   Env tokens only apply to the **default** account.
*   Base channel settings apply to all accounts unless overridden per account.
*   Use `bindings[].match.accountId` to route each account to a different agent.
*   If you add a non-default account via `openclaw channels add` (or channel onboarding) while still on a single-account top-level channel config, OpenClaw moves account-scoped top-level single-account values into `channels.<channel>.accounts.default` first so the original account keeps working.
*   Existing channel-only bindings (no `accountId`) keep matching the default account; account-scoped bindings remain optional.
*   `openclaw doctor --fix` also repairs mixed shapes by moving account-scoped top-level single-account values into `accounts.default` when named accounts exist but `default` is missing.

### Other extension channels

Many extension channels are configured as `channels.<id>` and documented in their dedicated channel pages (for example Feishu, Matrix, LINE, Nostr, Zalo, Nextcloud Talk, Synology Chat, and Twitch). See the full channel index: [Channels](https://docs.openclaw.ai/channels).

### Group chat mention gating

Group messages default to **require mention** (metadata mention or regex patterns). Applies to WhatsApp, Telegram, Discord, Google Chat, and iMessage group chats. **Mention types:**

*   **Metadata mentions**: Native platform @-mentions. Ignored in WhatsApp self-chat mode.
*   **Text patterns**: Regex patterns in `agents.list[].groupChat.mentionPatterns`. Always checked.
*   Mention gating is enforced only when detection is possible (native mentions or at least one pattern).

```
{
  messages: {
    groupChat: { historyLimit: 50 },
  },
  agents: {
    list: [{ id: "main", groupChat: { mentionPatterns: ["@openclaw", "openclaw"] } }],
  },
}
```

`messages.groupChat.historyLimit` sets the global default. Channels can override with `channels.<channel>.historyLimit` (or per-account). Set `0` to disable.

#### DM history limits

```
{
  channels: {
    telegram: {
      dmHistoryLimit: 30,
      dms: {
        "123456789": { historyLimit: 50 },
      },
    },
  },
}
```

Resolution: per-DM override → provider default → no limit (all retained). Supported: `telegram`, `whatsapp`, `discord`, `slack`, `signal`, `imessage`, `msteams`.

#### Self-chat mode

Include your own number in `allowFrom` to enable self-chat mode (ignores native @-mentions, only responds to text patterns):

```
{
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: { mentionPatterns: ["reisponde", "@openclaw"] },
      },
    ],
  },
}
```

### Commands (chat command handling)

```
{
  commands: {
    native: "auto", // register native commands when supported
    text: true, // parse /commands in chat messages
    bash: false, // allow ! (alias: /bash)
    bashForegroundMs: 2000,
    config: false, // allow /config
    debug: false, // allow /debug
    restart: false, // allow /restart + gateway restart tool
    allowFrom: {
      "*": ["user1"],
      discord: ["user:123"],
    },
    useAccessGroups: true,
  },
}
```

Command details

*   Text commands must be **standalone** messages with leading `/`.
*   `native: "auto"` turns on native commands for Discord/Telegram, leaves Slack off.
*   Override per channel: `channels.discord.commands.native` (bool or `"auto"`). `false` clears previously registered commands.
*   `channels.telegram.customCommands` adds extra Telegram bot menu entries.
*   `bash: true` enables `! <cmd>` for host shell. Requires `tools.elevated.enabled` and sender in `tools.elevated.allowFrom.<channel>`.
*   `config: true` enables `/config` (reads/writes `openclaw.json`). For gateway `chat.send` clients, persistent `/config set|unset` writes also require `operator.admin`; read-only `/config show` stays available to normal write-scoped operator clients.
*   `channels.<provider>.configWrites` gates config mutations per channel (default: true).
*   `allowFrom` is per-provider. When set, it is the **only** authorization source (channel allowlists/pairing and `useAccessGroups` are ignored).
*   `useAccessGroups: false` allows commands to bypass access-group policies when `allowFrom` is not set.

* * *

## Agent defaults

### `agents.defaults.workspace`

Default: `~/.openclaw/workspace`.

```
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

### `agents.defaults.repoRoot`

Optional repository root shown in the system prompt’s Runtime line. If unset, OpenClaw auto-detects by walking upward from the workspace.

```
{
  agents: { defaults: { repoRoot: "~/Projects/openclaw" } },
}
```

### `agents.defaults.skipBootstrap`

Disables automatic creation of workspace bootstrap files (`AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, `BOOTSTRAP.md`).

```
{
  agents: { defaults: { skipBootstrap: true } },
}
```

### `agents.defaults.bootstrapMaxChars`

Max characters per workspace bootstrap file before truncation. Default: `20000`.

```
{
  agents: { defaults: { bootstrapMaxChars: 20000 } },
}
```

### `agents.defaults.bootstrapTotalMaxChars`

Max total characters injected across all workspace bootstrap files. Default: `150000`.

```
{
  agents: { defaults: { bootstrapTotalMaxChars: 150000 } },
}
```

### `agents.defaults.bootstrapPromptTruncationWarning`

Controls agent-visible warning text when bootstrap context is truncated. Default: `"once"`.

*   `"off"`: never inject warning text into the system prompt.
*   `"once"`: inject warning once per unique truncation signature (recommended).
*   `"always"`: inject warning on every run when truncation exists.

```
{
  agents: { defaults: { bootstrapPromptTruncationWarning: "once" } }, // off | once | always
}
```

### `agents.defaults.imageMaxDimensionPx`

Max pixel size for the longest image side in transcript/tool image blocks before provider calls. Default: `1200`. Lower values usually reduce vision-token usage and request payload size for screenshot-heavy runs. Higher values preserve more visual detail.

```
{
  agents: { defaults: { imageMaxDimensionPx: 1200 } },
}
```

### `agents.defaults.userTimezone`

Timezone for system prompt context (not message timestamps). Falls back to host timezone.

```
{
  agents: { defaults: { userTimezone: "America/Chicago" } },
}
```

### `agents.defaults.timeFormat`

Time format in system prompt. Default: `auto` (OS preference).

```
{
  agents: { defaults: { timeFormat: "auto" } }, // auto | 12 | 24
}
```

### `agents.defaults.model`

```
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": { alias: "opus" },
        "minimax/MiniMax-M2.5": { alias: "minimax" },
      },
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["minimax/MiniMax-M2.5"],
      },
      imageModel: {
        primary: "openrouter/qwen/qwen-2.5-vl-72b-instruct:free",
        fallbacks: ["openrouter/google/gemini-2.0-flash-vision:free"],
      },
      pdfModel: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["openai/gpt-5-mini"],
      },
      pdfMaxBytesMb: 10,
      pdfMaxPages: 20,
      thinkingDefault: "low",
      verboseDefault: "off",
      elevatedDefault: "on",
      timeoutSeconds: 600,
      mediaMaxMb: 5,
      contextTokens: 200000,
      maxConcurrent: 3,
    },
  },
}
```

*   `model`: accepts either a string (`"provider/model"`) or an object (`{ primary, fallbacks }`).
    *   String form sets only the primary model.
    *   Object form sets primary plus ordered failover models.
*   `imageModel`: accepts either a string (`"provider/model"`) or an object (`{ primary, fallbacks }`).
    *   Used by the `image` tool path as its vision-model config.
    *   Also used as fallback routing when the selected/default model cannot accept image input.
*   `pdfModel`: accepts either a string (`"provider/model"`) or an object (`{ primary, fallbacks }`).
    *   Used by the `pdf` tool for model routing.
    *   If omitted, the PDF tool falls back to `imageModel`, then to best-effort provider defaults.
*   `pdfMaxBytesMb`: default PDF size limit for the `pdf` tool when `maxBytesMb` is not passed at call time.
*   `pdfMaxPages`: default maximum pages considered by extraction fallback mode in the `pdf` tool.
*   `model.primary`: format `provider/model` (e.g. `anthropic/claude-opus-4-6`). If you omit the provider, OpenClaw assumes `anthropic` (deprecated).
*   `models`: the configured model catalog and allowlist for `/model`. Each entry can include `alias` (shortcut) and `params` (provider-specific, for example `temperature`, `maxTokens`, `cacheRetention`, `context1m`).
*   `params` merge precedence (config): `agents.defaults.models["provider/model"].params` is the base, then `agents.list[].params` (matching agent id) overrides by key.
*   Config writers that mutate these fields (for example `/models set`, `/models set-image`, and fallback add/remove commands) save canonical object form and preserve existing fallback lists when possible.
*   `maxConcurrent`: max parallel agent runs across sessions (each session still serialized). Default: 1.

**Built-in alias shorthands** (only apply when the model is in `agents.defaults.models`):

Alias

Model

`opus`

`anthropic/claude-opus-4-6`

`sonnet`

`anthropic/claude-sonnet-4-6`

`gpt`

`openai/gpt-5.4`

`gpt-mini`

`openai/gpt-5-mini`

`gemini`

`google/gemini-3.1-pro-preview`

`gemini-flash`

`google/gemini-3-flash-preview`

`gemini-flash-lite`

`google/gemini-3.1-flash-lite-preview`

Your configured aliases always win over defaults. Z.AI GLM-4.x models automatically enable thinking mode unless you set `--thinking off` or define `agents.defaults.models["zai/<model>"].params.thinking` yourself. Z.AI models enable `tool_stream` by default for tool call streaming. Set `agents.defaults.models["zai/<model>"].params.tool_stream` to `false` to disable it. Anthropic Claude 4.6 models default to `adaptive` thinking when no explicit thinking level is set.

### `agents.defaults.cliBackends`

Optional CLI backends for text-only fallback runs (no tool calls). Useful as a backup when API providers fail.

```
{
  agents: {
    defaults: {
      cliBackends: {
        "claude-cli": {
          command: "/opt/homebrew/bin/claude",
        },
        "my-cli": {
          command: "my-cli",
          args: ["--json"],
          output: "json",
          modelArg: "--model",
          sessionArg: "--session",
          sessionMode: "existing",
          systemPromptArg: "--system",
          systemPromptWhen: "first",
          imageArg: "--image",
          imageMode: "repeat",
        },
      },
    },
  },
}
```

*   CLI backends are text-first; tools are always disabled.
*   Sessions supported when `sessionArg` is set.
*   Image pass-through supported when `imageArg` accepts file paths.

### `agents.defaults.heartbeat`

Periodic heartbeat runs.

```
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m", // 0m disables
        model: "openai/gpt-5.2-mini",
        includeReasoning: false,
        lightContext: false, // default: false; true keeps only HEARTBEAT.md from workspace bootstrap files
        session: "main",
        to: "+15555550123",
        directPolicy: "allow", // allow (default) | block
        target: "none", // default: none | options: last | whatsapp | telegram | discord | ...
        prompt: "Read HEARTBEAT.md if it exists...",
        ackMaxChars: 300,
        suppressToolErrorWarnings: false,
      },
    },
  },
}
```

*   `every`: duration string (ms/s/m/h). Default: `30m`.
*   `suppressToolErrorWarnings`: when true, suppresses tool error warning payloads during heartbeat runs.
*   `directPolicy`: direct/DM delivery policy. `allow` (default) permits direct-target delivery. `block` suppresses direct-target delivery and emits `reason=dm-blocked`.
*   `lightContext`: when true, heartbeat runs use lightweight bootstrap context and keep only `HEARTBEAT.md` from workspace bootstrap files.
*   Per-agent: set `agents.list[].heartbeat`. When any agent defines `heartbeat`, **only those agents** run heartbeats.
*   Heartbeats run full agent turns — shorter intervals burn more tokens.

### `agents.defaults.compaction`

```
{
  agents: {
    defaults: {
      compaction: {
        mode: "safeguard", // default | safeguard
        reserveTokensFloor: 24000,
        identifierPolicy: "strict", // strict | off | custom
        identifierInstructions: "Preserve deployment IDs, ticket IDs, and host:port pairs exactly.", // used when identifierPolicy=custom
        postCompactionSections: ["Session Startup", "Red Lines"], // [] disables reinjection
        model: "openrouter/anthropic/claude-sonnet-4-5", // optional compaction-only model override
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 6000,
          systemPrompt: "Session nearing compaction. Store durable memories now.",
          prompt: "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store.",
        },
      },
    },
  },
}
```

*   `mode`: `default` or `safeguard` (chunked summarization for long histories). See [Compaction](https://docs.openclaw.ai/concepts/compaction).
*   `identifierPolicy`: `strict` (default), `off`, or `custom`. `strict` prepends built-in opaque identifier retention guidance during compaction summarization.
*   `identifierInstructions`: optional custom identifier-preservation text used when `identifierPolicy=custom`.
*   `postCompactionSections`: optional AGENTS.md H2/H3 section names to re-inject after compaction. Defaults to `["Session Startup", "Red Lines"]`; set `[]` to disable reinjection. When unset or explicitly set to that default pair, older `Every Session`/`Safety` headings are also accepted as a legacy fallback.
*   `model`: optional `provider/model-id` override for compaction summarization only. Use this when the main session should keep one model but compaction summaries should run on another; when unset, compaction uses the session’s primary model.
*   `memoryFlush`: silent agentic turn before auto-compaction to store durable memories. Skipped when workspace is read-only.

### `agents.defaults.contextPruning`

Prunes **old tool results** from in-memory context before sending to the LLM. Does **not** modify session history on disk.

```
{
  agents: {
    defaults: {
      contextPruning: {
        mode: "cache-ttl", // off | cache-ttl
        ttl: "1h", // duration (ms/s/m/h), default unit: minutes
        keepLastAssistants: 3,
        softTrimRatio: 0.3,
        hardClearRatio: 0.5,
        minPrunableToolChars: 50000,
        softTrim: { maxChars: 4000, headChars: 1500, tailChars: 1500 },
        hardClear: { enabled: true, placeholder: "[Old tool result content cleared]" },
        tools: { deny: ["browser", "canvas"] },
      },
    },
  },
}
```

cache-ttl mode behavior

*   `mode: "cache-ttl"` enables pruning passes.
*   `ttl` controls how often pruning can run again (after the last cache touch).
*   Pruning soft-trims oversized tool results first, then hard-clears older tool results if needed.

**Soft-trim** keeps beginning + end and inserts `...` in the middle.**Hard-clear** replaces the entire tool result with the placeholder.Notes:

*   Image blocks are never trimmed/cleared.
*   Ratios are character-based (approximate), not exact token counts.
*   If fewer than `keepLastAssistants` assistant messages exist, pruning is skipped.

See [Session Pruning](https://docs.openclaw.ai/concepts/session-pruning) for behavior details.

### Block streaming

```
{
  agents: {
    defaults: {
      blockStreamingDefault: "off", // on | off
      blockStreamingBreak: "text_end", // text_end | message_end
      blockStreamingChunk: { minChars: 800, maxChars: 1200 },
      blockStreamingCoalesce: { idleMs: 1000 },
      humanDelay: { mode: "natural" }, // off | natural | custom (use minMs/maxMs)
    },
  },
}
```

*   Non-Telegram channels require explicit `*.blockStreaming: true` to enable block replies.
*   Channel overrides: `channels.<channel>.blockStreamingCoalesce` (and per-account variants). Signal/Slack/Discord/Google Chat default `minChars: 1500`.
*   `humanDelay`: randomized pause between block replies. `natural` = 800–2500ms. Per-agent override: `agents.list[].humanDelay`.

See [Streaming](https://docs.openclaw.ai/concepts/streaming) for behavior + chunking details.

### Typing indicators

```
{
  agents: {
    defaults: {
      typingMode: "instant", // never | instant | thinking | message
      typingIntervalSeconds: 6,
    },
  },
}
```

*   Defaults: `instant` for direct chats/mentions, `message` for unmentioned group chats.
*   Per-session overrides: `session.typingMode`, `session.typingIntervalSeconds`.

See [Typing Indicators](https://docs.openclaw.ai/concepts/typing-indicators).

### `agents.defaults.sandbox`

Optional **Docker sandboxing** for the embedded agent. See [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing) for the full guide.

```
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // off | non-main | all
        scope: "agent", // session | agent | shared
        workspaceAccess: "none", // none | ro | rw
        workspaceRoot: "~/.openclaw/sandboxes",
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          containerPrefix: "openclaw-sbx-",
          workdir: "/workspace",
          readOnlyRoot: true,
          tmpfs: ["/tmp", "/var/tmp", "/run"],
          network: "none",
          user: "1000:1000",
          capDrop: ["ALL"],
          env: { LANG: "C.UTF-8" },
          setupCommand: "apt-get update && apt-get install -y git curl jq",
          pidsLimit: 256,
          memory: "1g",
          memorySwap: "2g",
          cpus: 1,
          ulimits: {
            nofile: { soft: 1024, hard: 2048 },
            nproc: 256,
          },
          seccompProfile: "/path/to/seccomp.json",
          apparmorProfile: "openclaw-sandbox",
          dns: ["1.1.1.1", "8.8.8.8"],
          extraHosts: ["internal.service:10.0.0.5"],
          binds: ["/home/user/source:/source:rw"],
        },
        browser: {
          enabled: false,
          image: "openclaw-sandbox-browser:bookworm-slim",
          network: "openclaw-sandbox-browser",
          cdpPort: 9222,
          cdpSourceRange: "172.21.0.1/32",
          vncPort: 5900,
          noVncPort: 6080,
          headless: false,
          enableNoVnc: true,
          allowHostControl: false,
          autoStart: true,
          autoStartTimeoutMs: 12000,
        },
        prune: {
          idleHours: 24,
          maxAgeDays: 7,
        },
      },
    },
  },
  tools: {
    sandbox: {
      tools: {
        allow: [
          "exec",
          "process",
          "read",
          "write",
          "edit",
          "apply_patch",
          "sessions_list",
          "sessions_history",
          "sessions_send",
          "sessions_spawn",
          "session_status",
        ],
        deny: ["browser", "canvas", "nodes", "cron", "discord", "gateway"],
      },
    },
  },
}
```

Sandbox details

**Workspace access:**

*   `none`: per-scope sandbox workspace under `~/.openclaw/sandboxes`
*   `ro`: sandbox workspace at `/workspace`, agent workspace mounted read-only at `/agent`
*   `rw`: agent workspace mounted read/write at `/workspace`

**Scope:**

*   `session`: per-session container + workspace
*   `agent`: one container + workspace per agent (default)
*   `shared`: shared container and workspace (no cross-session isolation)

**`setupCommand`** runs once after container creation (via `sh -lc`). Needs network egress, writable root, root user.**Containers default to `network: "none"`** — set to `"bridge"` (or a custom bridge network) if the agent needs outbound access. `"host"` is blocked. `"container:<id>"` is blocked by default unless you explicitly set `sandbox.docker.dangerouslyAllowContainerNamespaceJoin: true` (break-glass).**Inbound attachments** are staged into `media/inbound/*` in the active workspace.**`docker.binds`** mounts additional host directories; global and per-agent binds are merged.**Sandboxed browser** (`sandbox.browser.enabled`): Chromium + CDP in a container. noVNC URL injected into system prompt. Does not require `browser.enabled` in `openclaw.json`. noVNC observer access uses VNC auth by default and OpenClaw emits a short-lived token URL (instead of exposing the password in the shared URL).

*   `allowHostControl: false` (default) blocks sandboxed sessions from targeting the host browser.
*   `network` defaults to `openclaw-sandbox-browser` (dedicated bridge network). Set to `bridge` only when you explicitly want global bridge connectivity.
*   `cdpSourceRange` optionally restricts CDP ingress at the container edge to a CIDR range (for example `172.21.0.1/32`).
*   `sandbox.browser.binds` mounts additional host directories into the sandbox browser container only. When set (including `[]`), it replaces `docker.binds` for the browser container.
*   Launch defaults are defined in `scripts/sandbox-browser-entrypoint.sh` and tuned for container hosts:
    *   `--remote-debugging-address=127.0.0.1`
    *   `--remote-debugging-port=<derived from OPENCLAW_BROWSER_CDP_PORT>`
    *   `--user-data-dir=${HOME}/.chrome`
    *   `--no-first-run`
    *   `--no-default-browser-check`
    *   `--disable-3d-apis`
    *   `--disable-gpu`
    *   `--disable-software-rasterizer`
    *   `--disable-dev-shm-usage`
    *   `--disable-background-networking`
    *   `--disable-features=TranslateUI`
    *   `--disable-breakpad`
    *   `--disable-crash-reporter`
    *   `--renderer-process-limit=2`
    *   `--no-zygote`
    *   `--metrics-recording-only`
    *   `--disable-extensions` (default enabled)
    *   `--disable-3d-apis`, `--disable-software-rasterizer`, and `--disable-gpu` are enabled by default and can be disabled with `OPENCLAW_BROWSER_DISABLE_GRAPHICS_FLAGS=0` if WebGL/3D usage requires it.
    *   `OPENCLAW_BROWSER_DISABLE_EXTENSIONS=0` re-enables extensions if your workflow depends on them.
    *   `--renderer-process-limit=2` can be changed with `OPENCLAW_BROWSER_RENDERER_PROCESS_LIMIT=<N>`; set `0` to use Chromium’s default process limit.
    *   plus `--no-sandbox` and `--disable-setuid-sandbox` when `noSandbox` is enabled.
    *   Defaults are the container image baseline; use a custom browser image with a custom entrypoint to change container defaults.

Build images:

```
scripts/sandbox-setup.sh           # main sandbox image
scripts/sandbox-browser-setup.sh   # optional browser image
```

### `agents.list` (per-agent overrides)

```
{
  agents: {
    list: [
      {
        id: "main",
        default: true,
        name: "Main Agent",
        workspace: "~/.openclaw/workspace",
        agentDir: "~/.openclaw/agents/main/agent",
        model: "anthropic/claude-opus-4-6", // or { primary, fallbacks }
        params: { cacheRetention: "none" }, // overrides matching defaults.models params by key
        identity: {
          name: "Samantha",
          theme: "helpful sloth",
          emoji: "🦥",
          avatar: "avatars/samantha.png",
        },
        groupChat: { mentionPatterns: ["@openclaw"] },
        sandbox: { mode: "off" },
        runtime: {
          type: "acp",
          acp: {
            agent: "codex",
            backend: "acpx",
            mode: "persistent",
            cwd: "/workspace/openclaw",
          },
        },
        subagents: { allowAgents: ["*"] },
        tools: {
          profile: "coding",
          allow: ["browser"],
          deny: ["canvas"],
          elevated: { enabled: true },
        },
      },
    ],
  },
}
```

*   `id`: stable agent id (required).
*   `default`: when multiple are set, first wins (warning logged). If none set, first list entry is default.
*   `model`: string form overrides `primary` only; object form `{ primary, fallbacks }` overrides both (`[]` disables global fallbacks). Cron jobs that only override `primary` still inherit default fallbacks unless you set `fallbacks: []`.
*   `params`: per-agent stream params merged over the selected model entry in `agents.defaults.models`. Use this for agent-specific overrides like `cacheRetention`, `temperature`, or `maxTokens` without duplicating the whole model catalog.
*   `runtime`: optional per-agent runtime descriptor. Use `type: "acp"` with `runtime.acp` defaults (`agent`, `backend`, `mode`, `cwd`) when the agent should default to ACP harness sessions.
*   `identity.avatar`: workspace-relative path, `http(s)` URL, or `data:` URI.
*   `identity` derives defaults: `ackReaction` from `emoji`, `mentionPatterns` from `name`/`emoji`.
*   `subagents.allowAgents`: allowlist of agent ids for `sessions_spawn` (`["*"]` = any; default: same agent only).
*   Sandbox inheritance guard: if the requester session is sandboxed, `sessions_spawn` rejects targets that would run unsandboxed.

* * *

## Multi-agent routing

Run multiple isolated agents inside one Gateway. See [Multi-Agent](https://docs.openclaw.ai/concepts/multi-agent).

```
{
  agents: {
    list: [
      { id: "home", default: true, workspace: "~/.openclaw/workspace-home" },
      { id: "work", workspace: "~/.openclaw/workspace-work" },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
}
```

### Binding match fields

*   `type` (optional): `route` for normal routing (missing type defaults to route), `acp` for persistent ACP conversation bindings.
*   `match.channel` (required)
*   `match.accountId` (optional; `*` = any account; omitted = default account)
*   `match.peer` (optional; `{ kind: direct|group|channel, id }`)
*   `match.guildId` / `match.teamId` (optional; channel-specific)
*   `acp` (optional; only for `type: "acp"`): `{ mode, label, cwd, backend }`

**Deterministic match order:**

1.  `match.peer`
2.  `match.guildId`
3.  `match.teamId`
4.  `match.accountId` (exact, no peer/guild/team)
5.  `match.accountId: "*"` (channel-wide)
6.  Default agent

Within each tier, the first matching `bindings` entry wins. For `type: "acp"` entries, OpenClaw resolves by exact conversation identity (`match.channel` + account + `match.peer.id`) and does not use the route binding tier order above.

### Per-agent access profiles

Full access (no sandbox)

```
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: { mode: "off" },
      },
    ],
  },
}
```

Read-only tools + workspace

No filesystem access (messaging only)

```
{
  agents: {
    list: [
      {
        id: "public",
        workspace: "~/.openclaw/workspace-public",
        sandbox: { mode: "all", scope: "agent", workspaceAccess: "none" },
        tools: {
          allow: [
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
            "whatsapp",
            "telegram",
            "slack",
            "discord",
            "gateway",
          ],
          deny: [
            "read",
            "write",
            "edit",
            "apply_patch",
            "exec",
            "process",
            "browser",
            "canvas",
            "nodes",
            "cron",
            "gateway",
            "image",
          ],
        },
      },
    ],
  },
}
```

See [Multi-Agent Sandbox & Tools](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools) for precedence details.

* * *

## Session

```
{
  session: {
    scope: "per-sender",
    dmScope: "main", // main | per-peer | per-channel-peer | per-account-channel-peer
    identityLinks: {
      alice: ["telegram:123456789", "discord:987654321012345678"],
    },
    reset: {
      mode: "daily", // daily | idle
      atHour: 4,
      idleMinutes: 60,
    },
    resetByType: {
      thread: { mode: "daily", atHour: 4 },
      direct: { mode: "idle", idleMinutes: 240 },
      group: { mode: "idle", idleMinutes: 120 },
    },
    resetTriggers: ["/new", "/reset"],
    store: "~/.openclaw/agents/{agentId}/sessions/sessions.json",
    parentForkMaxTokens: 100000, // skip parent-thread fork above this token count (0 disables)
    maintenance: {
      mode: "warn", // warn | enforce
      pruneAfter: "30d",
      maxEntries: 500,
      rotateBytes: "10mb",
      resetArchiveRetention: "30d", // duration or false
      maxDiskBytes: "500mb", // optional hard budget
      highWaterBytes: "400mb", // optional cleanup target
    },
    threadBindings: {
      enabled: true,
      idleHours: 24, // default inactivity auto-unfocus in hours (`0` disables)
      maxAgeHours: 0, // default hard max age in hours (`0` disables)
    },
    mainKey: "main", // legacy (runtime always uses "main")
    agentToAgent: { maxPingPongTurns: 5 },
    sendPolicy: {
      rules: [{ action: "deny", match: { channel: "discord", chatType: "group" } }],
      default: "allow",
    },
  },
}
```

Session field details

*   **`dmScope`**: how DMs are grouped.
    *   `main`: all DMs share the main session.
    *   `per-peer`: isolate by sender id across channels.
    *   `per-channel-peer`: isolate per channel + sender (recommended for multi-user inboxes).
    *   `per-account-channel-peer`: isolate per account + channel + sender (recommended for multi-account).
*   **`identityLinks`**: map canonical ids to provider-prefixed peers for cross-channel session sharing.
*   **`reset`**: primary reset policy. `daily` resets at `atHour` local time; `idle` resets after `idleMinutes`. When both configured, whichever expires first wins.
*   **`resetByType`**: per-type overrides (`direct`, `group`, `thread`). Legacy `dm` accepted as alias for `direct`.
*   **`parentForkMaxTokens`**: max parent-session `totalTokens` allowed when creating a forked thread session (default `100000`).
    *   If parent `totalTokens` is above this value, OpenClaw starts a fresh thread session instead of inheriting parent transcript history.
    *   Set `0` to disable this guard and always allow parent forking.
*   **`mainKey`**: legacy field. Runtime now always uses `"main"` for the main direct-chat bucket.
*   **`sendPolicy`**: match by `channel`, `chatType` (`direct|group|channel`, with legacy `dm` alias), `keyPrefix`, or `rawKeyPrefix`. First deny wins.
*   **`maintenance`**: session-store cleanup + retention controls.
    *   `mode`: `warn` emits warnings only; `enforce` applies cleanup.
    *   `pruneAfter`: age cutoff for stale entries (default `30d`).
    *   `maxEntries`: maximum number of entries in `sessions.json` (default `500`).
    *   `rotateBytes`: rotate `sessions.json` when it exceeds this size (default `10mb`).
    *   `resetArchiveRetention`: retention for `*.reset.<timestamp>` transcript archives. Defaults to `pruneAfter`; set `false` to disable.
    *   `maxDiskBytes`: optional sessions-directory disk budget. In `warn` mode it logs warnings; in `enforce` mode it removes oldest artifacts/sessions first.
    *   `highWaterBytes`: optional target after budget cleanup. Defaults to `80%` of `maxDiskBytes`.
*   **`threadBindings`**: global defaults for thread-bound session features.
    *   `enabled`: master default switch (providers can override; Discord uses `channels.discord.threadBindings.enabled`)
    *   `idleHours`: default inactivity auto-unfocus in hours (`0` disables; providers can override)
    *   `maxAgeHours`: default hard max age in hours (`0` disables; providers can override)

* * *

## Messages

```
{
  messages: {
    responsePrefix: "🦞", // or "auto"
    ackReaction: "👀",
    ackReactionScope: "group-mentions", // group-mentions | group-all | direct | all
    removeAckAfterReply: false,
    queue: {
      mode: "collect", // steer | followup | collect | steer-backlog | steer+backlog | queue | interrupt
      debounceMs: 1000,
      cap: 20,
      drop: "summarize", // old | new | summarize
      byChannel: {
        whatsapp: "collect",
        telegram: "collect",
      },
    },
    inbound: {
      debounceMs: 2000, // 0 disables
      byChannel: {
        whatsapp: 5000,
        slack: 1500,
      },
    },
  },
}
```

### Response prefix

Per-channel/account overrides: `channels.<channel>.responsePrefix`, `channels.<channel>.accounts.<id>.responsePrefix`. Resolution (most specific wins): account → channel → global. `""` disables and stops cascade. `"auto"` derives `[{identity.name}]`. **Template variables:**

Variable

Description

Example

`{model}`

Short model name

`claude-opus-4-6`

`{modelFull}`

Full model identifier

`anthropic/claude-opus-4-6`

`{provider}`

Provider name

`anthropic`

`{thinkingLevel}`

Current thinking level

`high`, `low`, `off`

`{identity.name}`

Agent identity name

(same as `"auto"`)

Variables are case-insensitive. `{think}` is an alias for `{thinkingLevel}`.

### Ack reaction

*   Defaults to active agent’s `identity.emoji`, otherwise `"👀"`. Set `""` to disable.
*   Per-channel overrides: `channels.<channel>.ackReaction`, `channels.<channel>.accounts.<id>.ackReaction`.
*   Resolution order: account → channel → `messages.ackReaction` → identity fallback.
*   Scope: `group-mentions` (default), `group-all`, `direct`, `all`.
*   `removeAckAfterReply`: removes ack after reply (Slack/Discord/Telegram/Google Chat only).

### Inbound debounce

Batches rapid text-only messages from the same sender into a single agent turn. Media/attachments flush immediately. Control commands bypass debouncing.

### TTS (text-to-speech)

```
{
  messages: {
    tts: {
      auto: "always", // off | always | inbound | tagged
      mode: "final", // final | all
      provider: "elevenlabs",
      summaryModel: "openai/gpt-4.1-mini",
      modelOverrides: { enabled: true },
      maxTextLength: 4000,
      timeoutMs: 30000,
      prefsPath: "~/.openclaw/settings/tts.json",
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
      openai: {
        apiKey: "openai_api_key",
        baseUrl: "https://api.openai.com/v1",
        model: "gpt-4o-mini-tts",
        voice: "alloy",
      },
    },
  },
}
```

*   `auto` controls auto-TTS. `/tts off|always|inbound|tagged` overrides per session.
*   `summaryModel` overrides `agents.defaults.model.primary` for auto-summary.
*   `modelOverrides` is enabled by default; `modelOverrides.allowProvider` defaults to `false` (opt-in).
*   API keys fall back to `ELEVENLABS_API_KEY`/`XI_API_KEY` and `OPENAI_API_KEY`.
*   `openai.baseUrl` overrides the OpenAI TTS endpoint. Resolution order is config, then `OPENAI_TTS_BASE_URL`, then `https://api.openai.com/v1`.
*   When `openai.baseUrl` points to a non-OpenAI endpoint, OpenClaw treats it as an OpenAI-compatible TTS server and relaxes model/voice validation.

* * *

## Talk

Defaults for Talk mode (macOS/iOS/Android).

```
{
  talk: {
    voiceId: "elevenlabs_voice_id",
    voiceAliases: {
      Clawd: "EXAVITQu4vr4xnSDxMaL",
      Roger: "CwhRBWXzGAHq8TQ4Fs17",
    },
    modelId: "eleven_v3",
    outputFormat: "mp3_44100_128",
    apiKey: "elevenlabs_api_key",
    silenceTimeoutMs: 1500,
    interruptOnSpeech: true,
  },
}
```

*   Voice IDs fall back to `ELEVENLABS_VOICE_ID` or `SAG_VOICE_ID`.
*   `apiKey` and `providers.*.apiKey` accept plaintext strings or SecretRef objects.
*   `ELEVENLABS_API_KEY` fallback applies only when no Talk API key is configured.
*   `voiceAliases` lets Talk directives use friendly names.
*   `silenceTimeoutMs` controls how long Talk mode waits after user silence before it sends the transcript. Unset keeps the platform default pause window (`700 ms on macOS and Android, 900 ms on iOS`).

* * *

### Tool profiles

`tools.profile` sets a base allowlist before `tools.allow`/`tools.deny`: Local onboarding defaults new local configs to `tools.profile: "coding"` when unset (existing explicit profiles are preserved).

Profile

Includes

`minimal`

`session_status` only

`coding`

`group:fs`, `group:runtime`, `group:sessions`, `group:memory`, `image`

`messaging`

`group:messaging`, `sessions_list`, `sessions_history`, `sessions_send`, `session_status`

`full`

No restriction (same as unset)

### Tool groups

Group

Tools

`group:runtime`

`exec`, `process` (`bash` is accepted as an alias for `exec`)

`group:fs`

`read`, `write`, `edit`, `apply_patch`

`group:sessions`

`sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`

`group:memory`

`memory_search`, `memory_get`

`group:web`

`web_search`, `web_fetch`

`group:ui`

`browser`, `canvas`

`group:automation`

`cron`, `gateway`

`group:messaging`

`message`

`group:nodes`

`nodes`

`group:openclaw`

All built-in tools (excludes provider plugins)

### `tools.allow` / `tools.deny`

Global tool allow/deny policy (deny wins). Case-insensitive, supports `*` wildcards. Applied even when Docker sandbox is off.

```
{
  tools: { deny: ["browser", "canvas"] },
}
```

### `tools.byProvider`

Further restrict tools for specific providers or models. Order: base profile → provider profile → allow/deny.

```
{
  tools: {
    profile: "coding",
    byProvider: {
      "google-antigravity": { profile: "minimal" },
      "openai/gpt-5.2": { allow: ["group:fs", "sessions_list"] },
    },
  },
}
```

### `tools.elevated`

Controls elevated (host) exec access:

```
{
  tools: {
    elevated: {
      enabled: true,
      allowFrom: {
        whatsapp: ["+15555550123"],
        discord: ["1234567890123", "987654321098765432"],
      },
    },
  },
}
```

*   Per-agent override (`agents.list[].tools.elevated`) can only further restrict.
*   `/elevated on|off|ask|full` stores state per session; inline directives apply to single message.
*   Elevated `exec` runs on the host, bypasses sandboxing.

### `tools.exec`

```
{
  tools: {
    exec: {
      backgroundMs: 10000,
      timeoutSec: 1800,
      cleanupMs: 1800000,
      notifyOnExit: true,
      notifyOnExitEmptySuccess: false,
      applyPatch: {
        enabled: false,
        allowModels: ["gpt-5.2"],
      },
    },
  },
}
```

### `tools.loopDetection`

Tool-loop safety checks are **disabled by default**. Set `enabled: true` to activate detection. Settings can be defined globally in `tools.loopDetection` and overridden per-agent at `agents.list[].tools.loopDetection`.

```
{
  tools: {
    loopDetection: {
      enabled: true,
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

*   `historySize`: max tool-call history retained for loop analysis.
*   `warningThreshold`: repeating no-progress pattern threshold for warnings.
*   `criticalThreshold`: higher repeating threshold for blocking critical loops.
*   `globalCircuitBreakerThreshold`: hard stop threshold for any no-progress run.
*   `detectors.genericRepeat`: warn on repeated same-tool/same-args calls.
*   `detectors.knownPollNoProgress`: warn/block on known poll tools (`process.poll`, `command_status`, etc.).
*   `detectors.pingPong`: warn/block on alternating no-progress pair patterns.
*   If `warningThreshold >= criticalThreshold` or `criticalThreshold >= globalCircuitBreakerThreshold`, validation fails.

### `tools.web`

```
{
  tools: {
    web: {
      search: {
        enabled: true,
        apiKey: "brave_api_key", // or BRAVE_API_KEY env
        maxResults: 5,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
      },
      fetch: {
        enabled: true,
        maxChars: 50000,
        maxCharsCap: 50000,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
        userAgent: "custom-ua",
      },
    },
  },
}
```

### `tools.media`

Configures inbound media understanding (image/audio/video):

```
{
  tools: {
    media: {
      concurrency: 2,
      audio: {
        enabled: true,
        maxBytes: 20971520,
        scope: {
          default: "deny",
          rules: [{ action: "allow", match: { chatType: "direct" } }],
        },
        models: [
          { provider: "openai", model: "gpt-4o-mini-transcribe" },
          { type: "cli", command: "whisper", args: ["--model", "base", "{{MediaPath}}"] },
        ],
      },
      video: {
        enabled: true,
        maxBytes: 52428800,
        models: [{ provider: "google", model: "gemini-3-flash-preview" }],
      },
    },
  },
}
```

Media model entry fields

**Provider entry** (`type: "provider"` or omitted):

*   `provider`: API provider id (`openai`, `anthropic`, `google`/`gemini`, `groq`, etc.)
*   `model`: model id override
*   `profile` / `preferredProfile`: `auth-profiles.json` profile selection

**CLI entry** (`type: "cli"`):

*   `command`: executable to run
*   `args`: templated args (supports `{{MediaPath}}`, `{{Prompt}}`, `{{MaxChars}}`, etc.)

**Common fields:**

*   `capabilities`: optional list (`image`, `audio`, `video`). Defaults: `openai`/`anthropic`/`minimax` → image, `google` → image+audio+video, `groq` → audio.
*   `prompt`, `maxChars`, `maxBytes`, `timeoutSeconds`, `language`: per-entry overrides.
*   Failures fall back to the next entry.

Provider auth follows standard order: `auth-profiles.json` → env vars → `models.providers.*.apiKey`.

### `tools.agentToAgent`

```
{
  tools: {
    agentToAgent: {
      enabled: false,
      allow: ["home", "work"],
    },
  },
}
```

### `tools.sessions`

Controls which sessions can be targeted by the session tools (`sessions_list`, `sessions_history`, `sessions_send`). Default: `tree` (current session + sessions spawned by it, such as subagents).

```
{
  tools: {
    sessions: {
      // "self" | "tree" | "agent" | "all"
      visibility: "tree",
    },
  },
}
```

Notes:

*   `self`: only the current session key.
*   `tree`: current session + sessions spawned by the current session (subagents).
*   `agent`: any session belonging to the current agent id (can include other users if you run per-sender sessions under the same agent id).
*   `all`: any session. Cross-agent targeting still requires `tools.agentToAgent`.
*   Sandbox clamp: when the current session is sandboxed and `agents.defaults.sandbox.sessionToolsVisibility="spawned"`, visibility is forced to `tree` even if `tools.sessions.visibility="all"`.

### `tools.sessions_spawn`

Controls inline attachment support for `sessions_spawn`.

```
{
  tools: {
    sessions_spawn: {
      attachments: {
        enabled: false, // opt-in: set true to allow inline file attachments
        maxTotalBytes: 5242880, // 5 MB total across all files
        maxFiles: 50,
        maxFileBytes: 1048576, // 1 MB per file
        retainOnSessionKeep: false, // keep attachments when cleanup="keep"
      },
    },
  },
}
```

Notes:

*   Attachments are only supported for `runtime: "subagent"`. ACP runtime rejects them.
*   Files are materialized into the child workspace at `.openclaw/attachments/<uuid>/` with a `.manifest.json`.
*   Attachment content is automatically redacted from transcript persistence.
*   Base64 inputs are validated with strict alphabet/padding checks and a pre-decode size guard.
*   File permissions are `0700` for directories and `0600` for files.
*   Cleanup follows the `cleanup` policy: `delete` always removes attachments; `keep` retains them only when `retainOnSessionKeep: true`.

### `tools.subagents`

```
{
  agents: {
    defaults: {
      subagents: {
        model: "minimax/MiniMax-M2.5",
        maxConcurrent: 1,
        runTimeoutSeconds: 900,
        archiveAfterMinutes: 60,
      },
    },
  },
}
```

*   `model`: default model for spawned sub-agents. If omitted, sub-agents inherit the caller’s model.
*   `runTimeoutSeconds`: default timeout (seconds) for `sessions_spawn` when the tool call omits `runTimeoutSeconds`. `0` means no timeout.
*   Per-subagent tool policy: `tools.subagents.tools.allow` / `tools.subagents.tools.deny`.

* * *

## Custom providers and base URLs

OpenClaw uses the pi-coding-agent model catalog. Add custom providers via `models.providers` in config or `~/.openclaw/agents/<agentId>/agent/models.json`.

```
{
  models: {
    mode: "merge", // merge (default) | replace
    providers: {
      "custom-proxy": {
        baseUrl: "http://localhost:4000/v1",
        apiKey: "LITELLM_KEY",
        api: "openai-completions", // openai-completions | openai-responses | anthropic-messages | google-generative-ai
        models: [
          {
            id: "llama-3.1-8b",
            name: "Llama 3.1 8B",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 128000,
            maxTokens: 32000,
          },
        ],
      },
    },
  },
}
```

*   Use `authHeader: true` + `headers` for custom auth needs.
*   Override agent config root with `OPENCLAW_AGENT_DIR` (or `PI_CODING_AGENT_DIR`).
*   Merge precedence for matching provider IDs:
    *   Non-empty agent `models.json` `baseUrl` values win.
    *   Non-empty agent `apiKey` values win only when that provider is not SecretRef-managed in current config/auth-profile context.
    *   SecretRef-managed provider `apiKey` values are refreshed from source markers (`ENV_VAR_NAME` for env refs, `secretref-managed` for file/exec refs) instead of persisting resolved secrets.
    *   Empty or missing agent `apiKey`/`baseUrl` fall back to `models.providers` in config.
    *   Matching model `contextWindow`/`maxTokens` use the higher value between explicit config and implicit catalog values.
    *   Use `models.mode: "replace"` when you want config to fully rewrite `models.json`.

### Provider field details

*   `models.mode`: provider catalog behavior (`merge` or `replace`).
*   `models.providers`: custom provider map keyed by provider id.
*   `models.providers.*.api`: request adapter (`openai-completions`, `openai-responses`, `anthropic-messages`, `google-generative-ai`, etc).
*   `models.providers.*.apiKey`: provider credential (prefer SecretRef/env substitution).
*   `models.providers.*.auth`: auth strategy (`api-key`, `token`, `oauth`, `aws-sdk`).
*   `models.providers.*.injectNumCtxForOpenAICompat`: for Ollama + `openai-completions`, inject `options.num_ctx` into requests (default: `true`).
*   `models.providers.*.authHeader`: force credential transport in the `Authorization` header when required.
*   `models.providers.*.baseUrl`: upstream API base URL.
*   `models.providers.*.headers`: extra static headers for proxy/tenant routing.
*   `models.providers.*.models`: explicit provider model catalog entries.
*   `models.providers.*.models.*.compat.supportsDeveloperRole`: optional compatibility hint. For `api: "openai-completions"` with a non-empty non-native `baseUrl` (host not `api.openai.com`), OpenClaw forces this to `false` at runtime. Empty/omitted `baseUrl` keeps default OpenAI behavior.
*   `models.bedrockDiscovery`: Bedrock auto-discovery settings root.
*   `models.bedrockDiscovery.enabled`: turn discovery polling on/off.
*   `models.bedrockDiscovery.region`: AWS region for discovery.
*   `models.bedrockDiscovery.providerFilter`: optional provider-id filter for targeted discovery.
*   `models.bedrockDiscovery.refreshInterval`: polling interval for discovery refresh.
*   `models.bedrockDiscovery.defaultContextWindow`: fallback context window for discovered models.
*   `models.bedrockDiscovery.defaultMaxTokens`: fallback max output tokens for discovered models.

### Provider examples

Cerebras (GLM 4.6 / 4.7)

```
{
  env: { CEREBRAS_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: {
        primary: "cerebras/zai-glm-4.7",
        fallbacks: ["cerebras/zai-glm-4.6"],
      },
      models: {
        "cerebras/zai-glm-4.7": { alias: "GLM 4.7 (Cerebras)" },
        "cerebras/zai-glm-4.6": { alias: "GLM 4.6 (Cerebras)" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      cerebras: {
        baseUrl: "https://api.cerebras.ai/v1",
        apiKey: "${CEREBRAS_API_KEY}",
        api: "openai-completions",
        models: [
          { id: "zai-glm-4.7", name: "GLM 4.7 (Cerebras)" },
          { id: "zai-glm-4.6", name: "GLM 4.6 (Cerebras)" },
        ],
      },
    },
  },
}
```

Use `cerebras/zai-glm-4.7` for Cerebras; `zai/glm-4.7` for Z.AI direct.

OpenCode Zen

```
{
  agents: {
    defaults: {
      model: { primary: "opencode/claude-opus-4-6" },
      models: { "opencode/claude-opus-4-6": { alias: "Opus" } },
    },
  },
}
```

Set `OPENCODE_API_KEY` (or `OPENCODE_ZEN_API_KEY`). Shortcut: `openclaw onboard --auth-choice opencode-zen`.

Z.AI (GLM-4.7)

```
{
  agents: {
    defaults: {
      model: { primary: "zai/glm-4.7" },
      models: { "zai/glm-4.7": {} },
    },
  },
}
```

Set `ZAI_API_KEY`. `z.ai/*` and `z-ai/*` are accepted aliases. Shortcut: `openclaw onboard --auth-choice zai-api-key`.

*   General endpoint: `https://api.z.ai/api/paas/v4`
*   Coding endpoint (default): `https://api.z.ai/api/coding/paas/v4`
*   For the general endpoint, define a custom provider with the base URL override.

Moonshot AI (Kimi)

```
{
  env: { MOONSHOT_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "moonshot/kimi-k2.5" },
      models: { "moonshot/kimi-k2.5": { alias: "Kimi K2.5" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "kimi-k2.5",
            name: "Kimi K2.5",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

For the China endpoint: `baseUrl: "https://api.moonshot.cn/v1"` or `openclaw onboard --auth-choice moonshot-api-key-cn`.

Kimi Coding

```
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "kimi-coding/k2p5" },
      models: { "kimi-coding/k2p5": { alias: "Kimi K2.5" } },
    },
  },
}
```

Anthropic-compatible, built-in provider. Shortcut: `openclaw onboard --auth-choice kimi-code-api-key`.

Synthetic (Anthropic-compatible)

```
{
  env: { SYNTHETIC_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.5" },
      models: { "synthetic/hf:MiniMaxAI/MiniMax-M2.5": { alias: "MiniMax M2.5" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "hf:MiniMaxAI/MiniMax-M2.5",
            name: "MiniMax M2.5",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 192000,
            maxTokens: 65536,
          },
        ],
      },
    },
  },
}
```

Base URL should omit `/v1` (Anthropic client appends it). Shortcut: `openclaw onboard --auth-choice synthetic-api-key`.

MiniMax M2.5 (direct)

```
{
  agents: {
    defaults: {
      model: { primary: "minimax/MiniMax-M2.5" },
      models: {
        "minimax/MiniMax-M2.5": { alias: "Minimax" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      minimax: {
        baseUrl: "https://api.minimax.io/anthropic",
        apiKey: "${MINIMAX_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "MiniMax-M2.5",
            name: "MiniMax M2.5",
            reasoning: false,
            input: ["text"],
            cost: { input: 15, output: 60, cacheRead: 2, cacheWrite: 10 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Set `MINIMAX_API_KEY`. Shortcut: `openclaw onboard --auth-choice minimax-api`.

Local models (LM Studio)

See [Local Models](https://docs.openclaw.ai/gateway/local-models). TL;DR: run MiniMax M2.5 via LM Studio Responses API on serious hardware; keep hosted models merged for fallback.

* * *

## Skills

```
{
  skills: {
    allowBundled: ["gemini", "peekaboo"],
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills"],
    },
    install: {
      preferBrew: true,
      nodeManager: "npm", // npm | pnpm | yarn
    },
    entries: {
      "nano-banana-pro": {
        apiKey: { source: "env", provider: "default", id: "GEMINI_API_KEY" }, // or plaintext string
        env: { GEMINI_API_KEY: "GEMINI_KEY_HERE" },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

*   `allowBundled`: optional allowlist for bundled skills only (managed/workspace skills unaffected).
*   `entries.<skillKey>.enabled: false` disables a skill even if bundled/installed.
*   `entries.<skillKey>.apiKey`: convenience for skills declaring a primary env var (plaintext string or SecretRef object).

* * *

## Plugins

```
{
  plugins: {
    enabled: true,
    allow: ["voice-call"],
    deny: [],
    load: {
      paths: ["~/Projects/oss/voice-call-extension"],
    },
    entries: {
      "voice-call": {
        enabled: true,
        hooks: {
          allowPromptInjection: false,
        },
        config: { provider: "twilio" },
      },
    },
  },
}
```

*   Loaded from `~/.openclaw/extensions`, `<workspace>/.openclaw/extensions`, plus `plugins.load.paths`.
*   **Config changes require a gateway restart.**
*   `allow`: optional allowlist (only listed plugins load). `deny` wins.
*   `plugins.entries.<id>.apiKey`: plugin-level API key convenience field (when supported by the plugin).
*   `plugins.entries.<id>.env`: plugin-scoped env var map.
*   `plugins.entries.<id>.hooks.allowPromptInjection`: when `false`, core blocks `before_prompt_build` and ignores prompt-mutating fields from legacy `before_agent_start`, while preserving legacy `modelOverride` and `providerOverride`.
*   `plugins.entries.<id>.config`: plugin-defined config object (validated by plugin schema).
*   `plugins.slots.memory`: pick the active memory plugin id, or `"none"` to disable memory plugins.
*   `plugins.slots.contextEngine`: pick the active context engine plugin id; defaults to `"legacy"` unless you install and select another engine.
*   `plugins.installs`: CLI-managed install metadata used by `openclaw plugins update`.
    *   Includes `source`, `spec`, `sourcePath`, `installPath`, `version`, `resolvedName`, `resolvedVersion`, `resolvedSpec`, `integrity`, `shasum`, `resolvedAt`, `installedAt`.
    *   Treat `plugins.installs.*` as managed state; prefer CLI commands over manual edits.

See [Plugins](https://docs.openclaw.ai/tools/plugin).

* * *

## Browser

```
{
  browser: {
    enabled: true,
    evaluateEnabled: true,
    defaultProfile: "chrome",
    ssrfPolicy: {
      dangerouslyAllowPrivateNetwork: true, // default trusted-network mode
      // allowPrivateNetwork: true, // legacy alias
      // hostnameAllowlist: ["*.example.com", "example.com"],
      // allowedHostnames: ["localhost"],
    },
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },
      work: { cdpPort: 18801, color: "#0066CC" },
      remote: { cdpUrl: "http://10.0.0.42:9222", color: "#00AA00" },
    },
    color: "#FF4500",
    // headless: false,
    // noSandbox: false,
    // extraArgs: [],
    // relayBindHost: "0.0.0.0", // only when the extension relay must be reachable across namespaces (for example WSL2)
    // executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    // attachOnly: false,
  },
}
```

*   `evaluateEnabled: false` disables `act:evaluate` and `wait --fn`.
*   `ssrfPolicy.dangerouslyAllowPrivateNetwork` defaults to `true` when unset (trusted-network model).
*   Set `ssrfPolicy.dangerouslyAllowPrivateNetwork: false` for strict public-only browser navigation.
*   `ssrfPolicy.allowPrivateNetwork` remains supported as a legacy alias.
*   In strict mode, use `ssrfPolicy.hostnameAllowlist` and `ssrfPolicy.allowedHostnames` for explicit exceptions.
*   Remote profiles are attach-only (start/stop/reset disabled).
*   Auto-detect order: default browser if Chromium-based → Chrome → Brave → Edge → Chromium → Chrome Canary.
*   Control service: loopback only (port derived from `gateway.port`, default `18791`).
*   `extraArgs` appends extra launch flags to local Chromium startup (for example `--disable-gpu`, window sizing, or debug flags).
*   `relayBindHost` changes where the Chrome extension relay listens. Leave unset for loopback-only access; set an explicit non-loopback bind address such as `0.0.0.0` only when the relay must cross a namespace boundary (for example WSL2) and the host network is already trusted.

* * *

## UI

```
{
  ui: {
    seamColor: "#FF4500",
    assistant: {
      name: "OpenClaw",
      avatar: "CB", // emoji, short text, image URL, or data URI
    },
  },
}
```

*   `seamColor`: accent color for native app UI chrome (Talk Mode bubble tint, etc.).
*   `assistant`: Control UI identity override. Falls back to active agent identity.

* * *

## Gateway

```
{
  gateway: {
    mode: "local", // local | remote
    port: 18789,
    bind: "loopback",
    auth: {
      mode: "token", // none | token | password | trusted-proxy
      token: "your-token",
      // password: "your-password", // or OPENCLAW_GATEWAY_PASSWORD
      // trustedProxy: { userHeader: "x-forwarded-user" }, // for mode=trusted-proxy; see /gateway/trusted-proxy-auth
      allowTailscale: true,
      rateLimit: {
        maxAttempts: 10,
        windowMs: 60000,
        lockoutMs: 300000,
        exemptLoopback: true,
      },
    },
    tailscale: {
      mode: "off", // off | serve | funnel
      resetOnExit: false,
    },
    controlUi: {
      enabled: true,
      basePath: "/openclaw",
      // root: "dist/control-ui",
      // allowedOrigins: ["https://control.example.com"], // required for non-loopback Control UI
      // dangerouslyAllowHostHeaderOriginFallback: false, // dangerous Host-header origin fallback mode
      // allowInsecureAuth: false,
      // dangerouslyDisableDeviceAuth: false,
    },
    remote: {
      url: "ws://gateway.tailnet:18789",
      transport: "ssh", // ssh | direct
      token: "your-token",
      // password: "your-password",
    },
    trustedProxies: ["10.0.0.1"],
    // Optional. Default false.
    allowRealIpFallback: false,
    tools: {
      // Additional /tools/invoke HTTP denies
      deny: ["browser"],
      // Remove tools from the default HTTP deny list
      allow: ["gateway"],
    },
  },
}
```

Gateway field details

*   `mode`: `local` (run gateway) or `remote` (connect to remote gateway). Gateway refuses to start unless `local`.
*   `port`: single multiplexed port for WS + HTTP. Precedence: `--port` > `OPENCLAW_GATEWAY_PORT` > `gateway.port` > `18789`.
*   `bind`: `auto`, `loopback` (default), `lan` (`0.0.0.0`), `tailnet` (Tailscale IP only), or `custom`.
*   **Legacy bind aliases**: use bind mode values in `gateway.bind` (`auto`, `loopback`, `lan`, `tailnet`, `custom`), not host aliases (`0.0.0.0`, `127.0.0.1`, `localhost`, `::`, `::1`).
*   **Docker note**: the default `loopback` bind listens on `127.0.0.1` inside the container. With Docker bridge networking (`-p 18789:18789`), traffic arrives on `eth0`, so the gateway is unreachable. Use `--network host`, or set `bind: "lan"` (or `bind: "custom"` with `customBindHost: "0.0.0.0"`) to listen on all interfaces.
*   **Auth**: required by default. Non-loopback binds require a shared token/password. Onboarding wizard generates a token by default.
*   If both `gateway.auth.token` and `gateway.auth.password` are configured (including SecretRefs), set `gateway.auth.mode` explicitly to `token` or `password`. Startup and service install/repair flows fail when both are configured and mode is unset.
*   `gateway.auth.mode: "none"`: explicit no-auth mode. Use only for trusted local loopback setups; this is intentionally not offered by onboarding prompts.
*   `gateway.auth.mode: "trusted-proxy"`: delegate auth to an identity-aware reverse proxy and trust identity headers from `gateway.trustedProxies` (see [Trusted Proxy Auth](https://docs.openclaw.ai/gateway/trusted-proxy-auth)).
*   `gateway.auth.allowTailscale`: when `true`, Tailscale Serve identity headers can satisfy Control UI/WebSocket auth (verified via `tailscale whois`); HTTP API endpoints still require token/password auth. This tokenless flow assumes the gateway host is trusted. Defaults to `true` when `tailscale.mode = "serve"`.
*   `gateway.auth.rateLimit`: optional failed-auth limiter. Applies per client IP and per auth scope (shared-secret and device-token are tracked independently). Blocked attempts return `429` + `Retry-After`.
    *   `gateway.auth.rateLimit.exemptLoopback` defaults to `true`; set `false` when you intentionally want localhost traffic rate-limited too (for test setups or strict proxy deployments).
*   Browser-origin WS auth attempts are always throttled with loopback exemption disabled (defense-in-depth against browser-based localhost brute force).
*   `tailscale.mode`: `serve` (tailnet only, loopback bind) or `funnel` (public, requires auth).
*   `controlUi.allowedOrigins`: explicit browser-origin allowlist for Gateway WebSocket connects. Required when browser clients are expected from non-loopback origins.
*   `controlUi.dangerouslyAllowHostHeaderOriginFallback`: dangerous mode that enables Host-header origin fallback for deployments that intentionally rely on Host-header origin policy.
*   `remote.transport`: `ssh` (default) or `direct` (ws/wss). For `direct`, `remote.url` must be `ws://` or `wss://`.
*   `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1`: client-side break-glass override that allows plaintext `ws://` to trusted private-network IPs; default remains loopback-only for plaintext.
*   `gateway.remote.token` / `.password` are remote-client credential fields. They do not configure gateway auth by themselves.
*   Local gateway call paths can use `gateway.remote.*` as fallback when `gateway.auth.*` is unset.
*   `trustedProxies`: reverse proxy IPs that terminate TLS. Only list proxies you control.
*   `allowRealIpFallback`: when `true`, the gateway accepts `X-Real-IP` if `X-Forwarded-For` is missing. Default `false` for fail-closed behavior.
*   `gateway.tools.deny`: extra tool names blocked for HTTP `POST /tools/invoke` (extends default deny list).
*   `gateway.tools.allow`: remove tool names from the default HTTP deny list.

### OpenAI-compatible endpoints

*   Chat Completions: disabled by default. Enable with `gateway.http.endpoints.chatCompletions.enabled: true`.
*   Responses API: `gateway.http.endpoints.responses.enabled`.
*   Responses URL-input hardening:
    *   `gateway.http.endpoints.responses.maxUrlParts`
    *   `gateway.http.endpoints.responses.files.urlAllowlist`
    *   `gateway.http.endpoints.responses.images.urlAllowlist`
*   Optional response hardening header:
    *   `gateway.http.securityHeaders.strictTransportSecurity` (set only for HTTPS origins you control; see [Trusted Proxy Auth](https://docs.openclaw.ai/gateway/trusted-proxy-auth#tls-termination-and-hsts))

### Multi-instance isolation

Run multiple gateways on one host with unique ports and state dirs:

```
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json \
OPENCLAW_STATE_DIR=~/.openclaw-a \
openclaw gateway --port 19001
```

Convenience flags: `--dev` (uses `~/.openclaw-dev` + port `19001`), `--profile <name>` (uses `~/.openclaw-<name>`). See [Multiple Gateways](https://docs.openclaw.ai/gateway/multiple-gateways).

* * *

## Hooks

```
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
    maxBodyBytes: 262144,
    defaultSessionKey: "hook:ingress",
    allowRequestSessionKey: false,
    allowedSessionKeyPrefixes: ["hook:"],
    allowedAgentIds: ["hooks", "main"],
    presets: ["gmail"],
    transformsDir: "~/.openclaw/hooks/transforms",
    mappings: [
      {
        match: { path: "gmail" },
        action: "agent",
        agentId: "hooks",
        wakeMode: "now",
        name: "Gmail",
        sessionKey: "hook:gmail:{{messages[0].id}}",
        messageTemplate: "From: {{messages[0].from}}\nSubject: {{messages[0].subject}}\n{{messages[0].snippet}}",
        deliver: true,
        channel: "last",
        model: "openai/gpt-5.2-mini",
      },
    ],
  },
}
```

Auth: `Authorization: Bearer <token>` or `x-openclaw-token: <token>`. **Endpoints:**

*   `POST /hooks/wake` → `{ text, mode?: "now"|"next-heartbeat" }`
*   `POST /hooks/agent` → `{ message, name?, agentId?, sessionKey?, wakeMode?, deliver?, channel?, to?, model?, thinking?, timeoutSeconds? }`
    *   `sessionKey` from request payload is accepted only when `hooks.allowRequestSessionKey=true` (default: `false`).
*   `POST /hooks/<name>` → resolved via `hooks.mappings`

Mapping details

*   `match.path` matches sub-path after `/hooks` (e.g. `/hooks/gmail` → `gmail`).
*   `match.source` matches a payload field for generic paths.
*   Templates like `{{messages[0].subject}}` read from the payload.
*   `transform` can point to a JS/TS module returning a hook action.
    *   `transform.module` must be a relative path and stays within `hooks.transformsDir` (absolute paths and traversal are rejected).
*   `agentId` routes to a specific agent; unknown IDs fall back to default.
*   `allowedAgentIds`: restricts explicit routing (`*` or omitted = allow all, `[]` = deny all).
*   `defaultSessionKey`: optional fixed session key for hook agent runs without explicit `sessionKey`.
*   `allowRequestSessionKey`: allow `/hooks/agent` callers to set `sessionKey` (default: `false`).
*   `allowedSessionKeyPrefixes`: optional prefix allowlist for explicit `sessionKey` values (request + mapping), e.g. `["hook:"]`.
*   `deliver: true` sends final reply to a channel; `channel` defaults to `last`.
*   `model` overrides LLM for this hook run (must be allowed if model catalog is set).

### Gmail integration

```
{
  hooks: {
    gmail: {
      account: "openclaw@gmail.com",
      topic: "projects/<project-id>/topics/gog-gmail-watch",
      subscription: "gog-gmail-watch-push",
      pushToken: "shared-push-token",
      hookUrl: "http://127.0.0.1:18789/hooks/gmail",
      includeBody: true,
      maxBytes: 20000,
      renewEveryMinutes: 720,
      serve: { bind: "127.0.0.1", port: 8788, path: "/" },
      tailscale: { mode: "funnel", path: "/gmail-pubsub" },
      model: "openrouter/meta-llama/llama-3.3-70b-instruct:free",
      thinking: "off",
    },
  },
}
```

*   Gateway auto-starts `gog gmail watch serve` on boot when configured. Set `OPENCLAW_SKIP_GMAIL_WATCHER=1` to disable.
*   Don’t run a separate `gog gmail watch serve` alongside the Gateway.

* * *

## Canvas host

```
{
  canvasHost: {
    root: "~/.openclaw/workspace/canvas",
    liveReload: true,
    // enabled: false, // or OPENCLAW_SKIP_CANVAS_HOST=1
  },
}
```

*   Serves agent-editable HTML/CSS/JS and A2UI over HTTP under the Gateway port:
    *   `http://<gateway-host>:<gateway.port>/__openclaw__/canvas/`
    *   `http://<gateway-host>:<gateway.port>/__openclaw__/a2ui/`
*   Local-only: keep `gateway.bind: "loopback"` (default).
*   Non-loopback binds: canvas routes require Gateway auth (token/password/trusted-proxy), same as other Gateway HTTP surfaces.
*   Node WebViews typically don’t send auth headers; after a node is paired and connected, the Gateway advertises node-scoped capability URLs for canvas/A2UI access.
*   Capability URLs are bound to the active node WS session and expire quickly. IP-based fallback is not used.
*   Injects live-reload client into served HTML.
*   Auto-creates starter `index.html` when empty.
*   Also serves A2UI at `/__openclaw__/a2ui/`.
*   Changes require a gateway restart.
*   Disable live reload for large directories or `EMFILE` errors.

* * *

## Discovery

### mDNS (Bonjour)

```
{
  discovery: {
    mdns: {
      mode: "minimal", // minimal | full | off
    },
  },
}
```

*   `minimal` (default): omit `cliPath` + `sshPort` from TXT records.
*   `full`: include `cliPath` + `sshPort`.
*   Hostname defaults to `openclaw`. Override with `OPENCLAW_MDNS_HOSTNAME`.

### Wide-area (DNS-SD)

```
{
  discovery: {
    wideArea: { enabled: true },
  },
}
```

Writes a unicast DNS-SD zone under `~/.openclaw/dns/`. For cross-network discovery, pair with a DNS server (CoreDNS recommended) + Tailscale split DNS. Setup: `openclaw dns setup --apply`.

* * *

## Environment

### `env` (inline env vars)

```
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: {
      GROQ_API_KEY: "gsk-...",
    },
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

*   Inline env vars are only applied if the process env is missing the key.
*   `.env` files: CWD `.env` + `~/.openclaw/.env` (neither overrides existing vars).
*   `shellEnv`: imports missing expected keys from your login shell profile.
*   See [Environment](https://docs.openclaw.ai/help/environment) for full precedence.

### Env var substitution

Reference env vars in any config string with `${VAR_NAME}`:

```
{
  gateway: {
    auth: { token: "${OPENCLAW_GATEWAY_TOKEN}" },
  },
}
```

*   Only uppercase names matched: `[A-Z_][A-Z0-9_]*`.
*   Missing/empty vars throw an error at config load.
*   Escape with `$${VAR}` for a literal `${VAR}`.
*   Works with `$include`.

* * *

## Secrets

Secret refs are additive: plaintext values still work.

### `SecretRef`

Use one object shape:

```
{ source: "env" | "file" | "exec", provider: "default", id: "..." }
```

Validation:

*   `provider` pattern: `^[a-z][a-z0-9_-]{0,63}$`
*   `source: "env"` id pattern: `^[A-Z][A-Z0-9_]{0,127}$`
*   `source: "file"` id: absolute JSON pointer (for example `"/providers/openai/apiKey"`)
*   `source: "exec"` id pattern: `^[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}$`

### Supported credential surface

*   Canonical matrix: [SecretRef Credential Surface](https://docs.openclaw.ai/reference/secretref-credential-surface)
*   `secrets apply` targets supported `openclaw.json` credential paths.
*   `auth-profiles.json` refs are included in runtime resolution and audit coverage.

### Secret providers config

```
{
  secrets: {
    providers: {
      default: { source: "env" }, // optional explicit env provider
      filemain: {
        source: "file",
        path: "~/.openclaw/secrets.json",
        mode: "json",
        timeoutMs: 5000,
      },
      vault: {
        source: "exec",
        command: "/usr/local/bin/openclaw-vault-resolver",
        passEnv: ["PATH", "VAULT_ADDR"],
      },
    },
    defaults: {
      env: "default",
      file: "filemain",
      exec: "vault",
    },
  },
}
```

Notes:

*   `file` provider supports `mode: "json"` and `mode: "singleValue"` (`id` must be `"value"` in singleValue mode).
*   `exec` provider requires an absolute `command` path and uses protocol payloads on stdin/stdout.
*   By default, symlink command paths are rejected. Set `allowSymlinkCommand: true` to allow symlink paths while validating the resolved target path.
*   If `trustedDirs` is configured, the trusted-dir check applies to the resolved target path.
*   `exec` child environment is minimal by default; pass required variables explicitly with `passEnv`.
*   Secret refs are resolved at activation time into an in-memory snapshot, then request paths read the snapshot only.
*   Active-surface filtering applies during activation: unresolved refs on enabled surfaces fail startup/reload, while inactive surfaces are skipped with diagnostics.

* * *

## Auth storage

```
{
  auth: {
    profiles: {
      "anthropic:me@example.com": { provider: "anthropic", mode: "oauth", email: "me@example.com" },
      "anthropic:work": { provider: "anthropic", mode: "api_key" },
    },
    order: {
      anthropic: ["anthropic:me@example.com", "anthropic:work"],
    },
  },
}
```

*   Per-agent profiles are stored at `<agentDir>/auth-profiles.json`.
*   `auth-profiles.json` supports value-level refs (`keyRef` for `api_key`, `tokenRef` for `token`).
*   Static runtime credentials come from in-memory resolved snapshots; legacy static `auth.json` entries are scrubbed when discovered.
*   Legacy OAuth imports from `~/.openclaw/credentials/oauth.json`.
*   See [OAuth](https://docs.openclaw.ai/concepts/oauth).
*   Secrets runtime behavior and `audit/configure/apply` tooling: [Secrets Management](https://docs.openclaw.ai/gateway/secrets).

* * *

## Logging

```
{
  logging: {
    level: "info",
    file: "/tmp/openclaw/openclaw.log",
    consoleLevel: "info",
    consoleStyle: "pretty", // pretty | compact | json
    redactSensitive: "tools", // off | tools
    redactPatterns: ["\\bTOKEN\\b\\s*[=:]\\s*([\"']?)([^\\s\"']+)\\1"],
  },
}
```

*   Default log file: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`.
*   Set `logging.file` for a stable path.
*   `consoleLevel` bumps to `debug` when `--verbose`.

* * *

## CLI

```
{
  cli: {
    banner: {
      taglineMode: "off", // random | default | off
    },
  },
}
```

*   `cli.banner.taglineMode` controls banner tagline style:
    *   `"random"` (default): rotating funny/seasonal taglines.
    *   `"default"`: fixed neutral tagline (`All your chats, one OpenClaw.`).
    *   `"off"`: no tagline text (banner title/version still shown).
*   To hide the entire banner (not just taglines), set env `OPENCLAW_HIDE_BANNER=1`.

* * *

## Wizard

Metadata written by CLI wizards (`onboard`, `configure`, `doctor`):

```
{
  wizard: {
    lastRunAt: "2026-01-01T00:00:00.000Z",
    lastRunVersion: "2026.1.4",
    lastRunCommit: "abc1234",
    lastRunCommand: "configure",
    lastRunMode: "local",
  },
}
```

* * *

## Identity

```
{
  agents: {
    list: [
      {
        id: "main",
        identity: {
          name: "Samantha",
          theme: "helpful sloth",
          emoji: "🦥",
          avatar: "avatars/samantha.png",
        },
      },
    ],
  },
}
```

Written by the macOS onboarding assistant. Derives defaults:

*   `messages.ackReaction` from `identity.emoji` (falls back to 👀)
*   `mentionPatterns` from `identity.name`/`identity.emoji`
*   `avatar` accepts: workspace-relative path, `http(s)` URL, or `data:` URI

* * *

## Bridge (legacy, removed)

Current builds no longer include the TCP bridge. Nodes connect over the Gateway WebSocket. `bridge.*` keys are no longer part of the config schema (validation fails until removed; `openclaw doctor --fix` can strip unknown keys).

Legacy bridge config (historical reference)

```
{
  "bridge": {
    "enabled": true,
    "port": 18790,
    "bind": "tailnet",
    "tls": {
      "enabled": true,
      "autoGenerate": true
    }
  }
}
```

* * *

## Cron

```
{
  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
    webhook: "https://example.invalid/legacy", // deprecated fallback for stored notify:true jobs
    webhookToken: "replace-with-dedicated-token", // optional bearer token for outbound webhook auth
    sessionRetention: "24h", // duration string or false
    runLog: {
      maxBytes: "2mb", // default 2_000_000 bytes
      keepLines: 2000, // default 2000
    },
  },
}
```

*   `sessionRetention`: how long to keep completed isolated cron run sessions before pruning from `sessions.json`. Also controls cleanup of archived deleted cron transcripts. Default: `24h`; set `false` to disable.
*   `runLog.maxBytes`: max size per run log file (`cron/runs/<jobId>.jsonl`) before pruning. Default: `2_000_000` bytes.
*   `runLog.keepLines`: newest lines retained when run-log pruning is triggered. Default: `2000`.
*   `webhookToken`: bearer token used for cron webhook POST delivery (`delivery.mode = "webhook"`), if omitted no auth header is sent.
*   `webhook`: deprecated legacy fallback webhook URL (http/https) used only for stored jobs that still have `notify: true`.

See [Cron Jobs](https://docs.openclaw.ai/automation/cron-jobs).

* * *

Template placeholders expanded in `tools.media.models[].args`:

Variable

Description

`{{Body}}`

Full inbound message body

`{{RawBody}}`

Raw body (no history/sender wrappers)

`{{BodyStripped}}`

Body with group mentions stripped

`{{From}}`

Sender identifier

`{{To}}`

Destination identifier

`{{MessageSid}}`

Channel message id

`{{SessionId}}`

Current session UUID

`{{IsNewSession}}`

`"true"` when new session created

`{{MediaUrl}}`

Inbound media pseudo-URL

`{{MediaPath}}`

Local media path

`{{MediaType}}`

Media type (image/audio/document/…)

`{{Transcript}}`

Audio transcript

`{{Prompt}}`

Resolved media prompt for CLI entries

`{{MaxChars}}`

Resolved max output chars for CLI entries

`{{ChatType}}`

`"direct"` or `"group"`

`{{GroupSubject}}`

Group subject (best effort)

`{{GroupMembers}}`

Group members preview (best effort)

`{{SenderName}}`

Sender display name (best effort)

`{{SenderE164}}`

Sender phone number (best effort)

`{{Provider}}`

Provider hint (whatsapp, telegram, discord, etc.)

* * *

## Config includes (`$include`)

Split config into multiple files:

```
// ~/.openclaw/openclaw.json
{
  gateway: { port: 18789 },
  agents: { $include: "./agents.json5" },
  broadcast: {
    $include: ["./clients/mueller.json5", "./clients/schmidt.json5"],
  },
}
```

**Merge behavior:**

*   Single file: replaces the containing object.
*   Array of files: deep-merged in order (later overrides earlier).
*   Sibling keys: merged after includes (override included values).
*   Nested includes: up to 10 levels deep.
*   Paths: resolved relative to the including file, but must stay inside the top-level config directory (`dirname` of `openclaw.json`). Absolute/`../` forms are allowed only when they still resolve inside that boundary.
*   Errors: clear messages for missing files, parse errors, and circular includes.

* * *

_Related: [Configuration](https://docs.openclaw.ai/gateway/configuration) · [Configuration Examples](https://docs.openclaw.ai/gateway/configuration-examples) · [Doctor](https://docs.openclaw.ai/gateway/doctor)_

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/sandboxing -->

# Sandboxing - OpenClaw

OpenClaw can run **tools inside Docker containers** to reduce blast radius. This is **optional** and controlled by configuration (`agents.defaults.sandbox` or `agents.list[].sandbox`). If sandboxing is off, tools run on the host. The Gateway stays on the host; tool execution runs in an isolated sandbox when enabled. This is not a perfect security boundary, but it materially limits filesystem and process access when the model does something dumb.

## What gets sandboxed

*   Tool execution (`exec`, `read`, `write`, `edit`, `apply_patch`, `process`, etc.).
*   Optional sandboxed browser (`agents.defaults.sandbox.browser`).
    *   By default, the sandbox browser auto-starts (ensures CDP is reachable) when the browser tool needs it. Configure via `agents.defaults.sandbox.browser.autoStart` and `agents.defaults.sandbox.browser.autoStartTimeoutMs`.
    *   By default, sandbox browser containers use a dedicated Docker network (`openclaw-sandbox-browser`) instead of the global `bridge` network. Configure with `agents.defaults.sandbox.browser.network`.
    *   Optional `agents.defaults.sandbox.browser.cdpSourceRange` restricts container-edge CDP ingress with a CIDR allowlist (for example `172.21.0.1/32`).
    *   noVNC observer access is password-protected by default; OpenClaw emits a short-lived token URL that serves a local bootstrap page and opens noVNC with password in URL fragment (not query/header logs).
    *   `agents.defaults.sandbox.browser.allowHostControl` lets sandboxed sessions target the host browser explicitly.
    *   Optional allowlists gate `target: "custom"`: `allowedControlUrls`, `allowedControlHosts`, `allowedControlPorts`.

Not sandboxed:

*   The Gateway process itself.
*   Any tool explicitly allowed to run on the host (e.g. `tools.elevated`).
    *   **Elevated exec runs on the host and bypasses sandboxing.**
    *   If sandboxing is off, `tools.elevated` does not change execution (already on host). See [Elevated Mode](https://docs.openclaw.ai/tools/elevated).

## Modes

`agents.defaults.sandbox.mode` controls **when** sandboxing is used:

*   `"off"`: no sandboxing.
*   `"non-main"`: sandbox only **non-main** sessions (default if you want normal chats on host).
*   `"all"`: every session runs in a sandbox. Note: `"non-main"` is based on `session.mainKey` (default `"main"`), not agent id. Group/channel sessions use their own keys, so they count as non-main and will be sandboxed.

## Scope

`agents.defaults.sandbox.scope` controls **how many containers** are created:

*   `"session"` (default): one container per session.
*   `"agent"`: one container per agent.
*   `"shared"`: one container shared by all sandboxed sessions.

## Workspace access

`agents.defaults.sandbox.workspaceAccess` controls **what the sandbox can see**:

*   `"none"` (default): tools see a sandbox workspace under `~/.openclaw/sandboxes`.
*   `"ro"`: mounts the agent workspace read-only at `/agent` (disables `write`/`edit`/`apply_patch`).
*   `"rw"`: mounts the agent workspace read/write at `/workspace`.

Inbound media is copied into the active sandbox workspace (`media/inbound/*`). Skills note: the `read` tool is sandbox-rooted. With `workspaceAccess: "none"`, OpenClaw mirrors eligible skills into the sandbox workspace (`.../skills`) so they can be read. With `"rw"`, workspace skills are readable from `/workspace/skills`.

## Custom bind mounts

`agents.defaults.sandbox.docker.binds` mounts additional host directories into the container. Format: `host:container:mode` (e.g., `"/home/user/source:/source:rw"`). Global and per-agent binds are **merged** (not replaced). Under `scope: "shared"`, per-agent binds are ignored. `agents.defaults.sandbox.browser.binds` mounts additional host directories into the **sandbox browser** container only.

*   When set (including `[]`), it replaces `agents.defaults.sandbox.docker.binds` for the browser container.
*   When omitted, the browser container falls back to `agents.defaults.sandbox.docker.binds` (backwards compatible).

Example (read-only source + an extra data directory):

```
{
  agents: {
    defaults: {
      sandbox: {
        docker: {
          binds: ["/home/user/source:/source:ro", "/var/data/myapp:/data:ro"],
        },
      },
    },
    list: [
      {
        id: "build",
        sandbox: {
          docker: {
            binds: ["/mnt/cache:/cache:rw"],
          },
        },
      },
    ],
  },
}
```

Security notes:

*   Binds bypass the sandbox filesystem: they expose host paths with whatever mode you set (`:ro` or `:rw`).
*   OpenClaw blocks dangerous bind sources (for example: `docker.sock`, `/etc`, `/proc`, `/sys`, `/dev`, and parent mounts that would expose them).
*   Sensitive mounts (secrets, SSH keys, service credentials) should be `:ro` unless absolutely required.
*   Combine with `workspaceAccess: "ro"` if you only need read access to the workspace; bind modes stay independent.
*   See [Sandbox vs Tool Policy vs Elevated](https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated) for how binds interact with tool policy and elevated exec.

## Images + setup

Default image: `openclaw-sandbox:bookworm-slim` Build it once:

Note: the default image does **not** include Node. If a skill needs Node (or other runtimes), either bake a custom image or install via `sandbox.docker.setupCommand` (requires network egress + writable root + root user). If you want a more functional sandbox image with common tooling (for example `curl`, `jq`, `nodejs`, `python3`, `git`), build:

```
scripts/sandbox-common-setup.sh
```

Then set `agents.defaults.sandbox.docker.image` to `openclaw-sandbox-common:bookworm-slim`. Sandboxed browser image:

```
scripts/sandbox-browser-setup.sh
```

By default, sandbox containers run with **no network**. Override with `agents.defaults.sandbox.docker.network`. The bundled sandbox browser image also applies conservative Chromium startup defaults for containerized workloads. Current container defaults include:

*   `--remote-debugging-address=127.0.0.1`
*   `--remote-debugging-port=<derived from OPENCLAW_BROWSER_CDP_PORT>`
*   `--user-data-dir=${HOME}/.chrome`
*   `--no-first-run`
*   `--no-default-browser-check`
*   `--disable-3d-apis`
*   `--disable-gpu`
*   `--disable-dev-shm-usage`
*   `--disable-background-networking`
*   `--disable-extensions`
*   `--disable-features=TranslateUI`
*   `--disable-breakpad`
*   `--disable-crash-reporter`
*   `--disable-software-rasterizer`
*   `--no-zygote`
*   `--metrics-recording-only`
*   `--renderer-process-limit=2`
*   `--no-sandbox` and `--disable-setuid-sandbox` when `noSandbox` is enabled.
*   The three graphics hardening flags (`--disable-3d-apis`, `--disable-software-rasterizer`, `--disable-gpu`) are optional and are useful when containers lack GPU support. Set `OPENCLAW_BROWSER_DISABLE_GRAPHICS_FLAGS=0` if your workload requires WebGL or other 3D/browser features.
*   `--disable-extensions` is enabled by default and can be disabled with `OPENCLAW_BROWSER_DISABLE_EXTENSIONS=0` for extension-reliant flows.
*   `--renderer-process-limit=2` is controlled by `OPENCLAW_BROWSER_RENDERER_PROCESS_LIMIT=<N>`, where `0` keeps Chromium’s default.

If you need a different runtime profile, use a custom browser image and provide your own entrypoint. For local (non-container) Chromium profiles, use `browser.extraArgs` to append additional startup flags. Security defaults:

*   `network: "host"` is blocked.
*   `network: "container:<id>"` is blocked by default (namespace join bypass risk).
*   Break-glass override: `agents.defaults.sandbox.docker.dangerouslyAllowContainerNamespaceJoin: true`.

Docker installs and the containerized gateway live here: [Docker](https://docs.openclaw.ai/install/docker) For Docker gateway deployments, `docker-setup.sh` can bootstrap sandbox config. Set `OPENCLAW_SANDBOX=1` (or `true`/`yes`/`on`) to enable that path. You can override socket location with `OPENCLAW_DOCKER_SOCKET`. Full setup and env reference: [Docker](https://docs.openclaw.ai/install/docker#enable-agent-sandbox-for-docker-gateway-opt-in).

## setupCommand (one-time container setup)

`setupCommand` runs **once** after the sandbox container is created (not on every run). It executes inside the container via `sh -lc`. Paths:

*   Global: `agents.defaults.sandbox.docker.setupCommand`
*   Per-agent: `agents.list[].sandbox.docker.setupCommand`

Common pitfalls:

*   Default `docker.network` is `"none"` (no egress), so package installs will fail.
*   `docker.network: "container:<id>"` requires `dangerouslyAllowContainerNamespaceJoin: true` and is break-glass only.
*   `readOnlyRoot: true` prevents writes; set `readOnlyRoot: false` or bake a custom image.
*   `user` must be root for package installs (omit `user` or set `user: "0:0"`).
*   Sandbox exec does **not** inherit host `process.env`. Use `agents.defaults.sandbox.docker.env` (or a custom image) for skill API keys.

Tool allow/deny policies still apply before sandbox rules. If a tool is denied globally or per-agent, sandboxing doesn’t bring it back. `tools.elevated` is an explicit escape hatch that runs `exec` on the host. `/exec` directives only apply for authorized senders and persist per session; to hard-disable `exec`, use tool policy deny (see [Sandbox vs Tool Policy vs Elevated](https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated)). Debugging:

*   Use `openclaw sandbox explain` to inspect effective sandbox mode, tool policy, and fix-it config keys.
*   See [Sandbox vs Tool Policy vs Elevated](https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated) for the “why is this blocked?” mental model. Keep it locked down.

## Multi-agent overrides

Each agent can override sandbox + tools: `agents.list[].sandbox` and `agents.list[].tools` (plus `agents.list[].tools.sandbox.tools` for sandbox tool policy). See [Multi-Agent Sandbox & Tools](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools) for precedence.

## Minimal enable example

```
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        scope: "session",
        workspaceAccess: "none",
      },
    },
  },
}
```

*   [Sandbox Configuration](https://docs.openclaw.ai/gateway/configuration#agentsdefaults-sandbox)
*   [Multi-Agent Sandbox & Tools](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools)
*   [Security](https://docs.openclaw.ai/gateway/security)

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/protocol -->

# Gateway Protocol - OpenClaw

## Gateway protocol (WebSocket)

The Gateway WS protocol is the **single control plane + node transport** for OpenClaw. All clients (CLI, web UI, macOS app, iOS/Android nodes, headless nodes) connect over WebSocket and declare their **role** + **scope** at handshake time.

## Transport

*   WebSocket, text frames with JSON payloads.
*   First frame **must** be a `connect` request.

## Handshake (connect)

Gateway → Client (pre-connect challenge):

```
{
  "type": "event",
  "event": "connect.challenge",
  "payload": { "nonce": "…", "ts": 1737264000000 }
}
```

Client → Gateway:

```
{
  "type": "req",
  "id": "…",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 3,
    "client": {
      "id": "cli",
      "version": "1.2.3",
      "platform": "macos",
      "mode": "operator"
    },
    "role": "operator",
    "scopes": ["operator.read", "operator.write"],
    "caps": [],
    "commands": [],
    "permissions": {},
    "auth": { "token": "…" },
    "locale": "en-US",
    "userAgent": "openclaw-cli/1.2.3",
    "device": {
      "id": "device_fingerprint",
      "publicKey": "…",
      "signature": "…",
      "signedAt": 1737264000000,
      "nonce": "…"
    }
  }
}
```

Gateway → Client:

```
{
  "type": "res",
  "id": "…",
  "ok": true,
  "payload": { "type": "hello-ok", "protocol": 3, "policy": { "tickIntervalMs": 15000 } }
}
```

When a device token is issued, `hello-ok` also includes:

```
{
  "auth": {
    "deviceToken": "…",
    "role": "operator",
    "scopes": ["operator.read", "operator.write"]
  }
}
```

### Node example

```
{
  "type": "req",
  "id": "…",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 3,
    "client": {
      "id": "ios-node",
      "version": "1.2.3",
      "platform": "ios",
      "mode": "node"
    },
    "role": "node",
    "scopes": [],
    "caps": ["camera", "canvas", "screen", "location", "voice"],
    "commands": ["camera.snap", "canvas.navigate", "screen.record", "location.get"],
    "permissions": { "camera.capture": true, "screen.record": false },
    "auth": { "token": "…" },
    "locale": "en-US",
    "userAgent": "openclaw-ios/1.2.3",
    "device": {
      "id": "device_fingerprint",
      "publicKey": "…",
      "signature": "…",
      "signedAt": 1737264000000,
      "nonce": "…"
    }
  }
}
```

## Framing

*   **Request**: `{type:"req", id, method, params}`
*   **Response**: `{type:"res", id, ok, payload|error}`
*   **Event**: `{type:"event", event, payload, seq?, stateVersion?}`

Side-effecting methods require **idempotency keys** (see schema).

## Roles + scopes

### Roles

*   `operator` = control plane client (CLI/UI/automation).
*   `node` = capability host (camera/screen/canvas/system.run).

### Scopes (operator)

Common scopes:

*   `operator.read`
*   `operator.write`
*   `operator.admin`
*   `operator.approvals`
*   `operator.pairing`

Method scope is only the first gate. Some slash commands reached through `chat.send` apply stricter command-level checks on top. For example, persistent `/config set` and `/config unset` writes require `operator.admin`.

### Caps/commands/permissions (node)

Nodes declare capability claims at connect time:

*   `caps`: high-level capability categories.
*   `commands`: command allowlist for invoke.
*   `permissions`: granular toggles (e.g. `screen.record`, `camera.capture`).

The Gateway treats these as **claims** and enforces server-side allowlists.

## Presence

*   `system-presence` returns entries keyed by device identity.
*   Presence entries include `deviceId`, `roles`, and `scopes` so UIs can show a single row per device even when it connects as both **operator** and **node**.

### Node helper methods

*   Nodes may call `skills.bins` to fetch the current list of skill executables for auto-allow checks.

### Operator helper methods

*   Operators may call `tools.catalog` (`operator.read`) to fetch the runtime tool catalog for an agent. The response includes grouped tools and provenance metadata:
    *   `source`: `core` or `plugin`
    *   `pluginId`: plugin owner when `source="plugin"`
    *   `optional`: whether a plugin tool is optional

## Exec approvals

*   When an exec request needs approval, the gateway broadcasts `exec.approval.requested`.
*   Operator clients resolve by calling `exec.approval.resolve` (requires `operator.approvals` scope).
*   For `host=node`, `exec.approval.request` must include `systemRunPlan` (canonical `argv`/`cwd`/`rawCommand`/session metadata). Requests missing `systemRunPlan` are rejected.

## Versioning

*   `PROTOCOL_VERSION` lives in `src/gateway/protocol/schema.ts`.
*   Clients send `minProtocol` + `maxProtocol`; the server rejects mismatches.
*   Schemas + models are generated from TypeBox definitions:
    *   `pnpm protocol:gen`
    *   `pnpm protocol:gen:swift`
    *   `pnpm protocol:check`

## Auth

*   If `OPENCLAW_GATEWAY_TOKEN` (or `--token`) is set, `connect.params.auth.token` must match or the socket is closed.
*   After pairing, the Gateway issues a **device token** scoped to the connection role + scopes. It is returned in `hello-ok.auth.deviceToken` and should be persisted by the client for future connects.
*   Device tokens can be rotated/revoked via `device.token.rotate` and `device.token.revoke` (requires `operator.pairing` scope).

## Device identity + pairing

*   Nodes should include a stable device identity (`device.id`) derived from a keypair fingerprint.
*   Gateways issue tokens per device + role.
*   Pairing approvals are required for new device IDs unless local auto-approval is enabled.
*   **Local** connects include loopback and the gateway host’s own tailnet address (so same‑host tailnet binds can still auto‑approve).
*   All WS clients must include `device` identity during `connect` (operator + node). Control UI can omit it **only** when `gateway.controlUi.dangerouslyDisableDeviceAuth` is enabled for break-glass use.
*   All connections must sign the server-provided `connect.challenge` nonce.

### Device auth migration diagnostics

For legacy clients that still use pre-challenge signing behavior, `connect` now returns `DEVICE_AUTH_*` detail codes under `error.details.code` with a stable `error.details.reason`. Common migration failures:

| Message | details.code | details.reason | Meaning |
| --- | --- | --- | --- |
| `device nonce required` | `DEVICE_AUTH_NONCE_REQUIRED` | `device-nonce-missing` | Client omitted `device.nonce` (or sent blank). |
| `device nonce mismatch` | `DEVICE_AUTH_NONCE_MISMATCH` | `device-nonce-mismatch` | Client signed with a stale/wrong nonce. |
| `device signature invalid` | `DEVICE_AUTH_SIGNATURE_INVALID` | `device-signature` | Signature payload does not match v2 payload. |
| `device signature expired` | `DEVICE_AUTH_SIGNATURE_EXPIRED` | `device-signature-stale` | Signed timestamp is outside allowed skew. |
| `device identity mismatch` | `DEVICE_AUTH_DEVICE_ID_MISMATCH` | `device-id-mismatch` | `device.id` does not match public key fingerprint. |
| `device public key invalid` | `DEVICE_AUTH_PUBLIC_KEY_INVALID` | `device-public-key` | Public key format/canonicalization failed. |

Migration target:

*   Always wait for `connect.challenge`.
*   Sign the v2 payload that includes the server nonce.
*   Send the same nonce in `connect.params.device.nonce`.
*   Preferred signature payload is `v3`, which binds `platform` and `deviceFamily` in addition to device/client/role/scopes/token/nonce fields.
*   Legacy `v2` signatures remain accepted for compatibility, but paired-device metadata pinning still controls command policy on reconnect.

## TLS + pinning

*   TLS is supported for WS connections.
*   Clients may optionally pin the gateway cert fingerprint (see `gateway.tls` config plus `gateway.remote.tlsFingerprint` or CLI `--tls-fingerprint`).

## Scope

This protocol exposes the **full gateway API** (status, channels, models, chat, agent, sessions, nodes, approvals, etc.). The exact surface is defined by the TypeBox schemas in `src/gateway/protocol/schema.ts`.

---

<!-- SOURCE: https://docs.openclaw.ai/auth-credential-semantics -->

# Auth credential semantics - OpenClaw

This document defines the canonical credential eligibility and resolution semantics used across:

*   `resolveAuthProfileOrder`
*   `resolveApiKeyForProfile`
*   `models status --probe`
*   `doctor-auth`

The goal is to keep selection-time and runtime behavior aligned.

## Stable Reason Codes

*   `ok`
*   `missing_credential`
*   `invalid_expires`
*   `expired`
*   `unresolved_ref`

## Token Credentials

Token credentials (`type: "token"`) support inline `token` and/or `tokenRef`.

### Eligibility rules

1.  A token profile is ineligible when both `token` and `tokenRef` are absent.
2.  `expires` is optional.
3.  If `expires` is present, it must be a finite number greater than `0`.
4.  If `expires` is invalid (`NaN`, `0`, negative, non-finite, or wrong type), the profile is ineligible with `invalid_expires`.
5.  If `expires` is in the past, the profile is ineligible with `expired`.
6.  `tokenRef` does not bypass `expires` validation.

### Resolution rules

1.  Resolver semantics match eligibility semantics for `expires`.
2.  For eligible profiles, token material may be resolved from inline value or `tokenRef`.
3.  Unresolvable refs produce `unresolved_ref` in `models status --probe` output.

## Legacy-Compatible Messaging

For script compatibility, probe errors keep this first line unchanged: `Auth profile credentials are missing or expired.` Human-friendly detail and stable reason codes may be added on subsequent lines.

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/authentication -->

# Authentication - OpenClaw

OpenClaw supports OAuth and API keys for model providers. For always-on gateway hosts, API keys are usually the most predictable option. Subscription/OAuth flows are also supported when they match your provider account model. See [/concepts/oauth](https://docs.openclaw.ai/concepts/oauth) for the full OAuth flow and storage layout. For SecretRef-based auth (`env`/`file`/`exec` providers), see [Secrets Management](https://docs.openclaw.ai/gateway/secrets). For credential eligibility/reason-code rules used by `models status --probe`, see [Auth Credential Semantics](https://docs.openclaw.ai/auth-credential-semantics).

## Recommended setup (API key, any provider)

If you’re running a long-lived gateway, start with an API key for your chosen provider. For Anthropic specifically, API key auth is the safe path and is recommended over subscription setup-token auth.

1.  Create an API key in your provider console.
2.  Put it on the **gateway host** (the machine running `openclaw gateway`).

```
export <PROVIDER>_API_KEY="..."
openclaw models status
```

3.  If the Gateway runs under systemd/launchd, prefer putting the key in `~/.openclaw/.env` so the daemon can read it:

```
cat >> ~/.openclaw/.env <<'EOF'
<PROVIDER>_API_KEY=...
EOF
```

Then restart the daemon (or restart your Gateway process) and re-check:

```
openclaw models status
openclaw doctor
```

If you’d rather not manage env vars yourself, the onboarding wizard can store API keys for daemon use: `openclaw onboard`. See [Help](https://docs.openclaw.ai/help) for details on env inheritance (`env.shellEnv`, `~/.openclaw/.env`, systemd/launchd).

## Anthropic: setup-token (subscription auth)

If you’re using a Claude subscription, the setup-token flow is supported. Run it on the **gateway host**:

Then paste it into OpenClaw:

```
openclaw models auth setup-token --provider anthropic
```

If the token was created on another machine, paste it manually:

```
openclaw models auth paste-token --provider anthropic
```

If you see an Anthropic error like:

```
This credential is only authorized for use with Claude Code and cannot be used for other API requests.
```

…use an Anthropic API key instead.

Manual token entry (any provider; writes `auth-profiles.json` + updates config):

```
openclaw models auth paste-token --provider anthropic
openclaw models auth paste-token --provider openrouter
```

Auth profile refs are also supported for static credentials:

*   `api_key` credentials can use `keyRef: { source, provider, id }`
*   `token` credentials can use `tokenRef: { source, provider, id }`

Automation-friendly check (exit `1` when expired/missing, `2` when expiring):

```
openclaw models status --check
```

Optional ops scripts (systemd/Termux) are documented here: [/automation/auth-monitoring](https://docs.openclaw.ai/automation/auth-monitoring)

> `claude setup-token` requires an interactive TTY.

## Checking model auth status

```
openclaw models status
openclaw doctor
```

## API key rotation behavior (gateway)

Some providers support retrying a request with alternative keys when an API call hits a provider rate limit.

*   Priority order:
    *   `OPENCLAW_LIVE_<PROVIDER>_KEY` (single override)
    *   `<PROVIDER>_API_KEYS`
    *   `<PROVIDER>_API_KEY`
    *   `<PROVIDER>_API_KEY_*`
*   Google providers also include `GOOGLE_API_KEY` as an additional fallback.
*   The same key list is deduplicated before use.
*   OpenClaw retries with the next key only for rate-limit errors (for example `429`, `rate_limit`, `quota`, `resource exhausted`).
*   Non-rate-limit errors are not retried with alternate keys.
*   If all keys fail, the final error from the last attempt is returned.

## Controlling which credential is used

### Per-session (chat command)

Use `/model <alias-or-id>@<profileId>` to pin a specific provider credential for the current session (example profile ids: `anthropic:default`, `anthropic:work`). Use `/model` (or `/model list`) for a compact picker; use `/model status` for the full view (candidates + next auth profile, plus provider endpoint details when configured).

### Per-agent (CLI override)

Set an explicit auth profile order override for an agent (stored in that agent’s `auth-profiles.json`):

```
openclaw models auth order get --provider anthropic
openclaw models auth order set --provider anthropic anthropic:default
openclaw models auth order clear --provider anthropic
```

Use `--agent <id>` to target a specific agent; omit it to use the configured default agent.

## Troubleshooting

### “No credentials found”

If the Anthropic token profile is missing, run `claude setup-token` on the **gateway host**, then re-check:

### Token expiring/expired

Run `openclaw models status` to confirm which profile is expiring. If the profile is missing, rerun `claude setup-token` and paste the token again.

## Requirements

*   Anthropic subscription account (for `claude setup-token`)
*   Claude Code CLI installed (`claude` command available)

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/secrets -->

# Secrets Management - OpenClaw

OpenClaw supports additive SecretRefs so supported credentials do not need to be stored as plaintext in configuration. Plaintext still works. SecretRefs are opt-in per credential.

## Goals and runtime model

Secrets are resolved into an in-memory runtime snapshot.

*   Resolution is eager during activation, not lazy on request paths.
*   Startup fails fast when an effectively active SecretRef cannot be resolved.
*   Reload uses atomic swap: full success, or keep the last-known-good snapshot.
*   Runtime requests read from the active in-memory snapshot only.

This keeps secret-provider outages off hot request paths.

## Active-surface filtering

SecretRefs are validated only on effectively active surfaces.

*   Enabled surfaces: unresolved refs block startup/reload.
*   Inactive surfaces: unresolved refs do not block startup/reload.
*   Inactive refs emit non-fatal diagnostics with code `SECRETS_REF_IGNORED_INACTIVE_SURFACE`.

Examples of inactive surfaces:

*   Disabled channel/account entries.
*   Top-level channel credentials that no enabled account inherits.
*   Disabled tool/feature surfaces.
*   Web search provider-specific keys that are not selected by `tools.web.search.provider`. In auto mode (provider unset), provider-specific keys are also active for provider auto-detection.
*   `gateway.remote.token` / `gateway.remote.password` SecretRefs are active (when `gateway.remote.enabled` is not `false`) if one of these is true:
    *   `gateway.mode=remote`
    *   `gateway.remote.url` is configured
    *   `gateway.tailscale.mode` is `serve` or `funnel` In local mode without those remote surfaces:
    *   `gateway.remote.token` is active when token auth can win and no env/auth token is configured.
    *   `gateway.remote.password` is active only when password auth can win and no env/auth password is configured.
*   `gateway.auth.token` SecretRef is inactive for startup auth resolution when `OPENCLAW_GATEWAY_TOKEN` (or `CLAWDBOT_GATEWAY_TOKEN`) is set, because env token input wins for that runtime.

## Gateway auth surface diagnostics

When a SecretRef is configured on `gateway.auth.token`, `gateway.auth.password`, `gateway.remote.token`, or `gateway.remote.password`, gateway startup/reload logs the surface state explicitly:

*   `active`: the SecretRef is part of the effective auth surface and must resolve.
*   `inactive`: the SecretRef is ignored for this runtime because another auth surface wins, or because remote auth is disabled/not active.

These entries are logged with `SECRETS_GATEWAY_AUTH_SURFACE` and include the reason used by the active-surface policy, so you can see why a credential was treated as active or inactive.

## Onboarding reference preflight

When onboarding runs in interactive mode and you choose SecretRef storage, OpenClaw runs preflight validation before saving:

*   Env refs: validates env var name and confirms a non-empty value is visible during onboarding.
*   Provider refs (`file` or `exec`): validates provider selection, resolves `id`, and checks resolved value type.
*   Quickstart reuse path: when `gateway.auth.token` is already a SecretRef, onboarding resolves it before probe/dashboard bootstrap (for `env`, `file`, and `exec` refs) using the same fail-fast gate.

If validation fails, onboarding shows the error and lets you retry.

## SecretRef contract

Use one object shape everywhere:

```
{ source: "env" | "file" | "exec", provider: "default", id: "..." }
```

### `source: "env"`

```
{ source: "env", provider: "default", id: "OPENAI_API_KEY" }
```

Validation:

*   `provider` must match `^[a-z][a-z0-9_-]{0,63}$`
*   `id` must match `^[A-Z][A-Z0-9_]{0,127}$`

### `source: "file"`

```
{ source: "file", provider: "filemain", id: "/providers/openai/apiKey" }
```

Validation:

*   `provider` must match `^[a-z][a-z0-9_-]{0,63}$`
*   `id` must be an absolute JSON pointer (`/...`)
*   RFC6901 escaping in segments: `~` => `~0`, `/` => `~1`

### `source: "exec"`

```
{ source: "exec", provider: "vault", id: "providers/openai/apiKey" }
```

Validation:

*   `provider` must match `^[a-z][a-z0-9_-]{0,63}$`
*   `id` must match `^[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}$`

## Provider config

Define providers under `secrets.providers`:

```
{
  secrets: {
    providers: {
      default: { source: "env" },
      filemain: {
        source: "file",
        path: "~/.openclaw/secrets.json",
        mode: "json", // or "singleValue"
      },
      vault: {
        source: "exec",
        command: "/usr/local/bin/openclaw-vault-resolver",
        args: ["--profile", "prod"],
        passEnv: ["PATH", "VAULT_ADDR"],
        jsonOnly: true,
      },
    },
    defaults: {
      env: "default",
      file: "filemain",
      exec: "vault",
    },
    resolution: {
      maxProviderConcurrency: 4,
      maxRefsPerProvider: 512,
      maxBatchBytes: 262144,
    },
  },
}
```

### Env provider

*   Optional allowlist via `allowlist`.
*   Missing/empty env values fail resolution.

### File provider

*   Reads local file from `path`.
*   `mode: "json"` expects JSON object payload and resolves `id` as pointer.
*   `mode: "singleValue"` expects ref id `"value"` and returns file contents.
*   Path must pass ownership/permission checks.
*   Windows fail-closed note: if ACL verification is unavailable for a path, resolution fails. For trusted paths only, set `allowInsecurePath: true` on that provider to bypass path security checks.

### Exec provider

*   Runs configured absolute binary path, no shell.
*   By default, `command` must point to a regular file (not a symlink).
*   Set `allowSymlinkCommand: true` to allow symlink command paths (for example Homebrew shims). OpenClaw validates the resolved target path.
*   Pair `allowSymlinkCommand` with `trustedDirs` for package-manager paths (for example `["/opt/homebrew"]`).
*   Supports timeout, no-output timeout, output byte limits, env allowlist, and trusted dirs.
*   Windows fail-closed note: if ACL verification is unavailable for the command path, resolution fails. For trusted paths only, set `allowInsecurePath: true` on that provider to bypass path security checks.

Request payload (stdin):

```
{ "protocolVersion": 1, "provider": "vault", "ids": ["providers/openai/apiKey"] }
```

Response payload (stdout):

```
{ "protocolVersion": 1, "values": { "providers/openai/apiKey": "<openai-api-key>" } } // pragma: allowlist secret
```

Optional per-id errors:

```
{
  "protocolVersion": 1,
  "values": {},
  "errors": { "providers/openai/apiKey": { "message": "not found" } }
}
```

## Exec integration examples

### 1Password CLI

```
{
  secrets: {
    providers: {
      onepassword_openai: {
        source: "exec",
        command: "/opt/homebrew/bin/op",
        allowSymlinkCommand: true, // required for Homebrew symlinked binaries
        trustedDirs: ["/opt/homebrew"],
        args: ["read", "op://Personal/OpenClaw QA API Key/password"],
        passEnv: ["HOME"],
        jsonOnly: false,
      },
    },
  },
  models: {
    providers: {
      openai: {
        baseUrl: "https://api.openai.com/v1",
        models: [{ id: "gpt-5", name: "gpt-5" }],
        apiKey: { source: "exec", provider: "onepassword_openai", id: "value" },
      },
    },
  },
}
```

### HashiCorp Vault CLI

```
{
  secrets: {
    providers: {
      vault_openai: {
        source: "exec",
        command: "/opt/homebrew/bin/vault",
        allowSymlinkCommand: true, // required for Homebrew symlinked binaries
        trustedDirs: ["/opt/homebrew"],
        args: ["kv", "get", "-field=OPENAI_API_KEY", "secret/openclaw"],
        passEnv: ["VAULT_ADDR", "VAULT_TOKEN"],
        jsonOnly: false,
      },
    },
  },
  models: {
    providers: {
      openai: {
        baseUrl: "https://api.openai.com/v1",
        models: [{ id: "gpt-5", name: "gpt-5" }],
        apiKey: { source: "exec", provider: "vault_openai", id: "value" },
      },
    },
  },
}
```

### `sops`

```
{
  secrets: {
    providers: {
      sops_openai: {
        source: "exec",
        command: "/opt/homebrew/bin/sops",
        allowSymlinkCommand: true, // required for Homebrew symlinked binaries
        trustedDirs: ["/opt/homebrew"],
        args: ["-d", "--extract", '["providers"]["openai"]["apiKey"]', "/path/to/secrets.enc.json"],
        passEnv: ["SOPS_AGE_KEY_FILE"],
        jsonOnly: false,
      },
    },
  },
  models: {
    providers: {
      openai: {
        baseUrl: "https://api.openai.com/v1",
        models: [{ id: "gpt-5", name: "gpt-5" }],
        apiKey: { source: "exec", provider: "sops_openai", id: "value" },
      },
    },
  },
}
```

## Supported credential surface

Canonical supported and unsupported credentials are listed in:

*   [SecretRef Credential Surface](https://docs.openclaw.ai/reference/secretref-credential-surface)

Runtime-minted or rotating credentials and OAuth refresh material are intentionally excluded from read-only SecretRef resolution.

## Required behavior and precedence

*   Field without a ref: unchanged.
*   Field with a ref: required on active surfaces during activation.
*   If both plaintext and ref are present, ref takes precedence on supported precedence paths.

Warning and audit signals:

*   `SECRETS_REF_OVERRIDES_PLAINTEXT` (runtime warning)
*   `REF_SHADOWED` (audit finding when `auth-profiles.json` credentials take precedence over `openclaw.json` refs)

Google Chat compatibility behavior:

*   `serviceAccountRef` takes precedence over plaintext `serviceAccount`.
*   Plaintext value is ignored when sibling ref is set.

## Activation triggers

Secret activation runs on:

*   Startup (preflight plus final activation)
*   Config reload hot-apply path
*   Config reload restart-check path
*   Manual reload via `secrets.reload`

Activation contract:

*   Success swaps the snapshot atomically.
*   Startup failure aborts gateway startup.
*   Runtime reload failure keeps the last-known-good snapshot.

## Degraded and recovered signals

When reload-time activation fails after a healthy state, OpenClaw enters degraded secrets state. One-shot system event and log codes:

*   `SECRETS_RELOADER_DEGRADED`
*   `SECRETS_RELOADER_RECOVERED`

Behavior:

*   Degraded: runtime keeps last-known-good snapshot.
*   Recovered: emitted once after the next successful activation.
*   Repeated failures while already degraded log warnings but do not spam events.
*   Startup fail-fast does not emit degraded events because runtime never became active.

## Command-path resolution

Command paths can opt into supported SecretRef resolution via gateway snapshot RPC. There are two broad behaviors:

*   Strict command paths (for example `openclaw memory` remote-memory paths and `openclaw qr --remote`) read from the active snapshot and fail fast when a required SecretRef is unavailable.
*   Read-only command paths (for example `openclaw status`, `openclaw status --all`, `openclaw channels status`, `openclaw channels resolve`, and read-only doctor/config repair flows) also prefer the active snapshot, but degrade instead of aborting when a targeted SecretRef is unavailable in that command path.

Read-only behavior:

*   When the gateway is running, these commands read from the active snapshot first.
*   If gateway resolution is incomplete or the gateway is unavailable, they attempt targeted local fallback for the specific command surface.
*   If a targeted SecretRef is still unavailable, the command continues with degraded read-only output and explicit diagnostics such as “configured but unavailable in this command path”.
*   This degraded behavior is command-local only. It does not weaken runtime startup, reload, or send/auth paths.

Other notes:

*   Snapshot refresh after backend secret rotation is handled by `openclaw secrets reload`.
*   Gateway RPC method used by these command paths: `secrets.resolve`.

## Audit and configure workflow

Default operator flow:

```
openclaw secrets audit --check
openclaw secrets configure
openclaw secrets audit --check
```

### `secrets audit`

Findings include:

*   plaintext values at rest (`openclaw.json`, `auth-profiles.json`, `.env`, and generated `agents/*/agent/models.json`)
*   plaintext sensitive provider header residues in generated `models.json` entries
*   unresolved refs
*   precedence shadowing (`auth-profiles.json` taking priority over `openclaw.json` refs)
*   legacy residues (`auth.json`, OAuth reminders)

Header residue note:

*   Sensitive provider header detection is name-heuristic based (common auth/credential header names and fragments such as `authorization`, `x-api-key`, `token`, `secret`, `password`, and `credential`).

### `secrets configure`

Interactive helper that:

*   configures `secrets.providers` first (`env`/`file`/`exec`, add/edit/remove)
*   lets you select supported secret-bearing fields in `openclaw.json` plus `auth-profiles.json` for one agent scope
*   can create a new `auth-profiles.json` mapping directly in the target picker
*   captures SecretRef details (`source`, `provider`, `id`)
*   runs preflight resolution
*   can apply immediately

Helpful modes:

*   `openclaw secrets configure --providers-only`
*   `openclaw secrets configure --skip-provider-setup`
*   `openclaw secrets configure --agent <id>`

`configure` apply defaults:

*   scrub matching static credentials from `auth-profiles.json` for targeted providers
*   scrub legacy static `api_key` entries from `auth.json`
*   scrub matching known secret lines from `<config-dir>/.env`

### `secrets apply`

Apply a saved plan:

```
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run
```

For strict target/path contract details and exact rejection rules, see:

*   [Secrets Apply Plan Contract](https://docs.openclaw.ai/gateway/secrets-plan-contract)

## One-way safety policy

OpenClaw intentionally does not write rollback backups containing historical plaintext secret values. Safety model:

*   preflight must succeed before write mode
*   runtime activation is validated before commit
*   apply updates files using atomic file replacement and best-effort restore on failure

## Legacy auth compatibility notes

For static credentials, runtime no longer depends on plaintext legacy auth storage.

*   Runtime credential source is the resolved in-memory snapshot.
*   Legacy static `api_key` entries are scrubbed when discovered.
*   OAuth-related compatibility behavior remains separate.

## Web UI note

Some SecretInput unions are easier to configure in raw editor mode than in form mode.

*   CLI commands: [secrets](https://docs.openclaw.ai/cli/secrets)
*   Plan contract details: [Secrets Apply Plan Contract](https://docs.openclaw.ai/gateway/secrets-plan-contract)
*   Credential surface: [SecretRef Credential Surface](https://docs.openclaw.ai/reference/secretref-credential-surface)
*   Auth setup: [Authentication](https://docs.openclaw.ai/gateway/authentication)
*   Security posture: [Security](https://docs.openclaw.ai/gateway/security)
*   Environment precedence: [Environment Variables](https://docs.openclaw.ai/help/environment)

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/secrets-plan-contract -->

# Secrets Apply Plan Contract - OpenClaw

This page defines the strict contract enforced by `openclaw secrets apply`. If a target does not match these rules, apply fails before mutating configuration.

## Plan file shape

`openclaw secrets apply --from <plan.json>` expects a `targets` array of plan targets:

```
{
  version: 1,
  protocolVersion: 1,
  targets: [
    {
      type: "models.providers.apiKey",
      path: "models.providers.openai.apiKey",
      pathSegments: ["models", "providers", "openai", "apiKey"],
      providerId: "openai",
      ref: { source: "env", provider: "default", id: "OPENAI_API_KEY" },
    },
    {
      type: "auth-profiles.api_key.key",
      path: "profiles.openai:default.key",
      pathSegments: ["profiles", "openai:default", "key"],
      agentId: "main",
      ref: { source: "env", provider: "default", id: "OPENAI_API_KEY" },
    },
  ],
}
```

## Supported target scope

Plan targets are accepted for supported credential paths in:

*   [SecretRef Credential Surface](https://docs.openclaw.ai/reference/secretref-credential-surface)

## Target type behavior

General rule:

*   `target.type` must be recognized and must match the normalized `target.path` shape.

Compatibility aliases remain accepted for existing plans:

*   `models.providers.apiKey`
*   `skills.entries.apiKey`
*   `channels.googlechat.serviceAccount`

## Path validation rules

Each target is validated with all of the following:

*   `type` must be a recognized target type.
*   `path` must be a non-empty dot path.
*   `pathSegments` can be omitted. If provided, it must normalize to exactly the same path as `path`.
*   Forbidden segments are rejected: `__proto__`, `prototype`, `constructor`.
*   The normalized path must match the registered path shape for the target type.
*   If `providerId` or `accountId` is set, it must match the id encoded in the path.
*   `auth-profiles.json` targets require `agentId`.
*   When creating a new `auth-profiles.json` mapping, include `authProfileProvider`.

## Failure behavior

If a target fails validation, apply exits with an error like:

```
Invalid plan target path for models.providers.apiKey: models.providers.openai.baseUrl
```

No writes are committed for an invalid plan.

## Runtime and audit scope notes

*   Ref-only `auth-profiles.json` entries (`keyRef`/`tokenRef`) are included in runtime resolution and audit coverage.
*   `secrets apply` writes supported `openclaw.json` targets, supported `auth-profiles.json` targets, and optional scrub targets.

## Operator checks

```
# Validate plan without writes
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run

# Then apply for real
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json
```

If apply fails with an invalid target path message, regenerate the plan with `openclaw secrets configure` or fix the target path to a supported shape above.

*   [Secrets Management](https://docs.openclaw.ai/gateway/secrets)
*   [CLI `secrets`](https://docs.openclaw.ai/cli/secrets)
*   [SecretRef Credential Surface](https://docs.openclaw.ai/reference/secretref-credential-surface)
*   [Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/health -->

# Health Checks - OpenClaw

Short guide to verify channel connectivity without guessing.

## Quick checks

*   `openclaw status` — local summary: gateway reachability/mode, update hint, linked channel auth age, sessions + recent activity.
*   `openclaw status --all` — full local diagnosis (read-only, color, safe to paste for debugging).
*   `openclaw status --deep` — also probes the running Gateway (per-channel probes when supported).
*   `openclaw health --json` — asks the running Gateway for a full health snapshot (WS-only; no direct Baileys socket).
*   Send `/status` as a standalone message in WhatsApp/WebChat to get a status reply without invoking the agent.
*   Logs: tail `/tmp/openclaw/openclaw-*.log` and filter for `web-heartbeat`, `web-reconnect`, `web-auto-reply`, `web-inbound`.

## Deep diagnostics

*   Creds on disk: `ls -l ~/.openclaw/credentials/whatsapp/<accountId>/creds.json` (mtime should be recent).
*   Session store: `ls -l ~/.openclaw/agents/<agentId>/sessions/sessions.json` (path can be overridden in config). Count and recent recipients are surfaced via `status`.
*   Relink flow: `openclaw channels logout && openclaw channels login --verbose` when status codes 409–515 or `loggedOut` appear in logs. (Note: the QR login flow auto-restarts once for status 515 after pairing.)

## When something fails

*   `logged out` or status 409–515 → relink with `openclaw channels logout` then `openclaw channels login`.
*   Gateway unreachable → start it: `openclaw gateway --port 18789` (use `--force` if the port is busy).
*   No inbound messages → confirm linked phone is online and the sender is allowed (`channels.whatsapp.allowFrom`); for group chats, ensure allowlist + mention rules match (`channels.whatsapp.groups`, `agents.list[].groupChat.mentionPatterns`).

## Dedicated “health” command

`openclaw health --json` asks the running Gateway for its health snapshot (no direct channel sockets from the CLI). It reports linked creds/auth age when available, per-channel probe summaries, session-store summary, and a probe duration. It exits non-zero if the Gateway is unreachable or the probe fails/timeouts. Use `--timeout <ms>` to override the 10s default.

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/heartbeat -->

# Heartbeat - OpenClaw

## Heartbeat (Gateway)

> **Heartbeat vs Cron?** See [Cron vs Heartbeat](https://docs.openclaw.ai/automation/cron-vs-heartbeat) for guidance on when to use each.

Heartbeat runs **periodic agent turns** in the main session so the model can surface anything that needs attention without spamming you. Troubleshooting: [/automation/troubleshooting](https://docs.openclaw.ai/automation/troubleshooting)

## Quick start (beginner)

1.  Leave heartbeats enabled (default is `30m`, or `1h` for Anthropic OAuth/setup-token) or set your own cadence.
2.  Create a tiny `HEARTBEAT.md` checklist in the agent workspace (optional but recommended).
3.  Decide where heartbeat messages should go (`target: "none"` is the default; set `target: "last"` to route to the last contact).
4.  Optional: enable heartbeat reasoning delivery for transparency.
5.  Optional: use lightweight bootstrap context if heartbeat runs only need `HEARTBEAT.md`.
6.  Optional: restrict heartbeats to active hours (local time).

Example config:

```
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last", // explicit delivery to last contact (default is "none")
        directPolicy: "allow", // default: allow direct/DM targets; set "block" to suppress
        lightContext: true, // optional: only inject HEARTBEAT.md from bootstrap files
        // activeHours: { start: "08:00", end: "24:00" },
        // includeReasoning: true, // optional: send separate `Reasoning:` message too
      },
    },
  },
}
```

## Defaults

*   Interval: `30m` (or `1h` when Anthropic OAuth/setup-token is the detected auth mode). Set `agents.defaults.heartbeat.every` or per-agent `agents.list[].heartbeat.every`; use `0m` to disable.
*   Prompt body (configurable via `agents.defaults.heartbeat.prompt`): `Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`
*   The heartbeat prompt is sent **verbatim** as the user message. The system prompt includes a “Heartbeat” section and the run is flagged internally.
*   Active hours (`heartbeat.activeHours`) are checked in the configured timezone. Outside the window, heartbeats are skipped until the next tick inside the window.

## What the heartbeat prompt is for

The default prompt is intentionally broad:

*   **Background tasks**: “Consider outstanding tasks” nudges the agent to review follow-ups (inbox, calendar, reminders, queued work) and surface anything urgent.
*   **Human check-in**: “Checkup sometimes on your human during day time” nudges an occasional lightweight “anything you need?” message, but avoids night-time spam by using your configured local timezone (see [/concepts/timezone](https://docs.openclaw.ai/concepts/timezone)).

If you want a heartbeat to do something very specific (e.g. “check Gmail PubSub stats” or “verify gateway health”), set `agents.defaults.heartbeat.prompt` (or `agents.list[].heartbeat.prompt`) to a custom body (sent verbatim).

## Response contract

*   If nothing needs attention, reply with **`HEARTBEAT_OK`**.
*   During heartbeat runs, OpenClaw treats `HEARTBEAT_OK` as an ack when it appears at the **start or end** of the reply. The token is stripped and the reply is dropped if the remaining content is **≤ `ackMaxChars`** (default: 300).
*   If `HEARTBEAT_OK` appears in the **middle** of a reply, it is not treated specially.
*   For alerts, **do not** include `HEARTBEAT_OK`; return only the alert text.

Outside heartbeats, stray `HEARTBEAT_OK` at the start/end of a message is stripped and logged; a message that is only `HEARTBEAT_OK` is dropped.

## Config

```
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m", // default: 30m (0m disables)
        model: "anthropic/claude-opus-4-6",
        includeReasoning: false, // default: false (deliver separate Reasoning: message when available)
        lightContext: false, // default: false; true keeps only HEARTBEAT.md from workspace bootstrap files
        target: "last", // default: none | options: last | none | <channel id> (core or plugin, e.g. "bluebubbles")
        to: "+15551234567", // optional channel-specific override
        accountId: "ops-bot", // optional multi-account channel id
        prompt: "Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.",
        ackMaxChars: 300, // max chars allowed after HEARTBEAT_OK
      },
    },
  },
}
```

### Scope and precedence

*   `agents.defaults.heartbeat` sets global heartbeat behavior.
*   `agents.list[].heartbeat` merges on top; if any agent has a `heartbeat` block, **only those agents** run heartbeats.
*   `channels.defaults.heartbeat` sets visibility defaults for all channels.
*   `channels.<channel>.heartbeat` overrides channel defaults.
*   `channels.<channel>.accounts.<id>.heartbeat` (multi-account channels) overrides per-channel settings.

### Per-agent heartbeats

If any `agents.list[]` entry includes a `heartbeat` block, **only those agents** run heartbeats. The per-agent block merges on top of `agents.defaults.heartbeat` (so you can set shared defaults once and override per agent). Example: two agents, only the second agent runs heartbeats.

```
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last", // explicit delivery to last contact (default is "none")
      },
    },
    list: [
      { id: "main", default: true },
      {
        id: "ops",
        heartbeat: {
          every: "1h",
          target: "whatsapp",
          to: "+15551234567",
          prompt: "Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.",
        },
      },
    ],
  },
}
```

### Active hours example

Restrict heartbeats to business hours in a specific timezone:

```
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last", // explicit delivery to last contact (default is "none")
        activeHours: {
          start: "09:00",
          end: "22:00",
          timezone: "America/New_York", // optional; uses your userTimezone if set, otherwise host tz
        },
      },
    },
  },
}
```

Outside this window (before 9am or after 10pm Eastern), heartbeats are skipped. The next scheduled tick inside the window will run normally.

### 24/7 setup

If you want heartbeats to run all day, use one of these patterns:

*   Omit `activeHours` entirely (no time-window restriction; this is the default behavior).
*   Set a full-day window: `activeHours: { start: "00:00", end: "24:00" }`.

Do not set the same `start` and `end` time (for example `08:00` to `08:00`). That is treated as a zero-width window, so heartbeats are always skipped.

### Multi account example

Use `accountId` to target a specific account on multi-account channels like Telegram:

```
{
  agents: {
    list: [
      {
        id: "ops",
        heartbeat: {
          every: "1h",
          target: "telegram",
          to: "12345678:topic:42", // optional: route to a specific topic/thread
          accountId: "ops-bot",
        },
      },
    ],
  },
  channels: {
    telegram: {
      accounts: {
        "ops-bot": { botToken: "YOUR_TELEGRAM_BOT_TOKEN" },
      },
    },
  },
}
```

### Field notes

*   `every`: heartbeat interval (duration string; default unit = minutes).
*   `model`: optional model override for heartbeat runs (`provider/model`).
*   `includeReasoning`: when enabled, also deliver the separate `Reasoning:` message when available (same shape as `/reasoning on`).
*   `lightContext`: when true, heartbeat runs use lightweight bootstrap context and keep only `HEARTBEAT.md` from workspace bootstrap files.
*   `session`: optional session key for heartbeat runs.
    *   `main` (default): agent main session.
    *   Explicit session key (copy from `openclaw sessions --json` or the [sessions CLI](https://docs.openclaw.ai/cli/sessions)).
    *   Session key formats: see [Sessions](https://docs.openclaw.ai/concepts/session) and [Groups](https://docs.openclaw.ai/channels/groups).
*   `target`:
    *   `last`: deliver to the last used external channel.
    *   explicit channel: `whatsapp` / `telegram` / `discord` / `googlechat` / `slack` / `msteams` / `signal` / `imessage`.
    *   `none` (default): run the heartbeat but **do not deliver** externally.
*   `directPolicy`: controls direct/DM delivery behavior:
    *   `allow` (default): allow direct/DM heartbeat delivery.
    *   `block`: suppress direct/DM delivery (`reason=dm-blocked`).
*   `to`: optional recipient override (channel-specific id, e.g. E.164 for WhatsApp or a Telegram chat id). For Telegram topics/threads, use `<chatId>:topic:<messageThreadId>`.
*   `accountId`: optional account id for multi-account channels. When `target: "last"`, the account id applies to the resolved last channel if it supports accounts; otherwise it is ignored. If the account id does not match a configured account for the resolved channel, delivery is skipped.
*   `prompt`: overrides the default prompt body (not merged).
*   `ackMaxChars`: max chars allowed after `HEARTBEAT_OK` before delivery.
*   `suppressToolErrorWarnings`: when true, suppresses tool error warning payloads during heartbeat runs.
*   `activeHours`: restricts heartbeat runs to a time window. Object with `start` (HH:MM, inclusive; use `00:00` for start-of-day), `end` (HH:MM exclusive; `24:00` allowed for end-of-day), and optional `timezone`.
    *   Omitted or `"user"`: uses your `agents.defaults.userTimezone` if set, otherwise falls back to the host system timezone.
    *   `"local"`: always uses the host system timezone.
    *   Any IANA identifier (e.g. `America/New_York`): used directly; if invalid, falls back to the `"user"` behavior above.
    *   `start` and `end` must not be equal for an active window; equal values are treated as zero-width (always outside the window).
    *   Outside the active window, heartbeats are skipped until the next tick inside the window.

## Delivery behavior

*   Heartbeats run in the agent’s main session by default (`agent:<id>:<mainKey>`), or `global` when `session.scope = "global"`. Set `session` to override to a specific channel session (Discord/WhatsApp/etc.).
*   `session` only affects the run context; delivery is controlled by `target` and `to`.
*   To deliver to a specific channel/recipient, set `target` + `to`. With `target: "last"`, delivery uses the last external channel for that session.
*   Heartbeat deliveries allow direct/DM targets by default. Set `directPolicy: "block"` to suppress direct-target sends while still running the heartbeat turn.
*   If the main queue is busy, the heartbeat is skipped and retried later.
*   If `target` resolves to no external destination, the run still happens but no outbound message is sent.
*   Heartbeat-only replies do **not** keep the session alive; the last `updatedAt` is restored so idle expiry behaves normally.

## Visibility controls

By default, `HEARTBEAT_OK` acknowledgments are suppressed while alert content is delivered. You can adjust this per channel or per account:

```
channels:
  defaults:
    heartbeat:
      showOk: false # Hide HEARTBEAT_OK (default)
      showAlerts: true # Show alert messages (default)
      useIndicator: true # Emit indicator events (default)
  telegram:
    heartbeat:
      showOk: true # Show OK acknowledgments on Telegram
  whatsapp:
    accounts:
      work:
        heartbeat:
          showAlerts: false # Suppress alert delivery for this account
```

Precedence: per-account → per-channel → channel defaults → built-in defaults.

### What each flag does

*   `showOk`: sends a `HEARTBEAT_OK` acknowledgment when the model returns an OK-only reply.
*   `showAlerts`: sends the alert content when the model returns a non-OK reply.
*   `useIndicator`: emits indicator events for UI status surfaces.

If **all three** are false, OpenClaw skips the heartbeat run entirely (no model call).

### Per-channel vs per-account examples

```
channels:
  defaults:
    heartbeat:
      showOk: false
      showAlerts: true
      useIndicator: true
  slack:
    heartbeat:
      showOk: true # all Slack accounts
    accounts:
      ops:
        heartbeat:
          showAlerts: false # suppress alerts for the ops account only
  telegram:
    heartbeat:
      showOk: true
```

### Common patterns

| Goal | Config |
| --- | --- |
| Default behavior (silent OKs, alerts on) | _(no config needed)_ |
| Fully silent (no messages, no indicator) | `channels.defaults.heartbeat: { showOk: false, showAlerts: false, useIndicator: false }` |
| Indicator-only (no messages) | `channels.defaults.heartbeat: { showOk: false, showAlerts: false, useIndicator: true }` |
| OKs in one channel only | `channels.telegram.heartbeat: { showOk: true }` |

## HEARTBEAT.md (optional)

If a `HEARTBEAT.md` file exists in the workspace, the default prompt tells the agent to read it. Think of it as your “heartbeat checklist”: small, stable, and safe to include every 30 minutes. If `HEARTBEAT.md` exists but is effectively empty (only blank lines and markdown headers like `# Heading`), OpenClaw skips the heartbeat run to save API calls. If the file is missing, the heartbeat still runs and the model decides what to do. Keep it tiny (short checklist or reminders) to avoid prompt bloat. Example `HEARTBEAT.md`:

```
# Heartbeat checklist

- Quick scan: anything urgent in inboxes?
- If it’s daytime, do a lightweight check-in if nothing else is pending.
- If a task is blocked, write down _what is missing_ and ask Peter next time.
```

### Can the agent update HEARTBEAT.md?

Yes — if you ask it to. `HEARTBEAT.md` is just a normal file in the agent workspace, so you can tell the agent (in a normal chat) something like:

*   “Update `HEARTBEAT.md` to add a daily calendar check.”
*   “Rewrite `HEARTBEAT.md` so it’s shorter and focused on inbox follow-ups.”

If you want this to happen proactively, you can also include an explicit line in your heartbeat prompt like: “If the checklist becomes stale, update HEARTBEAT.md with a better one.” Safety note: don’t put secrets (API keys, phone numbers, private tokens) into `HEARTBEAT.md` — it becomes part of the prompt context.

## Manual wake (on-demand)

You can enqueue a system event and trigger an immediate heartbeat with:

```
openclaw system event --text "Check for urgent follow-ups" --mode now
```

If multiple agents have `heartbeat` configured, a manual wake runs each of those agent heartbeats immediately. Use `--mode next-heartbeat` to wait for the next scheduled tick.

## Reasoning delivery (optional)

By default, heartbeats deliver only the final “answer” payload. If you want transparency, enable:

*   `agents.defaults.heartbeat.includeReasoning: true`

When enabled, heartbeats will also deliver a separate message prefixed `Reasoning:` (same shape as `/reasoning on`). This can be useful when the agent is managing multiple sessions/codexes and you want to see why it decided to ping you — but it can also leak more internal detail than you want. Prefer keeping it off in group chats.

## Cost awareness

Heartbeats run full agent turns. Shorter intervals burn more tokens. Keep `HEARTBEAT.md` small and consider a cheaper `model` or `target: "none"` if you only want internal state updates.

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/trusted-proxy-auth -->

# Trusted proxy auth - OpenClaw

> ⚠️ **Security-sensitive feature.** This mode delegates authentication entirely to your reverse proxy. Misconfiguration can expose your Gateway to unauthorized access. Read this page carefully before enabling.

## When to Use

Use `trusted-proxy` auth mode when:

*   You run OpenClaw behind an **identity-aware proxy** (Pomerium, Caddy + OAuth, nginx + oauth2-proxy, Traefik + forward auth)
*   Your proxy handles all authentication and passes user identity via headers
*   You’re in a Kubernetes or container environment where the proxy is the only path to the Gateway
*   You’re hitting WebSocket `1008 unauthorized` errors because browsers can’t pass tokens in WS payloads

## When NOT to Use

*   If your proxy doesn’t authenticate users (just a TLS terminator or load balancer)
*   If there’s any path to the Gateway that bypasses the proxy (firewall holes, internal network access)
*   If you’re unsure whether your proxy correctly strips/overwrites forwarded headers
*   If you only need personal single-user access (consider Tailscale Serve + loopback for simpler setup)

## How It Works

1.  Your reverse proxy authenticates users (OAuth, OIDC, SAML, etc.)
2.  Proxy adds a header with the authenticated user identity (e.g., `x-forwarded-user: nick@example.com`)
3.  OpenClaw checks that the request came from a **trusted proxy IP** (configured in `gateway.trustedProxies`)
4.  OpenClaw extracts the user identity from the configured header
5.  If everything checks out, the request is authorized

## Control UI Pairing Behavior

When `gateway.auth.mode = "trusted-proxy"` is active and the request passes trusted-proxy checks, Control UI WebSocket sessions can connect without device pairing identity. Implications:

*   Pairing is no longer the primary gate for Control UI access in this mode.
*   Your reverse proxy auth policy and `allowUsers` become the effective access control.
*   Keep gateway ingress locked to trusted proxy IPs only (`gateway.trustedProxies` + firewall).

## Configuration

```
{
  gateway: {
    // Use loopback for same-host proxy setups; use lan/custom for remote proxy hosts
    bind: "loopback",

    // CRITICAL: Only add your proxy's IP(s) here
    trustedProxies: ["10.0.0.1", "172.17.0.1"],

    auth: {
      mode: "trusted-proxy",
      trustedProxy: {
        // Header containing authenticated user identity (required)
        userHeader: "x-forwarded-user",

        // Optional: headers that MUST be present (proxy verification)
        requiredHeaders: ["x-forwarded-proto", "x-forwarded-host"],

        // Optional: restrict to specific users (empty = allow all)
        allowUsers: ["nick@example.com", "admin@company.org"],
      },
    },
  },
}
```

If `gateway.bind` is `loopback`, include a loopback proxy address in `gateway.trustedProxies` (`127.0.0.1`, `::1`, or an equivalent loopback CIDR).

### Configuration Reference

| Field | Required | Description |
| --- | --- | --- |
| `gateway.trustedProxies` | Yes | Array of proxy IP addresses to trust. Requests from other IPs are rejected. |
| `gateway.auth.mode` | Yes | Must be `"trusted-proxy"` |
| `gateway.auth.trustedProxy.userHeader` | Yes | Header name containing the authenticated user identity |
| `gateway.auth.trustedProxy.requiredHeaders` | No  | Additional headers that must be present for the request to be trusted |
| `gateway.auth.trustedProxy.allowUsers` | No  | Allowlist of user identities. Empty means allow all authenticated users. |

## TLS termination and HSTS

Use one TLS termination point and apply HSTS there.

### Recommended pattern: proxy TLS termination

When your reverse proxy handles HTTPS for `https://control.example.com`, set `Strict-Transport-Security` at the proxy for that domain.

*   Good fit for internet-facing deployments.
*   Keeps certificate + HTTP hardening policy in one place.
*   OpenClaw can stay on loopback HTTP behind the proxy.

Example header value:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### Gateway TLS termination

If OpenClaw itself serves HTTPS directly (no TLS-terminating proxy), set:

```
{
  gateway: {
    tls: { enabled: true },
    http: {
      securityHeaders: {
        strictTransportSecurity: "max-age=31536000; includeSubDomains",
      },
    },
  },
}
```

`strictTransportSecurity` accepts a string header value, or `false` to disable explicitly.

### Rollout guidance

*   Start with a short max age first (for example `max-age=300`) while validating traffic.
*   Increase to long-lived values (for example `max-age=31536000`) only after confidence is high.
*   Add `includeSubDomains` only if every subdomain is HTTPS-ready.
*   Use preload only if you intentionally meet preload requirements for your full domain set.
*   Loopback-only local development does not benefit from HSTS.

## Proxy Setup Examples

### Pomerium

Pomerium passes identity in `x-pomerium-claim-email` (or other claim headers) and a JWT in `x-pomerium-jwt-assertion`.

```
{
  gateway: {
    bind: "lan",
    trustedProxies: ["10.0.0.1"], // Pomerium's IP
    auth: {
      mode: "trusted-proxy",
      trustedProxy: {
        userHeader: "x-pomerium-claim-email",
        requiredHeaders: ["x-pomerium-jwt-assertion"],
      },
    },
  },
}
```

Pomerium config snippet:

```
routes:
  - from: https://openclaw.example.com
    to: http://openclaw-gateway:18789
    policy:
      - allow:
          or:
            - email:
                is: nick@example.com
    pass_identity_headers: true
```

### Caddy with OAuth

Caddy with the `caddy-security` plugin can authenticate users and pass identity headers.

```
{
  gateway: {
    bind: "lan",
    trustedProxies: ["127.0.0.1"], // Caddy's IP (if on same host)
    auth: {
      mode: "trusted-proxy",
      trustedProxy: {
        userHeader: "x-forwarded-user",
      },
    },
  },
}
```

Caddyfile snippet:

```
openclaw.example.com {
    authenticate with oauth2_provider
    authorize with policy1

    reverse_proxy openclaw:18789 {
        header_up X-Forwarded-User {http.auth.user.email}
    }
}
```

### nginx + oauth2-proxy

oauth2-proxy authenticates users and passes identity in `x-auth-request-email`.

```
{
  gateway: {
    bind: "lan",
    trustedProxies: ["10.0.0.1"], // nginx/oauth2-proxy IP
    auth: {
      mode: "trusted-proxy",
      trustedProxy: {
        userHeader: "x-auth-request-email",
      },
    },
  },
}
```

nginx config snippet:

```
location / {
    auth_request /oauth2/auth;
    auth_request_set $user $upstream_http_x_auth_request_email;

    proxy_pass http://openclaw:18789;
    proxy_set_header X-Auth-Request-Email $user;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### Traefik with Forward Auth

```
{
  gateway: {
    bind: "lan",
    trustedProxies: ["172.17.0.1"], // Traefik container IP
    auth: {
      mode: "trusted-proxy",
      trustedProxy: {
        userHeader: "x-forwarded-user",
      },
    },
  },
}
```

## Security Checklist

Before enabling trusted-proxy auth, verify:

*   **Proxy is the only path**: The Gateway port is firewalled from everything except your proxy
*   **trustedProxies is minimal**: Only your actual proxy IPs, not entire subnets
*   **Proxy strips headers**: Your proxy overwrites (not appends) `x-forwarded-*` headers from clients
*   **TLS termination**: Your proxy handles TLS; users connect via HTTPS
*   **allowUsers is set** (recommended): Restrict to known users rather than allowing anyone authenticated

## Security Audit

`openclaw security audit` will flag trusted-proxy auth with a **critical** severity finding. This is intentional — it’s a reminder that you’re delegating security to your proxy setup. The audit checks for:

*   Missing `trustedProxies` configuration
*   Missing `userHeader` configuration
*   Empty `allowUsers` (allows any authenticated user)

## Troubleshooting

### ”trusted\_proxy\_untrusted\_source”

The request didn’t come from an IP in `gateway.trustedProxies`. Check:

*   Is the proxy IP correct? (Docker container IPs can change)
*   Is there a load balancer in front of your proxy?
*   Use `docker inspect` or `kubectl get pods -o wide` to find actual IPs

### ”trusted\_proxy\_user\_missing”

The user header was empty or missing. Check:

*   Is your proxy configured to pass identity headers?
*   Is the header name correct? (case-insensitive, but spelling matters)
*   Is the user actually authenticated at the proxy?

A required header wasn’t present. Check:

*   Your proxy configuration for those specific headers
*   Whether headers are being stripped somewhere in the chain

### ”trusted\_proxy\_user\_not\_allowed”

The user is authenticated but not in `allowUsers`. Either add them or remove the allowlist.

### WebSocket Still Failing

Make sure your proxy:

*   Supports WebSocket upgrades (`Upgrade: websocket`, `Connection: upgrade`)
*   Passes the identity headers on WebSocket upgrade requests (not just HTTP)
*   Doesn’t have a separate auth path for WebSocket connections

## Migration from Token Auth

If you’re moving from token auth to trusted-proxy:

1.  Configure your proxy to authenticate users and pass headers
2.  Test the proxy setup independently (curl with headers)
3.  Update OpenClaw config with trusted-proxy auth
4.  Restart the Gateway
5.  Test WebSocket connections from the Control UI
6.  Run `openclaw security audit` and review findings

*   [Security](https://docs.openclaw.ai/gateway/security) — full security guide
*   [Configuration](https://docs.openclaw.ai/gateway/configuration) — config reference
*   [Remote Access](https://docs.openclaw.ai/gateway/remote) — other remote access patterns
*   [Tailscale](https://docs.openclaw.ai/gateway/tailscale) — simpler alternative for tailnet-only access

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/doctor -->

# Doctor - OpenClaw

`openclaw doctor` is the repair + migration tool for OpenClaw. It fixes stale config/state, checks health, and provides actionable repair steps.

## Quick start

### Headless / automation

Accept defaults without prompting (including restart/service/sandbox repair steps when applicable).

Apply recommended repairs without prompting (repairs + restarts where safe).

```
openclaw doctor --repair --force
```

Apply aggressive repairs too (overwrites custom supervisor configs).

```
openclaw doctor --non-interactive
```

Run without prompts and only apply safe migrations (config normalization + on-disk state moves). Skips restart/service/sandbox actions that require human confirmation. Legacy state migrations run automatically when detected.

Scan system services for extra gateway installs (launchd/systemd/schtasks). If you want to review changes before writing, open the config file first:

```
cat ~/.openclaw/openclaw.json
```

## What it does (summary)

*   Optional pre-flight update for git installs (interactive only).
*   UI protocol freshness check (rebuilds Control UI when the protocol schema is newer).
*   Health check + restart prompt.
*   Skills status summary (eligible/missing/blocked).
*   Config normalization for legacy values.
*   OpenCode Zen provider override warnings (`models.providers.opencode`).
*   Legacy on-disk state migration (sessions/agent dir/WhatsApp auth).
*   State integrity and permissions checks (sessions, transcripts, state dir).
*   Config file permission checks (chmod 600) when running locally.
*   Model auth health: checks OAuth expiry, can refresh expiring tokens, and reports auth-profile cooldown/disabled states.
*   Extra workspace dir detection (`~/openclaw`).
*   Sandbox image repair when sandboxing is enabled.
*   Legacy service migration and extra gateway detection.
*   Gateway runtime checks (service installed but not running; cached launchd label).
*   Channel status warnings (probed from the running gateway).
*   Supervisor config audit (launchd/systemd/schtasks) with optional repair.
*   Gateway runtime best-practice checks (Node vs Bun, version-manager paths).
*   Gateway port collision diagnostics (default `18789`).
*   Security warnings for open DM policies.
*   Gateway auth checks for local token mode (offers token generation when no token source exists; does not overwrite token SecretRef configs).
*   systemd linger check on Linux.
*   Source install checks (pnpm workspace mismatch, missing UI assets, missing tsx binary).
*   Writes updated config + wizard metadata.

## Detailed behavior and rationale

### 0) Optional update (git installs)

If this is a git checkout and doctor is running interactively, it offers to update (fetch/rebase/build) before running doctor.

### 1) Config normalization

If the config contains legacy value shapes (for example `messages.ackReaction` without a channel-specific override), doctor normalizes them into the current schema.

### 2) Legacy config key migrations

When the config contains deprecated keys, other commands refuse to run and ask you to run `openclaw doctor`. Doctor will:

*   Explain which legacy keys were found.
*   Show the migration it applied.
*   Rewrite `~/.openclaw/openclaw.json` with the updated schema.

The Gateway also auto-runs doctor migrations on startup when it detects a legacy config format, so stale configs are repaired without manual intervention. Current migrations:

*   `routing.allowFrom` → `channels.whatsapp.allowFrom`
*   `routing.groupChat.requireMention` → `channels.whatsapp/telegram/imessage.groups."*".requireMention`
*   `routing.groupChat.historyLimit` → `messages.groupChat.historyLimit`
*   `routing.groupChat.mentionPatterns` → `messages.groupChat.mentionPatterns`
*   `routing.queue` → `messages.queue`
*   `routing.bindings` → top-level `bindings`
*   `routing.agents`/`routing.defaultAgentId` → `agents.list` + `agents.list[].default`
*   `routing.agentToAgent` → `tools.agentToAgent`
*   `routing.transcribeAudio` → `tools.media.audio.models`
*   `bindings[].match.accountID` → `bindings[].match.accountId`
*   For channels with named `accounts` but missing `accounts.default`, move account-scoped top-level single-account channel values into `channels.<channel>.accounts.default` when present
*   `identity` → `agents.list[].identity`
*   `agent.*` → `agents.defaults` + `tools.*` (tools/elevated/exec/sandbox/subagents)
*   `agent.model`/`allowedModels`/`modelAliases`/`modelFallbacks`/`imageModelFallbacks` → `agents.defaults.models` + `agents.defaults.model.primary/fallbacks` + `agents.defaults.imageModel.primary/fallbacks`
*   `browser.ssrfPolicy.allowPrivateNetwork` → `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork`

Doctor warnings also include account-default guidance for multi-account channels:

*   If two or more `channels.<channel>.accounts` entries are configured without `channels.<channel>.defaultAccount` or `accounts.default`, doctor warns that fallback routing can pick an unexpected account.
*   If `channels.<channel>.defaultAccount` is set to an unknown account ID, doctor warns and lists configured account IDs.

### 2b) OpenCode Zen provider overrides

If you’ve added `models.providers.opencode` (or `opencode-zen`) manually, it overrides the built-in OpenCode Zen catalog from `@mariozechner/pi-ai`. That can force every model onto a single API or zero out costs. Doctor warns so you can remove the override and restore per-model API routing + costs.

### 3) Legacy state migrations (disk layout)

Doctor can migrate older on-disk layouts into the current structure:

*   Sessions store + transcripts:
    *   from `~/.openclaw/sessions/` to `~/.openclaw/agents/<agentId>/sessions/`
*   Agent dir:
    *   from `~/.openclaw/agent/` to `~/.openclaw/agents/<agentId>/agent/`
*   WhatsApp auth state (Baileys):
    *   from legacy `~/.openclaw/credentials/*.json` (except `oauth.json`)
    *   to `~/.openclaw/credentials/whatsapp/<accountId>/...` (default account id: `default`)

These migrations are best-effort and idempotent; doctor will emit warnings when it leaves any legacy folders behind as backups. The Gateway/CLI also auto-migrates the legacy sessions + agent dir on startup so history/auth/models land in the per-agent path without a manual doctor run. WhatsApp auth is intentionally only migrated via `openclaw doctor`.

### 4) State integrity checks (session persistence, routing, and safety)

The state directory is the operational brainstem. If it vanishes, you lose sessions, credentials, logs, and config (unless you have backups elsewhere). Doctor checks:

*   **State dir missing**: warns about catastrophic state loss, prompts to recreate the directory, and reminds you that it cannot recover missing data.
*   **State dir permissions**: verifies writability; offers to repair permissions (and emits a `chown` hint when owner/group mismatch is detected).
*   **macOS cloud-synced state dir**: warns when state resolves under iCloud Drive (`~/Library/Mobile Documents/com~apple~CloudDocs/...`) or `~/Library/CloudStorage/...` because sync-backed paths can cause slower I/O and lock/sync races.
*   **Linux SD or eMMC state dir**: warns when state resolves to an `mmcblk*` mount source, because SD or eMMC-backed random I/O can be slower and wear faster under session and credential writes.
*   **Session dirs missing**: `sessions/` and the session store directory are required to persist history and avoid `ENOENT` crashes.
*   **Transcript mismatch**: warns when recent session entries have missing transcript files.
*   **Main session “1-line JSONL”**: flags when the main transcript has only one line (history is not accumulating).
*   **Multiple state dirs**: warns when multiple `~/.openclaw` folders exist across home directories or when `OPENCLAW_STATE_DIR` points elsewhere (history can split between installs).
*   **Remote mode reminder**: if `gateway.mode=remote`, doctor reminds you to run it on the remote host (the state lives there).
*   **Config file permissions**: warns if `~/.openclaw/openclaw.json` is group/world readable and offers to tighten to `600`.

### 5) Model auth health (OAuth expiry)

Doctor inspects OAuth profiles in the auth store, warns when tokens are expiring/expired, and can refresh them when safe. If the Anthropic Claude Code profile is stale, it suggests running `claude setup-token` (or pasting a setup-token). Refresh prompts only appear when running interactively (TTY); `--non-interactive` skips refresh attempts. Doctor also reports auth profiles that are temporarily unusable due to:

*   short cooldowns (rate limits/timeouts/auth failures)
*   longer disables (billing/credit failures)

### 6) Hooks model validation

If `hooks.gmail.model` is set, doctor validates the model reference against the catalog and allowlist and warns when it won’t resolve or is disallowed.

### 7) Sandbox image repair

When sandboxing is enabled, doctor checks Docker images and offers to build or switch to legacy names if the current image is missing.

### 8) Gateway service migrations and cleanup hints

Doctor detects legacy gateway services (launchd/systemd/schtasks) and offers to remove them and install the OpenClaw service using the current gateway port. It can also scan for extra gateway-like services and print cleanup hints. Profile-named OpenClaw gateway services are considered first-class and are not flagged as “extra.”

### 9) Security warnings

Doctor emits warnings when a provider is open to DMs without an allowlist, or when a policy is configured in a dangerous way.

### 10) systemd linger (Linux)

If running as a systemd user service, doctor ensures lingering is enabled so the gateway stays alive after logout.

### 11) Skills status

Doctor prints a quick summary of eligible/missing/blocked skills for the current workspace.

### 12) Gateway auth checks (local token)

Doctor checks local gateway token auth readiness.

*   If token mode needs a token and no token source exists, doctor offers to generate one.
*   If `gateway.auth.token` is SecretRef-managed but unavailable, doctor warns and does not overwrite it with plaintext.
*   `openclaw doctor --generate-gateway-token` forces generation only when no token SecretRef is configured.

### 12b) Read-only SecretRef-aware repairs

Some repair flows need to inspect configured credentials without weakening runtime fail-fast behavior.

*   `openclaw doctor --fix` now uses the same read-only SecretRef summary model as status-family commands for targeted config repairs.
*   Example: Telegram `allowFrom` / `groupAllowFrom` `@username` repair tries to use configured bot credentials when available.
*   If the Telegram bot token is configured via SecretRef but unavailable in the current command path, doctor reports that the credential is configured-but-unavailable and skips auto-resolution instead of crashing or misreporting the token as missing.

### 13) Gateway health check + restart

Doctor runs a health check and offers to restart the gateway when it looks unhealthy.

### 14) Channel status warnings

If the gateway is healthy, doctor runs a channel status probe and reports warnings with suggested fixes.

### 15) Supervisor config audit + repair

Doctor checks the installed supervisor config (launchd/systemd/schtasks) for missing or outdated defaults (e.g., systemd network-online dependencies and restart delay). When it finds a mismatch, it recommends an update and can rewrite the service file/task to the current defaults. Notes:

*   `openclaw doctor` prompts before rewriting supervisor config.
*   `openclaw doctor --yes` accepts the default repair prompts.
*   `openclaw doctor --repair` applies recommended fixes without prompts.
*   `openclaw doctor --repair --force` overwrites custom supervisor configs.
*   If token auth requires a token and `gateway.auth.token` is SecretRef-managed, doctor service install/repair validates the SecretRef but does not persist resolved plaintext token values into supervisor service environment metadata.
*   If token auth requires a token and the configured token SecretRef is unresolved, doctor blocks the install/repair path with actionable guidance.
*   If both `gateway.auth.token` and `gateway.auth.password` are configured and `gateway.auth.mode` is unset, doctor blocks install/repair until mode is set explicitly.
*   For Linux user-systemd units, doctor token drift checks now include both `Environment=` and `EnvironmentFile=` sources when comparing service auth metadata.
*   You can always force a full rewrite via `openclaw gateway install --force`.

### 16) Gateway runtime + port diagnostics

Doctor inspects the service runtime (PID, last exit status) and warns when the service is installed but not actually running. It also checks for port collisions on the gateway port (default `18789`) and reports likely causes (gateway already running, SSH tunnel).

### 17) Gateway runtime best practices

Doctor warns when the gateway service runs on Bun or a version-managed Node path (`nvm`, `fnm`, `volta`, `asdf`, etc.). WhatsApp + Telegram channels require Node, and version-manager paths can break after upgrades because the service does not load your shell init. Doctor offers to migrate to a system Node install when available (Homebrew/apt/choco).

### 18) Config write + wizard metadata

Doctor persists any config changes and stamps wizard metadata to record the doctor run.

### 19) Workspace tips (backup + memory system)

Doctor suggests a workspace memory system when missing and prints a backup tip if the workspace is not already under git. See [/concepts/agent-workspace](https://docs.openclaw.ai/concepts/agent-workspace) for a full guide to workspace structure and git backup (recommended private GitHub or GitLab).

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/logging -->

# Logging - OpenClaw

For a user-facing overview (CLI + Control UI + config), see [/logging](https://docs.openclaw.ai/logging). OpenClaw has two log “surfaces”:

*   **Console output** (what you see in the terminal / Debug UI).
*   **File logs** (JSON lines) written by the gateway logger.

## File-based logger

*   Default rolling log file is under `/tmp/openclaw/` (one file per day): `openclaw-YYYY-MM-DD.log`
    *   Date uses the gateway host’s local timezone.
*   The log file path and level can be configured via `~/.openclaw/openclaw.json`:
    *   `logging.file`
    *   `logging.level`

The file format is one JSON object per line. The Control UI Logs tab tails this file via the gateway (`logs.tail`). CLI can do the same:

**Verbose vs. log levels**

*   **File logs** are controlled exclusively by `logging.level`.
*   `--verbose` only affects **console verbosity** (and WS log style); it does **not** raise the file log level.
*   To capture verbose-only details in file logs, set `logging.level` to `debug` or `trace`.

## Console capture

The CLI captures `console.log/info/warn/error/debug/trace` and writes them to file logs, while still printing to stdout/stderr. You can tune console verbosity independently via:

*   `logging.consoleLevel` (default `info`)
*   `logging.consoleStyle` (`pretty` | `compact` | `json`)

Verbose tool summaries (e.g. `🛠️ Exec: ...`) can mask sensitive tokens before they hit the console stream. This is **tools-only** and does not alter file logs.

*   `logging.redactSensitive`: `off` | `tools` (default: `tools`)
*   `logging.redactPatterns`: array of regex strings (overrides defaults)
    *   Use raw regex strings (auto `gi`), or `/pattern/flags` if you need custom flags.
    *   Matches are masked by keeping the first 6 + last 4 chars (length >= 18), otherwise `***`.
    *   Defaults cover common key assignments, CLI flags, JSON fields, bearer headers, PEM blocks, and popular token prefixes.

## Gateway WebSocket logs

The gateway prints WebSocket protocol logs in two modes:

*   **Normal mode (no `--verbose`)**: only “interesting” RPC results are printed:
    *   errors (`ok=false`)
    *   slow calls (default threshold: `>= 50ms`)
    *   parse errors
*   **Verbose mode (`--verbose`)**: prints all WS request/response traffic.

### WS log style

`openclaw gateway` supports a per-gateway style switch:

*   `--ws-log auto` (default): normal mode is optimized; verbose mode uses compact output
*   `--ws-log compact`: compact output (paired request/response) when verbose
*   `--ws-log full`: full per-frame output when verbose
*   `--compact`: alias for `--ws-log compact`

Examples:

```
# optimized (only errors/slow)
openclaw gateway

# show all WS traffic (paired)
openclaw gateway --verbose --ws-log compact

# show all WS traffic (full meta)
openclaw gateway --verbose --ws-log full
```

## Console formatting (subsystem logging)

The console formatter is **TTY-aware** and prints consistent, prefixed lines. Subsystem loggers keep output grouped and scannable. Behavior:

*   **Subsystem prefixes** on every line (e.g. `[gateway]`, `[canvas]`, `[tailscale]`)
*   **Subsystem colors** (stable per subsystem) plus level coloring
*   **Color when output is a TTY or the environment looks like a rich terminal** (`TERM`/`COLORTERM`/`TERM_PROGRAM`), respects `NO_COLOR`
*   **Shortened subsystem prefixes**: drops leading `gateway/` + `channels/`, keeps last 2 segments (e.g. `whatsapp/outbound`)
*   **Sub-loggers by subsystem** (auto prefix + structured field `{ subsystem }`)
*   **`logRaw()`** for QR/UX output (no prefix, no formatting)
*   **Console styles** (e.g. `pretty | compact | json`)
*   **Console log level** separate from file log level (file keeps full detail when `logging.level` is set to `debug`/`trace`)
*   **WhatsApp message bodies** are logged at `debug` (use `--verbose` to see them)

This keeps existing file logs stable while making interactive output scannable.

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated -->

# Sandbox vs Tool Policy vs Elevated

OpenClaw has three related (but different) controls:

1.  **Sandbox** (`agents.defaults.sandbox.*` / `agents.list[].sandbox.*`) decides **where tools run** (Docker vs host).
2.  **Tool policy** (`tools.*`, `tools.sandbox.tools.*`, `agents.list[].tools.*`) decides **which tools are available/allowed**.
3.  **Elevated** (`tools.elevated.*`, `agents.list[].tools.elevated.*`) is an **exec-only escape hatch** to run on the host when you’re sandboxed.

## Quick debug

Use the inspector to see what OpenClaw is _actually_ doing:

```
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --agent work
openclaw sandbox explain --json
```

It prints:

*   effective sandbox mode/scope/workspace access
*   whether the session is currently sandboxed (main vs non-main)
*   effective sandbox tool allow/deny (and whether it came from agent/global/default)
*   elevated gates and fix-it key paths

Sandboxing is controlled by `agents.defaults.sandbox.mode`:

*   `"off"`: everything runs on the host.
*   `"non-main"`: only non-main sessions are sandboxed (common “surprise” for groups/channels).
*   `"all"`: everything is sandboxed.

See [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing) for the full matrix (scope, workspace mounts, images).

### Bind mounts (security quick check)

*   `docker.binds` _pierces_ the sandbox filesystem: whatever you mount is visible inside the container with the mode you set (`:ro` or `:rw`).
*   Default is read-write if you omit the mode; prefer `:ro` for source/secrets.
*   `scope: "shared"` ignores per-agent binds (only global binds apply).
*   Binding `/var/run/docker.sock` effectively hands host control to the sandbox; only do this intentionally.
*   Workspace access (`workspaceAccess: "ro"`/`"rw"`) is independent of bind modes.

Two layers matter:

*   **Tool profile**: `tools.profile` and `agents.list[].tools.profile` (base allowlist)
*   **Provider tool profile**: `tools.byProvider[provider].profile` and `agents.list[].tools.byProvider[provider].profile`
*   **Global/per-agent tool policy**: `tools.allow`/`tools.deny` and `agents.list[].tools.allow`/`agents.list[].tools.deny`
*   **Provider tool policy**: `tools.byProvider[provider].allow/deny` and `agents.list[].tools.byProvider[provider].allow/deny`
*   **Sandbox tool policy** (only applies when sandboxed): `tools.sandbox.tools.allow`/`tools.sandbox.tools.deny` and `agents.list[].tools.sandbox.tools.*`

Rules of thumb:

*   `deny` always wins.
*   If `allow` is non-empty, everything else is treated as blocked.
*   Tool policy is the hard stop: `/exec` cannot override a denied `exec` tool.
*   `/exec` only changes session defaults for authorized senders; it does not grant tool access. Provider tool keys accept either `provider` (e.g. `google-antigravity`) or `provider/model` (e.g. `openai/gpt-5.2`).

### Tool groups (shorthands)

Tool policies (global, agent, sandbox) support `group:*` entries that expand to multiple tools:

```
{
  tools: {
    sandbox: {
      tools: {
        allow: ["group:runtime", "group:fs", "group:sessions", "group:memory"],
      },
    },
  },
}
```

Available groups:

*   `group:runtime`: `exec`, `bash`, `process`
*   `group:fs`: `read`, `write`, `edit`, `apply_patch`
*   `group:sessions`: `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
*   `group:memory`: `memory_search`, `memory_get`
*   `group:ui`: `browser`, `canvas`
*   `group:automation`: `cron`, `gateway`
*   `group:messaging`: `message`
*   `group:nodes`: `nodes`
*   `group:openclaw`: all built-in OpenClaw tools (excludes provider plugins)

## Elevated: exec-only “run on host”

Elevated does **not** grant extra tools; it only affects `exec`.

*   If you’re sandboxed, `/elevated on` (or `exec` with `elevated: true`) runs on the host (approvals may still apply).
*   Use `/elevated full` to skip exec approvals for the session.
*   If you’re already running direct, elevated is effectively a no-op (still gated).
*   Elevated is **not** skill-scoped and does **not** override tool allow/deny.
*   `/exec` is separate from elevated. It only adjusts per-session exec defaults for authorized senders.

Gates:

*   Enablement: `tools.elevated.enabled` (and optionally `agents.list[].tools.elevated.enabled`)
*   Sender allowlists: `tools.elevated.allowFrom.<provider>` (and optionally `agents.list[].tools.elevated.allowFrom.<provider>`)

See [Elevated Mode](https://docs.openclaw.ai/tools/elevated).

## Common “sandbox jail” fixes

### “Tool X blocked by sandbox tool policy”

Fix-it keys (pick one):

*   Disable sandbox: `agents.defaults.sandbox.mode=off` (or per-agent `agents.list[].sandbox.mode=off`)
*   Allow the tool inside sandbox:
    *   remove it from `tools.sandbox.tools.deny` (or per-agent `agents.list[].tools.sandbox.tools.deny`)
    *   or add it to `tools.sandbox.tools.allow` (or per-agent allow)

### “I thought this was main, why is it sandboxed?”

In `"non-main"` mode, group/channel keys are _not_ main. Use the main session key (shown by `sandbox explain`) or switch mode to `"off"`.

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/gateway-lock -->

# Gateway Lock - OpenClaw

##### Gateway

*   [](https://docs.openclaw.ai/gateway)
*   *   [](https://docs.openclaw.ai/gateway/configuration)
    *   [](https://docs.openclaw.ai/gateway/configuration-reference)
    *   [](https://docs.openclaw.ai/gateway/configuration-examples)
    *   [](https://docs.openclaw.ai/gateway/authentication)
    *   [
        
        Auth credential semantics
        
        
        
        ](https://docs.openclaw.ai/auth-credential-semantics)
    *   [](https://docs.openclaw.ai/gateway/secrets)
    *   [
        
        Secrets Apply Plan Contract
        
        
        
        ](https://docs.openclaw.ai/gateway/secrets-plan-contract)
    *   [](https://docs.openclaw.ai/gateway/trusted-proxy-auth)
    *   [](https://docs.openclaw.ai/gateway/health)
    *   [](https://docs.openclaw.ai/gateway/heartbeat)
    *   [](https://docs.openclaw.ai/gateway/doctor)
    *   [](https://docs.openclaw.ai/gateway/logging)
    *   [](https://docs.openclaw.ai/gateway/gateway-lock)
    *   [
        
        Background Exec and Process Tool
        
        
        
        ](https://docs.openclaw.ai/gateway/background-process)
    *   [](https://docs.openclaw.ai/gateway/multiple-gateways)
    *   [](https://docs.openclaw.ai/gateway/troubleshooting)

##### Remote access

*   [](https://docs.openclaw.ai/gateway/remote)
*   [](https://docs.openclaw.ai/gateway/remote-gateway-readme)
*   [](https://docs.openclaw.ai/gateway/tailscale)

##### Web interfaces

*   [](https://docs.openclaw.ai/web)
*   [](https://docs.openclaw.ai/web/control-ui)
*   [](https://docs.openclaw.ai/web/dashboard)
*   [](https://docs.openclaw.ai/web/webchat)
*   [](https://docs.openclaw.ai/web/tui)

*   [Gateway lock](https://docs.openclaw.ai/gateway/gateway-lock#gateway-lock)
*   [Why](https://docs.openclaw.ai/gateway/gateway-lock#why)
*   [Mechanism](https://docs.openclaw.ai/gateway/gateway-lock#mechanism)
*   [Error surface](https://docs.openclaw.ai/gateway/gateway-lock#error-surface)
*   [Operational notes](https://docs.openclaw.ai/gateway/gateway-lock#operational-notes)

Configuration and operations

## Gateway lock

Last updated: 2025-12-11

## Why

*   Ensure only one gateway instance runs per base port on the same host; additional gateways must use isolated profiles and unique ports.
*   Survive crashes/SIGKILL without leaving stale lock files.
*   Fail fast with a clear error when the control port is already occupied.

## Mechanism

*   The gateway binds the WebSocket listener (default `ws://127.0.0.1:18789`) immediately on startup using an exclusive TCP listener.
*   If the bind fails with `EADDRINUSE`, startup throws `GatewayLockError("another gateway instance is already listening on ws://127.0.0.1:<port>")`.
*   The OS releases the listener automatically on any process exit, including crashes and SIGKILL—no separate lock file or cleanup step is needed.
*   On shutdown the gateway closes the WebSocket server and underlying HTTP server to free the port promptly.

## Error surface

*   If another process holds the port, startup throws `GatewayLockError("another gateway instance is already listening on ws://127.0.0.1:<port>")`.
*   Other bind failures surface as `GatewayLockError("failed to bind gateway socket on ws://127.0.0.1:<port>: …")`.

## Operational notes

*   If the port is occupied by _another_ process, the error is the same; free the port or choose another with `openclaw gateway --port <port>`.
*   The macOS app still maintains its own lightweight PID guard before spawning the gateway; the runtime lock is enforced by the WebSocket bind.

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/background-process -->

# Background Exec and Process Tool

OpenClaw runs shell commands through the `exec` tool and keeps long‑running tasks in memory. The `process` tool manages those background sessions.

Key parameters:

*   `command` (required)
*   `yieldMs` (default 10000): auto‑background after this delay
*   `background` (bool): background immediately
*   `timeout` (seconds, default 1800): kill the process after this timeout
*   `elevated` (bool): run on host if elevated mode is enabled/allowed
*   Need a real TTY? Set `pty: true`.
*   `workdir`, `env`

Behavior:

*   Foreground runs return output directly.
*   When backgrounded (explicit or timeout), the tool returns `status: "running"` + `sessionId` and a short tail.
*   Output is kept in memory until the session is polled or cleared.
*   If the `process` tool is disallowed, `exec` runs synchronously and ignores `yieldMs`/`background`.
*   Spawned exec commands receive `OPENCLAW_SHELL=exec` for context-aware shell/profile rules.

## Child process bridging

When spawning long-running child processes outside the exec/process tools (for example, CLI respawns or gateway helpers), attach the child-process bridge helper so termination signals are forwarded and listeners are detached on exit/error. This avoids orphaned processes on systemd and keeps shutdown behavior consistent across platforms. Environment overrides:

*   `PI_BASH_YIELD_MS`: default yield (ms)
*   `PI_BASH_MAX_OUTPUT_CHARS`: in‑memory output cap (chars)
*   `OPENCLAW_BASH_PENDING_MAX_OUTPUT_CHARS`: pending stdout/stderr cap per stream (chars)
*   `PI_BASH_JOB_TTL_MS`: TTL for finished sessions (ms, bounded to 1m–3h)

Config (preferred):

*   `tools.exec.backgroundMs` (default 10000)
*   `tools.exec.timeoutSec` (default 1800)
*   `tools.exec.cleanupMs` (default 1800000)
*   `tools.exec.notifyOnExit` (default true): enqueue a system event + request heartbeat when a backgrounded exec exits.
*   `tools.exec.notifyOnExitEmptySuccess` (default false): when true, also enqueue completion events for successful backgrounded runs that produced no output.

Actions:

*   `list`: running + finished sessions
*   `poll`: drain new output for a session (also reports exit status)
*   `log`: read the aggregated output (supports `offset` + `limit`)
*   `write`: send stdin (`data`, optional `eof`)
*   `kill`: terminate a background session
*   `clear`: remove a finished session from memory
*   `remove`: kill if running, otherwise clear if finished

Notes:

*   Only backgrounded sessions are listed/persisted in memory.
*   Sessions are lost on process restart (no disk persistence).
*   Session logs are only saved to chat history if you run `process poll/log` and the tool result is recorded.
*   `process` is scoped per agent; it only sees sessions started by that agent.
*   `process list` includes a derived `name` (command verb + target) for quick scans.
*   `process log` uses line-based `offset`/`limit`.
*   When both `offset` and `limit` are omitted, it returns the last 200 lines and includes a paging hint.
*   When `offset` is provided and `limit` is omitted, it returns from `offset` to the end (not capped to 200).

## Examples

Run a long task and poll later:

```
{ "tool": "exec", "command": "sleep 5 && echo done", "yieldMs": 1000 }
```

```
{ "tool": "process", "action": "poll", "sessionId": "<id>" }
```

Start immediately in background:

```
{ "tool": "exec", "command": "npm run build", "background": true }
```

Send stdin:

```
{ "tool": "process", "action": "write", "sessionId": "<id>", "data": "y\n" }
```

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/openai-http-api -->

# OpenAI Chat Completions - OpenClaw

OpenClaw’s Gateway can serve a small OpenAI-compatible Chat Completions endpoint. This endpoint is **disabled by default**. Enable it in config first.

*   `POST /v1/chat/completions`
*   Same port as the Gateway (WS + HTTP multiplex): `http://<gateway-host>:<port>/v1/chat/completions`

Under the hood, requests are executed as a normal Gateway agent run (same codepath as `openclaw agent`), so routing/permissions/config match your Gateway.

## Authentication

Uses the Gateway auth configuration. Send a bearer token:

*   `Authorization: Bearer <token>`

Notes:

*   When `gateway.auth.mode="token"`, use `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`).
*   When `gateway.auth.mode="password"`, use `gateway.auth.password` (or `OPENCLAW_GATEWAY_PASSWORD`).
*   If `gateway.auth.rateLimit` is configured and too many auth failures occur, the endpoint returns `429` with `Retry-After`.

## Security boundary (important)

Treat this endpoint as a **full operator-access** surface for the gateway instance.

*   HTTP bearer auth here is not a narrow per-user scope model.
*   A valid Gateway token/password for this endpoint should be treated like an owner/operator credential.
*   Requests run through the same control-plane agent path as trusted operator actions.
*   There is no separate non-owner/per-user tool boundary on this endpoint; once a caller passes Gateway auth here, OpenClaw treats that caller as a trusted operator for this gateway.
*   If the target agent policy allows sensitive tools, this endpoint can use them.
*   Keep this endpoint on loopback/tailnet/private ingress only; do not expose it directly to the public internet.

See [Security](https://docs.openclaw.ai/gateway/security) and [Remote access](https://docs.openclaw.ai/gateway/remote).

## Choosing an agent

No custom headers required: encode the agent id in the OpenAI `model` field:

*   `model: "openclaw:<agentId>"` (example: `"openclaw:main"`, `"openclaw:beta"`)
*   `model: "agent:<agentId>"` (alias)

Or target a specific OpenClaw agent by header:

*   `x-openclaw-agent-id: <agentId>` (default: `main`)

Advanced:

*   `x-openclaw-session-key: <sessionKey>` to fully control session routing.

## Enabling the endpoint

Set `gateway.http.endpoints.chatCompletions.enabled` to `true`:

```
{
  gateway: {
    http: {
      endpoints: {
        chatCompletions: { enabled: true },
      },
    },
  },
}
```

## Disabling the endpoint

Set `gateway.http.endpoints.chatCompletions.enabled` to `false`:

```
{
  gateway: {
    http: {
      endpoints: {
        chatCompletions: { enabled: false },
      },
    },
  },
}
```

## Session behavior

By default the endpoint is **stateless per request** (a new session key is generated each call). If the request includes an OpenAI `user` string, the Gateway derives a stable session key from it, so repeated calls can share an agent session.

## Streaming (SSE)

Set `stream: true` to receive Server-Sent Events (SSE):

*   `Content-Type: text/event-stream`
*   Each event line is `data: <json>`
*   Stream ends with `data: [DONE]`

## Examples

Non-streaming:

```
curl -sS http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "messages": [{"role":"user","content":"hi"}]
  }'
```

Streaming:

```
curl -N http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "stream": true,
    "messages": [{"role":"user","content":"hi"}]
  }'
```

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/tools-invoke-http-api -->

# Tools Invoke API - OpenClaw

OpenClaw’s Gateway exposes a simple HTTP endpoint for invoking a single tool directly. It is always enabled, but gated by Gateway auth and tool policy.

*   `POST /tools/invoke`
*   Same port as the Gateway (WS + HTTP multiplex): `http://<gateway-host>:<port>/tools/invoke`

Default max payload size is 2 MB.

## Authentication

Uses the Gateway auth configuration. Send a bearer token:

*   `Authorization: Bearer <token>`

Notes:

*   When `gateway.auth.mode="token"`, use `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`).
*   When `gateway.auth.mode="password"`, use `gateway.auth.password` (or `OPENCLAW_GATEWAY_PASSWORD`).
*   If `gateway.auth.rateLimit` is configured and too many auth failures occur, the endpoint returns `429` with `Retry-After`.

## Request body

```
{
  "tool": "sessions_list",
  "action": "json",
  "args": {},
  "sessionKey": "main",
  "dryRun": false
}
```

Fields:

*   `tool` (string, required): tool name to invoke.
*   `action` (string, optional): mapped into args if the tool schema supports `action` and the args payload omitted it.
*   `args` (object, optional): tool-specific arguments.
*   `sessionKey` (string, optional): target session key. If omitted or `"main"`, the Gateway uses the configured main session key (honors `session.mainKey` and default agent, or `global` in global scope).
*   `dryRun` (boolean, optional): reserved for future use; currently ignored.

## Policy + routing behavior

Tool availability is filtered through the same policy chain used by Gateway agents:

*   `tools.profile` / `tools.byProvider.profile`
*   `tools.allow` / `tools.byProvider.allow`
*   `agents.<id>.tools.allow` / `agents.<id>.tools.byProvider.allow`
*   group policies (if the session key maps to a group or channel)
*   subagent policy (when invoking with a subagent session key)

If a tool is not allowed by policy, the endpoint returns **404**. Gateway HTTP also applies a hard deny list by default (even if session policy allows the tool):

*   `sessions_spawn`
*   `sessions_send`
*   `gateway`
*   `whatsapp_login`

You can customize this deny list via `gateway.tools`:

```
{
  gateway: {
    tools: {
      // Additional tools to block over HTTP /tools/invoke
      deny: ["browser"],
      // Remove tools from the default deny list
      allow: ["gateway"],
    },
  },
}
```

To help group policies resolve context, you can optionally set:

*   `x-openclaw-message-channel: <channel>` (example: `slack`, `telegram`)
*   `x-openclaw-account-id: <accountId>` (when multiple accounts exist)

## Responses

*   `200` → `{ ok: true, result }`
*   `400` → `{ ok: false, error: { type, message } }` (invalid request or tool input error)
*   `401` → unauthorized
*   `429` → auth rate-limited (`Retry-After` set)
*   `404` → tool not available (not found or not allowlisted)
*   `405` → method not allowed
*   `500` → `{ ok: false, error: { type, message } }` (unexpected tool execution error; sanitized message)

## Example

```
curl -sS http://127.0.0.1:18789/tools/invoke \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "tool": "sessions_list",
    "action": "json",
    "args": {}
  }'
```

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/cli-backends -->

# CLI Backends - OpenClaw

## CLI backends (fallback runtime)

OpenClaw can run **local AI CLIs** as a **text-only fallback** when API providers are down, rate-limited, or temporarily misbehaving. This is intentionally conservative:

*   **Tools are disabled** (no tool calls).
*   **Text in → text out** (reliable).
*   **Sessions are supported** (so follow-up turns stay coherent).
*   **Images can be passed through** if the CLI accepts image paths.

This is designed as a **safety net** rather than a primary path. Use it when you want “always works” text responses without relying on external APIs.

## Beginner-friendly quick start

You can use Claude Code CLI **without any config** (OpenClaw ships a built-in default):

```
openclaw agent --message "hi" --model claude-cli/opus-4.6
```

Codex CLI also works out of the box:

```
openclaw agent --message "hi" --model codex-cli/gpt-5.4
```

If your gateway runs under launchd/systemd and PATH is minimal, add just the command path:

```
{
  agents: {
    defaults: {
      cliBackends: {
        "claude-cli": {
          command: "/opt/homebrew/bin/claude",
        },
      },
    },
  },
}
```

That’s it. No keys, no extra auth config needed beyond the CLI itself.

## Using it as a fallback

Add a CLI backend to your fallback list so it only runs when primary models fail:

```
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["claude-cli/opus-4.6", "claude-cli/opus-4.5"],
      },
      models: {
        "anthropic/claude-opus-4-6": { alias: "Opus" },
        "claude-cli/opus-4.6": {},
        "claude-cli/opus-4.5": {},
      },
    },
  },
}
```

Notes:

*   If you use `agents.defaults.models` (allowlist), you must include `claude-cli/...`.
*   If the primary provider fails (auth, rate limits, timeouts), OpenClaw will try the CLI backend next.

## Configuration overview

All CLI backends live under:

```
agents.defaults.cliBackends
```

Each entry is keyed by a **provider id** (e.g. `claude-cli`, `my-cli`). The provider id becomes the left side of your model ref:

### Example configuration

```
{
  agents: {
    defaults: {
      cliBackends: {
        "claude-cli": {
          command: "/opt/homebrew/bin/claude",
        },
        "my-cli": {
          command: "my-cli",
          args: ["--json"],
          output: "json",
          input: "arg",
          modelArg: "--model",
          modelAliases: {
            "claude-opus-4-6": "opus",
            "claude-opus-4-5": "opus",
            "claude-sonnet-4-5": "sonnet",
          },
          sessionArg: "--session",
          sessionMode: "existing",
          sessionIdFields: ["session_id", "conversation_id"],
          systemPromptArg: "--system",
          systemPromptWhen: "first",
          imageArg: "--image",
          imageMode: "repeat",
          serialize: true,
        },
      },
    },
  },
}
```

## How it works

1.  **Selects a backend** based on the provider prefix (`claude-cli/...`).
2.  **Builds a system prompt** using the same OpenClaw prompt + workspace context.
3.  **Executes the CLI** with a session id (if supported) so history stays consistent.
4.  **Parses output** (JSON or plain text) and returns the final text.
5.  **Persists session ids** per backend, so follow-ups reuse the same CLI session.

## Sessions

*   If the CLI supports sessions, set `sessionArg` (e.g. `--session-id`) or `sessionArgs` (placeholder `{sessionId}`) when the ID needs to be inserted into multiple flags.
*   If the CLI uses a **resume subcommand** with different flags, set `resumeArgs` (replaces `args` when resuming) and optionally `resumeOutput` (for non-JSON resumes).
*   `sessionMode`:
    *   `always`: always send a session id (new UUID if none stored).
    *   `existing`: only send a session id if one was stored before.
    *   `none`: never send a session id.

## Images (pass-through)

If your CLI accepts image paths, set `imageArg`:

```
imageArg: "--image",
imageMode: "repeat"
```

OpenClaw will write base64 images to temp files. If `imageArg` is set, those paths are passed as CLI args. If `imageArg` is missing, OpenClaw appends the file paths to the prompt (path injection), which is enough for CLIs that auto- load local files from plain paths (Claude Code CLI behavior).

## Inputs / outputs

*   `output: "json"` (default) tries to parse JSON and extract text + session id.
*   `output: "jsonl"` parses JSONL streams (Codex CLI `--json`) and extracts the last agent message plus `thread_id` when present.
*   `output: "text"` treats stdout as the final response.

Input modes:

*   `input: "arg"` (default) passes the prompt as the last CLI arg.
*   `input: "stdin"` sends the prompt via stdin.
*   If the prompt is very long and `maxPromptArgChars` is set, stdin is used.

## Defaults (built-in)

OpenClaw ships a default for `claude-cli`:

*   `command: "claude"`
*   `args: ["-p", "--output-format", "json", "--permission-mode", "bypassPermissions"]`
*   `resumeArgs: ["-p", "--output-format", "json", "--permission-mode", "bypassPermissions", "--resume", "{sessionId}"]`
*   `modelArg: "--model"`
*   `systemPromptArg: "--append-system-prompt"`
*   `sessionArg: "--session-id"`
*   `systemPromptWhen: "first"`
*   `sessionMode: "always"`

OpenClaw also ships a default for `codex-cli`:

*   `command: "codex"`
*   `args: ["exec","--json","--color","never","--sandbox","read-only","--skip-git-repo-check"]`
*   `resumeArgs: ["exec","resume","{sessionId}","--color","never","--sandbox","read-only","--skip-git-repo-check"]`
*   `output: "jsonl"`
*   `resumeOutput: "text"`
*   `modelArg: "--model"`
*   `imageArg: "--image"`
*   `sessionMode: "existing"`

Override only if needed (common: absolute `command` path).

## Limitations

*   **No OpenClaw tools** (the CLI backend never receives tool calls). Some CLIs may still run their own agent tooling.
*   **No streaming** (CLI output is collected then returned).
*   **Structured outputs** depend on the CLI’s JSON format.
*   **Codex CLI sessions** resume via text output (no JSONL), which is less structured than the initial `--json` run. OpenClaw sessions still work normally.

## Troubleshooting

*   **CLI not found**: set `command` to a full path.
*   **Wrong model name**: use `modelAliases` to map `provider/model` → CLI model.
*   **No session continuity**: ensure `sessionArg` is set and `sessionMode` is not `none` (Codex CLI currently cannot resume with JSON output).
*   **Images ignored**: set `imageArg` (and verify CLI supports file paths).

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/local-models -->

# Local Models - OpenClaw

Local is doable, but OpenClaw expects large context + strong defenses against prompt injection. Small cards truncate context and leak safety. Aim high: **≥2 maxed-out Mac Studios or equivalent GPU rig (~$30k+)**. A single **24 GB** GPU works only for lighter prompts with higher latency. Use the **largest / full-size model variant you can run**; aggressively quantized or “small” checkpoints raise prompt-injection risk (see [Security](https://docs.openclaw.ai/gateway/security)).

## Recommended: LM Studio + MiniMax M2.5 (Responses API, full-size)

Best current local stack. Load MiniMax M2.5 in LM Studio, enable the local server (default `http://127.0.0.1:1234`), and use Responses API to keep reasoning separate from final text.

```
{
  agents: {
    defaults: {
      model: { primary: "lmstudio/minimax-m2.5-gs32" },
      models: {
        "anthropic/claude-opus-4-6": { alias: "Opus" },
        "lmstudio/minimax-m2.5-gs32": { alias: "Minimax" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      lmstudio: {
        baseUrl: "http://127.0.0.1:1234/v1",
        apiKey: "lmstudio",
        api: "openai-responses",
        models: [
          {
            id: "minimax-m2.5-gs32",
            name: "MiniMax M2.5 GS32",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 196608,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

**Setup checklist**

*   Install LM Studio: [https://lmstudio.ai](https://lmstudio.ai/)
*   In LM Studio, download the **largest MiniMax M2.5 build available** (avoid “small”/heavily quantized variants), start the server, confirm `http://127.0.0.1:1234/v1/models` lists it.
*   Keep the model loaded; cold-load adds startup latency.
*   Adjust `contextWindow`/`maxTokens` if your LM Studio build differs.
*   For WhatsApp, stick to Responses API so only final text is sent.

Keep hosted models configured even when running local; use `models.mode: "merge"` so fallbacks stay available.

### Hybrid config: hosted primary, local fallback

```
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["lmstudio/minimax-m2.5-gs32", "anthropic/claude-opus-4-6"],
      },
      models: {
        "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
        "lmstudio/minimax-m2.5-gs32": { alias: "MiniMax Local" },
        "anthropic/claude-opus-4-6": { alias: "Opus" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      lmstudio: {
        baseUrl: "http://127.0.0.1:1234/v1",
        apiKey: "lmstudio",
        api: "openai-responses",
        models: [
          {
            id: "minimax-m2.5-gs32",
            name: "MiniMax M2.5 GS32",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 196608,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

### Local-first with hosted safety net

Swap the primary and fallback order; keep the same providers block and `models.mode: "merge"` so you can fall back to Sonnet or Opus when the local box is down.

### Regional hosting / data routing

*   Hosted MiniMax/Kimi/GLM variants also exist on OpenRouter with region-pinned endpoints (e.g., US-hosted). Pick the regional variant there to keep traffic in your chosen jurisdiction while still using `models.mode: "merge"` for Anthropic/OpenAI fallbacks.
*   Local-only remains the strongest privacy path; hosted regional routing is the middle ground when you need provider features but want control over data flow.

## Other OpenAI-compatible local proxies

vLLM, LiteLLM, OAI-proxy, or custom gateways work if they expose an OpenAI-style `/v1` endpoint. Replace the provider block above with your endpoint and model ID:

```
{
  models: {
    mode: "merge",
    providers: {
      local: {
        baseUrl: "http://127.0.0.1:8000/v1",
        apiKey: "sk-local",
        api: "openai-responses",
        models: [
          {
            id: "my-local-model",
            name: "Local Model",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 120000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Keep `models.mode: "merge"` so hosted models stay available as fallbacks.

## Troubleshooting

*   Gateway can reach the proxy? `curl http://127.0.0.1:1234/v1/models`.
*   LM Studio model unloaded? Reload; cold start is a common “hanging” cause.
*   Context errors? Lower `contextWindow` or raise your server limit.
*   Safety: local models skip provider-side filters; keep agents narrow and compaction on to limit prompt injection blast radius.

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/openresponses-http-api -->

# OpenResponses API - OpenClaw

OpenClaw’s Gateway can serve an OpenResponses-compatible `POST /v1/responses` endpoint. This endpoint is **disabled by default**. Enable it in config first.

*   `POST /v1/responses`
*   Same port as the Gateway (WS + HTTP multiplex): `http://<gateway-host>:<port>/v1/responses`

Under the hood, requests are executed as a normal Gateway agent run (same codepath as `openclaw agent`), so routing/permissions/config match your Gateway.

## Authentication

Uses the Gateway auth configuration. Send a bearer token:

*   `Authorization: Bearer <token>`

Notes:

*   When `gateway.auth.mode="token"`, use `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`).
*   When `gateway.auth.mode="password"`, use `gateway.auth.password` (or `OPENCLAW_GATEWAY_PASSWORD`).
*   If `gateway.auth.rateLimit` is configured and too many auth failures occur, the endpoint returns `429` with `Retry-After`.

## Security boundary (important)

Treat this endpoint as a **full operator-access** surface for the gateway instance.

*   HTTP bearer auth here is not a narrow per-user scope model.
*   A valid Gateway token/password for this endpoint should be treated like an owner/operator credential.
*   Requests run through the same control-plane agent path as trusted operator actions.
*   There is no separate non-owner/per-user tool boundary on this endpoint; once a caller passes Gateway auth here, OpenClaw treats that caller as a trusted operator for this gateway.
*   If the target agent policy allows sensitive tools, this endpoint can use them.
*   Keep this endpoint on loopback/tailnet/private ingress only; do not expose it directly to the public internet.

See [Security](https://docs.openclaw.ai/gateway/security) and [Remote access](https://docs.openclaw.ai/gateway/remote).

## Choosing an agent

No custom headers required: encode the agent id in the OpenResponses `model` field:

*   `model: "openclaw:<agentId>"` (example: `"openclaw:main"`, `"openclaw:beta"`)
*   `model: "agent:<agentId>"` (alias)

Or target a specific OpenClaw agent by header:

*   `x-openclaw-agent-id: <agentId>` (default: `main`)

Advanced:

*   `x-openclaw-session-key: <sessionKey>` to fully control session routing.

## Enabling the endpoint

Set `gateway.http.endpoints.responses.enabled` to `true`:

```
{
  gateway: {
    http: {
      endpoints: {
        responses: { enabled: true },
      },
    },
  },
}
```

## Disabling the endpoint

Set `gateway.http.endpoints.responses.enabled` to `false`:

```
{
  gateway: {
    http: {
      endpoints: {
        responses: { enabled: false },
      },
    },
  },
}
```

## Session behavior

By default the endpoint is **stateless per request** (a new session key is generated each call). If the request includes an OpenResponses `user` string, the Gateway derives a stable session key from it, so repeated calls can share an agent session.

## Request shape (supported)

The request follows the OpenResponses API with item-based input. Current support:

*   `input`: string or array of item objects.
*   `instructions`: merged into the system prompt.
*   `tools`: client tool definitions (function tools).
*   `tool_choice`: filter or require client tools.
*   `stream`: enables SSE streaming.
*   `max_output_tokens`: best-effort output limit (provider dependent).
*   `user`: stable session routing.

Accepted but **currently ignored**:

*   `max_tool_calls`
*   `reasoning`
*   `metadata`
*   `store`
*   `previous_response_id`
*   `truncation`

## Items (input)

### `message`

Roles: `system`, `developer`, `user`, `assistant`.

*   `system` and `developer` are appended to the system prompt.
*   The most recent `user` or `function_call_output` item becomes the “current message.”
*   Earlier user/assistant messages are included as history for context.

### `function_call_output` (turn-based tools)

Send tool results back to the model:

```
{
  "type": "function_call_output",
  "call_id": "call_123",
  "output": "{\"temperature\": \"72F\"}"
}
```

### `reasoning` and `item_reference`

Accepted for schema compatibility but ignored when building the prompt.

Provide tools with `tools: [{ type: "function", function: { name, description?, parameters? } }]`. If the agent decides to call a tool, the response returns a `function_call` output item. You then send a follow-up request with `function_call_output` to continue the turn.

## Images (`input_image`)

Supports base64 or URL sources:

```
{
  "type": "input_image",
  "source": { "type": "url", "url": "https://example.com/image.png" }
}
```

Allowed MIME types (current): `image/jpeg`, `image/png`, `image/gif`, `image/webp`, `image/heic`, `image/heif`. Max size (current): 10MB.

## Files (`input_file`)

Supports base64 or URL sources:

```
{
  "type": "input_file",
  "source": {
    "type": "base64",
    "media_type": "text/plain",
    "data": "SGVsbG8gV29ybGQh",
    "filename": "hello.txt"
  }
}
```

Allowed MIME types (current): `text/plain`, `text/markdown`, `text/html`, `text/csv`, `application/json`, `application/pdf`. Max size (current): 5MB. Current behavior:

*   File content is decoded and added to the **system prompt**, not the user message, so it stays ephemeral (not persisted in session history).
*   PDFs are parsed for text. If little text is found, the first pages are rasterized into images and passed to the model.

PDF parsing uses the Node-friendly `pdfjs-dist` legacy build (no worker). The modern PDF.js build expects browser workers/DOM globals, so it is not used in the Gateway. URL fetch defaults:

*   `files.allowUrl`: `true`
*   `images.allowUrl`: `true`
*   `maxUrlParts`: `8` (total URL-based `input_file` + `input_image` parts per request)
*   Requests are guarded (DNS resolution, private IP blocking, redirect caps, timeouts).
*   Optional hostname allowlists are supported per input type (`files.urlAllowlist`, `images.urlAllowlist`).
    *   Exact host: `"cdn.example.com"`
    *   Wildcard subdomains: `"*.assets.example.com"` (does not match apex)

## File + image limits (config)

Defaults can be tuned under `gateway.http.endpoints.responses`:

```
{
  gateway: {
    http: {
      endpoints: {
        responses: {
          enabled: true,
          maxBodyBytes: 20000000,
          maxUrlParts: 8,
          files: {
            allowUrl: true,
            urlAllowlist: ["cdn.example.com", "*.assets.example.com"],
            allowedMimes: [
              "text/plain",
              "text/markdown",
              "text/html",
              "text/csv",
              "application/json",
              "application/pdf",
            ],
            maxBytes: 5242880,
            maxChars: 200000,
            maxRedirects: 3,
            timeoutMs: 10000,
            pdf: {
              maxPages: 4,
              maxPixels: 4000000,
              minTextChars: 200,
            },
          },
          images: {
            allowUrl: true,
            urlAllowlist: ["images.example.com"],
            allowedMimes: [
              "image/jpeg",
              "image/png",
              "image/gif",
              "image/webp",
              "image/heic",
              "image/heif",
            ],
            maxBytes: 10485760,
            maxRedirects: 3,
            timeoutMs: 10000,
          },
        },
      },
    },
  },
}
```

Defaults when omitted:

*   `maxBodyBytes`: 20MB
*   `maxUrlParts`: 8
*   `files.maxBytes`: 5MB
*   `files.maxChars`: 200k
*   `files.maxRedirects`: 3
*   `files.timeoutMs`: 10s
*   `files.pdf.maxPages`: 4
*   `files.pdf.maxPixels`: 4,000,000
*   `files.pdf.minTextChars`: 200
*   `images.maxBytes`: 10MB
*   `images.maxRedirects`: 3
*   `images.timeoutMs`: 10s
*   HEIC/HEIF `input_image` sources are accepted and normalized to JPEG before provider delivery.

Security note:

*   URL allowlists are enforced before fetch and on redirect hops.
*   Allowlisting a hostname does not bypass private/internal IP blocking.
*   For internet-exposed gateways, apply network egress controls in addition to app-level guards. See [Security](https://docs.openclaw.ai/gateway/security).

## Streaming (SSE)

Set `stream: true` to receive Server-Sent Events (SSE):

*   `Content-Type: text/event-stream`
*   Each event line is `event: <type>` and `data: <json>`
*   Stream ends with `data: [DONE]`

Event types currently emitted:

*   `response.created`
*   `response.in_progress`
*   `response.output_item.added`
*   `response.content_part.added`
*   `response.output_text.delta`
*   `response.output_text.done`
*   `response.content_part.done`
*   `response.output_item.done`
*   `response.completed`
*   `response.failed` (on error)

## Usage

`usage` is populated when the underlying provider reports token counts.

## Errors

Errors use a JSON object like:

```
{ "error": { "message": "...", "type": "invalid_request_error" } }
```

Common cases:

*   `401` missing/invalid auth
*   `400` invalid request body
*   `405` wrong method

## Examples

Non-streaming:

```
curl -sS http://127.0.0.1:18789/v1/responses \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "input": "hi"
  }'
```

Streaming:

```
curl -N http://127.0.0.1:18789/v1/responses \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "stream": true,
    "input": "hi"
  }'
```

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/discovery -->

# Discovery and Transports - OpenClaw

OpenClaw has two distinct problems that look similar on the surface:

1.  **Operator remote control**: the macOS menu bar app controlling a gateway running elsewhere.
2.  **Node pairing**: iOS/Android (and future nodes) finding a gateway and pairing securely.

The design goal is to keep all network discovery/advertising in the **Node Gateway** (`openclaw gateway`) and keep clients (mac app, iOS) as consumers.

## Terms

*   **Gateway**: a single long-running gateway process that owns state (sessions, pairing, node registry) and runs channels. Most setups use one per host; isolated multi-gateway setups are possible.
*   **Gateway WS (control plane)**: the WebSocket endpoint on `127.0.0.1:18789` by default; can be bound to LAN/tailnet via `gateway.bind`.
*   **Direct WS transport**: a LAN/tailnet-facing Gateway WS endpoint (no SSH).
*   **SSH transport (fallback)**: remote control by forwarding `127.0.0.1:18789` over SSH.
*   **Legacy TCP bridge (deprecated/removed)**: older node transport (see [Bridge protocol](https://docs.openclaw.ai/gateway/bridge-protocol)); no longer advertised for discovery.

Protocol details:

*   [Gateway protocol](https://docs.openclaw.ai/gateway/protocol)
*   [Bridge protocol (legacy)](https://docs.openclaw.ai/gateway/bridge-protocol)

## Why we keep both “direct” and SSH

*   **Direct WS** is the best UX on the same network and within a tailnet:
    *   auto-discovery on LAN via Bonjour
    *   pairing tokens + ACLs owned by the gateway
    *   no shell access required; protocol surface can stay tight and auditable
*   **SSH** remains the universal fallback:
    *   works anywhere you have SSH access (even across unrelated networks)
    *   survives multicast/mDNS issues
    *   requires no new inbound ports besides SSH

## Discovery inputs (how clients learn where the gateway is)

### 1) Bonjour / mDNS (LAN only)

Bonjour is best-effort and does not cross networks. It is only used for “same LAN” convenience. Target direction:

*   The **gateway** advertises its WS endpoint via Bonjour.
*   Clients browse and show a “pick a gateway” list, then store the chosen endpoint.

Troubleshooting and beacon details: [Bonjour](https://docs.openclaw.ai/gateway/bonjour).

#### Service beacon details

*   Service types:
    *   `_openclaw-gw._tcp` (gateway transport beacon)
*   TXT keys (non-secret):
    *   `role=gateway`
    *   `lanHost=<hostname>.local`
    *   `sshPort=22` (or whatever is advertised)
    *   `gatewayPort=18789` (Gateway WS + HTTP)
    *   `gatewayTls=1` (only when TLS is enabled)
    *   `gatewayTlsSha256=<sha256>` (only when TLS is enabled and fingerprint is available)
    *   `canvasPort=<port>` (canvas host port; currently the same as `gatewayPort` when the canvas host is enabled)
    *   `cliPath=<path>` (optional; absolute path to a runnable `openclaw` entrypoint or binary)
    *   `tailnetDns=<magicdns>` (optional hint; auto-detected when Tailscale is available)

Security notes:

*   Bonjour/mDNS TXT records are **unauthenticated**. Clients must treat TXT values as UX hints only.
*   Routing (host/port) should prefer the **resolved service endpoint** (SRV + A/AAAA) over TXT-provided `lanHost`, `tailnetDns`, or `gatewayPort`.
*   TLS pinning must never allow an advertised `gatewayTlsSha256` to override a previously stored pin.
*   iOS/Android nodes should treat discovery-based direct connects as **TLS-only** and require an explicit “trust this fingerprint” confirmation before storing a first-time pin (out-of-band verification).

Disable/override:

*   `OPENCLAW_DISABLE_BONJOUR=1` disables advertising.
*   `gateway.bind` in `~/.openclaw/openclaw.json` controls the Gateway bind mode.
*   `OPENCLAW_SSH_PORT` overrides the SSH port advertised in TXT (defaults to 22).
*   `OPENCLAW_TAILNET_DNS` publishes a `tailnetDns` hint (MagicDNS).
*   `OPENCLAW_CLI_PATH` overrides the advertised CLI path.

### 2) Tailnet (cross-network)

For London/Vienna style setups, Bonjour won’t help. The recommended “direct” target is:

*   Tailscale MagicDNS name (preferred) or a stable tailnet IP.

If the gateway can detect it is running under Tailscale, it publishes `tailnetDns` as an optional hint for clients (including wide-area beacons).

### 3) Manual / SSH target

When there is no direct route (or direct is disabled), clients can always connect via SSH by forwarding the loopback gateway port. See [Remote access](https://docs.openclaw.ai/gateway/remote).

## Transport selection (client policy)

Recommended client behavior:

1.  If a paired direct endpoint is configured and reachable, use it.
2.  Else, if Bonjour finds a gateway on LAN, offer a one-tap “Use this gateway” choice and save it as the direct endpoint.
3.  Else, if a tailnet DNS/IP is configured, try direct.
4.  Else, fall back to SSH.

## Pairing + auth (direct transport)

The gateway is the source of truth for node/client admission.

*   Pairing requests are created/approved/rejected in the gateway (see [Gateway pairing](https://docs.openclaw.ai/gateway/pairing)).
*   The gateway enforces:
    *   auth (token / keypair)
    *   scopes/ACLs (the gateway is not a raw proxy to every method)
    *   rate limits

## Responsibilities by component

*   **Gateway**: advertises discovery beacons, owns pairing decisions, and hosts the WS endpoint.
*   **macOS app**: helps you pick a gateway, shows pairing prompts, and uses SSH only as a fallback.
*   **iOS/Android nodes**: browse Bonjour as a convenience and connect to the paired Gateway WS.

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/pairing -->

# Gateway-Owned Pairing - OpenClaw

## Gateway-owned pairing (Option B)

In Gateway-owned pairing, the **Gateway** is the source of truth for which nodes are allowed to join. UIs (macOS app, future clients) are just frontends that approve or reject pending requests. **Important:** WS nodes use **device pairing** (role `node`) during `connect`. `node.pair.*` is a separate pairing store and does **not** gate the WS handshake. Only clients that explicitly call `node.pair.*` use this flow.

## Concepts

*   **Pending request**: a node asked to join; requires approval.
*   **Paired node**: approved node with an issued auth token.
*   **Transport**: the Gateway WS endpoint forwards requests but does not decide membership. (Legacy TCP bridge support is deprecated/removed.)

## How pairing works

1.  A node connects to the Gateway WS and requests pairing.
2.  The Gateway stores a **pending request** and emits `node.pair.requested`.
3.  You approve or reject the request (CLI or UI).
4.  On approval, the Gateway issues a **new token** (tokens are rotated on re‑pair).
5.  The node reconnects using the token and is now “paired”.

Pending requests expire automatically after **5 minutes**.

## CLI workflow (headless friendly)

```
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes reject <requestId>
openclaw nodes status
openclaw nodes rename --node <id|name|ip> --name "Living Room iPad"
```

`nodes status` shows paired/connected nodes and their capabilities.

## API surface (gateway protocol)

Events:

*   `node.pair.requested` — emitted when a new pending request is created.
*   `node.pair.resolved` — emitted when a request is approved/rejected/expired.

Methods:

*   `node.pair.request` — create or reuse a pending request.
*   `node.pair.list` — list pending + paired nodes.
*   `node.pair.approve` — approve a pending request (issues token).
*   `node.pair.reject` — reject a pending request.
*   `node.pair.verify` — verify `{ nodeId, token }`.

Notes:

*   `node.pair.request` is idempotent per node: repeated calls return the same pending request.
*   Approval **always** generates a fresh token; no token is ever returned from `node.pair.request`.
*   Requests may include `silent: true` as a hint for auto-approval flows.

## Auto-approval (macOS app)

The macOS app can optionally attempt a **silent approval** when:

*   the request is marked `silent`, and
*   the app can verify an SSH connection to the gateway host using the same user.

If silent approval fails, it falls back to the normal “Approve/Reject” prompt.

## Storage (local, private)

Pairing state is stored under the Gateway state directory (default `~/.openclaw`):

*   `~/.openclaw/nodes/paired.json`
*   `~/.openclaw/nodes/pending.json`

If you override `OPENCLAW_STATE_DIR`, the `nodes/` folder moves with it. Security notes:

*   Tokens are secrets; treat `paired.json` as sensitive.
*   Rotating a token requires re-approval (or deleting the node entry).

## Transport behavior

*   The transport is **stateless**; it does not store membership.
*   If the Gateway is offline or pairing is disabled, nodes cannot pair.
*   If the Gateway is in remote mode, pairing still happens against the remote Gateway’s store.

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/remote-gateway-readme -->

# Remote Gateway Setup - OpenClaw

## Running OpenClaw.app with a Remote Gateway

OpenClaw.app uses SSH tunneling to connect to a remote gateway. This guide shows you how to set it up.

## Overview

## Quick Setup

### Step 1: Add SSH Config

Edit `~/.ssh/config` and add:

```
Host remote-gateway
    HostName <REMOTE_IP>          # e.g., 172.27.187.184
    User <REMOTE_USER>            # e.g., jefferson
    LocalForward 18789 127.0.0.1:18789
    IdentityFile ~/.ssh/id_rsa
```

Replace `<REMOTE_IP>` and `<REMOTE_USER>` with your values.

### Step 2: Copy SSH Key

Copy your public key to the remote machine (enter password once):

```
ssh-copy-id -i ~/.ssh/id_rsa <REMOTE_USER>@<REMOTE_IP>
```

### Step 3: Set Gateway Token

```
launchctl setenv OPENCLAW_GATEWAY_TOKEN "<your-token>"
```

### Step 4: Start SSH Tunnel

### Step 5: Restart OpenClaw.app

```
# Quit OpenClaw.app (⌘Q), then reopen:
open /path/to/OpenClaw.app
```

The app will now connect to the remote gateway through the SSH tunnel.

* * *

## Auto-Start Tunnel on Login

To have the SSH tunnel start automatically when you log in, create a Launch Agent.

### Create the PLIST file

Save this as `~/Library/LaunchAgents/ai.openclaw.ssh-tunnel.plist`:

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.openclaw.ssh-tunnel</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/ssh</string>
        <string>-N</string>
        <string>remote-gateway</string>
    </array>
    <key>KeepAlive</key>
    <true/>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

### Load the Launch Agent

```
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.openclaw.ssh-tunnel.plist
```

The tunnel will now:

*   Start automatically when you log in
*   Restart if it crashes
*   Keep running in the background

Legacy note: remove any leftover `com.openclaw.ssh-tunnel` LaunchAgent if present.

* * *

## Troubleshooting

**Check if tunnel is running:**

```
ps aux | grep "ssh -N remote-gateway" | grep -v grep
lsof -i :18789
```

**Restart the tunnel:**

```
launchctl kickstart -k gui/$UID/ai.openclaw.ssh-tunnel
```

**Stop the tunnel:**

```
launchctl bootout gui/$UID/ai.openclaw.ssh-tunnel
```

* * *

## How It Works

| Component | What It Does |
| --- | --- |
| `LocalForward 18789 127.0.0.1:18789` | Forwards local port 18789 to remote port 18789 |
| `ssh -N` | SSH without executing remote commands (just port forwarding) |
| `KeepAlive` | Automatically restarts tunnel if it crashes |
| `RunAtLoad` | Starts tunnel when the agent loads |

OpenClaw.app connects to `ws://127.0.0.1:18789` on your client machine. The SSH tunnel forwards that connection to port 18789 on the remote machine where the Gateway is running.

---

<!-- SOURCE: https://docs.openclaw.ai/gateway/bonjour -->

# Bonjour Discovery - OpenClaw

OpenClaw uses Bonjour (mDNS / DNS‑SD) as a **LAN‑only convenience** to discover an active Gateway (WebSocket endpoint). It is best‑effort and does **not** replace SSH or Tailnet-based connectivity.

## Wide‑area Bonjour (Unicast DNS‑SD) over Tailscale

If the node and gateway are on different networks, multicast mDNS won’t cross the boundary. You can keep the same discovery UX by switching to **unicast DNS‑SD** (“Wide‑Area Bonjour”) over Tailscale. High‑level steps:

1.  Run a DNS server on the gateway host (reachable over Tailnet).
2.  Publish DNS‑SD records for `_openclaw-gw._tcp` under a dedicated zone (example: `openclaw.internal.`).
3.  Configure Tailscale **split DNS** so your chosen domain resolves via that DNS server for clients (including iOS).

OpenClaw supports any discovery domain; `openclaw.internal.` is just an example. iOS/Android nodes browse both `local.` and your configured wide‑area domain.

### Gateway config (recommended)

```
{
  gateway: { bind: "tailnet" }, // tailnet-only (recommended)
  discovery: { wideArea: { enabled: true } }, // enables wide-area DNS-SD publishing
}
```

### One‑time DNS server setup (gateway host)

```
openclaw dns setup --apply
```

This installs CoreDNS and configures it to:

*   listen on port 53 only on the gateway’s Tailscale interfaces
*   serve your chosen domain (example: `openclaw.internal.`) from `~/.openclaw/dns/<domain>.db`

Validate from a tailnet‑connected machine:

```
dns-sd -B _openclaw-gw._tcp openclaw.internal.
dig @<TAILNET_IPV4> -p 53 _openclaw-gw._tcp.openclaw.internal PTR +short
```

### Tailscale DNS settings

In the Tailscale admin console:

*   Add a nameserver pointing at the gateway’s tailnet IP (UDP/TCP 53).
*   Add split DNS so your discovery domain uses that nameserver.

Once clients accept tailnet DNS, iOS nodes can browse `_openclaw-gw._tcp` in your discovery domain without multicast.

### Gateway listener security (recommended)

The Gateway WS port (default `18789`) binds to loopback by default. For LAN/tailnet access, bind explicitly and keep auth enabled. For tailnet‑only setups:

*   Set `gateway.bind: "tailnet"` in `~/.openclaw/openclaw.json`.
*   Restart the Gateway (or restart the macOS menubar app).

## What advertises

Only the Gateway advertises `_openclaw-gw._tcp`.

## Service types

*   `_openclaw-gw._tcp` — gateway transport beacon (used by macOS/iOS/Android nodes).

## TXT keys (non‑secret hints)

The Gateway advertises small non‑secret hints to make UI flows convenient:

*   `role=gateway`
*   `displayName=<friendly name>`
*   `lanHost=<hostname>.local`
*   `gatewayPort=<port>` (Gateway WS + HTTP)
*   `gatewayTls=1` (only when TLS is enabled)
*   `gatewayTlsSha256=<sha256>` (only when TLS is enabled and fingerprint is available)
*   `canvasPort=<port>` (only when the canvas host is enabled; currently the same as `gatewayPort`)
*   `sshPort=<port>` (defaults to 22 when not overridden)
*   `transport=gateway`
*   `cliPath=<path>` (optional; absolute path to a runnable `openclaw` entrypoint)
*   `tailnetDns=<magicdns>` (optional hint when Tailnet is available)

Security notes:

*   Bonjour/mDNS TXT records are **unauthenticated**. Clients must not treat TXT as authoritative routing.
*   Clients should route using the resolved service endpoint (SRV + A/AAAA). Treat `lanHost`, `tailnetDns`, `gatewayPort`, and `gatewayTlsSha256` as hints only.
*   TLS pinning must never allow an advertised `gatewayTlsSha256` to override a previously stored pin.
*   iOS/Android nodes should treat discovery-based direct connects as **TLS-only** and require explicit user confirmation before trusting a first-time fingerprint.

## Debugging on macOS

Useful built‑in tools:

*   Browse instances:
    
    ```
    dns-sd -B _openclaw-gw._tcp local.
    ```
    
*   Resolve one instance (replace `<instance>`):
    
    ```
    dns-sd -L "<instance>" _openclaw-gw._tcp local.
    ```
    

If browsing works but resolving fails, you’re usually hitting a LAN policy or mDNS resolver issue.

## Debugging in Gateway logs

The Gateway writes a rolling log file (printed on startup as `gateway log file: ...`). Look for `bonjour:` lines, especially:

*   `bonjour: advertise failed ...`
*   `bonjour: ... name conflict resolved` / `hostname conflict resolved`
*   `bonjour: watchdog detected non-announced service ...`

## Debugging on iOS node

The iOS node uses `NWBrowser` to discover `_openclaw-gw._tcp`. To capture logs:

*   Settings → Gateway → Advanced → **Discovery Debug Logs**
*   Settings → Gateway → Advanced → **Discovery Logs** → reproduce → **Copy**

The log includes browser state transitions and result‑set changes.

## Common failure modes

*   **Bonjour doesn’t cross networks**: use Tailnet or SSH.
*   **Multicast blocked**: some Wi‑Fi networks disable mDNS.
*   **Sleep / interface churn**: macOS may temporarily drop mDNS results; retry.
*   **Browse works but resolve fails**: keep machine names simple (avoid emojis or punctuation), then restart the Gateway. The service instance name derives from the host name, so overly complex names can confuse some resolvers.

## Escaped instance names (`\032`)

Bonjour/DNS‑SD often escapes bytes in service instance names as decimal `\DDD` sequences (e.g. spaces become `\032`).

*   This is normal at the protocol level.
*   UIs should decode for display (iOS uses `BonjourEscapes.decode`).

## Disabling / configuration

*   `OPENCLAW_DISABLE_BONJOUR=1` disables advertising (legacy: `OPENCLAW_DISABLE_BONJOUR`).
*   `gateway.bind` in `~/.openclaw/openclaw.json` controls the Gateway bind mode.
*   `OPENCLAW_SSH_PORT` overrides the SSH port advertised in TXT (legacy: `OPENCLAW_SSH_PORT`).
*   `OPENCLAW_TAILNET_DNS` publishes a MagicDNS hint in TXT (legacy: `OPENCLAW_TAILNET_DNS`).
*   `OPENCLAW_CLI_PATH` overrides the advertised CLI path (legacy: `OPENCLAW_CLI_PATH`).

*   Discovery policy and transport selection: [Discovery](https://docs.openclaw.ai/gateway/discovery)
*   Node pairing + approvals: [Gateway pairing](https://docs.openclaw.ai/gateway/pairing)

---

<!-- SOURCE: https://docs.openclaw.ai/gateway -->

# Gateway Runbook - OpenClaw

Use this page for day-1 startup and day-2 operations of the Gateway service.

## 5-minute local startup

## Runtime model

*   One always-on process for routing, control plane, and channel connections.
*   Single multiplexed port for:
    *   WebSocket control/RPC
    *   HTTP APIs (OpenAI-compatible, Responses, tools invoke)
    *   Control UI and hooks
*   Default bind mode: `loopback`.
*   Auth is required by default (`gateway.auth.token` / `gateway.auth.password`, or `OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD`).

### Port and bind precedence

| Setting | Resolution order |
| --- | --- |
| Gateway port | `--port` → `OPENCLAW_GATEWAY_PORT` → `gateway.port` → `18789` |
| Bind mode | CLI/override → `gateway.bind` → `loopback` |

### Hot reload modes

| `gateway.reload.mode` | Behavior |
| --- | --- |
| `off` | No config reload |
| `hot` | Apply only hot-safe changes |
| `restart` | Restart on reload-required changes |
| `hybrid` (default) | Hot-apply when safe, restart when required |

## Operator command set

```
openclaw gateway status
openclaw gateway status --deep
openclaw gateway status --json
openclaw gateway install
openclaw gateway restart
openclaw gateway stop
openclaw secrets reload
openclaw logs --follow
openclaw doctor
```

## Remote access

Preferred: Tailscale/VPN. Fallback: SSH tunnel.

```
ssh -N -L 18789:127.0.0.1:18789 user@host
```

Then connect clients to `ws://127.0.0.1:18789` locally.

See: [Remote Gateway](https://docs.openclaw.ai/gateway/remote), [Authentication](https://docs.openclaw.ai/gateway/authentication), [Tailscale](https://docs.openclaw.ai/gateway/tailscale).

## Supervision and service lifecycle

Use supervised runs for production-like reliability.

*   macOS (launchd)
    
*   Linux (systemd user)
    
*   Linux (system service)
    

```
openclaw gateway install
openclaw gateway status
openclaw gateway restart
openclaw gateway stop
```

LaunchAgent labels are `ai.openclaw.gateway` (default) or `ai.openclaw.<profile>` (named profile). `openclaw doctor` audits and repairs service config drift.

```
openclaw gateway install
systemctl --user enable --now openclaw-gateway[-<profile>].service
openclaw gateway status
```

For persistence after logout, enable lingering:

```
sudo loginctl enable-linger <user>
```

Use a system unit for multi-user/always-on hosts.

```
sudo systemctl daemon-reload
sudo systemctl enable --now openclaw-gateway[-<profile>].service
```

## Multiple gateways on one host

Most setups should run **one** Gateway. Use multiple only for strict isolation/redundancy (for example a rescue profile). Checklist per instance:

*   Unique `gateway.port`
*   Unique `OPENCLAW_CONFIG_PATH`
*   Unique `OPENCLAW_STATE_DIR`
*   Unique `agents.defaults.workspace`

Example:

```
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json OPENCLAW_STATE_DIR=~/.openclaw-a openclaw gateway --port 19001
OPENCLAW_CONFIG_PATH=~/.openclaw/b.json OPENCLAW_STATE_DIR=~/.openclaw-b openclaw gateway --port 19002
```

See: [Multiple gateways](https://docs.openclaw.ai/gateway/multiple-gateways).

### Dev profile quick path

```
openclaw --dev setup
openclaw --dev gateway --allow-unconfigured
openclaw --dev status
```

Defaults include isolated state/config and base gateway port `19001`.

## Protocol quick reference (operator view)

*   First client frame must be `connect`.
*   Gateway returns `hello-ok` snapshot (`presence`, `health`, `stateVersion`, `uptimeMs`, limits/policy).
*   Requests: `req(method, params)` → `res(ok/payload|error)`.
*   Common events: `connect.challenge`, `agent`, `chat`, `presence`, `tick`, `health`, `heartbeat`, `shutdown`.

Agent runs are two-stage:

1.  Immediate accepted ack (`status:"accepted"`)
2.  Final completion response (`status:"ok"|"error"`), with streamed `agent` events in between.

See full protocol docs: [Gateway Protocol](https://docs.openclaw.ai/gateway/protocol).

## Operational checks

### Liveness

*   Open WS and send `connect`.
*   Expect `hello-ok` response with snapshot.

### Readiness

```
openclaw gateway status
openclaw channels status --probe
openclaw health
```

### Gap recovery

Events are not replayed. On sequence gaps, refresh state (`health`, `system-presence`) before continuing.

## Common failure signatures

| Signature | Likely issue |
| --- | --- |
| `refusing to bind gateway ... without auth` | Non-loopback bind without token/password |
| `another gateway instance is already listening` / `EADDRINUSE` | Port conflict |
| `Gateway start blocked: set gateway.mode=local` | Config set to remote mode |
| `unauthorized` during connect | Auth mismatch between client and gateway |

For full diagnosis ladders, use [Gateway Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting).

## Safety guarantees

*   Gateway protocol clients fail fast when Gateway is unavailable (no implicit direct-channel fallback).
*   Invalid/non-connect first frames are rejected and closed.
*   Graceful shutdown emits `shutdown` event before socket close.

* * *

Related:

*   [Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting)
*   [Background Process](https://docs.openclaw.ai/gateway/background-process)
*   [Configuration](https://docs.openclaw.ai/gateway/configuration)
*   [Health](https://docs.openclaw.ai/gateway/health)
*   [Doctor](https://docs.openclaw.ai/gateway/doctor)
*   [Authentication](https://docs.openclaw.ai/gateway/authentication)

---

<!-- SOURCE: https://docs.openclaw.ai/network -->

# Network - OpenClaw

## Network hub

This hub links the core docs for how OpenClaw connects, pairs, and secures devices across localhost, LAN, and tailnet.

## Core model

*   [Gateway architecture](https://docs.openclaw.ai/concepts/architecture)
*   [Gateway protocol](https://docs.openclaw.ai/gateway/protocol)
*   [Gateway runbook](https://docs.openclaw.ai/gateway)
*   [Web surfaces + bind modes](https://docs.openclaw.ai/web)

## Pairing + identity

*   [Pairing overview (DM + nodes)](https://docs.openclaw.ai/channels/pairing)
*   [Gateway-owned node pairing](https://docs.openclaw.ai/gateway/pairing)
*   [Devices CLI (pairing + token rotation)](https://docs.openclaw.ai/cli/devices)
*   [Pairing CLI (DM approvals)](https://docs.openclaw.ai/cli/pairing)

Local trust:

*   Local connections (loopback or the gateway host’s own tailnet address) can be auto‑approved for pairing to keep same‑host UX smooth.
*   Non‑local tailnet/LAN clients still require explicit pairing approval.

## Discovery + transports

*   [Discovery & transports](https://docs.openclaw.ai/gateway/discovery)
*   [Bonjour / mDNS](https://docs.openclaw.ai/gateway/bonjour)
*   [Remote access (SSH)](https://docs.openclaw.ai/gateway/remote)
*   [Tailscale](https://docs.openclaw.ai/gateway/tailscale)

## Nodes + transports

*   [Nodes overview](https://docs.openclaw.ai/nodes)
*   [Bridge protocol (legacy nodes)](https://docs.openclaw.ai/gateway/bridge-protocol)
*   [Node runbook: iOS](https://docs.openclaw.ai/platforms/ios)
*   [Node runbook: Android](https://docs.openclaw.ai/platforms/android)

## Security

*   [Security overview](https://docs.openclaw.ai/gateway/security)
*   [Gateway config reference](https://docs.openclaw.ai/gateway/configuration)
*   [Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting)
*   [Doctor](https://docs.openclaw.ai/gateway/doctor)

---

<!-- SOURCE: https://docs.openclaw.ai/logging -->

# Logging - OpenClaw

OpenClaw logs in two places:

*   **File logs** (JSON lines) written by the Gateway.
*   **Console output** shown in terminals and the Control UI.

This page explains where logs live, how to read them, and how to configure log levels and formats.

## Where logs live

By default, the Gateway writes a rolling log file under: `/tmp/openclaw/openclaw-YYYY-MM-DD.log` The date uses the gateway host’s local timezone. You can override this in `~/.openclaw/openclaw.json`:

```
{
  "logging": {
    "file": "/path/to/openclaw.log"
  }
}
```

## How to read logs

### CLI: live tail (recommended)

Use the CLI to tail the gateway log file via RPC:

Output modes:

*   **TTY sessions**: pretty, colorized, structured log lines.
*   **Non-TTY sessions**: plain text.
*   `--json`: line-delimited JSON (one log event per line).
*   `--plain`: force plain text in TTY sessions.
*   `--no-color`: disable ANSI colors.

In JSON mode, the CLI emits `type`\-tagged objects:

*   `meta`: stream metadata (file, cursor, size)
*   `log`: parsed log entry
*   `notice`: truncation / rotation hints
*   `raw`: unparsed log line

If the Gateway is unreachable, the CLI prints a short hint to run:

### Control UI (web)

The Control UI’s **Logs** tab tails the same file using `logs.tail`. See [/web/control-ui](https://docs.openclaw.ai/web/control-ui) for how to open it.

### Channel-only logs

To filter channel activity (WhatsApp/Telegram/etc), use:

```
openclaw channels logs --channel whatsapp
```

## Log formats

### File logs (JSONL)

Each line in the log file is a JSON object. The CLI and Control UI parse these entries to render structured output (time, level, subsystem, message).

### Console output

Console logs are **TTY-aware** and formatted for readability:

*   Subsystem prefixes (e.g. `gateway/channels/whatsapp`)
*   Level coloring (info/warn/error)
*   Optional compact or JSON mode

Console formatting is controlled by `logging.consoleStyle`.

## Configuring logging

All logging configuration lives under `logging` in `~/.openclaw/openclaw.json`.

```
{
  "logging": {
    "level": "info",
    "file": "/tmp/openclaw/openclaw-YYYY-MM-DD.log",
    "consoleLevel": "info",
    "consoleStyle": "pretty",
    "redactSensitive": "tools",
    "redactPatterns": ["sk-.*"]
  }
}
```

### Log levels

*   `logging.level`: **file logs** (JSONL) level.
*   `logging.consoleLevel`: **console** verbosity level.

You can override both via the **`OPENCLAW_LOG_LEVEL`** environment variable (e.g. `OPENCLAW_LOG_LEVEL=debug`). The env var takes precedence over the config file, so you can raise verbosity for a single run without editing `openclaw.json`. You can also pass the global CLI option **`--log-level <level>`** (for example, `openclaw --log-level debug gateway run`), which overrides the environment variable for that command. `--verbose` only affects console output; it does not change file log levels.

### Console styles

`logging.consoleStyle`:

*   `pretty`: human-friendly, colored, with timestamps.
*   `compact`: tighter output (best for long sessions).
*   `json`: JSON per line (for log processors).

### Redaction

Tool summaries can redact sensitive tokens before they hit the console:

*   `logging.redactSensitive`: `off` | `tools` (default: `tools`)
*   `logging.redactPatterns`: list of regex strings to override the default set

Redaction affects **console output only** and does not alter file logs.

## Diagnostics + OpenTelemetry

Diagnostics are structured, machine-readable events for model runs **and** message-flow telemetry (webhooks, queueing, session state). They do **not** replace logs; they exist to feed metrics, traces, and other exporters. Diagnostics events are emitted in-process, but exporters only attach when diagnostics + the exporter plugin are enabled.

### OpenTelemetry vs OTLP

*   **OpenTelemetry (OTel)**: the data model + SDKs for traces, metrics, and logs.
*   **OTLP**: the wire protocol used to export OTel data to a collector/backend.
*   OpenClaw exports via **OTLP/HTTP (protobuf)** today.

### Signals exported

*   **Metrics**: counters + histograms (token usage, message flow, queueing).
*   **Traces**: spans for model usage + webhook/message processing.
*   **Logs**: exported over OTLP when `diagnostics.otel.logs` is enabled. Log volume can be high; keep `logging.level` and exporter filters in mind.

### Diagnostic event catalog

Model usage:

*   `model.usage`: tokens, cost, duration, context, provider/model/channel, session ids.

Message flow:

*   `webhook.received`: webhook ingress per channel.
*   `webhook.processed`: webhook handled + duration.
*   `webhook.error`: webhook handler errors.
*   `message.queued`: message enqueued for processing.
*   `message.processed`: outcome + duration + optional error.

Queue + session:

*   `queue.lane.enqueue`: command queue lane enqueue + depth.
*   `queue.lane.dequeue`: command queue lane dequeue + wait time.
*   `session.state`: session state transition + reason.
*   `session.stuck`: session stuck warning + age.
*   `run.attempt`: run retry/attempt metadata.
*   `diagnostic.heartbeat`: aggregate counters (webhooks/queue/session).

### Enable diagnostics (no exporter)

Use this if you want diagnostics events available to plugins or custom sinks:

```
{
  "diagnostics": {
    "enabled": true
  }
}
```

### Diagnostics flags (targeted logs)

Use flags to turn on extra, targeted debug logs without raising `logging.level`. Flags are case-insensitive and support wildcards (e.g. `telegram.*` or `*`).

```
{
  "diagnostics": {
    "flags": ["telegram.http"]
  }
}
```

Env override (one-off):

```
OPENCLAW_DIAGNOSTICS=telegram.http,telegram.payload
```

Notes:

*   Flag logs go to the standard log file (same as `logging.file`).
*   Output is still redacted according to `logging.redactSensitive`.
*   Full guide: [/diagnostics/flags](https://docs.openclaw.ai/diagnostics/flags).

### Export to OpenTelemetry

Diagnostics can be exported via the `diagnostics-otel` plugin (OTLP/HTTP). This works with any OpenTelemetry collector/backend that accepts OTLP/HTTP.

```
{
  "plugins": {
    "allow": ["diagnostics-otel"],
    "entries": {
      "diagnostics-otel": {
        "enabled": true
      }
    }
  },
  "diagnostics": {
    "enabled": true,
    "otel": {
      "enabled": true,
      "endpoint": "http://otel-collector:4318",
      "protocol": "http/protobuf",
      "serviceName": "openclaw-gateway",
      "traces": true,
      "metrics": true,
      "logs": true,
      "sampleRate": 0.2,
      "flushIntervalMs": 60000
    }
  }
}
```

Notes:

*   You can also enable the plugin with `openclaw plugins enable diagnostics-otel`.
*   `protocol` currently supports `http/protobuf` only. `grpc` is ignored.
*   Metrics include token usage, cost, context size, run duration, and message-flow counters/histograms (webhooks, queueing, session state, queue depth/wait).
*   Traces/metrics can be toggled with `traces` / `metrics` (default: on). Traces include model usage spans plus webhook/message processing spans when enabled.
*   Set `headers` when your collector requires auth.
*   Environment variables supported: `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_SERVICE_NAME`, `OTEL_EXPORTER_OTLP_PROTOCOL`.

### Exported metrics (names + types)

Model usage:

*   `openclaw.tokens` (counter, attrs: `openclaw.token`, `openclaw.channel`, `openclaw.provider`, `openclaw.model`)
*   `openclaw.cost.usd` (counter, attrs: `openclaw.channel`, `openclaw.provider`, `openclaw.model`)
*   `openclaw.run.duration_ms` (histogram, attrs: `openclaw.channel`, `openclaw.provider`, `openclaw.model`)
*   `openclaw.context.tokens` (histogram, attrs: `openclaw.context`, `openclaw.channel`, `openclaw.provider`, `openclaw.model`)

Message flow:

*   `openclaw.webhook.received` (counter, attrs: `openclaw.channel`, `openclaw.webhook`)
*   `openclaw.webhook.error` (counter, attrs: `openclaw.channel`, `openclaw.webhook`)
*   `openclaw.webhook.duration_ms` (histogram, attrs: `openclaw.channel`, `openclaw.webhook`)
*   `openclaw.message.queued` (counter, attrs: `openclaw.channel`, `openclaw.source`)
*   `openclaw.message.processed` (counter, attrs: `openclaw.channel`, `openclaw.outcome`)
*   `openclaw.message.duration_ms` (histogram, attrs: `openclaw.channel`, `openclaw.outcome`)

Queues + sessions:

*   `openclaw.queue.lane.enqueue` (counter, attrs: `openclaw.lane`)
*   `openclaw.queue.lane.dequeue` (counter, attrs: `openclaw.lane`)
*   `openclaw.queue.depth` (histogram, attrs: `openclaw.lane` or `openclaw.channel=heartbeat`)
*   `openclaw.queue.wait_ms` (histogram, attrs: `openclaw.lane`)
*   `openclaw.session.state` (counter, attrs: `openclaw.state`, `openclaw.reason`)
*   `openclaw.session.stuck` (counter, attrs: `openclaw.state`)
*   `openclaw.session.stuck_age_ms` (histogram, attrs: `openclaw.state`)
*   `openclaw.run.attempt` (counter, attrs: `openclaw.attempt`)

### Exported spans (names + key attributes)

*   `openclaw.model.usage`
    *   `openclaw.channel`, `openclaw.provider`, `openclaw.model`
    *   `openclaw.sessionKey`, `openclaw.sessionId`
    *   `openclaw.tokens.*` (input/output/cache\_read/cache\_write/total)
*   `openclaw.webhook.processed`
    *   `openclaw.channel`, `openclaw.webhook`, `openclaw.chatId`
*   `openclaw.webhook.error`
    *   `openclaw.channel`, `openclaw.webhook`, `openclaw.chatId`, `openclaw.error`
*   `openclaw.message.processed`
    *   `openclaw.channel`, `openclaw.outcome`, `openclaw.chatId`, `openclaw.messageId`, `openclaw.sessionKey`, `openclaw.sessionId`, `openclaw.reason`
*   `openclaw.session.stuck`
    *   `openclaw.state`, `openclaw.ageMs`, `openclaw.queueDepth`, `openclaw.sessionKey`, `openclaw.sessionId`

### Sampling + flushing

*   Trace sampling: `diagnostics.otel.sampleRate` (0.0–1.0, root spans only).
*   Metric export interval: `diagnostics.otel.flushIntervalMs` (min 1000ms).

### Protocol notes

*   OTLP/HTTP endpoints can be set via `diagnostics.otel.endpoint` or `OTEL_EXPORTER_OTLP_ENDPOINT`.
*   If the endpoint already contains `/v1/traces` or `/v1/metrics`, it is used as-is.
*   If the endpoint already contains `/v1/logs`, it is used as-is for logs.
*   `diagnostics.otel.logs` enables OTLP log export for the main logger output.

### Log export behavior

*   OTLP logs use the same structured records written to `logging.file`.
*   Respect `logging.level` (file log level). Console redaction does **not** apply to OTLP logs.
*   High-volume installs should prefer OTLP collector sampling/filtering.

## Troubleshooting tips

*   **Gateway not reachable?** Run `openclaw doctor` first.
*   **Logs empty?** Check that the Gateway is running and writing to the file path in `logging.file`.
*   **Need more detail?** Set `logging.level` to `debug` or `trace` and retry.

