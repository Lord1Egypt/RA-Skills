---
name: openclaw-plugin-dev
description: OpenClaw Plugin Development Guide. For creating OpenClaw plugins, including hook mechanisms, logging, configuration management, etc. Trigger words: develop plugin, create plugin, plugin development, llm_input hook, llm_output hook, wrapStreamFn.
---

# OpenClaw Plugin Development Guide

## Core Concepts

### Hook Mechanism

OpenClaw provides various hooks to intercept and process events:

| Hook | Trigger Timing | Usage |
|------|----------------|-------|
| `llm_input` | Before an LLM request is sent | Capture requests (prompt, systemPrompt, historyMessages) |
| `llm_output` | After an LLM response is completed | Capture responses (assistantTexts, usage) |
| `agent_start` | When an Agent session starts | Initialize session state |
| `agent_end` | When an Agent session ends | Clean up resources and record statistics |

### Request-Response Correlation

Use `runId` to correlate requests and responses:

```typescript
const inFlightRequests = new Map<string, RequestData>();

api.on("llm_input", (event: any) => {
  const runId = event.runId;
  inFlightRequests.set(runId, { timestamp: Date.now(), input: event });
});

api.on("llm_output", (event: any) => {
  const runId = event.runId;
  const request = inFlightRequests.get(runId);
  // Successfully paired, record the complete request-response
  inFlightRequests.delete(runId);
});
```

## Plugin Structure

```
~/.openclaw/extensions/plugin-name/
├── openclaw.plugin.json    # Plugin manifest
├── index.ts                # Main entry
├── logger.ts               # Utility module (optional)
└── README.md               # Documentation (optional)
```

### Manifest Example

```json
{
  "id": "plugin-name",
  "name": "Plugin Name",
  "version": "1.0.0",
  "main": "index.ts",
  "description": "Plugin description"
}
```

### Main Entry Template

```typescript
type OpenClawPluginApi = {
  config?: any;
  pluginConfig?: unknown;
  logger: { info: (msg: string) => void; warn: (msg: string) => void; error: (msg: string) => void };
  on: (hookName: string, handler: (event: any, ctx?: any) => void, opts?: { priority?: number }) => void;
};

const plugin = {
  id: "plugin-name",
  name: "Plugin Name",
  description: "Plugin description",
  
  register(api: OpenClawPluginApi) {
    // Get configuration
    const config = api.config?.plugins?.entries?.["plugin-name"]?.config ?? {};
    
    // Register hooks
    api.on("llm_input", (event) => { /* Handle request */ });
    api.on("llm_output", (event) => { /* Handle response */ });
  },
};

export default plugin;
```

## Common Patterns

### Logging

```typescript
// JSONL format, split files by date
const logPath = path.join(basePath, `${new Date().toISOString().split('T')[0]}.jsonl`);
fs.appendFileSync(logPath, JSON.stringify(entry) + "\n");
```

### Configuration Management

```typescript
const DEFAULT_CONFIG = {
  enabled: true,
  logPath: "~/.openclaw/logs/plugin-name",
};

const config = { ...DEFAULT_CONFIG, ...rawConfig };
```

## Notes

### Hook Lifecycle

- `llm_output` **depends on normal session termination**
- `llm_output` may not fire if the session is interrupted (gateway restart, user sends a new message)
- Design for interruption scenarios to avoid resource leaks

### Debugging Methods

```bash
# Check gateway logs to confirm hook triggering
grep "llm_output" ~/.openclaw/logs/gateway.log

# Check plugin loading
grep "plugin-name" ~/.openclaw/logs/gateway.log
```

### Configuration Location

Enable the plugin in `openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "plugin-name": {
        "enabled": true,
        "config": {
          "option1": "value1"
        }
      }
    }
  }
}
```

## Example: LLM API Logger

Full example available at `https://github.com/cicadaFang/openclaw-llm-api-logger`

Features:
- Log all LLM API requests and responses
- JSONL formatted logs, split by date
- Correlate requests and responses using runId
- Record metrics such as durationMs and usage