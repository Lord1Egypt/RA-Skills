/**
 * Memory Palace v1.1 - ConceptExpanderLLM
 * 
 * Dynamic concept expansion using LLM for better search recall.
 * Target: 10-15s timeout with optimized prompt.
 */

import type { SubagentClient } from './subagent-client.js';
import type { ExpandedConcepts, ConceptExpandOptions, LLMResult } from './types.js';
import { defaultClient } from './subagent-client.js';

/**
 * ConceptExpanderLLM - Expand search concepts dynamically
 * 
 * Features:
 * - Expand keywords to related terms
 * - Discover related domains
 * - Support for both Chinese and English
 * - Quick response (target: 10-15s)
 */
export class ConceptExpanderLLM {
  private client: SubagentClient;
  private staticCache: Map<string, ExpandedConcepts>;

  constructor(client?: SubagentClient) {
    this.client = client ?? defaultClient;
    this.staticCache = new Map();
    this.initStaticCache();
  }

  /**
   * Initialize static concept mappings for common domains
   */
  private initStaticCache(): void {
    // Common concept mappings for instant fallback
    const mappings: Array<[string, ExpandedConcepts]> = [
      ['健康', {
        keywords: ['健康', '医疗', '医院', '医生', '体检', '保健', '养生', '营养', '运动', '健身'],
        domains: ['健康', '医疗'],
      }],
      ['运动', {
        keywords: ['运动', '健身', '锻炼', '跑步', '游泳', '瑜伽', '打球', '户外', '体育', '训练'],
        domains: ['健康', '运动'],
      }],
      ['编程', {
        keywords: ['编程', '代码', '开发', '程序', '软件', '技术', '算法', '架构', '调试', '测试'],
        domains: ['技术', '开发'],
      }],
      ['工作', {
        keywords: ['工作', '项目', '任务', '会议', '报告', '截止', '目标', '计划', '进度', '团队'],
        domains: ['工作', '项目'],
      }],
      ['学习', {
        keywords: ['学习', '阅读', '课程', '笔记', '知识', '技能', '教程', '培训', '研究', '理解'],
        domains: ['学习', '知识'],
      }],
      ['旅行', {
        keywords: ['旅行', '出行', '旅游', '度假', '酒店', '机票', '景点', '攻略', '行程', '签证'],
        domains: ['旅行', '生活'],
      }],
      ['财务', {
        keywords: ['财务', '工资', '账单', '投资', '理财', '存款', '支出', '收入', '预算', '发票'],
        domains: ['财务', '理财'],
      }],
      ['家人', {
        keywords: ['家人', '家庭', '父母', '孩子', '配偶', '亲戚', '家庭事务', '团聚', '家事'],
        domains: ['家庭', '关系'],
      }],
    ];

    for (const [key, value] of mappings) {
      this.staticCache.set(key, value);
      this.staticCache.set(key.toLowerCase(), value);
    }
  }

  /**
   * Expand concepts for a search query
   * 
   * @param query Search query to expand
   * @param options Expansion options
   * @returns Expanded keywords and domains
   */
  async expand(
    query: string,
    options?: ConceptExpandOptions
  ): Promise<LLMResult<ExpandedConcepts>> {
    // Check static cache first
    const cacheKey = query.toLowerCase().trim();
    const cached = this.staticCache.get(cacheKey);
    
    if (cached) {
      const result = this.limitResults(cached, options);
      return { success: true, data: result, duration: 0 };
    }

    // Build optimized prompt
    const prompt = this.buildPrompt(query, options);

    // Call LLM with timeout
    const result = await this.client.callJSONWithFallback<ExpandedConcepts>(
      {
        task: prompt,
        timeoutSeconds: 15, // Quick task target
        maxRetries: 1,
      },
      () => this.fallbackExpand(query, options)
    );

    if (result.success && result.data) {
      result.data = this.limitResults(result.data, options);
    }

    return result;
  }

  /**
   * Build optimized prompt
   */
  private buildPrompt(query: string, options?: ConceptExpandOptions): string {
    const maxKeywords = options?.maxKeywords ?? 10;
    return `搜索: ${query}
扩展关键词和领域。
返回JSON: {"keywords":["词1","词2","词3"],"domains":["领域1"]}
最多${maxKeywords}个关键词。
仅返回JSON，无解释。`;
  }

  /**
   * Limit results to configured max values
   */
  private limitResults(result: ExpandedConcepts, options?: ConceptExpandOptions): ExpandedConcepts {
    const maxKeywords = options?.maxKeywords ?? 10;
    const maxDomains = options?.maxDomains ?? 3;
    
    return {
      keywords: (result.keywords || []).slice(0, maxKeywords),
      domains: (result.domains || []).slice(0, maxDomains),
    };
  }

  /**
   * Fallback expansion when LLM is unavailable
   */
  private fallbackExpand(query: string, options?: ConceptExpandOptions): ExpandedConcepts {
    const keywords: string[] = [];
    const domains: string[] = [];
    
    // Check static mappings for partial matches
    for (const [key, value] of this.staticCache) {
      if (query.includes(key) || key.includes(query)) {
        keywords.push(...value.keywords);
        domains.push(...value.domains);
      }
    }

    // If no static match, extract keywords from query
    if (keywords.length === 0) {
      const words = query.split(/[\s,，。.！!？?；;：:""\"'\'【】\[\]（）()]+/);
      keywords.push(...words.filter(w => w.length >= 2 && w.length <= 10));
    }

    // Deduplicate
    const uniqueKeywords = [...new Set(keywords)];
    const uniqueDomains = [...new Set(domains)];

    return this.limitResults({
      keywords: uniqueKeywords,
      domains: uniqueDomains,
    }, options);
  }

  /**
   * Add custom concept mapping
   */
  addMapping(key: string, concepts: ExpandedConcepts): void {
    this.staticCache.set(key, concepts);
    this.staticCache.set(key.toLowerCase(), concepts);
  }

  /**
   * Get all cached mappings
   */
  getMappings(): Map<string, ExpandedConcepts> {
    return new Map(this.staticCache);
  }
}

/**
 * Default expander instance
 */
export const defaultExpander = new ConceptExpanderLLM();

/**
 * Quick helper for one-off expansion
 */
export async function expandConcepts(
  query: string,
  options?: ConceptExpandOptions
): Promise<LLMResult<ExpandedConcepts>> {
  return defaultExpander.expand(query, options);
}