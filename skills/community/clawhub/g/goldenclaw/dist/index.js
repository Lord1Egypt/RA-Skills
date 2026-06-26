"use strict";
/**
 * GoldenClaw Skill for OpenClaw
 *
 * A Solana SPL token skill for exchanging services like API tokens and AI compute.
 *
 * Commands:
 *   gclaw setup          - Create a new wallet
 *   gclaw recover        - Recover wallet from seed phrase
 *   gclaw balance        - Check GCLAW and SOL balance
 *   gclaw address        - Show wallet address
 *   gclaw send           - Send GCLAW tokens
 *   gclaw donate         - Donate SOL to main wallet
 *   gclaw history        - View transaction history
 *   gclaw limits         - View spending limits
 *   gclaw claim          - Claim tokens from distribution
 *   gclaw tokenomics     - View distribution stats
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.SPENDING_LIMITS = exports.NETWORK_NAME = exports.TOKEN_NAME = exports.TOKEN_SYMBOL = exports.isConfigured = exports.simulateDistribution = exports.getDistributionStats = exports.hasAlreadyClaimed = exports.calculateDistributionAmount = exports.DISTRIBUTION_DIVISOR = exports.TOTAL_SUPPLY = exports.formatTransactionHistory = exports.formatSendResult = exports.getTransactionHistory = exports.formatDonateResult = exports.donateSol = exports.sendTokens = exports.formatBalance = exports.getBalance = exports.deleteWallet = exports.getWalletAddress = exports.walletExists = exports.loadWallet = exports.recoverWallet = exports.createWallet = exports.skillMetadata = void 0;
exports.handleCommand = handleCommand;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const child_process_1 = require("child_process");
const skillRoot = path_1.default.join(__dirname, '..');
if (!fs_1.default.existsSync(path_1.default.join(skillRoot, 'node_modules'))) {
    console.log('Installing dependencies...');
    (0, child_process_1.execSync)('npm install', { cwd: skillRoot, stdio: 'inherit' });
}
// Load skill modules (after install so node_modules exists)
const { createWallet, recoverWallet, loadWallet, walletExists, getWalletAddress, checkSpendingLimit, getRemainingDailyAllowance, deleteWallet, } = require('./wallet.js');
exports.createWallet = createWallet;
exports.recoverWallet = recoverWallet;
exports.loadWallet = loadWallet;
exports.walletExists = walletExists;
exports.getWalletAddress = getWalletAddress;
exports.deleteWallet = deleteWallet;
const { getBalance, formatBalance } = require('./balance.js');
exports.getBalance = getBalance;
exports.formatBalance = formatBalance;
const { sendTokens, formatSendResult, donateSol, formatDonateResult, getTransactionHistory, formatTransactionHistory, } = require('./transactions.js');
exports.sendTokens = sendTokens;
exports.formatSendResult = formatSendResult;
exports.donateSol = donateSol;
exports.formatDonateResult = formatDonateResult;
exports.getTransactionHistory = getTransactionHistory;
exports.formatTransactionHistory = formatTransactionHistory;
const { TOKEN_SYMBOL, TOKEN_NAME, NETWORK_NAME, SPENDING_LIMITS, isConfigured, GCLAW_TOKEN_MINT, GCLAW_FAUCET_URL, GCLAW_DONATE_ADDRESS, } = require('./config.js');
exports.TOKEN_SYMBOL = TOKEN_SYMBOL;
exports.TOKEN_NAME = TOKEN_NAME;
exports.NETWORK_NAME = NETWORK_NAME;
exports.SPENDING_LIMITS = SPENDING_LIMITS;
exports.isConfigured = isConfigured;
const { TOTAL_SUPPLY, DISTRIBUTION_DIVISOR, calculateDistributionAmount, hasAlreadyClaimed, getDistributionStats, formatDistributionStats, simulateDistribution, saveClaimedAddress, formatClaimResult, } = require('./distribution.js');
exports.TOTAL_SUPPLY = TOTAL_SUPPLY;
exports.DISTRIBUTION_DIVISOR = DISTRIBUTION_DIVISOR;
exports.calculateDistributionAmount = calculateDistributionAmount;
exports.hasAlreadyClaimed = hasAlreadyClaimed;
exports.getDistributionStats = getDistributionStats;
exports.simulateDistribution = simulateDistribution;
// =============================================================================
// SKILL METADATA
// =============================================================================
exports.skillMetadata = {
    name: 'goldenclaw',
    version: '1.1.0',
    description: `Manage ${TOKEN_NAME} (${TOKEN_SYMBOL}) on Solana for exchanging services`,
    commands: ['gclaw'],
    author: 'MoltBotCrypto',
};
// =============================================================================
// COMMAND HANDLERS
// =============================================================================
/**
 * Main command handler for the skill
 */
async function handleCommand(command, args, context) {
    const subcommand = args[0]?.toLowerCase() || 'help';
    try {
        switch (subcommand) {
            case 'setup':
                return await handleSetup(context.password);
            case 'recover':
                return await handleRecover(args.slice(1).join(' '), context.password);
            case 'balance':
            case 'bal':
                return await handleBalance();
            case 'address':
            case 'addr':
                return handleAddress();
            case 'send':
                return await handleSend(args[1], args[2], context.password, context.confirm);
            case 'donate':
                return await handleDonate(args[1], context.password);
            case 'history':
            case 'hist':
                return await handleHistory(parseInt(args[1]) || 10);
            case 'limits':
                return handleLimits();
            case 'status':
                return handleStatus();
            case 'delete':
                return handleDelete(context.confirm);
            case 'claim':
                return await handleClaim();
            case 'tokenomics':
            case 'distribution':
            case 'dist':
                return handleTokenomics();
            case 'simulate':
                return handleSimulate(parseInt(args[1]) || 20);
            case 'help':
            default:
                return getHelpText();
        }
    }
    catch (error) {
        const message = error instanceof Error ? error.message : 'Unknown error';
        return `❌ Error: ${message}`;
    }
}
// =============================================================================
// INDIVIDUAL COMMAND HANDLERS
// =============================================================================
async function handleSetup(password) {
    if (walletExists()) {
        return `⚠️ Wallet already exists. Use 'gclaw address' to see your address or 'gclaw delete' to remove it.`;
    }
    if (!password) {
        return `❌ Password required. Please provide a password to encrypt your wallet.`;
    }
    const result = await createWallet(password);
    return [
        `✅ Wallet Created Successfully!`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        ``,
        `📍 Your Address:`,
        `${result.address}`,
        ``,
        `🔑 BACKUP SEED PHRASE (SAVE THIS!)`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        `${result.mnemonic}`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        ``,
        `⚠️ IMPORTANT:`,
        `• Write down these 24 words and store them safely`,
        `• This seed phrase is Phantom-compatible — restore it in Phantom for the same address`,
        `• Never share your seed phrase with anyone`,
        `• This message will not be shown again`,
        ``,
        `Next steps:`,
        `1. Send some SOL to your address for transaction fees`,
        `2. Send or receive ${TOKEN_SYMBOL} tokens`,
        `3. Use 'gclaw balance' to check your balance`,
    ].join('\n');
}
async function handleRecover(mnemonic, password) {
    if (!mnemonic || mnemonic.split(' ').length < 12) {
        return `❌ Please provide your 24-word seed phrase: claw recover <seed phrase>`;
    }
    if (!password) {
        return `❌ Password required to encrypt the recovered wallet.`;
    }
    if (walletExists()) {
        return `⚠️ Wallet already exists. Delete it first with 'gclaw delete' if you want to recover a different wallet.`;
    }
    const result = await recoverWallet(mnemonic.trim(), password);
    return [
        `✅ Wallet Recovered Successfully!`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        `Address: ${result.address}`,
        ``,
        `Your wallet has been restored. Same address in GCLAW and Phantom.`,
        `Use 'gclaw balance' to check your balance.`,
    ].join('\n');
}
async function handleBalance() {
    if (!walletExists()) {
        return `❌ No wallet found. Use 'gclaw setup' to create one.`;
    }
    if (!isConfigured()) {
        return `⚠️ ${TOKEN_SYMBOL} token not configured yet.`;
    }
    const balance = await getBalance();
    return formatBalance(balance);
}
function handleAddress() {
    const address = getWalletAddress();
    if (!address) {
        return `❌ No wallet found. Use 'gclaw setup' to create one.`;
    }
    return [
        `📍 Your ${TOKEN_SYMBOL} Wallet Address`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        `${address}`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        ``,
        `Share this address to receive ${TOKEN_SYMBOL} tokens.`,
        `Network: ${NETWORK_NAME}`,
    ].join('\n');
}
async function handleSend(amount, recipient, password, confirm) {
    if (!amount || !recipient) {
        return `❌ Usage: claw send <amount> <recipient_address>`;
    }
    if (!password) {
        return `❌ Password required to sign the transaction.`;
    }
    const amountNum = parseFloat(amount);
    if (isNaN(amountNum) || amountNum <= 0) {
        return `❌ Invalid amount: ${amount}`;
    }
    // Check limits before attempting
    const limitCheck = checkSpendingLimit(amountNum);
    if (!limitCheck.allowed) {
        return `❌ ${limitCheck.reason}`;
    }
    if (limitCheck.requiresConfirmation && !confirm) {
        return [
            `⚠️ Confirmation Required`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            `Amount: ${amountNum} ${TOKEN_SYMBOL}`,
            `To: ${recipient}`,
            ``,
            `This amount exceeds the confirmation threshold (${SPENDING_LIMITS.confirmationThreshold} ${TOKEN_SYMBOL}).`,
            `Please confirm this transaction.`,
        ].join('\n');
    }
    const result = await sendTokens(recipient, amountNum, password, confirm || false);
    return formatSendResult(result);
}
async function handleDonate(amountStr, password) {
    if (!amountStr) {
        return [
            `🩵 Donate SOL`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            ``,
            `Send SOL to the GoldenClaw main wallet (treasury).`,
            ``,
            `Usage: gclaw donate <amount_in_SOL>`,
            `Example: gclaw donate 0.01`,
            ``,
            `Recipient: ${GCLAW_DONATE_ADDRESS}`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        ].join('\n');
    }
    if (!password) {
        return `❌ Password required to sign the transaction.`;
    }
    const amount = parseFloat(amountStr);
    if (isNaN(amount) || amount <= 0) {
        return `❌ Invalid amount. Use a positive number, e.g. 0.01`;
    }
    const result = await donateSol(amount, password);
    return formatDonateResult(result);
}
async function handleHistory(limit) {
    if (!walletExists()) {
        return `❌ No wallet found. Use 'gclaw setup' to create one.`;
    }
    const transactions = await getTransactionHistory(limit);
    return formatTransactionHistory(transactions);
}
function handleLimits() {
    const remaining = getRemainingDailyAllowance();
    return [
        `🔒 Spending Limits`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        `Per Transaction: ${SPENDING_LIMITS.perTransaction} ${TOKEN_SYMBOL}`,
        `Daily Limit: ${SPENDING_LIMITS.daily} ${TOKEN_SYMBOL}`,
        `Confirmation Threshold: ${SPENDING_LIMITS.confirmationThreshold} ${TOKEN_SYMBOL}`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        `Remaining Today: ${remaining} ${TOKEN_SYMBOL}`,
        ``,
        `Set custom limits via environment variables:`,
        `• GCLAW_TX_LIMIT - Per transaction limit`,
        `• GCLAW_DAILY_LIMIT - Daily limit`,
        `• GCLAW_CONFIRM_THRESHOLD - Confirmation threshold`,
    ].join('\n');
}
function handleStatus() {
    const configured = isConfigured();
    const hasWallet = walletExists();
    const address = getWalletAddress();
    return [
        `📊 ${TOKEN_NAME} Skill Status`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        `Token Configured: ${configured ? '✅' : '❌'}`,
        `Network: ${NETWORK_NAME}`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        `Wallet Created: ${hasWallet ? '✅' : '❌'}`,
        `Wallet Address: ${address || 'N/A'}`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        ``,
        configured && hasWallet
            ? `✅ Ready to use! Try 'gclaw balance' or 'gclaw send'.`
            : !configured
                ? `⚠️ Token not configured. Check config.`
                : `⚠️ Use 'gclaw setup' to create a wallet.`,
    ].join('\n');
}
function handleDelete(confirm) {
    if (!walletExists()) {
        return `❌ No wallet to delete.`;
    }
    if (!confirm) {
        return [
            `⚠️ WARNING: This will permanently delete your wallet!`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            `Make sure you have backed up your seed phrase.`,
            `This action cannot be undone.`,
            ``,
            `To confirm, run with confirmation flag.`,
        ].join('\n');
    }
    deleteWallet();
    return [
        `✅ Wallet Deleted`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        `Your wallet has been securely deleted.`,
        `Use 'gclaw setup' to create a new wallet.`,
    ].join('\n');
}
async function handleClaim() {
    if (!walletExists()) {
        return `❌ No wallet found. Use 'gclaw setup' to create one first.`;
    }
    const address = getWalletAddress();
    if (!address) {
        return `❌ Could not get wallet address.`;
    }
    // Check if already claimed (local cache; server is source of truth)
    if (hasAlreadyClaimed(address)) {
        return [
            `⚠️ Already Claimed`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            `This wallet has already claimed ${TOKEN_SYMBOL} tokens.`,
            `Each wallet can only claim once.`,
            ``,
            `Use 'gclaw tokenomics' to view distribution stats.`,
        ].join('\n');
    }
    // Call faucet API (goldenclaw.org)
    const faucetUrl = GCLAW_FAUCET_URL.replace(/\/$/, '');
    try {
        const res = await fetch(`${faucetUrl}/api/claim`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ address }),
        });
        const data = (await res.json());
        if (res.ok && data.success) {
            saveClaimedAddress(address);
            const result = {
                success: true,
                amount: data.amount,
                signature: data.txSignature,
                treasuryRemaining: data.treasuryRemaining,
            };
            return formatClaimResult(result);
        }
        // 400 or error payload
        const errorMsg = data.error || (res.status === 400 ? 'Claim failed' : `Faucet returned ${res.status}`);
        return [
            `❌ Claim Failed`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            errorMsg,
            ``,
            `Faucet: ${faucetUrl}`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        ].join('\n');
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : 'Network error';
        return [
            `❌ Faucet Unavailable`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            `Could not reach the claim server: ${msg}`,
            ``,
            `Faucet: ${faucetUrl}`,
            `Try again later or check https://goldenclaw.org`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        ].join('\n');
    }
}
function handleTokenomics() {
    const stats = getDistributionStats();
    // Calculate estimated treasury based on claims
    const estimatedTreasury = TOTAL_SUPPLY * Math.pow((DISTRIBUTION_DIVISOR - 1) / DISTRIBUTION_DIVISOR, stats.claimedCount);
    const nextClaimAmount = calculateDistributionAmount(estimatedTreasury);
    return [
        `📊 ${TOKEN_SYMBOL} Tokenomics`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        ``,
        `📈 Supply`,
        `   Total Supply: ${TOTAL_SUPPLY.toLocaleString()} ${TOKEN_SYMBOL}`,
        `   Fixed: Yes (no minting after creation)`,
        ``,
        `🎁 Distribution Model`,
        `   Each new wallet receives: 1/${DISTRIBUTION_DIVISOR.toLocaleString()} of treasury`,
        `   Distribution ends when: Treasury < 0.000001 ${TOKEN_SYMBOL}`,
        ``,
        `📊 Current Status`,
        `   Wallets claimed: ${stats.claimedCount.toLocaleString()}`,
        `   Est. treasury remaining: ~${estimatedTreasury.toLocaleString()} ${TOKEN_SYMBOL}`,
        `   Next claim amount: ~${nextClaimAmount.toLocaleString()} ${TOKEN_SYMBOL}`,
        `   Est. remaining claims: ~${stats.estimatedRemainingClaims.toLocaleString()}`,
        ``,
        `💡 Use 'gclaw simulate [n]' to see distribution preview`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
    ].join('\n');
}
function handleSimulate(numClaims) {
    return simulateDistribution(Math.min(numClaims, 100));
}
function getHelpText() {
    return [
        `🦞 ${TOKEN_NAME} (${TOKEN_SYMBOL}) - OpenClaw Skill`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        ``,
        `Exchange services like API tokens and AI compute`,
        `using ${TOKEN_SYMBOL} on the Solana blockchain.`,
        ``,
        `Wallet Commands:`,
        `  gclaw setup              Create a new wallet`,
        `  gclaw recover <phrase>   Recover from seed phrase (Phantom-compatible)`,
        `  gclaw balance            Check your balance`,
        `  gclaw address            Show wallet address`,
        `  gclaw delete             Delete wallet (caution!)`,
        ``,
        `Transaction Commands:`,
        `  gclaw send <amt> <addr>  Send ${TOKEN_SYMBOL} tokens`,
        `  gclaw donate <SOL>       Donate SOL to main wallet`,
        `  gclaw history [n]        View last n transactions`,
        `  gclaw limits             View spending limits`,
        ``,
        `Distribution Commands:`,
        `  gclaw claim              Claim tokens (new wallets)`,
        `  gclaw tokenomics         View distribution stats`,
        `  gclaw simulate [n]       Preview first n distributions`,
        ``,
        `Other:`,
        `  gclaw status             Check configuration status`,
        `  gclaw help               Show this help`,
        ``,
        `Links:`,
        `  Website: https://goldenclaw.org`,
        `  X: https://x.com/GClaw68175`,
        `  Community: https://moltbook.com`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
    ].join('\n');
}
// Default export for OpenClaw skill system
exports.default = {
    metadata: exports.skillMetadata,
    handleCommand,
};
//# sourceMappingURL=index.js.map