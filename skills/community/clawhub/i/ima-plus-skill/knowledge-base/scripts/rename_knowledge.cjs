#!/usr/bin/env node
'use strict';

/**
 * 重命名知识库中的文件或文件夹（封装 openapi/wiki/v1/rename_knowledge）
 *
 * Usage:
 *   node rename_knowledge.cjs --path "我的知识库" --media-id <media_id> --name "新名称"
 *   node rename_knowledge.cjs --kb-name "我的知识库" --media-id <media_id> --name "新名称"
 */

const path = require('node:path');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima_api.cjs'));
const { resolveKbId: __resKb, resolvePathStr: __resPath, withPathRetry: __withRetry } = require(path.join(__dirname, '..', '..', 'resolve_path.cjs'));
const { call, log, parseArgs, resolveKbId } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

// 解析知识库 ID：必须显式指定（--kb 或 --kb-name）

async function main() {
  const args = parseArgs(process.argv);
  await __withRetry(args, async () => {
    if (!args['media-id']) {
      console.error('[error] 缺少必需参数 --media-id <media_id>');
      process.exit(1);
    }
    if (!args.name) {
      console.error('[error] 缺少必需参数 --name <新名称>');
      process.exit(1);
    }

    log('⏳', '定位目标知识库…');
    const kbId = await resolveKbId(args);

    const body = { knowledge_base_id: kbId, media_id: args['media-id'], name: args.name };
    log('⏳', `重命名 media_id=${args['media-id']} → 「${args.name}」…`);
    await call('openapi/wiki/v1/rename_knowledge', body);
    log('✅', `重命名成功：${args['media-id']} → ${args.name}`);
  });
}

main().catch((err) => {
  console.error(`[error] ${err.message}`);
  process.exit(1);
});
