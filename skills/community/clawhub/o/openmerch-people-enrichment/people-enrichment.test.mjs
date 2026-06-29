// people-enrichment.test.mjs — unit tests for people-enrichment.mjs
//
// Node 18+ native test runner. Zero external deps. No real network calls.
// Run: node --test people-enrichment.test.mjs

import { test } from "node:test";
import assert from "node:assert/strict";
import { parseArgs, normalize, run } from "./people-enrichment.mjs";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const noSleep = () => Promise.resolve();

function mockFetch(responses) {
  let callIndex = 0;
  return async (url, opts) => {
    const resp = responses[callIndex++];
    if (!resp) throw new Error(`unexpected fetch call #${callIndex} to ${url}`);
    const body = typeof resp.body === "string" ? resp.body : JSON.stringify(resp.body);
    return {
      ok:         resp.status >= 200 && resp.status < 300,
      status:     resp.status ?? 200,
      statusText: resp.statusText ?? "OK",
      text:       async () => body,
    };
  };
}

function makeArgs(overrides = {}) {
  return {
    id:      "abc123",
    apiKey:  "om_live_test",
    baseUrl: "https://api.openmerch.dev",
    ...overrides,
  };
}

function planOk(maxCost = 80000) {
  return { status: 200, body: { can_execute: true, quoted_customer_price_microcents: maxCost } };
}

function jobCompleted(person = {}) {
  return {
    status: 200,
    body: {
      status:  "completed",
      job_id:  "job-456",
      output:  { data: { person } },
      cost:    { total_microcents: 80000 },
    },
  };
}

// ---------------------------------------------------------------------------
// normalize() — pure function tests (no fetch)
// ---------------------------------------------------------------------------

test("normalize: extracts full profile fields from data.person", () => {
  const output = {
    data: {
      person: {
        id:           "p1",
        first_name:   "Jane",
        last_name:    "Doe",
        email:        "jane@example.com",
        email_status: "verified",
        title:        "Senior Engineer",
        seniority:    "senior",
        linkedin_url: "https://www.linkedin.com/in/janedoe",
        organization: { name: "Stripe" },
      },
    },
  };
  const profile = normalize(output);
  assert.equal(profile.first_name,   "Jane");
  assert.equal(profile.last_name,    "Doe");
  assert.equal(profile.email,        "jane@example.com");
  assert.equal(profile.email_status, "verified");
  assert.equal(profile.linkedin_url, "https://www.linkedin.com/in/janedoe");
  assert.equal(profile.organization, "Stripe");
  assert.equal("raw" in profile, false, "profile must not contain raw field");
});

test("normalize: optional fields omitted when absent", () => {
  const output = { data: { person: { id: "p2", first_name: "Marcus" } } };
  const profile = normalize(output);
  assert.equal(profile.id,         "p2");
  assert.equal(profile.first_name, "Marcus");
  assert.equal("email"        in profile, false);
  assert.equal("linkedin_url" in profile, false);
  assert.equal("last_name"    in profile, false);
});

test("normalize: empty data.person returns empty profile", () => {
  const profile = normalize({ data: { person: {} } });
  assert.deepEqual(profile, {});
});

test("normalize: missing data.person returns empty profile", () => {
  const profile = normalize({ data: {} });
  assert.deepEqual(profile, {});
  const profile2 = normalize(null);
  assert.deepEqual(profile2, {});
});

// ---------------------------------------------------------------------------
// parseArgs() — validation
// ---------------------------------------------------------------------------

test("parseArgs: rejects empty id", () => {
  process.env.OPENMERCH_API_KEY = "om_live_test";
  assert.throws(() => parseArgs([""]),  /usage/);
  assert.throws(() => parseArgs([]),    /usage/);
});

test("parseArgs: rejects missing OPENMERCH_API_KEY", () => {
  delete process.env.OPENMERCH_API_KEY;
  assert.throws(() => parseArgs(["abc123"]), /OPENMERCH_API_KEY/);
  process.env.OPENMERCH_API_KEY = "om_live_test";
});

// ---------------------------------------------------------------------------
// run() — API flow tests
// ---------------------------------------------------------------------------

test("run: can_execute:false → rejects without execute call", async () => {
  const fetch = mockFetch([
    { status: 200, body: { can_execute: false, reason: "no_provider" } },
  ]);
  await assert.rejects(
    () => run(makeArgs(), { fetch, sleep: noSleep }),
    /job not executable/,
  );
});

test("run: immediate completion — no polling", async () => {
  let fetchCallCount = 0;
  const fetch = async (url, opts) => {
    fetchCallCount++;
    const body = fetchCallCount === 1
      ? { can_execute: true, quoted_customer_price_microcents: 80000 }
      : { status: "completed", job_id: "j1", output: { data: { person: { id: "p1", first_name: "Jane" } } }, cost: { total_microcents: 80000 } };
    return { ok: true, status: 200, statusText: "OK", text: async () => JSON.stringify(body) };
  };
  const result = await run(makeArgs(), { fetch, sleep: noSleep });
  assert.equal(fetchCallCount, 2, "must make exactly 2 calls (plan + execute), no GET poll");
  assert.equal(result.job_id, "j1");
  assert.equal("raw" in result, false, "result must not contain raw field");
});

test("run: polls once when status is executing", async () => {
  let sleepCalls = 0;
  const sleep = () => { sleepCalls++; return Promise.resolve(); };
  const responses = [
    planOk(),
    { status: 200, body: { status: "executing", job_id: "j2" } },
    jobCompleted({ id: "p1", first_name: "Jane", last_name: "Doe", email: "jane@example.com" }),
  ];
  const result = await run(makeArgs(), { fetch: mockFetch(responses), sleep });
  assert.equal(sleepCalls, 1, "sleep must be called once");
  assert.equal(result.first_name, "Jane");
  assert.equal(result.last_name,  "Doe");
  assert.equal(result.email,      "jane@example.com");
});

test("run: failed job → rejects with error code and message", async () => {
  const responses = [
    planOk(),
    {
      status: 200,
      body: {
        status: "failed",
        job_id: "j3",
        error:  { code: "provider_error", message: "upstream timeout" },
      },
    },
  ];
  await assert.rejects(
    () => run(makeArgs(), { fetch: mockFetch(responses), sleep: noSleep }),
    /provider_error.*upstream timeout/,
  );
});

test("run: cancelled job → rejects", async () => {
  const responses = [
    planOk(),
    { status: 200, body: { status: "cancelled", job_id: "j4" } },
  ];
  await assert.rejects(
    () => run(makeArgs(), { fetch: mockFetch(responses), sleep: noSleep }),
    /cancelled/,
  );
});
