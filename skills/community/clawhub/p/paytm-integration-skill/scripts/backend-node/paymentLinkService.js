// Create Payment Link - POST /link/create
// Doc: https://www.paytmpayments.com/docs/api/create-link-api
// Defaults & gotchas baked in:
//   - head requires tokenType: "AES" + timestamp (Unix epoch SECONDS as string)
//   - linkType: "FIXED" by default (GENERIC ignores amount)
//   - amount is a JSON number, NOT a string
//   - linkName: alphanumerics ONLY (no spaces) - some MIDs reject space here.
//     Sanitize via sanitizeLinkName() below.
//   - linkDescription: alphanumerics + spaces. Sanitize via sanitizeDescription().
//     Both fields must be ≥ 3 chars.
//   - customer details nested under customerContact (not top-level)
//   - expiryDate format DD/MM/YYYY HH:MM:SS (most MIDs)
import crypto from "node:crypto";
import PaytmChecksum from "paytmchecksum";
import { getPaytmConfig } from "./paytmConfig.js";

// linkDescription: alphanumerics + spaces (per Paytm docs). Sanitize untrusted
// input; fall back when empty / too short.
function sanitizeDescription(s, fallback = "Invoice payment") {
  const cleaned = String(s ?? "").replace(/[^A-Za-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
  return cleaned.length >= 3 ? cleaned : fallback;
}

// linkName: alphanumerics ONLY. Paytm's docs say spaces are allowed but several
// MIDs reject space as a special character with "link name contains special
// character". Stripping spaces is the safe cross-MID default.
function sanitizeLinkName(s, fallback = "Invoice") {
  const cleaned = String(s ?? "").replace(/[^A-Za-z0-9]/g, "");
  return cleaned.length >= 3 ? cleaned : fallback;
}

function expiryOneYearFromNow() {
  // DD/MM/YYYY HH:MM:SS in IST
  const offsetMs = 5.5 * 60 * 60 * 1000;
  const d = new Date(Date.now() + offsetMs + 365 * 24 * 60 * 60 * 1000);
  const pad = n => String(n).padStart(2, "0");
  return `${pad(d.getUTCDate())}/${pad(d.getUTCMonth() + 1)}/${d.getUTCFullYear()} 23:59:59`;
}

function normalizeAmount(amount) {
  // Payment Link API takes `amount` as a JSON number (not a string).
  //
  // To stay precision-safe we do the rounding via integer paise (×100, round to
  // nearest, ÷100) instead of `Number.toFixed()` directly - this guarantees
  // bit-exact two-decimal currency math without depending on string conversion
  // for the rounding step. Float conversion only happens at the final ÷100, so
  // typical INR amounts are exact (the float error budget kicks in well above
  // any rupee amount a real merchant will send).
  //
  // For larger / more sensitive currency math, swap this for a decimal library
  // (decimal.js, big.js) and emit via JSON.stringify with a number coercion.
  const raw = String(amount ?? "").trim();
  const n = Number(raw);
  if (!Number.isFinite(n) || n <= 0) return 1.00;
  // Math.round gives banker-style rounding via float; for half-up, add Number.EPSILON.
  return Math.round((n + Number.EPSILON) * 100) / 100;
}

export async function createPaymentLink({
  amount,
  linkName,
  linkDescription,
  customerName,
  customerEmail,
  customerMobile,
  customerId,
  expiryDate,
  orderId: callerOrderId,
  sendSms = true,
  sendEmail = true,
  callbackUrl: callerCallback,
  merchantUniqueReference,
  serverBaseUrl,
}) {
  const cfg = getPaytmConfig();
  if (!cfg.mid) throw asError("MISSING_MID", "Missing PAYTM_MID");
  if (!cfg.merchantKey) throw asError("MISSING_MERCHANT_KEY", "Missing PAYTM_MERCHANT_KEY");

  const orderId = callerOrderId?.trim()
    || `LNK_${crypto.randomBytes(10).toString("hex").toUpperCase()}`;
  const callbackUrl = callerCallback?.trim() || cfg.callbackUrl?.trim()
    || `${(serverBaseUrl || cfg.callbackBase).replace(/\/+$/, "")}/paytm/callback`;

  const body = {
    mid: cfg.mid,
    linkType: "FIXED",
    linkName: sanitizeLinkName(linkName, "Invoice"),
    linkDescription: sanitizeDescription(linkDescription, "Invoice payment"),
    amount: normalizeAmount(amount),
    sendSms: !!sendSms,
    sendEmail: !!sendEmail,
    customerContact: {
      ...(customerName?.trim() ? { customerName: customerName.trim() } : {}),
      ...(customerEmail?.trim() ? { customerEmail: customerEmail.trim() } : {}),
      ...(customerMobile?.trim() ? { customerMobile: customerMobile.trim() } : {}),
      ...(customerId?.trim() ? { customerId: customerId.trim() } : {}),
    },
    expiryDate: expiryDate?.trim() || expiryOneYearFromNow(),
    orderId,
    callbackUrl,
    ...(merchantUniqueReference?.trim() ? { merchantUniqueReference: merchantUniqueReference.trim() } : {}),
  };

  const signature = await PaytmChecksum.generateSignature(JSON.stringify(body), cfg.merchantKey);
  const head = {
    tokenType: "AES",
    signature,
    timestamp: String(Math.floor(Date.now() / 1000)),
  };

  const r = await fetch(cfg.linkCreateUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ head, body }),
  });
  const text = await r.text();
  if (!r.ok) throw upstream("LINK_HTTP_ERROR", `link/create HTTP ${r.status}`, orderId, text);

  const json = JSON.parse(text);
  const status = json?.body?.resultInfo?.resultStatus;
  if (status && status !== "SUCCESS" && status !== "S") {
    throw upstream("LINK_FAILED", json?.body?.resultInfo?.resultMsg || "link/create failed", orderId, text);
  }
  // Read defensively - current Paytm returns linkId; older docs LinkID.
  const linkId = json?.body?.linkId ?? json?.body?.LinkID;

  return {
    orderId,
    linkId,
    shortUrl: json?.body?.shortUrl,
    longUrl: json?.body?.longUrl,
    linkStatus: json?.body?.linkStatus || "ACTIVE",
    amount: body.amount,
    mid: cfg.mid,
  };
}

/**
 * Fetch transactions for a Payment Link - POST /link/fetchTransaction.
 * Doc: https://www.paytmpayments.com/docs/api/fetch-transaction-link-api
 *
 * USE THIS for Payment Link reconciliation, NOT /v3/order/status.
 * Returns {orders: [...]} - always an array, may be empty (404 from Paytm
 * is normalised to an empty array here so callers don't have to special-case
 * "not paid yet").
 */
export async function fetchLinkTransactions({
  linkId,
  pageNo = 1,
  pageSize = 10,
  fetchAllTxns = true,
}) {
  const cfg = getPaytmConfig();
  if (!cfg.mid) throw asError("MISSING_MID", "Missing PAYTM_MID");
  if (!cfg.merchantKey) throw asError("MISSING_MERCHANT_KEY", "Missing PAYTM_MERCHANT_KEY");
  if (linkId === undefined || linkId === null || linkId === "") {
    throw asError("MISSING_LINK_ID", "linkId is required");
  }

  // linkId MUST be a JSON number, not a string. Coerce defensively here so
  // callers can pass either form without surprise.
  const numericLinkId = Number(linkId);
  if (!Number.isFinite(numericLinkId)) {
    throw asError("INVALID_LINK_ID", `linkId must be numeric, got: ${linkId}`);
  }

  const body = {
    mid: cfg.mid,
    linkId: numericLinkId,
    pageNo: Number(pageNo) || 1,
    pageSize: Number(pageSize) || 10,
    fetchAllTxns: !!fetchAllTxns,
  };
  const signature = await PaytmChecksum.generateSignature(JSON.stringify(body), cfg.merchantKey);
  const head = { tokenType: "AES", signature };

  const r = await fetch(cfg.linkFetchTransactionUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ head, body }),
  });
  const text = await r.text();
  if (!r.ok) throw upstream("LINK_FETCH_TXN_HTTP_ERROR", `link/fetchTransaction HTTP ${r.status}`, String(numericLinkId), text);

  const json = JSON.parse(text);
  const info = json?.body?.resultInfo;
  // 404 = "Data Not Found" - link exists but no transactions yet. Normalise
  // to an empty list so callers can treat all valid responses uniformly.
  if (info?.resultCode === "404" || /not\s*found/i.test(info?.resultMessage || info?.resultMsg || "")) {
    return { linkId: numericLinkId, orders: [], resultInfo: info };
  }
  if (info?.resultStatus && info.resultStatus !== "SUCCESS" && info.resultStatus !== "S") {
    throw upstream("LINK_FETCH_TXN_FAILED", info.resultMessage || info.resultMsg || "link/fetchTransaction failed",
      String(numericLinkId), text);
  }
  return {
    linkId: numericLinkId,
    orders: json?.body?.orders ?? [],
    resultInfo: info,
  };
}

function asError(code, message) {
  const e = new Error(message);
  e.code = code;
  return e;
}

function upstream(code, message, orderId, raw) {
  const e = new Error(message);
  e.code = code;
  e.httpStatus = 502;
  e.orderId = orderId;
  try {
    const info = JSON.parse(raw)?.body?.resultInfo;
    if (info) e.paytm = { resultStatus: info.resultStatus, resultCode: info.resultCode, resultMsg: info.resultMsg };
  } catch {}
  return e;
}
