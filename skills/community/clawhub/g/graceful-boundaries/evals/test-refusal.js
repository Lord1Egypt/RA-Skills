#!/usr/bin/env node

/**
 * Unit tests for Graceful Boundaries refusal body validation.
 *
 * Tests the checkRefusalBody function against conforming and
 * non-conforming response bodies without hitting a live service.
 *
 * Usage: node evals/test-refusal.js
 */

const { checkRefusalBody, assessLevel, REQUIRED_REFUSAL_FIELDS } = require("./check.js");

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`PASS  ${name}`);
    passed++;
  } catch (error) {
    console.log(`FAIL  ${name}: ${error.message}`);
    failed++;
  }
}

function assert(condition, message) {
  if (!condition) throw new Error(message || "Assertion failed");
}

// ─── Level 1: Structured Refusal ─────────────────────────────────

test("Level 1: conforming refusal has all required fields", () => {
  const body = {
    error: "rate_limit_exceeded",
    detail: "You can run up to 10 scans per hour. Try again in 42 seconds.",
    limit: "10 scans per IP per hour",
    retryAfterSeconds: 42,
    why: "Rate limits keep the service available for everyone.",
  };
  const result = checkRefusalBody(body);
  assert(result.isJson, "should be JSON");
  assert(result.hasRequiredFields, "should have all required fields");
  assert(result.missingFields.length === 0, "should have no missing fields");
});

test("Level 1: missing 'why' field fails", () => {
  const body = {
    error: "rate_limit_exceeded",
    detail: "Try again in 42 seconds.",
    limit: "10 per hour",
    retryAfterSeconds: 42,
  };
  const result = checkRefusalBody(body);
  assert(!result.hasRequiredFields, "should fail without 'why'");
  assert(result.missingFields.includes("why"), "should list 'why' as missing");
});

test("Level 1: missing 'retryAfterSeconds' field fails", () => {
  const body = {
    error: "rate_limit_exceeded",
    detail: "Try again later.",
    limit: "10 per hour",
    why: "Prevents abuse.",
  };
  const result = checkRefusalBody(body);
  assert(!result.hasRequiredFields, "should fail without retryAfterSeconds");
});

test("Level 1: generic body with only 'error' fails", () => {
  const body = { error: "rate limit exceeded" };
  const result = checkRefusalBody(body);
  assert(!result.hasRequiredFields, "should fail with only error");
  assert(result.missingFields.length === 4, "should have 4 missing fields");
});

test("Level 1: non-JSON body fails", () => {
  const result = checkRefusalBody("Too many requests");
  assert(!result.isJson, "should not be JSON");
  assert(!result.hasRequiredFields, "should fail");
});

// ─── Quality checks ──────────────────────────────────────────────

test("Quality: 'why' should not just restate the error", () => {
  const body = {
    error: "rate_limit_exceeded",
    detail: "Try again in 42 seconds.",
    limit: "10 per hour",
    retryAfterSeconds: 42,
    why: "Rate limit exceeded.",
  };
  const result = checkRefusalBody(body);
  assert(!result.whyIsNotRestated, "'why' restates the error — should flag this");
});

test("Quality: 'why' that explains purpose passes", () => {
  const body = {
    error: "rate_limit_exceeded",
    detail: "Try again in 42 seconds.",
    limit: "10 per hour",
    retryAfterSeconds: 42,
    why: "This limit prevents the scan engine from being used as a proxy.",
  };
  const result = checkRefusalBody(body);
  assert(result.whyIsNotRestated, "'why' explains purpose — should pass");
});

test("Quality: 'detail' should include specific time", () => {
  const body = {
    error: "rate_limit_exceeded",
    detail: "You can run up to 10 scans per hour. Try again in 42 seconds.",
    limit: "10 per hour",
    retryAfterSeconds: 42,
    why: "Keeps the service available.",
  };
  const result = checkRefusalBody(body);
  assert(result.detailIncludesTime, "detail should mention seconds/minutes");
});

test("Quality: vague 'detail' without time flagged", () => {
  const body = {
    error: "rate_limit_exceeded",
    detail: "Too many requests. Try again later.",
    limit: "10 per hour",
    retryAfterSeconds: 42,
    why: "Keeps the service available.",
  };
  const result = checkRefusalBody(body);
  assert(!result.detailIncludesTime, "vague detail should be flagged");
});

// ─── Level 3: Constructive Guidance ──────────────────────────────

test("Level 3: constructive fields detected", () => {
  const body = {
    error: "rate_limit_exceeded",
    detail: "Try again in 42 seconds.",
    limit: "10 per hour",
    retryAfterSeconds: 42,
    why: "Keeps the service available.",
    cachedResultUrl: "/api/result?id=example-com-20260321",
    alternativeEndpoint: "/api/result?id=example.com",
  };
  const result = checkRefusalBody(body);
  assert(result.hasConstructiveFields, "should detect constructive fields");
  assert(result.constructiveFields.length === 2, "should find 2 constructive fields");
});

test("Level 3: no constructive fields when absent", () => {
  const body = {
    error: "rate_limit_exceeded",
    detail: "Try again in 42 seconds.",
    limit: "10 per hour",
    retryAfterSeconds: 42,
    why: "Keeps the service available.",
  };
  const result = checkRefusalBody(body);
  assert(!result.hasConstructiveFields, "should not detect constructive fields");
});

// ─── Level Assessment ────────────────────────────────────────────

test("Assessment: N/A when declared with empty limits", () => {
  const level = assessLevel(
    [{ found: true, wellFormed: true, conformance: "not-applicable", limitCount: 0 }],
    null
  );
  assert(level === "not-applicable", `expected "not-applicable", got ${level}`);
});

test("Assessment: N/A declaration ignored when limits exist", () => {
  const level = assessLevel(
    [{ found: true, wellFormed: true, conformance: "not-applicable", limitCount: 2 }],
    checkRefusalBody({
      error: "rate_limit_exceeded",
      detail: "Try again in 42 seconds.",
      limit: "10 per hour",
      retryAfterSeconds: 42,
      why: "Keeps things running.",
    })
  );
  assert(level !== "not-applicable", `should not be N/A when limits exist, got ${level}`);
});

test("Assessment: Level 0 when nothing passes", () => {
  const level = assessLevel(
    [{ found: false }],
    checkRefusalBody({ error: "too many" })
  );
  assert(level === 0, `expected 0, got ${level}`);
});

test("Assessment: Level 1 with structured refusal only", () => {
  const level = assessLevel(
    [{ found: false }],
    checkRefusalBody({
      error: "rate_limit_exceeded",
      detail: "Try again in 42 seconds.",
      limit: "10 per hour",
      retryAfterSeconds: 42,
      why: "Keeps things running.",
    })
  );
  assert(level === 1, `expected 1, got ${level}`);
});

test("Assessment: Level 2 with discovery + structured refusal", () => {
  const level = assessLevel(
    [{ found: true, wellFormed: true }],
    checkRefusalBody({
      error: "rate_limit_exceeded",
      detail: "Try again in 42 seconds.",
      limit: "10 per hour",
      retryAfterSeconds: 42,
      why: "Keeps things running.",
    })
  );
  assert(level === 2, `expected 2, got ${level}`);
});

test("Assessment: Level 3 with discovery + refusal + guidance", () => {
  const level = assessLevel(
    [{ found: true, wellFormed: true }],
    checkRefusalBody({
      error: "rate_limit_exceeded",
      detail: "Try again in 42 seconds.",
      limit: "10 per hour",
      retryAfterSeconds: 42,
      why: "Keeps things running.",
      cachedResultUrl: "/api/result?id=test",
    })
  );
  assert(level === 3, `expected 3, got ${level}`);
});

// ─── Summary ─────────────────────────────────────────────────────

console.log("");
console.log(`${passed + failed} tests: ${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
