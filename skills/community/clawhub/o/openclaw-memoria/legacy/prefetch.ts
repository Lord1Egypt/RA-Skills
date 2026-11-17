/**
 * Memoria — Async Prefetch (inspired by Hermes)
 *
 * Strategy: When message_received fires, we immediately start the recall
 * computation in the background. By the time before_prompt_build fires
 * (usually 50-200ms later), the result is already cached.
 *
 * This eliminates recall latency from the critical path.
 */

export interface PrefetchResult {
  prompt: string;
  result: string | undefined;
  timestamp: number;
  computeTimeMs: number;
}

export class PrefetchCache {
  private cache: PrefetchResult | null = null;
  private pending: Promise<PrefetchResult> | null = null;
  private readonly maxAgeMs: number;

  constructor(maxAgeMs = 30_000) {
    this.maxAgeMs = maxAgeMs;
  }

  /**
   * Start a prefetch computation. Called from message_received hook.
   * Non-blocking — returns immediately.
   */
  startPrefetch(prompt: string, computeFn: () => Promise<string | undefined>): void {
    // Don't prefetch very short messages (system events, etc.)
    if (!prompt || prompt.length < 5) return;

    const startTime = Date.now();
    this.pending = computeFn()
      .then((result) => {
        const entry: PrefetchResult = {
          prompt,
          result,
          timestamp: Date.now(),
          computeTimeMs: Date.now() - startTime,
        };
        this.cache = entry;
        this.pending = null;
        return entry;
      })
      .catch(() => {
        this.pending = null;
        return { prompt, result: undefined, timestamp: Date.now(), computeTimeMs: Date.now() - startTime };
      });
  }

  /**
   * Get the prefetched result. Called from before_prompt_build hook.
   * If the prefetch is still running, waits for it (bounded by timeout).
   * If no prefetch was started, returns null (caller falls back to sync recall).
   */
  async get(currentPrompt: string, timeoutMs = 5_000): Promise<PrefetchResult | null> {
    // Check cache first
    if (this.cache) {
      const age = Date.now() - this.cache.timestamp;
      if (age < this.maxAgeMs && this.promptMatches(this.cache.prompt, currentPrompt)) {
        return this.cache;
      }
    }

    // Wait for pending computation if it exists
    if (this.pending) {
      try {
        const result = await Promise.race([
          this.pending,
          new Promise<null>((resolve) => setTimeout(() => resolve(null), timeoutMs)),
        ]);
        if (result && this.promptMatches(result.prompt, currentPrompt)) {
          return result;
        }
      } catch {
        // Prefetch failed, caller will do sync recall
      }
    }

    return null;
  }

  /**
   * Check if the prefetched prompt matches the current prompt.
   * Uses a fuzzy match — the user message portion should match
   * even if the full event prompt has different metadata.
   */
  private promptMatches(prefetchedPrompt: string, currentPrompt: string): boolean {
    // Extract user message from both (last significant chunk)
    const extractUserMsg = (p: string): string => {
      // Strip common Memoria/OpenClaw envelope
      const lastBlock = p.lastIndexOf("```\n\n");
      if (lastBlock !== -1 && p.includes("untrusted metadata")) {
        return p.slice(lastBlock + 5).trim().slice(0, 200);
      }
      return p.slice(-200).trim();
    };

    const a = extractUserMsg(prefetchedPrompt);
    const b = extractUserMsg(currentPrompt);

    // Exact match on user portion
    if (a === b) return true;

    // One contains the other (common when metadata wrapping differs)
    if (a.length > 20 && b.length > 20) {
      return a.includes(b.slice(0, 100)) || b.includes(a.slice(0, 100));
    }

    return false;
  }

  /** Clear the cache (e.g., on session end) */
  clear(): void {
    this.cache = null;
    this.pending = null;
  }

  /** Get stats for debugging */
  stats(): { hasCached: boolean; hasPending: boolean; lastComputeMs: number | null; cacheAgeMs: number | null } {
    return {
      hasCached: this.cache !== null,
      hasPending: this.pending !== null,
      lastComputeMs: this.cache?.computeTimeMs ?? null,
      cacheAgeMs: this.cache ? Date.now() - this.cache.timestamp : null,
    };
  }
}
