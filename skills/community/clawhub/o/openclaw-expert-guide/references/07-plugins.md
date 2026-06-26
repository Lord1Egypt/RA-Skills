# OpenClaw Plugins Reference

Plugins extend OpenClaw with new capabilities: channels, model providers, agent harnesses, tools, skills, speech, realtime transcription, realtime voice, media understanding, image generation, video generation, web fetch, web search, and more.

**Docs:** https://docs.openclaw.ai/plugins

## Table of Contents
- [Plugin Types](#plugin-types)
- [Quick Start](#quick-start)
- [Official Installable Plugins (npm)](#official-installable-plugins-npm)
- [Core Plugins (shipped with OpenClaw)](#core-plugins-shipped-with-openclaw)
- [Plugin Configuration](#plugin-configuration)
- [Plugin Slots (exclusive categories)](#plugin-slots-exclusive-categories)
- [Plugin Discovery Order (first match wins)](#plugin-discovery-order-first-match-wins)
- [CLI Reference](#cli-reference)
- [Plugin States](#plugin-states)
- [Plugin API Overview](#plugin-api-overview)
- [Voice Call Plugin](#voice-call-plugin-openclawvoice-call)
- [Memory Plugins](#memory-plugins)
- [Browser Plugin](#browser-plugin)
- [Bundle Plugins](#bundle-plugins)
- [MCP (Model Context Protocol) Tools](#mcp-model-context-protocol-tools)
- [Web Search Plugins](#web-search-plugins)
- [Image Generation Plugins](#image-generation-plugins)
- [Music Generation Plugins](#music-generation-plugins)
- [Video Generation Plugins](#video-generation-plugins)
- [Channel Plugins](#channel-plugins)
- [Troubleshooting Plugins](#troubleshooting-plugins)
- [Community Plugins](#community-plugins)
- [Building Plugins](#building-plugins)

---

## Plugin Types

| Format | How it works | Examples |
|---|---|---|
| **Native** | `openclaw.plugin.json` + runtime module; executes in-process | Official plugins, community npm packages |
| **Bundle** | Codex/Claude/Cursor-compatible layout; mapped to OpenClaw features | `.codex-plugin/`, `.claude-plugin/`, `.cursor-plugin/` |

---

## Quick Start

```bash
# See what is loaded
openclaw plugins list

# Install from npm
openclaw plugins install @openclaw/voice-call

# Install from local directory or archive
openclaw plugins install ./my-plugin
openclaw plugins install ./my-plugin.tgz

# Restart the gateway
openclaw gateway restart
```

Then configure under `plugins.entries.<id>.config`.

If config is invalid, install fails closed and points to `openclaw doctor --fix`. The only recovery exception is a narrow bundled-plugin reinstall path for plugins that opt into `openclaw.install.allowInvalidConfigRecovery`.

Packaged installs do not eagerly install every bundled plugin's runtime dependency tree. When a bundled OpenClaw-owned plugin is active (from config, legacy channel config, or default-enabled manifest), startup repairs only that plugin's declared runtime dependencies. Explicit disablement (`plugins.entries.<id>.enabled: false`, `plugins.deny`, `plugins.enabled: false`, `channels.<id>.enabled: false`) prevents automatic repair.

### Chat-native control

Enable with `commands.plugins: true`:

```
/plugin install clawhub:@openclaw/voice-call
/plugin show voice-call
/plugin enable voice-call
```

---

## Official Installable Plugins (npm)

| Plugin | Package | Docs |
|---|---|---|
| Matrix | `@openclaw/matrix` | channels/matrix |
| Microsoft Teams | `@openclaw/msteams` | channels/msteams |
| Nostr | `@openclaw/nostr` | channels/nostr |
| Voice Call | `@openclaw/voice-call` | plugins/voice-call |
| Zalo | `@openclaw/zalo` | channels/zalo |
| Zalo Personal | `@openclaw/zalouser` | plugins/zalouser |

---

## Core Plugins (shipped with OpenClaw)

### Model providers (enabled by default)

`anthropic`, `byteplus`, `cloudflare-ai-gateway`, `github-copilot`, `google`, `huggingface`, `kilocode`, `kimi-coding`, `minimax`, `mistral`, `qwen`, `moonshot`, `nvidia`, `openai`, `opencode`, `opencode-go`, `openrouter`, `qianfan`, `synthetic`, `together`, `venice`, `vercel-ai-gateway`, `volcengine`, `xiaomi`, `zai`

### Memory plugins

| Plugin | Description |
|---|---|
| `memory-core` | Default bundled memory search |
| `memory-lancedb` | Long-term memory with auto-recall/capture |

```json5
{
  plugins: {
    slots: {
      memory: "memory-lancedb"  // or "memory-core" (default) or "none"
    }
  }
}
```

### Speech providers (enabled by default)

`elevenlabs`, `microsoft`

### Other core plugins

| Plugin | Description |
|---|---|
| `browser` | Bundled browser plugin — browser tool, `openclaw browser` CLI, browser control service |
| `copilot-proxy` | VS Code Copilot Proxy bridge (disabled by default) |

---

## Plugin Configuration

```json5
{
  plugins: {
    enabled: true,
    allow: ["voice-call"],
    deny: ["untrusted-plugin"],
    load: { paths: ["~/Projects/oss/voice-call-plugin"] },
    entries: {
      "voice-call": { enabled: true, config: { provider: "twilio" } }
    }
  }
}
```

| Field | Description |
|---|---|
| `enabled` | Master toggle (default: `true`) |
| `allow` | Plugin allowlist (optional) |
| `deny` | Plugin denylist (deny wins) |
| `load.paths` | Extra plugin files/directories |
| `slots` | Exclusive slot selectors |
| `entries.<id>` | Per-plugin toggles + config |

Config changes require a gateway restart. If the Gateway is running with config watch + in-process restart enabled (the default `openclaw gateway` path), that restart is usually performed automatically a moment after the config write lands.
There is no supported hot-reload path for native plugin runtime code or lifecycle hooks; restart the Gateway process serving the live channel before expecting updated `register(api)` code, `api.on(...)` hooks, tools, services, or provider/runtime hooks to run.

`openclaw plugins list` is a local CLI/config snapshot. A `loaded` plugin means the plugin is discoverable and loadable from that CLI invocation. It does not prove an already-running remote Gateway child has restarted into the same code. On VPS/container setups with wrapper processes, send restarts to the actual `openclaw gateway run` process or use `openclaw gateway restart`.

---

## Plugin Slots (exclusive categories)

```json5
{
  plugins: {
    slots: {
      memory: "memory-core",   // or "none"
      contextEngine: "legacy"  // or a plugin id
    }
  }
}
```

| Slot | Controls | Default |
|---|---|---|
| `memory` | Active memory plugin | `memory-core` |
| `contextEngine` | Active context engine | `legacy` (built-in) |

---

## Plugin Discovery Order (first match wins)

1. `plugins.load.paths` — explicit paths
2. `<workspace>/.openclaw/<plugin-root>/*.ts` or `*/index.ts` — workspace plugins (disabled by default)
3. `~/.openclaw/<plugin-root>/*.ts` or `*/index.ts` — global plugins
4. Bundled plugins (shipped with OpenClaw)

### Enablement rules

- `plugins.enabled: false` → disables ALL plugins
- `plugins.deny` → always wins over allow
- `plugins.entries.<id>.enabled: false` → disables that plugin
- Workspace-origin plugins: **disabled by default** (must be explicitly enabled)
- Bundled plugins: default-on set unless overridden
- Exclusive slots can force-enable the selected plugin
- Some bundled opt-in plugins are enabled automatically when config names a plugin-owned surface, such as a provider model ref, channel config, or harness runtime
- **Codex routing note**: `openai-codex/*` model refs belong to the OpenAI plugin; the bundled Codex app-server plugin is selected by `embeddedHarness.runtime: "codex"` or legacy `codex/*` model refs — these keep separate plugin boundaries

---

## CLI Reference

```bash
# Inventory
openclaw plugins list                       # compact inventory
openclaw plugins list --enabled            # only loaded plugins
openclaw plugins list --verbose            # per-plugin detail lines
openclaw plugins list --json               # machine-readable
openclaw plugins inspect <id>              # deep detail
openclaw plugins inspect <id> --json       # machine-readable
openclaw plugins inspect --all             # fleet-wide table
openclaw plugins info <id>                 # inspect alias
openclaw plugins doctor                    # diagnostics

# Install / update / uninstall
openclaw plugins install <package>         # ClawHub first, then npm
openclaw plugins install clawhub:<pkg>     # ClawHub only
openclaw plugins install <spec> --force    # overwrite existing (not supported with --link)
openclaw plugins install <path>            # from local path
openclaw plugins install -l <path>         # link (dev mode; --force not supported with --link)
openclaw plugins install <plugin> --marketplace <source>  # source: name, local path, GitHub shorthand (owner/repo), GitHub URL, or git URL
openclaw plugins install <plugin> --marketplace https://github.com/<owner>/<repo>  # GitHub URL form
openclaw plugins install <spec> --pin      # record exact npm spec
openclaw plugins install <spec> --dangerously-force-unsafe-install
openclaw plugins update <id-or-npm-spec>  # update one
openclaw plugins update <id-or-npm-spec> --dangerously-force-unsafe-install
openclaw plugins update --all             # update all
openclaw plugins uninstall <id>           # remove
openclaw plugins uninstall <id> --keep-files

# Enable / disable
openclaw plugins enable <id>
openclaw plugins disable <id>

# Marketplace
openclaw plugins marketplace list <source>
openclaw plugins marketplace list <source> --json
```

### Notes on install/update

- `--force` overwrites existing install; **not supported with `--link`** (which reuses source path instead of copying)
- `--pin` is npm-only; not supported with `--marketplace`
- `--dangerously-force-unsafe-install` bypasses code scanner findings but not policy blocks
- When `plugins.allow` is set, `plugins install` adds the new plugin id to the allowlist automatically
- If the installed npm plugin already matches the resolved version and recorded artifact identity, `plugins update` skips the download/reinstall without rewriting config
- Marketplace source formats: Claude known-marketplace name (from `~/.claude/plugins/known_marketplaces.json`), a local marketplace root or `marketplace.json` path, a GitHub shorthand like `owner/repo`, a GitHub repo URL, or a git URL
- `openclaw plugins list` — a `loaded` plugin means the plugin is discoverable and loadable from the config/files seen by that CLI invocation; it does not prove an already-running remote Gateway child has restarted into the same plugin code
- `openclaw plugins inspect <id>` also reports supported or unsupported MCP and LSP server entries for bundle-backed plugins

---

## Plugin States

| State | Meaning |
|---|---|
| **Disabled** | Plugin exists but enablement rules turned it off |
| **Missing** | Config references a plugin id that discovery didn't find |
| **Invalid** | Plugin exists but config doesn't match declared schema |

---

## Plugin API Overview

Native plugins export an entry object with `register(api)`:

```typescript
export default definePluginEntry({
  id: "my-plugin",
  name: "My Plugin",
  register(api) {
    api.registerProvider({ /* ... */ });
    api.registerTool({ /* ... */ });
    api.registerChannel({ /* ... */ });
  }
});
```

> **Legacy alias**: Older plugins may still use `activate(api)` instead of `register(api)`. New plugins should use `register`.

**Codex app-server bridge**: Plugins can block native Codex tools through `before_tool_call`, observe results through `after_tool_call`, and participate in Codex `PermissionRequest` approvals.

### Registration methods

| Method | What it registers |
|---|---|
| `registerProvider` | Model provider (LLM) |
| `registerChannel` | Chat channel |
| `registerTool` | Agent tool |
| `registerHook` / `on(...)` | Lifecycle hooks |
| `registerSpeechProvider` | Text-to-speech / STT |
| `registerRealtimeTranscriptionProvider` | Streaming STT |
| `registerRealtimeVoiceProvider` | Duplex realtime voice |
| `registerMediaUnderstandingProvider` | Image/audio analysis |
| `registerImageGenerationProvider` | Image generation |
| `registerMusicGenerationProvider` | Music generation |
| `registerVideoGenerationProvider` | Video generation |
| `registerWebFetchProvider` | Web fetch / scrape |
| `registerWebSearchProvider` | Web search |
| `registerHttpRoute` | HTTP endpoint |
| `registerCliBackend` | CLI inference backend |
| `registerCommand` / `registerCli` | CLI commands |
| `registerContextEngine` | Context engine |
| `registerAgentToolResultMiddleware` | Tool-result middleware |
| `registerService` | Background service |

### Hook guard behavior

| Hook | Behavior |
|---|---|
| `before_tool_call` | `{ block: true }` is terminal (lower-priority handlers skipped); `{ block: false }` is a no-op and does not clear an earlier block |
| `before_install` | `{ block: true }` is terminal; `{ block: false }` is a no-op and does not clear an earlier block |
| `message_sending` | `{ cancel: true }` is terminal; `{ cancel: false }` is a no-op and does not clear an earlier cancel |

---

## Voice Call Plugin (`@openclaw/voice-call`)

```bash
openclaw plugins install @openclaw/voice-call
openclaw gateway restart
```

### Providers

| Provider | Description |
|---|---|
| `twilio` | Programmable Voice + Media Streams |
| `telnyx` | Call Control v2 |
| `plivo` | Voice API + XML transfer + GetInput speech |
| `mock` | Local dev/no network |

### Configuration structure

Full config reference (all major fields shown):

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        enabled: true,
        config: {
          provider: "twilio", // or "telnyx" | "plivo" | "mock"
          fromNumber: "+15550001234", // or TWILIO_FROM_NUMBER for Twilio
          toNumber: "+15550005678",

          twilio: {
            accountSid: "ACxxxxxxxx",
            authToken: "...",
          },

          telnyx: {
            apiKey: "...",
            connectionId: "...",
            // Telnyx webhook public key from Mission Control Portal
            // (Base64 string; or TELNYX_PUBLIC_KEY env var)
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

          // Inbound call policy (default: disabled)
          inboundPolicy: "allowlist", // disabled | allowlist
          allowFrom: ["+15550005678"],
          inboundGreeting: "Hello! How can I help?",

          // Stale call reaper (default: 0 = disabled)
          maxDurationSeconds: 300,
          staleCallReaperSeconds: 360, // should be > maxDurationSeconds

          // Streaming STT (realtime transcription)
          // Do NOT combine with realtime.enabled: true
          streaming: {
            enabled: true,
            provider: "openai", // optional; first registered realtime transcription provider when unset
            streamPath: "/voice/stream",
            providers: {
              openai: {
                apiKey: "sk-...", // optional if OPENAI_API_KEY is set
                model: "gpt-4o-transcribe",
                silenceDurationMs: 800,
                vadThreshold: 0.5,
              },
            },
            // Streaming security
            preStartTimeoutMs: 5000,
            maxPendingConnections: 32,
            maxPendingConnectionsPerIp: 4,
            maxConnections: 128,
          },

          // Realtime voice (full duplex, bidirectional audio)
          // Do NOT combine with streaming.enabled: true
          realtime: {
            enabled: false, // default; enable for live voice conversations
            provider: "google", // optional; first registered realtime voice provider when unset
            toolPolicy: "safe-read-only", // safe-read-only | owner | none
            providers: {
              google: {
                model: "gemini-2.5-flash-native-audio-preview-12-2025",
                voice: "Kore",
              },
            },
          },
        },
      },
    },
  },
}
```

### Realtime voice

`realtime` selects a full duplex realtime voice provider. Supported providers: `google` (default example), `openai`.

- `realtime.enabled: false` is the default. Enable for live voice-to-voice conversations.
- `realtime.provider` is optional. If unset, uses the first registered realtime voice provider.
- `realtime.toolPolicy` controls the `openclaw_agent_consult` tool:
  - `safe-read-only`: expose consult tool, limit agent to `read`, `web_search`, `web_fetch`, `memory_search`, `memory_get`
  - `owner`: expose consult tool with normal agent tool policy
  - `none`: do not expose the consult tool
- **Cannot be combined with `streaming.enabled: true`**

**Google Gemini Live (default example):**
```json5
realtime: {
  enabled: true,
  provider: "google",
  toolPolicy: "safe-read-only",
  providers: {
    google: {
      apiKey: "${GEMINI_API_KEY}",
      model: "gemini-2.5-flash-native-audio-preview-12-2025",
      voice: "Kore",
    },
  },
}
```

**OpenAI alternative:**
```json5
realtime: {
  enabled: true,
  provider: "openai",
  providers: {
    openai: {
      apiKey: "${OPENAI_API_KEY}",
    },
  },
}
```

### Streaming transcription (STT)

`streaming` selects a realtime transcription provider. Cannot be combined with `realtime.enabled: true`.

- `streaming.provider` is optional. If unset, uses the first registered realtime transcription provider.
- Supported streaming providers include: `openai`, `xai`, `deepgram`, `elevenlabs`, `mistral`
- Streaming security: `preStartTimeoutMs` (closes sockets without valid `start` frame), `maxPendingConnections` (total unauthenticated pre-start), `maxPendingConnectionsPerIp` (per source IP), `maxConnections` (total open media sockets)

**OpenAI defaults:** model `gpt-4o-transcribe`, `silenceDurationMs: 800`, `vadThreshold: 0.5`

**xAI defaults:** endpoint `wss://api.x.ai/v1/stt`, `encoding: "mulaw"`, `sampleRate: 8000`, `endpointingMs: 800`, `interimResults: true`

```json5
// OpenAI example
streaming: {
  enabled: true,
  provider: "openai",
  streamPath: "/voice/stream",
  providers: {
    openai: {
      apiKey: "sk-...",
      model: "gpt-4o-transcribe",
      silenceDurationMs: 800,
      vadThreshold: 0.5,
    },
  },
}

// xAI alternative
streaming: {
  enabled: true,
  provider: "xai",
  streamPath: "/voice/stream",
  providers: {
    xai: {
      apiKey: "${XAI_API_KEY}",
      endpointingMs: 800,
      language: "en",
    },
  },
}
```

### TTS for calls

Voice Call uses `messages.tts` for streaming speech. Override just for calls:

```json5
{
  plugins: { entries: { "voice-call": { config: {
    tts: {
      provider: "elevenlabs",
      providers: {
        elevenlabs: {
          voiceId: "pMsXgVXv3BLzUgSXRplE",
          modelId: "eleven_multilingual_v2",
        },
      },
    },
  }}}}
}
```

### Webhook security notes

- Twilio/Telnyx/Plivo require **publicly reachable** webhook URL
- `mock` is local dev provider (no network calls)
- Legacy config (`provider: "log"`, `twilio.from`) → run `openclaw doctor --fix`
- Telnyx requires `telnyx.publicKey` (or `TELNYX_PUBLIC_KEY`) unless `skipSignatureVerification: true` (local testing only)
- `tunnel.allowNgrokFreeTierLoopbackBypass: true` — allows Twilio webhooks with invalid signatures ONLY when `tunnel.provider="ngrok"` and `serve.bind` is loopback. Local dev only.
- Ngrok free tier URLs drift; use stable domain or Tailscale funnel for production

> **Note**: Microsoft speech is ignored for voice calls (telephony audio needs PCM).

### Voice Call CLI

```bash
openclaw voicecall setup           # check plugin setup (provider, creds, webhook)
openclaw voicecall setup --json    # machine-readable
openclaw voicecall smoke           # dry-run smoke test
openclaw voicecall smoke --to "+15555550123"        # dry run to specific number
openclaw voicecall smoke --to "+15555550123" --yes  # actually place a short call
```

`setup` checks: plugin enabled, provider+credentials present, webhook exposure configured, only one audio mode active. Fails if webhook resolves to loopback/private network.

### Stale call reaper

Use `staleCallReaperSeconds` to end calls that never receive a terminal webhook. Default: `0` (disabled).

- Recommended range: `120`–`300` seconds for notify-style flows
- Keep `staleCallReaperSeconds` **higher than `maxDurationSeconds`**

---

## Memory Plugins

### memory-core (default)

Built-in memory search. Uses `memory_search` and `memory_get` tools.

```json5
{
  plugins: { slots: { memory: "memory-core" } }
}
```

### memory-lancedb

Long-term memory with auto-recall and capture. Install on demand:

```json5
{
  plugins: { slots: { memory: "memory-lancedb" } }
}
```

Supports semantic vector search with embedding providers:
- Ollama (`nomic-embed-text`)
- Mistral (`mistral-embed`)
- OpenAI embeddings
- Amazon Bedrock embeddings (Titan, Nova, Cohere, TwelveLabs)

---

## Browser Plugin

Built-in browser plugin. Provides:
- `browser` agent tool
- `openclaw browser` CLI
- `browser.request` gateway method
- Default browser control service (loopback)

### Disable (to replace with custom)

```json5
{
  plugins: { entries: { browser: { enabled: false } } }
}
```

### Ensure it's in allowlist

```json5
{
  plugins: { allow: ["telegram", "browser"] }
}
```

---

## Bundle Plugins

Bundles are Codex/Claude/Cursor-compatible layouts:
- `.codex-plugin/`
- `.claude-plugin/`
- `.cursor-plugin/`

Supported bundle capabilities:
- Bundle skills
- Claude command-skills
- Claude `settings.json` defaults
- Claude `.lsp.json` and `lspServers` defaults
- Cursor command-skills
- Compatible Codex hook directories

Compatible bundles participate in the `plugins list/inspect/enable/disable` flow.

---

## MCP (Model Context Protocol) Tools

Bundle-MCP tools appear in `openclaw plugins list`. To hide MCP tools while keeping profile built-ins:

```json5
{
  tools: { deny: ["bundle-mcp"] }
}
```

The `minimal` profile does not include bundle-MCP tools. `coding` and `messaging` profiles allow configured bundle-MCP tools by default.

---

## Web Search Plugins

### Brave Search

```json5
{
  plugins: {
    entries: {
      brave: {
        config: {
          webSearch: {
            apiKey: "BRAVE_API_KEY",  // or BRAVE_API_KEY env var
            mode: "search"            // or "llm-context"
          }
        }
      }
    }
  }
}
```

`llm-context` mode returns optimized content for LLMs but rejects some filters (freshness, ui_lang, date_after/before).

### Exa Search

```json5
{
  plugins: {
    entries: {
      exa: {
        config: {
          webSearch: {
            apiKey: "EXA_API_KEY"  // or EXA_API_KEY env var
          }
        }
      }
    }
  }
}
```

Supports neural + keyword search, date filters, content extraction (highlights, text, summaries).

### Firecrawl

```json5
{
  plugins: {
    entries: {
      firecrawl: {
        enabled: true,
        config: {
          webSearch: {
            apiKey: "fc-...",       // or FIRECRAWL_API_KEY
            baseUrl: "https://api.firecrawl.dev"
          },
          webFetch: {
            apiKey: "fc-...",
            baseUrl: "https://api.firecrawl.dev",
            onlyMainContent: true,
            maxAgeMs: 86400000,
            timeoutSeconds: 60
          }
        }
      }
    }
  }
}
```

⚠️ `baseUrl` must be `https://api.firecrawl.dev` — other hosts blocked.

### SearXNG (self-hosted)

```json5
{
  plugins: {
    entries: {
      searxng: {
        config: {
          webSearch: {
            baseUrl: "http://localhost:8888"  // or SEARXNG_BASE_URL
          }
        }
      }
    }
  }
}
```

SearXNG `http://` only for trusted private-network/loopback; public endpoints must use `https://`.

### Tavily

```json5
{
  plugins: {
    entries: {
      tavily: {
        config: {
          webSearch: {
            apiKey: "TAVILY_API_KEY"
          }
        }
      }
    }
  }
}
```

Also provides `tavily_search` and `tavily_extract` tools.

### Perplexity

```json5
{
  plugins: {
    entries: {
      perplexity: {
        config: {
          webSearch: {
            apiKey: "pplx-..."  // or PERPLEXITY_API_KEY; sk-or- routes through OpenRouter
          }
        }
      }
    }
  }
}
```

### Gemini Search (Google Grounding)

```json5
{
  plugins: {
    entries: {
      google: {
        config: {
          webSearch: {
            apiKey: "GEMINI_API_KEY"
          }
        }
      }
    }
  }
}
```

Returns AI-synthesized answers with citations.

### Grok Search (xAI)

```json5
{
  plugins: {
    entries: {
      xai: {
        config: {
          webSearch: {
            apiKey: "xai-..."   // or XAI_API_KEY
          }
        }
      }
    }
  }
}
```

Returns AI-synthesized answers with citations.

### Kimi Search (Moonshot)

```json5
{
  plugins: {
    entries: {
      moonshot: {
        config: {
          webSearch: {
            apiKey: "KIMI_API_KEY",
            baseUrl: "https://api.moonshot.ai/v1",  // or .cn
            model: "kimi-k2.6"
          }
        }
      }
    }
  }
}
```

### MiniMax Search

```json5
{
  plugins: {
    entries: {
      minimax: {
        config: {
          webSearch: {
            region: "global"  // or "cn"
          }
        }
      }
    }
  }
}
```

Uses `MINIMAX_CODE_PLAN_KEY` or `MINIMAX_CODING_API_KEY`.

### Ollama Web Search

```json5
{
  tools: { web: { search: { provider: "ollama" } } }
}
```

Requires `ollama signin`. Key-free.

---

## Image Generation Plugins

### fal

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: { primary: "fal/fal-ai/flux/dev" }
    }
  }
}
```

Auth: `FAL_KEY`. Supports text-to-image and editing (1 reference image).

### ComfyUI

For local ComfyUI workflows:

```json5
{
  plugins: {
    entries: {
      comfy: {
        config: {
          apiKey: "COMFY_API_KEY",  // or COMFY_CLOUD_API_KEY for cloud
          baseUrl: "http://localhost:8188"
        }
      }
    }
  }
}
```

Model ref: `comfy/workflow` (workflow-defined outputs).

---

## Music Generation Plugins

### Google Lyria

```json5
{
  agents: {
    defaults: {
      musicGenerationModel: { primary: "google/lyria-3-clip-preview" }
    }
  }
}
```

- Also: `google/lyria-3-pro-preview`
- Controls: `lyrics`, `instrumental`
- Output: `mp3` (default), `wav` (pro only)
- Reference inputs: up to 10 images

### MiniMax Music

```json5
{
  agents: {
    defaults: {
      musicGenerationModel: { primary: "minimax/music-2.5+" }
    }
  }
}
```

- Also: `minimax/music-2.6`, `minimax/music-2.5`, `minimax/music-2.0`
- Controls: `lyrics`, `instrumental`, `durationSeconds`
- Output: `mp3`

---

## Video Generation Plugins

### BytePlus (Seedance)

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: { primary: "byteplus/seedance-1-5-pro-251215" }
    }
  }
}
```

- Auth: `BYTEPLUS_API_KEY`
- Supports first_frame / last_frame image roles
- `adaptive` aspect ratio supported

### Runway

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: { primary: "runway/gen4.5" }
    }
  }
}
```

- Auth: `RUNWAYML_API_SECRET`
- Supports text-to-video, image-to-video, video-to-video

### fal Video

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: { primary: "fal/fal-ai/minimax/video-01-live" }
    }
  }
}
```

---

## Channel Plugins

### Telegram (built-in)

Built into OpenClaw core. Configure:

```json5
{
  channels: {
    telegram: {
      enabled: true,
      token: "${TELEGRAM_BOT_TOKEN}",
      // ... other settings
    }
  }
}
```

### WhatsApp (built-in)

```json5
{
  channels: {
    whatsapp: {
      enabled: true
      // ... provider config
    }
  }
}
```

### Discord (built-in)

```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "${DISCORD_BOT_TOKEN}",
      threadBindings: {
        enabled: true,
        idleHours: 1,
        maxAgeHours: 24
      }
    }
  }
}
```

### Slack (built-in)

```json5
{
  channels: {
    slack: {
      enabled: true,
      token: "${SLACK_BOT_TOKEN}"
    }
  }
}
```

### Matrix (`@openclaw/matrix`)

```bash
openclaw plugins install @openclaw/matrix
```

### Microsoft Teams (`@openclaw/msteams`)

```bash
openclaw plugins install @openclaw/msteams
```

---

## Troubleshooting Plugins

### Plugin appears in list but hooks don't run

1. Run `openclaw gateway status --deep --require-rpc` to confirm active gateway URL/process
2. Restart the live gateway after plugin install/config/code changes
3. Use `openclaw plugins inspect <id> --json` to confirm hook registrations
4. Non-bundled conversation hooks (`llm_input`, `llm_output`, `agent_end`) need:
   ```json5
   { "plugins": { "entries": { "<id>": { "hooks": { "allowConversationAccess": true } } } } }
   ```
5. For model switching, prefer `before_model_resolve` hook (runs before model resolution)

### Plugin is "missing"

Config references a plugin id that discovery didn't find. Install it:
```bash
openclaw plugins install <package>
```

### Plugin is "invalid"

Plugin's config doesn't match declared schema. Check with:
```bash
openclaw plugins inspect <id> --json
openclaw doctor --fix
```

### Wrong plugin code in live chat

On VPS/container setups, PID 1 may be a supervisor. Signal the child `openclaw gateway run` process, or use:
```bash
openclaw gateway restart
```

---

## Community Plugins

See https://docs.openclaw.ai/plugins/community for third-party listings.

### Claude Max API Proxy

Community proxy for Claude subscription credentials:
- https://docs.openclaw.ai/providers/claude-max-api-proxy
- Verify Anthropic policy/terms before use

---

## Building Plugins

### Minimal native plugin structure

```typescript
// index.ts
import { definePluginEntry } from "@openclaw/sdk";

export default definePluginEntry({
  id: "my-plugin",
  name: "My Plugin",
  version: "1.0.0",
  
  register(api) {
    // Register a tool
    api.registerTool({
      name: "my_tool",
      description: "Does something useful",
      schema: {
        type: "object",
        properties: {
          input: { type: "string", description: "Input text" }
        },
        required: ["input"]
      },
      async execute({ input }) {
        return `Processed: ${input}`;
      }
    });
    
    // Register a hook
    api.registerHook("before_tool_call", async (event) => {
      // Can return { block: true } to prevent tool call
      return {};
    });
    
    // Register a web search provider
    api.registerWebSearchProvider({
      id: "my-search",
      async search({ query, count }) {
        // Return search results
        return { results: [] };
      }
    });
  }
});
```

### openclaw.plugin.json

```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "main": "dist/index.js"
}
```

### Plugin locations for dev

```json5
{
  plugins: {
    load: { paths: ["~/Projects/my-plugin"] }
  }
}
```

Or install with link (dev mode):
```bash
openclaw plugins install -l ./my-plugin
```

### Optional channel setup surface

For channel plugins that aren't guaranteed to be installed when onboarding/setup runs, use `createOptionalChannelSetupSurface(...)` from `openclaw/plugin-sdk/channel-setup`. It produces a setup adapter + wizard pair that advertises the install requirement and fails closed on real config writes until the plugin is installed.

### Key references

- Building Plugins: https://docs.openclaw.ai/plugins/building-plugins
- Plugin SDK Overview: https://docs.openclaw.ai/plugins/sdk-overview
- Plugin Bundles: https://docs.openclaw.ai/plugins/bundles
- Plugin Manifest: https://docs.openclaw.ai/plugins/manifest
- Plugin Architecture: https://docs.openclaw.ai/plugins/architecture
- Community Plugins: https://docs.openclaw.ai/plugins/community
