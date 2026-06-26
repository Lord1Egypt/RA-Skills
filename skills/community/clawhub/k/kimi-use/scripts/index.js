#!/usr/bin/env node

/**
 * Kimi Use - Kimi AI tools for Node.js
 * 
 * 使用 Kimi For Coding API（Anthropic 格式）
 * 用法:
 *   node scripts/index.js chat "hello"
 *   node scripts/index.js image "what is this?" /path/to/image.jpg
 *   node scripts/index.js translate "hello" --to Chinese
 */

import { readFileSync } from 'fs';
import { resolve, extname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));

const KIMI_API_KEY = process.env.KIMI_API_KEY;
const KIMI_API_HOST = process.env.KIMI_API_HOST || 'https://api.kimi.com/coding';
const MODEL = process.env.KIMI_MODEL || 'kimi-for-coding';
const VISION_MODEL = process.env.KIMI_VISION_MODEL || 'kimi-vl-flash';

if (!KIMI_API_KEY) {
  console.error('Error: KIMI_API_KEY environment variable not set.');
  console.error('Get your API key at: https://www.kimi.com/code/user-center/basic-information/interface-key');
  process.exit(1);
}

async function chat(message, opts = {}) {
  const { system = null, model = MODEL, temperature = 1.0, max_tokens = 4096, stream = false, history = null } = opts;
  
  const msgs = [];
  if (system) {
    msgs.push({ role: 'system', content: system });
  }
  if (history) {
    msgs.push(...history);
  }
  msgs.push({ role: 'user', content: message });

  try {
    const body = {
      model,
      messages: msgs,
      max_tokens,
      stream,
    };
    if (temperature !== undefined) body.temperature = temperature;

    const resp = await fetch(`${KIMI_API_HOST}/v1/messages`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${KIMI_API_KEY}`,
        'Content-Type': 'application/json',
        'anthropic-version': '2023-06-01',
        'x-api-provider': 'kimi',
      },
      body: JSON.stringify(body),
    });

    if (resp.status === 403) {
      const err = await resp.text();
      return { success: false, error: `403 Forbidden: ${err}` };
    }

    if (!resp.ok) {
      const err = await resp.text();
      return { success: false, error: `HTTP ${resp.status}: ${err}` };
    }

    if (stream) {
      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        process.stdout.write(decoder.decode(value));
      }
      return null;
    }

    const data = await resp.json();
    let content = '';
    for (const block of data.content || []) {
      if (block.type === 'text') content += block.text;
    }
    return { success: true, result: { content } };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

async function understandImage(prompt, imagePath, opts = {}) {
  const { model = VISION_MODEL, temperature = 0.3, max_tokens = 300 } = opts;
  
  try {
    const buffer = readFileSync(resolve(imagePath));
    const ext = extname(imagePath).toLowerCase().slice(1);
    const mimeMap = { jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', webp: 'image/webp', gif: 'image/gif' };
    const mimeType = mimeMap[ext] || 'image/jpeg';
    const imageData = buffer.toString('base64');
    const imageUrl = `data:${mimeType};base64,${imageData}`;

    const resp = await fetch(`${KIMI_API_HOST}/v1/messages`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${KIMI_API_KEY}`,
        'Content-Type': 'application/json',
        'anthropic-version': '2023-06-01',
        'x-api-provider': 'kimi',
      },
      body: JSON.stringify({
        model,
        messages: [{
          role: 'user',
          content: [
            { type: 'image', source: { type: 'base64', media_type: mimeType, data: imageData } },
            { type: 'text', text: prompt }
          ]
        }],
        temperature,
        max_tokens,
      }),
    });

    if (!resp.ok) {
      const err = await resp.text();
      return { success: false, error: `HTTP ${resp.status}: ${err}` };
    }

    const data = await resp.json();
    let content = '';
    for (const block of data.content || []) {
      if (block.type === 'text') content += block.text;
    }
    return { success: true, result: { content } };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

async function translate(text, opts = {}) {
  const { to = 'English', from = 'auto', model = MODEL } = opts;
  const systemPrompt = `You are a professional translator. Translate the following text to ${to}${from !== 'auto' ? ` from ${from}` : ''}. Only output the translated text, no explanations.`;
  return await chat(text, { system: systemPrompt, model, temperature: 0.3, max_tokens: 4096 });
}

// CLI entry point
async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log('Usage:');
    console.log('  node scripts/index.js chat "message" [--model MODEL] [--stream]');
    console.log('  node scripts/index.js image "prompt" /path/to/image.jpg [--model MODEL]');
    console.log('  node scripts/index.js translate "text" --to Chinese [--from English]');
    console.log('');
    console.log('Environment variables:');
    console.log('  KIMI_API_KEY      - API key (required)');
    console.log('  KIMI_API_HOST     - API host (default: https://api.kimi.com/coding)');
    console.log('  KIMI_MODEL        - chat model (default: kimi-for-coding)');
    console.log('  KIMI_VISION_MODEL - vision model (default: kimi-vl-flash)');
    process.exit(0);
  }

  const command = args[0];
  const rest = args.slice(1);

  const getOpt = (args) => {
    const result = {};
    const remaining = [];
    const consumed = new Set();
    for (let i = 0; i < args.length; i++) {
      if (consumed.has(i)) continue;
      const opt = args[i];
      if (opt === '--model' && i + 1 < args.length) { result.model = args[i + 1]; consumed.add(i); consumed.add(i + 1); }
      else if (opt === '--stream') { result.stream = true; consumed.add(i); }
      else if (opt === '--to' && i + 1 < args.length) { result.to = args[i + 1]; consumed.add(i); consumed.add(i + 1); }
      else if (opt === '--from' && i + 1 < args.length) { result.from = args[i + 1]; consumed.add(i); consumed.add(i + 1); }
      else if (!opt.startsWith('--')) { remaining.push(opt); consumed.add(i); }
    }
    return { parsed: result, remaining };
  };

  let result;
  switch (command) {
    case 'chat': {
      const msg = rest.find(a => !a.startsWith('--')) || '';
      const { parsed } = getOpt(rest);
      result = await chat(msg, parsed);
      break;
    }
    case 'image': {
      const prompt = rest.filter(a => !a.startsWith('--') && !a.startsWith('/')).join(' ');
      const imagePath = rest.find(a => a.startsWith('/'));
      const { parsed } = getOpt(rest);
      if (!imagePath) { console.error('Error: image path required'); process.exit(1); }
      result = await understandImage(prompt, imagePath, parsed);
      break;
    }
    case 'translate': {
      const text = rest.find(a => !a.startsWith('--')) || '';
      const { parsed } = getOpt(rest);
      result = await translate(text, parsed);
      break;
    }
    default:
      console.error(`Unknown command: ${command}`); process.exit(1);
  }

  if (result?.success) {
    console.log(result.result.content || '');
  } else {
    console.error('Error:', result?.error || 'Unknown error');
    process.exit(1);
  }
}

export { chat, understandImage, translate };
main().catch(err => { console.error('Fatal error:', err.message); process.exit(1); });
