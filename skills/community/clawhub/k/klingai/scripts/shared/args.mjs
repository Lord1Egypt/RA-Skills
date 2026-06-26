/**
 * Kling AI CLI helpers (zero external deps)
 * Argument parsing, auth, media file reading
 */
import { readFile } from 'node:fs/promises';
import { resolve, relative, sep } from 'node:path';
import { platform } from 'node:process';
import {
  getBearerToken,
  CredentialsMissingError,
  setSkillVersion,
} from './auth.mjs';
import { runDeviceBindFlow } from './client.mjs';

/** 是否允许读取/写入 cwd 与 KLING_MEDIA_ROOTS 以外的本地路径（默认关闭） */
function allowAbsolutePaths() {
  const v = (process.env.KLING_ALLOW_ABSOLUTE_PATHS || '').trim().toLowerCase();
  return v === '1' || v === 'true' || v === 'yes';
}

/** 额外允许的根目录（逗号分隔），用于下载目录、WSL 跨盘路径等 */
function extraMediaRoots() {
  const raw = (process.env.KLING_MEDIA_ROOTS || '').trim();
  if (!raw) return [];
  return raw.split(',').map((s) => s.trim()).filter(Boolean).map((p) => resolve(p));
}

function allAllowedRoots() {
  const roots = [resolve(process.cwd()), ...extraMediaRoots()];
  return roots;
}

/** Windows：仅在同盘内做 relative 校验 */
function sameDriveRoot(a, b) {
  if (platform !== 'win32') return true;
  const ra = resolve(a);
  const rb = resolve(b);
  const da = ra.match(/^([A-Za-z]:)/);
  const db = rb.match(/^([A-Za-z]:)/);
  if (!da || !db) return true;
  return da[1].toLowerCase() === db[1].toLowerCase();
}

/**
 * 判断绝对路径是否落在任一允许根下（用于本地文件读、输出目录写）
 * @param {string} absPath 已 resolve 的绝对路径
 */
export function isAllowedLocalPath(absPath) {
  if (allowAbsolutePaths()) return true;
  const normalized = resolve(absPath);
  for (const root of allAllowedRoots()) {
    if (!sameDriveRoot(root, normalized)) continue;
    const rel = relative(root, normalized);
    if (rel === '') return true;
    if (!rel.startsWith('..') && !rel.includes(`${sep}..`)) return true;
  }
  return false;
}

/**
 * 校验并返回用于读文件的绝对路径（URL 不适用）
 * @param {string} userPath 用户传入的本地路径
 * @returns {string}
 */
export function resolveAllowedReadPath(userPath) {
  const normalized = resolve(userPath.trim());
  if (!isAllowedLocalPath(normalized)) {
    const roots = allAllowedRoots().join(', ');
    throw new Error(
      `Local path outside allowed roots / 本地路径不在允许范围内: ${normalized}\n`
      + `Allowed / 允许: cwd + KLING_MEDIA_ROOTS, or set KLING_ALLOW_ABSOLUTE_PATHS=1\n`
      + `Roots / 当前根: ${roots}\n`
      + `Example / 示例: export KLING_MEDIA_ROOTS="/mnt/c/Users/you/Downloads,/tmp/claw-downloads"`,
    );
  }
  return normalized;
}

/**
 * 校验输出目录（相对路径相对于 cwd 解析）
 * @param {string} userPath 如 ./output 或绝对路径
 * @returns {string} 绝对路径
 */
export function resolveAllowedOutputDir(userPath) {
  const normalized = resolve(userPath.trim());
  if (!isAllowedLocalPath(normalized)) {
    const roots = allAllowedRoots().join(', ');
    throw new Error(
      `Output dir outside allowed roots / 输出目录不在允许范围内: ${normalized}\n`
      + `Allowed / 允许: under cwd, KLING_MEDIA_ROOTS, or KLING_ALLOW_ABSOLUTE_PATHS=1\n`
      + `Roots / 当前根: ${roots}`,
    );
  }
  return normalized;
}

/** 消费 --skill-version */
function consumeSkillVersionArgv(argv) {
  for (let i = 2; i < argv.length - 1; i++) {
    if (argv[i] === '--skill-version') {
      setSkillVersion(argv[i + 1]);
      argv.splice(i, 2);
      return;
    }
  }
}

/**
 * 解析命令行参数
 * @param {string[]} argv  process.argv（会原地消费 --skill-version）
 * @param {string[]} [booleanFlags]  额外的布尔标志名（不需要跟值的 --flag）
 * @returns {object} 参数键值对
 */
export function parseArgs(argv, booleanFlags = []) {
  consumeSkillVersionArgv(argv);
  const boolSet = new Set(['no-wait', 'download', 'wait', 'help', ...booleanFlags]);
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const key = argv[i];
    if (!key.startsWith('--')) continue;
    const name = key.slice(2);
    if (name === 'no-wait') { args.wait = false; continue; }
    if (boolSet.has(name)) { args[name] = true; continue; }
    const val = argv[i + 1];
    if (val !== undefined && !val.startsWith('--')) {
      args[name] = val; i++;
    } else {
      args[name] = true;
    }
  }
  return args;
}

/**
 * 获取 Bearer：优先进程内 KLING_TOKEN；否则 credentials 中 AK/SK → JWT。
 * 若皆无（首次或仅有空凭证），自动执行设备绑定（bind）后再取 token。
 */
export async function getTokenOrExit() {
  try {
    return getBearerToken();
  } catch (e) {
    const missing = e instanceof CredentialsMissingError || e?.name === 'CredentialsMissingError';
    if (!missing) {
      throw new Error(`Auth error / 鉴权错误: ${e?.message || e}`);
    }
    try {
      console.error('\n── No credentials / 无可用凭证，启动设备绑定 bind ────\n');
      await runDeviceBindFlow({});
      return getBearerToken();
    } catch (err) {
      const lines = [
        `Bind failed / 绑定失败: ${err?.message || err}`,
      ];
      if (err?.bindAuthorizeUrl) {
        lines.push(`Bind URL / 手动绑定链接: ${err.bindAuthorizeUrl}`);
      }
      lines.push('Fallback / 备选:');
      lines.push('  node skills/klingai/scripts/kling.mjs account --bind-url');
      lines.push('  set KLING_ACCESS_KEY_ID + KLING_SECRET_ACCESS_KEY, then');
      lines.push('  node skills/klingai/scripts/kling.mjs account --import-env');
      lines.push('  or pass args: --import-credentials --access_key_id <AK> --secret_access_key <SK>');
      lines.push('  or set KLING_TOKEN for this session / 或设置 KLING_TOKEN');
      throw new Error(lines.join('\n'));
    }
  }
}

/**
 * 读取媒体文件：URL 直接返回，本地文件读为 base64（路径受 KLING_MEDIA_ROOTS / KLING_ALLOW_ABSOLUTE_PATHS 约束）
 * @param {string} pathOrUrl  文件路径或 URL
 * @returns {Promise<string>} URL 或 base64 字符串
 */
export async function readMediaAsValue(pathOrUrl) {
  if (!pathOrUrl) return undefined;
  const s = pathOrUrl.trim();
  try {
    const u = new URL(s);
    if (u.protocol === 'http:' || u.protocol === 'https:') return s;
  } catch {
    // Not a URL: treat as local path below.
  }
  const abs = resolveAllowedReadPath(s);
  const buf = await readFile(abs);
  return buf.toString('base64');
}

/**
 * Omni-Video 参考视频字段 `video_list[].video_url`：仅接受公网 `http://` 或 `https://` 链接，不接受本地路径或 Base64。
 * @param {string} pathOrUrl
 * @returns {string|undefined}
 */
export function readOmniVideoRefUrl(pathOrUrl) {
  if (!pathOrUrl) return undefined;
  const s = pathOrUrl.trim();
  try {
    const u = new URL(s);
    if (u.protocol === 'http:' || u.protocol === 'https:') return s;
  } catch {
    // Fallthrough to unified error below.
  }
  throw new Error(
    'Omni --video must be a public http(s) URL / Omni --video 须为公网 http(s) 链接（不接受本地路径或 Base64）。\n'
    + 'Upload the file and pass the URL / 请先上传视频再传入 URL。',
  );
}
