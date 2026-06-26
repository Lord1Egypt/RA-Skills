/**
 * Memory Palace v1.1 - LLMSummarizer
 * 
 * Intelligent memory summarization using LLM.
 * Extracts key information, evaluates importance, and suggests tags.
 */

import type { SubagentClient } from './subagent-client.js';
import type { SummarizeResult, LLMResult } from './types.js';
import { defaultClient } from './subagent-client.js';

/**
 * Summarization options
 */
export interface SummarizerOptions {
  /** Include category classification */
  includeCategory?: boolean;
  /** Maximum summary length */
  maxSummaryLength?: number;
  /** Maximum key points */
  maxKeyPoints?: number;
  /** Maximum suggested tags */
  maxTags?: number;
}

/**
 * Default summarization options
 */
const DEFAULT_OPTIONS: Required<SummarizerOptions> = {
  includeCategory: true,
  maxSummaryLength: 50,
  maxKeyPoints: 5,
  maxTags: 5,
};

/**
 * LLMSummarizer - Intelligent memory summarization
 * 
 * Features:
 * - One-sentence summary generation
 * - Key points extraction
 * - Importance evaluation (0-1)
 * - Tag suggestions
 * - Category classification
 */
export class LLMSummarizer {
  private client: SubagentClient;
  private options: Required<SummarizerOptions>;

  constructor(client?: SubagentClient, options?: SummarizerOptions) {
    this.client = client ?? defaultClient;
    this.options = { ...DEFAULT_OPTIONS, ...options };
  }

  /**
   * Summarize memory content
   * 
   * @param content Memory content to summarize
   * @param options Override options
   * @returns Summarization result
   */
  async summarize(content: string, options?: Partial<SummarizerOptions>): Promise<LLMResult<SummarizeResult>> {
    const opts = { ...this.options, ...options };
    
    // Truncate content if too long
    const truncatedContent = this.truncateContent(content, 2000);
    
    // Build prompt
    const prompt = this.buildPrompt(truncatedContent, opts);
    
    // Call LLM
    const result = await this.client.callJSONWithFallback<SummarizeResult>(
      {
        task: prompt,
        timeoutSeconds: 30,
      },
      () => this.fallbackSummarize(truncatedContent)
    );

    if (result.success && result.data) {
      // Validate and sanitize result
      result.data = this.sanitizeResult(result.data, opts);
    }

    return result;
  }

  /**
   * Build the LLM prompt
   */
  private buildPrompt(content: string, opts: Required<SummarizerOptions>): string {
    const categoryInstruction = opts.includeCategory
      ? '"category": "分类（工作/生活/技术/学习/健康/财务/社交/其他）",'
      : '';

    return `请分析以下记忆内容，提取关键信息：

${content}

请以 JSON 格式返回：
{
  "summary": "一句话总结（不超过${opts.maxSummaryLength}字）",
  "keyPoints": ["要点1", "要点2", "要点3"],
  "importance": 0.8,
  "suggestedTags": ["标签1", "标签2"],
  ${categoryInstruction}
}

仅返回 JSON，不要解释。`;
  }

  /**
   * Truncate content to fit within token limits
   */
  private truncateContent(content: string, maxLength: number): string {
    if (content.length <= maxLength) {
      return content;
    }
    
    // Try to truncate at sentence boundary
    const lastPeriod = content.lastIndexOf('。', maxLength);
    const lastDot = content.lastIndexOf('.', maxLength);
    const lastQuestion = content.lastIndexOf('？', maxLength);
    const lastExclaim = content.lastIndexOf('！', maxLength);
    
    const cutPoint = Math.max(lastPeriod, lastDot, lastQuestion, lastExclaim);
    
    if (cutPoint > maxLength * 0.7) {
      return content.substring(0, cutPoint + 1);
    }
    
    return content.substring(0, maxLength) + '...';
  }

  /**
   * Sanitize and validate result
   */
  private sanitizeResult(result: SummarizeResult, opts: Required<SummarizerOptions>): SummarizeResult {
    return {
      summary: result.summary?.substring(0, opts.maxSummaryLength) || '无法总结',
      keyPoints: (result.keyPoints || []).slice(0, opts.maxKeyPoints),
      importance: Math.max(0, Math.min(1, result.importance ?? 0.5)),
      suggestedTags: (result.suggestedTags || []).slice(0, opts.maxTags),
      category: result.category || '其他',
    };
  }

  /**
   * Fallback summarization when LLM is unavailable
   */
  private fallbackSummarize(content: string): SummarizeResult {
    // Simple rule-based summarization
    const sentences = content.split(/[。.！!？?]/).filter(s => s.trim().length > 0);
    const summary = sentences.length > 0 
      ? sentences[0].trim().substring(0, 50) + (sentences[0].length > 50 ? '...' : '')
      : '内容摘要';

    // Extract simple keywords from content
    const keywords = this.extractKeywords(content);
    
    // Estimate importance based on content features
    const importance = this.estimateImportance(content);

    return {
      summary,
      keyPoints: sentences.slice(0, 3).map(s => s.trim().substring(0, 30)),
      importance,
      suggestedTags: keywords.slice(0, 5),
      category: '其他',
    };
  }

  /**
   * Extract simple keywords from content (fallback)
   */
  private extractKeywords(content: string): string[] {
    // Simple keyword extraction based on frequency
    const words = content.split(/[\s,，。.！!？?；;：:""\"'\'【】\[\]（）()]/);
    const frequency: Record<string, number> = {};
    
    for (const word of words) {
      const w = word.trim();
      if (w.length >= 2 && w.length <= 10) {
        frequency[w] = (frequency[w] || 0) + 1;
      }
    }
    
    return Object.entries(frequency)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([word]) => word);
  }

  /**
   * Estimate importance based on content features (fallback)
   */
  private estimateImportance(content: string): number {
    let score = 0.5;
    
    // Check for importance indicators
    const importantPatterns = [
      /重要|关键|必须|紧急|critical|important|urgent/i,
      /截止|deadline|due/i,
      /会议|meeting/i,
      /项目|project/i,
      /决定|decision/i,
    ];
    
    const unimportantPatterns = [
      /也许|可能|或许|maybe|might/i,
      /随便|anyway/i,
    ];

    for (const pattern of importantPatterns) {
      if (pattern.test(content)) {
        score += 0.1;
      }
    }

    for (const pattern of unimportantPatterns) {
      if (pattern.test(content)) {
        score -= 0.1;
      }
    }

    return Math.max(0, Math.min(1, score));
  }
}

/**
 * Default summarizer instance
 */
export const defaultSummarizer = new LLMSummarizer();

/**
 * Quick helper for one-off summarization
 */
export async function summarizeMemory(content: string): Promise<LLMResult<SummarizeResult>> {
  return defaultSummarizer.summarize(content);
}