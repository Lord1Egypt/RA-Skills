# Plugin Testing — Complete Reference

OpenClaw uses **Vitest** with V8 coverage thresholds.

---

## Test utilities import

```typescript
import {
  installCommonResolveTargetErrorCases,
  shouldAckReaction,
  removeAckReactionAfterReply,
} from "openclaw/plugin-sdk/testing";

import type {
  ChannelAccountSnapshot,
  ChannelGatewayContext,
  OpenClawConfig,
  PluginRuntime,
  RuntimeEnv,
  MockFn,
} from "openclaw/plugin-sdk/testing";
```

---

## Testing a channel plugin

```typescript
import { describe, it, expect, vi } from "vitest";
import { installCommonResolveTargetErrorCases } from "openclaw/plugin-sdk/testing";
import { channelPlugin } from "../src/channel.js";

describe("my-channel target resolution", () => {
  // Install standard error cases (no-target, invalid format, etc.)
  installCommonResolveTargetErrorCases({
    resolveTarget: ({ to, mode, allowFrom }) =>
      channelPlugin.messaging.resolveTarget({ to, mode, allowFrom }),
    implicitAllowFrom: ["user1", "user2"],
  });

  it("resolves @username targets", () => {
    const result = channelPlugin.messaging.resolveTarget({
      to: "@alice",
      mode: "direct",
      allowFrom: ["alice"],
    });
    expect(result.target).toBe("alice");
    expect(result.chatType).toBe("direct");
  });
});

describe("my-channel account config", () => {
  it("resolves account from config", () => {
    const cfg = {
      channels: { "my-channel": { token: "test-token", allowFrom: ["user1"] } },
    };
    const account = channelPlugin.config.resolveAccount(cfg as any, undefined);
    expect(account.token).toBe("test-token");
  });

  it("inspects account without exposing secrets", () => {
    const cfg = {
      channels: { "my-channel": { token: "test-token" } },
    };
    const inspection = channelPlugin.config.inspectAccount(cfg as any, undefined);
    expect(inspection.configured).toBe(true);
    // Should NOT expose the token value
    expect(inspection).not.toHaveProperty("token");
  });
});
```

---

## Testing a provider plugin

```typescript
import { describe, it, expect } from "vitest";
import { acmeProvider } from "../src/provider.js";

describe("acme-ai provider", () => {
  it("resolves dynamic models", () => {
    const model = acmeProvider.resolveDynamicModel!({
      modelId: "acme-beta-v3",
    } as any);
    expect(model.id).toBe("acme-beta-v3");
    expect(model.provider).toBe("acme-ai");
    expect(model.api).toBe("openai-completions");
  });

  it("returns catalog when API key is available", async () => {
    const result = await acmeProvider.catalog!.run({
      resolveProviderApiKey: () => ({ apiKey: "test-key" }),
    } as any);
    expect(result?.provider?.models).toHaveLength(2);
    expect(result?.provider?.baseUrl).toBe("https://api.acme-ai.com/v1");
  });

  it("returns null catalog when no key", async () => {
    const result = await acmeProvider.catalog!.run({
      resolveProviderApiKey: () => ({ apiKey: undefined }),
    } as any);
    expect(result).toBeNull();
  });
});
```

---

## Mocking api.runtime (createPluginRuntimeStore)

```typescript
import { vi } from "vitest";
import { createPluginRuntimeStore } from "openclaw/plugin-sdk/runtime-store";
import type { PluginRuntime } from "openclaw/plugin-sdk/testing";

const store = createPluginRuntimeStore<PluginRuntime>("test runtime not set");

// In beforeEach
const mockRuntime = {
  agent: {
    resolveAgentDir: vi.fn().mockReturnValue("/tmp/agent"),
    getSessionStore: vi.fn(),
  },
  config: {
    loadConfig: vi.fn().mockReturnValue({}),
    writeConfigFile: vi.fn().mockResolvedValue(undefined),
  },
  tts: {
    textToSpeechTelephony: vi.fn(),
    listVoices: vi.fn().mockResolvedValue([]),
  },
  system: {},
} as unknown as PluginRuntime;

beforeEach(() => {
  store.setRuntime(mockRuntime);
});

afterEach(() => {
  store.clearRuntime();
  vi.clearAllMocks();
});
```

---

## Per-instance stubs (preferred over prototype mutation)

```typescript
// ✅ Preferred: per-instance stub
const client = new MyChannelClient();
client.sendMessage = vi.fn().mockResolvedValue({ id: "msg-1" });
client.connect = vi.fn().mockResolvedValue(undefined);

// ❌ Avoid: prototype mutation (affects all instances)
// MyChannelClient.prototype.sendMessage = vi.fn();
```

---

## Reaction helpers

```typescript
import { shouldAckReaction, removeAckReactionAfterReply } from "openclaw/plugin-sdk/testing";

it("should add ack reaction on message receipt", () => {
  const result = shouldAckReaction(channelPlugin, {
    chatType: "direct",
    channelId: "my-channel",
  });
  expect(result).toBe(true);
});
```

---

## Contract tests (in-repo / bundled plugins)

```bash
# Verify registration ownership (which plugin owns which providers/channels)
pnpm test -- src/plugins/contracts/shape.contract.test.ts
pnpm test -- src/plugins/contracts/auth.contract.test.ts
pnpm test -- src/plugins/contracts/runtime.contract.test.ts
```

---

## Lint rules (enforced by pnpm check for in-repo plugins)

1. **No monolithic root imports** — `openclaw/plugin-sdk` root barrel is rejected
2. **No direct `src/` imports** — plugins cannot `import "../../src/..."` directly
3. **No self-imports** — plugins cannot import their own `plugin-sdk/<name>` subpath

External plugins aren't subject to lint rules, but following the same patterns is recommended.

---

## Running tests

```bash
# All tests
pnpm test

# Specific plugin
pnpm test -- extensions/my-plugin/

# Specific file
pnpm test -- extensions/my-plugin/src/channel.test.ts

# Filter by test name
pnpm test -- extensions/my-plugin/ -t "resolves account"

# With coverage
pnpm test:coverage

# Low-memory mode (for memory-constrained environments)
OPENCLAW_TEST_PROFILE=low OPENCLAW_TEST_SERIAL_GATEWAY=1 pnpm test
```

---

## Skills vs Plugins vs Webhooks (quick decision)

| Question | → Use |
|---|---|
| "I want to call an external API" | **Skill** (SKILL.md) |
| "I want a new messaging channel" | **Plugin (channel)** |
| "I want to add a new LLM backend" | **Plugin (provider)** |
| "External systems should trigger OpenClaw" | **Webhook** |
| "I need runtime hooks or Gateway access" | **Plugin** |
| "I want to extend the CLI" | **Plugin** |

Start with a Skill. Add a Plugin when you need runtime depth. Add a Webhook when external systems push events.
