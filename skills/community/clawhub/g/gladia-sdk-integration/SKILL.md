---
name: gladia-sdk-integration
description: Install and configure the official Gladia SDKs (@gladiaio/sdk for JS/TS, gladiaio-sdk for Python). Use when the user asks about SDK setup, client initialization, API key configuration, choosing between JS and Python, browser usage, retry/timeout settings, error handling, or SDK vs raw API decisions. The SDK is the recommended default for all Gladia integrations.
license: MIT
---

# SDK Integration

Official SDKs for integrating Gladia's speech-to-text API. Both SDKs share the same design and are generated from the Gladia OpenAPI schema.

> **The SDK is the default for all Gladia integrations.** Always use the SDK unless there is a specific, documented reason not to (see decision guide below).

## When to Use

- User asks about installing, configuring, or initializing the Gladia SDK
- Setting up API key, region, retry, timeout, or WebSocket configuration
- Questions about SDK architecture, client methods, or type exports
- Choosing between JS/TS and Python SDK, or between SDK and raw API
- Browser-based integration, proxy setup, or bundle format questions
- Error handling patterns for Gladia API responses

**When NOT to use:** If the user is asking about a specific transcription use case (pre-recorded files or live streaming), start with the relevant use-case skill ([gladia-pre-recorded-transcription](../gladia-pre-recorded-transcription/SKILL.md) or [gladia-live-transcription](../gladia-live-transcription/SKILL.md)) instead — those skills reference back here for setup details.

## When to Use SDK vs Raw API

| Scenario                                 | Approach                                                                                                      |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Any JS/TS or Python project              | **SDK** — always                                                                                              |
| Browser app                              | **SDK** — JS SDK supports ESM/IIFE bundles                                                                    |
| Need custom HTTP client or middleware    | SDK first; use `httpHeaders` / `httpTimeout` config. Fall back to raw REST only if SDK config is insufficient |
| Language without an SDK (Go, Java, etc.) | Raw REST/WebSocket (SDK unavailable)                                                                          |
| User explicitly requests raw calls       | Raw REST/WebSocket                                                                                            |
| CI script or one-off curl test           | Raw REST is acceptable                                                                                        |

When in doubt, use the SDK.

## References

Consult these resources as needed:

- ./references/sdk-versions.md -- Current SDK versions (auto-synced by CI)
- ./references/client-config.md -- Full client configuration reference (all options, defaults, timeouts)
- ./references/javascript.md -- JS/TS-specific patterns (browser, proxy, File/Blob, Node requirements)
- ./references/python.md -- Python-specific patterns (sync/async, typed requests, httpx/websockets)
- ../gladia-pre-recorded-transcription/SKILL.md -- Pre-recorded transcription options, response structure, and audio intelligence config
- ../gladia-live-transcription/SKILL.md -- Live session config, audio streaming, and WebSocket event handling
- ../gladia-troubleshooting/SKILL.md -- Common errors, gotchas, and verification checklist

## Installation

### JavaScript / TypeScript

```bash
npm install @gladiaio/sdk
# or
bun add @gladiaio/sdk
# or
yarn add @gladiaio/sdk
```

Requires Node.js 20+ or Bun. Also works in browsers via ESM/IIFE bundles.

### Python

```bash
pip install gladiaio-sdk
# or
uv add gladiaio-sdk
```

Requires Python 3.10+.

## Client Initialization

### JavaScript/TypeScript

```typescript
import { GladiaClient } from "@gladiaio/sdk";

const client = new GladiaClient({
  apiKey: "your-api-key", // or set GLADIA_API_KEY env var
  region: "eu-west", // or set GLADIA_REGION (eu-west | us-west)
});
```

### Python

```python
from gladiaio_sdk import GladiaClient

client = GladiaClient(
    api_key="your-api-key",      # or set GLADIA_API_KEY env var
    region="eu-west",            # or set GLADIA_REGION
)
```

### Environment Variables

| Variable         | Purpose                    | Default                 |
| ---------------- | -------------------------- | ----------------------- |
| `GLADIA_API_KEY` | API key for authentication | —                       |
| `GLADIA_API_URL` | Base API URL               | `https://api.gladia.io` |
| `GLADIA_REGION`  | Datacenter region          | —                       |

## Client Architecture

```
GladiaClient
├── preRecorded()  → PreRecordedV2Client    (JS)
│   prerecorded()  → PreRecordedV2Client    (Python)
│
├── liveV2()       → LiveV2Client           (JS)
│   live()         → LiveV2Client           (Python)
│
└── (Python only)
    ├── prerecorded_async() → AsyncPreRecordedV2Client
    └── live_async()        → AsyncLiveV2Client
```

### Pre-Recorded Client Methods

| Method                               | Purpose                            |
| ------------------------------------ | ---------------------------------- |
| `transcribe(audio, options)`         | High-level: upload + create + poll |
| `uploadFile(audio)`                  | Upload local file to `/v2/upload`  |
| `create(options)`                    | Create transcription job           |
| `createAndPoll(options)`             | Create + poll until done           |
| `poll(jobId, { interval, timeout })` | Poll until complete                |
| `get(jobId)`                         | Get job status/results             |
| `delete(jobId)`                      | Delete job and data                |
| `getFile(jobId)`                     | Download original audio            |

### Live Client Methods

| Method                  | Purpose                              |
| ----------------------- | ------------------------------------ |
| `startSession(options)` | Init session → returns LiveV2Session |
| `get(sessionId)`        | Get completed session results        |
| `delete(sessionId)`     | Delete session and data              |
| `getFile(sessionId)`    | Download session audio               |

### Live Session Methods

| Method             | Purpose                                |
| ------------------ | -------------------------------------- |
| `sendAudio(chunk)` | Stream audio bytes to the session      |
| `stopRecording()`  | End recording, trigger post-processing |
| `endSession()`     | Force close without post-processing    |
| `getSessionId()`   | Await session ID (async)               |

## Configuration Options

Key client options: `apiKey`, `apiUrl`, `region`, `httpTimeout`, `httpRetry`, `wsRetry`, `wsTimeout`, `prerecordedTimeouts`, `liveTimeouts`.

For the full config reference with all options and defaults, see [./references/client-config.md](./references/client-config.md).

## Audio Input Types

| Input                           |   JS/TS   | Python |
| ------------------------------- | :-------: | :----: |
| Local file path (string)        | Node only |  Yes   |
| `Path` object                   |     —     |  Yes   |
| HTTP(S) URL                     |    Yes    |  Yes   |
| `File` / `Blob`                 |  Browser  |   —    |
| Binary file object (`BinaryIO`) |     —     |  Yes   |

URLs are passed directly as `audio_url` without upload. Local files are automatically uploaded via `/v2/upload`.

## Error Handling

### JavaScript/TypeScript

```typescript
try {
  const result = await client.preRecorded().transcribe("./audio.mp3", options);
} catch (error) {
  if (error.message.includes("401")) {
    console.error("Invalid API key");
  } else if (error.message.includes("timeout")) {
    console.error("Request timed out");
  }
}
```

### Python

```python
from gladiaio_sdk import GladiaClient

try:
    result = client.prerecorded().transcribe("audio.mp3", options)
except Exception as e:
    print(f"Error: {e}")
```

Python exports `HttpError` and `TimeoutError` for specific error handling.

## Key Differences Between JS and Python

| Aspect          | JavaScript/TypeScript                       | Python                                   |
| --------------- | ------------------------------------------- | ---------------------------------------- |
| Async model     | Promise-based (async only)                  | Sync + async (separate clients)          |
| Naming          | camelCase (`preRecorded`, `sendAudio`)      | snake_case (`prerecorded`, `send_audio`) |
| Browser support | Yes (ESM, CJS, IIFE)                        | No (server only)                         |
| Runtime         | Node 20+, Bun, browsers                     | Python 3.10+                             |
| Dependencies    | 0 runtime deps (optional `ws` for Node <22) | httpx, websockets, pyee                  |
| Options format  | Plain objects (snake_case keys)             | Dataclasses or dicts                     |
| Untyped API     | `transcribeUntyped()`, `createUntyped()`    | Dict accepted on most methods            |

## Type Exports

Both SDKs export all request/response types from the main package:

```typescript
import type {
  LiveV2InitRequest,
  LiveV2WebSocketMessage,
  PreRecordedV2Response,
  PreRecordedV2TranscriptionOptions,
} from "@gladiaio/sdk";
```

```python
from gladiaio_sdk import (
    LiveV2InitRequest,
    LiveV2WebSocketMessage,
    LiveV2LanguageConfig,
    LiveV2MessagesConfig,
    PreRecordedV2Response,
)
```

## Common Mistakes

- **Wrong sub-client method name between JS and Python**: JS uses `client.preRecorded()` and `client.liveV2()`; Python uses `client.prerecorded()` and `client.live()`. Mixing the naming conventions causes "is not a function" / `AttributeError` at runtime.
- **Forgetting `await` in JavaScript**: every JS SDK method returns a Promise. Omitting `await` on `transcribe()`, `startSession()`, etc. lets the operation run silently in the background with no result or error surfaced to your code.
- **API key exposed in browser-side code**: never embed the API key directly in front-end JavaScript — it becomes publicly readable. Use a backend proxy that forwards requests with the key server-side. See [./references/javascript.md](./references/javascript.md) for the proxy pattern.
- **Node.js < 22 without the `ws` peer dependency**: the JS SDK requires the `ws` package for WebSocket on Node < 22, which lacks a native WebSocket. Without it, live sessions fail silently. Fix: `npm install ws`.
- **Python async client in sync context**: `client.live_async()` and `client.prerecorded_async()` cannot be called from synchronous code — they require an active event loop. Use the sync client (`client.live()`, `client.prerecorded()`) unless you are inside an `async def`.

## Further Reading

- [SDK integration guide](https://docs.gladia.io/chapters/integrations/sdk)
- [JS SDK on npm](https://www.npmjs.com/package/@gladiaio/sdk)
- [Python SDK on PyPI](https://pypi.org/project/gladiaio-sdk/)
- [SDK source code](https://github.com/gladiaio/sdk)
- [Code samples](https://github.com/gladiaio/gladia-samples)
