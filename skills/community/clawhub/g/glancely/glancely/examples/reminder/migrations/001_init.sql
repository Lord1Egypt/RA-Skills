CREATE TABLE IF NOT EXISTS reminders (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    due_date    TEXT,
    status      TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','done','cancelled')),
    notes       TEXT,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    completed_at TEXT
);
CREATE INDEX IF NOT EXISTS reminders_status ON reminders(status);
CREATE INDEX IF NOT EXISTS reminders_due_date ON reminders(due_date);
