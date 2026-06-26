/**
 * Memory-Master v4.2.0 - L0 热存储 (JavaScript ES Module 版本)
 * 
 * 设计灵感：OpenViking L0 层 + mem0 缓存
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export class L0HotStore {
  constructor(config = {}) {
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
  set(id, content, metadata) {
    const now = Date.now();
    const entry = {
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
  get(id) {
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
   * 搜索记忆（按内容）
   */
  search(query, limit = 10) {
    const results = [];
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
  delete(id) {
    const deleted = this.store.delete(id);
    if (deleted && this.config.autoPersist) {
      this.saveToDisk();
    }
    return deleted;
  }

  /**
   * 获取统计信息
   */
  getStats() {
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
  keys() {
    return Array.from(this.store.keys());
  }

  /**
   * 销毁
   */
  destroy() {
    if (this.cleanupTimer) {
      clearInterval(this.cleanupTimer);
    }
    this.saveToDisk();
  }

  /**
   * LRU 淘汰
   */
  evictLRU() {
    let lruEntry = null;
    let lruId = null;

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
  isExpired(entry) {
    return Date.now() - entry.timestamp > this.config.ttlMs;
  }

  /**
   * 后台清理
   */
  cleanup() {
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
  startCleanupTimer() {
    this.cleanupTimer = setInterval(() => {
      this.cleanup();
    }, this.config.cleanupIntervalMs);
  }

  /**
   * 保存到磁盘
   */
  saveToDisk() {
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
  loadFromDisk() {
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

export default L0HotStore;
