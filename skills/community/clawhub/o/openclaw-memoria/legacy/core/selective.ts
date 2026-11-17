/**
 * Memoria — Layer 3: Selective Memory (Gatekeeper)
 * 
 * Decides whether a new fact should be stored, merged, or rejected.
 * Like the brain filtering: important → store, noise → ignore.
 * 
 * Pipeline (in processAndApply):
 *   1. Noise filter — skip trivial facts ("ok", "merci", too short)
 *   2. FTS5 candidates — find similar existing facts
 *   3. Levenshtein dedup — reject near-exact duplicates
 *   4. Prefix dedup — reject facts that start the same way
 *   5. LLM contradiction check — if similarity > threshold, ask LLM if it contradicts
 *   6. Store / Enrich / Supersede / Skip
 * 
 * Thresholds are configurable per category (preferences have tighter dedup at 0.65).
 * LLM is only called for contradiction detection (step 5), not for every fact.
 * 
 * @example
 * const result = await selective.processAndApply("Bureau uses Convex", "savoir", 0.9);
 * // result: { stored: true, action: "store", factId: "f_abc123" }
 * // or:     { stored: false, action: "skip", reason: "duplicate" }
 */

import type { MemoriaDB, Fact } from "./db.js";
import type { LLMProvider } from "./providers/types.js";
import type { EmbeddingManager } from "./embeddings.js";

// ─── Config ───

export interface SelectiveConfig {
  /** Levenshtein similarity threshold (0-1). Above = duplicate. Default 0.85 */
  dupThreshold: number;
  /** FTS5 candidates to check for dedup. Default 5 */
  dupCandidates: number;
  /** Enable LLM contradiction check. Default true */
  contradictionCheck: boolean;
  /** Minimum fact length to store. Default 10 */
  minFactLength: number;
  /** Minimum importance score (0-1). Below = noise. Default 0.3 */
  importanceThreshold: number;
  /** Enable enrichment (merge similar facts). Default true */
  enrichEnabled: boolean;
  /** Similarity threshold for enrichment (higher than dedup). Default 0.7 */
  enrichThreshold: number;
  /** Cosine similarity threshold for semantic contradiction check. Default 0.55 */
  semanticContradictionThreshold: number;
}

export const DEFAULT_SELECTIVE_CONFIG: SelectiveConfig = {
  dupThreshold: 0.75,
  dupCandidates: 5,
  contradictionCheck: true,
  minFactLength: 10,
  importanceThreshold: 0.3,
  enrichEnabled: true,
  enrichThreshold: 0.60,
  semanticContradictionThreshold: 0.30,
};

// ─── Result type ───

export type SelectiveResult =
  | { action: "store"; fact: string; category: string; confidence: number }
  | { action: "skip"; reason: "noise" | "duplicate" | "too_short" }
  | { action: "supersede"; oldFactId: string; fact: string; category: string; confidence: number }
  | { action: "enrich"; existingFactId: string; mergedFact: string; confidence: number };

// ─── Noise patterns ───

const NOISE_PATTERNS = [
  /^(ok|okay|oui|non|yes|no|merci|thanks|thx|cool|nice|bien|parfait|super|top|génial|d'accord|alright|yep|nope|ah|oh|hmm|hm)\.?$/i,
  /^(bonjour|bonsoir|salut|hello|hi|hey|ciao|bye|bonne nuit|à demain|à \+)\.?$/i,
  /^(je comprends?|compris|noté|vu|reçu|roger|understood|got it|c'est bon|ça marche)\.?$/i,
  /^.{0,5}$/,  // Less than 6 chars = noise
];

const TEMPORAL_NOISE_KEYWORDS = [
  "en train de", "je vais", "je fais", "attends", "patience",
  "une seconde", "un moment", "working on", "processing",
];

// DISPOSABLE TODO patterns — short tasks with no learning value
// ⚠️ Keep ONLY shallow "go do X" patterns. Never filter:
//   - Process knowledge ("pour X il faut Y" = learned trick)
//   - What worked ("X a résolu Y" = experience)
//   - Explanations with "because/car/parce que"
//   - Anything with technical detail (>60 chars usually = knowledge)
const TODO_PATTERNS = [
  /^il faut\b(?!.*(?:car |parce|pour |sinon|→|cause|résou))/i,
  /^on doit\b(?!.*(?:car |parce|pour |sinon|→|cause|résou))/i,
  /^(à|a) faire\s*:/i,
  /^todo\s*:/i,
  /^faut\b(?!.*(?:car |parce|pour |sinon|→))/i,
  /^need(s)? to\b(?!.*(?:because|otherwise|since))/i,
];

// These are ALWAYS disposable — pure transitional state, no knowledge
const TRANSIENT_PATTERNS = [
  /\ben préparation\b/i,
  /\ben cours de\b/i,
  /\bpas encore\b/i,
  /\bnot yet\b/i,
  /\bprochaine étape\b/i,
  /\bnext step\b/i,
];

// Length heuristic: longer facts usually contain knowledge
const MIN_LENGTH_FOR_TRANSIENT = 60;

// ─── Levenshtein ───

function levenshtein(a: string, b: string): number {
  const la = a.length;
  const lb = b.length;
  if (la === 0) return lb;
  if (lb === 0) return la;

  // Optimization: if length difference > 50%, skip (can't be similar)
  if (Math.abs(la - lb) / Math.max(la, lb) > 0.5) return Math.max(la, lb);

  const matrix: number[][] = [];
  for (let i = 0; i <= la; i++) {
    matrix[i] = [i];
    for (let j = 1; j <= lb; j++) {
      if (i === 0) {
        matrix[i][j] = j;
      } else {
        const cost = a[i - 1] === b[j - 1] ? 0 : 1;
        matrix[i][j] = Math.min(
          matrix[i - 1][j] + 1,     // deletion
          matrix[i][j - 1] + 1,     // insertion
          matrix[i - 1][j - 1] + cost // substitution
        );
      }
    }
  }
  return matrix[la][lb];
}

function levenshteinSimilarity(a: string, b: string): number {
  const dist = levenshtein(a.toLowerCase(), b.toLowerCase());
  return 1 - dist / Math.max(a.length, b.length);
}

// ─── Keyword overlap (Jaccard) ───

/** Extract first N words, lowercased and normalized, for prefix dedup */
function extractPrefix(text: string, n: number): string {
  return text.toLowerCase().trim().split(/\s+/).slice(0, n).join(" ");
}

function extractKeywords(text: string): Set<string> {
  return new Set(
    text.toLowerCase()
      .replace(/[^\p{L}\p{N}\s]/gu, " ")
      .split(/\s+/)
      .filter(w => w.length > 2)
  );
}

function jaccardSimilarity(a: Set<string>, b: Set<string>): number {
  if (a.size === 0 && b.size === 0) return 1;
  let intersection = 0;
  for (const w of a) { if (b.has(w)) intersection++; }
  const union = a.size + b.size - intersection;
  return union === 0 ? 0 : intersection / union;
}

// ─── Entity extraction for semantic contradiction detection ───

/** 
 * Extract entities from text by matching against the knowledge graph.
 * Dynamic: uses entities learned by the graph (225+ in DB), not a hardcoded list.
 * Falls back to basic regex patterns for bootstrap (empty graph).
 */
function extractSubjectEntities(fact: string, knownEntities?: string[]): Set<string> {
  const entities = new Set<string>();
  const factLower = fact.toLowerCase();

  // 1. Dynamic: match against all known graph entities
  if (knownEntities && knownEntities.length > 0) {
    for (const entity of knownEntities) {
      // Only match entities with 3+ chars to avoid false positives
      if (entity.length >= 3 && factLower.includes(entity)) {
        entities.add(entity);
      }
    }
  }

  // 2. Fallback regex for bootstrap (when graph is empty or for entities not yet in graph)
  const fallbackPatterns = [
    /\b(Sol|Koda|Luna|Neto)\b/gi,
    /\b(Memoria|Cortex|Ollama|Convex|Bureau|OpenClaw|ClawHub)\b/gi,
    /\b(gemma3[:\w]*|qwen[\w.:]*|gpt[\w-]*|glm[\w.]*|nemotron[\w-]*)\b/gi,
    /\b(openclaw\.json|memoria\.db|cortex\.db)\b/gi,
    /\b(memory-convex|lossless-claw)\b/gi,
  ];
  for (const p of fallbackPatterns) {
    for (const m of fact.matchAll(p)) {
      entities.add(m[0].toLowerCase().trim());
    }
  }

  return entities;
}

// ─── Importance scoring ───

function computeImportance(fact: string, category: string): number {
  let score = 0.5; // baseline

  // Category boosts
  const catBoost: Record<string, number> = {
    erreur: 0.3,
    preference: 0.2,
    rh: 0.2,
    client: 0.15,
    savoir: 0.1,
    outil: 0.05,
    chronologie: 0.0,
  };
  score += catBoost[category] ?? 0;

  // Length signal (longer facts tend to be more informative)
  if (fact.length > 100) score += 0.1;
  if (fact.length > 200) score += 0.05;

  // Contains numbers/versions/dates = likely factual
  if (/\d{2,}/.test(fact)) score += 0.05;
  if (/v\d+\.\d+/i.test(fact)) score += 0.1;

  // Contains technical terms
  if (/(?:api|deploy|config|build|fix|bug|error|crash|prod|merge|commit)/i.test(fact)) score += 0.05;

  // Noise penalty
  for (const kw of TEMPORAL_NOISE_KEYWORDS) {
    if (fact.toLowerCase().includes(kw)) { score -= 0.2; break; }
  }

  return Math.max(0, Math.min(1, score));
}

// ─── Contradiction check prompt ───

const CONTRADICTION_PROMPT = `Compare ces deux faits et détermine leur relation.

Fait existant: "{OLD}"
Nouveau fait: "{NEW}"

RÈGLES IMPORTANTES:
- Un changement de VERSION (v2.7.0 → v3.11.0) est une CONTRADICTION (l'ancien est obsolète)
- Un changement de STATUS (offline → online, installé → désinstallé) est une CONTRADICTION
- Un changement de QUANTITÉ (9 facts → 450 facts) est une CONTRADICTION
- Si les deux parlent du MÊME sujet mais avec des valeurs différentes = CONTRADICTION

Réponds UNIQUEMENT en JSON:
- Si le nouveau CONTREDIT l'ancien: {"relation": "contradiction", "reason": "explication courte"}
- Si le nouveau COMPLÈTE l'ancien: {"relation": "enrichment", "merged": "fait fusionné en une phrase"}
- Si les deux sont INDÉPENDANTS: {"relation": "independent"}
- Si c'est un DOUBLON: {"relation": "duplicate"}`;

// ─── Preference enrichment formatter ───

/**
 * When merging preference facts, preserve ALL details/contexts from each occurrence.
 * Format: 'RÈGLE: [the rule]. Contextes: [context1 (date)], [context2 (date)], ...'
 */
function formatPreferenceEnrichment(existingFact: string, newFact: string, llmMerged: string): string {
  const now = new Date().toISOString().slice(0, 10);

  // If the existing fact already has the RÈGLE format, append new context
  if (existingFact.startsWith("RÈGLE:")) {
    const contextMatch = existingFact.match(/Contextes:\s*(.+)$/);
    const existingContexts = contextMatch ? contextMatch[1] : "";
    // Extract the rule part (up to "Contextes:" or full text)
    const rulePart = existingFact.replace(/\s*Contextes:\s*.+$/, "");
    const newContext = newFact.length > 80 ? newFact.slice(0, 80) + "…" : newFact;
    return `${rulePart} Contextes: ${existingContexts}${existingContexts ? ", " : ""}${newContext} (${now})`;
  }

  // First enrichment: create the RÈGLE format from LLM merged text
  const existingSnippet = existingFact.length > 80 ? existingFact.slice(0, 80) + "…" : existingFact;
  const newSnippet = newFact.length > 80 ? newFact.slice(0, 80) + "…" : newFact;
  return `RÈGLE: ${llmMerged} Contextes: ${existingSnippet} (antérieur), ${newSnippet} (${now})`;
}

// ─── Main class ───

export class SelectiveMemory {
  private db: MemoriaDB;
  private llm: LLMProvider;
  private cfg: SelectiveConfig;
  private embedder: EmbeddingManager | null;
  private knownEntities: string[] = [];
  private entitiesLoadedAt = 0;
  private static ENTITY_CACHE_TTL = 5 * 60 * 1000; // Refresh every 5 min

  /** Callback when a fact is superseded — lets other layers react (observations, clusters) */
  onSupersede: ((supersededFactId: string, newFactId: string) => void) | null = null;

  constructor(db: MemoriaDB, llm: LLMProvider, config?: Partial<SelectiveConfig>, embedder?: EmbeddingManager) {
    this.db = db;
    this.llm = llm;
    this.cfg = { ...DEFAULT_SELECTIVE_CONFIG, ...config };
    this.embedder = embedder ?? null;
    this.refreshEntities();
  }

  /** Load entity names from graph DB (cached, refreshes every 5 min) */
  private refreshEntities(): void {
    try {
      this.knownEntities = this.db.allEntityNames();
      this.entitiesLoadedAt = Date.now();
    } catch (e) { console.debug('memoria:selective: ' + String(e)); }
  }

  private getEntities(): string[] {
    if (Date.now() - this.entitiesLoadedAt > SelectiveMemory.ENTITY_CACHE_TTL) {
      this.refreshEntities();
    }
    return this.knownEntities;
  }

  /**
   * Process a candidate fact through the selective filter.
   * Returns the action to take: store, skip, supersede, or enrich.
   */
  async process(fact: string, category: string, confidence: number): Promise<SelectiveResult> {
    // 1. Basic filters
    if (fact.length < this.cfg.minFactLength) {
      return { action: "skip", reason: "too_short" };
    }

    // Noise pattern check
    for (const pattern of NOISE_PATTERNS) {
      if (pattern.test(fact.trim())) {
        return { action: "skip", reason: "noise" };
      }
    }

    // TODO filter — disposable tasks only (preserve process knowledge)
    const trimmed = fact.trim();
    for (const pattern of TODO_PATTERNS) {
      if (pattern.test(trimmed) && trimmed.length < MIN_LENGTH_FOR_TRANSIENT) {
        return { action: "skip", reason: "noise" };
      }
    }
    // Transient state — only skip if short (long = probably explains WHY)
    for (const pattern of TRANSIENT_PATTERNS) {
      if (pattern.test(trimmed) && trimmed.length < MIN_LENGTH_FOR_TRANSIENT) {
        return { action: "skip", reason: "noise" };
      }
    }

    // Importance check
    const importance = computeImportance(fact, category);
    if (importance < this.cfg.importanceThreshold) {
      return { action: "skip", reason: "noise" };
    }

    // Category-specific thresholds: preferences are often reformulated differently
    // but carry the same intent → use lower thresholds to catch more duplicates
    const isPreference = category === "preference";
    const dupThreshold = isPreference ? 0.65 : this.cfg.dupThreshold;
    const enrichThreshold = isPreference ? 0.45 : this.cfg.enrichThreshold;

    // 2. Dedup check (FTS5 + Levenshtein + Jaccard + prefix check)
    const candidates = this.db.searchFacts(fact, this.cfg.dupCandidates);
    const newKeywords = extractKeywords(fact);
    const newPrefix = extractPrefix(fact, 8);

    for (const candidate of candidates) {
      // Fast prefix check: if first 8 words are identical → duplicate
      if (newPrefix.length >= 6 && newPrefix === extractPrefix(candidate.fact, 8)) {
        return { action: "skip", reason: "duplicate" };
      }

      const levSim = levenshteinSimilarity(fact, candidate.fact);
      const jacSim = jaccardSimilarity(newKeywords, extractKeywords(candidate.fact));
      const combined = levSim * 0.6 + jacSim * 0.4; // weighted average

      // Exact duplicate
      if (combined >= dupThreshold) {
        return { action: "skip", reason: "duplicate" };
      }

      // Potential enrichment or contradiction (moderate similarity)
      if (combined >= enrichThreshold && (this.cfg.contradictionCheck || this.cfg.enrichEnabled)) {
        const relation = await this.checkRelation(candidate, fact);

        if (relation.type === "duplicate") {
          return { action: "skip", reason: "duplicate" };
        }

        if (relation.type === "contradiction") {
          return {
            action: "supersede",
            oldFactId: candidate.id,
            fact,
            category,
            confidence: Math.max(confidence, candidate.confidence),
          };
        }

        if (relation.type === "enrichment" && relation.merged) {
          // For preferences: format enriched fact with consolidated contexts
          const mergedText = isPreference
            ? formatPreferenceEnrichment(candidate.fact, fact, relation.merged)
            : relation.merged;
          return {
            action: "enrich",
            existingFactId: candidate.id,
            mergedFact: mergedText,
            confidence: Math.max(confidence, candidate.confidence),
          };
        }
      }
    }

    // 3. Entity-based contradiction check
    // When text is very different but same entities are mentioned (e.g. "no models on Sol" vs "gemma3 installed on Sol"),
    // Levenshtein/Jaccard miss it. Entity overlap triggers LLM contradiction check.
    if (this.cfg.contradictionCheck) {
      try {
        const newEntities = extractSubjectEntities(fact, this.getEntities());
        if (newEntities.size > 0) {
          // Search for facts sharing at least one entity (using graph DB when available)
          const entityCandidates = this.findFactsBySharedEntities(fact, newEntities, candidates);
          for (const candidate of entityCandidates) {
            const relation = await this.checkRelation(candidate, fact);

            if (relation.type === "contradiction") {
              return {
                action: "supersede",
                oldFactId: candidate.id,
                fact,
                category,
                confidence: Math.max(confidence, candidate.confidence),
              };
            }

            if (relation.type === "enrichment" && relation.merged) {
              return {
                action: "enrich",
                existingFactId: candidate.id,
                mergedFact: relation.merged,
                confidence: Math.max(confidence, candidate.confidence),
              };
            }

            if (relation.type === "duplicate") {
              return { action: "skip", reason: "duplicate" };
            }
          }
        }
      } catch (e) {
        console.debug('memoria:selective: ' + String(e));
        // Entity check failed → continue with store (fail-safe)
      }
    }

    // 4. No issues — store as new
    return { action: "store", fact, category, confidence };
  }

  /**
   * Process and apply: run the selective filter and execute the result.
   * Returns the stored/updated fact or null if skipped.
   */
  async processAndApply(fact: string, category: string, confidence: number, agent = "koda", factType: "semantic" | "episodic" = "semantic", relevanceWeight = 0.5): Promise<{ stored: boolean; action: string; factId?: string; reason?: string }> {
    const result = await this.process(fact, category, confidence);

    switch (result.action) {
      case "skip":
        return { stored: false, action: "skip", reason: result.reason };

      case "store": {
        const stored = this.db.storeFact({
          id: `fact_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`,
          fact: result.fact,
          category: result.category,
          confidence: result.confidence,
          source: "auto-capture",
          tags: "[]",
          agent,
          created_at: Date.now(),
          updated_at: Date.now(),
          fact_type: factType,
          relevance_weight: relevanceWeight,
        });
        return { stored: true, action: "store", factId: stored.id };
      }

      case "supersede": {
        // Store new fact
        const newFact = this.db.storeFact({
          id: `fact_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`,
          fact: result.fact,
          category: result.category,
          confidence: result.confidence,
          source: "auto-capture",
          tags: "[]",
          agent,
          created_at: Date.now(),
          updated_at: Date.now(),
          fact_type: factType,
          relevance_weight: relevanceWeight,
        });
        // Mark old as superseded
        this.db.supersedeFact(result.oldFactId, newFact.id);
        // Notify other layers (observations, clusters)
        try { this.onSupersede?.(result.oldFactId, newFact.id); } catch (e) { console.debug('memoria:selective: ' + String(e)); }
        return { stored: true, action: "supersede", factId: newFact.id };
      }

      case "enrich": {
        // Update existing fact with merged text
        this.db.enrichFact(result.existingFactId, result.mergedFact, result.confidence);
        return { stored: true, action: "enrich", factId: result.existingFactId };
      }
    }
  }

  // ─── Private ───

  /**
   * Find existing facts that share at least one entity with the new fact.
   * Excludes facts already checked in the textual dedup pass.
   * Limited to MAX_ENTITY_CANDIDATES to avoid excessive LLM calls.
   */
  private findFactsBySharedEntities(newFact: string, newEntities: Set<string>, alreadyChecked: Fact[]): Fact[] {
    // FIX 3: Increased from 5 to 10 — version contradictions need wider search
    // (e.g., "Sol = v2.7.0" stored 6 times won't all be caught with limit 5)
    const MAX_ENTITY_CANDIDATES = 10;
    const checkedIds = new Set(alreadyChecked.map(c => c.id));
    const candidates: Fact[] = [];

    // FIX 3: Prioritize version-containing facts when new fact has a version
    const hasVersion = /v\d+\.\d+/i.test(newFact);

    // Search for each entity via FTS (wider search to catch all related facts)
    for (const entity of newEntities) {
      if (candidates.length >= MAX_ENTITY_CANDIDATES) break;
      const ftsResults = this.db.searchFacts(entity, 30);
      for (const result of ftsResults) {
        if (candidates.length >= MAX_ENTITY_CANDIDATES) break;
        if (checkedIds.has(result.id)) continue;
        // Verify entity overlap
        const resultEntities = extractSubjectEntities(result.fact, this.getEntities());
        const shared = [...newEntities].filter(e => resultEntities.has(e));
        if (shared.length > 0) {
          // FIX 3: Boost priority for version-related facts
          // When new fact says "Sol = v3.11", and existing says "Sol = v2.7", 
          // this MUST be checked even if Levenshtein is low
          if (hasVersion && /v\d+\.\d+/i.test(result.fact)) {
            // Put version facts first (higher priority for contradiction check)
            candidates.unshift(result);
          } else {
            candidates.push(result);
          }
          checkedIds.add(result.id);
        }
      }
    }

    return candidates.slice(0, MAX_ENTITY_CANDIDATES);
  }

  private async checkRelation(existing: Fact, newFact: string): Promise<{
    type: "contradiction" | "enrichment" | "duplicate" | "independent";
    merged?: string;
    reason?: string;
  }> {
    try {
      const prompt = CONTRADICTION_PROMPT
        .replace("{OLD}", existing.fact)
        .replace("{NEW}", newFact);

      const response = await this.llm.generate(prompt, {
        maxTokens: 256,
        temperature: 0.1,
        format: "json",
        timeoutMs: 15000,
      });

      const parsed = this.parseJSON(response) as {
        relation?: string;
        merged?: string;
        reason?: string;
      };

      if (!parsed?.relation) return { type: "independent" };

      switch (parsed.relation) {
        case "contradiction":
          return { type: "contradiction", reason: parsed.reason };
        case "enrichment":
          return { type: "enrichment", merged: parsed.merged };
        case "duplicate":
          return { type: "duplicate" };
        default:
          return { type: "independent" };
      }
    } catch (e) {
      console.debug('memoria:selective: ' + String(e));
      // LLM failed → safe default: treat as independent (store both)
      return { type: "independent" };
    }
  }

  private parseJSON(text: string): unknown {
    let cleaned = text.trim();
    if (cleaned.startsWith("```")) {
      const lines = cleaned.split("\n");
      lines.shift();
      if (lines[lines.length - 1]?.trim() === "```") lines.pop();
      cleaned = lines.join("\n").trim();
    }
    const match = cleaned.match(/(\{[\s\S]*\}|\[[\s\S]*\])/);
    if (match) cleaned = match[1];
    return JSON.parse(cleaned);
  }
}
