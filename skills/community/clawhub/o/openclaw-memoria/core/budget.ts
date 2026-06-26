/**
 * Memoria — Layer 7: Adaptive Budget
 * 
 * Dynamically adjusts the number of facts injected based on available context space.
 * Tiers: empty (12 facts) → light (10) → medium (8) → heavy (5) → critical (2).
 * 
 * Début de session (context vide) → 8-10 faits
 * Session moyenne → 5-6 faits  
 * Session chargée → 2-3 faits essentiels
 * 
 * Évite de saturer le contexte et d'accélérer la compaction.
 */

export interface BudgetConfig {
  /** Max context window in tokens. Default 200000 (Opus) */
  contextWindow: number;
  /** Max facts to inject. Default 10 */
  maxFacts: number;
  /** Min facts to inject (always at least this). Default 2 */
  minFacts: number;
  /** Target % of context to use for memory. Default 0.03 (3%) */
  targetMemoryShare: number;
  /** Avg tokens per fact (estimated). Default 60 */
  avgTokensPerFact: number;
  /** Context usage thresholds */
  thresholds: {
    /** Below this = "light" (use maxFacts). Default 0.3 */
    light: number;
    /** Below this = "medium" (scale down). Default 0.7 */
    medium: number;
    /** Above this = "heavy" (use minFacts). Default 0.85 */
    heavy: number;
  };
}

export const DEFAULT_BUDGET_CONFIG: BudgetConfig = {
  contextWindow: 200000,
  maxFacts: 10,
  minFacts: 2,
  targetMemoryShare: 0.03,
  avgTokensPerFact: 60,
  thresholds: {
    light: 0.3,
    medium: 0.7,
    heavy: 0.85,
  },
};

export interface BudgetResult {
  /** Computed number of facts to inject */
  limit: number;
  /** Context usage ratio (0-1) */
  usage: number;
  /** Budget zone */
  zone: "light" | "medium" | "heavy" | "critical";
  /** Available tokens for memory */
  availableTokens: number;
}

export class AdaptiveBudget {
  private cfg: BudgetConfig;

  // ─── Learning from compactions ───
  // If we inject too many facts and compaction fires right after → we were too aggressive.
  // Track this to self-correct.
  private recentRecalls: Array<{ timestamp: number; limit: number }> = [];
  private compactionPenalty = 0;       // 0-3: reduces limit by this many facts
  private lastCompactionAt = 0;
  private static readonly RECALL_WINDOW_MS = 5 * 60 * 1000; // 5 min window
  private static readonly MAX_PENALTY = 3;

  constructor(config?: Partial<BudgetConfig>) {
    this.cfg = { ...DEFAULT_BUDGET_CONFIG, ...config };
    if (config?.thresholds) {
      this.cfg.thresholds = { ...DEFAULT_BUDGET_CONFIG.thresholds, ...config.thresholds };
    }
  }

  /** 
   * Called when compaction happens. If a recall happened recently,
   * we were likely too aggressive → increase penalty.
   */
  onCompaction(): void {
    const now = Date.now();
    this.lastCompactionAt = now;

    // Was there a recall in the last 5 minutes?
    const recentRecall = this.recentRecalls.find(
      r => (now - r.timestamp) < AdaptiveBudget.RECALL_WINDOW_MS
    );

    if (recentRecall) {
      // We injected facts and compaction fired soon after → too aggressive
      this.compactionPenalty = Math.min(
        this.compactionPenalty + 1,
        AdaptiveBudget.MAX_PENALTY
      );
    }

    // Clean old entries
    this.recentRecalls = this.recentRecalls.filter(
      r => (now - r.timestamp) < AdaptiveBudget.RECALL_WINDOW_MS * 2
    );
  }

  /**
   * Called after a successful recall to log timing.
   */
  recordRecall(limit: number): void {
    this.recentRecalls.push({ timestamp: Date.now(), limit });
    // Keep last 10
    if (this.recentRecalls.length > 10) this.recentRecalls.shift();

    // Decay penalty over time: if no compaction for 30 min, reduce penalty
    if (this.compactionPenalty > 0 && this.lastCompactionAt > 0) {
      const minSinceCompaction = (Date.now() - this.lastCompactionAt) / 60000;
      if (minSinceCompaction > 30) {
        this.compactionPenalty = Math.max(0, this.compactionPenalty - 1);
      }
    }
  }

  /** Current compaction penalty (for logging) */
  get penalty(): number {
    return this.compactionPenalty;
  }

  /**
   * Compute how many facts to inject given current context state.
   * 
   * @param messagesTokenEstimate - Estimated tokens already in conversation
   * @param systemTokenEstimate - Estimated tokens in system prompt + workspace files
   */
  compute(messagesTokenEstimate: number, systemTokenEstimate: number = 0): BudgetResult {
    const totalUsed = messagesTokenEstimate + systemTokenEstimate;
    const usage = Math.min(totalUsed / this.cfg.contextWindow, 1.0);

    // Determine zone
    let zone: BudgetResult["zone"];
    let limit: number;

    if (usage < this.cfg.thresholds.light) {
      zone = "light";
      limit = this.cfg.maxFacts;
    } else if (usage < this.cfg.thresholds.medium) {
      zone = "medium";
      // Aggressive curve: 10 → 4 across medium zone (quadratic ease-in)
      const t = (usage - this.cfg.thresholds.light) / (this.cfg.thresholds.medium - this.cfg.thresholds.light);
      const tCurve = t * t; // quadratic: drops slowly at start, fast at end
      const mediumFloor = this.cfg.minFacts + 2; // 4 facts at end of medium
      limit = Math.round(this.cfg.maxFacts - tCurve * (this.cfg.maxFacts - mediumFloor));
    } else if (usage < this.cfg.thresholds.heavy) {
      zone = "heavy";
      // 4 → minFacts across heavy zone
      const t = (usage - this.cfg.thresholds.medium) / (this.cfg.thresholds.heavy - this.cfg.thresholds.medium);
      const mediumFloor = this.cfg.minFacts + 2; // 4
      limit = Math.round(mediumFloor - t * (mediumFloor - this.cfg.minFacts));
    } else {
      zone = "critical";
      limit = this.cfg.minFacts;
    }

    // Apply compaction penalty (learned from recent compactions)
    if (this.compactionPenalty > 0) {
      limit = Math.max(this.cfg.minFacts, limit - this.compactionPenalty);
    }

    // Ensure bounds
    limit = Math.max(this.cfg.minFacts, Math.min(this.cfg.maxFacts, limit));

    // Available tokens for memory
    const availableTokens = Math.max(0, this.cfg.contextWindow * this.cfg.targetMemoryShare - totalUsed * this.cfg.targetMemoryShare);

    return { limit, usage, zone, availableTokens };
  }

  /**
   * Quick estimate: count messages × avg tokens per message.
   * Rough but fast — no tokenizer needed.
   */
  static estimateTokens(messageCount: number, avgCharsPerMessage: number = 200): number {
    // ~4 chars per token (rough English/French average)
    return Math.round(messageCount * avgCharsPerMessage / 4);
  }
}
