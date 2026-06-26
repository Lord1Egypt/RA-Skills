import { db } from './db.js';

db.exec(`
CREATE TABLE IF NOT EXISTS jobs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'queued',
  attempts INTEGER NOT NULL DEFAULT 0,
  last_error TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
`);

export function enqueueJob(type: string, payload: unknown) {
  const now = new Date().toISOString();
  const result = db.prepare('INSERT INTO jobs (type, payload_json, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)')
    .run(type, JSON.stringify(payload), 'queued', now, now);
  return result.lastInsertRowid;
}

export function getNextQueuedJob() {
  return db.prepare('SELECT * FROM jobs WHERE status = ? ORDER BY id ASC LIMIT 1').get('queued') as any;
}

export function markJobRunning(id: number) {
  db.prepare('UPDATE jobs SET status = ?, attempts = attempts + 1, updated_at = ? WHERE id = ?').run('running', new Date().toISOString(), id);
}

export function markJobDone(id: number) {
  db.prepare('UPDATE jobs SET status = ?, updated_at = ? WHERE id = ?').run('done', new Date().toISOString(), id);
}

export function markJobFailed(id: number, error: string) {
  db.prepare('UPDATE jobs SET status = ?, last_error = ?, updated_at = ? WHERE id = ?').run('failed', error, new Date().toISOString(), id);
}
