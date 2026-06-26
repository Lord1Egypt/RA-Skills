const { createWalletClient, createPublicClient, http, parseUnits, parseAbiItem, maxUint256 } = require('viem');
const { privateKeyToAccount } = require('viem/accounts');
const { linea } = require('viem/chains');
const { getRpcUrl, getPrivateKey } = require('./config');

// Constants
const LOCKER_ROUTER = '0xa289AE6ed8336CaB82626c3ff8e5Af334Eb7E0DE'; // Linea Router address
const USDC_LINEA = '0x176211869cA2b568f2A7D4EE941E073a821EE1ff';

// ABI Fragments
const erc20Abi = [
    parseAbiItem('function allowance(address owner, address spender) view returns (uint256)'),
    parseAbiItem('function approve(address spender, uint256 amount) returns (bool)')
];
const depositAbi = parseAbiItem('function deposit(address asset, uint256 amount) external');

async function main() {
    const args = process.argv.slice(2);
    const depositAmount = args[0]; // Amount in USDC (e.g., "10.5")

    if (!depositAmount) {
        console.error("Please provide an amount to deposit.");
        return;
    }

    const account = privateKeyToAccount(getPrivateKey());
    const amountInWei = parseUnits(depositAmount, 6);

    const publicClient = createPublicClient({ chain: linea, transport: http(getRpcUrl()) });
    const walletClient = createWalletClient({ account, chain: linea, transport: http(getRpcUrl()) });

    console.log(`Checking allowance for ${depositAmount} USDC...`);

    // 1. Check Allowance
    const currentAllowance = await publicClient.readContract({
        address: USDC_LINEA,
        abi: erc20Abi,
        functionName: 'allowance',
        args: [account.address, LOCKER_ROUTER]
    });

    // 2. Approve if necessary
    if (currentAllowance < amountInWei) {
        console.log("Allowance insufficient. Sending approval transaction...");
        const approveHash = await walletClient.writeContract({
            address: USDC_LINEA,
            abi: erc20Abi,
            functionName: 'approve',
            args: [LOCKER_ROUTER, maxUint256] // Infinite approval to save gas on future mints
        });
        console.log(`Approval Hash: ${approveHash}`);
        await publicClient.waitForTransactionReceipt({ hash: approveHash });
        console.log("Approval confirmed.");
    } else {
        console.log("Allowance sufficient.");
    }

    // 3. Execute Deposit
    console.log(`Depositing ${depositAmount} USDC into AutoHODL...`);
    const depositHash = await walletClient.writeContract({
        address: LOCKER_ROUTER,
        abi: [depositAbi],
        functionName: 'deposit',
        args: [USDC_LINEA, amountInWei]
    });

    console.log(`Deposit Hash: ${depositHash}`);
    await publicClient.waitForTransactionReceipt({ hash: depositHash });
    console.log("Mint confirmed.");
    console.log(`\nView your savings: https://autohodl.money (connect the same wallet)`);
}

main().catch(console.error);