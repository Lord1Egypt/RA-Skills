#!/usr/bin/env node
/**
 * Local Compaction Proxy
 *
 * Intercepts Anthropic Messages API calls from Pi Agent Runtime,
 * performs local summarization via ollama/qwen3.5:9b when the
 * conversation exceeds 65% of the model's context window,
 * then forwards the compacted request to the real LLM provider.
 *
 * Upstream target is read from COMPACTION_PROXY_UPSTREAM env var,
 * falling back to the kimi-coding endpoint.
 */

'use strict';

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

// ─── Configuration ────────────────────────────────────────────────────────────

const PORT = parseInt(process.env.COMPACTION_PROXY_PORT || '19000', 10);

// Real LLM provider upstream (legacy single-upstream fallback)
const UPSTREAM_BASE_URL = (
  process.env.COMPACTION_PROXY_UPSTREAM || 'https://api.kimi.com/coding'
).replace(/\/$/, '');
const UPSTREAM_API_KEY = process.env.UPSTREAM_API_KEY || '';

// Multi-upstream routing table: loaded from routes.json, keyed by model-ID prefix
const ROUTES_FILE = process.env.COMPACTION_ROUTES_FILE ||
  path.join(process.env.HOME || '/tmp', '.openclaw', 'compaction-proxy', 'routes.json');
let UPSTREAM_ROUTES = {};
try {
  UPSTREAM_ROUTES = JSON.parse(fs.readFileSync(ROUTES_FILE, 'utf8'));
} catch (_) { /* file absent → fall back to env-var single-upstream */ }

// ollama config
const OLLAMA_BASE_URL = process.env.OLLAMA_BASE_URL || 'http://127.0.0.1:11434';
const OLLAMA_MODEL = process.env.COMPACTION_OLLAMA_MODEL || 'qwen3.5:9b-q4_K_M';
const OLLAMA_TIMEOUT_MS = parseInt(process.env.COMPACTION_OLLAMA_TIMEOUT_MS || '120000', 10);

// Compaction trigger: fraction of contextWindow at which proxy intervenes.
// Set high (0.85) to let LLM prefix cache keep hitting; only compact near the actual limit.
const COMPACT_THRESHOLD = parseFloat(process.env.COMPACTION_THRESHOLD || '0.85');

// Already-compacted conversation: even higher bar before re-compacting
const RECOMPACT_THRESHOLD = parseFloat(process.env.RECOMPACT_THRESHOLD || '0.92');

// Circuit breaker: when an upstream returns 402, skip it for this many ms (default 5 min)
const CIRCUIT_BREAKER_TTL_MS = parseInt(process.env.CIRCUIT_BREAKER_TTL_MS || '300000', 10);
const upstreamCircuitBreaker = new Map(); // baseUrl → expiry timestamp

// Minimum summary length (chars) to accept ollama output as usable
const MIN_SUMMARY_LENGTH = parseInt(process.env.MIN_SUMMARY_LENGTH || '100', 10);

// How many recent turns (user+assistant pairs) to preserve verbatim
const RECENT_TURNS_PRESERVE = parseInt(process.env.COMPACTION_RECENT_TURNS || '10', 10);

// Known context windows by model ID substring (lower-case match)
const CONTEXT_WINDOWS = {
  'k2p5': 262144,
  'kimi': 262144,
  'claude-opus': 200000,
  'claude-sonnet': 200000,
  'claude-haiku': 200000,
};

// Log file
const LOG_FILE = process.env.COMPACTION_LOG_FILE ||
  path.join(process.env.HOME || '/tmp', '.openclaw', 'logs', 'compaction-proxy.log');

// ─── Logging ──────────────────────────────────────────────────────────────────

const logStream = (() => {
  try {
    fs.mkdirSync(path.dirname(LOG_FILE), { recursive: true });
    return fs.createWriteStream(LOG_FILE, { flags: 'a' });
  } catch (e) {
    return process.stderr;
  }
})();

function log(level, msg, extra) {
  const line = JSON.stringify({
    ts: new Date().toISOString(),
    level,
    msg,
    ...(extra !== undefined ? { data: extra } : {}),
  });
  logStream.write(line + '\n');
  if (process.env.COMPACTION_PROXY_VERBOSE) process.stderr.write(line + '\n');
}

// ─── Token estimation ─────────────────────────────────────────────────────────

/**
 * Rough token estimate: characters / 3.5 (good enough for threshold decisions).
 */
function estimateTokens(text) {
  return Math.ceil((text || '').length / 3.5);
}

function estimateMessagesTokens(messages) {
  let total = 0;
  for (const msg of messages) {
    if (typeof msg.content === 'string') {
      total += estimateTokens(msg.content);
    } else if (Array.isArray(msg.content)) {
      for (const block of msg.content) {
        if (block.type === 'text') total += estimateTokens(block.text);
        else total += 100; // rough estimate for non-text blocks
      }
    }
    total += 4; // per-message overhead
  }
  return total;
}

// ─── Context window lookup ────────────────────────────────────────────────────

function getContextWindow(modelId) {
  if (!modelId) return 200000;
  const lower = modelId.toLowerCase();
  for (const [key, val] of Object.entries(CONTEXT_WINDOWS)) {
    if (lower.includes(key)) return val;
  }
  return 200000; // conservative default
}

// ─── Upstream resolver ────────────────────────────────────────────────────────

/**
 * Resolve the upstream baseUrl + apiKey for a given model ID.
 * Model IDs follow the pattern "<provider-prefix>/<model-name>", e.g.
 *   "kimi-coding/k2p5"          → routes["kimi-coding"]
 *   "anthropic/claude-sonnet-4.6" → routes["anthropic"]
 * Falls back to the legacy UPSTREAM_BASE_URL / UPSTREAM_API_KEY env vars.
 */
function resolveUpstream(modelId) {
  const prefix = (modelId || '').split('/')[0];
  if (prefix && UPSTREAM_ROUTES[prefix]) return UPSTREAM_ROUTES[prefix];
  return { baseUrl: UPSTREAM_BASE_URL, apiKey: UPSTREAM_API_KEY };
}

// ─── Summarisation via ollama ─────────────────────────────────────────────────

// Max chars fed to ollama for summarisation (~23K tokens at 3.5 chars/token)
const OLLAMA_TRANSCRIPT_MAX_CHARS = parseInt(
  process.env.COMPACTION_TRANSCRIPT_MAX_CHARS || '80000', 10
);

/**
 * Serialize messages to a readable transcript for summarization.
 * Keeps the first portion and last portion when the full transcript
 * exceeds OLLAMA_TRANSCRIPT_MAX_CHARS, so ollama always gets a bounded input.
 */
function messagesToTranscript(messages) {
  const lines = messages.map((m) => {
    const role = m.role === 'assistant' ? '助手' : '用户';
    let content = '';
    if (typeof m.content === 'string') {
      content = m.content;
    } else if (Array.isArray(m.content)) {
      content = m.content
        .filter((b) => b.type === 'text')
        .map((b) => b.text)
        .join('\n');
    }
    return `${role}：${content}`;
  });

  const full = lines.join('\n\n');
  if (full.length <= OLLAMA_TRANSCRIPT_MAX_CHARS) return full;

  // Keep first 60% and last 40% of the budget, with an omission marker
  const headChars = Math.floor(OLLAMA_TRANSCRIPT_MAX_CHARS * 0.6);
  const tailChars = OLLAMA_TRANSCRIPT_MAX_CHARS - headChars;
  const omitted = full.length - headChars - tailChars;
  return (
    full.slice(0, headChars) +
    `\n\n[... ${omitted.toLocaleString()} characters omitted for brevity ...]\n\n` +
    full.slice(full.length - tailChars)
  );
}

/**
 * Call ollama chat API (non-streaming) with a timeout.
 * Uses /api/chat with think:false to disable Qwen3.5 thinking mode.
 * Returns the generated text or throws on error/timeout.
 */
function ollamaGenerate(prompt) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      model: OLLAMA_MODEL,
      messages: [{ role: 'user', content: prompt }],
      stream: false,
      think: false,
      options: { num_predict: 1500, temperature: 0.3 },
    });

    const url = new URL('/api/chat', OLLAMA_BASE_URL);
    const lib = url.protocol === 'https:' ? https : http;

    const req = lib.request(
      {
        hostname: url.hostname,
        port: url.port || (url.protocol === 'https:' ? 443 : 80),
        path: url.pathname,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body),
        },
      },
      (res) => {
        const chunks = [];
        res.on('data', (c) => chunks.push(c));
        res.on('end', () => {
          try {
            const parsed = JSON.parse(Buffer.concat(chunks).toString());
            resolve((parsed.message && parsed.message.content) || '');
          } catch (e) {
            reject(new Error('ollama response parse error: ' + e.message));
          }
        });
        res.on('error', reject);
      }
    );

    req.on('error', reject);

    const timer = setTimeout(() => {
      req.destroy();
      reject(new Error('ollama timeout'));
    }, OLLAMA_TIMEOUT_MS);

    req.on('close', () => clearTimeout(timer));
    req.write(body);
    req.end();
  });
}

/**
 * Summarise old messages using qwen3.5:9b.
 * Returns a summary string or throws.
 */
async function summariseMessages(messages) {
  const transcript = messagesToTranscript(messages);
  const prompt = `你是一个精炼的对话总结器。以下是需要压缩以节省上下文空间的部分对话记录。请生成一份密集、事实性的总结（800-1200字），严格保留以下内容：
- 所有做出的决定及其理由
- 所有编写、修改或审查的代码（包含文件名和关键代码片段）
- 遇到的所有错误及其解决过程
- 当前任务状态和待完成事项
- 提到的重要约束、需求或技术关键词

不要包含问候语、填充内容或元评论。只输出总结内容。

对话记录：
${transcript}

总结：`;

  return ollamaGenerate(prompt);
}

// ─── Compaction logic ─────────────────────────────────────────────────────────

/**
 * Attempt to compact messages array.
 * Returns compacted messages array, or the original array on failure.
 */
async function compactMessages(messages, contextWindow) {
  const threshold = Math.floor(contextWindow * COMPACT_THRESHOLD);
  const totalTokens = estimateMessagesTokens(messages);

  if (totalTokens <= threshold) {
    return { messages, compacted: false, totalTokens, threshold };
  }

  // ── Non-interference guard #1: already-compacted detection ──────────────────
  // If the conversation already contains a summary block from a previous compaction,
  // only re-compact when usage is very high (RECOMPACT_THRESHOLD), to avoid
  // repeatedly summarising summaries and losing context fidelity.
  const alreadyCompacted = messages.some((m) => {
    const text = typeof m.content === 'string' ? m.content
      : Array.isArray(m.content)
        ? m.content.filter((b) => b.type === 'text').map((b) => b.text).join('')
        : '';
    return text.includes('[对话总结]') || text.includes('[Conversation Summary]');
  });
  if (alreadyCompacted) {
    const reCompactThreshold = Math.floor(contextWindow * RECOMPACT_THRESHOLD);
    if (totalTokens <= reCompactThreshold) {
      log('info', 'skipping compaction: already compacted, below re-compact threshold',
        { totalTokens, reCompactThreshold });
      return { messages, compacted: false, totalTokens, threshold };
    }
  }

  log('info', 'compaction triggered', {
    totalTokens,
    threshold,
    contextWindow,
    messageCount: messages.length,
  });

  // Identify system messages (keep all) vs conversation turns
  const systemMessages = messages.filter((m) => m.role === 'system');
  const convMessages = messages.filter((m) => m.role !== 'system');

  // Keep the most recent N turns verbatim
  // A "turn" is one user message + one assistant message = 2 items
  const keepCount = Math.min(RECENT_TURNS_PRESERVE * 2, convMessages.length);
  const oldMessages = convMessages.slice(0, convMessages.length - keepCount);
  const recentMessages = convMessages.slice(convMessages.length - keepCount);

  if (oldMessages.length === 0) {
    log('warn', 'nothing to compact (all messages are recent)', {});
    return { messages, compacted: false, totalTokens, threshold };
  }

  let summaryText;
  try {
    summaryText = await summariseMessages(oldMessages);
    log('info', 'ollama summarisation complete', {
      inputMessages: oldMessages.length,
      summaryLength: summaryText.length,
    });
  } catch (err) {
    log('warn', 'ollama summarisation failed, skipping compaction', { error: err.message });
    return { messages, compacted: false, totalTokens, threshold, error: err.message };
  }

  // ── Non-interference guard #2: summary quality check ────────────────────────
  // A very short summary means ollama produced low-quality output; in that case
  // pass the original messages through so the upstream LLM can handle context itself.
  if (summaryText.length < MIN_SUMMARY_LENGTH) {
    log('warn', 'compaction skipped: summary too short (quality check failed)',
      { summaryLength: summaryText.length, minRequired: MIN_SUMMARY_LENGTH });
    return { messages, compacted: false, totalTokens, threshold };
  }

  // Build compacted message list:
  // [system messages..., summary-as-user+assistant exchange, recent messages...]
  const summaryTurn = [
    {
      role: 'user',
      content: '请在继续之前查看以下对话总结。',
    },
    {
      role: 'assistant',
      content: `[对话总结]\n\n${summaryText}`,
    },
  ];

  const compactedMessages = [...systemMessages, ...summaryTurn, ...recentMessages];

  const compactedTokens = estimateMessagesTokens(compactedMessages);
  log('info', 'compaction complete', {
    before: totalTokens,
    after: compactedTokens,
    reduction: totalTokens - compactedTokens,
  });

  return { messages: compactedMessages, compacted: true, totalTokens, compactedTokens };
}

// ─── HTTP proxying ────────────────────────────────────────────────────────────

/**
 * Forward a request to the upstream LLM provider.
 * Pipes the response (including SSE streams) directly back to the client.
 * @param {object} [upstream] - Optional { baseUrl, apiKey } override; falls back to env vars.
 */
function forwardRequest(upstreamPath, method, headers, bodyBuffer, clientRes, upstream) {
  return new Promise((resolve, reject) => {
    const { baseUrl, apiKey } = upstream || { baseUrl: UPSTREAM_BASE_URL, apiKey: UPSTREAM_API_KEY };

    // ── Circuit breaker check ────────────────────────────────────────────────
    // If this upstream recently returned 402 (quota exhausted), return 503 immediately
    // so OpenClaw can quickly fall through to the next provider without a network round-trip.
    const cbExpiry = upstreamCircuitBreaker.get(baseUrl);
    if (cbExpiry && Date.now() < cbExpiry) {
      log('info', 'circuit breaker open, skipping upstream', {
        baseUrl, retryAfter: Math.ceil((cbExpiry - Date.now()) / 1000) + 's',
      });
      clientRes.writeHead(503, { 'content-type': 'application/json' });
      clientRes.end(JSON.stringify({ error: { type: 'service_unavailable', message: 'upstream quota exhausted (circuit open)' } }));
      resolve();
      return;
    }

    // Strip leading slash so the path is relative to the base URL's path prefix
    // e.g. base=https://api.kimi.com/coding/  + v1/messages → .../coding/v1/messages
    const base = baseUrl.endsWith('/') ? baseUrl : baseUrl + '/';
    const upstreamUrl = new URL(upstreamPath.replace(/^\//, ''), base);
    const lib = upstreamUrl.protocol === 'https:' ? https : http;

    // Build forwarded headers (strip hop-by-hop, keep auth + content headers)
    const forwardHeaders = {};
    const hopByHop = new Set([
      'connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization',
      'te', 'trailer', 'transfer-encoding', 'upgrade', 'host',
    ]);
    for (const [k, v] of Object.entries(headers)) {
      if (!hopByHop.has(k.toLowerCase())) forwardHeaders[k] = v;
    }
    forwardHeaders['host'] = upstreamUrl.host;
    forwardHeaders['content-length'] = Buffer.byteLength(bodyBuffer);

    // Override x-api-key with the real upstream key (incoming request carries a passthrough placeholder)
    if (apiKey) {
      forwardHeaders['x-api-key'] = apiKey;
      forwardHeaders['authorization'] = `Bearer ${apiKey}`;
    }

    const upstreamReq = lib.request(
      {
        hostname: upstreamUrl.hostname,
        port: upstreamUrl.port || (upstreamUrl.protocol === 'https:' ? 443 : 80),
        path: upstreamUrl.pathname + (upstreamUrl.search || ''),
        method,
        headers: forwardHeaders,
      },
      (upstreamRes) => {
        // ── Circuit breaker: trip on 402 ──────────────────────────────────
        if (upstreamRes.statusCode === 402) {
          upstreamCircuitBreaker.set(baseUrl, Date.now() + CIRCUIT_BREAKER_TTL_MS);
          log('warn', 'upstream quota exhausted, circuit breaker tripped', {
            baseUrl, ttlMs: CIRCUIT_BREAKER_TTL_MS,
          });
        }
        // Relay status and headers
        const relayHeaders = {};
        for (const [k, v] of Object.entries(upstreamRes.headers)) {
          const lower = k.toLowerCase();
          if (!hopByHop.has(lower)) relayHeaders[k] = v;
        }
        clientRes.writeHead(upstreamRes.statusCode, relayHeaders);
        // Pipe SSE / body
        upstreamRes.pipe(clientRes);
        upstreamRes.on('end', () => resolve());
        upstreamRes.on('error', reject);
      }
    );

    upstreamReq.on('error', reject);
    upstreamReq.write(bodyBuffer);
    upstreamReq.end();
  });
}

// ─── Request handler ──────────────────────────────────────────────────────────

async function handleRequest(req, res) {
  // Collect request body
  const chunks = [];
  req.on('data', (c) => chunks.push(c));
  await new Promise((resolve, reject) => {
    req.on('end', resolve);
    req.on('error', reject);
  });
  const rawBody = Buffer.concat(chunks);

  // Only intercept POST /v1/messages
  if (req.method !== 'POST' || !req.url.startsWith('/v1/messages')) {
    // For non-messages paths, resolve upstream from a best-effort URL parse (no body yet)
    return forwardRequest(req.url, req.method, req.headers, rawBody, res).catch((err) => {
      log('error', 'forward error (non-messages)', { error: err.message });
      if (!res.headersSent) {
        res.writeHead(502);
        res.end('Bad Gateway');
      }
    });
  }

  let body;
  try {
    body = JSON.parse(rawBody.toString('utf8'));
  } catch (e) {
    log('error', 'JSON parse error', { error: e.message });
    res.writeHead(400);
    res.end('Bad Request');
    return;
  }

  const modelId = body.model || '';
  const upstream = resolveUpstream(modelId);
  const contextWindow = getContextWindow(modelId);

  log('info', 'request received', { model: modelId, upstream: upstream.baseUrl });

  let result;
  try {
    result = await compactMessages(body.messages || [], contextWindow);
  } catch (err) {
    log('error', 'compactMessages threw', { error: err.message });
    result = { messages: body.messages || [], compacted: false };
  }

  // Rebuild body with (potentially) compacted messages
  const outBody = result.compacted
    ? Buffer.from(JSON.stringify({ ...body, messages: result.messages }), 'utf8')
    : rawBody;

  // Forward to upstream
  try {
    await forwardRequest(req.url, req.method, req.headers, outBody, res, upstream);
  } catch (err) {
    log('error', 'upstream forward error', { error: err.message });
    if (!res.headersSent) {
      // Fallback: try again with original body
      try {
        await forwardRequest(req.url, req.method, req.headers, rawBody, res, upstream);
      } catch (err2) {
        log('error', 'fallback forward also failed', { error: err2.message });
        if (!res.headersSent) {
          res.writeHead(502);
          res.end('Bad Gateway');
        }
      }
    }
  }
}

// ─── Server startup ───────────────────────────────────────────────────────────

const server = http.createServer((req, res) => {
  handleRequest(req, res).catch((err) => {
    log('error', 'unhandled error in handleRequest', { error: err.message });
    if (!res.headersSent) {
      res.writeHead(500);
      res.end('Internal Server Error');
    }
  });
});

server.listen(PORT, '127.0.0.1', () => {
  log('info', 'compaction proxy started', {
    port: PORT,
    upstream: UPSTREAM_BASE_URL,
    ollamaModel: OLLAMA_MODEL,
    compactThreshold: COMPACT_THRESHOLD,
    recentTurnsPreserve: RECENT_TURNS_PRESERVE,
  });
});

server.on('error', (err) => {
  log('error', 'server error', { error: err.message });
  process.exit(1);
});

process.on('SIGTERM', () => {
  log('info', 'received SIGTERM, shutting down');
  server.close(() => process.exit(0));
});

process.on('SIGINT', () => {
  log('info', 'received SIGINT, shutting down');
  server.close(() => process.exit(0));
});
