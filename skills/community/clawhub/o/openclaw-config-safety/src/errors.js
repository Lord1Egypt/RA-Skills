/**
 * NormalizationError — thrown on fatal normalization failure
 *
 * Security: field path only, never the field value (credential exposure risk)
 */
class NormalizationError extends Error {
  constructor(field, message) {
    super(`normalizeOpenClawConfig: ${field}: ${message}`);
    this.name = "NormalizationError";
    this.field = field;
  }
}

/**
 * NormalizationWarning — non-fatal issue, collected but doesn't throw
 */
class NormalizationWarning {
  constructor(field, message) {
    this.field = field;
    this.message = message;
  }
  toString() {
    return `${this.field}: ${this.message}`;
  }
}

module.exports = { NormalizationError, NormalizationWarning };
