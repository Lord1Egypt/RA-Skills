#!/usr/bin/env node
'use strict';

/**
 * 删除标签（封装 openapi/wiki/v1/tag_delete）；所有文件上的该标签关联自动解除。
 * ⚠️ 不可逆操作，调用前应显式向用户确认。
 *
 * Usage:
 *   node tag_delete.cjs --path "我的知识库" --tag-name "待删标签"
 */

const path = require('node:path');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima_api.cjs'));
const { resolveKbId: __resKb, resolvePathStr: __resPath, withPathRetry: __withRetry } = require(path.join(__dirname, '..', '..', 'resolve_path.cjs'));
const { call, log, parseArgs, resolveKbId } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

async function main() {
  const args = parseArgs(process.argv);
  await __withRetry(args, async () => {
    if (!args['tag-name']) { console.error('[error] 缺少必需参数 --tag-name <标签名>'); process.exit(1); }
    const kbId = await resolveKbId(args);
    const body = { knowledge_base_id: kbId, tag_name: args['tag-name'] };
    log('⏳', `删除标签「${args['tag-name']}」（关联自动解除）…`);
    await call('openapi/wiki/v1/tag_delete', body);
    log('✅', `标签已删除：${args['tag-name']}`);
  });
}

main().catch((err) => { console.error(`[error] ${err.message}`); process.exit(1); });
