// Paytm S2S webhook receiver.
//
// Contract:
//   1. Read raw body bytes (we capture them in server.js via express.json verify).
//   2. Extract head.signature; verify against the body bytes Paytm signed.
//      Re-serializing here would change key order / whitespace and break the
//      signature - use the bytes Paytm sent.
//   3. Idempotency check: (orderId, status) - Paytm retries at-least-once.
//   4. Persist event for audit (here, just an in-memory log).
//   5. Apply state transition (here, a stub `fulfillOrder` hook - replace with
//      your real DB write).
//   6. Return 200 fast. Heavy lifting (emails, accounting) goes to a queue.
//
// PRODUCTION NOTES:
//   - Replace the in-memory dedup set with Redis / a DB unique-index on
//     (orderId, status).
//   - Whitelist Paytm's egress IPs at your firewall (request the current list
//     from Paytm support).
//   - Return 5xx on processing errors so Paytm retries; do NOT return 200 on
//     handler crashes.
import PaytmChecksum from "paytmchecksum";
import { getPaytmConfig } from "./paytmConfig.js";

const seen = new Set();                       // `${orderId}|${status}` - at-least-once dedup
const SEEN_MAX = 50_000;
const eventLog = [];                          // ring buffer for /paytm/webhook/events
const EVENT_LOG_MAX = 200;

function rememberEvent(parsed) {
  eventLog.push({ at: new Date().toISOString(), payload: parsed });
  if (eventLog.length > EVENT_LOG_MAX) eventLog.shift();
}

export function recentEvents() {
  return eventLog.slice().reverse();
}

/**
 * Substring of the raw body that corresponds to "body": {...}.
 * Paytm signs those bytes verbatim - re-serializing the parsed object would
 * change key order / whitespace and break the signature.
 */
function extractBodyBytes(rawBody) {
  if (!rawBody) return null;
  // Find the literal substring `"body":` then walk braces.
  const m = rawBody.match(/"body"\s*:\s*\{/);
  if (!m) return null;
  const start = m.index + m[0].length - 1;     // position of the opening '{'
  let depth = 0;
  let inString = false;
  let escape = false;
  for (let i = start; i < rawBody.length; i++) {
    const c = rawBody[i];
    if (escape) { escape = false; continue; }
    if (c === "\\") { escape = true; continue; }
    if (c === '"') { inString = !inString; continue; }
    if (inString) continue;
    if (c === "{") depth++;
    else if (c === "}") {
      depth--;
      if (depth === 0) return rawBody.slice(start, i + 1);
    }
  }
  return null;
}

export async function handleWebhook({ rawBody, parsed }) {
  const cfg = getPaytmConfig();
  if (!cfg.merchantKey) {
    return { ok: false, httpStatus: 500, detail: { error: "merchant key not configured" } };
  }

  const signature = parsed?.head?.signature;
  if (!signature) {
    return { ok: false, httpStatus: 401, detail: { error: "missing head.signature" } };
  }

  // Verify the signed body bytes (NOT a re-serialization).
  const bodyBytes = extractBodyBytes(rawBody) || JSON.stringify(parsed?.body || {});
  let signatureOk = false;
  try {
    signatureOk = PaytmChecksum.verifySignature(bodyBytes, cfg.merchantKey, signature);
  } catch {
    signatureOk = false;
  }
  if (!signatureOk) {
    return { ok: false, httpStatus: 401, detail: { error: "invalid signature" } };
  }

  // Persist for audit BEFORE dedup so we can see duplicates if they arrive.
  rememberEvent(parsed);

  // Idempotency: at-least-once delivery means duplicates are normal.
  // Key on (orderId, status) - Paytm always sets both for terminal events.
  const orderId = parsed?.body?.orderId;
  const status = parsed?.body?.status || parsed?.body?.STATUS;
  const dedupKey = `${orderId || "unknown"}|${status || "unknown"}`;
  if (seen.has(dedupKey)) {
    return { ok: true, httpStatus: 200, detail: { dedup: true, orderId, status } };
  }
  if (seen.size >= SEEN_MAX) seen.clear();   // crude wrap; Redis has TTLs in real life
  seen.add(dedupKey);

  // Apply state transition. Stub here - replace with your real fulfillment.
  await fulfillOrder({ orderId, status, parsed });

  return { ok: true, httpStatus: 200, detail: { orderId, status } };
}

/**
 * Replace this with your real DB write / queue push. Keep it FAST - webhook
 * timeout is 10s; queue heavy work (emails, accounting) if needed.
 */
async function fulfillOrder({ orderId, status, parsed }) {
  // eslint-disable-next-line no-console
  console.log("[paytm webhook] fulfill stub", { orderId, status, mid: parsed?.body?.mid });
}
