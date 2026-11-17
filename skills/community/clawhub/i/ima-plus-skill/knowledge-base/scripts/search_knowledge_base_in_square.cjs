#!/usr/bin/env node
'use strict';

/**
 * 在知识库广场发现/搜索公开知识库（封装 openapi/wiki/v1/search_knowledge_base_in_square）
 * 用于加入知识库前定位目标（返回 kb_id + 名称）。
 *
 * Usage:
 *   node search_knowledge_base_in_square.cjs --question "Python 教程"
 *   node search_knowledge_base_in_square.cjs --question "AI" --limit 20 --cursor "<next_cursor>"
 */

const path = require('node:path');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima_api.cjs'));
const { call, log, parseArgs } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

async function main() {
  const args = parseArgs(process.argv);
  if (!args.question) { console.error('[error] 缺少必需参数 --question <搜索关键词>'); process.exit(1); }
  const body = {
    question: args.question,
    cursor: args.cursor || '',
    limit: Number(args.limit) || 20,
  };
  log('⏳', `在广场搜索「${args.question}」…`);
  const resp = await call('openapi/wiki/v1/search_knowledge_base_in_square', body);
  const data = resp.data || {};
  const items = data.items || [];
  log('✅', `找到 ${items.length} 个公开知识库：`);
  for (const it of items) {
    console.log(`${it.kb_name}\t${it.kb_id}\t成员${it.member_count}\t内容${it.content_count}\t${it.creator}`);
  }
  if (data.next_cursor) log('➡️', `还有更多，翻页用 --cursor ${data.next_cursor}`);
  else log('➡️', '已到末尾');
}

main().catch((err) => { console.error(`[error] ${err.message}`); process.exit(1); });
