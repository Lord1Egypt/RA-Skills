/**
 * Audit Module Tests
 * Phase 1: Retrieval Audit + Staleness Detection
 */

import { describe, it, expect, beforeEach } from 'bun:test';
import Database from 'better-sqlite3';
import { 
  AuditStore, 
  calculateStaleness, 
  assessRetrievalQuality, 
  createRetrievalAuditLog,
  adjustScoresForStaleness,
  AUDIT_SQL_SCHEMA 
} from '../src/storage/audit.js';

describe('Audit Module', () => {
  let db: any;
  let auditStore: AuditStore;

  beforeEach(() => {
    // Create in-memory database for testing
    db = new Database(':memory:');
    auditStore = new AuditStore(db);
  });

  describe('Staleness Calculation', () => {
    it('should calculate low staleness for recent memories', () => {
      const recentMemory = {
        created_at: new Date().toISOString(),
        valid_at: null,
        invalid_at: null,
        last_confirmed_at: null,
        contradiction_flags: []
      };
      
      const staleness = calculateStaleness(recentMemory);
      expect(staleness.staleness_score).toBeLessThan(0.2);
      expect(staleness.requires_verification).toBe(false);
    });

    it('should calculate high staleness for old memories', () => {
      const oldMemory = {
        created_at: new Date(Date.now() - 100 * 24 * 60 * 60 * 1000).toISOString(), // 100 days ago
        valid_at: null,
        invalid_at: null,
        last_confirmed_at: null,
        contradiction_flags: []
      };
      
      const staleness = calculateStaleness(oldMemory);
      expect(staleness.staleness_score).toBeGreaterThanOrEqual(0.5);
      expect(staleness.requires_verification).toBe(true);
    });

    it('should increase staleness for invalidated memories', () => {
      const supersededMemory = {
        created_at: new Date(Date.now() - 60 * 24 * 60 * 60 * 1000).toISOString(), // 60 days ago
        valid_at: null,
        invalid_at: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(), // 30 days ago
        last_confirmed_at: null,
        contradiction_flags: []
      };
      
      const staleness = calculateStaleness(supersededMemory);
      // Age penalty (60 days) + invalidation penalty
      expect(staleness.staleness_score).toBeGreaterThan(0.5);
    });

    it('should increase staleness for future-dated content', () => {
      const futureMemory = {
        created_at: new Date().toISOString(),
        valid_at: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(), // 30 days in future
        invalid_at: null,
        last_confirmed_at: null,
        contradiction_flags: []
      };
      
      const staleness = calculateStaleness(futureMemory);
      // Fresh but future-dated
      expect(staleness.staleness_score).toBeGreaterThanOrEqual(0.3);
    });

    it('should increase staleness with contradiction flags', () => {
      const memoryWithContradictions = {
        created_at: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(), // 10 days ago
        valid_at: null,
        invalid_at: null,
        last_confirmed_at: null,
        contradiction_flags: ['mem_a', 'mem_b', 'mem_c'] // 3 contradictions
      };
      
      const staleness = calculateStaleness(memoryWithContradictions);
      // Age penalty + contradiction penalty (0.1 * 3 = 0.3, capped at 0.2)
      expect(staleness.staleness_score).toBeGreaterThan(0.2);
    });
  });

  describe('Retrieval Quality Assessment', () => {
    it('should return 0 for empty results', () => {
      const score = assessRetrievalQuality('test query', []);
      expect(score).toBe(0);
    });

    it('should assess quality based on similarity and term overlap', () => {
      const memories = [
        { content: 'Phillip works at Elev8Advisory', similarity: 0.9 },
        { content: 'Muninn is a memory system', similarity: 0.3 }
      ];
      
      const score = assessRetrievalQuality('Phillip', memories);
      expect(score).toBeGreaterThan(0.5); // Should have good score due to term overlap
    });

    it('should give diversity bonus for multiple matching memories', () => {
      const memories = [
        { content: 'Phillip lives in Brisbane', similarity: 0.8 },
        { content: 'Phillip works at Elev8Advisory', similarity: 0.7 }
      ];
      
      const score = assessRetrievalQuality('Phillip', memories);
      expect(score).toBeGreaterThan(0.5);
    });
  });

  describe('Retrieval Audit Log', () => {
    it('should create proper audit log structure', () => {
      const memories = [
        { id: 'mem1', content: 'First memory', similarity: 0.9 },
        { id: 'mem2', content: 'Second memory', similarity: 0.7 }
      ];
      const stalenessScores = [0.1, 0.2];
      
      const auditLog = createRetrievalAuditLog(
        'test query',
        memories,
        'hybrid',
        { method: 'bm25 + semantic' },
        stalenessScores
      );
      
      expect(auditLog.query_id).toMatch(/^q_[a-f0-9]+$/);
      expect(auditLog.query).toBe('test query');
      expect(auditLog.retrieved_memories).toHaveLength(2);
      expect(auditLog.verification_score).toBeGreaterThanOrEqual(0);
      expect(auditLog.verification_score).toBeLessThanOrEqual(1);
      expect(auditLog.overall_staleness).toBe(0.15); // (0.1 + 0.2) / 2
    });
  });

  describe('Score Adjustment for Staleness', () => {
    it('should penalize stale memories', () => {
      const memories = [
        { id: 'fresh', similarity: 0.9 },
        { id: 'stale', similarity: 0.9 }
      ];
      
      const stalenessMap = new Map([
        ['fresh', 0.1],  // 10% penalty
        ['stale', 0.8]   // 80% penalty
      ]);
      
      const adjusted = adjustScoresForStaleness(memories, stalenessMap);
      
      const fresh = adjusted.find(a => a.id === 'fresh');
      const stale = adjusted.find(a => a.id === 'stale');
      
      // Fresh: 0.9 - (0.1 * 0.3) = 0.87
      expect(fresh?.adjustedSimilarity).toBeCloseTo(0.87, 2);
      expect(fresh?.staleness).toBe(0.1);
      
      // Stale: 0.9 - (0.8 * 0.3) = 0.66
      expect(stale?.adjustedSimilarity).toBeCloseTo(0.66, 2);
      expect(stale?.staleness).toBe(0.8);
    });

    it('should handle missing staleness data', () => {
      const memories = [
        { id: 'unknown', similarity: 0.8 }
      ];
      
      const stalenessMap = new Map(); // Empty map
      
      const adjusted = adjustScoresForStaleness(memories, stalenessMap);
      
      expect(adjusted[0].adjustedSimilarity).toBe(0.8); // No penalty
      expect(adjusted[0].staleness).toBe(0);
    });
  });

  describe('Audit Store Operations', () => {
    it('should log audit events', () => {
      const event = auditStore.logEvent({
        event_type: 'recall_success',
        query: 'test query',
        result: JSON.stringify(['mem1', 'mem2']),
        success: true,
        verification_score: 0.85
      });
      
      expect(event.id).toMatch(/^ae_[a-f0-9]+$/);
      expect(event.event_type).toBe('recall_success');
      expect(event.success).toBe(true);
    });

    it('should record decision traces', () => {
      const trace = auditStore.recordDecisionTrace({
        query: 'test query',
        path: JSON.stringify({ method: 'hybrid' }),
        path_type: 'hybrid',
        result: JSON.stringify(['mem1']),
        result_ids: ['mem1'],
        similarity_scores: [0.9],
        verification_score: 0.85,
        staleness_scores: [0.1]
      });
      
      expect(trace.id).toMatch(/^dt_[a-f0-9]+$/);
      expect(trace.query).toBe('test query');
      expect(trace.verification_score).toBe(0.85);
    });

    it('should update and retrieve staleness', () => {
      const stalenessInfo: any = {
        memory_id: 'test_mem',
        created_at: new Date().toISOString(),
        staleness_score: 0.3,
        requires_verification: false
      };
      
      auditStore.updateStaleness('test_mem', stalenessInfo);
      
      const retrieved = auditStore.getStaleness('test_mem');
      expect(retrieved?.memory_id).toBe('test_mem');
      expect(retrieved?.staleness_score).toBe(0.3);
    });

    it('should get recent decision traces', () => {
      // Record some traces
      for (let i = 0; i < 5; i++) {
        auditStore.recordDecisionTrace({
          query: `query ${i}`,
          path: '{}',
          path_type: 'hybrid',
          result: '[]',
          result_ids: [],
          similarity_scores: []
        });
      }
      
      const traces = auditStore.getRecentTraces(3);
      expect(traces).toHaveLength(3);
    });

    it('should get memories needing verification', () => {
      // Add stale memories
      auditStore.updateStaleness('mem1', {
        memory_id: 'mem1',
        created_at: new Date().toISOString(),
        staleness_score: 0.6,
        requires_verification: true
      });
      
      auditStore.updateStaleness('mem2', {
        memory_id: 'mem2',
        created_at: new Date().toISOString(),
        staleness_score: 0.3,
        requires_verification: false
      });
      
      const needsVerification = auditStore.getMemoriesNeedingVerification();
      expect(needsVerification).toContain('mem1');
      expect(needsVerification).not.toContain('mem2');
    });

    it('should record user feedback', () => {
      // Record a trace first
      const trace = auditStore.recordDecisionTrace({
        query: 'test',
        path: '{}',
        path_type: 'hybrid',
        result: '[]',
        result_ids: [],
        similarity_scores: []
      });
      
      // Record feedback
      auditStore.recordFeedback(trace.id, 'helpful');
      
      // Retrieve and check
      const traces = auditStore.getRecentTraces(1);
      expect(traces[0].feedback).toBe('helpful');
    });
  });
});