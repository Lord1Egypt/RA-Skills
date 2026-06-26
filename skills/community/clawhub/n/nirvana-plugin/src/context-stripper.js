/**
 * Context Stripper - Privacy Boundary Enforcement
 * 
 * Removes identity before sending queries to cloud APIs.
 * Never exports:
 * - SOUL.md
 * - USER.md
 * - AGENTS.md
 * - MEMORY.md
 * - Personal memory files
 * - SESSION-STATE.md
 */

class ContextStripper {
  constructor(privacyConfig = {}) {
    this.config = privacyConfig;
    this.identityFiles = privacyConfig.identityFilesNeverExport || [
      'SOUL.md',
      'USER.md',
      'AGENTS.md',
      'MEMORY.md',
      'memory/*',
      'SESSION-STATE.md'
    ];
    this.stripDepth = privacyConfig.contextStripDepth || 'moderate';
  }

  /**
   * Strip private context before cloud export
   */
  strip(context, query) {
    if (!this.config.enforceContextBoundary) {
      return context; // If boundary not enforced, return as-is
    }

    const stripped = {};

    // Iterate over context keys
    for (const [key, value] of Object.entries(context || {})) {
      // Skip identity files completely
      if (this.isIdentityFile(key)) {
        continue;
      }

      // For other keys, selectively include
      switch (this.stripDepth) {
        case 'aggressive':
          // Only include absolute minimum
          if (this.isEssential(key, query)) {
            stripped[key] = this.sanitizeValue(value);
          }
          break;

        case 'moderate':
          // Include non-sensitive context
          if (!this.isSensitive(key)) {
            stripped[key] = this.sanitizeValue(value);
          }
          break;

        case 'minimal':
          // Include everything except identity files
          stripped[key] = this.sanitizeValue(value);
          break;
      }
    }

    return stripped;
  }

  /**
   * Check if key is an identity file
   */
  isIdentityFile(key) {
    return this.identityFiles.some(pattern => {
      if (pattern.endsWith('*')) {
        const prefix = pattern.slice(0, -1);
        return key.startsWith(prefix);
      }
      return key === pattern;
    });
  }

  /**
   * Check if value is sensitive
   */
  isSensitive(key) {
    const sensitivePatterns = [
      'password',
      'token',
      'key',
      'secret',
      'credential',
      'api',
      'private',
      'auth',
      'session'
    ];

    return sensitivePatterns.some(pattern =>
      key.toLowerCase().includes(pattern)
    );
  }

  /**
   * Check if this value is essential for the query
   */
  isEssential(key, query) {
    const queryText = typeof query === 'string' ? query : query.text || '';

    // If query mentions the key, it's likely essential
    if (queryText.toLowerCase().includes(key.toLowerCase())) {
      return true;
    }

    // Domain keywords
    const domainKeywords = {
      biology: ['protein', 'gene', 'cell', 'crispr'],
      crypto: ['blockchain', 'ethereum', 'defi'],
      trading: ['price', 'portfolio', 'position']
    };

    for (const [domain, keywords] of Object.entries(domainKeywords)) {
      if (keywords.some(kw => queryText.toLowerCase().includes(kw))) {
        if (key.toLowerCase().includes(domain)) {
          return true;
        }
      }
    }

    return false;
  }

  /**
   * Sanitize values to remove sensitive data
   */
  sanitizeValue(value) {
    if (value === null || value === undefined) {
      return value;
    }

    if (typeof value === 'string') {
      return this.sanitizeString(value);
    }

    if (typeof value === 'object') {
      if (Array.isArray(value)) {
        return value.map(v => this.sanitizeValue(v));
      }

      const sanitized = {};
      for (const [k, v] of Object.entries(value)) {
        if (!this.isSensitive(k)) {
          sanitized[k] = this.sanitizeValue(v);
        }
      }
      return sanitized;
    }

    return value;
  }

  /**
   * Sanitize string values
   */
  sanitizeString(str) {
    // Remove email addresses
    str = str.replace(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g, '[EMAIL]');

    // Remove phone numbers
    str = str.replace(/\+?1?\d{9,15}/g, '[PHONE]');

    // Remove API keys (basic pattern)
    str = str.replace(/(api[_-]?key|secret|token)[:\s=]+([a-zA-Z0-9_-]{20,})/gi, '$1: [REDACTED]');

    // Remove wallet addresses
    str = str.replace(/0x[a-fA-F0-9]{40,}/g, '[WALLET]');

    // Remove private keys (very basic)
    if (str.includes('private') || str.includes('secret')) {
      str = str.replace(/([a-fA-F0-9]{64})/g, '[KEY]');
    }

    return str;
  }

  /**
   * Validate that context is safe to export
   */
  validate(context) {
    const violations = [];

    for (const [key, value] of Object.entries(context || {})) {
      // Check for identity files
      if (this.isIdentityFile(key)) {
        violations.push(`Identity file detected: ${key}`);
      }

      // Check for sensitive keys
      if (this.isSensitive(key)) {
        const valueStr = JSON.stringify(value);
        if (valueStr.length > 100) {
          violations.push(`Sensitive data in key: ${key}`);
        }
      }
    }

    return {
      safe: violations.length === 0,
      violations
    };
  }

  /**
   * Reconfigure stripper
   */
  reconfigure(newConfig) {
    this.config = newConfig || {};
    this.identityFiles = newConfig.identityFilesNeverExport || this.identityFiles;
    this.stripDepth = newConfig.contextStripDepth || this.stripDepth;
  }

  /**
   * Get audit report
   */
  getAuditReport(originalContext, strippedContext) {
    const originalKeys = Object.keys(originalContext || {});
    const strippedKeys = Object.keys(strippedContext || {});
    const removed = originalKeys.filter(k => !strippedKeys.includes(k));

    return {
      timestamp: new Date().toISOString(),
      originalKeyCount: originalKeys.length,
      strippedKeyCount: strippedKeys.length,
      removedKeys: removed,
      stripDepth: this.stripDepth,
      violations: removed.filter(k => this.isIdentityFile(k)).length
    };
  }
}

module.exports = ContextStripper;
