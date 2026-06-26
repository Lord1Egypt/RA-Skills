# Channel Plugin — Complete Guide

Channel plugins connect OpenClaw to a messaging platform (Discord, Slack, WhatsApp, custom, etc.)

---

## Complete file structure

```
extensions/my-channel/
├── package.json
├── openclaw.plugin.json
├── index.ts                  ← defineChannelPluginEntry
├── setup-entry.ts            ← defineSetupPluginEntry (lightweight)
└── src/
    ├── channel.ts            ← ChannelPlugin object
    ├── runtime.ts            ← createPluginRuntimeStore
    ├── channel.setup.ts      ← ChannelSetupWizard
    ├── actions.ts            ← message tool actions
    └── channel.test.ts
```

---

## 1. channel.ts — ChannelPlugin object

```typescript
import { createChatChannelPlugin } from "openclaw/plugin-sdk/core";
import { buildChannelConfigSchema } from "openclaw/plugin-sdk/core";
import { createChannelPairingController } from "openclaw/plugin-sdk/channel-pairing";
import { createMessageToolButtonsSchema } from "openclaw/plugin-sdk/channel-actions";
import { z } from "zod";
import type { ChannelPlugin } from "openclaw/plugin-sdk/channel-contract";

// Config schema using Zod + buildChannelConfigSchema
const accountSchema = z.object({
  token: z.string().optional(),
  allowFrom: z.array(z.string()).optional(),
  accounts: z.object({}).catchall(z.any()).optional(),
  defaultAccount: z.string().optional(),
});
const configSchema = buildChannelConfigSchema(accountSchema);

export const channelPlugin: ChannelPlugin = {
  meta: {
    id: "my-channel",
    label: "My Channel",
    blurb: "OpenClaw on MyPlatform",
    docsPath: "/channels/my-channel",
  },

  capabilities: {
    replies: true,
    reactions: true,
    threads: false,
    polls: false,
    media: ["image", "audio"],
    chatTypes: ["direct", "group"],
  },

  config: {
    schema: configSchema,
    resolveAccount: (cfg, accountId) => {
      const channelCfg = (cfg.channels as any)?.["my-channel"];
      return { token: channelCfg?.token, allowFrom: channelCfg?.allowFrom };
    },
    inspectAccount: (cfg, accountId) => {
      const channelCfg = (cfg.channels as any)?.["my-channel"];
      return {
        configured: Boolean(channelCfg?.token),
        tokenStatus: channelCfg?.token ? "available" : "missing",
      };
    },
  },

  security: {
    dmPolicy: "allowlist",
    defaultAllowFrom: [],
  },

  messaging: {
    resolveTarget: ({ to, mode, allowFrom }) => {
      // Parse target string (e.g. "@username", "channel-id")
      if (!to) return { error: "no target provided" };
      return { target: to, chatType: "direct" };
    },

    resolveOutboundSessionRoute: ({ cfg, agentId, accountId, target }) => {
      return buildChannelOutboundSessionRoute({
        cfg,
        agentId,
        channel: "my-channel",
        accountId,
        peer: { kind: "direct", id: target },
        chatType: "direct",
        from: accountId ?? "default",
        to: target,
      });
    },
  },

  actions: {
    describeMessageTool() {
      return {
        actions: ["send", "edit", "react"],
        capabilities: ["buttons"],
        schema: {
          visibility: "current-channel",
          properties: {
            buttons: createMessageToolButtonsSchema(),
            threadId: Type.Optional(Type.String()),
          },
        },
      };
    },
    async handleAction(ctx) {
      if (ctx.action === "send") {
        const { client } = getMyRuntime();
        await client.sendMessage(ctx.params.to, ctx.params.text);
        return { content: [{ type: "text", text: "sent" }] };
      }
      return { content: [{ type: "text", text: `unsupported: ${ctx.action}` }] };
    },
  },

  setup: {
    resolveAccount: (cfg, accountId) => {
      // Same as config.resolveAccount, drives setup wizard inspection
      return (cfg.channels as any)?.["my-channel"];
    },
    inspectAccount: (cfg, accountId) => ({
      configured: Boolean((cfg.channels as any)?.["my-channel"]?.token),
    }),
    setupWizard: mySetupWizard,  // see channel.setup.ts
  },

  lifecycle: {
    async connect({ cfg, accountId, runtime }) {
      const token = (cfg.channels as any)?.["my-channel"]?.token;
      const client = new MyPlatformClient(token);
      
      client.on("message", (msg) => {
        runtime.ingest({
          channelId: "my-channel",
          accountId: accountId ?? "default",
          from: msg.from,
          to: msg.to,
          text: msg.text,
          raw: msg,
        });
      });

      await client.connect();
      return { client };
    },

    async disconnect({ runtime }) {
      const { client } = getMyRuntime();
      await client.disconnect();
    },
  },

  pairing: createChannelPairingController({
    channel: "my-channel",
    // Uses pairing storage helpers: allowlist reads, request upserts, challenge issuance
  }),
};
```

---

## 2. runtime.ts — Runtime store

```typescript
import { createPluginRuntimeStore } from "openclaw/plugin-sdk/runtime-store";
import type { MyPlatformClient } from "./client.js";

interface MyChannelRuntime {
  client: MyPlatformClient;
}

const store = createPluginRuntimeStore<MyChannelRuntime>(
  "My Channel runtime not initialized — plugin may not be connected"
);

export const setMyRuntime = (rt: MyChannelRuntime) => store.setRuntime(rt);
export const getMyRuntime = () => store.getRuntime();
export const tryGetMyRuntime = () => store.tryGetRuntime();
```

---

## 3. index.ts — Entry point

```typescript
import { defineChannelPluginEntry } from "openclaw/plugin-sdk/core";
import { channelPlugin } from "./src/channel.js";
import { setMyRuntime } from "./src/runtime.js";

export default defineChannelPluginEntry({
  id: "my-channel",
  name: "My Channel",
  description: "Connects OpenClaw to MyPlatform",
  plugin: channelPlugin,
  setRuntime: setMyRuntime,

  registerFull(api) {
    // Only runtime-only registrations here
    api.registerTool({
      name: "my_channel_status",
      description: "Inspect My Channel connection state",
      parameters: { type: "object", properties: {} },
      async execute() {
        const rt = tryGetMyRuntime();
        return { content: [{ type: "text", text: rt ? "connected" : "disconnected" }] };
      },
    });
  },
});
```

---

## 4. setup-entry.ts

```typescript
import { defineSetupPluginEntry } from "openclaw/plugin-sdk/core";
import { channelPlugin } from "./src/channel.js";

export default defineSetupPluginEntry(channelPlugin);
```

---

## 5. Setup wizard (channel.setup.ts)

```typescript
import type { ChannelSetupWizard } from "openclaw/plugin-sdk/channel-setup";
import { createStandardChannelSetupStatus } from "openclaw/plugin-sdk/setup";

export const mySetupWizard: ChannelSetupWizard = {
  channel: "my-channel",

  status: createStandardChannelSetupStatus({
    channel: "my-channel",
    configuredLabel: "Connected to MyPlatform",
    unconfiguredLabel: "Not configured",
    resolveConfigured: ({ cfg }) =>
      Boolean((cfg.channels as any)?.["my-channel"]?.token),
  }),

  credentials: [
    {
      inputKey: "token",
      providerHint: "my-channel",
      credentialLabel: "Bot token",
      preferredEnvVar: "MY_CHANNEL_BOT_TOKEN",
      envPrompt: "Use MY_CHANNEL_BOT_TOKEN from environment?",
      keepPrompt: "Keep current token?",
      inputPrompt: "Enter your MyPlatform bot token:",
      inspect: ({ cfg, accountId }) => {
        const token = (cfg.channels as any)?.["my-channel"]?.token;
        return {
          accountConfigured: Boolean(token),
          hasConfiguredValue: Boolean(token),
          // Never expose the token value here
        };
      },
    },
  ],

  // Optional: DM policy, allowFrom prompts, prepare/finalize hooks
  // For standard allowFrom flows, use:
  // import { createPromptParsedAllowFromForAccount } from "openclaw/plugin-sdk/setup";
};
```

---

## 6. Optional channel setup surface (for optional/installable channels)

```typescript
import { createOptionalChannelSetupSurface } from "openclaw/plugin-sdk/channel-setup";

const { setupAdapter, setupWizard } = createOptionalChannelSetupSurface({
  channel: "my-channel",
  label: "My Channel",
  npmSpec: "@myorg/openclaw-my-channel",
  docsPath: "/channels/my-channel",
});
```

---

## 7. openclaw.yml for channel

```yaml
channels:
  my-channel:
    enabled: true
    token: "bot-token-here"
    allowFrom:
      - "user-id-1"
      - "user-id-2"
    accounts:
      secondary:
        token: "another-token"

plugins:
  entries:
    my-channel:
      enabled: true
```

---

## ChannelPlugin shape summary

| Section | Purpose |
|---|---|
| `meta` | Docs, labels, picker metadata |
| `capabilities` | replies, polls, reactions, threads, media, chat types |
| `config` / `configSchema` | Account resolution and config parsing |
| `setup` / `setupWizard` | Onboarding / setup flow |
| `security` | DM policy and allowlist behavior |
| `messaging` | Target parsing and outbound session routing |
| `actions` | Shared `message` tool discovery and execution |
| `pairing` | DM approval flows |
| `threading` | Thread support |
| `status` | Connection status |
| `lifecycle` | connect / disconnect |
| `groups` | Group channel support |
| `directory` | User directory |

---

## Conflict debugging

```bash
# Find conflicting plugins
openclaw plugins list --enabled --verbose

# Inspect each suspected plugin
openclaw plugins inspect <id> --json
# Compare channels, channelConfigs, tools, diagnostics

# Refresh registry
openclaw plugins registry --refresh

# Fix stale entries
openclaw doctor --fix

# Restart after any changes
openclaw gateway restart
```
