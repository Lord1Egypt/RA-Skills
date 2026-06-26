const Database = require('better-sqlite3');
const config = require('../config');

/**
 * 数据库管理 - 统一数据库连接
 */
class DatabaseManager {
  constructor(dbPath = null) {
    // 从配置文件读取数据库路径
    this.dbPath = dbPath || config.database.path;
    this.db = null;
  }

  /**
   * 初始化数据库连接
   */
  init() {
    try {
      this.db = new Database(this.dbPath);
      this.db.pragma('journal_mode = WAL');
      console.log(`✅ 数据库已连接：${this.dbPath}`);
      return true;
    } catch (error) {
      console.error('❌ 数据库连接失败:', error.message);
      return false;
    }
  }

  /**
   * 执行 SQL 查询
   */
  query(sql, params = []) {
    if (!this.db) {
      throw new Error('数据库未初始化');
    }
    return this.db.prepare(sql).run(...params);
  }

  /**
   * 执行 SQL 查询并获取结果
   */
  getAll(sql, params = []) {
    if (!this.db) {
      throw new Error('数据库未初始化');
    }
    return this.db.prepare(sql).all(...params);
  }

  /**
   * 执行 SQL 查询并获取单条结果
   */
  getOne(sql, params = []) {
    if (!this.db) {
      throw new Error('数据库未初始化');
    }
    return this.db.prepare(sql).get(...params);
  }

  /**
   * 关闭数据库连接
   */
  close() {
    if (this.db) {
      this.db.close();
      console.log('👋 数据库已关闭');
    }
  }

  /**
   * 获取数据库路径
   */
  getDbPath() {
    return this.dbPath;
  }
}

module.exports = { DatabaseManager };
