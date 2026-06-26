#!/usr/bin/env node
/**
 * Prana 封装技能 — Node 薄客户端（与 prana_skill_client.py 行为对齐）
 * 依赖：Node 18+；包根目录执行 npm install（需 yaml 解析 SKILL.md frontmatter）
 * 本文件为 ES Module（由 package.json 中 "type": "module" 声明）
 */
import { randomUUID } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = path.resolve(__dirname, '..');
const CONFIG_DIR = path.join(SKILL_ROOT, 'config');
const API_KEY_FILE = path.join(CONFIG_DIR, 'api_key.txt');
const SKILL_MD_FILE = path.join(SKILL_ROOT, 'SKILL.md');

// 封装打包时由服务端替换为对象；仓库模板为 null
const ENCAPSULATION_EMBEDDED = {"public_skill_key": "market_beats_public", "original_skill_key": "market_beats", "encapsulation_target": "prana"};

const DEFAULT_PRANA_BASE = 'https://claw-uat.ebonex.io/';

const HTTP_TIMEOUT_MS = 7200 * 1000;
const AGENT_RESULT_POLL_INTERVAL_SEC = Number.parseInt(
  process.env.PRANA_AGENT_RESULT_POLL_INTERVAL_SEC || '120',
  10,
);
const AGENT_RESULT_POLL_MAX_ATTEMPTS = Number.parseInt(
  process.env.PRANA_AGENT_RESULT_POLL_MAX_ATTEMPTS || '20',
  10,
);
const API_KEYS_FETCH_TIMEOUT_MS = 60 * 1000;

function truthyEnv(name) {
  const v = (process.env[name] || '').trim().toLowerCase();
  return v === '1' || v === 'true' || v === 'yes' || v === 'on';
}

function autoFetchApiKeyDisabled() {
  return truthyEnv('PRANA_SKILL_NO_AUTO_API_KEY');
}

function skipWriteFetchedApiKey() {
  return truthyEnv('PRANA_SKILL_SKIP_WRITE_API_KEY');
}

function normalizeEncapsulationTarget(raw) {
  let s = (raw || '').trim().toLowerCase().replace(/-/g, '_');
  if (!s) return 'prana';
  const aliases = { clawhub: 'claw_hub', openclaw: 'claw_hub', open_claw: 'claw_hub' };
  const key = aliases[s] || s;
  return key.length > 64 ? key.slice(0, 64) : key;
}

function loadEncapsulationRuntime() {
  if (ENCAPSULATION_EMBEDDED && typeof ENCAPSULATION_EMBEDDED === 'object') {
    return { ...ENCAPSULATION_EMBEDDED };
  }
  return null;
}

let YAML;
try {
  YAML = (await import('yaml')).default;
} catch {
  YAML = null;
}

function extractFrontmatter(content) {
  const trimmed = content.trimStart();
  if (!trimmed.startsWith('---')) return [null, content];
  const re = /^---\s*\r?\n([\s\S]*?)\r?\n---\s*\r?\n([\s\S]*)$/;
  const m = trimmed.match(re);
  if (!m) return [null, content];
  if (!YAML) {
    console.error('错误: 解析 SKILL.md 需要依赖 yaml。请在技能包根目录执行: npm install');
    process.exit(1);
  }
  try {
    const fm = YAML.parse(m[1]);
    return [fm && typeof fm === 'object' ? fm : null, m[2]];
  } catch {
    return [null, content];
  }
}

function loadSkillConfig() {
  if (!fs.existsSync(SKILL_MD_FILE)) {
    console.error('错误: 未找到 SKILL.md，请使用完整封装技能包解压后运行。');
    process.exit(1);
  }
  const runtime = loadEncapsulationRuntime();
  const raw = fs.readFileSync(SKILL_MD_FILE, 'utf8');
  const [frontmatter] = extractFrontmatter(raw);
  if (!frontmatter) {
    console.error('错误: SKILL.md 缺少有效的 YAML frontmatter。');
    process.exit(1);
  }
  let original = String((runtime && runtime.original_skill_key) || '').trim();
  const pubFm = String(frontmatter.original_skill_key || '').trim();
  const pubKeyFm = String(frontmatter.skill_key || '').trim();
  if (!original) original = pubFm;
  let pub = String((runtime && runtime.public_skill_key) || '').trim();
  if (!pub) pub = pubKeyFm;
  const sk = original || pub;
  if (!sk) {
    console.error(
      '错误: 缺少远端技能标识。请使用服务端封装生成的技能包（脚本内已写入 ENCAPSULATION_EMBEDDED），' +
        '或为旧版包在 SKILL.md frontmatter 中保留 original_skill_key / skill_key。',
    );
    process.exit(1);
  }
  let sip = '';
  for (const key of ['input_format', 'input_schema', 'params']) {
    const v = frontmatter[key];
    if (v != null && String(v).trim()) {
      sip = String(v).trim().slice(0, 16000);
      break;
    }
  }
  if (!sip) {
    const d = frontmatter.description;
    if (d != null && String(d).trim()) sip = String(d).trim().slice(0, 8000);
  }
  const enc = normalizeEncapsulationTarget(
    String(
      (runtime && runtime.encapsulation_target) ||
        frontmatter.encapsulation_target ||
        '',
    ),
  );
  return { skill_key: sk, skill_invocation_params: sip, encapsulation_target: enc };
}

function parseCredentialsJson(text) {
  const t = text.trim();
  if (!t.startsWith('{')) return null;
  try {
    const obj = JSON.parse(t);
    if (!obj || typeof obj !== 'object') return null;
    const data = obj.data;
    let ak = null;
    if (data && typeof data === 'object') ak = data.api_key;
    if (ak && typeof ak === 'object' && ak.public_key && ak.secret_key) {
      return [String(ak.public_key).trim(), String(ak.secret_key).trim()];
    }
    ak = obj.api_key;
    if (ak && typeof ak === 'object' && ak.public_key && ak.secret_key) {
      return [String(ak.public_key).trim(), String(ak.secret_key).trim()];
    }
    if (obj.public_key && obj.secret_key) {
      return [String(obj.public_key).trim(), String(obj.secret_key).trim()];
    }
  } catch {
    return null;
  }
  return null;
}

function parseCredentialsLine(line) {
  line = line.trim();
  if (!line || line.startsWith('#')) return null;
  const i = line.indexOf(':');
  if (i === -1) return null;
  const pub = line.slice(0, i).trim();
  const sec = line.slice(i + 1).trim();
  if (pub && sec) return [pub, sec];
  return null;
}

function headersXApiKey(publicKey, secretKey) {
  return {
    'Content-Type': 'application/json',
    'x-api-key': `${publicKey}:${secretKey}`,
  };
}

function buildApiKeysFetchUrl(baseUrl) {
  const root = baseUrl.replace(/\/+$/, '');
  const aid = (process.env.ACCOUNT_ID || process.env.PRANA_ACCOUNT_ID || '').trim();
  if (aid) {
    const q = new URLSearchParams({ account_id: aid });
    return `${root}/api/v1/api-keys?${q.toString()}`;
  }
  return `${root}/api/v1/api-keys`;
}

async function fetchPranaApiKeysViaGet(baseUrl) {
  const url = buildApiKeysFetchUrl(baseUrl);
  try {
    const res = await fetch(url, {
      method: 'GET',
      signal: AbortSignal.timeout(API_KEYS_FETCH_TIMEOUT_MS),
    });
    const text = await res.text();
    if (!res.ok) {
      console.error(`错误: 自动获取 API key 失败（HTTP ${res.status}）：${text.slice(0, 2000)}`);
      return null;
    }
    const parsed = parseCredentialsJson(text);
    if (!parsed) {
      console.error('错误: 自动获取 API key 成功但响应无法解析出 public_key/secret_key。');
      return null;
    }
    return parsed;
  } catch (e) {
    console.error(`错误: 自动获取 API key 失败（网络）：${e && e.message ? e.message : e}`);
    return null;
  }
}

function persistFetchedApiKeyTxt(publicKey, secretKey) {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
  const lines = [
    '# Auto-saved by prana_skill_client after GET /api/v1/api-keys; do not commit to public repos.',
    `${publicKey}:${secretKey}`,
    '',
  ];
  fs.writeFileSync(API_KEY_FILE, lines.join('\n'), 'utf8');
}

async function loadPranaCredentials(pranaBaseUrl) {
  let pk = (process.env.PRANA_SKILL_PUBLIC_KEY || '').trim();
  let sk = (process.env.PRANA_SKILL_SECRET_KEY || '').trim();
  if (pk && sk) return [pk, sk];

  const rawEnv = (process.env.PRANA_SKILL_API_KEY || '').trim();
  if (rawEnv) {
    const parsed = parseCredentialsJson(rawEnv);
    if (parsed) return parsed;
    const pl = parseCredentialsLine(rawEnv);
    if (pl) return pl;
  }

  if (fs.existsSync(API_KEY_FILE)) {
    const txt = fs.readFileSync(API_KEY_FILE, 'utf8');
    const lines = txt
      .split(/\r?\n/)
      .filter((ln) => ln.trim() && !ln.trim().startsWith('#'));
    const joined = lines.join('\n').trim();
    if (joined) {
      const pj = parseCredentialsJson(joined);
      if (pj) return pj;
      for (const line of lines) {
        const pl = parseCredentialsLine(line);
        if (pl) return pl;
      }
    }
  }

  const base = (
    pranaBaseUrl ||
    process.env.NEXT_PUBLIC_URL ||
    DEFAULT_PRANA_BASE ||
    ''
  ).trim();
  if (base && !autoFetchApiKeyDisabled()) {
    const fetched = await fetchPranaApiKeysViaGet(base);
    if (fetched) {
      const [pub, sec] = fetched;
      if (!skipWriteFetchedApiKey()) {
        try {
          persistFetchedApiKeyTxt(pub, sec);
        } catch (e) {
          console.error(`警告: 无法写入 config/api_key.txt：${e && e.message ? e.message : e}`);
        }
      }
      return [pub, sec];
    }
  }

  console.error(
    '错误: 未配置 API 凭证（public_key + secret_key），且自动 GET /api/v1/api-keys 失败或未启用。\n' +
      '  可选方式：\n' +
      '  1) 设置 PRANA_SKILL_PUBLIC_KEY + PRANA_SKILL_SECRET_KEY，或 PRANA_SKILL_API_KEY；或写入 config/api_key.txt。\n' +
      '  2) 保证 --base-url（或 NEXT_PUBLIC_URL）可访问，并确保未设置 PRANA_SKILL_NO_AUTO_API_KEY；' +
      '可选设置 ACCOUNT_ID / PRANA_ACCOUNT_ID 以附加 account_id；成功后默认写入 config/api_key.txt（' +
      '若不想写盘可设 PRANA_SKILL_SKIP_WRITE_API_KEY=1）。',
  );
  process.exit(2);
}

function buildInvokeContent(cfg, userMessage) {
  const paramsFromSkill = (cfg.skill_invocation_params || '').trim();
  return [`参数：${paramsFromSkill}`, `用户消息：${userMessage}`].join('\n');
}

async function fetchAgentResult(baseUrl, requestId, publicKey, secretKey) {
  const url = `${baseUrl.replace(/\/+$/, '')}/api/claw/agent-result`;
  const body = { request_id: requestId };
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: headersXApiKey(publicKey, secretKey),
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(HTTP_TIMEOUT_MS),
    });
    const text = await res.text();
    if (!res.ok) {
      try {
        return JSON.parse(text);
      } catch {
        return {
          error: true,
          status: res.status,
          detail: text,
          _from: 'agent-result',
        };
      }
    }
    try {
      return JSON.parse(text);
    } catch {
      return {
        error: true,
        status: res.status,
        detail: text,
        _from: 'agent-result',
      };
    }
  } catch (e) {
    return {
      error: true,
      detail: String(e && e.reason != null ? e.reason : e && e.message ? e.message : e),
      _from: 'agent-result',
    };
  }
}

function agentResultPayloadStillRunning(payload) {
  if (payload.error === true) return false;
  const data = payload.data;
  if (!data || typeof data !== 'object') return false;
  return String(data.status || '')
    .trim()
    .toLowerCase() === 'running';
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function markRecovered(d) {
  return { ...d, _recovered_via: 'agent-result' };
}

async function pollAgentResultUntilSettled(
  baseUrl,
  requestId,
  publicKey,
  secretKey,
  triggerReason = '需通过 agent-result 拉取结果',
) {
  const interval = Math.max(1, AGENT_RESULT_POLL_INTERVAL_SEC);
  const maxAttempts = Math.max(1, AGENT_RESULT_POLL_MAX_ATTEMPTS);
  let last = {};
  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    if (attempt === 1) {
      console.error(
        `提示: ${triggerReason}，${interval} 秒后首次 POST /api/claw/agent-result … ` +
          `(request_id=${requestId}, 最多 ${maxAttempts} 次，每 ${interval}s)`,
      );
    } else {
      console.error(`提示: 第 ${attempt} 次查询 agent-result（间隔 ${interval}s）…`);
    }
    await sleep(interval * 1000);
    last = await fetchAgentResult(baseUrl, requestId, publicKey, secretKey);
    if (agentResultPayloadStillRunning(last)) continue;
    return markRecovered(last);
  }
  console.error(`警告: agent-result 已轮询 ${maxAttempts} 次仍未结束，返回最后一次响应。`);
  return markRecovered(last);
}

async function invokePrana(
  baseUrl,
  skillKey,
  content,
  threadId,
  requestId,
  publicKey,
  secretKey,
) {
  const url = `${baseUrl.replace(/\/+$/, '')}/api/claw/agent-run`;
  const body = {
    skill_key: skillKey,
    question: content,
    thread_id: threadId || '',
    request_id: requestId,
  };
  const opts = {
    method: 'POST',
    headers: headersXApiKey(publicKey, secretKey),
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(HTTP_TIMEOUT_MS),
  };
  try {
    const res = await fetch(url, opts);
    const raw = await res.text();
    if (!res.ok) {
      if (res.status >= 500 || res.status === 408 || res.status === 504) {
        return pollAgentResultUntilSettled(
          baseUrl,
          requestId,
          publicKey,
          secretKey,
          `agent-run HTTP ${res.status}，改查 agent-result`,
        );
      }
      try {
        return JSON.parse(raw);
      } catch {
        return { error: true, status: res.status, detail: raw };
      }
    }
    try {
      return JSON.parse(raw);
    } catch {
      return pollAgentResultUntilSettled(
        baseUrl,
        requestId,
        publicKey,
        secretKey,
        'agent-run 响应非合法 JSON',
      );
    }
  } catch (e) {
    return pollAgentResultUntilSettled(
      baseUrl,
      requestId,
      publicKey,
      secretKey,
      'agent-run 网络异常',
    );
  }
}

async function main() {
  let values;
  try {
    const parsed = parseArgs({
      args: process.argv.slice(2),
      options: {
        message: { type: 'string', short: 'm' },
        'thread-id': { type: 'string', short: 't', default: '' },
        'base-url': { type: 'string', short: 'b', default: DEFAULT_PRANA_BASE },
        help: { type: 'boolean', short: 'h', default: false },
      },
      allowPositionals: false,
    });
    values = parsed.values;
    if (values.help) {
      console.log(
        '用法: node scripts/prana_skill_client.js -m "用户消息" [-t thread_id] [-b base_url]',
      );
      process.exit(0);
    }
    if (!values.message) {
      console.error('错误: 必须使用 -m / --message 提供用户消息 / 任务描述');
      process.exit(1);
    }
  } catch (e) {
    console.error(e && e.message ? e.message : e);
    process.exit(1);
  }

  const cfg = loadSkillConfig();
  const skillKey = cfg.skill_key || '';
  if (!skillKey) {
    console.error('错误: 配置中缺少远端 skill_key（请检查脚本内 ENCAPSULATION_EMBEDDED 或旧版 SKILL.md）');
    process.exit(1);
  }

  const baseUrl = values['base-url'] || DEFAULT_PRANA_BASE;
  const [publicKey, secretKey] = await loadPranaCredentials(baseUrl);

  const requestId = randomUUID();
  const content = buildInvokeContent(cfg, values.message);
  const result = await invokePrana(
    baseUrl,
    skillKey,
    content,
    values['thread-id'] || null,
    requestId,
    publicKey,
    secretKey,
  );
  console.log(JSON.stringify(result, null, 2));
}

await main();
