#!/usr/bin/env node
/**
 * Configure Likes Training Planner Skill
 * Usage: node configure.js
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

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

function prompt(rl, question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer.trim());
    });
  });
}

async function main() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  console.log('🔧 Likes Training Planner - Configuration');
  console.log('=========================================\n');
  
  const config = loadConfig();
  
  // Show current config
  if (config.apiKey) {
    const masked = config.apiKey.substring(0, 8) + '****' + config.apiKey.substring(config.apiKey.length - 4);
    console.log(`Current API Key: ${masked}`);
    console.log(`Base URL: ${config.baseUrl || 'https://my.likes.com.cn'}\n`);
  }
  
  // Get API Key
  const apiKeyInput = await prompt(rl, 'Enter your Likes API Key (or press Enter to keep current): ');
  if (apiKeyInput) {
    config.apiKey = apiKeyInput;
  }
  
  // Get Base URL
  const baseUrlInput = await prompt(rl, `Base URL [${config.baseUrl || 'https://my.likes.com.cn'}]: `);
  if (baseUrlInput) {
    config.baseUrl = baseUrlInput;
  } else if (!config.baseUrl) {
    config.baseUrl = 'https://my.likes.com.cn';
  }
  
  // Save
  saveConfig(config);
  
  console.log('\n✅ Configuration saved!');
  console.log(`Location: ${CONFIG_FILE}`);
  console.log('\nYou can now use the skill without providing API key each time.');
  
  rl.close();
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
