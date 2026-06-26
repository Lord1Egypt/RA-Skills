const fs = require('fs');
const path = require('path');

class AuditLogger {
  constructor() {
    this.logPath = path.join(__dirname, '../logs', 'routing-audit.log');
    this.ensureLogDirectory();
  }

  ensureLogDirectory() {
    const logDir = path.dirname(this.logPath);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
  }

  logRoutingDecision(decision) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      model: decision.model,
      reason: decision.reason,
      contextLength: decision.analysis?.contextLength || 0,
      privacyLevel: decision.analysis?.privacyLevel || 'unknown',
      taskType: decision.analysis?.taskType || 'unknown'
    };

    const logLine = JSON.stringify(logEntry) + '\n';
    
    try {
      fs.appendFileSync(this.logPath, logLine);
    } catch (error) {
      console.warn('Failed to write audit log:', error.message);
    }
  }

  getRecentDecisions(limit = 100) {
    try {
      if (!fs.existsSync(this.logPath)) {
        return [];
      }
      
      const content = fs.readFileSync(this.logPath, 'utf8');
      const lines = content.trim().split('\n').filter(line => line.length > 0);
      const decisions = lines.map(line => JSON.parse(line));
      
      return decisions.slice(-limit).reverse(); // Return most recent first
    } catch (error) {
      console.error('Failed to read audit log:', error);
      return [];
    }
  }

  getStats() {
    const decisions = this.getRecentDecisions(1000);
    if (decisions.length === 0) {
      return { total: 0, models: {}, privacyLevels: {}, taskTypes: {} };
    }

    const modelCounts = {};
    const privacyCounts = {};
    const taskTypeCounts = {};

    decisions.forEach(decision => {
      modelCounts[decision.model] = (modelCounts[decision.model] || 0) + 1;
      privacyCounts[decision.privacyLevel] = (privacyCounts[decision.privacyLevel] || 0) + 1;
      taskTypeCounts[decision.taskType] = (taskTypeCounts[decision.taskType] || 0) + 1;
    });

    return {
      total: decisions.length,
      models: modelCounts,
      privacyLevels: privacyCounts,
      taskTypes: taskTypeCounts,
      lastDecision: decisions[0].timestamp
    };
  }
}

module.exports = AuditLogger;