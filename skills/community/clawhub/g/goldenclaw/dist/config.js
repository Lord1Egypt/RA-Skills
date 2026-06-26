"use strict";
/**
 * GoldenClaw Skill Configuration
 *
 * Configure your GCLAW token settings here after creating the token on Solana.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.SPENDING_FILE_NAME = exports.WALLET_FILE_NAME = exports.WALLET_DIR_NAME = exports.ARGON2_CONFIG = exports.SPENDING_LIMITS = exports.GCLAW_DONATE_ADDRESS = exports.GCLAW_FAUCET_URL = exports.NETWORK_NAME = exports.SOLANA_RPC_URL = exports.TOKEN_NAME = exports.TOKEN_SYMBOL = exports.TOKEN_DECIMALS = exports.GCLAW_TOKEN_MINT = void 0;
exports.getTokenMint = getTokenMint;
exports.toTokenUnits = toTokenUnits;
exports.fromTokenUnits = fromTokenUnits;
exports.isConfigured = isConfigured;
const web3_js_1 = require("@solana/web3.js");
// =============================================================================
// TOKEN CONFIGURATION - UPDATE THESE AFTER CREATING YOUR TOKEN
// =============================================================================
/**
 * GoldenClaw token mint address on Solana.
 * Default: mainnet GCLAW mint. Override with GCLAW_TOKEN_MINT for a different token (e.g. devnet).
 */
exports.GCLAW_TOKEN_MINT = process.env.GCLAW_TOKEN_MINT || '8fUqKCgQ2PHcYRnce9EPCeMKSaxd14t7323qbXnSJr4z';
/**
 * Token decimals (usually 6 for Solana SPL tokens)
 */
exports.TOKEN_DECIMALS = 6;
/**
 * Token symbol
 */
exports.TOKEN_SYMBOL = 'GCLAW';
/**
 * Token name
 */
exports.TOKEN_NAME = 'GoldenClaw';
// =============================================================================
// NETWORK CONFIGURATION
// =============================================================================
/**
 * Solana RPC endpoint
 * - Mainnet: https://api.mainnet-beta.solana.com (default for GCLAW)
 * - Devnet: https://api.devnet.solana.com (set SOLANA_RPC_URL for testing)
 */
exports.SOLANA_RPC_URL = process.env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com';
/**
 * Network name for display
 */
exports.NETWORK_NAME = exports.SOLANA_RPC_URL.includes('mainnet') ? 'mainnet' : 'devnet';
/**
 * Faucet API base URL for claiming GCLAW (goldenclaw.org)
 */
exports.GCLAW_FAUCET_URL = process.env.GCLAW_FAUCET_URL || 'https://goldenclaw.org';
/**
 * Main wallet address for SOL donations (treasury / project)
 */
exports.GCLAW_DONATE_ADDRESS = process.env.GCLAW_DONATE_ADDRESS || 'DfMVpQ7VVTpKaUikwL2F6J814rDzBppRm27SXSiNi4AW';
// =============================================================================
// SECURITY CONFIGURATION
// =============================================================================
/**
 * Spending limits to protect against unauthorized draining
 */
exports.SPENDING_LIMITS = {
    /** Maximum GCLAW tokens per single transaction */
    perTransaction: Number(process.env.GCLAW_TX_LIMIT) || 100,
    /** Maximum GCLAW tokens per 24-hour period */
    daily: Number(process.env.GCLAW_DAILY_LIMIT) || 1000,
    /** Transactions above this amount require explicit confirmation */
    confirmationThreshold: Number(process.env.GCLAW_CONFIRM_THRESHOLD) || 50,
};
/**
 * Argon2id parameters for key derivation
 * These are memory-hard to resist GPU/ASIC attacks
 */
exports.ARGON2_CONFIG = {
    memoryCost: 65536, // 64 MB
    timeCost: 3, // iterations
    parallelism: 4, // threads
    hashLength: 32, // 256 bits for AES-256
};
// =============================================================================
// WALLET STORAGE
// =============================================================================
/**
 * Directory name for wallet storage (relative to OpenClaw data dir)
 */
exports.WALLET_DIR_NAME = 'gclaw-wallet';
/**
 * Encrypted wallet file name
 */
exports.WALLET_FILE_NAME = 'wallet.enc';
/**
 * Spending tracker file name (for daily limits)
 */
exports.SPENDING_FILE_NAME = 'spending.json';
// =============================================================================
// HELPER FUNCTIONS
// =============================================================================
/**
 * Get the token mint as a PublicKey
 * @throws Error if mint address is not configured
 */
function getTokenMint() {
    if (!exports.GCLAW_TOKEN_MINT) {
        throw new Error('GoldenClaw token mint address not configured. ' +
            'Set GCLAW_TOKEN_MINT environment variable or update src/config.ts');
    }
    return new web3_js_1.PublicKey(exports.GCLAW_TOKEN_MINT);
}
/**
 * Convert human-readable amount to token units (with decimals)
 */
function toTokenUnits(amount) {
    return BigInt(Math.floor(amount * Math.pow(10, exports.TOKEN_DECIMALS)));
}
/**
 * Convert token units to human-readable amount
 */
function fromTokenUnits(units) {
    return Number(units) / Math.pow(10, exports.TOKEN_DECIMALS);
}
/**
 * Check if the skill is properly configured
 */
function isConfigured() {
    return exports.GCLAW_TOKEN_MINT.length > 0;
}
//# sourceMappingURL=config.js.map