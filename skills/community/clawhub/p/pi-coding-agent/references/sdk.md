# Pi SDK Integration

`npm install @earendil-works/pi-coding-agent`

## Quick Start

```ts
import { AuthStorage, createAgentSession, ModelRegistry, SessionManager } from "@earendil-works/pi-coding-agent";
const { session } = await createAgentSession({
  sessionManager: SessionManager.inMemory(), authStorage: AuthStorage.create(),
  modelRegistry: ModelRegistry.create(AuthStorage.create()),
});
session.subscribe(e => { if (e.type === "message_update" && e.assistantMessageEvent.type === "text_delta") process.stdout.write(e.assistantMessageEvent.delta); });
await session.prompt("What files are here?");
```

## createAgentSession() Parameters

```ts
const { session } = await createAgentSession({
  model?, tools?, customTools?, noTools?("all"|"builtin"),
  thinkingLevel?, cwd?, agentDir?,
  sessionManager?, resourceLoader?, authStorage?, modelRegistry?,
})
```

Defaults: cwd=process.cwd(), agentDir=~/.pi/agent, tools=[read,bash,edit,write], sessionManager=inMemory()

## AgentSession API

```ts
interface AgentSession {
  prompt(text, options?): Promise<void>;     // streamingBehavior?:"steer"|"followUp", images?
  steer(text): Promise<void>;
  followUp(text): Promise<void>;
  subscribe(fn): () => void;

  sessionFile, sessionId, agent, model, thinkingLevel, messages, isStreaming;
  setModel(m), setThinkingLevel(l), cycleModel(), cycleThinkingLevel();
  navigateTree(targetId, opts?): Promise<{editorText?,cancelled}>;
  compact(instructions?): Promise<CompactionResult>;
  abort(): Promise<void>;
  dispose(): void;
}
```

## Custom Tools

```ts
import { defineTool } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";

const myTool = defineTool({
  name: "my_tool", description: "Does something",
  parameters: Type.Object({ input: Type.String() }),
  execute: async (id, params) => ({ content: [{ type: "text", text: params.input }], details: {} }),
});
const { session } = await createAgentSession({ customTools: [myTool], tools: ["read", "my_tool"] });
```

## ResourceLoader Custom Loading

```ts
const loader = new DefaultResourceLoader({
  additionalExtensionPaths: ["/path/to/ext.ts"],
  extensionFactories: [(pi) => { pi.on("agent_start", () => {...}); }],
  skillsOverride: (cur) => ({ skills: [...cur.skills, mySkill], diagnostics: cur.diagnostics }),
  eventBus,
});
await loader.reload();
const { session } = await createAgentSession({ resourceLoader: loader });
```

## AgentSessionRuntime (Session Replacement)

```ts
const runtime = await createAgentSessionRuntime(createRuntime, {
  cwd: process.cwd(), agentDir: getAgentDir(),
  sessionManager: SessionManager.create(process.cwd()),
});
// runtime.session changes after newSession/switchSession/fork/clone, re-subscribe needed
await runtime.newSession();
```

## References

- [examples/sdk/](https://github.com/earendil-works/pi/tree/main/packages/coding-agent/examples/sdk)
- [OpenClaw real integration](https://github.com/OpenClaw/OpenClaw)
- [SessionManager API](session-format.md) | [Extensions API](extensions.md)