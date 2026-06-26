/**
 * Base64 Toolkit - Encoding, decoding, and validation utilities
 * Provides comprehensive base64 operations for data handling
 */

/**
 * Encode string to base64
 * @param {string|Buffer} input - Data to encode
 * @returns {string} Base64 encoded string
 */
function encode(input) {
  const buffer = Buffer.isBuffer(input) ? input : Buffer.from(String(input), 'utf8');
  return buffer.toString('base64');
}

/**
 * Decode base64 to string
 * @param {string} input - Base64 encoded string
 * @param {string} encoding - Output encoding (default: utf8)
 * @returns {string} Decoded string
 */
function decode(input, encoding = 'utf8') {
  return Buffer.from(input, 'base64').toString(encoding);
}

/**
 * Decode base64 to buffer
 * @param {string} input - Base64 encoded string
 * @returns {Buffer} Decoded buffer
 */
function decodeToBuffer(input) {
  return Buffer.from(input, 'base64');
}

/**
 * Encode to URL-safe base64
 * @param {string|Buffer} input - Data to encode
 * @returns {string} URL-safe base64 string
 */
function encodeURLSafe(input) {
  return encode(input)
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
}

/**
 * Decode URL-safe base64
 * @param {string} input - URL-safe base64 string
 * @param {string} encoding - Output encoding (default: utf8)
 * @returns {string} Decoded string
 */
function decodeURLSafe(input, encoding = 'utf8') {
  // Restore standard base64 format
  let standard = input
    .replace(/-/g, '+')
    .replace(/_/g, '/');

  // Add padding if needed
  const padding = standard.length % 4;
  if (padding) {
    standard += '='.repeat(4 - padding);
  }

  return decode(standard, encoding);
}

/**
 * Check if string is valid base64
 * @param {string} input - String to validate
 * @returns {boolean}
 */
function isValid(input) {
  if (typeof input !== 'string') return false;
  if (input.length === 0) return true;

  // Check for valid base64 characters
  const base64Regex = /^[A-Za-z0-9+/]*={0,2}$/;
  if (!base64Regex.test(input)) return false;

  // Check padding
  const padding = input.length % 4;
  if (padding === 1) return false;

  // Try to decode
  try {
    Buffer.from(input, 'base64');
    return true;
  } catch {
    return false;
  }
}

/**
 * Check if string is URL-safe base64
 * @param {string} input - String to check
 * @returns {boolean}
 */
function isURLSafe(input) {
  if (typeof input !== 'string') return false;
  const urlSafeRegex = /^[A-Za-z0-9_-]*$/;
  return urlSafeRegex.test(input);
}

/**
 * Detect if string is base64 encoded
 * @param {string} input - String to check
 * @returns {object} Detection result
 */
function detect(input) {
  const result = {
    isBase64: false,
    isURLSafe: false,
    decoded: null,
    confidence: 0
  };

  if (typeof input !== 'string' || input.length === 0) {
    return result;
  }

  // Check standard base64
  if (isValid(input)) {
    result.isBase64 = true;
    result.confidence = 0.7;

    try {
      const decoded = decode(input);
      // Check if decoded looks like text
      if (/^[\x20-\x7E\s]*$/.test(decoded)) {
        result.decoded = decoded;
        result.confidence = 0.9;
      }
    } catch {
      // Ignore decode errors
    }
  }

  // Check URL-safe base64
  if (isURLSafe(input) && input.length > 0) {
    result.isURLSafe = true;

    try {
      const decoded = decodeURLSafe(input);
      if (/^[\x20-\x7E\s]*$/.test(decoded)) {
        result.decoded = decoded;
        result.confidence = Math.max(result.confidence, 0.85);
      }
    } catch {
      // Ignore decode errors
    }
  }

  return result;
}

/**
 * Encode file to base64
 * @param {string} filePath - Path to file
 * @returns {string} Base64 encoded content
 */
function encodeFile(filePath) {
  const fs = require('fs');
  const content = fs.readFileSync(filePath);
  return content.toString('base64');
}

/**
 * Decode base64 to file
 * @param {string} input - Base64 encoded content
 * @param {string} filePath - Output file path
 */
function decodeToFile(input, filePath) {
  const fs = require('fs');
  const buffer = decodeToBuffer(input);
  fs.writeFileSync(filePath, buffer);
}

/**
 * Encode object to base64 JSON
 * @param {object} obj - Object to encode
 * @returns {string} Base64 encoded JSON
 */
function encodeJSON(obj) {
  return encode(JSON.stringify(obj));
}

/**
 * Decode base64 JSON to object
 * @param {string} input - Base64 encoded JSON
 * @returns {object} Decoded object
 */
function decodeJSON(input) {
  return JSON.parse(decode(input));
}

/**
 * Convert base64 to data URI
 * @param {string} input - Base64 content
 * @param {string} mimeType - MIME type
 * @returns {string} Data URI
 */
function toDataURI(input, mimeType = 'application/octet-stream') {
  return `data:${mimeType};base64,${input}`;
}

/**
 * Parse data URI to base64 content
 * @param {string} dataURI - Data URI
 * @returns {object} Parsed result
 */
function fromDataURI(dataURI) {
  const match = dataURI.match(/^data:([^;,]+)?(?:;base64)?,(.*)$/);
  if (!match) {
    return { mimeType: null, data: null };
  }

  return {
    mimeType: match[1] || 'text/plain',
    data: match[2],
    isBase64: dataURI.includes(';base64')
  };
}

/**
 * CLI entry point
 */
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('Base64 Toolkit Demo');
    console.log('==================\n');

    const test = 'Hello, World! 你好世界 🌍';
    console.log(`Original: ${test}`);

    const encoded = encode(test);
    console.log(`Encoded: ${encoded}`);

    const decoded = decode(encoded);
    console.log(`Decoded: ${decoded}`);

    const urlSafe = encodeURLSafe(test);
    console.log(`URL-Safe: ${urlSafe}`);

    console.log(`\nValidation:`);
    console.log(`  isValid("${encoded}"): ${isValid(encoded)}`);
    console.log(`  isValid("invalid!@#"): ${isValid('invalid!@#')}`);

    console.log(`\nDetection:`);
    const detected = detect(encoded);
    console.log(`  detect("${encoded}"):`, detected);

    return;
  }

  const command = args[0];

  switch (command) {
    case 'encode':
    case 'enc':
      console.log(encode(args[1] || ''));
      break;

    case 'decode':
    case 'dec':
      console.log(decode(args[1] || ''));
      break;

    case 'validate':
    case 'valid':
      const valid = isValid(args[1] || '');
      console.log(valid ? 'Valid base64' : 'Invalid base64');
      process.exit(valid ? 0 : 1);

    case 'detect':
      const result = detect(args[1] || '');
      console.log(JSON.stringify(result, null, 2));
      break;

    case 'urlsafe':
      console.log(encodeURLSafe(args[1] || ''));
      break;

    default:
      // Treat as encode
      console.log(encode(command));
  }
}

module.exports = {
  encode,
  decode,
  decodeToBuffer,
  encodeURLSafe,
  decodeURLSafe,
  isValid,
  isURLSafe,
  detect,
  encodeFile,
  decodeToFile,
  encodeJSON,
  decodeJSON,
  toDataURI,
  fromDataURI,
  main
};

// Run main if called directly
if (require.main === module) {
  main().catch(err => {
    console.error('Error:', err.message);
    process.exit(1);
  });
}
