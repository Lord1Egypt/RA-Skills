CREATE TABLE IF NOT EXISTS mit_entries (
    date        TEXT PRIMARY KEY,
    task        TEXT NOT NULL,
    completed   INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
