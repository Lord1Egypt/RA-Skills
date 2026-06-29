#!/usr/bin/env node
// openmerch-people-search — search for people at a company via OpenMerch.
//
// Zero dependencies. Requires Node 18+ (built-in fetch).
// Usage:   node people-search.mjs <domain> "<keywords>" [per_page] [page]
// Env:     OPENMERCH_API_KEY   (required)  agent API key, om_live_...
//          OPENMERCH_BASE_URL  (optional)  defaults to https://api.openmerch.dev
//
// Flow (the only network calls this script makes):
//   1. POST /v1/plan      confirm executable + get price
//   2. POST /v1/execute   run the job, max_cost = quoted price
//   3. GET  /v1/jobs/{id}  poll ONLY if status is "executing"
//
// Prints a normalized JSON result to stdout. Exits non-zero on error.
//
// Note: last names are obfuscated (e.g. "D."). For full profiles use openmerch-people-enrichment.

import { randomUUID } from "node:crypto";
import { fileURLToPath } from "node:url";

const JOB_TYPE = "people_enrichment_v1";
const POLL_MAX_ATTEMPTS = 8;
const POLL_INTERVAL_MS = 1000;

// ---------------------------------------------------------------------------
// Argument parsing — throws on invalid input
// ---------------------------------------------------------------------------

function parseIntArg(raw, name) {
  const parsed = Number(raw);
  if (!Number.isInteger(parsed) || parsed <= 0)
    throw new Error(`${name} must be a positive integer, got: ${JSON.stringify(raw)}`);
  return parsed;
}

export function parseArgs(argv) {
  const domain   = (argv[0] || "").trim();
  const keywords = (argv[1] || "").trim();
  if (!domain || !keywords)
    throw new Error("usage: node people-search.mjs <domain> \"<keywords>\" [per_page] [page]");

  const perPage = argv[2] !== undefined ? parseIntArg(argv[2], "per_page") : 25;
  const page    = argv[3] !== undefined ? parseIntArg(argv[3], "page")     : 1;

  const apiKey  = process.env.OPENMERCH_API_KEY;
  if (!apiKey)
    throw new Error("OPENMERCH_API_KEY is not set. Get a key from the Developer page in the OpenMerch app.");

  const baseUrl = (process.env.OPENMERCH_BASE_URL || "https://api.openmerch.dev").replace(/\/+$/, "");

  return { domain, keywords, perPage, page, apiKey, baseUrl };
}

// ---------------------------------------------------------------------------
// Output normalization
// ---------------------------------------------------------------------------

export function normalize(output) {
  const people = output?.data?.people ?? [];
  const normalized = people.map((p) => {
    const record = {};
    if (p.id)                    record.id                   = p.id;
    if (p.first_name)            record.first_name           = p.first_name;
    if (p.last_name_obfuscated)  record.last_name_obfuscated = p.last_name_obfuscated;
    if (p.title)                 record.title                = p.title;
    if (p.organization?.name)    record.organization         = p.organization.name;
    return record;
  });

  const result = {
    count: normalized.length,
    people: normalized,
  };

  if (typeof output?.data?.total_entries === "number")
    result.total_entries = output.data.total_entries;

  return result;
}

// ---------------------------------------------------------------------------
// Core run logic — exported for testing; never calls process.exit
// ---------------------------------------------------------------------------

export async function run(args, { fetch: fetchFn, sleep }) {
  const { domain, keywords, perPage, page, apiKey, baseUrl } = args;

  async function call(method, path, body) {
    const headers = { "X-OpenMerch-Key": apiKey };
    if (body !== undefined) headers["Content-Type"] = "application/json";
    const res = await fetchFn(`${baseUrl}${path}`, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
    const text = await res.text();
    let json;
    try { json = text ? JSON.parse(text) : {}; }
    catch { json = { raw_body: text }; }
    if (!res.ok)
      throw new Error(`${method} ${path} -> HTTP ${res.status}: ${text || res.statusText}`);
    return json;
  }

  const INPUT = {
    operation: "people-search",
    params: {
      q_organization_domains: domain,
      q_keywords:             keywords,
      per_page:               perPage,
      page,
    },
  };

  // 1. Plan — confirm executable and get the price.
  const plan = await call("POST", "/v1/plan", { job_type: JOB_TYPE, input: INPUT });
  if (plan.can_execute !== true)
    throw new Error(`job not executable: ${JSON.stringify(plan)}`);
  const maxCost = plan.quoted_customer_price_microcents ?? plan.estimated_cost?.max_microcents;
  if (!(typeof maxCost === "number" && maxCost > 0))
    throw new Error(`plan did not return a usable price: ${JSON.stringify(plan)}`);

  // 2. Execute — one job, one idempotency key for this submission.
  const idempotencyKey = randomUUID();
  let job = await call("POST", "/v1/execute", {
    job_type:         JOB_TYPE,
    input:            INPUT,
    max_cost:         maxCost,
    idempotency_key:  idempotencyKey,
  });

  // 3. Poll only if still executing.
  let attempts = 0;
  while (job.status === "executing" && attempts < POLL_MAX_ATTEMPTS) {
    await sleep(POLL_INTERVAL_MS);
    job = await call("GET", `/v1/jobs/${job.job_id}`);
    attempts++;
  }

  if (job.status !== "completed") {
    const err = job.error ? `${job.error.code}: ${job.error.message}` : `status=${job.status}`;
    throw new Error(`job did not complete (${err}) [job_id=${job.job_id}]`);
  }

  const totalMicrocents = job.cost?.total_microcents;
  const { count, people, total_entries } = normalize(job.output);

  const result = { count };
  if (typeof total_entries === "number") result.total_entries = total_entries;
  result.people   = people;
  result.cost_usd = typeof totalMicrocents === "number" ? totalMicrocents / 10_000_000 : null;
  result.job_id   = job.job_id;

  return result;
}

// ---------------------------------------------------------------------------
// CLI entry — only runs when invoked directly
// ---------------------------------------------------------------------------

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  async function main() {
    const args  = parseArgs(process.argv.slice(2));
    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
    const result = await run(args, { fetch: globalThis.fetch, sleep });
    console.log(JSON.stringify(result, null, 2));
  }

  main().catch((error) => {
    console.error(`error: ${error?.message || String(error)}`);
    process.exitCode = 1;
  });
}
