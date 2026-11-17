/**
 * Schéma memoria.db v3.34 reconstitué (source de vérité : docs/v3/port-map.json
 * module "db-schema", croisé avec legacy/core/db.ts).
 *
 * État « après boot plugin complet » — avec les pièges du legacy GRAVÉS pour
 * que la migration soit testée contre la réalité, pas contre un schéma idéal :
 *  - `facts.synced_to_md` créée uniquement par sync.ts (bug B2) → variante
 *    AVEC/SANS pilotée par option ;
 *  - PAS de colonne `status` (le bug db.ts:604 la supposait) ;
 *  - `lifecycle_state` à valeurs legacy fresh|settled|dormant ;
 *  - `procedures` SANS failure_reasons (bug B3), 13 colonnes additives
 *    optionnelles (les try/catch muets ont pu laisser des schémas partiels) ;
 *  - embeddings BLOB Float32 sans colonne dimensions → 768d et 1536d mélangés.
 *
 * `createSyntheticLegacyDb` fabrique une DB de test réaliste (la vraie DB
 * « Koda » vit sur une autre machine et ne doit jamais être requise en CI).
 */
import Database from 'better-sqlite3'
import { mkdirSync } from 'node:fs'
import { dirname } from 'node:path'

/** Tables/colonnes de base v3.34 (hors variantes). */
const LEGACY_BASE_SCHEMA = `
  CREATE TABLE meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
  );

  -- facts : 18 colonnes migrateV1 + 5 ALTER additifs (fact_type, usefulness,
  -- recall_count, used_count, relevance_weight, lifecycle_state)
  CREATE TABLE facts (
    id TEXT PRIMARY KEY,
    fact TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'savoir',
    confidence REAL NOT NULL DEFAULT 0.8,
    source TEXT DEFAULT 'auto-capture',
    tags TEXT DEFAULT '[]',
    agent TEXT DEFAULT 'koda',
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    access_count INTEGER DEFAULT 0,
    last_accessed_at INTEGER,
    superseded INTEGER DEFAULT 0,
    superseded_by TEXT,
    superseded_at INTEGER,
    md_file TEXT,
    md_line INTEGER,
    entity_ids TEXT DEFAULT '[]',
    fact_type TEXT DEFAULT 'semantic',
    usefulness REAL DEFAULT 0,
    recall_count INTEGER DEFAULT 0,
    used_count INTEGER DEFAULT 0,
    relevance_weight REAL DEFAULT 0.5,
    lifecycle_state TEXT DEFAULT 'fresh'
  );
  CREATE INDEX idx_facts_category ON facts(category);
  CREATE INDEX idx_facts_superseded ON facts(superseded);
  CREATE INDEX idx_facts_created ON facts(created_at);
  CREATE INDEX idx_facts_agent ON facts(agent);
  CREATE INDEX idx_facts_type ON facts(fact_type);
  CREATE INDEX idx_facts_relevance ON facts(relevance_weight DESC);
  CREATE INDEX idx_facts_lifecycle ON facts(lifecycle_state);

  CREATE VIRTUAL TABLE facts_fts USING fts5(
    fact, category, tags,
    content='facts',
    content_rowid='rowid'
  );
  CREATE TRIGGER facts_ai AFTER INSERT ON facts BEGIN
    INSERT INTO facts_fts(rowid, fact, category, tags)
    VALUES (new.rowid, new.fact, new.category, new.tags);
  END;
  CREATE TRIGGER facts_ad AFTER DELETE ON facts BEGIN
    INSERT INTO facts_fts(facts_fts, rowid, fact, category, tags)
    VALUES ('delete', old.rowid, old.fact, old.category, old.tags);
  END;
  CREATE TRIGGER facts_au AFTER UPDATE ON facts BEGIN
    INSERT INTO facts_fts(facts_fts, rowid, fact, category, tags)
    VALUES ('delete', old.rowid, old.fact, old.category, old.tags);
    INSERT INTO facts_fts(rowid, fact, category, tags)
    VALUES (new.rowid, new.fact, new.category, new.tags);
  END;

  -- ⚠ pas de colonne dimensions : 768d/1536d indiscernables sans byteLength/4
  CREATE TABLE embeddings (
    fact_id TEXT PRIMARY KEY,
    vector BLOB NOT NULL,
    model TEXT NOT NULL,
    created_at INTEGER NOT NULL,
    FOREIGN KEY (fact_id) REFERENCES facts(id) ON DELETE CASCADE
  );

  CREATE TABLE entities (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL DEFAULT 'concept',
    attributes TEXT DEFAULT '{}',
    created_at INTEGER NOT NULL,
    access_count INTEGER DEFAULT 0
  );
  CREATE INDEX idx_entities_name ON entities(name);
  CREATE INDEX idx_entities_type ON entities(type);

  CREATE TABLE relations (
    id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    relation TEXT NOT NULL,
    weight REAL DEFAULT 1.0,
    context TEXT,
    created_at INTEGER NOT NULL,
    last_accessed_at INTEGER,
    FOREIGN KEY (source_id) REFERENCES entities(id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES entities(id) ON DELETE CASCADE
  );
  CREATE INDEX idx_relations_source ON relations(source_id);
  CREATE INDEX idx_relations_target ON relations(target_id);

  -- chunks/chunks_fts : schéma mort depuis l'origine, présent quand même
  CREATE TABLE chunks (
    id TEXT PRIMARY KEY,
    file_path TEXT NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER DEFAULT 0,
    vector BLOB,
    updated_at INTEGER NOT NULL
  );
  CREATE INDEX idx_chunks_path ON chunks(file_path);
  CREATE VIRTUAL TABLE chunks_fts USING fts5(
    chunk_text, file_path,
    content='chunks',
    content_rowid='rowid'
  );

  CREATE TABLE identity_cache (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at INTEGER NOT NULL
  );

  -- procedures : 14 colonnes de base (failure_reasons ABSENTE — bug B3)
  CREATE TABLE procedures (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    goal TEXT,
    steps TEXT NOT NULL,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    last_success_at INTEGER,
    last_failure_at INTEGER,
    last_updated_at INTEGER NOT NULL,
    avg_duration_ms INTEGER,
    improvements TEXT DEFAULT '[]',
    context TEXT,
    degradation_score REAL DEFAULT 0.0,
    alternative_of TEXT
  );
  CREATE INDEX idx_procedures_name ON procedures(name);
  CREATE INDEX idx_procedures_degradation ON procedures(degradation_score);
  CREATE INDEX idx_procedures_success_rate ON procedures(success_count, failure_count);

  -- FTS procedures SANS triggers (maintenance manuelle dans le legacy)
  CREATE VIRTUAL TABLE procedures_fts USING fts5(
    name, goal, context, gotchas, steps,
    content='procedures',
    content_rowid='rowid'
  );

  CREATE TABLE cluster_members (
    cluster_id TEXT NOT NULL,
    fact_id TEXT NOT NULL,
    PRIMARY KEY (cluster_id, fact_id),
    FOREIGN KEY (cluster_id) REFERENCES facts(id) ON DELETE CASCADE,
    FOREIGN KEY (fact_id) REFERENCES facts(id) ON DELETE CASCADE
  );
  CREATE INDEX idx_cluster_members_fact ON cluster_members(fact_id);

  CREATE TABLE topics (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    keywords TEXT DEFAULT '[]',
    fact_count INTEGER DEFAULT 0,
    first_seen INTEGER NOT NULL,
    last_seen INTEGER NOT NULL,
    access_count INTEGER DEFAULT 0,
    importance_score REAL DEFAULT 0.0,
    parent_topic_id TEXT REFERENCES topics(id) ON DELETE SET NULL,
    embedding BLOB
  );
  CREATE INDEX idx_topics_importance ON topics(importance_score DESC);
  CREATE INDEX idx_topics_parent ON topics(parent_topic_id);

  CREATE TABLE fact_topics (
    fact_id TEXT NOT NULL REFERENCES facts(id) ON DELETE CASCADE,
    topic_id TEXT NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    PRIMARY KEY (fact_id, topic_id)
  );
  CREATE INDEX idx_fact_topics_topic ON fact_topics(topic_id);

  CREATE TABLE observations (
    id TEXT PRIMARY KEY,
    topic TEXT NOT NULL,
    summary TEXT NOT NULL,
    evidence_ids TEXT DEFAULT '[]',
    revision INTEGER DEFAULT 1,
    confidence REAL DEFAULT 0.8,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    last_accessed_at INTEGER,
    access_count INTEGER DEFAULT 0,
    embedding BLOB
  );
  CREATE INDEX idx_obs_topic ON observations(topic);
  CREATE INDEX idx_obs_updated ON observations(updated_at);

  CREATE TABLE wal_buffer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL DEFAULT '',
    role TEXT NOT NULL CHECK(role IN ('user','assistant')),
    content TEXT NOT NULL,
    created_at INTEGER NOT NULL,
    processed INTEGER NOT NULL DEFAULT 0
  );
  CREATE INDEX idx_wal_unprocessed ON wal_buffer(processed, created_at);

  CREATE TABLE self_observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT NOT NULL,
    signal TEXT NOT NULL CHECK(signal IN ('success','correction','frustration','retry')),
    detail TEXT NOT NULL DEFAULT '',
    created_at INTEGER NOT NULL
  );
  CREATE INDEX idx_self_obs_domain ON self_observations(domain, signal);
`

/** Les 13 ALTER de procedural.ts:249-263 (sans failure_reasons — bug B3). */
const PROCEDURE_EXTENSION_ALTERS = [
  "ALTER TABLE procedures ADD COLUMN version INTEGER DEFAULT 1",
  'ALTER TABLE procedures ADD COLUMN evolved_from TEXT',
  'ALTER TABLE procedures ADD COLUMN best_duration_ms INTEGER',
  'ALTER TABLE procedures ADD COLUMN quality_speed REAL DEFAULT 0.5',
  'ALTER TABLE procedures ADD COLUMN quality_reliability REAL DEFAULT 0.5',
  'ALTER TABLE procedures ADD COLUMN quality_elegance REAL DEFAULT 0.5',
  'ALTER TABLE procedures ADD COLUMN quality_safety REAL DEFAULT 0.8',
  'ALTER TABLE procedures ADD COLUMN quality_overall REAL DEFAULT 0.5',
  'ALTER TABLE procedures ADD COLUMN gotchas TEXT',
  'ALTER TABLE procedures ADD COLUMN preferred INTEGER DEFAULT 0',
  'ALTER TABLE procedures ADD COLUMN doc_sources TEXT',
  'ALTER TABLE procedures ADD COLUMN last_verified_at INTEGER',
  'ALTER TABLE procedures ADD COLUMN last_doc_check_at INTEGER',
]

export interface SyntheticLegacyOptions {
  /** Nombre de faits générés (défaut 50, dont des doublons de contenu). */
  factCount?: number
  /** Nombre de procédures (défaut 4). */
  procedureCount?: number
  /** Variante de schéma : colonne synced_to_md présente (sync.ts booté) ou non. */
  withSyncedToMd?: boolean
  /** Variante de schéma : les 13 colonnes additives de procedural.ts. */
  withProcedureExtensions?: boolean
  /** Epoch ms de référence pour des created_at déterministes. */
  baseTimestamp?: number
}

export interface SyntheticLegacySummary {
  path: string
  facts: number
  /** Faits dont le contenu normalisé duplique un fait antérieur du même lot. */
  duplicateFacts: number
  superseded: number
  dormant: number
  embeddings768: number
  embeddings1536: number
  procedures: number
  /** Ids de faits actifs non-superseded, pour les recalls de contrôle. */
  sentinelFactIds: string[]
}

const FR_FACT_TEMPLATES = [
  'Néto préfère les commits signés Hello-Primo pour déclencher le déploiement Vercel',
  'Le serveur Directus est derrière Cloudflare qui bloque python urllib avec une erreur 1010',
  'La clé API Anthropic est stockée dans le fichier api_key avec chmod 600',
  'Le projet JamBoard utilise Firebase jamboard-primo sur le compte hello',
  'Erreur récurrente : le build échoue quand le cache npm est corrompu sur la CI',
  "L'outil Maestro sert aux tests UI iOS avant chaque upload App Store",
  'Le client Transport Rino veut des bons de livraison numériques pour le BTP',
  'Préférence : toujours répondre en français dans les rapports de session',
  "L'app PixConsent gère les consentements droit à l'image pour les photographes",
  'Le pricing AutoCare est fixé à dix-neuf euros via achat intégré annuel',
  'Réunion hebdo équipe Primo le lundi matin à neuf heures heure de Cayenne',
  'Le NAS QNAP héberge les sauvegardes vidéo du studio',
  'Astuce SQLite : VACUUM INTO ne modifie jamais la base source',
  "Le bundle identifier d'Igara est fr.primo-studio.igara depuis le renommage",
  'Bug connu : la colonne synced_to_md manque sur les bases jamais synchronisées',
]

const LEGACY_CATEGORIES = ['savoir', 'erreur', 'outil', 'preference', 'client', 'rh', 'chronologie']

function deterministicVector(dimensions: number, seed: number): Buffer {
  const f32 = new Float32Array(dimensions)
  for (let i = 0; i < dimensions; i++) {
    f32[i] = Math.fround(Math.sin(seed * 31 + i) * 0.5)
  }
  return Buffer.from(f32.buffer, f32.byteOffset, f32.byteLength)
}

/**
 * Crée une memoria.db v3.34 synthétique réaliste : FR, nulls, superseded,
 * dormants, tags JSON invalides, embeddings 768d ET 1536d, procédures.
 * Journal par défaut (pas de WAL) → un seul fichier, hashable avant/après.
 */
export function createSyntheticLegacyDb(path: string, options: SyntheticLegacyOptions = {}): SyntheticLegacySummary {
  const factCount = options.factCount ?? 50
  const procedureCount = options.procedureCount ?? 4
  const withSyncedToMd = options.withSyncedToMd ?? true
  const withProcedureExtensions = options.withProcedureExtensions ?? true
  const base = options.baseTimestamp ?? Date.parse('2026-01-15T10:00:00.000Z')

  mkdirSync(dirname(path), { recursive: true })
  const db = new Database(path)
  try {
    db.pragma('foreign_keys = ON')
    db.exec(LEGACY_BASE_SCHEMA)
    if (withSyncedToMd) {
      db.exec('ALTER TABLE facts ADD COLUMN synced_to_md INTEGER DEFAULT 0')
    }
    if (withProcedureExtensions) {
      for (const alter of PROCEDURE_EXTENSION_ALTERS) db.exec(alter)
    }
    db.prepare('INSERT INTO meta (key, value) VALUES (?, ?)').run('schema_version', '1')

    const summary: SyntheticLegacySummary = {
      path,
      facts: factCount,
      duplicateFacts: 0,
      superseded: 0,
      dormant: 0,
      embeddings768: 0,
      embeddings1536: 0,
      procedures: procedureCount,
      sentinelFactIds: [],
    }

    const insertFact = db.prepare(`
      INSERT INTO facts (
        id, fact, category, confidence, source, tags, agent,
        created_at, updated_at, access_count, last_accessed_at,
        superseded, superseded_by, superseded_at, md_file, md_line,
        entity_ids, fact_type, usefulness, recall_count, used_count,
        relevance_weight, lifecycle_state
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `)
    const insertEmbedding = db.prepare(
      'INSERT INTO embeddings (fact_id, vector, model, created_at) VALUES (?, ?, ?, ?)',
    )

    const insertAll = db.transaction(() => {
      for (let i = 0; i < factCount; i++) {
        const id = `fact_${String(i).padStart(4, '0')}`
        const template = FR_FACT_TEMPLATES[i % FR_FACT_TEMPLATES.length]!
        // Le dernier fait duplique le premier (casse + espaces différents)
        // pour prouver la dédup par contenu NORMALISÉ.
        const isDuplicate = i === factCount - 1 && factCount > 1
        const text = isDuplicate
          ? `  ${FR_FACT_TEMPLATES[0]!.toUpperCase()}   — note 0  `
          : `${template} — note ${i}`
        if (isDuplicate) summary.duplicateFacts++

        const category = LEGACY_CATEGORIES[i % LEGACY_CATEGORIES.length]!
        const createdAt = base + i * 60_000
        const superseded = i % 9 === 0 && !isDuplicate ? 1 : 0
        if (superseded) summary.superseded++
        let lifecycle = 'fresh'
        if (i % 7 === 3) {
          lifecycle = 'dormant'
          summary.dormant++
        } else if (i % 5 === 2) {
          lifecycle = 'settled'
        }
        const nullSource = i % 11 === 4
        const invalidTags = i % 13 === 6
        const tags = nullSource ? null : invalidTags ? 'pas-du-json{' : JSON.stringify(['primo', category])
        const entityIds = i % 3 === 0 ? JSON.stringify([`ent_${i % 5}`]) : '[]'

        insertFact.run(
          id,
          text,
          category,
          0.6 + (i % 5) * 0.08,
          nullSource ? null : 'auto-capture',
          tags,
          'koda',
          createdAt,
          createdAt + 30_000,
          i % 6, // access_count (jeté en V3, fusionné via MAX)
          i % 4 === 0 ? createdAt + 120_000 : null,
          superseded,
          superseded ? `fact_${String(i + 1).padStart(4, '0')}` : null,
          superseded ? createdAt + 90_000 : null,
          null,
          null,
          entityIds,
          i % 8 === 0 ? 'episodic' : 'semantic',
          (i % 10) / 10,
          i % 7,
          i % 3,
          0.5,
          lifecycle,
        )

        if (!superseded && lifecycle !== 'dormant' && !isDuplicate && summary.sentinelFactIds.length < 8) {
          summary.sentinelFactIds.push(id)
        }

        // Embeddings : dims MÉLANGÉES (le piège v3.34 — pas de colonne dimensions)
        if (i % 4 === 1) {
          insertEmbedding.run(id, deterministicVector(768, i), 'nomic-embed-text', createdAt)
          summary.embeddings768++
        } else if (i % 10 === 5) {
          insertEmbedding.run(id, deterministicVector(1536, i), 'text-embedding-3-small', createdAt)
          summary.embeddings1536++
        }
      }

      const procCols = withProcedureExtensions
        ? '(id, name, goal, steps, success_count, failure_count, last_updated_at, improvements, context, quality_overall, gotchas)'
        : '(id, name, goal, steps, success_count, failure_count, last_updated_at, improvements, context)'
      const procPlaceholders = withProcedureExtensions
        ? '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        : '(?, ?, ?, ?, ?, ?, ?, ?, ?)'
      const insertProc = db.prepare(`INSERT INTO procedures ${procCols} VALUES ${procPlaceholders}`)
      for (let p = 0; p < procedureCount; p++) {
        const baseArgs: unknown[] = [
          `proc_${String(p).padStart(3, '0')}`,
          `procédure ${p} — déploiement ${p % 2 === 0 ? 'Vercel' : 'TestFlight'}`,
          p % 3 === 1 ? null : `objectif ${p} : livrer sans casser la prod`,
          p % 3 === 2 ? 'étapes en texte libre (JSON invalide)' : JSON.stringify([`étape A du process ${p}`, `étape B du process ${p}`]),
          p + 2,
          p % 2,
          base + p * 3_600_000,
          '[]',
          p % 2 === 0 ? 'contexte CI Primo' : null,
        ]
        if (withProcedureExtensions) baseArgs.push(0.5 + p * 0.1, p % 2 === 0 ? 'penser au cache npm' : null)
        insertProc.run(...baseArgs)
      }
    })
    insertAll()
    return summary
  } finally {
    db.close()
  }
}
