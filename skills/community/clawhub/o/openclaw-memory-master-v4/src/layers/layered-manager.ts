/**
 * Memory-Master v4.2.0 - 分层存储管理器
 * 
 * 设计灵感：OpenViking 三层架构 + MemGPT OS 级管理
 * 
 * 功能：
 * - 统一读写接口
 * - 自动分层（默认 L0）
 * - 跨层检索和融合排序
 * - 后台迁移任务（每小时）
 *   - L0 → L1（超过 24 小时）
 *   - L1 → L2（超过 7 天）
 * - 统计和监控
 */

import * as path from 'path';
import { L0HotStore, MemoryEntry as L0Entry } from './l0-hot-store';
import { L1WarmStore, MemoryEntry as L1Entry } from './l1-warm-store';
import { L2ColdStore, MemoryEntry as L2Entry } from './l2-cold-store';

export interface MemoryEntry {
  id: string;
  content: string;
  timestamp: number;
  layer: 'L0' | 'L1' | 'L2';
  metadata?: Record<string, any>;
}

export interface LayeredConfig {
  basePath?: string;
  l0MaxEntries?: number;
  l1MaxEntriesPerDay?: number;
  l1TtlDays?: number;
  l2ArchiveAfterDays?: number;
  autoMigrate?: boolean;
  migrationIntervalMs?: number;
}

export interface SearchOptions {
  limit?: number;
  layers?: Array<'L0' | 'L1' | 'L2'>;
  dateRange?: { start: string; end: string };
}

export interface LayerStats {
  layer: string;
  totalEntries: number;
  size: string;
  hitRate?: number;
}

export class LayeredManager {
  private l0: L0HotStore;
  private l1: L1WarmStore;
  private l2: L2ColdStore;
  private config: Required<LayeredConfig>;
  private migrationTimer?: NodeJS.Timeout;
  private stats = {
    queries: 0,
    hits: { L0: 0, L1: 0, L2: 0 },
    migrations: { L0ToL1: 0, L1ToL2: 0 }
  };

  constructor(config: LayeredConfig = {}) {
    const basePath = config.basePath || path.join(process.cwd(), 'memory');

    this.config = {
      basePath,
      l0MaxEntries: config.l0MaxEntries || 1000,
      l1MaxEntriesPerDay: config.l1MaxEntriesPerDay || 1000,
      l1TtlDays: config.l1TtlDays || 7,
      l2ArchiveAfterDays: config.l2ArchiveAfterDays || 30,
      autoMigrate: config.autoMigrate !== false,
      migrationIntervalMs: config.migrationIntervalMs || 60 * 60 * 1000 // 1 小时
    };

    // 初始化三层存储
    this.l0 = new L0HotStore({
      maxEntries: this.config.l0MaxEntries,
      persistPath: path.join(this.config.basePath, 'l0-cache.json')
    });

    this.l1 = new L1WarmStore({
      basePath: path.join(this.config.basePath, 'l1-warm'),
      maxEntriesPerDay: this.config.l1MaxEntriesPerDay,
      ttlDays: this.config.l1TtlDays
    });

    this.l2 = new L2ColdStore({
      basePath: path.join(this.config.basePath, 'l2-cold'),
      archiveAfterDays: this.config.l2ArchiveAfterDays
    });

    // 启动后台迁移
    if (this.config.autoMigrate) {
      this.startMigrationTimer();
    }

    console.log('[LayeredManager] 初始化完成 - 三层存储已就绪');
  }

  /**
   * 存储记忆（默认到 L0）
   */
  store(content: string, id?: string, metadata?: Record<string, any>): string {
    const memoryId = id || this.generateId();
    const timestamp = Date.now();

    // 默认存储到 L0
    this.l0.set(memoryId, content, metadata);

    console.log(`[LayeredManager] 存储：${memoryId} -> L0`);
    return memoryId;
  }

  /**
   * 存储到指定层
   */
  storeToLayer(content: string, layer: 'L0' | 'L1' | 'L2', id?: string, metadata?: Record<string, any>): string {
    const memoryId = id || this.generateId();

    switch (layer) {
      case 'L0':
        this.l0.set(memoryId, content, metadata);
        break;
      case 'L1':
        this.l1.set(memoryId, content, undefined, metadata);
        break;
      case 'L2':
        const entry: L2Entry = {
          id: memoryId,
          content,
          timestamp: Date.now(),
          date: new Date().toISOString().split('T')[0],
          metadata
        };
        this.l2.archive(entry);
        break;
    }

    console.log(`[LayeredManager] 存储：${memoryId} -> ${layer}`);
    return memoryId;
  }

  /**
   * 获取记忆（自动从三层查找）
   */
  get(id: string): MemoryEntry | null {
    this.stats.queries++;

    // 先查 L0
    const l0Entry = this.l0.get(id);
    if (l0Entry) {
      this.stats.hits.L0++;
      return {
        id: l0Entry.id,
        content: l0Entry.content,
        timestamp: l0Entry.timestamp,
        layer: 'L0',
        metadata: l0Entry.metadata
      };
    }

    // 再查 L1
    const l1Entry = this.l1.get(id);
    if (l1Entry) {
      this.stats.hits.L1++;
      return {
        id: l1Entry.id,
        content: l1Entry.content,
        timestamp: l1Entry.timestamp,
        layer: 'L1',
        metadata: l1Entry.metadata
      };
    }

    // 最后查 L2
    const l2Entry = this.l2.get(id);
    if (l2Entry) {
      this.stats.hits.L2++;
      return {
        id: l2Entry.id,
        content: l2Entry.content,
        timestamp: l2Entry.timestamp,
        layer: 'L2',
        metadata: l2Entry.metadata
      };
    }

    return null;
  }

  /**
   * 搜索记忆（跨层检索）
   */
  search(query: string, options: SearchOptions = {}): MemoryEntry[] {
    const {
      limit = 50,
      layers = ['L0', 'L1', 'L2'],
      dateRange
    } = options;

    const results: MemoryEntry[] = [];

    // L0 搜索
    if (layers.includes('L0')) {
      const l0Results = this.l0.search(query, limit);
      results.push(...l0Results.map(e => ({
        id: e.id,
        content: e.content,
        timestamp: e.timestamp,
        layer: 'L0' as const,
        metadata: e.metadata
      })));
    }

    // L1 搜索
    if (layers.includes('L1') && results.length < limit) {
      const l1Results = this.l1.search(query, dateRange, limit - results.length);
      results.push(...l1Results.map(e => ({
        id: e.id,
        content: e.content,
        timestamp: e.timestamp,
        layer: 'L1' as const,
        metadata: e.metadata
      })));
    }

    // L2 搜索
    if (layers.includes('L2') && results.length < limit) {
      const l2Results = this.l2.search(query, dateRange, limit - results.length);
      results.push(...l2Results.map(e => ({
        id: e.id,
        content: e.content,
        timestamp: e.timestamp,
        layer: 'L2' as const,
        metadata: e.metadata
      })));
    }

    // 按时间戳排序
    results.sort((a, b) => b.timestamp - a.timestamp);

    return results.slice(0, limit);
  }

  /**
   * 按日期范围查询
   */
  queryByDateRange(startDate: string, endDate: string, limit: number = 100): MemoryEntry[] {
    const results: MemoryEntry[] = [];

    // L1 查询（最近 7 天）
    const l1Results = this.l1.queryByDateRange(startDate, endDate, limit);
    results.push(...l1Results.map(e => ({
      id: e.id,
      content: e.content,
      timestamp: e.timestamp,
      layer: 'L1' as const,
      metadata: e.metadata
    })));

    // L2 查询（超过 7 天）
    if (results.length < limit) {
      const l2Results = this.l2.queryByDateRange(startDate, endDate, limit - results.length);
      results.push(...l2Results.map(e => ({
        id: e.id,
        content: e.content,
        timestamp: e.timestamp,
        layer: 'L2' as const,
        metadata: e.metadata
      })));
    }

    // 按时间戳排序
    results.sort((a, b) => b.timestamp - a.timestamp);

    return results.slice(0, limit);
  }

  /**
   * 删除记忆
   */
  delete(id: string): boolean {
    const deleted = this.l0.delete(id) || this.l1.delete(id) || this.l2.delete(id);
    return deleted;
  }

  /**
   * 获取统计信息
   */
  getStats(): {
    layers: LayerStats[];
    totalQueries: number;
    hitRates: { L0: number; L1: number; L2: number };
    migrations: { L0ToL1: number; L1ToL2: number };
  } {
    const l0Stats = this.l0.getStats();
    const l1Stats = this.l1.getStats();
    const l2Stats = this.l2.getStats();

    const totalHits = this.stats.hits.L0 + this.stats.hits.L1 + this.stats.hits.L2;

    return {
      layers: [
        {
          layer: 'L0',
          totalEntries: l0Stats.totalEntries,
          size: this.formatSize(l0Stats.totalEntries * 500) // 估算
        },
        {
          layer: 'L1',
          totalEntries: l1Stats.totalEntries,
          size: this.formatSize(l1Stats.totalEntries * 500)
        },
        {
          layer: 'L2',
          totalEntries: l2Stats.totalEntries,
          size: this.formatSize(l2Stats.totalEntries * 500)
        }
      ],
      totalQueries: this.stats.queries,
      hitRates: {
        L0: totalHits > 0 ? (this.stats.hits.L0 / totalHits * 100).toFixed(1) + '%' : '0%',
        L1: totalHits > 0 ? (this.stats.hits.L1 / totalHits * 100).toFixed(1) + '%' : '0%',
        L2: totalHits > 0 ? (this.stats.hits.L2 / totalHits * 100).toFixed(1) + '%' : '0%'
      },
      migrations: this.stats.migrations
    };
  }

  /**
   * 手动迁移 L0 → L1
   */
  migrateL0ToL1(): number {
    const cutoffTime = Date.now() - 24 * 60 * 60 * 1000; // 24 小时前
    const migrated: L0Entry[] = [];

    for (const id of this.l0.keys()) {
      const entry = this.l0.get(id);
      if (entry && entry.timestamp < cutoffTime) {
        migrated.push(entry);
      }
    }

    // 批量迁移到 L1
    for (const entry of migrated) {
      this.l1.set(entry.id, entry.content, entry.timestamp, entry.metadata);
      this.l0.delete(entry.id);
      this.stats.migrations.L0ToL1++;
    }

    if (migrated.length > 0) {
      console.log(`[LayeredManager] 迁移 L0→L1: ${migrated.length} 条`);
    }

    return migrated.length;
  }

  /**
   * 手动迁移 L1 → L2
   */
  migrateL1ToL2(): number {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - this.config.l1TtlDays);
    const cutoffStr = cutoffDate.toISOString().split('T')[0];

    // 获取所有超过 TTL 的日期
    const l1Stats = this.l1.getStats();
    const oldDates: string[] = [];

    // 简单实现：直接查询所有日期，过滤出旧的
    // 实际应该维护一个日期索引
    const migrated: L1Entry[] = [];

    // 这里简化处理，实际应该遍历 L1 的所有日期
    // 为了演示，我们假设有一个方法可以获取所有旧条目
    // 实际实现需要更复杂的逻辑

    console.log(`[LayeredManager] 迁移 L1→L2: ${migrated.length} 条`);
    return migrated.length;
  }

  /**
   * 销毁
   */
  destroy(): void {
    if (this.migrationTimer) {
      clearInterval(this.migrationTimer);
    }
    this.l0.destroy();
    this.l1.destroy();
    this.l2.destroy();
  }

  /**
   * 生成 ID
   */
  private generateId(): string {
    return `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 格式化大小
   */
  private formatSize(bytes: number): string {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  }

  /**
   * 启动后台迁移定时器
   */
  private startMigrationTimer(): void {
    this.migrationTimer = setInterval(() => {
      this.migrateL0ToL1();
      this.migrateL1ToL2();
    }, this.config.migrationIntervalMs);
  }
}

// 导出默认实例
export default LayeredManager;
