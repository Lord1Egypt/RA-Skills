/**
 * String Utils
 * Provides string manipulation and transformation operations
 */

/**
 * Convert string to camelCase
 */
function toCamelCase(str) {
  return str
    .replace(/[-_\s]+(.)?/g, (_, c) => c ? c.toUpperCase() : '')
    .replace(/^(.)/, c => c.toLowerCase());
}

/**
 * Convert string to PascalCase
 */
function toPascalCase(str) {
  return str
    .replace(/[-_\s]+(.)?/g, (_, c) => c ? c.toUpperCase() : '')
    .replace(/^(.)/, c => c.toUpperCase());
}

/**
 * Convert string to snake_case
 */
function toSnakeCase(str) {
  return str
    .replace(/([a-z])([A-Z])/g, '$1_$2')
    .replace(/[-\s]+/g, '_')
    .toLowerCase();
}

/**
 * Convert string to kebab-case
 */
function toKebabCase(str) {
  return str
    .replace(/([a-z])([A-Z])/g, '$1-$2')
    .replace(/[_\s]+/g, '-')
    .toLowerCase();
}

/**
 * Convert string to CONSTANT_CASE
 */
function toConstantCase(str) {
  return toSnakeCase(str).toUpperCase();
}

/**
 * Convert string to Title Case
 */
function toTitleCase(str) {
  return str
    .toLowerCase()
    .replace(/[-_\s]+(.)?/g, (_, c) => c ? ' ' + c.toUpperCase() : '')
    .replace(/^./, c => c.toUpperCase())
    .trim();
}

/**
 * Convert string to Sentence case
 */
function toSentenceCase(str) {
  return str
    .toLowerCase()
    .replace(/^[a-z]/, c => c.toUpperCase());
}

/**
 * Capitalize first letter
 */
function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Lowercase first letter
 */
function uncapitalize(str) {
  return str.charAt(0).toLowerCase() + str.slice(1);
}

/**
 * Swap case
 */
function swapCase(str) {
  return str.split('').map(c => {
    if (c === c.toUpperCase()) return c.toLowerCase();
    return c.toUpperCase();
  }).join('');
}

/**
 * Trim whitespace from both ends
 */
function trim(str, chars = null) {
  if (!chars) return str.trim();
  const pattern = new RegExp(`^[${chars}]+|[${chars}]+$`, 'g');
  return str.replace(pattern, '');
}

/**
 * Trim from left
 */
function trimLeft(str, chars = null) {
  if (!chars) return str.trimStart();
  const pattern = new RegExp(`^[${chars}]+`);
  return str.replace(pattern, '');
}

/**
 * Trim from right
 */
function trimRight(str, chars = null) {
  if (!chars) return str.trimEnd();
  const pattern = new RegExp(`[${chars}]+$`);
  return str.replace(pattern, '');
}

/**
 * Pad string on left
 */
function padLeft(str, length, char = ' ') {
  return str.padStart(length, char);
}

/**
 * Pad string on right
 */
function padRight(str, length, char = ' ') {
  return str.padEnd(length, char);
}

/**
 * Pad string on both sides
 */
function padBoth(str, length, char = ' ') {
  const padLength = Math.max(0, length - str.length);
  const padLeft = Math.floor(padLength / 2);
  const padRight = padLength - padLeft;
  return char.repeat(padLeft) + str + char.repeat(padRight);
}

/**
 * Truncate string with ellipsis
 */
function truncate(str, length, ellipsis = '...') {
  if (str.length <= length) return str;
  return str.slice(0, length - ellipsis.length) + ellipsis;
}

/**
 * Truncate in middle
 */
function truncateMiddle(str, length, ellipsis = '...') {
  if (str.length <= length) return str;
  const left = Math.ceil((length - ellipsis.length) / 2);
  const right = Math.floor((length - ellipsis.length) / 2);
  return str.slice(0, left) + ellipsis + str.slice(-right);
}

/**
 * Generate URL-friendly slug
 */
function slugify(str) {
  return str
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '')
    .replace(/[-\s]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

/**
 * Escape HTML entities
 */
function escapeHtml(str) {
  const entities = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
    '/': '&#x2F;',
    '`': '&#x60;',
    '=': '&#x3D;'
  };
  return str.replace(/[&<>"'`=/]/g, c => entities[c]);
}

/**
 * Unescape HTML entities
 */
function unescapeHtml(str) {
  const entities = {
    '&amp;': '&',
    '&lt;': '<',
    '&gt;': '>',
    '&quot;': '"',
    '&#39;': "'",
    '&#x27;': "'",
    '&#x2F;': '/',
    '&#x60;': '`',
    '&#x3D;': '='
  };
  return str.replace(/&(?:amp|lt|gt|quot|#39|#x27|#x2F|#x60|#x3D);/g, e => entities[e]);
}

/**
 * Escape regex special characters
 */
function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * URL encode
 */
function urlEncode(str) {
  return encodeURIComponent(str);
}

/**
 * URL decode
 */
function urlDecode(str) {
  return decodeURIComponent(str);
}

/**
 * Base64 encode
 */
function base64Encode(str) {
  return Buffer.from(str).toString('base64');
}

/**
 * Base64 decode
 */
function base64Decode(str) {
  return Buffer.from(str, 'base64').toString();
}

/**
 * Reverse string
 */
function reverse(str) {
  return str.split('').reverse().join('');
}

/**
 * Check if string starts with
 */
function startsWith(str, prefix) {
  return str.startsWith(prefix);
}

/**
 * Check if string ends with
 */
function endsWith(str, suffix) {
  return str.endsWith(suffix);
}

/**
 * Check if string contains substring
 */
function contains(str, substring) {
  return str.includes(substring);
}

/**
 * Count occurrences of substring
 */
function countOccurrences(str, substring) {
  if (!substring) return 0;
  return str.split(substring).length - 1;
}

/**
 * Repeat string n times
 */
function repeat(str, n) {
  return str.repeat(n);
}

/**
 * Split string into chunks
 */
function chunk(str, size) {
  const chunks = [];
  for (let i = 0; i < str.length; i += size) {
    chunks.push(str.slice(i, i + size));
  }
  return chunks;
}

/**
 * Remove non-printable characters
 */
function stripNonPrintable(str) {
  return str.replace(/[\x00-\x1F\x7F]/g, '');
}

/**
 * Remove extra whitespace
 */
function collapseWhitespace(str) {
  return str.replace(/\s+/g, ' ').trim();
}

/**
 * Template interpolation
 */
function template(str, data) {
  return str.replace(/\{\{(\w+)\}\}/g, (_, key) => {
    return data.hasOwnProperty(key) ? data[key] : '';
  });
}

/**
 * Levenshtein distance
 */
function levenshteinDistance(a, b) {
  const matrix = [];
  
  for (let i = 0; i <= b.length; i++) {
    matrix[i] = [i];
  }
  
  for (let j = 0; j <= a.length; j++) {
    matrix[0][j] = j;
  }
  
  for (let i = 1; i <= b.length; i++) {
    for (let j = 1; j <= a.length; j++) {
      if (b[i - 1] === a[j - 1]) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(
          matrix[i - 1][j - 1] + 1,
          matrix[i][j - 1] + 1,
          matrix[i - 1][j] + 1
        );
      }
    }
  }
  
  return matrix[b.length][a.length];
}

/**
 * String similarity (0-1)
 */
function similarity(a, b) {
  if (a === b) return 1;
  const maxLen = Math.max(a.length, b.length);
  if (maxLen === 0) return 1;
  return 1 - levenshteinDistance(a, b) / maxLen;
}

/**
 * Check if string is empty or whitespace
 */
function isEmpty(str) {
  return !str || str.trim().length === 0;
}

/**
 * Check if string is numeric
 */
function isNumeric(str) {
  return !isNaN(str) && !isNaN(parseFloat(str));
}

/**
 * Check if string is alphanumeric
 */
function isAlphanumeric(str) {
  return /^[a-zA-Z0-9]+$/.test(str);
}

/**
 * Check if string is valid email
 */
function isEmail(str) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(str);
}

/**
 * Check if string is valid URL
 */
function isUrl(str) {
  try {
    new URL(str);
    return true;
  } catch {
    return false;
  }
}

/**
 * Generate random string
 */
function random(length = 16, chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') {
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

/**
 * Word wrap
 */
function wordWrap(str, width = 80, newline = '\n') {
  const words = str.split(/\s+/);
  const lines = [];
  let currentLine = '';
  
  for (const word of words) {
    if (currentLine.length + word.length + 1 <= width) {
      currentLine += (currentLine ? ' ' : '') + word;
    } else {
      if (currentLine) lines.push(currentLine);
      currentLine = word;
    }
  }
  
  if (currentLine) lines.push(currentLine);
  return lines.join(newline);
}

/**
 * Main entry point for testing
 */
function main() {
  console.log('📝 String Utils Skill\n');
  
  // Test case conversion
  console.log('Testing case conversion:');
  console.log(`toCamelCase('hello world'): ${toCamelCase('hello world')}`);
  console.log(`toPascalCase('hello world'): ${toPascalCase('hello world')}`);
  console.log(`toSnakeCase('helloWorld'): ${toSnakeCase('helloWorld')}`);
  console.log(`toKebabCase('helloWorld'): ${toKebabCase('helloWorld')}`);
  
  // Test trimming and padding
  console.log('\nTesting trim and pad:');
  console.log(`trim('  hello  '): '${trim('  hello  ')}'`);
  console.log(`padLeft('5', 3, '0'): '${padLeft('5', 3, '0')}'`);
  console.log(`padBoth('hi', 6, '-'): '${padBoth('hi', 6, '-')}'`);
  
  // Test truncation
  console.log('\nTesting truncate:');
  console.log(`truncate('hello world', 8): '${truncate('hello world', 8)}'`);
  console.log(`truncateMiddle('hello world', 7): '${truncateMiddle('hello world', 7)}'`);
  
  // Test slugify
  console.log('\nTesting slugify:');
  console.log(`slugify('Hello World!'): '${slugify('Hello World!')}'`);
  
  // Test escape
  console.log('\nTesting escape:');
  console.log(`escapeHtml('<div>'): '${escapeHtml('<div>')}'`);
  
  // Test similarity
  console.log('\nTesting similarity:');
  console.log(`similarity('hello', 'hallo'): ${similarity('hello', 'hallo').toFixed(2)}`);
  
  // Test random
  console.log('\nTesting random:');
  console.log(`random(8): '${random(8)}'`);
  
  console.log('\n✅ string-utils loaded successfully');
}

module.exports = {
  toCamelCase,
  toPascalCase,
  toSnakeCase,
  toKebabCase,
  toConstantCase,
  toTitleCase,
  toSentenceCase,
  capitalize,
  uncapitalize,
  swapCase,
  trim,
  trimLeft,
  trimRight,
  padLeft,
  padRight,
  padBoth,
  truncate,
  truncateMiddle,
  slugify,
  escapeHtml,
  unescapeHtml,
  escapeRegex,
  urlEncode,
  urlDecode,
  base64Encode,
  base64Decode,
  reverse,
  startsWith,
  endsWith,
  contains,
  countOccurrences,
  repeat,
  chunk,
  stripNonPrintable,
  collapseWhitespace,
  template,
  levenshteinDistance,
  similarity,
  isEmpty,
  isNumeric,
  isAlphanumeric,
  isEmail,
  isUrl,
  random,
  wordWrap,
  main
};
