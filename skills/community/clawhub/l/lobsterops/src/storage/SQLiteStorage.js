const { StorageAdapter } = require('./StorageAdapter');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

/**
 * SQLite Storage Backend
 * Lightweight, file-based SQL database that works everywhere
 * Better performance than JSON files for querying and scaling
 */
class SQLiteStorage extends StorageAdapter {
  /**
   * @param {Object} config - Configuration options
   * @param {string} config.filename - SQLite database file path (default: ./lobsterops.db)
   * @param {boolean} config.verbose - Whether to log SQLite errors (default: false)
   */
  constructor(config = {}) {
    super();
    this.filename = config.filename || './lobsterops.db';
    this.verbose = config.verbose || false;
    this.db = null;
    this.initialized = false;
    
    // Ensure directory exists for the database file
    this._ensureDirectory();
  }

  async init() {
    if (this.initialized) return Promise.resolve();
    
    return new Promise((resolve, reject) => {
      this.db = new sqlite3.Database(this.filename, (err) => {
        if (err) {
          if (this.verbose) console.error('SQLite connection error:', err);
          reject(new Error(`Failed to connect to SQLite: ${err.message}`));
          return;
        }
        
        // Enable foreign key constraints
        this.db.run('PRAGMA foreign_keys = ON;', (err) => {
          if (err) {
            if (this.verbose) console.error('SQLite PRAGMA error:', err);
            // Continue anyway - this isn't critical
          }
          
          // Create tables if they don't exist
          this.db.serialize(() => {
            // Events table
            this.db.run(`
              CREATE TABLE IF NOT EXISTS lobsterops_events (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                agentId TEXT,
                action TEXT,
                timestamp TEXT NOT NULL,
                storedAt TEXT NOT NULL,
                data TEXT, -- JSON string of the event data
                updatedAt TEXT
              )
            `, (err) => {
              if (err) {
                if (this.verbose) console.error('SQLite table creation error:', err);
                reject(new Error(`Failed to create tables: ${err.message}`));
                return;
              }
              
              // Indexes for common query patterns
              this.db.run(`
                CREATE INDEX IF NOT EXISTS idx_events_timestamp 
                ON lobsterops_events(timestamp)
              `, (err) => {
                if (err && this.verbose) console.error('Index creation warning:', err);
                
                this.db.run(`
                  CREATE INDEX IF NOT EXISTS idx_events_type 
                  ON lobsterops_events(type)
                `, (err) => {
                  if (err && this.verbose) console.error('Index creation warning:', err);
                  
                  this.db.run(`
                    CREATE INDEX IF NOT EXISTS idx_events_agentId 
                    ON lobsterops_events(agentId)
                  `, (err) => {
                    if (err && this.verbose) console.error('Index creation warning:', err);
                    
                    this.db.run(`
                      CREATE INDEX IF NOT EXISTS idx_events_action 
                      ON lobsterops_events(action)
                    `, (err) => {
                      if (err && this.verbose) console.error('Index creation warning:', err);
                      this.initialized = true;
                      resolve();
                    });
                  });
                });
              });
            });
          });
        });
      });
    });
  }

  _executeQuery(sql, params = []) {
    if (!this.initialized || !this.db) {
      return Promise.reject(new Error('Storage not initialized'));
    }
    
    return new Promise((resolve, reject) => {
      this.db.all(sql, params, (err, rows) => {
        if (err) {
          if (this.verbose) console.error('SQLite query error:', err, sql, params);
          reject(new Error(`Database query failed: ${err.message}`));
          return;
        }
        resolve(rows);
      });
    });
  }

  _executeRun(sql, params = []) {
    if (!this.initialized || !this.db) {
      return Promise.reject(new Error('Storage not initialized'));
    }
    
    return new Promise((resolve, reject) => {
      this.db.run(sql, params, function(err) {
        if (err) {
          if (this.verbose) console.error('SQLite run error:', err, sql, params);
          reject(new Error(`Database operation failed: ${err.message}`));
          return;
        }
        resolve(this);
      });
    });
  }

  async saveEvent(event) {
    if (!this.initialized) await this.init();
    
    try {
      const enrichedEvent = {
        ...event,
        id: event.id || this._generateId(),
        timestamp: event.timestamp || new Date().toISOString(),
        storedAt: new Date().toISOString()
      };
      
      const dataJson = JSON.stringify(enrichedEvent);
      
      await this._executeRun(
        `INSERT INTO lobsterops_events (id, type, agentId, action, timestamp, storedAt, data) 
         VALUES (?, ?, ?, ?, ?, ?, ?)`,
        [
          enrichedEvent.id,
          enrichedEvent.type,
          enrichedEvent.agentId || null,
          enrichedEvent.action || null,
          enrichedEvent.timestamp,
          enrichedEvent.storedAt,
          dataJson
        ]
      );
      
      return enrichedEvent.id;
    } catch (error) {
      throw new Error(`Failed to save event: ${error.message}`);
    }
  }

  async queryEvents(filter = {}, options = {}) {
    if (!this.initialized) await this.init();
    
    try {
      const {
        startDate, endDate, eventTypes, agentIds, actions, 
        limit = 100, offset = 0, 
        sortBy = 'timestamp', sortOrder = 'desc'
      } = { 
        startDate: null, endDate: null, eventTypes: [], agentIds: [], actions: [],
        limit: 100, offset: 0, sortBy: 'timestamp', sortOrder: 'desc' 
      , ...filter, ...options };

      // Validate sort direction
      const validSortOrder = sortOrder.toLowerCase() === 'asc' ? 'ASC' : 'DESC';
      
      // Build WHERE clause and parameters
      let whereClause = '1=1'; // Start with always true
      const params = [];
      
      if (startDate) {
        whereClause += ' AND timestamp >= ?';
        params.push(startDate);
      }
      
      if (endDate) {
        whereClause += ' AND timestamp <= ?';
        params.push(endDate);
        }
      
      if (eventTypes.length > 0) {
        const placeholders = eventTypes.map(() => '?').join(',');
        whereClause += ` AND type IN (${placeholders})`;
        params.push(...eventTypes);
      }
      
      if (agentIds.length > 0) {
        const placeholders = agentIds.map(() => '?').join(',');
        whereClause += ` AND agentId IN (${placeholders})`;
        params.push(...agentIds);
      }
      
      if (actions.length > 0) {
        const placeholders = actions.map(() => '?').join(',');
        whereClause += ` AND action IN (${placeholders})`;
        params.push(...actions);
      }
      
      // Build and execute query
      const query = `
        SELECT * FROM lobsterops_events 
        WHERE ${whereClause}
        ORDER BY ${sortBy} ${validSortOrder}
        LIMIT ? OFFSET ?
      `;
      
      params.push(limit, offset);
      
      const rows = await this._executeQuery(query, params);
      
      // Parse JSON data back to objects
      const events = rows.map(row => {
        let parsedData;
        try {
          parsedData = JSON.parse(row.data);
        } catch (e) {
          // If JSON parsing fails, return raw data
          parsedData = row.data;
        }
        
        return {
          id: row.id,
          type: row.type,
          agentId: row.agentId,
          action: row.action,
          timestamp: row.timestamp,
          storedAt: row.storedAt,
          updatedAt: row.updatedAt,
          ...parsedData
        };
      });
      
      return events;
    } catch (error) {
      throw new Error(`Failed to query events: ${error.message}`);
    }
  }

  async getEventById(eventId) {
    if (!this.initialized) await this.init();
    
    try {
      const rows = await this._executeQuery(
        `SELECT * FROM lobsterops_events WHERE id = ?`,
        [eventId]
      );
      
      if (rows.length === 0) {
        return null;
      }
      
      const row = rows[0];
      let parsedData;
      try {
        parsedData = JSON.parse(row.data);
      } catch (e) {
        parsedData = row.data;
      }
      
      return {
        id: row.id,
        type: row.type,
        agentId: row.agentId,
        action: row.action,
        timestamp: row.timestamp,
        storedAt: row.storedAt,
        updatedAt: row.updatedAt,
        ...parsedData
      };
    } catch (error) {
      throw new Error(`Failed to get event: ${error.message}`);
    }
  }

  async updateEvent(eventId, updates) {
    if (!this.initialized) await this.init();
    
    try {
      // Add updatedAt timestamp
      const updateWithTime = {
        ...updates,
        updatedAt: new Date().toISOString()
      };
      
      // Get current event to merge updates
      const currentEvent = await this.getEventById(eventId);
      if (!currentEvent) {
        return false; // Event not found
      }
      
      const mergedEvent = {
        ...currentEvent,
        ...updateWithTime
      };
      
      const dataJson = JSON.stringify(mergedEvent);
      
      await this._executeRun(
        `UPDATE lobsterops_events 
         SET data = ?, updatedAt = ? 
         WHERE id = ?`,
        [dataJson, updateWithTime.updatedAt, eventId]
      );
      
      return true;
    } catch (error) {
      throw new Error(`Failed to update event: ${error.message}`);
    }
  }

  async deleteEvents(filter = {}) {
    if (!this.initialized) await this.init();
    
    try {
      const {
        startDate, endDate, eventTypes, agentIds, actions
      } = { 
        startDate: null, endDate: null, eventTypes: [], agentIds: [], actions: [] 
      , ...filter };

      // Build WHERE clause and parameters
      let whereClause = '1=1'; // Start with always true
      const params = [];
      
      if (startDate) {
        whereClause += ' AND timestamp >= ?';
        params.push(startDate);
      }
      
      if (endDate) {
        whereClause += ' AND timestamp <= ?';
        params.push(endDate);
      }
      
      if (eventTypes.length > 0) {
        const placeholders = eventTypes.map(() => '?').join(',');
        whereClause += ` AND type IN (${placeholders})`;
        params.push(...eventTypes);
      }
      
      if (agentIds.length > 0) {
        const placeholders = agentIds.map(() => '?').join(',');
        whereClause += ` AND agentId IN (${placeholders})`;
        params.push(...agentIds);
      }
      
      if (actions.length > 0) {
        const placeholders = actions.map(() => '?').join(',');
        whereClause += ` AND action IN (${placeholders})`;
        params.push(...actions);
      }
      
      // First, get count of events to delete (for return value)
      const countResult = await this._executeQuery(
        `SELECT COUNT(*) as count FROM lobsterops_events WHERE ${whereClause}`,
        params
      );
      
      const countToDelete = countResult[0].count;
      
      // Then perform the deletion
      await this._executeRun(
        `DELETE FROM lobsterops_events WHERE ${whereClause}`,
        params
      );
      
      return countToDelete;
    } catch (error) {
      throw new Error(`Failed to delete events: ${error.message}`);
    }
  }

  async cleanupOld(maxAgeDays = 30) {
    if (!this.initialized) await this.init();

    try {
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - maxAgeDays);
      const cutoffISO = cutoffDate.toISOString();

      // Count events to delete
      const countResult = await this._executeQuery(
        'SELECT COUNT(*) as count FROM lobsterops_events WHERE timestamp < ?',
        [cutoffISO]
      );
      const countToDelete = countResult[0].count;

      if (countToDelete === 0) return 0;

      // Delete old events
      await this._executeRun(
        'DELETE FROM lobsterops_events WHERE timestamp < ?',
        [cutoffISO]
      );

      return countToDelete;
    } catch (error) {
      throw new Error(`Failed to cleanup old events: ${error.message}`);
    }
  }

  async getStats() {
    if (!this.initialized) await this.init();
    
    try {
      // Get total count
      const countResult = await this._executeQuery(`SELECT COUNT(*) as count FROM lobsterops_events`);
      const count = countResult[0].count;
      
      // Get size info (approximate)
      const sizeResult = await this._executeQuery(`SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()`);
      const sizeInBytes = sizeResult[0].size || 0;
      
      return {
        backend: 'sqlite',
        filename: this.filename,
        eventCount: count,
        databaseSizeBytes: sizeInBytes,
        databaseSizeMB: Number((sizeInBytes / (1024 * 1024)).toFixed(2))
      };
    } catch (error) {
      throw new Error(`Failed to get stats: ${error.message}`);
    }
  }

  async close() {
    if (this.db) {
      return new Promise((resolve, reject) => {
        this.db.close((err) => {
          if (err) {
            if (this.verbose) console.error('SQLite close error:', err);
            reject(new Error(`Failed to close database: ${err.message}`));
            return;
          }
          this.initialized = false;
          resolve();
        });
      });
    }
    this.initialized = false;
    return Promise.resolve();
  }

  /**
   * Ensure the directory for the database file exists
   * @private
   */
  _ensureDirectory() {
    const dir = path.dirname(this.filename);
    if (dir && dir !== '.') {
      const fs = require('fs').promises;
      fs.mkdir(dir, { recursive: true }).catch(() => {
        // Ignore if directory already exists or we can't create it
      });
    }
  }

  /**
   * Generate a simple unique ID
   * @returns {string} - Unique ID
   */
  _generateId() {
    return Math.random().toString(36).substr(2, 9) + 
           Date.now().toString(36) +
           Math.random().toString(36).substr(2, 9);
  }
}

module.exports = { SQLiteStorage };