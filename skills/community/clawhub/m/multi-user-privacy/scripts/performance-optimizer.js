#!/usr/bin/env node

/**
 * 性能优化模块
 * 
 * 功能：
 * 1. 配置缓存（减少磁盘 IO）
 * 2. 行为数据库缓存
 * 3. 内存管理
 * 
 * 用法：
 * const perf = require('./scripts/performance-optimizer');
 * perf.enable();
 */

const fs = require('fs');
const path = require('path');

// 缓存配置
const CACHE_CONFIG = {
  configTTL: 300000,        // 配置缓存 TTL（5 分钟）
  behaviorTTL: 60000,       // 行为缓存 TTL（1 分钟）
  maxCacheSize: 1000,       // 最大缓存条目数
  cleanupInterval: 300000   // 清理间隔（5 分钟）
};

// 内存缓存
const cache = {
  configs: {},
  behaviorDB: null,
  lastCleanup: Date.now()
};

/**
 * 带缓存的配置读取
 */
function getCachedConfig(configPath) {
  const now = Date.now();
  const cached = cache.configs[configPath];
  
  // 检查缓存是否有效
  if (cached && (now - cached.timestamp) < CACHE_CONFIG.configTTL) {
    return cached.data;
  }
  
  // 从磁盘读取
  try {
    const content = fs.readFileSync(configPath, 'utf-8');
    const data = JSON.parse(content);
    
    cache.configs[configPath] = {
      data,
      timestamp: now
    };
    
    return data;
  } catch (e) {
    console.warn('[PerfOptimizer] 读取配置失败:', configPath);
    return null;
  }
}

/**
 * 带缓存的行为数据库读取
 */
function getCachedBehaviorDB() {
  const now = Date.now();
  
  // 检查缓存是否有效
  if (cache.behaviorDB && (now - cache.behaviorDB.timestamp) < CACHE_CONFIG.behaviorTTL) {
    return cache.behaviorDB.data;
  }
  
  // 从磁盘读取
  const behaviorDBPath = path.join(process.env.HOME, '.openclaw/logs/behavior-db.json');
  try {
    if (fs.existsSync(behaviorDBPath)) {
      const content = fs.readFileSync(behaviorDBPath, 'utf-8');
      const data = JSON.parse(content);
      
      cache.behaviorDB = {
        data,
        timestamp: now
      };
      
      return data;
    }
  } catch (e) {
    // 忽略
  }
  
  return { users: {}, alerts: [] };
}

/**
 * 保存行为数据库（更新缓存）
 */
function saveCachedBehaviorDB(data) {
  const behaviorDBPath = path.join(process.env.HOME, '.openclaw/logs/behavior-db.json');
  
  const dir = path.dirname(behaviorDBPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  fs.writeFileSync(behaviorDBPath, JSON.stringify(data, null, 2), 'utf-8');
  
  // 更新缓存
  cache.behaviorDB = {
    data,
    timestamp: Date.now()
  };
}

/**
 * 清理过期缓存
 */
function cleanupCache() {
  const now = Date.now();
  let cleaned = 0;
  
  // 清理过期配置缓存
  Object.keys(cache.configs).forEach(key => {
    if ((now - cache.configs[key].timestamp) > CACHE_CONFIG.configTTL * 2) {
      delete cache.configs[key];
      cleaned++;
    }
  });
  
  // 清理过期行为缓存
  if (cache.behaviorDB && (now - cache.behaviorDB.timestamp) > CACHE_CONFIG.behaviorTTL * 2) {
    cache.behaviorDB = null;
    cleaned++;
  }
  
  // 检查缓存大小
  const cacheSize = Object.keys(cache.configs).length + (cache.behaviorDB ? 1 : 0);
  if (cacheSize > CACHE_CONFIG.maxCacheSize) {
    // 清理最旧的缓存
    const sortedKeys = Object.keys(cache.configs).sort((a, b) => {
      return cache.configs[a].timestamp - cache.configs[b].timestamp;
    });
    
    sortedKeys.slice(0, Math.floor(CACHE_CONFIG.maxCacheSize * 0.2)).forEach(key => {
      delete cache.configs[key];
      cleaned++;
    });
  }
  
  cache.lastCleanup = now;
  
  if (cleaned > 0) {
    console.log(`[PerfOptimizer] 🧹 清理了 ${cleaned} 个缓存条目`);
  }
}

/**
 * 启动性能优化器
 */
function enable() {
  console.log('[PerfOptimizer] ⚡ 性能优化已启用');
  console.log(`[PerfOptimizer]   配置缓存 TTL: ${CACHE_CONFIG.configTTL / 1000}秒`);
  console.log(`[PerfOptimizer]   行为缓存 TTL: ${CACHE_CONFIG.behaviorTTL / 1000}秒`);
  console.log(`[PerfOptimizer]   最大缓存条目：${CACHE_CONFIG.maxCacheSize}`);
  console.log(`[PerfOptimizer]   清理间隔：${CACHE_CONFIG.cleanupInterval / 1000}秒\n`);
  
  // 启动定期清理
  setInterval(cleanupCache, CACHE_CONFIG.cleanupInterval);
}

/**
 * 获取缓存统计
 */
function getCacheStats() {
  return {
    configCacheSize: Object.keys(cache.configs).length,
    behaviorCacheHit: cache.behaviorDB ? 1 : 0,
    lastCleanup: new Date(cache.lastCleanup).toISOString()
  };
}

/**
 * 清空缓存
 */
function clearCache() {
  cache.configs = {};
  cache.behaviorDB = null;
  cache.lastCleanup = Date.now();
  console.log('[PerfOptimizer] 🧹 缓存已清空');
}

// 导出
module.exports = {
  enable,
  getCachedConfig,
  getCachedBehaviorDB,
  saveCachedBehaviorDB,
  getCacheStats,
  clearCache,
  CACHE_CONFIG
};
