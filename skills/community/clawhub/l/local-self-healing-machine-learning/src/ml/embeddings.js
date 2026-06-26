// embeddings.js — Local Ollama embeddings for semantic error matching.
// Uses llama3.2:3b via localhost:11434 to produce 3072-dim vectors.
// Caches embeddings in SQLite to avoid recomputing. Graceful fallback
// if Ollama is unavailable.

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const http = require('http');

const MEMORY_DIR = path.resolve(__dirname, '..', '..', 'memory');
const CACHE_PATH = path.join(MEMORY_DIR, 'embeddings-cache.json');
const OLLAMA_URL = process.env.OLLAMA_URL || 'http://localhost:11434';
const OLLAMA_MODEL = process.env.OLLAMA_EMBED_MODEL || 'llama3.2:3b';
const REQUEST_TIMEOUT_MS = 30000;

let _cache = null;
let _ollamaAvailable = null;

function ensureMemoryDir() {
  try {
    if (!fs.existsSync(MEMORY_DIR)) fs.mkdirSync(MEMORY_DIR, { recursive: true });
  } catch {}
}

function loadCache() {
  if (_cache) return _cache;
  ensureMemoryDir();
  try {
    if (fs.existsSync(CACHE_PATH)) {
      _cache = JSON.parse(fs.readFileSync(CACHE_PATH, 'utf8'));
    } else {
      _cache = {};
    }
  } catch {
    _cache = {};
  }
  return _cache;
}

const MAX_CACHE_ENTRIES = 1000;

function pruneCache() {
  if (!_cache) return;
  const keys = Object.keys(_cache);
  if (keys.length <= MAX_CACHE_ENTRIES) return;
  // Drop oldest entries (first inserted = first keys in object iteration order)
  const toRemove = keys.length - MAX_CACHE_ENTRIES;
  for (let i = 0; i < toRemove; i++) {
    delete _cache[keys[i]];
  }
}

function saveCache() {
  if (!_cache) return;
  pruneCache();
  ensureMemoryDir();
  try {
    const tmp = CACHE_PATH + '.tmp';
    fs.writeFileSync(tmp, JSON.stringify(_cache), 'utf8');
    fs.renameSync(tmp, CACHE_PATH);
  } catch {}
}

function textHash(text) {
  return crypto.createHash('sha256').update(String(text)).digest('hex').slice(0, 24);
}

// Check if Ollama is reachable (cached for session).
function isOllamaAvailable() {
  if (_ollamaAvailable !== null) return Promise.resolve(_ollamaAvailable);
  return new Promise((resolve) => {
    const url = new URL('/api/tags', OLLAMA_URL);
    const req = http.get(url, { timeout: 5000 }, (res) => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        _ollamaAvailable = res.statusCode === 200;
        resolve(_ollamaAvailable);
      });
    });
    req.on('error', () => { _ollamaAvailable = false; resolve(false); });
    req.on('timeout', () => { req.destroy(); _ollamaAvailable = false; resolve(false); });
  });
}

// Reset availability cache (useful for testing).
function resetAvailabilityCache() {
  _ollamaAvailable = null;
}

// Get embedding vector for text. Returns Float64Array or null.
async function embedText(text) {
  const t = String(text || '').trim();
  if (!t) return null;

  const hash = textHash(t);
  const cache = loadCache();
  if (cache[hash]) return new Float64Array(cache[hash]);

  const available = await isOllamaAvailable();
  if (!available) return null;

  return new Promise((resolve) => {
    const url = new URL('/api/embeddings', OLLAMA_URL);
    const body = JSON.stringify({ model: OLLAMA_MODEL, prompt: t });
    const req = http.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      timeout: REQUEST_TIMEOUT_MS,
    }, (res) => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (parsed.embedding && Array.isArray(parsed.embedding)) {
            cache[hash] = parsed.embedding;
            saveCache();
            resolve(new Float64Array(parsed.embedding));
          } else {
            resolve(null);
          }
        } catch {
          resolve(null);
        }
      });
    });
    req.on('error', () => resolve(null));
    req.on('timeout', () => { req.destroy(); resolve(null); });
    req.write(body);
    req.end();
  });
}

// Cosine similarity between two vectors.
function cosineSimilarity(vecA, vecB) {
  if (!vecA || !vecB || vecA.length !== vecB.length || vecA.length === 0) return 0;
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < vecA.length; i++) {
    dot += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }
  const denom = Math.sqrt(normA) * Math.sqrt(normB);
  return denom === 0 ? 0 : dot / denom;
}

// Cluster error lines by semantic similarity.
// Returns array of clusters: [{centroid, members: [string], label}]
async function clusterErrors(errorLines, threshold = 0.85) {
  if (!Array.isArray(errorLines) || errorLines.length === 0) return [];

  const embeddings = [];
  for (const line of errorLines) {
    const vec = await embedText(line);
    embeddings.push({ text: line, vec });
  }

  // Filter out lines that couldn't be embedded
  const valid = embeddings.filter(e => e.vec !== null);
  if (valid.length === 0) return [];

  // Simple agglomerative clustering
  const clusters = [];
  const assigned = new Set();

  for (let i = 0; i < valid.length; i++) {
    if (assigned.has(i)) continue;

    const cluster = { centroid: valid[i].vec, members: [valid[i].text], indices: [i] };
    assigned.add(i);

    for (let j = i + 1; j < valid.length; j++) {
      if (assigned.has(j)) continue;
      const sim = cosineSimilarity(valid[i].vec, valid[j].vec);
      if (sim >= threshold) {
        cluster.members.push(valid[j].text);
        cluster.indices.push(j);
        assigned.add(j);
      }
    }

    // Label is the shortest member (most concise error description)
    cluster.label = cluster.members.reduce((a, b) => a.length <= b.length ? a : b);
    clusters.push({ centroid: Array.from(cluster.centroid), members: cluster.members, label: cluster.label });
  }

  return clusters;
}

// Get cache stats for reporting.
function getCacheStats() {
  const cache = loadCache();
  return {
    entries: Object.keys(cache).length,
    model: OLLAMA_MODEL,
    url: OLLAMA_URL,
  };
}

// Clear the embedding cache.
function clearCache() {
  _cache = {};
  saveCache();
}

module.exports = {
  embedText,
  cosineSimilarity,
  clusterErrors,
  isOllamaAvailable,
  resetAvailabilityCache,
  getCacheStats,
  clearCache,
  textHash,
  OLLAMA_URL,
  OLLAMA_MODEL,
};
