/**
 * Integrity Verification Tests
 * Phase 4: Memory Integrity Verification
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import Database from 'better-sqlite3';
import { 
  IntegrityStore, 
  computeContentHash, 
  computeEntityHash, 
  computeHMAC,
  verifyHMAC,
  formatIntegrityReport
} from '../src/storage/integrity.js';

describe('IntegrityStore', () => {
  let db: Database.Database;
  let store: IntegrityStore;
  const testSecret = 'test-secret-key';
  
  beforeEach(() => {
    db = new Database(':memory:');
    store = new IntegrityStore(db, testSecret);
  });
  
  afterEach(() => {
    db.close();
  });
  
  describe('computeContentHash()', () => {
    it('should compute consistent SHA-256 hash', () => {
      const content = 'Muninn is a memory system';
      
      const hash1 = computeContentHash(content);
      const hash2 = computeContentHash(content);
      
      expect(hash1).toBe(hash2);
      expect(hash1).toHaveLength(64); // SHA-256 produces 64 hex chars
    });
    
    it('should produce different hashes for different content', () => {
      const hash1 = computeContentHash('content A');
      const hash2 = computeContentHash('content B');
      
      expect(hash1).not.toBe(hash2);
    });
  });
  
  describe('computeEntityHash()', () => {
    it('should compute consistent entity hash regardless of order', () => {
      const entities1 = ['Phillip', 'Muninn', 'AI'];
      const entities2 = ['AI', 'Phillip', 'Muninn']; // Different order
      
      const hash1 = computeEntityHash(entities1);
      const hash2 = computeEntityHash(entities2);
      
      expect(hash1).toBe(hash2);
    });
    
    it('should produce different hashes for different entity sets', () => {
      const hash1 = computeEntityHash(['A', 'B']);
      const hash2 = computeEntityHash(['A', 'B', 'C']);
      
      expect(hash1).not.toBe(hash2);
    });
  });
  
  describe('computeHMAC() and verifyHMAC()', () => {
    it('should compute and verify HMAC', () => {
      const content = 'test content';
      const secret = 'my-secret';
      
      const hmac = computeHMAC(content, secret);
      const valid = verifyHMAC(content, hmac, secret);
      
      expect(valid).toBe(true);
    });
    
    it('should reject invalid HMAC', () => {
      const content = 'test content';
      const secret = 'my-secret';
      
      const hmac = computeHMAC(content, secret);
      const invalid = verifyHMAC(content, hmac, 'wrong-secret');
      
      expect(invalid).toBe(false);
    });
  });
  
  describe('initializeMemoryIntegrity()', () => {
    it('should initialize integrity record for new memory', () => {
      const integrity = store.initializeMemoryIntegrity(
        'm_test',
        'This is a test memory',
        ['test', 'memory']
      );
      
      expect(integrity.memory_id).toBe('m_test');
      expect(integrity.content_hash).toBeDefined();
      expect(integrity.created_signature).toBeDefined();
      expect(integrity.verification_status).toBe('valid');
    });
    
    it('should track chain of memories', () => {
      store.initializeMemoryIntegrity('m_1', 'First memory', ['first']);
      store.initializeMemoryIntegrity('m_2', 'Second memory', ['second']);
      
      const m2Record = store.getIntegrityStatus('m_2');
      
      expect(m2Record?.previous_hash).toBeDefined();
    });
  });
  
  describe('verifyMemoryIntegrity()', () => {
    it('should verify unmodified memory as valid', () => {
      store.initializeMemoryIntegrity('m_test', 'Original content', ['test']);
      
      const result = store.verifyMemoryIntegrity('m_test', 'Original content', ['test']);
      
      expect(result.status).toBe('valid');
    });
    
    it('should detect modified content', () => {
      store.initializeMemoryIntegrity('m_test', 'Original content', ['test']);
      
      const result = store.verifyMemoryIntegrity('m_test', 'Modified content', ['test']);
      
      expect(result.status).toBe('modified');
      expect(result.error).toContain('mismatch');
    });
    
    it('should return missing_hash for unknown memory', () => {
      const result = store.verifyMemoryIntegrity('m_unknown', 'Some content', []);
      
      expect(result.status).toBe('missing_hash');
    });
  });
  
  describe('verifyWithSignature()', () => {
    it('should verify valid signature', () => {
      store.initializeMemoryIntegrity('m_test', 'Test content', ['test']);
      
      const result = store.verifyWithSignature('m_test', 'Test content', ['test']);
      
      expect(result.status).toBe('valid');
      expect(result.signature_valid).toBe(true);
    });
    
    it('should reject tampered content', () => {
      store.initializeMemoryIntegrity('m_test', 'Original content', ['test']);
      
      const result = store.verifyWithSignature('m_test', 'Tampered content', ['test']);
      
      expect(result.status).toBe('modified');
      expect(result.signature_valid).toBe(false);
    });
  });
  
  describe('generateIntegrityReport()', () => {
    it('should generate comprehensive report', () => {
      // Setup test memories
      db.exec(`
        CREATE TABLE memories (
          id TEXT PRIMARY KEY,
          content TEXT,
          entities TEXT,
          deleted_at TEXT
        );
        INSERT INTO memories VALUES ('m_1', 'Content 1', '[]', NULL);
        INSERT INTO memories VALUES ('m_2', 'Content 2', '[]', NULL);
      `);
      
      // Initialize integrity for both
      store.initializeMemoryIntegrity('m_1', 'Content 1', []);
      store.initializeMemoryIntegrity('m_2', 'Content 2', []);
      
      // Tamper with one
      store.verifyMemoryIntegrity('m_1', 'Tampered', []);
      
      const report = store.generateIntegrityReport(
        () => db.prepare('SELECT id, content, entities FROM memories WHERE deleted_at IS NULL').all() as any[]
      );
      
      expect(report.total_memories).toBe(2);
      expect(report.valid_count).toBe(1);
      expect(report.invalid_count).toBe(1);
      expect(report.corrupted_memories.length).toBe(1);
      expect(report.by_status.valid).toBe(1);
      expect(report.by_status.modified).toBe(1);
    });
  });
  
  describe('verifyChainIntegrity()', () => {
    it('should verify valid hash chain', () => {
      store.initializeMemoryIntegrity('m_1', 'First', ['a']);
      store.initializeMemoryIntegrity('m_2', 'Second', ['b']);
      store.initializeMemoryIntegrity('m_3', 'Third', ['c']);
      
      const result = store.verifyChainIntegrity();
      
      expect(result.valid).toBe(true);
    });
    
    it('should detect broken chain', () => {
      store.initializeMemoryIntegrity('m_1', 'First', ['a']);
      
      // Manually break the chain
      db.prepare(`
        UPDATE memory_integrity SET previous_hash = 'invalid_hash' WHERE memory_id = 'm_1'
      `).run();
      
      const result = store.verifyChainIntegrity();
      
      expect(result.valid).toBe(false);
      expect(result.broken_at).toBeDefined();
    });
  });
  
  describe('getIntegrityStatus()', () => {
    it('should return integrity status for memory', () => {
      store.initializeMemoryIntegrity('m_test', 'Test', ['test']);
      
      const status = store.getIntegrityStatus('m_test');
      
      expect(status?.memory_id).toBe('m_test');
      expect(status?.verification_status).toBe('valid');
    });
    
    it('should return null for unknown memory', () => {
      const status = store.getIntegrityStatus('m_unknown');
      
      expect(status).toBeNull();
    });
  });
  
  describe('getInvalidMemories()', () => {
    it('should return memories with invalid integrity', () => {
      store.initializeMemoryIntegrity('m_1', 'Content', []);
      store.initializeMemoryIntegrity('m_2', 'Content', []);
      
      // Tamper with m_1
      store.verifyMemoryIntegrity('m_1', 'Modified', []);
      
      const invalid = store.getInvalidMemories();
      
      expect(invalid).toContain('m_1');
      expect(invalid).not.toContain('m_2');
    });
  });
  
  describe('rehashMemory()', () => {
    it('should rehash and restore integrity', () => {
      store.initializeMemoryIntegrity('m_test', 'Original', []);
      
      // First verify shows modified
      const before = store.verifyMemoryIntegrity('m_test', 'Modified', []);
      expect(before.status).toBe('modified');
      
      // Rehash with correct content
      const rehashed = store.rehashMemory('m_test', 'Correct content', []);
      
      // Now should be valid
      const after = store.verifyMemoryIntegrity('m_test', 'Correct content', []);
      expect(after.status).toBe('valid');
    });
  });
  
  describe('getVerificationHistory()', () => {
    it('should return verification history', () => {
      store.initializeMemoryIntegrity('m_test', 'Content', []);
      
      // Verify multiple times
      store.verifyMemoryIntegrity('m_test', 'Content', []);
      store.verifyMemoryIntegrity('m_test', 'Content', []);
      
      const history = store.getVerificationHistory('m_test', 10);
      
      expect(history.length).toBeGreaterThan(0);
    });
  });
  
  describe('formatIntegrityReport()', () => {
    it('should format report for display', () => {
      const report = {
        generated_at: '2024-01-15T10:00:00.000Z',
        total_memories: 100,
        verified_count: 95,
        invalid_count: 3,
        missing_hash_count: 2,
        by_status: { valid: 95, modified: 2, corrupted: 1, missing_hash: 2 },
        corrupted_memories: [{ memory_id: 'm_1', stored_hash: 'abc', computed_hash: 'def', error: 'test' }],
        verification_time_ms: 150
      };
      
      const formatted = formatIntegrityReport(report);
      
      expect(formatted).toContain('100');
      expect(formatted).toContain('95');
      expect(formatted).toContain('Invalid: 3');
      expect(formatted).toContain('150ms');
    });
  });
});