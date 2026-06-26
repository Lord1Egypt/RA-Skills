/**
 * Session Auto-Scaling Manager
 * 
 * Features:
 * 1. Monitor session load (message count, request rate, active time)
 * 2. Auto-create new sessions when load is high
 * 3. Auto-merge sessions when load is low
 * 4. Load balancing across sessions
 * 5. Configurable thresholds and policies
 */

const fs = require('fs');
const path = require('path');
const { getSessionManager, SessionState } = require('../session-persistence/session-manager');

// Configuration
const STATE_FILE = path.join(__dirname, '..', 'memory', 'autoscaler-state.json');
const CONFIG_FILE = path.join(__dirname, 'autoscaler-config.json');

// Default configuration
const DEFAULT_CONFIG = {
  // Load thresholds
  load: {
    // High load triggers: create new session
    highMessageCount: 100,           // Messages per session
    highRequestRate: 10,             // Requests per minute
    highCpuUsage: 80,                // CPU usage percentage (if available)
    highMemoryUsage: 80,             // Memory usage percentage (if available)
    
    // Low load triggers: merge sessions
    lowMessageCount: 20,             // Messages per session
    lowRequestRate: 2,               // Requests per minute
    lowActiveTime: 30,               // Minutes of low activity before merge
    
    // Load calculation weights
    weights: {
      messageCount: 0.4,
      requestRate: 0.4,
      cpuUsage: 0.1,
      memoryUsage: 0.1
    }
  },
  
  // Scaling policies
  scaling: {
    minSessions: 1,                  // Minimum number of sessions
    maxSessions: 10,                 // Maximum number of sessions
    scaleUpThreshold: 0.8,           // Load score to trigger scale up (0-1)
    scaleDownThreshold: 0.3,         // Load score to trigger scale down (0-1)
    cooldownMinutes: 5,              // Minutes between scaling operations
    mergeMinSessions: 2,             // Minimum sessions required to merge
    loadBalancingEnabled: true       // Enable automatic load balancing
  },
  
  // Monitoring
  monitoring: {
    checkIntervalSeconds: 30,        // How often to check load
    metricsRetentionHours: 24,       // How long to keep metrics history
    enableLoadBalancing: true,       // Auto-balance load across sessions
    balanceThreshold: 0.3            // Load difference threshold to trigger balancing
  },
  
  // Session naming
  naming: {
    prefix: 'session',               // Session ID prefix
    includeTimestamp: true           // Include timestamp in session ID
  }
};

/**
 * Session metrics tracker
 */
class SessionMetrics {
  constructor(sessionId) {
    this.sessionId = sessionId;
    this.messageCount = 0;
    this.requestCount = 0;
    this.lastRequestTime = Date.now();
    this.requestHistory = [];        // Last N request timestamps
    this.cpuUsage = 0;
    this.memoryUsage = 0;
    this.createdAt = Date.now();
    this.lastActivityAt = Date.now();
  }
  
  /**
   * Record a message
   */
  recordMessage() {
    this.messageCount++;
    this.lastActivityAt = Date.now();
  }
  
  /**
   * Record a request
   */
  recordRequest() {
    const now = Date.now();
    this.requestCount++;
    this.lastRequestTime = now;
    
    // Keep last 5 minutes of requests
    this.requestHistory.push(now);
    const fiveMinutesAgo = now - 5 * 60 * 1000;
    this.requestHistory = this.requestHistory.filter(t => t > fiveMinutesAgo);
  }
  
  /**
   * Get request rate (requests per minute)
   */
  getRequestRate() {
    const now = Date.now();
    const fiveMinutesAgo = now - 5 * 60 * 1000;
    const recentRequests = this.requestHistory.filter(t => t > fiveMinutesAgo);
    
    if (recentRequests.length < 2) {
      return 0;
    }
    
    // Calculate rate based on time span
    const timeSpanMinutes = (now - recentRequests[0]) / 60000;
    if (timeSpanMinutes < 0.1) {
      return recentRequests.length;
    }
    
    return recentRequests.length / timeSpanMinutes;
  }
  
  /**
   * Calculate load score (0-1)
   */
  calculateLoadScore(config) {
    const weights = config.load.weights;
    const load = config.load;
    
    // Normalize each metric to 0-1
    const messageScore = Math.min(1, this.messageCount / load.highMessageCount);
    const requestRateScore = Math.min(1, this.getRequestRate() / load.highRequestRate);
    const cpuScore = this.cpuUsage / 100;
    const memoryScore = this.memoryUsage / 100;
    
    // Weighted average
    const score = 
      messageScore * weights.messageCount +
      requestRateScore * weights.requestRate +
      cpuScore * weights.cpuUsage +
      memoryScore * weights.memoryUsage;
    
    return Math.min(1, Math.max(0, score));
  }
  
  toJSON(config) {
    const cfg = config || DEFAULT_CONFIG;
    return {
      sessionId: this.sessionId,
      messageCount: this.messageCount,
      requestCount: this.requestCount,
      requestRate: this.getRequestRate(),
      cpuUsage: this.cpuUsage,
      memoryUsage: this.memoryUsage,
      createdAt: this.createdAt,
      lastActivityAt: this.lastActivityAt,
      loadScore: this.calculateLoadScore(cfg)
    };
  }
}

/**
 * Auto-Scaling Manager
 */
class SessionAutoScaler {
  constructor() {
    this.sessionManager = null;
    this.metrics = new Map();        // sessionId -> SessionMetrics
    this.config = null;
    this.state = {
      lastScaleUp: null,
      lastScaleDown: null,
      lastBalance: null,
      totalScaleUps: 0,
      totalScaleDowns: 0,
      totalMerges: 0,
      history: []
    };
    this.initialized = false;
    this.checkInterval = null;
  }
  
  /**
   * Initialize the auto-scaler
   */
  async initialize() {
    try {
      // Load configuration
      this.config = this._loadConfig();
      
      // Get session manager
      this.sessionManager = getSessionManager();
      
      // Load state
      this._loadState();
      
      // Initialize metrics for existing sessions
      await this._initializeMetrics();
      
      this.initialized = true;
      console.log('[AutoScaler] Initialized with config:', JSON.stringify(this.config, null, 2));
      
      // Start monitoring
      this._startMonitoring();
      
      return true;
    } catch (error) {
      console.error('[AutoScaler] Initialization failed:', error);
      return false;
    }
  }
  
  /**
   * Load configuration
   */
  _loadConfig() {
    try {
      if (fs.existsSync(CONFIG_FILE)) {
        const userConfig = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
        return this._mergeConfig(DEFAULT_CONFIG, userConfig);
      }
    } catch (error) {
      console.error('[AutoScaler] Failed to load config:', error);
    }
    
    return DEFAULT_CONFIG;
  }
  
  /**
   * Merge configurations
   */
  _mergeConfig(defaultConfig, userConfig) {
    const result = { ...defaultConfig };
    
    for (const key in userConfig) {
      if (userConfig[key] !== null && typeof userConfig[key] === 'object' && !Array.isArray(userConfig[key])) {
        result[key] = this._mergeConfig(result[key], userConfig[key]);
      } else {
        result[key] = userConfig[key];
      }
    }
    
    return result;
  }
  
  /**
   * Load state from disk
   */
  _loadState() {
    try {
      if (fs.existsSync(STATE_FILE)) {
        const state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
        this.state = { ...this.state, ...state };
        console.log('[AutoScaler] Loaded state from disk');
      }
    } catch (error) {
      console.error('[AutoScaler] Failed to load state:', error);
    }
  }
  
  /**
   * Save state to disk
   */
  _saveState() {
    try {
      const dir = path.dirname(STATE_FILE);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.writeFileSync(STATE_FILE, JSON.stringify(this.state, null, 2), 'utf8');
    } catch (error) {
      console.error('[AutoScaler] Failed to save state:', error);
    }
  }
  
  /**
   * Initialize metrics for existing sessions
   */
  async _initializeMetrics() {
    if (!this.sessionManager || !this.sessionManager.initialized) {
      return;
    }
    
    const sessions = this.sessionManager.getActiveSessions();
    for (const session of sessions) {
      if (!this.metrics.has(session.id)) {
        const metrics = new SessionMetrics(session.id);
        metrics.messageCount = session.messageCount || 0;
        this.metrics.set(session.id, metrics);
      }
    }
    
    console.log('[AutoScaler] Initialized metrics for', this.metrics.size, 'sessions');
  }
  
  /**
   * Start periodic monitoring
   */
  _startMonitoring() {
    const interval = this.config.monitoring.checkIntervalSeconds * 1000;
    
    this.checkInterval = setInterval(async () => {
      await this._checkAndScale();
    }, interval);
    
    console.log('[AutoScaler] Monitoring started (interval:', interval / 1000, 'seconds)');
  }
  
  /**
   * Stop monitoring
   */
  stop() {
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
      this.checkInterval = null;
      console.log('[AutoScaler] Monitoring stopped');
    }
  }
  
  /**
   * Record a message for a session
   */
  recordMessage(sessionId) {
    if (!this.metrics.has(sessionId)) {
      this.metrics.set(sessionId, new SessionMetrics(sessionId));
    }
    
    const metrics = this.metrics.get(sessionId);
    metrics.recordMessage();
  }
  
  /**
   * Record a request for a session
   */
  recordRequest(sessionId) {
    if (!this.metrics.has(sessionId)) {
      this.metrics.set(sessionId, new SessionMetrics(sessionId));
    }
    
    const metrics = this.metrics.get(sessionId);
    metrics.recordRequest();
  }
  
  /**
   * Update CPU/memory usage for a session
   */
  updateResourceUsage(sessionId, cpuUsage, memoryUsage) {
    if (!this.metrics.has(sessionId)) {
      this.metrics.set(sessionId, new SessionMetrics(sessionId));
    }
    
    const metrics = this.metrics.get(sessionId);
    metrics.cpuUsage = cpuUsage;
    metrics.memoryUsage = memoryUsage;
  }
  
  /**
   * Check load and perform scaling operations
   */
  async _checkAndScale() {
    try {
      // Refresh session list
      await this._initializeMetrics();
      
      // Check if we need to scale up
      await this._checkScaleUp();
      
      // Check if we need to scale down
      await this._checkScaleDown();
      
      // Check if we need to balance load
      if (this.config.scaling.loadBalancingEnabled) {
        await this._checkLoadBalance();
      }
      
      // Save state
      this._saveState();
      
      // Record history
      this._recordHistory();
    } catch (error) {
      console.error('[AutoScaler] Check failed:', error);
    }
  }
  
  /**
   * Check if scale up is needed
   */
  async _checkScaleUp() {
    const now = Date.now();
    const cooldown = this.config.scaling.cooldownMinutes * 60 * 1000;
    
    // Check cooldown
    if (this.state.lastScaleUp && (now - this.state.lastScaleUp) < cooldown) {
      return;
    }
    
    // Check session count limit
    const activeSessions = this.sessionManager.getActiveSessions();
    if (activeSessions.length >= this.config.scaling.maxSessions) {
      return;
    }
    
    // Check if any session is overloaded
    for (const [sessionId, metrics] of this.metrics) {
      const loadScore = metrics.calculateLoadScore(this.config);
      
      if (loadScore >= this.config.scaling.scaleUpThreshold) {
        console.log('[AutoScaler] High load detected on', sessionId, '(score:', loadScore, ')');
        await this._createNewSession();
        this.state.lastScaleUp = now;
        this.state.totalScaleUps++;
        return;
      }
    }
  }
  
  /**
   * Check if scale down is needed
   */
  async _checkScaleDown() {
    const now = Date.now();
    const cooldown = this.config.scaling.cooldownMinutes * 60 * 1000;
    
    // Check cooldown
    if (this.state.lastScaleDown && (now - this.state.lastScaleDown) < cooldown) {
      return;
    }
    
    // Check session count limit
    const activeSessions = this.sessionManager.getActiveSessions();
    if (activeSessions.length <= this.config.scaling.minSessions) {
      return;
    }
    
    // Find underloaded sessions
    const underloadedSessions = [];
    for (const [sessionId, metrics] of this.metrics) {
      const loadScore = metrics.calculateLoadScore(this.config);
      
      if (loadScore < this.config.scaling.scaleDownThreshold) {
        underloadedSessions.push({ sessionId, loadScore });
      }
    }
    
    // Merge underloaded sessions if we have enough
    if (underloadedSessions.length >= this.config.scaling.mergeMinSessions) {
      console.log('[AutoScaler] Low load detected, merging', underloadedSessions.length, 'sessions');
      await this._mergeSessions(underloadedSessions.map(s => s.sessionId));
      this.state.lastScaleDown = now;
      this.state.totalScaleDowns++;
    }
  }
  
  /**
   * Check if load balancing is needed
   */
  async _checkLoadBalance() {
    const now = Date.now();
    const cooldown = this.config.scaling.cooldownMinutes * 60 * 1000;
    
    // Check cooldown
    if (this.state.lastBalance && (now - this.state.lastBalance) < cooldown) {
      return;
    }
    
    // Calculate load distribution
    const loadScores = [];
    for (const [sessionId, metrics] of this.metrics) {
      loadScores.push({
        sessionId,
        loadScore: metrics.calculateLoadScore(this.config)
      });
    }
    
    if (loadScores.length < 2) {
      return;
    }
    
    // Check load imbalance
    const maxLoad = Math.max(...loadScores.map(s => s.loadScore));
    const minLoad = Math.min(...loadScores.map(s => s.loadScore));
    
    if ((maxLoad - minLoad) > this.config.monitoring.balanceThreshold) {
      console.log('[AutoScaler] Load imbalance detected (max:', maxLoad, 'min:', minLoad, ')');
      await this._balanceLoad(loadScores);
      this.state.lastBalance = now;
    }
  }
  
  /**
   * Create a new session
   */
  async _createNewSession() {
    try {
      // Generate session ID
      const timestamp = this.config.naming.includeTimestamp ? '-' + Date.now() : '';
      const sessionId = this.config.naming.prefix + timestamp;
      
      // Create session
      const session = await this.sessionManager.createSession(sessionId);
      
      // Initialize metrics
      this.metrics.set(sessionId, new SessionMetrics(sessionId));
      
      console.log('[AutoScaler] Created new session:', sessionId);
      
      // Record in history
      this._addToHistory('scale_up', { sessionId, reason: 'high_load' });
      
      return session;
    } catch (error) {
      console.error('[AutoScaler] Failed to create session:', error);
      throw error;
    }
  }
  
  /**
   * Merge multiple sessions into one
   */
  async _mergeSessions(sessionIds) {
    try {
      if (sessionIds.length < 2) {
        return;
      }
      
      // Keep the first session, merge others into it
      const targetSessionId = sessionIds[0];
      const sessionsToMerge = sessionIds.slice(1);
      
      console.log('[AutoScaler] Merging sessions:', sessionsToMerge, 'into', targetSessionId);
      
      // For each session to merge:
      for (const sessionId of sessionsToMerge) {
        // Transfer metrics
        const sourceMetrics = this.metrics.get(sessionId);
        const targetMetrics = this.metrics.get(targetSessionId);
        
        if (sourceMetrics && targetMetrics) {
          targetMetrics.messageCount += sourceMetrics.messageCount;
          targetMetrics.requestCount += sourceMetrics.requestCount;
        }
        
        // Hibernate the merged session
        await this.sessionManager.hibernateSession(sessionId);
        
        // Remove from metrics
        this.metrics.delete(sessionId);
        
        console.log('[AutoScaler] Merged session:', sessionId);
      }
      
      // Record in history
      this._addToHistory('merge', {
        targetSessionId,
        mergedSessions: sessionsToMerge
      });
      
      this.state.totalMerges++;
      
    } catch (error) {
      console.error('[AutoScaler] Failed to merge sessions:', error);
      throw error;
    }
  }
  
  /**
   * Balance load across sessions
   */
  async _balanceLoad(loadScores) {
    try {
      // Sort by load score
      loadScores.sort((a, b) => b.loadScore - a.loadScore);
      
      const overloaded = loadScores.filter(s => s.loadScore > 0.5);
      const underloaded = loadScores.filter(s => s.loadScore <= 0.5);
      
      if (overloaded.length === 0 || underloaded.length === 0) {
        return;
      }
      
      // In a real implementation, this would redistribute work
      // For now, we just log the imbalance
      console.log('[AutoScaler] Load balancing recommendation:');
      console.log('  Overloaded sessions:', overloaded.map(s => s.sessionId).join(', '));
      console.log('  Underloaded sessions:', underloaded.map(s => s.sessionId).join(', '));
      
      // Record in history
      this._addToHistory('balance', {
        overloaded: overloaded.map(s => s.sessionId),
        underloaded: underloaded.map(s => s.sessionId)
      });
      
    } catch (error) {
      console.error('[AutoScaler] Failed to balance load:', error);
    }
  }
  
  /**
   * Record action in history
   */
  _addToHistory(action, details) {
    const entry = {
      timestamp: Date.now(),
      action,
      details
    };
    
    this.state.history.push(entry);
    
    // Keep only last 100 entries
    if (this.state.history.length > 100) {
      this.state.history = this.state.history.slice(-100);
    }
  }
  
  /**
   * Record metrics history
   */
  _recordHistory() {
    const entry = {
      timestamp: Date.now(),
      sessions: Array.from(this.metrics.values()).map(m => m.toJSON())
    };
    
    // In a real implementation, this would be saved to a time-series database
    console.log('[AutoScaler] Current load:', 
      Array.from(this.metrics.values()).map(m => 
        `${m.sessionId}:${m.calculateLoadScore(this.config).toFixed(2)}`
      ).join(', ')
    );
  }
  
  /**
   * Get current status
   */
  getStatus() {
    const activeSessions = this.sessionManager ? 
      this.sessionManager.getActiveSessions() : [];
    
    return {
      initialized: this.initialized,
      activeSessions: activeSessions.length,
      metricsCount: this.metrics.size,
      config: this.config,
      state: {
        lastScaleUp: this.state.lastScaleUp,
        lastScaleDown: this.state.lastScaleDown,
        lastBalance: this.state.lastBalance,
        totalScaleUps: this.state.totalScaleUps,
        totalScaleDowns: this.state.totalScaleDowns,
        totalMerges: this.state.totalMerges
      },
      sessions: Array.from(this.metrics.values()).map(m => m.toJSON(this.config))
    };
  }
  
  /**
   * Get metrics for a specific session
   */
  getSessionMetrics(sessionId) {
    const metrics = this.metrics.get(sessionId);
    return metrics ? metrics.toJSON(this.config) : null;
  }
  
  /**
   * Get all metrics
   */
  getAllMetrics() {
    return Array.from(this.metrics.values()).map(m => m.toJSON(this.config));
  }
}

// Singleton instance
let instance = null;

/**
 * Get the auto-scaler instance
 */
function getSessionAutoScaler() {
  if (!instance) {
    instance = new SessionAutoScaler();
  }
  return instance;
}

// Export for usage
module.exports = {
  SessionAutoScaler,
  SessionMetrics,
  getSessionAutoScaler,
  DEFAULT_CONFIG
};
