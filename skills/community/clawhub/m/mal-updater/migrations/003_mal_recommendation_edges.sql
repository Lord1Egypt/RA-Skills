CREATE TABLE IF NOT EXISTS mal_anime_recommendations (
    source_mal_anime_id INTEGER NOT NULL,
    target_mal_anime_id INTEGER NOT NULL,
    target_title TEXT,
    num_recommendations INTEGER,
    hop_distance INTEGER,
    source_kind TEXT NOT NULL DEFAULT 'mal_recommendation',
    raw_json TEXT NOT NULL,
    fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (source_mal_anime_id, target_mal_anime_id, source_kind)
);

CREATE INDEX IF NOT EXISTS idx_mal_recommendations_source ON mal_anime_recommendations(source_mal_anime_id, num_recommendations DESC);
CREATE INDEX IF NOT EXISTS idx_mal_recommendations_target ON mal_anime_recommendations(target_mal_anime_id, num_recommendations DESC);
