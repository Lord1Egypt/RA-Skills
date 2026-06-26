/**
 * Security scan module
 * Pre-send content scan: reject if text matches sensitive patterns
 */

const DEFAULT_SCAN_PATTERNS = [
  'OPENAI_API_KEY',
  'sk-',
  'Bearer ',
  'Authorization:',
  'api_key',
  'apikey',
  'secret_key',
  'private_key',
  'password',
  'passwd',
];

/**
 * Scan text for sensitive strings
 * @param {string} text - Text to scan
 * @param {string[]} patterns - Patterns (regex-capable)
 * @throws {Error} When sensitive content is found
 */
export function scan(text, patterns = DEFAULT_SCAN_PATTERNS) {
  if (!text || typeof text !== 'string') return;

  for (const pattern of patterns) {
    try {
      const regex = new RegExp(pattern, 'i');
      if (regex.test(text)) {
        throw new Error(`Security scan failed: content matches sensitive pattern "${pattern}". Send rejected.`);
      }
    } catch (err) {
      if (err.message.includes('Security scan failed')) throw err;
      // Invalid regex: fall back to substring match
      if (text.toLowerCase().includes(pattern.toLowerCase())) {
        throw new Error(`Security scan failed: content matches sensitive pattern "${pattern}". Send rejected.`);
      }
    }
  }
}

/**
 * Scan and return result (does not throw)
 * @returns {{ safe: boolean, matched?: string }}
 */
export function scanSafe(text, patterns = DEFAULT_SCAN_PATTERNS) {
  try {
    scan(text, patterns);
    return { safe: true };
  } catch (err) {
    return { safe: false, matched: err.message };
  }
}
