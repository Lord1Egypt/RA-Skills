#!/usr/bin/env node
/**
 * Configure Likes Training Planner Skill
 * Usage: 
 *   node configure.cjs                    # Interactive mode
 *   node set-config.cjs <api_key>         # Direct set
 *   API_KEY=xxx node set-config.cjs       # From env
 */

const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(require('os').homedir(), '.openclaw');
const CONFIG_FILE = path.join(CONFIG_DIR, 'likes-training-planner.json');

function ensureConfigDir() {
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  }
}

function loadConfig() {
  if (fs.existsSync(CONFIG_FILE)) {
    try {
      return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
    } catch (e) {
      return {};
    }
  }
  return {};
}

function saveConfig(config) {
  ensureConfigDir();
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
}

function main() {
  const args = process.argv.slice(2);
  const envKey = process.env.API_KEY || process.env.LIKES_API_KEY;
  
  let apiKey = args[0] || envKey;
  
  if (!apiKey) {
    console.log('Usage: node set-config.cjs <api_key>');
    console.log('   or: API_KEY=xxx node set-config.cjs');
    process.exit(1);
  }
  
  const config = loadConfig();
  config.apiKey = apiKey;
  if (!config.baseUrl) {
    config.baseUrl = 'https://my.likes.com.cn';
  }
  
  saveConfig(config);
  
  const masked = apiKey.substring(0, 8) + '****' + apiKey.substring(apiKey.length - 4);
  console.log('✅ Configuration saved!');
  console.log(`   API Key: ${masked}`);
  console.log(`   Base URL: ${config.baseUrl}`);
  console.log(`   Location: ${CONFIG_FILE}`);
}

main();
