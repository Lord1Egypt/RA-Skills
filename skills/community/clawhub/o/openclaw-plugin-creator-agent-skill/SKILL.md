---
name: openclaw-plugin-creator-skill
description: Build OpenClaw plugins from scratch — including the manifest, entry point, tool registration, channel plugins, provider plugins, config schema, setup wizards, runtime helpers, and publishing steps. Use this skill whenever the user wants to create, extend, debug, or publish any OpenClaw plugin, skill, or hook.
version: 1.0.0
homepage: https://github.com/pathanaawej0-dot/openclaw-plugin-creation-skill
metadata:
  clawdbot: true
---

# OpenClaw Plugin Development — Expert Reference

## 🛡️ Security, Privacy & Trust
This skill is purely instructional and does not execute remote code, access external endpoints (other than documentation), or modify system files without explicit user direction. All generated code should be reviewed before execution.
- **Data Privacy:** This skill does not collect or transmit user data.
- **External Calls:** No hidden background network requests.
- **Trust Statement:** This skill follows OpenClaw's security best practices for plugin development.

## What can a plugin do?

Plugins run **in-process with the Gateway** (via `jiti`, TypeScript loaded at runtime). They extend OpenClaw with:

| Capability | Registration method |
|---|---|
| Messaging channel | `api.registerChannel(...)` |
| LLM / model provider | `api.registerProvider(...)` |
| Agent tool (LLM-callable) | `api.registerTool(tool, opts?)` |
| Text-to-speech / STT | `api.registerSpeechProvider(...)` |
| Image generation | `api.registerImageGenerationProvider(...)` |
| Media understanding | `api.registerMediaUnderstandingProvider(...)` |
| Web search | `api.registerWebSearchProvider(...)` |
| Custom CLI command | `api.registerCommand(def)` |
| Event hook | `api.registerHook(events, handler, opts?)` |
| Gateway HTTP route | `api.registerHttpRoute(params)` |
| Gateway RPC method | `api.registerGatewayMethod(name, handler)` |
| CLI subcommand | `api.registerCli(registrar, opts?)` |
| Background service | `api.registerService(service)` |
| Interactive handler | `api.registerInteractiveHandler(registration)` |
| Context engine (exclusive) | `api.registerContextEngine(id, factory)` |
| Memory prompt section | `api.registerMemoryPromptSection(builder)` |

> Treat plugins as trusted code — they run with full Gateway access.

---

## Plugin formats

| Format | How it works |
|---|---|
| **Native** | `openclaw.plugin.json` + TypeScript module — official plugins, npm packages |
| **Bundle** | Codex/Claude/Cursor-compatible layout (`.codex-plugin/`, `.claude-plugin/`, `.cursor-plugin/`) |

This skill covers **native plugins**. For bundles see the Bundles docs.

---

## Step 1 — File structure

```
my-plugin/
├── openclaw.plugin.json   ← REQUIRED manifest
├── package.json           ← npm package + openclaw metadata
├── index.ts               ← main entry point
├── setup-entry.ts         ← lightweight setup-only entry (optional, channels)
└── src/
    ├── channel.ts         ← channel plugin object (if channel plugin)
    ├── runtime.ts         ← createPluginRuntimeStore (if needed)
    ├── tools.ts
    └── provider.test.ts
```

Internal barrel convention:
```
api.ts          ← public exports for external consumers
runtime-api.ts  ← internal-only runtime exports
```
Never import your own plugin through `openclaw/plugin-sdk/<your-plugin>`. Route internal imports through `./api.ts`.

---

## Step 2 — package.json

**Tool / provider plugin:**
```json
{
  "name": "@myorg/openclaw-my-plugin",
  "version": "1.0.0",
  "type": "module",
  "openclaw": {
    "extensions": ["./index.ts"],
    "providers": ["my-provider"]
  }
}
```

**Channel plugin:**
```json
{
  "name": "@myorg/openclaw-my-channel",
  "version": "1.0.0",
  "type": "module",
  "openclaw": {
    "extensions": ["./index.ts"],
    "setupEntry": "./setup-entry.ts",
    "channel": {
      "id": "my-channel",
      "label": "My Channel",
      "blurb": "Short description shown in onboarding."
    },
    "startup": {
      "deferConfiguredChannelFullLoadUntilAfterListen": true
    }
  }
}
```

`openclaw` field reference:

| Field | Type | Description |
|---|---|---|
| `extensions` | `string[]` | Entry point files (relative paths) |
| `setupEntry` | `string` | Lightweight setup-only entry (optional) |
| `channel` | `object` | Channel metadata: `id`, `label`, `blurb`, `selectionLabel`, `docsPath`, `order`, `aliases` |
| `providers` | `string[]` | Provider ids registered by this plugin |
| `install` | `object` | Install hints: `npmSpec`, `localPath`, `defaultChoice` |
| `startup` | `object` | Startup behavior flags |

---

## Step 3 — openclaw.plugin.json (Manifest)

> Every native plugin MUST have this file. OpenClaw validates config from it WITHOUT executing plugin code.

**Minimal (no config):**
```json
{
  "id": "my-plugin",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

**Full example (provider with auth):**
```json
{
  "id": "my-provider",
  "name": "My Provider",
  "description": "Adds My Provider LLM to OpenClaw",
  "version": "1.0.0",
  "providers": ["my-provider"],
  "providerAuthEnvVars": {
    "my-provider": ["MY_PROVIDER_API_KEY"]
  },
  "providerAuthChoices": [
    {
      "provider": "my-provider",
      "method": "api-key",
      "choiceId": "my-provider-api-key",
      "choiceLabel": "My Provider API key",
      "optionKey": "myProviderApiKey",
      "cliFlag": "--my-provider-api-key",
      "cliOption": "--my-provider-api-key <key>",
      "cliDescription": "My Provider API key",
      "onboardingScopes": ["text-inference"]
    }
  ],
  "uiHints": {
    "apiKey": {
      "label": "API Key",
      "placeholder": "sk-...",
      "sensitive": true,
      "help": "From your My Provider dashboard"
    }
  },
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "apiKey": { "type": "string" }
    },
    "required": ["apiKey"]
  }
}
```

**Full manifest field reference** → see `references/manifest.md`

---

## Step 4 — Entry Points

### Import rules (CRITICAL)
```typescript
// ✅ ALWAYS use focused subpaths
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { defineChannelPluginEntry } from "openclaw/plugin-sdk/core";
import { createPluginRuntimeStore } from "openclaw/plugin-sdk/runtime-store";

// ❌ NEVER use monolithic root (deprecated, will be removed)
import { ... } from "openclaw/plugin-sdk";
```

Full subpath reference → see `references/sdk-subpaths.md`

### Tool / Hook / Provider plugin (definePluginEntry)
```typescript
import { definePluginEntry, type OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";
import { Type } from "@sinclair/typebox";

export default definePluginEntry({
  id: "my-plugin",
  name: "My Plugin",
  description: "Human-readable description",

  register(api: OpenClawPluginApi) {
    // Access plugin config (from plugins.entries.my-plugin.config)
    const config = api.pluginConfig as { apiKey: string };

    // Required tool — always available to LLM
    api.registerTool({
      name: "my_tool",                      // must not clash with core tools
      description: "Does something useful",
      parameters: Type.Object({
        input: Type.String({ description: "The input" }),
        count: Type.Optional(Type.Number()),
      }),
      async execute(_callId, params) {
        return {
          content: [{ type: "text", text: `Result: ${params.input}` }],
        };
      },
    });

    // Optional tool — user must add to tools.allow
    api.registerTool(
      {
        name: "advanced_tool",
        description: "Side-effect tool (opt-in)",
        parameters: Type.Object({ pipeline: Type.String() }),
        async execute(_callId, params) {
          return { content: [{ type: "text", text: params.pipeline }] };
        },
      },
      { optional: true },
    );

    // Command — runs without going through LLM
    api.registerCommand({
      name: "my-plugin-status",
      description: "Show plugin status",
      handler: async () => ({ text: "Plugin is running" }),
    });

    // Event hook
    api.registerHook(["message.received"], async (event) => {
      api.logger.info(`Received message: ${event.type}`);
    });
  },
});
```

### Channel plugin (defineChannelPluginEntry)
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

  // registerFull: only for tools/routes that should NOT load in setup-only mode
  registerFull(api) {
    api.registerTool({
      name: "my_channel_status",
      description: "Check channel connection",
      parameters: { type: "object", properties: {} },
      async execute() {
        return { content: [{ type: "text", text: "connected" }] };
      },
    });
  },
});
```

### Setup entry (channels only)
```typescript
// setup-entry.ts — lightweight, no heavy imports
import { defineSetupPluginEntry } from "openclaw/plugin-sdk/core";
import { channelPlugin } from "./src/channel.js";

export default defineSetupPluginEntry(channelPlugin);
```

**When OpenClaw uses setupEntry:** channel is disabled/unconfigured, or deferred loading is on.
**Must include:** channel registration, HTTP routes needed before listen, gateway methods for startup.
**Must NOT include:** CLI registrations, background services, heavy runtime imports.

### One plugin, many capabilities
```typescript
export default definePluginEntry({
  id: "my-hybrid",
  name: "My Hybrid Plugin",
  register(api) {
    api.registerProvider({ id: "my-provider", /* ... */ });
    api.registerSpeechProvider({ id: "my-speech", /* ... */ });
    api.registerTool({ name: "my_tool", /* ... */ });
    api.registerCommand({ name: "my-cmd", /* ... */ });
  },
});
```

---

## Step 5 — Runtime helpers (api.runtime)

```typescript
// Read/write config
const cfg = api.runtime.config.loadConfig();
await api.runtime.config.writeConfigFile({ ...cfg, talk: { enabled: true } });

// TTS (telephony)
const result = await api.runtime.tts.textToSpeechTelephony({
  text: "Hello from OpenClaw",
  cfg: api.config,
});
// Returns PCM audio buffer + sample rate. Edge TTS NOT supported for telephony.

// List voices
const voices = await api.runtime.tts.listVoices({ provider: "openai", cfg });

// Web search
const results = await api.runtime.webSearch.search({ query: "...", maxResults: 5 });

// Spawn subagent
const session = await api.runtime.subagent.spawn({ /* ... */ });
```

Full runtime namespace reference → see `references/runtime.md`

### createPluginRuntimeStore
For shared mutable state across module imports (the correct pattern):
```typescript
import { createPluginRuntimeStore } from "openclaw/plugin-sdk/runtime-store";

const runtimeStore = createPluginRuntimeStore<{
  client: MyPlatformClient;
  logger: Logger;
}>("My Channel runtime not initialized");

export const setMyRuntime = (rt: { client: MyPlatformClient; logger: Logger }) =>
  runtimeStore.setRuntime(rt);
export const getMyRuntime = () => runtimeStore.getRuntime();
// Also: tryGetRuntime(), clearRuntime()
```

---

## Step 6 — openclaw.yml config

```yaml
plugins:
  enabled: true
  allow:
    - my-plugin
  deny: []
  load:
    paths:
      - ~/Projects/my-plugin   # for dev/local plugins
  entries:
    my-plugin:
      enabled: true
      config:
        apiKey: "sk-..."
        timeout: 60

# Enable optional tools
tools:
  allow:
    - advanced_tool      # specific tool
    - my-plugin          # all tools from plugin

# Plugin slots (exclusive categories)
plugins:
  slots:
    memory: memory-lancedb       # or "memory-core" or "none"
    contextEngine: my-engine     # or "legacy"

# Channel config (for channel plugins)
channels:
  my-channel:
    enabled: true
    token: "bot-token"
    allowFrom:
      - "user-id-1"
```

---

## Step 7 — Discovery precedence (first match wins)

1. `plugins.load.paths` — explicit paths in config
2. `<workspace>/.openclaw/<plugin-root>/` — workspace-local (**disabled by default**, must explicitly enable)
3. `~/.openclaw/<plugin-root>/` — global user extensions
4. Bundled plugins — shipped with OpenClaw (many enabled by default)

**Conflict rule:** If multiple plugins try to own the same channel/tool id, first match wins, others are skipped with a warning.

---

## Step 8 — CLI commands

```bash
# Discovery
openclaw plugins list
openclaw plugins list --enabled --verbose
openclaw plugins list --json
openclaw plugins inspect <id>
openclaw plugins inspect <id> --json
openclaw plugins doctor

# Install
openclaw plugins install @myorg/my-plugin          # ClawHub first, npm fallback
openclaw plugins install clawhub:@myorg/my-plugin  # ClawHub only
openclaw plugins install ./my-plugin               # local path
openclaw plugins install -l ./my-plugin            # link (dev, no copy)
openclaw plugins install <spec> --force            # overwrite existing
openclaw plugins install <spec> --pin              # record exact npm spec
openclaw plugins install <spec> --marketplace https://github.com/<owner>/<repo>

# Manage
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw plugins update <id>
openclaw plugins update --all
openclaw plugins uninstall <id>
openclaw plugins uninstall <id> --keep-files
openclaw plugins registry --refresh               # refresh metadata after changes

# Fix
openclaw doctor --fix                             # auto-remove stale entries
openclaw gateway restart                          # REQUIRED after any plugin change
```

---

## Step 9 — Testing

```bash
# Run plugin tests (vitest)
pnpm test -- extensions/my-plugin/

# With coverage
pnpm test:coverage

# Scoped
pnpm test -- extensions/my-plugin/src/channel.test.ts -t "resolves account"

# Low-memory mode
OPENCLAW_TEST_PROFILE=low OPENCLAW_TEST_SERIAL_GATEWAY=1 pnpm test
```

Full testing patterns → see `references/testing.md`

---

## Security rules (MUST follow)

- Dependencies installed with `npm install --ignore-scripts` — **no lifecycle scripts**
- Keep deps "pure JS/TS" — avoid packages with postinstall builds
- Plugin entries must resolve **inside** the plugin directory (symlink escapes are rejected)
- Non-bundled plugins without `plugins.allow` entry emit a startup warning
- `plugins.deny` always wins over `plugins.allow`
- Use `optional: true` for tools with side effects or extra binary requirements
- Treat all plugin code as trusted — review before installing from unknown sources

---

## Pre-submission checklist

- [ ] `package.json` has `"type": "module"` and correct `openclaw.extensions`
- [ ] `openclaw.plugin.json` present with valid `id` and `configSchema` (even if empty)
- [ ] Entry uses `definePluginEntry` (tools/providers) or `defineChannelPluginEntry` (channels)
- [ ] All imports use `openclaw/plugin-sdk/<subpath>` — never the root barrel
- [ ] Internal imports go through `./api.ts` or `./runtime-api.ts`, not SDK self-imports
- [ ] No `scripts` in dependency packages (security)
- [ ] Optional tools marked `{ optional: true }`
- [ ] `uiHints.sensitive: true` on any API key / secret config fields
- [ ] Gateway restarted: `openclaw gateway restart`
- [ ] Tests pass: `pnpm test -- extensions/my-plugin/`

---

## Publishing

```bash
# Publish to npm (ClawHub auto-indexes npm)
npm publish --access public

# Users install with:
openclaw plugins install @myorg/my-plugin
# OpenClaw tries ClawHub first, npm fallback automatically
```

---

## Reference files (read when needed)

- `references/manifest.md` — complete openclaw.plugin.json field reference
- `references/sdk-subpaths.md` — all 100+ SDK import subpaths grouped by purpose
- `references/channel-plugin.md` — full channel plugin walkthrough (ChannelPlugin shape, pairing, actions, setup wizard)
- `references/provider-plugin.md` — full provider plugin (all 22 hooks, auth, catalog, dynamic models, multi-capability)
- `references/runtime.md` — all api.runtime namespaces with examples
- `references/testing.md` — unit testing patterns, mocking, contract tests
