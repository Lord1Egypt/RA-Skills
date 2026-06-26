"use strict";
/**
 * Balance Checking Module
 *
 * Handles checking GCLAW token balances and SOL balances (for transaction fees).
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.getTokenAccountAddress = getTokenAccountAddress;
exports.getBalance = getBalance;
exports.getGclawBalance = getGclawBalance;
exports.getSolBalance = getSolBalance;
exports.hasEnoughSolForFees = hasEnoughSolForFees;
exports.formatBalance = formatBalance;
exports.getBalanceForAddress = getBalanceForAddress;
const web3_js_1 = require("@solana/web3.js");
const spl_token_1 = require("@solana/spl-token");
const config_js_1 = require("./config.js");
const wallet_js_1 = require("./wallet.js");
// =============================================================================
// CONNECTION
// =============================================================================
/**
 * Create a Solana connection
 */
function getConnection() {
    return new web3_js_1.Connection(config_js_1.SOLANA_RPC_URL, 'confirmed');
}
// =============================================================================
// BALANCE FUNCTIONS
// =============================================================================
/**
 * Get the associated token account address for a wallet
 */
async function getTokenAccountAddress(walletAddress) {
    const wallet = new web3_js_1.PublicKey(walletAddress);
    const mint = (0, config_js_1.getTokenMint)();
    return (0, spl_token_1.getAssociatedTokenAddress)(mint, wallet);
}
/**
 * Get full balance information for the wallet
 */
async function getBalance() {
    if (!(0, config_js_1.isConfigured)()) {
        throw new Error('GoldenClaw token not configured. Set GCLAW_TOKEN_MINT first.');
    }
    const address = (0, wallet_js_1.getWalletAddress)();
    if (!address) {
        throw new Error('No wallet found. Create a wallet first.');
    }
    const connection = getConnection();
    const walletPubkey = new web3_js_1.PublicKey(address);
    // Get SOL balance
    const solBalance = await connection.getBalance(walletPubkey);
    // Get GCLAW token balance
    let gclawBalance = 0;
    let tokenAccountExists = false;
    try {
        const tokenAccountAddress = await getTokenAccountAddress(address);
        const tokenAccount = await (0, spl_token_1.getAccount)(connection, tokenAccountAddress);
        gclawBalance = (0, config_js_1.fromTokenUnits)(tokenAccount.amount);
        tokenAccountExists = true;
    }
    catch (error) {
        // Token account doesn't exist yet (will be created on first receive)
        // Handle both TokenAccountNotFoundError and generic not found errors
        const errorName = error instanceof Error ? error.constructor.name : '';
        const errorMessage = error instanceof Error ? error.message : '';
        if (errorName === 'TokenAccountNotFoundError' ||
            errorMessage.includes('could not find account') ||
            errorMessage.includes('Account does not exist')) {
            tokenAccountExists = false;
        }
        else {
            throw error;
        }
    }
    return {
        gclawBalance,
        solBalance: solBalance / web3_js_1.LAMPORTS_PER_SOL,
        address,
        tokenAccountExists,
    };
}
/**
 * Get GCLAW balance only (simpler query)
 */
async function getGclawBalance() {
    const balance = await getBalance();
    return balance.gclawBalance;
}
/**
 * Get SOL balance only
 */
async function getSolBalance() {
    const balance = await getBalance();
    return balance.solBalance;
}
/**
 * Check if wallet has enough SOL for transaction fees
 * Solana transactions typically cost ~0.000005 SOL
 */
async function hasEnoughSolForFees(estimatedFee = 0.001) {
    const solBalance = await getSolBalance();
    return solBalance >= estimatedFee;
}
/**
 * Format balance for display
 */
function formatBalance(balance) {
    const lines = [
        `💰 Wallet Balance`,
        `━━━━━━━━━━━━━━━━━━━━━`,
        `${config_js_1.TOKEN_SYMBOL}: ${balance.gclawBalance.toLocaleString(undefined, { maximumFractionDigits: 6 })}`,
        `SOL: ${balance.solBalance.toLocaleString(undefined, { maximumFractionDigits: 9 })} (for fees)`,
        `━━━━━━━━━━━━━━━━━━━━━`,
        `Address: ${balance.address}`,
    ];
    if (!balance.tokenAccountExists) {
        lines.push(`\n⚠️ Token account not yet created. It will be created automatically when you receive ${config_js_1.TOKEN_SYMBOL}.`);
    }
    if (balance.solBalance < 0.001) {
        lines.push(`\n⚠️ Low SOL balance. You need SOL to pay for transaction fees.`);
    }
    return lines.join('\n');
}
/**
 * Get balance for any address (not just own wallet)
 */
async function getBalanceForAddress(address) {
    if (!(0, config_js_1.isConfigured)()) {
        throw new Error('GoldenClaw token not configured. Set GCLAW_TOKEN_MINT first.');
    }
    const connection = getConnection();
    const walletPubkey = new web3_js_1.PublicKey(address);
    // Get SOL balance
    const solBalance = await connection.getBalance(walletPubkey);
    // Get GCLAW token balance
    let gclawBalance = 0;
    let tokenAccountExists = false;
    try {
        const tokenAccountAddress = await getTokenAccountAddress(address);
        const tokenAccount = await (0, spl_token_1.getAccount)(connection, tokenAccountAddress);
        gclawBalance = (0, config_js_1.fromTokenUnits)(tokenAccount.amount);
        tokenAccountExists = true;
    }
    catch {
        tokenAccountExists = false;
    }
    return {
        gclawBalance,
        solBalance: solBalance / web3_js_1.LAMPORTS_PER_SOL,
        address,
        tokenAccountExists,
    };
}
//# sourceMappingURL=balance.js.map