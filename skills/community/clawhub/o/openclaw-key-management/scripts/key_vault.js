const crypto = require('crypto');
const fs = require('fs').promises;
const path = require('path');

class SecureKeyVault {
  constructor(workspacePath) {
    this.workspacePath = workspacePath;
    this.secretsPath = path.join(workspacePath, '.secrets');
    this.configPath = path.join(workspacePath, 'config', 'key_management.json');
    this.vaultPath = path.join(this.secretsPath, 'vault.json.enc');
    this.masterKey = null;
    this.runtimeCache = new Map();
    this.vault = {};
  }

  async initialize() {
    // Load configuration
    const config = JSON.parse(await fs.readFile(this.configPath, 'utf8'));
    
    // Generate system key from machine UUID and hostname
    const machineId = await this.getMachineId();
    const hostname = require('os').hostname();
    const systemKey = crypto.createHash('sha256')
      .update(machineId + hostname)
      .digest();
    
    // Derive master key from system key
    this.masterKey = await this.deriveMasterKeyFromSystem(systemKey);
    
    // Load and decrypt vault
    await this.loadVault();
  }

  async getMachineId() {
    try {
      // Try to get machine ID from /etc/machine-id (Linux)
      const machineId = await fs.readFile('/etc/machine-id', 'utf8');
      return machineId.trim();
    } catch (error) {
      // Fallback to MAC address hash
      const os = require('os');
      const networkInterfaces = os.networkInterfaces();
      let macAddress = '';
      for (const interfaceName in networkInterfaces) {
        const interfaces = networkInterfaces[interfaceName];
        for (const iface of interfaces) {
          if (iface.family === 'IPv4' && !iface.internal) {
            macAddress = iface.mac.replace(/:/g, '');
            break;
          }
        }
        if (macAddress) break;
      }
      return crypto.createHash('sha256').update(macAddress).digest('hex');
    }
  }

  async deriveMasterKeyFromSystem(systemKey) {
    const salt = Buffer.from('OpenClawKeyVaultSalt2026', 'utf8');
    return new Promise((resolve, reject) => {
      crypto.pbkdf2(
        systemKey,
        salt,
        100000,
        32,
        'sha256',
        (err, derivedKey) => {
          if (err) reject(err);
          else resolve(derivedKey);
        }
      );
    });
  }

  async loadVault() {
    try {
      // Check if file exists using stat
      const stats = await fs.stat(this.vaultPath);
      if (stats.isFile()) {
        // Read the encrypted vault data
        const encryptedVaultData = await fs.readFile(this.vaultPath, 'base64');
        
        // The vault file contains the encrypted vault JSON directly
        const decryptedVaultJson = await this.decryptData(encryptedVaultData, this.masterKey);
        this.vault = JSON.parse(decryptedVaultJson);
        console.log('Vault loaded successfully with', Object.keys(this.vault).length, 'secrets');
      } else {
        console.log('Vault file exists but is not a regular file');
        this.vault = {};
      }
    } catch (error) {
      if (error.code === 'ENOENT') {
        console.log('No existing vault found, creating new one');
        this.vault = {};
      } else {
        console.error('Error loading vault:', error.message);
        this.vault = {};
      }
    }
  }

  async saveVault() {
    const vaultJson = JSON.stringify(this.vault, null, 2);
    const encryptedVault = await this.encryptData(vaultJson, this.masterKey);
    // Save the encrypted data directly as base64 string
    await fs.writeFile(this.vaultPath, encryptedVault);
  }

  async getSecret(name) {
    // Check runtime cache first
    if (this.runtimeCache.has(name)) {
      const cached = this.runtimeCache.get(name);
      if (Date.now() - cached.timestamp < 30000) { // 30 seconds
        return cached.value;
      }
      // Clear expired cache
      this.runtimeCache.delete(name);
    }

    // Decrypt from vault
    const encryptedData = this.vault[name];
    if (!encryptedData) {
      throw new Error(`Secret '${name}' not found`);
    }

    const decrypted = await this.decryptCredential(encryptedData, this.masterKey);
    
    // Cache in memory
    this.runtimeCache.set(name, {
      value: decrypted,
      timestamp: Date.now()
    });

    // Schedule cleanup
    setTimeout(() => {
      if (this.runtimeCache.has(name)) {
        this.secureZero(this.runtimeCache.get(name).value);
        this.runtimeCache.delete(name);
      }
    }, 30000);

    return decrypted;
  }

  async setSecret(name, value, metadata = {}) {
    const encrypted = await this.encryptCredential(value, this.masterKey);
    this.vault[name] = {
      ...encrypted,
      metadata: {
        ...metadata,
        created: new Date().toISOString(),
        last_modified: new Date().toISOString()
      }
    };
    await this.saveVault();
  }

  async encryptCredential(credential, masterKey) {
    const salt = crypto.randomBytes(16);
    const iv = crypto.randomBytes(12);
    
    // Derive credential-specific key
    const credentialKey = crypto.pbkdf2Sync(
      masterKey, 
      salt, 
      100000, 
      32, 
      'sha256'
    );
    
    // Encrypt with AES-256-GCM
    const cipher = crypto.createCipheriv('aes-256-gcm', credentialKey, iv);
    const encrypted = cipher.update(credential, 'utf8', 'base64');
    const final = cipher.final('base64');
    const authTag = cipher.getAuthTag();
    
    return {
      encrypted: encrypted + final,
      iv: iv.toString('base64'),
      salt: salt.toString('base64'),
      authTag: authTag.toString('base64'),
      timestamp: Date.now()
    };
  }

  async decryptCredential(encryptedData, masterKey) {
    const { encrypted, iv, salt, authTag } = encryptedData;
    
    // Derive credential-specific key
    const credentialKey = crypto.pbkdf2Sync(
      masterKey,
      Buffer.from(salt, 'base64'),
      100000,
      32,
      'sha256'
    );
    
    // Decrypt with AES-256-GCM
    const decipher = crypto.createDecipheriv('aes-256-gcm', credentialKey, Buffer.from(iv, 'base64'));
    decipher.setAuthTag(Buffer.from(authTag, 'base64'));
    const decrypted = decipher.update(encrypted, 'base64', 'utf8');
    const final = decipher.final('utf8');
    
    return decrypted + final;
  }

  async encryptData(data, key) {
    const iv = crypto.randomBytes(12);
    const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
    const encrypted = cipher.update(data, 'utf8', 'base64');
    const final = cipher.final('base64');
    const authTag = cipher.getAuthTag();
    
    // Return as JSON string
    const result = {
      encrypted: encrypted + final,
      iv: iv.toString('base64'),
      authTag: authTag.toString('base64')
    };
    
    return JSON.stringify(result);
  }

  async decryptData(encryptedDataBase64, key) {
    // Parse the base64 encoded JSON string
    const encryptedDataString = Buffer.from(encryptedDataBase64, 'base64').toString('utf8');
    const encryptedData = JSON.parse(encryptedDataString);
    
    const { encrypted, iv, authTag } = encryptedData;
    
    const decipher = crypto.createDecipheriv('aes-256-gcm', key, Buffer.from(iv, 'base64'));
    decipher.setAuthTag(Buffer.from(authTag, 'base64'));
    const decrypted = decipher.update(encrypted, 'base64', 'utf8');
    const final = decipher.final('utf8');
    
    return decrypted + final;
  }

  secureZero(buffer) {
    if (typeof buffer === 'string') {
      // Convert string to buffer for zeroing
      const buf = Buffer.from(buffer, 'utf8');
      buf.fill(0);
    } else if (Buffer.isBuffer(buffer)) {
      buffer.fill(0);
    }
  }

  async backupVault() {
    const backupPath = path.join(
      this.secretsPath, 
      'backup', 
      `vault_${new Date().toISOString().split('T')[0]}.json.enc`
    );
    await fs.copyFile(this.vaultPath, backupPath);
  }
}

module.exports = SecureKeyVault;