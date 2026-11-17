#!/usr/bin/env node
/**
 * Search Notion workspace for pages and databases
 *
 * Usage: search-notion.js <query> [--filter page|database] [--limit 10]
 */

const {
  checkApiKey,
  notionRequest,
  extractTitle,
  stripTokenArg,
  parsePageSizeLimit,
  hasJsonFlag,
  hasHelpFlag,
  log,
} = require('./notion-utils.js');

checkApiKey();

async function searchNotion(query, filter = null, pageSize = 10) {
  const payload = { query, page_size: pageSize };

  if (filter) {
    payload.filter = { property: 'object', value: filter };
  }

  log(`Searching for: "${query}"${filter ? ` (filter: ${filter})` : ''}`);

  const result = await notionRequest('/v1/search', 'POST', payload);

  return result.results.map(item => ({
    id: item.id,
    object: item.object,
    title: extractTitle(item),
    url: item.url,
    lastEdited: item.last_edited_time,
    parent: item.parent
  }));
}

async function main() {
  const args = stripTokenArg(process.argv.slice(2));

  if (args.length === 0 || hasHelpFlag()) {
    console.log('Usage: search-notion.js <query> [options]');
    console.log('');
    console.log('Options:');
    console.log('  --filter <page|database>  Filter by object type');
    console.log('  --limit <number>          Maximum results (default: 10)');
    console.log('  --json                    Output JSON only (suppress stderr logs)');
    console.log('');
    console.log('Examples:');
    console.log('  search-notion.js "newsletter"');
    console.log('  search-notion.js "research" --filter page');
    console.log('  search-notion.js "AI" --limit 20');
    process.exit(0);
  }

  const query = args[0];
  let filter = null;
  let limit = 10;

  try {
    for (let i = 1; i < args.length; i++) {
      if (args[i] === '--filter') {
        if (!args[i + 1]) throw new Error('--filter requires page or database');
        filter = args[++i];
        if (!['page', 'database'].includes(filter)) {
          throw new Error('--filter must be page or database');
        }
      } else if (args[i] === '--limit') {
        limit = parsePageSizeLimit(args[++i]);
      } else if (args[i].startsWith('-')) {
        throw new Error(`Unknown option: ${args[i]}`);
      } else {
        throw new Error(`Unexpected argument: ${args[i]}`);
      }
    }

    const results = await searchNotion(query, filter, limit);
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
