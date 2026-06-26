/**
 * PII Filter - Detects and redacts personally identifiable information
 *
 * Supports filtering of: emails, phone numbers, SSNs, credit cards,
 * IP addresses, and API keys/tokens.
 */
class PIIFilter {
  /**
   * @param {Object} options - Filter configuration
   * @param {boolean} options.enabled - Whether filtering is active (default: true)
   * @param {string[]} options.patterns - Which PII types to filter (default: all)
   * @param {string} options.replacement - Replacement text (default: '[REDACTED]')
   */
  constructor(options = {}) {
    this.enabled = options.enabled !== false;
    this.replacement = options.replacement || '[REDACTED]';

    const allPatterns = ['email', 'phone', 'ssn', 'creditCard', 'ipAddress', 'apiKey'];
    this.activePatterns = options.patterns || allPatterns;

    this.matchers = {
      email: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g,
      phone: /(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}/g,
      ssn: /\b\d{3}-\d{2}-\d{4}\b/g,
      creditCard: /\b(?:\d[ -]*?){13,19}\b/g,
      ipAddress: /\b(?:\d{1,3}\.){3}\d{1,3}\b/g,
      apiKey: /(?:sk|pk|key|token|api[_-]?key|bearer)[-_]?(?:[a-zA-Z0-9][-_]?){20,}/gi,
    };
  }

  /**
   * Filter PII from a string value
   * @param {string} value - The string to filter
   * @returns {string} - Filtered string
   */
  filterString(value) {
    if (!this.enabled || typeof value !== 'string') return value;

    let filtered = value;
    for (const patternName of this.activePatterns) {
      const matcher = this.matchers[patternName];
      if (matcher) {
        filtered = filtered.replace(matcher, this.replacement);
      }
    }
    return filtered;
  }

  /**
   * Recursively filter PII from an object or value
   * @param {*} data - The data to filter
   * @returns {*} - Filtered data
   */
  filter(data) {
    if (!this.enabled) return data;

    if (data === null || data === undefined) return data;

    if (typeof data === 'string') {
      return this.filterString(data);
    }

    if (Array.isArray(data)) {
      return data.map(item => this.filter(item));
    }

    if (typeof data === 'object') {
      const filtered = {};
      for (const [key, value] of Object.entries(data)) {
        filtered[key] = this.filter(value);
      }
      return filtered;
    }

    return data;
  }
}

module.exports = { PIIFilter };
