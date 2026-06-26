/**
 * Config Manager
 * 配置数据库操作模块
 */

const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const DB_PATH = process.env.DB_PATH || 
                process.env.OPENCLAW_DB_PATH || 
                path.join(__dirname, 'config.db');

/**
 * 获取数据库连接
 */
function getDb() {
  return new Database(DB_PATH);
}

/**
 * 初始化数据库表
 */
function initDatabase() {
  const db = getDb();
  
  db.exec(`
    CREATE TABLE IF NOT EXISTS configs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      key TEXT UNIQUE NOT NULL,
      value TEXT,
      description TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
  
  console.log('✅ 配置数据库表已初始化');
  db.close();
}

/**
 * 保存配置
 */
function saveConfig(key, value, description = '') {
  const db = getDb();
  const stmt = db.prepare(`
    INSERT INTO configs (key, value, description)
    VALUES (?, ?, ?)
    ON CONFLICT(key) DO UPDATE SET
      value = excluded.value,
      description = excluded.description,
      updated_at = CURRENT_TIMESTAMP
  `);
  
  stmt.run(key, value, description);
  db.close();
  return { key, value };
}

/**
 * 获取配置
 */
function getConfig(key) {
  const db = getDb();
  const row = db.prepare('SELECT * FROM configs WHERE key = ?').get(key);
  db.close();
  return row;
}

/**
 * 获取所有配置
 */
function getAllConfigs() {
  const db = getDb();
  const rows = db.prepare('SELECT * FROM configs ORDER BY key').all();
  db.close();
  return rows;
}

/**
 * 删除配置
 */
function deleteConfig(key) {
  const db = getDb();
  const stmt = db.prepare('DELETE FROM configs WHERE key = ?');
  const info = stmt.run(key);
  db.close();
  return { changes: info.changes };
}

/**
 * 备份配置
 */
function backupConfig(backupPath = null) {
  const defaultBackupPath = path.join(__dirname, 'config_backup.json');
  const targetPath = backupPath || defaultBackupPath;
  
  const configs = getAllConfigs();
  const backup = {
    timestamp: new Date().toISOString(),
    configs: configs
  };
  
  fs.writeFileSync(targetPath, JSON.stringify(backup, null, 2));
  return { path: targetPath, count: configs.length };
}

/**
 * 恢复配置
 */
function restoreConfig(backupPath) {
  const backupData = JSON.parse(fs.readFileSync(backupPath, 'utf-8'));
  
  const results = [];
  for (const config of backupData.configs) {
    try {
      saveConfig(config.key, config.value, config.description);
      results.push({ key: config.key, success: true });
    } catch (error) {
      results.push({ key: config.key, success: false, error: error.message });
    }
  }
  
  return {
    total: backupData.configs.length,
    success: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length
  };
}

/**
 * 导出配置为 JSON
 */
function exportConfig() {
  const configs = getAllConfigs();
  return JSON.stringify(configs, null, 2);
}

/**
 * 从 JSON 导入配置
 */
function importConfig(jsonString) {
  const configs = JSON.parse(jsonString);
  
  const results = [];
  for (const config of configs) {
    try {
      saveConfig(config.key, config.value, config.description);
      results.push({ key: config.key, success: true });
    } catch (error) {
      results.push({ key: config.key, success: false, error: error.message });
    }
  }
  
  return {
    total: configs.length,
    success: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length
  };
}

module.exports = {
  initDatabase,
  saveConfig,
  getConfig,
  getAllConfigs,
  deleteConfig,
  backupConfig,
  restoreConfig,
  exportConfig,
  importConfig
};
