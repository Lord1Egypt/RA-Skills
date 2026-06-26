/**
 * Storage Adapter Interface
 * Defines the contract for all storage backends in LobsterOps
 * 
 * This interface ensures storage pluggability - you can swap between
 * Supabase, SQLite, JSON files, memory, etc. without changing core logic
 */
class StorageAdapter {
  /**
   * Initialize the storage backend
   * @returns {Promise<void>}
   */
  async init() {
    throw new Error('StorageAdapter.init() must be implemented by subclass');
  }

  /**
   * Save a single agent event
   * @param {Object} event - The agent event to store
   * @returns {Promise<string>} - Returns the event ID
   */
  async saveEvent(event) {
    throw new Error('StorageAdapter.saveEvent() must be implemented by subclass');
  }

  /**
   * Query events with filtering options
   * @param {Object} filter - Filter criteria (time range, event types, etc.)
   * @param {Object} options - Pagination and sorting options
   * @returns {Promise<Array<Object>>} - Array of matching events
   */
  async queryEvents(filter = {}, options = {}) {
    throw new Error('StorageAdapter.queryEvents() must be implemented by subclass');
  }

  /**
   * Retrieve a specific event by ID
   * @param {string} eventId - The ID of the event to retrieve
   * @returns {Promise<Object|null>} - The event or null if not found
   */
  async getEventById(eventId) {
    throw new Error('StorageAdapter.getEventById() must be implemented by subclass');
  }

  /**
   * Update an existing event
   * @param {string} eventId - The ID of the event to update
   * @param {Object} updates - The fields to update
   * @returns {Promise<boolean>} - True if successful
   */
  async updateEvent(eventId, updates) {
    throw new Error('StorageAdapter.updateEvent() must be implemented by subclass');
  }

  /**
   * Delete events matching criteria
   * @param {Object} filter - Filter criteria for deletion
   * @returns {Promise<number>} - Number of events deleted
   */
  async deleteEvents(filter) {
    throw new Error('StorageAdapter.deleteEvents() must be implemented by subclass');
  }

  /**
   * Clean up old events based on retention policy
   * @returns {Promise<number>} - Number of events removed
   */
  async cleanupOld() {
    throw new Error('StorageAdapter.cleanupOld() must be implemented by subclass');
  }

  /**
   * Get storage statistics
   * @returns {Promise<Object>} - Storage usage statistics
   */
  async getStats() {
    throw new Error('StorageAdapter.getStats() must be implemented by subclass');
  }

  /**
   * Close storage connections and cleanup
   * @returns {Promise<void>}
   */
  async close() {
    throw new Error('StorageAdapter.close() must be implemented by subclass');
  }
}

module.exports = { StorageAdapter };