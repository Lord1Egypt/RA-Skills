/**
 * 结果合并模块
 * 多引擎结果去重、评分融合、排序
 */

import { SearchResult, EngineType, ENGINE_PRIORITIES } from './types';

/**
 * 合并选项
 */
export interface MergeOptions {
  /** 最大返回结果数 */
  maxResults?: number;
  /** 是否按 URL 去重 */
  dedupByUrl?: boolean;
  /** 是否按分数排序 */
  sortByScore?: boolean;
  /** 是否应用时间衰减 */
  applyTimeDecay?: boolean;
  /** 是否应用引擎权重 */
  applyEngineWeight?: boolean;
  /** 引擎权重覆盖 */
  engineWeights?: Partial<Record<EngineType, number>>;
  /** 时间衰减半衰期（天） */
  timeDecayHalfLife?: number;
}

/**
 * 引擎默认权重
 */
const DEFAULT_ENGINE_WEIGHTS: Record<EngineType, number> = {
  bailian: 1.1,    // 中文优化
  tavily: 1.0,     // 基准
  serper: 1.05,    // Google 结果
  exa: 1.15,       // 学术/技术优化
  firecrawl: 0.9   // 内容获取（非搜索）
};

/**
 * 结果合并器
 */
export class ResultMerger {
  private engineWeights: Record<EngineType, number>;
  
  constructor(options: { engineWeights?: Partial<Record<EngineType, number>> } = {}) {
    this.engineWeights = {
      ...DEFAULT_ENGINE_WEIGHTS,
      ...(options.engineWeights || {})
    };
  }
  
  /**
   * 合并多个引擎的搜索结果
   * @param results 多个引擎的结果数组
   * @param options 合并选项
   * @returns 合并后的结果
   */
  merge(results: SearchResult[][], options: MergeOptions = {}): SearchResult[] {
    // 1. 展平结果
    let merged = this.flattenResults(results);
    
    // 2. 计算 URL 标准化（用于去重）
    merged = merged.map(result => ({
      ...result,
      url: this.normalizeUrl(result.url)
    }));
    
    // 3. 按 URL 去重
    if (options.dedupByUrl !== false) {
      merged = this.deduplicateByUrl(merged);
    }
    
    // 4. 计算最终得分
    merged = merged.map(result => ({
      ...result,
      finalScore: this.calculateFinalScore(result, options)
    }));
    
    // 5. 按分数排序
    if (options.sortByScore !== false) {
      merged.sort((a, b) => (b.finalScore || 0) - (a.finalScore || 0));
    }
    
    // 6. 限制结果数量
    const maxResults = options.maxResults || 10;
    return merged.slice(0, maxResults);
  }
  
  /**
   * 展平多引擎结果
   */
  private flattenResults(results: SearchResult[][]): SearchResult[] {
    return results.flat();
  }
  
  /**
   * URL 标准化
   * 移除协议、www、尾部斜杠等，用于更好的去重
   */
  private normalizeUrl(url: string): string {
    try {
      const parsed = new URL(url);
      
      // 统一小写域名
      let normalized = parsed.hostname.toLowerCase();
      
      // 移除 www 前缀
      if (normalized.startsWith('www.')) {
        normalized = normalized.slice(4);
      }
      
      // 添加路径
      normalized += parsed.pathname;
      
      // 移除尾部斜杠
      if (normalized.endsWith('/') && normalized.length > 1) {
        normalized = normalized.slice(0, -1);
      }
      
      // 添加查询参数（可选，某些情况下需要保留）
      // normalized += parsed.search;
      
      return normalized;
    } catch {
      // URL 解析失败，返回原始 URL
      return url.toLowerCase();
    }
  }
  
  /**
   * 按 URL 去重
   * 保留得分最高的结果
   */
  private deduplicateByUrl(results: SearchResult[]): SearchResult[] {
    const urlMap = new Map<string, SearchResult>();
    
    for (const result of results) {
      const normalizedUrl = result.url;
      
      const existing = urlMap.get(normalizedUrl);
      
      if (!existing) {
        // 首次遇到此 URL
        urlMap.set(normalizedUrl, result);
      } else {
        // 已存在，比较分数保留更高的
        const existingScore = existing.originalScore || 0.5;
        const newScore = result.originalScore || 0.5;
        
        if (newScore > existingScore) {
          urlMap.set(normalizedUrl, result);
        }
      }
    }
    
    return Array.from(urlMap.values());
  }
  
  /**
   * 计算最终得分
   */
  private calculateFinalScore(result: SearchResult, options: MergeOptions): number {
    // 基础分
    let score = result.originalScore || 0.5;
    
    // 应用引擎权重
    if (options.applyEngineWeight !== false) {
      const engine = result.engine as EngineType;
      const weight = this.engineWeights[engine] || 1.0;
      score *= weight;
    }
    
    // 应用时间衰减
    if (options.applyTimeDecay !== false && result.publishedDate) {
      const decayFactor = this.calculateTimeDecay(
        result.publishedDate,
        options.timeDecayHalfLife || 30
      );
      score *= decayFactor;
    }
    
    // 内容完整性加分
    if (result.content && result.content.length > 200) {
      score *= 1.05;
    }
    
    // 标题完整性加分
    if (result.title && result.title.length > 10) {
      score *= 1.02;
    }
    
    // 摘要完整性加分
    if (result.snippet && result.snippet.length > 100) {
      score *= 1.03;
    }
    
    // 限制在 0-1 范围
    return Math.max(0, Math.min(1, score));
  }
  
  /**
   * 计算时间衰减因子
   * @param dateStr 发布日期
   * @param halfLife 半衰期（天）
   * @returns 衰减因子 (0-1)
   */
  private calculateTimeDecay(dateStr: string, halfLife: number): number {
    try {
      const publishedDate = new Date(dateStr);
      const now = new Date();
      
      // 计算天数差
      const daysOld = Math.floor(
        (now.getTime() - publishedDate.getTime()) / (1000 * 60 * 60 * 24)
      );
      
      // 负数表示未来日期，给予满分
      if (daysOld < 0) {
        return 1.0;
      }
      
      // 指数衰减：score = 0.5^(days / halfLife)
      // 0 天：1.0, halfLife 天：0.5, 2*halfLife 天：0.25
      const decay = Math.pow(0.5, daysOld / halfLife);
      
      // 设置最低衰减为 0.5，避免旧内容完全被忽略
      return Math.max(0.5, decay);
    } catch {
      // 日期解析失败，返回 1.0
      return 1.0;
    }
  }
  
  /**
   * 设置引擎权重
   */
  setEngineWeight(engine: EngineType, weight: number): void {
    this.engineWeights[engine] = weight;
  }
  
  /**
   * 获取引擎权重
   */
  getEngineWeight(engine: EngineType): number {
    return this.engineWeights[engine] || 1.0;
  }
  
  /**
   * 获取合并统计信息
   */
  getMergeStats(results: SearchResult[][], merged: SearchResult[]): {
    totalResults: number;
    uniqueResults: number;
    duplicatesRemoved: number;
    enginesUsed: string[];
    avgScore: number;
  } {
    const total = results.reduce((sum, r) => sum + r.length, 0);
    const unique = merged.length;
    
    // 统计引擎
    const engines = new Set<string>();
    for (const resultArray of results) {
      for (const result of resultArray) {
        engines.add(result.engine);
      }
    }
    
    // 计算平均分
    const avgScore = merged.length > 0
      ? merged.reduce((sum, r) => sum + (r.finalScore || 0), 0) / merged.length
      : 0;
    
    return {
      totalResults: total,
      uniqueResults: unique,
      duplicatesRemoved: total - unique,
      enginesUsed: Array.from(engines),
      avgScore: Math.round(avgScore * 1000) / 1000
    };
  }
  
  /**
   * 按引擎分组结果
   */
  groupByEngine(results: SearchResult[]): Record<string, SearchResult[]> {
    const grouped: Record<string, SearchResult[]> = {};
    
    for (const result of results) {
      if (!grouped[result.engine]) {
        grouped[result.engine] = [];
      }
      grouped[result.engine].push(result);
    }
    
    return grouped;
  }
  
  /**
   * 获取每个引擎的最佳结果
   */
  getTopResultsByEngine(results: SearchResult[], topN: number = 3): Record<string, SearchResult[]> {
    const grouped = this.groupByEngine(results);
    const topResults: Record<string, SearchResult[]> = {};
    
    for (const [engine, engineResults] of Object.entries(grouped)) {
      // 按分数排序
      const sorted = [...engineResults].sort(
        (a, b) => (b.finalScore || 0) - (a.finalScore || 0)
      );
      topResults[engine] = sorted.slice(0, topN);
    }
    
    return topResults;
  }
}

// 导出单例
export const resultMerger = new ResultMerger();