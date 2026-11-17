/**
 * Hebbian Learning — "Neurons that fire together, wire together"
 * 
 * Human memory strengthens connections between concepts that frequently co-occur.
 * 
 * Example:
 *   - "Bureau" + "Convex" appear together 10 times → strong relation
 *   - "Memoria" + "ClawHub" appear together 3 times → weak relation
 * 
 * Implementation:
 *   - Track entity co-occurrence in facts and graph enrichment
 *   - Boost relation weight when entities co-occur
 *   - Decay weight for unused relations
 * 
 * DB schema: relations(id, source_id, target_id, relation, weight, context, created_at, last_accessed_at)
 */

import type { MemoriaDB } from "./db.js";

export const HEBBIAN_CONFIG = {
  boostAmount: 0.1,        // Increase weight by 0.1 on each co-occurrence
  maxWeight: 2.0,          // Cap weight at 2.0 (very strong)
  decayRate: 0.95,         // Multiply weight by 0.95 if not used recently
  decayThresholdDays: 30,  // Decay relations not used in 30 days
  minWeight: 0.1,          // Minimum weight before pruning
};

export interface RelationStats {
  total: number;
  strong: number;    // weight >= 1.0
  weak: number;      // weight < 0.5
  decayed: number;   // recently decayed
}

export class HebbianManager {
  private db: MemoriaDB;
  
  constructor(db: MemoriaDB) {
    this.db = db;
  }

  /**
   * Reinforce relation between two entities (co-occurrence detected)
   */
  reinforceRelation(fromEntity: string, toEntity: string, relationType: string = "co-occurs"): void {
    const now = Date.now();

    // Check if relation exists (use actual DB column names)
    const existing = this.db.raw.prepare(
      "SELECT weight, last_accessed_at FROM relations WHERE source_id = ? AND target_id = ? AND relation = ?"
    ).get(fromEntity, toEntity, relationType) as { weight: number; last_accessed_at: number } | undefined;

    if (existing) {
      // Boost existing relation (capped at maxWeight)
      const newWeight = Math.min(existing.weight + HEBBIAN_CONFIG.boostAmount, HEBBIAN_CONFIG.maxWeight);
      this.db.raw.prepare(
        "UPDATE relations SET weight = ?, last_accessed_at = ? WHERE source_id = ? AND target_id = ? AND relation = ?"
      ).run(newWeight, now, fromEntity, toEntity, relationType);
    } else {
      // Create new relation with initial weight
      const id = `rel_${now}_${Math.random().toString(36).slice(2, 9)}`;
      this.db.raw.prepare(
        "INSERT INTO relations (id, source_id, target_id, relation, weight, context, created_at, last_accessed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
      ).run(id, fromEntity, toEntity, relationType, HEBBIAN_CONFIG.boostAmount, null, now, now);
    }
  }

  /**
   * Decay relations not used recently
   */
  decayStaleRelations(): { decayed: number; pruned: number } {
    const now = Date.now();
    const cutoff = now - HEBBIAN_CONFIG.decayThresholdDays * 24 * 60 * 60 * 1000;

    // Find stale relations
    const stale = this.db.raw.prepare(
      "SELECT id, source_id, target_id, relation, weight FROM relations WHERE last_accessed_at < ? AND weight > ?"
    ).all(cutoff, HEBBIAN_CONFIG.minWeight) as Array<{ id: string; source_id: string; target_id: string; relation: string; weight: number }>;

    let decayed = 0;
    let pruned = 0;

    for (const rel of stale) {
      const newWeight = rel.weight * HEBBIAN_CONFIG.decayRate;

      if (newWeight < HEBBIAN_CONFIG.minWeight) {
        // Prune very weak relations
        this.db.raw.prepare("DELETE FROM relations WHERE id = ?").run(rel.id);
        pruned++;
      } else {
        // Decay weight
        this.db.raw.prepare(
          "UPDATE relations SET weight = ?, last_accessed_at = ? WHERE id = ?"
        ).run(newWeight, now, rel.id);
        decayed++;
      }
    }

    return { decayed, pruned };
  }

  /**
   * Detect co-occurrences in a fact and reinforce
   */
  reinforceFromFact(factId: string, entities: string[]): void {
    try {
      if (entities.length < 2) return;

      // Reinforce all pairs (N×N-1)/2 relations
      for (let i = 0; i < entities.length; i++) {
        for (let j = i + 1; j < entities.length; j++) {
          this.reinforceRelation(entities[i], entities[j], "co-occurs");
          // Bidirectional
          this.reinforceRelation(entities[j], entities[i], "co-occurs");
        }
      }
    } catch (err) {
      console.error("[hebbian] reinforceFromFact failed:", err);
    }
  }

  /**
   * Get stats on relation strengths
   */
  getStats(): RelationStats {
    try {
      const all = this.db.raw.prepare("SELECT weight FROM relations").all() as Array<{ weight: number }>;
      
      const stats: RelationStats = {
        total: all.length,
        strong: 0,
        weak: 0,
        decayed: 0,
      };

      for (const rel of all) {
        if (rel.weight >= 1.0) stats.strong++;
        else if (rel.weight < 0.5) stats.weak++;
      }

      return stats;
    } catch (err) {
      console.error("[hebbian] getStats failed:", err);
      return { total: 0, strong: 0, weak: 0, decayed: 0 };
    }
  }

  /**
   * Get strongest relations for an entity (for contextual recall)
   */
  getStrongestRelations(entity: string, limit = 5): Array<{ target_id: string; weight: number; relation: string }> {
    return this.db.raw.prepare(
      `SELECT target_id, weight, relation FROM relations 
       WHERE source_id = ? 
       ORDER BY weight DESC 
       LIMIT ?`
    ).all(entity, limit) as Array<{ target_id: string; weight: number; relation: string }>;
  }
}
