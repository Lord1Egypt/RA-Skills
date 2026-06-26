/**
 * Muninn Audit Integration
 * 
 * Provides audit wrappers around core memory operations
 * Phase 1: Retrieval Audit + Staleness Detection
 * Phase 2: Comprehensive Access Logging  
 * Phase 3: Contradiction Detection
 * Phase 4: Integrity Verification
 */

import { 
  AuditStore, 
  AuditEvent,
  AuditEventType,
  DecisionTrace,
  calculateStaleness,
  assessRetrievalQuality,
  createRetrievalAuditLog,
  adjustScoresForStaleness,
  AUDIT_SQL_SCHEMA,
  type StalenessInfo,
  type RetrievalAuditResult
} from './audit.js';

import { 
  AccessLogStore, 
  AccessLogEntry, 
  ACCESS_LOG_SQL_SCHEMA,
  createAccessLogEntry 
} from './access-log.js';

import {
  ContradictionStore,
  MemoryContradiction,
  CONTRADICTION_SQL_SCHEMA,
  quickContradictionCheck
} from '../reasoning/memory-contradiction.js';

import {
  ContradictionResolver
} from '../reasoning/resolution.js';

// Re-export ResolutionStrategy from memory-contradiction
export type { ResolutionStrategy } from '../reasoning/memory-contradiction.js';

import {
  IntegrityStore,
  MemoryIntegrity,
  INTEGRITY_SQL_SCHEMA,
  computeContentHash,
  formatIntegrityReport,
  type IntegrityReport,
  type IntegrityStatus
} from './integrity.js';

import type { Memory } from './index.js';

export { 
  AuditStore, 
  AuditEvent, 
  AuditEventType, 
  DecisionTrace,
  calculateStaleness,
  assessRetrievalQuality,
  createRetrievalAuditLog,
  adjustScoresForStaleness,
  AUDIT_SQL_SCHEMA,
  type StalenessInfo,
  type RetrievalAuditResult
};

export {
  AccessLogStore,
  AccessLogEntry,
  ACCESS_LOG_SQL_SCHEMA,
  createAccessLogEntry
};

export {
  ContradictionStore,
  MemoryContradiction,
  CONTRADICTION_SQL_SCHEMA,
  quickContradictionCheck
};

export {
  ContradictionResolver
};

export {
  IntegrityStore,
  MemoryIntegrity,
  INTEGRITY_SQL_SCHEMA,
  computeContentHash,
  formatIntegrityReport,
  type IntegrityReport,
  type IntegrityStatus
};

/**
 * Create an audit store from an existing database
 */
export function createAuditStore(db: any): AuditStore {
  return new AuditStore(db);
}

/**
 * Audit wrapper for store/remember operations
 */
export function createAuditWrappers(auditStore: AuditStore) {
  
  /**
   * Audit a successful store operation
   */
  function auditStoreSuccess(
    memory: Memory,
    options: {
      agent_id?: string;
      session_id?: string;
      context?: Record<string, unknown>;
      duration_ms?: number;
    } = {}
  ): void {
    auditStore.logEvent({
      event_type: 'store_success',
      memory_key: memory.content.substring(0, 50),
      memory_id: memory.id,
      success: true,
      agent_id: options.agent_id,
      session_id: options.session_id,
      context: options.context,
      duration_ms: options.duration_ms
    });
  }

  /**
   * Audit a failed store operation
   */
  function auditStoreFailure(
    error: Error,
    content: string,
    options: {
      agent_id?: string;
      session_id?: string;
      context?: Record<string, unknown>;
      duration_ms?: number;
    } = {}
  ): void {
    auditStore.logEvent({
      event_type: 'store_failure',
      memory_key: content.substring(0, 50),
      success: false,
      error_message: error.message,
      agent_id: options.agent_id,
      session_id: options.session_id,
      context: options.context,
      duration_ms: options.duration_ms
    });
  }

  /**
   * Audit a successful recall operation
   */
  function auditRecallSuccess(
    query: string,
    memories: Memory[],
    options: {
      path_type?: string;
      path?: unknown;
      agent_id?: string;
      session_id?: string;
      context?: Record<string, unknown>;
      duration_ms?: number;
    } = {}
  ): RetrievalAuditResult {
    // Calculate staleness for each memory
    const stalenessScores = memories.map(m => {
      const staleness = calculateStaleness({
        created_at: m.created_at,
        valid_at: m.valid_at,
        invalid_at: m.invalid_at
      });
      return staleness.staleness_score;
    });

    // Create audit result
    const auditResult = createRetrievalAuditLog(
      query,
      memories.map(m => ({ id: m.id, content: m.content, similarity: 0.8 })), // similarity placeholder
      options.path_type || 'hybrid',
      options.path || {},
      stalenessScores
    );

    // Log audit event
    auditStore.logEvent({
      event_type: 'recall_success',
      query,
      result: JSON.stringify(memories.map(m => m.id)),
      success: true,
      retrieval_path: options.path_type,
      verification_score: auditResult.verification_score,
      staleness_score: auditResult.overall_staleness,
      agent_id: options.agent_id,
      session_id: options.session_id,
      context: options.context,
      duration_ms: options.duration_ms
    });

    // Record decision trace
    auditStore.recordDecisionTrace({
      query,
      path: options.path ? JSON.stringify(options.path) : '{}',
      path_type: options.path_type || 'hybrid',
      result: JSON.stringify(memories),
      result_ids: memories.map(m => m.id),
      similarity_scores: memories.map(() => 0.8), // Placeholder
      verification_score: auditResult.verification_score,
      staleness_scores: stalenessScores
    });

    return auditResult;
  }

  /**
   * Audit a failed recall operation
   */
  function auditRecallFailure(
    query: string,
    error: Error,
    options: {
      agent_id?: string;
      session_id?: string;
      context?: Record<string, unknown>;
      duration_ms?: number;
    } = {}
  ): void {
    auditStore.logEvent({
      event_type: 'recall_failure',
      query,
      success: false,
      error_message: error.message,
      agent_id: options.agent_id,
      session_id: options.session_id,
      context: options.context,
      duration_ms: options.duration_ms
    });
  }

  /**
   * Audit a recall miss (no memory found when one expected)
   */
  function auditRecallMiss(
    query: string,
    options: {
      expected_memory_key?: string;
      agent_id?: string;
      session_id?: string;
      context?: Record<string, unknown>;
    } = {}
  ): void {
    auditStore.logEvent({
      event_type: 'recall_miss',
      query,
      memory_key: options.expected_memory_key,
      success: false,
      agent_id: options.agent_id,
      session_id: options.session_id,
      context: options.context
    });
  }

  /**
   * Update staleness for a memory
   */
  function updateMemoryStaleness(memory: Memory): void {
    const staleness = calculateStaleness({
      created_at: memory.created_at,
      valid_at: memory.valid_at,
      invalid_at: memory.invalid_at,
      last_confirmed_at: memory.last_confirmed_at,
      contradiction_flags: memory.contradiction_flags
    });
    
    staleness.memory_id = memory.id;
    auditStore.updateStaleness(memory.id, staleness);
  }

  /**
   * Get retrieval audit data for analysis
   */
  function getRetrievalStats(days: number = 7) {
    const traces = auditStore.getRecentTraces(100);
    
    const total = traces.length;
    const avgVerification = total > 0 
      ? traces.reduce((sum, t) => sum + (t.verification_score || 0), 0) / total 
      : 0;
    const helpfulCount = traces.filter(t => t.feedback === 'helpful').length;
    const notRelevantCount = traces.filter(t => t.feedback === 'not_relevant').length;
    
    return {
      total_retrievals: total,
      avg_verification_score: avgVerification,
      helpful_count: helpfulCount,
      not_relevant_count: notRelevantCount,
      feedback_ratio: (helpfulCount + notRelevantCount) > 0 
        ? helpfulCount / (helpfulCount + notRelevantCount) 
        : null
    };
  }

  /**
   * Get memories that need verification due to staleness
   */
  function getMemoriesNeedingVerification(): string[] {
    return auditStore.getMemoriesNeedingVerification();
  }

  /**
   * Record user feedback on a retrieval
   */
  function recordRetrievalFeedback(traceId: string, feedback: 'helpful' | 'not_relevant'): void {
    auditStore.recordFeedback(traceId, feedback);
  }

  return {
    auditStoreSuccess,
    auditStoreFailure,
    auditRecallSuccess,
    auditRecallFailure,
    auditRecallMiss,
    updateMemoryStaleness,
    getRetrievalStats,
    getMemoriesNeedingVerification,
    recordRetrievalFeedback
  };
}

/**
 * Extend memory type to include staleness-related fields
 */
export interface AuditedMemory extends Memory {
  staleness_score?: number;
  requires_verification?: boolean;
  last_confirmed_at?: string;
  valid_at?: string;
  invalid_at?: string;
  contradiction_flags?: string[];
}

// =============================================================================
// PHASE 2-4: COMPREHENSIVE AUDIT WRAPPERS
// =============================================================================

/**
 * Create a comprehensive audit wrapper with all phases
 */
export function createComprehensiveAuditWrappers(db: any) {
  const auditStore = new AuditStore(db);
  const accessLogStore = new AccessLogStore(db);
  const contradictionStore = new ContradictionStore(db);
  const integrityStore = new IntegrityStore(db);
  const resolver = new ContradictionResolver(contradictionStore);
  
  return {
    // Phase 1: Core Audit
    audit: auditStore,
    
    // Phase 2: Access Logging
    accessLog: accessLogStore,
    
    // Phase 3: Contradiction Detection  
    contradiction: contradictionStore,
    
    // Phase 4: Integrity Verification
    integrity: integrityStore,
    
    // Helper: Log memory store with full audit trail
    logMemoryStore: (memory: Memory, actor: string, sessionId?: string) => {
      const startTime = Date.now();
      
      // Log to audit events
      auditStore.logEvent({
        event_type: 'store_success',
        memory_key: memory.content.substring(0, 50),
        memory_id: memory.id,
        success: true,
        session_id: sessionId,
        agent_id: actor
      });
      
      // Log to access log (Phase 2)
      accessLogStore.logStore(memory.id, actor, sessionId);
      
      // Initialize integrity record (Phase 4)
      integrityStore.initializeMemoryIntegrity(
        memory.id,
        memory.content,
        memory.entities
      );
      
      return Date.now() - startTime;
    },
    
    // Helper: Log memory recall with full audit trail
    logMemoryRecall: (
      query: string,
      memories: Memory[],
      actor: string,
      sessionId: string,
      retrievalPath: string,
      durationMs: number
    ) => {
      const startTime = Date.now();
      
      // Log to audit events (Phase 1)
      const stalenessScores = memories.map(m => {
        const s = calculateStaleness({
          created_at: m.created_at,
          valid_at: m.valid_at,
          invalid_at: m.invalid_at
        });
        return s.staleness_score;
      });
      
      const auditResult = createRetrievalAuditLog(
        query,
        memories.map(m => ({ id: m.id, content: m.content, similarity: 0.8 })),
        retrievalPath,
        {},
        stalenessScores
      );
      
      auditStore.logEvent({
        event_type: 'recall_success',
        query,
        result: JSON.stringify(memories.map(m => m.id)),
        success: true,
        retrieval_path: retrievalPath,
        verification_score: auditResult.verification_score,
        staleness_score: auditResult.overall_staleness,
        agent_id: actor,
        session_id: sessionId,
        duration_ms: durationMs
      });
      
      auditStore.recordDecisionTrace({
        query,
        path: JSON.stringify({ path: retrievalPath }),
        path_type: retrievalPath,
        result: JSON.stringify(memories),
        result_ids: memories.map(m => m.id),
        similarity_scores: memories.map(() => 0.8),
        verification_score: auditResult.verification_score,
        staleness_scores: stalenessScores
      });
      
      // Log to access log (Phase 2)
      accessLogStore.logRecall(
        actor,
        query,
        memories.length,
        retrievalPath,
        sessionId,
        durationMs,
        memories.map(m => m.id)
      );
      
      // Log query metrics
      accessLogStore.logQueryMetrics({
        query,
        retrieval_path: retrievalPath,
        result_count: memories.length,
        duration_ms: durationMs
      });
      
      return {
        auditResult,
        duration: Date.now() - startTime
      };
    },
    
    // Helper: Check for contradictions on store (Phase 3)
    checkContradictions: async (memory: Memory) => {
      const result = await contradictionStore.checkForContradictions(
        {
          memory_id: memory.id,
          content: memory.content,
          entities: memory.entities,
          threshold: 0.85
        },
        (limit: number) => {
          return db.prepare(`
            SELECT id, content, entities, created_at, last_confirmed_at
            FROM memories
            WHERE deleted_at IS NULL AND id != ?
            ORDER BY created_at DESC
            LIMIT ?
          `).all(memory.id, limit) as any[];
        }
      );
      
      return result;
    },
    
    // Helper: Verify memory integrity on recall (Phase 4)
    verifyOnRecall: (memory: Memory): { status: string; verified: boolean } => {
      const result = integrityStore.verifyMemoryIntegrity(
        memory.id,
        memory.content,
        memory.entities
      );
      
      return {
        status: result.status,
        verified: result.status === 'valid'
      };
    },
    
    // Helper: Generate full integrity report
    generateIntegrityReport: () => {
      return integrityStore.generateIntegrityReport(
        () => db.prepare(`
          SELECT id, content, entities FROM memories
          WHERE deleted_at IS NULL
        `).all() as any[]
      );
    },
    
    // Helper: Get access pattern for actor
    getAccessPattern: (actor: string, hours: number = 24) => {
      return accessLogStore.getAccessPattern(actor, hours);
    },
    
    // Helper: Get query stats
    getQueryStats: (retrievalPath?: string, hours: number = 24) => {
      return accessLogStore.getQueryStats(retrievalPath, hours);
    },
    
    // Helper: Get session audit trail
    getSessionAuditTrail: (sessionId: string) => {
      return accessLogStore.getSessionAuditTrail(sessionId);
    }
  };
}