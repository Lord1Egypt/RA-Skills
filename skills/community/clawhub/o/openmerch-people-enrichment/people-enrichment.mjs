#!/usr/bin/env node
// openmerch-people-enrichment — retrieve a full personal profile via OpenMerch.
//
// Zero dependencies. Requires Node 18+ (built-in fetch).
// Usage:   node people-enrichment.mjs <apollo_person_id>
// Env:     OPENMERCH_API_KEY   (required)  agent API key, om_live_...
//          OPENMERCH_BASE_URL  (optional)  defaults to https://api.openmerch.dev
//
// Flow (the only network calls this script makes):
//   1. POST /v1/plan      confirm executable + get price
//   2. POST /v1/execute   run the job, max_cost = quoted price
//   3. GET  /v1/jobs/{id}  poll ONLY if status is "executing"
//
// Returns sensitive personal data (full name, email, LinkedIn URL).
// Use only for lawful, authorized purposes.
//
// Prints a normalized JSON result to stdout. Exits non-zero on error.

import { randomUUID } from "node:crypto";
import { fileURLToPath } from "node:url";

const JOB_TYPE = "people_enrichment_v1";
const POLL_MAX_ATTEMPTS = 8;
const POLL_INTERVAL_MS = 1000;

// ---------------------------------------------------------------------------
// Argument parsing — throws on invalid input
// ---------------------------------------------------------------------------

export function parseArgs(argv) {
  const id = (argv[0] || "").trim();
  if (!id)
    throw new Error("usage: node people-enrichment.mjs <apollo_person_id>");

  const apiKey = process.env.OPENMERCH_API_KEY;
  if (!apiKey)
    throw new Error("OPENMERCH_API_KEY is not set. Get a key from the Developer page in the OpenMerch app.");

  const baseUrl = (process.env.OPENMERCH_BASE_URL || "https://api.openmerch.dev").replace(/\/+$/, "");

  return { id, apiKey, baseUrl };
}

// ---------------------------------------------------------------------------
// Output normalization — data minimization, no raw provider output
// ---------------------------------------------------------------------------

export function normalize(output) {
  const p = output?.data?.person ?? {};
  const profile = {};
  if (p.id)               profile.id           = p.id;
  if (p.first_name)       profile.first_name   = p.first_name;
  if (p.last_name)        profile.last_name    = p.last_name;
  if (p.email)            profile.email        = p.email;
  if (p.email_status)     profile.email_status = p.email_status;
  if (p.title)            profile.title        = p.title;
  if (p.seniority)        profile.seniority    = p.seniority;
  if (p.linkedin_url)     profile.linkedin_url = p.linkedin_url;
  if (p.organization?.name) profile.organization = p.organization.name;
  return profile;
}

// ---------------------------------------------------------------------------
// Core run logic — exported for testing; never calls process.exit
// ---------------------------------------------------------------------------

export async function run(args, { fetch: fetchFn, sleep }) {
  const { id, apiKey, baseUrl } = args;

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
    operation: "people-enrichment",
    params: { id },
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
    job_type:        JOB_TYPE,
    input:           INPUT,
    max_cost:        maxCost,
    idempotency_key: idempotencyKey,
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
  const profile = normalize(job.output);

  const result = { ...profile };
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
