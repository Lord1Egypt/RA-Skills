/**
 * Contradiction Detection Tests
 * Phase 3: Memory Contradiction Detection
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import Database from 'better-sqlite3';
import { ContradictionStore, MemoryContradiction } from '../src/reasoning/memory-contradiction.js';

describe('ContradictionStore', () => {
  let db: Database.Database;
  let store: ContradictionStore;
  
  beforeEach(() => {
    db = new Database(':memory:');
    store = new ContradictionStore(db);
  });
  
  afterEach(() => {
    db.close();
  });
  
  describe('checkForContradictions()', () => {
    it('should detect direct contradictions', async () => {
      // First, insert a "fake" memory into test DB for comparison
      db.exec(`
        CREATE TABLE memories (
          id TEXT PRIMARY KEY,
          content TEXT,
          entities TEXT,
          created_at TEXT,
          deleted_at TEXT
        );
        INSERT INTO memories VALUES ('m_1', 'Phillip uses Australian English', '["Phillip", "English"]', datetime('now'), NULL);
        INSERT INTO memories VALUES ('m_2', 'Phillip prefers British English', '["Phillip", "English"]', datetime('now'), NULL);
      `);
      
      const result = await store.checkForContradictions(
        {
          memory_id: 'm_2',
          content: 'Phillip prefers British English',
          entities: ['Phillip', 'English'],
          threshold: 0.7
        },
        (limit) => db.prepare(`
          SELECT id, content, entities, created_at, last_confirmed_at 
          FROM memories WHERE deleted_at IS NULL AND id != ?
          LIMIT ?
        `).all('m_2', limit) as any[]
      );
      
      // Should find contradiction with high similarity but different content
      expect(result.checked_count).toBeGreaterThan(0);
    });
    
    it('should not flag similar/reinforcing content', async () => {
      db.exec(`
        CREATE TABLE memories (
          id TEXT PRIMARY KEY,
          content TEXT,
          entities TEXT,
          created_at TEXT,
          deleted_at TEXT
        );
        INSERT INTO memories VALUES ('m_1', 'Muninn is a memory system', '["Muninn", "memory"]', datetime('now'), NULL);
      `);
      
      const result = await store.checkForContradictions(
        {
          memory_id: 'm_2',
          content: 'Muninn is a memory system for AI agents',
          entities: ['Muninn', 'memory', 'AI'],
          threshold: 0.7
        },
        (limit) => db.prepare(`
          SELECT id, content, entities, created_at, last_confirmed_at 
          FROM memories WHERE deleted_at IS NULL AND id != ?
          LIMIT ?
        `).all('m_2', limit) as any[]
      );
      
      // Should not find contradiction - same topic being expanded
      expect(result.has_contradiction).toBe(false);
    });
    
    it('should skip memories without entity overlap', async () => {
      db.exec(`
        CREATE TABLE memories (
          id TEXT PRIMARY KEY,
          content TEXT,
          entities TEXT,
          created_at TEXT,
          deleted_at TEXT
        );
        INSERT INTO memories VALUES ('m_1', 'The sky is blue', '["sky", "color"]', datetime('now'), NULL);
      `);
      
      const result = await store.checkForContradictions(
        {
          memory_id: 'm_2',
          content: 'Phillip lives in Brisbane',
          entities: ['Phillip', 'Brisbane'],
          threshold: 0.7
        },
        (limit) => db.prepare(`
          SELECT id, content, entities, created_at, last_confirmed_at 
          FROM memories WHERE deleted_at IS NULL AND id != ?
          LIMIT ?
        `).all('m_2', limit) as any[]
      );
      
      // Should check but find no contradiction due to entity mismatch
      expect(result.checked_count).toBe(1);
      expect(result.has_contradiction).toBe(false);
    });
  });
  
  describe('getUnresolvedContradictions()', () => {
    it('should return unresolved contradictions', async () => {
      // Manually insert a contradiction for testing
      db.exec(`
        INSERT INTO memory_contradictions 
        (id, memory_a_id, memory_b_id, entity, value_a, value_b, detection_method, similarity_score, contradiction_score, resolution_status, created_at)
        VALUES ('mc_1', 'm_a', 'm_b', 'Phillip', 'Australian', 'British', 'embedding', 0.9, 0.8, 'unresolved', datetime('now'))
      `);
      
      const unresolved = store.getUnresolvedContradictions();
      
      expect(unresolved.length).toBe(1);
      expect(unresolved[0].resolution_status).toBe('unresolved');
    });
  });
  
  describe('resolveContradiction()', () => {
    it('should resolve contradiction with strategy', async () => {
      db.exec(`
        INSERT INTO memory_contradictions 
        (id, memory_a_id, memory_b_id, entity, value_a, value_b, detection_method, similarity_score, contradiction_score, resolution_status, created_at)
        VALUES ('mc_1', 'm_a', 'm_b', 'Phillip', 'Australian', 'British', 'embedding', 0.9, 0.8, 'unresolved', datetime('now'))
      `);
      
      const resolved = store.resolveContradiction('mc_1', 'prefer_recent', 'system', 'Auto-resolved by preferring recent');
      
      expect(resolved?.resolution_status).toBe('auto_resolved');
      expect(resolved?.resolution_strategy).toBe('prefer_recent');
      expect(resolved?.resolved_by).toBe('system');
    });
  });
  
  describe('ignoreContradiction()', () => {
    it('should ignore contradiction', () => {
      db.exec(`
        INSERT INTO memory_contradictions 
        (id, memory_a_id, memory_b_id, entity, detection_method, similarity_score, contradiction_score, resolution_status, created_at)
        VALUES ('mc_1', 'm_a', 'm_b', 'Phillip', 'embedding', 0.9, 0.3, 'unresolved', datetime('now'))
      `);
      
      const ignored = store.ignoreContradiction('mc_1', 'admin', 'False positive - different contexts');
      
      expect(ignored?.resolution_status).toBe('ignored');
      expect(ignored?.resolution_note).toContain('False positive');
    });
  });
  
  describe('getContradictionsForMemory()', () => {
    it('should get contradictions for specific memory', () => {
      db.exec(`
        INSERT INTO memory_contradictions 
        (id, memory_a_id, memory_b_id, entity, detection_method, similarity_score, contradiction_score, resolution_status, created_at)
        VALUES 
          ('mc_1', 'm_target', 'm_other', 'Phillip', 'embedding', 0.9, 0.8, 'unresolved', datetime('now')),
          ('mc_2', 'm_other2', 'm_target', 'Tech', 'embedding', 0.85, 0.75, 'unresolved', datetime('now'))
      `);
      
      const contradictions = store.getContradictionsForMemory('m_target');
      
      expect(contradictions.length).toBe(2);
    });
  });
  
  describe('getStats()', () => {
    it('should return contradiction statistics', () => {
      db.exec(`
        INSERT INTO memory_contradictions 
        (id, memory_a_id, memory_b_id, detection_method, similarity_score, contradiction_score, resolution_status, created_at)
        VALUES 
          ('mc_1', 'm_a', 'm_b', 'embedding', 0.9, 0.8, 'unresolved', datetime('now')),
          ('mc_2', 'm_c', 'm_d', 'embedding', 0.85, 0.75, 'auto_resolved', datetime('now')),
          ('mc_3', 'm_e', 'm_f', 'rule', 0.8, 0.6, 'ignored', datetime('now'))
      `);
      
      const stats = store.getStats();
      
      expect(stats.total).toBe(3);
      expect(stats.unresolved).toBe(1);
      expect(stats.auto_resolved).toBe(1);
      expect(stats.ignored).toBe(1);
    });
  });
  
  describe('addToReviewQueue()', () => {
    it('should add contradiction to review queue', () => {
      db.exec(`
        INSERT INTO memory_contradictions 
        (id, memory_a_id, memory_b_id, detection_method, similarity_score, contradiction_score, resolution_status, created_at)
        VALUES ('mc_1', 'm_a', 'm_b', 'embedding', 0.9, 0.8, 'unresolved', datetime('now'))
      `);
      
      store.addToReviewQueue('mc_1', 5, 'admin');
      
      const queue = store.getReviewQueue(10);
      
      expect(queue.length).toBe(1);
      expect(queue[0].priority).toBe(5);
    });
  });
});