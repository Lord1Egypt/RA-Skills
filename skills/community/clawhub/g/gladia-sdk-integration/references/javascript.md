# JavaScript / TypeScript SDK

Patterns and details specific to the `@gladiaio/sdk` package.

## Contents

- Package Info
- Browser Usage (ESM, IIFE, API key security via proxy)
- File Upload in Browsers
- Node.js Specifics (file paths, WebSocket for Node < 22, streaming from file/mic)
- Untyped API
- TypeScript Types
- Error Handling
- Live Session Event Typing
- CDN / IIFE Bundle
- Package Size

## Package Info

- **npm**: [@gladiaio/sdk](https://www.npmjs.com/package/@gladiaio/sdk)
- **Version**: 1.0.4 (auto-synced by CI — see [sdk-versions.md](./sdk-versions.md))
- **Runtime**: Node.js 20+, Bun, browsers
- **Bundle formats**: ESM, CJS, IIFE (via unpkg/jsdelivr)
- **Dependencies**: 0 runtime deps
- **Peer deps**: `ws` (only for Node < 22, which lacks native WebSocket)

## Browser Usage

The SDK works in browsers out of the box. Use ESM imports or the IIFE bundle:

```html
<script src="https://unpkg.com/@gladiaio/sdk/dist/index.iife.js"></script>
<script>
  const client = new GladiaSDK.GladiaClient({ apiKey: "..." });
</script>
```

### API Key Security in Browsers

Never expose your API key in client-side code for production. Instead, use a proxy:

```typescript
// Point the SDK at your backend proxy (no apiKey needed)
const client = new GladiaClient({
  apiUrl: "https://your-server.com/api/gladia",
});
```

Your backend proxy adds the `x-gladia-key` header before forwarding to `api.gladia.io`.

## File Upload in Browsers

Use `File` or `Blob` objects for uploads:

```typescript
const fileInput = document.querySelector('input[type="file"]');
const file = fileInput.files[0];

const result = await client.preRecorded().transcribe(file, {
  language_config: { languages: ["en"] },
});
```

## Node.js Specifics

### File path input

```typescript
// Node: pass a file path string
const result = await client
  .preRecorded()
  .transcribe("./recordings/meeting.wav", options);
```

### WebSocket for Node < 22

Node versions before 22 don't have native WebSocket. Install the `ws` package:

```bash
npm install ws
```

The SDK auto-detects and uses it. Node 22+ uses the built-in `WebSocket` global.

### Streaming audio from a file

```typescript
import { createReadStream } from "fs";

const session = client.liveV2().startSession({
  encoding: "wav/pcm",
  sample_rate: 16000,
  bit_depth: 16,
  channels: 1,
  language_config: { languages: ["en"] },
});

session.once("started", () => {
  const stream = createReadStream("./audio.pcm", { highWaterMark: 3200 });
  stream.on("data", (chunk) => session.sendAudio(chunk));
  stream.on("end", () => session.stopRecording());
});
```

### Streaming from microphone (Node)

Use a library like `node-mic` or `node-record-lpcm16`:

```typescript
import mic from "mic";

const micInstance = mic({ rate: 16000, bitwidth: 16, channels: 1 });
const micStream = micInstance.getAudioStream();

session.once("started", () => {
  micStream.on("data", (chunk) => session.sendAudio(chunk));
  micInstance.start();
});

// Stop
micInstance.stop();
session.stopRecording();
```

## Untyped API

For maximum flexibility or when migrating from raw HTTP calls:

```typescript
// Pass raw JSON matching the API schema
const result = await client.preRecorded().createUntyped({
  audio_url: "https://example.com/audio.mp3",
  diarization: true,
  custom_field: "value",
});

// Full untyped transcribe flow
const result = await client.preRecorded().transcribeUntyped("./file.mp3", {
  language_config: { languages: ["en"] },
});
```

## TypeScript Types

All types are exported from the main package:

```typescript
import type {
  GladiaClientOptions,
  PreRecordedV2TranscriptionOptions,
  PreRecordedV2Response,
  PreRecordedV2InitTranscriptionRequest,
  LiveV2InitRequest,
  LiveV2Session,
  LiveV2WebSocketMessage,
  LiveV2TranscriptMessage,
} from "@gladiaio/sdk";
```

## Error Handling

The JS SDK throws standard `Error` objects. Check the message for HTTP status codes:

```typescript
try {
  await client.preRecorded().transcribe(audio, options);
} catch (err) {
  if (err instanceof Error) {
    if (err.message.includes("401")) {
      /* auth error */
    }
    if (err.message.includes("429")) {
      /* rate limited */
    }
    if (err.message.includes("timeout")) {
      /* timed out */
    }
  }
}
```

## Live Session Event Typing

```typescript
import type { LiveV2WebSocketMessage } from "@gladiaio/sdk";

session.on("message", (msg: LiveV2WebSocketMessage) => {
  // msg.type is a discriminated union
  if (msg.type === "transcript") {
    msg.data.is_final; // boolean
    msg.data.utterance.text; // string
  }
});
```

## CDN / IIFE Bundle

For quick prototyping without a bundler:

```html
<script src="https://cdn.jsdelivr.net/npm/@gladiaio/sdk/dist/index.iife.js"></script>
```

Global namespace: `window.GladiaSDK`

## Package Size

~741 KB unpacked (134 files). Tree-shaking-friendly ESM exports keep bundle size small when using a bundler.
