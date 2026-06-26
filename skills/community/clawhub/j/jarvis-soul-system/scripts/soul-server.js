#!/usr/bin/env node
/**
 * SOUL.md File Server
 * Serves the soul-editor and handles save requests to agent directories
 * 
 * Usage: node soul-server.js [--port 3000]
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const AGENTS_DIR = 'C:\\Users\\Administrator\\.openclaw\\agents';
const PORT = parseInt(process.argv[2]) || 3000;

const MIME_TYPES = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.md': 'text/markdown'
};

const server = http.createServer((req, res) => {
  const parsed = url.parse(req.url, true);
  const pathname = parsed.pathname;

  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // API: Health check
  if (pathname === '/api/health' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', port: PORT, agents_dir: AGENTS_DIR }));
    return;
  }

  // API: List agents
  if (pathname === '/api/agents' && req.method === 'GET') {
    try {
      const agents = fs.readdirSync(AGENTS_DIR).filter(name => {
        const soulPath = path.join(AGENTS_DIR, name, 'SOUL.md');
        return fs.statSync(soulPath).isFile();
      });
      const result = {};
      for (const name of agents) {
        const soulPath = path.join(AGENTS_DIR, name, 'SOUL.md');
        const content = fs.readFileSync(soulPath, 'utf-8');
        // Extract personality from content
        const personaMatch = content.match(/\*\*([^*]+)\*\*/);
        result[name] = {
          personality: personaMatch ? personaMatch[1] : '(unknown)',
          updated: fs.statSync(soulPath).mtime.toISOString()
        };
      }
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(result));
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  // API: Get single agent SOUL.md
  if (pathname.startsWith('/api/agents/') && req.method === 'GET') {
    const name = pathname.split('/')[3];
    const soulPath = path.join(AGENTS_DIR, name, 'SOUL.md');
    try {
      const content = fs.readFileSync(soulPath, 'utf-8');
      res.writeHead(200, { 'Content-Type': 'text/markdown' });
      res.end(content);
    } catch (e) {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Agent not found' }));
    }
    return;
  }

  // API: Save agent SOUL.md
  if (pathname.startsWith('/api/agents/') && req.method === 'POST') {
    const name = pathname.split('/')[3];
    const soulPath = path.join(AGENTS_DIR, name, 'SOUL.md');
    
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const data = JSON.parse(body);
        fs.writeFileSync(soulPath, data.content, 'utf-8');
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true, path: soulPath }));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
    });
    return;
  }

  // Serve static files from canvas dir
  const canvasDir = path.join(process.env.APPDATA, '.openclaw', 'canvas');
  let filePath = path.join(canvasDir, pathname === '/' ? 'soul-editor.html' : pathname);
  
  // Security: stay within canvas dir
  if (!filePath.startsWith(canvasDir)) {
    res.writeHead(403);
    res.end('Forbidden');
    return;
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('Not found: ' + pathname);
      return;
    }
    const ext = path.extname(filePath);
    res.writeHead(200, { 'Content-Type': MIME_TYPES[ext] || 'text/plain' });
    res.end(data);
  });
});

server.listen(PORT, () => {
  console.log(`SOUL Editor server running at http://localhost:${PORT}`);
  console.log(`Agents directory: ${AGENTS_DIR}`);
  console.log('Press Ctrl+C to stop');
});