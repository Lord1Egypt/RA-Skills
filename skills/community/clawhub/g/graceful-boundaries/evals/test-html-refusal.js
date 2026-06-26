#!/usr/bin/env node

/**
 * Graceful Boundaries HTML 429 refusal tests (v1.1).
 *
 * Validates that HTML rate-limit pages provide machine-accessible
 * retry information via <meta> and/or <link> tags.
 *
 * Usage: node evals/test-html-refusal.js
 */

const { checkHtmlRefusal } = require("./check.js");

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

// ─── Valid HTML 429 responses ────────────────────────────────────

test("HTML with retry-after meta and JSON alternate passes", () => {
  const html = `
    <html><head>
      <meta name="retry-after" content="42" />
      <link rel="alternate" type="application/json" href="/api/scan?format=json" />
    </head><body><h1>Too many requests</h1></body></html>
  `;
  const result = checkHtmlRefusal(html);
  assert(result.hasRetryMeta, "should detect retry-after meta");
  assert(result.retrySeconds === 42, `expected 42, got ${result.retrySeconds}`);
  assert(result.hasJsonAlternate, "should detect JSON alternate link");
  assert(result.jsonAlternateUrl === "/api/scan?format=json", "should extract href");
  assert(result.errors.length === 0, "should have no errors");
});

test("HTML with only retry-after meta is sufficient", () => {
  const html = `
    <html><head>
      <meta name="retry-after" content="60" />
    </head><body><p>Slow down</p></body></html>
  `;
  const result = checkHtmlRefusal(html);
  assert(result.hasRetryMeta, "should detect retry-after meta");
  assert(result.retrySeconds === 60, "should parse seconds");
  assert(!result.hasJsonAlternate, "no alternate link");
  assert(result.errors.length === 0, "meta alone is sufficient — no errors");
});

test("HTML with only JSON alternate link is sufficient", () => {
  const html = `
    <html><head>
      <link rel="alternate" type="application/json" href="/api/error.json" />
    </head><body><p>Rate limited</p></body></html>
  `;
  const result = checkHtmlRefusal(html);
  assert(!result.hasRetryMeta, "no retry meta");
  assert(result.hasJsonAlternate, "should detect JSON alternate");
  assert(result.errors.length === 0, "alternate link alone is sufficient");
});

// ─── Failing HTML 429 responses ──────────────────────────────────

test("HTML missing both meta and link fails", () => {
  const html = `
    <html><head><title>429</title></head>
    <body><h1>Too many requests</h1><p>Try again later.</p></body></html>
  `;
  const result = checkHtmlRefusal(html);
  assert(!result.hasRetryMeta, "no retry meta");
  assert(!result.hasJsonAlternate, "no alternate link");
  assert(result.errors.length > 0, "should report error");
  assert(result.errors.some((e) => e.includes("machine-accessible")), "should explain the problem");
});

test("Empty string fails", () => {
  const result = checkHtmlRefusal("");
  assert(result.errors.length > 0, "empty string should fail");
});

test("Null input fails", () => {
  const result = checkHtmlRefusal(null);
  assert(result.errors.length > 0, "null should fail");
});

// ─── Edge cases ──────────────────────────────────────────────────

test("Alternate link with wrong type warns", () => {
  const html = `
    <html><head>
      <meta name="retry-after" content="30" />
      <link rel="alternate" type="text/xml" href="/api/error.xml" />
    </head><body></body></html>
  `;
  const result = checkHtmlRefusal(html);
  assert(result.hasRetryMeta, "retry meta present");
  assert(!result.hasJsonAlternate, "wrong type should not count as JSON alternate");
  assert(result.warnings.some((w) => w.includes("text/xml")), "should warn about wrong type");
  assert(result.errors.length === 0, "meta is sufficient — no errors");
});

test("Meta with large retry value parses correctly", () => {
  const html = `<html><head><meta name="retry-after" content="86400" /></head><body></body></html>`;
  const result = checkHtmlRefusal(html);
  assert(result.hasRetryMeta, "should detect meta");
  assert(result.retrySeconds === 86400, `expected 86400, got ${result.retrySeconds}`);
});

test("Self-closing meta tag works", () => {
  const html = `<html><head><meta name="retry-after" content="10"/></head><body></body></html>`;
  const result = checkHtmlRefusal(html);
  assert(result.hasRetryMeta, "self-closing meta should work");
  assert(result.retrySeconds === 10, "should parse value");
});

test("Case-insensitive meta name matching", () => {
  const html = `<html><head><meta name="Retry-After" content="15" /></head><body></body></html>`;
  const result = checkHtmlRefusal(html);
  assert(result.hasRetryMeta, "should match case-insensitively");
  assert(result.retrySeconds === 15, "should parse value");
});

test("Link tag with attributes in different order", () => {
  const html = `
    <html><head>
      <link href="/api/error.json" type="application/json" rel="alternate" />
    </head><body></body></html>
  `;
  const result = checkHtmlRefusal(html);
  assert(result.hasJsonAlternate, "should detect regardless of attribute order");
  assert(result.jsonAlternateUrl === "/api/error.json", "should extract href");
});

// ─── Summary ─────────────────────────────────────────────────────

console.log("");
console.log(`${passed + failed} tests: ${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
