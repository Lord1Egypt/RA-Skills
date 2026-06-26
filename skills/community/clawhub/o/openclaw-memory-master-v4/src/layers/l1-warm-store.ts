/**
 * Memory-Master v4.2.0 - L1 温存储
 * 
 * 设计灵感：OpenViking L1 层 + MemGPT 文件系统
 * 
 * 特性：
 * - 按天组织（memory/l1-warm/days/YYYY-MM-DD/）
 * - LRU 缓存管理（1000 条）
 * - 预加载最近 3 天
 * - 7 天 TTL 自动过期
 * - 支持日期范围查询
 * 
 * 适用场景：最近 7 天记忆、中等频率访问
 */

import * as fs from 'fs';
import * as path from 'path';

export interface MemoryEntry {
  id: string;
  content: string;
  timestamp: number;
  date: string; // YYYY-MM-DD
  lastAccessed: number;
  accessCount: number;
  metadata?: Record<string, any>;
}

export interface L1Config {
  basePath?: string;        // 基础路径（默认 memory/l1-warm）
  maxEntriesPerDay?: number; // 每天最大条目数（默认 1000）
  ttlDays?: number;         // TTL 天数（默认 7 天）
  preloadDays?: number;     // 预加载天数（默认 3 天）
  cacheSize?: number;       // 内存缓存大小（默认 500）
}

export class L1WarmStore {
  private config: Required<L1Config>;
  private daysPath: string;
  private cache: Map<string, MemoryEntry>; // 内存缓存
  private loadedDays: Set<string>; // 已加载的日期

  constructor(config: L1Config = {}) {
    this.config = {
      basePath: config.basePath || path.join(process.cwd(), 'memory', 'l1-warm'),
      maxEntriesPerDay: config.maxEntriesPerDay || 1000,
      ttlDays: config.ttlDays || 7,
      preloadDays: config.preloadDays || 3,
      cacheSize: config.cacheSize || 500
    };

    this.daysPath = path.join(this.config.basePath, 'days');
    this.cache = new Map();
    this.loadedDays = new Set();

    // 确保目录存在
    if (!fs.existsSync(this.daysPath)) {
      fs.mkdirSync(this.daysPath, { recursive: true });
    }

    // 预加载最近几天的数据
    this.preloadRecentDays();

    console.log(`[L1WarmStore] 初始化完成 - 每天最大：${this.config.maxEntriesPerDay}, TTL: ${this.config.ttlDays}天`);
  }

  /**
   * 存储记忆
   */
  set(id: string, content: string, timestamp?: number, metadata?: Record<string, any>): boolean {
    const now = timestamp || Date.now();
    const date = this.getDateStr(now);
    const entry: MemoryEntry = {
      id,
      content,
      timestamp: now,
      date,
      lastAccessed: now,
      accessCount: 0,
      metadata
    };

    // 确保日期目录存在
    const dayDir = path.join(this.daysPath, date);
    if (!fs.existsSync(dayDir)) {
      fs.mkdirSync(dayDir, { recursive: true });
    }

    // 读取当天的所有记忆
    const dayEntries = this.getDayEntries(date);

    // 检查是否需要淘汰
    if (dayEntries.length >= this.config.maxEntriesPerDay && !dayEntries.find(e => e.id === id)) {
      this.evictDayLRU(date);
    }

    // 写入文件
    const filePath = path.join(dayDir, `${id}.json`);
    fs.writeFileSync(filePath, JSON.stringify(entry, null, 2), 'utf-8');

    // 更新缓存
    this.cache.set(id, entry);
    if (this.cache.size > this.config.cacheSize) {
      this.evictCacheLRU();
    }

    return true;
  }

  /**
   * 获取记忆
   */
  get(id: string): MemoryEntry | null {
    // 先查缓存
    const cached = this.cache.get(id);
    if (cached) {
      cached.lastAccessed = Date.now();
      cached.accessCount++;
      return cached;
    }

    // 从文件读取
    const date = cached?.date || this.guessDateFromId(id);
    if (!date) {
      return null;
    }

    const filePath = path.join(this.daysPath, date, `${id}.json`);
    if (!fs.existsSync(filePath)) {
      return null;
    }

    try {
      const entry: MemoryEntry = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
      
      // 检查是否过期
      if (this.isExpired(entry)) {
        this.delete(id);
        return null;
      }

      // 更新访问信息
      entry.lastAccessed = Date.now();
      entry.accessCount++;

      // 更新缓存
      this.cache.set(id, entry);

      // 更新文件
      fs.writeFileSync(filePath, JSON.stringify(entry, null, 2), 'utf-8');

      return entry;
    } catch (error) {
      console.error('[L1WarmStore] 读取失败:', error);
      return null;
    }
  }

  /**
   * 按日期范围查询
   */
  queryByDateRange(startDate: string, endDate: string, limit: number = 100): MemoryEntry[] {
    const results: MemoryEntry[] = [];
    const start = new Date(startDate);
    const end = new Date(endDate);

    // 遍历日期范围内的所有天
    const current = new Date(start);
    while (current <= end) {
      const dateStr = this.getDateStr(current.getTime());
      const dayEntries = this.getDayEntries(dateStr);
      results.push(...dayEntries);

      if (results.length >= limit) {
        break;
      }

      current.setDate(current.getDate() + 1);
    }

    // 按时间戳排序
    results.sort((a, b) => b.timestamp - a.timestamp);

    return results.slice(0, limit);
  }

  /**
   * 按日期查询
   */
  queryByDate(date: string, limit: number = 100): MemoryEntry[] {
    return this.getDayEntries(date).slice(0, limit);
  }

  /**
   * 搜索记忆（按内容）
   */
  search(query: string, dateRange?: { start: string; end: string }, limit: number = 50): MemoryEntry[] {
    const results: MemoryEntry[] = [];
    const queryLower = query.toLowerCase();

    // 确定搜索范围
    const datesToSearch = dateRange
      ? this.getDateRange(dateRange.start, dateRange.end)
      : this.getRecentDates(this.config.ttlDays);

    for (const date of datesToSearch) {
      const dayEntries = this.getDayEntries(date);
      for (const entry of dayEntries) {
        if (entry.content.toLowerCase().includes(queryLower)) {
          results.push(entry);
          if (results.length >= limit) {
            return results;
          }
        }
      }
    }

    return results;
  }

  /**
   * 删除记忆
   */
  delete(id: string): boolean {
    const entry = this.cache.get(id);
    const date = entry?.date || this.guessDateFromId(id);

    if (!date) {
      return false;
    }

    const filePath = path.join(this.daysPath, date, `${id}.json`);
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
      this.cache.delete(id);
      return true;
    }

    return false;
  }

  /**
   * 删除某一天的所有记忆
   */
  deleteDay(date: string): boolean {
    const dayDir = path.join(this.daysPath, date);
    if (fs.existsSync(dayDir)) {
      fs.rmSync(dayDir, { recursive: true });
      
      // 清除缓存中该日期的条目
      for (const [id, entry] of this.cache.entries()) {
        if (entry.date === date) {
          this.cache.delete(id);
        }
      }

      return true;
    }
    return false;
  }

  /**
   * 获取统计信息
   */
  getStats(): {
    totalDays: number;
    totalEntries: number;
    dateRange: { start: string; end: string };
    cacheSize: number;
  } {
    const days = this.getAvailableDays();
    const totalEntries = days.reduce((sum, date) => sum + this.getDayEntries(date).length, 0);

    return {
      totalDays: days.length,
      totalEntries,
      dateRange: {
        start: days[0] || '',
        end: days[days.length - 1] || ''
      },
      cacheSize: this.cache.size
    };
  }

  /**
   * 清理过期数据
   */
  cleanup(): number {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - this.config.ttlDays);
    const cutoffStr = this.getDateStr(cutoffDate.getTime());

    const days = this.getAvailableDays();
    let deleted = 0;

    for (const day of days) {
      if (day < cutoffStr) {
        this.deleteDay(day);
        deleted++;
      }
    }

    console.log(`[L1WarmStore] 清理完成 - 删除 ${deleted} 天的数据`);
    return deleted;
  }

  /**
   * 销毁
   */
  destroy(): void {
    this.cache.clear();
    this.loadedDays.clear();
  }

  /**
   * 预加载最近几天的数据到缓存
   */
  private preloadRecentDays(): void {
    const dates = this.getRecentDates(this.config.preloadDays);
    
    for (const date of dates) {
      const entries = this.getDayEntries(date);
      for (const entry of entries) {
        this.cache.set(entry.id, entry);
        if (this.cache.size >= this.config.cacheSize) {
          break;
        }
      }
      this.loadedDays.add(date);
    }

    console.log(`[L1WarmStore] 预加载 ${dates.length} 天，缓存 ${this.cache.size} 条`);
  }

  /**
   * 获取某一天的所有记忆
   */
  private getDayEntries(date: string): MemoryEntry[] {
    const dayDir = path.join(this.daysPath, date);
    if (!fs.existsSync(dayDir)) {
      return [];
    }

    const entries: MemoryEntry[] = [];
    const files = fs.readdirSync(dayDir);

    for (const file of files) {
      if (file.endsWith('.json')) {
        try {
          const filePath = path.join(dayDir, file);
          const entry: MemoryEntry = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
          entries.push(entry);
        } catch (error) {
          console.error('[L1WarmStore] 读取文件失败:', file, error);
        }
      }
    }

    // 按时间戳排序
    entries.sort((a, b) => b.timestamp - a.timestamp);

    return entries;
  }

  /**
   * 淘汰某一天中 LRU 的条目
   */
  private evictDayLRU(date: string): void {
    const entries = this.getDayEntries(date);
    if (entries.length === 0) return;

    // 找到最少访问的条目
    let lruEntry = entries[0];
    for (const entry of entries) {
      if (entry.accessCount < lruEntry.accessCount || 
          (entry.accessCount === lruEntry.accessCount && entry.lastAccessed < lruEntry.lastAccessed)) {
        lruEntry = entry;
      }
    }

    this.delete(lruEntry.id);
    console.log(`[L1WarmStore] LRU 淘汰 (${date}): ${lruEntry.id}`);
  }

  /**
   * 淘汰缓存中 LRU 的条目
   */
  private evictCacheLRU(): void {
    let lruId: string | null = null;
    let lruEntry: MemoryEntry | null = null;

    for (const [id, entry] of this.cache.entries()) {
      if (!lruEntry || entry.lastAccessed < lruEntry.lastAccessed) {
        lruEntry = entry;
        lruId = id;
      }
    }

    if (lruId) {
      this.cache.delete(lruId);
    }
  }

  /**
   * 检查是否过期
   */
  private isExpired(entry: MemoryEntry): boolean {
    const now = new Date();
    const entryDate = new Date(entry.timestamp);
    const daysDiff = (now.getTime() - entryDate.getTime()) / (1000 * 60 * 60 * 24);
    return daysDiff > this.config.ttlDays;
  }

  /**
   * 获取日期字符串
   */
  private getDateStr(timestamp: number): string {
    return new Date(timestamp).toISOString().split('T')[0];
  }

  /**
   * 获取最近 N 天的日期列表
   */
  private getRecentDates(days: number): string[] {
    const dates: string[] = [];
    const now = new Date();
    
    for (let i = 0; i < days; i++) {
      const date = new Date(now);
      date.setDate(date.getDate() - i);
      dates.push(this.getDateStr(date.getTime()));
    }

    return dates;
  }

  /**
   * 获取日期范围内的所有日期
   */
  private getDateRange(start: string, end: string): string[] {
    const dates: string[] = [];
    const startDate = new Date(start);
    const endDate = new Date(end);
    const current = new Date(startDate);

    while (current <= endDate) {
      dates.push(this.getDateStr(current.getTime()));
      current.setDate(current.getDate() + 1);
    }

    return dates;
  }

  /**
   * 获取所有可用的日期
   */
  private getAvailableDays(): string[] {
    if (!fs.existsSync(this.daysPath)) {
      return [];
    }

    return fs.readdirSync(this.daysPath)
      .filter(name => /^\d{4}-\d{2}-\d{2}$/.test(name))
      .sort();
  }

  /**
   * 从 ID 猜测日期（简单实现）
   */
  private guessDateFromId(id: string): string {
    // 如果 ID 包含时间戳
    const match = id.match(/(\d{10,13})/);
    if (match) {
      const timestamp = parseInt(match[1]);
      return this.getDateStr(timestamp);
    }
    
    // 默认返回今天
    return this.getDateStr(Date.now());
  }
}

// 导出默认实例
export default L1WarmStore;
