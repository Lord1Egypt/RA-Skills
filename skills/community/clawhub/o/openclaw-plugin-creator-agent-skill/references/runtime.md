# Plugin Runtime (api.runtime) — Complete Reference

Access via `api.runtime` inside `register(api)`.

**Principle:** Use focused SDK subpath helpers when available. Use `api.runtime.*` only when the host owns the operation.

---

## Runtime namespaces

| Namespace | What it covers |
|---|---|
| `api.runtime.config` | Load and persist OpenClaw config |
| `api.runtime.agent` | Agent workspace, identity, timeouts, session store |
| `api.runtime.system` | System events, heartbeats, command execution |
| `api.runtime.media` | File/media loading and transforms |
| `api.runtime.tts` | Speech synthesis and voice listing |
| `api.runtime.mediaUnderstanding` | Image/audio/video understanding |
| `api.runtime.imageGeneration` | Image generation providers |
| `api.runtime.webSearch` | Runtime web-search execution |
| `api.runtime.modelAuth` | Resolve model/provider credentials |
| `api.runtime.subagent` | Spawn, wait, inspect, and delete subagent sessions |
| `api.runtime.channel` | Channel-heavy helpers (prefer narrower subpaths first) |

---

## api.runtime.config

```typescript
// Read config (synchronous snapshot)
const cfg = api.runtime.config.loadConfig();

// Write config (async, triggers config watch reload)
await api.runtime.config.writeConfigFile({
  ...cfg,
  talk: { enabled: true },
  plugins: {
    ...cfg.plugins,
    entries: {
      ...cfg.plugins?.entries,
      "my-plugin": { enabled: true, config: { key: "value" } },
    },
  },
});
```

> Do NOT cache config snapshots longer than needed — config can change at runtime.

---

## api.runtime.tts

```typescript
// List voices for a provider
const voices = await api.runtime.tts.listVoices({
  provider: "openai",   // or "elevenlabs", "microsoft"
  cfg: api.config,
});
// voices: Array<{ id: string; name?: string; ... }>

// Telephony TTS (for voice call plugins)
const result = await api.runtime.tts.textToSpeechTelephony({
  text: "Hello from OpenClaw",
  cfg: api.config,
});
// Returns: { audioBuffer: Buffer, sampleRate: number }
// Plugin must resample/encode for provider
// NOTE: Edge TTS NOT supported for telephony
```

---

## api.runtime.webSearch

```typescript
const results = await api.runtime.webSearch.search({
  query: "latest TypeScript features",
  maxResults: 5,
});
// results: Array<{ title: string; url: string; snippet: string }>
```

---

## api.runtime.subagent

```typescript
// Spawn a subagent session
const session = await api.runtime.subagent.spawn({
  agentId: "assistant",
  prompt: "Summarize this document",
  input: { text: documentContent },
});

// Wait for completion
const result = await api.runtime.subagent.wait(session.id, {
  timeoutMs: 30000,
});

// Inspect status
const status = await api.runtime.subagent.inspect(session.id);

// Clean up
await api.runtime.subagent.delete(session.id);
```

---

## api.runtime.imageGeneration

```typescript
const image = await api.runtime.imageGeneration.generate({
  prompt: "A futuristic cityscape at night",
  width: 1024,
  height: 1024,
  provider: "my-provider",  // optional, uses default if omitted
});
// image: { url?: string; base64?: string; mimeType: string }
```

---

## api.runtime.mediaUnderstanding

```typescript
const description = await api.runtime.mediaUnderstanding.describeImage({
  imageUrl: "https://example.com/photo.jpg",
  // or imageBase64: "...",
});

const transcript = await api.runtime.mediaUnderstanding.transcribeAudio({
  audioBuffer: Buffer,
  mimeType: "audio/mp3",
});
```

---

## api.runtime.channel

For native channel plugins needing tight coupling with the OpenClaw messaging stack. Prefer narrower subpaths first:
- `plugin-sdk/channel-pairing` → pairing flows
- `plugin-sdk/channel-actions` → message tool buttons/cards
- `plugin-sdk/channel-feedback` → reactions wiring
- `plugin-sdk/channel-lifecycle` → account status

Use `api.runtime.channel.*` only when no smaller public seam exists.

---

## createPluginRuntimeStore

For shared mutable state that must be initialized before use:

```typescript
import { createPluginRuntimeStore } from "openclaw/plugin-sdk/runtime-store";

interface MyRuntime {
  client: SomeClient;
  logger: Logger;
  accountId: string;
}

// Pass a clear error message for when getRuntime() is called before setRuntime()
const store = createPluginRuntimeStore<MyRuntime>(
  "My Plugin runtime not initialized. Is the plugin connected?"
);

// Exports to use in index.ts (setRuntime) and src/ (getRuntime)
export const setMyRuntime = (rt: MyRuntime) => store.setRuntime(rt);
export const getMyRuntime = () => store.getRuntime();          // throws if not set
export const tryGetMyRuntime = () => store.tryGetRuntime();   // returns undefined if not set
export const clearMyRuntime = () => store.clearRuntime();     // for cleanup

// Usage in channel lifecycle:
async connect({ cfg, runtime }) {
  const client = new SomeClient(cfg.channels["my-channel"].token);
  await client.connect();
  setMyRuntime({ client, logger: api.logger, accountId: "default" });
}

async disconnect() {
  const { client } = getMyRuntime();
  await client.disconnect();
  clearMyRuntime();
}
```

---

## Runtime safety guidelines

- Do NOT cache config snapshots longer than needed
- Prefer `createPluginRuntimeStore(...)` for shared module state — never use unguarded `let runtime`
- Keep runtime-backed code behind small local helpers
- Avoid reaching into runtime namespaces you do not need
- `api.runtime.channel.*` is the heaviest namespace — always prefer focused subpaths
