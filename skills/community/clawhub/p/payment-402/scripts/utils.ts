#!/usr/bin/env bun
import { ethers } from 'ethers';
import * as dotenv from 'dotenv';
import {
    PAYNODE_ROUTER_ADDRESS,
    PAYNODE_ROUTER_ADDRESS_SANDBOX,
    BASE_USDC_ADDRESS,
    BASE_USDC_ADDRESS_SANDBOX,
    BASE_RPC_URLS,
    BASE_RPC_URLS_SANDBOX
} from '@paynodelabs/sdk-js';

// Load environment variables
dotenv.config();

/**
 * Note: In Bun's self-contained mode, versioned imports auto-resolve at runtime.
 */

export interface CliConfig {
    isJson: boolean;
    isHelp: boolean;
    isDryRun: boolean;
    rpcUrl?: string;
    network?: string;
    method?: string;
    data?: string;
    headers?: Record<string, string>;
    params: string[];
}

export interface NetworkConfig {
    provider: ethers.JsonRpcProvider;
    chainId: number;
    isSandbox: boolean;
    rpcUrl: string;
    rpcUrls: string[];
    usdcAddress: string;
    routerAddress: string;
    networkName: string;
}

/**
 * Exit codes for agentic use.
 */
export const EXIT_CODES = {
    SUCCESS: 0,
    GENERIC_ERROR: 1,
    INVALID_ARGS: 2,
    AUTH_FAILURE: 3,
    NETWORK_ERROR: 4,
    PAYMENT_REQUIRED: 402 // Specialized exit code for X402 challenges if needed
};

/**
 * Utility to mask sensitive data for logging.
 */
export function maskString(str: string, visiblePrefix = 6, visibleSuffix = 4): string {
    if (!str || str.length <= visiblePrefix + visibleSuffix) return '********';
    return `${str.substring(0, visiblePrefix)}...${str.substring(str.length - visibleSuffix)}`;
}

/**
 * Parses common CLI flags and arguments.
 * Standard format: [OPTIONS] <PARAMS...>
 * Options: --json, --help, --rpc <URL>, --network <name>, --dry-run
 */
export function parseArgs(): CliConfig {
    const args = process.argv.slice(2);
    const config: CliConfig = {
        isJson: false,
        isHelp: false,
        isDryRun: false,
        params: []
    };

    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg === '--json') {
            config.isJson = true;
        } else if (arg === '--help') {
            config.isHelp = true;
        } else if (arg === '--dry-run') {
            config.isDryRun = true;
        } else if (arg === '--rpc') {
            config.rpcUrl = args[++i];
        } else if (arg === '--network') {
            config.network = args[++i];
        } else if (arg === '-X' || arg === '--method') {
            config.method = args[++i];
        } else if (arg === '-d' || arg === '--data') {
            config.data = args[++i];
        } else if (arg === '-H' || arg === '--header') {
            const header = args[++i];
            if (header) {
                const [key, ...valueParts] = header.split(':');
                if (key && valueParts.length > 0) {
                    if (!config.headers) config.headers = {};
                    config.headers[key.trim()] = valueParts.join(':').trim();
                }
            }
        } else if (!arg.startsWith('--')) {
            config.params.push(arg);
        }
    }

    return config;
}

/**
 * Validates existence and format of CLIENT_PRIVATE_KEY.
 */
export function getPrivateKey(isJson: boolean): string {
    const pk = process.env.CLIENT_PRIVATE_KEY;
    if (!pk) {
        reportError('CLIENT_PRIVATE_KEY not found in environment. Check .env file.', isJson, EXIT_CODES.AUTH_FAILURE);
    }
    // Simple format check (0x followed by 64 hex characters)
    const pkRegex = /^0x[0-9a-fA-F]{64}$/;
    if (!pkRegex.test(pk!)) {
        reportError('Invalid CLIENT_PRIVATE_KEY format. Must be a 0x-prefixed 64-character hex string.', isJson, EXIT_CODES.AUTH_FAILURE);
    }
    return pk!;
}

/**
 * Resolves network configuration (Provider and Addresses) based on RPC URL or Network Name.
 */
export async function resolveNetwork(rpcUrl?: string, network?: string): Promise<NetworkConfig> {
    let finalRpcUrls: string[] = [];

    const networkAlias = (network || '').toLowerCase();
    const isTestnetRequest = 
        networkAlias === 'testnet' || 
        networkAlias === 'sepolia' || 
        networkAlias === 'base-sepolia' || 
        networkAlias === '84532' ||
        networkAlias === 'base-testnet';

    if (rpcUrl) {
        finalRpcUrls = [rpcUrl];
    } else {
        if (isTestnetRequest) {
            finalRpcUrls = BASE_RPC_URLS_SANDBOX;
        } else {
            // Default to mainnet if nothing specified or 'mainnet'/'base' passed
            finalRpcUrls = BASE_RPC_URLS;
        }
    }

    const primaryRpc = finalRpcUrls[0];
    let provider: ethers.JsonRpcProvider;

    try {
        provider = new ethers.JsonRpcProvider(primaryRpc, undefined, { staticNetwork: true });
    } catch (e) {
        throw new Error(`Invalid RPC URL format: ${primaryRpc}`);
    }

    let chainId: bigint;
    try {
        const networkInfo = await provider.getNetwork();
        chainId = networkInfo.chainId;
    } catch (error: any) {
        throw new Error(`Failed to connect to RPC (${primaryRpc}): ${error.message}`);
    }

    const isSandbox = chainId === 84532n; // Base Sepolia
    const networkName = isSandbox ? 'Base Sepolia (84532)' : 'Base L2 (8453)';

    return {
        provider,
        chainId: Number(chainId),
        isSandbox,
        rpcUrl: primaryRpc,
        rpcUrls: finalRpcUrls,
        usdcAddress: isSandbox ? BASE_USDC_ADDRESS_SANDBOX : BASE_USDC_ADDRESS,
        routerAddress: isSandbox ? PAYNODE_ROUTER_ADDRESS_SANDBOX : PAYNODE_ROUTER_ADDRESS,
        networkName: networkName
    };
}

/**
 * Standard error reporter.
 */
export function reportError(message: string, isJson: boolean, exitCode: number = EXIT_CODES.GENERIC_ERROR) {
    if (isJson) {
        // Output JSON errors to stdout so agents can decode consistently
        console.log(JSON.stringify({ status: 'error', message, exitCode }));
    } else {
        console.error(`❌ ERROR: ${message} (Exit Code: ${exitCode})`);
    }
    process.exit(exitCode);
}
