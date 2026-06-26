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
  toBool,
} from "./shared.mjs";

const TERMINAL_STATES = new Set(["COMPLETED", "REJECTED", "EXPIRED"]);

const args = parseCliArgs();
const baseUrl = normalizeBaseUrl(args["base-url"] || process.env.GHOST_OPENCLAW_BASE_URL || DEFAULT_BASE_URL);
const timeoutMs = parsePositiveInt(args["timeout-ms"] || process.env.GHOST_OPENCLAW_TIMEOUT_MS, DEFAULT_TIMEOUT_MS);
const endpoint = `${baseUrl}/api/mcp/read-only`;
const jobId = String(args["job-id"] || args.job || process.env.GHOSTWIRE_JOB_ID || "").trim();
const waitTerminal = toBool(args["wait-terminal"], false);
const pollEveryMs = parsePositiveInt(args["poll-every-ms"] || process.env.GHOSTWIRE_POLL_EVERY_MS, 5000);
const maxAttempts = parsePositiveInt(args["max-attempts"] || process.env.GHOSTWIRE_MAX_POLL_ATTEMPTS, 60);

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function fetchWireJobStatus(currentJobId) {
  const rpcPayload = {
    jsonrpc: "2.0",
    id: `oc-wire-status-${Date.now()}`,
    method: "tools/call",
    params: {
      name: "get_wire_job_status",
      arguments: {
        job_id: currentJobId,
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
  const status = structured?.status ?? null;
  const job = status?.job ?? null;

  if (!response.ok || rpcError) {
    return {
      ok: false,
      statusCode: response.status,
      error: rpcError || "MCP request failed.",
      body: body || rawText,
      job: null,
    };
  }

  return {
    ok: true,
    statusCode: response.status,
    error: null,
    body: body || rawText,
    job,
  };
}

if (!jobId) {
  printJson({
    ok: false,
    error: "Missing required --job-id (or GHOSTWIRE_JOB_ID).",
    example: "node integrations/openclaw-ghost-pay/bin/get-wire-job-status.mjs --job-id wj_...",
  });
  process.exitCode = 1;
} else {
  let lastResult = null;

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      const result = await fetchWireJobStatus(jobId);
      lastResult = result;

      if (!result.ok) {
        printJson({
          ok: false,
          endpoint,
          jobId,
          attempt,
          status: result.statusCode,
          error: result.error,
          body: result.body,
        });
        process.exitCode = 1;
        break;
      }

      const contractState = String(result.job?.contractState || result.job?.state || "").trim().toUpperCase();
      const terminal = TERMINAL_STATES.has(contractState);

      printJson({
        ok: true,
        endpoint,
        jobId,
        attempt,
        waitTerminal,
        terminal,
        contractState,
        job: result.job,
      });

      if (!waitTerminal || terminal) {
        break;
      }

      if (attempt < maxAttempts) {
        await sleep(pollEveryMs);
      }
    } catch (error) {
      printJson({
        ok: false,
        endpoint,
        jobId,
        error: error instanceof Error ? error.message : "Unknown failure",
      });
      process.exitCode = 1;
      break;
    }
  }

  if (waitTerminal && process.exitCode !== 1) {
    const contractState = String(lastResult?.job?.contractState || lastResult?.job?.state || "")
      .trim()
      .toUpperCase();
    if (!TERMINAL_STATES.has(contractState)) {
      printJson({
        ok: false,
        endpoint,
        jobId,
        error: `Terminal state not reached after ${maxAttempts} attempts.`,
        lastContractState: contractState || null,
      });
      process.exitCode = 1;
    }
  }
}
