import crypto from "node:crypto";
import PaytmChecksum from "paytmchecksum";
import { getPaytmConfig } from "./paytmConfig.js";

function normalizeAmount(amount) {
  // Two-decimal currency normalization. We round via integer paise (×100,
  // round-half-up via Number.EPSILON, ÷100) to avoid binary-float drift, then
  // emit as a string with exactly two decimals - Paytm's `txnAmount.value`
  // contract.
  const raw = (amount ?? "").toString().trim();
  if (!raw) return "1.00";
  const n = Number(raw);
  if (!Number.isFinite(n) || n <= 0) return "1.00";
  const rounded = Math.round((n + Number.EPSILON) * 100) / 100;
  return rounded.toFixed(2);
}

export function requireCredentials() {
  const cfg = getPaytmConfig();
  if (!cfg.mid) {
    const err = new Error("Missing PAYTM_MID");
    err.code = "MISSING_MID";
    throw err;
  }
  if (!cfg.merchantKey) {
    const err = new Error("Missing PAYTM_MERCHANT_KEY");
    err.code = "MISSING_MERCHANT_KEY";
    throw err;
  }
  return cfg;
}

export async function initiateTransaction({ amount, custId, mobile, email, orderId: callerOrderId, serverBaseUrl }) {
  const cfg = requireCredentials();
  // Accept a merchant-supplied orderId for reconciliation against your own orders table.
  // Falls back to a random 20-hex-char id when not supplied.
  const orderId = callerOrderId?.trim() || `ORD_${crypto.randomBytes(10).toString("hex").toUpperCase()}`;
  const effectiveBase = (serverBaseUrl ?? "").toString().trim() || cfg.callbackBase;
  const callbackUrl = cfg.callbackUrl?.trim() || `${effectiveBase}/paytm/callback`;

  const body = {
    requestType: "Payment",
    mid: cfg.mid,
    websiteName: cfg.websiteName,
    orderId,
    callbackUrl: callbackUrl,
    txnAmount: { value: normalizeAmount(amount), currency: "INR" },
    userInfo: {
      custId: custId?.trim() ? custId.trim() : "CUST_DEMO",
      // mobile + email are strongly recommended - pre-fill the consent screen and
      // drive OTP / notifications. Real merchants should always pass these through.
      ...(mobile?.trim() ? { mobile: mobile.trim() } : {}),
      ...(email?.trim() ? { email: email.trim() } : {}),
    },
  };

  const signature = await PaytmChecksum.generateSignature(JSON.stringify(body), cfg.merchantKey);
  const payload = { body, head: { signature } };

  const url = new URL(cfg.initiateTransactionUrl);
  url.searchParams.set("mid", cfg.mid);
  url.searchParams.set("orderId", orderId);

  const r = await fetch(url.toString(), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const text = await r.text();
  if (!r.ok) throw asPaytmUpstreamError("INITIATE_HTTP_ERROR", `initiateTransaction failed (HTTP ${r.status})`, orderId, text);

  const json = JSON.parse(text);
  const status = json?.body?.resultInfo?.resultStatus;
  if (status !== "S") {
    const msg = json?.body?.resultInfo?.resultMsg || "initiateTransaction failed";
    throw asPaytmUpstreamError("INITIATE_FAILED", msg, orderId, text);
  }

  const txnToken = json?.body?.txnToken;
  if (!txnToken) throw asPaytmUpstreamError("MISSING_TXN_TOKEN", "Missing txnToken in Paytm response", orderId, text);

  return { orderId, txnToken, amount: body.txnAmount.value, mid: cfg.mid, tokenType: "TXN_TOKEN" };
}

export async function fetchOrderStatus({ orderId }) {
  const cfg = requireCredentials();
  const body = { mid: cfg.mid, orderId };
  const signature = await PaytmChecksum.generateSignature(JSON.stringify(body), cfg.merchantKey);
  const payload = { body, head: { signature } };

  const r = await fetch(cfg.orderStatusUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const text = await r.text();
  if (!r.ok) throw new Error(`order status HTTP ${r.status} - ${text}`);
  return text;
}

export function verifyCallbackChecksum(params) {
  const cfg = getPaytmConfig();
  const signature = params?.CHECKSUMHASH;
  if (!signature || !cfg.merchantKey) return false;

  const toVerify = { ...params };
  delete toVerify.CHECKSUMHASH;
  try {
    return PaytmChecksum.verifySignature(toVerify, cfg.merchantKey, signature);
  } catch {
    // Library can throw on malformed/empty input - treat as failed verification.
    return false;
  }
}

function asPaytmUpstreamError(code, message, orderId, rawBody) {
  const e = new Error(message);
  e.code = code;
  e.orderId = orderId;
  e.httpStatus = 502;
  e.paytm = {};
  try {
    const json = JSON.parse(rawBody);
    const info = json?.body?.resultInfo ?? {};
    if (info.resultStatus) e.paytm.resultStatus = info.resultStatus;
    if (info.resultCode) e.paytm.resultCode = info.resultCode;
    if (info.resultMsg) e.paytm.resultMsg = info.resultMsg;
  } catch {
    // ignore
  }
  if (Object.keys(e.paytm).length === 0) delete e.paytm;
  return e;
}
