/**
 * Entity Tracking
 * 
 * Track entities (people, projects, concepts) mentioned across memories.
 */

import type { Memory } from '../types.js';

/**
 * Entity types
 */
export type EntityType = 'person' | 'project' | 'concept' | 'tool' | 'event' | 'location' | 'other';

/**
 * Tracked entity
 */
export interface Entity {
  /** Entity name */
  name: string;
  
  /** Entity type */
  type: EntityType;
  
  /** Memory IDs mentioning this entity */
  mentions: string[];
  
  /** First seen date */
  firstSeen: Date;
  
  /** Last seen date */
  lastSeen: Date;
  
  /** Associated tags */
  tags: string[];
  
  /** Importance score */
  importance: number;
  
  /** Related entities */
  relatedEntities: string[];
}

/**
 * Entity tracking result
 */
export interface EntityTrackingResult {
  /** All tracked entities */
  entities: Entity[];
  
  /** Entity co-occurrence map */
  coOccurrences: Map<string, Set<string>>;
}

/**
 * Simple entity tracker
 */
export class EntityTracker {
  private entityPatterns: Map<EntityType, RegExp[]>;
  
  constructor() {
    // Define patterns for different entity types
    this.entityPatterns = new Map([
      ['person', [
        /\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b/g, // Names like "John Doe"
        /\b(@[a-zA-Z0-9_]+)\b/g, // Handles like @username
      ]],
      ['project', [
        /\b([A-Z][a-zA-Z0-9]*(?:-[a-zA-Z0-9]+)*\s*(?:project|Project|PROJECT))\b/g,
        /\b(project\s+[a-zA-Z0-9-]+)\b/gi,
      ]],
      ['tool', [
        /\b([a-zA-Z0-9-]+(?:\.js|\.ts|\.py|\.go|\.rs))\b/g, // Files/libs
        /\b(npm\s+[a-zA-Z0-9-]+)\b/g,
        /\b(pip\s+[a-zA-Z0-9-]+)\b/g,
        /\b([a-zA-Z0-9-]+\s+CLI)\b/gi,
      ]],
      ['event', [
        /\b(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)\b/g, // Dates
        /\b(meeting|会议|schedule|deadline)\b/gi,
      ]],
      ['location', [
        /\b(in\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b/g,
        /\b(at\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b/g,
      ]],
      ['concept', [
        /\b([A-Z][A-Z0-9]+(?:\s+[A-Z][A-Z0-9]+)*)\b/g, // Acronyms like API, SDK
        /\b([a-z]+(?:-[a-z]+)+)\b/g, // kebab-case concepts
      ]],
    ]);
  }
  
  /**
   * Track entities across memories
   */
  async track(memories: Memory[]): Promise<EntityTrackingResult> {
    const entityMap = new Map<string, Entity>();
    const coOccurrences = new Map<string, Set<string>>();
    
    for (const memory of memories) {
      const memoryEntities = this.extractEntities(memory);
      
      // Record each entity
      for (const [name, entity] of memoryEntities) {
        if (entityMap.has(name)) {
          const existing = entityMap.get(name)!;
          existing.mentions.push(memory.id);
          existing.lastSeen = memory.updatedAt;
          existing.importance = Math.min(1, existing.importance + 0.1);
          
          // Merge tags
          for (const tag of memory.tags) {
            if (!existing.tags.includes(tag)) {
              existing.tags.push(tag);
            }
          }
        } else {
          entityMap.set(name, entity);
        }
      }
      
      // Record co-occurrences
      const entityNames = Array.from(memoryEntities.keys());
      for (let i = 0; i < entityNames.length; i++) {
        for (let j = i + 1; j < entityNames.length; j++) {
          const a = entityNames[i];
          const b = entityNames[j];
          
          if (!coOccurrences.has(a)) {
            coOccurrences.set(a, new Set());
          }
          coOccurrences.get(a)!.add(b);
          
          if (!coOccurrences.has(b)) {
            coOccurrences.set(b, new Set());
          }
          coOccurrences.get(b)!.add(a);
        }
      }
    }
    
    // Build related entities from co-occurrences
    for (const [name, entity] of entityMap) {
      entity.relatedEntities = Array.from(coOccurrences.get(name) || []);
    }
    
    return {
      entities: Array.from(entityMap.values()),
      coOccurrences,
    };
  }
  
  /**
   * Extract entities from a single memory
   */
  private extractEntities(memory: Memory): Map<string, Entity> {
    const entities = new Map<string, Entity>();
    const content = memory.content + ' ' + (memory.summary || '');
    
    for (const [type, patterns] of this.entityPatterns) {
      for (const pattern of patterns) {
        // Reset regex
        pattern.lastIndex = 0;
        
        let match;
        while ((match = pattern.exec(content)) !== null) {
          const name = match[1].trim();
          if (name.length < 2 || name.length > 50) continue;
          
          // Skip common words
          if (this.isCommonWord(name)) continue;
          
          const key = `${type}:${name.toLowerCase()}`;
          
          if (!entities.has(key)) {
            entities.set(key, {
              name,
              type,
              mentions: [memory.id],
              firstSeen: memory.createdAt,
              lastSeen: memory.updatedAt,
              tags: [...memory.tags],
              importance: 0.3,
              relatedEntities: [],
            });
          }
        }
      }
    }
    
    return entities;
  }
  
  /**
   * Check if a word is too common to be an entity
   */
  private isCommonWord(word: string): boolean {
    const commonWords = new Set([
      'the', 'The', 'a', 'A', 'an', 'An', 'is', 'Is', 'are', 'Are',
      'was', 'Was', 'were', 'Were', 'be', 'Been', 'being', 'Being',
      'have', 'Has', 'had', 'Had', 'do', 'Does', 'did', 'Did',
      'will', 'Will', 'would', 'Would', 'could', 'Could', 'should', 'Should',
      'this', 'This', 'that', 'That', 'these', 'These', 'those', 'Those',
      'in', 'In', 'at', 'At', 'on', 'On', 'by', 'By', 'for', 'For',
      'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December',
    ]);
    return commonWords.has(word);
  }
  
  /**
   * Find entities of a specific type
   */
  filterByType(entities: Entity[], type: EntityType): Entity[] {
    return entities.filter(e => e.type === type);
  }
  
  /**
   * Find entities mentioned in multiple memories
   */
  findFrequent(entities: Entity[], minMentions: number = 3): Entity[] {
    return entities.filter(e => e.mentions.length >= minMentions)
      .sort((a, b) => b.mentions.length - a.mentions.length);
  }
  
  /**
   * Find related entities
   */
  findRelated(entityName: string, entities: Entity[]): Entity[] {
    const entity = entities.find(e => e.name.toLowerCase() === entityName.toLowerCase());
    if (!entity) return [];
    
    return entities.filter(e => entity.relatedEntities.includes(e.name));
  }
}