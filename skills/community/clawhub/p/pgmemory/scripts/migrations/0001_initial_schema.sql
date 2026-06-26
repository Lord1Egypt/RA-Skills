-- pgmemory migration 0001
-- Initial schema — safe for both fresh installs and existing tables

-- UP

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Create memories table (fresh install)
CREATE TABLE IF NOT EXISTS memories (
  id              BIGSERIAL   PRIMARY KEY,
  agent           TEXT        NOT NULL DEFAULT 'default',
  namespace       TEXT        NOT NULL DEFAULT 'default',
  category        TEXT        NOT NULL DEFAULT 'context',
  key             TEXT,
  content         TEXT        NOT NULL,
  embedding       vector(1024),
  importance      INT         NOT NULL DEFAULT 2 CHECK (importance BETWEEN 1 AND 3),
  relevance_score FLOAT       NOT NULL DEFAULT 1.0,
  access_count    INT         NOT NULL DEFAULT 0,
  source          TEXT        DEFAULT 'session',
  tags            TEXT[]      DEFAULT '{}',
  metadata        JSONB       DEFAULT '{}',
  expires_at      TIMESTAMPTZ,
  last_accessed   TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Add any columns that may be missing on existing tables
ALTER TABLE memories ADD COLUMN IF NOT EXISTS namespace       TEXT        NOT NULL DEFAULT 'default';
ALTER TABLE memories ADD COLUMN IF NOT EXISTS relevance_score FLOAT       NOT NULL DEFAULT 1.0;
ALTER TABLE memories ADD COLUMN IF NOT EXISTS access_count    INT         NOT NULL DEFAULT 0;
ALTER TABLE memories ADD COLUMN IF NOT EXISTS tags            TEXT[]      DEFAULT '{}';
ALTER TABLE memories ADD COLUMN IF NOT EXISTS expires_at      TIMESTAMPTZ;
ALTER TABLE memories ADD COLUMN IF NOT EXISTS last_accessed   TIMESTAMPTZ;

-- Ensure unique index on (agent, key) — may already exist under a different name
DO $$ BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_indexes WHERE tablename='memories' AND indexname='idx_memories_agent_key'
  ) THEN
    CREATE UNIQUE INDEX idx_memories_agent_key ON memories (agent, key) WHERE key IS NOT NULL;
  END IF;
END $$;

-- Vector search index
DO $$ BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_indexes WHERE tablename='memories' AND indexname='idx_memories_embedding'
  ) THEN
    CREATE INDEX idx_memories_embedding ON memories USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
  END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_memories_agent_importance ON memories (agent, importance DESC);
CREATE INDEX IF NOT EXISTS idx_memories_category         ON memories (agent, category);
CREATE INDEX IF NOT EXISTS idx_memories_expires_at       ON memories (expires_at) WHERE expires_at IS NOT NULL;

-- Archived memories table
CREATE TABLE IF NOT EXISTS archived_memories (
  id              BIGSERIAL   PRIMARY KEY,
  agent           TEXT        NOT NULL DEFAULT 'default',
  namespace       TEXT        NOT NULL DEFAULT 'default',
  category        TEXT        NOT NULL DEFAULT 'context',
  key             TEXT,
  content         TEXT        NOT NULL,
  embedding       vector(1024),
  importance      INT         NOT NULL DEFAULT 2,
  relevance_score FLOAT       NOT NULL DEFAULT 1.0,
  access_count    INT         NOT NULL DEFAULT 0,
  source          TEXT        DEFAULT 'session',
  tags            TEXT[]      DEFAULT '{}',
  metadata        JSONB       DEFAULT '{}',
  expires_at      TIMESTAMPTZ,
  last_accessed   TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  archived_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  archive_reason  TEXT        NOT NULL DEFAULT 'expired'
);

CREATE INDEX IF NOT EXISTS idx_archived_memories_agent ON archived_memories (agent, archived_at DESC);

-- Session state table
CREATE TABLE IF NOT EXISTS session_state (
  agent        TEXT        PRIMARY KEY,
  current_task TEXT,
  summary      TEXT,
  active_jobs  TEXT[]      DEFAULT '{}',
  blocked_on   TEXT[]      DEFAULT '{}',
  metadata     JSONB       DEFAULT '{}',
  last_updated TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Updated_at trigger (create or replace)
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS memories_updated_at ON memories;
CREATE TRIGGER memories_updated_at
  BEFORE UPDATE ON memories
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- DOWN

DROP TRIGGER IF EXISTS memories_updated_at ON memories;
DROP FUNCTION IF EXISTS update_updated_at();
DROP TABLE IF EXISTS session_state;
DROP TABLE IF EXISTS archived_memories;
DROP TABLE IF EXISTS memories;
