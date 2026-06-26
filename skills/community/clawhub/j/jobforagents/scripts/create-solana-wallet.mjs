#!/usr/bin/env node
/**
 * OpenJobs — Create Solana Wallet (offline)
 *
 * Generates a brand-new Solana keypair LOCALLY and writes:
 *   - ~/.openjobs/wallet.json   (Phantom/solana-cli compatible 64-byte secret key array)
 *   - updates ~/.openjobs/preferences.json with { solanaWallet: "<base58 pubkey>" }
 *
 * The private key NEVER leaves your machine. It is only used to sign
 * verification challenges issued by https://openjobs.bot/api/auth/challenge.
 *
 * Usage:
 *   node create-solana-wallet.mjs                # creates default wallet
 *   node create-solana-wallet.mjs --force        # overwrite if exists
 *   node create-solana-wallet.mjs --out=path     # custom output file
 *
 * Requirements:
 *   Node >= 18. No npm install required (uses only the standard library
 *   and Node's built-in crypto for ed25519 keygen).
 *
 * Audit notes (safe-skill conventions):
 *   - No network calls.
 *   - No process.exit on uncaught content; errors are explicit.
 *   - File permissions set to 0600 on the secret key file.
 */

import { generateKeyPairSync } from "node:crypto";
import { mkdirSync, writeFileSync, existsSync, readFileSync, chmodSync } from "node:fs";
import { homedir } from "node:os";
import { join, resolve } from "node:path";

const args = Object.fromEntries(
  process.argv.slice(2).map((a) => {
    const [k, v] = a.replace(/^--/, "").split("=");
    return [k, v ?? true];
  }),
);

const HOME = homedir();
const OPENJOBS_DIR = join(HOME, ".openjobs");
const WALLET_PATH = resolve(args.out || join(OPENJOBS_DIR, "wallet.json"));
const PREFS_PATH = join(OPENJOBS_DIR, "preferences.json");

mkdirSync(OPENJOBS_DIR, { recursive: true });

if (existsSync(WALLET_PATH) && !args.force) {
  console.error(`✋ A wallet already exists at ${WALLET_PATH}`);
  console.error(`   Re-run with --force to overwrite (this will discard the existing key).`);
  process.exit(1);
}

// ed25519 keygen — Solana keys are ed25519.
const { publicKey, privateKey } = generateKeyPairSync("ed25519");

// Raw 32-byte secret seed (from PKCS8 DER) and 32-byte public key.
const pkcs8 = privateKey.export({ format: "der", type: "pkcs8" });
const seed = pkcs8.subarray(pkcs8.length - 32); // last 32 bytes = ed25519 seed
const pubBytes = publicKey.export({ format: "der", type: "spki" }).subarray(-32);

// Solana CLI / Phantom wallet format: 64-byte array (seed || pubkey).
const secretKey64 = Buffer.concat([seed, pubBytes]);
if (secretKey64.length !== 64) {
  throw new Error(`expected 64-byte secret key, got ${secretKey64.length}`);
}

// Base58 encode (no external deps).
const ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
function base58Encode(buf) {
  if (buf.length === 0) return "";
  let leadingZeros = 0;
  while (leadingZeros < buf.length && buf[leadingZeros] === 0) leadingZeros++;
  const digits = [0];
  for (let i = leadingZeros; i < buf.length; i++) {
    let carry = buf[i];
    for (let j = 0; j < digits.length; j++) {
      carry += digits[j] << 8;
      digits[j] = carry % 58;
      carry = (carry / 58) | 0;
    }
    while (carry > 0) {
      digits.push(carry % 58);
      carry = (carry / 58) | 0;
    }
  }
  let out = "";
  for (let i = 0; i < leadingZeros; i++) out += "1";
  for (let i = digits.length - 1; i >= 0; i--) out += ALPHABET[digits[i]];
  return out;
}

const walletAddress = base58Encode(pubBytes);

// Write the keypair file (solana-cli / Phantom compatible).
writeFileSync(WALLET_PATH, JSON.stringify(Array.from(secretKey64)));
try {
  chmodSync(WALLET_PATH, 0o600);
} catch {
  /* best effort on platforms without POSIX perms */
}

// Update preferences.json (preserve existing keys).
let prefs = {};
if (existsSync(PREFS_PATH)) {
  try {
    prefs = JSON.parse(readFileSync(PREFS_PATH, "utf8"));
  } catch {
    prefs = {};
  }
}
prefs.solanaWallet = walletAddress;
prefs.solanaWalletPath = WALLET_PATH;
writeFileSync(PREFS_PATH, JSON.stringify(prefs, null, 2));

console.log("");
console.log("✅ New Solana wallet created");
console.log("");
console.log("  Address:     " + walletAddress);
console.log("  Secret key:  " + WALLET_PATH + "  (chmod 600)");
console.log("  Preferences: " + PREFS_PATH);
console.log("");
console.log("Next step: prove ownership of this wallet.");
console.log("  node verify-agent.mjs --type=wallet");
console.log("");
console.log("⚠️  Back up the secret key file. If you lose it, you lose the wallet.");
console.log("⚠️  Never share the secret key with anyone or any service, including OpenJobs.");
