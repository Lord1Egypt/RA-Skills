#!/usr/bin/env node
/**
 * imgen - Low-cost AI image generation CLI
 * 
 * Usage:
 *   imgen "prompt"                    Generate image from text
 *   imgen edit "url" "prompt"         Edit existing image
 *   imgen config --token YOUR_TOKEN   Set API token
 *   imgen models                      List available models
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// Config paths
const CONFIG_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.imgen');
const TOKEN_FILE = path.join(CONFIG_DIR, 'token');
const OUTPUT_DIR = path.join(process.cwd(), 'generated-images');

// Default API endpoint (OpenAI-compatible)
// Default to laozhang API as documented in SKILL.md
const DEFAULT_API_URL = process.env.IMGEN_API_URL || 'https://api.laozhang.ai/v1/chat/completions';

// Available models with pricing (laozhang API)
// Sorted by price, cheapest first (sora_image is default)
const MODELS = {
  // $0.01/image models (cheapest)
  'sora': { id: 'sora_image', price: '$0.01/img', format: 'url', desc: 'Sora Image, URL output' },
  'gpt4o': { id: 'gpt-4o-image', price: '$0.01/img', format: 'url', desc: 'GPT-4o Image, URL output' },
  // Gemini-based models (base64 output)
  'cheap': { id: 'gemini-2.5-flash-image', price: '$0.025/img', format: 'base64', desc: 'Nano Banana, 1K fixed' },
  'fast': { id: 'gemini-3.1-flash-image-preview', price: '$0.045/img', format: 'base64', desc: 'Nano Banana2, 4K support' },
  'quality': { id: 'gemini-3-pro-image-preview', price: '$0.05/img', format: 'base64', desc: 'Nano Banana Pro, 4K + advanced' },
};

// Preset styles for image editing
const STYLES = {
  'cartoon': 'Convert to Disney cartoon style, bright colors',
  'oil': 'Convert to classic oil painting style, like Van Gogh',
  'ink': 'Convert to Chinese ink wash painting style',
  'cyberpunk': 'Convert to cyberpunk style with neon light effects',
  'sketch': 'Convert to pencil sketch style, black and white lines',
  'watercolor': 'Convert to watercolor painting style',
};

// ============ Utility Functions ============

function ensureConfigDir() {
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  }
}

function getToken() {
  if (fs.existsSync(TOKEN_FILE)) {
    return fs.readFileSync(TOKEN_FILE, 'utf8').trim();
  }
  const envToken = process.env.IMGEN_TOKEN || process.env.OPENAI_API_KEY;
  if (envToken) return envToken;
  return null;
}

function saveToken(token) {
  ensureConfigDir();
  fs.writeFileSync(TOKEN_FILE, token, { mode: 0o600 });
  console.log(`✓ Token saved to ${TOKEN_FILE}`);
}

function generateFilename(prompt, suffix = '') {
  const date = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const keywords = prompt.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '-').slice(0, 20);
  return `${date}-${keywords}${suffix}.png`;
}

function httpGet(url) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    client.get(url, (res) => {
      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => resolve(Buffer.concat(chunks)));
      res.on('error', reject);
    }).on('error', reject);
  });
}

function httpPost(urlString, headers, body) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlString);
    const client = url.protocol === 'https:' ? https : http;
    
    const options = {
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname + url.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...headers
      }
    };
    
    const req = client.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error(`Invalid JSON: ${data.slice(0, 200)}`));
        }
      });
    });
    
    req.on('error', reject);
    req.write(JSON.stringify(body));
    req.end();
  });
}

// ============ Core Functions ============

async function generateImage(prompt, options = {}) {
  const token = options.token || getToken();
  if (!token) {
    console.error('Error: No API token. Run: imgen config --token YOUR_TOKEN');
    process.exit(1);
  }

  const model = options.model || 'cheap';
  const modelInfo = MODELS[model] || MODELS['cheap'];
  
  // Build request - simple text prompt
  const body = {
    model: modelInfo.id,
    messages: [{ role: 'user', content: prompt }],
    n: 1,
    size: options.size || '1024x1024'
  };

  console.error(`Generating with ${modelInfo.id} (${modelInfo.price})...`);

  try {
    const result = await httpPost(DEFAULT_API_URL, {
      'Authorization': `Bearer ${token}`
    }, body);

    // Extract image from response (URL or base64)
    const content = result.choices?.[0]?.message?.content || '';
    
    // Check for markdown image with URL
    let imageUrl = null;
    let base64Data = null;
    
    const urlMatch = content.match(/!\[.*?\]\((https?:\/\/[^)]+)\)/);
    const base64Match = content.match(/!\[.*?\]\((data:image\/[^;]+;base64,([^)]+))\)/);
    
    if (urlMatch) {
      imageUrl = urlMatch[1];
    } else if (base64Match) {
      base64Data = base64Match[2];
    } else {
      imageUrl = result.data?.[0]?.url;
    }

    if (!imageUrl && !base64Data) {
      console.error('No image in response');
      if (options.verbose) console.log(JSON.stringify(result, null, 2));
      process.exit(1);
    }

    // Save or print
    if (!options.noSave) {
      const outputPath = options.output || path.join(OUTPUT_DIR, generateFilename(prompt));
      
      if (base64Data) {
        // Save base64 directly
        const dir = path.dirname(outputPath);
        if (!fs.existsSync(dir)) {
          fs.mkdirSync(dir, { recursive: true });
        }
        fs.writeFileSync(outputPath, Buffer.from(base64Data, 'base64'));
        console.error(`✓ Saved: ${outputPath}`);
        console.log(outputPath);
      } else {
        console.log(imageUrl);
        await downloadImage(imageUrl, outputPath);
      }
    } else if (imageUrl) {
      console.log(imageUrl);
    } else if (base64Match) {
      console.log(base64Match[1]); // Full data URL
    }

    return imageUrl || (base64Match ? base64Match[1] : null);
  } catch (err) {
    console.error('API error:', err.message);
    process.exit(1);
  }
}

async function editImage(imageUrl, prompt, options = {}) {
  const token = options.token || getToken();
  if (!token) {
    console.error('Error: No API token. Run: imgen config --token YOUR_TOKEN');
    process.exit(1);
  }

  // Apply style preset if provided
  if (options.style && STYLES[options.style]) {
    prompt = STYLES[options.style];
  }

  const model = options.model || 'cheap';
  const modelInfo = MODELS[model] || MODELS['cheap'];

  // Build request with image
  const body = {
    model: modelInfo.id,
    messages: [{
      role: 'user',
      content: [
        { type: 'text', text: prompt },
        { type: 'image_url', image_url: { url: imageUrl } }
      ]
    }]
  };

  console.error(`Editing with ${modelInfo.id} (${modelInfo.price})...`);

  try {
    const result = await httpPost(DEFAULT_API_URL, {
      'Authorization': `Bearer ${token}`
    }, body);

    const content = result.choices?.[0]?.message?.content || '';
    
    // Check for markdown image with URL or base64
    let resultUrl = null;
    let base64Data = null;
    
    const urlMatch = content.match(/!\[.*?\]\((https?:\/\/[^)]+)\)/);
    const base64Match = content.match(/!\[.*?\]\((data:image\/[^;]+;base64,([^)]+))\)/);
    
    if (urlMatch) {
      resultUrl = urlMatch[1];
    } else if (base64Match) {
      base64Data = base64Match[2];
    } else {
      resultUrl = result.data?.[0]?.url;
    }

    if (!resultUrl && !base64Data) {
      console.error('No image in response');
      process.exit(1);
    }

    if (!options.noSave) {
      const suffix = options.style ? `-${options.style}` : '-edited';
      const outputPath = options.output || path.join(OUTPUT_DIR, generateFilename(prompt, suffix));
      
      if (base64Data) {
        const dir = path.dirname(outputPath);
        if (!fs.existsSync(dir)) {
          fs.mkdirSync(dir, { recursive: true });
        }
        fs.writeFileSync(outputPath, Buffer.from(base64Data, 'base64'));
        console.error(`✓ Saved: ${outputPath}`);
        console.log(outputPath);
      } else {
        console.log(resultUrl);
        await downloadImage(resultUrl, outputPath);
      }
    } else if (resultUrl) {
      console.log(resultUrl);
    } else if (base64Match) {
      console.log(base64Match[1]);
    }

    return resultUrl || (base64Match ? base64Match[1] : null);
  } catch (err) {
    console.error('API error:', err.message);
    process.exit(1);
  }
}

async function downloadImage(url, outputPath) {
  try {
    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    const buffer = await httpGet(url);
    fs.writeFileSync(outputPath, buffer);
    console.error(`✓ Saved: ${outputPath}`);
  } catch (err) {
    console.error('Download failed:', err.message);
  }
}

function printHelp() {
  console.log(`
imgen - Low-cost AI image generation CLI

USAGE:
  imgen "prompt"                        Generate image from text
  imgen edit <url> "prompt"             Edit an image
  imgen edit <url> --style <style>      Apply preset style
  imgen config --token <token>          Set API token
  imgen models                          List available models

OPTIONS:
  -m, --model <name>      Model to use (cheap/fast/quality)
  -o, --output <path>     Save to specific path
  --size <size>           Image size (1024x1024, 512x512, etc.)
  --no-save               Don't save, just print URL
  -v, --verbose           Show detailed output
  -h, --help              Show this help

MODELS:
  sora      sora_image                       $0.01/img (default, URL)
  gpt4o     gpt-4o-image                     $0.01/img (URL)
  cheap     gemini-2.5-flash-image           $0.025/img (base64)
  fast      gemini-3.1-flash-image-preview   $0.045/img (base64, 4K)
  quality   gemini-3-pro-image-preview       $0.05/img (base64, 4K)

STYLES (for editing):
  cartoon, oil, ink, cyberpunk, sketch, watercolor

EXAMPLES:
  imgen "A cute cat in a garden"
  imgen "Sunset beach" --ratio 3:2 -o beach.png
  imgen edit "https://example.com/cat.jpg" "Make it look like a cartoon"
  imgen edit "https://example.com/photo.jpg" --style cyberpunk

ENVIRONMENT:
  IMGEN_TOKEN      API token (alternative to config file)
  IMGEN_API_URL    Custom API endpoint

First time? Run: imgen config --token YOUR_API_TOKEN
`);
}

// ============ CLI Entry Point ============

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('-h') || args.includes('--help')) {
    printHelp();
    process.exit(0);
  }

  const command = args[0];

  // Parse flags
  const options = {};
  let positional = [];
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '-m' || arg === '--model') {
      options.model = args[++i];
    } else if (arg === '-o' || arg === '--output') {
      options.output = args[++i];
    } else if (arg === '--size') {
      options.size = args[++i];
    } else if (arg === '--no-save') {
      options.noSave = true;
    } else if (arg === '-v' || arg === '--verbose') {
      options.verbose = true;
    } else if (arg === '--token') {
      options.token = args[++i];
    } else if (arg === '--style' || arg === '-s') {
      options.style = args[++i];
    } else if (!arg.startsWith('-')) {
      positional.push(arg);
    }
  }

  // Handle commands
  if (command === 'config') {
    if (options.token) {
      saveToken(options.token);
    } else {
      console.error('Usage: imgen config --token YOUR_TOKEN');
      process.exit(1);
    }
    return;
  }

  if (command === 'models') {
    console.log('\nAvailable Models:\n');
    for (const [key, info] of Object.entries(MODELS)) {
      console.log(`  ${key.padEnd(10)} ${info.id.padEnd(20)} ${info.price}`);
    }
    console.log('\nStyles: ' + Object.keys(STYLES).join(', ') + '\n');
    return;
  }

  if (command === 'edit') {
    const [imageUrl, prompt] = positional.slice(1);
    if (!imageUrl) {
      console.error('Usage: imgen edit <image_url> "prompt" [--style <style>]');
      process.exit(1);
    }
    await editImage(imageUrl, prompt || '', options);
    return;
  }

  // Default: generate image
  const prompt = positional.join(' ');
  if (!prompt) {
    console.error('Error: No prompt provided');
    console.error('Usage: imgen "your prompt here"');
    process.exit(1);
  }
  
  await generateImage(prompt, options);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
