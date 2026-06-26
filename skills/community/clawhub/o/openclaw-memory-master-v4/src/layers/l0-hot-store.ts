/**
 * Memory-Master v4.2.0 - L0 热存储
 * 
 * 设计灵感：OpenViking L0 层 + mem0 缓存
 * 
 * 特性：
 * - 基于 Map 的内存存储
 * - LRU 淘汰策略
 * - 24 小时 TTL 自动过期
 * - 自动持久化到磁盘
 * - 后台清理（每 5 分钟）
 * 
 * 适用场景：最近对话、短期上下文、高频访问记忆
 */

import * as fs from 'fs';
import * as path from 'path';

export interface MemoryEntry {
  id: string;
  content: string;
  timestamp: number;
  lastAccessed: number;
  accessCount: number;
  metadata?: Record<string, any>;
}

export interface L0Config {
  maxEntries?: number;        // 最大条目数（默认 1000）
  ttlMs?: number;             // TTL 时间（默认 24 小时）
  persistPath?: string;       // 持久化路径
  autoPersist?: boolean;      // 是否自动持久化（默认 true）
  cleanupIntervalMs?: number; // 清理间隔（默认 5 分钟）
}

export class L0HotStore {
  private store: Map<string, MemoryEntry>;
  private config: Required<L0Config>;
  private cleanupTimer?: NodeJS.Timeout;
  private persistPath: string;

  constructor(config: L0Config = {}) {
    this.store = new Map();
    this.config = {
      maxEntries: config.maxEntries || 1000,
      ttlMs: config.ttlMs || 24 * 60 * 60 * 1000, // 24 小时
      persistPath: config.persistPath || path.join(process.cwd(), 'memory', 'l0-cache.json'),
      autoPersist: config.autoPersist !== false,
      cleanupIntervalMs: config.cleanupIntervalMs || 5 * 60 * 1000 // 5 分钟
    };

    this.persistPath = this.config.persistPath;

    // 确保目录存在
    const dir = path.dirname(this.persistPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    // 加载持久化数据
    this.loadFromDisk();

    // 启动后台清理
    this.startCleanupTimer();

    console.log(`[L0HotStore] 初始化完成 - 最大条目：${this.config.maxEntries}, TTL: ${this.config.ttlMs / 1000}s`);
  }

  /**
   * 存储记忆
   */
  set(id: string, content: string, metadata?: Record<string, any>): boolean {
    const now = Date.now();
    const entry: MemoryEntry = {
      id,
      content,
      timestamp: now,
      lastAccessed: now,
      accessCount: 0,
      metadata
    };

    // 检查是否需要淘汰
    if (this.store.size >= this.config.maxEntries && !this.store.has(id)) {
      this.evictLRU();
    }

    this.store.set(id, entry);

    // 自动持久化
    if (this.config.autoPersist) {
      this.saveToDisk();
    }

    return true;
  }

  /**
   * 获取记忆
   */
  get(id: string): MemoryEntry | null {
    const entry = this.store.get(id);
    if (!entry) {
      return null;
    }

    // 检查是否过期
    if (this.isExpired(entry)) {
      this.store.delete(id);
      return null;
    }

    // 更新访问信息
    entry.lastAccessed = Date.now();
    entry.accessCount++;

    return entry;
  }

  /**
   * 批量获取
   */
  getMany(ids: string[]): MemoryEntry[] {
    return ids
      .map(id => this.get(id))
      .filter((entry): entry is MemoryEntry => entry !== null);
  }

  /**
   * 搜索记忆（按内容）
   */
  search(query: string, limit: number = 10): MemoryEntry[] {
    const results: MemoryEntry[] = [];
    const queryLower = query.toLowerCase();

    for (const entry of this.store.values()) {
      if (entry.content.toLowerCase().includes(queryLower)) {
        results.push(entry);
        if (results.length >= limit) {
          break;
        }
      }
    }

    return results;
  }

  /**
   * 删除记忆
   */
  delete(id: string): boolean {
    const deleted = this.store.delete(id);
    if (deleted && this.config.autoPersist) {
      this.saveToDisk();
    }
    return deleted;
  }

  /**
   * 清空所有记忆
   */
  clear(): void {
    this.store.clear();
    if (this.config.autoPersist) {
      this.saveToDisk();
    }
  }

  /**
   * 获取统计信息
   */
  getStats(): {
    totalEntries: number;
    oldestEntry: number;
    newestEntry: number;
    totalAccessCount: number;
  } {
    const entries = Array.from(this.store.values());
    
    return {
      totalEntries: this.store.size,
      oldestEntry: entries.length > 0 ? Math.min(...entries.map(e => e.timestamp)) : 0,
      newestEntry: entries.length > 0 ? Math.max(...entries.map(e => e.timestamp)) : 0,
      totalAccessCount: entries.reduce((sum, e) => sum + e.accessCount, 0)
    };
  }

  /**
   * 获取所有记忆 ID
   */
  keys(): string[] {
    return Array.from(this.store.keys());
  }

  /**
   * 检查是否包含某个记忆
   */
  has(id: string): boolean {
    const entry = this.store.get(id);
    if (!entry) return false;
    if (this.isExpired(entry)) {
      this.store.delete(id);
      return false;
    }
    return true;
  }

  /**
   * 销毁（停止清理定时器）
   */
  destroy(): void {
    if (this.cleanupTimer) {
      clearInterval(this.cleanupTimer);
    }
    this.saveToDisk();
  }

  /**
   * LRU 淘汰（淘汰最少访问的条目）
   */
  private evictLRU(): void {
    let lruEntry: MemoryEntry | null = null;
    let lruId: string | null = null;

    for (const [id, entry] of this.store.entries()) {
      if (!lruEntry || entry.lastAccessed < lruEntry.lastAccessed) {
        lruEntry = entry;
        lruId = id;
      }
    }

    if (lruId) {
      this.store.delete(lruId);
      console.log(`[L0HotStore] LRU 淘汰：${lruId}`);
    }
  }

  /**
   * 检查是否过期
   */
  private isExpired(entry: MemoryEntry): boolean {
    return Date.now() - entry.timestamp > this.config.ttlMs;
  }

  /**
   * 后台清理（删除过期条目）
   */
  private cleanup(): void {
    const now = Date.now();
    let deleted = 0;

    for (const [id, entry] of this.store.entries()) {
      if (now - entry.timestamp > this.config.ttlMs) {
        this.store.delete(id);
        deleted++;
      }
    }

    if (deleted > 0) {
      console.log(`[L0HotStore] 清理完成 - 删除 ${deleted} 个过期条目`);
      if (this.config.autoPersist) {
        this.saveToDisk();
      }
    }
  }

  /**
   * 启动后台清理定时器
   */
  private startCleanupTimer(): void {
    this.cleanupTimer = setInterval(() => {
      this.cleanup();
    }, this.config.cleanupIntervalMs);
  }

  /**
   * 保存到磁盘
   */
  private saveToDisk(): void {
    try {
      const data = Array.from(this.store.values());
      fs.writeFileSync(this.persistPath, JSON.stringify(data, null, 2), 'utf-8');
    } catch (error) {
      console.error('[L0HotStore] 持久化失败:', error);
    }
  }

  /**
   * 从磁盘加载
   */
  private loadFromDisk(): void {
    try {
      if (fs.existsSync(this.persistPath)) {
        const data = JSON.parse(fs.readFileSync(this.persistPath, 'utf-8'));
        const now = Date.now();
        
        // 只加载未过期的条目
        for (const entry of data) {
          if (now - entry.timestamp < this.config.ttlMs) {
            this.store.set(entry.id, entry);
          }
        }

        console.log(`[L0HotStore] 从磁盘加载 ${this.store.size} 个条目`);
      }
    } catch (error) {
      console.error('[L0HotStore] 加载失败:', error);
    }
  }
}

// 导出默认实例
export default L0HotStore;
