#!/usr/bin/env node
/**
 * Hypawave pubkey-signature helper (Paths 3a / 3b).
 *
 * Produces the secp256k1 signatures + headers the server requires for signed
 * requests under /api/offers/*. This is a faithful port of the reference
 * implementation in https://hypawave.com/llms.txt ("Reference implementation"
 * + "Test vector") — the server rejects compact signatures and validates a
 * specific canonical hash, so use this rather than hand-rolling.
 *
 * Dependency: @noble/secp256k1 is VENDORED at ./vendor/noble-secp256k1.mjs
 * (v1.7.1, MIT, 0-dependency, single file) so the bundle is self-contained —
 * no `npm install` and no network needed on a fresh install. Node 18+.
 *
 * Module use:
 *   import { signRequest } from "./sign_request.mjs";
 *   const { headers, body } = await signRequest({ body: {...}, privKey });
 *   await fetch(url, { method: "POST", headers, body });   // send `body` verbatim
 *
 * Body-less (GET/DELETE): pass { body: null, privKey } → header-only signature.
 *
 * CLI:
 *   echo '{"amount":1,...}' | node sign_request.mjs --key <privhex>     # signed POST body
 *   node sign_request.mjs --key <privhex> --bodyless                    # header-only (GET/DELETE)
 *   node sign_request.mjs --selftest                                    # verify against llms.txt vector
 *   (private key also read from $HYPAWAVE_PRIVKEY if --key is omitted)
 */

import * as secp from "./vendor/noble-secp256k1.mjs";
import crypto from "crypto";
import { fileURLToPath } from "url";
import { realpathSync } from "fs";

const sha256Hex = (input) => crypto.createHash("sha256").update(input).digest("hex");

// Version-tolerant DER hex: v1.x sign() returns a DER Uint8Array; v2.x returns
// a Signature with .toDERRawBytes(). Both are normalized to lowercase hex.
const toDerHex = (sig) => Buffer.from(sig.toDERRawBytes?.() ?? sig).toString("hex");

/**
 * @param {object|null} body      Request body object, or null for body-less requests.
 * @param {string} privKey        32-byte private key, hex (64 chars).
 * @param {string} [timestamp]    Override unix-seconds string (tests only).
 * @param {string} [nonce]        Override nonce hex (tests only).
 * @returns {{ headers: object, body: string|undefined, debug: object }}
 */
export async function signRequest({ body, privKey, timestamp, nonce }) {
  const privBytes = Buffer.from(privKey, "hex");
  const pubKey = Buffer.from(secp.getPublicKey(privBytes, true)).toString("hex");

  // Body-level signature: sign sha256(JSON.stringify(body)) and store it on the
  // body as `signed_payload_hash` — the body-level proof you submitted these exact
  // request bytes. This is NOT the server's canonical `terms_hash` (the 409
  // terms_changed check is computed server-side over specific offer fields).
  // llms.txt's signing section/test vector calls this value `terms_hash`, so the
  // local variable follows that naming. Body-less → skip.
  let fullBody = body;
  let termsHash = null;
  if (body) {
    termsHash = sha256Hex(JSON.stringify(body));
    const termsSig = await secp.sign(Buffer.from(termsHash, "hex"), privBytes);
    fullBody = { ...body, signed_payload_hash: termsHash, signature: toDerHex(termsSig) };
  }

  // Header-level auth signature over the exact bytes you send as the HTTP body.
  const bodyStr = fullBody ? JSON.stringify(fullBody) : "";
  const bodyHash = sha256Hex(bodyStr);
  const ts = timestamp ?? Math.floor(Date.now() / 1000).toString();
  const nce = nonce ?? crypto.randomBytes(16).toString("hex");
  const canonicalHash = sha256Hex(`${bodyHash}:${ts}:${nce}`);
  const sigBytes = await secp.sign(Buffer.from(canonicalHash, "hex"), privBytes);

  return {
    headers: {
      "Content-Type": "application/json",
      "x-pubkey": pubKey,
      "x-signature": toDerHex(sigBytes),
      "x-signed-payload-hash": bodyHash,
      "x-timestamp": ts,
      "x-nonce": nce,
    },
    body: bodyStr || undefined,
    debug: { pubKey, termsHash, bodyHash, canonicalHash },
  };
}

// ── Self-test against the published llms.txt test vector ────────────────────
async function selftest() {
  const privKey = "0000000000000000000000000000000000000000000000000000000000000001";
  const body = {
    amount: 0.01,
    pricing_type: "fiat",
    currency: "USD",
    description: "Test offer",
    payment_destination: "https://example.invalid/.well-known/lnurlp/creator",
    activation_window: "30d",
  };
  const expected = {
    pubKey: "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798",
    termsHash: "4e5c7c24dd3c9ca598c65699a13084bd687b99365c249d4f2e3fe9363c6f1cac",
    bodyHash: "472412ee78dd3bade6df5ade1733c91b1823f097ab87c377bdb3838b89e6ff51",
    canonicalHash: "6adbcd803a3650d108a854c3e333fa8562b83e5f62937039f8f0acdeb957e3aa",
  };
  const { debug } = await signRequest({
    body,
    privKey,
    timestamp: "1779148800",
    nonce: "a1b2c3d4e5f60718293a4b5c6d7e8f90",
  });

  let ok = true;
  for (const k of Object.keys(expected)) {
    const pass = debug[k] === expected[k];
    if (!pass) ok = false;
    console.log(`  ${pass ? "✓" : "✗"} ${k}: ${debug[k]}${pass ? "" : `\n      expected ${expected[k]}`}`);
  }
  console.log(ok ? "\nself-test passed — hashing + serialization correct." : "\nself-test FAILED.");
  process.exit(ok ? 0 : 1);
}

// ── CLI ─────────────────────────────────────────────────────────────────────
async function main() {
  const argv = process.argv.slice(2);
  if (argv.includes("--selftest")) return selftest();

  const keyIdx = argv.indexOf("--key");
  const privKey = (keyIdx >= 0 ? argv[keyIdx + 1] : process.env.HYPAWAVE_PRIVKEY) || "";
  if (!/^[0-9a-fA-F]{64}$/.test(privKey)) {
    console.error("error: provide a 32-byte hex private key via --key <hex> or $HYPAWAVE_PRIVKEY");
    process.exit(2);
  }

  let body = null;
  if (!argv.includes("--bodyless")) {
    const raw = await new Promise((res) => {
      let d = "";
      process.stdin.on("data", (c) => (d += c)).on("end", () => res(d.trim()));
    });
    if (raw) {
      try {
        body = JSON.parse(raw);
      } catch {
        console.error("error: stdin is not valid JSON (use --bodyless for GET/DELETE)");
        process.exit(2);
      }
    }
  }

  let result;
  try {
    result = await signRequest({ body, privKey });
  } catch (e) {
    console.error(`error: could not sign — ${e?.message || e}. Is the private key a valid secp256k1 scalar (1 <= key < curve order)?`);
    process.exit(2);
  }
  const { headers, body: signedBody } = result;
  console.log(JSON.stringify({ headers, body: signedBody ?? null }, null, 2));
}

// Run the CLI only when executed directly — never on `import { signRequest }`.
// realpath both sides so a symlinked invocation path (e.g. /tmp → /private/tmp,
// or npm bin links) still matches the resolved module URL.
function isEntrypoint() {
  if (!process.argv[1]) return false;
  try {
    return realpathSync(process.argv[1]) === realpathSync(fileURLToPath(import.meta.url));
  } catch {
    return false;
  }
}
if (isEntrypoint()) main();
