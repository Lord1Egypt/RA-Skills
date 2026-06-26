/**
 * Kling AI HTTP client (zero external deps, Node.js 18+ fetch)
 *
 * - **klingGet / klingPost**：Bearer 鉴权 + resolveApiBase（业务 API）
 * - **runAccountBindHttpSequence**：无 Bearer，固定 bind 端点（与鉴权流量区分在实现上，不混用 token）
 */
import { createHash, randomBytes } from 'node:crypto';
import {
  getBearerToken,
  makeKlingHeaders,
  getConfiguredApiBase,
  getConfiguredBindBase,
  persistProbedApiBase,
  getSkillVersion,
  ensureIdentityForBind,
  patchKlingIdentity,
  persistBoundApiKeys,
} from './auth.mjs';

const KLING_API_ENDPOINTS = Object.freeze([
  {
    key: 'cn',
    apiBase: 'https://api-beijing.klingai.com',
    bindBase: 'https://klingai.com',
    consoleUrl: 'https://klingai.com/dev/api-key',
  },
  {
    key: 'global',
    apiBase: 'https://api-singapore.klingai.com',
    bindBase: 'https://kling.ai',
    consoleUrl: 'https://kling.ai/dev/api-key',
  },
]);

const ALL_KLING_CONSOLE_URLS = Object.freeze(
  Object.fromEntries(KLING_API_ENDPOINTS.map((item) => [item.key, item.consoleUrl])),
);

const API_BASE = KLING_API_ENDPOINTS[0].apiBase;
const CANDIDATE_BASES = KLING_API_ENDPOINTS.map((item) => item.apiBase);
export let KLING_CONSOLE_URLS = ALL_KLING_CONSOLE_URLS;

function normalizeApiBase(base) {
  return String(base || '').trim().replace(/\/+$/, '');
}

function findEndpointByBase(base) {
  const normalized = normalizeApiBase(base);
  if (!normalized) return null;
  const direct = KLING_API_ENDPOINTS.find((item) => normalizeApiBase(item.apiBase) === normalized);
  if (direct) return direct;
  const bindDirect = KLING_API_ENDPOINTS.find((item) => normalizeApiBase(item.bindBase) === normalized);
  if (bindDirect) return bindDirect;
  if (normalized.includes('api-beijing.klingai.com')) return KLING_API_ENDPOINTS.find((item) => item.key === 'cn') || null;
  if (normalized.includes('api-singapore.klingai.com')) return KLING_API_ENDPOINTS.find((item) => item.key === 'global') || null;
  if (normalized.includes('klingai.com')) return KLING_API_ENDPOINTS.find((item) => item.key === 'cn') || null;
  if (normalized.includes('kling.ai')) return KLING_API_ENDPOINTS.find((item) => item.key === 'global') || null;
  if (normalized.includes('kuaishou.com')) return KLING_API_ENDPOINTS.find((item) => item.key === 'cn') || null;
  return null;
}

function setConsoleUrlsForBase(base) {
  const endpoint = findEndpointByBase(base);
  if (!endpoint) {
    KLING_CONSOLE_URLS = ALL_KLING_CONSOLE_URLS;
    return;
  }
  KLING_CONSOLE_URLS = Object.freeze({ [endpoint.key]: endpoint.consoleUrl });
}

const initialConfiguredApiBase = getConfiguredApiBase();
if (initialConfiguredApiBase) {
  setConsoleUrlsForBase(initialConfiguredApiBase);
}

function printConsoleUrlsHint(prefix = '     ') {
  for (const [region, url] of Object.entries(KLING_CONSOLE_URLS)) {
    const label = region === 'cn' ? 'China / 国内' : (region === 'global' ? 'Global / 国际' : region);
    console.error(`${prefix}${label}: ${url}`);
  }
}

async function probeBase(base, token) {
  try {
    const res = await fetch(`${base}/v1/videos/text2video?pageNum=1&pageSize=1`, {
      method: 'GET',
      headers: makeKlingHeaders(token, null),
      signal: AbortSignal.timeout(8000),
    });
    if (!res.ok) return false;
    const json = await res.json().catch(() => null);
    return json != null && (json.code === 0 || json.code === 200);
  } catch {
    return false;
  }
}

let _resolvedBase = null;

async function resolveApiBase(token) {
  if (_resolvedBase) return _resolvedBase;
  const configuredApiBase = getConfiguredApiBase();
  if (configuredApiBase) {
    _resolvedBase = normalizeApiBase(configuredApiBase);
    setConsoleUrlsForBase(_resolvedBase);
    return _resolvedBase;
  }

  console.error('\n🔍 Probing API endpoints... / 正在检测 API 节点...');
  for (const endpoint of KLING_API_ENDPOINTS) {
    process.stderr.write(`   [${endpoint.key}] ${endpoint.apiBase} ... `);
    if (await probeBase(endpoint.apiBase, token)) {
      process.stderr.write('✓ OK\n\n');
      _resolvedBase = endpoint.apiBase;
      setConsoleUrlsForBase(_resolvedBase);
      try {
        persistProbedApiBase(_resolvedBase);
      } catch {}
      return _resolvedBase;
    }
    process.stderr.write('✗\n');
  }

  console.error('\n❌ Cannot connect to any Kling API endpoint / 无法连接任何可灵 API 节点');
  for (const base of CANDIDATE_BASES) console.error(`   • ${base}`);
  console.error('\nPossible causes / 可能原因:');
  console.error('  1. Token invalid or expired / Token 无效或已过期:');
  printConsoleUrlsHint();
  console.error('  2. Network issue / 网络问题');
  console.error('\nCheck credentials file, KLING_TOKEN, or run account configure / 检查 credentials、KLING_TOKEN 或 account configure:\n');
  process.exit(1);
}

/**
 * 保护 JSON 中的大整数字段（防止 Number 精度丢失）
 * 将 element_id, task_id 等大整数字段转为字符串
 */
function protectBigInts(text) {
  return text.replace(
    /"(element_id|task_id|elementId|taskId)":\s*(\d{15,})/g,
    '"$1":"$2"'
  );
}

/**
 * 解析可灵 API 响应，code 为 0 或 200 为成功
 */
function parseResponse(json) {
  if (json.code !== 0 && json.code !== 200) {
    throw new Error(`API error / API 错误 (code=${json.code}): ${json.message || 'Unknown error'}`);
  }
  return json.data;
}

function parseJsonSafely(text) {
  try {
    return JSON.parse(protectBigInts(String(text || '')));
  } catch {
    return null;
  }
}

function buildHttpErrorMessage(status, text) {
  const body = parseJsonSafely(text);
  if (status === 401 && body && typeof body === 'object') {
    const code = Number(body.code);
    const requestId = body.request_id ? `, request_id=${body.request_id}` : '';
    if (code === 1000) {
      return `HTTP 401: code=1000，signature is invalid / 秘钥无效，请重新绑定${requestId}`;
    }
    if (code === 1002) {
      return `HTTP 401: code=1002，access key not exist / 账户不存在，请重新绑定${requestId}`;
    }
  }
  return `HTTP ${status}: ${text}`;
}

function parseApiJsonOrThrow(text) {
  const parsed = parseJsonSafely(text);
  if (parsed != null) return parsed;
  const preview = String(text || '').trim().slice(0, 60);
  if (preview.startsWith('<')) {
    throw new Error(`API Service Error: Non-JSON content. check KLING_API_BASE and network/DNS/proxy: ${preview}`);
  }
  throw new Error(`API Service Error: Cannot parse JSON: ${preview}`);
}

async function safeFetch(url, init, context) {
  try {
    return await fetch(url, init);
  } catch (e) {
    const baseHint = getConfiguredApiBase() || '<auto>';
    const msg = e?.message || String(e);
    throw new Error(
      `Network error / 网络错误: ${msg}\n`
      + `Request / 请求: ${context.method} ${url}\n`
      + `KLING_API_BASE: ${baseHint}\n`
      + 'Hint / 提示: check KLING_API_BASE and network/DNS/proxy, or remove KLING_API_BASE to auto-probe official endpoints / '
      + '请检查 KLING_API_BASE 与网络(DNS/代理)，或移除 KLING_API_BASE 让脚本自动探测官方节点。',
    );
  }
}

/**
 * POST 请求可灵 API
 * @param {string} path  API 路径，如 /v1/videos/image2video
 * @param {object} body  请求体
 * @param {string} [token]  可选 token，不传则自动获取
 * @returns {Promise<object>} data 字段
 */
export async function klingPost(path, body, token) {
  if (!token) token = getBearerToken();
  const base = await resolveApiBase(token);
  const url = `${base}${path}`;
  const res = await safeFetch(url, {
    method: 'POST',
    headers: makeKlingHeaders(token),
    body: JSON.stringify(body),
  }, { method: 'POST' });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(buildHttpErrorMessage(res.status, text));
  }
  const text = await res.text();
  return parseResponse(parseApiJsonOrThrow(text));
}

/**
 * GET 请求可灵 API
 * @param {string} path  API 路径，如 /v1/videos/image2video/{task_id}
 * @param {string} [token]  可选 token，不传则自动获取
 * @param {{ contentType?: string|null }} [options]  如部分接口要求 `Content-Type: application/json`（传 `'application/json'`）；默认不传 Content-Type
 * @returns {Promise<object>} data 字段
 */
export async function klingGet(path, token, options = {}) {
  if (!token) token = getBearerToken();
  const base = await resolveApiBase(token);
  const ct = options.contentType !== undefined ? options.contentType : null;
  const url = `${base}${path}`;
  const res = await safeFetch(url, {
    method: 'GET',
    headers: makeKlingHeaders(token, ct),
  }, { method: 'GET' });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(buildHttpErrorMessage(res.status, text));
  }
  const text = await res.text();
  return parseResponse(parseApiJsonOrThrow(text));
}

// —— 设备绑定 HTTP（无 Authorization；不经过 resolveApiBase） ——

const DEFAULT_BIND_INIT = '/console/api/auth/skill/init-sessions';
const DEFAULT_BIND_EXCHANGE = '/console/api/auth/skill/exchange';
const DEFAULT_BIND_SKILL_ID = 'Kling-Provider-Skill';
const DEFAULT_BIND_SCOPE = 'kling.openapi.invoke';
const DEFAULT_BIND_FETCH_TIMEOUT_MS = 30000;
const DEFAULT_BIND_TIMEOUT_MS = 180000;

function sleepBind(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function base64url(input) {
  return Buffer.from(input).toString('base64')
    .replace(/=/g, '')
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
}

function createPkcePair() {
  const codeVerifier = base64url(randomBytes(48));
  const codeChallenge = base64url(createHash('sha256').update(codeVerifier, "utf8").digest());
  return { codeVerifier, codeChallenge };
}

function bindExtractData(json) {
  if (json == null || typeof json !== 'object') return json;
  const c = json.code;
  if (c !== undefined && c !== 0 && c !== 200) {
    const msg = json.message || json.msg || 'Unknown error';
    throw new Error(`Bind API error / 绑定接口错误 (code=${c}): ${msg}`);
  }
  return json.data !== undefined ? json.data : json;
}

function normalizeBindBase(base) {
  const raw = String(base || '').trim();
  return raw.replace(/\/+$/, '');
}

function resolveBindBase(bindBaseOverride) {
  const override = normalizeBindBase(bindBaseOverride);
  if (override) {
    const overrideEndpoint = findEndpointByBase(override);
    if (overrideEndpoint?.bindBase) return normalizeBindBase(overrideEndpoint.bindBase);
    return override;
  }
  const configuredBindBase = getConfiguredBindBase();
  if (configuredBindBase) return normalizeBindBase(configuredBindBase);
  const candidate = getConfiguredApiBase() || _resolvedBase || API_BASE;
  const endpoint = findEndpointByBase(candidate);
  if (endpoint?.bindBase) return normalizeBindBase(endpoint.bindBase);
  return normalizeBindBase(candidate);
}

async function skillBindHttpJson(userAgent, base, path, body, method = 'POST') {
  const b = String(base || '').replace(/\/$/, '');
  const p = path.startsWith('/') ? path : `/${path}`;
  const url = method === 'GET' && body && typeof body === 'object'
    ? `${b}${p}${p.includes('?') ? '&' : '?'}${new URLSearchParams(
        Object.entries(body).filter(([, v]) => v != null).map(([k, v]) => [k, String(v)]),
      ).toString()}`
    : `${b}${p}`;
  const headers = { 'User-Agent': userAgent };
  if (method !== 'GET') headers['Content-Type'] = 'application/json';
  const init = {
    method,
    headers,
    signal: AbortSignal.timeout(DEFAULT_BIND_FETCH_TIMEOUT_MS),
  };
  if (method !== 'GET' && body != null) init.body = JSON.stringify(body);
  let res;
  try {
    res = await fetch(url, init);
  } catch (e) {
    throw new Error(
      `Network error / 网络错误: ${e?.message || e}\n`
      + 'Hint / 提示: check network/DNS/proxy and endpoint reachability / 请检查网络、DNS、代理与目标地址可达性。',
    );
  }
  const text = await res.text().catch(() => '');
  if (!res.ok) {
    throw new Error(
      `HTTP ${res.status}: ${text}\n`
      + 'Hint / 提示: verify API base and network reachability / 请确认 API 基址与网络可达性。',
    );
  }
  let json;
  try {
    json = JSON.parse(text);
  } catch {
    throw new Error(`Invalid JSON / 非 JSON 响应: ${text.slice(0, 200)}`);
  }
  return bindExtractData(json);
}

function pickBindSessionId(data) {
  if (!data || typeof data !== 'object') return null;
  return data.session_id || data.sessionId || data.bind_session_id || data.id || null;
}

function pickBindAuthorizeHint(data) {
  if (!data || typeof data !== 'object') return null;
  return (
    data.verificationUriComplete
    || data.verification_uri_complete
    || data.verificationUri
    || data.verification_uri
    || data.authorize_url
    || data.authorization_url
    || data.qr_url
    || null
  );
}

function pickBindAccessSecretKeys(data) {
  const src = data?.credential && typeof data.credential === 'object' ? data.credential : data;
  if (!src || typeof src !== 'object') {
    return {
      ak: null, sk: null, credentialId: null, accountId: null,
    };
  }
  const ak = src.accessKey || src.access_key || src.access_key_id || src.accessKeyId || src.ak;
  const sk = src.secretKey || src.secret_key || src.secret_access_key || src.secretAccessKey || src.sk;
  const credentialId = src.credentialId || src.credential_id || src.credentialID || src.credentialid;
  const accountId = src.accountId || src.account_id || src.accountID || src.accountid;
  return {
    ak: ak != null ? String(ak).trim() : null,
    sk: sk != null ? String(sk).trim() : null,
    credentialId: credentialId != null ? String(credentialId).trim() : null,
    accountId: accountId != null ? String(accountId).trim() : null,
  };
}

function normalizeBindStatus(data) {
  if (!data || typeof data !== 'object') return 'pending';
  const s = data.status || data.state || data.bind_status || data.phase;
  if (s == null) return 'pending';
  return String(s).toUpperCase();
}

function makeBindFlowError(message, meta = {}) {
  const err = new Error(message);
  err.name = 'BindFlowError';
  if (meta.code) err.bindCode = meta.code;
  if (meta.authorizeUrl) err.bindAuthorizeUrl = meta.authorizeUrl;
  if (meta.sessionId) err.bindSessionId = meta.sessionId;
  if (meta.status) err.bindStatus = meta.status;
  if (meta.responseData !== undefined) err.bindResponseData = meta.responseData;
  return err;
}

function resolveAuthorizationUrl(bindBase, authorizePathOrUrl) {
  const raw = String(authorizePathOrUrl || '').trim();
  if (!raw) return null;
  if (raw.startsWith('http://') || raw.startsWith('https://')) return raw;
  const baseUrl = new URL(`${normalizeBindBase(bindBase)}/`);
  if (raw.startsWith('/')) return `${baseUrl.origin}${raw}`;
  return new URL(raw, baseUrl).toString();
}

function defaultBindOnLog(ev) {
  if (ev.url) {
    console.error(`${ev.message}\n  ${ev.url}`);
  } else {
    console.error(ev.message);
  }
}

function maskSecret(secret) {
  const s = String(secret || '');
  if (!s) return '';
  if (s.length <= 6) return '***';
  return `${s.slice(0, 3)}***${s.slice(-2)}`;
}

function maskAccessKey(accessKey) {
  const s = String(accessKey || '');
  if (!s) return '';
  if (s.length <= 8) return `${s.slice(0, 2)}***`;
  return `${s.slice(0, 4)}***${s.slice(-3)}`;
}

/**
 * 执行完整设备绑定并写入 credentials（供 account 与 getTokenOrExit 自动调用）
 * @param {{ onLog?: function }} [options]
 */
export async function runDeviceBindFlow(options = {}) {
  const onLog = options.onLog || defaultBindOnLog;
  const identity = ensureIdentityForBind();
  const {
    client_instance_id, device_name, platform, hostname,
  } = identity;
  const userAgent = `Kling-Provider-Skill/${getSkillVersion()}`;

  const result = await runAccountBindHttpSequence({
    userAgent,
    skillVersion: getSkillVersion(),
    identity: {
      clientInstanceId: client_instance_id,
      deviceName: device_name,
      platform,
      hostname,
    },
    onInitSession: (sessionId) => {
      patchKlingIdentity({ session_id: sessionId });
    },
    onLog,
  });
  const persisted = persistBoundApiKeys(
    result.accessKey,
    result.secretKey,
    { session_id: result.sessionId },
    {
      credentialId: result.credentialId || null,
      accountId: result.accountId || null,
    },
  );
  return {
    sessionId: result.sessionId,
    authorizeUrl: result.authorizeHint || null,
    savePath: persisted.savePath,
    accessKeyMasked: maskAccessKey(result.accessKey),
    secretKeyMasked: maskSecret(result.secretKey),
  };
}

/**
 * 仅执行绑定前置：init → verify，返回可手动打开的授权 URL。
 * @param {{ onLog?: function }} [options]
 */
export async function prepareDeviceBindUrl(options = {}) {
  const onLog = options.onLog || defaultBindOnLog;
  const identity = ensureIdentityForBind();
  const {
    client_instance_id, device_name, platform, hostname,
  } = identity;
  const userAgent = `Kling-Provider-Skill/${getSkillVersion()}`;
  const result = await runAccountBindInitVerify({
    userAgent,
    skillVersion: getSkillVersion(),
    identity: {
      clientInstanceId: client_instance_id,
      deviceName: device_name,
      platform,
      hostname,
    },
    onInitSession: (sessionId) => {
      patchKlingIdentity({ session_id: sessionId });
    },
    onLog,
  });
  return {
    sessionId: result.sessionId,
    authorizeUrl: result.authorizeHint || null,
  };
}

/**
 * 账号绑定前半段：init → verify，拿到可给用户手动打开的授权 URL。
 * @returns {Promise<{sessionId: string, authorizeHint: string|null}>}
 */
export async function runAccountBindInitVerify(options) {
  const bindBase = options.bindBase ? normalizeBindBase(options.bindBase) : resolveBindBase();
  const initPath = options.initPath || DEFAULT_BIND_INIT;
  const {
    clientInstanceId,
    deviceName,
    platform,
    hostname,
  } = options.identity || {};
  if (!clientInstanceId) {
    throw makeBindFlowError('identity.clientInstanceId is required / 缺少 identity.clientInstanceId', { code: 'MISSING_CLIENT_INSTANCE_ID' });
  }
  const userAgent = String(options.userAgent || 'Kling-Provider-Skill/unknown');
  const skillVersion = String(options.skillVersion || getSkillVersion());
  const onLog = typeof options.onLog === 'function' ? options.onLog : () => {};
  const onInitSession = options.onInitSession;
  const { codeVerifier, codeChallenge } = createPkcePair();
  onLog({ step: 'base', message: 'Using bind base / 当前 bind 基址:', url: bindBase });

  onLog({ step: 'init', message: 'Calling init-sessions / 调用 init-sessions …' });
  const initData = await skillBindHttpJson(userAgent, bindBase, initPath, {
    skillId: DEFAULT_BIND_SKILL_ID,
    skillVersion,
    clientInstanceId,
    deviceName: String(deviceName || '').trim() || 'unknown',
    platform: String(platform || '').trim() || 'unknown',
    hostname: String(hostname || '').trim() || 'unknown',
    requestedScopes: [DEFAULT_BIND_SCOPE],
    codeChallenge,
    codeChallengeMethod: 'S256',
  });
  const sessionId = pickBindSessionId(initData);
  if (!sessionId) {
    throw makeBindFlowError(
      'init-sessions response missing sessionId / init-sessions 响应缺少 sessionId',
      { code: 'MISSING_SESSION_ID' },
    );
  }
  if (onInitSession) await onInitSession(sessionId);
  const deviceCode = String(initData.deviceCode || initData.device_code || '').trim();
  if (!deviceCode) {
    throw makeBindFlowError(
      'init-sessions response missing deviceCode / init-sessions 响应缺少 deviceCode',
      { code: 'MISSING_DEVICE_CODE', sessionId },
    );
  }
  const authorizeHint = resolveAuthorizationUrl(bindBase, pickBindAuthorizeHint(initData));
  if (!authorizeHint) {
    throw makeBindFlowError(
      'init-sessions response missing authorize url / init-sessions 响应缺少授权链接',
      { code: 'MISSING_AUTHORIZE_URL', sessionId },
    );
  }

  onLog({ step: 'authorize', message: 'Open in browser / 请在浏览器完成授权:', url: authorizeHint });
  return {
    sessionId,
    deviceCode,
    codeVerifier,
    authorizeHint,
    interval: Number(initData.interval),
    expiresIn: Number(initData.expiresIn),
  };
}

/**
 * 账号设备绑定：init → verify → 轮询 check。无 Bearer；凭证落盘由调用方配合 auth 负责。
 */
export async function runAccountBindHttpSequence(options) {
  const bindBase = resolveBindBase(options.bindBase);
  const exchangePath = options.exchangePath || DEFAULT_BIND_EXCHANGE;
  const timeoutMs = Math.max(1000, Number(options.timeoutMs ?? DEFAULT_BIND_TIMEOUT_MS));
  const userAgent = String(options.userAgent || 'Kling-Provider-Skill/unknown');
  const onLog = typeof options.onLog === 'function' ? options.onLog : () => {};
  const {
    sessionId,
    deviceCode,
    codeVerifier,
    authorizeHint,
    expiresIn,
  } = await runAccountBindInitVerify({
    ...options,
    bindBase,
    userAgent,
    onLog,
  });

  const deadline = Date.now() + timeoutMs;

  // 服务端已返回 ttl，优先取较小值避免本地等待过长。
  let remainingTtlSec = Number.isFinite(Number(expiresIn))
    ? Number(expiresIn)
    : null;

  while (Date.now() < deadline) {
    if (remainingTtlSec != null && remainingTtlSec <= 0) {
      throw makeBindFlowError('Bind expired / 绑定已过期', {
        code: 'BIND_EXPIRED',
        authorizeUrl: authorizeHint,
        sessionId,
        status: 'EXPIRED',
      });
    }
    onLog({ step: 'exchange', message: 'Polling exchange / 轮询 exchange …' });
    const exchangeData = await skillBindHttpJson(userAgent, bindBase, exchangePath, {
      sessionId,
      deviceCode,
      codeVerifier,
    }, 'POST');
    const status = normalizeBindStatus(exchangeData);
    if (status === 'ISSUED' || status === 'ALREADY_EXCHANGED') {
      const {
        ak, sk, credentialId, accountId,
      } = pickBindAccessSecretKeys(exchangeData);
      if (!ak || !sk) {
        throw makeBindFlowError(`${status} without credential / ${status} 但缺少 credential`, {
          code: 'MISSING_CREDENTIAL',
          authorizeUrl: authorizeHint,
          sessionId,
          status,
          responseData: exchangeData,
        });
      }
      return {
        sessionId,
        authorizeHint,
        accessKey: ak,
        secretKey: sk,
        credentialId,
        accountId,
        status,
      };
    }
    if (status !== 'PENDING') {
      throw makeBindFlowError(`Bind status: ${status}`, {
        code: 'BIND_STATUS',
        authorizeUrl: authorizeHint,
        sessionId,
        status,
        responseData: exchangeData,
      });
    }
    const waitSec = Number(exchangeData?.pollAfterSeconds);
    const nextExpiresSec = Number(exchangeData?.expiresIn);
    if (Number.isFinite(nextExpiresSec)) remainingTtlSec = nextExpiresSec;
    if (!Number.isFinite(waitSec) || waitSec <= 0) {
      throw makeBindFlowError('Missing pollAfterSeconds, treat as timeout / 缺少 pollAfterSeconds，按超时处理', {
        code: 'BIND_TIMEOUT',
        authorizeUrl: authorizeHint,
        sessionId,
        status,
      });
    }
    await sleepBind(waitSec * 1000);
  }

  throw makeBindFlowError(`Bind timeout / 绑定超时（>${timeoutMs}ms）`, {
    code: 'BIND_TIMEOUT',
    authorizeUrl: authorizeHint,
    sessionId,
    status: 'TIMEOUT',
  });
}

export { getBearerToken, makeKlingHeaders, setSkillVersion, getSkillVersion } from './auth.mjs';
export { API_BASE, CANDIDATE_BASES, resolveApiBase };
