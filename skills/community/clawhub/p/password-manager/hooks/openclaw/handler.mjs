/**
 * handler.mjs - OpenClaw Hook Handler
 * 
 * Provides password-manager integration interface with OpenClaw
 */

import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Import core modules
import storage, { sanitizeInput } from '../../scripts/storage.js';
import cryptoLib from '../../scripts/crypto.js';
import generator from '../../scripts/generator.js';
import validator from '../../scripts/validator.js';
import detector from '../../scripts/detector.js';

/**
 * Tool definitions
 */
export const tools = [
  {
    name: 'password_manager_add',
    description: 'Add entry to password manager',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string', description: 'Entry name' },
        type: { 
          type: 'string', 
          enum: ['password', 'token', 'api_key', 'secret'],
          description: 'Entry type'
        },
        username: { type: 'string', description: 'Username (optional)' },
        password: { type: 'string', description: 'Password/value (auto-generate if not provided)' },
        tags: { 
          type: 'array', 
          items: { type: 'string' },
          description: 'Tag list'
        },
        notes: { type: 'string', description: 'Notes (optional)' }
      },
      required: ['name', 'type']
    }
  },
  {
    name: 'password_manager_get',
    description: 'Get entry content',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string', description: 'Entry name' },
        showPassword: { 
          type: 'boolean', 
          description: 'Whether to show password in plaintext',
          default: true
        }
      },
      required: ['name']
    }
  },
  {
    name: 'password_manager_update',
    description: 'Update entry',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string', description: 'Entry name' },
        password: { type: 'string', description: 'New password' },
        username: { type: 'string', description: 'New username' },
        tags: { type: 'array', items: { type: 'string' } },
        notes: { type: 'string', description: 'New notes' }
      },
      required: ['name']
    }
  },
  {
    name: 'password_manager_delete',
    description: 'Delete entry (sensitive operation)',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string', description: 'Entry name' },
        confirmed: { 
          type: 'boolean', 
          description: 'Whether confirmed (requires user to re-enter master password)'
        }
      },
      required: ['name', 'confirmed']
    }
  },
  {
    name: 'password_manager_search',
    description: 'Search entries',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Search keyword' },
        type: { type: 'string', description: 'Entry type filter' },
        tag: { type: 'string', description: 'Tag filter' }
      }
    }
  },
  {
    name: 'password_manager_list',
    description: 'List all entries (metadata only)',
    inputSchema: {
      type: 'object',
      properties: {
        type: { type: 'string', description: 'Entry type filter' }
      }
    }
  },
  {
    name: 'password_manager_generate',
    description: 'Generate random password',
    inputSchema: {
      type: 'object',
      properties: {
        length: { type: 'number', description: 'Password length', default: 32 },
        includeUppercase: { type: 'boolean', default: true },
        includeNumbers: { type: 'boolean', default: true },
        includeSymbols: { type: 'boolean', default: true }
      }
    }
  },
  {
    name: 'password_manager_check_strength',
    description: 'Check password strength',
    inputSchema: {
      type: 'object',
      properties: {
        password: { type: 'string', description: 'Password to check' }
      },
      required: ['password']
    }
  },
  {
    name: 'password_manager_status',
    description: 'View password manager status',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  },
  {
    name: 'password_manager_detect',
    description: 'Detect sensitive information in text',
    inputSchema: {
      type: 'object',
      properties: {
        text: { type: 'string', description: 'Text to detect' }
      },
      required: ['text']
    }
  }
];

/**
 * Tool handler
 */
export async function handleToolCall(toolName, params) {
  try {
    switch (toolName) {
      case 'password_manager_add':
        return await toolAdd(params);
      case 'password_manager_get':
        return await toolGet(params);
      case 'password_manager_update':
        return await toolUpdate(params);
      case 'password_manager_delete':
        return await toolDelete(params);
      case 'password_manager_search':
        return await toolSearch(params);
      case 'password_manager_list':
        return await toolList(params);
      case 'password_manager_generate':
        return await toolGenerate(params);
      case 'password_manager_check_strength':
        return await toolCheckStrength(params);
      case 'password_manager_status':
        return await toolStatus(params);
      case 'password_manager_detect':
        return await toolDetect(params);
      default:
        return { error: `Unknown tool: ${toolName}` };
    }
  } catch (error) {
    return { error: error.message, stack: error.stack };
  }
}

/**
 * Add entry
 */
async function toolAdd(params) {
  const { name, type, username, password, tags, notes } = params;
  
  // Input validation and sanitization
  const sanitizedName = sanitizeInput(name, 100);
  const sanitizedUsername = username ? sanitizeInput(username, 200) : '';
  const sanitizedPassword = password ? sanitizeInput(password, 1024) : '';
  const sanitizedTags = tags ? tags.map(t => sanitizeInput(t, 50)) : [];
  const sanitizedNotes = notes ? sanitizeInput(notes, 1000) : '';
  
  // Check status
  const status = storage.getVaultStatus();
  
  if (!status.initialized) {
    return {
      requiresAuth: true,
      message: '🔒 Password manager not initialized, please run `password-manager init` first',
      action: 'init'
    };
  }
  
  if (status.locked) {
    return {
      requiresAuth: true,
      message: '🔒 Password manager is locked, please provide master password to unlock',
      action: 'unlock'
    };
  }
  
  // Get key
  const auth = storage.getDecryptionKey();
  if (auth.locked) {
    return {
      requiresAuth: true,
      message: '🔒 Password manager is locked or expired',
      action: 'unlock'
    };
  }
  
  // Load vault
  const vault = storage.loadVault(auth.key);
  
  // Generate password (if not provided)
  const finalPassword = sanitizedPassword || generator.generatePassword();
  
  const entry = {
    id: cryptoLib.randomHex(16),
    name: sanitizedName,
    type,
    username: sanitizedUsername,
    password: finalPassword,
    tags: sanitizedTags,
    notes: sanitizedNotes,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };
  
  // Validate
  const validation = validator.validateEntry(entry);
  if (!validation.valid) {
    return { error: validation.errors.join(', ') };
  }
  
  vault.entries.push(entry);
  storage.saveVault(vault, auth.key);
  
  return {
    success: true,
    message: `✅ Saved: ${sanitizedName}`,
    entry: {
      name: entry.name,
      type: entry.type,
      tags: entry.tags,
      passwordGenerated: !sanitizedPassword
    }
  };
}

/**
 * Get entry
 */
async function toolGet(params) {
  const { name, showPassword = true } = params;
  
  // Input sanitization
  const sanitizedName = sanitizeInput(name, 100);
  
  const status = storage.getVaultStatus();
  
  if (status.locked) {
    return {
      requiresAuth: true,
      message: '🔒 Password manager is locked',
      action: 'unlock'
    };
  }
  
  const auth = storage.getDecryptionKey();
  if (auth.locked) {
    return { requiresAuth: true, message: '🔒 Requires unlock' };
  }
  
  const vault = storage.loadVault(auth.key);
  const entry = vault.entries.find(e => e.name === sanitizedName);
  
  if (!entry) {
    return { error: `Entry not found: ${sanitizedName}` };
  }
  
  return {
    success: true,
    entry: {
      name: entry.name,
      type: entry.type,
      username: entry.username,
      password: showPassword ? entry.password : '********',
      tags: entry.tags,
      notes: entry.notes,
      createdAt: entry.createdAt,
      updatedAt: entry.updatedAt
    }
  };
}

/**
 * Update entry
 */
async function toolUpdate(params) {
  const { name, password, username, tags, notes } = params;
  
  // Input sanitization
  const sanitizedName = sanitizeInput(name, 100);
  const sanitizedPassword = password ? sanitizeInput(password, 1024) : null;
  const sanitizedUsername = username ? sanitizeInput(username, 200) : null;
  const sanitizedTags = tags ? tags.map(t => sanitizeInput(t, 50)) : null;
  const sanitizedNotes = notes ? sanitizeInput(notes, 1000) : null;
  
  const status = storage.getVaultStatus();
  if (status.locked) {
    return { requiresAuth: true, message: '🔒 Requires unlock' };
  }
  
  const auth = storage.getDecryptionKey();
  const vault = storage.loadVault(auth.key);
  
  const entry = vault.entries.find(e => e.name === sanitizedName);
  if (!entry) {
    return { error: `Entry not found: ${sanitizedName}` };
  }
  
  if (sanitizedPassword) entry.password = sanitizedPassword;
  if (sanitizedUsername) entry.username = sanitizedUsername;
  if (sanitizedTags) entry.tags = sanitizedTags;
  if (sanitizedNotes) entry.notes = sanitizedNotes;
  entry.updatedAt = new Date().toISOString();
  
  storage.saveVault(vault, auth.key);
  
  return { success: true, message: `✅ Updated: ${sanitizedName}` };
}

/**
 * Delete entry
 */
async function toolDelete(params) {
  const { name, confirmed } = params;
  
  // Input sanitization
  const sanitizedName = sanitizeInput(name, 100);
  
  if (!confirmed) {
    return {
      requiresAuth: true,
      message: `⚠️  Confirm deletion of "${sanitizedName}"? This action cannot be undone!`,
      action: 'confirm_delete',
      params: { name: sanitizedName }
    };
  }
  
  const status = storage.getVaultStatus();
  if (status.locked) {
    return { requiresAuth: true, message: '🔒 Requires unlock' };
  }
  
  const auth = storage.getDecryptionKey();
  const vault = storage.loadVault(auth.key);
  
  const index = vault.entries.findIndex(e => e.name === sanitizedName);
  if (index === -1) {
    return { error: `Entry not found: ${sanitizedName}` };
  }
  
  vault.entries.splice(index, 1);
  storage.saveVault(vault, auth.key);
  
  return { success: true, message: `✅ Deleted: ${sanitizedName}` };
}

/**
 * Search entries
 */
async function toolSearch(params) {
  const { query, type, tag } = params;
  
  // Input sanitization
  const sanitizedQuery = query ? sanitizeInput(query, 100) : null;
  const sanitizedType = type ? sanitizeInput(type, 20) : null;
  const sanitizedTag = tag ? sanitizeInput(tag, 50) : null;
  
  const status = storage.getVaultStatus();
  if (status.locked) {
    return { requiresAuth: true, message: '🔒 Requires unlock' };
  }
  
  const auth = storage.getDecryptionKey();
  const vault = storage.loadVault(auth.key);
  
  let results = vault.entries;
  
  if (sanitizedQuery) {
    const q = sanitizedQuery.toLowerCase();
    results = results.filter(e => 
      e.name.toLowerCase().includes(q) ||
      e.tags.some(t => t.toLowerCase().includes(q))
    );
  }
  
  if (sanitizedType) {
    results = results.filter(e => e.type === sanitizedType);
  }
  
  if (sanitizedTag) {
    results = results.filter(e => e.tags.includes(sanitizedTag));
  }
  
  return {
    success: true,
    count: results.length,
    entries: results.map(e => ({
      name: e.name,
      type: e.type,
      tags: e.tags
    }))
  };
}

/**
 * List entries
 */
async function toolList(params) {
  const { type } = params;
  
  // Input sanitization
  const sanitizedType = type ? sanitizeInput(type, 20) : null;
  
  const status = storage.getVaultStatus();
  if (status.locked) {
    return { requiresAuth: true, message: '🔒 Requires unlock' };
  }
  
  const auth = storage.getDecryptionKey();
  const vault = storage.loadVault(auth.key);
  
  let entries = vault.entries;
  if (sanitizedType) {
    entries = entries.filter(e => e.type === sanitizedType);
  }
  
  return {
    success: true,
    count: entries.length,
    entries: entries.map(e => ({
      name: e.name,
      type: e.type,
      tags: e.tags
    }))
  };
}

/**
 * Generate password
 */
async function toolGenerate(params) {
  const {
    length = 32,
    includeUppercase = true,
    includeNumbers = true,
    includeSymbols = true
  } = params;
  
  const password = generator.generatePassword({
    length,
    includeUppercase,
    includeNumbers,
    includeSymbols
  });
  
  const strength = generator.checkStrength(password);
  
  return {
    success: true,
    password,
    length,
    strength: strength.description
  };
}

/**
 * Check password strength
 */
async function toolCheckStrength(params) {
  const { password } = params;
  
  const strength = generator.checkStrength(password);
  
  return {
    success: true,
    strength
  };
}

/**
 * View status
 */
async function toolStatus(params) {
  const status = storage.getVaultStatus();
  
  return {
    success: true,
    status
  };
}

/**
 * Detect sensitive information
 */
async function toolDetect(params) {
  const { text } = params;
  const config = storage.loadConfig();
  
  const detections = detector.detect(text, config.autoDetect);
  
  return {
    success: true,
    count: detections.length,
    detections: detections.map(d => ({
      type: d.type,
      name: d.name,
      sensitivity: d.sensitivity,
      suggestedEntryName: d.suggestedEntryName,
      suggestedEntryType: detector.suggestEntryType(d.type)
    }))
  };
}

/**
 * User message hook - detect sensitive information
 */
export async function onUserMessage(message) {
  const config = storage.loadConfig();
  
  if (!config.autoDetect.enabled) {
    return {};
  }
  
  const detections = detector.detect(message.content, config.autoDetect);
  
  if (detections.length > 0) {
    // Log detection events
    detections.forEach(d => {
      storage.logDetection(d.type, 'asked', 'pending');
    });
    
    return {
      hasSensitiveInfo: true,
      detections,
      prompt: detector.generatePrompt(detections)
    };
  }
  
  return {};
}

export default {
  tools,
  handleToolCall,
  onUserMessage
};
