/**
 * Relationship Store for Knowledge Graph
 * Stores relationships with timestamps, sessionId, and contradiction tracking
 */

import Database from 'better-sqlite3';
import { v4 as uuidv4 } from 'uuid';

export type RelationshipType = 
  | 'has_target' | 'has_customer' | 'uses' | 'built_by' | 'employs' | 'has_priority' | 'part_of'
  // P7: Conversational relationships for multi-hop reasoning
  | 'went_to' | 'works_at' | 'knows' | 'has_interest' | 'has_identity' | 'has_plan'
  // Entity co-occurrence relationships
  | 'co_occurs_with';

export interface Relationship {
  id: string;
  source: string;       // Entity ID
  target: string;       // Entity ID  
  type: RelationshipType;
  value?: string;       // "$1000/month"
  timestamp: string;    // ISO date string
  sessionId: string;
  confidence: number;   // 0-1
  supersededBy?: string; // ID of relationship that contradicts this
}

export class RelationshipStore {
  private db: Database.Database;
  
  constructor(db: Database.Database) {
    this.db = db;
    this.createTables();
  }
  
  private createTables(): void {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS kg_relationships (
        id TEXT PRIMARY KEY,
        source TEXT NOT NULL,
        target TEXT NOT NULL,
        type TEXT NOT NULL,
        value TEXT,
        timestamp TEXT NOT NULL,
        session_id TEXT,
        confidence REAL DEFAULT 1.0,
        superseded_by TEXT
      );
      
      CREATE INDEX IF NOT EXISTS idx_kg_rel_source ON kg_relationships(source);
      CREATE INDEX IF NOT EXISTS idx_kg_rel_target ON kg_relationships(target);
      CREATE INDEX IF NOT EXISTS idx_kg_rel_type ON kg_relationships(type);
      CREATE INDEX IF NOT EXISTS idx_kg_rel_timestamp ON kg_relationships(timestamp);
    `);
  }
  
  /**
   * Add a relationship
   * Returns the relationship and any superseded relationship
   */
  addRelationship(rel: Omit<Relationship, 'id'>): { relationship: Relationship; superseded?: Relationship } {
    const id = `rel_${uuidv4().slice(0, 8)}`;
    
    // Check for contradictions (same source, type, different value, not already superseded)
    const conflicting = this.findContradiction(rel.source, rel.type, rel.value);
    
    let supersededBy: string | undefined;
    let supersededRel: Relationship | undefined;
    
    if (conflicting) {
      // Mark the old relationship as superseded by the NEW relationship
      // UPDATE superseded_by = ? (new id) WHERE id = ? (old id)
      // Arguments: new_id, old_id
      const updateStmt = this.db.prepare(`
        UPDATE kg_relationships SET superseded_by = ? WHERE id = ?
      `);
      updateStmt.run(id, conflicting.id);
      supersededBy = id;
      supersededRel = conflicting;
    }
    
    // Insert new relationship (should NOT set superseded_by to itself!)
    const stmt = this.db.prepare(`
      INSERT INTO kg_relationships (id, source, target, type, value, timestamp, session_id, confidence, superseded_by)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);
    
    stmt.run(
      id,
      rel.source,
      rel.target,
      rel.type,
      rel.value || null,
      rel.timestamp,
      rel.sessionId || null,
      rel.confidence,
      null  // Not superseded when created
    );
    
    return {
      relationship: this.getById(id)!,
      superseded: supersededRel
    };
  }
  
  /**
   * Find contradiction (same source, same type, different value, not superseded)
   */
  private findContradiction(source: string, type: string, value?: string): Relationship | null {
    if (!value) return null;
    
    const stmt = this.db.prepare(`
      SELECT * FROM kg_relationships 
      WHERE source = ? AND type = ? AND value != ? AND superseded_by IS NULL
      ORDER BY timestamp DESC
      LIMIT 1
    `);
    
    const row = stmt.get(source, type, value) as any;
    if (!row) return null;
    
    return this.rowToRelationship(row);
  }
  
  /**
   * Get relationship by ID
   */
  getById(id: string): Relationship | null {
    const stmt = this.db.prepare('SELECT * FROM kg_relationships WHERE id = ?');
    const row = stmt.get(id) as any;
    
    if (!row) return null;
    return this.rowToRelationship(row);
  }
  
  /**
   * Get relationships from a source entity
   */
  getBySource(sourceId: string): Relationship[] {
    const stmt = this.db.prepare('SELECT * FROM kg_relationships WHERE source = ? ORDER BY timestamp DESC');
    const rows = stmt.all(sourceId) as any[];
    
    return rows.map(row => this.rowToRelationship(row));
  }
  
  /**
   * Get relationships to a target entity
   */
  getByTarget(targetId: string): Relationship[] {
    const stmt = this.db.prepare('SELECT * FROM kg_relationships WHERE target = ? ORDER BY timestamp DESC');
    const rows = stmt.all(targetId) as any[];
    
    return rows.map(row => this.rowToRelationship(row));
  }
  
  /**
   * Get relationships by type
   */
  getByType(type: RelationshipType): Relationship[] {
    const stmt = this.db.prepare('SELECT * FROM kg_relationships WHERE type = ? ORDER BY timestamp DESC');
    const rows = stmt.all(type) as any[];
    
    return rows.map(row => this.rowToRelationship(row));
  }
  
  /**
   * Get temporal history for an entity and relationship type
   * Returns all versions ordered chronologically
   */
  getHistory(sourceId: string, type?: RelationshipType): Relationship[] {
    let query = 'SELECT * FROM kg_relationships WHERE source = ?';
    const params: any[] = [sourceId];
    
    if (type) {
      query += ' AND type = ?';
      params.push(type);
    }
    
    query += ' ORDER BY timestamp ASC'; // Chronological order
    
    const stmt = this.db.prepare(query);
    const rows = stmt.all(...params) as any[];
    
    return rows.map(row => this.rowToRelationship(row));
  }
  
  /**
   * Get current (non-superseded) relationship for entity + type
   */
  getCurrent(sourceId: string, type: RelationshipType): Relationship | null {
    const stmt = this.db.prepare(`
      SELECT * FROM kg_relationships 
      WHERE source = ? AND type = ? AND superseded_by IS NULL
      ORDER BY timestamp DESC
      LIMIT 1
    `);
    
    const row = stmt.get(sourceId, type) as any;
    if (!row) return null;
    
    return this.rowToRelationship(row);
  }
  
  /**
   * Get all relationships
   */
  getAll(): Relationship[] {
    const stmt = this.db.prepare('SELECT * FROM kg_relationships ORDER BY timestamp DESC');
    const rows = stmt.all() as any[];
    
    return rows.map(row => this.rowToRelationship(row));
  }
  
  /**
   * Get relationships by session
   */
  getBySession(sessionId: string): Relationship[] {
    const stmt = this.db.prepare('SELECT * FROM kg_relationships WHERE session_id = ? ORDER BY timestamp DESC');
    const rows = stmt.all(sessionId) as any[];
    
    return rows.map(row => this.rowToRelationship(row));
  }
  
  /**
   * Find all active contradictions (relationships that have been superseded)
   */
  getContradictions(): { current: Relationship; superseded: Relationship }[] {
    const stmt = this.db.prepare(`
      SELECT r.*, s.value as superseded_value
      FROM kg_relationships r
      LEFT JOIN kg_relationships s ON r.superseded_by = s.id
      WHERE r.superseded_by IS NOT NULL
      ORDER BY r.timestamp DESC
    `);
    
    const rows = stmt.all() as any[];
    const contradictions: { current: Relationship; superseded: Relationship }[] = [];
    
    for (const row of rows) {
      const current = this.rowToRelationship(row);
      if (row.superseded_by) {
        const superseded = this.getById(row.superseded_by);
        if (superseded) {
          contradictions.push({ current, superseded });
        }
      }
    }
    
    return contradictions;
  }
  
  /**
   * Get all superseded relationships
   */
  getSuperseded(): Relationship[] {
    const stmt = this.db.prepare('SELECT * FROM kg_relationships WHERE superseded_by IS NOT NULL ORDER BY timestamp DESC');
    const rows = stmt.all() as any[];
    
    return rows.map(row => this.rowToRelationship(row));
  }
  
  private rowToRelationship(row: any): Relationship {
    return {
      id: row.id,
      source: row.source,
      target: row.target,
      type: row.type,
      value: row.value,
      timestamp: row.timestamp,
      sessionId: row.session_id,
      confidence: row.confidence,
      supersededBy: row.superseded_by
    };
  }
}
