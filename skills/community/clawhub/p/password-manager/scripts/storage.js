import { readFileSync, writeFileSync, existsSync, mkdirSync, unlinkSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import crypto from './crypto.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Default paths
const DEFAULT_DATA_DIR = join(__dirname, '..', 'data');
const DEFAULT_CACHE_DIR = join(__dirname, '..', '.cache');
const VAULT_FILE = join(DEFAULT_DATA_DIR, 'vault.enc');
const CACHE_FILE = join(DEFAULT_CACHE_DIR, 'key.enc');
const CONFIG_FILE = join(__dirname, '..', 'config.json');

// Memory cache (avoid repeated decryption)
let vaultCache = null;
let vaultCacheKeyHex = null;

// Input validation constants
const MAX_INPUT_LENGTH = 1024;

// Default configuration
const DEFAULT_CONFIG = {
  cacheTimeout: 172800,          // 48 hours (seconds)
  maxHistoryVersions: 3,         // Number of historical versions to retain
  auditLogLevel: 'all',          // all/sensitive/none
  autoDetect: {
    enabled: true,
    sensitivityThreshold: 'medium',
    askBeforeSave: true
  },
  requireConfirm: {
    delete: true,
    deleteAll: true,
    export: true,
    backup: true,
    restore: true
  },
  generator: {
    defaultLength: 32,
    includeUppercase: true,
    includeNumbers: true,
    includeSymbols: true
  }
};

/**
 * Ensure directories exist
 */
function ensureDirectories() {
  [DEFAULT_DATA_DIR, DEFAULT_CACHE_DIR].forEach(dir => {
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }
  });
}

/**
 * Sanitize and validate user input
 * @param {string} input - User input
 * @param {number} maxLength - Maximum length
 * @returns {string} - Sanitized input
 */
export function sanitizeInput(input, maxLength = MAX_INPUT_LENGTH) {
  if (!input) {
    return '';
  }
  
  // Convert to string
  let result = String(input);
  
  // Limit length
  if (result.length > maxLength) {
    result = result.substring(0, maxLength);
  }
  
  // Remove control characters (except newline and tab)
  result = result.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '');
  
  return result;
}

/**
 * Load configuration
 */
export function loadConfig() {
  if (existsSync(CONFIG_FILE)) {
    const saved = JSON.parse(readFileSync(CONFIG_FILE, 'utf8'));
    return { ...DEFAULT_CONFIG, ...saved };
  }
  return DEFAULT_CONFIG;
}

/**
 * Save configuration
 */
export function saveConfig(config) {
  ensureDirectories();
  writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2), 'utf8');
}

/**
 * Get vault status
 */
export function getVaultStatus() {
  const config = loadConfig();
  
  if (!existsSync(VAULT_FILE)) {
    return { exists: false, initialized: false };
  }
  
  if (!existsSync(CACHE_FILE)) {
    return { exists: true, locked: true, initialized: true };
  }
  
  // Check if cache is expired
  try {
    const cachePacked = readFileSync(CACHE_FILE);
    const { key: dummyKey } = crypto.deriveCacheKey("dummy"); // We need to decrypt with master password
    // Actually, we can't check expiration without master password
    // So just return locked if cache exists but we can't verify
    return { exists: true, locked: true, initialized: true };
  } catch (e) {
    return { exists: true, locked: true, initialized: true, error: true };
  }
}

/**
 * Initialize vault
 */
export function initializeVault(masterPassword) {
  ensureDirectories();
  
  const { key, salt } = crypto.deriveKey(masterPassword);
  
  const vaultData = {
    version: 1,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    salt: salt.toString('hex'),
    entries: [],
    history: []
  };
  
  // Encrypt and save (pass PBKDF2 salt so it's embedded in vault file)
  const packed = crypto.encryptAndPack(key, vaultData, salt);
  writeFileSync(VAULT_FILE, packed);
  
  // Cache key (encrypted version using master password)
  cacheKey(key, masterPassword);
  
  // Clear key from memory
  crypto.secureWipe(key);
  
  return { success: true, message: 'Vault initialized' };
}

/**
 * Cache decryption key (encrypted version)
 * @param {Buffer} key - Derived encryption key
 * @param {string} masterPassword - Master password (used to derive cache encryption key)
 */
function cacheKey(key, masterPassword) {
  const config = loadConfig();
  
  // Derive cache encryption key from master password
  const { key: cacheEncryptionKey } = crypto.deriveCacheKey(masterPassword);
  
  // Encrypt key data
  const keyData = {
    key: key.toString('hex'),
    createdAt: new Date().toISOString(),
    lastUsedAt: new Date().toISOString(),
    expiresAt: new Date(Date.now() + config.cacheTimeout * 1000).toISOString()
  };
  
  const encrypted = crypto.encryptAndPack(cacheEncryptionKey, keyData);
  writeFileSync(CACHE_FILE, encrypted, 'utf8');
}

/**
 * Get decryption key
 */
export function getDecryptionKey(masterPassword = null) {
  if (!existsSync(CACHE_FILE)) {
    return { locked: true, reason: 'no_cache' };
  }
  
  // If no master password provided and cache exists, try to decrypt cache
  if (!masterPassword) {
    try {
      // Need master password to decrypt cache, so return locked when no password
      return { locked: true, reason: 'need_password_for_cache' };
    } catch (e) {
      return { locked: true, reason: 'read_cache_failed' };
    }
  }
  
  // If master password provided, verify and decrypt cache
  try {
    // Read salt from vault and verify password
    if (existsSync(VAULT_FILE)) {
      try {
        const vaultPacked = readFileSync(VAULT_FILE);
        // Extract salt from vault file (first 16 bytes)
        const vaultSalt = vaultPacked.subarray(0, 16);
        // Derive key with vault salt and verify decryption
        const { key: testKey } = crypto.deriveKey(masterPassword, vaultSalt);
        const vaultData = crypto.unpackAndDecrypt(vaultPacked, testKey);
        // Decryption successful, password is correct
      } catch (e) {
        // Decryption failed, wrong password
        return { locked: true, reason: 'wrong_password' };
      }
    }
    
    // Decrypt cache with master password
    const { key: cacheEncryptionKey } = crypto.deriveCacheKey(masterPassword);
    const cachePacked = readFileSync(CACHE_FILE);
    const cacheData = crypto.unpackAndDecrypt(cachePacked, cacheEncryptionKey);
    
    const now = Date.now();
    const expiresAt = new Date(cacheData.expiresAt).getTime();
    
    if (now > expiresAt) {
      // Cache expired, clear cache file
      unlinkSync(CACHE_FILE);
      return { locked: true, reason: 'expired', lastUsed: cacheData.lastUsedAt };
    }
    
    // Update cache time and re-encrypt save
    cacheData.lastUsedAt = new Date().toISOString();
    cacheData.expiresAt = new Date(now + loadConfig().cacheTimeout * 1000).toISOString();
    
    const { key: newCacheEncryptionKey } = crypto.deriveCacheKey(masterPassword);
    const newCachePacked = crypto.encryptAndPack(newCacheEncryptionKey, cacheData);
    writeFileSync(CACHE_FILE, newCachePacked, 'utf8');
    
    // Get actual key from cache
    const key = Buffer.from(cacheData.key, 'hex');
    
    return {
      locked: false,
      key,
      expiresAt: cacheData.expiresAt
    };
  } catch (e) {
    return { locked: true, reason: 'wrong_password' };
  }
}

/**
 * Load and decrypt vault (with caching)
 * @param {Buffer} decryptionKey - Decryption key
 */
export function loadVault(decryptionKey) {
  const keyHex = decryptionKey.toString('hex');
  
  // Check cache
  if (vaultCache && vaultCacheKeyHex === keyHex) {
    return vaultCache;
  }
  
  const packed = readFileSync(VAULT_FILE);
  const vaultData = crypto.unpackAndDecrypt(packed, decryptionKey);
  
  // Update cache
  vaultCache = vaultData;
  vaultCacheKeyHex = keyHex;
  
  return vaultData;
}

/**
 * Clear vault cache (use when security requires)
 */
export function clearVaultCache() {
  vaultCache = null;
  vaultCacheKeyHex = null;
}

/**
 * Save vault (create version history)
 */
export function saveVault(vaultData, decryptionKey) {
  const config = loadConfig();
  
  // Save current version to history
  if (existsSync(VAULT_FILE)) {
    const timestamp = Date.now();
    const historyFile = join(DEFAULT_DATA_DIR, `vault.${timestamp}.enc`);
    
    // Copy old file to history
    const oldPacked = readFileSync(VAULT_FILE);
    writeFileSync(historyFile, oldPacked);
    
    vaultData.history = vaultData.history || [];
    vaultData.history.push({
      version: vaultData.history.length + 1,
      timestamp: new Date().toISOString(),
      file: historyFile
    });
    
    // Keep only the most recent N versions
    while (vaultData.history.length > config.maxHistoryVersions) {
      const old = vaultData.history.shift();
      if (existsSync(old.file)) {
        unlinkSync(old.file);
      }
    }
  }
  
  vaultData.updatedAt = new Date().toISOString();
  
  // Convert hex salt back to buffer for consistent encryption
  const saltBuffer = Buffer.from(vaultData.salt, 'hex');
  
  // Encrypt and save with the original salt
  const packed = crypto.encryptAndPack(decryptionKey, vaultData, saltBuffer);
  writeFileSync(VAULT_FILE, packed);
  
  // Update cache
  vaultCache = vaultData;
  vaultCacheKeyHex = decryptionKey.toString('hex');
  
  // Verify write
  try {
    const verifyData = crypto.unpackAndDecrypt(packed, decryptionKey);
    return { success: true, entries: verifyData.entries ? verifyData.entries.length : 0 };
  } catch (e) {
    return { success: false, error: "Write verification failed" };
  }
}

/**
 * Rebuild cache from master password
 * @param {string} masterPassword - Master password
 * @returns {Object} - Result object
 */
export function rebuildCache(masterPassword) {
  try {
    // Verify master password by attempting to decrypt vault
    if (!existsSync(VAULT_FILE)) {
      return { success: false, error: 'Vault not initialized' };
    }
    
    const vaultPacked = readFileSync(VAULT_FILE);
    const vaultSalt = vaultPacked.subarray(0, 16);
    const { key: decryptionKey } = crypto.deriveKey(masterPassword, vaultSalt);
    
    // Try to decrypt vault to verify password
    const vaultData = crypto.unpackAndDecrypt(vaultPacked, decryptionKey);
    
    // Password is correct, create cache
    cacheKey(decryptionKey, masterPassword);
    
    // Create a copy of the key before wiping
    const keyCopy = Buffer.from(decryptionKey);
    
    // Clear original key from memory
    crypto.secureWipe(decryptionKey);
    
    return { success: true, key: keyCopy };
  } catch (e) {
    return { success: false, error: 'Invalid master password or vault corrupted' };
  }
}

/**
 * Change master password
 */
export function changeMasterPassword(oldPassword, newPassword) {
  try {
    // Get current decryption key
    const oldResult = getDecryptionKey(oldPassword);
    if (oldResult.locked) {
      return { success: false, error: 'Invalid old password' };
    }
    
    // Load vault with old key
    const vault = loadVault(oldResult.key);
    
    // Derive new key with new password
    const { key: newKey, salt: newSalt } = crypto.deriveKey(newPassword);
    
    // Update vault salt
    vault.salt = newSalt.toString('hex');
    vault.updatedAt = new Date().toISOString();
    
    // Save vault with new key
    const packed = crypto.encryptAndPack(newKey, vault, newSalt);
    writeFileSync(VAULT_FILE, packed);
    
    // Update cache with new password
    cacheKey(newKey, newPassword);
    
    // Clear keys from memory
    crypto.secureWipe(oldResult.key);
    crypto.secureWipe(newKey);
    
    return { success: true, message: 'Master password changed successfully' };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

/**
 * Lock vault (clear cache)
 */
export function lockVault() {
  if (existsSync(CACHE_FILE)) {
    unlinkSync(CACHE_FILE);
  }
  return { locked: true };
}

export default {
  loadConfig,
  saveConfig,
  getVaultStatus,
  initializeVault,
  getDecryptionKey,
  loadVault,
  saveVault,
  rebuildCache,
  changeMasterPassword,
  lockVault,
  paths: {
    VAULT_FILE,
    CACHE_FILE,
    CONFIG_FILE
  }
};