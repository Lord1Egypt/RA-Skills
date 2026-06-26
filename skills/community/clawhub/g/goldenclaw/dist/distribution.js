"use strict";
/**
 * Token Distribution Module
 *
 * Implements the GoldenClaw (GCLAW) tokenomics:
 * - Fixed supply: 1,000,000,000,000 (1 trillion) tokens
 * - Each new wallet receives 1/1,000,000 of remaining treasury balance
 * - Distribution continues until treasury reaches minimum precision
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
exports.MIN_TREASURY_BALANCE = exports.DISTRIBUTION_DIVISOR = exports.TOTAL_SUPPLY = void 0;
exports.loadClaimedAddresses = loadClaimedAddresses;
exports.saveClaimedAddress = saveClaimedAddress;
exports.loadDistributionState = loadDistributionState;
exports.calculateDistributionAmount = calculateDistributionAmount;
exports.hasAlreadyClaimed = hasAlreadyClaimed;
exports.hasAlreadyClaimedOnChain = hasAlreadyClaimedOnChain;
exports.getTreasuryBalance = getTreasuryBalance;
exports.getDistributionStats = getDistributionStats;
exports.processClaim = processClaim;
exports.formatDistributionStats = formatDistributionStats;
exports.formatClaimResult = formatClaimResult;
exports.simulateDistribution = simulateDistribution;
const web3_js_1 = require("@solana/web3.js");
const spl_token_1 = require("@solana/spl-token");
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const config_js_1 = require("./config.js");
// =============================================================================
// TOKENOMICS CONSTANTS
// =============================================================================
/**
 * Total fixed supply of GCLAW tokens
 */
exports.TOTAL_SUPPLY = 1_000_000_000_000; // 1 trillion
/**
 * Distribution divisor - each claim gets 1/DIVISOR of remaining
 */
exports.DISTRIBUTION_DIVISOR = 1_000_000; // 1 millionth
/**
 * Minimum treasury balance before distribution stops
 * This is the smallest unit possible (1 with 6 decimals = 0.000001)
 */
exports.MIN_TREASURY_BALANCE = 1 / Math.pow(10, config_js_1.TOKEN_DECIMALS); // 0.000001
function getDistributionDir() {
    const baseDir = process.env.OPENCLAW_DATA_DIR ||
        path.join(process.env.HOME || process.env.USERPROFILE || '.', '.openclaw');
    return path.join(baseDir, config_js_1.WALLET_DIR_NAME);
}
function getDistributionStatePath() {
    return path.join(getDistributionDir(), 'distribution-state.json');
}
function getClaimedAddressesPath() {
    return path.join(getDistributionDir(), 'claimed-addresses.json');
}
/**
 * Load the list of addresses that have already claimed
 */
function loadClaimedAddresses() {
    const filePath = getClaimedAddressesPath();
    if (!fs.existsSync(filePath)) {
        return new Set();
    }
    const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    return new Set(data.addresses || []);
}
/**
 * Save claimed address (exported so skill can record successful faucet claims locally)
 */
function saveClaimedAddress(address) {
    const dir = getDistributionDir();
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    const claimed = loadClaimedAddresses();
    claimed.add(address);
    fs.writeFileSync(getClaimedAddressesPath(), JSON.stringify({ addresses: Array.from(claimed) }, null, 2));
}
/**
 * Load distribution state
 */
function loadDistributionState() {
    const filePath = getDistributionStatePath();
    if (!fs.existsSync(filePath)) {
        return null;
    }
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}
/**
 * Save distribution state
 */
function saveDistributionState(state) {
    const dir = getDistributionDir();
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(getDistributionStatePath(), JSON.stringify(state, null, 2));
}
// =============================================================================
// DISTRIBUTION LOGIC
// =============================================================================
/**
 * Calculate the amount a new wallet should receive based on remaining treasury
 *
 * @param remainingTreasury - Current treasury balance
 * @returns Amount to distribute (0 if below minimum)
 */
function calculateDistributionAmount(remainingTreasury) {
    if (remainingTreasury <= exports.MIN_TREASURY_BALANCE) {
        return 0; // Distribution complete
    }
    const amount = remainingTreasury / exports.DISTRIBUTION_DIVISOR;
    // Round down to token precision
    const units = Math.floor(amount * Math.pow(10, config_js_1.TOKEN_DECIMALS));
    const roundedAmount = units / Math.pow(10, config_js_1.TOKEN_DECIMALS);
    // If rounded amount is less than minimum precision, return 0
    if (roundedAmount < exports.MIN_TREASURY_BALANCE) {
        return 0;
    }
    return roundedAmount;
}
/**
 * Check if an address has already claimed (local check - fast but not tamper-proof)
 */
function hasAlreadyClaimed(address) {
    const claimed = loadClaimedAddresses();
    return claimed.has(address);
}
/**
 * Check if an address has already claimed BY CHECKING THE BLOCKCHAIN
 * This is tamper-proof because it uses on-chain data as the source of truth.
 *
 * @param claimantAddress - Address to check
 * @param treasuryAddress - Treasury wallet address
 * @returns true if the address has received tokens from treasury
 */
async function hasAlreadyClaimedOnChain(claimantAddress, treasuryAddress) {
    const connection = new web3_js_1.Connection(config_js_1.SOLANA_RPC_URL, 'confirmed');
    const mint = (0, config_js_1.getTokenMint)();
    try {
        const claimantPubkey = new web3_js_1.PublicKey(claimantAddress);
        const treasuryPubkey = new web3_js_1.PublicKey(treasuryAddress);
        // Get claimant's token account
        const claimantTokenAccount = await getAssociatedTokenAddress(mint, claimantPubkey);
        // Get treasury's token account
        const treasuryTokenAccount = await getAssociatedTokenAddress(mint, treasuryPubkey);
        // Get transaction signatures for the claimant's token account
        const signatures = await connection.getSignaturesForAddress(claimantTokenAccount, { limit: 100 });
        // Check each transaction to see if it came from treasury
        for (const sig of signatures) {
            const tx = await connection.getParsedTransaction(sig.signature, {
                maxSupportedTransactionVersion: 0,
            });
            if (!tx?.meta || tx.meta.err)
                continue;
            // Look for token transfers from treasury to this wallet
            const instructions = tx.transaction.message.instructions;
            for (const ix of instructions) {
                if (!('parsed' in ix) || !ix.parsed)
                    continue;
                const parsed = ix.parsed;
                if (parsed.type === 'transfer' || parsed.type === 'transferChecked') {
                    const source = parsed.info.source;
                    const destination = parsed.info.destination;
                    // Check if this transfer was FROM treasury TO claimant
                    if (source === treasuryTokenAccount.toBase58() &&
                        destination === claimantTokenAccount.toBase58()) {
                        return true; // Already received from treasury!
                    }
                }
            }
        }
        return false; // No transfers from treasury found
    }
    catch (error) {
        // If token account doesn't exist, they haven't claimed
        console.error('Error checking on-chain claim status:', error);
        return false;
    }
}
/**
 * Get the associated token address for a wallet
 */
async function getAssociatedTokenAddress(mint, owner) {
    const { getAssociatedTokenAddress: getATA } = await import('@solana/spl-token');
    return getATA(mint, owner);
}
/**
 * Get the current treasury balance
 */
async function getTreasuryBalance(treasuryAddress) {
    const connection = new web3_js_1.Connection(config_js_1.SOLANA_RPC_URL, 'confirmed');
    const mint = (0, config_js_1.getTokenMint)();
    const treasuryPubkey = new web3_js_1.PublicKey(treasuryAddress);
    try {
        const tokenAccount = await (0, spl_token_1.getOrCreateAssociatedTokenAccount)(connection, web3_js_1.Keypair.generate(), // Dummy keypair for read-only
        mint, treasuryPubkey);
        const account = await (0, spl_token_1.getAccount)(connection, tokenAccount.address);
        return (0, config_js_1.fromTokenUnits)(account.amount);
    }
    catch {
        return 0;
    }
}
/**
 * Get distribution statistics
 */
function getDistributionStats() {
    const claimed = loadClaimedAddresses();
    // Estimate remaining claims based on exponential decay
    // After n claims: remaining = TOTAL_SUPPLY * ((DIVISOR-1)/DIVISOR)^n
    // Solve for n when remaining = MIN_TREASURY_BALANCE
    const decayFactor = (exports.DISTRIBUTION_DIVISOR - 1) / exports.DISTRIBUTION_DIVISOR;
    const maxClaims = Math.floor(Math.log(exports.MIN_TREASURY_BALANCE / exports.TOTAL_SUPPLY) / Math.log(decayFactor));
    return {
        totalSupply: exports.TOTAL_SUPPLY,
        divisor: exports.DISTRIBUTION_DIVISOR,
        minBalance: exports.MIN_TREASURY_BALANCE,
        claimedCount: claimed.size,
        estimatedRemainingClaims: Math.max(0, maxClaims - claimed.size),
    };
}
/**
 * Process a claim for a wallet address
 *
 * Security: Uses DUAL verification:
 * 1. Local file check (fast, first line of defense)
 * 2. On-chain verification (tamper-proof, blockchain as source of truth)
 *
 * @param claimantAddress - Address claiming tokens
 * @param treasuryKeypair - Treasury wallet keypair (for signing)
 * @param skipOnChainCheck - Skip on-chain check (for testing only!)
 */
async function processClaim(claimantAddress, treasuryKeypair, skipOnChainCheck = false) {
    // SECURITY CHECK 1: Local file check (fast)
    if (hasAlreadyClaimed(claimantAddress)) {
        return { success: false, error: 'This address has already claimed tokens (local record)' };
    }
    // Validate claimant address
    let claimantPubkey;
    try {
        claimantPubkey = new web3_js_1.PublicKey(claimantAddress);
    }
    catch {
        return { success: false, error: 'Invalid claimant address' };
    }
    const treasuryAddress = treasuryKeypair.publicKey.toBase58();
    // SECURITY CHECK 2: On-chain verification (tamper-proof)
    if (!skipOnChainCheck) {
        try {
            const alreadyClaimedOnChain = await hasAlreadyClaimedOnChain(claimantAddress, treasuryAddress);
            if (alreadyClaimedOnChain) {
                // Update local record to match on-chain state
                saveClaimedAddress(claimantAddress);
                return {
                    success: false,
                    error: 'This address has already received tokens from treasury (verified on-chain)'
                };
            }
        }
        catch (error) {
            // If on-chain check fails, continue with local check only
            // but log the error for monitoring
            console.warn('On-chain claim check failed, using local check only:', error);
        }
    }
    const connection = new web3_js_1.Connection(config_js_1.SOLANA_RPC_URL, 'confirmed');
    const mint = (0, config_js_1.getTokenMint)();
    // Get treasury balance
    let treasuryBalance;
    try {
        const treasuryTokenAccount = await (0, spl_token_1.getOrCreateAssociatedTokenAccount)(connection, treasuryKeypair, mint, treasuryKeypair.publicKey);
        const account = await (0, spl_token_1.getAccount)(connection, treasuryTokenAccount.address);
        treasuryBalance = (0, config_js_1.fromTokenUnits)(account.amount);
    }
    catch (error) {
        return { success: false, error: `Failed to get treasury balance: ${error}` };
    }
    // Calculate distribution amount
    const amount = calculateDistributionAmount(treasuryBalance);
    if (amount === 0) {
        return {
            success: false,
            error: 'Distribution complete - treasury has reached minimum balance',
            treasuryRemaining: treasuryBalance,
        };
    }
    try {
        // Get or create token accounts
        const treasuryTokenAccount = await (0, spl_token_1.getOrCreateAssociatedTokenAccount)(connection, treasuryKeypair, mint, treasuryKeypair.publicKey);
        const claimantTokenAccount = await (0, spl_token_1.getOrCreateAssociatedTokenAccount)(connection, treasuryKeypair, // Treasury pays for account creation
        mint, claimantPubkey);
        // Create transfer instruction
        const transferInstruction = (0, spl_token_1.createTransferInstruction)(treasuryTokenAccount.address, claimantTokenAccount.address, treasuryKeypair.publicKey, (0, config_js_1.toTokenUnits)(amount));
        // Send transaction
        const transaction = new web3_js_1.Transaction().add(transferInstruction);
        const signature = await (0, web3_js_1.sendAndConfirmTransaction)(connection, transaction, [treasuryKeypair]);
        // Record the claim
        saveClaimedAddress(claimantAddress);
        // Update distribution state
        const state = loadDistributionState() || {
            claims: [],
            totalDistributed: 0,
            treasuryAddress: treasuryKeypair.publicKey.toBase58(),
        };
        state.claims.push({
            address: claimantAddress,
            amount,
            timestamp: new Date().toISOString(),
            txSignature: signature,
        });
        state.totalDistributed += amount;
        saveDistributionState(state);
        return {
            success: true,
            amount,
            signature,
            treasuryRemaining: treasuryBalance - amount,
        };
    }
    catch (error) {
        return { success: false, error: `Claim failed: ${error}` };
    }
}
// =============================================================================
// FORMATTING
// =============================================================================
/**
 * Format distribution stats for display
 */
function formatDistributionStats(treasuryBalance) {
    const stats = getDistributionStats();
    const nextAmount = treasuryBalance ? calculateDistributionAmount(treasuryBalance) : null;
    const lines = [
        `📊 ${config_js_1.TOKEN_SYMBOL} Distribution Stats`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        ``,
        `Total Supply: ${stats.totalSupply.toLocaleString()} ${config_js_1.TOKEN_SYMBOL}`,
        `Distribution Rate: 1/${stats.divisor.toLocaleString()} of remaining`,
        ``,
        `Wallets Claimed: ${stats.claimedCount.toLocaleString()}`,
        `Est. Remaining Claims: ~${stats.estimatedRemainingClaims.toLocaleString()}`,
    ];
    if (treasuryBalance !== undefined) {
        lines.push(``);
        lines.push(`Treasury Balance: ${treasuryBalance.toLocaleString()} ${config_js_1.TOKEN_SYMBOL}`);
        if (nextAmount !== null) {
            lines.push(`Next Claim Amount: ${nextAmount.toLocaleString()} ${config_js_1.TOKEN_SYMBOL}`);
        }
    }
    lines.push(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
    return lines.join('\n');
}
/**
 * Format claim result for display
 */
function formatClaimResult(result) {
    if (result.success) {
        return [
            `✅ Claim Successful!`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            `Amount Received: ${result.amount?.toLocaleString()} ${config_js_1.TOKEN_SYMBOL}`,
            `Transaction: ${result.signature}`,
            `Treasury Remaining: ${result.treasuryRemaining?.toLocaleString()} ${config_js_1.TOKEN_SYMBOL}`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            `View on Solscan: https://solscan.io/tx/${result.signature}`,
        ].join('\n');
    }
    else {
        return `❌ Claim Failed: ${result.error}`;
    }
}
/**
 * Simulate distribution to show how amounts decrease over time
 */
function simulateDistribution(numClaims = 20) {
    let remaining = exports.TOTAL_SUPPLY;
    const lines = [
        `📈 Distribution Simulation (first ${numClaims} claims)`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        ``,
        `| Claim # | Amount Received | Treasury Remaining |`,
        `|---------|-----------------|-------------------|`,
    ];
    for (let i = 1; i <= numClaims; i++) {
        const amount = calculateDistributionAmount(remaining);
        if (amount === 0) {
            lines.push(`| ${i.toString().padStart(7)} | Distribution complete |`);
            break;
        }
        remaining -= amount;
        lines.push(`| ${i.toString().padStart(7)} | ${amount.toLocaleString().padStart(15)} | ${remaining.toLocaleString().padStart(17)} |`);
    }
    lines.push(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
    return lines.join('\n');
}
//# sourceMappingURL=distribution.js.map