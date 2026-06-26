/**
 * Muninn Memory Access Logging
 * Phase 2: Comprehensive Access Logging
 * 
 * Provides:
 * - Full access logging for every memory operation (store, recall, remember, forget)
 * - Access patterns tracking (who accessed what, when, from where)
 * - Session-based audit trails
 * - Query logging with performance metrics
 */

import { v4 as uuidv4 } from 'uuid';
import Database from 'better-sqlite3';

// Types for access logging
export type AccessAction = 'store' | 'recall' | 'remember' | 'update' | 'delete' | 'forget' | 'consolidate';

export interface AccessLogEntry {
  id: string;
  memory_id?: string;
  memory_key?: string;
  action: AccessAction;
  actor: string;              // agent_id, user_id, or 'system'
  session_id?: string;
  context?: Record<string, unknown>;
  query?: string;              // For recall operations
  retrieval_path?: string;    // 'hybrid' | 'semantic' | 'keyword' | 'temporal' | 'multi_hop'
  result_count?: number;      // Number of memories returned
  duration_ms?: number;      // Operation duration
  success: boolean;
  error_message?: string;
  metadata?: Record<string, unknown>;  // Additional operation-specific data
  created_at: string;
}

export interface AccessPattern {
  actor: string;
  memory_id?: string;
  action: AccessAction;
  time_range: {
    start: string;
    end: string;
  };
  count: number;
  last_access?: string;
}

export interface QueryMetrics {
  id?: string;
  query: string;
  retrieval_path: string;
  result_count: number;
  duration_ms: number;
  timestamp: string;
  similarity_scores?: number[];
}

// =============================================================================
// SQL SCHEMA FOR ACCESS LOGGING
// =============================================================================

export const ACCESS_LOG_SQL_SCHEMA = `
-- Comprehensive access log for all memory operations
CREATE TABLE IF NOT EXISTS access_log (
  id TEXT PRIMARY KEY,
  memory_id TEXT,
  memory_key TEXT,
  action TEXT NOT NULL CHECK(action IN ('store', 'recall', 'remember', 'update', 'delete', 'forget', 'consolidate')),
  actor TEXT NOT NULL,
  session_id TEXT,
  context TEXT,
  query TEXT,
  retrieval_path TEXT,
  result_count INTEGER,
  duration_ms INTEGER,
  success INTEGER DEFAULT 1,
  error_message TEXT,
  metadata TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_access_log_memory ON access_log(memory_id);
CREATE INDEX IF NOT EXISTS idx_access_log_actor ON access_log(actor);
CREATE INDEX IF NOT EXISTS idx_access_log_session ON access_log(session_id);
CREATE INDEX IF NOT EXISTS idx_access_log_action ON access_log(action);
CREATE INDEX IF NOT EXISTS idx_access_log_created ON access_log(created_at DESC);

-- Query performance metrics (lightweight for high-frequency logging)
CREATE TABLE IF NOT EXISTS query_metrics (
  id TEXT PRIMARY KEY,
  query TEXT NOT NULL,
  retrieval_path TEXT,
  result_count INTEGER,
  duration_ms INTEGER,
  similarity_scores TEXT,
  timestamp TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_query_metrics_query ON query_metrics(query);
CREATE INDEX IF NOT EXISTS idx_query_metrics_created ON query_metrics(timestamp DESC);
`;

// =============================================================================
// ACCESS LOG STORE
// =============================================================================

export class AccessLogStore {
  private db: Database.Database;
  
  constructor(db: Database.Database) {
    this.db = db;
    this.initializeTables();
  }
  
  private initializeTables(): void {
    this.db.exec(ACCESS_LOG_SQL_SCHEMA);
  }
  
  /**
   * Log an access event
   */
  log(entry: Omit<AccessLogEntry, 'id' | 'created_at'>): AccessLogEntry {
    const id = `al_${uuidv4().slice(0, 8)}`;
    const now = new Date().toISOString();
    
    const stmt = this.db.prepare(`
      INSERT INTO access_log (
        id, memory_id, memory_key, action, actor, session_id, context,
        query, retrieval_path, result_count, duration_ms, success,
        error_message, metadata, created_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);
    
    stmt.run(
      id,
      entry.memory_id || null,
      entry.memory_key || null,
      entry.action,
      entry.actor,
      entry.session_id || null,
      entry.context ? JSON.stringify(entry.context) : null,
      entry.query || null,
      entry.retrieval_path || null,
      entry.result_count || null,
      entry.duration_ms || null,
      entry.success ? 1 : 0,
      entry.error_message || null,
      entry.metadata ? JSON.stringify(entry.metadata) : null,
      now
    );
    
    return { ...entry, id, created_at: now };
  }
  
  /**
   * Log a store operation
   */
  logStore(memoryId: string, actor: string, sessionId?: string, metadata?: Record<string, unknown>): AccessLogEntry {
    return this.log({
      memory_id: memoryId,
      action: 'store',
      actor,
      session_id: sessionId,
      success: true,
      metadata
    });
  }
  
  /**
   * Log a recall/remember operation
   */
  logRecall(
    actor: string,
    query: string,
    resultCount: number,
    retrievalPath: string,
    sessionId?: string,
    durationMs?: number,
    memoryIds?: string[]
  ): AccessLogEntry {
    return this.log({
      action: 'recall',
      actor,
      query,
      retrieval_path: retrievalPath,
      result_count: resultCount,
      duration_ms: durationMs,
      session_id: sessionId,
      success: true,
      metadata: memoryIds ? { retrieved_memory_ids: memoryIds } : undefined
    });
  }
  
  /**
   * Log a forget/delete operation
   */
  logForget(memoryId: string, actor: string, hardDelete: boolean, sessionId?: string): AccessLogEntry {
    return this.log({
      memory_id: memoryId,
      action: hardDelete ? 'delete' : 'forget',
      actor,
      session_id: sessionId,
      success: true
    });
  }
  
  /**
   * Log a failed operation
   */
  logFailure(
    action: AccessAction,
    actor: string,
    error: string,
    memoryId?: string,
    query?: string,
    sessionId?: string
  ): AccessLogEntry {
    return this.log({
      memory_id: memoryId,
      action,
      actor,
      query,
      session_id: sessionId,
      success: false,
      error_message: error
    });
  }
  
  /**
   * Log query performance metrics (lightweight)
   */
  logQueryMetrics(metrics: Omit<QueryMetrics, 'id' | 'timestamp'>): QueryMetrics {
    const id = `qm_${uuidv4().slice(0, 8)}`;
    const now = new Date().toISOString();
    
    const stmt = this.db.prepare(`
      INSERT INTO query_metrics (
        id, query, retrieval_path, result_count, duration_ms, similarity_scores, timestamp
      ) VALUES (?, ?, ?, ?, ?, ?, ?)
    `);
    
    stmt.run(
      id,
      metrics.query,
      metrics.retrieval_path,
      metrics.result_count,
      metrics.duration_ms,
      metrics.similarity_scores ? JSON.stringify(metrics.similarity_scores) : null,
      now
    );
    
    return { ...metrics, id, timestamp: now };
  }
  
  /**
   * Get access logs for a specific memory
   */
  getAccessLogsForMemory(memoryId: string, limit: number = 100): AccessLogEntry[] {
    const stmt = this.db.prepare(`
      SELECT * FROM access_log
      WHERE memory_id = ?
      ORDER BY created_at DESC
      LIMIT ?
    `);
    
    return stmt.all(memoryId, limit).map(this.parseRow);
  }
  
  /**
   * Get access logs for a specific actor
   */
  getAccessLogsByActor(actor: string, limit: number = 100): AccessLogEntry[] {
    const stmt = this.db.prepare(`
      SELECT * FROM access_log
      WHERE actor = ?
      ORDER BY created_at DESC
      LIMIT ?
    `);
    
    return stmt.all(actor, limit).map(this.parseRow);
  }
  
  /**
   * Get access logs for a specific session
   */
  getAccessLogsBySession(sessionId: string, limit: number = 100): AccessLogEntry[] {
    const stmt = this.db.prepare(`
      SELECT * FROM access_log
      WHERE session_id = ?
      ORDER BY created_at DESC
      LIMIT ?
    `);
    
    return stmt.all(sessionId, limit).map(this.parseRow);
  }
  
  /**
   * Get recent access logs
   */
  getRecentAccessLogs(limit: number = 100): AccessLogEntry[] {
    const stmt = this.db.prepare(`
      SELECT * FROM access_log
      ORDER BY created_at DESC
      LIMIT ?
    `);
    
    return stmt.all(limit).map(this.parseRow);
  }
  
  /**
   * Get access pattern for an actor
   */
  getAccessPattern(actor: string, timeRangeHours: number = 24): AccessPattern {
    const startTime = new Date(Date.now() - timeRangeHours * 60 * 60 * 1000).toISOString();
    
    const stmt = this.db.prepare(`
      SELECT action, memory_id, COUNT(*) as count, MAX(created_at) as last_access
      FROM access_log
      WHERE actor = ? AND created_at >= ?
      GROUP BY action, memory_id
    `);
    
    const rows = stmt.all(actor, startTime) as any[];
    
    const actions: Record<string, number> = {};
    let totalCount = 0;
    let lastAccess: string | undefined;
    
    for (const row of rows) {
      actions[row.action] = row.count;
      totalCount += row.count;
      if (!lastAccess || row.last_access > lastAccess) {
        lastAccess = row.last_access;
      }
    }
    
    return {
      actor,
      time_range: { start: startTime, end: new Date().toISOString() },
      count: totalCount,
      last_access: lastAccess,
      action: (Object.keys(actions)[0] as AccessAction) || 'store'
    };
  }
  
  /**
   * Get most accessed memories
   */
  getMostAccessedMemories(limit: number = 10): Array<{ memory_id: string; access_count: number; last_access: string }> {
    const stmt = this.db.prepare(`
      SELECT memory_id, COUNT(*) as access_count, MAX(created_at) as last_access
      FROM access_log
      WHERE memory_id IS NOT NULL
      GROUP BY memory_id
      ORDER BY access_count DESC
      LIMIT ?
    `);
    
    return stmt.all(limit) as any[];
  }
  
  /**
   * Get most active actors
   */
  getMostActiveActors(limit: number = 10): Array<{ actor: string; action_count: number; last_action: string }> {
    const stmt = this.db.prepare(`
      SELECT actor, COUNT(*) as action_count, MAX(created_at) as last_action
      FROM access_log
      GROUP BY actor
      ORDER BY action_count DESC
      LIMIT ?
    `);
    
    return stmt.all(limit) as any[];
  }
  
  /**
   * Get query performance stats
   */
  getQueryStats(retrievalPath?: string, hours: number = 24): {
    avg_duration_ms: number;
    total_queries: number;
    avg_results: number;
    p95_duration_ms: number;
  } {
    const startTime = new Date(Date.now() - hours * 60 * 60 * 1000).toISOString();
    
    let query = `
      SELECT 
        AVG(duration_ms) as avg_duration_ms,
        COUNT(*) as total_queries,
        AVG(result_count) as avg_results
      FROM query_metrics
      WHERE timestamp >= ?
    `;
    
    const params: any[] = [startTime];
    
    if (retrievalPath) {
      query += ` AND retrieval_path = ?`;
      params.push(retrievalPath);
    }
    
    const avgStats = this.db.prepare(query).get(...params) as any;
    
    // Get p95
    const p95Stmt = this.db.prepare(`
      SELECT duration_ms FROM query_metrics
      WHERE timestamp >= ? ${retrievalPath ? 'AND retrieval_path = ?' : ''}
      ORDER BY duration_ms ASC
    `);
    
    const p95Rows = p95Stmt.all(...params) as any[];
    const p95Index = Math.floor(p95Rows.length * 0.95);
    const p95Duration = p95Rows[p95Index]?.duration_ms || 0;
    
    return {
      avg_duration_ms: avgStats.avg_duration_ms || 0,
      total_queries: avgStats.total_queries || 0,
      avg_results: avgStats.avg_results || 0,
      p95_duration_ms: p95Duration
    };
  }
  
  /**
   * Get recent query metrics
   */
  getRecentQueries(limit: number = 50): QueryMetrics[] {
    const stmt = this.db.prepare(`
      SELECT * FROM query_metrics
      ORDER BY timestamp DESC
      LIMIT ?
    `);
    
    return stmt.all(limit).map((row: any) => ({
      id: row.id,
      query: row.query,
      retrieval_path: row.retrieval_path,
      result_count: row.result_count,
      duration_ms: row.duration_ms,
      similarity_scores: row.similarity_scores ? JSON.parse(row.similarity_scores) : undefined,
      timestamp: row.timestamp
    }));
  }
  
  /**
   * Clear old access logs (retention policy)
   */
  clearOldLogs(daysToKeep: number = 90): number {
    const cutoffDate = new Date(Date.now() - daysToKeep * 24 * 60 * 60 * 1000).toISOString();
    
    // Delete old access logs
    const accessStmt = this.db.prepare(`
      DELETE FROM access_log WHERE created_at < ?
    `);
    const accessResult = accessStmt.run(cutoffDate);
    
    // Delete old query metrics (keep shorter - 30 days)
    const metricsCutoff = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString();
    const metricsStmt = this.db.prepare(`
      DELETE FROM query_metrics WHERE timestamp < ?
    `);
    const metricsResult = metricsStmt.run(metricsCutoff);
    
    return accessResult.changes + metricsResult.changes;
  }
  
  /**
   * Get session audit trail
   */
  getSessionAuditTrail(sessionId: string): AccessLogEntry[] {
    const stmt = this.db.prepare(`
      SELECT * FROM access_log
      WHERE session_id = ?
      ORDER BY created_at ASC
    `);
    
    return stmt.all(sessionId).map(this.parseRow);
  }
  
  private parseRow(row: any): AccessLogEntry {
    return {
      id: row.id,
      memory_id: row.memory_id,
      memory_key: row.memory_key,
      action: row.action,
      actor: row.actor,
      session_id: row.session_id,
      context: row.context ? JSON.parse(row.context) : undefined,
      query: row.query,
      retrieval_path: row.retrieval_path,
      result_count: row.result_count,
      duration_ms: row.duration_ms,
      success: row.success === 1,
      error_message: row.error_message,
      metadata: row.metadata ? JSON.parse(row.metadata) : undefined,
      created_at: row.created_at
    };
  }
}

// =============================================================================
// CONVENIENCE FUNCTIONS (for use without direct DB access)
// =============================================================================

/**
 * Create an access log entry from a memory operation
 */
export function createAccessLogEntry(
  action: AccessAction,
  actor: string,
  options: {
    memoryId?: string;
    memoryKey?: string;
    sessionId?: string;
    query?: string;
    retrievalPath?: string;
    resultCount?: number;
    durationMs?: number;
    success?: boolean;
    error?: string;
    context?: Record<string, unknown>;
    metadata?: Record<string, unknown>;
  } = {}
): Omit<AccessLogEntry, 'id' | 'created_at'> {
  return {
    memory_id: options.memoryId,
    memory_key: options.memoryKey,
    action,
    actor,
    session_id: options.sessionId,
    query: options.query,
    retrieval_path: options.retrievalPath,
    result_count: options.resultCount,
    duration_ms: options.durationMs,
    success: options.success ?? true,
    error_message: options.error,
    context: options.context,
    metadata: options.metadata
  };
}

/**
 * Format access log for display
 */
export function formatAccessLog(entry: AccessLogEntry): string {
  const time = new Date(entry.created_at).toLocaleString();
  const memory = entry.memory_id ? `[${entry.memory_id}]` : '';
  const query = entry.query ? `"${entry.query.substring(0, 50)}..."` : '';
  const result = entry.result_count !== undefined ? `(${entry.result_count} results)` : '';
  const duration = entry.duration_ms !== undefined ? `${entry.duration_ms}ms` : '';
  
  return `[${time}] ${entry.actor}: ${entry.action} ${memory} ${query} ${result} ${duration} ${entry.success ? '' : '(FAILED)'}`;
}