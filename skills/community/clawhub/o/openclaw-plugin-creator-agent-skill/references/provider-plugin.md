# Provider Plugin — Complete Guide (All 22 Hooks)

---

## File structure

```
extensions/my-provider/
├── package.json
├── openclaw.plugin.json
├── index.ts
└── src/
    ├── provider.ts
    ├── usage.ts           (optional)
    └── provider.test.ts
```

---

## 1. package.json

```json
{
  "name": "@myorg/openclaw-acme-ai",
  "version": "1.0.0",
  "type": "module",
  "openclaw": {
    "extensions": ["./index.ts"],
    "providers": ["acme-ai"]
  }
}
```

---

## 2. openclaw.plugin.json

```json
{
  "id": "acme-ai",
  "name": "Acme AI",
  "description": "Acme AI model provider",
  "version": "1.0.0",
  "providers": ["acme-ai"],
  "providerAuthEnvVars": {
    "acme-ai": ["ACME_AI_API_KEY"]
  },
  "providerAuthChoices": [
    {
      "provider": "acme-ai",
      "method": "api-key",
      "choiceId": "acme-ai-api-key",
      "choiceLabel": "Acme AI API key",
      "optionKey": "acmeAiApiKey",
      "cliFlag": "--acme-ai-api-key",
      "cliOption": "--acme-ai-api-key <key>",
      "cliDescription": "Acme AI API key",
      "onboardingScopes": ["text-inference"]
    }
  ],
  "uiHints": {
    "apiKey": { "label": "API key", "placeholder": "sk-...", "sensitive": true }
  },
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "apiKey": { "type": "string" }
    }
  }
}
```

---

## 3. index.ts — Full provider plugin

```typescript
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { createProviderApiKeyAuthMethod } from "openclaw/plugin-sdk/provider-auth";

export default definePluginEntry({
  id: "acme-ai",
  name: "Acme AI",
  description: "Acme AI model provider",

  register(api) {
    api.registerProvider({
      id: "acme-ai",
      label: "Acme AI",
      docsPath: "/providers/acme-ai",
      envVars: ["ACME_AI_API_KEY"],

      // --- AUTH ---
      auth: [
        createProviderApiKeyAuthMethod({
          providerId: "acme-ai",
          methodId: "api-key",
          label: "Acme AI API key",
          hint: "API key from your Acme AI dashboard",
          optionKey: "acmeAiApiKey",
          flagName: "--acme-ai-api-key",
          envVar: "ACME_AI_API_KEY",
          promptMessage: "Enter your Acme AI API key",
          defaultModel: "acme-ai/acme-large",
        }),
      ],

      // --- CATALOG (Hook 1) ---
      catalog: {
        order: "simple",    // "simple" | "profile" | "paired" | "late"
        run: async (ctx) => {
          const { apiKey } = ctx.resolveProviderApiKey("acme-ai");
          if (!apiKey) return null;
          return {
            provider: {
              baseUrl: "https://api.acme-ai.com/v1",
              apiKey,
              api: "openai-completions",   // or "anthropic", "google", custom
              models: [
                {
                  id: "acme-large",
                  name: "Acme Large",
                  reasoning: true,
                  input: ["text", "image"],
                  cost: { input: 3, output: 15, cacheRead: 0.3, cacheWrite: 3.75 },
                  contextWindow: 200000,
                  maxTokens: 32768,
                },
                {
                  id: "acme-small",
                  name: "Acme Small",
                  reasoning: false,
                  input: ["text"],
                  cost: { input: 1, output: 5, cacheRead: 0.1, cacheWrite: 1.25 },
                  contextWindow: 128000,
                  maxTokens: 8192,
                },
              ],
            },
          };
        },
      },

      // --- DYNAMIC MODELS (Hook 2) — for proxy/router providers ---
      resolveDynamicModel: (ctx) => ({
        id: ctx.modelId,
        name: ctx.modelId,
        provider: "acme-ai",
        api: "openai-completions",
        baseUrl: "https://api.acme-ai.com/v1",
        reasoning: false,
        input: ["text"],
        cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
        contextWindow: 128000,
        maxTokens: 8192,
      }),

      // --- ASYNC WARM-UP (Hook 3) — async metadata fetch before resolveDynamicModel ---
      prepareDynamicModel: async (ctx) => {
        // fetch metadata for ctx.modelId, then resolveDynamicModel runs again
      },

      // --- TRANSPORT REWRITE (Hook 4) ---
      normalizeResolvedModel: (ctx) => {
        // Rewrite model before passing to runner
        return ctx.model;
      },

      // --- CUSTOM REQUEST PARAMS (Hook 6) ---
      prepareExtraParams: (ctx) => ({
        temperature: 0.7,
        max_tokens: ctx.model.maxTokens,
      }),

      // --- CUSTOM HEADERS/BODY (Hook 7) ---
      wrapStreamFn: (ctx) => {
        if (!ctx.streamFn) return undefined;
        const inner = ctx.streamFn;
        return async (params) => {
          params.headers = {
            ...params.headers,
            "X-Acme-Version": "2",
            "X-Custom-Header": "value",
          };
          return inner(params);
        };
      },

      // --- TOKEN EXCHANGE (Hook 19) — async auth before each inference call ---
      prepareRuntimeAuth: async (ctx) => {
        const exchanged = await exchangeToken(ctx.apiKey);
        return {
          apiKey: exchanged.token,
          baseUrl: exchanged.baseUrl,
          expiresAt: exchanged.expiresAt,
        };
      },

      // --- USAGE (Hook 20-21) ---
      resolveUsageAuth: async (ctx) => {
        const auth = await ctx.resolveOAuthToken();
        return auth ? { token: auth.token } : null;
      },
      fetchUsageSnapshot: async (ctx) => {
        return await fetchAcmeUsage(ctx.token, ctx.timeoutMs);
      },
    });
  },
});
```

---

## All 22 provider hooks (in order)

| # | Hook | When to use |
|---|---|---|
| 1 | `catalog` | Model catalog or base URL defaults |
| 2 | `resolveDynamicModel` | Accept arbitrary upstream model IDs (proxy/router) |
| 3 | `prepareDynamicModel` | Async metadata fetch before resolving |
| 4 | `normalizeResolvedModel` | Transport rewrites before the runner |
| 5 | `capabilities` | Transcript/tooling metadata (data, not callable) |
| 6 | `prepareExtraParams` | Default request params |
| 7 | `wrapStreamFn` | Custom headers/body wrappers |
| 8 | `formatApiKey` | Custom runtime token shape |
| 9 | `refreshOAuth` | Custom OAuth refresh |
| 10 | `buildAuthDoctorHint` | Auth repair guidance shown in Doctor |
| 11 | `isCacheTtlEligible` | Prompt cache TTL gating |
| 12 | `buildMissingAuthMessage` | Custom missing-auth hint for users |
| 13 | `suppressBuiltInModel` | Hide stale upstream model rows |
| 14 | `augmentModelCatalog` | Synthetic forward-compat rows |
| 15 | `isBinaryThinking` | Binary thinking on/off |
| 16 | `supportsXHighThinking` | `xhigh` reasoning support |
| 17 | `resolveDefaultThinkingLevel` | Default `/think` policy |
| 18 | `isModernModelRef` | Live/smoke model matching |
| 19 | `prepareRuntimeAuth` | Token exchange before inference |
| 20 | `resolveUsageAuth` | Custom usage credential parsing |
| 21 | `fetchUsageSnapshot` | Custom usage/billing endpoint |
| 22 | `onModelSelected` | Post-selection callback (e.g. telemetry) |

**Most providers only need hooks 1-2 + 7 or 19.**

---

## Shorthand: defineSingleProviderPluginEntry

For simple single-provider API-key plugins:

```typescript
import { defineSingleProviderPluginEntry } from "openclaw/plugin-sdk/provider-entry";

export default defineSingleProviderPluginEntry({
  id: "acme-ai",
  name: "Acme AI",
  description: "Acme AI model provider",
  provider: {
    label: "Acme AI",
    docsPath: "/providers/acme-ai",
    auth: [{
      methodId: "api-key",
      label: "Acme AI API key",
      optionKey: "acmeAiApiKey",
      flagName: "--acme-ai-api-key",
      envVar: "ACME_AI_API_KEY",
      promptMessage: "Enter your Acme AI API key",
      defaultModel: "acme-ai/acme-large",
    }],
    catalog: {
      buildProvider: () => ({
        api: "openai-completions",
        baseUrl: "https://api.acme-ai.com/v1",
        models: [
          { id: "acme-large", name: "Acme Large" },
          { id: "acme-small", name: "Acme Small" },
        ],
      }),
    },
  },
});
```

---

## Catalog order reference

| Order | When it runs | Use case |
|---|---|---|
| `simple` | First pass | Plain API-key providers |
| `profile` | After simple | Providers gated on auth profiles |
| `paired` | After profile | Synthesize multiple related entries |
| `late` | Last pass | Override existing providers (wins on collision) |

---

## Multi-capability (hybrid) plugin

One plugin can own multiple provider types. Recommended pattern for vendor plugins:

```typescript
register(api) {
  // LLM
  api.registerProvider({ id: "acme-ai", /* ... */ });

  // TTS/STT
  api.registerSpeechProvider({
    id: "acme-ai",
    label: "Acme Speech",
    isConfigured: ({ config }) => Boolean(config.messages?.tts),
    synthesize: async (req) => ({
      audioBuffer: Buffer.from(/* PCM data */),
      outputFormat: "mp3",
      fileExtension: ".mp3",
      voiceCompatible: false,
    }),
  });

  // Image/audio/video understanding
  api.registerMediaUnderstandingProvider({
    id: "acme-ai",
    capabilities: ["image", "audio"],
    describeImage: async (req) => ({ text: "A photo of..." }),
    transcribeAudio: async (req) => ({ text: "Transcript..." }),
  });

  // Image generation
  api.registerImageGenerationProvider({
    id: "acme-ai",
    label: "Acme Images",
    generate: async (req) => ({ url: "https://..." }),
  });

  // Web search
  api.registerWebSearchProvider({
    id: "acme-ai",
    label: "Acme Search",
    search: async ({ query, maxResults }) => [
      { title: "Result", url: "https://...", snippet: "..." }
    ],
  });
}
```

---

## onboarding preset helpers (for model config patching)

```typescript
import { 
  createDefaultModelPresetAppliers,
  createDefaultModelsPresetAppliers,
  createModelCatalogPresetAppliers,
} from "openclaw/plugin-sdk/provider-onboard";
```
Use when auth flow needs to patch `models.providers.*`, aliases, and agent default model during onboarding.

---

## Tests

```typescript
import { describe, it, expect, vi } from "vitest";
import { acmeProvider } from "./src/provider.js";

describe("acme-ai provider", () => {
  it("resolves dynamic models", () => {
    const model = acmeProvider.resolveDynamicModel!({
      modelId: "acme-beta-v3",
    } as any);
    expect(model.id).toBe("acme-beta-v3");
    expect(model.provider).toBe("acme-ai");
  });

  it("returns catalog when key is available", async () => {
    const result = await acmeProvider.catalog!.run({
      resolveProviderApiKey: () => ({ apiKey: "test-key" }),
    } as any);
    expect(result?.provider?.models).toHaveLength(2);
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

## openclaw.yml for provider

```yaml
# After install + restart:
providers:
  default: acme-ai
  models:
    chat: acme-ai/acme-large
    fast: acme-ai/acme-small

# Provider auth (set during openclaw onboard --acme-ai-api-key <key>)
# or manually:
plugins:
  entries:
    acme-ai:
      enabled: true
      config:
        apiKey: "sk-..."
```
