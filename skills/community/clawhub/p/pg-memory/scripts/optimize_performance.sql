-- pg-memory Performance Optimization Script
-- Run this to improve query speed and reduce storage

-- ============================================================
-- 1. DROP UNUSED INDEXES (saves write speed + storage)
-- ============================================================
-- These indexes have 0 scans according to pg_stat_user_indexes

DROP INDEX IF EXISTS idx_observations_status;
DROP INDEX IF EXISTS idx_observations_high_importance;
DROP INDEX IF EXISTS idx_observations_priority;
DROP INDEX IF EXISTS idx_observations_tags;
DROP INDEX IF EXISTS idx_observations_type;
DROP INDEX IF EXISTS idx_observations_agent;
DROP INDEX IF EXISTS idx_observations_importance;

-- Keep these (they have scans):
-- - observations_pkey (154 scans) - PRIMARY KEY
-- - idx_observations_fts (4 scans) - Full-text search
-- - idx_observations_agent_time (3 scans) - Time-based queries
-- - idx_observations_content_type_importance (1 scan)
-- - idx_observations_project (1 scan)
-- - idx_observations_source_time (1 scan)
-- - idx_observations_timestamp (used for ordering)
-- - idx_observations_instance (multi-instance support)
-- - idx_observations_embedding (semantic search)

-- ============================================================
-- 2. OPTIMIZE IVFFLAT INDEX FOR SMALL DATASETS
-- ============================================================
-- For <1000 rows, use lists=10 (faster, still accurate)
-- For 1000-10000 rows, use lists=100 (default)
-- For >10000 rows, use lists=1000+

-- Drop old index
DROP INDEX IF EXISTS idx_observations_embedding;

-- Recreate with optimized lists parameter (10 for ~76 rows)
-- Formula: lists = rows / 1000 (minimum 10, maximum 4000)
CREATE INDEX idx_observations_embedding 
    ON observations USING ivfflat (embedding vector_cosine_ops) 
    WITH (lists = 10)
    WHERE embedding IS NOT NULL;

-- ============================================================
-- 3. VACUUM AND ANALYZE (update statistics)
-- ============================================================
VACUUM ANALYZE observations;
VACUUM ANALYZE raw_exchanges;
VACUUM ANALYZE summaries;

-- ============================================================
-- 4. OPTIMIZE POSTGRESQL CONFIGURATION (if you have sudo)
-- ============================================================
-- Add to postgresql.conf or run via ALTER SYSTEM:

-- shared_buffers = 256MB              # 25% of RAM (for dedicated DB)
-- effective_cache_size = 1GB          # 50-75% of RAM
-- work_mem = 16MB                     # For sorting/hash operations
-- maintenance_work_mem = 128MB        # For VACUUM, CREATE INDEX
-- checkpoint_completion_target = 0.9  # Spread checkpoint I/O
-- wal_buffers = 16MB                  # WAL write buffer
-- default_statistics_target = 100     # Increase for better query plans

-- For vector search specifically:
-- ivfflat.probes = 5                  # Higher = more accurate, slower (default: 1)

-- ============================================================
-- 5. VERIFY OPTIMIZATION
-- ============================================================
-- Check index sizes after cleanup
SELECT 
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as size
FROM pg_indexes
WHERE tablename = 'observations'
ORDER BY pg_relation_size(indexname::regclass) DESC;

-- Check total size reduction
SELECT 
    pg_size_pretty(pg_total_relation_size('observations')) as total_size,
    pg_size_pretty(pg_relation_size('observations')) as table_size,
    pg_size_pretty(pg_indexes_size('observations')) as index_size;
