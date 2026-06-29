// people-search.test.mjs — unit tests for people-search.mjs
//
// Node 18+ native test runner. Zero external deps. No real network calls.
// Run: node --test people-search.test.mjs

import { test } from "node:test";
import assert from "node:assert/strict";
import { parseArgs, normalize, run } from "./people-search.mjs";

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
      ok:     resp.status >= 200 && resp.status < 300,
      status: resp.status ?? 200,
      statusText: resp.statusText ?? "OK",
      text:   async () => body,
    };
  };
}

function makeArgs(overrides = {}) {
  return {
    domain:   "stripe.com",
    keywords: "backend engineer",
    perPage:  25,
    page:     1,
    apiKey:   "om_live_test",
    baseUrl:  "https://api.openmerch.dev",
    ...overrides,
  };
}

function planOk(maxCost = 59000) {
  return { status: 200, body: { can_execute: true, quoted_customer_price_microcents: maxCost } };
}

function jobCompleted(people = [], totalEntries) {
  const data = { people };
  if (typeof totalEntries === "number") data.total_entries = totalEntries;
  return {
    status: 200,
    body: {
      status:  "completed",
      job_id:  "job-123",
      output:  { data },
      cost:    { total_microcents: 59000 },
    },
  };
}

// ---------------------------------------------------------------------------
// normalize() — pure function tests (no fetch)
// ---------------------------------------------------------------------------

test("normalize: obfuscated last name and nested org name", () => {
  const output = {
    data: {
      people: [
        { id: "p1", first_name: "Jane", last_name_obfuscated: "D.", title: "Engineer", organization: { name: "Stripe" } },
      ],
    },
  };
  const { people } = normalize(output);
  assert.equal(people.length, 1);
  assert.equal(people[0].last_name_obfuscated, "D.");
  assert.equal(people[0].organization, "Stripe");
  assert.equal("linkedin_url" in people[0], false, "linkedin_url must not be present");
});

test("normalize: nested org name extracted correctly", () => {
  const output = { data: { people: [{ id: "p2", organization: { name: "Acme Corp" } }] } };
  const { people } = normalize(output);
  assert.equal(people[0].organization, "Acme Corp");
});

test("normalize: empty result set", () => {
  const { count, people, total_entries } = normalize({ data: { people: [] } });
  assert.equal(count, 0);
  assert.deepEqual(people, []);
  assert.equal(total_entries, undefined, "total_entries must be absent when not in output");
});

test("normalize: total_entries = 0 is preserved (typeof check, not truthiness)", () => {
  const output = { data: { people: [], total_entries: 0 } };
  const result = normalize(output);
  assert.equal(typeof result.total_entries, "number");
  assert.equal(result.total_entries, 0);
});

test("normalize: total_entries absent when field missing", () => {
  const output = { data: { people: [] } };
  const result = normalize(output);
  assert.equal("total_entries" in result, false);
});

// ---------------------------------------------------------------------------
// parseArgs() — numeric validation
// ---------------------------------------------------------------------------

test("parseArgs: rejects non-numeric per_page", () => {
  process.env.OPENMERCH_API_KEY = "om_live_test";
  assert.throws(() => parseArgs(["stripe.com", "eng", "abc"]), /positive integer/);
});

test("parseArgs: rejects float per_page", () => {
  assert.throws(() => parseArgs(["stripe.com", "eng", "1.5"]), /positive integer/);
});

test("parseArgs: rejects trailing-garbage per_page", () => {
  assert.throws(() => parseArgs(["stripe.com", "eng", "25abc"]), /positive integer/);
});

test("parseArgs: rejects empty string per_page", () => {
  assert.throws(() => parseArgs(["stripe.com", "eng", ""]), /positive integer/);
});

test("parseArgs: rejects zero page", () => {
  assert.throws(() => parseArgs(["stripe.com", "eng", "25", "0"]), /positive integer/);
});

test("parseArgs: rejects negative per_page", () => {
  assert.throws(() => parseArgs(["stripe.com", "eng", "-1"]), /positive integer/);
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
      ? { can_execute: true, quoted_customer_price_microcents: 59000 }
      : { status: "completed", job_id: "j1", output: { data: { people: [] } }, cost: { total_microcents: 59000 } };
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
    jobCompleted([{ id: "p1", first_name: "Jane", last_name_obfuscated: "D." }], 10),
  ];
  const result = await run(makeArgs(), { fetch: mockFetch(responses), sleep });
  assert.equal(sleepCalls, 1, "sleep must be called once");
  assert.equal(result.count, 1);
  assert.equal(result.total_entries, 10);
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
