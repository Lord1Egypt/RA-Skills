#!/usr/bin/env node
import "dotenv/config";
import express from "express";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { fetchOrderStatus, initiateTransaction, verifyCallbackChecksum } from "./paytmService.js";
import { createSubscription } from "./subscriptionService.js";
import { createPaymentLink, fetchLinkTransactions } from "./paymentLinkService.js";
import { createDynamicQr } from "./qrService.js";
import { getPaytmConfig } from "./paytmConfig.js";
import { getCached, setCached, readKey } from "./idempotency.js";
import { handleWebhook } from "./webhookHandler.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const app = express();
// Capture raw body bytes for webhook signature verification - Paytm signs the
// body it sent, so re-serializing in your language can change key order /
// whitespace and break the signature.
app.use(express.json({
  verify: (req, _res, buf) => { req.rawBody = buf?.toString("utf8") || ""; },
}));
app.use(express.urlencoded({ extended: false }));

function requestBase(req) {
  const protoRaw = (req.headers["x-forwarded-proto"] || req.protocol || "http").toString();
  const hostRaw = (req.headers["x-forwarded-host"] || req.headers.host || "localhost").toString();
  const proto = protoRaw.split(",")[0].trim();
  const host = hostRaw.split(",")[0].trim();
  return `${proto}://${host}`;
}

app.get("/paytm-client-config.json", (req, res) => {
  const cfg = getPaytmConfig();
  res.json({
    mid: cfg.mid,
    api_host: cfg.pgDomain,
    loader_url: cfg.checkoutJsLoaderUrl,
  });
});

// Wrap a create-handler with Idempotency-Key support so double-clicks don't
// produce two Paytm orders. See idempotency.js for the cache contract.
function withIdempotency(handler) {
  return async (req, res) => {
    const key = readKey(req);
    if (key) {
      const cached = getCached(key);
      if (cached) {
        res.setHeader("Idempotent-Replayed", "true");
        return res.status(cached.status).json(cached.body);
      }
    }
    try {
      const body = await handler(req);
      if (key) setCached(key, 200, body);
      res.json(body);
    } catch (e) {
      const status = Number(e?.httpStatus) || 500;
      const body = payloadFromError(e);
      // Cache failures only if Paytm-side definitive (4xx) - never on transient
      // 5xx so the next retry can succeed.
      if (key && status >= 400 && status < 500) setCached(key, status, body);
      res.status(status).json(body);
    }
  };
}

app.post("/paytm/create-order", withIdempotency(async (req) => {
  const { amount, custId, mobile, email, orderId } = req.body ?? {};
  return initiateTransaction({ amount, custId, mobile, email, orderId, serverBaseUrl: requestBase(req) });
}));

app.post("/paytm/create-subscription", withIdempotency(async (req) => {
  return createSubscription({ ...(req.body ?? {}), serverBaseUrl: requestBase(req) });
}));

app.post("/paytm/create-link", withIdempotency(async (req) => {
  return createPaymentLink({ ...(req.body ?? {}), serverBaseUrl: requestBase(req) });
}));

app.post("/paytm/create-qr", withIdempotency(async (req) => {
  return createDynamicQr({ ...(req.body ?? {}) });
}));

// Reconcile a Payment Link - POST /link/fetchTransaction. Use this for Payment
// Link flows instead of /v3/order/status; the response wraps each payer's
// order under body.orders[].
app.post("/paytm/link-transactions", async (req, res) => {
  try {
    const out = await fetchLinkTransactions({ ...(req.body ?? {}) });
    res.json(out);
  } catch (e) {
    res.status(Number(e?.httpStatus) || 500).json(payloadFromError(e));
  }
});

// S2S webhook from Paytm. Verifies head.signature, dedupes on (orderId, status),
// and applies a stub fulfillment hook. See webhookHandler.js for the contract.
app.post("/paytm/webhook", async (req, res) => {
  try {
    const result = await handleWebhook({ rawBody: req.rawBody, parsed: req.body });
    res.status(result.httpStatus).json({ ok: result.ok, ...(result.detail || {}) });
  } catch (e) {
    // 5xx so Paytm retries - never silently swallow a webhook we couldn't process.
    console.error("[paytm webhook] handler crash", e);
    res.status(500).json({ ok: false, error: e?.message || String(e) });
  }
});

function payloadFromError(e) {
  const out = { error: true, code: e?.code || "INTERNAL_ERROR", message: e?.message || String(e) };
  if (e?.orderId) out.orderId = e.orderId;
  if (e?.paytm) out.paytm = e.paytm;
  return out;
}

app.post("/paytm/order-status", async (req, res) => {
  try {
    const orderId = req.body?.orderId;
    if (!orderId) return res.status(400).json({ error: true, message: "orderId required" });
    const json = await fetchOrderStatus({ orderId });
    res.type("application/json").send(json);
  } catch (e) {
    res.status(500).json({ error: true, message: e?.message || String(e) });
  }
});

// Paytm posts callback fields directly from the user's browser, so EVERY value is
// untrusted input. HTML-escape before rendering or you've shipped reflected XSS.
function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function callbackHtml(params, checksumOk) {
  const lines = Object.entries(params || {})
    .map(([k, v]) => `${escapeHtml(k)}=${escapeHtml(Array.isArray(v) ? v.join(",") : v)}`)
    .join("\n");
  return [
    "<!DOCTYPE html><html><head><meta charset=\"UTF-8\"><title>Paytm callback</title></head><body>",
    "<h1>Paytm callback</h1>",
    `<p><strong>CHECKSUMHASH validation:</strong> ${checksumOk ? "OK (signature verified)" : "FAILED or CHECKSUMHASH missing - do not treat as paid"}</p>`,
    "<p>Also verify via Transaction Status API (or webhook) before confirming an order.</p>",
    `<pre>${lines}</pre>`,
    "</body></html>",
  ].join("");
}

app.post("/paytm/callback", (req, res) => {
  const params = req.body ?? {};
  const ok = verifyCallbackChecksum(params);
  res.type("text/html").send(callbackHtml(params, ok));
});

app.get("/paytm/callback", (req, res) => {
  const params = req.query ?? {};
  const ok = verifyCallbackChecksum(params);
  res.type("text/html").send(callbackHtml(params, ok));
});

// Single source of truth for frontend HTMLs lives at scripts/frontend/. Each
// backend serves it directly to avoid maintaining duplicate copies.
app.use(express.static(path.join(__dirname, "..", "frontend")));

const PORT = Number(process.env.PORT) || 3001;
app.listen(PORT, "127.0.0.1", () => {
  console.log(`Node backend running at http://localhost:${PORT}`);
});
