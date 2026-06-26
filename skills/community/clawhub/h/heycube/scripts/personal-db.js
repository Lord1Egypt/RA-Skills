/**
 * personal-db.js — 黑方体个人档案 SQLite 管理工具
 *
 * 用法:
 *   node personal-db.js init              初始化数据库
 *   node personal-db.js get <id>          查询单个维度
 *   node personal-db.js get-all           查询所有维度
 *   node personal-db.js set <id> <value>  写入/更新维度（value 为 JSON 字符串）
 *   node personal-db.js merge <id> <json> 合并更新维度（JSON 合并）
 *   node personal-db.js get-batch <ids>   批量查询（逗号分隔）
 */
const Database = require('better-sqlite3');
const fs = require('fs');
const path = require('path');

const DB_PATH = process.env.SOUL_DB_PATH || path.join(__dirname, '..', 'personal-db.sqlite');

function getDb() {
  return new Database(DB_PATH);
}

function init() {
  const db = getDb();
  db.exec(`
    CREATE TABLE IF NOT EXISTS dimensions (
      dimension_id TEXT PRIMARY KEY,
      value TEXT NOT NULL,
      updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    );
    CREATE INDEX IF NOT EXISTS idx_dim_parent ON dimensions(dimension_id);
  `);
  db.close();
  console.log(JSON.stringify({ status: 'ok', db: DB_PATH }));
}

function get(id) {
  const db = getDb();
  const row = db.prepare('SELECT dimension_id, value, updated_at FROM dimensions WHERE dimension_id = ?').get(id);
  db.close();
  console.log(JSON.stringify(row || null));
}

function getAll() {
  const db = getDb();
  const rows = db.prepare('SELECT dimension_id, value, updated_at FROM dimensions ORDER BY dimension_id').all();
  db.close();
  console.log(JSON.stringify(rows));
}

function set(id, value) {
  const db = getDb();
  db.prepare(`
    INSERT INTO dimensions (dimension_id, value, updated_at) VALUES (?, ?, datetime('now', 'localtime'))
    ON CONFLICT(dimension_id) DO UPDATE SET value = excluded.value, updated_at = datetime('now', 'localtime')
  `).run(id, value);
  db.close();
  console.log(JSON.stringify({ status: 'ok', dimension_id: id }));
}

function merge(id, jsonStr) {
  const db = getDb();
  const existing = db.prepare('SELECT value FROM dimensions WHERE dimension_id = ?').get(id);
  let newValue = jsonStr;
  if (existing) {
    try {
      const old = JSON.parse(existing.value);
      const patch = JSON.parse(jsonStr);
      newValue = JSON.stringify({ ...old, ...patch });
    } catch {
      newValue = jsonStr;
    }
  }
  db.prepare(`
    INSERT INTO dimensions (dimension_id, value, updated_at) VALUES (?, ?, datetime('now', 'localtime'))
    ON CONFLICT(dimension_id) DO UPDATE SET value = excluded.value, updated_at = datetime('now', 'localtime')
  `).run(id, newValue);
  db.close();
  console.log(JSON.stringify({ status: 'ok', dimension_id: id, merged: true }));
}

function getBatch(idsStr) {
  const ids = idsStr.split(',').map(s => s.trim()).filter(Boolean);
  const db = getDb();
  const stmt = db.prepare('SELECT dimension_id, value, updated_at FROM dimensions WHERE dimension_id = ?');
  const results = ids.map(id => stmt.get(id) || null);
  db.close();
  console.log(JSON.stringify(results));
}

const [,, cmd, ...args] = process.argv;
switch (cmd) {
  case 'init': init(); break;
  case 'get': get(args[0]); break;
  case 'get-all': getAll(); break;
  case 'set': set(args[0], args[1]); break;
  case 'merge': merge(args[0], args[1]); break;
  case 'get-batch': getBatch(args[0]); break;
  default: console.log('Usage: node personal-db.js [init|get|get-all|set|merge|get-batch] ...'); process.exit(1);
}
