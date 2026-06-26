/**
 * L0 Hot Store - 热记忆存储
 * 
 * 存储最近 24 小时的记忆，常驻内存，提供毫秒级访问
 * 
 * @author 小鬼 👻 + Jake
 * @version 4.2.0
 */

import * as fs from 'fs';
import * as path from 'path';

export interface HotMemory {
  id: string;
  content: string;
  timestamp: number;
  type: string;
  tags?: string[];
  metadata?: Record<string, any>;
}

export interface L0StoreConfig {
  maxSize?: number;        // 最大条目数（默认 100）
  ttl?: number;            // 生存时间 ms（默认 24 小时）
  eviction?: 'lru' | 'fifo'; // 淘汰策略
  persistPath?: string;    // 持久化路径
  autoPersist?: boolean;   // 自动持久化
}

/**
 * L0 热存储 - 常驻内存的高速缓存
 */
export class L0HotStore {
  private store: Map<string, HotMemory>;
  private accessOrder: string[];  // LRU 访问顺序
  private config: Required<L0StoreConfig>;
  private persistTimer?: NodeJS.Timeout;

  constructor(config: L0StoreConfig = {}) {
    this.store = new Map();
    this.accessOrder = [];
    this.config = {
      maxSize: config.maxSize ?? 100,
      ttl: config.ttl ?? 24 * 60 * 60 * 1000, // 24 小时
      eviction: config.eviction ?? 'lru',
      persistPath: config.persistPath ?? 'memory/l0-hot',
      autoPersist: config.autoPersist ?? true,
    };

    // 初始化持久化
    this.initPersist();
    
    // 启动清理定时器（每 5 分钟清理过期记忆）
    this.startCleanupTimer();
  }

  /**
   * 初始化持久化
   */
  private async initPersist(): Promise<void> {
    try {
      const indexPath = path.join(this.config.persistPath, 'index.json');
      if (fs.existsSync(indexPath)) {
        const data = fs.readFileSync(indexPath, 'utf-8');
        const parsed = JSON.parse(data);
        
        // 恢复内存
        if (parsed.memories) {
          for (const memory of parsed.memories) {
            this.store.set(memory.id, memory);
          }
        }
        
        // 恢复访问顺序
        if (parsed.accessOrder) {
          this.accessOrder = parsed.accessOrder;
        }
        
        console.log(`[L0HotStore] 恢复了 ${this.store.size} 条热记忆`);
      }
    } catch (error) {
      console.warn('[L0HotStore] 恢复持久化失败:', error);
    }
  }

  /**
   * 启动清理定时器
   */
  private startCleanupTimer(): void {
    setInterval(() => {
      this.cleanup();
    }, 5 * 60 * 1000); // 5 分钟
  }

  /**
   * 写入记忆
   */
  async write(memory: HotMemory): Promise<void> {
    // 检查是否已存在
    if (this.store.has(memory.id)) {
      this.update(memory);
      return;
    }

    // 检查是否需要淘汰
    if (this.store.size >= this.config.maxSize) {
      await this.evict();
    }

    // 写入内存
    this.store.set(memory.id, memory);
    this.accessOrder.push(memory.id);

    // 自动持久化
    if (this.config.autoPersist) {
      await this.persist();
    }

    console.log(`[L0HotStore] 写入记忆 ${memory.id}, 当前大小：${this.store.size}`);
  }

  /**
   * 读取记忆
   */
  async read(id: string): Promise<HotMemory | null> {
    const memory = this.store.get(id);
    
    if (!memory) {
      return null;
    }

    // 检查是否过期
    if (this.isExpired(memory)) {
      await this.delete(id);
      return null;
    }

    // 更新访问顺序（LRU）
    if (this.config.eviction === 'lru') {
      const index = this.accessOrder.indexOf(id);
      if (index > -1) {
        this.accessOrder.splice(index, 1);
        this.accessOrder.push(id);
      }
    }

    return memory;
  }

  /**
   * 更新记忆
   */
  async update(memory: Partial<HotMemory> & { id: string }): Promise<void> {
    const existing = this.store.get(memory.id);
    
    if (!existing) {
      throw new Error(`Memory ${memory.id} not found`);
    }

    const updated = { ...existing, ...memory };
    this.store.set(memory.id, updated);

    // 自动持久化
    if (this.config.autoPersist) {
      await this.persist();
    }
  }

  /**
   * 删除记忆
   */
  async delete(id: string): Promise<boolean> {
    const deleted = this.store.delete(id);
    
    if (deleted) {
      const index = this.accessOrder.indexOf(id);
      if (index > -1) {
        this.accessOrder.splice(index, 1);
      }

      // 自动持久化
      if (this.config.autoPersist) {
        await this.persist();
      }
    }

    return deleted;
  }

  /**
   * 批量写入
   */
  async batchWrite(memories: HotMemory[]): Promise<void> {
    for (const memory of memories) {
      await this.write(memory);
    }
  }

  /**
   * 批量读取
   */
  async batchRead(ids: string[]): Promise<(HotMemory | null)[]> {
    return Promise.all(ids.map(id => this.read(id)));
  }

  /**
   * 获取所有记忆
   */
  getAll(): HotMemory[] {
    return Array.from(this.store.values());
  }

  /**
   * 获取记忆数量
   */
  size(): number {
    return this.store.size;
  }

  /**
   * 清空存储
   */
  async clear(): Promise<void> {
    this.store.clear();
    this.accessOrder = [];
    
    if (this.config.autoPersist) {
      await this.persist();
    }
  }

  /**
   * 清理过期记忆
   */
  async cleanup(): Promise<number> {
    const now = Date.now();
    let cleaned = 0;

    for (const [id, memory] of this.store.entries()) {
      if (now - memory.timestamp > this.config.ttl) {
        await this.delete(id);
        cleaned++;
      }
    }

    if (cleaned > 0) {
      console.log(`[L0HotStore] 清理了 ${cleaned} 条过期记忆`);
    }

    return cleaned;
  }

  /**
   * 淘汰记忆（当达到容量上限时）
   */
  private async evict(): Promise<void> {
    if (this.config.eviction === 'lru') {
      // LRU: 淘汰最久未访问的
      const oldestId = this.accessOrder[0];
      if (oldestId) {
        await this.delete(oldestId);
        console.log(`[L0HotStore] LRU 淘汰：${oldestId}`);
      }
    } else {
      // FIFO: 淘汰最早写入的
      const oldestId = this.accessOrder[0];
      if (oldestId) {
        await this.delete(oldestId);
        console.log(`[L0HotStore] FIFO 淘汰：${oldestId}`);
      }
    }
  }

  /**
   * 检查记忆是否过期
   */
  private isExpired(memory: HotMemory): boolean {
    return Date.now() - memory.timestamp > this.config.ttl;
  }

  /**
   * 持久化到磁盘
   */
  async persist(): Promise<void> {
    try {
      // 确保目录存在
      const dir = this.config.persistPath;
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }

      // 写入索引
      const indexPath = path.join(dir, 'index.json');
      const data = {
        memories: this.getAll(),
        accessOrder: this.accessOrder,
        timestamp: Date.now(),
        size: this.store.size,
      };

      fs.writeFileSync(indexPath, JSON.stringify(data, null, 2), 'utf-8');
    } catch (error) {
      console.error('[L0HotStore] 持久化失败:', error);
    }
  }

  /**
   * 获取统计信息
   */
  getStats(): {
    size: number;
    maxSize: number;
    ttl: number;
    eviction: string;
    memoryUsage: number;
  } {
    // 估算内存使用（字节）
    let memoryUsage = 0;
    for (const memory of this.store.values()) {
      memoryUsage += JSON.stringify(memory).length * 2; // UTF-16
    }

    return {
      size: this.store.size,
      maxSize: this.config.maxSize,
      ttl: this.config.ttl,
      eviction: this.config.eviction,
      memoryUsage,
    };
  }

  /**
   * 搜索记忆（简单关键词匹配）
   */
  search(query: string, limit: number = 10): HotMemory[] {
    const results: Array<{ memory: HotMemory; score: number }> = [];
    const queryLower = query.toLowerCase();

    for (const memory of this.store.values()) {
      let score = 0;

      // 内容匹配
      if (memory.content.toLowerCase().includes(queryLower)) {
        score += 10;
      }

      // 标签匹配
      if (memory.tags?.some(tag => tag.toLowerCase().includes(queryLower))) {
        score += 5;
      }

      // 类型匹配
      if (memory.type.toLowerCase().includes(queryLower)) {
        score += 3;
      }

      if (score > 0) {
        results.push({ memory, score });
      }
    }

    // 按评分排序
    results.sort((a, b) => b.score - a.score);

    // 返回 Top-K
    return results.slice(0, limit).map(r => r.memory);
  }

  /**
   * 销毁（停止定时器）
   */
  destroy(): void {
    if (this.persistTimer) {
      clearInterval(this.persistTimer);
    }
  }
}
