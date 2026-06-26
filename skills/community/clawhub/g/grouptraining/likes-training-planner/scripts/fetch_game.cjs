#!/usr/bin/env node
/**
 * Fetch training camp/game details from Likes API
 * GET /api/open/game?game_id=<id>
 * Returns camp details and member list
 * Usage: node fetch_game.cjs --game-id <id> [options]
 * 
 * Options:
 *   --game-id <id>   Training camp/game ID (required)
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

function fetchGame(apiKey, baseUrl, gameId) {
  return new Promise((resolve, reject) => {
    const path = `/api/open/game?game_id=${gameId}`;
    
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
          if (res.statusCode === 400) {
            reject(new Error(`Bad request: Invalid game_id`));
            return;
          }
          if (res.statusCode === 403) {
            reject(new Error('Forbidden: You are not the creator or coach of this training camp'));
            return;
          }
          if (res.statusCode === 404) {
            reject(new Error('Not found: Training camp does not exist'));
            return;
          }
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
    game_id: null,
    output: null
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--game-id' && i + 1 < args.length) {
      options.game_id = args[i + 1];
      i++;
    } else if (args[i] === '--output' && i + 1 < args.length) {
      options.output = args[i + 1];
      i++;
    }
  }
  
  return options;
}

function showUsage() {
  console.log('Usage: node fetch_game.cjs --game-id <id> [options]');
  console.log('');
  console.log('Required:');
  console.log('  --game-id <id>   Training camp/game ID');
  console.log('');
  console.log('Optional:');
  console.log('  --output <file>  Output file (default: stdout)');
  console.log('');
  console.log('Example:');
  console.log('  node fetch_game.cjs --game-id 973');
}

async function main() {
  const options = parseArgs();
  
  if (!options.game_id) {
    console.error('❌ Error: --game-id is required');
    showUsage();
    process.exit(1);
  }
  
  const apiKey = getApiKey();
  
  if (!apiKey) {
    console.error('❌ Error: No API key found');
    console.error('Please configure the skill first:');
    console.error('  OpenClaw Control UI → Skills → likes-training-planner → Configure');
    process.exit(1);
  }
  
  const userConfig = loadUserConfig();
  const baseUrl = getBaseUrl(userConfig);
  
  try {
    console.error(`🏃 Fetching training camp details for game_id=${options.game_id}...`);
    console.error(`⚠️  Note: You must be the creator or coach of this camp`);
    
    const result = await fetchGame(apiKey, baseUrl, options.game_id);
    
    const output = {
      fetchedAt: new Date().toISOString(),
      game_id: options.game_id,
      game: result.game || null,
      total_members: result.total || 0,
      members: result.rows || []
    };
    
    const jsonOutput = JSON.stringify(output, null, 2);
    
    if (options.output) {
      fs.writeFileSync(options.output, jsonOutput);
      console.error(`✅ Fetched camp details`);
      console.error(`📊 Total members: ${result.total || 0}`);
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
