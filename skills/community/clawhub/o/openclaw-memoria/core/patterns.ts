/**
 * patterns.ts — Layer 20: Behavioral Pattern Detection
 *
 * Detects recurring patterns across facts and consolidates them:
 *   1. Repeated preferences → single consolidated RULE with all contexts preserved
 *   2. If/then behavioral patterns → trigger → action correlations
 *   3. Pattern-boosted recall → confirmed patterns injected first
 *
 * Philosophy: consolidation must be ADDITIVE — never lose a detail.
 * Each occurrence is preserved in an `occurrences` JSON array.
 *
 * Stored as regular facts with fact_type='pattern' for FTS/embedding compatibility.
 */

import type { MemoriaDB, Fact } from "./db.js";
import type { LLMProvider } from "./providers/types.js";

// ─── Types ───

export interface PatternOccurrence {
  factId: string;
  snippet: string;       // first 120 chars of source fact
  date: string;          // ISO date
  category: string;
}

export interface DetectedPattern {
  id: string;
  rule: string;            // consolidated rule text
  patternType: "preference" | "behavior" | "error" | "workflow";
  occurrences: PatternOccurrence[];
  confidence: number;      // 0-1, increases with each occurrence
  triggerContext?: string;  // for if/then patterns: "when X happens"
  action?: string;         // for if/then patterns: "do Y"
  autoWritten: boolean;    // true if already written to USER.md
}

export interface PatternConfig {
  /** Minimum similar facts to form a pattern. Default 3 */
  minOccurrences: number;
  /** Levenshtein similarity threshold for grouping. Default 0.55 */
  similarityThreshold: number;
  /** Jaccard keyword overlap threshold. Default 0.40 */
  jaccardThreshold: number;
  /** Min occurrences before auto-writing to USER.md. Default 5 */
  autoWriteThreshold: number;
  /** Score boost multiplier for pattern facts at recall. Default 1.5 */
  recallBoost: number;
  /** Max patterns to detect per run. Default 10 */
  maxPatternsPerRun: number;
}

const DEFAULT_CONFIG: PatternConfig = {
  minOccurrences: 3,
  similarityThreshold: 0.55,
  jaccardThreshold: 0.40,
  autoWriteThreshold: 5,
  recallBoost: 1.5,
  maxPatternsPerRun: 10,
};

// ─── Helpers ───

function levenshteinSimilarity(a: string, b: string): number {
  const la = a.length, lb = b.length;
  if (la === 0 || lb === 0) return 0;
  // Quick length check: if too different, skip expensive computation
  if (Math.abs(la - lb) / Math.max(la, lb) > 0.6) return 0;

  const maxLen = Math.max(la, lb);
  // Use trimmed/lowered versions
  const sa = a.toLowerCase().trim();
  const sb = b.toLowerCase().trim();

  const prev = new Uint16Array(sb.length + 1);
  const curr = new Uint16Array(sb.length + 1);
  for (let j = 0; j <= sb.length; j++) prev[j] = j;
  for (let i = 1; i <= sa.length; i++) {
    curr[0] = i;
    for (let j = 1; j <= sb.length; j++) {
      curr[j] = sa[i - 1] === sb[j - 1]
        ? prev[j - 1]
        : 1 + Math.min(prev[j - 1], prev[j], curr[j - 1]);
    }
    prev.set(curr);
  }
  return 1 - prev[sb.length] / maxLen;
}

function extractKeywords(text: string): Set<string> {
  const stopWords = new Set([
    "le", "la", "les", "de", "du", "des", "un", "une", "et", "en", "à", "est",
    "que", "qui", "pour", "par", "sur", "pas", "son", "ses", "dans", "avec",
    "the", "a", "an", "is", "are", "was", "of", "to", "and", "in", "for", "on",
    "it", "this", "that", "has", "have", "be", "not", "but", "or", "from",
  ]);
  return new Set(
    text.toLowerCase()
      .replace(/[^\w\sàâéèêëïîôùûüç-]/g, " ")
      .split(/\s+/)
      .filter(w => w.length >= 3 && !stopWords.has(w))
  );
}

function jaccardSimilarity(a: Set<string>, b: Set<string>): number {
  if (a.size === 0 || b.size === 0) return 0;
  let intersection = 0;
  for (const w of a) if (b.has(w)) intersection++;
  return intersection / (a.size + b.size - intersection);
}

// ─── Pattern Manager ───

export class PatternManager {
  private db: MemoriaDB;
  private llm: LLMProvider;
  private cfg: PatternConfig;

  constructor(db: MemoriaDB, llm: LLMProvider, config?: Partial<PatternConfig>) {
    this.db = db;
    this.llm = llm;
    this.cfg = { ...DEFAULT_CONFIG, ...config };
  }

  /**
   * Main entry: scan for repeated similar facts and consolidate into patterns.
   * Called after postProcessNewFacts or periodically.
   */
  async detectAndConsolidate(): Promise<{ detected: number; consolidated: number; autoWritten: number }> {
    const raw = this.db.raw;
    let detected = 0, consolidated = 0, autoWritten = 0;

    // 1. Find groups of similar active non-pattern facts (focus on preferences first, then errors)
    const targetCategories = ["preference", "erreur", "savoir"];

    for (const category of targetCategories) {
      const facts = raw.prepare(
        `SELECT * FROM facts WHERE superseded = 0 AND category = ? AND (fact_type != 'cluster' OR fact_type IS NULL) AND (fact_type != 'pattern' OR fact_type IS NULL) ORDER BY created_at DESC`
      ).all(category) as Fact[];

      if (facts.length < this.cfg.minOccurrences) continue;

      // Group similar facts using keyword + levenshtein clustering
      const groups = this.clusterSimilarFacts(facts);

      for (const group of groups.slice(0, this.cfg.maxPatternsPerRun)) {
        if (group.length < this.cfg.minOccurrences) continue;

        detected++;

        // Check if a pattern already exists for this group
        const existingPattern = this.findExistingPattern(group, category);
        if (existingPattern) {
          // Update existing pattern with new occurrences
          const updated = this.updatePattern(existingPattern, group);
          if (updated) consolidated++;
          continue;
        }

        // Create new pattern via LLM consolidation
        const pattern = await this.consolidateGroup(group, category);
        if (pattern) {
          this.storePattern(pattern);
          consolidated++;

          // Auto-write to USER.md if enough occurrences
          if (pattern.occurrences.length >= this.cfg.autoWriteThreshold && !pattern.autoWritten) {
            // Don't auto-write yet — mark for next run when confirmed
          }
        }
      }
    }

    // 2. Check existing patterns for auto-write eligibility
    const patterns = raw.prepare(
      `SELECT * FROM facts WHERE fact_type = 'pattern' AND superseded = 0`
    ).all() as Fact[];

    for (const pFact of patterns) {
      try {
        const meta = JSON.parse(pFact.tags || "{}") as DetectedPattern;
        if (!meta.autoWritten && meta.occurrences && meta.occurrences.length >= this.cfg.autoWriteThreshold) {
          // Mark as eligible — actual writing done by caller (index.ts)
          autoWritten++;
        }
      } catch (e) { console.debug('memoria:patterns: ' + String(e)); }
    }

    return { detected, consolidated, autoWritten };
  }

  /**
   * Cluster similar facts together using keyword overlap + levenshtein.
   * Returns groups of 2+ similar facts, sorted by group size descending.
   */
  private clusterSimilarFacts(facts: Fact[]): Fact[][] {
    const used = new Set<string>();
    const groups: Fact[][] = [];

    // Precompute keywords
    const kwCache = new Map<string, Set<string>>();
    for (const f of facts) {
      kwCache.set(f.id, extractKeywords(f.fact));
    }

    for (let i = 0; i < facts.length; i++) {
      if (used.has(facts[i].id)) continue;

      const group: Fact[] = [facts[i]];
      const kwA = kwCache.get(facts[i].id)!;

      for (let j = i + 1; j < facts.length; j++) {
        if (used.has(facts[j].id)) continue;

        const kwB = kwCache.get(facts[j].id)!;
        const jaccard = jaccardSimilarity(kwA, kwB);
        const lev = levenshteinSimilarity(facts[i].fact, facts[j].fact);
        const combined = jaccard * 0.5 + lev * 0.5;

        if (combined >= this.cfg.similarityThreshold || jaccard >= this.cfg.jaccardThreshold) {
          group.push(facts[j]);
          used.add(facts[j].id);
        }
      }

      if (group.length >= 2) {
        used.add(facts[i].id);
        groups.push(group);
      }
    }

    // Sort by group size (largest first)
    groups.sort((a, b) => b.length - a.length);
    return groups;
  }

  /**
   * Find an existing pattern that covers this group of facts.
   */
  private findExistingPattern(group: Fact[], category: string): Fact | null {
    const raw = this.db.raw;
    const patterns = raw.prepare(
      `SELECT * FROM facts WHERE fact_type = 'pattern' AND superseded = 0 AND category = ?`
    ).all(category) as Fact[];

    for (const p of patterns) {
      try {
        const meta = JSON.parse(p.tags || "{}") as DetectedPattern;
        if (!meta.occurrences) continue;
        // Check if any member of this group is already in the pattern
        const existingIds = new Set(meta.occurrences.map(o => o.factId));
        const overlap = group.filter(f => existingIds.has(f.id)).length;
        if (overlap >= Math.ceil(group.length * 0.4)) return p;
      } catch (e) { console.debug('memoria:patterns: ' + String(e)); }
    }
    return null;
  }

  /**
   * Update an existing pattern with new occurrences from the group.
   */
  private updatePattern(patternFact: Fact, group: Fact[]): boolean {
    try {
      const meta = JSON.parse(patternFact.tags || "{}") as DetectedPattern;
      const existingIds = new Set(meta.occurrences.map(o => o.factId));

      let added = 0;
      for (const f of group) {
        if (!existingIds.has(f.id)) {
          meta.occurrences.push({
            factId: f.id,
            snippet: f.fact.slice(0, 120),
            date: new Date(f.created_at).toISOString().slice(0, 10),
            category: f.category,
          });
          added++;
          // Supersede the individual fact — it's now part of the pattern
          this.db.raw.prepare("UPDATE facts SET superseded = 1, superseded_by = ? WHERE id = ?")
            .run(patternFact.id, f.id);
        }
      }

      if (added > 0) {
        meta.confidence = Math.min(0.99, 0.7 + meta.occurrences.length * 0.03);
        this.db.raw.prepare("UPDATE facts SET tags = ?, confidence = ?, updated_at = ? WHERE id = ?")
          .run(JSON.stringify(meta), meta.confidence, Date.now(), patternFact.id);
        return true;
      }
    } catch (e) { console.debug('memoria:patterns: ' + String(e)); }
    return false;
  }

  /**
   * Use LLM to consolidate a group of similar facts into a single pattern rule.
   * CRITICAL: The LLM must preserve ALL details from each occurrence.
   */
  private async consolidateGroup(group: Fact[], category: string): Promise<DetectedPattern | null> {
    const occurrences: PatternOccurrence[] = group.map(f => ({
      factId: f.id,
      snippet: f.fact.slice(0, 120),
      date: new Date(f.created_at).toISOString().slice(0, 10),
      category: f.category,
    }));

    const factsText = group.map((f, i) => `${i + 1}. [${new Date(f.created_at).toISOString().slice(0, 10)}] ${f.fact}`).join("\n");

    const prompt = `Consolide ces ${group.length} faits similaires en UNE SEULE règle claire et actionnable.
IMPORTANT: Préserve TOUS les détails et contextes spécifiques de chaque fait. Ne résume pas de façon vague.

Faits:
${factsText}

Réponds en JSON STRICT (pas de markdown, pas de \`\`\`):
{"rule": "La règle consolidée avec tous les détails", "patternType": "${category === 'preference' ? 'preference' : category === 'erreur' ? 'error' : 'behavior'}", "trigger": "contexte déclencheur (si applicable, sinon null)", "action": "action recommandée (si applicable, sinon null)"}`;

    try {
      const response = await this.llm.generate(prompt);
      const cleaned = response.replace(/```json?\s*|\s*```/g, "").trim();
      const parsed = JSON.parse(cleaned);

      if (!parsed.rule) return null;

      const patternType = parsed.patternType || (category === "preference" ? "preference" : "behavior");

      return {
        id: `pattern_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`,
        rule: parsed.rule,
        patternType,
        occurrences,
        confidence: Math.min(0.99, 0.7 + group.length * 0.03),
        triggerContext: parsed.trigger || undefined,
        action: parsed.action || undefined,
        autoWritten: false,
      };
    } catch (e) {
      console.debug('memoria:patterns: ' + String(e));
      // LLM failed — create pattern without LLM (just concatenate facts)
      const rule = `[Auto-consolidé] ${group[0].fact.slice(0, 200)} (${group.length} occurrences similaires)`;
      return {
        id: `pattern_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`,
        rule,
        patternType: category === "preference" ? "preference" : "behavior",
        occurrences,
        confidence: 0.7,
        autoWritten: false,
      };
    }
  }

  /**
   * Store a pattern as a regular fact with fact_type='pattern'.
   * Supersede the individual member facts (they're now consolidated).
   */
  private storePattern(pattern: DetectedPattern): void {
    const fact = pattern.rule;
    const meta = JSON.stringify(pattern);

    this.db.storeFact({
      id: pattern.id,
      fact,
      category: pattern.patternType === "preference" ? "preference" : pattern.patternType === "error" ? "erreur" : "savoir",
      confidence: pattern.confidence,
      source: `pattern:${pattern.patternType}`,
      tags: meta,
      agent: "memoria",
      created_at: Date.now(),
      updated_at: Date.now(),
      fact_type: "pattern",
    });

    // Supersede member facts — they're now consolidated
    for (const occ of pattern.occurrences) {
      this.db.raw.prepare("UPDATE facts SET superseded = 1, superseded_by = ? WHERE id = ? AND superseded = 0")
        .run(pattern.id, occ.factId);
    }
  }

  // ─── Recall helpers ───

  /**
   * Get all active patterns for recall injection.
   */
  getActivePatterns(): Array<{ fact: string; confidence: number; occurrenceCount: number; patternType: string }> {
    const raw = this.db.raw;
    const patterns = raw.prepare(
      `SELECT * FROM facts WHERE fact_type = 'pattern' AND superseded = 0 ORDER BY confidence DESC`
    ).all() as Fact[];

    return patterns.map(p => {
      let occCount = 0;
      let pType = "behavior";
      try {
        const meta = JSON.parse(p.tags || "{}") as DetectedPattern;
        occCount = meta.occurrences?.length || 0;
        pType = meta.patternType || "behavior";
      } catch (e) { console.debug('memoria:patterns: ' + String(e)); }
      return {
        fact: p.fact,
        confidence: p.confidence,
        occurrenceCount: occCount,
        patternType: pType,
      };
    });
  }

  /**
   * Apply recall boost: pattern facts get a multiplier.
   */
  applyPatternBoost(score: number, factType: string | undefined): number {
    if (factType === "pattern") return score * this.cfg.recallBoost;
    return score;
  }

  /**
   * Get patterns eligible for auto-write to USER.md (5+ occurrences, not yet written).
   */
  getPatternsForAutoWrite(): DetectedPattern[] {
    const raw = this.db.raw;
    const patterns = raw.prepare(
      `SELECT * FROM facts WHERE fact_type = 'pattern' AND superseded = 0`
    ).all() as Fact[];

    const eligible: DetectedPattern[] = [];
    for (const p of patterns) {
      try {
        const meta = JSON.parse(p.tags || "{}") as DetectedPattern;
        if (!meta.autoWritten && meta.occurrences && meta.occurrences.length >= this.cfg.autoWriteThreshold) {
          eligible.push(meta);
        }
      } catch (e) { console.debug('memoria:patterns: ' + String(e)); }
    }
    return eligible;
  }

  /**
   * Mark a pattern as auto-written.
   */
  markAutoWritten(patternId: string): void {
    const raw = this.db.raw;
    const fact = raw.prepare("SELECT * FROM facts WHERE id = ?").get(patternId) as Fact | undefined;
    if (!fact) return;
    try {
      const meta = JSON.parse(fact.tags || "{}") as DetectedPattern;
      meta.autoWritten = true;
      raw.prepare("UPDATE facts SET tags = ?, updated_at = ? WHERE id = ?")
        .run(JSON.stringify(meta), Date.now(), patternId);
    } catch (e) { console.debug('memoria:patterns: ' + String(e)); }
  }

  // ─── Stats ───

  stats(): { total: number; byType: Record<string, number>; avgOccurrences: number } {
    const raw = this.db.raw;
    const patterns = raw.prepare(
      `SELECT * FROM facts WHERE fact_type = 'pattern' AND superseded = 0`
    ).all() as Fact[];

    const byType: Record<string, number> = {};
    let totalOcc = 0;

    for (const p of patterns) {
      try {
        const meta = JSON.parse(p.tags || "{}") as DetectedPattern;
        const t = meta.patternType || "unknown";
        byType[t] = (byType[t] || 0) + 1;
        totalOcc += meta.occurrences?.length || 0;
      } catch (e) {
        console.debug('memoria:patterns: ' + String(e));
        byType["unknown"] = (byType["unknown"] || 0) + 1;
      }
    }

    return {
      total: patterns.length,
      byType,
      avgOccurrences: patterns.length > 0 ? Math.round(totalOcc / patterns.length * 10) / 10 : 0,
    };
  }
}
