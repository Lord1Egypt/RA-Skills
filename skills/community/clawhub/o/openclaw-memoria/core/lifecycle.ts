/**
 * Lifecycle Manager — Human-like memory prioritization
 * 
 * Philosophy: NEVER delete, NEVER forget. Everything stays in the DB forever.
 * Lifecycle controls RECALL PRIORITY, not existence.
 * 
 * States:
 *   fresh    → new facts (< freshDays), high recall priority
 *   settled  → established facts (accessed 3+ times OR aged past freshDays), normal priority
 *   dormant  → not accessed in 60+ days, low auto-recall priority but ALWAYS searchable on demand
 * 
 * The "detail cursor" (1-10) lets the user control how much dormant context
 * gets included in automatic recall:
 *   cursor 1  → only fresh + top settled
 *   cursor 5  → fresh + settled (default)
 *   cursor 10 → fresh + settled + dormant (everything)
 * 
 * When the user explicitly asks about a past event ("what did I do on March 15?"),
 * ALL states are searched regardless of cursor — like asking your secretary to check the calendar.
 * 
 * Key insight from Neto: "I still remember learning to ride a bike at age 7.
 * You don't forget — you just don't think about it every day."
 */

import type { MemoriaDB, Fact } from "./db.js";

export interface LifecycleConfig {
  /** Days a fact stays "fresh" (high priority). Default: 15 */
  freshDays: number;
  /** Min access_count to become "settled" before freshDays. Default: 3 */
  settledMinAccess: number;
  /** Days without access before becoming "dormant". Default: 60 */
  dormantAfterDays: number;
  /** Detail cursor (1-10). Controls how much dormant context is auto-recalled. Default: 5 */
  detailCursor: number;
  /** After N recalls of a settled fact, consider proactive revision. Default: 10 */
  revisionRecallThreshold: number;
}

export const DEFAULT_LIFECYCLE_CONFIG: LifecycleConfig = {
  freshDays: 15,
  settledMinAccess: 3,
  dormantAfterDays: 60,
  detailCursor: 5,
  revisionRecallThreshold: 10,
};

export type LifecycleState = "fresh" | "settled" | "dormant";

// Backward compat: map old states to new
function normalizeState(state: string | null | undefined): LifecycleState {
  if (!state || state === "fresh") return "fresh";
  if (state === "mature" || state === "settled") return "settled";
  if (state === "aged" || state === "archived" || state === "dormant") return "dormant";
  return "fresh";
}

export class LifecycleManager {
  private db: MemoriaDB;
  private cfg: LifecycleConfig;

  constructor(db: MemoriaDB, config?: Partial<LifecycleConfig>) {
    this.db = db;
    this.cfg = { ...DEFAULT_LIFECYCLE_CONFIG, ...config };
  }

  /**
   * Update lifecycle state for a single fact.
   * Uses access_count as the real signal (not recall_count which was broken).
   */
  updateLifecycle(fact: Fact, now = Date.now()): LifecycleState {
    const ageDays = (now - fact.created_at) / (1000 * 60 * 60 * 24);
    const accessCount = fact.access_count ?? 0;
    const lastAccessed = fact.last_accessed_at ?? fact.created_at;
    const daysSinceAccess = (now - lastAccessed) / (1000 * 60 * 60 * 24);

    let newState: LifecycleState;

    // Dormant: not accessed in dormantAfterDays AND past fresh period
    if (
      ageDays > this.cfg.freshDays &&
      daysSinceAccess > this.cfg.dormantAfterDays
    ) {
      newState = "dormant";
    }
    // Settled: either accessed enough times, or past fresh period with some access
    else if (
      accessCount >= this.cfg.settledMinAccess ||
      (ageDays > this.cfg.freshDays && accessCount > 0)
    ) {
      newState = "settled";
    }
    // Fresh: still new
    else if (ageDays <= this.cfg.freshDays) {
      newState = "fresh";
    }
    // Past fresh period, never accessed → still settled (not dormant yet, needs dormantAfterDays)
    else {
      newState = "settled";
    }

    // Normalize old state for comparison
    const currentState = normalizeState(fact.lifecycle_state);

    // A dormant fact that gets accessed again → back to settled (wake up)
    if (currentState === "dormant" && accessCount > 0 && daysSinceAccess < this.cfg.dormantAfterDays) {
      newState = "settled";
    }

    // Only update DB if state changed
    if (newState !== currentState) {
      this.db.raw.prepare("UPDATE facts SET lifecycle_state = ? WHERE id = ?").run(newState, fact.id);
    }

    return newState;
  }

  /**
   * Batch update: refresh all active facts' lifecycle states
   */
  refreshAll(): { updated: number; breakdown: Record<LifecycleState, number> } {
    try {
      const facts = this.db.raw.prepare("SELECT * FROM facts WHERE superseded = 0").all() as Fact[];
      const now = Date.now();
      let updated = 0;

      const breakdown: Record<LifecycleState, number> = {
        fresh: 0,
        settled: 0,
        dormant: 0,
      };

      for (const fact of facts) {
        const oldState = normalizeState(fact.lifecycle_state);
        const newState = this.updateLifecycle(fact, now);
        if (oldState !== newState) updated++;
        breakdown[newState]++;
      }

      return { updated, breakdown };
    } catch (err) {
      console.error("[lifecycle] refreshAll failed:", err);
      return { updated: 0, breakdown: { fresh: 0, settled: 0, dormant: 0 } };
    }
  }

  /**
   * Get the recall score multiplier based on lifecycle state and detail cursor.
   * 
   * fresh   → 1.0 (always full priority)
   * settled → 0.8 (slight reduction)
   * dormant → scales with cursor:
   *   cursor 1  → 0.05 (almost invisible in auto-recall)
   *   cursor 5  → 0.25 (occasionally surfaces)
   *   cursor 10 → 0.7  (nearly full priority)
   */
  getRecallMultiplier(state: string | null | undefined): number {
    const s = normalizeState(state);
    if (s === "fresh") return 1.0;
    if (s === "settled") return 0.85;
    // dormant: scale with cursor (1-10)
    const cursor = Math.max(1, Math.min(10, this.cfg.detailCursor));
    return 0.05 + (cursor - 1) * 0.072; // cursor 1→0.05, 5→0.34, 10→0.70
  }

  /**
   * Check if a settled fact needs proactive revision
   */
  needsRevision(fact: Fact): boolean {
    const state = normalizeState(fact.lifecycle_state);
    if (state !== "settled") return false;
    const accessCount = fact.access_count ?? 0;
    return accessCount >= this.cfg.revisionRecallThreshold;
  }

  /**
   * Get all facts needing revision
   */
  getFactsNeedingRevision(): Fact[] {
    const facts = this.db.raw.prepare(
      `SELECT * FROM facts 
       WHERE superseded = 0 
       AND lifecycle_state = 'settled' 
       AND access_count >= ?
       ORDER BY access_count DESC
       LIMIT 5`
    ).all(this.cfg.revisionRecallThreshold) as Fact[];
    return facts;
  }

  /**
   * Get stats breakdown by lifecycle state
   */
  getStats(): Record<LifecycleState, number> {
    try {
      const rows = this.db.raw.prepare(
        `SELECT lifecycle_state, COUNT(*) as count 
         FROM facts 
         WHERE superseded = 0 
         GROUP BY lifecycle_state`
      ).all() as Array<{ lifecycle_state: string; count: number }>;

      const stats: Record<LifecycleState, number> = {
        fresh: 0,
        settled: 0,
        dormant: 0,
      };

      for (const row of rows) {
        const normalized = normalizeState(row.lifecycle_state);
        stats[normalized] += row.count;
      }

      return stats;
    } catch (err) {
      console.error("[lifecycle] getStats failed:", err);
      return { fresh: 0, settled: 0, dormant: 0 };
    }
  }

  /** Get current detail cursor value */
  get detailCursor(): number {
    return this.cfg.detailCursor;
  }
}
