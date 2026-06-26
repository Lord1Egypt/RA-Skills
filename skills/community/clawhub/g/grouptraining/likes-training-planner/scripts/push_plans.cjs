#!/usr/bin/env node
/**
 * Push training plans to Likes API
 * POST /api/open/plans/push
 * Supports single user or bulk push to training camp members
 * Usage: node push_plans.cjs <plans.json> [options]
 * 
 * Options:
 *   --key <api_key>     Use specific API key
 *   --game-id <id>      Training camp ID (for bulk push to camp members)
 *   --user-ids <ids>    Comma-separated user IDs for bulk push (e.g., "4,5,6")
 *   --overwrite         Overwrite existing plans (replace instead of duplicate)
 *   --dry-run           Preview without actually pushing
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

function getBaseUrl(config) {
  const url = config.baseUrl || 'https://my.likes.com.cn';
  return url.replace(/^https?:\/\//, '');
}

function pushPlans(apiKey, baseUrl, plansData, options = {}) {
  return new Promise((resolve, reject) => {
    // Build request body
    const requestBody = {
      plans: plansData.plans || plansData
    };
    
    // Add game_id and user_ids for bulk push
    if (options.game_id) {
      requestBody.game_id = parseInt(options.game_id);
    }
    
    if (options.user_ids && options.user_ids.length > 0) {
      requestBody.user_ids = options.user_ids;
    }
    
    // Add overwrite flag
    if (options.overwrite) {
      requestBody.overwrite = true;
    }
    
    const postData = JSON.stringify(requestBody);
    
    const requestOptions = {
      hostname: baseUrl,
      path: '/api/open/plans/push',
      method: 'POST',
      headers: {
        'X-API-Key': apiKey,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = https.request(requestOptions, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          
          // Handle specific error codes
          if (res.statusCode === 400) {
            if (result.message?.includes('game_id')) {
              reject(new Error('Bad request: game_id is required when pushing to multiple users'));
            } else if (result.message?.includes('user_ids')) {
              reject(new Error('Bad request: user_ids cannot be empty'));
            } else if (result.message?.includes('训练营不存在')) {
              reject(new Error('Bad request: Training camp does not exist'));
            } else if (result.message?.includes('非该训练营成员')) {
              reject(new Error('Bad request: Some user_ids are not members of this camp'));
            } else {
              reject(new Error(`Bad request: ${result.message || 'Invalid request'}`));
            }
            return;
          }
          
          if (res.statusCode === 403) {
            reject(new Error('Forbidden: Only camp creator or coach can bulk push'));
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
    
    req.write(postData);
    req.end();
  });
}

function showUsage() {
  console.log('Usage: node push_plans.cjs <plans.json> [options]');
  console.log('');
  console.log('Options:');
  console.log('  --key <api_key>     Use specific API key');
  console.log('  --game-id <id>      Training camp ID (for bulk push)');
  console.log('  --user-ids <ids>    Comma-separated user IDs (e.g., "4,5,6")');
  console.log('  --overwrite         Overwrite existing plans (replace instead of duplicate)');
  console.log('  --dry-run           Preview without pushing');
  console.log('  --help              Show this help');
  console.log('');
  console.log('Examples:');
  console.log('  # Push to yourself:');
  console.log('  node push_plans.cjs plans.json');
  console.log('');
  console.log('  # Push to specific camp member:');
  console.log('  node push_plans.cjs plans.json --user-ids 123');
  console.log('');
  console.log('  # Bulk push to multiple camp members:');
  console.log('  node push_plans.cjs plans.json --game-id 973 --user-ids "4,5,6"');
  console.log('');
  console.log('  # Overwrite existing plans (replace instead of duplicate):');
  console.log('  node push_plans.cjs plans.json --game-id 973 --user-ids "4,5,6" --overwrite');
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help')) {
    showUsage();
    process.exit(0);
  }
  
  let apiKey = null;
  let plansFile = null;
  const options = {
    game_id: null,
    user_ids: null,
    overwrite: false,
    dry_run: false
  };
  
  // Parse args
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--key' && i + 1 < args.length) {
      apiKey = args[i + 1];
      i++;
    } else if (args[i] === '--game-id' && i + 1 < args.length) {
      options.game_id = args[i + 1];
      i++;
    } else if (args[i] === '--user-ids' && i + 1 < args.length) {
      // Parse comma-separated user IDs
      options.user_ids = args[i + 1].split(',').map(id => parseInt(id.trim())).filter(id => !isNaN(id));
      i++;
    } else if (args[i] === '--overwrite') {
      options.overwrite = true;
    } else if (args[i] === '--dry-run') {
      options.dry_run = true;
    } else if (!plansFile && !args[i].startsWith('--')) {
      plansFile = args[i];
    }
  }
  
  if (!plansFile) {
    console.error('❌ Error: Please specify a plans.json file');
    showUsage();
    process.exit(1);
  }
  
  // Load configs
  const userConfig = loadUserConfig();
  const openclawConfig = loadOpenclawConfig();
  const baseUrl = getBaseUrl(userConfig);
  
  // Get API key (priority: arg > env > config)
  if (!apiKey) {
    apiKey = process.env.LIKES_API_KEY || openclawConfig.apiKey || userConfig.apiKey;
  }
  
  if (!apiKey) {
    console.error('❌ Error: No API key found');
    console.error('');
    console.error('Please configure the skill:');
    console.error('  OpenClaw Control UI → Skills → likes-training-planner → Configure');
    console.error('');
    console.error('Or provide via command line:');
    console.error('  node push_plans.cjs --key YOUR_KEY plans.json');
    process.exit(1);
  }
  
  if (!fs.existsSync(plansFile)) {
    console.error(`❌ Error: File not found: ${plansFile}`);
    process.exit(1);
  }

  let plansData;
  try {
    const content = fs.readFileSync(plansFile, 'utf8');
    plansData = JSON.parse(content);
  } catch (e) {
    console.error(`❌ Error: Failed to parse JSON: ${e.message}`);
    process.exit(1);
  }

  const plans = plansData.plans || plansData;
  
  if (!Array.isArray(plans)) {
    console.error('❌ Error: Invalid format. Expected { "plans": [...] } or array');
    process.exit(1);
  }
  
  if (plans.length === 0) {
    console.error('❌ Error: No plans to push');
    process.exit(1);
  }
  
  if (plans.length > 200) {
    console.error(`❌ Error: Too many plans (${plans.length}). Maximum is 200 per request.`);
    process.exit(1);
  }

  console.log(`📤 Preparing to push ${plans.length} plan(s)...`);
  
  // Show push mode
  if (options.game_id && options.user_ids) {
    console.log(`📋 Mode: Bulk push to training camp`);
    console.log(`   Camp ID: ${options.game_id}`);
    console.log(`   Users: ${options.user_ids.join(', ')}`);
  } else if (options.user_ids) {
    console.log(`📋 Mode: Push to specific user(s)`);
    console.log(`   Users: ${options.user_ids.join(', ')}`);
  } else {
    console.log(`📋 Mode: Push to yourself (current API key user)`);
  }
  
  if (options.overwrite) {
    console.log(`🔄 Overwrite: Enabled (will replace existing plans)`);
  }
  
  if (options.dry_run) {
    console.log('🔍 DRY RUN - Not actually pushing');
    console.log('');
    console.log('Plans preview:');
    plans.forEach((plan, i) => {
      console.log(`  ${i + 1}. ${plan.title} (${plan.start})`);
    });
    process.exit(0);
  }

  try {
    console.log('');
    console.log(`⏳ Pushing to Likes (${baseUrl})...`);
    
    const result = await pushPlans(apiKey, baseUrl, plansData, options);
    
    console.log('');
    console.log('════════════════════════════════════════════════════════════');
    console.log('✅ Push Results');
    console.log('════════════════════════════════════════════════════════════');
    console.log(`  Total: ${result.total}`);
    console.log(`  ✅ Parse OK: ${result.parse_ok}`);
    console.log(`  ❌ Parse Failed: ${result.parse_failed}`);
    console.log(`  ✅ Inserted: ${result.inserted}`);
    console.log(`  ❌ Insert Failed: ${result.insert_failed}`);
    console.log('');

    if (result.results && result.results.length > 0) {
      console.log('Details:');
      result.results.forEach((r, i) => {
        const status = r.status === 'ok' ? '✅' : 
                      r.status === 'parse_error' ? '⚠️ ' : '❌';
        console.log(`  ${status} [${i}] ${r.title} (${r.start}): ${r.status}`);
        if (r.message) {
          console.log(`      ${r.message}`);
        }
      });
    }
    console.log('════════════════════════════════════════════════════════════');

    const hasErrors = result.parse_failed > 0 || result.insert_failed > 0;
    process.exit(hasErrors ? 1 : 0);
    
  } catch (e) {
    console.error(`❌ Error: ${e.message}`);
    process.exit(1);
  }
}

main();
