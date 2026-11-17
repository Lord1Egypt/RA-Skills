#!/usr/bin/env node
'use strict';

/**
 * 批量更新知识条目的访问权限状态（封装 openapi/wiki/v1/update_knowledge_access_status）
 *
 * Usage:
 *   node update_knowledge_access_status.cjs --path "我的知识库" --media-id <media_id> --access-status 3
 *   node update_knowledge_access_status.cjs --path "我的知识库" --media-id id1,id2,id3 --access-status 2
 *
 * access_status: 1-不可查看不可导出, 2-可查看不可导出, 3-可查看可导出
 */

const path = require('node:path');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima_api.cjs'));
const { resolveKbId: __resKb, resolvePathStr: __resPath, withPathRetry: __withRetry } = require(path.join(__dirname, '..', '..', 'resolve_path.cjs'));
const { call, log, parseArgs, resolveKbId } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

async function main() {
  const args = parseArgs(process.argv);
  await __withRetry(args, async () => {
    if (!args['media-id']) { console.error('[error] 缺少必需参数 --media-id <media_id>（多个用逗号分隔，最多10个）'); process.exit(1); }
    if (args['access-status'] === undefined) { console.error('[error] 缺少必需参数 --access-status <1|2|3>'); process.exit(1); }
    const accessStatus = Number(args['access-status']);
    if (![1, 2, 3].includes(accessStatus)) throw new Error(`--access-status 必须是 1/2/3，收到 ${args['access-status']}`);
    const mediaIds = String(args['media-id']).split(',').map((s) => s.trim()).filter(Boolean);
    if (mediaIds.length === 0) { console.error('[error] --media-id 为空'); process.exit(1); }
    if (mediaIds.length > 10) { console.error('[error] infos 最多 10 个'); process.exit(1); }
    const kbId = await resolveKbId(args);
    const body = {
      knowledge_base_id: kbId,
      infos: mediaIds.map((id) => ({ media_id: id })),
      access_status: accessStatus,
    };
    log('⏳', `更新 ${mediaIds.length} 个条目的访问状态 → ${accessStatus}…`);
    await call('openapi/wiki/v1/update_knowledge_access_status', body);
    log('✅', '访问状态更新成功');
  });
}

main().catch((err) => { console.error(`[error] ${err.message}`); process.exit(1); });
