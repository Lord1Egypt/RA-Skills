-- pg-memory v2.4.0 to v2.4.1 Schema Patch
-- Fixes schema mismatch between code and database
-- Run this to add missing columns that v2.4.0 code expects
-- Created: 2026-02-28

-- Check current schema first:
-- \d observations

-- ============================================
-- ADD MISSING COLUMNS TO OBSERVATIONS TABLE
-- ============================================

-- Add 'source' column (who/what created this)
ALTER TABLE observations
ADD COLUMN IF NOT EXISTS source VARCHAR(100) DEFAULT 'manual';

-- Add 'content_type' column (text, decision, error, etc.)
ALTER TABLE observations
ADD COLUMN IF NOT EXISTS content_type VARCHAR(50) DEFAULT 'observation';

-- Add 'timestamp' column (alias for created_at for compatibility)
-- Note: If created_at exists, we can create a view or rename
-- Option 1: Add timestamp as separate column (keeps both)
ALTER TABLE observations
ADD COLUMN IF NOT EXISTS timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Option 2: If you want to migrate created_at to timestamp:
-- UPDATE observations SET timestamp = created_at WHERE timestamp IS NULL;

-- Add 'embedding' column (for vector search)
ALTER TABLE observations
ADD COLUMN IF NOT EXISTS embedding vector(384);
-- Note: Requires pgvector extension: CREATE EXTENSION IF NOT EXISTS vector;

-- Add 'metadata' column (JSON for structured data)
ALTER TABLE observations
ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}';

-- ============================================
-- ADD PROJECT-RELATED COLUMNS
-- ============================================

-- Add 'project_name' column
ALTER TABLE observations
ADD COLUMN IF NOT EXISTS project_name VARCHAR(255);

-- Add 'assigned_by' column (who assigned this observation)
ALTER TABLE observations
ADD COLUMN IF NOT EXISTS assigned_by VARCHAR(100);

-- Add 'next_steps' column (what needs to happen next)
ALTER TABLE observations
ADD COLUMN IF NOT EXISTS next_steps TEXT;

-- Add 'priority' column (urgency level)
ALTER TABLE observations
ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'medium' 
    CHECK (priority IN ('low', 'medium', 'high', 'critical'));

-- Add 'reminder_date' column (when to follow up)
ALTER TABLE observations
ADD COLUMN IF NOT EXISTS reminder_date TIMESTAMP WITH TIME ZONE;

-- ============================================
-- CREATE INDEXES FOR NEW COLUMNS
-- ============================================

-- Index for source filtering
CREATE INDEX IF NOT EXISTS idx_observations_source ON observations(source);

-- Index for content_type filtering
CREATE INDEX IF NOT EXISTS idx_observations_content_type ON observations(content_type);

-- Index for timestamp (if separate from created_at)
CREATE INDEX IF NOT EXISTS idx_observations_timestamp ON observations(timestamp);

-- Index for project_name
CREATE INDEX IF NOT EXISTS idx_observations_project_name ON observations(project_name);

-- Index for priority
CREATE INDEX IF NOT EXISTS idx_observations_priority ON observations(priority);

-- Index for reminder_date
CREATE INDEX IF NOT EXISTS idx_observations_reminder_date ON observations(reminder_date) 
    WHERE reminder_date IS NOT NULL;

-- GIN index for metadata JSONB
CREATE INDEX IF NOT EXISTS idx_observations_metadata ON observations USING gin(metadata);

-- ============================================
-- VERIFY COLUMNS EXIST
-- ============================================

-- Run this to check:
-- \d observations

-- Expected columns after migration:
-- - id (UUID, PRIMARY KEY)
-- - session_id (UUID)
-- - content (TEXT)
-- - tags (TEXT[])
-- - importance_score (DECIMAL)
-- - status (VARCHAR)
-- - created_at (TIMESTAMP)
-- - source (VARCHAR) [NEW]
-- - content_type (VARCHAR) [NEW]
-- - timestamp (TIMESTAMP) [NEW]
-- - embedding (vector) [NEW]
-- - metadata (JSONB) [NEW]
-- - project_name (VARCHAR) [NEW]
-- - assigned_by (VARCHAR) [NEW]
-- - next_steps (TEXT) [NEW]
-- - priority (VARCHAR) [NEW]
-- - reminder_date (TIMESTAMP) [NEW]

-- ============================================
-- RUN THIS MIGRATION
-- ============================================

-- psql -d openclaw_memory -f schema_v2_4_patch.sql

-- Or run directly:
-- psql -d openclaw_memory -c "\i schema_v2_4_patch.sql"
