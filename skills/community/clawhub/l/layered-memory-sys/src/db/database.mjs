// database.mjs - SQLite 数据库管理 (v2.0)
// 使用 sql.js (SQLite WASM) 实现，零原生编译依赖

import initSqlJs from 'sql.js';
import fs from 'fs';
import path from 'path';
import { getPath } from './config-loader.mjs';

let _db = null;
let _savePath = null;

// 初始化数据库
export async function initDatabase(config) {
  const SQL = await initSqlJs();
  const dbPath = getPath('memoryDir', config);
  const dbFile = path.join(dbPath, 'memory.db');

  // 加载已有数据库或创建新的
  if (fs.existsSync(dbFile)) {
    const buf = fs.readFileSync(dbFile);
    _db = new SQL.Database(buf);
  } else {
    _db = new SQL.Database();
  }
  _savePath = dbFile;

  // 执行 schema
  const schema = fs.readFileSync(
    new URL('./schema.sql', import.meta.url),
    'utf-8'
  );
  _db.run(schema);

  console.log(`✅ 数据库已初始化: ${dbFile}`);
  return _db;
}

// 保存到磁盘（WAL 模拟：每次写入后保存）
export function saveDatabase() {
  if (!_db || !_savePath) return;
  const data = _db.export();
  const buffer = Buffer.from(data);
  fs.writeFileSync(_savePath, buffer);
}

// 获取数据库实例
export function getDb() {
  if (!_db) throw new Error('数据库未初始化，请先调用 initDatabase()');
  return _db;
}

// 原子事务执行
export function transaction(fn) {
  const db = getDb();
  try {
    db.exec('BEGIN');
    const result = fn(db);
    db.exec('COMMIT');
    saveDatabase();
    return result;
  } catch (e) {
    db.exec('ROLLBACK');
    throw e;
  }
}

// 从 JSON 迁移数据
export function migrateFromJSON(config) {
  const jsonPath = getPath('indexFile', config);
  if (!fs.existsSync(jsonPath)) {
    console.log('ℹ️ 未找到 index.json，跳过迁移');
    return;
  }

  const data = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
  const memories = data.memories || [];
  if (memories.length === 0) {
    console.log('ℹ️ index.json 无记忆数据，跳过迁移');
    return;
  }

  const db = getDb();
  let migrated = 0;

  db.exec('BEGIN');
  try {
    for (const mem of memories) {
      const createdTs = new Date(mem.created || mem.lastActive).getTime();
      const lastActiveTs = new Date(mem.lastActive || mem.created).getTime();

      db.run(
        `INSERT OR REPLACE INTO memories 
         (id, title, summary, content, layer, ttl, type, status, 
          created_at, last_active, recall_count, recall_days, turns, 
          remind_at, auto_detected, source, metadata, created_ts, last_active_ts)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        [
          mem.id, mem.title, mem.summary || '', mem.content || '',
          mem.layer || 'active', mem.ttl || 7, mem.type || 'exploration',
          mem.status || 'active', mem.created || new Date().toISOString().split('T')[0],
          mem.lastActive || new Date().toISOString().split('T')[0],
          mem.recallCount || 0, JSON.stringify(mem.recallDays || []),
          mem.turns || 0, mem.remindAt || null,
          mem.autoDetected ? 1 : 0, mem.source || '',
          JSON.stringify({}), createdTs, lastActiveTs
        ]
      );

      // 标签
      if (db.exec('SELECT changes()').length > 0 || true) {
        for (const tag of mem.tags || []) {
          db.run(
            'INSERT OR IGNORE INTO memory_tags (memory_id, tag) VALUES (?, ?)',
            [mem.id, tag]
          );
        }
      }

      // 事件记录
      db.run(
        'INSERT INTO events (event_type, memory_id, detail) VALUES (?, ?, ?)',
        ['migrated', mem.id, JSON.stringify({ from: 'index.json' })]
      );

      migrated++;
    }

    db.exec('COMMIT');
    saveDatabase();

    // 备份原始 JSON
    const backupPath = jsonPath + '.v1-backup';
    fs.copyFileSync(jsonPath, backupPath);
    console.log(`✅ 迁移完成: ${migrated} 条记忆从 JSON → SQLite`);
    console.log(`📄 JSON 备份: ${backupPath}`);
  } catch (e) {
    db.exec('ROLLBACK');
    throw e;
  }
}
