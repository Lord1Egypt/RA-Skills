# Full Client Configuration Reference

Complete configuration options for `GladiaClient` constructor.

## Contents

- Full Config Example (JavaScript/TypeScript)
- Config Summary Table

## Full Config Example

```typescript
const client = new GladiaClient({
  apiKey: "your-key",
  apiUrl: "https://api.gladia.io",
  region: "eu-west",

  // HTTP settings
  httpHeaders: { "X-Custom-Header": "value" },
  httpTimeout: 10000, // 10s default
  httpRetry: {
    maxRetries: 3,
    retryDelay: 1000,
  },

  // WebSocket settings
  wsRetry: {
    maxRetries: 5,
    retryDelay: 1000,
  },
  wsTimeout: 30000,

  // Pre-recorded operation timeouts
  prerecordedTimeouts: {
    transcribe: 7200000, // 2 hours (full flow)
    poll: 7200000,
    upload: 300000, // 5 minutes
    create: 30000,
    get: 10000,
    delete: 10000,
    getFile: 60000,
  },

  // Live operation timeouts
  liveTimeouts: {
    get: 10000,
    delete: 10000,
    getFile: 60000,
  },
});
```

## Config Summary

| Option                  | Type     | Default                 | Description                |
| ----------------------- | -------- | ----------------------- | -------------------------- |
| `apiKey`                | `string` | `GLADIA_API_KEY` env    | API key                    |
| `apiUrl`                | `string` | `https://api.gladia.io` | Base API URL               |
| `region`                | `string` | `GLADIA_REGION` env     | `eu-west` or `us-west`     |
| `httpHeaders`           | `object` | `{}`                    | Custom HTTP headers        |
| `httpTimeout`           | `number` | `10000`                 | HTTP request timeout (ms)  |
| `httpRetry.maxRetries`  | `number` | `3`                     | Max HTTP retries           |
| `httpRetry.retryDelay`  | `number` | `1000`                  | Delay between retries (ms) |
| `wsRetry.maxRetries`    | `number` | `5`                     | Max WebSocket reconnects   |
| `wsRetry.retryDelay`    | `number` | `1000`                  | WS reconnect delay (ms)    |
| `wsTimeout`             | `number` | `30000`                 | WebSocket timeout (ms)     |
| `prerecordedTimeouts.*` | `number` | varies                  | Per-operation timeouts     |
| `liveTimeouts.*`        | `number` | varies                  | Per-operation timeouts     |
