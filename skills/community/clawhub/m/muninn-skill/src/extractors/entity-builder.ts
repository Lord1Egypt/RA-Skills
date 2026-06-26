/**
 * Canonical Entity List Builder
 * 
 * Scans memories and builds a canonical entity list with:
 * - Entity extraction (NER + LLM)
 * - Alias clustering
 * - Manual merge/dedup support
 */

import fs from 'fs';
import path from 'path';

const ENTITY_CACHE_PATH = '/tmp/muninn-entity-cache.json';

export interface CanonicalEntity {
  id: string;
  name: string;
  type: 'person' | 'org' | 'project' | 'location' | 'event' | 'concept' | 'other';
  aliases: string[];
  mentionCount: number;
  firstMentioned: string;
  lastMentioned: string;
  confidence: number;
  merged?: boolean;
  mergedInto?: string;
}

export interface EntityCache {
  entities: Record<string, CanonicalEntity>;
  aliasToEntity: Record<string, string>; // alias -> entityId
  lastId: number;
}

// Global cache
let cache: EntityCache | null = null;

function loadCache(): EntityCache {
  if (cache) return cache;
  
  if (fs.existsSync(ENTITY_CACHE_PATH)) {
    try {
      const data = JSON.parse(fs.readFileSync(ENTITY_CACHE_PATH, 'utf-8'));
      cache = {
        entities: data.entities || {},
        aliasToEntity: data.aliasToEntity || {},
        lastId: data.lastId || 0
      };
      return cache;
    } catch (e) {
      // Corrupted, start fresh
    }
  }
  
  cache = {
    entities: {},
    aliasToEntity: {},
    lastId: 0
  };
  return cache;
}

function saveCache(): void {
  if (!cache) return;
  fs.writeFileSync(ENTITY_CACHE_PATH, JSON.stringify(cache, null, 2));
}

function generateId(type: string): string {
  const c = loadCache();
  c.lastId++;
  const prefix = {
    person: 'PERSON',
    org: 'ORG',
    project: 'PROJECT',
    location: 'LOC',
    event: 'EVENT',
    concept: 'CONCEPT',
    other: 'ENTITY'
  }[type] || 'ENTITY';
  return `${prefix}_${String(c.lastId).padStart(3, '0')}`;
}

/**
 * Register a new entity or add alias to existing
 */
export function registerEntity(
  name: string,
  type: CanonicalEntity['type'],
  timestamp?: string
): CanonicalEntity {
  const c = loadCache();
  const normalizedName = name.trim().toLowerCase();
  
  // Check if already exists as alias
  const existingId = c.aliasToEntity[normalizedName];
  if (existingId) {
    const existing = c.entities[existingId];
    if (existing) {
      existing.mentionCount++;
      existing.lastMentioned = timestamp || new Date().toISOString();
      saveCache();
      return existing;
    }
  }
  
  // Check if similar name exists (fuzzy match)
  for (const [id, entity] of Object.entries(c.entities)) {
    if (entity.merged) continue;
    
    // Check if names are similar
    if (isSimilarName(normalizedName, entity.name.toLowerCase())) {
      // Add as alias
      entity.aliases.push(name);
      c.aliasToEntity[normalizedName] = entity.id;
      entity.mentionCount++;
      entity.lastMentioned = timestamp || new Date().toISOString();
      saveCache();
      return entity;
    }
  }
  
  // Create new entity
  const id = generateId(type);
  const entity: CanonicalEntity = {
    id,
    name: name.trim(),
    type,
    aliases: [name],
    mentionCount: 1,
    firstMentioned: timestamp || new Date().toISOString(),
    lastMentioned: timestamp || new Date().toISOString(),
    confidence: 1.0
  };
  
  c.entities[id] = entity;
  c.aliasToEntity[normalizedName] = id;
  saveCache();
  
  return entity;
}

/**
 * Add alias to existing entity
 */
export function addAlias(entityId: string, alias: string): boolean {
  const c = loadCache();
  const entity = c.entities[entityId];
  if (!entity) return false;
  
  const normalizedAlias = alias.trim().toLowerCase();
  
  // Check if alias already mapped
  const existingId = c.aliasToEntity[normalizedAlias];
  if (existingId && existingId !== entityId) {
    // Alias belongs to another entity - would need merge
    return false;
  }
  
  if (!entity.aliases.includes(alias)) {
    entity.aliases.push(alias);
  }
  c.aliasToEntity[normalizedAlias] = entityId;
  saveCache();
  return true;
}

/**
 * Find entity by name or alias
 */
export function findEntity(nameOrAlias: string): CanonicalEntity | null {
  const c = loadCache();
  const normalized = nameOrAlias.trim().toLowerCase();
  
  // Check alias map
  const entityId = c.aliasToEntity[normalized];
  if (entityId) {
    const entity = c.entities[entityId];
    if (entity && !entity.merged) return entity;
  }
  
  // Fuzzy search
  for (const entity of Object.values(c.entities)) {
    if (entity.merged) continue;
    if (isSimilarName(normalized, entity.name.toLowerCase())) {
      return entity;
    }
    for (const alias of entity.aliases) {
      if (isSimilarName(normalized, alias.toLowerCase())) {
        return entity;
      }
    }
  }
  
  return null;
}

/**
 * Get all entities
 */
export function getAllEntities(): CanonicalEntity[] {
  const c = loadCache();
  return Object.values(c.entities).filter(e => !e.merged);
}

/**
 * Get entities by type
 */
export function getEntitiesByType(type: CanonicalEntity['type']): CanonicalEntity[] {
  return getAllEntities().filter(e => e.type === type);
}

/**
 * Merge entity A into entity B
 */
export function mergeEntities(sourceId: string, targetId: string): boolean {
  const c = loadCache();
  const source = c.entities[sourceId];
  const target = c.entities[targetId];
  
  if (!source || !target) return false;
  
  // Move all aliases to target
  for (const alias of source.aliases) {
    if (!target.aliases.includes(alias)) {
      target.aliases.push(alias);
    }
    c.aliasToEntity[alias.toLowerCase()] = targetId;
  }
  
  // Update mention count
  target.mentionCount += source.mentionCount;
  
  // Mark source as merged
  source.merged = true;
  source.mergedInto = targetId;
  
  saveCache();
  return true;
}

/**
 * Extract entities from text using LLM
 */
export async function extractEntitiesFromText(
  text: string,
  timestamp?: string
): Promise<CanonicalEntity[]> {
  const prompt = `Extract all named entities from the following text. Return JSON array with objects containing: name, type (person|org|project|location|event|concept|other).

Text: ${text}

Entities (JSON array):`;

  try {
    const response = await fetch('http://localhost:11434/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'qwen2.5:1.5b',
        prompt,
        stream: false,
        options: { num_predict: 500, temperature: 0.1 }
      })
    });
    
    const data = await response.json() as { response?: string; thinking?: string };
    const output = data.response || data.thinking || '';
    
    // Parse JSON array from response
    const jsonMatch = output.match(/\[[\s\S]*\]/);
    if (!jsonMatch) return [];
    
    const entities = JSON.parse(jsonMatch[0]);
    const registered: CanonicalEntity[] = [];
    
    for (const e of entities) {
      if (e.name && e.type) {
        const registered_entity = registerEntity(
          e.name,
          e.type as CanonicalEntity['type'],
          timestamp
        );
        registered.push(registered_entity);
      }
    }
    
    return registered;
  } catch (e) {
    console.error('Entity extraction error:', e);
    return [];
  }
}

/**
 * Scan all memories and build entity list
 */
export async function scanMemoriesForEntities(
  memories: Array<{ content: string; timestamp?: string }>
): Promise<{
  total: number;
  newEntities: number;
  entities: CanonicalEntity[];
}> {
  let newEntities = 0;
  const beforeCount = getAllEntities().length;
  
  for (const memory of memories) {
    const extracted = await extractEntitiesFromText(memory.content, memory.timestamp);
    newEntities += extracted.length;
  }
  
  const afterCount = getAllEntities().length;
  
  return {
    total: afterCount,
    newEntities: afterCount - beforeCount,
    entities: getAllEntities()
  };
}

/**
 * Export entity list for review
 */
export function exportEntityList(): {
  entities: CanonicalEntity[];
  statistics: {
    total: number;
    byType: Record<string, number>;
    topMentioned: CanonicalEntity[];
  };
} {
  const entities = getAllEntities();
  
  const byType: Record<string, number> = {};
  for (const entity of entities) {
    byType[entity.type] = (byType[entity.type] || 0) + 1;
  }
  
  const topMentioned = [...entities]
    .sort((a, b) => b.mentionCount - a.mentionCount)
    .slice(0, 10);
  
  return {
    entities,
    statistics: {
      total: entities.length,
      byType,
      topMentioned
    }
  };
}

/**
 * Clear cache (for testing)
 */
export function clearCache(): void {
  cache = null;
  if (fs.existsSync(ENTITY_CACHE_PATH)) {
    fs.unlinkSync(ENTITY_CACHE_PATH);
  }
}

// Fuzzy name matching
function isSimilarName(a: string, b: string): boolean {
  // Exact match
  if (a === b) return true;
  
  // One contains the other (e.g., "BHP" in "BHP Billiton")
  if (a.includes(b) || b.includes(a)) return true;
  
  // Common nicknames
  const nicknames: Record<string, string[]> = {
    'william': ['will', 'bill', 'billy'],
    'elizabeth': ['liz', 'beth', 'betty', 'eliza'],
    'michael': ['mike', 'mikey'],
    'jennifer': ['jen', 'jenny'],
    'katherine': ['kate', 'kathy', 'katie'],
    'robert': ['rob', 'bob', 'bobby'],
    'richard': ['rick', 'dick', 'rich'],
    'charles': ['charlie', 'chuck'],
    'margaret': ['maggie', 'meg', 'peggy'],
    'patricia': ['pat', 'patty'],
    'david': ['dave', 'davey'],
    'james': ['jim', 'jimmy', 'jamie'],
    'caroline': ['carol', 'carrie'],
    'melanie': ['mel', 'melody']
  };
  
  const aLower = a.toLowerCase();
  const bLower = b.toLowerCase();
  
  for (const [full, nicks] of Object.entries(nicknames)) {
    if ((aLower === full && nicks.includes(bLower)) ||
        (bLower === full && nicks.includes(aLower)) ||
        (nicks.includes(aLower) && nicks.includes(bLower))) {
      return true;
    }
  }
  
  // Levenshtein distance for short names
  if (a.length <= 5 && b.length <= 5) {
    const distance = levenshteinDistance(a, b);
    if (distance <= 1) return true;
  }
  
  return false;
}

function levenshteinDistance(a: string, b: string): number {
  const matrix: number[][] = [];
  
  for (let i = 0; i <= b.length; i++) {
    matrix[i] = [i];
  }
  
  for (let j = 0; j <= a.length; j++) {
    matrix[0][j] = j;
  }
  
  for (let i = 1; i <= b.length; i++) {
    for (let j = 1; j <= a.length; j++) {
      if (b.charAt(i - 1) === a.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(
          matrix[i - 1][j - 1] + 1,
          matrix[i][j - 1] + 1,
          matrix[i - 1][j] + 1
        );
      }
    }
  }
  
  return matrix[b.length][a.length];
}