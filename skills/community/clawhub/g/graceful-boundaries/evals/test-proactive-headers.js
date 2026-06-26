#!/usr/bin/env node

/**
 * Graceful Boundaries proactive header validation tests.
 *
 * Tests RateLimit and RateLimit-Policy header parsing
 * and Level 4 conformance assessment.
 *
 * Usage: node evals/test-proactive-headers.js
 */

const { checkProactiveHeaders } = require("./check.js");

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

// ─── Valid proactive headers ─────────────────────────────────────

test("Fully conforming headers", () => {
  const result = checkProactiveHeaders({
    RateLimit: "limit=10, remaining=9, reset=3540",
    "RateLimit-Policy": "10;w=3600",
  });
  assert(result.hasProactiveHeaders, "should have proactive headers");
  assert(result.limitValue === 10, `expected limit=10, got ${result.limitValue}`);
  assert(result.remainingValue === 9, `expected remaining=9, got ${result.remainingValue}`);
  assert(result.resetValue === 3540, `expected reset=3540, got ${result.resetValue}`);
  assert(result.policyValid, "policy should be valid");
  assert(result.errors.length === 0, "should have no errors");
});

test("Headers with case variations", () => {
  const result = checkProactiveHeaders({
    ratelimit: "limit=60, remaining=59, reset=60",
    "ratelimit-policy": "60;w=60",
  });
  assert(result.hasProactiveHeaders, "should handle lowercase headers");
});

test("RateLimit without Policy is valid", () => {
  const result = checkProactiveHeaders({
    RateLimit: "limit=10, remaining=5, reset=1800",
  });
  assert(result.hasProactiveHeaders, "should be valid without policy");
  assert(result.policyValid === null, "policy should be null");
});

test("remaining=0 signals imminent limit", () => {
  const result = checkProactiveHeaders({
    RateLimit: "limit=10, remaining=0, reset=120",
  });
  assert(result.hasProactiveHeaders, "should be valid");
  assert(result.remainingValue === 0, "remaining should be 0");
});

test("Large values handled correctly", () => {
  const result = checkProactiveHeaders({
    RateLimit: "limit=10000, remaining=9999, reset=86400",
    "RateLimit-Policy": "10000;w=86400",
  });
  assert(result.hasProactiveHeaders, "should handle large values");
  assert(result.limitValue === 10000, "should parse large limit");
});

// ─── Missing components ──────────────────────────────────────────

test("Missing RateLimit header fails", () => {
  const result = checkProactiveHeaders({
    "RateLimit-Policy": "10;w=3600",
  });
  assert(!result.hasProactiveHeaders, "should fail without RateLimit");
  assert(result.errors.some((e) => e.includes("Missing RateLimit")), "should report missing header");
});

test("Missing 'limit' component fails", () => {
  const result = checkProactiveHeaders({
    RateLimit: "remaining=9, reset=3540",
  });
  assert(!result.hasProactiveHeaders, "should fail without limit component");
  assert(result.errors.some((e) => e.includes("limit")), "should report missing limit");
});

test("Missing 'remaining' component fails", () => {
  const result = checkProactiveHeaders({
    RateLimit: "limit=10, reset=3540",
  });
  assert(!result.hasProactiveHeaders, "should fail without remaining");
  assert(result.errors.some((e) => e.includes("remaining")), "should report missing remaining");
});

test("Missing 'reset' component fails", () => {
  const result = checkProactiveHeaders({
    RateLimit: "limit=10, remaining=9",
  });
  assert(!result.hasProactiveHeaders, "should fail without reset");
  assert(result.errors.some((e) => e.includes("reset")), "should report missing reset");
});

test("No headers at all fails", () => {
  const result = checkProactiveHeaders(null);
  assert(!result.hasProactiveHeaders, "should fail with null");
});

test("Empty headers object fails", () => {
  const result = checkProactiveHeaders({});
  assert(!result.hasProactiveHeaders, "should fail with empty object");
});

// ─── Invalid values ──────────────────────────────────────────────

test("Non-numeric limit value fails", () => {
  const result = checkProactiveHeaders({
    RateLimit: "limit=abc, remaining=9, reset=3540",
  });
  assert(!result.hasProactiveHeaders, "should fail with non-numeric limit");
  assert(result.errors.some((e) => e.includes("not a number")), "should report NaN");
});

test("remaining exceeding limit fails", () => {
  const result = checkProactiveHeaders({
    RateLimit: "limit=10, remaining=15, reset=3540",
  });
  assert(!result.hasProactiveHeaders, "should fail when remaining > limit");
  assert(result.errors.some((e) => e.includes("exceeds")), "should report remaining > limit");
});

test("Invalid RateLimit-Policy format flagged", () => {
  const result = checkProactiveHeaders({
    RateLimit: "limit=10, remaining=9, reset=3540",
    "RateLimit-Policy": "10 per 3600",
  });
  assert(result.hasProactiveHeaders, "RateLimit itself is valid");
  assert(!result.policyValid, "policy format should be invalid");
});

test("RateLimit-Policy without semicolon fails", () => {
  const result = checkProactiveHeaders({
    RateLimit: "limit=10, remaining=9, reset=3540",
    "RateLimit-Policy": "10",
  });
  assert(!result.policyValid, "policy without window should be invalid");
});

// ─── Summary ─────────────────────────────────────────────────────

console.log("");
console.log(`${passed + failed} tests: ${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
