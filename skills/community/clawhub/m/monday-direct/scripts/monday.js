#!/usr/bin/env node
/**
 * monday.js — CLI wrapper for the monday.com GraphQL API
 *
 * Usage:
 *   node monday.js query '<graphql>'
 *   node monday.js query '<graphql>' --variables '{"boardId": "123"}'
 *   node monday.js query '<graphql>' --version '2026-01'
 *
 * Reads API token from MONDAY_API_TOKEN env var.
 * Prints JSON result to stdout. Exits non-zero on error.
 */

'use strict';

const { ApiClient, ClientError } = require('@mondaydotcomorg/api');

function usage() {
  console.error('Usage: node monday.js query <graphql> [--variables <json>] [--version <yyyy-mm>]');
  process.exit(1);
}

function parseArgs(argv) {
  const args = argv.slice(2);
  if (args[0] !== 'query' || !args[1]) usage();

  const graphql = args[1];
  let variables = undefined;
  let version = undefined;

  for (let i = 2; i < args.length; i++) {
    if (args[i] === '--variables' && args[i + 1]) {
      try {
        variables = JSON.parse(args[++i]);
      } catch {
        console.error('Error: --variables must be valid JSON');
        process.exit(1);
      }
    } else if (args[i] === '--version' && args[i + 1]) {
      version = args[++i];
    }
  }

  return { graphql, variables, version };
}

async function main() {
  const token = process.env.MONDAY_API_TOKEN;
  if (!token) {
    console.error('Error: MONDAY_API_TOKEN environment variable is not set');
    process.exit(1);
  }

  const { graphql, variables, version } = parseArgs(process.argv);

  const clientConfig = { token };
  if (version) clientConfig.apiVersion = version;

  const client = new ApiClient(clientConfig);

  try {
    const data = await client.request(graphql, variables);
    console.log(JSON.stringify(data, null, 2));
  } catch (err) {
    if (err instanceof ClientError) {
      console.error(JSON.stringify({ error: err.message, graphqlErrors: err.response?.errors ?? [] }, null, 2));
    } else {
      console.error(JSON.stringify({ error: String(err) }, null, 2));
    }
    process.exit(1);
  }
}

main();
