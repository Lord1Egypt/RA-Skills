/**
 * GPT Chat - GPT对话与内容生成
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// 从环境变量读取 API Key
const API_KEY = process.env.OPENAI_API_KEY || '';
const API_BASE = process.env.OPENAI_API_BASE || 'https://api.openai-proxy.org';

const MODELS = {
  'gpt-5.2': 'gpt-5.2',
  'gpt-5.1': 'gpt-5.1', 
  'gpt-5': 'gpt-5'
};

const MODEL_PRICING = {
  'gpt-5.2': { name: 'GPT-5.2', input: 1.75, output: 14 },
  'gpt-5.1': { name: 'GPT-5.1', input: 1.25, output: 10 },
  'gpt-5': { name: 'GPT-5', input: 1.25, output: 10 }
};

const STATE_FILE = path.join(__dirname, 'state.json');

function loadState() {
  try {
    if (fs.existsSync(STATE_FILE)) {
      return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
    }
  } catch (e) {}
  return { currentModel: 'gpt-5.1' };
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

let state = loadState();

function callOpenAI(message, model) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      model: model,
      messages: [{ role: 'user', content: message }],
      max_completion_tokens: 4000
    });

    const options = {
      hostname: API_BASE.replace('https://', '').replace('http://', ''),
      path: '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.error) {
            reject(new Error(result.error.message));
          } else {
            resolve(result.choices[0].message.content);
          }
        } catch (e) {
          reject(new Error('Failed to parse response: ' + e.message + ' | ' + data.slice(0, 200)));
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

const args = process.argv.slice(2);
const command = args[0];

async function main() {
  try {
    if (command === 'list') {
      console.log('Available models:');
      for (const [key, val] of Object.entries(MODEL_PRICING)) {
        const defaultTag = key === 'gpt-5.1' ? ' [DEFAULT]' : '';
        console.log(`  ${key} - ${val.name} ($${val.input}/1M in, $${val.output}/1M out)${defaultTag}`);
      }
      console.log(`\nCurrent model: ${state.currentModel}`);
    } 
    else if (command === 'set' && args[1]) {
      const model = args[1];
      if (MODELS[model]) {
        state.currentModel = model;
        saveState(state);
        console.log(`Model switched to: ${state.currentModel}`);
      } else {
        console.log(`Invalid model: ${model}`);
        console.log('Available models:', Object.keys(MODELS).join(', '));
        process.exit(1);
      }
    } 
    else if (command === 'chat' && args[1]) {
      const message = args.slice(1).join(' ');
      console.log(`Using model: ${state.currentModel}`);
      console.log('Calling API...');
      const response = await callOpenAI(message, state.currentModel);
      console.log('\n--- Response ---');
      console.log(response);
    }
    else if (command === 'current') {
      console.log(state.currentModel);
    }
    else if (command === 'state') {
      console.log(JSON.stringify(state, null, 2));
    }
    else {
      console.log('Usage:');
      console.log('  node gpt.js list              - List available models');
      console.log('  node gpt.js set <model>       - Switch model (gpt-5.2/gpt-5.1/gpt-5)');
      console.log('  node gpt.js chat <message> - Send chat message');
      console.log('  node gpt.js current          - Show current model');
    }
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();
