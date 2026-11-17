#!/usr/bin/env node
'use strict';

/**
 * 加入知识库（封装 openapi/wiki/v1/join_knowledge）
 * 通常通过 search_knowledge_base_in_square 找到目标知识库 ID 后再加入。
 *
 * Usage:
 *   node join_knowledge.cjs --path "知识库名称" --name "知识库名称"
 */

const path = require('node:path');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima_api.cjs'));
const { resolveKbId: __resKb, withPathRetry: __withRetry } = require(path.join(__dirname, '..', '..', 'resolve_path.cjs'));
const { call, log, parseArgs } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

async function main() {
  const args = parseArgs(process.argv);
  await __withRetry(args, async () => {
    if (!args.kb && !args['kb-name'] && !args.path) {
      console.error('[error] 缺少必需参数：--kb <id> 或 --kb-name <知识库名称> 或 --path <自然语言路径>');
      process.exit(1);
    }
    if (!args.name) { console.error('[error] 缺少必需参数 --name <知识库名称>'); process.exit(1); }
    let kbId;
    if (args.kb) kbId = args.kb;
    else {
      const r = await __resKb(args);
      kbId = (r && typeof r === 'object') ? r.kb_id : r;
    }
    const body = { knowledge_base_id: kbId, name: args.name };
    log('⏳', `加入知识库「${args.name}」…`);
    await call('openapi/wiki/v1/join_knowledge', body);
    log('✅', `已加入知识库：${args.name}`);
  });
}

main().catch((err) => { console.error(`[error] ${err.message}`); process.exit(1); });
