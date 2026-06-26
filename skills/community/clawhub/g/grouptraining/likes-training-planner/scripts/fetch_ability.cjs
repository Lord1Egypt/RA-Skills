#!/usr/bin/env node
/**
 * Fetch running ability from Likes API
 * GET /api/open/ability
 * Two modes: (1) By run force: get predicted times and pace zones. (2) By race times: get estimated run force.
 * Usage: node fetch_ability.cjs [options]
 *
 * Mode 1 (by run force):
 *   --runforce <0-99>   Ability value, e.g. 50 or 50.5 (required for mode 1)
 *   --celsius <0-40>    Optional. Temperature in Celsius, default 6
 *
 * Mode 2 (by race times, at least one required):
 *   --time-5km <sec|M:SS|H:MM:SS>
 *   --time-10km, --time-hm, --time-fm, --time-3km, --time-mile  Same format
 *
 * Options:
 *   --output <file>  Output file (default: stdout)
 *   --key <api_key>  Override API key
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

function fetchAbility(apiKey, baseUrl, params) {
  return new Promise((resolve, reject) => {
    const queryParams = new URLSearchParams();
    if (params.runforce != null) queryParams.append('runforce', String(params.runforce));
    if (params.celsius != null) queryParams.append('celsius', String(params.celsius));
    const timeKeys = ['time_5km', 'time_10km', 'time_hm', 'time_fm', 'time_3km', 'time_mile'];
    for (const key of timeKeys) {
      if (params[key] != null && String(params[key]).trim()) {
        queryParams.append(key, String(params[key]).trim());
      }
    }
    const queryString = queryParams.toString();
    const pathStr = `/api/open/ability${queryString ? '?' + queryString : ''}`;

    const options = {
      hostname: baseUrl,
      path: pathStr,
      method: 'GET',
      headers: {
        'X-API-Key': apiKey,
        'Accept': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (res.statusCode === 400) {
            reject(new Error(`Bad request: ${result.message || data}`));
            return;
          }
          if (res.statusCode === 503) {
            reject(new Error('Service unavailable: Run force / race model not ready'));
            return;
          }
          if (res.statusCode === 401) {
            reject(new Error('Unauthorized: Invalid API key'));
            return;
          }
          if (res.statusCode !== 200) {
            reject(new Error(`API error ${res.statusCode}: ${data}`));
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
    runforce: null,
    celsius: null,
    time_5km: null,
    time_10km: null,
    time_hm: null,
    time_fm: null,
    time_3km: null,
    time_mile: null,
    output: null,
    key: null
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const next = () => args[i + 1];
    if (arg === '--runforce' && next()) { options.runforce = next(); i++; }
    else if (arg === '--celsius' && next()) { options.celsius = next(); i++; }
    else if (arg === '--time-5km' && next()) { options.time_5km = next(); i++; }
    else if (arg === '--time-10km' && next()) { options.time_10km = next(); i++; }
    else if (arg === '--time-hm' && next()) { options.time_hm = next(); i++; }
    else if (arg === '--time-fm' && next()) { options.time_fm = next(); i++; }
    else if (arg === '--time-3km' && next()) { options.time_3km = next(); i++; }
    else if (arg === '--time-mile' && next()) { options.time_mile = next(); i++; }
    else if (arg === '--output' && next()) { options.output = next(); i++; }
    else if (arg === '--key' && next()) { options.key = next(); i++; }
  }

  return options;
}

function showUsage() {
  console.error('Usage: node fetch_ability.cjs [options]');
  console.error('');
  console.error('Mode 1 — by run force (get predicted times and pace zones):');
  console.error('  --runforce <0-99>   Ability value, e.g. 50 or 50.5 (required for mode 1)');
  console.error('  --celsius <0-40>   Optional. Temperature in Celsius, default 6');
  console.error('');
  console.error('Mode 2 — by race times (get estimated run force):');
  console.error('  At least one of: --time-5km, --time-10km, --time-hm, --time-fm, --time-3km, --time-mile');
  console.error('  Value format: seconds (e.g. 1948), or M:SS (e.g. 32:28), or H:MM:SS');
  console.error('');
  console.error('Optional:');
  console.error('  --output <file>   Output file (default: stdout)');
  console.error('  --key <api_key>   Override API key');
  console.error('');
  console.error('Examples:');
  console.error('  node fetch_ability.cjs --runforce 51');
  console.error('  node fetch_ability.cjs --runforce 50.5 --celsius 10 --output ability.json');
  console.error('  node fetch_ability.cjs --time-5km 32:28 --time-10km 1:07:20 --output ability.json');
}

async function main() {
  const options = parseArgs();

  const hasRunforce = options.runforce != null && String(options.runforce).trim() !== '';
  const timeKeys = ['time_5km', 'time_10km', 'time_hm', 'time_fm', 'time_3km', 'time_mile'];
  const hasAnyTime = timeKeys.some((k) => options[k] != null && String(options[k]).trim() !== '');

  if (!hasRunforce && !hasAnyTime) {
    console.error('❌ Error: Provide either --runforce (0–99) or at least one race time (--time-5km, --time-10km, etc.)');
    showUsage();
    process.exit(1);
  }

  const apiKey = options.key || getApiKey();
  if (!apiKey) {
    console.error('❌ Error: No API key found');
    console.error('Please configure the skill first:');
    console.error('  OpenClaw Control UI → Skills → likes-training-planner → Configure');
    process.exit(1);
  }

  const userConfig = loadUserConfig();
  const baseUrl = getBaseUrl(userConfig);

  const params = {};
  if (hasRunforce) params.runforce = options.runforce;
  if (options.celsius != null) params.celsius = options.celsius;
  for (const k of timeKeys) {
    if (options[k] != null && String(options[k]).trim()) params[k] = options[k].trim();
  }

  try {
    if (hasRunforce) {
      console.error(`🏃 Fetching running ability for runforce=${options.runforce}${options.celsius != null ? `, celsius=${options.celsius}` : ''}...`);
    } else {
      console.error('🏃 Fetching run force from race times...');
    }

    const result = await fetchAbility(apiKey, baseUrl, params);

    const output = {
      fetchedAt: new Date().toISOString(),
      ...result
    };

    const jsonOutput = JSON.stringify(output, null, 2);

    if (options.output) {
      fs.writeFileSync(options.output, jsonOutput);
      console.error('✅ Fetched running ability');
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
