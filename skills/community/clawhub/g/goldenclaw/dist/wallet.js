"use strict";
/**
 * Wallet Management Module
 *
 * Handles secure keypair generation, encryption, storage, and recovery.
 * Uses Argon2id for key derivation and AES-256-GCM for encryption.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.getWalletDirectory = getWalletDirectory;
exports.walletExists = walletExists;
exports.createWallet = createWallet;
exports.recoverWallet = recoverWallet;
exports.loadWallet = loadWallet;
exports.getWalletAddress = getWalletAddress;
exports.deleteWallet = deleteWallet;
exports.checkSpendingLimit = checkSpendingLimit;
exports.recordSpending = recordSpending;
exports.getRemainingDailyAllowance = getRemainingDailyAllowance;
const web3_js_1 = require("@solana/web3.js");
const crypto = __importStar(require("crypto"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const argon2 = __importStar(require("argon2"));
const bip39 = __importStar(require("bip39"));
const ed25519_hd_key_1 = require("ed25519-hd-key");
const config_js_1 = require("./config.js");
// =============================================================================
// WALLET STORAGE PATHS
// =============================================================================
/**
 * Get the wallet storage directory path
 */
function getWalletDir() {
    // Use OpenClaw's data directory if available, otherwise use home directory
    const baseDir = process.env.OPENCLAW_DATA_DIR ||
        path.join(process.env.HOME || process.env.USERPROFILE || '.', '.openclaw');
    return path.join(baseDir, config_js_1.WALLET_DIR_NAME);
}
/**
 * Get the wallet directory path (for display in errors so users can verify which folder is used)
 */
function getWalletDirectory() {
    return getWalletDir();
}
/**
 * Get the wallet file path
 */
function getWalletPath() {
    return path.join(getWalletDir(), config_js_1.WALLET_FILE_NAME);
}
/**
 * Get the spending tracker file path
 */
function getSpendingPath() {
    return path.join(getWalletDir(), config_js_1.SPENDING_FILE_NAME);
}
/**
 * Ensure wallet directory exists with secure permissions
 */
function ensureWalletDir() {
    const dir = getWalletDir();
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true, mode: 0o700 }); // Owner only
    }
}
// =============================================================================
// KEY DERIVATION & ENCRYPTION
// =============================================================================
/**
 * Derive an encryption key from password using Argon2id.
 * Password is trimmed so recover/setup and donate use the same key even if the UI adds spaces/newlines.
 */
async function deriveKey(password, salt) {
    const normalized = (password ?? '').trim();
    const hash = await argon2.hash(normalized, {
        type: argon2.argon2id,
        memoryCost: config_js_1.ARGON2_CONFIG.memoryCost,
        timeCost: config_js_1.ARGON2_CONFIG.timeCost,
        parallelism: config_js_1.ARGON2_CONFIG.parallelism,
        hashLength: config_js_1.ARGON2_CONFIG.hashLength,
        salt: salt,
        raw: true,
    });
    return Buffer.from(hash);
}
/**
 * Encrypt data using AES-256-GCM
 */
function encrypt(data, key) {
    const iv = crypto.randomBytes(12); // 96-bit IV for GCM
    const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
    const encrypted = Buffer.concat([cipher.update(data), cipher.final()]);
    const authTag = cipher.getAuthTag();
    return { encrypted, iv, authTag };
}
/**
 * Decrypt data using AES-256-GCM
 */
function decrypt(encrypted, key, iv, authTag) {
    const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
    decipher.setAuthTag(authTag);
    return Buffer.concat([decipher.update(encrypted), decipher.final()]);
}
// =============================================================================
// WALLET OPERATIONS
// =============================================================================
/** Solana system program address – we must never use or store this as a user wallet */
const SYSTEM_PROGRAM_ID = '11111111111111111111111111111111';
/**
 * Check if a wallet already exists
 */
function walletExists() {
    return fs.existsSync(getWalletPath());
}
/** Solana standard derivation path (BIP44) - same as Phantom, Solflare, etc. */
const SOLANA_DERIVATION_PATH = "m/44'/501'/0'/0'";
/**
 * Derive keypair from mnemonic using BIP44 path (Phantom-compatible).
 */
async function deriveKeypairFromMnemonic(mnemonic) {
    const seed = await bip39.mnemonicToSeed(mnemonic);
    const hexSeed = seed.toString('hex');
    const { key } = (0, ed25519_hd_key_1.derivePath)(SOLANA_DERIVATION_PATH, hexSeed);
    return web3_js_1.Keypair.fromSeed(key);
}
/**
 * Create a new wallet with BIP39 mnemonic backup.
 * Uses BIP44 derivation (m/44'/501'/0'/0') — same as Phantom and other Solana wallets.
 * Your seed phrase can be restored in Phantom to get the same address.
 *
 * @param password - Password to encrypt the wallet
 * @returns The keypair, mnemonic (SAVE THIS!), and address
 */
async function createWallet(password) {
    if (walletExists()) {
        throw new Error('Wallet already exists. Use loadWallet() or delete existing wallet first.');
    }
    const pwd = (password ?? '').trim();
    if (!pwd) {
        throw new Error('Password cannot be empty.');
    }
    const mnemonic = bip39.generateMnemonic(256);
    const keypair = await deriveKeypairFromMnemonic(mnemonic);
    if (keypair.publicKey.toBase58() === SYSTEM_PROGRAM_ID) {
        throw new Error('Generated keypair is the system program; please run "gclaw setup" again.');
    }
    await saveWallet(keypair, pwd);
    return {
        keypair,
        mnemonic,
        address: keypair.publicKey.toBase58(),
    };
}
/**
 * Recover wallet from BIP39 mnemonic.
 * Uses BIP44 derivation — same as Phantom. Restore your seed phrase in Phantom to get the same address.
 *
 * @param mnemonic - The 24-word recovery phrase
 * @param password - New password to encrypt the recovered wallet
 */
async function recoverWallet(mnemonic, password) {
    if (!bip39.validateMnemonic(mnemonic)) {
        throw new Error('Invalid mnemonic phrase');
    }
    const pwd = (password ?? '').trim();
    if (!pwd) {
        throw new Error('Password cannot be empty.');
    }
    const keypair = await deriveKeypairFromMnemonic(mnemonic);
    if (keypair.publicKey.toBase58() === SYSTEM_PROGRAM_ID) {
        throw new Error('Recovered keypair is the system program; use a different mnemonic or run "gclaw setup" for a new wallet.');
    }
    // Encrypt and save (use trimmed password so donate can decrypt with same password)
    await saveWallet(keypair, pwd);
    return {
        keypair,
        mnemonic,
        address: keypair.publicKey.toBase58(),
    };
}
/**
 * Save wallet to encrypted file
 */
async function saveWallet(keypair, password) {
    ensureWalletDir();
    // Generate salt for key derivation
    const salt = crypto.randomBytes(32);
    // Derive encryption key
    const key = await deriveKey(password, salt);
    // Normalize to 64-byte Uint8Array so save/load match regardless of Buffer vs Uint8Array from Keypair
    const secretBytes = new Uint8Array(keypair.secretKey);
    if (secretBytes.length !== 64) {
        key.fill(0);
        throw new Error(`Wallet save failed: keypair.secretKey length is ${secretBytes.length}, expected 64`);
    }
    const { encrypted, iv, authTag } = encrypt(Buffer.from(secretBytes), key);
    // Create wallet file structure
    const wallet = {
        encryptedKey: encrypted.toString('base64'),
        iv: iv.toString('base64'),
        authTag: authTag.toString('base64'),
        salt: salt.toString('base64'),
        publicKey: keypair.publicKey.toBase58(),
        version: 1,
    };
    // Write with secure permissions
    const walletPath = getWalletPath();
    fs.writeFileSync(walletPath, JSON.stringify(wallet, null, 2), { mode: 0o600 });
    // Clear sensitive data from memory
    key.fill(0);
}
/**
 * Load and decrypt wallet
 *
 * @param password - Password to decrypt the wallet
 * @returns The decrypted keypair
 */
async function loadWallet(password) {
    if (!walletExists()) {
        throw new Error('No wallet found. Create one first with createWallet()');
    }
    const pwd = (password ?? '').trim();
    if (!pwd) {
        throw new Error('Password cannot be empty.');
    }
    // Read wallet file
    const walletData = fs.readFileSync(getWalletPath(), 'utf-8');
    const wallet = JSON.parse(walletData);
    // Decode from base64
    const encrypted = Buffer.from(wallet.encryptedKey, 'base64');
    const iv = Buffer.from(wallet.iv, 'base64');
    const authTag = Buffer.from(wallet.authTag, 'base64');
    const salt = Buffer.from(wallet.salt, 'base64');
    // Derive key and decrypt (same trimmed password as recover/setup)
    const key = await deriveKey(pwd, salt);
    try {
        const decrypted = decrypt(encrypted, key, iv, authTag);
        // Normalize to Uint8Array(64) so Keypair.fromSecretKey gets same type as fromSeed (avoids Buffer vs Uint8Array differences)
        const secretBytes = new Uint8Array(decrypted);
        if (secretBytes.length !== 64) {
            key.fill(0);
            decrypted.fill(0);
            throw new Error(`Wallet file invalid: decrypted secret key length is ${secretBytes.length}, expected 64. The file may be corrupted.`);
        }
        // Pass a copy so the keypair keeps its own secret; we can safely clear secretBytes/decrypted below
        const keypair = web3_js_1.Keypair.fromSecretKey(new Uint8Array(secretBytes));
        // Reject system program keypair with clear instructions
        if (keypair.publicKey.toBase58() === SYSTEM_PROGRAM_ID) {
            key.fill(0);
            secretBytes.fill(0);
            decrypted.fill(0);
            throw new Error([
                'Invalid wallet: decrypted keypair is the system program (1111...).',
                '',
                'Why: "gclaw balance" shows the address from the wallet file (no password). "gclaw donate" decrypts the file with your password to sign. The file at the path below decrypts to 1111..., so either that file is wrong or OPENCLAW_DATA_DIR points to a different folder than when you run balance.',
                '',
                `Wallet folder: ${getWalletDirectory()}`,
                `Address in that file (what balance shows): ${wallet.publicKey}`,
                '',
                'Fix: Run balance and donate in the same way (same shell, same OPENCLAW_DATA_DIR). Use the same password you used for gclaw setup. If the file is wrong, use "gclaw recover <your-24-word-mnemonic>" to restore, or delete the wallet and run "gclaw setup" again.',
            ].join('\n'));
        }
        // Verify decrypted keypair matches the stored public key (catches corrupt/inconsistent file)
        if (keypair.publicKey.toBase58() !== wallet.publicKey) {
            key.fill(0);
            secretBytes.fill(0);
            decrypted.fill(0);
            throw new Error(`Wallet file inconsistent: file says address ${wallet.publicKey} but decrypted keypair is ${keypair.publicKey.toBase58()}. ` +
                'The wallet file may be corrupted. Use "gclaw recover <your-24-word-mnemonic>" to restore from backup, or delete the wallet and run "gclaw setup" again.');
        }
        // Clear sensitive data
        key.fill(0);
        secretBytes.fill(0);
        decrypted.fill(0);
        return keypair;
    }
    catch (error) {
        key.fill(0);
        if (error instanceof Error) {
            if (error.message.startsWith('Wallet file inconsistent') || error.message.startsWith('Invalid wallet:')) {
                throw error;
            }
        }
        throw new Error('Invalid password or corrupted wallet file');
    }
}
/**
 * Get wallet public address without decrypting
 */
function getWalletAddress() {
    if (!walletExists()) {
        return null;
    }
    const walletData = fs.readFileSync(getWalletPath(), 'utf-8');
    const wallet = JSON.parse(walletData);
    return wallet.publicKey;
}
/**
 * Delete wallet (use with caution!)
 */
function deleteWallet() {
    const walletPath = getWalletPath();
    const spendingPath = getSpendingPath();
    if (fs.existsSync(walletPath)) {
        // Overwrite with zeros before deleting (secure deletion)
        const size = fs.statSync(walletPath).size;
        fs.writeFileSync(walletPath, Buffer.alloc(size, 0));
        fs.unlinkSync(walletPath);
    }
    if (fs.existsSync(spendingPath)) {
        fs.unlinkSync(spendingPath);
    }
}
// =============================================================================
// SPENDING LIMITS
// =============================================================================
/**
 * Get today's date string
 */
function getTodayString() {
    return new Date().toISOString().split('T')[0];
}
/**
 * Load spending tracker
 */
function loadSpending() {
    const spendingPath = getSpendingPath();
    if (!fs.existsSync(spendingPath)) {
        return { date: getTodayString(), spent: 0 };
    }
    const data = JSON.parse(fs.readFileSync(spendingPath, 'utf-8'));
    // Reset if it's a new day
    if (data.date !== getTodayString()) {
        return { date: getTodayString(), spent: 0 };
    }
    return data;
}
/**
 * Save spending tracker
 */
function saveSpending(tracker) {
    ensureWalletDir();
    fs.writeFileSync(getSpendingPath(), JSON.stringify(tracker, null, 2));
}
/**
 * Check if a transaction amount is within spending limits
 *
 * @param amount - Amount to spend
 * @returns Object with allowed status and reason if denied
 */
function checkSpendingLimit(amount) {
    // Check per-transaction limit
    if (amount > config_js_1.SPENDING_LIMITS.perTransaction) {
        return {
            allowed: false,
            reason: `Amount ${amount} exceeds per-transaction limit of ${config_js_1.SPENDING_LIMITS.perTransaction} CLAW`,
            requiresConfirmation: false,
        };
    }
    // Check daily limit
    const tracker = loadSpending();
    if (tracker.spent + amount > config_js_1.SPENDING_LIMITS.daily) {
        return {
            allowed: false,
            reason: `Amount would exceed daily limit of ${config_js_1.SPENDING_LIMITS.daily} CLAW (already spent: ${tracker.spent})`,
            requiresConfirmation: false,
        };
    }
    // Check if confirmation required
    const requiresConfirmation = amount > config_js_1.SPENDING_LIMITS.confirmationThreshold;
    return { allowed: true, requiresConfirmation };
}
/**
 * Record a spending transaction
 */
function recordSpending(amount) {
    const tracker = loadSpending();
    tracker.spent += amount;
    saveSpending(tracker);
}
/**
 * Get remaining daily spending allowance
 */
function getRemainingDailyAllowance() {
    const tracker = loadSpending();
    return Math.max(0, config_js_1.SPENDING_LIMITS.daily - tracker.spent);
}
//# sourceMappingURL=wallet.js.map