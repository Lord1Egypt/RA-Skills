/**
 * Memoria — Provider Interfaces
 * 
 * These interfaces are the contract between Memoria and any LLM/embedding backend.
 * To add a new provider (e.g., Groq, Together, Mistral):
 *   1. Create providers/your-provider.ts implementing LLMProvider and/or EmbedProvider
 *   2. Add to the switch in fallback.ts buildProvider()
 *   3. Add your type to the ProviderConfig.type union below
 * 
 * All providers are wrapped by FallbackChain — modules never call providers directly.
 */

/** Embedding provider: converts text → float vector. */
export interface EmbedProvider {
  embed(text: string): Promise<number[]>;
  embedBatch(texts: string[]): Promise<number[][]>;
  readonly dimensions: number;
  readonly name: string;
}

/** Options for LLM generation. All optional — providers use their own defaults. */
export interface GenerateOptions {
  maxTokens?: number;
  temperature?: number;
  format?: "json" | "text";
  timeoutMs?: number;
}

/** Extended result with metadata for debugging/logging. */
export interface GenerateResult {
  response: string;
  provider: string;
  attemptMs: number;
  fallbacksUsed: number;
}

/** LLM text generation provider. Only generate() is required; generateWithMeta() is optional. */
export interface LLMProvider {
  generate(prompt: string, options?: GenerateOptions): Promise<string>;
  /** Extended generate with metadata. Default implementation wraps generate(). */
  generateWithMeta?(prompt: string, options?: GenerateOptions): Promise<GenerateResult | null>;
  readonly name: string;
}

/** Config for building a provider instance. Used in fallback[] array and llm/embed config sections. */
export interface ProviderConfig {
  type: "ollama" | "lmstudio" | "openai" | "openrouter" | "anthropic";
  baseUrl: string;
  model: string;
  apiKey?: string;
  dimensions?: number;  // for embed
}
