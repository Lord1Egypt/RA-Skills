# Hook Examples - OpenClaw Hook Usage Examples

## Overview

OpenClaw supports 16+ Hook types that can intercept and modify behavior at various stages.

## Available Hooks

| Hook | Timing | Can Block? |
|------|--------|------------|
| before_model_resolve | Before model resolution | ❌ |
| before_prompt_build | Before prompt building | ❌ |
| before_tool_call | Before tool call | ✅ |
| after_tool_call | After tool call | ❌ |
| message_sending | Before message sending | ✅ cancel |
| message_sent | After message sent | ❌ |
| subagent_spawning | Before subagent spawn | ❌ |
| subagent_ended | After subagent ended | ❌ |

## Example 1: Tool Audit Log

Record all tool calls to a file:

```javascript
api.registerHook("before_tool_call", async ({ event, ctx }) => {
  const log = {
    time: new Date().toISOString(),
    tool: event.tool.name,
    params: event.tool.params,
    session: ctx.sessionKey
  };
  // Write to log file
  console.log("[TOOL_AUDIT]", JSON.stringify(log));
  return {}; // Don't block, continue execution
});
```

## Example 2: Dangerous Tool Interception

Block dangerous tools in non-elevated sessions:

```javascript
api.registerHook("before_tool_call", async ({ event, ctx }) => {
  const dangerous = ["gateway", "cron", "nodes"];
  if (dangerous.includes(event.tool.name) && !ctx.session.elevated) {
    return { 
      block: true, 
      reason: `Tool '${event.tool.name}' requires elevated permissions` 
    };
  }
  return {};
});
```

## Example 3: Parameter Validation

Validate dangerous commands in exec tool:

```javascript
api.registerHook("before_tool_call", async ({ event, ctx }) => {
  if (event.tool.name === "exec") {
    const cmd = event.tool.params.command || "";
    const dangerous = ["rm -rf", "dd if=", "mkfs", ":(){:|:&}:"];
    for (const d of dangerous) {
      if (cmd.includes(d)) {
        return { 
          block: true, 
          reason: `Dangerous command pattern detected: ${d}` 
        };
      }
    }
  }
  return {};
});
```

## Example 4: Dynamic Model Switching

Switch models based on task type:

```javascript
api.registerHook("before_model_resolve", async ({ event, ctx }) => {
  const msg = event.messages?.[0]?.content || "";
  if (msg.includes("write code") || msg.includes("debug")) {
    return { 
      model: "ollama/deepseek-r1:70b",
      provider: "ollama"
    };
  }
  if (msg.includes("document") || msg.includes("summary")) {
    return { 
      model: "ollama/qwen3:14b",
      provider: "ollama"
    };
  }
  return {};
});
```

## Example 5: Subagent Result Routing

Custom subagent result delivery:

```javascript
api.registerHook("subagent_ended", async ({ event, ctx }) => {
  // Do extra processing here
  console.log("[SUBAGENT_ENDED]", event.result);
  return {}; 
});
```

## Registration

Register in the plugin's `register(api)`:

```javascript
export default definePluginEntry({
  id: "my-hook-plugin",
  name: "My Hook Plugin",
  register(api) {
    api.registerHook("before_tool_call", myHandler);
  }
});
```

## Notes

- Returning `{ block: true }` from a hook blocks the operation
- `before_model_resolve` can return `{ model, provider }` to override
- Hooks are synchronous; avoid long-running operations
- Multiple hooks execute in priority order
