#!/usr/bin/env node
/**
 * Kling AI — 账号：资源包查询、设备绑定、交互式配置 credentials
 */
import {
  klingGet,
  runDeviceBindFlow,
  KLING_CONSOLE_URLS,
} from './shared/client.mjs';
import {
  getActiveProfile,
  getCredentialsFilePath,
  getIdentityFilePath,
  hasStoredAccessKeys,
  promptInteractiveCredentialsFile,
  writeCredentialsProfile,
} from './shared/auth.mjs';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';
import { parseArgs, getTokenOrExit } from './shared/args.mjs';

const API_COSTS = '/account/costs';
const MS_PER_DAY = 24 * 60 * 60 * 1000;

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

function printConsoleUrls() {
  for (const [region, url] of Object.entries(KLING_CONSOLE_URLS || {})) {
    const label = region === 'cn' ? 'China / 国内' : (region === 'global' ? 'Global / 国际' : region);
    console.error(`${label}: ${url}`);
  }
}

function printHelp() {
  console.log(`Kling AI account — quota, device bind, configure credentials

Usage:
  node kling.mjs account [options]
  node kling.mjs account --costs   (default)
  node kling.mjs account --bind-url
  node kling.mjs account --bind    (alias of --bind-url, kept for compatibility)
  node kling.mjs account --configure
  node kling.mjs account --import-env
  node kling.mjs account --import-credentials --access_key_id <ak> --secret_access_key <sk>

--costs (default)
  GET ${API_COSTS}  (Bearer from credentials JWT or KLING_TOKEN)
  --days, --start_time, --end_time, --resource_pack_name

--bind-url
  init → verify → print URL (manual open) → poll
  --bind is equivalent to --bind-url (compatibility alias)
  --force   Re-bind even if credentials already exist
  writes ~/.config/kling/.credentials after exchange succeeds

--import-env
  Read KLING_ACCESS_KEY_ID + KLING_SECRET_ACCESS_KEY from env and save (no prompt)

--import-credentials
  Write AK/SK via args in one step, no prompts

--configure
  Interactive prompts → credentials file (hidden SK on TTY, paste supported)

Env:
  KLING_STORAGE_ROOT         Optional storage root for credentials/identity/env files
  KLING_TOKEN                Session Bearer (not loaded from kling.env; export or agent env)
  KLING_API_BASE             Optional API origin
  KLING_ACCESS_KEY_ID        With KLING_SECRET_ACCESS_KEY: used by import-env (not echoed)
  KLING_SECRET_ACCESS_KEY    (same)`);
}

function saveCredentialsQuietly(ak, sk, source = 'input') {
  const savePath = writeCredentialsProfile(getActiveProfile(), String(ak || '').trim(), String(sk || '').trim());
  console.error(`✓ Credentials saved / 凭证已保存（来源: ${source}；密钥未在日志中输出）`);
  console.error(`  Path / 路径: ${savePath}\n`);
  return {
    savePath,
    accessKeyMasked: maskAccessKey(ak),
    secretKeyMasked: maskSecret(sk),
  };
}

function getEnvCredentials() {
  const ak = (process.env.KLING_ACCESS_KEY_ID || '').trim();
  const sk = (process.env.KLING_SECRET_ACCESS_KEY || '').trim();
  return { ak, sk };
}

export function importCredentialsFromEnv() {
  const { ak, sk } = getEnvCredentials();
  if (!ak || !sk) {
    throw new Error(
      'Set both KLING_ACCESS_KEY_ID and KLING_SECRET_ACCESS_KEY / '
      + '请同时设置 KLING_ACCESS_KEY_ID 与 KLING_SECRET_ACCESS_KEY',
    );
  }
  return saveCredentialsQuietly(ak, sk, 'env');
}

export function importCredentialsFromArgs(accessKey, secretKey) {
  const ak = String(accessKey || '').trim();
  const sk = String(secretKey || '').trim();
  if (!ak || !sk) {
    throw new Error(
      'import-credentials requires --access_key_id and --secret_access_key / '
      + 'import-credentials 需要 --access_key_id 与 --secret_access_key',
    );
  }
  return saveCredentialsQuietly(ak, sk, 'args');
}

function parseMs(name, raw) {
  const n = parseInt(String(raw).trim(), 10);
  if (!Number.isFinite(n)) {
    console.error(`Error / 错误: ${name} must be a valid integer (ms) / 须为有效整数（毫秒）`);
    process.exit(1);
  }
  return n;
}

function buildCostsQueryPath(args) {
  let endMs;
  let startMs;

  if (args.end_time != null) {
    endMs = parseMs('--end_time', args.end_time);
  } else {
    endMs = Date.now();
  }

  if (args.start_time != null) {
    startMs = parseMs('--start_time', args.start_time);
  } else {
    const days = Math.max(1, parseInt(String(args.days ?? '30'), 10) || 30);
    startMs = endMs - days * MS_PER_DAY;
  }

  if (startMs >= endMs) {
    console.error('Error / 错误: start_time must be < end_time / start_time 须小于 end_time');
    process.exit(1);
  }

  const params = new URLSearchParams();
  params.set('start_time', String(startMs));
  params.set('end_time', String(endMs));
  if (args.resource_pack_name) {
    params.set('resource_pack_name', String(args.resource_pack_name).trim());
  }

  return `${API_COSTS}?${params.toString()}`;
}

function printAccountStateNoAccount(detail = '') {
  console.error('Account State / 账号状态: NO_ACCOUNT / 无可用账号凭证');
  if (detail) {
    console.error(`  Detail / 详情: ${detail}`);
  }
}

function isPermissionOrServerIssue(errorMessage = '') {
  const msg = String(errorMessage || '').toLowerCase();
  return (
    msg.includes('http 401')
    || msg.includes('http 403')
    || msg.includes('code=1000')
    || msg.includes('code=1002')
    || msg.includes('permission')
    || msg.includes('forbidden')
    || msg.includes('unauthorized')
    || msg.includes('api service error')
    || msg.includes('http 500')
    || msg.includes('http 502')
    || msg.includes('http 503')
    || msg.includes('http 504')
    || msg.includes('server error')
  );
}

async function runBindUrlAction(args, options = {}) {
  const viaAliasBind = options.viaAliasBind === true;
  if (!args.force && hasStoredAccessKeys()) {
    console.error('Credentials already present / 已存在凭证（使用 --force 重新绑定）');
    console.error(`Credentials file / 凭证文件: ${getCredentialsFilePath()}`);
    process.exit(0);
  }
  if (viaAliasBind) {
    console.error('Info / 提示: --bind is an alias of --bind-url / --bind 与 --bind-url 等价');
  }

  try {
    const result = await runDeviceBindFlow();
    console.error('\n✓ Bind succeeded / 绑定成功');
    console.error(`  Saved / 已写入: ${result.savePath || getCredentialsFilePath()}`);
  } catch (e) {
    console.error(`\nBind failed / 绑定失败: ${e?.message || e}\n`);
    console.error('Hint / 提示:');
    console.error('  1) Check network/DNS/proxy / 检查网络、DNS、代理');
    console.error('  2) Check configured API base in ~/.config/kling/kling.env / 检查 ~/.config/kling/kling.env 中的 API 基址配置');
    console.error('  3) Re-probe business API base: remove KLING_API_BASE then run account --costs / 重新探测业务 API 基址：删除 KLING_API_BASE 后执行 account --costs');
    console.error('Fallback / 备选:');
    console.error('  1) Create keys Manually / 手动创建密钥:');
    printConsoleUrls();
    console.error('  2) Set env then: node skills/klingai/scripts/kling.mjs account --import-env');
    console.error('  3) or Pass args: node skills/klingai/scripts/kling.mjs account --import-credentials --access_key_id <AK> --secret_access_key <SK>\n');
    process.exit(1);
  }
}

export async function main() {
  const args = parseArgs(process.argv);
  if (args.help) {
    printHelp();
    return;
  }
  if (args.action != null) {
    console.error('Error / 错误: --action has been removed. Use one flag: --costs | --bind-url (or alias --bind) | --import-env | --import-credentials | --configure');
    process.exit(1);
  }

  const modes = ['costs', 'bind', 'bind-url', 'configure', 'import-env', 'import-credentials'];
  const selected = modes.filter((m) => args[m]);
  if (selected.length > 1) {
    console.error(`Error / 错误: account mode flags are mutually exclusive / account 模式参数互斥: ${selected.map((s) => `--${s}`).join(', ')}`);
    process.exit(1);
  }
  const action = selected[0] || 'costs';

  if (action === 'bind') {
    await runBindUrlAction(args, { viaAliasBind: true });
    return;
  }

  if (action === 'bind-url') {
    await runBindUrlAction(args);
    return;
  }

  if (action === 'import-env') {
    try {
      importCredentialsFromEnv();
    } catch (e) {
      console.error(`Error / 错误: ${e?.message || e}`);
      process.exit(1);
    }
    return;
  }

  if (action === 'import-credentials') {
    try {
      importCredentialsFromArgs(args.access_key_id, args.secret_access_key);
    } catch (e) {
      console.error(`Error / 错误: ${e?.message || e}`);
      process.exit(1);
    }
    return;
  }

  if (action === 'configure') {
    try {
      console.error('Get keys / 获取密钥:');
      printConsoleUrls();
      await promptInteractiveCredentialsFile();
    } catch (e) {
      console.error(`Error / 错误: ${e?.message || e}`);
      process.exit(1);
    }
    return;
  }

  let token;
  try {
    token = await getTokenOrExit();
  } catch (e) {
    const msg = e?.message || String(e);
    printAccountStateNoAccount(msg);
    console.error(`Error / 错误: ${msg}`);
    console.error('Get keys / 获取密钥:');
    printConsoleUrls();
    process.exit(1);
  }
  const pathWithQuery = buildCostsQueryPath(args);

  try {
    const data = await klingGet(pathWithQuery, token, { contentType: 'application/json' });
    const infos = Array.isArray(data?.resource_pack_subscribe_infos) ? data.resource_pack_subscribe_infos : [];
    console.error(`Account State / 账号状态: ACCOUNT_OK / 账号正常（资源包 ${infos.length}）`);
    console.log('Account / 账户资源 (API data):');
    console.log(JSON.stringify(data, null, 2));
    return;
  } catch (e) {
    const msg = e?.message || String(e);
    if (isPermissionOrServerIssue(msg)) {
      console.error('Account State / 账号状态: BOUND_BUT_PERMISSION_OR_SERVER_ERROR / 已绑定但权限或服务异常');
    }
    console.error(`Error / 错误: ${msg}`);
    process.exit(1);
  }
}

const __filename = fileURLToPath(import.meta.url);
if (process.argv[1] && resolve(__filename) === resolve(process.argv[1])) {
  main().catch((e) => {
    console.error(`Error / 错误: ${e?.message || e}`);
    process.exit(1);
  });
}
