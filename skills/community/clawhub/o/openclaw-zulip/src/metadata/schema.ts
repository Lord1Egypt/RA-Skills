import { DatabaseSync } from "node:sqlite";

export function initDatabase(dbPath: string): DatabaseSync {
  const db = new DatabaseSync(dbPath);

  db.exec(`
		CREATE TABLE IF NOT EXISTS topic_metadata (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			stream_id INTEGER NOT NULL,
			topic_name TEXT NOT NULL,
			status TEXT DEFAULT 'open',
			priority TEXT DEFAULT NULL,
			assignee TEXT DEFAULT NULL,
			labels TEXT DEFAULT '[]',
			due_date TEXT DEFAULT NULL,
			context TEXT DEFAULT NULL,
			created_at TEXT NOT NULL DEFAULT (datetime('now')),
			updated_at TEXT NOT NULL DEFAULT (datetime('now')),
			UNIQUE(stream_id, topic_name)
		);

		CREATE TABLE IF NOT EXISTS topic_rename_log (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			stream_id INTEGER NOT NULL,
			old_name TEXT NOT NULL,
			new_name TEXT NOT NULL,
			renamed_at TEXT NOT NULL DEFAULT (datetime('now'))
		);

		CREATE INDEX IF NOT EXISTS idx_topic_meta_stream ON topic_metadata(stream_id);
		CREATE INDEX IF NOT EXISTS idx_topic_meta_status ON topic_metadata(status);
	`);

  return db;
}
