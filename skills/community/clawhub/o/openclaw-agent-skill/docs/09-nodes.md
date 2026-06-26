# Nodes & Devices

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 8

---

<!-- SOURCE: https://docs.openclaw.ai/nodes/troubleshooting -->

# Node Troubleshooting - OpenClaw

Use this page when a node is visible in status but node tools fail.

## Command ladder

```
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Then run node specific checks:

```
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
openclaw approvals get --node <idOrNameOrIp>
```

Healthy signals:

*   Node is connected and paired for role `node`.
*   `nodes describe` includes the capability you are calling.
*   Exec approvals show expected mode/allowlist.

## Foreground requirements

`canvas.*`, `camera.*`, and `screen.*` are foreground only on iOS/Android nodes. Quick check and fix:

```
openclaw nodes describe --node <idOrNameOrIp>
openclaw nodes canvas snapshot --node <idOrNameOrIp>
openclaw logs --follow
```

If you see `NODE_BACKGROUND_UNAVAILABLE`, bring the node app to the foreground and retry.

## Permissions matrix

| Capability | iOS | Android | macOS node app | Typical failure code |
| --- | --- | --- | --- | --- |
| `camera.snap`, `camera.clip` | Camera (+ mic for clip audio) | Camera (+ mic for clip audio) | Camera (+ mic for clip audio) | `*_PERMISSION_REQUIRED` |
| `screen.record` | Screen Recording (+ mic optional) | Screen capture prompt (+ mic optional) | Screen Recording | `*_PERMISSION_REQUIRED` |
| `location.get` | While Using or Always (depends on mode) | Foreground/Background location based on mode | Location permission | `LOCATION_PERMISSION_REQUIRED` |
| `system.run` | n/a (node host path) | n/a (node host path) | Exec approvals required | `SYSTEM_RUN_DENIED` |

## Pairing versus approvals

These are different gates:

1.  **Device pairing**: can this node connect to the gateway?
2.  **Exec approvals**: can this node run a specific shell command?

Quick checks:

```
openclaw devices list
openclaw nodes status
openclaw approvals get --node <idOrNameOrIp>
openclaw approvals allowlist add --node <idOrNameOrIp> "/usr/bin/uname"
```

If pairing is missing, approve the node device first. If pairing is fine but `system.run` fails, fix exec approvals/allowlist.

## Common node error codes

*   `NODE_BACKGROUND_UNAVAILABLE` → app is backgrounded; bring it foreground.
*   `CAMERA_DISABLED` → camera toggle disabled in node settings.
*   `*_PERMISSION_REQUIRED` → OS permission missing/denied.
*   `LOCATION_DISABLED` → location mode is off.
*   `LOCATION_PERMISSION_REQUIRED` → requested location mode not granted.
*   `LOCATION_BACKGROUND_UNAVAILABLE` → app is backgrounded but only While Using permission exists.
*   `SYSTEM_RUN_DENIED: approval required` → exec request needs explicit approval.
*   `SYSTEM_RUN_DENIED: allowlist miss` → command blocked by allowlist mode. On Windows node hosts, shell-wrapper forms like `cmd.exe /c ...` are treated as allowlist misses in allowlist mode unless approved via ask flow.

## Fast recovery loop

```
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
openclaw approvals get --node <idOrNameOrIp>
openclaw logs --follow
```

If still stuck:

*   Re-approve device pairing.
*   Re-open node app (foreground).
*   Re-grant OS permissions.
*   Recreate/adjust exec approval policy.

Related:

*   [/nodes/index](https://docs.openclaw.ai/nodes/index)
*   [/nodes/camera](https://docs.openclaw.ai/nodes/camera)
*   [/nodes/location-command](https://docs.openclaw.ai/nodes/location-command)
*   [/tools/exec-approvals](https://docs.openclaw.ai/tools/exec-approvals)
*   [/gateway/pairing](https://docs.openclaw.ai/gateway/pairing)

---

<!-- SOURCE: https://docs.openclaw.ai/nodes/media-understanding -->

# Media Understanding - OpenClaw

## Media Understanding (Inbound) — 2026-01-17

OpenClaw can **summarize inbound media** (image/audio/video) before the reply pipeline runs. It auto‑detects when local tools or provider keys are available, and can be disabled or customized. If understanding is off, models still receive the original files/URLs as usual.

## Goals

*   Optional: pre‑digest inbound media into short text for faster routing + better command parsing.
*   Preserve original media delivery to the model (always).
*   Support **provider APIs** and **CLI fallbacks**.
*   Allow multiple models with ordered fallback (error/size/timeout).

## High‑level behavior

1.  Collect inbound attachments (`MediaPaths`, `MediaUrls`, `MediaTypes`).
2.  For each enabled capability (image/audio/video), select attachments per policy (default: **first**).
3.  Choose the first eligible model entry (size + capability + auth).
4.  If a model fails or the media is too large, **fall back to the next entry**.
5.  On success:
    *   `Body` becomes `[Image]`, `[Audio]`, or `[Video]` block.
    *   Audio sets `{{Transcript}}`; command parsing uses caption text when present, otherwise the transcript.
    *   Captions are preserved as `User text:` inside the block.

If understanding fails or is disabled, **the reply flow continues** with the original body + attachments.

## Config overview

`tools.media` supports **shared models** plus per‑capability overrides:

*   `tools.media.models`: shared model list (use `capabilities` to gate).
*   `tools.media.image` / `tools.media.audio` / `tools.media.video`:
    *   defaults (`prompt`, `maxChars`, `maxBytes`, `timeoutSeconds`, `language`)
    *   provider overrides (`baseUrl`, `headers`, `providerOptions`)
    *   Deepgram audio options via `tools.media.audio.providerOptions.deepgram`
    *   audio transcript echo controls (`echoTranscript`, default `false`; `echoFormat`)
    *   optional **per‑capability `models` list** (preferred before shared models)
    *   `attachments` policy (`mode`, `maxAttachments`, `prefer`)
    *   `scope` (optional gating by channel/chatType/session key)
*   `tools.media.concurrency`: max concurrent capability runs (default **2**).

```
{
  tools: {
    media: {
      models: [
        /* shared list */
      ],
      image: {
        /* optional overrides */
      },
      audio: {
        /* optional overrides */
        echoTranscript: true,
        echoFormat: '📝 "{transcript}"',
      },
      video: {
        /* optional overrides */
      },
    },
  },
}
```

### Model entries

Each `models[]` entry can be **provider** or **CLI**:

```
{
  type: "provider", // default if omitted
  provider: "openai",
  model: "gpt-5.2",
  prompt: "Describe the image in <= 500 chars.",
  maxChars: 500,
  maxBytes: 10485760,
  timeoutSeconds: 60,
  capabilities: ["image"], // optional, used for multi‑modal entries
  profile: "vision-profile",
  preferredProfile: "vision-fallback",
}
```

```
{
  type: "cli",
  command: "gemini",
  args: [
    "-m",
    "gemini-3-flash",
    "--allowed-tools",
    "read_file",
    "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
  ],
  maxChars: 500,
  maxBytes: 52428800,
  timeoutSeconds: 120,
  capabilities: ["video", "image"],
}
```

CLI templates can also use:

*   `{{MediaDir}}` (directory containing the media file)
*   `{{OutputDir}}` (scratch dir created for this run)
*   `{{OutputBase}}` (scratch file base path, no extension)

## Defaults and limits

Recommended defaults:

*   `maxChars`: **500** for image/video (short, command‑friendly)
*   `maxChars`: **unset** for audio (full transcript unless you set a limit)
*   `maxBytes`:
    *   image: **10MB**
    *   audio: **20MB**
    *   video: **50MB**

Rules:

*   If media exceeds `maxBytes`, that model is skipped and the **next model is tried**.
*   Audio files smaller than **1024 bytes** are treated as empty/corrupt and skipped before provider/CLI transcription.
*   If the model returns more than `maxChars`, output is trimmed.
*   `prompt` defaults to simple “Describe the .” plus the `maxChars` guidance (image/video only).
*   If `<capability>.enabled: true` but no models are configured, OpenClaw tries the **active reply model** when its provider supports the capability.

### Auto-detect media understanding (default)

If `tools.media.<capability>.enabled` is **not** set to `false` and you haven’t configured models, OpenClaw auto-detects in this order and **stops at the first working option**:

1.  **Local CLIs** (audio only; if installed)
    *   `sherpa-onnx-offline` (requires `SHERPA_ONNX_MODEL_DIR` with encoder/decoder/joiner/tokens)
    *   `whisper-cli` (`whisper-cpp`; uses `WHISPER_CPP_MODEL` or the bundled tiny model)
    *   `whisper` (Python CLI; downloads models automatically)
2.  **Gemini CLI** (`gemini`) using `read_many_files`
3.  **Provider keys**
    *   Audio: OpenAI → Groq → Deepgram → Google
    *   Image: OpenAI → Anthropic → Google → MiniMax
    *   Video: Google

To disable auto-detection, set:

```
{
  tools: {
    media: {
      audio: {
        enabled: false,
      },
    },
  },
}
```

Note: Binary detection is best-effort across macOS/Linux/Windows; ensure the CLI is on `PATH` (we expand `~`), or set an explicit CLI model with a full command path.

### Proxy environment support (provider models)

When provider-based **audio** and **video** media understanding is enabled, OpenClaw honors standard outbound proxy environment variables for provider HTTP calls:

*   `HTTPS_PROXY`
*   `HTTP_PROXY`
*   `https_proxy`
*   `http_proxy`

If no proxy env vars are set, media understanding uses direct egress. If the proxy value is malformed, OpenClaw logs a warning and falls back to direct fetch.

## Capabilities (optional)

If you set `capabilities`, the entry only runs for those media types. For shared lists, OpenClaw can infer defaults:

*   `openai`, `anthropic`, `minimax`: **image**
*   `google` (Gemini API): **image + audio + video**
*   `groq`: **audio**
*   `deepgram`: **audio**

For CLI entries, **set `capabilities` explicitly** to avoid surprising matches. If you omit `capabilities`, the entry is eligible for the list it appears in.

## Provider support matrix (OpenClaw integrations)

| Capability | Provider integration | Notes |
| --- | --- | --- |
| Image | OpenAI / Anthropic / Google / others via `pi-ai` | Any image-capable model in the registry works. |
| Audio | OpenAI, Groq, Deepgram, Google, Mistral | Provider transcription (Whisper/Deepgram/Gemini/Voxtral). |
| Video | Google (Gemini API) | Provider video understanding. |

## Model selection guidance

*   Prefer the strongest latest-generation model available for each media capability when quality and safety matter.
*   For tool-enabled agents handling untrusted inputs, avoid older/weaker media models.
*   Keep at least one fallback per capability for availability (quality model + faster/cheaper model).
*   CLI fallbacks (`whisper-cli`, `whisper`, `gemini`) are useful when provider APIs are unavailable.
*   `parakeet-mlx` note: with `--output-dir`, OpenClaw reads `<output-dir>/<media-basename>.txt` when output format is `txt` (or unspecified); non-`txt` formats fall back to stdout.

## Attachment policy

Per‑capability `attachments` controls which attachments are processed:

*   `mode`: `first` (default) or `all`
*   `maxAttachments`: cap the number processed (default **1**)
*   `prefer`: `first`, `last`, `path`, `url`

When `mode: "all"`, outputs are labeled `[Image 1/2]`, `[Audio 2/2]`, etc.

## Config examples

### 1) Shared models list + overrides

```
{
  tools: {
    media: {
      models: [
        { provider: "openai", model: "gpt-5.2", capabilities: ["image"] },
        {
          provider: "google",
          model: "gemini-3-flash-preview",
          capabilities: ["image", "audio", "video"],
        },
        {
          type: "cli",
          command: "gemini",
          args: [
            "-m",
            "gemini-3-flash",
            "--allowed-tools",
            "read_file",
            "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
          ],
          capabilities: ["image", "video"],
        },
      ],
      audio: {
        attachments: { mode: "all", maxAttachments: 2 },
      },
      video: {
        maxChars: 500,
      },
    },
  },
}
```

### 2) Audio + Video only (image off)

```
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [
          { provider: "openai", model: "gpt-4o-mini-transcribe" },
          {
            type: "cli",
            command: "whisper",
            args: ["--model", "base", "{{MediaPath}}"],
          },
        ],
      },
      video: {
        enabled: true,
        maxChars: 500,
        models: [
          { provider: "google", model: "gemini-3-flash-preview" },
          {
            type: "cli",
            command: "gemini",
            args: [
              "-m",
              "gemini-3-flash",
              "--allowed-tools",
              "read_file",
              "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
            ],
          },
        ],
      },
    },
  },
}
```

### 3) Optional image understanding

```
{
  tools: {
    media: {
      image: {
        enabled: true,
        maxBytes: 10485760,
        maxChars: 500,
        models: [
          { provider: "openai", model: "gpt-5.2" },
          { provider: "anthropic", model: "claude-opus-4-6" },
          {
            type: "cli",
            command: "gemini",
            args: [
              "-m",
              "gemini-3-flash",
              "--allowed-tools",
              "read_file",
              "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
            ],
          },
        ],
      },
    },
  },
}
```

### 4) Multi‑modal single entry (explicit capabilities)

```
{
  tools: {
    media: {
      image: {
        models: [
          {
            provider: "google",
            model: "gemini-3.1-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
      audio: {
        models: [
          {
            provider: "google",
            model: "gemini-3.1-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
      video: {
        models: [
          {
            provider: "google",
            model: "gemini-3.1-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
    },
  },
}
```

## Status output

When media understanding runs, `/status` includes a short summary line:

```
📎 Media: image ok (openai/gpt-5.2) · audio skipped (maxBytes)
```

This shows per‑capability outcomes and the chosen provider/model when applicable.

## Notes

*   Understanding is **best‑effort**. Errors do not block replies.
*   Attachments are still passed to models even when understanding is disabled.
*   Use `scope` to limit where understanding runs (e.g. only DMs).

*   [Configuration](https://docs.openclaw.ai/gateway/configuration)
*   [Image & Media Support](https://docs.openclaw.ai/nodes/images)

---

<!-- SOURCE: https://docs.openclaw.ai/nodes/images -->

# Image and Media Support - OpenClaw

## Image & Media Support — 2025-12-05

The WhatsApp channel runs via **Baileys Web**. This document captures the current media handling rules for send, gateway, and agent replies.

## Goals

*   Send media with optional captions via `openclaw message send --media`.
*   Allow auto-replies from the web inbox to include media alongside text.
*   Keep per-type limits sane and predictable.

## CLI Surface

*   `openclaw message send --media <path-or-url> [--message <caption>]`
    *   `--media` optional; caption can be empty for media-only sends.
    *   `--dry-run` prints the resolved payload; `--json` emits `{ channel, to, messageId, mediaUrl, caption }`.

## WhatsApp Web channel behavior

*   Input: local file path **or** HTTP(S) URL.
*   Flow: load into a Buffer, detect media kind, and build the correct payload:
    *   **Images:** resize & recompress to JPEG (max side 2048px) targeting `agents.defaults.mediaMaxMb` (default 5 MB), capped at 6 MB.
    *   **Audio/Voice/Video:** pass-through up to 16 MB; audio is sent as a voice note (`ptt: true`).
    *   **Documents:** anything else, up to 100 MB, with filename preserved when available.
*   WhatsApp GIF-style playback: send an MP4 with `gifPlayback: true` (CLI: `--gif-playback`) so mobile clients loop inline.
*   MIME detection prefers magic bytes, then headers, then file extension.
*   Caption comes from `--message` or `reply.text`; empty caption is allowed.
*   Logging: non-verbose shows `↩️`/`✅`; verbose includes size and source path/URL.

## Auto-Reply Pipeline

*   `getReplyFromConfig` returns `{ text?, mediaUrl?, mediaUrls? }`.
*   When media is present, the web sender resolves local paths or URLs using the same pipeline as `openclaw message send`.
*   Multiple media entries are sent sequentially if provided.

*   When inbound web messages include media, OpenClaw downloads to a temp file and exposes templating variables:
    *   `{{MediaUrl}}` pseudo-URL for the inbound media.
    *   `{{MediaPath}}` local temp path written before running the command.
*   When a per-session Docker sandbox is enabled, inbound media is copied into the sandbox workspace and `MediaPath`/`MediaUrl` are rewritten to a relative path like `media/inbound/<filename>`.
*   Media understanding (if configured via `tools.media.*` or shared `tools.media.models`) runs before templating and can insert `[Image]`, `[Audio]`, and `[Video]` blocks into `Body`.
    *   Audio sets `{{Transcript}}` and uses the transcript for command parsing so slash commands still work.
    *   Video and image descriptions preserve any caption text for command parsing.
*   By default only the first matching image/audio/video attachment is processed; set `tools.media.<cap>.attachments` to process multiple attachments.

## Limits & Errors

**Outbound send caps (WhatsApp web send)**

*   Images: ~6 MB cap after recompression.
*   Audio/voice/video: 16 MB cap; documents: 100 MB cap.
*   Oversize or unreadable media → clear error in logs and the reply is skipped.

**Media understanding caps (transcription/description)**

*   Image default: 10 MB (`tools.media.image.maxBytes`).
*   Audio default: 20 MB (`tools.media.audio.maxBytes`).
*   Video default: 50 MB (`tools.media.video.maxBytes`).
*   Oversize media skips understanding, but replies still go through with the original body.

## Notes for Tests

*   Cover send + reply flows for image/audio/document cases.
*   Validate recompression for images (size bound) and voice-note flag for audio.
*   Ensure multi-media replies fan out as sequential sends.

---

<!-- SOURCE: https://docs.openclaw.ai/nodes/camera -->

# Camera Capture - OpenClaw

## Camera capture (agent)

OpenClaw supports **camera capture** for agent workflows:

*   **iOS node** (paired via Gateway): capture a **photo** (`jpg`) or **short video clip** (`mp4`, with optional audio) via `node.invoke`.
*   **Android node** (paired via Gateway): capture a **photo** (`jpg`) or **short video clip** (`mp4`, with optional audio) via `node.invoke`.
*   **macOS app** (node via Gateway): capture a **photo** (`jpg`) or **short video clip** (`mp4`, with optional audio) via `node.invoke`.

All camera access is gated behind **user-controlled settings**.

## iOS node

### User setting (default on)

*   iOS Settings tab → **Camera** → **Allow Camera** (`camera.enabled`)
    *   Default: **on** (missing key is treated as enabled).
    *   When off: `camera.*` commands return `CAMERA_DISABLED`.

### Commands (via Gateway `node.invoke`)

*   `camera.list`
    *   Response payload:
        *   `devices`: array of `{ id, name, position, deviceType }`
*   `camera.snap`
    *   Params:
        *   `facing`: `front|back` (default: `front`)
        *   `maxWidth`: number (optional; default `1600` on the iOS node)
        *   `quality`: `0..1` (optional; default `0.9`)
        *   `format`: currently `jpg`
        *   `delayMs`: number (optional; default `0`)
        *   `deviceId`: string (optional; from `camera.list`)
    *   Response payload:
        *   `format: "jpg"`
        *   `base64: "<...>"`
        *   `width`, `height`
    *   Payload guard: photos are recompressed to keep the base64 payload under 5 MB.
*   `camera.clip`
    *   Params:
        *   `facing`: `front|back` (default: `front`)
        *   `durationMs`: number (default `3000`, clamped to a max of `60000`)
        *   `includeAudio`: boolean (default `true`)
        *   `format`: currently `mp4`
        *   `deviceId`: string (optional; from `camera.list`)
    *   Response payload:
        *   `format: "mp4"`
        *   `base64: "<...>"`
        *   `durationMs`
        *   `hasAudio`

### Foreground requirement

Like `canvas.*`, the iOS node only allows `camera.*` commands in the **foreground**. Background invocations return `NODE_BACKGROUND_UNAVAILABLE`.

### CLI helper (temp files + MEDIA)

The easiest way to get attachments is via the CLI helper, which writes decoded media to a temp file and prints `MEDIA:<path>`. Examples:

```
openclaw nodes camera snap --node <id>               # default: both front + back (2 MEDIA lines)
openclaw nodes camera snap --node <id> --facing front
openclaw nodes camera clip --node <id> --duration 3000
openclaw nodes camera clip --node <id> --no-audio
```

Notes:

*   `nodes camera snap` defaults to **both** facings to give the agent both views.
*   Output files are temporary (in the OS temp directory) unless you build your own wrapper.

## Android node

### Android user setting (default on)

*   Android Settings sheet → **Camera** → **Allow Camera** (`camera.enabled`)
    *   Default: **on** (missing key is treated as enabled).
    *   When off: `camera.*` commands return `CAMERA_DISABLED`.

### Permissions

*   Android requires runtime permissions:
    *   `CAMERA` for both `camera.snap` and `camera.clip`.
    *   `RECORD_AUDIO` for `camera.clip` when `includeAudio=true`.

If permissions are missing, the app will prompt when possible; if denied, `camera.*` requests fail with a `*_PERMISSION_REQUIRED` error.

### Android foreground requirement

Like `canvas.*`, the Android node only allows `camera.*` commands in the **foreground**. Background invocations return `NODE_BACKGROUND_UNAVAILABLE`.

### Android commands (via Gateway `node.invoke`)

*   `camera.list`
    *   Response payload:
        *   `devices`: array of `{ id, name, position, deviceType }`

### Payload guard

Photos are recompressed to keep the base64 payload under 5 MB.

## macOS app

### User setting (default off)

The macOS companion app exposes a checkbox:

*   **Settings → General → Allow Camera** (`openclaw.cameraEnabled`)
    *   Default: **off**
    *   When off: camera requests return “Camera disabled by user”.

### CLI helper (node invoke)

Use the main `openclaw` CLI to invoke camera commands on the macOS node. Examples:

```
openclaw nodes camera list --node <id>            # list camera ids
openclaw nodes camera snap --node <id>            # prints MEDIA:<path>
openclaw nodes camera snap --node <id> --max-width 1280
openclaw nodes camera snap --node <id> --delay-ms 2000
openclaw nodes camera snap --node <id> --device-id <id>
openclaw nodes camera clip --node <id> --duration 10s          # prints MEDIA:<path>
openclaw nodes camera clip --node <id> --duration-ms 3000      # prints MEDIA:<path> (legacy flag)
openclaw nodes camera clip --node <id> --device-id <id>
openclaw nodes camera clip --node <id> --no-audio
```

Notes:

*   `openclaw nodes camera snap` defaults to `maxWidth=1600` unless overridden.
*   On macOS, `camera.snap` waits `delayMs` (default 2000ms) after warm-up/exposure settle before capturing.
*   Photo payloads are recompressed to keep base64 under 5 MB.

## Safety + practical limits

*   Camera and microphone access trigger the usual OS permission prompts (and require usage strings in Info.plist).
*   Video clips are capped (currently `<= 60s`) to avoid oversized node payloads (base64 overhead + message limits).

## macOS screen video (OS-level)

For _screen_ video (not camera), use the macOS companion:

```
openclaw nodes screen record --node <id> --duration 10s --fps 15   # prints MEDIA:<path>
```

Notes:

*   Requires macOS **Screen Recording** permission (TCC).

---

<!-- SOURCE: https://docs.openclaw.ai/nodes/talk -->

# Talk Mode - OpenClaw

Talk mode is a continuous voice conversation loop:

1.  Listen for speech
2.  Send transcript to the model (main session, chat.send)
3.  Wait for the response
4.  Speak it via ElevenLabs (streaming playback)

## Behavior (macOS)

*   **Always-on overlay** while Talk mode is enabled.
*   **Listening → Thinking → Speaking** phase transitions.
*   On a **short pause** (silence window), the current transcript is sent.
*   Replies are **written to WebChat** (same as typing).
*   **Interrupt on speech** (default on): if the user starts talking while the assistant is speaking, we stop playback and note the interruption timestamp for the next prompt.

The assistant may prefix its reply with a **single JSON line** to control voice:

```
{ "voice": "<voice-id>", "once": true }
```

Rules:

*   First non-empty line only.
*   Unknown keys are ignored.
*   `once: true` applies to the current reply only.
*   Without `once`, the voice becomes the new default for Talk mode.
*   The JSON line is stripped before TTS playback.

Supported keys:

*   `voice` / `voice_id` / `voiceId`
*   `model` / `model_id` / `modelId`
*   `speed`, `rate` (WPM), `stability`, `similarity`, `style`, `speakerBoost`
*   `seed`, `normalize`, `lang`, `output_format`, `latency_tier`
*   `once`

## Config (`~/.openclaw/openclaw.json`)

```
{
  talk: {
    voiceId: "elevenlabs_voice_id",
    modelId: "eleven_v3",
    outputFormat: "mp3_44100_128",
    apiKey: "elevenlabs_api_key",
    silenceTimeoutMs: 1500,
    interruptOnSpeech: true,
  },
}
```

Defaults:

*   `interruptOnSpeech`: true
*   `silenceTimeoutMs`: when unset, Talk keeps the platform default pause window before sending the transcript (`700 ms on macOS and Android, 900 ms on iOS`)
*   `voiceId`: falls back to `ELEVENLABS_VOICE_ID` / `SAG_VOICE_ID` (or first ElevenLabs voice when API key is available)
*   `modelId`: defaults to `eleven_v3` when unset
*   `apiKey`: falls back to `ELEVENLABS_API_KEY` (or gateway shell profile if available)
*   `outputFormat`: defaults to `pcm_44100` on macOS/iOS and `pcm_24000` on Android (set `mp3_*` to force MP3 streaming)

## macOS UI

*   Menu bar toggle: **Talk**
*   Config tab: **Talk Mode** group (voice id + interrupt toggle)
*   Overlay:
    *   **Listening**: cloud pulses with mic level
    *   **Thinking**: sinking animation
    *   **Speaking**: radiating rings
    *   Click cloud: stop speaking
    *   Click X: exit Talk mode

## Notes

*   Requires Speech + Microphone permissions.
*   Uses `chat.send` against session key `main`.
*   TTS uses ElevenLabs streaming API with `ELEVENLABS_API_KEY` and incremental playback on macOS/iOS/Android for lower latency.
*   `stability` for `eleven_v3` is validated to `0.0`, `0.5`, or `1.0`; other models accept `0..1`.
*   `latency_tier` is validated to `0..4` when set.
*   Android supports `pcm_16000`, `pcm_22050`, `pcm_24000`, and `pcm_44100` output formats for low-latency AudioTrack streaming.

---

<!-- SOURCE: https://docs.openclaw.ai/nodes/voicewake -->

# Voice Wake - OpenClaw

## Voice Wake (Global Wake Words)

OpenClaw treats **wake words as a single global list** owned by the **Gateway**.

*   There are **no per-node custom wake words**.
*   **Any node/app UI may edit** the list; changes are persisted by the Gateway and broadcast to everyone.
*   macOS and iOS keep local **Voice Wake enabled/disabled** toggles (local UX + permissions differ).
*   Android currently keeps Voice Wake off and uses a manual mic flow in the Voice tab.

## Storage (Gateway host)

Wake words are stored on the gateway machine at:

*   `~/.openclaw/settings/voicewake.json`

Shape:

```
{ "triggers": ["openclaw", "claude", "computer"], "updatedAtMs": 1730000000000 }
```

## Protocol

### Methods

*   `voicewake.get` → `{ triggers: string[] }`
*   `voicewake.set` with params `{ triggers: string[] }` → `{ triggers: string[] }`

Notes:

*   Triggers are normalized (trimmed, empties dropped). Empty lists fall back to defaults.
*   Limits are enforced for safety (count/length caps).

### Events

*   `voicewake.changed` payload `{ triggers: string[] }`

Who receives it:

*   All WebSocket clients (macOS app, WebChat, etc.)
*   All connected nodes (iOS/Android), and also on node connect as an initial “current state” push.

## Client behavior

### macOS app

*   Uses the global list to gate `VoiceWakeRuntime` triggers.
*   Editing “Trigger words” in Voice Wake settings calls `voicewake.set` and then relies on the broadcast to keep other clients in sync.

### iOS node

*   Uses the global list for `VoiceWakeManager` trigger detection.
*   Editing Wake Words in Settings calls `voicewake.set` (over the Gateway WS) and also keeps local wake-word detection responsive.

### Android node

*   Voice Wake is currently disabled in Android runtime/Settings.
*   Android voice uses manual mic capture in the Voice tab instead of wake-word triggers.

---

<!-- SOURCE: https://docs.openclaw.ai/nodes/location-command -->

# Location Command - OpenClaw

## TL;DR

*   `location.get` is a node command (via `node.invoke`).
*   Off by default.
*   Android app settings use a selector: Off / While Using.
*   Separate toggle: Precise Location.

## Why a selector (not just a switch)

OS permissions are multi-level. We can expose a selector in-app, but the OS still decides the actual grant.

*   iOS/macOS may expose **While Using** or **Always** in system prompts/Settings.
*   Android app currently supports foreground location only.
*   Precise location is a separate grant (iOS 14+ “Precise”, Android “fine” vs “coarse”).

Selector in UI drives our requested mode; actual grant lives in OS settings.

## Settings model

Per node device:

*   `location.enabledMode`: `off | whileUsing`
*   `location.preciseEnabled`: bool

UI behavior:

*   Selecting `whileUsing` requests foreground permission.
*   If OS denies requested level, revert to the highest granted level and show status.

## Permissions mapping (node.permissions)

Optional. macOS node reports `location` via the permissions map; iOS/Android may omit it.

## Command: `location.get`

Called via `node.invoke`. Params (suggested):

```
{
  "timeoutMs": 10000,
  "maxAgeMs": 15000,
  "desiredAccuracy": "coarse|balanced|precise"
}
```

Response payload:

```
{
  "lat": 48.20849,
  "lon": 16.37208,
  "accuracyMeters": 12.5,
  "altitudeMeters": 182.0,
  "speedMps": 0.0,
  "headingDeg": 270.0,
  "timestamp": "2026-01-03T12:34:56.000Z",
  "isPrecise": true,
  "source": "gps|wifi|cell|unknown"
}
```

Errors (stable codes):

*   `LOCATION_DISABLED`: selector is off.
*   `LOCATION_PERMISSION_REQUIRED`: permission missing for requested mode.
*   `LOCATION_BACKGROUND_UNAVAILABLE`: app is backgrounded but only While Using allowed.
*   `LOCATION_TIMEOUT`: no fix in time.
*   `LOCATION_UNAVAILABLE`: system failure / no providers.

## Background behavior

*   Android app denies `location.get` while backgrounded.
*   Keep OpenClaw open when requesting location on Android.
*   Other node platforms may differ.

*   Tool surface: `nodes` tool adds `location_get` action (node required).
*   CLI: `openclaw nodes location get --node <id>`.
*   Agent guidelines: only call when user enabled location and understands the scope.

## UX copy (suggested)

*   Off: “Location sharing is disabled.”
*   While Using: “Only when OpenClaw is open.”
*   Precise: “Use precise GPS location. Toggle off to share approximate location.”

---

<!-- SOURCE: https://docs.openclaw.ai/nodes/audio -->

# Audio and Voice Notes - OpenClaw

## Audio / Voice Notes — 2026-01-17

## What works

*   **Media understanding (audio)**: If audio understanding is enabled (or auto‑detected), OpenClaw:
    1.  Locates the first audio attachment (local path or URL) and downloads it if needed.
    2.  Enforces `maxBytes` before sending to each model entry.
    3.  Runs the first eligible model entry in order (provider or CLI).
    4.  If it fails or skips (size/timeout), it tries the next entry.
    5.  On success, it replaces `Body` with an `[Audio]` block and sets `{{Transcript}}`.
*   **Command parsing**: When transcription succeeds, `CommandBody`/`RawBody` are set to the transcript so slash commands still work.
*   **Verbose logging**: In `--verbose`, we log when transcription runs and when it replaces the body.

## Auto-detection (default)

If you **don’t configure models** and `tools.media.audio.enabled` is **not** set to `false`, OpenClaw auto-detects in this order and stops at the first working option:

1.  **Local CLIs** (if installed)
    *   `sherpa-onnx-offline` (requires `SHERPA_ONNX_MODEL_DIR` with encoder/decoder/joiner/tokens)
    *   `whisper-cli` (from `whisper-cpp`; uses `WHISPER_CPP_MODEL` or the bundled tiny model)
    *   `whisper` (Python CLI; downloads models automatically)
2.  **Gemini CLI** (`gemini`) using `read_many_files`
3.  **Provider keys** (OpenAI → Groq → Deepgram → Google)

To disable auto-detection, set `tools.media.audio.enabled: false`. To customize, set `tools.media.audio.models`. Note: Binary detection is best-effort across macOS/Linux/Windows; ensure the CLI is on `PATH` (we expand `~`), or set an explicit CLI model with a full command path.

## Config examples

### Provider + CLI fallback (OpenAI + Whisper CLI)

```
{
  tools: {
    media: {
      audio: {
        enabled: true,
        maxBytes: 20971520,
        models: [
          { provider: "openai", model: "gpt-4o-mini-transcribe" },
          {
            type: "cli",
            command: "whisper",
            args: ["--model", "base", "{{MediaPath}}"],
            timeoutSeconds: 45,
          },
        ],
      },
    },
  },
}
```

### Provider-only with scope gating

```
{
  tools: {
    media: {
      audio: {
        enabled: true,
        scope: {
          default: "allow",
          rules: [{ action: "deny", match: { chatType: "group" } }],
        },
        models: [{ provider: "openai", model: "gpt-4o-mini-transcribe" }],
      },
    },
  },
}
```

### Provider-only (Deepgram)

```
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "deepgram", model: "nova-3" }],
      },
    },
  },
}
```

### Provider-only (Mistral Voxtral)

```
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "mistral", model: "voxtral-mini-latest" }],
      },
    },
  },
}
```

### Echo transcript to chat (opt-in)

```
{
  tools: {
    media: {
      audio: {
        enabled: true,
        echoTranscript: true, // default is false
        echoFormat: '📝 "{transcript}"', // optional, supports {transcript}
        models: [{ provider: "openai", model: "gpt-4o-mini-transcribe" }],
      },
    },
  },
}
```

## Notes & limits

*   Provider auth follows the standard model auth order (auth profiles, env vars, `models.providers.*.apiKey`).
*   Deepgram picks up `DEEPGRAM_API_KEY` when `provider: "deepgram"` is used.
*   Deepgram setup details: [Deepgram (audio transcription)](https://docs.openclaw.ai/providers/deepgram).
*   Mistral setup details: [Mistral](https://docs.openclaw.ai/providers/mistral).
*   Audio providers can override `baseUrl`, `headers`, and `providerOptions` via `tools.media.audio`.
*   Default size cap is 20MB (`tools.media.audio.maxBytes`). Oversize audio is skipped for that model and the next entry is tried.
*   Tiny/empty audio files below 1024 bytes are skipped before provider/CLI transcription.
*   Default `maxChars` for audio is **unset** (full transcript). Set `tools.media.audio.maxChars` or per-entry `maxChars` to trim output.
*   OpenAI auto default is `gpt-4o-mini-transcribe`; set `model: "gpt-4o-transcribe"` for higher accuracy.
*   Use `tools.media.audio.attachments` to process multiple voice notes (`mode: "all"` + `maxAttachments`).
*   Transcript is available to templates as `{{Transcript}}`.
*   `tools.media.audio.echoTranscript` is off by default; enable it to send transcript confirmation back to the originating chat before agent processing.
*   `tools.media.audio.echoFormat` customizes the echo text (placeholder: `{transcript}`).
*   CLI stdout is capped (5MB); keep CLI output concise.

### Proxy environment support

Provider-based audio transcription honors standard outbound proxy env vars:

*   `HTTPS_PROXY`
*   `HTTP_PROXY`
*   `https_proxy`
*   `http_proxy`

If no proxy env vars are set, direct egress is used. If proxy config is malformed, OpenClaw logs a warning and falls back to direct fetch.

## Mention Detection in Groups

When `requireMention: true` is set for a group chat, OpenClaw now transcribes audio **before** checking for mentions. This allows voice notes to be processed even when they contain mentions. **How it works:**

1.  If a voice message has no text body and the group requires mentions, OpenClaw performs a “preflight” transcription.
2.  The transcript is checked for mention patterns (e.g., `@BotName`, emoji triggers).
3.  If a mention is found, the message proceeds through the full reply pipeline.
4.  The transcript is used for mention detection so voice notes can pass the mention gate.

**Fallback behavior:**

*   If transcription fails during preflight (timeout, API error, etc.), the message is processed based on text-only mention detection.
*   This ensures that mixed messages (text + audio) are never incorrectly dropped.

**Opt-out per Telegram group/topic:**

*   Set `channels.telegram.groups.<chatId>.disableAudioPreflight: true` to skip preflight transcript mention checks for that group.
*   Set `channels.telegram.groups.<chatId>.topics.<threadId>.disableAudioPreflight` to override per-topic (`true` to skip, `false` to force-enable).
*   Default is `false` (preflight enabled when mention-gated conditions match).

**Example:** A user sends a voice note saying “Hey @Claude, what’s the weather?” in a Telegram group with `requireMention: true`. The voice note is transcribed, the mention is detected, and the agent replies.

## Gotchas

*   Scope rules use first-match wins. `chatType` is normalized to `direct`, `group`, or `room`.
*   Ensure your CLI exits 0 and prints plain text; JSON needs to be massaged via `jq -r .text`.
*   For `parakeet-mlx`, if you pass `--output-dir`, OpenClaw reads `<output-dir>/<media-basename>.txt` when `--output-format` is `txt` (or omitted); non-`txt` output formats fall back to stdout parsing.
*   Keep timeouts reasonable (`timeoutSeconds`, default 60s) to avoid blocking the reply queue.
*   Preflight transcription only processes the **first** audio attachment for mention detection. Additional audio is processed during the main media understanding phase.



---

<!-- SOURCE: https://docs.openclaw.ai/nodes -->

# Nodes - OpenClaw

A **node** is a companion device (macOS/iOS/Android/headless) that connects to the Gateway **WebSocket** (same port as operators) with `role: "node"` and exposes a command surface (e.g. `canvas.*`, `camera.*`, `device.*`, `notifications.*`, `system.*`) via `node.invoke`. Protocol details: [Gateway protocol](https://docs.openclaw.ai/gateway/protocol). Legacy transport: [Bridge protocol](https://docs.openclaw.ai/gateway/bridge-protocol) (TCP JSONL; deprecated/removed for current nodes). macOS can also run in **node mode**: the menubar app connects to the Gateway’s WS server and exposes its local canvas/camera commands as a node (so `openclaw nodes …` works against this Mac). Notes:

*   Nodes are **peripherals**, not gateways. They don’t run the gateway service.
*   Telegram/WhatsApp/etc. messages land on the **gateway**, not on nodes.
*   Troubleshooting runbook: [/nodes/troubleshooting](https://docs.openclaw.ai/nodes/troubleshooting)

## Pairing + status

**WS nodes use device pairing.** Nodes present a device identity during `connect`; the Gateway creates a device pairing request for `role: node`. Approve via the devices CLI (or UI). Quick CLI:

```
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
```

Notes:

*   `nodes status` marks a node as **paired** when its device pairing role includes `node`.
*   `node.pair.*` (CLI: `openclaw nodes pending/approve/reject`) is a separate gateway-owned node pairing store; it does **not** gate the WS `connect` handshake.

## Remote node host (system.run)

Use a **node host** when your Gateway runs on one machine and you want commands to execute on another. The model still talks to the **gateway**; the gateway forwards `exec` calls to the **node host** when `host=node` is selected.

### What runs where

*   **Gateway host**: receives messages, runs the model, routes tool calls.
*   **Node host**: executes `system.run`/`system.which` on the node machine.
*   **Approvals**: enforced on the node host via `~/.openclaw/exec-approvals.json`.

### Start a node host (foreground)

On the node machine:

```
openclaw node run --host <gateway-host> --port 18789 --display-name "Build Node"
```

### Remote gateway via SSH tunnel (loopback bind)

If the Gateway binds to loopback (`gateway.bind=loopback`, default in local mode), remote node hosts cannot connect directly. Create an SSH tunnel and point the node host at the local end of the tunnel. Example (node host -> gateway host):

```
# Terminal A (keep running): forward local 18790 -> gateway 127.0.0.1:18789
ssh -N -L 18790:127.0.0.1:18789 user@gateway-host

# Terminal B: export the gateway token and connect through the tunnel
export OPENCLAW_GATEWAY_TOKEN="<gateway-token>"
openclaw node run --host 127.0.0.1 --port 18790 --display-name "Build Node"
```

Notes:

*   `openclaw node run` supports token or password auth.
*   Env vars are preferred: `OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD`.
*   Config fallback is `gateway.auth.token` / `gateway.auth.password`; in remote mode, `gateway.remote.token` / `gateway.remote.password` are also eligible.
*   Legacy `CLAWDBOT_GATEWAY_*` env vars are intentionally ignored by node-host auth resolution.

### Start a node host (service)

```
openclaw node install --host <gateway-host> --port 18789 --display-name "Build Node"
openclaw node restart
```

### Pair + name

On the gateway host:

```
openclaw devices list
openclaw devices approve <requestId>
openclaw nodes status
```

Naming options:

*   `--display-name` on `openclaw node run` / `openclaw node install` (persists in `~/.openclaw/node.json` on the node).
*   `openclaw nodes rename --node <id|name|ip> --name "Build Node"` (gateway override).

### Allowlist the commands

Exec approvals are **per node host**. Add allowlist entries from the gateway:

```
openclaw approvals allowlist add --node <id|name|ip> "/usr/bin/uname"
openclaw approvals allowlist add --node <id|name|ip> "/usr/bin/sw_vers"
```

Approvals live on the node host at `~/.openclaw/exec-approvals.json`.

### Point exec at the node

Configure defaults (gateway config):

```
openclaw config set tools.exec.host node
openclaw config set tools.exec.security allowlist
openclaw config set tools.exec.node "<id-or-name>"
```

Or per session:

```
/exec host=node security=allowlist node=<id-or-name>
```

Once set, any `exec` call with `host=node` runs on the node host (subject to the node allowlist/approvals). Related:

*   [Node host CLI](https://docs.openclaw.ai/cli/node)
*   [Exec tool](https://docs.openclaw.ai/tools/exec)
*   [Exec approvals](https://docs.openclaw.ai/tools/exec-approvals)

## Invoking commands

Low-level (raw RPC):

```
openclaw nodes invoke --node <idOrNameOrIp> --command canvas.eval --params '{"javaScript":"location.href"}'
```

Higher-level helpers exist for the common “give the agent a MEDIA attachment” workflows.

## Screenshots (canvas snapshots)

If the node is showing the Canvas (WebView), `canvas.snapshot` returns `{ format, base64 }`. CLI helper (writes to a temp file and prints `MEDIA:<path>`):

```
openclaw nodes canvas snapshot --node <idOrNameOrIp> --format png
openclaw nodes canvas snapshot --node <idOrNameOrIp> --format jpg --max-width 1200 --quality 0.9
```

### Canvas controls

```
openclaw nodes canvas present --node <idOrNameOrIp> --target https://example.com
openclaw nodes canvas hide --node <idOrNameOrIp>
openclaw nodes canvas navigate https://example.com --node <idOrNameOrIp>
openclaw nodes canvas eval --node <idOrNameOrIp> --js "document.title"
```

Notes:

*   `canvas present` accepts URLs or local file paths (`--target`), plus optional `--x/--y/--width/--height` for positioning.
*   `canvas eval` accepts inline JS (`--js`) or a positional arg.

### A2UI (Canvas)

```
openclaw nodes canvas a2ui push --node <idOrNameOrIp> --text "Hello"
openclaw nodes canvas a2ui push --node <idOrNameOrIp> --jsonl ./payload.jsonl
openclaw nodes canvas a2ui reset --node <idOrNameOrIp>
```

Notes:

*   Only A2UI v0.8 JSONL is supported (v0.9/createSurface is rejected).

## Photos + videos (node camera)

Photos (`jpg`):

```
openclaw nodes camera list --node <idOrNameOrIp>
openclaw nodes camera snap --node <idOrNameOrIp>            # default: both facings (2 MEDIA lines)
openclaw nodes camera snap --node <idOrNameOrIp> --facing front
```

Video clips (`mp4`):

```
openclaw nodes camera clip --node <idOrNameOrIp> --duration 10s
openclaw nodes camera clip --node <idOrNameOrIp> --duration 3000 --no-audio
```

Notes:

*   The node must be **foregrounded** for `canvas.*` and `camera.*` (background calls return `NODE_BACKGROUND_UNAVAILABLE`).
*   Clip duration is clamped (currently `<= 60s`) to avoid oversized base64 payloads.
*   Android will prompt for `CAMERA`/`RECORD_AUDIO` permissions when possible; denied permissions fail with `*_PERMISSION_REQUIRED`.

## Screen recordings (nodes)

Supported nodes expose `screen.record` (mp4). Example:

```
openclaw nodes screen record --node <idOrNameOrIp> --duration 10s --fps 10
openclaw nodes screen record --node <idOrNameOrIp> --duration 10s --fps 10 --no-audio
```

Notes:

*   `screen.record` availability depends on node platform.
*   Screen recordings are clamped to `<= 60s`.
*   `--no-audio` disables microphone capture on supported platforms.
*   Use `--screen <index>` to select a display when multiple screens are available.

## Location (nodes)

Nodes expose `location.get` when Location is enabled in settings. CLI helper:

```
openclaw nodes location get --node <idOrNameOrIp>
openclaw nodes location get --node <idOrNameOrIp> --accuracy precise --max-age 15000 --location-timeout 10000
```

Notes:

*   Location is **off by default**.
*   “Always” requires system permission; background fetch is best-effort.
*   The response includes lat/lon, accuracy (meters), and timestamp.

## SMS (Android nodes)

Android nodes can expose `sms.send` when the user grants **SMS** permission and the device supports telephony. Low-level invoke:

```
openclaw nodes invoke --node <idOrNameOrIp> --command sms.send --params '{"to":"+15555550123","message":"Hello from OpenClaw"}'
```

Notes:

*   The permission prompt must be accepted on the Android device before the capability is advertised.
*   Wi-Fi-only devices without telephony will not advertise `sms.send`.

## Android device + personal data commands

Android nodes can advertise additional command families when the corresponding capabilities are enabled. Available families:

*   `device.status`, `device.info`, `device.permissions`, `device.health`
*   `notifications.list`, `notifications.actions`
*   `photos.latest`
*   `contacts.search`, `contacts.add`
*   `calendar.events`, `calendar.add`
*   `motion.activity`, `motion.pedometer`

Example invokes:

```
openclaw nodes invoke --node <idOrNameOrIp> --command device.status --params '{}'
openclaw nodes invoke --node <idOrNameOrIp> --command notifications.list --params '{}'
openclaw nodes invoke --node <idOrNameOrIp> --command photos.latest --params '{"limit":1}'
```

Notes:

*   Motion commands are capability-gated by available sensors.

## System commands (node host / mac node)

The macOS node exposes `system.run`, `system.notify`, and `system.execApprovals.get/set`. The headless node host exposes `system.run`, `system.which`, and `system.execApprovals.get/set`. Examples:

```
openclaw nodes run --node <idOrNameOrIp> -- echo "Hello from mac node"
openclaw nodes notify --node <idOrNameOrIp> --title "Ping" --body "Gateway ready"
```

Notes:

*   `system.run` returns stdout/stderr/exit code in the payload.
*   `system.notify` respects notification permission state on the macOS app.
*   Unrecognized node `platform` / `deviceFamily` metadata uses a conservative default allowlist that excludes `system.run` and `system.which`. If you intentionally need those commands for an unknown platform, add them explicitly via `gateway.nodes.allowCommands`.
*   `system.run` supports `--cwd`, `--env KEY=VAL`, `--command-timeout`, and `--needs-screen-recording`.
*   For shell wrappers (`bash|sh|zsh ... -c/-lc`), request-scoped `--env` values are reduced to an explicit allowlist (`TERM`, `LANG`, `LC_*`, `COLORTERM`, `NO_COLOR`, `FORCE_COLOR`).
*   For allow-always decisions in allowlist mode, known dispatch wrappers (`env`, `nice`, `nohup`, `stdbuf`, `timeout`) persist inner executable paths instead of wrapper paths. If unwrapping is not safe, no allowlist entry is persisted automatically.
*   On Windows node hosts in allowlist mode, shell-wrapper runs via `cmd.exe /c` require approval (allowlist entry alone does not auto-allow the wrapper form).
*   `system.notify` supports `--priority <passive|active|timeSensitive>` and `--delivery <system|overlay|auto>`.
*   Node hosts ignore `PATH` overrides and strip dangerous startup/shell keys (`DYLD_*`, `LD_*`, `NODE_OPTIONS`, `PYTHON*`, `PERL*`, `RUBYOPT`, `SHELLOPTS`, `PS4`). If you need extra PATH entries, configure the node host service environment (or install tools in standard locations) instead of passing `PATH` via `--env`.
*   On macOS node mode, `system.run` is gated by exec approvals in the macOS app (Settings → Exec approvals). Ask/allowlist/full behave the same as the headless node host; denied prompts return `SYSTEM_RUN_DENIED`.
*   On headless node host, `system.run` is gated by exec approvals (`~/.openclaw/exec-approvals.json`).

## Exec node binding

When multiple nodes are available, you can bind exec to a specific node. This sets the default node for `exec host=node` (and can be overridden per agent). Global default:

```
openclaw config set tools.exec.node "node-id-or-name"
```

Per-agent override:

```
openclaw config get agents.list
openclaw config set agents.list[0].tools.exec.node "node-id-or-name"
```

Unset to allow any node:

```
openclaw config unset tools.exec.node
openclaw config unset agents.list[0].tools.exec.node
```

## Permissions map

Nodes may include a `permissions` map in `node.list` / `node.describe`, keyed by permission name (e.g. `screenRecording`, `accessibility`) with boolean values (`true` = granted).

## Headless node host (cross-platform)

OpenClaw can run a **headless node host** (no UI) that connects to the Gateway WebSocket and exposes `system.run` / `system.which`. This is useful on Linux/Windows or for running a minimal node alongside a server. Start it:

```
openclaw node run --host <gateway-host> --port 18789
```

Notes:

*   Pairing is still required (the Gateway will show a device pairing prompt).
*   The node host stores its node id, token, display name, and gateway connection info in `~/.openclaw/node.json`.
*   Exec approvals are enforced locally via `~/.openclaw/exec-approvals.json` (see [Exec approvals](https://docs.openclaw.ai/tools/exec-approvals)).
*   On macOS, the headless node host executes `system.run` locally by default. Set `OPENCLAW_NODE_EXEC_HOST=app` to route `system.run` through the companion app exec host; add `OPENCLAW_NODE_EXEC_FALLBACK=0` to require the app host and fail closed if it is unavailable.
*   Add `--tls` / `--tls-fingerprint` when the Gateway WS uses TLS.

## Mac node mode

*   The macOS menubar app connects to the Gateway WS server as a node (so `openclaw nodes …` works against this Mac).
*   In remote mode, the app opens an SSH tunnel for the Gateway port and connects to `localhost`.

