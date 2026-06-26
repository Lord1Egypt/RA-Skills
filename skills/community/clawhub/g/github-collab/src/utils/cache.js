/**
 * 高性能缓存模块
 * 支持内存缓存、TTL 过期、LRU 淘汰策略、缓存预热
 */

class CacheNode {
  constructor(key, value, ttl) {
    this.key = key;
    this.value = value;
    this.createdAt = Date.now();
    this.expiresAt = ttl ? this.createdAt + ttl : null;
    this.prev = null;
    this.next = null;
  }

  isExpired() {
    if (!this.expiresAt) return false;
    return Date.now() > this.expiresAt;
  }
}

class LRUCache {
  /**
   * 创建 LRU 缓存实例
   * @param {Object} options - 配置选项
   * @param {number} options.maxSize - 最大缓存项数
   * @param {number} options.defaultTTL - 默认 TTL（毫秒）
   * @param {Function} options.onEvict - 淘汰回调函数
   */
  constructor(options = {}) {
    this.maxSize = options.maxSize || 1000;
    this.defaultTTL = options.defaultTTL || 300; // 默认 300 秒
    this.onEvict = options.onEvict || null;
    this.enableLRU = options.enableLRU !== false; // 默认启用 LRU
    
    // 核心数据结构
    this.cache = new Map(); // key -> CacheNode
    this.head = new CacheNode(null, null); // 虚拟头节点
    this.tail = new CacheNode(null, null); // 虚拟尾节点
    this.head.next = this.tail;
    this.tail.prev = this.head;
    
    // 统计信息
    this.stats = {
      hits: 0,
      misses: 0,
      evictions: 0,
      expirations: 0
    };
  }

  /**
   * 将节点移动到链表头部（最近使用）
   */
  _moveToFront(node) {
    // 先从原位置移除
    node.prev.next = node.next;
    node.next.prev = node.prev;
    
    // 插入到头部
    node.next = this.head.next;
    node.prev = this.head;
    this.head.next.prev = node;
    this.head.next = node;
  }

  /**
   * 从链表中移除节点
   */
  _removeNode(node) {
    node.prev.next = node.next;
    node.next.prev = node.prev;
  }

  /**
   * 淘汰最久未使用的节点
   */
  _evict() {
    if (!this.enableLRU) {
      // 禁用 LRU 时，不淘汰
      return;
    }
    
    if (this.cache.size >= this.maxSize) {
      const lruNode = this.tail.prev;
      if (lruNode !== this.head) {
        this._removeNode(lruNode);
        this.cache.delete(lruNode.key);
        this.stats.evictions++;
        
        if (this.onEvict) {
          this.onEvict(lruNode.key, lruNode.value);
        }
      }
    }
  }

  /**
   * 获取缓存值
   * @param {string} key - 缓存键
   * @returns {*} 缓存值，未找到返回 undefined
   */
  get(key) {
    const node = this.cache.get(key);
    
    if (!node) {
      this.stats.misses++;
      return undefined;
    }
    
    // 检查是否过期
    if (node.isExpired()) {
      this._removeNode(node);
      this.cache.delete(key);
      this.stats.expirations++;
      this.stats.misses++;
      
      // 调用淘汰回调
      if (this.onEvict) {
        this.onEvict(key, node.value);
      }
      
      return undefined;
    }
    
    // 移动到头部（标记为最近使用）
    this._moveToFront(node);
    this.stats.hits++;
    
    return node.value;
  }

  /**
   * 设置缓存值
   * @param {string} key - 缓存键
   * @param {*} value - 缓存值
   * @param {number} ttl - TTL（毫秒），不传则使用默认值
   */
  set(key, value, ttl = this.defaultTTL) {
    const existingNode = this.cache.get(key);
    
    if (existingNode) {
      // 更新已有项
      existingNode.value = value;
      existingNode.createdAt = Date.now();
      existingNode.expiresAt = ttl ? existingNode.createdAt + ttl : null;
      if (this.enableLRU) {
        this._moveToFront(existingNode);
      }
      return true;
    } else {
      // 创建新项
      this._evict(); // 先检查是否需要淘汰
      
      const node = new CacheNode(key, value, ttl);
      this.cache.set(key, node);
      
      // 插入到头部
      node.next = this.head.next;
      node.prev = this.head;
      this.head.next.prev = node;
      this.head.next = node;
      
      return true;
    }
  }

  /**
   * 删除指定键
   * @param {string} key - 缓存键
   * @returns {boolean} 是否成功删除
   */
  delete(key) {
    const node = this.cache.get(key);
    
    if (!node) return false;
    
    this._removeNode(node);
    this.cache.delete(key);
    return true;
  }

  /**
   * 清空所有缓存
   */
  clear() {
    this.cache.clear();
    this.head.next = this.tail;
    this.tail.prev = this.head;
  }

  /**
   * 检查键是否存在
   * @param {string} key - 缓存键
   * @returns {boolean}
   */
  has(key) {
    const node = this.cache.get(key);
    if (!node) return false;
    if (node.isExpired()) {
      this._removeNode(node);
      this.cache.delete(key);
      return false;
    }
    return true;
  }

  /**
   * 获取缓存大小
   * @returns {number}
   */
  size() {
    let count = 0;
    for (const [key, node] of this.cache) {
      if (!node.isExpired()) {
        count++;
      }
    }
    return count;
  }

  /**
   * 获取统计信息
   * @returns {Object}
   */
  getStats() {
    const total = this.stats.hits + this.stats.misses;
    return {
      ...this.stats,
      hitRate: total > 0 ? ((this.stats.hits / total) * 100).toFixed(2) + '%' : '0%',
      size: this.cache.size,
      maxSize: this.maxSize
    };
  }

  /**
   * 重置统计信息
   */
  resetStats() {
    this.stats = {
      hits: 0,
      misses: 0,
      evictions: 0,
      expirations: 0
    };
  }

  /**
   * 预热缓存
   * @param {Array<{key: string, value: *, ttl?: number}>} items - 预热数据
   */
  warmUp(items) {
    for (const item of items) {
      this.set(item.key, item.value, item.ttl);
    }
  }

  /**
   * 预热缓存（别名）
   * @param {Array<{key: string, value: *, ttl?: number}>} items - 预热数据
   */
  warm(items) {
    this.warmUp(items);
  }

  /**
   * 刷新 TTL
   * @param {string} key - 缓存键
   * @param {number} ttl - TTL（毫秒），不传则使用默认值
   */
  /**
   * 刷新缓存项的 TTL
   * @param {string} key - 缓存键
   * @param {number} ttl - 新的 TTL（毫秒），不传则使用默认值
   * @returns {boolean} 是否成功刷新
   */
  refresh(key, ttl = this.defaultTTL) {
    const node = this.cache.get(key);
    if (node) {
      const now = Date.now();
      node.createdAt = now;
      // ttl 为 0 或 false 时永不过期，否则使用指定 TTL
      node.expiresAt = (ttl !== 0 && ttl !== false) ? now + ttl : null;
      this._moveToFront(node);
      return true;
    }
    return false;
  }

  /**
   * 批量获取缓存
   * @param {string[]} keys - 缓存键列表
   * @returns {Object} 键值对对象
   */
  getMany(keys) {
    const result = {};
    for (const key of keys) {
      const value = this.get(key);
      if (value !== undefined) {
        result[key] = value;
      }
    }
    return result;
  }

  /**
   * 批量设置缓存
   * @param {Object} data - 键值对对象
   * @param {number} ttl - TTL（毫秒），不传则使用默认值
   */
  setMany(data, ttl = this.defaultTTL) {
    for (const [key, value] of Object.entries(data)) {
      this.set(key, value, ttl);
    }
  }

  /**
   * 批量删除缓存
   * @param {string[]} keys - 缓存键列表
   * @returns {number} 删除的数量
   */
  deleteMany(keys) {
    let count = 0;
    for (const key of keys) {
      if (this.delete(key)) {
        count++;
      }
    }
    return count;
  }

  /**
   * 根据前缀失效缓存
   * @param {string} prefix - 前缀
   * @returns {number} 失效的数量
   */
  invalidateByPrefix(prefix) {
    let count = 0;
    const keysToDelete = [];
    
    for (const key of this.cache.keys()) {
      if (key.startsWith(prefix)) {
        keysToDelete.push(key);
      }
    }
    
    for (const key of keysToDelete) {
      this.delete(key);
      count++;
    }
    
    return count;
  }

  /**
   * 根据正则模式失效缓存
   * @param {RegExp} pattern - 正则表达式
   * @returns {number} 失效的数量
   */
  invalidateByPattern(pattern) {
    let count = 0;
    const keysToDelete = [];
    
    for (const key of this.cache.keys()) {
      if (pattern.test(key)) {
        keysToDelete.push(key);
      }
    }
    
    for (const key of keysToDelete) {
      this.delete(key);
      count++;
    }
    
    return count;
  }

  /**
   * 清除过期缓存
   * @returns {number} 清理的数量
   */
  clearExpired() {
    return this.cleanup();
  }

  /**
   * 获取所有有效键
   * @returns {string[]}
   */
  getValidKeys() {
    return this.keys();
  }

  /**
   * 获取所有键
   * @returns {string[]}
   */
  keys() {
    const result = [];
    for (const [key, node] of this.cache) {
      if (!node.isExpired()) {
        result.push(key);
      }
    }
    return result;
  }

  /**
   * 过期清理（主动清理所有过期项）
   * @returns {number} 清理的数量
   */
  cleanup() {
    let count = 0;
    const expiredKeys = [];
    
    for (const [key, node] of this.cache) {
      if (node.isExpired()) {
        expiredKeys.push(key);
      }
    }
    
    for (const key of expiredKeys) {
      this.delete(key);
      count++;
    }
    
    this.stats.expirations += count;
    return count;
  }
}

// 导出
module.exports = { LRUCache, Cache: LRUCache, CacheNode };
