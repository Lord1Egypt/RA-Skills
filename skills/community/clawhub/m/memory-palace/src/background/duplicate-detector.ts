/**
 * Duplicate Detector
 *
 * Detects and handles duplicate memories before storage.
 */

import type { Memory } from '../types.js';

/**
 * Similarity thresholds
 */
const SIMILARITY_THRESHOLDS = {
  /** Skip writing, consider duplicate */
  skip: 0.95,
  /** Prompt user for merge decision */
  merge: 0.85,
};

/**
 * Detection options
 */
export interface DuplicateDetectionOptions {
  /** Similarity threshold for skip (default: 0.95) */
  skipThreshold?: number;
  /** Similarity threshold for merge prompt (default: 0.85) */
  mergeThreshold?: number;
  /** Whether to skip detection (e.g., user explicitly wants new memory) */
  skipDetection?: boolean;
  /** Search function to find similar memories */
  searchFn: (query: string, topK: number) => Promise<{ memory: Memory; score: number }[]>;
}

/**
 * Detection result
 */
export interface DuplicateDetectionResult {
  /** Whether this is a duplicate */
  isDuplicate: boolean;
  /** Similarity score (0-1) */
  similarity: number;
  /** Similar memory found (if any) */
  similarMemory?: Memory;
  /** Recommended action */
  action: 'create' | 'skip' | 'merge';
}

/**
 * Merge options
 */
export interface MergeOptions {
  /** Original memory */
  original: Memory;
  /** New content to merge */
  newContent: string;
  /** New tags to merge */
  newTags?: string[];
  /** New importance */
  newImportance?: number;
}

/**
 * Duplicate Detector
 */
export class DuplicateDetector {
  private skipThreshold: number;
  private mergeThreshold: number;

  constructor(skipThreshold = 0.95, mergeThreshold = 0.85) {
    this.skipThreshold = skipThreshold;
    this.mergeThreshold = mergeThreshold;
  }

  /**
   * Detect if content is duplicate
   */
  async detect(content: string, options: DuplicateDetectionOptions): Promise<DuplicateDetectionResult> {
    // Skip detection if requested
    if (options.skipDetection) {
      return {
        isDuplicate: false,
        similarity: 0,
        action: 'create',
      };
    }

    const skipThreshold = options.skipThreshold ?? this.skipThreshold;
    const mergeThreshold = options.mergeThreshold ?? this.mergeThreshold;

    // Search for similar memories
    const results = await options.searchFn(content, 5);

    if (results.length === 0) {
      return {
        isDuplicate: false,
        similarity: 0,
        action: 'create',
      };
    }

    // Get highest similarity
    const topResult = results[0];
    const similarity = topResult.score;

    // Determine action based on similarity
    if (similarity >= skipThreshold) {
      return {
        isDuplicate: true,
        similarity,
        similarMemory: topResult.memory,
        action: 'skip',
      };
    }

    if (similarity >= mergeThreshold) {
      return {
        isDuplicate: true,
        similarity,
        similarMemory: topResult.memory,
        action: 'merge',
      };
    }

    return {
      isDuplicate: false,
      similarity,
      action: 'create',
    };
  }

  /**
   * Merge two memories
   */
  merge(options: MergeOptions): Partial<Memory> {
    const { original, newContent, newTags = [], newImportance } = options;

    // Merge content
    const mergedContent = `${original.content}\n\n补充：${newContent}`;

    // Merge tags (dedupe)
    const mergedTags = [...new Set([...original.tags, ...newTags])];

    // Take higher importance
    const mergedImportance = newImportance !== undefined
      ? Math.max(original.importance, newImportance)
      : original.importance;

    return {
      content: mergedContent,
      tags: mergedTags,
      importance: mergedImportance,
      updatedAt: new Date(),
    };
  }

  /**
   * Calculate text similarity (fallback when vector search unavailable)
   */
  calculateTextSimilarity(a: string, b: string): number {
    // Simple word overlap similarity
    const wordsA = new Set(a.toLowerCase().split(/\s+/).filter(w => w.length > 2));
    const wordsB = new Set(b.toLowerCase().split(/\s+/).filter(w => w.length > 2));

    if (wordsA.size === 0 || wordsB.size === 0) {
      return 0;
    }

    const intersection = new Set([...wordsA].filter(w => wordsB.has(w)));
    const union = new Set([...wordsA, ...wordsB]);

    return intersection.size / union.size;
  }
}

/**
 * Create a DuplicateDetector instance
 */
export function createDuplicateDetector(): DuplicateDetector {
  return new DuplicateDetector();
}