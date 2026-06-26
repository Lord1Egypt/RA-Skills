#!/usr/bin/env node

const { program } = require('commander');
const BraveSearch = require('./brave-search');
const Browserless = require('./browserless');

// Get API key from environment or TOOLS.md
const BRAVE_API_KEY = process.env.BRAVE_API_KEY;
if (!BRAVE_API_KEY) {
  console.error('❌ Error: BRAVE_API_KEY environment variable not set');
  console.error('Set it: export BRAVE_API_KEY=your_key_here');
  console.error('Get a free key at: https://api.search.brave.com/');
  process.exit(1);
}
const BROWSERLESS_HOST = process.env.BROWSERLESS_HOST || 'http://localhost';
const BROWSERLESS_PORT = process.env.BROWSERLESS_PORT || '3000';

program
  .name('search')
  .description('Power Search: Brave Search API + Browserless content fetching')
  .version('2.0.0');

program
  .argument('<query>', 'search query')
  .option('--fetch', 'fetch full content from top results', false)
  .option('--limit <n>', 'number of results to return/fetch', '10')
  .option('--timeout <ms>', 'timeout in milliseconds', '10000')
  .option('--verbose', 'verbose logging', false)
  .action(async (query, options) => {
    try {
      const limit = parseInt(options.limit);
      const timeout = parseInt(options.timeout);
      const verbose = options.verbose;
      
      if (verbose) console.log(`🔍 Searching for: "${query}"`);
      
      const brave = new BraveSearch(BRAVE_API_KEY);
      const results = await brave.search(query, limit);
      
      console.log(`\n=== Search Results for "${query}" ===\n`);
      
      results.results.forEach((result) => {
        console.log(`[${result.rank}] ${result.title}`);
        console.log(`    ${result.url}`);
        if (result.description) {
          console.log(`    ${result.description.substring(0, 150)}...`);
        }
        console.log();
      });
      
      if (options.fetch && results.results.length > 0) {
        console.log('\n🌐 Fetching content from results...\n');
        
        const browserless = new Browserless(BROWSERLESS_HOST, BROWSERLESS_PORT);
        
        for (let i = 0; i < Math.min(results.results.length, limit); i++) {
          const result = results.results[i];
          try {
            if (verbose) console.log(`Fetching [${i + 1}/${Math.min(results.results.length, limit)}]...`);
            
            const content = await browserless.fetchContent(result.url, timeout);
            console.log(`[${i + 1}] ${result.title}`);
            console.log(`    URL: ${result.url}`);
            console.log(`    Content: ${content}`);
            console.log();
          } catch (error) {
            console.log(`[${i + 1}] ${result.title}`);
            console.log(`    Error: ${error.message}`);
            console.log();
          }
        }
      } else if (options.fetch) {
        console.log('⚠️  No results to fetch.');
      }
      
      if (verbose) console.log('✅ Search complete');
    } catch (error) {
      console.error(`❌ Error: ${error.message}`);
      process.exit(1);
    }
  });

program.parse(process.argv);
