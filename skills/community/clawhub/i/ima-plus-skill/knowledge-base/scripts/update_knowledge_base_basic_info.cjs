#!/usr/bin/env node
'use strict';

/**
 * 修改知识库基本信息（封装 openapi/wiki/v1/update_knowledge_base_basic_info）
 * 按提供的字段自动推导 update_fields（1-名称 2-封面 3-简介 4-推荐问题）。
 *
 * Usage:
 *   node update_knowledge_base_basic_info.cjs --path "我的知识库" --name "新名称"
 *   node update_knowledge_base_basic_info.cjs --kb-name "我的知识库" --description "新简介" --recommended-questions "问题1,问题2"
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
    if (args['current-name']) body.current_name = args['current-name'];
    if (args.name) { body.update_fields.push(1); body.name = args.name; }
    if (args['cover-url']) { body.update_fields.push(2); body.cover_url = args['cover-url']; }
    if (args.description) { body.update_fields.push(3); body.description = args.description; }
    if (args['recommended-questions']) {
      body.update_fields.push(4);
      body.recommended_questions = String(args['recommended-questions']).split(',').map((s) => s.trim()).filter(Boolean);
    }
    if (args['update-fields']) {
      body.update_fields = String(args['update-fields']).split(',').map((s) => Number(s.trim())).filter((n) => [1, 2, 3, 4].includes(n));
    }
    if (!body.update_fields.length) {
      console.error('[error] 至少提供一个要更新的字段：--name / --cover-url / --description / --recommended-questions');
      process.exit(1);
    }
    log('⏳', `更新知识库 ${kbId} 字段 [${body.update_fields.join(',')}]…`);
    await call('openapi/wiki/v1/update_knowledge_base_basic_info', body);
    log('✅', '知识库信息更新成功');
  });
}

main().catch((err) => { console.error(`[error] ${err.message}`); process.exit(1); });
