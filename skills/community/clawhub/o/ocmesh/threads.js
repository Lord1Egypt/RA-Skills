/**
 * threads.js
 * Conversation threading — groups messages by peer into conversations.
 * Each thread is identified by the peer's public key.
 */

const db = require('./db');

db.exec(`
  CREATE TABLE IF NOT EXISTS threads (
    peer_pk     TEXT PRIMARY KEY,
    last_msg    TEXT,
    last_ts     INTEGER,
    unread      INTEGER DEFAULT 0,
    created_at  INTEGER
  );
`);

function touchThread(peerPk, messageContent, ts) {
  const existing = db.prepare('SELECT peer_pk FROM threads WHERE peer_pk = ?').get(peerPk);
  const now = ts || Date.now();

  if (existing) {
    db.prepare(`
      UPDATE threads SET last_msg = ?, last_ts = ?, unread = unread + 1 WHERE peer_pk = ?
    `).run(messageContent.slice(0, 100), now, peerPk);
  } else {
    db.prepare(`
      INSERT INTO threads (peer_pk, last_msg, last_ts, unread, created_at)
      VALUES (?, ?, ?, 1, ?)
    `).run(peerPk, messageContent.slice(0, 100), now, now);
  }
}

function markRead(peerPk) {
  db.prepare('UPDATE threads SET unread = 0 WHERE peer_pk = ?').run(peerPk);
  db.prepare('UPDATE messages SET read = 1 WHERE from_pk = ?').run(peerPk);
}

function getAll() {
  return db.prepare('SELECT * FROM threads ORDER BY last_ts DESC').all();
}

function getThread(peerPk, limit = 50) {
  return db.prepare(`
    SELECT * FROM messages
    WHERE (from_pk = ? OR to_pk = ?)
    ORDER BY received_at DESC
    LIMIT ?
  `).all(peerPk, peerPk, limit).reverse();
}

module.exports = { touchThread, markRead, getAll, getThread };
