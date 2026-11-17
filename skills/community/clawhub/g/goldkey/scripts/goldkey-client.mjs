#!/usr/bin/env node

import { open, realpath, unlink } from "node:fs/promises";
import { isAbsolute } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const MAINNET_CHAIN_ID = 8453;
const BASE_MAINNET_USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";
const PAYGO_TREASURY = "0xd6b7E00FcD46966676F554fE0455BfF739e85b1b";
const PAYGO_NETWORK = "eip155:8453";
const PAYGO_AMOUNT_ATOMIC = "10000";
const GUARD_NETWORK_AMOUNT_ATOMIC = "50000";
const GUARD_EVM_AMOUNT_ATOMIC = "100000";
const PAYGO_MAX_TIMEOUT_SECONDS = 300;
const MAX_SIGNATURE_CHARS = 32 * 1024;

// Frozen, source-verified Base mainnet release identity.
export const RELEASE_IDENTITY_SOURCE = Object.freeze({
  origin: "https://goldkey-edge-storefront.noah-ing.workers.dev",
  chainId: MAINNET_CHAIN_ID,
  contract: "0x220FE98C77CE79baa00d47C5896BE05C2A7D3db0",
  usdc: BASE_MAINNET_USDC,
  termsHash: "0xd1fb20b0e28b63e18b660a2710f1b69b356bc87829a01cf5d75e572ae7de3750",
});

function fail(message) {
  throw new Error(message);
}

function isPlaceholder(value) {
  return typeof value === "string" && value.includes("{{");
}

export function normalizeBaseUrl(value, name = "GoldKey origin") {
  if (typeof value !== "string" || value.length === 0 || isPlaceholder(value)) {
    fail(`${name} is not configured; release template values must be replaced before publication`);
  }
  let url;
  try {
    url = new URL(value);
  } catch {
    fail(`${name} must be an absolute URL`);
  }
  if (url.protocol !== "https:" || url.username || url.password || url.search || url.hash) {
    fail(`${name} must be a credential-free HTTPS origin`);
  }
  if (url.pathname !== "/") fail(`${name} must not contain a path`);
  return url.origin;
}

function normalizeAddress(value, name) {
  if (typeof value !== "string" || isPlaceholder(value)) {
    fail(`${name} is not configured; release template values must be replaced before publication`);
  }
  if (!/^0x[0-9a-fA-F]{40}$/.test(value) || /^0x0{40}$/i.test(value)) {
    fail(`${name} must be a nonzero EVM address`);
  }
  return value.toLowerCase();
}

function normalizeTermsHash(value) {
  if (typeof value !== "string" || isPlaceholder(value)) {
    fail("GoldKey terms hash is not configured; release template values must be replaced before publication");
  }
  if (!/^0x[0-9a-fA-F]{64}$/.test(value) || /^0x0{64}$/i.test(value)) {
    fail("GoldKey terms hash must be a nonzero bytes32 value");
  }
  return value.toLowerCase();
}

export function validateReleaseIdentity(source = RELEASE_IDENTITY_SOURCE) {
  if (!source || typeof source !== "object" || Array.isArray(source)) fail("GoldKey release identity must be an object");
  if (source.chainId !== MAINNET_CHAIN_ID) fail(`GoldKey release chain must be Base mainnet ${MAINNET_CHAIN_ID}`);
  const usdc = normalizeAddress(source.usdc, "GoldKey USDC address");
  if (usdc !== BASE_MAINNET_USDC.toLowerCase()) fail("GoldKey release USDC address must be the canonical Base mainnet USDC contract");
  return Object.freeze({
    origin: normalizeBaseUrl(source.origin, "GoldKey release origin"),
    chainId: MAINNET_CHAIN_ID,
    contract: normalizeAddress(source.contract, "GoldKey mainnet contract"),
    usdc,
    termsHash: normalizeTermsHash(source.termsHash),
  });
}

export function resolveRuntimeConfig({ env = process.env, releaseIdentitySource = RELEASE_IDENTITY_SOURCE } = {}) {
  const allowDev = env.GOLDKEY_ALLOW_DEV_ORIGIN;
  const devOrigin = env.GOLDKEY_DEV_API_URL;
  if (allowDev !== undefined && allowDev !== "" && allowDev !== "1") {
    fail("GOLDKEY_ALLOW_DEV_ORIGIN must be exactly 1 when development routing is intended");
  }
  if (devOrigin && allowDev !== "1") {
    fail("GOLDKEY_DEV_API_URL is ignored unless GOLDKEY_ALLOW_DEV_ORIGIN=1");
  }
  if (allowDev === "1") {
    if (!devOrigin) fail("GOLDKEY_DEV_API_URL is required when GOLDKEY_ALLOW_DEV_ORIGIN=1");
    const origin = normalizeBaseUrl(devOrigin, "GoldKey development origin");
    let releaseIdentity;
    try {
      releaseIdentity = validateReleaseIdentity(releaseIdentitySource);
    } catch {
      releaseIdentity = null;
    }
    const canonical = releaseIdentity !== null && origin === releaseIdentity.origin;
    return Object.freeze({
      origin,
      mode: "development",
      canonical,
      identity: canonical ? releaseIdentity : null,
    });
  }

  const identity = validateReleaseIdentity(releaseIdentitySource);
  return Object.freeze({ origin: identity.origin, mode: "production", canonical: true, identity });
}

function parseFlags(argv) {
  const flags = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const item = argv[index];
    if (!item.startsWith("--")) fail(`Unexpected argument: ${item}`);
    const key = item.slice(2);
    if (key === "authorized") {
      flags.set(key, true);
      continue;
    }
    const value = argv[index + 1];
    if (value === undefined || value.startsWith("--")) fail(`Missing value for --${key}`);
    flags.set(key, value);
    index += 1;
  }
  return flags;
}

function required(flags, name) {
  const value = flags.get(name);
  if (value === undefined || value === "") fail(`--${name} is required`);
  return value;
}

function integerFlag(flags, name, { min = 0, max = Number.MAX_SAFE_INTEGER } = {}) {
  const raw = required(flags, name);
  if (!/^\d+$/.test(raw)) fail(`--${name} must be an integer`);
  const value = Number(raw);
  if (!Number.isSafeInteger(value) || value < min || value > max) fail(`--${name} is out of range`);
  return value;
}

function jsonFlag(flags, name) {
  const raw = required(flags, name);
  try {
    const parsed = JSON.parse(raw);
    if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) fail(`--${name} must be a JSON object`);
    return parsed;
  } catch (error) {
    if (error.message.includes(`--${name}`)) throw error;
    fail(`--${name} must be valid JSON`);
  }
}

function identityMismatch(field) {
  fail(`GoldKey identity mismatch: ${field}`);
}

function expectExact(actual, expected, field) {
  if (actual !== expected) identityMismatch(field);
}

function expectAddress(actual, expected, field) {
  if (typeof actual !== "string" || !/^0x[0-9a-fA-F]{40}$/.test(actual) || actual.toLowerCase() !== expected) {
    identityMismatch(field);
  }
}

function expectTermsHash(actual, expected, field) {
  if (typeof actual !== "string" || actual.toLowerCase() !== expected) identityMismatch(field);
}

function expectCanonicalUrl(actual, identity, field) {
  let parsed;
  try {
    parsed = new URL(actual);
  } catch {
    identityMismatch(field);
  }
  if (parsed.origin !== identity.origin || parsed.protocol !== "https:") identityMismatch(field);
}

function validateTransactionTargets(payload, identity) {
  if (!Array.isArray(payload.unsigned_transactions)) identityMismatch("unsigned_transactions");
  for (const transaction of payload.unsigned_transactions) {
    if (!transaction || typeof transaction !== "object" || Array.isArray(transaction)) identityMismatch("unsigned_transactions item");
    const target = typeof transaction.to === "string" ? transaction.to.toLowerCase() : "";
    if (target !== identity.usdc && target !== identity.contract) identityMismatch("unsigned transaction target");
    if (transaction.value !== "0") identityMismatch("unsigned transaction native value");
  }
}

export function validateIdentityPayload(kind, payload, identity) {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) identityMismatch(`${kind} payload`);

  if (kind === "guard-keyset") {
    if (Object.keys(payload).length !== 2 || !Object.hasOwn(payload, "schema") || !Object.hasOwn(payload, "keys")) identityMismatch("Guard keyset fields");
    expectExact(payload.schema, "goldkey.guard-receipt-keyset.v1", "Guard keyset schema");
    if (!Array.isArray(payload.keys) || payload.keys.length < 1 || payload.keys.length > 32) identityMismatch("Guard keyset keys");
    const keyIds = new Set();
    const canonicalDate = (value) => typeof value === "string" && Number.isFinite(Date.parse(value)) && new Date(Date.parse(value)).toISOString() === value;
    for (const [index, key] of payload.keys.entries()) {
      const allowedFields = new Set(["kty", "crv", "x", "kid", "use", "alg", "key_ops", "not_before", "signing_not_after", "revoked_at"]);
      if (!key || typeof key !== "object" || Array.isArray(key) || Object.keys(key).some((field) => !allowedFields.has(field)) || key.kty !== "OKP" || key.crv !== "Ed25519" || typeof key.x !== "string" || !/^[A-Za-z0-9_-]{43}$/.test(key.x) || typeof key.kid !== "string" || key.kid.length < 1 || key.kid.length > 128 || (key.use !== undefined && key.use !== "sig") || (key.alg !== undefined && key.alg !== "EdDSA") || (key.key_ops !== undefined && (!Array.isArray(key.key_ops) || key.key_ops.length !== 1 || key.key_ops[0] !== "verify"))) {
        identityMismatch("Guard keyset public Ed25519 key");
      }
      const hasNotBefore = key.not_before !== undefined;
      const hasSigningNotAfter = key.signing_not_after !== undefined;
      if (hasNotBefore !== hasSigningNotAfter || (index > 0 && !hasNotBefore) || (key.revoked_at !== undefined && !hasNotBefore)) {
        identityMismatch("Guard keyset signing interval");
      }
      if (hasNotBefore) {
        if (!canonicalDate(key.not_before) || !canonicalDate(key.signing_not_after) || Date.parse(key.not_before) >= Date.parse(key.signing_not_after)) {
          identityMismatch("Guard keyset signing interval");
        }
        if (key.revoked_at !== undefined && (!canonicalDate(key.revoked_at) || Date.parse(key.revoked_at) < Date.parse(key.not_before) || Date.parse(key.revoked_at) > Date.parse(key.signing_not_after))) {
          identityMismatch("Guard keyset revocation interval");
        }
      }
      if (keyIds.has(key.kid)) identityMismatch("Guard keyset distinct key IDs");
      keyIds.add(key.kid);
    }
    return payload;
  }

  if (!identity) return payload;

  if (kind === "offer") {
    expectExact(payload.schema, "goldkey.offer.v1", "offer schema");
    expectExact(payload.price?.chain_id, identity.chainId, "offer chain_id");
    expectAddress(payload.price?.token_address, identity.usdc, "offer USDC address");
    expectAddress(payload.contract?.address, identity.contract, "offer contract address");
    expectTermsHash(payload.contract?.terms_hash, identity.termsHash, "offer terms hash");
    expectCanonicalUrl(payload.contract?.terms_uri, identity, "offer terms URI");
    expectCanonicalUrl(payload.alternative?.endpoint, identity, "offer paygo endpoint");
    for (const [name, value] of Object.entries(payload.discovery ?? {})) expectCanonicalUrl(value, identity, `offer discovery ${name}`);
    return payload;
  }

  if (kind === "commerce") {
    expectExact(payload.schema, "goldkey.commerce-response.v1", "commerce schema");
    expectExact(payload.chain_id, identity.chainId, "commerce chain_id");
    expectAddress(payload.contract, identity.contract, "commerce contract address");
    expectAddress(payload.payment_token, identity.usdc, "commerce USDC address");
    expectTermsHash(payload.terms_hash, identity.termsHash, "commerce terms hash");
    expectCanonicalUrl(payload.terms_uri, identity, "commerce terms URI");
    expectCanonicalUrl(payload.response_schema_url, identity, "commerce response schema URL");
    validateTransactionTargets(payload, identity);
    return payload;
  }

  if (kind === "renewal") {
    expectExact(payload.schema, "goldkey.renewal-response.v1", "renewal schema");
    expectExact(payload.chain_id, identity.chainId, "renewal chain_id");
    expectAddress(payload.contract, identity.contract, "renewal contract address");
    expectCanonicalUrl(payload.terms_uri, identity, "renewal terms URI");
    validateTransactionTargets(payload, identity);
    return payload;
  }

  fail(`Unknown identity payload kind: ${kind}`);
}

async function request(path, { method = "GET", body, token, headers = {}, validateAs } = {}, context) {
  if (token && !context.runtime.canonical) {
    fail("Refusing to send GOLDKEY_ACCESS_TOKEN to a noncanonical development origin");
  }
  const response = await context.fetchImpl(`${context.runtime.origin}${path}`, {
    method,
    redirect: "error",
    headers: {
      accept: "application/json",
      ...(body === undefined ? {} : { "content-type": "application/json" }),
      ...(token ? { authorization: `Bearer ${token}` } : {}),
      ...headers,
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  let payload;
  try {
    payload = text ? JSON.parse(text) : null;
  } catch {
    fail(`GoldKey returned non-JSON HTTP ${response.status}`);
  }
  if (!response.ok) {
    const code = payload?.error?.code || "request_failed";
    const message = payload?.error?.message || `HTTP ${response.status}`;
    fail(`${code}: ${message}`);
  }
  return validateAs ? validateIdentityPayload(validateAs, payload, context.runtime.identity) : payload;
}

async function paymentProbe(path, requestBody, context, label, fallbackCode, {
  expectedAmountAtomic = PAYGO_AMOUNT_ATOMIC,
  allowIdempotentReplay = false,
} = {}) {
  if (!context.runtime.canonical) fail("Refusing to probe x402 payment against a noncanonical development origin");
  const response = await context.fetchImpl(`${context.runtime.origin}${path}`, {
    method: "POST",
    redirect: "error",
    headers: { accept: "application/json", "content-type": "application/json" },
    body: JSON.stringify(requestBody),
  });
  const text = await response.text();
  let body;
  try {
    body = text ? JSON.parse(text) : null;
  } catch {
    body = text || null;
  }
  if (allowIdempotentReplay && response.ok && response.headers.get("x-goldkey-idempotent-replay") === "true") {
    return { http_status: response.status, idempotent_replay: true, payment_required: false, authorization_verified: false };
  }
  if (response.status !== 402) {
    if (response.ok) fail(`${label} executed without an x402 payment challenge; no payment was authorized`);
    const code = body?.error?.code || fallbackCode;
    const message = body?.error?.message || `HTTP ${response.status}`;
    fail(`${code}: ${message}`);
  }
  const paymentRequired = response.headers.get("payment-required");
  if (!paymentRequired) fail("HTTP 402 response omitted the PAYMENT-REQUIRED header");
  if (paymentRequired.length > 128 * 1024) fail("PAYMENT-REQUIRED header is too large");
  let challenge;
  try {
    challenge = JSON.parse(Buffer.from(paymentRequired, "base64").toString("utf8"));
  } catch {
    fail("PAYMENT-REQUIRED header is not valid base64-encoded JSON");
  }
  if (!challenge || typeof challenge !== "object" || Array.isArray(challenge)) fail("PAYMENT-REQUIRED challenge must be an object");
  if (challenge.x402Version !== 2) fail("PAYMENT-REQUIRED challenge must use x402 v2");
  const resource = `${context.runtime.origin}${path}`;
  if (challenge.resource?.url !== resource) fail("PAYMENT-REQUIRED resource URL does not match the canonical endpoint");
  if (!Array.isArray(challenge.accepts) || challenge.accepts.length !== 1) fail("PAYMENT-REQUIRED challenge must contain exactly one payment option");
  const option = challenge.accepts[0];
  if (!option || typeof option !== "object" || Array.isArray(option)) fail("PAYMENT-REQUIRED payment option must be an object");
  if (option.scheme !== "exact") fail("PAYMENT-REQUIRED payment scheme must be exact");
  if (option.network !== PAYGO_NETWORK) fail(`PAYMENT-REQUIRED network must be ${PAYGO_NETWORK}`);
  if (option.amount !== expectedAmountAtomic) fail(`PAYMENT-REQUIRED amount must be ${expectedAmountAtomic} atomic USDC`);
  if (normalizeAddress(option.asset, "PAYMENT-REQUIRED asset") !== context.runtime.identity.usdc) fail("PAYMENT-REQUIRED asset must be canonical Base USDC");
  if (normalizeAddress(option.payTo, "PAYMENT-REQUIRED payee") !== PAYGO_TREASURY.toLowerCase()) fail("PAYMENT-REQUIRED payee does not match the GoldKey treasury");
  if (!Number.isInteger(option.maxTimeoutSeconds) || option.maxTimeoutSeconds < 1 || option.maxTimeoutSeconds > PAYGO_MAX_TIMEOUT_SECONDS) {
    fail(`PAYMENT-REQUIRED maxTimeoutSeconds must be 1-${PAYGO_MAX_TIMEOUT_SECONDS}`);
  }
  return {
    http_status: 402,
    payment_required: paymentRequired,
    payment: {
      x402_version: 2,
      scheme: option.scheme,
      network: option.network,
      amount_atomic: option.amount,
      asset: normalizeAddress(option.asset, "PAYMENT-REQUIRED asset"),
      pay_to: normalizeAddress(option.payTo, "PAYMENT-REQUIRED payee"),
      resource,
      max_timeout_seconds: option.maxTimeoutSeconds,
    },
    body,
  };
}

function accessToken(env) {
  const value = env.GOLDKEY_ACCESS_TOKEN;
  if (!value) fail("Set GOLDKEY_ACCESS_TOKEN through the agent secret store for this authenticated command");
  return value;
}

function requireCanonicalWalletAuthentication(context) {
  if (!context.runtime.canonical) {
    fail("Refusing wallet authentication against a noncanonical development origin");
  }
}

async function readSignatureFromStdin(stream = process.stdin) {
  if (stream.isTTY) fail("Inject GOLDKEY_WALLET_SIGNATURE through the secret store or provide the signature on standard input");
  let value = "";
  for await (const chunk of stream) {
    value += chunk.toString("utf8");
    if (value.length > MAX_SIGNATURE_CHARS) fail("Wallet signature input is too large");
  }
  return value;
}

async function walletSignature(flags, env, readStdinImpl) {
  if (flags.has("signature")) fail("--signature is disabled because command arguments are logged; use GOLDKEY_WALLET_SIGNATURE or standard input");
  const raw = env.GOLDKEY_WALLET_SIGNATURE || await readStdinImpl();
  const value = typeof raw === "string" ? raw.trim() : "";
  if (value.length > MAX_SIGNATURE_CHARS || !/^0x(?:[0-9a-fA-F]{2})+$/.test(value)) {
    fail("Wallet signature must be nonempty 0x-prefixed bytes");
  }
  return value;
}

function quoteBody(flags) {
  const body = {
    forecast_calls: integerFlag(flags, "forecast", { max: 10_000_000 }),
    pass_purchase_budget_usdc: flags.get("budget") || "50.00",
    switching_cost_usdc: flags.get("switching-cost") || "0.00",
    risk_reserve_usdc: flags.get("risk-reserve") || "0.00",
    purchase_authority: flags.get("authorized") === true,
  };
  if (flags.has("wallet")) body.wallet = flags.get("wallet");
  return body;
}

const help = `GoldKey client

Commands:
  offer
  catalog
  demo
  openapi
  quote --forecast N [--wallet 0x...] [--budget 50.00] [--switching-cost 0.00] [--risk-reserve 0.00] [--authorized]
  renew --token-id N --forecast N [--wallet 0x...] [--switching-cost 0.00] [--risk-reserve 0.00] [--authorized]
  challenge --token-id N --wallet 0x...
  verify --challenge-id UUID --secret-output /absolute/private/file
  quota
  tool --name TOOL --idempotency KEY --input JSON_OBJECT
  keys-list
  key-issue --secret-output /absolute/private/file --body JSON_OBJECT
  key-revoke --id KEY_ID
  keys-revoke-all
  action-gate-probe --input JSON_OBJECT
  paygo-probe --name TOOL --input JSON_OBJECT
  guard-keyset
  guard-network-probe --request SIGNED_SYNTHETIC_GUARD_REQUEST_JSON
  guard-evm-probe --request SIGNED_SYNTHETIC_GUARD_REQUEST_JSON
  self-test

The published release embeds and validates its canonical Base mainnet origin and identity.
For verify, inject GOLDKEY_WALLET_SIGNATURE temporarily or provide the signature on stdin.
Inject authenticated credentials through GOLDKEY_ACCESS_TOKEN; never pass them as arguments.`;

export async function run(argv, options = {}) {
  const [command, ...rest] = argv;
  const flags = parseFlags(rest);
  if (!command || command === "help" || command === "--help") return { help };

  const releaseIdentitySource = options.releaseIdentitySource ?? RELEASE_IDENTITY_SOURCE;
  if (command === "self-test") {
    const identity = validateReleaseIdentity(releaseIdentitySource);
    const sample = quoteBody(new Map([["forecast", "7200"], ["budget", "50.00"]]));
    if (sample.forecast_calls !== 7200 || sample.purchase_authority !== false) fail("quote construction failed");
    return {
      ok: true,
      origin: identity.origin,
      chain_id: identity.chainId,
      contract: identity.contract,
      usdc: identity.usdc,
      terms_hash: identity.termsHash,
    };
  }

  const env = options.env ?? process.env;
  const runtime = resolveRuntimeConfig({ env, releaseIdentitySource });
  const context = { runtime, fetchImpl: options.fetchImpl ?? fetch };
  const readStdinImpl = options.readStdinImpl ?? (() => readSignatureFromStdin());

  if (command === "offer") return request("/.well-known/goldkey.json", { validateAs: "offer" }, context);
  if (command === "catalog") return request("/v1/catalog", {}, context);
  if (command === "demo") return request("/v1/demo", {}, context);
  if (command === "openapi") return request("/openapi.json", {}, context);
  if (command === "guard-keyset") return request("/.well-known/goldkey-guard-keys.json", { validateAs: "guard-keyset" }, context);
  if (command === "quote") {
    return request("/v1/commerce/respond", { method: "POST", body: quoteBody(flags), validateAs: "commerce" }, context);
  }
  if (command === "renew") {
    const body = {
      token_id: required(flags, "token-id"),
      forecast_calls: integerFlag(flags, "forecast", { max: 10_000_000 }),
      switching_cost_usdc: flags.get("switching-cost") || "0.00",
      risk_reserve_usdc: flags.get("risk-reserve") || "0.00",
      purchase_authority: flags.get("authorized") === true,
    };
    if (flags.has("wallet")) body.wallet = flags.get("wallet");
    return request("/v1/renewal/quote", { method: "POST", body, validateAs: "renewal" }, context);
  }
  if (command === "challenge") {
    requireCanonicalWalletAuthentication(context);
    return request("/v1/auth/challenge", {
      method: "POST",
      body: { token_id: required(flags, "token-id"), wallet: required(flags, "wallet") },
    }, context);
  }
  if (command === "verify") {
    requireCanonicalWalletAuthentication(context);
    return request("/v1/auth/verify", {
      method: "POST",
      body: { challenge_id: required(flags, "challenge-id"), signature: await walletSignature(flags, env, readStdinImpl) },
    }, context);
  }
  if (command === "quota") return request("/v1/quota", { token: accessToken(env) }, context);
  if (command === "tool") {
    return request(`/v1/tools/${encodeURIComponent(required(flags, "name"))}`, {
      method: "POST",
      token: accessToken(env),
      headers: { "idempotency-key": required(flags, "idempotency") },
      body: jsonFlag(flags, "input"),
    }, context);
  }
  if (command === "keys-list") return request("/v1/keys", { token: accessToken(env) }, context);
  if (command === "key-issue") {
    return request("/v1/keys", { method: "POST", token: accessToken(env), body: jsonFlag(flags, "body") }, context);
  }
  if (command === "key-revoke") {
    return request(`/v1/keys/${encodeURIComponent(required(flags, "id"))}`, { method: "DELETE", token: accessToken(env) }, context);
  }
  if (command === "keys-revoke-all") return request("/v1/keys", { method: "DELETE", token: accessToken(env) }, context);
  if (command === "action-gate-probe") {
    return paymentProbe(
      "/v1/action-gate",
      jsonFlag(flags, "input"),
      context,
      "Action Gate",
      "action_gate_probe_failed",
    );
  }
  if (command === "paygo-probe") {
    return paymentProbe(
      "/v1/paygo/execute",
      { tool: required(flags, "name"), input: jsonFlag(flags, "input") },
      context,
      "Paygo",
      "paygo_probe_failed",
    );
  }
  if (command === "guard-network-probe") {
    return paymentProbe(
      "/v1/guard/paygo/authorize/network",
      jsonFlag(flags, "request"),
      context,
      "Guard network authorization",
      "guard_network_probe_failed",
      { expectedAmountAtomic: GUARD_NETWORK_AMOUNT_ATOMIC, allowIdempotentReplay: true },
    );
  }
  if (command === "guard-evm-probe") {
    return paymentProbe(
      "/v1/guard/paygo/authorize/evm",
      jsonFlag(flags, "request"),
      context,
      "Guard EVM authorization",
      "guard_evm_probe_failed",
      { expectedAmountAtomic: GUARD_EVM_AMOUNT_ATOMIC, allowIdempotentReplay: true },
    );
  }
  fail(`Unknown command: ${command}`);
}

function secretField(command) {
  if (command === "verify") return "access_token";
  if (command === "key-issue") return "access_key";
  return null;
}

export async function runCli(argv, options = {}) {
  const command = argv[0];
  const field = secretField(command);
  if (!field) {
    if (argv.includes("--secret-output")) fail("--secret-output is valid only for verify and key-issue");
    return run(argv, options);
  }

  const flags = parseFlags(argv.slice(1));
  const outputPath = required(flags, "secret-output");
  if (!isAbsolute(outputPath)) fail("--secret-output must be an absolute path");
  const openSecretFileImpl = options.openSecretFileImpl ?? ((filePath) => open(filePath, "wx", 0o600));
  const removeSecretFileImpl = options.removeSecretFileImpl ?? ((filePath) => unlink(filePath));
  let handle;
  let created = false;
  try {
    handle = await openSecretFileImpl(outputPath);
    created = true;
    const result = await run(argv, options);
    const credential = result?.[field];
    if (typeof credential !== "string" || credential.length === 0) fail(`GoldKey response omitted ${field}`);
    await handle.writeFile(`${JSON.stringify({ [field]: credential })}\n`, { encoding: "utf8" });
    await handle.close();
    handle = null;
    return { ...result, [field]: "[REDACTED]", secret_output_written: true };
  } catch (error) {
    if (handle) {
      try {
        await handle.close();
      } catch {
        // Preserve the original error.
      }
    }
    if (created) {
      try {
        await removeSecretFileImpl(outputPath);
      } catch {
        // The path was created by this process; cleanup failure must not mask the request error.
      }
    }
    throw error;
  }
}

export async function isDirectExecution(moduleUrl, argvPath, { realpathImpl = realpath } = {}) {
  if (!argvPath) return false;
  try {
    const [modulePath, entryPath] = await Promise.all([
      realpathImpl(fileURLToPath(moduleUrl)),
      realpathImpl(argvPath),
    ]);
    return modulePath === entryPath;
  } catch {
    return moduleUrl === pathToFileURL(argvPath).href;
  }
}

if (await isDirectExecution(import.meta.url, process.argv[1])) {
  runCli(process.argv.slice(2))
    .then((result) => {
      if (result?.help) process.stdout.write(`${result.help}\n`);
      else process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    })
    .catch((error) => {
      process.stderr.write(`${error.message}\n`);
      process.exitCode = 1;
    });
}
