#!/usr/bin/env node
/**
 * Config CLI
 * 配置管理命令行工具
 */

const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const DB_PATH = process.env.DB_PATH || 
                process.env.OPENCLAW_DB_PATH || 
                path.join(__dirname, '..', 'db', 'config.db');

/**
 * 获取数据库连接
 */
function getDb() {
  return new Database(DB_PATH);
}

/**
 * 初始化配置表
 */
function initConfigTable() {
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
  db.close();
  console.log('✅ 配置表已初始化');
}

/**
 * 设置配置
 */
function setConfig(key, value, description = '') {
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
  console.log(`✅ 配置已保存：${key}`);
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
 * 显示配置
 */
function showConfig(key) {
  const config = getConfig(key);
  if (!config) {
    console.error(`❌ 配置不存在：${key}`);
    return;
  }
  console.log(`\n配置：${config.key}`);
  console.log(`值：${config.value}`);
  console.log(`描述：${config.description || '无'}`);
  console.log(`更新时间：${config.updated_at}`);
}

/**
 * 列出所有配置
 */
function listConfigs() {
  const db = getDb();
  const rows = db.prepare('SELECT * FROM configs ORDER BY key').all();
  db.close();
  
  if (rows.length === 0) {
    console.log('📭 暂无配置');
    return;
  }
  
  console.log('\n配置列表:');
  console.log('─'.repeat(60));
  rows.forEach(row => {
    console.log(`  ${row.key.padEnd(30)} ${row.value ? '✓' : ''}`);
    if (row.description) {
      console.log(`    ${row.description}`);
    }
  });
  console.log('─'.repeat(60));
  console.log(`总计：${rows.length} 个配置`);
}

/**
 * 删除配置
 */
function deleteConfig(key) {
  const db = getDb();
  const stmt = db.prepare('DELETE FROM configs WHERE key = ?');
  const info = stmt.run(key);
  db.close();
  
  if (info.changes === 0) {
    console.error(`❌ 配置不存在：${key}`);
    return;
  }
  console.log(`✅ 配置已删除：${key}`);
}

/**
 * 备份配置
 */
function backupConfig(outputPath = null) {
  const db = getDb();
  const rows = db.prepare('SELECT * FROM configs').all();
  db.close();
  
  const backup = {
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    configs: rows
  };
  
  const targetPath = outputPath || path.join(__dirname, '..', 'config_backup.json');
  fs.writeFileSync(targetPath, JSON.stringify(backup, null, 2));
  console.log(`✅ 配置已备份到：${targetPath}`);
}

/**
 * 恢复配置
 */
function restoreConfig(inputPath) {
  if (!fs.existsSync(inputPath)) {
    console.error(`❌ 备份文件不存在：${inputPath}`);
    return;
  }
  
  const backup = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));
  const db = getDb();
  
  let successCount = 0;
  let failCount = 0;
  
  for (const config of backup.configs) {
    try {
      const stmt = db.prepare(`
        INSERT INTO configs (key, value, description)
        VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET
          value = excluded.value,
          description = excluded.description,
          updated_at = CURRENT_TIMESTAMP
      `);
      stmt.run(config.key, config.value, config.description);
      successCount++;
    } catch (error) {
      console.error(`❌ 恢复配置 ${config.key} 失败:`, error.message);
      failCount++;
    }
  }
  
  db.close();
  console.log(`✅ 配置恢复完成：成功 ${successCount} 个，失败 ${failCount} 个`);
}

/**
 * 导出配置
 */
function exportConfig(outputPath = null) {
  const db = getDb();
  const rows = db.prepare('SELECT key, value, description FROM configs').all();
  db.close();
  
  const targetPath = outputPath || path.join(__dirname, '..', 'config_export.json');
  fs.writeFileSync(targetPath, JSON.stringify(rows, null, 2));
  console.log(`✅ 配置已导出到：${targetPath}`);
}

/**
 * 导入配置
 */
function importConfig(inputPath) {
  if (!fs.existsSync(inputPath)) {
    console.error(`❌ 文件不存在：${inputPath}`);
    return;
  }
  
  const configs = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));
  const db = getDb();
  
  let successCount = 0;
  let failCount = 0;
  
  for (const config of configs) {
    try {
      const stmt = db.prepare(`
        INSERT INTO configs (key, value, description)
        VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET
          value = excluded.value,
          description = excluded.description,
          updated_at = CURRENT_TIMESTAMP
      `);
      stmt.run(config.key, config.value, config.description);
      successCount++;
    } catch (error) {
      console.error(`❌ 导入配置 ${config.key} 失败:`, error.message);
      failCount++;
    }
  }
  
  db.close();
  console.log(`✅ 配置导入完成：成功 ${successCount} 个，失败 ${failCount} 个`);
}

/**
 * 显示帮助信息
 */
function showHelp() {
  console.log(`
配置管理工具 - 使用说明

用法:
  node config-cli.js <命令> [参数]

命令:
  init                    初始化配置表
  set <key> <value>       设置配置
  get <key>               获取配置
  show <key>              显示配置详情
  list                    列出所有配置
  delete <key>            删除配置
  backup [输出路径]       备份配置
  restore <备份路径>      恢复配置
  export [输出路径]       导出配置
  import <输入路径>       导入配置
  help                    显示帮助信息

示例:
  node config-cli.js init
  node config-cli.js set AGENT_MAIN qqbot:c2c:123456
  node config-cli.js get AGENT_MAIN
  node config-cli.js list
  node config-cli.js backup
  node config-cli.js restore config_backup.json
`);
}

/**
 * 主函数
 */
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    showHelp();
    return;
  }
  
  switch (command) {
    case 'init':
      initConfigTable();
      break;
    case 'set':
      if (args.length < 3) {
        console.error('❌ 用法：set <key> <value> [description]');
        return;
      }
      setConfig(args[1], args[2], args[3] || '');
      break;
    case 'get':
    case 'show':
      if (args.length < 2) {
        console.error('❌ 用法：get/show <key>');
        return;
      }
      showConfig(args[1]);
      break;
    case 'list':
      listConfigs();
      break;
    case 'delete':
      if (args.length < 2) {
        console.error('❌ 用法：delete <key>');
        return;
      }
      deleteConfig(args[1]);
      break;
    case 'backup':
      backupConfig(args[1]);
      break;
    case 'restore':
      if (args.length < 2) {
        console.error('❌ 用法：restore <备份路径>');
        return;
      }
      restoreConfig(args[1]);
      break;
    case 'export':
      exportConfig(args[1]);
      break;
    case 'import':
      if (args.length < 2) {
        console.error('❌ 用法：import <输入路径>');
        return;
      }
      importConfig(args[1]);
      break;
    case 'help':
    default:
      showHelp();
      break;
  }
}

// 如果直接运行此文件
if (require.main === module) {
  main();
}

module.exports = {
  initConfigTable,
  setConfig,
  getConfig,
  showConfig,
  listConfigs,
  deleteConfig,
  backupConfig,
  restoreConfig,
  exportConfig,
  importConfig
};
