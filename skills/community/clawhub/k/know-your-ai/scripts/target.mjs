#!/usr/bin/env node

/**
 * Know Your AI — Target
 * Show linked product, model & connection info.
 *
 * Requires: node (>=18), KNOW_YOUR_AI_DSN env var
 */

import { parseDsn, gql, requireDsn, formatError } from "./lib/helpers.mjs";

const dsn = requireDsn();
const parsed = parseDsn(dsn);

const query = `
  query GetProduct($id: ID!) {
    getProduct(id: $id) {
      id
      name
      description
      modelEndpoint
      createdAt
      updatedAt
    }
  }
`;

try {
  const data = await gql(parsed, query, { id: parsed.productId });
  const product = data?.data?.getProduct;

  if (!product) {
    console.error("✖ Product not found for ID:", parsed.productId);
    process.exit(1);
  }

  console.log("## Target Product\n");
  console.log(`- **Name:** ${product.name || "(unnamed)"}`);
  console.log(`- **ID:** ${product.id}`);
  if (product.description) console.log(`- **Description:** ${product.description}`);
  if (product.modelEndpoint) console.log(`- **Model Endpoint:** ${product.modelEndpoint}`);
  console.log(`- **Host:** ${parsed.host}`);
  console.log(`- **Created:** ${product.createdAt || "N/A"}`);
} catch (err) {
  console.error(`✖ ${formatError(err)}`);
  process.exit(1);
}
