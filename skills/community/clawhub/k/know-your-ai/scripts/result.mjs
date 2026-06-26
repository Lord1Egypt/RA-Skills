#!/usr/bin/env node

/**
 * Know Your AI — Result
 * View results of a specific evaluation run.
 *
 * Usage: result.mjs <run-id>
 * Requires: node (>=18), KNOW_YOUR_AI_DSN env var
 */

import { parseDsn, gql, requireDsn, formatError, sanitizeId } from "./lib/helpers.mjs";

function usage() {
  console.error('Usage: result.mjs <run-id>');
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const runId = sanitizeId(args[0], "Run ID");

const dsn = requireDsn();
const parsed = parseDsn(dsn);

try {
  const query = `
    query GetEvaluationRun($id: ID!) {
      getEvaluationRun(id: $id) {
        id
        evaluationID
        status
        score
        totalTests
        secureCount
        vulnerableCount
        duration
        createdAt
        completedAt
      }
    }
  `;

  const data = await gql(parsed, query, { id: runId });
  const run = data?.data?.getEvaluationRun;

  if (!run) {
    console.error(`✖ Run not found: ${runId}`);
    process.exit(1);
  }

  console.log("## Evaluation Run Result\n");
  console.log("─".repeat(50));
  console.log(`  Run ID:          ${run.id}`);
  console.log(`  Evaluation ID:   ${run.evaluationID || "N/A"}`);
  console.log(`  Status:          ${run.status}`);
  console.log(`  Total tests:     ${run.totalTests ?? "N/A"}`);
  console.log(`  Secure:          ${run.secureCount ?? "N/A"}`);
  console.log(`  Vulnerable:      ${run.vulnerableCount ?? "N/A"}`);
  if (run.score != null) {
    console.log(`  Score:           ${(run.score * 100).toFixed(1)}%`);
  }
  if (run.duration != null) {
    console.log(`  Duration:        ${run.duration.toFixed(1)}s`);
  }
  if (run.createdAt) {
    console.log(`  Started:         ${new Date(run.createdAt).toLocaleString()}`);
  }
  if (run.completedAt) {
    console.log(`  Completed:       ${new Date(run.completedAt).toLocaleString()}`);
  }
  console.log("─".repeat(50));

  if (run.vulnerableCount > 0) {
    console.log(`\n⚠ ${run.vulnerableCount} out of ${run.totalTests} tests found vulnerabilities.`);
    console.log("ℹ Review detailed results in the Know Your AI dashboard.");
  } else if (run.status === "COMPLETED") {
    console.log("\n✔ All tests passed — no vulnerabilities detected.");
  }
} catch (err) {
  console.error(`✖ ${formatError(err)}`);
  process.exit(1);
}
