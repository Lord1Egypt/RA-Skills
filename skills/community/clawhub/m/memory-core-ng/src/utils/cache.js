/**
 * 🎯 智能缓存系统
 * 分层缓存 + 智能过期
 */

class IntelligentCache {
  constructor(options = {}) {
    this.options = {
      defaultTTLs: {
        embeddings: 3600000,    // 1小时
        reranker: 1800000,      // 30分钟
        search: 600000,         // 10分钟
        metadata: 300000        // 5分钟
      },
      maxSize: 1000,            // 最大缓存条目数
      ...options
    };
    
    this.caches = new Map();
    this.timers = new Map();
    this.stats = {
      hits: 0,
      misses: 0,
      evictions: 0,
      sets: 0
    };
    
    // 初始化各个缓存层
    for (const category of Object.keys(this.options.defaultTTLs)) {
      this.caches.set(category, new Map());
    }
  }
  
  /**
   * 获取缓存值
   */
  get(category, key) {
    const cache = this.caches.get(category);
    if (!cache) {
      this.stats.misses++;
      return null;
    }
    
    if (cache.has(key)) {
      this.stats.hits++;
      
      // 更新访问时间（用于智能过期）
      const entry = cache.get(key);
      entry.lastAccessed = Date.now();
      
      return entry.value;
    }
    
    this.stats.misses++;
    return null;
  }
  
  /**
   * 设置缓存值
   */
  set(category, key, value, ttlMs = null) {
    let cache = this.caches.get(category);
    if (!cache) {
      cache = new Map();
      this.caches.set(category, cache);
    }
    
    // 检查缓存大小，如果超过限制则清理
    if (cache.size >= this.options.maxSize) {
      this.evictOldest(category);
    }
    
    const ttl = ttlMs || this.options.defaultTTLs[category] || 300000;
    const now = Date.now();
    
    const entry = {
      value,
      createdAt: now,
      lastAccessed: now,
      ttl
    };
    
    cache.set(key, entry);
    this.stats.sets++;
    
    // 设置自动过期
    const timerKey = `${category}:${key}`;
    if (this.timers.has(timerKey)) {
      clearTimeout(this.timers.get(timerKey));
    }
    
    const timer = setTimeout(() => {
      this.delete(category, key);
    }, ttl);
    
    this.timers.set(timerKey, timer);
    
    return true;
  }
  
  /**
   * 智能设置：根据使用频率调整 TTL
   */
  intelligentSet(category, key, value) {
    const cache = this.caches.get(category);
    if (!cache) {
      return this.set(category, key, value);
    }
    
    // 检查历史访问模式
    const existing = cache.get(key);
    let ttlMultiplier = 1;
    
    if (existing) {
      // 如果频繁访问，延长 TTL
      const accessCount = (existing.accessCount || 0) + 1;
      if (accessCount > 5) {
        ttlMultiplier = 2; // 双倍 TTL
      } else if (accessCount > 10) {
        ttlMultiplier = 3; // 三倍 TTL
      }
    }
    
    const baseTTL = this.options.defaultTTLs[category] || 300000;
    const ttl = baseTTL * ttlMultiplier;
    
    return this.set(category, key, value, ttl);
  }
  
  /**
   * 删除缓存
   */
  delete(category, key) {
    const cache = this.caches.get(category);
    if (!cache) {
      return false;
    }
    
    const deleted = cache.delete(key);
    if (deleted) {
      this.stats.evictions++;
      
      // 清理定时器
      const timerKey = `${category}:${key}`;
      if (this.timers.has(timerKey)) {
        clearTimeout(this.timers.get(timerKey));
        this.timers.delete(timerKey);
      }
    }
    
    return deleted;
  }
  
  /**
   * 清理最旧的条目
   */
  evictOldest(category) {
    const cache = this.caches.get(category);
    if (!cache || cache.size === 0) {
      return;
    }
    
    let oldestKey = null;
    let oldestTime = Date.now();
    
    for (const [key, entry] of cache.entries()) {
      if (entry.lastAccessed < oldestTime) {
        oldestTime = entry.lastAccessed;
        oldestKey = key;
      }
    }
    
    if (oldestKey) {
      this.delete(category, oldestKey);
    }
  }
  
  /**
   * 清空所有缓存
   */
  clear() {
    for (const [category, cache] of this.caches.entries()) {
      cache.clear();
      
      // 清理定时器
      for (const [timerKey, timer] of this.timers.entries()) {
        if (timerKey.startsWith(`${category}:`)) {
          clearTimeout(timer);
          this.timers.delete(timerKey);
        }
      }
    }
    
    this.stats.hits = 0;
    this.stats.misses = 0;
    this.stats.evictions = 0;
    this.stats.sets = 0;
    
    return true;
  }
  
  /**
   * 获取统计信息
   */
  getStats() {
    const cacheSizes = {};
    for (const [category, cache] of this.caches.entries()) {
      cacheSizes[category] = cache.size;
    }
    
    const hitRate = this.stats.hits + this.stats.misses > 0 
      ? this.stats.hits / (this.stats.hits + this.stats.misses) 
      : 0;
    
    return {
      ...this.stats,
      cacheSizes,
      hitRate: Math.round(hitRate * 10000) / 100, // 百分比，两位小数
      totalTimers: this.timers.size
    };
  }
}

module.exports = { IntelligentCache };
