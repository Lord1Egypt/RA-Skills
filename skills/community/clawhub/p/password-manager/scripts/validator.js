/**
 * validator.js - Validation Module
 * 
 * Validates password strength, entry data, etc.
 */

import { checkStrength } from './generator.js';

/**
 * Validate entry data
 * @param {Object} entry - Entry data
 * @returns {Object} - Validation result
 */
export function validateEntry(entry) {
  const errors = [];
  const warnings = [];
  
  // Required fields
  if (!entry.name || entry.name.trim() === '') {
    errors.push('Entry name cannot be empty');
  }
  
  if (!entry.type) {
    errors.push('Entry type cannot be empty');
  } else if (!['password', 'token', 'api_key', 'secret'].includes(entry.type)) {
    errors.push(`Invalid entry type: ${entry.type}`);
  }
  
  // Name length
  if (entry.name && entry.name.length > 100) {
    errors.push('Entry name too long (max 100 characters)');
  }
  
  // Password strength (if password type)
  if (entry.type === 'password' && entry.password) {
    const strength = checkStrength(entry.password);
    if (strength.level === 'weak') {
      warnings.push(`Password strength is weak: ${strength.description}`);
      warnings.push(...strength.feedback);
    }
  }
  
  // Tag validation
  if (entry.tags) {
    if (!Array.isArray(entry.tags)) {
      errors.push('Tags must be an array');
    } else if (entry.tags.length > 20) {
      warnings.push('Too many tags (recommended: max 20)');
    }
    
    entry.tags.forEach((tag, i) => {
      if (typeof tag !== 'string') {
        errors.push(`Tag ${i} must be a string`);
      } else if (tag.length > 50) {
        warnings.push(`Tag "${tag}" is too long`);
      }
    });
  }
  
  // Notes length
  if (entry.notes && entry.notes.length > 1000) {
    warnings.push('Notes too long (recommended: max 1000 characters)');
  }
  
  return {
    valid: errors.length === 0,
    errors,
    warnings
  };
}

/**
 * Validate master password strength
 * @param {string} password - Master password
 * @returns {Object} - Validation result
 */
export function validateMasterPassword(password) {
  const errors = [];
  const suggestions = [];
  
  if (!password || password.length === 0) {
    errors.push('Master password cannot be empty');
    return { valid: false, errors, suggestions };
  }
  
  if (password.length < 8) {
    errors.push('Master password must be at least 8 characters');
  }
  
  if (password.length < 12) {
    suggestions.push('Recommended to use 12+ character master password');
  }
  
  const strength = checkStrength(password);
  if (strength.level === 'weak') {
    errors.push('Master password strength is insufficient');
    suggestions.push(...strength.feedback);
  } else if (strength.level === 'medium') {
    suggestions.push('Master password strength is medium, consider increasing length and character types');
  }
  
  // Common password detection
  const commonPatterns = ['password', '123456', 'qwerty', 'admin', 'welcome'];
  const lowerPassword = password.toLowerCase();
  for (const pattern of commonPatterns) {
    if (lowerPassword.includes(pattern)) {
      errors.push('Master password contains common patterns, not secure');
      break;
    }
  }
  
  return {
    valid: errors.length === 0,
    errors,
    suggestions,
    strength: strength.description
  };
}

/**
 * Validate search query
 * @param {string} query - Search query
 * @returns {Object} - Validation result
 */
export function validateSearchQuery(query) {
  const errors = [];
  
  if (!query || query.trim() === '') {
    errors.push('Search keyword cannot be empty');
  }
  
  if (query.length > 100) {
    errors.push('Search keyword too long');
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}

/**
 * Validate backup path
 * @param {string} path - Backup path
 * @returns {Object} - Validation result
 */
export function validateBackupPath(path) {
  const errors = [];
  
  if (!path || path.trim() === '') {
    errors.push('Backup path cannot be empty');
  }
  
  if (!path.endsWith('.enc')) {
    errors.push('Backup file should end with .enc');
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}

export default {
  validateEntry,
  validateMasterPassword,
  validateSearchQuery,
  validateBackupPath
};
