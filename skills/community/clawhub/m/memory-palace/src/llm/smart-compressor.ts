/**
 * Memory Palace v1.1 - SmartCompressor
 * 
 * Intelligent memory compression using LLM.
 * Compresses old or related memories while preserving key information.
 */

import type { Memory } from '../types.js';
import type { SubagentClient } from './subagent-client.js';
import type { CompressedMemory, CompressionOptions, LLMResult } from './types.js';
import { defaultClient } from './subagent-client.js';

/**
 * SmartCompressor - Compress memories intelligently
 * 
 * Features:
 * - Merge related memories
 * - Preserve key information
 * - Calculate compression ratio
 * - Support for batch processing
 */
export class SmartCompressor {
  private client: SubagentClient;

  constructor(client?: SubagentClient) {
    this.client = client ?? defaultClient;
  }

  /**
   * Compress multiple memories into one
   * 
   * @param memories Memories to compress
   * @param options Compression options
   * @returns Compressed memory result
   */
  async compress(
    memories: Memory[],
    options?: CompressionOptions
  ): Promise<LLMResult<CompressedMemory>> {
    const minMemories = options?.minMemories ?? 2;
    
    if (memories.length < minMemories) {
      return {
        success: false,
        error: `Need at least ${minMemories} memories to compress`,
        duration: 0,
      };
    }

    // Format memories for LLM
    const memoriesText = this.formatMemories(memories);
    
    // Build prompt
    const prompt = this.buildPrompt(memoriesText, options);

    // Call LLM
    const result = await this.client.callJSONWithFallback<CompressedMemory>(
      {
        task: prompt,
        timeoutSeconds: 60, // Compression takes more time
        maxRetries: 2,
      },
      () => this.fallbackCompress(memories, options)
    );

    if (result.success && result.data) {
      // Add original IDs (ensure they're set)
      result.data.originalIds = memories.map(m => m.id);
      // Ensure compression ratio is calculated
      if (!result.data.compressionRatio) {
        result.data.compressionRatio = this.calculateRatio(
          memoriesText.length,
          result.data.compressedContent?.length || 0
        );
      }
      // Ensure compressedContent exists
      if (!result.data.compressedContent) {
        result.data.compressedContent = memories.map(m => m.content).join(' ');
      }
      // Ensure preservedKeyInfo exists
      if (!result.data.preservedKeyInfo) {
        result.data.preservedKeyInfo = [];
      }
      // Ensure summary exists
      if (!result.data.summary) {
        result.data.summary = `${memories.length} 条记忆合并`;
      }
    }

    return result;
  }

  /**
   * Check if memories should be compressed (similarity check)
   */
  async shouldCompress(memories: Memory[]): Promise<boolean> {
    if (memories.length < 2) return false;
    
    // Check for common tags or topics
    const allTags = memories.flatMap(m => m.tags);
    const uniqueTags = new Set(allTags);
    
    // If more than 50% tag overlap, consider compressing
    if (uniqueTags.size < allTags.length * 0.5) {
      return true;
    }
    
    // Check for similar locations
    const locations = new Set(memories.map(m => m.location));
    if (locations.size === 1) {
      return true;
    }
    
    return false;
  }

  /**
   * Format memories for LLM input
   */
  private formatMemories(memories: Memory[]): string {
    return memories
      .map((m, index) => {
        const date = m.createdAt instanceof Date
          ? m.createdAt.toISOString().split('T')[0]
          : new Date(m.createdAt).toISOString().split('T')[0];
        const tags = m.tags.length > 0 ? ` [${m.tags.join(', ')}]` : '';
        const summary = m.summary ? `\n摘要: ${m.summary}` : '';
        return `[${index + 1}] ${date}${tags}\n内容: ${m.content}${summary}`;
      })
      .join('\n\n');
  }

  /**
   * Build the LLM prompt
   */
  private buildPrompt(memoriesText: string, options?: CompressionOptions): string {
    const preserveInstruction = options?.preservePhrases
      ? `必须保留的关键词: ${options.preservePhrases.join(', ')}\n`
      : '';

    return `${preserveInstruction}请将以下多条相关记忆压缩为一条，保留关键信息：

${memoriesText}

返回 JSON：
{
  "compressedContent": "压缩后的内容（合并重复，保留关键信息）",
  "preservedKeyInfo": ["保留的关键信息1", "保留的关键信息2"],
  "summary": "整体摘要（一句话）"
}

仅返回 JSON，不要解释。`;
  }

  /**
   * Calculate compression ratio
   */
  private calculateRatio(originalLength: number, compressedLength: number): number {
    if (originalLength === 0) return 1;
    if (compressedLength === 0) return 1;
    // Return ratio as a decimal (e.g., 0.5 means compressed is half the original size)
    const ratio = Math.round((compressedLength / originalLength) * 100) / 100;
    // Ensure ratio is always positive
    return Math.max(0.01, ratio);
  }

  /**
   * Fallback compression when LLM is unavailable
   */
  private fallbackCompress(
    memories: Memory[],
    options?: CompressionOptions
  ): CompressedMemory {
    // Simple concatenation with deduplication
    const allContent: string[] = [];
    const allTags: string[] = [];
    const allKeyInfo: string[] = [];

    for (const memory of memories) {
      // Add unique content
      const sentences = memory.content.split(/[。.！!？?]/).filter(s => s.trim());
      for (const sentence of sentences) {
        const trimmed = sentence.trim();
        if (!allContent.some(c => c.includes(trimmed) || trimmed.includes(c))) {
          allContent.push(trimmed);
        }
      }
      
      // Collect tags
      allTags.push(...memory.tags);
      
      // Use summary if available
      if (memory.summary) {
        allKeyInfo.push(memory.summary);
      }
    }

    // Compress content
    const maxContentLength = options?.maxContentLength ?? 500;
    let compressedContent = allContent.join('。');
    
    if (compressedContent.length > maxContentLength) {
      compressedContent = compressedContent.substring(0, maxContentLength) + '...';
    }

    // Deduplicate tags
    const uniqueTags = [...new Set(allTags)];

    // Create summary
    const dateRange = this.getDateRange(memories);
    const summary = `${dateRange}期间 ${memories.length} 条记忆合并`;

    return {
      originalIds: memories.map(m => m.id),
      compressedContent,
      preservedKeyInfo: allKeyInfo.slice(0, 5),
      compressionRatio: this.calculateRatio(
        memories.reduce((sum, m) => sum + m.content.length, 0),
        compressedContent.length
      ),
      summary,
    };
  }

  /**
   * Get date range string from memories
   */
  private getDateRange(memories: Memory[]): string {
    const dates = memories.map(m => {
      const d = m.createdAt instanceof Date ? m.createdAt : new Date(m.createdAt);
      return d.getTime();
    }).sort((a, b) => a - b);

    if (dates.length === 0) return '未知';

    const first = new Date(dates[0]);
    const last = new Date(dates[dates.length - 1]);
    
    const firstStr = first.toISOString().split('T')[0];
    const lastStr = last.toISOString().split('T')[0];

    if (firstStr === lastStr) {
      return firstStr;
    }
    return `${firstStr} 至 ${lastStr}`;
  }
}

/**
 * Default compressor instance
 */
export const defaultCompressor = new SmartCompressor();

/**
 * Quick helper for one-off compression
 */
export async function compressMemories(
  memories: Memory[],
  options?: CompressionOptions
): Promise<LLMResult<CompressedMemory>> {
  return defaultCompressor.compress(memories, options);
}