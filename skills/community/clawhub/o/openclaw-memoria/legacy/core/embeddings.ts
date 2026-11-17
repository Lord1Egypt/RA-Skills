/**
 * Memoria — Layer 4: Embeddings + Hybrid Search
 * 
 * Stores 768d float vectors in SQLite (BLOB), computes cosine similarity,
 * and provides hybrid search (FTS5 text match + cosine similarity + temporal scoring).
 * 
 * Key methods:
 *   embedFact(id, text) — compute and store embedding for one fact
 *   embedBatch() — batch process all unembedded facts
 *   hybridSearch(query) — combined FTS5 + cosine + scoring
 *   cosineSimilarity(a, b) — vector distance (exported utility)
 * 
 * Les vecteurs sont stockés en Float32Array → BLOB pour perf maximale.
 */

import type { MemoriaDB, Fact } from "./db.js";
import type { EmbedProvider } from "./providers/types.js";
import type { ScoredFact } from "./scoring.js";
import { scoreFact } from "./scoring.js";

// ─── Vector Utils ───

/** Float32Array → Buffer (for SQLite BLOB storage) */
export function vectorToBlob(vec: number[]): Buffer {
  return Buffer.from(new Float32Array(vec).buffer);
}

/** Buffer (SQLite BLOB) → number[] */
export function blobToVector(blob: Buffer): number[] {
  const f32 = new Float32Array(blob.buffer, blob.byteOffset, blob.byteLength / 4);
  return Array.from(f32);
}

/** Cosine similarity between two vectors. Returns 0-1. */
export function cosineSimilarity(a: number[], b: number[]): number {
  if (a.length !== b.length) return 0;
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  const denom = Math.sqrt(normA) * Math.sqrt(normB);
  return denom === 0 ? 0 : dot / denom;
}

// ─── Types ───

export interface EmbeddedFact extends Fact {
  similarity: number;
  temporalScore: number;
  hybridScore: number;
}

interface EmbeddingRow {
  fact_id: string;
  vector: Buffer;
  model: string;
}

// ─── Embedding Manager ───

export class EmbeddingManager {
  private db: MemoriaDB;
  private provider: EmbedProvider;
  private modelName: string;

  constructor(db: MemoriaDB, provider: EmbedProvider) {
    this.db = db;
    this.provider = provider;
    this.modelName = provider.name;
  }

  /** Get raw DB handle for direct queries */
  private get rawDb() {
    return this.db.raw;
  }

  // ─── Store ───

  /** Embed a single fact and store the vector */
  async embedFact(factId: string, text: string): Promise<void> {
    const vector = await this.provider.embed(text);
    const blob = vectorToBlob(vector);
    this.rawDb.prepare(
      "INSERT OR REPLACE INTO embeddings (fact_id, vector, model, created_at) VALUES (?, ?, ?, ?)"
    ).run(factId, blob, this.modelName, Date.now());
  }

  /** Embed multiple facts in batch */
  async embedBatch(facts: Array<{ id: string; text: string }>): Promise<number> {
    if (facts.length === 0) return 0;

    // Batch embed (max 32 at a time to avoid timeout)
    const BATCH_SIZE = 32;
    let embedded = 0;

    for (let i = 0; i < facts.length; i += BATCH_SIZE) {
      const batch = facts.slice(i, i + BATCH_SIZE);
      const texts = batch.map(f => f.text);

      try {
        const vectors = await this.provider.embedBatch(texts);
        const stmt = this.rawDb.prepare(
          "INSERT OR REPLACE INTO embeddings (fact_id, vector, model, created_at) VALUES (?, ?, ?, ?)"
        );
        const now = Date.now();
        const tx = this.rawDb.transaction(() => {
          for (let j = 0; j < batch.length; j++) {
            stmt.run(batch[j].id, vectorToBlob(vectors[j]), this.modelName, now);
          }
        });
        tx();
        embedded += batch.length;
      } catch (err) {
        // Try one by one on batch failure
        for (const fact of batch) {
          try {
            await this.embedFact(fact.id, fact.text);
            embedded++;
          } catch (e) { console.debug('memoria:embeddings: ' + String(e)); }
        }
      }
    }

    return embedded;
  }

  // ─── Search ───

  /** Semantic search: embed query → cosine similarity with all stored vectors */
  async semanticSearch(query: string, limit = 10, minSimilarity = 0.3): Promise<EmbeddedFact[]> {
    const queryVector = await this.provider.embed(query);

    // Get all embeddings (we compute cosine in JS — fast enough for <10K facts)
    const rows = this.rawDb.prepare(
      "SELECT e.fact_id, e.vector FROM embeddings e JOIN facts f ON e.fact_id = f.id WHERE f.superseded = 0"
    ).all() as EmbeddingRow[];

    if (rows.length === 0) return [];

    // Compute similarities
    const scored: Array<{ factId: string; similarity: number }> = [];
    for (const row of rows) {
      const vec = blobToVector(row.vector);
      const sim = cosineSimilarity(queryVector, vec);
      if (sim >= minSimilarity) {
        scored.push({ factId: row.fact_id, similarity: sim });
      }
    }

    // Sort by similarity, take top N
    scored.sort((a, b) => b.similarity - a.similarity);
    const topIds = scored.slice(0, limit * 2); // Get extras for post-filtering

    // Fetch full facts
    const results: EmbeddedFact[] = [];
    for (const { factId, similarity } of topIds) {
      const fact = this.db.getFact(factId);
      if (!fact || fact.superseded) continue;

      const sf = scoreFact(fact);
      results.push({
        ...fact,
        similarity,
        temporalScore: sf.temporalScore,
        hybridScore: 0, // computed in hybridSearch
      });
    }

    return results.slice(0, limit);
  }

  // ─── Query Expansion ───

  /**
   * Expand a query into multiple variants for better recall.
   * Uses the embedding model to find semantically similar terms.
   * No LLM needed — pure heuristic expansion with synonym/concept maps.
   */
  expandQuery(query: string): string[] {
    const variants = [query];
    const lower = query.toLowerCase().trim();

    // Concept expansions: STRICT synonym pairs only (avoid noise from loose associations)
    const conceptMap: Record<string, string[]> = {
      // Money/salary — bidirectional synonyms
      "taux horaire": ["€/h", "salaire"],
      "salaire": ["taux horaire", "€/h"],
      "rémunération": ["salaire", "€/h"],
      "ca": ["chiffre d'affaires"],
      "chiffre d'affaires": ["CA"],
      // Tech — FR↔EN translations only
      "deploy": ["déploiement"],
      "déploiement": ["deploy"],
      "modèle": ["model"],
      "modèles": ["models"],
      // Config
      "config": ["configuration"],
      "configuration": ["config"],
    };

    // Check each concept key against the query
    for (const [key, synonyms] of Object.entries(conceptMap)) {
      if (lower.includes(key)) {
        // Add 1-2 best synonym variants
        for (const syn of synonyms.slice(0, 2)) {
          const variant = query.replace(new RegExp(key, "gi"), syn);
          if (variant !== query && !variants.includes(variant)) {
            variants.push(variant);
          }
        }
      }
    }

    // Entity extraction: if query contains a proper noun, add it standalone
    const properNouns = query.match(/\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*/g);
    if (properNouns) {
      for (const noun of properNouns) {
        if (noun.length > 2 && !variants.includes(noun)) {
          variants.push(noun);
        }
      }
    }

    return variants.slice(0, 4); // Max 4 variants
  }

  /** Hybrid search: FTS5 + cosine, merge and rank — with query expansion */
  async hybridSearch(query: string, limit = 10, options?: {
    ftsWeight?: number;    // Weight for FTS5 results (default 0.4)
    cosineWeight?: number; // Weight for cosine results (default 0.4)
    temporalWeight?: number; // Weight for temporal score (default 0.2)
    minSimilarity?: number;
    expandQueries?: boolean; // Enable query expansion (default true)
  }): Promise<EmbeddedFact[]> {
    // Adaptive weights: short/generic queries → favor semantic over FTS
    // because FTS on a 1-word query like "Bureau" matches too many facts
    const queryWords = query.trim().split(/\s+/).filter(w => w.length > 2);
    const isShortQuery = queryWords.length <= 2;
    const ftsW = options?.ftsWeight ?? (isShortQuery ? 0.20 : 0.40);
    const cosW = options?.cosineWeight ?? (isShortQuery ? 0.55 : 0.40);
    const tempW = options?.temporalWeight ?? (isShortQuery ? 0.25 : 0.20);
    const minSim = options?.minSimilarity ?? 0.25;

    // Query expansion: generate variants for better recall
    const doExpand = options?.expandQueries !== false;
    const queries = doExpand ? this.expandQuery(query) : [query];

    // 1. FTS5 search — across all query variants
    const allFtsResults: Fact[] = [];
    const seenFtsIds = new Set<string>();
    for (const q of queries) {
      const results = this.db.searchFacts(q, limit * 2);
      for (const f of results) {
        if (!seenFtsIds.has(f.id)) {
          seenFtsIds.add(f.id);
          allFtsResults.push(f);
        }
      }
    }

    // 2. Semantic search — across all query variants
    let allCosResults: EmbeddedFact[] = [];
    const seenCosIds = new Set<string>();
    for (const q of queries) {
      try {
        const results = await this.semanticSearch(q, limit * 2, minSim);
        for (const f of results) {
          if (!seenCosIds.has(f.id)) {
            seenCosIds.add(f.id);
            allCosResults.push(f);
          } else {
            // Keep highest similarity
            const existing = allCosResults.find(r => r.id === f.id);
            if (existing && f.similarity > existing.similarity) {
              existing.similarity = f.similarity;
            }
          }
        }
      } catch (e) {
        console.debug('memoria:embeddings: ' + String(e));
        // Embedding not available → FTS only
      }
    }

    // 3. Merge by fact ID
    const merged = new Map<string, EmbeddedFact>();

    // Add FTS results with rank-based score
    for (let i = 0; i < allFtsResults.length; i++) {
      const f = allFtsResults[i];
      const ftsScore = 1 - i / Math.max(allFtsResults.length, 1); // 1.0 for best, decreasing
      const sf = scoreFact(f);
      merged.set(f.id, {
        ...f,
        similarity: 0,
        temporalScore: sf.temporalScore,
        hybridScore: ftsScore * ftsW + sf.temporalScore * tempW,
      });
    }

    // Merge cosine results
    for (const cr of allCosResults) {
      const existing = merged.get(cr.id);
      if (existing) {
        // Boost: fact found by BOTH methods
        existing.similarity = cr.similarity;
        existing.hybridScore += cr.similarity * cosW;
      } else {
        const sf = scoreFact(cr);
        merged.set(cr.id, {
          ...cr,
          temporalScore: sf.temporalScore,
          hybridScore: cr.similarity * cosW + sf.temporalScore * tempW,
        });
      }
    }

    // 4. Sort by hybrid score, return top N
    const results = Array.from(merged.values());
    results.sort((a, b) => b.hybridScore - a.hybridScore);
    return results.slice(0, limit);
  }

  // ─── Stats ───

  /** Count of embedded facts */
  /**
   * Called when a fact is superseded — remove its embedding to prevent
   * stale results in semantic search.
   */
  onFactSuperseded(factId: string): boolean {
    try {
      const result = this.db.raw.prepare("DELETE FROM embeddings WHERE fact_id = ?").run(factId);
      return (result.changes ?? 0) > 0;
    } catch (e) { console.debug('memoria:embeddings: ' + String(e)); return false; }
  }

  embeddedCount(): number {
    return (this.rawDb.prepare("SELECT COUNT(*) as c FROM embeddings").get() as { c: number }).c;
  }

  /** Facts without embeddings */
  unembeddedFacts(limit = 100): Array<{ id: string; fact: string }> {
    return this.rawDb.prepare(`
      SELECT f.id, f.fact FROM facts f
      LEFT JOIN embeddings e ON f.id = e.fact_id
      WHERE e.fact_id IS NULL AND f.superseded = 0
      ORDER BY f.created_at DESC
      LIMIT ?
    `).all(limit) as Array<{ id: string; fact: string }>;
  }
}
