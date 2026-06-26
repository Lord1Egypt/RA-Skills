/**
 * KreadoAI — 鉴权层
 *
 * 凭证优先级：
 *   1. 环境变量 KREADO_API_TOKEN
 *   2. ~/.config/kreado/.credentials 文件中存储的 apiToken
 *
 * KreadoAI 使用简单的 apiToken 鉴权（HTTP Header: apiToken）
 */
import { readFileSync, writeFileSync, mkdirSync, chmodSync } from 'node:fs';
import { dirname, resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createInterface } from 'node:readline';

const __dir = dirname(fileURLToPath(import.meta.url));

const CREDENTIALS_FILENAME = '.credentials';
const ENV_FILENAME = 'kreado.env';
const STORAGE_ROOT_ENV = 'KREADO_STORAGE_ROOT';

export function getKreadoConfigDir() {
  const explicitRoot = (process.env[STORAGE_ROOT_ENV] || '').trim();
  if (explicitRoot) return resolve(explicitRoot);
  const home = process.env.HOME || process.env.USERPROFILE;
  if (home) return join(home, '.config', 'kreado');
  return resolve(__dir, '..', '..', '..');
}

export function getCredentialsFilePath() {
  return join(getKreadoConfigDir(), CREDENTIALS_FILENAME);
}

function getEnvFilePath() {
  return join(getKreadoConfigDir(), ENV_FILENAME);
}

(function loadEnvFile() {
  try {
    const content = readFileSync(getEnvFilePath(), 'utf-8');
    for (const line of content.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const eqIdx = trimmed.indexOf('=');
      if (eqIdx <= 0) continue;
      const key = trimmed.slice(0, eqIdx).trim();
      let val = trimmed.slice(eqIdx + 1).trim();
      if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
        val = val.slice(1, -1);
      }
      if (!(key in process.env)) {
        process.env[key] = val;
      }
    }
  } catch {}
})();

export class CredentialsMissingError extends Error {
  constructor(msg = '未配置 API Token') {
    super(msg);
    this.name = 'CredentialsMissingError';
  }
}

function readStoredToken() {
  try {
    const raw = readFileSync(getCredentialsFilePath(), 'utf-8');
    const trimmed = raw.trim();
    if (trimmed.startsWith('{')) {
      const obj = JSON.parse(trimmed);
      return (obj.apiToken || obj.api_token || '').trim();
    }
    for (const line of trimmed.split('\n')) {
      const l = line.trim();
      if (!l || l.startsWith('#')) continue;
      const eqIdx = l.indexOf('=');
      if (eqIdx > 0) {
        const key = l.slice(0, eqIdx).trim();
        if (key === 'apiToken' || key === 'api_token') {
          let val = l.slice(eqIdx + 1).trim();
          if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
            val = val.slice(1, -1);
          }
          return val;
        }
      }
    }
    if (trimmed && !trimmed.includes('\n') && !trimmed.includes('=')) {
      return trimmed;
    }
    return '';
  } catch {
    return '';
  }
}

export function hasStoredToken() {
  return Boolean(readStoredToken());
}

export function getApiToken() {
  const envToken = (process.env.KREADO_API_TOKEN || '').trim();
  if (envToken) {
    console.error('鉴权来源：KREADO_API_TOKEN（环境变量）');
    return envToken;
  }
  const stored = readStoredToken();
  if (stored) {
    console.error('鉴权来源：凭证文件');
    return stored;
  }
  throw new CredentialsMissingError(
    '请设置 KREADO_API_TOKEN 或执行：kreado account --configure',
  );
}

export function writeToken(token) {
  const path = getCredentialsFilePath();
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `apiToken=${token}\n`);
  try {
    if (process.platform !== 'win32') chmodSync(path, 0o600);
  } catch {}
  return path;
}

export function maskToken(token) {
  const s = String(token || '');
  if (!s) return '';
  if (s.length <= 8) return '***';
  return `${s.slice(0, 4)}***${s.slice(-4)}`;
}

export async function promptInteractiveToken() {
  if (!process.stdin.isTTY || !process.stderr.isTTY) {
    throw new CredentialsMissingError('需要交互式终端');
  }
  console.error('\n── KreadoAI 凭证配置 ─────────────────────────────');
  console.error(`文件：${getCredentialsFilePath()}`);
  console.error('获取 Token：https://www.kreadoai.com/ -> 账号 -> API 设置');
  console.error('────────────────────────────────────────────────\n');

  const rl = createInterface({ input: process.stdin, output: process.stderr });
  const token = await new Promise((r) => {
    rl.question('API Token：', (a) => r(a.trim()));
  });
  rl.close();
  if (!token) throw new Error('需要 API Token');
  const savePath = writeToken(token);
  console.error(`\n✓ 已保存：${savePath}\n`);
  return token;
}

let _skillVersion = '1.1.0';
export function setSkillVersion(v) { _skillVersion = String(v || '1.1.0'); }
export function getSkillVersion() { return _skillVersion; }
