#!/usr/bin/env node

/**
 * Know Your AI — Run an evaluation
 *
 * Usage: evaluate.mjs <evaluation-id> [--max-prompts <n>] [--timeout <seconds>] [--debug]
 * Requires: node (>=18), KNOW_YOUR_AI_DSN env var
 */

import { parseDsn, gql, requireDsn, formatError, sanitizeId } from "./lib/helpers.mjs";

function usage() {
  console.error('Usage: evaluate.mjs <evaluation-id> [--max-prompts <n>] [--timeout <seconds>] [--debug]');
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const evaluationId = args[0];
let maxPrompts = 3;
let timeoutSec = 600;
let debug = false;

for (let i = 1; i < args.length; i++) {
  const a = args[i];
  if (a === "--max-prompts") { maxPrompts = Number.parseInt(args[++i] ?? "3", 10); continue; }
  if (a === "--timeout") { timeoutSec = Number.parseInt(args[++i] ?? "600", 10); continue; }
  if (a === "--debug") { debug = true; continue; }
  console.error(`Unknown arg: ${a}`);
  usage();
}

const dsn = requireDsn();
const parsed = parseDsn(dsn);
const timeoutMs = timeoutSec * 1000;

// Sanitize user-supplied ID to prevent GraphQL injection
const safeEvaluationId = sanitizeId(evaluationId, "Evaluation ID");

if (debug) console.log(`[debug] evaluationId=${safeEvaluationId} maxPrompts=${maxPrompts} timeout=${timeoutSec}s`);

try {
  // 1. Get evaluation details
  const evalQuery = `
    query GetEvaluation($id: ID!) {
      getEvaluation(id: $id) {
        id
        name
        judgeModel
        threshold
        productID
      }
    }
  `;

  const evalData = await gql(parsed, evalQuery, { id: safeEvaluationId });
  const evaluation = evalData?.data?.getEvaluation;

  if (!evaluation) {
    console.error(`✖ Evaluation not found: ${safeEvaluationId}`);
    process.exit(1);
  }

  console.log("## Evaluation\n");
  console.log(`- **Name:** ${evaluation.name || "(unnamed)"}`);
  console.log(`- **Judge model:** ${evaluation.judgeModel || "N/A"}`);
  console.log(`- **Threshold:** ${evaluation.threshold ?? "N/A"}`);
  console.log();

  // 2. Create evaluation run
  console.log("Starting evaluation run...\n");

  const createRunMutation = `
    mutation CreateEvaluationRun($input: CreateEvaluationRunInput!) {
      createEvaluationRun(input: $input) {
        id
        status
      }
    }
  `;

  const runData = await gql(parsed, createRunMutation, {
    input: {
      evaluationID: safeEvaluationId,
      productID: parsed.productId,
      status: "PENDING",
      maxPrompts: maxPrompts,
    },
  });
  const run = runData?.data?.createEvaluationRun;

  if (!run?.id) {
    console.error("✖ Failed to create evaluation run.");
    if (debug) console.error(JSON.stringify(runData, null, 2));
    process.exit(1);
  }

  const runId = run.id;
  console.log(`Run ID: ${runId}`);
  console.log(`Status: ${run.status}\n`);

  // 3. Poll for results
  const startTime = Date.now();
  let finalRun = null;

  while (Date.now() - startTime < timeoutMs) {
    await sleep(3000);

    const pollQuery = `
      query GetEvaluationRun($id: ID!) {
        getEvaluationRun(id: $id) {
          id
          status
          score
          totalTests
          secureCount
          vulnerableCount
          duration
          completedAt
        }
      }
    `;

    const pollData = await gql(parsed, pollQuery, { id: runId });
    finalRun = pollData?.data?.getEvaluationRun;

    if (!finalRun) {
      console.error("✖ Lost track of evaluation run.");
      process.exit(1);
    }

    if (debug) {
      console.log(`[debug] status=${finalRun.status} score=${finalRun.score ?? "?"} total=${finalRun.totalTests ?? "?"}`);
    }

    const status = (finalRun.status ?? "").toUpperCase();
    if (status === "COMPLETED" || status === "FAILED" || status === "ERROR") {
      break;
    }

    // Simple progress indicator
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(0);
    process.stdout.write(`\r  polling... (${elapsed}s)`);
  }

  // Clear progress line
  process.stdout.write("\r" + " ".repeat(40) + "\r");

  if (!finalRun || (finalRun.status ?? "").toUpperCase() === "PENDING" || (finalRun.status ?? "").toUpperCase() === "RUNNING") {
    console.error(`✖ Evaluation timed out after ${timeoutSec}s.`);
    console.log(`  Run ID: ${runId} — check the dashboard for results.`);
    process.exit(1);
  }

  // 4. Print results
  console.log("## Results\n");
  console.log("─".repeat(50));
  console.log(`  Status:          ${finalRun.status}`);
  console.log(`  Total tests:     ${finalRun.totalTests ?? "N/A"}`);
  console.log(`  Secure:          ${finalRun.secureCount ?? "N/A"}`);
  console.log(`  Vulnerable:      ${finalRun.vulnerableCount ?? "N/A"}`);
  if (finalRun.score != null) {
    console.log(`  Score:           ${(finalRun.score * 100).toFixed(1)}%`);
  }
  if (finalRun.duration != null) {
    console.log(`  Duration:        ${finalRun.duration.toFixed(1)}s`);
  }
  console.log(`  Run ID:          ${runId}`);
  console.log("─".repeat(50));

  if (finalRun.vulnerableCount > 0) {
    console.log(`\n⚠ ${finalRun.vulnerableCount} out of ${finalRun.totalTests} tests found vulnerabilities.`);
  } else {
    console.log("\n✔ All tests passed — no vulnerabilities detected.");
  }

  console.log("ℹ Review detailed results in the Know Your AI dashboard.");
} catch (err) {
  console.error(`✖ ${formatError(err)}`);
  process.exit(1);
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}
