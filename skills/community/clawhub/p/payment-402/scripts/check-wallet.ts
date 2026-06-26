#!/usr/bin/env bun
import { ethers } from 'ethers';
import { parseArgs, getPrivateKey, resolveNetwork, reportError, EXIT_CODES } from './utils.ts';

async function main() {
    const args = parseArgs();

    if (args.isHelp) {
        console.log(
            `
Usage: bun run scripts/check-wallet.ts [OPTIONS]

Checks the wallet balance (ETH and USDC) on Base L2.

Options:
  --network <NAME>  Optional. Network to use: mainnet or testnet/sepolia.
  --rpc <URL>       Optional. Custom RPC URL for the network.
  --json            Output results in JSON format.
  --help            Show this help message.

Environment:
  CLIENT_PRIVATE_KEY  Required. 64-character hex string starting with 0x.

Example:
  bun run scripts/check-wallet.ts --network testnet --json
`.trim()
        );
        process.exit(EXIT_CODES.SUCCESS);
    }

    const pk = getPrivateKey(args.isJson);

    try {
        const { provider, usdcAddress, chainId, networkName, isSandbox } = await resolveNetwork(
            args.rpcUrl,
            args.network
        );
        const wallet = new ethers.Wallet(pk, provider);
        const address = wallet.address;

        const [ethBalance, usdcBalance] = await Promise.all([
            provider.getBalance(address),
            new ethers.Contract(
                usdcAddress,
                ['function balanceOf(address) view returns (uint256)'],
                provider
            ).balanceOf(address)
        ]);

        const ethValue = parseFloat(ethers.formatEther(ethBalance));
        const usdcValue = parseFloat(ethers.formatUnits(usdcBalance, 6));

        // Thresholds
        const isGasReady = ethValue >= 0.001;
        const isTokensReady = usdcValue > 0;

        if (args.isJson) {
            console.log(
                JSON.stringify(
                    {
                        status: 'success',
                        address: address,
                        eth: ethValue,
                        usdc: usdcValue,
                        network: networkName,
                        chainId: chainId,
                        is_sandbox: isSandbox,
                        checks: {
                            gas_ready: isGasReady,
                            tokens_ready: isTokensReady,
                            can_pay: isGasReady && isTokensReady
                        }
                    },
                    null,
                    2
                )
            );
        } else {
            console.log(`\n### 💳 Wallet Status (${networkName})`);
            console.log(`| Attribute | Value | Status |`);
            console.log(`| :--- | :--- | :--- |`);
            console.log(`| **Address** | \`${address}\` | - |`);
            console.log(`| **ETH (Gas)** | ${ethValue.toFixed(6)} ETH | ${isGasReady ? '✅ Ready' : '⚠️ Low'} |`);
            console.log(`| **USDC** | ${usdcValue.toFixed(2)} USDC | ${isTokensReady ? '✅ Ready' : '⚠️ Empty'} |`);

            if (!isGasReady) {
                console.warn(
                    `\n> [!WARNING]\n> Gas balance is critically low (< 0.001 ETH). Please deposit ETH to \`${address}\`.`
                );
            }
            if (!isTokensReady && !isSandbox) {
                console.warn(
                    `\n> [!NOTE]\n> USDC balance is 0. If this is a test, use \`scripts/mint-test-tokens.ts\` on Sepolia.`
                );
            }
        }
    } catch (error: any) {
        reportError(`Network Error: ${error.message}`, args.isJson, EXIT_CODES.NETWORK_ERROR);
    }
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});
