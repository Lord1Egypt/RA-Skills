/**
 * Muninn Memory Audit Module
 * Phase 1: Retrieval Audit + Staleness Detection
 * 
 * Provides:
 * - Retrieval correctness verification
 * - Decision trace extension with verification scores
 * - Staleness detection based on temporal validity
 * - Access pattern logging
 */

import { v4 as uuidv4 } from 'uuid';

// Types for audit system
export interface AuditEvent {
  id: string;
  event_type: AuditEventType;
  memory_key?: string;
  memory_id?: string;
  query?: string;
  result?: string;
  success: boolean;
  error_message?: string;
  agent_id?: string;
  session_id?: string;
  context?: Record<string, unknown>;
  retrieval_path?: string;
  verification_score?: number;
  staleness_score?: number;
  duration_ms?: number;
  created_at: string;
}

export type AuditEventType = 
  | 'store_success'
  | 'store_failure'
  | 'recall_success'
  | 'recall_failure'
  | 'recall_miss'
  | 'consolidation'
  | 'lesson_learned'
  | 'retrieval_audit'
  | 'staleness_check';

export interface DecisionTrace {
  id: string;
  query: string;
  path: string;           // JSON: retrieval path taken
  path_type: string;      // 'hybrid' | 'semantic' | 'keyword' | 'temporal' | 'multi_hop'
  result: string;        // JSON: retrieved memories
  result_ids: string[];   // Memory IDs returned
  similarity_scores: number[];
  entities_traversed?: string[];
  confidence_score?: number;
  verification_score?: number;    // LLM-assessed relevance (Phase 1)
  feedback?: string;              // User feedback: 'helpful' | 'not_relevant'
  staleness_scores?: number[];    // Per-memory staleness
  created_at: string;
}

export interface StalenessInfo {
  memory_id: string;
  created_at: string;
  valid_at?: string;     // When memory becomes valid (future-dated content)
  invalid_at?: string;   // When memory was superseded
  last_confirmed_at?: string;
  contradiction_flags?: string[];
  staleness_score: number;
  requires_verification: boolean;
}

export interface RetrievalAuditResult {
  query_id: string;
  query: string;
  retrieved_memories: Array<{
    id: string;
    content: string;
    similarity: number;
    staleness: number;
  }>;
  retrieval_path: string;
  verification_score: number;
  overall_staleness: number;
  timestamp: string;
}

// =============================================================================
// SQL SCHEMA FOR AUDIT TABLES (SQLite compatible)
// =============================================================================

export const AUDIT_SQL_SCHEMA = `
-- Decision traces for retrieval auditing
CREATE TABLE IF NOT EXISTS decision_traces (
  id TEXT PRIMARY KEY,
  query TEXT NOT NULL,
  path TEXT,
  path_type TEXT DEFAULT 'hybrid',
  result TEXT,
  result_ids TEXT,
  similarity_scores TEXT,
  entities_traversed TEXT,
  confidence_score REAL,
  verification_score REAL,
  feedback TEXT,
  staleness_scores TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_decision_traces_query ON decision_traces(query);
CREATE INDEX IF NOT EXISTS idx_decision_traces_created ON decision_traces(created_at DESC);

-- Audit events for memory operations
CREATE TABLE IF NOT EXISTS audit_events (
  id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,
  memory_key TEXT,
  memory_id TEXT,
  query TEXT,
  result TEXT,
  success INTEGER DEFAULT 0,
  error_message TEXT,
  agent_id TEXT,
  session_id TEXT,
  context TEXT,
  retrieval_path TEXT,
  verification_score REAL,
  staleness_score REAL,
  duration_ms INTEGER,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_audit_events_type ON audit_events(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_events_memory ON audit_events(memory_key);
CREATE INDEX IF NOT EXISTS idx_audit_events_created ON audit_events(created_at DESC);

-- Staleness tracking (extends memories table conceptually)
CREATE TABLE IF NOT EXISTS staleness_tracker (
  memory_id TEXT PRIMARY KEY,
  valid_at TEXT,
  invalid_at TEXT,
  last_confirmed_at TEXT,
  staleness_score REAL DEFAULT 0,
  requires_verification INTEGER DEFAULT 0,
  updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_staleness_score ON staleness_tracker(staleness_score DESC);
`;

// =============================================================================
// STALENESS CALCULATION
// =============================================================================

const STALENESS_THRESHOLDS = {
  CRITICAL_AGE_DAYS: 90,
  WARNING_AGE_DAYS: 30,
  RECENT_AGE_DAYS: 7,
};

/**
 * Calculate staleness score for a memory
 * Score: 0 (fresh) to 1 (stale)
 */
export function calculateStaleness(memory: {
  created_at?: string;
  valid_at?: string | null;
  invalid_at?: string | null;
  last_confirmed_at?: string | null;
  contradiction_flags?: string[];
}): StalenessInfo {
  const now = new Date();
  const createdAt = memory.created_at ? new Date(memory.created_at) : now;
  
  // Base staleness from age
  const ageMs = now.getTime() - createdAt.getTime();
  const ageDays = ageMs / (1000 * 60 * 60 * 24);
  
  let score = 0;
  
  // Age-based scoring
  if (ageDays > STALENESS_THRESHOLDS.CRITICAL_AGE_DAYS) {
    score += 0.5;
  } else if (ageDays > STALENESS_THRESHOLDS.WARNING_AGE_DAYS) {
    score += 0.3;
  } else if (ageDays > STALENESS_THRESHOLDS.RECENT_AGE_DAYS) {
    score += 0.1;
  }
  
  // Invalidated memory (superseded)
  if (memory.invalid_at && new Date(memory.invalid_at) < now) {
    score += 0.4;
  }
  
  // Future-dated content (not yet valid)
  if (memory.valid_at && new Date(memory.valid_at) > now) {
    score += 0.3;
  }
  
  // Confirmation penalty - if never confirmed and old
  if (!memory.last_confirmed_at && ageDays > STALENESS_THRESHOLDS.WARNING_AGE_DAYS) {
    score += 0.1;
  }
  
  // Contradiction flags
  if (memory.contradiction_flags && memory.contradiction_flags.length > 0) {
    score += Math.min(0.2, memory.contradiction_flags.length * 0.1);
  }
  
  return {
    memory_id: '', // Will be set by caller
    created_at: memory.created_at || now.toISOString(),
    valid_at: memory.valid_at || undefined,
    invalid_at: memory.invalid_at || undefined,
    last_confirmed_at: memory.last_confirmed_at || undefined,
    contradiction_flags: memory.contradiction_flags,
    staleness_score: Math.min(1, score),
    requires_verification: score >= 0.5
  };
}

// =============================================================================
// RETRIEVAL AUDIT
// =============================================================================

/**
 * Generate a unique query ID for tracking
 */
export function generateQueryId(): string {
  return `q_${uuidv4().slice(0, 8)}`;
}

/**
 * Assess retrieval quality (simplified - can be extended with LLM)
 * Returns a score 0-1 based on semantic relevance estimation
 */
export function assessRetrievalQuality(
  query: string,
  memories: Array<{ content: string; similarity: number }>
): number {
  if (memories.length === 0) return 0;
  
  // Simple heuristic: average similarity + diversity bonus
  const avgSimilarity = memories.reduce((sum, m) => sum + m.similarity, 0) / memories.length;
  
  // Check for keyword overlap (simple relevance proxy)
  const queryTerms = query.toLowerCase().split(/\s+/).filter(t => t.length > 2);
  let termOverlap = 0;
  
  for (const mem of memories) {
    const contentLower = mem.content.toLowerCase();
    for (const term of queryTerms) {
      if (contentLower.includes(term)) {
        termOverlap++;
        break; // Count each memory once if it matches any term
      }
    }
  }
  
  const diversityBonus = Math.min(0.2, (termOverlap / memories.length) * 0.2);
  
  return Math.min(1, avgSimilarity * 0.7 + diversityBonus);
}

/**
 * Log a retrieval event with full audit trail
 */
export function createRetrievalAuditLog(
  query: string,
  memories: Array<{ id: string; content: string; similarity: number }>,
  pathType: string,
  path: unknown,
  stalenessScores: number[]
): RetrievalAuditResult {
  const queryId = generateQueryId();
  const verificationScore = assessRetrievalQuality(query, memories);
  
  return {
    query_id: queryId,
    query,
    retrieved_memories: memories.map(m => ({
      id: m.id,
      content: m.content.substring(0, 100) + (m.content.length > 100 ? '...' : ''),
      similarity: m.similarity,
      staleness: stalenessScores[memories.indexOf(m)] || 0
    })),
    retrieval_path: pathType,
    verification_score: verificationScore,
    overall_staleness: stalenessScores.length > 0
      ? stalenessScores.reduce((a, b) => a + b, 0) / stalenessScores.length
      : 0,
    timestamp: new Date().toISOString()
  };
}

// =============================================================================
// AUDIT DATABASE OPERATIONS (for SQLite in muninn-skill)
// =============================================================================

export class AuditStore {
  private db: any; // Database instance
  
  constructor(db: any) {
    this.db = db;
    this.initializeTables();
  }
  
  private initializeTables(): void {
    this.db.exec(AUDIT_SQL_SCHEMA);
  }
  
  /**
   * Log an audit event
   */
  logEvent(event: Omit<AuditEvent, 'id' | 'created_at'>): AuditEvent {
    const id = `ae_${uuidv4().slice(0, 8)}`;
    const now = new Date().toISOString();
    
    const stmt = this.db.prepare(`
      INSERT INTO audit_events (
        id, event_type, memory_key, memory_id, query, result, success,
        error_message, agent_id, session_id, context, retrieval_path,
        verification_score, staleness_score, duration_ms, created_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);
    
    stmt.run(
      id,
      event.event_type,
      event.memory_key || null,
      event.memory_id || null,
      event.query || null,
      event.result || null,
      event.success ? 1 : 0,
      event.error_message || null,
      event.agent_id || null,
      event.session_id || null,
      event.context ? JSON.stringify(event.context) : null,
      event.retrieval_path || null,
      event.verification_score || null,
      event.staleness_score || null,
      event.duration_ms || null,
      now
    );
    
    return { ...event, id, created_at: now };
  }
  
  /**
   * Record a decision trace for retrieval audit
   */
  recordDecisionTrace(trace: Omit<DecisionTrace, 'id' | 'created_at'>): DecisionTrace {
    const id = `dt_${uuidv4().slice(0, 8)}`;
    const now = new Date().toISOString();
    
    const stmt = this.db.prepare(`
      INSERT INTO decision_traces (
        id, query, path, path_type, result, result_ids, similarity_scores,
        entities_traversed, confidence_score, verification_score, feedback,
        staleness_scores, created_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);
    
    stmt.run(
      id,
      trace.query,
      typeof trace.path === 'string' ? trace.path : JSON.stringify(trace.path),
      trace.path_type,
      typeof trace.result === 'string' ? trace.result : JSON.stringify(trace.result),
      JSON.stringify(trace.result_ids),
      JSON.stringify(trace.similarity_scores),
      trace.entities_traversed ? JSON.stringify(trace.entities_traversed) : null,
      trace.confidence_score || null,
      trace.verification_score || null,
      trace.feedback || null,
      trace.staleness_scores ? JSON.stringify(trace.staleness_scores) : null,
      now
    );
    
    return { ...trace, id, created_at: now };
  }
  
  /**
   * Update staleness for a memory
   */
  updateStaleness(memoryId: string, staleness: StalenessInfo): void {
    const now = new Date().toISOString();
    
    const stmt = this.db.prepare(`
      INSERT OR REPLACE INTO staleness_tracker (
        memory_id, valid_at, invalid_at, last_confirmed_at,
        staleness_score, requires_verification, updated_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?)
    `);
    
    stmt.run(
      memoryId,
      staleness.valid_at || null,
      staleness.invalid_at || null,
      staleness.last_confirmed_at || null,
      staleness.staleness_score,
      staleness.requires_verification ? 1 : 0,
      now
    );
  }
  
  /**
   * Get staleness info for a memory
   */
  getStaleness(memoryId: string): StalenessInfo | null {
    const stmt = this.db.prepare('SELECT * FROM staleness_tracker WHERE memory_id = ?');
    const row = stmt.get(memoryId);
    
    if (!row) return null;
    
    return {
      memory_id: row.memory_id,
      created_at: row.created_at,
      valid_at: row.valid_at,
      invalid_at: row.invalid_at,
      last_confirmed_at: row.last_confirmed_at,
      staleness_score: row.staleness_score,
      requires_verification: row.requires_verification === 1
    };
  }
  
  /**
   * Get recent decision traces for analysis
   */
  getRecentTraces(limit: number = 100): DecisionTrace[] {
    const stmt = this.db.prepare(`
      SELECT * FROM decision_traces
      ORDER BY created_at DESC
      LIMIT ?
    `);
    
    return stmt.all(limit).map((row: any) => ({
      id: row.id,
      query: row.query,
      path: row.path,
      path_type: row.path_type,
      result: row.result,
      result_ids: JSON.parse(row.result_ids || '[]'),
      similarity_scores: JSON.parse(row.similarity_scores || '[]'),
      entities_traversed: row.entities_traversed ? JSON.parse(row.entities_traversed) : undefined,
      confidence_score: row.confidence_score,
      verification_score: row.verification_score,
      feedback: row.feedback,
      staleness_scores: row.staleness_scores ? JSON.parse(row.staleness_scores) : undefined,
      created_at: row.created_at
    }));
  }
  
  /**
   * Get audit events for a memory
   */
  getEventsForMemory(memoryId: string, limit: number = 50): AuditEvent[] {
    const stmt = this.db.prepare(`
      SELECT * FROM audit_events
      WHERE memory_id = ? OR memory_key = ?
      ORDER BY created_at DESC
      LIMIT ?
    `);
    
    return stmt.all(memoryId, memoryId, limit).map((row: any) => ({
      id: row.id,
      event_type: row.event_type,
      memory_key: row.memory_key,
      memory_id: row.memory_id,
      query: row.query,
      result: row.result,
      success: row.success === 1,
      error_message: row.error_message,
      agent_id: row.agent_id,
      session_id: row.session_id,
      context: row.context ? JSON.parse(row.context) : undefined,
      retrieval_path: row.retrieval_path,
      verification_score: row.verification_score,
      staleness_score: row.staleness_score,
      duration_ms: row.duration_ms,
      created_at: row.created_at
    }));
  }
  
  /**
   * Get memories requiring verification (high staleness)
   */
  getMemoriesNeedingVerification(): string[] {
    const stmt = this.db.prepare(`
      SELECT memory_id FROM staleness_tracker
      WHERE requires_verification = 1
      ORDER BY staleness_score DESC
    `);
    
    return stmt.all().map((row: any) => row.memory_id);
  }
  
  /**
   * Record user feedback for a retrieval
   */
  recordFeedback(traceId: string, feedback: 'helpful' | 'not_relevant'): void {
    const stmt = this.db.prepare(`
      UPDATE decision_traces SET feedback = ? WHERE id = ?
    `);
    stmt.run(feedback, traceId);
  }
}

// =============================================================================
// HELPER: Apply staleness boost/penalty during retrieval
// =============================================================================

/**
 * Adjust similarity scores based on staleness
 * Fresh memories get boosted, stale memories get penalized
 */
export function adjustScoresForStaleness(
  memories: Array<{ id: string; similarity: number }>,
  stalenessMap: Map<string, number>
): Array<{ id: string; adjustedSimilarity: number; staleness: number }> {
  return memories.map(mem => {
    const staleness = stalenessMap.get(mem.id) || 0;
    
    // Staleness penalty: reduce score by up to 30% for very stale memories
    const penalty = staleness * 0.3;
    const adjustedSimilarity = Math.max(0, mem.similarity - penalty);
    
    return {
      id: mem.id,
      adjustedSimilarity,
      staleness
    };
  });
}

// =============================================================================
// PHASE 2: INTEGRATION WITH ACCESS LOGGING
// =============================================================================

import { AccessLogStore, AccessLogEntry, ACCESS_LOG_SQL_SCHEMA } from './access-log.js';

/**
 * Extended AuditStore with Access Logging (Phase 2)
 */
export class AuditStoreWithAccess extends AuditStore {
  private accessLog: AccessLogStore;
  
  constructor(db: any) {
    super(db);
    // Initialize access log tables
    db.exec(ACCESS_LOG_SQL_SCHEMA);
    this.accessLog = new AccessLogStore(db);
  }
  
  /**
   * Log a memory store operation
   */
  logStoreOperation(
    memoryId: string,
    actor: string,
    sessionId?: string,
    metadata?: Record<string, unknown>
  ): AccessLogEntry {
    return this.accessLog.logStore(memoryId, actor, sessionId, metadata);
  }
  
  /**
   * Log a memory recall operation
   */
  logRecallOperation(
    actor: string,
    query: string,
    resultCount: number,
    retrievalPath: string,
    sessionId?: string,
    durationMs?: number,
    memoryIds?: string[]
  ): AccessLogEntry {
    return this.accessLog.logRecall(
      actor, query, resultCount, retrievalPath, sessionId, durationMs, memoryIds
    );
  }
  
  /**
   * Log a forget/delete operation
   */
  logForgetOperation(
    memoryId: string,
    actor: string,
    hardDelete: boolean,
    sessionId?: string
  ): AccessLogEntry {
    return this.accessLog.logForget(memoryId, actor, hardDelete, sessionId);
  }
  
  /**
   * Log query performance metrics
   */
  logQueryPerformance(
    query: string,
    retrievalPath: string,
    resultCount: number,
    durationMs: number,
    similarityScores?: number[]
  ): void {
    this.accessLog.logQueryMetrics({
      query,
      retrieval_path: retrievalPath,
      result_count: resultCount,
      duration_ms: durationMs,
      similarity_scores: similarityScores
    });
  }
  
  /**
   * Get access logs for a memory
   */
  getAccessLogsForMemory(memoryId: string, limit?: number): AccessLogEntry[] {
    return this.accessLog.getAccessLogsForMemory(memoryId, limit);
  }
  
  /**
   * Get access logs by actor
   */
  getAccessLogsByActor(actor: string, limit?: number): AccessLogEntry[] {
    return this.accessLog.getAccessLogsByActor(actor, limit);
  }
  
  /**
   * Get session audit trail
   */
  getSessionAuditTrail(sessionId: string): AccessLogEntry[] {
    return this.accessLog.getSessionAuditTrail(sessionId);
  }
  
  /**
   * Get access pattern for an actor
   */
  getAccessPattern(actor: string, timeRangeHours?: number) {
    return this.accessLog.getAccessPattern(actor, timeRangeHours);
  }
  
  /**
   * Get query performance stats
   */
  getQueryStats(retrievalPath?: string, hours?: number) {
    return this.accessLog.getQueryStats(retrievalPath, hours);
  }
}