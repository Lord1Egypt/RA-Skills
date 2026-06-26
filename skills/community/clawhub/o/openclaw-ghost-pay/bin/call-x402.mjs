#!/usr/bin/env node

import { decodeXPaymentResponse, wrapFetchWithPayment } from "x402-fetch";
import { createSigner } from "x402/types";
import {
  DEFAULT_CHAIN_ID,
  DEFAULT_TIMEOUT_MS,
  normalizeOptionalString,
  parseCliArgs,
  parseJson,
  parsePositiveBigIntString,
  parsePositiveInt,
  printJson,
  toBool,
} from "./shared.mjs";

const CHAIN_ID_TO_NETWORK = {
  8453: "base",
  84532: "base-sepolia",
};

const args = parseCliArgs();
const url = normalizeOptionalString(args.url || process.env.GHOST_OPENCLAW_X402_URL);
const method = normalizeOptionalString(args.method)?.toUpperCase() || "GET";
const chainId = parsePositiveInt(args["chain-id"] || process.env.GHOST_OPENCLAW_CHAIN_ID, DEFAULT_CHAIN_ID);
const network = normalizeOptionalString(args.network || process.env.GHOST_OPENCLAW_X402_NETWORK) || CHAIN_ID_TO_NETWORK[chainId];
const timeoutMs = parsePositiveInt(args["timeout-ms"] || process.env.GHOST_OPENCLAW_TIMEOUT_MS, DEFAULT_TIMEOUT_MS);
const maxAmountAtomic = parsePositiveBigIntString(
  args["max-amount-atomic"] || process.env.GHOST_OPENCLAW_X402_MAX_AMOUNT_ATOMIC,
  "100000",
);
const bodyJsonArg = normalizeOptionalString(args["body-json"]);
const bodyJson = bodyJsonArg ? parseJson(bodyJsonArg, undefined) : undefined;
const headersJsonArg = normalizeOptionalString(args["headers-json"]);
const headersJson = headersJsonArg ? parseJson(headersJsonArg, undefined) : undefined;
const dryRun = toBool(args["dry-run"], false);
const privateKey = normalizeOptionalString(args["private-key"] || process.env.GHOST_SIGNER_PRIVATE_KEY);

if (!url) {
  printJson({
    ok: false,
    error: "Missing required --url (or GHOST_OPENCLAW_X402_URL).",
    example:
      "node integrations/openclaw-ghost-pay/bin/call-x402.mjs --url https://merchant.example.com/ask --method POST --body-json '{\"prompt\":\"hello\"}'",
  });
  process.exitCode = 1;
} else if (!network) {
  printJson({
    ok: false,
    error: `Unsupported chain id ${chainId}. Pass --network explicitly.`,
  });
  process.exitCode = 1;
} else if (bodyJsonArg && bodyJson === undefined) {
  printJson({
    ok: false,
    error: "Invalid JSON passed to --body-json.",
  });
  process.exitCode = 1;
} else if (headersJsonArg && (!headersJson || typeof headersJson !== "object" || Array.isArray(headersJson))) {
  printJson({
    ok: false,
    error: "Invalid JSON passed to --headers-json. Expected an object.",
  });
  process.exitCode = 1;
} else if (!privateKey && !dryRun) {
  printJson({
    ok: false,
    error: "Missing signer private key. Set GHOST_SIGNER_PRIVATE_KEY or pass --private-key.",
  });
  process.exitCode = 1;
} else {
  try {
    const requestHeaders = {
      accept: "application/json, text/plain;q=0.9, */*;q=0.8",
      ...(headersJson || {}),
    };

    if (dryRun) {
      printJson({
        ok: true,
        mode: "dry-run",
        request: {
          url,
          method,
          network,
          chainId,
          maxAmountAtomic,
          headers: requestHeaders,
          body: bodyJson ?? null,
        },
      });
      process.exit(0);
    }

    const signer = await createSigner(network, privateKey);
    const fetchWithPayment = wrapFetchWithPayment(globalThis.fetch, signer, BigInt(maxAmountAtomic));
    const response = await fetchWithPayment(
      url,
      {
        method,
        headers: {
          ...requestHeaders,
          ...(bodyJson !== undefined ? { "content-type": "application/json" } : {}),
        },
        ...(bodyJson !== undefined && method !== "GET" && method !== "HEAD" ? { body: JSON.stringify(bodyJson) } : {}),
      },
    );

    const rawBody = await response.text();
    const parsedBody = parseJson(rawBody, null);
    const paymentResponseHeader =
      response.headers.get("x-payment-response") || response.headers.get("X-PAYMENT-RESPONSE");

    printJson({
      ok: response.ok,
      status: response.status,
      url: response.url || url,
      request: {
        method,
        network,
        chainId,
        maxAmountAtomic,
      },
      response: {
        paymentResponseHeader,
        paymentResponse: paymentResponseHeader ? decodeXPaymentResponse(paymentResponseHeader) : null,
        body: parsedBody ?? rawBody,
      },
    });

    if (!response.ok) process.exitCode = 1;
  } catch (error) {
    printJson({
      ok: false,
      url,
      error: error instanceof Error ? error.message : "Unknown failure",
    });
    process.exitCode = 1;
  }
}
