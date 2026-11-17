/**
 * Memoria — Temporal Scoring & Decay
 * 
 * Mimics brain memory: errors are immune, recent is boosted,
 * old facts decay, frequently accessed facts are stronger.
 */

import type { Fact } from "./db.js";

// ─── Config ───

export const DECAY_CONFIG = {
  // Half-lives by category (in days) — for SEMANTIC facts
  halfLife: {
    erreur: Infinity,     // IMMUNE — never decays
    savoir: 90,
    preference: 90,
    rh: 60,
    client: 60,
    outil: 30,
    chronologie: 14,
  } as Record<string, number>,

  // Episodic facts decay faster (contextual, dated)
  episodicHalfLife: {
    erreur: 30,           // Even episodic errors eventually fade
    savoir: 14,
    preference: 14,
    rh: 14,
    client: 14,
    outil: 7,
    chronologie: 7,
  } as Record<string, number>,

  // Default for unknown categories
  defaultHalfLife: 30,
  defaultEpisodicHalfLife: 14,

  // Recency boost
  recentBoostHours: 24,
  recentBoostFactor: 1.3,
  weekBoostHours: 168, // 7 days
  weekBoostFactor: 1.1,

  // Access frequency boost — muscled: frequent = retained like human memory
  accessBoostFactor: 0.3,  // × log(count+1) — was 0.1, now 3x stronger

  // Freshness bonus (recently UPDATED facts)
  freshnessHours: 48,
  freshnessFactor: 1.2,

  // Stale penalty
  staleThresholdDays: 90,
  stalePenalty: 0.7,
  staleMinConfidence: 0.8,  // Only penalize low-confidence stale facts
};

// ─── Types ───

export interface ScoredFact extends Fact {
  temporalScore: number;
  ageHours: number;
  decayFactor: number;
}

// ─── Scoring ───

export function scoreFact(fact: Fact, now = Date.now()): ScoredFact {
  const ageMs = now - fact.created_at;
  const ageHours = ageMs / (1000 * 60 * 60);
  const ageDays = ageHours / 24;

  let score = fact.confidence;
  let decayFactor = 1.0;

  // 1. Category decay — semantic vs episodic
  const factType = fact.fact_type || "semantic";
  let halfLife: number;
  if (factType === "episodic") {
    halfLife = DECAY_CONFIG.episodicHalfLife[fact.category] ?? DECAY_CONFIG.defaultEpisodicHalfLife;
  } else {
    halfLife = DECAY_CONFIG.halfLife[fact.category] ?? DECAY_CONFIG.defaultHalfLife;
  }
  if (halfLife === Infinity) {
    decayFactor = 1.0; // Immune
  } else {
    decayFactor = Math.pow(0.5, ageDays / halfLife);
  }
  score *= decayFactor;

  // 2. Recency boost
  if (ageHours < DECAY_CONFIG.recentBoostHours) {
    score *= DECAY_CONFIG.recentBoostFactor;
  } else if (ageHours < DECAY_CONFIG.weekBoostHours) {
    score *= DECAY_CONFIG.weekBoostFactor;
  }

  // 3. Access frequency boost
  if (fact.access_count > 0) {
    score *= (1 + DECAY_CONFIG.accessBoostFactor * Math.log(fact.access_count + 1));
  }

  // 4. Freshness bonus (recently MODIFIED, not just created)
  const updateAgeHours = (now - fact.updated_at) / (1000 * 60 * 60);
  if (updateAgeHours < DECAY_CONFIG.freshnessHours) {
    score *= DECAY_CONFIG.freshnessFactor;
  }

  // 5. Stale penalty (old + low confidence)
  if (ageDays > DECAY_CONFIG.staleThresholdDays && fact.confidence < DECAY_CONFIG.staleMinConfidence) {
    score *= DECAY_CONFIG.stalePenalty;
  }

  // 6. Cluster boost — clusters are aggregated "dossiers", more info-dense
  if (factType === "cluster") {
    score *= 1.15; // 15% boost: clusters contain multiple facts = higher recall value
  }

  // 7. Feedback loop: usefulness from actual usage in responses
  const usefulness = fact.usefulness ?? 0;
  const recallCount = fact.recall_count ?? 0;
  if (recallCount > 0) {
    // Useful facts get boosted, consistently ignored facts get penalized
    // Use ratio: used_count / recall_count → 0-1 scale
    const usedCount = fact.used_count ?? 0;
    const usageRatio = usedCount / recallCount;
    
    if (usageRatio > 0.5) {
      // Used more than half the time → boost proportional to usage
      score *= (1 + 0.2 * usageRatio); // Up to +20%
    } else if (recallCount >= 5 && usageRatio < 0.1) {
      // Recalled 5+ times but almost never used → deprioritize
      score *= 0.8; // -20%
    }
    
    // Direct usefulness score influence (capped)
    if (usefulness > 3) {
      score *= 1.1; // Proven useful: +10%
    } else if (usefulness < -2) {
      score *= 0.85; // Proven useless: -15%
    }
  }

  // 8. Relevance weight — identity-aware prioritization (Phase 0)
  // Facts about daily projects (Bureau, Polymarket) > internal tools (Memoria)
  const relevanceWeight = fact.relevance_weight ?? 0.5;
  score *= (0.7 + relevanceWeight * 0.6); // Scale: 0.7x (weight=0) to 1.3x (weight=1.0)

  // 9. Lifecycle multiplier — prioritize fresh > settled > dormant
  // Dormant facts are NOT deleted — they just surface less in auto-recall.
  // When user explicitly asks about past events, lifecycle filter is bypassed.
  // The multiplier is applied externally via LifecycleManager.getRecallMultiplier()
  // to keep scoring independent of lifecycle config/cursor.

  return { ...fact, temporalScore: score, ageHours, decayFactor };
}

export function scoreAndRank(facts: Fact[]): ScoredFact[] {
  const now = Date.now();
  return facts
    .map(f => scoreFact(f, now))
    .sort((a, b) => b.temporalScore - a.temporalScore);
}

// ─── Hot Tier ───
// Facts accessed frequently = "learned by heart" like a phone number you dial often.
// These are always injected in recall, regardless of query relevance.

export const HOT_TIER_CONFIG = {
  /** Minimum access count to be "hot" */
  minAccessCount: 5,
  /** Maximum hot facts to always inject */
  maxHotFacts: 3,
  /** Don't include if last accessed more than X days ago (stale even if hot) */
  staleAfterDays: 30,
};

export function getHotFacts(facts: Fact[], config = HOT_TIER_CONFIG): ScoredFact[] {
  const now = Date.now();
  const staleCutoff = now - config.staleAfterDays * 24 * 60 * 60 * 1000;

  return facts
    .filter(f => f.access_count >= config.minAccessCount && (f.last_accessed_at || f.updated_at) > staleCutoff)
    .map(f => scoreFact(f, now))
    .sort((a, b) => b.access_count - a.access_count) // Sort by usage, not temporal
    .slice(0, config.maxHotFacts);
}
