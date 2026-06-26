const { StorageAdapter } = require('./StorageAdapter');
const fs = require('fs').promises;
const path = require('path');

/**
 * JSON File Storage Backend
 * Zero-dependency storage that works anywhere with file system access
 * Stores events as daily JSON files for easy portability and backup
 */
class JsonFileStorage extends StorageAdapter {
  /**
   * @param {Object} config - Configuration options
   * @param {string} config.dataDir - Directory to store JSON files (default: ./lobsterops-data)
   * @param {number} config.maxAgeDays - Maximum age of files to keep (default: 30)
   */
  constructor(config = {}) {
    super();
    this.dataDir = config.dataDir || './lobsterops-data';
    this.maxAgeDays = config.maxAgeDays || 30;
    this.filePrefix = 'lobsterops-events-';
    this.initialized = false;
  }

  async init() {
    try {
      // Ensure data directory exists
      await fs.mkdir(this.dataDir, { recursive: true });
      
      this.initialized = true;
      
      // Run initial cleanup of old files
      await this.cleanupOld();
    } catch (error) {
      throw new Error(`Failed to initialize JsonFileStorage: ${error.message}`);
    }
  }

  /**
   * Get the filename for a given date
   * @param {Date} date - The date to get filename for
   * @returns {string} - Filename for the date
   */
  _getFilenameForDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${this.filePrefix}${year}-${month}-${day}.json`;
  }

  /**
   * Get today's filename
   * @returns {string} - Today's filename
   */
  _getTodayFilename() {
    return this._getFilenameForDate(new Date());
  }

  /**
   * Read events from a JSON file
   * @param {string} filename - The filename to read from
   * @returns {Promise<Array>} - Events stored in the file
   */
  async _readEventsFromFile(filename) {
    try {
      const filepath = path.join(this.dataDir, filename);
      const data = await fs.readFile(filepath, 'utf8');
      const parsed = JSON.parse(data);
      return Array.isArray(parsed) ? parsed : [];
    } catch (error) {
      // If file doesn't exist or is invalid JSON, return empty array
      if (error.code === 'ENOENT' || error instanceof SyntaxError) {
        return [];
      }
      throw error;
    }
  }

  /**
   * Write events to a JSON file
   * @param {string} filename - The filename to write to
   * @param {Array} events - Events to write
   * @returns {Promise<void>}
   */
  async _writeEventsToFile(filename, events) {
    const filepath = path.join(this.dataDir, filename);
    const data = JSON.stringify(events, null, 2);
    await fs.writeFile(filepath, data, 'utf8');
  }

  async saveEvent(event) {
    if (!this.initialized) await this.init();
    
    try {
      // Add metadata to the event
      const enrichedEvent = {
        ...event,
        id: event.id || this._generateId(),
        timestamp: event.timestamp || new Date().toISOString(),
        storedAt: new Date().toISOString()
      };

      // Get today's events
      const todayFilename = this._getTodayFilename();
      let events = await this._readEventsFromFile(todayFilename);
      
      // Add the new event
      events.push(enrichedEvent);
      
      // Write back to file
      await this._writeEventsToFile(todayFilename, events);
      
      return enrichedEvent.id;
    } catch (error) {
      throw new Error(`Failed to save event: ${error.message}`);
    }
  }

  async queryEvents(filter = {}, options = {}) {
    if (!this.initialized) await this.init();
    
    try {
      const {
        startDate, endDate, eventTypes, agentIds, limit = 100, offset = 0, sortBy = 'timestamp', sortOrder = 'desc'
      } = { 
        startDate: null, endDate: null, eventTypes: [], agentIds: [], 
        limit: 100, offset: 0, sortBy: 'timestamp', sortOrder: 'desc' 
      , ...filter, ...options };

      // Determine which date ranges we need to check
      const filesToCheck = this._getFilesInDateRange(startDate, endDate);
      
      // Collect all matching events
      let allEvents = [];
      for (const filename of filesToCheck) {
        const events = await this._readEventsFromFile(filename);
        allEvents = [...allEvents, ...events];
      }
      
      // Apply filters
      let filteredEvents = allEvents;
      
      if (startDate) {
        const start = new Date(startDate);
        filteredEvents = filteredEvents.filter(event => new Date(event.timestamp) >= start);
      }
      
      if (endDate) {
        const end = new Date(endDate);
        filteredEvents = filteredEvents.filter(event => new Date(event.timestamp) <= end);
      }
      
      if (eventTypes.length > 0) {
        filteredEvents = filteredEvents.filter(event => eventTypes.includes(event.type));
      }
      
      if (agentIds.length > 0) {
        filteredEvents = filteredEvents.filter(event => agentIds.includes(event.agentId));
      }
      
      // Apply sorting
      const reverse = sortOrder.toLowerCase() === 'desc';
      filteredEvents.sort((a, b) => {
        const aVal = new Date(a[sortBy]);
        const bVal = new Date(b[sortBy]);
        return reverse ? bVal - aVal : aVal - bVal;
      });
      
      // Apply pagination
      const startIdx = offset;
      const endIdx = offset + limit;
      const paginatedEvents = filteredEvents.slice(startIdx, endIdx);
      
      return paginatedEvents;
    } catch (error) {
      throw new Error(`Failed to query events: ${error.message}`);
    }
  }

  /**
   * Get list of files to check based on date range
   * @param {Date|null} startDate - Start of date range (inclusive)
   * @param {Date|null} endDate - End of date range (inclusive)
   * @returns {Array<string>} - List of filenames to check
   */
  _getFilesInDateRange(startDate, endDate) {
    const files = [];
    
    // If no date range specified, just check today
    if (!startDate && !endDate) {
      return [this._getTodayFilename()];
    }
    
    const start = startDate ? new Date(startDate) : new Date(0);
    const end = endDate ? new Date(endDate) : new Date();
    
    // Clamp start to reasonable minimum (avoid checking years of empty files)
    const clampedStart = new Date(Math.max(start.getTime(), Date.now() - (this.maxAgeDays + 1) * 24 * 60 * 60 * 1000));
    
    let current = new Date(clampedStart);
    while (current <= end) {
      files.push(this._getFilenameForDate(new Date(current)));
      current.setDate(current.getDate() + 1);
    }
    
    return files;
  }

  async getEventById(eventId) {
    if (!this.initialized) await this.init();
    
    try {
      // We'll need to search through files to find the event
      // For efficiency in production, you'd want an index, but for simplicity
      // we'll search recent files first
      const filesToCheck = this._getFilesInDateRange(
        null, 
        new Date(Date.now() + 24 * 60 * 60 * 1000) // Today + 1 day to be safe
      );
      
      // Search from most recent to oldest (more likely to find recent events)
      for (let i = filesToCheck.length - 1; i >= 0; i--) {
        const filename = filesToCheck[i];
        const events = await this._readEventsFromFile(filename);
        const event = events.find(e => e.id === eventId);
        if (event) {
          return event;
        }
      }
      
      return null; // Not found
    } catch (error) {
      throw new Error(`Failed to get event by ID: ${error.message}`);
    }
  }

  async updateEvent(eventId, updates) {
    if (!this.initialized) await this.init();
    
    try {
      // Find which file contains the event
      const filesToCheck = this._getFilesInDateRange(null, new Date());
      
      for (const filename of filesToCheck) {
        const filepath = path.join(this.dataDir, filename);
        let events = await this._readEventsFromFile(filename);
        
        const eventIndex = events.findIndex(e => e.id === eventId);
        if (eventIndex !== -1) {
          // Found the event, update it
          events[eventIndex] = {
            ...events[eventIndex],
            ...updates,
            updatedAt: new Date().toISOString()
          };
          
          // Write back to file
          await this._writeEventsToFile(filename, events);
          return true;
        }
      }
      
      return false; // Event not found
    } catch (error) {
      throw new Error(`Failed to update event: ${error.message}`);
    }
  }

  async deleteEvents(filter = {}) {
    if (!this.initialized) await this.init();
    
    try {
      let deletedCount = 0;
      
      const {
        startDate, endDate, eventTypes, agentIds
      } = { 
        startDate: null, endDate: null, eventTypes: [], agentIds: [] 
      , ...filter };

      const filesToCheck = this._getFilesInDateRange(startDate, endDate);
      
      for (const filename of filesToCheck) {
        const filepath = path.join(this.dataDir, filename);
        let events = await this._readEventsFromFile(filename);
        
        const initialLength = events.length;
        
        // Apply filters in reverse (so we can safely splice)
        events = events.filter(event => {
          let shouldDelete = true;
          
          if (startDate && new Date(event.timestamp) < new Date(startDate)) {
            shouldDelete = false;
          }
          
          if (endDate && new Date(event.timestamp) > new Date(endDate)) {
            shouldDelete = false;
          }
          
          if (eventTypes.length > 0 && !eventTypes.includes(event.type)) {
            shouldDelete = false;
          }
          
          if (agentIds.length > 0 && !agentIds.includes(event.agentId)) {
            shouldDelete = false;
          }
          
          return !shouldDelete;
        });
        
        const deletedFromFile = initialLength - events.length;
        deletedCount += deletedFromFile;
        
        // Write back the filtered events
        await this._writeEventsToFile(filename, events);
      }
      
      return deletedCount;
    } catch (error) {
      throw new Error(`Failed to delete events: ${error.message}`);
    }
  }

  async cleanupOld() {
    if (!this.initialized) await this.init();
    
    try {
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - this.maxAgeDays);
      
      // Read all files in the data directory
      const files = await fs.readdir(this.dataDir);
      const jsonFiles = files.filter(file => 
        file.startsWith(this.filePrefix) && file.endsWith('.json')
      );
      
      let deletedCount = 0;
      
      for (const filename of jsonFiles) {
        // Extract date from filename
        const dateStr = filename.substring(this.filePrefix.length, filename.length - 5); // Remove .json
        const [year, month, day] = dateStr.split('-').map(Number);
        const fileDate = new Date(year, month - 1, day);
        
        // If file is older than cutoff, delete it
        if (fileDate < cutoffDate) {
          await fs.unlink(path.join(this.dataDir, filename));
          deletedCount++;
        }
      }
      
      return deletedCount;
    } catch (error) {
      throw new Error(`Failed to cleanup old files: ${error.message}`);
    }
  }

  async getStats() {
    if (!this.initialized) await this.init();
    
    try {
      const files = await fs.readdir(this.dataDir);
      const jsonFiles = files.filter(file => 
        file.startsWith(this.filePrefix) && file.endsWith('.json')
      );
      
      let totalEvents = 0;
      let totalSize = 0;
      
      for (const filename of jsonFiles) {
        const filepath = path.join(this.dataDir, filename);
        const stats = await fs.stat(filepath);
        totalSize += stats.size;
        
        // Count events in file (efficiently for large files would require streaming)
        try {
          const data = await fs.readFile(filepath, 'utf8');
          const events = JSON.parse(data);
          totalEvents += Array.isArray(events) ? events.length : 0;
        } catch (e) {
          // If we can't parse JSON, skip counting events for this file
        }
      }
      
      return {
        backend: 'json-file',
        dataDir: this.dataDir,
        fileCount: jsonFiles.length,
        totalEvents: totalEvents,
        totalSizeBytes: totalSize,
        maxAgeDays: this.maxAgeDays,
        oldestFile: null, // Would need to scan to find actual oldest
        newestFile: null  // Would need to scan to find actual newest
      };
    } catch (error) {
      throw new Error(`Failed to get stats: ${error.message}`);
    }
  }

  async close() {
    // JSON file storage doesn't keep open connections
    this.initialized = false;
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

module.exports = { JsonFileStorage };