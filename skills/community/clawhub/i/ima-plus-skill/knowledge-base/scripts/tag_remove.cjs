#!/usr/bin/env node
'use strict';

/**
 * 从文件移除标签（封装 openapi/wiki/v1/tag_remove）；仅解除关联，不删除标签本身。
 *
 * Usage:
 *   node tag_remove.cjs --path "我的知识库" --media-id <media_id> --tag-name "重要"
 */

const path = require('node:path');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima_api.cjs'));
const { resolveKbId: __resKb, resolvePathStr: __resPath, withPathRetry: __withRetry } = require(path.join(__dirname, '..', '..', 'resolve_path.cjs'));
const { call, log, parseArgs, resolveKbId } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

async function main() {
  const args = parseArgs(process.argv);
  await __withRetry(args, async () => {
    if (!args['media-id']) { console.error('[error] 缺少必需参数 --media-id <media_id>'); process.exit(1); }
    if (!args['tag-name']) { console.error('[error] 缺少必需参数 --tag-name <标签名>'); process.exit(1); }
    const kbId = await resolveKbId(args);
    const body = { knowledge_base_id: kbId, item_id: args['media-id'], tag_name: args['tag-name'] };
    log('⏳', `从 media_id=${args['media-id']} 移除标签「${args['tag-name']}」…`);
    await call('openapi/wiki/v1/tag_remove', body);
    log('✅', `标签已移除：${args['tag-name']}`);
  });
}

main().catch((err) => { console.error(`[error] ${err.message}`); process.exit(1); });
