#!/usr/bin/env node

import { privateKeyToAccount } from "viem/accounts";
import {
  DEFAULT_BASE_URL,
  DEFAULT_TIMEOUT_MS,
  DEFAULT_X402_SCHEME,
  fetchWithTimeout,
  normalizeBaseUrl,
  normalizeOptionalString,
  parseCliArgs,
  parseJson,
  parsePositiveBigIntString,
  parsePositiveInt,
  printJson,
  toBool,
} from "./shared.mjs";

const buildMerchantGatewayAuthPayload = (input) => ({
  scope: "agent_gateway",
  version: "1",
  action: "x402_settlement_report",
  agentId: input.agentId,
  ownerAddress: input.ownerAddress.toLowerCase(),
  actorAddress: input.actorAddress.toLowerCase(),
  serviceSlug: input.serviceSlug,
  nonce: crypto.randomUUID().replace(/-/g, ""),
  issuedAt: Math.floor(Date.now() / 1000),
});

const buildMerchantGatewayAuthMessage = (payload) =>
  [
    "Ghost Protocol Merchant Gateway Authorization",
    `scope:${payload.scope}`,
    `version:${payload.version}`,
    `action:${payload.action}`,
    `agentId:${payload.agentId}`,
    `serviceSlug:${payload.serviceSlug}`,
    `ownerAddress:${payload.ownerAddress}`,
    `actorAddress:${payload.actorAddress}`,
    `issuedAt:${payload.issuedAt}`,
    `nonce:${payload.nonce}`,
  ].join("\n");

const args = parseCliArgs();
const baseUrl = normalizeBaseUrl(args["base-url"] || process.env.GHOST_OPENCLAW_BASE_URL || DEFAULT_BASE_URL);
const agentId = normalizeOptionalString(args["agent-id"] || process.env.GHOST_OPENCLAW_AGENT_ID);
const serviceSlug = normalizeOptionalString(args.service || args["service-slug"] || process.env.GHOST_OPENCLAW_SERVICE_SLUG);
const requestId = normalizeOptionalString(args["request-id"]);
const paymentReference = normalizeOptionalString(args["payment-reference"]);
const payerIdentity = normalizeOptionalString(args["payer-identity"]);
const payerAddress = normalizeOptionalString(args["payer-address"]);
const scheme = normalizeOptionalString(args.scheme) || DEFAULT_X402_SCHEME;
const network = normalizeOptionalString(args.network);
const chainId = parsePositiveInt(args["chain-id"], 0) || undefined;
const asset = normalizeOptionalString(args.asset) || "USDC";
const amountAtomic = parsePositiveBigIntString(args["amount-atomic"], "");
const decimals = parsePositiveInt(args.decimals, 6);
const success = toBool(args.success, true);
const statusCode = normalizeOptionalString(args["status-code"]);
const latencyMs = normalizeOptionalString(args["latency-ms"]);
const occurredAt = normalizeOptionalString(args["occurred-at"]) || new Date().toISOString();
const metadataJsonArg = normalizeOptionalString(args["metadata-json"]);
const metadata = metadataJsonArg ? parseJson(metadataJsonArg, undefined) : undefined;
const timeoutMs = parsePositiveInt(args["timeout-ms"] || process.env.GHOST_OPENCLAW_TIMEOUT_MS, DEFAULT_TIMEOUT_MS);
const privateKey = normalizeOptionalString(args["private-key"] || process.env.GHOST_SIGNER_PRIVATE_KEY);

if (!agentId || !serviceSlug || !requestId || !paymentReference || !payerIdentity || !amountAtomic) {
  printJson({
    ok: false,
    error:
      "Missing required args. Need --agent-id, --service, --request-id, --payment-reference, --payer-identity, and --amount-atomic.",
  });
  process.exitCode = 1;
} else if (!privateKey) {
  printJson({
    ok: false,
    error: "Missing signer private key. Set GHOST_SIGNER_PRIVATE_KEY or pass --private-key.",
  });
  process.exitCode = 1;
} else if (metadataJsonArg && metadata === undefined) {
  printJson({
    ok: false,
    error: "Invalid JSON passed to --metadata-json.",
  });
  process.exitCode = 1;
} else {
  try {
    const actorAddress = privateKeyToAccount(privateKey).address.toLowerCase();
    const ownerLookupUrl = `${baseUrl}/api/agent-gateway/config?agentId=${encodeURIComponent(agentId)}`;
    const ownerLookupResponse = await fetchWithTimeout(
      ownerLookupUrl,
      {
        method: "GET",
        headers: {
          accept: "application/json",
        },
      },
      timeoutMs,
    );
    const ownerLookupBody = await ownerLookupResponse.json();
    const ownerAddress = normalizeOptionalString(ownerLookupBody?.config?.ownerAddress);
    if (!ownerLookupResponse.ok || !ownerAddress) {
      throw new Error("Failed to resolve gateway owner address for x402 settlement reporting.");
    }

    const authPayload = buildMerchantGatewayAuthPayload({
      agentId,
      ownerAddress,
      actorAddress,
      serviceSlug,
    });
    const authSignature = await privateKeyToAccount(privateKey).signMessage({
      message: buildMerchantGatewayAuthMessage(authPayload),
    });

    const endpoint = `${baseUrl}/api/telemetry/x402/settlements`;
    const response = await fetchWithTimeout(
      endpoint,
      {
        method: "POST",
        headers: {
          accept: "application/json",
          "content-type": "application/json",
        },
        body: JSON.stringify({
          agentId,
          ownerAddress,
          actorAddress,
          serviceSlug,
          requestId,
          paymentReference,
          payerIdentity,
          ...(payerAddress ? { payerAddress } : {}),
          scheme,
          ...(network ? { network } : {}),
          ...(chainId ? { chainId } : {}),
          asset,
          amountAtomic,
          decimals,
          success,
          ...(statusCode ? { statusCode: Number.parseInt(statusCode, 10) } : {}),
          ...(latencyMs ? { latencyMs: Number.parseInt(latencyMs, 10) } : {}),
          occurredAt,
          ...(metadata ? { metadata } : {}),
          authPayload,
          authSignature,
        }),
      },
      timeoutMs,
    );

    const rawBody = await response.text();
    const parsedBody = parseJson(rawBody, null);
    printJson({
      ok: response.ok,
      status: response.status,
      endpoint,
      body: parsedBody ?? rawBody,
    });
    if (!response.ok) process.exitCode = 1;
  } catch (error) {
    printJson({
      ok: false,
      error: error instanceof Error ? error.message : "Unknown failure",
    });
    process.exitCode = 1;
  }
}
