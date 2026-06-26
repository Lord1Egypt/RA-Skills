import express from 'express';
import WebSocket from 'ws';
import { execFile } from 'child_process';
import { appendFileSync, existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';
import { promisify } from 'util';

const execFileAsync = promisify(execFile);
const CONFIG_FILE = './config/bridge.json';

const defaultConfig = {
  bot: {
    qq: 0,
    adminQq: 0,
    name: 'Assistant',
  },
  monitoredGroups: [],
  humanLike: {
    enabled: true,
    typingIndicator: true,
    randomDelay: true,
    probabilisticIgnore: true,
    ignorePatterns: ['^ok$', '^\\.+$', '^emm+$', '^hi$', '^hello$'],
    ignoreChance: 0.25,
    minReplyDelayMs: 1200,
    maxReplyDelayMs: 4000,
    typingSpeedCps: 5,
  },
  bridge: {
    httpPort: 3002,
    logDir: './chat-logs',
  },
  napcat: {
    apiUrl: 'http://127.0.0.1:3001',
    apiToken: '',
    wsUrl: 'ws://127.0.0.1:6700',
  },
  openClaw: {
    wslDistro: 'Ubuntu-22.04',
    container: 'openclaw-qq-bridge',
    timeoutSeconds: 120,
    healthUrl: 'http://127.0.0.1:18789/health',
  },
  persona: {
    tone: 'calm, restrained, observant, precise, slightly cool, quietly caring',
    extraRules: 'Do not use fixed honorifics or nicknames unless the user does first.',
  },
};

function deepMerge(base, override) {
  const result = { ...base };
  for (const key of Object.keys(override || {})) {
    const left = base?.[key];
    const right = override[key];
    if (left && right && typeof left === 'object' && typeof right === 'object'
      && !Array.isArray(left) && !Array.isArray(right)) {
      result[key] = deepMerge(left, right);
    } else {
      result[key] = right;
    }
  }
  return result;
}

function loadConfig() {
  try {
    if (existsSync(CONFIG_FILE)) {
      const saved = JSON.parse(readFileSync(CONFIG_FILE, 'utf-8'));
      return deepMerge(defaultConfig, saved);
    }
  } catch (error) {
    console.error('[bridge] config load error:', error.message);
  }
  return structuredClone(defaultConfig);
}

function saveConfig(cfg) {
  try {
    writeFileSync(CONFIG_FILE, JSON.stringify(cfg, null, 2), 'utf-8');
  } catch (error) {
    console.error('[bridge] config save error:', error.message);
  }
}

let config = loadConfig();
saveConfig(config);

const LOG_DIR = config.bridge?.logDir || './chat-logs';
if (!existsSync(LOG_DIR)) mkdirSync(LOG_DIR, { recursive: true });

let wsConnected = false;
const startTime = Date.now();
const recentMessages = new Map();
const conversationCtx = new Map();

function nowStr() {
  return new Date().toLocaleTimeString('zh-CN', { hour12: false });
}

function today() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

function uptime() {
  const total = Math.floor((Date.now() - startTime) / 1000);
  const h = Math.floor(total / 3600);
  const m = Math.floor((total % 3600) / 60);
  const s = total % 60;
  return `${h}h${m}m${s}s`;
}

function sleep(ms) {
  return new Promise(resolveSleep => setTimeout(resolveSleep, ms));
}

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function shouldMonitorGroup(groupId) {
  const groups = config.monitoredGroups || [];
  if (groups.length === 0) return true;
  return groups.includes(Number(groupId));
}

function segmentsToText(message) {
  if (typeof message === 'string') return message;
  if (!Array.isArray(message)) return JSON.stringify(message);
  return message.map(seg => {
    if (seg.type === 'text') return seg.data?.text || '';
    if (seg.type === 'at') return `@${seg.data?.qq || '?'}`;
    if (seg.type === 'image') return '[image]';
    if (seg.type === 'record') return '[audio]';
    if (seg.type === 'video') return '[video]';
    if (seg.type === 'reply') return '';
    return `[${seg.type}]`;
  }).join('').trim();
}

function segmentsToRich(message) {
  if (typeof message === 'string') return message;
  if (!Array.isArray(message)) return JSON.stringify(message);
  return message.map(seg => {
    if (seg.type === 'text') return seg.data?.text || '';
    if (seg.type === 'at') return `@${seg.data?.qq || '?'}`;
    if (seg.type === 'image') return `[image: ${seg.data?.url || seg.data?.file || 'unknown'}]`;
    if (seg.type === 'record') return `[audio: ${seg.data?.url || seg.data?.file || 'unknown'}]`;
    if (seg.type === 'video') return `[video: ${seg.data?.url || seg.data?.file || 'unknown'}]`;
    if (seg.type === 'reply') return '';
    return `[${seg.type}]`;
  }).join('').trim();
}

function logFileForEvent(event) {
  if (event.group_id) return `${LOG_DIR}/${today()}-g${event.group_id}.log`;
  return `${LOG_DIR}/${today()}-p${event.user_id}.log`;
}

function logMessage(event, sender, text) {
  appendFileSync(logFileForEvent(event), `[${nowStr()}] ${sender}: ${text}\n`, 'utf-8');
}

function ctxKey(event) {
  return event.group_id ? `g:${event.group_id}` : `p:${event.user_id}`;
}

function pushContext(key, role, sender, text) {
  if (!conversationCtx.has(key)) conversationCtx.set(key, []);
  const arr = conversationCtx.get(key);
  arr.push({ role, sender, text, time: Date.now() });
  if (arr.length > 20) arr.splice(0, arr.length - 20);
}

function getRecentContext(key) {
  return (conversationCtx.get(key) || []).slice(-10);
}

setInterval(() => {
  const cutoff = Date.now() - 30 * 60_000;
  for (const [key, messages] of conversationCtx) {
    const last = messages[messages.length - 1];
    if (!last || last.time < cutoff) conversationCtx.delete(key);
  }
}, 30 * 60_000);

function cleanIncomingText(text) {
  return text.replace(/@\d+\s*/g, '').trim();
}

function shouldIgnoreMessage(text) {
  const cfg = config.humanLike || {};
  if (!cfg.enabled || !cfg.probabilisticIgnore) return false;
  const patterns = cfg.ignorePatterns || [];
  const trivial = patterns.some(pattern => new RegExp(pattern, 'i').test(text));
  if (!trivial) return false;
  return Math.random() < Number(cfg.ignoreChance || 0);
}

async function sendTypingIndicator(userId) {
  const cfg = config.humanLike || {};
  if (!cfg.enabled || !cfg.typingIndicator) return;
  try {
    await fetch(`${config.napcat.apiUrl}/.handle_quick_operation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.napcat.apiToken}`,
      },
      body: JSON.stringify({ context: { user_id: userId }, operation: {} }),
    }).catch(() => {});
  } catch {}
}

async function getNapCatStatus() {
  const response = await fetch(`${config.napcat.apiUrl}/get_status`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${config.napcat.apiToken}`,
    },
    signal: AbortSignal.timeout(3000),
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(`NapCat ${response.status}`);
  return data;
}

function buildContextBlock(recentCtx) {
  if (recentCtx.length <= 1) return '';
  const lines = recentCtx.slice(0, -1).map(item => `  ${item.sender}: ${item.text.slice(0, 120)}`).join('\n');
  return `\nRecent conversation context:\n${lines}\n`;
}

function buildDirectReplyPrompt({ event, sender, richText, contextBlock }) {
  let prefix = `[QQ ${event.message_type}]`;
  if (event.group_id) prefix += ` [group ${event.group_id}]`;
  return `${prefix} ${sender}: ${richText}
${contextBlock}
Reply with exactly the plain text that should be sent back to QQ.

Voice target:
- Sound ${config.persona.tone}.
- Keep it human and believable in QQ chat.
- Replies should usually be 1-2 short sentences.

Rules:
- Reply in the same language as the user unless context strongly suggests otherwise.
- Do not use markdown, code fences, or surrounding quotes.
- Do not describe actions, tools, or internal reasoning.
- Do not use parentheses, brackets, stage directions, or side comments for tone.
- Avoid excessive ellipses or exaggerated catchphrases.
- ${config.persona.extraRules}
- If the user only mentioned the bot without a real request, ask a short follow-up.`;
}

async function getOpenClawDirectReply(sessionId, prompt) {
  const timeoutSeconds = Number(config.openClaw.timeoutSeconds || 120);
  const args = [
    '-d', config.openClaw.wslDistro,
    '--',
    'docker', 'exec',
    config.openClaw.container,
    'openclaw', 'agent',
    '--session-id', sessionId,
    '--message', prompt,
    '--json',
    '--timeout', String(timeoutSeconds),
  ];

  const { stdout, stderr } = await execFileAsync('wsl', args, {
    windowsHide: true,
    timeout: (timeoutSeconds + 15) * 1000,
    maxBuffer: 10 * 1024 * 1024,
  });

  if (stderr && stderr.trim()) {
    console.warn(`[bridge] OpenClaw stderr: ${stderr.trim().slice(0, 200)}`);
  }

  const data = JSON.parse(stdout);
  const payloads = Array.isArray(data?.result?.payloads) ? data.result.payloads : [];
  const reply = payloads
    .map(payload => typeof payload?.text === 'string' ? payload.text.trim() : '')
    .filter(Boolean)
    .join('\n')
    .trim();

  if (!reply) throw new Error('OpenClaw returned an empty reply');
  return reply;
}

async function sendQQMessage(type, target, message, skipDelay = false) {
  const cfg = config.humanLike || {};
  if (!skipDelay && cfg.enabled && cfg.randomDelay) {
    const thinkDelay = randomInt(Number(cfg.minReplyDelayMs || 1200), Number(cfg.maxReplyDelayMs || 4000));
    const typingDelay = Math.min(Math.round((message.length / Number(cfg.typingSpeedCps || 5)) * 1000), 6000);
    await sleep(thinkDelay + typingDelay);
  }

  const apiPath = type === 'group' ? 'send_group_msg' : 'send_private_msg';
  const idField = type === 'group' ? 'group_id' : 'user_id';
  const body = {
    [idField]: Number(target),
    message: [{ type: 'text', data: { text: message } }],
  };

  const response = await fetch(`${config.napcat.apiUrl}/${apiPath}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${config.napcat.apiToken}`,
    },
    body: JSON.stringify(body),
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(`NapCat ${response.status}`);
  if (data?.status !== 'ok' || Number(data?.retcode ?? 0) !== 0) {
    const detail = data?.wording || data?.message || `retcode=${data?.retcode ?? 'unknown'}`;
    throw new Error(`NapCat send failed: ${detail}`);
  }

  const key = type === 'group' ? `g:${target}` : `p:${target}`;
  pushContext(key, 'bot', config.bot.name || 'Assistant', message);
  return data;
}

const COMMANDS = {
  '/ping': async () => 'pong',
  '/status': async () => {
    let napcatOnline = false;
    try {
      const status = await getNapCatStatus();
      napcatOnline = Boolean(status?.data?.online);
    } catch {}
    return [
      'NapCat QQ Bridge',
      `uptime: ${uptime()}`,
      `napcat ws: ${wsConnected}`,
      `napcat online: ${napcatOnline}`,
      `groups: ${(config.monitoredGroups || []).length === 0 ? 'all' : config.monitoredGroups.join(',')}`,
      `context buckets: ${conversationCtx.size}`,
      `container: ${config.openClaw.container}`,
    ].join('\n');
  },
};

async function handleEvent(event) {
  if (event.post_type !== 'message') return;
  if (event.self_id && String(event.user_id) === String(event.self_id)) return;

  const text = segmentsToText(event.message) || event.raw_message || '';
  const richText = segmentsToRich(event.message) || text;
  const sender = event.sender?.card || event.sender?.nickname || `${event.user_id}`;

  recentMessages.set(event.message_id || `${Date.now()}-${Math.random()}`, {
    sender,
    text,
    time: Date.now(),
  });

  if (event.group_id && shouldMonitorGroup(event.group_id)) {
    logMessage(event, sender, text);
  }
  if (!event.group_id) {
    logMessage(event, sender, text);
  }

  const key = ctxKey(event);
  pushContext(key, 'user', sender, text);

  const selfId = config.bot.qq || event.self_id;
  const isAtBot = Array.isArray(event.message) &&
    event.message.some(seg => seg.type === 'at' && String(seg.data?.qq) === String(selfId));
  const isPrivate = !event.group_id;

  if (!isPrivate && !isAtBot) return;

  const cleanText = cleanIncomingText(text);
  if (cleanText.startsWith('/')) {
    const handler = COMMANDS[cleanText.split(/\s+/)[0].toLowerCase()];
    if (handler) {
      const reply = await handler(event);
      await sendQQMessage(isPrivate ? 'private' : 'group', event.group_id || event.user_id, reply, true);
      return;
    }
  }

  if (!isPrivate && shouldIgnoreMessage(cleanText)) {
    console.log(`[bridge] ignored trivial group ping: ${cleanText}`);
    return;
  }

  await sendTypingIndicator(event.user_id);

  const recentCtx = getRecentContext(key);
  const contextBlock = buildContextBlock(recentCtx);
  const sessionId = `qq-${isPrivate ? 'private' : 'group'}-${event.group_id || event.user_id}`;
  const prompt = buildDirectReplyPrompt({ event, sender, richText, contextBlock });
  const reply = await getOpenClawDirectReply(sessionId, prompt);
  await sendQQMessage(isPrivate ? 'private' : 'group', event.group_id || event.user_id, reply);
}

function connectWS() {
  console.log(`[bridge] connecting to ${config.napcat.wsUrl}`);
  const ws = new WebSocket(config.napcat.wsUrl);

  ws.on('open', () => {
    wsConnected = true;
    console.log('[bridge] WS connected');
  });

  ws.on('message', async raw => {
    try {
      const event = JSON.parse(raw.toString());
      await handleEvent(event);
    } catch (error) {
      console.error('[bridge] event error:', error.message);
    }
  });

  ws.on('close', () => {
    wsConnected = false;
    console.log('[bridge] WS disconnected, reconnecting in 5s');
    setTimeout(connectWS, 5000);
  });

  ws.on('error', error => {
    wsConnected = false;
    console.error('[bridge] WS error:', error.message);
  });
}

const app = express();
app.use(express.json({ limit: '1mb' }));

app.get('/health', async (_req, res) => {
  let napcatHttpOk = false;
  let napcatOnline = false;
  let napcatGood = false;
  let openclawOk = false;

  try {
    const status = await getNapCatStatus();
    napcatHttpOk = true;
    napcatOnline = Boolean(status?.data?.online);
    napcatGood = Boolean(status?.data?.good);
  } catch {}

  try {
    const response = await fetch(config.openClaw.healthUrl, { signal: AbortSignal.timeout(3000) });
    openclawOk = response.ok;
  } catch {}

  res.json({
    status: 'ok',
    uptime: uptime(),
    napcat_ws: wsConnected,
    napcat_http: napcatHttpOk,
    napcat_online: napcatOnline,
    napcat_good: napcatGood,
    openclaw_reachable: openclawOk,
    monitored_groups: (config.monitoredGroups || []).length === 0 ? 'all' : config.monitoredGroups,
    cached_messages: recentMessages.size,
    conversations: conversationCtx.size,
  });
});

app.get('/logs', (_req, res) => {
  try {
    res.json(readdirSync(LOG_DIR).filter(name => name.endsWith('.log')).sort());
  } catch {
    res.json([]);
  }
});

app.get('/logs/:filename', (req, res) => {
  const path = resolve(LOG_DIR, req.params.filename);
  if (!existsSync(path)) {
    res.status(404).send('not found');
    return;
  }
  res.type('text/plain; charset=utf-8').send(readFileSync(path, 'utf-8'));
});

app.get('/config', (_req, res) => {
  res.json(config);
});

app.post('/config', (req, res) => {
  config = deepMerge(config, req.body || {});
  saveConfig(config);
  res.json({ ok: true, config });
});

app.post('/send_qq', async (req, res) => {
  const { type, target, message } = req.body || {};
  if (!type || !target || !message) {
    res.status(400).json({ error: 'need type, target, message' });
    return;
  }

  try {
    const data = await sendQQMessage(type, target, message, true);
    res.json({ ok: true, data });
  } catch (error) {
    res.status(502).json({ ok: false, error: error.message });
  }
});

app.listen(Number(config.bridge.httpPort || 3002), () => {
  console.log(`[bridge] HTTP listening on ${config.bridge.httpPort || 3002}`);
});

connectWS();
