#!/usr/bin/env node

import { Indexer, Searcher } from './index.js';

const args = process.argv.slice(2);

function parseArgs(args) {
  const options = { category: null, format: 'text', limit: 10 };
  const positional = [];

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--reindex') { options.reindex = true; }
    else if (arg === '--categories') { options.categories = true; }
    else if (arg === '--help') { options.help = true; }
    else if (arg === '--category' && args[i + 1] && !args[i + 1].startsWith('--')) {
      options.category = args[i + 1]; i++;
    } else if (arg === '--format' && args[i + 1] && !args[i + 1].startsWith('--')) {
      options.format = args[i + 1]; i++;
    } else if (arg === '--limit' && args[i + 1] && !args[i + 1].startsWith('--')) {
      options.limit = parseInt(args[i + 1]) || 10; i++;
    } else { positional.push(arg); }
  }

  return { options, query: positional.join(' ') };
}

async function main() {
  const indexer = new Indexer();
  const searcher = new Searcher();
  const { options, query } = parseArgs(args);

  if (options.reindex) {
    console.log('Building index...\n');
    await indexer.buildIndex();
    return;
  }

  if (options.categories) {
    const cats = await searcher.listCategories();
    console.log('Document categories:\n');
    for (const [cat, count] of Object.entries(cats)) {
      console.log(`  ${cat}: ${count} docs`);
    }
    return;
  }

  if (options.help || (!query && !options.reindex && !options.categories)) {
    console.log(`
OpenClaw Knowledge Search CLI

Usage:
  npm run search -- "query"          Search for documents
  npm run search -- --reindex        Rebuild the search index
  npm run search -- --categories     List all categories
  npm run search -- --help           Show this help

Options:
  --category <name>   Filter by category
  --format json      Output as JSON (for AI integration)
  --limit <n>        Limit results (default: 10)
    `);
    return;
  }

  try {
    const results = await searcher.search(query, options);
    console.log(results);
  } catch (err) {
    if (err.message.includes('Index not found')) {
      console.error('Index not found. Building index first...\n');
      await indexer.buildIndex();
      const results = await searcher.search(query, options);
      console.log(results);
    } else { throw err; }
  }
}

main().catch(console.error);
