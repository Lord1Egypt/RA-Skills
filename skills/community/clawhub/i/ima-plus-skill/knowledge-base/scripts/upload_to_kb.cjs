#!/usr/bin/env node
'use strict';

/**
 * 一键上传文件到 IMA 知识库（快速通道）
 *
 * 把原本需要手动跑 5 步、还要解析 JSON / 拼接临时文件的流程，
 * 封装成一条命令。内部依次执行：
 *   preflight-check → 重名检查 → create_media → cos-upload → add_knowledge
 *
 * 相比手工流程的优化点：
 *   1. 一条命令搞定，无需中间解析 JSON / 临时文件
 *   2. 未指定知识库时，自动挑「唯一可添加的知识库」；多个时打印列表提示
 *   3. 支持 --kb-name 按名称自动匹配知识库
 *   4. 遇到重名默认「保留两者」（自动追加 _YYYYMMDDHHmmss），符合 GATE 3
 *      可用 --cancel-if-dup 在重名时直接取消
 *   5. 全程进度输出，失败时给出可读错误（绝不吞错）
 *
 * Usage:
 *   node upload_to_kb.cjs --file /path/to/file.pdf
 *   node upload_to_kb.cjs --file a.pdf --path "我的知识库"
 *   node upload_to_kb.cjs --file a.pdf --kb-name "我的知识库"
 *   node upload_to_kb.cjs --file a.pdf --folder <folder_id>
 *   node upload_to_kb.cjs --file a.pdf --cancel-if-dup
 */

const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima_api.cjs'));
const { resolveKbId: __resKb, resolvePathStr: __resPath, withPathRetry: __withRetry } = require(path.join(__dirname, '..', '..', 'resolve_path.cjs'));
const { call, log, parseArgs, resolveKbId } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

const PREFLIGHT = path.join(__dirname, 'preflight-check.cjs');
const COS_UPLOAD = path.join(__dirname, 'cos-upload.cjs');

// ─── 参数解析 ───────────────────────────────────────────────────────────────

function runPreflight(filePath) {
  // 用 process.execPath（当前 node 绝对路径）而非裸 'node'，
  // 避免 Windows 上 node 不在 PATH 时 spawn 失败，跨平台更稳。
  const r = spawnSync(process.execPath, [PREFLIGHT, '--file', filePath], { encoding: 'utf8' });
  if (r.status !== 0) {
    const detail = (r.stderr || r.stdout || '').trim();
    throw new Error(`前置类型检查失败：${detail}`);
  }
  const pf = JSON.parse(r.stdout);
  if (!pf.pass) {
    throw new Error(`文件类型不支持，已拒绝：${pf.reason || pf.file_name}`);
  }
  return pf;
}

// 解析知识库 ID：必须显式指定（--kb 或 --kb-name），脚本不替用户做选择

function appendTimestamp(name) {
  const ext = path.extname(name);
  const base = name.slice(0, name.length - ext.length);
  const ts = new Date()
    .toISOString()
    .replace(/[-:T]/g, '')
    .slice(0, 14); // YYYYMMDDHHmmss
  return `${base}_${ts}${ext}`;
}

async function main() {
  const args = parseArgs(process.argv);
  await __withRetry(args, async () => {
  const filePath = args.file;
  if (!filePath) {
    console.error('[error] 缺少必需参数 --file <path>');
    process.exit(1);
  }
  if (!fs.existsSync(filePath)) {
    console.error(`[error] 文件不存在：${filePath}`);
    process.exit(1);
  }

  // Step 1: preflight
  log('⏳', '前置类型检查…');
  const pf = runPreflight(filePath);
  log('✅', `类型检查通过：${pf.file_name} (${pf.file_size} 字节, media_type=${pf.media_type})`);

  // Step 2: 解析知识库
  log('⏳', '定位目标知识库…');
  let kbId, folderId = args.folder;
  if (args.path) {
    const r = await resolveKbId(args, { needFolder: true });
    kbId = r.kb_id;
    if (r.folder_id && !folderId) folderId = r.folder_id;
  } else {
    kbId = await resolveKbId(args);
  }

  // Step 3: 重名检查（GATE 3）
  log('⏳', '检查文件名是否重复…');
  const checkBody = {
    params: [{ name: pf.file_name, media_type: pf.media_type }],
    knowledge_base_id: kbId,
  };
  if (folderId) checkBody.folder_id = folderId;
  const dupResp = await call('openapi/wiki/v1/check_repeated_names', checkBody);
  const dupResult = (dupResp.data && dupResp.data.results && dupResp.data.results[0]) || {};
  let fileName = pf.file_name;
  if (dupResult.is_repeated) {
    if (args['cancel-if-dup']) {
      throw new Error(`知识库中已存在同名文件「${pf.file_name}」，按 --cancel-if-dup 取消上传`);
    }
    fileName = appendTimestamp(pf.file_name);
    log('⚠️', `检测到重名，保留两者，文件名改为：${fileName}`);
  }

  // Step 4: create_media
  log('⏳', '创建媒体并获取 COS 凭证…');
  const createBody = {
    file_name: fileName,
    file_size: pf.file_size,
    content_type: pf.content_type,
    knowledge_base_id: kbId,
    file_ext: pf.file_ext,
  };
  if (folderId) createBody.folder_id = folderId;
  const createResp = await call('openapi/wiki/v1/create_media', createBody);
  const { media_id, cos_credential: cred } = createResp.data;
  if (!media_id || !cred) throw new Error('create_media 返回缺少 media_id 或 cos_credential');

  // Step 5: cos-upload（GATE 5，非零即停）
  log('⏳', `上传文件到 COS (${cred.region})…`);
  // V1.0.11 加固：COS 临时凭证经环境变量传给子进程，不再出现在 argv（进程列表中）。
  const cosArgs = [
    COS_UPLOAD,
    '--file', filePath,
    '--bucket', cred.bucket_name,
    '--region', cred.region,
    '--cos-key', cred.cos_key,
    '--content-type', pf.content_type,
    '--start-time', String(cred.start_time),
    '--expired-time', String(cred.expired_time),
    '--timeout', '120000',
  ];
  const cosRun = spawnSync(process.execPath, cosArgs, {
    encoding: 'utf8',
    env: {
      ...process.env,
      IMA_COS_SECRET_ID: cred.secret_id,
      IMA_COS_SECRET_KEY: cred.secret_key,
      IMA_COS_TOKEN: cred.token,
    },
  });
  if (cosRun.status !== 0) {
    const detail = (cosRun.stderr || cosRun.stdout || '').trim();
    throw new Error(`COS 上传失败，已中止入库：${detail}`);
  }
  log('✅', 'COS 上传成功');

  // Step 6: add_knowledge（GATE 2，title 必须等于文件名）
  log('⏳', '写入知识库条目…');
  const addBody = {
    media_type: pf.media_type,
    media_id,
    title: fileName,
    knowledge_base_id: kbId,
    file_info: { cos_key: cred.cos_key, file_size: pf.file_size, file_name: fileName },
  };
  if (folderId) addBody.folder_id = folderId;
  const addResp = await call('openapi/wiki/v1/add_knowledge', addBody);
  const finalMediaId = (addResp.data && addResp.data.media_id) || media_id;

  log('🎉', `上传完成！文件「${fileName}」已成功入库`);
  log('   ', `media_id: ${finalMediaId}`);
  });
}

main().catch((err) => {
  console.error(`[error] ${err.message}`);
  process.exit(1);
});
