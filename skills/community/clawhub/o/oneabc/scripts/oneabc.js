#!/usr/bin/env node

const API_KEY = process.env.ONEABC_API_KEY || process.env.OPENAI_API_KEY;
const BASE_URL = process.env.ONEABC_BASE_URL || 'https://api.oneabc.org';

if (!API_KEY) {
  console.error('Missing ONEABC_API_KEY');
  process.exit(1);
}

const args = process.argv.slice(2);
const command = args[0] || 'help';
const input = args.slice(1).join(' ');

async function callChat(model, prompt, maxTokens = 2000) {
  const response = await fetch(`${BASE_URL}/v1/chat/completions`, {
    method: 'POST',
    headers: {
      'Authorization': API_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model,
      messages: [{ role: 'user', content: prompt }],
      max_tokens: maxTokens
    })
  });
  const data = await response.json();
  if (data.error) return `❌ Error: ${data.error.message}`;
  return data.choices?.[0]?.message?.content || JSON.stringify(data, null, 2);
}

async function main() {
  switch (command) {
    case 'chat': {
      const model = args[1] || 'gpt-4o';
      const prompt = args.slice(2).join(' ');
      if (!prompt) return console.log('Usage: node oneabc.js chat <model> <prompt>');
      console.log(await callChat(model, prompt, 2000));
      break;
    }
    case 'video':
    case 'sora':
      if (!input) return console.log('Usage: node oneabc.js video <prompt>');
      console.log(await callChat('sora-2', args.slice(1).join(' '), 500));
      break;
    case 'image':
    case 'img':
      if (!input) return console.log('Usage: node oneabc.js image <prompt>');
      console.log(await callChat('flux-1-schnell', args.slice(1).join(' '), 500));
      break;
    case 'music':
    case 'suno':
      if (!input) return console.log('Usage: node oneabc.js music <prompt>');
      console.log(await callChat('suno-v3.5', args.slice(1).join(' '), 500));
      break;
    case 'models': {
      const response = await fetch(`${BASE_URL}/v1/models`, { headers: { 'Authorization': API_KEY } });
      const data = await response.json();
      console.log((data.data || []).map(m => m.id).join('\n'));
      break;
    }
    default:
      console.log('Usage: node scripts/oneabc.js <chat|video|image|music|models> ...');
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
