-- ============================================
-- MIGRATION: Add Partitioning to raw_exchanges (v2.5.0)
-- Run this if you have an existing pg-memory database
-- from v2.4.1 or earlier and want partitioning
-- ============================================

-- WARNING: This is a heavy migration. Back up your database first!
-- Suggested: pg_dump -d openclaw_memory -f backup_pre_partitioning.sql

-- Step 1: Create new partitioned table
CREATE TABLE raw_exchanges_new (
    id UUID NOT NULL,
    session_id UUID NOT NULL,
    exchange_number INTEGER NOT NULL,
    
    user_message TEXT NOT NULL,
    user_message_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_metadata JSONB DEFAULT '{}',
    
    assistant_thinking TEXT,
    assistant_response TEXT NOT NULL,
    response_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    context_window_tokens INTEGER,
    model_version VARCHAR(100),
    compaction_imminent BOOLEAN DEFAULT FALSE,
    full_context_snapshot JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Step 2: Create initial partitions
DO $$
DECLARE
    current_month DATE := DATE_TRUNC('month', CURRENT_DATE);
    partition_name TEXT;
    start_date DATE;
    end_date DATE;
    i INTEGER;
BEGIN
    FOR i IN -3..3 LOOP
        start_date := current_month + (i || ' months')::INTERVAL;
        end_date := start_date + INTERVAL '1 month';
        partition_name := 'raw_exchanges_' || TO_CHAR(start_date, 'YYYY_MM');
        
        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS %I PARTITION OF raw_exchanges_new
             FOR VALUES FROM (%L) TO (%L)',
            partition_name, start_date, end_date
        );
    END LOOP;
END $$;

-- Step 3: Copy data (this may take a while if you have lots of exchanges)
INSERT INTO raw_exchanges_new
SELECT * FROM raw_exchanges;

-- Step 4: Create indexes on new table
CREATE INDEX idx_raw_sessions_time ON raw_exchanges_new(session_id, exchange_number);
CREATE INDEX idx_raw_created ON raw_exchanges_new(created_at DESC);
CREATE INDEX idx_raw_user_message ON raw_exchanges_new USING gin(to_tsvector('english', user_message));
CREATE INDEX idx_raw_assistant_response ON raw_exchanges_new USING gin(to_tsvector('english', assistant_response));

-- Step 5: Create auto-partition function
CREATE OR REPLACE FUNCTION create_raw_exchanges_partition()
RETURNS TRIGGER AS $$
DECLARE
    partition_name TEXT;
    start_date DATE;
    end_date DATE;
BEGIN
    start_date := DATE_TRUNC('month', NEW.created_at);
    end_date := start_date + INTERVAL '1 month';
    partition_name := 'raw_exchanges_' || TO_CHAR(start_date, 'YYYY_MM');
    
    IF NOT EXISTS (
        SELECT 1 FROM pg_tables 
        WHERE tablename = partition_name AND schemaname = 'public'
    ) THEN
        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS %I PARTITION OF raw_exchanges_new
             FOR VALUES FROM (%L) TO (%L)',
            partition_name, start_date, end_date
        );
        
        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS %I PARTITION OF raw_exchanges_new
             FOR VALUES FROM (%L) TO (%L)',
            'raw_exchanges_' || TO_CHAR(end_date, 'YYYY_MM'),
            end_date, end_date + INTERVAL '1 month'
        );
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER auto_create_raw_exchanges_partition
    BEFORE INSERT ON raw_exchanges_new
    FOR EACH ROW EXECUTE FUNCTION create_raw_exchanges_partition();

-- Step 6: Update tool_executions foreign key reference
-- Note: PostgreSQL partitioned tables don't support FK references well
-- We need to remove the FK constraint and use application-level enforcement
ALTER TABLE tool_executions 
DROP CONSTRAINT IF EXISTS tool_executions_exchange_id_fkey;

-- Step 7: Swap tables (use a transaction to minimize downtime)
BEGIN;
    ALTER TABLE raw_exchanges RENAME TO raw_exchanges_old;
    ALTER TABLE raw_exchanges_new RENAME TO raw_exchanges;
    -- Recreate indexes on renamed table
    ALTER INDEX idx_raw_sessions_time RENAME TO idx_raw_sessions_time_old;
    ALTER INDEX idx_raw_created RENAME TO idx_raw_created_old;
COMMIT;

-- Step 8: Verify
SELECT 
    schemaname, 
    tablename, 
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE tablename LIKE 'raw_exchanges%'
ORDER BY tablename;

-- Step 9: Drop old table after verification (manual step)
-- DROP TABLE raw_exchanges_old CASCADE;

-- Step 10: Update comments
COMMENT ON TABLE raw_exchanges IS 'Partitioned by month for time-series performance';

SELECT 'raw_exchanges partitioning migration complete' AS status;
