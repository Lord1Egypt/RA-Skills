#!/usr/bin/env node
/**
 * Fetch activities from Likes API
 * Updated for new API: supports user_id, date range, pagination, sorting
 * Usage: node fetch_activities.cjs [options]
 * 
 * Options:
 *   --days <n>       Number of days to fetch (default: 30, max: 30 due to API limit)
 *   --start <date>   Start date (YYYY-MM-DD)
 *   --end <date>     End date (YYYY-MM-DD, max 30 days from start)
 *   --user-id <id>   User ID (optional, for coaches to query trainees)
 *   --page <n>       Page number (default: 1)
 *   --limit <n>      Items per page (default: 20, max: 2000)
 *   --order-by <field>  Sort field: sign_date, run_km, run_time, tss (default: sign_date)
 *   --order <asc|desc>  Sort order (default: desc)
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

function fetchActivities(apiKey, baseUrl, params) {
  return new Promise((resolve, reject) => {
    // Build query string
    const queryParams = new URLSearchParams();
    if (params.start_date) queryParams.append('start_date', params.start_date);
    if (params.end_date) queryParams.append('end_date', params.end_date);
    if (params.user_id) queryParams.append('user_id', params.user_id);
    if (params.page) queryParams.append('page', params.page);
    if (params.limit) queryParams.append('limit', params.limit);
    if (params.order_by) queryParams.append('order_by', params.order_by);
    if (params.order) queryParams.append('order', params.order);
    
    const queryString = queryParams.toString();
    const path = `/api/open/activity${queryString ? '?' + queryString : ''}`;
    
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
          if (res.statusCode === 429) {
            reject(new Error('Rate limit exceeded: max 1 request per minute'));
            return;
          }
          if (res.statusCode === 400) {
            reject(new Error(`Bad request: ${result.message || 'Date range exceeds 30 days'}`));
            return;
          }
          if (res.statusCode === 403) {
            reject(new Error('Forbidden: not authorized to query this user'));
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
    days: 7,  // Default to 7 days (safer for rate limits)
    start: null,
    end: null,
    user_id: null,
    page: 1,
    limit: 200,
    order_by: 'sign_date',
    order: 'desc',
    output: null
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--days' && i + 1 < args.length) {
      options.days = Math.min(parseInt(args[i + 1]), 30); // Max 30 days
      i++;
    } else if (args[i] === '--start' && i + 1 < args.length) {
      options.start = args[i + 1];
      i++;
    } else if (args[i] === '--end' && i + 1 < args.length) {
      options.end = args[i + 1];
      i++;
    } else if (args[i] === '--user-id' && i + 1 < args.length) {
      options.user_id = args[i + 1];
      i++;
    } else if (args[i] === '--page' && i + 1 < args.length) {
      options.page = parseInt(args[i + 1]);
      i++;
    } else if (args[i] === '--limit' && i + 1 < args.length) {
      options.limit = Math.min(parseInt(args[i + 1]), 2000); // Max 2000
      i++;
    } else if (args[i] === '--order-by' && i + 1 < args.length) {
      options.order_by = args[i + 1];
      i++;
    } else if (args[i] === '--order' && i + 1 < args.length) {
      options.order = args[i + 1];
      i++;
    } else if (args[i] === '--output' && i + 1 < args.length) {
      options.output = args[i + 1];
      i++;
    }
  }
  
  return options;
}

async function fetchAllActivities(apiKey, baseUrl, params) {
  const allActivities = [];
  let page = params.page;
  let hasMore = true;
  
  while (hasMore && page <= 10) { // Safety limit
    const pageParams = { ...params, page };
    const result = await fetchActivities(apiKey, baseUrl, pageParams);
    
    if (result.list && result.list.length > 0) {
      allActivities.push(...result.list);
    }
    
    hasMore = result.has_more || (result.list && result.list.length === params.limit);
    
    if (hasMore) {
      page++;
      // Rate limit: 1 request per minute for activity API
      if (hasMore) {
        console.error(`⏳ Rate limit: waiting 60 seconds before next page...`);
        await new Promise(resolve => setTimeout(resolve, 60000));
      }
    }
  }
  
  return {
    list: allActivities,
    total: allActivities.length,
    page: params.page,
    limit: params.limit,
    has_more: hasMore
  };
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
  
  let startDate, endDate;
  
  if (options.start && options.end) {
    startDate = options.start;
    endDate = options.end;
    
    // Validate 30 day limit
    const start = new Date(startDate);
    const end = new Date(endDate);
    const diffDays = (end - start) / (1000 * 60 * 60 * 24);
    if (diffDays > 30) {
      console.error('❌ Error: Date range exceeds 30 days (API limit)');
      process.exit(1);
    }
  } else {
    const now = new Date();
    const daysAgo = new Date(now);
    daysAgo.setDate(daysAgo.getDate() - options.days);
    endDate = now.toISOString().split('T')[0];
    startDate = daysAgo.toISOString().split('T')[0];
  }
  
  const params = {
    start_date: startDate,
    end_date: endDate,
    page: options.page,
    limit: options.limit,
    order_by: options.order_by,
    order: options.order
  };
  
  if (options.user_id) {
    params.user_id = options.user_id;
  }
  
  try {
    console.error(`📊 Fetching activities from ${startDate} to ${endDate}...`);
    console.error(`⚠️  Note: Activity API has rate limit of 1 request per minute`);
    
    const result = await fetchAllActivities(apiKey, baseUrl, params);
    
    const output = {
      fetchedAt: new Date().toISOString(),
      period: {
        start: startDate,
        end: endDate
      },
      count: result.list.length,
      total: result.total,
      page: result.page,
      has_more: result.has_more,
      activities: result.list
    };
    
    const jsonOutput = JSON.stringify(output, null, 2);
    
    if (options.output) {
      fs.writeFileSync(options.output, jsonOutput);
      console.error(`✅ Fetched ${result.list.length} activities`);
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
