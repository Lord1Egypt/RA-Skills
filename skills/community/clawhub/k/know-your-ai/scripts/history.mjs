#!/usr/bin/env node

/**
 * Know Your AI — History
 * Show recent evaluation runs.
 *
 * Usage: history.mjs [-a | --all]
 * Requires: node (>=18), KNOW_YOUR_AI_DSN env var
 */

import { parseDsn, gql, requireDsn, formatError } from "./lib/helpers.mjs";

const args = process.argv.slice(2);
const showAll = args.includes("-a") || args.includes("--all");
const limit = showAll ? 100 : 10;

const dsn = requireDsn();
const parsed = parseDsn(dsn);

try {
  const query = `
    query ListEvaluationRuns($productId: String!, $limit: Int!) {
      listEvaluationRuns(
        filter: { productID: { eq: $productId } }
        limit: $limit
        sortDirection: DESC
      ) {
        items {
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
    }
  `;

  const data = await gql(parsed, query, { productId: parsed.productId, limit });
  const runs = data?.data?.listEvaluationRuns?.items ?? [];

  console.log(`## Evaluation Run History${showAll ? " (all)" : " (last 10)"}\n`);

  if (runs.length === 0) {
    console.log("  (no runs found)");
    process.exit(0);
  }

  for (const run of runs) {
    const score = run.score != null ? `${(run.score * 100).toFixed(1)}%` : "N/A";
    const dur = run.duration != null ? `${run.duration.toFixed(1)}s` : "";
    const date = run.createdAt ? new Date(run.createdAt).toLocaleString() : "";
    const vuln = run.vulnerableCount != null ? `${run.vulnerableCount} vuln` : "";

    console.log(`- **${run.id}** — ${run.status}`);
    console.log(`  Score: ${score} | Tests: ${run.totalTests ?? "?"} | ${vuln} | ${dur}`);
    if (date) console.log(`  ${date}`);
    console.log();
  }
} catch (err) {
  console.error(`✖ ${formatError(err)}`);
  process.exit(1);
}
