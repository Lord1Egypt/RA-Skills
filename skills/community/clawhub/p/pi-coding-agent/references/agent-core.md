# @earendil-works/pi-agent-core

Agent runtime, built on @earendil-works/pi-ai.

## Agent Class

```ts
const agent = new Agent({
  initialState: { systemPrompt, model, thinkingLevel, tools, messages },
  convertToLlm: (msgs) => msgs.filter(m => ["user","assistant","toolResult"].includes(m.role)),
  toolExecution: "parallel",    // or "sequential"
  steeringMode: "one-at-a-time", followUpMode: "one-at-a-time",
  beforeToolCall, afterToolCall, transformContext, streamFn, sessionId, getApiKey,
  thinkingBudgets: { minimal: 128, low: 512, medium: 1024, high: 2048 },
});
```

## Event Stream

`prompt → agent_start → turn_start → message_start/update/end → tool_execution_start/update/end → turn_end → agent_end`

10 event types: agent_start/end, turn_start/end, message_start/update/end, tool_execution_start/update/end

## Tool Definition

```ts
import { Type } from "typebox";

const tool = {
  name: "read_file", description: "Read a file",
  parameters: Type.Object({ path: Type.String() }),
  executionMode: "sequential",           // optional: override global
  execute: async (toolCallId, params, signal, onUpdate) => ({
    content: [{ type: "text", text: await fs.readFile(params.path, "utf-8") }],
    details: { path: params.path },
    // terminate: true                    // optional: stop after this tool completes
  }),
};
```

**Tool parallelism**: default parallel (preflight sequential, execution concurrent), can set sequential. If any tool sets sequential, the entire batch runs sequentially.
**Errors**: throw Error (no error content returned), agent reports to LLM with isError:true.

## AgentState

```ts
agent.state = {
  systemPrompt, model, thinkingLevel, tools, messages,
  isStreaming, streamingMessage?, pendingToolCalls, errorMessage?
}
// assignment copies top-level arrays; .push() mutates directly
```

## Steering & Follow-Up

```ts
agent.steer(msg); agent.followUp(msg);       // send while running
agent.clearSteeringQueue(); agent.clearAllQueues();
```

## Custom Message Types

```ts
declare module "@earendil-works/pi-agent-core" {
  interface CustomAgentMessages {
    mytype: { role: "notification"; text: string; timestamp: number };
  }
}
// filter custom types in convertToLlm
```

## Low-Level API

```ts
import { agentLoop, agentLoopContinue } from "@earendil-works/pi-agent-core";
for await (const e of agentLoop([msg], ctx, cfg)) { /* observational events */ }
```

## streamProxy (Browser Proxy)

```ts
const agent = new Agent({
  streamFn: (model, ctx, opt) => streamProxy(model, ctx, { ...opt, authToken, proxyUrl }),
});
```

## Method Reference

| Method | Description |
|--------|-------------|
| `agent.prompt(msg, images?)` | Send a message |
| `agent.continue()` | Continue from current context |
| `agent.reset()` / `agent.abort()` | Reset / Cancel |
| `agent.waitForIdle()` | Wait for completion |
| `agent.subscribe(fn)` | Subscribe to events → unsubscribe |