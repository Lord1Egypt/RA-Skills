/**
 * OpenClaw Memory System v1
 * Storage Layer - SQLite + Vector Search
 * 
 * Local-first, Ollama-compatible memory system
 * Forked from Engram patterns, optimized for OpenClaw
 */

import Database from 'better-sqlite3';
import { v4 as uuidv4 } from 'uuid';
import path from 'path';

// Types
export type MemoryType = 'episodic' | 'semantic' | 'procedural';

// ============================================================================
// PHASE 1.4 RETRIEVAL FEATURES - IMPORTS
// ============================================================================

import { hybridSearch } from '../retrieval/hybrid.js';
import { filterMemories, scoreForQuestionType } from '../retrieval/filter.js';
import { normalizeEntities, createAliasStore, type EntityAliasStore } from '../extractors/normalize.js';
import { extractTemporalMetadata } from '../extractors/temporal-metadata.js';
import { extractDates, detectTemporalQuery } from '../extractors/temporal.js';
import { EntityStore, EntityType } from './entity-store.js';
import { RelationshipStore } from './relationship-store.js';
import { extractRelationships, inferEntityType } from '../extractors/relationships.js';

// Alias store for spelling variants and entity aliases
let aliasStore: EntityAliasStore | null = null;

function getAliasStore(): EntityAliasStore {
  if (!aliasStore) {
    aliasStore = createAliasStore();
  }
  return aliasStore;
}

// ============================================================================
// ENTITY EXTRACTION (simple version for storage)
// ============================================================================

function extractEntitiesFromText(text: string): string[] {
  const entities: string[] = [];
  const patterns = [
    'Phillip', 'KakāpōHiko', 'Kakāpō', 'Hiko',
    'Elev8Advisory', 'BrandForge', 'Muninn', 'OpenClaw',
    'Sammy Clemens', 'Charlie Babbage', 'Donna Paulsen',
    'Brisbane', 'Australia', 'React', 'Node.js', 'PostgreSQL',
    'SQLite', 'Ollama', 'Stripe'
  ];
  
  for (const p of patterns) {
    if (text.toLowerCase().includes(p.toLowerCase())) {
      entities.push(p);
    }
  }
  
  return [...new Set(entities)];
}

// ============================================================================
// QUERY EXPANSION FOR SPELLING VARIANTS
// ============================================================================

/**
 * Expand query with spelling variants (UK↔US English)
 */
function expandQueryWithVariants(query: string): string[] {
  const expandedQueries: string[] = [query];
  
  // Common spelling variants to check
  const variantPairs = [
    ['colour', 'color'],
    ['flavour', 'flavor'],
    ['honour', 'honor'],
    ['organise', 'organize'],
    ['realise', 'realize'],
    ['recognise', 'recognize'],
    ['analyse', 'analyze'],
    ['centre', 'center'],
    ['theatre', 'theater'],
    ['defence', 'defense'],
    ['offence', 'offense'],
    ['licence', 'license'],
    ['programme', 'program'],
    ['behaviour', 'behavior'],
  ];
  
  for (const [uk, us] of variantPairs) {
    // If query contains UK form, add US version
    if (query.toLowerCase().includes(uk)) {
      expandedQueries.push(query.replace(new RegExp(uk, 'gi'), us));
    }
    // If query contains US form, add UK version  
    if (query.toLowerCase().includes(us)) {
      expandedQueries.push(query.replace(new RegExp(us, 'gi'), uk));
    }
  }
  
  return [...new Set(expandedQueries)];
}

// Import audit types
import type { StalenessInfo } from './audit.js';

export interface Memory {
  id: string;
  type: MemoryType;
  content: string;
  resolved_content?: string;      // Phase 1.6: Temporal-resolved content
  title?: string;
  summary?: string;
  entities: string[];
  topics: string[];
  embedding: number[];
  salience: number;
  timestamp: string;              // When the memory occurred
  sessionId?: string;             // Session/conversation ID
  ttl?: number;                   // Time-to-live in seconds
  user_id?: string;               // Multi-tenancy: user namespace
  created_at: string;
  updated_at: string;
  deleted_at?: string;
  
  // === Phase 1.4 Audit Extension Fields ===
  valid_at?: string;              // When memory becomes valid (future content)
  invalid_at?: string;            // When memory was superseded
  last_confirmed_at?: string;     // Last verification timestamp
  contradiction_flags?: string[]; // IDs of conflicting memories
}

export interface Procedure {
  id: string;
  title: string;
  description?: string;
  steps: ProcedureStep[];
  version: number;
  success_count: number;
  failure_count: number;
  is_reliable: boolean;
  evolution_log: EvolutionEvent[];
  created_at: string;
  updated_at: string;
}

export interface ProcedureStep {
  id: string;
  order: number;
  description: string;
  expected_outcome?: string;
}

export interface EvolutionEvent {
  version: number;
  trigger: 'failure' | 'success_pattern' | 'manual';
  change: string;
  timestamp: string;
}

export interface Entity {
  name: string;
  memory_count: number;
  last_seen: string;
}

export interface MemoryEdge {
  id: string;
  source_id: string;
  target_id: string;
  relationship: string;
  created_at: string;
}

export interface VaultStats {
  total: number;
  byType: Record<MemoryType, number>;
  entities: number;
  edges: number;
  procedures: number;
}

// Embedding function - supports Ollama (local), OpenAI, Gemini, or zero-vector fallback (cloud)
export async function generateEmbedding(text: string): Promise<number[]> {
  const mode = process.env.EMBEDDING_MODE || 'ollama';
  
  // Zero-vector fallback for cloud deployments without Ollama
  if (mode === 'zero') {
    // Return a deterministic pseudo-embedding based on text hash
    // This enables basic keyword matching without semantic search
    const hash = text.split('').reduce((acc, char) => {
      return ((acc << 5) - acc + char.charCodeAt(0)) | 0;
    }, 0);
    const embedding = new Array(768).fill(0);
    // Add some variation based on hash to differentiate texts slightly
    for (let i = 0; i < 10; i++) {
      embedding[i] = ((hash >> (i * 3)) & 0x7) / 10 - 0.4; // small values -0.4 to 0.3
    }
    return embedding;
  }
  
  // Gemini embeddings (Google Generative AI)
  if (mode === 'gemini') {
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      throw new Error('GEMINI_API_KEY required for EMBEDDING_MODE=gemini');
    }
    
    // Use Gemini's embedding model
    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key=${apiKey}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'models/gemini-embedding-001',
        content: {
          parts: [{ text }]
        },
        taskType: 'RETRIEVAL_DOCUMENT'
      })
    });
    
    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Gemini embedding failed (${response.status}): ${error}`);
    }
    
    const data = await response.json() as { embedding: { values: number[] } };
    return data.embedding.values;
  }
  
  // OpenAI embeddings
  if (mode === 'openai') {
    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) {
      throw new Error('OPENAI_API_KEY required for EMBEDDING_MODE=openai');
    }
    const response = await fetch('https://api.openai.com/v1/embeddings', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: 'text-embedding-3-small',
        input: text
      })
    });
    if (!response.ok) {
      throw new Error(`OpenAI embedding failed: ${response.statusText}`);
    }
    const data = await response.json() as { data: Array<{ embedding: number[] }> };
    return data.data[0].embedding;
  }
  
  // Default: Ollama (local)
  const response = await fetch('http://localhost:11434/api/embeddings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'nomic-embed-text',
      prompt: text
    })
  });
  
  if (!response.ok) {
    // Fallback to zero-vector if Ollama not available
    console.warn(`Ollama embedding failed (${response.statusText}), falling back to zero-vector`);
    return new Array(768).fill(0);
  }
  
  const data = await response.json() as { embedding: number[] };
  return data.embedding;
}
function cosineSimilarity(a: number[], b: number[]): number {
  if (a.length !== b.length) return 0;
  
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;
  
  for (let i = 0; i < a.length; i++) {
    dotProduct += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

export class MemoryStore {
  private db: Database.Database;
  private entityStore: EntityStore;
  private relationshipStore: RelationshipStore;

  constructor(dbPath?: string) {
    const defaultPath = path.join(process.cwd(), 'openclaw-memory.db');
    this.db = new Database(dbPath || defaultPath);
    this.entityStore = new EntityStore(this.db);
    this.relationshipStore = new RelationshipStore(this.db);
    this.init();
  }

  /**
   * Get the entity store for direct access
   */
  getEntityStore(): EntityStore {
    return this.entityStore;
  }

  /**
   * Get the relationship store for direct access
   */
  getRelationshipStore(): RelationshipStore {
    return this.relationshipStore;
  }
  
  private init(): void {
    // Enable vector similarity search using simple implementation
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS memories (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL CHECK(type IN ('episodic', 'semantic', 'procedural')),
        content TEXT NOT NULL,
        resolved_content TEXT,
        title TEXT,
        summary TEXT,
        entities TEXT DEFAULT '[]',
        topics TEXT DEFAULT '[]',
        embedding BLOB,
        salience REAL DEFAULT 0.5,
        timestamp TEXT,
        session_id TEXT,
        ttl INTEGER,
        user_id TEXT DEFAULT 'default',
        created_at TEXT DEFAULT (datetime('now')),
        updated_at TEXT DEFAULT (datetime('now')),
        deleted_at TEXT
      );

      CREATE INDEX IF NOT EXISTS idx_memories_timestamp ON memories(timestamp);
      CREATE INDEX IF NOT EXISTS idx_memories_session ON memories(session_id);
      CREATE INDEX IF NOT EXISTS idx_memories_user ON memories(user_id);
      
      CREATE TABLE IF NOT EXISTS entities (
        name TEXT PRIMARY KEY,
        memory_count INTEGER DEFAULT 0,
        last_seen TEXT DEFAULT (datetime('now'))
      );
      
      CREATE TABLE IF NOT EXISTS edges (
        id TEXT PRIMARY KEY,
        source_id TEXT NOT NULL,
        target_id TEXT NOT NULL,
        relationship TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (source_id) REFERENCES memories(id) ON DELETE CASCADE,
        FOREIGN KEY (target_id) REFERENCES memories(id) ON DELETE CASCADE
      );
      
      CREATE TABLE IF NOT EXISTS procedures (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        steps TEXT DEFAULT '[]',
        version INTEGER DEFAULT 1,
        success_count INTEGER DEFAULT 0,
        failure_count INTEGER DEFAULT 0,
        is_reliable INTEGER DEFAULT 0,
        evolution_log TEXT DEFAULT '[]',
        created_at TEXT DEFAULT (datetime('now')),
        updated_at TEXT DEFAULT (datetime('now'))
      );
      
      CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(type);
      CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at);
      CREATE INDEX IF NOT EXISTS idx_memories_deleted ON memories(deleted_at);
      CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);
      CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_id);
      CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_id);
      
      -- TEMPORAL INDEX: Store extracted dates for fast temporal queries
      CREATE TABLE IF NOT EXISTS temporal_index (
        id TEXT PRIMARY KEY,
        memory_id TEXT NOT NULL,
        date TEXT NOT NULL,           -- ISO format date (YYYY-MM-DD)
        date_type TEXT NOT NULL,      -- 'absolute', 'relative', 'range'
        granularity TEXT NOT NULL,    -- 'hour', 'day', 'week', 'month', 'year'
        original_text TEXT NOT NULL,  -- Original text that was parsed
        confidence REAL NOT NULL,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (memory_id) REFERENCES memories(id) ON DELETE CASCADE
      );
      
      CREATE INDEX IF NOT EXISTS idx_temporal_memory ON temporal_index(memory_id);
      CREATE INDEX IF NOT EXISTS idx_temporal_date ON temporal_index(date);
    `);
    
    console.log('📦 Memory database initialized');
  }
  
  // Memory CRUD
  async remember(
    content: string,
    type: MemoryType = 'semantic',
    options: {
      title?: string;
      summary?: string;
      entities?: string[];
      topics?: string[];
      salience?: number;
      timestamp?: string;      // When the memory occurred (defaults to now)
      sessionId?: string;     // Session/conversation ID
      ttl?: number;            // Time-to-live in seconds
      sessionDate?: Date | string;  // Reference date for temporal resolution
      user_id?: string;        // Multi-tenancy: user namespace
    } = {}
  ): Promise<Memory> {
    const id = `m_${uuidv4().slice(0, 8)}`;
    const embedding = await generateEmbedding(content);
    const now = new Date().toISOString();
    const timestamp = options.timestamp || now;
    const userId = options.user_id || 'default';

    // ========================================================================
    // TEMPORAL RESOLUTION: Convert relative dates to absolute
    // ========================================================================
    
    let resolvedContent: string | null = null;
    const temporalMeta = extractTemporalMetadata(content, options.sessionDate || timestamp);
    
    if (temporalMeta?.eventTime && temporalMeta.confidence > 0.5) {
      // Prepend resolved date: "[2023-05-07] I went to the LGBTQ group yesterday"
      resolvedContent = `[${temporalMeta.eventTime}] ${content}`;
    }

    // ========================================================================
    // PHASE 1.4: ENTITY NORMALIZATION
    // ========================================================================

    // Extract entities if not provided
    const extractedEntities = options.entities || extractEntitiesFromText(content);

    // Create properly typed entities for normalization
    const entitiesForNormalization = extractedEntities.map(e => ({
      text: e,
      type: 'concept' as const,
      confidence: 0.8,
      context: '',
    }));

    // Normalize entities and store aliases
    const normalized = await normalizeEntities(content, entitiesForNormalization);

    // Store aliases for retrieval
    const aliasStore = getAliasStore();
    for (const norm of normalized) {
      for (const alias of norm.aliases) {
        aliasStore.addAlias(norm.canonical, alias);
      }
    }

    // Get canonical entity names
    const canonicalEntities = [...new Set(normalized.map(n => n.canonical))];

    // Convert embedding to base64 for storage
    const embeddingBuffer = Buffer.from(new Float32Array(embedding).buffer);

    const stmt = this.db.prepare(`
      INSERT INTO memories (id, type, content, resolved_content, title, summary, entities, topics, embedding, salience, timestamp, session_id, ttl, user_id, created_at, updated_at)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);
    
    stmt.run(
      id,
      type,
      content,
      resolvedContent,  // Resolved date content or null
      options.title || null,
      options.summary || null,
      JSON.stringify(canonicalEntities),
      JSON.stringify(options.topics || []),
      embeddingBuffer,
      options.salience || 0.5,
      timestamp,
      options.sessionId || null,
      options.ttl || null,
      userId,
      now,
      now
    );
    
    // Update entity counts (use canonical names)
    if (canonicalEntities.length) {
      const entityStmt = this.db.prepare(`
        INSERT INTO entities (name, memory_count, last_seen)
        VALUES (?, 1, ?)
        ON CONFLICT(name) DO UPDATE SET
          memory_count = memory_count + 1,
          last_seen = ?
      `);
      
      for (const entity of canonicalEntities) {
        entityStmt.run(entity, now, now);
      }
    }

    // ========================================================================
    // PHASE 1.7: KNOWLEDGE GRAPH CONSTRUCTION
    // Register entities and extract relationships
    // ========================================================================

    // Register entities in EntityStore with inferred types
    for (const entityName of canonicalEntities) {
      const entityType = inferEntityType(entityName) as EntityType;
      this.entityStore.addEntity({
        name: entityName,
        type: entityType,
        aliases: []
      });
    }

    // Extract relationships from content
    const knownEntities = new Map<string, string>();
    for (const entity of canonicalEntities) {
      knownEntities.set(entity.toLowerCase(), entity);
    }
    
    const extractedRels = extractRelationships(content, knownEntities);
    
    // Store relationships in knowledge graph
    for (const rel of extractedRels) {
      // Find or create entity IDs for source and target
      let sourceEntity = this.entityStore.findEntity(rel.source);
      if (!sourceEntity) {
        sourceEntity = this.entityStore.addEntity({
          name: rel.source,
          type: inferEntityType(rel.source) as EntityType,
          aliases: []
        });
      }
      
      // For numeric targets (e.g., "$2000/month"), use a placeholder
      let targetEntity = this.entityStore.findEntity(rel.target);
      if (!targetEntity && !rel.value) {
        targetEntity = this.entityStore.addEntity({
          name: rel.target,
          type: inferEntityType(rel.target) as EntityType,
          aliases: []
        });
      }
      
      // Store the relationship
      if (sourceEntity && (targetEntity || rel.value)) {
        this.relationshipStore.addRelationship({
          source: sourceEntity.id,
          target: targetEntity?.id || rel.target,
          type: rel.type,
          value: rel.value,
          timestamp: now,
          sessionId: options.sessionId || 'default',
          confidence: rel.confidence
        });
      }
    }
    
    // ==========================================================================
    // TEMPORAL INDEX: Store all extracted dates for fast temporal queries
    // ==========================================================================
    
    // Use session date as reference if provided, otherwise use timestamp
    const temporalRefDate = options.sessionDate 
      ? (typeof options.sessionDate === 'string' ? new Date(options.sessionDate) : options.sessionDate)
      : new Date(timestamp);
    
    const extractedTemporalDates = extractDates(content, temporalRefDate);
    
    if (extractedTemporalDates.length > 0) {
      const temporalStmt = this.db.prepare(`
        INSERT INTO temporal_index (id, memory_id, date, date_type, granularity, original_text, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?)
      `);
      
      for (const td of extractedTemporalDates) {
        const tdId = `t_${uuidv4().slice(0, 8)}`;
        const dateStr = td.date.toISOString().split('T')[0]; // YYYY-MM-DD
        
        temporalStmt.run(
          tdId,
          id,
          dateStr,
          td.dateType,
          td.granularity,
          td.originalText,
          td.confidence
        );
        
        // If it's a range, also store the end date
        if (td.endDate) {
          const endDateStr = td.endDate.toISOString().split('T')[0];
          const tdIdEnd = `t_${uuidv4().slice(0, 8)}`;
          temporalStmt.run(
            tdIdEnd,
            id,
            endDateStr,
            td.dateType,
            td.granularity,
            td.originalText + ' (end)',
            td.confidence
          );
        }
      }
    }
    
    return this.getMemory(id)!;
  }
  
  getMemory(id: string): Memory | null {
    const stmt = this.db.prepare('SELECT * FROM memories WHERE id = ? AND deleted_at IS NULL');
    const row = stmt.get(id) as any;

    if (!row) return null;

    return {
      ...row,
      sessionId: row.session_id,  // Map snake_case to camelCase
      entities: JSON.parse(row.entities || '[]'),
      topics: JSON.parse(row.topics || '[]'),
      embedding: Array.from(new Float32Array(row.embedding?.buffer || new ArrayBuffer(0)))
    };
  }
  
  async recall(
    context: string,
    options: {
      types?: MemoryType[];
      entities?: string[];
      topics?: string[];
      limit?: number;
      user_id?: string;  // Multi-tenancy: filter by user
    } = {}
  ): Promise<Memory[]> {
    // P8.1: Increased retrieval budget (Engram uses K=25)
    // Default limit increased from 10 to 20 for better multi-hop coverage
    const limit = options.limit || 20;

    // ========================================================================
    // P8.2: TEMPORAL EVOLUTION DETECTION
    // Detect queries asking about changes over time
    // ========================================================================

    const isTemporalEvolutionQuery = /how (did|has|does).*(change|evolve|progress|develop|vary)/i.test(context) ||
      /over (time|the sessions|the (last|past) \w+)/i.test(context) ||
      /what (was|were) .*(before|initially|originally|started)/i.test(context) ||
      /history|timeline|chronolog/i.test(context);

    // ========================================================================
    // P8: MULTI-HOP DETECTION - Entity-centric retrieval
    // ========================================================================

    const isMultiHopQuery = /^(would|could|should|what (would|could)|is .+ likely)/i.test(context) ||
      /likely|consider|pursue|interested|would be|if she|if he|if they/i.test(context);

    if (isMultiHopQuery) {
      // Use entity-centric retrieval for multi-hop reasoning
      const entityResults = await this.recallEntityContext(context, { limit, user_id: options.user_id });
      if (entityResults.length > 0) {
        return entityResults;
      }
    }

    // ========================================================================
    // PHASE 1.6: TEMPORAL QUERY RESOLUTION
    // ========================================================================

    // Extract temporal reference from query (e.g., "on Tuesday", "yesterday")
    const temporalQuery = extractTemporalMetadata(context, new Date());

    // Get all non-deleted memories, filtered by user if specified
    const targetUserId = options.user_id;
    let memories;
    if (targetUserId) {
      memories = this.db.prepare(`
        SELECT * FROM memories WHERE deleted_at IS NULL AND (user_id = ? OR user_id = 'default')
      `).all(targetUserId) as any[];
    } else {
      memories = this.db.prepare(`
        SELECT * FROM memories WHERE deleted_at IS NULL
      `).all() as any[];
    }

    // Filter by temporal reference if present with high confidence
    if (temporalQuery.eventTime && temporalQuery.confidence > 0.7) {
      const targetDate = temporalQuery.eventTime; // YYYY-MM-DD format

      // Try to find memories using the temporal_index table first
      const temporalMatches = this.db.prepare(`
        SELECT DISTINCT m.* FROM memories m
        INNER JOIN temporal_index t ON m.id = t.memory_id
        WHERE t.date = ? AND m.deleted_at IS NULL
      `).all(targetDate) as any[];

      // If we have temporal index matches, use those
      if (temporalMatches.length > 0) {
        console.log(`Temporal index found ${temporalMatches.length} memories for "${targetDate}"`);
        const parsed = temporalMatches.map(row => ({
          ...row,
          sessionId: row.session_id,
          entities: JSON.parse(row.entities || '[]'),
          topics: JSON.parse(row.topics || '[]'),
          embedding: Array.from(new Float32Array(row.embedding?.buffer || new ArrayBuffer(0)))
        }));
        return parsed.slice(0, limit);
      }

      // Fallback to content-based filtering
      memories = memories.filter(m => {
        // Check resolved_content first (contains [YYYY-MM-DD] prefix)
        if (m.resolved_content && m.resolved_content.includes(`[${targetDate}]`)) {
          return true;
        }
        // Check timestamp field
        if (m.timestamp && m.timestamp.startsWith(targetDate)) {
          return true;
        }
        // Check created_at for episodic memories
        if (m.type === 'episodic' && m.created_at && m.created_at.startsWith(targetDate)) {
          return true;
        }
        return false;
      });

      // If temporal filter found memories, return them directly
      if (memories.length > 0) {
        const parsed = memories.map(row => ({
          ...row,
          sessionId: row.session_id,  // Map snake_case to camelCase
          entities: JSON.parse(row.entities || '[]'),
          topics: JSON.parse(row.topics || '[]'),
          embedding: Array.from(new Float32Array(row.embedding?.buffer || new ArrayBuffer(0)))
        }));
        return parsed.slice(0, limit);
      }
      // If no exact matches, fall through to semantic search
      // but log that we tried temporal filtering
      console.log(`Temporal filter for "${targetDate}" found no exact matches, falling back to semantic search`);
    }
    
    // ==========================================================================
    // TEMPORAL QUERY DETECTION: Handle "When did..." questions
    // And also handle queries with explicit dates like "in June 2022"
    // ==========================================================================
    
    const temporalQueryDetection = detectTemporalQuery(context);
    
    // Also try to extract any dates from the query directly
    const queryDates = extractDates(context);
    
    if (temporalQueryDetection.isTemporal || queryDates.length > 0) {
      // This is a temporal question OR has dates in the query
      // Extract key entities from the query to narrow down temporal search
      const queryEntities = extractEntitiesFromText(context);
      
      // If we have explicit dates in the query, prioritize temporal_index
      if (queryDates.length > 0) {
        const dateStrs = queryDates.map(d => {
          const iso = d.date.toISOString ? d.date.toISOString() : String(d.date);
          return iso.split('T')[0];
        });
        
        // Search using temporal_index
        const temporalMemories: any[] = [];
        for (const dateStr of dateStrs) {
          // Try exact date match
          const exactMatches = this.db.prepare(`
            SELECT DISTINCT m.* FROM memories m
            INNER JOIN temporal_index t ON m.id = t.memory_id
            WHERE t.date = ? AND m.deleted_at IS NULL
          `).all(dateStr) as any[];
          
          for (const m of exactMatches) {
            const exists = temporalMemories.find(x => x.id === m.id);
            if (!exists) temporalMemories.push(m);
          }
          
          // Try date range match (for month/year queries)
          if (queryDates[0].granularity === 'month' || queryDates[0].granularity === 'year') {
            const rangeStart = queryDates[0].date;
            const rangeEnd = queryDates[0].endDate || queryDates[0].date;
            
            const rangeMatches = this.db.prepare(`
              SELECT DISTINCT m.* FROM memories m
              INNER JOIN temporal_index t ON m.id = t.memory_id
              WHERE t.date >= ? AND t.date <= ? AND m.deleted_at IS NULL
            `).all(
              rangeStart.toISOString().split('T')[0],
              rangeEnd.toISOString().split('T')[0]
            ) as any[];
            
            for (const m of rangeMatches) {
              const exists = temporalMemories.find(x => x.id === m.id);
              if (!exists) temporalMemories.push(m);
            }
          }
        }
        
        if (temporalMemories.length > 0) {
          console.log(`Temporal index found ${temporalMemories.length} memories for dates: ${dateStrs.join(', ')}`);
          
          const parsed = temporalMemories.slice(0, limit).map(row => ({
            ...row,
            sessionId: row.session_id,
            entities: JSON.parse(row.entities || '[]'),
            topics: JSON.parse(row.topics || '[]'),
            embedding: Array.from(new Float32Array(row.embedding?.buffer || new ArrayBuffer(0)))
          }));
          
          return this.recallInternal(context, parsed, limit);
        }
        
        // Fallback to content search if no temporal_index matches
        console.log(`Temporal index had no matches for dates: ${dateStrs.join(', ')}, trying content search`);
      }
      
      // Try entity-based search for "When did X..." type questions
      if (queryEntities.length > 0) {
        const entityPlaceholders = queryEntities.map(() => '?').join(',');
        
        // Get all memories with the entity
        let entityMemories = this.db.prepare(`
          SELECT * FROM memories 
          WHERE deleted_at IS NULL 
          AND (${queryEntities.map(() => 'content LIKE ?').join(' OR ')})
        `).all(...queryEntities.map(e => `%${e}%`)) as any[];
        
        if (entityMemories.length > 0) {
          // Sort by temporal relevance (memories with temporal metadata first)
          entityMemories.sort((a, b) => {
            const aHasTemp = a.resolved_content ? 1 : 0;
            const bHasTemp = b.resolved_content ? 1 : 0;
            return bHasTemp - aHasTemp;
          });
          
          const parsed = entityMemories.slice(0, limit).map(row => ({
            ...row,
            sessionId: row.session_id,
            entities: JSON.parse(row.entities || '[]'),
            topics: JSON.parse(row.topics || '[]'),
            embedding: Array.from(new Float32Array(row.embedding?.buffer || new ArrayBuffer(0)))
          }));
          
          // Use hybrid to re-rank them
          if (parsed.length > 0) {
            return this.recallInternal(context, parsed, limit);
          }
        }
      }
    }
    
    // Parse stored fields
    memories = memories.map(row => ({
      ...row,
      sessionId: row.session_id,  // Map snake_case to camelCase
      user_id: row.user_id || undefined,
      entities: JSON.parse(row.entities || '[]'),
      topics: JSON.parse(row.topics || '[]'),
      embedding: Array.from(new Float32Array(row.embedding?.buffer || new ArrayBuffer(0)))
    }));
    
    // Filter by type
    if (options.types?.length) {
      memories = memories.filter(m => options.types!.includes(m.type));
    }
    
    // Filter by entities
    if (options.entities?.length) {
      memories = memories.filter(m => 
        options.entities!.some(e => m.entities.includes(e))
      );
    }
    
    // Filter by user_id (multi-tenancy)
    if (options.user_id) {
      memories = memories.filter(m => m.user_id === options.user_id || !m.user_id || m.user_id === 'default');
    }
    
    // If too few memories, fall back to simple similarity
    if (memories.length < 3) {
      return this.simpleRecall(context, limit, options.user_id);
    }

    // ========================================================================
    // P8.2: TEMPORAL EVOLUTION HANDLING
    // For "how did X change over time" queries, get all entity memories chronologically
    // ========================================================================

    if (isTemporalEvolutionQuery) {
      const queryEntities = extractEntitiesFromText(context);
      if (queryEntities.length > 0) {
        const entityMemories: Memory[] = [];
        const seen = new Set<string>();
        for (const entity of queryEntities) {
          const mems = this.getMemoriesByEntity(entity, 50);
          for (const m of mems) {
            if (!seen.has(m.id)) {
              seen.add(m.id);
              entityMemories.push(m);
            }
          }
        }
        if (entityMemories.length > 0) {
          // Sort chronologically by timestamp
          entityMemories.sort((a, b) => {
            const aTime = a.timestamp || a.created_at || '';
            const bTime = b.timestamp || b.created_at || '';
            return aTime.localeCompare(bTime);
          });
          return entityMemories.slice(0, limit * 2); // Return more for temporal aggregation
        }
      }
    }

    // ========================================================================
    // PHASE 1.4: HYBRID RETRIEVAL + TYPE-AWARE FILTERING
    // ========================================================================
    
    try {
      // Detect factual questions that should prioritize semantic memories
      // Expanded keyword list for better detection
      const isFactualQuery = /^(what|who|which|when|where|how (does|do|is|did|can|was|were)|why|whose)/i.test(context) ||
        /name|called|mean|stand for|relationship|port|model|database|stack|agents?|team|projects?|revenue|target|priority|embedding|spelling/i.test(context);
      
      // For factual questions, prioritize semantic memories first
      if (isFactualQuery && !options.types) {
        const semanticOnly = memories.filter(m => m.type === 'semantic' && (m.salience || 0.5) >= 0.5);
        if (semanticOnly.length > 0) {
          const semanticResults = await this.recallInternal(context, semanticOnly, limit);
          // If we got good results from semantic, return them
          if (semanticResults.length > 0) {
            return semanticResults;
          }
        }
        // Fallback: if semantic returned nothing, try all memories with hybrid
        // Don't return empty - try the full set
      }
      
      return this.recallInternal(context, memories, limit);
    } catch (error) {
      console.warn('Hybrid retrieval failed, using fallback:', error);
      return this.simpleRecall(context, limit, undefined);
    }
  }
  
  /**
   * Internal recall with hybrid search
   */
  private async recallInternal(context: string, memories: Memory[], limit: number): Promise<Memory[]> {
    try {
      // 1. Expand query with spelling variants (UK↔US)
      const expandedQueries = expandQueryWithVariants(context);
      
      // 2. Extract entities from query for boosting
      const queryEntities = extractEntitiesFromText(context);
      
      // 3. Run hybrid search with BM25 + semantic
      let candidates = await hybridSearch(context, memories, { 
        k: limit * 3,
        enableLLMFilter: false
      });
      
      // 4. Also search with expanded queries and merge results
      for (const expandedQuery of expandedQueries.slice(1)) {
        const expandedResults = await hybridSearch(expandedQuery, memories, { 
          k: limit * 2,
          enableLLMFilter: false
        });
        
        // Merge unique results
        const existingIds = new Set(candidates.map(m => m.id));
        for (const m of expandedResults) {
          if (!existingIds.has(m.id)) {
            candidates.push(m);
          }
        }
      }
      
      // 5. Boost by entity overlap
      if (queryEntities.length > 0) {
        for (const c of candidates) {
          const memoryEntities = c.entities || [];
          const overlap = memoryEntities.filter((e: string) => 
            queryEntities.some((qe: string) => e.toLowerCase() === qe.toLowerCase())
          );
          if (overlap.length > 0) {
            (c as any)._entityBoost = 1 + (overlap.length * 0.5); // 50% boost per matching entity
          }
        }
      }
      
      // 6. Re-sort with entity boost
      candidates.sort((a, b) => {
        const scoreA = (a as any)._finalScore || (a as any)._rrfScore || 0;
        const scoreB = (b as any)._finalScore || (b as any)._rrfScore || 0;
        const boostA = (a as any)._entityBoost || 1;
        const boostB = (b as any)._entityBoost || 1;
        return (scoreB * boostB) - (scoreA * boostA);
      });
      
      // 7. Apply question-type specific scoring (temporal/contradiction handling)
      const scored = scoreForQuestionType(candidates.slice(0, limit), context);
      
      return scored;
    } catch (error) {
      console.warn('Recall internal failed:', error);
      return [];
    }
  }
  
  /**
   * Simple semantic recall fallback
   */
  private async simpleRecall(context: string, limit: number, user_id?: string): Promise<Memory[]> {
    const queryEmbedding = await generateEmbedding(context);
    
    let memories;
    if (user_id) {
      memories = this.db.prepare(`
        SELECT * FROM memories WHERE deleted_at IS NULL AND (user_id = ? OR user_id = 'default')
      `).all(user_id) as any[];
    } else {
      memories = this.db.prepare(`
        SELECT * FROM memories WHERE deleted_at IS NULL
      `).all() as any[];
    }
    
    memories = memories.map(row => ({
      ...row,
      sessionId: row.session_id,  // Map snake_case to camelCase
      user_id: row.user_id || undefined,
      entities: JSON.parse(row.entities || '[]'),
      topics: JSON.parse(row.topics || '[]'),
      embedding: Array.from(new Float32Array(row.embedding?.buffer || new ArrayBuffer(0)))
    }));

    const scored = memories.map(m => ({
      ...m,
      _similarity: m.embedding.length > 0 ? cosineSimilarity(queryEmbedding, m.embedding) : 0
    }));
    
    scored.sort((a, b) => b._similarity - a._similarity);
    
    return scored.slice(0, limit).map(({ _similarity, ...m }) => m as Memory);
  }
  
  forget(id: string, hard: boolean = false): boolean {
    if (hard) {
      const stmt = this.db.prepare('DELETE FROM memories WHERE id = ?');
      return stmt.run(id).changes > 0;
    } else {
      const stmt = this.db.prepare("UPDATE memories SET deleted_at = datetime('now') WHERE id = ?");
      return stmt.run(id).changes > 0;
    }
  }
  
  // Entity management
  getEntities(): Entity[] {
    return this.db.prepare('SELECT * FROM entities ORDER BY memory_count DESC').all() as Entity[];
  }
  
  // Graph edges
  connect(sourceId: string, targetId: string, relationship: string): MemoryEdge {
    const id = `e_${uuidv4().slice(0, 8)}`;
    const now = new Date().toISOString();
    
    const stmt = this.db.prepare(`
      INSERT INTO edges (id, source_id, target_id, relationship, created_at)
      VALUES (?, ?, ?, ?, ?)
    `);
    
    stmt.run(id, sourceId, targetId, relationship, now);
    
    return { id, source_id: sourceId, target_id: targetId, relationship, created_at: now };
  }
  
  getNeighbors(memoryId: string, depth: number = 1): Memory[] {
    const neighbors: Set<string> = new Set([memoryId]);
    const result: Memory[] = [];
    
    for (let i = 0; i < depth; i++) {
      const ids = Array.from(neighbors);
      if (ids.length === 0) break;
      
      const rows = this.db.prepare(`
        SELECT DISTINCT target_id FROM edges WHERE source_id IN (${ids.map(() => '?').join(',')})
      `).all(...ids) as { target_id: string }[];
      
      for (const row of rows) {
        if (!neighbors.has(row.target_id)) {
          neighbors.add(row.target_id);
        }
      }
    }
    
    const memStmt = this.db.prepare(`SELECT * FROM memories WHERE id IN (${Array.from(neighbors).map(() => '?').join(',')})`);
    const rows = memStmt.all(...Array.from(neighbors)) as any[];
    
    return rows.map(row => ({
      ...row,
      sessionId: row.session_id,  // Map snake_case to camelCase
      entities: JSON.parse(row.entities || '[]'),
      topics: JSON.parse(row.topics || '[]'),
      embedding: Array.from(new Float32Array(row.embedding?.buffer || new ArrayBuffer(0)))
    }));
  }
  
  // Stats
  getStats(): VaultStats {
    const total = (this.db.prepare('SELECT COUNT(*) as count FROM memories WHERE deleted_at IS NULL').get() as any).count;
    
    const byType: Record<MemoryType, number> = {
      episodic: (this.db.prepare("SELECT COUNT(*) as count FROM memories WHERE type = 'episodic' AND deleted_at IS NULL").get() as any).count,
      semantic: (this.db.prepare("SELECT COUNT(*) as count FROM memories WHERE type = 'semantic' AND deleted_at IS NULL").get() as any).count,
      procedural: (this.db.prepare("SELECT COUNT(*) as count FROM memories WHERE type = 'procedural' AND deleted_at IS NULL").get() as any).count
    };
    
    const entities = (this.db.prepare('SELECT COUNT(*) as count FROM entities').get() as any).count;
    const edges = (this.db.prepare('SELECT COUNT(*) as count FROM edges').get() as any).count;
    const procedures = (this.db.prepare('SELECT COUNT(*) as count FROM procedures').get() as any).count;
    
    return { total, byType, entities, edges, procedures };
  }
  
  // Procedure management
  async createProcedure(
    title: string,
    steps: string[],
    description?: string
  ): Promise<Procedure> {
    const id = `proc_${uuidv4().slice(0, 8)}`;
    const now = new Date().toISOString();
    
    const procedureSteps: ProcedureStep[] = steps.map((desc, i) => ({
      id: `step_${uuidv4().slice(0, 8)}`,
      order: i + 1,
      description: desc
    }));
    
    const stmt = this.db.prepare(`
      INSERT INTO procedures (id, title, description, steps, version, success_count, failure_count, is_reliable, evolution_log, created_at, updated_at)
      VALUES (?, ?, ?, ?, 1, 0, 0, 0, '[]', ?, ?)
    `);
    
    stmt.run(id, title, description || null, JSON.stringify(procedureSteps), now, now);
    
    return this.getProcedure(id)!;
  }
  
  getProcedure(id: string): Procedure | null {
    const stmt = this.db.prepare('SELECT * FROM procedures WHERE id = ?');
    const row = stmt.get(id) as any;
    
    if (!row) return null;
    
    return {
      ...row,
      steps: JSON.parse(row.steps || '[]'),
      evolution_log: JSON.parse(row.evolution_log || '[]'),
      is_reliable: Boolean(row.is_reliable)
    };
  }
  
  getAllProcedures(): Procedure[] {
    const rows = this.db.prepare('SELECT * FROM procedures ORDER BY updated_at DESC').all() as any[];
    
    return rows.map(row => ({
      ...row,
      steps: JSON.parse(row.steps || '[]'),
      evolution_log: JSON.parse(row.evolution_log || '[]'),
      is_reliable: Boolean(row.is_reliable)
    }));
  }
  
  async procedureFeedback(
    procedureId: string,
    success: boolean,
    failedAtStep?: number,
    context?: string
  ): Promise<Procedure> {
    const proc = this.getProcedure(procedureId);
    if (!proc) throw new Error('Procedure not found');
    
    const now = new Date().toISOString();
    const newVersion = proc.version + 1;
    
    if (success) {
      const newCount = proc.success_count + 1;
      const isReliable = newCount >= 3 && !proc.is_reliable;
      
      const evolutionEvent: EvolutionEvent = {
        version: newVersion,
        trigger: 'success_pattern',
        change: `Success count: ${newCount}. ${isReliable ? 'Promoted to reliable workflow.' : ''}`,
        timestamp: now
      };
      
      this.db.prepare(`
        UPDATE procedures SET 
          success_count = ?,
          is_reliable = ?,
          evolution_log = ?,
          updated_at = ?
        WHERE id = ?
      `).run(newCount, isReliable ? 1 : 0, JSON.stringify([...proc.evolution_log, evolutionEvent]), now, procedureId);
    } else {
      // On failure, create new version with modified step if provided
      let newSteps = proc.steps;
      if (failedAtStep) {
        newSteps = proc.steps.map((step, i) => {
          if (i + 1 === failedAtStep) {
            return {
              ...step,
              description: `${step.description} [RETRY: add error handling]`
            };
          }
          return step;
        });
      }
      
      const evolutionEvent: EvolutionEvent = {
        version: newVersion,
        trigger: 'failure',
        change: `Failed at step ${failedAtStep || 'unknown'}. ${context || ''} New version created.`,
        timestamp: now
      };
      
      this.db.prepare(`
        UPDATE procedures SET 
          version = ?,
          failure_count = failure_count + 1,
          steps = ?,
          evolution_log = ?,
          updated_at = ?
        WHERE id = ?
      `).run(newVersion, JSON.stringify(newSteps), JSON.stringify([...proc.evolution_log, evolutionEvent]), now, procedureId);
    }
    
    return this.getProcedure(procedureId)!;
  }
  
  /**
   * P8: Entity-centric recall for multi-hop reasoning
   * Returns all memories containing a specific entity
   */
  getMemoriesByEntity(entityName: string, limit: number = 50): Memory[] {
    // Normalize entity name using alias store
    const aliasStore = getAliasStore();
    const canonicalName = aliasStore.findCanonical(entityName) || entityName;
    const aliases = aliasStore.getAliases(canonicalName);
    
    // Build pattern to match any variant
    const patterns = [canonicalName, ...aliases].map(n => n.toLowerCase());
    
    const memories = this.db.prepare(`
      SELECT * FROM memories WHERE deleted_at IS NULL
    `).all() as any[];
    
    // Filter memories that contain the entity (by name or alias)
    const matching = memories.filter(m => {
      const entities = JSON.parse(m.entities || '[]');
      const content = (m.content || '').toLowerCase();
      
      // Check if entity is in the entities array
      if (entities.some((e: string) => patterns.includes(e.toLowerCase()))) {
        return true;
      }
      
      // Also check content for mentions
      return patterns.some(p => content.includes(p));
    });
    
    // Parse and return
    return matching.slice(0, limit).map(row => ({
      ...row,
      sessionId: row.session_id,  // Map snake_case to camelCase
      entities: JSON.parse(row.entities || '[]'),
      topics: JSON.parse(row.topics || '[]'),
      embedding: Array.from(new Float32Array(row.embedding?.buffer || new ArrayBuffer(0)))
    }));
  }
  
  /**
   * P8: Multi-hop retrieval - aggregate context for entity questions
   */
  async recallEntityContext(query: string, options: { limit?: number; user_id?: string } = {}): Promise<Memory[]> {
    const limit = options.limit || 20;
    
    // Extract entity names from query
    const entities = extractEntitiesFromText(query);
    
    if (entities.length === 0) {
      // Fall back to regular recall (but skip multi-hop detection to avoid recursion)
      return this.simpleRecall(query, limit, options.user_id);
    }
    
    // Get all memories for each entity
    const allMemories: Memory[] = [];
    const seen = new Set<string>();
    
    for (const entity of entities) {
      const entityMems = this.getMemoriesByEntity(entity, limit);
      for (const m of entityMems) {
        if (!seen.has(m.id)) {
          seen.add(m.id);
          allMemories.push(m);
        }
      }
    }
    
    // If we got memories, rank them by relevance to query
    if (allMemories.length > 0) {
      // Simple keyword matching for relevance
      const queryWords = query.toLowerCase().split(/\s+/).filter(w => w.length > 3);
      
      const scored = allMemories.map(m => {
        const content = m.content.toLowerCase();
        let score = m.salience || 0.5;
        
        // Boost if query keywords appear
        for (const word of queryWords) {
          if (content.includes(word)) {
            score += 0.1;
          }
        }
        
        return { ...m, salience: score };
      });
      
      scored.sort((a, b) => (b.salience || 0) - (a.salience || 0));
      return scored.slice(0, limit);
    }
    
    // Fallback to semantic recall
    return this.recall(query, { limit });
  }
  
  close(): void {
    this.db.close();
  }
}

// Default export
export default MemoryStore;
