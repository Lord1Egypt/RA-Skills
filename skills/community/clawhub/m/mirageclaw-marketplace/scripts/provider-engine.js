'use strict';

const fs   = require('fs');
const path = require('path');

// Map Content-Type to file extension
const CONTENT_TYPE_EXT = {
  'image/png': '.png',
  'image/jpeg': '.jpg',
  'image/webp': '.webp',
  'image/gif': '.gif',
  'video/mp4': '.mp4',
  'video/quicktime': '.mov',
  'video/webm': '.webm'
};

function resolveExt(contentType) {
  if (!contentType) return '.png';
  const mime = contentType.split(';')[0].trim().toLowerCase();
  return CONTENT_TYPE_EXT[mime] || '.png';
}

const REGISTRY_PATH = path.join(__dirname, '..', 'data', 'providers.json');

// ── Registry ────────────────────────────────────────────────────────────────

function loadRegistry() {
  return JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf-8'));
}

function resolveProvider(capability) {
  const registry = loadRegistry();
  const base = registry[capability.api] || {};
  const inline = capability.provider || {};

  return {
    endpoint:    capability.endpoint || inline.endpoint || base.endpoint,
    auth:        inline.auth         || base.auth       || 'Bearer {{apiKey}}',
    body:        inline.body         || base.body       || { prompt: '{{prompt}}' },
    sizeMap:     inline.sizeMap      || base.sizeMap    || null,
    contentType: inline.contentType  || base.contentType || 'application/json',
    response:    { ...base.response, ...inline.response },
  };
}

// ── Prompt builder ──────────────────────────────────────────────────────────

function buildPrompt(spec) {
  return [
    spec.description,
    spec.style && `style: ${spec.style}`,
    spec.mood  && `mood: ${spec.mood}`,
    spec.color && `colors: ${spec.color}`,
    spec.title && `subject: ${spec.title}`,
  ].filter(Boolean).join(', ');
}

// ── Fetch with retry (5xx and network errors only) ──────────────────────────

async function fetchWithRetry(url, opts, maxRetries = 2) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const res = await fetch(url, opts);
      if (res.ok || res.status < 500) return res;
      if (attempt < maxRetries) await new Promise(r => setTimeout(r, 5000));
    } catch (err) {
      if (attempt >= maxRetries) throw err;
      await new Promise(r => setTimeout(r, 5000));
    }
  }
  return fetch(url, opts);
}

// ── Template interpolation ──────────────────────────────────────────────────

function interpolate(template, vars) {
  if (typeof template === 'string') {
    // If the entire string is a single {{var}}, preserve the original type (number, boolean, etc.)
    const exactMatch = template.match(/^\{\{(\w+)\}\}$/);
    if (exactMatch) {
      const val = vars[exactMatch[1]];
      return val !== undefined ? val : '';
    }
    // Otherwise, string interpolation (always returns string)
    return template.replace(/\{\{(\w+)\}\}/g, (_, k) => vars[k] ?? '');
  }
  if (Array.isArray(template)) return template.map(v => interpolate(v, vars));
  if (typeof template === 'object' && template !== null) {
    const out = {};
    for (const [k, v] of Object.entries(template)) {
      out[k] = interpolate(v, vars);
    }
    return out;
  }
  return template;
}

function resolveSize(sizeMap, ratio) {
  if (!sizeMap) return null;
  return sizeMap[ratio] || sizeMap['default'] || null;
}

function resolvePath(obj, pathStr) {
  return pathStr.replace(/\[(\d+)\]/g, '.$1').split('.').reduce((o, k) => o?.[k], obj);
}

// ── Main entry point ────────────────────────────────────────────────────────

async function callProvider(capability, specPath, resultBase) {
  const apiKey = process.env[capability.envKey];
  if (!apiKey) throw new Error(`Missing env: ${capability.envKey}`);

  const spec = JSON.parse(fs.readFileSync(specPath, 'utf-8'));
  const prompt = buildPrompt(spec);
  const provider = resolveProvider(capability);

  if (!provider.endpoint) {
    throw new Error(`No endpoint for "${capability.api}". Set endpoint in config or add to data/providers.json`);
  }

  // Resolve size from ratio
  const sizeVal = resolveSize(provider.sizeMap, spec.ratio);
  const vars = { apiKey, prompt };
  if (typeof sizeVal === 'string') {
    vars.size = sizeVal;
  } else if (typeof sizeVal === 'object' && sizeVal) {
    Object.assign(vars, sizeVal);
  }

  // Build request
  const headers = {};
  if (provider.auth) {
    headers['Authorization'] = interpolate(provider.auth, vars);
  }
  const body = interpolate(provider.body, vars);

  let fetchOpts;
  if (provider.contentType === 'multipart/form-data') {
    const form = new FormData();
    for (const [k, v] of Object.entries(body)) form.append(k, String(v));
    fetchOpts = { method: 'POST', headers, body: form };
  } else {
    headers['Content-Type'] = 'application/json';
    fetchOpts = { method: 'POST', headers, body: JSON.stringify(body) };
  }

  // Timeout: 15 minutes
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 15 * 60 * 1000);
  fetchOpts.signal = controller.signal;

  try {
    const res = await fetchWithRetry(provider.endpoint, fetchOpts);
    if (!res.ok) {
      throw new Error(`${capability.api} ${res.status}: ${(await res.text()).slice(0, 300)}`);
    }

    // Binary response (HuggingFace, Stability AI, video APIs)
    if (provider.response.type === 'binary') {
      const buffer = Buffer.from(await res.arrayBuffer());
      const ext = resolveExt(res.headers.get('content-type'));
      const outputPath = `${resultBase}${ext}`;
      fs.writeFileSync(outputPath, buffer);
      return outputPath;
    }

    // JSON response
    const data = await res.json();

    // Async polling (Leonardo etc.)
    if (provider.response.poll) {
      return await pollForResult(data, provider, vars, resultBase, capability);
    }

    // Direct image URL
    const imageUrl = resolvePath(data, provider.response.imagePath);
    if (!imageUrl) {
      throw new Error(`No image URL at "${provider.response.imagePath}" in response`);
    }
    return await downloadImage(imageUrl, resultBase);
  } finally {
    clearTimeout(timer);
  }
}

// ── Polling for async APIs ──────────────────────────────────────────────────

async function pollForResult(initialData, provider, vars, resultBase, capability = {}) {
  const poll = provider.response.poll;
  const genId = resolvePath(initialData, poll.idPath);
  if (!genId) throw new Error(`No generation ID at "${poll.idPath}"`);

  const statusUrl = poll.statusUrl.replace('{{generationId}}', genId);
  const deadline = Date.now() + (capability.timeout || poll.timeout || 120000);
  const interval = poll.interval || 3000;

  while (Date.now() < deadline) {
    await new Promise(r => setTimeout(r, interval));
    const res = await fetch(statusUrl, {
      headers: { 'Authorization': interpolate(provider.auth, vars) }
    });
    if (!res.ok) continue;
    const data = await res.json();
    const status = resolvePath(data, poll.completePath);
    if (status === poll.completeValue) {
      const imageUrl = resolvePath(data, poll.imagePath);
      if (!imageUrl) throw new Error(`No image URL at "${poll.imagePath}" after completion`);
      return await downloadImage(imageUrl, resultBase);
    }
  }
  throw new Error(`Polling timeout after ${poll.timeout || 120000}ms`);
}

// ── Download helper ─────────────────────────────────────────────────────────

async function downloadImage(url, resultBase) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Image download failed: ${res.status}`);
  const buffer = Buffer.from(await res.arrayBuffer());
  const ext = resolveExt(res.headers.get('content-type'));
  const outputPath = `${resultBase}${ext}`;
  fs.writeFileSync(outputPath, buffer);
  return outputPath;
}

// ── Exports ─────────────────────────────────────────────────────────────────

module.exports = { callProvider, loadRegistry };
