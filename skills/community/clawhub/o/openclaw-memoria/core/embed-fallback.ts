/**
 * Memoria — Embed Fallback Provider
 * 
 * Wraps multiple EmbedProviders and tries them in order.
 * If provider 1 fails → try provider 2 → try provider 3.
 * Analogous to FallbackChain for LLMProviders.
 */

import type { EmbedProvider } from "./providers/types.js";

export class EmbedFallback implements EmbedProvider {
  private providers: EmbedProvider[];
  private _dimensions: number;
  private _name: string;
  private logger?: { info?: (...args: unknown[]) => void; warn?: (...args: unknown[]) => void };

  constructor(providers: EmbedProvider[], logger?: { info?: (...args: unknown[]) => void; warn?: (...args: unknown[]) => void }) {
    if (providers.length === 0) throw new Error("EmbedFallback requires at least one provider");
    this.providers = providers;
    this._dimensions = providers[0].dimensions;
    this._name = `embed-fallback(${providers.map(p => p.name).join("→")})`;
    this.logger = logger;
  }

  get dimensions(): number {
    return this._dimensions;
  }

  get name(): string {
    return this._name;
  }

  get providerNames(): string[] {
    return this.providers.map(p => p.name);
  }

  async embed(text: string): Promise<number[]> {
    let lastErr: Error | null = null;
    for (const provider of this.providers) {
      try {
        return await provider.embed(text);
      } catch (err) {
        lastErr = err instanceof Error ? err : new Error(String(err));
        this.logger?.warn?.(`memoria: embed fallback — ${provider.name} failed: ${lastErr.message}`);
      }
    }
    throw lastErr || new Error("All embed providers failed");
  }

  async embedBatch(texts: string[]): Promise<number[][]> {
    let lastErr: Error | null = null;
    for (const provider of this.providers) {
      try {
        return await provider.embedBatch(texts);
      } catch (err) {
        lastErr = err instanceof Error ? err : new Error(String(err));
        this.logger?.warn?.(`memoria: embedBatch fallback — ${provider.name} failed: ${lastErr.message}`);
      }
    }
    throw lastErr || new Error("All embed providers failed");
  }
}
