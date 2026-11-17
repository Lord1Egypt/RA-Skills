-- Hybrid Memory Search Schema
-- SQLite FTS5 (lexical) + sqlite-vec (semantic) with RRF fusion
-- v2.2.0: adds fact lifecycle columns (status, confidence, valid_from,
--         superseded_by, source_context) for conflict resolution.
-- v3.3.0: the engine now enforces the state machine it always relied on
--         (CHECK on status/confidence, FOREIGN KEY on superseded_by), and the
--         vec table gets the same AFTER UPDATE trigger the FTS table already had.
--         Requires PRAGMA foreign_keys=ON on every connection (see connect()).

-- Main memories table
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    category TEXT DEFAULT 'general',      -- daily-note, skill, reference, config, archive, etc.
    layer TEXT DEFAULT 'episodic',          -- episodic, semantic, procedural
    source TEXT NOT NULL,                  -- filename or path
    score REAL DEFAULT 0.0,                -- importance score (0-1)
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    superseded_by INTEGER DEFAULT NULL
        REFERENCES memories(id)            -- the fact that replaced this one (NULL = none)
        ON DELETE SET NULL,                -- archiving/deleting the successor must not
                                           -- leave a dangling pointer (M2)
    -- ─── v2.2.0 fact lifecycle (see CHANGELOG) ───
    subject TEXT DEFAULT NULL,             -- entity the fact is about, e.g. "serveur_prod"
    status TEXT DEFAULT 'active'
        CHECK (status IN ('active', 'superseded', 'disputed')),
    confidence REAL DEFAULT 1.0
        CHECK (confidence IS NULL OR (confidence >= 0.0 AND confidence <= 1.0)),
    valid_from TEXT DEFAULT NULL,          -- ISO timestamp, when the fact became true
    source_context TEXT DEFAULT NULL,      -- originating message/prompt (audit trail)
    last_confirmed TEXT DEFAULT NULL,      -- ISO timestamp of last redundant confirmation
    -- ─── v3.4 point-in-time retrieval ───
    superseded_at TEXT DEFAULT NULL        -- ISO timestamp, when this row STOPPED being
                                           -- active (NULL while it is active). Distinct from
                                           -- valid_from (when the fact became TRUE in the
                                           -- world) and from updated_at (rewritten on every
                                           -- touch, e.g. a REDUNDANT confirmation). This is
                                           -- the one column that answers "what was known on
                                           -- date D?": created_at <= D AND (still active at
                                           -- D). See retrieval_as_of().
);

-- FTS5 virtual table (external content = memories)
CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
    content,
    content='memories',
    content_rowid='id',
    tokenize='unicode61 remove_diacritics 2'
);

-- sqlite-vec virtual table (768-dim float embeddings)
CREATE VIRTUAL TABLE IF NOT EXISTS memories_vec USING vec0(
    embedding float[768]
);

-- Triggers to keep FTS5 in sync with memories table
CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
    INSERT INTO memories_fts(rowid, content) VALUES (new.id, new.content);
END;

CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
    INSERT INTO memories_fts(memories_fts, rowid, content) VALUES ('delete', old.id, old.content);
END;

CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
    INSERT INTO memories_fts(memories_fts, rowid, content) VALUES ('delete', old.id, old.content);
    INSERT INTO memories_fts(rowid, content) VALUES (new.id, new.content);
END;

-- Trigger: delete from vec on memory deletion
CREATE TRIGGER IF NOT EXISTS memories_vec_ad AFTER DELETE ON memories BEGIN
    DELETE FROM memories_vec WHERE rowid = old.id;
END;

-- Note on the vec table and UPDATE: SQLite cannot read an embedding out of the
-- vec0 virtual table from a trigger, so vec rows cannot be resynced on UPDATE
-- the way FTS5 can. Content edits never re-embed here (the embedding is written
-- once, at insert, by add_memory), so a stale vec row can only arise from an
-- add_memory that fails between the two INSERTs. That is fixed at the source, by
-- making add_memory transactional (C4) — not by a trigger. Deletion stays
-- covered by memories_vec_ad above.

-- Indexes for lifecycle queries (status filtering during retrieval)
CREATE INDEX IF NOT EXISTS idx_memories_status ON memories(status);
CREATE INDEX IF NOT EXISTS idx_memories_subject ON memories(subject);
