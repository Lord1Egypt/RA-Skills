# OpenClaw Provider Plugin SDK

Source: https://github.com/openclaw/openclaw/blob/main/docs/plugins/sdk-provider-plugins.md

## Package Structure
```
extensions/<plugin-name>/
├── package.json          # openclaw.providers metadata
├── openclaw.plugin.json  # Manifest
├── index.ts              # definePluginEntry / defineSingleProviderPluginEntry
└── src/
    ├── provider.test.ts
    └── usage.ts          # (optional) usage endpoint
```

## package.json
```json
{
  "name": "@myorg/openclaw-nano-gpt",
  "version": "1.0.0",
  "type": "module",
  "openclaw": {
    "extensions": ["./index.ts"],
    "providers": ["nano-gpt"]
  }
}
```

## openclaw.plugin.json (Manifest)
```json
{
  "id": "nano-gpt",
  "name": "NanoGPT",
  "description": "NanoGPT model provider — access to 50+ models via nano-gpt.com",
  "providers": ["nano-gpt"],
  "providerAuthEnvVars": {
    "nano-gpt": ["NANOGPT_API_KEY"]
  },
  "providerAuthChoices": [
    {
      "provider": "nano-gpt",
      "method": "api-key",
      "choiceId": "nano-gpt-api-key",
      "choiceLabel": "NanoGPT API key",
      "groupId": "nano-gpt",
      "groupLabel": "NanoGPT",
      "cliFlag": "--nano-gpt-api-key",
      "cliOption": "--nano-gpt-api-key <key>",
      "cliDescription": "NanoGPT API key"
    }
  ],
  "configSchema": {
    "type": "object",
    "additionalProperties": false
  }
}
```

## Minimal Provider (defineSingleProviderPluginEntry)
```typescript
import { defineSingleProviderPluginEntry } from "openclaw/plugin-sdk/provider-entry";

export default defineSingleProviderPluginEntry({
  id: "nano-gpt",
  name: "NanoGPT",
  description: "NanoGPT model provider",
  provider: {
    label: "NanoGPT",
    docsPath: "/providers/nano-gpt",
    auth: [
      {
        methodId: "api-key",
        label: "NanoGPT API key",
        hint: "API key from nano-gpt.com/api",
        optionKey: "nanoGptApiKey",
        flagName: "--nano-gpt-api-key",
        envVar: "NANOGPT_API_KEY",
        promptMessage: "Enter your NanoGPT API key",
        defaultModel: "nano-gpt/anthropic/claude-opus-4.6",
      },
    ],
    catalog: {
      buildProvider: () => ({
        api: "openai-completions",
        baseUrl: "https://nano-gpt.com/api/v1",
        models: [{ id: "anthropic/claude-opus-4.6", name: "Claude Opus 4.6" }],
      }),
    },
  },
});
```

## Dynamic Model Resolution (key for nano-gpt)
Since nano-gpt has 50+ models that change over time, use `resolveDynamicModel`:
```typescript
resolveDynamicModel: (ctx) => ({
  id: ctx.modelId,           // e.g., "anthropic/claude-opus-4.6"
  name: ctx.modelId,
  provider: "nano-gpt",
  api: "openai-completions",
  baseUrl: "https://nano-gpt.com/api/v1",
  reasoning: false,
  input: ["text"],
  cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },  // unknown statically
  contextWindow: 128000,      // unknown statically
  maxTokens: 8192,            // unknown statically
}),
```

## Async Model Catalog (fetches from nano-gpt API)
```typescript
catalog: {
  order: "simple",
  run: async (ctx) => {
    const apiKey = ctx.resolveProviderApiKey("nano-gpt").apiKey;
    if (!apiKey) return null;

    const res = await fetch(`https://nano-gpt.com/api/v1/models?detailed=true`, {
      headers: { Authorization: `Bearer ${apiKey}` },
    });
    const data = await res.json();

    return {
      provider: {
        baseUrl: "https://nano-gpt.com/api/v1",
        apiKey,
        api: "openai-completions",
        models: data.data.map((m: any) => ({
          id: m.id,
          name: m.name ?? m.id,
          reasoning: m.capabilities?.reasoning ?? false,
          input: m.capabilities?.vision ? ["text", "image"] : ["text"],
          cost: {
            input: m.pricing?.prompt ?? 0,
            output: m.pricing?.completion ?? 0,
            cacheRead: 0,
            cacheWrite: 0,
          },
          contextWindow: m.context_length ?? 128000,
          maxTokens: m.max_output_tokens ?? 8192,
        })),
      },
    };
  },
},
```

## Usage Tracking Hooks
```typescript
resolveUsageAuth: async (ctx) => {
  const apiKey = ctx.resolveProviderApiKey("nano-gpt").apiKey;
  return apiKey ? { token: apiKey } : null;
},

fetchUsageSnapshot: async (ctx) => {
  const res = await fetch("https://nano-gpt.com/api/subscription/v1/usage", {
    headers: { Authorization: `Bearer ${ctx.token}` },
  });
  const data = await res.json();
  return {
    used: data.daily?.used ?? 0,
    limit: data.limits?.daily ?? 0,
    remaining: data.daily?.remaining ?? 0,
    resetAt: data.daily?.resetAt ? new Date(data.daily.resetAt) : undefined,
    periodEnd: data.period?.currentPeriodEnd
      ? new Date(data.period.currentPeriodEnd)
      : undefined,
  };
},
```

## Provider Hooks Reference (in call order)
| # | Hook | When to use |
|---|---|---|
| 1 | `catalog` | Model catalog + base URL defaults |
| 2 | `resolveDynamicModel` | Accept arbitrary upstream model IDs |
| 3 | `prepareDynamicModel` | Async metadata fetch before resolving |
| 4 | `normalizeResolvedModel` | Transport rewrites before runner |
| 5 | `capabilities` | Transcript/tooling metadata |
| 6 | `prepareExtraParams` | Default request params |
| 7 | `wrapStreamFn` | Custom headers/body wrappers |
| 8 | `formatApiKey` | Custom runtime token shape |
| 9 | `refreshOAuth` | Custom OAuth refresh |
| 10 | `buildAuthDoctorHint` | Auth repair guidance |
| 11 | `isCacheTtlEligible` | Prompt cache TTL gating |
| 12 | `buildMissingAuthMessage` | Custom missing-auth hint |
| 13 | `suppressBuiltInModel` | Hide stale upstream rows |
| 14 | `augmentModelCatalog` | Synthetic forward-compat rows |
| 15 | `isBinaryThinking` | Binary thinking on/off |
| 16 | `supportsXHighThinking` | `xhigh` reasoning support |
| 17 | `resolveDefaultThinkingLevel` | Default `/think` policy |
| 18 | `isModernModelRef` | Live/smoke model matching |
| 19 | `prepareRuntimeAuth` | Token exchange before inference |
| 20 | `resolveUsageAuth` | Custom usage credential parsing |
| 21 | `fetchUsageSnapshot` | Custom usage endpoint |
| 22 | `onModelSelected` | Post-selection callback |
