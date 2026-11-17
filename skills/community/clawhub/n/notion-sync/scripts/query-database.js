#!/usr/bin/env node
/**
 * Query Notion database with filters and sorting
 *
 * Usage: query-database.js <database-id> [--filter <json>] [--sort <json>] [--limit 10]
 */

const {
  checkApiKey,
  notionRequest,
  extractPropertyValue,
  stripTokenArg,
  parsePageSizeLimit,
  hasJsonFlag,
  hasHelpFlag,
  log,
} = require('./notion-utils.js');

checkApiKey();

async function queryDatabase(databaseId, filter = null, sorts = null, pageSize = 10) {
  log(`Fetching database info: ${databaseId}`);
  const dbInfo = await notionRequest(`/v1/databases/${databaseId}`, 'GET');

  // Use data_source_id if available (Notion API 2025-09-03)
  const dataSourceId = dbInfo.data_sources && dbInfo.data_sources.length > 0
    ? dbInfo.data_sources[0].id
    : databaseId;

  log(`Querying data source: ${dataSourceId}`);

  const payload = { page_size: pageSize };
  if (filter) {
    payload.filter = filter;
    log(`Filter: ${JSON.stringify(filter, null, 2)}`);
  }
  if (sorts) {
    payload.sorts = sorts;
    log(`Sort: ${JSON.stringify(sorts, null, 2)}`);
  }

  const result = await notionRequest(`/v1/data_sources/${dataSourceId}/query`, 'POST', payload);

  return result.results.map(page => {
    const properties = {};
    for (const [key, value] of Object.entries(page.properties)) {
      properties[key] = extractPropertyValue(value);
    }
    return {
      id: page.id,
      url: page.url,
      lastEdited: page.last_edited_time,
      properties
    };
  });
}

async function main() {
  const args = stripTokenArg(process.argv.slice(2));

  if (args.length === 0 || hasHelpFlag()) {
    console.log('Usage: query-database.js <database-id> [options]');
    console.log('');
    console.log('Options:');
    console.log('  --filter <json>  Filter expression (JSON)');
    console.log('  --sort <json>    Sort expression (JSON)');
    console.log('  --limit <num>    Maximum results (default: 10)');
    console.log('  --json           Output JSON only (suppress stderr logs)');
    console.log('');
    console.log('Examples:');
    console.log('  query-database.js <db-id>');
    console.log('  query-database.js <db-id> --filter \'{"property":"Status","select":{"equals":"Complete"}}\'');
    console.log('  query-database.js <db-id> --sort \'[{"property":"Date","direction":"descending"}]\'');
    process.exit(0);
  }

  try {
    const databaseId = args[0];
    let filter = null;
    let sorts = null;
    let limit = 10;

    for (let i = 1; i < args.length; i++) {
      if (args[i] === '--filter') {
        if (!args[i + 1]) throw new Error('--filter requires a JSON value');
        try {
          filter = JSON.parse(args[++i]);
        } catch (err) {
          throw new Error(`Invalid JSON for --filter: ${err.message}`);
        }
      } else if (args[i] === '--sort') {
        if (!args[i + 1]) throw new Error('--sort requires a JSON value');
        try {
          sorts = JSON.parse(args[++i]);
        } catch (err) {
          throw new Error(`Invalid JSON for --sort: ${err.message}`);
        }
      } else if (args[i] === '--limit') {
        limit = parsePageSizeLimit(args[++i]);
      } else if (args[i].startsWith('-')) {
        throw new Error(`Unknown option: ${args[i]}`);
      } else {
        throw new Error(`Unexpected argument: ${args[i]}`);
      }
    }

    const results = await queryDatabase(databaseId, filter, sorts, limit);
    console.log(JSON.stringify(results, null, 2));
    log(`\n✓ Found ${results.length} result(s)`);
  } catch (error) {
    if (hasJsonFlag()) {
      console.log(JSON.stringify({ error: error.message }, null, 2));
    } else {
      console.error('Error:', error.message);
    }
    process.exit(1);
  }
}

main();
