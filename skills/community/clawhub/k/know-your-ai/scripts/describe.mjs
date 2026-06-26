#!/usr/bin/env node

/**
 * Know Your AI — Describe
 * Show detailed evaluation configuration.
 *
 * Usage: describe.mjs <evaluation-id>
 * Requires: node (>=18), KNOW_YOUR_AI_DSN env var
 */

import { parseDsn, gql, requireDsn, formatError, sanitizeId } from "./lib/helpers.mjs";

function usage() {
  console.error('Usage: describe.mjs <evaluation-id>');
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const evaluationId = sanitizeId(args[0], "Evaluation ID");

const dsn = requireDsn();
const parsed = parseDsn(dsn);

try {
  const query = `
    query GetEvaluation($id: ID!) {
      getEvaluation(id: $id) {
        id
        name
        description
        judgeModel
        threshold
        productID
        createdAt
        updatedAt
        datasets {
          items {
            id
            name
            promptCount
          }
        }
      }
    }
  `;

  const data = await gql(parsed, query, { id: evaluationId });
  const ev = data?.data?.getEvaluation;

  if (!ev) {
    console.error(`✖ Evaluation not found: ${evaluationId}`);
    process.exit(1);
  }

  console.log("## Evaluation Details\n");
  console.log(`- **Name:** ${ev.name || "(unnamed)"}`);
  console.log(`- **ID:** ${ev.id}`);
  if (ev.description) console.log(`- **Description:** ${ev.description}`);
  console.log(`- **Judge Model:** ${ev.judgeModel || "N/A"}`);
  console.log(`- **Threshold:** ${ev.threshold ?? "N/A"}`);
  console.log(`- **Product ID:** ${ev.productID || "N/A"}`);
  if (ev.createdAt) console.log(`- **Created:** ${new Date(ev.createdAt).toLocaleString()}`);
  if (ev.updatedAt) console.log(`- **Updated:** ${new Date(ev.updatedAt).toLocaleString()}`);

  const datasets = ev.datasets?.items ?? [];
  if (datasets.length > 0) {
    console.log(`\n### Linked Datasets (${datasets.length})\n`);
    for (const ds of datasets) {
      const count = ds.promptCount != null ? ` — ${ds.promptCount} prompts` : "";
      console.log(`- **${ds.name || "(unnamed)"}** (${ds.id})${count}`);
    }
  }
} catch (err) {
  console.error(`✖ ${formatError(err)}`);
  process.exit(1);
}
