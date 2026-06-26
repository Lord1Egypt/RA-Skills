#!/usr/bin/env node

/**
 * Telegram Handler for Power Search
 * Intercepts /search commands and sends formatted results back to chat
 */

const BraveSearch = require('./brave-search');
const Browserless = require('./browserless');

const BRAVE_API_KEY = process.env.BRAVE_API_KEY;
if (!BRAVE_API_KEY) {
  throw new Error('BRAVE_API_KEY environment variable not set. Get a free key at: https://api.search.brave.com/');
}
const BROWSERLESS_HOST = process.env.BROWSERLESS_HOST || 'http://localhost';
const BROWSERLESS_PORT = process.env.BROWSERLESS_PORT || '3000';

/**
 * Format search results for Telegram
 */
function formatResults(results, fetchMode = false) {
  let message = `🔍 *Search Results for "${results.query}"*\n\n`;
  
  results.results.forEach((result, idx) => {
    message += `*[${idx + 1}]* ${result.title}\n`;
    message += `🔗 ${result.url}\n`;
    if (result.description) {
      message += `${result.description.substring(0, 200)}...\n`;
    }
    message += '\n';
  });

  return message;
}

/**
 * Format fetched content for Telegram
 */
function formatFetchedContent(results) {
  let message = `📄 *Content from "${results.query}"*\n\n`;
  
  results.results.forEach((result, idx) => {
    message += `*[${idx + 1}]* ${result.title}\n`;
    message += `🔗 ${result.url}\n`;
    if (result.content) {
      const preview = result.content.substring(0, 300);
      message += `\`\`\`\n${preview}...\n\`\`\`\n`;
    }
    message += '\n';
  });

  return message;
}

/**
 * Main handler - called by OpenClaw when /search command received
 */
async function handleSearch(context) {
  try {
    // Parse command: /search query [--fetch] [--limit N]
    const match = context.message.text.match(/^\/search\s+(.+)$/);
    if (!match) {
      return { text: '❌ Usage: /search <query> [--fetch] [--limit N]' };
    }

    const args = match[1];
    const query = args.replace(/--fetch|--limit\s+\d+|--verbose/g, '').trim();
    const fetchMode = args.includes('--fetch');
    const limitMatch = args.match(/--limit\s+(\d+)/);
    const limit = limitMatch ? parseInt(limitMatch[1]) : 10;

    if (!query) {
      return { text: '❌ No search query provided' };
    }

    // Search
    const brave = new BraveSearch(BRAVE_API_KEY);
    const searchResults = await brave.search(query, limit);

    if (searchResults.results.length === 0) {
      return { text: `❌ No results found for "${query}"` };
    }

    let response = {
      text: formatResults(searchResults, fetchMode),
      parse_mode: 'Markdown',
    };

    // If fetch mode, get content from top results
    if (fetchMode && searchResults.results.length > 0) {
      const browserless = new Browserless(BROWSERLESS_HOST, BROWSERLESS_PORT);
      
      for (let i = 0; i < Math.min(searchResults.results.length, 3); i++) {
        try {
          const content = await browserless.fetchContent(searchResults.results[i].url);
          searchResults.results[i].content = content;
        } catch (error) {
          searchResults.results[i].content = `Error fetching: ${error.message}`;
        }
      }

      response.text = formatFetchedContent(searchResults);
    }

    return response;
  } catch (error) {
    return {
      text: `❌ Search failed: ${error.message}`,
    };
  }
}

/**
 * Export for OpenClaw integration
 */
module.exports = {
  handler: handleSearch,
  name: 'power-search',
  version: '2.0.0',
};

// CLI fallback for testing
if (require.main === module) {
  const testContext = {
    message: {
      text: process.argv.slice(2).join(' '),
    },
  };

  handleSearch(testContext).then((result) => {
    console.log(result.text);
  });
}
