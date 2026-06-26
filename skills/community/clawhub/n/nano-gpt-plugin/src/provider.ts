import { defineSingleProviderPluginEntry } from "openclaw/plugin-sdk/provider-entry";
import type { ModelProviderConfig } from "openclaw/plugin-sdk/provider-models";
import { fetchDynamicCatalog } from "./catalog";

// ---------------------------------------------------------------------------
// Hardcoded catalog — Phase 1 static baseline
// These models are representative of what NanoGPT actually serves.
// Phase 2 will replace this with a dynamic fetch from /api/v1/models.
// ---------------------------------------------------------------------------
const STATIC_MODELS: ModelProviderConfig["models"] = [
  {
    id: "nano-gpt/openai/gpt-5.2",
    name: "GPT-5.2 (via NanoGPT)",
    reasoning: false,
    input: ["text", "image"] as ("text" | "image")[],
    cost: { input: 1.25, output: 10, cacheRead: 0, cacheWrite: 0 },
    contextWindow: 128_000,
    maxTokens: 32_768,
    compat: { supportsUsageInStreaming: true },
  },
  {
    id: "nano-gpt/anthropic/claude-opus-4.6",
    name: "Claude Opus 4.6 (via NanoGPT)",
    reasoning: true,
    input: ["text", "image"] as ("text" | "image")[],
    cost: { input: 6, output: 30, cacheRead: 0, cacheWrite: 0 },
    contextWindow: 200_000,
    maxTokens: 32_768,
    compat: { supportsUsageInStreaming: true },
  },
];

// ---------------------------------------------------------------------------
// Exported for unit testing — call these directly without booting OpenClaw
// ---------------------------------------------------------------------------

/** Phase 1 static catalog builder */
export function buildProvider(): ModelProviderConfig {
  return {
    api: "openai-completions",
    baseUrl: "https://nano-gpt.com/api/v1",
    models: STATIC_MODELS,
  };
}

/** Phase 3 dynamic model resolution */
export function resolveDynamicModel(ctx: { modelId: string }) {
  const modelId = ctx.modelId.replace(/^nano-gpt\//, "");
  return {
    id: ctx.modelId,
    name: modelId,
    provider: "nano-gpt",
    api: "openai-completions" as const,
    baseUrl: "https://nano-gpt.com/api/v1",
    reasoning: false,
    input: ["text"] as ("text" | "image")[],
    cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
    contextWindow: 128_000,
    maxTokens: 8_192,
    compat: { supportsUsageInStreaming: true },
  };
}

/** Phase 4 usage auth — resolves API key from config/env */
export async function resolveUsageAuth(ctx: {
  resolveApiKeyFromConfigAndStore: (params: { providerIds: string[] }) => string | undefined;
}): Promise<{ token: string } | null> {
  const apiKey = ctx.resolveApiKeyFromConfigAndStore({ providerIds: ["nano-gpt"] });
  return apiKey ? { token: apiKey } : null;
}

/** Phase 4 usage snapshot — fetches daily tokens used + account balance */
export async function fetchUsageSnapshot(ctx: {
  token: string;
  timeoutMs?: number;
  fetchFn?: typeof fetch;
}): Promise<{
  period: "daily" | "monthly";
  used: number;
  limit: number;
  balanceUsd: number;
}> {
  const { token = "", timeoutMs = 10_000, fetchFn = globalThis.fetch } = ctx;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const [usageRes, balanceRes] = await Promise.all([
      fetchFn("https://nano-gpt.com/api/subscription/v1/usage", {
        headers: { Authorization: `Bearer ${token}` },
        signal: controller.signal,
      }),
      fetchFn("https://nano-gpt.com/api/check-balance", {
        headers: { Authorization: `Bearer ${token}` },
        signal: controller.signal,
      }),
    ]);

    clearTimeout(timer);

    if (!usageRes.ok) throw new Error(`Usage API ${usageRes.status}`);
    if (!balanceRes.ok) throw new Error(`Balance API ${balanceRes.status}`);

    const usageData = (await usageRes.json()) as {
      dailyInputTokens?: { used: number; limit: number };
      weeklyInputTokens?: { used: number; limit: number };
    };
    const balanceData = (await balanceRes.json()) as { balance: number };

    const daily = usageData.dailyInputTokens;
    const period: "daily" | "monthly" = daily ? "daily" : "monthly";
    const used = daily?.used ?? usageData.weeklyInputTokens?.used ?? 0;
    const limit = daily?.limit ?? usageData.weeklyInputTokens?.limit ?? 0;

    return {
      period,
      used,
      limit,
      balanceUsd: balanceData.balance ?? 0,
    };
  } catch (err) {
    clearTimeout(timer);
    throw err;
  }
}

/** Phase 2 dynamic catalog builder */
export async function buildProviderWithDiscovery(ctx?: {
  apiKey?: string;
}): Promise<ModelProviderConfig> {
  const apiKey = ctx?.apiKey;
  if (!apiKey) {
    return buildProvider();
  }
  try {
    const dynamic = await fetchDynamicCatalog({
      resolveProviderApiKey: () => ({ apiKey }),
    } as any);
    if (dynamic) return dynamic;
  } catch (e) {
    console.warn("Failed to fetch dynamic NanoGPT catalog, falling back to static:", e);
  }
  return buildProvider();
}

/** Prepare extra params for requests — adds stream_options with include_usage for token tracking */
export function prepareExtraParams(ctx: { extraParams?: Record<string, unknown> }) {
  const input = ctx.extraParams || {};
  return { ...input, stream_options: { include_usage: true } };
}

// ---------------------------------------------------------------------------
// Plugin entry — wires the above into OpenClaw's plugin system
// ---------------------------------------------------------------------------
const plugin = defineSingleProviderPluginEntry({
  id: "nano-gpt",
  name: "NanoGPT",
  description:
    "NanoGPT provider plugin — dynamic model catalog, usage tracking, and balance checking via nano-gpt.com",

  provider: {
    label: "NanoGPT",
    docsPath: "/providers/nano-gpt",

      auth: [
        {
          methodId: "api-key",
          label: "NanoGPT API key",
          hint: "API key from your nano-gpt.com dashboard",
          optionKey: "nanoGptApiKey",
          flagName: "--nano-gpt-api-key",
          envVar: "NANOGPT_API_KEY",
          promptMessage: "Enter your NanoGPT API key",
        },
      ],

    catalog: {
      buildProvider: buildProviderWithDiscovery,
    },

    resolveDynamicModel,
    prepareExtraParams,
    wrapStreamFn: (ctx) => {
      if (!ctx.streamFn) return undefined;
      const inner = ctx.streamFn;
      return (model, context, options) => {
        const originalOnPayload = options?.onPayload;
        return inner(model, context, {
          ...options,
          onPayload: (payload) => {
            if (payload && typeof payload === "object" && !Array.isArray(payload)) {
              const p = payload as Record<string, unknown>;
              if (!p.stream_options) {
                p.stream_options = { include_usage: true };
              }
            }
            return originalOnPayload?.(payload, model);
          },
        });
      };
    },
  },
});

export default plugin;

