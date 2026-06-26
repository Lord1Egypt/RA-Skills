/**
 * Conflict Detection
 * 
 * Detect contradictions and conflicts between memories.
 */

import type { Memory } from '../types.js';

/**
 * Conflict type
 */
export type ConflictType = 
  | 'contradiction'    // Direct contradiction between memories
  | 'outdated'        // Information may be outdated
  | 'duplicate'       // Similar or duplicate information
  | 'ambiguous';      // Ambiguous or unclear information

/**
 * Detected conflict
 */
export interface Conflict {
  /** Conflict ID */
  id: string;
  
  /** Conflict type */
  type: ConflictType;
  
  /** Involved memory IDs */
  memoryIds: string[];
  
  /** Confidence level (0-1) */
  confidence: number;
  
  /** Description of the conflict */
  description: string;
  
  /** Suggested resolution */
  suggestion?: string;
  
  /** Detection timestamp */
  detectedAt: Date;
}

/**
 * Conflict detection options
 */
export interface ConflictOptions {
  /** Minimum confidence to report */
  minConfidence?: number;
  
  /** Maximum conflicts to return */
  maxConflicts?: number;
  
  /** Conflict types to check */
  types?: ConflictType[];
}

/**
 * Conflict detector
 */
export class ConflictDetector {
  private conflictId = 0;
  
  /**
   * Detect conflicts among memories
   */
  async detect(memories: Memory[], options: ConflictOptions = {}): Promise<Conflict[]> {
    const minConfidence = options.minConfidence || 0.5;
    const maxConflicts = options.maxConflicts || 50;
    const types = options.types || ['contradiction', 'outdated', 'duplicate', 'ambiguous'];
    
    const conflicts: Conflict[] = [];
    
    // Check for duplicates
    if (types.includes('duplicate')) {
      conflicts.push(...await this.detectDuplicates(memories));
    }
    
    // Check for contradictions
    if (types.includes('contradiction')) {
      conflicts.push(...await this.detectContradictions(memories));
    }
    
    // Check for outdated information
    if (types.includes('outdated')) {
      conflicts.push(...await this.detectOutdated(memories));
    }
    
    // Check for ambiguous content
    if (types.includes('ambiguous')) {
      conflicts.push(...await this.detectAmbiguous(memories));
    }
    
    // Filter by confidence and limit
    return conflicts
      .filter(c => c.confidence >= minConfidence)
      .sort((a, b) => b.confidence - a.confidence)
      .slice(0, maxConflicts);
  }
  
  /**
   * Detect duplicate or highly similar memories
   */
  private async detectDuplicates(memories: Memory[]): Promise<Conflict[]> {
    const conflicts: Conflict[] = [];
    
    for (let i = 0; i < memories.length; i++) {
      for (let j = i + 1; j < memories.length; j++) {
        const memA = memories[i];
        const memB = memories[j];
        
        // Skip if either is deleted
        if (memA.status === 'deleted' || memB.status === 'deleted') continue;
        
        // Calculate content similarity
        const similarity = this.calculateContentSimilarity(memA.content, memB.content);
        
        if (similarity >= 0.8) {
          conflicts.push({
            id: `conflict-${++this.conflictId}`,
            type: 'duplicate',
            memoryIds: [memA.id, memB.id],
            confidence: similarity,
            description: `Highly similar content detected (${Math.round(similarity * 100)}% match)`,
            suggestion: 'Consider merging or deleting one of these memories',
            detectedAt: new Date(),
          });
        }
      }
    }
    
    return conflicts;
  }
  
  /**
   * Detect contradictions between memories
   */
  private async detectContradictions(memories: Memory[]): Promise<Conflict[]> {
    const conflicts: Conflict[] = [];
    
    // Contradiction patterns
    const contradictionPatterns = [
      { pattern: /\b(is|are|was|were)\s+(true|false|yes|no)\b/gi, weight: 0.8 },
      { pattern: /\b(can|cannot|can't|will|won't)\b/gi, weight: 0.6 },
      { pattern: /\b(supports?|opposes?|against?|for)\b/gi, weight: 0.5 },
    ];
    
    // Group memories by topic (using tags)
    const tagGroups = new Map<string, Memory[]>();
    for (const memory of memories) {
      if (memory.status === 'deleted') continue;
      for (const tag of memory.tags) {
        if (!tagGroups.has(tag)) {
          tagGroups.set(tag, []);
        }
        tagGroups.get(tag)!.push(memory);
      }
    }
    
    // Check for contradictions within each group
    for (const [, group] of tagGroups) {
      if (group.length < 2) continue;
      
      for (let i = 0; i < group.length; i++) {
        for (let j = i + 1; j < group.length; j++) {
          const memA = group[i];
          const memB = group[j];
          
          // Check for contradictory patterns
          for (const { pattern, weight } of contradictionPatterns) {
            const matchesA = memA.content.match(pattern);
            const matchesB = memB.content.match(pattern);
            
            if (matchesA && matchesB) {
              // Check if values are different
              const valuesA = matchesA.map(m => m.toLowerCase());
              const valuesB = matchesB.map(m => m.toLowerCase());
              
              const hasContradiction = valuesA.some(va => 
                valuesB.some(vb => va !== vb && this.areOpposites(va, vb))
              );
              
              if (hasContradiction) {
                conflicts.push({
                  id: `conflict-${++this.conflictId}`,
                  type: 'contradiction',
                  memoryIds: [memA.id, memB.id],
                  confidence: weight,
                  description: 'Potential contradiction detected in memories with same tags',
                  suggestion: 'Review and resolve the conflicting information',
                  detectedAt: new Date(),
                });
                break;
              }
            }
          }
        }
      }
    }
    
    return conflicts;
  }
  
  /**
   * Detect potentially outdated information
   */
  private async detectOutdated(memories: Memory[]): Promise<Conflict[]> {
    const conflicts: Conflict[] = [];
    const now = new Date();
    const thirtyDaysAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
    
    // Time-sensitive keywords
    const timeSensitivePatterns = [
      /\b(current|currently|now|today|this\s+week|this\s+month)\b/gi,
      /\b(latest|recent|updated|new)\b/gi,
      /\b(\d{4})\b/g, // Years
    ];
    
    for (const memory of memories) {
      if (memory.status === 'deleted') continue;
      if (memory.importance < 0.3) continue; // Skip low importance
      
      const age = now.getTime() - memory.updatedAt.getTime();
      const daysOld = age / (24 * 60 * 60 * 1000);
      
      // Check for time-sensitive content
      let hasTimeSensitive = false;
      for (const pattern of timeSensitivePatterns) {
        if (pattern.test(memory.content)) {
          hasTimeSensitive = true;
          break;
        }
      }
      
      // Flag old memories with time-sensitive content
      if (hasTimeSensitive && memory.updatedAt < thirtyDaysAgo) {
        conflicts.push({
          id: `conflict-${++this.conflictId}`,
          type: 'outdated',
          memoryIds: [memory.id],
          confidence: Math.min(1, daysOld / 90), // Older = more confident
          description: `Time-sensitive content may be outdated (${Math.round(daysOld)} days old)`,
          suggestion: 'Review and update if needed',
          detectedAt: new Date(),
        });
      }
    }
    
    return conflicts;
  }
  
  /**
   * Detect ambiguous or unclear information
   */
  private async detectAmbiguous(memories: Memory[]): Promise<Conflict[]> {
    const conflicts: Conflict[] = [];
    
    // Ambiguity patterns
    const ambiguousPatterns = [
      { pattern: /\b(maybe|perhaps|possibly|might|could|probably|likely)\b/gi, confidence: 0.4 },
      { pattern: /\b(someone|something|somewhere|sometime)\b/gi, confidence: 0.5 },
      { pattern: /\b(they|it|this|that|these|those)\b(?!\s+(is|are|was|were|means|refers))/gi, confidence: 0.3 },
      { pattern: /\?\s*$/g, confidence: 0.3 }, // Ends with question
    ];
    
    for (const memory of memories) {
      if (memory.status === 'deleted') continue;
      
      let totalConfidence = 0;
      const matches: string[] = [];
      
      for (const { pattern, confidence } of ambiguousPatterns) {
        const found = memory.content.match(pattern);
        if (found) {
          totalConfidence += confidence * found.length;
          matches.push(...found);
        }
      }
      
      if (totalConfidence >= 0.5) {
        conflicts.push({
          id: `conflict-${++this.conflictId}`,
          type: 'ambiguous',
          memoryIds: [memory.id],
          confidence: Math.min(1, totalConfidence),
          description: `Potentially ambiguous content detected: "${matches.slice(0, 3).join(', ')}"`,
          suggestion: 'Consider clarifying the ambiguous terms',
          detectedAt: new Date(),
        });
      }
    }
    
    return conflicts;
  }
  
  /**
   * Calculate content similarity between two texts
   */
  private calculateContentSimilarity(a: string, b: string): number {
    const normalize = (text: string) => 
      text.toLowerCase().replace(/[^\w\s]/g, ' ').split(/\s+/).filter(w => w.length > 2);
    
    const wordsA = new Set(normalize(a));
    const wordsB = new Set(normalize(b));
    
    const intersection = new Set([...wordsA].filter(w => wordsB.has(w)));
    const union = new Set([...wordsA, ...wordsB]);
    
    return union.size > 0 ? intersection.size / union.size : 0;
  }
  
  /**
   * Check if two values are opposites
   */
  private areOpposites(a: string, b: string): boolean {
    const opposites: [Set<string>, Set<string>][] = [
      [new Set(['true', 'yes', 'correct', 'right']), new Set(['false', 'no', 'incorrect', 'wrong'])],
      [new Set(['can', 'will', 'should', 'must']), new Set(["can't", "won't", "shouldn't", "mustn't", 'cannot'])],
      [new Set(['support', 'for', 'approve']), new Set(['oppose', 'against', 'disapprove'])],
    ];
    
    for (const [positive, negative] of opposites) {
      if ((positive.has(a) && negative.has(b)) || (negative.has(a) && positive.has(b))) {
        return true;
      }
    }
    
    return false;
  }
}