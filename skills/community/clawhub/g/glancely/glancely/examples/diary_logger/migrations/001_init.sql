-- diary_logger: minimal local cache. Time-tracking source of truth is Calendar.
CREATE TABLE IF NOT EXISTS diary_category_overrides (
    keyword     TEXT PRIMARY KEY,
    category    TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
