/**
 * A/B 测试执行脚本
 * 对比 Jarvis 在有无 Memory Palace 时的记忆能力表现
 */

import { testMemories, TestMemory } from './test-data';
import { testQueries, TestQuery } from './test-queries';

// ========== 测试配置 ==========

export interface TestConfig {
  baseUrl: string;
  apiKey?: string;
  timeout: number; // ms
  retries: number;
  parallel: boolean;
  batchSize: number;
}

export interface TestResult {
  testId: string;
  timestamp: string;
  config: TestConfig;
  storage: StorageMetrics;
  retrieval: RetrievalMetrics;
  performance: PerformanceMetrics;
  errors: ErrorInfo[];
}

export interface StorageMetrics {
  totalAttempts: number;
  successful: number;
  failed: number;
  successRate: number;
  avgStoreTime: number; // ms
  duplicateDetectRate: number;
}

export interface RetrievalMetrics {
  totalQueries: number;
  hits: number;
  misses: number;
  hitRate: number;
  
  // Precision@K
  precisionAt1: number;
  precisionAt3: number;
  precisionAt5: number;
  precisionAt10: number;
  
  // Recall
  recallAt1: number;
  recallAt3: number;
  recallAt5: number;
  recallAt10: number;
  
  // 按难度分组
  easyHitRate: number;
  mediumHitRate: number;
  hardHitRate: number;
  
  // 关键词匹配
  keywordMatchRate: number;
  avgKeywordMatchCount: number;
}

export interface PerformanceMetrics {
  avgQueryTime: number; // ms
  p50QueryTime: number;
  p95QueryTime: number;
  p99QueryTime: number;
  maxQueryTime: number;
  minQueryTime: number;
}

export interface ErrorInfo {
  testId: string;
  operation: 'store' | 'retrieve';
  error: string;
  timestamp: string;
}

// ========== Memory Palace 接口 ==========

export interface MemoryPalaceClient {
  // 存储记忆
  store(memory: Omit<TestMemory, 'id'>): Promise<{ success: boolean; id?: string; error?: string }>;
  
  // 批量存储
  storeBatch(memories: Omit<TestMemory, 'id'>[]): Promise<{ success: number; failed: number; errors: string[] }>;
  
  // 检索记忆
  retrieve(query: string): Promise<{ memories: TestMemory[]; scores?: number[] }>;
  
  // 清除所有记忆（测试后清理）
  clear(): Promise<void>;
  
  // 健康检查
  healthCheck(): Promise<boolean>;
}

// ========== 测试执行器 ==========

export class ABTestRunner {
  private client: MemoryPalaceClient;
  private config: TestConfig;
  private results: TestResult;
  private queryTimes: number[] = [];
  private storeTimes: number[] = [];

  constructor(client: MemoryPalaceClient, config: Partial<TestConfig> = {}) {
    this.client = client;
    this.config = {
      baseUrl: config.baseUrl || 'http://localhost:3000',
      timeout: config.timeout || 30000,
      retries: config.retries || 3,
      parallel: config.parallel ?? false,
      batchSize: config.batchSize || 10,
      ...config
    };
    
    this.results = this.initResults();
  }

  private initResults(): TestResult {
    return {
      testId: `test-${Date.now()}`,
      timestamp: new Date().toISOString(),
      config: this.config,
      storage: {
        totalAttempts: 0,
        successful: 0,
        failed: 0,
        successRate: 0,
        avgStoreTime: 0,
        duplicateDetectRate: 0
      },
      retrieval: {
        totalQueries: 0,
        hits: 0,
        misses: 0,
        hitRate: 0,
        precisionAt1: 0,
        precisionAt3: 0,
        precisionAt5: 0,
        precisionAt10: 0,
        recallAt1: 0,
        recallAt3: 0,
        recallAt5: 0,
        recallAt10: 0,
        easyHitRate: 0,
        mediumHitRate: 0,
        hardHitRate: 0,
        keywordMatchRate: 0,
        avgKeywordMatchCount: 0
      },
      performance: {
        avgQueryTime: 0,
        p50QueryTime: 0,
        p95QueryTime: 0,
        p99QueryTime: 0,
        maxQueryTime: 0,
        minQueryTime: Infinity
      },
      errors: []
    };
  }

  /**
   * 运行完整测试
   */
  async runFullTest(): Promise<TestResult> {
    console.log('🚀 开始 A/B 测试...');
    console.log(`📋 测试配置: ${JSON.stringify(this.config, null, 2)}`);
    
    // 1. 健康检查
    console.log('\n📊 步骤 1/4: 健康检查...');
    const healthy = await this.client.healthCheck();
    if (!healthy) {
      throw new Error('Memory Palace 服务不可用');
    }
    console.log('✅ 服务健康');

    // 2. 存储测试
    console.log('\n📊 步骤 2/4: 存储测试...');
    await this.runStorageTest();
    console.log(`✅ 存储完成: ${this.results.storage.successful}/${this.results.storage.totalAttempts}`);

    // 3. 检索测试
    console.log('\n📊 步骤 3/4: 检索测试...');
    await this.runRetrievalTest();
    console.log(`✅ 检索完成: 命中率 ${this.results.retrieval.hitRate.toFixed(2)}%`);

    // 4. 计算最终指标
    console.log('\n📊 步骤 4/4: 计算指标...');
    this.calculateFinalMetrics();

    console.log('\n🎉 测试完成！');
    return this.results;
  }

  /**
   * 存储测试
   */
  async runStorageTest(): Promise<void> {
    const memories = testMemories.map(m => ({
      content: m.content,
      category: m.category,
      tags: m.tags,
      importance: m.importance,
      createdAt: m.createdAt
    }));

    if (this.config.parallel) {
      // 并行存储
      const batchSize = this.config.batchSize;
      for (let i = 0; i < memories.length; i += batchSize) {
        const batch = memories.slice(i, i + batchSize);
        const result = await this.client.storeBatch(batch);
        this.results.storage.totalAttempts += batch.length;
        this.results.storage.successful += result.success;
        this.results.storage.failed += result.failed;
        result.errors.forEach(e => this.results.errors.push({
          testId: this.results.testId,
          operation: 'store',
          error: e,
          timestamp: new Date().toISOString()
        }));
      }
    } else {
      // 串行存储
      for (const memory of memories) {
        this.results.storage.totalAttempts++;
        const startTime = Date.now();
        
        try {
          const result = await this.retryWithBackoff(() => this.client.store(memory));
          const elapsed = Date.now() - startTime;
          this.storeTimes.push(elapsed);
          
          if (result.success) {
            this.results.storage.successful++;
          } else {
            this.results.storage.failed++;
            this.results.errors.push({
              testId: this.results.testId,
              operation: 'store',
              error: result.error || 'Unknown error',
              timestamp: new Date().toISOString()
            });
          }
        } catch (error) {
          const elapsed = Date.now() - startTime;
          this.storeTimes.push(elapsed);
          this.results.storage.failed++;
          this.results.errors.push({
            testId: this.results.testId,
            operation: 'store',
            error: error instanceof Error ? error.message : String(error),
            timestamp: new Date().toISOString()
          });
        }
      }
    }

    this.results.storage.successRate = 
      (this.results.storage.successful / this.results.storage.totalAttempts) * 100;
    this.results.storage.avgStoreTime = 
      this.storeTimes.reduce((a, b) => a + b, 0) / this.storeTimes.length;
  }

  /**
   * 检索测试
   */
  async runRetrievalTest(): Promise<void> {
    const queryResults: {
      query: TestQuery;
      retrieved: TestMemory[];
      elapsed: number;
      hits: number;
      keywordsFound: string[];
    }[] = [];

    for (const query of testQueries) {
      const startTime = Date.now();
      
      try {
        const result = await this.retryWithBackoff(() => this.client.retrieve(query.query));
        const elapsed = Date.now() - startTime;
        this.queryTimes.push(elapsed);

        // 计算命中
        const retrievedIds = new Set(result.memories.map(m => m.id));
        const expectedIds = new Set(query.expectedMemoryIds);
        const hits = [...retrievedIds].filter(id => expectedIds.has(id)).length;

        // 检查关键词
        const keywordsFound = query.expectedKeywords.filter(kw =>
          result.memories.some(m => m.content.includes(kw) || m.tags.includes(kw))
        );

        queryResults.push({
          query,
          retrieved: result.memories,
          elapsed,
          hits,
          keywordsFound
        });

        // 更新计数
        this.results.retrieval.totalQueries++;
        if (hits > 0) {
          this.results.retrieval.hits++;
        } else {
          this.results.retrieval.misses++;
        }

      } catch (error) {
        const elapsed = Date.now() - startTime;
        this.queryTimes.push(elapsed);
        this.results.retrieval.totalQueries++;
        this.results.retrieval.misses++;
        
        this.results.errors.push({
          testId: this.results.testId,
          operation: 'retrieve',
          error: error instanceof Error ? error.message : String(error),
          timestamp: new Date().toISOString()
        });

        queryResults.push({
          query,
          retrieved: [],
          elapsed,
          hits: 0,
          keywordsFound: []
        });
      }
    }

    // 计算命中率
    this.results.retrieval.hitRate = 
      (this.results.retrieval.hits / this.results.retrieval.totalQueries) * 100;

    // 计算 Precision@K
    this.calculatePrecisionAtK(queryResults);

    // 计算 Recall@K
    this.calculateRecallAtK(queryResults);

    // 按难度分组计算
    this.calculateByDifficulty(queryResults);

    // 关键词匹配率
    const totalKeywords = queryResults.reduce((sum, r) => sum + r.query.expectedKeywords.length, 0);
    const foundKeywords = queryResults.reduce((sum, r) => sum + r.keywordsFound.length, 0);
    this.results.retrieval.keywordMatchRate = (foundKeywords / totalKeywords) * 100;
    this.results.retrieval.avgKeywordMatchCount = foundKeywords / queryResults.length;
  }

  /**
   * 计算 Precision@K
   */
  private calculatePrecisionAtK(results: { retrieved: TestMemory[]; query: TestQuery }[]): void {
    const ks = [1, 3, 5, 10];
    const precisions: Record<number, number[]> = { 1: [], 3: [], 5: [], 10: [] };

    for (const result of results) {
      const expectedIds = new Set(result.query.expectedMemoryIds);
      
      for (const k of ks) {
        const topK = result.retrieved.slice(0, k);
        const relevant = topK.filter(m => expectedIds.has(m.id)).length;
        precisions[k].push(topK.length > 0 ? relevant / topK.length : 0);
      }
    }

    this.results.retrieval.precisionAt1 = this.average(precisions[1]) * 100;
    this.results.retrieval.precisionAt3 = this.average(precisions[3]) * 100;
    this.results.retrieval.precisionAt5 = this.average(precisions[5]) * 100;
    this.results.retrieval.precisionAt10 = this.average(precisions[10]) * 100;
  }

  /**
   * 计算 Recall@K
   */
  private calculateRecallAtK(results: { retrieved: TestMemory[]; query: TestQuery }[]): void {
    const ks = [1, 3, 5, 10];
    const recalls: Record<number, number[]> = { 1: [], 3: [], 5: [], 10: [] };

    for (const result of results) {
      const expectedIds = new Set(result.query.expectedMemoryIds);
      const totalRelevant = expectedIds.size;
      
      for (const k of ks) {
        const topK = result.retrieved.slice(0, k);
        const found = topK.filter(m => expectedIds.has(m.id)).length;
        recalls[k].push(totalRelevant > 0 ? found / totalRelevant : 0);
      }
    }

    this.results.retrieval.recallAt1 = this.average(recalls[1]) * 100;
    this.results.retrieval.recallAt3 = this.average(recalls[3]) * 100;
    this.results.retrieval.recallAt5 = this.average(recalls[5]) * 100;
    this.results.retrieval.recallAt10 = this.average(recalls[10]) * 100;
  }

  /**
   * 按难度计算
   */
  private calculateByDifficulty(results: { query: TestQuery; hits: number }[]): void {
    const byDifficulty = {
      easy: results.filter(r => r.query.difficulty === 'easy'),
      medium: results.filter(r => r.query.difficulty === 'medium'),
      hard: results.filter(r => r.query.difficulty === 'hard')
    };

    for (const [diff, items] of Object.entries(byDifficulty)) {
      const hitRate = items.length > 0 
        ? (items.filter(i => i.hits > 0).length / items.length) * 100 
        : 0;
      
      if (diff === 'easy') this.results.retrieval.easyHitRate = hitRate;
      else if (diff === 'medium') this.results.retrieval.mediumHitRate = hitRate;
      else this.results.retrieval.hardHitRate = hitRate;
    }
  }

  /**
   * 计算最终性能指标
   */
  private calculateFinalMetrics(): void {
    const times = this.queryTimes.sort((a, b) => a - b);
    
    if (times.length === 0) return;

    this.results.performance.avgQueryTime = this.average(times);
    this.results.performance.p50QueryTime = this.percentile(times, 50);
    this.results.performance.p95QueryTime = this.percentile(times, 95);
    this.results.performance.p99QueryTime = this.percentile(times, 99);
    this.results.performance.maxQueryTime = times[times.length - 1];
    this.results.performance.minQueryTime = times[0];
  }

  /**
   * 重试机制
   */
  private async retryWithBackoff<T>(
    fn: () => Promise<T>,
    retries = this.config.retries
  ): Promise<T> {
    let lastError: Error | null = null;
    
    for (let i = 0; i < retries; i++) {
      try {
        return await fn();
      } catch (error) {
        lastError = error instanceof Error ? error : new Error(String(error));
        if (i < retries - 1) {
          await this.sleep(Math.pow(2, i) * 1000);
        }
      }
    }
    
    throw lastError;
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  private average(arr: number[]): number {
    return arr.length > 0 ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
  }

  private percentile(sortedArr: number[], p: number): number {
    if (sortedArr.length === 0) return 0;
    const idx = Math.ceil((p / 100) * sortedArr.length) - 1;
    return sortedArr[Math.max(0, idx)];
  }

  /**
   * 清理测试数据
   */
  async cleanup(): Promise<void> {
    console.log('🧹 清理测试数据...');
    await this.client.clear();
    console.log('✅ 清理完成');
  }
}

// ========== 导出辅助函数 ==========

export function createMockClient(): MemoryPalaceClient {
  // 模拟 Memory Palace 客户端（用于测试测试脚本）
  const stored: TestMemory[] = [];
  
  return {
    async store(memory) {
      await new Promise(r => setTimeout(r, 10)); // 模拟延迟
      const id = `mem-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
      stored.push({ ...memory, id } as TestMemory);
      return { success: true, id };
    },
    
    async storeBatch(memories) {
      const errors: string[] = [];
      let success = 0;
      for (const m of memories) {
        const result = await this.store(m);
        if (result.success) success++;
        else errors.push(result.error || 'Unknown');
      }
      return { success, failed: memories.length - success, errors };
    },
    
    async retrieve(query) {
      await new Promise(r => setTimeout(r, 50)); // 模拟延迟
      const lowerQuery = query.toLowerCase();
      const results = stored.filter(m => 
        m.content.toLowerCase().includes(lowerQuery) ||
        m.tags.some(t => lowerQuery.includes(t.toLowerCase()))
      );
      return { memories: results.slice(0, 10) };
    },
    
    async clear() {
      stored.length = 0;
    },
    
    async healthCheck() {
      return true;
    }
  };
}

// ========== CLI 入口 ==========

if (require.main === module) {
  (async () => {
    const client = createMockClient();
    const runner = new ABTestRunner(client, {
      timeout: 30000,
      retries: 3,
      parallel: false
    });
    
    try {
      const results = await runner.runFullTest();
      console.log('\n📊 测试结果:');
      console.log(JSON.stringify(results, null, 2));
    } finally {
      await runner.cleanup();
    }
  })().catch(console.error);
}