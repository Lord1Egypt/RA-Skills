#!/usr/bin/env node
/**
 * Fetch training feedback from Likes API
 * GET /api/open/feedback
 * Returns user feedback for a date range (max 7 days)
 * Each feedback includes coach_comment: true/false indicating if coach has commented
 * Usage: node fetch_feedback.cjs [options]
 * 
 * Options:
 *   --start <date>    Start date, required (YYYY-MM-DD)
 *   --end <date>      End date, required (YYYY-MM-DD, max 7 days from start)
 *   --user-ids <ids>  Comma-separated user IDs (optional, for coaches to query multiple trainees, e.g., "4,5,6")
 *   --output <file>   Output file (default: stdout)
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

function fetchFeedback(apiKey, baseUrl, params) {
  return new Promise((resolve, reject) => {
    const queryParams = new URLSearchParams();
    queryParams.append('start', params.start);
    queryParams.append('end', params.end);
    if (params.user_ids) {
      queryParams.append('user_ids', params.user_ids);
    }
    
    const path = `/api/open/feedback?${queryParams.toString()}`;
    
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
            reject(new Error(`Bad request: ${result.message || 'Date range exceeds 30 days'}`));
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
    start: null,
    end: null,
    user_ids: null,
    output: null
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--start' && i + 1 < args.length) {
      options.start = args[i + 1];
      i++;
    } else if (args[i] === '--end' && i + 1 < args.length) {
      options.end = args[i + 1];
      i++;
    } else if (args[i] === '--user-ids' && i + 1 < args.length) {
      options.user_ids = args[i + 1];
      i++;
    } else if (args[i] === '--output' && i + 1 < args.length) {
      options.output = args[i + 1];
      i++;
    }
  }
  
  return options;
}

function showUsage() {
  console.log('Usage: node fetch_feedback.cjs --start <YYYY-MM-DD> --end <YYYY-MM-DD> [options]');
  console.log('');
  console.log('Required:');
  console.log('  --start <date>   Start date (YYYY-MM-DD)');
  console.log('  --end <date>     End date (YYYY-MM-DD), max 30 days from start');
  console.log('');
  console.log('Optional:');
  console.log('  --user-ids <ids>  Comma-separated user IDs (coach only, e.g., "4,5,6")');
  console.log('  --output <file>   Output file (default: stdout)');
  console.log('');
  console.log('Examples:');
  console.log('  node fetch_feedback.cjs --start 2026-03-01 --end 2026-03-07');
  console.log('  node fetch_feedback.cjs --start 2026-03-01 --end 2026-03-07 --user-ids 123');
  console.log('  node fetch_feedback.cjs --start 2026-03-01 --end 2026-03-07 --user-ids "4,5,6"');
}

async function main() {
  const options = parseArgs();
  
  if (!options.start || !options.end) {
    console.error('❌ Error: --start and --end are required');
    showUsage();
    process.exit(1);
  }
  
  // Validate date format and range
  const startDate = new Date(options.start);
  const endDate = new Date(options.end);
  
  if (isNaN(startDate.getTime()) || isNaN(endDate.getTime())) {
    console.error('❌ Error: Invalid date format. Use YYYY-MM-DD');
    process.exit(1);
  }
  
  const diffDays = (endDate - startDate) / (1000 * 60 * 60 * 24);
  if (diffDays > 7) {
    console.error('❌ Error: Date range exceeds 7 days (API limit)');
    process.exit(1);
  }
  
  if (diffDays < 0) {
    console.error('❌ Error: End date must be after start date');
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
  
  const params = {
    start: options.start,
    end: options.end
  };
  
  if (options.user_ids) {
    params.user_ids = options.user_ids;
  }
  
  try {
    console.error(`💬 Fetching feedback from ${options.start} to ${options.end}...`);
    if (options.user_ids) {
      console.error(`👤 User IDs: ${options.user_ids}`);
    }
    
    const result = await fetchFeedback(apiKey, baseUrl, params);
    
    const feedbacks = result.rows || [];
    const commentedCount = feedbacks.filter(f => f.coach_comment).length;
    const unCommentedCount = feedbacks.length - commentedCount;
    
    const output = {
      fetchedAt: new Date().toISOString(),
      period: {
        start: options.start,
        end: options.end
      },
      total: result.total || 0,
      coachCommented: commentedCount,
      needsComment: unCommentedCount,
      feedback: feedbacks
    };
    
    const jsonOutput = JSON.stringify(output, null, 2);
    
    if (options.output) {
      fs.writeFileSync(options.output, jsonOutput);
      console.error(`✅ Fetched ${result.total || 0} feedback entries`);
      console.error(`💬 Coach commented: ${commentedCount}`);
      console.error(`📝 Needs comment: ${unCommentedCount}`);
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
