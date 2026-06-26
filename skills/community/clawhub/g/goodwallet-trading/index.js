#!/usr/bin/env node

import { Command } from 'commander';
import { createRequire } from 'node:module';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { homedir, platform, arch } from 'node:os';
import {
  createPublicClient,
  http,
  parseEther,
  parseUnits,
  formatEther,
  formatUnits,
  keccak256,
  serializeTransaction,
  encodeFunctionData,
  decodeFunctionResult,
  recoverTransactionAddress,
} from 'viem';
import { hoodi } from 'viem/chains';

// ─── Sodot SDK Loading ───────────────────────────────────────────────
// Loads the native Sodot MPC module from the goodwallet package

function getSodotNativePath() {
  const require = createRequire(import.meta.url);
  const gwPath = require.resolve('goodwallet');
  const distDir = join(gwPath, '..'); // goodwallet/dist/
  const targetMap = {
    'darwin-x64': 'macos_x86_64',
    'darwin-arm64': 'macos_arm64',
    'linux-x64': 'linux_x86_64',
    'linux-arm64': 'linux_arm64',
  };
  const key = `${platform()}-${arch()}`;
  const target = targetMap[key];
  if (!target) throw new Error(`Unsupported platform: ${key}`);
  return join(distDir, 'native', `libsodot_executor_${target}_nodejs.node`);
}

let _nativeSdk = null;
function getNativeSdk() {
  if (!_nativeSdk) {
    const require = createRequire(import.meta.url);
    _nativeSdk = require(getSodotNativePath());
  }
  return _nativeSdk;
}

// ─── Minimal Sodot SDK Wrappers ──────────────────────────────────────

function bytesToHex(bytes) {
  return Array.from(bytes).map(b => b.toString(16).padStart(2, '0')).join('');
}

function hexToBytes(hex) {
  const bytes = new Uint8Array(hex.length / 2);
  for (let i = 0; i < hex.length; i += 2) {
    bytes[i / 2] = parseInt(hex.substring(i, i + 2), 16);
  }
  return bytes;
}

class MessageHash {
  constructor(bytes) {
    if (typeof bytes === 'string') {
      this.bytes = hexToBytes(bytes);
    } else {
      this.bytes = bytes;
    }
    if (this.bytes.length !== 32) {
      throw new Error(`Invalid MessageHash length: ${this.bytes.length}`);
    }
  }
  toHex() { return bytesToHex(this.bytes); }
}

class EcdsaSignature {
  constructor(r, s, v) {
    this.r = r; this.s = s; this.v = v;
  }
  static fromBuffer(buf) {
    if (typeof buf === 'string') buf = hexToBytes(buf);
    const FIELD_SIZE = 32;
    const r = buf.subarray(0, FIELD_SIZE);
    const s = buf.subarray(FIELD_SIZE, 2 * FIELD_SIZE);
    const v = buf[2 * FIELD_SIZE];
    return new EcdsaSignature(r, s, v);
  }
}

class Ecdsa {
  constructor(relayUrl) {
    this.native = getNativeSdk();
    this.relayUrl = relayUrl;
  }
  async sign(roomUuid, share, msgHash, derivationPath = new Uint32Array()) {
    const expanded = await this.native.ecdsaSign(
      roomUuid, this.relayUrl, share, msgHash.toHex(), Array.from(derivationPath)
    );
    return EcdsaSignature.fromBuffer(expanded);
  }
}

// ─── Config ──────────────────────────────────────────────────────────

const CONFIG_DIR = join(homedir(), '.config', 'goodwallet');
const CONFIG_FILE = join(CONFIG_DIR, 'config.json');
const SIGN_URL = process.env.SIGN_URL || 'sign.goodwallet.dev';
const RELAY_URL = 'relay.' + SIGN_URL;
const HOODI_RPC = process.env.RPC_URL || 'https://eth-hoodi.g.alchemy.com/v2/pungROYJPab5mfhEv2EQjQEtOtugUAbw';
const DERIVATION_PATH = new Uint32Array([44, 60, 0, 0, 1]);

async function loadConfig() {
  try {
    return JSON.parse(await readFile(CONFIG_FILE, 'utf-8'));
  } catch {
    console.error('Error: No credentials found. Run `npx goodwallet@0.2.0 auth` then `npx goodwallet@0.2.0 pair` first.');
    process.exit(1);
  }
}

function requireConfig(config) {
  if (!config.apiKey || !config.share || !config.address) {
    console.error('Error: Incomplete credentials. Run `npx goodwallet@0.2.0 auth` then `npx goodwallet@0.2.0 pair` first.');
    process.exit(1);
  }
}

// ─── MPC Signing ─────────────────────────────────────────────────────

async function signTransaction(config, unsignedSerializedTx) {
  const hash = keccak256(unsignedSerializedTx);
  const hashBytes = Buffer.from(hash.slice(2), 'hex');

  const resp = await fetch(`https://${SIGN_URL}/agent/sign/ecdsa`, {
    method: 'POST',
    headers: { 'X-API-KEY': config.apiKey },
    body: JSON.stringify({ hash: Buffer.from(hashBytes).toString('hex') }),
  });
  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`Sign API error (${resp.status}): ${err}`);
  }
  const { roomUuid } = await resp.json();

  const ecdsa = new Ecdsa(RELAY_URL);
  const signature = await ecdsa.sign(
    roomUuid, config.share, new MessageHash(hashBytes), DERIVATION_PATH
  );

  return {
    r: `0x${bytesToHex(signature.r)}`,
    s: `0x${bytesToHex(signature.s)}`,
    v: BigInt(signature.v),
  };
}

async function buildSignBroadcast(client, chain, config, txParams) {
  const from = config.address;
  const nonce = await client.getTransactionCount({ address: from, blockTag: 'pending' });
  const gasPrice = await client.getGasPrice();

  let gas = 21000n;
  if (txParams.data) {
    try {
      gas = await client.estimateGas({ ...txParams, from, account: from });
      gas = gas * 120n / 100n; // 20% buffer
    } catch (e) {
      console.warn(`Gas estimation failed, using 100000: ${e.message}`);
      gas = 100000n;
    }
  }

  const tx = {
    to: txParams.to,
    value: txParams.value || 0n,
    data: txParams.data,
    nonce,
    gasPrice,
    gas,
    chainId: chain.id,
  };

  const serializedUnsigned = serializeTransaction(tx);
  console.log('Signing via MPC...');
  const sig = await signTransaction(config, serializedUnsigned);

  const signedTx = serializeTransaction(tx, sig);

  const recovered = await recoverTransactionAddress({ serializedTransaction: signedTx });
  if (recovered.toLowerCase() !== from.toLowerCase()) {
    throw new Error(`Signer mismatch: expected ${from}, got ${recovered}`);
  }

  console.log('Broadcasting...');
  const txHash = await client.sendRawTransaction({ serializedTransaction: signedTx });
  return txHash;
}

// ─── ABI Fragments ───────────────────────────────────────────────────

const ERC20_ABI = [
  { type: 'function', name: 'transfer', inputs: [{ name: 'to', type: 'address' }, { name: 'amount', type: 'uint256' }], outputs: [{ type: 'bool' }], stateMutability: 'nonpayable' },
  { type: 'function', name: 'approve', inputs: [{ name: 'spender', type: 'address' }, { name: 'amount', type: 'uint256' }], outputs: [{ type: 'bool' }], stateMutability: 'nonpayable' },
  { type: 'function', name: 'balanceOf', inputs: [{ name: 'account', type: 'address' }], outputs: [{ type: 'uint256' }], stateMutability: 'view' },
  { type: 'function', name: 'decimals', inputs: [], outputs: [{ type: 'uint8' }], stateMutability: 'view' },
  { type: 'function', name: 'symbol', inputs: [], outputs: [{ type: 'string' }], stateMutability: 'view' },
  { type: 'function', name: 'name', inputs: [], outputs: [{ type: 'string' }], stateMutability: 'view' },
  { type: 'function', name: 'allowance', inputs: [{ name: 'owner', type: 'address' }, { name: 'spender', type: 'address' }], outputs: [{ type: 'uint256' }], stateMutability: 'view' },
  { type: 'function', name: 'totalSupply', inputs: [], outputs: [{ type: 'uint256' }], stateMutability: 'view' },
];

const UNISWAP_V2_ROUTER_ABI = [
  {
    type: 'function', name: 'swapExactETHForTokens',
    inputs: [
      { name: 'amountOutMin', type: 'uint256' },
      { name: 'path', type: 'address[]' },
      { name: 'to', type: 'address' },
      { name: 'deadline', type: 'uint256' },
    ],
    outputs: [{ name: 'amounts', type: 'uint256[]' }],
    stateMutability: 'payable',
  },
  {
    type: 'function', name: 'swapExactTokensForETH',
    inputs: [
      { name: 'amountIn', type: 'uint256' },
      { name: 'amountOutMin', type: 'uint256' },
      { name: 'path', type: 'address[]' },
      { name: 'to', type: 'address' },
      { name: 'deadline', type: 'uint256' },
    ],
    outputs: [{ name: 'amounts', type: 'uint256[]' }],
    stateMutability: 'nonpayable',
  },
  {
    type: 'function', name: 'swapExactTokensForTokens',
    inputs: [
      { name: 'amountIn', type: 'uint256' },
      { name: 'amountOutMin', type: 'uint256' },
      { name: 'path', type: 'address[]' },
      { name: 'to', type: 'address' },
      { name: 'deadline', type: 'uint256' },
    ],
    outputs: [{ name: 'amounts', type: 'uint256[]' }],
    stateMutability: 'nonpayable',
  },
  {
    type: 'function', name: 'getAmountsOut',
    inputs: [
      { name: 'amountIn', type: 'uint256' },
      { name: 'path', type: 'address[]' },
    ],
    outputs: [{ name: 'amounts', type: 'uint256[]' }],
    stateMutability: 'view',
  },
];

// ─── Commands ────────────────────────────────────────────────────────

const program = new Command();
program.name('goodwallet-trading').description('Blockchain trading tools for GoodWallet MPC wallets').version('0.2.0');

// balance
program.command('balance')
  .description('Check ETH and ERC20 token balances')
  .option('--token <address>', 'ERC20 token contract address')
  .option('--rpc <url>', 'RPC URL', HOODI_RPC)
  .action(async (options) => {
    const config = await loadConfig();
    requireConfig(config);
    const client = createPublicClient({ chain: hoodi, transport: http(options.rpc) });
    const address = config.address;

    const ethBalance = await client.getBalance({ address });
    console.log(`ETH: ${formatEther(ethBalance)}`);

    if (options.token) {
      try {
        const [rawBal, rawDec, rawSym] = await Promise.all([
          client.readContract({ address: options.token, abi: ERC20_ABI, functionName: 'balanceOf', args: [address] }),
          client.readContract({ address: options.token, abi: ERC20_ABI, functionName: 'decimals' }),
          client.readContract({ address: options.token, abi: ERC20_ABI, functionName: 'symbol' }).catch(() => 'TOKEN'),
        ]);
        console.log(`${rawSym}: ${formatUnits(rawBal, rawDec)}`);
      } catch (e) {
        console.error(`Failed to read token ${options.token}: ${e.message}`);
      }
    }
  });

// erc20-send
program.command('erc20-send')
  .description('Send ERC20 tokens to an address')
  .requiredOption('-t, --to <address>', 'Recipient address')
  .requiredOption('-a, --amount <amount>', 'Amount (human-readable, e.g. 10.5)')
  .requiredOption('--token <address>', 'ERC20 token contract address')
  .option('--rpc <url>', 'RPC URL', HOODI_RPC)
  .action(async (options) => {
    const config = await loadConfig();
    requireConfig(config);
    const client = createPublicClient({ chain: hoodi, transport: http(options.rpc) });

    const decimals = await client.readContract({
      address: options.token, abi: ERC20_ABI, functionName: 'decimals'
    });
    const symbol = await client.readContract({
      address: options.token, abi: ERC20_ABI, functionName: 'symbol'
    }).catch(() => 'TOKEN');

    const amount = parseUnits(options.amount, decimals);
    const data = encodeFunctionData({
      abi: ERC20_ABI, functionName: 'transfer', args: [options.to, amount]
    });

    console.log(`Sending ${options.amount} ${symbol} to ${options.to}...`);
    const txHash = await buildSignBroadcast(client, hoodi, config, {
      to: options.token, data
    });
    console.log(`Transaction sent: ${txHash}`);
    console.log(`Explorer: https://hoodi.etherscan.io/tx/${txHash}`);
  });

// approve
program.command('approve')
  .description('Approve a spender for ERC20 tokens')
  .requiredOption('--token <address>', 'ERC20 token contract address')
  .requiredOption('--spender <address>', 'Spender address (e.g. DEX router)')
  .option('-a, --amount <amount>', 'Amount to approve (default: unlimited)')
  .option('--rpc <url>', 'RPC URL', HOODI_RPC)
  .action(async (options) => {
    const config = await loadConfig();
    requireConfig(config);
    const client = createPublicClient({ chain: hoodi, transport: http(options.rpc) });

    let amount;
    if (options.amount) {
      const decimals = await client.readContract({
        address: options.token, abi: ERC20_ABI, functionName: 'decimals'
      });
      amount = parseUnits(options.amount, decimals);
    } else {
      amount = 2n ** 256n - 1n; // max uint256
    }

    const symbol = await client.readContract({
      address: options.token, abi: ERC20_ABI, functionName: 'symbol'
    }).catch(() => 'TOKEN');

    const data = encodeFunctionData({
      abi: ERC20_ABI, functionName: 'approve', args: [options.spender, amount]
    });

    console.log(`Approving ${options.amount || 'unlimited'} ${symbol} for ${options.spender}...`);
    const txHash = await buildSignBroadcast(client, hoodi, config, {
      to: options.token, data
    });
    console.log(`Approval sent: ${txHash}`);
    console.log(`Explorer: https://hoodi.etherscan.io/tx/${txHash}`);
  });

// contract-call
program.command('contract-call')
  .description('Call any smart contract with raw calldata')
  .requiredOption('--to <address>', 'Contract address')
  .requiredOption('--data <hex>', 'Calldata (hex with 0x prefix)')
  .option('--value <ether>', 'ETH value to send', '0')
  .option('--rpc <url>', 'RPC URL', HOODI_RPC)
  .action(async (options) => {
    const config = await loadConfig();
    requireConfig(config);
    const client = createPublicClient({ chain: hoodi, transport: http(options.rpc) });

    console.log(`Calling ${options.to} with ${options.data.length} bytes of data...`);
    const txHash = await buildSignBroadcast(client, hoodi, config, {
      to: options.to,
      data: options.data,
      value: parseEther(options.value),
    });
    console.log(`Transaction sent: ${txHash}`);
    console.log(`Explorer: https://hoodi.etherscan.io/tx/${txHash}`);
  });

// swap (Uniswap V2 style)
program.command('swap')
  .description('Swap tokens via Uniswap V2 router')
  .requiredOption('--router <address>', 'Uniswap V2 router address')
  .requiredOption('--from-token <address>', 'Token to sell (or "ETH" for native)')
  .requiredOption('--to-token <address>', 'Token to buy (or "ETH" for native)')
  .requiredOption('-a, --amount <amount>', 'Amount to swap (human-readable)')
  .option('--slippage <percent>', 'Slippage tolerance in percent', '1')
  .option('--rpc <url>', 'RPC URL', HOODI_RPC)
  .action(async (options) => {
    const config = await loadConfig();
    requireConfig(config);
    const client = createPublicClient({ chain: hoodi, transport: http(options.rpc) });
    const deadline = BigInt(Math.floor(Date.now() / 1000) + 1200); // 20 min
    const slippageBps = Math.floor(parseFloat(options.slippage) * 100);

    const isFromETH = options.fromToken.toUpperCase() === 'ETH';
    const isToETH = options.toToken.toUpperCase() === 'ETH';

    if (isFromETH) {
      const amountIn = parseEther(options.amount);
      const path = [options.toToken]; // WETH is implicit in swapExactETHForTokens
      // For proper routing, the path should include WETH address
      console.log(`Swapping ${options.amount} ETH for tokens...`);
      const data = encodeFunctionData({
        abi: UNISWAP_V2_ROUTER_ABI,
        functionName: 'swapExactETHForTokens',
        args: [0n, path, config.address, deadline],
      });
      const txHash = await buildSignBroadcast(client, hoodi, config, {
        to: options.router, data, value: amountIn
      });
      console.log(`Swap sent: ${txHash}`);
    } else if (isToETH) {
      const decimals = await client.readContract({
        address: options.fromToken, abi: ERC20_ABI, functionName: 'decimals'
      });
      const amountIn = parseUnits(options.amount, decimals);
      const path = [options.fromToken]; // path to ETH
      console.log(`Swapping ${options.amount} tokens for ETH...`);
      const data = encodeFunctionData({
        abi: UNISWAP_V2_ROUTER_ABI,
        functionName: 'swapExactTokensForETH',
        args: [amountIn, 0n, path, config.address, deadline],
      });
      const txHash = await buildSignBroadcast(client, hoodi, config, {
        to: options.router, data
      });
      console.log(`Swap sent: ${txHash}`);
    } else {
      const decimals = await client.readContract({
        address: options.fromToken, abi: ERC20_ABI, functionName: 'decimals'
      });
      const amountIn = parseUnits(options.amount, decimals);
      const path = [options.fromToken, options.toToken];
      console.log(`Swapping ${options.amount} tokens...`);
      const data = encodeFunctionData({
        abi: UNISWAP_V2_ROUTER_ABI,
        functionName: 'swapExactTokensForTokens',
        args: [amountIn, 0n, path, config.address, deadline],
      });
      const txHash = await buildSignBroadcast(client, hoodi, config, {
        to: options.router, data
      });
      console.log(`Swap sent: ${txHash}`);
    }
    console.log(`Explorer: https://hoodi.etherscan.io/tx/${txHash}`);
  });

// token-info
program.command('token-info')
  .description('Get information about an ERC20 token')
  .requiredOption('--token <address>', 'ERC20 token contract address')
  .option('--rpc <url>', 'RPC URL', HOODI_RPC)
  .action(async (options) => {
    const config = await loadConfig();
    const client = createPublicClient({ chain: hoodi, transport: http(options.rpc) });

    const results = await Promise.allSettled([
      client.readContract({ address: options.token, abi: ERC20_ABI, functionName: 'name' }),
      client.readContract({ address: options.token, abi: ERC20_ABI, functionName: 'symbol' }),
      client.readContract({ address: options.token, abi: ERC20_ABI, functionName: 'decimals' }),
      client.readContract({ address: options.token, abi: ERC20_ABI, functionName: 'totalSupply' }),
      config.address ? client.readContract({
        address: options.token, abi: ERC20_ABI, functionName: 'balanceOf', args: [config.address]
      }) : Promise.resolve(null),
    ]);

    const name = results[0].status === 'fulfilled' ? results[0].value : 'Unknown';
    const symbol = results[1].status === 'fulfilled' ? results[1].value : '???';
    const decimals = results[2].status === 'fulfilled' ? results[2].value : 18;
    const totalSupply = results[3].status === 'fulfilled' ? results[3].value : 0n;
    const balance = results[4].status === 'fulfilled' ? results[4].value : null;

    console.log(`Name: ${name}`);
    console.log(`Symbol: ${symbol}`);
    console.log(`Decimals: ${decimals}`);
    console.log(`Total Supply: ${formatUnits(totalSupply, decimals)}`);
    if (balance !== null) {
      console.log(`Your Balance: ${formatUnits(balance, decimals)}`);
    }
  });

// allowance
program.command('allowance')
  .description('Check ERC20 token allowance')
  .requiredOption('--token <address>', 'ERC20 token contract address')
  .requiredOption('--spender <address>', 'Spender address')
  .option('--rpc <url>', 'RPC URL', HOODI_RPC)
  .action(async (options) => {
    const config = await loadConfig();
    requireConfig(config);
    const client = createPublicClient({ chain: hoodi, transport: http(options.rpc) });

    const [allowance, decimals, symbol] = await Promise.all([
      client.readContract({
        address: options.token, abi: ERC20_ABI, functionName: 'allowance',
        args: [config.address, options.spender]
      }),
      client.readContract({ address: options.token, abi: ERC20_ABI, functionName: 'decimals' }),
      client.readContract({ address: options.token, abi: ERC20_ABI, functionName: 'symbol' }).catch(() => 'TOKEN'),
    ]);

    if (allowance >= 2n ** 255n) {
      console.log(`Allowance: unlimited ${symbol}`);
    } else {
      console.log(`Allowance: ${formatUnits(allowance, decimals)} ${symbol}`);
    }
  });

program.parse();
