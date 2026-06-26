/**
 * Multi-Hop Retrieval - Token-Efficient Implementation
 * 
 * Combines:
 * 1. Entity-centric retrieval with temporal filtering
 * 2. PPR graph traversal (zero tokens)
 * 3. Spreading activation (zero tokens)
 * 4. IRCoT fallback (tokens only when needed)
 * 
 * Based on: Ernie's multi-hop research (2026-02-27)
 */

import type { Memory } from '../storage/index.js';
import { EntityStore } from '../storage/entity-store.js';
import { RelationshipStore } from '../storage/relationship-store.js';
import { spreadActivation } from './spreading-activation.js';
import { findPaths, Path } from './graph-traversal.js';
import { extractTemporalMetadata } from '../extractors/temporal-metadata.js';

// ============================================================================
// TYPES
// ============================================================================

export interface MultiHopOptions {
  /** Maximum memories to return (default: 20) */
  limit?: number;
  /** Entity-centric retrieval budget per entity (default: 50) */
  entityBudget?: number;
  /** PPR damping factor (default: 0.85) */
  pprDamping?: number;
  /** PPR iterations (default: 20) */
  pprIterations?: number;
  /** Spreading activation decay (default: 0.5) */
  activationDecay?: number;
  /** Maximum spreading hops (default: 2) */
  maxActivationHops?: number;
  /** Confidence threshold for IRCoT fallback (default: 0.7) */
  fallbackThreshold?: number;
  /** Enable IRCoT fallback (default: true) */
  enableFallback?: boolean;
  /** Entity store for graph operations */
  entityStore?: EntityStore;
  /** Relationship store for graph operations */
  relationshipStore?: RelationshipStore;
  /** All memories for spreading activation */
  allMemories?: Memory[];
}

export interface MultiHopResult {
  memories: Memory[];
  confidence: number;
  usedFallback: boolean;
  method: string;
  /** Paths found between entities (for multi-hop queries) */
  paths?: Path[];
  /** Entity pairs that were queried for paths */
  pathEntities?: string[];
}

export interface TemporalConstraint {
  after?: Date;
  before?: Date;
  on?: Date;
  raw?: string;
}

// ============================================================================
// KEYWORD EXPANSION (rule-based, zero tokens)
// ============================================================================

const KEYWORD_EXPANSIONS: Record<string, string[]> = {
  // Work/career
  'job': ['job', 'work', 'career', 'position', 'role', 'employment', 'occupation'],
  'work': ['work', 'job', 'career', 'position', 'role', 'employment'],
  'career': ['career', 'job', 'work', 'profession', 'occupation', 'position'],
  
  // Emotions
  'worried': ['worried', 'concerned', 'anxious', 'stressed', 'nervous', 'uneasy'],
  'happy': ['happy', 'pleased', 'glad', 'delighted', 'joyful', 'content'],
  'sad': ['sad', 'upset', 'unhappy', 'depressed', 'down', 'melancholy'],
  'angry': ['angry', 'frustrated', 'annoyed', 'irritated', 'mad', 'upset'],
  'excited': ['excited', 'thrilled', 'eager', 'enthusiastic', 'pumped'],
  
  // Communication
  'said': ['said', 'mentioned', 'told', 'stated', 'expressed', 'noted'],
  'asked': ['asked', 'inquired', 'questioned', 'requested', 'wondered'],
  'discussed': ['discussed', 'talked about', 'covered', 'addressed', 'reviewed'],
  
  // Time
  'recently': ['recently', 'lately', 'newly', 'just', 'freshly'],
  'previously': ['previously', 'before', 'earlier', 'formerly', 'once'],
  
  // Projects
  'project': ['project', 'initiative', 'task', 'assignment', 'endeavor'],
  'goal': ['goal', 'objective', 'target', 'aim', 'purpose', 'mission'],
  
  // Deadlines/Timing
  'deadline': ['deadline', 'due', 'due date', 'completion', 'finish', 'target date'],
  'when': ['when', 'date', 'time', 'schedule', 'timeline'],
  'june': ['june', 'jun', '6'],
  'july': ['july', 'jul', '7'],
  
  // Technical
  'bug': ['bug', 'issue', 'problem', 'error', 'defect', 'glitch'],
  'feature': ['feature', 'capability', 'functionality', 'ability', 'option'],
  'api': ['api', 'endpoint', 'interface', 'service', 'integration'],
  'website': ['website', 'site', 'web', 'webpage', 'landing page'],
  
  // People
  'team': ['team', 'group', 'squad', 'crew', 'staff', 'colleagues'],
  'client': ['client', 'customer', 'user', 'stakeholder', 'patron'],
};

/**
 * Expand keywords with synonyms (rule-based, zero tokens)
 */
function expandKeywords(keywords: string[]): string[] {
  const expanded = new Set<string>();
  
  for (const kw of keywords) {
    expanded.add(kw.toLowerCase());
    
    // Check for expansions
    const lower = kw.toLowerCase();
    if (KEYWORD_EXPANSIONS[lower]) {
      KEYWORD_EXPANSIONS[lower].forEach(e => expanded.add(e));
    }
    
    // Check if this keyword is in any expansion list
    for (const [key, values] of Object.entries(KEYWORD_EXPANSIONS)) {
      if (values.includes(lower)) {
        expanded.add(key);
        values.forEach(v => expanded.add(v));
      }
    }
  }
  
  return [...expanded];
}

// ============================================================================
// ENTITY EXTRACTION (rule-based, zero tokens)
// ============================================================================

const KNOWN_ENTITIES = [
  // People
  'Phillip', 'KakāpōHiko', 'Kakāpō', 'Hiko', 'KH',
  'Sammy Clemens', 'Sammy', 'Charlie Babbage', 'Charlie', 
  'Melvil Dewey', 'Melvil', 'Ernie Rutherford', 'Ernie',
  'Hedy Lamarr', 'Hedy', 'Caroline', 'David', 'Sarah', 'John', 'Jane',
  
  // Organizations
  'Elev8Advisory', 'BrandForge', 'Muninn', 'OpenClaw',
  'BHP', 'Google', 'Microsoft', 'Apple', 'Amazon',
  
  // Projects
  'DashClaw', 'GigHunter', 'The Shed', 'Mission Control',
  'Zto5k', 'ClawHub', 'Moltbook', 'website project',
  
  // Technologies
  'React', 'Node.js', 'PostgreSQL', 'SQLite', 'Ollama',
  'Stripe', 'TypeScript', 'JavaScript', 'Python',
  
  // Locations
  'Brisbane', 'Australia', 'Sydney', 'Melbourne',
  
  // Events
  'LGBTQ', 'LGBTQ support group',
  
  // Common entities
  'deadline', 'website', 'project',
];

// Question words to exclude from entity extraction
const QUESTION_WORDS = new Set([
  'what', 'which', 'who', 'whom', 'whose', 'where', 'when', 'why', 'how',
  'is', 'are', 'was', 'were', 'will', 'would', 'could', 'should', 'can',
  'does', 'did', 'has', 'have', 'had', 'the', 'a', 'an', 'this', 'that',
  'these', 'those', 'there', 'here', 'all', 'each', 'every', 'both',
  'few', 'more', 'most', 'other', 'some', 'such', 'no', 'any', 'only',
  'own', 'same', 'so', 'than', 'too', 'very', 'just', 'also', 'now',
]);

/**
 * Extract entities from query (rule-based, zero tokens)
 */
function extractQueryEntities(query: string): string[] {
  const found: string[] = [];
  const lower = query.toLowerCase();
  
  for (const entity of KNOWN_ENTITIES) {
    if (lower.includes(entity.toLowerCase())) {
      found.push(entity);
    }
  }
  
  // Also extract capitalized words that might be entities
  const capitalized = query.match(/\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b/g) || [];
  for (const cap of capitalized) {
    // Skip question words and common words
    if (!QUESTION_WORDS.has(cap.toLowerCase()) && !found.includes(cap) && cap.length > 2) {
      found.push(cap);
    }
  }
  
  return [...new Set(found)];
}

// ============================================================================
// TEMPORAL CONSTRAINT EXTRACTION (rule-based, zero tokens)
// ============================================================================

const TEMPORAL_PATTERNS = [
  { pattern: /after\s+(.+)/i, type: 'after' },
  { pattern: /before\s+(.+)/i, type: 'before' },
  { pattern: /since\s+(.+)/i, type: 'after' },
  { pattern: /following\s+(.+)/i, type: 'after' },
  { pattern: /prior to\s+(.+)/i, type: 'before' },
];

/**
 * Extract temporal constraints from query (rule-based, zero tokens)
 */
function extractTemporalConstraints(query: string): TemporalConstraint {
  const constraint: TemporalConstraint = {};
  
  for (const { pattern, type } of TEMPORAL_PATTERNS) {
    const match = query.match(pattern);
    if (match) {
      const eventText = match[1].trim();
      constraint.raw = eventText;
      
      // Try to parse as date
      const temporal = extractTemporalMetadata(eventText, new Date());
      if (temporal.eventTime && temporal.confidence > 0.5) {
        if (type === 'after') {
          constraint.after = new Date(temporal.eventTime);
        } else if (type === 'before') {
          constraint.before = new Date(temporal.eventTime);
        }
      }
    }
  }
  
  return constraint;
}

/**
 * Filter memories by temporal constraints
 */
function filterByTemporal(memories: Memory[], constraint: TemporalConstraint): Memory[] {
  if (!constraint.after && !constraint.before && !constraint.on) {
    return memories;
  }
  
  return memories.filter(m => {
    // Try resolved_content first (has [YYYY-MM-DD] prefix)
    let memDate: Date | null = null;
    
    if (m.resolved_content) {
      const dateMatch = m.resolved_content.match(/\[(\d{4}-\d{2}-\d{2})\]/);
      if (dateMatch) {
        memDate = new Date(dateMatch[1]);
      }
    }
    
    // Fall back to timestamp
    if (!memDate && m.timestamp) {
      memDate = new Date(m.timestamp);
    }
    
    // Fall back to created_at
    if (!memDate && (m as any).created_at) {
      memDate = new Date((m as any).created_at);
    }
    
    if (!memDate) return false;
    
    if (constraint.on) {
      return memDate.toDateString() === constraint.on.toDateString();
    }
    
    if (constraint.after && memDate <= constraint.after) {
      return false;
    }
    
    if (constraint.before && memDate >= constraint.before) {
      return false;
    }
    
    return true;
  });
}

// ============================================================================
// ENTITY-CENTRIC RETRIEVAL
// ============================================================================

/**
 * Retrieve all memories for entities, then filter and rank
 */
export async function retrieveEntityCentric(
  query: string,
  getMemoriesByEntity: (entity: string, limit: number) => Memory[],
  options: MultiHopOptions = {}
): Promise<{ memories: Memory[]; entities: string[]; temporalConstraint: TemporalConstraint }> {
  const entityBudget = options.entityBudget || 50;
  
  // Extract entities (rule-based, zero tokens)
  const entities = extractQueryEntities(query);
  
  // Extract temporal constraints (rule-based, zero tokens)
  const temporalConstraint = extractTemporalConstraints(query);
  
  // Extract keywords for filtering
  const queryWords = query.toLowerCase()
    .replace(/[?.,!]/g, '')
    .split(/\s+/)
    .filter(w => w.length > 3);
  const keywords = expandKeywords(queryWords);
  
  // Collect memories for each entity
  const allMemories: Memory[] = [];
  const seen = new Set<string>();
  
  for (const entity of entities) {
    const entityMems = getMemoriesByEntity(entity, entityBudget);
    for (const m of entityMems) {
      if (!seen.has(m.id)) {
        seen.add(m.id);
        allMemories.push(m);
      }
    }
  }
  
  // Apply temporal filtering (rule-based, zero tokens)
  let filtered = filterByTemporal(allMemories, temporalConstraint);
  
  // Apply keyword filtering
  if (keywords.length > 0) {
    filtered = filtered.filter(m => {
      const content = m.content.toLowerCase();
      return keywords.some(kw => content.includes(kw));
    });
  }
  
  // Rank by relevance
  const scored = filtered.map(m => {
    const content = m.content.toLowerCase();
    let score = m.salience || 0.5;
    
    // Boost for keyword matches
    for (const kw of keywords) {
      if (content.includes(kw)) {
        score += 0.1;
      }
    }
    
    // Boost for entity count
    const entityCount = (m.entities || []).filter(e => 
      entities.some(qe => e.toLowerCase().includes(qe.toLowerCase()))
    ).length;
    score += entityCount * 0.05;
    
    return { ...m, salience: score };
  });
  
  scored.sort((a, b) => (b.salience || 0) - (a.salience || 0));
  
  return {
    memories: scored.slice(0, options.limit || 20),
    entities,
    temporalConstraint
  };
}

// ============================================================================
// CONFIDENCE SCORING (rule-based, zero tokens)
// ============================================================================

/**
 * Compute confidence score for retrieval results
 */
function computeConfidence(
  memories: Memory[],
  query: string,
  entities: string[],
  temporalConstraint: TemporalConstraint
): number {
  if (memories.length === 0) return 0;
  
  let score = 0;
  
  // 1. Entity coverage (40%)
  const memoryEntities = new Set(
    memories.flatMap(m => (m.entities || []).map(e => e.toLowerCase()))
  );
  const queryEntitySet = new Set(entities.map(e => e.toLowerCase()));
  const entityCoverage = entities.length > 0 
    ? [...queryEntitySet].filter(e => memoryEntities.has(e)).length / queryEntitySet.size
    : 1;
  score += entityCoverage * 0.4;
  
  // 2. Temporal coverage (30%)
  if (temporalConstraint.after || temporalConstraint.before) {
    const satisfyingMemories = memories.filter(m => {
      let memDate: Date | null = null;
      
      if (m.resolved_content) {
        const dateMatch = m.resolved_content.match(/\[(\d{4}-\d{2}-\d{2})\]/);
        if (dateMatch) memDate = new Date(dateMatch[1]);
      }
      if (!memDate && m.timestamp) memDate = new Date(m.timestamp);
      if (!memDate && (m as any).created_at) memDate = new Date((m as any).created_at);
      
      if (!memDate) return false;
      if (temporalConstraint.after && memDate <= temporalConstraint.after) return false;
      if (temporalConstraint.before && memDate >= temporalConstraint.before) return false;
      return true;
    });
    score += (satisfyingMemories.length / memories.length) * 0.3;
  } else {
    score += 0.3; // No temporal constraint, full points
  }
  
  // 3. Keyword coverage (30%)
  const queryWords = query.toLowerCase()
    .replace(/[?.,!]/g, '')
    .split(/\s+/)
    .filter(w => w.length > 3);
  const keywords = expandKeywords(queryWords);
  
  const keywordMatches = keywords.filter(kw =>
    memories.some(m => m.content.toLowerCase().includes(kw))
  );
  score += (keywordMatches.length / Math.max(keywords.length, 1)) * 0.3;
  
  return score;
}

// ============================================================================
// MAIN MULTI-HOP RETRIEVAL
// ============================================================================

/**
 * Multi-hop retrieval with zero-token graph methods
 * Falls back to IRCoT only if confidence < threshold
 */
export async function multiHopRetrieval(
  query: string,
  getMemoriesByEntity: (entity: string, limit: number) => Memory[],
  options: MultiHopOptions = {}
): Promise<MultiHopResult> {
  const limit = options.limit || 20;
  const fallbackThreshold = options.fallbackThreshold || 0.7;
  
  // Phase 1: Entity-centric retrieval with temporal filtering
  const { memories: entityMemories, entities, temporalConstraint } = await retrieveEntityCentric(
    query,
    getMemoriesByEntity,
    { ...options, limit: limit * 2 } // Get more for graph expansion
  );
  
  // Phase 1.5: BFS Path Finding for multi-hop queries
  // If we have 2+ entities and stores available, find paths between them
  let foundPaths: Path[] = [];
  let pathEntities: string[] = [];
  
  if (entities.length >= 2 && options.entityStore && options.relationshipStore) {
    try {
      // Try to find paths between entity pairs
      for (let i = 0; i < entities.length; i++) {
        for (let j = i + 1; j < entities.length; j++) {
          const sourceEntity = options.entityStore.findEntity(entities[i]);
          const targetEntity = options.entityStore.findEntity(entities[j]);
          
          if (sourceEntity && targetEntity) {
            const paths = findPaths(
              sourceEntity.id,
              targetEntity.id,
              options.relationshipStore,
              { maxHops: 3, maxPaths: 5 }
            );
            
            if (paths.length > 0) {
              foundPaths.push(...paths);
              pathEntities.push(`${entities[i]} ↔ ${entities[j]}`);
              
              // Add memories from path entities to results
              for (const path of paths) {
                for (const segment of path.segments) {
                  // Get memories for target entity in each segment
                  const segMemories = getMemoriesByEntity(segment.target, 5);
                  for (const mem of segMemories) {
                    if (!entityMemories.find(m => m.id === mem.id)) {
                      entityMemories.push(mem);
                    }
                  }
                }
              }
            }
          }
        }
      }
      
      if (foundPaths.length > 0) {
        console.log(`[MultiHop] Found ${foundPaths.length} paths between ${pathEntities.join(', ')}`);
      }
    } catch (error) {
      console.error('[MultiHop] Path finding failed:', error);
    }
  }
  
  // Phase 2: Graph expansion via spreading activation (if stores available)
  let expandedMemories = entityMemories;
  
  if (options.entityStore && options.relationshipStore && options.allMemories) {
    try {
      expandedMemories = await spreadActivation(
        entityMemories,
        options.relationshipStore,
        options.entityStore,
        options.allMemories,
        {
          maxHops: options.maxActivationHops || 2,
          decayFactor: options.activationDecay || 0.5,
          maxNeighbors: 10,
          minActivation: 0.25
        }
      );
      
      // Re-filter after expansion
      expandedMemories = filterByTemporal(expandedMemories, temporalConstraint);
    } catch (error) {
      console.error('[MultiHop] Spreading activation failed:', error);
      // Continue with entity-centric results
    }
  }
  
  // Rank and limit
  expandedMemories.sort((a, b) => (b.salience || 0.5) - (a.salience || 0.5));
  const finalMemories = expandedMemories.slice(0, limit);
  
  // Compute confidence
  const confidence = computeConfidence(finalMemories, query, entities, temporalConstraint);
  
  // Check if fallback needed
  if (options.enableFallback !== false && confidence < fallbackThreshold) {
    console.log(`[MultiHop] Confidence ${confidence.toFixed(2)} < ${fallbackThreshold}, would use IRCoT fallback`);
    // Note: IRCoT fallback would go here, but we return the graph results for now
    // since IRCoT requires LLM calls
    return {
      memories: finalMemories,
      confidence,
      usedFallback: false, // Set to true when IRCoT is implemented
      method: 'entity-centric + spreading-activation (low confidence, IRCoT not implemented)',
      paths: foundPaths.length > 0 ? foundPaths : undefined,
      pathEntities: pathEntities.length > 0 ? pathEntities : undefined
    };
  }
  
  return {
    memories: finalMemories,
    confidence,
    usedFallback: false,
    method: confidence >= 0.7 
      ? 'entity-centric + temporal + spreading-activation'
      : 'entity-centric + temporal (no graph expansion)',
    paths: foundPaths.length > 0 ? foundPaths : undefined,
    pathEntities: pathEntities.length > 0 ? pathEntities : undefined
  };
}

// ============================================================================
// EXPORTS
// ============================================================================

export {
  extractQueryEntities,
  extractTemporalConstraints,
  expandKeywords,
  filterByTemporal,
  computeConfidence
};