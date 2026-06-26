// Create Dynamic QR - POST /paymentservices/qr/create
// Doc: https://www.paytmpayments.com/docs/api/create-qr-code-api
// Defaults & gotchas baked in:
//   - posId is REQUIRED (omitting it returns 400)
//   - amount must be a STRING with two decimals
//   - head requires clientId + version + signature
//   - Response `image` is RAW base64 - we prepend `data:image/png;base64,` here
//     so the frontend can drop it straight into <img src>.
import crypto from "node:crypto";
import PaytmChecksum from "paytmchecksum";
import { getPaytmConfig } from "./paytmConfig.js";

function normalizeAmount(amount) {
  // Two-decimal currency normalization. Integer-paise rounding to avoid
  // binary-float drift. Returns a string (Paytm QR `amount` contract).
  const n = Number(String(amount ?? "").trim());
  if (!Number.isFinite(n) || n <= 0) return "1.00";
  const rounded = Math.round((n + Number.EPSILON) * 100) / 100;
  return rounded.toFixed(2);
}

export async function createDynamicQr({
  amount,
  posId = "POS001",
  displayName,
  expiryDate,
  imageRequired = true,
  orderId: callerOrderId,
}) {
  const cfg = getPaytmConfig();
  if (!cfg.mid) throw asError("MISSING_MID", "Missing PAYTM_MID");
  if (!cfg.merchantKey) throw asError("MISSING_MERCHANT_KEY", "Missing PAYTM_MERCHANT_KEY");
  if (!posId || !String(posId).trim()) {
    throw asError("MISSING_POS_ID", "posId is required for QR creation (Paytm returns 400 without it)");
  }

  const orderId = callerOrderId?.trim()
    || `QR_${crypto.randomBytes(10).toString("hex").toUpperCase()}`;

  const body = {
    mid: cfg.mid,
    orderId,
    amount: normalizeAmount(amount),
    businessType: "UPI_QR_CODE",
    posId: String(posId).trim(),
    imageRequired: !!imageRequired,
    ...(displayName?.trim() ? { displayName: displayName.trim().slice(0, 30) } : {}),
    ...(expiryDate?.trim() ? { expiryDate: expiryDate.trim() } : {}),
  };

  const signature = await PaytmChecksum.generateSignature(JSON.stringify(body), cfg.merchantKey);
  const head = {
    clientId: cfg.clientId,
    version: "v1",
    signature,
  };

  const r = await fetch(cfg.qrCreateUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ head, body }),
  });
  const text = await r.text();
  if (!r.ok) throw upstream("QR_HTTP_ERROR", `qr/create HTTP ${r.status}`, orderId, text);

  const json = JSON.parse(text);
  const status = json?.body?.resultInfo?.resultStatus;
  if (status && status !== "SUCCESS" && status !== "S") {
    throw upstream("QR_FAILED", json?.body?.resultInfo?.resultMsg || "qr/create failed", orderId, text);
  }

  // Paytm returns `image` as RAW base64 (no data-URI prefix). Inject the prefix
  // server-side so the frontend can drop it into <img src> without surprises.
  const rawImage = json?.body?.image;
  const image = rawImage ? `data:image/png;base64,${rawImage}` : null;

  return {
    orderId,
    qrCodeId: json?.body?.qrCodeId,
    qrData: json?.body?.qrData,
    image,
    mid: cfg.mid,
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
