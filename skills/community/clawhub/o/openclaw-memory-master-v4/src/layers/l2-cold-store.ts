/**
 * Memory-Master v4.2.0 - L2 冷存储
 * 
 * 设计灵感：OpenViking L2 层 + 归档系统
 * 
 * 特性：
 * - 按月组织（memory/l2-cold/months/YYYY-MM/）
 * - 懒加载策略
 * - 自动归档（30 天后从 L1 移入 L2）
 * - 查询缓存
 * - 容量无限制
 * 
 * 适用场景：长期记忆、归档、低频访问
 */

import * as fs from 'fs';
import * as path from 'path';

export interface MemoryEntry {
  id: string;
  content: string;
  timestamp: number;
  date: string; // YYYY-MM-DD
  month: string; // YYYY-MM
  metadata?: Record<string, any>;
  archivedAt?: number;
}

export interface L2Config {
  basePath?: string;        // 基础路径（默认 memory/l2-cold）
  archiveAfterDays?: number; // 多少天后归档（默认 30 天）
  queryCacheSize?: number;  // 查询缓存大小（默认 100）
}

export class L2ColdStore {
  private config: Required<L2Config>;
  private monthsPath: string;
  private queryCache: Map<string, MemoryEntry[]>; // 查询结果缓存

  constructor(config: L2Config = {}) {
    this.config = {
      basePath: config.basePath || path.join(process.cwd(), 'memory', 'l2-cold'),
      archiveAfterDays: config.archiveAfterDays || 30,
      queryCacheSize: config.queryCacheSize || 100
    };

    this.monthsPath = path.join(this.config.basePath, 'months');
    this.queryCache = new Map();

    // 确保目录存在
    if (!fs.existsSync(this.monthsPath)) {
      fs.mkdirSync(this.monthsPath, { recursive: true });
    }

    console.log(`[L2ColdStore] 初始化完成 - 归档时间：${this.config.archiveAfterDays}天`);
  }

  /**
   * 归档记忆（从 L1 移入 L2）
   */
  archive(entry: MemoryEntry): boolean {
    const month = entry.date.substring(0, 7); // YYYY-MM
    const monthDir = path.join(this.monthsPath, month);

    // 确保月份目录存在
    if (!fs.existsSync(monthDir)) {
      fs.mkdirSync(monthDir, { recursive: true });
    }

    // 写入文件
    const filePath = path.join(monthDir, `${entry.id}.json`);
    const archivedEntry: MemoryEntry = {
      ...entry,
      month,
      archivedAt: Date.now()
    };

    fs.writeFileSync(filePath, JSON.stringify(archivedEntry, null, 2), 'utf-8');

    // 清除查询缓存
    this.queryCache.clear();

    console.log(`[L2ColdStore] 归档：${entry.id} -> ${month}`);
    return true;
  }

  /**
   * 批量归档
   */
  archiveBatch(entries: MemoryEntry[]): number {
    let archived = 0;
    for (const entry of entries) {
      if (this.archive(entry)) {
        archived++;
      }
    }
    return archived;
  }

  /**
   * 获取记忆
   */
  get(id: string): MemoryEntry | null {
    // 遍历所有月份查找（懒加载）
    const months = this.getAvailableMonths();
    
    for (const month of months) {
      const filePath = path.join(this.monthsPath, month, `${id}.json`);
      if (fs.existsSync(filePath)) {
        try {
          return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
        } catch (error) {
          console.error('[L2ColdStore] 读取失败:', error);
          return null;
        }
      }
    }

    return null;
  }

  /**
   * 按月份查询
   */
  queryByMonth(month: string, limit: number = 100): MemoryEntry[] {
    const cacheKey = `month:${month}:${limit}`;
    const cached = this.queryCache.get(cacheKey);
    if (cached) {
      return cached;
    }

    const monthDir = path.join(this.monthsPath, month);
    if (!fs.existsSync(monthDir)) {
      return [];
    }

    const entries: MemoryEntry[] = [];
    const files = fs.readdirSync(monthDir);

    for (const file of files) {
      if (file.endsWith('.json')) {
        try {
          const filePath = path.join(monthDir, file);
          const entry: MemoryEntry = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
          entries.push(entry);
        } catch (error) {
          console.error('[L2ColdStore] 读取文件失败:', file, error);
        }
      }
    }

    // 按时间戳排序
    entries.sort((a, b) => b.timestamp - a.timestamp);

    const result = entries.slice(0, limit);
    
    // 缓存结果
    if (this.queryCache.size >= this.config.queryCacheSize) {
      const firstKey = this.queryCache.keys().next().value;
      this.queryCache.delete(firstKey);
    }
    this.queryCache.set(cacheKey, result);

    return result;
  }

  /**
   * 按日期范围查询
   */
  queryByDateRange(startDate: string, endDate: string, limit: number = 200): MemoryEntry[] {
    const results: MemoryEntry[] = [];
    const startMonth = startDate.substring(0, 7);
    const endMonth = endDate.substring(0, 7);

    // 获取范围内的所有月份
    const months = this.getAvailableMonths()
      .filter(m => m >= startMonth && m <= endMonth);

    for (const month of months) {
      const monthEntries = this.queryByMonth(month, limit);
      results.push(...monthEntries);

      if (results.length >= limit) {
        break;
      }
    }

    // 按时间戳排序
    results.sort((a, b) => b.timestamp - a.timestamp);

    return results.slice(0, limit);
  }

  /**
   * 搜索记忆（按内容）
   */
  search(query: string, dateRange?: { start: string; end: string }, limit: number = 50): MemoryEntry[] {
    const results: MemoryEntry[] = [];
    const queryLower = query.toLowerCase();

    // 确定搜索范围
    const monthsToSearch = dateRange
      ? this.getAvailableMonths().filter(m => {
          const monthStart = `${m}-01`;
          return monthStart >= dateRange.start && monthStart <= dateRange.end;
        })
      : this.getAvailableMonths();

    for (const month of monthsToSearch) {
      const monthEntries = this.queryByMonth(month, 500); // 每个月最多查 500 条
      for (const entry of monthEntries) {
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
    const entry = this.get(id);
    if (!entry) {
      return false;
    }

    const filePath = path.join(this.monthsPath, entry.month, `${id}.json`);
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
      this.queryCache.clear();
      return true;
    }

    return false;
  }

  /**
   * 删除整个月份的数据
   */
  deleteMonth(month: string): boolean {
    const monthDir = path.join(this.monthsPath, month);
    if (fs.existsSync(monthDir)) {
      fs.rmSync(monthDir, { recursive: true });
      this.queryCache.clear();
      return true;
    }
    return false;
  }

  /**
   * 获取统计信息
   */
  getStats(): {
    totalMonths: number;
    totalEntries: number;
    monthRange: { start: string; end: string };
    queryCacheSize: number;
  } {
    const months = this.getAvailableMonths();
    let totalEntries = 0;

    for (const month of months) {
      const monthDir = path.join(this.monthsPath, month);
      if (fs.existsSync(monthDir)) {
        const files = fs.readdirSync(monthDir);
        totalEntries += files.filter(f => f.endsWith('.json')).length;
      }
    }

    return {
      totalMonths: months.length,
      totalEntries,
      monthRange: {
        start: months[0] || '',
        end: months[months.length - 1] || ''
      },
      queryCacheSize: this.queryCache.size
    };
  }

  /**
   * 销毁
   */
  destroy(): void {
    this.queryCache.clear();
  }

  /**
   * 获取所有可用的月份
   */
  private getAvailableMonths(): string[] {
    if (!fs.existsSync(this.monthsPath)) {
      return [];
    }

    return fs.readdirSync(this.monthsPath)
      .filter(name => /^\d{4}-\d{2}$/.test(name))
      .sort();
  }
}

// 导出默认实例
export default L2ColdStore;
