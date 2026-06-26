/**
 * Memory Compression
 * 
 * Compress and summarize older memories to save space while preserving key information.
 */

import type { Memory } from '../types.js';

/**
 * Compression strategy
 */
export type CompressionStrategy = 
  | 'summarize'     // Generate summary of multiple memories
  | 'merge'        // Merge similar memories
  | 'archive'      // Move to archive (less accessible)
  | 'prune';       // Remove low-importance details

/**
 * Compression result
 */
export interface CompressionResult {
  /** Original memory IDs */
  originalIds: string[];
  
  /** Compressed memory (if any) */
  compressedMemory?: Memory;
  
  /** Strategy used */
  strategy: CompressionStrategy;
  
  /** Space saved (in characters) */
  spaceSaved: number;
  
  /** Compression ratio */
  ratio: number;
}

/**
 * Compression options
 */
export interface CompressionOptions {
  /** Minimum age in days before compression */
  minAgeDays?: number;
  
  /** Minimum importance threshold */
  importanceThreshold?: number;
  
  /** Strategies to apply (in order) */
  strategies?: CompressionStrategy[];
  
  /** Maximum memories to compress in one run */
  maxMemories?: number;
}

/**
 * Memory compressor
 */
export class MemoryCompressor {
  /**
   * Compress memories based on options
   */
  async compress(memories: Memory[], options: CompressionOptions = {}): Promise<CompressionResult[]> {
    const minAgeDays = options.minAgeDays || 30;
    const importanceThreshold = options.importanceThreshold || 0.3;
    const strategies = options.strategies || ['summarize', 'merge', 'archive'];
    const maxMemories = options.maxMemories || 100;
    
    const results: CompressionResult[] = [];
    const now = new Date();
    const cutoffDate = new Date(now.getTime() - minAgeDays * 24 * 60 * 60 * 1000);
    
    // Filter memories eligible for compression
    const eligible = memories.filter(m => 
      m.status === 'active' &&
      m.updatedAt < cutoffDate &&
      m.importance < importanceThreshold
    ).slice(0, maxMemories);
    
    // Group by tags for merging
    const tagGroups = this.groupByTags(eligible);
    
    // Apply strategies
    for (const strategy of strategies) {
      for (const group of tagGroups) {
        if (group.length < 2) continue;
        
        const result = await this.applyStrategy(group, strategy);
        if (result) {
          results.push(result);
        }
      }
    }
    
    return results;
  }
  
  /**
   * Group memories by common tags
   */
  private groupByTags(memories: Memory[]): Memory[][] {
    const groups = new Map<string, Memory[]>();
    
    for (const memory of memories) {
      // Use first tag as grouping key, or 'untagged'
      const key = memory.tags[0] || 'untagged';
      
      if (!groups.has(key)) {
        groups.set(key, []);
      }
      groups.get(key)!.push(memory);
    }
    
    return Array.from(groups.values());
  }
  
  /**
   * Apply a compression strategy to a group of memories
   */
  private async applyStrategy(memories: Memory[], strategy: CompressionStrategy): Promise<CompressionResult | null> {
    switch (strategy) {
      case 'summarize':
        return this.summarize(memories);
      case 'merge':
        return this.merge(memories);
      case 'archive':
        return this.archive(memories);
      case 'prune':
        return this.prune(memories);
      default:
        return null;
    }
  }
  
  /**
   * Summarize multiple memories into one
   */
  private async summarize(memories: Memory[]): Promise<CompressionResult> {
    const totalSize = memories.reduce((sum, m) => sum + m.content.length, 0);
    
    // Create a summary memory
    const summaryContent = this.generateSummary(memories);
    
    const compressedMemory: Memory = {
      id: `compressed-${Date.now()}`,
      content: summaryContent,
      summary: `Compressed from ${memories.length} memories`,
      tags: this.mergeTags(memories),
      importance: Math.max(...memories.map(m => m.importance)),
      status: 'active',
      source: 'system',
      location: memories[0]?.location || 'default',
      createdAt: memories[0]?.createdAt || new Date(),
      updatedAt: new Date(),
    };
    
    return {
      originalIds: memories.map(m => m.id),
      compressedMemory,
      strategy: 'summarize',
      spaceSaved: totalSize - summaryContent.length,
      ratio: summaryContent.length / totalSize,
    };
  }
  
  /**
   * Merge similar memories
   */
  private async merge(memories: Memory[]): Promise<CompressionResult> {
    const totalSize = memories.reduce((sum, m) => sum + m.content.length, 0);
    
    // Combine contents with timestamps
    const mergedContent = memories
      .sort((a, b) => a.createdAt.getTime() - b.createdAt.getTime())
      .map(m => `[${m.createdAt.toISOString().split('T')[0]}] ${m.content}`)
      .join('\n\n---\n\n');
    
    const compressedMemory: Memory = {
      id: `merged-${Date.now()}`,
      content: mergedContent,
      summary: `Merged from ${memories.length} memories`,
      tags: this.mergeTags(memories),
      importance: Math.max(...memories.map(m => m.importance)),
      status: 'active',
      source: 'system',
      location: memories[0]?.location || 'default',
      createdAt: memories[0]?.createdAt || new Date(),
      updatedAt: new Date(),
    };
    
    return {
      originalIds: memories.map(m => m.id),
      compressedMemory,
      strategy: 'merge',
      spaceSaved: totalSize - mergedContent.length,
      ratio: mergedContent.length / totalSize,
    };
  }
  
  /**
   * Archive old memories
   */
  private async archive(memories: Memory[]): Promise<CompressionResult> {
    for (const memory of memories) {
      memory.status = 'archived';
      memory.updatedAt = new Date();
    }
    
    return {
      originalIds: memories.map(m => m.id),
      strategy: 'archive',
      spaceSaved: 0,
      ratio: 1,
    };
  }
  
  /**
   * Prune low-importance content
   */
  private async prune(memories: Memory[]): Promise<CompressionResult> {
    const totalSize = memories.reduce((sum, m) => sum + m.content.length, 0);
    let prunedSize = 0;
    
    for (const memory of memories) {
      // Remove repetitive phrases and filler words
      const originalLength = memory.content.length;
      memory.content = this.pruneContent(memory.content);
      prunedSize += originalLength - memory.content.length;
      memory.updatedAt = new Date();
    }
    
    return {
      originalIds: memories.map(m => m.id),
      strategy: 'prune',
      spaceSaved: prunedSize,
      ratio: (totalSize - prunedSize) / totalSize,
    };
  }
  
  /**
   * Generate a summary from multiple memories
   */
  private generateSummary(memories: Memory[]): string {
    const dateRange = this.getDateRange(memories);
    const topics = this.extractTopics(memories);
    const keyPoints = this.extractKeyPoints(memories);
    
    const parts: string[] = [];
    
    parts.push(`## Summary (${dateRange})`);
    parts.push('');
    parts.push(`This summary covers ${memories.length} related memories.`);
    parts.push('');
    
    if (topics.length > 0) {
      parts.push('**Topics:** ' + topics.join(', '));
      parts.push('');
    }
    
    parts.push('**Key Points:**');
    for (const point of keyPoints.slice(0, 5)) {
      parts.push('- ' + point);
    }
    
    return parts.join('\n');
  }
  
  /**
   * Get date range string
   */
  private getDateRange(memories: Memory[]): string {
    const dates = memories.map(m => m.createdAt.getTime()).sort((a, b) => a - b);
    const start = new Date(dates[0]).toISOString().split('T')[0];
    const end = new Date(dates[dates.length - 1]).toISOString().split('T')[0];
    return start === end ? start : `${start} to ${end}`;
  }
  
  /**
   * Extract topics from memories
   */
  private extractTopics(memories: Memory[]): string[] {
    const tagFreq = new Map<string, number>();
    
    for (const memory of memories) {
      for (const tag of memory.tags) {
        tagFreq.set(tag, (tagFreq.get(tag) || 0) + 1);
      }
    }
    
    return Array.from(tagFreq.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([tag]) => tag);
  }
  
  /**
   * Extract key points from memories
   */
  private extractKeyPoints(memories: Memory[]): string[] {
    const points: string[] = [];
    
    for (const memory of memories) {
      // Use summary if available
      if (memory.summary) {
        points.push(memory.summary);
        continue;
      }
      
      // Extract first sentence or line
      const firstSentence = memory.content.split(/[.!?\n]/)[0];
      if (firstSentence && firstSentence.length > 20) {
        points.push(firstSentence);
      }
    }
    
    return points;
  }
  
  /**
   * Merge tags from multiple memories
   */
  private mergeTags(memories: Memory[]): string[] {
    const tags = new Set<string>();
    for (const memory of memories) {
      for (const tag of memory.tags) {
        tags.add(tag);
      }
    }
    return Array.from(tags);
  }
  
  /**
   * Prune content by removing filler and redundancy
   */
  private pruneContent(content: string): string {
    // Remove excessive whitespace
    let pruned = content.replace(/\s+/g, ' ');
    
    // Remove common filler phrases
    const fillerPatterns = [
      /\b(basically|actually|honestly|literally|just|really|very|quite|rather)\b/gi,
      /\b(I\s+think|I\s+believe|it\s+seems|it\s+appears)\b/gi,
      /\b(in\s+order\s+to|due\s+to\s+the\s+fact\s+that|at\s+this\s+point\s+in\s+time)\b/gi,
    ];
    
    for (const pattern of fillerPatterns) {
      pruned = pruned.replace(pattern, '');
    }
    
    // Clean up
    pruned = pruned.replace(/\s+/g, ' ').trim();
    
    return pruned;
  }
}