#!/usr/bin/env node

/**
 * Graceful Boundaries conformance declaration tests.
 *
 * Validates that self-declared conformance levels are consistent
 * with actual service behavior and spec rules.
 *
 * Usage: node evals/test-conformance.js
 */

const {
  checkRefusalBody,
  checkLimitsBody,
  checkProactiveHeaders,
  assessLevel,
  VALID_CONFORMANCE_VALUES,
} = require("./check.js");

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

// ─── Valid conformance values ────────────────────────────────────

test("Valid conformance values accepted", () => {
  for (const value of VALID_CONFORMANCE_VALUES) {
    const result = checkLimitsBody({
      service: "Test",
      description: "Test service.",
      conformance: value,
      limits: {},
    });
    assert(result.conformanceValid, `"${value}" should be valid`);
  }
});

test("Invalid conformance value flagged", () => {
  const result = checkLimitsBody({
    service: "Test",
    description: "Test service.",
    conformance: "level-5",
    limits: {},
  });
  assert(!result.conformanceValid, "should flag invalid value");
  assert(result.errors.some((e) => e.includes("level-5")), "error should mention the bad value");
});

test("Unknown conformance value flagged", () => {
  const result = checkLimitsBody({
    service: "Test",
    conformance: "advanced",
    limits: {},
  });
  assert(!result.conformanceValid, "should flag unknown value");
});

test("Missing conformance field is valid (optional)", () => {
  const result = checkLimitsBody({
    service: "Test",
    limits: {},
  });
  assert(result.conformance === null, "should be null when absent");
  assert(result.conformanceValid, "absent conformance is valid");
});

// ─── N/A consistency ─────────────────────────────────────────────

test("N/A with empty limits is consistent", () => {
  const result = checkLimitsBody({
    service: "My Blog",
    description: "Personal blog.",
    conformance: "not-applicable",
    limits: {},
  });
  assert(result.conformanceConsistent, "N/A + empty limits should be consistent");
  assert(result.isValid, "should be valid");
});

test("N/A with populated limits is inconsistent", () => {
  const result = checkLimitsBody({
    service: "My API",
    description: "Has rate limits.",
    conformance: "not-applicable",
    limits: {
      scan: {
        endpoint: "/api/scan",
        method: "GET",
        limits: [
          { type: "ip-rate", maxRequests: 10, windowSeconds: 3600, description: "10 per hour" },
        ],
      },
    },
  });
  assert(!result.conformanceConsistent, "N/A + limits should be inconsistent");
  assert(!result.isValid, "should be invalid");
});

// ─── "none" consistency ──────────────────────────────────────────

test("'none' with empty limits is consistent", () => {
  const result = checkLimitsBody({
    service: "Example API",
    description: "REST API with rate limiting.",
    conformance: "none",
    limits: {},
  });
  assert(result.conformanceConsistent, "'none' + empty limits is consistent");
  assert(result.isValid, "should be valid");
});

test("'none' with populated limits warns about understatement", () => {
  const result = checkLimitsBody({
    service: "Example API",
    description: "REST API with rate limiting.",
    conformance: "none",
    limits: {
      scan: {
        endpoint: "/api/scan",
        method: "GET",
        limits: [
          { type: "ip-rate", maxRequests: 10, windowSeconds: 3600, description: "10 per hour" },
        ],
      },
    },
  });
  assert(result.warnings.some((w) => w.includes("understate")), "should warn about understatement");
});

// ─── Declared vs. validated level ────────────────────────────────

test("Declared level-3 matches validated Level 3", () => {
  const validated = assessLevel(
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
  assert(validated === 3, `expected 3, got ${validated}`);
  // A service declaring "level-3" with this behavior: declaration matches
});

test("Declared level-3 but validated Level 1 is a mismatch", () => {
  const validated = assessLevel(
    [{ found: false }],
    checkRefusalBody({
      error: "rate_limit_exceeded",
      detail: "Try again in 42 seconds.",
      limit: "10 per hour",
      retryAfterSeconds: 42,
      why: "Keeps things running.",
    })
  );
  assert(validated === 1, `expected 1, got ${validated}`);
  // A service declaring "level-3" but validating at 1: declaration overstates
  assert(validated < 3, "validated level should be below declared");
});

test("Declared level-1 but validated Level 3 is an understatement", () => {
  const validated = assessLevel(
    [{ found: true, wellFormed: true }],
    checkRefusalBody({
      error: "rate_limit_exceeded",
      detail: "Try again in 42 seconds.",
      limit: "10 per hour",
      retryAfterSeconds: 42,
      why: "Keeps things running.",
      alternativeEndpoint: "/api/result?id=test",
    })
  );
  assert(validated === 3, `expected 3, got ${validated}`);
  // A service declaring "level-1" but validating at 3: understatement (safe but imprecise)
  assert(validated > 1, "validated level exceeds declared");
});

test("Declared N/A but service has limits is a misclassification", () => {
  const validated = assessLevel(
    [{ found: true, wellFormed: true, conformance: "not-applicable", limitCount: 2 }],
    checkRefusalBody({
      error: "rate_limit_exceeded",
      detail: "Try again in 42 seconds.",
      limit: "10 per hour",
      retryAfterSeconds: 42,
      why: "Keeps things running.",
    })
  );
  assert(validated !== "not-applicable", "should not validate as N/A when limits exist");
});

// ─── Level 4 assessment ──────────────────────────────────────────

test("Level 4 requires Level 3 + proactive headers", () => {
  const headers = checkProactiveHeaders({
    RateLimit: "limit=10, remaining=9, reset=3540",
    "RateLimit-Policy": "10;w=3600",
  });
  const validated = assessLevel(
    [{ found: true, wellFormed: true }],
    checkRefusalBody({
      error: "rate_limit_exceeded",
      detail: "Try again in 42 seconds.",
      limit: "10 per hour",
      retryAfterSeconds: 42,
      why: "Keeps things running.",
      cachedResultUrl: "/api/result?id=test",
    }),
    headers
  );
  assert(validated === 4, `expected 4, got ${validated}`);
});

test("Level 3 + bad headers does not reach Level 4", () => {
  const headers = checkProactiveHeaders({
    RateLimit: "limit=10",
  });
  const validated = assessLevel(
    [{ found: true, wellFormed: true }],
    checkRefusalBody({
      error: "rate_limit_exceeded",
      detail: "Try again in 42 seconds.",
      limit: "10 per hour",
      retryAfterSeconds: 42,
      why: "Keeps things running.",
      cachedResultUrl: "/api/result?id=test",
    }),
    headers
  );
  assert(validated === 3, `expected 3, got ${validated}`);
});

test("Level 4 not reachable without constructive fields", () => {
  const headers = checkProactiveHeaders({
    RateLimit: "limit=10, remaining=9, reset=3540",
    "RateLimit-Policy": "10;w=3600",
  });
  const validated = assessLevel(
    [{ found: true, wellFormed: true }],
    checkRefusalBody({
      error: "rate_limit_exceeded",
      detail: "Try again in 42 seconds.",
      limit: "10 per hour",
      retryAfterSeconds: 42,
      why: "Keeps things running.",
    }),
    headers
  );
  assert(validated === 2, `expected 2, got ${validated}`);
});

// ─── Summary ─────────────────────────────────────────────────────

console.log("");
console.log(`${passed + failed} tests: ${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
