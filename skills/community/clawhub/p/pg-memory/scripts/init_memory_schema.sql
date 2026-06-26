-- PostgreSQL Agent Memory Schema v2.4.1 (Complete)
-- Full fresh install with all v2.4.1 features
-- No patches needed - this is the complete schema
-- Created: 2026-02-28

-- ============================================
-- ENABLE REQUIRED EXTENSIONS
-- ============================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy text search
CREATE EXTENSION IF NOT EXISTS "vector";   -- For embeddings (optional but recommended)

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
-- 2. RAW_EXCHANGES (PARTITIONED by month)
-- Every user message and my response (the "full context")
-- Partitioned for performance with high-volume time-series data
-- ============================================
CREATE TABLE raw_exchanges (
    id UUID NOT NULL,
    session_id UUID NOT NULL,
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
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Create index on parent table (will be inherited by partitions)
CREATE INDEX idx_raw_sessions_time ON raw_exchanges(session_id, exchange_number);
CREATE INDEX idx_raw_created ON raw_exchanges(created_at DESC);
CREATE INDEX idx_raw_user_message ON raw_exchanges USING gin(to_tsvector('english', user_message));
CREATE INDEX idx_raw_assistant_response ON raw_exchanges USING gin(to_tsvector('english', assistant_response));

-- Create initial partitions (current month and next 2 months)
-- Future partitions are auto-created by trigger
DO $$
DECLARE
    current_month DATE := DATE_TRUNC('month', CURRENT_DATE);
    partition_name TEXT;
    start_date DATE;
    end_date DATE;
    i INTEGER;
BEGIN
    FOR i IN 0..2 LOOP
        start_date := current_month + (i || ' months')::INTERVAL;
        end_date := start_date + INTERVAL '1 month';
        partition_name := 'raw_exchanges_' || TO_CHAR(start_date, 'YYYY_MM');
        
        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS %I PARTITION OF raw_exchanges
             FOR VALUES FROM (%L) TO (%L)',
            partition_name, start_date, end_date
        );
    END LOOP;
END $$;

-- Function to auto-create partitions
CREATE OR REPLACE FUNCTION create_raw_exchanges_partition()
RETURNS TRIGGER AS $$
DECLARE
    partition_name TEXT;
    start_date DATE;
    end_date DATE;
    current_partition TEXT;
    next_partition TEXT;
BEGIN
    -- Calculate partition boundaries
    start_date := DATE_TRUNC('month', NEW.created_at);
    end_date := start_date + INTERVAL '1 month';
    partition_name := 'raw_exchanges_' || TO_CHAR(start_date, 'YYYY_MM');
    
    -- Create partition if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 FROM pg_tables 
        WHERE tablename = partition_name 
        AND schemaname = 'public'
    ) THEN
        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS %I PARTITION OF raw_exchanges
             FOR VALUES FROM (%L) TO (%L)',
            partition_name, start_date, end_date
        );
        
        -- Also create next month partition to avoid race conditions
        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS %I PARTITION OF raw_exchanges
             FOR VALUES FROM (%L) TO (%L)',
            'raw_exchanges_' || TO_CHAR(end_date, 'YYYY_MM'),
            end_date, end_date + INTERVAL '1 month'
        );
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-create partitions on insert
CREATE TRIGGER auto_create_raw_exchanges_partition
    BEFORE INSERT ON raw_exchanges
    FOR EACH ROW EXECUTE FUNCTION create_raw_exchanges_partition();

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
    execution_status VARCHAR(20) NOT NULL DEFAULT 'pending',
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
-- 4. OBSERVATIONS (v2.4.1 Complete)
-- The important takeaways with full v2.4.1 column set
-- ============================================
CREATE TABLE observations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    
    -- Content
    obs_type VARCHAR(50) NOT NULL DEFAULT 'note',
    title VARCHAR(255),
    content TEXT NOT NULL,
    
    -- NEW v2.4: Source and type tracking
    source VARCHAR(100) DEFAULT 'manual',
    content_type VARCHAR(50) DEFAULT 'observation',
    
    -- Curation
    importance_score DECIMAL(3,2) CHECK (importance_score >= 0 AND importance_score <= 1) DEFAULT 0.5,
    tags TEXT[] DEFAULT '{}',
    related_files TEXT[] DEFAULT '{}',
    related_urls TEXT[] DEFAULT '{}',
    
    -- NEW v2.4: Metadata and embedding
    metadata JSONB DEFAULT '{}',
    embedding VECTOR(1024),  -- Requires pgvector (BGE-M3 via Ollama)
    
    -- Source tracking
    derived_from_raw BOOLEAN DEFAULT FALSE,
    derived_from_exchange_ids UUID[],
    
    -- Related observations (v2.3)
    related_observation_ids UUID[] DEFAULT '{}',
    supersedes_observation_id UUID REFERENCES observations(id) ON DELETE SET NULL,
    
    -- User request
    user_requested BOOLEAN DEFAULT FALSE,
    
    -- NEW v2.4: Project tracking
    project_name VARCHAR(255),
    assigned_by VARCHAR(100),
    next_steps TEXT,
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    reminder_date TIMESTAMP WITH TIME ZONE,
    
    -- Temporal tracking
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'ongoing', 'resolved', 'superseded')),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE,
    
    -- NOTE: Using 'timestamp' for v2.4+ compatibility
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Full-text search
CREATE INDEX idx_observations_fts ON observations USING gin(to_tsvector('english', content));
CREATE INDEX idx_observations_type ON observations(obs_type, timestamp DESC);
CREATE INDEX idx_observations_tags ON observations USING gin(tags);
CREATE INDEX idx_observations_importance ON observations(importance_score DESC, timestamp DESC);
CREATE INDEX idx_observations_timestamp ON observations(timestamp DESC);

-- NEW v2.4 indexes
CREATE INDEX idx_observations_source ON observations(source);
CREATE INDEX idx_observations_content_type ON observations(content_type);
CREATE INDEX idx_observations_metadata ON observations USING gin(metadata);
CREATE INDEX idx_observations_project_name ON observations(project_name);
CREATE INDEX idx_observations_priority ON observations(priority);
CREATE INDEX idx_observations_reminder_date ON observations(reminder_date) WHERE reminder_date IS NOT NULL;
CREATE INDEX idx_observations_related ON observations USING gin(related_observation_ids);
CREATE INDEX idx_observations_supersedes ON observations(supersedes_observation_id) WHERE supersedes_observation_id IS NOT NULL;

-- Temporal indexes
CREATE INDEX idx_observations_status ON observations(status, started_at DESC) WHERE status IN ('active', 'ongoing');
CREATE INDEX idx_observations_temporal ON observations(started_at, resolved_at) WHERE resolved_at IS NOT NULL;

-- Embedding index (only if pgvector available)
CREATE INDEX idx_observations_embedding ON observations USING ivfflat(embedding vector_cosine_ops) WHERE embedding IS NOT NULL;

-- ============================================
-- 5. SUMMARIES (v2.3+)
-- Auto-generated summaries, separate from observations
-- ============================================
CREATE TABLE summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Source tracking
    source_observation_ids UUID[] NOT NULL,
    source_session_ids UUID[],
    source_tags TEXT[],
    
    -- The summary itself
    summary_type VARCHAR(50) NOT NULL DEFAULT 'auto',
    title VARCHAR(255),
    content TEXT NOT NULL,
    
    -- Metadata
    importance_score DECIMAL(3,2) DEFAULT 0.5 CHECK (importance_score >= 0 AND importance_score <= 1),
    generated_by VARCHAR(100) DEFAULT 'system',
    generation_model VARCHAR(100),
    
    -- Temporal
    covers_from TIMESTAMP WITH TIME ZONE,
    covers_until TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Status
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'archived', 'superseded'))
);

CREATE INDEX idx_summaries_source_obs ON summaries USING gin(source_observation_ids);
CREATE INDEX idx_summaries_type ON summaries(summary_type, created_at DESC);
CREATE INDEX idx_summaries_covers ON summaries(covers_from, covers_until);
CREATE INDEX idx_summaries_created ON summaries(created_at DESC);
CREATE INDEX idx_summaries_fts ON summaries USING gin(to_tsvector('english', content));

-- ============================================
-- 6. OBSERVATION CHAINS (v2.3+)
-- Project/workflow tracking
-- ============================================
CREATE TABLE observation_chains (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    chain_name VARCHAR(255) NOT NULL,
    chain_type VARCHAR(50) NOT NULL DEFAULT 'project',
    chain_description TEXT,
    
    root_observation_id UUID REFERENCES observations(id) ON DELETE SET NULL,
    
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'complete', 'abandoned', 'paused')),
    current_step INTEGER DEFAULT 0,
    total_steps INTEGER DEFAULT 0,
    
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    
    tags TEXT[] DEFAULT '{}',
    importance_score DECIMAL(3,2) DEFAULT 0.5,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_chains_type ON observation_chains(chain_type, status);
CREATE INDEX idx_chains_root ON observation_chains(root_observation_id);
CREATE INDEX idx_chains_status ON observation_chains(status, started_at DESC);

-- Chain steps
CREATE TABLE chain_steps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chain_id UUID NOT NULL REFERENCES observation_chains(id) ON DELETE CASCADE,
    observation_id UUID REFERENCES observations(id) ON DELETE SET NULL,
    
    step_number INTEGER NOT NULL,
    step_type VARCHAR(50) NOT NULL DEFAULT 'milestone',
    step_description TEXT,
    
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'complete', 'blocked')),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    
    UNIQUE(chain_id, step_number)
);

CREATE INDEX idx_chain_steps_chain ON chain_steps(chain_id, step_number);
CREATE INDEX idx_chain_steps_observation ON chain_steps(observation_id);

-- ============================================
-- 7. OBSERVATION TEMPLATES (v2.3+)
-- Reusable templates for common observation types
-- ============================================
CREATE TABLE observation_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    template_name VARCHAR(255) NOT NULL,
    template_type VARCHAR(50) NOT NULL,  -- 'bug_report', 'decision', 'project_kickoff', 'milestone', etc
    template_description TEXT,
    
    -- The template content
    content_template TEXT NOT NULL,
    default_tags TEXT[] DEFAULT '{}',
    default_importance DECIMAL(3,2) DEFAULT 0.5,
    
    -- Usage tracking
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    is_system BOOLEAN DEFAULT FALSE,
    
    created_by VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_templates_type ON observation_templates(template_type, is_active);
CREATE INDEX idx_templates_active ON observation_templates(is_active, usage_count DESC);

-- Insert default templates
INSERT INTO observation_templates (template_name, template_type, template_description, content_template, default_tags, default_importance, is_system)
VALUES 
('Bug Report', 'bug_report', 'Standard bug report template', '## Bug Report: {title}

**Severity**: {severity}
**Component**: {component}

### Description
{description}

### Steps to Reproduce
{steps}

### Expected Behavior
{expected}

### Actual Behavior
{actual}

### Environment
- OS: {os}
- Browser/Version: {browser}', ARRAY['bug', 'issue'], 0.7, TRUE),

('Decision Record', 'decision', 'Record a significant decision', '## Decision: {title}

**Date**: {date}
**Decision Maker**: {decision_maker}

### Context
{context}

### Decision
{decision}

### Alternatives Considered
{alternatives}

### Consequences
{consequences}

### Implementation Status
{status}', ARRAY['decision'], 0.8, TRUE),

('Project Kickoff', 'project_kickoff', 'New project initialization', '## Project: {project_name}

**Kickoff Date**: {date}
**Lead**: {lead}

### Goals
{goals}

### Scope
{scope}

### Key Milestones
{milestones}

### Success Criteria
{success_criteria}

### Resources Needed
{resources}', ARRAY['project', 'kickoff'], 0.9, TRUE),

('Milestone', 'milestone', 'Project milestone achievement', '## Milestone: {title}

**Project**: {project_name}
**Date Achieved**: {date}

### What Was Delivered
{delivered}

### Impact
{impact}

### Next Steps
{next_steps}', ARRAY['milestone', 'achievement'], 0.8, TRUE);

-- ============================================
-- 8. FOLLOW-UP REMINDERS (v2.3+)
-- Track stale observations needing attention
-- ============================================
CREATE TABLE follow_up_reminders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    observation_id UUID NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
    
    reminder_type VARCHAR(50) NOT NULL,  -- 'project_stale', 'decision_pending', 'milestone_overdue', 'custom'
    reminder_message TEXT NOT NULL,
    
    -- Scheduling
    remind_at TIMESTAMP WITH TIME ZONE NOT NULL,
    reminder_sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP WITH TIME ZONE,
    
    -- Recurring reminders
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_pattern VARCHAR(50),  -- 'daily', 'weekly', 'monthly'
    
    -- Actions taken
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    acknowledged_by VARCHAR(100),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_reminders_observation ON follow_up_reminders(observation_id, remind_at);
CREATE INDEX idx_reminders_pending ON follow_up_reminders(remind_at, reminder_sent) WHERE NOT reminder_sent;
CREATE INDEX idx_reminders_acknowledged ON follow_up_reminders(acknowledged, remind_at);

-- ============================================
-- 9. OBSERVATION CONFLICTS (v2.3+)
-- Track contradictions between observations
-- ============================================
CREATE TABLE observation_conflicts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    observation_a_id UUID NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
    observation_b_id UUID NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
    
    conflict_type VARCHAR(50) NOT NULL,  -- 'contradiction', 'incomplete', 'outdated', 'duplication'
    conflict_description TEXT NOT NULL,
    
    -- Resolution
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'investigating', 'resolved', 'confirmed_conflict')),
    resolution_notes TEXT,
    resolved_by VARCHAR(100),
    resolved_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(observation_a_id, observation_b_id, conflict_type)
);

CREATE INDEX idx_conflicts_open ON observation_conflicts(status) WHERE status NOT IN ('resolved', 'confirmed_conflict');
CREATE INDEX idx_conflicts_type ON observation_conflicts(conflict_type, status);

-- ============================================
-- 10. PG_MEMORY_SETTINGS (v2.4+)
-- Configuration and user preferences
-- ============================================
CREATE TABLE pg_memory_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    setting_group VARCHAR(50) NOT NULL DEFAULT 'general',
    setting_key VARCHAR(100) NOT NULL,
    setting_value TEXT NOT NULL,
    setting_type VARCHAR(20) DEFAULT 'string' CHECK (setting_type IN ('string', 'int', 'float', 'bool', 'json')),
    
    description TEXT,
    is_user_configurable BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(setting_group, setting_key)
);

CREATE INDEX idx_settings_group ON pg_memory_settings(setting_group, setting_key);

-- Insert default settings
INSERT INTO pg_memory_settings (setting_group, setting_key, setting_value, setting_type, description, is_user_configurable)
VALUES 
('nl_query', 'nl_query_model', 'ollama/mistral:latest', 'string', 'Default model for natural language queries', TRUE),
('nl_query', 'nl_query_max_results', '50', 'int', 'Maximum results for NL queries', TRUE),
('nl_query', 'nl_query_timeout', '30', 'int', 'Timeout for NL queries in seconds', TRUE),
('nl_query', 'nl_query_temperature', '0.1', 'float', 'Temperature for NL query SQL generation', TRUE),
('general', 'max_observations_retention_days', '90', 'int', 'Default retention period', FALSE),
('general', 'auto_summarize_days', '7', 'int', 'Auto-generate summaries every N days', TRUE);

-- ============================================
-- 11. MEMORY_IMPORTS
-- Track migration from markdown files
-- ============================================
CREATE TABLE memory_imports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    import_batch_id UUID DEFAULT gen_random_uuid(),
    
    source_file VARCHAR(500) NOT NULL,
    source_type VARCHAR(50) NOT NULL,
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
-- 12. CONFIG_VERSIONS
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
-- 13. MEMORY_RETENTION_LOG
-- Track what was pruned/archived
-- ============================================
CREATE TABLE memory_retention_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    retention_type VARCHAR(50) NOT NULL,
    item_identifier VARCHAR(500) NOT NULL,
    item_summary TEXT,
    
    retention_days INTEGER NOT NULL,
    archived_to VARCHAR(500),
    deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_retention_log_type ON memory_retention_log(retention_type, deleted_at DESC);

-- ============================================
-- HELPER FUNCTIONS
-- ============================================

-- Function to get current setting
CREATE OR REPLACE FUNCTION get_memory_setting(
    p_group VARCHAR,
    p_key VARCHAR
) RETURNS TEXT AS $$
DECLARE
    v_value TEXT;
BEGIN
    SELECT setting_value INTO v_value
    FROM pg_memory_settings
    WHERE setting_group = p_group AND setting_key = p_key;
    RETURN v_value;
END;
$$ LANGUAGE plpgsql;

-- Function to find related observations
CREATE OR REPLACE FUNCTION find_related_observations(
    p_observation_id UUID,
    p_match_tags BOOLEAN DEFAULT TRUE,
    p_match_session BOOLEAN DEFAULT FALSE
) RETURNS TABLE (
    id UUID,
    title VARCHAR(255),
    content TEXT,
    obs_type VARCHAR(50),
    importance_score DECIMAL(3,2),
    tags TEXT[],
    timestamp TIMESTAMP WITH TIME ZONE,
    related_score INTEGER
) AS $$
BEGIN
    RETURN QUERY
    WITH base_obs AS (
        SELECT o.*, o.tags as base_tags, o.session_id as base_session
        FROM observations o
        WHERE o.id = p_observation_id
    )
    SELECT o.id, o.title, o.content, o.obs_type, o.importance_score, o.tags, o.timestamp,
        CASE 
            WHEN o.id = ANY(bo.related_observation_ids) THEN 100
            WHEN p_match_tags AND o.tags && bo.base_tags THEN 50
            WHEN p_match_session AND o.session_id = bo.base_session THEN 25
            ELSE 0
        END as related_score
    FROM observations o, base_obs bo
    WHERE o.id != p_observation_id
        AND (o.id = ANY(bo.related_observation_ids) 
            OR (p_match_tags AND o.tags && bo.base_tags)
            OR (p_match_session AND o.session_id = bo.base_session))
    ORDER BY related_score DESC, o.importance_score DESC, o.timestamp DESC;
END;
$$ LANGUAGE plpgsql;

-- Function to check for conflicts
CREATE OR REPLACE FUNCTION check_observation_conflicts(
    p_content TEXT,
    p_tags TEXT[],
    p_days_back INTEGER DEFAULT 30
) RETURNS TABLE (
    observation_id UUID,
    similarity DECIMAL,
    content TEXT,
    reason TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        o.id as observation_id,
        similarity(o.content, p_content) as similarity,
        o.content,
        CASE 
            WHEN o.tags && p_tags THEN 'tag_overlap'
            ELSE 'content_similarity'
        END as reason
    FROM observations o
    WHERE o.timestamp > NOW() - INTERVAL '1 day' * p_days_back
        AND (o.tags && p_tags OR similarity(o.content, p_content) > 0.6)
    ORDER BY similarity DESC
    LIMIT 5;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- VIEWS FOR COMMON QUERIES
-- ============================================

-- Daily summary view
CREATE VIEW daily_summary AS
SELECT 
    DATE_TRUNC('day', timestamp) as day,
    COUNT(*) as observation_count,
    COUNT(*) FILTER (WHERE importance_score > 0.8) as high_importance_count,
    array_agg(DISTINCT obs_type) as types,
    array_agg(title) FILTER (WHERE importance_score > 0.8) as important_titles
FROM observations
GROUP BY DATE_TRUNC('day', timestamp)
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
    COUNT(DISTINCT te.id) as tool_calls,
    COUNT(DISTINCT o.id) as observations_created
FROM sessions s
LEFT JOIN raw_exchanges re ON re.session_id = s.id
LEFT JOIN tool_executions te ON te.session_id = s.id
LEFT JOIN observations o ON o.session_id = s.id
GROUP BY s.id;

-- Active observations with chain info
CREATE VIEW active_observations_detailed AS
SELECT 
    o.*,
    oc.chain_name,
    oc.status as chain_status,
    cs.step_number,
    cs.step_type
FROM observations o
LEFT JOIN chain_steps cs ON cs.observation_id = o.id
LEFT JOIN observation_chains oc ON oc.id = cs.chain_id
WHERE o.status IN ('active', 'ongoing')
ORDER BY o.importance_score DESC, o.timestamp DESC;

-- Overdue reminders view
CREATE VIEW overdue_reminders AS
SELECT 
    r.*,
    o.title as observation_title,
    o.content as observation_content
FROM follow_up_reminders r
JOIN observations o ON o.id = r.observation_id
WHERE r.remind_at < NOW()
    AND NOT r.reminder_sent
    AND NOT r.acknowledged
ORDER BY r.remind_at ASC;

-- Open conflicts view
CREATE VIEW open_conflicts AS
SELECT 
    c.*,
    oa.title as observation_a_title,
    ob.title as observation_b_title
FROM observation_conflicts c
JOIN observations oa ON oa.id = c.observation_a_id
JOIN observations ob ON ob.id = c.observation_b_id
WHERE c.status NOT IN ('resolved', 'confirmed_conflict')
ORDER BY c.created_at DESC;

-- ============================================
-- VERSION INFO
-- ============================================

COMMENT ON DATABASE CURRENT_DATABASE IS 'pg-memory v2.4.1 — PostgreSQL Agent Memory System';

-- Verify installation
SELECT 'pg-memory v2.4.1 installed successfully' as status;
SELECT 'Tables created: ' || COUNT(*)::text as tables FROM information_schema.tables WHERE table_schema = 'public';
