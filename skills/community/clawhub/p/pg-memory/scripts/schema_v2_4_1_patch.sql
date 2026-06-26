-- pg-memory v2.4.0 to v2.4.1 Schema Patch
-- Fixes schema mismatch between code and database
-- Run this to add missing columns that v2.4.0 code expects
-- Created: 2026-02-28

-- ============================================
-- NOTE: Run these commands in order
-- ============================================

-- First, check what exists:
-- \d observations

-- ============================================
-- ADD MISSING COLUMNS TO OBSERVATIONS TABLE
-- ============================================

-- If 'created_at' exists but 'timestamp' doesn't, rename it
-- If both exist, timestamp can be a copy
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name = 'observations' AND column_name = 'created_at') 
       AND NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'observations' AND column_name = 'timestamp') THEN
        -- Rename created_at to timestamp for v2.4.0 compatibility
        ALTER TABLE observations RENAME COLUMN created_at TO timestamp;
        RAISE NOTICE 'Renamed created_at to timestamp';
    ELSIF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                      WHERE table_name = 'observations' AND column_name = 'timestamp') THEN
        -- Neither exists, create timestamp
        ALTER TABLE observations ADD COLUMN timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW();
        RAISE NOTICE 'Added timestamp column';
    END IF;
END $$;

-- Add 'source' column
ALTER TABLE observations
ADD COLUMN IF NOT EXISTS source VARCHAR(100) DEFAULT 'manual';

-- Add 'content_type' column  
ALTER TABLE observations
ADD COLUMN IF NOT EXISTS content_type VARCHAR(50) DEFAULT 'observation';

-- Add 'embedding' column (requires pgvector)
-- First check if pgvector is available
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') THEN
        CREATE EXTENSION IF NOT EXISTS vector;
        RAISE NOTICE 'Created pgvector extension';
    END IF;
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'pgvector extension not available, skipping embedding column';
END $$;

-- Only add embedding if pgvector is available
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') THEN
        ALTER TABLE observations ADD COLUMN IF NOT EXISTS embedding vector(384);
        RAISE NOTICE 'Added embedding column';
    END IF;
END $$;

-- Add 'metadata' column (JSONB)
ALTER TABLE observations
ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}';

-- ============================================
-- ADD PROJECT-RELATED COLUMNS
-- ============================================

ALTER TABLE observations
ADD COLUMN IF NOT EXISTS project_name VARCHAR(255);

ALTER TABLE observations
ADD COLUMN IF NOT EXISTS assigned_by VARCHAR(100);

ALTER TABLE observations
ADD COLUMN IF NOT EXISTS next_steps TEXT;

ALTER TABLE observations
ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'medium';
-- Note: Check constraint added separately below

ALTER TABLE observations
ADD COLUMN IF NOT EXISTS reminder_date TIMESTAMP WITH TIME ZONE;

-- ============================================
-- ADD CONSTRAINTS (safely)
-- ============================================

-- Add priority check constraint if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.constraint_column_usage 
        WHERE constraint_name = 'chk_observations_priority'
    ) THEN
        ALTER TABLE observations 
        ADD CONSTRAINT chk_observations_priority 
        CHECK (priority IN ('low', 'medium', 'high', 'critical'));
    END IF;
EXCEPTION WHEN duplicate_object THEN
    RAISE NOTICE 'Priority constraint already exists';
END $$;

-- ============================================
-- CREATE INDEXES
-- ============================================

CREATE INDEX IF NOT EXISTS idx_observations_source ON observations(source);
CREATE INDEX IF NOT EXISTS idx_observations_content_type ON observations(content_type);
CREATE INDEX IF NOT EXISTS idx_observations_timestamp ON observations(timestamp);
CREATE INDEX IF NOT EXISTS idx_observations_project_name ON observations(project_name);
CREATE INDEX IF NOT EXISTS idx_observations_priority ON observations(priority);
CREATE INDEX IF NOT EXISTS idx_observations_reminder_date ON observations(reminder_date) WHERE reminder_date IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_observations_metadata ON observations USING gin(metadata);

-- Only create if embedding column exists
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name = 'observations' AND column_name = 'embedding') THEN
        CREATE INDEX IF NOT EXISTS idx_observations_embedding ON observations USING ivfflat(embedding vector_cosine_ops);
    END IF;
END $$;

-- ============================================
-- VERIFY
-- ============================================

-- Uncomment to verify:
-- SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'observations' ORDER BY ordinal_position;

-- ============================================
-- FIX DATA (if renamed)
-- ============================================

-- If we renamed created_at to timestamp, populate any NULL timestamps
UPDATE observations SET timestamp = NOW() WHERE timestamp IS NULL;

-- Set default values for new columns
UPDATE observations SET source = 'manual' WHERE source IS NULL;
UPDATE observations SET content_type = 'observation' WHERE content_type IS NULL;
UPDATE observations SET metadata = '{}' WHERE metadata IS NULL;
UPDATE observations SET priority = 'medium' WHERE priority IS NULL;

-- Add comments for documentation
COMMENT ON COLUMN observations.source IS 'Who/what created this (e.g., arty, user, system)';
COMMENT ON COLUMN observations.content_type IS 'Type of content (text, decision, error, etc)';
COMMENT ON COLUMN observations.timestamp IS 'When created (v2.4.0 compatibility)';
COMMENT ON COLUMN observations.metadata IS 'Additional structured data (JSONB)';
COMMENT ON COLUMN observations.project_name IS 'Associated project';
COMMENT ON COLUMN observations.priority IS 'Urgency level (low, medium, high, critical)';

-- ============================================
-- DONE
-- ============================================
-- Run with: psql -d openclaw_memory -f schema_v2_4_1_patch.sql
