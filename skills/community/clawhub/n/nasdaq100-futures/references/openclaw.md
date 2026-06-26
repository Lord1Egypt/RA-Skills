## OpenClaw / ClawHub runtime notes

### Entry point

This skill exposes `get_nasdaq100_futures` (see `manifest.json`). The runtime entrypoint is:

- `handler`: `scripts/main.handler`

### Event shape

The function parameters are provided under `event.parameters`:

```json
{
  "parameters": {
    "symbol": "NQ=F"
  }
}
```

### Requirements

- Node.js **>= 18** (uses built-in `fetch`)

