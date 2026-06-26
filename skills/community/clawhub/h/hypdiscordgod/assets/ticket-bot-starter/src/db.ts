import Database from 'better-sqlite3';

export const db = new Database('tickets.db');

db.exec(`
CREATE TABLE IF NOT EXISTS tickets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  guild_id TEXT NOT NULL,
  channel_id TEXT NOT NULL UNIQUE,
  creator_user_id TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open',
  claimed_by_user_id TEXT,
  created_at TEXT NOT NULL,
  closed_at TEXT
);
`);
