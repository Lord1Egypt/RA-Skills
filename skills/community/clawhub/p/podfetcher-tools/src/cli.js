#!/usr/bin/env node

import { parseArgs } from "node:util";
import { randomUUID } from "node:crypto";
import {
  createPodfetcherClient,
  isTranscriptProcessingResponse,
  isTranscriptReadyResponse,
  PodfetcherApiError,
} from "./sdk.js";

const HELP_TEXT = `
Podfetcher CLI

Usage:
  podfetcher <group> <command> [options]

Groups and commands:
  shows search        Search shows
  shows episodes      List episodes for a show
  transcripts fetch   Fetch transcript for an episode

Global options:
  --base-url <url>       API base URL (env: PODFETCHER_BASE_URL, default: https://api.podfetcher.com)
  --api-key <key>        API key (env: PODFETCHER_API_KEY)
  --api-key-header <h>   API key header (env: PODFETCHER_API_KEY_HEADER, default: X-API-Key)
  --timeout-ms <ms>      HTTP timeout per request (default: 15000)
  --json                 Print JSON output
  -h, --help             Show help

Examples:
  podfetcher shows search --q "ai" --limit 5
  podfetcher shows episodes --show-id pi_1001 --order-by publishedAt --order desc --limit 10
  podfetcher transcripts fetch --episode-id ep_pi_1001_002 --wait --poll-interval-ms 1000
`.trim();

async function main() {
  const raw = process.argv.slice(2);
  if (raw.length === 0 || raw.includes("--help") || raw.includes("-h")) {
    console.log(HELP_TEXT);
    return;
  }

  const [group, command, ...rest] = raw;
  if (!group || !command) {
    throw new Error("Expected command in format: podfetcher <group> <command> [options]");
  }

  if (group === "shows" && command === "search") {
    await runShowsSearch(rest);
    return;
  }

  if (group === "shows" && command === "episodes") {
    await runShowsEpisodes(rest);
    return;
  }

  if (group === "transcripts" && command === "fetch") {
    await runTranscriptFetch(rest);
    return;
  }

  throw new Error(`Unknown command: ${group} ${command}`);
}

async function runShowsSearch(args) {
  const parsed = parseArgs({
    args,
    options: {
      q: { type: "string" },
      limit: { type: "string" },
      cursor: { type: "string" },
      "base-url": { type: "string" },
      "api-key": { type: "string" },
      "api-key-header": { type: "string" },
      "timeout-ms": { type: "string" },
      json: { type: "boolean", default: false },
    },
    allowPositionals: false,
  });

  if (!parsed.values.q || parsed.values.q.trim().length === 0) {
    throw new Error("--q is required");
  }

  const client = clientFromValues(parsed.values);
  const response = await client.searchShows({
    q: parsed.values.q,
    limit: parseOptionalInt(parsed.values.limit, "limit"),
    cursor: parsed.values.cursor,
  });

  if (parsed.values.json) {
    console.log(JSON.stringify(response, null, 2));
    return;
  }

  console.log(`Found ${response.items.length} show(s)`);
  for (const item of response.items) {
    console.log(`- ${item.showId} | ${item.title}${item.author ? ` (${item.author})` : ""}`);
  }
  if (response.nextCursor) {
    console.log(`nextCursor: ${response.nextCursor}`);
  }
}

async function runShowsEpisodes(args) {
  const parsed = parseArgs({
    args,
    options: {
      "show-id": { type: "string" },
      since: { type: "string" },
      from: { type: "string" },
      to: { type: "string" },
      "order-by": { type: "string" },
      orderBy: { type: "string" },
      order: { type: "string" },
      limit: { type: "string" },
      cursor: { type: "string" },
      "base-url": { type: "string" },
      "api-key": { type: "string" },
      "api-key-header": { type: "string" },
      "timeout-ms": { type: "string" },
      json: { type: "boolean", default: false },
    },
    allowPositionals: false,
  });

  if (!parsed.values["show-id"]) {
    throw new Error("--show-id is required");
  }

  const client = clientFromValues(parsed.values);
  const response = await client.listEpisodes({
    showId: parsed.values["show-id"],
    since: parsed.values.since,
    from: parsed.values.from,
    to: parsed.values.to,
    orderBy: parsed.values["order-by"] || parsed.values.orderBy,
    order: parsed.values.order,
    limit: parseOptionalInt(parsed.values.limit, "limit"),
    cursor: parsed.values.cursor,
  });

  if (parsed.values.json) {
    console.log(JSON.stringify(response, null, 2));
    return;
  }

  console.log(`Found ${response.items.length} episode(s)`);
  for (const item of response.items) {
    console.log(
      `- ${item.episodeId} | ${item.publishedAt} | ${item.title} | transcript=${item.transcriptStatus}`,
    );
  }
  if (response.nextCursor) {
    console.log(`nextCursor: ${response.nextCursor}`);
  }
}

async function runTranscriptFetch(args) {
  const parsed = parseArgs({
    args,
    options: {
      "episode-id": { type: "string" },
      wait: { type: "boolean", default: false },
      "poll-interval-ms": { type: "string" },
      "wait-timeout-ms": { type: "string" },
      "idempotency-key": { type: "string" },
      "base-url": { type: "string" },
      "api-key": { type: "string" },
      "api-key-header": { type: "string" },
      "timeout-ms": { type: "string" },
      json: { type: "boolean", default: false },
    },
    allowPositionals: false,
  });

  const episodeId = parsed.values["episode-id"];
  if (!episodeId) {
    throw new Error("--episode-id is required");
  }

  const client = clientFromValues(parsed.values);
  const idempotencyKey = parsed.values["idempotency-key"] || randomUUID();

  let response;
  if (parsed.values.wait) {
    response = await client.fetchTranscriptAndWait({
      episodeId,
      idempotencyKey,
      pollIntervalMs: parseOptionalInt(parsed.values["poll-interval-ms"], "poll-interval-ms", 1_000),
      waitTimeoutMs: parseOptionalInt(parsed.values["wait-timeout-ms"], "wait-timeout-ms", 60_000),
    });
  } else {
    response = await client.fetchTranscript({ episodeId, idempotencyKey });
  }

  if (parsed.values.json) {
    console.log(JSON.stringify(response, null, 2));
    return;
  }

  if (isTranscriptReadyResponse(response)) {
    console.log(`Episode: ${response.episodeId}`);
    console.log(`Source: ${response.transcript.source}`);
    console.log(`Tokens charged: ${response.billing?.tokensCharged ?? "n/a"}`);
    console.log("Transcript:");
    console.log(response.transcript.content);
    return;
  }

  if (isTranscriptProcessingResponse(response)) {
    console.log(`Job queued: ${response.jobId} (${response.status})`);
    if (typeof response.estimatedTokens === "number") {
      console.log(`Estimated tokens: ${response.estimatedTokens}`);
    }
    return;
  }

  console.log(JSON.stringify(response, null, 2));
}

function clientFromValues(values) {
  return createPodfetcherClient({
    baseUrl: values["base-url"],
    apiKey: values["api-key"],
    apiKeyHeader: values["api-key-header"],
    timeoutMs: parseOptionalInt(values["timeout-ms"], "timeout-ms"),
  });
}

function parseOptionalInt(raw, name, fallback) {
  if (raw === undefined || raw === null) {
    return fallback;
  }
  const value = Number(raw);
  if (!Number.isInteger(value) || value <= 0) {
    throw new Error(`--${name} must be a positive integer`);
  }
  return value;
}

function printError(error) {
  if (error instanceof PodfetcherApiError) {
    console.error(`[HTTP ${error.status}] ${error.code || "API_ERROR"}: ${error.message}`);
    if (error.details) {
      for (const [key, value] of Object.entries(error.details)) {
        console.error(`  - ${key}: ${value}`);
      }
    }
    return;
  }
  console.error(error.message || String(error));
}

main().catch((error) => {
  printError(error);
  process.exitCode = 1;
});
