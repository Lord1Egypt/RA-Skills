/**
 * Memoria — Layer 9: Observations
 * 
 * Living syntheses that evolve as new evidence appears.
 * Instead of 10 scattered facts about "Bureau deploy",
 * UNE observation cohérente qui se met à jour.
 *
 * Cycle de vie:
 *   1. Nouveau fait capturé
 *   2. Cherche observations liées (embedding similarity)
 *   3. Si trouvée → re-synthétise avec le nouveau fait
 *   4. Si pas trouvée → accumule, quand 3+ faits partagent un topic → crée observation
 *   5. Recall injecte observations EN PRIORITÉ, faits individuels en complément
 */

import type { MemoriaDB, Fact } from "./db.js";
import type { LLMProvider } from "./providers/types.js";
import type { EmbedProvider } from "./providers/types.js";

// ─── Schema ───

export interface Observation {
  id: string;
  topic: string;
  summary: string;
  evidence_ids: string;   // JSON array of fact IDs
  revision: number;
  confidence: number;
  created_at: number;
  updated_at: number;
  last_accessed_at: number | null;
  access_count: number;
  embedding: Float32Array | null;
}

export interface ObservationConfig {
  /** Min facts sharing a topic before creating an observation. Default 3 */
  emergenceThreshold: number;
  /** Cosine similarity threshold to match a fact to an observation. Default 0.6 */
  matchThreshold: number;
  /** Max observations to inject in recall. Default 5 */
  maxRecallObservations: number;
  /** Max evidence facts per observation before pruning old ones. Default 15 */
  maxEvidencePerObservation: number;
}

export const DEFAULT_OBS_CONFIG: ObservationConfig = {
  emergenceThreshold: 3,
  matchThreshold: 0.6,
  maxRecallObservations: 5,
  maxEvidencePerObservation: 15,
};

// ─── Prompts ───

const SYNTHESIZE_PROMPT = `Tu synthétises des faits en UNE observation cohérente.
Combine ces faits en un paragraphe concis (2-4 phrases max) qui capture l'état actuel.
Si un fait contredit un autre, garde le plus récent.
Le résultat doit être autonome (compréhensible sans les faits originaux).

Topic: "{TOPIC}"

Faits (du plus ancien au plus récent):
{FACTS}

Réponds UNIQUEMENT avec le texte de l'observation (pas de JSON, pas de préfixe).`;

const UPDATE_PROMPT = `Mets à jour cette observation avec un nouveau fait.
Si le nouveau fait contredit l'observation, corrige-la.
Si il la complète, intègre-le.
Si il est redondant, garde l'observation telle quelle.

Observation actuelle:
"{CURRENT}"

Nouveau fait:
"{NEW_FACT}"

Réponds UNIQUEMENT avec le texte de l'observation mise à jour (pas de JSON, pas de préfixe).`;

const TOPIC_EXTRACT_PROMPT = `Quel est le sujet principal de ce fait ? Réponds en 2-4 mots maximum (le topic).
Exemples: "Sol infrastructure", "Memoria config", "Bureau CRM", "Neto préférences", "API Twitter"

Fait: "{FACT}"

Topic:`;

// ─── Main class ───

export class ObservationManager {
  private db: MemoriaDB;
  private llm: LLMProvider;
  private embedder: EmbedProvider | null;
  private cfg: ObservationConfig;

  constructor(db: MemoriaDB, llm: LLMProvider, embedder: EmbedProvider | null, config?: Partial<ObservationConfig>) {
    this.db = db;
    this.llm = llm;
    this.embedder = embedder;
    this.cfg = { ...DEFAULT_OBS_CONFIG, ...config };
    this.ensureSchema();
  }

  // ─── Schema ───

  private ensureSchema(): void {
    this.db.raw.exec(`
      CREATE TABLE IF NOT EXISTS observations (
        id TEXT PRIMARY KEY,
        topic TEXT NOT NULL,
        summary TEXT NOT NULL,
        evidence_ids TEXT DEFAULT '[]',
        revision INTEGER DEFAULT 1,
        confidence REAL DEFAULT 0.8,
        created_at INTEGER NOT NULL,
        updated_at INTEGER NOT NULL,
        last_accessed_at INTEGER,
        access_count INTEGER DEFAULT 0,
        embedding BLOB
      );
      CREATE INDEX IF NOT EXISTS idx_obs_topic ON observations(topic);
      CREATE INDEX IF NOT EXISTS idx_obs_updated ON observations(updated_at);
    `);
  }

  // ─── Core: process a new fact ───

  async onFactCaptured(factId: string, factText: string, category: string): Promise<{
    action: "updated_observation" | "created_observation" | "accumulated" | "skipped";
    observationId?: string;
  }> {
    try {
      // 1. Find matching observation by embedding similarity
      const matched = await this.findMatchingObservation(factText);
      
      if (matched) {
        // Update existing observation with new fact
        await this.updateObservation(matched.id, factId, factText);
        return { action: "updated_observation", observationId: matched.id };
      }

      // 2. Extract topic from fact
      const topic = await this.extractTopic(factText);
      if (!topic) return { action: "skipped" };

      // 3. Check if enough facts share this topic to create an observation
      const relatedFacts = this.findFactsByTopic(topic);
      if (relatedFacts.length >= this.cfg.emergenceThreshold - 1) {
        // +1 for the current fact = threshold met
        const obsId = await this.createObservation(topic, [...relatedFacts, { id: factId, fact: factText, category }]);
        return { action: "created_observation", observationId: obsId };
      }

      return { action: "accumulated" };
    } catch (e) {
      console.debug('memoria:observations: ' + String(e));
      return { action: "skipped" };
    }
  }

  // ─── Find matching observation ───

  private async findMatchingObservation(factText: string): Promise<Observation | null> {
    if (!this.embedder) {
      // Fallback: keyword matching
      return this.findByKeywords(factText);
    }

    try {
      const factEmb = await this.embedder.embed(factText);
      const allObs = this.getAllObservations();
      
      let best: Observation | null = null;
      let bestSim = 0;

      for (const obs of allObs) {
        if (!obs.embedding) continue;
        const sim = cosineSimilarity(new Float32Array(factEmb), new Float32Array(obs.embedding));
        if (sim > bestSim && sim >= this.cfg.matchThreshold) {
          bestSim = sim;
          best = obs;
        }
      }

      return best;
    } catch (e) {
      console.debug('memoria:observations: ' + String(e));
      return this.findByKeywords(factText);
    }
  }

  private findByKeywords(factText: string): Observation | null {
    const words = factText.toLowerCase().split(/\s+/).filter(w => w.length > 3);
    const allObs = this.getAllObservations();
    
    let best: Observation | null = null;
    let bestOverlap = 0;

    for (const obs of allObs) {
      const obsWords = new Set(obs.summary.toLowerCase().split(/\s+/).filter(w => w.length > 3));
      let overlap = 0;
      for (const w of words) if (obsWords.has(w)) overlap++;
      const ratio = overlap / Math.max(words.length, 1);
      if (ratio > bestOverlap && ratio >= 0.3) {
        bestOverlap = ratio;
        best = obs;
      }
    }
    return best;
  }

  // ─── Update observation ───

  private async updateObservation(obsId: string, newFactId: string, newFactText: string): Promise<void> {
    const obs = this.getObservation(obsId);
    if (!obs) return;

    // Add fact to evidence
    const evidenceIds: string[] = JSON.parse(obs.evidence_ids || "[]");
    if (!evidenceIds.includes(newFactId)) {
      evidenceIds.push(newFactId);
      // Prune old evidence if too many
      if (evidenceIds.length > this.cfg.maxEvidencePerObservation) {
        evidenceIds.splice(0, evidenceIds.length - this.cfg.maxEvidencePerObservation);
      }
    }

    // Re-synthesize
    let newSummary: string;
    try {
      const prompt = UPDATE_PROMPT
        .replace("{CURRENT}", obs.summary)
        .replace("{NEW_FACT}", newFactText);
      newSummary = (await this.llm.generate(prompt, {
        maxTokens: 300,
        temperature: 0.2,
        timeoutMs: 15000,
      })).trim();
      
      if (newSummary.length < 10) newSummary = obs.summary; // LLM returned garbage
    } catch (e) {
      console.debug('memoria:observations: ' + String(e));
      // LLM failed — just append fact reference, keep old summary
      newSummary = obs.summary;
    }

    // Update embedding
    let embedding: Buffer | null = null;
    if (this.embedder) {
      try {
        const emb = await this.embedder.embed(newSummary);
        embedding = Buffer.from(new Float32Array(emb).buffer);
      } catch (e) { console.debug('memoria:observations: ' + String(e)); }
    }

    const now = Date.now();
    this.db.raw.prepare(`
      UPDATE observations SET 
        summary = ?, evidence_ids = ?, revision = revision + 1,
        updated_at = ?, embedding = COALESCE(?, embedding)
      WHERE id = ?
    `).run(newSummary, JSON.stringify(evidenceIds), now, embedding, obsId);
  }

  // ─── Create observation ───

  private async createObservation(topic: string, facts: Array<{ id: string; fact: string; category: string }>): Promise<string> {
    const factsText = facts.map((f, i) => `${i + 1}. ${f.fact}`).join("\n");
    
    let summary: string;
    try {
      const prompt = SYNTHESIZE_PROMPT
        .replace("{TOPIC}", topic)
        .replace("{FACTS}", factsText);
      summary = (await this.llm.generate(prompt, {
        maxTokens: 300,
        temperature: 0.2,
        timeoutMs: 15000,
      })).trim();
      
      if (summary.length < 10) {
        // LLM returned garbage — use concat fallback
        summary = facts.map(f => f.fact).join(". ");
      }
    } catch (e) {
      console.debug('memoria:observations: ' + String(e));
      summary = facts.map(f => f.fact).join(". ");
    }

    const id = `obs_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`;
    const evidenceIds = facts.map(f => f.id);
    const now = Date.now();
    const avgConfidence = 0.8;

    // Embed the observation
    let embedding: Buffer | null = null;
    if (this.embedder) {
      try {
        const emb = await this.embedder.embed(summary);
        embedding = Buffer.from(new Float32Array(emb).buffer);
      } catch (e) { console.debug('memoria:observations: ' + String(e)); }
    }

    this.db.raw.prepare(`
      INSERT INTO observations (id, topic, summary, evidence_ids, revision, confidence, created_at, updated_at, access_count, embedding)
      VALUES (?, ?, ?, ?, 1, ?, ?, ?, 0, ?)
    `).run(id, topic, summary, JSON.stringify(evidenceIds), avgConfidence, now, now, embedding);

    return id;
  }

  // ─── Topic extraction ───

  private async extractTopic(factText: string): Promise<string | null> {
    try {
      const prompt = TOPIC_EXTRACT_PROMPT.replace("{FACT}", factText);
      const response = (await this.llm.generate(prompt, {
        maxTokens: 20,
        temperature: 0.1,
        timeoutMs: 10000,
      })).trim();
      
      // Clean up: remove quotes, "Topic:", etc.
      const cleaned = response.replace(/^["']|["']$/g, "").replace(/^topic:\s*/i, "").trim();
      return cleaned.length > 1 && cleaned.length < 60 ? cleaned : null;
    } catch (e) {
      console.debug('memoria:observations: ' + String(e));
      return null;
    }
  }

  // ─── Find facts by topic (keyword overlap with topic name) ───

  private findFactsByTopic(topic: string): Array<{ id: string; fact: string; category: string }> {
    const topicWords = topic.toLowerCase().split(/\s+/).filter(w => w.length > 2);
    if (topicWords.length === 0) return [];

    // Use FTS5 to find candidate facts
    const query = topicWords.map(w => `"${w}"`).join(" OR ");
    try {
      const results = this.db.raw.prepare(`
        SELECT f.id, f.fact, f.category FROM facts f
        JOIN facts_fts fts ON f.rowid = fts.rowid
        WHERE facts_fts MATCH ? AND f.superseded = 0
        ORDER BY rank LIMIT 20
      `).all(query) as Array<{ id: string; fact: string; category: string }>;
      return results;
    } catch (e) {
      console.debug('memoria:observations: ' + String(e));
      return [];
    }
  }

  // ─── Recall: get relevant observations ───

  async getRelevantObservations(query: string, limit?: number): Promise<Array<{ observation: Observation; score: number }>> {
    const maxObs = limit || this.cfg.maxRecallObservations;
    const allObs = this.getAllObservations();
    if (allObs.length === 0) return [];

    // Score by embedding similarity if available
    if (this.embedder) {
      try {
        const queryEmb = await this.embedder.embed(query);
        const scored = allObs
          .filter(o => o.embedding)
          .map(o => ({
            observation: o,
            score: cosineSimilarity(new Float32Array(queryEmb), new Float32Array(o.embedding!)),
          }))
          .filter(s => s.score >= 0.3)
          .sort((a, b) => b.score - a.score)
          .slice(0, maxObs);
        
        // Track access
        for (const s of scored) this.trackAccess(s.observation.id);
        return scored;
      } catch (e) { console.debug('memoria:observations: ' + String(e)); }
    }

    // Fallback: keyword matching
    const queryWords = new Set(query.toLowerCase().split(/\s+/).filter(w => w.length > 3));
    const scored = allObs.map(o => {
      const obsWords = o.summary.toLowerCase().split(/\s+/).filter(w => w.length > 3);
      let overlap = 0;
      for (const w of obsWords) if (queryWords.has(w)) overlap++;
      return { observation: o, score: overlap / Math.max(queryWords.size, 1) };
    })
    .filter(s => s.score > 0.1)
    .sort((a, b) => b.score - a.score)
    .slice(0, maxObs);

    for (const s of scored) this.trackAccess(s.observation.id);
    return scored;
  }

  // ─── Format for injection ───

  formatForRecall(observations: Array<{ observation: Observation; score: number }>): string {
    if (observations.length === 0) return "";
    const lines = observations.map(({ observation: o }) => {
      const evidenceCount = JSON.parse(o.evidence_ids || "[]").length;
      const revNote = o.revision > 1 ? ` (rev.${o.revision})` : "";
      return `- 🔮 **${o.topic}**${revNote}: ${o.summary} [${evidenceCount} sources]`;
    });
    return lines.join("\n");
  }

  // ─── Helpers ───

  private getAllObservations(): Observation[] {
    const rows = this.db.raw.prepare("SELECT * FROM observations ORDER BY updated_at DESC").all() as any[];
    return rows.map(r => ({
      ...r,
      embedding: r.embedding ? new Float32Array(r.embedding.buffer, r.embedding.byteOffset, r.embedding.byteLength / 4) : null,
    }));
  }

  private getObservation(id: string): Observation | null {
    const row = this.db.raw.prepare("SELECT * FROM observations WHERE id = ?").get(id) as any;
    if (!row) return null;
    return {
      ...row,
      embedding: row.embedding ? new Float32Array(row.embedding.buffer, row.embedding.byteOffset, row.embedding.byteLength / 4) : null,
    };
  }

  private trackAccess(id: string): void {
    const now = Date.now();
    this.db.raw.prepare("UPDATE observations SET access_count = access_count + 1, last_accessed_at = ? WHERE id = ?").run(now, id);
  }

  /** 
   * Called when a fact is superseded — remove it from evidence lists
   * and flag affected observations for re-synthesis on next access.
   */
  onFactSuperseded(factId: string): number {
    let affected = 0;
    try {
      const allObs = this.db.raw.prepare(
        "SELECT id, evidence_ids FROM observations"
      ).all() as Array<{ id: string; evidence_ids: string }>;

      for (const obs of allObs) {
        const evidenceIds: string[] = JSON.parse(obs.evidence_ids || "[]");
        if (evidenceIds.includes(factId)) {
          // Remove the superseded fact from evidence
          const updated = evidenceIds.filter(id => id !== factId);
          
          if (updated.length === 0) {
            // No evidence left → delete the observation
            this.db.raw.prepare("DELETE FROM observations WHERE id = ?").run(obs.id);
          } else {
            // Mark as needing re-synthesis (bump revision to signal staleness)
            this.db.raw.prepare(
              "UPDATE observations SET evidence_ids = ?, updated_at = ? WHERE id = ?"
            ).run(JSON.stringify(updated), Date.now(), obs.id);
          }
          affected++;
        }
      }
    } catch (e) { console.debug('memoria:observations: ' + String(e)); }
    return affected;
  }

  stats(): { total: number; avgRevision: number; avgEvidence: number } {
    const total = (this.db.raw.prepare("SELECT COUNT(*) as c FROM observations").get() as any)?.c || 0;
    if (total === 0) return { total: 0, avgRevision: 0, avgEvidence: 0 };
    const avgRev = (this.db.raw.prepare("SELECT AVG(revision) as a FROM observations").get() as any)?.a || 0;
    const rows = this.db.raw.prepare("SELECT evidence_ids FROM observations").all() as any[];
    const avgEvidence = rows.reduce((sum, r) => sum + JSON.parse(r.evidence_ids || "[]").length, 0) / total;
    return { total, avgRevision: Math.round(avgRev * 10) / 10, avgEvidence: Math.round(avgEvidence * 10) / 10 };
  }
}

// ─── Cosine Similarity ───

function cosineSimilarity(a: Float32Array, b: Float32Array): number {
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
