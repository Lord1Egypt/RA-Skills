#!/usr/bin/env node
// openmerch-company-brief — look up a company profile via OpenMerch.
//
// Zero dependencies. Requires Node 18+ (built-in fetch).
// Usage:   node company-brief.mjs <domain>
// Env:     OPENMERCH_API_KEY   (required)  agent API key, om_live_...
//          OPENMERCH_BASE_URL  (optional)  defaults to https://api.openmerch.dev
//
// Flow (the only network calls this script makes):
//   1. POST /v1/plan      confirm executable + get the price
//   2. POST /v1/execute   run the job, max_cost = quoted price
//   3. GET  /v1/jobs/{id}  poll ONLY if status is "executing"
//
// Prints a normalized JSON result to stdout. Exits non-zero on error.

import { randomUUID } from "node:crypto";
import { fileURLToPath } from "node:url";

const JOB_TYPE = "company_enrichment_v1";
const POLL_MAX_ATTEMPTS = 8;
const POLL_INTERVAL_MS = 1000;

// ---------------------------------------------------------------------------
// Domain normalization — exported for testing
// ---------------------------------------------------------------------------

export function normalizeDomain(input) {
  let raw = (input || "").trim();
  if (!raw) throw new Error("domain is required");

  if (raw.includes("://")) {
    try {
      raw = new URL(raw).hostname;
    } catch {
      raw = raw.replace(/^[^:]+:\/\//, "").split("/")[0];
    }
  } else {
    raw = raw.split("/")[0];
  }

  raw = raw.toLowerCase();

  if (!raw.includes(".")) throw new Error(`invalid domain: "${raw}"`);
  return raw;
}

// ---------------------------------------------------------------------------
// Output normalization — exported for testing
// ---------------------------------------------------------------------------

export function normalize(output, jobId, costMicrocents, requestedDomain) {
  const src = output?.data?.organization ?? output?.data ?? {};

  const domain =
    src.primary_domain ||
    extractHostname(src.website_url) ||
    src.domain ||
    requestedDomain;

  const result = { domain, raw: output, job_id: jobId };

  if (typeof costMicrocents === "number")
    result.cost_usd = costMicrocents / 10_000_000;

  if (src.name) result.name = src.name;

  const description = src.short_description || src.description;
  if (description) result.description = description;

  if (src.industry) result.industry = src.industry;

  const employeeCount = src.estimated_num_employees ?? src.employees_count;
  if (typeof employeeCount === "number") result.employee_count = employeeCount;

  const foundedYear = src.founded_year ?? src.year_founded;
  if (typeof foundedYear === "number") result.founded_year = foundedYear;

  const city = src.city || src.locality;
  const locationParts = [city, src.state, src.country].filter(Boolean);
  if (locationParts.length > 0) result.location = locationParts.join(", ");

  if (src.annual_revenue_printed) result.annual_revenue = src.annual_revenue_printed;
  if (src.linkedin_url) result.linkedin_url = src.linkedin_url;

  if (Array.isArray(src.technology_names)) {
    const techs = src.technology_names.filter((t) => typeof t === "string");
    if (techs.length > 0) result.technologies = techs;
  }

  const funding = {};
  if (typeof src.total_funding === "number") funding.total_usd = src.total_funding;
  if (src.latest_funding_stage) funding.latest_stage = src.latest_funding_stage;
  if (Object.keys(funding).length > 0) result.funding = funding;

  return result;
}

function extractHostname(url) {
  if (!url) return null;
  try {
    return new URL(url.startsWith("http") ? url : `https://${url}`).hostname;
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// Core run logic — exported for testing; never calls process.exit
// ---------------------------------------------------------------------------

export async function run(args, { fetch: fetchFn, sleep }) {
  const { domain, apiKey, baseUrl } = args;

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

  const INPUT = { company_domain: domain };

  // 1. Plan — confirm executable and get the price.
  const plan = await call("POST", "/v1/plan", { job_type: JOB_TYPE, input: INPUT });
  if (plan.can_execute !== true)
    throw new Error(
      `plan returned can_execute: false — ${plan.error?.message ?? plan.error_code ?? "no reason given"}`,
    );

  const maxCost = plan.quoted_customer_price_microcents ?? plan.estimated_cost?.max_microcents;
  if (!(typeof maxCost === "number" && maxCost >= 0))
    throw new Error(`cannot determine max cost from plan response: ${JSON.stringify(plan)}`);

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

  // 4. Terminal state handling.
  if (job.status === "failed")
    throw new Error(`job failed: ${job.error?.code} — ${job.error?.message}`);
  if (job.status === "cancelled")
    throw new Error("job was cancelled");
  if (job.status !== "completed")
    throw new Error(`unexpected terminal status: ${job.status} [job_id=${job.job_id}]`);

  return normalize(job.output, job.job_id, job.cost?.total_microcents, domain);
}

// ---------------------------------------------------------------------------
// CLI entry — only runs when invoked directly
// ---------------------------------------------------------------------------

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  async function main() {
    const rawDomain = process.argv[2];
    if (!rawDomain) {
      console.error("usage: node company-brief.mjs <domain>");
      console.error("  node company-brief.mjs stripe.com");
      console.error("  node company-brief.mjs https://stripe.com/about");
      process.exitCode = 1;
      return;
    }

    let domain;
    try {
      domain = normalizeDomain(rawDomain);
    } catch (err) {
      console.error(`error: ${err.message}`);
      process.exitCode = 1;
      return;
    }

    const apiKey = process.env.OPENMERCH_API_KEY;
    if (!apiKey) {
      console.error(
        "error: OPENMERCH_API_KEY is not set. Get a key from the Developer page in the OpenMerch app.",
      );
      process.exitCode = 1;
      return;
    }

    const baseUrl = (process.env.OPENMERCH_BASE_URL || "https://api.openmerch.dev").replace(
      /\/+$/,
      "",
    );
    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

    try {
      const result = await run({ domain, apiKey, baseUrl }, { fetch: globalThis.fetch, sleep });
      console.log(JSON.stringify(result, null, 2));
    } catch (err) {
      console.error(`error: ${err?.message || String(err)}`);
      process.exitCode = 1;
    }
  }

  main();
}
