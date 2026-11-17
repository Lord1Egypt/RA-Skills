#!/usr/bin/env node
'use strict';

/**
 * 创建知识库（封装 openapi/wiki/v1/create_knowledge_base）
 *
 * Usage:
 *   node create_knowledge_base.cjs --name "我的知识库" --type 1001
 *   node create_knowledge_base.cjs --name "团队库" --type 1002 --description "资料汇总" --recommended-questions "有哪些文档?,怎么用?"
 *
 * type: 1001=个人, 1002=共享, 1004=订阅（发布到广场）
 */

const path = require('node:path');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima_api.cjs'));
const { call, log, parseArgs } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

async function main() {
  const args = parseArgs(process.argv);
  if (!args.name) { console.error('[error] 缺少必需参数 --name <知识库名称>'); process.exit(1); }
  if (!args.type) { console.error('[error] 缺少必需参数 --type <1001个人|1002共享|1004订阅>'); process.exit(1); }
  const type = Number(args.type);
  if (![1001, 1002, 1004].includes(type)) throw new Error(`--type 必须是 1001/1002/1004，收到 ${args.type}`);

  const body = { name: args.name, type };
  if (args.description) body.description = args.description;
  if (args['cover-url']) body.cover_url = args['cover-url'];
  if (args['recommended-questions']) {
    body.recommended_questions = String(args['recommended-questions']).split(',').map((s) => s.trim()).filter(Boolean);
  }

  log('⏳', `创建知识库「${args.name}」(type=${type})…`);
  const resp = await call('openapi/wiki/v1/create_knowledge_base', body);
  const id = (resp.data && resp.data.id) || '';
  log('✅', `知识库创建成功：id=${id}`);
}

main().catch((err) => { console.error(`[error] ${err.message}`); process.exit(1); });
