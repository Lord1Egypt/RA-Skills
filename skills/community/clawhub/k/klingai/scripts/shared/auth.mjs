/**
 * Kling AI — 鉴权层（无网络）
 *
 * 凭证优先级：
 *   1. 当前进程 KLING_API_KEY（仅环境变量显式传入，不落盘；原样作为 Bearer）
 *   2. ~/.config/kling/.credentials（INI，[profile] api_key）→ 原样作为 Bearer，不再签 JWT
 * bind / configure 写入 credentials，固定 default profile。
 * 存储根目录默认 ~/.config/kling；可选 KLING_STORAGE_ROOT 指向统一存储根。
 * 非凭证 env：仅读 <storageRoot>/kling.env，不覆盖启动前已在 process.env 中的键。
 * 探测得到的 API Base 由 client 调用 `persistProbedApiBase` 写回 ~/.config/kling/kling.env 中的 KLING_API_BASE；
 * **不会**从文件注入 KLING_API_KEY（凭证仅 credentials 文件 + 可选进程内 KLING_API_KEY）。不认 KLING_TOKEN。
 *
 * 网络与 API Base 探测统一在 client.mjs。
 */
import { randomUUID } from 'node:crypto';
import {
  readFileSync, writeFileSync, mkdirSync, chmodSync,
} from 'node:fs';
import { dirname, resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createInterface } from 'node:readline';
import os from 'node:os';

const __dir = dirname(fileURLToPath(import.meta.url));

const KLING_ENV_FILENAME = 'kling.env';
const IDENTITY_FILENAME = 'identity.json';
const CREDENTIALS_FILENAME = '.credentials';
const STORAGE_ROOT_ENV = 'KLING_STORAGE_ROOT';

/** 写入 process.env 时跳过（凭证不走 dotenv 文件） */
const CREDENTIAL_ENV_DENYLIST = new Set(['KLING_API_KEY', 'KLING_TOKEN']);

/**
 * @param {string} content
 */
function parseEnvContent(content) {
  for (const line of content.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eqIdx = trimmed.indexOf('=');
    if (eqIdx <= 0) continue;
    const key = trimmed.slice(0, eqIdx).trim();
    if (CREDENTIAL_ENV_DENYLIST.has(key)) continue;
    let val = trimmed.slice(eqIdx + 1).trim();
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    // 启动前已存在的键优先。只查询文件里的这一个键，不枚举 process.env。
    if (!Object.hasOwn(process.env, key)) {
      process.env[key] = val;
    }
  }
}

export function getKlingConfigDir() {
  const explicitRoot = (process.env[STORAGE_ROOT_ENV] || '').trim();
  if (explicitRoot) return resolve(explicitRoot);
  const home = process.env.HOME || process.env.USERPROFILE;
  if (home) return join(home, '.config', 'kling');
  return resolve(__dir, '..', '..', '..');
}

function getDefaultKlingEnvPath() {
  return join(getKlingConfigDir(), KLING_ENV_FILENAME);
}

/** 更新或追加 KLING_API_BASE=…，仅写入 ~/.config/kling/kling.env */
function upsertEnvFileKey(content, key, value) {
  const line = `${key}=${value}`;
  const escaped = key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const re = new RegExp(`^${escaped}=.*$`, 'm');
  if (re.test(content)) return content.replace(re, line);
  const trimmed = content.replace(/\s+$/, '');
  if (!trimmed) return `${line}\n`;
  return `${trimmed}\n${line}\n`;
}

(function loadEnvFiles() {
  try {
    parseEnvContent(readFileSync(getDefaultKlingEnvPath(), 'utf-8'));
  } catch {}
})();

export function getIdentityFilePath() {
  return join(getKlingConfigDir(), IDENTITY_FILENAME);
}

/** 凭证 INI 路径：<storageRoot>/.credentials */
export function getCredentialsFilePath() {
  return join(getKlingConfigDir(), CREDENTIALS_FILENAME);
}

export function getActiveProfile() {
  return 'default';
}

export class CredentialsMissingError extends Error {
  constructor(msg = 'No credentials / 未配置凭证') {
    super(msg);
    this.name = 'CredentialsMissingError';
  }
}

function logAuthSource(source) {
  const messageMap = {
    credentials: 'Auth source / 鉴权来源: credentials (api_key -> Bearer)',
    env_api_key: 'Auth source / 鉴权来源: KLING_API_KEY (process env)',
  };
  const msg = messageMap[source];
  if (msg) console.error(msg);
}

function parseCredentialsIni(content) {
  const profiles = {};
  let current = null;
  for (const line of content.split('\n')) {
    const t = line.trim();
    if (!t || t.startsWith('#') || t.startsWith(';')) continue;
    const m = t.match(/^\[([^\]]+)\]\s*$/);
    if (m) {
      current = m[1].trim();
      if (!profiles[current]) profiles[current] = {};
      continue;
    }
    const eqIdx = t.indexOf('=');
    if (eqIdx <= 0 || !current) continue;
    const k = t.slice(0, eqIdx).trim();
    let v = t.slice(eqIdx + 1).trim();
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
      v = v.slice(1, -1);
    }
    profiles[current][k] = v;
  }
  return profiles;
}

const LEGACY_CREDENTIAL_KEYS = ['access_key_id', 'secret_access_key', 'access_key', 'secret_key'];

function stripLegacyCredentialKeys(obj = {}) {
  const next = { ...obj };
  for (const k of LEGACY_CREDENTIAL_KEYS) delete next[k];
  return next;
}

/** @returns {{ api_key: string, access_key_id: string, secret_access_key: string }} */
export function readCredentialsProfile(profile) {
  try {
    const raw = readFileSync(getCredentialsFilePath(), 'utf-8');
    const all = parseCredentialsIni(raw);
    const p = all[profile] || {};
    const apiKey = String(p.api_key || p.apikey || p.apiKey || '').trim();
    const ak = String(p.access_key_id || p.access_key || '').trim();
    const sk = String(p.secret_access_key || p.secret_key || '').trim();
    return { api_key: apiKey, access_key_id: ak, secret_access_key: sk };
  } catch {
    return { api_key: '', access_key_id: '', secret_access_key: '' };
  }
}

export function hasStoredApiKey() {
  const { api_key } = readCredentialsProfile(getActiveProfile());
  return Boolean(api_key);
}

/** @deprecated 与 hasStoredApiKey 相同；旧 AK/SK 不再视为可用凭证 */
export function hasStoredAccessKeys() {
  return hasStoredApiKey();
}

export function hasSessionBearerOverride() {
  return Boolean((process.env.KLING_API_KEY || '').trim());
}

export function hasUsableCredentialSource() {
  return hasStoredApiKey() || hasSessionBearerOverride();
}

/**
 * 写入 [profile] 下 api_key，并清除历史 AK/SK 键；Unix 上 chmod 600
 * @param {string} profile
 * @param {string} apiKey
 * @param {Record<string,string>} [extra]  如 credentialId / accountId
 */
export function writeCredentialsProfile(profile, apiKey, extra = {}) {
  const path = getCredentialsFilePath();
  mkdirSync(dirname(path), { recursive: true });
  let all = {};
  try {
    all = parseCredentialsIni(readFileSync(path, 'utf-8'));
  } catch {}
  const cleanedExtra = {};
  for (const [k, v] of Object.entries(extra || {})) {
    if (v == null || String(v) === '') continue;
    cleanedExtra[k] = String(v);
  }
  all[profile] = {
    ...stripLegacyCredentialKeys(all[profile]),
    api_key: String(apiKey || '').trim(),
    ...cleanedExtra,
  };
  const lines = [];
  for (const prof of Object.keys(all)) {
    lines.push(`[${prof}]`);
    const o = all[prof];
    for (const [k, v] of Object.entries(o)) {
      if (v == null || String(v) === '') continue;
      lines.push(`${k} = ${String(v)}`);
    }
    lines.push('');
  }
  writeFileSync(path, lines.join('\n').trimEnd() + '\n');
  try {
    if (process.platform !== 'win32') chmodSync(path, 0o600);
  } catch {}
  return path;
}

// —— Skill 版本 / 请求头 ——
const DEFAULT_SKILL_VERSION = '1.0.0';
let skillVersion = DEFAULT_SKILL_VERSION;
export function setSkillVersion(version) {
  skillVersion = String(version || DEFAULT_SKILL_VERSION);
}
export function getSkillVersion() {
  return skillVersion;
}

export function makeKlingHeaders(token, contentType = 'application/json') {
  const h = { 'User-Agent': `Kling-Provider-Skill/${getSkillVersion()}` };
  if (token) h['Authorization'] = `Bearer ${token}`;
  if (contentType) h['Content-Type'] = contentType;
  return h;
}

/**
 * 1) 进程环境变量 KLING_API_KEY（不落盘；kling.env 不会注入 KLING_API_KEY）
 * 2) 否则 credentials 文件 api_key → 原样作为 Bearer（不再签 JWT）
 * 不认 KLING_TOKEN。
 */
export function getBearerToken() {
  let token = (process.env.KLING_API_KEY || '').trim();
  if (token) {
    logAuthSource('env_api_key');
    if (token.toLowerCase().startsWith('bearer ')) {
      token = token.slice(7).trim();
    }
    return token;
  }
  const profile = getActiveProfile();
  const { api_key, access_key_id, secret_access_key } = readCredentialsProfile(profile);
  if (api_key) {
    logAuthSource('credentials');
    return api_key;
  }
  if (access_key_id || secret_access_key) {
    console.error(
      'Warning / 提示: stored AK/SK is ignored; re-run account --bind-url --force to get an API Key / '
      + '本地 AK/SK 已停用，请重新绑定以获取 API Key',
    );
  }
  throw new CredentialsMissingError(
    'Configure credentials under KLING_STORAGE_ROOT (or ~/.config/kling), set KLING_API_KEY for this session, or run account bind/configure / '
    + '请在 KLING_STORAGE_ROOT（或 ~/.config/kling）下配置 credentials、本次 shell 导出 KLING_API_KEY，或执行 account --bind|--configure',
  );
}

export function getConfiguredApiBase() {
  const baseTest = (process.env.KLING_API_BASE_TEST || '').trim();
  if (baseTest) return baseTest;
  const base = (process.env.KLING_API_BASE || '').trim();
  return base || null;
}

export function getConfiguredBindBase() {
  const baseTest = (process.env.KLING_BIND_BASE_TEST || '').trim();
  if (baseTest) return baseTest;
  const base = (process.env.KLING_BIND_BASE || '').trim();
  return base || null;
}

/** 将探测到的业务 API 根写入 ~/.config/kling/kling.env（仅 KLING_API_BASE 一行） */
export function persistProbedApiBase(baseUrl) {
  const b = String(baseUrl || '').trim();
  if (!b) return;
  const dir = getKlingConfigDir();
  const path = getDefaultKlingEnvPath();
  mkdirSync(dir, { recursive: true });
  let raw = '';
  try {
    raw = readFileSync(path, 'utf-8');
  } catch {}
  writeFileSync(path, upsertEnvFileKey(raw, 'KLING_API_BASE', b));
  process.env.KLING_API_BASE = b;
}

export function readIdentity() {
  try {
    const raw = readFileSync(getIdentityFilePath(), 'utf-8');
    const o = JSON.parse(raw);
    return o && typeof o === 'object' ? o : null;
  } catch {
    return null;
  }
}

function writeIdentity(obj) {
  const dir = getKlingConfigDir();
  mkdirSync(dir, { recursive: true });
  writeFileSync(getIdentityFilePath(), `${JSON.stringify(obj, null, 2)}\n`);
}

export function ensureIdentityForBind() {
  const existing = readIdentity() || {};
  const id = { ...existing };
  let dirty = Object.keys(existing).length === 0;
  if (!id.client_instance_id) {
    id.client_instance_id = randomUUID();
    dirty = true;
  }
  const localHostname = (() => {
    try {
      const h = String(os.hostname() || '').trim();
      return h || 'unknown';
    } catch {
      return 'unknown';
    }
  })();
  if (!id.hostname) {
    id.hostname = localHostname;
    dirty = true;
  }
  if (!id.device_name) {
    const n = String(process.env.COMPUTERNAME || process.env.HOSTNAME || id.hostname || '').trim();
    id.device_name = n || 'unknown';
    dirty = true;
  }
  if (!id.platform) {
    if (process.platform === 'darwin') id.platform = 'macOS';
    else if (process.platform === 'win32') id.platform = 'Windows';
    else if (process.platform === 'linux') id.platform = 'Linux';
    else id.platform = 'unknown';
    dirty = true;
  }
  id.version = id.version ?? 1;
  if (id.session_id === undefined) id.session_id = null;
  id.updated_at = Date.now();
  if (dirty) writeIdentity(id);
  return id;
}

export function patchKlingIdentity(patch) {
  const cur = readIdentity() || {};
  const next = { ...cur, ...patch, updated_at: Date.now() };
  writeIdentity(next);
  return next;
}

/** 绑定 / configure 成功后写入 credentials；identity 中不保留明文 API Key / AK/SK */
export function persistBoundApiKeys(apiKey, extraIdentity = {}, extraCredentials = {}) {
  const key = String(apiKey || '').trim();
  if (!key) throw new Error('Missing api_key / 缺少 api_key');
  const profile = getActiveProfile();
  const savePath = writeCredentialsProfile(profile, key, extraCredentials);
  const cur = readIdentity() || {};
  const next = { ...cur, ...extraIdentity, bound_at: Date.now(), updated_at: Date.now() };
  for (const k of LEGACY_CREDENTIAL_KEYS) delete next[k];
  delete next.api_key;
  delete next.apiKey;
  delete next.credential_id;
  delete next.account_id;
  delete next.credentialId;
  delete next.accountId;
  writeIdentity(next);
  return { savePath, token: key };
}

function readHiddenLine(prompt) {
  function sanitizeChunk(chunk) {
    // Strip bracketed-paste markers (\x1b[200~...\x1b[201~), keep printable chars only.
    return String(chunk || '')
      .replace(/\u001b\[200~/g, '')
      .replace(/\u001b\[201~/g, '')
      .replace(/[\u0000-\u001f\u007f]/g, '');
  }

  const stdin = process.stdin;
  const stdout = process.stderr;
  if (!stdin.isTTY) {
    return new Promise((r) => {
      const rl = createInterface({ input: stdin, output: stdout });
      rl.question(prompt, (a) => {
        rl.close();
        r(a.trim());
      });
    });
  }
  stdout.write(prompt);
  return new Promise((resolveLine) => {
    stdin.setRawMode(true);
    stdin.resume();
    stdin.setEncoding('utf8');
    let s = '';
    const onData = (key) => {
      const k = String(key);
      if (k === '\u0003') {
        stdin.setRawMode(false);
        stdin.removeListener('data', onData);
        stdin.pause();
        process.exit(1);
      }
      if (k === '\r' || k === '\n') {
        stdin.setRawMode(false);
        stdin.removeListener('data', onData);
        stdin.pause();
        stdout.write('\n');
        resolveLine(s);
        return;
      }
      if (k === '\u007f' || k === '\b') {
        s = s.slice(0, -1);
        return;
      }
      s += sanitizeChunk(k);
    };
    stdin.on('data', onData);
  });
}

/** 交互式录入 API Key → credentials（TTY 下隐藏输入，支持粘贴） */
export async function promptInteractiveCredentialsFile() {
  if (!process.stdin.isTTY || !process.stderr.isTTY) {
    throw new CredentialsMissingError(
      'TTY required / 需要交互式终端',
    );
  }

  console.error('\n── Kling AI configure / 可灵凭证配置 ─────────────');
  console.error(`Profile / 配置名: ${getActiveProfile()}`);
  console.error(`File / 文件: ${getCredentialsFilePath()}`);
  console.error('────────────────────────────────────────────────\n');

  const apiKey = await readHiddenLine('API Key / API 密钥（隐藏输入，可粘贴）: ');
  if (!apiKey) throw new Error('API Key required / 需要 API Key');
  const savePath = writeCredentialsProfile(getActiveProfile(), apiKey);
  console.error(`\n✓ Saved / 已保存（密钥未在日志中输出）: ${savePath}\n`);
  return apiKey;
}
