"use strict";
/**
 * Transaction Module
 *
 * Handles sending CLAW tokens and viewing transaction history.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.sendTokens = sendTokens;
exports.formatSendResult = formatSendResult;
exports.donateSol = donateSol;
exports.formatDonateResult = formatDonateResult;
exports.getTransactionHistory = getTransactionHistory;
exports.formatTransactionHistory = formatTransactionHistory;
exports.getTransaction = getTransaction;
const web3_js_1 = require("@solana/web3.js");
const spl_token_1 = require("@solana/spl-token");
const config_js_1 = require("./config.js");
const wallet_js_1 = require("./wallet.js");
const balance_js_1 = require("./balance.js");
// =============================================================================
// CONNECTION
// =============================================================================
function getConnection() {
    return new web3_js_1.Connection(config_js_1.SOLANA_RPC_URL, 'confirmed');
}
// =============================================================================
// SEND TOKENS
// =============================================================================
/**
 * Send CLAW tokens to another address
 *
 * @param recipientAddress - Destination wallet address
 * @param amount - Amount of CLAW to send
 * @param password - Wallet password for signing
 * @param skipConfirmation - Skip confirmation for amounts above threshold
 */
async function sendTokens(recipientAddress, amount, password, skipConfirmation = false) {
    // Validate configuration
    if (!(0, config_js_1.isConfigured)()) {
        return { success: false, error: 'CLAW token not configured. Set CLAW_TOKEN_MINT first.' };
    }
    // Validate amount
    if (amount <= 0) {
        return { success: false, error: 'Amount must be greater than 0' };
    }
    // Check spending limits
    const limitCheck = (0, wallet_js_1.checkSpendingLimit)(amount);
    if (!limitCheck.allowed) {
        return { success: false, error: limitCheck.reason };
    }
    if (limitCheck.requiresConfirmation && !skipConfirmation) {
        return {
            success: false,
            error: `Amount ${amount} ${config_js_1.TOKEN_SYMBOL} requires confirmation. Call with skipConfirmation=true to proceed.`
        };
    }
    // Validate recipient address
    let recipientPubkey;
    try {
        recipientPubkey = new web3_js_1.PublicKey(recipientAddress);
    }
    catch {
        return { success: false, error: 'Invalid recipient address' };
    }
    // Check SOL balance for fees (need ~0.001 SOL for tx + possible token account rent)
    const MIN_SOL_FOR_FEES = 0.001;
    let balanceInfo;
    try {
        balanceInfo = await (0, balance_js_1.getBalance)();
    }
    catch (e) {
        return { success: false, error: `Could not read wallet balance: ${e instanceof Error ? e.message : 'Unknown error'}` };
    }
    if (balanceInfo.solBalance < MIN_SOL_FOR_FEES) {
        return {
            success: false,
            error: `Insufficient SOL balance for transaction fees. Wallet ${balanceInfo.address} has ${balanceInfo.solBalance.toFixed(6)} SOL; need at least ${MIN_SOL_FOR_FEES} SOL. Check OPENCLAW_DATA_DIR if this is not the wallet you expect.`,
        };
    }
    try {
        // Load wallet
        const keypair = await (0, wallet_js_1.loadWallet)(password);
        const connection = getConnection();
        const mint = (0, config_js_1.getTokenMint)();
        // Get or create sender's token account
        const senderTokenAccount = await (0, spl_token_1.getOrCreateAssociatedTokenAccount)(connection, keypair, mint, keypair.publicKey);
        // Recipient's associated token account address
        const recipientAta = await (0, spl_token_1.getAssociatedTokenAddress)(mint, recipientPubkey);
        // Ensure recipient's token account exists (create in same tx if needed)
        let recipientExists = false;
        try {
            await (0, spl_token_1.getAccount)(connection, recipientAta);
            recipientExists = true;
        }
        catch {
            recipientExists = false;
        }
        // Convert amount to token units
        const amountInUnits = (0, config_js_1.toTokenUnits)(amount);
        const transaction = new web3_js_1.Transaction();
        if (!recipientExists) {
            transaction.add((0, spl_token_1.createAssociatedTokenAccountInstruction)(keypair.publicKey, recipientAta, recipientPubkey, mint));
        }
        transaction.add((0, spl_token_1.createTransferInstruction)(senderTokenAccount.address, recipientAta, keypair.publicKey, amountInUnits));
        const signature = await (0, web3_js_1.sendAndConfirmTransaction)(connection, transaction, [keypair]);
        // Record spending
        (0, wallet_js_1.recordSpending)(amount);
        // Clear keypair from memory
        keypair.secretKey.fill(0);
        return {
            success: true,
            signature,
            amount,
            recipient: recipientAddress,
        };
    }
    catch (error) {
        const errorMessage = formatTransactionError(error);
        return { success: false, error: `Transaction failed: ${errorMessage}` };
    }
}
/**
 * Extract a readable message from Solana/transaction errors (may be Error, object with logs, etc.)
 */
function formatTransactionError(error) {
    if (error instanceof Error) {
        if (error.message)
            return error.message;
        return error.name || 'Unknown error';
    }
    if (error && typeof error === 'object') {
        const o = error;
        if (typeof o.message === 'string' && o.message)
            return o.message;
        if (Array.isArray(o.logs) && o.logs.length)
            return o.logs.slice(-3).join('; ');
        if (o.err)
            return String(o.err);
    }
    return String(error) || 'Unknown error';
}
/**
 * Format send result for display
 */
function formatSendResult(result) {
    if (result.success) {
        return [
            `✅ Transaction Successful!`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            `Amount: ${result.amount} ${config_js_1.TOKEN_SYMBOL}`,
            `To: ${result.recipient}`,
            `Signature: ${result.signature}`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            `View on Solscan: https://solscan.io/tx/${result.signature}`,
        ].join('\n');
    }
    else {
        return `❌ Transaction Failed: ${result.error}`;
    }
}
const MIN_SOL_FEE_LAMPORTS = 5000; // reserve for tx fee
/**
 * Donate SOL to the main wallet (treasury / project).
 */
async function donateSol(amountSol, password) {
    if (amountSol <= 0) {
        return { success: false, error: 'Amount must be greater than 0' };
    }
    let keypair;
    try {
        keypair = await (0, wallet_js_1.loadWallet)(password);
    }
    catch (e) {
        return { success: false, error: e instanceof Error ? e.message : 'Failed to load wallet' };
    }
    // Wallet file is inconsistent: file says one address but decryption produced another (e.g. 1111...).
    const addressFromFile = (0, wallet_js_1.getWalletAddress)();
    const decryptedAddress = keypair.publicKey.toBase58();
    const SYSTEM_PROGRAM_ID = '11111111111111111111111111111111';
    const isWrongKeypair = decryptedAddress === SYSTEM_PROGRAM_ID || (addressFromFile && decryptedAddress !== addressFromFile);
    if (isWrongKeypair) {
        keypair.secretKey.fill(0);
        const walletDir = (0, wallet_js_1.getWalletDirectory)();
        return {
            success: false,
            error: [
                'Invalid wallet: the wallet file does not match the decrypted keypair.',
                '',
                'The file at the path below says address: ' + (addressFromFile || '(none)'),
                'But with your password it decrypts to: ' + decryptedAddress + (decryptedAddress === SYSTEM_PROGRAM_ID ? ' (system program)' : ''),
                '',
                'Wallet folder: ' + walletDir,
                '',
                'Fix (choose one):',
                '  • If you have your 24-word recovery phrase:  gclaw recover "word1 word2 ... word24"',
                '  • If you do not:  gclaw delete   then  gclaw setup   (new wallet; you will need to claim again)',
                '',
                'Use the same password you want for the wallet. After recover or setup, try donate again.',
            ].join('\n'),
        };
    }
    const connection = getConnection();
    const toPubkey = new web3_js_1.PublicKey(config_js_1.GCLAW_DONATE_ADDRESS);
    const lamportsToSend = Math.floor(amountSol * web3_js_1.LAMPORTS_PER_SOL);
    const balanceLamports = await connection.getBalance(keypair.publicKey);
    if (balanceLamports < lamportsToSend + MIN_SOL_FEE_LAMPORTS) {
        const walletAddr = keypair.publicKey.toBase58();
        keypair.secretKey.fill(0);
        const balanceSol = (balanceLamports / web3_js_1.LAMPORTS_PER_SOL).toFixed(6);
        return {
            success: false,
            error: `Insufficient SOL. Wallet ${walletAddr} has ${balanceSol} SOL; need ${amountSol} SOL plus ~0.000005 SOL for fee. Check SOLANA_RPC_URL is mainnet (https://api.mainnet-beta.solana.com) and that this is the wallet you funded. If not, check OPENCLAW_DATA_DIR.`,
        };
    }
    try {
        const tx = new web3_js_1.Transaction().add(web3_js_1.SystemProgram.transfer({
            fromPubkey: keypair.publicKey,
            toPubkey,
            lamports: lamportsToSend,
        }));
        const signature = await (0, web3_js_1.sendAndConfirmTransaction)(connection, tx, [keypair]);
        keypair.secretKey.fill(0);
        return { success: true, signature, amountSol };
    }
    catch (error) {
        keypair.secretKey.fill(0);
        return { success: false, error: `Transaction failed: ${formatTransactionError(error)}` };
    }
}
function formatDonateResult(result) {
    if (result.success) {
        return [
            `✅ Donation Sent!`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            `Amount: ${result.amountSol} SOL`,
            `To: ${config_js_1.GCLAW_DONATE_ADDRESS}`,
            `Signature: ${result.signature}`,
            `━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            `View on Solscan: https://solscan.io/tx/${result.signature}`,
        ].join('\n');
    }
    return `❌ Donation Failed: ${result.error}`;
}
// =============================================================================
// TRANSACTION HISTORY
// =============================================================================
/**
 * Get recent transaction history for the wallet
 *
 * @param limit - Maximum number of transactions to return
 */
async function getTransactionHistory(limit = 10) {
    if (!(0, config_js_1.isConfigured)()) {
        throw new Error('CLAW token not configured');
    }
    const address = (0, wallet_js_1.getWalletAddress)();
    if (!address) {
        throw new Error('No wallet found');
    }
    const connection = getConnection();
    const walletPubkey = new web3_js_1.PublicKey(address);
    const mint = (0, config_js_1.getTokenMint)();
    // Get token account address
    const tokenAccountAddress = await (0, spl_token_1.getAssociatedTokenAddress)(mint, walletPubkey);
    try {
        // Get recent signatures
        const signatures = await connection.getSignaturesForAddress(tokenAccountAddress, { limit });
        // Fetch transaction details
        const transactions = [];
        for (const sig of signatures) {
            try {
                const tx = await connection.getParsedTransaction(sig.signature, { maxSupportedTransactionVersion: 0 });
                if (tx?.meta && tx.blockTime) {
                    // Parse the transaction to determine type and amount
                    const record = parseTransaction(tx, address, tokenAccountAddress.toBase58());
                    if (record) {
                        transactions.push(record);
                    }
                }
            }
            catch {
                // Skip failed transaction parsing
            }
        }
        return transactions;
    }
    catch {
        // Token account might not exist yet
        return [];
    }
}
/**
 * Parse a transaction to extract relevant info
 */
function parseTransaction(tx, walletAddress, tokenAccountAddress) {
    const signature = tx.transaction.signatures[0];
    const timestamp = tx.blockTime ? new Date(tx.blockTime * 1000) : null;
    // Look for token transfer instructions
    const instructions = tx.transaction.message.instructions;
    for (const ix of instructions) {
        // Type guard: check if this is a ParsedInstruction with parsed data
        if (!('parsed' in ix) || !ix.parsed) {
            continue;
        }
        const parsed = ix.parsed;
        if (parsed.type === 'transfer' || parsed.type === 'transferChecked') {
            const info = parsed.info;
            // Extract fields with type assertions
            const source = info.source;
            const destination = info.destination;
            const authority = info.authority;
            // Determine if this is a send or receive
            const isSend = source === tokenAccountAddress || authority === walletAddress;
            const isReceive = destination === tokenAccountAddress;
            // Extract amount
            let amount = 0;
            if (info.amount) {
                amount = (0, config_js_1.fromTokenUnits)(BigInt(info.amount));
            }
            else if (info.tokenAmount && typeof info.tokenAmount === 'object') {
                const tokenAmount = info.tokenAmount;
                if (tokenAmount.amount) {
                    amount = (0, config_js_1.fromTokenUnits)(BigInt(tokenAmount.amount));
                }
            }
            // Determine other party
            let otherParty = 'Unknown';
            if (isSend && destination) {
                otherParty = destination;
            }
            else if (isReceive && source) {
                otherParty = source;
            }
            return {
                signature,
                timestamp,
                type: isSend ? 'send' : isReceive ? 'receive' : 'unknown',
                amount,
                otherParty,
                status: tx.meta?.err ? 'failed' : 'confirmed',
            };
        }
    }
    return null;
}
/**
 * Format transaction history for display
 */
function formatTransactionHistory(transactions) {
    if (transactions.length === 0) {
        return `📜 No transactions found yet.`;
    }
    const lines = [
        `📜 Recent Transactions`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
    ];
    for (const tx of transactions) {
        const icon = tx.type === 'send' ? '📤' : tx.type === 'receive' ? '📥' : '❓';
        const sign = tx.type === 'send' ? '-' : '+';
        const date = tx.timestamp ? tx.timestamp.toLocaleDateString() : 'Unknown';
        const time = tx.timestamp ? tx.timestamp.toLocaleTimeString() : '';
        lines.push(`${icon} ${sign}${tx.amount} ${config_js_1.TOKEN_SYMBOL}`);
        lines.push(`   ${date} ${time}`);
        lines.push(`   ${tx.otherParty.slice(0, 20)}...`);
        lines.push(`   ${tx.signature.slice(0, 20)}...`);
        lines.push(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
    }
    return lines.join('\n');
}
/**
 * Get transaction details by signature
 */
async function getTransaction(signature) {
    const connection = getConnection();
    const address = (0, wallet_js_1.getWalletAddress)();
    if (!address) {
        throw new Error('No wallet found');
    }
    const tx = await connection.getParsedTransaction(signature, { maxSupportedTransactionVersion: 0 });
    if (!tx) {
        return null;
    }
    const tokenAccountAddress = await (0, spl_token_1.getAssociatedTokenAddress)((0, config_js_1.getTokenMint)(), new web3_js_1.PublicKey(address));
    return parseTransaction(tx, address, tokenAccountAddress.toBase58());
}
//# sourceMappingURL=transactions.js.map