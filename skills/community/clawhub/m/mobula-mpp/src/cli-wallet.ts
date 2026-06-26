/**
 * Standalone CLI wallet for the `mpp` command.
 *
 * SECURITY:
 *  - Private key is AES-256-GCM encrypted at rest.
 *  - Encryption key is a 32-byte secret stored at ~/.mpp-skill/.secret (chmod 600),
 *    auto-generated on first wallet creation.
 *  - The plaintext private key only exists in memory inside this process,
 *    just long enough to sign a Tempo transaction.
 *
 * Threat model: this is a hot wallet for pay-as-you-go API calls (~$0.0004 each).
 * It is intended to hold a few dollars at a time. A local-machine compromise = wallet
 * compromise — keep balances small and bridge top-ups on demand.
 *
 * For per-user wallets in a multi-tenant agent (e.g. Telegram bot),
 * use the encrypted helpers in `./wallet.ts` keyed by user ID.
 */

import { join } from "node:path";
import { homedir } from "node:os";
import { mkdir, chmod, readFile, writeFile, access } from "node:fs/promises";
import {
  createCipheriv,
  createDecipheriv,
  randomBytes,
} from "node:crypto";
import { generatePrivateKey, privateKeyToAccount } from "viem/accounts";
import type { Hex } from "viem";

export const CLI_WALLET_DIR = join(homedir(), ".mpp-skill");
export const CLI_WALLET_FILE = join(CLI_WALLET_DIR, "wallet.json");
export const CLI_SECRET_FILE = join(CLI_WALLET_DIR, ".secret");

export interface CliWallet {
  address: string;
  privateKey: Hex;
  createdAt: string;
}

interface StoredWallet {
  v: 1;
  address: string;
  encryptedKey: string; // iv(24hex) | tag(32hex) | ciphertext(hex)
  createdAt: string;
}

async function exists(p: string): Promise<boolean> {
  try {
    await access(p);
    return true;
  } catch {
    return false;
  }
}

async function getOrCreateSecret(): Promise<Buffer> {
  await mkdir(CLI_WALLET_DIR, { recursive: true });
  if (await exists(CLI_SECRET_FILE)) {
    const hex = (await readFile(CLI_SECRET_FILE, "utf8")).trim();
    return Buffer.from(hex, "hex");
  }
  const secret = randomBytes(32);
  await writeFile(CLI_SECRET_FILE, secret.toString("hex"));
  await chmod(CLI_SECRET_FILE, 0o600);
  return secret;
}

function encrypt(key: Buffer, plaintext: string): string {
  const iv = randomBytes(12);
  const cipher = createCipheriv("aes-256-gcm", key, iv);
  const enc = Buffer.concat([cipher.update(plaintext, "utf8"), cipher.final()]);
  const tag = cipher.getAuthTag();
  return iv.toString("hex") + tag.toString("hex") + enc.toString("hex");
}

function decrypt(key: Buffer, data: string): string {
  const iv = Buffer.from(data.slice(0, 24), "hex");
  const tag = Buffer.from(data.slice(24, 56), "hex");
  const enc = Buffer.from(data.slice(56), "hex");
  const decipher = createDecipheriv("aes-256-gcm", key, iv);
  decipher.setAuthTag(tag);
  return Buffer.concat([decipher.update(enc), decipher.final()]).toString("utf8");
}

export async function loadCliWallet(): Promise<CliWallet | null> {
  if (!(await exists(CLI_WALLET_FILE))) return null;
  const raw = await readFile(CLI_WALLET_FILE, "utf8");
  const parsed = JSON.parse(raw) as Partial<StoredWallet> & Partial<CliWallet>;

  // Backward-compat: pre-2.1 wallets were stored as plaintext { address, privateKey, createdAt }.
  // Detect, migrate to encrypted-at-rest in place, and continue.
  if (!parsed.v && typeof parsed.privateKey === "string" && typeof parsed.address === "string") {
    const secret = await getOrCreateSecret();
    const stored: StoredWallet = {
      v: 1,
      address: parsed.address,
      encryptedKey: encrypt(secret, parsed.privateKey),
      createdAt: parsed.createdAt ?? new Date().toISOString(),
    };
    await writeFile(CLI_WALLET_FILE, JSON.stringify(stored, null, 2));
    await chmod(CLI_WALLET_FILE, 0o600);
    return {
      address: parsed.address,
      privateKey: parsed.privateKey as Hex,
      createdAt: stored.createdAt,
    };
  }

  if (parsed.v !== 1) {
    throw new Error(`Unsupported wallet version: ${parsed.v}`);
  }
  const stored = parsed as StoredWallet;
  const secret = await getOrCreateSecret();
  const privateKey = decrypt(secret, stored.encryptedKey) as Hex;
  return { address: stored.address, privateKey, createdAt: stored.createdAt };
}

export async function createCliWallet(): Promise<CliWallet> {
  if (await exists(CLI_WALLET_FILE)) {
    throw new Error(
      `Wallet already exists at ${CLI_WALLET_FILE}. Delete it first to regenerate.`,
    );
  }
  await mkdir(CLI_WALLET_DIR, { recursive: true });
  const secret = await getOrCreateSecret();
  const privateKey = generatePrivateKey();
  const account = privateKeyToAccount(privateKey);
  const stored: StoredWallet = {
    v: 1,
    address: account.address,
    encryptedKey: encrypt(secret, privateKey),
    createdAt: new Date().toISOString(),
  };
  await writeFile(CLI_WALLET_FILE, JSON.stringify(stored, null, 2));
  await chmod(CLI_WALLET_FILE, 0o600);
  return {
    address: account.address,
    privateKey,
    createdAt: stored.createdAt,
  };
}

export async function requireCliWallet(): Promise<CliWallet> {
  const w = await loadCliWallet();
  if (!w) {
    console.error("No wallet found. Run: bun run start wallet-create");
    process.exit(1);
  }
  return w;
}
