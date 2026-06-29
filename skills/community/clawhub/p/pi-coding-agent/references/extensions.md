# Pi Extensions

TypeScript modules that extend Pi with tools, commands, events, shortcuts, and UI.

## Structure

```
~/.pi/agent/extensions/my-ext.ts         # single file
~/.pi/agent/extensions/my-ext/index.ts   # multi-file (with package.json for dependencies)
.pi/extensions/my-ext.ts                 # project-level
```

## Basics

```ts
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";

export default function (pi: ExtensionAPI) {
  // sync or async factory (async for startup initialization)
}
```

## Events

### Lifecycle

```
session_start → resources_discover → input → before_agent_start →
  agent_start → turn_start → context → before_provider_request →
    tool_execution_start → tool_call (blockable) → tool_execution_end →
  turn_end → agent_end → session_shutdown
```

| Event | Timing | Return Value |
|-------|--------|--------------|
| `session_start` | Session start/load | — |
| `session_before_switch` | Before switching sessions | `{ cancel?: boolean }` |
| `session_before_fork` | Before fork/clone | `{ cancel?: boolean }` |
| `session_before_compact` | Before compaction | `{ cancel?: boolean, compaction?: {...} }` |
| `session_compact` | Compaction done | — |
| `session_before_tree` | Before tree navigation | `{ cancel?: boolean, summary?: {...} }` |
| `session_shutdown` | Session end | — |
| `resources_discover` | Resource discovery | `{ skillPaths?, promptPaths?, themePaths? }` |
| `input` | User input | Can intercept/transform |
| `before_agent_start` | Before agent starts | `{ message?, systemPrompt? }` |
| `agent_start` / `agent_end` | Agent start/end | — |
| `turn_start` / `turn_end` | Single LLM call cycle | — |
| `message_start/update/end` | Message lifecycle | message_end can replace message |
| `context` | Before LLM call | `{ messages }` (deep copy mutable) |
| `before_provider_request` | Before sending provider request | Can replace payload |
| `after_provider_response` | After receiving response | — |
| `tool_execution_start/update/end` | Tool execution | — |
| `tool_call` | Tool called | `{ block?: boolean, reason? }` |
| `tool_result` | Tool result returned | Modifiable |
| `model_select` | Model switched | — |
| `thinking_level_select` | Thinking level switched | — |

## ExtensionAPI Methods

```ts
export default function (pi: ExtensionAPI) {
  pi.registerTool({ name, label, description, parameters: Type.Object({...}), execute })
  pi.registerCommand("name", { description, handler })
  pi.registerShortcut("ctrl+x", { handler })
  pi.registerFlag("my-flag", { description })
  pi.registerProvider("provider-name", { baseUrl, apiKey, api, models })
  pi.on("event_name", async (event, ctx) => {...})
  pi.sendMessage(text)                    // send message to agent
  pi.sendImage(text, { type:"image", data, mimeType })
  pi.appendEntry({ type, data })          // persist extension state
  pi.setThinkingLevel("high")
  pi.events                               // cross-extension event bus
}
```

## ExtensionContext API

```ts
ctx.ui.notify(text, type)        // "info" | "warn" | "error"
ctx.ui.confirm(title, message)   // → boolean
ctx.ui.select(title, options)    // → string
ctx.ui.input(title, prompt)      // → string
ctx.ui.custom(component)         // custom TUI component
ctx.ui.setStatus(name, text)     // footer status bar
ctx.ui.setWidget(name, lines)    // widget above editor
ctx.sessionManager               // session management API
ctx.getSystemPrompt()            // get current system prompt
```

## State Management

- `pi.appendEntry({ type, data })` — persist state into session JSONL
- `session_shutdown` — cleanup resources
- `session_start` — restore state

## Custom UI

Extensions can use `ctx.ui.custom()` to render custom TUI components with keyboard input, selection, forms, and more.

## Mode Behavior

Extensions in print/JSON mode: `ctx.ui.notify/confirm/select/input` work via stdout. In RPC mode, they work via the JSONL protocol.

## References

- 50+ examples: [examples/extensions/](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions)
- Available packages: `@earendil-works/pi-coding-agent`, `typebox`, `@earendil-works/pi-ai`, `@earendil-works/pi-tui`