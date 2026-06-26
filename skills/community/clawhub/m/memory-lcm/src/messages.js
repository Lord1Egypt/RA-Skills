const { getDb, saveDb } = require('./db');

function storeMessage(sessionKey, role, content, tokens = null) {
  const db = getDb();
  const timestamp = new Date().toISOString();
  db.run(
    `INSERT INTO messages (session_key, timestamp, role, content, tokens) VALUES (?, ?, ?, ?, ?)`,
    [sessionKey, timestamp, role, content, tokens]
  );
  saveDb();
  const result = db.exec(`SELECT last_insert_rowid() as id`);
  return result[0]?.values[0]?.[0] || 0;
}

function getRecentMessages(sessionKey, limit = 50) {
  const db = getDb();
  const result = db.exec(
    `SELECT id, session_key, timestamp, role, content, tokens, compacted FROM messages 
     WHERE session_key = '${sessionKey.replace(/'/g, "''")}' AND compacted = 0
     ORDER BY timestamp DESC LIMIT ${parseInt(limit)}`
  );
  if (!result[0]) return [];
  return result[0].values.map(row => ({
    id: row[0], session_key: row[1], timestamp: row[2], role: row[3],
    content: row[4], tokens: row[5], compacted: row[6]
  }));
}

function getUncompactedMessages(sessionKey, limit = 100) {
  const db = getDb();
  const result = db.exec(
    `SELECT id, session_key, timestamp, role, content, tokens, compacted FROM messages 
     WHERE session_key = '${sessionKey.replace(/'/g, "''")}' AND compacted = 0
     ORDER BY timestamp ASC LIMIT ${parseInt(limit)}`
  );
  if (!result[0]) return [];
  return result[0].values.map(row => ({
    id: row[0], session_key: row[1], timestamp: row[2], role: row[3],
    content: row[4], tokens: row[5], compacted: row[6]
  }));
}

function markCompacted(ids) {
  if (!ids.length) return;
  const db = getDb();
  const placeholders = ids.map(() => '?').join(',');
  db.run(`UPDATE messages SET compacted = 1 WHERE id IN (${placeholders})`, ids);
  saveDb();
}

function getStats() {
  const db = getDb();
  const total = db.exec(`SELECT COUNT(*) FROM messages`);
  const totalCount = total[0]?.values[0]?.[0] || 0;
  const active = db.exec(`SELECT COUNT(*) FROM messages WHERE compacted = 0`);
  const activeCount = active[0]?.values[0]?.[0] || 0;
  const sessions = db.exec(`SELECT COUNT(DISTINCT session_key) FROM messages`);
  const sessionCount = sessions[0]?.values[0]?.[0] || 0;
  const summaries = db.exec(`SELECT COUNT(*) FROM chunk_summaries`);
  const summaryCount = summaries[0]?.values[0]?.[0] || 0;
  return { total: totalCount, active: activeCount, sessions: sessionCount, summaries: summaryCount };
}

module.exports = { storeMessage, getRecentMessages, getUncompactedMessages, markCompacted, getStats };
