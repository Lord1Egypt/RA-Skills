-- Memory V2.5 Database Schema
-- SQLite database schema for Memory Lucia V2.5

-- Priority Analysis Table
CREATE TABLE IF NOT EXISTS memory_priorities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id TEXT NOT NULL,
    conversation_id INTEGER,
    priority_level INTEGER CHECK(priority_level BETWEEN 1 AND 4),
    importance_score REAL DEFAULT 0,
    keywords TEXT,
    context_summary TEXT,
    auto_detected BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Learning Tracking Table
CREATE TABLE IF NOT EXISTS memory_learning (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id TEXT NOT NULL,
    conversation_id INTEGER,
    learning_topic TEXT NOT NULL,
    topic_category TEXT,
    progress_status TEXT CHECK(progress_status IN ('not_started', 'started', 'in_progress', 'completed', 'on_hold')),
    progress_percentage INTEGER DEFAULT 0 CHECK(progress_percentage BETWEEN 0 AND 100),
    estimated_completion_date DATETIME,
    actual_completion_date DATETIME,
    milestone_count INTEGER DEFAULT 0,
    completed_milestones INTEGER DEFAULT 0,
    resources TEXT,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Learning Milestones Table
CREATE TABLE IF NOT EXISTS memory_learning_milestones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    learning_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending',
    target_date DATETIME,
    completed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (learning_id) REFERENCES memory_learning(id) ON DELETE CASCADE
);

-- Decision Records Table
CREATE TABLE IF NOT EXISTS memory_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id TEXT NOT NULL,
    conversation_id INTEGER,
    decision_type TEXT,
    decision_question TEXT NOT NULL,
    decision_context TEXT,
    options_considered TEXT,
    chosen_option TEXT,
    rationale TEXT,
    confidence_level INTEGER CHECK(confidence_level BETWEEN 1 AND 5),
    expected_outcome TEXT,
    actual_outcome TEXT,
    outcome_status TEXT CHECK(outcome_status IN ('pending', 'implemented', 'validated', 'rejected')),
    review_date DATETIME,
    reviewed_at DATETIME,
    review_notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Skill Evolution Table
CREATE TABLE IF NOT EXISTS memory_evolution (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT NOT NULL,
    skill_category TEXT,
    proficiency_level INTEGER DEFAULT 1 CHECK(proficiency_level BETWEEN 1 AND 10),
    experience_points INTEGER DEFAULT 0,
    usage_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    last_used_at DATETIME,
    first_used_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    performance_metrics TEXT,
    improvement_areas TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Skill Evolution History Table
CREATE TABLE IF NOT EXISTS memory_evolution_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    event_data TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (skill_id) REFERENCES memory_evolution(id) ON DELETE CASCADE
);

-- Version Management Table
CREATE TABLE IF NOT EXISTS memory_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_name TEXT NOT NULL,
    version_type TEXT,
    description TEXT,
    backup_path TEXT,
    backup_size INTEGER,
    checksum TEXT,
    is_active BOOLEAN DEFAULT 0,
    migration_script TEXT,
    rollback_script TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    activated_at DATETIME
);

-- Version Statistics Table
CREATE TABLE IF NOT EXISTS memory_version_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_id INTEGER,
    stat_name TEXT,
    stat_value INTEGER,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_priorities_level ON memory_priorities(priority_level);
CREATE INDEX IF NOT EXISTS idx_priorities_created ON memory_priorities(created_at);
CREATE INDEX IF NOT EXISTS idx_learning_status ON memory_learning(progress_status);
CREATE INDEX IF NOT EXISTS idx_learning_topic ON memory_learning(learning_topic);
CREATE INDEX IF NOT EXISTS idx_decisions_status ON memory_decisions(outcome_status);
CREATE INDEX IF NOT EXISTS idx_decisions_review ON memory_decisions(review_date);
CREATE INDEX IF NOT EXISTS idx_evolution_skill ON memory_evolution(skill_name);
CREATE INDEX IF NOT EXISTS idx_evolution_category ON memory_evolution(skill_category);

-- Insert initial version
INSERT OR IGNORE INTO memory_versions (version_name, version_type, description, is_active) 
VALUES ('2.5.0', 'initial', 'Memory V2.5 Initial Version', 1);

-- Views for common queries

-- View: Pending Decisions
CREATE VIEW IF NOT EXISTS v_pending_decisions AS
SELECT 
    d.*,
    CASE 
        WHEN review_date < datetime('now') THEN 'overdue'
        WHEN review_date <= datetime('now', '+7 days') THEN 'due_soon'
        ELSE 'scheduled'
    END as review_status
FROM memory_decisions d
WHERE outcome_status IN ('pending', 'implemented')
    AND (review_date IS NULL OR review_date <= datetime('now', '+7 days'))
ORDER BY review_date ASC;

-- View: Skill Summary
CREATE VIEW IF NOT EXISTS v_skill_summary AS
SELECT 
    skill_name,
    skill_category,
    usage_count,
    success_count,
    CASE 
        WHEN usage_count > 0 THEN ROUND(100.0 * success_count / usage_count, 2)
        ELSE 0
    END as success_rate,
    proficiency_level,
    experience_points,
    last_used_at,
    first_used_at
FROM memory_evolution
ORDER BY usage_count DESC;

-- View: Active Learning
CREATE VIEW IF NOT EXISTS v_active_learning AS
SELECT 
    l.*,
    CASE 
        WHEN progress_percentage = 0 THEN 'not_started'
        WHEN progress_percentage < 50 THEN 'early_stage'
        WHEN progress_percentage < 100 THEN 'in_progress'
        ELSE 'completed'
    END as stage
FROM memory_learning l
WHERE progress_status IN ('started', 'in_progress')
ORDER BY updated_at DESC;

-- View: Weekly Learning Report
CREATE VIEW IF NOT EXISTS v_weekly_learning_report AS
SELECT 
    learning_topic,
    topic_category,
    progress_status,
    progress_percentage,
    milestone_count,
    completed_milestones,
    updated_at,
    CASE 
        WHEN progress_percentage = 100 THEN 'completed'
        WHEN progress_percentage > 0 THEN 'in_progress'
        ELSE 'not_started'
    END as status_label
FROM memory_learning
WHERE updated_at >= datetime('now', '-7 days')
ORDER BY updated_at DESC;

-- View: High Priority Items
CREATE VIEW IF NOT EXISTS v_high_priority_messages AS
SELECT 
    'priority' as type,
    id,
    message_id,
    priority_level as level,
    importance_score,
    context_summary as details,
    created_at
FROM memory_priorities
WHERE priority_level <= 2
UNION ALL
SELECT 
    'decision' as type,
    id,
    message_id,
    CASE outcome_status 
        WHEN 'pending' THEN 1
        WHEN 'implemented' THEN 2
        ELSE 3
    END as level,
    confidence_level as importance_score,
    decision_question as details,
    created_at
FROM memory_decisions
WHERE outcome_status = 'pending' AND review_date <= datetime('now', '+7 days')
ORDER BY created_at DESC;
