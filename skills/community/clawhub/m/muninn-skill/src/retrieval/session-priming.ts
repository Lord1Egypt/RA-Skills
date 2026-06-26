/**
 * Session Priming (Working Memory Buffer)
 * 
 * At session start, preloads "stale but important" entities - those
 * mentioned frequently in past sessions but not recently.
 * 
 * This ensures continuity between sessions by surfacing relevant
 * context that would otherwise be forgotten.
 * 
 * Based on: MemGPT/Letta architecture for working memory
 */

import type { Memory } from '../storage/index.js';
import { EntityStore } from '../storage/entity-store.js';
import { RelationshipStore } from '../storage/relationship-store.js';

export interface SessionPrimingOptions {
  /** Minimum session mentions to be considered "important" (default: 3) */
  minMentions: number;
  /** Hours since last mention to be considered "stale" (default: 48) */
  staleHours: number;
  /** Maximum entities to preload (default: 5) */
  maxEntities: number;
  /** Maximum memories per entity to retrieve (default: 2) */
  memoriesPerEntity: number;
}

const DEFAULT_OPTIONS: SessionPrimingOptions = {
  minMentions: 3,
  staleHours: 48,
  maxEntities: 5,
  memoriesPerEntity: 2
};

/**
 * Find entities that are "stale but important"
 * - Mentioned in multiple sessions (>= minMentions)
 * - Not mentioned recently (>= staleHours ago)
 */
export interface StaleImportantEntity {
  entity: {
    id: string;
    name: string;
    type: string;
    mentions: number;
  };
  lastMentioned: Date;
  hoursSinceMention: number;
}

/**
 * Query for stale-but-important entities
 * Returns entities that were frequently referenced but haven't been
 * mentioned recently - good candidates for session context
 */
export async function findStaleImportantEntities(
  entityStore: EntityStore,
  options: Partial<SessionPrimingOptions> = {}
): Promise<StaleImportantEntity[]> {
  const opts = { ...DEFAULT_OPTIONS, ...options };
  const now = new Date();
  const staleThreshold = new Date(now.getTime() - opts.staleHours * 60 * 60 * 1000);
  
  // Get all entities
  const allEntities = entityStore.getAll();
  
  // Filter for stale but important
  const staleImportant: StaleImportantEntity[] = [];
  
  for (const entity of allEntities) {
    const lastSeen = new Date(entity.lastSeen);
    const hoursSince = (now.getTime() - lastSeen.getTime()) / (1000 * 60 * 60);
    
    // Check if stale AND important
    if (hoursSince >= opts.staleHours && entity.mentions >= opts.minMentions) {
      staleImportant.push({
        entity: {
          id: entity.id,
          name: entity.name,
          type: entity.type,
          mentions: entity.mentions
        },
        lastMentioned: lastSeen,
        hoursSinceMention: hoursSince
      });
    }
  }
  
  // Sort by importance (mentions * recency)
  staleImportant.sort((a, b) => {
    // Score: more mentions = more important, but stale = needs priming
    const scoreA = a.entity.mentions * (1 / (1 + a.hoursSinceMention / 24));
    const scoreB = b.entity.mentions * (1 / (1 + b.hoursSinceMention / 24));
    return scoreB - scoreA;
  });
  
  return staleImportant.slice(0, opts.maxEntities);
}

/**
 * Get all sessions an entity was mentioned in
 */
function getEntitySessions(
  relationshipStore: RelationshipStore,
  entityId: string
): string[] {
  const sessions = new Set<string>();
  
  // Check as source
  const asSource = relationshipStore.getBySource(entityId);
  for (const rel of asSource) {
    if (rel.sessionId) {
      sessions.add(rel.sessionId);
    }
  }
  
  // Check as target
  const asTarget = relationshipStore.getByTarget(entityId);
  for (const rel of asTarget) {
    if (rel.sessionId) {
      sessions.add(rel.sessionId);
    }
  }
  
  return Array.from(sessions);
}

/**
 * Cohesion Query - main function for session priming
 * 
 * Finds entities that are frequently mentioned across sessions but have
 * gone stale, then retrieves recent memories about them.
 * 
 * @param entityStore - Entity store for finding stale-important entities
 * @param relationshipStore - Relationship store for session tracking
 * @param recallFn - Function to recall memories (context, options) => Promise<Memory[]>
 * @param options - Configuration options
 * @returns Array of primed memories for session context
 */
export async function cohesionQuery(
  entityStore: EntityStore,
  relationshipStore: RelationshipStore,
  recallFn: (context: string, options?: any) => Promise<Memory[]>,
  options: Partial<SessionPrimingOptions> = {}
): Promise<{
  primedMemories: Memory[];
  staleEntities: StaleImportantEntity[];
  summary: string;
}> {
  const opts = { ...DEFAULT_OPTIONS, ...options };
  
  // Find stale-but-important entities
  const staleEntities = await findStaleImportantEntities(entityStore, opts);
  
  if (staleEntities.length === 0) {
    return {
      primedMemories: [],
      staleEntities: [],
      summary: 'No stale-but-important entities found for session priming.'
    };
  }
  
  // Collect recent memories for each entity
  const primedMemories: Memory[] = [];
  const seenIds = new Set<string>();
  
  for (const staleEntity of staleEntities) {
    // Query for recent memories about this entity
    const memories = await recallFn(staleEntity.entity.name, {
      limit: opts.memoriesPerEntity
    });
    
    for (const mem of memories) {
      if (!seenIds.has(mem.id)) {
        seenIds.add(mem.id);
        primedMemories.push(mem);
      }
    }
  }
  
  // Generate summary
  const entityNames = staleEntities.map(e => e.entity.name).join(', ');
  const summary = `Session Priming: Preloaded ${primedMemories.length} memories about stale entities (${entityNames})`;
  
  return {
    primedMemories,
    staleEntities,
    summary
  };
}

/**
 * Simple cohesion query that works with memory store
 * 
 * @param entityStore - Entity store
 * @param relationshipStore - Relationship store  
 * @param memories - All available memories
 * @param options - Configuration options
 * @returns Primed memories
 */
export async function simpleCohesionQuery(
  entityStore: EntityStore,
  relationshipStore: RelationshipStore,
  memories: Memory[],
  options: Partial<SessionPrimingOptions> = {}
): Promise<{
  primedMemories: Memory[];
  staleEntities: StaleImportantEntity[];
}> {
  const opts = { ...DEFAULT_OPTIONS, ...options };
  
  // Find stale-but-important entities
  const staleEntities = await findStaleImportantEntities(entityStore, opts);
  
  if (staleEntities.length === 0) {
    return { primedMemories: [], staleEntities: [] };
  }
  
  // Find memories containing these entities
  const primedMemories: Memory[] = [];
  const seenIds = new Set<string>();
  
  for (const staleEntity of staleEntities) {
    const entityName = staleEntity.entity.name.toLowerCase();
    
    // Find memories containing this entity
    for (const mem of memories) {
      if (seenIds.has(mem.id)) continue;
      
      const memEntities = mem.entities.map(e => e.toLowerCase());
      if (memEntities.includes(entityName)) {
        seenIds.add(mem.id);
        // Boost salience for primed memories
        primedMemories.push({
          ...mem,
          salience: Math.min(1.0, (mem.salience || 0.5) * 1.5) // 50% boost
        });
      }
    }
  }
  
  // Sort by boosted salience
  primedMemories.sort((a, b) => (b.salience || 0.5) - (a.salience || 0.5));
  
  return {
    primedMemories,
    staleEntities
  };
}

/**
 * Get session cohesion score
 * Measures how well connected the current session is to past sessions
 */
export function calculateSessionCohesion(
  currentSessionEntities: string[],
  staleEntities: StaleImportantEntity[]
): number {
  if (currentSessionEntities.length === 0 || staleEntities.length === 0) {
    return 0;
  }
  
  const currentSet = new Set(currentSessionEntities.map(e => e.toLowerCase()));
  let overlap = 0;
  
  for (const stale of staleEntities) {
    if (currentSet.has(stale.entity.name.toLowerCase())) {
      overlap++;
    }
  }
  
  return overlap / staleEntities.length;
}
