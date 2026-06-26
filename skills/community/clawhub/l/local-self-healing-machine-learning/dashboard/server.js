// dashboard/server.js — Tiny HTTP server for LSHML dashboard
const http = require('http');
const fs = require('fs');
const path = require('path');

const SKILL_ROOT = path.resolve(__dirname, '..');
const MEMORY_DIR = path.join(SKILL_ROOT, 'memory');
const GEP_DIR = path.join(SKILL_ROOT, 'assets', 'gep');
const HTML_PATH = path.join(__dirname, 'index.html');

function readJsonSafe(p) {
  try {
    if (!fs.existsSync(p)) return null;
    const raw = fs.readFileSync(p, 'utf8');
    if (!raw.trim()) return null;
    return JSON.parse(raw);
  } catch { return null; }
}

function readJsonlSafe(p, limit) {
  try {
    if (!fs.existsSync(p)) return [];
    const raw = fs.readFileSync(p, 'utf8');
    const lines = raw.split('\n').filter(l => l.trim());
    const parsed = [];
    for (const line of lines) {
      try { parsed.push(JSON.parse(line)); } catch {}
    }
    if (limit && limit > 0) return parsed.slice(-limit);
    return parsed;
  } catch { return []; }
}

function fileSizeSafe(p) {
  try {
    if (!fs.existsSync(p)) return 0;
    return fs.statSync(p).size;
  } catch { return 0; }
}

function gatherData() {
  const pkg = readJsonSafe(path.join(SKILL_ROOT, 'package.json')) || {};

  // Memory files
  const feedbackAll = readJsonlSafe(path.join(MEMORY_DIR, 'feedback.jsonl'));
  const knowledge = readJsonSafe(path.join(MEMORY_DIR, 'knowledge.json')) || { lessons: [] };
  const predictor = readJsonSafe(path.join(MEMORY_DIR, 'predictor.json'));
  const clusters = readJsonSafe(path.join(MEMORY_DIR, 'cluster-registry.json')) || [];
  const embeddingsCacheSize = fileSizeSafe(path.join(MEMORY_DIR, 'embeddings-cache.json'));

  // GEP assets
  const genesData = readJsonSafe(path.join(GEP_DIR, 'genes.json')) || { genes: [] };
  const capsulesData = readJsonSafe(path.join(GEP_DIR, 'capsules.json')) || { capsules: [] };
  const failedCapsulesData = readJsonSafe(path.join(GEP_DIR, 'failed_capsules.json')) || { failed_capsules: [] };
  const eventsAll = readJsonlSafe(path.join(GEP_DIR, 'events.jsonl'));
  const recentEvents = eventsAll.slice(-10);

  // Env settings
  const env = {
    EVOLVE_STRATEGY: process.env.EVOLVE_STRATEGY || '(not set)',
    OLLAMA_URL: process.env.OLLAMA_URL || '(not set)',
    OLLAMA_EMBED_MODEL: process.env.OLLAMA_EMBED_MODEL || '(not set)',
  };

  return {
    version: pkg.version || 'unknown',
    name: pkg.name || 'lshml',
    timestamp: new Date().toISOString(),
    feedback: feedbackAll,
    knowledge,
    predictor,
    clusters,
    embeddingsCacheSize,
    genes: genesData.genes || [],
    capsules: capsulesData.capsules || [],
    failedCapsules: failedCapsulesData.failed_capsules || [],
    recentEvents,
    totalEvents: eventsAll.length,
    env,
  };
}

function startServer(port) {
  const server = http.createServer((req, res) => {
    if (req.method === 'GET' && req.url === '/api/data') {
      res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
      res.end(JSON.stringify(gatherData()));
    } else if (req.method === 'GET' && (req.url === '/' || req.url === '/index.html')) {
      try {
        const html = fs.readFileSync(HTML_PATH, 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(html);
      } catch (e) {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Dashboard HTML not found: ' + e.message);
      }
    } else {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('Not found');
    }
  });

  server.listen(port, () => {
    console.log(`[LSHML Dashboard] Running at http://localhost:${port}`);
    console.log(`[LSHML Dashboard] API endpoint: http://localhost:${port}/api/data`);
    console.log('[LSHML Dashboard] Press Ctrl+C to stop.');
  });

  return server;
}

module.exports = { startServer, gatherData };
