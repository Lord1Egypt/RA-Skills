#!/usr/bin/env node

import {
  DEFAULT_BASE_URL,
  DEFAULT_CHAIN_ID,
  DEFAULT_TIMEOUT_MS,
  fetchWithTimeout,
  normalizeBaseUrl,
  parseCliArgs,
  parseJson,
  parsePositiveInt,
  printJson,
} from "./shared.mjs";

const args = parseCliArgs();
const baseUrl = normalizeBaseUrl(args["base-url"] || process.env.GHOST_OPENCLAW_BASE_URL || DEFAULT_BASE_URL);
const timeoutMs = parsePositiveInt(args["timeout-ms"] || process.env.GHOST_OPENCLAW_TIMEOUT_MS, DEFAULT_TIMEOUT_MS);
const endpoint = `${baseUrl}/api/mcp/read-only`;

const providerAddress = String(
  args.provider || args["provider-address"] || process.env.GHOSTWIRE_PROVIDER_ADDRESS || "",
).trim();
const evaluatorAddress = String(
  args.evaluator || args["evaluator-address"] || process.env.GHOSTWIRE_EVALUATOR_ADDRESS || "",
).trim();
const clientAddress = String(args.client || args["client-address"] || process.env.GHOSTWIRE_CLIENT_ADDRESS || "").trim();
const principalAmount = String(
  args["principal-amount"] || args.principal || process.env.GHOSTWIRE_PRINCIPAL_AMOUNT || "",
).trim();
const chainId = parsePositiveInt(args["chain-id"] || process.env.GHOST_OPENCLAW_CHAIN_ID, DEFAULT_CHAIN_ID);
const settlementAsset = String(args["settlement-asset"] || process.env.GHOSTWIRE_SETTLEMENT_ASSET || "USDC").trim();

if (!clientAddress || !providerAddress || !evaluatorAddress || !principalAmount) {
  printJson({
    ok: false,
    error: "Missing required --client, --provider, --evaluator, or --principal-amount.",
    example:
      "node integrations/openclaw-ghost-pay/bin/get-wire-quote.mjs --client 0x... --provider 0x... --evaluator 0x... --principal-amount 1000000",
  });
  process.exitCode = 1;
} else {
  try {
    const rpcPayload = {
      jsonrpc: "2.0",
      id: `oc-wire-quote-${Date.now()}`,
      method: "tools/call",
      params: {
        name: "get_wire_quote",
        arguments: {
          provider_address: providerAddress,
          evaluator_address: evaluatorAddress,
          client_address: clientAddress,
          principal_amount: principalAmount,
          chain_id: chainId,
          settlement_asset: settlementAsset,
        },
      },
    };

    const response = await fetchWithTimeout(
      endpoint,
      {
        method: "POST",
        headers: {
          accept: "application/json",
          "content-type": "application/json",
        },
        body: JSON.stringify(rpcPayload),
      },
      timeoutMs,
    );

    const rawText = await response.text();
    const body = parseJson(rawText, null);
    const rpcError = body?.error ?? null;
    const rpcResult = body?.result ?? null;
    const structured = rpcResult?.structuredContent ?? null;
    const textContent = Array.isArray(rpcResult?.content)
      ? String(rpcResult.content.find((entry) => entry?.type === "text")?.text || "")
      : "";
    const parsedTextContent = parseJson(textContent, null);

    if (!response.ok || rpcError) {
      printJson({
        ok: false,
        status: response.status,
        endpoint,
        error: rpcError || "MCP request failed.",
        body: body || rawText,
      });
      process.exitCode = 1;
    } else {
      printJson({
        ok: true,
        status: response.status,
        endpoint,
        quote: structured || parsedTextContent || rpcResult,
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
