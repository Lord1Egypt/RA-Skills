/**
 * 🧠 Memoria — Configuration parser and provider factories
 * 
 * This module exports:
 *   - MemoriaConfig interface (typed config from openclaw.json)
 *   - parseConfig() — raw JSON → typed config with smart defaults
 *   - createEmbedProvider() — factory for embedding providers
 *   - createLLMProvider() — factory for LLM providers
 */

import { OllamaEmbed, OllamaLLM } from "./providers/ollama.js";
import { lmStudioLLM, lmStudioEmbed, openaiLLM, openaiEmbed, openrouterLLM, openrouterEmbed } from "./providers/openai-compat.js";
import type { EmbedProvider, LLMProvider } from "./providers/types.js";
import type { FallbackProviderConfig } from "./fallback.js";
import { AnthropicLLM } from "./providers/anthropic.js";

// ─── Config Interface ───

export interface MemoriaConfig {
  autoRecall: boolean;
  autoCapture: boolean;
  recallLimit: number;
  captureMaxFacts: number;
  defaultAgent: string;
  contextWindow: number;
  workspacePath: string;
  syncMd: boolean;
  fallback: FallbackProviderConfig[];
  /** Continuous Learning (Layer 21) config */
  continuous?: {
    /** Extract every N turns (default 4) */
    interval?: number;
    /** Cooldown between periodic extractions in ms (default 45000) */
    cooldownMs?: number;
    /** Enable/disable (default true when autoCapture is true) */
    enabled?: boolean;
  };
  embed: {
    provider: "ollama" | "lmstudio" | "openai" | "openrouter" | "anthropic";
    baseUrl?: string;
    model: string;
    dimensions: number;
    apiKey?: string;
  };
  llm: {
    provider: "ollama" | "lmstudio" | "openai" | "openrouter" | "anthropic";
    baseUrl?: string;
    model: string;
    apiKey?: string;
    /** Per-layer overrides: each key = layer name, value = provider config */
    overrides?: Partial<Record<MemoriaLayer, LayerLLMConfig>>;
  };
  lifecycle?: {
    freshDays?: number;
    settledMinAccess?: number;
    dormantAfterDays?: number;
    detailCursor?: number;
    revisionRecallThreshold?: number;
  };
  procedural?: {
    reflectEvery?: number;
    degradedThreshold?: number;
    defaultSafety?: number;
    staleDays?: number;
    docCheckDays?: number;
  };
  patterns?: any; // PatternManager config, loosely typed for now
  autoSkill?: {
    minSuccesses?: number;
    minQuality?: number;
    skillDir?: string;
    maxPerSession?: number;
  };
}

/** Named layers that accept a per-layer LLM override */
export type MemoriaLayer = "extract" | "contradiction" | "graph" | "topics" | "procedural";

export interface LayerLLMConfig {
  provider: "ollama" | "lmstudio" | "openai" | "openrouter" | "anthropic";
  baseUrl?: string;
  model: string;
  apiKey?: string;
}

// ─── Config Parser ───

/** Parse raw plugin config (from openclaw.json) into typed MemoriaConfig with smart defaults. */
export function parseConfig(raw: Record<string, unknown> | undefined): MemoriaConfig {
  const embed = (raw?.embed as Record<string, unknown>) || {};
  const llm = (raw?.llm as Record<string, unknown>) || {};
  return {
    autoRecall: raw?.autoRecall !== false,
    autoCapture: raw?.autoCapture !== false,
    recallLimit: (raw?.recallLimit as number) || 12,
    captureMaxFacts: (raw?.captureMaxFacts as number) || 8,
    defaultAgent: (raw?.defaultAgent as string) || "koda",
    contextWindow: (raw?.contextWindow as number) || 200000,
    workspacePath: (raw?.workspacePath as string) || process.env.HOME + "/.openclaw/workspace",
    syncMd: raw?.syncMd !== false,
    fallback: ((raw?.fallback as any[]) || []).map((f: any) => ({
      ...f,
      // Normalize: user config uses "provider", internal uses "type"
      type: f.type || f.provider || "ollama",
      name: f.name || f.provider || f.type || "ollama",
    })) as FallbackProviderConfig[],
    embed: {
      provider: (embed.provider as MemoriaConfig["embed"]["provider"]) || "ollama",
      baseUrl: embed.baseUrl as string | undefined,
      model: (embed.model as string) || "nomic-embed-text-v2-moe",
      dimensions: (embed.dimensions as number) || 768,
      apiKey: embed.apiKey as string | undefined,
    },
    llm: {
      provider: (llm.provider as MemoriaConfig["llm"]["provider"]) || "ollama",
      baseUrl: llm.baseUrl as string | undefined,
      model: (llm.model as string) || "gemma3:4b",
      apiKey: llm.apiKey as string | undefined,
      overrides: (llm.overrides as MemoriaConfig["llm"]["overrides"]) || undefined,
    },
  };
}

// ─── Provider Factories ───

/** Create an embedding provider from config. Used for the main embedder + fallback list. */
export function createEmbedProvider(cfg: MemoriaConfig["embed"]): EmbedProvider {
  switch (cfg.provider) {
    case "ollama":
      return new OllamaEmbed(cfg.baseUrl || "http://localhost:11434", cfg.model, cfg.dimensions);
    case "lmstudio":
      return lmStudioEmbed(cfg.model, cfg.dimensions, cfg.baseUrl || "http://localhost:1234/v1");
    case "openai":
      return openaiEmbed(cfg.model, cfg.apiKey || "", cfg.dimensions);
    case "openrouter":
      return openrouterEmbed(cfg.model, cfg.apiKey || "", cfg.dimensions);
    default:
      return new OllamaEmbed(); // safe default
  }
}

/** Create an LLM provider from config. Used for the main chain + per-layer overrides. */
export function createLLMProvider(cfg: MemoriaConfig["llm"]): LLMProvider {
  switch (cfg.provider) {
    case "ollama":
      return new OllamaLLM(cfg.baseUrl || "http://localhost:11434", cfg.model);
    case "lmstudio":
      return lmStudioLLM(cfg.model, cfg.baseUrl || "http://localhost:1234/v1");
    case "openai":
      return openaiLLM(cfg.model, cfg.apiKey || "");
    case "openrouter":
      return openrouterLLM(cfg.model, cfg.apiKey || "");
    case "anthropic":
      return new AnthropicLLM(cfg.model, cfg.apiKey || "", cfg.baseUrl);
    default:
      return new OllamaLLM(); // safe default
  }
}
