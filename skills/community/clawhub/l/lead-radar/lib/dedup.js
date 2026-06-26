const path = require('path');
const os = require('os');
const fs = require('fs');

let db = null;

function getDb() {
  if (db) return db;

  const Database = require('better-sqlite3');
  const dbDir = path.join(os.homedir(), '.lead-radar');

  if (!fs.existsSync(dbDir)) {
    fs.mkdirSync(dbDir, { recursive: true });
  }

  const dbPath = path.join(dbDir, 'seen.db');
  db = new Database(dbPath);

  // Create table if it doesn't exist
  db.exec(`
    CREATE TABLE IF NOT EXISTS seen_posts (
      id TEXT PRIMARY KEY,
      sent_at INTEGER NOT NULL
    )
  `);

  // Create index for cleanup queries
  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_sent_at ON seen_posts(sent_at)
  `);

  return db;
}

/**
 * Filter out posts that have already been sent.
 * Returns only fresh (unseen) posts.
 */
function dedup(posts) {
  const database = getDb();
  const stmt = database.prepare('SELECT id FROM seen_posts WHERE id = ?');

  return posts.filter((post) => {
    const row = stmt.get(post.id);
    return !row; // Keep only posts NOT in the database
  });
}

/**
 * Mark posts as seen so they won't be sent again.
 */
function markSeen(posts) {
  const database = getDb();
  const stmt = database.prepare(
    'INSERT OR IGNORE INTO seen_posts (id, sent_at) VALUES (?, ?)'
  );

  const now = Math.floor(Date.now() / 1000);
  const insertMany = database.transaction((items) => {
    for (const post of items) {
      stmt.run(post.id, now);
    }
  });

  insertMany(posts);
}

/**
 * Auto-purge rows older than 30 days to keep the database small.
 */
function purgeOld() {
  const database = getDb();
  const thirtyDaysAgo = Math.floor(Date.now() / 1000) - 30 * 86400;
  const result = database.prepare('DELETE FROM seen_posts WHERE sent_at < ?').run(thirtyDaysAgo);
  if (result.changes > 0) {
    console.log(`Purged ${result.changes} old dedup entries`);
  }
}

/**
 * Close the database connection (for clean shutdown).
 */
function closeDb() {
  if (db) {
    db.close();
    db = null;
  }
}

module.exports = { dedup, markSeen, purgeOld, closeDb };
