const { StorageFactory } = require('../storage/StorageFactory');
const { v4: uuidv4 } = require('uuid');
const { PIIFilter } = require('./PIIFilter');
const { Exporter } = require('./Exporter');
const { DebugConsole } = require('./DebugConsole');
const { Analytics } = require('./Analytics');
const { AlertManager } = require('./AlertManager');

/**
 * LobsterOps - AI Agent Observability & Debug Console
 * 
 * Main class for recording, querying, and analyzing AI agent events.
 * Designed to be flexible, dependency-free, and easy to integrate.
 * 
 * Features:
 * - Pluggable storage backends (JSON files, memory, SQLite, Supabase)
 * - Structured event logging with automatic enrichment
 * - AI-agent specific logging helpers (thoughts, tool calls, decisions, etc.)
 * - Powerful querying capabilities
 * - OpenClaw integration ready
 * - Zero configuration required to get started
 */
class LobsterOps {
  /**
   * @param {Object} options - Configuration options
   * @param {string} options.storageType - Storage backend type ('json', 'memory', 'sqlite', 'supabase')
   * @param {Object} options.storageConfig - Configuration for the storage backend
   * @param {boolean} options.enabled - Whether LobsterOps is enabled (default: true)
   * @param {string} options.instanceId - Unique identifier for this LobsterOps instance
   * @param {Object} options.piiFiltering - PII filtering configuration
   * @param {Object} options.alerts - Alert configuration
   */
  constructor(options = {}) {
    this.enabled = options.enabled !== false; // Default to true
    this.instanceId = options.instanceId || this._generateInstanceId();
    this.storageType = options.storageType || 'json'; // Default to JSON file storage
    this.storageConfig = options.storageConfig || {};

    // Add instance ID to storage config for backends that might need it
    this.storageConfig.instanceId = this.instanceId;

    this.storage = null;
    this.initialized = false;

    // PII filtering
    this.piiFilter = new PIIFilter(options.piiFiltering || {});

    // Alert manager
    this.alertManager = new AlertManager();

    // Bind methods for easier use
    this.logEvent = this.logEvent.bind(this);
    this.logThought = this.logThought.bind(this);
    this.logToolCall = this.logToolCall.bind(this);
    this.logDecision = this.logDecision.bind(this);
    this.logError = this.logError.bind(this);
    this.logSpawning = this.logSpawning.bind(this);
    this.queryEvents = this.queryEvents.bind(this);
    this.getEvent = this.getEvent.bind(this);
    this.getAgentTrace = this.getAgentTrace.bind(this);
    this.getRecentActivity = this.getRecentActivity.bind(this);
  }

  /**
   * Initialize LobsterOps and the storage backend
   * @returns {Promise<void>}
   */
  async init() {
    if (!this.enabled) {
      this.initialized = true;
      return;
    }
    
    try {
      // Create the storage backend using the factory
      this.storage = StorageFactory.createStorage(this.storageType, this.storageConfig);
      
      // Initialize the storage backend
      await this.storage.init();
      
      this.initialized = true;
    } catch (error) {
      throw new Error(`Failed to initialize LobsterOps: ${error.message}`);
    }
  }

  /**
   * Log a general agent event
   * @param {Object} event - The agent event to log
   * @param {Object} options - Additional options
   * @returns {Promise<string>} - The ID of the logged event
   */
  async logEvent(event, options = {}) {
    if (!this.enabled) {
      return null; // Silently ignore if disabled
    }
    
    if (!this.initialized) {
      await this.init();
    }
    
    try {
      // Apply PII filtering
      const filteredEvent = this.piiFilter.filter(event);

      // Enrich the event with metadata
      const enrichedEvent = {
        ...filteredEvent,
        id: event.id || uuidv4(),
        timestamp: event.timestamp || new Date().toISOString(),
        lobsterOpsInstanceId: this.instanceId,
        loggedAt: new Date().toISOString(),
        ...options
      };

      // Evaluate alert rules
      this.alertManager.evaluate(enrichedEvent);

      // Save to storage
      const eventId = await this.storage.saveEvent(enrichedEvent);
      return eventId;
    } catch (error) {
      throw new Error(`Failed to log event: ${error.message}`);
    }
  }

  /**
   * Log an agent thought/reasoning step
   * @param {Object} thought - The thought content and metadata
   * @param {Object} options - Additional options
   * @returns {Promise<string>} - The ID of the logged thought
   */
  async logThought(thought, options = {}) {
    return this.logEvent({
      type: 'agent-thought',
      ...thought
    }, {
      category: 'reasoning',
      ...options
    });
  }

  /**
   * Log a tool call execution
   * @param {Object} toolCall - Tool call details
   * @param {Object} options - Additional options
   * @returns {Promise<string>} - The ID of the logged tool call
   */
  async logToolCall(toolCall, options = {}) {
    return this.logEvent({
      type: 'tool-call',
      ...toolCall
    }, {
      category: 'action',
      ...options
    });
  }

  /**
   * Log an agent decision
   * @param {Object} decision - Decision details
   * @param {Object} options - Additional options
   * @returns {Promise<string>} - The ID of the logged decision
   */
  async logDecision(decision, options = {}) {
    return this.logEvent({
      type: 'agent-decision',
      ...decision
    }, {
      category: 'decision',
      ...options
    });
  }

  /**
   * Log an agent error
   * @param {Object} error - Error details
   * @param {Object} options - Additional options
   * @returns {Promise<string>} - The ID of the logged error
   */
  async logError(error, options = {}) {
    return this.logEvent({
      type: 'agent-error',
      ...error
    }, {
      category: 'error',
      severity: options.severity || 'medium',
      ...options
    });
  }

  /**
   * Log agent spawning/subagent creation
   * @param {Object} spawnInfo - Spawning details
   * @param {Object} options - Additional options
   * @returns {Promise<string>} - The ID of the logged spawn event
   */
  async logSpawning(spawnInfo, options = {}) {
    return this.logEvent({
      type: 'agent-spawn',
      ...spawnInfo
    }, {
      category: 'lifecycle',
      ...options
    });
  }

  /**
   * Log agent lifecycle event (startup, shutdown, etc.)
   * @param {Object} lifecycleInfo - Lifecycle event details
   * @param {Object} options - Additional options
   * @returns {Promise<string>} - The ID of the logged lifecycle event
   */
  async logLifecycle(lifecycleInfo, options = {}) {
    return this.logEvent({
      type: 'agent-lifecycle',
      ...lifecycleInfo
    }, {
      category: 'lifecycle',
      ...options
    });
  }

  /**
   * Query events with filtering options
   * @param {Object} filter - Filter criteria
   * @param {Object} options - Query options (limit, offset, sort, etc.)
   * @returns {Promise<Array>} - Matching events
   */
  async queryEvents(filter = {}, options = {}) {
    if (!this.enabled) {
      return [];
    }
    
    if (!this.initialized) {
      await this.init();
    }
    
    try {
      return await this.storage.queryEvents(filter, options);
    } catch (error) {
      throw new Error(`Failed to query events: ${error.message}`);
    }
  }

  /**
   * Get a specific event by ID
   * @param {string} eventId - The ID of the event to retrieve
   * @returns {Promise<Object|null>} - The event or null if not found
   */
  async getEvent(eventId) {
    if (!this.enabled) {
      return null;
    }
    
    if (!this.initialized) {
      await this.init();
    }
    
    try {
      return await this.storage.getEventById(eventId);
    } catch (error) {
      throw new Error(`Failed to get event: ${error.message}`);
    }
  }

  /**
   * Update an existing event
   * @param {string} eventId - The ID of the event to update
   * @param {Object} updates - The fields to update
   * @returns {Promise<boolean>} - True if successful
   */
  async updateEvent(eventId, updates) {
    if (!this.enabled) {
      return false;
    }
    
    if (!this.initialized) {
      await this.init();
    }
    
    try {
      return await this.storage.updateEvent(eventId, updates);
    } catch (error) {
      throw new Error(`Failed to update event: ${error.message}`);
    }
  }

  /**
   * Delete events matching criteria
   * @param {Object} filter - Filter criteria for deletion
   * @returns {Promise<number>} - Number of events deleted
   */
  async deleteEvents(filter = {}) {
    if (!this.enabled) {
      return 0;
    }
    
    if (!this.initialized) {
      await this.init();
    }
    
    try {
      return await this.storage.deleteEvents(filter);
    } catch (error) {
      throw new Error(`Failed to delete events: ${error.message}`);
    }
  }

  /**
   * Clean up old events based on retention policy
   * @returns {Promise<number>} - Number of events removed
   */
  async cleanupOld() {
    if (!this.enabled) {
      return 0;
    }
    
    if (!this.initialized) {
      await this.init();
    }
    
    try {
      return await this.storage.cleanupOld();
    } catch (error) {
      throw new Error(`Failed to cleanup old events: ${error.message}`);
    }
  }

  /**
   * Get a complete trace of an agent's activity
   * @param {string} agentId - The ID of the agent to trace
   * @param {Object} options - Trace options (time range, limit, etc.)
   * @returns {Promise<Array>} - Chronological trace of agent activity
   */
  async getAgentTrace(agentId, options = {}) {
    if (!this.enabled) {
      return [];
    }
    
    if (!this.initialized) {
      await this.init();
    }
    
    try {
      const traceOptions = {
        agentIds: [agentId],
        limit: options.limit || 1000,
        offset: options.offset || 0,
        sortBy: 'timestamp',
        sortOrder: options.sortOrder || 'asc', // Chronological by default for traces
        ...options
      };
      
      // Remove agentIds from options since we handle it separately
      delete traceOptions.agentIds;
      
      return await this.queryEvents(
        { agentId },
        traceOptions
      );
    } catch (error) {
      throw new Error(`Failed to get agent trace: ${error.message}`);
    }
  }

  /**
   * Get recent activity across all agents or for a specific agent
   * @param {Object} options - Activity options
   * @returns {Promise<Array>} - Recent events
   */
  async getRecentActivity(options = {}) {
    if (!this.enabled) {
      return [];
    }
    
    if (!this.initialized) {
      await this.init();
    }
    
    try {
      const activityOptions = {
        limit: options.limit || 50,
        offset: options.offset || 0,
        sortBy: 'timestamp',
        sortOrder: 'desc', // Most recent first
        ...options
      };
      
      return await this.queryEvents({}, activityOptions);
    } catch (error) {
      throw new Error(`Failed to get recent activity: ${error.message}`);
    }
  }

  /**
   * Get storage and usage statistics
   * @returns {Promise<Object>} - Statistics about storage usage
   */
  async getStats() {
    if (!this.enabled) {
      return { enabled: false };
    }
    
    if (!this.initialized) {
      await this.init();
    }
    
    try {
      const stats = await this.storage.getStats();
      return {
        enabled: true,
        instanceId: this.instanceId,
        storageType: this.storageType,
        ...stats
      };
    } catch (error) {
      throw new Error(`Failed to get stats: ${error.message}`);
    }
  }

  /**
   * Close LobsterOps and release resources
   * @returns {Promise<void>}
   */
  async close() {
    if (!this.initialized) {
      return;
    }
    
    try {
      if (this.storage) {
        await this.storage.close();
      }
      this.initialized = false;
    } catch (error) {
      throw new Error(`Failed to close LobsterOps: ${error.message}`);
    }
  }

  /**
   * Export events to a specific format
   * @param {string} format - Export format: 'json', 'csv', or 'markdown'
   * @param {Object} filter - Filter criteria for events to export
   * @param {Object} options - Export and query options
   * @returns {Promise<string>} - Exported data as string
   */
  async exportEvents(format = 'json', filter = {}, options = {}) {
    const events = await this.queryEvents(filter, { limit: options.limit || 10000, ...options });

    switch (format.toLowerCase()) {
      case 'csv':
        return Exporter.toCSV(events, options);
      case 'markdown':
      case 'md':
        return Exporter.toMarkdown(events, options);
      case 'json':
      default:
        return Exporter.toJSON(events, options);
    }
  }

  /**
   * Create a debug console for stepping through an agent's event trace
   * @param {string} agentId - Agent ID to debug
   * @param {Object} options - Query options
   * @returns {Promise<DebugConsole>} - Interactive debug console
   */
  async createDebugConsole(agentId, options = {}) {
    const events = await this.getAgentTrace(agentId, options);
    return new DebugConsole(events);
  }

  /**
   * Run behavioral analytics on events
   * @param {Object} filter - Filter criteria
   * @param {Object} options - Query options
   * @returns {Promise<Object>} - Analytics report
   */
  async analyze(filter = {}, options = {}) {
    const events = await this.queryEvents(filter, { limit: options.limit || 10000, ...options });
    return Analytics.analyze(events);
  }

  /**
   * Check if LobsterOps is initialized and ready
   * @returns {boolean} - True if ready to use
   */
  isReady() {
    return this.enabled && this.initialized && this.storage !== null;
  }

  /**
   * Generate a unique instance ID
   * @returns {string} - Unique instance ID
   */
  _generateInstanceId() {
    return `lobsterops-${Math.random().toString(36).substr(2, 9)}-${Date.now().toString(36)}`;
  }
}

module.exports = { LobsterOps };