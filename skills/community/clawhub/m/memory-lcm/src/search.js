const { getDb } = require('./db');

function search(query, sessionKey, limit = 10) {
  const db = getDb();
  const terms = query.replace(/'/g, "''").split(/\s+/).filter(t => t.length > 0);
  if (!terms.length) return [];
  
  const conditions = terms.map(t => `content LIKE '%${t}%'`).join(' AND ');
  const safeSession = sessionKey.replace(/'/g, "''");
  const result = db.exec(
    `SELECT id, session_key, timestamp, role, substr(content, 1, 200) as content, tokens FROM messages 
     WHERE session_key = '${safeSession}' AND ${conditions}
     ORDER BY timestamp DESC LIMIT ${parseInt(limit)}`
  );
  if (!result[0]) return [];
  return result[0].values.map(row => ({
    id: row[0], session_key: row[1], timestamp: row[2], role: row[3], content: row[4], tokens: row[5]
  }));
}

function recallTopic(sessionKey, topic, daysBack = 7) {
  const db = getDb();
  const since = new Date();
  since.setDate(since.getDate() - daysBack);
  const sinceStr = since.toISOString();
  const safeSession = sessionKey.replace(/'/g, "''");
  const safeTopic = topic.replace(/'/g, "''");
  
  const result = db.exec(
    `SELECT id, summary, message_count, created_at FROM chunk_summaries
     WHERE session_key = '${safeSession}' AND created_at >= '${sinceStr}' AND summary LIKE '%${safeTopic}%'
     ORDER BY created_at DESC LIMIT 20`
  );
  if (!result[0]) return [];
  return result[0].values.map(row => ({
    id: row[0], summary: row[1], message_count: row[2], created_at: row[3]
  }));
}

module.exports = { search, recallTopic };
