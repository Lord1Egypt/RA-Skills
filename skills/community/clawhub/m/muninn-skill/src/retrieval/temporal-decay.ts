/**
 * Temporal Decay Scorer
 * 
 * Applies exponential half-life decay to memory scores based on age.
 * Memories older than the half-life are penalized but never fully removed.
 * 
 * Also handles contradiction chains - when an entity has been superseded,
 * the entire chain is boosted to provide context.
 * 
 * Based on: "Temporal RAG: Why RAG Always Gets 'When' Questions Wrong" (SOTA Blog, Jan 2026)
 */

import type { Memory } from '../storage/index.js';
import { RelationshipStore, Relationship } from '../storage/relationship-store.js';
import { EntityStore } from '../storage/entity-store.js';

export interface TemporalDecayOptions {
  /** Half-life in days (default: 30) */
  halfLifeDays: number;
  /** Minimum score floor (default: 0.1) */
  minScore: number;
  /** Contradiction chain boost factor (default: 1.5) */
  contradictionBoost: number;
}

const DEFAULT_OPTIONS: TemporalDecayOptions = {
  halfLifeDays: 30,
  minScore: 0.1,
  contradictionBoost: 1.5
};

/**
 * Calculate decay rate from half-life
 * λ = ln(2) / half_life_days
 */
function calculateDecayRate(halfLifeDays: number): number {
  return Math.log(2) / halfLifeDays;
}

/**
 * Temporal Decay Scorer class
 */
export class TemporalDecayScorer {
  private decayRate: number;
  private options: TemporalDecayOptions;
  
  constructor(options: Partial<TemporalDecayOptions> = {}) {
    this.options = { ...DEFAULT_OPTIONS, ...options };
    this.decayRate = calculateDecayRate(this.options.halfLifeDays);
  }
  
  /**
   * Calculate temporal score for a memory
   * Score = e^(-λt) where t is age in days
   * 
   * @param memory - The memory to score
   * @param referenceDate - Reference date for calculating age (default: now)
   * @returns Score between minScore and 1.0
   */
  score(memory: Memory, referenceDate: Date = new Date()): number {
    // Get memory timestamp (use created_at if no timestamp)
    const memTime = memory.timestamp 
      ? new Date(memory.timestamp) 
      : new Date(memory.created_at);
    
    // Calculate age in days
    const ageMs = referenceDate.getTime() - memTime.getTime();
    const ageDays = ageMs / (1000 * 60 * 60 * 24);
    
    // Calculate exponential decay
    const temporalScore = Math.exp(-this.decayRate * ageDays);
    
    // Apply minimum floor
    return Math.max(temporalScore, this.options.minScore);
  }
  
  /**
   * Get the decay rate
   */
  getDecayRate(): number {
    return this.decayRate;
  }
  
  /**
   * Get the half-life in days
   */
  getHalfLifeDays(): number {
    return this.options.halfLifeDays;
  }
  
  /**
   * Apply temporal decay to an array of memories
   * 
   * @param memories - Array of memories with existing scores
   * @param scoreProperty - Property name containing the base score (default: '_finalScore')
   * @param referenceDate - Reference date for calculating age
   * @returns Memories with temporal scores applied
   */
  applyDecay<T extends Memory>(
    memories: T[],
    scoreProperty: string = '_finalScore',
    referenceDate: Date = new Date()
  ): Array<T & { _temporalScore: number; _combinedScore: number }> {
    return memories.map(mem => {
      const temporalScore = this.score(mem, referenceDate);
      const baseScore = (mem as any)[scoreProperty] || 1.0;
      const combinedScore = baseScore * temporalScore;
      
      return {
        ...mem,
        _temporalScore: temporalScore,
        _combinedScore: combinedScore
      };
    });
  }
  
  /**
   * Sort memories by combined score (base score * temporal decay)
   */
  sortByTemporalScore<T extends Memory>(
    memories: T[],
    scoreProperty: string = '_finalScore'
  ): T[] {
    const scored = this.applyDecay(memories, scoreProperty);
    scored.sort((a, b) => b._combinedScore - a._combinedScore);
    return scored;
  }
}

/**
 * Check if an entity has contradictions and get the chain
 */
export function getContradictionChain(
  entityStore: EntityStore,
  relationshipStore: RelationshipStore,
  entityName: string
): { current?: Relationship; superseded: Relationship[] } {
  const entity = entityStore.findEntity(entityName);
  if (!entity) {
    return { superseded: [] };
  }
  
  // Get all relationships for this entity
  const outgoing = relationshipStore.getBySource(entity.id);
  const incoming = relationshipStore.getByTarget(entity.id);
  
  // Find contradictions (relationships with supersededBy set)
  const superseded: Relationship[] = [];
  let current: Relationship | undefined;
  
  for (const rel of [...outgoing, ...incoming]) {
    if (rel.supersededBy) {
      // This relationship has been superseded
      const supersededRel = relationshipStore.getById(rel.supersededBy);
      if (supersededRel) {
        superseded.push(supersededRel);
      }
    } else {
      // This is the current relationship
      if (!current || new Date(rel.timestamp) > new Date(current.timestamp)) {
        current = rel;
      }
    }
  }
  
  return { current, superseded };
}

/**
 * Apply temporal decay with contradiction handling
 * 
 * @param memories - Base memories to score
 * @param baseScores - Map of memory ID to base score
 * @param entityStore - Entity store for contradiction lookup
 * @param relationshipStore - Relationship store for contradiction lookup
 * @param options - Temporal decay options
 * @returns Memories with temporal scores and contradiction boosts applied
 */
export function applyTemporalDecayWithContradictions(
  memories: Memory[],
  baseScores: Map<string, number>,
  entityStore: EntityStore,
  relationshipStore: RelationshipStore,
  options: Partial<TemporalDecayOptions> = {}
): Memory[] {
  const scorer = new TemporalDecayScorer(options);
  const referenceDate = new Date();
  
  // First, collect all entities that have contradictions
  const contradictionEntities = new Map<string, { current?: Relationship; superseded: Relationship[] }>();
  
  for (const mem of memories) {
    for (const entityName of mem.entities) {
      if (!contradictionEntities.has(entityName)) {
        const chain = getContradictionChain(entityStore, relationshipStore, entityName);
        if (chain.superseded.length > 0) {
          contradictionEntities.set(entityName, chain);
        }
      }
    }
  }
  
  // Apply temporal decay and contradiction boosts
  const scored = memories.map(mem => {
    const baseScore = baseScores.get(mem.id) || (mem.salience || 0.5);
    const temporalScore = scorer.score(mem, referenceDate);
    
    // Check if this memory's entities have contradictions
    let hasContradiction = false;
    for (const entityName of mem.entities) {
      if (contradictionEntities.has(entityName)) {
        hasContradiction = true;
        break;
      }
    }
    
    // Apply boost if entity has contradictions
    const contradictionBoost = hasContradiction ? (options.contradictionBoost || DEFAULT_OPTIONS.contradictionBoost) : 1.0;
    
    const finalScore = baseScore * temporalScore * contradictionBoost;
    
    return {
      ...mem,
      _baseScore: baseScore,
      _temporalScore: temporalScore,
      _contradictionBoost: contradictionBoost,
      _finalScore: finalScore,
      _hasContradiction: hasContradiction
    };
  });
  
  // Sort by final score
  scored.sort((a, b) => (b._finalScore || 0) - (a._finalScore || 0));
  
  // Also collect superseded memories from contradiction chains
  const additionalMemories: Memory[] = [];
  for (const [, chain] of contradictionEntities) {
    for (const superseded of chain.superseded) {
      // Find memories related to this superseded relationship
      // For now, we just flag them - full implementation would retrieve the memories
    }
  }
  
  return scored;
}

/**
 * Default scorer instance with 30-day half-life
 */
export const defaultTemporalScorer = new TemporalDecayScorer();

/**
 * Quick score function for simple use cases
 */
export function getTemporalScore(memory: Memory, halfLifeDays: number = 30): number {
  const scorer = new TemporalDecayScorer({ halfLifeDays });
  return scorer.score(memory);
}
