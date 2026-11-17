/**
 * Memoria — Write-Ahead Log (WAL)
 *
 * Persists conversation turns to SQLite IMMEDIATELY when they arrive,
 * before any LLM processing. If the process crashes mid-session,
 * these messages survive and are processed on next boot.
 *
 * Inspired by proactive-agent's "working buffer" + database WAL concept.
 *
 * Table: wal_buffer
 *   - id: auto-increment
 *   - session_id: string (current session identifier)
 *   - role: "user" | "assistant"
 *   - content: message text (truncated to 5000 chars)
 *   - created_at: timestamp ms
 *   - processed: 0 | 1 (whether extraction has consumed this entry)
 */

import type Database from "better-sqlite3";

export interface WALEntry {
  id: number;
  session_id: string;
  role: "user" | "assistant";
  content: string;
  created_at: number;
  processed: number;
}

export class WriteAheadLog {
  private db: Database.Database;

  constructor(db: Database.Database) {
    this.db = db;
    this.ensureTable();
  }

  private ensureTable(): void {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS wal_buffer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL DEFAULT '',
        role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
        content TEXT NOT NULL,
        created_at INTEGER NOT NULL,
        processed INTEGER NOT NULL DEFAULT 0
      );
      CREATE INDEX IF NOT EXISTS idx_wal_unprocessed
        ON wal_buffer(processed, created_at);
    `);
  }

  /**
   * Write a message to the WAL immediately.
   * This is synchronous (SQLite write) — no LLM, no network.
   * Typically < 1ms.
   */
  write(role: "user" | "assistant", content: string, sessionId = ""): void {
    if (!content || content.length < 5) return;
    this.db.prepare(
      "INSERT INTO wal_buffer (session_id, role, content, created_at, processed) VALUES (?, ?, ?, ?, 0)"
    ).run(sessionId, role, content.slice(0, 5000), Date.now());
  }

  /**
   * Get unprocessed entries (oldest first), up to `limit`.
   */
  getUnprocessed(limit = 20): WALEntry[] {
    return this.db.prepare(
      "SELECT * FROM wal_buffer WHERE processed = 0 ORDER BY created_at ASC LIMIT ?"
    ).all(limit) as WALEntry[];
  }

  /**
   * Mark entries as processed after successful extraction.
   */
  markProcessed(ids: number[]): void {
    if (ids.length === 0) return;
    const placeholders = ids.map(() => "?").join(",");
    this.db.prepare(
      `UPDATE wal_buffer SET processed = 1 WHERE id IN (${placeholders})`
    ).run(...ids);
  }

  /**
   * Clean up old processed entries (older than `maxAgeDays`).
   * Called periodically to prevent unbounded growth.
   */
  cleanup(maxAgeDays = 7): number {
    const cutoff = Date.now() - maxAgeDays * 86_400_000;
    const result = this.db.prepare(
      "DELETE FROM wal_buffer WHERE processed = 1 AND created_at < ?"
    ).run(cutoff);
    return result.changes;
  }

  /**
   * Count unprocessed entries.
   */
  unprocessedCount(): number {
    const row = this.db.prepare(
      "SELECT COUNT(*) as cnt FROM wal_buffer WHERE processed = 0"
    ).get() as { cnt: number };
    return row.cnt;
  }

  /**
   * Get a text representation of unprocessed entries for extraction.
   * Format suitable for LLM fact extraction.
   */
  getUnprocessedText(limit = 20): string {
    const entries = this.getUnprocessed(limit);
    if (entries.length === 0) return "";
    return entries
      .map(e => `[${e.role}] ${e.content}`)
      .join("\n\n");
  }
}
