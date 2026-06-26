import path from "node:path";
import os from "node:os";
import { mkdtemp } from "node:fs/promises";
import { DatabaseSync } from "node:sqlite";

export async function createLcmFixtureDb() {
  const tempDir = await mkdtemp(path.join(os.tmpdir(), "mindkeeper-lcm-"));
  const dbPath = path.join(tempDir, "lcm.db");
  const db = new DatabaseSync(dbPath);

  db.exec(`
    CREATE TABLE conversations (
      conversation_id INTEGER PRIMARY KEY,
      session_id TEXT NOT NULL,
      session_key TEXT,
      title TEXT,
      bootstrapped_at TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      active INTEGER NOT NULL DEFAULT 1,
      archived_at TEXT
    );

    CREATE TABLE messages (
      message_id INTEGER PRIMARY KEY,
      conversation_id INTEGER NOT NULL,
      seq INTEGER NOT NULL,
      role TEXT NOT NULL,
      content TEXT NOT NULL,
      token_count INTEGER NOT NULL,
      created_at TEXT NOT NULL
    );

    CREATE TABLE summaries (
      summary_id TEXT PRIMARY KEY,
      conversation_id INTEGER NOT NULL,
      kind TEXT NOT NULL,
      depth INTEGER NOT NULL DEFAULT 0,
      content TEXT NOT NULL,
      token_count INTEGER NOT NULL,
      earliest_at TEXT,
      latest_at TEXT,
      descendant_count INTEGER NOT NULL DEFAULT 0,
      descendant_token_count INTEGER NOT NULL DEFAULT 0,
      source_message_token_count INTEGER NOT NULL DEFAULT 0,
      created_at TEXT NOT NULL,
      file_ids TEXT NOT NULL DEFAULT '[]',
      model TEXT NOT NULL DEFAULT 'unknown'
    );
  `);

  const insertConversation = db.prepare(`INSERT INTO conversations (conversation_id, session_id, session_key, created_at, updated_at) VALUES (?, ?, ?, ?, ?)`);
  insertConversation.run(1, "session-1", "agent:main:main", "2026-04-09 09:00:00", "2026-04-09 10:00:00");
  insertConversation.run(2, "session-2", "agent:main:main", "2026-04-09 21:00:00", "2026-04-09 22:00:00");
  insertConversation.run(3, "session-3", "agent:other:chat", "2026-04-09 11:00:00", "2026-04-09 12:00:00");

  const insertMessage = db.prepare(`INSERT INTO messages (message_id, conversation_id, seq, role, content, token_count, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)`);
  insertMessage.run(1, 1, 1, "user", "We decided the final product name is OldProject.", 10, "2026-04-09 09:05:00");
  insertMessage.run(2, 1, 2, "assistant", "Recommendation: old conversation recommendation.", 5, "2026-04-09 09:07:00");
  insertMessage.run(3, 2, 1, "user", "We decided the final product name is Mindkeeper.", 10, "2026-04-09 21:05:00");
  insertMessage.run(4, 2, 2, "tool", "Noisy tool output", 5, "2026-04-09 21:06:00");
  insertMessage.run(5, 2, 3, "assistant", "Recommendation: validate the brief manually before cron.", 12, "2026-04-09 21:07:00");
  insertMessage.run(6, 3, 1, "user", "Different session message.", 4, "2026-04-09 11:05:00");
  insertMessage.run(7, 2, 4, "assistant", "Remaining open loop: improve LCM scoping for the real day brief.", 8, "2026-04-09 21:08:00");

  const insertSummary = db.prepare(`INSERT INTO summaries (summary_id, conversation_id, kind, depth, content, token_count, earliest_at, latest_at, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`);
  insertSummary.run("sum-old", 1, "leaf", 0, "OldProject summary context", 20, "2026-04-09 09:00:00", "2026-04-09 09:07:00", "2026-04-09 09:08:00");
  insertSummary.run("sum-new", 2, "leaf", 0, "Mindkeeper summary context with lossless-claw integration", 20, "2026-04-09 21:00:00", "2026-04-09 21:08:00", "2026-04-09 21:09:00");
  db.close();

  return dbPath;
}
