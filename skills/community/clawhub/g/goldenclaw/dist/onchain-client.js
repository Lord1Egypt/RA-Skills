"use strict";
/**
 * On-Chain Distribution Client
 *
 * TypeScript client for interacting with the CLAW distribution program.
 * This replaces the off-chain distribution logic with on-chain verification.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.DISTRIBUTION_DIVISOR = exports.DISTRIBUTION_PROGRAM_ID = void 0;
exports.getConfigPDA = getConfigPDA;
exports.getTreasuryPDA = getTreasuryPDA;
exports.getClaimRecordPDA = getClaimRecordPDA;
exports.hasClaimedOnChain = hasClaimedOnChain;
exports.getOnChainTreasuryBalance = getOnChainTreasuryBalance;
exports.calculateOnChainClaimAmount = calculateOnChainClaimAmount;
exports.getClaimRecord = getClaimRecord;
exports.getOnChainStats = getOnChainStats;
exports.formatOnChainStatus = formatOnChainStatus;
exports.formatClaimStatus = formatClaimStatus;
const web3_js_1 = require("@solana/web3.js");
const spl_token_1 = require("@solana/spl-token");
const config_js_1 = require("./config.js");
// =============================================================================
// PROGRAM CONSTANTS
// =============================================================================
// Update this after deploying the program!
exports.DISTRIBUTION_PROGRAM_ID = new web3_js_1.PublicKey(process.env.CLAW_DISTRIBUTION_PROGRAM || 'CLAWdist111111111111111111111111111111111111');
// PDA Seeds (must match the Rust program)
const CONFIG_SEED = Buffer.from('config');
const TREASURY_SEED = Buffer.from('treasury');
const CLAIM_RECORD_SEED = Buffer.from('claim');
// Distribution constants (must match Rust program)
exports.DISTRIBUTION_DIVISOR = 1000000n;
// =============================================================================
// PDA DERIVATION
// =============================================================================
/**
 * Get the config PDA address
 */
function getConfigPDA() {
    return web3_js_1.PublicKey.findProgramAddressSync([CONFIG_SEED], exports.DISTRIBUTION_PROGRAM_ID);
}
/**
 * Get the treasury PDA address for a token mint
 */
function getTreasuryPDA(tokenMint) {
    return web3_js_1.PublicKey.findProgramAddressSync([TREASURY_SEED, tokenMint.toBuffer()], exports.DISTRIBUTION_PROGRAM_ID);
}
/**
 * Get the claim record PDA for a user
 */
function getClaimRecordPDA(claimant) {
    return web3_js_1.PublicKey.findProgramAddressSync([CLAIM_RECORD_SEED, claimant.toBuffer()], exports.DISTRIBUTION_PROGRAM_ID);
}
// =============================================================================
// ON-CHAIN QUERIES
// =============================================================================
/**
 * Check if a wallet has already claimed (on-chain verification)
 *
 * This checks if a ClaimRecord PDA exists for the wallet.
 * If it exists, the wallet has claimed.
 */
async function hasClaimedOnChain(walletAddress) {
    const connection = new web3_js_1.Connection(config_js_1.SOLANA_RPC_URL, 'confirmed');
    const wallet = new web3_js_1.PublicKey(walletAddress);
    const [claimRecordPDA] = getClaimRecordPDA(wallet);
    try {
        const accountInfo = await connection.getAccountInfo(claimRecordPDA);
        return accountInfo !== null; // If account exists, they've claimed
    }
    catch {
        return false;
    }
}
/**
 * Get the current treasury balance
 */
async function getOnChainTreasuryBalance() {
    const connection = new web3_js_1.Connection(config_js_1.SOLANA_RPC_URL, 'confirmed');
    const tokenMint = (0, config_js_1.getTokenMint)();
    const [treasuryPDA] = getTreasuryPDA(tokenMint);
    try {
        const treasuryATA = await (0, spl_token_1.getAssociatedTokenAddress)(tokenMint, treasuryPDA, true);
        const balance = await connection.getTokenAccountBalance(treasuryATA);
        return Number(balance.value.amount) / Math.pow(10, balance.value.decimals);
    }
    catch {
        return 0;
    }
}
/**
 * Calculate how much a user would receive if they claimed now
 */
async function calculateOnChainClaimAmount() {
    const treasuryBalance = await getOnChainTreasuryBalance();
    if (treasuryBalance <= 0)
        return 0;
    const claimAmount = treasuryBalance / Number(exports.DISTRIBUTION_DIVISOR);
    return claimAmount;
}
/**
 * Get claim record details for a wallet
 */
async function getClaimRecord(walletAddress) {
    const connection = new web3_js_1.Connection(config_js_1.SOLANA_RPC_URL, 'confirmed');
    const wallet = new web3_js_1.PublicKey(walletAddress);
    const [claimRecordPDA] = getClaimRecordPDA(wallet);
    try {
        const accountInfo = await connection.getAccountInfo(claimRecordPDA);
        if (!accountInfo) {
            return { claimed: false };
        }
        // Parse the account data (ClaimRecord structure)
        // Skip 8 bytes discriminator
        const data = accountInfo.data.slice(8);
        // claimant: Pubkey (32 bytes)
        // amount: u64 (8 bytes)
        // timestamp: i64 (8 bytes)
        // bump: u8 (1 byte)
        const amount = data.readBigUInt64LE(32);
        const timestamp = data.readBigInt64LE(40);
        return {
            claimed: true,
            amount: (0, config_js_1.fromTokenUnits)(amount),
            timestamp: new Date(Number(timestamp) * 1000),
        };
    }
    catch {
        return null;
    }
}
/**
 * Get distribution statistics from the on-chain config
 */
async function getOnChainStats() {
    const connection = new web3_js_1.Connection(config_js_1.SOLANA_RPC_URL, 'confirmed');
    const [configPDA] = getConfigPDA();
    try {
        const accountInfo = await connection.getAccountInfo(configPDA);
        if (!accountInfo) {
            return null;
        }
        // Parse Config structure
        // Skip 8 bytes discriminator
        const data = accountInfo.data.slice(8);
        // authority: Pubkey (32)
        // token_mint: Pubkey (32)
        // treasury: Pubkey (32)
        // total_claims: u64 (8)
        // total_distributed: u64 (8)
        // is_active: bool (1)
        const totalClaims = Number(data.readBigUInt64LE(96));
        const totalDistributed = data.readBigUInt64LE(104);
        const isActive = data.readUInt8(112) === 1;
        const treasuryBalance = await getOnChainTreasuryBalance();
        return {
            totalClaims,
            totalDistributed: (0, config_js_1.fromTokenUnits)(totalDistributed),
            isActive,
            treasuryBalance,
        };
    }
    catch {
        return null;
    }
}
// =============================================================================
// FORMATTING
// =============================================================================
/**
 * Format on-chain distribution status
 */
async function formatOnChainStatus() {
    const stats = await getOnChainStats();
    const claimAmount = await calculateOnChainClaimAmount();
    if (!stats) {
        return [
            `⚠️ On-Chain Program Not Initialized`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            `The CLAW distribution program has not been deployed or initialized.`,
            ``,
            `To use on-chain distribution:`,
            `1. Deploy the program (see programs/claw-distribution/README.md)`,
            `2. Initialize with your CLAW token`,
            `3. Fund the treasury`,
        ].join('\n');
    }
    return [
        `📊 On-Chain Distribution Status`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        ``,
        `Status: ${stats.isActive ? '✅ Active' : '⏸️ Paused'}`,
        ``,
        `Treasury Balance: ${stats.treasuryBalance.toLocaleString()} ${config_js_1.TOKEN_SYMBOL}`,
        `Next Claim Amount: ~${claimAmount.toLocaleString()} ${config_js_1.TOKEN_SYMBOL}`,
        ``,
        `Total Claims: ${stats.totalClaims.toLocaleString()}`,
        `Total Distributed: ${stats.totalDistributed.toLocaleString()} ${config_js_1.TOKEN_SYMBOL}`,
        ``,
        `🔒 Security: Claims verified on-chain via PDA`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
    ].join('\n');
}
/**
 * Format claim status for a specific wallet
 */
async function formatClaimStatus(walletAddress) {
    const record = await getClaimRecord(walletAddress);
    if (!record) {
        return `❌ Could not check claim status for ${walletAddress}`;
    }
    if (record.claimed) {
        return [
            `📋 Claim Record Found`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            `Wallet: ${walletAddress}`,
            `Status: Already Claimed ✅`,
            `Amount: ${record.amount?.toLocaleString()} ${config_js_1.TOKEN_SYMBOL}`,
            `Date: ${record.timestamp?.toLocaleDateString()}`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            ``,
            `This wallet has already received its distribution.`,
            `Each wallet can only claim once (enforced on-chain).`,
        ].join('\n');
    }
    else {
        const claimAmount = await calculateOnChainClaimAmount();
        return [
            `🎁 Eligible to Claim!`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            `Wallet: ${walletAddress}`,
            `Status: Not Yet Claimed`,
            `Estimated Amount: ~${claimAmount.toLocaleString()} ${config_js_1.TOKEN_SYMBOL}`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            ``,
            `Call the claim instruction to receive tokens.`,
        ].join('\n');
    }
}
//# sourceMappingURL=onchain-client.js.map