/**
 * Secure per-user wallet management.
 *
 * Each user gets an isolated wallet file at:
 *   .claude/claudeclaw/wallets/{userId}.json
 *
 * The private key is AES-256-GCM encrypted with a key derived from:
 *   HMAC-SHA256(WALLET_SECRET, userId)
 * where WALLET_SECRET is a server-side secret loaded from env or generated once.
 *
 * No other user can decrypt another user's private key.
 */

import { join } from "node:path";
import { mkdir, chmod, readFile, writeFile, access } from "node:fs/promises";
import { createHmac, createCipheriv, createDecipheriv, randomBytes } from "node:crypto";
import { generatePrivateKey, privateKeyToAccount } from "viem/accounts";

async function fileExists(p: string): Promise<boolean> {
  try { await access(p); return true; } catch { return false; }
}

const WALLETS_DIR = join(process.cwd(), ".claude", "claudeclaw", "wallets");
const SECRET_FILE = join(process.cwd(), ".claude", "claudeclaw", "wallet.secret");

let _secret: Buffer | null = null;

async function getSecret(): Promise<Buffer> {
  if (_secret) return _secret;
  if (await fileExists(SECRET_FILE)) {
    _secret = Buffer.from(await readFile(SECRET_FILE, "utf8"), "hex");
  } else {
    _secret = randomBytes(32);
    await mkdir(join(SECRET_FILE, ".."), { recursive: true });
    await writeFile(SECRET_FILE, _secret.toString("hex"));
    await chmod(SECRET_FILE, 0o600);
  }
  return _secret;
}

function deriveKey(secret: Buffer, userId: number): Buffer {
  return createHmac("sha256", secret).update(String(userId)).digest();
}

function encrypt(key: Buffer, plaintext: string): string {
  const iv = randomBytes(12);
  const cipher = createCipheriv("aes-256-gcm", key, iv);
  const enc = Buffer.concat([cipher.update(plaintext, "utf8"), cipher.final()]);
  const tag = cipher.getAuthTag();
  // Format: iv(24hex) + tag(32hex) + ciphertext(hex)
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

function walletPath(userId: number): string {
  return join(WALLETS_DIR, `${userId}.json`);
}

export interface UserWallet {
  address: string;
  createdAt: string;
}

/** Generate a new wallet for a user using viem (correct keccak256 derivation). */
function generateWallet(): { address: string; privateKey: string } {
  const privateKey = generatePrivateKey();
  const account = privateKeyToAccount(privateKey);
  return { address: account.address, privateKey };
}

/** Create a wallet for a user. Throws if one already exists. */
export async function createUserWallet(userId: number): Promise<UserWallet> {
  await mkdir(WALLETS_DIR, { recursive: true });
  const path = walletPath(userId);
  if (await fileExists(path)) {
    throw new Error("Wallet already exists for this user");
  }

  const secret = await getSecret();
  const key = deriveKey(secret, userId);
  const { address, privateKey } = generateWallet();

  const record = {
    address,
    encryptedKey: encrypt(key, privateKey),
    createdAt: new Date().toISOString(),
  };

  await writeFile(path, JSON.stringify(record, null, 2));
  await chmod(path, 0o600);

  return { address, createdAt: record.createdAt };
}

/** Get a user's wallet address (public info only). Returns null if no wallet. */
export async function getUserWalletAddress(userId: number): Promise<string | null> {
  const path = walletPath(userId);
  if (!(await fileExists(path))) return null;
  const record = JSON.parse(await readFile(path, "utf8"));
  return record.address ?? null;
}

/** Get the decrypted private key for a user's wallet. Only call for the user's own operations. */
export async function getUserPrivateKey(userId: number): Promise<string | null> {
  const path = walletPath(userId);
  if (!(await fileExists(path))) return null;
  const secret = await getSecret();
  const key = deriveKey(secret, userId);
  const record = JSON.parse(await readFile(path, "utf8"));
  return decrypt(key, record.encryptedKey);
}
