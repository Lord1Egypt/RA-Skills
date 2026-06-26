/**
 * metrics.ts
 *
 * Persistent metrics collector for the CLI bridge proxy.
 * Tracks request counts, errors, latency, and token usage per model.
 * All operations are O(1) — cannot block the event loop.
 *
 * Metrics are persisted to disk on every recordRequest() call (debounced)
 * and restored on startup so stats survive gateway restarts.
 */

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { METRICS_FILE } from "./config.js";

export interface ModelMetrics {
  model: string;
  requests: number;
  errors: number;
  totalLatencyMs: number;
  promptTokens: number;
  completionTokens: number;
  lastRequestAt: number | null;
}

export interface MetricsSnapshot {
  startedAt: number;
  totalRequests: number;
  totalErrors: number;
  models: ModelMetrics[]; // sorted by requests desc
}

// ── Token estimation ────────────────────────────────────────────────────────

/**
 * Rough token count estimate: ~4 characters per token.
 * This matches the commonly used GPT tokenizer heuristic and is
 * accurate within ~15% for English text / code.
 */
export function estimateTokens(text: string): number {
  if (!text) return 0;
  return Math.ceil(text.length / 4);
}

// ── Persistence format ──────────────────────────────────────────────────────

interface PersistedMetrics {
  version: 1;
  startedAt: number;
  models: ModelMetrics[];
}

// ── Collector ───────────────────────────────────────────────────────────────

class MetricsCollector {
  private startedAt = Date.now();
  private data = new Map<string, ModelMetrics>();
  private flushTimer: ReturnType<typeof setTimeout> | null = null;
  private dirty = false;

  constructor() {
    this.load();
  }

  recordRequest(
    model: string,
    durationMs: number,
    success: boolean,
    promptTokens?: number,
    completionTokens?: number,
  ): void {
    let entry = this.data.get(model);
    if (!entry) {
      entry = {
        model,
        requests: 0,
        errors: 0,
        totalLatencyMs: 0,
        promptTokens: 0,
        completionTokens: 0,
        lastRequestAt: null,
      };
      this.data.set(model, entry);
    }
    entry.requests++;
    if (!success) entry.errors++;
    entry.totalLatencyMs += durationMs;
    if (promptTokens) entry.promptTokens += promptTokens;
    if (completionTokens) entry.completionTokens += completionTokens;
    entry.lastRequestAt = Date.now();
    this.scheduleSave();
  }

  getMetrics(): MetricsSnapshot {
    let totalRequests = 0;
    let totalErrors = 0;
    const models: ModelMetrics[] = [];

    for (const entry of this.data.values()) {
      totalRequests += entry.requests;
      totalErrors += entry.errors;
      models.push({ ...entry });
    }

    models.sort((a, b) => b.requests - a.requests);

    return {
      startedAt: this.startedAt,
      totalRequests,
      totalErrors,
      models,
    };
  }

  reset(): void {
    this.startedAt = Date.now();
    this.data.clear();
    this.saveNow();
  }

  // ── Persistence ─────────────────────────────────────────────────────────

  private load(): void {
    try {
      const raw = readFileSync(METRICS_FILE, "utf-8");
      const persisted = JSON.parse(raw) as PersistedMetrics;
      if (persisted.version === 1 && Array.isArray(persisted.models)) {
        this.startedAt = persisted.startedAt;
        for (const m of persisted.models) {
          this.data.set(m.model, { ...m });
        }
      }
    } catch {
      // File doesn't exist or is corrupt — start fresh
    }
  }

  private scheduleSave(): void {
    this.dirty = true;
    if (this.flushTimer) return;
    // Debounce: save at most once per 5 seconds
    this.flushTimer = setTimeout(() => {
      this.flushTimer = null;
      if (this.dirty) this.saveNow();
    }, 5_000);
  }

  saveNow(): void {
    this.dirty = false;
    const persisted: PersistedMetrics = {
      version: 1,
      startedAt: this.startedAt,
      models: Array.from(this.data.values()),
    };
    try {
      mkdirSync(dirname(METRICS_FILE), { recursive: true });
      writeFileSync(METRICS_FILE, JSON.stringify(persisted, null, 2) + "\n", "utf-8");
    } catch {
      // Best effort — don't crash the proxy for metrics I/O
    }
  }
}

export const metrics = new MetricsCollector();
