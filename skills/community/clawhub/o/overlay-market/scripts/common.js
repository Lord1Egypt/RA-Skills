// Shared constants, ABIs, and utilities for Overlay skill scripts.

// Global error handler — catches unhandled rejections and prints structured errors
process.on("unhandledRejection", (err) => {
  const message = err?.shortMessage || err?.cause?.reason || err?.message || String(err);
  console.error(JSON.stringify({ error: message }));
  process.exit(1);
});

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const CACHE_DIR = join(__dirname, "..", ".cache");
const CACHE_TTL = 60 * 60 * 1000; // 1 hour

// ── Contracts (BSC Mainnet) ──────────────────────────────────────────────────

export const CHAIN_ID = 56;

export const CONTRACTS = {
  SHIVA: "0xeB497c228F130BD91E7F13f81c312243961d894A",
  LBSC: "0xb777ef1b4581677a0c764bFBc33c568d00e97DfC",
  STATE: "0x10575a9C8F36F9F42D7DB71Ef179eD9BEf8Df238",
  OVL_USDT_POOL: "0x927aE3c2cd88717a1525a55021AF9612C3F04583",
};

// Token addresses
export const OVL_TOKEN = "0x1F34c87ded863Fe3A3Cd76FAc8adA9608137C8c3";
export const USDT_TOKEN = "0x55d398326f99059fF775485246999027B3197955";

export const MARKETS_API = "https://api.overlay.market/data/api/markets";
export const CHARTS_API = "https://api.overlay.market/bsc-charts/v1/charts";
export const PRICES_API = "https://api.overlay.market/bsc-charts/v1/charts/marketsPricesOverview";
export const SUBGRAPH_URL = "https://api.goldsky.com/api/public/project_clyiptt06ifuv01ul9xiwfj28/subgraphs/overlay-bsc/prod/gn";

// ── ABIs ─────────────────────────────────────────────────────────────────────

export const SHIVA_ABI = [
  {
    inputs: [{
      components: [
        { name: "ovlMarket", type: "address" },
        { name: "brokerId", type: "uint32" },
        { name: "isLong", type: "bool" },
        { name: "stableCollateral", type: "uint256" },
        { name: "leverage", type: "uint256" },
        { name: "priceLimit", type: "uint256" },
        { name: "minOvl", type: "uint256" },
      ],
      name: "params",
      type: "tuple",
    }],
    name: "buildStable",
    outputs: [{ name: "", type: "uint256" }],
    stateMutability: "nonpayable",
    type: "function",
  },
  {
    inputs: [
      {
        components: [
          { name: "ovlMarket", type: "address" },
          { name: "brokerId", type: "uint32" },
          { name: "positionId", type: "uint256" },
          { name: "fraction", type: "uint256" },
          { name: "priceLimit", type: "uint256" },
        ],
        name: "params",
        type: "tuple",
      },
      { name: "swapData", type: "bytes" },
      { name: "minOut", type: "uint256" },
    ],
    name: "unwindStable",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function",
  },
];

export const STATE_ABI = [
  {
    inputs: [{ name: "market", type: "address" }],
    name: "mid",
    outputs: [{ name: "mid_", type: "uint256" }],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [
      { name: "market", type: "address" },
      { name: "owner", type: "address" },
      { name: "id", type: "uint256" },
    ],
    name: "value",
    outputs: [{ name: "", type: "uint256" }],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [
      { name: "market", type: "address" },
      { name: "owner", type: "address" },
      { name: "id", type: "uint256" },
    ],
    name: "tradingFee",
    outputs: [{ name: "", type: "uint256" }],
    stateMutability: "view",
    type: "function",
  },
];

export const POOL_ABI = [
  {
    inputs: [],
    name: "slot0",
    outputs: [
      { name: "sqrtPriceX96", type: "uint160" },
      { name: "tick", type: "int24" },
      { name: "observationIndex", type: "uint16" },
      { name: "observationCardinality", type: "uint16" },
      { name: "observationCardinalityNext", type: "uint16" },
      { name: "feeProtocol", type: "uint8" },
      { name: "unlocked", type: "bool" },
    ],
    stateMutability: "view",
    type: "function",
  },
];

// ── ERC20 ABIs ──────────────────────────────────────────────────────────────

export const ERC20_BALANCE = [{ inputs: [{ name: "account", type: "address" }], name: "balanceOf", outputs: [{ name: "", type: "uint256" }], stateMutability: "view", type: "function" }];
export const ERC20_ALLOWANCE = [{ inputs: [{ name: "owner", type: "address" }, { name: "spender", type: "address" }], name: "allowance", outputs: [{ name: "", type: "uint256" }], stateMutability: "view", type: "function" }];
export const ERC20_APPROVE = [{ inputs: [{ name: "spender", type: "address" }, { name: "amount", type: "uint256" }], name: "approve", outputs: [{ name: "", type: "bool" }], stateMutability: "nonpayable", type: "function" }];

// ── BSC client ───────────────────────────────────────────────────────────────

import { createPublicClient, createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { bsc } from "viem/chains";

const BSC_RPC = process.env.BSC_RPC_URL || "https://bsc-dataseed.binance.org/";

export const publicClient = createPublicClient({
  chain: bsc,
  transport: http(BSC_RPC),
});

export function getAccount() {
  const key = process.env.OVERLAY_PRIVATE_KEY;
  if (!key) return null;
  return privateKeyToAccount(key.startsWith("0x") ? key : `0x${key}`);
}

export function getWalletClient() {
  const account = getAccount();
  if (!account) return null;
  return createWalletClient({ account, chain: bsc, transport: http(BSC_RPC) });
}

// ── Price fetching ────────────────────────────────────────────────────────────

const DEFAULT_SLIPPAGE = 0.01; // 1%
const FETCH_TIMEOUT = 15000; // 15s

export async function fetchWithTimeout(url, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), options.timeout || FETCH_TIMEOUT);
  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    if (!res.ok) {
      const text = await res.text().catch(() => "");
      throw new Error(`HTTP ${res.status}: ${text.slice(0, 200)}`);
    }
    return res;
  } finally {
    clearTimeout(timeout);
  }
}

export async function fetchMidPrice(marketAddress) {
  return publicClient.readContract({
    address: CONTRACTS.STATE,
    abi: STATE_ABI,
    functionName: "mid",
    args: [marketAddress],
  });
}

// OVL price from Uniswap pool (token0=OVL, token1=USDT)
// Uses BigInt arithmetic to avoid Number precision loss on sqrtPriceX96
export async function fetchOvlPrice() {
  const slot0 = await publicClient.readContract({
    address: CONTRACTS.OVL_USDT_POOL,
    abi: POOL_ABI,
    functionName: "slot0",
  });
  const sqrtPriceX96 = slot0[0];
  // price = sqrtPriceX96^2 / 2^192, scaled to 1e18
  const sq = sqrtPriceX96 * sqrtPriceX96;
  const priceE18 = (sq * BigInt(1e18)) >> 192n;
  return priceE18;
}

export function calcPriceLimit(midPrice, isLong, isBuild, slippage = DEFAULT_SLIPPAGE) {
  // Build LONG / Unwind SHORT: accept price up to mid * (1 + slippage)
  // Build SHORT / Unwind LONG: accept price down to mid * (1 - slippage)
  const wantHigh = (isBuild && isLong) || (!isBuild && !isLong);
  if (wantHigh) {
    return midPrice + (midPrice * BigInt(Math.round(slippage * 10000))) / 10000n;
  } else {
    return midPrice - (midPrice * BigInt(Math.round(slippage * 10000))) / 10000n;
  }
}

// ── Cache ────────────────────────────────────────────────────────────────────

function readCache(key) {
  try {
    const raw = readFileSync(join(CACHE_DIR, key + ".json"), "utf-8");
    const { ts, data } = JSON.parse(raw);
    if (Date.now() - ts < CACHE_TTL) return data;
  } catch {}
  return null;
}

function writeCache(key, data) {
  try {
    mkdirSync(CACHE_DIR, { recursive: true });
    writeFileSync(join(CACHE_DIR, key + ".json"), JSON.stringify({ ts: Date.now(), data }));
  } catch {}
}

export async function fetchMarkets() {
  const cached = readCache("markets");
  if (cached) return cached;
  const res = await fetchWithTimeout(MARKETS_API);
  const data = await res.json();
  writeCache("markets", data);
  return data;
}

// ── Market resolution ────────────────────────────────────────────────────────

export async function resolveMarket(query) {
  const marketsRaw = await fetchMarkets();
  const bscMarkets = marketsRaw["56"] || [];

  if (query.startsWith("0x") && query.length === 42) {
    for (const m of bscMarkets) {
      for (const c of m.chains || []) {
        if (String(c.chainId) === "56" && c.deploymentAddress.toLowerCase() === query.toLowerCase()) {
          return { address: query.toLowerCase(), name: m.marketName };
        }
      }
    }
    return { address: query.toLowerCase(), name: query.slice(0, 10) + "..." };
  }

  const q = query.toLowerCase().replace(/[\s\/]+/g, "");
  let best = null;

  for (const m of bscMarkets) {
    const mName = m.marketName.toLowerCase().replace(/[\s\/]+/g, "");
    for (const c of m.chains || []) {
      if (String(c.chainId) !== "56" || c.disabled || c.deprecated) continue;
      if (mName === q) return { address: c.deploymentAddress.toLowerCase(), name: m.marketName };
      if (mName.includes(q) || q.includes(mName)) {
        best = { address: c.deploymentAddress.toLowerCase(), name: m.marketName };
      }
    }
  }

  if (best) return best;

  const available = bscMarkets
    .filter((m) => m.chains.some((c) => String(c.chainId) === "56" && !c.disabled && !c.deprecated))
    .map((m) => m.marketName)
    .sort();
  console.error('Market "' + query + '" not found. Available:');
  available.forEach((n) => console.error("  - " + n));
  process.exit(1);
}

// ── BigInt-safe conversion ────────────────────────────────────────────────────

// Convert an 18-decimal BigInt to a Number without intermediate precision loss.
// Splits into whole and fractional parts so values up to ~9 quadrillion are safe.
export function bigIntToNumber(value, decimals = 18) {
  const divisor = 10n ** BigInt(decimals);
  const whole = value / divisor;
  const frac = value % divisor;
  // Number(whole) is safe up to 2^53; frac/divisor is always < 1
  return Number(whole) + Number(frac) / Number(divisor);
}

// ── Formatting (for charting scripts) ────────────────────────────────────────

export function fmtPrice(n) {
  if (n == null) return "N/A";
  if (Math.abs(n) >= 1000) return n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  if (Math.abs(n) >= 1) return n.toFixed(2);
  if (Math.abs(n) >= 0.0001) return n.toFixed(6);
  return n.toExponential(4);
}

export function fmtPct(p) {
  if (p == null) return "N/A";
  return (p >= 0 ? "+" : "") + p.toFixed(2) + "%";
}

export function padCol(s, len, right) {
  s = String(s);
  if (right) return s.length >= len ? s : s + " ".repeat(len - s.length);
  return s.length >= len ? s : " ".repeat(len - s.length) + s;
}
