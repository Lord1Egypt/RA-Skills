#!/usr/bin/env node

/**
 * Know Your AI — Doctor (connectivity check)
 * Validates DSN configuration and tests API connectivity.
 *
 * Requires: node (>=18), KNOW_YOUR_AI_DSN env var
 */

import { parseDsn, gql, requireDsn } from "./lib/helpers.mjs";

const dsn = requireDsn();

let parsed;
try {
  parsed = parseDsn(dsn);
} catch (e) {
  console.error(`✖ Invalid DSN format: ${e.message}`);
  process.exit(1);
}

console.log("Know Your AI CLI — Doctor\n");
console.log("Checking your configuration and connectivity...\n");

const checks = [];

// Check 1: DSN is set
checks.push({ name: "KNOW_YOUR_AI_DSN", ok: true, detail: "Environment variable is set" });

// Check 2: DSN format
checks.push({
  name: "DSN Format",
  ok: true,
  detail: `Host: ${parsed.host} | Product: ${parsed.productId}`,
});

// Check 3: API Key
const keyPreview = parsed.apiKey.length > 8
  ? parsed.apiKey.slice(0, 8) + "..."
  : parsed.apiKey;
checks.push({
  name: "API Key",
  ok: parsed.apiKey.startsWith("kya_"),
  detail: parsed.apiKey.startsWith("kya_")
    ? `Valid KYA key: ${keyPreview}`
    : `Key does not start with kya_: ${keyPreview}`,
});

// Check 4: API Connection
try {
  const testQuery = `
    query ListEvaluations($productId: String!) {
      listEvaluations(filter: { productID: { eq: $productId } }, limit: 1) {
        items { id name }
      }
    }
  `;

  const data = await gql(parsed, testQuery, { productId: parsed.productId });

  checks.push({ name: "API Connection", ok: true, detail: "Connected successfully" });
  const items = data?.data?.listEvaluations?.items ?? [];
  checks.push({ name: "Evaluations", ok: true, detail: `Query returned ${items.length} evaluation(s) (limit 1)` });
} catch (err) {
  checks.push({ name: "API Connection", ok: false, detail: `Connection failed: ${err.message}` });
}

// Print results
console.log("Results");
console.log("─".repeat(56));
for (const c of checks) {
  const icon = c.ok ? "✔" : "✖";
  console.log(`  ${icon} ${c.name}`);
  console.log(`    ${c.detail}`);
}
console.log("─".repeat(56));

const allOk = checks.every((c) => c.ok);
if (allOk) {
  console.log("✔ All checks passed! You're ready to run evaluations.");
} else {
  console.log("✖ Some checks failed. Please review the errors above.");
  process.exit(1);
}
