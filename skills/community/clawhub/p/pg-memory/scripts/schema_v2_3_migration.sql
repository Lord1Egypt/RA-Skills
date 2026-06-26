-- pg-memory v2.3 Schema Migration
-- Adds: related observations, summaries, chains, templates, reminders
-- Created: 2026-02-28

-- ============================================
-- 1. ENHANCE OBSERVATIONS (Related linking)
-- ============================================

-- Add related_observation_ids for bidirectional linking
ALTER TABLE observations
ADD COLUMN IF NOT EXISTS related_observation_ids UUID[] DEFAULT '{}',
ADD COLUMN IF NOT EXISTS supersedes_observation_id UUID REFERENCES observations(id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_observations_related ON observations USING gin(related_observation_ids);
CREATE INDEX IF NOT EXISTS idx_observations_supersedes ON observations(supersedes_observation_id) WHERE supersedes_observation_id IS NOT NULL;

-- ============================================
-- 2. SUMMARIES TABLE (Auto-generated, separate from observations)
-- ============================================
-- CRITICAL: This table is ADDITIONAL, does not modify observations

CREATE TABLE IF NOT EXISTS summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Source tracking (what this summarizes)
    source_observation_ids UUID[] NOT NULL,  -- Array of observation IDs summarized
    source_session_ids UUID[],               -- Sessions included
    source_tags TEXT[],                      -- Tags filter used
    
    -- The summary itself
    summary_type VARCHAR(50) NOT NULL DEFAULT 'auto',  -- 'auto', 'manual', 'weekly', 'project'
    title VARCHAR(255),
    content TEXT NOT NULL,
    
    -- Metadata
    importance_score DECIMAL(3,2) DEFAULT 0.5 CHECK (importance_score >= 0 AND importance_score <= 1),
    generated_by VARCHAR(100) DEFAULT 'system',  -- 'system', 'user', agent name
    generation_model VARCHAR(100),               -- LLM model used
    
    -- Temporal
    covers_from TIMESTAMP WITH TIME ZONE,    -- Start of period summarized
    covers_until TIMESTAMP WITH TIME ZONE,       -- End of period
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Status
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'archived', 'superseded'))
);

-- Indexes for summaries
CREATE INDEX IF NOT EXISTS idx_summaries_source_obs ON summaries USING gin(source_observation_ids);
CREATE INDEX IF NOT EXISTS idx_summaries_type ON summaries(summary_type, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_summaries_covers ON summaries(covers_from, covers_until);
CREATE INDEX IF NOT EXISTS idx_summaries_created ON summaries(created_at DESC);

-- Full-text search on summaries
CREATE INDEX IF NOT EXISTS idx_summaries_fts ON summaries USING gin(to_tsvector('english', content));

-- ============================================
-- 3. OBSERVATION CHAINS (Project/workflow tracking)
-- ============================================

CREATE TABLE IF NOT EXISTS observation_chains (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Chain identification
    chain_name VARCHAR(255) NOT NULL,
    chain_type VARCHAR(50) NOT NULL DEFAULT 'project',  -- 'project', 'decision', 'bugfix', 'workflow'
    chain_description TEXT,
    
    -- Initial observation that started this chain
    root_observation_id UUID REFERENCES observations(id) ON DELETE SET NULL,
    
    -- Chain status
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'complete', 'abandoned', 'paused')),
    
    -- Progress tracking
    current_step INTEGER DEFAULT 0,
    total_steps INTEGER DEFAULT 0,
    
    -- Temporal
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    tags TEXT[] DEFAULT '{}',
    importance_score DECIMAL(3,2) DEFAULT 0.5,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Chain steps (linking observations to chains)
CREATE TABLE IF NOT EXISTS chain_steps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chain_id UUID NOT NULL REFERENCES observation_chains(id) ON DELETE CASCADE,
    observation_id UUID REFERENCES observations(id) ON DELETE SET NULL,
    
    step_number INTEGER NOT NULL,
    step_type VARCHAR(50) NOT NULL DEFAULT 'milestone',  -- 'decision', 'action', 'milestone', 'blocker', 'resolution'
    step_description TEXT,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    
    -- Unique constraint: one observation per position in chain
    UNIQUE(chain_id, step_number)
);

-- Indexes for chains
CREATE INDEX IF NOT EXISTS idx_chains_status ON observation_chains(status, started_at DESC);
CREATE INDEX IF NOT EXISTS idx_chains_type ON observation_chains(chain_type, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_chains_root ON observation_chains(root_observation_id) WHERE root_observation_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_chain_steps_chain ON chain_steps(chain_id, step_number);
CREATE INDEX IF NOT EXISTS idx_chain_steps_obs ON chain_steps(observation_id) WHERE observation_id IS NOT NULL;

-- ============================================
-- 4. OBSERVATION TEMPLATES
-- ============================================

CREATE TABLE IF NOT EXISTS observation_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    template_name VARCHAR(100) NOT NULL UNIQUE,
    template_type VARCHAR(50) NOT NULL,  -- 'bug_report', 'decision', 'project_kickoff', 'milestone'
    
    -- Template structure
    title_template VARCHAR(255),           -- e.g., "Bug: {brief_description}"
    content_template TEXT NOT NULL,        -- Markdown template with placeholders
    
    -- Default values
    default_tags TEXT[] DEFAULT '{}',
    default_importance DECIMAL(3,2) DEFAULT 0.5,
    default_obs_type VARCHAR(50) DEFAULT 'note',
    
    -- Placeholder hints
    placeholder_descriptions JSONB DEFAULT '{}',  -- {"{brief_description}": "One-line bug summary"}
    
    -- Metadata
    created_by VARCHAR(100) DEFAULT 'system',
    usage_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default templates
INSERT INTO observation_templates (template_name, template_type, title_template, content_template, default_tags, default_importance, default_obs_type, placeholder_descriptions)
VALUES 
    ('Bug Report', 'bug_report', 'Bug: {brief_description}', 
     '## Bug Description\n{detailed_description}\n\n## Steps to Reproduce\n{steps}\n\n## Expected Result\n{expected}\n\n## Actual Result\n{actual}\n\n## Related Files\n{files}',
     ARRAY['bug', 'needs-fix'], 0.8, 'error',
     '{"{brief_description}": "One-line summary", "{detailed_description}": "What happened", "{steps}": "How to reproduce", "{expected}": "What should happen", "{actual}": "What actually happened", "{files}": "Files involved"}'),
     
    ('Decision Record', 'decision', 'Decision: {title}',
     '## Context\n{context}\n\n## Decision\n{decision}\n\n## Rationale\n{rationale}\n\n## Alternatives Considered\n{alternatives}\n\n## Consequences\n{consequences}',
     ARRAY['decision', 'adr'], 0.9, 'decision',
     '{"{title}": "Short decision title", "{context}": "What led to this", "{decision}": "What we decided", "{rationale}": "Why", "{alternatives}": "What else was considered", "{consequences}": "Impact"}'),
     
    ('Project Kickoff', 'project_kickoff', 'Project: {project_name}',
     '## {project_name}\n**Assigned**: {timestamp} EST\n**Status**: Active\n**Location**: {project_location}\n\n**Key Details**: {key_details}\n\n**Next Steps**: {next_steps}\n',
     ARRAY['project', 'active'], 0.7, 'ongoing',
     '{"{project_name}": "Project name", "{timestamp}": "YYYY-MM-DD HH:MM", "{project_location}": "Where files are", "{key_details}": "Brief summary", "{next_steps}": "Action items"}'),
     
    ('Milestone', 'milestone', 'Milestone: {title}',
     '## {title}\n**Date**: {date}\n**Project**: {project}\n\n**Achievement**: {achievement}\n\n**Blockers**: {blockers}\n\n**Next**: {next_steps}',
     ARRAY['milestone', 'progress'], 0.6, 'milestone',
     '{"{title}": "Milestone name", "{date}": "When achieved", "{project}": "Related project", "{achievement}": "What was accomplished", "{blockers}": "Any issues", "{next_steps}": "What''s next"}')
ON CONFLICT (template_name) DO NOTHING;

CREATE INDEX IF NOT EXISTS idx_templates_type ON observation_templates(template_type);
CREATE INDEX IF NOT EXISTS idx_templates_active ON observation_templates(is_active) WHERE is_active = TRUE;

-- ============================================
-- 5. FOLLOW-UP REMINDERS (Stale observation alerts)
-- ============================================

CREATE TABLE IF NOT EXISTS follow_up_reminders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- What to remind about
    observation_id UUID REFERENCES observations(id) ON DELETE CASCADE,
    chain_id UUID REFERENCES observation_chains(id) ON DELETE CASCADE,
    
    -- Reminder settings
    reminder_type VARCHAR(50) NOT NULL DEFAULT 'stale_ongoing',  -- 'stale_ongoing', 'milestone_due', 'follow_up'
    reminder_message TEXT,
    
    -- Timing
    remind_at TIMESTAMP WITH TIME ZONE NOT NULL,
    reminded_at TIMESTAMP WITH TIME ZONE,  -- When actually sent
    
    -- Status
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'dismissed', 'snoozed')),
    snooze_until TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reminders_pending ON follow_up_reminders(status, remind_at) WHERE status = 'pending';
CREATE INDEX IF NOT EXISTS idx_reminders_obs ON follow_up_reminders(observation_id) WHERE observation_id IS NOT NULL;

-- ============================================
-- 6. CONFLICT DETECTION LOG (For tracking flagged contradictions)
-- ============================================

CREATE TABLE IF NOT EXISTS observation_conflicts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- The conflicting pair
    observation_1_id UUID NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
    observation_2_id UUID NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
    
    -- Conflict details
    conflict_type VARCHAR(50) NOT NULL,  -- 'contradiction', 'duplicate', 'outdated'
    conflict_score DECIMAL(3,2) NOT NULL,  -- 0.0-1.0 confidence
    conflict_description TEXT,
    
    -- Resolution
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'resolved', 'false_positive')),
    resolved_by VARCHAR(100),
    resolution_notes TEXT,
    resolved_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_conflicts_open ON observation_conflicts(status) WHERE status = 'open';
CREATE INDEX IF NOT EXISTS idx_conflicts_pair ON observation_conflicts(observation_1_id, observation_2_id);

-- ============================================
-- 7. VIEWS FOR NEW FEATURES
-- ============================================

-- Stale ongoing observations view
CREATE OR REPLACE VIEW stale_ongoing_observations AS
SELECT 
    o.id,
    o.title,
    o.content,
    o.status,
    o.started_at,
    o.tags,
    NOW() - o.started_at as age,
    EXTRACT(DAY FROM NOW() - o.started_at) as days_old
FROM observations o
WHERE o.status = 'ongoing'
AND o.started_at < NOW() - INTERVAL '3 days';

-- Chain progress view
CREATE OR REPLACE VIEW chain_progress AS
SELECT 
    c.id as chain_id,
    c.chain_name,
    c.chain_type,
    c.status as chain_status,
    c.current_step,
    c.total_steps,
    ROUND(100.0 * c.current_step / NULLIF(c.total_steps, 0), 1) as percent_complete,
    c.started_at,
    c.completed_at
FROM observation_chains c;

-- Activity timeline (observations + summaries + chain steps)
CREATE OR REPLACE VIEW activity_timeline AS
SELECT 
    'observation' as activity_type,
    o.id,
    o.created_at as activity_time,
    o.title as title,
    o.content as content,
    o.importance_score,
    o.tags,
    NULL::UUID as chain_id
FROM observations o

UNION ALL

SELECT 
    'summary' as activity_type,
    s.id,
    s.created_at as activity_time,
    s.title,
    s.content,
    s.importance_score,
    s.source_tags as tags,
    NULL::UUID
FROM summaries s

UNION ALL

SELECT 
    'chain_step' as activity_type,
    cs.id,
    cs.created_at as activity_time,
    'Step ' || cs.step_number || ' in ' || c.chain_name,
    cs.step_description as content,
    0.5 as importance_score,
    c.tags,
    c.id as chain_id
FROM chain_steps cs
JOIN observation_chains c ON cs.chain_id = c.id

ORDER BY activity_time DESC;

-- ============================================
-- FUNCTIONS FOR NEW FEATURES
-- ============================================

-- Generate summary for time period
CREATE OR REPLACE FUNCTION generate_period_summary(
    p_from TIMESTAMP WITH TIME ZONE,
    p_until TIMESTAMP WITH TIME ZONE,
    p_tags TEXT[] DEFAULT NULL
)
RETURNS TABLE(
    observation_count BIGINT,
    high_importance_count BIGINT,
    file_count BIGINT,
    url_count BIGINT,
    top_tags TEXT[],
    summary_text TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*) as observation_count,
        COUNT(*) FILTER (WHERE importance_score > 0.8) as high_importance_count,
        COUNT(DISTINCT unnest_rel_files) FILTER (WHERE unnest_rel_files IS NOT NULL) as file_count,
        COUNT(DISTINCT unnest_rel_urls) FILTER (WHERE unnest_rel_urls IS NOT NULL) as url_count,
        ARRAY(
            SELECT unnest_tags 
            FROM unnest(array_agg(tags)) as unnest_tags 
            GROUP BY unnest_tags 
            ORDER BY COUNT(*) DESC 
            LIMIT 10
        ) as top_tags,
        string_agg(
            CASE 
                WHEN importance_score > 0.7 THEN '• ' || COALESCE(title, substring(content from 1 for 100))
                ELSE NULL
            END, 
            E'\n'
        ) as summary_text
    FROM observations
    WHERE created_at BETWEEN p_from AND p_until
    AND (p_tags IS NULL OR tags && p_tags);
END;
$$ LANGUAGE plpgsql;

-- Find related observations
CREATE OR REPLACE FUNCTION find_related_observations(
    p_observation_id UUID,
    p_match_tags BOOLEAN DEFAULT TRUE,
    p_match_session BOOLEAN DEFAULT FALSE
)
RETURNS TABLE(
    related_id UUID,
    related_title VARCHAR,
    related_content TEXT,
    relation_type TEXT,
    similarity_score REAL
) AS $$
BEGIN
    RETURN QUERY
    WITH source_obs AS (
        SELECT * FROM observations WHERE id = p_observation_id
    )
    SELECT 
        o.id as related_id,
        o.title as related_title,
        substring(o.content from 1 for 200) as related_content,
        CASE 
            WHEN o.id = ANY(so.related_observation_ids) THEN 'directly_linked'
            WHEN so.id = ANY(o.related_observation_ids) THEN 'reverse_linked'
            WHEN o.tags && so.tags THEN 'tag_match'
            WHEN o.session_id = so.session_id THEN 'same_session'
            ELSE 'similar_content'
        END as relation_type,
        ts_rank(to_tsvector('english', o.content), plainto_tsquery('english', so.content)) as similarity_score
    FROM observations o
    CROSS JOIN source_obs so
    WHERE o.id != p_observation_id
    AND (
        (p_match_tags AND o.tags && so.tags)
        OR (p_match_session AND o.session_id = so.session_id)
        OR (ts_rank(to_tsvector('english', o.content), plainto_tsquery('english', so.content)) > 0.1)
    )
    ORDER BY similarity_score DESC
    LIMIT 20;
END;
$$ LANGUAGE plpgsql;

-- Check for stale observations and create reminders
CREATE OR REPLACE FUNCTION create_stale_reminders(
    p_min_days INTEGER DEFAULT 3
)
RETURNS INTEGER AS $$
DECLARE
    v_count INTEGER := 0;
    obs_record RECORD;
BEGIN
    FOR obs_record IN 
        SELECT id, title, started_at, tags
        FROM observations
        WHERE status = 'ongoing'
        AND started_at < NOW() - INTERVAL '1 day' * p_min_days
        AND NOT EXISTS (
            SELECT 1 FROM follow_up_reminders 
            WHERE observation_id = observations.id 
            AND reminder_type = 'stale_ongoing'
            AND status = 'pending'
        )
    LOOP
        INSERT INTO follow_up_reminders (
            observation_id,
            reminder_type,
            reminder_message,
            remind_at
        ) VALUES (
            obs_record.id,
            'stale_ongoing',
            'Observation "' || COALESCE(obs_record.title, 'Untitled') || '" has been ongoing for ' || p_min_days || '+ days',
            NOW() + INTERVAL '1 hour'
        );
        v_count := v_count + 1;
    END LOOP;
    
    RETURN v_count;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 8. SETTINGS TABLE (For nl_query and other configuration)
-- ============================================

CREATE TABLE IF NOT EXISTS pg_memory_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Setting identity
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT NOT NULL,
    setting_group VARCHAR(50) DEFAULT 'general',  -- 'nl_query', 'performance', 'general'
    
    -- Description for users
    description TEXT,
    
    -- Change tracking
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for settings
CREATE INDEX IF NOT EXISTS idx_settings_key ON pg_memory_settings(setting_key);
CREATE INDEX IF NOT EXISTS idx_settings_group ON pg_memory_settings(setting_group);

-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION update_settings_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS settings_updated_at ON pg_memory_settings;
CREATE TRIGGER settings_updated_at
    BEFORE UPDATE ON pg_memory_settings
    FOR EACH ROW
    EXECUTE FUNCTION update_settings_timestamp();

-- ============================================
-- DEFAULT SETTINGS (nl_query defaults to OpenClaw model)
-- ============================================

-- Get OpenClaw's current model or default to mistral
INSERT INTO pg_memory_settings (setting_key, setting_value, setting_group, description)
VALUES 
    ('nl_query_model', 'ollama/mistral:latest', 'nl_query', 'Model used for natural language to SQL queries'),
    ('nl_query_max_results', '50', 'nl_query', 'Maximum results returned by nl_query'),
    ('nl_query_timeout', '30', 'nl_query', 'Timeout in seconds for SQL generation'),
    ('nl_query_temperature', '0.1', 'nl_query', 'Temperature for LLM SQL generation (0.0-1.0)')
ON CONFLICT (setting_key) DO NOTHING;

-- ============================================
-- COMPLETION
-- ============================================

SELECT 'pg-memory v2.3 schema migration completed successfully' as status;
SELECT 'New tables: summaries, observation_chains, chain_steps, observation_templates, follow_up_reminders, observation_conflicts, pg_memory_settings' as new_tables;
