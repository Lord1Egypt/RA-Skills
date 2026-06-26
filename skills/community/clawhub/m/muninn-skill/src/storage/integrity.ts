/**
 * Muninn Memory Integrity Verification
 * Phase 4: Integrity Verification
 * 
 * Provides:
 * - Hash-based integrity checks for stored memories
 * - Tamper detection (detect if memory content changed outside system)
 * - Verification on retrieval
 * - Integrity report generation
 */

import { v4 as uuidv4 } from 'uuid';
import Database from 'better-sqlite3';
import crypto from 'crypto';

// Types for integrity verification
export type IntegrityStatus = 'valid' | 'modified' | 'corrupted' | 'missing_hash';

export interface MemoryIntegrity {
  memory_id: string;
  content_hash: string;
  entity_hash: string;
  created_signature?: string;     // HMAC at creation time
  last_verified_at: string;
  verification_status: IntegrityStatus;
  previous_hash?: string;         // For chain verification
}

export interface IntegrityReport {
  generated_at: string;
  total_memories: number;
  verified_count: number;
  invalid_count: number;
  missing_hash_count: number;
  by_status: Record<IntegrityStatus, number>;
  corrupted_memories: Array<{
    memory_id: string;
    stored_hash: string;
    computed_hash: string;
    error?: string;
  }>;
  verification_time_ms: number;
}

// =============================================================================
// SQL SCHEMA FOR INTEGRITY
// =============================================================================

export const INTEGRITY_SQL_SCHEMA = `
-- Memory integrity verification table
CREATE TABLE IF NOT EXISTS memory_integrity (
  memory_id TEXT PRIMARY KEY,
  content_hash TEXT NOT NULL,
  entity_hash TEXT,
  created_signature TEXT,
  last_verified_at TEXT DEFAULT (datetime('now')),
  verification_status TEXT DEFAULT 'valid',
  previous_hash TEXT
);

CREATE INDEX IF NOT EXISTS idx_integrity_status ON memory_integrity(verification_status);
CREATE INDEX IF NOT EXISTS idx_integrity_verified ON memory_integrity(last_verified_at DESC);

-- Integrity verification log
CREATE TABLE IF NOT EXISTS integrity_verification_log (
  id TEXT PRIMARY KEY,
  memory_id TEXT,
  verification_type TEXT NOT NULL,
  stored_hash TEXT,
  computed_hash TEXT,
  status TEXT NOT NULL,
  error_message TEXT,
  verified_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_integrity_log_memory ON integrity_verification_log(memory_id);
CREATE INDEX IF NOT EXISTS idx_integrity_log_verified ON integrity_verification_log(verified_at DESC);
`;

// =============================================================================
// HASHING FUNCTIONS
// =============================================================================

const HASH_ALGORITHM = 'sha256';

/**
 * Compute SHA-256 hash of content
 */
export function computeContentHash(content: string): string {
  return crypto.createHash(HASH_ALGORITHM).update(content, 'utf8').digest('hex');
}

/**
 * Compute hash of entities (sorted JSON for consistency)
 */
export function computeEntityHash(entities: string[]): string {
  const sorted = [...entities].sort();
  return crypto.createHash(HASH_ALGORITHM).update(JSON.stringify(sorted), 'utf8').digest('hex');
}

/**
 * Compute HMAC signature for creation verification
 */
export function computeHMAC(content: string, secretKey: string): string {
  return crypto.createHmac(HASH_ALGORITHM, secretKey).update(content, 'utf8').digest('hex');
}

/**
 * Verify HMAC signature
 */
export function verifyHMAC(content: string, signature: string, secretKey: string): boolean {
  const computed = computeHMAC(content, secretKey);
  return crypto.timingSafeEqual(
    Buffer.from(computed, 'utf8'),
    Buffer.from(signature, 'utf8')
  );
}

// =============================================================================
// INTEGRITY STORE
// =============================================================================

export class IntegrityStore {
  private db: Database.Database;
  private secretKey: string;
  
  constructor(db: Database.Database, secretKey?: string) {
    this.db = db;
    this.secretKey = secretKey || process.env.MUNINN_INTEGRITY_SECRET || 'default-secret-change-in-production';
    this.initializeTables();
  }
  
  private initializeTables(): void {
    this.db.exec(INTEGRITY_SQL_SCHEMA);
  }
  
  /**
   * Initialize integrity record for a new memory
   */
  initializeMemoryIntegrity(
    memoryId: string,
    content: string,
    entities: string[]
  ): MemoryIntegrity {
    const contentHash = computeContentHash(content);
    const entityHash = computeEntityHash(entities);
    const signature = computeHMAC(content + entityHash, this.secretKey);
    
    // Get previous hash for chain
    const lastMemory = this.db.prepare(`
      SELECT content_hash FROM memory_integrity
      ORDER BY last_verified_at DESC
      LIMIT 1
    `).get() as any;
    
    const previousHash = lastMemory?.content_hash;
    
    this.db.prepare(`
      INSERT INTO memory_integrity (
        memory_id, content_hash, entity_hash, created_signature,
        last_verified_at, verification_status, previous_hash
      ) VALUES (?, ?, ?, ?, datetime('now'), 'valid', ?)
    `).run(memoryId, contentHash, entityHash, signature, previousHash || null);
    
    return {
      memory_id: memoryId,
      content_hash: contentHash,
      entity_hash: entityHash,
      created_signature: signature,
      last_verified_at: new Date().toISOString(),
      verification_status: 'valid',
      previous_hash: previousHash
    };
  }
  
  /**
   * Verify integrity of a single memory
   */
  verifyMemoryIntegrity(
    memoryId: string,
    content: string,
    entities: string[]
  ): {
    status: IntegrityStatus;
    stored_hash: string;
    computed_hash: string;
    error?: string;
  } {
    const record = this.db.prepare(`
      SELECT * FROM memory_integrity WHERE memory_id = ?
    `).get(memoryId) as any;
    
    if (!record) {
      return {
        status: 'missing_hash',
        stored_hash: '',
        computed_hash: '',
        error: 'No integrity record found for memory'
      };
    }
    
    const computedContentHash = computeContentHash(content);
    const computedEntityHash = computeEntityHash(entities);
    const combinedHash = computeContentHash(content + computedEntityHash);
    
    // Check content hash
    if (computedContentHash !== record.content_hash) {
      this.logVerification(memoryId, 'content_hash', record.content_hash, computedContentHash, 'modified');
      
      this.db.prepare(`
        UPDATE memory_integrity SET
          verification_status = 'modified',
          last_verified_at = datetime('now')
        WHERE memory_id = ?
      `).run(memoryId);
      
      return {
        status: 'modified',
        stored_hash: record.content_hash,
        computed_hash: computedContentHash,
        error: 'Content hash mismatch - memory may have been tampered with'
      };
    }
    
    // Check entity hash
    if (computedEntityHash !== record.entity_hash) {
      this.logVerification(memoryId, 'entity_hash', record.entity_hash, computedEntityHash, 'modified');
    }
    
    // All good
    this.db.prepare(`
      UPDATE memory_integrity SET
        verification_status = 'valid',
        last_verified_at = datetime('now')
      WHERE memory_id = ?
    `).run(memoryId);
    
    return {
      status: 'valid',
      stored_hash: record.content_hash,
      computed_hash: computedContentHash
    };
  }
  
  /**
   * Verify integrity with signature check
   */
  verifyWithSignature(
    memoryId: string,
    content: string,
    entities: string[]
  ): {
    status: IntegrityStatus;
    signature_valid: boolean;
    error?: string;
  } {
    const record = this.db.prepare(`
      SELECT * FROM memory_integrity WHERE memory_id = ?
    `).get(memoryId) as any;
    
    if (!record || !record.created_signature) {
      return {
        status: 'missing_hash',
        signature_valid: false,
        error: 'No signature record found'
      };
    }
    
    const entityHash = computeEntityHash(entities);
    const expectedSignature = computeHMAC(content + entityHash, this.secretKey);
    
    try {
      const signatureValid = record.created_signature === expectedSignature;
      
      if (!signatureValid) {
        return {
          status: 'modified',
          signature_valid: false,
          error: 'HMAC signature mismatch'
        };
      }
      
      return {
        status: 'valid',
        signature_valid: true
      };
    } catch (e: any) {
      return {
        status: 'corrupted',
        signature_valid: false,
        error: e.message
      };
    }
  }
  
  /**
   * Generate full integrity report
   */
  generateIntegrityReport(
    getMemories: () => Array<{ id: string; content: string; entities: string }>
  ): IntegrityReport {
    const startTime = Date.now();
    const memories = getMemories();
    
    const byStatus: Record<IntegrityStatus, number> = {
      valid: 0,
      modified: 0,
      corrupted: 0,
      missing_hash: 0
    };
    
    const corrupted: IntegrityReport['corrupted_memories'] = [];
    let verifiedCount = 0;
    let missingHashCount = 0;
    
    for (const memory of memories) {
      const entities = typeof memory.entities === 'string' 
        ? JSON.parse(memory.entities) 
        : memory.entities;
      
      const result = this.verifyMemoryIntegrity(memory.id, memory.content, entities);
      
      if (result.status === 'missing_hash') {
        missingHashCount++;
      } else if (result.status === 'valid') {
        verifiedCount++;
      } else {
        corrupted.push({
          memory_id: memory.id,
          stored_hash: result.stored_hash,
          computed_hash: result.computed_hash,
          error: result.error
        });
      }
      
      byStatus[result.status]++;
    }
    
    return {
      generated_at: new Date().toISOString(),
      total_memories: memories.length,
      verified_count: verifiedCount,
      invalid_count: corrupted.length,
      missing_hash_count: missingHashCount,
      by_status: byStatus,
      corrupted_memories: corrupted,
      verification_time_ms: Date.now() - startTime
    };
  }
  
  /**
   * Verify chain integrity (hash chain)
   */
  verifyChainIntegrity(): {
    valid: boolean;
    broken_at?: string;
    details: string[];
  } {
    const chain = this.db.prepare(`
      SELECT memory_id, content_hash, previous_hash
      FROM memory_integrity
      WHERE previous_hash IS NOT NULL
      ORDER BY last_verified_at ASC
    `).all() as any[];
    
    const details: string[] = [];
    
    for (const record of chain) {
      // Get the memory that should have this previous_hash
      const expectedPrev = this.db.prepare(`
        SELECT memory_id FROM memory_integrity
        WHERE content_hash = ? AND memory_id != ?
      `).get(record.previous_hash, record.memory_id) as any;
      
      if (!expectedPrev) {
        return {
          valid: false,
          broken_at: record.memory_id,
          details: [`Chain broken at ${record.memory_id}: previous hash ${record.previous_hash} not found`]
        };
      }
      
      details.push(`Chain link verified: ${expectedPrev.memory_id} -> ${record.memory_id}`);
    }
    
    return { valid: true, details };
  }
  
  /**
   * Get integrity status for a memory
   */
  getIntegrityStatus(memoryId: string): MemoryIntegrity | null {
    const row = this.db.prepare(`
      SELECT * FROM memory_integrity WHERE memory_id = ?
    `).get(memoryId) as any;
    
    if (!row) return null;
    
    return {
      memory_id: row.memory_id,
      content_hash: row.content_hash,
      entity_hash: row.entity_hash,
      created_signature: row.created_signature,
      last_verified_at: row.last_verified_at,
      verification_status: row.verification_status,
      previous_hash: row.previous_hash
    };
  }
  
  /**
   * Get all memories with invalid integrity
   */
  getInvalidMemories(): string[] {
    const rows = this.db.prepare(`
      SELECT memory_id FROM memory_integrity
      WHERE verification_status != 'valid'
      ORDER BY last_verified_at DESC
    `).all() as any[];
    
    return rows.map(r => r.memory_id);
  }
  
  /**
   * Rehash memory (for fixing integrity issues)
   */
  rehashMemory(memoryId: string, content: string, entities: string[]): MemoryIntegrity {
    const contentHash = computeContentHash(content);
    const entityHash = computeEntityHash(entities);
    const signature = computeHMAC(content + entityHash, this.secretKey);
    
    this.db.prepare(`
      UPDATE memory_integrity SET
        content_hash = ?,
        entity_hash = ?,
        created_signature = ?,
        verification_status = 'valid',
        last_verified_at = datetime('now')
      WHERE memory_id = ?
    `).run(contentHash, entityHash, signature, memoryId);
    
    return this.getIntegrityStatus(memoryId)!;
  }
  
  /**
   * Bulk initialize integrity for memories without records
   */
  bulkInitialize(
    getMemoriesWithoutIntegrity: () => Array<{ id: string; content: string; entities: string }>
  ): number {
    const memories = getMemoriesWithoutIntegrity();
    let count = 0;
    
    for (const memory of memories) {
      const entities = typeof memory.entities === 'string'
        ? JSON.parse(memory.entities)
        : memory.entities;
      
      try {
        this.initializeMemoryIntegrity(memory.id, memory.content, entities);
        count++;
      } catch (e) {
        // Already exists, skip
      }
    }
    
    return count;
  }
  
  private logVerification(
    memoryId: string,
    verificationType: string,
    storedHash: string,
    computedHash: string,
    status: IntegrityStatus
  ): void {
    const id = `ivl_${uuidv4().slice(0, 8)}`;
    
    this.db.prepare(`
      INSERT INTO integrity_verification_log (
        id, memory_id, verification_type, stored_hash, computed_hash, status
      ) VALUES (?, ?, ?, ?, ?, ?)
    `).run(id, memoryId, verificationType, storedHash, computedHash, status);
  }
  
  /**
   * Get verification history for a memory
   */
  getVerificationHistory(memoryId: string, limit: number = 20): Array<{
    id: string;
    verification_type: string;
    status: string;
    verified_at: string;
  }> {
    const rows = this.db.prepare(`
      SELECT * FROM integrity_verification_log
      WHERE memory_id = ?
      ORDER BY verified_at DESC
      LIMIT ?
    `).all(memoryId, limit) as any[];
    
    return rows.map(r => ({
      id: r.id,
      verification_type: r.verification_type,
      status: r.status,
      verified_at: r.verified_at
    }));
  }
}

// =============================================================================
// CONVENIENCE FUNCTIONS
// =============================================================================

/**
 * Quick integrity check (without full initialization)
 */
export function quickIntegrityCheck(content: string, storedHash: string): boolean {
  const computed = computeContentHash(content);
  return computed === storedHash;
}

/**
 * Format integrity report for display
 */
export function formatIntegrityReport(report: IntegrityReport): string {
  let output = `Integrity Report - ${report.generated_at}\n`;
  output += `${'='.repeat(50)}\n\n`;
  output += `Total Memories: ${report.total_memories}\n`;
  output += `Verified: ${report.verified_count}\n`;
  output += `Invalid: ${report.invalid_count}\n`;
  output += `Missing Hash: ${report.missing_hash_count}\n\n`;
  output += `Status Breakdown:\n`;
  output += `  Valid: ${report.by_status.valid}\n`;
  output += `  Modified: ${report.by_status.modified}\n`;
  output += `  Corrupted: ${report.by_status.corrupted}\n`;
  output += `  Missing Hash: ${report.by_status.missing_hash}\n\n`;
  output += `Verification Time: ${report.verification_time_ms}ms\n`;
  
  if (report.corrupted_memories.length > 0) {
    output += `\nCorrupted Memories:\n`;
    for (const c of report.corrupted_memories) {
      output += `  - ${c.memory_id}: ${c.error}\n`;
    }
  }
  
  return output;
}