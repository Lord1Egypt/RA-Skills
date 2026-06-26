/**
 * Concept Expansion Engine
 * 
 * Expands query concepts to related terms for better memory retrieval.
 * Uses predefined concept mappings and can discover related concepts via
 * vector similarity propagation.
 */

import type { VectorSearchProvider } from '../types.js';

/**
 * Concept expansion result
 */
export interface ConceptExpansion {
  /** Original query */
  originalQuery: string;
  /** Expanded keywords for search */
  expandedKeywords: string[];
  /** Related concepts discovered */
  relatedConcepts: string[];
  /** Expansion method used */
  method: 'mapping' | 'vector' | 'hybrid';
}

/**
 * Predefined concept mappings for common domains
 */
const CONCEPT_MAPPINGS: Record<string, string[]> = {
  // Health & Fitness
  '健康': ['健康', '医疗', '医院', '医生', '体检', '保健', '养生', '营养'],
  '运动': ['运动', '健身', '锻炼', '跑步', '游泳', '爬山', '瑜伽', '体育', '训练'],
  '医疗': ['医疗', '医院', '医生', '治疗', '诊断', '药物', '手术', '康复'],
  '体检': ['体检', '检查', '化验', '报告', '指标', '健康'],
  '牙医': ['牙医', '牙齿', '口腔', '牙科', '拔牙', '补牙', '洗牙'],
  
  // Programming & Tech
  '编程': ['编程', '代码', '开发', '程序', '编程语言', '算法', '软件'],
  'TypeScript': ['TypeScript', 'TS', 'JavaScript', 'JS', '前端', '类型', '接口'],
  'Python': ['Python', 'py', '脚本', '自动化', '数据处理', '机器学习', 'AI'],
  'Rust': ['Rust', '系统编程', '内存安全', '性能', 'Cargo', 'Rustacean'],
  '代码': ['代码', '编程', '开发', '源码', '实现', '函数', '类', '模块'],
  '开发': ['开发', '编程', '软件', '项目', '代码', '构建', '部署'],
  '框架': ['框架', '库', 'SDK', 'API', '架构', '设计模式'],
  
  // Work & Projects
  '项目': ['项目', '任务', '工作', '进度', '里程碑', '交付'],
  '会议': ['会议', '开会', '讨论', '安排', '议程', '纪要', '参会'],
  '截止': ['截止', 'deadline', '期限', '到期', '紧急', '重要'],
  '重要': ['重要', '紧急', '优先', '关键', '核心'],
  '任务': ['任务', '工作', '待办', 'TODO', '安排', '事项'],
  
  // Life & Activities
  '旅行': ['旅行', '旅游', '出行', '度假', '景点', '酒店', '机票'],
  '购物': ['购物', '买', '订单', '快递', '物流', '支付'],
  '学习': ['学习', '课程', '培训', '书籍', '笔记', '知识'],
  '阅读': ['阅读', '书', '文章', '笔记', '摘录', '读书'],
  
  // People & Relationships
  '家人': ['家人', '父母', '子女', '配偶', '亲戚', '家庭'],
  '朋友': ['朋友', '同事', '伙伴', '社交', '聚会'],
  
  // Time & Planning
  '安排': ['安排', '计划', '日程', '时间', '事项'],
  '计划': ['计划', '规划', '目标', '安排', 'TODO'],
  '日程': ['日程', '安排', '时间', '日历', '事项', '提醒'],
  
  // Location
  '北京': ['北京', 'Beijing', '首都', '京', '北方'],
  '上海': ['上海', 'Shanghai', '沪', '东方'],
  '深圳': ['深圳', 'Shenzhen', '鹏城', '南方', '广东'],
  '广州': ['广州', 'Guangzhou', '穗', '广东', '南方'],
  '杭州': ['杭州', 'Hangzhou', '浙', '浙江', '西湖'],
  
  // Finance
  '工资': ['工资', '收入', '薪资', '薪酬', '发放'],
  '账单': ['账单', '支付', '费用', '开销', '支出', '缴费'],
  '投资': ['投资', '理财', '基金', '股票', '收益', '风险'],
};

/**
 * Domain categories for concept grouping
 */
const DOMAIN_CATEGORIES: Record<string, string[]> = {
  '健康与运动': ['健康', '运动', '医疗', '体检', '牙医', '健身', '跑步', '爬山'],
  '编程与技术': ['编程', 'TypeScript', 'Python', 'Rust', '代码', '开发', '框架', 'AI', '算法'],
  '工作与项目': ['项目', '会议', '截止', '重要', '任务', '进度', '里程碑'],
  '生活日常': ['旅行', '购物', '学习', '阅读', '饮食', '作息'],
  '人际关系': ['家人', '朋友', '同事', '客户', '社交'],
  '时间规划': ['安排', '计划', '日程', '提醒', '截止'],
  '财务管理': ['工资', '账单', '投资', '理财', '支出', '收入'],
};

/**
 * Concept Expander
 * 
 * Expands query concepts using predefined mappings and vector similarity.
 */
export class ConceptExpander {
  private vectorSearch?: VectorSearchProvider;
  private conceptCache: Map<string, string[]>;
  
  constructor(vectorSearch?: VectorSearchProvider) {
    this.vectorSearch = vectorSearch;
    this.conceptCache = new Map();
  }
  
  /**
   * Expand a query to related keywords
   */
  async expandQuery(query: string): Promise<ConceptExpansion> {
    const keywords: string[] = [];
    const relatedConcepts: string[] = [];
    
    // Step 1: Extract keywords from query
    const extractedKeywords = this.extractKeywords(query);
    keywords.push(...extractedKeywords);
    
    // Step 2: Expand using predefined mappings
    const mappedExpansion = this.expandWithMappings(extractedKeywords);
    keywords.push(...mappedExpansion.keywords);
    relatedConcepts.push(...mappedExpansion.relatedConcepts);
    
    // Step 3: If vector search available, discover more related concepts
    if (this.vectorSearch) {
      const vectorExpansion = await this.expandWithVectors(query, keywords);
      keywords.push(...vectorExpansion.keywords);
      relatedConcepts.push(...vectorExpansion.relatedConcepts);
    }
    
    // Remove duplicates while preserving order
    const uniqueKeywords = [...new Set(keywords)];
    const uniqueConcepts = [...new Set(relatedConcepts)];
    
    const method = this.vectorSearch ? 'hybrid' : 'mapping';
    
    return {
      originalQuery: query,
      expandedKeywords: uniqueKeywords,
      relatedConcepts: uniqueConcepts,
      method,
    };
  }
  
  /**
   * Extract keywords from a query
   */
  private extractKeywords(query: string): string[] {
    const keywords: string[] = [];
    
    // Extract Chinese keywords (2+ characters)
    const chineseMatches = query.match(/[\u4e00-\u9fa5]{2,}/g) || [];
    keywords.push(...chineseMatches);
    
    // Extract English words
    const englishMatches = query.match(/[a-zA-Z]{2,}/gi) || [];
    keywords.push(...englishMatches.map(w => w.toLowerCase()));
    
    // Extract technical terms (with numbers/symbols)
    const techMatches = query.match(/[a-zA-Z]+\d+|\d+[a-zA-Z]+|[A-Z]{2,}/g) || [];
    keywords.push(...techMatches);
    
    return keywords;
  }
  
  /**
   * Expand keywords using predefined concept mappings
   */
  private expandWithMappings(keywords: string[]): { 
    keywords: string[]; 
    relatedConcepts: string[];
  } {
    const expandedKeywords: string[] = [];
    const relatedConcepts: string[] = [];
    
    for (const keyword of keywords) {
      // Direct mapping
      if (CONCEPT_MAPPINGS[keyword]) {
        expandedKeywords.push(...CONCEPT_MAPPINGS[keyword]);
        relatedConcepts.push(keyword);
      }
      
      // Partial match (keyword contains or is contained by mapping key)
      for (const [key, values] of Object.entries(CONCEPT_MAPPINGS)) {
        if (key.includes(keyword) || keyword.includes(key)) {
          expandedKeywords.push(...values);
          relatedConcepts.push(key);
        }
      }
    }
    
    // Also find domain categories
    for (const [category, concepts] of Object.entries(DOMAIN_CATEGORIES)) {
      const hasConcept = concepts.some(c => 
        keywords.some(k => c.includes(k) || k.includes(c))
      );
      if (hasConcept) {
        expandedKeywords.push(...concepts);
      }
    }
    
    return { 
      keywords: [...new Set(expandedKeywords)], 
      relatedConcepts: [...new Set(relatedConcepts)] 
    };
  }
  
  /**
   * Expand keywords using vector similarity
   */
  private async expandWithVectors(
    query: string, 
    existingKeywords: string[]
  ): Promise<{ 
    keywords: string[]; 
    relatedConcepts: string[];
  }> {
    if (!this.vectorSearch) {
      return { keywords: [], relatedConcepts: [] };
    }
    
    const keywords: string[] = [];
    const relatedConcepts: string[] = [];
    
    try {
      // Search for semantically similar content
      const results = await this.vectorSearch.search(query, 5);
      
      // Extract keywords from search results
      for (const result of results) {
        if (result.metadata?.tags && Array.isArray(result.metadata.tags)) {
          keywords.push(...result.metadata.tags);
        }
        if (result.score > 0.7) {
          // High similarity - treat as related concept
          relatedConcepts.push(result.id);
        }
      }
    } catch (error) {
      // Vector search failed, return empty
      console.warn('Vector-based expansion failed:', error);
    }
    
    return { keywords, relatedConcepts };
  }
  
  /**
   * Discover related concepts using similarity propagation
   * 
   * @param concept Starting concept
   * @param maxDepth Maximum propagation depth
   * @param minScore Minimum similarity score to follow
   */
  async discoverRelated(
    concept: string, 
    maxDepth: number = 2,
    minScore: number = 0.6
  ): Promise<string[]> {
    if (!this.vectorSearch || maxDepth <= 0) {
      // Fall back to mapping-based discovery
      return this.discoverRelatedFromMappings(concept);
    }
    
    const visited = new Set<string>();
    const discovered: string[] = [];
    const queue: Array<{ term: string; depth: number }> = [{ term: concept, depth: 0 }];
    
    while (queue.length > 0) {
      const { term, depth } = queue.shift()!;
      
      if (visited.has(term) || depth > maxDepth) {
        continue;
      }
      
      visited.add(term);
      
      try {
        const results = await this.vectorSearch!.search(term, 10);
        
        for (const result of results) {
          if (result.score >= minScore && !visited.has(result.id)) {
            discovered.push(result.id);
            
            // Extract keywords from metadata
            if (result.metadata?.tags && Array.isArray(result.metadata.tags)) {
              for (const tag of result.metadata.tags) {
                if (!visited.has(tag) && typeof tag === 'string') {
                  queue.push({ term: tag, depth: depth + 1 });
                }
              }
            }
          }
        }
      } catch (error) {
        console.warn(`Vector search failed for term "${term}":`, error);
      }
    }
    
    return [...new Set(discovered)];
  }
  
  /**
   * Discover related concepts from predefined mappings
   */
  private discoverRelatedFromMappings(concept: string): string[] {
    const related: string[] = [];
    
    // Check if concept is in any domain category
    for (const [category, concepts] of Object.entries(DOMAIN_CATEGORIES)) {
      if (concepts.includes(concept)) {
        related.push(...concepts.filter(c => c !== concept));
      }
    }
    
    // Check direct mappings
    if (CONCEPT_MAPPINGS[concept]) {
      related.push(...CONCEPT_MAPPINGS[concept].filter(c => c !== concept));
    }
    
    // Find concepts that include this concept
    for (const [key, values] of Object.entries(CONCEPT_MAPPINGS)) {
      if (values.includes(concept) && key !== concept) {
        related.push(key);
      }
    }
    
    return [...new Set(related)];
  }
  
  /**
   * Get domain category for a concept
   */
  getDomainCategory(concept: string): string | null {
    for (const [category, concepts] of Object.entries(DOMAIN_CATEGORIES)) {
      if (concepts.includes(concept)) {
        return category;
      }
    }
    return null;
  }
  
  /**
   * Get all concepts in a domain
   */
  getDomainConcepts(domain: string): string[] {
    return DOMAIN_CATEGORIES[domain] || [];
  }
  
  /**
   * Check if two concepts are related
   */
  areRelated(concept1: string, concept2: string): boolean {
    // Check same domain
    const domain1 = this.getDomainCategory(concept1);
    const domain2 = this.getDomainCategory(concept2);
    if (domain1 && domain1 === domain2) {
      return true;
    }
    
    // Check mapping relationship
    const map1 = CONCEPT_MAPPINGS[concept1] || [];
    const map2 = CONCEPT_MAPPINGS[concept2] || [];
    
    return map1.includes(concept2) || map2.includes(concept1);
  }
}

/**
 * Create a ConceptExpander instance
 */
export function createConceptExpander(vectorSearch?: VectorSearchProvider): ConceptExpander {
  return new ConceptExpander(vectorSearch);
}