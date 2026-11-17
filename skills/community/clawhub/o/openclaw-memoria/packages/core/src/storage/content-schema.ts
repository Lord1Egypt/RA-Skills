/**
 * Schéma des DB de contenu (spec §3.2) — une par instance d'assistant
 * (`assistants/<instance_id>/memory.sqlite`) + une par scope partagé
 * (`shared/<scope>.sqlite`).
 *
 * Corrections de bugs GRAVÉES dans le schéma :
 *  - pas de colonne `status` → `superseded` + `lifecycle_state` (bug db.ts:604) ;
 *  - `failure_reasons` présente sur procedures (bug procedural.ts:1053) ;
 *  - FTS5 external-content synchronisé par TRIGGERS sur rowid explicite —
 *    plus jamais de rebuild manuel désaligné (bug procedural.ts:296) ;
 *  - `embeddings.model` + `dimensions` obligatoires — la comparaison
 *    inter-dimensions est interdite (bug fallback 768/1536).
 *
 * Les tables des couches cognitives avancées (observations, entities,
 * relations, cluster_members…) arrivent par migrations additives au moment
 * du port de chaque couche.
 */
import type { Migration } from './migrations.js'

export const contentMigrations: Migration[] = [
  {
    version: 1,
    name: 'content-initial',
    up(db) {
      db.exec(`
        CREATE TABLE meta (
          key TEXT PRIMARY KEY,
          value TEXT
        );

        CREATE TABLE facts (
          id TEXT PRIMARY KEY,
          fact TEXT NOT NULL,
          category TEXT NOT NULL DEFAULT 'general',
          fact_type TEXT NOT NULL DEFAULT 'statement',
          confidence REAL NOT NULL DEFAULT 0.8,
          source TEXT NOT NULL DEFAULT 'manual',
          assistant_instance_id TEXT,
          user_id TEXT,
          org_id TEXT,
          client_org_id TEXT,
          project_id TEXT,
          topic_id TEXT,
          scope_id TEXT NOT NULL,
          sensitivity TEXT NOT NULL DEFAULT 'normal' CHECK (sensitivity IN ('normal','sensitive','critical')),
          visibility TEXT NOT NULL DEFAULT 'private' CHECK (visibility IN ('private','shared')),
          tags TEXT NOT NULL DEFAULT '[]',
          entity_ids TEXT NOT NULL DEFAULT '[]',
          lifecycle_state TEXT NOT NULL DEFAULT 'active' CHECK (lifecycle_state IN ('active','dormant','archived')),
          superseded INTEGER NOT NULL DEFAULT 0,
          superseded_by TEXT,
          usefulness REAL NOT NULL DEFAULT 0,
          recall_count INTEGER NOT NULL DEFAULT 0,
          used_count INTEGER NOT NULL DEFAULT 0,
          relevance_weight REAL NOT NULL DEFAULT 1.0,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          last_accessed_at TEXT
        );
        CREATE INDEX idx_facts_scope ON facts(scope_id);
        CREATE INDEX idx_facts_lifecycle ON facts(lifecycle_state, superseded);
        CREATE INDEX idx_facts_category ON facts(category);
        CREATE INDEX idx_facts_project ON facts(project_id) WHERE project_id IS NOT NULL;
        CREATE INDEX idx_facts_client ON facts(client_org_id) WHERE client_org_id IS NOT NULL;

        CREATE VIRTUAL TABLE facts_fts USING fts5(
          fact, category, tags,
          content='facts', content_rowid='rowid',
          tokenize='unicode61 remove_diacritics 2'
        );
        CREATE TRIGGER facts_ai AFTER INSERT ON facts BEGIN
          INSERT INTO facts_fts(rowid, fact, category, tags)
          VALUES (new.rowid, new.fact, new.category, new.tags);
        END;
        CREATE TRIGGER facts_ad AFTER DELETE ON facts BEGIN
          INSERT INTO facts_fts(facts_fts, rowid, fact, category, tags)
          VALUES ('delete', old.rowid, old.fact, old.category, old.tags);
        END;
        CREATE TRIGGER facts_au AFTER UPDATE OF fact, category, tags ON facts BEGIN
          INSERT INTO facts_fts(facts_fts, rowid, fact, category, tags)
          VALUES ('delete', old.rowid, old.fact, old.category, old.tags);
          INSERT INTO facts_fts(rowid, fact, category, tags)
          VALUES (new.rowid, new.fact, new.category, new.tags);
        END;

        CREATE TABLE procedures (
          id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          description TEXT NOT NULL DEFAULT '',
          steps TEXT NOT NULL DEFAULT '[]',
          trigger_patterns TEXT NOT NULL DEFAULT '[]',
          success_count INTEGER NOT NULL DEFAULT 0,
          failure_count INTEGER NOT NULL DEFAULT 0,
          failure_reasons TEXT NOT NULL DEFAULT '[]',
          scope_id TEXT NOT NULL,
          assistant_instance_id TEXT,
          project_id TEXT,
          lifecycle_state TEXT NOT NULL DEFAULT 'active' CHECK (lifecycle_state IN ('active','dormant','archived')),
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );
        CREATE INDEX idx_procedures_scope ON procedures(scope_id);

        CREATE VIRTUAL TABLE procedures_fts USING fts5(
          name, description, trigger_patterns,
          content='procedures', content_rowid='rowid',
          tokenize='unicode61 remove_diacritics 2'
        );
        CREATE TRIGGER procedures_ai AFTER INSERT ON procedures BEGIN
          INSERT INTO procedures_fts(rowid, name, description, trigger_patterns)
          VALUES (new.rowid, new.name, new.description, new.trigger_patterns);
        END;
        CREATE TRIGGER procedures_ad AFTER DELETE ON procedures BEGIN
          INSERT INTO procedures_fts(procedures_fts, rowid, name, description, trigger_patterns)
          VALUES ('delete', old.rowid, old.name, old.description, old.trigger_patterns);
        END;
        CREATE TRIGGER procedures_au AFTER UPDATE OF name, description, trigger_patterns ON procedures BEGIN
          INSERT INTO procedures_fts(procedures_fts, rowid, name, description, trigger_patterns)
          VALUES ('delete', old.rowid, old.name, old.description, old.trigger_patterns);
          INSERT INTO procedures_fts(rowid, name, description, trigger_patterns)
          VALUES (new.rowid, new.name, new.description, new.trigger_patterns);
        END;

        CREATE TABLE topics (
          id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          scope_id TEXT,
          share_policy TEXT,
          sensitivity TEXT NOT NULL DEFAULT 'normal' CHECK (sensitivity IN ('normal','sensitive','critical')),
          importance_score REAL NOT NULL DEFAULT 0,
          keywords TEXT NOT NULL DEFAULT '[]',
          created_at TEXT NOT NULL
        );
        CREATE TABLE fact_topics (
          fact_id TEXT NOT NULL REFERENCES facts(id) ON DELETE CASCADE,
          topic_id TEXT NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
          PRIMARY KEY (fact_id, topic_id)
        );

        CREATE TABLE embeddings (
          id TEXT PRIMARY KEY,
          owner_type TEXT NOT NULL CHECK (owner_type IN ('fact','procedure','observation','topic')),
          owner_id TEXT NOT NULL,
          model TEXT NOT NULL,
          dimensions INTEGER NOT NULL,
          vector BLOB NOT NULL,
          created_at TEXT NOT NULL
        );
        CREATE UNIQUE INDEX idx_embeddings_owner ON embeddings(owner_type, owner_id, model);
        CREATE INDEX idx_embeddings_model ON embeddings(model, dimensions);

        CREATE TABLE embedding_jobs (
          id TEXT PRIMARY KEY,
          target_model TEXT NOT NULL,
          target_dimensions INTEGER NOT NULL,
          status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','running','done','failed')),
          created_at TEXT NOT NULL,
          completed_at TEXT
        );

        -- WAL = SOURCE DE VÉRITÉ de la capture (spec §6.2) :
        -- append AVANT tout LLM, markProcessed APRÈS succès, replay au boot, cleanup borné.
        CREATE TABLE wal_buffer (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          ts TEXT NOT NULL,
          assistant_instance_id TEXT NOT NULL,
          role TEXT NOT NULL CHECK (role IN ('user','assistant','tool')),
          content TEXT NOT NULL,
          processed INTEGER NOT NULL DEFAULT 0,
          attempts INTEGER NOT NULL DEFAULT 0
        );
        CREATE INDEX idx_wal_pending ON wal_buffer(processed, ts);

        CREATE TABLE memory_projection (
          fact_id TEXT NOT NULL,
          projection_model TEXT NOT NULL,
          x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL,
          created_at TEXT NOT NULL,
          PRIMARY KEY (fact_id, projection_model)
        );

        CREATE TABLE memory_sources (
          id TEXT PRIMARY KEY,
          source_type TEXT NOT NULL,
          source_path TEXT,
          source_hash TEXT NOT NULL,
          imported_at TEXT NOT NULL,
          metadata TEXT NOT NULL DEFAULT '{}'
        );
        CREATE UNIQUE INDEX idx_sources_hash ON memory_sources(source_hash);

        CREATE TABLE memory_import_items (
          id TEXT PRIMARY KEY,
          source_id TEXT NOT NULL REFERENCES memory_sources(id) ON DELETE CASCADE,
          target_memory_id TEXT,
          target_type TEXT,
          proposed_scope_id TEXT,
          proposed_entity_ids TEXT NOT NULL DEFAULT '[]',
          status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','accepted','rejected','duplicate')),
          confidence REAL NOT NULL DEFAULT 0.5,
          reviewed_by TEXT,
          reviewed_at TEXT
        );
      `)
    },
  },
  {
    version: 2,
    name: 'content-sync-provenance',
    up(db) {
      // SYNCHRO INTER-MACHINES (SYNC-INTER-MACHINES.md §3.2) : provenance + LWW.
      // ALTER additifs (DB v1 existante préservée).
      const cols = (db.pragma('table_info(facts)') as Array<{ name: string }>).map(c => c.name)
      if (!cols.includes('origin_machine_id')) db.exec('ALTER TABLE facts ADD COLUMN origin_machine_id TEXT')
      if (!cols.includes('origin_rev')) db.exec('ALTER TABLE facts ADD COLUMN origin_rev INTEGER NOT NULL DEFAULT 0')
      if (!cols.includes('content_hash')) db.exec('ALTER TABLE facts ADD COLUMN content_hash TEXT')
      if (!cols.includes('deleted_at')) db.exec('ALTER TABLE facts ADD COLUMN deleted_at TEXT')
      db.exec('CREATE INDEX IF NOT EXISTS idx_facts_origin ON facts(origin_machine_id, origin_rev)')
      db.exec('CREATE INDEX IF NOT EXISTS idx_facts_content_hash ON facts(content_hash)')
    },
  },
]
