#!/usr/bin/env node
/**
 * Initialize Database
 * 初始化数据库脚本
 */

const path = require('path');
const { initDatabase, initDefaultAgents } = require('../db/init');

const DB_PATH = path.join(__dirname, '..', 'db', 'github-collab.db');

console.log('🚀 初始化数据库...\n');
console.log(`数据库路径：${DB_PATH}\n`);

try {
  const db = initDatabase(DB_PATH);
  initDefaultAgents(db);
  db.close();
  console.log('\n✅ 数据库初始化完成！');
} catch (error) {
  console.error('❌ 初始化失败:', error);
  process.exit(1);
}
