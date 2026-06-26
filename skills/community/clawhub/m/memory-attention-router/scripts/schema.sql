PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS memories (
  id TEXT PRIMARY KEY,
  memory_type TEXT NOT NULL CHECK (memory_type IN ('episode','summary','reflection','procedure','preference')),
  abstraction_level INTEGER NOT NULL CHECK (abstraction_level BETWEEN 0 AND 3),
  role_scope TEXT NOT NULL CHECK (role_scope IN ('planner','executor','critic','responder','global')),
  session_id TEXT,
  task_id TEXT,
  title TEXT NOT NULL,
  summary TEXT NOT NULL,
  details_json TEXT NOT NULL,
  keywords_json TEXT NOT NULL,
  tags_json TEXT NOT NULL,
  source_refs_json TEXT NOT NULL,
  importance REAL NOT NULL DEFAULT 0.5 CHECK (importance BETWEEN 0.0 AND 1.0),
  confidence REAL NOT NULL DEFAULT 0.5 CHECK (confidence BETWEEN 0.0 AND 1.0),
  success_score REAL NOT NULL DEFAULT 0.5 CHECK (success_score BETWEEN 0.0 AND 1.0),
  recency_ts TEXT NOT NULL,
  valid_from_ts TEXT,
  valid_to_ts TEXT,
  is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1)),
  replaced_by_memory_id TEXT,
  retired_reason TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (replaced_by_memory_id) REFERENCES memories(id)
);

CREATE INDEX IF NOT EXISTS idx_memories_active_type ON memories(is_active, memory_type);
CREATE INDEX IF NOT EXISTS idx_memories_task ON memories(task_id);
CREATE INDEX IF NOT EXISTS idx_memories_session ON memories(session_id);
CREATE INDEX IF NOT EXISTS idx_memories_replaced_by ON memories(replaced_by_memory_id);
CREATE INDEX IF NOT EXISTS idx_memories_updated ON memories(updated_at DESC);

CREATE TABLE IF NOT EXISTS memory_edges (
  id TEXT PRIMARY KEY,
  from_memory_id TEXT NOT NULL,
  to_memory_id TEXT NOT NULL,
  edge_type TEXT NOT NULL CHECK (edge_type IN ('similar','supports','contradicts','extends','derived_from')),
  weight REAL NOT NULL DEFAULT 0.5 CHECK (weight BETWEEN 0.0 AND 1.0),
  created_at TEXT NOT NULL,
  FOREIGN KEY (from_memory_id) REFERENCES memories(id) ON DELETE CASCADE,
  FOREIGN KEY (to_memory_id) REFERENCES memories(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_memory_edges_from ON memory_edges(from_memory_id);
CREATE INDEX IF NOT EXISTS idx_memory_edges_to ON memory_edges(to_memory_id);
CREATE INDEX IF NOT EXISTS idx_memory_edges_type ON memory_edges(edge_type);

CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
  id UNINDEXED,
  title,
  summary,
  keywords,
  tags,
  tokenize='porter unicode61'
);

CREATE TABLE IF NOT EXISTS working_memory_packets (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  task_id TEXT,
  step_role TEXT NOT NULL CHECK (step_role IN ('planner','executor','critic','responder')),
  goal TEXT NOT NULL,
  packet_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_working_packets_session ON working_memory_packets(session_id, created_at DESC);

PRAGMA user_version = 2;
