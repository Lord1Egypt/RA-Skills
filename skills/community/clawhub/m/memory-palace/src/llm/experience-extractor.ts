/**
 * Memory Palace v1.1 - ExperienceExtractor
 * 
 * Extract reusable experiences and lessons from memories using LLM.
 * Identifies patterns, best practices, and applicable scenarios.
 */

import type { Memory } from '../types.js';
import type { SubagentClient } from './subagent-client.js';
import type { ExtractedExperience, ExtractOptions, LLMResult } from './types.js';
import { defaultClient } from './subagent-client.js';

/**
 * ExperienceExtractor - Extract experiences from memories
 * 
 * Features:
 * - Identify success patterns (best practices)
 * - Extract lessons from failures
 * - Discover reusable patterns
 * - Determine applicable scenarios
 */
export class ExperienceExtractor {
  private client: SubagentClient;

  constructor(client?: SubagentClient) {
    this.client = client ?? defaultClient;
  }

  /**
   * Extract experiences from multiple memories
   * 
   * @param memories Memories to analyze
   * @param options Extraction options
   * @returns Array of extracted experiences
   */
  async extract(
    memories: Memory[],
    options?: ExtractOptions
  ): Promise<LLMResult<ExtractedExperience[]>> {
    if (memories.length === 0) {
      return {
        success: true,
        data: [],
        duration: 0,
      };
    }

    // Format memories for LLM
    const memoriesText = this.formatMemories(memories);
    
    // Build prompt
    const prompt = this.buildPrompt(memoriesText, options);

    // Call LLM
    const result = await this.client.callJSONWithFallback<ExtractedExperience[]>(
      {
        task: prompt,
        timeoutSeconds: 60, // Batch processing needs more time
        maxRetries: 2,
      },
      () => this.fallbackExtract(memories)
    );

    if (result.success && result.data) {
      // Validate and limit results
      result.data = this.validateResults(result.data, options?.maxExperiences);
    }

    return result;
  }

  /**
   * Extract experiences from a single memory
   */
  async extractOne(memory: Memory): Promise<LLMResult<ExtractedExperience[]>> {
    return this.extract([memory]);
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
        return `[${index + 1}] ${date}${tags}\n${m.content}`;
      })
      .join('\n\n');
  }

  /**
   * Build the LLM prompt
   */
  private buildPrompt(memoriesText: string, options?: ExtractOptions): string {
    const focusInstruction = options?.focusArea
      ? `重点关注领域: ${options.focusArea}\n\n`
      : '';

    return `${focusInstruction}请从以下记忆中提取可复用的经验和教训：

${memoriesText}

请识别：
1. 成功的经验（最佳实践）
2. 失败的教训
3. 可复用的模式
4. 适用场景

以 JSON 数组格式返回：
[
  {
    "experience": "经验描述",
    "context": "适用场景",
    "lessons": ["教训1", "教训2"],
    "bestPractices": ["最佳实践1", "最佳实践2"],
    "relatedTopics": ["相关主题1"]
  }
]

仅返回 JSON 数组，不要解释。如果没有可提取的经验，返回空数组 []。`;
  }

  /**
   * Validate and limit results
   */
  private validateResults(
    experiences: ExtractedExperience[],
    maxExperiences?: number
  ): ExtractedExperience[] {
    const validated = experiences.map(exp => ({
      experience: exp.experience || '未命名经验',
      context: exp.context || '通用场景',
      lessons: Array.isArray(exp.lessons) ? exp.lessons : [],
      bestPractices: Array.isArray(exp.bestPractices) ? exp.bestPractices : [],
      relatedTopics: Array.isArray(exp.relatedTopics) ? exp.relatedTopics : [],
    }));

    return maxExperiences ? validated.slice(0, maxExperiences) : validated;
  }

  /**
   * Fallback extraction when LLM is unavailable
   */
  private fallbackExtract(memories: Memory[]): ExtractedExperience[] {
    const experiences: ExtractedExperience[] = [];
    
    // Simple pattern-based extraction
    for (const memory of memories) {
      const content = memory.content.toLowerCase();
      
      // Look for success indicators
      if (content.includes('成功') || content.includes('完成') || content.includes('解决')) {
        experiences.push({
          experience: `成功经验: ${memory.content.substring(0, 100)}...`,
          context: '基于成功模式识别',
          lessons: [],
          bestPractices: [memory.content.substring(0, 50)],
          relatedTopics: memory.tags,
        });
      }
      
      // Look for failure indicators
      if (content.includes('失败') || content.includes('错误') || content.includes('问题')) {
        experiences.push({
          experience: `教训总结: ${memory.content.substring(0, 100)}...`,
          context: '基于失败教训识别',
          lessons: [memory.content.substring(0, 50)],
          bestPractices: [],
          relatedTopics: memory.tags,
        });
      }
      
      // Look for learning indicators
      if (content.includes('学习') || content.includes('发现') || content.includes('理解')) {
        experiences.push({
          experience: `学习收获: ${memory.content.substring(0, 100)}...`,
          context: '基于学习内容识别',
          lessons: [],
          bestPractices: [],
          relatedTopics: memory.tags,
        });
      }
    }

    // Deduplicate and limit
    return this.deduplicateExperiences(experiences).slice(0, 5);
  }

  /**
   * Remove duplicate experiences
   */
  private deduplicateExperiences(experiences: ExtractedExperience[]): ExtractedExperience[] {
    const seen = new Set<string>();
    return experiences.filter(exp => {
      const key = exp.experience.substring(0, 50);
      if (seen.has(key)) {
        return false;
      }
      seen.add(key);
      return true;
    });
  }
}

/**
 * Default extractor instance
 */
export const defaultExtractor = new ExperienceExtractor();

/**
 * Quick helper for one-off extraction
 */
export async function extractExperiences(
  memories: Memory[],
  options?: ExtractOptions
): Promise<LLMResult<ExtractedExperience[]>> {
  return defaultExtractor.extract(memories, options);
}