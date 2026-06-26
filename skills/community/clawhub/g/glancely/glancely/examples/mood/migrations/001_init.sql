CREATE TABLE IF NOT EXISTS mood_entries (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    mood_score  INTEGER,
    mood_label  TEXT,
    note        TEXT,
    raw_text    TEXT
);
CREATE INDEX IF NOT EXISTS mood_entries_created_at ON mood_entries(created_at);
