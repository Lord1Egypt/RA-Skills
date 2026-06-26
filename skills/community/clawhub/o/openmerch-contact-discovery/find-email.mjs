#!/usr/bin/env node
// openmerch-contact-discovery — find a professional's work email via OpenMerch.
//
// Zero dependencies. Requires Node 18+ (built-in fetch).
// Usage:   node find-email.mjs <first_name> <last_name> <domain>
// Env:     OPENMERCH_API_KEY   (required)  agent API key, om_live_...
//          OPENMERCH_BASE_URL  (optional)  defaults to https://api.openmerch.dev
//
// Flow (the only network calls this script makes):
//   1. POST /v1/plan      confirm executable + get price
//   2. POST /v1/execute   run the job, max_cost = quoted price
//   3. GET  /v1/jobs/{id}  poll ONLY if status is "executing"
//
// Prints a normalized JSON result to stdout. Exits non-zero on error.

import { randomUUID } from "node:crypto";

const JOB_TYPE = "contact_discovery_v1";
const POLL_MAX_ATTEMPTS = 8;
const POLL_INTERVAL_MS = 1000;

function fail(message) {
  console.error(`error: ${message}`);
  process.exit(1);
}

const firstName = (process.argv[2] || "").trim();
const lastName  = (process.argv[3] || "").trim();
const domain    = (process.argv[4] || "").trim();
if (!firstName || !lastName || !domain)
  fail("usage: node find-email.mjs <first_name> <last_name> <domain>");

const apiKey = process.env.OPENMERCH_API_KEY;
if (!apiKey) fail("OPENMERCH_API_KEY is not set. Get a key from the Developer page in the OpenMerch app.");

const baseUrl = (process.env.OPENMERCH_BASE_URL || "https://api.openmerch.dev").replace(/\/+$/, "");

async function call(method, path, body) {
  const headers = { "X-OpenMerch-Key": apiKey };
  if (body !== undefined) headers["Content-Type"] = "application/json";
  const res = await fetch(`${baseUrl}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let json;
  try { json = text ? JSON.parse(text) : {}; }
  catch { json = { raw_body: text }; }
  if (!res.ok) fail(`${method} ${path} -> HTTP ${res.status}: ${text || res.statusText}`);
  return json;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const INPUT = {
  operation: "email-finder",
  params: { first_name: firstName, last_name: lastName, domain },
};

// Hunter (and Apollo fallback) return data double-wrapped: data.data.*
function normalize(output) {
  const d = output?.data?.data ?? {};
  const result = {};
  if (typeof d.email        === "string" && d.email)        result.email        = d.email;
  if (typeof d.first_name   === "string" && d.first_name)   result.first_name   = d.first_name;
  if (typeof d.last_name    === "string" && d.last_name)     result.last_name    = d.last_name;
  if (typeof d.domain       === "string" && d.domain)        result.domain       = d.domain;
  if (typeof d.position     === "string" && d.position)      result.position     = d.position;
  if (typeof d.linkedin_url === "string" && d.linkedin_url)  result.linkedin_url = d.linkedin_url;
  if (typeof d.score === "number")                           result.score        = d.score;
  return result;
}

async function main() {
  // 1. Plan — confirm executable and get the price.
  const plan = await call("POST", "/v1/plan", { job_type: JOB_TYPE, input: INPUT });
  if (plan.can_execute !== true) fail(`job not executable: ${JSON.stringify(plan)}`);
  const maxCost = plan.quoted_customer_price_microcents ?? plan.estimated_cost?.max_microcents;
  if (!(typeof maxCost === "number" && maxCost > 0))
    fail(`plan did not return a usable price: ${JSON.stringify(plan)}`);

  // 2. Execute — one job, one idempotency key for this submission.
  const idempotencyKey = randomUUID();
  let job = await call("POST", "/v1/execute", {
    job_type: JOB_TYPE,
    input: INPUT,
    max_cost: maxCost,
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
    fail(`job did not complete (${err}) [job_id=${job.job_id}]`);
  }

  const totalMicrocents = job.cost?.total_microcents;
  const result = {
    ...normalize(job.output),
    raw: job.output ?? null,
    cost_usd: typeof totalMicrocents === "number" ? totalMicrocents / 10_000_000 : null,
    job_id: job.job_id,
  };
  console.log(JSON.stringify(result, null, 2));
}

main().catch((e) => fail(e?.message || String(e)));
