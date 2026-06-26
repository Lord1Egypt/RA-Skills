/**
 * Canonical Entity Table
 * 
 * Solves the Single-Hop factual recall problem by assigning unique IDs
 * to all entities, regardless of how they're referenced.
 * 
 * Example:
 * - "BHP" → ORG_001
 * - "the client" → ORG_001 (same entity)
 * - "Phillip" → PERSON_001
 * - "he" → PERSON_001 (after coreference resolution)
 * 
 * This ensures all facts about an entity are linked, even if mentioned
 * with different names or pronouns.
 */

import type { Database as SQLiteDatabase } from 'better-sqlite3';

export interface CanonicalEntity {
  id: string;           // Unique ID: PERSON_001, ORG_001, PROJECT_001
  canonicalName: string; // Primary name: "Phillip", "BHP", "Muninn"
  aliases: string[];    // All known references: ["he", "him", "the founder"]
  type: 'person' | 'org' | 'project' | 'location' | 'event' | 'concept';
  firstMentioned: string; // ISO date
  lastMentioned: string;  // ISO date
  mentionCount: number;
  metadata?: Record<string, any>;
}

export class CanonicalEntityTable {
  private db: SQLiteDatabase;
  
  constructor(db: SQLiteDatabase) {
    this.db = db;
    this.initTable();
  }
  
  private initTable(): void {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS canonical_entities (
        id TEXT PRIMARY KEY,
        canonical_name TEXT NOT NULL,
        aliases TEXT NOT NULL DEFAULT '[]',
        type TEXT NOT NULL DEFAULT 'concept',
        first_mentioned TEXT NOT NULL,
        last_mentioned TEXT NOT NULL,
        mention_count INTEGER DEFAULT 1,
        metadata TEXT
      );
      
      CREATE INDEX IF NOT EXISTS idx_entity_canonical ON canonical_entities(canonical_name);
      CREATE INDEX IF NOT EXISTS idx_entity_type ON canonical_entities(type);
    `);
  }
  
  /**
   * Find an entity by any of its aliases or canonical name
   */
  findByAlias(name: string): CanonicalEntity | null {
    // Try exact match on canonical name first
    const exact = this.db.prepare(`
      SELECT * FROM canonical_entities WHERE canonical_name = ?
    `).get(name) as any;
    
    if (exact) return this.fromRow(exact);
    
    // Try alias match (JSON array contains)
    const aliasMatch = this.db.prepare(`
      SELECT * FROM canonical_entities WHERE aliases LIKE ?
    `).get(`%"${name}"%`) as any;
    
    if (aliasMatch) return this.fromRow(aliasMatch);
    
    return null;
  }
  
  /**
   * Register a new entity or update an existing one
   */
  register(
    name: string,
    type: CanonicalEntity['type'],
    aliases: string[] = [],
    metadata?: Record<string, any>
  ): CanonicalEntity {
    // Check if exists
    const existing = this.findByAlias(name);
    
    if (existing) {
      // Update: add new aliases, increment count
      const newAliases = [...new Set([...existing.aliases, name, ...aliases])];
      this.db.prepare(`
        UPDATE canonical_entities 
        SET aliases = ?, last_mentioned = ?, mention_count = mention_count + 1
        WHERE id = ?
      `).run(JSON.stringify(newAliases), new Date().toISOString(), existing.id);
      
      return { ...existing, aliases: newAliases, mentionCount: existing.mentionCount + 1 };
    }
    
    // Create new entity
    const typePrefix = {
      person: 'PERSON',
      org: 'ORG',
      project: 'PROJECT',
      location: 'LOC',
      event: 'EVENT',
      concept: 'CONCEPT'
    }[type] || 'ENTITY';
    
    // Get next ID number
    const count = this.db.prepare(`
      SELECT COUNT(*) as count FROM canonical_entities WHERE type = ?
    `).get(type) as any;
    
    const id = `${typePrefix}_${String(count.count + 1).padStart(3, '0')}`;
    
    this.db.prepare(`
      INSERT INTO canonical_entities (id, canonical_name, aliases, type, first_mentioned, last_mentioned, mention_count, metadata)
      VALUES (?, ?, ?, ?, ?, ?, 1, ?)
    `).run(
      id,
      name,
      JSON.stringify([name, ...aliases]),
      type,
      new Date().toISOString(),
      new Date().toISOString(),
      metadata ? JSON.stringify(metadata) : null
    );
    
    return {
      id,
      canonicalName: name,
      aliases: [name, ...aliases],
      type,
      firstMentioned: new Date().toISOString(),
      lastMentioned: new Date().toISOString(),
      mentionCount: 1,
      metadata
    };
  }
  
  /**
   * Link an alias to an existing entity
   */
  linkAlias(entityId: string, alias: string): void {
    const entity = this.db.prepare(`
      SELECT * FROM canonical_entities WHERE id = ?
    `).get(entityId) as any;
    
    if (!entity) return;
    
    const aliases = JSON.parse(entity.aliases || '[]');
    if (!aliases.includes(alias)) {
      aliases.push(alias);
      this.db.prepare(`
        UPDATE canonical_entities SET aliases = ? WHERE id = ?
      `).run(JSON.stringify(aliases), entityId);
    }
  }
  
  /**
   * Get all entities of a type
   */
  getByType(type: CanonicalEntity['type']): CanonicalEntity[] {
    const rows = this.db.prepare(`
      SELECT * FROM canonical_entities WHERE type = ? ORDER BY mention_count DESC
    `).all(type) as any[];
    
    return rows.map(r => this.fromRow(r));
  }
  
  /**
   * Get most mentioned entities (for importance ranking)
   */
  getTopEntities(limit: number = 10): CanonicalEntity[] {
    const rows = this.db.prepare(`
      SELECT * FROM canonical_entities ORDER BY mention_count DESC LIMIT ?
    `).all(limit) as any[];
    
    return rows.map(r => this.fromRow(r));
  }
  
  /**
   * Resolve a mention to its canonical entity ID
   * Returns null if not found (new entity)
   */
  resolve(mention: string): string | null {
    const entity = this.findByAlias(mention);
    return entity?.id || null;
  }
  
  /**
   * Get canonical name for an entity ID
   */
  getCanonicalName(entityId: string): string | null {
    const row = this.db.prepare(`
      SELECT canonical_name FROM canonical_entities WHERE id = ?
    `).get(entityId) as any;
    
    return row?.canonical_name || null;
  }
  
  /**
   * Merge two entities (for deduplication)
   */
  merge(primaryId: string, secondaryId: string): void {
    const primary = this.db.prepare(`
      SELECT * FROM canonical_entities WHERE id = ?
    `).get(primaryId) as any;
    const secondary = this.db.prepare(`
      SELECT * FROM canonical_entities WHERE id = ?
    `).get(secondaryId) as any;
    
    if (!primary || !secondary) return;
    
    // Merge aliases
    const mergedAliases = [...new Set([
      ...JSON.parse(primary.aliases || '[]'),
      ...JSON.parse(secondary.aliases || '[]')
    ])];
    
    // Update primary
    this.db.prepare(`
      UPDATE canonical_entities 
      SET aliases = ?, mention_count = ? 
      WHERE id = ?
    `).run(
      JSON.stringify(mergedAliases),
      primary.mention_count + secondary.mention_count,
      primaryId
    );
    
    // Delete secondary
    this.db.prepare(`DELETE FROM canonical_entities WHERE id = ?`).run(secondaryId);
  }
  
  private fromRow(row: any): CanonicalEntity {
    return {
      id: row.id,
      canonicalName: row.canonical_name,
      aliases: JSON.parse(row.aliases || '[]'),
      type: row.type,
      firstMentioned: row.first_mentioned,
      lastMentioned: row.last_mentioned,
      mentionCount: row.mention_count,
      metadata: row.metadata ? JSON.parse(row.metadata) : undefined
    };
  }
}