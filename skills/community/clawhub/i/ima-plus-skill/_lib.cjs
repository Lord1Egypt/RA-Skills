'use strict';
// 共享工具（V1.0.11 体积优化）：parseArgs / log / call / resolveKbId
// 各脚本 require 本模块，不再各自重复定义（原先在 26 个脚本里各抄一份，约 24KB）。
const path = require('node:path');
const { imaApi } = require(path.join(__dirname, 'ima_api.cjs'));
const { resolveKbId: __resKb, resolvePathStr: __resPath } = require(path.join(__dirname, 'resolve_path.cjs'));

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const tok = argv[i];
    if (!tok.startsWith('--')) continue;
    const key = tok.replace(/^--/, '');
    const next = argv[i + 1];
    if (next && !next.startsWith('--')) {
      args[key] = next;
      i++;
    } else {
      args[key] = true;
    }
  }
  return args;
}

function log(step, msg) {
  console.log(`${step} ${msg}`);
}

async function call(apiPath, body) {
  const raw = await imaApi(apiPath, body);
  let json;
  try {
    json = JSON.parse(raw);
  } catch {
    throw new Error(`接口 ${apiPath} 返回非 JSON：${raw}`);
  }
  if (json.code !== 0) {
    throw new Error(`接口 ${apiPath} 失败 (code=${json.code}): ${json.msg || ''}`);
  }
  return json;
}

async function resolveKbId(args, extra) {
  // 统一解析：--path "知识库名/文件夹..." 优先；兼容 --kb / --kb-name
  if (args.path) {
    const r = await __resPath(args.path, extra || {});
    if (extra && extra.needFolder) return r;
    return r.kb_id;
  }
  const r = await __resKb(args);
  return (r && typeof r === 'object') ? (extra && extra.needFolder ? r : r.kb_id) : r;
}

module.exports = { parseArgs, log, call, resolveKbId };
