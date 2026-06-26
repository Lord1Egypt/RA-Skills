/**
 * Access Log Tests
 * Phase 2: Comprehensive Access Logging
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import Database from 'better-sqlite3';
import { AccessLogStore, AccessLogEntry, createAccessLogEntry, formatAccessLog } from '../src/storage/access-log.js';

describe('AccessLogStore', () => {
  let db: Database.Database;
  let store: AccessLogStore;
  
  beforeEach(() => {
    db = new Database(':memory:');
    store = new AccessLogStore(db);
  });
  
  afterEach(() => {
    db.close();
  });
  
  describe('log()', () => {
    it('should log a basic access event', () => {
      const entry = store.log({
        action: 'store',
        actor: 'agent:test',
        success: true
      });
      
      expect(entry.id).toBeDefined();
      expect(entry.action).toBe('store');
      expect(entry.actor).toBe('agent:test');
      expect(entry.success).toBe(true);
      expect(entry.created_at).toBeDefined();
    });
    
    it('should log with full context', () => {
      const entry = store.log({
        memory_id: 'm_123',
        action: 'recall',
        actor: 'user:phillip',
        session_id: 'session_abc',
        query: 'What is Muninn?',
        retrieval_path: 'hybrid',
        result_count: 5,
        duration_ms: 150,
        success: true,
        context: { user_agent: 'cli' }
      });
      
      expect(entry.memory_id).toBe('m_123');
      expect(entry.query).toBe('What is Muninn?');
      expect(entry.result_count).toBe(5);
      expect(entry.duration_ms).toBe(150);
      expect(entry.context).toEqual({ user_agent: 'cli' });
    });
  });
  
  describe('logStore(), logRecall(), logForget()', () => {
    it('should log store operations', () => {
      const entry = store.logStore('m_test', 'agent:test', 'session_1');
      
      expect(entry.action).toBe('store');
      expect(entry.memory_id).toBe('m_test');
    });
    
    it('should log recall operations', () => {
      const entry = store.logRecall(
        'agent:test',
        'Tell me about Muninn',
        3,
        'hybrid',
        'session_1',
        200
      );
      
      expect(entry.action).toBe('recall');
      expect(entry.query).toBe('Tell me about Muninn');
      expect(entry.result_count).toBe(3);
      expect(entry.duration_ms).toBe(200);
    });
    
    it('should log forget operations', () => {
      const entry = store.logForget('m_old', 'agent:test', false, 'session_1');
      
      expect(entry.action).toBe('forget');
      expect(entry.memory_id).toBe('m_old');
    });
    
    it('should log delete operations', () => {
      const entry = store.logForget('m_old', 'agent:test', true, 'session_1');
      
      expect(entry.action).toBe('delete');
    });
  });
  
  describe('logFailure()', () => {
    it('should log failed operations', () => {
      const entry = store.logFailure(
        'recall',
        'agent:test',
        'Database connection failed',
        'm_123',
        'test query',
        'session_1'
      );
      
      expect(entry.success).toBe(false);
      expect(entry.error_message).toBe('Database connection failed');
    });
  });
  
  describe('getAccessLogsForMemory()', () => {
    it('should retrieve access logs for a memory', () => {
      store.logStore('m_test', 'agent:a', 'session_1');
      store.logStore('m_test', 'agent:b', 'session_1');
      store.logStore('m_other', 'agent:c', 'session_1');
      
      const logs = store.getAccessLogsForMemory('m_test');
      
      expect(logs.length).toBe(2);
      expect(logs.every(l => l.memory_id === 'm_test')).toBe(true);
    });
  });
  
  describe('getAccessLogsByActor()', () => {
    it('should retrieve logs by actor', () => {
      store.logStore('m_1', 'agent:alice', 's1');
      store.logStore('m_2', 'agent:bob', 's1');
      store.logStore('m_3', 'agent:alice', 's2');
      
      const aliceLogs = store.getAccessLogsByActor('agent:alice');
      
      expect(aliceLogs.length).toBe(2);
      expect(aliceLogs.every(l => l.actor === 'agent:alice')).toBe(true);
    });
  });
  
  describe('getAccessPattern()', () => {
    it('should get access pattern for actor', () => {
      store.logStore('m_1', 'agent:alice', 's1');
      store.logRecall('agent:alice', 'query 1', 3, 'hybrid', 's1', 100);
      store.logRecall('agent:alice', 'query 2', 2, 'semantic', 's1', 150);
      
      const pattern = store.getAccessPattern('agent:alice', 24);
      
      expect(pattern.actor).toBe('agent:alice');
      expect(pattern.count).toBe(3);
    });
  });
  
  describe('getMostAccessedMemories()', () => {
    it('should return most accessed memories', () => {
      store.logStore('m_1', 'a', 's1');
      store.logRecall('a', 'q', 1, 'h', 's1');
      store.logRecall('a', 'q', 1, 'h', 's1');
      store.logRecall('a', 'q', 1, 'h', 's1');
      store.logStore('m_2', 'a', 's1');
      
      const top = store.getMostAccessedMemories(5);
      
      expect(top[0].memory_id).toBe('m_1');
      expect(top[0].access_count).toBe(3); // 1 store + 2 recalls
    });
  });
  
  describe('clearOldLogs()', () => {
    it('should clear old logs based on retention policy', () => {
      store.logStore('m_1', 'a', 's1');
      
      const deleted = store.clearOldLogs(0); // Delete everything older than 0 days
      
      expect(deleted).toBeGreaterThan(0);
    });
  });
  
  describe('createAccessLogEntry()', () => {
    it('should create access log entry object', () => {
      const entry = createAccessLogEntry('recall', 'agent:test', {
        memoryId: 'm_123',
        sessionId: 'session_1',
        query: 'test query',
        retrievalPath: 'hybrid',
        resultCount: 5,
        durationMs: 150,
        success: true
      });
      
      expect(entry.action).toBe('recall');
      expect(entry.memory_id).toBe('m_123');
      expect(entry.query).toBe('test query');
    });
  });
  
  describe('formatAccessLog()', () => {
    it('should format access log for display', () => {
      const entry: AccessLogEntry = {
        id: 'al_123',
        action: 'recall',
        actor: 'agent:test',
        session_id: 'session_1',
        query: 'What is Muninn?',
        retrieval_path: 'hybrid',
        result_count: 5,
        duration_ms: 150,
        success: true,
        created_at: '2024-01-15T10:30:00.000Z'
      };
      
      const formatted = formatAccessLog(entry);
      
      expect(formatted).toContain('recall');
      expect(formatted).toContain('agent:test');
      expect(formatted).toContain('(5 results)');
      expect(formatted).toContain('150ms');
    });
  });
  
  describe('logQueryMetrics()', () => {
    it('should log query performance metrics', () => {
      store.logQueryMetrics({
        query: 'test query',
        retrieval_path: 'hybrid',
        result_count: 5,
        duration_ms: 150,
        similarity_scores: [0.9, 0.8, 0.7]
      });
      
      const queries = store.getRecentQueries(10);
      
      expect(queries.length).toBe(1);
      expect(queries[0].query).toBe('test query');
      expect(queries[0].similarity_scores).toEqual([0.9, 0.8, 0.7]);
    });
  });
  
  describe('getQueryStats()', () => {
    it('should return query performance statistics', () => {
      store.logQueryMetrics({ query: 'q1', retrieval_path: 'hybrid', result_count: 3, duration_ms: 100 });
      store.logQueryMetrics({ query: 'q2', retrieval_path: 'hybrid', result_count: 5, duration_ms: 200 });
      store.logQueryMetrics({ query: 'q3', retrieval_path: 'semantic', result_count: 2, duration_ms: 150 });
      
      const stats = store.getQueryStats();
      
      expect(stats.total_queries).toBe(3);
      expect(stats.avg_duration_ms).toBe(150);
      expect(stats.avg_results).toBeCloseTo(3.33, 0);
    });
  });
});