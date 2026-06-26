#!/usr/bin/env node
/**
 * Fetch plans from Likes API
 * GET /api/open/plans
 * Returns plans for next 42 days from start date
 * Usage: node fetch_plans.cjs [options]
 * 
 * Options:
 *   --start <date>   Start date (YYYY-MM-DD), default: today
 *   --game-id <id>   Filter by game/training camp ID (optional)
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

function fetchPlans(apiKey, baseUrl, params) {
  return new Promise((resolve, reject) => {
    const queryParams = new URLSearchParams();
    if (params.start) queryParams.append('start', params.start);
    if (params.game_id) queryParams.append('game_id', params.game_id);
    
    const queryString = queryParams.toString();
    const path = `/api/open/plans${queryString ? '?' + queryString : ''}`;
    
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
    start: new Date().toISOString().split('T')[0], // Today
    game_id: null,
    output: null
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--start' && i + 1 < args.length) {
      options.start = args[i + 1];
      i++;
    } else if (args[i] === '--game-id' && i + 1 < args.length) {
      options.game_id = args[i + 1];
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
    start: options.start
  };
  
  if (options.game_id) {
    params.game_id = options.game_id;
  }
  
  try {
    console.error(`📅 Fetching plans from ${options.start} (next 42 days)...`);
    
    const result = await fetchPlans(apiKey, baseUrl, params);
    
    const output = {
      fetchedAt: new Date().toISOString(),
      period: {
        start: options.start,
        range: '42 days'
      },
      total: result.total || 0,
      plans: result.rows || []
    };
    
    const jsonOutput = JSON.stringify(output, null, 2);
    
    if (options.output) {
      fs.writeFileSync(options.output, jsonOutput);
      console.error(`✅ Fetched ${result.total || 0} plans`);
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
