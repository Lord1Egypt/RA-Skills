/**
 * Privacy Auditor - Security Monitoring & Compliance
 * 
 * Logs all privacy decisions, monitors boundary violations,
 * and maintains audit trail for compliance.
 */

const fs = require('fs').promises;
const path = require('path');

class PrivacyAuditor {
  constructor(privacyConfig, openclaw) {
    this.config = privacyConfig || {};
    this.openclaw = openclaw;
    this.auditLogPath = privacyConfig.auditLogPath || 'memory/nirvana-audit.log';
    this.enforceContextBoundary = privacyConfig.enforceContextBoundary !== false;
    this.auditLog = [];
    this.violations = [];
  }

  /**
   * Initialize auditor
   */
  async initialize() {
    // Create audit log file if it doesn't exist
    try {
      const dir = path.dirname(this.auditLogPath);
      await fs.mkdir(dir, { recursive: true });
      
      // Initialize log with header
      const header = `[Nirvana Privacy Audit Log - Started ${new Date().toISOString()}]\n`;
      await fs.appendFile(this.auditLogPath, header);
    } catch (error) {
      console.warn('[PrivacyAuditor] Failed to initialize log:', error.message);
    }
  }

  /**
   * Check privacy boundary before query
   */
  async checkBoundary(context) {
    if (!this.enforceContextBoundary) {
      return { allowed: true };
    }

    const violations = [];
    const identityFiles = this.config.identityFilesNeverExport || [];

    // Check for identity files in context
    for (const key of Object.keys(context || {})) {
      if (this.isIdentityFile(key, identityFiles)) {
        violations.push({
          type: 'identity-file-detected',
          key,
          severity: 'critical'
        });
      }
    }

    if (violations.length > 0) {
      await this.logViolation(violations);
      return {
        allowed: false,
        reason: `Privacy boundary violation: ${violations.map(v => v.type).join(', ')}`
      };
    }

    return { allowed: true };
  }

  /**
   * Log query (for audit trail)
   */
  async logQuery(query, context) {
    const entry = {
      timestamp: new Date().toISOString(),
      event: 'query',
      queryLength: typeof query === 'string' ? query.length : query.text?.length || 0,
      contextKeys: Object.keys(context || {}),
      privacyBoundaryEnforced: this.enforceContextBoundary
    };

    await this.writeAuditLog(entry);
  }

  /**
   * Log violation
   */
  async logViolation(violations) {
    const entry = {
      timestamp: new Date().toISOString(),
      event: 'violation',
      violations,
      severity: violations.some(v => v.severity === 'critical') ? 'critical' : 'warning'
    };

    this.violations.push(entry);
    await this.writeAuditLog(entry);

    if (entry.severity === 'critical') {
      console.error('[PrivacyAuditor] CRITICAL VIOLATION:', violations);
    }
  }

  /**
   * Write to audit log
   */
  async writeAuditLog(entry) {
    try {
      const logLine = JSON.stringify(entry) + '\n';
      await fs.appendFile(this.auditLogPath, logLine);
      this.auditLog.push(entry);

      // Keep in-memory log manageable
      if (this.auditLog.length > 10000) {
        this.auditLog = this.auditLog.slice(-5000);
      }
    } catch (error) {
      console.warn('[PrivacyAuditor] Failed to write audit log:', error.message);
    }
  }

  /**
   * Check if key is identity file
   */
  isIdentityFile(key, patterns = []) {
    const identityPatterns = patterns || this.config.identityFilesNeverExport || [];

    return identityPatterns.some(pattern => {
      if (pattern.endsWith('*')) {
        const prefix = pattern.slice(0, -1);
        return key.startsWith(prefix);
      }
      return key === pattern;
    });
  }

  /**
   * Get audit summary
   */
  getAuditSummary(hours = 24) {
    const cutoff = new Date(Date.now() - hours * 3600 * 1000);

    const recentEntries = this.auditLog.filter(entry =>
      new Date(entry.timestamp) > cutoff
    );

    const summary = {
      period: `${hours}h`,
      totalQueries: recentEntries.filter(e => e.event === 'query').length,
      violations: recentEntries.filter(e => e.event === 'violation').length,
      criticalViolations: recentEntries.filter(e =>
        e.event === 'violation' && e.severity === 'critical'
      ).length,
      violations: this.violations.filter(v =>
        new Date(v.timestamp) > cutoff
      )
    };

    return summary;
  }

  /**
   * Health check
   */
  healthCheck() {
    const recentViolations = this.violations.filter(v =>
      new Date(v.timestamp) > new Date(Date.now() - 1000 * 3600) // Last hour
    );

    return {
      enabled: this.enforceContextBoundary,
      logPath: this.auditLogPath,
      logSize: this.auditLog.length,
      recentViolations: recentViolations.length,
      criticalViolations: recentViolations.filter(v => v.severity === 'critical').length
    };
  }

  /**
   * Export audit log for compliance
   */
  async exportLog(outputPath) {
    try {
      const content = this.auditLog
        .map(entry => JSON.stringify(entry))
        .join('\n');

      await fs.writeFile(outputPath, content);
      console.log('[PrivacyAuditor] Exported audit log to:', outputPath);
    } catch (error) {
      console.error('[PrivacyAuditor] Failed to export log:', error.message);
      throw error;
    }
  }

  /**
   * Clear violations (with timestamp)
   */
  clearViolations() {
    const clearedCount = this.violations.length;
    this.violations = [];
    console.log('[PrivacyAuditor] Cleared ' + clearedCount + ' violation records');
  }

  /**
   * Shutdown
   */
  async shutdown() {
    try {
      const summary = this.getAuditSummary(24);
      const finalEntry = {
        timestamp: new Date().toISOString(),
        event: 'shutdown',
        summary
      };

      await this.writeAuditLog(finalEntry);
      console.log('[PrivacyAuditor] Audit log finalized');
    } catch (error) {
      console.warn('[PrivacyAuditor] Failed to finalize log:', error.message);
    }
  }
}

module.exports = PrivacyAuditor;
