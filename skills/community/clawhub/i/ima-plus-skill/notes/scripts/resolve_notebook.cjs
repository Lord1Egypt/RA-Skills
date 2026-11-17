#!/usr/bin/env node
'use strict';

/**
 * resolve_notebook.cjs — 笔记笔记本名 → folder_id 解析器（notes 模块统一入口）
 *
 * 让 AI/用户用笔记本名称代替 folder_id，消除长 ID 幻觉。
 *
 * Usage:
 *   node notes/scripts/resolve_notebook.cjs --path "我的笔记本"
 *   node notes/scripts/resolve_notebook.cjs --name "学习笔记"
 *   node notes/scripts/resolve_notebook.cjs --list          # 列出所有笔记本
 *
 * 输出：{ note_folder_id, note_folder_name }
 */

const path = require('node:path');
const { imaApi } = require(path.join(__dirname, '..', '..', 'ima_api.cjs'));
const { resolveNotePathStr } = require(path.join(__dirname, '..', '..', 'resolve_path.cjs'));
const { parseArgs } = require(path.join(__dirname, '..', '..', '_lib.cjs'));

async function listNotebooks() {
  const raw = await imaApi('openapi/note/v1/list_notebook', { cursor: '0', limit: 20 });
  let json;
  try {
    json = JSON.parse(raw);
  } catch {
    throw new Error(`list_notebook 返回非 JSON：${raw}`);
  }
  if (json.code !== 0) throw new Error(`list_notebook 失败 (code=${json.code}): ${json.msg || ''}`);
  return (json.data && json.data.note_folder_infos) || [];
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.list) {
    const notebooks = await listNotebooks();
    console.log(JSON.stringify(notebooks.map((n) => ({ note_folder_id: n.folder_id, note_folder_name: n.name || n.folder_name })), null, 2));
    return;
  }
  const name = (args.path || args.name || '').trim();
  if (!name) {
    console.error('[error] 缺少参数：--path <笔记本名> 或 --name <笔记本名> 或 --list');
    process.exit(1);
  }
  // 带分层缓存解析（缓存优先，miss 才调 list_notebook；结果持久化，无 TTL）
  const { note_folder_id, note_folder_name } = await resolveNotePathStr(name);
  console.log(JSON.stringify({ note_folder_id, note_folder_name }, null, 2));
}

main().catch((err) => {
  console.error(`[error] ${err.message}`);
  process.exit(1);
});
