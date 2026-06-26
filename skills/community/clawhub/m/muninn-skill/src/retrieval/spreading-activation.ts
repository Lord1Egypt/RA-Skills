/**
 * Spreading Activation via Knowledge Graph
 * 
 * Implements 2-hop graph traversal to expand initial retrieval results
 * with connected entities from the knowledge graph.
 * 
 * Based on: arXiv:2512.15922 - "Leveraging Spreading Activation for Improved Document Retrieval"
 */

import type { Memory } from '../storage/index.js';
import { RelationshipStore, Relationship } from '../storage/relationship-store.js';
import { EntityStore, Entity } from '../storage/entity-store.js';

export interface SpreadingActivationOptions {
  /** Maximum hops for graph traversal (default: 2) */
  maxHops: number;
  /** Decay factor per hop (default: 0.5) */
  decayFactor: number;
  /** Maximum neighbors per entity (default: 10) */
  maxNeighbors: number;
  /** Minimum activation threshold (default: 0.25) */
  minActivation: number;
}

export interface NeighborResult {
  entityId: string;
  entityName: string;
  activation: number;
  relationship: Relationship;
}

const DEFAULT_OPTIONS: SpreadingActivationOptions = {
  maxHops: 2,
  decayFactor: 0.5,
  maxNeighbors: 10,
  minActivation: 0.25
};

/**
 * Get all neighbors (connected entities) for a given entity
 * 
 * Note: Relationships store entity NAMES (not IDs) as source/target for co_occurs_with edges.
 * This function looks up by name to match our edge storage convention.
 */
function getNeighbors(
  entity: Entity,
  relationshipStore: RelationshipStore,
  maxNeighbors: number
): NeighborResult[] {
  const neighbors: NeighborResult[] = [];
  
  // Get outgoing relationships (entity name as source)
  // For co_occurs_with edges, source/target are entity names, not IDs
  const outgoing = relationshipStore.getBySource(entity.name);
  for (const rel of outgoing) {
    if (rel.supersededBy) continue;
    if (rel.type !== 'co_occurs_with') continue;  // Only use co-occurrence edges
    neighbors.push({
      entityId: rel.target,
      entityName: rel.target,  // Target is an entity name
      activation: rel.confidence || 1.0,
      relationship: rel
    });
  }
  
  // Get incoming relationships (entity name as target)
  const incoming = relationshipStore.getByTarget(entity.name);
  for (const rel of incoming) {
    if (rel.supersededBy) continue;
    if (rel.type !== 'co_occurs_with') continue;
    neighbors.push({
      entityId: rel.source,
      entityName: rel.source,  // Source is an entity name
      activation: rel.confidence || 1.0,
      relationship: rel
    });
  }
  
  // Sort by confidence and limit
  neighbors.sort((a, b) => b.activation - a.activation);
  return neighbors.slice(0, maxNeighbors);
}

/**
 * Recursive spreading activation from an entity
 */
async function spreadFromEntity(
  entity: Entity,
  currentActivation: number,
  currentHop: number,
  options: SpreadingActivationOptions,
  activated: Map<string, { activation: number; sourceRel: Relationship }>,
  relationshipStore: RelationshipStore,
  entityStore: EntityStore
): Promise<void> {
  // Base cases
  if (currentHop > options.maxHops) return;
  if (currentActivation < options.minActivation) return;
  
  // Get neighbors
  const neighbors = getNeighbors(entity, relationshipStore, options.maxNeighbors);
  
  for (const neighbor of neighbors) {
    // Calculate new activation (decay per hop)
    const newActivation = currentActivation * options.decayFactor;
    
    // Skip if below threshold
    if (newActivation < options.minActivation) continue;
    
    // Update activation if higher than existing
    const existing = activated.get(neighbor.entityId);
    if (!existing || newActivation > existing.activation) {
      activated.set(neighbor.entityId, {
        activation: newActivation,
        sourceRel: neighbor.relationship
      });
      
      // Recursively spread from this neighbor
      // Try to resolve the neighbor entity
      const neighborEntity = entityStore.findEntity(neighbor.entityName);
      if (neighborEntity) {
        await spreadFromEntity(
          neighborEntity,
          newActivation,
          currentHop + 1,
          options,
          activated,
          relationshipStore,
          entityStore
        );
      }
    }
  }
}

/**
 * Get memories for activated entities
 */
async function getActivatedMemories(
  activated: Map<string, { activation: number; sourceRel: Relationship }>,
  entityStore: EntityStore,
  relationshipStore: RelationshipStore,
  allMemories: Memory[],
  minActivation: number
): Promise<Memory[]> {
  const activatedMemories: Memory[] = [];
  
  // Build a map of entity name -> memory
  const memoryByEntity = new Map<string, Memory[]>();
  for (const mem of allMemories) {
    for (const entityName of mem.entities) {
      const key = entityName.toLowerCase();
      if (!memoryByEntity.has(key)) {
        memoryByEntity.set(key, []);
      }
      memoryByEntity.get(key)!.push(mem);
    }
  }
  
  // For each activated entity, find memories
  const seenMemoryIds = new Set<string>();
  
  for (const [entityId, { activation }] of activated) {
    if (activation < minActivation) continue;
    
    // Skip if this is a memory ID (starts with m_)
    if (entityId.startsWith('m_')) continue;
    
    // Find entity by ID or name
    let entity = entityStore.getById(entityId);
    if (!entity) {
      entity = entityStore.getByName(entityId);
    }
    if (!entity) {
      entity = entityStore.findEntity(entityId);
    }
    
    if (entity) {
      // Find memories containing this entity
      for (const mem of allMemories) {
        if (seenMemoryIds.has(mem.id)) continue;
        
        const memEntities = mem.entities.map(e => e.toLowerCase());
        if (memEntities.includes(entity.name.toLowerCase())) {
          seenMemoryIds.add(mem.id);
          activatedMemories.push({
            ...mem,
            salience: Math.max(mem.salience || 0.5, activation) // Boost by activation
          });
        }
      }
    }
  }
  
  return activatedMemories;
}

/**
 * Merge initial results with activated neighbors, boosting by activation score
 */
function mergeWithActivation(
  initialResults: Memory[],
  activatedMemories: Memory[],
  options: SpreadingActivationOptions
): Memory[] {
  const resultMap = new Map<string, Memory & { _activationBoost: number }>();
  
  // Add initial results
  for (const mem of initialResults) {
    resultMap.set(mem.id, { ...mem, _activationBoost: 1.0 });
  }
  
  // Merge activated memories
  for (const mem of activatedMemories) {
    const existing = resultMap.get(mem.id);
    if (!existing) {
      // New memory from spreading activation
      const boost = Math.max(mem.salience || 0.5, 0.25);
      resultMap.set(mem.id, { ...mem, _activationBoost: boost });
    } else {
      // Already in results - boost if activation is higher
      existing._activationBoost = Math.max(existing._activationBoost, mem.salience || 0.5);
    }
  }
  
  // Sort by activation boost (descending), then by original salience
  const results = Array.from(resultMap.values());
  results.sort((a, b) => {
    if (Math.abs(b._activationBoost - a._activationBoost) > 0.1) {
      return b._activationBoost - a._activationBoost;
    }
    return (b.salience || 0.5) - (a.salience || 0.5);
  });
  
  return results;
}

/**
 * Main spreading activation function
 * 
 * Takes initial retrieval results and expands them via 2-hop graph traversal
 * to capture related entities that weren't in the initial query results.
 * 
 * @param initialResults - Initial BM25 + Vector search results
 * @param relationshipStore - The knowledge graph relationship store
 * @param entityStore - The entity store
 * @param allMemories - All available memories for finding neighbor memories
 * @param options - Configuration options
 * @returns Expanded results with graph neighbors
 */
export async function spreadActivation(
  initialResults: Memory[],
  relationshipStore: RelationshipStore,
  entityStore: EntityStore,
  allMemories: Memory[],
  options: Partial<SpreadingActivationOptions> = {}
): Promise<Memory[]> {
  const opts = { ...DEFAULT_OPTIONS, ...options };
  
  if (initialResults.length === 0) {
    return [];
  }
  
  console.log(`[SpreadingActivation] Starting with ${initialResults.length} initial results`);
  
  // Phase 1: Seed with initial results
  // Extract entities from initial results and start spreading from each
  const activated = new Map<string, { activation: number; sourceRel: Relationship }>();
  
  for (const mem of initialResults) {
    // Add initial memory with activation 1.0
    activated.set(mem.id, { activation: 1.0, sourceRel: null as any });
    
    // Spread from each entity in the memory
    for (const entityName of mem.entities) {
      const entity = entityStore.findEntity(entityName);
      if (entity) {
        await spreadFromEntity(
          entity,
          1.0,           // Initial activation
          1,              // First hop
          opts,
          activated,
          relationshipStore,
          entityStore
        );
      }
    }
  }
  
  console.log(`[SpreadingActivation] Activated ${activated.size} entities`);
  
  // Phase 2: Collect memories for activated entities
  const activatedMemories = await getActivatedMemories(
    activated,
    entityStore,
    relationshipStore,
    allMemories,
    opts.minActivation
  );
  
  console.log(`[SpreadingActivation] Found ${activatedMemories.length} neighbor memories`);
  
  // Phase 3: Merge and return
  const merged = mergeWithActivation(initialResults, activatedMemories, opts);
  
  console.log(`[SpreadingActivation] Returning ${merged.length} total results`);
  
  return merged;
}

/**
 * Simple version that only uses relationship store (for compatibility)
 */
export async function spreadActivationSimple(
  initialResults: Memory[],
  relationshipStore: RelationshipStore,
  options: Partial<SpreadingActivationOptions> = {}
): Promise<Memory[]> {
  const opts = { ...DEFAULT_OPTIONS, ...options };
  
  if (initialResults.length === 0) {
    return [];
  }
  
  // For simple version, we return initial results with a flag
  // Full version needs entity store for proper implementation
  return initialResults;
}
