const Database = require('better-sqlite3');
const path = require('path');

const DB_PATH = path.join(__dirname, 'memos.db');

let db;

function getDb() {
  if (!db) {
    db = new Database(DB_PATH);
    db.pragma('journal_mode = WAL');
    db.pragma('foreign_keys = ON');
    initSchema();
  }
  return db;
}

function initSchema() {
  db.exec(`
    CREATE TABLE IF NOT EXISTS memos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL DEFAULT '',
      content TEXT NOT NULL DEFAULT '',
      tags TEXT NOT NULL DEFAULT '[]',
      pinned INTEGER NOT NULL DEFAULT 0,
      created_at TEXT NOT NULL DEFAULT (datetime('now', '+8 hours')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now', '+8 hours'))
    );

    CREATE INDEX IF NOT EXISTS idx_memos_created_at ON memos(created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_memos_pinned ON memos(pinned DESC);
  `);
}

function listMemos({ page = 1, pageSize = 20, search, tag } = {}) {
  const db = getDb();
  const offset = (page - 1) * pageSize;
  let where = [];
  let params = [];

  if (search) {
    where.push('(title LIKE ? OR content LIKE ?)');
    params.push(`%${search}%`, `%${search}%`);
  }
  if (tag) {
    where.push("tags LIKE ?");
    params.push(`%"${tag}"%`);
  }

  const whereClause = where.length > 0 ? 'WHERE ' + where.join(' AND ') : '';

  const countRow = db.prepare(`SELECT COUNT(*) as total FROM memos ${whereClause}`).get(...params);
  const rows = db.prepare(`SELECT * FROM memos ${whereClause} ORDER BY pinned DESC, created_at DESC LIMIT ? OFFSET ?`).all(...params, pageSize, offset);

  return {
    memos: rows.map(r => ({ ...r, tags: JSON.parse(r.tags) })),
    total: countRow.total,
    page,
    pageSize,
    totalPages: Math.ceil(countRow.total / pageSize)
  };
}

function getMemo(id) {
  const db = getDb();
  const row = db.prepare('SELECT * FROM memos WHERE id = ?').get(id);
  if (!row) return null;
  return { ...row, tags: JSON.parse(row.tags) };
}

function createMemo({ title, content, tags }) {
  const db = getDb();
  const tagsStr = JSON.stringify(tags || []);
  const result = db.prepare(
    'INSERT INTO memos (title, content, tags) VALUES (?, ?, ?)'
  ).run(title || '', content || '', tagsStr);
  return getMemo(result.lastInsertRowid);
}

function updateMemo(id, { title, content, tags, pinned }) {
  const db = getDb();
  const existing = getMemo(id);
  if (!existing) return null;

  const newTitle = title !== undefined ? title : existing.title;
  const newContent = content !== undefined ? content : existing.content;
  const newTags = tags !== undefined ? JSON.stringify(tags) : JSON.stringify(existing.tags);
  const newPinned = pinned !== undefined ? (pinned ? 1 : 0) : existing.pinned;

  db.prepare(`
    UPDATE memos SET title = ?, content = ?, tags = ?, pinned = ?, updated_at = datetime('now', '+8 hours')
    WHERE id = ?
  `).run(newTitle, newContent, newTags, newPinned, id);

  return getMemo(id);
}

function deleteMemo(id) {
  const db = getDb();
  const existing = getMemo(id);
  if (!existing) return false;
  db.prepare('DELETE FROM memos WHERE id = ?').run(id);
  return true;
}

function close() {
  if (db) {
    db.close();
    db = null;
  }
}

module.exports = { getDb, listMemos, getMemo, createMemo, updateMemo, deleteMemo, close };
