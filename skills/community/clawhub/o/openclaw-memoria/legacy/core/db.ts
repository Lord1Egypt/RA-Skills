/**
 * Memoria — SQLite Database Layer (Layer 1)
 * 
 * The foundation of Memoria. Manages the SQLite database with:
 * - facts + facts_fts (FTS5 full-text search)
 * - embeddings (768d float vectors as BLOBs)
 * - entities + relations (knowledge graph)
 * - topics + fact_topics (emergent topic system)
 * - observations (living syntheses)
 * - procedures + procedures_fts (how-to memory)
 * - cluster_members (fact → cluster mapping)
 * - identity_cache, meta, chunks
 * 
 * Uses better-sqlite3 for synchronous, fast, zero-dependency SQLite.
 * All migrations auto-run on construction (additive, never destructive).
 * 
 * @example
 * const db = new MemoriaDB("/path/to/workspace");
 * db.storeFact({ id: "f_123", fact: "...", category: "savoir", ... });
 * const results = db.searchFacts("Bureau"); // FTS5 search
 * db.raw.prepare("SELECT ...").all(); // direct SQLite access
 */

import Database from "better-sqlite3";
import path from "path";
import fs from "fs";

const SCHEMA_VERSION = 1;

/**
 * Core fact record stored in SQLite. Every piece of knowledge Memoria captures.
 * 
 * Key fields for contributors:
 * - `fact_type`: "semantic" (durable truth) | "episodic" (dated event) | "cluster" (summary) | "pattern" (consolidated)
 * - `lifecycle_state`: "fresh" → "settled" → "dormant" (controls recall priority, NOT deletion)
 * - `superseded`: 0 = active, 1 = replaced by a newer/better version (superseded_by has the replacement ID)
 * - `tags`: JSON string array, e.g. '["convex","bureau"]'
 * - `entity_ids`: JSON string array of entity IDs linked to this fact
 */
export interface Fact {
  id: string;
  fact: string;
  category: string;
  confidence: number;
  source: string;
  tags: string;           // JSON array
  agent: string;
  created_at: number;
  updated_at: number;
  access_count: number;
  last_accessed_at: number | null;
  superseded: number;     // 0 or 1
  superseded_by: string | null;
  superseded_at: number | null;
  md_file: string | null;
  md_line: number | null;
  entity_ids: string;     // JSON array
  fact_type: "semantic" | "episodic" | "cluster" | "pattern"; // semantic = durable, episodic = dated/contextual, cluster = thematic summary, pattern = consolidated behavioral
  usefulness: number;       // feedback score, higher = more useful
  recall_count: number;     // times recalled in prompts
  used_count: number;       // times actually used in answers
  synced_to_md: number;     // 0 = not synced, 1 = synced, 2 = regenerated
  relevance_weight: number; // 0.0-1.0, calculated from identity context
  lifecycle_state: "fresh" | "settled" | "dormant"; // fresh = new, settled = confirmed, dormant = unused
}

/** Knowledge graph node. Types: person, project, tool, concept, place. */
export interface Entity {
  id: string;
  name: string;
  type: string;           // person|project|tool|concept|place
  attributes: string;     // JSON
  created_at: number;
  access_count: number;
}

/** Knowledge graph edge. Weight increases via Hebbian reinforcement (co-occurrence), decays when unused. */
export interface Relation {
  id: string;
  source_id: string;
  target_id: string;
  relation: string;
  weight: number;
  context: string | null;
  created_at: number;
  last_accessed_at: number | null;
}

/**
 * Main database class. Created once in index.ts and shared with all managers.
 * 
 * Key methods:
 * - `storeFact(fact)` — INSERT OR REPLACE with full column list
 * - `searchFacts(query)` — FTS5 full-text search on fact text
 * - `getActiveFacts()` — all non-superseded facts
 * - `supersedeFact(oldId, newId)` — mark fact as replaced
 * - `raw` — direct better-sqlite3 Database for custom queries
 * 
 * Schema migrations run automatically in constructor (additive only).
 */
export class MemoriaDB {
  /** Direct better-sqlite3 access for custom queries from other modules */
  readonly raw: Database.Database;
  private db: Database.Database;

  constructor(workspaceRoot: string) {
    const dbPath = path.join(workspaceRoot, "memory", "memoria.db");
    const dir = path.dirname(dbPath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    // Auto-migrate from cortex.db if memoria.db doesn't exist or is empty
    const legacyPath = path.join(workspaceRoot, "memory", "cortex.db");
    if (fs.existsSync(legacyPath)) {
      const needsMigration = !fs.existsSync(dbPath) || fs.statSync(dbPath).size < 8192;
      const legacySize = fs.statSync(legacyPath).size;
      if (needsMigration && legacySize > 8192) {
        // Use VACUUM INTO to safely copy WAL-mode DBs (plain cp can lose data)
        try {
          const legacyDb = new Database(legacyPath, { readonly: true });
          legacyDb.exec(`VACUUM INTO '${dbPath.replace(/'/g, "''")}'`);
          legacyDb.close();
        } catch (_e) {
          // Fallback: copy file + WAL + SHM
          fs.copyFileSync(legacyPath, dbPath);
          const walPath = legacyPath + "-wal";
          const shmPath = legacyPath + "-shm";
          if (fs.existsSync(walPath)) fs.copyFileSync(walPath, dbPath + "-wal");
          if (fs.existsSync(shmPath)) fs.copyFileSync(shmPath, dbPath + "-shm");
        }
      }
    }

    this.db = new Database(dbPath);
    this.raw = this.db;
    this.db.pragma("journal_mode = WAL");    // Better concurrent read perf
    this.db.pragma("foreign_keys = ON");
    this.migrate();
  }

  // ─── Schema Migration ───

  private migrate(): void {
    const version = this.getSchemaVersion();
    if (version < 1) this.migrateV1();
    // V2: add fact_type column for semantic/episodic distinction
    this.migrateAddFactType();
    this.migrateAddFeedbackColumns();
    this.migrateAddRelevanceWeight();
    this.migrateAddIdentityCache();
    this.migrateAddLifecycleState();
    this.migrateAddProcedures();
    this.migrateAddClusterMembers();
    this.setSchemaVersion(SCHEMA_VERSION);
  }

  private migrateAddFactType(): void {
    try {
      // Check if column exists
      const cols = this.db.prepare("PRAGMA table_info(facts)").all() as Array<{ name: string }>;
      if (!cols.some(c => c.name === "fact_type")) {
        this.db.exec("ALTER TABLE facts ADD COLUMN fact_type TEXT DEFAULT 'semantic'");
        // Index for filtering
        this.db.exec("CREATE INDEX IF NOT EXISTS idx_facts_type ON facts(fact_type)");
      }
    } catch (_e) { /* column already exists or table not yet created */ }
  }

  /** Migration: add feedback loop columns (usefulness, recall_count, used_count) */
  private migrateAddFeedbackColumns(): void {
    try {
      const cols = this.db.prepare("PRAGMA table_info(facts)").all() as Array<{ name: string }>;
      const colNames = new Set(cols.map(c => c.name));
      if (!colNames.has("usefulness")) {
        this.db.exec("ALTER TABLE facts ADD COLUMN usefulness REAL DEFAULT 0");
      }
      if (!colNames.has("recall_count")) {
        this.db.exec("ALTER TABLE facts ADD COLUMN recall_count INTEGER DEFAULT 0");
      }
      if (!colNames.has("used_count")) {
        this.db.exec("ALTER TABLE facts ADD COLUMN used_count INTEGER DEFAULT 0");
      }
    } catch (_e) { /* columns already exist or table not yet created */ }
  }

  /** Migration: add relevance_weight column for identity-aware prioritization */
  private migrateAddRelevanceWeight(): void {
    try {
      const cols = this.db.prepare("PRAGMA table_info(facts)").all() as Array<{ name: string }>;
      if (!cols.some(c => c.name === "relevance_weight")) {
        this.db.exec("ALTER TABLE facts ADD COLUMN relevance_weight REAL DEFAULT 0.5");
        // Index for sorting by relevance
        this.db.exec("CREATE INDEX IF NOT EXISTS idx_facts_relevance ON facts(relevance_weight DESC)");
      }
    } catch (_e) { /* column already exists or table not yet created */ }
  }

  /** Migration: add identity_cache table for parsed USER.md/COMPANY.md */
  private migrateAddIdentityCache(): void {
    try {
      this.db.exec(`
        CREATE TABLE IF NOT EXISTS identity_cache (
          key TEXT PRIMARY KEY,
          value TEXT NOT NULL,
          updated_at INTEGER NOT NULL
        );
      `);
    } catch (_e) { /* table already exists */ }
  }

  /** Migration: add lifecycle_state for fact evolution (fresh/settled/dormant) */
  private migrateAddLifecycleState(): void {
    try {
      const cols = this.db.prepare("PRAGMA table_info(facts)").all() as Array<{ name: string }>;
      if (!cols.some(c => c.name === "lifecycle_state")) {
        this.db.exec("ALTER TABLE facts ADD COLUMN lifecycle_state TEXT DEFAULT 'fresh'");
        this.db.exec("CREATE INDEX IF NOT EXISTS idx_facts_lifecycle ON facts(lifecycle_state)");
      }
    } catch (_e) { /* column already exists or table not yet created */ }
  }

  /** Migration: add procedures table for procedural memory (Phase 3) */
  private migrateAddProcedures(): void {
    try {
      this.db.exec(`
        CREATE TABLE IF NOT EXISTS procedures (
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
        CREATE INDEX IF NOT EXISTS idx_procedures_name ON procedures(name);
        CREATE INDEX IF NOT EXISTS idx_procedures_degradation ON procedures(degradation_score);
        CREATE INDEX IF NOT EXISTS idx_procedures_success_rate ON procedures(success_count, failure_count);
      `);
    } catch (_e) { /* table already exists */ }
  }

  /** Migration: add cluster_members table to track which facts compose a cluster */
  private migrateAddClusterMembers(): void {
    try {
      this.db.exec(`
        CREATE TABLE IF NOT EXISTS cluster_members (
          cluster_id TEXT NOT NULL,
          fact_id TEXT NOT NULL,
          PRIMARY KEY (cluster_id, fact_id),
          FOREIGN KEY (cluster_id) REFERENCES facts(id) ON DELETE CASCADE,
          FOREIGN KEY (fact_id) REFERENCES facts(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_cluster_members_fact ON cluster_members(fact_id);
      `);
    } catch (_e) { /* table already exists */ }
  }

  private getSchemaVersion(): number {
    try {
      const row = this.db.prepare("SELECT value FROM meta WHERE key = 'schema_version'").get() as { value: string } | undefined;
      return row ? parseInt(row.value, 10) : 0;
    } catch (_e) {
      return 0; // meta table doesn't exist yet
    }
  }

  private setSchemaVersion(v: number): void {
    this.db.prepare("INSERT OR REPLACE INTO meta (key, value) VALUES ('schema_version', ?)").run(String(v));
  }

  private migrateV1(): void {
    this.db.exec(`
      -- Meta table
      CREATE TABLE IF NOT EXISTS meta (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
      );

      -- Facts (mémoire déclarative)
      CREATE TABLE IF NOT EXISTS facts (
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
        fact_type TEXT DEFAULT 'semantic'
      );

      -- FTS5 full-text search on facts
      CREATE VIRTUAL TABLE IF NOT EXISTS facts_fts USING fts5(
        fact, category, tags,
        content='facts',
        content_rowid='rowid'
      );

      -- Triggers to keep FTS in sync
      CREATE TRIGGER IF NOT EXISTS facts_ai AFTER INSERT ON facts BEGIN
        INSERT INTO facts_fts(rowid, fact, category, tags)
        VALUES (new.rowid, new.fact, new.category, new.tags);
      END;

      CREATE TRIGGER IF NOT EXISTS facts_ad AFTER DELETE ON facts BEGIN
        INSERT INTO facts_fts(facts_fts, rowid, fact, category, tags)
        VALUES ('delete', old.rowid, old.fact, old.category, old.tags);
      END;

      CREATE TRIGGER IF NOT EXISTS facts_au AFTER UPDATE ON facts BEGIN
        INSERT INTO facts_fts(facts_fts, rowid, fact, category, tags)
        VALUES ('delete', old.rowid, old.fact, old.category, old.tags);
        INSERT INTO facts_fts(rowid, fact, category, tags)
        VALUES (new.rowid, new.fact, new.category, new.tags);
      END;

      -- Embeddings (vecteurs 768d)
      CREATE TABLE IF NOT EXISTS embeddings (
        fact_id TEXT PRIMARY KEY,
        vector BLOB NOT NULL,
        model TEXT NOT NULL,
        created_at INTEGER NOT NULL,
        FOREIGN KEY (fact_id) REFERENCES facts(id) ON DELETE CASCADE
      );

      -- Knowledge Graph: entities
      CREATE TABLE IF NOT EXISTS entities (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT NOT NULL DEFAULT 'concept',
        attributes TEXT DEFAULT '{}',
        created_at INTEGER NOT NULL,
        access_count INTEGER DEFAULT 0
      );
      CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);
      CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type);

      -- Knowledge Graph: relations
      CREATE TABLE IF NOT EXISTS relations (
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
      CREATE INDEX IF NOT EXISTS idx_relations_source ON relations(source_id);
      CREATE INDEX IF NOT EXISTS idx_relations_target ON relations(target_id);

      -- Chunks (fichiers .md indexés)
      CREATE TABLE IF NOT EXISTS chunks (
        id TEXT PRIMARY KEY,
        file_path TEXT NOT NULL,
        chunk_text TEXT NOT NULL,
        chunk_index INTEGER DEFAULT 0,
        vector BLOB,
        updated_at INTEGER NOT NULL
      );
      CREATE INDEX IF NOT EXISTS idx_chunks_path ON chunks(file_path);

      -- FTS5 on chunks
      CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
        chunk_text, file_path,
        content='chunks',
        content_rowid='rowid'
      );

      CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
        INSERT INTO chunks_fts(rowid, chunk_text, file_path)
        VALUES (new.rowid, new.chunk_text, new.file_path);
      END;

      CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
        INSERT INTO chunks_fts(chunks_fts, rowid, chunk_text, file_path)
        VALUES ('delete', old.rowid, old.chunk_text, old.file_path);
      END;

      CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
        INSERT INTO chunks_fts(chunks_fts, rowid, chunk_text, file_path)
        VALUES ('delete', old.rowid, old.chunk_text, old.file_path);
        INSERT INTO chunks_fts(rowid, chunk_text, file_path)
        VALUES (new.rowid, new.chunk_text, new.file_path);
      END;

      -- Indexes for common queries
      CREATE INDEX IF NOT EXISTS idx_facts_category ON facts(category);
      CREATE INDEX IF NOT EXISTS idx_facts_superseded ON facts(superseded);
      CREATE INDEX IF NOT EXISTS idx_facts_created ON facts(created_at);
      CREATE INDEX IF NOT EXISTS idx_facts_agent ON facts(agent);
      CREATE INDEX IF NOT EXISTS idx_facts_type ON facts(fact_type);
    `);
  }

  // ─── Facts CRUD ───

  storeFact(fact: Omit<Fact, "access_count" | "last_accessed_at" | "superseded" | "superseded_by" | "superseded_at" | "md_file" | "md_line" | "entity_ids" | "usefulness" | "recall_count" | "used_count" | "synced_to_md" | "relevance_weight" | "lifecycle_state"> & Partial<Fact>): Fact {
    const now = Date.now();
    const row: Fact = {
      id: fact.id || `fact_${now}_${Math.random().toString(36).slice(2, 9)}`,
      fact: fact.fact,
      category: fact.category || "savoir",
      confidence: fact.confidence ?? 0.8,
      source: fact.source || "auto-capture",
      tags: fact.tags || "[]",
      agent: fact.agent || "koda",
      created_at: fact.created_at || now,
      updated_at: fact.updated_at || now,
      access_count: fact.access_count ?? 0,
      last_accessed_at: fact.last_accessed_at ?? null,
      superseded: fact.superseded ?? 0,
      superseded_by: fact.superseded_by ?? null,
      superseded_at: fact.superseded_at ?? null,
      md_file: fact.md_file ?? null,
      md_line: fact.md_line ?? null,
      entity_ids: fact.entity_ids || "[]",
      fact_type: fact.fact_type || "semantic",
      usefulness: fact.usefulness ?? 0,
      recall_count: fact.recall_count ?? 0,
      used_count: fact.used_count ?? 0,
      synced_to_md: fact.synced_to_md ?? 0,
      relevance_weight: fact.relevance_weight ?? 0.5,
      lifecycle_state: fact.lifecycle_state ?? "fresh",
    };

    this.db.prepare(`
      INSERT OR REPLACE INTO facts
      (id, fact, category, confidence, source, tags, agent, created_at, updated_at,
       access_count, last_accessed_at, superseded, superseded_by, superseded_at,
       md_file, md_line, entity_ids, fact_type,
       usefulness, recall_count, used_count, synced_to_md, relevance_weight, lifecycle_state)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).run(
      row.id, row.fact, row.category, row.confidence, row.source, row.tags, row.agent,
      row.created_at, row.updated_at, row.access_count, row.last_accessed_at,
      row.superseded, row.superseded_by, row.superseded_at,
      row.md_file, row.md_line, row.entity_ids, row.fact_type,
      row.usefulness, row.recall_count, row.used_count, row.synced_to_md,
      row.relevance_weight, row.lifecycle_state
    );

    return row;
  }

  searchFacts(query: string, limit = 10): Fact[] {
    if (!query || query.trim().length === 0) {
      return this.db.prepare(
        "SELECT * FROM facts WHERE superseded = 0 AND lifecycle_state != 'dormant' ORDER BY updated_at DESC LIMIT ?"
      ).all(limit) as Fact[];
    }

    // Sanitize for FTS5: keep only alphanumeric + spaces, wrap each word in quotes
    const sanitized = query
      .replace(/[^\p{L}\p{N}\s]/gu, " ")  // Remove special chars
      .split(/\s+/)
      .filter(w => w.length > 1)
      .map(w => `"${w}"`)                  // Quote each word
      .join(" OR ");                        // OR between words

    if (!sanitized) {
      return this.db.prepare(
        "SELECT * FROM facts WHERE superseded = 0 ORDER BY updated_at DESC LIMIT ?"
      ).all(limit) as Fact[];
    }

    try {
      return this.db.prepare(`
        SELECT f.* FROM facts f
        JOIN facts_fts fts ON f.rowid = fts.rowid
        WHERE facts_fts MATCH ? AND f.superseded = 0 AND f.lifecycle_state != 'dormant'
        ORDER BY rank
        LIMIT ?
      `).all(sanitized, limit) as Fact[];
    } catch (_e) {
      // Fallback: LIKE search if FTS5 fails
      return this.db.prepare(
        "SELECT * FROM facts WHERE superseded = 0 AND lifecycle_state != 'dormant' AND fact LIKE ? ORDER BY updated_at DESC LIMIT ?"
      ).all(`%${query.slice(0, 100)}%`, limit) as Fact[];
    }
  }

  recentFacts(hours = 24, limit = 10): Fact[] {
    const cutoff = Date.now() - hours * 3600 * 1000;
    return this.db.prepare(
      "SELECT * FROM facts WHERE superseded = 0 AND created_at >= ? ORDER BY created_at DESC LIMIT ?"
    ).all(cutoff, limit) as Fact[];
  }

  getFact(id: string): Fact | undefined {
    return this.db.prepare("SELECT * FROM facts WHERE id = ?").get(id) as Fact | undefined;
  }

  supersedeFact(oldId: string, newId: string): void {
    const now = Date.now();
    this.db.prepare(
      "UPDATE facts SET superseded = 1, superseded_by = ?, superseded_at = ?, updated_at = ? WHERE id = ?"
    ).run(newId, now, now, oldId);
  }

  enrichFact(id: string, newText: string, newConfidence?: number): void {
    const now = Date.now();
    const existing = this.getFact(id);
    if (!existing) return;
    const confidence = newConfidence ? Math.max(existing.confidence, newConfidence) : existing.confidence;
    this.db.prepare(
      "UPDATE facts SET fact = ?, confidence = ?, updated_at = ? WHERE id = ?"
    ).run(newText, confidence, now, id);
  }

  /** Get frequently accessed facts (hot tier — "learned by heart") */
  hotFacts(minAccess: number = 5, staleDays: number = 30, limit: number = 5): Fact[] {
    const cutoff = Date.now() - staleDays * 24 * 60 * 60 * 1000;
    return this.db.prepare(
      `SELECT * FROM facts WHERE superseded = 0 AND lifecycle_state != 'dormant' AND access_count >= ? 
       AND COALESCE(last_accessed_at, updated_at) >= ?
       ORDER BY access_count DESC LIMIT ?`
    ).all(minAccess, cutoff, limit) as Fact[];
  }

  trackAccess(ids: string[]): void {
    const now = Date.now();
    const stmt = this.db.prepare(
      "UPDATE facts SET access_count = access_count + 1, last_accessed_at = ? WHERE id = ?"
    );
    const tx = this.db.transaction(() => {
      for (const id of ids) stmt.run(now, id);
    });
    tx();
  }

  // ─── Stats ───

  stats(): { total: number; active: number; superseded: number; categories: Record<string, number> } {
    const total = (this.db.prepare("SELECT COUNT(*) as c FROM facts").get() as { c: number }).c;
    const active = (this.db.prepare("SELECT COUNT(*) as c FROM facts WHERE superseded = 0").get() as { c: number }).c;
    const cats = this.db.prepare(
      "SELECT category, COUNT(*) as c FROM facts WHERE superseded = 0 GROUP BY category"
    ).all() as Array<{ category: string; c: number }>;
    
    const categories: Record<string, number> = {};
    for (const row of cats) categories[row.category] = row.c;
    
    return { total, active, superseded: total - active, categories };
  }

  // ─── Entities CRUD ───

  storeEntity(entity: Omit<Entity, "created_at" | "access_count"> & Partial<Entity>): Entity {
    const now = Date.now();
    const row: Entity = {
      id: entity.id || `ent_${now}_${Math.random().toString(36).slice(2, 9)}`,
      name: entity.name,
      type: entity.type || "concept",
      attributes: entity.attributes || "{}",
      created_at: entity.created_at || now,
      access_count: entity.access_count ?? 0,
    };

    this.db.prepare(`
      INSERT OR REPLACE INTO entities (id, name, type, attributes, created_at, access_count)
      VALUES (?, ?, ?, ?, ?, ?)
    `).run(row.id, row.name, row.type, row.attributes, row.created_at, row.access_count);

    return row;
  }

  findEntityByName(name: string): Entity | undefined {
    return this.db.prepare(
      "SELECT * FROM entities WHERE LOWER(name) = LOWER(?)"
    ).get(name) as Entity | undefined;
  }

  /** Return all entity names (lowercased) for fast in-text matching */
  allEntityNames(): string[] {
    const rows = this.db.prepare("SELECT DISTINCT LOWER(name) as name FROM entities").all() as { name: string }[];
    return rows.map(r => r.name);
  }

  /** Find facts linked to any of the given entity IDs */
  findFactsByEntityIds(entityIds: string[], limit = 10): Fact[] {
    if (entityIds.length === 0) return [];
    // entity_ids is stored as JSON array string, e.g. '["ent_123","ent_456"]'
    const placeholders = entityIds.map(() => "entity_ids LIKE ?").join(" OR ");
    const params = entityIds.map(id => `%${id}%`);
    return this.db.prepare(
      `SELECT * FROM facts WHERE status = 'active' AND (${placeholders}) ORDER BY updated_at DESC LIMIT ?`
    ).all(...params, limit) as Fact[];
  }

  // ─── Relations CRUD ───

  storeRelation(rel: Omit<Relation, "created_at" | "last_accessed_at"> & Partial<Relation>): Relation {
    const now = Date.now();
    const row: Relation = {
      id: rel.id || `rel_${now}_${Math.random().toString(36).slice(2, 9)}`,
      source_id: rel.source_id,
      target_id: rel.target_id,
      relation: rel.relation,
      weight: rel.weight ?? 1.0,
      context: rel.context ?? null,
      created_at: rel.created_at || now,
      last_accessed_at: rel.last_accessed_at ?? null,
    };

    this.db.prepare(`
      INSERT OR REPLACE INTO relations
      (id, source_id, target_id, relation, weight, context, created_at, last_accessed_at)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).run(row.id, row.source_id, row.target_id, row.relation, row.weight, row.context, row.created_at, row.last_accessed_at);

    return row;
  }

  getRelationsFrom(entityId: string, minWeight = 0.1): Relation[] {
    return this.db.prepare(
      "SELECT * FROM relations WHERE source_id = ? AND weight >= ? ORDER BY weight DESC"
    ).all(entityId, minWeight) as Relation[];
  }

  getRelationsTo(entityId: string, minWeight = 0.1): Relation[] {
    return this.db.prepare(
      "SELECT * FROM relations WHERE target_id = ? AND weight >= ? ORDER BY weight DESC"
    ).all(entityId, minWeight) as Relation[];
  }

  reinforceRelation(id: string, boost = 0.1): void {
    const now = Date.now();
    this.db.prepare(
      "UPDATE relations SET weight = weight + ?, last_accessed_at = ? WHERE id = ?"
    ).run(boost, now, id);
  }

  // ─── Bulk import ───

  importFacts(facts: Array<Omit<Fact, "access_count" | "last_accessed_at" | "superseded" | "superseded_by" | "superseded_at" | "md_file" | "md_line" | "entity_ids"> & Partial<Fact>>): number {
    const tx = this.db.transaction(() => {
      let count = 0;
      for (const fact of facts) {
        this.storeFact(fact);
        count++;
      }
      return count;
    });
    return tx();
  }

  // ─── Identity Cache ───

  /** Store identity cache (JSON stringified) */
  storeIdentityCache(key: string, value: string): void {
    const now = Date.now();
    this.db.prepare("INSERT OR REPLACE INTO identity_cache (key, value, updated_at) VALUES (?, ?, ?)").run(key, value, now);
  }

  /** Get identity cache */
  getIdentityCache(key: string): string | null {
    const row = this.db.prepare("SELECT value FROM identity_cache WHERE key = ?").get(key) as { value: string } | undefined;
    return row?.value ?? null;
  }

  // ─── Close ───

  close(): void {
    this.db.close();
  }
}
