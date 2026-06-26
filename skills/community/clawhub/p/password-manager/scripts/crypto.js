/**
 * crypto.js - Crypto Module
 * 
 * Provides AES-256-GCM encryption/decryption and PBKDF2 key derivation
 */

import { createCipheriv, createDecipheriv, randomBytes, pbkdf2Sync, randomInt } from 'crypto';

const ALGORITHM = 'aes-256-gcm';
const KEY_LENGTH = 32; // 256 bits
const IV_LENGTH = 16;
const SALT_LENGTH = 16;
const PBKDF2_ITERATIONS = 100000;
const PBKDF2_DIGEST = 'sha256';
const CACHE_SALT_SUFFIX = '_cache_key_derivation';
const CACHE_SALT_FIXED = Buffer.from('openclaw_cache_salt_v1_fixed_16', 'utf8').subarray(0, 16);

/**
 * Derive encryption key from master password
 * @param {string} masterPassword - Master password
 * @param {Buffer} salt - Salt (optional, generated if not provided)
 * @returns {{ key: Buffer, salt: Buffer }} - Derived key and salt
 */
export function deriveKey(masterPassword, salt = null) {
  if (!salt) {
    salt = randomBytes(SALT_LENGTH);
  }
  
  const key = pbkdf2Sync(
    masterPassword,
    salt,
    PBKDF2_ITERATIONS,
    KEY_LENGTH,
    PBKDF2_DIGEST
  );
  
  return { key, salt };
}

/**
 * Encrypt data
 * @param {Buffer} key - Encryption key (32 bytes)
 * @param {Buffer|String} data - Data to encrypt
 * @returns {{ encrypted: Buffer, iv: Buffer, authTag: Buffer }} - Encrypted result
 */
export function encrypt(key, data) {
  const iv = randomBytes(IV_LENGTH);
  const dataBuffer = Buffer.isBuffer(data) ? data : Buffer.from(data, 'utf8');
  
  const cipher = createCipheriv(ALGORITHM, key, iv);
  
  let encrypted = cipher.update(dataBuffer);
  encrypted = Buffer.concat([encrypted, cipher.final()]);
  
  const authTag = cipher.getAuthTag();
  
  return { encrypted, iv, authTag };
}

/**
 * Decrypt data
 * @param {Buffer} key - Decryption key (32 bytes)
 * @param {Buffer} encrypted - Encrypted data
 * @param {Buffer} iv - Initialization vector
 * @param {Buffer} authTag - Authentication tag
 * @returns {Buffer} - Decrypted data
 */
export function decrypt(key, encrypted, iv, authTag) {
  const decipher = createDecipheriv(ALGORITHM, key, iv);
  decipher.setAuthTag(authTag);
  
  let decrypted = decipher.update(encrypted);
  decrypted = Buffer.concat([decrypted, decipher.final()]);
  
  return decrypted;
}

/**
 * Encrypt and pack (includes IV and authTag)
 * @param {Buffer} key - Encryption key
 * @param {Object} data - JSON object to encrypt
 * @returns {Buffer} - Packed binary data
 */
export function encryptAndPack(key, data, pbkdf2Salt = null) {
  const jsonString = JSON.stringify(data);
  const { encrypted, iv, authTag } = encrypt(key, jsonString);
  
  // Pack format: [pbkdf2Salt(16)][iv(16)][authTag(16)][encrypted(n)]
  // Use provided PBKDF2 salt (from vaultData.salt) or generate random
  const salt = pbkdf2Salt || randomBytes(SALT_LENGTH);
  const packed = Buffer.concat([
    salt,
    iv,
    authTag,
    encrypted
  ]);
  
  return packed;
}

/**
 * Unpack and decrypt
 * @param {Buffer} packed - Packed binary data
 * @param {Buffer|string} decryptionKey - Decryption key (Buffer or hex string)
 * @returns {Object} - Decrypted JSON object
 */
export function unpackAndDecrypt(packed, decryptionKey) {
  // Unpack format: [salt(16)][iv(16)][authTag(16)][encrypted(n)]
  const salt = packed.subarray(0, SALT_LENGTH);
  const iv = packed.subarray(SALT_LENGTH, SALT_LENGTH + IV_LENGTH);
  const authTag = packed.subarray(SALT_LENGTH + IV_LENGTH, SALT_LENGTH + IV_LENGTH + 16);
  const encrypted = packed.subarray(SALT_LENGTH + IV_LENGTH + 16);
  
  // Handle both Buffer and string types
  let key;
  if (Buffer.isBuffer(decryptionKey)) {
    // If Buffer is passed, use directly
    key = decryptionKey;
  } else if (typeof decryptionKey === 'string') {
    // If string is passed, parse as hex
    key = Buffer.from(decryptionKey, 'hex');
  } else {
    throw new Error('Invalid key type: expected Buffer or hex string');
  }
  
  const decrypted = decrypt(key, encrypted, iv, authTag);
  return JSON.parse(decrypted.toString('utf8'));
}

/**
 * Generate random bytes
 * @param {number} length - Byte length
 * @returns {string} - Hex string
 */
export function randomHex(length = 32) {
  return randomBytes(length).toString('hex');
}

/**
 * Verify if key is correct (via decryption test)
 * @param {Buffer} key - Key
 * @param {Buffer} testVector - Test vector
 * @param {Buffer} iv - IV
 * @param {Buffer} authTag - Authentication tag
 * @returns {boolean} - Whether key is valid
 */
export function verifyKey(key, testVector, iv, authTag) {
  try {
    decrypt(key, testVector, iv, authTag);
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * Derive cache encryption key from master password (for encrypting cache file)
 * @param {string} masterPassword - Master password
 * @param {Buffer} salt - Salt (optional, generated if not provided)
 * @returns {{ key: Buffer, salt: Buffer }} - Derived key and salt
 */
export function deriveCacheKey(masterPassword, salt = null) {
  const saltedPassword = masterPassword + CACHE_SALT_SUFFIX;
  // Use fixed salt for consistent cache key derivation
  return deriveKey(saltedPassword, salt || CACHE_SALT_FIXED);
}

/**
 * Securely clear Buffer content (prevent memory dump attacks)
 * @param {Buffer} buffer - Buffer to clear
 */
export function secureWipe(buffer) {
  if (Buffer.isBuffer(buffer)) {
    buffer.fill(0);
  }
}

/**
 * Generate unbiased random index (eliminate modulo bias)
 * @param {number} max - Maximum value (exclusive)
 * @returns {number} - Random integer
 */
export function randomIntUnbiased(max) {
  if (max <= 0) {
    throw new Error('max must be greater than 0');
  }
  return randomInt(0, max);
}

export default {
  deriveKey,
  deriveCacheKey,
  encrypt,
  decrypt,
  encryptAndPack,
  unpackAndDecrypt,
  randomHex,
  verifyKey,
  secureWipe,
  randomIntUnbiased,
  constants: {
    ALGORITHM,
    KEY_LENGTH,
    IV_LENGTH,
    SALT_LENGTH,
    PBKDF2_ITERATIONS,
    CACHE_SALT_SUFFIX
  }
};
