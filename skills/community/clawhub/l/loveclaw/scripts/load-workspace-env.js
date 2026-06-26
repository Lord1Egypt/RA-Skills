'use strict';

/**
 * 仅将 OpenClaw 工作区 ~/.openclaw/workspace/.env 中 **允许名单** 内的键合并进 process.env，
 * 避免把整个工作区 .env 里的无关秘密暴露给本 skill 进程（ClawHub reads_workspace_dotenv 关切）。
 *
 * 允许：
 * - LOVECLAW_*、OPENCLAW_BIN
 * - API_TOKEN：兼容仅在工作区 .env 写 API_TOKEN 的旧部署（与部分 FC 示例环境变量同名；等同 LOVECLAW_API_TOKEN）
 * - HTTP(S)_PROXY 等：fetch 上传大图时偶发需要
 *
 * 已存在于 process.env 的键不覆盖（与历史行为一致）。
 */

const path = require('path');
const fs = require('fs');

const EXTRA_ALLOW = new Set([
  'API_TOKEN',
  'HTTP_PROXY',
  'HTTPS_PROXY',
  'NO_PROXY',
  'ALL_PROXY',
  'NODE_EXTRA_CA_CERTS',
]);

function allowlistedKey(key) {
  return (
    key === 'OPENCLAW_BIN' ||
    key.startsWith('LOVECLAW_') ||
    EXTRA_ALLOW.has(key)
  );
}

function applyFromWorkspaceDotenv() {
  const envPath = path.join(process.env.HOME || '/root', '.openclaw', 'workspace', '.env');
  if (!fs.existsSync(envPath)) return;

  fs.readFileSync(envPath, 'utf-8').split('\n').forEach((line) => {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) return;
    const eqIdx = trimmed.indexOf('=');
    if (eqIdx < 0) return;
    const key = trimmed.slice(0, eqIdx).trim();
    let val = trimmed.slice(eqIdx + 1).trim();
    if (
      (val.startsWith('"') && val.endsWith('"')) ||
      (val.startsWith("'") && val.endsWith("'"))
    ) {
      val = val.slice(1, -1);
    }
    if (!key || !allowlistedKey(key)) return;
    if (!process.env[key]) process.env[key] = val;
  });
}

module.exports = { applyFromWorkspaceDotenv, allowlistedKey };
