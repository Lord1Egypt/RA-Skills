#!/usr/bin/env node
'use strict';

/**
 * 置顶 / 取消置顶知识库内的内容（封装 openapi/wiki/v1/set_knowledge_top）
 * 注意：不适用于名称为"某某的知识库"的个人知识库。
 *
 * Usage:
 *   node set_knowledge_top.cjs --path "我的知识库" --media-id <media_id> --is-top true
 *   node set_knowledge_top.cjs --kb-name "我的知识库" --media-id <media_id> --is-top false
 */

const path = require('node:path');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima_api.cjs'));
const { resolveKbId: __resKb, resolvePathStr: __resPath, withPathRetry: __withRetry } = require(path.join(__dirname, '..', '..', 'resolve_path.cjs'));
const { call, log, parseArgs, resolveKbId } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

async function main() {
  const args = parseArgs(process.argv);
  await __withRetry(args, async () => {
    if (!args['media-id']) { console.error('[error] 缺少必需参数 --media-id <media_id>'); process.exit(1); }
    if (args['is-top'] === undefined) { console.error('[error] 缺少必需参数 --is-top <true|false>'); process.exit(1); }
    const isTop = args['is-top'] === 'true' || args['is-top'] === '1';
    const kbId = await resolveKbId(args);
    const body = { knowledge_base_id: kbId, media_id: args['media-id'], is_top: isTop };
    log('⏳', `设置置顶 media_id=${args['media-id']} → is_top=${isTop}…`);
    await call('openapi/wiki/v1/set_knowledge_top', body);
    log('✅', `置顶状态已更新：${isTop ? '已置顶' : '已取消置顶'}`);
  });
}

main().catch((err) => { console.error(`[error] ${err.message}`); process.exit(1); });
