/**
 * Layered Memory Manager - 分层记忆管理器
 * 
 * 统一管理 L0/L1/L2 三层存储，提供透明的读写接口
 * 自动处理层级迁移、缓存管理、跨层检索
 * 
 * @author 小鬼 👻 + Jake
 * @version 4.2.0
 */

import * as path from 'path';
import { L0HotStore, HotMemory } from './l0-hot-store';
import { L1WarmStore, WarmMemory } from './l1-warm-store';
import { L2ColdStore, ColdMemory } from './l2-cold-store';

export interface LayeredMemory {
  id: string;
  content: string;
  timestamp: number;
  type: string;
  tags?: string[];
  metadata?: Record<string, any>;
  layer: 'L0' | 'L1' | 'L2';
  compressed?: boolean;
  compressionRatio?: number;
  archivePath?: string;
}

export interface WriteOptions {
  type?: string;
  tags?: string[];
  metadata?: Record<string, any>;
  skipL0?: boolean;  // 跳过 L0（直接写入 L1/L2）
}

export interface SearchOptions {
  limit?: number;
  layers?: Array<'L0' | 'L1' | 'L2'>;  // 搜索哪些层
  timeRange?: {
    start?: Date;
    end?: Date;
  };
  type?: string;
  tags?: string[];
}

export interface MigrationResult {
  l0ToL1: number;
  l1ToL2: number;
  total: number;
}

export interface LayeredStats {
  l0: {
    size: number;
    maxSize: number;
    memoryUsage: number;
  };
  l1: {
    totalMemories: number;
    totalDays: number;
    cacheUsage: number;
  };
  l2: {
    totalMemories: number;
    totalMonths: number;
    archivedMonths: number;
  };
  total: number;
}

/**
 * 分层记忆管理器
 */
export class LayeredMemoryManager {
  private l0: L0HotStore;
  private l1: L1WarmStore;
  private l2: L2ColdStore;
  private migrationInterval?: NodeJS.Timeout;

  constructor(basePath: string = 'memory') {
    this.l0 = new L0HotStore({
      persistPath: path.join(basePath, 'l0-hot'),
      maxSize: 100,
      ttl: 24 * 60 * 60 * 1000, // 24 小时
    });

    this.l1 = new L1WarmStore({
      basePath: path.join(basePath, 'l1-warm'),
      cacheSize: 1000,
      ttl: 7 * 24 * 60 * 60 * 1000, // 7 天
    });

    this.l2 = new L2ColdStore({
      basePath: path.join(basePath, 'l2-cold'),
      compressAll: true,
      archiveAfterDays: 30,
    });

    // 启动后台迁移任务（每小时）
    this.startMigrationTask();
  }

  /**
   * 写入记忆（自动分层）
   */
  async write(content: string, options: WriteOptions = {}): Promise<string> {
    const id = this.generateId();
    const timestamp = Date.now();

    const memory: LayeredMemory = {
      id,
      content,
      timestamp,
      type: options.type || 'general',
      tags: options.tags || [],
      metadata: options.metadata || {},
      layer: 'L0',
      compressed: false,
    };

    // 默认写入 L0（热存储）
    if (!options.skipL0) {
      const l0Memory: HotMemory = {
        id: memory.id,
        content: memory.content,
        timestamp: memory.timestamp,
        type: memory.type,
        tags: memory.tags,
        metadata: memory.metadata,
      };
      await this.l0.write(l0Memory);
      console.log(`[LayeredManager] 写入 L0: ${id}`);
    } else {
      // 直接写入 L1
      const l1Memory: WarmMemory = {
        id: memory.id,
        content: memory.content,
        timestamp: memory.timestamp,
        type: memory.type,
        tags: memory.tags,
        metadata: memory.metadata,
        compressed: false,
      };
      await this.l1.write(l1Memory);
      console.log(`[LayeredManager] 跳过 L0，直接写入 L1: ${id}`);
    }

    return id;
  }

  /**
   * 批量写入
   */
  async batchWrite(items: Array<{ content: string; options?: WriteOptions }>): Promise<string[]> {
    const ids = await Promise.all(
      items.map(item => this.write(item.content, item.options))
    );
    return ids;
  }

  /**
   * 读取记忆（自动从合适层级加载）
   */
  async read(id: string): Promise<LayeredMemory | null> {
    // 先查 L0
    let memory = await this.l0.read(id);
    if (memory) {
      return { ...memory, layer: 'L0' } as LayeredMemory;
    }

    // 再查 L1
    memory = await this.l1.read(id);
    if (memory) {
      return { ...memory, layer: 'L1' } as LayeredMemory;
    }

    // 最后查 L2
    memory = await this.l2.read(id);
    if (memory) {
      return { ...memory, layer: 'L2' } as LayeredMemory;
    }

    return null;
  }

  /**
   * 批量读取
   */
  async batchRead(ids: string[]): Promise<(LayeredMemory | null)[]> {
    const results = await Promise.all(ids.map(id => this.read(id)));
    return results;
  }

  /**
   * 删除记忆
   */
  async delete(id: string): Promise<boolean> {
    // 尝试从所有层删除
    const deleted = 
      (await this.l0.delete(id)) ||
      (await this.l1.delete(id)) ||
      (await this.l2.delete(id));

    if (deleted) {
      console.log(`[LayeredManager] 删除记忆：${id}`);
    }

    return deleted;
  }

  /**
   * 搜索记忆（跨层检索）
   */
  async search(query: string, options: SearchOptions = {}): Promise<LayeredMemory[]> {
    const {
      limit = 20,
      layers = ['L0', 'L1', 'L2'],
      timeRange,
      type,
      tags,
    } = options;

    const results: Array<{ memory: LayeredMemory; score: number }> = [];

    // L0 搜索
    if (layers.includes('L0')) {
      const l0Results = this.l0.search(query, limit);
      for (const memory of l0Results) {
        if (this.matchesFilter(memory as any, { timeRange, type, tags })) {
          results.push({
            memory: { ...memory, layer: 'L0' } as any,
            score: this.calculateScore(memory as any, query),
          });
        }
      }
    }

    // L1 搜索
    if (layers.includes('L1')) {
      const l1Results = await this.l1.search(query, limit);
      for (const memory of l1Results) {
        if (this.matchesFilter(memory as any, { timeRange, type, tags })) {
          results.push({
            memory: { ...memory, layer: 'L1' } as any,
            score: this.calculateScore(memory as any, query),
          });
        }
      }
    }

    // L2 搜索
    if (layers.includes('L2')) {
      const l2Results = await this.l2.search(query, limit);
      for (const memory of l2Results) {
        if (this.matchesFilter(memory as any, { timeRange, type, tags })) {
          results.push({
            memory: { ...memory, layer: 'L2' } as any,
            score: this.calculateScore(memory as any, query),
          });
        }
      }
    }

    // 按评分排序
    results.sort((a, b) => b.score - a.score);

    // 返回 Top-K
    return results.slice(0, limit).map(r => r.memory);
  }

  /**
   * 按类型筛选
   */
  async getByType(type: string, limit: number = 50): Promise<LayeredMemory[]> {
    const query = ''; // 空查询，只按类型过滤
    const results = await this.search(query, {
      limit,
      type,
    });
    return results;
  }

  /**
   * 按标签筛选
   */
  async getByTags(tags: string[], limit: number = 50): Promise<LayeredMemory[]> {
    const results: LayeredMemory[] = [];

    // 简单实现：搜索后过滤
    const allResults = await this.search('', { limit: limit * 3 });
    
    for (const memory of allResults) {
      if (memory.tags?.some(tag => tags.includes(tag))) {
        results.push(memory);
        if (results.length >= limit) {
          break;
        }
      }
    }

    return results;
  }

  /**
   * 按时间范围筛选
   */
  async getByTimeRange(start: Date, end: Date, limit: number = 100): Promise<LayeredMemory[]> {
    const results = await this.search('', {
      limit,
      timeRange: { start, end },
    });
    return results;
  }

  /**
   * 层级迁移（后台任务）
   */
  async migrate(): Promise<MigrationResult> {
    const result: MigrationResult = {
      l0ToL1: 0,
      l1ToL2: 0,
      total: 0,
    };

    try {
      // L0 → L1 迁移（超过 24 小时的记忆）
      const l0Memories = this.l0.getAll();
      const now = Date.now();
      const l0Threshold = 24 * 60 * 60 * 1000; // 24 小时

      for (const memory of l0Memories) {
        if (now - memory.timestamp > l0Threshold) {
          // 迁移到 L1
          const l1Memory: WarmMemory = {
            id: memory.id,
            content: memory.content,
            timestamp: memory.timestamp,
            type: memory.type,
            tags: memory.tags,
            metadata: memory.metadata,
            compressed: false,
          };
          await this.l1.write(l1Memory);
          await this.l0.delete(memory.id);
          result.l0ToL1++;
          result.total++;
          console.log(`[LayeredManager] 迁移 L0→L1: ${memory.id}`);
        }
      }

      // L1 → L2 迁移（超过 7 天的记忆）
      const l1Summaries = this.l1.getAllDaySummaries();
      const l1Threshold = 7 * 24 * 60 * 60 * 1000; // 7 天

      for (const summary of l1Summaries) {
        const summaryDate = new Date(summary.date).getTime();
        if (now - summaryDate > l1Threshold) {
          // 迁移这天的所有记忆到 L2
          for (const id of summary.memoryIds) {
            const memory = await this.l1.read(id);
            if (memory) {
              const l2Memory: ColdMemory = {
                id: memory.id,
                content: memory.content,
                timestamp: memory.timestamp,
                type: memory.type,
                tags: memory.tags,
                metadata: memory.metadata,
                compressed: memory.compressed || false,
              };
              await this.l2.write(l2Memory);
              await this.l1.delete(id);
              result.l1ToL2++;
              result.total++;
              console.log(`[LayeredManager] 迁移 L1→L2: ${memory.id}`);
            }
          }
        }
      }

      if (result.total > 0) {
        console.log(`[LayeredManager] 迁移完成：${result.total} 条记忆`);
      }
    } catch (error) {
      console.error('[LayeredManager] 迁移失败:', error);
    }

    return result;
  }

  /**
   * 启动后台迁移任务
   */
  private startMigrationTask(): void {
    // 每小时运行一次
    this.migrationInterval = setInterval(async () => {
      await this.migrate();
      
      // L2 自动归档
      await this.l2.autoArchive();
      
      // L1 清理
      await this.l1.cleanup();
    }, 60 * 60 * 1000); // 1 小时

    console.log('[LayeredManager] 后台迁移任务已启动（每小时）');
  }

  /**
   * 获取统计信息
   */
  getStats(): LayeredStats {
    const l0Stats = this.l0.getStats();
    const l1Stats = this.l1.getStats();
    const l2Stats = this.l2.getStats();

    return {
      l0: {
        size: l0Stats.size,
        maxSize: l0Stats.maxSize,
        memoryUsage: l0Stats.memoryUsage,
      },
      l1: {
        totalMemories: l1Stats.totalMemories,
        totalDays: l1Stats.totalDays,
        cacheUsage: l1Stats.cacheUsage,
      },
      l2: {
        totalMemories: l2Stats.totalMemories,
        totalMonths: l2Stats.totalMonths,
        archivedMonths: l2Stats.archivedMonths,
      },
      total: l0Stats.size + l1Stats.totalMemories + l2Stats.totalMemories,
    };
  }

  /**
   * 清空所有层
   */
  async clear(): Promise<void> {
    await this.l0.clear();
    // L1 和 L2 不清空，保留历史数据
    console.log('[LayeredManager] 已清空 L0 热存储');
  }

  /**
   * 销毁（停止后台任务）
   */
  destroy(): void {
    if (this.migrationInterval) {
      clearInterval(this.migrationInterval);
    }
    this.l0.destroy();
  }

  /**
   * 生成唯一 ID
   */
  private generateId(): string {
    return `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 计算搜索评分
   */
  private calculateScore(memory: any, query: string): number {
    let score = 0;
    const queryLower = query.toLowerCase();
    const contentLower = memory.content.toLowerCase();

    // 内容匹配
    if (contentLower.includes(queryLower)) {
      score += 10;
    }

    // 标签匹配
    if (memory.tags?.some((tag: string) => tag.toLowerCase().includes(queryLower))) {
      score += 5;
    }

    // 类型匹配
    if (memory.type.toLowerCase().includes(queryLower)) {
      score += 3;
    }

    // 层级加分（L0 > L1 > L2）
    if (memory.layer === 'L0') {
      score += 2;
    } else if (memory.layer === 'L1') {
      score += 1;
    }

    // 近因加分
    const age = Date.now() - memory.timestamp;
    if (age < 24 * 60 * 60 * 1000) {
      score += 3; // 24 小时内
    } else if (age < 3 * 24 * 60 * 60 * 1000) {
      score += 2; // 3 天内
    } else if (age < 7 * 24 * 60 * 60 * 1000) {
      score += 1; // 7 天内
    }

    return score;
  }

  /**
   * 检查是否匹配过滤条件
   */
  private matchesFilter(
    memory: any,
    filters: {
      timeRange?: { start?: Date; end?: Date };
      type?: string;
      tags?: string[];
    }
  ): boolean {
    // 时间范围过滤
    if (filters.timeRange) {
      const { start, end } = filters.timeRange;
      if (start && memory.timestamp < start.getTime()) {
        return false;
      }
      if (end && memory.timestamp > end.getTime()) {
        return false;
      }
    }

    // 类型过滤
    if (filters.type && memory.type !== filters.type) {
      return false;
    }

    // 标签过滤
    if (filters.tags && filters.tags.length > 0) {
      if (!memory.tags?.some((tag: string) => filters.tags!.includes(tag))) {
        return false;
      }
    }

    return true;
  }
}
