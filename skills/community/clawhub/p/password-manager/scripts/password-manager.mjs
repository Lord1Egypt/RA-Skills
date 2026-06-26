#!/usr/bin/env node

/**
 * password-manager.mjs - Password Manager Main Entry
 * 
 * Provides CLI interface and library functions
 */

import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createInterface } from 'readline';

import storage, { sanitizeInput } from './storage.js';
import cryptoLib from './crypto.js';
import generator from './generator.js';
import validator from './validator.js';
import detector from './detector.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// CLI arguments
const args = process.argv.slice(2);
const command = args[0];

/**
 * Create readline interface
 */
function createReadline() {
  return createInterface({
    input: process.stdin,
    output: process.stdout
  });
}

/**
 * Hidden password input - with environment variable support
 */
async function promptPassword(rl, question) {
  // Check environment variable first (for automation/PTY)
  if (process.env.PASSWORD_MANAGER_MASTER_PASSWORD) {
    return process.env.PASSWORD_MANAGER_MASTER_PASSWORD;
  }
  
  // Try hidden input in TTY mode
  if (process.stdin.isTTY) {
    return new Promise((resolve) => {
      let password = '';
      process.stdout.write(question);
      process.stdin.setRawMode(true);
      process.stdin.resume();
      
      const onData = (key) => {
        if (key[0] === 13) { // Enter
          process.stdin.setRawMode(false);
          process.stdin.pause();
          process.stdin.removeListener('data', onData);
          resolve(password);
        } else if (key[0] === 3) { // Ctrl+C
          process.exit(0);
        } else {
          password += key;
          process.stdout.write('*');
        }
      };
      
      process.stdin.on('data', onData);
    });
  }
  
  // Fallback: visible input for non-TTY (pipes, redirects)
  return new Promise((resolve) => {
    rl.question(question + ' ', resolve);
  });
}

/**
 * Regular input
 */
async function prompt(rl, question) {
  return new Promise((resolve) => {
    rl.question(question, resolve);
  });
}

/**
 * Get master password
 */
async function getMasterPassword(rl, required = true) {
  const status = storage.getVaultStatus();
  
  // Check for vault errors
  if (status.error) {
    console.log('❌ Vault error:', status.error);
    if (!status.initialized) {
      console.log('   Run "password-manager init" to create a new vault');
    }
    return { key: null, unlocked: false, error: status.error };
  }
  
  if (status.unlocked) {
    return { key: null, unlocked: true };
  }
  
  if (!required && status.locked) {
    return { key: null, unlocked: false };
  }
  
  // First try to use existing cache (without password)
  const cacheResult = storage.getDecryptionKey();
  if (!cacheResult.locked) {
    // Cache is valid, use it directly
    return { key: cacheResult.key, unlocked: true, fromCache: true };
  }
  
  // Cache missing/expired, need password
  // Check environment variable
  if (process.env.PASSWORD_MANAGER_MASTER_PASSWORD && !status.error) {
    console.log('🔒 Cache missing, attempting to rebuild from environment variable...');
    const rebuildResult = storage.rebuildCache(process.env.PASSWORD_MANAGER_MASTER_PASSWORD);
    
    if (rebuildResult.success) {
      console.log('✅ Cache rebuilt successfully');
      return { key: rebuildResult.key, unlocked: true, fromCache: false };
    } else {
      console.log('❌ Cache rebuild failed:', rebuildResult.error);
      console.log('   Please check your PASSWORD_MANAGER_MASTER_PASSWORD environment variable');
    }
  }
  
  // Interactive input (command-line password parameters no longer supported)
  if (status.expired) {
    console.log('🔒 Master password expired (48 hours of inactivity), please re-enter');
  } else if (!status.initialized) {
    console.log('🔐 First-time use, please set master password');
  } else {
    console.log('🔒 Password manager is locked, please enter master password');
  }
  
  const password = await promptPassword(rl, 'Master Password: ');
  console.log(); // Newline
  
  // Verify and get key
  const result = storage.getDecryptionKey(password);
  
  if (result.locked) {
    if (result.reason === 'expired') {
      console.log('❌ Master password expired');
    } else if (result.reason === 'wrong_password' || result.reason === 'decrypt_failed') {
      console.log('❌ Incorrect master password');
    } else {
      console.log('❌ Vault corrupted or cannot be unlocked');
    }
    return { key: null, unlocked: false };
  }
  
  return { key: result.key, unlocked: true };
}

/**
 * Confirm sensitive action
 */
async function confirmSensitiveAction(rl, action) {
  const config = storage.loadConfig();
  
  if (!config.requireConfirm[action]) {
    return true;
  }
  
  console.log(`⚠️  This is a sensitive operation (${action}), please re-enter master password to confirm`);
  const password = await promptPassword(rl, 'Master Password: ');
  console.log();
  
  const result = storage.getDecryptionKey(password);
  return !result.locked;
}

/**
 * Initialize command
 */
async function cmdInit() {
  const rl = createReadline();
  
  console.log('🔐 Initialize Password Manager');
  console.log('');
  console.log('Master password is used to encrypt all sensitive information, please store it securely.');
  console.log('Once lost, it cannot be recovered!');
  console.log('');
  
  const password = await promptPassword(rl, 'Set Master Password: ');
  console.log();
  const confirm = await promptPassword(rl, 'Confirm Master Password: ');
  console.log();
  
  if (password !== confirm) {
    console.log('❌ Passwords do not match');
    rl.close();
    process.exit(1);
  }
  
  // Validate master password strength
  const validation = validator.validateMasterPassword(password);
  if (!validation.valid) {
    console.log('⚠️  Master password strength is insufficient:');
    validation.errors.forEach(e => console.log(`   - ${e}`));
    console.log('');
    
    const force = args.includes('--force');
    if (!force) {
      const continueAnyway = await prompt(rl, 'Continue anyway? (y/N): ');
      if (continueAnyway.toLowerCase() !== 'y') {
        console.log('Cancelled');
        rl.close();
        process.exit(0);
      }
    }
  }
  
  const result = storage.initializeVault(password);
  console.log('✅', result.message);
  
  rl.close();
}

/**
 * Add entry command
 */
async function cmdAdd() {
  const rl = createReadline();
  const auth = await getMasterPassword(rl);
  
  if (!auth.unlocked) {
    rl.close();
    return;
  }
  
  const name = args.find((_, i) => args[i - 1] === '--name');
  const type = args.find((_, i) => args[i - 1] === '--type') || 'password';
  const username = args.find((_, i) => args[i - 1] === '--username');
  const password = args.find((_, i) => args[i - 1] === '--password');
  const tagsArg = args.find((_, i) => args[i - 1] === '--tags');
  
  if (!name) {
    console.log('❌ Missing --name parameter');
    rl.close();
    return;
  }
  
  // Input validation and sanitization
  const sanitizedName = sanitizeInput(name, 100);
  const sanitizedUsername = username ? sanitizeInput(username, 200) : '';
  const sanitizedPassword = password ? sanitizeInput(password, 1024) : '';
  const sanitizedTags = tagsArg ? sanitizeInput(tagsArg, 500) : '';
  
  // Load vault
  const vault = storage.loadVault(auth.key);
  
  // Check if already exists
  const existing = vault.entries.find(e => e.name === sanitizedName);
  if (existing) {
    console.log(`⚠️  Entry "${sanitizedName}" already exists, overwrite?`);
    const confirm = await prompt(rl, '(y/N): ');
    if (confirm.toLowerCase() !== 'y') {
      console.log('Cancelled');
      rl.close();
      return;
    }
    vault.entries = vault.entries.filter(e => e.name !== sanitizedName);
  }
  
  const entry = {
    id: cryptoLib.randomHex(16),
    name: sanitizedName,
    type,
    username: sanitizedUsername,
    password: sanitizedPassword || generator.generatePassword(),
    tags: sanitizedTags ? sanitizedTags.split(',').map(t => sanitizeInput(t, 50)) : [],
    notes: '',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };
  
  // Validate
  const validation = validator.validateEntry(entry);
  if (!validation.valid) {
    console.log('❌ Validation failed:');
    validation.errors.forEach(e => console.log(`   - ${e}`));
    rl.close();
    return;
  }
  
  if (validation.warnings) {
    validation.warnings.forEach(w => console.log('⚠️  ', w));
  }
  
  vault.entries.push(entry);
  storage.saveVault(vault, auth.key);
  
  console.log(`✅ Entry added: ${sanitizedName}`);
  if (!sanitizedPassword) {
    console.log(`   Generated password: ${entry.password}`);
  }
  
  rl.close();
}

/**
 * Get entry command
 */
async function cmdGet() {
  const rl = createReadline();
  const auth = await getMasterPassword(rl);
  
  if (!auth.unlocked) {
    rl.close();
    return;
  }
  
  const name = args.find((_, i) => args[i - 1] === '--name');
  const showPassword = args.includes('--show-password');
  
  if (!name) {
    console.log('❌ Missing --name parameter');
    rl.close();
    return;
  }
  
  // Input sanitization
  const sanitizedName = sanitizeInput(name, 100);
  
  const vault = storage.loadVault(auth.key);
  const entry = vault.entries.find(e => e.name === sanitizedName);
  
  if (!entry) {
    console.log(`❌ Entry not found: ${sanitizedName}`);
    rl.close();
    return;
  }
  
  console.log(`\n📋 ${entry.name}`);
  console.log(`   Type: ${entry.type}`);
  console.log(`   Username: ${entry.username || '-'}`);
  console.log(`   Tags: ${entry.tags.length > 0 ? entry.tags.join(', ') : '-'}`);
  console.log(`   Created: ${entry.createdAt}`);
  console.log(`   Updated: ${entry.updatedAt}`);
  
  if (showPassword) {
    console.log(`   Password/Value: ${entry.password}`);
  } else {
    console.log(`   Password/Value: ******** (use --show-password to view)`);
  }
  
  rl.close();
}

/**
 * Search command
 */
async function cmdSearch() {
  const rl = createReadline();
  const auth = await getMasterPassword(rl);
  
  if (!auth.unlocked) {
    rl.close();
    return;
  }
  
  const query = args.find((_, i) => args[i - 1] === '--query');
  const type = args.find((_, i) => args[i - 1] === '--type');
  const tag = args.find((_, i) => args[i - 1] === '--tag');
  
  const vault = storage.loadVault(auth.key);
  let results = vault.entries;
  
  if (query) {
    const sanitizedQuery = sanitizeInput(query, 100).toLowerCase();
    results = results.filter(e => 
      e.name.toLowerCase().includes(sanitizedQuery) ||
      e.tags.some(t => t.toLowerCase().includes(sanitizedQuery))
    );
  }
  
  if (type) {
    const sanitizedType = sanitizeInput(type, 20);
    results = results.filter(e => e.type === sanitizedType);
  }
  
  if (tag) {
    const sanitizedTag = sanitizeInput(tag, 50);
    results = results.filter(e => e.tags.includes(sanitizedTag));
  }
  
  console.log(`\n📊 Found ${results.length} entries:\n`);
  
  results.forEach(e => {
    console.log(`   ${e.name} (${e.type}) [${e.tags.join(', ') || 'No tags'}]`);
  });
  
  rl.close();
}

/**
 * List command
 */
async function cmdList() {
  const rl = createReadline();
  const auth = await getMasterPassword(rl);
  
  if (!auth.unlocked) {
    rl.close();
    return;
  }
  
  const type = args.find((_, i) => args[i - 1] === '--type');
  
  const vault = storage.loadVault(auth.key);
  let entries = vault.entries;
  
  if (type) {
    const sanitizedType = sanitizeInput(type, 20);
    entries = entries.filter(e => e.type === sanitizedType);
  }
  
  console.log(`\n📋 Vault (${entries.length} entries):\n`);
  
  entries.forEach(e => {
    console.log(`   ${e.name.padEnd(30)} ${e.type.padEnd(10)} [${e.tags.join(', ') || 'No tags'}]`);
  });
  
  rl.close();
}

/**
 * Generate password command
 */
async function cmdGenerate() {
  const length = parseInt(args.find((_, i) => args[i - 1] === '--length') || '32');
  // Support both --no-symbols and --include-symbols false
  const noSymbols = args.includes('--no-symbols') || 
                    (args.includes('--include-symbols') && 
                     args[args.indexOf('--include-symbols') + 1] === 'false');
  const includeNumbers = !args.includes('--no-numbers');
  const includeUppercase = !args.includes('--no-uppercase');
  
  const password = generator.generatePassword({
    length,
    includeSymbols: !noSymbols,
    includeNumbers,
    includeUppercase
  });
  
  console.log(`\n🔑 Generated Password:\n`);
  console.log(`   ${password}`);
  console.log(`\n   Length: ${length}`);
  
  const strength = generator.checkStrength(password);
  console.log(`   Strength: ${strength.description}`);
}

/**
 * Check password strength command
 */
async function cmdCheckStrength() {
  const passwordIndex = args.findIndex(a => a === '--password');
  let password;
  
  if (passwordIndex !== -1 && args[passwordIndex + 1]) {
    password = args[passwordIndex + 1];
  } else {
    // If no --password parameter, try to get first non-argument value
    const nonArg = args.find(a => !a.startsWith('-'));
    password = nonArg;
  }
  
  if (!password) {
    console.log('❌ Please provide password to check');
    console.log('Usage: password-manager check-strength --password <pwd>');
    return;
  }
  
  const strength = generator.checkStrength(password);
  
  console.log(`\n📊 Password Strength Assessment:\n`);
  console.log(`   Length: ${strength.length}`);
  console.log(`   Strength: ${strength.description}`);
  console.log(`   Score: ${strength.score}`);
  console.log(`\n   Characteristics:`);
  console.log(`     - Lowercase: ${strength.hasLowercase ? '✓' : '✗'}`);
  console.log(`     - Uppercase: ${strength.hasUppercase ? '✓' : '✗'}`);
  console.log(`     - Numbers: ${strength.hasNumbers ? '✓' : '✗'}`);
  console.log(`     - Symbols: ${strength.hasSymbols ? '✓' : '✗'}`);
  
  if (strength.feedback.length > 0) {
    console.log(`\n   Recommendations:`);
    strength.feedback.forEach(f => console.log(`     - ${f}`));
  }
}

/**
 * Status command
 */
async function cmdStatus() {
  const status = storage.getVaultStatus();
  
  console.log('\n📊 Password Manager Status:\n');
  
  if (!status.exists || !status.initialized) {
    console.log('   Status: Not initialized');
    console.log('\n   Run "password-manager init" to initialize');
  } else if (status.unlocked) {
    console.log('   Status: 🔓 Unlocked');
    console.log(`   Last used: ${status.lastUsed}`);
    console.log(`   Expires at: ${status.expiresAt}`);
  } else {
    console.log('   Status: 🔒 Locked');
    if (status.expired) {
      console.log('   Reason: Master password expired');
      console.log(`   Last used: ${status.lastUsed}`);
    }
  }
}

/**
 * Lock command
 */
async function cmdLock() {
  storage.lockVault();
  console.log('✅ Password manager locked');
}

/**
 * Unlock command
 */
async function cmdUnlock() {
  const rl = createReadline();
  const auth = await getMasterPassword(rl);
  
  if (auth.unlocked) {
    console.log('✅ Unlocked');
  }
  
  rl.close();
}


/**
 * Update entry command (NEW)
 */
async function cmdUpdate() {
  const rl = createReadline();
  const auth = await getMasterPassword(rl);
  
  if (!auth.unlocked) {
    rl.close();
    return;
  }
  
  const name = args.find((_, i) => args[i - 1] === '--name');
  const password = args.find((_, i) => args[i - 1] === '--password');
  const username = args.find((_, i) => args[i - 1] === '--username');
  const tagsArg = args.find((_, i) => args[i - 1] === '--tags');
  const notes = args.find((_, i) => args[i - 1] === '--notes');
  
  if (!name) {
    console.log('❌ Missing --name parameter');
    rl.close();
    return;
  }
  
  // Load vault
  const vault = storage.loadVault(auth.key);
  const entry = vault.entries.find(e => e.name === name);
  
  if (!entry) {
    console.log(`❌ Entry "${name}" not found`);
    rl.close();
    return;
  }
  
  // Update fields if provided
  let updated = false;
  if (password !== undefined) {
    entry.password = sanitizeInput(password, 1024);
    updated = true;
  }
  if (username !== undefined) {
    entry.username = sanitizeInput(username, 200);
    updated = true;
  }
  if (tagsArg !== undefined) {
    entry.tags = sanitizeInput(tagsArg, 500).split(',').map(t => sanitizeInput(t, 50));
    updated = true;
  }
  if (notes !== undefined) {
    entry.notes = sanitizeInput(notes, 1000);
    updated = true;
  }
  
  if (!updated) {
    console.log('❌ No fields to update. Use --password, --username, --tags, or --notes');
    rl.close();
    return;
  }
  
  entry.updatedAt = new Date().toISOString();
  
  // Save vault
  const result = storage.saveVault(vault, auth.key);
  if (result.success) {
    console.log(`✅ Entry updated: ${name}`);
  } else {
    console.log(`❌ Failed to update: ${result.error}`);
  }
  
  rl.close();
}


/**
 * Change master password command (NEW)
 */
async function cmdChangePassword() {
  const rl = createReadline();
  
  const oldPassword = args.find((_, i) => args[i - 1] === '--old');
  const newPassword = args.find((_, i) => args[i - 1] === '--new');
  
  if (!oldPassword || !newPassword) {
    console.log('❌ Missing --old or --new parameter');
    console.log('Usage: password-manager change-password --old <old-password> --new <new-password>');
    rl.close();
    return;
  }
  
  // Validate new password strength
  const validation = validator.validateMasterPassword(newPassword);
  if (!validation.valid) {
    console.log('⚠️  New password strength is insufficient:');
    validation.errors.forEach(e => console.log(`   - ${e}`));
    const force = args.includes('--force');
    if (!force) {
      const continueAnyway = await prompt(rl, 'Continue anyway? (y/N): ');
      if (continueAnyway.toLowerCase() !== 'y') {
        console.log('Cancelled');
        rl.close();
        process.exit(0);
      }
    }
  }
  
  // Use storage.changeMasterPassword API
  const result = storage.changeMasterPassword(oldPassword, newPassword);
  
  if (result.success) {
    console.log('✅ Master password changed successfully');
    console.log('   Vault re-encrypted with new password');
    console.log('   Cache updated');
  } else {
    console.log(`❌ Failed: ${result.error}`);
  }
  
  rl.close();
}

/**
 * Delete entry command
 */
async function cmdDelete() {
  const rl = createReadline();
  const auth = await getMasterPassword(rl);
  
  if (!auth.unlocked) {
    rl.close();
    return;
  }
  
  const name = args.find((_, i) => args[i - 1] === '--name');
  const confirm = args.includes('--confirm');
  
  if (!name) {
    console.log('❌ Missing --name parameter');
    rl.close();
    return;
  }
  
  // Input sanitization
  const sanitizedName = sanitizeInput(name, 100);
  
  // Sensitive action confirmation
  if (!confirm) {
    const confirmed = await confirmSensitiveAction(rl, 'delete');
    if (!confirmed) {
      console.log('❌ Incorrect master password, operation cancelled');
      rl.close();
      return;
    }
  }
  
  const vault = storage.loadVault(auth.key);
  const index = vault.entries.findIndex(e => e.name === sanitizedName);
  
  if (index === -1) {
    console.log(`❌ Entry not found: ${sanitizedName}`);
    rl.close();
    return;
  }
  
  vault.entries.splice(index, 1);
  storage.saveVault(vault, auth.key);
  
  console.log(`✅ Entry deleted: ${sanitizedName}`);
  
  rl.close();
}

/**
 * Help command
 */
function cmdHelp() {
  console.log(`
🔐 password-manager - Local Password Manager

Usage: password-manager <command> [options]

Commands:
  init                    Initialize vault (first-time use)
  add                     Add entry
  get                     View entry
  update                  Update entry
  delete                  Delete entry
  update                  Update entry (NEW)
  search                  Search entries
  list                    List all entries
  generate                Generate password
  check-strength          Check password strength
  status                  View status
  lock                    Lock vault
  unlock                  Unlock vault
  change-password         Change master password (NEW)
  backup                  Backup vault
  restore                 Restore vault
  config                  Configuration management
  help                    Show help

Options:
  --name <name>           Entry name
  --type <type>           Entry type (password/token/api_key/secret)
  --username <user>       Username
  --password <pass>       Password
  --tags <tag1,tag2>      Tags
  --length <n>            Password length
  --master-password <pwd> Master password (command-line, insecure)
  --show-password         Show password in plaintext
  --confirm               Skip confirmation
  --force                 Force execution
  --old <pwd>             Old password (for change-password)
  --new <pwd>             New password (for change-password)
  --notes <notes>         Notes (for update)
  --no-symbols            Exclude symbols (for generate)
  --include-symbols false Exclude symbols (for generate)

Examples:
  password-manager init
  password-manager add --name "github" --type "token"
  password-manager get --name "github" --show-password
  password-manager update --name "github" --password "new_token"
  password-manager change-password --old "old-pass" --new "new-pass"
  password-manager generate --length 32
  password-manager search --query "github"
`);
}

// Main entry
async function main() {
  switch (command) {
    case 'init':
      await cmdInit();
      break;
    case 'add':
      await cmdAdd();
      break;
    case 'get':
      await cmdGet();
      break;
    case 'update':
      await cmdUpdate();
      break;
    case 'change-password':
      await cmdChangePassword();
      break;
    case 'search':
      await cmdSearch();
      break;
    case 'list':
      await cmdList();
      break;
    case 'generate':
      await cmdGenerate();
      break;
    case 'check-strength':
      await cmdCheckStrength();
      break;
    case 'status':
      await cmdStatus();
      break;
    case 'lock':
      await cmdLock();
      break;
    case 'unlock':
      await cmdUnlock();
      break;
    case 'delete':
      await cmdDelete();
      break;
    case 'help':
    case '--help':
    case '-h':
      cmdHelp();
      break;
    default:
      if (!command) {
        cmdHelp();
      } else {
        console.log(`❌ Unknown command: ${command}`);
        console.log('Run "password-manager help" for help');
        process.exit(1);
      }
  }
}

// Export library functions
export {
  storage,
  cryptoLib as crypto,
  generator,
  validator,
  detector
};

// Run CLI
if (process.argv[1].includes('password-manager.mjs')) {
  main();
}

export default { main };
