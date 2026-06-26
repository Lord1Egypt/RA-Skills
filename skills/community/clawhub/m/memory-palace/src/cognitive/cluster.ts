/**
 * Topic Clustering
 * 
 * Automatically group memories by topics/themes.
 */

import type { Memory } from '../types.js';

/**
 * Cluster of related memories
 */
export interface MemoryCluster {
  /** Cluster ID */
  id: string;
  
  /** Cluster label/topic */
  label: string;
  
  /** Memory IDs in this cluster */
  memoryIds: string[];
  
  /** Common tags in this cluster */
  commonTags: string[];
  
  /** Cluster keywords */
  keywords: string[];
  
  /** Average importance */
  avgImportance: number;
}

/**
 * Clustering options
 */
export interface ClusteringOptions {
  /** Minimum cluster size */
  minClusterSize?: number;
  
  /** Maximum clusters to return */
  maxClusters?: number;
  
  /** Similarity threshold (0-1) */
  similarityThreshold?: number;
}

/**
 * Simple topic clustering based on tags and content keywords
 */
export class TopicCluster {
  /**
   * Cluster memories by topics
   */
  async cluster(memories: Memory[], options: ClusteringOptions = {}): Promise<MemoryCluster[]> {
    const minSize = options.minClusterSize || 2;
    const maxClusters = options.maxClusters || 20;
    const threshold = options.similarityThreshold || 0.3;
    
    // Build tag-based clusters
    const tagClusters = new Map<string, Set<string>>();
    
    for (const memory of memories) {
      for (const tag of memory.tags) {
        if (!tagClusters.has(tag)) {
          tagClusters.set(tag, new Set());
        }
        tagClusters.get(tag)!.add(memory.id);
      }
    }
    
    // Convert to cluster objects
    const clusters: MemoryCluster[] = [];
    const usedIds = new Set<string>();
    
    // Sort tags by cluster size
    const sortedTags = Array.from(tagClusters.entries())
      .sort((a, b) => b[1].size - a[1].size);
    
    for (const [tag, ids] of sortedTags) {
      if (ids.size < minSize) continue;
      if (clusters.length >= maxClusters) break;
      
      // Skip if most memories are already clustered
      const newIds = Array.from(ids).filter(id => !usedIds.has(id));
      if (newIds.length < minSize) continue;
      
      const clusterMemories = memories.filter(m => newIds.includes(m.id));
      const keywords = this.extractKeywords(clusterMemories);
      const avgImportance = clusterMemories.reduce((sum, m) => sum + m.importance, 0) / clusterMemories.length;
      
      clusters.push({
        id: `cluster-${clusters.length + 1}`,
        label: tag,
        memoryIds: newIds,
        commonTags: [tag],
        keywords,
        avgImportance,
      });
      
      newIds.forEach(id => usedIds.add(id));
    }
    
    // Create "uncategorized" cluster for remaining memories
    const uncategorized = memories.filter(m => !usedIds.has(m.id));
    if (uncategorized.length > 0) {
      clusters.push({
        id: `cluster-${clusters.length + 1}`,
        label: 'uncategorized',
        memoryIds: uncategorized.map(m => m.id),
        commonTags: [],
        keywords: this.extractKeywords(uncategorized),
        avgImportance: uncategorized.reduce((sum, m) => sum + m.importance, 0) / uncategorized.length,
      });
    }
    
    return clusters;
  }
  
  /**
   * Extract keywords from memories
   */
  private extractKeywords(memories: Memory[]): string[] {
    const wordFreq = new Map<string, number>();
    const stopWords = this.getStopWords();

    for (const memory of memories) {
      const words = memory.content.toLowerCase()
        .replace(/[^\w\s\u4e00-\u9fff]/g, ' ')
        .split(/\s+/)
        .filter(w => w.length > 1 && !stopWords.has(w));

      for (const word of words) {
        wordFreq.set(word, (wordFreq.get(word) || 0) + 1);
      }
    }

    return Array.from(wordFreq.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([word]) => word);
  }

  /**
   * Extract keywords from a single content string
   * @param content - Content to extract keywords from
   * @param topN - Number of top keywords to return (default: 5)
   * @returns Array of top keywords
   */
  extractKeywordsFromContent(content: string, topN: number = 5): string[] {
    const wordFreq = new Map<string, number>();
    const stopWords = this.getStopWords();

    const words = content.toLowerCase()
      .replace(/[^\w\s\u4e00-\u9fff]/g, ' ')
      .split(/\s+/)
      .filter(w => w.length > 1 && !stopWords.has(w));

    for (const word of words) {
      wordFreq.set(word, (wordFreq.get(word) || 0) + 1);
    }

    return Array.from(wordFreq.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, topN)
      .map(([word]) => word);
  }

  /**
   * Get stop words set
   */
  private getStopWords(): Set<string> {
    return new Set([
      // English stop words
      'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
      'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
      'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'to', 'of',
      'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through',
      'during', 'before', 'after', 'above', 'below', 'between', 'under',
      'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
      'why', 'how', 'all', 'each', 'few', 'more', 'most', 'other', 'some',
      'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
      'very', 'just', 'and', 'but', 'if', 'or', 'because', 'until', 'while',
      'this', 'that', 'these', 'those', 'what', 'which', 'who', 'whom',
      // Chinese stop words
      '的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一',
      '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有',
      '看', '好', '自己', '这', '那', '她', '他', '它', '们', '这个', '那个',
    ]);
  }
  
  /**
   * Find similar memories to a given memory
   */
  findSimilar(memory: Memory, allMemories: Memory[], threshold: number = 0.3): Memory[] {
    const similar: Memory[] = [];
    
    for (const other of allMemories) {
      if (other.id === memory.id) continue;
      
      const similarity = this.calculateSimilarity(memory, other);
      if (similarity >= threshold) {
        similar.push(other);
      }
    }
    
    return similar.sort((a, b) => 
      this.calculateSimilarity(memory, b) - this.calculateSimilarity(memory, a)
    );
  }
  
  /**
   * Calculate similarity between two memories
   */
  private calculateSimilarity(a: Memory, b: Memory): number {
    // Tag similarity (Jaccard coefficient)
    const tagSetA = new Set(a.tags);
    const tagSetB = new Set(b.tags);
    const tagIntersection = new Set([...tagSetA].filter(t => tagSetB.has(t)));
    const tagUnion = new Set([...tagSetA, ...tagSetB]);
    const tagSimilarity = tagUnion.size > 0 ? tagIntersection.size / tagUnion.size : 0;
    
    // Location similarity
    const locationSimilarity = a.location === b.location ? 1 : 0;
    
    // Importance similarity
    const importanceSimilarity = 1 - Math.abs(a.importance - b.importance);
    
    // Weighted combination
    return tagSimilarity * 0.5 + locationSimilarity * 0.2 + importanceSimilarity * 0.3;
  }
}