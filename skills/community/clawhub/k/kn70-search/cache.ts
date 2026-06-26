/**
 * 搜索结果缓存
 * 防止重复搜索相同内容
 */

export class SearchCache {
  private static readonly TTL_MS = 5 * 60 * 1000; // 5 minutes
  private static cache = new Map<string, { data: any[], timestamp: number }>();
  
  /**
   * 生成缓存键
   * @param engine 搜索引擎
   * @param query 搜索查询
   * @returns 缓存键
   */
  static generateKey(engine: string, query: string): string {
    const hash = require('crypto').createHash('md5');
    hash.update(`${engine}::${query}`);
    return hash.digest('hex');
  }
  
  /**
   * 获取缓存结果
   * @param key 缓存键
   * @returns 缓存数据或 null
   */
  static get(key: string): any[] | null {
    const cached = this.cache.get(key);
    if (!cached) {
      return null;
    }
    
    // 检查是否过期
    if (Date.now() - cached.timestamp > this.TTL_MS) {
      this.cache.delete(key);
      return null;
    }
    
    return cached.data;
  }
  
  /**
   * 设置缓存
   * @param key 缓存键
   * @param data 缓存数据
   */
  static set(key: string, data: any[]): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now()
    });
  }
  
  /**
   * 清理过期缓存
   */
  static cleanup(): void {
    const now = Date.now();
    for (const [key, cached] of this.cache.entries()) {
      if (now - cached.timestamp > this.TTL_MS) {
        this.cache.delete(key);
      }
    }
  }
}
