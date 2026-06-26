#!/usr/bin/env node

import {
  DEFAULT_BASE_URL,
  DEFAULT_TIMEOUT_MS,
  buildGhostWireRequestSpecHash,
  fetchWithTimeout,
  normalizeBaseUrl,
  normalizeGhostWireRequestPayload,
  parseCliArgs,
  parseJson,
  parsePositiveInt,
  printJson,
} from "./shared.mjs";

const HEX32_REGEX = /^0x[a-fA-F0-9]{64}$/;

const args = parseCliArgs();
const baseUrl = normalizeBaseUrl(args["base-url"] || process.env.GHOST_OPENCLAW_BASE_URL || DEFAULT_BASE_URL);
const timeoutMs = parsePositiveInt(args["timeout-ms"] || process.env.GHOST_OPENCLAW_TIMEOUT_MS, DEFAULT_TIMEOUT_MS);
const endpoint = `${baseUrl}/api/wire/jobs`;

const quoteId = String(args["quote-id"] || process.env.GHOSTWIRE_QUOTE_ID || "").trim();
const clientAddress = String(args.client || args["client-address"] || process.env.GHOSTWIRE_CLIENT_ADDRESS || "").trim();
const providerAddress = String(
  args.provider || args["provider-address"] || process.env.GHOSTWIRE_PROVIDER_ADDRESS || "",
).trim();
const evaluatorAddress = String(
  args.evaluator || args["evaluator-address"] || process.env.GHOSTWIRE_EVALUATOR_ADDRESS || "",
).trim();
const specHash = String(args["spec-hash"] || process.env.GHOSTWIRE_SPEC_HASH || "").trim();
const metadataUri = String(args["metadata-uri"] || process.env.GHOSTWIRE_METADATA_URI || "").trim();
const requestPrompt = String(args["request-prompt"] || process.env.GHOSTWIRE_REQUEST_PROMPT || "").trim();
const requestWallet = String(args["request-wallet"] || process.env.GHOSTWIRE_REQUEST_WALLET || "").trim();
const requestMetadataJson = String(args["request-metadata-json"] || process.env.GHOSTWIRE_REQUEST_METADATA_JSON || "").trim();
const requestJsonRaw = String(args["request-json"] || process.env.GHOSTWIRE_REQUEST_JSON || "").trim();
const webhookUrl = String(args["webhook-url"] || process.env.GHOSTWIRE_WEBHOOK_URL || "").trim();
const webhookSecret = String(args["webhook-secret"] || process.env.GHOSTWIRE_WEBHOOK_SECRET || "").trim();
const approvalMode = String(args["approval-mode"] || process.env.GHOSTWIRE_APPROVAL_MODE || "").trim();

let requestPayload = null;
if (requestJsonRaw) {
  const parsed = parseJson(requestJsonRaw, null);
  requestPayload = normalizeGhostWireRequestPayload(parsed);
} else if (requestPrompt) {
  requestPayload = normalizeGhostWireRequestPayload({
    prompt: requestPrompt,
    ...((requestWallet || clientAddress) ? { walletAddress: requestWallet || clientAddress } : {}),
    ...(requestMetadataJson ? { metadata: parseJson(requestMetadataJson, null) } : {}),
  });
}

if (specHash && requestPayload) {
  const derivedSpecHash = buildGhostWireRequestSpecHash(requestPayload);
  if (derivedSpecHash.toLowerCase() !== specHash.toLowerCase()) {
    printJson({
      ok: false,
      error: "request does not match the supplied --spec-hash / GHOSTWIRE_SPEC_HASH.",
      derivedSpecHash,
      suppliedSpecHash: specHash,
    });
    process.exit(1);
  }
}

const resolvedSpecHash = specHash || (requestPayload ? buildGhostWireRequestSpecHash(requestPayload) : "");

if (!quoteId || !clientAddress || !providerAddress || !evaluatorAddress || !resolvedSpecHash) {
  printJson({
    ok: false,
    error: "Missing required --quote-id, --client, --provider, --evaluator, and either --spec-hash or --request-prompt/--request-json.",
    example:
      "node integrations/openclaw-ghost-pay/bin/create-wire-job-from-quote.mjs --quote-id wq_... --client 0x... --provider 0x... --evaluator 0x... --request-prompt \"Roast my wallet honestly.\"",
  });
  process.exitCode = 1;
} else if (!HEX32_REGEX.test(resolvedSpecHash)) {
  printJson({
    ok: false,
    error: "Invalid resolved spec hash; expected 32-byte hex string (0x + 64 hex chars).",
  });
  process.exitCode = 1;
} else if ((webhookUrl && !webhookSecret) || (!webhookUrl && webhookSecret)) {
  printJson({
    ok: false,
    error: "webhook-url and webhook-secret must be provided together.",
  });
  process.exitCode = 1;
} else {
  try {
    const body = {
      quoteId,
      client: clientAddress,
      provider: providerAddress,
      evaluator: evaluatorAddress,
      specHash: resolvedSpecHash,
      request: requestPayload || undefined,
      metadataUri: metadataUri || undefined,
      webhookUrl: webhookUrl || undefined,
      webhookSecret: webhookSecret || undefined,
      approvalMode: approvalMode || undefined,
    };

    const response = await fetchWithTimeout(
      endpoint,
      {
        method: "POST",
        headers: {
          accept: "application/json",
          "content-type": "application/json",
        },
        body: JSON.stringify(body),
      },
      timeoutMs,
    );

    const rawText = await response.text();
    const payload = parseJson(rawText, null);

    if (!response.ok) {
      printJson({
        ok: false,
        status: response.status,
        endpoint,
        error: payload?.error || "GhostWire job preparation failed.",
        errorCode: payload?.errorCode || null,
        details: payload?.details || null,
        body: payload || rawText,
      });
      process.exitCode = 1;
    } else {
      printJson({
        ok: true,
        status: response.status,
        endpoint,
        preparedJob: payload,
      });
    }
  } catch (error) {
    printJson({
      ok: false,
      endpoint,
      error: error instanceof Error ? error.message : "Unknown failure",
    });
    process.exitCode = 1;
  }
}
