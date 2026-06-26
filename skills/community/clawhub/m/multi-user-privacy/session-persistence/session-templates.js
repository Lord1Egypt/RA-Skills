/**
 * Session Template Manager
 * 
 * Provides predefined and custom session templates for different user types:
 * 1. Admin Template - High quota, full permissions
 * 2. Standard Template - Standard quota, normal permissions
 * 3. Guest Template - Low quota, read-only
 * 4. Custom Templates - User-defined templates
 */

const fs = require('fs');
const path = require('path');

// Template storage location
const TEMPLATES_DIR = path.join(__dirname, '..', 'config', 'session-templates');
const TEMPLATES_CONFIG_FILE = path.join(TEMPLATES_DIR, 'templates-config.json');

// Built-in template IDs
const BUILTIN_TEMPLATES = {
  ADMIN: 'admin',
  STANDARD: 'standard',
  GUEST: 'guest'
};

// Default built-in templates
const DEFAULT_TEMPLATES = {
  [BUILTIN_TEMPLATES.ADMIN]: {
    id: BUILTIN_TEMPLATES.ADMIN,
    name: '管理员模板',
    description: '高配额、完整权限，适用于系统管理员',
    isBuiltIn: true,
    quota: {
      diskQuotaMB: 1024,        // 1GB
      tokenQuota: 1000000,       // 1M tokens
      messageQuota: 10000,       // 10K messages
      sessionTimeoutHours: 168,  // 7 days
      maxSubAgents: 10,          // Max concurrent sub-agents
      maxFileSize: 100,          // MB
      allowFileUpload: true,
      allowCodeExecution: true,
      allowExternalAPI: true,
      allowSystemCommands: true
    },
    permissions: {
      canManageUsers: true,
      canManageSessions: true,
      canManageTemplates: true,
      canAccessSystemLogs: true,
      canModifyConfig: true,
      canDeleteSessions: true,
      canExportData: true,
      canInstallSkills: true,
      canExecuteDangerousCommands: true,
      readOnly: false
    },
    features: {
      priority: 'high',
      autoSave: true,
      autoRecovery: true,
      advancedLogging: true,
      customVariables: true,
      webhooks: true
    },
    createdAt: Date.now(),
    updatedAt: Date.now()
  },

  [BUILTIN_TEMPLATES.STANDARD]: {
    id: BUILTIN_TEMPLATES.STANDARD,
    name: '普通用户模板',
    description: '标准配额，适用于常规用户',
    isBuiltIn: true,
    quota: {
      diskQuotaMB: 100,          // 100MB
      tokenQuota: 100000,        // 100K tokens
      messageQuota: 1000,        // 1K messages
      sessionTimeoutHours: 24,   // 1 day
      maxSubAgents: 3,           // Max concurrent sub-agents
      maxFileSize: 10,           // MB
      allowFileUpload: true,
      allowCodeExecution: true,
      allowExternalAPI: true,
      allowSystemCommands: false
    },
    permissions: {
      canManageUsers: false,
      canManageSessions: false,
      canManageTemplates: false,
      canAccessSystemLogs: false,
      canModifyConfig: false,
      canDeleteSessions: false,
      canExportData: true,
      canInstallSkills: false,
      canExecuteDangerousCommands: false,
      readOnly: false
    },
    features: {
      priority: 'normal',
      autoSave: true,
      autoRecovery: true,
      advancedLogging: false,
      customVariables: true,
      webhooks: false
    },
    createdAt: Date.now(),
    updatedAt: Date.now()
  },

  [BUILTIN_TEMPLATES.GUEST]: {
    id: BUILTIN_TEMPLATES.GUEST,
    name: '访客模板',
    description: '低配额、只读权限，适用于临时访客',
    isBuiltIn: true,
    quota: {
      diskQuotaMB: 10,           // 10MB
      tokenQuota: 10000,         // 10K tokens
      messageQuota: 100,         // 100 messages
      sessionTimeoutHours: 1,    // 1 hour
      maxSubAgents: 1,           // Max concurrent sub-agents
      maxFileSize: 1,            // MB
      allowFileUpload: false,
      allowCodeExecution: false,
      allowExternalAPI: false,
      allowSystemCommands: false
    },
    permissions: {
      canManageUsers: false,
      canManageSessions: false,
      canManageTemplates: false,
      canAccessSystemLogs: false,
      canModifyConfig: false,
      canDeleteSessions: false,
      canExportData: false,
      canInstallSkills: false,
      canExecuteDangerousCommands: false,
      readOnly: true
    },
    features: {
      priority: 'low',
      autoSave: false,
      autoRecovery: false,
      advancedLogging: false,
      customVariables: false,
      webhooks: false
    },
    createdAt: Date.now(),
    updatedAt: Date.now()
  }
};

class SessionTemplateManager {
  constructor() {
    this.templates = new Map();
    this.templatesDir = TEMPLATES_DIR;
    this.configFile = TEMPLATES_CONFIG_FILE;
    this.initialized = false;
  }

  /**
   * Initialize the template manager
   * Loads existing templates from disk
   */
  async initialize() {
    try {
      // Ensure templates directory exists
      await this._ensureDirectories();
      
      // Load templates from disk
      await this._loadTemplates();
      
      // Ensure built-in templates exist
      await this._ensureBuiltInTemplates();
      
      this.initialized = true;
      console.log('[SessionTemplate] Initialized with', this.templates.size, 'templates');
      
      return true;
    } catch (error) {
      console.error('[SessionTemplate] Initialization failed:', error);
      return false;
    }
  }

  /**
   * Ensure templates directory exists
   */
  async _ensureDirectories() {
    if (!fs.existsSync(this.templatesDir)) {
      fs.mkdirSync(this.templatesDir, { recursive: true });
      console.log('[SessionTemplate] Created templates directory:', this.templatesDir);
    }
  }

  /**
   * Load templates from disk
   */
  async _loadTemplates() {
    if (fs.existsSync(this.configFile)) {
      try {
        const data = fs.readFileSync(this.configFile, 'utf-8');
        const config = JSON.parse(data);
        
        if (config.templates && Array.isArray(config.templates)) {
          for (const templateData of config.templates) {
            this.templates.set(templateData.id, templateData);
          }
        }
        
        console.log('[SessionTemplate] Loaded', this.templates.size, 'templates from disk');
      } catch (error) {
        console.error('[SessionTemplate] Failed to load templates:', error);
      }
    } else {
      console.log('[SessionTemplate] No existing templates config, starting fresh');
    }
  }

  /**
   * Ensure all built-in templates exist
   */
  async _ensureBuiltInTemplates() {
    let updated = false;
    
    for (const [templateId, templateData] of Object.entries(DEFAULT_TEMPLATES)) {
      if (!this.templates.has(templateId)) {
        this.templates.set(templateId, templateData);
        updated = true;
        console.log('[SessionTemplate] Added built-in template:', templateId);
      } else {
        // Update built-in templates if they have changed
        const existing = this.templates.get(templateId);
        if (existing.isBuiltIn) {
          // Merge updates while preserving user customizations
          const updatedTemplate = this._mergeTemplateUpdates(existing, templateData);
          this.templates.set(templateId, updatedTemplate);
          updated = true;
        }
      }
    }
    
    if (updated) {
      await this._saveTemplates();
    }
  }

  /**
   * Merge template updates (preserves customizations)
   */
  _mergeTemplateUpdates(existing, newTemplate) {
    return {
      ...newTemplate,
      ...existing,
      quota: { ...newTemplate.quota, ...existing.quota },
      permissions: { ...newTemplate.permissions, ...existing.permissions },
      features: { ...newTemplate.features, ...existing.features },
      updatedAt: Date.now()
    };
  }

  /**
   * Save templates to disk
   */
  async _saveTemplates() {
    try {
      const config = {
        version: 1,
        lastSaved: Date.now(),
        templateCount: this.templates.size,
        templates: Array.from(this.templates.values())
      };
      
      fs.writeFileSync(this.configFile, JSON.stringify(config, null, 2), 'utf-8');
      console.log('[SessionTemplate] Templates saved to', this.configFile);
    } catch (error) {
      console.error('[SessionTemplate] Failed to save templates:', error);
      throw error;
    }
  }

  /**
   * Get a template by ID
   */
  getTemplate(templateId) {
    return this.templates.get(templateId);
  }

  /**
   * Get all templates
   */
  getAllTemplates() {
    return Array.from(this.templates.values());
  }

  /**
   * Get only custom (non-built-in) templates
   */
  getCustomTemplates() {
    return Array.from(this.templates.values()).filter(t => !t.isBuiltIn);
  }

  /**
   * Create a custom template
   */
  async createTemplate(templateData) {
    const { id, name, description } = templateData;
    
    if (!id || !name) {
      throw new Error('Template ID and name are required');
    }
    
    if (this.templates.has(id)) {
      throw new Error(`Template '${id}' already exists`);
    }
    
    // Check if trying to create with a built-in ID
    if (Object.values(BUILTIN_TEMPLATES).includes(id)) {
      throw new Error(`Cannot create custom template with built-in ID: ${id}`);
    }
    
    const template = {
      id,
      name,
      description: description || '',
      isBuiltIn: false,
      quota: {
        diskQuotaMB: templateData.quota?.diskQuotaMB || 100,
        tokenQuota: templateData.quota?.tokenQuota || 100000,
        messageQuota: templateData.quota?.messageQuota || 1000,
        sessionTimeoutHours: templateData.quota?.sessionTimeoutHours || 24,
        maxSubAgents: templateData.quota?.maxSubAgents || 3,
        maxFileSize: templateData.quota?.maxFileSize || 10,
        allowFileUpload: templateData.quota?.allowFileUpload ?? true,
        allowCodeExecution: templateData.quota?.allowCodeExecution ?? true,
        allowExternalAPI: templateData.quota?.allowExternalAPI ?? true,
        allowSystemCommands: templateData.quota?.allowSystemCommands ?? false
      },
      permissions: {
        canManageUsers: templateData.permissions?.canManageUsers ?? false,
        canManageSessions: templateData.permissions?.canManageSessions ?? false,
        canManageTemplates: templateData.permissions?.canManageTemplates ?? false,
        canAccessSystemLogs: templateData.permissions?.canAccessSystemLogs ?? false,
        canModifyConfig: templateData.permissions?.canModifyConfig ?? false,
        canDeleteSessions: templateData.permissions?.canDeleteSessions ?? false,
        canExportData: templateData.permissions?.canExportData ?? true,
        canInstallSkills: templateData.permissions?.canInstallSkills ?? false,
        canExecuteDangerousCommands: templateData.permissions?.canExecuteDangerousCommands ?? false,
        readOnly: templateData.permissions?.readOnly ?? false
      },
      features: {
        priority: templateData.features?.priority || 'normal',
        autoSave: templateData.features?.autoSave ?? true,
        autoRecovery: templateData.features?.autoRecovery ?? true,
        advancedLogging: templateData.features?.advancedLogging ?? false,
        customVariables: templateData.features?.customVariables ?? true,
        webhooks: templateData.features?.webhooks ?? false
      },
      createdAt: Date.now(),
      updatedAt: Date.now()
    };
    
    this.templates.set(id, template);
    await this._saveTemplates();
    
    console.log('[SessionTemplate] Created custom template:', id);
    return template;
  }

  /**
   * Update an existing custom template
   */
  async updateTemplate(templateId, updates) {
    const template = this.templates.get(templateId);
    
    if (!template) {
      throw new Error(`Template '${templateId}' not found`);
    }
    
    if (template.isBuiltIn) {
      throw new Error(`Cannot modify built-in template: ${templateId}`);
    }
    
    // Apply updates
    if (updates.name) template.name = updates.name;
    if (updates.description !== undefined) template.description = updates.description;
    if (updates.quota) template.quota = { ...template.quota, ...updates.quota };
    if (updates.permissions) template.permissions = { ...template.permissions, ...updates.permissions };
    if (updates.features) template.features = { ...template.features, ...updates.features };
    
    template.updatedAt = Date.now();
    
    this.templates.set(templateId, template);
    await this._saveTemplates();
    
    console.log('[SessionTemplate] Updated template:', templateId);
    return template;
  }

  /**
   * Delete a custom template
   */
  async deleteTemplate(templateId) {
    const template = this.templates.get(templateId);
    
    if (!template) {
      throw new Error(`Template '${templateId}' not found`);
    }
    
    if (template.isBuiltIn) {
      throw new Error(`Cannot delete built-in template: ${templateId}`);
    }
    
    this.templates.delete(templateId);
    await this._saveTemplates();
    
    console.log('[SessionTemplate] Deleted template:', templateId);
    return true;
  }

  /**
   * Apply a template to session configuration
   */
  applyTemplateToSession(templateId, sessionConfig = {}) {
    const template = this.templates.get(templateId);
    
    if (!template) {
      throw new Error(`Template '${templateId}' not found`);
    }
    
    // Merge template with session config (session config takes precedence)
    return {
      templateId,
      quota: { ...template.quota, ...sessionConfig.quota },
      permissions: { ...template.permissions, ...sessionConfig.permissions },
      features: { ...template.features, ...sessionConfig.features },
      metadata: {
        templateName: template.name,
        templateDescription: template.description,
        appliedAt: Date.now()
      }
    };
  }

  /**
   * Validate session against template quotas
   */
  validateSessionQuota(sessionId, templateId, usage) {
    const template = this.templates.get(templateId);
    
    if (!template) {
      return { valid: false, error: 'Template not found' };
    }
    
    const violations = [];
    
    if (usage.diskMB > template.quota.diskQuotaMB) {
      violations.push(`Disk usage (${usage.diskMB}MB) exceeds quota (${template.quota.diskQuotaMB}MB)`);
    }
    
    if (usage.tokens > template.quota.tokenQuota) {
      violations.push(`Token usage (${usage.tokens}) exceeds quota (${template.quota.tokenQuota})`);
    }
    
    if (usage.messages > template.quota.messageQuota) {
      violations.push(`Message count (${usage.messages}) exceeds quota (${template.quota.messageQuota})`);
    }
    
    return {
      valid: violations.length === 0,
      violations,
      quota: template.quota
    };
  }

  /**
   * Check if user has permission based on template
   */
  checkPermission(templateId, permission) {
    const template = this.templates.get(templateId);
    
    if (!template) {
      return false;
    }
    
    return template.permissions[permission] || false;
  }

  /**
   * Export templates for backup
   */
  async exportTemplates() {
    const exportData = {
      exportedAt: Date.now(),
      version: 1,
      templates: Array.from(this.templates.values())
    };
    
    const exportPath = path.join(this.templatesDir, 'templates-export-' + Date.now() + '.json');
    fs.writeFileSync(exportPath, JSON.stringify(exportData, null, 2), 'utf-8');
    
    return exportPath;
  }

  /**
   * Import templates from backup
   */
  async importTemplates(exportPath) {
    try {
      const data = fs.readFileSync(exportPath, 'utf-8');
      const exportData = JSON.parse(data);
      
      if (!exportData.templates || !Array.isArray(exportData.templates)) {
        throw new Error('Invalid export format');
      }
      
      let imported = 0;
      for (const templateData of exportData.templates) {
        // Don't overwrite built-in templates
        if (!templateData.isBuiltIn || !this.templates.has(templateData.id)) {
          this.templates.set(templateData.id, templateData);
          imported++;
        }
      }
      
      await this._saveTemplates();
      console.log('[SessionTemplate] Imported', imported, 'templates');
      
      return imported;
    } catch (error) {
      console.error('[SessionTemplate] Failed to import templates:', error);
      throw error;
    }
  }

  /**
   * Get template statistics
   */
  getStats() {
    const templates = Array.from(this.templates.values());
    return {
      total: templates.length,
      builtIn: templates.filter(t => t.isBuiltIn).length,
      custom: templates.filter(t => !t.isBuiltIn).length,
      templateIds: templates.map(t => t.id)
    };
  }
}

// Singleton instance
let instance = null;

function getTemplateManager() {
  if (!instance) {
    instance = new SessionTemplateManager();
  }
  return instance;
}

// Export for usage
module.exports = {
  SessionTemplateManager,
  BUILTIN_TEMPLATES,
  DEFAULT_TEMPLATES,
  getTemplateManager
};
