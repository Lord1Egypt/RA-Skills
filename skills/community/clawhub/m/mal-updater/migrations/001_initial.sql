CREATE TABLE IF NOT EXISTS provider_series (
    provider TEXT NOT NULL,
    provider_series_id TEXT NOT NULL,
    title TEXT NOT NULL,
    season_title TEXT,
    season_number INTEGER,
    raw_json TEXT,
    first_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (provider, provider_series_id)
);

CREATE TABLE IF NOT EXISTS provider_episode_progress (
    provider TEXT NOT NULL,
    provider_episode_id TEXT NOT NULL,
    provider_series_id TEXT NOT NULL,
    episode_number INTEGER,
    episode_title TEXT,
    playback_position_ms INTEGER,
    duration_ms INTEGER,
    completion_ratio REAL,
    last_watched_at TEXT,
    audio_locale TEXT,
    subtitle_locale TEXT,
    rating TEXT,
    raw_json TEXT,
    first_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (provider, provider_episode_id),
    FOREIGN KEY (provider, provider_series_id)
        REFERENCES provider_series(provider, provider_series_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS provider_watchlist (
    provider TEXT NOT NULL,
    provider_series_id TEXT NOT NULL,
    added_at TEXT,
    status TEXT,
    raw_json TEXT,
    first_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (provider, provider_series_id),
    FOREIGN KEY (provider, provider_series_id)
        REFERENCES provider_series(provider, provider_series_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mal_series_mapping (
    provider TEXT NOT NULL,
    provider_series_id TEXT NOT NULL,
    mal_anime_id INTEGER NOT NULL,
    confidence REAL,
    mapping_source TEXT NOT NULL,
    approved_by_user INTEGER NOT NULL DEFAULT 0,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (provider, provider_series_id),
    FOREIGN KEY (provider, provider_series_id)
        REFERENCES provider_series(provider, provider_series_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS review_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    provider_series_id TEXT,
    provider_episode_id TEXT,
    issue_type TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'warning',
    payload_json TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TEXT
);

CREATE TABLE IF NOT EXISTS sync_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    contract_version TEXT NOT NULL,
    mode TEXT NOT NULL,
    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TEXT,
    status TEXT NOT NULL DEFAULT 'running',
    summary_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_progress_series ON provider_episode_progress(provider, provider_series_id);
CREATE INDEX IF NOT EXISTS idx_review_status ON review_queue(status, severity);
