/**
 * Kite AI Wallet - Telegram Commands
 * Integrated with OpenClaw messaging
 */

const ethers = require('ethers');

// Configuration
const CONFIG = {
    rpcUrl: 'https://rpc-testnet.gokite.ai',
    factoryAddress: '0x0fa9F878B038DE435b1EFaDA3eed1859a6Dc098a'
};

const FACTORY_ABI = [
    'function createWallet(address agent, uint256 spendingLimit) returns (address)',
    'function getWalletAddress(address owner, address agent) view returns (address)'
];

const WALLET_ABI = [
    'function owner() view returns (address)',
    'function agent() view returns (address)',
    'function spendingLimit() view returns (uint256)',
    'function isSessionKey(address) view returns (bool)',
    'function sessionLimits(address) view returns (uint256)',
    'function addSessionKey(address sessionKey, uint256 limit, bytes4[] functions)',
    'function removeSessionKey(address sessionKey)',
    'function updateSpendingLimit(uint256 newLimit)',
    'function execute(bytes data) payable'
];

// Note: Private key should be set in environment or gateway config
const PRIVATE_KEY = process.env.KITE_WALLET_PRIVATE_KEY;

let provider, wallet, factory;

function init() {
    if (!PRIVATE_KEY) {
        console.log('⚠️ KITE_WALLET_PRIVATE_KEY not set - wallet operations disabled');
        return;
    }
    provider = new ethers.JsonRpcProvider(CONFIG.rpcUrl);
    wallet = new ethers.Wallet(PRIVATE_KEY, provider);
    factory = new ethers.Contract(CONFIG.factoryAddress, FACTORY_ABI, wallet);
    console.log('🤖 Kite Wallet initialized:', wallet.address);
}

function parseCommand(text) {
    const parts = text.trim().split(/\s+/);
    const command = parts[0].toLowerCase();
    const args = parts.slice(1);
    return { command, args };
}

async function getOrCreateWallet(userAddress) {
    if (!factory) return null;
    const agentAddress = userAddress;
    let walletAddress = await factory.getWalletAddress(userAddress, agentAddress);
    
    if (walletAddress === ethers.ZeroAddress) {
        const tx = await factory.createWallet(agentAddress, ethers.parseEther('1'));
        await tx.wait();
        walletAddress = await factory.getWalletAddress(userAddress, agentAddress);
    }
    return walletAddress;
}

async function handleKiteCommand(text, userId) {
    if (!wallet) {
        return '⚠️ Wallet not configured. Ask admin to set KITE_WALLET_PRIVATE_KEY.';
    }
    
    const { command, args } = parseCommand(text);
    
    try {
        switch (command) {
            case '/create': {
                const walletAddress = await getOrCreateWallet(userId);
                return `✅ *Wallet Created!*\n\nAddress: \`${walletAddress}\``;
            }
            case '/wallet': {
                const walletAddress = await factory.getWalletAddress(userId, userId);
                if (walletAddress === ethers.ZeroAddress) return '❌ No wallet. Use /create';
                return `🔗 Wallet: \`${walletAddress}\``;
            }
            case '/balance': {
                let targetAddress = args[0] || await factory.getWalletAddress(userId, userId);
                if (targetAddress === ethers.ZeroAddress) return '❌ No wallet.';
                const balance = await provider.getBalance(targetAddress);
                return `💰 Balance: *${ethers.formatEther(balance)} KITE*`;
            }
            case '/session': {
                const walletAddress = await factory.getWalletAddress(userId, userId);
                if (walletAddress === ethers.ZeroAddress) return '❌ No wallet.';
                
                if (args[0] === 'add') {
                    if (args.length < 3) return '❌ Usage: /session add <addr> <limit>';
                    const sessionKey = args[1];
                    const limit = ethers.parseEther(args[2]);
                    const walletContract = new ethers.Contract(walletAddress, WALLET_ABI, wallet);
                    const tx = await walletContract.addSessionKey(sessionKey, limit, ['0x00000000']);
                    await tx.wait();
                    return `✅ Key added: \`${sessionKey}\`\nLimit: ${args[2]} KITE`;
                }
                return 'Usage: /session add <addr> <limit>';
            }
            case '/limit': {
                const walletAddress = await factory.getWalletAddress(userId, userId);
                if (walletAddress === ethers.ZeroAddress) return '❌ No wallet.';
                
                if (args[0] === 'set') {
                    if (args.length < 2) return '❌ Usage: /limit set <amount>';
                    const newLimit = ethers.parseEther(args[1]);
                    const walletContract = new ethers.Contract(walletAddress, WALLET_ABI, wallet);
                    const tx = await walletContract.updateSpendingLimit(newLimit);
                    await tx.wait();
                    return `✅ Limit: ${args[1]} KITE`;
                }
                const walletContract = new ethers.Contract(walletAddress, WALLET_ABI, provider);
                const limit = await walletContract.spendingLimit();
                return `💰 Limit: *${ethers.formatEther(limit)} KITE*`;
            }
            case '/send': {
                if (args.length < 2) return '❌ Usage: /send <addr> <amount>';
                const toAddress = args[0];
                const amount = ethers.parseEther(args[1]);
                const walletAddress = await factory.getWalletAddress(userId, userId);
                if (walletAddress === ethers.ZeroAddress) return '❌ No wallet.';
                
                const walletContract = new ethers.Contract(walletAddress, WALLET_ABI, wallet);
                const data = ethers.AbiCoder.defaultAbiCoder.encode(
                    ['address', 'uint256', 'bytes'],
                    [toAddress, amount, '0x']
                );
                const tx = await walletContract.execute(data);
                await tx.wait();
                return `✅ Sent ${args[1]} KITE → \`${toAddress}\``;
            }
            case '/help':
                return `📖 *Kite Wallet*

/create - New wallet
/wallet - Your address  
/balance - Check balance
/session add <addr> <limit> - Add key
/limit set <amount> - Set limit
/send <addr> <amount> - Send`;
            default:
                return null;
        }
    } catch (error) {
        return `❌ Error: ${error.message}`;
    }
}

init();

module.exports = {
    handleKiteCommand,
    config: CONFIG
};
