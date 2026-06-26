const { StorageAdapter } = require('./StorageAdapter');

/**
 * In-Memory Storage Backend
 * Useful for testing, temporary sessions, or when persistence isn't needed
 * All data is lost when the process exits
 */
class MemoryStorage extends StorageAdapter {
  /**
   * @param {Object} config - Configuration options
   * @param {number} config.maxEvents - Maximum events to keep in memory (default: 10000)
   */
  constructor(config = {}) {
    super();
    this.events = new Map(); // eventId -> event
    this.maxEvents = config.maxEvents || 10000;
    this.initialized = false;
  }

  async init() {
    this.initialized = true;
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

      this.events.set(enrichedEvent.id, enrichedEvent);
      
      // Enforce max events limit (remove oldest first)
      if (this.events.size > this.maxEvents) {
        // Get oldest events by timestamp
        const sortedEvents = Array.from(this.events.values()).sort(
          (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
        );
        
        // Remove excess events
        const eventsToRemove = sortedEvents.slice(0, this.events.size - this.maxEvents);
        for (const event of eventsToRemove) {
          this.events.delete(event.id);
        }
      }
      
      return enrichedEvent.id;
    } catch (error) {
      throw new Error(`Failed to save event: ${error.message}`);
    }
  }

  async queryEvents(filter = {}, options = {}) {
    if (!this.initialized) await this.init();
    
    try {
      const {
        startDate, endDate, eventTypes, agentIds, limit = 100, offset = 0, 
        sortBy = 'timestamp', sortOrder = 'desc'
      } = { 
        startDate: null, endDate: null, eventTypes: [], agentIds: [], 
        limit: 100, offset: 0, sortBy: 'timestamp', sortOrder: 'desc' 
      , ...filter, ...options };

      // Convert Map values to array and apply filters
      let filteredEvents = Array.from(this.events.values());
      
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

  async getEventById(eventId) {
    if (!this.initialized) await this.init();
    
    try {
      return this.events.get(eventId) || null;
    } catch (error) {
      throw new Error(`Failed to get event by ID: ${error.message}`);
    }
  }

  async updateEvent(eventId, updates) {
    if (!this.initialized) await this.init();
    
    try {
      const event = this.events.get(eventId);
      if (!event) {
        return false; // Event not found
      }
      
      const updatedEvent = {
        ...event,
        ...updates,
        updatedAt: new Date().toISOString()
      };
      
      this.events.set(eventId, updatedEvent);
      return true;
    } catch (error) {
      throw new Error(`Failed to update event: ${error.message}`);
    }
  }

  async deleteEvents(filter = {}) {
    if (!this.initialized) await this.init();
    
    try {
      const {
        startDate, endDate, eventTypes, agentIds
      } = { 
        startDate: null, endDate: null, eventTypes: [], agentIds: [] 
      , ...filter };

      let deletedCount = 0;
      const eventsToDelete = [];
      
      for (const [eventId, event] of this.events.entries()) {
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
        
        if (shouldDelete) {
          eventsToDelete.push(eventId);
        }
      }
      
      // Delete the marked events
      for (const eventId of eventsToDelete) {
        this.events.delete(eventId);
        deletedCount++;
      }
      
      return deletedCount;
    } catch (error) {
      throw new Error(`Failed to delete events: ${error.message}`);
    }
  }

  async cleanupOld() {
    if (!this.initialized) await this.init();
    
    try {
      // For memory storage, cleanup old means applying our maxEvents limit
      // or we could add a maxAge option
      const initialSize = this.events.size;
      
      if (this.events.size > this.maxEvents) {
        // Remove oldest events
        const sortedEvents = Array.from(this.events.values()).sort(
          (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
        );
        
        const eventsToRemove = sortedEvents.slice(0, this.events.size - this.maxEvents);
        for (const event of eventsToRemove) {
          this.events.delete(event.id);
        }
      }
      
      return initialSize - this.events.size;
    } catch (error) {
      throw new Error(`Failed to cleanup old events: ${error.message}`);
    }
  }

  async getStats() {
    if (!this.initialized) await this.init();
    
    try {
      const events = Array.from(this.events.values());
      const timestamps = events.map(e => new Date(e.timestamp));
      const oldest = timestamps.length > 0 ? new Date(Math.min(...timestamps.map(t => t.getTime()))) : null;
      const newest = timestamps.length > 0 ? new Date(Math.max(...timestamps.map(t => t.getTime()))) : null;
      
      return {
        backend: 'memory',
        eventCount: this.events.size,
        oldestEvent: oldest ? oldest.toISOString() : null,
        newestEvent: newest ? newest.toISOString() : null,
        maxEvents: this.maxEvents
      };
    } catch (error) {
      throw new Error(`Failed to get stats: ${error.message}`);
    }
  }

  async close() {
    this.events.clear();
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

module.exports = { MemoryStorage };