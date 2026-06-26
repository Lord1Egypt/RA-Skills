/**
 * Dynamic catalog fetcher — Phase 2.
 *
 * Fetches the live model list from nano-gpt.com and maps each model to
 * OpenClaw's internal model schema.
 *
 * This module is imported by provider.ts but not yet wired as the catalog
 * source (static catalog is used until Phase 2 is explicitly activated).
 */

import type { ProviderCatalogContext } from "openclaw/plugin-sdk/provider-catalog";

// ---------------------------------------------------------------------------
// Types — mirror NanoGPT API response shapes
// ---------------------------------------------------------------------------

export interface NanoGPTUsageResponse {
  dailyInputTokens?: { used: number; limit: number };
  weeklyInputTokens?: { used: number; limit: number };
}

export interface NanoGPTBalanceResponse {
  balance: number;
}

// ---------------------------------------------------------------------------
// Model field mapper
// ---------------------------------------------------------------------------

/**
 * Maps a raw NanoGPT model object to OpenClaw's internal model representation.
 * Defensively handles null / missing fields with safe defaults.
 */
export function mapNanoModelToOpenClaw(raw: {
  id: string;
  name?: string;
  context_length?: number | null;
  max_output_tokens?: number | null;
  pricing?: { prompt?: number | null; completion?: number | null } | null;
  capabilities?: { vision?: boolean; reasoning?: boolean } | null;
}): {
  id: string;
  name: string;
  reasoning: boolean;
  input: ("text" | "image")[];
  cost: { input: number; output: number; cacheRead: number; cacheWrite: number };
  contextWindow: number;
  maxTokens: number;
  compat: { supportsUsageInStreaming: true };
} {
  // Pricing is in $/million tokens — convert to per-token cost
  const promptPrice = raw.pricing?.prompt ?? 0;
  const completionPrice = raw.pricing?.completion ?? 0;

  return {
    // Prepend "nano-gpt/" so the model ID is namespaced to this provider
    id: raw.id.startsWith("nano-gpt/") ? raw.id : `nano-gpt/${raw.id}`,
    name: raw.name ?? raw.id,
    reasoning: raw.capabilities?.reasoning ?? false,
    input: (raw.capabilities?.vision ? ["text", "image"] : ["text"]) as ("text" | "image")[],
    cost: {
      input: promptPrice / 1_000_000,
      output: completionPrice / 1_000_000,
      cacheRead: 0,
      cacheWrite: 0,
    },
    contextWindow: raw.context_length ?? 128_000,
    maxTokens: raw.max_output_tokens ?? 8_192,
    compat: { supportsUsageInStreaming: true },
  };
}

// ---------------------------------------------------------------------------
// Catalog fetcher
// ---------------------------------------------------------------------------

export interface DynamicCatalogResult {
  api: "openai-completions";
  baseUrl: string;
  models: ReturnType<typeof mapNanoModelToOpenClaw>[];
}

/**
 * Fetches the live model catalog from nano-gpt.com.
 *
 * Returns null if no API key is available (catalog is skipped gracefully).
 * Throws on network or HTTP errors so the caller can handle them explicitly.
 */
export async function fetchDynamicCatalog(
  ctx: ProviderCatalogContext & { signal?: AbortSignal }
): Promise<DynamicCatalogResult | null> {
  const { resolveProviderApiKey, signal } = ctx;
  const { apiKey } = await resolveProviderApiKey();

  if (!apiKey) return null;

  const response = await fetch(
    "https://nano-gpt.com/api/v1/models?detailed=true",
    {
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      signal,
    }
  );

  if (!response.ok) {
    throw new Error(`NanoGPT catalog fetch failed: ${response.status} ${response.statusText}`);
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const body = (await response.json()) as { models?: any[] };
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const models = (body.models ?? []).map((m) => mapNanoModelToOpenClaw(m as Parameters<typeof mapNanoModelToOpenClaw>[0]));

  return {
    api: "openai-completions",
    baseUrl: "https://nano-gpt.com/api/v1",
    models,
  };
}
