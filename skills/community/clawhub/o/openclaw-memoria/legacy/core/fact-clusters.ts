/**
 * Memoria — Fact Clusters (v3.4.0)
 * 
 * Generates thematic summaries from groups of related atomic facts.
 * Solves the "multi-session" problem: when facts about the same entity
 * are scattered across sessions, a cluster aggregates them into one
 * searchable summary.
 * 
 * Like a "dossier" in an office: when you look up a client, you get
 * the complete file, not individual scattered notes.
 * 
 * Clusters are:
 * - Generated from atomic facts sharing the same entity/topic
 * - Stored as regular facts (fact_type = "cluster") for FTS/embedding search
 * - Auto-invalidated when a member fact is superseded
 * - Regenerated periodically to stay fresh
 */

import type { MemoriaDB, Fact } from "./db.js";
import type { LLMProvider } from "./providers/types.js";

// ─── Types ───

export interface ClusterMeta {
  memberIds: string[];      // IDs of atomic facts in this cluster
  entityName: string;       // Primary entity ("Sol", "Bureau", "RH Primo Studio")
  generatedAt: number;      // Timestamp of generation
  stale: boolean;           // True if a member was superseded since generation
}

export interface ClusterResult {
  created: number;
  updated: number;
  stale: number;
}

// ─── Config ───

const MIN_FACTS_FOR_CLUSTER = 3;   // Need at least 3 facts to justify a cluster
const MAX_CLUSTER_FACTS = 12;      // Don't cluster more than 12 facts (context limit)
const CLUSTER_REGEN_HOURS = 24;    // Regenerate stale clusters after this delay
const MAX_CLUSTERS_PER_RUN = 5;    // Limit cluster generation per postProcess call

// ─── Prompt ───

const CLUSTER_PROMPT = `Tu résumes un groupe de faits liés à la même entité en UN SEUL paragraphe dense.

Règles:
- Le résumé doit contenir TOUTES les informations clés des faits (noms, chiffres, dates, versions, états)
- Commence par l'entité principale en gras contexte
- Si des infos se contredisent, garde la plus récente
- Si un fait dit qu'une personne est partie ou qu'un outil est remplacé, reflète cet état actuel
- 2-4 phrases maximum, dense et factuel
- En français

Entité: {ENTITY}

Faits:
{FACTS}

Résumé dense (texte brut, pas de JSON):`;

// ─── Manager ───

export class FactClusterManager {
  private db: MemoriaDB;
  private llm: LLMProvider;

  constructor(db: MemoriaDB, llm: LLMProvider) {
    this.db = db;
    this.llm = llm;
  }

  /**
   * Main entry point: generate/refresh clusters for entities with enough facts.
   * Called from postProcessNewFacts.
   */
  async generateClusters(): Promise<ClusterResult> {
    const result: ClusterResult = { created: 0, updated: 0, stale: 0 };

    try {
      // 1. Find entities with enough active facts
      const entityGroups = this.groupFactsByEntity();

      // 2. Check existing clusters for staleness
      result.stale = this.markStaleClusters();

      // 3. Generate/regenerate clusters for top entities
      let generated = 0;
      for (const [entityName, facts] of entityGroups) {
        if (generated >= MAX_CLUSTERS_PER_RUN) break;
        if (facts.length < MIN_FACTS_FOR_CLUSTER) continue;

        const existing = this.findCluster(entityName);

        // Skip if cluster exists and is fresh
        if (existing && !this.isStale(existing)) continue;

        // Generate cluster
        const clusterText = await this.generateClusterText(entityName, facts);
        if (!clusterText) continue;

        if (existing) {
          // Update existing cluster
          this.updateCluster(existing.id, clusterText, facts);
          result.updated++;
        } else {
          // Create new cluster
          this.createCluster(entityName, clusterText, facts);
          result.created++;
        }
        generated++;
      }
    } catch (e) {
      console.debug('memoria:clusters: ' + String(e));
      // Non-critical: clusters are a quality enhancement, not required
    }

    return result;
  }

  /**
   * Group active (non-superseded, non-cluster) facts by their primary entity.
   * Uses entity_ids from the knowledge graph when available,
   * falls back to keyword extraction.
   */
  private groupFactsByEntity(): Map<string, Fact[]> {
    const groups = new Map<string, Fact[]>();

    // Get all active non-cluster facts
    const facts = this.db.raw.prepare(
      "SELECT * FROM facts WHERE superseded = 0 AND (fact_type != 'cluster' OR fact_type IS NULL) ORDER BY created_at DESC"
    ).all() as Fact[];

    for (const fact of facts) {
      // Try entity_ids first (from knowledge graph)
      let entities: string[] = [];
      try {
        const ids = JSON.parse(fact.entity_ids || "[]") as string[];
        if (ids.length > 0) {
          // Look up entity names
          for (const id of ids) {
            const ent = this.db.raw.prepare("SELECT name FROM entities WHERE id = ?").get(id) as { name: string } | undefined;
            if (ent) entities.push(ent.name);
          }
        }
      } catch (e) { console.debug('memoria:clusters: ' + String(e)); }

      // Fallback: extract proper nouns as entity proxies
      if (entities.length === 0) {
        entities = this.extractProperNouns(fact.fact);
      }

      // Add fact to each entity group
      for (const entity of entities) {
        const key = entity.toLowerCase().trim();
        if (key.length < 2) continue;
        if (!groups.has(key)) groups.set(key, []);
        groups.get(key)!.push(fact);
      }
    }

    // Sort by group size (largest first) and filter minimum
    const sorted = new Map(
      Array.from(groups.entries())
        .filter(([, facts]) => facts.length >= MIN_FACTS_FOR_CLUSTER)
        .sort((a, b) => b[1].length - a[1].length)
    );

    return sorted;
  }

  /**
   * Extract proper nouns from text (capitalized words that aren't sentence-starters).
   */
  private extractProperNouns(text: string): string[] {
    const nouns = new Set<string>();

    // Match capitalized words (2+ chars) that appear after other text
    const matches = text.match(/(?<=\s)[A-Z][a-zéèêëàâäôöùûüïîç]+(?:\s+[A-Z][a-zéèêëàâäôöùûüïîç]+)*/g) || [];
    for (const m of matches) {
      if (m.length > 2) nouns.add(m);
    }

    // Also match common entity patterns
    const techTerms = text.match(/\b(?:Memoria|Bureau|Convex|Primask|DockGroups|Sol|Luna|Koda|Neto|Ollama|Vercel|Cloudflare|Qonto|Alexandre|Pierre|HydroTrack|OpenClaw)\b/gi) || [];
    for (const t of techTerms) {
      nouns.add(t.charAt(0).toUpperCase() + t.slice(1).toLowerCase());
    }

    return Array.from(nouns);
  }

  /**
   * Find existing cluster for an entity.
   */
  private findCluster(entityName: string): Fact | undefined {
    const pattern = `%${entityName}%`;
    return this.db.raw.prepare(
      "SELECT * FROM facts WHERE fact_type = 'cluster' AND superseded = 0 AND source LIKE ? LIMIT 1"
    ).get(`cluster:${entityName.toLowerCase()}`) as Fact | undefined
    // Fallback: search by source field
    || this.db.raw.prepare(
      "SELECT * FROM facts WHERE fact_type = 'cluster' AND superseded = 0 AND source = ? LIMIT 1"
    ).get(`cluster:${entityName.toLowerCase()}`) as Fact | undefined;
  }

  /**
   * Check if a cluster is stale (member superseded or too old).
   */
  private isStale(cluster: Fact): boolean {
    try {
      const meta = JSON.parse(cluster.tags) as ClusterMeta;
      if (meta.stale) return true;

      // Check age
      const ageHours = (Date.now() - meta.generatedAt) / (3600 * 1000);
      if (ageHours > CLUSTER_REGEN_HOURS) return true;

      // Check if any member was superseded
      for (const id of meta.memberIds) {
        const member = this.db.getFact(id);
        if (member && member.superseded) return true;
      }

      return false;
    } catch (e) {
      console.debug('memoria:clusters: ' + String(e));
      return true; // Can't parse meta → treat as stale
    }
  }

  /**
   * Mark clusters as stale if any member fact was recently superseded.
   */
  private markStaleClusters(): number {
    let staleCount = 0;
    const clusters = this.db.raw.prepare(
      "SELECT * FROM facts WHERE fact_type = 'cluster' AND superseded = 0"
    ).all() as Fact[];

    for (const cluster of clusters) {
      if (this.isStale(cluster)) {
        try {
          const meta = JSON.parse(cluster.tags) as ClusterMeta;
          meta.stale = true;
          this.db.raw.prepare("UPDATE facts SET tags = ?, updated_at = ? WHERE id = ?")
            .run(JSON.stringify(meta), Date.now(), cluster.id);
          staleCount++;
        } catch (e) { console.debug('memoria:clusters: ' + String(e)); }
      }
    }

    return staleCount;
  }

  /**
   * Generate cluster text via LLM.
   */
  private async generateClusterText(entityName: string, facts: Fact[]): Promise<string | null> {
    // Take most recent facts, up to limit
    const selected = facts
      .sort((a, b) => b.created_at - a.created_at)
      .slice(0, MAX_CLUSTER_FACTS);

    const factsText = selected
      .map((f, i) => `${i + 1}. [${f.category}] ${f.fact}`)
      .join("\n");

    const prompt = CLUSTER_PROMPT
      .replace("{ENTITY}", entityName)
      .replace("{FACTS}", factsText);

    try {
      const genFn = this.llm.generateWithMeta;
      if (!genFn) return null;
      const result = await genFn.call(this.llm, prompt, {
        maxTokens: 300,
        temperature: 0.1,
        timeoutMs: 15000,
      });

      if (!result?.response) return null;

      // Clean response: remove JSON wrapping if present, take plain text
      let text = result.response.trim();
      // Remove markdown formatting artifacts
      text = text.replace(/^```[\s\S]*?```$/gm, "").trim();
      text = text.replace(/^["']|["']$/g, "").trim();

      if (text.length < 20) return null;
      return text;
    } catch (e) {
      console.debug('memoria:clusters: ' + String(e));
      return null;
    }
  }

  /**
   * Create a new cluster fact.
   */
  private createCluster(entityName: string, text: string, memberFacts: Fact[]): void {
    const members = memberFacts.slice(0, MAX_CLUSTER_FACTS);
    const meta: ClusterMeta = {
      memberIds: members.map(f => f.id),
      entityName,
      generatedAt: Date.now(),
      stale: false,
    };

    const clusterId = `cluster_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`;
    this.db.storeFact({
      id: clusterId,
      fact: text,
      category: memberFacts[0]?.category || "savoir",
      confidence: 0.85,
      source: `cluster:${entityName.toLowerCase()}`,
      tags: JSON.stringify(meta),
      agent: "memoria",
      created_at: Date.now(),
      updated_at: Date.now(),
      fact_type: "cluster",
    });

    // Populate cluster_members table
    this.syncClusterMembers(clusterId, members);
  }

  /**
   * Update an existing cluster with fresh text and members.
   */
  private updateCluster(clusterId: string, text: string, memberFacts: Fact[]): void {
    const members = memberFacts.slice(0, MAX_CLUSTER_FACTS);
    const meta: ClusterMeta = {
      memberIds: members.map(f => f.id),
      entityName: memberFacts[0]?.category || "entity",
      generatedAt: Date.now(),
      stale: false,
    };

    this.db.raw.prepare(
      "UPDATE facts SET fact = ?, tags = ?, updated_at = ? WHERE id = ?"
    ).run(text, JSON.stringify(meta), Date.now(), clusterId);

    // Refresh cluster_members table
    this.syncClusterMembers(clusterId, members);
  }

  /**
   * Sync the cluster_members relational table with the cluster's member facts.
   * Replaces all existing entries for this cluster.
   */
  private syncClusterMembers(clusterId: string, memberFacts: Fact[]): void {
    try {
      const raw = this.db.raw;
      raw.prepare("DELETE FROM cluster_members WHERE cluster_id = ?").run(clusterId);
      const insert = raw.prepare("INSERT OR IGNORE INTO cluster_members (cluster_id, fact_id) VALUES (?, ?)");
      for (const f of memberFacts) {
        insert.run(clusterId, f.id);
      }
    } catch (e) { console.debug('memoria:clusters: ' + String(e)); }
  }

  /**
   * Stats for logging.
   */
  stats(): { total: number; stale: number } {
    const total = (this.db.raw.prepare(
      "SELECT COUNT(*) as c FROM facts WHERE fact_type = 'cluster' AND superseded = 0"
    ).get() as { c: number }).c;
    const stale = (this.db.raw.prepare(
      "SELECT COUNT(*) as c FROM facts WHERE fact_type = 'cluster' AND superseded = 0 AND tags LIKE '%\"stale\":true%'"
    ).get() as { c: number }).c;
    return { total, stale };
  }
}
