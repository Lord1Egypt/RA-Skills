const crypto = require("node:crypto");
const { LinkdropSDK } = require("linkdrop-sdk");
const {
  createPublicClient,
  createWalletClient,
  http,
  parseEther,
  parseUnits,
  isAddress,
} = require("viem");
const { privateKeyToAccount } = require("viem/accounts");
const { polygon, base, arbitrum, optimism, avalanche } = require("viem/chains");

const DEFAULT_LINKDROP_BASE_URL = "https://p2p.linkdrop.io";
const DEFAULT_LINKDROP_API_URL = "https://escrow-api.linkdrop.io/v3";

const CHAIN_CONFIG = {
  polygon: { chain: polygon, chainId: 137 },
  base: { chain: base, chainId: 8453 },
  arbitrum: { chain: arbitrum, chainId: 42161 },
  optimism: { chain: optimism, chainId: 10 },
  avalanche: { chain: avalanche, chainId: 43114 },
};

const SUPPORTED_CHAINS = Object.keys(CHAIN_CONFIG);

const ERC20_DECIMALS_ABI = [
  {
    constant: true,
    inputs: [],
    name: "decimals",
    outputs: [{ name: "", type: "uint8" }],
    payable: false,
    stateMutability: "view",
    type: "function",
  },
];

function serializeError(error) {
  if (error instanceof Error) {
    const details = {};
    if (Object.prototype.hasOwnProperty.call(error, "code")) {
      details.code = error.code;
    }
    if (Object.prototype.hasOwnProperty.call(error, "shortMessage")) {
      details.shortMessage = error.shortMessage;
    }
    if (Object.prototype.hasOwnProperty.call(error, "details")) {
      details.details = error.details;
    }
    if (Object.prototype.hasOwnProperty.call(error, "cause")) {
      details.cause = String(error.cause);
    }
    return {
      name: error.name || "Error",
      message: error.message || "Unknown error",
      ...(Object.keys(details).length ? { details } : {}),
    };
  }

  return {
    name: "Error",
    message: typeof error === "string" ? error : JSON.stringify(error),
  };
}

function normalizePrivateKey(rawPrivateKey) {
  if (!rawPrivateKey || typeof rawPrivateKey !== "string") {
    throw new Error("Missing PRIVATE_KEY");
  }

  const withPrefix = rawPrivateKey.startsWith("0x")
    ? rawPrivateKey
    : `0x${rawPrivateKey}`;

  if (!/^0x[0-9a-fA-F]{64}$/.test(withPrefix)) {
    throw new Error("Invalid PRIVATE_KEY format. Expected 32-byte hex.");
  }

  return withPrefix.toLowerCase();
}

function getRuntimeConfig(env = process.env) {
  const privateKey = normalizePrivateKey(env.PRIVATE_KEY);
  const apiKey = env.LINKDROP_API_KEY;
  if (!apiKey || typeof apiKey !== "string") {
    throw new Error("Missing LINKDROP_API_KEY");
  }
  if (!apiKey.startsWith("zpka_")) {
    throw new Error("Invalid LINKDROP_API_KEY format. Expected prefix 'zpka_'.");
  }

  return {
    privateKey,
    apiKey,
    linkdropBaseUrl: env.LINKDROP_BASE_URL || DEFAULT_LINKDROP_BASE_URL,
    linkdropApiUrl: env.LINKDROP_API_URL || DEFAULT_LINKDROP_API_URL,
  };
}

function resolveChain(chainNameInput) {
  const chainName = String(chainNameInput || "base").toLowerCase();
  const resolved = CHAIN_CONFIG[chainName];
  if (!resolved) {
    throw new Error(
      `Unsupported chain '${chainNameInput}'. Allowed: ${SUPPORTED_CHAINS.join(", ")}.`
    );
  }
  return { chainName, ...resolved };
}

function getAccountFromEnv(env = process.env) {
  const { privateKey } = getRuntimeConfig(env);
  return privateKeyToAccount(privateKey);
}

function createClients({ chainName, chain, privateKey, env = process.env }) {
  const chainRpcEnvKey = `RPC_URL_${chainName.toUpperCase()}`;
  const rpcUrl =
    env[chainRpcEnvKey] ||
    env.RPC_URL ||
    (chain.rpcUrls.default.http && chain.rpcUrls.default.http[0]);

  if (!rpcUrl) {
    throw new Error(`No RPC URL available for chain '${chainName}'.`);
  }

  const account = privateKeyToAccount(privateKey);
  const transport = http(rpcUrl);
  const publicClient = createPublicClient({ chain, transport });
  const walletClient = createWalletClient({ account, chain, transport });

  return { account, publicClient, walletClient, rpcUrl };
}

function createSdk({ apiKey, linkdropBaseUrl, linkdropApiUrl }) {
  return new LinkdropSDK({
    apiKey,
    baseUrl: linkdropBaseUrl,
    apiUrl: linkdropApiUrl,
    getRandomBytes: (length) => crypto.randomBytes(length),
  });
}

function toBigIntOrUndefined(value) {
  if (value === undefined || value === null) {
    return undefined;
  }
  if (typeof value === "bigint") {
    return value;
  }
  if (typeof value === "number") {
    return BigInt(value);
  }
  if (typeof value === "string") {
    if (value.trim() === "") {
      return undefined;
    }
    return BigInt(value);
  }
  return undefined;
}

function createSendTransactionWrapper({ walletClient, account }) {
  return async (tx) => {
    const request = tx || {};
    if (!request.to) {
      throw new Error("sendTransaction requires 'to'");
    }

    const hash = await walletClient.sendTransaction({
      account,
      to: request.to,
      data: request.data || "0x",
      value: toBigIntOrUndefined(request.value),
      gas: toBigIntOrUndefined(request.gas),
      nonce:
        request.nonce !== undefined && request.nonce !== null
          ? Number(request.nonce)
          : undefined,
      maxFeePerGas: toBigIntOrUndefined(request.maxFeePerGas),
      maxPriorityFeePerGas: toBigIntOrUndefined(request.maxPriorityFeePerGas),
    });

    return { hash, type: "tx" };
  };
}

async function parseAmountAtomic({ amountInput, tokenInput, publicClient }) {
  if (!amountInput) {
    throw new Error("Missing amount. Use --amount <decimal>.");
  }

  const normalizedToken = String(tokenInput || "native").toLowerCase();
  if (normalizedToken === "native") {
    return {
      tokenType: "NATIVE",
      tokenAddress: undefined,
      atomicAmount: parseEther(String(amountInput)).toString(),
    };
  }

  if (!isAddress(tokenInput)) {
    throw new Error("Invalid ERC20 token address.");
  }

  const decimalsRaw = await publicClient.readContract({
    address: tokenInput,
    abi: ERC20_DECIMALS_ABI,
    functionName: "decimals",
  });

  const decimals = Number(decimalsRaw);
  if (!Number.isInteger(decimals) || decimals < 0 || decimals > 255) {
    throw new Error("Invalid ERC20 decimals value.");
  }

  return {
    tokenType: "ERC20",
    tokenAddress: tokenInput.toLowerCase(),
    atomicAmount: parseUnits(String(amountInput), decimals).toString(),
  };
}

async function sendClaimableTransfer({
  amount,
  token = "native",
  chain = "base",
  env = process.env,
}) {
  const runtime = getRuntimeConfig(env);
  const { chainName, chain: chainConfig, chainId } = resolveChain(chain);
  const { account, publicClient, walletClient } = createClients({
    chainName,
    chain: chainConfig,
    privateKey: runtime.privateKey,
    env,
  });
  const sdk = createSdk(runtime);

  const { tokenType, tokenAddress, atomicAmount } = await parseAmountAtomic({
    amountInput: amount,
    tokenInput: token,
    publicClient,
  });

  const claimLink = await sdk.createClaimLink({
    from: account.address,
    chainId,
    tokenType,
    token: tokenAddress,
    amount: atomicAmount,
  });

  const sendTransaction = createSendTransactionWrapper({ walletClient, account });
  const depositResult = await claimLink.deposit({ sendTransaction });

  return {
    ok: true,
    chain: chainName,
    chainId,
    sender: account.address,
    tokenType,
    tokenAddress,
    amount,
    atomicAmount,
    claimUrl: depositResult.claimUrl || claimLink.claimUrl,
    transferId: depositResult.transferId || claimLink.transferId,
    depositTx: depositResult.hash,
  };
}

async function claimTransfer({
  claimUrl,
  to,
  chain = "base",
  env = process.env,
}) {
  const runtime = getRuntimeConfig(env);
  const { chainName } = resolveChain(chain);

  if (!claimUrl || typeof claimUrl !== "string") {
    throw new Error("Missing claim URL. Use --url <claimUrl>.");
  }
  if (!to || !isAddress(to)) {
    throw new Error("Invalid destination address. Use --to <0xAddress>.");
  }

  const sdk = createSdk(runtime);
  const claimLink = await sdk.getClaimLink(claimUrl);
  const redeemTx = await claimLink.redeem(to);

  return {
    ok: true,
    chain: chainName,
    to,
    redeemTx,
  };
}

module.exports = {
  CHAIN_CONFIG,
  DEFAULT_LINKDROP_API_URL,
  DEFAULT_LINKDROP_BASE_URL,
  SUPPORTED_CHAINS,
  claimTransfer,
  getAccountFromEnv,
  getRuntimeConfig,
  resolveChain,
  sendClaimableTransfer,
  serializeError,
};
