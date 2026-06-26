#!/usr/bin/env node
/**
 * 从本机向当前 LOVECLAW_API_BASE 发 POST /api/photo（1×1 PNG），用于排查「OSS 无对象 / 上传失败」。
 * 依赖：~/.openclaw/workspace/.env 或环境中已有 LOVECLAW_API_TOKEN（或 API_TOKEN）。
 *
 *   node scripts/photo-oss-probe.js [phoneOrUserId]
 *
 * 成功会打印返回的 OSS URL；失败打印云函数错误信息（含 OSS region/bucket 提示若已部署新版 FC）。
 */
'use strict';

require('./load-workspace-env').applyFromWorkspaceDotenv();
const cloudData = require('./cloud-data');

// 最小合法 PNG（Base64）
const PNG1 =
  'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';

async function main() {
  const id = process.argv[2] || '13900000000';
  try {
    const url = await cloudData.uploadPhoto(id, PNG1);
    console.log('photo-oss-probe OK');
    console.log('url:', url);
  } catch (e) {
    console.error('photo-oss-probe FAIL:', e.message || e);
    process.exit(1);
  }
}

main();
