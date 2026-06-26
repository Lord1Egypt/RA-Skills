const { createWalletClient, createPublicClient, http, parseUnits, parseAbiItem } = require('viem');
const { privateKeyToAccount } = require('viem/accounts');
const { linea } = require('viem/chains');
const { getRpcUrl, getPrivateKey } = require('./config');

const SYT_ADDRESS = "0x060c1cBE54a34deCE77f27ca9955427c0e295Fd4"; //sUSDC Linea

const transferAbi = parseAbiItem('function transfer(address to, uint256 amount) returns (bool)');
const balanceAbi = parseAbiItem('function balanceOf(address account) view returns (uint256)');

async function main() {
    const args = process.argv.slice(2);
    const recipient = args[0];
    const amountStr = args[1];

    if (!recipient || !amountStr) {
        console.error("Usage: node transferSYT.js <recipient_address> <amount>");
        return;
    }

    const account = privateKeyToAccount(getPrivateKey());
    const amountInWei = parseUnits(amountStr, 6); // Assuming USDC 6 decimals

    const publicClient = createPublicClient({ chain: linea, transport: http(getRpcUrl()) });
    const walletClient = createWalletClient({ account, chain: linea, transport: http(getRpcUrl()) });

    console.log(`Preparing to send ${amountStr} sUSDC to ${recipient}...`);

    // 1. Check current balance
    const balance = await publicClient.readContract({
        address: SYT_ADDRESS,
        abi: [balanceAbi],
        functionName: 'balanceOf',
        args: [account.address]
    });

    if (balance < amountInWei) {
        console.error(`Insufficient balance. Current: ${balance.toString()}, Required: ${amountInWei.toString()}`);
        return;
    }

    // 2. Execute Transfer
    const hash = await walletClient.writeContract({
        address: SYT_ADDRESS,
        abi: [transferAbi],
        functionName: 'transfer',
        args: [recipient, amountInWei]
    });

    console.log(`Transaction Hash: ${hash}`);
    await publicClient.waitForTransactionReceipt({ hash });
    console.log("Transfer confirmed.");
    console.log(`\nManage your account: https://autohodl.money (connect the same wallet)`);
}

main().catch(console.error);