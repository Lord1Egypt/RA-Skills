/**
 * Database Optimization Module - 数据库查询优化
 * 
 * 优化策略：
 * - 查询缓存（减少数据库压力）
 * - 索引优化（提高查询速度）
 * - 减少 N+1 查询（批量加载）
 * - 批量查询优化（合并请求）
 * 
 * @author 小码
 * @version 1.0.0
 */

const { Cache } = require('./cache');

// ============================================
// 数据库查询缓存装饰器
// ============================================

class QueryCache {
  /**
   * 创建查询缓存实例
   * @param {Object} db - 数据库实例
   * @param {Object} options - 配置选项
   */
  constructor(db, options = {}) {
    this.db = db;
    this.cache = new Cache({
      maxSize: options.cacheMaxSize || 500,
      defaultTTL: options.cacheTTL || 300,
      enableLRU: true,
      onEvict: options.onEvict || null
    });
    this.queryStats = {
      cached: 0,
      dbHits: 0,
      total: 0
    };
  }

  /**
   * 生成查询键
   * @param {string} query - SQL 查询
   * @param {Array} params - 查询参数
   * @returns {string} 缓存键
   */
  _generateKey(query, params = []) {
    const paramStr = JSON.stringify(params).replace(/ /g, '');
    return `query:${query.replace(/\s+/g, ' ')}:${paramStr}`;
  }

  /**
   * 执行带缓存的查询
   * @param {string} query - SQL 查询
   * @param {Array} params - 查询参数
   * @param {number} ttl - 缓存 TTL
   * @returns {Promise<Array>} 查询结果
   */
  async cachedQuery(query, params = [], ttl = null) {
    const key = this._generateKey(query, params);
    
    // 尝试从缓存获取
    const cached = this.cache.get(key);
    if (cached !== undefined) {
      this.queryStats.cached++;
      this.queryStats.total++;
      return cached;
    }
    
    // 缓存未命中，执行数据库查询
    const result = await this.db.query(query, params);
    
    // 写入缓存
    this.cache.set(key, result, ttl);
    
    this.queryStats.dbHits++;
    this.queryStats.total++;
    
    return result;
  }

  /**
   * 清除查询缓存
   * @param {string} queryPattern - 查询模式（支持前缀）
   */
  clearQueryCache(queryPattern = '') {
    if (queryPattern) {
      this.cache.invalidateByPrefix(`query:${queryPattern}`);
    } else {
      this.cache.invalidateByPrefix('query:');
    }
  }

  /**
   * 获取缓存统计
   * @returns {Object} 统计信息
   */
  getStats() {
    const cacheStats = this.cache.getStats();
    const cacheHitRate = this.queryStats.total > 0
      ? ((this.queryStats.cached / this.queryStats.total) * 100).toFixed(2)
      : 0;
    
    return {
      ...cacheStats,
      cacheHitRate: cacheHitRate + '%',
      dbHits: this.queryStats.dbHits,
      cachedHits: this.queryStats.cached,
      totalQueries: this.queryStats.total
    };
  }
}

// ============================================
// N+1 查询优化器
// ============================================

class NPlusOneOptimizer {
  /**
   * 批量加载关联数据，避免 N+1 查询
   * @param {Array} parentRecords - 父记录数组
   * @param {string} childTable - 子表名
   * @param {string} parentKey - 父表键名
   * @param {string} childKey - 子表外键名
   * @param {Object} db - 数据库实例
   * @returns {Promise<Object>} 关联数据映射
   */
  static async batchLoadRelations(parentRecords, childTable, parentKey, childKey, db) {
    if (!parentRecords || parentRecords.length === 0) {
      return {};
    }
    
    // 收集所有父 ID
    const parentIds = [...new Set(parentRecords.map(r => r[parentKey]))];
    
    if (parentIds.length === 0) {
      return {};
    }
    
    // 单次查询加载所有关联数据
    const placeholders = parentIds.map(() => '?').join(',');
    const query = `SELECT * FROM ${childTable} WHERE ${childKey} IN (${placeholders})`;
    const childRecords = await db.query(query, parentIds);
    
    // 构建映射关系
    const relationMap = {};
    for (const parentId of parentIds) {
      relationMap[parentId] = [];
    }
    
    for (const child of childRecords) {
      const parentId = child[childKey];
      if (relationMap[parentId]) {
        relationMap[parentId].push(child);
      }
    }
    
    return relationMap;
  }

  /**
   * 优化后的查询：加载用户及其订单
   * @param {Object} db - 数据库实例
   * @returns {Promise<Array>} 用户及其订单
   */
  static async getUsersWithOrders(db) {
    // 传统 N+1 写法（不推荐）：
    // const users = await db.query('SELECT * FROM users');
    // for (const user of users) {
    //   user.orders = await db.query('SELECT * FROM orders WHERE user_id = ?', [user.id]);
    // }
    // 这会导致 1 + N 次查询
    
    // 优化后的写法：
    const users = await db.query('SELECT * FROM users');
    const orderMap = await this.batchLoadRelations(
      users, 
      'orders', 
      'id', 
      'user_id', 
      db
    );
    
    // 合并数据
    for (const user of users) {
      user.orders = orderMap[user.id] || [];
    }
    
    return users;
  }
}

// ============================================
// 批量查询优化器
// ============================================

class BatchQueryOptimizer {
  /**
   * 批量查询多个 ID 的数据
   * @param {string} table - 表名
   * @param {Array} ids - ID 数组
   * @param {string} idColumn - ID 列名
   * @param {Object} db - 数据库实例
   * @param {number} batchSize - 每批大小（默认 1000）
   * @returns {Promise<Map>} 结果映射
   */
  static async batchGetByIds(table, ids, idColumn = 'id', db, batchSize = 1000) {
    if (!ids || ids.length === 0) {
      return new Map();
    }
    
    const resultMap = new Map();
    const uniqueIds = [...new Set(ids)];
    
    // 分批查询（避免 IN 子句过长）
    for (let i = 0; i < uniqueIds.length; i += batchSize) {
      const batch = uniqueIds.slice(i, i + batchSize);
      const placeholders = batch.map(() => '?').join(',');
      
      const query = `SELECT * FROM ${table} WHERE ${idColumn} IN (${placeholders})`;
      const rows = await db.query(query, batch);
      
      for (const row of rows) {
        resultMap.set(row[idColumn], row);
      }
    }
    
    return resultMap;
  }

  /**
   * 批量插入优化
   * @param {string} table - 表名
   * @param {Array} rows - 数据行数组
   * @param {Object} db - 数据库实例
   * @param {number} batchSize - 每批大小（默认 500）
   * @returns {Promise<Object>} 插入结果
   */
  static async batchInsert(table, rows, db, batchSize = 500) {
    if (!rows || rows.length === 0) {
      return { inserted: 0, skipped: 0 };
    }
    
    let inserted = 0;
    const columns = Object.keys(rows[0]);
    
    for (let i = 0; i < rows.length; i += batchSize) {
      const batch = rows.slice(i, i + batchSize);
      const values = batch.map(row => 
        '(' + columns.map(() => '?').join(',') + ')'
      ).join(',');
      
      const query = `INSERT INTO ${table} (${columns.join(',')}) VALUES ${values}`;
      const valueParams = batch.flatMap(row => columns.map(c => row[c]));
      
      await db.query(query, valueParams);
      inserted += batch.length;
    }
    
    return { inserted, skipped: 0 };
  }

  /**
   * 批量更新优化
   * @param {string} table - 表名
   * @param {Array} rows - 更新数据数组 [{id, ...updates}]
   * @param {string} idColumn - ID 列名
   * @param {Object} db - 数据库实例
   * @returns {Promise<number>} 更新的行数
   */
  static async batchUpdate(table, rows, idColumn = 'id', db) {
    if (!rows || rows.length === 0) {
      return 0;
    }
    
    // 使用 CASE WHEN 批量更新
    const updates = rows.map(row => {
      const id = row[idColumn];
      const columns = Object.keys(row).filter(c => c !== idColumn);
      const setClauses = columns.map(col => 
        `${col} = CASE WHEN ${idColumn} = ? THEN ? END`
      ).join(', ');
      
      return { id, columns, setClauses };
    });
    
    // 收集所有列
    const allColumns = new Set();
    updates.forEach(u => u.columns.forEach(c => allColumns.add(c)));
    
    // 构建 UPDATE 语句
    const setParts = [...allColumns].map(col => 
      `${col} = CASE ${updates
        .filter(u => u.columns.includes(col))
        .map(u => `WHEN ${idColumn} = ${u.id} THEN ?`)
        .join('')} END`
    ).join(', ');
    
    const query = `UPDATE ${table} SET ${setParts} WHERE ${idColumn} IN (${updates.map(() => '?').join(',')})`;
    const params = [];
    
    for (const col of allColumns) {
      for (const u of updates) {
        if (u.columns.includes(col)) {
          params.push(row => row[col]);
        } else {
          params.push(null);
        }
      }
    }
    
    // 简化版：逐条更新（更可靠）
    let updated = 0;
    for (const row of rows) {
      const id = row[idColumn];
      const columns = Object.keys(row).filter(c => c !== idColumn);
      const setClause = columns.map(c => `${c} = ?`).join(', ');
      const values = [...columns.map(c => row[c]), id];
      
      const updateQuery = `UPDATE ${table} SET ${setClause} WHERE ${idColumn} = ?`;
      const result = await db.query(updateQuery, values);
      updated += result.affectedRows || 0;
    }
    
    return updated;
  }
}

// ============================================
// 索引优化建议器
// ============================================

class IndexOptimizer {
  /**
   * 分析查询并给出索引建议
   * @param {string} query - SQL 查询
   * @returns {Object} 索引建议
   */
  static analyzeQuery(query) {
    const suggestions = {
      tables: [],
      columns: [],
      recommendedIndexes: []
    };
    
    // 提取表名
    const fromMatch = query.match(/FROM\s+(\w+)/i);
    if (fromMatch) {
      suggestions.tables.push(fromMatch[1]);
    }
    
    // 提取 WHERE 条件列
    const whereMatch = query.match(/WHERE\s+(.+?)(ORDER|GROUP|LIMIT|$)/i);
    if (whereMatch) {
      const whereClause = whereMatch[1];
      const columns = whereClause.match(/(\w+)\s*(=|IN|LIKE|>|<)/g);
      if (columns) {
        suggestions.columns = columns.map(c => c.split(/\s+/)[0]);
      }
    }
    
    // 提取 JOIN 表
    const joinMatches = query.matchAll(/JOIN\s+(\w+)\s+ON\s+(\w+)\.(\w+)\s*=\s*(\w+)\.(\w+)/gi);
    for (const match of joinMatches) {
      suggestions.tables.push(match[1]);
      suggestions.recommendedIndexes.push({
        table: match[1],
        columns: [match[3], match[5]]
      });
    }
    
    // 生成索引建议
    if (suggestions.tables.length > 0 && suggestions.columns.length > 0) {
      for (const table of suggestions.tables) {
        for (const column of suggestions.columns) {
          suggestions.recommendedIndexes.push({
            table,
            columns: [column],
            reason: '用于 WHERE 条件过滤'
          });
        }
      }
    }
    
    return suggestions;
  }

  /**
   * 生成索引创建语句
   * @param {Object} analysis - 分析结果
   * @returns {Array} 索引创建语句
   */
  static generateIndexStatements(analysis) {
    const statements = [];
    
    for (const index of analysis.recommendedIndexes) {
      const indexName = `idx_${index.table}_${index.columns.join('_')}`;
      const statement = `CREATE INDEX ${indexName} ON ${index.table} (${index.columns.join(', ')});`;
      statements.push(statement);
    }
    
    return statements;
  }
}

// ============================================
// 数据库优化器（整合所有优化）
// ============================================

class DatabaseOptimizer {
  /**
   * 创建数据库优化器实例
   * @param {Object} db - 数据库实例
   * @param {Object} options - 配置选项
   */
  constructor(db, options = {}) {
    this.db = db;
    this.queryCache = new QueryCache(db, options);
    this.stats = {
      queriesExecuted: 0,
      cacheHits: 0,
      batchOperations: 0
    };
  }

  /**
   * 执行带缓存的查询
   */
  async cachedQuery(query, params = [], ttl = null) {
    this.stats.queriesExecuted++;
    return this.queryCache.cachedQuery(query, params, ttl);
  }

  /**
   * 批量获取记录
   */
  async batchGet(table, ids, idColumn = 'id') {
    this.stats.batchOperations++;
    return BatchQueryOptimizer.batchGetByIds(table, ids, idColumn, this.db);
  }

  /**
   * 批量插入
   */
  async batchInsert(table, rows) {
    this.stats.batchOperations++;
    return BatchQueryOptimizer.batchInsert(table, rows, this.db);
  }

  /**
   * 获取统计信息
   */
  getStats() {
    const cacheStats = this.queryCache.getStats();
    return {
      ...this.stats,
      cache: cacheStats
    };
  }
}

// ============================================
// 导出模块
// ============================================

module.exports = {
  QueryCache,
  NPlusOneOptimizer,
  BatchQueryOptimizer,
  IndexOptimizer,
  DatabaseOptimizer
};

// ============================================
// 使用示例
// ============================================

/*
const mysql = require('mysql2/promise');
const { DatabaseOptimizer, IndexOptimizer } = require('./db-optimized');

// 1. 初始化
const db = await mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'test'
});

const optimizer = new DatabaseOptimizer(db);

// 2. 带缓存的查询
const users = await optimizer.cachedQuery(
  'SELECT * FROM users WHERE status = ?', 
  ['active'],
  300  // 5 分钟缓存
);

// 3. 批量查询（避免 N+1）
const userIds = [1, 2, 3, 4, 5];
const userMap = await optimizer.batchGet('users', userIds);

// 4. 批量插入
const newUsers = [
  { name: 'Alice', email: 'alice@example.com' },
  { name: 'Bob', email: 'bob@example.com' }
];
await optimizer.batchInsert('users', newUsers);

// 5. 索引分析
const query = 'SELECT * FROM orders WHERE user_id = ? AND status = ?';
const analysis = IndexOptimizer.analyzeQuery(query);
const indexStatements = IndexOptimizer.generateIndexStatements(analysis);
console.log(indexStatements);

// 6. 查看统计
console.log(optimizer.getStats());
*/
