-- ============================================================================
-- Personal Assistant Skill — Database Schema
-- Sprint 0: SQLite 建表语句
-- ============================================================================

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ============================================================================
-- 1. tasks — 核心任务表
-- ============================================================================
CREATE TABLE IF NOT EXISTS tasks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,

    -- 基本信息
    title           TEXT NOT NULL,                     -- 任务标题
    description     TEXT DEFAULT '',                   -- 详细描述（Markdown）
    category        TEXT DEFAULT '',                   -- 分类标签（如 "开发"、"会议"、"文档"）

    -- 状态
    status          TEXT NOT NULL DEFAULT 'todo'
                    CHECK(status IN ('todo', 'in_progress', 'blocked', 'done', 'cancelled')),
    priority        INTEGER NOT NULL DEFAULT 3
                    CHECK(priority BETWEEN 1 AND 5),   -- 1=最高, 5=最低

    -- 时间
    deadline        TEXT,                              -- ISO 8601，如 "2026-06-01T18:00:00"
    start_time      TEXT,                              -- 计划开始时间
    estimated_hours REAL DEFAULT 0,                    -- 预估耗时（小时）
    actual_hours    REAL DEFAULT 0,                    -- 实际耗时（小时）

    -- 进展
    progress        INTEGER DEFAULT 0
                    CHECK(progress BETWEEN 0 AND 100), -- 完成百分比
    progress_note   TEXT DEFAULT '',                   -- 最新进展简述

    -- 关联
    parent_task_id  INTEGER REFERENCES tasks(id) ON DELETE SET NULL,
    okr_id          INTEGER REFERENCES okr_items(id) ON DELETE SET NULL,
    source_type     TEXT DEFAULT 'manual'
                    CHECK(source_type IN ('manual', 'recurring', 'okr', 'import')),
    recurring_id    INTEGER REFERENCES recurring_tasks(id) ON DELETE SET NULL,

    -- 元数据
    extra           TEXT DEFAULT '{}',                 -- JSON 扩展字段
    created_at      TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_deadline ON tasks(deadline);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category);
CREATE INDEX IF NOT EXISTS idx_tasks_parent ON tasks(parent_task_id);
CREATE INDEX IF NOT EXISTS idx_tasks_okr ON tasks(okr_id);


-- ============================================================================
-- 2. milestones — 里程碑表
-- ============================================================================
CREATE TABLE IF NOT EXISTS milestones (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id         INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    title           TEXT NOT NULL,                     -- 里程碑名称
    status          TEXT NOT NULL DEFAULT 'pending'
                    CHECK(status IN ('pending', 'completed')),
    due_date        TEXT,                              -- 预期完成时间
    completed_at    TEXT,                              -- 实际完成时间
    sort_order      INTEGER DEFAULT 0,                 -- 排序权重
    created_at      TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE INDEX IF NOT EXISTS idx_milestones_task ON milestones(task_id);


-- ============================================================================
-- 3. progress_logs — 进展日志表
-- ============================================================================
CREATE TABLE IF NOT EXISTS progress_logs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id         INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    content         TEXT NOT NULL,                     -- 进展内容（Markdown）
    progress_before INTEGER,                           -- 更新前进度 %
    progress_after  INTEGER,                           -- 更新后进度 %
    hours_spent     REAL DEFAULT 0,                    -- 本次投入小时
    logged_at       TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE INDEX IF NOT EXISTS idx_progress_logs_task ON progress_logs(task_id);
CREATE INDEX IF NOT EXISTS idx_progress_logs_date ON progress_logs(logged_at);


-- ============================================================================
-- 4. recurring_tasks — 周期任务模板表
-- ============================================================================
CREATE TABLE IF NOT EXISTS recurring_tasks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,

    -- 任务模板
    template_title  TEXT NOT NULL,                     -- 任务标题模板
    template_desc   TEXT DEFAULT '',                   -- 描述模板
    category        TEXT DEFAULT '',
    priority        INTEGER DEFAULT 3,
    estimated_hours REAL DEFAULT 0,

    -- 周期规则
    recurrence_type TEXT NOT NULL
                    CHECK(recurrence_type IN ('daily', 'weekly', 'biweekly', 'monthly', 'custom')),
    recurrence_rule TEXT,                              -- 自定义规则（类 cron 或 iCal RRULE）

    -- 调度状态
    enabled         INTEGER NOT NULL DEFAULT 1,        -- 0=暂停, 1=启用
    next_run_date   TEXT NOT NULL,                     -- 下次生成实例的日期
    last_run_date   TEXT,                              -- 上次生成日期
    advance_days    INTEGER DEFAULT 0,                 -- 提前生成天数

    -- 元数据
    extra           TEXT DEFAULT '{}',
    created_at      TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);


-- ============================================================================
-- 5. okr_items — OKR 本地缓存表
-- ============================================================================
CREATE TABLE IF NOT EXISTS okr_items (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,

    -- OKR 基本信息
    title           TEXT NOT NULL,
    description     TEXT DEFAULT '',
    parent_id       INTEGER REFERENCES okr_items(id) ON DELETE SET NULL,
    obj_type        TEXT NOT NULL DEFAULT 'objective'
                    CHECK(obj_type IN ('objective', 'key_result', 'initiative')),

    -- 进展与状态
    progress        INTEGER DEFAULT 0
                    CHECK(progress BETWEEN 0 AND 100),
    status          TEXT NOT NULL DEFAULT 'active'
                    CHECK(status IN ('active', 'completed', 'cancelled')),

    -- 时间范围
    start_date      TEXT,
    end_date        TEXT,

    -- 权重与扩展
    weight          REAL DEFAULT 1.0,
    extra           TEXT DEFAULT '{}',

    -- 飞书文档来源
    source_doc_token TEXT,                             -- 飞书文档 token
    synced_at       TEXT,                              -- 最后同步时间

    -- 元数据
    created_at      TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE INDEX IF NOT EXISTS idx_okr_status ON okr_items(status);
CREATE INDEX IF NOT EXISTS idx_okr_parent ON okr_items(parent_id);
CREATE INDEX IF NOT EXISTS idx_okr_source ON okr_items(source_doc_token);


-- ============================================================================
-- 6. reminder_log — 提醒去重日志表
-- ============================================================================
CREATE TABLE IF NOT EXISTS reminder_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id         INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    reminder_type   TEXT NOT NULL
                    CHECK(reminder_type IN ('morning', 'afternoon', 'evening', 'deadline_alert', 'manual')),
    reminder_date   TEXT NOT NULL,                     -- 提醒日期，如 "2026-05-26"
    sent_at         TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    message         TEXT DEFAULT '',

    UNIQUE(task_id, reminder_type, reminder_date)
);
