CREATE TABLE IF NOT EXISTS mal_anime_metadata (
    mal_anime_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    title_english TEXT,
    title_japanese TEXT,
    alternative_titles_json TEXT,
    media_type TEXT,
    status TEXT,
    num_episodes INTEGER,
    mean REAL,
    popularity INTEGER,
    start_season_json TEXT,
    raw_json TEXT NOT NULL,
    fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mal_anime_relations (
    mal_anime_id INTEGER NOT NULL,
    related_mal_anime_id INTEGER NOT NULL,
    relation_type TEXT NOT NULL,
    relation_type_formatted TEXT,
    related_title TEXT,
    raw_json TEXT NOT NULL,
    fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (mal_anime_id, related_mal_anime_id, relation_type)
);

CREATE INDEX IF NOT EXISTS idx_mal_relations_source ON mal_anime_relations(mal_anime_id, relation_type);
CREATE INDEX IF NOT EXISTS idx_mal_relations_target ON mal_anime_relations(related_mal_anime_id, relation_type);
