#!/usr/bin/env node
'use strict';

/**
 * 修改知识库权限（封装 openapi/wiki/v1/update_knowledge_base_permission）
 * 按提供的字段自动推导 update_fields（1-导出状态 2-加入类型）。
 *
 * Usage:
 *   node update_knowledge_base_permission.cjs --path "我的知识库" --visible-export-status 3
 *   node update_knowledge_base_permission.cjs --kb-name "我的知识库" --join-type 1
 *
 * visible_export_status: 1-不可查看不可导出, 2-可查看不可导出, 3-可查看可导出
 * join_type:            1-直接加入, 2-管理员批准加入, 3-付费加入
 */

const path = require('node:path');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima_api.cjs'));
const { resolveKbId: __resKb, resolvePathStr: __resPath, withPathRetry: __withRetry } = require(path.join(__dirname, '..', '..', 'resolve_path.cjs'));
const { call, log, parseArgs, resolveKbId } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

async function main() {
  const args = parseArgs(process.argv);
  await __withRetry(args, async () => {
    const kbId = await resolveKbId(args);
    const body = { id: kbId, update_fields: [] };
    if (args.name) body.name = args.name;
    if (args['visible-export-status'] !== undefined) {
      body.update_fields.push(1);
      body.visible_export_status = Number(args['visible-export-status']);
    }
    if (args['join-type'] !== undefined) {
      body.update_fields.push(2);
      body.join_type = Number(args['join-type']);
    }
    if (args['update-fields']) {
      body.update_fields = String(args['update-fields']).split(',').map((s) => Number(s.trim())).filter((n) => [1, 2].includes(n));
    }
    if (!body.update_fields.length) {
      console.error('[error] 至少提供一个要更新的权限字段：--visible-export-status / --join-type');
      process.exit(1);
    }
    log('⏳', `更新知识库 ${kbId} 权限字段 [${body.update_fields.join(',')}]…`);
    await call('openapi/wiki/v1/update_knowledge_base_permission', body);
    log('✅', '知识库权限更新成功');
  });
}

main().catch((err) => { console.error(`[error] ${err.message}`); process.exit(1); });
