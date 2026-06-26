import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

import { getAddress, isAddress, isHex, zeroAddress } from "viem";
import { privateKeyToAccount } from "viem/accounts";

export type RuntimeConfig = {
  rpcUrl: string;
  coreAddress: `0x${string}`;
  councilAddress: `0x${string}`;
  predictionAddress: `0x${string}`;
  walletAddress?: `0x${string}`;
};

const DEFAULT_RPC_URL = "https://base-mainnet.g.alchemy.com/v2/JJnstbeYnuQz5s8Rbn91V";
export const DEFAULT_CORE_ADDRESS = "0xfeBB259e83Bb133E87Ee85A48DC205c8043B3A99" as `0x${string}`;
export const DEFAULT_COUNCIL_ADDRESS = "0x545e8f8d77dC3FAA74cee11572Dc4BAF35c6Ca0d" as `0x${string}`;
export const DEFAULT_PREDICTION_ADDRESS = "0xE348e71B3D9b8e0420E74a3FB1Ec022b80a27F83" as `0x${string}`;
export const DEFAULT_IDENTITY_ADDRESS = "0xb16aA007A5F0C6dE1A69D0D81412BA6d77c685Ab" as `0x${string}`;
export const DEFAULT_VAULT_ADDRESS = "0x372290907d22544cfa0f75dfe1FCE0eBfcE18cd2" as `0x${string}`;

export const PAYMASTER_URL = "https://api.pimlico.io/v2/8453/rpc?apikey=pim_2V2Kb734c4mRdagDnBGdHc";

// ── API constants (operator-configured, not user-facing) ─────────────────────
export const API_URL = "https://eplsuascoclomzejttgz.supabase.co";
export const API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVwbHN1YXNjb2Nsb216ZWp0dGd6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU5Mjg1MTMsImV4cCI6MjA5MTUwNDUxM30.pOErf06RIzzs6eRmtRXVrefoC1oyjY2agbLaHK-MbcQ";
const CONFIG_DIR = path.join(os.homedir(), ".moltx");
const CONFIG_PATH = path.join(CONFIG_DIR, "config.json");

const DEFAULT_CONFIG: RuntimeConfig = {
  rpcUrl: DEFAULT_RPC_URL,
  coreAddress: DEFAULT_CORE_ADDRESS,
  councilAddress: DEFAULT_COUNCIL_ADDRESS,
  predictionAddress: DEFAULT_PREDICTION_ADDRESS,
};
 
function ensureConfigDir(): void {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
}

function parseAddress(
  value: unknown,
  key: string,
): `0x${string}` | undefined {
  if (value === undefined || value === null || value === "") {
    return undefined;
  }
  if (typeof value !== "string" || !isAddress(value)) {
    throw new Error(`${key} must be a valid address`);
  }

  return getAddress(value);
}

function normalizeRuntimeConfig(value: unknown): RuntimeConfig {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new Error("runtime config must be a JSON object");
  }

  const record = value as Record<string, unknown>;
  const rpcUrl = typeof record.rpcUrl === "string" && record.rpcUrl.trim() !== ""
    ? record.rpcUrl
    : DEFAULT_RPC_URL;
  const coreAddress =
    parseAddress(record.coreAddress ?? DEFAULT_CORE_ADDRESS, "coreAddress") ??
    DEFAULT_CORE_ADDRESS;

  return {
    rpcUrl,
    coreAddress,
    councilAddress:
      parseAddress(record.councilAddress ?? DEFAULT_COUNCIL_ADDRESS, "councilAddress") ??
      DEFAULT_COUNCIL_ADDRESS,
    predictionAddress:
      parseAddress(record.predictionAddress ?? DEFAULT_PREDICTION_ADDRESS, "predictionAddress") ??
      DEFAULT_PREDICTION_ADDRESS,
    walletAddress: parseAddress(record.walletAddress, "walletAddress"),
  };
}

function readConfigFile(): RuntimeConfig {
  if (!fs.existsSync(CONFIG_PATH)) {
    return DEFAULT_CONFIG;
  }

  return normalizeRuntimeConfig(JSON.parse(fs.readFileSync(CONFIG_PATH, "utf8")));
}

export function getRuntimeConfig(): RuntimeConfig {
  return readConfigFile();
}

export function readRuntimeConfig(): RuntimeConfig {
  return readConfigFile();
}

export function setRuntimeConfig(patch: Partial<RuntimeConfig>): RuntimeConfig {
  const next = normalizeRuntimeConfig({
    ...readConfigFile(),
    ...patch,
  });

  ensureConfigDir();
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(next, null, 2));

  return next;
}

// ── Wallet persistence (~/.moltx/wallet.json) ───────────────────────────────

const WALLET_PATH = path.join(CONFIG_DIR, "wallet.json");

type WalletState = {
  privateKey: `0x${string}`;
  address: `0x${string}`;
};

function readStoredWallet(): WalletState | undefined {
  if (!fs.existsSync(WALLET_PATH)) return undefined;
  try {
    const raw = JSON.parse(fs.readFileSync(WALLET_PATH, "utf8"));
    if (typeof raw.privateKey !== "string" || !isHex(raw.privateKey) || raw.privateKey.length !== 66) {
      return undefined;
    }
    return raw as WalletState;
  } catch {
    return undefined;
  }
}

function writeStoredWallet(state: WalletState): void {
  ensureConfigDir();
  fs.writeFileSync(WALLET_PATH, JSON.stringify(state, null, 2), { mode: 0o600 });
  fs.chmodSync(WALLET_PATH, 0o600);
}

/**
 * Returns the agent's private key.
 *
 * Resolution order:
 *   1. ~/.moltx/wallet.json (file-based, auto-generated on first run)
 *
 * If no wallet exists, a new one is generated and persisted automatically.
 */
export function getPrivateKey(): `0x${string}` {
  const stored = readStoredWallet();
  if (stored) return stored.privateKey;

  // First run: generate a new wallet
  const privateKey = `0x${crypto.randomBytes(32).toString("hex")}` as `0x${string}`;
  const account = privateKeyToAccount(privateKey);
  writeStoredWallet({ privateKey, address: getAddress(account.address) });
  return privateKey;
}

export function getWalletAddress(): `0x${string}` {
  const stored = readStoredWallet();
  if (stored) return getAddress(stored.address);

  // Triggers wallet generation if not exists
  const privateKey = getPrivateKey();
  const account = privateKeyToAccount(privateKey);
  return getAddress(account.address);
}
