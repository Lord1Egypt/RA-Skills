/**
 * PowPow Platform API Client
 *
 * Security model:
 * - No Supabase keys, no service credentials. All operations go through the
 *   platform's own HTTP API (https://global.powpow.online/api/...) with a
 *   per-user JWT obtained via /api/auth/login.
 * - The JWT is bound to a device fingerprint (User-Agent + Accept-Language),
 *   so we pin both headers at login time and reuse them for every call.
 * - Passwords are never persisted. Only the short-lived token is stored in
 *   the user's state directory (session.json) and it expires server-side (7 days).
 */
const fs = require('fs');
const os = require('os');
const path = require('path');

// Skill bundles are installed read-only in most agent hosts (OpenClaw included),
// so mutable state must live outside the bundled folder. Resolution order:
//   1. POWPOW_STATE_DIR            - explicit override (any host)
//   2. ~/.powpow                   - per-user default
// config.json ships with the bundle and stays read-only; only the session file
// is written, and only into the resolved state directory.
function resolveStateDir() {
  if (process.env.POWPOW_STATE_DIR) return path.resolve(process.env.POWPOW_STATE_DIR);
  return path.join(os.homedir(), '.powpow');
}

const BUNDLED_CONFIG_PATH = path.join(__dirname, '..', '..', 'config.json');
const STATE_DIR = resolveStateDir();
const SESSION_PATH = path.join(STATE_DIR, 'session.json');
const USER_CONFIG_PATH = path.join(STATE_DIR, 'config.json');

const DEFAULT_USER_AGENT = 'PowPow-Skill/2.0 (+https://global.powpow.online)';
const DEFAULT_ACCEPT_LANGUAGE = 'zh-CN,zh;q=0.9,en;q=0.8';

// The platform base URL is a security boundary: session tokens and login
// credentials are sent there. A user-writable override (state-dir config.json)
// would let a tampered file redirect credentials to an attacker host, so
// platformUrl is pinned to this whitelist and CANNOT be changed via the
// user config. To test against a staging host, edit the BUNDLED config.json.
const ALLOWED_PLATFORM_URLS = ['https://global.powpow.online'];

class SessionExpiredError extends Error {
  constructor(message = '登录已过期，请重新运行 login.js') {
    super(message);
    this.name = 'SessionExpiredError';
  }
}

class ApiError extends Error {
  constructor(status, body) {
    super(`API ${status}: ${typeof body === 'string' ? body : JSON.stringify(body)}`);
    this.name = 'ApiError';
    this.status = status;
    this.body = body;
  }
}

function loadConfig() {
  // User overrides in the state dir win over the bundled defaults for
  // NON-SECURITY settings (e.g. unsplashAccessKey, sessionMaxAgeDays).
  // platformUrl from the USER config is only honored when it is whitelisted;
  // anything else is rejected instead of silently redirecting credentials.
  const candidates = [USER_CONFIG_PATH, BUNDLED_CONFIG_PATH];
  const found = candidates.find(p => fs.existsSync(p));
  if (!found) {
    throw new Error('platformUrl config not found. A bundled config.json with { "platformUrl": "..." } is required.');
  }
  const config = JSON.parse(fs.readFileSync(found, 'utf-8'));
  if (!ALLOWED_PLATFORM_URLS.includes(config.platformUrl)) {
    // Fall back to the bundled config if the user config points elsewhere.
    if (found !== BUNDLED_CONFIG_PATH && fs.existsSync(BUNDLED_CONFIG_PATH)) {
      const bundled = JSON.parse(fs.readFileSync(BUNDLED_CONFIG_PATH, 'utf-8'));
      if (ALLOWED_PLATFORM_URLS.includes(bundled.platformUrl)) {
        return { ...config, platformUrl: bundled.platformUrl };
      }
    }
    throw new Error(`platformUrl "${config.platformUrl}" is not in the allowed list (${ALLOWED_PLATFORM_URLS.join(', ')}). Refusing to continue.`);
  }
  return config;
}

function loadSession() {
  if (!fs.existsSync(SESSION_PATH)) return null;
  try {
    const session = JSON.parse(fs.readFileSync(SESSION_PATH, 'utf-8'));
    if (!session.token) return null;
    const maxAgeDays = loadConfig().sessionMaxAgeDays || 6;
    const ageMs = Date.now() - new Date(session.loginAt).getTime();
    if (ageMs > maxAgeDays * 24 * 60 * 60 * 1000) return null;
    return session;
  } catch {
    return null;
  }
}

function saveSession(session) {
  // Owner-only permissions: the session file is a reusable bearer credential.
  fs.mkdirSync(path.dirname(SESSION_PATH), { recursive: true, mode: 0o700 });
  fs.writeFileSync(SESSION_PATH, JSON.stringify(session, null, 2), { encoding: 'utf-8', mode: 0o600 });
  try { fs.chmodSync(SESSION_PATH, 0o600); } catch { /* non-POSIX fs (e.g. win32) */ }
}

function clearSession() {
  if (fs.existsSync(SESSION_PATH)) fs.unlinkSync(SESSION_PATH);
}

function requireSession() {
  const session = loadSession();
  if (!session) {
    throw new SessionExpiredError('未登录或会话已过期。请先运行: node scripts/login.js <username>');
  }
  return session;
}

function baseHeaders(session) {
  return {
    'Content-Type': 'application/json',
    'User-Agent': session.userAgent || DEFAULT_USER_AGENT,
    'Accept-Language': session.acceptLanguage || DEFAULT_ACCEPT_LANGUAGE,
  };
}

/**
 * Login with username/password and store the JWT session.
 * Password is used only for this request and never written to disk.
 */
async function login(username, password) {
  const config = loadConfig();
  const userAgent = DEFAULT_USER_AGENT;
  const acceptLanguage = DEFAULT_ACCEPT_LANGUAGE;

  const resp = await fetch(`${config.platformUrl}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': userAgent,
      'Accept-Language': acceptLanguage,
    },
    body: JSON.stringify({ step: 1, username, password }),
    signal: AbortSignal.timeout(15000),
  });

  const body = await resp.json().catch(() => ({}));

  if (resp.status === 423) {
    throw new ApiError(423, body.error || '账户已锁定，请稍后再试');
  }
  if (resp.status === 403 && body.status === 'pending_payment') {
    throw new ApiError(403, '该账号尚未完成开通，请先在平台完成开通流程');
  }
  if (resp.status === 401) {
    throw new ApiError(401, body.error || '用户名或密码错误');
  }
  if (!resp.ok) {
    throw new ApiError(resp.status, body.error || '登录失败');
  }

  // Token in body is only returned for trusted native-bridge clients; the
  // web path sets an HttpOnly cookie. Accept either source.
  let token = body.token || body.bridgeToken || null;
  if (!token) {
    const cookies = resp.headers.getSetCookie ? resp.headers.getSetCookie() : [];
    for (const cookie of cookies) {
      const m = cookie.match(/(?:^|;\s*)powpow_token=([^;]+)/);
      if (m) { token = m[1]; break; }
    }
  }
  if (!token) {
    throw new Error('登录成功但未能获取 token（平台响应异常）');
  }

  const session = {
    token,
    username: body.user ? body.user.username : username,
    userId: body.user ? body.user.id : null,
    nickname: body.user ? body.user.nickname : null,
    userAgent,
    acceptLanguage,
    loginAt: new Date().toISOString(),
  };
  saveSession(session);
  return session;
}

/**
 * Authenticated request to the platform API. Throws SessionExpiredError on
 * 401 so callers can prompt for re-login. Transient failures (network errors,
 * 5xx) are retried once before giving up.
 */
async function api(method, apiPath, data = null) {
  const config = loadConfig();
  const session = requireSession();

  const doFetch = () => fetch(`${config.platformUrl}${apiPath}`, {
    method,
    headers: { ...baseHeaders(session), Authorization: `Bearer ${session.token}` },
    body: data ? JSON.stringify(data) : undefined,
    signal: AbortSignal.timeout(30000),
  });

  const readAndCheck = async (resp) => {
    if (resp.status === 401) {
      clearSession();
      throw new SessionExpiredError();
    }
    const body = await resp.json().catch(() => ({}));
    if (!resp.ok) throw new ApiError(resp.status, body);
    return body;
  };

  let resp;
  try {
    resp = await doFetch();
  } catch (err) {
    // one retry on transient network failure
    await new Promise(r => setTimeout(r, 2000));
    resp = await doFetch().catch(() => { throw err; });
  }

  // One retry on server errors (5xx) - transient infrastructure issues only.
  if (resp.status >= 500) {
    await new Promise(r => setTimeout(r, 2000));
    resp = await doFetch();
  }

  return readAndCheck(resp);
}

module.exports = {
  loadConfig,
  login,
  api,
  loadSession,
  clearSession,
  requireSession,
  resolveStateDir,
  STATE_DIR,
  SESSION_PATH,
  SessionExpiredError,
  ApiError,
  DEFAULT_USER_AGENT,
  DEFAULT_ACCEPT_LANGUAGE,
};
