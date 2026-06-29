const http = require('http');
const { execSync, exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const HTTPS = require('https');

const PORT = 9877;  // v1.3.0: 错开 9876 (minimax-embedding-adapter)
const MMX_CONFIG = path.join(process.env.HOME, '.mmx', 'config.json');

// ── v1.4.0: CLI flags ───────────────────────────────────
const FLAGS = {
  // 默认禁用 header 透传 API key,避免本地服务被恶意网页当作 proxy 消费你的配额
  // 需要使用 header key 时显式开启:node mmx-monitor-server.js --allow-header-key
  allowHeaderKey: process.argv.includes('--allow-header-key'),
};

// ── v1.4.0: CORS origin allowlist ───────────────────────
// 只允许本地源(浏览器 / 文件协议)调本机 server,禁止跨域乱用。
// 历史 v1.3.x 使用 Access-Control-Allow-Origin: *,被 ClawHub 标记为高危(F5,97%)。
const ALLOWED_ORIGINS = [
  'http://127.0.0.1:9877',
  'http://localhost:9877',
  'http://127.0.0.1',
  'http://localhost',
  'file://',
  'null',  // file:// 协议在某些浏览器下 Origin 头为 "null"
];

function corsOriginFor(req) {
  const origin = req.headers['origin'] || '';
  // 同源请求(curl / 本机直连)通常不带 Origin header,直接返回 false 表示无需 CORS 头
  if (!origin) return false;
  if (ALLOWED_ORIGINS.includes(origin)) return origin;
  // 不在白名单:返回 null(不允许跨源)
  return null;
}

// ── Read mmx API key ─────────────────────────────────────
// v1.6.0 (F8): 不再自动读 ~/.mmx/config.json。用户点击 "加载本地凭证" 才会调
// /api/load_cred 读一次。键存在本进程的 credLoadedKey 变量里,server 重启后丢失。
let credLoadedKey = '';  // 按需加载后才会被填入
let credLoadedAt = 0;     // 加载时间戳(debug / banner 显示用)

function readMmxConfigKey() {
  try {
    const config = JSON.parse(fs.readFileSync(MMX_CONFIG, 'utf8'));
    return config.api_key || '';
  } catch { return ''; }
}

function getReqKey(req) {
  // v1.4.0: F3 - 默认拒绝 request header 透传的 API key,避免本机 server 变成 proxy。
  // 开启方式:node mmx-monitor-server.js --allow-header-key
  if (FLAGS.allowHeaderKey && req.headers['x-mmx-api-key']) {
    return req.headers['x-mmx-api-key'];
  }
  // v1.6.0: 返回用户主动加载的 key。未加载则为空,所有需要 key 的请求会返 401。
  return credLoadedKey;
}



function parseJson(raw) {
  try { return JSON.parse(raw); } catch { return null; }
}

// ── v1.5.0: 24h usage history (ring buffer) ────────────────
// 每次 /api/token_plan 调用后写入一行 JSONL。文件按 mtime + 行数 trim 到 24h。
// v1.6.1: 明确这是**写入**操作，SKILL.md permissions 加 write:filesystem。
const HISTORY_FILE = path.join(__dirname, 'history.jsonl');
const HISTORY_MAX_AGE_MS = 24 * 3600 * 1000;

function appendHistory(snapshot) {
  try {
    const line = JSON.stringify({ ts: Date.now(), ...snapshot }) + '\n';
    fs.appendFileSync(HISTORY_FILE, line);
    // Trim:删 24h 前的行
    trimHistory();
  } catch (e) {
    console.warn('[history] append failed:', e.message);
  }
}

function trimHistory() {
  try {
    if (!fs.existsSync(HISTORY_FILE)) return;
    const lines = fs.readFileSync(HISTORY_FILE, 'utf8').split('\n').filter(Boolean);
    const cutoff = Date.now() - HISTORY_MAX_AGE_MS;
    const kept = lines.filter(l => {
      try { return (JSON.parse(l).ts || 0) >= cutoff; }
      catch { return false; }
    });
    if (kept.length < lines.length) {
      fs.writeFileSync(HISTORY_FILE, kept.join('\n') + (kept.length ? '\n' : ''));
    }
  } catch {}
}

function readHistory(hours) {
  try {
    if (!fs.existsSync(HISTORY_FILE)) return [];
    const cutoff = Date.now() - (hours || 24) * 3600 * 1000;
    const lines = fs.readFileSync(HISTORY_FILE, 'utf8').split('\n').filter(Boolean);
    return lines
      .map(l => { try { return JSON.parse(l); } catch { return null; } })
      .filter(x => x && x.ts >= cutoff);
  } catch { return []; }
}

function httpsGet(url, headers, body) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const postData = body ? JSON.stringify(body) : null;
    const opts = {
      hostname: urlObj.hostname,
      path: urlObj.pathname + urlObj.search,
      method: postData ? 'POST' : 'GET',
      headers: {
        ...headers,
        ...(postData ? { 'Content-Length': Buffer.byteLength(postData) } : {}),
      },
    };
    const req = HTTPS.request(opts, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ status: res.statusCode, data }));
    });
    req.on('error', reject);
    req.setTimeout(20000, () => { req.destroy(); reject(new Error('timeout')); });
    if (postData) req.write(postData);
    req.end();
  });
}

const MODEL_NAME_MAP = {
  'MiniMax-M*':             'MiniMax-M2.7',
  'speech-hd':              'Text to Speech HD',
  'MiniMax-Hailuo-2.3-Fast-6s-768p': 'Hailuo-2.3-Fast-768P',
  'MiniMax-Hailuo-2.3-6s-768p':     'Hailuo-2.3-768P',
  'music-2.5':              'Music-2.5',
  'music-2.6':              'Music-2.6',
  'music-cover':            'Music-Cover',
  'lyrics_generation':      'Lyrics Gen',
  'image-01':               'Image-01',
  'coding-plan-vlm':        'Coding-VLM',
  'coding-plan-search':     'Coding-Search',
  'video':                  '海螺视频',
};

function is4HourWindow(entry) {
  const dur = entry.end_time - entry.start_time;
  return dur <= 5 * 3600 * 1000;
}

function buildModels(remains) {
  if (!remains || !Array.isArray(remains)) return [];
  // v1.2.0: 官方改为只返"剩余百分比"(*_remaining_percent),不再返具体 count。
  // 我们把 used 推导成"已用百分比" (100 - remaining),total 设为 100,
  // 这样下游的 used/total 比例和百分比语义保持不变,前端零改动。
  const sorted = [...remains].sort((a, b) => {
    const a4 = is4HourWindow(a) ? 0 : 1;
    const b4 = is4HourWindow(b) ? 0 : 1;
    if (a4 !== b4) return a4 - b4;
    return (a.current_interval_remaining_percent ?? 100) <
           (b.current_interval_remaining_percent ?? 100) ? 1 : -1;
  });
  return sorted.map(e => {
    const remPct = clampPct(e.current_interval_remaining_percent);
    const wRemPct = clampPct(e.current_weekly_remaining_percent);
    // 官方 status: 1=限额中 3=无限制/正常。wstatus=3 表示该模型本周无配额上限。
    const weeklyUnlimited = e.current_weekly_status === 3;
    // v1.3.0: status=3 在 interval 上其实有两种情况--
    //   (a) 真·无限额(语音/音乐/图像 等总是开放)
    //   (b) 套餐未启用(video 额度项元数据存在但被屏蔽,调 API 会被拒"用量上限")
    // 仅靠元数据无法区分。但后端实际是 status=3 时让前端显示"套餐未启用"提示,
    // 顶部聚合排除掉,避免假数据污染大圆环。
    const intervalUnlimited = e.current_interval_status === 3;
    return {
      name:      MODEL_NAME_MAP[e.model_name] || e.model_name,
      used:      100 - remPct, // 已用百分比
      total:     100,           // 基数 100,前端 used/total 比例 = 已用%
      window:    is4HourWindow(e) ? '4小时' : '24小时',
      remains_time_ms: e.remains_time,
      weekly_used:     100 - wRemPct,
      weekly_total:    100,
      weekly_unlimited: weeklyUnlimited,
      interval_unlimited: intervalUnlimited,
    };
  });
}

function clampPct(v) {
  const n = Number(v);
  if (!Number.isFinite(n)) return 100;
  if (n < 0) return 0;
  if (n > 100) return 100;
  return n;
}

// ── Ordinary (non-streaming) API probe ────────────────
async function probeOrdinaryApi(apiKey) {
  const key = apiKey;
  const testMessages = [{ role: 'user', content: 'Hi' }];
  const t0 = Date.now();
  try {
    const { status, data } = await httpsGet(
      'https://api.minimaxi.com/v1/text/chatcompletion_v2',
      {
        'Authorization': 'Bearer ' + key,
        'Content-Type': 'application/json',
      },
      {
        model: 'MiniMax-M2.7',
        messages: testMessages,
        max_tokens: 30,
        stream: false,
      }
    );
    const latency = Date.now() - t0;
    const parsed = parseJson(data);
    return {
      ok: status === 200 && parsed ? 1 : 0,
      total: 1,
      latency,
    };
  } catch {
    return { ok: 0, total: 1, latency: Date.now() - t0 };
  }
}

// ── BURST (3 concurrent streaming) probe ───────────────
async function probeBurstApi(apiKey) {
  const key = apiKey;
  const testMessages = [{ role: 'user', content: 'Hi' }];
  const t0 = Date.now();
  const makeReq = () => httpsGet(
    'https://api.minimaxi.com/v1/text/chatcompletion_v2',
    { 'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json' },
    { model: 'MiniMax-M2.7', messages: testMessages, max_tokens: 30, stream: true }
  ).then(({ status, data }) => {
    const latency = Date.now() - t0;
    // v1.3.0: SSE 流式响应是多行 "data: {...}\n\n..." 格式,parseJson 整块会失败。
    // 只要 status=200 且 body 以 "data:" 开头就视为成功。
    const ok = status === 200 && data.trimStart().startsWith('data:') ? 1 : 0;
    return { ok, total: 1, latency };
  }).catch(() => ({ ok: 0, total: 1, latency: Date.now() - t0 }));
  const results = await Promise.all([makeReq(), makeReq(), makeReq()]);
  return {
    burst_ok: results.reduce((s, r) => s + r.ok, 0),
    burst_total: 3,
    burst_latency: Math.round(results.reduce((s, r) => s + r.latency, 0) / 3),
  };
}

// ── Real API probe ───────────────────────────────────────
async function probeApiLatency(apiKey) {
  const key = apiKey;
  const testMessages = [
    { role: 'user', content: 'Hi' },
  ];

  // TTFT: time to first byte (streaming)
  const t0 = Date.now();
  let ttft = 0;
  let totalMsgs = 0;
  let tokensReceived = 0;
  let lastByteTime = t0;

  try {
    const { status, data } = await httpsGet(
      'https://api.minimaxi.com/v1/text/chatcompletion_v2',
      {
        'Authorization': 'Bearer ' + key,
        'Content-Type': 'application/json',
      },
      {
        model: 'MiniMax-M2.7',
        messages: testMessages,
        max_tokens: 60,
        stream: true,
      }
    );

    // If streaming fails (no SSE), fall back to non-streaming
    if (status !== 200 || !data.includes('\n')) {
      const t1 = Date.now();
      const latency = t1 - t0;
      const parsed = parseJson(data);
      const tokens = parsed?.usage?.completion_tokens || 0;
      return {
        latency,
        ttft: latency,
        speed: tokens > 0 ? Math.round(tokens / (latency / 1000)) : 0,
        tokens,
      };
    }

    // Parse SSE lines - find time to first content
    const lines = data.split('\n');
    for (const line of lines) {
      if (line.startsWith('data:')) {
        const ts = Date.now();
        if (ttft === 0) ttft = ts - t0;
        totalMsgs++;
        try {
          const obj = parseJson(line.slice(5));
          const txt = obj?.choices?.[0]?.delta?.content || '';
          tokensReceived += txt.length;
          lastByteTime = ts;
        } catch {}
      }
    }

    const totalTime = lastByteTime - t0;
    const speed = tokensReceived > 0 && totalTime > 0
      ? Math.round(tokensReceived / (totalTime / 1000))
      : 0;

    return {
      ttft,
      latency: totalTime,
      speed,
      tokens: tokensReceived,
      seq_min: totalTime,
      seq_max: totalTime,
      burst_ok: 0,
      burst_total: 0,
      ordinary_ok: 0,
      ordinary_total: 0,
    };
  } catch (e) {
    const elapsed = Date.now() - t0;
    return {
      ttft: elapsed,
      latency: elapsed,
      speed: 0,
      tokens: 0,
      seq_min: elapsed,
      seq_max: elapsed,
      burst_ok: 0,
      burst_total: 0,
      ordinary_ok: 0,
      ordinary_total: 0,
    };
  }
}

// ── Rate counters (cumulative) ───────────────────────────

// ── Server ───────────────────────────────────────────────
const server = http.createServer(async (req, res) => {
  // v1.6.0 debug: log every request to debug Safari fetch issue
  console.log(`[req] ${req.method} ${req.url}  Origin=${req.headers['origin']||'-'}  Referer=${(req.headers['referer']||'').slice(0,80)}`);
  // v1.4.0: F5 - CORS 严格化。只允许本机 / file:// 同源。
  const allowOrigin = corsOriginFor(req);
  if (allowOrigin) {
    res.setHeader('Access-Control-Allow-Origin', allowOrigin);
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    // F3: 只在 allowHeaderKey 开启时才暴露 X-MMX-API-Key header
    res.setHeader('Access-Control-Allow-Headers', FLAGS.allowHeaderKey ? 'Content-Type, X-MMX-API-Key' : 'Content-Type');
    res.setHeader('Vary', 'Origin');
  }

  if (req.method === 'OPTIONS') {
    res.writeHead(allowOrigin ? 204 : 403);
    res.end();
    return;
  }

  const urlPath = new URL(req.url, `http://localhost:${PORT}`).pathname;
  const apiKey = getReqKey(req);

  // v1.6.0 (F8): 未加载凭证就调需要 key 的端点 → 返 401。提示前端提示用户点 "加载本地凭证"。
  function requireKeyOrFail(res) {
    if (apiKey) return false;
    res.writeHead(401, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ ok: false, error: 'API key 未加载:请点顶部 "加载本地凭证" 按钮或手动输入' }));
    return true;
  }

  // ── POST /api/load_cred ─────────────────────────────────────────
  // v1.6.1 (F8): 用户主动点击 "加载本地凭证" 才读 ~/.mmx/config.json。
  // 必须满足 Referer 是本机白名单（防止恶意网页/curl 拉走本地 key）。
  if (req.method === 'POST' && urlPath === '/api/load_cred') {
    const referer = req.headers['referer'] || '';
    // v1.6.1: 强制要求 Referer 是本机白名单之一，不再放行空 referer。
    // curl / CLI 手动调用请带 -H 'Referer: http://127.0.0.1:9877/'。
    const allowedOrigin = referer && ALLOWED_ORIGINS.some(o => o !== 'null' && referer.startsWith(o));
    if (!allowedOrigin) {
      res.writeHead(403, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: 'load_cred requires Referer from local origin (e.g. http://127.0.0.1:9877/)' }));
      return;
    }
    const k = readMmxConfigKey();
    if (!k) {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: `未找到 ${MMX_CONFIG} 或其中无 api_key` }));
      return;
    }
    credLoadedKey = k;
    credLoadedAt = Date.now();
    // v1.6.1 (审计 finding 99%): 响应里**绝不返回** key。
    // 浏览器侧的输入框可以直接从 `getMmxKey()` 读本地配置，不需要 server 中转 key。
    // 之前响应里包含 `key: k` 是个真 bug —— 任何能 reach 到本机 server 的进程
    // 都能拿到完整 API key；现在 server 只确认"已加载"这件事。
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      ok: true,
      loaded: true,
      keyLength: k.length,  // 给前端一个长度提示，方便 UI 显示 "sk-cp-…XXXX (24 chars)"
      keyPrefix: k.slice(0, 6),  // 前缀用来视觉确认（"sk-cp-"），不暴露完整 key
      msg: '已加载到会话内存，server 重启后需重新加载',
    }));
    return;
  }

  // ── GET /api/token_plan ────────────────────────────────
  if (req.method === 'GET' && urlPath === '/api/token_plan') {
    if (requireKeyOrFail(res)) return;
    try {
      const key = apiKey;
      const raw = await httpsGet(
        'https://www.minimaxi.com/v1/token_plan/remains',
        { 'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json' }
      );
      let parsed = parseJson(raw.data);
      // API wraps response in {status, data} where data is a JSON string
      if (parsed && parsed.data && typeof parsed.data === 'string') {
        parsed = parseJson(parsed.data);
      }
      if (!parsed || (parsed.base_resp && parsed.base_resp.status_code !== 0)) {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, error: parsed?.base_resp?.status_msg || 'API error', raw: raw.data }));
        return;
      }
      const models = buildModels(parsed.model_remains || []);
      const fourHModels = models.filter(m => m.window === '4小时');
      const fourHTotal  = fourHModels.reduce((s, m) => s + m.total, 0);
      const fourHUsed   = fourHModels.reduce((s, m) => s + m.used, 0);
      const minResetMs = fourHModels.length ? Math.min(...fourHModels.map(m => m.remains_time_ms)) : 0;
      // v1.5.0: 写一行 history(环形 buffer)。只记 totalUsed/totalLimit 摘要 + 模型快照。
      appendHistory({
        used:  fourHUsed,
        total: fourHTotal,
        models: models.map(m => ({ name: m.name, used: m.used, total: m.total, window: m.window })),
      });
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        ok: true,
        data: {
          models,
          totalUsed:  fourHUsed,
          totalLimit: fourHTotal,
          resetSeconds: Math.ceil(minResetMs / 1000),
        }
      }));
    } catch (e) {
      res.writeHead(502, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
    return;
  }

  // ── GET /api/history ──────────────────────────────────────────
  // v1.5.0: 返回最近 N 小时的 usage history 采样(默认 24h)。
  // 客户端可以用这数据画趋势线。
  if (req.method === 'GET' && urlPath === '/api/history') {
    const hours = Math.max(1, Math.min(168, Number(new URL(req.url, `http://localhost:${PORT}`).searchParams.get('hours')) || 24));
    const rows = readHistory(hours);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ ok: true, hours, count: rows.length, data: rows }));
    return;
  }

  // ── GET /api/probe ──────────────────────────────────────────
  // v1.6.0 (F6/F7): probe 改按需触发。端点保留,但不在后台定时调用。
  // 前端 "开始速率测试" 按钮才会调,发起 5 次真实 chat completion 请求(×~180 token)。
  // 必须满足两个条件才放行:
  //   (1) Referer 是本机页面(CORS allowlist 已经检过 Origin,这里加 Referer 二次防御)
  //   (2) 响应里带回 cost_estimate 字段,前端会先弹 confirm 才发
  if (req.method === 'GET' && urlPath === '/api/probe') {
    if (requireKeyOrFail(res)) return;
    const referer = req.headers['referer'] || '';
    // Referer 为空(curl / 本机直连)或不在本机白名单 → 拒绝
    if (referer) {
      const ok = ALLOWED_ORIGINS.some(o => o !== 'null' && referer.startsWith(o));
      if (!ok) {
        res.writeHead(403, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, error: 'probe requires Referer from local origin' }));
        return;
      }
    }
    const [probeResult, burstResult, ordinaryResult] = await Promise.all([
      probeApiLatency(apiKey),
      probeBurstApi(apiKey),
      probeOrdinaryApi(apiKey),
    ]);

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      ok: true,
      cost_estimate: '5 chat completion requests, max ~180 tokens',
      // SEQ test: sequential probe, use last latency as baseline
      seq_ok: 1, seq10_total: 1,
      seq10_latency: probeResult.latency,
      seq_min: probeResult.seq_min,
      seq_max: probeResult.seq_max,
      // BURST test: 3 concurrent
      burst_ok: burstResult.burst_ok,
      burst_total: burstResult.burst_total,
      burst_latency: burstResult.burst_latency,
      // LLM / ordinary
      llm_ok: 1, llm_total: 1,
      ordinary_ok: ordinaryResult.ok,
      ordinary_total: ordinaryResult.total,
      // Performance data from real probe
      latency: probeResult.latency,    // P50
      ttft: probeResult.ttft,
      speed: probeResult.speed,        // tokens/s
    }));
    return;
  }

  // ── GET / 或 /mmx-monitor.html ──────────────────────────────
  // v1.6.0 (Safari file:// 兼容性):让 server 也服务 HTML,
  // 浏览器通过 http://127.0.0.1:9877/ 打开,同源 fetch 避免 file:// → http CORS 问题。
  if (urlPath === '/' || urlPath === '/mmx-monitor.html' || urlPath === '/index.html') {
    try {
      const html = fs.readFileSync(path.join(__dirname, 'mmx-monitor.html'), 'utf8');
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(html);
      return;
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'text/plain' });
      res.end('Failed to read mmx-monitor.html: ' + e.message);
      return;
    }
  }

  // ── GET /health ────────────────────────────────────────
  if (urlPath === '/health') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('ok');
    return;
  }

  res.writeHead(404); res.end('Not found');
});

server.listen(PORT, () => {
  console.log(`MiniMax Monitor API -> http://localhost:${PORT}`);
  console.log('  GET /api/token_plan - MiniMax token_plan');
  console.log('  POST /api/load_cred - load API key from ~/.mmx/config.json (v1.6.0: 需用户主动点击)');
  console.log('  GET /api/history   - 24h usage history (v1.5.0)');
  console.log('  GET /health        - health check');
  // v1.4.0: F11 - 明确告知本服务会读 ~/.mmx/config.json 拿 MiniMax API key。
  console.log('');
  console.log('[security] v1.4.0 security posture:');
  console.log(`  - CORS allowlist: 127.0.0.1/localhost/file:// (no longer *)`);
  console.log(`  - Header API key: ${FLAGS.allowHeaderKey ? 'ALLOWED (--allow-header-key)' : 'DENIED (use local ~/.mmx/config.json only)'}`);
  console.log(`  - Probe endpoint: ON-DEMAND ONLY (v1.6.0 起不再定时调用,UI 点 "开始速率测试" 才触发)`);
  console.log(`  - Credential: ON-DEMAND ONLY (v1.6.0 起不再自动读取,UI 点 "加载本地凭证" 才读)`);
});
