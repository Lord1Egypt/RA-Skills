#!/usr/bin/env node
/**
 * Fetch training camps/games list from Likes API
 * GET /api/open/games
 * Returns camps where you are creator or coach
 * Usage: node fetch_games.cjs [options]
 * 
 * Options:
 *   --page <n>       Page number (default: 1)
 *   --limit <n>      Items per page (default: 10, max: 10)
 *   --output <file>  Output file (default: stdout)
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const USER_CONFIG_FILE = path.join(require('os').homedir(), '.openclaw', 'likes-training-planner.json');
const OPENCLAW_CONFIG_FILE = path.join(require('os').homedir(), '.openclaw', 'openclaw.json');

function loadUserConfig() {
  if (fs.existsSync(USER_CONFIG_FILE)) {
    try {
      return JSON.parse(fs.readFileSync(USER_CONFIG_FILE, 'utf8'));
    } catch (e) {
      return {};
    }
  }
  return {};
}

function loadOpenclawConfig() {
  if (fs.existsSync(OPENCLAW_CONFIG_FILE)) {
    try {
      const config = JSON.parse(fs.readFileSync(OPENCLAW_CONFIG_FILE, 'utf8'));
      if (config.skills?.entries?.['likes-training-planner']) {
        return config.skills.entries['likes-training-planner'];
      }
    } catch (e) {
      return {};
    }
  }
  return {};
}

function getApiKey() {
  const userConfig = loadUserConfig();
  const openclawConfig = loadOpenclawConfig();
  return process.env.LIKES_API_KEY || openclawConfig.apiKey || userConfig.apiKey;
}

function getBaseUrl(config) {
  const url = config.baseUrl || 'https://my.likes.com.cn';
  return url.replace(/^https?:\/\//, '');
}

function fetchGames(apiKey, baseUrl, params) {
  return new Promise((resolve, reject) => {
    const queryParams = new URLSearchParams();
    if (params.page) queryParams.append('page', params.page);
    if (params.limit) queryParams.append('limit', params.limit);
    
    const path = `/api/open/games?${queryParams.toString()}`;
    
    const options = {
      hostname: baseUrl,
      path: path,
      method: 'GET',
      headers: {
        'X-API-Key': apiKey,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (res.statusCode === 401) {
            reject(new Error('Unauthorized: Invalid API key'));
            return;
          }
          resolve(result);
        } catch (e) {
          reject(new Error(`Failed to parse response: ${e.message}`));
        }
      });
    });

    req.on('error', (e) => reject(e));
    req.setTimeout(30000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
    req.end();
  });
}

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    page: 1,
    limit: 10, // Max 10 per API
    output: null
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--page' && i + 1 < args.length) {
      options.page = parseInt(args[i + 1]);
      i++;
    } else if (args[i] === '--limit' && i + 1 < args.length) {
      options.limit = Math.min(parseInt(args[i + 1]), 10); // Max 10
      i++;
    } else if (args[i] === '--output' && i + 1 < args.length) {
      options.output = args[i + 1];
      i++;
    }
  }
  
  return options;
}

async function main() {
  const options = parseArgs();
  const apiKey = getApiKey();
  
  if (!apiKey) {
    console.error('❌ Error: No API key found');
    console.error('Please configure the skill first:');
    console.error('  OpenClaw Control UI → Skills → likes-training-planner → Configure');
    process.exit(1);
  }
  
  const userConfig = loadUserConfig();
  const baseUrl = getBaseUrl(userConfig);
  
  const params = {
    page: options.page,
    limit: options.limit
  };
  
  try {
    console.error(`🏃 Fetching your training camps (page ${options.page})...`);
    console.error(`⚠️  Note: Only shows camps where you are creator or coach`);
    
    const result = await fetchGames(apiKey, baseUrl, params);
    
    const output = {
      fetchedAt: new Date().toISOString(),
      total: result.total || 0,
      page: result.page || options.page,
      limit: result.limit || options.limit,
      camps: result.rows || []
    };
    
    const jsonOutput = JSON.stringify(output, null, 2);
    
    if (options.output) {
      fs.writeFileSync(options.output, jsonOutput);
      console.error(`✅ Fetched ${result.rows?.length || 0} camps`);
      console.error(`📊 Total: ${result.total || 0}`);
      console.error(`📁 Saved to: ${options.output}`);
    } else {
      console.log(jsonOutput);
    }
    
  } catch (e) {
    console.error(`❌ Error: ${e.message}`);
    process.exit(1);
  }
}

main();
