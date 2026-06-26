import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { CLI_NAME, PACKAGE_NAME } from '../constants.js';
import { ensureDir, formatPath, pathExists } from '../utils.js';

export const CONFIG_DIR = path.join(os.homedir(), '.config', 'insentek');
export const CREDENTIALS_FILE = path.join(CONFIG_DIR, 'credentials.json');
export const CREDENTIALS_VERSION = 2;
export const API_BASE_URL = process.env.INSENTEK_API_BASE || 'https://openapi.ecois.info';
export const SCRYPT_SALT = 'insentek-skill-salt-v1';

export const NOT_CONNECTED_MESSAGE = `这台电脑还没有连接 Insentek API，需要先完成一次本地配置，通常 1 分钟就好。

请在终端运行：

npx @insentek/openapi-skill login

按提示输入 appid 和 secret 即可（加密保存在本机，无需发到这个对话）。配置完成后回来继续提问，我接着帮你处理。`;

const KEY_MATERIAL_SUFFIX = ':insentek-openapi-skill';

function deriveKeyMaterial() {
  const { username } = os.userInfo();
  return `${os.hostname()}:${username}${KEY_MATERIAL_SUFFIX}`;
}

function deriveKey() {
  return crypto.scryptSync(deriveKeyMaterial(), SCRYPT_SALT, 32);
}

function encryptField(plaintext) {
  const key = deriveKey();
  const iv = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const encrypted = Buffer.concat([cipher.update(plaintext, 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();
  return Buffer.concat([iv, tag, encrypted]).toString('base64');
}

function decryptField(payload) {
  const key = deriveKey();
  const data = Buffer.from(payload, 'base64');
  const iv = data.subarray(0, 12);
  const tag = data.subarray(12, 28);
  const ciphertext = data.subarray(28);
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(tag);
  return Buffer.concat([decipher.update(ciphertext), decipher.final()]).toString('utf8');
}

function maskSecret(secret) {
  if (!secret || secret.length <= 8) {
    return '****';
  }
  return `${secret.slice(0, 4)}****${secret.slice(-4)}`;
}

function maskToken(token) {
  if (!token) {
    return '(not cached)';
  }
  if (token.length <= 12) {
    return '****';
  }
  return `${token.slice(0, 8)}****${token.slice(-4)}`;
}

async function setFilePermissions(filePath) {
  if (process.platform === 'win32') {
    return;
  }
  await fs.chmod(filePath, 0o600);
}

function normalizeLoadedCredentials(raw) {
  if (!raw || typeof raw !== 'object') {
    return null;
  }

  if (raw.version >= CREDENTIALS_VERSION && raw.encrypted) {
    try {
      return {
        appid: raw.appid,
        secret: decryptField(raw.secret_enc),
        token: raw.token_enc ? decryptField(raw.token_enc) : null,
        token_updated_at: raw.token_updated_at ?? null,
        created_at: raw.created_at ?? null,
        version: raw.version,
        encrypted: true,
      };
    } catch {
      return null;
    }
  }

  if (raw.appid && raw.secret) {
    return {
      appid: raw.appid,
      secret: raw.secret,
      token: raw.token ?? null,
      token_updated_at: raw.token_updated_at ?? null,
      created_at: raw.created_at ?? null,
      version: raw.version ?? 1,
      encrypted: false,
    };
  }

  return null;
}

export async function loadCredentials() {
  if (!(await pathExists(CREDENTIALS_FILE))) {
    return null;
  }

  try {
    const raw = JSON.parse(await fs.readFile(CREDENTIALS_FILE, 'utf8'));
    return normalizeLoadedCredentials(raw);
  } catch {
    return null;
  }
}

export async function hasCredentials() {
  const creds = await loadCredentials();
  return Boolean(creds?.appid && creds?.secret);
}

export async function saveCredentials({ appid, secret, token = null }) {
  await ensureDir(CONFIG_DIR);

  const now = new Date().toISOString();
  const payload = {
    version: CREDENTIALS_VERSION,
    encrypted: true,
    appid,
    secret_enc: encryptField(secret),
    token_enc: token ? encryptField(token) : null,
    token_updated_at: token ? now : null,
    created_at: now,
  };

  await fs.writeFile(CREDENTIALS_FILE, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
  await setFilePermissions(CREDENTIALS_FILE);
  return payload;
}

export async function updateToken(token) {
  const creds = await loadCredentials();
  if (!creds) {
    return null;
  }

  return saveCredentials({
    appid: creds.appid,
    secret: creds.secret,
    token,
  });
}

export async function clearCredentials() {
  if (!(await pathExists(CREDENTIALS_FILE))) {
    return false;
  }
  await fs.unlink(CREDENTIALS_FILE);
  return true;
}

export async function getCredentialStatus() {
  const creds = await loadCredentials();
  if (!creds) {
    return {
      connected: false,
      config_path: CREDENTIALS_FILE,
      message: NOT_CONNECTED_MESSAGE,
    };
  }

  return {
    connected: true,
    appid: creds.appid,
    secret: maskSecret(creds.secret),
    token: maskToken(creds.token),
    token_updated_at: creds.token_updated_at,
    created_at: creds.created_at,
    encrypted: creds.encrypted ?? false,
    config_path: CREDENTIALS_FILE,
  };
}

export async function fetchToken(appid, secret) {
  const url = new URL('/v3/token', API_BASE_URL);
  url.searchParams.set('appid', appid);
  url.searchParams.set('secret', secret);

  const response = await fetch(url, { method: 'GET' });
  const body = await response.json().catch(() => ({}));

  if (!response.ok) {
    const message = body?.message || body?.error || `HTTP ${response.status}`;
    throw new Error(`Authentication failed: ${message}`);
  }

  if (!body.token) {
    throw new Error('Authentication failed: token missing in response');
  }

  return body;
}

export async function loginWithCredentials({ appid, secret }) {
  const trimmedAppId = appid?.trim();
  const trimmedSecret = secret?.trim();

  if (!trimmedAppId || !trimmedSecret) {
    throw new Error('App ID and App Secret are required.');
  }

  const tokenResponse = await fetchToken(trimmedAppId, trimmedSecret);
  await saveCredentials({
    appid: trimmedAppId,
    secret: trimmedSecret,
    token: tokenResponse.token,
  });

  return {
    appid: trimmedAppId,
    secret: maskSecret(trimmedSecret),
    token: maskToken(tokenResponse.token),
    expires: tokenResponse.expires ?? null,
    config_path: CREDENTIALS_FILE,
  };
}

export function getLoginHelpText() {
  return [
    'Configure Insentek API credentials locally (never paste secrets into chat).',
    '',
    `  npx ${PACKAGE_NAME} login`,
    `  npx ${PACKAGE_NAME} logout`,
    `  npx ${CLI_NAME} auth status`,
    '',
    `Credentials are encrypted and stored at ${formatPath(CREDENTIALS_FILE)}`,
  ].join('\n');
}
