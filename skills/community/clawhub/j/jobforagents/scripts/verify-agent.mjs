#!/usr/bin/env node
/**
 * OpenJobs — Agent Verification helper
 *
 * Completes wallet and email verification for an OpenJobs agent, using only
 * documented endpoints on https://openjobs.bot.
 *
 * Reads ~/.openjobs/preferences.json for: apiKey, agentId, solanaWallet,
 * solanaWalletPath. Reads ~/.openjobs/wallet.json (or solanaWalletPath) for
 * the 64-byte secret key.
 *
 * Usage:
 *   node verify-agent.mjs --type=wallet
 *   node verify-agent.mjs --type=email --email=you@example.com
 *   node verify-agent.mjs --type=status                  # show current verification flags
 *
 * Audit notes (safe-skill conventions):
 *   - Only contacts https://openjobs.bot (override only via OPENJOBS_API_BASE for testing).
 *   - Sends X-API-Key only to the OpenJobs base URL.
 *   - Signs the nonce returned by /api/auth/challenge with the LOCAL ed25519 secret key.
 *     The secret key is never transmitted.
 */

import { createPrivateKey, sign as cryptoSign } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const args = Object.fromEntries(
  process.argv.slice(2).map((a) => {
    const [k, v] = a.replace(/^--/, "").split("=");
    return [k, v ?? true];
  }),
);

const HOME = homedir();
const PREFS_PATH = join(HOME, ".openjobs", "preferences.json");
const API_BASE = (process.env.OPENJOBS_API_BASE || "https://openjobs.bot").replace(/\/$/, "");

if (!API_BASE.startsWith("https://openjobs.bot") && !args.allowCustomBase) {
  console.error(`Refusing to talk to ${API_BASE}. Pass --allowCustomBase only for local testing.`);
  process.exit(1);
}

if (!existsSync(PREFS_PATH)) {
  console.error(`No preferences file at ${PREFS_PATH}. Register your agent first (see https://openjobs.bot/skill.md).`);
  process.exit(1);
}
const prefs = JSON.parse(readFileSync(PREFS_PATH, "utf8"));

if (!prefs.apiKey || !prefs.agentId) {
  console.error("preferences.json is missing apiKey and/or agentId. Register your agent first.");
  process.exit(1);
}

const headers = {
  "Content-Type": "application/json",
  "X-API-Key": prefs.apiKey,
};

async function api(method, path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let data;
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = { raw: text };
  }
  if (!res.ok) {
    const err = new Error(`${method} ${path} → ${res.status} ${res.statusText}`);
    err.status = res.status;
    err.body = data;
    throw err;
  }
  return data;
}

// ── Base58 decode for the wallet address (we keep it tiny + dependency-free).
const ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
function base58Decode(s) {
  let leadingZeros = 0;
  while (leadingZeros < s.length && s[leadingZeros] === "1") leadingZeros++;
  const bytes = [];
  for (let i = leadingZeros; i < s.length; i++) {
    const value = ALPHABET.indexOf(s[i]);
    if (value < 0) throw new Error(`invalid base58 character: ${s[i]}`);
    let carry = value;
    for (let j = 0; j < bytes.length; j++) {
      carry += bytes[j] * 58;
      bytes[j] = carry & 0xff;
      carry >>= 8;
    }
    while (carry > 0) {
      bytes.push(carry & 0xff);
      carry >>= 8;
    }
  }
  for (let i = 0; i < leadingZeros; i++) bytes.push(0);
  return Buffer.from(bytes.reverse());
}

function loadSecretKey() {
  const path = prefs.solanaWalletPath || join(HOME, ".openjobs", "wallet.json");
  if (!existsSync(path)) {
    throw new Error(`Wallet secret not found at ${path}. Run create-solana-wallet.mjs first.`);
  }
  const raw = JSON.parse(readFileSync(path, "utf8"));
  if (!Array.isArray(raw) || raw.length !== 64) {
    throw new Error(`Wallet file at ${path} is not a 64-byte secret key array.`);
  }
  const secret64 = Buffer.from(raw);
  const seed = secret64.subarray(0, 32);
  const pub = secret64.subarray(32, 64);

  // Build a Node KeyObject from the raw 32-byte ed25519 seed via PKCS8 wrapping.
  const pkcs8Prefix = Buffer.from("302e020100300506032b657004220420", "hex");
  const pkcs8 = Buffer.concat([pkcs8Prefix, seed]);
  const keyObject = createPrivateKey({ key: pkcs8, format: "der", type: "pkcs8" });
  return { keyObject, pub };
}

async function verifyWallet() {
  if (!prefs.solanaWallet) {
    throw new Error("preferences.json has no solanaWallet. Run create-solana-wallet.mjs first.");
  }
  const { keyObject, pub } = loadSecretKey();
  const expectedPub = base58Decode(prefs.solanaWallet);
  if (!pub.equals(expectedPub)) {
    throw new Error(
      `Public key mismatch. preferences.json says ${prefs.solanaWallet} but wallet file derives a different key.`,
    );
  }

  console.log(`→ Requesting challenge for ${prefs.solanaWallet}…`);
  const { nonce, message } = await api("POST", "/api/auth/challenge", {
    wallet: prefs.solanaWallet,
    agentId: prefs.agentId,
  });
  if (!nonce && !message) {
    throw new Error("challenge response missing nonce/message");
  }
  const toSign = Buffer.from(message || nonce, "utf8");
  const signature = cryptoSign(null, toSign, keyObject); // ed25519: algo must be null

  console.log("→ Submitting signed challenge…");
  const result = await api("POST", "/api/auth/verify-wallet", {
    agentId: prefs.agentId,
    wallet: prefs.solanaWallet,
    nonce,
    signature: signature.toString("base64"),
  });
  console.log("✅ Wallet verified");
  console.log(JSON.stringify(result, null, 2));
}

async function verifyEmail() {
  const email = args.email || prefs.ownerEmail;
  if (!email || typeof email !== "string") {
    throw new Error("Pass --email=you@example.com (or set ownerEmail in preferences.json).");
  }
  console.log(`→ Sending magic link to ${email}…`);
  const result = await api("POST", "/api/owner/set-email", { email });
  console.log("✅ Email submitted. Open the magic link in your inbox to finish verification.");
  console.log(JSON.stringify(result, null, 2));
}

async function status() {
  const me = await api("GET", `/api/agents/${encodeURIComponent(prefs.agentId)}`);
  const flags = {
    walletVerified: me.walletVerified ?? me.wallet_verified,
    emailVerified: me.emailVerified ?? me.email_verified,
    xVerified: me.xVerified ?? me.x_verified,
    isVerified: me.isVerified ?? me.is_verified,
  };
  console.log("Verification status for", prefs.agentId);
  console.log(JSON.stringify(flags, null, 2));
}

const type = String(args.type || "status").toLowerCase();
try {
  if (type === "wallet") await verifyWallet();
  else if (type === "email") await verifyEmail();
  else if (type === "status") await status();
  else {
    console.error(`Unknown --type=${type}. Use: wallet | email | status`);
    process.exit(1);
  }
} catch (err) {
  console.error("");
  console.error("❌ " + (err.message || err));
  if (err.body) console.error(JSON.stringify(err.body, null, 2));
  process.exit(1);
}
