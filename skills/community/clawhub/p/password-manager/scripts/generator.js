/**
 * generator.js - Password Generation Module
 * 
 * Generates high-strength random passwords
 */

import { randomBytes, randomInt } from 'crypto';

// Character sets
const CHARSETS = {
  lowercase: 'abcdefghijklmnopqrstuvwxyz',
  uppercase: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
  numbers: '0123456789',
  symbols: '!@#$%^&*()_+-=[]{}|;:,.<>?'
};

// Ambiguous characters (optional exclusion)
const AMBIGUOUS = '0O1lI|';

/**
 * Generate random password
 * @param {Object} options - Generation options
 * @param {number} options.length - Password length (default: 32)
 * @param {boolean} options.includeUppercase - Include uppercase letters (default: true)
 * @param {boolean} options.includeNumbers - Include numbers (default: true)
 * @param {boolean} options.includeSymbols - Include special symbols (default: true)
 * @param {boolean} options.excludeAmbiguous - Exclude ambiguous characters (default: false)
 * @returns {string} - Generated password
 */
export function generatePassword(options = {}) {
  const {
    length = 32,
    includeUppercase = true,
    includeNumbers = true,
    includeSymbols = true,
    excludeAmbiguous = false
  } = options;
  
  // Build character pool
  let charset = CHARSETS.lowercase;
  
  if (includeUppercase) {
    charset += CHARSETS.uppercase;
  }
  
  if (includeNumbers) {
    charset += CHARSETS.numbers;
  }
  
  if (includeSymbols) {
    charset += CHARSETS.symbols;
  }
  
  // Exclude ambiguous characters
  if (excludeAmbiguous) {
    for (const char of AMBIGUOUS) {
      charset = charset.replace(char, '');
    }
  }
  
  if (charset.length < 10) {
    throw new Error('Character set too small, please add character types');
  }
  
  // Ensure at least one character of each type (using unbiased random)
  let password = '';
  const required = [];
  
  if (includeUppercase) {
    required.push(CHARSETS.uppercase[randomInt(0, CHARSETS.uppercase.length)]);
  }
  
  if (includeNumbers) {
    required.push(CHARSETS.numbers[randomInt(0, CHARSETS.numbers.length)]);
  }
  
  if (includeSymbols) {
    required.push(CHARSETS.symbols[randomInt(0, CHARSETS.symbols.length)]);
  }
  
  // Fill remaining length (using unbiased random)
  const remaining = length - required.length;
  for (let i = 0; i < remaining; i++) {
    const randomIndex = randomInt(0, charset.length);
    password += charset[randomIndex];
  }
  
  // Add required characters and shuffle
  password += required.join('');
  password = shuffleString(password);
  
  return password;
}

/**
 * Generate mnemonic password (memorable passphrase)
 * @param {number} wordCount - Number of words (default: 4)
 * @param {string[]} customWords - Custom word list (optional)
 * @returns {string} - Mnemonic password
 */
export function generateMnemonicPassword(wordCount = 4, customWords = null) {
  // Simplified word list (should use larger word list in production)
  const defaultWords = [
    'apple', 'blue', 'cloud', 'dream', 'eagle', 'fire', 'green', 'hill',
    'island', 'jade', 'king', 'lemon', 'moon', 'night', 'ocean', 'pearl',
    'queen', 'river', 'star', 'tree', 'umbrella', 'violet', 'water', 'xenon',
    'yellow', 'zebra', 'amber', 'berry', 'crystal', 'diamond', 'emerald', 'forest'
  ];
  
  const words = customWords || defaultWords;
  const result = [];
  
  for (let i = 0; i < wordCount; i++) {
    const index = randomInt(0, words.length);
    result.push(words[index]);
  }
  
  return result.join('-');
}

/**
 * Check password strength
 * @param {string} password - Password to check
 * @returns {Object} - Strength assessment result
 */
export function checkStrength(password) {
  let score = 0;
  const feedback = [];
  
  // Length scoring
  if (password.length >= 8) score += 1;
  if (password.length >= 12) score += 1;
  if (password.length >= 16) score += 1;
  if (password.length >= 24) score += 1;
  
  // Character type scoring
  if (/[a-z]/.test(password)) score += 1;
  if (/[A-Z]/.test(password)) score += 1;
  if (/[0-9]/.test(password)) score += 1;
  if (/[^a-zA-Z0-9]/.test(password)) score += 1;
  
  // Pattern detection (deductions)
  if (/^(.)\1+$/.test(password)) {
    score -= 3;
    feedback.push('Avoid using repeated characters');
  }
  
  if (/^(012|123|234|345|456|567|678|789|890)/.test(password)) {
    score -= 2;
    feedback.push('Avoid using sequential numbers');
  }
  
  if (/^(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)/i.test(password)) {
    score -= 2;
    feedback.push('Avoid using sequential letters');
  }
  
  if (/^(qwerty|asdfgh|zxcvbn)/i.test(password)) {
    score -= 3;
    feedback.push('Avoid using keyboard patterns');
  }
  
  // Common password detection
  const commonPasswords = ['password', '123456', '12345678', 'qwerty', 'abc123', 'letmein', 'welcome'];
  if (commonPasswords.some(p => password.toLowerCase().includes(p))) {
    score -= 3;
    feedback.push('Avoid using common passwords');
  }
  
  // Determine strength level
  let level, color, description;
  
  if (score <= 2) {
    level = 'weak';
    color = 'red';
    description = 'Weak';
    feedback.push('Consider increasing length and character types');
  } else if (score <= 4) {
    level = 'medium';
    color = 'yellow';
    description = 'Medium';
    feedback.push('Consider increasing length');
  } else if (score <= 6) {
    level = 'strong';
    color = 'green';
    description = 'Strong';
  } else {
    level = 'very-strong';
    color = 'dark-green';
    description = 'Very Strong';
  }
  
  return {
    score,
    level,
    color,
    description,
    feedback,
    length: password.length,
    hasLowercase: /[a-z]/.test(password),
    hasUppercase: /[A-Z]/.test(password),
    hasNumbers: /[0-9]/.test(password),
    hasSymbols: /[^a-zA-Z0-9]/.test(password)
  };
}

/**
 * Shuffle string (Fisher-Yates shuffle algorithm, using unbiased random)
 */
function shuffleString(str) {
  const arr = str.split('');
  for (let i = arr.length - 1; i > 0; i--) {
    const j = randomInt(0, i + 1);
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr.join('');
}

/**
 * Generate API Key format password
 * @param {string} prefix - Prefix (e.g., 'sk-', 'ghp_')
 * @param {number} length - Random part length
 * @returns {string} - API Key format password
 */
export function generateApiKey(prefix = '', length = 32) {
  const random = generatePassword({
    length,
    includeUppercase: true,
    includeNumbers: true,
    includeSymbols: false
  });
  
  return prefix + random;
}

export default {
  generatePassword,
  generateMnemonicPassword,
  checkStrength,
  generateApiKey,
  CHARSETS
};
