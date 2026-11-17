#!/usr/bin/env node
'use strict';

/**
 * 重命名标签（封装 openapi/wiki/v1/tag_rename）；所有打了旧标签的文件自动迁移到新名。
 * ⚠️ 若新名已存在会自动合并（旧标签关联并入新标签并删除旧标签），调用前应确认。
 *
 * Usage:
 *   node tag_rename.cjs --path "我的知识库" --old-tag-name "旧名" --new-tag-name "新名"
 */

const path = require('node:path');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima_api.cjs'));
const { resolveKbId: __resKb, resolvePathStr: __resPath, withPathRetry: __withRetry } = require(path.join(__dirname, '..', '..', 'resolve_path.cjs'));
const { call, log, parseArgs, resolveKbId } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

async function main() {
  const args = parseArgs(process.argv);
  await __withRetry(args, async () => {
    if (!args['old-tag-name']) { console.error('[error] 缺少必需参数 --old-tag-name <旧标签名>'); process.exit(1); }
    if (!args['new-tag-name']) { console.error('[error] 缺少必需参数 --new-tag-name <新标签名>'); process.exit(1); }
    const kbId = await resolveKbId(args);
    const body = { knowledge_base_id: kbId, old_tag_name: args['old-tag-name'], new_tag_name: args['new-tag-name'] };
    log('⏳', `重命名标签「${args['old-tag-name']}」→「${args['new-tag-name']}」…`);
    await call('openapi/wiki/v1/tag_rename', body);
    log('✅', `标签已重命名（若新名已存在则自动合并）`);
  });
}

main().catch((err) => { console.error(`[error] ${err.message}`); process.exit(1); });
