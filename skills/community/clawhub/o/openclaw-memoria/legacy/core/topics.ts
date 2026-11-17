/**
 * topics.ts — Phase 8: Emergent Topics
 *
 * Topics emerge automatically from repeated patterns in facts.
 * No manual categories — everything comes from usage.
 *
 * Flow:
 *   1. After capture: extract keywords → match/create topic associations
 *   2. Periodically: scan orphans, merge, create sub-topics
 *   3. At recall: topic embeddings enrich search results
 */

import type { LLMProvider, EmbedProvider } from "./providers/types.js";
import type { MemoriaDB } from "./db.js";

// ─── Types ───

export interface Topic {
  id: string;
  name: string;
  keywords: string[];
  fact_count: number;
  first_seen: number;
  last_seen: number;
  access_count: number;
  importance_score: number;
  parent_topic_id: string | null;
  embedding: number[] | null;
}

export interface TopicMatch {
  topic: Topic;
  overlap: number; // 0-1
}

export interface TopicsConfig {
  emergenceThreshold: number;    // min facts to create topic (default: 3)
  mergeOverlap: number;          // keyword overlap to merge (default: 0.7)
  subtopicThreshold: number;     // min facts for sub-topic (default: 5)
  decayDays: number;             // days before decay starts (default: 30)
  scanInterval: number;          // scan orphans every N captures (default: 15)
  maxKeywordsPerFact: number;    // keywords extracted per fact (default: 5)
}

const DEFAULT_CONFIG: TopicsConfig = {
  emergenceThreshold: 3,
  mergeOverlap: 0.7,
  subtopicThreshold: 5,
  decayDays: 30,
  scanInterval: 15,
  maxKeywordsPerFact: 5,
};

// ─── Schema Migration ───

export function migrateTopicsSchema(db: MemoriaDB): void {
  const raw = db.raw;

  raw.exec(`
    CREATE TABLE IF NOT EXISTS topics (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      keywords TEXT DEFAULT '[]',
      fact_count INTEGER DEFAULT 0,
      first_seen INTEGER NOT NULL,
      last_seen INTEGER NOT NULL,
      access_count INTEGER DEFAULT 0,
      importance_score REAL DEFAULT 0.0,
      parent_topic_id TEXT,
      embedding BLOB,
      FOREIGN KEY (parent_topic_id) REFERENCES topics(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS fact_topics (
      fact_id TEXT NOT NULL,
      topic_id TEXT NOT NULL,
      PRIMARY KEY (fact_id, topic_id),
      FOREIGN KEY (fact_id) REFERENCES facts(id) ON DELETE CASCADE,
      FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_fact_topics_topic ON fact_topics(topic_id);
    CREATE INDEX IF NOT EXISTS idx_topics_importance ON topics(importance_score DESC);
    CREATE INDEX IF NOT EXISTS idx_topics_parent ON topics(parent_topic_id);
  `);
}

// ─── Helper: generate ID ───

function genId(): string {
  return `topic_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 8)}`;
}

// ─── Keyword Extraction Prompt ───

const KEYWORD_PROMPT = `Extrais les mots-clés principaux de ce fait. Ce sont des concepts, noms propres, ou thèmes durables.

Règles :
- Maximum {MAX} mots-clés
- Mots-clés en minuscules, français ou anglais technique
- Pas de mots vides (le, la, de, est, un, etc.)
- Pas de verbes conjugués
- Privilégier les noms propres et concepts techniques

Fait : "{FACT}"

Réponds UNIQUEMENT en JSON : {"keywords": ["mot1", "mot2"]}`;

// ─── Main Class ───

export class TopicManager {
  private db: MemoriaDB;
  private llm: LLMProvider;
  private embedder: EmbedProvider | null;
  private cfg: TopicsConfig;
  private capturesSinceLastScan: number = 0;

  constructor(db: MemoriaDB, llm: LLMProvider, embedder: EmbedProvider | null, config?: Partial<TopicsConfig>) {
    this.db = db;
    this.llm = llm;
    this.embedder = embedder;
    this.cfg = { ...DEFAULT_CONFIG, ...config };

    // Ensure schema
    migrateTopicsSchema(db);
  }

  // ─── 1. Extract keywords from a fact ───

  async extractKeywords(fact: string): Promise<string[]> {
    try {
      const prompt = KEYWORD_PROMPT
        .replace("{MAX}", String(this.cfg.maxKeywordsPerFact))
        .replace("{FACT}", fact.slice(0, 500));

      const response = await this.llm.generate(prompt, {
        maxTokens: 128,
        temperature: 0.1,
        format: "json",
        timeoutMs: 10000,
      });

      const parsed = this.parseJSON(response) as { keywords?: string[] };
      if (!parsed?.keywords || !Array.isArray(parsed.keywords)) return [];

      return parsed.keywords
        .filter((k: unknown) => typeof k === "string" && k.length > 1 && k.length < 50)
        .map((k: string) => k.toLowerCase().trim())
        .slice(0, this.cfg.maxKeywordsPerFact);
    } catch (e) {
      console.debug('memoria:topics: ' + String(e));
      return [];
    }
  }

  // ─── 2. After capture: tag fact + associate with topics ───

  async onFactCaptured(factId: string, fact: string, category: string): Promise<{ keywords: string[]; topics: string[] }> {
    // Extract keywords
    const keywords = await this.extractKeywords(fact);
    if (keywords.length === 0) return { keywords: [], topics: [] };

    // Update fact tags
    const raw = this.db.raw;
    raw.prepare("UPDATE facts SET tags = ? WHERE id = ?")
      .run(JSON.stringify(keywords), factId);

    // Rebuild FTS for this fact
    try {
      const rowid = raw.prepare("SELECT rowid FROM facts WHERE id = ?").get(factId) as { rowid: number } | undefined;
      if (rowid) {
        raw.prepare("INSERT OR REPLACE INTO facts_fts(rowid, fact, category, tags) VALUES (?, (SELECT fact FROM facts WHERE rowid = ?), (SELECT category FROM facts WHERE rowid = ?), ?)").run(
          rowid.rowid, rowid.rowid, rowid.rowid, JSON.stringify(keywords),
        );
      }
    } catch (e) { console.debug('memoria:topics: ' + String(e)); }

    // Find matching topics
    const matchedTopics = this.findMatchingTopics(keywords);
    const topicNames: string[] = [];

    for (const match of matchedTopics) {
      // Associate fact with topic
      raw.prepare("INSERT OR IGNORE INTO fact_topics (fact_id, topic_id) VALUES (?, ?)")
        .run(factId, match.topic.id);

      // Update topic stats
      const now = Date.now();
      raw.prepare(`UPDATE topics SET 
        fact_count = fact_count + 1,
        last_seen = ?,
        importance_score = (fact_count + 1) * (1.0 + ? / (? + 86400000.0 * ?))
        WHERE id = ?`)
        .run(now, now, now, this.cfg.decayDays, match.topic.id);

      // Merge keywords
      const existing: string[] = JSON.parse(match.topic.keywords as unknown as string || "[]");
      const merged = [...new Set([...existing, ...keywords])];
      raw.prepare("UPDATE topics SET keywords = ? WHERE id = ?")
        .run(JSON.stringify(merged), match.topic.id);

      topicNames.push(match.topic.name);
    }

    // Track for periodic scan
    this.capturesSinceLastScan++;

    return { keywords, topics: topicNames };
  }

  // ─── 3. Find topics matching keywords ───

  findMatchingTopics(keywords: string[]): TopicMatch[] {
    if (keywords.length === 0) return [];

    const raw = this.db.raw;
    const allTopics = raw.prepare("SELECT * FROM topics WHERE parent_topic_id IS NULL OR parent_topic_id = ''").all() as Topic[];

    const matches: TopicMatch[] = [];
    for (const topic of allTopics) {
      const topicKw: string[] = JSON.parse(topic.keywords as unknown as string || "[]");
      if (topicKw.length === 0) continue;

      const overlap = this.jaccardOverlap(keywords, topicKw);
      if (overlap >= 0.25) { // Lower threshold for matching (vs merge)
        matches.push({ topic, overlap });
      }
    }

    return matches.sort((a, b) => b.overlap - a.overlap);
  }

  // ─── 4. Periodic scan: create topics from orphans ───

  async scanAndEmerge(): Promise<{ created: number; merged: number; subtopics: number }> {
    this.capturesSinceLastScan = 0;
    const raw = this.db.raw;
    let created = 0;
    let merged = 0;
    let subtopics = 0;

    // Find orphan facts (have tags but no topic)
    const orphans = raw.prepare(`
      SELECT f.id, f.fact, f.tags, f.category
      FROM facts f
      WHERE f.superseded = 0
        AND f.tags != '[]'
        AND f.tags IS NOT NULL
        AND f.id NOT IN (SELECT fact_id FROM fact_topics)
    `).all() as Array<{ id: string; fact: string; tags: string; category: string }>;

    // Count keyword frequency among orphans
    const kwCount = new Map<string, string[]>(); // keyword → [factId, ...]
    for (const orphan of orphans) {
      const tags: string[] = JSON.parse(orphan.tags || "[]");
      for (const kw of tags) {
        const existing = kwCount.get(kw) || [];
        existing.push(orphan.id);
        kwCount.set(kw, existing);
      }
    }

    // Find clusters (keywords appearing in >= threshold facts)
    const clusters: Array<{ keyword: string; factIds: string[] }> = [];
    for (const [kw, factIds] of kwCount.entries()) {
      if (factIds.length >= this.cfg.emergenceThreshold) {
        clusters.push({ keyword: kw, factIds: [...new Set(factIds)] });
      }
    }

    // Merge overlapping clusters
    const mergedClusters = this.mergeClusters(clusters);

    // Create topics from clusters
    for (const cluster of mergedClusters) {
      // Check if a similar topic already exists
      const existing = this.findMatchingTopics(cluster.keywords);
      if (existing.length > 0 && existing[0].overlap > 0.5) {
        // Associate orphans with existing topic instead
        for (const fid of cluster.factIds) {
          raw.prepare("INSERT OR IGNORE INTO fact_topics (fact_id, topic_id) VALUES (?, ?)")
            .run(fid, existing[0].topic.id);
        }
        raw.prepare("UPDATE topics SET fact_count = fact_count + ? WHERE id = ?")
          .run(cluster.factIds.length, existing[0].topic.id);
        continue;
      }

      // Generate topic name via LLM
      const name = await this.generateTopicName(cluster.keywords, cluster.factIds);
      const now = Date.now();
      const topicId = genId();

      // Find potential parent topic by keyword overlap or name inclusion
      const parentId = this.findParentTopic(name, cluster.keywords);

      raw.prepare(`INSERT INTO topics (id, name, keywords, fact_count, first_seen, last_seen, importance_score, parent_topic_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)`).run(
        topicId, name, JSON.stringify(cluster.keywords),
        cluster.factIds.length, now, now,
        cluster.factIds.length * 1.0, parentId, // initial importance + parent
      );

      // Link facts
      for (const fid of cluster.factIds) {
        raw.prepare("INSERT OR IGNORE INTO fact_topics (fact_id, topic_id) VALUES (?, ?)")
          .run(fid, topicId);
      }

      // Register topic as entity in knowledge graph
      try {
        raw.prepare(`INSERT OR IGNORE INTO entities (id, name, type, created_at)
          VALUES (?, ?, 'topic', ?)`).run(topicId, name, now);
      } catch (e) { console.debug('memoria:topics: ' + String(e)); }

      created++;
    }

    // ─── Sub-topics ───
    const topLevelTopics = raw.prepare("SELECT * FROM topics WHERE parent_topic_id IS NULL OR parent_topic_id = ''").all() as Topic[];
    for (const topic of topLevelTopics) {
      if (topic.fact_count < this.cfg.subtopicThreshold * 2) continue; // Need enough facts

      const factIds = raw.prepare("SELECT fact_id FROM fact_topics WHERE topic_id = ?")
        .all(topic.id) as Array<{ fact_id: string }>;

      // Get keywords per fact within this topic
      const subKwCount = new Map<string, string[]>();
      for (const { fact_id } of factIds) {
        const f = raw.prepare("SELECT tags FROM facts WHERE id = ?").get(fact_id) as { tags: string } | undefined;
        if (!f) continue;
        const tags: string[] = JSON.parse(f.tags || "[]");
        for (const kw of tags) {
          const existing = subKwCount.get(kw) || [];
          existing.push(fact_id);
          subKwCount.set(kw, existing);
        }
      }

      // Find sub-clusters within this topic
      for (const [kw, fids] of subKwCount.entries()) {
        if (fids.length < this.cfg.subtopicThreshold) continue;
        // Don't create sub-topic if it's the same as the parent's main keywords
        const parentKw: string[] = JSON.parse(topic.keywords as unknown as string || "[]");
        if (parentKw.includes(kw)) continue;

        // Check if sub-topic already exists
        const existingSub = raw.prepare("SELECT id FROM topics WHERE parent_topic_id = ? AND keywords LIKE ?")
          .get(topic.id, `%"${kw}"%`) as { id: string } | undefined;
        if (existingSub) continue;

        const name = await this.generateTopicName([kw], fids.slice(0, 3));
        const now = Date.now();
        const subId = genId();

        raw.prepare(`INSERT INTO topics (id, name, keywords, fact_count, first_seen, last_seen, importance_score, parent_topic_id)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?)`).run(
          subId, name, JSON.stringify([kw]),
          fids.length, now, now, fids.length * 0.8, topic.id,
        );

        for (const fid of fids) {
          raw.prepare("INSERT OR IGNORE INTO fact_topics (fact_id, topic_id) VALUES (?, ?)")
            .run(fid, subId);
        }

        subtopics++;
      }
    }

    // ─── Merge similar topics ───
    merged = await this.mergeTopics();

    // ─── Update embeddings for all topics ───
    await this.updateTopicEmbeddings();

    // ─── Apply decay ───
    this.applyDecay();

    return { created, merged, subtopics };
  }

  // ─── 5. Merge overlapping topics ───

  private async mergeTopics(): Promise<number> {
    const raw = this.db.raw;
    const topics = raw.prepare("SELECT * FROM topics WHERE parent_topic_id IS NULL OR parent_topic_id = ''")
      .all() as Topic[];

    let mergeCount = 0;
    const toDelete = new Set<string>();

    for (let i = 0; i < topics.length; i++) {
      if (toDelete.has(topics[i].id)) continue;
      for (let j = i + 1; j < topics.length; j++) {
        if (toDelete.has(topics[j].id)) continue;

        const kw1: string[] = JSON.parse(topics[i].keywords as unknown as string || "[]");
        const kw2: string[] = JSON.parse(topics[j].keywords as unknown as string || "[]");
        const overlap = this.jaccardOverlap(kw1, kw2);

        if (overlap >= this.cfg.mergeOverlap) {
          // Merge j into i (keep the one with more facts)
          const [keep, remove] = topics[i].fact_count >= topics[j].fact_count
            ? [topics[i], topics[j]]
            : [topics[j], topics[i]];

          // Transfer facts
          raw.prepare("UPDATE fact_topics SET topic_id = ? WHERE topic_id = ?")
            .run(keep.id, remove.id);

          // Merge keywords
          const merged = [...new Set([...kw1, ...kw2])];
          raw.prepare("UPDATE topics SET keywords = ?, fact_count = fact_count + ? WHERE id = ?")
            .run(JSON.stringify(merged), remove.fact_count, keep.id);

          // Delete merged topic
          raw.prepare("DELETE FROM topics WHERE id = ?").run(remove.id);
          toDelete.add(remove.id);
          mergeCount++;
        }
      }
    }

    return mergeCount;
  }

  // ─── 6. Update topic embeddings ───

  async updateTopicEmbeddings(): Promise<number> {
    if (!this.embedder) return 0;

    const raw = this.db.raw;
    const topics = raw.prepare("SELECT * FROM topics").all() as Topic[];
    let updated = 0;

    for (const topic of topics) {
      // Get all fact embeddings for this topic
      const factEmbeddings = raw.prepare(`
        SELECT e.vector FROM embeddings e
        JOIN fact_topics ft ON ft.fact_id = e.fact_id
        WHERE ft.topic_id = ?
      `).all(topic.id) as Array<{ vector: Buffer }>;

      if (factEmbeddings.length === 0) continue;

      // Compute mean embedding
      const dims = factEmbeddings[0].vector.length / 4; // Float32
      const mean = new Float32Array(dims);

      for (const { vector } of factEmbeddings) {
        const arr = new Float32Array(vector.buffer, vector.byteOffset, dims);
        for (let d = 0; d < dims; d++) mean[d] += arr[d];
      }
      for (let d = 0; d < dims; d++) mean[d] /= factEmbeddings.length;

      // Normalize
      let norm = 0;
      for (let d = 0; d < dims; d++) norm += mean[d] * mean[d];
      norm = Math.sqrt(norm);
      if (norm > 0) for (let d = 0; d < dims; d++) mean[d] /= norm;

      // Store
      raw.prepare("UPDATE topics SET embedding = ? WHERE id = ?")
        .run(Buffer.from(mean.buffer), topic.id);

      updated++;
    }

    return updated;
  }

  // ─── 7. Recall: find relevant topics for a query ───

  async findRelevantTopics(query: string, limit = 5, expandedQueries?: string[]): Promise<Array<{ topic: Topic; score: number; facts: string[] }>> {
    const raw = this.db.raw;
    const results: Array<{ topic: Topic; score: number; facts: string[] }> = [];

    // Strategy 1: Keyword matching — use expanded queries if available
    const allQueries = expandedQueries && expandedQueries.length > 0 ? expandedQueries : [query];
    const queryWords = new Set<string>();
    for (const q of allQueries) {
      for (const w of q.toLowerCase().split(/\s+/).filter(w => w.length > 2)) {
        queryWords.add(w);
      }
    }
    const allTopics = raw.prepare("SELECT * FROM topics ORDER BY importance_score DESC").all() as Topic[];

    for (const topic of allTopics) {
      const kw: string[] = JSON.parse(topic.keywords as unknown as string || "[]");
      let keywordScore = 0;

      for (const qw of queryWords) {
        if (kw.some(k => k.includes(qw) || qw.includes(k))) keywordScore += 1;
        if (topic.name.toLowerCase().includes(qw)) keywordScore += 2;
      }
      // Bonus: topic name exact match with any expanded query
      const topicLower = topic.name.toLowerCase();
      for (const q of allQueries) {
        if (q.toLowerCase().includes(topicLower) || topicLower.includes(q.toLowerCase())) {
          keywordScore += 3;
          break;
        }
      }

      if (keywordScore > 0) {
        // Boost by importance and recency
        const recencyBoost = Math.exp(-(Date.now() - topic.last_seen) / (86400000 * 14));
        const score = keywordScore * (0.5 + topic.importance_score * 0.3 + recencyBoost * 0.2);

        const factRows = raw.prepare(
          "SELECT f.fact FROM facts f JOIN fact_topics ft ON ft.fact_id = f.id WHERE ft.topic_id = ? AND f.superseded = 0 ORDER BY f.created_at DESC LIMIT 10"
        ).all(topic.id) as Array<{ fact: string }>;

        results.push({ topic, score, facts: factRows.map(r => r.fact) });
      }
    }

    // Strategy 2: Semantic (embedding) matching
    if (this.embedder) {
      try {
        const queryEmb = await this.embedder.embed(query);
        const topicsWithEmb = raw.prepare("SELECT * FROM topics WHERE embedding IS NOT NULL").all() as Topic[];

        for (const topic of topicsWithEmb) {
          // Skip if already found by keywords
          if (results.some(r => r.topic.id === topic.id)) continue;

          const topicEmb = new Float32Array(
            (topic.embedding as unknown as Buffer).buffer,
            (topic.embedding as unknown as Buffer).byteOffset,
            queryEmb.length,
          );

          const cos = this.cosine(new Float32Array(queryEmb), topicEmb);
          if (cos >= 0.45) {
            const recencyBoost = Math.exp(-(Date.now() - topic.last_seen) / (86400000 * 14));
            const score = cos * (0.5 + topic.importance_score * 0.3 + recencyBoost * 0.2);

            const factRows = raw.prepare(
              "SELECT f.fact FROM facts f JOIN fact_topics ft ON ft.fact_id = f.id WHERE ft.topic_id = ? AND f.superseded = 0 ORDER BY f.created_at DESC LIMIT 10"
            ).all(topic.id) as Array<{ fact: string }>;

            results.push({ topic, score, facts: factRows.map(r => r.fact) });
          }
        }
      } catch (e) { console.debug('memoria:topics: ' + String(e)); }
    }

    // Sort by score and limit
    results.sort((a, b) => b.score - a.score);

    // Track access on returned topics
    for (const r of results.slice(0, limit)) {
      raw.prepare("UPDATE topics SET access_count = access_count + 1, last_seen = ? WHERE id = ?")
        .run(Date.now(), r.topic.id);
    }

    return results.slice(0, limit);
  }

  // ─── 8. Apply decay on old topics ───

  private applyDecay(): void {
    const raw = this.db.raw;
    const now = Date.now();
    const decayMs = this.cfg.decayDays * 86400000;

    // Reduce importance of topics not seen recently
    raw.prepare(`
      UPDATE topics SET importance_score = importance_score * 
        MAX(0.1, 1.0 - (? - last_seen) / (? * 2.0))
      WHERE (? - last_seen) > ?
    `).run(now, decayMs, now, decayMs);
  }

  // ─── 9. Should scan? ───

  /**
   * Called when a fact is superseded — remove fact↔topic links
   * and update topic fact_count. Delete empty topics.
   */
  onFactSuperseded(factId: string): number {
    let affected = 0;
    try {
      const raw = this.db.raw;
      // Find topics linked to this fact
      const linked = raw.prepare(
        "SELECT topic_id FROM fact_topics WHERE fact_id = ?"
      ).all(factId) as Array<{ topic_id: string }>;

      // Remove the links
      raw.prepare("DELETE FROM fact_topics WHERE fact_id = ?").run(factId);

      // Update fact_count and clean up empty topics
      for (const { topic_id } of linked) {
        const count = (raw.prepare(
          "SELECT COUNT(*) as c FROM fact_topics WHERE topic_id = ?"
        ).get(topic_id) as { c: number }).c;

        if (count === 0) {
          // No facts left → delete topic
          raw.prepare("DELETE FROM topics WHERE id = ?").run(topic_id);
        } else {
          raw.prepare("UPDATE topics SET fact_count = ? WHERE id = ?").run(count, topic_id);
        }
        affected++;
      }
    } catch (e) { console.debug('memoria:topics: ' + String(e)); }
    return affected;
  }

  /**
   * Re-parent existing orphan topics.
   * Called once at boot to fix topics created before hierarchy logic existed.
   */
  reparentExistingTopics(): number {
    const raw = this.db.raw;
    const orphans = raw.prepare(
      "SELECT * FROM topics WHERE parent_topic_id IS NULL OR parent_topic_id = '' ORDER BY fact_count ASC"
    ).all() as Topic[];

    let reparented = 0;
    for (const topic of orphans) {
      const kw: string[] = JSON.parse(topic.keywords as unknown as string || "[]");
      const parentId = this.findParentTopic(topic.name, kw);
      if (parentId && parentId !== topic.id) {
        raw.prepare("UPDATE topics SET parent_topic_id = ? WHERE id = ?").run(parentId, topic.id);
        reparented++;
      }
    }
    return reparented;
  }

  shouldScan(): boolean {
    return this.capturesSinceLastScan >= this.cfg.scanInterval;
  }

  // ─── Stats ───

  stats(): { totalTopics: number; topLevelTopics: number; subTopics: number; orphanFacts: number; avgFactsPerTopic: number } {
    const raw = this.db.raw;
    const total = (raw.prepare("SELECT COUNT(*) as c FROM topics").get() as { c: number }).c;
    const topLevel = (raw.prepare("SELECT COUNT(*) as c FROM topics WHERE parent_topic_id IS NULL OR parent_topic_id = ''").get() as { c: number }).c;
    const orphans = (raw.prepare(`
      SELECT COUNT(*) as c FROM facts 
      WHERE superseded = 0 AND tags != '[]' AND tags IS NOT NULL
      AND id NOT IN (SELECT fact_id FROM fact_topics)
    `).get() as { c: number }).c;
    const avgFacts = total > 0
      ? (raw.prepare("SELECT AVG(fact_count) as a FROM topics").get() as { a: number }).a
      : 0;

    return {
      totalTopics: total,
      topLevelTopics: topLevel,
      subTopics: total - topLevel,
      orphanFacts: orphans,
      avgFactsPerTopic: Math.round(avgFacts * 10) / 10,
    };
  }

  // ─── Helpers ───

  /**
   * Find a parent topic for a newly created topic.
   * Strategies:
   *   1. Name inclusion: if an existing topic's name is contained in the new name (or vice-versa)
   *   2. Keyword overlap: if a top-level topic shares keywords but is broader
   * Returns parent topic ID or null.
   */
  private findParentTopic(newName: string, newKeywords: string[]): string | null {
    const raw = this.db.raw;
    const topLevelTopics = raw.prepare(
      "SELECT * FROM topics WHERE (parent_topic_id IS NULL OR parent_topic_id = '') ORDER BY fact_count DESC"
    ).all() as Topic[];

    const newNameLower = newName.toLowerCase();
    // Extract significant words (skip stop words, min 3 chars)
    const stopWords = new Set(["et", "de", "du", "des", "le", "la", "les", "un", "une", "en", "à", "the", "and", "of", "for", "in", "on", "with", "a"]);
    const newNameWords = newNameLower.split(/[\s/,—–-]+/).filter(w => w.length >= 3 && !stopWords.has(w));

    let bestCandidate: { id: string; score: number } | null = null;

    for (const topic of topLevelTopics) {
      const topicNameLower = topic.name.toLowerCase();
      // Skip if same name (would be a self-reference)
      if (topicNameLower === newNameLower) continue;

      // Strategy 1: Name inclusion — new topic name contains existing topic name
      // e.g., "Memoria ClawHub" contains "Memoria" → parent is "Memoria" topic
      if (newNameLower.includes(topicNameLower) && topicNameLower.length >= 3) {
        return topic.id;
      }

      // Strategy 2: Shared significant words in name
      // e.g., "Sol Memory" and "Sol Succès" share "sol" → broader one (more facts) is parent
      const topicNameWords = topicNameLower.split(/[\s/,—–-]+/).filter(w => w.length >= 3 && !stopWords.has(w));
      const sharedWords = newNameWords.filter(w => topicNameWords.includes(w));
      if (sharedWords.length > 0 && topic.fact_count > 3) {
        // Score: shared words / max words, weighted by parent fact_count
        const wordOverlap = sharedWords.length / Math.max(newNameWords.length, topicNameWords.length);
        // Prefer the topic with more facts (broader = better parent)
        const score = wordOverlap * Math.log2(topic.fact_count + 1);
        if (score > 0.4 && (!bestCandidate || score > bestCandidate.score)) {
          // Only set as parent if existing topic is broader (more facts)
          if (topic.fact_count >= 5) {
            bestCandidate = { id: topic.id, score };
          }
        }
      }

      // Strategy 3: Keyword overlap — existing topic has ≥50% of new topic's keywords
      // but is broader (has more facts)
      const topicKw: string[] = JSON.parse(topic.keywords as unknown as string || "[]");
      if (topicKw.length > 0 && newKeywords.length > 0) {
        const shared = newKeywords.filter(k => topicKw.includes(k)).length;
        const overlapRatio = shared / newKeywords.length;
        // New topic shares ≥50% keywords with existing AND existing is broader
        if (overlapRatio >= 0.5 && topic.fact_count > newKeywords.length * 2) {
          return topic.id;
        }
      }
    }

    return bestCandidate?.id ?? null;
  }

  private async generateTopicName(keywords: string[], sampleFactIds: string[]): Promise<string> {
    try {
      // Get sample facts
      const raw = this.db.raw;
      const facts: string[] = [];
      for (const fid of sampleFactIds.slice(0, 3)) {
        const f = raw.prepare("SELECT fact FROM facts WHERE id = ?").get(fid) as { fact: string } | undefined;
        if (f) facts.push(f.fact);
      }

      const prompt = `Donne un nom court (1-3 mots) pour un topic regroupant ces faits.
Keywords: ${keywords.join(", ")}
Faits exemples: ${facts.join(" | ")}

Réponds UNIQUEMENT le nom du topic, rien d'autre. Exemples: "Bureau CRM", "Infrastructure Ollama", "Mémoire Agents", "Déploiement Vercel"`;

      const response = await this.llm.generate(prompt, {
        maxTokens: 20,
        temperature: 0.3,
        timeoutMs: 8000,
      });

      const name = response.trim().replace(/["\n]/g, "").slice(0, 50);
      return name || keywords.slice(0, 2).join(" ");
    } catch (e) {
      console.debug('memoria:topics: ' + String(e));
      return keywords.slice(0, 2).join(" ");
    }
  }

  private mergeClusters(clusters: Array<{ keyword: string; factIds: string[] }>): Array<{ keywords: string[]; factIds: string[] }> {
    if (clusters.length === 0) return [];

    // Sort by size (biggest first)
    clusters.sort((a, b) => b.factIds.length - a.factIds.length);

    const merged: Array<{ keywords: string[]; factIds: Set<string> }> = [];
    const used = new Set<number>();

    for (let i = 0; i < clusters.length; i++) {
      if (used.has(i)) continue;

      const group = { keywords: [clusters[i].keyword], factIds: new Set(clusters[i].factIds) };

      for (let j = i + 1; j < clusters.length; j++) {
        if (used.has(j)) continue;

        // Check fact overlap
        const overlap = clusters[j].factIds.filter(f => group.factIds.has(f)).length;
        const overlapRatio = overlap / Math.min(group.factIds.size, clusters[j].factIds.length);

        if (overlapRatio >= 0.5) {
          group.keywords.push(clusters[j].keyword);
          for (const f of clusters[j].factIds) group.factIds.add(f);
          used.add(j);
        }
      }

      merged.push(group);
      used.add(i);
    }

    return merged.map(g => ({ keywords: g.keywords, factIds: [...g.factIds] }));
  }

  private jaccardOverlap(a: string[], b: string[]): number {
    if (a.length === 0 || b.length === 0) return 0;
    const setA = new Set(a);
    const setB = new Set(b);
    let intersection = 0;
    for (const x of setA) if (setB.has(x)) intersection++;
    const union = new Set([...a, ...b]).size;
    return union > 0 ? intersection / union : 0;
  }

  private cosine(a: Float32Array, b: Float32Array): number {
    let dot = 0, na = 0, nb = 0;
    for (let i = 0; i < a.length; i++) {
      dot += a[i] * b[i];
      na += a[i] * a[i];
      nb += b[i] * b[i];
    }
    const denom = Math.sqrt(na) * Math.sqrt(nb);
    return denom > 0 ? dot / denom : 0;
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
