# OpenClaw Tools Reference

Tools are typed functions the agent can invoke. OpenClaw ships built-in tools; plugins can register additional ones.

## Table of Contents
- [Tool Architecture](#tool-architecture)
- [Built-in Tools Overview](#built-in-tools-overview)
- [exec](#exec)
- [code_execution](#code_execution)
- [browser](#browser)
- [message (Agent Send)](#message-agent-send)
- [image_generate](#image_generate)
- [video_generate](#video_generate)
- [music_generate](#music_generate)
- [tts](#tts)
- [web_fetch](#web_fetch)
- [sessions_spawn (Sub-agents)](#sessions_spawn-sub-agents)
- [web_search](#web_search)
- [Tool Configuration](#tool-configuration)
- [gateway tool](#gateway-tool)
- [memory_search / memory_get](#memory_search--memory_get)
- [session_status](#session_status)
- [Plugin-provided tools (examples)](#plugin-provided-tools-examples)

## Tool Architecture

- **Tools**: typed functions the agent calls (`exec`, `browser`, `web_search`, `message`)
- **Skills**: markdown files (`SKILL.md`) injected into system prompt giving context and guidance
- **Plugins**: packages that register capabilities (channels, providers, tools, skills, etc.)

---

## Built-in Tools Overview

| Tool | What it does | Page |
|---|---|---|
| `exec` / `process` | Run shell commands, manage background processes | exec |
| `code_execution` | Run sandboxed remote Python analysis | code-execution |
| `browser` | Control a Chromium browser | browser |
| `web_search` / `x_search` / `web_fetch` | Search web, X posts, fetch pages | web / web-fetch |
| `read` / `write` / `edit` | File I/O in the workspace | — |
| `apply_patch` | Multi-hunk file patches | apply-patch |
| `message` | Send messages across all channels | agent-send |
| `canvas` | Drive node Canvas (present, eval, snapshot) | — |
| `nodes` | Discover and target paired devices | — |
| `cron` / `gateway` | Manage scheduled jobs; inspect/patch/restart gateway | — |
| `image` / `image_generate` | Analyze or generate images | image-generation |
| `music_generate` | Generate music tracks | music-generation |
| `video_generate` | Generate videos | video-generation |
| `tts` | One-shot text-to-speech | tts |
| `sessions_*` / `subagents` / `agents_list` | Session management, sub-agent orchestration | subagents |
| `session_status` | Lightweight status readback | session-tool |
| `memory_search` / `memory_get` | Search memory files | memory |

---

## exec

Run shell commands in the workspace. Supports foreground + background execution via `process`.

**Docs:** https://docs.openclaw.ai/tools/exec

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `command` | string | required | Shell command to run |
| `workdir` | string | cwd | Working directory |
| `env` | object | — | Key/value env overrides |
| `yieldMs` | number | 10000 | Auto-background after this delay (ms) |
| `background` | boolean | false | Background immediately |
| `timeout` | number | 1800 | Kill after this many seconds |
| `pty` | boolean | false | Run in pseudo-terminal (for TTY-only CLIs) |
| `host` | string | `auto` | Where to execute: `auto`, `sandbox`, `gateway`, `node` |
| `security` | string | `deny` for sandbox; `full` for gateway+node | `deny`, `allowlist`, or `full` |
| `ask` | string | — | `off`, `on-miss`, or `always` |
| `node` | string | — | Node id/name when `host=node` |
| `elevated` | boolean | false | Escape sandbox onto configured host path |

### host resolution

- `auto` → `sandbox` when sandbox runtime is active; `gateway` otherwise
- `host=node` requires a paired node device
- `elevated` escapes the sandbox; only when elevated access is enabled

### Examples

```json
// Foreground
{ "tool": "exec", "command": "ls -la" }

// Background + poll
{ "tool": "exec", "command": "npm run build", "yieldMs": 1000 }
{ "tool": "process", "action": "poll", "sessionId": "<id>" }

// PTY for interactive CLIs
{ "tool": "exec", "command": "claude", "pty": true }
```

### process actions

| Action | Description |
|---|---|
| `list` | List background sessions |
| `poll` | Check status of a session |
| `log` | Get output from a session |
| `write` | Write to session stdin |
| `send-keys` | Send keys (tmux-style): `["Enter"]`, `["C-c"]`, `["Up","Up","Enter"]` |
| `submit` | Send CR only |
| `paste` | Paste text (bracketed by default) |
| `kill` | Terminate a session |

### Config

```json5
{
  tools: {
    exec: {
      host: "auto",             // default routing
      security: "full",         // deny | allowlist | full
      ask: "off",               // off | on-miss | always
      notifyOnExit: true,       // heartbeat on exit
      approvalRunningNoticeMs: 10000,
      pathPrepend: ["~/bin", "/opt/oss/bin"],
      safeBins: ["cat", "grep"], // stdin-only safe binaries (NOT interpreters)
      safeBinTrustedDirs: ["/opt/custom/bin"],  // extra trusted directories for safe-bin path checks (built-in defaults: /bin and /usr/bin)
      safeBinProfiles: {        // optional custom argv policy per safe bin
        "grep": { minPositional: 1, maxPositional: 2, allowedValueFlags: ["-i", "-n"], deniedFlags: ["-r"] }
      },
      strictInlineEval: false,   // when true, inline eval always needs approval
      applyPatch: {              // enabled defaults to true; only set when you want to disable it
        workspaceOnly: true,
        allowModels: ["gpt-5.5"]
      }
    }
  }
}
```

`openclaw security audit` warns when interpreter/runtime `safeBins` entries are missing explicit profiles, and `openclaw doctor --fix` can scaffold missing `safeBinProfiles` entries.

### Session overrides

```
/exec host=auto security=allowlist ask=on-miss node=mac-1
```

### PATH handling

- `host=gateway`: merges login-shell PATH; `env.PATH` overrides rejected
- `host=sandbox`: runs `sh -lc` (login shell); `tools.exec.pathPrepend` applies
- `host=node`: only non-blocked env overrides sent; `env.PATH` rejected

### Security rules

- Manual allowlist matches **resolved binary paths only** (no basename matches)
- In `security=allowlist`: shell commands auto-allowed only if every pipeline segment is allowlisted or a safe bin
- Chaining (`;`, `&&`, `||`) rejected in allowlist mode unless every segment qualifies
- `tools.exec.safeBins`: for stdin-only stream filters — NOT for interpreters
- Do not add `python3`, `node`, `ruby`, `bash` to safeBins — use explicit allowlist entries

### Approval behavior

When approvals are required, exec returns immediately with `status: "approval-pending"` and an approval id. Once approved (or denied / timed out), the Gateway emits system events (`Exec finished` / `Exec denied`). A single `Exec running` notice is emitted if the command runs longer than `approvalRunningNoticeMs`. On channels with native approval cards/buttons, rely on that native UI first; only include a manual `/approve` command when the tool result explicitly says chat approvals are unavailable.

### apply_patch subtool

Multi-file patch tool for OpenAI/Codex models. Enabled by default; only configure when you want to disable it or restrict models:

```json5
{
  tools: {
    exec: {
      applyPatch: {             // enabled defaults to true
        workspaceOnly: true,    // default: true
        allowModels: ["gpt-5.5"]
      }
    }
  }
}
```

### Gotchas

- `OPENCLAW_SHELL=exec` is set in spawned environments for shell/profile detection
- Sandboxing is OFF by default — `host=auto` resolves to `gateway`
- For long work: start once, rely on automatic completion wake; use `process` for status
- Do not use sleep loops or repeated polling for background work
- Use cron for scheduled/delayed work (not exec sleep patterns)
- On non-Windows: uses `SHELL` env var; if fish, prefers `bash`/`sh`
- On Windows: prefers PowerShell 7 (`pwsh`), fallback to Windows PowerShell 5.1

---

## code_execution

Run sandboxed remote Python analysis on xAI's Responses API.

**Docs:** https://docs.openclaw.ai/tools/code-execution

Different from `exec`: runs remotely in xAI sandbox, not locally.

**Use for:** calculations, tabulation, quick statistics, chart-style analysis, analyzing data from `x_search`/`web_search`.

**Do NOT use for:** local files, your shell, your repo, paired devices (use `exec`).

### Setup

Requires `XAI_API_KEY` or `plugins.entries.xai.config.webSearch.apiKey`.

```json5
{
  plugins: {
    entries: {
      xai: {
        config: {
          codeExecution: {
            enabled: true,
            model: "grok-4-1-fast",
            maxTurns: 2,
            timeoutSeconds: 30
          }
        }
      }
    }
  }
}
```

Takes single `task` parameter; treat as ephemeral analysis, not persistent notebook.

---

## browser

OpenClaw-managed Chrome/Brave/Edge/Chromium profile isolated from personal browser.

**Docs:** https://docs.openclaw.ai/tools/browser

### Profiles

| Profile | Description |
|---|---|
| `openclaw` | Managed, isolated browser (default) |
| `user` | Built-in Chrome MCP attach for real signed-in Chrome |
| custom | Any named profile you define |

A bundled `browser-automation` skill provides the full operating loop (snapshot→act→resnapshot, stale-ref recovery, login/2FA/captcha blocker reporting).

### Quick start

```bash
openclaw browser --browser-profile openclaw status
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

### Configuration

```json5
{
  browser: {
    enabled: true,
    defaultProfile: "openclaw",
    color: "#FF4500",   // tints the browser UI so you can see which profile is active
    headless: false,
    noSandbox: false,
    attachOnly: false,
    executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    remoteCdpTimeoutMs: 1500,
    remoteCdpHandshakeTimeoutMs: 3000,
    localLaunchTimeoutMs: 15000,       // local managed Chrome discovery timeout
    localCdpReadyTimeoutMs: 8000,      // local managed post-launch CDP readiness timeout
    actionTimeoutMs: 60000,            // default browser act timeout
    tabCleanup: {
      enabled: true,
      idleMinutes: 120,                // 0 disables idle cleanup
      maxTabsPerSession: 8,            // 0 disables per-session cap
      sweepMinutes: 5
    },
    ssrfPolicy: {
      // dangerouslyAllowPrivateNetwork: true  // opt-in only
      // hostnameAllowlist: ["*.example.com"]
    },
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },  // port derived from gateway.port + 2 (default gateway port = 18789)
      work: { cdpPort: 18801, color: "#0066CC" },
      user: {
        driver: "existing-session",
        attachOnly: true,
        color: "#00AA00"
      },
      brave: {
        driver: "existing-session",
        attachOnly: true,
        userDataDir: "~/Library/Application Support/BraveSoftware/Brave-Browser",
        color: "#FB542B"
      },
      remote: { cdpUrl: "http://10.0.0.42:9222", color: "#00AA00" },
      browserless: {
        cdpUrl: "wss://production-sfo.browserless.io?token=<KEY>",
        color: "#00AA00"
      },
      browserbase: {
        cdpUrl: "wss://connect.browserbase.com?apiKey=<KEY>",
        color: "#F97316"
      }
    }
  }
}
```

### Setting executable path

```bash
openclaw config set browser.executablePath "/usr/bin/google-chrome"
```

### Plugin control

```json5
// Disable browser plugin (to replace with another)
{
  plugins: { entries: { browser: { enabled: false } } }
}

// Restore (if plugins.allow was blocking it)
{
  plugins: { allow: ["telegram", "browser"] }
}
```

### Tool parameters

| Action | Description |
|---|---|
| `status` | Check browser status |
| `start` | Launch the browser |
| `stop` | Stop the browser (for attach-only and remote CDP profiles, closes the active control session and releases Playwright/CDP emulation overrides such as viewport, color scheme, and locale — even though no browser process was launched) |
| `profiles` | List profiles |
| `tabs` | List open tabs |
| `open` | Open a URL |
| `focus` | Focus a tab |
| `close` | Close a tab |
| `snapshot` | Capture accessibility tree snapshot |
| `screenshot` | Capture screenshot |
| `navigate` | Navigate to URL |
| `console` | Get console logs |
| `pdf` | Export PDF |
| `upload` | Upload files |
| `dialog` | Handle dialogs |
| `act` | Perform actions (click, type, press, hover, drag, select, fill, resize, wait, evaluate, close) |

### act kinds

| Kind | Description |
|---|---|
| `click` | Click an element |
| `type` | Type text |
| `press` | Press a key |
| `hover` | Hover over element |
| `drag` | Drag from one element to another |
| `select` | Select dropdown option |
| `fill` | Fill an input field |
| `resize` | Resize the browser window |
| `wait` | Wait (use sparingly) |
| `evaluate` | Run JavaScript |
| `close` | Close tab/popup |

### Node browser proxy (zero-config for remote gateways)

- Runs on node host, accessible via proxy without extra browser config
- Configure `nodeHost.browserProxy.allowProfiles` to limit accessible profiles
- Disable on node: `nodeHost.browserProxy.enabled=false`
- Disable on gateway: `gateway.nodes.browser.mode="off"`

### CDP URL shapes supported

- `http(s)://host[:port]` — HTTP discovery via `/json/version`
- `ws://host[:port]/devtools/<kind>/<id>` — direct WebSocket
- `ws://host[:port]` — bare WebSocket root (tries HTTP discovery first, fallback to WebSocket)

### Security

- Browser control is loopback-only
- Shared-secret auth only (gateway token, `x-openclaw-password`, HTTP Basic)
- `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork` is OFF by default
- Remote CDP URLs are SSRF-guarded
- **Tailscale exception:** Tailscale Serve identity headers and `gateway.auth.mode: "trusted-proxy"` do NOT authenticate the standalone loopback browser HTTP API. Only shared-secret auth (gateway token bearer, `x-openclaw-password`, or HTTP Basic) is accepted for this API.

### Existing-session (Chrome DevTools MCP)

```json5
{
  browser: {
    profiles: {
      brave: {
        driver: "existing-session",
        attachOnly: true,
        userDataDir: "~/Library/Application Support/BraveSoftware/Brave-Browser",
        color: "#FB542B"
      }
    }
  }
}
```

Enable remote debugging in the browser: chrome/brave/edge → `inspect/#remote-debugging`

### Gotchas

- `plugins.allow` must include `browser` — tool policy runs after load
- Browser version 144+ required for Chromium-based browsers
- `driver: "existing-session"` uses Chrome DevTools MCP — do NOT set `cdpUrl`
- SSRF policy blocks private network by default; use `dangerouslyAllowPrivateNetwork: true` for LAN
- Browser config changes require gateway restart

---

## message (Agent Send)

Send messages across all channels.

**Docs:** https://docs.openclaw.ai/tools/agent-send

The `message` tool sends to channels. `openclaw agent` runs a single agent turn from CLI.

### CLI: openclaw agent

```bash
# Simple turn
openclaw agent --message "What is the weather today?"

# Target agent
openclaw agent --agent ops --message "Summarize logs"

# Target by phone
openclaw agent --to +15555550123 --message "Status update"

# Reuse session
openclaw agent --session-id abc123 --message "Continue"

# Deliver to channel
openclaw agent --to +15555550123 --message "Report ready" --deliver

# Deliver to Slack
openclaw agent --agent ops --message "Generate report" \
  --deliver --reply-channel slack --reply-to "#reports"
```

### CLI flags

| Flag | Description |
|---|---|
| `--message <text>` | Message to send (required) |
| `--to <dest>` | Derive session key from target (phone, chat id) |
| `--agent <id>` | Target a configured agent |
| `--session-id <id>` | Reuse existing session |
| `--local` | Force local embedded runtime |
| `--deliver` | Send reply to a chat channel |
| `--channel <name>` | Delivery channel |
| `--reply-to <target>` | Delivery target override |
| `--reply-channel <name>` | Delivery channel override |
| `--reply-account <id>` | Delivery account id override |
| `--thinking <level>` | Set thinking level |
| `--verbose <on\|full\|off>` | Verbose output |
| `--timeout <seconds>` | Agent timeout override |
| `--json` | Structured JSON output |

### message tool parameters (in-agent)

| Parameter | Description |
|---|---|
| `action` | `send`, `poll`, `react`, `delete`, `edit`, `topic-create`, `topic-edit` |
| `target` | Channel/user id or name |
| `message` | Message text |
| `channel` | Channel type (`telegram`, `whatsapp`, `discord`, etc.) |
| `media` | Media URL or local path |
| `buffer` | Base64 payload (data: URL supported) |
| `filePath` | Local file path |
| `caption` | Media caption |
| `replyTo` | Message ID to reply to |
| `asVoice` | Send as voice message (boolean) |
| `asDocument` | Send image/GIF as document (telegram only) |
| `silent` | Send without notification |
| `buttons` | Button rows for inline keyboards |

---

## image_generate

Generate or edit images using configured providers.

**Docs:** https://docs.openclaw.ai/tools/image-generation

### Quick start

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: { primary: "openai/gpt-image-2" }
    }
  }
}
```

Ask: *"Generate an image of a friendly robot mascot."*

### Supported providers

| Provider | Default model | Edit support | Auth |
|---|---|---|---|
| OpenAI | `gpt-image-2` | Yes (up to 4 images) | `OPENAI_API_KEY` or Codex OAuth |
| OpenRouter | `google/gemini-3.1-flash-image-preview` | Yes (up to 5 images) | `OPENROUTER_API_KEY` |
| Google | `gemini-3.1-flash-image-preview` | Yes | `GEMINI_API_KEY` |
| fal | `fal-ai/flux/dev` | Yes | `FAL_KEY` |
| MiniMax | `image-01` | Yes (1 image, subject ref) | `MINIMAX_API_KEY` |
| ComfyUI | `workflow` | Yes (1 image, workflow) | `COMFY_API_KEY` |
| Vydra | `grok-imagine` | No | `VYDRA_API_KEY` |
| xAI | `grok-imagine-image` | Yes (up to 5 images) | `XAI_API_KEY` |

### Tool parameters

| Parameter | Type | Description |
|---|---|---|
| `prompt` | string (required) | Image description |
| `action` | `generate` \| `list` | `list` to inspect providers |
| `model` | string | Provider/model override (`openai/gpt-image-2`) |
| `image` | string | Single reference image path/URL |
| `images` | string[] | Multiple reference images (up to 5) |
| `size` | string | `1024x1024`, `1536x1024`, `3840x2160`, etc. |
| `aspectRatio` | string | `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` |
| `resolution` | string | `1K`, `2K`, `4K` |
| `quality` | string | `low`, `medium`, `high`, `auto` |
| `outputFormat` | string | `png`, `jpeg`, `webp` |
| `count` | number | Number of images (1–4) |
| `timeoutMs` | number | Timeout in ms |
| `filename` | string | Output filename hint |
| `openai` | object | OpenAI-only: `background`, `moderation`, `outputCompression`, `user` |

### Provider selection order

1. `model` parameter in tool call
2. `imageGenerationModel.primary` in config
3. `imageGenerationModel.fallbacks` in order
4. Auto-detection (auth-backed providers)

### Configuration

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: {
        primary: "openai/gpt-image-2",
        fallbacks: [
          "openrouter/google/gemini-3.1-flash-image-preview",
          "google/gemini-3.1-flash-image-preview",
          "fal/fal-ai/flux/dev"
        ]
      }
    }
  }
}
```

### List providers at runtime

```
/tool image_generate action=list
```

### OpenAI-specific options

```json
{
  "quality": "low",
  "outputFormat": "jpeg",
  "openai": {
    "background": "opaque",        // transparent | opaque | auto
    "moderation": "low",
    "outputCompression": 60,       // for JPEG/WebP
    "user": "end-user-42"
  }
}
```

`background: "transparent"` requires `outputFormat: "png"` or `"webp"`.

### Examples

```
# Generate 4K landscape
/tool image_generate model=openai/gpt-image-2 prompt="editorial poster" size=3840x2160 count=1

# Edit reference image
/tool image_generate model=openai/gpt-image-2 prompt="Replace background with studio" image=/path/to/ref.png size=1024x1536

# Multi-reference edit
/tool image_generate model=openai/gpt-image-2 prompt="Combine character from first, palette from second" images='["/char.png","/palette.jpg"]'
```

### Provider capabilities

| Capability | OpenAI | Google | fal | MiniMax | ComfyUI | xAI |
|---|---|---|---|---|---|---|
| Max generate | 4 | 4 | 4 | 9 | workflow | 4 |
| Edit/reference | Up to 5 | Up to 5 | 1 | 1 | 1 | Up to 5 |
| Size control | Yes (4K) | Yes | Yes | No | No | No |
| Aspect ratio | No | Yes | Yes | Yes | No | Yes |
| Resolution 1K/2K/4K | No | Yes | Yes | No | No | Yes (1K/2K) |

---

## video_generate

Generate videos from text prompts, reference images, or existing videos.

**Docs:** https://docs.openclaw.ai/tools/video-generation

### Supported providers (14 total)

| Provider | Default model | Auth |
|---|---|---|
| Alibaba | `wan2.6-t2v` | `MODELSTUDIO_API_KEY` |
| BytePlus (1.0) | `seedance-1-0-pro-250528` | `BYTEPLUS_API_KEY` |
| BytePlus Seedance 1.5 | `seedance-1-5-pro-251215` | `BYTEPLUS_API_KEY` |
| BytePlus Seedance 2.0 | `dreamina-seedance-2-0-260128` | `BYTEPLUS_API_KEY` |
| ComfyUI | `workflow` | `COMFY_API_KEY` |
| fal | `fal-ai/minimax/video-01-live` | `FAL_KEY` |
| Google | `veo-3.1-fast-generate-preview` | `GEMINI_API_KEY` |
| MiniMax | `MiniMax-Hailuo-2.3` | `MINIMAX_API_KEY` |
| OpenAI | `sora-2` | `OPENAI_API_KEY` |
| Qwen | `wan2.6-t2v` | `QWEN_API_KEY` |
| Runway | `gen4.5` | `RUNWAYML_API_SECRET` |
| Together | `Wan-AI/Wan2.2-T2V-A14B` | `TOGETHER_API_KEY` |
| Vydra | `veo3` | `VYDRA_API_KEY` |
| xAI | `grok-imagine-video` | `XAI_API_KEY` |

### Runtime modes

| Mode | When |
|---|---|
| `generate` | Text-to-video (no reference media) |
| `imageToVideo` | Request includes image reference(s) |
| `videoToVideo` | Request includes video reference(s) |

### Tool parameters

| Parameter | Type | Description |
|---|---|---|
| `prompt` | string (required for generate) | Video description |
| `action` | string | `generate`, `status`, `list` |
| `model` | string | Provider/model override |
| `image` | string | Single reference image |
| `images` | string[] | Multiple reference images (up to 9) |
| `imageRoles` | string[] | Role per image: `first_frame`, `last_frame`, `reference_image` |
| `video` | string | Single reference video |
| `videos` | string[] | Multiple reference videos (up to 4) |
| `videoRoles` | string[] | Role per video: `reference_video` |
| `audioRef` | string | Reference audio |
| `audioRefs` | string[] | Multiple reference audios (up to 3) |
| `audioRoles` | string[] | Role per audio: `reference_audio` |
| `aspectRatio` | string | `1:1`, `2:3`, `3:2`, `4:3`, `9:16`, `16:9`, `21:9`, `adaptive` |
| `resolution` | string | `480P`, `720P`, `768P`, `1080P` |
| `durationSeconds` | number | Target duration (rounded to nearest supported) |
| `size` | string | Size hint |
| `audio` | boolean | Enable generated audio in output |
| `watermark` | boolean | Toggle provider watermarking |
| `filename` | string | Output filename hint |
| `timeoutMs` | number | Request timeout |
| `providerOptions` | object | Provider-specific options (`{"seed": 42, "draft": true}`) |

### Configuration

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "google/veo-3.1-fast-generate-preview",
        fallbacks: ["together/Wan-AI/Wan2.2-T2V-A14B"]
      }
    }
  }
}
```

### How video generation works

1. Agent calls `video_generate` → OpenClaw submits request, returns task ID immediately
2. Provider processes in background (30 seconds to 5 minutes)
3. When ready, OpenClaw wakes same session with completion event
4. Agent posts finished video to conversation

### Check status

```bash
openclaw tasks list
openclaw tasks show <taskId>
openclaw tasks cancel <taskId>
```

Or in-agent:
```
video_generate action=status
```

### Task states

1. **queued** — waiting for provider to accept
2. **running** — provider processing
3. **succeeded** — video ready; agent wakes and posts
4. **failed** — provider error or timeout

### List providers

```
video_generate action=list
```

### `adaptive` aspect ratio

Some providers (BytePlus Seedance) use `adaptive` to auto-detect ratio from input image. Not supported by all providers.

---

## music_generate

Generate music or audio using configured providers.

**Docs:** https://docs.openclaw.ai/tools/music-generation

### Supported providers

| Provider | Default model | Reference inputs | Auth |
|---|---|---|---|
| ComfyUI | `workflow` | Up to 1 image | `COMFY_API_KEY` |
| Google | `lyria-3-clip-preview` | Up to 10 images | `GEMINI_API_KEY` |
| MiniMax | `music-2.6` | None | `MINIMAX_API_KEY` |

### Configuration

```json5
{
  agents: {
    defaults: {
      musicGenerationModel: { primary: "google/lyria-3-clip-preview" }
    }
  }
}
```

Also `google/lyria-3-pro-preview` supports both MP3 and WAV. Works as async background task (same pattern as video_generate).

---

## tts

One-shot text-to-speech conversion.

**Docs:** https://docs.openclaw.ai/tools/tts

### Supported providers

- **ElevenLabs** (`ELEVENLABS_API_KEY` or `XI_API_KEY`)
- **Google Gemini** (`GEMINI_API_KEY`)
- **Gradium** (`GRADIUM_API_KEY`)
- **Local CLI** (no API key — runs a configured local TTS command)
- **Microsoft** (no API key — uses `node-edge-tts`, hosted service, best-effort)
- **MiniMax** (`MINIMAX_API_KEY`; also accepts Token Plan via `MINIMAX_OAUTH_TOKEN`, `MINIMAX_CODE_PLAN_KEY`, `MINIMAX_CODING_API_KEY`)
- **OpenAI** (`OPENAI_API_KEY`)
- **Vydra** (`VYDRA_API_KEY`)
- **xAI** (`XAI_API_KEY`)
- **Xiaomi MiMo** (`XIAOMI_API_KEY`)

### Enabling TTS

Auto-TTS is **OFF by default**. Enable:

```json5
{
  messages: {
    tts: {
      auto: "always",   // off | always | inbound | tagged
      provider: "elevenlabs"
    }
  }
}
```

Or toggle in chat: `/tts on`

### `auto` modes

| Value | Description |
|---|---|
| `off` | Disabled |
| `always` | Always generate audio |
| `inbound` | Only after inbound voice message |
| `tagged` | Only when reply includes `[[tts:...]]` directives |

### Config examples

```json5
// OpenAI primary with ElevenLabs fallback
{
  messages: {
    tts: {
      auto: "always",
      provider: "openai",
      providers: {
        openai: {
          model: "gpt-4o-mini-tts",
          voice: "coral"
        },
        elevenlabs: {
          voiceId: "voice_id",
          modelId: "eleven_multilingual_v2",
          voiceSettings: {
            stability: 0.5,
            similarityBoost: 0.75,
            speed: 1.0
          }
        }
      }
    }
  }
}

// Microsoft (no API key)
{
  messages: {
    tts: {
      auto: "always",
      provider: "microsoft",
      providers: {
        microsoft: {
          voice: "en-US-MichelleNeural",
          lang: "en-US",
          outputFormat: "audio-24khz-48kbitrate-mono-mp3",
          rate: "+10%",
          pitch: "-5%"
        }
      }
    }
  }
}

// MiniMax
{
  messages: {
    tts: {
      auto: "always",
      provider: "minimax",
      providers: {
        minimax: {
          model: "speech-2.8-hd",
          voiceId: "English_expressive_narrator",
          speed: 1.0,
          vol: 1.0,
          pitch: 0
        }
      }
    }
  }
}

// Google Gemini
{
  messages: {
    tts: {
      auto: "always",
      provider: "google",
      providers: {
        google: {
          model: "gemini-3.1-flash-tts-preview",
          voiceName: "Kore"
        }
      }
    }
  }
}

// xAI
{
  messages: {
    tts: {
      auto: "always",
      provider: "xai",
      providers: {
        xai: {
          voiceId: "eve",
          language: "en",
          responseFormat: "mp3",
          speed: 1.0
        }
      }
    }
  }
}
```

### Key config fields

| Field | Description |
|---|---|
| `auto` | `off\|always\|inbound\|tagged` |
| `provider` | Provider id |
| `summaryModel` | Model for auto-summarizing long replies |
| `maxTextLength` | Hard cap for TTS input |
| `timeoutMs` | Request timeout |
| `prefsPath` | Local prefs JSON path |
| `mode` | `final` (default) or `all` (includes tool/block replies) |

### Model-driven directives

Model can emit TTS directives for per-reply overrides:

```
Here you go.

[[tts:voiceId=pMsXgVXv3BLzUgSXRplE model=eleven_v3 speed=1.1]]
[[tts:text]](laughs) Read the song once more.[[/tts:text]]
```

Available directive keys: `provider`, `voice`, `voiceId`, `voiceName`, `model`, `stability`, `similarityBoost`, `style`, `speed`, `useSpeakerBoost`, `vol`, `pitch`, `applyTextNormalization`, `languageCode`, `seed`

Disable all model overrides:
```json5
{
  messages: { tts: { modelOverrides: { enabled: false } } }
}
```

Allow provider switching:
```json5
{
  messages: { tts: { modelOverrides: { enabled: true, allowProvider: true } } }
}
```

### Output formats by channel

| Channel | Format |
|---|---|
| Telegram / WhatsApp / Matrix | Opus voice message |
| Other channels | MP3 |
| MiniMax | MP3 only |
| Google Gemini | WAV for attachments, PCM for telephony |
| Gradium | WAV/Opus/ulaw |
| xAI | MP3 default (configurable) |
| Microsoft | Configured `outputFormat` (default: mp3) |

### Slash commands

```
/tts off
/tts on
/tts status
/tts provider openai
/tts limit 2000
/tts summary off
/tts audio Hello from OpenClaw
```

On Discord, use `/voice` (Discord has its own `/tts`).

### Auto-TTS behavior

- Skips if reply already has media or `MEDIA:` directive
- Skips very short replies (< 10 chars)
- Summarizes long replies when enabled using `summaryModel`
- Audio attached to reply

---

## web_fetch

Fetch a URL and extract readable content (HTML → markdown/text). Does NOT execute JavaScript.

**Docs:** https://docs.openclaw.ai/tools/web-fetch

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string (required) | — | HTTP(S) URL to fetch |
| `extractMode` | string | `markdown` | `markdown` or `text` |
| `maxChars` | number | — | Max output characters |

### How it works

1. HTTP GET with Chrome-like User-Agent
2. Runs Readability (main-content extraction)
3. Optional Firecrawl fallback for bot-circumvention
4. 15-minute cache

### Config

```json5
{
  tools: {
    web: {
      fetch: {
        enabled: true,
        provider: "firecrawl",  // optional fallback
        maxChars: 50000,
        maxCharsCap: 50000,
        maxResponseBytes: 2000000,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
        maxRedirects: 3,
        readability: true,
        userAgent: "Mozilla/5.0 ..."
      }
    }
  }
}
```

### Firecrawl fallback

```json5
{
  tools: { web: { fetch: { provider: "firecrawl" } } },
  plugins: {
    entries: {
      firecrawl: {
        enabled: true,
        config: {
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

### Limits & safety

- `maxChars` clamped to `maxCharsCap`
- Private/internal hostnames blocked
- Redirects checked and limited

---

## sessions_spawn (Sub-agents)

Spawn background agent runs from an existing agent run.

**Docs:** https://docs.openclaw.ai/tools/subagents

### Slash commands

```
/subagents list
/subagents kill <id|#|all>
/subagents log <id|#> [limit] [tools]
/subagents info <id|#>
/subagents send <id|#> <message>
/subagents steer <id|#> <message>
/subagents spawn <agentId> <task> [--model <model>] [--thinking <level>]
```

### Tool parameters (sessions_spawn)

| Parameter | Type | Description |
|---|---|---|
| `task` | string (required) | Task for the sub-agent |
| `label` | string | Optional label |
| `agentId` | string | Target agent id |
| `model` | string | Override sub-agent model |
| `thinking` | string | Override thinking level |
| `runTimeoutSeconds` | number | Abort after N seconds (0 = no timeout) |
| `thread` | boolean | Request thread binding |
| `mode` | `run\|session` | `run` (default) or `session` (requires `thread: true`) |
| `cleanup` | `delete\|keep` | Archive behavior (default: `keep`) |
| `sandbox` | `inherit\|require` | Sandbox inheritance |
| `context` | `isolated\|fork` | Context mode (default: `isolated`) |
| `runtime` | string | Set to `"acp"` for ACP harness sessions (Codex, Claude Code, Gemini CLI) |

### Context modes

| Mode | When to use |
|---|---|
| `isolated` | Fresh research, independent implementation (default, lower tokens) |
| `fork` | Work depending on current conversation, prior tool results |

Use `fork` sparingly — only when child needs current transcript.

### Configuration

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxSpawnDepth: 2,          // allow sub-agents to spawn children (default: 1)
        maxChildrenPerAgent: 5,    // max active children per session (default: 5)
        maxConcurrent: 8,          // global concurrency lane cap (default: 8)
        runTimeoutSeconds: 900,    // default timeout when omitted (0 = no timeout)
        model: "anthropic/claude-sonnet-4-6",  // sub-agent model (per-agent list[] override wins)
        archiveAfterMinutes: 60,   // auto-archive after N minutes
        allowAgents: ["*"],        // allowed target agent ids
        requireAgentId: false      // force explicit agentId
      }
    }
  }
}
```

### Depth levels

| Depth | Session key | Role | Can spawn? |
|---|---|---|---|
| 0 | `agent:<id>:main` | Main agent | Always |
| 1 | `agent:<id>:subagent:<uuid>` | Sub-agent (orchestrator when depth 2 allowed) | Only if `maxSpawnDepth >= 2` |
| 2 | `agent:<id>:subagent:<uuid>:subagent:<uuid>` | Leaf worker | Never |

### Tool policy by depth

- **Depth 1 (orchestrator, when `maxSpawnDepth >= 2`)**: Gets `sessions_spawn`, `subagents`, `sessions_list`, `sessions_history` so it can manage its children
- **Depth 1 (leaf, when `maxSpawnDepth == 1`)**: No session tools (default)
- **Depth 2 (leaf)**: No session tools; `sessions_spawn` always denied

### Announce behavior

Sub-agents report back via announce step:
- Posts result to requester chat channel
- `ANNOUNCE_SKIP` → nothing posted
- `NO_REPLY` / `no_reply` → announce suppressed
- Includes: result, status, runtime/token stats, session key, transcript path
- **Delivery resilience:** Direct `agent` delivery is attempted first with a stable idempotency key; if that fails, falls back to queue routing; if queue routing is unavailable, retries with short exponential backoff before final give-up.

### sessions_history sanitization

`sessions_history` applies safety filtering before returning transcript content:
- Strips thinking tags
- Strips `<relevant-memories>` / `<relevant_memories>` scaffolding blocks
- Strips plain-text tool-call XML payload blocks (`<tool_call>...</tool_call>`, `<function_calls>...</function_calls>`, etc.)
- Strips leaked model control tokens (`<|assistant|>`, `<|...|>`, `<｜...｜>` variants)
- Strips malformed MiniMax tool-call XML
- Redacts credential/token-like text
- Long blocks may be truncated; very large histories can drop older rows

For the full raw byte-for-byte transcript, inspect the file on disk directly.

### sessions_yield tool

`sessions_yield` ends the current turn and waits for subagent results to be announced back. It is available in the `group:sessions` tool group. Use it after spawning subagents to receive their results as the next message rather than busy-polling.

### Cascade stop

- `/stop` in main chat → stops all depth-1 agents + cascades to depth-2
- `/subagents kill <id>` → stops specific sub-agent + cascades to children

### Thread bindings (Discord)

```json5
{
  channels: {
    discord: {
      threadBindings: {
        enabled: true,
        idleHours: 1,
        maxAgeHours: 24,
        spawnSubagentSessions: true
      }
    }
  }
}
```

```
/focus <subagent-label>
/unfocus
/agents
/session idle <duration|off>
/session max-age <duration|off>
```

### Cost

Each sub-agent has its OWN context and token usage. Set cheaper model for sub-agents:

```json5
{
  agents: {
    defaults: {
      subagents: { model: "anthropic/claude-haiku-4-5" }
    }
  }
}
```

---

## web_search

Search the web using configured provider.

**Docs:** https://docs.openclaw.ai/tools/web

### Providers

| Provider | Result style | API key |
|---|---|---|
| Brave | Structured snippets | `BRAVE_API_KEY` |
| DuckDuckGo | Structured snippets | None (key-free) |
| Exa | Structured + extracted | `EXA_API_KEY` |
| Firecrawl | Structured snippets | `FIRECRAWL_API_KEY` |
| Gemini | AI-synthesized + citations | `GEMINI_API_KEY` |
| Grok (xAI) | AI-synthesized + citations | `XAI_API_KEY` |
| Kimi | AI-synthesized + citations | `KIMI_API_KEY` |
| MiniMax Search | Structured snippets | `MINIMAX_CODE_PLAN_KEY` |
| Ollama | Structured snippets | None (requires `ollama signin`) |
| Perplexity | Structured snippets | `PERPLEXITY_API_KEY` |
| SearXNG | Structured snippets | None (self-hosted) |
| Tavily | Structured snippets | `TAVILY_API_KEY` |

### Auto-detection order

1. Brave (order 10)
2. MiniMax Search (order 15)
3. Gemini (order 20)
4. Grok (order 30)
5. Kimi (order 40)
6. Perplexity (order 50)
7. Firecrawl (order 60)
8. Exa (order 65)
9. Tavily (order 70)
10. DuckDuckGo (order 100, key-free)
11. Ollama Web Search (order 110, key-free)
12. SearXNG (order 200)

### Config

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        provider: "brave",   // or omit for auto-detection
        maxResults: 5,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15
      }
    }
  }
}
```

### Store API key

```json5
{
  plugins: {
    entries: {
      brave: {
        config: {
          webSearch: { apiKey: "YOUR_KEY" }
        }
      }
    }
  }
}
```

Or set env var: `export BRAVE_API_KEY="YOUR_KEY"`

### Tool parameters

| Parameter | Description |
|---|---|
| `query` | Search query (required) |
| `count` | Results 1-10 (default: 5) |
| `country` | ISO country code (`US`, `DE`) |
| `language` | ISO 639-1 language (`en`, `de`) |
| `freshness` | `day`, `week`, `month`, `year` |
| `date_after` | YYYY-MM-DD |
| `date_before` | YYYY-MM-DD |
| `domain_filter` | Domain allowlist/denylist (Perplexity only) |
| `max_tokens` | Content budget (Perplexity only) |

### x_search (X/Twitter search via xAI)

```json5
{
  plugins: {
    entries: {
      xai: {
        config: {
          xSearch: {
            enabled: true,
            model: "grok-4-1-fast",
            inlineCitations: false,
            maxTurns: 2,
            timeoutSeconds: 30,
            cacheTtlMinutes: 15
          }
        }
      }
    }
  }
}
```

x_search parameters: `query`, `allowed_x_handles`, `excluded_x_handles`, `from_date`, `to_date`, `enable_image_understanding`, `enable_video_understanding`

### Native OpenAI web search

Direct OpenAI Responses models use OpenAI's hosted `web_search` tool automatically when `tools.web.search.enabled: true` and no provider is pinned.

### Native Codex web search

```json5
{
  tools: {
    web: {
      search: {
        openaiCodex: {
          enabled: true,
          mode: "cached",
          allowedDomains: ["example.com"],
          contextSize: "high",
          userLocation: {
            country: "US",
            city: "New York",
            timezone: "America/New_York"
          }
        }
      }
    }
  }
}
```

---

## Tool Configuration

### Allow and deny lists

```json5
{
  tools: {
    allow: ["group:fs", "browser", "web_search"],
    deny: ["exec"]
  }
}
```

Deny always wins over allow.

### Tool profiles

```json5
{
  tools: { profile: "coding" }  // full | coding | messaging | minimal
}
```

| Profile | Includes |
|---|---|
| `full` | No restriction |
| `coding` | fs, runtime, web, sessions, memory, cron, image, image_generate, music_generate, video_generate |
| `messaging` | group:messaging, sessions_list, sessions_history, sessions_send, session_status |
| `minimal` | session_status only |

### Tool groups

| Group | Tools |
|---|---|
| `group:runtime` | exec, process, code_execution |
| `group:fs` | read, write, edit, apply_patch |
| `group:sessions` | sessions_list, sessions_history, sessions_send, sessions_spawn, sessions_yield, subagents, session_status |
| `group:memory` | memory_search, memory_get |
| `group:web` | web_search, x_search, web_fetch |
| `group:ui` | browser, canvas |
| `group:automation` | cron, gateway |
| `group:messaging` | message |
| `group:nodes` | nodes |
| `group:agents` | agents_list |
| `group:media` | image, image_generate, music_generate, video_generate, tts |
| `group:openclaw` | All built-in tools (excludes plugin tools) |

### Provider-specific tool restrictions

```json5
{
  tools: {
    profile: "coding",
    byProvider: {
      "google-antigravity": { profile: "minimal" }
    }
  }
}
```

---

## gateway tool

Owner-only runtime tool for gateway operations:

| Action | Purpose |
|---|---|
| `config.schema.lookup` | One path-scoped config subtree before edits |
| `config.get` | Current config snapshot + hash |
| `config.patch` | Partial config updates with restart |
| `config.apply` | Full config replacement (use sparingly) |
| `update.run` | Explicit self-update + restart |

⚠️ `config.patch` is preferred over `config.apply`. The gateway tool refuses to change `tools.exec.ask` or `tools.exec.security`.

---

## memory_search / memory_get

Search memory files in MEMORY.md and memory/*.md.

```json5
{
  // Configure memory slot
  plugins: {
    slots: {
      memory: "memory-core"  // or "memory-lancedb" for long-term memory
    }
  }
}
```

`memory-lancedb` provides install-on-demand long-term memory with auto-recall/capture.

---

## session_status

Lightweight status readback tool:

- Answers `/status`-style questions about current session
- Can set per-session model override (`model=default` to clear)
- Backfills sparse token/cache counters from latest transcript usage entry

---

## Plugin-provided tools (examples)

| Tool | Plugin | Description |
|---|---|---|
| `web_search` (SearXNG) | `searxng` | Self-hosted meta-search |
| `firecrawl_search` / `firecrawl_scrape` | `firecrawl` | Deep web extraction |
| `tavily_search` / `tavily_extract` | `tavily` | Structured search + URL extraction |
| Music generation tools | `minimax`, `google` | Music generation |
| Diffs | `diffs` | Diff viewer |
| Lobster | `lobster` | Typed workflow runtime |
| LLM Task | `llm-task` | JSON-only LLM structured output |
| Tokenjuice | `tokenjuice` | Compact noisy exec output |
