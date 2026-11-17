/**
 * Memoria — Layer 5: Knowledge Graph
 * 
 * Extracts entities (person/project/tool/concept/place) and relations from facts via LLM.
 * Enables associative recall: "Bureau" → Convex, CRM, Qonto, Alexandre...
 * 
 * Key methods:
 *   extractAndStore(facts) — LLM extracts entities/relations, stores in DB
 *   findEntitiesInText(query) — find mentioned entities in a search query
 *   getRelatedFacts(entityIds) — BFS 2 hops to find connected facts
 * 
 * Note: Hebbian reinforcement (co-occurrence strengthening) is in hebbian.ts (Layer 16).
 * 
 * Les connexions se RENFORCENT à chaque co-accès (Hebb: "neurons that fire together wire together").
 * Les connexions inutilisées s'AFFAIBLISSENT (decay).
 */

import type { MemoriaDB, Entity, Relation } from "./db.js";
import type { LLMProvider } from "./providers/types.js";

// ─── Config ───

export interface GraphConfig {
  /** Weight increment on co-access (Hebbian). Default 0.1 */
  hebbianIncrement: number;
  /** Decay factor per day for unused relations. Default 0.995 (~0.5% per day) */
  decayPerDay: number;
  /** Minimum weight before pruning. Default 0.05 */
  pruneThreshold: number;
  /** Max entities to extract per fact. Default 5 */
  maxEntitiesPerFact: number;
  /** Max hops for graph traversal. Default 2 */
  maxHops: number;
  /** Max related facts to return. Default 5 */
  maxRelatedFacts: number;
}

export const DEFAULT_GRAPH_CONFIG: GraphConfig = {
  hebbianIncrement: 0.1,
  decayPerDay: 0.995,
  pruneThreshold: 0.05,
  maxEntitiesPerFact: 5,
  maxHops: 2,
  maxRelatedFacts: 5,
};

// ─── Extraction prompt ───

const EXTRACT_PROMPT = `Extrais les entités et relations de ce fait.

Fait: "{FACT}"

Réponds UNIQUEMENT en JSON:
{
  "entities": [
    {"name": "NomExact", "type": "person|project|tool|concept|place|company"}
  ],
  "relations": [
    {"from": "NomExact1", "to": "NomExact2", "type": "uses|part_of|works_on|manages|created_by|depends_on|deployed_on|related_to"}
  ]
}

Règles:
- Noms propres exacts (pas de descriptions)
- Types stricts: person, project, tool, concept, place, company
- Relations: max 3, les plus importantes
- Si rien d'intéressant: {"entities": [], "relations": []}`;

// ─── Graph Manager ───

export class KnowledgeGraph {
  private db: MemoriaDB;
  private llm: LLMProvider;
  private cfg: GraphConfig;

  constructor(db: MemoriaDB, llm: LLMProvider, config?: Partial<GraphConfig>) {
    this.db = db;
    this.llm = llm;
    this.cfg = { ...DEFAULT_GRAPH_CONFIG, ...config };
  }

  private get rawDb() {
    return this.db.raw;
  }

  // ─── Entity extraction ───

  /** Extract entities and relations from a fact, store them */
  async extractAndStore(factId: string, factText: string): Promise<{ entities: number; relations: number }> {
    try {
      const prompt = EXTRACT_PROMPT.replace("{FACT}", factText);
      const response = await this.llm.generate(prompt, {
        maxTokens: 512,
        temperature: 0.1,
        format: "json",
        timeoutMs: 15000,
      });

      const parsed = this.parseJSON(response) as {
        entities?: Array<{ name: string; type: string }>;
        relations?: Array<{ from: string; to: string; type: string }>;
      };

      if (!parsed) return { entities: 0, relations: 0 };

      let entCount = 0;
      let relCount = 0;

      // Store entities
      const entityIds = new Map<string, string>();
      for (const e of (parsed.entities || []).slice(0, this.cfg.maxEntitiesPerFact)) {
        if (!e.name || e.name.length < 2) continue;
        const normalized = e.name.trim();
        const type = this.normalizeType(e.type);

        // Find existing or create
        let entity = this.findEntityByName(normalized);
        if (!entity) {
          const id = `ent_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
          this.rawDb.prepare(
            "INSERT INTO entities (id, name, type, attributes, created_at, access_count) VALUES (?, ?, ?, ?, ?, ?)"
          ).run(id, normalized, type, "{}", Date.now(), 0);
          entity = { id, name: normalized, type, attributes: "{}", created_at: Date.now(), access_count: 0 };
          entCount++;
        }
        entityIds.set(normalized, entity.id);
      }

      // Store relations
      for (const r of (parsed.relations || []).slice(0, 3)) {
        const fromId = entityIds.get(r.from) || this.findEntityByName(r.from)?.id;
        const toId = entityIds.get(r.to) || this.findEntityByName(r.to)?.id;
        if (!fromId || !toId || fromId === toId) continue;

        const relType = this.normalizeRelType(r.type);
        this.upsertRelation(fromId, toId, relType, factId);
        relCount++;
      }

      // Link fact to entities
      if (entityIds.size > 0) {
        const ids = Array.from(entityIds.values());
        this.rawDb.prepare(
          "UPDATE facts SET entity_ids = ? WHERE id = ?"
        ).run(JSON.stringify(ids), factId);
      }

      return { entities: entCount, relations: relCount };
    } catch (e) {
      console.debug('memoria:graph: ' + String(e));
      return { entities: 0, relations: 0 };
    }
  }

  // ─── Graph traversal ───

  /** Get related facts by traversing the graph from seed entities */
  getRelatedFacts(entityNames: string[], maxHops?: number, maxFacts?: number): Array<{ fact: string; id: string; score: number; path: string[] }> {
    const hops = maxHops ?? this.cfg.maxHops;
    const limit = maxFacts ?? this.cfg.maxRelatedFacts;

    // Find seed entity IDs
    const seedIds = new Set<string>();
    for (const name of entityNames) {
      const entity = this.findEntityByName(name);
      if (entity) seedIds.add(entity.id);
    }
    if (seedIds.size === 0) return [];

    // BFS traversal
    const visited = new Set<string>();
    const queue: Array<{ entityId: string; hop: number; path: string[] }> = [];
    const factScores = new Map<string, { score: number; path: string[] }>();

    for (const id of seedIds) {
      queue.push({ entityId: id, hop: 0, path: [this.getEntityName(id)] });
      visited.add(id);
    }

    while (queue.length > 0) {
      const { entityId, hop, path } = queue.shift()!;
      if (hop >= hops) continue;

      // Get relations from this entity
      const relations = this.getRelations(entityId);
      for (const rel of relations) {
        const neighborId = rel.source_id === entityId ? rel.target_id : rel.source_id;
        const weight = rel.weight;

        // Score facts linked to this neighbor
        const neighborFacts = this.getFactsByEntity(neighborId);
        for (const f of neighborFacts) {
          const hopPenalty = 1 / (hop + 1); // Closer = higher score
          const score = weight * hopPenalty;
          const existing = factScores.get(f.id);
          if (!existing || existing.score < score) {
            const neighborName = this.getEntityName(neighborId);
            factScores.set(f.id, { score, path: [...path, neighborName] });
          }
        }

        // Continue traversal
        if (!visited.has(neighborId)) {
          visited.add(neighborId);
          const neighborName = this.getEntityName(neighborId);
          queue.push({ entityId: neighborId, hop: hop + 1, path: [...path, neighborName] });
        }
      }
    }

    // Sort by score, return top N
    const results = Array.from(factScores.entries())
      .map(([factId, { score, path }]) => {
        const fact = this.db.getFact(factId);
        if (!fact || fact.superseded) return null;
        return { fact: fact.fact, id: factId, score, path };
      })
      .filter(Boolean) as Array<{ fact: string; id: string; score: number; path: string[] }>;

    results.sort((a, b) => b.score - a.score);
    return results.slice(0, limit);
  }

  /** Extract entity names from a query (keyword match + partial match against known entities) */
  findEntitiesInText(text: string): Entity[] {
    const allEntities = this.rawDb.prepare(
      "SELECT * FROM entities ORDER BY access_count DESC LIMIT 200"
    ).all() as Entity[];

    const lower = text.toLowerCase();
    const words = lower.split(/\s+/).filter(w => w.length > 2);

    return allEntities.filter(e => {
      const eName = e.name.toLowerCase();
      // Exact containment (text contains entity name)
      if (lower.includes(eName)) return true;
      // Reverse: entity name contains a word from query (for multi-word entities)
      if (words.some(w => eName.includes(w) && w.length > 3)) return true;
      return false;
    });
  }

  // ─── Hebbian learning ───

  /** Strengthen connections between co-accessed entities */
  hebbianReinforce(entityIds: string[]): void {
    if (entityIds.length < 2) return;

    // All pairs
    for (let i = 0; i < entityIds.length; i++) {
      for (let j = i + 1; j < entityIds.length; j++) {
        this.reinforceRelation(entityIds[i], entityIds[j]);
      }
      // Increment access count
      this.rawDb.prepare(
        "UPDATE entities SET access_count = access_count + 1 WHERE id = ?"
      ).run(entityIds[i]);
    }
  }

  /** Apply decay to all relations (call periodically, e.g. daily) */
  applyDecay(): number {
    const now = Date.now();
    const relations = this.rawDb.prepare("SELECT * FROM relations").all() as any[];
    let pruned = 0;

    const updateStmt = this.rawDb.prepare("UPDATE relations SET weight = ? WHERE id = ?");
    const deleteStmt = this.rawDb.prepare("DELETE FROM relations WHERE id = ?");

    const tx = this.rawDb.transaction(() => {
      for (const rel of relations) {
        const daysSinceAccess = (now - (rel.last_accessed_at || rel.created_at)) / 86400000;
        const decayedWeight = rel.weight * Math.pow(this.cfg.decayPerDay, daysSinceAccess);

        if (decayedWeight < this.cfg.pruneThreshold) {
          deleteStmt.run(rel.id);
          pruned++;
        } else if (decayedWeight < rel.weight) {
          updateStmt.run(decayedWeight, rel.id);
        }
      }
    });
    tx();

    return pruned;
  }

  // ─── Stats ───

  /** 
   * Called when a fact is superseded — weaken relations that depended on it.
   * Removes factId from relation context arrays; if no facts left → prune relation.
   */
  onFactSuperseded(factId: string): number {
    let affected = 0;
    try {
      // 1. Remove from relation context arrays
      const relations = this.rawDb.prepare(
        "SELECT id, context FROM relations WHERE context LIKE ?"
      ).all(`%${factId}%`) as Array<{ id: string; context: string }>;

      for (const rel of relations) {
        try {
          const ctx = JSON.parse(rel.context || "[]") as string[];
          const updated = ctx.filter(id => id !== factId);
          if (updated.length === 0) {
            // No facts support this relation anymore → delete it
            this.rawDb.prepare("DELETE FROM relations WHERE id = ?").run(rel.id);
          } else {
            // Weaken the relation (lost a supporting fact)
            this.rawDb.prepare(
              "UPDATE relations SET context = ?, weight = MAX(weight - 0.15, 0.1) WHERE id = ?"
            ).run(JSON.stringify(updated), rel.id);
          }
          affected++;
        } catch (e) { console.debug('memoria:graph: ' + String(e)); }
      }

      // 2. Clean entity_ids from the superseded fact (clear the link)
      this.rawDb.prepare(
        "UPDATE facts SET entity_ids = NULL WHERE id = ? AND superseded = 1"
      ).run(factId);
    } catch (e) { console.debug('memoria:graph: ' + String(e)); }
    return affected;
  }

  stats(): { entities: number; relations: number; avgWeight: number } {
    const entities = (this.rawDb.prepare("SELECT COUNT(*) as c FROM entities").get() as { c: number }).c;
    const relStats = this.rawDb.prepare("SELECT COUNT(*) as c, AVG(weight) as avg FROM relations").get() as { c: number; avg: number | null };
    return {
      entities,
      relations: relStats.c,
      avgWeight: relStats.avg ?? 0,
    };
  }

  // ─── Private helpers ───

  private findEntityByName(name: string): Entity | undefined {
    // Exact match first
    let entity = this.rawDb.prepare(
      "SELECT * FROM entities WHERE name = ? COLLATE NOCASE LIMIT 1"
    ).get(name) as Entity | undefined;
    if (entity) return entity;

    // Fuzzy: LIKE match
    entity = this.rawDb.prepare(
      "SELECT * FROM entities WHERE name LIKE ? COLLATE NOCASE LIMIT 1"
    ).get(`%${name}%`) as Entity | undefined;
    return entity;
  }

  private getEntityName(id: string): string {
    const e = this.rawDb.prepare("SELECT name FROM entities WHERE id = ?").get(id) as { name: string } | undefined;
    return e?.name ?? id;
  }

  private getRelations(entityId: string): Array<{ id: string; source_id: string; target_id: string; relation: string; weight: number; context: string | null; created_at: number; last_accessed_at: number | null }> {
    return this.rawDb.prepare(
      "SELECT * FROM relations WHERE source_id = ? OR target_id = ?"
    ).all(entityId, entityId) as any[];
  }

  private getFactsByEntity(entityId: string): Array<{ id: string }> {
    return this.rawDb.prepare(
      "SELECT id FROM facts WHERE entity_ids LIKE ? AND superseded = 0 LIMIT 10"
    ).all(`%${entityId}%`) as Array<{ id: string }>;
  }

  private upsertRelation(fromId: string, toId: string, type: string, factId: string): void {
    const existing = this.rawDb.prepare(
      "SELECT * FROM relations WHERE (source_id = ? AND target_id = ?) OR (source_id = ? AND target_id = ?)"
    ).get(fromId, toId, toId, fromId) as any | undefined;

    if (existing) {
      // Reinforce existing
      const ctx = this.appendToJsonArray(existing.context || "[]", factId);
      this.rawDb.prepare(
        "UPDATE relations SET weight = MIN(weight + ?, 1.0), last_accessed_at = ?, context = ? WHERE id = ?"
      ).run(this.cfg.hebbianIncrement, Date.now(), ctx, existing.id);
    } else {
      const id = `rel_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
      this.rawDb.prepare(
        "INSERT INTO relations (id, source_id, target_id, relation, weight, context, created_at, last_accessed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
      ).run(id, fromId, toId, type, 0.5, JSON.stringify([factId]), Date.now(), Date.now());
    }
  }

  private reinforceRelation(entityA: string, entityB: string): void {
    const rel = this.rawDb.prepare(
      "SELECT * FROM relations WHERE (source_id = ? AND target_id = ?) OR (source_id = ? AND target_id = ?)"
    ).get(entityA, entityB, entityB, entityA) as any | undefined;

    if (rel) {
      this.rawDb.prepare(
        "UPDATE relations SET weight = MIN(weight + ?, 1.0), last_accessed_at = ? WHERE id = ?"
      ).run(this.cfg.hebbianIncrement, Date.now(), rel.id);
    }
  }

  private appendToJsonArray(existing: string, newItem: string): string {
    try {
      const arr = JSON.parse(existing) as string[];
      if (!arr.includes(newItem)) arr.push(newItem);
      return JSON.stringify(arr.slice(-20));
    } catch (e) {
      console.debug('memoria:graph: ' + String(e));
      return JSON.stringify([newItem]);
    }
  }

  private normalizeType(type: string): string {
    const valid = ["person", "project", "tool", "concept", "place", "company"];
    const lower = (type || "").toLowerCase().trim();
    return valid.includes(lower) ? lower : "concept";
  }

  private normalizeRelType(type: string): string {
    const valid = ["uses", "part_of", "works_on", "manages", "created_by", "depends_on", "deployed_on", "related_to"];
    const lower = (type || "").toLowerCase().trim();
    return valid.includes(lower) ? lower : "related_to";
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
