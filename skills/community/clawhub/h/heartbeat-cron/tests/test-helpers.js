/**
 * Test helpers for heartbeat-cron skill tests
 */

import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

/**
 * Parse YAML frontmatter from markdown content
 * @param {string} content - Markdown content with YAML frontmatter
 * @returns {object|null} Parsed frontmatter object or null if invalid
 */
export function parseFrontmatter(content) {
  const frontmatterRegex = /^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/;
  const match = content.match(frontmatterRegex);
  
  if (!match) {
    return null;
  }
  
  const yamlContent = match[1];
  const bodyContent = match[2];
  
  // Simple YAML parser for heartbeat frontmatter
  const frontmatter = {};
  const lines = yamlContent.split('\n');
  
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) {
      continue;
    }
    
    const colonIndex = line.indexOf(':');
    if (colonIndex === -1) {
      continue;
    }
    
    const key = line.slice(0, colonIndex).trim();
    let value = line.slice(colonIndex + 1).trim();
    
    // Remove quotes if present
    if ((value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    
    // Convert boolean strings
    if (value === 'true') {
      value = true;
    } else if (value === 'false') {
      value = false;
    }
    
    // Convert numbers (but not if they're quoted)
    const originalValue = line.slice(colonIndex + 1).trim();
    if (/^\d+$/.test(value) && !originalValue.startsWith('"') && !originalValue.startsWith("'")) {
      value = parseInt(value, 10);
    }
    
    frontmatter[key] = value;
  }
  
  return {
    frontmatter,
    body: bodyContent.trim()
  };
}

/**
 * Validate interval format (e.g., 15m, 1h, 6h, 1d)
 * @param {string} interval - Interval string to validate
 * @returns {boolean} True if valid interval format
 */
export function isValidInterval(interval) {
  if (typeof interval !== 'string') {
    return false;
  }
  
  const intervalPattern = /^(\d+)(m|h|d)$/;
  const match = interval.match(intervalPattern);
  
  if (!match) {
    return false;
  }
  
  const value = parseInt(match[1], 10);
  const unit = match[2];
  
  // Validate reasonable ranges
  if (unit === 'm' && (value < 1 || value > 1440)) {
    return false;
  }
  if (unit === 'h' && (value < 1 || value > 168)) {
    return false;
  }
  if (unit === 'd' && (value < 1 || value > 365)) {
    return false;
  }
  
  return true;
}

/**
 * Validate cron expression (basic 5-field validation)
 * @param {string} cron - Cron expression to validate
 * @returns {boolean} True if valid cron format
 */
export function isValidCron(cron) {
  if (typeof cron !== 'string') {
    return false;
  }
  
  const parts = cron.trim().split(/\s+/);
  if (parts.length !== 5) {
    return false;
  }
  
  const [minute, hour, dayOfMonth, month, dayOfWeek] = parts;
  
  // Basic validation patterns
  const patterns = {
    minute: /^(\*|(\d{1,2}(-\d{1,2})?)(\/\d+)?|(\*(\/\d+)?))$/,
    hour: /^(\*|(\d{1,2}(-\d{1,2})?)(\/\d+)?|(\*(\/\d+)?))$/,
    dayOfMonth: /^(\*|(\d{1,2}(-\d{1,2})?)(\/\d+)?|(\*(\/\d+)?))$/,
    month: /^(\*|(\d{1,2}(-\d{1,2})?)(\/\d+)?|(\*(\/\d+)?))$/,
    dayOfWeek: /^(\*|(\d{1}(-\d{1})?)(\/\d+)?|(\*(\/\d+)?))$/
  };
  
  return patterns.minute.test(minute) &&
         patterns.hour.test(hour) &&
         patterns.dayOfMonth.test(dayOfMonth) &&
         patterns.month.test(month) &&
         patterns.dayOfWeek.test(dayOfWeek);
}

/**
 * Validate timezone string (basic IANA timezone format)
 * @param {string} tz - Timezone string
 * @returns {boolean} True if valid timezone format
 */
export function isValidTimezone(tz) {
  if (typeof tz !== 'string') {
    return false;
  }
  
  // Allow UTC as a special case
  if (tz === 'UTC') {
    return true;
  }
  
  // Basic IANA timezone pattern
  const tzPattern = /^[A-Za-z]+\/[A-Za-z_]+(?:\/[A-Za-z_]+)?$/;
  return tzPattern.test(tz);
}

/**
 * Validate agent type
 * @param {string} agent - Agent type
 * @returns {boolean} True if valid agent
 */
export function isValidAgent(agent) {
  const validAgents = ['claude-code', 'codex', 'pi'];
  return validAgents.includes(agent);
}

/**
 * Validate sandbox type
 * @param {string} sandbox - Sandbox type
 * @returns {boolean} True if valid sandbox
 */
export function isValidSandbox(sandbox) {
  const validSandboxes = ['read-only', 'workspace-write', 'danger-full-access'];
  return validSandboxes.includes(sandbox);
}

/**
 * Validate permissions value
 * @param {string} permissions - Permissions value
 * @returns {boolean} True if valid permissions
 */
export function isValidPermissions(permissions) {
  return permissions === 'skip';
}

/**
 * Load fixture file content
 * @param {string} filename - Fixture filename
 * @returns {string} File content
 */
export function loadFixture(filename) {
  const fixturePath = join(__dirname, 'fixtures', filename);
  return readFileSync(fixturePath, 'utf-8');
}

/**
 * Validate complete heartbeat configuration
 * @param {object} frontmatter - Parsed frontmatter object
 * @returns {object} Validation result with isValid and errors
 */
export function validateHeartbeatConfig(frontmatter) {
  const errors = [];
  
  // Check for schedule (interval or cron, but not both)
  const hasInterval = frontmatter.hasOwnProperty('interval');
  const hasCron = frontmatter.hasOwnProperty('cron');
  
  if (!hasInterval && !hasCron) {
    errors.push('Missing schedule: must have either "interval" or "cron"');
  }
  
  if (hasInterval && hasCron) {
    errors.push('Invalid schedule: cannot have both "interval" and "cron"');
  }
  
  // Validate interval if present
  if (hasInterval && !isValidInterval(frontmatter.interval)) {
    errors.push(`Invalid interval format: "${frontmatter.interval}"`);
  }
  
  // Validate cron if present
  if (hasCron && !isValidCron(frontmatter.cron)) {
    errors.push(`Invalid cron expression: "${frontmatter.cron}"`);
  }
  
  // Validate timezone if present
  if (frontmatter.hasOwnProperty('tz') && !isValidTimezone(frontmatter.tz)) {
    errors.push(`Invalid timezone: "${frontmatter.tz}"`);
  }
  
  // Validate agent if present
  if (frontmatter.hasOwnProperty('agent') && !isValidAgent(frontmatter.agent)) {
    errors.push(`Invalid agent: "${frontmatter.agent}". Valid agents: claude-code, codex, pi`);
  }
  
  // Validate sandbox if present
  if (frontmatter.hasOwnProperty('sandbox') && !isValidSandbox(frontmatter.sandbox)) {
    errors.push(`Invalid sandbox: "${frontmatter.sandbox}". Valid sandboxes: read-only, workspace-write, danger-full-access`);
  }
  
  // Validate permissions if present
  if (frontmatter.hasOwnProperty('permissions') && !isValidPermissions(frontmatter.permissions)) {
    errors.push(`Invalid permissions: "${frontmatter.permissions}". Only "skip" is supported`);
  }
  
  // Validate maxTurns if present (should be positive integer)
  if (frontmatter.hasOwnProperty('maxTurns')) {
    const maxTurns = frontmatter.maxTurns;
    if (typeof maxTurns !== 'number' || maxTurns < 1 || !Number.isInteger(maxTurns)) {
      errors.push(`Invalid maxTurns: "${maxTurns}". Must be a positive integer`);
    }
  }
  
  // Validate timeout format if present
  if (frontmatter.hasOwnProperty('timeout') && !isValidInterval(frontmatter.timeout)) {
    errors.push(`Invalid timeout format: "${frontmatter.timeout}"`);
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
}

export default {
  parseFrontmatter,
  isValidInterval,
  isValidCron,
  isValidTimezone,
  isValidAgent,
  isValidSandbox,
  isValidPermissions,
  loadFixture,
  validateHeartbeatConfig
};
