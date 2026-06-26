// Multi-Model Router Skill Entry Point
const fs = require('fs');
const path = require('path');
const MultiModelRouter = require('./scripts/router');
const AuditLogger = require('./scripts/audit-logger');

class MultiModelRouterSkill {
  constructor() {
    this.config = this.loadConfig();
    this.router = new MultiModelRouter(this.config);
    this.userPreferences = this.loadUserPreferences();
    this.auditLogger = new AuditLogger();
  }

  loadConfig() {
    try {
      const configPath = path.join(__dirname, 'config', 'default.json');
      return JSON.parse(fs.readFileSync(configPath, 'utf8'));
    } catch (error) {
      console.error('Failed to load config:', error);
      // Return minimal default config
      return {
        models: {
          high_context: {
            alias: "xinliu/qwen3-max",
            context_window: 256000,
            privacy_level: "cloud",
            priority: 1
          },
          offline: {
            alias: "ollama/qwen35-32k", 
            context_window: 32768,
            privacy_level: "local",
            priority: 2
          }
        },
        fallback_strategy: "high_context"
      };
    }
  }

  loadUserPreferences() {
    try {
      const prefsPath = path.join(__dirname, 'config', 'user-preferences.json');
      if (fs.existsSync(prefsPath)) {
        return JSON.parse(fs.readFileSync(prefsPath, 'utf8'));
      }
    } catch (error) {
      console.warn('No user preferences found, using defaults');
    }
    return {
      default_mode: "auto",
      privacy_threshold: "medium",
      cost_sensitivity: true,
      performance_priority: false
    };
  }

  async routeModel(prompt, context = "", requirements = {}) {
    // Merge user preferences with requirements
    const mergedRequirements = {
      ...this.userPreferences,
      ...requirements
    };

    // Route to the best model
    const result = await this.router.route(prompt, context, mergedRequirements);
    
    // Log routing decision for auditing
    this.auditLogger.logRoutingDecision(result);
    
    // Log routing decision for debugging
    console.log(`[MultiModelRouter] Selected model: ${result.model} (${result.reason})`);
    
    return result;
  }

  // OpenClaw skill interface methods
  async handleRequest(request) {
    const { prompt, context, requirements } = request;
    return await this.routeModel(prompt, context, requirements);
  }

  async updatePreferences(newPreferences) {
    this.userPreferences = { ...this.userPreferences, ...newPreferences };
    this.saveUserPreferences();
  }

  saveUserPreferences() {
    try {
      const prefsPath = path.join(__dirname, 'config', 'user-preferences.json');
      fs.writeFileSync(prefsPath, JSON.stringify(this.userPreferences, null, 2));
    } catch (error) {
      console.error('Failed to save user preferences:', error);
    }
  }

  // Health check method
  getHealthStatus() {
    const routerHealth = this.router.getHealthStatus();
    const auditStats = this.auditLogger.getStats();
    
    return {
      status: 'healthy',
      models: Object.keys(this.config.models),
      active: true,
      version: '1.0.0',
      router: routerHealth,
      audit: auditStats
    };
  }
  
  // Get audit logs
  getAuditLogs(limit = 100) {
    return this.auditLogger.getRecentDecisions(limit);
  }
}

// Export as OpenClaw skill
module.exports = new MultiModelRouterSkill();