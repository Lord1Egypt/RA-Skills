-- ============================================
-- MIGRATION: Profile Abstraction + Auto-Forgetting
-- 
-- Adds memory type classification, strength scoring,
-- and temporal expiration for Supermemory parity.
-- 
-- Run: sqlite3 muninn.db < migrations/002_profile_forgetting.sql
-- ============================================

-- ============================================
-- 1. FACTS: Add memory type and strength
-- ============================================

-- Memory type: 'fact' (persists), 'preference' (strengthens), 'episode' (decays)
ALTER TABLE facts ADD COLUMN memory_type TEXT DEFAULT 'fact';

-- Strength: 0-1, increases with repetition for preferences
ALTER TABLE facts ADD COLUMN strength REAL DEFAULT 0.8;

-- Repetition count: how many times this fact has been observed
ALTER TABLE facts ADD COLUMN repetition_count INTEGER DEFAULT 1;

-- Expiration: when this fact should be forgotten (for temporal facts)
ALTER TABLE facts ADD COLUMN expires_at TEXT;

-- Index for auto-forgetting queries
CREATE INDEX IF NOT EXISTS idx_facts_expires ON facts(expires_at) WHERE expires_at IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_facts_memory_type ON facts(memory_type);
CREATE INDEX IF NOT EXISTS idx_facts_strength ON facts(strength);

-- ============================================
-- 2. ENTITIES: Add profile classification
-- ============================================

-- Entity classification for profile building
ALTER TABLE entities ADD COLUMN is_static INTEGER DEFAULT 0;  -- 1 = static fact (preference, skill)
ALTER TABLE entities ADD COLUMN last_accessed TEXT;

-- Index for profile queries
CREATE INDEX IF NOT EXISTS idx_entities_static ON entities(is_static);
CREATE INDEX IF NOT EXISTS idx_entities_last_accessed ON entities(last_accessed);

-- ============================================
-- 3. PROFILES: New table for cached profiles
-- ============================================

CREATE TABLE IF NOT EXISTS profiles (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  profile_type TEXT NOT NULL,      -- 'static' or 'dynamic'
  facts TEXT NOT NULL,              -- JSON array of distilled facts
  token_count INTEGER DEFAULT 0,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(user_id, profile_type)
);

CREATE INDEX IF NOT EXISTS idx_profiles_user ON profiles(user_id);

-- ============================================
-- 4. MEMORY_HISTORY: Track fact evolution
-- ============================================

CREATE TABLE IF NOT EXISTS memory_history (
  id TEXT PRIMARY KEY,
  fact_id TEXT REFERENCES facts(id),
  action TEXT NOT NULL,             -- 'created', 'strengthened', 'expired', 'decayed'
  old_strength REAL,
  new_strength REAL,
  occurred_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_history_fact ON memory_history(fact_id);
CREATE INDEX IF NOT EXISTS idx_history_occurred ON memory_history(occurred_at);

-- ============================================
-- 5. TEMPORAL_PATTERNS: Auto-forget detection
-- ============================================

CREATE TABLE IF NOT EXISTS temporal_patterns (
  id TEXT PRIMARY KEY,
  pattern TEXT NOT NULL,            -- Regex pattern
  expiry_rule TEXT NOT NULL,        -- 'tomorrow', 'next_week', etc.
  example TEXT,                     -- Example matching text
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Seed temporal patterns
INSERT OR IGNORE INTO temporal_patterns (id, pattern, expiry_rule, example) VALUES
  ('tp_exam', 'exam (tomorrow|next week|on \\d+)', 'tomorrow', 'I have an exam tomorrow'),
  ('tp_meeting', 'meeting (today|tomorrow|next \\w+)', 'event_date', 'Meeting with Alex at 3pm today'),
  ('tp_deadline', 'deadline (is|on) \\d+', 'event_date', 'The deadline is Friday'),
  ('tp_flight', 'flight (on|at) \\d+', 'event_date', 'My flight is on March 15'),
  ('tp_temporary', '(today|tomorrow|this week|next week)', 'relative', 'I''m in Sydney this week');

-- ============================================
-- VIEWS FOR PROFILE QUERIES
-- ============================================

-- Static facts view (preferences, skills, long-term attributes)
CREATE VIEW IF NOT EXISTS v_static_facts AS
SELECT 
  e.name AS entity_name,
  e.type AS entity_type,
  e.summary,
  f.predicate,
  f.object_value,
  f.strength,
  f.memory_type
FROM entities e
JOIN facts f ON f.subject_entity_id = e.id
WHERE f.invalidated_at IS NULL
  AND f.valid_until IS NULL
  AND f.memory_type IN ('fact', 'preference')
  AND f.strength >= 0.5
ORDER BY f.strength DESC, f.created_at DESC;

-- Dynamic facts view (recent activity, projects, temporary states)
CREATE VIEW IF NOT EXISTS v_dynamic_facts AS
SELECT 
  e.name AS entity_name,
  e.type AS entity_type,
  e.summary,
  f.predicate,
  f.object_value,
  f.created_at,
  f.memory_type,
  datetime(f.created_at) > datetime('now', '-30 days') AS is_recent
FROM entities e
JOIN facts f ON f.subject_entity_id = e.id
WHERE f.invalidated_at IS NULL
  AND f.valid_until IS NULL
  AND datetime(f.created_at) > datetime('now', '-30 days')
ORDER BY f.created_at DESC;

-- ============================================
-- NOTES
-- 
-- Memory Types:
-- - fact: Stable knowledge (persists until updated)
-- - preference: User preferences (strengthens with repetition)
-- - episode: Events and activities (decays over time)
--
-- Strength:
-- - 0.0-0.4: Weak (may be noise)
-- - 0.5-0.7: Moderate (observed a few times)
-- - 0.8-1.0: Strong (well-established)
--
-- Expiration:
-- - NULL: Permanent fact
-- - Date: Should be forgotten after this date
--
-- ============================================