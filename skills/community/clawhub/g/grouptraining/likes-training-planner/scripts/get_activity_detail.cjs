#!/usr/bin/env node
/**
 * Get activity detail from Likes API
 * GET /api/open/activity/detail
 * Returns raw JSON detail for one activity by ID
 * Supports overview (record=null) or full detailed (including GPS)
 * Usage: node get_activity_detail.cjs --id <activity_id> [--mode <overview|detailed>]
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

function getActivityDetail(apiKey, baseUrl, id, mode) {
  return new Promise((resolve, reject) => {
    const queryParams = new URLSearchParams();
    queryParams.append('id', id);
    queryParams.append('mode', mode);
    
    const path = `/api/open/activity/detail?${queryParams.toString()}`;
    
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
            reject(new Error(`Bad request: ${result.message || 'Invalid activity ID'}`));
            return;
          }
          if (res.statusCode === 401) {
            reject(new Error('Unauthorized: Invalid API key'));
            return;
          }
          if (res.statusCode === 403) {
            reject(new Error('Forbidden: Not authorized to access this activity'));
            return;
          }
          if (res.statusCode === 404) {
            reject(new Error('Not found: Activity does not exist'));
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
    id: null,
    mode: 'overview', // default: overview
    output: null
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--id' && i + 1 < args.length) {
      options.id = parseInt(args[i + 1]);
      i++;
    } else if (args[i] === '--mode' && i + 1 < args.length) {
      options.mode = args[i + 1];
      i++;
    } else if (args[i] === '--output' && i + 1 < args.length) {
      options.output = args[i + 1];
      i++;
    }
  }
  
  return options;
}

function showUsage() {
  console.log('Usage: node get_activity_detail.cjs --id <activity_id> [options]');
  console.log('');
  console.log('Required:');
  console.log('  --id <activity_id>   Activity ID (from list_activities)');
  console.log('');
  console.log('Optional:');
  console.log('  --mode <mode>        overview (default) or detailed (includes GPS)');
  console.log('  --output <file>      Output file (default: stdout)');
  console.log('');
  console.log('Examples:');
  console.log('  node get_activity_detail.cjs --id 12345');
  console.log('  node get_activity_detail.cjs --id 12345 --mode detailed');
  console.log('  node get_activity_detail.cjs --id 12345 --mode detailed --output activity.json');
}

async function main() {
  const options = parseArgs();
  
  if (!options.id || options.id <= 0) {
    console.error('❌ Error: --id is required (positive integer)');
    showUsage();
    process.exit(1);
  }
  
  if (!['overview', 'detailed'].includes(options.mode)) {
    console.error('❌ Error: --mode must be "overview" or "detailed"');
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
    console.error(`📊 Fetching activity detail...`);
    console.error(`   Activity ID: ${options.id}`);
    console.error(`   Mode: ${options.mode}`);
    if (options.mode === 'detailed') {
      console.error(`   ⚠️  Detailed mode may include GPS data (larger response)`);
    }
    console.error('');
    
    const result = await getActivityDetail(apiKey, baseUrl, options.id, options.mode);
    
    const jsonOutput = JSON.stringify(result, null, 2);
    
    if (options.output) {
      fs.writeFileSync(options.output, jsonOutput);
      console.error(`✅ Activity detail saved`);
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
