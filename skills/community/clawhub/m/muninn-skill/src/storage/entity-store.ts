/**
 * Entity Store for Knowledge Graph
 * Stores entities with aliases, mentions, and timestamps
 */

import Database from 'better-sqlite3';
import { v4 as uuidv4 } from 'uuid';

export type EntityType = 'organization' | 'person' | 'project' | 'technology' | 'location';

export interface Entity {
  id: string;
  name: string;
  type: EntityType;
  aliases: string[];
  mentions: number;
  firstSeen: string;
  lastSeen: string;
}

export class EntityStore {
  private db: Database.Database;
  
  constructor(db: Database.Database) {
    this.db = db;
    this.createTables();
  }
  
  private createTables(): void {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS kg_entities (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        aliases TEXT DEFAULT '[]',
        mentions INTEGER DEFAULT 1,
        first_seen TEXT NOT NULL,
        last_seen TEXT NOT NULL
      );
      
      CREATE INDEX IF NOT EXISTS idx_kg_entities_type ON kg_entities(type);
      CREATE INDEX IF NOT EXISTS idx_kg_entities_name ON kg_entities(name);
    `);
  }
  
  /**
   * Add or update an entity
   */
  addEntity(entity: Omit<Entity, 'id' | 'mentions' | 'firstSeen' | 'lastSeen'> & { firstSeen?: string; lastSeen?: string }): Entity {
    const now = new Date().toISOString();
    const existing = this.getByName(entity.name);
    
    if (existing) {
      // Update existing entity
      const aliases = [...new Set([...existing.aliases, ...entity.aliases])];
      const stmt = this.db.prepare(`
        UPDATE kg_entities 
        SET aliases = ?, mentions = mentions + 1, last_seen = ?
        WHERE name = ?
      `);
      stmt.run(JSON.stringify(aliases), now, entity.name);
      
      return this.getByName(entity.name)!;
    }
    
    // Create new entity
    const id = `ent_${uuidv4().slice(0, 8)}`;
    const stmt = this.db.prepare(`
      INSERT INTO kg_entities (id, name, type, aliases, mentions, first_seen, last_seen)
      VALUES (?, ?, ?, ?, 1, ?, ?)
    `);
    
    stmt.run(
      id,
      entity.name,
      entity.type,
      JSON.stringify(entity.aliases),
      entity.firstSeen || now,
      entity.lastSeen || now
    );
    
    return this.getById(id)!;
  }
  
  /**
   * Get entity by ID
   */
  getById(id: string): Entity | null {
    const stmt = this.db.prepare('SELECT * FROM kg_entities WHERE id = ?');
    const row = stmt.get(id) as any;
    
    if (!row) return null;
    
    return {
      ...row,
      aliases: JSON.parse(row.aliases || '[]')
    };
  }
  
  /**
   * Get entity by name (case-insensitive)
   */
  getByName(name: string): Entity | null {
    const stmt = this.db.prepare('SELECT * FROM kg_entities WHERE LOWER(name) = LOWER(?)');
    const row = stmt.get(name) as any;
    
    if (!row) return null;
    
    return {
      ...row,
      aliases: JSON.parse(row.aliases || '[]')
    };
  }
  
  /**
   * Get all entities of a specific type
   */
  getByType(type: EntityType): Entity[] {
    const stmt = this.db.prepare('SELECT * FROM kg_entities WHERE type = ? ORDER BY mentions DESC');
    const rows = stmt.all(type) as any[];
    
    return rows.map(row => ({
      ...row,
      aliases: JSON.parse(row.aliases || '[]')
    }));
  }
  
  /**
   * Get all entities
   */
  getAll(): Entity[] {
    const stmt = this.db.prepare('SELECT * FROM kg_entities ORDER BY mentions DESC');
    const rows = stmt.all() as any[];
    
    return rows.map(row => ({
      ...row,
      aliases: JSON.parse(row.aliases || '[]')
    }));
  }
  
  /**
   * Find entity by exact name or alias
   */
  findEntity(nameOrAlias: string): Entity | null {
    // Try exact name match first
    const byName = this.getByName(nameOrAlias);
    if (byName) return byName;
    
    // Search aliases
    const stmt = this.db.prepare('SELECT * FROM kg_entities WHERE aliases LIKE ?');
    const rows = stmt.all(`%${nameOrAlias}%`) as any[];
    
    for (const row of rows) {
      const aliases = JSON.parse(row.aliases || '[]') as string[];
      if (aliases.some(a => a.toLowerCase() === nameOrAlias.toLowerCase())) {
        return {
          ...row,
          aliases
        };
      }
    }
    
    return null;
  }
  
  /**
   * Get entity history (all updates)
   */
  getHistory(entityName: string): { mentions: number; lastSeen: string }[] {
    // Since we don't track history in the current schema, return current state
    const entity = this.getByName(entityName);
    if (!entity) return [];
    
    return [{
      mentions: entity.mentions,
      lastSeen: entity.lastSeen
    }];
  }
}
