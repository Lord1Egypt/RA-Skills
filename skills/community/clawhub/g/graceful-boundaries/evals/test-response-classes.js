#!/usr/bin/env node

/**
 * Graceful Boundaries response class validation tests.
 *
 * Tests every response class defined in the spec:
 *   - Limit (429)
 *   - Input (400, 405, 422)
 *   - Access (401, 403)
 *   - Not Found (404, 410)
 *   - Availability (500, 502, 503, 504)
 *   - Success (200) — proactive headers
 *   - Resource Deduplication (200 with _rescanBlocked)
 *   - Error field stability
 *
 * Usage: node evals/test-response-classes.js
 */

const { checkDedupResponse, checkResponseBody, isStableErrorValue } = require("./check.js");

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

const CORE_FIELDS = ["error", "detail"];

function hasCore(body) {
  return CORE_FIELDS.every((f) => typeof body[f] === "string" && body[f].length > 0);
}

function hasWhy(body) {
  return typeof body.why === "string" && body.why.length > 0;
}

function whyExplainsNotRestates(body) {
  if (!body.why || !body.error) return false;
  const errorWords = body.error.toLowerCase().replace(/_/g, " ");
  return !body.why.toLowerCase().includes(errorWords);
}

function detailIsActionable(body) {
  // Detail should tell the caller what to DO, not just what happened
  const d = body.detail.toLowerCase();
  return (
    d.includes("try") ||
    d.includes("use") ||
    d.includes("provide") ||
    d.includes("check") ||
    d.includes("scan") ||
    d.includes("wait") ||
    d.includes("contact") ||
    d.includes("fix") ||
    d.includes("how to") ||
    d.includes("can") ||
    d.includes("available")
  );
}

// ─── Class: Limit (429) ──────────────────────────────────────────

test("Limit: conforming 429 has all required fields", () => {
  const body = {
    error: "rate_limit_exceeded",
    detail: "You can run up to 10 scans per hour. Try again in 42 seconds.",
    limit: "10 scans per IP per hour",
    retryAfterSeconds: 42,
    why: "Rate limits keep the service available for everyone and prevent abuse.",
  };
  assert(hasCore(body), "missing core fields");
  assert(hasWhy(body), "missing why");
  assert(typeof body.limit === "string", "missing limit");
  assert(typeof body.retryAfterSeconds === "number", "missing retryAfterSeconds");
  assert(whyExplainsNotRestates(body), "why restates error");
});

test("Limit: constructive 429 includes alternative", () => {
  const body = {
    error: "rate_limit_exceeded",
    detail: "Try again in 42 seconds.",
    limit: "10 per hour",
    retryAfterSeconds: 42,
    why: "Prevents abuse.",
    alternativeEndpoint: "/api/result?id=example.com",
  };
  assert(typeof body.alternativeEndpoint === "string", "missing alternativeEndpoint");
});

test("Limit: 429 without limit field fails class validation", () => {
  const body = {
    error: "rate_limit_exceeded",
    detail: "Too many requests.",
    retryAfterSeconds: 60,
    why: "Prevents abuse.",
  };
  assert(typeof body.limit !== "string", "should fail without limit");
});

// ─── Class: Input (400, 405, 422) ────────────────────────────────

test("Input: conforming 400 explains what's wrong and how to fix", () => {
  const body = {
    error: "invalid_input",
    detail: "This URL points to a private or reserved address and cannot be scanned.",
    why: "Blocks private IPs to prevent server-side request forgery.",
    field: "url",
    expected: "A public URL with a resolvable hostname on port 80 or 443.",
  };
  assert(hasCore(body), "missing core fields");
  assert(hasWhy(body), "missing why");
  assert(typeof body.field === "string", "missing field");
  assert(typeof body.expected === "string", "missing expected");
});

test("Input: 400 without field/expected is valid but less helpful", () => {
  const body = {
    error: "invalid_input",
    detail: "A URL is required.",
  };
  assert(hasCore(body), "has core fields");
  assert(!body.field, "field is optional");
});

test("Input: conforming 405 lists allowed methods", () => {
  const body = {
    error: "method_not_allowed",
    detail: "This endpoint only accepts GET requests.",
    allowedMethods: ["GET"],
  };
  assert(hasCore(body), "missing core fields");
  assert(Array.isArray(body.allowedMethods), "missing allowedMethods");
});

// ─── Class: Access (401, 403) ────────────────────────────────────

test("Access: conforming 403 explains the security policy", () => {
  const body = {
    error: "forbidden",
    detail: "API key required for batch operations. Free scans are available at the public endpoint.",
    why: "Batch access requires authentication to prevent abuse and track usage.",
    authUrl: "https://example.com/api/keys",
    alternativeEndpoint: "/api/scan",
  };
  assert(hasCore(body), "missing core fields");
  assert(hasWhy(body), "missing why");
  assert(whyExplainsNotRestates(body), "why explains security policy");
});

test("Access: 403 with only 'forbidden' as detail is not actionable", () => {
  const body = {
    error: "forbidden",
    detail: "Forbidden.",
  };
  assert(!detailIsActionable(body), "vague detail should not pass actionability check");
});

// ─── Class: Not Found (404, 410) ─────────────────────────────────

test("Not Found: conforming 404 distinguishes never-existed from expired", () => {
  const body = {
    error: "result_not_found",
    detail: "No scan result exists for example.com. This domain has not been scanned yet.",
    why: "Results are kept for 30 days. This domain may not have been scanned.",
    scanAvailable: true,
    scanUrl: "/api/scan?url=https://example.com",
    humanUrl: "https://siteline.to/?url=example.com",
  };
  assert(hasCore(body), "missing core fields");
  assert(body.scanAvailable === true, "should indicate scan is available");
  assert(typeof body.scanUrl === "string", "should provide scan URL");
  assert(typeof body.humanUrl === "string", "should provide human URL");
});

test("Not Found: 404 with scan capability is constructive", () => {
  const body = {
    error: "result_not_found",
    detail: "Not found.",
    scanAvailable: true,
    scanUrl: "/api/scan?url=https://example.com",
  };
  assert(body.scanAvailable && body.scanUrl, "constructive 404 offers creation path");
});

test("Not Found: 410 Gone indicates permanence", () => {
  const body = {
    error: "gone",
    detail: "This result has been permanently removed.",
    why: "Results older than 30 days are deleted to manage storage.",
  };
  assert(hasCore(body), "missing core fields");
  assert(body.error === "gone", "should use 'gone' not 'not_found'");
});

// ─── Class: Availability (500, 502, 503, 504) ────────────────────

test("Availability: conforming 503 indicates transience and retry", () => {
  const body = {
    error: "service_unavailable",
    detail: "Result storage is temporarily unavailable. Scans still work but results are not persisted.",
    why: "The storage backend is unreachable. This is usually transient.",
    retryAfterSeconds: 60,
  };
  assert(hasCore(body), "missing core fields");
  assert(hasWhy(body), "missing why");
  assert(typeof body.retryAfterSeconds === "number", "should suggest retry timing");
});

test("Availability: 500 without why gives no diagnostic value", () => {
  const body = {
    error: "internal_error",
    detail: "An unexpected error occurred.",
  };
  assert(hasCore(body), "has core fields");
  assert(!hasWhy(body), "missing why — caller can't diagnose");
});

test("Availability: 503 with statusUrl is maximally helpful", () => {
  const body = {
    error: "service_unavailable",
    detail: "Scheduled maintenance until 14:00 UTC.",
    why: "Database migration in progress.",
    retryAfterSeconds: 3600,
    statusUrl: "https://status.example.com",
    humanUrl: "https://example.com/contact",
  };
  assert(body.statusUrl && body.humanUrl, "provides both status and human URLs");
});

// ─── Class: Success (200) ────────────────────────────────────────

test("Success: proactive headers present", () => {
  const headers = {
    ratelimit: "limit=60, remaining=59, reset=60",
    "ratelimit-policy": "60;w=60",
  };
  assert(headers.ratelimit, "missing RateLimit header");
  assert(headers["ratelimit-policy"], "missing RateLimit-Policy header");

  const parts = headers.ratelimit.split(",").map((s) => s.trim());
  const limitPart = parts.find((p) => p.startsWith("limit="));
  const remainingPart = parts.find((p) => p.startsWith("remaining="));
  const resetPart = parts.find((p) => p.startsWith("reset="));
  assert(limitPart, "RateLimit missing limit");
  assert(remainingPart, "RateLimit missing remaining");
  assert(resetPart, "RateLimit missing reset");
});

test("Success: remaining=0 signals imminent limit", () => {
  const remaining = 0;
  assert(remaining === 0, "should signal caller to stop");
  // A well-behaved caller seeing remaining=0 should not make another request
});

// ─── Cross-class: why MUST (v1.1) ────────────────────────────────

test("v1.1: Input (400) missing why fails checkResponseBody", () => {
  const result = checkResponseBody({
    error: "invalid_input",
    detail: "A URL is required.",
  }, "input");
  assert(!result.isValid, "should fail without why");
  assert(result.missingFields.includes("why"), "should list why as missing");
});

test("v1.1: Input (400) with why passes checkResponseBody", () => {
  const result = checkResponseBody({
    error: "invalid_input",
    detail: "This URL points to a private address and cannot be scanned.",
    why: "Blocks private IPs to prevent server-side request forgery.",
  }, "input");
  assert(result.isValid, "should pass with all required fields");
  assert(result.missingFields.length === 0, "no missing fields");
});

test("v1.1: Not Found (404) missing why fails checkResponseBody", () => {
  const result = checkResponseBody({
    error: "result_not_found",
    detail: "No scan result exists for example.com.",
  }, "not-found");
  assert(!result.isValid, "should fail without why");
  assert(result.missingFields.includes("why"), "should list why as missing");
});

test("v1.1: Availability (500) missing why fails checkResponseBody", () => {
  const result = checkResponseBody({
    error: "internal_error",
    detail: "An unexpected error occurred.",
  }, "availability");
  assert(!result.isValid, "should fail without why");
  assert(result.missingFields.includes("why"), "should list why as missing");
});

test("v1.1: Access (403) with why passes checkResponseBody", () => {
  const result = checkResponseBody({
    error: "forbidden",
    detail: "API key required for batch operations.",
    why: "Batch access requires authentication to prevent abuse and track usage.",
  }, "access");
  assert(result.isValid, "should pass with all required fields");
});

test("v1.1: Limit (429) missing limit field fails class-specific check", () => {
  const result = checkResponseBody({
    error: "rate_limit_exceeded",
    detail: "Try again in 42 seconds.",
    why: "Prevents abuse.",
    retryAfterSeconds: 42,
  }, "limit");
  assert(!result.isValid, "should fail without limit field");
  assert(result.errors.some((e) => e.includes("limit")), "should report missing limit");
});

test("v1.1: checkResponseBody warns when why restates error", () => {
  const result = checkResponseBody({
    error: "not_found",
    detail: "The resource was not found.",
    why: "The resource was not found.",
  }, "not-found");
  assert(result.isValid, "still valid — why quality is a warning");
  assert(result.warnings.some((w) => w.includes("restates")), "should warn about restated why");
});

// ─── Cross-class: why quality ────────────────────────────────────

test("Quality: why should explain security intent, not restate error", () => {
  const examples = [
    { error: "rate_limit_exceeded", why: "Rate limit exceeded." },
    { error: "forbidden", why: "Access is forbidden." },
    { error: "not_found", why: "The resource was not found." },
  ];
  examples.forEach((ex) => {
    assert(!whyExplainsNotRestates(ex), `why for ${ex.error} restates error — should fail`);
  });
});

test("Quality: good why fields explain the purpose", () => {
  const examples = [
    { error: "rate_limit_exceeded", why: "Prevents the scan engine from being used as a proxy to attack other sites." },
    { error: "forbidden", why: "Batch access requires authentication to track usage and prevent abuse." },
    { error: "result_not_found", why: "Results are kept for 30 days to manage storage costs." },
  ];
  examples.forEach((ex) => {
    assert(whyExplainsNotRestates(ex), `why for ${ex.error} should explain purpose`);
  });
});

// ─── Resource Deduplication (spec section 5) ─────────────────────

test("Dedup: conforming response includes flag and result data", () => {
  const result = checkDedupResponse({
    grade: "B",
    score: 82,
    _rescanBlocked: true,
    _cacheStatus: "KV_HIT",
  });
  assert(result.isDedup, "should be identified as dedup");
  assert(result.hasRescanBlocked, "should have _rescanBlocked");
  assert(result.hasCacheStatus, "should have _cacheStatus");
  assert(result.hasResultData, "should have result data");
  assert(result.errors.length === 0, "should have no errors");
});

test("Dedup: missing _rescanBlocked flag fails", () => {
  const result = checkDedupResponse({
    grade: "B",
    score: 82,
  });
  assert(!result.isDedup, "should not be identified as dedup");
  assert(result.errors.some((e) => e.includes("_rescanBlocked")), "should report missing flag");
});

test("Dedup: _rescanBlocked=false is not a dedup response", () => {
  const result = checkDedupResponse({
    grade: "B",
    _rescanBlocked: false,
  });
  assert(!result.isDedup, "false flag should not count as dedup");
});

test("v1.1 Dedup: returnsCached in discovery predicts 200 with data", () => {
  // When discovery says returnsCached: true, agents expect a 200 with cached data
  // not a 429 refusal. Verify the dedup response matches that expectation.
  const dedupBody = {
    grade: "B",
    score: 82,
    _rescanBlocked: true,
    _cacheStatus: "KV_HIT",
  };
  const result = checkDedupResponse(dedupBody);
  assert(result.isDedup, "should be a dedup response");
  assert(result.hasResultData, "should include result data — consistent with returnsCached: true");
  assert(result.errors.length === 0, "no errors");
});

test("Dedup: flag without result data warns", () => {
  const result = checkDedupResponse({
    _rescanBlocked: true,
  });
  assert(result.isDedup, "should be identified as dedup");
  assert(!result.hasResultData, "should flag missing result data");
});

// ─── Error field stability ───────────────────────────────────────

test("Stable error: snake_case values pass", () => {
  assert(isStableErrorValue("rate_limit_exceeded"), "rate_limit_exceeded should pass");
  assert(isStableErrorValue("not_found"), "not_found should pass");
  assert(isStableErrorValue("invalid_input"), "invalid_input should pass");
  assert(isStableErrorValue("cooldown_active"), "cooldown_active should pass");
  assert(isStableErrorValue("resource_dedup"), "resource_dedup should pass");
});

test("Stable error: kebab-case values pass", () => {
  assert(isStableErrorValue("rate-limit-exceeded"), "kebab-case should pass");
  assert(isStableErrorValue("not-found"), "kebab-case should pass");
});

test("Stable error: single word passes", () => {
  assert(isStableErrorValue("forbidden"), "single word should pass");
  assert(isStableErrorValue("timeout"), "single word should pass");
});

test("Stable error: human-readable strings fail", () => {
  assert(!isStableErrorValue("Rate limit exceeded"), "spaces should fail");
  assert(!isStableErrorValue("Too many requests"), "spaces should fail");
  assert(!isStableErrorValue("Not Found"), "uppercase should fail");
});

test("Stable error: punctuation fails", () => {
  assert(!isStableErrorValue("rate_limit_exceeded."), "trailing period should fail");
  assert(!isStableErrorValue("error!"), "exclamation should fail");
});

test("Stable error: empty or non-string fails", () => {
  assert(!isStableErrorValue(""), "empty string should fail");
  assert(!isStableErrorValue(null), "null should fail");
  assert(!isStableErrorValue(429), "number should fail");
});

// ─── Summary ─────────────────────────────────────────────────────

console.log("");
console.log(`${passed + failed} tests: ${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
