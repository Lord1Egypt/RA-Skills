#!/usr/bin/env node
// openmerch-email-verify — verify one email address via OpenMerch.
//
// Zero dependencies. Requires Node 18+ (built-in fetch).
// Usage:   node verify-email.mjs <email>
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

const JOB_TYPE = "email_reputation_v1";
const POLL_MAX_ATTEMPTS = 8;
const POLL_INTERVAL_MS = 1000;
const TERMINAL = new Set(["completed", "failed", "cancelled"]);

function fail(message) {
  console.error(`error: ${message}`);
  process.exit(1);
}

const email = (process.argv[2] || "").trim();
if (!email) fail("usage: node verify-email.mjs <email>");
if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) fail(`not a valid email address: ${email}`);

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
  try {
    json = text ? JSON.parse(text) : {};
  } catch {
    json = { raw_body: text };
  }
  if (!res.ok) {
    fail(`${method} ${path} -> HTTP ${res.status}: ${text || res.statusText}`);
  }
  return json;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Best-effort summary. Includes a key only when the underlying value is present;
// never fabricates fields. The provider response is passed through unchanged, so
// field names are not guaranteed — `raw` remains the source of truth.
function firstDefined(...vals) {
  for (const v of vals) if (v !== undefined && v !== null) return v;
  return undefined;
}

function summarize(output) {
  if (!output || typeof output !== "object") return undefined;
  const d = output.email_deliverability ?? output.deliverability ?? {};
  const q = output.email_quality ?? output.quality ?? {};
  const summary = {};

  const status = firstDefined(d.status, output.status, output.deliverability_status);
  const deliverable = firstDefined(
    typeof status === "string" ? status.toLowerCase() === "deliverable" : undefined,
    output.is_deliverable,
    d.is_deliverable,
  );
  if (deliverable !== undefined) summary.deliverable = deliverable;

  const disposable = firstDefined(d.is_disposable_email, output.is_disposable_email, output.is_disposable);
  if (disposable !== undefined) summary.is_disposable = disposable;

  const free = firstDefined(d.is_free_email, q.is_free_email, output.is_free_email);
  if (free !== undefined) summary.is_free_email = free;

  const score = firstDefined(q.score, output.quality_score, output.score);
  if (score !== undefined) summary.quality_score = score;

  return Object.keys(summary).length ? summary : undefined;
}

async function main() {
  // 1. Plan — confirm executable and get the price.
  const plan = await call("POST", "/v1/plan", { job_type: JOB_TYPE, input: { email } });
  if (plan.can_execute !== true) {
    fail(`job not executable: ${JSON.stringify(plan)}`);
  }
  const maxCost = plan.quoted_customer_price_microcents ?? plan.estimated_cost?.max_microcents;
  if (!(typeof maxCost === "number" && maxCost > 0)) {
    fail(`plan did not return a usable price: ${JSON.stringify(plan)}`);
  }

  // 2. Execute — one job, one idempotency key for this submission.
  const idempotencyKey = randomUUID();
  let job = await call("POST", "/v1/execute", {
    job_type: JOB_TYPE,
    input: { email },
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
    email,
    summary: summarize(job.output),
    raw: job.output ?? null,
    cost_usd: typeof totalMicrocents === "number" ? totalMicrocents / 10000000 : null,
    job_id: job.job_id,
  };
  console.log(JSON.stringify(result, null, 2));
}

main().catch((e) => fail(e?.message || String(e)));
