-- PostgreSQL Agent Memory Schema v2.0
-- For Option A: PostgreSQL as primary, Markdown as short-term backup
-- Created: 2026-02-25

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy text search

-- ============================================
-- 1. SESSIONS
-- Tracks each conversation session
-- ============================================
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_key VARCHAR(255) UNIQUE NOT NULL,
    agent_id VARCHAR(100) NOT NULL DEFAULT 'arty',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    provider VARCHAR(50),
    channel_id VARCHAR(100),
    user_id VARCHAR(100),
    user_label VARCHAR(255),
    group_name VARCHAR(255),
    summary TEXT,
    metadata JSONB DEFAULT '{}',
    context_compacted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_sessions_agent_time ON sessions(agent_id, started_at DESC);
CREATE INDEX idx_sessions_key ON sessions(session_key);
CREATE INDEX idx_sessions_provider ON sessions(provider, started_at DESC);

-- ============================================
-- 2. RAW_EXCHANGES  
-- Every user message and my response (the "full context")
-- ============================================
CREATE TABLE raw_exchanges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    exchange_number INTEGER NOT NULL,
    
    -- User message
    user_message TEXT NOT NULL,
    user_message_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_metadata JSONB DEFAULT '{}',
    
    -- My response
    assistant_thinking TEXT,
    assistant_response TEXT NOT NULL,
    response_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- System / technical
    context_window_tokens INTEGER,
    model_version VARCHAR(100),
    compaction_imminent BOOLEAN DEFAULT FALSE,
    
    -- Full message envelope (JSON backup of complete context)
    full_context_snapshot JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(session_id, exchange_number)
);

CREATE INDEX idx_raw_sessions_time ON raw_exchanges(session_id, exchange_number);
CREATE INDEX idx_raw_created ON raw_exchanges(created_at DESC);
CREATE INDEX idx_raw_user_message ON raw_exchanges USING gin(to_tsvector('english', user_message));
CREATE INDEX idx_raw_assistant_response ON raw_exchanges USING gin(to_tsvector('english', assistant_response));

-- ============================================
-- 3. TOOL_EXECUTIONS
-- Every tool I call with parameters and results
-- ============================================
CREATE TABLE tool_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exchange_id UUID REFERENCES raw_exchanges(id) ON DELETE CASCADE,
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    
    tool_name VARCHAR(100) NOT NULL,
    tool_params JSONB NOT NULL,
    tool_result JSONB,
    execution_status VARCHAR(20) NOT NULL DEFAULT 'pending',  -- pending, success, error, timeout
    error_message TEXT,
    
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_tool_executions_name ON tool_executions(tool_name, created_at DESC);
CREATE INDEX idx_tool_executions_session ON tool_executions(session_id, created_at DESC);
CREATE INDEX idx_tool_executions_status ON tool_executions(execution_status, created_at DESC);

-- ============================================
-- 4. OBSERVATIONS (Curated summaries)
-- The important takeaways, like current memory/*.md content
-- ============================================
CREATE TABLE observations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    
    obs_type VARCHAR(50) NOT NULL,  -- decision, file_created, error, config, milestone, note, ongoing
    title VARCHAR(255),
    content TEXT NOT NULL,
    
    -- Curation
    importance_score DECIMAL(3,2) CHECK (importance_score >= 0 AND importance_score <= 1) DEFAULT 0.5,
    tags TEXT[] DEFAULT '{}',
    related_files TEXT[] DEFAULT '{}',
    related_urls TEXT[] DEFAULT '{}',
    
    -- Source tracking
    derived_from_raw BOOLEAN DEFAULT FALSE,
    derived_from_exchange_ids UUID[],
    
    -- User request
    user_requested BOOLEAN DEFAULT FALSE,  -- Did user say "remember this"
    
    -- Temporal tracking (Option 2: Multi-day observations)
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'ongoing', 'resolved', 'superseded')),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Full-text search on content
CREATE INDEX idx_observations_fts ON observations USING gin(to_tsvector('english', content));
CREATE INDEX idx_observations_type ON observations(obs_type, created_at DESC);
CREATE INDEX idx_observations_tags ON observations USING gin(tags);
CREATE INDEX idx_observations_importance ON observations(importance_score DESC, created_at DESC);
CREATE INDEX idx_observations_created ON observations(created_at DESC);

-- Temporal indexes
CREATE INDEX idx_observations_status ON observations(status, started_at DESC) WHERE status IN ('active', 'ongoing');
CREATE INDEX idx_observations_temporal ON observations(started_at, resolved_at) WHERE resolved_at IS NOT NULL;

-- ============================================
-- 5. MEMORY_IMPORTS
-- Track migration from markdown files
-- ============================================
CREATE TABLE memory_imports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    import_batch_id UUID DEFAULT gen_random_uuid(),
    
    source_file VARCHAR(500) NOT NULL,
    source_type VARCHAR(50) NOT NULL,  -- curated_summary, session_state, memory_md, working_buffer
    source_date DATE,
    
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    
    import_status VARCHAR(20) NOT NULL DEFAULT 'pending',
    error_message TEXT,
    
    imported_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    verified_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_memory_imports_batch ON memory_imports(import_batch_id);
CREATE INDEX idx_memory_imports_status ON memory_imports(import_status);
CREATE INDEX idx_memory_imports_file ON memory_imports(source_file);

-- ============================================
-- 6. CONFIG_VERSIONS
-- Settings and configuration changes over time
-- ============================================
CREATE TABLE config_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    config_key VARCHAR(255) NOT NULL,
    config_value JSONB NOT NULL,
    config_category VARCHAR(50) DEFAULT 'general',
    
    changed_by VARCHAR(100) NOT NULL,
    change_reason TEXT,
    
    valid_from TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    valid_until TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT valid_range CHECK (valid_until IS NULL OR valid_until > valid_from)
);

CREATE INDEX idx_config_versions_key ON config_versions(config_key, valid_from DESC);
CREATE INDEX idx_config_versions_current ON config_versions(valid_until) WHERE valid_until IS NULL;

-- ============================================
-- 7. MEMORY_RETENTION_LOG
-- Track what was pruned/archived
-- ============================================
CREATE TABLE memory_retention_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    retention_type VARCHAR(50) NOT NULL,  -- markdown_file, raw_exchange, observation
    item_identifier VARCHAR(500) NOT NULL,  -- filename or record ID
    item_summary TEXT,
    
    retention_days INTEGER NOT NULL,
    archived_to VARCHAR(500),  -- Path if archived
    deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_retention_log_type ON memory_retention_log(retention_type, deleted_at DESC);

-- ============================================
-- VIEWS FOR COMMON QUERIES
-- ============================================

-- Daily summary view
CREATE VIEW daily_summary AS
SELECT 
    DATE_TRUNC('day', created_at) as day,
    COUNT(*) as observation_count,
    COUNT(*) FILTER (WHERE importance_score > 0.8) as high_importance_count,
    array_agg(DISTINCT obs_type) as types,
    array_agg(title) FILTER (WHERE importance_score > 0.8) as important_titles
FROM observations
GROUP BY DATE_TRUNC('day', created_at)
ORDER BY day DESC;

-- Session summary with metrics
CREATE VIEW session_summary AS
SELECT 
    s.id as session_id,
    s.session_key,
    s.agent_id,
    s.started_at,
    s.ended_at,
    s.provider,
    s.summary,
    COUNT(DISTINCT re.id) as exchange_count,
    COUNT(DISTINCT te.id) as tool_call_count,
    array_agg(DISTINCT te.tool_name) FILTER (WHERE te.tool_name IS NOT NULL) as tools_used
FROM sessions s
LEFT JOIN raw_exchanges re ON s.id = re.session_id
LEFT JOIN tool_executions te ON s.id = te.session_id
GROUP BY s.id, s.session_key, s.agent_id, s.started_at, s.ended_at, s.provider, s.summary
ORDER BY s.started_at DESC;

-- Recent activity view
CREATE VIEW recent_activity AS
SELECT 
    'session' as activity_type,
    id,
    started_at as activity_time,
    summary as description,
    metadata
FROM sessions
WHERE started_at > NOW() - INTERVAL '24 hours'

UNION ALL

SELECT 
    'observation' as activity_type,
    id,
    created_at as activity_time,
    title as description,
    jsonb_build_object('importance', importance_score, 'type', obs_type) as metadata
FROM observations
WHERE created_at > NOW() - INTERVAL '24 hours'

ORDER BY activity_time DESC;

-- ============================================
-- FUNCTIONS
-- ============================================

-- Search observations with ranking
CREATE OR REPLACE FUNCTION search_observations(
    query_text TEXT,
    p_agent_id VARCHAR DEFAULT 'arty',
    p_days INTEGER DEFAULT 30,
    p_min_importance DECIMAL DEFAULT 0.0
)
RETURNS TABLE(
    id UUID,
    obs_type VARCHAR,
    title VARCHAR,
    content TEXT,
    importance_score DECIMAL,
    rank REAL,
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        o.id,
        o.obs_type,
        o.title,
        o.content,
        o.importance_score,
        ts_rank(to_tsvector('english', o.content), plainto_tsquery('english', query_text)) as rank,
        o.created_at
    FROM observations o
    WHERE o.created_at > NOW() - INTERVAL '1 day' * p_days
    AND o.importance_score >= p_min_importance
    AND (
        to_tsvector('english', o.content) @@ plainto_tsquery('english', query_text)
        OR o.tags && ARRAY[query_text]
    )
    ORDER BY o.importance_score DESC, rank DESC
    LIMIT 50;
END;
$$ LANGUAGE plpgsql;

-- Search raw exchanges
CREATE OR REPLACE FUNCTION search_exchanges(
    query_text TEXT,
    p_agent_id VARCHAR DEFAULT 'arty',
    p_days INTEGER DEFAULT 7
)
RETURNS TABLE(
    id UUID,
    session_id UUID,
    exchange_number INTEGER,
    user_message TEXT,
    assistant_response TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    rank REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        re.id,
        re.session_id,
        re.exchange_number,
        re.user_message,
        re.assistant_response,
        re.created_at,
        GREATEST(
            ts_rank(to_tsvector('english', re.user_message), plainto_tsquery('english', query_text)),
            ts_rank(to_tsvector('english', re.assistant_response), plainto_tsquery('english', query_text))
        ) as rank
    FROM raw_exchanges re
    JOIN sessions s ON re.session_id = s.id
    WHERE re.created_at > NOW() - INTERVAL '1 day' * p_days
    AND s.agent_id = p_agent_id
    AND (
        to_tsvector('english', re.user_message) @@ plainto_tsquery('english', query_text)
        OR to_tsvector('english', re.assistant_response) @@ plainto_tsquery('english', query_text)
    )
    ORDER BY rank DESC
    LIMIT 50;
END;
$$ LANGUAGE plpgsql;

-- Get current config value
CREATE OR REPLACE FUNCTION get_config(p_key VARCHAR)
RETURNS JSONB AS $$
BEGIN
    RETURN (
        SELECT config_value
        FROM config_versions
        WHERE config_key = p_key
        AND valid_until IS NULL
        ORDER BY valid_from DESC
        LIMIT 1
    );
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- INITIAL CONFIGURATION
-- ============================================

INSERT INTO config_versions (config_key, config_value, config_category, changed_by, change_reason, valid_from)
VALUES 
    ('memory.retention_days', '"7"', 'memory', 'system', 'Initial setup: 7 days of markdown backup', NOW()),
    ('memory.markdown_backup', 'true', 'memory', 'system', 'Enable markdown backup during transition', NOW()),
    ('memory.primary_backend', '"postgresql"', 'memory', 'system', 'Primary storage is PostgreSQL', NOW()),
    ('agent.default_importance', '0.5', 'memory', 'system', 'Default importance score for observations', NOW())
ON CONFLICT DO NOTHING;

-- ============================================
-- COMPLETION
-- ============================================

SELECT 'Agent Memory Schema v2.0 initialized successfully' as status;
