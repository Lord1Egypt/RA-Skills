-- layered-memory-sys v2.0 Schema
-- SQLite 表结构定义

-- 记忆主表
CREATE TABLE IF NOT EXISTS memories (
  id            TEXT PRIMARY KEY,
  title         TEXT NOT NULL,
  summary       TEXT DEFAULT '',
  content       TEXT DEFAULT '',
  layer         TEXT NOT NULL DEFAULT 'active' CHECK(layer IN ('flash','active','attention','settled')),
  ttl           INTEGER NOT NULL DEFAULT 7,
  type          TEXT NOT NULL DEFAULT 'exploration' CHECK(type IN ('short','recurring','exploration')),
  status        TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','completed','archived')),
  created_at    TEXT NOT NULL,
  last_active   TEXT NOT NULL,
  recall_count  INTEGER DEFAULT 0,
  recall_days   TEXT DEFAULT '[]',
  turns         INTEGER DEFAULT 0,
  remind_at     TEXT,
  auto_detected INTEGER DEFAULT 0,
  source        TEXT DEFAULT '',
  metadata      TEXT DEFAULT '{}',
  embedding_id  INTEGER,
  created_ts    INTEGER,
  last_active_ts INTEGER
);

-- 标签表
CREATE TABLE IF NOT EXISTS memory_tags (
  memory_id  TEXT NOT NULL REFERENCES memories(id) ON DELETE CASCADE,
  tag        TEXT NOT NULL,
  PRIMARY KEY (memory_id, tag)
);
CREATE INDEX IF NOT EXISTS idx_tags_tag ON memory_tags(tag);
CREATE INDEX IF NOT EXISTS idx_tags_memory ON memory_tags(memory_id);

-- 向量表
CREATE TABLE IF NOT EXISTS embeddings (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  memory_id  TEXT NOT NULL REFERENCES memories(id) ON DELETE CASCADE,
  model      TEXT NOT NULL,
  dimensions INTEGER DEFAULT 0,
  vector     BLOB NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_embeddings_memory ON embeddings(memory_id);

-- 梦境日志
CREATE TABLE IF NOT EXISTS dream_logs (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  date       TEXT NOT NULL,
  action     TEXT NOT NULL,
  detail     TEXT DEFAULT '',
  memory_id  TEXT DEFAULT '',
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_dream_logs_date ON dream_logs(date);

-- 操作事件
CREATE TABLE IF NOT EXISTS events (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  event_type TEXT NOT NULL,
  memory_id  TEXT DEFAULT '',
  detail     TEXT DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_time ON events(created_at);

-- 记忆索引
CREATE INDEX IF NOT EXISTS idx_memories_layer ON memories(layer);
CREATE INDEX IF NOT EXISTS idx_memories_status ON memories(status);
CREATE INDEX IF NOT EXISTS idx_memories_last_active ON memories(last_active_ts);
CREATE INDEX IF NOT EXISTS idx_memories_remind ON memories(remind_at);
CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_ts);
