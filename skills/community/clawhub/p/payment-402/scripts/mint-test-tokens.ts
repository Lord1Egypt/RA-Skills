#!/usr/bin/env bun
import { ethers } from 'ethers';
import { parseArgs, getPrivateKey, resolveNetwork, reportError, EXIT_CODES } from './utils.ts';

async function main() {
    const args = parseArgs();

    if (args.isHelp) {
        console.log(
            `
Usage: bun run scripts/mint-test-tokens.ts [OPTIONS]

Mints 1,000 Test USDC on the Base Sepolia Testnet.

Options:
  --network <NAME>  Optional. Network to use: testnet/sepolia.
  --rpc <URL>       Optional. Custom RPC URL (must be a Sepolia network).
  --json            Output results in JSON format.
  --help            Show this help message.

Environment:
  CLIENT_PRIVATE_KEY  Required. Must have some Sepolia ETH for gas.

Example:
  bun run scripts/mint-test-tokens.ts --json
`.trim()
        );
        process.exit(EXIT_CODES.SUCCESS);
    }

    const pk = getPrivateKey(args.isJson);

    try {
        const { provider, usdcAddress, chainId, networkName, isSandbox } = await resolveNetwork(
            args.rpcUrl,
            args.network || 'testnet'
        );

        if (!isSandbox) {
            throw new Error(`Minting is only supported on Sepolia. Current ChainID: ${chainId}`);
        }

        const wallet = new ethers.Wallet(pk, provider);

        if (!args.isJson) {
            console.error(`💰 Connecting to ${networkName}...`);
            console.error(`🔗 Minting for address: ${wallet.address}`);
        }

        const abi = ['function mint(address to, uint256 amount) external'];
        const usdc = new ethers.Contract(usdcAddress, abi, wallet);

        const amount = ethers.parseUnits('1000', 6);

        if (!args.isJson) console.error('⏳ Sending mint transaction...');
        const tx = await usdc.mint(wallet.address, amount);

        if (!args.isJson) console.error('⏳ Waiting for confirmation...');
        const receipt = await tx.wait();

        if (receipt.status !== 1) {
            throw new Error('Transaction reverted.');
        }

        if (args.isJson) {
            console.log(
                JSON.stringify(
                    {
                        status: 'success',
                        txHash: tx.hash,
                        address: wallet.address,
                        amount: '1000',
                        token: 'MockUSDC',
                        network: networkName
                    },
                    null,
                    2
                )
            );
        } else {
            console.log(`✅ SUCCESS: You now have 1,000 Test USDC on ${networkName}!`);
        }
    } catch (error: any) {
        reportError(`Minting failed: ${error.message}`, args.isJson, EXIT_CODES.NETWORK_ERROR);
    }
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});
