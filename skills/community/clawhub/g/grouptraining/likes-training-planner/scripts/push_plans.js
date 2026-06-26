#!/usr/bin/env node
/**
 * Push training plans to Likes API
 * Usage: node push_plans.js <api_key> <plans.json>
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'my.likes.com.cn';

function pushPlans(apiKey, plansData) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(plansData);
    
    const options = {
      hostname: BASE_URL,
      path: '/api/open/plans/push',
      method: 'POST',
      headers: {
        'X-API-Key': apiKey,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
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

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.error('Usage: node push_plans.js <api_key> <plans.json>');
    console.error('  or:  node push_plans.js --env <plans.json>  (reads API_KEY from env)');
    process.exit(1);
  }

  let apiKey, plansFile;
  
  if (args[0] === '--env') {
    apiKey = process.env.LIKES_API_KEY;
    if (!apiKey) {
      console.error('Error: LIKES_API_KEY environment variable not set');
      process.exit(1);
    }
    plansFile = args[1];
  } else {
    apiKey = args[0];
    plansFile = args[1];
  }

  if (!fs.existsSync(plansFile)) {
    console.error(`Error: File not found: ${plansFile}`);
    process.exit(1);
  }

  let plansData;
  try {
    const content = fs.readFileSync(plansFile, 'utf8');
    plansData = JSON.parse(content);
  } catch (e) {
    console.error(`Error: Failed to parse JSON: ${e.message}`);
    process.exit(1);
  }

  if (!plansData.plans || !Array.isArray(plansData.plans)) {
    console.error('Error: Invalid format. Expected { "plans": [...] }');
    process.exit(1);
  }

  console.log(`Pushing ${plansData.plans.length} plan(s) to Likes...`);
  console.log('');

  try {
    const result = await pushPlans(apiKey, plansData);
    
    console.log('Result:');
    console.log(`  Total: ${result.total}`);
    console.log(`  Parse OK: ${result.parse_ok}`);
    console.log(`  Parse Failed: ${result.parse_failed}`);
    console.log(`  Inserted: ${result.inserted}`);
    console.log(`  Insert Failed: ${result.insert_failed}`);
    console.log('');

    if (result.results && result.results.length > 0) {
      console.log('Details:');
      result.results.forEach((r, i) => {
        const status = r.status === 'ok' ? '✓' : '✗';
        console.log(`  ${status} [${i}] ${r.title} (${r.start}): ${r.status}`);
        if (r.message) {
          console.log(`      ${r.message}`);
        }
      });
    }

    const hasErrors = result.parse_failed > 0 || result.insert_failed > 0;
    process.exit(hasErrors ? 1 : 0);
    
  } catch (e) {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  }
}

main();
