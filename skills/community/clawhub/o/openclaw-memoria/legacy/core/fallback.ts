/**
 * Memoria — Layer 12: Fallback Chain
 * 
 * Implements both LLMProvider and EmbedProvider interfaces.
 * Tries providers in order; first successful response wins.
 * If all fail → throws (callers wrap in try/catch for graceful degradation).
 * 
 * Default order (configurable via "fallback" in plugin config):
 *   1. Ollama gemma3:4b (local, 0€)
 *   2. OpenAI GPT-5.4-nano (cloud, ~$0.001)
 *   3. LM Studio GLM-4.7 (local, 0€)
 * 
 * Used by: every module that needs LLM (selective, graph, topics, observations,
 * clusters, procedural, revision, patterns). Modules receive the chain via constructor
 * and don't know/care about the fallback — they see a single LLMProvider.
 * 
 * @example
 * const chain = new FallbackChain([
 *   { type: "ollama", model: "gemma3:4b" },
 *   { type: "openai", model: "gpt-5.4-nano", apiKey: "..." }
 * ]);
 * const answer = await chain.generate("Extract entities..."); // tries Ollama first
 *   4. null → FTS-only / skip
 */

import type { LLMProvider, EmbedProvider, GenerateOptions, GenerateResult } from "./providers/types.js";
import { OllamaLLM, OllamaEmbed } from "./providers/ollama.js";
import {
  OpenAICompatLLM,
  OpenAICompatEmbed,
  lmStudioLLM,
  lmStudioEmbed,
} from "./providers/openai-compat.js";
import { AnthropicLLM } from "./providers/anthropic.js";

// ─── Config ───

export interface FallbackProviderConfig {
  name: string;
  type: "ollama" | "lmstudio" | "openai" | "openrouter" | "anthropic";
  model: string;
  baseUrl?: string;
  apiKey?: string;
  timeoutMs?: number;
  /** For embed providers */
  embedModel?: string;
  embedDimensions?: number;
}

export interface FallbackConfig {
  providers: FallbackProviderConfig[];
  /** Global timeout per provider attempt. Default 15000ms */
  defaultTimeoutMs: number;
}

export const DEFAULT_FALLBACK_CONFIG: FallbackConfig = {
  providers: [
    {
      name: "ollama",
      type: "ollama",
      model: "gemma3:4b",
      baseUrl: "http://localhost:11434",
      timeoutMs: 12000,
      embedModel: "nomic-embed-text-v2-moe",
      embedDimensions: 768,
    },
    {
      name: "openai",
      type: "openai",
      model: "gpt-5.4-nano",
      baseUrl: "https://api.openai.com/v1",
      timeoutMs: 15000,
    },
    {
      name: "lmstudio",
      type: "lmstudio",
      model: "auto",
      baseUrl: "http://localhost:1234/v1",
      timeoutMs: 12000,
    },
  ],
  defaultTimeoutMs: 15000,
};

// ─── Provider Factory ───

function createLLM(cfg: FallbackProviderConfig): LLMProvider {
  switch (cfg.type) {
    case "ollama":
      return new OllamaLLM(cfg.baseUrl, cfg.model);
    case "lmstudio":
      return lmStudioLLM(cfg.model, cfg.baseUrl);
    case "openai":
      return new OpenAICompatLLM(
        cfg.name,
        cfg.baseUrl || "https://api.openai.com/v1",
        cfg.model,
        cfg.apiKey || "",
      );
    case "openrouter":
      return new OpenAICompatLLM(
        cfg.name,
        cfg.baseUrl || "https://openrouter.ai/api/v1",
        cfg.model,
        cfg.apiKey || "",
      );
    case "anthropic":
      return new AnthropicLLM(cfg.model, cfg.apiKey || "", cfg.baseUrl);
    default:
      throw new Error(`Unknown provider type: ${cfg.type}`);
  }
}

function createEmbed(cfg: FallbackProviderConfig): EmbedProvider | null {
  if (!cfg.embedModel) return null;
  switch (cfg.type) {
    case "ollama":
      return new OllamaEmbed(cfg.baseUrl, cfg.embedModel, cfg.embedDimensions);
    case "lmstudio":
      return lmStudioEmbed(cfg.embedModel!, cfg.embedDimensions, cfg.baseUrl);
    default:
      return null;
  }
}

// ─── Fallback Chain ───

export interface FallbackResult {
  response: string;
  provider: string;
  attemptMs: number;
  fallbacksUsed: number;
}

export class FallbackChain implements LLMProvider {
  private providers: FallbackProviderConfig[];
  private llmInstances: Map<string, LLMProvider> = new Map();
  private embedInstances: Map<string, EmbedProvider> = new Map();
  private defaultTimeoutMs: number;
  private logger?: { info?: (...args: any[]) => void; warn?: (...args: any[]) => void; debug?: (...args: any[]) => void };

  get name(): string {
    return `fallback(${this.providerNames.join("→")})`;
  }

  constructor(config?: Partial<FallbackConfig>, logger?: typeof FallbackChain.prototype.logger) {
    const cfg = { ...DEFAULT_FALLBACK_CONFIG, ...config };
    this.providers = cfg.providers;
    this.defaultTimeoutMs = cfg.defaultTimeoutMs;
    this.logger = logger;
  }

  /**
   * LLMProvider-compatible generate: returns string or throws.
   * Modules (selective, graph, topics, context-tree) call this interface.
   */
  async generate(prompt: string, options?: GenerateOptions): Promise<string> {
    const result = await this.generateWithMeta(prompt, options);
    if (!result) throw new Error("All LLM providers failed");
    return result.response;
  }

  /**
   * Try to generate text using the fallback chain with metadata.
   * Returns null if ALL providers fail (caller should handle FTS-only mode).
   */
  async generateWithMeta(prompt: string, options?: GenerateOptions): Promise<FallbackResult | null> {
    let fallbacksUsed = 0;

    for (const provCfg of this.providers) {
      const start = Date.now();
      const timeoutMs = provCfg.timeoutMs || this.defaultTimeoutMs;

      try {
        const llm = this.getLLM(provCfg);
        
        // Race between LLM call and timeout
        const response = await Promise.race([
          llm.generate(prompt, { ...options, timeoutMs }),
          this.timeout(timeoutMs, provCfg.name),
        ]);

        if (!response || response.trim().length === 0) {
          throw new Error("Empty response");
        }

        const elapsed = Date.now() - start;
        
        if (fallbacksUsed > 0) {
          this.logger?.info?.(`memoria/fallback: ${provCfg.name} responded in ${elapsed}ms (after ${fallbacksUsed} fallback(s))`);
        } else {
          this.logger?.debug?.(`memoria/fallback: ${provCfg.name} responded in ${elapsed}ms`);
        }

        return {
          response,
          provider: provCfg.name,
          attemptMs: elapsed,
          fallbacksUsed,
        };
      } catch (err) {
        const elapsed = Date.now() - start;
        this.logger?.warn?.(`memoria/fallback: ${provCfg.name} failed in ${elapsed}ms: ${String(err).slice(0, 100)}`);
        fallbacksUsed++;
      }
    }

    this.logger?.warn?.(`memoria/fallback: ALL providers failed (${this.providers.length} attempts)`);
    return null;
  }

  /**
   * Get the best available embed provider (first one that has embed config).
   * Embed doesn't need full fallback chain — just use the first available.
   */
  getEmbedProvider(): EmbedProvider | null {
    for (const provCfg of this.providers) {
      if (!provCfg.embedModel) continue;
      try {
        return this.getEmbed(provCfg);
      } catch (_e) {
        continue;
      }
    }
    return null;
  }

  // ─── Private ───

  private getLLM(cfg: FallbackProviderConfig): LLMProvider {
    if (!this.llmInstances.has(cfg.name)) {
      this.llmInstances.set(cfg.name, createLLM(cfg));
    }
    return this.llmInstances.get(cfg.name)!;
  }

  private getEmbed(cfg: FallbackProviderConfig): EmbedProvider {
    if (!this.embedInstances.has(cfg.name)) {
      const embed = createEmbed(cfg);
      if (!embed) throw new Error(`No embed config for ${cfg.name}`);
      this.embedInstances.set(cfg.name, embed);
    }
    return this.embedInstances.get(cfg.name)!;
  }

  private timeout(ms: number, name: string): Promise<never> {
    return new Promise((_, reject) => {
      setTimeout(() => reject(new Error(`${name} timeout after ${ms}ms`)), ms);
    });
  }

  /** Get primary LLM (first in chain) for direct use where fallback isn't needed */
  get primaryLLM(): LLMProvider {
    return this.getLLM(this.providers[0]);
  }

  /** Provider names in order */
  get providerNames(): string[] {
    return this.providers.map(p => p.name);
  }
}
