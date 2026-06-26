#!/usr/bin/env node
/**
 * Add coach comment to trainee's training feedback
 * POST /api/open/feedback/comment
 * 
 * API Change: Now only requires content and feedback_id
 * user_id and uid are taken from session on the server
 * 
 * Usage: node add_feedback_comment.cjs --feedback-id <id> --content <text>
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

function addFeedbackComment(apiKey, baseUrl, commentData) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(commentData);
    
    const options = {
      hostname: baseUrl,
      path: '/api/open/feedback/comment',
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
          if (res.statusCode === 400) {
            reject(new Error(`Bad request: ${result.message || 'Invalid parameters'}`));
            return;
          }
          if (res.statusCode === 401) {
            reject(new Error('Unauthorized: Invalid API key'));
            return;
          }
          if (res.statusCode === 403) {
            reject(new Error('Forbidden: You are not authorized to comment on this feedback'));
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

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    feedback_id: null,
    content: null
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--feedback-id' && i + 1 < args.length) {
      options.feedback_id = parseInt(args[i + 1]);
      i++;
    } else if (args[i] === '--content' && i + 1 < args.length) {
      options.content = args[i + 1];
      i++;
    }
  }
  
  return options;
}

function showUsage() {
  console.log('Usage: node add_feedback_comment.cjs --feedback-id <id> --content <text>');
  console.log('');
  console.log('Required:');
  console.log('  --feedback-id <id>   Trainee\'s feedback ID to comment on');
  console.log('  --content <text>     Comment content / training advice');
  console.log('');
  console.log('Example:');
  console.log('  node add_feedback_comment.cjs --feedback-id 227639 --content "跑得很好，继续加油！"');
  console.log('');
  console.log('Note:');
  console.log('  - You must be the trainee\'s coach (camp editor/coach)');
  console.log('  - user_id and uid are automatically taken from your session');
}

async function main() {
  const options = parseArgs();
  
  if (!options.feedback_id || !options.content) {
    console.error('❌ Error: --feedback-id and --content are required');
    showUsage();
    process.exit(1);
  }
  
  if (options.feedback_id <= 0) {
    console.error('❌ Error: feedback_id must be a positive integer');
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
  
  const commentData = {
    feedback_id: options.feedback_id,
    content: options.content.trim()
  };
  
  try {
    console.log('💬 Adding feedback comment...');
    console.log(`   Feedback ID: ${options.feedback_id}`);
    console.log(`   Content: ${options.content}`);
    console.log('');
    
    const result = await addFeedbackComment(apiKey, baseUrl, commentData);
    
    console.log('✅ Comment added successfully!');
    console.log('');
    console.log('Response:');
    console.log(JSON.stringify(result, null, 2));
    
  } catch (e) {
    console.error(`❌ Error: ${e.message}`);
    process.exit(1);
  }
}

main();
