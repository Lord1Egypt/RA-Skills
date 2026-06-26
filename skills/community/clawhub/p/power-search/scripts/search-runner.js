#!/usr/bin/env node

/**
 * Power Search - Direct command execution
 * Run via: node search-runner.js "query" [--fetch] [--limit N]
 */

const BraveSearch = require('./brave-search');
const Browserless = require('./browserless');

const BRAVE_API_KEY = process.env.BRAVE_API_KEY;
if (!BRAVE_API_KEY) {
  console.error(JSON.stringify({
    success: false,
    error: 'BRAVE_API_KEY environment variable not set',
    hint: 'Set it: export BRAVE_API_KEY=your_key_here',
    help: 'Get a free key at: https://api.search.brave.com/',
  }));
  process.exit(1);
}
const BROWSERLESS_HOST = process.env.BROWSERLESS_HOST || 'http://localhost';
const BROWSERLESS_PORT = process.env.BROWSERLESS_PORT || '3000';

async function main() {
  try {
    const args = process.argv.slice(2);
    if (args.length === 0) {
      console.error('Usage: search-runner.js "query" [--fetch] [--limit N]');
      process.exit(1);
    }

    const query = args[0];
    const fetchMode = args.includes('--fetch');
    const limitMatch = args.join(' ').match(/--limit\s+(\d+)/);
    const limit = limitMatch ? parseInt(limitMatch[1]) : 10;

    // Search
    const brave = new BraveSearch(BRAVE_API_KEY);
    const searchResults = await brave.search(query, limit);

    // Output as JSON for easy parsing by agent
    const output = {
      success: true,
      query,
      count: searchResults.results.length,
      results: searchResults.results,
    };

    // If fetch mode, get content
    if (fetchMode) {
      const browserless = new Browserless(BROWSERLESS_HOST, BROWSERLESS_PORT);
      
      for (let i = 0; i < Math.min(searchResults.results.length, 3); i++) {
        try {
          const content = await browserless.fetchContent(searchResults.results[i].url);
          output.results[i].content = content;
        } catch (error) {
          output.results[i].content = null;
          output.results[i].fetchError = error.message;
        }
      }
      output.fetched = true;
    }

    console.log(JSON.stringify(output, null, 2));
  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message,
    }));
    process.exit(1);
  }
}

main();
