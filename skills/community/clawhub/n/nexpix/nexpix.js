#!/usr/bin/env node

/**
 * NexPix — Cloudflare Image Generation
 * 
 * Free tier image gen (FLUX) + premium fallback (EvoLink).
 * Smart routing, quota tracking, zero cost by default.
 * 
 * Usage:
 *   const nexpix = require('./nexpix');
 *   const result = await nexpix.generate({ prompt: "..." });
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// ─── Paths ───────────────────────────────────────────────────
const HOME = process.env.HOME || '';
const WORKSPACE = path.join(HOME, '.openclaw/workspace');
const ACCESS_DIR = path.join(WORKSPACE, 'ACCESS');
const MEDIA_DIR_FREE = path.join(HOME, '.openclaw/media/workers-ai');
const MEDIA_DIR_PAID = path.join(HOME, '.openclaw/media/evolink');
const TRACKING_PATH = path.join(WORKSPACE, 'notes/image-gen-tracking.json');

// ─── Config ──────────────────────────────────────────────────
const CF_ACCOUNT_ID = process.env.CF_WORKERS_AI_ACCOUNT || 'c52d61bc44ff08ef8c10e06bd007a27c';
const DAILY_NEURON_QUOTA = 10000;
const QUOTA_SAFETY_MARGIN = 0.90;
const EVOLINK_COST_PER_IMAGE = 0.15;

const MODELS = {
  'flux-schnell': '@cf/black-forest-labs/flux-1-schnell',
  'flux-2-dev': '@cf/black-forest-labs/flux-2-dev',
  'sdxl': '@cf/stabilityai/stable-diffusion-xl-base-1.0',
  'dreamshaper': '@cf/lykon/dreamshaper-8-lcm',
};

// ─── Token Helpers ───────────────────────────────────────────
function getCfToken() {
  if (process.env.CF_WORKERS_AI_TOKEN) return process.env.CF_WORKERS_AI_TOKEN;
  const envPath = path.join(ACCESS_DIR, 'cloudflare-workers-ai.env');
  if (fs.existsSync(envPath)) {
    const content = fs.readFileSync(envPath, 'utf8');
    const match = content.match(/CF_WORKERS_AI_TOKEN=(.+)/);
    if (match) return match[1].trim();
  }
  throw new Error('No Cloudflare Workers AI token found. Set CF_WORKERS_AI_TOKEN or create ACCESS/cloudflare-workers-ai.env');
}

function getEvoLinkKey() {
  if (process.env.EVOLINK_API_KEY) return process.env.EVOLINK_API_KEY;
  const envPath = path.join(ACCESS_DIR, 'evolink.env');
  if (fs.existsSync(envPath)) {
    const content = fs.readFileSync(envPath, 'utf8');
    const match = content.match(/EVOLINK_API_KEY=(.+)/);
    if (match) return match[1].trim();
  }
  return null;
}

// ─── Tracking ────────────────────────────────────────────────
function loadTracking() {
  try {
    return JSON.parse(fs.readFileSync(TRACKING_PATH, 'utf8'));
  } catch {
    return {
      daily: {}, totalImages: 0, totalNeurons: 0,
      totalFreeImages: 0, totalPaidImages: 0,
      totalCost: 0, totalSaved: 0, history: [],
    };
  }
}

function saveTracking(tracking) {
  fs.mkdirSync(path.dirname(TRACKING_PATH), { recursive: true });
  fs.writeFileSync(TRACKING_PATH, JSON.stringify(tracking, null, 2));
}

function getDailyUsage() {
  const tracking = loadTracking();
  const today = new Date().toISOString().split('T')[0];
  const day = tracking.daily[today] || { neurons: 0, images: 0 };
  return {
    neuronsUsed: day.neurons || 0,
    neuronsRemaining: DAILY_NEURON_QUOTA - (day.neurons || 0),
    quotaPercent: (((day.neurons || 0) / DAILY_NEURON_QUOTA) * 100).toFixed(1),
    imagesGenerated: day.images || 0,
  };
}

function logGeneration(entry) {
  const tracking = loadTracking();
  const today = new Date().toISOString().split('T')[0];

  if (!tracking.daily[today]) {
    tracking.daily[today] = { neurons: 0, images: 0, freeImages: 0, paidImages: 0, cost: 0, saved: 0 };
  }

  const day = tracking.daily[today];
  day.images += 1;
  day.neurons += entry.neurons || 0;
  day.cost += entry.cost || 0;

  if (entry.source === 'workers-ai') {
    day.freeImages += 1;
    day.saved += EVOLINK_COST_PER_IMAGE;
    tracking.totalFreeImages = (tracking.totalFreeImages || 0) + 1;
    tracking.totalSaved = (tracking.totalSaved || 0) + EVOLINK_COST_PER_IMAGE;
  } else {
    day.paidImages += 1;
    tracking.totalPaidImages = (tracking.totalPaidImages || 0) + 1;
  }

  tracking.totalImages = (tracking.totalImages || 0) + 1;
  tracking.totalNeurons = (tracking.totalNeurons || 0) + (entry.neurons || 0);
  tracking.totalCost = (tracking.totalCost || 0) + (entry.cost || 0);

  tracking.history = tracking.history || [];
  tracking.history.push(entry);
  if (tracking.history.length > 500) tracking.history = tracking.history.slice(-500);

  saveTracking(tracking);
}

// ─── HTTP Helper ─────────────────────────────────────────────
function httpRequest(options, body = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          // Check if response is binary (image)
          if (res.headers['content-type']?.includes('image/')) {
            resolve({ _binary: true, statusCode: res.statusCode, headers: res.headers });
          } else {
            resolve(JSON.parse(data));
          }
        } catch {
          resolve({ _raw: data, statusCode: res.statusCode });
        }
      });
    });
    req.on('error', reject);
    req.setTimeout(60000, () => req.destroy(new Error('Request timeout')));
    if (body) req.write(typeof body === 'string' ? body : JSON.stringify(body));
    req.end();
  });
}

function httpRequestBinary(options, body = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => resolve({ buffer: Buffer.concat(chunks), statusCode: res.statusCode, headers: res.headers }));
    });
    req.on('error', reject);
    req.setTimeout(60000, () => req.destroy(new Error('Request timeout')));
    if (body) req.write(typeof body === 'string' ? body : JSON.stringify(body));
    req.end();
  });
}

function downloadFile(url, filepath) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : require('http');
    client.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return downloadFile(res.headers.location, filepath).then(resolve).catch(reject);
      }
      const ws = fs.createWriteStream(filepath);
      res.pipe(ws);
      ws.on('finish', () => { ws.close(); resolve(); });
      ws.on('error', reject);
    }).on('error', reject);
  });
}

// ─── Route Decision ──────────────────────────────────────────
function decideRoute(options = {}) {
  const { quality = 'standard', preferFree = true, route = null } = options;

  if (route === 'workers-ai') return { route: 'workers-ai', reason: 'forced' };
  if (route === 'evolink') return { route: 'evolink', reason: 'forced' };

  if (quality === 'premium' || quality === '4K') {
    return { route: 'evolink', reason: 'premium quality requested' };
  }

  const usage = getDailyUsage();
  if (parseFloat(usage.quotaPercent) >= QUOTA_SAFETY_MARGIN * 100) {
    return { route: 'evolink', reason: `quota at ${usage.quotaPercent}% (safety margin)` };
  }

  try { getCfToken(); } catch {
    return { route: 'evolink', reason: 'no Workers AI token' };
  }

  if (preferFree) return { route: 'workers-ai', reason: 'free tier available' };
  return { route: 'evolink', reason: 'preferFree=false' };
}

// ─── Workers AI Generation ───────────────────────────────────
async function generateViaWorkersAI(prompt, opts = {}) {
  const { width = 1024, height = 1024, model = 'flux-schnell', steps = 4 } = opts;
  const token = getCfToken();
  const modelId = MODELS[model] || MODELS['flux-schnell'];

  console.log(`🆓 Workers AI: Generating with ${model}...`);
  const startTime = Date.now();

  const bodyStr = JSON.stringify({ prompt, num_steps: steps, width, height });
  const result = await httpRequestBinary({
    hostname: 'api.cloudflare.com',
    path: `/client/v4/accounts/${CF_ACCOUNT_ID}/ai/run/${modelId}`,
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(bodyStr),
    },
  }, bodyStr);

  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  const contentType = result.headers['content-type'] || '';

  let imgBuf;
  let ext = 'jpg';

  if (contentType.includes('image/')) {
    // Direct binary image response
    imgBuf = result.buffer;
    ext = contentType.includes('png') ? 'png' : 'jpg';
  } else {
    // JSON response with base64 image
    let json;
    try { json = JSON.parse(result.buffer.toString()); } catch {
      throw new Error(`Unexpected response: ${result.buffer.toString().slice(0, 200)}`);
    }

    if (json.result?.image) {
      imgBuf = Buffer.from(json.result.image, 'base64');
    } else if (json.result && typeof json.result === 'string') {
      imgBuf = Buffer.from(json.result, 'base64');
    } else {
      throw new Error(json.errors?.[0]?.message || `No image in response: ${JSON.stringify(json).slice(0, 300)}`);
    }
  }

  fs.mkdirSync(MEDIA_DIR_FREE, { recursive: true });
  const filename = `nexpix-${Date.now()}.${ext}`;
  const filepath = path.join(MEDIA_DIR_FREE, filename);
  fs.writeFileSync(filepath, imgBuf);

  const neurons = 1;
  logGeneration({
    source: 'workers-ai', model, prompt, filepath,
    cost: 0, neurons, inferenceTime: parseFloat(elapsed),
    timestamp: new Date().toISOString(),
  });

  console.log(`✅ Generated in ${elapsed}s (FREE)`);
  return {
    success: true, filepath, filename,
    size: imgBuf.length, model, source: 'workers-ai',
    neuronsUsed: neurons, inferenceTime: parseFloat(elapsed),
    prompt, cost: 0, costSaved: EVOLINK_COST_PER_IMAGE,
  };
}

// ─── EvoLink Generation ─────────────────────────────────────
async function generateViaEvoLink(prompt, opts = {}) {
  const { quality = '2K', size = 'auto' } = opts;
  const apiKey = getEvoLinkKey();
  if (!apiKey) return { success: false, error: 'No EvoLink API key configured', source: 'evolink' };

  console.log(`💎 EvoLink: Generating (quality: ${quality})...`);
  const startTime = Date.now();

  const submitBody = JSON.stringify({
    model: 'gemini-3-pro-image-preview', prompt, size, quality,
  });

  const submitResult = await httpRequest({
    hostname: 'api.evolink.ai', path: '/v1/images/generations',
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(submitBody),
    },
  }, submitBody);

  const taskId = submitResult.id || submitResult.task_id;
  if (!taskId) return { success: false, error: `Submit failed: ${JSON.stringify(submitResult).slice(0, 200)}`, source: 'evolink' };

  // Poll for completion
  for (let i = 0; i < 72; i++) {
    await new Promise(r => setTimeout(r, 10000));
    const status = await httpRequest({
      hostname: 'api.evolink.ai', path: `/v1/tasks/${taskId}`,
      headers: { 'Authorization': `Bearer ${apiKey}` },
    });

    if (status.status === 'completed' && status.results?.[0]) {
      const imageUrl = status.results[0].url || status.results[0];
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);

      fs.mkdirSync(MEDIA_DIR_PAID, { recursive: true });
      const ext = imageUrl.includes('.png') ? 'png' : imageUrl.includes('.webp') ? 'webp' : 'jpg';
      const filename = `nexpix-${Date.now()}.${ext}`;
      const filepath = path.join(MEDIA_DIR_PAID, filename);
      await downloadFile(imageUrl, filepath);

      logGeneration({
        source: 'evolink', model: 'gemini-3-pro-image-preview', prompt, filepath,
        cost: EVOLINK_COST_PER_IMAGE, neurons: 0, inferenceTime: parseFloat(elapsed),
        timestamp: new Date().toISOString(),
      });

      console.log(`✅ EvoLink: Generated in ${elapsed}s ($${EVOLINK_COST_PER_IMAGE})`);
      return {
        success: true, filepath, filename, size: fs.statSync(filepath).size,
        model: 'gemini-3-pro-image-preview', source: 'evolink',
        neuronsUsed: 0, inferenceTime: parseFloat(elapsed),
        prompt, cost: EVOLINK_COST_PER_IMAGE, costSaved: 0,
      };
    }

    if (status.status === 'failed') {
      return { success: false, error: `Task failed: ${JSON.stringify(status).slice(0, 200)}`, source: 'evolink' };
    }
  }

  return { success: false, error: 'Timed out after 12 minutes', source: 'evolink' };
}

// ─── Main Generate Function ─────────────────────────────────
async function generate(options = {}) {
  const { prompt, quality = 'standard', preferFree = true, route = null,
    width = 1024, height = 1024, model = null } = options;

  if (!prompt) throw new Error('Prompt is required');

  const decision = decideRoute({ quality, preferFree, route });
  console.log(`🧭 NexPix: routing → ${decision.route} (${decision.reason})`);

  try {
    if (decision.route === 'workers-ai') {
      return await generateViaWorkersAI(prompt, { width, height, model: model || 'flux-schnell' });
    } else {
      return await generateViaEvoLink(prompt, { quality: quality === 'premium' ? '4K' : '2K' });
    }
  } catch (error) {
    if (decision.route === 'workers-ai') {
      console.error(`⚠️ Workers AI failed: ${error.message}`);
      console.log('📌 Falling back to EvoLink...');
      return await generateViaEvoLink(prompt, { quality: '2K' });
    }
    throw error;
  }
}

// ─── Status ──────────────────────────────────────────────────
function getStatus() {
  const tracking = loadTracking();
  const usage = getDailyUsage();
  const today = new Date().toISOString().split('T')[0];
  const day = tracking.daily[today] || { images: 0, freeImages: 0, paidImages: 0, cost: 0, saved: 0 };

  return {
    date: today,
    today: {
      images: day.images, free: day.freeImages || 0, paid: day.paidImages || 0,
      cost: `$${(day.cost || 0).toFixed(2)}`, saved: `$${(day.saved || 0).toFixed(2)}`,
    },
    quota: {
      used: usage.neuronsUsed, remaining: usage.neuronsRemaining,
      percent: `${usage.quotaPercent}%`, limit: DAILY_NEURON_QUOTA,
    },
    allTime: {
      totalImages: tracking.totalImages || 0,
      free: tracking.totalFreeImages || 0, paid: tracking.totalPaidImages || 0,
      totalCost: `$${(tracking.totalCost || 0).toFixed(2)}`,
      totalSaved: `$${(tracking.totalSaved || 0).toFixed(2)}`,
    },
  };
}

// ─── Exports ─────────────────────────────────────────────────
module.exports = { generate, decideRoute, getStatus, getDailyUsage,
  generateViaWorkersAI, generateViaEvoLink,
  DAILY_NEURON_QUOTA, QUOTA_SAFETY_MARGIN, MODELS };
