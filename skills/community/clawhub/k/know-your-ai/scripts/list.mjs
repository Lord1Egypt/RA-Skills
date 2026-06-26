#!/usr/bin/env node

/**
 * Know Your AI — List evaluations and datasets
 *
 * Requires: node (>=18), KNOW_YOUR_AI_DSN env var
 */

import { parseDsn, gql, requireDsn, formatError } from "./lib/helpers.mjs";

const dsn = requireDsn();
const parsed = parseDsn(dsn);

try {
  // Fetch evaluations
  const evalQuery = `
    query ListEvaluations($productId: String!) {
      listEvaluations(filter: { productID: { eq: $productId } }, limit: 50) {
        items {
          id
          name
          judgeModel
          threshold
          createdAt
        }
      }
    }
  `;

  const evalData = await gql(parsed, evalQuery, { productId: parsed.productId });
  const evaluations = evalData?.data?.listEvaluations?.items ?? [];

  console.log("## Evaluations\n");
  if (evaluations.length === 0) {
    console.log("  (none found)\n");
  } else {
    for (const ev of evaluations) {
      const threshold = ev.threshold != null ? ` | threshold: ${ev.threshold}` : "";
      const judge = ev.judgeModel ? ` | judge: ${ev.judgeModel}` : "";
      console.log(`- **${ev.name || "(unnamed)"}**`);
      console.log(`  ID: ${ev.id}${judge}${threshold}`);
    }
  }

  // Fetch datasets
  const dsQuery = `
    query ListDatasets($productId: String!) {
      listDatasets(filter: { productID: { eq: $productId } }, limit: 50) {
        items {
          id
          name
          promptCount
          createdAt
        }
      }
    }
  `;

  const dsData = await gql(parsed, dsQuery, { productId: parsed.productId });
  const datasets = dsData?.data?.listDatasets?.items ?? [];

  console.log("\n## Datasets\n");
  if (datasets.length === 0) {
    console.log("  (none found)");
  } else {
    for (const ds of datasets) {
      const count = ds.promptCount != null ? ` | ${ds.promptCount} prompts` : "";
      console.log(`- **${ds.name || "(unnamed)"}**`);
      console.log(`  ID: ${ds.id}${count}`);
    }
  }
} catch (err) {
  console.error(`✖ ${formatError(err)}`);
  process.exit(1);
}
