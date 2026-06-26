#!/usr/bin/env node

import {
  DEFAULT_BASE_URL,
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
const serviceSlug = String(
  args.service || args["service-slug"] || process.env.GHOST_OPENCLAW_SERVICE_SLUG || "",
).trim();
const timeoutMs = parsePositiveInt(args["timeout-ms"] || process.env.GHOST_OPENCLAW_TIMEOUT_MS, DEFAULT_TIMEOUT_MS);
const endpoint = `${baseUrl}/api/mcp/read-only`;

if (!serviceSlug) {
  printJson({
    ok: false,
    error: "Missing required --service (or GHOST_OPENCLAW_SERVICE_SLUG).",
    example:
      "node integrations/openclaw-ghost-pay/bin/get-payment-requirements.mjs --service agent-18755",
  });
  process.exitCode = 1;
} else {
  try {
    const rpcPayload = {
      jsonrpc: "2.0",
      id: `oc-req-${Date.now()}`,
      method: "tools/call",
      params: {
        name: "get_payment_requirements",
        arguments: {
          service_slug: serviceSlug,
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
        serviceSlug,
        error: rpcError || "MCP request failed.",
        body: body || rawText,
      });
      process.exitCode = 1;
    } else {
      printJson({
        ok: true,
        status: response.status,
        endpoint,
        serviceSlug,
        requirements: structured || parsedTextContent || rpcResult,
      });
    }
  } catch (error) {
    printJson({
      ok: false,
      endpoint,
      serviceSlug,
      error: error instanceof Error ? error.message : "Unknown failure",
    });
    process.exitCode = 1;
  }
}
