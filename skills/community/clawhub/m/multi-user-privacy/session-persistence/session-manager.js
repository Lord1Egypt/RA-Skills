/**
 * Session Persistence Manager
 * 
 * Features:
 * 1. Save session state to disk
 * 2. Auto-recovery on restart
 * 3. State migration (active → hibernating → archived)
 * 4. Session template support (admin/standard/guest/custom)
 * 5. Test utilities
 */

const fs = require('fs');
const path = require('path');
const { getTemplateManager, BUILTIN_TEMPLATES } = require('./session-templates');

// Configuration
const SESSIONS_DIR = path.join(__dirname, '..', 'memory', 'sessions');
const SESSION_STATE_FILE = path.join(__dirname, '..', 'memory', 'session-state.json');
const ARCHIVE_DIR = path.join(__dirname, '..', 'memory', 'sessions-archive');

// Session states
const SessionState = {
  ACTIVE: 'active',
  HIBERNATING: 'hibernating',
  ARCHIVED: 'archived'
};

// Session metadata structure
class Session {
  constructor(id, userId = null, channel = null, templateId = null) {
    this.id = id;
    this.userId = userId;
    this.channel = channel;
    this.templateId = templateId || BUILTIN_TEMPLATES.STANDARD;
    this.state = SessionState.ACTIVE;
    this.createdAt = Date.now();
    this.lastActivityAt = Date.now();
    this.hibernatedAt = null;
    this.archivedAt = null;
    this.context = {};
    this.variables = {};
    this.messageCount = 0;
    this.metadata = {};
    this.quota = null;
    this.permissions = null;
    this.usage = {
      diskMB: 0,
      tokens: 0,
      messages: 0,
      subAgents: 0
    };
  }

  toJSON() {
    return {
      id: this.id,
      userId: this.userId,
      channel: this.channel,
      templateId: this.templateId,
      state: this.state,
      createdAt: this.createdAt,
      lastActivityAt: this.lastActivityAt,
      hibernatedAt: this.hibernatedAt,
      archivedAt: this.archivedAt,
      context: this.context,
      variables: this.variables,
      messageCount: this.messageCount,
      metadata: this.metadata,
      quota: this.quota,
      permissions: this.permissions,
      usage: this.usage
    };
  }

  static fromJSON(data) {
    const session = new Session(data.id, data.userId, data.channel, data.templateId);
    session.state = data.state;
    session.createdAt = data.createdAt;
    session.lastActivityAt = data.lastActivityAt;
    session.hibernatedAt = data.hibernatedAt;
    session.archivedAt = data.archivedAt;
    session.context = data.context || {};
    session.variables = data.variables || {};
    session.messageCount = data.messageCount || 0;
    session.metadata = data.metadata || {};
    session.quota = data.quota || null;
    session.permissions = data.permissions || null;
    session.usage = data.usage || { diskMB: 0, tokens: 0, messages: 0, subAgents: 0 };
    return session;
  }
}

class SessionPersistenceManager {
  constructor() {
    this.sessions = new Map();
    this.stateFile = SESSION_STATE_FILE;
    this.sessionsDir = SESSIONS_DIR;
    this.archiveDir = ARCHIVE_DIR;
    this.initialized = false;
    this.templateManager = null;
    
    // Auto-hibernation config (in ms)
    this.hibernationTimeout = 30 * 60 * 1000; // 30 minutes
    this.archiveTimeout = 24 * 60 * 60 * 1000; // 24 hours
  }

  /**
   * Initialize the session manager
   * Loads existing sessions from disk and initializes template manager
   */
  async initialize() {
    try {
      // Initialize template manager first
      this.templateManager = getTemplateManager();
      await this.templateManager.initialize();
      
      // Ensure directories exist
      await this._ensureDirectories();
      
      // Load session state
      await this._loadState();
      
      // Recover active sessions
      await this._recoverSessions();
      
      this.initialized = true;
      console.log('[SessionPersistence] Initialized with', this.sessions.size, 'sessions');
      
      // Start auto-migration checker
      this._startMigrationChecker();
      
      return true;
    } catch (error) {
      console.error('[SessionPersistence] Initialization failed:', error);
      return false;
    }
  }

  /**
   * Ensure required directories exist
   */
  async _ensureDirectories() {
    const dirs = [this.sessionsDir, this.archiveDir];
    for (const dir of dirs) {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
        console.log('[SessionPersistence] Created directory:', dir);
      }
    }
  }

  /**
   * Load global session state from disk
   */
  async _loadState() {
    if (fs.existsSync(this.stateFile)) {
      try {
        const data = fs.readFileSync(this.stateFile, 'utf-8');
        const state = JSON.parse(data);
        
        // Load each session
        if (state.sessions && Array.isArray(state.sessions)) {
          for (const sessionData of state.sessions) {
            const session = Session.fromJSON(sessionData);
            this.sessions.set(session.id, session);
          }
        }
        
        console.log('[SessionPersistence] Loaded', this.sessions.size, 'sessions from disk');
      } catch (error) {
        console.error('[SessionPersistence] Failed to load state:', error);
        // Create fresh state file
        await this._saveState();
      }
    } else {
      console.log('[SessionPersistence] No existing state file, starting fresh');
      await this._saveState();
    }
  }

  /**
   * Save global session state to disk
   */
  async _saveState() {
    try {
      const state = {
        version: 1,
        lastSaved: Date.now(),
        sessionCount: this.sessions.size,
        sessions: Array.from(this.sessions.values()).map(s => s.toJSON())
      };
      
      fs.writeFileSync(this.stateFile, JSON.stringify(state, null, 2), 'utf-8');
      console.log('[SessionPersistence] State saved to', this.stateFile);
    } catch (error) {
      console.error('[SessionPersistence] Failed to save state:', error);
      throw error;
    }
  }

  /**
   * Recover sessions from disk (for restart scenarios)
   */
  async _recoverSessions() {
    const recovered = [];
    
    for (const [sessionId, session] of this.sessions) {
      const sessionDir = path.join(this.sessionsDir, sessionId);
      
      if (fs.existsSync(sessionDir)) {
        // Load session-specific files
        const userMdPath = path.join(sessionDir, 'user.md');
        if (fs.existsSync(userMdPath)) {
          session.context.userMd = fs.readFileSync(userMdPath, 'utf-8');
        }
        
        const contextPath = path.join(sessionDir, 'context.json');
        if (fs.existsSync(contextPath)) {
          const contextData = JSON.parse(fs.readFileSync(contextPath, 'utf-8'));
          session.context = { ...session.context, ...contextData };
        }
        
        // Mark as recovered if it was active
        if (session.state === SessionState.ACTIVE) {
          session.metadata.recovered = true;
          session.metadata.recoveredAt = Date.now();
          recovered.push(sessionId);
        }
      }
    }
    
    if (recovered.length > 0) {
      console.log('[SessionPersistence] Recovered', recovered.length, 'active sessions:', recovered);
    }
  }

  /**
   * Create a new session with optional template
   */
  async createSession(sessionId, userId = null, channel = null, templateId = null, sessionConfig = {}) {
    if (this.sessions.has(sessionId)) {
      console.log('[SessionPersistence] Session already exists:', sessionId);
      return this.sessions.get(sessionId);
    }
    
    // Determine template to use
    const effectiveTemplateId = templateId || BUILTIN_TEMPLATES.STANDARD;
    
    // Apply template configuration
    let templateConfig = null;
    if (this.templateManager) {
      try {
        templateConfig = this.templateManager.applyTemplateToSession(effectiveTemplateId, sessionConfig);
      } catch (error) {
        console.warn('[SessionPersistence] Failed to apply template, using defaults:', error.message);
      }
    }
    
    const session = new Session(sessionId, userId, channel, effectiveTemplateId);
    
    // Apply template quota and permissions
    if (templateConfig) {
      session.quota = templateConfig.quota;
      session.permissions = templateConfig.permissions;
      session.metadata.template = templateConfig.metadata;
    }
    
    this.sessions.set(sessionId, session);
    
    // Create session directory
    const sessionDir = path.join(this.sessionsDir, sessionId);
    if (!fs.existsSync(sessionDir)) {
      fs.mkdirSync(sessionDir, { recursive: true });
    }
    
    // Save initial state
    await this._saveState();
    await this._saveSessionContext(session);
    
    console.log('[SessionPersistence] Created session:', sessionId, 'with template:', effectiveTemplateId);
    return session;
  }

  /**
   * Get a session by ID
   */
  getSession(sessionId) {
    return this.sessions.get(sessionId);
  }

  /**
   * Update session activity timestamp
   */
  async touchSession(sessionId) {
    const session = this.sessions.get(sessionId);
    if (session) {
      session.lastActivityAt = Date.now();
      session.messageCount++;
      
      // If hibernating, wake it up
      if (session.state === SessionState.HIBERNATING) {
        session.state = SessionState.ACTIVE;
        session.hibernatedAt = null;
        console.log('[SessionPersistence] Session awakened:', sessionId);
      }
      
      await this._saveState();
    }
  }

  /**
   * Set session context/variables
   */
  async setSessionContext(sessionId, key, value) {
    const session = this.sessions.get(sessionId);
    if (session) {
      session.context[key] = value;
      await this._saveSessionContext(session);
      await this._saveState();
    }
  }

  /**
   * Set session variable
   */
  async setSessionVariable(sessionId, key, value) {
    const session = this.sessions.get(sessionId);
    if (session) {
      session.variables[key] = value;
      await this._saveState();
    }
  }

  /**
   * Save session context to disk
   */
  async _saveSessionContext(session) {
    const sessionDir = path.join(this.sessionsDir, session.id);
    
    // Save context.json
    const contextPath = path.join(sessionDir, 'context.json');
    fs.writeFileSync(contextPath, JSON.stringify(session.context, null, 2), 'utf-8');
    
    // Save user.md if present
    if (session.context.userMd) {
      const userMdPath = path.join(sessionDir, 'user.md');
      fs.writeFileSync(userMdPath, session.context.userMd, 'utf-8');
    }
  }

  /**
   * Migrate session to hibernating state
   */
  async hibernateSession(sessionId) {
    const session = this.sessions.get(sessionId);
    if (!session || session.state !== SessionState.ACTIVE) {
      return false;
    }
    
    session.state = SessionState.HIBERNATING;
    session.hibernatedAt = Date.now();
    
    await this._saveState();
    console.log('[SessionPersistence] Session hibernated:', sessionId);
    return true;
  }

  /**
   * Migrate session to archived state
   */
  async archiveSession(sessionId) {
    const session = this.sessions.get(sessionId);
    if (!session) {
      return false;
    }
    
    // Move to archive
    session.state = SessionState.ARCHIVED;
    session.archivedAt = Date.now();
    
    // Move session directory to archive
    const sourceDir = path.join(this.sessionsDir, sessionId);
    const targetDir = path.join(this.archiveDir, sessionId);
    
    if (fs.existsSync(sourceDir)) {
      if (!fs.existsSync(this.archiveDir)) {
        fs.mkdirSync(this.archiveDir, { recursive: true });
      }
      
      // Move directory
      fs.renameSync(sourceDir, targetDir);
      console.log('[SessionPersistence] Session directory archived:', sessionId);
    }
    
    // Keep in sessions map for persistence, but mark as archived
    // This allows recovery and audit trail
    await this._saveState();
    
    console.log('[SessionPersistence] Session archived:', sessionId);
    return true;
  }

  /**
   * Start periodic migration checker
   */
  _startMigrationChecker() {
    setInterval(async () => {
      const now = Date.now();
      
      for (const [sessionId, session] of this.sessions) {
        // Check for hibernation
        if (session.state === SessionState.ACTIVE) {
          const inactiveTime = now - session.lastActivityAt;
          if (inactiveTime > this.hibernationTimeout) {
            await this.hibernateSession(sessionId);
          }
        }
        
        // Check for archival
        if (session.state === SessionState.HIBERNATING) {
          const hibernatingTime = now - session.hibernatedAt;
          if (hibernatingTime > this.archiveTimeout) {
            await this.archiveSession(sessionId);
          }
        }
      }
    }, 60 * 1000); // Check every minute
    
    console.log('[SessionPersistence] Migration checker started');
  }

  /**
   * Get all active sessions
   */
  getActiveSessions() {
    return Array.from(this.sessions.values()).filter(
      s => s.state === SessionState.ACTIVE
    );
  }

  /**
   * Get session statistics
   */
  getStats() {
    const sessions = Array.from(this.sessions.values());
    return {
      total: sessions.length,
      active: sessions.filter(s => s.state === SessionState.ACTIVE).length,
      hibernating: sessions.filter(s => s.state === SessionState.HIBERNATING).length,
      archived: sessions.filter(s => s.state === SessionState.ARCHIVED).length
    };
  }

  /**
   * Check if session has permission
   */
  hasPermission(sessionId, permission) {
    const session = this.sessions.get(sessionId);
    if (!session || !session.permissions) {
      return false;
    }
    return session.permissions[permission] || false;
  }

  /**
   * Validate session quota usage
   */
  validateQuota(sessionId, usageType, value) {
    const session = this.sessions.get(sessionId);
    if (!session || !session.quota) {
      return { valid: true }; // No quota限制
    }
    
    let quotaLimit = null;
    let currentValue = 0;
    
    switch (usageType) {
      case 'disk':
        quotaLimit = session.quota.diskQuotaMB;
        currentValue = session.usage.diskMB;
        break;
      case 'tokens':
        quotaLimit = session.quota.tokenQuota;
        currentValue = session.usage.tokens;
        break;
      case 'messages':
        quotaLimit = session.quota.messageQuota;
        currentValue = session.usage.messages;
        break;
      case 'subAgents':
        quotaLimit = session.quota.maxSubAgents;
        currentValue = session.usage.subAgents;
        break;
      default:
        return { valid: true };
    }
    
    if (quotaLimit === null) {
      return { valid: true };
    }
    
    const valid = (currentValue + value) <= quotaLimit;
    return {
      valid,
      limit: quotaLimit,
      current: currentValue,
      remaining: quotaLimit - currentValue,
      requested: value
    };
  }

  /**
   * Update session usage
   */
  async updateUsage(sessionId, usageType, value) {
    const session = this.sessions.get(sessionId);
    if (!session) {
      return false;
    }
    
    switch (usageType) {
      case 'disk':
        session.usage.diskMB += value;
        break;
      case 'tokens':
        session.usage.tokens += value;
        break;
      case 'messages':
        session.usage.messages += value;
        break;
      case 'subAgents':
        session.usage.subAgents += value;
        break;
    }
    
    await this._saveState();
    return true;
  }

  /**
   * Get session template info
   */
  getSessionTemplate(sessionId) {
    const session = this.sessions.get(sessionId);
    if (!session || !this.templateManager) {
      return null;
    }
    return this.templateManager.getTemplate(session.templateId);
  }

  /**
   * Change session template
   */
  async changeSessionTemplate(sessionId, newTemplateId) {
    const session = this.sessions.get(sessionId);
    if (!session || !this.templateManager) {
      return false;
    }
    
    try {
      const templateConfig = this.templateManager.applyTemplateToSession(newTemplateId);
      session.templateId = newTemplateId;
      session.quota = templateConfig.quota;
      session.permissions = templateConfig.permissions;
      session.metadata.template = templateConfig.metadata;
      
      await this._saveState();
      console.log('[SessionPersistence] Changed template for session:', sessionId, 'to:', newTemplateId);
      return true;
    } catch (error) {
      console.error('[SessionPersistence] Failed to change template:', error.message);
      return false;
    }
  }

  /**
   * Export session data for backup
   */
  async exportSessions() {
    const exportData = {
      exportedAt: Date.now(),
      version: 1,
      sessions: Array.from(this.sessions.values()).map(s => s.toJSON())
    };
    
    const exportPath = path.join(__dirname, '..', 'memory', 'sessions-export-' + Date.now() + '.json');
    fs.writeFileSync(exportPath, JSON.stringify(exportData, null, 2), 'utf-8');
    
    return exportPath;
  }
}

// Singleton instance
let instance = null;

function getSessionManager() {
  if (!instance) {
    instance = new SessionPersistenceManager();
  }
  return instance;
}

// Export for testing and usage
module.exports = {
  SessionPersistenceManager,
  Session,
  SessionState,
  getSessionManager
};
