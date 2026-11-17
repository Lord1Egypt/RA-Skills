#!/usr/bin/env node
'use strict';

/**
 * 在 IMA 知识库里创建文件夹（封装 openapi/wiki/v1/create_folder）
 *
 * Usage:
 *   node create_folder.cjs --path "我的知识库" --name "新文件夹"
 *   node create_folder.cjs --kb-name "我的知识库" --name "新文件夹"
 *   node create_folder.cjs --path "我的知识库/父文件夹" --name "子文件夹"
 *
 * 必须显式指定目标知识库（--kb 或 --kb-name），脚本不替用户选库。
 */

const path = require('node:path');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima_api.cjs'));
const { resolveKbId: __resKb, resolvePathStr: __resPath, withPathRetry: __withRetry } = require(path.join(__dirname, '..', '..', 'resolve_path.cjs'));
const { call, log, parseArgs, resolveKbId } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

// 解析知识库 ID：必须显式指定（--kb 或 --kb-name）

async function main() {
  const args = parseArgs(process.argv);
  await __withRetry(args, async () => {
    if (!args.name) {
      console.error('[error] 缺少必需参数 --name <文件夹名称>');
      process.exit(1);
    }
    const folderName = args.name;
    let parentFolderId = args.folder;

    log('⏳', '定位目标知识库…');
    // --path "知识库名/父夹路径" 时：父夹由路径解析得出
    let kbId;
    if (args.path) {
      const r = await resolveKbId(args, { needFolder: true });
      kbId = r.kb_id;
      if (r.folder_id && !parentFolderId) parentFolderId = r.folder_id;
    } else {
      kbId = await resolveKbId(args);
    }

    const body = { knowledge_base_id: kbId, name: folderName };
    if (parentFolderId) body.folder_id = parentFolderId;

    log('⏳', `在知识库 ${kbId} 创建文件夹「${folderName}」…`);
    const resp = await call('openapi/wiki/v1/create_folder', body);
    const mediaId = (resp.data && resp.data.media_id) || '';
    log('✅', `文件夹创建成功：media_id=${mediaId}（即 folder_id）`);
  });
}

main().catch((err) => {
  console.error(`[error] ${err.message}`);
  process.exit(1);
});
