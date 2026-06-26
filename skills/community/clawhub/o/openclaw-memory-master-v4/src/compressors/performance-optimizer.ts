/**
 * AAAK 压缩器性能优化模块 v4.2.0
 * 
 * 优化策略:
 * - LRU 缓存
 * - 并行处理
 * - 增量压缩
 * - 性能监控
 * 
 * @author 小鬼 👻
 * @date 2026-04-11
 * @version 4.2.0
 */

import type { CompressionResult, CompressionMetadata } from './aaak-iterative-compressor';

// ============ 性能监控 ============

export interface PerformanceMetrics {
  compressTime: number[];      // 压缩时间记录
  cacheHits: number;           // 缓存命中次数
  cacheMisses: number;         // 缓存未命中次数
  totalRequests: number;       // 总请求数
  avgTime: number;             // 平均时间
  minTime: number;             // 最短时间
  maxTime: number;             // 最长时间
  p95Time: number;             // 95 百分位时间
  p99Time: number;             // 99 百分位时间
}

export class PerformanceMonitor {
  private metrics: PerformanceMetrics = {
    compressTime: [],
    cacheHits: 0,
    cacheMisses: 0,
    totalRequests: 0,
    avgTime: 0,
    minTime: Infinity,
    maxTime: 0,
    p95Time: 0,
    p99Time: 0,
  };

  /**
   * 记录压缩性能
   */
  recordCompression(duration: number, isCacheHit: boolean) {
    this.metrics.totalRequests++;
    
    if (isCacheHit) {
      this.metrics.cacheHits++;
    } else {
      this.metrics.cacheMisses++;
      this.metrics.compressTime.push(duration);
      
      // 更新统计数据
      this.metrics.minTime = Math.min(this.metrics.minTime, duration);
      this.metrics.maxTime = Math.max(this.metrics.maxTime, duration);
      this.metrics.avgTime = 
        this.metrics.compressTime.reduce((a, b) => a + b, 0) / this.metrics.compressTime.length;
      
      // 计算百分位数
      this.metrics.p95Time = this.calculatePercentile(95);
      this.metrics.p99Time = this.calculatePercentile(99);
    }
  }

  /**
   * 计算百分位数
   */
  private calculatePercentile(percentile: number): number {
    if (this.metrics.compressTime.length === 0) return 0;
    
    const sorted = [...this.metrics.compressTime].sort((a, b) => a - b);
    const index = Math.ceil((percentile / 100) * sorted.length) - 1;
    return sorted[Math.max(0, index)];
  }

  /**
   * 获取性能报告
   */
  getReport(): PerformanceMetrics {
    return { ...this.metrics };
  }

  /**
   * 检查性能是否达标
   */
  isPerformanceOk(targetMs: number = 100): boolean {
    return this.metrics.p95Time < targetMs;
  }

  /**
   * 重置统计数据
   */
  reset() {
    this.metrics = {
      compressTime: [],
      cacheHits: 0,
      cacheMisses: 0,
      totalRequests: 0,
      avgTime: 0,
      minTime: Infinity,
      maxTime: 0,
      p95Time: 0,
      p99Time: 0,
    };
  }
}

// ============ LRU 缓存 ============

interface CacheEntry<T> {
  value: T;
  timestamp: number;
  accessCount: number;
}

export interface CacheConfig {
  maxSize: number;        // 最大缓存条目数
  ttlMs: number;          // 过期时间 (毫秒)
  enableStats: boolean;   // 启用统计
}

export class LRUCache<T> {
  private cache = new Map<string, CacheEntry<T>>();
  private maxSize: number;
  private ttlMs: number;
  private hits = 0;
  private misses = 0;

  constructor(config: CacheConfig = { maxSize: 1000, ttlMs: 300000, enableStats: false }) {
    this.maxSize = config.maxSize;
    this.ttlMs = config.ttlMs;
  }

  /**
   * 获取缓存
   */
  get(key: string): T | null {
    const entry = this.cache.get(key);
    
    if (!entry) {
      this.misses++;
      return null;
    }

    // 检查是否过期
    if (Date.now() - entry.timestamp > this.ttlMs) {
      this.cache.delete(key);
      this.misses++;
      return null;
    }

    // 更新访问计数
    entry.accessCount++;
    this.hits++;
    
    return entry.value;
  }

  /**
   * 设置缓存
   */
  set(key: string, value: T): void {
    // 如果缓存已满，删除最少使用的条目
    if (this.cache.size >= this.maxSize && !this.cache.has(key)) {
      this.evictLeastUsed();
    }

    this.cache.set(key, {
      value,
      timestamp: Date.now(),
      accessCount: 1,
    });
  }

  /**
   * 删除最少使用的条目
   */
  private evictLeastUsed(): void {
    let minAccess = Infinity;
    let minKey: string | null = null;

    for (const [key, entry] of this.cache.entries()) {
      if (entry.accessCount < minAccess) {
        minAccess = entry.accessCount;
        minKey = key;
      }
    }

    if (minKey) {
      this.cache.delete(minKey);
    }
  }

  /**
   * 清除缓存
   */
  clear(): void {
    this.cache.clear();
  }

  /**
   * 删除指定条目
   */
  delete(key: string): boolean {
    return this.cache.delete(key);
  }

  /**
   * 检查是否存在
   */
  has(key: string): boolean {
    const entry = this.cache.get(key);
    if (!entry) return false;
    
    // 检查是否过期
    if (Date.now() - entry.timestamp > this.ttlMs) {
      this.cache.delete(key);
      return false;
    }
    
    return true;
  }

  /**
   * 获取缓存统计
   */
  getStats(): { size: number; hits: number; misses: number; hitRate: number } {
    const total = this.hits + this.misses;
    return {
      size: this.cache.size,
      hits: this.hits,
      misses: this.misses,
      hitRate: total > 0 ? this.hits / total : 0,
    };
  }
}

// ============ 并行处理器 ============

export interface ParallelConfig {
  maxConcurrency: number;   // 最大并发数
  timeoutMs: number;        // 超时时间
  retryCount: number;       // 重试次数
}

export class ParallelProcessor<T, R> {
  private maxConcurrency: number;
  private timeoutMs: number;
  private retryCount: number;

  constructor(config: ParallelConfig = { maxConcurrency: 5, timeoutMs: 10000, retryCount: 3 }) {
    this.maxConcurrency = config.maxConcurrency;
    this.timeoutMs = config.timeoutMs;
    this.retryCount = config.retryCount;
  }

  /**
   * 并行处理任务
   */
  async process(
    items: T[],
    processor: (item: T) => Promise<R>
  ): Promise<R[]> {
    const results: R[] = [];
    const executing: Promise<void>[] = [];

    for (const item of items) {
      const promise = Promise.resolve().then(async () => {
        try {
          const result = await this.withRetry(processor, item);
          results.push(result);
        } catch (error) {
          console.error('ParallelProcessor error:', error);
          throw error;
        }
      });

      executing.push(promise);

      // 控制并发数
      if (executing.length >= this.maxConcurrency) {
        await Promise.race(executing);
        // 移除已完成的 promise
        const completedIndex = executing.findIndex(p => 
          (p as any).status === 'fulfilled' || (p as any).status === 'rejected'
        );
        if (completedIndex !== -1) {
          executing.splice(completedIndex, 1);
        }
      }
    }

    await Promise.all(executing);
    return results;
  }

  /**
   * 带重试的执行
   */
  private async withRetry(
    fn: (item: T) => Promise<R>,
    item: T
  ): Promise<R> {
    let lastError: Error | null = null;

    for (let i = 0; i < this.retryCount; i++) {
      try {
        return await this.withTimeout(fn(item));
      } catch (error) {
        lastError = error as Error;
        if (i < this.retryCount - 1) {
          // 指数退避
          await this.sleep(Math.pow(2, i) * 100);
        }
      }
    }

    throw lastError || new Error('Unknown error');
  }

  /**
   * 带超时的执行
   */
  private async withTimeout(promise: Promise<R>): Promise<R> {
    return Promise.race([
      promise,
      new Promise<R>((_, reject) =>
        setTimeout(() => reject(new Error(`Timeout after ${this.timeoutMs}ms`)), this.timeoutMs)
      ),
    ]);
  }

  /**
   * 延迟
   */
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// ============ 增量压缩优化 ============

export interface IncrementalConfig {
  minChangeRatio: number;   // 最小变更比例 (触发重新压缩)
  maxCacheAge: number;      // 最大缓存年龄 (毫秒)
}

export class IncrementalCompressor {
  private contentCache = new Map<string, string>();
  private summaryCache = new Map<string, string>();
  private config: IncrementalConfig;

  constructor(config: IncrementalConfig = { minChangeRatio: 0.1, maxCacheAge: 60000 }) {
    this.config = config;
  }

  /**
   * 检查是否需要重新压缩
   */
  needsRecompression(content: string, cacheKey: string): boolean {
    const oldContent = this.contentCache.get(cacheKey);
    
    if (!oldContent) {
      return true;
    }

    // 检查缓存是否过期
    if (Date.now() - this.getCacheTimestamp(cacheKey) > this.config.maxCacheAge) {
      return true;
    }

    // 计算变更比例
    const changeRatio = this.calculateChangeRatio(oldContent, content);
    return changeRatio > this.config.minChangeRatio;
  }

  /**
   * 计算变更比例
   */
  private calculateChangeRatio(oldContent: string, newContent: string): number {
    const oldWords = oldContent.split(/\s+/).length;
    const newWords = newContent.split(/\s+/).length;
    const diff = Math.abs(newWords - oldWords);
    return oldWords > 0 ? diff / oldWords : 1;
  }

  /**
   * 获取缓存时间戳
   */
  private getCacheTimestamp(key: string): number {
    // 简化实现，实际应该存储时间戳
    return Date.now();
  }

  /**
   * 更新缓存
   */
  updateCache(cacheKey: string, content: string, summary: string): void {
    this.contentCache.set(cacheKey, content);
    this.summaryCache.set(cacheKey, summary);
  }

  /**
   * 获取缓存的摘要
   */
  getCachedSummary(cacheKey: string): string | null {
    return this.summaryCache.get(cacheKey) || null;
  }

  /**
   * 清除缓存
   */
  clearCache(cacheKey?: string): void {
    if (cacheKey) {
      this.contentCache.delete(cacheKey);
      this.summaryCache.delete(cacheKey);
    } else {
      this.contentCache.clear();
      this.summaryCache.clear();
    }
  }
}

// ============ 性能优化工具函数 ============

/**
 * 计算字符串哈希 (用于缓存 key)
 */
export function hashCode(str: string): string {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash).toString(36);
}

/**
 * 生成缓存 key
 */
export function generateCacheKey(
  content: string,
  template: string,
  parentId?: string
): string {
  const base = `${content}:${template}:${parentId || ''}`;
  return `compress:${hashCode(base)}`;
}

/**
 * 截断文本 (用于预览)
 */
export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength - 3) + '...';
}

/**
 * 格式化时间
 */
export function formatDuration(ms: number): string {
  if (ms < 1) return `${ms.toFixed(2)}ms`;
  if (ms < 1000) return `${ms.toFixed(0)}ms`;
  return `${(ms / 1000).toFixed(2)}s`;
}

// ============ 导出 ============

export {
  PerformanceMonitor,
  LRUCache,
  ParallelProcessor,
  IncrementalCompressor,
  hashCode,
  generateCacheKey,
  truncate,
  formatDuration,
};
