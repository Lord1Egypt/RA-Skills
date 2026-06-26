/**
 * L2 Cold Store - 冷记忆存储
 * 
 * 存储历史记忆，磁盘存储，懒加载，容量无限制
 * 
 * @author 小鬼 👻 + Jake
 * @version 4.2.0
 */

import * as fs from 'fs';
import * as path from 'path';

export interface ColdMemory {
  id: string;
  content: string;
  timestamp: number;
  type: string;
  tags?: string[];
  metadata?: Record<string, any>;
  compressed: boolean;
  compressionRatio?: number;
  archivePath?: string;  // 归档路径
}

export interface L2StoreConfig {
  basePath?: string;     // 基础路径
  compressAll?: boolean; // 是否全部压缩
  archiveAfterDays?: number; // 多少天后归档
}

interface MonthArchive {
  month: string;         // YYYY-MM
  memoryIds: string[];
  totalSize: number;
  compressedSize?: number;
  archived: boolean;
  archivePath?: string;
}

/**
 * L2 冷存储 - 按月归档的长期存储
 */
export class L2ColdStore {
  private config: Required<L2StoreConfig>;
  private index: Map<string, { month: string; path: string }>;
  private monthArchives: Map<string, MonthArchive>;
  private queryCache: Map<string, ColdMemory[]>;

  constructor(config: L2StoreConfig = {}) {
    this.config = {
      basePath: config.basePath ?? 'memory/l2-cold',
      compressAll: config.compressAll ?? true,
      archiveAfterDays: config.archiveAfterDays ?? 30,
    };

    this.index = new Map();
    this.monthArchives = new Map();
    this.queryCache = new Map();

    // 初始化
    this.init();
  }

  /**
   * 初始化存储
   */
  private async init(): Promise<void> {
    try {
      // 确保基础目录存在
      if (!fs.existsSync(this.config.basePath)) {
        fs.mkdirSync(this.config.basePath, { recursive: true });
      }

      // 加载索引
      const indexPath = path.join(this.config.basePath, 'index.json');
      if (fs.existsSync(indexPath)) {
        const data = fs.readFileSync(indexPath, 'utf-8');
        const parsed = JSON.parse(data);

        if (parsed.index) {
          this.index = new Map(Object.entries(parsed.index));
        }

        if (parsed.monthArchives) {
          this.monthArchives = new Map(
            parsed.monthArchives.map((a: MonthArchive) => [a.month, a])
          );
        }

        console.log(`[L2ColdStore] 恢复了 ${this.index.size} 条冷记忆，${this.monthArchives.size} 个月`);
      }

      // 加载已归档的索引
      await this.loadArchives();
    } catch (error) {
      console.warn('[L2ColdStore] 初始化失败:', error);
    }
  }

  /**
   * 加载归档索引
   */
  private async loadArchives(): Promise<void> {
    const archiveDir = path.join(this.config.basePath, 'archives');
    
    if (!fs.existsSync(archiveDir)) {
      return;
    }

    const files = fs.readdirSync(archiveDir);
    for (const file of files) {
      if (file.endsWith('.json')) {
        try {
          const filePath = path.join(archiveDir, file);
          const data = fs.readFileSync(filePath, 'utf-8');
          const archive = JSON.parse(data);

          // 更新索引
          for (const id of archive.memoryIds) {
            this.index.set(id, {
              month: archive.month,
              path: filePath,
            });
          }
        } catch (error) {
          console.warn(`[L2ColdStore] 加载归档 ${file} 失败:`, error);
        }
      }
    }
  }

  /**
   * 写入记忆
   */
  async write(memory: ColdMemory): Promise<void> {
    const monthStr = this.toMonthString(new Date(memory.timestamp));
    const monthPath = path.join(this.config.basePath, 'months', monthStr);

    // 确保目录存在
    if (!fs.existsSync(monthPath)) {
      fs.mkdirSync(monthPath, { recursive: true });
    }

    // 压缩（如果需要）
    if (this.config.compressAll && !memory.compressed) {
      // TODO: 集成 AAAK 压缩
      // memory = await this.compress(memory);
      memory.compressed = true;
    }

    // 写入文件
    const filePath = path.join(monthPath, `${memory.id}.json`);
    fs.writeFileSync(filePath, JSON.stringify(memory, null, 2), 'utf-8');

    // 更新索引
    this.index.set(memory.id, {
      month: monthStr,
      path: filePath,
    });

    // 更新月归档
    let archive = this.monthArchives.get(monthStr);
    if (!archive) {
      archive = {
        month: monthStr,
        memoryIds: [],
        totalSize: 0,
        archived: false,
      };
      this.monthArchives.set(monthStr, archive);
    }

    if (!archive.memoryIds.includes(memory.id)) {
      archive.memoryIds.push(memory.id);
      const contentSize = Buffer.byteLength(memory.content, 'utf-8');
      archive.totalSize += contentSize;
    }

    // 持久化索引
    await this.persistIndex();

    console.log(`[L2ColdStore] 写入记忆 ${memory.id} (${monthStr})`);
  }

  /**
   * 批量写入
   */
  async batchWrite(memories: ColdMemory[]): Promise<void> {
    for (const memory of memories) {
      await this.write(memory);
    }
  }

  /**
   * 读取记忆
   */
  async read(id: string): Promise<ColdMemory | null> {
    const location = this.index.get(id);
    if (!location) {
      return null;
    }

    try {
      // 检查是否是归档文件
      if (location.path.endsWith('.json') && fs.existsSync(location.path)) {
        const data = fs.readFileSync(location.path, 'utf-8');
        
        // 如果是归档文件，需要找到对应的记忆
        if (location.path.includes('archives')) {
          const archive = JSON.parse(data);
          const memory = archive.memories?.find((m: ColdMemory) => m.id === id);
          return memory || null;
        } else {
          return JSON.parse(data);
        }
      }

      return null;
    } catch (error) {
      console.error(`[L2ColdStore] 读取记忆 ${id} 失败:`, error);
      return null;
    }
  }

  /**
   * 批量读取
   */
  async batchRead(ids: string[]): Promise<(ColdMemory | null)[]> {
    return Promise.all(ids.map(id => this.read(id)));
  }

  /**
   * 按月范围读取
   */
  async readByMonthRange(startMonth: string, endMonth: string): Promise<ColdMemory[]> {
    const memories: ColdMemory[] = [];

    for (const [monthStr, archive] of this.monthArchives.entries()) {
      if (monthStr >= startMonth && monthStr <= endMonth) {
        const monthMemories = await this.batchRead(archive.memoryIds);
        memories.push(...monthMemories.filter((m): m is ColdMemory => m !== null));
      }
    }

    return memories;
  }

  /**
   * 删除记忆
   */
  async delete(id: string): Promise<boolean> {
    const location = this.index.get(id);
    if (!location) {
      return false;
    }

    // 删除文件
    if (fs.existsSync(location.path)) {
      fs.unlinkSync(location.path);
    }

    // 更新索引
    this.index.delete(id);

    // 更新月归档
    const archive = this.monthArchives.get(location.month);
    if (archive) {
      archive.memoryIds = archive.memoryIds.filter(mid => mid !== id);
    }

    // 持久化索引
    await this.persistIndex();

    return true;
  }

  /**
   * 获取记忆数量
   */
  size(): number {
    return this.index.size;
  }

  /**
   * 获取月归档
   */
  getMonthArchive(monthStr: string): MonthArchive | null {
    return this.monthArchives.get(monthStr) || null;
  }

  /**
   * 获取所有月归档
   */
  getAllMonthArchives(): MonthArchive[] {
    return Array.from(this.monthArchives.values());
  }

  /**
   * 搜索记忆（懒加载）
   */
  async search(query: string, limit: number = 50): Promise<ColdMemory[]> {
    const queryLower = query.toLowerCase();
    const results: Array<{ memory: ColdMemory; score: number }> = [];

    // 检查查询缓存
    const cacheKey = queryLower;
    if (this.queryCache.has(cacheKey)) {
      return this.queryCache.get(cacheKey) || [];
    }

    // 遍历所有月份（可能需要优化）
    for (const [monthStr, archive] of this.monthArchives.entries()) {
      // 懒加载：只加载部分月份
      const monthMemories = await this.batchRead(archive.memoryIds.slice(0, 100));
      
      for (const memory of monthMemories.filter((m): m is ColdMemory => m !== null)) {
        const score = this.calculateScore(memory, queryLower);
        if (score > 0) {
          results.push({ memory, score });
        }
      }

      // 如果结果已够，提前退出
      if (results.length >= limit * 2) {
        break;
      }
    }

    // 按评分排序
    results.sort((a, b) => b.score - a.score);

    const topResults = results.slice(0, limit).map(r => r.memory);

    // 缓存结果
    this.queryCache.set(cacheKey, topResults);

    return topResults;
  }

  /**
   * 计算搜索评分
   */
  private calculateScore(memory: ColdMemory, query: string): number {
    let score = 0;
    const contentLower = memory.content.toLowerCase();

    // 内容匹配
    if (contentLower.includes(query)) {
      score += 10;
    }

    // 标签匹配
    if (memory.tags?.some(tag => tag.toLowerCase().includes(query))) {
      score += 5;
    }

    // 类型匹配
    if (memory.type.toLowerCase().includes(query)) {
      score += 3;
    }

    return score;
  }

  /**
   * 归档月份数据
   */
  async archiveMonth(monthStr: string): Promise<void> {
    const archive = this.monthArchives.get(monthStr);
    if (!archive || archive.archived) {
      return;
    }

    try {
      // 读取所有记忆
      const memories = await this.batchRead(archive.memoryIds);
      const validMemories = memories.filter((m): m is ColdMemory => m !== null);

      if (validMemories.length === 0) {
        return;
      }

      // 创建归档文件
      const archiveDir = path.join(this.config.basePath, 'archives');
      if (!fs.existsSync(archiveDir)) {
        fs.mkdirSync(archiveDir, { recursive: true });
      }

      const archivePath = path.join(archiveDir, `${monthStr}.json`);
      const archiveData = {
        month: monthStr,
        memories: validMemories,
        memoryIds: archive.memoryIds,
        totalSize: archive.totalSize,
        archivedAt: Date.now(),
      };

      fs.writeFileSync(archivePath, JSON.stringify(archiveData, null, 2), 'utf-8');

      // 更新归档状态
      archive.archived = true;
      archive.archivePath = archivePath;

      // 删除原始文件
      const monthPath = path.join(this.config.basePath, 'months', monthStr);
      if (fs.existsSync(monthPath)) {
        for (const id of archive.memoryIds) {
          const filePath = path.join(monthPath, `${id}.json`);
          if (fs.existsSync(filePath)) {
            fs.unlinkSync(filePath);
          }
        }
        fs.rmdirSync(monthPath);
      }

      // 更新索引
      for (const id of archive.memoryIds) {
        this.index.set(id, {
          month: monthStr,
          path: archivePath,
        });
      }

      await this.persistIndex();

      console.log(`[L2ColdStore] 归档月份 ${monthStr} (${validMemories.length} 条记忆)`);
    } catch (error) {
      console.error(`[L2ColdStore] 归档月份 ${monthStr} 失败:`, error);
    }
  }

  /**
   * 自动归档（后台任务）
   */
  async autoArchive(): Promise<number> {
    const now = Date.now();
    let archived = 0;

    for (const [monthStr, archive] of this.monthArchives.entries()) {
      if (archive.archived) {
        continue;
      }

      const monthDate = new Date(monthStr + '-01');
      const age = now - monthDate.getTime();

      // 超过配置天数后归档
      if (age > this.config.archiveAfterDays * 24 * 60 * 60 * 1000) {
        await this.archiveMonth(monthStr);
        archived++;
      }
    }

    if (archived > 0) {
      console.log(`[L2ColdStore] 自动归档了 ${archived} 个月份`);
    }

    return archived;
  }

  /**
   * 持久化索引
   */
  private async persistIndex(): Promise<void> {
    try {
      const indexPath = path.join(this.config.basePath, 'index.json');
      const data = {
        index: Object.fromEntries(this.index),
        monthArchives: Array.from(this.monthArchives.values()),
        timestamp: Date.now(),
      };

      fs.writeFileSync(indexPath, JSON.stringify(data, null, 2), 'utf-8');
    } catch (error) {
      console.error('[L2ColdStore] 持久化索引失败:', error);
    }
  }

  /**
   * 月份字符串
   */
  private toMonthString(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    return `${year}-${month}`;
  }

  /**
   * 获取统计信息
   */
  getStats(): {
    totalMemories: number;
    totalMonths: number;
    archivedMonths: number;
    totalSize: number;
  } {
    const totalSize = Array.from(this.monthArchives.values())
      .reduce((sum, a) => sum + a.totalSize, 0);

    const archivedMonths = Array.from(this.monthArchives.values())
      .filter(a => a.archived).length;

    return {
      totalMemories: this.index.size,
      totalMonths: this.monthArchives.size,
      archivedMonths,
      totalSize,
    };
  }

  /**
   * 清理查询缓存
   */
  clearQueryCache(): void {
    this.queryCache.clear();
  }
}
