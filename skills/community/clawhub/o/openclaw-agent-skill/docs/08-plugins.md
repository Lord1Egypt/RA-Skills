# Plugins & Extensions

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 6

---

<!-- SOURCE: https://docs.openclaw.ai/plugins/community -->

# Community plugins - OpenClaw

This page tracks high-quality **community-maintained plugins** for OpenClaw. We accept PRs that add community plugins here when they meet the quality bar.

## Required for listing

*   Plugin package is published on npmjs (installable via `openclaw plugins install <npm-spec>`).
*   Source code is hosted on GitHub (public repository).
*   Repository includes setup/use docs and an issue tracker.
*   Plugin has a clear maintenance signal (active maintainer, recent updates, or responsive issue handling).

## How to submit

Open a PR that adds your plugin to this page with:

*   Plugin name
*   npm package name
*   GitHub repository URL
*   One-line description
*   Install command

## Review bar

We prefer plugins that are useful, documented, and safe to operate. Low-effort wrappers, unclear ownership, or unmaintained packages may be declined.

## Candidate format

Use this format when adding entries:

*   **Plugin Name** — short description npm: `@scope/package` repo: `https://github.com/org/repo` install: `openclaw plugins install @scope/package`

## Listed plugins

*   **WeChat** — Connect OpenClaw to WeChat personal accounts via WeChatPadPro (iPad protocol). Supports text, image, and file exchange with keyword-triggered conversations. npm: `@icesword760/openclaw-wechat` repo: `https://github.com/icesword0760/openclaw-wechat` install: `openclaw plugins install @icesword760/openclaw-wechat`

---

<!-- SOURCE: https://docs.openclaw.ai/plugins/voice-call -->

# Voice Call Plugin - OpenClaw

Voice calls for OpenClaw via a plugin. Supports outbound notifications and multi-turn conversations with inbound policies. Current providers:

*   `twilio` (Programmable Voice + Media Streams)
*   `telnyx` (Call Control v2)
*   `plivo` (Voice API + XML transfer + GetInput speech)
*   `mock` (dev/no network)

Quick mental model:

*   Install plugin
*   Restart Gateway
*   Configure under `plugins.entries.voice-call.config`
*   Use `openclaw voicecall ...` or the `voice_call` tool

## Where it runs (local vs remote)

The Voice Call plugin runs **inside the Gateway process**. If you use a remote Gateway, install/configure the plugin on the **machine running the Gateway**, then restart the Gateway to load it.

## Install

### Option A: install from npm (recommended)

```
openclaw plugins install @openclaw/voice-call
```

Restart the Gateway afterwards.

### Option B: install from a local folder (dev, no copying)

```
openclaw plugins install ./extensions/voice-call
cd ./extensions/voice-call && pnpm install
```

Restart the Gateway afterwards.

## Config

Set config under `plugins.entries.voice-call.config`:

```
{
  plugins: {
    entries: {
      "voice-call": {
        enabled: true,
        config: {
          provider: "twilio", // or "telnyx" | "plivo" | "mock"
          fromNumber: "+15550001234",
          toNumber: "+15550005678",

          twilio: {
            accountSid: "ACxxxxxxxx",
            authToken: "...",
          },

          telnyx: {
            apiKey: "...",
            connectionId: "...",
            // Telnyx webhook public key from the Telnyx Mission Control Portal
            // (Base64 string; can also be set via TELNYX_PUBLIC_KEY).
            publicKey: "...",
          },

          plivo: {
            authId: "MAxxxxxxxxxxxxxxxxxxxx",
            authToken: "...",
          },

          // Webhook server
          serve: {
            port: 3334,
            path: "/voice/webhook",
          },

          // Webhook security (recommended for tunnels/proxies)
          webhookSecurity: {
            allowedHosts: ["voice.example.com"],
            trustedProxyIPs: ["100.64.0.1"],
          },

          // Public exposure (pick one)
          // publicUrl: "https://example.ngrok.app/voice/webhook",
          // tunnel: { provider: "ngrok" },
          // tailscale: { mode: "funnel", path: "/voice/webhook" }

          outbound: {
            defaultMode: "notify", // notify | conversation
          },

          streaming: {
            enabled: true,
            streamPath: "/voice/stream",
            preStartTimeoutMs: 5000,
            maxPendingConnections: 32,
            maxPendingConnectionsPerIp: 4,
            maxConnections: 128,
          },
        },
      },
    },
  },
}
```

Notes:

*   Twilio/Telnyx require a **publicly reachable** webhook URL.
*   Plivo requires a **publicly reachable** webhook URL.
*   `mock` is a local dev provider (no network calls).
*   Telnyx requires `telnyx.publicKey` (or `TELNYX_PUBLIC_KEY`) unless `skipSignatureVerification` is true.
*   `skipSignatureVerification` is for local testing only.
*   If you use ngrok free tier, set `publicUrl` to the exact ngrok URL; signature verification is always enforced.
*   `tunnel.allowNgrokFreeTierLoopbackBypass: true` allows Twilio webhooks with invalid signatures **only** when `tunnel.provider="ngrok"` and `serve.bind` is loopback (ngrok local agent). Use for local dev only.
*   Ngrok free tier URLs can change or add interstitial behavior; if `publicUrl` drifts, Twilio signatures will fail. For production, prefer a stable domain or Tailscale funnel.
*   Streaming security defaults:
    *   `streaming.preStartTimeoutMs` closes sockets that never send a valid `start` frame.
    *   `streaming.maxPendingConnections` caps total unauthenticated pre-start sockets.
    *   `streaming.maxPendingConnectionsPerIp` caps unauthenticated pre-start sockets per source IP.
    *   `streaming.maxConnections` caps total open media stream sockets (pending + active).

## Stale call reaper

Use `staleCallReaperSeconds` to end calls that never receive a terminal webhook (for example, notify-mode calls that never complete). The default is `0` (disabled). Recommended ranges:

*   **Production:** `120`–`300` seconds for notify-style flows.
*   Keep this value **higher than `maxDurationSeconds`** so normal calls can finish. A good starting point is `maxDurationSeconds + 30–60` seconds.

Example:

```
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          maxDurationSeconds: 300,
          staleCallReaperSeconds: 360,
        },
      },
    },
  },
}
```

## Webhook Security

When a proxy or tunnel sits in front of the Gateway, the plugin reconstructs the public URL for signature verification. These options control which forwarded headers are trusted. `webhookSecurity.allowedHosts` allowlists hosts from forwarding headers. `webhookSecurity.trustForwardingHeaders` trusts forwarded headers without an allowlist. `webhookSecurity.trustedProxyIPs` only trusts forwarded headers when the request remote IP matches the list. Webhook replay protection is enabled for Twilio and Plivo. Replayed valid webhook requests are acknowledged but skipped for side effects. Twilio conversation turns include a per-turn token in `<Gather>` callbacks, so stale/replayed speech callbacks cannot satisfy a newer pending transcript turn. Example with a stable public host:

```
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          publicUrl: "https://voice.example.com/voice/webhook",
          webhookSecurity: {
            allowedHosts: ["voice.example.com"],
          },
        },
      },
    },
  },
}
```

## TTS for calls

Voice Call uses the core `messages.tts` configuration (OpenAI or ElevenLabs) for streaming speech on calls. You can override it under the plugin config with the **same shape** — it deep‑merges with `messages.tts`.

```
{
  tts: {
    provider: "elevenlabs",
    elevenlabs: {
      voiceId: "pMsXgVXv3BLzUgSXRplE",
      modelId: "eleven_multilingual_v2",
    },
  },
}
```

Notes:

*   **Edge TTS is ignored for voice calls** (telephony audio needs PCM; Edge output is unreliable).
*   Core TTS is used when Twilio media streaming is enabled; otherwise calls fall back to provider native voices.

### More examples

Use core TTS only (no override):

```
{
  messages: {
    tts: {
      provider: "openai",
      openai: { voice: "alloy" },
    },
  },
}
```

Override to ElevenLabs just for calls (keep core default elsewhere):

```
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          tts: {
            provider: "elevenlabs",
            elevenlabs: {
              apiKey: "elevenlabs_key",
              voiceId: "pMsXgVXv3BLzUgSXRplE",
              modelId: "eleven_multilingual_v2",
            },
          },
        },
      },
    },
  },
}
```

Override only the OpenAI model for calls (deep‑merge example):

```
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          tts: {
            openai: {
              model: "gpt-4o-mini-tts",
              voice: "marin",
            },
          },
        },
      },
    },
  },
}
```

## Inbound calls

Inbound policy defaults to `disabled`. To enable inbound calls, set:

```
{
  inboundPolicy: "allowlist",
  allowFrom: ["+15550001234"],
  inboundGreeting: "Hello! How can I help?",
}
```

Auto-responses use the agent system. Tune with:

*   `responseModel`
*   `responseSystemPrompt`
*   `responseTimeoutMs`

## CLI

```
openclaw voicecall call --to "+15555550123" --message "Hello from OpenClaw"
openclaw voicecall continue --call-id <id> --message "Any questions?"
openclaw voicecall speak --call-id <id> --message "One moment"
openclaw voicecall end --call-id <id>
openclaw voicecall status --call-id <id>
openclaw voicecall tail
openclaw voicecall expose --mode funnel
```

Tool name: `voice_call` Actions:

*   `initiate_call` (message, to?, mode?)
*   `continue_call` (callId, message)
*   `speak_to_user` (callId, message)
*   `end_call` (callId)
*   `get_status` (callId)

This repo ships a matching skill doc at `skills/voice-call/SKILL.md`.

## Gateway RPC

*   `voicecall.initiate` (`to?`, `message`, `mode?`)
*   `voicecall.continue` (`callId`, `message`)
*   `voicecall.speak` (`callId`, `message`)
*   `voicecall.end` (`callId`)
*   `voicecall.status` (`callId`)

---

<!-- SOURCE: https://docs.openclaw.ai/plugins/manifest -->

# Plugin Manifest - OpenClaw

Every plugin **must** ship a `openclaw.plugin.json` file in the **plugin root**. OpenClaw uses this manifest to validate configuration **without executing plugin code**. Missing or invalid manifests are treated as plugin errors and block config validation. See the full plugin system guide: [Plugins](https://docs.openclaw.ai/tools/plugin).

## Required fields

```
{
  "id": "voice-call",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

Required keys:

*   `id` (string): canonical plugin id.
*   `configSchema` (object): JSON Schema for plugin config (inline).

Optional keys:

*   `kind` (string): plugin kind (examples: `"memory"`, `"context-engine"`).
*   `channels` (array): channel ids registered by this plugin (example: `["matrix"]`).
*   `providers` (array): provider ids registered by this plugin.
*   `skills` (array): skill directories to load (relative to the plugin root).
*   `name` (string): display name for the plugin.
*   `description` (string): short plugin summary.
*   `uiHints` (object): config field labels/placeholders/sensitive flags for UI rendering.
*   `version` (string): plugin version (informational).

## JSON Schema requirements

*   **Every plugin must ship a JSON Schema**, even if it accepts no config.
*   An empty schema is acceptable (for example, `{ "type": "object", "additionalProperties": false }`).
*   Schemas are validated at config read/write time, not at runtime.

## Validation behavior

*   Unknown `channels.*` keys are **errors**, unless the channel id is declared by a plugin manifest.
*   `plugins.entries.<id>`, `plugins.allow`, `plugins.deny`, and `plugins.slots.*` must reference **discoverable** plugin ids. Unknown ids are **errors**.
*   If a plugin is installed but has a broken or missing manifest or schema, validation fails and Doctor reports the plugin error.
*   If plugin config exists but the plugin is **disabled**, the config is kept and a **warning** is surfaced in Doctor + logs.

## Notes

*   The manifest is **required for all plugins**, including local filesystem loads.
*   Runtime still loads the plugin module separately; the manifest is only for discovery + validation.
*   Exclusive plugin kinds are selected through `plugins.slots.*`.
    *   `kind: "memory"` is selected by `plugins.slots.memory`.
    *   `kind: "context-engine"` is selected by `plugins.slots.contextEngine` (default: built-in `legacy`).
*   If your plugin depends on native modules, document the build steps and any package-manager allowlist requirements (for example, pnpm `allow-build-scripts`
    *   `pnpm rebuild <package>`).

---

<!-- SOURCE: https://docs.openclaw.ai/plugins/agent-tools -->

# Plugin Agent Tools - OpenClaw

OpenClaw plugins can register **agent tools** (JSON‑schema functions) that are exposed to the LLM during agent runs. Tools can be **required** (always available) or **optional** (opt‑in). Agent tools are configured under `tools` in the main config, or per‑agent under `agents.list[].tools`. The allowlist/denylist policy controls which tools the agent can call.

```
import { Type } from "@sinclair/typebox";

export default function (api) {
  api.registerTool({
    name: "my_tool",
    description: "Do a thing",
    parameters: Type.Object({
      input: Type.String(),
    }),
    async execute(_id, params) {
      return { content: [{ type: "text", text: params.input }] };
    },
  });
}
```

Optional tools are **never** auto‑enabled. Users must add them to an agent allowlist.

```
export default function (api) {
  api.registerTool(
    {
      name: "workflow_tool",
      description: "Run a local workflow",
      parameters: {
        type: "object",
        properties: {
          pipeline: { type: "string" },
        },
        required: ["pipeline"],
      },
      async execute(_id, params) {
        return { content: [{ type: "text", text: params.pipeline }] };
      },
    },
    { optional: true },
  );
}
```

Enable optional tools in `agents.list[].tools.allow` (or global `tools.allow`):

```
{
  agents: {
    list: [
      {
        id: "main",
        tools: {
          allow: [
            "workflow_tool", // specific tool name
            "workflow", // plugin id (enables all tools from that plugin)
            "group:plugins", // all plugin tools
          ],
        },
      },
    ],
  },
}
```

Other config knobs that affect tool availability:

*   Allowlists that only name plugin tools are treated as plugin opt-ins; core tools remain enabled unless you also include core tools or groups in the allowlist.
*   `tools.profile` / `agents.list[].tools.profile` (base allowlist)
*   `tools.byProvider` / `agents.list[].tools.byProvider` (provider‑specific allow/deny)
*   `tools.sandbox.tools.*` (sandbox tool policy when sandboxed)

## Rules + tips

*   Tool names must **not** clash with core tool names; conflicting tools are skipped.
*   Plugin ids used in allowlists must not clash with core tool names.
*   Prefer `optional: true` for tools that trigger side effects or require extra binaries/credentials.

---

<!-- SOURCE: https://docs.openclaw.ai/plugins/zalouser -->

# Zalo Personal Plugin - OpenClaw

Zalo Personal support for OpenClaw via a plugin, using native `zca-js` to automate a normal Zalo user account.

> **Warning:** Unofficial automation may lead to account suspension/ban. Use at your own risk.

## Naming

Channel id is `zalouser` to make it explicit this automates a **personal Zalo user account** (unofficial). We keep `zalo` reserved for a potential future official Zalo API integration.

## Where it runs

This plugin runs **inside the Gateway process**. If you use a remote Gateway, install/configure it on the **machine running the Gateway**, then restart the Gateway. No external `zca`/`openzca` CLI binary is required.

## Install

### Option A: install from npm

```
openclaw plugins install @openclaw/zalouser
```

Restart the Gateway afterwards.

### Option B: install from a local folder (dev)

```
openclaw plugins install ./extensions/zalouser
cd ./extensions/zalouser && pnpm install
```

Restart the Gateway afterwards.

## Config

Channel config lives under `channels.zalouser` (not `plugins.entries.*`):

```
{
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}
```

## CLI

```
openclaw channels login --channel zalouser
openclaw channels logout --channel zalouser
openclaw channels status --probe
openclaw message send --channel zalouser --target <threadId> --message "Hello from OpenClaw"
openclaw directory peers list --channel zalouser --query "name"
```

Tool name: `zalouser` Actions: `send`, `image`, `link`, `friends`, `groups`, `me`, `status` Channel message actions also support `react` for message reactions.

---

<!-- SOURCE: https://docs.openclaw.ai/prose -->

# OpenProse - OpenClaw

OpenProse is a portable, markdown-first workflow format for orchestrating AI sessions. In OpenClaw it ships as a plugin that installs an OpenProse skill pack plus a `/prose` slash command. Programs live in `.prose` files and can spawn multiple sub-agents with explicit control flow. Official site: [https://www.prose.md](https://www.prose.md/)

## What it can do

*   Multi-agent research + synthesis with explicit parallelism.
*   Repeatable approval-safe workflows (code review, incident triage, content pipelines).
*   Reusable `.prose` programs you can run across supported agent runtimes.

## Install + enable

Bundled plugins are disabled by default. Enable OpenProse:

```
openclaw plugins enable open-prose
```

Restart the Gateway after enabling the plugin. Dev/local checkout: `openclaw plugins install ./extensions/open-prose` Related docs: [Plugins](https://docs.openclaw.ai/tools/plugin), [Plugin manifest](https://docs.openclaw.ai/plugins/manifest), [Skills](https://docs.openclaw.ai/tools/skills).

## Slash command

OpenProse registers `/prose` as a user-invocable skill command. It routes to the OpenProse VM instructions and uses OpenClaw tools under the hood. Common commands:

```
/prose help
/prose run <file.prose>
/prose run <handle/slug>
/prose run <https://example.com/file.prose>
/prose compile <file.prose>
/prose examples
/prose update
```

## Example: a simple `.prose` file

```
# Research + synthesis with two agents running in parallel.

input topic: "What should we research?"

agent researcher:
  model: sonnet
  prompt: "You research thoroughly and cite sources."

agent writer:
  model: opus
  prompt: "You write a concise summary."

parallel:
  findings = session: researcher
    prompt: "Research {topic}."
  draft = session: writer
    prompt: "Summarize {topic}."

session "Merge the findings + draft into a final answer."
context: { findings, draft }
```

## File locations

OpenProse keeps state under `.prose/` in your workspace:

```
.prose/
├── .env
├── runs/
│   └── {YYYYMMDD}-{HHMMSS}-{random}/
│       ├── program.prose
│       ├── state.md
│       ├── bindings/
│       └── agents/
└── agents/
```

User-level persistent agents live at:

## State modes

OpenProse supports multiple state backends:

*   **filesystem** (default): `.prose/runs/...`
*   **in-context**: transient, for small programs
*   **sqlite** (experimental): requires `sqlite3` binary
*   **postgres** (experimental): requires `psql` and a connection string

Notes:

*   sqlite/postgres are opt-in and experimental.
*   postgres credentials flow into subagent logs; use a dedicated, least-privileged DB.

## Remote programs

`/prose run <handle/slug>` resolves to `https://p.prose.md/<handle>/<slug>`. Direct URLs are fetched as-is. This uses the `web_fetch` tool (or `exec` for POST).

## OpenClaw runtime mapping

OpenProse programs map to OpenClaw primitives:

| OpenProse concept | OpenClaw tool |
| --- | --- |
| Spawn session / Task tool | `sessions_spawn` |
| File read/write | `read` / `write` |
| Web fetch | `web_fetch` |

If your tool allowlist blocks these tools, OpenProse programs will fail. See [Skills config](https://docs.openclaw.ai/tools/skills-config).

## Security + approvals

Treat `.prose` files like code. Review before running. Use OpenClaw tool allowlists and approval gates to control side effects. For deterministic, approval-gated workflows, compare with [Lobster](https://docs.openclaw.ai/tools/lobster).

