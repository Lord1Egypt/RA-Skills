const { storeMessage, getRecentMessages, getUncompactedMessages, markCompacted, getStats } = require('./messages');
const { search, recallTopic } = require('./search');
const { extractDecisions, syncToMemory } = require('./memory-sync');
const { initDb, getDb, saveDb } = require('./db');

class MemoryLCM {
  constructor(sessionKey = 'default') {
    this.sessionKey = sessionKey;
  }
  
  async init() {
    await initDb();
    return this;
  }
  
  log(role, content, tokens = null) {
    storeMessage(this.sessionKey, role, content, tokens);
  }
  
  search(query, limit = 10) {
    return search(query, this.sessionKey, limit);
  }
  
  recall(topic, days = 7) {
    return recallTopic(this.sessionKey, topic, days);
  }
  
  compact(options = {}) {
    const { chunkSize = 20, minMessages = 10 } = options;
    
    const messages = getUncompactedMessages(this.sessionKey, chunkSize * 3);
    if (messages.length < minMessages) {
      return { compacted: 0, decisions: 0, summaries: 0 };
    }
    
    const toCompact = messages.slice(0, chunkSize);
    
    // Simple summarization: key content concatenated
    const summary = toCompact
      .filter(m => m.role === 'user' || m.content.length > 80)
      .map(m => `[${m.role}] ${m.content.substring(0, 200)}`)
      .join('\n---\n');
    
    // Store summary
    const db = getDb();
    db.run(
      `INSERT INTO chunk_summaries (session_key, summary, message_count) VALUES (?, ?, ?)`,
      [this.sessionKey, summary, toCompact.length]
    );
    
    // Mark messages as compacted
    markCompacted(toCompact.map(m => m.id));
    
    // Extract and sync decisions
    const decisions = extractDecisions(summary);
    if (decisions.length > 0) {
      const today = new Date().toISOString().split('T')[0];
      syncToMemory(today, decisions);
    }
    
    saveDb();
    return { compacted: toCompact.length, decisions: decisions.length, summaries: 1 };
  }
  
  daily() {
    const db = getDb();
    const safeSession = this.sessionKey.replace(/'/g, "''");
    
    // Get all summaries for today
    const today = new Date().toISOString().split('T')[0];
    const result = db.exec(
      `SELECT summary, message_count, created_at FROM chunk_summaries
       WHERE session_key = '${safeSession}'
       ORDER BY created_at DESC LIMIT 10`
    );
    
    if (!result[0]?.values.length) return { daily: 0 };
    
    const summaries = result[0].values.map(row => row[0]).join('\n\n---\n\n');
    const totalMessages = result[0].values.reduce((sum, row) => sum + (row[1] || 0), 0);
    
    // Store daily summary
    db.run(
      `INSERT INTO daily_summaries (session_key, summary, date) VALUES (?, ?, ?)`,
      [this.sessionKey, summaries, today]
    );
    
    // Extract decisions from all summaries
    const decisions = extractDecisions(summaries);
    if (decisions.length > 0) {
      syncToMemory(today, decisions);
    }
    
    saveDb();
    return { daily: totalMessages, decisions: decisions.length };
  }
  
  status() {
    return getStats();
  }
}

module.exports = { MemoryLCM };
