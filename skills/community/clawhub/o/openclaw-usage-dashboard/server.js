#!/usr/bin/env node
/**
 * OpenClaw Usage Dashboard v2.0 — Local Server
 * Serves dashboard.html and provides secure API endpoints for log parsing.
 * 
 * Usage: node server.js [--port 7842] [--host 127.0.0.1]
 * 
 * Security: All data stays local. No external network calls.
 */

'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
// child_process is used ONLY for fixed, hardcoded system commands:
//   - vm_stat, memory_pressure (macOS RAM info)
//   - df (Linux/macOS disk free)
//   - powershell / wmic (Windows disk free)
//   - openclaw version (version string)
//   - xdg-open / open / start (auto-open browser — uses spawn with array args, NO shell)
// No user input is ever interpolated into any shell command.
// All calls have explicit timeouts and are wrapped in try/catch.
const { execSync, spawn } = require('child_process');

// ─── CONFIG ────────────────────────────────────────────────────────────────
const DEFAULT_PORT = 7842;
const DEFAULT_HOST = '127.0.0.1';
const MAX_SESSIONS = 2000;
const MAX_DAYS = 365;
const MEMORY_BUDGET_MB = 100;

// Parse CLI args
const args = process.argv.slice(2);
const portArg = args.indexOf('--port');
const hostArg = args.indexOf('--host');
const PORT = portArg !== -1 ? parseInt(args[portArg + 1]) : DEFAULT_PORT;
const HOST = hostArg !== -1 ? args[hostArg + 1] : DEFAULT_HOST;

// OpenClaw home directory (cross-platform)
function getOpenClawHome() {
  if (process.platform === 'win32') {
    return path.join(process.env.USERPROFILE || os.homedir(), '.openclaw');
  }
  return path.join(os.homedir(), '.openclaw');
}

const OPENCLAW_HOME = getOpenClawHome();
const AGENTS_DIR = path.join(OPENCLAW_HOME, 'agents');

// ─── SECRETS SANITIZATION ─────────────────────────────────────────────────
const SECRET_PATTERNS = [
  /\bsk-ant-[a-zA-Z0-9_-]{20,}\b/g,
  /\bsk-proj-[a-zA-Z0-9_-]{20,}\b/g,
  /\bsk-kimi-[a-zA-Z0-9_-]{20,}\b/g,
  /\bsk-[a-zA-Z0-9_-]{32,}\b/g,
  /Bearer\s+[a-zA-Z0-9_\-\.]{32,}/gi,
  /([A-Z_]{2,}(?:_API)?_KEY|TOKEN|PASSWORD|SECRET)\s*[:=]\s*["']?[^\s"',\n]{8,}["']?/gi,
  /\bsbp_[a-zA-Z0-9]{20,}\b/g,
  /\bntn_[a-zA-Z0-9_-]{20,}\b/g,
  /eyJ[A-Za-z0-9_-]{20,}/g,
  /AIzaSy[A-Za-z0-9_-]{20,}/g,
];

const RISKY_FIELDS = new Set(['solutionCode', 'systemPrompt', 'errorOutput', 'rawResponse', 'envVars', 'credentials', 'headers']);

function sanitizeText(text) {
  if (typeof text !== 'string') return text;
  let s = text;
  for (const pat of SECRET_PATTERNS) {
    s = s.replace(pat, '[REDACTED]');
  }
  // Truncate very long strings
  if (s.length > 2000) s = s.substring(0, 2000) + ' [truncated]';
  return s;
}

function sanitizeEntry(entry) {
  // We only expose safe aggregated metrics — never raw message content
  // This function is used to clean config data if needed
  if (typeof entry !== 'object' || entry === null) return entry;
  const out = {};
  for (const [k, v] of Object.entries(entry)) {
    if (RISKY_FIELDS.has(k)) continue;
    if (typeof v === 'string') {
      out[k] = sanitizeText(v);
    } else if (typeof v === 'object' && v !== null) {
      out[k] = sanitizeEntry(v);
    } else {
      out[k] = v;
    }
  }
  return out;
}

// ─── LOG PARSING ──────────────────────────────────────────────────────────
function parseSessionFile(filePath) {
  const result = {
    sessionId: null,
    agentId: null,
    timestamp: null,
    endTime: null,
    models: {},        // modelId -> { requests, inputTokens, outputTokens, cacheRead, cacheWrite }
    messageCount: 0,
    durationMs: 0,
    rateLimits: {},    // modelId -> { limitRequests, usedRequests, limitTokens, usedTokens }
  };

  let content;
  try {
    const stat = fs.statSync(filePath);
    // Memory budget: skip files > 10MB individually
    if (stat.size > 10 * 1024 * 1024) return null;
    content = fs.readFileSync(filePath, 'utf8');
  } catch (e) {
    return null;
  }

  const lines = content.split('\n');
  let firstTimestamp = null;
  let lastTimestamp = null;

  // Extract agent from path
  const pathParts = filePath.split(path.sep);
  const agentsIdx = pathParts.indexOf('agents');
  if (agentsIdx !== -1 && agentsIdx + 1 < pathParts.length) {
    result.agentId = pathParts[agentsIdx + 1];
  }

  for (const line of lines) {
    if (!line.trim()) continue;
    let entry;
    try {
      entry = JSON.parse(line);
    } catch (e) {
      continue; // Skip malformed lines gracefully
    }

    const type = entry.type;
    const ts = entry.timestamp ? new Date(entry.timestamp).getTime() : null;

    if (ts) {
      if (!firstTimestamp || ts < firstTimestamp) firstTimestamp = ts;
      if (!lastTimestamp || ts > lastTimestamp) lastTimestamp = ts;
    }

    if (type === 'session') {
      result.sessionId = entry.id;
      result.timestamp = entry.timestamp;
    }

    if (type === 'message') {
      const msg = entry.message || {};
      const role = msg.role;
      const usage = msg.usage;
      const model = msg.model;

      if (role === 'assistant' && usage && model) {
        result.messageCount++;
        if (!result.models[model]) {
          result.models[model] = { requests: 0, inputTokens: 0, outputTokens: 0, cacheRead: 0, cacheWrite: 0 };
        }
        result.models[model].requests++;
        result.models[model].inputTokens += (usage.input || 0);
        result.models[model].outputTokens += (usage.output || 0);
        result.models[model].cacheRead += (usage.cacheRead || 0);
        result.models[model].cacheWrite += (usage.cacheWrite || 0);
      }

      // Extract rate limit data from tool results if present
      if (role === 'toolResult') {
        const content = msg.content || [];
        for (const item of (Array.isArray(content) ? content : [])) {
          if (item && item.type === 'text' && typeof item.text === 'string') {
            // Look for rate-limit headers in curl output
            const rlReq = item.text.match(/anthropic-ratelimit-requests-remaining:\s*(\d+)/i);
            const rlTok = item.text.match(/anthropic-ratelimit-tokens-remaining:\s*(\d+)/i);
            const rlReqLimit = item.text.match(/anthropic-ratelimit-requests-limit:\s*(\d+)/i);
            const rlTokLimit = item.text.match(/anthropic-ratelimit-tokens-limit:\s*(\d+)/i);
            if (rlReq || rlTok) {
              // Associate with the most recent model
              const lastModel = Object.keys(result.models).pop();
              if (lastModel) {
                if (!result.rateLimits[lastModel]) {
                  result.rateLimits[lastModel] = {};
                }
                if (rlReqLimit) result.rateLimits[lastModel].limitRequests = parseInt(rlReqLimit[1]);
                if (rlReq) result.rateLimits[lastModel].usedRequests = parseInt(rlReq[1]);
                if (rlTokLimit) result.rateLimits[lastModel].limitTokens = parseInt(rlTokLimit[1]);
                if (rlTok) result.rateLimits[lastModel].usedTokens = parseInt(rlTok[1]);
              }
            }
          }
        }
      }
    }
  }

  if (firstTimestamp) result.timestamp = result.timestamp || new Date(firstTimestamp).toISOString();
  if (firstTimestamp && lastTimestamp) result.durationMs = lastTimestamp - firstTimestamp;

  return result;
}

// ─── DATA AGGREGATION ─────────────────────────────────────────────────────
function getAllSessionFiles() {
  const files = [];
  try {
    const agentDirs = fs.readdirSync(AGENTS_DIR).filter(d => {
      try {
        return fs.statSync(path.join(AGENTS_DIR, d)).isDirectory();
      } catch { return false; }
    });

    for (const agentId of agentDirs) {
      const sessionsDir = path.join(AGENTS_DIR, agentId, 'sessions');
      try {
        const sessionFiles = fs.readdirSync(sessionsDir)
          .filter(f => f.endsWith('.jsonl'))
          .map(f => ({
            filePath: path.join(sessionsDir, f),
            agentId,
            mtime: fs.statSync(path.join(sessionsDir, f)).mtimeMs,
          }));
        files.push(...sessionFiles);
      } catch { /* No sessions dir */ }
    }
  } catch { /* No agents dir */ }

  return files.sort((a, b) => b.mtime - a.mtime); // Newest first
}

function computeDashboardData(periodMs) {
  const now = Date.now();
  const cutoff = now - periodMs;
  const daysCutoff = now - MAX_DAYS * 24 * 60 * 60 * 1000;
  const effectiveCutoff = Math.max(cutoff, daysCutoff);

  const allFiles = getAllSessionFiles();
  
  // Estimate memory usage and limit
  let estimatedBytesProcessed = 0;
  const maxBytes = MEMORY_BUDGET_MB * 1024 * 1024;

  // Aggregate data
  const models = {};          // modelId -> { requests, inputTokens, outputTokens, cacheRead, cacheWrite }
  const sessions = [];        // { sessionId, agentId, timestamp, durationMs, models }
  const timeline = {};        // timestamp (bucketed) -> { total, per model }
  const rateLimits = {};      // modelId -> latest rate limit data
  let oldestSession = null;
  let newestSession = null;
  let processedCount = 0;
  const agentStats = {};      // agentId -> session count
  const hourlyActivity = new Array(24).fill(0); // Hour 0-23 activity counts
  const dailyActivity = {};   // YYYY-MM-DD -> count
  let totalDurationMs = 0;
  let sessionCount = 0;

  for (const { filePath, agentId, mtime } of allFiles) {
    if (processedCount >= MAX_SESSIONS) break;
    if (mtime < effectiveCutoff) continue;
    if (estimatedBytesProcessed > maxBytes) break;

    try {
      const stat = fs.statSync(filePath);
      estimatedBytesProcessed += stat.size;
    } catch { continue; }

    const parsed = parseSessionFile(filePath);
    if (!parsed) continue;

    const sessionTs = parsed.timestamp ? new Date(parsed.timestamp).getTime() : mtime;
    if (sessionTs < effectiveCutoff) continue;

    processedCount++;
    sessionCount++;

    if (!oldestSession || sessionTs < oldestSession) oldestSession = sessionTs;
    if (!newestSession || sessionTs > newestSession) newestSession = sessionTs;

    // Agent stats
    agentStats[agentId] = (agentStats[agentId] || 0) + 1;

    // Session duration
    totalDurationMs += parsed.durationMs || 0;

    // Hourly activity
    const hour = new Date(sessionTs).getHours();
    hourlyActivity[hour]++;

    // Daily activity
    const day = new Date(sessionTs).toISOString().substring(0, 10);
    dailyActivity[day] = (dailyActivity[day] || 0) + 1;

    // Per-model aggregation
    for (const [modelId, usage] of Object.entries(parsed.models)) {
      if (!models[modelId]) {
        models[modelId] = { requests: 0, inputTokens: 0, outputTokens: 0, cacheRead: 0, cacheWrite: 0 };
      }
      models[modelId].requests += usage.requests;
      models[modelId].inputTokens += usage.inputTokens;
      models[modelId].outputTokens += usage.outputTokens;
      models[modelId].cacheRead += usage.cacheRead;
      models[modelId].cacheWrite += usage.cacheWrite;

      // Timeline bucketing — bucket by period
      const bucketMs = getBucketMs(periodMs);
      const bucket = Math.floor(sessionTs / bucketMs) * bucketMs;
      if (!timeline[bucket]) timeline[bucket] = { total: 0, agents: {} };
      timeline[bucket].total += usage.requests;
      if (!timeline[bucket][modelId]) timeline[bucket][modelId] = 0;
      timeline[bucket][modelId] += usage.requests;

      // Agent breakdown within bucket
      if (!timeline[bucket].agents[agentId]) timeline[bucket].agents[agentId] = {};
      if (!timeline[bucket].agents[agentId][modelId]) timeline[bucket].agents[agentId][modelId] = 0;
      timeline[bucket].agents[agentId][modelId] += usage.requests;
    }

    // Rate limits (keep latest)
    for (const [modelId, rl] of Object.entries(parsed.rateLimits)) {
      rateLimits[modelId] = rl;
    }

    sessions.push({
      sessionId: parsed.sessionId,
      agentId,
      timestamp: sessionTs,
      durationMs: parsed.durationMs,
      models: Object.keys(parsed.models),
    });
  }

  // Total tokens across all models
  let totalRequests = 0, totalInput = 0, totalOutput = 0, totalCacheRead = 0, totalCacheWrite = 0;
  for (const m of Object.values(models)) {
    totalRequests += m.requests;
    totalInput += m.inputTokens;
    totalOutput += m.outputTokens;
    totalCacheRead += m.cacheRead;
    totalCacheWrite += m.cacheWrite;
  }

  // Cache hit ratio
  const totalRead = totalInput + totalCacheRead;
  const cacheHitRatio = totalRead > 0 ? Math.round((totalCacheRead / totalRead) * 100) : 0;

  // Avg prompt size (tokens)
  const avgPromptSize = totalRequests > 0 ? Math.round(totalInput / totalRequests) : 0;

  // Avg session duration
  const avgSessionDurationMs = sessionCount > 0 ? Math.round(totalDurationMs / sessionCount) : 0;

  // Data range in days
  const dataRangeDays = oldestSession && newestSession
    ? (newestSession - oldestSession) / (1000 * 60 * 60 * 24)
    : 0;

  return {
    generatedAt: new Date().toISOString(),
    processedSessions: processedCount,
    dataRangeDays,
    oldestSession,
    newestSession,
    models,
    totalStats: { totalRequests, totalInput, totalOutput, totalCacheRead, totalCacheWrite },
    timeline: Object.entries(timeline)
      .map(([ts, data]) => ({ ts: parseInt(ts), ...data }))
      .sort((a, b) => a.ts - b.ts),
    rateLimits,
    sessions: sessions.slice(0, 100), // Sample for UI
    sessionCount,
    agentStats,
    hourlyActivity,
    dailyActivity,
    efficiency: { cacheHitRatio, avgPromptSize, avgSessionDurationMs },
  };
}

function getBucketMs(periodMs) {
  // Bucket resolution based on period
  if (periodMs <= 60 * 60 * 1000) return 5 * 60 * 1000;       // Hour: 5-min buckets
  if (periodMs <= 24 * 60 * 60 * 1000) return 60 * 60 * 1000;  // Day: 1-hour buckets
  if (periodMs <= 7 * 24 * 60 * 60 * 1000) return 4 * 60 * 60 * 1000; // Week: 4-hour buckets
  if (periodMs <= 30 * 24 * 60 * 60 * 1000) return 24 * 60 * 60 * 1000; // Month: daily
  return 7 * 24 * 60 * 60 * 1000; // Year: weekly
}

// ─── SYSTEM INFO ──────────────────────────────────────────────────────────
function getSystemInfo() {
  const totalMem = os.totalmem();
  // On macOS, use vm_stat for app memory (excludes OrbStack/VM balloon pages)
  let usedMem = totalMem - os.freemem();
  let memPressure = null;
  if (process.platform === 'darwin') {
    try {
      const vmstat = execSync('vm_stat', { timeout: 2000, encoding: 'utf8' });
      const pageSizeMatch = vmstat.match(/page size of (\d+) bytes/);
      const pageSize = pageSizeMatch ? parseInt(pageSizeMatch[1]) : 16384;
      const active   = parseInt((vmstat.match(/Pages active:\s+(\d+)/) || [])[1] || 0);
      const wired    = parseInt((vmstat.match(/Pages wired down:\s+(\d+)/) || [])[1] || 0);
      const compressed = parseInt((vmstat.match(/Pages occupied by compressor:\s+(\d+)/) || [])[1] || 0);
      const appBytes = (active + wired + compressed) * pageSize;
      if (appBytes > 0) usedMem = appBytes;
    } catch {}
    try {
      const pOut = execSync('memory_pressure', { timeout: 2000, encoding: 'utf8' });
      if (pOut.includes('System-wide memory free percentage')) {
        if (pOut.toLowerCase().includes('critical')) memPressure = 'critical';
        else if (pOut.toLowerCase().includes('warn')) memPressure = 'warn';
        else memPressure = 'normal';
      }
    } catch {}
  }
  let diskFree = null;
  let version = 'Unknown';

  try {
    if (process.platform === 'win32') {
      // Windows: try PowerShell (works on Win 10+, Win 11 where wmic is removed)
      try {
        const out = execSync('powershell -NoProfile -Command "(Get-PSDrive C).Free"', { timeout: 5000, encoding: 'utf8' });
        diskFree = parseInt(out.trim()) || null;
      } catch {
        // Fallback to wmic for older Windows
        try {
          const out = execSync('wmic logicaldisk where "DeviceID=\'C:\'" get FreeSpace /format:value', { timeout: 3000, encoding: 'utf8' });
          const match = out.match(/FreeSpace=(\d+)/);
          diskFree = match ? parseInt(match[1]) : null;
        } catch { /* ignore */ }
      }
    } else {
      // Use spawnSync to avoid shell interpolation of home path
      const { spawnSync } = require('child_process');
      const home = os.homedir();
      const dfResult = spawnSync('df', ['-k', home], { timeout: 3000, encoding: 'utf8' });
      const dfLines = (dfResult.stdout || '').trim().split('\n');
      const parts = (dfLines[dfLines.length - 1] || '').trim().split(/\s+/);
      if (parts.length >= 4) diskFree = parseInt(parts[3]) * 1024;
    }
  } catch { /* ignore */ }

  try {
    version = execSync('openclaw version', { timeout: 3000, encoding: 'utf8' })
      .trim().split('\n')[0].replace(/^openclaw\s+/i, '').trim() || 'Unknown';
  } catch {
    try {
      version = execSync('openclaw --version', { timeout: 3000, encoding: 'utf8' })
        .trim().split('\n')[0].replace(/^openclaw\s+/i, '').trim() || 'Unknown';
    } catch { version = 'Unknown'; }
  }

  return {
    ramUsedMB: Math.round(usedMem / 1024 / 1024),
    ramTotalMB: Math.round(totalMem / 1024 / 1024),
    ramFreeMB: Math.round((totalMem - usedMem) / 1024 / 1024),
    memPressure,
    diskFreeGB: diskFree ? Math.round(diskFree / 1024 / 1024 / 1024 * 10) / 10 : null,
    uptimeSeconds: Math.round(os.uptime()),
    platform: process.platform,
    arch: os.arch(),
    nodeVersion: process.version,
    version,
  };
}


function getConfig() {
  const configPath = path.join(OPENCLAW_HOME, 'openclaw.json');
  try {
    const raw = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(raw);
    // Extract ONLY model metadata — never credentials
    const providers = config.models?.providers || {};
    const modelList = [];
    for (const [providerId, pData] of Object.entries(providers)) {
      for (const model of (pData.models || [])) {
        modelList.push({
          id: model.id,
          name: model.name || model.id,
          provider: providerId,
          contextWindow: model.contextWindow,
          maxTokens: model.maxTokens,
        });
      }
    }

    // Extract primary & fallback model from agents.defaults
    const agentsDefaults = config.agents?.defaults || {};
    const primaryModel = agentsDefaults.model?.primary || null;
    const fallbackModels = agentsDefaults.model?.fallbacks || [];
    const fallbackModel = fallbackModels[0] || null;

    // Extract alias map for display names
    const modelAliases = agentsDefaults.models || {};

    // Build a helper to get short alias for a model id
    const getAlias = (id) => {
      if (!id) return null;
      if (modelAliases[id]?.alias) return modelAliases[id].alias;
      return id.split('/').pop();
    };

    // Extract per-agent models from agents.list
    const agentModels = {};
    for (const agent of (config.agents?.list || [])) {
      if (agent.id && agent.model) {
        agentModels[agent.id] = agent.model;
      }
    }

    return {
      models: modelList,
      primaryModel,
      fallbackModel,
      primaryModelAlias: getAlias(primaryModel),
      fallbackModelAlias: getAlias(fallbackModel),
      agentModels,
    };
  } catch (e) {
    return { models: [] };
  }
}

// ─── HTTP SERVER ───────────────────────────────────────────────────────────
const PERIOD_MAP = {
  hour: 60 * 60 * 1000,
  day: 24 * 60 * 60 * 1000,
  week: 7 * 24 * 60 * 60 * 1000,
  month: 30 * 24 * 60 * 60 * 1000,
  year: 365 * 24 * 60 * 60 * 1000,
};

const DASHBOARD_FILE = path.join(__dirname, 'dashboard.html');

function jsonResponse(res, data, status = 200) {
  const body = JSON.stringify(data);
  res.writeHead(status, {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(body),
    'Cache-Control': 'no-cache',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
  });
  res.end(body);
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const pathname = url.pathname;

  // CORS — localhost only
  res.setHeader('Access-Control-Allow-Origin', `http://${HOST}:${PORT}`);

  // Serve dashboard HTML
  if (pathname === '/' || pathname === '/dashboard.html') {
    try {
      const html = fs.readFileSync(DASHBOARD_FILE, 'utf8');
      res.writeHead(200, {
        'Content-Type': 'text/html; charset=utf-8',
        'Content-Security-Policy': [
          "default-src 'self' 'unsafe-inline'",
          "img-src 'self' data:",
          "font-src 'self' data:",
          "connect-src 'self'",
          "frame-ancestors 'none'",
        ].join('; '),
        'X-Frame-Options': 'DENY',
        'X-Content-Type-Options': 'nosniff',
      });
      res.end(html);
    } catch (e) {
      res.writeHead(404);
      res.end('dashboard.html not found');
    }
    return;
  }

  // API: /api/stats?period=day
  if (pathname === '/api/stats') {
    const periodKey = url.searchParams.get('period') || 'day';
    const periodMs = PERIOD_MAP[periodKey] || PERIOD_MAP.day;
    try {
      const data = computeDashboardData(periodMs);
      jsonResponse(res, data);
    } catch (e) {
      jsonResponse(res, { error: e.message }, 500);
    }
    return;
  }

  // API: /api/system
  if (pathname === '/api/system') {
    try {
      jsonResponse(res, getSystemInfo());
    } catch (e) {
      jsonResponse(res, { error: e.message }, 500);
    }
    return;
  }

  // API: /api/config
  if (pathname === '/api/config') {
    try {
      jsonResponse(res, getConfig());
    } catch (e) {
      jsonResponse(res, { error: e.message }, 500);
    }
    return;
  }

  // 404
  res.writeHead(404);
  res.end('Not found');
});

server.listen(PORT, HOST, () => {
  console.log(`\n🦞 OpenClaw Usage Dashboard v2.0`);
  console.log(`   Server running at http://${HOST}:${PORT}`);
  console.log(`   Data source: ${OPENCLAW_HOME}`);
  console.log(`   Press Ctrl+C to stop\n`);
  
  // Auto-open browser (optional) — uses spawn with array args (no shell, no injection risk)
  if (process.argv.includes('--open')) {
    const url = `http://localhost:${PORT}`;
    const cmd = process.platform === 'win32' ? ['cmd', ['/c', 'start', url]]
              : process.platform === 'darwin' ? ['open', [url]]
              : ['xdg-open', [url]];
    try { spawn(cmd[0], cmd[1], { detached: true, stdio: 'ignore' }).unref(); } catch {}
  }
});

server.on('error', (e) => {
  if (e.code === 'EADDRINUSE') {
    console.error(`\n❌ Port ${PORT} is already in use. Try: node server.js --port 7843\n`);
  } else {
    console.error(`\n❌ Server error: ${e.message}\n`);
  }
  process.exit(1);
});
