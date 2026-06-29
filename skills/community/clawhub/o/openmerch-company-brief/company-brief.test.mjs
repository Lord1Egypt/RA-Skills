// company-brief.test.mjs — unit tests for company-brief.mjs
//
// Node 18+ native test runner. Zero external deps. No real network calls.
// Run: node --test company-brief.test.mjs

import { test } from "node:test";
import assert from "node:assert/strict";
import { normalizeDomain, normalize, run } from "./company-brief.mjs";

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
    domain:  "stripe.com",
    apiKey:  "om_live_test",
    baseUrl: "https://api.openmerch.dev",
    ...overrides,
  };
}

function planOk(price = 60000) {
  return { status: 200, body: { can_execute: true, quoted_customer_price_microcents: price } };
}

function jobCompleted(outputData = {}, costMicrocents = 60000) {
  return {
    status: 200,
    body: {
      status: "completed",
      job_id: "job-123",
      output: { data: outputData },
      cost:   { total_microcents: costMicrocents },
    },
  };
}

const fullOrg = {
  organization: {
    name:                   "Stripe",
    primary_domain:         "stripe.com",
    short_description:      "Financial infrastructure for the internet.",
    industry:               "financial services",
    estimated_num_employees: 7000,
    founded_year:           2010,
    city:                   "San Francisco",
    state:                  "California",
    country:                "United States",
    annual_revenue_printed: "$1B+",
    linkedin_url:           "https://www.linkedin.com/company/stripe",
    technology_names:       ["React", "Ruby on Rails", "AWS"],
    total_funding:          8700000000,
    latest_funding_stage:   "Series I",
    website_url:            "https://stripe.com",
  },
};

// ---------------------------------------------------------------------------
// normalizeDomain()
// ---------------------------------------------------------------------------

test("normalizeDomain: bare domain", () => {
  assert.equal(normalizeDomain("stripe.com"), "stripe.com");
});

test("normalizeDomain: URL with protocol and path", () => {
  assert.equal(normalizeDomain("https://stripe.com/about"), "stripe.com");
});

test("normalizeDomain: http URL", () => {
  assert.equal(normalizeDomain("http://stripe.com"), "stripe.com");
});

test("normalizeDomain: uppercase domain lowercased", () => {
  assert.equal(normalizeDomain("STRIPE.COM"), "stripe.com");
});

test("normalizeDomain: bare domain with trailing slash stripped", () => {
  assert.equal(normalizeDomain("stripe.com/"), "stripe.com");
});

test("normalizeDomain: bare domain with path stripped", () => {
  assert.equal(normalizeDomain("stripe.com/products/billing"), "stripe.com");
});

test("normalizeDomain: trims leading and trailing whitespace", () => {
  assert.equal(normalizeDomain("  stripe.com  "), "stripe.com");
});

test("normalizeDomain: empty string throws", () => {
  assert.throws(() => normalizeDomain(""), /domain is required/);
});

test("normalizeDomain: whitespace-only string throws", () => {
  assert.throws(() => normalizeDomain("   "), /domain is required/);
});

test("normalizeDomain: no dot throws", () => {
  assert.throws(() => normalizeDomain("notadomain"), /invalid domain/);
});

// ---------------------------------------------------------------------------
// normalize() — pure function tests
// ---------------------------------------------------------------------------

test("normalize: output.data.organization.* — all fields populated", () => {
  const result = normalize({ data: fullOrg }, "job-1", 60000, "stripe.com");
  assert.equal(result.domain, "stripe.com");
  assert.equal(result.name, "Stripe");
  assert.equal(result.description, "Financial infrastructure for the internet.");
  assert.equal(result.industry, "financial services");
  assert.equal(result.employee_count, 7000);
  assert.equal(result.founded_year, 2010);
  assert.equal(result.location, "San Francisco, California, United States");
  assert.equal(result.annual_revenue, "$1B+");
  assert.equal(result.linkedin_url, "https://www.linkedin.com/company/stripe");
  assert.deepEqual(result.technologies, ["React", "Ruby on Rails", "AWS"]);
  assert.deepEqual(result.funding, { total_usd: 8700000000, latest_stage: "Series I" });
  assert.equal(result.cost_usd, 0.006);
  assert.equal(result.job_id, "job-1");
  assert.deepEqual(result.raw, { data: fullOrg });
});

test("normalize: output.data.* fallback — no organization key", () => {
  const flat = {
    data: {
      name:            "Acme Corp",
      domain:          "acme.com",
      description:     "A software company.",
      employees_count: 500,
      year_founded:    2005,
    },
  };
  const result = normalize(flat, "job-2", 60000, "acme.com");
  assert.equal(result.name, "Acme Corp");
  assert.equal(result.description, "A software company.");
  assert.equal(result.employee_count, 500);
  assert.equal(result.founded_year, 2005);
  assert.equal("location" in result, false);
});

test("normalize: short_description wins over description", () => {
  const result = normalize(
    { data: { organization: { short_description: "Short.", description: "Long version." } } },
    "j", 0, "x.com",
  );
  assert.equal(result.description, "Short.");
});

test("normalize: description falls back when short_description absent", () => {
  const result = normalize(
    { data: { organization: { description: "A company." } } },
    "j", 0, "x.com",
  );
  assert.equal(result.description, "A company.");
});

test("normalize: employee_count falls back from estimated_num_employees to employees_count", () => {
  const result = normalize(
    { data: { organization: { employees_count: 200 } } },
    "j", 0, "x.com",
  );
  assert.equal(result.employee_count, 200);
});

test("normalize: founded_year falls back from founded_year to year_founded", () => {
  const result = normalize(
    { data: { organization: { year_founded: 1999 } } },
    "j", 0, "x.com",
  );
  assert.equal(result.founded_year, 1999);
});

test("normalize: domain from primary_domain", () => {
  const result = normalize(
    { data: { organization: { primary_domain: "stripe.com" } } },
    "j", 0, "stripe.com",
  );
  assert.equal(result.domain, "stripe.com");
});

test("normalize: domain falls back to website_url hostname", () => {
  const result = normalize(
    { data: { organization: { website_url: "https://acme.com/home" } } },
    "j", 0, "acme.com",
  );
  assert.equal(result.domain, "acme.com");
});

test("normalize: domain falls back to src.domain when primary_domain and website_url absent", () => {
  const result = normalize(
    { data: { organization: { domain: "fallback.com" } } },
    "j", 0, "fallback.com",
  );
  assert.equal(result.domain, "fallback.com");
});

test("normalize: domain falls back to requestedDomain when src has no domain fields", () => {
  const result = normalize(
    { data: { organization: { name: "NoName" } } },
    "j", 0, "requested.com",
  );
  assert.equal(result.domain, "requested.com");
});

test("normalize: location assembled from city, state, and country", () => {
  const result = normalize(
    { data: { organization: { city: "San Francisco", state: "California", country: "United States" } } },
    "j", 0, "x.com",
  );
  assert.equal(result.location, "San Francisco, California, United States");
});

test("normalize: location assembled from city and country when state absent", () => {
  const result = normalize(
    { data: { organization: { city: "London", country: "United Kingdom" } } },
    "j", 0, "x.com",
  );
  assert.equal(result.location, "London, United Kingdom");
});

test("normalize: locality used as city fallback in location", () => {
  const result = normalize(
    { data: { organization: { locality: "Berlin", country: "Germany" } } },
    "j", 0, "x.com",
  );
  assert.equal(result.location, "Berlin, Germany");
});

test("normalize: location omitted when all location fields absent", () => {
  const result = normalize(
    { data: { organization: { name: "NoLocation" } } },
    "j", 0, "x.com",
  );
  assert.equal("location" in result, false);
});

test("normalize: technology_names empty array — technologies omitted", () => {
  const result = normalize(
    { data: { organization: { technology_names: [] } } },
    "j", 0, "x.com",
  );
  assert.equal("technologies" in result, false);
});

test("normalize: technology_names with non-string entries — filtered out", () => {
  const result = normalize(
    { data: { organization: { technology_names: ["React", null, 42, "AWS", undefined] } } },
    "j", 0, "x.com",
  );
  assert.deepEqual(result.technologies, ["React", "AWS"]);
});

test("normalize: funding omitted when no funding fields present", () => {
  const result = normalize(
    { data: { organization: { name: "Lean Co" } } },
    "j", 0, "x.com",
  );
  assert.equal("funding" in result, false);
});

test("normalize: funding with only latest_stage — total_usd absent", () => {
  const result = normalize(
    { data: { organization: { latest_funding_stage: "Seed" } } },
    "j", 0, "x.com",
  );
  assert.deepEqual(result.funding, { latest_stage: "Seed" });
  assert.equal("total_usd" in result.funding, false);
});

test("normalize: costMicrocents not a number — cost_usd omitted", () => {
  const result = normalize({ data: {} }, "j", undefined, "x.com");
  assert.equal("cost_usd" in result, false);
});

test("normalize: raw always equals the full output argument unchanged", () => {
  const output = { data: { organization: { name: "Stripe" } }, extra: "preserved" };
  const result = normalize(output, "j", 0, "stripe.com");
  assert.strictEqual(result.raw, output, "raw must be the exact same object reference");
});

test("normalize: null output — only domain, raw, job_id present", () => {
  const result = normalize(null, "j", undefined, "x.com");
  assert.deepEqual(Object.keys(result).sort(), ["domain", "job_id", "raw"]);
  assert.equal(result.domain, "x.com");
  assert.equal(result.raw, null);
  assert.equal(result.job_id, "j");
});

// ---------------------------------------------------------------------------
// run() — API flow tests
// ---------------------------------------------------------------------------

test("run: can_execute:false → rejects without execute call", async () => {
  const fetch = mockFetch([
    { status: 200, body: { can_execute: false, error_code: "no_provider" } },
  ]);
  await assert.rejects(
    () => run(makeArgs(), { fetch, sleep: noSleep }),
    /can_execute: false/,
  );
});

test("run: quoted_customer_price_microcents used as max_cost", async () => {
  const capturedBodies = [];
  const fetch = async (url, opts) => {
    if (opts?.body) capturedBodies.push(JSON.parse(opts.body));
    const idx = capturedBodies.length;
    const body =
      idx === 1
        ? { can_execute: true, quoted_customer_price_microcents: 60000 }
        : { status: "completed", job_id: "j1", output: { data: {} }, cost: { total_microcents: 60000 } };
    return { ok: true, status: 200, statusText: "OK", text: async () => JSON.stringify(body) };
  };
  await run(makeArgs(), { fetch, sleep: noSleep });
  assert.equal(capturedBodies[1].max_cost, 60000, "max_cost must equal the quoted price");
  assert.equal("max_job_cost" in capturedBodies[1], false, "must not use max_job_cost");
});

test("run: falls back to estimated_cost.max_microcents when no quoted price", async () => {
  const capturedBodies = [];
  const fetch = async (url, opts) => {
    if (opts?.body) capturedBodies.push(JSON.parse(opts.body));
    const idx = capturedBodies.length;
    const body =
      idx === 1
        ? { can_execute: true, estimated_cost: { max_microcents: 70000 } }
        : { status: "completed", job_id: "j2", output: { data: {} }, cost: { total_microcents: 65000 } };
    return { ok: true, status: 200, statusText: "OK", text: async () => JSON.stringify(body) };
  };
  await run(makeArgs(), { fetch, sleep: noSleep });
  assert.equal(capturedBodies[1].max_cost, 70000, "max_cost must fall back to estimated_cost.max_microcents");
});

test("run: throws before executing when plan has no cost fields", async () => {
  let executeCallMade = false;
  const fetch = async (url, opts) => {
    if (url.includes("/v1/execute")) executeCallMade = true;
    return {
      ok: true, status: 200, statusText: "OK",
      text: async () => JSON.stringify({ can_execute: true }),
    };
  };
  await assert.rejects(
    () => run(makeArgs(), { fetch, sleep: noSleep }),
    /cannot determine max cost/,
  );
  assert.equal(executeCallMade, false, "execute must not be called");
});

test("run: immediate completion — no polling", async () => {
  let fetchCallCount = 0;
  const fetch = async () => {
    fetchCallCount++;
    const body =
      fetchCallCount === 1
        ? { can_execute: true, quoted_customer_price_microcents: 60000 }
        : {
            status: "completed",
            job_id: "j3",
            output: { data: { organization: { name: "Stripe" } } },
            cost:   { total_microcents: 60000 },
          };
    return { ok: true, status: 200, statusText: "OK", text: async () => JSON.stringify(body) };
  };
  const result = await run(makeArgs(), { fetch, sleep: noSleep });
  assert.equal(fetchCallCount, 2, "must make exactly 2 calls (plan + execute), no GET poll");
  assert.equal(result.name, "Stripe");
  assert.equal(result.job_id, "j3");
});

test("run: polls when status is executing", async () => {
  let sleepCalls = 0;
  const sleep = () => { sleepCalls++; return Promise.resolve(); };
  const responses = [
    planOk(),
    { status: 200, body: { status: "executing", job_id: "j4" } },
    jobCompleted({ organization: { name: "Acme" } }),
  ];
  const result = await run(makeArgs(), { fetch: mockFetch(responses), sleep });
  assert.equal(sleepCalls, 1, "sleep must be called once before the poll");
  assert.equal(result.name, "Acme");
});

test("run: failed job → rejects with code and message", async () => {
  const responses = [
    planOk(),
    {
      status: 200,
      body: {
        status: "failed",
        job_id: "j5",
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
    { status: 200, body: { status: "cancelled", job_id: "j6" } },
  ];
  await assert.rejects(
    () => run(makeArgs(), { fetch: mockFetch(responses), sleep: noSleep }),
    /cancelled/,
  );
});

test("run: cost_usd absent when job has no cost field", async () => {
  const responses = [
    planOk(),
    { status: 200, body: { status: "completed", job_id: "j7", output: { data: {} } } },
  ];
  const result = await run(makeArgs(), { fetch: mockFetch(responses), sleep: noSleep });
  assert.equal("cost_usd" in result, false, "cost_usd must be absent when cost is missing");
});

test("run: domain, raw, and job_id always present in output", async () => {
  const responses = [planOk(), jobCompleted({})];
  const result = await run(makeArgs(), { fetch: mockFetch(responses), sleep: noSleep });
  assert.ok("domain" in result);
  assert.ok("raw" in result);
  assert.ok("job_id" in result);
  assert.equal(result.domain, "stripe.com");
  assert.equal(result.job_id, "job-123");
});
