// Native Create Subscription - POST /subscription/create
// Doc: https://www.paytmpayments.com/docs/api/initiate-subscription-api
// Defaults baked in:
//   - subscriptionPaymentMode: "UNKNOWN"  (Paytm renders all enabled rails)
//   - txnAmount.value: "2.00"             (CC/DC mandates require > ₹1)
//   - subscriptionGraceDays: "3"          (CC/DC max)
//   - subscriptionStartDate: today (IST)
//   - subscriptionEnableRetry: "0"        (retry off; subscriptionRetryCount omitted)
import crypto from "node:crypto";
import PaytmChecksum from "paytmchecksum";
import { getPaytmConfig } from "./paytmConfig.js";

function sanitizeCustId(s) {
  return (s || "CUST_DEMO").replace(/[^a-zA-Z0-9_]/g, "_");
}

function todayIST() {
  // YYYY-MM-DD in IST regardless of server timezone.
  const offsetMs = 5.5 * 60 * 60 * 1000;
  return new Date(Date.now() + offsetMs).toISOString().slice(0, 10);
}

function plusOneYear(yyyymmdd) {
  const [y, m, d] = yyyymmdd.split("-").map(Number);
  return `${y + 1}-${String(m).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
}

function normalizeAmount(amount, minRupees = 2) {
  // Two-decimal currency normalization, integer-paise rounding to avoid
  // binary-float drift. Returns a string (Paytm subscription `txnAmount.value`
  // contract).
  const n = Number(String(amount ?? "").trim());
  if (!Number.isFinite(n) || n < minRupees) return minRupees.toFixed(2);
  const rounded = Math.round((n + Number.EPSILON) * 100) / 100;
  return rounded.toFixed(2);
}

export async function createSubscription({
  amount,                           // first-debit amount (string/number, ≥ ₹2 for cross-rail)
  renewalAmount,                    // optional; only set if you want a different recurring amount
  custId,
  mobile,
  email,
  firstName,
  lastName,
  frequency = "1",                  // number of units per cycle
  frequencyUnit = "MONTH",          // DAY | WEEK | MONTH | YEAR | ONDEMAND
  amountType = "FIX",               // FIX | VARIABLE (VARIABLE requires subscriptionMaxAmount)
  maxAmount,                        // required when amountType === "VARIABLE"
  startDate,                        // YYYY-MM-DD; defaults to today
  expiryDate,                       // YYYY-MM-DD; defaults to startDate + 1 year
  graceDays = "3",
  paymentMode = "UNKNOWN",          // CC | DC | BANK_MANDATE | UNKNOWN
  mandateType,                      // E_MANDATE | PAPER_MANDATE - only with BANK_MANDATE
  orderId: callerOrderId,
  serverBaseUrl,
}) {
  const cfg = getPaytmConfig();
  if (!cfg.mid) throw asError("MISSING_MID", "Missing PAYTM_MID");
  if (!cfg.merchantKey) throw asError("MISSING_MERCHANT_KEY", "Missing PAYTM_MERCHANT_KEY");

  const orderId = callerOrderId?.trim()
    || `SUB_${crypto.randomBytes(10).toString("hex").toUpperCase()}`;
  const traceId = `TRC_${crypto.randomBytes(10).toString("hex").toUpperCase()}`;
  const start = startDate?.trim() || todayIST();
  const expiry = expiryDate?.trim() || plusOneYear(start);
  const callbackUrl = cfg.callbackUrl?.trim()
    || `${(serverBaseUrl || cfg.callbackBase).replace(/\/+$/, "")}/paytm/callback`;

  const body = {
    requestType: "NATIVE_SUBSCRIPTION",
    mid: cfg.mid,
    orderId,
    websiteName: cfg.websiteName,
    txnAmount: { value: normalizeAmount(amount), currency: "INR" },
    subscriptionPaymentMode: paymentMode,
    subscriptionAmountType: amountType,
    subscriptionFrequency: String(frequency),
    subscriptionFrequencyUnit: frequencyUnit,
    subscriptionStartDate: start,
    subscriptionExpiryDate: expiry,
    subscriptionGraceDays: String(graceDays),
    subscriptionEnableRetry: "0",
    userInfo: {
      custId: sanitizeCustId(custId),
      ...(mobile?.trim() ? { mobile: mobile.trim() } : {}),
      ...(email?.trim() ? { email: email.trim() } : {}),
      ...(firstName?.trim() ? { firstName: firstName.trim() } : {}),
      ...(lastName?.trim() ? { lastName: lastName.trim() } : {}),
    },
    callbackUrl,
  };
  if (amountType === "VARIABLE") {
    if (!maxAmount) throw asError("MISSING_MAX_AMOUNT", "subscriptionMaxAmount required for VARIABLE amount type");
    body.subscriptionMaxAmount = normalizeAmount(maxAmount);
  } else if (maxAmount) {
    body.subscriptionMaxAmount = normalizeAmount(maxAmount);
  }
  if (renewalAmount) body.renewalAmount = normalizeAmount(renewalAmount);
  if (paymentMode === "BANK_MANDATE") {
    body.mandateType = mandateType || "E_MANDATE";
  }

  const signature = await PaytmChecksum.generateSignature(JSON.stringify(body), cfg.merchantKey);
  const head = {
    clientId: cfg.clientId,
    channelId: "WEB",
    version: "v1",
    requestTimestamp: String(Date.now()),
    signature,
  };

  const url = new URL(cfg.subscriptionCreateUrl);
  url.searchParams.set("mid", cfg.mid);
  url.searchParams.set("orderId", orderId);
  url.searchParams.set("traceId", traceId);

  const r = await fetch(url.toString(), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ head, body }),
  });
  const text = await r.text();
  if (!r.ok) throw upstream("SUBSCRIPTION_HTTP_ERROR", `subscription/create HTTP ${r.status}`, orderId, text);

  const json = JSON.parse(text);
  const status = json?.body?.resultInfo?.resultStatus;
  if (status !== "S") {
    throw upstream("SUBSCRIPTION_FAILED", json?.body?.resultInfo?.resultMsg || "subscription/create failed", orderId, text);
  }
  return {
    orderId,
    traceId,
    txnToken: json?.body?.txnToken,
    subscriptionId: json?.body?.subscriptionId,
    amount: body.txnAmount.value,
    mid: cfg.mid,
    tokenType: "TXN_TOKEN",
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
