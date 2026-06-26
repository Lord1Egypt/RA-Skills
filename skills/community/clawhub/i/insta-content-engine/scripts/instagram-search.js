#!/usr/bin/env node
/**
 * Instagram Search via Brave Search API
 * Searches site:instagram.com for posts, profiles, and reels
 * No Instagram API or paid keys needed — uses Brave Search
 */

const https = require('https');

// Parse args
const args = process.argv.slice(2);
let query = '';
let limit = 10;
let type = 'all'; // posts, profiles, reels, all

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--limit' && args[i + 1]) {
    limit = parseInt(args[i + 1], 10);
    i++;
  } else if (args[i] === '--type' && args[i + 1]) {
    type = args[i + 1];
    i++;
  } else if (!args[i].startsWith('--')) {
    query += (query ? ' ' : '') + args[i];
  }
}

if (!query) {
  console.error('Usage: instagram-search.js "query" [--limit N] [--type posts|profiles|reels|all]');
  process.exit(1);
}

// Build site-scoped query
let siteQuery;
switch (type) {
  case 'profiles':
    siteQuery = `site:instagram.com inurl:/ -inurl:/p/ -inurl:/reel/ ${query}`;
    break;
  case 'reels':
    siteQuery = `site:instagram.com inurl:/reel/ ${query}`;
    break;
  case 'posts':
    siteQuery = `site:instagram.com inurl:/p/ ${query}`;
    break;
  default:
    siteQuery = `site:instagram.com ${query}`;
}

// Find API key from env or OpenClaw config
function getApiKey() {
  if (process.env.BRAVE_API_KEY) return process.env.BRAVE_API_KEY;
  
  // Try reading from OpenClaw config
  try {
    const fs = require('fs');
    const path = require('path');
    const home = process.env.HOME || process.env.USERPROFILE;
    const configPath = path.join(home, '.openclaw', 'clawdbot.json');
    if (fs.existsSync(configPath)) {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      const key = config?.tools?.web?.search?.apiKey;
      if (key) return key;
    }
  } catch (e) {}
  
  return null;
}

const apiKey = getApiKey();
if (!apiKey) {
  console.error('❌ No Brave API key found.');
  console.error('   Set BRAVE_API_KEY env var or configure tools.web.search.apiKey in OpenClaw.');
  process.exit(1);
}

// Brave Search API call
const params = new URLSearchParams({
  q: siteQuery,
  count: Math.min(limit, 20).toString(),
});

const options = {
  hostname: 'api.search.brave.com',
  path: `/res/v1/web/search?${params}`,
  method: 'GET',
  headers: {
    'Accept': 'application/json',
    'Accept-Encoding': 'identity',
    'X-Subscription-Token': apiKey,
  },
};

console.log(`🔍 Searching Instagram: "${query}" (type: ${type})\n`);

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    if (res.statusCode !== 200) {
      console.error(`❌ Brave API error: ${res.statusCode}`);
      console.error(data);
      process.exit(1);
    }

    try {
      const json = JSON.parse(data);
      const results = json.web?.results || [];

      if (results.length === 0) {
        console.log('No results found.');
        return;
      }

      let count = 0;
      for (const r of results) {
        count++;
        const url = r.url || '';
        
        // Determine type
        let resultType = '📄';
        if (url.includes('/reel/')) resultType = '🎬 Reel';
        else if (url.includes('/p/')) resultType = '📸 Post';
        else if (url.match(/instagram\.com\/[^\/]+\/?$/)) resultType = '👤 Profile';
        else resultType = '📄 Page';

        // Extract username from URL
        const usernameMatch = url.match(/instagram\.com\/([^\/\?]+)/);
        const username = usernameMatch ? `@${usernameMatch[1]}` : '';

        console.log(`${count}. ${resultType} ${username ? `(${username})` : ''}`);
        console.log(`   ${r.title || 'No title'}`);
        if (r.description) {
          console.log(`   ${r.description.substring(0, 200)}`);
        }
        console.log(`   🔗 ${url}`);
        console.log();
      }

      console.log(`---\n${count} results found for "${query}" on Instagram`);
    } catch (e) {
      console.error('❌ Failed to parse response:', e.message);
    }
  });
});

req.on('error', (e) => {
  console.error('❌ Request failed:', e.message);
  process.exit(1);
});

req.end();
