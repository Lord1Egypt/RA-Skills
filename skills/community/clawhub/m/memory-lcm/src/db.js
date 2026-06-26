const initSqlJs = require('sql.js');
const path = require('path');
const fs = require('fs');
const os = require('os');

const DB_PATH = path.join(process.env.HOME || os.homedir(), '.openclaw', 'workspace', 'data', 'tony-lcm.db');

let db = null;
let SQL = null;

async function initSql() {
  if (!SQL) {
    SQL = await initSqlJs();
  }
  return SQL;
}

function getDb() {
  if (!db) throw new Error('DB not initialized. Call initDb() first.');
  return db;
}

async function initDb() {
  const S = await initSql();
  
  // Ensure data directory exists
  const dir = path.dirname(DB_PATH);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  db = new S.Database();
  
  // Load existing DB if it exists
  if (fs.existsSync(DB_PATH)) {
    try {
      const fileBuffer = fs.readFileSync(DB_PATH);
      db = new S.Database(fileBuffer);
    } catch (e) {
      // If corrupt, start fresh
      db = new S.Database();
    }
  }
  
  // Schema
  db.run(`
    CREATE TABLE IF NOT EXISTS messages (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      session_key TEXT NOT NULL,
      timestamp TEXT NOT NULL,
      role TEXT NOT NULL,
      content TEXT NOT NULL,
      tokens INTEGER,
      compacted INTEGER DEFAULT 0
    )
  `);
  
  db.run(`CREATE INDEX IF NOT EXISTS idx_session ON messages(session_key)`);
  db.run(`CREATE INDEX IF NOT EXISTS idx_compacted ON messages(compacted) WHERE compacted = 0`);
  
  db.run(`
    CREATE TABLE IF NOT EXISTS chunk_summaries (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      session_key TEXT NOT NULL,
      summary TEXT NOT NULL,
      message_count INTEGER NOT NULL,
      created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
  `);
  
  db.run(`
    CREATE TABLE IF NOT EXISTS daily_summaries (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      session_key TEXT NOT NULL,
      summary TEXT NOT NULL,
      date TEXT NOT NULL,
      created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
  `);
  
  return db;
}

function saveDb() {
  if (!db) return;
  const data = db.export();
  const buffer = Buffer.from(data);
  fs.writeFileSync(DB_PATH, buffer);
}

function closeDb() {
  if (db) {
    saveDb();
    db.close();
    db = null;
  }
}

module.exports = { initDb, getDb, saveDb, closeDb, DB_PATH };
