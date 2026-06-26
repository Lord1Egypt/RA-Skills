#!/usr/bin/env node
/**
 * memory-index.js — Scan memory/*.md + MEMORY.md, chunk and build FTS5 index
 * Usage: node memory-index.js [--workspace /path] [--force]
 * Deps: better-sqlite3 (npm install -g better-sqlite3)
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const GLOBAL_MODULES = require('child_process').execSync('npm root -g', { encoding: 'utf8' }).trim();
const Database = require(path.join(GLOBAL_MODULES, 'better-sqlite3'));

const DEFAULT_WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw/workspace');
const CHUNK_MAX_CHARS = 300;  // v2.0.2: smaller chunks for better CJK precision
const CHUNK_OVERLAP_CHARS = 60;

const args = process.argv.slice(2);
let workspace = DEFAULT_WORKSPACE, force = false;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--workspace' && args[i + 1]) workspace = args[++i];
  if (args[i] === '--force') force = true;
}

const DB_PATH = path.join(workspace, '.memory', 'index.sqlite');
const MEMORY_DIR = path.join(workspace, 'memory');
const MEMORY_MD = path.join(workspace, 'MEMORY.md');

function ensureDir(dir) { if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true }); }
function fileHash(content) { return crypto.createHash('sha256').update(content).digest('hex').slice(0, 16); }

function chunkMarkdown(content, filePath) {
  const lines = content.split('\n'), chunks = [];
  let current = [], currentLen = 0, startLine = 1, heading = '';
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i], lineNum = i + 1;
    if (/^#{1,4}\s/.test(line)) {
      if (current.length > 0 && currentLen > 20)
        chunks.push({ text: current.join('\n').trim(), file: filePath, lineStart: startLine, lineEnd: lineNum - 1, heading });
      heading = line.replace(/^#+\s*/, '').trim();
      current = [line]; currentLen = line.length; startLine = lineNum; continue;
    }
    current.push(line); currentLen += line.length;
    if (currentLen >= CHUNK_MAX_CHARS) {
      chunks.push({ text: current.join('\n').trim(), file: filePath, lineStart: startLine, lineEnd: lineNum, heading });
      const overlap = []; let oLen = 0;
      for (let j = current.length - 1; j >= 0 && oLen < CHUNK_OVERLAP_CHARS; j--) { overlap.unshift(current[j]); oLen += current[j].length; }
      current = overlap; currentLen = oLen; startLine = lineNum - overlap.length + 1;
    }
  }
  if (current.length > 0 && currentLen > 20)
    chunks.push({ text: current.join('\n').trim(), file: filePath, lineStart: startLine, lineEnd: lines.length, heading });
  return chunks;
}

function extractDate(filePath) { const m = path.basename(filePath).match(/(\d{4}-\d{2}-\d{2})/); return m ? m[1] : null; }

function main() {
  ensureDir(path.dirname(DB_PATH));

  // Auto-recover from corrupted database
  if (fs.existsSync(DB_PATH)) {
    try {
      const testDb = new Database(DB_PATH, { readonly: true });
      testDb.pragma('integrity_check');
      testDb.close();
    } catch (e) {
      if (e.code === 'SQLITE_NOTADB' || e.code === 'SQLITE_CORRUPT') {
        console.error(`[index] Database corrupted (${e.code}), deleting and rebuilding...`);
        try { fs.unlinkSync(DB_PATH); } catch (_) {}
        try { fs.unlinkSync(DB_PATH + '-wal'); } catch (_) {}
        try { fs.unlinkSync(DB_PATH + '-shm'); } catch (_) {}
      } else throw e;
    }
  }

  const db = new Database(DB_PATH);
  db.pragma('journal_mode = WAL');
  db.exec(`
    CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY, path TEXT UNIQUE NOT NULL, hash TEXT NOT NULL, date TEXT, is_core INTEGER DEFAULT 0, indexed_at TEXT DEFAULT (datetime('now')));
    CREATE TABLE IF NOT EXISTS chunks (id INTEGER PRIMARY KEY, file_id INTEGER NOT NULL, text TEXT NOT NULL, heading TEXT, line_start INTEGER, line_end INTEGER, FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE);
    CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(text, heading, content='chunks', content_rowid='id', tokenize='unicode61');
    CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN INSERT INTO chunks_fts(rowid, text, heading) VALUES (new.id, new.text, new.heading); END;
    CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN INSERT INTO chunks_fts(chunks_fts, rowid, text, heading) VALUES ('delete', old.id, old.text, old.heading); END;
    CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN INSERT INTO chunks_fts(chunks_fts, rowid, text, heading) VALUES ('delete', old.id, old.text, old.heading); INSERT INTO chunks_fts(rowid, text, heading) VALUES (new.id, new.text, new.heading); END;
  `);

  const files = [];
  if (fs.existsSync(MEMORY_MD)) files.push({ path: 'MEMORY.md', fullPath: MEMORY_MD, isCore: true });
  if (fs.existsSync(MEMORY_DIR)) fs.readdirSync(MEMORY_DIR).filter(f => f.endsWith('.md')).sort().forEach(f => files.push({ path: `memory/${f}`, fullPath: path.join(MEMORY_DIR, f), isCore: false }));

  if (!files.length) { console.log(JSON.stringify({ status: 'ok', indexed: 0, skipped: 0, totalFiles: 0, totalChunks: 0 })); db.close(); return; }

  const insertFile = db.prepare('INSERT OR REPLACE INTO files (path, hash, date, is_core) VALUES (?, ?, ?, ?)');
  const deleteChunks = db.prepare('DELETE FROM chunks WHERE file_id = ?');
  const deleteFile = db.prepare('DELETE FROM files WHERE id = ?');
  const getFile = db.prepare('SELECT id, hash FROM files WHERE path = ?');
  const insertChunk = db.prepare('INSERT INTO chunks (file_id, text, heading, line_start, line_end) VALUES (?, ?, ?, ?, ?)');
  let indexed = 0, skipped = 0, cleaned = 0;

  // Clean up orphaned entries (files deleted from disk but still in index)
  const diskPaths = new Set(files.map(f => f.path));
  const dbFiles = db.prepare('SELECT id, path FROM files').all();
  db.transaction(() => {
    for (const dbFile of dbFiles) {
      if (!diskPaths.has(dbFile.path)) {
        deleteChunks.run(dbFile.id);
        deleteFile.run(dbFile.id);
        cleaned++;
      }
    }
  })();

  db.transaction(() => {
    for (const file of files) {
      const content = fs.readFileSync(file.fullPath, 'utf8'), hash = fileHash(content);
      const existing = getFile.get(file.path);
      if (!force && existing && existing.hash === hash) { skipped++; continue; }
      if (existing) deleteChunks.run(existing.id);
      insertFile.run(file.path, hash, extractDate(file.path), file.isCore ? 1 : 0);
      const fileId = getFile.get(file.path).id;
      for (const chunk of chunkMarkdown(content, file.path))
        insertChunk.run(fileId, chunk.text, chunk.heading, chunk.lineStart, chunk.lineEnd);
      indexed++;
    }
  })();

  const totalChunks = db.prepare('SELECT COUNT(*) as cnt FROM chunks').get().cnt;
  const totalFiles = db.prepare('SELECT COUNT(*) as cnt FROM files').get().cnt;
  console.log(JSON.stringify({ status: 'ok', indexed, skipped, cleaned, totalFiles, totalChunks, dbPath: DB_PATH }));
  db.close();
}
main();
