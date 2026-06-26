-- =============================================================================
-- Migration: Multi-Instance Support (v2.6.0 → v2.7.0)
-- =============================================================================
-- Adds instance tracking for shared database deployments
-- Run after upgrading pg_memory.py to v2.7.0
-- =============================================================================

-- Start transaction
BEGIN;

-- =============================================================================
-- Step 1: Add Instance Tracking Columns
-- =============================================================================

-- Add instance_id for unique machine identification
ALTER TABLE observations 
ADD COLUMN IF NOT EXISTS instance_id UUID;

-- Add agent_label for human-readable instance name
ALTER TABLE observations 
ADD COLUMN IF NOT EXISTS agent_label VARCHAR(100);

COMMENT ON COLUMN observations.instance_id IS 'Unique UUID per machine (auto-generated on first run)';
COMMENT ON COLUMN observations.agent_label IS 'Human-readable agent name (e.g., arty, brodie)';

-- =============================================================================
-- Step 2: Create Indexes for Instance Queries
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_observations_instance 
ON observations(instance_id, timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_observations_agent 
ON observations(agent_label, instance_id);

CREATE INDEX IF NOT EXISTS idx_observations_agent_time 
ON observations(agent_label, timestamp DESC);

-- =============================================================================
-- Step 3: Migration Helper - Populate Existing Data
-- =============================================================================

-- Set default values for existing observations
-- Existing data gets NULL instance_id (backward compatible)
-- New captures will have auto-generated UUIDs

-- Optional: Update existing observations if you know their source
-- UPDATE observations 
-- SET agent_label = 'arty', instance_id = 'your-uuid-here'
-- WHERE source = 'manual' AND instance_id IS NULL;

-- =============================================================================
-- Step 4: Add Unique Constraint Prevention (observation_links)
-- =============================================================================

-- Prevent duplicate observation links between same instances
-- This is critical for multi-instance safety

-- Check if constraint exists
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'unique_observation_link'
    ) THEN
        ALTER TABLE observation_links
        ADD CONSTRAINT unique_observation_link 
        UNIQUE (source_observation_id, target_observation_id, link_type);
    END IF;
EXCEPTION
    WHEN duplicate_table THEN
        RAISE NOTICE 'Constraint already exists';
END $$;

-- =============================================================================
-- Step 5: Create Function for Safe Link Creation
-- =============================================================================

CREATE OR REPLACE FUNCTION safe_create_observation_link(
    p_source_id UUID,
    p_target_id UUID,
    p_link_type VARCHAR(50) DEFAULT 'related',
    p_metadata JSONB DEFAULT '{}'
) RETURNS UUID AS $$
DECLARE
    v_link_id UUID;
BEGIN
    -- Use INSERT ON CONFLICT for safe concurrent access
    INSERT INTO observation_links (
        id, source_observation_id, target_observation_id,
        link_type, metadata, created_at
    ) VALUES (
        gen_random_uuid(), p_source_id, p_target_id,
        p_link_type, p_metadata, NOW()
    )
    ON CONFLICT (source_observation_id, target_observation_id, link_type) 
    DO UPDATE SET 
        metadata = EXCLUDED.metadata,
        created_at = NOW()
    RETURNING id INTO v_link_id;
    
    RETURN v_link_id;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- Step 6: Create View for Multi-Instance Queries
-- =============================================================================

CREATE OR REPLACE VIEW instance_stats AS
SELECT 
    agent_label,
    instance_id,
    COUNT(*) as observation_count,
    COUNT(DISTINCT DATE(timestamp)) as active_days,
    MAX(timestamp) as last_capture,
    MIN(timestamp) as first_capture,
    AVG(importance_score) as avg_importance
FROM observations
WHERE instance_id IS NOT NULL
GROUP BY agent_label, instance_id
ORDER BY last_capture DESC;

-- =============================================================================
-- Step 7: Verification
-- =============================================================================

-- Check columns added
SELECT 
    column_name, 
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'observations' 
AND column_name IN ('instance_id', 'agent_label')
ORDER BY ordinal_position;

-- Check indexes created
SELECT 
    indexname, 
    indexdef 
FROM pg_indexes 
WHERE tablename = 'observations' 
AND indexname LIKE 'idx_observations_instance%';

-- Test view
SELECT * FROM instance_stats LIMIT 5;

-- =============================================================================
-- Complete
-- =============================================================================

COMMIT;

SELECT 'v2.7.0 Multi-Instance migration complete' AS status;
