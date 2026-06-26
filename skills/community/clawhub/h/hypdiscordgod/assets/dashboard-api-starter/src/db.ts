import Database from 'better-sqlite3';

const dbPath = process.env.DATABASE_PATH || 'bot.db';
export const db = new Database(dbPath);

db.exec(`
CREATE TABLE IF NOT EXISTS guild_settings (
  guild_id TEXT PRIMARY KEY,
  settings_json TEXT NOT NULL DEFAULT '{}',
  updated_at TEXT NOT NULL
);
`);
