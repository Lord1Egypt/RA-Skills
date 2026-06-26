/**
 * GPT Model Selector Script
 * Supports GPT-5.2, GPT-5.1, GPT-5 model selection
 */

const OPENAI_API_KEY = process.env.OPENAI_API_KEY || '';
const DEFAULT_MODEL = 'gpt-5.1';

const MODELS = {
  'gpt-5.2': { name: 'GPT-5.2', inputPrice: 1.75, outputPrice: 14 },
  'gpt-5.1': { name: 'GPT-5.1', inputPrice: 1.25, outputPrice: 10 },
  'gpt-5': { name: 'GPT-5', inputPrice: 1.25, outputPrice: 10 }
};

let currentModel = DEFAULT_MODEL;

// Simple HTTP server for receiving requests
const http = require('http');
const url = require('url');

const server = http.createServer(async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;

  try {
    if (pathname === '/health') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ status: 'ok', currentModel }));
      return;
    }

    if (pathname === '/set-model' && req.method === 'POST') {
      let body = '';
      req.on('data', chunk => body += chunk);
      req.on('end', () => {
        const { model } = JSON.parse(body);
        if (MODELS[model]) {
          currentModel = model;
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: true, model: currentModel }));
        } else {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Invalid model' }));
        }
      });
      return;
    }

    if (pathname === '/chat' && req.method === 'POST') {
      let body = '';
      req.on('data', chunk => body += chunk);
      req.on('end', async () => {
        const { message } = JSON.parse(body);
        
        const response = await callOpenAI(message);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ 
          response, 
          model: currentModel,
          modelInfo: MODELS[currentModel]
        }));
      });
      return;
    }

    if (pathname === '/models' && req.method === 'GET') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ models: MODELS, currentModel }));
      return;
    }

    res.writeHead(404);
    res.end(JSON.stringify({ error: 'Not found' }));
  } catch (error) {
    res.writeHead(500, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: error.message }));
  }
});

async function callOpenAI(message) {
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${OPENAI_API_KEY}`
    },
    body: JSON.stringify({
      model: currentModel,
      messages: [
        { role: 'user', content: message }
      ],
      max_tokens: 4000
    })
  });

  const data = await response.json();
  
  if (data.error) {
    throw new Error(data.error.message);
  }
  
  return data.choices[0].message.content;
}

const PORT = process.env.PORT || 3456;

server.listen(PORT, () => {
  console.log(`GPT Model Selector running on port ${PORT}`);
  console.log(`Default model: ${DEFAULT_MODEL}`);
  console.log(`Available models: ${Object.keys(MODELS).join(', ')}`);
});

// Handle process termination
process.on('SIGTERM', () => {
  server.close(() => process.exit(0));
});

process.on('SIGINT', () => {
  server.close(() => process.exit(0));
});
