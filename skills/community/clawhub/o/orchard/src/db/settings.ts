import type Database from "better-sqlite3";

export function getSetting<T = unknown>(db: Database.Database, key: string): T | undefined {
  const row = db.prepare(`SELECT value FROM settings WHERE key = ?`).get(key) as { value: string } | undefined;
  return row ? JSON.parse(row.value) as T : undefined;
}

export function getSettingOr<T>(db: Database.Database, key: string, fallback: T): T {
  const value = getSetting<T>(db, key);
  return value === undefined ? fallback : value;
}

export function setSetting(db: Database.Database, key: string, value: unknown): void {
  db.prepare(`INSERT INTO settings (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP`)
    .run(key, JSON.stringify(value));
}

export function getAllSettings(db: Database.Database): Record<string, unknown> {
  const rows = db.prepare(`SELECT key, value FROM settings`).all() as { key: string; value: string }[];
  return Object.fromEntries(rows.map(r => [r.key, JSON.parse(r.value)]));
}
